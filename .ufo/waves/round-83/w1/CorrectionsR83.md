CorrectionsR83 — coverage/calibration scribe
Recorded 2026-11-04T15:52:19Z (UTC)
BASE 614f00559c75155ec100e945b3e8257b14fb7496
Freeze 6f076679931367d540c3897a4eafa0eca752e1d4

BEHAVIOR / DELIVERABLES
- lesson-corrections.md: complete R82-V1..V8 correction paragraphs, source line mapping, Gate supplement for historical S265/S266 omissions, and eight-row mistake table with class/evidence/captured-by/fix. Not a product edit or an assertion of discharged gates.
- readme-rows.md: replace malformed round81 outside-spotcheck row; add round82 lesson and round82 outside-spotcheck rows, all three cells. Install in Lessons before Knowledge table. Do not duplicate an already-integrated row.
- skill-registry-rows.md: four proposed complete eight-cell rows: round83-code-image-probe, round83-c1-replay, round83-c2-debt, round83-c2-checks. These are frozen-contract drafts, not observations of executable implementations. Probe/checks have no separate selftest declared by the frozen contract; counter selftests are not inherited. No run tallies claimed.
- r82-seat-counts.json: full machine-readable V3 receipt in agreed DebtR83 schema, ready for installation as corpus/evidence/round83/r82-seat-counts.json subject to path reconciliation below.
- mechanical-counts.json: actual extracted selftest cells and output category names.
- derivation-receipt.json: exact Git argv, derivation algorithms, UTC timestamp, original report hash.

OBSERVED FINDINGS
1. Frozen SKILL bytes mechanically yield ten specified round82 additions, seven selftest declarations, three none-declared exceptions: round37-c1-attribution, round80-c1-remint, round82-c2-checks. These are declarations, not successful execution evidence.
2. Frozen results bytes mechanically yield seats=12, final_terminal=10, final_empty=1, final_unstructured=1. Empty: SweepGateR82. Unstructured: RegistryCounterR82. Source SHA256 e9cb0af961345c30563fb025e8e867dfa92723071d5ef5221182da4bfdf944bc.
3. The outside spotcheck names six historically affected identities. Unrecovered=2, recovered=4 is the report/spotcheck recovery classification, not an inference about provider events from final outputs. Four recovered: SweepHarvestR82, ReviewerR82, CriticR82, MutationR82.
4. Git --diff-filter=A returns 82fe89d5dd29fa4c1bb8d85399d9e43442d1b862 for the two round82 C2 tool paths. Exact argv and output summary are retained in derivation-receipt.json and lesson fragment.
5. Explicit correction: 07:24-03:00=10:24Z; round83 report timestamps UTC. Approximate historical time remains approximate.
6. Actual historical report lives at fleet .ufo/reports/round-82/kengaku.md, not lane. Reading the guessed lane-relative report failed; L1 supplied the actual location. SHA256 observed 5a83443dc6544a76633ee42b90394cb1028a1abab18ee69ff54a4857758b0480, matching L1's communicated preservation hash. This is a single observed hash, not an independent before/after preservation proof.
7. Exact V source lines: V1 161; V2 168; V3 173; V4 178; V5 182; V6 187; V7 192; V8 195.

GATES / EXECUTION BOUNDARY
No build, lint, general tests, gate, counter, selftest, mutants, controls, census or replay was run. No new C1/C2 pass is claimed. Static derivation used functions.eval Python and read-only git show/log. HEAD read returned frozen commit; no Git mutation. At the initial explicit presence observation all four shared ReplayR83/CounterR83/DebtR83 script paths were absent; no validation against those scripts is claimed. No tool installed or updated. No pacman transaction, service restart, config edit or other runtime launch. TMPDIR explicitly set to private scratch; no clone needed.

INTEGRATION CONFLICTS / LIMITS (report, do not judge)
- DebtR83 accepted literal fragments in lesson-corrections.md, but L1 independently integrated a lesson with semantically equivalent different literals (notably V1 and V7). DebtR83 was notified; its substantive checks must not falsely require an unused draft literal. This seat does not change judge/predicate/checks.
- DebtR83 agreed receipt path corpus/evidence/round83/r82-seat-counts.json; observed L1 lesson instead refers to corpus/evidence/round83/r82-seat-census.json. DebtR83 notified to reconcile source path/check/install, not silently validate a different receipt.
- SourcesR83 supplied a fresh Gate draft with access evidence; prefer its Gate.proposed.md for source integration. This seat's Gate supplement deliberately labels historical access records and uses the exact eight-token vulnerable-secret substring rather than dropping backticks from a longer quote. Peer fetches are not this seat's executions.
- Registry rows are contract-grounded proposals: L1 must reconcile actual declared flags, exact exit maps and write scope against final instrument bytes before installing; they are not executable evidence. No fake successful battery counts appear.
- L1's observed production mistake table uses rule names under captured-by, whereas this draft names the actual outside spotcheck. Retain the outside capture provenance rather than implying a lane self-catch.
- V2 after-census execution/receipt and SOURCE row repairs belong to other seats/L1. This scribe does not fabricate or duplicate their execution.

TOUCHED SURFACES
Only authorized .ufo/waves/round-83/w1/CorrectionsR83/ outputs plus the required sibling report CorrectionsR83.md. Private scratch created for TMPDIR and removed before yield. No production/domain/fleet tracked file changed; historical round82 lesson/report/LOG/SCORECARD untouched. No commits, push, index, refs, fleet metadata or runtime controls changed.

SELF-EVALUATION (not admission)
Accuracy 4: historical arithmetic/provenance grounded; new registry implementation details remain contract-only.
Completeness 4: all eight corrections, mistake table, README/registry fragments and mechanical counts delivered; integration paths/literal wording require L1 reconciliation.
Clarity 4: draft versus measured boundaries explicit; multiple evidence paths need careful integration.
Actionability 4: complete fragments and V3 JSON supplied; L1 owns final implementation/installation and gates.
Conciseness 4: intentionally repeated provenance boundaries avoid execution overclaims.
Overall 4.0. Improvement priority: resolve receipt filename, then bind registry cells to final code. Would user agree: likely, provided these remain drafts rather than claimed passing repairs.

ARTIFACT ROOT
.ufo/waves/round-83/w1/CorrectionsR83/
Report .ufo/waves/round-83/w1/CorrectionsR83.md
