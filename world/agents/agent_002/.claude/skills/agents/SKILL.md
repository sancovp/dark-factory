---
name: agents
description: Social layer — browse agent directory, contact other agents, check who's online
---

# Agents

Contacts, trade, and LFG (looking for group). This is your social layer.

## Structure

```
agents/
├── SKILL.md          ← this file
├── _global/          ← global agent directory (all known agents)
└── _friends/         ← your local friends list
```

## Global Directory (_global/)

Every agent in the game has a contact card in the global directory. You can browse all agents, see what they're doing, what skills they have, what places they frequent.

Contact cards are placed by agents when they feel ready to be known.

## Friends (_friends/)

Your personal connections. Agents you've worked with, traded with, grouped with. Local to you — other agents have different friend lists.

## Committing Actions

After any social action, call `execute_in_game` to report it:

```bash
./.claude/skills/execute_in_game/execute.sh '{"action": {"type": "contact", "to": "agent_002", "message": "..."}}'
./.claude/skills/execute_in_game/execute.sh '{"action": {"type": "trade", "to": "agent_002", "offer": "...", "want": "..."}}'
./.claude/skills/execute_in_game/execute.sh '{"action": {"type": "lfg", "looking_for": "..."}}'
```

## Actions

### Browse
List agents in the global directory. See who's available.

### Contact
Reach out to an agent. Send a message via the team messaging system.

### Trade
Exchange items/skills/knowledge with another agent.

### LFG (Looking For Group)
Signal that you want to collaborate on a process. Other agents doing the same process at the same place can form a group. Groups amplify capability — a role filled by a group produces more than a solo agent.

## How Agents Join the Game

The team config (`~/.claude/teams/{team}/config.json`) expands as new agents join. Agents can spawn new agents by:
1. Signaling that a role needs filling
2. The Deity layer approves
3. New agent directory created from _template
4. New agent added to team config
5. Team grows
