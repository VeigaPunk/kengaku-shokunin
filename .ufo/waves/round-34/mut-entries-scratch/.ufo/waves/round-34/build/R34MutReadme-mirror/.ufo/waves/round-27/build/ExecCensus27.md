# ExecCensus27 — Round 27 census

Axes: novelty (C1 extraction-policy observability); calibration (C2 state assertions).

## Implementation

- Private clone based at `11a7fc8c64dc5d634331be24ccf5936f84a11f03` (the registered `11a7fc8c64dc` base).
- Wrote `plans/round27_census.sh` in the private clone only. It is a no-argument, read-only lane-root census; missing C1/oracle/C2/Q13 evidence is rendered `absent`. See `plans/round27_census.sh:6-19,31-39,41-108,110-160`.
- C1 prints summary TOTAL, its disagreement count, each exit, and the independent oracle exit (`:41-63`). C2 preserves the first summary line and counts P4 IDs and their MISMATCH verdicts from `--json` (`:65-88`). Q13 is checked against round-27 lesson at `refs/heads/master` when present (`:90-96`).
- SOURCES counts use the four frozen CORPUS.md census commands; knowledge/README parity is bidirectional (`:98-160`).
- Clone file SHA-256: `3a537e8d5177bde7c809b68240a54b6155b5efdb346a99c65f048fdc2571cb7c` (`plans/round27_census.sh`).

## Lane run (read-only)

Command: `sh /tmp/kengaku-r27-ExecCensus27/plans/round27_census.sh` from `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; exit 0.

```text
head=11a7fc8
c1_instrument=absent
c1_total=absent
c1_disagreements=absent
c1_exit=absent
c1_oracle_exit=absent
c2_state_check_first_line=assertions=278 match=270 mismatch=0 superseded=5 offline_unverifiable=3
c2_p4_assertions=0
c2_p4_mismatch=0
c2_exit=0
q13_round27_lesson_exit=absent
sources_rows=48
sources_malformed=0
sources_tier_histogram=A=43 B=3 C=2
sources_status_histogram=mined=36 queued=9 rejected=3
knowledge_files=34
knowledge_readme_index_rows=34
knowledge_readme_unindexed_files=none
knowledge_readme_dangling_rows=none
knowledge_readme_duplicate_rows=none
knowledge_readme_parity=match
exit=0
```

At this run C1 and the round-27 lesson are absent; the existing state checker has zero P4 IDs and zero P4 mismatches. It exits 0. SOURCES reports 48 rows, zero malformed, and knowledge index parity matches.

Installs: none.

VERDICT: Implemented the round-27 census in the private clone and captured the requested clean base-lane census (exit 0); no C1 instrument or C2 P4 assertions are present yet.
