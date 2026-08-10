---
name: 0.3.2-understand-fermentation_byproducts
description: "[0.3.2] Compounds produced by microbial fermentation including carbon dioxide for dough rise, lactic and acetic acids "
---

# understand-fermentation_byproducts

**CALL NUMBER:** `deep_fermentation.fermentation_byproducts : sourdough_baking(3)`
**DEFINITION:** Compounds produced by microbial fermentation including carbon dioxide for dough rise, lactic and acetic acids for sour flavor, and alcohols for aroma.

Invoke this skill to understand `fermentation_byproducts` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `?`
- **flavor_complexity** (d2): The depth and nuance of sourdough taste arising from multiple organic acids, esters, and alcohols produced during extended fermentation, creating tangy and complex notes.

### from `deep_fermentation`
- **carbon_dioxide** (d1): Gaseous byproduct of wild_yeast fermentation that provides dough rise and open crumb structure in sourdough bread.
- **ethanol** (d1): Alcohol produced by wild_yeast during anaerobic fermentation that evaporates during baking and contributes to flavor_complexity development.
- **organic_acids** (d1): Carbon-chain acids produced by lactobacillus metabolism including lactic_acid and acetic_acid that determine sourness_level and contribute to flavor_complexity.
- **aroma_compounds** (d2): Volatile fermentation byproducts including alcohols and esters that create the aromatic profile of sourdough.

### from `sourdough_baking`
- **acetic_acid** (d1): Sharp sour acid produced by lactobacillus in presence of oxygen creating tangy flavor
- **lactic_acid** (d1): Milder sour acid produced by lactobacillus contributing to bread tanginess
- **sourness_level** (d2): Intensity of acidic tang from lactobacillus fermentation ranging from mild to pronounced

## CONSUMERS (what needs this)
`fermentation`

---
*Projected from the `sourdough baking` KB (373 concepts / 213 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*

_(leaf — this is an actual skill.)_
