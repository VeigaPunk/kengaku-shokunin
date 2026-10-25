# Round 26 census writer report

## Changed files and behavior
- Private clone: `/tmp/kengaku-r26-ExecRound26Census`, branch `r26-ExecRound26Census`; requested base resolved to `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`.
- Wrote `plans/round26_census.sh` in the clone (lines 1–162), SHA-256 `b0fdaaa4c6f5165c8535043cd61b2d6e45f6432f27d5dbd4880a8d57e27969b4`.
- C1 captures instrument presence, `TOTAL` and interval-family count; C2 captures the first summary line and P3 mismatch count (reports absent when the checker has no P3 IDs); Q13 captures the 8ea41f9 red-before result and round-26 lesson result when its landing tree contains the lesson (`plans/round26_census.sh:41-96`).
- SOURCES rows, malformed count, tier/status histograms follow the frozen `CORPUS.md:131-141` commands; histogram order is stabilized using the round-25 census pattern (`plans/round26_census.sh:98-109`; `plans/round25_census.sh:57-69`). Knowledge index parity is bidirectional and reports missing rows, dangling rows, and duplicates (`plans/round26_census.sh:111-161`). Missing instruments print `absent`; census ends with exit 0.

## Base execution evidence
Command: `sh plans/round26_census.sh` from `/tmp/kengaku-r26-ExecRound26Census`.

```text
head=e0037a8
c1_instrument=absent
c1_total=absent
c1_families_with_interval_verdict=absent
c1_exit=absent
c2_state_check_first_line=assertions=235 match=231 mismatch=0 superseded=1 offline_unverifiable=3
c2_p3_mismatch_count=absent
c2_exit=0
q13_instrument=absent
q13_round25_8ea41f9_exit=absent
q13_round26_lesson=absent
q13_round26_lesson_exit=absent
sources_rows=42
sources_malformed=0
sources_tier_histogram=A=38 B=2 C=2
sources_status_histogram=mined=30 queued=9 rejected=3
knowledge_files=33
knowledge_readme_index_rows=33
knowledge_readme_unindexed_files=none
knowledge_readme_dangling_rows=none
knowledge_readme_duplicate_rows=none
knowledge_readme_parity=match
```

## Risks, blockers, installs
- At this base, `grader_perturb.py` and `gate_timing_check.py` are absent, the round-26 lesson is absent, and `state_check.py` contains no P3 assertions. Their counts are deliberately `absent`, not zero; this base census does not establish later instrument results.
- No blocker to this scoped implementation. No tools installed or updated.

VERDICT: Round-26 base census implemented and run; source counts and knowledge/README parity are recorded above, while not-yet-landed instrument outputs remain absent.
