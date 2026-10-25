ATTACKS: C2 calibration move — plans/state_check.py, claimed base mismatch=11 → tip mismatch=0; superseded=1. Method: `git archive 6180e4f`/`8ea41f9ed` → /tmp/k25w2-CritC2Fresh/{base,tip}; ran tip instrument on both roots plus 6 mutations on copies.

REPRODUCE (survives): `python3 tip/plans/state_check.py --root base --summary` → `assertions=242 match=228 mismatch=11 superseded=0`, byte-identical assertion set to committed receipt `corpus/evidence/round25-calibration/state-check-before-6180e4f.txt`. `--root tip` → `mismatch=0 superseded=1`, exit 0; `--selftest` exit 0. All 11 base mismatches re-verified as real drift (dead paths re-checked on host: `~/Projects/webzites/repos/llm-wiki`, `~/archive/bench-arena`, `/proc/1299/cmdline`, `~/.bailian/*` all absent).

WHAT IT IS: bookkeeping-grade calibration, not a scored probe — honestly framed (claims file:92-93, SCORECARD:668 "score held"). Closures are documentation-of-drift: PROVINCE rows got ABSENT markers (paths still dead), SHONEN prose → bare pointers (contract-mandated: PROTOCOL.md:432 "one indented evidence line … resolvable pointer; no other prose"), README row added for pre-existing unindexed lesson. Legitimate self-assessment-vs-repo-state (AXES.md:15 fit), but "11→0" is inflated: 4 of 11 are SHONEN pointer-only violations of a rule this same instrument newly enforces — found-and-fixed by its own definition.

LAUNDERING — confirmed three paths:
- L1 SUPERSEDED (state_check.py:390-423): correction tokens are re-checked only against CURRENT observed census; no baseline. Mutation M1 (m1/): deleted `| S010 |` from corpus/SOURCES.md, appended `R25-E6 … supersedes P2a.capability.sources-registry — now `rows 25`` → `SUPERSEDED`, mismatch=0, exit 0. Any registry regression is re-blessed by restating the drifted tokens; cherry-pick one token (observed `A=23 C=2; mined=17` silently re-documented). SUPERSEDED never distinguishes stale-claim from regressed-world.
- L2 out-of-population row→file hole (state_check.py:1027-1038): rows not in frozen README_INDEX_PATHS are tagged OUT_OF_POPULATION and never checked. Mutation M4 (m4/): deleted corpus/lessons/round-24-verifier-spotcheck.md (indexed at tip) → dangling row, mismatch=0, exit 0. Every row C2 itself added is permanently unchecked in the file direction.
- L3 axis value cells never re-derived (state_check.py:529-531): only `Basis` spans are resolved; the `Round-24 value` column is unread. Mutation M3 (m3/): `| novelty | 7 |` → `| 9 |` → mismatch=0, exit 0. The "re-derived" score table cannot catch score inflation.
- L4 prose supersessions unchecked: R25-E2..E5 (tip SCORECARD:647-650) supersede free-form text, never match SUPERSEDE_RE (needs backticked id), so no assertion verifies them.

DETECTION still works where aimed: M4b deleted base-indexed knowledge/attrib-r21.md → MISMATCH exit 1; M5 ABSENT on existing grader.py → MISMATCH; M6 registry regression with stale R25-E1 → MISMATCH (`correction_missing` surfaces it).

Smallest safe corrections: (a) require correction tokens to cover every census field, or pin expected-observed at correction-append time; (b) row→file check for out-of-population rows; (c) emit an explicit UNCHECKED assertion per axis value cell and per prose supersession so they are visible, not silent.
Impacted axis: calibration — the move is real but thin; L1 is a judge-relevant laundering channel if SUPERSEDED is cited as evidence of closed drift.

VERDICT: PARTIAL — instrument re-derives honestly and base/tip numbers reproduce, but SUPERSEDED launders arbitrary registry regressions (M1), its own new index rows are uncheckable (M4), and score cells are unverified (M3).
Installs: none (python3 3.14 stdlib only).
