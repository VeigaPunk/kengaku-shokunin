# C4ClassNovelty — seat report (kengaku round 55, wave 1)

Seat question: is order-insensitive full-multiset equality over whitespace-split tokens REALLY a
graded-artefact class new to this lane, or a re-label of r45's password-recovery membership?

## What I ran

1. `read plans/round-55-claims.md` — the frozen R55-C3 claim wording. (No exit code; read tool.)
2. Read the four assigned knowledge entries in full:
   `corpus/knowledge/tb2-password-recovery-grader.md` (r45),
   `tb2-regex-log-grader.md` (r36), `tb2-polyglot-c-py-grader.md` (r46),
   `tb2-protein-assembly-grader.md` (r35).
3. Verified the capture under test:
   - `sha256sum corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` →
     `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` (matches the frozen pin in
     the claims file). Exit 0.
   - Read the file (25 lines): decision is `move = move_file.read_text().strip().split()` +
     `assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"`. Byte-exact match with the
     claim's quoted assert.
4. Semantics demonstration, host python3 inline heredoc (no files written), exit 0: implemented
   the r55 rule and the r45 rule each as a function and evaluated 13 content shapes. Key results:
   r55: exact-both True; reordered True; one-token-only False; both-plus-decoy False;
   duplicated-correct False; one-per-line True; `G2G4` case-variant False; padded-ws True.
   r45: answer-alone True; answer+1000-decoys True; answer-duplicated True; joined-line False;
   crlf-line True.
5. Novelty sweep: `grep -rn "sorted(\|Counter(" corpus/evidence --include=test_outputs.py` → the
   only graded-artefact sorted-equality decision in the whole corpus is chess-best-move;
   db-wal-recovery has `ids == sorted(ids)` (order-enforcing) + `len(ids) == len(set(ids))`;
   schemelike/sparql `sorted(` hits are harness-side listing/display, not artefact equality.
   Follow-up `grep -rln "== sorted\|Counter("` confirms the same set. Exit 0/1 as expected.
6. Read `tb2-db-wal-recovery-grader.md` (r40) in full for the nearest-neighbour axis table row.
7. `git rev-parse HEAD` → `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (the freeze commit). Exit 0.

No clone was needed (read-only analysis of in-repo captures). No scratch dir was created; nothing
needed `/fast/scratch`. No tools installed. No git/jj mutations. No subagents dispatched.

## Files written

- `.ufo/waves/round-55/w1/C4ClassNovelty/ruling.md` — the ruling (per-entry axis table + final
  ruling + evidence log).
- `.ufo/waves/round-55/w1/C4ClassNovelty/report.md` — this file.
- `.ufo/waves/round-55/w1/C4ClassNovelty.md` — scoped findings for the L1 (trailer path).

## Verdict

**NOVEL — not a re-label of r45.** Decisive discriminator: extras/duplicates. Content with both
required tokens plus one decoy (`g2g4 e2e4 h7h5`) passes r45-style membership and FAILS r55's
sorted multiset (demonstrated); r45's own `decoys-1000` receipt case (answer + 1000 shuffled
decoys) passes membership and would fail multiset. The classes cross on granularity too (any-
whitespace vs newline split). It differs from every exact-equality prior class (r36 regex-log,
r46 polyglot, r40 db-wal-recovery) on order: those enforce it, r55 ignores it. R35 is a positional
chain, not an equality. The R55-C3 class claim stands.

**Cap that must ride with the entry:** novelty is combinatorial, not per-axis. Order-freeness is
old (r45); exact count/multiplicity is old (r36, r46, r40). The entry must phrase the class as
the conjunction (order-free AND multiplicity-exact AND any-whitespace-token over a bare token
file) and must keep "no normalization" qualified to case/digit-width (strip + whitespace split
are real normalizations; the claims file already words it correctly).

## Defects found

None in the lane. Two wording cautions for the C3 entry author (carried in the ruling):
(1) per-axis novelty claims would be falsifiable from r36/r40 receipts;
(2) unqualified "no normalization" would be false of `.strip().split()`.

## Dead ends

None. The one apparent counterexample (db-wal-recovery "the id multiset is checked exactly")
survived inspection as the nearest neighbour but enforces order and grades structured JSON, so it
does not collapse the class.
