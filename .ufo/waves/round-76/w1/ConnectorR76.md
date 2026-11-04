# ConnectorR76 — cross-lane instrument scan

## Scope and axes

Axes: **coverage** (C1 declaration-to-live-verdict coverage) and **calibration** (C2 closure-to-evidence correspondence). Read the frozen `plans/round-76-claims.md` in full first. No predicate, target, control, kill rule, production file, or sibling file was changed. No gate, selftest, another runtime, or dispatch was invoked. This is a source/evidence scan, not an admission or score.

## What ran and observed output

All commands below ran with cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`:

1. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -e 6977019bdf56a88921e14f728167da8f5726c1fc:corpus/evidence/round76/r74-c1-tip.txt` — **exit 128**:

   `fatal: path 'corpus/evidence/round76/r74-c1-tip.txt' exists on disk, but not in '6977019bdf56a88921e14f728167da8f5726c1fc'`

2. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -e 6977019bdf56a88921e14f728167da8f5726c1fc:corpus/evidence/round76/r74-c2-tip.txt` — **exit 128**:

   `fatal: path 'corpus/evidence/round76/r74-c2-tip.txt' exists on disk, but not in '6977019bdf56a88921e14f728167da8f5726c1fc'`

3. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log master --format=%H --diff-filter=A -- corpus/evidence/round76/r74-c1-tip.txt corpus/evidence/round76/r74-c2-tip.txt` — **exit 0**:

   `f0d5232208d45a8e3ba120ceb2b12a3c5f627137`

4. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree f0d5232208d45a8e3ba120ceb2b12a3c5f627137 -- corpus/evidence/round76/r74-c1-tip.txt corpus/evidence/round76/r74-c2-tip.txt` — **exit 0**:

   `100644 blob fd64d03a40bf1b27dc9265862a67b4c7b4fd40a1 corpus/evidence/round76/r74-c1-tip.txt`

   `100644 blob 12ea39f6c0c237c5bfd328590d2d2b6a1f93151a corpus/evidence/round76/r74-c2-tip.txt`

   (The separator before each path in actual git output is a tab.)

Discovery used `read`, `glob`, and `grep`, not shell searches; these tools have no process exit code. Searches covered lane tools/scripts/verifiers/plans and corpus-root/instruments, plus filename searches for surface/debt/defect/closure/citation/ledger/disposition/freshness. Excluded other seats' `.ufo/waves`, state, watchdog and scratch contents. Early fleet-root searches respected gitignore and mainly found fleet records; explicit `*-shokunin` path searches with `gitignore:false` supplied the sibling evidence below. Broad searches were paginated/narrowed; no claim of semantic exhaustiveness over every historical fixture is made.

Representative exact search inputs:
- `grep(pattern="routed.findings|close_commit|fixed-verified|surface.{0,25}(resolv|census)|resolv.{0,25}surface", path="/home/vgpnk/Projects/shokunin/*-shokunin/**/*.py;/home/vgpnk/Projects/shokunin/*-shokunin/**/*.sh;!**/.ufo/**;!**/.scratch/**;!**/.git/**", gitignore=false)`
- `glob(path="/home/vgpnk/Projects/shokunin/*-shokunin/**/*surface*;/home/vgpnk/Projects/shokunin/*-shokunin/**/*debt*;/home/vgpnk/Projects/shokunin/*-shokunin/**/*defect*;/home/vgpnk/Projects/shokunin/*-shokunin/**/*closure*;/home/vgpnk/Projects/shokunin/*-shokunin/**/*citation*", hidden=false, gitignore=false, limit=300)` (tool clamped limit to 200; supplemented with targeted reads/searches).
- `grep(pattern="receipt|ledger|stamp|ancestor", path="/home/vgpnk/Projects/shokunin/PROTOCOL.md;/home/vgpnk/Projects/shokunin/PROTOCOL-APPENDIX.md;/home/vgpnk/Projects/shokunin/CORPUS.md", gitignore=false)`.

## Numbered findings

### 1. MEDIUM — measurement revision and closure-bearing commit are different facts

Pointer: `corpus/routed-findings.jsonl:85` (R75-D6 as read), `plans/round76_c2_defect_discharge.py:295-307,331-346`; sibling precedents `souji-shokunin/tools/souji-citation-reconcile.py:25-35`, `tameshi-shokunin/tools/receipt-commit-bind.py:8-16,34-39`.

The actual row bytes include `"id": "R75-D6"`, `"status": "closed"`, and `"close_commit": "6977019bdf56a88921e14f728167da8f5726c1fc"`; its close text says the two r74 receipts were produced at that revision. Both receipts are absent from that commit (commands 1–2) and present at `f0d5232208d45a8e3ba120ceb2b12a3c5f627137` (commands 3–4).

**Contradiction:** production C2 checks receipt content in the selected/current tree and checks close-commit ancestry separately. An ancestor can predate the very receipt offered as closing evidence. Ancestry is not evidence-at-commit. This is a provenance counterexample, **not a claim that the frozen C2 predicate fails**, and no C2 pass was run or asserted here.

### 2. INFO — overlapping primitives already exist; R76's increment is narrower than their broad capability names

Paths below are fleet-relative. Each classification concerns the named overlapping leg, not ownership of all the lane's work. No sibling implementation was executed.

| Lane / existing file (lines) | Existing primitive / exact overlap | Disposition and R76-only leg |
|---|---|---|
| kengaku `plans/round51_surfaces.py:2-23,93-139`; `plans/round51-surfaces.json:5-10` | Per-declared-table-row manifest, live path/digest/TCP/HTTP probes, prose/state/dated-absence agreement, counts and resolve floor. Direct C1 prior. | **increment**: C1 extracts anchors and stale prose from current table bytes instead of trusting a separately authored `prose` field. Not first live surface resolver. R51 HTTP requires 200 and all path targets; R76 accepts any HTTP response and any brace alternative: preserve the frozen distinctions. |
| kagi `corpus/surface-census.sh:2-38,71-72`, TSV + state-shape files | Declared host asset/runtime set re-resolved; kind/mode/schema checks and undeclared-child discovery. | **report-out** host shape/discovery to kagi; **increment** only C1's direct PROVINCE dated-marker/prose agreement, which this TSV census does not parse. |
| kagi `corpus/claim-ledger.sh`; `SKILL.md:45-47` | Persisted file stamps, claim reruns, citation/cell auditing. | **report-out** reusable stamp/cell audit; C2's seven particular native derivations remain an **increment**, not a replacement claim ledger. |
| kagi `corpus/closure-dispositions.py:2-47` | Pinned closure obligation set, exactly one typed disposition and resolving fixed pointer. Explicitly does not rerun fixes. | **report-out** disposition coverage/pointer leg; **increment** C2 live value derivation and ancestry. Do not call kagi's fixed-pointer success verified repair. |
| kumitate `scripts/surface-probe.mjs:3-28,38-95` | Live manifest/status resolution, disk-derived digest set and source-vs-declared verbs; checklist exit plus substring verification. | **report-out** orchestration surface conformance; **increment** direct PROVINCE-row absence agreement, not manifest/digest verification. |
| kumitate `scripts/routed-ledger.mjs:9-30`; `corpus/routed-ledger.md:3-9` | All routed sections/items in a round range; located unique source quote; closed/wontfix answers bound at exact file:line; rejects contradictory rows and escapes. | **report-out** durable queue and source/answer binding; **increment** C2 native recomputed values and close-commit ancestry. Exact answer-line binding is stronger than C2's token-window correction leg, not something C2 already replaces. |
| kama `tools/kama-probe.sh:2-41` | Re-resolves registered consumer baseURLs from config, reconciles endpoint/model identity and liveness. | **report-out** model readiness/identity. **increment** C1 row declaration agreement only. HTTP response presence must not be promoted to MODEL_OK/readiness. |
| kama `tools/round73-province-host-drift.py`, `tools/round74-province-host-drift.py` (registry `SKILL.md:316,319`) | PROVINCE host identity reconciled against live OS/architecture/distribution; v2 preserves recorded-at revision blocks. | **report-out** host-identity truth; **increment** C1 path/HTTP surface census. |
| kama `tools/round69-newest-closure-counter.py:4-47` | Newest closure derived from committed candidates, date/round order, checks latest-outside-closure pointer. | **report-out** chronological closure freshness; C2's highest-round scope selection is narrower and must not be described as the same date-based algorithm. |
| kama `tools/round72-receipt-tip-binding.py:8-11,60-78`; successors `round73-receipt-claim-binding.py`, `round74-receipt-claim-binding.py` (registry `SKILL.md:313,315,318`) | Receipt exists at tip, measured header revision ancestor, intervening changes restricted; successors bind explicit/paragraph claims. | **report-out** measurement-versus-landing receipt binding; **increment** only C2's lane-specific discharge values. |
| kotoba `verifiers/verify_surfaces.py:4-9,58-108` | Loader-derived instruction-class set parity against declared governed/excluded inventory and literal presence. | **report-out** instruction-class discovery; **increment** C1 actual path/endpoint existence and dated absence, not proof a loader fires at runtime. |
| kotoba `verifiers/check_host_skill_surfaces.py:2-28` | Enumerates installed SKILL surfaces, compares lane hashes, classifies absent/drifted/identical; drift itself does not fail. | **report-out** host instruction-copy census; **increment** C1 declaration-truth gate. Do not flatten its probe success into no drift. |
| kake `scripts/freshness-sweep.mjs:2-28`; `SKILL.md:189-205` | Rechecks cited filesystem paths and per-occurrence absence annotation; history and pinned HTTP standing claims. | **report-out** whole-document citation/live-web drift; **increment** C1's bounded Surfaces table plus exact dated-marker/stale-text rules. |
| kake `scripts/ledger_latest_check.py:1-53` | Re-derives latest declared score/ratio figures from committed receipts. | **report-out** general receipt-to-self-description arithmetic; **increment** C2 specific R75-D1…D7 scope and register/ancestry integration. |
| mado `tools/mado-verify.sh:3-42` | Declared config/source sets versus live file and available compositor state, exact membership and UNKNOWN blocking clean. | **report-out** desktop config-plane semantics; **increment** C1 table declaration truth, not config correctness. |
| mado `quality/check-tool-ledger.py:2-45` | Tree-derived instrument population, one row per tool, resolving accountability pointers, no empty-population pass. | **report-out** inventory completeness; adjacent but not a routed-defect close verifier. |
| kasegi `corpus/instruments/r-defect-closure.sh`, `r35-defect-closure.sh`, `r36-closure.sh`…`r43-closure.sh`; `r44-routed-defects.py:4-9,68-70`, `r45-routed-defects.py:4-46`, `r47-routed-defects.py:4-37,45-49` | Per-defect/substantive-evidence closure limbs, committed-content checks, capture/code pins, counts and attributed hostile fixtures. Direct C2 prior family. | **report-out** closure-counter/content-binding method; **increment** C2 integrating its own newest closure into its standing ledger with native values plus ancestry. Do not advertise substantive closure checking as new to the fleet. |
| souji `tools/souji-citation-reconcile.py:10-39` | Register row binds expected token to citation and committed SUMMARY receipt; optional commit must resolve, be ancestor, be cited, and itself contain agreeing receipt. | **report-out** receipt-at-commit provenance. **increment** C2 native recomputation rather than only receipt-token comparison. This is the compatible leg behind finding 1. |
| tameshi `corpus/routed-defects.json:2-18` | Typed routed-defect register, evidence excerpts/ranges and commit fields; note names its r50 measurement instrument. | **report-out** register precedent. Verification of that historical instrument was not performed; do not infer a rerun from a status field. |
| tameshi `tools/evidence-disposition.py:4-13,15-38,48-60` | Frozen expected checks accounted exactly once; retained raw receipts re-evaluated after digest verification, historical input commit ancestry. Explicitly not command rerun evidence. | **report-out** receipt integrity/disposition binding; **increment** C2 executing value derivations at check time. |
| tameshi `tools/receipt-commit-bind.py:8-16,24-49` | Checks that commits naming receipt content actually carry that content; direct counterexample precedent for finding 1. | **report-out** named-commit content binding; no new reusable checker required in kengaku. |
| kotodama `reports/round-43/calib/defect-queue-v2-successor-r43.json:6-20,24-32`; parent r40 queue | Append-only pinned-parent successor queue; fixed-with-evidence versus routed-with-owner versus recorded/could-not-recover. Example verification still says OWED. | **report-out** queue/disposition precedent, **not** proof that all fixes reverify. **increment** C2 executable seven-leg discharge. |
| kotodama `tools/check-supersession-settlement.py:4-41` | Derives settled/pending correction chains from current registry status and used-by evidence; validates disposition ledger consistency. | **report-out** source-registry settlement; **increment** C2 routed closure and commit legs. Distinct debt populations, not one shared schema. |
| kengaku `plans/defect_ledger.py:2-18`, `plans/routed_open.py:2-31`, `plans/round51_routing.py:2-17,38-42,126-153`; r69/r70/r71/r72 `*_c2_routed_defects.py` | Already has persistent rechecked defect ledger, routed-open burn-down, owner/disposition attribution, fixed-verified check execution, historical resolving close refs, and subsequent closure-specific legs (r72 header:25-39). | **increment** C2's newest-seven registration, nontrivial-check constraint, explicit close_commit three-state ancestry and named native derivations; not a first persistent ledger/burn-down. Keep existing ledger field conventions. |

`kotoba/verifiers/check_cn_vendor_surfaces.py:10-14,101-108` is a committed vendor-document backing counter, not live endpoint/path resolution; `kaidoku/tools/round-40/ledger-status.py:2-13` only classifies seat-report presence, not verified defect closure. These filename hits were screened out of direct overlap. Domain-specific live audio/game fixtures were not treated as fleet declaration resolvers merely because they use the word surface.

### 3. INFO — fleet standards exist for semantics/interface, not one universal JSON defect schema

Authoritative local quotes:
- `PROTOCOL.md:119-121`: a cited hash absent from the repo fails verification; a hash not ancestor of closure HEAD is a conformance defect, with `git merge-base --is-ancestor <hash> HEAD` as the check.
- `PROTOCOL.md:244-248`: aggregator keeps an **open routed-defects row** until the owning correction lands; “The ledger row, not round notes alone, is the durable queue”.
- `PROTOCOL.md:334-341`: canonical aggregator ledger is `.ufo/reports/AGGREGATE.md`; refresh is append-only with explicit supersession. This is ownership/routing, not permission to create a second fleet queue here.
- `PROTOCOL.md:352-359`: numeric claims carry counting command; endpoint claims need real-surface probe; evidence pointer must resolve at closure, not just write time.
- `PROTOCOL.md:390-397`: “A verdict names the revision it was measured against”; snapshot inputs have digest pins. This does **not** say a receipt must already exist at its measurement revision.
- `PROTOCOL.md:380-389,398-404`: declared exit mapping, isolated selftests with stable expected finding IDs; eight registry fields in lane SKILL; “a fleet index is pointers to lane rows, never copied expected values.”

No universal JSONL field schema or universal `LANE_TIP` header spelling was found in these standard sections. `close_commit` is this lane's instrument schema; `LANE_TIP` must not be passed off as a fleet-mandated byte spelling. R51's FIELDS/dispositions remain the existing local schema precedent.

## One bounded proposed move and arbitration

**Move: report out the existing souji/tameshi receipt-at-commit leg, and separate D6's measurement stamp from its closure-bearing commit in the R76 record.** Preserve the receipts' measured `6977019b…` stamp; recommend D6 `close_commit` name the receipt-bearing `f0d5232208d45a8e3ba120ceb2b12a3c5f627137` (or an explicitly evidenced later landing commit), with human close text stating both roles. Cite the sibling primitives rather than building another receipt checker or changing the frozen C2 predicate.

**One arbitration:** the integrator must choose whether `close_commit` denotes the correction's evidence-bearing landing or only the measured/source revision. Recommend evidence-bearing landing. If choosing the weaker interpretation, state it expressly and do not describe ancestry as proof the closing evidence exists at that commit. No ownership arbitration is otherwise needed: model identity → kama, instruction inventory → kotoba, host security shape → kagi, orchestration manifests/queues → kumitate, lane-specific PROVINCE/defect predicates → kengaku.

Second-order effects:
- Runtime: no new runtime dependency, no sibling tool execution, no live-surface mutation.
- Contract: no altered frozen target/control/kill rule; only a more truthful existing row and explicit provenance terminology. C1 and its HTTP/test-e semantics remain untouched.
- Substrate: uses existing lane git objects; original measured receipt bytes and stamps stay intact; no copied expected-value cache.
- Verification: ancestry and receipt-at-commit existence become separately legible facts. Calibration improves by eliminating one observed provenance ambiguity; coverage is unchanged, not traded away.

Risks: record paths/headers may be host-specific; sibling command-line contracts do not directly accept R76's corpus receipt paths. Do not invoke them blindly or normalize away measurement stamps. A later receipt-bearing commit alone does not prove intervening executable inputs stayed invariant (kama's stronger delta leg remains a separately owned concern). This proposal does not assert content-at-commit binding is already in the frozen C2 kill rule.

Integrator verification (not run by this seat): check chosen close_commit ancestry against landing tip with all three exit states distinguished; `git cat-file -e <close_commit>:<each-r74-receipt>` must exit 0; inspect receipt headers to retain their original measurement revision; run the frozen C1/C2 commands through the assigned replay seats and retain their actual receipts. No new gate is proposed.

## Could not verify / hygiene

No C1/C2 pass, sibling gate pass, historical tameshi r50 verifier pass, full cross-fleet historical-fixture exhaustiveness, or final-tip invariance is claimed. Production files were changing during the wave; file:line references describe the bytes read, while the explicit commit/path observations above are immutable. No scratch tree, clone, fixture, tool installation/update, or PATH change was created, so no scratch cleanup or install record is owed. Only this findings file was written.
