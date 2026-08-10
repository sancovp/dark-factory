---
name: 0.3.1-understand-fermentation_vigor
description: "[0.3.1] Intensity and rate of the combined microbial fermentation process in sourdough, driven by wild_yeast gas produ"
---

# understand-fermentation_vigor

**CALL NUMBER:** `deep_fermentation.fermentation_vigor : sourdough_baking(1)`
**DEFINITION:** Intensity and rate of the combined microbial fermentation process in sourdough, driven by wild_yeast gas production and lactobacillus acid generation, determining dough rise speed and flavor development timing.

Invoke this skill to understand `fermentation_vigor` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `?`
- **flavor_complexity** (d2): The depth and nuance of sourdough taste arising from multiple organic acids, esters, and alcohols produced during extended fermentation, creating tangy and complex notes.

### from `deep_fermentation`
- **carbon_dioxide** (d1): Gaseous byproduct of wild_yeast fermentation that provides dough rise and open crumb structure in sourdough bread.
- **organic_acids** (d1): Carbon-chain acids produced by lactobacillus metabolism including lactic_acid and acetic_acid that determine sourness_level and contribute to flavor_complexity.

### from `sourdough_baking`
- **sourness_level** (d2): Intensity of acidic tang from lactobacillus fermentation ranging from mild to pronounced

## CONSUMERS (what needs this)
`as_vigor_level`, `fermentation_onset_timing`, `microbial_activity_intensity`, `peak_fermentation_rate`, `starter_vitality`, `temperature_coefficient`, `wild_yeast`

---
*Projected from the `sourdough baking` KB (373 concepts / 213 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*

_(leaf — this is an actual skill.)_
