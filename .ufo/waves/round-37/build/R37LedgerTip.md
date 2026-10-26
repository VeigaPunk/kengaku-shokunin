# R37LedgerTip — every closed routed defect's check re-run at the round-37 lane tip

**Assignment.** considerthese/2026-10-25.md proposal 2(a) (`considerthese/2026-10-25.md:39-45`): re-run
every closed routed defect's check at the tip. Tool: `ledger_tip.py` (this dir). Result:
**rows=9 closed=9 observed_pass=9 mismatches=0 at tip `44b7298`** — no row fails, so no
regression-or-stale-pin finding of the requested kind. The rest of this report is the calibration
that makes that zero mean something, and three structural findings about how the ledger *counts*
when a row does fail.

- Lane tip examined: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` →
  `44b7298ae1e03791173097cef0e898285f238870` ("round-37: wave-1 spec and validated dispatch"),
  which is `ca7904` (claim freeze) + the probe commit `5c7b34e` + the wave-1 dispatch commit.
- Runner: `.ufo/waves/round-37/build/R37LedgerTip/ledger_tip.py`
  sha256 `67cb3966c0dfc56f29997a7fc3e3200d07d7096f0f35bf70adb8fae5d051a271`.
- No ledger, no check body, no lane file edited. All work on `git clone --shared` under
  `/fast/scratch/hyaku/kengaku-r37/R37LedgerTip/` (removed at the end; receipts copied here first).

## 1. What runs

`ledger_tip.py` clones the lane (`git clone -q --shared`, refuses a non-existent/dirty result and
verifies `rev-parse --show-toplevel` equals the clone), imports the clone's **tip bytes** of the two
check modules by path (`importlib`), and calls every row's named check with the clone as `lane`:

| ledger | check module | rows |
|---|---|---|
| `corpus/defects.jsonl` | `plans/defect_ledger.py` → `CHECKS` | R34-D1 … R34-D5 |
| `corpus/defects-round35.jsonl` | `plans/round36_c1_verify.py` → `CHECKS` | R35-D1 … R35-D4 |

It prints, per row, `<id> status=<s> observed=<pass|fail> agree=<yes|NO> <note> ledger=<file>
kind=<pin|live>` and then `rows=… closed=… observed_pass=… mismatches=…`; a check that raises is an
observed **failure**, never a pass (same rule as both checkers of record); `mismatches` = closed-row
check fails + open-row check passes, i.e. the two checkers' own definition. Exit 0 iff
`rows>0 and mismatches==0`. `--lane <tree>` is a control mode that skips the clean-tree refusal so a
deliberately broken clone can be used (below).

`kind` is **my** annotation, not ledger data: `live` = the check exercises behaviour (package gate,
battery, line fixtures, repo-state query); `pin` = the check only re-reads closure bytes (a path
count, a digest list, a correction/erratum line, a quote's presence in a frozen capture).

## 2. The tip run (receipt `ledger-tip-run1.txt`, sha256 `46c77d7f…ab73`)

```
$ export TMPDIR=/fast/scratch/hyaku/kengaku-r37/R37LedgerTip
$ python3 ledger_tip.py --source /home/vgpnk/Projects/shokunin/kengaku-shokunin --work "$TMPDIR/run"
TIP commit=44b7298ae1e03791173097cef0e898285f238870 clone=/fast/scratch/hyaku/kengaku-r37/R37LedgerTip/run/lane
R34-D1 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=live
R34-D2 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
R34-D3 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
R34-D4 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
R34-D5 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
LEDGER corpus/defects.jsonl rows=5 closed=5 observed_pass=5 mismatches=0
R35-D1 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=live
R35-D2 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=live
R35-D3 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=pin
R35-D4 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=pin
LEDGER corpus/defects-round35.jsonl rows=4 closed=4 observed_pass=4 mismatches=0
rows=9 closed=9 observed_pass=9 mismatches=0
EXIT=0   (wall 2.04 s)
```

Per-row observation notes (`--keep-notes`, receipt `ledger-tip-run2-notes.txt`, sha256
`ed60d355…f9ab`) — these are the numbers behind each pass:

| row | class | kind | note at tip |
|---|---|---|---|
| R34-D1 | uncommitted-round-work | live | `untracked=0` |
| R34-D2 | committed-scratch-bloat | pin | `committed_mirror_paths=0` |
| R34-D3 | receipt-claims-unbacked-manifest | pin | `listed=6 evaluator_listed=True bad=0` |
| R34-D4 | scorecard-misattribution | pin | `correction_lines=1` |
| R34-D5 | false-refusal-reason | pin | `erratum_lines=1 r35_mistake_row=True` |
| R35-D1 | counter-accepts-junk | live | `fixtures=14 false_green=0 false_red=0 unevaluated=0 tip_package_rc=0` |
| R35-D2 | working-tree-and-token-cooccurrence-checks | live | `untracked_anywhere=0 line_fixtures_wrong=0/6` |
| R35-D3 | narrow-scratch-roots | pin | `committed_nested_wave_paths=0` |
| R35-D4 | gate-row-omission | pin | `erratum_lines=1 recount=13 + 23 + 1 = 37 stated_denominator=38` |

Determinism: a third fresh clone (`run3`) produced output byte-equal to `run1` after normalising the
work-dir path — `cmp` clean, both sha256 `1104ee6bd29151880a4490bb33e259171f55eebe50034b074f97742d515151aa`.
Non-mutation: after a run the clone is `git status --porcelain` empty (2 ignored `__pycache__` dirs),
so the checks write nothing into the tree they measure.

`R35-D1`'s `fixtures=14 … tip_package_rc=0` is the round-36 C1 battery re-derived at the tip and the
genuine round-35 package re-run through `plans/pkg_gate.py --rerun --require-clean-tree`: the round-36
counter's own frozen line still holds at round-37.

## 3. Are the passes load-bearing? Nine controls (all receipts `control-ctl*.txt`)

Each control is a fresh `--shared` clone under scratch, mutated once, then run with `--lane`; `dirty=1`
appears in every control header. `mismatches` is the runner's own count.

| control | single mutation (in the clone) | rows= | mism | which rows |
|---|---|---|---|---|
| ctlA | delete `SCORECARD.md:1178` line `- **D4 correction (round 34 C2):**` | 9 | 3 | R34-D4 fail (`correction_lines=0`); R35-D1, R35-D2 **crash** `AttributeError: 'NoneType' object has no attribute 'replace'` |
| ctlB | add one untracked file `.ufo/waves/round-34/stray-untracked.txt` | 9 | 3 | R34-D1 (`untracked=1`), R35-D1 (`tip_package_rc=1`), R35-D2 (`untracked_anywhere=1`) |
| ctlC | append a quote-shaped row **after** the last `##` section of the package entry (tracked edit) | 9 | **0** | none — negative control, see §4.3 |
| ctlD | rewrite the 8 `## Located quotes` rows' quotes to one word each (tracked edit) | 9 | 1 | R35-D1 `false_red=1 … tip_package_rc=1` |
| ctlE | append a comment line to the captured `.ufo/waves/round-34/…/tb2-eval/test_outputs.py` | 9 | 1 | R34-D3 `bad=1` |
| ctlF | append ` (reflowed)` to the D5 erratum line in `corpus/lessons/round-34.md` | 9 | 0 | none (all three readers still match) |
| ctlF2 | **delete** that D5 erratum line | 9 | 3 | R34-D5 fail (`erratum_lines=0`); R35-D1, R35-D2 crash `TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'` |
| ctlF3 | reword that line `is present` → `appears present` | 9 | 2 | R35-D1 `false_red=1` (fixture L4), R35-D2 `line_fixtures_wrong=1/6`; **R34-D5 still passes** |
| ctlG | flip `R34-D2`'s status to `open` in the clone's `corpus/defects.jsonl` | 9 | 1 | R34-D2 `status=open observed=pass agree=NO` — the stale-self-assessment direction bites |

So every row's check can fail, the counter catches both disagreement directions, and the live rows
bite on real content (`ctlD`, `ctlE`, `ctlB`), not just on file presence. The runner's own contract was
measured in the same pass: `EXIT=1` for the seven controls with `mismatches>0`, `EXIT=0` for ctlC and
ctlF (`mismatches=0`) — every `control-ctl*.txt` ends with its true exit code. The nine controls were
executed twice (independent clones per run) with identical per-control mismatch counts
(3 3 0 1 1 0 3 2 1), so the control outcomes are deterministic, not a one-off.

## 4. Findings (structural; all measured, none of them a failing row)

### 4.1 One text edit is counted against up to three unrelated classes (ctlA, ctlF2, ctlF3)
The D4/D5 correction lines are **shared inputs**. `r34_d4`/`r34_d5` pin them as closure bytes, and
`plans/round36_c1_verify.py:161-165` (`d4_line`) / `:168-173` (`d5_line`) re-read the *same* lines to
build the directional line fixtures used by R35-D1 and R35-D2 (`build_line_fixtures`, used at
`r35_d1`/`r35_d2`, `plans/round36_c1_verify.py:267-290`); the callers do `d4.replace(...)` at `:189`
and `d5.replace(...)` at `:198` with no `None` guard. Consequence, measured:
- delete the SCORECARD D4 line → R34-D4 *plus two crashes* in `counter-accepts-junk` and
  `working-tree-and-token-cooccurrence` (ctlA, mismatches 3);
- delete the round-34 D5 erratum line → same 3 (ctlF2);
- reword `is present` → `appears present` → R34-D5 keeps passing (its condition is the substring
  `present`) while R35-D1 shifts its *genuine* L4 fixture (`plans/round36_c1_verify.py:195`) so
  `false_red=1`, and R35-D2 reports `line_fixtures_wrong=1/6` (ctlF3).

Classification if such a row fails at the tip: **not a recurrence and not a freeze-only pin of the
failing class** — it is a dependency artefact. A recurring-class reading of a ledger whose rows share
frozen inputs is an over-count: 3 mismatches, 2 of them false attribution, from one edit.

### 4.2 Working-tree coupling duplicates signal (ctlB)
`R35-D1` runs the gate with `--require-clean-tree`, whose P9 is `git ls-files --others
--exclude-standard` (`plans/pkg_gate.py:259-263`), and `R35-D2` runs the same whole-lane query
(`plans/round36_c1_verify.py:279-289`); one untracked file fails both, plus `R34-D1` for the
round-34 path subset. Three mismatches for one stray file.

### 4.3 The gate's clean-tree leg is untracked-only, so a tracked edit alone is not "dirty" (ctlC)
`c_clean_tree` (`plans/pkg_gate.py:259-263`) only lists untracked files; `ctlC` modified a tracked
file and `tip_package_rc=0`. This is the documented intent (the round-36 recipe labels P9 "untracked
leftover file", `plans/round36_c1_verify.py:137`), so ctlC is a **no-false-alarm** control: the runner
does not manufacture a mismatch where the gate legitimately accepts. It also fixes what "clean tree"
means in these rows: untracked only.

### 4.4 The ledger cannot be run in place mid-wave; run it on a clean clone
At 01:40 the lane worktree had `git status --porcelain` = 4 entries (all untracked directories/files
of this wave: `.ufo/waves/round-37/build.ready`, `build/`, `claims/measure-before-committed.txt`,
`integrate/`) and `git ls-files --others --exclude-standard | wc -l` = **78** files (the count grows
as peers write; it read 7 status entries a minute later, `modified_tracked=0` throughout). Feeding
that tree to `R35-D2`'s first conjunct (`not left`, `plans/round36_c1_verify.py:279`) or to the gate's
P9 would print `untracked_anywhere=78` / `tip_package_rc=1` and count two mismatches for classes
`working-tree…` and `counter-accepts-junk` that did not recur. Because the clone carries only
committed bytes (and `modified_tracked=0`, so the clone's tracked bytes equal the worktree's), the
tip run in §2 is the well-defined reading. That is also the operational lesson: at wave close, wave
outputs left untracked will make the ledger itself red — hygiene, not a defect recurrence.

### 4.5 Six of nine passes are closure-byte pins; only three rows still exercise behaviour
`pin`: R34-D2 (committed path count 0), R34-D3 (`listed=6` digests over a frozen capture), R34-D4
(one correction line), R34-D5 (erratum + round-35 mistake row), R35-D3 (`committed_nested_wave_paths=0`
at `refs/heads/master`), R35-D4 (`recount 13 + 23 + 1 = 37 vs stated denominator 38`, i.e. the erratum
line must exist and must disagree). A pin pass means *the closure evidence has not moved*; it is not
a re-demonstration that the class is fixed. `live`: R34-D1, R35-D1, R35-D2 — and R35-D1/R35-D2 are
themselves the round-36 battery, so the ledger's behavioural coverage of rounds 34-35 is essentially
the one 14-fixture battery plus two git queries.

### 4.6 Shape notes for the L1 (data, not judgement)
- Proposal 2(a) asked for **one** ledger; the tip has two files with two different checkers
  (5 + 4 rows, 8 distinct check functions) — no shared schema, and a new row must be routed to the
  module that owns its check by file, not by id.
- Every row is `closed`; there is **no open row at the tip**, so `mismatches=0` rests on the
  9 × (closed → pass) direction only. The other direction is exercised only synthetically (ctlG).
- Runtime of the whole ledger at the tip: 2.0-2.2 s, 15 gate subprocesses — cheap enough to run every
  wave from a clone; the cost is the clone, not the checks.

## 5. Operability

```
python3 .ufo/waves/round-37/build/R37LedgerTip/ledger_tip.py \
    --source <lane> --work <scratch>            # clone + clean-tree refusal (exit 0 iff mismatches==0)
python3 .ufo/waves/round-37/build/R37LedgerTip/ledger_tip.py \
    --lane <prepared clone> [--keep-notes]      # control mode, prints dirty=<n>
```
Refuses to reuse an existing `<work>/lane`; verifies the clone top-level; imports check bodies from
the tree it measures (never from the runner's own directory); `TMPDIR` governs the battery's mktemp
fixtures. `--keep-notes` prints each passing row's note. Tooling: nothing installed (pacman paused
host-wide; `python3`, `git` sufficed).

## 6. Risks / blockers

- The zero is a zero **of these nine checks at `44b7298`**, not of the defect classes: 6/9 rows are
  pins (§4.5) and the ledger's behavioural surface is one battery + two git queries.
- Any future edit to `SCORECARD.md:1178` or the round-34 D5 erratum line re-reds 2-3 rows, 2 of them
  by crash and in the wrong class (§4.1). Guarding those two lines is a prerequisite for treating the
  ledger's `mismatches` as class-attributed.
- Running the ledger in place is unusable mid-wave (§4.4); the clone is required, so an integrator
  must not "fix" a red by committing scratch or by editing a row.
- No blocker to the assignment; no lane writes; no ledger edits.

VERDICT: ledger-tip-rows-9-mismatches-0
