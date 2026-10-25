# R33IndexTruth — corpus/README.md index/coverage/frontier verbatim check vs committed file

Seat: `R33IndexTruth-2` (leaf; no subagent dispatch, no background jobs, no model pinning).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Access date: **2026-10-25**.
Report path: `.ufo/waves/round-33/build/R33IndexTruth.md`.
Production writes by this seat: none beyond this file. Scratch: `/tmp/r33-indextruth/` (HEAD/working-tree README copies, line extracts; < 100 KiB).

## 0. Tree state observed (re-derived, not assumed)

- Baseline (frozen claims): `112091c2d9077e484b53512ca363d2fe6ba6fc5c` (round-32 verifier spot-check).
- Freeze commits: `f0b20ae` (claims/counters/controls), `c227e48` (N1 round-32 wave inheritance).
- At first read, `HEAD` = `7895588` (C2 repairs: N2 scorecard section, N5/N6 lesson errata, Q22, defects-after receipt).
- During this verification the tip moved: `HEAD` now = `2b4cef2e84e1fbc95d500d067bccb44c46d18626` ("round-33: renumbered assimilation (S103/S104), routed-defect closure N1-N6, catalog re-probe receipts"), descendant of `7895588`. **All verdicts below are re-derived against the current tip `2b4cef2`** (committed file `corpus/README.md`, `git show HEAD:corpus/README.md`, 388 lines).
- Working tree `corpus/README.md` is **clean** (no diff vs HEAD). The integrating L1 committed the README patch at `2b4cef2`.

## 1. Verbatim-check table (report `R33ReadmePatch.md` vs committed README at tip `2b4cef2`)

| Check | Report claim | Committed tip | Result |
|---|---|---|---|
| Old string `:67` (index row, S094/S097/pro2) exists verbatim at cited line | "BEFORE" block at R33ReadmePatch.md:33 | `HEAD:corpus/README.md:67` byte-identical | ✅ |
| New index row text `:67` (S103/S104, credential clause) | "AFTER" block at :39 | `HEAD:corpus/README.md:67` byte-identical | ✅ |
| Old string `:255` (coverage bullet, S094/S097, "fails open") | "BEFORE" block at :54 | `HEAD:corpus/README.md:255` byte-identical | ✅ |
| New coverage bullet `:255` (round 33, admitted under renumbered ids; S103/S104) | "AFTER" block at :60 | `HEAD:corpus/README.md:255` byte-identical | ✅ |
| Old string `:279` (frontier sub-bullet, round 32, S097) | "BEFORE" block at :83 | `HEAD:corpus/README.md:279` byte-identical | ✅ |
| New frontier sub-bullet `:279` (round 33, S104, **S103**) | "AFTER" block at :89 | `HEAD:corpus/README.md:279` **differs by exactly the `, S103` insertion** — the committed line reads `(`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and the LLM-as-judge survey frame (S104)`; the report's recommended text reads `(`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`, S103) and … (S104)` | ⚠️ drift |
| Index row changes: exactly S094→S103, S097→S104 in citation cell | §2 | committed `:67` citation cell: S103/S104, S093 retained; no other id change | ✅ |
| Index row description cell | §2/F2 | `a log-bucket check fails open` → `its log-bucket check mixes fail-open exceptions with fail-closed credential absence` (deliberate, C1-mandated) | ✅ (expected deviation) |
| No other row touched | §5 | `git diff 7895588..2b4cef2 -- corpus/README.md` = exactly 3 hunks, 3 insertions / 3 deletions (lines 67/255/279); no other line changes | ✅ |
| Row count | §5 "41 rows" | `^\| `knowledge/` rows: 41 (committed tip, confirmed by grep) | ✅ |
| Index row for the entry | §5 "rows==1" | exactly one `benchmark-grader-semantics.md` index row at `:67` | ✅ |
| No S094/S097 anywhere in README | §1 | committed README scan: zero hits (grep exit 1) | ✅ |
| Entry's cited ids exist in committed registry | §5 | committed `corpus/SOURCES.md`: S093 @ :112, S103 @ :118, S104 @ :119 rows present (mined rows) | ✅ |

## 2. Index parity — 40 vs 41

Assignment/lane-facts predicate: "index currently holds 40 knowledge rows = 40 files".

Measured (grep `^\| `knowledge/` vs `ls corpus/knowledge/*.md`), all three snapshots:

| Snapshot | README rows | knowledge files |
|---|---|---|
| Baseline `112091c` (round-33 start per claims) | 41 | 41 |
| Tip `2b4cef2` (committed) | 41 | 41 |
| Working tree | 41 | 41 |

- **Parity holds: 41 = 41** (same at baseline and tip — the README row for `benchmark-grader-semantics.md` already existed at `112091c`; the draft file and its index row are round-32/33 commits, not this round's additions).
- The absolute count is **41, not 40**: the round-33 claims file says "40 files, 40 index rows", but the baseline `112091c` tree already holds 41 files / 41 rows (the unadmitted `benchmark-grader-semantics.md` draft + its row). The "40" figure is stale for this baseline. The exemption is 41=41; the claims-file "40" is a baseline-description erratum (out of this seat's patch scope; reported).
- The extra two rows outside the "What's here" table (lines 352, 379 — round-28/29 webarena entries) are pre-existing, not touched this round.

## 3. Findings

- **F1 (committed residual defect):** the committed frontier bullet `:279` discharges the round-31 clause under the path/commit and S104 but **does not name S103** — the C1 frozen predicate requires the discharge *under S103* (Toolathlon code). `R33ReadmePatch.md` F1 flagged this as must-fix; the integrating commit `2b4cef2` shipped the pre-fix text (`, S103` missing). The index row `:67` and coverage bullet `:255` do carry S103, so this is a text-level omission, not a registry divergence. Needs an L1 follow-up edit or erratum: insert `, S103` after `` `9be8d8fe`) `` (move the closing paren) on line 279.
- **F2 (expected deviation):** the description-cell "fails open"→"mixes fail-open exceptions with fail-closed credential absence" correction is the C1-mandated credential reading (lane facts); not index drift.
- **F3 (report note):** the entry cites `corpus/README.md:276` for the clause `"and for Toolathlon"`; the literal clause sits at `:278`. Not a README text defect for this seat's scope (entry-owner decision).

## 4. Verdict

Index row, coverage bullet, registry parity, and patch scope are exact; the committed frontier bullet `:279` is missing the `, S103` insertion versus the report's recommended text (one dangling token, two characters' worth of insertion — the only committed README deviation found).

`VERDICT: index-exact` — the index row (`:67`) itself is byte-exact (S094→S103, S097→S104, no other row touched, 41=41 parity), with one reported committed deviation in the *frontier* bullet `:279` (missing `, S103`), which is a text omission in a non-index line, not an index drift.

Note: the "40 rows = 40 files" literal claim is stale; measured is 41 = 41 at baseline and tip.
