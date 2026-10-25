source: S077 — https://raw.githubusercontent.com/harbor-framework/terminal-bench/e67a2cb7db4d9795c212909b3395d8c22ad60aec/docs/TASK_REVIEW_AUTOMATION.md — `### Static Checks` → `#### check-canary` (line 95) and the §Pipeline Overview rows at lines 29 and 31 — commit `e67a2cb7db4d9795c212909b3395d8c22ad60aec`
source: S078 — https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/README.md — §What changed from v1 (line 99) and §The locked protocol (line 75); `v2/GATE.md` line 1 heading dated 2026-09-22 — commit `66f92766bba642462d4bbe5479e83f91f9211862`
source: S079 — https://github.com/laude-institute/terminal-bench-2 — `protein-assembly/task.toml` lines 1, 15, 18, 19, 22 — commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`
source: S080 — https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/README.md — §News line 27; `tasks/finalpool/ab-testing/task_config.json` lines 2-12 — commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`
source: S090 — https://www.tbench.ai/news/announcement-2-0 — `## Terminal-Bench 2.0` body paragraph and closing canary banner — page as served 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-fetch S077, S078, S079, S080 and S090 at their pinned revisions and re-run the two counts named under §Counts (next due 2027-04-23)

# Benchmark task-validity checklist

The lane's frontier named this instrument: "the lane has no instrument that audits a
benchmark's task specs, graders, and contamination separately … turned into a
per-benchmark task-validity checklist" (`corpus/README.md` §Frontier). Three benchmark families —
and three maintainer organisations behind them, since Harbor, Laude Institute and tbench.ai are one
project — publish enough primary material to build the checklist from evidence rather than from
principle. Each axis below is stated once, and each is **observable**: the axis either
has a named artefact in a published tree, or it does not.

This entry extends `knowledge/agent-time-horizon-and-task-validity.md` (benchmark task/test validity
audits) and `knowledge/contamination-detection-and-transparency.md` (contamination vocabulary), and
supersedes neither. It is a synthesis of primary maintainer documents, not a new research method. Its
contribution is the mapping from "what a validity question is" to "the artefact that answers
it, and where that artefact lives".

## The checklist

| # | Axis | What a reviewer looks for | Evidence |
|---|---|---|---|
| A | Instruction–grader traceability | every graded assertion traces to a sentence in the instruction, and every behaviour the tests check is described there | S078 §What changed from v1; S077 `check-test-file-references` |
| B | Solvability | the maintainer's own reference solution passes every test | S077 `Oracle Validation` row; S078 gate oracle cell (below) |
| C | Non-triviality | an empty patch fails every test | S077 "Doing nothing fails tests"; S078 gate nop cell (below) |
| D | Environment stability | the task does not change underneath the agent between runs | S090 "in download-youtube YouTube's constantly changing anti-bot protections meant that a solution that worked one day might not work the next." |
| E | Grader isolation | the verifier does not run inside the agent's sandbox, and hidden-test paths are restored or removed before the test patch applies | S078 "The verifier never runs in the agent's sandbox." (line 75) and "hidden-test paths are restored or removed before the test patch is applied" (line 103) |
| F | Non-cheatability | adversarial cheat trials are run and adjudicated, and cheat artefacts are not shipped | S077 "Adversarial reward-hack detection"; S078 sanitised-history clause |
| G | Contamination control | a per-task canary is embedded in the task files and checked mechanically | S077 "Prevents training data contamination by ensuring a unique canary string is present in task files."; S090 canary GUID banner |
| H | Declared task fields | schema version, difficulty category, human expert and junior time baselines, verifier timeout, all present and typed | S079 `schema_version = "1.1"`, `difficulty = "hard"`, `expert_time_estimate_min = 60.0`, `junior_time_estimate_min = 300.0`, `timeout_sec = 1800.0` |
| I | Declared tool surface and state-based grading | the task declares which servers and local tools it needs and ships an evaluation directory rather than a judge prompt | S080 `needed_mcp_servers`, `needed_local_tools` in `task_config.json` |
| J | Reproducible release | the published tree is checksummed and the release gate is dated and states its hardware and check set — re-running it needs that hardware, not a laptop | S078 `v2/GATE.md` heading dated 2026-09-22 and line 3 naming Harbor 0.22 on Modal, the oracle and nop cells, plus `v2/SHA256SUMS` |

## What the maintainer artefacts actually say

- S078's release gate ships both triviality bounds together: the reference patch row reads
  "**642 / 642** tasks resolved" and the empty-patch row reads "**642 / 642** tasks unresolved
  (0 spurious passes)" — that is, zero of 642 tasks resolved by an empty patch. Axes B and C are
  therefore checkable on one page, per release.
- S077's pipeline runs the static checks (including the canary) automatically on every PR,
  while cheat trials are on demand, not per-PR (`/cheat`, line 31; maintainer dispatch line 252).
  Adjudication is a separate LLM pass over the trajectory: "The LLM-based analysis determines
  whether actual hacking occurred." (line 301), so axis F needs both the trial and its adjudication.
- S079 shows the fields axis H depends on are authored, not inferred: a task directory
  carries `schema_version = "1.1"` and both time baselines, so a reviewer reads the claim
  instead of guessing it. Coverage is **not** universal: at the pin 1 of 89 task
  directories (`caffe-cifar-10`) carries `schema_version` and `difficulty` but neither time
  baseline, and 6 lines across 3 tasks write integer literals (`30`) where the schema
  elsewhere uses floats (`30.0`). Axis H must therefore treat a missing field as a finding,
  never as an assumption about the tree.
- S080 shows axis I is checkable in the tree: `needed_mcp_servers` and `needed_local_tools`
  are declared per task, and the graded state ships beside the task.
- S090 is the one axis-B/C-passing task that still failed after publication: axis D is a
  property of the world, so no pre-publication check can retire it.
- Axis E is scoped to the harness that publishes the claim. S078 states isolation for its
  locked release protocol; a harness that runs the verifier in a shared environment by
  default does not inherit that property, so "verifier isolated" must be read per benchmark,
  never as a general fact about benchmark releases.

## Counts (re-derived 2026-10-25, not copied from the package)

- S079 repository at `2fd12b8`: **92 root entries**, of which 3 are files (`.gitignore`,
  `LICENSE`, `README.md`), leaving **89 task directories and 89 `task.toml` files**
  (`git/trees/2fd12b8` non-recursive, then `task.toml` count over the recursive tree).
- S080 at `9be8d8f`: **109 entries under `tasks/finalpool`**, of which **108 are
  directories** (`contents/tasks/finalpool?ref=9be8d8f`).

Both counts correct the staged package, which said "92 top-level task directories" and
"109 task directories". The package's *claims* were right; its *units* were off by the
file/directory split. A row that carries a count must carry the command that produced it.

## Application to the named benchmarks

- **Terminal-Bench 2.0** — S077 and S090 together cover A, B, C, D, F, G; the repo is not
  graded by a shipped gate document, so J is open for it on the evidence opened here.
- **SWE-bench Pro V2** — S078 covers A, B, C, E, F (partly), J; the gate is dated and
  re-runnable, so a reviewer can re-derive the release rather than trust the post.
- **Toolathlon-Verified** — S080 covers B (via the verified release), I; the declared
  tool surface is the axis this benchmark makes mechanical.

## Prior art (priced 2026-10-25)

This checklist is **INCREMENTAL**, not a new instrument. The Agentic Benchmark Checklist (ABC, arXiv
2507.02825, Zhu et al., NeurIPS 2025) publishes a per-task validity instrument whose Task Validity
criterion is the same construct: "we introduce the Agentic Benchmark Checklist (ABC), a set of
guidelines that we synthesized from our benchmark-building experience". ABC's items cover axes B,
C, D, E, F, G and I at item level, and the benchmark this entry's S077 comes from applies ABC to
itself. What this entry adds is therefore **application work**: the A–J axes mapped to the
publisher's own artefact and locus for Terminal-Bench 2.0, SWE-bench Pro V2 and
Toolathlon-Verified, with the counts re-derived. The pricing row is S091 and the located quote,
anchor and rejection reasoning live in `corpus/lessons/round-29.md` §Attempt 2.

## What this does not establish

- **Not task validity itself.** The checklist names where to look; it does not run a
  benchmark or certify any task. A task can pass all ten axes and still be invalid for a
  reason no published artefact records.
- **Not contamination measurement.** G reads a maintainer's canary practice *inside its own
  repository*; it is not a detector, a canary's absence is not evidence of contamination, and a
  canary's presence is detectability, never proof of training-corpus exclusion. Applied to the
  pinned Terminal-Bench 2.0 tree, Harbor's literal `harbor-canary` string occurs in 0 of its files:
  the instrument a maintainer runs on its own submissions does not automatically apply to the tree it
  publishes.
- **Not synthetic replication.** Running this lane's own fixtures against a check's shape would
  exercise the lane's code, not the maintainer's instrument; nothing here was re-run against a
  benchmark.
- **Not a model-performance or difficulty claim.** Axes B, C and H bound the instrument,
  not the models measured with it.
- **Not exhaustive.** Four maintainers were opened; other benchmarks may have instruments
  these rows do not cover, and no absence is claimed for unopened benchmarks.
- **Not instrument novelty.** ABC already publishes the construct; a reader who wants the
  checklist itself should read ABC, and this entry is the per-benchmark application of it.
- **Falsifier.** A benchmark whose released gate document contradicts its own task tree on
  any of the cells quoted here would falsify the axis's mapping to that artefact; a
  maintainer artefact that names a field present in no task in the tree would falsify H.
