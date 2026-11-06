# ExecHarm — R98 harm battery (BASE 49a1c4f1 vs T 8e37fc65)

Method: isolated `git clone --shared` checkouts at BASE (`cloneB`) and T
(`cloneT`) under scratch `/fast/scratch/hyaku/kengaku-r98/ExecHarm`.
Every command run independently at BASE and at T, rc and last lines
recorded verbatim in `ExecHarm/{B,T,extra}/*.log`. No production edits,
no commits. Tooling: none installed (python3 stdlib only, per RULES.md
pacman guard; no uv/pacman transaction taken).

## Verdict: NO HARM — no green→red, no new DEFECT line

All 22 checks either hold green→green, red→red with identical
predicate/counts/diff-sets, or improve (anchor defects fall 86→45 because
the candidate's provenance file binds previously unbound rows). Every
counter that changed is an expected R98 population/registry delta
(row counts, executed 41→42, file-artifact 32→33 / serialization-schema
7→8), not a new red.

## Candidate scope (exact match)

`git diff --name-status F T` (F=e1a3afd9, T=8e37fc65):

```
M	SKILL.md
M	corpus/SOURCES.md
A	corpus/evidence/PROVENANCE.md
A	corpus/evidence/round98/regexchess-probe.txt
M	plans/grader-population-ledger.json
```

Exactly the five files declared in the assignment. All 13
frozen-instrument sha256 values from `plans/round-98-claims.md`
(frozen-instruments table) match at T (`INSTRUMENTS-MATCH`,
`T_tab.txt` vs `T_sha.txt`); all 4 candidate-bytes sha256 match
(`CANDIDATE-MATCH`, `T_ctab.txt` vs `T_csha.txt`).

## Side-by-side battery (rc, predicate, DEFECT count)

Run inside cloneB/cloneT. Command → BASE / T:

| Check (registry command) | BASE | T | Δ |
|---|---|---|---|
| `python3 grader.py` (hermetic-grader) | rc=0 PASS, n=733 mismatches=0 | rc=0 PASS, same | identical |
| `plans/round52_c2_registry.py --lane .` | rc=1 R52-C2/R73-C1 fail (pre-existing) | rc=1 same predicates, MISSING set identical (19 files) | counts only: files 163→164, plans_seen 133→135, ADVERTISED 188→192, REGISTERED 169→173 (4 round98 rows) |
| `plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .` | rc=1 R63-C2 fail, ROWS n=16 count_mismatch=0 | rc=1 identical line | byte-identical log |
| `plans/round68_capability_table.py --lane .` | rc=0 R68-A3 pass | rc=0 same | identical |
| `plans/round72_c2_routed_defects.py --lane .` | rc=0 R72-C2 pass DEFECTS n=0 | rc=0 same | identical |
| `plans/round73_c2_registry_audit.py --lane .` | rc=0 R73-C2 pass | rc=0 same | identical |
| `plans/round74_c1_registry.py --lane .` | rc=1 R52-C2/R74-C1 fail | rc=1 same predicates; counts files 163→164, REGISTERED 170→174 | counts only |
| `plans/round74_c2_registry_audit.py --lane .` | rc=1 R74-C2 fail, 1 MALFORMED row (round88-fixgit-probe) | rc=1 same, INSTRUMENTS 170→174 | identical defects |
| `plans/round75_c2_registry_audit.py --lane .` | rc=1 R75-C2 fail, DEFECTS n=2 (round88 MALFORMED + round77 flag-not-declared) | rc=1 same, INSTRUMENTS 170→174 | identical defects |
| `plans/round78_c1_class_member_ledger.py --lane .` | rc=1 R78-C1 fail DEFECTS n=121 | rc=1 same, DEFECTS n=121 | k diffs only: file-artifact 32→33, serialization-schema 7→8 (the R98 claim itself); COUNT-DRIFT/COVERAGE-REGRESSION lines differ only in that digit |
| `plans/round79_c1_population_ledger.py --lane .` | rc=1 R79-C1 fail DEFECTS n=1 (mteb-retrieve SUBJECT-MISMATCH, pre-existing) | rc=1 same 1 defect | executed 41→42, regex-chess now `executed` (evidence regexchess-probe.txt), unexecuted 47→46 — expected R98-C1 flip |
| `plans/round82_c1_plans_registry.py --lane .` | rc=1 R82-C1 fail DEFECTS n=12 | rc=1 same 12 | byte-identical log |
| `plans/anchor_digest_check.py --lane .` | rc=1 rows=317 tokens=201 defects=86 | rc=1 rows=325 tokens=209 defects=45 | see anchor section below |
| `plans/anchor_digest_check.py --lane . --verbose` | rc=1 rows=317 defects=86 | rc=1 rows=325 defects=45 | same as above |
| `plans/anchor_line_check.py --lane .` | rc=0 live=0 cells=0 rows=317 captured=112 | rc=0 live=0 cells=0 rows=325 cited 125→132 captured 112→119 | captured+7 = new regex-chess flat captures |
| `sources-census.sh validate --root … kengaku` | rc=0, W04 warnings S266-S270 | rc=0 identical | byte-identical log |
| `plans/round94_freeze_integrity.py --lane . --freeze F --rev T --claims plans/round-98-claims.md --work DIR` (T only; F not an ancestor at BASE) | — | rc=0 `PREDICATE freeze-integrity pass`, instruments=13 intact=13 broken=0 | freeze clean |
| `plans/round97_gate_selftest_census.py --lane . --rev REV` (r97 census) | rc=0 R97-C2 pass, rows=171 | rc=0 R97-C2 pass, rows=175 | +4 registry rows, no findings |
| `plans/round95_c2_counter.py --lane . --rev REV --work DIR` | W4 fail freeze=d9cd18a7 summary=(11,10,1) — pre-existing (round95_c1_replay touched=2 after its freeze) | W4 fail same freeze/summary, same touched=2 | identical (log truncated by the long battery; W4 line and W1-W5 preamble identical at both revs) |

### Anchor gate: no new DEFECT, 41 cleared, 0 added

- BASE: `rows=317 tokens=201 defects=86` (73 anchor-unbound,
  9 digest-wrong-capture, 2 token-outside-anchor, 1 capture-unanchored,
  1 digest-unknown).
- T: `rows=325 tokens=209 defects=45` (33 anchor-unbound,
  8 digest-wrong-capture, 2 token-outside-anchor, 1 capture-unanchored,
  1 digest-unknown).
- DEFECT-id set intersection is exactly the T set; `comm` shows
  **zero** new ids in T. 41 ids cleared — the R98-C2 population cleared by
  the new PROVENANCE.md (S181,S182,S183,S201,S224,S230,S234,S241,S243,
  S273-S278,S280,S282-S284,S290-S292,S297,S299,S301-S305,S308,S310-S313,
  S317-S320,S322,S323).
- **S326-S333: none flagged** at T (`grep -E 'S32[6-9]\|S33[0-3]'`
  over T/anchor.log → NONE), confirming C1 L10: the new rows are bound by
  the flat captures and not flagged by the BASE gate bytes.

## Files changed
None (read-only battery; all writes confined to scratch clones +
`ExecHarm.md` / `ExecHarm/`).

## Evidence retained (exact)
- `ExecHarm/{B,T}/*.log` — 16 checks × 2 revs, full stdout+stderr+rc.
- `ExecHarm/extra/freeze98.log` — round98 freeze-integrity at T,
  rc=0 pass (`Instruments 13/13 intact`); `freeze98B.log`, `r95c2{,B}.log`,
  `r97census{,B}.log`.
- `ExecHarm/{T_tab,T_sha,T_ctab,T_csha}.txt` — claims tables vs computed
  sha256 (both diffs empty).

## Risks / blockers
- Collateral reds at BASE (r52-c2, r63, r74-c1/c2, r75-c2, r78-c1,
  r79-c1, r82-c1, r95 W4) are carried over unchanged at T; flagged here
  as pre-existing, not round-98 harm.
- `round95_c2_counter`'s long battery was killed once by the harness
  600s timeout during a chained run; re-run individually, W1-W5
  preamble and the failing W4 line are identical at both revs
  (receipts may end mid-W5 but every pass/fail line before truncation
  agrees).
- C1/C2 probes themselves were not re-run (L1's measurement at T stands);
  this seat only covered the standing registry/ledger/source battery.

Report: .ufo/waves/round-98/w1/ExecHarm.md
