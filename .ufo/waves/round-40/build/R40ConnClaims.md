# R40ConnClaims — cross-document consistency check (round 40 wave 1)

Seat: R40ConnClaims (connector). Scope: every number and hash in
`plans/round-40-claims.md`, the C1/C2 counter docstrings, `.ufo/waves/round-40/claims/*.txt`,
`.ufo/waves/round-40/first-run/first-run.txt`, checked against each other and against
`git -C <lane> log`. Read-only work; no scratch fixtures were needed (no clone, no writes
outside this report).

## Checks performed (command → result)

### Commit hashes vs git log
- `git log --format='%H %s' -3`:
  - `3077adbc7145726519f60f01426a5d03381ad444` round-40 wave-1 spec/dispatch (tip)
  - `055748f78a3335434f2a4070bb3fb1cf8d0eba1f` first recorded db-wal probe run
  - `bbb109505670192035ef63d7c8b37733e99fa1a3` freeze
- Assignment/claims cite freeze `bbb109505670192035ef63d7c8b37733e99fa1a3` and first run
  `055748f78a3335434f2a4070bb3fb1cf8d0eba1f` — both resolve in-repo (`git rev-parse` exact match).
- Baseline tip `d3a6277f188434458e1d2ce04aff59392c6f0dc6` (claims.md header) resolves; it is the
  round-39 non-author spot-check commit, parent of the freeze. **Agree.**
- `git show --stat bbb1095…`: freeze commit contains exactly the frozen set (claims.md, both
  counters, probe, spec, gate digests file, dry table, 8 captures + SHA256SUMS, all 9 control/witness
  txts, 3 witness modules). `git show --stat 055748f…`: run commit contains exactly
  `corpus/evidence/round40/db-wal-probe.txt` + `first-run/{first-run.txt,run2.txt}`. **Agree.**

### Frozen digests vs files on disk (HEAD)
- `sha256sum` of all 11 paths in `.ufo/waves/round-40/claims/frozen-digests.txt` → all 11 match the
  file's entries, including tool pins `11bb2cad…` (anchor), `853bcb2a…` (ledger), `948d5e1d…` (order),
  which also match the `PINS` dict in `plans/round40_c1_verify.py` and the short digests quoted in
  claims.md. Probe digest `69af65df…`, spec `4af78f4f…`, dry table `688f3475…`, gate `ea638822…`,
  SHA256SUMS manifest `7300c7ea…`, claims.md itself `8b9ed6e8…` — all agree with the C2 counter's
  embedded constants (SPEC_SHA256, GATE_SHA256, PROBE_SHA256, DRY_SHA256, CAPTURES). **Agree.**

### C1 mutant count (21 vs 22 question)
- `MUTANTS` table in `plans/round40_c1_verify.py`: 21 tuples; per-tool split anchor 11
  (A01,A02,A03,A06,A08,A09,A15,A17,A21,A22,A27), ledger 7 (L01,L05,L06,L11,L14,L15,L21), order 3
  (O04,O12,O14) — matches claims.md "Total 21 (anchor 11, ledger 7, order 3)" and every control
  receipt (`MUTANTS total=21 …` in control-c1-nothing, witness-run, control-c1-tool-edited).
- Arithmetic in claims.md: 17 (R39PlanNext §2.7) − 1 (L08 withdrawn) + 2 (A27, L21 per R5) +
  3 (O04, O12, O14) = 21. O13 withdrawal recorded in both claims.md and the C1 counter docstring.
- Grep for a stray "22" across claims.md, all `claims/*.txt`, `first-run/*.txt`: none (the only
  "22/22" in `git log` is round-38's battery, unrelated). **No 21-vs-22 drift anywhere.**

### Witness kills (7)
- `witness-run.txt`: `MUTANTS total=21 killed=7 survived=14`, the 7 killed are exactly
  A27, L01, L11, L21, O04, O12, O14 — matching claims.md ("7 by this freeze's witness run", the
  named list) and the assignment. The other 14 survive, matching "tip-only control … kill none of
  the 14 mutants the witnesses do not target".
- Witness sources exist: `claims/witness/{w_anchor,w_ledger,w_order}.py` (3 modules hosting the 7
  fixtures) and pre-freeze `R39PlanNext/{out_anchor_r5,out_ledger_r5,h_anchor,h_ledger}.py` +
  `dbwal/run1.txt`; spot-check `out_anchor_r5.txt:15` shows `X01-upper rc=1
  classes=['digest-uppercase']` as the A01 witness cell claims (`:15,41`). **Agree.**
- Wording nit (not a number/hash drift): claims.md says "modules in `claims/witness/`: A27, L01,
  L11, L21, O04, O12, O14" — there are 7 fixtures but 3 module files. The count that matters (7)
  is consistent everywhere.

### C1 controls vs claims.md "Before" descriptions
- `control-c1-nothing.txt`: `BATTERY fixtures=0`, `MUTANTS total=21 killed=0 survived=21`,
  `PREDICATE C1 fail`, `exit=1` — exactly as quoted in claims.md.
- `control-c1-tool-edited.txt`: `PINS total=3 mismatched=1 first=plans/anchor_digest_check.py`,
  all 11 anchor mutants `invalid` — as claimed.
- `control-c1-hostile-daemon.txt`: `tampered=0`, A01 SURVIVED, plus the counterfactual line
  confirming the no-namespace rewrite — as claimed.
- C1 frozen predicate wording is identical in claims.md and the counter docstring
  (`PINS total=3 mismatched=0` → `BATTERY …` → `MUTANTS total=21 killed=21 survived=0 invalid=0
  null_detected=0` → `PINS-AFTER mismatched=0` → `PREDICATE C1 pass`, exit 0). **Agree.**

### C2 case counts and splits (28 / 8 / 20)
- Receipt `corpus/evidence/round40/db-wal-probe.txt`: `grep -c '^CASE'` = 28;
  `observed=pass` = 8; `observed=fail` = 20; `match=no` = 0; trailer `regrade cases=28 differ=0` and
  `cases=28 observed_pass=8 observed_fail=20 mismatches=0`. Matches claims.md, the assignment, and
  `first-run.txt`.
- Dry table `db-wal-dry-cases-freeze.txt`: 28 CASE lines, 6 TAG lines, trailer
  `cases=28 predicted_pass=8 predicted_fail=20` — matches claims.md's quote. `diff` of CASE ids and
  of (id, prediction) pairs between dry table and receipt: identical, in order (V4's precondition).
- `first-run.txt`: `run1 rc=0, run2 rc=0, cmp run1 run2: byte-equal`; `sha256sum` of
  `.ufo/waves/round-40/first-run/run2.txt` = `c74c6b91…` = sha256 of the receipt = the digest
  printed as the last line of `first-run.txt`. **Agree on all three.**
- `c2-stage-check.txt`: 28 STAGECHECK lines, `stagecheck cases=28 failed=0` — matches claims.md.
- `control-c2-nothing.txt`: gate P10 `receipt unreadable`, `checks=7 defects=4`, `PREDICATE C2
  fail`, exit 1 — matches the claims.md do-nothing description (P10 fires before the probe runs).
- C2 frozen predicate identical in claims.md and counter docstring (`checks=7 defects=0` →
  `PREDICATE C2 pass`, exit 0). **Agree.**

### Captures and tags
- `corpus/evidence/round40/tb2-db-wal-recovery/`: exactly 8 files + SHA256SUMS (matches claims.md
  "8 files + SHA256SUMS" and the C2 counter's CAPTURES dict of 8);
  `sha256sum -c SHA256SUMS` → all 8 OK; manifest digest matches frozen-digests.txt and the counter.
- Dry-table TAG lines vs `instruction.md`: `fix-wal→:7` ("Fix the WAL file…"), `extract-all→:8`,
  `json-at-path→:9`, `record-format→:12`, `sorted-by-id→:13`, `eleven-records→:13` — all line
  pointers land on the correct requirement sentences.
- Receipt `violates=` tag vocabulary = exactly those 6 tags. **Agree.**

### Headline observations in claims.md vs receipt evidence
- `literals-never-open-db` PPPPPPP (hand-typed JSON passes 7/7) ✓.
- `plain-read-then-solve` PPPPFPF (task's own solve.sh fails exactly 2 tests after a plain
  read-write open) ✓; `xor-wrong-key` PPPPFPF, 5 base rows ✓.
- `truth-bool-value-id5` pass (`True` is an int) ✓; `truth-extra-field` pass ✓;
  `truth-ids-as-floats` = PPFPPPP, and `grep '^def test_' test_outputs.py` puts
  `test_recovered_data_structure` 3rd — "fail only the structure test" ✓.
- `fix-wal` never enforced: receipt shows fix-wal-violating cases observed both pass and fail,
  consistent with "'Fix the WAL file' is never checked".
- Probe docstring: exactly 7 rows copy the R39PlanNext pilot (`untouched`, `oracle-solve-sh`,
  `base-only-ro`, `literals-never-open-db`, `literals-names-1-2-wrong`, `literals-id3-name-wrong`,
  `truth-value-float-id1`) — matches claims.md "Seven of the 28 … graded … by the round-39
  planning seat"; pilot file `R39PlanNext/dbwal/run1.txt` exists. **Agree.**

## Drift list

None. Every checked number and hash agrees across `plans/round-40-claims.md`, both counter
docstrings, all `.ufo/waves/round-40/claims/*.txt`, `.ufo/waves/round-40/first-run/*`, the receipt,
the dry table, the captures manifest, and `git log` (freeze `bbb1095…`, first run `055748f…`,
baseline `d3a6277…`). The only imprecision found is cosmetic: claims.md calls the 7 witness
fixtures "modules in claims/witness/" where 3 module files host 7 fixtures — the count (7) is
consistent everywhere and no number or hash is affected.

VERDICT: drift-0
