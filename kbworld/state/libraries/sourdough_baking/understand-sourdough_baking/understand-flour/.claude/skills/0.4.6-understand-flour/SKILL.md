---
name: 0.4.6-understand-flour
description: [0.4.6] Ground grain (typically wheat) used as the carbohydrate base for sourdough, providing starch, protein for glut
---

# understand-flour

**CALL NUMBER:** `sourdough_baking.flour`
**DEFINITION:** Ground grain (typically wheat) used as the carbohydrate base for sourdough, providing starch, protein for gluten, and nutrients for the starter ecosystem.

Invoke this skill to understand `flour` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `?`
- **mixing** (d2): Combining flour, water, and other ingredients to form a cohesive dough, developing initial gluten structure through mechanical stirring or hand work.

### from `sourdough_baking`
- **autolyse** (d1): Initial rest period after mixing flour and water where gluten develops without kneading, improving dough extensibility and reducing mixing time.
- **bread_flour** (d1): High-protein wheat flour (12-14%) providing strong gluten network ideal for open crumb sourdough structure.
- **enriched_sourdough** (d1): Dough containing eggs, butter, or sugar alongside the sourdough culture
- **flour_type** (d1): Variety of grain including whole_wheat, rye, spelt, or mixed with different protein contents
- **gluten_development** (d1): Process of hydrating and aligning gluten proteins through mixing, folding, or autolyse to create strong extensible dough.
- **water** (d1): Filtered water used to hydrate flour and feed the starter culture; temperature affects fermentation speed and dough behavior.
- **enzymatic_activity** (d2): Natural enzyme breakdown of starches to sugars feeding fermentation microbes
- **hydration_ratio** (d2): Percentage of water relative to flour weight determining dough consistency and crumb openness
- **rye_sourdough** (d2): Bread with significant rye flour content requiring adjusted hydration and fermentation
- **whole_wheat_sourdough** (d2): Bread using entire grain flour with higher nutrient content and denser texture
- **bread_volume** (d2): Total size and height of finished loaf indicating proper fermentation and oven spring
- **crumb_structure** (d2): Internal architecture of bread defined by bubble size, distribution, and tenderness
- **dough_consistency** (d2): Viscosity and handling quality from soft and extensible to firm and tight
- **lactobacillus** (d3): Bacterial strains producing lactic and acetic acids that create sourdough tanginess
- **acetic_acid** (d4): Sharp sour acid produced by lactobacillus in presence of oxygen creating tangy flavor
- **lactic_acid** (d4): Milder sour acid produced by lactobacillus contributing to bread tanginess
- **sourness_level** (d4): Intensity of acidic tang from lactobacillus fermentation ranging from mild to pronounced

## CONSUMERS (what needs this)
`salt`

---
*Projected from the `sourdough baking` KB (298 concepts / 165 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*

_(leaf — this is an actual skill.)_
