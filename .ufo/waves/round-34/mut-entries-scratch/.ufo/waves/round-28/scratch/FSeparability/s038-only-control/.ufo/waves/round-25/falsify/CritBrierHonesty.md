ATTACKS: round-25 P1–P5 scoring honesty — outcomes, Brier arithmetic, P2 89.6% share, "only non-derivable" claim, "no calibration credit".

F1 — Brier arithmetic exact. Recomputed from plans/round-25-claims.md:52-56
  (p=0.95/0.55/0.90/0.97/0.10) with o=(1,1,1,1,0): rows 0.0025/0.2025/0.0100/0.0009/0.0100,
  mean 0.2259/5 = 0.0452, P2 share 0.2025/0.2259 = 89.6%, other-four mean 0.0059.
  Every number on SCORECARD.md:671-673 reproduces. SURVIVES.

F2 — P2 outcome=1 is defensible ONLY under the literal frozen key; the gloss is falsified.
  Predicate "(dedup fires)" fired (attrib-calibration-summary.txt:49
  `dup=[...legs.log:312-362=...opencode-trials.log:204-254]`), and the rule at
  round-25-claims.md:31-32 defines same-sample = identical (ids, predictions, GT, chains).
  But the English content "same sample" is false on the lane's own evidence:
  DupR22Scout.md:25-39 — identical 20-row table (sha256 54c7888c… both), yet disjoint
  request windows (11:50:40–11:52:42Z vs 11:53:36–11:55:37Z), different freeze pins
  (3d7861f8 vs 77b8d4a0), different LOO (18/20 vs 19/20), 0 cross-file feature-id
  duplicates → two distinct executions scored as one sample. Amendment 1 item 4
  (round-25-claims.md:~128-132) concedes this and keeps the dedup anyway. Scoring P2 YES
  rewards a dedup the lane itself proved wrong; semantic scoring (o2=0) gives Brier
  0.3025, mean 0.0652, P2 share 92.8% — both published figures then misstate reality.

F3 — "P2 — the only forecast not derivable from committed bytes at filing" is FALSE.
  attrib-r22-legs.log and attrib-r22-opencode-trials.log were committed at 8a08483
  (round 22); pre-registration landed at 3f371d2. Their 20-row scored tables were
  byte-identical at base 6180e4f: `git show 6180e4f:...legs.log | sed -n 319,339p` and
  `...opencode...| sed -n 211,231p` → sha256 91158095… equal. Dedup-firing was fully
  determined by committed bytes + the frozen key filed in the same document.
  Amendment 1 item 7 ("P2 is the only genuine forecast") repeats the error. All five
  predictions were derivable; there were zero genuine forecasts this round.

F4 — P1/P3/P4/P5 outcome flags check against instrument output (summary:32 P1
  target:hyper PASS>INDETERMINATE; :3,13,25,38 four n≥17 accuracy blocks all PASS; :14,16…
  per-leg INDETERMINATEs present; :49 incorrect=0 → P5=0). Transition counts
  FAIL>UNTESTED:2 PASS>INDETERMINATE:1 PASS>PASS:4 = 7/7 re-verdicted match :49.

F5 — "No calibration credit is taken" survives and is load-bearing: under F3 the
  honest statement is stronger — no genuine forecast existed at all, so the 0.0452
  mean must not be cited as forecast skill in any later round or rubric leg.

Impacted axis: calibration (falsified narrative legs F2-gloss + F3-derivability;
arithmetic and outcome flags survive). Smallest correction: relabel P2 outcome
"1 under the frozen literal key / 0 under the lane's own distinct-execution
evidence", restate P2 as derivable-at-filing, keep the no-credit disclaimer.

VERDICT: PARTIAL — Brier math, per-row outcomes, and 89.6% reproduce exactly; the P2
"same sample" gloss and the "only non-derivable forecast" claim are both falsified by
committed bytes and the lane's own scout. Installs: none (python3 stdlib + git read-only).
