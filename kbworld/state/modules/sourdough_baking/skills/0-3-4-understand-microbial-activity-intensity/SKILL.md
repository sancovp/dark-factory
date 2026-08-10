---
name: 0.3.4-understand-microbial_activity_intensity
description: "[0.3.4] Combined metabolic activity level of wild_yeast and lactobacillus populations during fermentation, representin"
---

# understand-microbial_activity_intensity

**CALL NUMBER:** `deep_fermentation.microbial_activity_intensity : sourdough_baking(1)`
**DEFINITION:** Combined metabolic activity level of wild_yeast and lactobacillus populations during fermentation, representing the aggregate fermentation capacity of the sourdough system.

Invoke this skill to understand `microbial_activity_intensity` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `?`
- **flavor_complexity** (d3): The depth and nuance of sourdough taste arising from multiple organic acids, esters, and alcohols produced during extended fermentation, creating tangy and complex notes.

### from `deep_fermentation`
- **dough_expansion_velocity** (d1): Rate at which dough volume increases due to carbon_dioxide retention in the gluten network, expressed as percentage increase per hour during active fermentation.
- **fermentation_vigor** (d1): Intensity and rate of the combined microbial fermentation process in sourdough, driven by wild_yeast gas production and lactobacillus acid generation, determining dough rise speed and flavor development timing.
- **peak_fermentation_rate** (d1): Maximum intensity reached during the fermentation cycle when wild_yeast activity is highest, marking the most vigorous phase of gas production.
- **carbon_dioxide** (d2): Gaseous byproduct of wild_yeast fermentation that provides dough rise and open crumb structure in sourdough bread.
- **organic_acids** (d2): Carbon-chain acids produced by lactobacillus metabolism including lactic_acid and acetic_acid that determine sourness_level and contribute to flavor_complexity.

### from `sourdough_baking`
- **sourness_level** (d3): Intensity of acidic tang from lactobacillus fermentation ranging from mild to pronounced

## CONSUMERS (what needs this)
`acid_generation_rate`, `gas_production_rate`, `starter_vitality`

---
*Projected from the `sourdough baking` KB (373 concepts / 213 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*

_(leaf — this is an actual skill.)_
