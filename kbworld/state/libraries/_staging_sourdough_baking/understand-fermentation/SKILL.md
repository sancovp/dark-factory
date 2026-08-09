# understand-fermentation

**CALL NUMBER:** `sourdough_baking.fermentation : deep_fermentation(1)`
**DEFINITION:** Metabolic process where microbes convert sugars to CO2 for rise and acids for sour flavor

Invoke this skill to understand `fermentation` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `?`
- **fermentation_byproducts** (d1): Compounds produced by microbial fermentation including carbon dioxide for dough rise, lactic and acetic acids for sour flavor, and alcohols for aroma.
- **flavor_complexity** (d1): The depth and nuance of sourdough taste arising from multiple organic acids, esters, and alcohols produced during extended fermentation, creating tangy and complex notes.

### from `deep_fermentation`
- **fermentation_vigor** (d2): Intensity and rate of the combined microbial fermentation process in sourdough, driven by wild_yeast gas production and lactobacillus acid generation, determining dough rise speed and flavor development timing.

### from `sourdough_baking`
- **acetic_acid** (d1): Sharp sour acid produced by lactobacillus in presence of oxygen creating tangy flavor
- **lactic_acid** (d1): Milder sour acid produced by lactobacillus contributing to bread tanginess
- **lactobacillus** (d1): Bacterial strains producing lactic and acetic acids that create sourdough tanginess
- **sourness_level** (d1): Intensity of acidic tang from lactobacillus fermentation ranging from mild to pronounced
- **wild_yeast** (d1): Naturally occurring yeast strains captured from flour and the environment that ferment dough, providing rise without commercial yeast.

## CONSUMERS (what needs this)
`bulk_fermentation`, `depleted_nutrients`, `pizza_dough`, `salt`, `sourdough_starter`

---
*Projected from the `sourdough baking` KB (298 concepts / 165 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*