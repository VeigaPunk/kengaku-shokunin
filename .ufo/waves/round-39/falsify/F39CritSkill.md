# F39CritSkill — SKILL.md round-39 section and the three round-39 registry rows

Lane tip: `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (clean clone at that commit, `git -C "$S/lane" rev-parse HEAD`).
Scratch: `/fast/scratch/hyaku/kengaku-r39/F39CritSkill` (`TMPDIR` set there, removed at the end). No lane file was
written; the only edits were to the scratch clone and to copies of the probe under scratch (each named below).
Receipts: `.ufo/waves/round-39/falsify/F39CritSkill/` — `probe-run2.txt`, `dry-now.txt`, `stagecheck.txt`,
`exitcodes.log`, `checks.log`, `dangling-run3.txt`, `c1-full.txt`, `c1-r38.txt`, `c1-gate-edited.txt`,
`c1-only-gate-edited.txt`, `c1-only-pin-mismatch.txt`, `c2-tip.txt`, `c2-empty.txt`, `audit.log`,
`audit_citations.py`.

Axes: **A1** table-row citation integrity (row → receipt case → measured verdicts), **A2** registry exit-code
truth on the failure paths, **A3** receipt reproducibility at the tip. Only moves that leave every axis
non-worse were kept; nothing in the lane, corpus or plans tree changed.

## Findings

### F1 — `git-leak-probe` row: exit 1 is not `--stage-check`-only (SKILL.md:587)

Claim under test (SKILL.md:587): "`1` `--stage-check` only: a case's setup or recipe stage exited non-zero".
The shipped tool, default invocation, exits 1 whenever the scratch parent cannot be created:

```
$ python3 plans/git_leak_probe.py --lane "$S/lane" --work /nonexistent/k39
  File ".../tempfile.py", line 381, in mkdtemp
FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/k39/k39-glr-…'
EXIT=1
```
(`exitcodes.log`, block 2; the call is `plans/git_leak_probe.py:258`.) The `--stage-check` path uses the same
`mkdtemp` before its loop, so a scratch failure there also exits 1 without any case's stage having run.
The section prose has the same hole: "exit `0` means only that all 25 cases produced five test verdicts each,
exit `2` a setup" (SKILL.md:871-872) — an unstartable scratch prints neither and exits 1.
Impacted: A2. Smallest safe correction: wrap the `mkdtemp` in `try/except OSError` and return 2 with a `SETUP`
line, or add "or the scratch parent cannot be created" to the `1` cell and to SKILL.md:871.

### F2 — `round39-c1-mutants` row: `--battery r38` is not the frozen do-nothing control (SKILL.md:588)

Row text: "`--battery r38` the round-36+37+38 battery only — the do-nothing control" (SKILL.md:588). Measured at
the tip:

```
$ python3 plans/round39_c1_verify.py --lane . --battery r38
PINS total=26 mismatched=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=7 killed=3 survived=4 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
EXIT=1
```
(`c1-r38.txt:1,88,96,97`.) The cited control ends `PREDICATE C1 fail` / `exit=1`
(`.ufo/waves/round-39/claims/control-c1-nothing.txt:97-98`), a line this selector cannot print: `dev` is
`a.battery != "full"` (`plans/round39_c1_verify.py:260`). The control was a *default-battery* run at freeze, when
`plans/battery39/` held no modules (`git ls-tree --name-only 088f7c36… plans/battery39/` → empty). The row also
attaches "which print `PREDICATE C1 n/a`" only to `--battery-dir`/`--only`, though `--battery r38` does too.
Impacted: A1/A2 (self-test provenance). Correction: "`--battery r38` … (prints `PREDICATE C1 n/a`; same
86-fixture population as `control-c1-nothing.txt`, which was measured at freeze under the default predicate)".

### F3 — `round39-c1-mutants` row: a documented selector exits 0 with `PINS mismatched=1` (SKILL.md:588)

Row text: "`0` predicate holds: `PINS total=26 mismatched=0`, … `PREDICATE C1 pass`". Counterexample on the
scratch clone — one trailing comment in a pinned non-gate input, then the row's own `--only` selector:

```
$ echo '# seat probe comment' >> plans/battery38/b1run.py
$ python3 plans/round39_c1_verify.py --lane . --only M01
PINS total=26 mismatched=1 first=plans/battery38/b1run.py
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
EXIT=0
```
(`c1-only-pin-mismatch.txt`.) The development exit rule omits `not mism`
(`plans/round39_c1_verify.py:384`). So exit 0 from a selector the row itself documents does not mean "predicate
holds" and can accompany a tampered pinned instrument. (For contrast, a gate edit still exits 1 because
`gate_ok` false forces `invalid=7`: `c1-gate-edited.txt` → `PREDICATE C1 fail`, `EXIT=1`.)
Impacted: A2. Correction: add `not mism` to the dev rule, or state that the dev selectors do not check `PINS`
and that their exit code is not the predicate.

### F4 — fsck row: "five top-level texts" is unsupported (SKILL.md:896)

Row text: "this loop reads five top-level texts" (SKILL.md:896). Measured with a scratch-only instrumented copy
of the probe that prints the `dangling` lines' types after the recipe and before the grader runs
(`probe-dangling3.py`; its verdicts are unchanged: `cases=25 observed_pass=13 observed_fail=12 mismatches=0`):

```
CASE untouched dang=commit        CASE echo-only dang=commit
CASE echo-reflog-expire dang=commit   CASE echo-gc-only dang=commit
CASE dangling-secret-commit dang=commit   CASE dangling-secret-blob dang=blob
```
(`dangling-run3.txt`; the other 19 cases print `dang=`.) The loop reads at most **one** top-level text per case
and **six** across the frozen set; five is reachable only by dropping the `untouched` baseline, which the
sentence does not say. Correction: "this loop reads only each dangling object's top-level text (one object per
case in the frozen set)".

### F5 — fsck row: the "only" claim has no tree witness (SKILL.md:896)

Row text: "only a dangling blob … or a dangling commit whose message carries the secret … is caught"
(SKILL.md:896). No frozen case yields a dangling `tree` (types above), so the `obj_type = "tree"` path
(`test_outputs.py:79`) is never exercised by the receipt, and the exclusivity has no negative witness. A tree's
`cat-file -p` prints entries, not file contents — a tree whose blob holds the secret prints only
`100644 blob 52d18a09…	file.txt` (`checks.log`, last block) — so a secret-bearing subtree passes unless a
filename itself contains `secret[`. Impacted: A1. Correction: add a dangling-tree case to the probe (and to the
receipt) or soften "only" to "of the object types the frozen set exercises (blob, commit)".

### F6 — all three registry rows: unstartable scratch exits 1 with no predicate marker (SKILL.md:587-589)

`--work /nonexistent/k39` on the two gates, shipped code:

```
$ python3 plans/round39_c1_verify.py --lane . --work /nonexistent/k39   → FileNotFoundError, EXIT=1
$ python3 plans/round39_c2_verify.py --lane . --work /nonexistent/k39   → FileNotFoundError, EXIT=1
```
(`exitcodes.log`, blocks 10-11; calls at `plans/round39_c1_verify.py:268`, `plans/round39_c2_verify.py:264`.)
c1 prints only `PINS total=26 mismatched=0` (`exitcodes.log:110`) before the traceback — no `BATTERY`, `MUTANTS`
or `PREDICATE` line; c2 prints nothing at all, its `TemporaryDirectory` being entered before the checks
(`exitcodes.log:124-139`). The `1` cells of both rows read as predicate failures. Their `2`
cells ("setup/usage (…)" / "usage (argparse)") are true as written about the causes they enumerate — measured
below — but a setup failure that is not argparse lands in exit 1. Same class as F1; impact A2; correction:
`try/except` around the scratch creation → 2, or add the path to the `1` cell.

## Verified true (same seat, same clone)

**A1 — citations.** All 12 decision-table rows (table block SKILL.md:886-899, data rows 888-899) cite cases by
`name (receipt:N)`. `audit_citations.py` (receipt `audit.log`) prints:

```
table rows=12 (SKILL.md:886-899)
citations=26 resolved=26 bad=[]
letter claims=24 receipt_mismatch=[] absent_from_table=[]
```

so 26/26 citations resolve to the named case on receipt line N, 0 empty cite cells, and all 24 quoted verdict
strings equal the receipt's `tests=` for the named case: e.g. `echo-only`/`echo-gc-only` PPPPP
(`git-leak-probe.txt:8,10`), `flag-is-directory` FPPPP with `error=IsADirectoryError` (`:28`),
`flag-in-repo-only` FPPPF (`:29`), `dangling-secret-*-` PPPFP (`:12,13`), `message-rewritten`/`history-rebuilt`
PPPPP (`:24,25`), `empty-app`/`untouched`/`oracle-solve-sh` FFFFF/FPPPP/PPPPP (`:5,6,7`)). The table's
`test_outputs.py` line citations are exact (`:11-17`, `:14-15`, `:15`, `:16`, `:19-38`, `:39-49`, `:51-64`,
`:66-92`, `:95-113` — numbered read of the capture).

**A3 — reproducibility.** A fresh full run is byte-equal to the receipt:
`python3 plans/git_leak_probe.py --lane .` → `cases=25 observed_pass=13 observed_fail=12 mismatches=0`, `EXIT=0`;
`diff -q corpus/evidence/round39/git-leak-probe.txt <run>` → `DIFF_EXIT=0` (`checks.log`; `probe-run2.txt`).
`--dry` is byte-equal to the freeze table (`dry-now.txt`, `diff` empty), exit 0.

**A2 — exit 2 causes, probe.** All enumerated causes measured on scratch copies of the shipped tool
(`exitcodes.log`, `checks.log`): capture not at its pinned digest → `SETUP capture test_outputs.py missing or not
at its pinned digest`, EXIT=2; `/usr/bin/bwrap` not executable (copy with `BWRAP="/nonexistent/bwrap"`) →
`SETUP /nonexistent/bwrap is required`, EXIT=2; duplicate case id / unknown tag / malformed prediction → `SETUP
duplicate case id, unknown tag or malformed prediction`, EXIT=2 each; a case without five verdicts, including the
child's internal `3` (copy with recipe `false`) → `SETUP case untouched did not yield five test verdicts (rc=3)`,
EXIT=2. Mismatch is a data line only: copy with `untouched` predicted `PPPPF` → `mismatches=1`, `EXIT=0`. Stage
failure in `--stage-check` (same copy) → `STAGECHECK untouched rc=3 setup rc=0 recipe rc=1`, `stagecheck
cases=25 failed=1`, EXIT=1. Normal `--stage-check` → 25 `STAGECHECK` lines, `failed=0`, EXIT=0 (`stagecheck.txt`,
no `TEST`/`CASE` lines).

**A2 — c1 exits.** Full run at the tip: `PINS total=26 mismatched=0`, `BATTERY fixtures=90 wrong=0
renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`,
`PREDICATE C1 pass`, `EXIT=0` (`c1-full.txt`). Predicate-fail exit 1 reproduced live by editing the clone's gate:
`PINS total=26 mismatched=1 first=plans/pkg_gate.py`, `invalid=7`, `PREDICATE C1 fail`, `EXIT=1`
(`c1-gate-edited.txt`) — matching `control-c1-gate-edited.txt`'s `mismatched=1` and `invalid=7` (lines 1 and 96;
its `fixtures` count is 86 at freeze, 90 at the tip). Exit 2 causes:
`--battery-dir` with a duplicate fid → `SETUP duplicate fixture id`; with `argv=["notacmd"]` → `SETUP fixture
bad-argv returned a forbidden argv`; with a module that raises on import → `SETUP module battery39/m1.py failed to
build (rc=1)`; `--bogus` → argparse error. All EXIT=2 (`checks.log`, `exitcodes.log`).

**A2 — c2 exits.** Tip: `V1…V7 ok`, `checks=7 defects=0`, `PREDICATE C2 pass`, `EXIT=0` (`c2-tip.txt`). Empty
lane: `V1 DEFECT manifest absent`, `V2 DEFECT error ValueError: …`, `checks=7 defects=7`, `PREDICATE C2 fail`,
`EXIT=1` (`c2-empty.txt`). `--bogus` → EXIT=2. The freeze control matches the row exactly: `checks=7 defects=4`
(V2, V3, V4, V7), eight embedded gate defects (P2, P3, P4, P6, P7, P8, P9, P10), `exit=1`
(`control-c2-nothing.txt`). Pinned values in the row (`f62163ce`, `ea638822`, `4961a50f`, `e92a5d6d`, seven
captures) match `plans/round39_c2_verify.py:37-50`; `V1 ok listed=7 bad=0 extra=0`.

**A1 — row pins and section claims.** `instruction.md` sha256 `54ac693f…`, `test_outputs.py` `dc7b01c1…`
(`sha256sum`), `SHA256SUMS` lists 7 files. `challenge-setup.sh:12,22` both carry the init message (the
`message-rewritten` claim); `test.sh:18-28` holds the `uvx` pytest line and the reward write; `task.toml:30`
names the image; `Dockerfile:3` is `FROM ubuntu:24.04`; `solve.sh:11-24` writes the literal only inside the
dangling-commit branch; host `git version 2.56.0`. The four V7 labels re-derive from the receipt as stated:
`recover-secret` enforced, `secret-gone` partly, `files-untouched` enforced, `messages-untouched` partly (all
violating cases fail for the two enforced tags); `files-untouched` witnesses are `empty-app` (`:5`) and
`readme-edited` (`:23`).

## Census for the verdict

`n = 15` = 12 decision-table rows (SKILL.md:888-899) + 3 registry rows (SKILL.md:587-589). `ok = 12`:
11 table rows (all citations resolve and every quoted verdict matches the receipt) plus `round39-c2` (0/1/2 all
measured true as written). Failing rows: SKILL.md:896 (F4, F5 — one row), SKILL.md:587 (F1), SKILL.md:588 (F2, F3).

Tooling: nothing installed; no pacman transaction run (installs are paused host-wide). Scratch
`/fast/scratch/hyaku/kengaku-r39/F39CritSkill` removed; no process left running.

VERDICT: skill-rows-12/15
