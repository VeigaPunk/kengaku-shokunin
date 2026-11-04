# ReviewerC2R76 — scoped C2 review

Axes: coverage (all five assigned attacks); calibration (observed verdicts, exact bytes, explicit limitations). Recommendations only; no admission or production changes.

## Findings, severity first

1. **HIGH — REJECT item 4: a future empty closure erases the entire burn-down universe.** `plans/round76_c2_defect_discharge.py:134-157,381-400` chooses the highest filename round without validating a nonempty scope. Fixture `fix/e4/corpus/lessons/round-77-verifier-spotcheck.md` contains exactly `# Round 77 — draft\n\nNo routed defects named yet.\n`. In the current-byte replay its ledger is an existing zero-byte file: there are **no registered rows at all**. Printed verbatim (rc 0):

   ```text
   SCOPE-SOURCE corpus/lessons/round-77-verifier-spotcheck.md
   SCOPE ids=0 registered=0 closed=0 open=0 discharged=0 legs_passed=7 legs_pending=0 wrong=0
   PREDICATE R76-C2 pass
   ```

   `discharged != len(ids)` cannot reject `0 == 0`. Smallest repair: fail closed on empty IDs; for this R75-specific gate, pin/validate the required R75-D1…D7 scope so a future file cannot replace it. Add future-empty and future-unrelated-ID selftest arms without changing the frozen target.

2. **HIGH — REJECT item 5: deleting the only closure also passes with zero rows.** Same pointers. `fix/e5` has no `round-*-verifier-spotcheck.md`; the ledger is again an existing zero-byte file. Current-byte replay, rc 0:

   ```text
   SCOPE-SOURCE 
   SCOPE ids=0 registered=0 closed=0 open=0 discharged=0 legs_passed=7 legs_pending=0 wrong=0
   PREDICATE R76-C2 pass
   ```

   Smallest repair: reject a missing scope source/empty universe before evaluating success. This is the same root cause as finding 1, independently exercised. Removing only round-75 from the full production tree could instead fall back to an older closure; this result is specifically the assigned isolated fixture.

3. **HIGH — REJECT item 2: leg inputs are raw bytes; invisible HTML comments satisfy correction legs.** `plans/round76_c2_defect_discharge.py:255-315` reads QUALITY/SCORECARD/LOG/SKILL/round-74 lesson without `visible()`. That helper is used only for README derivation at lines 178-198. Exact fixture SCORECARD bytes:

   ```html
   <!-- - R75-D2 correction: stamp fda63968f29f8f58dc2b28831acac879405b8326 and report tip 5d9a0ccc. -->
   <!-- - R75-D3 correction: the final-rule before is 60 (4/36/20). -->
   ```

   QUALITY and LOG correction text is also HTML-commented; SKILL registry rows and the lesson correction are inside triple-backtick fences. The complete bytes are preserved in `ReviewerC2R76/fix/e2/`. Current-byte replay uses valid evidence-at-close fields copied from the real R75 rows (so A5's new evidence binding is not bypassed or omitted). Printed rc 0:

   ```text
   LEG D2 ok SCORECARD line with R75-D2, stamp fda63968f29f, 5d9a0ccc
   LEG D3 ok SCORECARD line with R75-D3, total 60, split 4/36/20 at 43255758
   SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
   PREDICATE R76-C2 pass
   ```

   Smallest repair: apply the existing `visible()` policy to the Markdown leg inputs, at minimum stripping HTML comments. Scratch candidate `gate_visible.py` does this for six inputs: on E2 it prints six `LEG-FAIL` lines (D1–D5,D7), rc 1; on the actual lane it retains `PREDICATE R76-C2 pass`, rc 0. This candidate was tested against the earlier snapshot, not integrated. Code fences are visible code rather than invisible comments; the unambiguous hidden-content counterexample is D2/D3's HTML comments. A5 checks committed evidence literals raw too; it does not repair this worktree-leg issue.

4. **MEDIUM — pass can mean two required derivations never ran.** `plans/round76_c2_defect_discharge.py:255-315,383-400` adds a defect only for FAIL, not PENDING. Calling the current canonical `emit` against `master` in revision mode prints, rc 0:

   ```text
   LEG D4 PENDING needs the two round-75 selftests (rev mode)
   LEG D5 PENDING needs the selftest counts (rev mode)
   SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=5 legs_pending=2 wrong=0
   PREDICATE R76-C2 pass
   ```

   The frozen landing target requires `legs_passed=7 legs_pending=0`. Retain PENDING as an honest descriptive state for historical receipts, but do not print full predicate pass when execution-dependent legs are incomplete. Missing worktree selftest output enters the same PENDING branch; that failure mode was inspected, not injected. Smallest repair: make pending legs prevent success, or give historical declaration-only checks a separate non-success verdict.

5. **LOW — REJECT item 1 as a semantic check: a meaningless literal passes CHECK-TRIVIAL.** `plans/round76_c2_defect_discharge.py:172-174,344-345` only searches for path-shaped text and a quoted literal of length >=3; it neither verifies that the check's named path is committed nor executes that check. Current replay replaces **all seven** checks with exactly `grep -q 'the' SCORECARD.md` while retaining their valid A5 evidence fields. Printed rc 0:

   ```text
   LEDGER R75-D1 ok closed close_commit=6977019bdf56
   SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
   PREDICATE R76-C2 pass
   ```

   This is a limitation of the syntactic rule, not proof that all independent discharge legs failed: the frozen claim explicitly defines triviality by path + literal, and the real evidence/legs still carry the proof. Smallest meaningful tightening: bind the check literal/path to that row's declared evidence tuple or a re-derived value, rather than arbitrary words. Merely executing grep or requiring longer words cannot establish relevance. Requiring the row ID alone would also require changing existing D4/D6 check strings, which currently cite values instead of their IDs.

6. **INFO — ACCEPT item 3: side-branch close is classified correctly.** A disposable initialized repo explicitly using branch `master` has a side commit diverging from the master's first commit. R75-D1 points at side; other rows point at master. The corrected fixture prints:

   ```text
   E3 branches: on=master first=3e874cccce39 master=0d268595bb29 side=cbf879b8834f
   LEDGER R75-D1 DEFECT CLOSE-NOT-ANCESTOR
   DEFECT CLOSE-NOT-ANCESTOR R75-D1
   PREDICATE R76-C2 fail
   ```

   The underlying receipt records the gate's fail. The wrapper's final `rc=0` was the filtering pipeline's status, **not the gate's exit status**; do not read it as a pass. This fixture used the earlier snapshot; current source lines 339-343 retain the same explicit mapping of ancestry state `not-ancestor` to `CLOSE-NOT-ANCESTOR`. No repair needed. The first fixture attempt used the host-default branch instead of explicitly creating master and failed to switch back; its CLOSE-UNRESOLVED output is a fixture error, not a gate defect.

## Commands and evidence

Let `L=/home/vgpnk/Projects/shokunin/kengaku-shokunin`, `S=/fast/scratch/hyaku/kengaku-r76/ReviewerC2R76`. Artifacts named below are preserved under `.ufo/waves/round-76/w1/ReviewerC2R76/`; scratch-path strings in scripts describe their original execution locations.

- Read the complete frozen claims before commands; read `skill://godspeed`. Later requested `xd://lsp`: **no such mounted tool**. Semantic references/definition/diagnostics were therefore unavailable; source inspection is literal fallback, not semantic proof.
- `git -C "$L" diff fda63968f29f8f58dc2b28831acac879405b8326 -- plans/round76_c2_defect_discharge.py` — rc 0, new 687-line gate; source sections inspected through read/grep.
- From `$L`: `python3 plans/round76_c2_defect_discharge.py --lane . --receipt "$S/work/canonical.txt"` — rc 0; baseline `ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0`. Receipt preserves tip/worktree stamp; the live tree changed during review.
- `python3 -m py_compile "$S/gate_fixture.py" "$S/gate_visible.py"` — rc 0, `COMPILE-OK`.
- `python3 "$S/driver_fixtures.py"` — process rc 0. Individual experiment gate return codes: E1=0, E2=0, E2b=1, E2c=0, E4=0, E5=0, E6=1. E6 at `6977019b...` correctly failed because ledger rows/receipts were not yet committed; superseded for pending-leg evidence by current revision replay.
- `bash "$S/e3_notancestor.sh"` — corrected wrapper rc 0; gate receipt says fail, with correct CLOSE-NOT-ANCESTOR. Git fixtures created using mktemp/init and explicit `-C`, toplevel assertion before first commit; no lane commits created. Temporary fixture removed by EXIT trap.
- `python3 "$S/current_replay.py"` — process rc 0; current canonical module `emit(..., probe=L, work=S/'work/current')` return codes: E1=0, E2=0, E4=0, E5=0, revision master=0. This is the decisive replay, using canonical functions without changing their source. Current-byte fixtures use real R75 evidence bindings; E4/E5 deliberately have no ledger rows. Receipts: `receipts/current-e1.txt`, `current-e2.txt`, `current-e4.txt`, `current-e5.txt`, `current-rev.txt`.
- Canonical batteries, each from `$L`, each rc 0:
  - `python3 plans/round76_c2_defect_discharge.py --selftest --work "$S/work"` → `SELFTEST cases=11 red=10 failures=0 ok=True`.
  - `python3 plans/round76_c2_defect_discharge.py --mutants --work "$S/work"` → `MUTANTS total=9 killed=9 expected_matched=9 wrong_id=0 survived=0`.
  - `python3 plans/round76_c2_defect_discharge.py --control-status --work "$S/work"` → `CONTROL rows_claimed_closed=7 trivial_checks=1 failed_legs=3`; `PREDICATE R76-C2-control pass`.
  - `python3 plans/round76_c2_defect_discharge.py --selftest-git --work "$S/work"` → `SELFTEST-GIT cases=3 failures=0 ok=True`.
- `git -C "$L" merge-base --is-ancestor fda63968f29f8f58dc2b28831acac879405b8326 master` and the equivalent for freeze `42fad482...` — both rc 0.
- `sha256sum "$L/plans/round76_c2_defect_discharge.py" "$S/gate_orig.py"` — rc 0. Initial snapshot `48241a7230356f9100dcee747aae1cebcba66b1583bf130996dde629fa70e9c7`; decisive current replay `d6615bd299856d9a0fc257f2a32eaf4c2de1238bde0e821a63f45f6f78dc1cd8`. Latest observed master `7f2cd3b979700f3f24391c720a3ec2a6d40b47e4`.

## Residual risk / verification gaps

- Production advanced during review. A2 documents the `--work` repair, A5 documents evidence-at-close and 11/10 selftests plus 9/9 mutants. Consequently the initially suspected undocumented battery drift / ignored CLI work flag are **withdrawn**, not findings. Four assigned attacks were replayed on the newer canonical functions after reading these changes.
- The visible-input repair is a scratch candidate only. No production edits, integration, shipping, runtime switch, or admission performed. No actual concurrency collision was reproduced; no saturation claim is made. Resume continuity/rerouting are outside this assigned Python gate.
- The current gate adds committed evidence checks, so older synthetic rows without evidence fields would now fail; the decisive replay deliberately retains valid real evidence fields and still demonstrates the reported holes.
- No tools installed or updated. System Python and Git only. The initial canonical CLI/battery internals used the gate's then-shared scratch defaults; current decisive replay explicitly supplies this seat's own work directory.
- Self-evaluation: accuracy 4 (versioned receipts and current replay; Q3 exercised older bytes with unchanged current mapping), completeness 4 (all five attacks covered; no concurrent-failure injection), clarity 4 (severity ordered, historical caveats explicit), actionability 4 (smallest repairs named, not integrated), conciseness 3 (evidence/version caveats add length). Overall 3.8/5. Most useful improvement: replay the proposed scope/rendering repairs through the L1's full battery; user should regard the findings as recommendations backed by scoped probes, not an admission decision.
