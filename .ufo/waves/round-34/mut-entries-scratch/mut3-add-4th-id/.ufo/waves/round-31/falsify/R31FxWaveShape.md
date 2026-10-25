# R31FxWaveShape — wave-shape audit (round-31 build + falsify)

Auditor: L1Kengaku31.R31FxWaveShape (scout, leaf). Audit time: 2026-10-25 ~06:04 (falsify wave in flight).
Method: parsed JSON with python3 stdlib (no tools installed; nothing needed). Sources below are in the lane
/home/vgpnk/Projects/shokunin/kengaku-shokunin unless an absolute path is given.

## 1. Member counts and assignment linkage

| Wave | Spec items | Registry members | Name sets identical |
|---|---|---|---|
| build (wave 1) | 36 (`.ufo/waves/round-31/build-spec.json` items) | 36 (`.ufo/waves/round-31/build/swarm-registry.json` members) | yes |
| falsify (wave 2) | 36 (`.ufo/waves/round-31/falsify-spec.json` items) | 36 (`.ufo/waves/round-31/falsify/swarm-registry.json` members) | yes |

- Check: `python3` set-diff over spec `items[].name` vs registry `members` keys → both waves `sets equal: True`, no extras on either side.
- Every member record: `kind=spawn`, `agentId`, `role`, `axes`, `milestone`, `item: null` (registry `.ufo/waves/round-31/build/swarm-registry.json:8-387`, member schema e.g. `:9-18`; falsify `:8-382`). Assignment linkage spec↔registry is by identical name key only; the `item` field is null on all 72 records.
- Both waves are within the v1 band 32–64 (kengaku-round-31.md §6, lines 182-192; policy fixture `scripts/hyaku/ufo-wave-policy.json`); round total 72 ≤ 128 (line 192).

## 2. Role histograms (registry `role` field)

build (36): scout 12, reviewer 10, critic 4, scribe 3, executor 2, mutation-tester 2, connector 1, revenger 1, simplifier 1.
falsify (36): reviewer 13, critic 11, scout 7, mutation-tester 4, revenger 1.
All kinds: `spawn` (36/36 per wave). No `labrat`, `planner` or `distiller` seats in either wave.

## 3. Attack-role share under named conventions

Convention A — falsify-wave attack mix (kengaku-round-31.md lines 187-190: "fresh
reviewer/critic/mutation-tester/scout seats attack what wave 1 produced"): attack set {reviewer, critic,
mutation-tester, scout}. build 28/36 = 77.8%; falsify 35/36 = 97.2%.
Convention B — policy v2 attack roles (same file lines 195-196: "attack roles (reviewer, critic,
mutation-tester, labrat)"): attack set {reviewer, critic, mutation-tester, labrat}. build 16/36 = 44.4%
(labrat 0); falsify 28/36 = 77.8% (labrat 0). Both waves exceed the v2 ≥25% attack floor under either
convention; the only non-attack seats are connector/scribe/executor/simplifier/revenger.

## 4. Null agentId

None. 0/72 members have `agentId: null` (both registries; check: dump of every member's `agentId`).

## 5. Seat reports

build: exactly 36 `.md` files in `.ufo/waves/round-31/build/`, one per member, no missing, no orphans
(member-set — file-set diff empty; sizes 7,882–31,785 B, all non-empty). Committed in `dbb07364`
(`git log --oneline -1 -- .ufo/waves/round-31/build` → `dbb0736 round-31: ...`).
Post-commit worktree deviations (git status --porcelain): ` M .ufo/waves/round-31/build/R31MutCounter.md`,
`?? .ufo/waves/round-31/build/R31DraftGate.md` — two of the 36 build reports no longer match the landed
commit; also `?? .ufo/waves/round-31/falsify-spec.json`, `?? .ufo/waves/round-31/falsify/` (in-flight).
falsify: at audit time 0/36... 1/36 reports present (R31FxSeatDeaths.md landed 06:04 during this audit);
35 missing (list per registry keys minus present). This is the wave in flight, not a dead seat; seats are
still landing. No orphan `.md` files in either directory.

## 6. Spec items whose prompts name relative paths that would land in the fleet repo

Documented rule: "Seat paths are absolute: seat tools also start at the fleet root, so a relative path
such as `.ufo/waves/...` lands in the FLEET repo" (kengaku-round-31.md lines 253-261). Relative path
tokens found in prompt bodies (extracted with regex `[A-Za-z0-9_~.\-]+(?:/[A-Za-z0-9_~.\-]+)+`):

build (7 items): R31DefR9 (`build/R30DraftGate.md`, `build/R30RevLesson.md`,
`falsify/R30FxCoverageAxis.md`, `falsify/R30FxEntryCompleteSet.md`, `falsify/R30FxEntryQ4Q6.md`,
under an absolute round-30 directory prefix), R31DefR10 (`falsify/swarm-registry.json`), R31DraftRows
(`corpus/knowledge/benchmark-verifier-execution-model.md` as a `used-by` cell value), R31PlanWalk
(`plans/sources_adopt.py`, inside a `git -C <abs-lane> show 0883e72:plans/sources_adopt.py` command),
R31DraftEntry (`corpus/knowledge/benchmark-task-validity-checklist.md`), R31DraftGate
(`corpus/lessons/round-31.md`), R31ReconPackage (`knowledge/corpus/knowledge/.`).

falsify (18 items): R31FxGraderProbe (`.ufo/waves/round-31/build/R31SrcS093b.md`),
R31FxC1Counter (`.ufo/waves/round-31/build/R31CritC1.md`, `.ufo/waves/round-31/claims/control-nothing.txt`),
R31FxC2Survivors (`.ufo/waves/round-31/build/R31CritC2.md`),
R31FxC3Gate (`.ufo/waves/round-31/build/R31GateDesign.md`),
R31FxC3Regress (`.ufo/waves/round-30/falsify/R30FxGateRegression.md`,
`corpus/evidence/round30/quote-mode-six-rows.txt.`), R31FxEvidenceRerun (`corpus/evidence/round31/`),
R31FxLogErrata (`LOG.md`, `corpus/lessons/round-30.md`), R31FxClaimsOrder (`plans/round-31-claims.md`,
`.ufo/waves/round-31/claims/`), R31FxCensus7 (`corpus/evidence/round31/`), R31FxFrontierRows
(`corpus/README.md`, `corpus/knowledge/`, `knowledge/`), R31FxEntryBar (`corpus/QUALITY.md`),
R31FxLessonDraft (`corpus/lessons/round-30.md`), R31FxQualityBar (`corpus/QUALITY.md`,
`corpus/lessons/round-31.md`, `.ufo/waves/round-31/build/.`), R31FxSeatDeaths (`.ufo/waves/round-31/`),
R31FxWaveShape (`.ufo/waves/round-31/build-spec.json`, `build/swarm-registry.json`),
R31FxRowIdentity (`plans/round31_c1_verify.py`), R31FxC2AppendOnly (`plans/round31_defects.py.`),
R31FxC2R6R8 (`plans/round31_defects.py.`). (`tests/test.sh`, `v2/README.md`, `models/task/verifier_mode.py`
are remote-repo-relative fetch targets, not fleet-relative.)

Classification: all of these are READ references or data values — **no item prompt directs a write to a
relative path**; every report destination is deferred to the validator's `Report:` trailer, and both spec
contexts carry the mandated resolution clause ("Every `Report:` trailer path the validator appends is
relative to /home/vgpnk/Projects/shokunin/kengaku-shokunin — write it at ...", build-spec.json:5,
falsify-spec.json:5). So no prompt alone lands bytes in the fleet repo; the misroot risk is for reads
(silent wrong-location lookups) if a seat resolves them from the fleet root. Notable: my own item names
`build/swarm-registry.json`, which is (a) relative → fleet-root resolution puts it in the fleet repo, and
(b) wrong even lane-relative — no `build/` dir exists at the lane root; the registry actually lives at
`.ufo/waves/round-31/build/swarm-registry.json` (verified: `ls build` → no such file; file exists at the
wave dir).

VERDICT: Survived — 36+36 members with assignments recorded (spec↔registry name sets identical), zero null
agentIds, build wave full seat-report presence (36/36, committed at dbb07364, no orphans), both waves in
v1 band, attack shares ≥77.8% (falsify) under either named convention; Fell — 35/36 falsify seat reports
absent at audit time (in-flight, tracked), two build seat reports deviate from the landed commit
(`M R31MutCounter.md`, `?? R31DraftGate.md`), and 25 spec items (7 build + 18 falsify) name relative paths
that would resolve into the fleet repo from the fleet root (read refs; no write instruction found).
