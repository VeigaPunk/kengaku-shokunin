import sys
Q = [
 ("plans/round-29-claims.md", 11, "lowest legacy novelty7 → canonical coverage/constructs"),
 ("plans/round-29-claims.md", 15, "only for an offline source-faithful projection. Score7 held;"),
 ("plans/round-29-claims.md", 16, "calibration8 and other axes unchanged."),
 ("plans/round-29-claims.md", 15, "README's generated-eval-config frontier"),
 ("plans/round-29-claims.md", 95, "index/coverage and source-used-by links"),
 ("SCORECARD.md", 716, "a mapping, not an AXES.md split"),
 ("SCORECARD.md", 890, "tied coverage/surfaces7 remains capped, no waiver."),
 ("SCORECARD.md", 908, "capped, operability8, freshness8, adjacency8"),
 ("SCORECARD.md", 247, "a gap line contradicted by an artifact already in the repo"),
 ("SCORECARD.md", 569, "the nudge is inactive while novelty sits below 8"),
 ("corpus/README.md", 338, "generated eval-time configs, runtime DOM/helper/judge validity and contamination checks remain open."),
 ("PROVINCE.md", 201, "generated configs, runtime task validity, hosted judges and contamination remain open."),
 ("../AXES.md", 37, "saturates, the lane may retire it or split it into a sub-axis"),
 ("../PROTOCOL.md", 515, "is worked only if its row carries its mapping to one of the"),
]
bad = 0
for f, ln, q in Q:
    lines = open(f, encoding="utf-8").read().split("\n")
    hits = [i + 1 for i, l in enumerate(lines) if q in l]
    ok = (ln in hits) if ln else bool(hits)
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {f}:{hits} words={len(q.split())} {q!r}")
print("bad", bad); sys.exit(1 if bad else 0)
