# R31FxSeatDeaths — seat-liveness audit, round 31 (both wave registries)

- Seat: `R31FxSeatDeaths` (scout, calibration axis; leaf — no subagents, no respawn).
- Audit time (snapshot): **2026-10-25T09:04:40Z** (`date -u`).
- Registries read: `.ufo/waves/round-31/build/swarm-registry.json` (wave `kengaku-r31-build`,
  createdAt 2026-10-25T08:48:44Z, updatedAt 08:48:47Z) and
  `.ufo/waves/round-31/falsify/swarm-registry.json` (wave `kengaku-r31-falsify`,
  createdAt 2026-10-25T09:02:41Z, updatedAt 09:03:57Z).
- Spec cross-check: `build-spec.json` and `falsify-spec.json` each list exactly the same 36
  members with identical roles as their registry (JSON diff: no name or role mismatch).
- No tools installed/upgraded this run (no need; PACMAN paused was never touched).

## 1. Wave 1 — build (kengaku-r31-build), 36 members, reportDir `.ufo/waves/round-31/build`

Method: for each registry member `<seat>` tested `build/<seat>.md` (glob + `os.path.getsize`).
Files on disk: 36 `.md` reports + `swarm-registry.json`; no extra `.md`, zero missing, zero empty.

| seat | role | report file | bytes | self-named |
|---|---|---:|---:|---|
| R31ConnSibling | connector | R31ConnSibling.md | 22979 | yes |
| R31CritC1 | critic | R31CritC1.md | 13497 | yes |
| R31CritC2 | critic | R31CritC2.md | 19777 | yes |
| R31CritC3 | critic | R31CritC3.md | 16272 | yes |
| R31DefR1 | reviewer | R31DefR1.md | 24316 | yes |
| R31DefR10 | reviewer | R31DefR10.md | 14018 | yes |
| R31DefR2R3 | reviewer | R31DefR2R3.md | 18628 | yes |
| R31DefR4R5 | reviewer | R31DefR4R5.md | 25864 | yes |
| R31DefR6 | reviewer | R31DefR6.md | 13409 | yes |
| R31DefR7 | reviewer | R31DefR7.md | 15872 | yes |
| R31DefR8 | reviewer | R31DefR8.md | 10658 | yes |
| R31DefR9 | reviewer | R31DefR9.md | 25791 | yes |
| R31DraftEntry | scribe | R31DraftEntry.md | 28463 | yes |
| R31DraftGate | scribe | R31DraftGate.md | 31785 | yes |
| R31DraftRows | scribe | R31DraftRows.md | 21330 | yes |
| R31EntryScope | scout | R31EntryScope.md | 29014 | yes |
| R31GateAdv | mutation-tester | R31GateAdv.md | 12641 | yes |
| R31GateDesign | critic | R31GateDesign.md | 24923 | **no** |
| R31GateFixture | executor | R31GateFixture.md | 31368 | yes |
| R31GateRegress | executor | R31GateRegress.md | 20003 | yes |
| R31MutCounter | mutation-tester | R31MutCounter.md | 13210 | yes |
| R31PlanWalk | scout | R31PlanWalk.md | 17017 | yes |
| R31ReconCensus | scout | R31ReconCensus.md | 12236 | yes |
| R31ReconPackage | scout | R31ReconPackage.md | 18387 | yes |
| R31ReconRegistry | scout | R31ReconRegistry.md | 19809 | yes |
| R31RevClaims | reviewer | R31RevClaims.md | 20981 | yes |
| R31RevScope | reviewer | R31RevScope.md | 17987 | yes |
| R31Revenger | revenger | R31Revenger.md | 18737 | yes |
| R31SimplGate | simplifier | R31SimplGate.md | 17908 | yes |
| R31SrcS092a | scout | R31SrcS092a.md | 7882 | yes |
| R31SrcS092b | scout | R31SrcS092b.md | 11763 | yes |
| R31SrcS092c | scout | R31SrcS092c.md | 12319 | yes |
| R31SrcS093a | scout | R31SrcS093a.md | 9004 | yes |
| R31SrcS093b | scout | R31SrcS093b.md | 13687 | yes |
| R31SrcS100a | scout | R31SrcS100a.md | 11617 | yes |
| R31SrcS100b | scout | R31SrcS100b.md | 13794 | yes |

Role mix (build): scout 12, reviewer 10, critic 4, scribe 3, executor 2, mutation-tester 2,
connector 1, revenger 1, simplifier 1.

Findings:
- All 36 reports present, non-empty (min 7882 B), none names a different seat
  (header grep: every file's first non-empty lines cite its own seat/topic).
- Exception noted: `R31GateDesign.md` never contains the string `R31GateDesign`; it identifies
  only as "Seat: UFO-FSD critic" and is titled "R31 C3 — design review". This is self-identification
  omission, not a mislabeled/foreign report (it matches the seat's C3 assignment). Not dead by the
  three criteria, flagged as weakly identified.

## 2. Wave 2 — falsify (kengaku-r31-falsify), 36 members, reportDir `.ufo/waves/round-31/falsify`

Method: same `glob`/`getsize` check; directory listing at audit time:
`swarm-registry.json` only — **0/36 `.md` reports present**.
Lane-wide sweep: `find kengaku-shokunin -name 'R31Fx*.md' -not -path '*/.git/*'` → empty
(no R31Fx report exists anywhere else in the lane).

| seat | role | report file at audit |
|---|---|---|
| R31FxQuoteS092 | reviewer | missing |
| R31FxQuoteS093 | reviewer | missing |
| R31FxQuoteS100 | reviewer | missing |
| R31FxSweep731 | critic | missing |
| R31FxSharedMode | revenger | missing |
| R31FxGraderProbe | mutation-tester | missing |
| R31FxRowsSchema | reviewer | missing |
| R31FxRowIdentity | critic | missing |
| R31FxC1Counter | critic | missing |
| R31FxC2Survivors | mutation-tester | missing |
| R31FxC2AppendOnly | critic | missing |
| R31FxC2R9 | mutation-tester | missing |
| R31FxC2R6R8 | critic | missing |
| R31FxC3Gate | critic | missing |
| R31FxC3Tally | mutation-tester | missing |
| R31FxC3Regress | reviewer | missing |
| R31FxEvidenceRerun | reviewer | missing |
| R31FxLogErrata | reviewer | missing |
| R31FxScorecard | reviewer | missing |
| R31FxClaimsOrder | scout | missing |
| R31FxCensus7 | scout | missing |
| R31FxFrontierRows | reviewer | missing |
| R31FxEntryBar | reviewer | missing |
| R31FxUncommitted | reviewer | missing |
| R31FxWaveShape | scout | missing |
| R31FxHashCite | scout | missing |
| R31FxS100Dupe | critic | missing |
| R31FxSkipUpload | critic | missing |
| R31FxTB2Reset | critic | missing |
| R31FxPriorArt | scout | missing |
| R31FxLessonDraft | reviewer | missing |
| R31FxQualityBar | reviewer | missing |
| R31FxSeatDeaths | scout | missing (this report, written now) |
| R31FxAdoptionRule | critic | missing |
| R31FxConsiderthese | scout | missing |
| R31FxTrends | critic | missing |

Role mix (falsify): reviewer 13, critic 11, scout 7, mutation-tester 4, revenger 1.

Reason for missing reports: the falsify wave is **mid-flight at audit time** — registry
createdAt 09:02:41Z (≈13 min before snapshot), peer roster shows the R31Fx seats still running,
and `yield.tsv` has **zero** round-31 rows (`grep -c $'\t31\t' yield.tsv` → 0). So the observed
reason is "report not yet landed / wave in flight", not "seat finished without a report".
No seat can yet be certified dead by completion from this snapshot.

## 3. Dead-seat list (criteria: no report file, empty file, or report naming a different seat)

- Build wave: **none dead** (36/36 present, non-empty, none mislabeled; one weak self-ID: R31GateDesign).
- Falsify wave: **36/36 currently without a report file** — not dead, un-landed as of the snapshot.
  Re-check after wave completion; any seat that then still lacks a non-empty, self-identified report
  would be dead.

## VERDICT

- **Survived:** build-wave seat liveness — all 36 build seats have present, non-empty, correctly
  attributed reports; no dead seats in wave 1.
- **Not proven / un-landed:** falsify-wave seat liveness — 0/36 reports exist at 09:04:40Z, so no
  falsify seat liveness claim survives this snapshot; the wave is still in flight (registry 09:02:41Z,
  no yield.tsv rows), which is the reason, not a completed-seat failure.

## Evidence pointers

- Registries: `.ufo/waves/round-31/build/swarm-registry.json` (members lines 8-387),
  `.ufo/waves/round-31/falsify/swarm-registry.json` (members lines 8-382); specs
  `.ufo/waves/round-31/build-spec.json`, `.ufo/waves/round-31/falsify-spec.json`.
- On-disk directory listings: `ls -la .ufo/waves/round-31/build/` (36 md + registry),
  `ls -la .ufo/waves/round-31/falsify/` (registry only).
- Lane-wide R31Fx sweep: `find kengaku-shokunin -name 'R31Fx*.md' -not -path '*/.git/*'` → empty.
- Yield ledger: `.ufo/waves/yield.tsv` — no round-31 rows (last round present: 30, rows 42-110).
- Size/self-name scan: per-file `os.path.getsize` + first-lines header read (this report's tables).
