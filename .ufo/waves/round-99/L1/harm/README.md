# Round 99 L1 harm battery (KengakuR99)

`run_harm.sh` (copied from round 98, BASE swapped to 2233a661) over BASE and the integration tip `fc65aa9a`:
`summary-fc65aa9a.txt`. Every rc unchanged. Finding deltas only:
- anchor-digest 45 -> 33 (the 12 R99-C2 rows cleared);
- r82c3 sweep 30 -> 31: `STATUS-LINE-MISSING bn-fit-modify` plus the histogram counters 42->43 / 33->34
  (the per-member frozen-declaration delta every new member produces; r97 27->28, r98 29->30). Gate red at BASE.

Separately:
- `anchor-line-T.txt`: at T (f72a8bc7) `plans/anchor_line_check.py` was live=5 rc 1 (typed word counts, lesson M3);
  `anchor-line-corrected.txt`: live=0 rc 0 after the dated correction `b71b990a` (also green at fc65aa9a above).
- `r98-c2-at-T.txt`: round-98 C2 counter at round-99 T: PREDICATE R98-C2 pass (K4 reads only BIND lines of its
  39 rows; the new files do not touch them). GATE base=86 rev=33.
- `r98-c1-at-T.txt`: round-98 C1 counter at round-99 T: L7 fail, `set_added=['bn-fit-modify','regex-chess']`.
  By construction: the round-98 predicate requires the executed set to EQUAL round-98 BASE + regex-chess, so
  every later member flips it at later revisions. `r98-c1-at-own-T.txt`: the same counter at its recorded
  revision 8e37fc65 still passes (rc 0); its SCORECARD counting command names that revision. Routed as a
  design note on revision-scoped set-equality legs, not a harm by this round.

Correction after the wave (ExecHarm, `.ufo/waves/round-99/w1/ExecHarm.md:30`):
- `plans/round82_c1_plans_registry.py` defaults `--tip` to `rev-parse master`, so in this battery's clones both
  "BASE" and "fc65aa9a" logs read the clone's `master` (= the lane tip at clone time): the r82c1 rows above
  are NOT revision-scoped and their 17 = 17 comparison is void (the same runner was used in round 98).
- Revision-scoped re-run with `--tip REV` (`r82c1-tip-<rev8>.txt`): BASE 13 DEFECT, T f72a8bc7 17 DEFECT
  (+4 `ROW-SELFTEST-UNBACKED` for the four round99 registry rows, whose selftest cell said `none — no
  self-invocation mode` instead of the gate's literal `none declared`), 3fdecf31 13 DEFECT, DEFECT set equal
  to BASE after the dated correction `3fdecf31` (lesson M5). Gate red at BASE throughout (MISSING scripts).
