# Lotion math

Split a lotion batch into exact grams, count the jars, and check the preservative against a labeled band. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/lotionmath/

## The three tools

- **Batch split** - `batchPlan(totalG, waterPct, oilPct, emulsPct, preservPct)`: percentages become grams, with an exact 100% sum check.
- **Jar plan** - `jarPlan(totalG)`: grams become milliliters at a labeled 0.95 g/ml, rounded up to labeled 100 ml jars.
- **Preservative check** - `preservCheck(totalG, preservG)`: grams become a percent, checked against the labeled 0.5-1.5% band.

## Labeled norms (illustrative references, not rules)

- Starting phases: about 70% water, 24% oils, 5% emulsifier, 1% preservative.
- Density: about 0.95 g per ml. Jar size: 100 ml. Preservative band: 0.5-1.5% of the batch.

Your preservative's own instructions are the authority on its dose, and water-based products grow microbes without one.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (35 cases, 105 checks)

Regenerate the oracle expectations: `python3 oracle.py`
