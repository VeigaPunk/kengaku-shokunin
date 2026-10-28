#!/usr/bin/env python3
"""Compare attrib.py runs and emit the per-row kill-stability table.

A row is STABLE iff it APPLIES and is CAUGHT (>=1 changed per-fixture verdict) in EVERY run, and the set of
(fid, old, new) triples is identical across runs. Otherwise the row is order/path dependent and must be DROPPED.

Usage: compare.py RUN.json[:label] ... --out TABLE.txt
"""
import argparse
import json
import pathlib
import sys


def triples(row):
    return frozenset((c["fid"], c["old"], c["new"]) for c in row["changed"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    runs = []
    for spec in a.runs:
        path, _, label = spec.partition(":")
        d = json.loads(pathlib.Path(path).read_text())
        d["_label"] = label or pathlib.Path(path).stem
        d["_rows"] = {r["id"]: r for r in d["rows"]}
        runs.append(d)

    ids, order_consistent = [], True
    for r in runs:
        for i in r["_rows"]:
            if i not in ids:
                ids.append(i)

    lines, unstable, stable_rows, nchanged, na, surv = [], [], [], 0, [], []
    fences = {r["fence_sha256"] for r in runs}
    digests = {r["ref_digest"] for r in runs}
    for i in ids:
        per = []
        for r in runs:
            row = r["_rows"].get(i)
            if row is None:
                per.append(("MISSING", frozenset(), r["_label"]))
                continue
            per.append(("APPLIES" if row["applies"] else "BROKEN", triples(row) if row["applies"] else
                        frozenset(), r["_label"]))
        states = {p[0] for p in per}
        sets = {p[1] for p in per}
        if len(states) > 1 or len(sets) > 1:
            unstable.append(i)
            why = []
            if len(states) > 1:
                why.append("state=" + ",".join(f"{p[2]}:{p[0]}" for p in per))
            if len(sets) > 1:
                why.append("changeset=" + " | ".join(
                    f"{p[2]}:{','.join(sorted(f + ':' + o + '>' + n for f, o, n in p[1])) or '-'}" for p in per))
            lines.append(f"ORDER-DEPENDENT {i} " + " ".join(why))
            lines.append(f"DROP {i}")
        elif states == {"BROKEN"}:
            na.append(i)
            lines.append(f"NOT-APPLICABLE {i} (out of ordering scope)")
        elif not next(iter(sets)):
            surv.append(i)
            lines.append(f"SURVIVED {i} (applies, no verdict change; out of ordering scope)")
        else:
            kinds = sorted(next(iter(sets)))
            stable_rows.append(i)
            nchanged += len(kinds)
            semantic = sum(1 for _f, o, n in kinds if n != "ERROR" and o != "ERROR")
            lines.append(f"STABLE {i} tuples={len(kinds)} semantic={semantic} "
                         f"error-vector={len(kinds) - semantic}")
            for fid, old, new in kinds:
                lines.append(f"STABLE {i} {fid} {old}->{new}")

    head = [f"RUNS {' '.join(r['_label'] for r in runs)}",
            f"FENCES {' '.join(sorted(fences))}",
            f"REFDIGESTS {' '.join(sorted(digests))}",
            f"REF-ORDER-INVARIANT {'yes' if len(digests) == 1 else 'NO'}",
            f"ROWS total={len(ids)} stable={len(stable_rows)} dropped={len(unstable)} "
            f"not-applicable={len(na)} survived={len(surv)} stable-tuples={nchanged}"]
    out = "\n".join(head + [""] + lines) + "\n"
    pathlib.Path(a.out).write_text(out)
    print(out, end="")
    return 0 if not unstable and len(digests) == 1 else 1


if __name__ == "__main__":
    sys.exit(main())
