# C2ScribeRowsB — R52-C2 wave 1 (build), scribe: five missing registry rows

Seat: scribe. Axis named: **operability** (the lane's declared axis for R52-C2). Lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, base tip `30801b479e3418c11089b8586178b6960216f364`,
lane HEAD during the seat `1315234bdc8024499d943f0483dcb51fb5e4a618` (base tip + the round-52 freeze
commit; `git merge-base --is-ancestor 30801b47 HEAD` → true). No lane byte was edited by this seat.

## 1. What I did

Read the frozen claims file in full, then read each of the five scripts (`docstring`, `argparse`
block, every `return`/`sys.exit` site, every write site) and **measured** every leg I could run
without a lane write:

| instrument | read | ran |
|---|---|---|
| `plans/parser_policy_compare.py` | full `main`, `compute`, `render`, `selftest`, `PINS`/population import from `plans/grader_perturb.py` | `--summary`, `--selftest`, `--bogus` |
| `plans/password_recovery_probe.py` | `main`, `run_case`, `sandbox_argv`, `PINS`, `TAGS`, harness | `--dry`, `--stage-check`, full run, `--dry --stage-check` |
| `plans/polyglot_c_py_probe.py` | `main`, `run_case`, `sandbox_argv`, `PINS`, `TAGS`, harness | `--dry`, `--stage-check`, full run, `--dry --stage-check` |
| `plans/round28_census.py` | whole file (108 lines) | `--revision REV` at base tip and at the freeze tip, and with no `--revision` |
| `plans/round30_defects.py` | whole file (all five checks, `FROZEN`, `selftest`, `main`) | `--lane .`, `--selftest`, `--bogus` |

Sibling artefacts were **absent** when I started: `/fast/scratch/hyaku/kengaku-r52/C2ExecRowFacts/`
did not exist and `/fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/` held only an empty `tmp/`. I
therefore derived every fact myself, as the item permits. `C2ExecRowFacts` then appeared at
17:01–17:04 while this seat was mid-flight; after finishing my own derivation I cross-checked the
five instruments against its `selftest_static.json`, `runtime_selftest.json`, `writes_static.json`
and `runtime_default.json` and found **no disagreement** with any cell I wrote (§2b).
`C2ExecRowRuns/` was still empty of measurements when I read it, so nothing here rests on it.

Every row was validated against the **frozen counter's own parser** in a scratch clone of the lane
(`git clone --shared` into my scratch, `git checkout 1315234`), never against the lane.

## 2. Exact commands and measured numbers

All runs with `TMPDIR=/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsB/tmp` and cwd = lane root unless
stated. Exit codes are the script's own (`; echo $?` immediately after, no pipe).

```sh
# frozen counter, lane at freeze tip 1315234 (read-only; the script writes nothing)
python3 plans/round52_c2_registry.py --lane .
#   ADVERTISED total=72 / REGISTERED total=44 rows=46 / MISSING 28 / INCOMPLETE 0
#   ENTRY-MISSING 0 / SELFTEST-UNBACKED 1 (`order-check`) / PREDICATE R52-C2 fail ; exit 1
#   → reproduces the claims file's before-block exactly; all five of my instruments are in MISSING.

python3 plans/parser_policy_compare.py --root . --summary
#   exit 0 ; TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089
#             policies_with_flips=5 ; 73 lines
python3 plans/parser_policy_compare.py --selftest
#   exit 0 ; SELFTEST total policies=9 cases=59 mutants=10 killed=10 failures=0
#            (incl. SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1
#             pin_error=True policy_calls=0)
python3 plans/parser_policy_compare.py --bogus            # exit 2

python3 plans/password_recovery_probe.py --lane . --dry
#   exit 0 ; cases=16 predicted_pass=5 predicted_fail=11
python3 plans/password_recovery_probe.py --lane . --stage-check --work "$TMPDIR"
#   exit 0 ; stagecheck cases=16 failed=0
python3 plans/password_recovery_probe.py --lane . --work "$TMPDIR"
#   exit 0 ; regrade cases=16 differ=0 ; cases=16 observed_pass=5 observed_fail=11 mismatches=0
#   diff against corpus/evidence/round45/password-recovery-probe.txt → 0 differing lines (byte-equal)
python3 plans/password_recovery_probe.py --lane . --dry --stage-check   # exit 2 (mutually exclusive)

python3 plans/polyglot_c_py_probe.py --lane . --dry
#   exit 0 ; cases=18 predicted_pass=7 predicted_fail=11
python3 plans/polyglot_c_py_probe.py --lane . --stage-check --work "$TMPDIR"
#   exit 0 ; stagecheck cases=18 failed=0 (each line carries pycheck=ok ccheck=ok cwarn=<n>)
python3 plans/polyglot_c_py_probe.py --lane . --work "$TMPDIR"
#   exit 0 ; regrade cases=18 differ=7 ; cases=18 observed_pass=7 observed_fail=11 mismatches=0
#   diff against corpus/evidence/round46/polyglot-c-py-probe.txt → 0 differing lines (byte-equal)
python3 plans/polyglot_c_py_probe.py --lane . --dry --stage-check        # exit 2

python3 plans/round28_census.py --root . --revision 30801b479e3418c11089b8586178b6960216f364
#   lane at freeze tip → exit 1
#   clean-clone of 30801b47 (my scratch) → exit 1, same shape:
#     c1(exit 0) distinct_task_ids=812 selected_count=16
#     c2(exit 0) source_rows_checked=13 findings=0
#     state(exit 1) mismatch=1 → P3c.box.4.pointer.1
#     sources rows=171 malformed=0 ; knowledge files=55 index_rows=54
#     unindexed=['knowledge/fixture-honest-geometry.md'] dangling=[] duplicate_rows=[]
python3 plans/round28_census.py --root .                 # exit 2, usage: --revision required

python3 plans/round30_defects.py --lane .
#   exit 0 ; ok D1…ok D5 ; checks=5 defects=0
python3 plans/round30_defects.py --selftest
#   exit 0 ; CASE registry-complete PASS + CASE D1..D5-red-on-empty PASS ; SELFTEST checks=5 failed=0
python3 plans/round30_defects.py --bogus                 # exit 2
```

Validation of the rows themselves (scratch clone `head1315234`, my rows appended after the
`gate-flip-check` row):

```sh
python3 plans/round52_c2_registry.py --lane .     # clone with my 5 rows only
#   REGISTERED 44→49, rows 46→51, MISSING 28→23, INCOMPLETE 0, ENTRY-MISSING 0,
#   SELFTEST-UNBACKED 1 (`order-check` unchanged), exit 1
# per-row parse check (importing the counter's own functions):
#   each of the 5 rows → cells=8, all-nonempty=True, unbacked=False, entry_script=<its script>
```

## 2b. Cross-check against the sibling `C2ExecRowFacts` measurements

Read after my own derivation was complete (the seat's facts appeared at 17:01–17:04; files under
`/fast/scratch/hyaku/kengaku-r52/C2ExecRowFacts/`). Every entry below agrees with the cell I wrote:

| instrument | sibling measurement | my row's claim |
|---|---|---|
| `plans/parser_policy_compare.py` | `selftest_static.json`: two `_selftest_*` functions; `runtime_selftest.json`: `exit_code 0`, stdout starts `SELFTEST pass policy=E0 probes=5 failed=[]`; `writes_static.json`: writes only inside `_selftest_pin_rejection` | has `--selftest`, exit 0, writes one selftest temp tree |
| `plans/password_recovery_probe.py` | `selftest_static.json`: `functions: []`, `main_dispatch: []`; no `runtime_selftest` entry; writes only in `run_case` (`mkdir`/`write_text`/`copyfile` under the scratch root) | no self-test; scratch-only writes |
| `plans/polyglot_c_py_probe.py` | `functions: []`, `main_dispatch: []`; no `runtime_selftest` entry; writes only in `run_case` | no self-test; scratch-only writes |
| `plans/round28_census.py` | `functions: []`, `main_dispatch: []`; no `runtime_selftest` entry; `writes_static.json`: `[]` | no self-test; writes nothing |
| `plans/round30_defects.py` | `runtime_selftest.json`: `exit_code 0`, stdout `SELFTEST checks=5 failed=0`, `writes_in_lane: []`; `writes_static.json`: `[]` | has `--selftest`, exit 0, writes nothing |

## 3. Files produced (absolute paths)
- `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsB/rows.md` — **the deliverable**: five markdown table
  rows with the eight registry columns, plus the paste target note. That scratch path was removed at
  seat end (scratch discipline); the kept copy is
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsB/rows.md`.
- Kept copies in this report directory: `rows.md`, `counter-before.txt`, `counter-with-rows.txt`,
  `counter-pipe-fixed.txt`, `counter-orderfix.txt`, `counter-final.txt`, `ppc-summary.txt`,
  `ppc-selftest.txt`, `prp-dry.txt`, `prp-stage.txt`, `prp-full.txt`, `prp-diff.txt`, `pgp-dry.txt`,
  `pgp-stage.txt`, `pgp-full.txt`, `pgp-diff.txt`, `r30-run.txt`, `r30-selftest.txt`,
  `census-base.json`, `census-noarg.txt`.

## 4. Row kinds (as delivered)

| row name | instrument | kind |
|---|---|---|
| `extraction-policy-compare` | `plans/parser_policy_compare.py` | probe |
| `password-recovery-probe` | `plans/password_recovery_probe.py` | probe |
| `polyglot-c-py-probe` | `plans/polyglot_c_py_probe.py` | probe |
| `round28-census` | `plans/round28_census.py` | gate |
| `round30-defects` | `plans/round30_defects.py` | gate |

`probe` for the three measurement instruments follows the existing registry's own precedent
(`grader-perturb`: exit encodes pin/baseline integrity, findings are on the output lines). `gate` for
the two that decide a clean/unclean predicate.

## 5. Rows I could not fill truthfully

**None.** Two of the five have a real `--selftest` (`extraction-policy-compare`,
`round30-defects`; both measured green) and three have **no self-test at all**
(`round28-census`, `password-recovery-probe`, `polyglot-c-py-probe`); those three cells say so
plainly and name the control that exists instead, which is the spelling the frozen counter accepts
(`selftest_unbacked` returns False when a cell names no single script, or names no flag).

## 6. Findings — two counter defects that would have blocked R52-C2 as frozen

These are measured in the scratch clone at `1315234`; both are in the **frozen** counter, so the L1
cannot patch them without breaking the freeze — they must be routed, not fixed in place.

### F1 — `parse_rows` silently drops any row whose cells contain an escaped pipe; `gate-flip-check` is one of the "28 missing" *because of this*

`plans/round52_c2_registry.py:56-67` splits a table line on every `|` and keeps only lines that yield
exactly 8 cells. The `gate-flip-check` row at `SKILL.md:609` carries `fired\|not fired` in its verdict
map, so it splits into **9** cells and is dropped — the row exists and is well-formed markdown, but
the counter never sees it.

Evidence (measured, in the clone):

```
physical table lines: 48   parsed rows: 46   dropped (cells != 8): 1
  DROP | `gate-flip-check` | gate | `python3 plans/gate_flip_check.py --lesson <path>` …
escaped-pipe occurrences in that row: 1   cells split: 9
```

Consequence: after adding my five rows the counter still reported `MISSING plans/gate_flip_check.py`
(28→23 instead of 28→28−5=23 … and it stayed in the list). Rewriting that one cell as
`fired or not fired` (meaning unchanged, no `|`) makes the row parse and the counter prints
**`MISSING 22`** and drops `plans/gate_flip_check.py` from the list:

```
# clone: my 5 rows + this one-character-class fix
REGISTERED total=50 rows=52 / MISSING 22 / INCOMPLETE 0 / ENTRY-MISSING 0
SELFTEST-UNBACKED 1 (`order-check`) / PREDICATE R52-C2 fail ; exit 1
```

So **one of the 28 "missing" instruments already has a truthful row**; it is invisible to the parser.
Any integration that adds 28 new rows without touching this cell will end at `MISSING 1`, and the
kill rule would then fail C2 for a parser artefact rather than a registry gap.

### F2 — the SELFTEST-UNBACKED leg misfires on a truthful negation (`order-check`)

`selftest_unbacked` (`:75-86`) counts a cell as unbacked when it names exactly one script path and
every `--flag` in it is absent from that script's body. The `order-check` cell says the opposite of
an unbacked claim — "no `--selftest` in the script" — but it names exactly one *other* script
(`plans/round40_c1_verify.py`) and the flags `--selftest`, `--receipt`, `--claims`, and none of the
three appears in that file (measured: all three `ABSENT`; `plans/order_check.py` also has no
`--selftest`). The leg therefore reports the truthful row as a false positive, and the claims file's
`SELFTEST-UNBACKED 1` is not the defect it reads as.

Evidence (measured): naming both scripts in the cell —
`no \`--selftest\` in \`plans/order_check.py\`; falsifiers are external — \`plans/round40_c1_verify.py\``
— makes `len(scripts)==2`, the leg skips the cell, and the counter prints **`SELFTEST-UNBACKED 0`**
with my five rows in place (`MISSING 22`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, exit 1 on MISSING only).
The counter's own `--selftest` is green in the clone: `SELFTEST cases=3 failures=0`, exit 0.

### F3 — `round28-census` is **red at the base tip**, and its row says so

`plans/round28_census.py --root . --revision 30801b47…` exits **1** at `30801b47` (and at the freeze
tip), on two legs: `plans/state_check.py --json` exits 1 with exactly one `MISMATCH`
(`P3c.box.4.pointer.1`, `PROVINCE.md:129` anchor `### Adjacent` with 0 hits), and one knowledge file
is unindexed (`knowledge/fixture-honest-geometry.md`; files=55 vs index_rows=54). The claims file
requires this census to exit 0 at round end (frontier step 1), so the L1 needs this number now: it is
a **pre-existing red**, not caused by this wave. My row records it inside the verdict-map cell rather
than advertising the instrument as green.

### F4 — minor accounting facts about the frozen counter (no action implied)

- `REGISTERED … rows=46` in the claims' before-block counts the **table header** as a row
  (`parse_rows` only skips the `---` separator): 48 physical lines = header + separator + 46 data
  rows; parsed 46 = header + 45 data rows, of which one is the dropped `gate-flip-check` row.
- `coverage-census`'s entry (`python3 corpus/evidence/round13-coverage/coverage_census.py`) can never
  be extracted by either regex — `[A-Za-z0-9_]+` excludes the hyphen in `round13-coverage`. It is
  therefore neither `REGISTERED` nor `ADVERTISED`; harmless today, but any future hyphenated path is
  invisible to both legs of this counter.

## 7. Attacks attempted (scribe seat — self-attack on my own deliverable)

I did not take an attack seat; the checks below are what I ran against **my own rows** so the L1 is
not the first reader to find them wrong:

| attack | how | result |
|---|---|---|
| a row that does not parse | import `parse_rows` and count cells | 5/5 rows → 8 cells, all non-empty |
| a row that registers the wrong script | `entry_script(cell[2])` per row | 5/5 → its own `plans/*.py` |
| a false self-test claim | `selftest_unbacked(cell[4])` per row | 5/5 → False; the two claimed `--selftest` runs measured green, the three "no self-test" cells name no script+flag pair |
| a verdict map copied from the docstring | re-derived from code: every `return`/`sys.exit` in each script, then confirmed by running each reachable leg | `0`/`1`/`2` in each row matches a measured run above; the two probes' "mismatches never in the exit code" is code (`return 0` after the summary print) **and** receipt-backed |
| a stale pin | recomputed the probes against their captures by running them | both captures at their pinned digests (else the run would have printed `SETUP …` and exited 2); fresh receipts byte-equal |

What I did **not** do: I did not re-verify the round-45/46 capture digests by hand against
`SHA256SUMS` (the probes check them before any case, and both runs passed that gate); I did not run
the two probes under their round-45/46 `envelope.sh` wrapper, so my re-runs are plain `bwrap` runs
(byte-equal output, so the envelope is not needed for reproducibility of the receipt); I did not run
`plans/round28_census.py` under a `--revision` other than the base tip.

## 8. Tooling

No tool was installed or upgraded: nothing was needed (Python 3 stdlib, `git`, `/usr/bin/bwrap`,
`/usr/bin/gcc`, `/usr/bin/zip`, `/usr/bin/dd`, `/usr/bin/strings` were all already present and
executable). No pacman transaction was attempted. No campaign tool was run inside
`/home/vgpnk/Projects/shokuknow`.

## 9. Scratch discipline

Scratch root `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsB/` (two `git clone --shared` fixtures
`base30801` and `head1315234`, plus `tmp/` and `out/`). Receipts I wanted kept were copied into this
report directory and the scratch root was then removed with
`rm -rf -- /fast/scratch/hyaku/kengaku-r52/C2ScribeRowsB/`; a `ls` of the parent after the delete is
recorded in the transcript. No `ENOSPC` was seen.
