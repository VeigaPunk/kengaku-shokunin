#!/usr/bin/env python3
"""FP4Preservation scratch comparator: round-28 run vs round-27 frozen receipt.

Compares EVERY keyed assertion/disclosure: id set, verdict, and full payload.
Read-only over production. Output: comparison-result.json (same scratch dir).
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
S = LANE / ".ufo/waves/round-28/scratch/FP4Preservation"
RUN = S / "state-check-round28-run1.json"
BASE = LANE / "corpus/evidence/round27-calibration/state-final-json.json"

run = json.loads(RUN.read_text(encoding="utf-8"))
base = json.loads(BASE.read_text(encoding="utf-8"))


def index(items):
    ids = [a["id"] for a in items]
    dupes = [k for k, v in Counter(ids).items() if v > 1]
    return {a["id"]: a for a in items}, dupes


ra, rdup = index(run["assertions"])
ba, bdup = index(base["assertions"])

summary_fields = ["assertions", "match", "mismatch", "superseded",
                  "offline_unverifiable", "out_of_population"]
summary_cmp = {
    f: {"run": run["summary"].get(f), "baseline": base["summary"].get(f),
        "equal": run["summary"].get(f) == base["summary"].get(f)}
    for f in summary_fields
}

verdict_diffs, payload_diffs, run_only, base_only = [], [], [], []
for aid in sorted(set(ra) | set(ba)):
    r, b = ra.get(aid), ba.get(aid)
    if r is None:
        base_only.append({"id": aid, "baseline_verdict": b["verdict"]})
        continue
    if b is None:
        run_only.append({"id": aid, "run_verdict": r["verdict"],
                         "run_observed": r["observed"]})
        continue
    if r["verdict"] != b["verdict"]:
        verdict_diffs.append({"id": aid, "baseline": b["verdict"], "run": r["verdict"]})
    if json.dumps(r, sort_keys=True, ensure_ascii=False) != json.dumps(b, sort_keys=True, ensure_ascii=False):
        field_diffs = {}
        for f in ("source_line", "check", "observed", "verdict"):
            if json.dumps(r.get(f), sort_keys=True, ensure_ascii=False) != json.dumps(b.get(f), sort_keys=True, ensure_ascii=False):
                field_diffs[f] = {"baseline": b.get(f), "run": r.get(f)}
        payload_diffs.append({"id": aid, "fields": field_diffs})

oop_base = sorted(i for i in ba if ba[i]["verdict"] == "OUT_OF_POPULATION")
oop_run = sorted(i for i in ra if ra[i]["verdict"] == "OUT_OF_POPULATION")
oop_preserved = [i for i in oop_base if i in ra and ra[i]["verdict"] == "OUT_OF_POPULATION"]
oop_new = [i for i in oop_run if i not in ba]
oop_lost = [i for i in oop_base if i not in ra]
oop_changed = [i for i in oop_base if i in ra and ra[i]["verdict"] != "OUT_OF_POPULATION"]

p4 = {i: ra[i]["verdict"] for i in sorted(ra) if i.startswith("P4.")}
p4_counts = Counter(p4.values())

superseded = sorted(i for i in ra if ra[i]["verdict"] == "SUPERSEDED")
offline = sorted(i for i in ra if ra[i]["verdict"] == "OFFLINE_UNVERIFIABLE")
mismatches = sorted(i for i in ra if ra[i]["verdict"] == "MISMATCH")
sup_base = sorted(i for i in ba if ba[i]["verdict"] == "SUPERSEDED")
off_base = sorted(i for i in ba if ba[i]["verdict"] == "OFFLINE_UNVERIFIABLE")

result = {
    "inputs": {
        "run": str(RUN), "run_sha256": hashlib.sha256(RUN.read_bytes()).hexdigest(),
        "baseline": str(BASE), "baseline_sha256": hashlib.sha256(BASE.read_bytes()).hexdigest(),
    },
    "duplicate_ids": {"run": rdup, "baseline": bdup},
    "summary_comparison": summary_cmp,
    "id_set": {
        "run_count": len(ra), "baseline_count": len(ba),
        "run_only_count": len(run_only), "base_only_count": len(base_only),
    },
    "verdict_diff_count": len(verdict_diffs), "verdict_diffs": verdict_diffs,
    "payload_diff_count": len(payload_diffs), "payload_diffs": payload_diffs,
    "run_only": run_only, "base_only": base_only,
    "out_of_population": {
        "baseline_total": len(oop_base), "run_total": len(oop_run),
        "preserved_old_count": len(oop_preserved),
        "preserved_old_ids": oop_preserved,
        "new_ids": oop_new,
        "lost_old_ids": oop_lost,
        "old_changed_verdict": oop_changed,
        "new_details": [{"id": i, "observed": ra[i]["observed"],
                         "source_line": ra[i]["source_line"],
                         "check": ra[i]["check"]} for i in oop_new],
    },
    "P4": {"total": len(p4), "verdict_counts": dict(p4_counts),
           "superseded_ids": [i for i in superseded if i.startswith("P4.")],
           "offline_ids": [i for i in offline if i.startswith("P4.")],
           "by_id": p4},
    "superseded_run": superseded, "superseded_baseline": sup_base,
    "superseded_set_equal": superseded == sup_base,
    "offline_run": offline, "offline_baseline": off_base,
    "offline_set_equal": offline == off_base,
    "mismatch_run": mismatches,
}

(S / "comparison-result.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps({k: v for k, v in result.items() if k != "P4"}, ensure_ascii=False)[:1] if False else "", end="")
print("summary_cmp:", json.dumps(summary_cmp, ensure_ascii=False))
print("id_set:", json.dumps(result["id_set"], ensure_ascii=False))
print("verdict_diff_count:", len(verdict_diffs), "payload_diff_count:", len(payload_diffs))
print("verdict_diffs:", json.dumps(verdict_diffs, ensure_ascii=False))
print("payload_diffs:", json.dumps(payload_diffs, ensure_ascii=False))
print("run_only:", json.dumps(run_only, ensure_ascii=False))
print("base_only:", json.dumps(base_only, ensure_ascii=False))
print("oop:", json.dumps({k: v for k, v in result["out_of_population"].items()}, ensure_ascii=False))
print("P4:", json.dumps(result["P4"], ensure_ascii=False))
print("superseded_run:", superseded)
print("offline_run:", offline)
print("mismatch_run:", mismatches)
print("superseded_set_equal:", result["superseded_set_equal"],
      "offline_set_equal:", result["offline_set_equal"])
