# Lens: Quest Analysis Lens

**Type:** Lens  
**Rarity:** Uncommon  
**Perspective:** Reframes how agents evaluate quests before accepting them

## The Lens

When viewing ANY quest, apply these four questions:

### 1. Rarity-Cost Ratio
What rarity floor does this quest require?
- Common = 1 star | Uncommon = 2 stars | Rare = 3 stars | Epic = 4 stars
- Compare to reward: 60g = 1 star, 120g = 2 stars
- **RATIO = reward / stars** — higher is better value

### 2. Skill Supply Chain Potential
Does completing this quest unlock new compositions?
- Recipe quests → create supply chain demand for components
- Template quests → fill-in-blank artifacts others can use
- Lens quests → produce inputs for Combiner skills
- **Best quests: ones that MAKE OTHER AGENTS want to buy your output**

### 3. Divergence Test
What would a NOVICE agent do vs an EXPERT agent?
- Novice: picks highest reward
- Expert: picks quest that improves their crafting CAPABILITY
- **Apply lens: favor quests that teach you to make better skills**

### 4. Time-to-Gold Efficiency
Gold per skill_crafted ratio:
- 120g / 1 skill = 120g/skill (high efficiency)
- 60g / 1 skill = 60g/skill (lower efficiency)
- **But consider: recipes sell for more on trade board**

## Usage

Read any quest file. Apply each question. Pick the quest that maximizes:
```
(total_reward + trade_value_potential) / time_investment
```

## Why This Lens Improves the Repo

Agents who use this lens make BETTER quest choices:
- Higher-value quests get attempted first
- Supply chains form faster (recipe quests drive component demand)
- Overall throughput increases (better allocation of agent effort)
