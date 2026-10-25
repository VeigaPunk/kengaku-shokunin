# FxScope — round-32 build wave scope audit (leaf sentinel)

Seat: `L1Kengaku32.FxScope` · 2026-10-25 · Lane: `kengaku-shokunin` (read-only git only; this report is the only file written).

VERDICT: scope-clean

## 1. Build-report path inventory (34/34 reports)

Every path each seat declares touching, cross-checked against `git status --porcelain` (lane), the build spec (`build-spec.json`, 34 items), and live filesystem state. All writes fall into exactly two classes: **the report's own path under `.ufo/waves/round-32/build/`** and **`/tmp/r32-*` scratch** (every scratch dir < 60 MB, verified via `du`).

| Report | Declared writes (all within build/ or /tmp) |
|---|---|
| R32ReconPackage | /tmp/r32-R32ReconPackage/ captures (~75 KB); "No writes outside this file and /tmp/r32-R32ReconPackage/" |
| R32SrcS094a / R32SrcS094b | /tmp/r32-R32SrcS094a/main.py, /tmp/r32-R32SrcS094b/main.py (+retry.py) captures |
| R32SrcS097 | /tmp/r32-R32SrcS097/arxiv-2412.05579v2.html capture |
| R32PlanWalk | read-only commands; path-hazard notes; no writes declared |
| R32DraftEntry | scratch /tmp/r32-R32DraftEntry/ empty; "No lane file was created, edited or deleted by this seat" |
| R32DraftRows | /tmp/r32-R32DraftRows/sim/ (344 KB); "Nothing under the lane was created, edited or deleted except this one report file" |
| R32DraftLesson | "no lesson/product file was written (leaf write boundary permits only this report)" |
| R32DraftMistakes | "I wrote only my own path"; fleet status quoted read-only (git status --porcelain) |
| R32DraftErrata | "proposed text only; no fleet report, lane receipt, or lesson was edited here" |
| R32DraftScorecard | drafted table in report; after-receipt files "did not exist when this draft was written" (confirmed absent on disk) |
| R32DraftReport | skeleton in report; fleet target `.ufo/reports/round-32/kengaku.md` is L1's landing job — "No write" |
| R32GateBlock | all outputs to /tmp/r32-R32GateBlock/block.md; "nothing under the lane repo was created or changed except this single report file" |
| R32QuoteMode | /tmp/r32-R32QuoteMode/ captures + rows/map/block files |
| R32MirrorCensus | /tmp/r32-R32MirrorCensus/ mirror (23 MB); "No lane production files were modified" |
| R32CollisionGuard | /tmp/r32-CollisionGuard/scratch-registry.md; "this report is the only file written under the lane repo" |
| R32Quarantine | curl fetches (HTTP 200 bodies reported); no writes declared beyond report |
| R32CountersPreflight | counter runs on live lane, read-only; no edits declared |
| R32CatProbe | /tmp/r32-R32CatProbe/ raw JSON (cleaned after handoff); "no production files touched" |
| R32LearnC1 | /tmp/r32-R32LearnC1/ captures + SHA256SUMS.txt |
| R32RevClaims | read-only git + counter runs; "No seat edits" |
| R32RevEntry | /tmp/r32-R32RevEntry/ (16,626 B fetches); "No lane file was created, edited or deleted by this seat" |
| R32RevGate | /tmp/r32-R32RevGate/s093-test.sh fetch |
| R32RevFixes | /tmp/r32-R32RevFixes/sim4/ copies + verifier_mode.py fetch |
| R32CritC1 | /tmp/r32-l1kengaku32/fleet/c1fake-shokunin/ synthetic trees (23 MB); "No repo bytes were modified" |
| R32CritC2 | /tmp/r32-critc2/ (~0.4 MB); "Nothing in the lane was written" (records mid-review edits by an unattributed sibling seat — see §4) |
| R32CritC3 | "Read-only review; no probe or production files changed" |
| R32MutCounters | /tmp/r32-R32MutCounters/ battle copies (272 KB); "Nothing outside /tmp/r32-R32MutCounters/ and this report was written" |
| R32MutRows | /tmp/r32-R32MutRows/ (96 KB); "no lane-repo writes except this report" |
| R32ConnSibling | read-only scan of 20 sibling lane repos; "No production edits; this report is the only file written" |
| R32Sentinel | scan of new bytes; no tools installed; no writes declared |
| R32SentinelScope | read-only inspection; item-by-item confirmation all 34 planned writes stay in build/ + /tmp |
| R32Frontier | /tmp/r32-frontier/ (68 KB); "Read-only git only" |
| R32Considerthese | "nothing was changed outside this report" |

Check: build/ holds exactly 34 `.md` reports + `swarm-registry.json`; no `-3`-suffixed report files exist (duplicate seat set reconciled — only scratch dirs /tmp/r32-L1Kengaku32.R32Sentinel-3, /tmp/r32-R32Sentinel remain). No report references a write to `watchdog.log`, `MANIFEST.json`, `.ufo/state`, sibling lane repos, lane git indexes, or any fleet-report path; `corpus/evidence/round32/` does not exist (landing receipt slots unwritten, as claimed).

## 2. Lane uncommitted state (`git status --porcelain`)

**Untracked — exactly `.ufo/waves/round-32/*` + the planned entry:**
- `.ufo/waves/round-32/{assimilation/,build/,falsify/,build-assignments.json,build-run.log,build-spec.json,falsify-assignments.json,falsify-assignments.raw.txt,falsify-run.log,falsify-spec.json}`
- `corpus/knowledge/benchmark-grader-semantics.md` (C1 entry, planned landing)

**Modified — exactly the planned landing files:**
- `SKILL.md` (+`sources-adopt` §Gate/probe registry row — C2 D4/R4 fix)
- `corpus/README.md` (index rows +1 — C1)
- `corpus/SOURCES.md` (+S094/S097 rows, S093 used-by — C1)
- `corpus/evidence/round31/gate-cli-exits.txt` (regenerated CLI receipt — C2 D3/R3 fix)
- `corpus/knowledge/open-model-catalogs.md` (C3 refresh)
- `plans/catalog_probe.py` (C3 counter)
- `plans/round32_defects.py` (C2 counter)

Nothing staged (index untouched), no deletions, no unexpected untracked paths anywhere else in the lane. `plans/adoption_check.py` and `plans/round32_c1_verify.py` remain tracked and unmodified (frozen counters).

## 3. Fleet-repo / root-file check

- No round-32 build report writes to the fleet repo. The wave's only fleet targets (round-31 report erratum D1; round-32 report) are unwritten: `.ufo/reports/round-32/kengaku.md` absent; `.ufo/reports/round-31/kengaku.md` mtime 2026-10-25 06:07 (pre-wave).
- Fleet worktree deltas are all harness/orchestrator-owned or from other lanes: `.ufo/state/*.report-baseline` (mtime 09:35, at setup), `.ufo/watchdog.log`, `scripts/hyaku/*`, `.omp/mcp.json`, `.scratch/goal-20261025-hyaku-12h.md` (09:29, pre-wave). None is claimed or evidenced as a round-32 build write.
- Fleet-root untracked `m-rev-vs-rev.py` (8,796 B, mtime 09:36:30) **predates** the freeze (09:40:16) and wave launch (09:41:08); it is recorded only as an *observed* misroot in `R32DraftMistakes.md` (an untracked fork of the souji-lane coverage-agreement tool), not written by any round-32 build seat. No fleet-repo root file is involved in the wave.

## 4. Notes (non-leaks)

- **Mid-review edits to `plans/round32_defects.py`:** `R32CritC2.md` records the live working tree being edited twice during its review by an unattributed sibling seat (injection seams/params + synthetic R1/R2 selftest fixtures; `if item_id in ("R1", "R2"): continue` at live :229). Both change sets are present in the current uncommitted diff of `plans/round32_defects.py` — i.e. they fold into the planned C2 counter landing (the file is a planned landing file, modified not untracked). No bytes outside that planned file were produced; recorded for attribution completeness.
- **Duplicate `-3` seat set:** `R32DraftMistakes.md` observed two concurrent seat sets (34 unsuffixed + 34 `-3`-suffixed) in `build-assignments.json`. Only the unsuffixed 34 reports exist in `build/`; `-3` seats left only /tmp scratch dirs (e.g. `/tmp/r32-L1Kengaku32.R32Sentinel-3`), no stray write paths.
- **Scratch hygiene:** all `/tmp/r32-*` dirs ≤ 23 MB; no scratch outside /tmp; no `/tmp` cleanup outside own dirs claimed.

## 5. Acceptance summary

- Build reports touch only their report paths under `.ufo/waves/round-32/build/` and `/tmp/r32-*` scratch — no leak.
- Lane untracked paths are only `.ufo/waves/round-32/*` and the planned entry; modified set is exactly the planned landings (entry, SOURCES.md, README.md, open-model-catalogs.md, counters, SKILL.md row, regenerated round-31 CLI receipt) — no leak.
- No fleet-repo root file involved; fleet writable surfaces untouched by the wave — no leak.

VERDICT: scope-clean
