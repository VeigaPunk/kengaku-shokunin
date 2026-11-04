# ConnectorR79 — sibling-overlap scan

## Scope and axes

Axes: **coverage** (R79-C1, capped at 7) and **calibration** (R79-C2, held at 10). Read the entire frozen `plans/round-79-claims.md` before commands and read `PROVINCE.md` §Refusals. No predicate, target, control, kill rule, counter, or domain artifact changed. Lane `master` observed as `42d9d60a32d4fee74297c16ba6b5dc1b8ade9f4a`; sibling citations below refer to the locally observed files, not a synchronized fleet snapshot.

Twenty sibling repositories were enumerated under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding kengaku). Searches were issued separately against every concrete repository, case-insensitively, respecting gitignore, excluding `.ufo` and `corpus/SOURCES.md` for the broad analogue scan. Patterns: `population[- ]ledger|per[- ]member|member[- ]ledger|benchmark population|grader population|routed[- ]defect|discharge[- ]gate|blocker[- ]taxonomy|closure[- ]debt|routed.findings`. Follow-up targeted reads distinguished executable mechanisms from prose. An initial wildcard-path grep returned no matches; it was not used as negative evidence and was replaced by the twenty concrete-root searches.

## Closest analogues

Paths in this section are relative to the named sibling repository.

1. **Population accounting plus honest per-member blockers: audio.** `audio-shokunin/corpus/fixtures/measure_audio.py:1494-1498` explicitly records missing ffmpeg/failed synthesis as per-member blockage, lets hand-built members run, and refuses fabricated substitutes. `:185-187` identifies a complete tracked autodetect family and explicit per-member transport recording. This is a finite audio-format population, not TB2 grader members, grader-class pairs, subject-stamped replay receipts, or the frozen four-detector taxonomy. Closest *population-integrity* analogue, not a second grader ledger.
2. **Derived obligations plus typed repair pointers: kagi.** `kagi-shokunin/corpus/closure-dispositions.py:2-10,21-27` parses a closure, requires exactly one typed disposition per obligation, and resolves a fixed pointer carrying its obligation id. Crucial difference: `:41-46` expressly disclaims rerunning fixes or establishing that fixes work. Thus this is closest to C2's obligation-ledger structure, but it cannot replace C2's executable repair checks.
3. **Red-base/green-tip routed repair gate: kotoba.** `kotoba-shokunin/verifiers/check_r64_routed_repairs.py:2-13` requires four routed repairs, refuses certification unless the pinned base scores zero, and derives evidence from committed blobs. It is the closest *behavioral* C2 analogue. Its domain-specific four checks are not the seven R78-D rows or C2's schema.
4. **Evidence-derived blocker/failure taxonomy: kumitate.** `kumitate-shokunin/corpus/knowledge/route-probe-cluster.md:222-227` names the route failure classes and classifier; `:229-236` separately defines persisted-health statuses/reasons. The important adjacency is the separation of reason, health, and cleanup, not reuse of its operational vocabulary as grader prerequisites. These classify observed routing failures; C1's detectors classify text in captured grader bodies. Neither establishes the other's runtime facts.
5. **Population/denominator consistency: mado.** `mado-shokunin/SKILL.md:723` registers a checker comparing parsed denominators, CASE-line counts and registered totals; `:733` registers population/readers/guarded counts. Useful census analogy, but neither records execution status for the TB2 grader population.

## Lane × artifact matrix

“Adjacent” means a concrete shared mechanism, but different subject universe or contract; “disjoint” means the located material concerns another product domain and did not establish one of the three requested artifacts. Generic use of words such as member, ledger, probe or routed defect is not artifact identity. Every path below is rooted at `/home/vgpnk/Projects/shokunin/`.

| Lane | Classification against R79 artifacts | Evidence |
|---|---|---|
| audio | adjacent artifact | `audio-shokunin/corpus/fixtures/measure_audio.py:1494-1498`: honest per-member synthesis blockage, not grader census. |
| chousa | adjacent artifact | `chousa-shokunin/corpus/QUALITY.md:931`: routed defects carried through two closures must land with a test or retire with a reason; research-method debt, not R78-D closure rows. |
| game-dev-2d | disjoint | `game-dev-2d-shokunin/PROVINCE.md:3,10`: game-production fixtures; harness/evidence auditing expressly routed elsewhere. |
| game-dev-3d | adjacent artifact | `game-dev-3d-shokunin/SCORECARD.md:307`: five routed repairs with before-fail/after-pass receipts; engine-domain repair evidence, not C2's ledger schema. |
| kagi | adjacent artifact | `kagi-shokunin/corpus/closure-dispositions.py:21-27,41-46`: typed obligation ledger/pointer checks, expressly no repair rerun. |
| kaidoku | adjacent artifact | `kaidoku-shokunin/SKILL.md:986`: strict routed-defects gate over six R17 defects; reverse-engineering debt, not R78-D1…D7. |
| kake | adjacent artifact | `kake-shokunin/SKILL.md:1188-1192`: gate-registry addition and committed verification pointers for routed defects; publishing-domain evidence. |
| kama | disjoint | `kama-shokunin/PROVINCE.md:3-4`: serving/endpoint health, not static grader prerequisites; generic repair discussions do not establish the requested ledger. |
| kasegi | adjacent artifact | `kasegi-shokunin/SKILL.md:1151,1154`: routed-defects counters derive fixed/unresolved limbs, return zero only when unresolved is zero; different debt universe. |
| kotoba | adjacent artifact | `kotoba-shokunin/verifiers/check_r64_routed_repairs.py:2-13`: committed-blob repair checks and red-base requirement, not C2's seven-id ledger contract. |
| kotodama | adjacent artifact | `kotodama-shokunin/LOG.md:4256`: exact ten routed ids, uniqueness and correction-record accounting; fictional-language/culture debts rather than grader members. |
| kumitate | adjacent artifact | `kumitate-shokunin/corpus/knowledge/route-probe-cluster.md:222-236`: classified route failures and separate persisted-health reasons, not grader-text dependency detectors. |
| lore | disjoint | `lore-shokunin/PROVINCE.md:3,9`: fictional entity/timeline consistency and canon boundaries; per-member dependency loops are not benchmark-population ledgers. |
| mado | adjacent artifact | `mado-shokunin/SKILL.md:723`: registration/denominator/CASE population checker, not TB2 member-status accounting. |
| mori | adjacent artifact | `mori-shokunin/PROVINCE.md:589-590`: routed-defect gates recheck committed Git objects, but for mori R23/R24 obligations. |
| revenger | disjoint | `revenger-shokunin/PROVINCE.md:3-7`: shipped-artifact observation/inference/unknown evidence ledger; not benchmark membership or C2 discharge. |
| souji | adjacent artifact | `souji-shokunin/PROVINCE.md:14-15`: preservation ledger binds source/vault paths and hashes; structural ledger analogy, not grader execution or mission state. |
| tabi | adjacent artifact | `tabi-shokunin/LOG.md:1649`: six routed defects made mechanical; browser-domain debts rather than C2's source/repair/check rows. |
| tameshi | adjacent artifact | `tameshi-shokunin/PROVINCE.md:3-5,14-17`: reusable hermetic/mutation/before-after method; explicitly leaves each lane's gate with that lane. |
| tsukuroi | disjoint | `tsukuroi-shokunin/PROVINCE.md:3-4,8-14`: package/systemd/driver/boot substrate; not the grader population or dependency semantics. |

### Duplicate count and explicit contradiction

**Exact R79 artifact duplicates observed: 0.** Additional searches against all twenty concrete sibling roots for `grader-population-ledger|round79_c2_closure_debt|no-subject-stamp|browser-required|candidate-library-required` returned no matches (gitignore respected; `.ufo` and `corpus/live` excluded). Broad analogue searches likewise did not establish another lane owning this TB2 subject universe or R78-D1…D7 closure contract. This is bounded repository evidence, not proof about ignored files, future changes, or every semantically equivalent implementation.

**A stronger interpretation of “expect 0” is contradicted.** If “same artifact” means the generic artifact class *machine-checked routed-defect discharge gate*, kotoba, kasegi and mori already have that class (citations above): three independently named lanes, therefore at least three unordered lane-pair duplications. Kagi additionally has a non-executing obligation-disposition analogue. Zero exact-domain duplicates must not be reported as zero mechanism overlap or novel general-purpose verification craft. The matrix uses exact contract/subject identity; under the coarse artifact-class interpretation those three entries become “same artifact.” This is not a scalar disagreement to average away.

## Province leakage: concepts and dispositions

Frozen claim anchors: C1 membership/status/receipt semantics `plans/round-79-claims.md:15-24`; blocker detectors `:57-64`; C2 source/close/check `:96-101`; source taxonomy `:143-145`.

| External province | Claim concept / actual boundary | Disposition in this report |
|---|---|---|
| kotoba — prompt/skill craft | C1 updates derived cells in `SKILL.md`; that is evaluation content, not trigger/render/prompt-craft authority. No prompt intervention is claimed. | Keep measured counts local; reusable wording/decision-table craft goes out to kotoba, not absorbed. |
| kumitate — route resolution / operational failure taxonomy | The words “routed defects” and “blocker” occur, but C2 routes review debt and C1 detects grader prerequisites; neither is model-route resolution, fallback policy or live launch-failure classification. | Report operational analogues out informationally; never map C1 reason strings into route policy. |
| kama — serving plane | Harness container/network model and VM prerequisites are not serving flags, slots, model identity or endpoint health. No serving-plane change or measurement appears in either claim. | No serving-plane finding asserted; any actual service-health/configuration consequence belongs to kama/operator. |
| kagi — secrets | Tracked receipts and check commands are evidence surfaces, not permission to inspect credentials. Neither frozen claim names a secret, credential flow or vault operation. | No secrets finding asserted or absorbed; credential material would be reported out, never copied into the ledger. |
| kasegi — ledger mission state | `executed`, `executed-unlocated`, `unexecuted` describe captured evaluation evidence; `closed` describes review repair debt. Neither updates bounty mission state, dispatch, submission or leases. | Report shared ledger idiom, retain evaluation-only state semantics; mission-state authority stays out. |
| kake — web properties | `browser-required` is a frozen Selenium-token detector over grader text, not a claim about benchmark sites, a browser run, deployment or web correctness. | Report any real web/deployment issue out; do not “fix” sites to satisfy a static ledger. |
| tabi — browser interaction | The same `browser-required` label does not authorize launching/driving a browser or handling a browser profile. | Runtime browser-interaction craft remains tabi's; only source-text dependency accounting stays local. |
| tameshi — verification craft | Controls, mutant matrices, red-base/green-tip and nontrivial checks are reusable verification concepts. | Own lane-local counters, not a new fleet verification method; report the cross-lane pattern out. Its explicit boundary is `tameshi-shokunin/PROVINCE.md:14-17`. |
| chousa — source research method | SOURCES curation and source/claim linkage use research/citation craft. | Keep domain-specific interpretation; report general research-method implications out, not a competing method. |
| tsukuroi / protocol-integrator | Container/network/VM prerequisite vocabulary touches host substrate; the census contract and any fleet-wide ledger standard exceed a lane. | No host remediation or fleet standard imposed. Route those implications out through the orchestrator. |

**Existing province contradiction:** kengaku `PROVINCE.md:26-27` calls the serving plane unowned, while its later Adjacent map at `:158` assigns serving-plane health/detection and endpoint identity to kama, consistent with `kama-shokunin/PROVINCE.md:3-4`; that later row still reserves flag-change authority to the integrator. Preserve this as historical versus later ownership text; do not use the older refusal to acquire serving authority. No province correction made here.

“Report out” above means explicit routed recommendations in this report for the orchestrator; no sibling was messaged and no handoff delivery beyond this report is claimed. Negative entries do not invent a cross-domain defect merely to fill a routing table.

## One bounded connecting move

**Proposed move:** carry an evaluation-only scope note alongside the existing population-ledger explanation: distinguish *static prerequisite classification*, *subject-located execution evidence*, and *repair checks*; cite the audio member-blockage analogue, kagi's non-executing disposition limit, and kotoba's red-base/green-tip gate. Report the reusable synthesis to tameshi/protocol through the orchestrator; do not copy their implementations or add ledger fields, detectors, controls or frozen requirements.

- **Evidence:** audio `measure_audio.py:1494-1498`; kagi `closure-dispositions.py:41-46`; kotoba `check_r64_routed_repairs.py:4-13`; the frozen C1/C2 anchors above.
- **Affected axes:** calibration can improve through a precise boundary on what “blocked,” “executed” and “closed” prove; coverage's 88-member/16-class accounting remains unchanged. This is a proposed interpretive improvement, not an observed score increase or admission.
- **Second-order effects:** runtime — no new browser/VM/service execution; contract — preserve all frozen statuses, subject shapes and predicates; substrate — no provisioned dependencies, configuration or secrets access; verification — do not mistake pointer resolution for repair efficacy or source-token detection for runtime impossibility.
- **Risks:** shared vocabulary could hide generic mechanism duplication; an annotation could overstate actual handoff, runtime unavailability or fleet ownership. Explicit distinctions and scoped citations avoid these harms without reopening the claim.
- **Verification for integrator:** review that the scope note adds no counter requirement; retain the frozen C1/C2 before/after, mutants and controls; check that no source-only blocker sentence asserts runtime necessity and no pointer-only closure is described as executable repair evidence. These checks were not executed by this connector.

## Evidence and execution limits

Only reads, searches and one read-only `git rev-parse master` were performed. No model/browser/service runtime, counters, fixtures, tests, installs, updates, git mutations, source edits or sibling messages. No scratch was created, so no scratch cleanup remained. Only this assigned report was written.

Self-evaluation (report only): accuracy 4/5 — citations are observed local bytes, not a fleet-wide revision-pinned snapshot; completeness 4/5 — all twenty repos searched, but ignored files and semantic equivalents are not exhaustively excluded; clarity 4/5 — exact-artifact versus generic-pattern duplicate definitions must remain explicit; actionability 4/5 — one bounded documentation/report-out move, intentionally not integrated; conciseness 4/5 — the twenty-row census and province audit require length. Mean 4.0. Main improvement: pin sibling revisions if a synchronized historical duplicate claim is needed; no such claim is made here. The user should agree with these stated limitations.
