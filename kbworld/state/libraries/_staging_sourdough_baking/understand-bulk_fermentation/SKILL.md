# understand-bulk_fermentation

**CALL NUMBER:** `sourdough_baking.bulk_fermentation : deep_fermentation(6)`
**DEFINITION:** Primary fermentation phase where the mixed dough rests and ferments before shaping; time and temperature control gas production and flavor development.

Invoke this skill to understand `bulk_fermentation` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `?`
- **flavor_complexity** (d2): The depth and nuance of sourdough taste arising from multiple organic acids, esters, and alcohols produced during extended fermentation, creating tangy and complex notes.
- **banneton_flouring** (d4): Dusting the interior of a proofing basket with flour before placing shaped dough, preventing sticking and creating decorative flour patterns on the finished crust.

### from `deep_fermentation`
- **fermentation_byproducts** (d2): Compounds produced by microbial fermentation including carbon dioxide for dough rise, lactic and acetic acids for sour flavor, and alcohols for aroma.
- **carbon_dioxide** (d3): Gaseous byproduct of wild_yeast fermentation that provides dough rise and open crumb structure in sourdough bread.
- **ethanol** (d3): Alcohol produced by wild_yeast during anaerobic fermentation that evaporates during baking and contributes to flavor_complexity development.
- **organic_acids** (d3): Carbon-chain acids produced by lactobacillus metabolism including lactic_acid and acetic_acid that determine sourness_level and contribute to flavor_complexity.
- **fermentation_vigor** (d3): Intensity and rate of the combined microbial fermentation process in sourdough, driven by wild_yeast gas production and lactobacillus acid generation, determining dough rise speed and flavor development timing.
- **aroma_compounds** (d4): Volatile fermentation byproducts including alcohols and esters that create the aromatic profile of sourdough.

### from `sourdough_baking`
- **dough_temperature** (d1): Target temperature of mixed dough (typically 75-80F/24-27C) ensuring predictable fermentation timing regardless of room conditions.
- **fermentation** (d1): Metabolic process where microbes convert sugars to CO2 for rise and acids for sour flavor
- **fermentation_temperature** (d1): Environmental temperature during bulk and final proof that directly controls fermentation speed; warmer accelerates, cooler slows.
- **fold_count** (d1): Number of stretch and fold repetitions during bulk fermentation for gluten development
- **proofing** (d1): Final fermentation phase where shaped dough rises before baking
- **stretch_and_fold** (d1): Method of periodically stretching dough quarters and folding them into the center during bulk fermentation to develop structure without degassing.
- **acetic_acid** (d2): Sharp sour acid produced by lactobacillus in presence of oxygen creating tangy flavor
- **lactic_acid** (d2): Milder sour acid produced by lactobacillus contributing to bread tanginess
- **lactobacillus** (d2): Bacterial strains producing lactic and acetic acids that create sourdough tanginess
- **sourness_level** (d2): Intensity of acidic tang from lactobacillus fermentation ranging from mild to pronounced
- **wild_yeast** (d2): Naturally occurring yeast strains captured from flour and the environment that ferment dough, providing rise without commercial yeast.
- **banneton** (d2): Proofing basket made of woven rattan that supports shaped dough during final proof and leaves characteristic flour patterns on crust.
- **cold_retardation** (d2): Refrigerated proofing slowing fermentation for flavor development and scheduling flexibility
- **overproofing** (d2): Excessive fermentation causing dough to collapse, lose structure, and create flat dense bread
- **proofing_duration** (d2): Time allowance for final dough rise before scoring and baking
- **room_temperature_fermentation** (d2): Proofing at ambient warmth for faster fermentation with brighter flavors
- **underproofing** (d2): Insufficient fermentation leaving dough dense with tight crumb and raw starchy flavor
- **dough_consistency** (d2): Viscosity and handling quality from soft and extensible to firm and tight
- **gluten_development** (d2): Process of hydrating and aligning gluten proteins through mixing, folding, or autolyse to create strong extensible dough.
- **rice_flour** (d3): Fine powder often used for dusting bannetons preventing sticking without dense crust
- **bread_volume** (d3): Total size and height of finished loaf indicating proper fermentation and oven spring
- **crumb_structure** (d3): Internal architecture of bread defined by bubble size, distribution, and tenderness

## CONSUMERS (what needs this)
`dough_temperature`, `levain`

---
*Projected from the `sourdough baking` KB (373 concepts / 213 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*