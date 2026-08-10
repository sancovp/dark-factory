# understand-gluten_development

**CALL NUMBER:** `sourdough_baking.gluten_development`
**DEFINITION:** Process of hydrating and aligning gluten proteins through mixing, folding, or autolyse to create strong extensible dough.

Invoke this skill to understand `gluten_development` down to its primitives. The RELATIVE ROOT below is the least-fixed-point closure of everything it bundles from — the full import cone, grouped by the lib each prim comes from. Projected from a prover-typed KB (MAP/SWI-Prolog consistency gate): every reference below resolves.

## THE RELATIVE ROOT (the import cone, by lib)

### from `sourdough_baking`
- **bread_volume** (d1): Total size and height of finished loaf indicating proper fermentation and oven spring
- **crumb_structure** (d1): Internal architecture of bread defined by bubble size, distribution, and tenderness
- **dough_consistency** (d1): Viscosity and handling quality from soft and extensible to firm and tight

## CONSUMERS (what needs this)
`autolyse`, `flour`, `oven_spring`, `salt`, `stretch_and_fold`, `whole_wheat_sourdough`

---
*Projected from the `sourdough baking` KB (298 concepts / 165 relations) — consistency-typed by MAP; the facet list after the colon IS the cross-lib dependency web.*