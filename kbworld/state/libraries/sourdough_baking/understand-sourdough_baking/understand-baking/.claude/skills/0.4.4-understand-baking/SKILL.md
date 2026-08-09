---
name: 0.4.4-understand-baking
description: [0.4.4] Cooking dough in hot oven transforming it into bread through heat and chemical reactions
---

# understand-baking

**CALL NUMBER:** `sourdough_baking.baking : deep_fermentation(1)`
**DEFINITION:** Cooking dough in hot oven transforming it into bread through heat and chemical reactions

Invoke this skill to understand `baking` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `?`
- **baking_duration** (d1): The total time bread spends in the oven during baking, typically 20-50 minutes depending on loaf size and oven temperature.
- **crumb_color** (d2): The visual shade of the bread interior ranging from pale ivory to deep golden depending on fermentation length, dough hydration, and baking time and temperature.
- **crumb_texture** (d2): The physical feel and structural quality of bread's interior ranging from fine and tender to coarse and chewy based on gluten development and fermentation.
- **crust_color** (d2): The brown coloration of bread's outer layer produced by Maillard reaction and caramelization during baking, ranging from pale gold to deep mahogany.
- **fermentation_byproducts** (d5): Compounds produced by microbial fermentation including carbon dioxide for dough rise, lactic and acetic acids for sour flavor, and alcohols for aroma.
- **flavor_complexity** (d5): The depth and nuance of sourdough taste arising from multiple organic acids, esters, and alcohols produced during extended fermentation, creating tangy and complex notes.
- **banneton_flouring** (d7): Dusting the interior of a proofing basket with flour before placing shaped dough, preventing sticking and creating decorative flour patterns on the finished crust.

### from `deep_fermentation`
- **fermentation_vigor** (d6): Intensity and rate of the combined microbial fermentation process in sourdough, driven by wild_yeast gas production and lactobacillus acid generation, determining dough rise speed and flavor development timing.

### from `sourdough_baking`
- **baking_temperature** (d1): Oven heat setting typically between 450-500F for home sourdough baking
- **crumb** (d1): The interior crumb structure of bread characterized by hole size, distribution, tenderness, and openness ranging from tight and dense to open and airy.
- **crust** (d1): The baked outer layer of bread formed by Maillard reaction and caramelization; texture ranges from thin and crispy to thick and chewy based on hydration and baking method.
- **dutch_oven** (d1): Heavy lidded pot used to bake sourdough that traps steam from dough moisture, creating professional results without an oven steam injection system.
- **internal_temperature** (d1): Bread center temperature (typically 195-210F/90-99C) indicating doneness; lower temps leave gummy crumb.
- **lid_removal** (d1): Taking Dutch oven lid off mid-bake to release steam and finish crust coloring
- **oven_spring** (d1): Rapid oven rise occurring in the first 10-15 minutes of baking due to yeast activity, gas expansion, and steam; creates open crumb and dramatic ear.
- **steam_production** (d1): Water vapor released in oven creating humid environment for optimal crust development
- **bread_volume** (d2): Total size and height of finished loaf indicating proper fermentation and oven spring
- **crumb_structure** (d2): Internal architecture of bread defined by bubble size, distribution, and tenderness
- **crust_texture** (d2): External characteristics of crust from chewy and thick to thin and crispy
- **ear** (d2): The lifted crust edge formed from scoring that rises dramatically during oven spring; prized aesthetic and texture element in artisan sourdough.
- **maillard_reaction** (d2): Chemical reaction between amino acids and sugars at high temperatures creating brown crust color and complex savory flavors.
- **dough_temperature** (d2): Target temperature of mixed dough (typically 75-80F/24-27C) ensuring predictable fermentation timing regardless of room conditions.
- **gluten_development** (d2): Process of hydrating and aligning gluten proteins through mixing, folding, or autolyse to create strong extensible dough.
- **scoring** (d2): Shallow cuts made on proofed dough before baking to control oven spring direction, create visual patterns, and allow steam to escape during baking.
- **bulk_fermentation** (d3): Primary fermentation phase where the mixed dough rests and ferments before shaping; time and temperature control gas production and flavor development.
- **fermentation_temperature** (d3): Environmental temperature during bulk and final proof that directly controls fermentation speed; warmer accelerates, cooler slows.
- **dough_consistency** (d3): Viscosity and handling quality from soft and extensible to firm and tight
- **lame** (d3): Sharp curved blade used for scoring bread, typically with a wooden handle, that creates clean precise cuts for ear formation.
- **scoring_angle** (d3): Blade orientation relative to dough surface affecting ear formation and rise pattern
- **fermentation** (d4): Metabolic process where microbes convert sugars to CO2 for rise and acids for sour flavor
- **fold_count** (d4): Number of stretch and fold repetitions during bulk fermentation for gluten development
- **proofing** (d4): Final fermentation phase where shaped dough rises before baking
- **stretch_and_fold** (d4): Method of periodically stretching dough quarters and folding them into the center during bulk fermentation to develop structure without degassing.

---
*Projected from the `sourdough baking` KB (298 concepts / 165 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*

_(leaf — this is an actual skill.)_
