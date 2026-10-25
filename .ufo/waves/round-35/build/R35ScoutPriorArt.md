# R35ScoutPriorArt — prior art for the C1 instrument (round 35, wave 1, hyaku run 7, 2026-10-25)

Seat: `R35ScoutPriorArt` (scout). Scope: prior-art check for the **C1 instrument** — executing a benchmark
task's own grader on synthetic, requirement-targeted outputs (mutants) to map which instruction
requirements the grader enforces. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Read-only on the lane; nothing outside `.ufo/waves/round-35/build/` was written.

## 0. What the instrument is (as priced by the frozen claim)

Frozen claim file: `plans/round-35-claims.md` (freeze commit `11d64530179b78e33ba6074fc77d63d36ee7ac31`).
C1's instrument, in the claim's own words:

- pinned TB2 `protein-assembly` grader `tests/test_outputs.py` + `tests/test.sh` + `instruction.md`
  (S105–S107, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`);
- an **offline probe** `plans/tb2_grader_probe.py` (18 frozen cases) that runs the captured grader on
  synthetic gBlocks and emits, per case: predicted verdict, observed verdict, the first failing
  assertion message, and the instruction requirement the case targets;
- receipt `corpus/evidence/round35/tb2-grader-probe.txt`, `cases=18 observed_pass=5 observed_fail=13 mismatches=0`.

So the instrument pattern is: **(a) execute a benchmark task's own grader**, offline, on
**(b) synthetic, requirement-targeted mutants**, and report **(c) a requirement→assertion traceability map**
with the first-failing-assertion text. The lane's own coverage-map row already prices ABC (S091) and
the round-29 checklist as prior art; this seat prices the *instrument*, not the checklist.

## 1. Search axes (cheap, parallel) and what each axis returned

| # | Axis | Outcome |
|---|---|---|
| A1 | Agentic Benchmark Checklist (ABC) — outcome validity, per-task grading items | Hit: ABC.md raw, item-level |
| A2 | Terminal-Bench oracle / null-agent / no-op checks as an instrument | Hit: TB paper §2.3, harbor authoring manual, harbor CI (`Nop Validation`), deaimer `tb-docs` |
| A3 | SWE-bench test-validity audits (weak tests, false positives/negatives) | Hits: UTBoost, PatchDiff, OpenAI Pro audit, STING, SWE-ABS, SWE-Mutation, ABA, BenchGuard |
| A4 | Mutation testing of test suites applied to benchmark graders/verifiers | Hits: deaimer §6.2 "thin mutant", task-scoped state oracles (researchsquare), Red-Teaming the Grader (NeurIPS), AppWorld/WorkArena blind spots (NeurIPS), fixture-coverage mutation (NeurIPS), MORPH-DA (NeurIPS), Scale Labs, Agents-on-Rails |
| A5 | Grader-hacking / reward-hacking audits of agent benchmarks | Hits: BenchJack (arXiv 2605.12673), hacker-fixer loops (arXiv 2606.08960), RHB (arXiv 2605.02964), HVTB (arXiv 2608.22103), "How We Broke Top AI Agent Benchmarks" |
| A6 | Requirement→grader-assertion traceability mapping (the map itself) | Hit: TestJack (arXiv 2610.10619) "requirements checklist"; deaimer §9 checklist; `check-test-file-references` (harbor static check) |
| A7 | Offline, container-free execution of a benchmark grader | Hits: deaimer §6.2/§9 (no-container thin-mutant protocol), Scale Labs ("pass a defective artifact to the new grader"), harbor `/regrade` (recorded outputs through the updated verifier), june.kim `regrade.sh` |

## 2. Hits, each with a located quote (fetched 2026-10-25)

Quotes are byte-exact from the fetched page/PDF; location given as URL + section. Word counts ≤25.

**Hit count: 40 distinct prior-art source documents** carrying at least one located quote.
Accounting (reproducible): `grep '^- URL:' R35ScoutPriorArt.md | sed 's/^- URL: //' | sed 's/ .*//' | sort -u | wc -l`
returns **41** distinct URLs; arXiv 2609.37315 appears twice (abs + HTML of one paper), so **40
distinct documents**. The same document reused across sections is counted once (the deaimer article
appears in H3 and H9; ABC.md in H1). Not counted: the two TB2 raw-grader URLs in §3 (a byte-identity
check, not a prior-art source) and the `fail-validate-oracle` path (a search-synthesis hit that 404s
on fetch, see §5). 85 quote bullets in total across the 40 documents.

### H1 — ABC (the checklist instrument itself)
- URL: https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/ABC.md (§Outcome Validity → Unit Testing)
- Quote: “Measures quality of test cases using objective metrics (e.g., code coverage, cyclomatic complexity control).”
- URL: https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/ABC.md (§Benchmark Reporting → Interpretation)
- Quote: “Reports results of trivial agents (e.g., one that does nothing).”
- URL: https://arxiv.org/abs/2507.02825 (Abstract)
- Quote: “we introduce the Agentic Benchmark Checklist (ABC), a set of guidelines that we synthesized from our benchmark-building experience”
- Bears on: ABC asks for objective test-quality metrics and for trivial-agent baselines, but ships **items, not an executed grader-probe instrument**.

### H2 — Terminal-Bench's own paper applies ABC to Terminal-Bench (so TB2's graders are already ABC-scored)
- URL: https://arxiv.org/html/2601.11868v1 (§B.5 Assessment of Terminal-Bench on the Agentic Benchmark Checklist)
- Quote: “We applied the Agentic Benchmark Checklist (ABC) ( Zhu et al., 2025 ) to further troubleshoot and demonstrate the evaluation rigor.”
- Same URL (§B.5, item I.d.2 rationale)
- Quote: “Test case quality is not assessed via objective, automated metrics. Instead, the benchmark relies on extensive human review of test specifications and coverage.”
- Same URL (§2.3, task review process)
- Quote: “a no-op “dummy” agent should fail the task”
- Same URL (§B.4 Adversarial Exploit Agent)
- Quote: “An adversarial exploit agent was run to detect design flaws that could allow agents to cheat and pass the tests.”
- Bears on: the maintainers themselves score ABC for TB2 and admit the *objective test-quality metric* is missing; the lane's probe supplies it for one task.

### H3 — The deaimer/Harbor “thin mutant” protocol (closest conceptual match to C1's protocol)
- URL: https://www.deaimer.com/research/the-sandbox-is-not-the-grader-building-trustworthy-agent-eva-1e271b26 (§6.2 Discrimination: one rule, one witness)
- Quote: “This is the logic of mutation testing applied to verifiers.”
- Same URL (§6.2)
- Quote: “For each material requirement, an author constructs a thin mutant, a candidate solution that is correct except for a single deliberate violation, and confirms that the verifier rejects it.”
- Same URL (§6.2, config-precedence worked example)
- Quote: “A verifier that only checks a scenario where all three layers agree … will pass a loader that ignores environment variables entirely.”
- Same URL (§9 working checklist, Judgment row)
- Quote: “Does violating any single stated rule flip the reward to 0?”
- Same URL (§9 working checklist, Judgment row, supporting practice)
- Quote: “thin-mutant battery per requirement”
- Same URL (§10 Open research questions)
- Quote: “Constructing thin mutants by hand is labor-intensive.”
- Same URL (§10)
- Quote: “ensuring generated mutants are genuinely plausible rather than trivially broken, since trivially broken mutants overstate verifier strength”
- Bears on: **the C1 protocol is described as a published recommendation, one rule at a time.** This is prior art for the *method*, and it names the same failure modes C1 hit (a mutant can pass; the assertion text can misattribute the cause).

### H4 — Harbor's own reviewer tooling (the maintainer-side instrument)
- URL: https://raw.githubusercontent.com/harbor-framework/terminal-bench/main/docs/TASK_REVIEW_AUTOMATION.md (§Pipeline Overview table)
- Quote: “Nop Validation | Doing nothing fails tests | Auto on PR + every push / `/validate`”
- Same URL (§Pipeline Overview table)
- Quote: “Hacker-Fixer Loop | Iterative adversarial task hardening | `/fortify`”
- Same URL (§Static Checks → check-test-file-references)
- Quote: “Ensures all expected output files are documented in `instruction.md`.”
- Same URL (§Cheat Trials)
- Quote: “an adversarial prompt (from [`docs/prompts/hack-trial-prompt.md`](prompts/hack-trial-prompt.md)) is prepended to the task instruction, instructing the agent to cheat rather than solve the task legitimately.”
- Same URL (check-trial-network-fetch)
- Quote: “a known reward-hacking surface (an agent can shim `/usr/bin/curl` in its phase so the verifier's later fetch returns trojaned output”
- URL: https://deaimer.github.io/tb-docs/validation/oracle (§Required outcome)
- Quote: “Oracle `1.0` does not prove wrong solutions fail, every requirement is tested, ground truth is hidden, or the task is difficult.”
- URL: https://raw.githubusercontent.com/harbor-framework/terminal-bench/main/docs/REVIEWING.md (step 4)
- Quote: “Would the instruction alone let you write the same tests? (test-instruction alignment)”
- Bears on: Harbor ships **no-op** and **instruction↔test** checks but no requirement-targeted mutant battery per task; the manual explicitly states that an oracle pass does not establish that wrong solutions fail or that every requirement is tested — exactly the gap C1's probe fills.

### H5 — SWE-bench test-validity audits (the "weak tests" family)
- URL: https://arxiv.org/abs/2506.09289 (UTBoost, Abstract)
- Quote: “we identified 36 task instances with insufficient test cases and uncovered 345 erroneous patches incorrectly labeled as passed”
- URL: https://arxiv.org/abs/2503.15223 (PatchDiff, Abstract)
- Quote: “Our findings reveal critical weaknesses in SWE-bench's patch validation mechanism, which causes 7.8% of all patches to count as “correct” while failing the developer-written test suite.”
- URL: https://openai.com/index/separating-signal-from-noise-coding-evaluations/ (failure-mode list)
- Quote: “*Low-coverage tests* under check the requested feature, so incomplete fixes can pass.”
- Same URL (Methodology)
- Quote: “Our datapoint analysis pipeline flagged 200 (27.4%) broken tasks, while the human annotation campaign identified 249 (34.1%).”
- URL: https://arxiv.org/abs/2604.01518 (STING, Abstract)
- Quote: “Variants of the reference patch that survive the original tests reveal under-constrained behaviors”
- Same URL
- Quote: “On SWE-bench Verified, 77% of instances admit at least one surviving variant.”
- URL: https://arxiv.org/abs/2603.00520 (SWE-ABS, Abstract)
- Quote: “mutation-driven adversarial testing that synthesizes plausible but incorrect patches to expose semantic blind spots”
- URL: https://arxiv.org/abs/2605.22175 (SWE-Mutation, Abstract)
- Quote: “The benchmark characterizes test suites by introducing systematically mutated solutions that attempt to ``fool'' the test suites and pass validation.”
- URL: https://arxiv.org/abs/2605.26079 (ABA, Abstract)
- Quote: “We run ABA on a collection of frontier LLM benchmarks and previous NeurIPS publications, totaling 168 benchmarks across nine domains.”
- Same URL
- Quote: “filtering out these tasks with issues shifts model rankings and increases average performance on SWE-bench Verified and Terminal-Bench 2 by 9.9% and 9.6%”
- URL: https://arxiv.org/abs/2604.24955 (BenchGuard, Abstract)
- Quote: “BenchGuard cross-verifies all benchmark artifacts via structured LLM protocols, optionally incorporating agent solutions or execution traces as additional diagnostic evidence.”
- Bears on: the *auditing-of-test-strength* family is dense and mature; all of it operates on **patches/solutions**, not on synthetic outputs fed to a grader, and none of it emits a requirement→assertion map.

### H6 — Mutation testing of benchmark verifiers/graders (the closest family)
- URL: https://www.researchsquare.com/article/rs-10665114/latest (Abstract) — *Mutation Testing of Task-Scoped State Oracles in Software-Agent Benchmarks*
- Quote: “We introduce a deterministic mutation-testing protocol for calibrating such task-scoped state oracles.”
- Same URL (Abstract)
- Quote: “the protocol injects six classes of harmful state faults and three schema-certified benign transformations, then compares official scores with three controlled reference rules”
- Same URL (Abstract)
- Quote: “Official evaluators rejected 100 of 110 harmful mutations (90.9%; Wilson 95% CI 84.1–95.0%) and preserved all 35 applicable JSON-key-order variants”
- URL: https://neurips.cc/virtual/2026/172887 (Red-Teaming the Grader: Mutation-Validated Constraint Checking for Tool-Agent Benchmarks, Abstract)
- Quote: “mutation probes that attack verified reference solutions with step drops, delete-substitutions, wrong targets, value perturbations, and string-literal swaps”
- Same URL (Abstract)
- Quote: “a fail-closed predicate registry with per-predicate normal/boundary/adversarial fixtures enforced by a meta-test”
- Same URL (Abstract)
- Quote: “The protocol caught real defects. Across two probe rounds it surfaced 527 unique passing mutants”
- URL: https://neurips.cc/virtual/2026/172904 (Finding Blind Spots in AppWorld and WorkArena Task Verifiers, Abstract)
- Quote: “We audit the shipped AppWorld and WorkArena verifiers with source-informed, mutation-inspired tests.”
- Same URL (Abstract)
- Quote: “AppWorld has a concrete blind spot: duplicating a non-idempotent write preserves every value the evaluator checks while creating an extra record.”
- URL: https://neurips.cc/virtual/2026/173032 (Discriminating Fixture Coverage in Agent-Infrastructure Verification Suites, Abstract)
- Quote: “Applying mutation analysis to an invariant suite for a multi-session agent state-projection layer, we first find that this standard validation certifies a suite in which a first-order mutant removing event-identity deduplication survives every check.”
- Same URL (Abstract)
- Quote: “we enumerate seven discriminating dimensions of the input space, register in advance which are uncovered and which survivors they should explain”
- URL: https://neurips.cc/virtual/2026/173029 (MORPH-DA, Abstract)
- Quote: “The benchmark contains 101 compositional tasks and 563 validated, non-equivalent semantic mutants.”
- Same URL (Abstract)
- Quote: “MORPH-DA detects 364/563 faults (64.7%, 95% task-clustered CI [58.4, 70.5]) versus 9/563 for universal robustness checks”
- URL: https://labs.scale.com/blog/verifier-design-for-cua (§One wrong number, thirty-eight perfect scores)
- Quote: “We intentionally corrupted the single most important number in each deliverable across 38 tasks, representing the exact error that invalidates a document in real life.”
- Same URL (§same)
- Quote: “Zero out of 38 programmatic verifiers failed the corrupted document.”
- Same URL (§Takeaways)
- Quote: “Apply mutation testing by deliberately corrupting key output values to verify that scores actually drop.”
- URL: https://evilmartians.com/chronicles/the-agents-on-rails-files-designing-black-box-evals-for-coding-agents (§On calibration and mutation)
- Quote: “**Equivalent mutants** change the UI but not the behavior. Every test must still pass.”
- Same URL (§same)
- Quote: “**Faulty mutants** break the behavior behind a UI that looks right. At least one test must fail.”
- Same URL (§same)
- Quote: “For the Campfire Bots task, we've ended up with 13 mutants (8 + 5).”
- Bears on: **the "mutate the grader's inputs and see whether it catches it" instrument is established** across at least six independent groups in 2026 (task-scoped state oracles; Red-Teaming the Grader; AppWorld/WorkArena blind spots; fixture-coverage mutation; MORPH-DA; Scale; Agents-on-Rails). Each differs in the *object* mutated (state, solution, UI, deliverable) and none of them builds a requirement→assertion traceability map from an `instruction.md`.

### H7 — Grader-hacking / reward-hacking audits
- URL: https://arxiv.org/abs/2605.12673 (BenchJack, Abstract)
- Quote: “We apply BenchJack to 10 popular agent benchmarks spanning software engineering, web navigation, desktop computing, and terminal operations.”
- Same URL (Abstract)
- Quote: “BenchJack synthesizes reward-hacking exploits that achieve near-perfect scores on most of the benchmarks without solving a single task, surfacing 219 distinct flaws across the eight classes.”
- URL: https://moogician.github.io/blog/2026/trustworthy-benchmarks-cont/ (§The Agent-Eval Checklist)
- Quote: “Run a **null agent** that takes no actions. Its score is your floor. If it’s not zero, something is wrong.”
- Same URL (§Terminal-Bench exploit)
- Quote: “Our exploit replaces `/usr/bin/curl` with a wrapper during the agent phase.”
- URL: https://arxiv.org/abs/2606.08960 (hacker-fixer loops, Abstract)
- Quote: “We audit 1,968 tasks across five terminal-agent benchmarks and find 323 (16%) hackable by frontier models given only the task description.”
- URL: https://arxiv.org/abs/2605.02964 (RHB, Abstract)
- Quote: “We introduce the Reward Hacking Benchmark (RHB), a suite of multi-step tasks requiring sequential tool operations with naturalistic shortcut opportunities”
- URL: https://arxiv.org/abs/2608.22103 (HVTB, Abstract)
- Quote: “we adapt HVE to Terminal Bench, a leading benchmark of real-world terminal and coding tasks, and introduce Hack-Verifiable Terminal Bench (HVTB).”
- URL: https://arxiv.org/abs/2510.20270 (ImpossibleBench, Abstract)
- Quote: “We measure an agent's "cheating rate" as its pass rate on these impossible tasks, where any pass necessarily implies a specification-violating shortcut.”
- Bears on: reward-hacking audits ask “can a wrong solution pass?”; C1 asks the dual “does the grader enforce the stated requirement, and does it say so correctly?”.

### H8 — Requirement→assertion traceability (the map itself) and determinacy
- URL: https://arxiv.org/html/2610.10619v1 (§3.2 Per-Trial Auditing, step 2)
- Quote: “The agent decomposes PP into atomic, testable clauses, which instantiate 𝒬(P), and records for each clause whether T0 covers it and whether the trial implements it.”
- Same URL (§3.1 Problem Formulation)
- Quote: “a trial should be judged against the requirements stated in the task prompt, and the ground-truth solution … can serve as an executable oracle”
- Same URL (Abstract)
- Quote: “about 34.4% of the model trials currently judged correct violate the task requirements”
- URL: https://www.june.kim/a-determinacy-audit-of-swebench-pro (§Method)
- Quote: “Every gold is graded by the official evaluator at the pinned commit under a two-pass isolation protocol”
- Same URL (Abstract)
- Quote: “A benchmark score is only as meaningful as the determinacy of its tasks.”
- Same URL (§Introduction)
- Quote: “a *codebase-determinacy sweep* settles it against grep-verified live precedents at the base commit”
- URL: https://www.june.kim/terminal-bench-frame (§Method)
- Quote: “compose the task's own reference solution with a careless suffix, a documented terminal-agent accident such as `rm -rf .git`, re-run the official grader, and read the verdict.”
- Same URL (§Abstract)
- Quote: “On Terminal-Bench 2.1, 40 of 83 gold-passing tasks (48%) certify success after a careless deletion inside the task's own workspace.”
- Same URL (§Related work)
- Quote: “Reward hacking asks whether a wrong solution can pass. We ask the opposite: whether a right solution that also causes harm still passes.”
- URL: https://arxiv.org/html/2609.37315v1 (§V-A Experimental Setup)
- Quote: “Validation is pre-registered (§V-B): injected defects on and off the taxonomy, negative controls with verdicts predicted before the run, gold replays”
- Same URL (§I Introduction)
- Quote: “The benchmark audits we survey examine task artifacts, environment configuration, graders, and judges”
- Same URL (Abstract)
- Quote: “in 29 of 33 scored misses a clause covered the defect but no probe revealed it.”
- URL: https://arxiv.org/abs/2609.37315 — the survey's taxonomy counts: “27 categories: BenchGuard 14, Automated Benchmark Audit 3, Tool-Veritas 10”
- URL: https://neurips.cc/virtual/2026/173047 (Diagnosing the Test Before Anyone Takes It, Abstract)
- Quote: “A leakage audit treats every clause of the problem's contract as falsifiable and attempts to falsify each”
- Same URL (Abstract)
- Quote: “A discrimination audit fields five reference submissions on the real evaluation segment and reads only relations between them”
- URL: https://neurips.cc/virtual/2026/173003 (When the Verifier Is Wrong, Abstract)
- Quote: “We use a closed-loop protein-design agent as a controlled testbed because nearly every available action has a recorded experimental outcome.”
- URL: https://neurips.cc/virtual/2026/172962 (The Verifier Never Saw the Error, Abstract)
- Quote: “Copying the balance preserves the evidence and makes an arithmetic checker fire; replacing it with the value implied by the ledger makes the same checker accept.”
- URL: https://neurips.cc/virtual/2026/172894 (Three-State Audit of Active GUI-Agent Evaluation, Abstract)
- Quote: “But an inspection can also change the success predicate it is supposed to verify.”
- Bears on: the *traceability-map* idea exists (TestJack's requirements checklist; june.kim's determinacy classes; harbor's `check-test-file-references`), and the *pre-registered prediction + negative control* discipline is published (2609.37315, 173047). C1's combination — offline execution of the shipped grader on requirement-targeted mutants, with predictions frozen before the run — is not published as such.

### H9 — Prior audits of the *same* TB2 task family (adjacency, not instrument prior art)
- URL: https://www.horizonanalyticslabs.com/research/public-benchmark-dataset-audit (§The published solution scored zero)
- Quote: “We ran the author’s own solution five times, including three runs against the version served by the hub during this audit. It scored zero every time.”
- Same URL (§The published solution scored zero)
- Quote: “The external protein data had changed. The tests still expected the older representation, leaving no valid sequence that could satisfy both the data and the grader.”
- Same URL (Appendix, Terminal-Bench 2.1 rows)
- Quote: “Three required behaviors are never checked” / “An empty dependency file and two hardcoded numbers pass”
- Same URL (§Five ways a benchmark breaks)
- Quote: “**Incomplete tests:** The grader checks less than the instruction requires.”
- URL: https://icml.cc/virtual/2026/82793 (Benchmarks as Software, Abstract)
- Quote: “We find task-side defects in 28 of 89 tasks (31%) in the benchmark.”
- Same URL (Abstract)
- Quote: “Agentic benchmarks accumulate defects on every axis: instructions can be overspecified, verifiers can be underspecified, and environments drift as external dependencies change after release.”
- URL: https://www.tbench.ai/news/terminal-bench-2-1 (What changed)
- Quote: “Misspecification: Some tasks had instructions that were not aligned to their tests.”
- URL: https://shreyashgondane.com/research/tb2-oracle-audit.html (Abstract)
- Quote: “8 of 65 tasks failed 3 out of 3 tries.”
- Same URL (Setup and limits)
- Quote: “harbor run -d terminal-bench@2.0 -a oracle -i <task>   # one task's reference against its own tests”
- URL: https://www.deaimer.com/research/the-sandbox-is-not-the-grader-building-trustworthy-agent-eva-1e271b26 (§Abstract)
- Quote: “whether the verifier's reward changes when, and only when, a required behavior is violated”
- Bears on: **prior work already reports defects in TB2 `protein-assembly`** — the Horizon audit reports the author's own solution failing in TB2.1 because the live PDB data changed while the grader keeps literals; "Benchmarks as Software" reports 28/89 TB2 tasks defective and 2.1 changed `protein-assembly` (−7.1 pp). So the *phenomenon* C1 touches on this task is already published; C1's contribution is a different (grader-semantics) measurement of the same pinned grader.

## 3. Instrument-pattern comparison (what is prior art, what is not)

| C1 instrument element | Prior art | Status |
|---|---|---|
| Run a benchmark task's own grader, offline, no container | deaimer §6.2/§9 thin-mutant protocol; Scale Labs "pass a defective artifact to the new grader"; harbor `/regrade`; june.kim `regrade.sh` | **established** (the offline, container-free grader probe is published practice) |
| Feed it synthetic, deliberately-broken outputs to test discrimination | task-scoped state oracles (rs-10665114); Red-Teaming the Grader (172887); AppWorld/WorkArena blind spots (172904); fixture-coverage mutation (173032); MORPH-DA (173029); Agents-on-Rails equivalent/faulty mutants; Scale 38/38 corruption test | **established** (at least seven independent 2026 executions) |
| One mutant per *stated requirement* (thin mutant), not per generic fault | deaimer §6.2 "For each material requirement … a thin mutant"; TestJack's per-clause witnesses; 173047 per-clause falsification | **established as a published recommendation**; executed form seen only via LLM-generated witnesses (TestJack) |
| Requirement → enforcing-assertion traceability map | TestJack §3.2 step 2 requirements checklist; june.kim determinacy classes; harbor `check-test-file-references` (file-level only) | **partially established**: the *mapping* is published; the *per-assertion, executed* map keyed to a shipped grader's own assertion text is not |
| Predictions frozen before the first run; mismatches reported, never re-predicted | 2609.37315 §V-A ("negative controls with verdicts predicted before the run"); lane's own pre-registration practice (r11/r12) | **established** |
| Report the *first failing assertion message* as the attributed cause | not found as prior art; deaimer §6.3 is the nearest (over-strict verifier framing) | **gap — but it is a reporting detail, and deaimer §10 warns trivially-broken mutants overstate strength** |
| Scale: one task, one grader, 18 cases | most prior work is cross-benchmark (168, 731, 1,968 tasks, 800 scenarios) | **gap at scale, not at method** |

**Verdict on the pattern:** the C1 instrument is **incremental, not novel** and not unique — it is a
byte-pinned, offline, requirement-targeted instance of a **published and repeatedly executed**
instrument family (mutation-testing a benchmark's own verifier), with two additions of its own:
(1) the requirement→assertion **traceability map keyed to the shipped grader's own assertion text**,
and (2) attribution of *why* a case failed by reading the grader's first failing assertion. Neither
addition is a new method: (1) is a per-task instance of TestJack's requirements checklist and
harbor's `check-test-file-references`; (2) is a reporting choice the deaimer §6.2/§6.3 discussion
implies. The lane's own prior-art entry (`corpus/knowledge/benchmark-task-validity-checklist.md`,
round 29) already priced ABC as **INCREMENTAL** for the A–J axis checklist; this seat prices the
*probe* the same way.

**Novelty claim the entry may make:** none at instrument level. **What is defensible:** that for
`protein-assembly` at `2fd12b88`, the executed grader (i) accepts a G-only linker under a
requirement that says "GS linkers" — a requirement-vs-grader gap of the kind ABC's outcome-validity
item I.d.2 asks for and TB2's own ABC table leaves open; (ii) never lets the 3000-nt cap decide an
otherwise-passing gBlock (`max_passing_nt=2766`), so the cap is inert on the reward; and (iii)
misattributes a one-residue subprotein error to the *order* assertion, because `str.find` returns
−1. Points (i) and (iii) are **the same class of finding the prior art already publishes for other
benchmarks** (deaimer §6.2 "undiscriminated rules"; Task-scoped state oracles' 10 false negatives;
173047's "no probe revealed it"; AppWorld's blind spot). Point (ii) is a *quantitative* addition
specific to this grader (and is arithmetic on the pinned literals, not a generalisable method).

**Adjacency risk the L1 must weigh:** the same task has two published defect reports — Horizon's
(TB2.1 `protein-assembly` author solution scores zero because live PDB data drifted from the
grader's literals) and "Benchmarks as Software" (28/89 TB2 tasks defective; 2.1 changed
`protein-assembly` −7.1 pp per https://www.tbench.ai/news/terminal-bench-2-1, "What changed" table).
C1's entry says the grader "never opens the task's reference inputs … the five expected subproteins
are amino-acid literals" — that observation *is* the mechanism behind Horizon's reported failure, so
C1's mechanism note should cite that adjacency rather than stand as if the literal-vs-live-data gap
were unremarked.

**Byte-level check of where the TB2.1 fix landed** (all fetched 2026-10-25; `diff` exit 0 = identical):

| file | TB2.0 @ `2fd12b88` | TB2.1 @ `7131e437` | verdict |
|---|---|---|---|
| `tests/test_outputs.py` | sha256 `44a05a24…6582`, 3847 B | sha256 `44a05a24…6582`, 3847 B | **byte-identical** |
| `instruction.md` | sha256 `1bb2af1d…37f5c`, 34 lines | sha256 `1bb2af1d…37f5c`, 34 lines | **byte-identical** |
| `tests/test.sh` | — | — | **byte-identical** (`diff` empty) |
| `task.toml` | `docker_image = "alexgshaw/protein-assembly:20251031"` | `docker_image = "alexgshaw/protein-assembly:20260403"` | image retagged |
| `solution/solve.sh` | RCSB `fasta/entry/{id}/download` + `len(lines) > 3 → None` | RCSB `rest/v1/core/polymer_entity/…`, explicit `modified_monomer` handling | **rewritten** |

Fetched 2026-10-25 from
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py`
and
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2-1/7131e4375048a0e408a8fb404b5f499d726b695b/tasks/protein-assembly/tests/test_outputs.py`
(TB2.1 `main` head at fetch time was `7131e4375048a0e408a8fb404b5f499d726b695b`), and compared with
`diff -q` (exit 0) plus `sha256sum` on the lane's own captured copies under
`corpus/evidence/round35/tb2-eval/`.

So the 2.1 repair of this task was made in the **reference solution** (and the environment image),
**not** in the grader and **not** in the instruction: the shipped grader still asserts the same five
literal amino-acid strings, and the instruction still asks for "GS linkers". C1's executed findings
therefore transfer unchanged to TB2.1, and the published 2.1 delta (−7.1 pp on this task) is a
solution-side fix, not a grader-semantics fix. This is a concrete, checkable statement the L1 can
make about the pinned grader's status — and it is stronger than the entry currently claims, because
it shows the literal-vs-live-data gap was addressed by changing the *solution*, leaving the
literal-vs-requirement gap C1 measured untouched.

## 4. Coverage of the four prior-art families named in the assignment

1. **ABC (outcome validity)** — covered (H1, H2). ABC supplies checklist *items*; it does not supply an
   executed grader probe, and TB2's own ABC assessment (H2) explicitly records the objective
   test-quality metric as not satisfied.
2. **Terminal-Bench oracle / null-agent checks** — covered (H2, H4, H9). TB2's pipeline ships Oracle +
   Nop + cheat-trial + `/fortify`; the authoring manual states that oracle 1.0 "does not prove wrong
   solutions fail, every requirement is tested" — the exact gap C1 closes, one task at a time.
3. **SWE-bench test-validity audits** — covered (H5): UTBoost, PatchDiff, OpenAI Pro audit, STING,
   SWE-ABS, SWE-Mutation, ABA, BenchGuard. All operate on patches/solutions, not on synthetic outputs
   fed to a shipped grader.
4. **Mutation testing applied to benchmark graders** — covered (H6): rs-10665114, Red-Teaming the
   Grader, AppWorld/WorkArena blind spots, fixture-coverage mutation, MORPH-DA, Scale Labs,
   Agents-on-Rails.
5. **Grader-hacking / reward-hacking audits** — covered (H7): BenchJack, hacker-fixer loops, RHB,
   HVTB, ImpossibleBench, and the Berkeley-style "how we broke" write-up (null-agent floor).

## 5. Gaps / what I could not establish

- I did not fetch any arXiv paper's full PDF (only arXiv API abstracts/markdown, plus the TB paper's
  HTML rendering). Quotes from arXiv items are therefore abstract-level; the NeurIPS/ICML/venue
  abstracts are the publisher's own full abstracts.
- `openreview.net` forum/PDF pages returned a bot challenge page for `zh33pqlBjf`, `AhXMZPnOPS`,
  `F0fm6Wgkd0`, `uR6EWsGE48`, `JCARdreq38`, `JsrKw3nUSV`, `RyzGAFDM8S`, `cHVzNvdhVi`, `y6ouHLaxYb`;
  I cite those works via the venue's own abstract pages instead (nips.cc / icml.cc), which are the
  publisher-rendered abstracts.
- The `terminal-bench/checks/test-tasks/fail-validate-oracle` path cited by search synthesis returned
  404 on `main` (the repo tree at `main` has no `checks/` directory at this pin) — I did not count it as
  a hit; harbor's `docs/TASK_REVIEW_AUTOMATION.md` is the located artifact for the same checks.
- No source found that publishes a **per-assertion, executed requirement→assertion map of a shipped
  benchmark grader keyed to that grader's own assertion text**. Closest: TestJack (requirements
  checklist + witness tests, LLM-generated), 2609.37315 (per-clause predicates, tool-layer),
  harbor `check-test-file-references` (file references only). This is a real but narrow gap.
- No source found that reports the **first-failing-assertion misattribution** phenomenon (C1 finding
  (iii)) as such. Absence of evidence at ~20 searches, not evidence of absence.
- I did not attempt any live benchmark run, container pull, or model request. Every number quoted
  above is from a fetched primary document.

## 6. Recommendation to the L1 (draft, not applied)

- Price the C1 **instrument** as **INCREMENTAL** in the round-35 lesson and in the entry's prior-art
  line, citing deaimer §6.2/§9 (thin-mutant protocol), rs-10665114, 172887, 172904, 173032, 173029,
  Scale, Agents-on-Rails for the family, and H8 for the traceability/ prediction-freezing components.
  Do **not** claim instrument novelty anywhere in `corpus/knowledge/tb2-protein-assembly-grader.md`.
- Add the **adjacency** obligations the new sources create: (a) the entry's "literals vs live data"
  observation is the published mechanism of Horizon's reported `protein-assembly` failure; (b) TB2.1
  changed the task but left `tests/test_outputs.py`, `tests/test.sh` and `instruction.md`
  byte-identical to the pinned 2.0 files (verified by `diff` exit 0 and sha256
  `44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582` /
  `1bb2af1d85e9a823a8ae7273a87df8a3f67e2c93b06cddf34f0051a8b003f7c5`), so the findings are not
  2.0-only and the 2.1 repair landed in `solution/solve.sh` and the environment image, **not** in the
  grader — the entry may say the literal-vs-requirement gap C1 measured is still open in 2.1;
  (c) TB2's own paper (H2) already applies ABC to Terminal-Bench, so the entry should say which ABC
  item the probe instantiates (I.d.2 / outcome validity) rather than implying the checklist had not
  been applied to TB2.
- If the L1 wants a *novelty* contribution this round, it is not in the instrument; the only
  non-published things found here are the two grader-specific results (the inert 3000-nt cap, and the
  `find`-based misattribution) — both are single-task facts, not phenomena.

VERDICT: priorart-40-hits-novelty-incremental
