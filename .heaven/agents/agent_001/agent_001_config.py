"""dark-factory roster entry — the dispatch/Automations ROSTER shape from
HEAVEN-DOTDIR-SPEC.md §3.1 (the spec's own minimax_default example). NOTE:
this is the roster OM/heaven can talk to — the factory's runtime constructs
its own richer prompts (factory/wos_team.py); this stub does not replace them.
D4 loader bug (spec §3.1): nested agent_config loads via direct import only
until the use_hermes fix lands."""
from heaven_base.baseheavenagent import HeavenAgentConfig
from heaven_base.unified_chat import ProviderEnum

agent_config = HeavenAgentConfig(
    name="agent_001",
    system_prompt="""A World of Skillcraft player embodied in world/agents/agent_001. Crafts, tests, trades skills; quests; audits the economy.""",
    tools=[],
    provider=ProviderEnum.ANTHROPIC,
    model="MiniMax-M2.7-highspeed",
    temperature=0.7, max_tokens=8000,
)
