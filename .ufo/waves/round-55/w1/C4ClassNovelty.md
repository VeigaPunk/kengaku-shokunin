# C4ClassNovelty — scoped findings (R55-C3 class-novelty attack)

**Verdict: NOVEL — not a re-label of r45 membership.** The R55-C3 class claim
("order-insensitive full-multiset equality over whitespace-split tokens") survives this attack.

Verified ground: `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` sha256
`a540714e…8f286` = the frozen pin; the whole score is
`move = move_file.read_text().strip().split()` + `assert sorted(move) == sorted(["g2g4", "e2e4"])`.

Axis table (partial credit / order / duplicates-extras / normalization / split):

| Grader | Partial credit | Order | Duplicates/extras | Normalization | Split |
|---|---|---|---|---|---|
| r45 password-recovery (membership) | none, extras free (`decoys-1000` P) | free | tolerated | universal NL + strip; case-sensitive | newline |
| r36 regex-log (list equality) | none | enforced | exact | input strip | n/a |
| r46 polyglot (listing + literal) | none | enforced | exact | stdout.strip() | n/a |
| r35 protein-assembly (chain) | none | enforced positionally | repeats fail incidentally | lower + rstrip, 1 line | single line |
| r40 db-wal-recovery (JSON exact) | none | enforced (`ids == sorted(ids)`) | exact (`len(ids)==len(set(ids))`) | typed JSON parse | n/a |
| **r55 chess-best-move (sorted multiset)** | **none — partial fails** | **free** | **exact — extras AND dups fail** | strip + WS split; case-sensitive | **any whitespace** |

Decisive counterexample to the re-label hypothesis: content `g2g4 e2e4 h7h5` (both required
tokens + one decoy) → r45-style membership PASSES, r55 multiset FAILS (demonstrated in host
python3, 13 shapes, exit 0). r45's own `decoys-1000` passes membership and would fail multiset.
Converse granularity split: `g2g4 e2e4` on ONE line passes r55, fails newline-membership of both
tokens. Sweep of all captured `test_outputs.py`: no prior grader decides by
`sorted()==sorted()`/`Counter()`; db-wal's `ids == sorted(ids)` enforces order, it does not ignore
it.

**Cap on the entry (reported, not buried):** novelty is combinatorial. No single axis is new —
order-freeness (r45), exact count/multiplicity (r36, r46, r40) each predate r55. The entry must
claim the conjunction (order-free AND multiplicity-exact AND whitespace-token over a bare token
file) and must keep "no normalization" qualified to case/digit-width (`.strip().split()` is real
normalization; the claims file already words it correctly). A per-axis novelty claim in the entry
would be falsifiable from r36/r40 receipts.

Full ruling with quotes: `.ufo/waves/round-55/w1/C4ClassNovelty/ruling.md`. Seat report:
`.ufo/waves/round-55/w1/C4ClassNovelty/report.md`.
