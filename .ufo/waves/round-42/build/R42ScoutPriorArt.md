# R42ScoutPriorArt — prior art for the C2 `circuit-fibsqrt` findings

Seat: scout (leaf, read-only). Window: 2026-10-26 17:20:45 → 17:27 -03 (`date +%T` at start 17:20:45, end 17:26:59).
Scratch: `/fast/scratch/hyaku/kengaku-r42/R42ScoutPriorArt` (clones + raw search output; deleted at the end). Nothing was written to the lane, `~/.local/bin`, or fleet root.
`ls -A /home/vgpnk/.local/bin | sha256sum` before = after = `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18`.
Envelope note: this seat ran no counter, battery, or fixture build (network reads and `git clone` into scratch only), so the bwrap envelope did not apply; no file was written outside scratch and the report path.
Tools: `gh` 2.x (already installed, authenticated as VeigaPunk), `curl`, `git`. Nothing installed.

## Verdict table

| # | Finding | Prior art | Strength |
|---|---|---|---|
| 1 | lookup / hard-coded circuit passes the 28 fixed inputs | **Adjacent, published:** the 28-input / max-48,401 coverage gap and real circuits that pass it while wrong above it. **The lookup construct itself: not found.** | counted as published in the weaker (coverage-gap) form |
| 2 | instruction says stdin, sim.c reads argv | not found | — |
| 3 | "the last 32 lines" vs 32 highest-indexed signals | not found | — |
| 4 | instruction examples 208 / 20000 not graded | **published** (LLM-generated audit committed to GitHub, 2026-01-20) | published, with a caveat on provenance |
| 5 | grader compiles sim into cwd and runs /app/sim | not found | — |
| 6 | whitespace sensitivity of sim.c parser | not found | — |

Strict count (the exact claim as worded in the task) = 1/6 (finding 4). Count including the weaker coverage-gap form of finding 1 = 2/6. The terminal verdict uses 2/6; finding 1's lookup circuit stays novel.

Grader on TB2.1 main: **byte-identical to the pin** (section "Pin check").

## Per-finding detail

### (1) Lookup / hard-coded circuit passes the 28 fixed inputs

**Published, adjacent (coverage gap, not the lookup construct).**
- URL: https://github.com/OpenAgentsInc/openagents/issues/9645 (closed 2026-09-25; comment at 09:11:26Z) and https://github.com/OpenAgentsInc/openagents/blob/0712c6176cd47a3d82df13a350fe63efcf0a276b/docs/terminal-bench/2026-09-25-archive-check-confirmation.md ("Circuit audit" section, ~lines 146–176). Both accessed 2026-10-26 17:24–17:25 -03 via `gh api`.
- Quote (issue body): "The official grader exercises 28 values, none above 48,401. Retained review commands show wrong answers above that range."
- Quote (doc): "All three Luna circuits return zero for `N=16,777,216`; the independently computed required result is **1,501,401,659**."
- What it establishes: three real agent-produced circuits (Luna executor) passed the official grader and are wrong on 3, 6 and 2 of nine extra inputs; its sim.c digest `700645ac…796173` equals the pin's (so the same simulator and the same 28-value table). It also notes that the 28 values are only a subset of the 32-bit domain.
- What it does not do: build or grade a lookup / hard-coded circuit, claim a circuit can pass by encoding exactly the 28 graded inputs, or report the 1195-line figure. Greps of the document for `lookup|hard-?cod|table|stdin|argv|last 32|208|20000|trailing|whitespace|CRLF|blank|/app/sim|compile|gcc|cwd` returned only the 28 / 48,401 lines (doc lines 25, 152, 178).
- Opposite statement, also published: https://github.com/JonathanGabor/terminal-bench-2-audit (commit `35f110397bc8ea58538424a1951760a9c5a0a710`), `audit_results/20260120_125158/audit.txt` line 454: "Hardcoding prevention: 28 distinct test cases with varied inputs make hardcoding impractical". It rated the task 4 (`ratings.json` line 11). This is an LLM-generated audit (the text opens "Looking at this task, I need to evaluate…"), not a human finding. A web_search synthesis (answer engine, not a primary source) also asserted "A lookup-table-only solution is not viable" for a full 2^16-entry ROM; that claim is about a full ROM and does not address the 28-input case.

Queries run (all `gh api -X GET search/issues -f q=…`, 2026-10-26 17:20–17:25 -03):
- Repos: `harbor-framework/terminal-bench-2` (circuit-fibsqrt, fibsqrt, gates.txt, "circuit fibsqrt", sim.c, gates, stdin, lookup, hardcode, isqrt, circuit → all total 0 for fibsqrt/gates/sim.c/isqrt/circuit; hardcode=5, lookup=1, stdin=1: PRs/issues #84, #86, #53, #28, #32, #79, #73, none about this task).
- `harbor-framework/terminal-bench-2-1` (circuit-fibsqrt / fibsqrt / "circuit fibsqrt" / "circuit" → 4 hits, all leaderboard-submission PRs #44, #140, #206, #208; PR #44's files and comments contain no finding about the task (one trial row: "circuit-fibsqrt · CancelledError"); gates.txt=0; hardcode=5 (#135 schemelike-metacircular-eval, #242 modernize-scientific-stack, #5), lookup=4 (#239 sanitize-git-repo): not this task).
- `harbor-framework/terminal-bench` (the legacy repo; same queries → 0 for circuit-fibsqrt/fibsqrt/gates.txt/sim.c/isqrt; broad words give hundreds of unrelated task-PR hits). `laude-institute/terminal-bench*` returned HTTP 422 (repo no longer resolvable under that owner).
- `harbor-framework/harbor`: circuit-fibsqrt → #565 (procps/Claude Code KillShell) and PR #60 — not about grading.
- Full title lists of both repos (`gh api --paginate repos/<r>/issues?state=all`, 247 and 89 rows) grepped for `circuit|fib|sqrt|gates|sim|logic|simulat|example|stdin|argv|last 32|whitespace|trailing|crlf|/app/sim`: only TB2.1 #241 "Fix whitespace-sensitive ARS verification…" (adaptive-rejection-sampler, not this task) and TB2 #13 (a README link).
- Global issue/PR search: `circuit-fibsqrt` (total 86 — mostly agent-harness repos listing the task name; relevant: OpenAgents #9645; RyanMarten/terminal-bench-3 PR #10 "Add circuit-fibsqrt task", body "Task imported from terminal-bench-2 for QA testing", no content); `circuit-fibsqrt hardcode lookup table gates.txt` (0); `circuit-fibsqrt instruction stdin argv` (2: tb-3 PR #10, fw-ai/cookbook #692, neither on topic); `circuit-fibsqrt reward hack` (6: the same leaderboard PRs plus unrelated agent-run repos); `circuit-fibsqrt grader weak` (0); `fibsqrt sim.c trailing whitespace` (0); `fibsqrt "gcc -O3" "/app/sim"` (0).
- Global code search: `circuit-fibsqrt` (3348 files: task copies, skill registries, trajectory dumps) and `fibsqrt` (3888); `sim.c "gates.txt" "out%d"` (74; first hits are this lane's own `plans/fibsqrt_probe.py` and `.ufo/waves/round-42/make_build_spec.py` indexed at commit `fda71ae0…` — self-references, excluded — and agent trajectories in UkisAI/Swift-Qwen3.8-27B-evals). I did not read the trajectory dumps or the skill-registry SKILL.md files (the registry page is a stub pointing to a data repo); a finding stated only inside a trajectory would be missed by this search. [INFERENCE: low probability, since trajectories are agent transcripts, not audits].

### (2) instruction.md says stdin, sim.c reads argv

**Not found** as a published finding.
- Source fact, for the record (pin and TB2.1 main identical): `instruction.md:8` "Initially, the first 32 lines are defined by the binary representation of stdin." and `sim.c:324` `input_value = (unsigned int)strtoul(argv[1], NULL, 0);` (read from the TB2.1 main clone, `grep -n 'argv\|stdin' tests/sim.c`). The same file's line 10 says "the provided example /app/gates.txt file prints outputs argv[1]/2", and line 11 says "when you call /app/sim N", so the instruction contradicts itself, which any prior mention would have to address.
- The legacy repo carries the same text (`harbor-framework/terminal-bench` @ `e67a2cb7db4d9795c212909b3395d8c22ad60aec`, `legacy/circuit-fibsqrt/instruction.md:8-10`, tests sha equal to the pin), so the inconsistency is inherited, not introduced by TB2.
- Queries: the issue searches above (`stdin`, `circuit-fibsqrt instruction stdin argv`) in all four repos plus global; the JonathanGabor audit text for circuit-fibsqrt (audit.txt lines 429–470) lists "Missing N=0", "Example values … not directly tested", "No very large N", "Maximum isqrt tested is 220" — nothing about stdin/argv; HF `zai-org/terminal-bench-2-verified` discussions (#1 README, #2 polyglot-rust-c); `harborframework/terminal-bench-2.0` discussions (#1–#5, none on this task); `harborframework/terminal-bench-2.1` discussion #1 (a submission).

### (3) "the last 32 lines" vs the 32 highest-indexed signals

**Not found.** Same queries as (2) plus `circuit-fibsqrt "last 32"` (GitHub returns 3.6 M generic "last 32" hits; the only relevant first hit is tb-3 PR #10 whose body has no content). Source fact (pin = TB2.1 main = legacy): `instruction.md:9` "the last 32 lines are converted to an integer and printed to stdout" against sim.c printing the 32 highest-indexed signals (per the frozen claim; I did not re-derive it here).

### (4) The instruction's examples 208 / 20000 are not graded

**Published.**
- URL: https://github.com/JonathanGabor/terminal-bench-2-audit/blob/35f110397bc8ea58538424a1951760a9c5a0a710/audit/audit_results/20260120_125158/audit.txt (lines 460, section "Potential Weaknesses"); run dir `20260120_125158` (=2026-01-20 12:51:58); repo last pushed 2026-01-24T01:06:43Z. Accessed 2026-10-26 17:22 -03 (local clone, `grep -n`).
- Quote: "Example values from problem not directly tested: N=208 and N=20000 mentioned in the problem aren't in the test suite".
- Provenance caveat: the text is an LLM-generated rating of 89 tasks (circuit-fibsqrt scored 4 on the audit's scale), published as raw audit output; the same passage calls the weakness minor and concludes that "gaming the tests [is] nearly impossible" — opposite to what the lane's receipt shows (a lookup circuit with 208 → 0 passes 3/3).
- The OpenAgents doc/issue (finding 1) shows the 28-value table (none above 48,401) but does not mention 208 or 20000.
- The task's own files show it indirectly: `instruction.md` lists both examples; the lane capture `test_outputs.py` contains neither number (`grep -n -E '\b(208|20000)\b' corpus/evidence/round42/tb2-circuit-fibsqrt/test_outputs.py` printed nothing).

### (5) Grader compiles sim into the cwd and runs /app/sim

**Not found.** Queries: `fibsqrt "gcc -O3" "/app/sim"` (global issues, 0); the circuit-fibsqrt issue lists above; the kimjune01 repo (below). No issue, PR, or audit mentions that `gcc -O3 /tests/sim.c -o sim` runs in the cwd or that a pre-planted `/app/sim` is replaced / ignored.
- Nearest adjacent: https://github.com/kimjune01/terminal-bench-audit (commit `bbe0f8c39fc291e3c3eb20bb0dc47c1c861d5d23`, 2026-07-20), `results/verdicts-2.1.jsonl` lines 46–50 and `WORKLOG.md:80-89`. Quote (WORKLOG.md:83): "`nuke-preexisting`: **19 FRAME_BLIND / 11 caught**". For circuit-fibsqrt the row reads `"mut":"nuke-preexisting","applied":"yes","reward":1,"deleted":1,"verdict":"FRAME_BLIND"`: the grader still passes after pre-existing /app data is deleted. That is a different finding (task certifies completion regardless of deleted workspace files; the oracle regenerates gates.txt) and says nothing about the compile or `/app/sim` path. I count it as not prior art for (5).

### (6) Whitespace sensitivity of sim.c's parser

**Not found.** Queries: `fibsqrt sim.c trailing whitespace` (0), `circuit-fibsqrt` + `trailing|CRLF|blank` in the title scan (0), the OpenAgents doc grep (0), the JonathanGabor audit text (0). The only whitespace-related hit anywhere in the two benchmark repos is TB2.1 #241, "Fix whitespace-sensitive ARS verification and add verifier regression CI" (open), which concerns the `adaptive-rejection-sampler` task, not this one. Source fact for (6): sim.c's parse is `sscanf(line, "out%d = %[^\n]", …)` (line 113), with later `sscanf(op, "out%d %c out%d", …)` (line 156); the exact trailing-space behaviour is measured in the lane's receipt, not here.

## Pin check — is the TB2.1 main grader byte-identical to the pin?

Yes. `harbor-framework/terminal-bench-2-1` main = `7131e4375048a0e408a8fb404b5f499d726b695b` (2026-08-11T20:46:41Z; GitHub API `commits/main` at 17:27, same as the local `git rev-parse HEAD`). Command: `sha256sum tb21/tasks/circuit-fibsqrt/{tests/*,instruction.md,README.md,task.toml,solution/solve.sh,environment/Dockerfile,environment/gates.txt}` against `git -C tb2 show 2fd12b88…:circuit-fibsqrt/<f> | sha256sum` and against the lane captures `sha256sum corpus/evidence/round42/tb2-circuit-fibsqrt/*`:

| File | sha256 (TB2.1 main = TB2 pin = lane capture) |
|---|---|
| tests/test_outputs.py (S125) | `6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438` |
| instruction.md (S126) | `a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea` |
| tests/sim.c (S127) | `700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173` |
| tests/test.sh | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` |
| solution/solve.sh | `a4ffab4183815a0eb7646abc1de1fc67695014c060d7ff16e8bca9ec94385d0b` |
| task.toml | `9f5aa1f7ebbbcec90fd109121e9bd509af3cfff6b4cec701bd91947988f40972` |
| environment/Dockerfile | `780c23986778f3e5f842567868af30b1135ed095ca9449e1c90b7f0e0483d3d4` |
| environment/gates.txt | `032786f94f16605767c62bb61ce4dbba7ab7d3f1046712c975f01c9a04b6ad29` |
| README.md | `201f7c889dd6f73dd83ca078e347272b33720fa622f8c757ea6d5770453f4cbd` |

Additional equalities found:
- The pin's TB2 repo main is also `2fd12b88…` (`git -C tb2 rev-parse HEAD`, 2026-10-26; commit date 2026-04-29), so the pin is the current TB2 tip. TB2.1's full history for the task dir is one commit, `5fc7d3b` "Move dataset files under tasks" (`git -C tb21 log --oneline -- tasks/circuit-fibsqrt` after `git fetch --unshallow`), which adds every file; so TB2.1 never edited the grader after import, consistent with the equal digests above.
- At the pin, `circuit-fibsqrt/environment/tests/{sim.c,test_outputs.py}` exist and hash-equal `tests/…`; i.e. the grader's test_outputs.py is also under the agent-visible `environment/` directory in the repo. The Dockerfile copies only `tests/sim.c` and `gates.txt` into /app (`COPY tests/sim.c /app`; comment: "Copying tests/sim.c is allowed for the agent to check its work"), so the grader's table is not in the image from the Dockerfile alone; the repo copy is a leak-by-publication only. [Not asserted as a finding; not in any claim.]
- Legacy repo `harbor-framework/terminal-bench` @ `e67a2cb7…` (2026-10-22): `legacy/circuit-fibsqrt/{tests/sim.c,tests/test_outputs.py,instruction.md,…}` all equal the pin (sha prefixes `700645ac`, `6117b8ed`, `a7f50026`).
- HF `zai-org/terminal-bench-2-verified` (sha `2d28949d…`, lastModified 2026-08-24): `circuit-fibsqrt/instruction.md`, `tests/sim.c`, `tests/test_outputs.py` fetched via `resolve/main` hash-equal the pin. The dataset README lists circuit-fibsqrt only under "procps + python3 + python3-pip installation (All 89 Tasks)" — a Dockerfile change; its text says "instructions and tests remain unchanged". So that "verified" copy did not touch the grader.
- OpenAgents' pin at legacy path `archive/circuit-fibsqrt` (commit `3b5caaa4…`) reports sim.c sha `700645ac…796173` (its doc line 152), the same.

## Net for the entry

- Do not claim novelty for "the grader tests only 28 inputs": published 2026-09-25 (OpenAgents #9645) and "examples not graded" 2026-01-20 (JonathanGabor audit, LLM-generated).
- Safe novelty (not found in any searched source): a concrete lookup circuit built for exactly the 28 graded inputs passing 3/3 while failing the instruction's own examples; the argv/stdin contradiction; "last 32 lines" vs highest-indexed signals; grader recompiles into the cwd and overwrites a fake `/app/sim`; trailing-space / CRLF / comment / blank-line behaviour of the parser.
- Citation hygiene: the JonathanGabor audit asserts the opposite of the lane's lookup result ("hardcoding impractical"); cite it as an LLM-generated audit.
- Limits of this search: GitHub issue/code search and HF API only; no Google Scholar / arXiv / blog search beyond one web_search query (answer-engine output, discarded as non-primary); trajectory dumps and skill-registry files not read; `laude-institute/*` repos were not resolvable (422).

VERDICT: prior-art-published-2/6
