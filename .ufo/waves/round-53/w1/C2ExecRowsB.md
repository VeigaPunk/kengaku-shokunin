# C2ExecRowsB — wave 1 report (R53-C2, 9 registry rows)

Seat: executor. Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ExecRowsB/ledger-part.json` (9 entries, validated: every red reason >=10 words, evidence >=6 chars and verified verbatim in the observed output). Driver kept at `.../C2ExecRowsB/run-rows.py`.

## Method
- `C=$(mktemp -d -p /fast/scratch/hyaku/kengaku-r53 C2ExecRowsB.XXXX)`; per row and per run a fresh `git clone -q --shared` of the lane (HEAD `1373b6c`; `git rev-parse --show-toplevel` asserted equal to the clone dir before each run). `git diff --name-only 536925b 1373b6c` touches only `plans/round53_*`, `plans/round-53-claims.md`, `corpus/evidence/round53`, `.ufo/waves`: `SKILL.md`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/` are byte-identical to the base tip, so every row input equals the base tip's.
- Each argv run with `cwd=<clone>`, `TMPDIR=` dir under scratch, timeout 900 s, 9 rows in parallel; run twice (fresh clone each time). Post-run `git status --porcelain` empty for every clone.
- Exit codes agreed on both runs for all 9 rows and the combined stdout+stderr was byte-identical (`cmp`) for all 9: no flaky row. `help`-kind rows: 0.

## Per row (argv, exit, seconds run1/run2, state, cause)
| row | argv (after `python3` unless noted) | exit | sec | state |
|---|---|---|---|---|
| anchor-digest-check | `plans/anchor_digest_check.py --lane .` | 1 | 0.2/0.1 | red |
| defect-ledger | `plans/defect_ledger.py --lane .` | 0 | 0.2/0.1 | green |
| grader-perturb | `plans/grader_perturb.py --summary` | 0 | 0.5/0.3 | green |
| regex-log-probe | `plans/regex_log_probe.py --lane .` | 0 | 0.1/0.1 | green |
| round35-c1-coverage | `plans/round35_c1_verify.py --lane .` | 1 | 1.1/0.7 | red |
| round39-c1-mutants | `plans/round39_c1_verify.py --lane .` | 1 | 143.6/82.8 | red |
| round43-c2 | `plans/round43_c2_verify.py --lane .` | 1 | 105.5/98.9 | red |
| round50-c2 | `plans/round50_c2_audit.py --lane .` | 0 | 0.7/0.3 | green |
| tb2-grader-probe | `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` | 0 | 0.4/0.2 | green |

All kind `entry`. `DIR` in the anchor-digest-check cell became `.` (lane root, the cell's own `--lane DIR`); no other placeholder arises. No `--work`/`--scratch` argument passed.

Green summary lines observed: defect-ledger `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`; grader-perturb `TOTAL population=1964 excluded=0 audited_verdicts=15168 ...`; regex-log-probe `cases=24 observed_pass=8 observed_fail=16 mismatches=0`; round50-c2 `POINTERS total=299 paths=233 hashes=66 resolved=299 ... unresolved=0`; tb2-grader-probe `cases=18 observed_pass=5 observed_fail=13 mismatches=0`.

## Red rows
1. **anchor-digest-check** (exit 1, `rows=186 tokens=92 defects=21`): 21 SOURCES rows S173-S193 (corpus/SOURCES.md lines 188-208) have a sha256 anchor token but no capture locator in the row (`class=anchor-unbound`). Evidence: `class=anchor-unbound detail=row-carries-no-capture-locator`. **Tip-dependent**: re-measure after the round's final `corpus/SOURCES.md` (S194+ rows opened this round add rows; they stay green only if each anchor token has a locator or no sha256 anchor). The evidence fragment holds as long as any one unbound row remains.
2. **round35-c1-coverage** (exit 1, `V4 DEFECT knowledge files=56 index rows=55 (want 42/42)`, `checks=6 defects=1`): V4 hard-codes `len(files) == nidx == 42` (`plans/round35_c1_verify.py:154`). **Tip-independent**: red whatever this round commits; evidence `(want 42/42)` is stable (the counts before it drift). V5 (uv biopython) and V6 passed; note V6 runs the census on the live fleet lane via the default `--fleet`, not the clone.
3. **round39-c1-mutants** (exit 1, `BATTERY fixtures=90 wrong=54`, `MUTANTS total=7 killed=6 survived=1`, `PREDICATE C1 fail`): the embedded package gate's P8 (`plans/pkg_gate.py:255`) fails on every fixture: 56 knowledge files vs 55 README index table rows. The orphan is `corpus/knowledge/fixture-honest-geometry.md` (added by `822f3b7`, round 50; README line 664 mentions it as a bullet, but `INDEX_ROW` needs a `| \`knowledge/...md\` |` table row). Mutant M06 (rc-mirror, genuine package must exit 0) survives because the genuine package now exits 1. Evidence `MUTANT M06 MAIN rc-mirror SURVIVED exhibits=none`. **Tip-dependent**: depends on `corpus/README.md` and `corpus/knowledge/*`. The L1 must re-measure after the round's README/knowledge edits (a new entry + its index row keeps the 1-file gap; indexing the orphan would turn this row and round43-c2 green, and the ledger would then need green declarations).
4. **round43-c2** (exit 1, `checks=10 defects=1`): same P8 cause surfaced as `gate: P8 DEFECT index_rows=55 knowledge_files=56` and `V2 DEFECT spec=frozen gate=frozen gate_exit=1`; V1, V3-V10 ok. Evidence `V2 DEFECT spec=frozen gate=frozen gate_exit=1`. **Tip-dependent**, same files as row 3 (re-measure after `corpus/README.md`/`corpus/knowledge/`).

## Registry cells that disagree with observation
- `round39-c1-mutants` verdict map says exit 0 with `MUTANTS total=7 killed=7 survived=0 ... PREDICATE C1 pass`; observed `killed=6 survived=1`, `wrong=54`, exit 1.
- `round43-c2` verdict map says exit 0 `checks=10 defects=0`; observed `checks=10 defects=1`, exit 1.
- `round35-c1-coverage` self-test cell: "measured 55 files / 54 index rows at the base tip `30801b47` and at HEAD"; observed now 56 files / 55 rows (red-by-construction statement still true).
- `anchor-digest-check` self-test cell: "Measured on the lane tip `44b7298`: `rows=103 tokens=11 defects=5`"; observed `rows=186 tokens=92 defects=21` with class `anchor-unbound`, a class the row's verdict map (`digest-short`/`digest-unknown`) does not mention.
- `round50-c2` verdict map: `POINTERS total=292 paths=228 hashes=64 ... exists=216` at `1315234b`; observed total=299 paths=233 hashes=66 exists=221 (exit still 0, count text stale).
- `defect-ledger`, `grader-perturb`, `regex-log-probe`, `tb2-grader-probe`: cells agree (tb2-grader-probe cell "uv ... reaches the network": ran in 0.2-0.4 s, biopython came from the uv cache; a cold cache needs network).

## Tools / hazards
- No installs. `tool:` none inconsistent.
- First driver run printed nothing (my own filter bug: empty selection); fixed, re-run. A background subshell I started for run 2 was killed with its shell; run 2 was redone in the foreground. Neither affected measured numbers.
- Scratch `/fast/scratch/hyaku/kengaku-r53/C2ExecRowsB.*` removed before yield.
