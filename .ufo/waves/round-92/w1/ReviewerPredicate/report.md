# ReviewerPredicate — R92 predicate audit (claims text vs instrument code)

Seat: ReviewerPredicate (leaf). Audit is read-only line-by-line between the frozen claims at
A `96f249e05a88c8a81a49a380c72e0c6bfec82480` (`plans/round-92-claims.md`,
`plans/round92-cases.json` sha256 `2249d5c0…a693`, verified byte-identical at A and B2) and
the instrument bytes at B2 `f0018773f507f363854123856990f8ff8a87eb8c`
(sha256: c1_replay `ebce59…5f1`, c2_conformance `4aa6e3…648`, burndown `c8a2c5…806`,
f2_counter `c14fe1…7ea`, bs_probe `13e41e…f82`). The lane has moved past B2 (C `42bd5104`,
registry fix, D `b62ea270`, E..E7 conformance/battery repairs, F `288511d8`): every
post-B2 instrument change is named with its commit. Findings are F-numbered; each cites
file:line, the claims sentence, the code condition, and the SAME/DIFFERENT verdict.

## Placeholders used below

- `claims(a)` = `plans/round-92-claims.md`, commit A.
- Instruments: `C1R` = `plans/round92_c1_replay.py` @B2, `C2C` =
  `plans/round92_c2_conformance.py` @B2, `G3` = `plans/round92_burndown.py` @B2,
  `F2C` = `plans/round92_f2_counter.py` @B2, `P91` = `plans/round91_counter_pin.py` @B2,
  `C91R` = `plans/round91_c1_replay.py` @B and @BASE.
- Line numbers refer to the B2 blobs (E7/HEAD line numbers differ; both given where useful).

---

## Findings (severity ordering: HIGH, MEDIUM, LOW, INFO)

### F-1 (HIGH) — R92-C2 claims: M7's frozen green leg is unsatisfiable at any rev carrying the r92 ledger, and the conformance counter itself grew a rewind-control that changed its semantics after B2

- **Claims sentence** (claims(a) R92-C2, M7 leg): "at REV=T the amended counter bytes exit 0
  with `PREDICATE R91-C1 pass` on the SAME receipt bytes (the ten `ok=True` CASE lines are the
  red-then-green witness; no receipt byte changes)."
- **Code condition at B2** (`c2_conformance.py:104-108`): the green leg runs the tip's r91
  counter bytes against the *measured lane* (`--lane lane.root --rev tip`). The r91 counter
  carries frozen `EXECUTED_AFTER = 35` and r91 class cells (`round91_c1_replay.py@B2`, lines
  36, 38) and asserts them in L7 (`l7` conjunction, line ~216). Against the tip lane (ledger
  36 executed, r92 cells 4/27/4/5) the green leg *cannot* pass; L7 fails and rc is 1. The
  committed receipt `c2-c3-tip.txt` at `d1ccf56d` documents exactly this:
  `M7-CASE-PARSER FAIL base-rc=1 base-L5=10 tip-rc=1 tip-pass=False`.
- **What happened next**: the repair E `6a51ff0e` rewrote the green leg into a scratch clone
  whose ledger is rewound to the r91 population (HEAD `c2_conformance.py:104-130`), with a
  follow-up red-leg restore loss fixed in E3 `801b8157`. The green leg now semantics: tip
  counter bytes vs a *rewound fixture lane*, not vs the measured lane.
- **Verdict: DIFFERENT** at the frozen A sentence vs the B2 code. The claims' T-leg condition
  ("exit 0 … on the SAME receipt bytes" against the measured rev) has no implementing
  condition in the frozen instrument; the instrument's green leg has a different (fixture)
  target. This is a disclosed mispredict (lesson M1–M7, E commits) under the re-freeze route,
  reported here so the residual is explicit: **the frozen text and the shipped counter now
  disagree on what M7's green leg measures**, and the residual is disclosed, not closed.
- Cross-check: the claims' own M7 discipline does hold for the *receipt bytes* (red leg runs
  the committed `corpus/evidence/round91/modernize-probe.txt` unchanged in both legs,
  `RECEIPT` constant `c2_conformance.py:31`; the L5 parse of it is positional at tip bytes,
  `(cid, pred, obs)` tokens[0] at `c1_replay.py` B2 `parse_receipt` lines 76–96). No receipt
  byte changed (E3 restored the dropped red leg). Only the *lane target* of the green leg
  moved.

### F-2 (HIGH) — R92-C3 claims: the frozen BASE legend ("freeze=refused oldest_pending_round=82 pending=1" from "the same gate") is contradicted by the v3 gate at BASE, and the frozen text contradicts itself

- **Claims sentence** (claims(a) R92-C3, frozen predicate): "At BASE `4ba56182`: the same gate
  prints `freeze=refused oldest_pending_round=82 pending=1` with the three
  `override-unjustified` DEFECTs (the one-level resolver names the R90 rows as deciding), rc 1."
- **Code condition at B2** (`burndown.py@B2` lines 214–263): the v3 gate's supersede resolver
  is already chain-aware (`chain_end()` walk, `chain_next`), so at BASE the R90/R91 supersede
  chain of the r82 pending row resolves and `pending` becomes 0. The committed receipt
  `c3-base.txt` (E7-era bytes, same resolver) shows it: `freeze=refused oldest_pending_round=-
  pending=0 … their only DEFECT check-failed R82-V8 rc=1 'CHECK v8 fail'` — a *different*
  refusal cause than the claims sentence. I reproduced the refusal shape with the B2 bytes
  against a BASE clone (scratch run, timed out only on the M8 battery bug below, see F-3; the
  CHECK lines confirm `override-rc=0` for the three R42 rows, i.e. no
  `override-unjustified` emission under the v3 anchor rules).
- **Internal contradiction**: the *same* frozen claims sentence in the do-nothing-control
  paragraph says: "— decisive — the pre-audit showing the CHAIN-AWARE state at BASE already
  resolves `pending` to 0". So the frozen text asserts at BASE both `pending=1` (predicate
  leg) and `pending=0` (control paragraph). The `pending=1 … override-unjustified` triple is
  the **v2 gate** behavior (committed pre-freeze witness `base-batteries.txt`, third battery:
  `PREDICATE R91-C3 fail`, `oldest_pending_round=82 pending=1`, three
  `override-unjustified`), not the v3 gate. The v2-at-tip witness `v2-at-tip.txt` shows the
  same v2 shape at the tip. The claims' BASE legend conflates the two gates.
- **Verdict: DIFFERENT** — the claims sentence names a code condition (v3 gate at BASE
  printing `oldest_pending_round=82 pending=1` + three override-unjustified) that the frozen
  instrument cannot satisfy, and the frozen text itself carries the contradicting pre-audit
  sentence. Nothing was repaired; the mispredict is named here.

### F-3 (HIGH) — R92-C3 claims M8: the B2 gate's child-proof whitelists `--selftest` in the parent argv, but the selftest's own children are spawned without `--selftest` — guaranteed recursive battery (hang), empirically reproduced

- **Claims sentence** (claims(a) R92-C3 (d) M8): "the gate's selftest runs inside the default
  predicate path and any red case fails the PREDICATE."
- **Code condition at B2** (`burndown.py@B2:565`, `in_child_mode`): returns True only if
  `/proc/<ppid>/cmdline` contains `"round92_burndown.py" in raw and "--selftest" in raw`. But
  the selftest's `gate()` runs each case child with
  `cmd = [python, burndown, --lane, --rev, --work] (+ --freeze-round)` — no `--selftest`
  flag (`burndown.py@B2:~447-455`; at HEAD the list is the same before E5). Therefore every
  battery child's `in_child_mode` is False, each child runs the battery again, recursing
  without bound.
- **Empirical evidence (mine)**: running the B2 gate at BASE in a `--shared` scratch clone
  (v1) hung in the in-path battery and was killed at the 300 s tool deadline; the fixture dir
  contained 20+ nested `predicate-selftest/chain-two-level-run` generations. The committed
  receipt `c2-c3-tip.txt` shows the same hang live at the tip: `TimeoutExpired` after 600 s
  for `…/predicate-selftest/chain-two-level-run … --freeze-round 92`.
- **What happened next**: E5 `a0c7438a` relaxed the check to "any live-gate parent"
  (`"round92_burndown.py" in raw`, HEAD `burndown.py` line ~566), making children skip the
  battery. The M8 claim invariant (battery in the default predicate path, no off switch)
  *holds at B2 and after*; the failed part is the child-proof, i.e., an M7-class instrument
  defect caught and repaired post-freeze (disclosed). Reported as a frozen-code live defect;
  residually the *frozen* M8 sentence and the code are the SAME condition, the defect was in
  the recursion guard, not in the in-path run.

### F-4 (MEDIUM) — R92-C2 claims M9: the frozen green literal `PINS checked=17 matched=17` matched B2 bytes but not the measured tip; the conformance counter's green condition was reworded post-freeze (E2)

- **Claims sentence** (claims(a) R92-C2, M9): "the amended checker's default run at T prints
  `PINS checked=17 matched=17 mismatched=0` and `SELFTEST cases=9 red-green-ok=9`, rc 0."
- **Code condition at B2** (`c2_conformance.py@B2:171`): green requires the literal substring
  `PINS checked=17 matched=17` in the amended checker's stdout. At B2 the pin ledger has 17
  entries (verified: `counter-pins-r91.json` @B2 = 17 entries), so the condition is the same
  as the claims *at B2*.
- **Divergence after freeze**: commit D `b62ea270` grew the ledger to 18 entries (adding the
  bs_probe pin, revealed by the C1 counter's own L8 leg, receipt `c1-tip.txt`: `DEFECT L8
  probe pin unreadable … 13e41e…`). The frozen instrument's green literal then fails against
  any tip carrying D; E2 `1d5634e3` reworded the condition to an all-pins-matched regex
  (`PINS checked=(\d+) matched=\1 mismatched=0`), with an initial escaping bug fixed in E4
  `5b6c00b8` (receipt `c2-tip-final.txt` shows the E2-era crash, `c2-tip-final2.txt` a
  mangled M9 FAIL at 801b8157, `c2-tip-final3.txt` the green E4 result).
- **Verdict: DIFFERENT** at the measured tip vs the frozen sentence, SAME at B2. The frozen
  sentence's value literal (17) encodes a count that the round's later work moves; the
  predicate text freezes a transient value — reported so the residual is explicit (this is
  the same family as the L0 in-tree-pin residual: pin count literals rotate with any ledger
  growth).

### F-5 (MEDIUM) — R92-C2 claims M9: the frozen text ("the checker bytes contain no `--skip-selftest`") is false at B2 (docstring/comment mentions), true only after E; and the frozen BASE-leg receipt (R92-C2 fail rc 1 with all three checks red) has no committed witness

- **Claims sentence** (claims(a) R92-C2, M9): "at REV=T the checker bytes contain no
  `--skip-selftest`"; predicate leg: "At BASE `4ba56182`: `PREDICATE R92-C2 fail`, exit 1,
  with all three checks red."
- **Code condition at B2**: the B2 `round91_counter_pin.py` no longer *exposes* the flag
  (argparse has no `--skip-selftest` at @B2 line ~355-370), but the bytes still *contain* the
  literal in the usage docstring (line 16) and a comment (line 211). The conformance check
  `tip-flag-absent` tests `"--skip-selftest" not in tip_c2_text` (`c2_conformance.py@B2:178`),
  so at B2 the M9 flag leg is red on its own instrument bytes. Committed receipts trace the
  error and the fix: `c2-c3-tip.txt` at `d1ccf56d` shows `tip-flag-absent=False`;
  `c2-tip-final2.txt` at `801b8157` (post-E `6a51ff0e` docstring cleanup
  "stale docstring flag mentions cleaned") shows `tip-flag-absent=True`.
- **BASE-leg receipt**: no committed receipt anywhere in the wave shows
  `PREDICATE R92-C2 fail rc 1` with `M7-CASE-PARSER FAIL / M12-HOST-PROBE-GUARD FAIL /
  M9-SELFTEST-ESCAPE FAIL` at BASE. The committed `base-batteries.txt` (at A) shows the r91
  C2 checker green at BASE (the claims' do-nothing control), not the R92-C2 conformance
  counter. I verified by code reading (`c2_conformance.py@B2` verdicts: with `rev==base`,
  `tip-flag-absent` False and `green_closed` False and M7 green rc≠0 → all three red, rc 1)
  that the code would produce the frozen legend, but the *committed witness for the frozen
  BASE leg of R92-C2 does not exist*. All other claims-named receipts are committed
  (c1-base, c1-tip, c1-tip-d, c2-* , c3-base, c3-tip, f2-base, f2-tip, v2-at-tip,
  base-batteries — file inventory at HEAD checked).
- **Verdict: DIFFERENT** (half). The flag-existence sentence and BASE legend have no B2-byte
  implementation at B2 (repaired post-freeze) and the BASE leg lacks its committed receipt.
  The *intent* (no predicate-path skip switch) is implemented at B2; the *bytes* criterion is
  the part that was off.

### F-6 (MEDIUM) — R92-C3 claims kill rule: "a named conflict, not a silent pass: the gate stops and the report carries it" has no distinct implementing condition in the gate

- **Claims sentence** (claims(a) R92-C3, kill rule, last sentence): "A check that breaks
  because a round-92 registry edit changed a counted surface is a named conflict, not a
  silent pass: the gate stops and the report carries it."
- **Code condition** (`burndown.py@B2`, `evaluate()`): a failing check emits
  `DEFECT check-failed <sid> rc=…` and `check_failed=True`, forcing freeze=refused. There is
  no separate "conflict" classification, no distinguishable output, and nothing in the gate
  detects "a round-92 registry edit changed a counted surface" as a category; every
  check-failure is uniformly just a defect. The refusal-and-name is implemented (the DEFECT
  line names the row, the gate refuses); the "named conflict" distinction is not — any
  conflict is indistinguishable from any other red check.
- **Verdict: PARTIAL** — the stop-and-name half is implemented
  (`check-failed` defect + refused); the *conflict-specific* half has no condition.

### F-7 (LOW) — R92-F2 claims: "prints the before/after `ANCHORLINE` lines" — the counter prints only the after line; the "before" value appears only in its docstring

- **Claims sentence** (claims(a) companion F2): "`plans/round92_f2_counter.py` (successor of
  `round91_f1_counter.py`) prints the before/after `ANCHORLINE` lines and
  `WRONG-LINE-CAUGHT True` at the tip, rc 0; at BASE it prints no `CAPTURE-PINNED` lines, rc 1."
- **Code condition** (`f2_counter.py@B2`): one `ANCHORLINE` line is printed (line 78: the
  checker run at the current rev); the before value (captured=71) exists only in the
  docstring (line 13). The BASE leg exists as a separate invocation on a BASE clone —
  committed `f2-base.txt` shows the after-only `ANCHORLINE captured=71` from a BASE-registry
  run, `CAPTURE-PINNED` printed with an empty value list, three `DEFECT PARSE-MISSING` rows,
  rc 1.
- Additional literal: claims "at BASE it prints no `CAPTURE-PINNED` lines" — the code always
  prints the `CAPTURE-PINNED` line, with no entries (f2_counter.py:73). The committed
  receipt has the header line with empty values. Same underlying condition (no pins at
  BASE), different literal.
- **Verdict: DIFFERENT (literal level)** for both halves; the substantive predicate
  (tip: three pins + captured ≥ 74 + live=0 + wrong-line caught, rc 0; base: rc 1) is
  implemented and green/red as claimed (`f2-tip.txt`: `CAPTURE-PINNED S287=1,S288=1,S289=1`,
  `captured=78 live=0`, `WRONG-LINE-CAUGHT True`, `PREDICATE R92-F2 pass` rc 0).

### F-8 (LOW) — R92-C3 claims: the frozen predicate string `SELFTEST cases=M red-green-ok=M` is not the gate's printed literal (`SELFTEST-DETAIL cases=M red-green-ok=M`), and the gate emits an extra `PREDICATE R92-C3-BATTERY` line the claims don't predict

- **Claims sentence** (claims(a) R92-C3 predicate): "…`SELFTEST cases=M red-green-ok=M` in
  the same invocation, and `PREDICATE R92-C3 pass`, exit 0."
- **Code condition** (`burndown.py@B2`): the battery summary the gate prints is
  `SELFTEST-DETAIL cases=%d red-green-ok=%d` (selftest(), line ~486 in the B2 blob as
  `Battery detail` print); the case children each print `SELFTEST <name> rc=…`; and main()
  adds `PREDICATE R92-C3-BATTERY pass|fail` in addition to `PREDICATE R92-C3`.
  Committed receipt `c3-tip.txt` shows both prints.
- **Verdict: DIFFERENT only in literal** — `SELFTEST cases=` (the claims' literal) would not
  byte-match the gate's summary line; the counts and battery-in-path meaning are the same.
  The extra `-BATTERY` line is counter behavior the claims do not predict (harmless but
  unnamed). Note the r91 checker's own line `SELFTEST cases=9 red-green-ok=9` is a *different*
  instrument (`P91`, used by the C2 counter) where the claims' literal does hold.

### F-9 (LOW) — R92-C1 claims "guarded host probes": one of the L9 host probes is unguarded code that re-runs an already-guarded probe; the guard holds only because it cannot fail in practice

- **Claims sentence** (claims(a) R92-C1, item list): "…(each asserted by the counter's L7 leg
  from the committed ledger bytes)… guarded host probes" (also the C91R docstring claims the
  M12 discipline).
- **Code condition** (`c1_replay.py@B2`, L9 block, lines ~266-276): `py_now_line` is first
  computed with `guarded_run([sys.executable, "-V"])`, then *immediately overwritten* by an
  unguarded `_py = subprocess.run([sys.executable, "-V"], …)` whose `.strip().splitlines()[0]`
  would raise IndexError on empty output. OpenSSL and userns probes are guarded
  (`guarded_run(["openssl", "version"])`, `/proc` read in try/except). Python itself cannot
  be absent while the counter is running, so no live crash path exists.
- **Verdict: PARTIAL** — the claims' guard invariant holds by impossibility, not by code;
  the dead guarded computation is misleading. Behavior-informative only; no observed defect.

### F-10 (INFO) — R92-C1 claims vs code: all leg and TARGET conditions verified SAME (detail list)

Verified the same condition at file:line (B2 blob line numbers):

1. "TARGET … executed=1 cases=10 legs=60 mismatches=0 defects=0" ↔ `c1_replay.py:285-291`
   (`legs = len(receipt cases) × len(table leg_order)` = 10×6; table `leg_order` has 6
   entries, verified in the A case table). RECEIPT `c1-tip-d.txt` matches.
2. "executed_rows=36" ↔ constant `EXECUTED_AFTER=36` (`c1_replay.py:37`) + printed value
   `EXECUTED_AFTER if exec_total==36 else exec_total` (line 286) so 36 is forced by L7
   (`l7` line 236). Ledger at official tip: 36 executed members; class cells 4/27/4/5 match
   the claims' denominators/counts (10 filesystem, 12 crypto, 10 serialization, 76
   file-artifact) — computed from `grader-population-ledger.json` @C.
3. "member … located=1" ↔ `located = 1 if cap_bytes present` (line 284); at BASE located=0,
   receipt `c1-base.txt` ✓ (BASE legend rc 1 ✓).
4. "each asserted by … L7" ✓ lines 228-241; "committed ledger bytes" ✓ L7 reads rev-blob only.
5. Nine legs L1–L9 all rev-controlled reads of the measured revision ✓.
6. Predictions: receipt has 10 CASE lines ok=True mismatches=0 (`corpus/evidence/round92/
   bs-probe.txt` @C) ✓; case table frozen sha ≡ A ≡ B2 (computed) ✓; the shipped-probe
   TOOL_SHA drift (db02… → 13e4…) is inside the claims' own allowance "may differ only by the
   stamp/paths" — the committed probe differs *only* in stamp-neutral bytes; the pin was
   added later in D (see F-4 note; at A the probe was unpinned and L8 then had to fail — the
   receipt `c1-tip.txt` documents that red-before faithfully).
7. SOURCES rows S283/S284/S285/S286(marked rejected) all present at C with capture shas
   (S283 sha 80b06b7c… = SUBJECT_SHA; the input shas are pinned inside the grader itself at
   capture lines 27/30, matching the claims' S285 description) ✓.
8. "row land with commit C; the lesson's `## Gate` carries URL, access date…" — rows at C ✓;
   the Gate quote/date fields were verified by the scribe seat wave receipts; my scope did
   not re-fetch URLs (no network in this audit), so the located-quote half is reported as
   not independently re-verified here (noted residual, not a finding).

### F-11 (INFO) — R92-C2 claims vs code: M12, M9-table, M7-red and BASE legs verified SAME (detail list)

1. M7 red: ten `DEFECT L5 receipt names unknown case ?` and rc 1 on the committed
   `corpus/evidence/round91/modernize-probe.txt` — BASE counter bytes do parse `id` from
   `key=value` tokens (`round91_c1_replay.py` @BASE:69-88: `cases.append((parts.get("id","?")…`))
   and the receipt carries it positionally ✓; frozen-green at BASE impossible ✓; the B2-era
   pre-E red leg (`c2-c3-tip.txt` line 1) and restored E3 red leg (`c2-tip-final*.txt`) ✓.
2. M12: BASE bytes call `openssl` with no try/except (`round91_c1_replay.py` @BASE line ~243)
   → unguarded die rc 1, no PREDICATE line in stdout (traceback on stderr) ✓; tip bytes
   guard with `guarded_run` + fail-closed `CouldNotEvaluate("host probe absent …")`
   (`round91_c1_replay.py` @B2:242-263) → `DEFECT SETUP` + `PREDICATE R91-C1
   could-not-evaluate` rc 2 ✓; conformance driver uses a masked PATH without openssl but
   with git/python/etc (`c2_conformance.py:70-79` `masked_bin`) ✓ and asserts red-unguarded
   (rc 1, no predicate) + green-closed (rc 2, DEFECT SETUP, exact predicate line)
   (`c2_conformance.py:130-140`) ✓. Committed receipts show both ✓ (`c2-tip-final3.txt`,
   `c2-tip-final2.txt`).
3. M9 table: expectations table exists at T (sha 4453495a… pinned as an entry — verified the
   B2 ledger entry equals the B2 table bytes by sha256) ✓; BASE table absent (blob None) ✓;
   case 9 `expectations-tampered` reds with `DEFECT SETUP expectations-pin mismatch` rc 2
   (`P91` @B2:280-300) ✓; `SELFTEST cases=9 red-green-ok=9` ✓ (`P91` @B2:158).
   The `PINS checked=` literal family: see F-4.
4. R92-C2 BASE legend (all three red, rc 1): implementable per code reading (each green-side
   conjunct individually false when rev==base) but no committed receipt — see F-5.

### F-12 (INFO) — R92-C3 claims vs code: M10, M11, M13, M6, M14 verified SAME (detail list), plus the R42 override anchor verification I recomputed

1. M10 vacuous: `vacuous_check` = fullmatch `true|:|exit 0|/bin/true` OR (no path token AND
   no file operator) (`burndown.py@B2:144-149`) — claims wording matches exactly ✓.
2. M10 override anchoring: deciding-row check tokens must intersect
   close|source|base-check tokens (`burndown.py@B2:305-311`). I recomputed the anchor logic
   over the tip ledger with the real R42-R2/R3-33/R3-37 chain ends (R90/R91 partner rows):
   each override's tokens (plans/scratch_guard.py, SKILL.md, feal_probe.py, …) all appear in
   the partner row's close+source+base-check evidence — `missing=[]` for all three, so the
   three `override-unjustified` v2 defects are *cleared by M10's own rule* at the tip, exactly
   as the claims' "any rows the new M10 rules require" clause anticipates. (My earlier
   definition-literal test with a paraphrased close string produced `missing=['SKILL.md']`;
   with the actual committed close strings the anchors hold — the SKILL.md token is carried by
   the R42-R2-R90 close "R42-R2.2 SKILL.md:640 registry row".) Verdict: SAME.
3. M10 owner: `unowned_blocked` from deciding-row owner ∉ lane_ids(shokunin.conf)
   (`burndown.py@B2:269-285, 347-355`) + `owner-not-a-lane` defect ✓ selftest cases 6-8 ✓.
4. M11: checks run with cwd = fresh detached worktree at the measured revision under
   `--work` (`git worktree add --detach`, removed in finally) ✓ same condition.
5. M13: chain-aware resolver by `chain_end` over `supersedes` links, effective state from the
   chain-end row ✓ (`burndown.py@B2:214-283`); selftest case 1 `chain-two-level` proves the
   two-level chain grays-free — but its asserted text is only `pending=0`+rc0 (the chain-end
   status is not spelled in any stdout line): the claims' "proves … the chain-end status" is
   proven *implicationally* (a one-level-closed supersede would pass the identical
   assertion), so the named differentiating observable is weaker than the wording. Noted,
   not a defect claim (case 2 chain-open-tail refuses, so the chain rule is exercised both
   directions).
6. M6: R82-V8 in `round83_c2_checks.py`: `explicit=R83_FLEET_REPO or SHOKUNIN_ROOT`,
   `fleet=explicit if explicit else origin.parent` (`round83_c2_checks.py` @A→B2 diff lines
   167-171) — the claims' "reads SHOKUNIN_ROOT (or R83_FLEET_REPO) first, origin.parent
   fallback" — note precedence: code prefers `R83_FLEET_REPO` over `SHOKUNIN_ROOT`; the
   claims put SHOKUNIN_ROOT first in the sentence with R83_FLEET_REPO in parentheses. Both
   env vars are "first" in the sense of before the fallback; the ordering *between the two*
   envs (FLEET_REPO > SHOKUNIN_ROOT in code) is unspecified by the claims. No live conflict
   (the gate exports SHOKUNIN_ROOT; no caller in the round sets R83_FLEET_REPO). Info-only.
   The gate's own fleet-root default is `SHOKUNIN_ROOT or lane.root.parent`
   (`burndown.py@B2:277`), and E7 `dd48027f` additionally exports SHOKUNIN_ROOT to child
   checks so R82-V8's `git show` resolves the fleet repo rather than the scratch worktree
   parent (receipt `c3-base.txt` shows the red-before: `DEFECT check-failed R82-V8 rc=1
   'CHECK v8 fail'`; `c3-tip.txt` shows `check-failed` gone).
7. M14 correction row: present at C (`R84-V9-R91-R92`, status closed, supersedes
   R84-V9-R91, disposition correction, append-only ✓), its check `grep -q 'R84-V9-R91'
   corpus/routed-findings.jsonl` is non-vacuous and anchored ✓.

## Verification gaps and residual risk

- **One BASE-leg frozen legend lacks any committed witness** (R92-C2 all-red rc 1 at BASE —
  inference from code only, no receipt exists anywhere in the wave; R92-C3's v3-at-BASE legend
  is contradicted by the only committed v3-at-BASE receipt). For R92-C1, R92-F2 and all v2-gate
  controls the committed receipts exist and match.
- My audit did not re-run the C1/C2/F2 counters end-to-end at the tip (the measured tips are
  recorded in LOG.md and the committed receipts carry the outputs); the only counter I ran was
  the B2 gate at BASE (to test F-2/F-3 empirically), which timed out at the battery recursion
  after completing all check lines but before its summary lines.
- The M8 recursion at B2 and its E5 repair mean the *frozen instrument bytes* and the *ships*
  gate differ; any future replay of the frozen bytes at a tip will hang unless E5 (or a
  successor patch) is carried. Same pattern for F-1 (M7 green leg), F-4 (PINS literal), F-5
  (skip-selftest bytes): the B2 bytes are the frozen baseline, the HEAD bytes are the shipped
  bytes; the residual is the disclosed gap in between (in-tree-pin residual family), not closed
  by this round by design (L0).
- The L9 unguarded python probe (F-9) is dead-code-only risk today; if the harness repeated it
  for a non-self binary the unguarded re-run pattern is a crash risk.

## Bound adherence

No subagents, no task, no commit/push/mutating git/jj in the lane (only `git show`, `rev-parse`,
`ls-tree`, `diff`, `log`, `merge-base` style read-onlys against the lane and one `git clone
--shared` + B2-blob checkouts + a fixture git repo inside my scratch, with `rev-parse
--show-toplevel` asserted). One fixture git worktree-add by the gate ran inside my scratch clone
only. No host sysctls touched; no tools installed; no pacman use. Scratch dir to be removed at
yield; receipts cited here live in the lane at `.ufo/waves/round-92/L1/*` (committed at F
`288511d8`) or `corpus/evidence/round92/*`; my scratch-only intermediates (extracted blobs,
`findings_tip.jsonl`, `ledger_tip.json`) are not citable evidence and are discarded with the
scratch.
