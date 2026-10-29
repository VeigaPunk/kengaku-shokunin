# C2ExecRowsC — round 53 wave 1 (R53-C2 tip-state, 9 rows)

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ExecRowsC/ledger-part.json` (9 entries, exactly my rows).

## Method
Clean shared clones of the lane at its committed HEAD `1373b6ca` (= base tip `536925b` + a34838f claims + 1373b6c wave spec; `git status --porcelain` empty;
`git rev-parse --show-toplevel` printed the clone dir before every run). One fresh clone per row per repetition
(`git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin <scratch>/rows/<row>/lane{1,2}`), `cwd`=clone, `TMPDIR` = a per-run dir, timeout 900 s,
two runs each, all nine rows in parallel (9 workers). Driver: scratch `drive.py` (removed). Two exit codes agreed for every row; stdout+stderr of the two runs
were byte-identical for all nine rows (`cmp`). No `--work`/`--scratch` passed. Static check: each argv contains the script `row_script()` extracts from its row (all 9 True).
Note: HEAD is not literally `536925b`; the only differences are claims/counters/pin files (no corpus/SKILL/README change), so the observed states are base-tip states.

## Per row (argv after `python3`; exit; wall s (run1/run2, 9 jobs in parallel); state; kind=entry for all)
| row | argv | exit | s | state |
|---|---|---|---|---|
| attrib-probe | `plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md` | 0 | 0.1/0.1 | green |
| extraction-policy-compare | `plans/parser_policy_compare.py --summary` | 0 | 0.5/0.5 | green |
| hermetic-grader | `grader.py` | 0 | 0.4/0.4 | green |
| registry-reference-check | `plans/registry_check.py --summary` | 0 | 0.1/0.1 | green |
| round35-hardening | `plans/round35_hardening.py --lane .` | 0 | 0.5/0.1 | green |
| round39-c2 | `plans/round39_c2_verify.py --lane .` | **1** | 11.2/17.4 | **red** |
| round44-c1-mutants | `plans/round44_c1_verify.py --lane .` | 0 | 11.2/17.0 | green |
| round51-routing | `plans/round51_routing.py --lane . --run-checks` | 0 | 2.1/1.5 | green |
| tip-receipts | `plans/tip_receipts.py --lane .` | 0 | 168.2/106.2 | green |

Argv sources: all are the row's own entry cell verbatim; the only placeholder was tip-receipts `--lane DIR`, replaced by `.` (lane root, as in sibling rows).
No help-kind rows from me; no selftest fallback was needed.

Observed key lines (green): attrib-probe `FREEZE-CHECK … stable=True -> OK`; extraction-policy-compare `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`;
hermetic-grader `CHECKS n=733 mismatches=0`; registry-reference-check `source_rows_checked=13 … finding_count=0 exit=0`; round35-hardening `hardening run=6 failed=0`;
round44 `PREDICATE C1 pass` (`BATTERY fixtures=33`); round51-routing `VERIFIED ran=41 passed=41 failed=0`, `PREDICATE R51-C2 pass`;
tip-receipts `receipts=33 byte_equal=12 differ=0 skipped=21`, control `verdict=differ`.

## The one red row: round39-c2 (exit 1, tip-independent)
Output: `checks=7 defects=1`, `PREDICATE C2 fail`; V2 DEFECT because the embedded gate exits 1; the single gate defect is
`gate: P8 DEFECT index_rows=55 knowledge_files=56 …` (`pkg_gate.py c_readme`: set of `corpus/knowledge/*.md` names != set of `` | `knowledge/…` `` index rows in `corpus/README.md`).
Cause: `corpus/knowledge/fixture-honest-geometry.md` (added in round-50 commit 822f3b7) has only a README coverage bullet (README:664), never a `| \`knowledge/…\` |` index row, and is therefore the one unindexed file at 536925b too.
Tip-independent: a round-53 knowledge entry plus its own index row keeps the delta at one (counts become 57/56). It turns green only if the L1 adds an index row for fixture-honest-geometry.md
(then the declared `red` would MISMATCH — L1 must re-declare). V6 (census) and P9 (clean tree) also depend on committed `corpus/SOURCES.md` shape and a clean clone: re-measure round39-c2 after the S194+ rows land.
Evidence fragment chosen count-independent: `gate: P8 DEFECT` (present in both runs). Ledger `tip_dependent=false`.

## Watch-points on green rows (tip-dependence the L1 should re-measure after landing; ledger tip_dependent=false because they pass on any compliant addition)
- round51-routing: reads `corpus/routed-findings.jsonl` (75 rows) and executes 41 `fixed-verified` checks via `bash -lc` against `SKILL.md`, `SCORECARD.md`, `LOG.md`, knowledge entries; check R39-R5 also needs no `/fast/scratch/hyaku/kengaku-r39*` dir (host state). New routed rows this round must be complete/attributed.
- tip-receipts: population = committed `corpus/evidence/**/probe*.{txt,log}` at HEAD and their `doc=SKILL.md:<line>` mapping; a new `probe*` receipt or SKILL.md row shift could change `byte_equal`/`skipped` counts (exit stays 0 unless `differ`). Slowest row, ~106–168 s with 9 parallel jobs; <=900 s timeout is safe.
- round35-hardening H6 counts untracked files: it passed only because the clone is clean (live lane with wave files fails it, as the row's text already says).

## Registry cells that disagree with observation
- `round39-c2` exit cell: "`0` `checks=7 defects=0` then `PREDICATE C2 pass`" — observed exit 1, `checks=7 defects=1` (P8 above). The registry row carries no tip-state note.
- No other row disagreed: round35-hardening (`run=6 failed=0`), round51-routing (`ran=41`), extraction-policy-compare (`TOTAL …1089…`), registry-reference-check (13 rows/35 paths), attrib-probe (`1b2d6a01bfa431ec`) all match their cells. (round44 cell says `fixtures=<n>`; observed 33.)

## Tools / anomalies
No installs. No tool-output inconsistencies observed. Scratch `/fast/scratch/hyaku/kengaku-r53/C2ExecRowsC/` removed before yield.
