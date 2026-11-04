# RegistryAuditR72 — the four new registry rows against the Gate standard

Seat `RegistryAuditR72`, round 72 wave w1. Read-only over the lane: no file was edited except this
report; `SKILL.md`, the predicates, case tables, vectors, digests and kill rules are untouched.
No tool installed, no host mutation, no subagent dispatch. Scratch
(`/fast/scratch/hyaku/kengaku-r72/RegistryAuditR72{,b,base,c}`) was removed before yielding;
`git status --porcelain plans corpus SKILL.md LOG.md SCORECARD.md` shows no change attributable to
this seat (only sibling rounds' untracked evidence).

## 1. Surfaces read

| surface | pointer |
|---|---|
| registry block | `SKILL.md:587` `## Gate/probe registry`, rows at `:695` `round71-c1-hf-probe`, `:696` `round71-c2-routed-defects`, `:697` `round72-c1-hf-probe`, `:698` `round72-c2-routed-defects`; block ends at the next `## ` (`:797` `## Production checklist — running an eval`) |
| Gate standard | `PROTOCOL.md:375` §Gate standard (kind definition, verdict map, self-test, registry fields, scope) |
| scripts | `plans/round71_c1_hf_probe.py`, `plans/round71_c2_routed_defects.py`, `plans/round72_c1_hf_probe.py`, `plans/round72_c2_routed_defects.py` |
| pre-existing registry gate | `plans/round52_c2_registry.py` (`SKILL.md:663` row `round52-c2`) |
| sibling receipt, agrees | `corpus/evidence/round72/registry-debt.txt` (same `round52-c2` red, run at tip `b6336136`) |

Tip at audit: `b6336136e0e891522b113a94d8e0bd65e0eae8de`; freeze base: `c6322972`.

## 2. Commands run (exact, with exit codes)

| # | command | rc | observed |
|---|---|---|---|
| 1 | `python3 plans/<each of the four>.py --help` | 0 | flag lists quoted in §3 |
| 2 | `python3 plans/round71_c1_hf_probe.py --selftest` | **1** | `--selftest requires --work` |
| 3 | `python3 plans/round72_c1_hf_probe.py --selftest` | **1** | `--selftest requires --work` |
| 4 | `python3 plans/round71_c1_hf_probe.py --control` | **1** | `--control requires --work and --receipt` |
| 5 | `python3 plans/round72_c1_hf_probe.py --control` | **1** | `--control requires --work and --receipt` |
| 6 | `python3 plans/round71_c2_routed_defects.py --selftest` | **1** | `--selftest requires --work` |
| 7 | `python3 plans/round71_c2_routed_defects.py --mutants` | **1** | `--mutants requires --work` |
| 8 | `python3 plans/round72_c2_routed_defects.py --selftest` | **1** | `--selftest requires --work` |
| 9 | `python3 plans/round72_c2_routed_defects.py --mutants` | **1** | `--mutants requires --work` |
| 10 | `python3 plans/round72_c2_routed_defects.py --bogus` | **2** | argparse `unrecognized arguments` |
| 11 | `python3 plans/round71_c1_hf_probe.py --bogus` | **2** | argparse `unrecognized arguments` |
| 12 | `python3 plans/round72_c1_hf_probe.py` (no args) | **2** | help printed |
| 13 | `python3 plans/round72_c2_routed_defects.py --lane .` | **0** | `E1a ok` `E1b ok` `E1c ok` `E2 ok` `DEFECTS n=0` `PREDICATE R72-C2 pass` |
| 14 | `python3 plans/round71_c2_routed_defects.py --lane .` | **0** | `E1a ok` `E1b ok` `E1c ok` `E2a ok` `DEFECTS n=0` `PREDICATE R71-C2 pass` |
| 15 | `python3 plans/round71_c2_routed_defects.py --selftest --work <scratch>/s71` | 0 | `SELFTEST defects-in-fake=4 want=4 all-fail=True append-only-arm=True ok=True` |
| 16 | `python3 plans/round71_c2_routed_defects.py --mutants --work <scratch>/m71` | 0 | `MUTANTS total=4 killed=4 survived=0` |
| 17 | `python3 plans/round72_c2_routed_defects.py --selftest --work <scratch>/s72` | 0 | `SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True positional-arm=True parser-arm=True ok=True` |
| 18 | `python3 plans/round72_c2_routed_defects.py --mutants --work <scratch>/m72` | 0 | `MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1`, `ARM accept-green=ok refuse-red=ok attribution=ok` |
| 19 | `python3 plans/round71_c1_hf_probe.py --lane . --check-receipt corpus/evidence/round71/hf/receipt.txt` | 0 | `DEFECTS n=0` `PREDICATE R71-C1 pass` |
| 20 | `python3 plans/round72_c1_hf_probe.py --lane . --check-receipt corpus/evidence/round72/hf/receipt.txt` | 0 | `DEFECTS n=0` `PREDICATE R72-C1 pass` (wall 2.41 s for both) |
| 21 | digest re-derivation (script's own `tree_digest`/sha256, §5) | 0 | all four pins reproduce |
| 22 | `prepare_work` with `GRADER_SHA256` zeroed (r72c1 module, scratch `--work`) | **1** | `grader sha mismatch: 61a686d6…f87857`, `SystemExit` string ⇒ rc 1 |
| 23 | `python3 plans/round52_c2_registry.py --lane .` | **1** | `ADVERTISED total=110`, `REGISTERED total=105 rows=107`, `MISSING 5`, `PREDICATE R52-C2 fail` |
| 24 | same gate, `--lane` = base tree extracted with `git archive c6322972` (partial: SKILL/SCORECARD/LOG/corpus README+knowledge/plans) | **1** | `MISSING 7` incl. both round-71 scripts; `ENTRY-MISSING grader.py` is an artifact of the partial archive and is excluded from every claim below |
| 25 | registry-row parse with the r72c2 parser (`registry_rows`) | 0 | four rows × 8 cells; kinds `probe, gate, probe, gate`; owner `kengaku`; entry names the script |
| 26 | `python3 plans/round7{1,2}_c1_hf_probe.py --lane .` (the rows' literal entry command) | **2** | usage printed, battery never reached |

The r72c1/r71c1 **battery, `--control` and `--selftest` runs were not executed** (they stage live
bwrap batteries on shared port 5000 and would duplicate the C1 seat); their printed formats are
read from source and are marked "read, not run" in §6.

## 3. Flag-set comparison — row text vs `--help` / argparse

All four rows match the script **exactly**; no row names a flag the script lacks and no script has
a flag the row omits.

| instrument | row-declared set (entry cell) | argparse (`--help`) | verdict |
|---|---|---|---|
| `round71-c1-hf-probe` | `--lane --work --receipt --evidence-dir --check-receipt --selftest --control --render-table --stage-sha --port-lock` (10) | same 10 (`round71_c1_hf_probe.py:833-842`) | **match** |
| `round71-c2-routed-defects` | `--lane --work --selftest --mutants --json` (5) | same 5 (`:352-356`) | **match** |
| `round72-c1-hf-probe` | the 10 above **+ `--stub-control`** (11) | same 11 (`:1031-1041`) | **match** |
| `round72-c2-routed-defects` | `--lane --work --selftest --mutants --json` (5) | same 5 (`:465-469`) | **match** |

Entry command cells also name the correct script path and lane root in all four
(`python3 plans/<name>.py --lane .`); `round52-c2`'s `entry_script()` binds all four (in-adv and
in-reg both true). One operability gap: for the two c1 rows the bare `--lane .` invocation is
**help + exit 2** (no mode flag reaches the battery), while for the two c2 rows `--lane .` *is* the
gate invocation. See F9.

## 4. Eight-cell matrix (32 cells; 21 clean, 11 defective)

Cells: name · kind · entry · verdict map · self-test · pinned values · write scope · owner.
`ok` = matches the script and the Gate standard; `DEF` = defect, numbered in §7.

| instrument | name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|---|
| `round71-c1-hf-probe` | ok | **DEF F3** | **DEF F9** | **DEF F1/F2/F6** | **DEF F5** | ok | **DEF F4** | ok |
| `round71-c2-routed-defects` | ok | ok | ok | **DEF F1** | ok (ran) | ok | ok | ok |
| `round72-c1-hf-probe` | ok | **DEF F3** | **DEF F9** | **DEF F1/F2/F6** | ok (read, not run) | ok | **DEF F4** | ok |
| `round72-c2-routed-defects` | ok | ok | ok | **DEF F1** | ok (ran) | ok | ok | ok |

Per-row one-line verdict:

- **`round71-c1-hf-probe` — DEFECT.** Pins and owner correct; entry, verdict map, kind, self-test
  and write scope do not describe the script.
- **`round71-c2-routed-defects` — DEFECT (narrow).** Conformant except the declared `2` usage code;
  its `0` output was reproduced live and its self-test/mutant tallies reproduce exactly.
- **`round72-c1-hf-probe` — DEFECT.** Pins, self-test/owner correct; entry, verdict map, kind and
  write scope are wrong.
- **`round72-c2-routed-defects` — DEFECT (narrow).** Conformant except the `2` usage code (and a
  "fixture mode" that has no CLI surface).

## 5. Pinned values — re-derived, not trusted

| instrument | pin as written | re-derived | verdict |
|---|---|---|---|
| r71c1, r72c1 | grader `61a686d6…87857` | `sha256(corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py)` = `61a686d6caf8…f87857` | ok |
| r71c1, r72c1 | instruction `29151c5b…d1cc1` | `sha256(corpus/evidence/round71/hf/instruction.md)` = `29151c5b23…d51dcc1` | ok |
| r71c1, r72c1 | model tree `c5c25767…8944` | script's own `tree_digest()` over `corpus/evidence/round71/hf/model` = `c5c25767…b858944`, `MODEL_FILES=5`, five files on disk | ok |
| r71c1 | probe blob `d5ce2fa5…a82e` | `sha256(git show HEAD:plans/round71_c1_hf_probe.py)` = `d5ce2fa5871b…c1aa82e` | ok (current at tip) |
| r71c1 | eight cases K1–K8 | `len(CASES) == 8` | ok |
| r72c1 | nine cases K1–K9 | `len(CASES) == 9` | ok |
| r72c1 | nine-variable `ENV_ALLOW` | tuple length 9 (PATH, HOME, LANG, PYTHONPATH, PYTHONNOUSERSITE, PYTHONWARNINGS, TMPDIR, HF_HUB_OFFLINE, TRANSFORMERS_OFFLINE) | ok |
| r72c1 | canary `R72_CANARY` | `CANARY_NAME = "R72_CANARY"` (`:113`) | ok |
| r71c2 | round-70 lesson 8 rows, `LOG.md` R70-D1, two `corpus/README.md` mentions, nginx `E-D2`/`E-D2a` | script reads `corpus/lessons/round-70.md` (`LESSON_REL`), LOG entry, README sites, nginx `instruction.md:6-11,15-18`; gate green | ok |
| r72c2 | `SKILL.md` rows for four instruments + `plans/round-71-claims.md` erratum, no input digests | `INSTRUMENTS` = exactly those four (4); `CLAIMS_REL` erratum; gate green | ok |

The r72c1 row does not pin a probe-blob value (r71c1 does); not a defect — the standard requires a
pinned-value cell, not a particular constant — but the asymmetry is noted.

## 6. Self-test spellings

| instrument | row spelling | script | observed |
|---|---|---|---|
| r71c1 | "none declared in the script; the receipt of record is the self-test …" | **`--selftest` exists** (`:840`, `run_selftest` `:733`) | contradiction — F5 |
| r71c2 | `--selftest --work DIR` / `--mutants --work DIR` | `:352-356`, `:361-365` | **ran**: `defects-in-fake=4 want=4 all-fail=True`; `MUTANTS total=4 killed=4` — matches cell |
| r72c1 | `--selftest --work DIR` (`red_refused=8/8 accept_ok=1 state_sensitive=1 path_independent=1`) plus two refusal controls | `run_selftest :867`, print `:962`; `run_control :671`; `run_stub_control :988` | format matches source; **not run** (full 9-case battery) |
| r72c2 | `--selftest --work DIR` / `--mutants --work DIR` | `:465-469` | **ran**: `defects-in-fake=3 want=3 all-fail=True append-only-arm=True positional-arm=True parser-arm=True`; `MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1` — exact match |

Note on r72c2's `ARM … attribution=ok`: the token is printed unconditionally (`:455`); the return
value nevertheless gates on it through `invalid` (`:439`, `:459-460`), so the quoted line is
decorative but not false. Not a registry defect.

## 7. Findings

**F1 — all four rows: the declared `2` usage class is not implemented (high).**
Every row maps a usage error to `2` (could-not-evaluate), but every script lets
`raise SystemExit("<message>")` produce **exit 1**. Demonstrated live for the exact spellings the
rows name: `--selftest` without `--work` → rc 1 (rows 2,3,6,8 above), `--mutants` without `--work`
→ rc 1 (rows 7,9). `--control` without `--work/--receipt` → rc 1 (rows 4,5). Only argparse-level
errors exit 2 (rows 10-12). `round72_c2`'s "unknown fixture mode" (`:306`) is a `SystemExit` string
→ rc 1 and has **no CLI flag** to reach it. Under `PROTOCOL.md:380-383` an undeclared nonzero code
reads as could-not-evaluate, so a reader following the row maps the opposite class on every one of
these paths.

**F2 — both c1 rows: the `0` cell states the opposite of the script (high).**
Cell text: "battery ran and printed its `SUMMARY` line — mismatches, setup and provenance are data
lines, never the exit code." The battery's last line is `PREDICATE … pass|fail` and the return is
`0 if lines[-1].endswith("pass") else 1`
(`round71_c1_hf_probe.py:573`, `round72_c1_hf_probe.py:668`). A red table, a `SETUP` case, a
duplicate/absent `PROVENANCE` line or `canary_seen>0` all exit 1 — the most common failure mode is
undeclared, and the cell says it cannot happen.

**F3 — both c1 rows: `kind = probe` conflicts with F2 (medium).**
`PROTOCOL.md:377-379` defines kind by failability: "A gate is a committed, re-runnable verdict script …
returns a verdict. A tool that cannot fail is a **probe**." Both batteries compare derived vectors
against committed `VECTORS` and exit 1 on mismatch, so they can fail. Either the kind cell or the
battery's exit contract must change for the row to be self-consistent; as written the row's `probe`
label rests on the false `0`-cell premise.

**F4 — both c1 rows: write scope understates two write paths and one namespace (medium-high).**
"`--work` scratch only (per-case trees and receipts); loopback inside the sandbox only":
- `--receipt` is written wherever the caller names it (`r71 :571,:588`; `r72 :666,:684,:1021`) —
  the round's own commands write `corpus/evidence/round72/hf/receipt.txt` and `stub-control.txt`.
- `--evidence-dir` writes per-case `sandbox-stdout.txt`/`sandbox-stderr.txt`/`manifest.json`/
  `app-tree.txt` (`r71 :477`; `r72 :555`), outside `--work`, into a lane path.
- The sandbox runs `bwrap --unshare-all --share-net` (`round72_c1_hf_probe.py:495-496`), i.e. it
  **shares the host network namespace**; "loopback inside the sandbox only" is not what the flags do.

**F5 — `round71-c1-hf-probe` self-test cell is false and self-contradictory (medium).**
"none declared in the script" while the same row's entry cell lists `--selftest` and the script
defines it (`argparse :840`, `run_selftest :733`). The cell also calls the receipt "the self-test",
which conflates evidence with an invocation mode; the Gate standard's self-test clause is about a
self-invocation over isolated fixtures.

**F6 — c1 rows' `2` sub-cases (digest mismatch, port busy, bwrap missing, bwrap without
`--clearenv`) are not exit 2 (medium).**
- digest mismatch: `prepare_work` raises `SystemExit` (`r71 :503,:509`; `r72 :582,:588`) — proven
  rc 1 at command 22.
- port 5000 busy: `wait_port_free` fails → a per-case `SETUP` data row (`r72 :523-526`), then
  `setup>0` makes the battery return 1 (`:638,:668`), never 2.
- bwrap missing: `subprocess.run` raises `FileNotFoundError`; only `TimeoutExpired` is caught
  (`:530-533`) → traceback, rc 1.
- bwrap "without `--clearenv`": there is **no capability probe** anywhere in either script
  (`grep clearenv` finds only the comment and the argv); on an old bwrap the cases would fail as
  `SETUP` and the process would exit 1.

**F7 — item 3: the R71-R1 class has recurred and is not closed at lane level (high; outside the
four rows' own cells).**
`plans/round7[12]_*.py` on disk = exactly four files, and each has a row:
`round71_c1_hf_probe.py`→`:695`, `round71_c2_routed_defects.py`→`:696`,
`round72_c1_hf_probe.py`→`:697`, `round72_c2_routed_defects.py`→`:698` (1:1; all bind in
`round52-c2`'s parser). But the lane's own registry gate is red at tip: `MISSING 5` —
`plans/round66_c1_tensor_probe.py`, `plans/round69_c1_nginx_probe.py`,
`plans/round69_c2_routed_defects.py`, `plans/round70_c1_nginx_probe.py`,
`plans/round70_c2_routed_defects.py` — `PREDICATE R52-C2 fail`, rc 1 (command 23; the sibling
`corpus/evidence/round72/registry-debt.txt` records the identical run at the same tip).
Base `c6322972` was red too, at `MISSING 7` (the same five plus both round-71 scripts), so the
round-72 rows closed exactly the two R71-R1 instruments and left the other five. The
`round66_c1_tensor_probe` row exists at `SKILL.md:688` but is **five columns** (six pipes; name,
kind, entry, one verdict code, one pinned-prose cell) — no self-test, write-scope or owner column —
so `round52-c2`'s `parse_rows()` drops it (`len(cells) != 8` → `continue`) and it surfaces as
MISSING, not INCOMPLETE. The class has now recurred at least three times (its own cell text says the
row "was missing at `0e52fb5d`", re-found in round 68 attempt 2; rounds 69–70 added four more
instruments with no row; round 71 added two more, i.e. R71-R1).

**F8 — the closing gate re-derives the instance, not the class (medium; calibration note).**
`round72_c2`'s `E1a` (`:106-126`) iterates a hardcoded `INSTRUMENTS` tuple of four names and checks
only: row present, `len(cells)==8`, entry cell names the script, kind ∈ {gate, probe}, owner ==
`kengaku`. It does not read the self-test, pinned-value or write-scope cells, and it cannot see an
instrument absent from its tuple — so the F1–F6 defects pass it, as would any future round-73
script not added by hand. Positively: unlike `round52-c2`, its `registry_rows()` keeps non-8-cell
rows, so a malformed row like `:688` *would* be reported as `row-columns` if the instrument were in
`INSTRUMENTS`.

**F9 — both c1 rows: the entry command named in the row does not reach the instrument (medium).**
`python3 plans/round71_c1_hf_probe.py --lane .` and the round-72 twin print the usage block and exit
**2** (command 26): `main()` falls through to `ap.print_help(); return 2` when no mode flag is given
(`r71 :867-868`; `r72 :1071-1072`). The verdict map in the same row then describes a battery run
("0 battery ran and printed its SUMMARY line") that the advertised command cannot produce. The
round's own counting command supplies `--work --receipt …`; the row should name a mode
(`--check-receipt …` or the battery form), as the `round66_c1_tensor_probe` row does.

## 8. What is right (so the record is not only negative)

- R71-R1's named instance is closed: both round-71 scripts have eight-column rows whose entry cells
  name the script, with `kind` and `owner`; both moved from MISSING to registered at the tip.
- R71-R7's erratum exists as the file's last `##` section (`plans/round-71-claims.md:137`), quotes
  both superseded labels verbatim above it and names both true revisions (`c80fcdb3`, `d8a77d3f`);
  `E1b`/`E2` pass live.
- `round72-c2` is green at tip (`E1a`–`E2`, `DEFECTS n=0`, `PREDICATE R72-C2 pass`, rc 0), and its
  selftest and mutant tallies reproduce the row's numbers exactly (commands 13, 17, 18).
- `round71-c2` is green at tip and its `E1a…E2a` output and `MUTANTS total=4 killed=4` reproduce
  (commands 14–16).
- Both c1 receipts are internally consistent (`DEFECTS n=0`, `PREDICATE … pass`); the round-71
  receipt carries eight `VECTOR … agree=True` and `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`, exactly
  as the row's self-test cell claims.
- All four entry cells match the real flag sets exactly (the primary question the item asks).

## 9. Unrun / limits

- r72c1 and r71c1 `--selftest`, `--control` and `--stub-control` batteries were **not run**: they
  stage live `bwrap` batteries against shared port 5000 and duplicate the C1 lane's work. Their
  formats were read from source and the two committed receipts were checked instead. F2/F6 rest on
  source lines and the direct rc measurements in command 22, not on a battery observation.
- `corpus/evidence/round72/hf/stub-control.txt` (claim counting command 3) does not exist as of this
  audit; the row's `1` branch for `--stub-control` is implemented (`:1024`) but has no committed
  receipt to exercise it. Not a registry defect; a lane-state observation.
- The base-tree arm of `round52-c2` used a partial `git archive` (no `grader.py`); its
  `ENTRY-MISSING grader.py` line is an artifact and is excluded from §7.
- Cell verdicts for `kind` (F3) are a standards reading; the canonical judge decides whether the
  lane may register a fail-able battery as `probe`, but the `0`-cell rationale for it is false
  either way.

## 10. Verdict

**Four rows, four defects; no row conformant. 11 of 32 cells defective.** The two c2 rows are
one-cell defects (the `2` usage mapping); the two c1 rows carry the heavier ones (entry, kind,
`0`-cell, write scope, and for r71c1 the self-test cell). The four round-72 rows do close R71-R1's
named instance — but the lane's own registry gate is red at the round tip with five instruments still
unregistered or unparseable, so the *class* R71-R1 raised can recur, and has.
