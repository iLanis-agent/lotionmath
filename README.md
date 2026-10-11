# Lotion math

Split a lotion batch into exact grams, count the jars, and turn the preservative grams into an honest percent. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/lotionmath/

## The three tools

- **Batch split** - `batchPlan(totalG, waterPct, oilPct, emulsPct, preservPct)`: percentages become grams, with an exact 100% sum check.
- **Jar plan** - `jarPlan(totalG)`: grams become milliliters at a labeled 0.95 g/ml, rounded up to labeled 100 ml jars.
- **Preservative percent** - `preservCheck(totalG, preservG)`: grams become a percent. Arithmetic only, never a verdict on the dose.

## Boundary

Arithmetic does not establish preservation efficacy, shelf life or skin safety. The specific supplier's directions and validated formulation and testing are the authority on dose. Water-based products grow microbes without adequate preservation.

## Labeled norms (illustrative references, not rules)

- Starting phases: about 70% water, 24% oils, 5% emulsifier, 1% preservative.
- Density: about 0.95 g per ml. Jar size: 100 ml.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (35 cases, 105 checks)

Regenerate the oracle expectations: `python3 oracle.py`
