# Kengaku round 89 — a seventh executed Terminal-Bench 2.0 member (polyglot-rust-c), and the Q66 counter-side check hardened on its round-88 attack findings

Round 89 (hyaku run 15, attempt 1), 2026-11-05. L1 `KengakuR89`. Lane `kengaku-shokunin`, branch `master`.
Freeze (claims and case table): commit `d1c4f1b04bb39d18967075974b5984238b7c97f7` (`plans/round-89-claims.md`,
`plans/round89-cases.json`), frozen before any instrument. Base `192e809d582ecbd544798cbc03da1666a0de23f7`.
Instruments: `0e6bb05f3a6c2d9a96bb26db31a4fd39f58c2619` (probe, C1 counter, Q66 v2, pinned record table, probe receipt).
Measured tip: the commit that lands the tip fixes, ledger flip and this lesson (named in the round report).

Two claims on two distinct surfaces:

- `R89-C1` coverage (lowest non-retired axis, held at its L0 cap 7): a seventh located offline replay, `polyglot-rust-c`,
  by `plans/round89_c1_replay.py` (nine legs, `TRUSTED_TOOL_SHA` pin on the probe). It moves `shell-exec` 1 of 6 → 2 of 6,
  `stdout-inspection` 8 of 29 → 9 of 29, `subprocess-exec` 10 of 45 → 11 of 45.
- `R89-C2` calibration (held at ceiling 10): `plans/round89_claim_figures.py` (Q66 v2) — the four round-88 attack findings
  (KNOWN check ignores the claimed value; deleted before-figures pass; record counts not gated; selftest outside the
  predicate path) answered by a pinned record table and four control fixtures.

## Gate

### Source admitted (S278)

The L1 opened the source below on 2026-11-05 (`curl`, HTTP 200, 1638 bytes) and compared its sha256 with the round-52
capture (`baed5e4d0cc0e5809ff41a7df1815d18c65c708a3a3f264428e1cda11ce692f9` on both; `sha256sum` identical).

| id and decision | URL | access date | located quote (≤25 words) | reason / flip |
|---|---|---|---|---|
| S278 admit, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-rust-c/tests/test_outputs.py | 2026-11-05 | `assert polyglot_files == ["main.rs"], (` at line 19 | the listing assertion is the first graded refusal; compiles at :24-25 are silent (`os.popen(...).read()`); the five sizes at :27-44 run under `check=True`, so a non-zero binary exit surfaces as `CalledProcessError` (verdict E). Scope is member replay only. |

Quarantine: no shokuknow register slice this round (`.ufo/waves/round-89/assimilation` not created; assimilation none).

### Census

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` before the round: exit 0, `kengaku ok`,
269 rows (measured 2026-11-05). After: 270 rows, S278 `mined`, A 239 → 240, mined 244 → 245, rejected 17, queued 8.
Round-end exit 0 is measured in the report.

### considerthese

`considerthese/2026-10-26.md` item 1 (routed-findings burn-down, with a freeze refusal) is the named candidate; it is mined
here and not implemented (the round's two claims are the four round-88 findings it does not cover). Recorded for round 90.
Items 2 and 3 are not taken this round.

Assimilation: none — `merge/kengaku/` remains blocked by L0 `kengaku | round-54`.

## Claims and their measurements

Measured figures are filled by the report; the counting commands are in `plans/round-89-claims.md`.

- **R89-C1 (coverage).** BASE `192e809d` (measured 2026-11-05): `TARGET executed_rows=32 member=polyglot-rust-c located=0 executed=0 cases=0 legs=0 mismatches=0 defects=4`, `PREDICATE R89-C1 fail`, exit 1 (defects L1-receipt, L4-table, L7-ledger, L9-tool). Instrument commit `0e6bb05f`: `defects=1` (L7-ledger only: the ledger row was not yet flipped), `located=1 executed=0`. Predicted tip: `defects=0`, `PREDICATE R89-C1 pass`.
- **R89-C2 (calibration, ceiling).** Instrument commit `0e6bb05f`: `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1`, `DEFECTS n=0`, `PREDICATE R89-C2 pass`, exit 0; controls (after the fixes under Mistakes 1–2): doctored-claimed red (`F7-record-missing`), deleted-figure red (`F7-record-missing`, 7 defects), doctored-key red, selftest-in-path red (`F8-selftest`), tip green, `PREDICATE R89-C2-CONTROLS pass red=4 of 4 tip=green`.

## Mistakes

1. **Class `vacuous` (the control fixture was not a control).** Evidence: the first `--controls` run printed
   `CONTROL deleted-figure green rc=0 defects=0 first=none` for a fixture that was byte-identical to the BASE claims.
   The `_drop_before` marker looked for `**Before` while the R85-C1 line reads `Before (BASE \`0de45354\`): \`TARGET …\``.
   Captured-by: none (no check verified that a control's fixture differs from its source). Fix: the marker matches
   `Before (BASE`, and `controls()` refuses a fixture equal to the git bytes (`CONTROL <name> vacuous`) and makes the
   predicate fail on one. Able-to-fail: the rerun prints `CONTROL deleted-figure red rc=1 defects=7 first=F7-record-missing ('R85-C1', 'kv', 'cases', '=', 0)`.
2. **Class `vacuous`-adjacent instrument bug (control write path).** Evidence: first controls run stopped with
   `FileNotFoundError: …/c2-ctl/deleted-figure/q66-selftest-…` (the per-control work directory was not created before the
   selftest). Captured-by: none. Fix: `run_check` creates its work directory before the selftest; the rerun reached all five controls.
3. **Class `landing` (probe stdout pollution, instrument-side).** Evidence: the first probe run exited 2 with
   `DEFECT SETUP sandbox-protocol`, because the grader's own `print(polyglot_files)` writes to stdout inside the sandbox and
   corrupts the JSON protocol. Captured-by: none (the round-88 probe had no such print). Fix: the harness redirects the
   test's stdout and frames its verdict as a single `PAYLOAD ` line; the rerun gave `cases=8 legs=8 mismatches=0`.
   The first attempt also corrupted `round89_polyglot_probe.py` with a wrong-range edit; it was rewritten in full before commit B.
4. **Disclosure — the instrument moved after commit A.** The C1 and C2 counters and the probe were written after the claims
   freeze (`d1c4f1b0`) and committed at `0e6bb05f`; Mistakes 1–2 fixes landed after that commit and before the tip.
   These are the instruments' bytes, not the claims text: no frozen predicate, target, case table or KNOWN set changed.

## Attempt 2 — re-measurement at tip `00462b59` (KengakuR89a2, 2026-11-05)

Attempt 1 (`KengakuR89`) ended without a report after dispatching wave `w1`. Attempt 2 re-runs both counters at the current tip
and does not re-declare any claim. Frozen files are byte-identical to the freeze commit `d1c4f1b0`
(`git diff --stat d1c4f1b0 master -- plans/round-89-claims.md plans/round89-cases.json` prints nothing).

- **R89-C1, re-measured at tip `00462b59`: verified on its frozen predicate.** `plans/round89_c1_replay.py --rev 00462b59…` →
  `TARGET executed_rows=33 member=polyglot-rust-c located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0`, `PREDICATE R89-C1 pass`, exit 0.
  The first attempt-2 run (earlier in the same session) failed at L6 (`DEFECT L6-reproduce probe re-run rc=2 produced no observation block`) because the host read `max_user_namespaces` = 0 and bwrap could not create a namespace (ENOSPC). The host later read `122865` and bwrap ran (rc 0); the re-run above is on that host state. Attempt 1's PASS was measured while ExecProbeR89 had raised the sysctl for one window (`.ufo/waves/round-89/w1/ExecProbeR89/report.md`).
  Forgery limit (SentinelR89 `forge-f1`, scratch commits `3a04bfa9` → `25188f73`, not in the lane): a commit that rewrites the counter's own `TRUSTED_TOOL_SHA` together with an echo probe passes C1 with rc 0. L9 checks the probe against a pin that the measured revision carries itself. The lane tip is not such a commit (the counter bytes at `00462b59` equal the instrument commit `0e6bb05f`), so the verdict stands for the tip; a third party must check the counter bytes against the instrument commit.
- **R89-C2, re-measured: pass at tip.** `plans/round89_claim_figures.py --rev 00462b59…` →
  `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0`, `DEFECTS n=0`, `PREDICATE R89-C2 pass`, exit 0.
  `--controls` → `CONTROL doctored-claimed red`, `CONTROL deleted-figure red`, `CONTROL doctored-key red`, `CONTROL selftest-in-path red`,
  `CONTROL tip green`, `PREDICATE R89-C2-CONTROLS pass red=4 of 4 tip=green`, exit 0.
  Do-nothing control (round-88 counter on the same attack fixtures, ExecCtrlC2 `round88-baseline.txt`): doctored-claimed `pass`, deleted-figure `pass`, doctored-key `fail`.

## Mistakes (attempt 2)

5. **Class `environment` (receipt depends on a host sysctl).** Evidence: the first attempt-2 run found `/proc/sys/user/max_user_namespaces` = `0`; `bwrap --ro-bind / / --dev /dev --proc /proc true` failed with ENOSPC; the L6 leg reported `DEFECT L6-reproduce probe re-run rc=2 produced no observation block` and `PREDICATE R89-C1 fail`, rc 1. The same host later read `122865`, bwrap ran, and the counter passed at the tip (rc 0). Captured-by: L6-reproduce (it reported the failure and did not pass a stale receipt). Fix: none in the lane; the frozen probe and predicate are not repaired. The receipt stamp does not record the host sysctl, so a transient change leaves no trace in committed bytes; recording it is a round-90 candidate.
6. **Class `figure-not-measured` (after-figure side).** Evidence: `.ufo/waves/round-89/w1/ReviewerR89b/report.md` Finding 1 — the
   R85-C2 Target after-figure `ids=8` → `ids=9` leaves `RECORDS … mismatches=1`, `DEFECTS n=0`, `PREDICATE R89-C2 pass`, exit 0.
   Captured-by: none (the record table pins before-figures only, `claim_spans` reads `Before (BASE` / `at BASE` spans). Fix: not made this round
   (frozen predicate and record table); routed to round 90 as a counter-side extension with a fail-before control.
7. **Class `spec-error` (wave item anchor).** Evidence: `ReviewerR89b` report, "Spec anomaly" — the item asks for the digit `4` in
   `ids=8`; `grep -n "ids=" plans/round-*-claims.md` finds no such anchor. Captured-by: none. Fix: none in the frozen spec; disclosed.
8. **Class `process-contamination` (blindness).** Evidence: `ReviewerR89a/agreement.md` "Process disclosure" — the frozen `predicted`
   values were visible before the seat's derivation. The seat restaged a blind copy and re-derived; the 8/8 agreement is reported with that
   caveat. Captured-by: none. Fix: routed to the wave-context template (blind staging copy before any read of the case table).
9. **Class `self-pinned instrument` (a commit can rewrite the pins it is checked against).** Evidence: SentinelR89 H1–H3 (`.ufo/waves/round-89/w1/SentinelR89/report.md` §2; transcripts `forge-c2-ii-regen-table.txt`, `forge-known-kv-counter-edit.txt`, `forge-f1-echo-same-commit-pin.txt`). Scratch-only forged commits in the sentinel's clone (not in the lane): a regenerated record table passes after a deleted before-figure (`PREDICATE R89-C2 pass`); a doctored claim with a KNOWN edit and a regenerated table passes; an echo probe with `TRUSTED_TOOL_SHA` rewritten in the same counter commit passes C1 (`PREDICATE R89-C1 pass`, rc 0). ExecCtrlC1 control 5b shows L9 is the only defence against the echo probe. Captured-by: none (L9 checks the probe against a pin the measured revision carries; C2 pins nothing). The lane tip is not such a commit: the counter bytes at `00462b59` equal instrument commit `0e6bb05f` (`git diff --stat 0e6bb05f master -- plans/round89_c1_replay.py` prints nothing). Fix: none this round (frozen instruments). Routed to round 90: pin counter, probe and record table to the freeze commit by ancestry and blob sha, checked by a leg that a same-commit rewrite cannot satisfy.
10. **Class `frozen-text` (a frozen claim sentence the instrument does not implement).** Evidence: CriticR89 F1 (`plans/round-89-claims.md:14`, C2 change (d): "pinned to its blob sha at the freeze commit"; the table is absent at `d1c4f1b0` and first committed at `0e6bb05f`, and the counter has no sha pin), F3 (`plans/round-89-claims.md:44`: control `selftest-removed-from-path` is implemented as `selftest-in-path`), F5/F6 (C1 predicate sentence and C2 controls clause diverge from the counter's printed line). Captured-by: none (the claim was frozen with text the counter was not checked against). Fix: none; frozen text is reported, not repaired. The verdict on C2 is taken on its predicate; the operator rules whether the unimplemented element (d) admits the claim (see the report).
11. **Disclosure gap, now corrected.** CriticR89 F2: the committed record did not say that the C1 probe re-runs happened in a transient user-namespace window. Attempt-2 Mistake 5 above and the C1 bullet add that disclosure; the attempt-1 SCORECARD/LOG entries do not, and this is named in the report as an open correction.

## Frontier

One source admitted (S278); one new member executed (33 of 88 ledger members). The thinnest executed classes at BASE were
`shell-exec` (1 of 6) and `stdout-inspection` (8 of 29); after the round they read 2 of 6 and 9 of 29.

## Routed to round 90

Routed-findings burn-down (considerthese item 1) remains open. The round-88 KNOWN-check hole is closed by Q66 v2 only for the
four named fixtures; record-level drift in the claims file outside the pinned table is caught by F7, not by a semantic check.

Attempt-2 routing (wave `w1` attack findings, not repaired in round 89):

- Pin the counters, the probe and the record table to the freeze commit by ancestry and blob sha (Mistake 9; SentinelR89 H1–H3).
- C2 counter: check after-figures as well as before-figures (ReviewerR89b F6: `ids=8` → `ids=9` at `plans/round-85-claims.md:106` is green).
- Mutants that survive the tip predicate: C1 M1–M5, M7 (leg-disabling; only fixtures kill them, and M2/M5 have no real-harness fixture); C2 N1 (label-only KNOWN text), N4 (vacuity guard prints only), N6 (`work.mkdir` removal gives a traceback, not a verdict). `.ufo/waves/round-89/w1/MutTesterR89/mutants.md`.
- Frozen text corrections, reported not repaired: Mistake 10 (CriticR89 F1/F3/F5/F6, and the control name).
- Sentinel L1–L6 (hostile case path stall 120 s and uncaught crash; empty or `"."` paths; control "red" means rc≠0; literal `claims=17`; prior counters run from the working tree, not BASE blobs; `/proc` stdout reach, fail-closed).
- Record the host `user.max_user_namespaces` value in the probe receipt (Mistake 5).
- Scout candidate set for round 90 (24 unexecuted members with captured grader bytes at the tip): `.ufo/waves/round-89/w1/ScoutR89/next.md`.
