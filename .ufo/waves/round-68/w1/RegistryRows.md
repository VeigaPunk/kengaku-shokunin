# RegistryRows — round 68 wave 1, R68-C2 routed defect 4 (check E4)

DRAFT ONLY: no byte of `SKILL.md` was written by this seat. Both rows below are ready to
paste and were tested on a copy of `SKILL.md` under this seat's scratch root
(`/fast/scratch/hyaku/kengaku-r68/RegistryRows`, deleted before the seat returned).

## What was read (working tree as found; uncommitted round-68 bytes are real)

- `plans/round-68-claims.md` in full. E4 = `SKILL.md` carries at least one
  `round67_c1_pipeline_probe` registry row and the `round65-c1-sqlite-probe` row line contains
  `--strict` (`plans/round68_c2_correction_gate.py:131-147`).
- `SKILL.md` registry: heading at line 587, first row 591, last row 687, section ends at the
  next `## ` (line 786); the `round65-c1-sqlite-probe` row (line 686, 1304 bytes); house-format
  siblings `round63-c1-pypi-probe` (683) and `round64-c1-kvstore-probe` (685).
- `plans/round67_c1_pipeline_probe.py` argparse (lines 375-397) and `check_receipt` (:255),
  `selftest` (:357), `setup_error` (:139), `case_app_dir` (:145).
- `plans/round65_c1_sqlite_probe.py` argparse (lines 1147-1191), `strict_failures` (:817),
  `check_receipt_strict` (:949).
- Round-67 record: `plans/round-67-claims.md` (R67-C1 named limitations; R67-C2 clauses s1-s6 and
  its named limitation), `corpus/evidence/round67/pipe/a1-mutants.txt`,
  `.ufo/waves/round-67/w1/ClaimFalsifier/falsify.md` (A1 `no_hooks`, A2 forged pair, A3 ENV-value
  forge), `.ufo/waves/round-67/w1/SecurityScan.md` (M-1),
  `corpus/lessons/round-67-verifier-spotcheck.md` §5 items 3-5.

## Row 1 — new `round67_c1_pipeline_probe` row (insert after the sqlite row)

Ready to paste (one line, 8 cells, no trailing spaces):

```
| `round67_c1_pipeline_probe` | probe | `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt` (flags implemented: `--run --receipt --check-receipt --selftest --work`; the battery form `--run --receipt <path> --work <scratch>` runs the six frozen cases in bwrap with the grader's own pytest module, gloo on 127.0.0.1:12355 under `~/.local/share/kengaku-r67/port-12355.lock`, and copies each junit beside the receipt at `<stem>.junit/<case>.xml`; `--run` refuses to overwrite an existing receipt; `--check-receipt` re-derives the PROBE and GRADER shas, every CASE `case_sha256`/`junit_sha256`/`rc`, and every VECTOR from its own junit against the frozen table — it cannot prove a live run, and four limitations are named: a forged-but-consistent receipt+junit pair passes (ClaimFalsifier A2); a candidate-spawned process can rewrite `/ctl/junit.xml` after pytest's verdict, so the receipt is not an adversarial verdict on a non-lane-authored candidate (SecurityScan M-1 must-fix); the `no_hooks` leg is a substring match for the two literals, not a hook detector (ClaimFalsifier A1); the dictionary-order AFAB check is confirmed at world size 1 only (labrat, round 67)) | `0` pass (`CHECK ok cases=6`, `PREDICATE R67-C1 pass`) · `1` fail (`CHECK findings=<n>`, one `CHECK defect: …` line per finding, `PREDICATE R67-C1 fail`: any vector ≠ the frozen table, a frozen label contradicting its vector, a CASE rc that is not pytest's status, a junit sha or value mismatch, or a duplicate, unknown or malformed CASE/VECTOR line) · `2` SETUP (`SETUP <reason>`, `PREDICATE R67-C1 could-not-evaluate`: unreadable receipt, grader sha drift, missing venv or bwrap, port 12355 busy, a case yielding no junit, timeout; also rc 2 for no mode or `--run`/`--selftest` without `--work`) | `--selftest --work <dir>` (the dir is created if absent) — green on the committed receipt (rc 0) and red on a copy whose `VECTOR q1-ref exists=P` is flipped to `F` (rc 1, 4 findings); prints `SELFTEST green_rc=0 red_rc=1 ok`; tally `corpus/evidence/round68/r67-probe-selftest.txt` (R68-C2 E3) | grader `corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py` sha256 `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f` (`corpus/evidence/round52/graders/SHA256SUMS` line 169); frozen table `FROZEN_TABLE` (order `exists/no_hooks/ws1/ws2`, q1–q6); the six case files under `corpus/evidence/round67/pipe/cases/` (q2-none has none — an empty `/app`); receipt of record `corpus/evidence/round67/pipe/receipt.txt` with `corpus/evidence/round67/pipe/receipt.junit/`; the retained pre-A1 run `corpus/evidence/round67/pipe/receipt-prea1.txt`; mutants `corpus/evidence/round67/pipe/a1-mutants.txt`; claims `plans/round-67-claims.md` | `--run` writes only the `--receipt` path, its `<stem>.junit/`, and `--work`; it binds 127.0.0.1:12355 under `~/.local/share/kengaku-r67/port-12355.lock`; `--check-receipt` reads the lane's committed bytes only | kengaku L1, round 67 |
```

Insertion anchor (run from the lane root):

```
grep -cE '^\| `round67_c1_pipeline_probe` \| probe \|' SKILL.md
awk '/^## Gate\/probe registry/,0' SKILL.md | grep -c 'round67_c1_pipeline_probe'
```

Measured: current tree `0` / `0`; on the scratch copy with this row inserted after line 686
`1` / `1`. The second (section-scoped) form is the E4-relevant one; the first also fails if the
row is pasted without its leading `| `.

## Row 2 — updated `round65-c1-sqlite-probe` row (replaces line 686 in place)

Every existing cell's substance is kept; the additions are `--strict` in the flag list, the
strict verdict codes, the strict clause summary, the A3 ENV-value limitation, the hand-copied
receipt limitation, and the strict evidence pointers.

Ready to paste (one line, 8 cells, no trailing spaces):

```
| `round65-c1-sqlite-probe` | probe | `python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt` (flags implemented: `--lane --work --receipt --check-receipt --strict --selftest --render-table`; the battery form `--lane . --work <scratch> --receipt <path>` compiles the amalgamation in place per case and runs the three legs in bwrap; `--check-receipt` re-derives text fields and cannot prove a live run — named limitation, the live evidence is the per-case BUILD/RUN/FILES lines in `corpus/evidence/round65/battery-run.txt`; a hand-fabricated receipt passes default mode, see the round-65 lesson `## Mistakes`; `--strict` (with `--check-receipt` only; landed round 67, R67-C2) adds clauses s1–s6 — header/`PROBE_VERSION`, grader sha plus committed grader bytes, amalgamation sha, TOOLCHAIN against the CC/GCOV/BWRAP version tokens, RUN rc=0 with the frozen driver, NOBIND delta=0 and BUILD/FILES/ENV presence for G1–G5, VECTOR equals the frozen table — but it does not bind `ENV` values (a forged `ENV … version=` passes: ClaimFalsifier A3), and a hand-copied full receipt passes it; named limitation, R67-C2) | `0` pass (`PREDICATE R65-C1 pass`) · `1` fail — `PREDICATE R65-C1 fail` (any vector ≠ the frozen five, or the G2/G4 fragment, grader sha, amalgamation sha, gcc/gcov line or no-bind clause missing) · `2` setup (grader sha or `def test_` order drift, amalgamation zip sha drift, missing bwrap/gcc/gcov, missing zip) · with `--strict`: `0` `PREDICATE R65-C1 strict-pass` · `1` `PREDICATE R65-C1 strict-fail` (one `CHECK defect: s<n> …` line per violated clause s1–s6; the fabricated fixture gives 24) · `2` `SETUP receipt-missing` | `--selftest --work <existing dir>` — synthesized-receipt text-field fixtures, `SELFTEST pass` (`corpus/evidence/round65/selftest.txt`); strict-mode evidence `corpus/evidence/round67/strict/` — `committed-strict.txt` (`strict-pass`), `fabricated-strict.txt` (24 defects, `strict-fail`), and the 11-fixture clause matrix `fixture-runner.txt` (`RESULT fixtures=11 mismatches=0`; external runner, not the probe's `--selftest`) | grader `b165f850…2993b` (`corpus/evidence/round52/graders/SHA256SUMS` line 167); amalgamation zip `0a9c8e34…d1f9` (S233) | `corpus/evidence/round65/`, `plans/round65_c1_sqlite_probe.py` | kengaku L1, round 65 |
```

Replacement anchors (run from the lane root):

```
grep -cE '^\| `round65-c1-sqlite-probe` \| probe \|.*--strict' SKILL.md
grep -c 'round65-c1-sqlite-probe' SKILL.md
```

Measured: current tree `0` / `1`; on the scratch copy `1` / `1`. The second count staying `1`
is the check that the stale row was replaced, not duplicated. Appending the new row below the
stale one (measured on the copy) leaves E4 **False**: the gate's E4 loop breaks at the first
line containing the name, which would be the old row without `--strict`
(`plans/round68_c2_correction_gate.py:141-145`).

## Verification run (read-only instruments; scratch under the seat root, deleted)

- `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt`
  → `CHECK ok cases=6`, `PREDICATE R67-C1 pass`, rc 0 (the row's primary command).
- `python3 plans/round67_c1_pipeline_probe.py --selftest --work <scratch>`
  → `SELFTEST green_rc=0 red_rc=1 ok`, rc 0. Its 9 stdout lines are byte-identical (clean
  `diff`) to the body of the working-tree tally `corpus/evidence/round68/r67-probe-selftest.txt`
  after that file's recorded command line.
- `--check-receipt <absent path>` → `SETUP cannot read receipt: …`,
  `PREDICATE R67-C1 could-not-evaluate`, rc 2 (the row's `2` code).
- no arguments → rc 2 (help); `--run` without `--work` → `usage: --work <scratch dir> is
  required (scratch is never /tmp)`, rc 2.
- `--selftest --work <nonexistent dir>` → runs and creates the dir, rc 0 (the row says so).
- r65 strict: on `corpus/evidence/round65/sqlite-gcov-probe.txt` → `PREDICATE R65-C1 strict-pass`,
  rc 0; on `corpus/evidence/round66/red/fabricated-r65.txt` → 24 `CHECK defect:` lines,
  `PREDICATE R65-C1 strict-fail`, rc 1; on a missing path → `SETUP receipt-missing`, rc 2.
- r65 default mode on `corpus/evidence/round66/red/fabricated-r65.txt` → `CHECK ok cases=5`,
  `PREDICATE R65-C1 pass`, rc 0 (the existing "hand-fabricated receipt passes it" sentence is
  still true for default mode; only `--strict` refuses it).
- A3 limitation reproduced: `--check-receipt .ufo/waves/round-67/w1/ClaimFalsifier/a3-forges/forge1-env-version.txt --strict`
  → `PREDICATE R65-C1 strict-pass`, rc 0 (ENV value forged, accepted).
- `--strict` at the freeze base is absent (`git show dcc39ea3:plans/round65_c1_sqlite_probe.py |
  grep -c -- '--strict'` → `0`; working tree → `1`), so "landed round 67" is first-hand.
- E4 itself: importing the committed gate's `registry_section` and running its E4 predicates
  gives `pipeline-row=False, sqlite-row-strict=False` on the current tree and
  `pipeline-row=True, sqlite-row-strict=True` on the copy with both rows in place.
- SHA256SUMS cross-checks: line 169 = `23574246…c64f ./torch-pipeline-parallelism/tests/test_outputs.py`;
  line 167 = `b165f850…993b ./sqlite-with-gcov/tests/test_outputs.py`.

## Findings (reported, not edited)

1. **The flag list routed to this seat does not match the committed round-67 probe.**
   The brief says ``--lane --work --receipt --check-receipt --selftest --render-table``; the
   committed `plans/round67_c1_pipeline_probe.py` argparse (lines 375-397) implements
   ``--run --receipt --check-receipt --selftest --work``. There is no `--lane` and no
   `--render-table` in that file (grep: 0 each); the routed list is the round-63/64/65 family
   (`plans/round63_c1_pypi_probe.py`, `plans/round64_c1_kvstore_probe.py`,
   `plans/round65_c1_sqlite_probe.py`). The drafted row follows the committed bytes.
2. **No torch registry row exists to model.** The registry section has no `--torch`/`round66`
   row (`awk '/^## Gate\/probe registry/,0' SKILL.md | grep -ci torch` → 0). The only torch
   mention is the `process-environment` class row at `SKILL.md:81`, which is not a registry
   row. House format was taken from `round63-c1-pypi-probe` and `round64-c1-kvstore-probe`
   (same `--check-receipt` shape). Consequence: round 66's `round66_c1_tensor_probe.py` is also
   unregistered — out of this seat's scope, flagged for the L1's defect routing.
3. **A naive insertion anchor misleads.** `grep -c 'round67_c1_pipeline_probe' SKILL.md` is
   already `1` at the current tree because `SKILL.md:81` cites the instrument path. The row
   anchors above are line-anchored/section-scoped so they read 0→1 rather than 1→2.
4. **Replacement, not append, for the sqlite row.** E4 breaks at the first line containing
   `round65-c1-sqlite-probe`; a stale row left above the updated one fails E4 (measured).
5. **The strict-mode A3 limitation is real, not copied from prose.** A receipt with only
   `ENV G5 version=` replaced by a forged value passes `--strict` (rc 0); the strict clauses
   check ENV line *presence* only (`plans/round65_c1_sqlite_probe.py:918`), while `s4`
   cross-checks only gcc/gcov/bwrap tokens.
6. **The tally pointer is live but uncommitted.** `corpus/evidence/round68/r67-probe-selftest.txt`
   exists in the working tree with `PROBE sha256=03793f4f…`, a `SELFTEST` line and `rc=0`; the
   row cites it as R68-C2 E3 evidence, so it must land with the C2 package or the pointer
   dangles.
7. **Round-67 A1 mutant tally re-read, not re-counted:** `a1-mutants.txt` shows 7 `rc=1`
   mutants plus `v1_vector_before_case rc=0` accepted by design (the base line is the control),
   consistent with R68-C2's "7 refused + 1 accepted by design". The file's header still cites
   the wrong probe sha `32bacf1d…` — the erratum (E1) is the seat that corrects it; the row
   cites the correct `03793f4f…` via the receipt's `PROBE` line and does not repeat the
   header's sha.

## Not done / out of scope

- No edit to `SKILL.md`, `plans/round-68-claims.md`, or any other lane byte; drafts only.
- No git/jj mutation; no installs (nothing needed); no bind on 127.0.0.1:8080 or 12355 (only
  `--check-receipt`/`--selftest`, which bind nothing).
- Not produced: an entry for `round66_c1_tensor_probe.py` (not asked; see finding 2), and no
  change to the class row at `SKILL.md:81` (owned by the C1 integration).

ROWS drafted=2
