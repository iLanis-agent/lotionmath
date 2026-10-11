/* Lotion math engine - pure arithmetic, every borrowed number labeled. */
(function (root) {
  "use strict";
  function r1(x) { return Math.round(x * 10) / 10; }
  function r2(x) { return Math.round(x * 100) / 100; }

  function batchPlan(totalG, waterPct, oilPct, emulsPct, preservPct) {
    if (!(totalG > 0)) return { error: "batch size must be positive" };
    if (!(waterPct >= 0) || !(oilPct >= 0) || !(emulsPct >= 0) || !(preservPct >= 0)) return { error: "phase percentages cannot be negative" };
    if (waterPct + oilPct + emulsPct + preservPct !== 100) return { error: "phases must add to 100%" };
    return { totalG: totalG, waterG: r1(totalG * waterPct / 100), oilG: r1(totalG * oilPct / 100),
             emulsG: r1(totalG * emulsPct / 100), preservG: r1(totalG * preservPct / 100) };
  }

  function jarPlan(totalG) {
    if (!(totalG > 0)) return { error: "batch size must be positive" };
    var ml = totalG / 0.95;
    var jars = Math.ceil(ml / 100);
    return { totalG: totalG, ml: r1(ml), jars: jars, spareMl: r1(jars * 100 - ml) };
  }

  function preservCheck(totalG, preservG) {
    if (!(totalG > 0) || !(preservG >= 0)) return { error: "grams must be positive" };
    return { totalG: totalG, preservG: preservG, pct: r2(preservG / totalG * 100) };
  }

  function renderBatch(r) {
    return "A " + r.totalG + " g batch splits into " + r.waterG + " g water, " + r.oilG + " g oils, " + r.emulsG + " g emulsifier and " + r.preservG + " g preservative (labeled phases).";
  }

  function renderJar(r) {
    return r.totalG + " g of lotion is about " + r.ml + " ml at the labeled 0.95 g/ml - " + r.jars + " labeled 100 ml jar" + (r.jars === 1 ? "" : "s") + ", " + r.spareMl + " ml spare.";
  }

  function renderPreserv(r) {
    return r.preservG + " g in a " + r.totalG + " g batch is " + r.pct + "% - a percentage, not a verdict on the dose.";
  }

  var api = { batchPlan: batchPlan, jarPlan: jarPlan, preservCheck: preservCheck, renderBatch: renderBatch, renderJar: renderJar, renderPreserv: renderPreserv };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.LotionMath = api;
})(typeof window !== "undefined" ? window : this);
