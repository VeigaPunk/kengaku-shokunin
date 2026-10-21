# probeC_grader_check.py — import-free replay of probe-C graders (horizon.py:226-230, 270-289).
import itertools, json
CONFLICT_ROWS = [["A","B","C","D"], ["B","C","D","A"], ["A","B","D","C"]]   # h.py:226
BENIGN_ROWS   = [["A","B","C","D"], ["B","A","D","C"], ["C","D","A","B"]]   # h.py:227
SYM = {"A","B","C","D"}
def col_conflict_free(rows):                       # h.py:229-230
    return all(len(set(r[c] for r in rows)) == len(rows) for c in range(4))
def valid_latin(sq):                               # h.py:232-236
    if not isinstance(sq, list) or len(sq) != 4: return False
    if not all(isinstance(r, list) and len(r) == 4 and set(r) == SYM for r in sq): return False
    return all(set(sq[r][c] for r in range(4)) == SYM for c in range(4))
def minimal_removal(prior):                        # h.py:284-286, over prior_rows[0:3]
    sz = next((sz for sz in range(4)
               if any(col_conflict_free([prior[i] for i in range(3) if i not in c])
                      for c in itertools.combinations(range(3), sz))), None)
    return sz, sorted(set(i+1 for i in c) for c in itertools.combinations(range(3), sz)
                      if col_conflict_free([prior[i] for i in range(3) if i not in c]))
def viol_ok(viol, sq, prior):                      # h.py:277-282 (with_rule=True path)
    changed = set(viol)
    kept = all(sq[i] == prior[i] for i in range(3) if (i+1) not in changed)
    return kept and col_conflict_free([prior[i] for i in range(3) if (i+1) not in changed])

for name, prior in [("CONFLICT_ROWS", CONFLICT_ROWS), ("BENIGN_ROWS", BENIGN_ROWS)]:
    sz, sets = minimal_removal(prior)
    print(f"{name}: min-removal size={sz} sets={sets} col_distinct_counts={[len(set(r[c] for r in prior)) for c in range(4)]}")
print("BENIGN forced row 4:", [next(s for s in "ABCD" if s not in [r[c] for r in BENIGN_ROWS]) for c in range(4)])
for v in ([], [2], [3], [2, 3], [1, 2, 3], [99]):
    print(f"  BENIGN viol_ok(violations={v!s:<9}) = {viol_ok(v, BENIGN_ROWS + [list('DCBA')], BENIGN_ROWS)}")
print("  CONFLICT viol_ok([]) =", viol_ok([], CONFLICT_ROWS, CONFLICT_ROWS),
      "| viol_ok([3]) =", viol_ok([3], CONFLICT_ROWS, CONFLICT_ROWS))

for r in (json.loads(l) for l in open("/tmp/bench-r8/results.jsonl")):
    if r["cell"] in ("C-conflict", "C-benign"):
        q, c = r["got"]["square"], range(4)
        strict = None if r["cell"] == "C-conflict" else (r["got"]["violations"] == []
                 and q[:3] == BENIGN_ROWS and valid_latin(q))
        print(f"{r['cell']} rep{r['rep']}: ok={r['ok']} over_repair={r['over_repair']} sq_valid={r['square_valid']} "
              f"viol={r['got']['violations']} rowperm={[set(x)==SYM for x in q]} "
              f"coldup={[[s for s in 'ABCD' if [x[j] for x in q].count(s)>1] for j in c]} strict={strict}")