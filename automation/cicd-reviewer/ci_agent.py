#!/usr/bin/env python3
"""CICD Reviewer — headless heaven review agent (one-shot, CI).

Runs inside the CI container. Its process cwd MUST be the cicd_aios AIOS directory
(the entrypoint chdir's there) so heaven-framework's resolve_devdirs auto-loads the
AIOS's .claude/rules + .claude/skills into the system prompt. The repo under review is
checked out at /repo (its own git repo); the agent operates on it via bash `-C /repo`.

Pattern mirrors integration/observatory-sdna/container/grug_agent.py (BaseHeavenAgent +
UnifiedChat + History, tools=[BashTool], provider=ANTHROPIC, model=MiniMax-M3). MiniMax
is auto-selected by unified_chat.py when model starts with "minimax" (needs MINIMAX_API_KEY).

Env:
  MODE               review | pr | harvest   (which task to run)
  REPO_DIR           checked-out repo path (default /repo)
  GITHUB_REPOSITORY  owner/name
  PR_NUMBER          (review mode) the PR to review
  BASE_REF HEAD_REF  branch refs
  MINIMAX_API_KEY    model credential (required)
  GITHUB_TOKEN       for gh (required for posting)
  HEAVEN_DATA_DIR    heaven state dir (required by heaven; fresh in container)
"""
import asyncio
import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s cicd_reviewer: %(message)s"
)
log = logging.getLogger("cicd_reviewer")

BASE_SYSTEM_PROMPT = (
    "You are running as the CICD Reviewer in a CI container. Your full identity, rules, "
    "and skills are provided in the <DEVDIR_CONTEXT> and <AVAILABLE_SKILLS> sections that "
    "follow — read them and follow them exactly. Use your BashTool to inspect the repo at "
    "/repo (always with an explicit path, e.g. `git -C /repo ...`) and to post results with "
    "`gh`. When the deliverable is produced, end your final message with DONE."
)


def _review_prompt(repo, gh_repo, pr, base, head):
    return (
        f"MODE=review. Review pull request #{pr} on {gh_repo}: head `{head}` against base "
        f"`{base}`. The repo is checked out at {repo}. Follow the `review-pr-diff` skill: read "
        f"the diff, find real correctness/security/contract issues per your review-discipline "
        f"rule (cite path:line, trace each to an exact symptom, drop vague ones), and post your "
        f"review with `gh pr review {pr} --repo {gh_repo}` (--approve if clean, --request-changes "
        f"if there are real blocking findings, else --comment). End with DONE."
    )


def _pr_prompt(repo, gh_repo, head):
    return (
        f"MODE=pr. Branch `{head}` was pushed to {gh_repo} with no open PR. The repo is checked "
        f"out at {repo}. Follow the `open-pr-for-branch` skill: find the default branch, summarize "
        f"what this branch changes against it from the actual diff, check no PR already exists for "
        f"`{head}`, then open one with `gh pr create --repo {gh_repo} --head {head}` giving it a "
        f"real title and body. Print the PR URL. End with DONE."
    )


def _harvest_prompt(repo, gh_repo):
    return (
        f"MODE=harvest. You are running your scheduled rule-harvest over your own past reviews "
        f"on {gh_repo}. The repo is checked out at {repo}. Follow the `harvest-rules-from-reviews` "
        f"skill EXACTLY: gather your recent posted reviews with gh, read your current rules, and "
        f"look for a RECURRING finding class (>=2 distinct reviews) not already covered. Either "
        f"(a) author ONE new rule-candidate file under "
        f"automation/cicd-reviewer/cicd_aios/.claude/rules/ on a cicd-rules/<slug> branch and "
        f"open a PR for it (the maintainer's merge is the approval gate — never approve or merge "
        f"it yourself), or (b) if nothing recurs or it is already covered, add nothing and say "
        f"so plainly. Your ONLY tool is bash: write the rule file with a quoted heredoc "
        f"(cat > path <<'EOF' ... EOF). Never call WriteBlockReportTool unless you are truly "
        f"blocked — it HALTS the run; it is not a progress note. End with DONE."
    )


def build_agent():
    from heaven_base import BaseHeavenAgent, HeavenAgentConfig, UnifiedChat, ProviderEnum
    from heaven_base.memory.history import History
    from heaven_base.tools import BashTool

    config = HeavenAgentConfig(
        name="cicd_reviewer",
        system_prompt=BASE_SYSTEM_PROMPT,
        tools=[BashTool],
        provider=ProviderEnum.ANTHROPIC,
        model=os.environ.get("CICD_MODEL", "MiniMax-M3"),
        temperature=0.3,
        max_tokens=8000,
        use_uni_api=False,
        enable_compaction=True,
    )
    # max_tool_calls: a real multi-file code review reads the diff, opens
    # context files, and posts — 40 starved the reviewer on large PRs
    # (found 2026-08-10: exhausted mid-read on a ~1400-line diff). Raising a
    # REVIEWER's READ budget is not gate-softening — it makes the gate MORE
    # able to catch things; the acceptance bar (real findings, cite path:line)
    # is unchanged. Overridable via CICD_MAX_TOOL_CALLS.
    return BaseHeavenAgent(
        config, UnifiedChat, history=History(messages=[]), adk=False,
        max_tool_calls=int(os.environ.get("CICD_MAX_TOOL_CALLS", "90"))
    )


def extract_text(result):
    if not isinstance(result, dict):
        return str(result)
    if result.get("prepared_message"):
        return result["prepared_message"]
    hist = result.get("history")
    if hist is not None and getattr(hist, "messages", None):
        for msg in reversed(hist.messages):
            if msg.__class__.__name__ == "AIMessage" and getattr(msg, "content", None):
                return msg.content if isinstance(msg.content, str) else str(msg.content)
    return ""


def main():
    mode = os.environ.get("MODE", "").strip().lower()
    repo = os.environ.get("REPO_DIR", "/repo")
    gh_repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not os.environ.get("MINIMAX_API_KEY"):
        sys.exit("FATAL: MINIMAX_API_KEY is not set — the review agent has no model credential.")

    if mode == "review":
        prompt = _review_prompt(
            repo, gh_repo, os.environ.get("PR_NUMBER", ""),
            os.environ.get("BASE_REF", ""), os.environ.get("HEAD_REF", ""),
        )
    elif mode == "pr":
        prompt = _pr_prompt(repo, gh_repo, os.environ.get("HEAD_REF", ""))
    elif mode == "harvest":
        prompt = _harvest_prompt(repo, gh_repo)
    else:
        sys.exit(f"FATAL: MODE must be 'review', 'pr' or 'harvest', got {mode!r}")

    # Deployed-fork extension (2026-08-10, upstreamable): the caller may scope
    # the task — e.g. a state-only factory-round PR must NOT be reviewed by
    # paging its enormous raw diff. A precise instruction, not a raised limit.
    extra = os.environ.get("REVIEW_CONTEXT", "").strip()
    if extra:
        prompt += "\n\nSCOPE NOTE FROM THE PIPELINE: " + extra

    log.info("mode=%s repo=%s gh_repo=%s model=%s cwd=%s",
             mode, repo, gh_repo, os.environ.get("CICD_MODEL", "MiniMax-M3"), os.getcwd())
    agent = build_agent()
    log.info("agent built; running review loop (max_tool_calls=40)")
    result = asyncio.run(agent.run(prompt=prompt))
    text = extract_text(result)
    print("=== CICD Reviewer output ===")
    print(text)
    if "DONE" not in (text or ""):
        # The agent did not signal completion — surface as failure so CI is not silently green.
        log.error("agent did not emit DONE — run incomplete")
        sys.exit("FATAL: agent did not emit DONE — treating run as incomplete.")
    log.info("review run complete")


if __name__ == "__main__":
    main()
