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

## Frontier

One source admitted (S278); one new member executed (33 of 88 ledger members). The thinnest executed classes at BASE were
`shell-exec` (1 of 6) and `stdout-inspection` (8 of 29); after the round they read 2 of 6 and 9 of 29.

## Routed to round 90

Routed-findings burn-down (considerthese item 1) remains open. The round-88 KNOWN-check hole is closed by Q66 v2 only for the
four named fixtures; record-level drift in the claims file outside the pinned table is caught by F7, not by a semantic check.
