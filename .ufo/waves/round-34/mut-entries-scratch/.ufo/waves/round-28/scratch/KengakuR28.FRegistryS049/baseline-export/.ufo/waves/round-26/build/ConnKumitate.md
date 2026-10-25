# Round 26 connector — kumitate overlap

**Axes:** calibration (directly relevant); novelty is not claimed by this overlap scan.

## Evidence and ruling

- Kumitate defines its domain as “orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime” and says it “Refuses” outside-domain work, reporting cross-domain evidence to the orchestrator (`kumitate-shokunin/PROVINCE.md:3-6`). Its governed core names origin `scripts/`, runtime, Kimi substrate, and its own instruments (`PROVINCE.md:12-15`); upstream defects are “filed in lane reports … never patched from here” (`:28`).
- The fleet addendum names the shared validator: validate wave under policy, then issue exactly one task call with its `taskCall` unchanged (`scripts/hyaku/lane-addendum.md:42-50`). `ufo-swarm-wave.mjs` is a dispatch planner: `planSwarmWave` “validates the spec” and returns a plan (`ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:733-744`); its `run` emits the task-call/resume payload and persists member registry (`:43-62`, `planToDispatchPayload` `:1282-1315`). These are topology, prompt, route/policy, and dispatch/registry concerns.
- Q13 instead asks whether an admitting commit’s own tree already contains the Gate-cited Q10 re-read report; it rejects generic “wave-2 seats” support and takes `--lesson` plus `--commit` (`kengaku-shokunin/plans/round-26-claims.md:20-26`). The concrete failure was `8ea41f9`: its Gate already said “by wave-2 seats” before those reports existed (`corpus/lessons/round-25-verifier-spotcheck.md:36-39`).
- There is one narrow shared predicate: the *collector*, not the wave planner, records per-member `reportPresent` when a trusted `reportDir` is declared (`ufo-fsd-alpha/scripts/ufo-swarm-collect.mjs:450-455,593-603`) and emits a present/missing summary (`:719-731`). That is a current collection-time filesystem observation; Q13 is a historical, commit-tree admission check. Neither result substitutes for the other.

**Ruling:** No ownership overlap with Kumitate’s orchestration surface as specified. Q13 is lane-local corpus admission/verification; the shared word “wave” and presence of report files do not make it a dispatch validator. The collector’s report-presence observation is adjacent evidence, not the same temporal claim.

## Proposed bounded move

Keep `plans/gate_timing_check.py` Kengaku-local and make the selected Git commit tree—not current checkout state, mtimes, or dispatch/collector state—the authority for the Q13 timing decision. This prevents a report arriving later from repairing the historical landing fact. If implementation changes `ufo-swarm-wave.mjs`, collector behavior, fleet policy, or OMP task/hub orchestration, report that cross-domain requirement to Kumitate/origin rather than absorbing it (`PROVINCE.md:5-6,28`). This preserves calibration evidence without touching dispatch semantics.

## Risk / contradiction to keep explicit

Q13 promises a *second-seat* re-read, but the pre-registration describes extracting cited paths, requiring a path to exist in the commit, and rejecting generic references (`round-26-claims.md:20-24`); that alone does not establish roster membership, reviewer≠writer, or that the file contains a genuine Q10 re-read. The round-26 Q13 wording review independently flags this interface gap (`.ufo/waves/round-26/build/RevQ13Text.md:5-6`). Do not treat tree presence as proof of review quality; keep Q10 content/independence verification explicit rather than expanding the fleet dispatcher to claim it.

## Verification

Read-only comparison of PROVINCE, SKILL, the round-26 pre-registration, Q13 review evidence, round-25 closure, and the fleet validator/collector source. No checker or wave was run; no source was changed. Installs/updates: none.

VERDICT: Keep Q13 in-lane as a commit-tree admission check; report out only if it requires changing orchestration/dispatch or collector behavior.