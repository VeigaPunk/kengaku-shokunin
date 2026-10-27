# R44ConnSibling — sibling overlap scan (kengaku round 44 connector)

Seat: R44ConnSibling · round 44 wave (hyaku run 9) · 2026-10-26 · leaf seat, no subagents.
Scope: sibling lanes' `PROVINCE.md` + `corpus/README.md` (all 20 sibling lanes; kengaku excluded as
self). Topics scanned: cryptanalysis, benchmark-grader auditing, answer-leak detection,
mutation-attributed gate testing. Read-only scan: no counters/probes/batteries were run, so no
envelope lines apply; no tools installed; no scratch dir created (nothing written outside this
report).

## Method (evidence commands)

- `read /home/vgpnk/Projects/shokunin` — fleet root listing: 21 physical `*-shokunin` lanes.
- topic greps (case-insensitive) over all 20 sibling PROVINCE.md and all 20 corpus/README.md:
  crypt|feal|cipher|xor|s-box|krypto|affine; grader|grading|benchmark|terminal-bench|tb2|
  test_outputs|task-deps|pytest; leak|cheat|bypass|decoy|substring|ground truth|answer key|
  contamination; mutation|mutant|battery|attributed|kill|surviv.
- Full reads of tameshi, revenger, kasegi, kumitate, chousa PROVINCE.md; tameshi corpus/README.md
  head+frontier; kotoba PROVINCE.md grep for kengaku/eval rows.

## Findings by topic

### 1. Benchmark-grader auditing — kengaku-only; three siblings explicitly route it to kengaku
No sibling claims grader/benchmark ownership. Sibling records that point the topic at kengaku:
- kasegi PROVINCE.md:50 — sibling adjacency table: `kengaku — LLM evaluation and benchmarks`.
- chousa PROVINCE.md:10-11 — `Refuses: … model-quality or evaluation claims (→ kengaku)`.
- kumitate PROVINCE.md:24 — `adjacent, not absorbed: kengaku evaluates agents, this lane
  arranges the seats around that judgment`.
- kotoba PROVINCE.md:65 (round-74 census row): `kengaku owns measured capability effects of prompt
  format and hands reusable craft out` (kotoba owns prompt/skill craft only).
- chousa's gate reinforces the same routing: `SCOPE_KENGAKU` phrase list now includes
  `llm benchmark|llm benchmarks|llm scoring` (`corpus/README.md:23,678-681`), so a record declaring
  `domain: LLM benchmarks` is warned `SCOPE_MODEL_QUALITY_ABSORBED`. kengaku's round-44 C2 record
  (S138-S146) is exactly that class — chousa would flag it as ours, not absorb it. No fork needed.
- Near but distinct: kotoba skill-eval artefacts (`corpus/README.md:133`, round 70: hand-authored
  `evals/evals.json`, `grading.json`/`benchmark.json`) evaluate SKILLS (kotoba's own craft), not
  model task graders; kama “grades” a loading server's 503 bodies (endpoint health, not a
  benchmark). Neither overlaps C2.

### 2. Cryptanalysis — no owner in the fleet; kaidoku explicitly parks decrypt ground as unowned
- kaidoku PROVINCE.md:309-311: `Live packet capture (…), analyst-supplied decryption keys and
  network-forensics case ownership remain unowned/Adjacent; saved-capture envelopes do not absorb
  them`. kaidoku itself is REA reverse-engineering; revenger is binary forensics + evidence-ledger
  and refuses harness/evidence auditing (revenger PROVINCE.md:22). kasegi (bounty/security research)
  covers program rules, severity ladders, VEX/EPSS/SSVC — no cryptanalysis. tsukuroi's `crypttab`
  is host LUKS config, not analysis. Conclusion: the feal-linear-cryptanalysis SUBJECT is unowned;
  kengaku's C2 is a grader-quality claim on a named benchmark, not a cryptanalysis claim — keep the
  grader in-lane, and report the unowned subject (FEAL linear cryptanalysis technique) to the
  integrator rather than absorbing it.

### 3. Answer-leak detection — no owner; adjacent leak/evasion work is a different class
No sibling detects benchmark-answer leaks. Adjacent neighbours, not overlaps:
- kagi PROVINCE.md:48 — `corpus/transcript-scan.sh` — transcript-leak gate over the durable DB:
  credential/transcript hygiene (secret-shaped redaction), not benchmark answers.
- kama corpus/README.md ~:1171-1179 — round-49 K1Cheat/K2UrlSwap class: decoy replays and
  `PYTHONPATH`/`sitecustomize` hijacks that fake a tool run — counter-evasion testing for
  verification receipts, not benchmark answer leak.
- Other `leak` hits are unrelated (audio-leak-warning, coverage-member leaks, fixture-hermeticity
  leaks). Nothing routes to or from kengaku here.

### 4. Mutation-attributed gate testing — the reusable METHOD is tameshi's; each lane's gate stays its own
- tameshi PROVINCE.md:3-5: `Domain: verification-fixture craft — the reusable method of honest
  checks: hermetic suites, mutation testing, fail-closed arms, verdict-line discipline,
  no-permissiveness audits, before/after proof`. Lines 14-17: refuses product domains; `every
  lane's gate remains its own; tameshi owns only the reusable craft`; never edits a sibling's gate.
- tameshi's kill semantics already include attribution/witness: F2 `knowledge/witness-scoped-kill-
  verdict.md` (pre-registered witness split: 8 killed-on-witness / 0 accidental / 2 survived);
  F1 `knowledge/mutation-score-semantics.md` (kill rate k/(k+s), `timeout counts as a kill`
  rejected); `knowledge/fleet-kill-rate-ledger.md` (per-gate suite size, kill rate, survivor
  classes). K-R2-3 notes `no gate ships a kill-rate harness` — kengaku's C1 counter IS such a
  harness, a first in-fleet application on a gate.
- tameshi F9 frontier is open: `LLM-era mutant generation + equivalence … no LLM-specific search
  run yet` (corpus/README.md:86). kengaku's battery44 is hand-written single-purpose fixtures —
  adjacent to F9, not a claim on it.
- Routing: kengaku must build battery44 itself (its gate is its own product surface); it should
  cite tameshi's method/provenance in its counter docs (precedent: mado PROVINCE.md:20,28 —
  `tools/mado-verify.sh` consumes tameshi's `mutate-and-run.sh` read-only and prints its revision
  as provenance), and must not claim method novelty or mutate tameshi's tools. kotoba's round-65
  scan independently fixes the same map: `tameshi owns the fixture/mutation method across lanes'
  gates, kengaku's calibration is model-eval` (kotoba PROVINCE.md:27).

## Owners / overlaps / route summary

| Topic | Owner | Sibling overlap | kengaku routing |
|---|---|---|---|
| benchmark-grader auditing | kengaku (sole) | kasegi, chousa, kumitate, kotoba all route it to kengaku; chousa's SCOPE_KENGAKU screen enforces it | keep C2 in-lane; no handoff |
| cryptanalysis (FEAL subject) | none | kaidoku parks decrypt keys as unowned/Adjacent | keep grader claim; report unowned subject to integrator, don't absorb |
| answer-leak detection | none | kagi transcript-leak (credentials), kama cheat/decoy counters (evasion) | keep C2 receipt leak-facts in-lane; no absorb |
| mutation-attributed gate testing (method) | tameshi | tameshi owns method incl. witness kills; mado/kagi/kumitate/tsukuroi consume its service | battery44 is kengaku's own gate fixture; cite tameshi provenance; no method novelty claim; don't touch tameshi tools |

## Round-44 package/counters adjacency verdict
- C2 (TB2 feal-linear-cryptanalysis grader): no sibling contention. External rows already fix the
  boundary (kasegi:50, chousa:10-11, kumitate:24). Nothing to route out; everything routes in.
- C1 (battery44, mutation-attributed kills): method provenance belongs to tameshi; the battery is
  kengaku's own fixture. Recommended: name tameshi's witness/kill semantics as prior art in the C1
  counter docstring (or at least keep the attribution legs f/g aligned with tameshi's F2 grammar),
  and leave tameshi F9 (LLM-era mutant generation) untouched/unclaimed.
- Neither counter reads sibling work products; the scan found no sibling that would conflict with
  the frozen separability claim. No `contested` record, so no integrator arbitration is needed.

VERDICT: sibling-overlap-7
