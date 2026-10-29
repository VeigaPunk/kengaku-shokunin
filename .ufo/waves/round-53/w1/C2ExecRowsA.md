# C2ExecRowsA — tip-state of 9 registry rows (round 53 wave 1)

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ExecRowsA/ledger-part.json` (9 rows; 6 green, 3 red; all kind `entry`, no help/selftest argv).
Blindness: no C1 file read or touched. No script, SKILL.md or ledger edited.

## Method (exact)
- Clone: `git clone -q --shared <lane> $C/lane && git -C $C/lane checkout -q 536925b5…` (scratch clone only; the lane HEAD was already 1373b6c, so the clone was moved to the base tip 536925b). `rev-parse --show-toplevel` printed the clone dir; status clean.
- One clone per row (5 rows in parallel), `git reset --hard && git clean -fdx` before each run, `cwd=<clone>`, `TMPDIR` a fresh dir under the scratch root, timeout 900 s, each argv run twice. All 9 rows: both exit codes agreed (no flaky row).
- Cross-check with the frozen counter itself: `TMPDIR=… python3 plans/round53_c2_tipstate.py --lane <scratch lane with SKILL.md + ledger of only my 9 rows> --source <clean clone of 536925b> --work … --jobs 3 --only <my 9 names>` → `ROWS registry=75 ledger=9 … entry_mismatch=0 bad_decl=0 bad_reason=0`, `SOURCE rev=536925b5… clean=yes`, `RUN executed=9 timeout=0 mismatched=0 evidence_missing=0`, `TIPSTATE declared_green=6 declared_red=3 observed_green=6 observed_red=3` (PREDICATE fail there is only because `--only`/66 missing rows, as designed). 122 s wall.

## Per row (argv · exit · seconds run1/run2 · state · cause)
Common prefix `python3`, run from lane root.
| row | argv tail | exit | s | state | tip-dep |
|---|---|---|---|---|---|
| adoption-check | `plans/adoption_check.py --lane . --expect .ufo/waves/round-33/claims/adoption-expect.json --census` | 1 | 0.1/0.1 | red | no |
| db-wal-probe | `plans/db_wal_probe.py --lane .` | 0 | 3.6/2.8 | green | no |
| git-webserver-probe | `plans/git_webserver_probe.py --lane .` | 0 | 55.6/55.3 | green | no |
| polyglot-c-py-probe | `plans/polyglot_c_py_probe.py --lane .` | 0 | 3.9/3.9 | green | no |
| round33-defects | `plans/round33_defects.py --lane .` | 0 | 0.1/0.1 | green | no |
| round39-c1-audit | `plans/round39_c1_audit.py --lane .` | 1 | 110.6/51.4 | red | YES |
| round43-c1-mutants | `plans/round43_c1_verify.py --lane .` | 0 | 22.7/15.5 | green | no |
| round50-c1 | `plans/round50_c1_verify.py --lane .` | 0 | 112.5/65.9 | green | no |
| state-assertion-check | `plans/state_check.py --summary` | 1 | 2.5/3.4 | red | YES |

Argument sources: every argv is the row's entry cell verbatim with `--lane .` (or `--summary`); `--work`/`--dry`/`--smoke`/`--stage-check` omitted (the counter sets TMPDIR; db-wal, polyglot, round39, round43, round50 fall back to `$TMPDIR` via `tempfile`; checked in each script's argparse). The only placeholder was adoption-check's `<expect.json>`: `.ufo/waves/round-33/claims/adoption-expect.json`, the file the row's own *pinned* cell names.

### Red causes
- **adoption-check** (tip-independent): census leg runs the hardcoded `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <lane.parent> <lane.name minus -shokunin>`; in the counter's clone (`…/w{i}/src`) there is no `shokunin.conf` and no such lane, census exits 2 (`ERROR: config not found: …/shokunin.conf`) so the script prints `census=fail`, exit 1. The other six printed legs are `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1`. Evidence: `census=fail`. It will stay red in any clone outside the fleet root; a green would need a clone named `kengaku-shokunin` under a fleet root (the counter does not do that).
- **round39-c1-audit** (tip-dependent): package gate clause P8 (`c_readme`) fails on every fixture because `corpus/knowledge/*.md` has 56 files and `corpus/README.md` indexes 55 (`fixture-honest-geometry.md` has no index row). Result `BATTERY fixtures=90 wrong=54`, `MUTANTS total=7 killed=6 survived=1` (M06), `PINS total=26 mismatched=0`, `AUDIT C1 clean`, `PREDICATE C1 fail`. Evidence: `PREDICATE C1 fail`. L1 must re-measure after any change to `corpus/README.md` or `corpus/knowledge/` (an index row for `fixture-honest-geometry.md`, or adding a knowledge entry without its row, changes the count; red→green flips only if every knowledge file ends up indexed exactly once).
- **state-assertion-check** (tip-dependent): `assertions=329 match=317 mismatch=1 superseded=6 offline_unverifiable=5`; the single mismatch is the frozen P3c assertion that `SHONEN.md` box 4 pointer `PROVINCE.md:129` names `### Adjacent`; that line is blank (`token_hits=0`). Evidence: `MISMATCH: P3c.box.4.pointer.1:12`. L1 re-measure after any edit to `PROVINCE.md` or `SHONEN.md` (and note SCORECARD/LOG/SOURCES/README counts feed other assertions: re-run after landing).

### Green rows: tip dependence
db-wal, git-webserver, polyglot: pinned captures + bwrap (`/usr/bin/bwrap` host dependency), no read of SCORECARD/LOG/SKILL/SOURCES. round43: `PINS total=2`, no read of those files. round50-c1: reads only fence/population/mutants, `TREE dirty=0` (counter resets the tree). round33-defects reads `SCORECARD.md` only for the `## Round 32` heading (append-only) and N3/N4 read absolute fleet paths `/home/vgpnk/Projects/shokunin/.ufo/reports/round-3{1,2}/kengaku.md`, which are outside the clone (host-state dependency, not a tip dependency).

## Registry cells that disagree with observation (cell quote ≤25 words)
- adoption-check, pinned cell: "measured on `.ufo/waves/round-33/claims/adoption-expect.json` → … `census=ok`, exit 0" — observed `census=fail`, exit 1 in a clean shared clone outside the fleet root (reproduces; cell is true only when run inside the fleet checkout).
- state-assertion-check, verdict cell: "`0` all comparable frozen assertions match" — observed exit 1, `mismatch=1` (P3c.box.4.pointer.1:12).
- round39-c1-audit, self-test cell: "measured full run at the lane tip is green (§2.5), 55 s" — observed exit 1 (`PREDICATE C1 fail`), 51–111 s; P8 README-index defect.
- round33-defects, scope cell is consistent (cell says `--lane` does not redirect N3/N4; observed exit 0 anyway). git-webserver "(same run, 53 s wall)": observed 55 s: agrees.
- No cell disagreement for db-wal-probe, polyglot-c-py-probe, round43-c1-mutants, round50-c1.

## Tool notes
No tools installed. tool: the `_eval` python cell timed out at 30 s during a `git checkout` and left a half-checked-out clone (staged deletions); I removed and re-cloned it (scratch only).
Scratch `/fast/scratch/hyaku/kengaku-r53/C2ExecRowsA` removed.
