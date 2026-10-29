# C2ExecRowsD — round 53 wave 1 (R53-C2, rows D)

Clone: `git clone -q --shared` of the lane at HEAD `1373b6c` (one clone per row under `/fast/scratch/hyaku/kengaku-r53/C2ExecRowsD/`, `git rev-parse --show-toplevel` asserted equal to the clone path before each run, `git reset --hard` + `clean -fdx` between runs, TMPDIR per row, 900 s timeout, all 8 rows run in parallel, twice). Driver: a short python script (scratch, removed). Output of run 1 and run 2 was byte-identical for all 7 non-round-close rows (`cmp`); round-close-check was run twice separately (identical, exit 0, 0.4 s each). Exit codes agreed on every row: no flaky row. Scratch removed before yield.

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ExecRowsD/ledger-part.json` (8 rows). No `--work`/`--scratch` in any argv. No help-kind row.

## Per row (argv after `python3`; all `kind: entry`)
| row | argv | exit | s | state |
|---|---|---|---|---|
| benchmark-spec-audit | `plans/benchmark_spec_audit.py --summary` | 0 | 0.4 | green |
| feal-linear-probe | `plans/feal_linear_probe.py --lane .` | 0 | 10.4 | green |
| interval-reverdict | `plans/attrib_calibration.py --summary` | 0 | 0.6 | green |
| round-close-check | `plans/round_close.py --lane . --round 44 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | 0 | 0.4 | green |
| round36-c1-battery | `plans/round36_c1_verify.py --lane .` | 1 | 19.2 | red |
| round40-c1-mutants | `plans/round40_c1_verify.py --lane .` | 1 | 157.7 | red |
| round44-c2 | `plans/round44_c2_verify.py --lane .` | 1 | 13.4 | red |
| round51-surfaces | `plans/round51_surfaces.py --lane .` | 1 | 0.2 | red |

Seconds are from run 1 (run 2: 0.4, 8.1, 0.6, 0.1(exit 2 variant), 8.4, 136.1, 8.9, 0.4).

## Argument sources
- `--summary` / `--lane .`: the row's own entry cell.
- round-close-check: `N` = 44 chosen because round-44's claims name `corpus/evidence/round44/feal-linear-probe.txt` as a readable receipt. Round 52 (my first try, exit 2 both runs) prints `the claims name no readable receipt for round 52`, which is the cell's documented exit 2. `--census` is the fleet's `scripts/sources-census.sh`: a path **outside the lane**, necessary because a clone under /fast/scratch has no census in its parents (cell: "`--census` else `$SHOKUNIN_ROOT`, else the lane's parents"). The counter's own cwd is a scratch clone, so the same absolute path applies there. I also confirmed rounds 40-43 give exit 0.

## Red causes
- **round44-c2** (tip-dependent): V2 gate exit 1 because pkg_gate P8 sees `knowledge files=56 index rows=55`; the unindexed file is `corpus/knowledge/fixture-honest-geometry.md` (no `| \`knowledge/...\` |` row in `corpus/README.md`; I computed the set difference with `pkg_gate.INDEX_ROW`). Re-measure after `corpus/README.md` (adding that row, or the round's own knowledge entry) changes. Evidence: `gate: P8 DEFECT index_rows=55 knowledge_files=56 bad=1`.
- **round36-c1-battery** (tip-dependent): genuine package fixture P0 rejected for the same P8 mismatch (`python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r35.json` prints `P8 DEFECT ... defects=1`); `R35-D1 status=closed observed=fail agree=NO`, `rows=4 closed=4 observed_pass=3 mismatches=1`. Re-measure after `corpus/README.md` and `corpus/knowledge/`.
- **round40-c1-mutants** (tip-dependent): `BATTERY fixtures=21 wrong=11`, `MUTANTS total=21 killed=11 survived=10`. Two causes visible in output: the ledger fixtures observe an extra `NO:R35-D1` (same P8 cause) and the anchor fixtures observe an extra `anchor-unbound` — `python3 plans/anchor_digest_check.py --lane .` on the tip prints `rows=186 tokens=92 defects=21`, all `class=anchor-unbound detail=row-carries-no-capture-locator` for S173-S193 (committed rounds 50-52 rows; append-only, so these persist unless the round amends them, and new S194+ rows could add more). That the fixtures inherit the lane clone's SOURCES/README is [INFERENCE] from the matching extra findings; I did not read the whole harness. Re-measure after `corpus/SOURCES.md` and `corpus/README.md`.
- **round51-surfaces** (tip-dependent): `NUMBER-DRIFT SF14 row claims 171, probe says SOURCES rows=186`; the 171 sits at `PROVINCE.md:113` and `plans/round51-surfaces.json:214` (`count_claim`), SOURCES has 186 rows after round 52 added S179-S193. The count will move again when this round appends S194+: re-measure after `corpus/SOURCES.md` (and any PROVINCE.md/manifest edit). If the L1 updates both claim and manifest to the final row count the row can flip green; the predicate compares to the live count.

## Registry cells that disagree with observation (cell text <= 25 words)
- round36-c1-battery: "`rows=4 closed=4 observed_pass=4 mismatches=0`, `PREDICATE C1 pass`" -> observed `observed_pass=3 mismatches=1`, `PREDICATE C1 fail`, exit 1.
- round40-c1-mutants: "`MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`" -> observed `killed=11 survived=10`, `wrong=11`.
- round44-c2: "`checks=11 defects=0` then `PREDICATE C2 pass`" -> observed `checks=11 defects=1`, `PREDICATE C2 fail`.
- round51-surfaces: "measured at tip `1315234`: `ANCHORS total=20 dup=0 missing=0`... exit 0" -> now exit 1 (NUMBER-DRIFT 1); the rest of the quoted counters still hold (`PROBES run=20 present=14 absent=6 errors=0`, `RESOLVE observed_present=14 floor=13 verdict=met`).
- round-close-check: cell says `--round N` without naming a round that works; round 52 (the most recent) exits 2. Not a contradiction, only a usability note.
- benchmark-spec-audit, feal-linear-probe, interval-reverdict: no disagreement (feal ends `cases=14 observed_pass=8 observed_fail=6 mismatches=0`; benchmark-spec-audit `findings=0 exit=0`).
- interval-reverdict note: exit 0 although stored-verdict lines read `stored=FAIL interval=UNTESTED`; the cell's exit-0 meaning ("every stored line re-derives") is not contradicted by the exit but the output does show FAIL tokens at one stream block; ledger declares green on exit.

## Tools
No installs. Missing in the host: `/usr/bin/time`, `bc` (used python timing instead).
tool: none inconsistent.
