# C2ScribeRowsC — wave-1 scribe report (round 52, kengaku, hyaku run 11)

Seat: `C2ScribeRowsC` (scribe). Item: draft the missing `SKILL.md` *## Gate/probe registry* rows
for five advertised instruments. Leaf member: no subagent dispatch, no lane edits, no commits.

**Deliverable:** `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsC/rows.md`, preserved as
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsC/rows.md`
(five rows, eight registry columns each, all cells non-empty).

## What I did

1. Read `plans/round-52-claims.md` in full first (C2's frozen rules, the eight-column row
   contract, the `selftest_unbacked` definition, the four controls).
2. Checked for sibling artefacts before deriving anything:
   `/fast/scratch/hyaku/kengaku-r52/C2ExecRowFacts/` **did not exist** and
   `/fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/` contained only an empty `tmp/`. So no sibling
   measurement was available and **every fact in my rows is derived by this seat** from the five
   scripts' bytes plus runs of the five scripts.
3. Read all five scripts whole (`:1-191`, `:1-389`, `:1-266`, `:1-266`, `:1-217` raw) — docstring,
   argparse block, check list, every exit path, every path it reads, every subprocess it spawns.
4. Read `plans/round52_c2_registry.py` (`:1-130`) to learn the parser my rows must survive:
   exactly eight `|`-cells, `CMD = python3 plans/<name>.py` in the entry cell, and the
   `selftest_unbacked` rule (a cell naming exactly one `plans/*.py` script plus a `--flag` that
   script does not accept is flagged).
5. Measured every claim (commands below), wrote the rows, then validated the rows against the
   counter's own imported parser.

## Exact commands and measured output

All run from `/home/vgpnk/Projects/shokunin/kengaku-shokunin` with
`TMPDIR=/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsC/tmp`.

Sibling-artefact check:

```sh
ls -la /fast/scratch/hyaku/kengaku-r52/ ; ls -la .../C2ExecRowFacts/ ; ls -la .../C2ExecRowRuns/
# C2ExecRowFacts: No such file or directory
# C2ExecRowRuns: only tmp/ (empty)
```

Self-tests (the four scripts that declare one):

```sh
python3 plans/round31_c1_verify.py --selftest   # SELFTEST checks=6 failed=0   exit=0
python3 plans/round31_defects.py    --selftest  # SELFTEST checks=10 failed=0  exit=0 (11 CASE lines)
python3 plans/round33_c1_verify.py  --selftest  # SELFTEST cases=11 failed=0   exit=0
python3 plans/round33_defects.py    --selftest  # SELFTEST checks=14 failed=0  exit=0 (14 CASE lines)
```

The round-35 counter has no self-test (measured, not assumed):

```sh
python3 plans/round35_c1_verify.py --help       # usage: ... [-h] [--lane LANE] [--fleet FLEET]  exit=0
python3 plans/round35_c1_verify.py --selftest   # error: unrecognized arguments: --selftest  exit=2
```

Usage exit (argparse `2`) on all five:

```sh
python3 plans/<each>.py --bogus                 # error: unrecognized arguments: --bogus  exit=2
```

Frozen counter, confirming all five are advertised-and-missing:

```sh
python3 plans/round52_c2_registry.py --lane .
# ADVERTISED total=72 / REGISTERED total=44 rows=46 / MISSING 28
#   MISSING plans/round31_c1_verify.py, round31_defects.py, round33_c1_verify.py,
#           round33_defects.py, round35_c1_verify.py  (all five present in the list)
# INCOMPLETE 0 / ENTRY-MISSING 0 / SELFTEST-UNBACKED 1 (`order-check`)
# PREDICATE R52-C2 fail  exit=1
```

Run-mode verdicts on the lane (read-only):

```sh
python3 plans/round31_c1_verify.py --lane .   # checks=6 defects=0   exit=0
python3 plans/round31_defects.py   --lane .   # checks=10 defects=0  exit=0
python3 plans/round33_c1_verify.py --lane .   # checks=8 defects=0   exit=0
python3 plans/round33_defects.py   --lane .   # checks=6 defects=0   exit=0
python3 plans/round35_c1_verify.py --lane .   # V1 ok V2 ok V3 ok
                                              # V4 DEFECT knowledge files=55 index rows=54 (want 42/42)
                                              # V5 ok V6 ok / checks=6 defects=1 / PREDICATE C1 fail  exit=1
```

Red paths (empty lane, to pin the exit maps rather than infer them):

```sh
python3 plans/round31_c1_verify.py --lane <empty>
# VERIFY expect unreadable: [Errno 2] ... ; checks=6 defects=6            exit=1
python3 plans/round33_c1_verify.py --lane <empty>
# DEFECT V0 expect: ... is absent ; checks=8 defects=1                    exit=1
python3 plans/round31_defects.py   --lane <empty>
# ten DEFECT R<n> lines ; checks=10 defects=10                            exit=1
python3 plans/round33_defects.py   --lane <empty>
# DEFECT N1, N2, N5, N6 ; checks=6 defects=4 (N3/N4 stayed green)         exit=1
```

Why round-35's V4 is red and always will be — the 42/42 pin is stale, at the frozen base tip
itself, not a round-52 regression:

```sh
git ls-tree --name-only 30801b47… corpus/knowledge/ | grep -c '\.md$'   # 55
git ls-tree --name-only HEAD      corpus/knowledge/ | grep -c '\.md$'   # 55
git show 30801b47…:corpus/README.md | grep -c '^| `knowledge/'          # 54
grep -c '^| `knowledge/' corpus/README.md                               # 54
```

Rows validated with the counter's own parser (imported read-only, nothing written to the lane):

```sh
python3 - <<'PY'  # import plans/round52_c2_registry.py, parse rows.md
PY
# 5 data rows: cells=8, no empty cell, entry extracted for each, selftest_unbacked=False for each
# (a 6th parsed row is the markdown header, which the live SKILL.md header produces identically)
```

Injection simulation (add my five rows to the live registry in memory, recompute `MISSING`):

```sh
# MISSING before: 28 -> after injecting my 5 rows: 23
# my five still missing: []
# remaining 23: adoption_check, attrib_probe, catalog_probe, defect_ledger, gate_flip_check,
#   parser_policy_compare, password_recovery_probe, polyglot_c_py_probe, round28_census,
#   round30_defects, round35_hardening, round36_c2_verify, round45_c1/c2, round46_c1/c2/c3,
#   round50_c1_verify, round50_c2_audit, round51_routing, round51_surfaces, routed_open,
#   tb2_grader_probe
```

## The five rows — names and kinds

| instrument | registry name | kind | self-test cell basis |
|---|---|---|---|
| `plans/round31_c1_verify.py` | `round31-c1-literals` | **gate** | real: `--selftest`, measured `checks=6 failed=0` |
| `plans/round31_defects.py` | `round31-defects` | **gate** | real: `--selftest`, measured `checks=10 failed=0` |
| `plans/round33_c1_verify.py` | `round33-c1-literals` | **gate** | real: `--selftest`, measured `cases=11 failed=0` |
| `plans/round33_defects.py` | `round33-defects` | **gate** | real: `--selftest`, measured `checks=14 failed=0` |
| `plans/round35_c1_verify.py` | `round35-c1-coverage` | **gate** | **none declared**: argparse rejects `--selftest`, exit 2 (measured) |

`kind = gate` for all five because each exits non-zero on a defect; none prints its mismatches on
a summary line while exiting 0, which is the registry's `probe` shape.

**Rows I could not fill truthfully: none.** All five are complete, and every cell is backed by
either the script's bytes or a run recorded above.

## Findings the integrator must not lose

1. **`round35-c1-coverage` is red at the base tip by construction.** Its V4 pins
   `knowledge files == index rows == 42`; the lane carries 55/54 at `30801b47` *and* at HEAD. The
   row says so inside its pinned-values cell. If the row instead claimed "0 = clean", it would be
   false the moment a reader ran it. The other four are green as measured today.
2. **`round33-defects` reads two absolute fleet paths.** N3 and N4 read
   `/home/vgpnk/Projects/shokunin/.ufo/reports/round-3{1,2}/kengaku.md`, so `--lane` does not
   redirect them; measured on an empty lane they stayed green while the run reported
   `checks=6 defects=4`. Recorded in that row's write-scope cell.
3. **`round35-c1-verify` executes two other instruments and can reach the network**: it runs
   `plans/tb2_grader_probe.py` (V5, byte-compared to its committed receipt) and
   `scripts/sources-census.sh` (V6), and falls back to
   `uv run --no-project --with biopython==1.85` when `Bio` is not importable. Its write-scope cell
   says this, since "none" alone would understate it.
4. **Self-test cells were written to survive the frozen `selftest_unbacked` rule.** The round-35
   cell deliberately names no `plans/*.py` path: naming the script there alongside `--selftest`
   would trip the rule and manufacture the very `SELFTEST-UNBACKED` defect the rule exists to
   catch. The four real self-tests name `--selftest`, which is in each script's argparse block.

## Scope, hygiene and disclosure

- **Lane untouched.** `git status --porcelain` in the lane at the end of my seat shows my two
  report paths (`.ufo/waves/round-52/w1/C2ScribeRowsC/`, `…/C2ScribeRowsC.md`), the L1's
  `w1.ready`/`w1.ready.dispatched` markers, and other seats' wave directories — no tracked file
  modified, and nothing of mine outside my two report paths. No
  `git add/commit/stash/checkout/reset`, no `jj`, no edit to `SKILL.md`, `plans/`, `.ufo/state/`,
  `templates/`, `scripts/`, `MANIFEST.json`, or `~/.local/bin`. Nothing written under `/tmp`.
- **Measured at HEAD `1315234bdc8024499d943f0483dcb51fb5e4a618`**, one commit ahead of the frozen
  base tip `30801b47`; that single commit is the round-52 claims/counters/wave-spec freeze and
  changes none of these five scripts. Disclosed because my numbers are not literally taken at the
  base tip; the one base-tip comparison I needed (the 55/54 knowledge counts) I took directly from
  `git ls-tree 30801b47…` and `git show 30801b47…:corpus/README.md`.
- **Tooling:** no installs, no upgrades, no `pacman` transaction of any kind (host-wide pause
  respected). Everything ran on the stock `python3` and `git` already present.
- **Scratch removed** before yield: `rm -rf -- /fast/scratch/hyaku/kengaku-r52/C2ScribeRowsC/`,
  after copying `rows.md` into this report directory.

## Late cross-check against `C2ExecRowFacts` (corroboration, not source)

The sibling artefacts were **absent when this seat started** (17:00 check) and appeared at 17:03,
after my rows were written from independent derivation and my own runs. I read them afterwards and
they agree with every cell-relevant fact; I did not change a number on their authority.

| fact | my row (independently derived) | `C2ExecRowFacts` |
|---|---|---|
| flags, r31_c1_verify / r31_defects / r33_c1_verify / r33_defects | `--lane`, `--selftest` | `argparse_flag_names: ["--lane","--selftest"]`, `has_selftest_flag: true` (all four) |
| flags, r35_c1_verify | `--lane`, `--fleet` (fleet default `/home/vgpnk/Projects/shokunin`), no self-test | `["--fleet","--lane"]`, `--fleet` default `/home/vgpnk/Projects/shokunin`, `has_selftest_flag: false`, `selftest_static.functions: []` |
| selftest summary labels | `checks=` for r31_c1_verify, r31_defects, r33_defects; **`cases=`** for r33_c1_verify | `SELFTEST checks={...}` ×3, `SELFTEST cases={...}` for r33_c1_verify |
| selftest writes | r31_c1_verify none; r33_c1_verify a synthetic registry in a temp dir; r33_defects temp fixtures plus `git init`/`git add` | r31_c1_verify `writes: []`; r33_c1_verify `mkdir` + 2 `write_text`; r33_defects four `write_text` fixtures |
| default run exit | 0, 0, 0, 0 for the four; **1** for r35_c1_verify | `runtime_default.json` `default.exit_code`: 0, 0, 0, 0, and 1 |
| r35_c1_verify red line | `V4 DEFECT knowledge files=55 index rows=54 (want 42/42)` … `PREDICATE C1 fail` | byte-identical stdout head |
| r35_c1_verify network | reaches the network via `uv run --with biopython==1.85` | `network: true` |

One difference worth naming, because it shows why a static extractor is not a substitute for a
run: `facts_ast.json` lists `declared_exit_codes: []` for `round33_defects.py`, which returns
`0 if defects == 0 else 1` as a conditional expression rather than a literal `return 1`. My row
says `1` on a defect, and I measured it (`--lane <empty>` → `checks=6 defects=4`, exit 1). The
static extractor's empty list is a blind spot of its AST shape, not a contradiction of my cell.

## Files produced (absolute)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsC/rows.md`
  — the five rows, ready to paste into the *## Gate/probe registry* table.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsC/report.md`
  — this report.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsC.md`
  — the same report at the flattened path the seat trailer named (both shapes exist in earlier
  rounds' wave trees; kept identical on purpose).
