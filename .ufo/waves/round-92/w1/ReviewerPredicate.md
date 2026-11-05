# ReviewerPredicate — seat findings (round-92 w1)

Full line-by-line audit: `.ufo/waves/round-92/w1/ReviewerPredicate/report.md` (this dir). All
findings F-numbered there; condensed here. Audit is claims-at-A `96f249e05` vs instruments-at-B2
`f0018773`, read-only; verified bytes (sha256) and receipts; no edits to code or claims.

- **F-1 (HIGH)** R92-C2 M7: frozen green leg ("tip counter bytes exit 0 with `PREDICATE R91-C1
  pass` on the SAME receipt bytes" at REV=T) has no implementing condition in the frozen
  instrument — the B2 conformance counter runs the green leg against the measured lane, whose
  ledger (36 executed) cannot pass the r91 counter's frozen `EXECUTED_AFTER=35` constants
  (`c2_conformance.py@B2:104-108` vs `round91_c1_replay.py@B2:36-38`); receipt `c2-c3-tip.txt`
  shows the red `M7-CASE-PARSER FAIL tip-rc=1`. Post-freeze E `6a51ff0e` (+E3 red-leg restore
  `801b8157`) re-targets the green leg to a scratch clone with a rewound ledger (HEAD
  `c2_conformance.py:104-130`). Frozen text and shipped counter now measure different things;
  disclosed mispredict, residual open.
- **F-2 (HIGH)** R92-C3 BASE legend contradiction: frozen predicate says "At BASE the same
  [v3] gate prints `freeze=refused oldest_pending_round=82 pending=1` with the three
  `override-unjustified` DEFECTs (one-level resolver)"; the B2/HEAD v3 gate is already
  chain-aware, its only committed BASE receipt (`c3-base.txt`) shows `pending=0
  oldest_pending_round=-` with sole defect `check-failed R82-V8`. The `pending=1` triple is
  the **v2** gate (`base-batteries.txt`, `v2-at-tip.txt`). The same frozen text's
  do-nothing-control paragraph even states the chain-aware BASE already resolves pending to 0
  — the claims contradict themselves.
- **F-3 (HIGH)** M8 B2 live defect: `in_child_mode` (`burndown.py@B2:565`) requires
  `--selftest` in the parent's argv, but the selftest spawns case children *without*
  `--selftest` → unbounded battery recursion; reproduced empirically (B2 gate at BASE hung
  past the 300 s kill with 20+ nested `chain-two-level-run` generations) and committed
  (`c2-c3-tip.txt` 600 s `TimeoutExpired`). E5 `a0c7438a` repairs it ("any live-gate parent").
  M8's in-path/no-off-switch invariant itself holds — the defect is in the child-proof.
- **F-4 (MEDIUM)** M9 frozen literal `PINS checked=17 matched=17` (B2 = 17 entries, matches)
  breaks once commit D grows the ledger to 18 (bs_probe pin); E2 `1d5634e3` rewords the
  conformance green condition to all-pins-matched (regex escaping fixed at E4). A transient
  count is frozen inside the predicate text.
- **F-5 (MEDIUM)** M9 "checker bytes contain no `--skip-selftest`" — false at B2 (the flag's
  argparse is gone but the literal survives in the docstring/comment, `P91@B2:16,211`), red on
  its own test (`tip-flag-absent=False`, receipt `c2-c3-tip.txt`), true only after the E
  docstring cleanup. Separately, the frozen R92-C2 BASE leg ("all three checks red, rc 1")
  has **no committed receipt anywhere** — I verified implementability only by code reading.
- **F-6 (MEDIUM)** R92-C3 kill rule "a named conflict, not a silent pass" — no distinct
  implementing condition; every check failure is a uniform `DEFECT check-failed` + refused;
  nothing classifies "round-92 registry edit changed a counted surface" specifically.
- **F-7 (LOW)** F2 claims "prints the before/after `ANCHORLINE` lines" — code prints only the
  after line (`f2_counter.py@B2:77-78`); the "before" (captured=71) exists only in its
  docstring. And "at BASE prints no `CAPTURE-PINNED` lines" — the line is printed with empty
  values (committed `f2-base.txt`). Same underlying conditions; different literals.
- **F-8 (LOW)** R92-C3 predicate literal `SELFTEST cases=M red-green-ok=M` — the gate prints
  `SELFTEST-DETAIL cases=… red-green-ok=…` plus an extra `PREDICATE R92-C3-BATTERY pass`
  line the claims do not predict (`c3-tip.txt`). The literal `SELFTEST cases=9 …` in the C2
  claims does match the r91 checker.
- **F-9 (LOW)** R92-C1 "guarded host probes" — in the C1 L9 block, `py_now_line` is computed
  with `guarded_run` and then immediately overwritten by an unguarded re-run of the same
  probe (`c1_replay.py@B2` L9 block); no live crash path (the counter itself is python), so
  the guard holds by impossibility, not by code.
- **F-10/F-11/F-12 (INFO)** — SAME-condition verifications (all C1 TARGET values, class cells
  4/27/4/5 with denominators 10/12/10/76 computed from the committed ledger; L1–L9; M7 red
  ten-L5; M12 both legs rc 1/2; M9 table-pin sha 445349…≡bytes; M10 vacuous/anchor/owner with
  my recomputed anchors over the three R42 override chains (`missing=[]` — the v2
  override-unjustified triple is cleared by M10's rule exactly as the claims anticipate);
  M11 worktree cwd; M13 chain resolver (selftest case asserts only `pending=0`, weaker than
  the "chain-end status" wording); M6 `R83_FLEET_REPO` > `SHOKUNIN_ROOT` > `origin.parent`
  precedence (claims don't fix the env-vs-env order); M14 correction row present at C; S283–
  S286 rows with capture shas, S286 marked rejected).
- **Residual**: disclosure gap between frozen B2 bytes and shipped HEAD bytes on F-1/F-4/F-5
  (M-family re-freeze route; the in-tree-pin residual stays open per L0). No committed witness
  for the R92-C2 BASE triple-red leg. C1 S283–S285 quote/word-count fields are in W-seat scope,
  not re-verified here.
- **Bounds**: no subagents/task/commits/pushes; no lane or fleet-root writes except my seat
  report paths; one read-only `git clone --shared` + scratch fixture with
  `--show-toplevel` asserted; no sysctls; no tool installs (channel: none used; pacman paused).
  Scratch removed after copying cites into the lane; /tmp never used for citable evidence.
