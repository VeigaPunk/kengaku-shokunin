# F42CritPriorArt — wider prior-art search for circuit-fibsqrt (round 42, wave 2, falsify)

Seat: scout (leaf, read-only). Window 2026-10-26 18:03:29 → 18:11:41 (-03, `date +%T`). Scratch `/fast/scratch/hyaku/kengaku-r42/F42CritPriorArt` (clones, fetched pages; not copied into the lane).
`ls -A /home/vgpnk/.local/bin | sha256sum` before = after = `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52`.
Envelope note: no battery, counter or fixture build was run (network reads, `curl`/`gh api`/`git clone --depth 1` into scratch only), so the bwrap envelope did not apply. Nothing installed. Nothing written outside scratch and this report dir.
Attacked: `R42ScoutPriorArt` (2/6) and the landed S128 row + entry text (`corpus/knowledge/tb2-circuit-fibsqrt-grader.md` §Prior art, §Wave-1 integration; `corpus/README.md:371`).

## Headline

1. **The wave-1 count survives: 2/6.** Strict (claim as worded) = 1/6 (finding 4, 208/20000 not graded). Weak adjacent form of finding 1 = +1. I found **no new published source** for the lookup construct (built and graded), stdin-vs-argv, last-32-lines vs highest-index, cwd compile / `/app/sim` overwrite, or whitespace/CRLF parse behaviour.
2. **But the wave-1 attribution of the coverage-gap prior art is wrong in time and strength.** The earliest published form is not S128 (2026-09-25) but the JonathanGabor audit (2026-01-20), which already lists "no very large N", "max isqrt tested is 220" and "N=0 missing" as weaknesses of this grader, beside the 208/20000 point. The entry and README cite that audit only for its *opposite* sentence ("hardcoding impractical") and for 208/20000, and credit S128 alone with the 48,401 gap (`README.md:371`). Fix: cite the audit for the range gap too (below).
3. **S128 says what the entry says it says**, with two small wording gaps (below). No reason to drop the row.
4. A web_search answer engine asserted a published "GPT-5.2 circuit-fibsqrt hardcoding" example (arXiv 2608.09867 App. E.3.1). **That is false**: E.3.1 is a quantum-factoring task. The paper's circuit-fibsqrt example is E.3.3 and is about restricting the input range, not hardcoding graded values. Recorded so no later seat imports it.

## Findings table

| # | Finding | Published? | Best source (access time) | Strength |
|---|---|---|---|---|
| 1a | grader exercises only 28 inputs, max 48,401; circuits pass and are wrong above | **yes, twice** | OpenAgents #9645 (2026-09-25); Gabor audit (2026-01-20) | coverage gap: published |
| 1b | a lookup/hard-coded gates.txt for exactly the 28 graded inputs passes 3/3 | **no** (built + graded: not found). Counter-claim published | Gabor audit line 454 says hardcoding "impractical" | construct not found |
| 2 | instruction says stdin, sim.c reads argv | no | — | not found (agents notice it privately, see §2) |
| 3 | "last 32 lines" vs 32 highest-indexed signals | no | — | not found |
| 4 | examples 208/20000 not graded | **yes** | Gabor audit line 460 (LLM-written) | published |
| 5 | grader compiles into cwd; `/app/sim` overwritten | no | — | not found |
| 6 | whitespace/CRLF/blank-line parse sensitivity | no | — | not found |

## Per-finding detail

### 1a/1b — coverage gap and lookup

**Published (coverage gap), new attribution.** `JonathanGabor/terminal-bench-2-audit`, commit `35f110397bc8ea58538424a1951760a9c5a0a710`, `audit_results/20260120_125158/audit.txt`, fetched 2026-10-26 18:10 -03 via `gh api …/contents/…?ref=35f1103…` (sha256 prefix `f0ee15c951e5…`, 3687 lines). Lines 459–462, "Potential Weaknesses":
- :459 "Missing N=0 edge case: isqrt(0)=0, fib(0)=0 not tested"
- :461 "No very large N values: Near 2^32 range not tested" (7 words)
- :462 "Maximum isqrt tested is 220: … higher isqrt values aren't tested"

The same audit at :454 and :466 asserts the opposite: "28 distinct test cases with varied inputs make hardcoding impractical"; "gaming the tests nearly impossible without a correct implementation". So the audit publishes the range gap and then draws the wrong conclusion from it. It is an LLM auditor (text opens "Looking at this task, I need to evaluate"), tier C. Date: run dir 2026-01-20, eight months before S128.

**Published (coverage gap, with real circuits).** OpenAgents #9645 — see §S128. Adds agent-built circuits that pass the 28 and fail beyond.

**Not found: the lookup circuit as a built, graded artefact.** Queries (all 2026-10-26 18:03–18:11 -03):
- `gh api search/code`: `circuit-fibsqrt hardcode` (42; non-lane hits are trajectory dumps, `atif-scan` pack lists, `JonathanGabor` audit, task lists), `circuit-fibsqrt lookup` (80; 15 shown: `evalstate/fast-agent` benchmark JSONs, `atif-scan/detectors/lookup.py` which is about *benchmark-source lookups*, not circuits), `fibsqrt gates.txt hardcoded test cases` (6), `gates.txt isqrt fib lookup table 28` (81), `circuit-fibsqrt cheat` (43), `circuit-fibsqrt memorize` (2), `circuit-fibsqrt overfit test inputs` (20), `fibsqrt "28 test"` (4), `circuit-fibsqrt verifier hardcode exploit` (9), `test_sqrt_fib fibsqrt coverage weak` (3).
- I opened: `huggingface/atif-scan` `detectors/lookup.py` and `packs/tb21.py` (no gate-lookup content; `circuit-fibsqrt` only in the 89-task list and a comment that a judge-flagged trial's only trace is `solve.sh`), `graphwork/wg` audit + DESIGN doc, `singhaganesh/Turminus-2`, `charles-azam/CLIArena`, `solvyxtech/molt docs/sharper-checks.md`, `getkimchi/kimchi-workflows`, `msf/msf.github.io`, `Evan-Kim2028/task_validation` (zai-verified README), `zignd/harbor-tbench-worktrial`, `copse-dev/agent-pane`, `ruturajs-turing/Local_LLmReviewer`, `mert-cemri/tb3_task_discover`, `ErixWong/erix-agent`, `jyyang26/Terminal-RSI TB2_OVERFIT_ANALYSIS.md`. `circuit-fibsqrt` appears only as a task-list entry, a failure count, or a model-capability remark; none states a lookup/hardcode finding.
- Trajectory dumps downloaded and grepped (`lookup|hardcode|test cases|28 inputs|memoriz|special-case`): `llm-as-a-verifier` (mini-swe-agent DeepSeek), `predotdev/predev-terminal-bench-2.0` (Sonnet 4.6), `NJU-LINK/CodeTracer` (Kimi K2.5), two `hamishivi/tmax` (Qwen3.5-9B, tmax-9b), `220488/Sorting-Hat` (Qwen3-480B), HF leaderboard `Gemini_CLI__Gemini-3-Flash-Preview` circuit-fibsqrt trial, `zxss702/terminal-bench-2.1` swe-agent log, `mescribano23/TerminalBenchAnalysis` GLM-5. Every "lookup/hardcode" hit is the agent rejecting a full 2^16 ROM or an isqrt lookup *inside* a real circuit (e.g. tmax-9b: "Maybe I should just hardcode the result based on some lookup? But N varies, so that won't work."). None builds a lookup for the 28 graded values; none reads the grader's table (the grader is not in the agent's image per the entry).
- arXiv: `2608.22103` (HVTB, honeypot hacks; html grepped for `fibsqrt|gates.txt|sim.c`: 0 hits), `2606.28430`, `2610.02588`, `2605.26079` (ABA audit of TB2 vs PR #53; 0 hits), `2601.11868` (TB paper; only the task-description row), `2607.14004` (task-list exclusion only), `2609.26826` ("What Makes a TB Task Hard"; 0 hits). `harbor-framework/terminal-bench#2086` (verifier hardening framework, 52 KB) and `#2150` (Tokenless findings; the 24-write-up index): 0 hits for `fibsqrt|circuit|gates.txt`. OpenReview "Continuous Validation and a Patch for TB2.0" (28/89 defects): the PDF endpoint returned a Cloudflare-style challenge (HTTP 403, `ChallengeRequiredError`), so its text was **not readable**; its search snippet describes categories (spec-verification mismatch, resource, drift) without naming this task. Gap noted.
- `harbor-framework/terminal-bench-2` PR #53 (TB2.1 patch) file list grepped for `fibsqrt`: 0. TB2.1 never edited this grader (wave-1 pin check).
- Answer-engine synthesis (web_search, not primary, discarded as evidence): it described the sparse equality-detector lookup circuit as feasible against "fixed 28-input" tests and cited the Gabor audit text; it also said "A lookup-table-only solution is not viable" for a full ROM. Neither is a published measurement.

**Adjacent, not hardcoding:** arXiv 2608.09867 *Stealing Reasoning Traces from Proprietary LLM APIs*, App. E.3.3 "Claude Opus 4.7: considers restricting the supported input range" (html fetched 18:07 -03, section located in the extracted text). It quotes a decoded trace on circuit-fibsqrt: "What if I do 2 iterations per step, then cheat by limiting to N<=2^30 , so isqrt<=32768?" (19 words) and then rejects it: the task says fib(isqrt(N)) and tests "probably include large N". This is an agent *considering* a range cut, in reasoning, with no grader reading. It is not a lookup and not a grader finding. E.3.1 (the section a web_search claimed was circuit-fibsqrt) is a quantum-factoring prompt (Qiskit, N=15) — verified in the fetched text.

### 2 — stdin vs argv

Not found as a finding. Agents hit it privately: the tmax-9b and zxss702 traces restate "first 32 lines … stdin" and then "where N comes from command line argument", and Qwen3.5-9B (tmax) says "Wait, I need to re-read the problem" before reading `sim.c`. Those are agent transcripts, not published reports. The Gemini CLI leaderboard trajectory prints `sim.c` lines 322-331 including the comment "signal 0 gets MSB, signal 31 gets LSB" over `(input_value >> i) & 1` (the entry's unexercised second contradiction), again unremarked. The contradiction is in the legacy repo's own text (`legacy/circuit-fibsqrt/instruction.md`, wave-1). An answer engine volunteered the argv/stdin mismatch from reading the files; that is a derivation, not a publication.
Queries: GitHub issue searches (wave-1, all four task repos + global), code search `circuit-fibsqrt instruction stdin argv`, HF `harborframework/terminal-bench-2.0` discussions (#1 eval.yaml, #2 rename, #3 define harbor: none on this task); `harborframework/terminal-bench-2-leaderboard` has discussions **disabled** (`{"error":"Discussions are disabled for this repo"}`, 18:11 -03), so no hidden threads exist there; `zai-org/terminal-bench-2-verified` discussions #1/#2 (README, polyglot-rust-c); `harborframework/terminal-bench-2.1` #1 (a submission).

### 3 — last 32 lines vs highest index
Not found. Searches `fibsqrt sim.c num_signals highest index last 32` (6 hits: lane files + three trajectory logs; the trajectory hits contain `num_signals` in pasted `sim.c` source only). No source discusses that file order does not matter or that the print window is the 32 highest indices.

### 4 — 208/20000 not graded
Published: Gabor audit :460, "Example values from problem not directly tested: N=208 and N=20000 mentioned in the problem aren't in the test suite" (25 words; fetched 18:10 -03). Same provenance caveat as wave-1: LLM auditor, and the audit calls it minor.

### 5 — compile into cwd / overwrite `/app/sim`
Not found. `kimjune01/terminal-bench-audit` (`nuke-preexisting` FRAME_BLIND, wave-1) is a different finding. Code searches `circuit-fibsqrt "gcc -O3" sim cwd` (22 hits: lane files, task-instruction copies (`lhannnn/agentic-abstention`, `strands-labs/benchmark-harnesses`, `AbyssCN/oh-my-dag`), Sorting-Hat job logs): none discusses the compile destination.

### 6 — whitespace parse
Not found. Code search `gates.txt "out0 = out0" trailing space` (4: lane entry, `zxss702` swe-agent log, `voctory/tbench-runs` GPT-5.2 codex logs); the two non-lane trajectory hits are agents writing gates, not reports about trailing-space behaviour. I did not open the `voctory` Codex logs (large; a trajectory, not an audit) — a finding stated only inside it would be missed.

## Does S128 say what the entry says it says?

Fetched `gh api repos/OpenAgentsInc/openagents/issues/9645` at 18:03:43 -03 and the linked doc at `0712c6176cd47a3d82df13a350fe63efcf0a276b`.

| S128 row / entry claim | Check |
|---|---|
| title “Audit circuit grader coverage beyond its 48,401 input ceiling” | issue title matches (JSON `t` field) |
| created 2026-09-25T09:01:50Z, closed 09:11:26Z, state closed | `created_at`/`closed_at`/`state` = identical; `state_reason` = `completed` |
| quote “The official grader exercises 28 values, none above 48,401.” (9 words) | in issue body paragraph 1, **body line 3** (`gh api … --jq .body | cat -n`, line 1 is `## Problem`, line 2 blank) — exact |
| "real agent circuits that pass the 28-value table and are wrong above it" | body says: flags all three Luna candidates "which the official grader passes"; "Retained review commands show wrong answers above that range" — supported by the body. The per-candidate counts (3/6/2 extra mismatches) and "executor Luna/Astra" are in the linked **doc** (table, Circuit audit section), not the issue; S128's locator names only the issue |
| "builds no lookup circuit and names none of the parse, ordering or cwd mechanics" | true of the body; body "Work" section is a task list ("Document the coverage gap and a reproducible regression …") |

Two precision gaps, neither fatal:
- **A.** The issue is a *claim/work ticket* by the OpenAgents team's own tracker, closed by a single comment from `AtlantisPleb` 9 min 36 s after creation, not a report filed with Terminal-Bench. "A third party's published report on this task's grader coverage" is true of the doc, which is a post-label audit of OpenAgents' own prediction run. The row's tier B label is fine; "report" slightly overstates the issue itself.
- **B.** The doc's nine extra inputs include zero and square boundaries (doc: "including zero, square boundaries, one million, `2^24`, and `2^32−1`"). It names only N=16,777,216 as a wrong value (Luna circuits return 0 vs 1,501,401,659). So "wrong above it" is exactly supported for the 2^24 case and by the issue's sentence; the mismatch lists of 3/6/2 do not say which of the nine failed. The row should not be read as "every mismatch is above 48,401".

## Entry and README text to correct (advice for the L1; not edited)

1. `README.md:371` (and the entry's integration bullet) credit S128 alone with the range gap. Add: the Gabor audit :461-462 published "No very large N values: Near 2^32 range not tested" and "Maximum isqrt tested is 220" on 2026-01-20, and :459 N=0. The coverage gap is therefore published 8 months before S128 (LLM-written, tier C).
2. Entry §Prior art (line 364) cites the audit as `audit_results/audit.txt`; the real path is `audit_results/20260120_125158/audit.txt` (the tree has no top-level `audit.txt`). The integration bullet at line 443 already has the right path; the §Prior art paragraph is stale beside it (still says the sentence is "not re-fetched" and that "I ran no tracker search"). Fetched and quoted now: :454 and :466 quoted above.
3. Optional: the arXiv 2608.09867 E.3.3 trace is a published agent *considering* a range cut on this task; adjacent, not the lookup construct. Do not cite E.3.1.

## Limits of this search
GitHub issue/code search, `gh api` repo contents, HF API, arXiv html (only the papers listed), a handful of web_search answers. Not covered: OpenReview PDF (challenge-blocked), X/Twitter, the full `voctory`/other trajectory dumps, Google Scholar, the Harbor hub task page text for a "reward hack" note, full-text of all 3,348 global code hits for `circuit-fibsqrt`. A finding that lives only inside a trajectory transcript or a closed-door audit would be missed.

VERDICT: prior-art-wider-published-2/6
