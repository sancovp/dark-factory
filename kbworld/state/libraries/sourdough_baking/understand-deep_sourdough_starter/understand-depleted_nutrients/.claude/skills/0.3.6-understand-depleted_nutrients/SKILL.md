---
name: 0.3.6-understand-depleted_nutrients
description: [0.3.6] Exhausted flour sugars and starches in starter following active fermentation, triggering dormancy as microbial
---

# understand-depleted_nutrients

**CALL NUMBER:** `deep_sourdough_starter.depleted_nutrients : sourdough_baking(6), deep_fermentation(1)`
**DEFINITION:** Exhausted flour sugars and starches in starter following active fermentation, triggering dormancy as microbial food source is consumed.

Invoke this skill to understand `depleted_nutrients` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `?`
- **fermentation_byproducts** (d2): Compounds produced by microbial fermentation including carbon dioxide for dough rise, lactic and acetic acids for sour flavor, and alcohols for aroma.
- **flavor_complexity** (d2): The depth and nuance of sourdough taste arising from multiple organic acids, esters, and alcohols produced during extended fermentation, creating tangy and complex notes.

### from `deep_fermentation`
- **fermentation_vigor** (d3): Intensity and rate of the combined microbial fermentation process in sourdough, driven by wild_yeast gas production and lactobacillus acid generation, determining dough rise speed and flavor development timing.

### from `sourdough_baking`
- **fermentation** (d1): Metabolic process where microbes convert sugars to CO2 for rise and acids for sour flavor
- **acetic_acid** (d2): Sharp sour acid produced by lactobacillus in presence of oxygen creating tangy flavor
- **lactic_acid** (d2): Milder sour acid produced by lactobacillus contributing to bread tanginess
- **lactobacillus** (d2): Bacterial strains producing lactic and acetic acids that create sourdough tanginess
- **sourness_level** (d2): Intensity of acidic tang from lactobacillus fermentation ranging from mild to pronounced
- **wild_yeast** (d2): Naturally occurring yeast strains captured from flour and the environment that ferment dough, providing rise without commercial yeast.

## CONSUMERS (what needs this)
`dormant_starter`

---
*Projected from the `sourdough baking` KB (298 concepts / 165 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*

_(leaf — this is an actual skill.)_
