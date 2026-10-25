# F35LogDraft — errata draft (round-35 LOG/SCORECARD vs landed state)

Seat: F35LogDraft (scribe, wave 2 falsify). Target: `LOG.md` round-35 entry (lines 989–1020)
and `SCORECARD.md` round-35 section (lines 1174–1204) at landed tip
`dfee6fff631ebc5f623ba4506e5c7992a215401c`. All counters re-run in fixture clones at the named
commits (full clone, `--shared`, verified `rev-parse --show-toplevel`, no lane writes).

## E1 (MAJOR) — C2's green state is attributed to the wrong commit

- `LOG.md:1005-1006` says: "C2 landed at `dfcd294c`: `python3 plans/defect_ledger.py --lane .` →
  `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`."
- `SCORECARD.md:1188` (C2 cell) says the same: "after `rows=5 closed=5 observed_pass=5
  mismatches=0`, `PREDICATE C2 pass`, exit 0 at `dfcd294c`".

Re-derivation at the named commit (fixture clone of `dfcd294c`, `git rev-parse HEAD` =
`dfcd294c60a00215c55bc4ce0b620440cd5e402f`):

```
$ python3 plans/defect_ledger.py --lane .
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=fail agree=NO erratum_lines=1 r35_mistake_row=False
rows=5 closed=5 observed_pass=4 mismatches=1
PREDICATE C2 fail
EXIT=1
```

Cause: `r34_d5` requires the S091 row in `corpus/lessons/round-35.md` §Mistakes
(`r35_mistake_row=True`). `corpus/lessons/round-35.md` does not exist at `dfcd294c`
(`git ls-tree -r --name-only dfcd294c` has no `corpus/lessons/round-35.md`); it first lands in
commit `4fe72a9a` (C1 commit, message "… lesson; post-hoc hardening"). At `4fe72a9a` the ledger
is green:

```
$ python3 plans/defect_ledger.py --lane .
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
EXIT=0
```

Green persists at the integrated tip `dfee6fff` (same output, exit 0).

Fix wording (append only): the C2 predicate first holds at `4fe72a9a`; the statement "exit 0 at
`dfcd294c`" is not re-derivable from that commit's tree. The C2 closure's *landing commit* is
`dfcd294c` (drafts moved, mirror roots deleted, manifest, D4/D5 corrections, ledger rows closed),
but the frozen predicate's green state required the round-35 lesson §Mistakes row that only the
subsequent C1 commit `4fe72a9a` supplied.

## N1 (informational) — `.ufo/l0-questions.md:163` resolves only from the fleet root

`plans/round-35-claims.md:10` and `SCORECARD.md:1183` cite `(.ufo/l0-questions.md:163)` for the
open coverage-cap L0. As written (relative to the lane), the path does not resolve: the lane has no
`.ufo/l0-questions.md`. The file exists at the fleet root — `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`,
line 163 is exactly the `kengaku | round-33` coverage-cap decision packet. The reference is
correct with an implied `../` prefix; not a numeric/hash error.

## Verified-clean summary (no errata needed)

- C1 frozen predicate at tip and at `4fe72a9a`: `checks=6 defects=0`, `PREDICATE C1 pass`, exit 0.
- Freeze controls: `control-c1-nothing.txt` (`checks=6 defects=5`, exit 1), `control-c1-skip.txt`
  (`checks=6 defects=5`, exit 1), `control-c2-nothing.txt` (`rows=5 closed=0 observed_pass=0
  mismatches=0`, exit 1), `control-c2-flip.txt` (`rows=5 closed=5 observed_pass=1 mismatches=4`,
  exit 1) — all match the claims file's control sentences.
- `corpus/defects.jsonl`: five rows R34-D1…D5, all `closed`; R34-D1 `recurrence_of` at freeze =
  `R32-N2 (… SCORECARD.md round-32 section)`, at tip = `R33-N1 (… plans/round-33-claims.md:87)`
  — the post-freeze correction is real, and `plans/round-33-claims.md:87` does define N1 as the
  untracked-paths check. `grep recurrence_of plans/defect_ledger.py` hits only the docstring; no
  check reads the field.
- D2: `git ls-tree -r --name-only 11d6453` contains exactly 109,413 committed paths under
  `.ufo/waves/round-34/mut-entries-scratch/` + `build/R34MutRegistry/{mirror,mut}/`; at tip the
  count is 0. The deletion is in `dfcd294c` (109,420 total files changed). The mirror paths remain
  in history/object store.
- D1: three plan drafts exist at tip under `.ufo/waves/round-34/drafts/`
  (`round34_c1_verify.py`, `round34_defects.py`, `round34_mutate.py`); `plans/round34_*` absent;
  the two cited scratch JSONL files (`R34MutGrader.scratch/{pristine,mutated}.jsonl`) are committed
  in `dfcd294c`; no `R34MutReadme-*` directory exists in the live lane or in the tip tree
  (only the authored `R34MutReadme.md` / `R34MutReadme-work.apply.py` build reports). The
  untracked-mirror removal itself is not git-verifiable (they were never tracked).
- Registry: 97 → 100 SOURCES rows (tier A 82 → 85, B 13, C 2); knowledge files 41 → 42; README
  knowledge index rows 41 → 42; census pre/post receipts both exit 0 with the same 15 `W04` rows.
- Probe: receipt `corpus/evidence/round35/tb2-grader-probe.txt` = 21 lines, `cases=18
  observed_pass=5 observed_fail=13 mismatches=0`, grader sha256 `44a05a24…096582` matches the
  capture manifest; counter V5 re-runs the probe and byte-compares (stock ok in both fixture runs).
- Wave-1 reports exist and match their claims: `R35ReopenPins.md` (6/6 re-fetch byte-identical;
  404 for all six `/tasks/`-prefixed URLs), `R35ProbeRerun.md` (deterministic across two lane
  runs and Python 3.13, receipt sha256 `2359d906…`), `R35IndepGrader.md` (`disagreements=0`,
  18/18), `R35ProbeHarnessMut.md` (three mutants a/b/c), `R35CritControls.md` (junk package scores
  `checks=6 defects=0`), `R35CritC2.md` (D4/D5 false-but-labelled lines pass; D1 vacuous in a
  clean clone), `R35MutC1Quotes.md` M4 (straight-quote row survives), `R35CritScope.md`
  (PROVINCE wording).
- Post-hoc hardening: `python3 plans/round35_hardening.py --lane .` at tip → `hardening run=6
  failed=0`, exit 0; committed `hardening-counterexamples.txt` shows each of the five
  counterexamples failing (CE1 failed=3, CE2–CE5 failed=1) with H6 run in the receipt as `--skip
  H6` (the receipt is still failed=0 for the honest copy).
- `PROVINCE.md:230` carries `## Round35 partial frontier admission (2026-10-25)` (the round-35
  paragraph).
- SCORECARD D4 correction text re-derives: `R34C2CounterDraft.md:8` = `SELFTEST cases=10
  failed=0`; `R34MutC2Harness.md:12-13` = `SELFTEST green failed (1)` (exit 1).
