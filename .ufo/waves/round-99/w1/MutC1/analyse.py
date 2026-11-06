#!/usr/bin/env python3
"""Summarise the MutC1 matrix: verdicts, killing legs, probe-observation diffs, hashes."""
import json
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r99/MutC1")
RECEIPT = S / "clone" / "corpus/evidence/round99/bnfit-probe.txt"


def obs_lines(text):
    inside, out = False, []
    for ln in text.splitlines():
        if ln == "OBSERVATIONS_BEGIN":
            inside = True
            continue
        if ln == "OBSERVATIONS_END":
            break
        if inside:
            out.append(ln)
    return out


def main():
    summary = json.loads((S / "summary.json").read_text())
    manifest = json.loads((S / "manifest.json").read_text())
    receipt_obs = obs_lines(RECEIPT.read_text())
    rows = []
    for mid in sorted(summary):
        r = summary[mid]
        legs = r["legs"].replace("LEGS ", "")
        failed = [x.split("=")[0] for x in legs.split() if x.endswith("fail")]
        rc = r["rc"]
        if rc == 0 and r["predicate"].endswith("pass"):
            verdict = "SURVIVED"
        elif rc == 2:
            verdict = "KILLED(rc2)"
        else:
            verdict = "KILLED"
        probe_diff = ""
        if "probe_obs" in r:
            po = r["probe_obs"]
            if po == receipt_obs:
                probe_diff = "obs identical to receipt"
            else:
                d = []
                for a, b in zip(receipt_obs, po):
                    if a != b:
                        d.append(f"- {a}\n+ {b}")
                if len(po) != len(receipt_obs):
                    d.append(f"line count {len(po)} vs {len(receipt_obs)}")
                probe_diff = " | ".join(d) if d else "obs identical"
        rows.append({
            "id": mid, "desc": r["desc"], "expected": r["expected"], "rc": rc,
            "failed_legs": failed, "verdict": verdict, "target": r.get("target", ""),
            "setup": r.get("setup", ""), "probe_rc": r.get("probe_rc"),
            "probe_diff": probe_diff, "commit": r["commit"], "paths": r["paths"],
        })
    (S / "matrix.json").write_text(json.dumps(rows, indent=1))
    print(f"{'id':5} {'rc':>2} {'verdict':12} {'failed legs':22} expected")
    for r in rows:
        print(f"{r['id']:5} {r['rc']:>2} {r['verdict']:12} {','.join(r['failed_legs']) or '-':22} {r['expected']}")
    print("\n--- probe-direct observation diffs ---")
    for r in rows:
        if r["probe_rc"] is not None:
            print(f"{r['id']} probe_rc={r['probe_rc']}: {r['probe_diff'][:400]}")
    print("\n--- survivors / rc2 detail ---")
    for r in rows:
        if r["verdict"] != "KILLED":
            print(f"{r['id']} {r['verdict']} {r['desc']}")
            print("   target:", r["target"])
            if r["setup"]:
                print("   setup:", r["setup"])
    print("\n--- before/after hashes ---")
    for r in rows:
        for p, h in r["paths"].items():
            print(f"{r['id']:5} {p} {h['before'][:16]} -> {h['after'][:16]}")


if __name__ == "__main__":
    main()
