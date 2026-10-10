#!/usr/bin/env python3
"""Oracle mirror of engine.js for Lotion math. Writes expected.json (with trailing newline)."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100

def jsnum(x):
    if isinstance(x, float) and x == int(x) and abs(x) < 1e15:
        return int(x)
    return x

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return repr(x) if isinstance(x, float) else str(x)

def batchPlan(totalG, waterPct, oilPct, emulsPct, preservPct):
    if not (totalG > 0):
        return {"error": "batch size must be positive"}
    if not (waterPct >= 0) or not (oilPct >= 0) or not (emulsPct >= 0) or not (preservPct >= 0):
        return {"error": "phase percentages cannot be negative"}
    if waterPct + oilPct + emulsPct + preservPct != 100:
        return {"error": "phases must add to 100%"}
    return {"totalG": jsnum(float(totalG)), "waterG": jsnum(r1(totalG * waterPct / 100)),
            "oilG": jsnum(r1(totalG * oilPct / 100)), "emulsG": jsnum(r1(totalG * emulsPct / 100)),
            "preservG": jsnum(r1(totalG * preservPct / 100))}

def jarPlan(totalG):
    if not (totalG > 0):
        return {"error": "batch size must be positive"}
    ml = totalG / 0.95
    jars = math.ceil(ml / 100)
    return {"totalG": jsnum(float(totalG)), "ml": jsnum(r1(ml)), "jars": jars, "spareMl": jsnum(r1(jars * 100 - ml))}

def preservCheck(totalG, preservG):
    if not (totalG > 0) or not (preservG >= 0):
        return {"error": "grams must be positive"}
    pct = r2(preservG / totalG * 100)
    if pct < 0.5:
        verdict = "below the labeled 0.5-1.5% band - check your recipe"
    elif pct > 1.5:
        verdict = "above the labeled 0.5-1.5% band - check your recipe"
    else:
        verdict = "inside the labeled 0.5-1.5% band"
    return {"totalG": jsnum(float(totalG)), "preservG": jsnum(float(preservG)), "pct": jsnum(pct), "verdict": verdict}

def renderBatch(r):
    return ("A " + fmt(r["totalG"]) + " g batch splits into " + fmt(r["waterG"]) + " g water, " + fmt(r["oilG"]) +
            " g oils, " + fmt(r["emulsG"]) + " g emulsifier and " + fmt(r["preservG"]) + " g preservative (labeled phases).")

def renderJar(r):
    return (fmt(r["totalG"]) + " g of lotion is about " + fmt(r["ml"]) + " ml at the labeled 0.95 g/ml - " + str(r["jars"]) +
            " labeled 100 ml jar" + ("" if r["jars"] == 1 else "s") + ", " + fmt(r["spareMl"]) + " ml spare.")

def renderPreserv(r):
    return fmt(r["preservG"]) + " g in a " + fmt(r["totalG"]) + " g batch is " + fmt(r["pct"]) + "% - " + r["verdict"] + "."

CASES = []
def add(fn, args): CASES.append({"fn": fn, "args": args})

for a in [(500, 70, 24, 5, 1), (200, 75, 20, 4, 1), (1000, 70, 24, 5, 1), (100, 80, 15, 4, 1), (250, 72, 22, 5, 1),
          (50, 70, 24, 5, 1), (400, 65, 28, 6, 1), (500, 70, 24, 5, 0), (500, 60, 24, 5, 1), (0, 70, 24, 5, 1),
          (500, 70, 24, 5, -1), (300, 76.5, 20, 3, 0.5)]:
    add("batchPlan", list(a))
for a in [(500,), (250,), (95,), (1000,), (47.5,), (190,), (760,), (100,), (330,), (0,), (-100,)]:
    add("jarPlan", list(a))
for a in [(500, 5), (500, 1), (500, 10), (500, 2.5), (500, 7.5), (200, 1), (200, 4), (1000, 12), (250, 3), (500, 0), (0, 5), (500, -1)]:
    add("preservCheck", list(a))

out = []
for c in CASES:
    fn = {"batchPlan": batchPlan, "jarPlan": jarPlan, "preservCheck": preservCheck}[c["fn"]]
    res = fn(*c["args"])
    is_err = "error" in res
    if is_err:
        render = res["error"]
    else:
        render = {"batchPlan": renderBatch, "jarPlan": renderJar, "preservCheck": renderPreserv}[c["fn"]](res)
    out.append({"fn": c["fn"], "args": c["args"], "result": res, "render": render, "isError": is_err})

with open("expected.json", "w") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
print("wrote", len(out), "cases")
