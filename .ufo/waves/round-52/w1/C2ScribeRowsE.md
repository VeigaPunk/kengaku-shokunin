# C2ScribeRowsE — round 52 wave 1 (scribe): five Gate/probe registry rows

Seat: `C2ScribeRowsE` (scribe, leaf member — no subagent dispatch). Lane `kengaku-shokunin`, base tip
`30801b479e3418c11089b8586178b6960216f364`; the lane HEAD measured during this seat is
`1315234bdc8024499d943f0483dcb51fb5e4a618` (the round-52 claims/counter freeze commit on top of it).
Frozen rules read first and in full: `plans/round-52-claims.md` (predicate, thresholds, populations,
controls, kill rules for R52-C1 and R52-C2).

## 1. What I did

Drafted the five missing rows R52-C2 needs for these instruments:

| instrument | row name | kind |
|---|---|---|
| `plans/round46_c2_verify.py` | `round46-c2` | gate |
| `plans/round46_c3_verify.py` | `round46-c3` | gate |
| `plans/round50_c1_verify.py` | `round50-c1` | gate |
| `plans/round50_c2_audit.py` | `round50-c2` | gate |
| `plans/round51_routing.py` | `round51-routing` | gate |

All five are `gate`: each prints a frozen predicate line and returns 0 only when every leg holds
(`PREDICATE C2 pass`, `PREDICATE C3 pass`, `PREDICATE R50-C1 pass`, `POINTERS … unresolved=0`,
`PREDICATE R51-C2 pass`). None is a `probe` in the registry sense (a probe reports even when it
finds failures — `grader-perturb`, `regex-log-probe`): `round50-c1` and `round46-c2/c3` fail the
run on a bad leg, and `round51-routing` fails on any `DETAIL` line.

Method: read each script myself (docstring, argparse block, every `return`/`sys.exit` site, the
pinned constants, the write calls), then measure what could be measured without mutating the lane.
Where the sibling seats' artefacts existed I used them and say so; where they did not, the facts
are derived from source and labelled as such.

**Sibling artefacts used (not `facts.json`).** `C2ExecRowFacts/facts.json` never existed during
this seat; `C2ExecRowFacts/facts_ast.json`, `runtime_default.json`, `runtime_selftest.json` and
`selftest_static.json` did, and `C2ExecRowRuns/` held only a lane clone with no receipt. I used:
`facts_ast.json` (argparse flags, `has_selftest_flag`, declared exit codes, write sites) for all
five; `runtime_default.json` for the `round46_c3_verify.py` verdict map (I did not run that
instrument — see §5.5) and as an independent second reading of `round46_c2_verify.py`,
`round50_c1_verify.py`, `round50_c2_audit.py`, `round51_routing.py`; `runtime_selftest.json` as a
second reading of the two real self-tests.

## 2. Exact commands run

All with `TMPDIR=/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsE/tmp`, cwd the lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` unless stated. Nothing was written inside the lane
by any of these (the lane's own `git status` dirt is other seats' wave files, not mine).

```
python3 plans/round52_c2_registry.py --lane .                       # frozen counter, before
python3 plans/<each of the five>.py --help                          # argparse surface
python3 plans/round46_c2_verify.py --selftest                       # -> exit 2, "unrecognized arguments"
python3 plans/round46_c3_verify.py --selftest                       # -> exit 2, "unrecognized arguments"
python3 plans/round50_c1_verify.py --selftest                       # -> exit 2, "unrecognized arguments"
python3 plans/round46_c2_verify.py --lane .                         # -> exit 0, PREDICATE C2 pass
python3 plans/round50_c2_audit.py --lane .                          # -> exit 0, unresolved=0
python3 plans/round50_c2_audit.py --lane . --selftest               # -> exit 0, verdict=ok
python3 plans/round51_routing.py --lane .                           # -> exit 0, PREDICATE R51-C2 pass
python3 plans/round51_routing.py --lane . --selftest                # -> exit 0, cases=11 failures=0
python3 plans/round50_c1_verify.py --lane . --work $TMPDIR/r50c1work   # (1st attempt: parent absent -> FileNotFoundError)
mkdir -p $TMPDIR/r50c1work && python3 plans/round50_c1_verify.py --lane . --work $TMPDIR/r50c1work
python3 verify_rows.py <scratch>/mirror <scratch>/rows.md           # scratch harness, see §4
```

`plans/round46_c3_verify.py` was **not** run by this seat: its own docstring says V2 (which runs
`pkg_gate.py … --rerun`) "is never run by a wave-1 seat", and the order rule the counter cites
(`plans/round-46-claims.md` §C3, QUALITY Q30) holds that "before stage 2 the probe runs only
`--dry`/stage-check". Its measured lines come from `C2ExecRowFacts/runtime_default.json` and are
attributed as that seat's measurement, not mine.

No tool was installed or upgraded by this seat (nothing was needed; pacman is paused host-wide and
`uv`/`npx`/`~/.local/bin` were not used).

## 3. Measured numbers (this seat, verbatim)

Frozen counter before my rows (re-measured, matches the claims' before-block):

```
ADVERTISED total=72
REGISTERED total=44 rows=46
MISSING 28
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 1     (`order-check`)
PREDICATE R52-C2 fail
```

`round46_c2_verify.py --lane .` → exit 0:

```
PINS total=3 mismatched=0
A anchorline live=0 repaired=8 base_rows=149 base_missing=0 base_changed=0 ok
B predictor states=16 grader_pass=10 grader_fail=6 disagree=0 ok
C entry source_ranges=9 source_ranges_bad=0 errata_marks=5/5 ok
D selftest exit=0 ok
checks=4 defects=0
PREDICATE C2 pass
```

`round50_c2_audit.py --lane .` → exit 0:
`TIP 1315234bdc8024499d943f0483dcb51fb5e4a618 branch=master`,
`POINTERS total=292 paths=228 hashes=64 resolved=292 exists=216 superseded=3 never-landed=9 unresolved=0`.

`round50_c2_audit.py --selftest` → exit 0:
`SELFTEST pristine_rc=0 bogus_rc=1 new_unresolved=['plans/round50_selftest_bogus.py'] verdict=ok`.

`round51_routing.py --lane .` → exit 0: `LEDGER corpus/routed-findings.jsonl rows=75`, FIELDS 75/0,
OWNERS 75/0, DISPOSITIONS 75/0, SOURCES 75/0, CHECKS 75/0, `VERIFIED ran=0 passed=0 failed=0`,
CLOSE_REFS 0/0, `NEXT violations=0`, `PREDICATE R51-C2 pass`.

`round51_routing.py --selftest` → exit 0: `[selftest] cases=11 failures=0`, `[selftest] ALL PASS`.

`round50_c1_verify.py --lane . --work <existing dir>` → exit 1, 54 s:

```
REV 1315234bdc8024499d943f0483dcb51fb5e4a618
TREE dirty=4
FENCE …/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=20 clean=20 leaked=0 build_errors=0
MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 fail
```

Every substantive leg green; the predicate failed on `TREE dirty=4` alone (the four untracked
wave-1 files present at that moment). The same instrument on the `C2ExecRowFacts` clone measured
`TREE dirty=2` and the identical leg values.

`round46_c3_verify.py` (C2ExecRowFacts clone, default mode, exit 1 in 3.87 s) — 13 legs, of which
`V2 DEFECT spec=frozen gate=frozen gate_exit=1`, `V7 DEFECT rows=5 tags=7 …`,
`V8 DEFECT order_exit=1 result=not-PASS`; `V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0`;
`V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12`; `checks=13 defects=3`,
`PREDICATE C3 fail`. The gate's own P8/P9 defected on the clone (`index_rows=54 knowledge_files=55`;
`untracked=2 first=.ufo/waves/round-52/w1.ready`), which is what makes V2's
`--require-clean-tree` fail there.

## 4. How the rows were validated

`verify_rows.py` (kept as a receipt) mirrors the lane into
`/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsE/mirror/lane` by symlinking every top-level entry
except `SKILL.md`, writes a copy of `SKILL.md` with my five rows inserted after the `gate-flip-check`
row, and calls the **frozen** `plans/round52_c2_registry.py`'s own `collect()` on that mirror. It
never touches the lane tree. Result:

```
ROWS-INSERTED 5
ADVERTISED 72 REGISTERED 49 ROWS 51
MISSING 23 INCOMPLETE 0 ENTRY-MISSING 0 SELFTEST-UNBACKED 1
ROW `round46-c2`      cells=8 entry=plans/round46_c2_verify.py registered=True empty=[] unbacked=False
ROW `round46-c3`      cells=8 entry=plans/round46_c3_verify.py registered=True empty=[] unbacked=False
ROW `round50-c1`      cells=8 entry=plans/round50_c1_verify.py registered=True empty=[] unbacked=False
ROW `round50-c2`      cells=8 entry=plans/round50_c2_audit.py registered=True empty=[] unbacked=False
ROW `round51-routing` cells=8 entry=plans/round51_routing.py registered=True empty=[] unbacked=False
SELFTEST-UNBACKED-LIST ['`order-check`']
```

So each row removes exactly one `MISSING`, adds no `INCOMPLETE` and no `SELFTEST-UNBACKED`; the
remaining 23 and the pre-existing `order-check` row belong to other seats. The counter keys rows on
the `python3 plans/<file>.py` in the entry cell, so the *names* are the L1's to rename — as long as
each entry cell keeps that command the row stays registered.

Self-test cells and the frozen rule: `SELFTEST-UNBACKED` fires only when a cell names exactly one
script **and** one flag the script's bytes lack. `round50-c2` and `round51-routing` name
`plans/round50_c2_audit.py --selftest` and `plans/round51_routing.py --selftest` — both flags exist
and both were executed green here. `round46-c2`, `round46-c3` and `round50-c1` have no `--selftest`
flag at all (each rejected it with exit 2, measured), so their cells say so plainly, as the frozen
rule accepts, and name the red fixture that actually exercises them (leg D, the `plans/filler46/`
control package, the 15-mutant battery). `round46-c2`'s cell names `plans/anchor_line_check.py`,
which really does accept `--selftest` (`plans/anchor_line_check.py:201`), so the cell is backed.

## 5. Findings (things the L1 should know before integrating)

1. **`round46_c2_verify.py` and `round46_c3_verify.py` document an exit code they never return.**
   Both docstrings say "Exit 0 pass, 1 fail, 2 setup error". Every return site is `0`/`1`
   (`round46_c2_verify.py:205,225`; `round46_c3_verify.py:879,904,909`), and the setup paths print
   `SETUP a pinned tool is not at its freeze digest` (stderr) or `PACKAGE unreadable: …` and then
   return 1. My rows state the measured map and name the docstring's `2` as unimplemented rather
   than repeating the docstring — a row that repeated it would be false of the script.
2. **`round50_c1_verify.py`'s docstring says `MUTANTS total=23`; the artefact carries 15.**
   `plans/mutants50/c1-mutants.json` has 15 rows (`c50-01-gitfile-refused` … `c50-21-ref-value-any`),
   and the leg enforces only `total>=12` and `caught>=12`, so the predicate still holds
   (measured `caught=15 broken=0 floor=12 verdict=met`). The row records 15 and names the
   discrepancy; the docstring's frozen sentence and the committed mutant set disagree and only the
   L1 can say which is canonical (a change to either is new round text, not a patch).
3. **`round50_c1_verify.py --work DIR` requires the parent to exist.** Measured: an absent parent
   raises `FileNotFoundError` from `tempfile.mkdtemp` (traceback, exit 1) instead of a `SETUP` line
   and exit 2. The row's entry cell says the directory must already exist.
4. **`round50_c1_verify.py` is not measurable on a dirty tree.** It failed with every substantive
   leg green because four untracked wave files made `TREE dirty=4`. Any acceptance run of this
   instrument — and of `round46_c3_verify.py`, whose V2 passes `--require-clean-tree` — has to be
   on a clean clone, so the L1 cannot score either on the working lane during a wave.
5. **`round46_c3_verify.py` V2 executed in a wave-1 seat's clone.** `C2ExecRowFacts` ran the
   default mode, which includes V2 (`pkg_gate.py package --rerun --require-clean-tree`, i.e. it
   executed the graded `polyglot-c-py` probe). The counter's own docstring says V2 "is never run by
   a wave-1 seat", and the order rule it cites (`plans/round-46-claims.md` §C3, QUALITY Q30) holds
   that before stage 2 the probe runs only `--dry`/stage-check. I did not run it; I cite that
   seat's measurement as theirs. This is an order-rule observation for the L1, not a defect in the
   instrument.
6. **`round46_c3_verify.py` V6 shells to a host-absolute path**,
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`round46_c3_verify.py:127`), inside a
   lane instrument. The row's entry cell names it, so a stranger is not surprised by a lane
   instrument depending on a fleet script outside the lane.
7. **`round51_routing.py --run-checks` executes ledger-supplied commands.** Each
   `disposition=fixed-verified` row's `check` runs through `bash -lc` with cwd = lane, `TMPDIR` =
   scratch and a 90 s timeout. The row's write-scope cell states this, because the honest answer to
   "what does this write" is "whatever the ledger says".
8. **`round50_c1_verify.py` prints `SEALED` twice** (12 modules from `plans/sealed46/`, 20 from
   `plans/sealed50/`, both labelled `SEALED`). A reader who expects one `SEALED` line will think a
   line is missing; the row's verdict map names both.

## 6. Rows I could not fill truthfully

None. All five rows are complete (8 non-empty cells), each claim was read off the script or
measured, and every self-test cell is either an executed spelling or an explicit "no self-test, and
here is why". Two cells deliberately **differ from the script's own docstring** — the exit-code map
of `round46-c2`/`round46-c3` (§5.1) and the mutant count of `round50-c1` (§5.2) — because the
docstring is wrong there and the row must be true of the code.

## 7. Files produced (absolute paths)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsE.md` — this report.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsE/rows.md` — the five rows, ready to paste after the `gate-flip-check` row of `SKILL.md` §Gate/probe registry (also at `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsE/rows.md` until the scratch dir is removed).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsE/verify_rows.py` — the mirror-and-recount harness (§4).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsE/r50c1-measured.txt` — raw `round50_c1_verify.py` output quoted in §3.

Nothing was written to the lane tree, `.ufo/state/`, `.ufo/watchdog.log`, `templates/`, `scripts/`,
`MANIFEST.json`, `~/.local/bin`, any other PATH directory, or `/home/vgpnk/Projects/shokuknow`. No
`git`/`jj` mutation was run anywhere. Scratch dir `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsE/`
was removed before yielding (`rm -rf --`), after the three receipts above were copied out; free
space on `/fast` at start was 540 GB of 804 GB.
