# Kengaku round 26 — PROVINCE overlap scan

Axes: **novelty** (mapped to coverage/constructs) and **calibration**. Scope from `plans/round-26-claims.md:37-44` (C1 grader response perturbation), `:119-147` (C2 state-check population), and `:20-24` (Q13 Gate timing).

Method: case-insensitive searches over all 21 `/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` files for `grader`, `metamorphic`, `perturbation`, `invariance`, `extractor`, `evaluation harness`, and `gate timing` (individual regex searches; no public-web or model requests).

| Lane | Matching line(s) | Contested for Kengaku round 26? |
|---|---|---|
| mori | — no keyword matches | No evidence of overlap in PROVINCE |
| kagi | — no keyword matches | No evidence of overlap in PROVINCE |
| souji | — no keyword matches | No evidence of overlap in PROVINCE |
| kengaku | `PROVINCE.md:19` in-repo `grader.py` replay gate; `:108` verdict-gate `grader.py` presence check; `:126` judge calibration applied to this lane's own grader/attribution outputs | **No cross-lane contest**; direct same-lane ownership supports C1 scope |
| kama | — no keyword matches | No evidence of overlap in PROVINCE |
| kake | — no keyword matches | No evidence of overlap in PROVINCE |
| tsukuroi | — no keyword matches | No evidence of overlap in PROVINCE |
| kaidoku | `PROVINCE.md:147` “sasquatch” unblob squashfs recursion extractor | **No**; unrelated filesystem/archive extractor, not response extraction, grader verdicts, or Q13 Gate evidence |
| tameshi | — no keyword matches | No evidence of overlap in PROVINCE |
| mado | — no keyword matches | No evidence of overlap in PROVINCE |
| audio | — no keyword matches | No evidence of overlap in PROVINCE |
| game-dev-2d | — no keyword matches | No evidence of overlap in PROVINCE |
| kumitate | — no keyword matches | No evidence of overlap in PROVINCE |
| kotoba | — no keyword matches | No evidence of overlap in PROVINCE |
| lore | — no keyword matches | No evidence of overlap in PROVINCE |
| kasegi | — no keyword matches | No evidence of overlap in PROVINCE |
| game-dev-3d | — no keyword matches | No evidence of overlap in PROVINCE |
| kotodama | — no keyword matches | No evidence of overlap in PROVINCE |
| revenger | — no keyword matches | No evidence of overlap in PROVINCE |
| chousa | — no keyword matches | No evidence of overlap in PROVINCE |
| tabi | — no keyword matches | No evidence of overlap in PROVINCE |

**Bounded move:** classify roster collisions by shared method/artifact/population, not token alone. Keep Kengaku's grader entry as the positive same-owner match and Kaidoku's `extractor` as a negative-control lexical collision; this avoids falsely narrowing the novelty construct while preserving calibration about the scope of the scan. It does not replace the preregistered papers-and-tooling-registry prior-art search.

**Risks / limits:** PROVINCE text is a declared-ownership census, not proof of actual work or exhaustive synonym search. No matches for `evaluation harness` or `gate timing`; this is not evidence that no such work exists elsewhere. Kaidoku's line is a false positive only at keyword level; no technical conflict is indicated by the cited text.

**Verification:** case-insensitive grep over the 21 PROVINCE files returned only Kengaku lines 19/108/126 and Kaidoku line 147 for the complete requested term set; individual searches for `metamorphic`, `perturbation`, `invariance`, `evaluation harness`, and `gate timing` returned no matches. Re-run that grep before treating the census as current; inspect any new hit for shared grader method or response population rather than lexical overlap.

Files written: `.ufo/waves/round-26/build/ConnRosterScan.md` (SHA-256 recorded in handoff). Installs: none.

VERDICT: No competing lane ownership appears in the scanned PROVINCE files; the sole cross-lane hit is Kaidoku's unrelated squashfs extractor.