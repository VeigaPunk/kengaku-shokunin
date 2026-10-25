# Round-25 out-of-population scout

## Run and scope
- Ran `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/state_check.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --json`: summary `assertions=235 match=231 mismatch=0 superseded=1 offline_unverifiable=3 out_of_population=14`.
- P2e freezes README rows/files; `plans/state_check.py:60-62,1017-1079` defines its scope and semantics. P3a–e below are planned, not implemented here (`plans/round-26-claims.md`, §C2).
- `OUT_OF_POPULATION` receipts list 2 capability cells, 5 README rows and 7 on-disk paths:

| Observed item | Assertion if admitted | Receipt/verification |
|---|---|---|
| `SCORECARD.md:558` interval-reverdict | P3a numeric tokens in capability cell match named receipts | `attrib-calibration-summary-v2.txt`, `attrib-calibration-selftest-v2.txt`; rerun `python3 plans/attrib_calibration.py --summary` and `--selftest`. Cell says 14 checks; receipt ends `18 checks, 0 failed`. |
| `SCORECARD.md:559` state-assertion-check | P3a numeric tokens in capability cell match named receipts | `state-check-before-6180e4f-v2.txt`, `state-check-after-v2.txt`; rerun `python3 plans/state_check.py --summary`. Before receipt says `mismatch=10`, while cell says 11. |
| README row `knowledge/attribution-interval-calibration.md` (`corpus/README.md:61`) | P3e row-to-file resolves to a file | `test -f corpus/knowledge/attribution-interval-calibration.md` (content is not tested). |
| README row `lessons/round-24-verifier-spotcheck.md` (`:92`) | P3e row-to-file resolves to a file | `test -f corpus/lessons/round-24-verifier-spotcheck.md`. |
| README row `lessons/round-25.md` (`:93`) | P3e row-to-file resolves to a file | `test -f corpus/lessons/round-25.md`. |
| README row `evidence/round25-sources/` (`:167`) | P3e row-to-directory resolves | `test -d corpus/evidence/round25-sources/`. |
| README row `evidence/round25-calibration/` (`:168`) | P3e row-to-directory resolves | `test -d corpus/evidence/round25-calibration/`. |
| On-disk `evidence/round25-calibration/` | P3e file-to-row: existing path has README index row | `test -d corpus/evidence/round25-calibration/` and README row `:168`. |
| On-disk `evidence/round25-sources/` | P3e file-to-row: existing path has README index row | `test -d corpus/evidence/round25-sources/` and README row `:167`. |
| On-disk `evidence/round26-calibration/` | Hypothetical P3e file-to-row; **excluded from frozen P3e** because post-base | `grep -n round26 corpus/README.md` returned no match; if admitted now, index-row requirement fails. |
| On-disk `evidence/round26-sources/` | Hypothetical P3e file-to-row; **excluded from frozen P3e** because post-base | Same no-match command; if admitted now, index-row requirement fails. |
| On-disk `knowledge/attribution-interval-calibration.md` | P3e file-to-row: existing file has README index row | `test -f corpus/knowledge/attribution-interval-calibration.md`; README row `:61`. |
| On-disk `lessons/round-25-verifier-spotcheck.md` | P3e file-to-row: existing file has README index row | File exists; `grep -n round-25-verifier-spotcheck corpus/README.md` found no match. **Would fail P3e unless indexed.** |
| On-disk `lessons/round-25.md` | P3e file-to-row: existing file has README index row | `test -f corpus/lessons/round-25.md`; README row `:93`. |

## Round-25 self-assertions not covered by P2 or planned P3
- **Knowledge-entry content:** `corpus/knowledge/attribution-interval-calibration.md` contains CP bounds, 92/92 and transition totals, plus falsify-wave numeric corrections; P3e checks only its row/file existence. Check with `python3 plans/attrib_calibration.py --summary`, v2 summary receipt, `plans/fixtures/r25/cp_reference.tsv` and `attrib-oracle-intervals.txt`.
- **SCORECARD narrative/corrections:** `SCORECARD.md:647-650,665-685,701-722` has R25-E2–E5, C1/C2 claim tables, Brier values and axis-state assertions. P3a covers only capability cells; P3d covers anchored line content, not these numeric assertions. Receipts/commands include `attrib_calibration.py --summary`, `state_check.py --summary`, the cited lesson/commit, and the in-row `grep` commands (`:648-650`).
- **SKILL additions:** `SKILL.md:467-470` asserts the 17/26/34 sample-size thresholds; `:557-558` asserts capability/selftest/manifest details. No P2/P3 class scans these rows. Verify thresholds with `python3 plans/fixtures/r25/power_table.py --check`; verify selftest claims with the respective `--selftest` commands and committed v2 receipts.
- **PROVINCE report-outs:** `PROVINCE.md:168-171` makes round-25 attribution-scope conclusions outside the four P3b lines (`:112,:116,:117,:119`). Check against `corpus/knowledge/attribution-interval-calibration.md` and `falsify/ConnKumitateReportOut.md`.
- **README prose/index additions:** P2/P3e only check index/path parity. `corpus/README.md:61`'s numeric abstract, plans rows `:182-187`, coverage-map row `:226`, and frontier corrections `:254-255` are not content-checked; P2e scans only immediate `corpus/knowledge`, `lessons`, and `evidence` children (`state_check.py:1017-1030`). Verify rows against their named files and the offline commands above.
- **Lesson content:** `corpus/lessons/round-25.md` gets only P3e index/path coverage; Q13 separately checks Gate citation timing, not the rest of the lesson's claims. The unindexed closure report is integrator-authored, not lane-authored, but its missing README row is a P3e file-to-row failure if included.
- Round-26 paths are post-base and explicitly outside frozen P3e; no README rows exist yet. Current `PROVINCE.md:175-178` already appends R26-E3; `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` returned `42`, which is the P3b census value.
- No LSP route was exposed in the available tools; source-scope findings above are grounded in the state-check JSON and cited source lines. No tools installed.

VERDICT: P2 reports 14 exclusions; planned P3 extends checks to the listed round-25 populations, but leaves substantive content claims outside its enumerated checks. P3e should catch the unindexed round-25 closure lesson; keep post-base round-26 directories excluded.
