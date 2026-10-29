# C2ExecRowsE report (round 53 wave 1, R53-C2)

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ExecRowsE/ledger-part.json` (8 rows). Nothing in the lane was edited.

## Method (commands)
- Clones under `/fast/scratch/hyaku/kengaku-r53/C2ExecRowsE/tmp.*` (removed before yield): `git clone -q --shared <lane> baseN|headN`, each `git rev-parse --show-toplevel` printed the clone dir. `base1/base2` = detached `536925b5…` (base tip); `head1/head2` = lane HEAD `1373b6c` (base + claims + spec commits; adds only counters/claims files, none of the probed trees).
- Each argv run with `cwd=<clone>`, `TMPDIR` = a per-row dir under the scratch root, 900 s timeout, `capture_output` (stdout+stderr). Runs: base x2 (all rows), head x2 (all rows), plus ledger-tip once more on base1 after `git branch -f master 536925b` inside my own clone. Exit codes agreed on every repeat; no flaky row.
- Evidence fragments were checked verbatim against every observed output (stdout+stderr).

## Per row
| row | argv (after `python3`) | exit | sec | state | kind |
|---|---|---|---|---|---|
| build-pmars-probe | `plans/build_pmars_probe.py --lane .` | 0 | 1.7 (4.6 cold) | green | entry |
| feal-probe | `plans/feal_probe.py --lane .` | 0 | 99.2 | green | entry |
| ledger-tip | `plans/ledger_tip.py --lane .` | 1 | 5.1 | red | entry |
| round28-census | `plans/round28_census.py --root . --revision 536925b5320fa64298030b4ee76a58fc4b82723f` | 1 | 1.9 | red | entry |
| round36-c2 | `plans/round36_c2_verify.py --lane .` | 1 | 0.5 | red | entry |
| round40-c2 | `plans/round40_c2_verify.py --lane .` | 1 | 3.2 | red | entry |
| round45-c1 | `plans/round45_c1_verify.py --lane .` | 0 | 8.9 | green | entry |
| round52-c1 | `plans/round52_c1_grader_audit.py --lane .` | 1 | 0.6 | red | entry |

All kind=entry, no help/selftest argv. Argument sources: every argv is the entry cell's own `--lane .` / `--root .` form; the only invented value is the `--revision` label (the base-tip sha from the claims file; the script accepts any caller label). ledger-tip uses the cell's "control mode `--lane <clone>`" because the `--source/--work` form needs `--work`, which the counter forbids; `--lane .` is the lane root of the counter's worker clone.

## Red rows: cause, evidence, tip dependence
- **ledger-tip** — closed row R35-D1 observes fail: its check re-runs `pkg_gate package --rerun` whose P8 leg reports `index_rows=55 knowledge_files=56` (verified by running the gate in head1), so `false_red=1 tip_package_rc=1`. Evidence `R35-D1 status=closed observed=fail agree=NO`. **Tip-dependent**: re-measure after `corpus/README.md` index rows / `corpus/knowledge/*.md` are final. Caveat: on a clone whose `refs/heads/master` is not the audited commit the script exits 2 (`REFUSE stale pin ref`); my detached base clone gave exit 2 until I set master; the counter's source must be a normal clone of the landing tip with master at HEAD.
- **round28-census** — exit 1 from two legs: state_check `P3c.box.4.pointer.1` MISMATCH (PROVINCE.md:129 token `### Adjacent` absent) and one unindexed file `knowledge/fixture-honest-geometry.md` (files 56 / index 55). Evidence `"MISMATCH": 1,`. **Tip-independent** (the state_check mismatch persists even if the index is repaired). Counts like `total_json_records` shift by +1 at head (503 -> 504), not the exit.
- **round36-c2** — `W4 DEFECT knowledge files=56 index rows=55 (want equal and >=43)`, `checks=6 defects=1`. **Tip-dependent**: re-measure after `corpus/README.md` and `corpus/knowledge/` are final (indexing every new entry should flip it green).
- **round40-c2** — V2 fails because gate leg `P8 DEFECT index_rows=55 knowledge_files=56`; V1, V3–V7 ok, `checks=7 defects=1`. Evidence `gate: P8 DEFECT index_rows=55 knowledge_files=56`. **Tip-dependent**, same files as round36-c2.
- **round52-c1** — `PREDICATE R52-C1 fail` because `CAPTURES expected=184 present=183` (operator-excluded `sanitize-git-repo` capture is absent); `PREDICATE R52-C1-A5 pass` is printed after it, but exit is 1. Evidence `CAPTURES expected=184 present=183 mismatched=0`. **Tip-independent**.

round36-c2, round40-c2 and ledger-tip share one cause (corpus/README.md index vs corpus/knowledge file count): the L1 must re-measure all three after landing the knowledge entry and its index row; round28-census stays red either way.

## Registry cells that disagree with observation
- `ledger-tip` verdict cell: "`0` every closed ledger row's check passes at the tip" — observed exit 1, `R35-D1 … agree=NO`.
- `round40-c2` self-test/pinned cells: "measured green at the landing tip" — observed exit 1 (P8 index drift).
- `round52-c1` verdict cell: "`0` `PREDICATE R52-C1 pass`: `CAPTURES expected=184 present=184 …`" — observed exit 1, `present=183`, only the A5 line passes.
- `round36-c2` states the base-tip failure as "`W4 DEFECT knowledge files=55 index rows=54`" — count drifted to 56/55 (state agrees, number stale).
- `round28-census` cell (red at `30801b47`, `mismatch=1` `P3c.box.4.pointer.1`, one unindexed file) still matches; counts in its pinned cell (`knowledge files 55 against 54 index rows`) are stale.
- build-pmars-probe, feal-probe, round45-c1 cells agree (exit 0; probes `mismatches=0`, round45 `PREDICATE C1 pass`).

## Tooling / anomalies
No tools installed. Probe wall times vary with load (build-pmars 4.6 s cold, 1.7 s warm; feal ~100 s) — well under 900 s. Scratch removed; no lane or fleet file written other than this report and ledger-part.json.
