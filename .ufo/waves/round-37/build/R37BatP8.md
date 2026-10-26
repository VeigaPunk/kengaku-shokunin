# R37BatP8 — C1 battery module for gate clause P8 (mutants M34–M38)

Seat: R37BatP8 (executor, kengaku round 37 wave 1). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Frozen artefacts read, never written: `plans/round-37-claims.md` (in full), `plans/round37_c1_verify.py`
(mutant list + Ctx API), `plans/pkg_gate.py` (`c_readme`, `INDEX_ROW`, `Package.load`),
`plans/pkg-spec-r35.json`, `plans/battery37` (absent at the time of writing, so this module lives in my
report subdir as instructed), the freeze example `.ufo/waves/round-37/claims/example_battery/ex_p3_words.py`.

## Deliverable

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatP8/battery/p8.py`
(stdlib only: `pathlib`; fids all prefixed `p8-`).

sha256 (command: `sha256sum …/battery/p8.py`, output kept at `R37BatP8/receipts/p8-module-sha256.txt`):

```
cfbe5cf93d46ee30f90e4603367c39bf793aad7f205367182388bd224a7e76ff  .../R37BatP8/battery/p8.py
```

## Design — one fixture per P8 branch, single defect each

Every builder starts from `ctx.genuine_package(d)` (the genuine round-35 package, `spec` =
`pkg-spec-r35.json`, entry `corpus/knowledge/tb2-protein-assembly-grader.md`), edits **only**
`corpus/README.md` or adds one file under `corpus/knowledge/`, stages with `ctx.git_add(d)` (index only,
no commit), and returns `["package", "--root", str(d), "--require-clean-tree"]` (no `--rerun`, no `--spec`).

| fid | edit | gate branch silenced by the mutant | mutant | declared `defects` |
|---|---|---|---|---|
| `p8-readme-deleted` | `corpus/README.md` unlinked | `c_readme`: `return False, "README unreadable"` | M34 | `["P8"]` |
| `p8-index-row-duplicated` | the entry's index row duplicated verbatim next to itself | `c_readme`: `bad.append(f"index rows for knowledge/{entry_name}={len(rows)}")` | M35 | `["P8"]` |
| `p8-index-row-missing-sid` | the entry's index row loses one registry S-id (derived as `sorted(ctx.spec["rows"])[-1]` = S107, formatted `", S107"` → `""`) | `c_readme`: `bad.append("index row does not cite every registry row")` | M36 | `["P8"]` |
| `p8-coverage-bullet-removed` | the one line starting `"- "` that names both the entry and `evidence/round35/tb2-grader-probe.txt` is deleted | `c_readme`: `bad.append("no coverage bullet naming the entry and its receipt")` | M37 | `["P8"]` |
| `p8-extra-knowledge-file` | `corpus/knowledge/zz-unindexed-fixture-note.md` added, not indexed | `c_readme`: `bad.append(f"knowledge files={len(files)} index rows={len(indexed)}")` | M38 | `["P8"]` |

Why exactly one clause fires (`{"P8"}` and nothing else) for all five: no other package clause reads
`corpus/README.md` or `corpus/knowledge/*` — P1 reads `frozen_instruments` (`plans/tb2_grader_probe.py`,
`plans/round35_c1_verify.py`, `plans/defect_ledger.py`), P2 the receipt, P3/P4 `spec["entry"]`, P5 the
capture dir + `SHA256SUMS`, P6 `spec["sources"]`, P7 the entry, P9 the git tree. M35's duplicate row keeps
the `{files} == {indexed}` set equal, M36's dropped S-id keeps the row count at one, so no second P8 branch
fires either. Observed reference results (receipt below) confirm `observed_defects=P8` for all five.

No builder inspects the directory name; the counter's renamed run reports `renamed_disagree=0`.

## Proof run (full output)

Command (run from the lane; `$S` = `/fast/scratch/hyaku/kengaku-r37/R37BatP8`, `TMPDIR="$S"`):

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round37_c1_verify.py \
  --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatP8/battery \
  --only M34,M35,M36,M37,M38 --work "$S/w"
```

exit 0. Output (byte copy: `R37BatP8/receipts/p8-counter-run.txt`):

```
GATE plans/pkg_gate.py sha256=frozen
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-P1 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P2 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P3 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P4 expect=reject declared=- observed_rc=1 observed_defects=P6 ok
FIXTURE r36-P5 expect=reject declared=- observed_rc=1 observed_defects=P1 ok
FIXTURE r36-P6 expect=reject declared=- observed_rc=1 observed_defects=P9 ok
FIXTURE r36-P7 expect=reject declared=- observed_rc=1 observed_defects=P1,P3,P6,P9 ok
FIXTURE r36-L1 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L2 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L3 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L4 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L5 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE r36-L6 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE p8-readme-deleted expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-index-row-duplicated expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-index-row-missing-sid expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-coverage-bullet-removed expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-extra-knowledge-file expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
BATTERY fixtures=19 wrong=0 renamed_disagree=0
MUTANT M34 P8 killed by=p8-readme-deleted -- README unreadable
MUTANT M35 P8 killed by=p8-index-row-duplicated -- index rows for the entry not exactly one
MUTANT M36 P8 killed by=p8-index-row-missing-sid -- index row does not cite every registry row
MUTANT M37 P8 killed by=p8-coverage-bullet-removed -- no coverage bullet naming entry and receipt
MUTANT M38 P8 killed by=p8-extra-knowledge-file -- knowledge files differ from index rows
MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

`fixtures=19` = the 14 frozen round-36 fixtures plus my 5; `wrong=0` includes the fact that every one of
my declarations matches the unmodified gate; `null_detected=0`; `invalid=0` (all five `old` strings occur
exactly once in the frozen gate and every mutant compiles).

## Load-bearing ablation (each fixture removed in turn)

Method: a copy of `p8.py` in scratch with one line appended —
`FIXTURES = [f for f in FIXTURES if f["fid"] != "<fid>"]` — reloaded to confirm the fid was gone, then the
counter re-run with `--battery-dir <copy dir> --only <matching mutant>`. Output: `receipts/p8-ablation.txt`.

| removed fixture | mutant | result | killed | survived | wrong | renamed_disagree |
|---|---|---|---|---|---|---|
| `p8-readme-deleted` | M34 | `MUTANT M34 P8 SURVIVED -- README unreadable` | 0 | 1 | 0 | 0 |
| `p8-index-row-duplicated` | M35 | `MUTANT M35 P8 SURVIVED -- index rows for the entry not exactly one` | 0 | 1 | 0 | 0 |
| `p8-index-row-missing-sid` | M36 | `MUTANT M36 P8 SURVIVED -- index row does not cite every registry row` | 0 | 1 | 0 | 0 |
| `p8-coverage-bullet-removed` | M37 | `MUTANT M37 P8 SURVIVED -- no coverage bullet naming entry and receipt` | 0 | 1 | 0 | 0 |
| `p8-extra-knowledge-file` | M38 | `MUTANT M38 P8 SURVIVED -- knowledge files differ from index rows` | 0 | 1 | 0 | 0 |

Each ablation leaves `BATTERY fixtures=18 wrong=0 renamed_disagree=0`: the remaining four fixtures still
match their declarations, and the removed branch has no other killer. So each fixture is necessary and
sufficient for its own mutant, and no fixture cross-kills another's mutant (single-defect clarity holds in
both directions).

## Calibration / operability notes

- Gate at freeze digest throughout: the counter prints `GATE plans/pkg_gate.py sha256=frozen`; I never
  edited it, the counters, the probe or the mutant list.
- The two-line difference between the 6 s proof run and the 19–21 s ablation runs is the counter's full
  battery build (19 vs 18 fixtures) and gate invocations per mutant; no fixture is slow (the fastest case,
  M34, needs one `git add` of the genuine package only, no `--rerun`, so P10 never executes).
- Hard-coded strings avoided where the spec supplies them: entry name from `ctx.spec["entry"]`, README path
  from `ctx.spec["readme"]`, knowledge dir from the parent of `ctx.spec["knowledge_glob"]`, receipt rel from
  `ctx.spec["receipt"].split("/", 1)[1]`, the dropped S-id from `sorted(ctx.spec["rows"])[-1]`. A builder
  raises `RuntimeError` (counter `SETUP` exit 2) if the expected single index row / bullet is not found,
  rather than silently building an unchanged package.
- Limit (same as the frozen claim's): demonstration is observational — each fixture shows a branch is
  reached and its verdict observable; it does not show that the P8 check is the right check for a package.
  M36's fixture depends on the last key of the frozen spec's `rows` (S107) being cited in the entry's index
  row, which it is at `corpus/README.md:68`.

## Boundaries respected

Wrote only `R37BatP8/` under `.ufo/waves/round-37/build/` (module + three receipts) and scratch
`/fast/scratch/hyaku/kengaku-r37/R37BatP8` (removed: `ls` now says *No such file or directory*). No lane
`corpus/`, `plans/`, SCORECARD/LOG/README/SKILL/PROVINCE/SHONEN edits; no `git`/`jj` mutation anywhere; no
subagents or background jobs; no tool installs (nothing needed).

VERDICT: battery-p8-killed-5/5-wrong-0
