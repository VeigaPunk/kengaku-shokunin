#!/usr/bin/env python3
"""Reference oracle probe for mutate_test.sh (round 10).

Independently re-derives the three verification layers from the given copies:
  layer record  : ok-vs-(got==want) consistency for graded records
  layer summary : run.log SUMMARY lines vs tallies recomputed from records
                  (A-* rollup = last graded turn ok per pid; others = ok count)
  layer reparse : fenced ```json block inside `raw` re-parses and matches `got`
Exit 0 if every layer agrees; exit 1 listing which layer(s) diverge.
This is NOT the grader — it is the probe that proves each mutation is
detectable by an independent recomputation of the intended layer.
"""
import json, re, sys


def last_turn_ok(recs, pids):
    # horizon.py: summary value = final_ok = last graded turn exact per pid
    per_pid = {}
    for r in recs:
        per_pid.setdefault(r["pid"], {})[r["turn"]] = r.get("ok") is True
    return sum(1 for p in pids if per_pid.get(p, {}).get(max(per_pid.get(p, {0: False})))) if False else None


def summary_counts(recs):
    cells = {}
    for r in recs:
        cells.setdefault(r["cell"], []).append(r)
    out = {}
    # A-INC / A-CKPT: per-pid rollup of last graded turn ok (10 pids)
    for cell in ("A-INC", "A-CKPT"):
        graded = [r for r in cells.get(cell, []) if "ok" in r]
        per_pid = {}
        for r in graded:
            per_pid.setdefault(r["pid"], []).append(r)
        out[cell] = sum(1 for p in per_pid
                        if max(per_pid[p], key=lambda r: r["turn"]).get("ok") is True), len(per_pid)
    # plain ok-count cells
    for cell, rs in cells.items():
        if cell in ("A-INC", "A-CKPT", "meta") or "-ack" in cell:
            continue
        graded = [r for r in rs if "ok" in r]
        out[cell] = sum(1 for r in graded if r.get("ok") is True), len(graded)
    return out


def main():
    r8j, r8l, r9j, r9md = sys.argv[1:5]
    recs8 = [json.loads(l) for l in open(r8j, encoding="utf-8") if l.strip()]
    log = open(r8l, encoding="utf-8").read()
    recs9 = [json.loads(l) for l in open(r9j, encoding="utf-8") if l.strip()]

    problems = []

    # ---- layer record: ok must equal (got == want) whenever both exist ----
    for r in recs8 + recs9:
        if "ok" in r and "got" in r and "want" in r and r.get("ok") != (r["got"] == r["want"]):
            problems.append(f"record: {r['cell']} pid={r.get('pid')} turn={r.get('turn')} "
                            f"ok={r['ok']} but got==want is {r['got'] == r['want']}")

    # ---- layer summary: every SUMMARY line vs recomputed tallies ----
    recomputed = summary_counts(recs8)
    summ = log.split("=== SUMMARY ===")[-1]
    for line in summ.strip().splitlines():
        m = re.match(r"^(\S+): (\d+)/(\d+)$", line.strip())
        if not m:
            problems.append(f"summary: unparsable line {line!r}")
            continue
        key, num, den = m.group(1), int(m.group(2)), int(m.group(3))
        if key not in recomputed:
            problems.append(f"summary: {key} not recomputable from records")
            continue
        rnum, rden = recomputed[key]
        if (num, den) != (rnum, rden):
            problems.append(f"summary: {key} stored {num}/{den} recomputed {rnum}/{rden}")

    # ---- layer reparse: for GRADED records (those with `got`), the fenced
    # ```json block inside `raw` must re-parse and match `got`. Ack/filler
    # records legitimately carry truncated raw (r["content"][:80] in
    # horizon.py) with no block, so they are exempt.
    def extract_json_block(text):
        blocks = re.findall(r"```(?:json)?\s*\n(.*?)```", text, re.S)
        if blocks:
            try: return json.loads(blocks[-1])
            except Exception: pass
        m = re.findall(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]", text, re.S)
        for cand in reversed(m):
            try: return json.loads(cand)
            except Exception: continue
        return None
    for r in recs9:
        if "got" not in r or "raw" not in r:
            continue
        try:
            b = extract_json_block(r["raw"])
        except Exception as e:
            problems.append(f"reparse: {r['cell']} pid={r.get('pid')} raw block fails json.loads ({type(e).__name__})")
            continue
        if b is None:
            problems.append(f"reparse: {r['cell']} pid={r.get('pid')} no fenced json block")
        elif b != r["got"]:
            problems.append(f"reparse: {r['cell']} pid={r.get('pid')} block != got")

    if problems:
        for p in problems:
            print("DIVERGENT", p)
        sys.exit(1)
    print("ALL LAYERS AGREE")
    sys.exit(0)


if __name__ == "__main__":
    main()
