# ExecHarm — BASE 78460376 vs T dbe0cefa (leaf harm check, round 100)

Axes: (1) no standing gate turns green→red between BASE and T; (2) round-99 counters do not regress silently (their fails, if any, are by-construction and stated); (3) every historical `frozen-instruments` sha pinned at its adding commit still matches T; (4) the L1's own round-100 counters pass at T in an independent clone (falsification of the L1 battery).

Method: two `git clone --shared` checkouts (base @ 78460376, cand @ dbe0cefa, detached) under scratch; all 23 round-99 battery checks (`.ufo/waves/round-99/L1/harm/run_harm.sh`) run in each, in parallel; finding SETS compared (normalized, `loc=`/line numbers stripped). `plans/round82_c1_plans_registry.py` additionally run with `--tip` set to each revision from the cand tree. `plans/round100_prefreeze_check.py --base 78460376 --cand dbe0cefa` run. Round-99 counters run at T. Frozen tables re-derived: for each `plans/round-*-claims.md`, the adding commit (first `--diff-filter=A` commit) bytes parsed for a ```` ```frozen-instruments ```` block; every pinned sha recomputed against T bytes.

Tooling: uv (preinstalled) venv G (py3.13, pytest 8.4.1, pandas 2.3.2, pytest-json-ctrf 0.3.5, + scipy 1.16.1 for r99c1); git preinstalled. No other installs; no pacman. Receipts: `.ufo/waves/round-100/w1/ExecHarm/out/` (battery logs, diffs, frozen-union, counter logs).

## Verdicts

- HARM-BATTERY anchor (plans/anchor_digest_check.py) — MOVED (expected by design) — 9 expected `digest-wrong-capture`/`anchor-unbound` findings cleared (S210 S211 S219 S228 S232 S279 S281 S298 S300-old-class), S295 capture-unanchored cleared by the P0 capture; **no new finding class introduced** — `.ufo/waves/round-100/w1/ExecHarm/out/base-anchor.defects` + `cand-anchor.defects`.
- HARM-BATTERY anchorS300-newclass — NEW-RISK routed to L1 (informational in R100-C2) — the cleared S300 `anchor-unbound` line re-appears as `abbrev-unresolved token=fa53d657` at T (matches the counter's informational `RECLASS`); the row is bound by provenance for its 64-hex token, not for the abbreviated locator — `out/cand/anchor.log`.
- HARM-BATTERY anchorline — NO-CHANGE — both rc=0, live=0, row counts 333→341 (8 new rows) only — `out/base/anchorline.log` vs `out/cand/anchorline.log`.
- HARM-BATTERY grader — NO-CHANGE — rc=0 both — `out/base/grader.log` vs `out/cand/grader.log`.
- HARM-BATTERY r52c2/r63depth/r74c1/r75c1/r76c1 — NO-CHANGE — identical rc and identical (empty) finding sets — `out/*/r{52c2,63depth,74c1,75c1,76c1}.log`.
- HARM-BATTERY r68cap/r72c2/r73c2/r74c2/r75c2/r79c1/r80c1/r80c2/r81c2/r82c2 — NO-CHANGE — identical rc and finding sets (pre-existing findings unchanged, counts equal) — `out/*/<check>.log`.
- HARM-BATTERY r77c1 — MOVED-expected — sole difference `COUNT-DRIFT 1041 rows=333→341 pin=266` (8 new SOURCES rows S342–S349); same defect class at both revisions — `out/base/r77c1.log` vs `out/cand/r77c1.log`.
- HARM-BATTERY r78c1 — MOVED-expected — count drift k=4→5 (crypto-credential), k=34→35 (file-artifact), coverage-regression line re-pointed; class set unchanged (122 lines both) — `out/base/r78c1.log` vs `out/cand/r78c1.log`.
- HARM-BATTERY r81c1 — MOVED-expected — executed 43→44, unexecuted 45→44; same single defect — `out/base/r81c1.log` vs `out/cand/r81c1.log`.
- HARM-BATTERY r82c1-at-default-tip — NO-CHANGE (sets identical, 13=13) — both trees produce the same 12 DEFECTs (DEFECTS n=12) plus the TARGET/PREDICATE lines — `out/base/r82c1.log` vs `out/cand/r82c1.log`.
- HARM-BATTERY r82c3 — MOVED-expected — histogram recomputed 4→5, 34→35, ledger 43→44; the new finding `STATUS-LINE-MISSING financial-document-processor` is the same class as BASE's own `STATUS-LINE-MISSING bn-fit-modify` (each round's member lacks its addendum until its own round; bn-fit-modify's line is round-99's, not round-100's to add) — `out/base/r82c3.log` vs `out/cand/r82c3.log`.
- REGISTRY --tip r82c1 — NO-CHANGE — `--tip 78460376` and `--tip dbe0cefa` from the cand tree give identical DEFECT sets (12=12, sets byte-equal); only registered rows 177→182, base_scripts 178→183 — `out/r82-base.log` vs `out/r82-cand.log`.
- PREFREEZE round100_prefreeze_check — clean — `PREFREEZE new=0 gone=0 line_base=0 line_cand=0 reg_base=12 reg_cand=12`, `VERDICT clean`, rc=0 — `out/prefreeze.log`.
- R99-C1 at T — fail by construction (stated) — L7 fails only: the counter expects ledger == BASE(2233a661)+bn-fit-modify, but T also holds round-100's financial-document-processor (`set_added=['bn-fit-modify','financial-document-processor']`); all other legs L1–L6,L8–L11 pass — `out/r99c1.log`.
- R99-C2 at T — fail by construction (stated) — K7 fails: its population is anchor-unbound@2233a661 (12 rows), and R100-C2's new provenance binds moved 10 of those rows; counters K1–K6 pass. The counter's BASE differs from this assignment's BASE (its 2233a661 ≠ 78460376), and its gate counts (45 base / 23 rev) reflect that older anchor — `out/r99c2.log`.
- FROZEN-UNION rounds 93–100 — verified — all 7 claims files with `frozen-instruments` blocks (rounds 93–100) match T sha-for-sha: 9/9, 11/11, 11/11, 11/11, 10/10, 13/13, 18/18 entries, plus round-100's 16 — `out/frozen-union.txt`.
- FROZEN-UNION rounds 24–92 — N/A by format — none of the 69 earlier `plans/round-*-claims.md` files contains a ```` ```frozen-instruments ```` sha block (round-37 and round-45 mention the phrase in prose only; frozen-instruments sha tables begin at round 93's fresh-start) — `out/frozen-union.txt`.
- R100-C1 independent run at T — pass — all 13 legs L1–L13 pass, TARGET line byte-matches the frozen predicate (`set_equals_base_plus_member=1 … defects=0`), rc=0 — `out/r100c1.log`.
- R100-C2 independent run at T — pass — all 10 legs K1–K10 pass, gate line 33/32/23 as predicted, `RECLASS` line for S300 as predicted, rc=0 — `out/r100c2.log`.

## Green→red summary

No standing gate turned green→red: the only red→red moves are the expected ledger/class/snapshot deltas (r77c1, r78c1, r81c1, r82c3) and the anchor's designed purification; the one genuinely new finding line at T is `anchor S300 abbrev-unresolved`, which the R100-C2 counter already classifies informational (`RECLASS`) and carries as a routed item, not a new gate class. Round-99 counters fail at T only for the two stated by-construction reasons.
