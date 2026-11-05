## Round 91 (hyaku run 15, attempt 1, 2026-11-05): a ninth executed member whose frozen replay fails at the tip on a counter defect; the checker pinned to itself with the selftest in the predicate path (met); the routed-findings freeze gate v2 refuses at the tip with no triage landed (not met)

Base `59764383d4dd33d58faa50daad4c06d0cde410aa`; claims and case table freeze `cd0c116ef8c453d076031bdf5888b1e1b83bb0be` (commit A); instruments and pin ledger `386184a6085ed01bbfbf73a4dc694a02fc3a01d5` (commit B); checker correction and pin regeneration `b836a862f5b9ba9cecbcff457003f1eabee70fba` (commit B2); receipt, ledger flip, S281/S282 and lesson `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0` (measured tip). No triage row is in the measured tip (`corpus/routed-findings.jsonl` blob `830c0daeb9b42fc094e05ea1c64c8cb5f5d94529` at both BASE and tip). Three claims on three surfaces.

| claim / axis | before → after at the measured tip | counting command | verdict / score |
|---|---|---|---|
| R91-C1 / **coverage** (held at its L0 cap 7): a ninth located offline replay, `modernize-scientific-stack` | BASE `59764383`: `TARGET executed_rows=34 member=modernize-scientific-stack located=1 executed=0 cases=0 legs=0 mismatches=0 defects=9`, `PREDICATE R91-C1 fail`, rc 1 (nine DEFECT lines, L1–L9). At `a8de3e69`: `TARGET executed_rows=35 member=modernize-scientific-stack located=1 executed=0 cases=10 legs=20 mismatches=10 defects=10`, `PREDICATE R91-C1 fail`, rc 1; all ten DEFECT lines are `L5 receipt names unknown case ?` (counter parser, `plans/round91_c1_replay.py:86`; the probe's receipt shows ten of ten `ok=True`). Ledger executed 34 → 35 of 88 (recorded): file-artifact 25 → 26 of 76; filesystem-metadata 2 → 3 of 10; numeric-band 3 → 4 of 10; stdout-inspection 10 → 11 of 29; subprocess-exec 12 → 13 of 45. | `python3 plans/round91_c1_replay.py --lane . --rev REV --work DIR` | **not met on its frozen predicate.** The `executed=` gate printed 0 under a failing leg, as frozen. Coverage held at 7 (cap); the ledger count moved but the claim did not pass. |
| R91-C2 / **calibration** (held at ceiling 10): the pin set extended to the checker itself, the selftest in the predicate path, fail-closed absence | BASE `59764383`: `DEFECT SETUP unreadable plans/counter-pins-r91.json`, `PREDICATE R91-C2 could-not-evaluate`, rc 2 (as predicted). At `a8de3e69`: sixteen `PIN-OK` lines, `PINS checked=16 matched=16 mismatched=0`, `SELFTEST cases=8 red-green-ok=8`, `PREDICATE R91-C2 pass`, rc 0. Selftest measured 4 of 8 at B before the B2 correction (pre-correction, disclosed). | `python3 plans/round91_counter_pin.py --lane . --rev REV --work DIR` | **met on the conjunction its frozen predicate states.** Held at ceiling 10; a count at the ceiling is recorded, not added. Caveats: `git diff --stat 386184a6 a8de3e69` over the pinned set prints two files (B2's edits), so the frozen tip rule fails literally; the kill rule's "any edit after commit B" clause is read against the disclosed B2 correction, for the operator's ruling. |
| R91-C3 / **operability** (held at ceiling 10) + capability `routed-findings freeze gate v2` | BASE `59764383` and tip `a8de3e69` give the same verdict (the ledger file is unchanged): `ROWS total=213 valid=212 invalid=1 superseded=34`, `freeze=refused oldest_pending_round=82 pending=30 parked=7 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=34 checks_run=114 overrides=3`, `PREDICATE R91-C3 fail`, rc 1. Gate DEFECT lines in a scratch clone: `override-unjustified R42-R2`, `override-unjustified R42-R3-33`, `override-unjustified R42-R3-37`, `check-failed R82-V8 rc=1`. Selftest 13 of 13 at the tip. | `python3 plans/round91_burndown.py --lane . --rev REV --work DIR --freeze-round 92`; `--selftest --work DIR` | **not met on its frozen predicate.** Predicted `freeze=admitted`: mispredict; no round-91 resolution row exists at the tip. The R82-V8 repair named in the frozen Move did not land (`plans/round83_c2_checks.py` unchanged since `ddb903a8`); the check passes only with `R83_ORIGIN_REPO` and `R83_FLEET_REPO` set. Owner `unowned:integrator` on `R51-R3-R90` passes the non-empty-owner clause. Held at ceiling 10; the capability row is not admitted. |
| companion R82-F1 (`round91_f1_counter.py` over `anchor_line_check.py`) | tip: `PARSED S260=1,S261=2,S265=1,S266=2`, `ANCHORLINE rows=274 cited=84 captured=71 uncaptured=13 defective=10 repaired=10 live=0`, `WRONG-LINE-CAUGHT True`, `PREDICATE R91-F1 pass`, rc 0. BASE: not reproduced; the tip counter against the BASE checker exits 1 (`AttributeError: no attribute 'anchor_quotes'`) and the label `PARSE-ABSENT` appears in neither checker revision [INFERENCE: the L1's BASE figure came from a different harness state]. | `python3 plans/round91_f1_counter.py --lane . --work DIR` | **met at the tip on its frozen predicate.** Not a scored claim axis; the BASE half is unreproduced. |

**Prediction ledger.** Each frozen prediction against its measured figure. Mispredicts are recorded here, never repaired in the frozen text.

| claim | figure | predicted (frozen text) | measured at BASE | measured at tip `a8de3e69` |
|---|---|---|---|---|
| C1 | before `defects` | N (control) | 9 | — |
| C1 | after `executed` / `defects` / `mismatches` | 1 / 0 / 0 | — | 0 / 10 / 10 (mispredict) |
| C1 | after `legs` | 10 × 2 = 20 | — | 20 (match) |
| C1 | `executed_rows` | 34 → 35 | 34 | 35 (match) |
| C1 | ledger `filesystem-metadata` / `numeric-band` | 2→3 / 3→4 | 2 / 3 | 3 / 4 (match) |
| C1 | ledger `stdout-inspection` / `file-artifact` / `subprocess-exec` | 10→11 / 25→26 / 12→13 | 10 / 25 / 12 | 11 / 26 / 13 (match) |
| C2 | pinned entries `K` | 13 sha + 3 blob = 16 | — | 16 (match) |
| C2 | selftest cases `C` | 6 | — | 8 (mispredict) |
| C2 | predicate exit | 2 at BASE, 0 at tip | 2 | 0 (match) |
| C3 | `pending` at BASE | ≥ 29 | 30 (match) | 30 |
| C3 | `malformed_or_invalid_unresolved` | ≥ 1 | 0 unresolved, 1 invalid (mispredict) | 0 unresolved, 1 invalid |
| C3 | after `freeze` / `checks_run` / `seeds` | admitted / ≥ 117 / ≥ 46 | refused / 114 / 46 | refused / 114 / 46 (mispredict on freeze and checks) |
| C3 | selftest cases | 9 | 13 | 13 (mispredict) |
| C3 | DEFECT class at BASE | unresolved invalid rows | override-unjustified ×3, check-failed R82-V8 | same (mispredict) |
| F1 | tip `PARSED` / `captured` / `defective` | no frozen figure (companion, not a claim) | not reproduced (tip counter vs BASE checker: AttributeError, rc 1) | `1/2/1/2` · 71 · 10 (matches the L1's tip figures) |

**Controls and batteries.** The scribe ran: C1 at BASE and at the tip (rc 1 both; the BASE run is the do-nothing control); C2 at BASE (rc 2) and at the tip (rc 0); C3 at BASE and tip (rc 1 both) and its selftest (13 of 13, rc 0); F1 at the tip (rc 0) and against the BASE checker (rc 1, AttributeError). The frozen C1 controls (ledger-only, forged-tip, forged-stamp, decorative-stamp, executed-gating) and the frozen C2 controls (one-byte mutation, absent path, tampered pin) were not re-run by the scribe; they are the L1's, and their figures are not restated here.

**Other axis scores.** Coverage 7 (C1 unmet; cap). Calibration 10 (C2 met, ceiling). Operability 10 (C3 unmet, ceiling). Novelty, depth, freshness, adjacency: not moved this round [INFERENCE: carried from the round-90 SCORECARD, not re-scored here].

**Sources.** S281 admitted (tier A, member replay only); S282 rejected (verifier wrapper). Registry 272 → 274 rows; census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` exit 0, `kengaku ok`.

**Mistakes mined** (`corpus/lessons/round-91.md` M1–M6; scribe S1–S5 from the measurements above): M1 prediction-unit (C2 selftest 6 vs 8, C3 selftest 9 vs 13); M2 frozen-text line-range error (grader defs at lines 11 and 46, cited as 16–42 and 45–48); M3 checker fixtures wrong (selftest 4 of 8 at B; corrected at B2); M4 vacuous able-to-fail control (F1 fixture); M5 blind-spot quotes unverified (no capture pins); M6 frozen C3 claims the R82-V8 repair, not implemented. S1 counter-format drift: the C1 parser expects `id=`, the probe writes the id positionally; the probe's own `ok=True` lines hid it. S2 kill-rule self-conflict: the C2 kill rule voids on edits after B; B2 made two such edits; the frozen tip rule fails literally. S3 owner-clause gap: `unowned:integrator` satisfies the non-empty check. S4 R82-V8 still path-dependent (clone-cwd check fails). S5 BASE F1 figure not reproduced.

**Corrections (append-only).** None made in this draft. The L1's BASE F1 `PARSE-ABSENT` figure and the single-DEFECT excerpt for C3 are recorded as not reproduced, not corrected in place, pending the L1's reconciliation.

### Round91 capabilities

| name | what it can now do | evidence pointer | first-working round |
|---|---|---|---|
| routed-findings freeze gate v2 | refuses a freeze while an old finding is open, a check fails, a blocked row is unowned (non-empty string), or a malformed row is unresolved; prints each override with its base check; runs each closed row's check once; selftest 13 of 13 | `python3 plans/round91_burndown.py --lane . --rev a8de3e69… --work DIR --freeze-round 92` → `freeze=refused … PREDICATE R91-C3 fail` rc 1; `--selftest` 13/13 rc 0. Admitted path not demonstrated; the owner clause accepts `unowned:` prefixes | 91 (refusal demonstrated; admission not yet) |
| external counter pin ledger with checker self-pin | pins 16 entries (13 sha, 3 blob) and the checker's own running bytes; the selftest runs inside the predicate | `python3 plans/round91_counter_pin.py --lane . --rev a8de3e69… --work DIR` → `PREDICATE R91-C2 pass` rc 0; kill-rule caveat on B2 | 91 |

### Planned (round 92; not a claim until frozen)

1. C1 counter: read the probe's positional case id in `parse_receipt`; amend under a new frozen predicate; re-run the full control set at the amended tip.
2. C3 triage: resolution rows for the 30 effectively-open rows (opened 82–89), the four blocked R51 rows (give `R51-R3-R90` a real owner), the three override rows missing `override_reason`, and the R82-V8 path repair; then `--freeze-round 92` must print `freeze=admitted`.
3. C2 kill rule and tip rule: the operator rules whether B2 counts as a post-B edit (`.ufo/l0-questions.md`).
4. Reproduce or retract the BASE `PARSE-ABSENT` figure for the F1 companion.
