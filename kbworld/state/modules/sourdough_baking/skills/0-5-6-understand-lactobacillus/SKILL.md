---
name: 0.5.6-understand-lactobacillus
description: "[0.5.6] Bacterial strains producing lactic and acetic acids that create sourdough tanginess"
---

# understand-lactobacillus

**CALL NUMBER:** `sourdough_baking.lactobacillus : deep_fermentation(1)`
**DEFINITION:** Bacterial strains producing lactic and acetic acids that create sourdough tanginess

Invoke this skill to understand `lactobacillus` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `?`
- **flavor_complexity** (d2): The depth and nuance of sourdough taste arising from multiple organic acids, esters, and alcohols produced during extended fermentation, creating tangy and complex notes.

### from `deep_fermentation`
- **organic_acids** (d1): Carbon-chain acids produced by lactobacillus metabolism including lactic_acid and acetic_acid that determine sourness_level and contribute to flavor_complexity.

### from `sourdough_baking`
- **acetic_acid** (d1): Sharp sour acid produced by lactobacillus in presence of oxygen creating tangy flavor
- **lactic_acid** (d1): Milder sour acid produced by lactobacillus contributing to bread tanginess
- **sourness_level** (d1): Intensity of acidic tang from lactobacillus fermentation ranging from mild to pronounced

## CONSUMERS (what needs this)
`as_lactobacillus_density`, `fermentation`, `rye_sourdough`, `sourdough_starter`

---
*Projected from the `sourdough baking` KB (373 concepts / 213 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*

_(leaf — this is an actual skill.)_
