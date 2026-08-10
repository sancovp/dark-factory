# understand-sourdough_starter

**CALL NUMBER:** `sourdough_baking.sourdough_starter : deep_fermentation(6), deep_sourdough_starter(5)`
**DEFINITION:** A fermented mixture of flour and water containing wild yeast and lactic acid bacteria that serves as the natural leaven for sourdough bread, maintained through regular feedings.

Invoke this skill to understand `sourdough_starter` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `?`
- **flavor_complexity** (d2): The depth and nuance of sourdough taste arising from multiple organic acids, esters, and alcohols produced during extended fermentation, creating tangy and complex notes.
- **banneton_flouring** (d6): Dusting the interior of a proofing basket with flour before placing shaped dough, preventing sticking and creating decorative flour patterns on the finished crust.

### from `deep_fermentation`
- **fermentation_byproducts** (d2): Compounds produced by microbial fermentation including carbon dioxide for dough rise, lactic and acetic acids for sour flavor, and alcohols for aroma.
- **organic_acids** (d2): Carbon-chain acids produced by lactobacillus metabolism including lactic_acid and acetic_acid that determine sourness_level and contribute to flavor_complexity.
- **carbon_dioxide** (d2): Gaseous byproduct of wild_yeast fermentation that provides dough rise and open crumb structure in sourdough bread.
- **ethanol** (d2): Alcohol produced by wild_yeast during anaerobic fermentation that evaporates during baking and contributes to flavor_complexity development.
- **fermentation_vigor** (d2): Intensity and rate of the combined microbial fermentation process in sourdough, driven by wild_yeast gas production and lactobacillus acid generation, determining dough rise speed and flavor development timing.
- **aroma_compounds** (d3): Volatile fermentation byproducts including alcohols and esters that create the aromatic profile of sourdough.

### from `deep_sourdough_starter`
- **cold_storage_duration** (d2): Time period a starter spends refrigerated during dormancy, during which yeast and bacterial metabolism slow significantly from peak activity levels.
- **cold_temperature_trigger** (d2): Temperature threshold causing metabolic slowdown that initiates dormant state in starter culture.
- **depleted_nutrients** (d2): Exhausted flour sugars and starches in starter following active fermentation, triggering dormancy as microbial food source is consumed.
- **refrigeration_metabolism** (d2): Reduced metabolic rate of wild_yeast and lactobacillus populations occurring at cold temperatures, producing minimal CO2 and acid output.
- **storage_viability** (d2): Degree to which dormant_starter retains fermentation capability over cold_storage_duration, affected by starter_age and storage conditions.

### from `sourdough_baking`
- **active_starter** (d1): Starter exhibiting vigorous bubbling, foam surface, and doubling within hours of feeding, indicating healthy yeast and bacterial populations.
- **discard** (d1): Excess starter removed during feeding that can be used in discard recipes
- **dormant_starter** (d1): Starter stored in refrigerator with slowed activity due to cold temperature and depleted food; revives after feeding at room temperature.
- **feed_ratio** (d1): Proportion of flour and water added relative to existing starter weight during feeding
- **fermentation** (d1): Metabolic process where microbes convert sugars to CO2 for rise and acids for sour flavor
- **lactobacillus** (d1): Bacterial strains producing lactic and acetic acids that create sourdough tanginess
- **levain** (d1): A portion of active sourdough starter built up before baking, used to leaven the main dough; can be stiff or liquid in consistency.
- **starter_age** (d1): Duration since last feeding affecting fermentation vigor and flavor complexity
- **starter_feeding_schedule** (d1): Regular timing pattern for maintaining starter such as daily or twice daily
- **starter_hydration** (d1): Consistency of starter ranging from thick and stiff to loose and liquid
- **starter_maintenance** (d1): Ongoing care of sourdough culture through regular feeding schedules and storage conditions
- **starter_refreshment** (d1): Process of feeding starter with fresh flour and water to maintain microbial balance and fermentation vigor.
- **starter_storage_temperature** (d1): Refrigerated or room temperature holding conditions affecting fermentation rhythm
- **starter_vigor** (d1): Observable rising speed and bubble activity indicating culture health and strength
- **wild_yeast** (d1): Naturally occurring yeast strains captured from flour and the environment that ferment dough, providing rise without commercial yeast.
- **pizza_dough** (d2): Sourdough base fermented for complex flavor before topping and high-heat baking
- **sourdough_pancakes** (d2): Breakfast preparation using discard starter for fluffy tangy pancakes
- **sourdough_waffles** (d2): Crispy waffles made with discard starter for complex sour flavor
- **acetic_acid** (d2): Sharp sour acid produced by lactobacillus in presence of oxygen creating tangy flavor
- **lactic_acid** (d2): Milder sour acid produced by lactobacillus contributing to bread tanginess
- **sourness_level** (d2): Intensity of acidic tang from lactobacillus fermentation ranging from mild to pronounced
- **bulk_fermentation** (d2): Primary fermentation phase where the mixed dough rests and ferments before shaping; time and temperature control gas production and flavor development.
- **inoculation** (d2): Adding levain to new dough batch to begin fermentation with established culture
- **dough_temperature** (d3): Target temperature of mixed dough (typically 75-80F/24-27C) ensuring predictable fermentation timing regardless of room conditions.
- **fermentation_temperature** (d3): Environmental temperature during bulk and final proof that directly controls fermentation speed; warmer accelerates, cooler slows.

---
*Projected from the `sourdough baking` KB (373 concepts / 213 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*