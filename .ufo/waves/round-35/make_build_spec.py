#!/usr/bin/env python3
"""Renders .ufo/waves/round-35/build-spec.json (wave 1 of 2, policy v1, 32 seats)."""
import json
import pathlib

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
W = f"{L}/.ufo/waves/round-35"
B = f"{W}/build"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
CAP = f"{L}/corpus/evidence/round35/tb2-eval"
R34 = f"{L}/.ufo/waves/round-34"
PIN = "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly"
CLONE = (f'Fixture rule: D=$(mktemp -d /tmp/k35-XXXX); git clone -q --no-checkout --shared {L} "$D/lane"; '
         f'git -C "$D/lane" sparse-checkout set --no-cone <patterns>; git -C "$D/lane" checkout -q master; verify '
         f'`git -C "$D/lane" rev-parse --show-toplevel` equals "$D/lane" before any write; every git call names -C "$D/lane"; '
         f'never commit; copy uncommitted lane files you need (e.g. {CAP}/*, {L}/corpus/evidence/round35/tb2-grader-probe.txt) into the clone. rm -rf "$D" at the end.')

CONTEXT = f"""# Goal
kengaku round 35 (hyaku run 7, 2026-10-25), WAVE 1 of 2 (build + first falsifiers). Lane repo: {L}.
Two claims are FROZEN at {L}/plans/round-35-claims.md (freeze commit 11d64530179b78e33ba6074fc77d63d36ee7ac31) — read it first.
- C1 coverage: pinned Terminal-Bench 2.0 `protein-assembly` grader (terminal-bench-2 @ 2fd12b88aafdd04a52c298e3940bcb189f9766d6)
  admitted as corpus/knowledge/tb2-protein-assembly-grader.md with rows S105 (tests/test_outputs.py), S106 (tests/test.sh),
  S107 (instruction.md) and an executed offline probe: {L}/plans/tb2_grader_probe.py (18 frozen cases) whose receipt is
  {L}/corpus/evidence/round35/tb2-grader-probe.txt (`cases=18 observed_pass=5 observed_fail=13 mismatches=0`).
  Counter: `python3 plans/round35_c1_verify.py --lane .` (V1–V6, docstring). Captures: {CAP}/ (byte-identical to the pinned
  raw files; re-fetched 2026-10-25). Biopython for the grader: `uv run --no-project --with biopython==1.85 python3 ...`.
- C2 calibration: persistent routed-defect ledger {L}/corpus/defects.jsonl + checker {L}/plans/defect_ledger.py closing the
  five round-34 spot-check defects D1–D5 ({L}/corpus/lessons/round-34-verifier-spotcheck.md:75-79). Frozen predicate:
  `rows=5 closed=5 observed_pass=5 mismatches=0` + `PREDICATE C2 pass`.
- Controls already scored (all red): {W}/claims/control-*.txt.

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Any scratch/draft files go under {B}/<YourSeatName>/ (create it).
- Write ONLY inside {B}/ (your report + your own scratch dir) or a mktemp dir under /tmp. NEVER edit corpus/, plans/,
  SCORECARD.md, LOG.md, README.md, SKILL.md, PROVINCE.md, SHONEN.md or any other lane file — draft for the L1, who integrates.
  Never write into /home/vgpnk/Projects/shokunin (fleet root), sibling lanes, the lane's jj state, or the lane's Git index.
  Never run git add/commit/stash/checkout/reset/push or any mutating jj command in the lane.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY: never write/commit there; run no campaign tools.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read
  /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason).
  pacman transactions are PAUSED host-wide: install via uv tool / npx / an official binary into ~/.local/bin, or file an
  L0 question. Never run pacman -Sy/-Syu/-U/-R or name an already-installed package.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none,
  never stall in clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location
  (file:line or URL+section). Do not fabricate output; if something cannot be fetched or run, say so.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""

ITEMS = [
 # ---- executors (10) ----
 ("R35ReopenPins", "executor", ["coverage", "freshness"],
  f"Independently re-open the six pinned files at {PIN}/{{tests/test_outputs.py,tests/test.sh,instruction.md,task.toml,environment/antibody.fasta,environment/pdb_ids.txt}} with curl -fsSL into {B}/R35ReopenPins/. cmp each against {CAP}/<basename>; sha256sum all. Write a draft manifest {B}/R35ReopenPins/SHA256SUMS (sha256sum format, basenames) covering all six and run `cd {CAP} && sha256sum -c {B}/R35ReopenPins/SHA256SUMS`. Also confirm the /tasks/-prefixed URLs round 34 used return 404 (curl -s -o /dev/null -w '%{{http_code}}').",
  "VERDICT: reopen-<n_identical>/6-manifest-<ok|bad>"),
 ("R35ProbeRerun", "executor", ["coverage", "operability"],
  f"Re-run the frozen probe twice in the lane read-only: `cd {L} && uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane . > {B}/R35ProbeRerun/run1.txt` (and run2). Byte-compare both runs with {L}/corpus/evidence/round35/tb2-grader-probe.txt (cmp). Also run it in a fixture clone at the freeze commit with the uncommitted capture copied in, and with Python 3.13 (`uv run -p 3.13 ...`, the version test.sh pins) — record any byte difference and its cause.",
  "VERDICT: probe-deterministic-<yes|no>-py313-<same|diff>"),
 ("R35IndepGrader", "executor", ["coverage", "calibration"],
  f"Write an INDEPENDENT checker {B}/R35IndepGrader/indep.py that re-implements the grader's assertions from your own reading of {CAP}/test_outputs.py (own translation table, own window loop; do NOT import the grader or the probe's run_grader). Generate the 18 case contents by importing build_cases/components from {L}/plans/tb2_grader_probe.py, score each with your checker, and compare pass/fail and the first failing assertion class to the `observed=` and `assertion=` fields in {L}/corpus/evidence/round35/tb2-grader-probe.txt. Any disagreement is a finding against the probe or the receipt.",
  "VERDICT: indep-agree-<n>/18"),
 ("R35ProbeHarnessMut", "executor", ["calibration", "operability"],
  f"Attack the probe HARNESS ({L}/plans/tb2_grader_probe.py run_grader monkeypatches the module's Path). In copies under {B}/R35ProbeHarnessMut/: (a) break the patch so the grader reads a nonexistent path — the valid case must turn fail; (b) feed every case the valid content — mismatches must become >0; (c) tamper one byte of a copied test_outputs.py — the probe must REFUSE on digest. Run each with uv/biopython 1.85 and paste outputs. Goal: prove the harness actually grades the case bytes.",
  "VERDICT: harness-mutants-<detected>/3"),
 ("R35MutC1Quotes", "executor", ["calibration"],
  f"Attack C1 counter check V3 ({L}/plans/round35_c1_verify.py v3). In a fixture clone build a minimal entry at corpus/knowledge/tb2-protein-assembly-grader.md that passes V3 (correct triad lines, Negative space with 'falsif', ≥8 `| claim | “quote” | `file:line` |` rows quoting {CAP} files exactly). Then mutate one property at a time: quote off by one line, quote with one changed char, 26-word quote, curly vs straight quotes, missing falsifier, verified-at date changed, S106 line swapped with S105, recheck without cadence, quote citing a file outside the capture dir. Report which mutants V3 catches; any survivor is a false-green finding.",
  "VERDICT: v3-mutants-<caught>/<total>"),
 ("R35MutC1Rows", "executor", ["calibration"],
  f"Attack C1 counter check V2. In a fixture clone append three S105–S107 rows to corpus/SOURCES.md that pass V2 (URLs {PIN}/tests/test_outputs.py, {PIN}/tests/test.sh, {PIN}/instruction.md; tier A; status mined; opened 2026-10-25; used-by corpus/knowledge/tb2-protein-assembly-grader.md; 11 cells). Mutate one at a time: 10 cells, escaped \\| in a cell, /tasks/ path, #L anchor fragment on the URL, tier B, status queued, used-by with a second path, duplicate S105 row, row indented by 2 spaces, URL in a different cell order. Report caught/survived; also run `scripts/sources-census.sh validate --file` on each mutant registry.",
  "VERDICT: v2-mutants-<caught>/<total>"),
 ("R35MutLedgerD1D2", "executor", ["calibration"],
  f"Attack {L}/plans/defect_ledger.py checks r34_d1 and r34_d2. In a fixture clone (sparse: /corpus/ /plans/ /SCORECARD.md /.ufo/waves/round-34/assimilation/ /.ufo/waves/round-34/build/*.md): (a) create an untracked file under .ufo/waves/round-34/ → D1 must fail; an ignored __pycache__ file → D1 must stay as is (document); untracked plans/round34_mutate.py → fail. (b) D2 reads the committed branch tip, not the working tree: show that deleting mirror files on disk WITHOUT committing leaves D2 red, and that a fixture commit (in the clone only, identity `fixture <fixture@invalid>`) removing them turns D2 green. Paste outputs.",
  "VERDICT: d1d2-mutants-<caught>/<total>"),
 ("R35MutLedgerD3", "executor", ["calibration"],
  f"Attack check r34_d3. In a fixture clone holding {R34}/assimilation/captures/tb2-eval/: (a) append correct sha256 lines for test_outputs.py and test.sh to SHA256SUMS → D3 green; (b) wrong digest for test.sh → red; (c) listed file deleted → red; (d) only test_outputs.py listed → red; (e) path written as ./test.sh or with `*` binary marker → document behaviour. Paste the exact two manifest lines the L1 should append (computed with sha256sum).",
  "VERDICT: d3-mutants-<caught>/<total>"),
 ("R35MutLedgerD4D5", "executor", ["calibration"],
  f"Attack checks r34_d4 and r34_d5. Fixture clone. D4: append the correction line form `- **D4 correction (round 34 C2):** ...` with all four tokens → green; drop each token in turn → red; two correction lines → red; alter R34C2CounterDraft.md line 8 in the fixture → observation red. D5: add an erratum line `Erratum (round 35): ... nec-s091-reopen.html ... present ...` to corpus/lessons/round-34.md and a `## Mistakes` table row naming S091 in corpus/lessons/round-35.md → green; remove each → red; corrupt the quote inside the fixture's nec-s091-reopen.html → red. Report survivors (e.g. a Mistakes row outside the table).",
  "VERDICT: d4d5-mutants-<caught>/<total>"),
 ("R35IdGuard", "executor", ["calibration", "coverage"],
  f"Run the addendum §10 id-collision check exactly, with A={W}/assimilation (mkdir -p): reg-ids from {L}/corpus/SOURCES.md and staged-ids from /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md using the 0–3-space pattern `^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}`, comm -12 → $A/collisions. Prove the guard: a scratch registry under $A/guard-proof/ with an indented `  | S002 |` row and a staged copy containing S002 must yield nonempty collisions. Also derive the quarantine slice with the §10 awk over /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md into $A/quarantine-slice. Paste counts and both id lists' sizes.",
  "VERDICT: collisions-<n>-guard-<ok|broken>-slice-<n>"),
 # ---- scribes (6) ----
 ("R35EntryDraft", "scribe", ["coverage", "depth"],
  f"Draft the C1 knowledge entry at {B}/R35EntryDraft/entry.md. It must satisfy counter V3/V5 exactly (read {L}/plans/round35_c1_verify.py): lines 1–3 `source: S105 — {PIN}/tests/test_outputs.py — <anchor>` / S106 test.sh / S107 instruction.md (URL must be the bare pinned URL, no fragment); line 4 `verified-at: 2026-10-25`; line 5 `recheck: 180d — <action>`. Sections: summary; load-bearing grader logic; instruction-requirement → assertion map built from the probe receipt {L}/corpus/evidence/round35/tb2-grader-probe.txt (include its summary line `cases=18 observed_pass=5 observed_fail=13 mismatches=0` verbatim, and findings such as: a G-only linker passes; the 3000-nt cap cannot decide any otherwise-passing gBlock since max_passing_nt=2766; a one-residue donor substitution fails with the *order* message; the donor-repeated case fails on length first; expected proteins are literals, environment files are never read); `## Negative space` with an explicit falsifier sentence; `## Located quotes` table rows of the exact form `| claim | “quote” | `test_outputs.py:NN` |` (≥10 rows, each ≤25 words, quote copied byte-exact from {CAP}/<file> at that line). Fix every finding in {R34}/build/R34CriticEntryTB2.md and R34ReviewEntryTB2.md (no S092/S100 assertions without quotes; name the extended coverage row = corpus/README.md §Frontier round-33 clause; label sources: maintainer task code, not independent). Self-check every quote with grep -nF against the capture.",
  "VERDICT: entry-drafted-<n_quotes>-quotes"),
 ("R35RowsDraft", "scribe", ["coverage"],
  f"Draft the three registry rows S105–S107 for {L}/corpus/SOURCES.md in its exact 11-column schema (read its header and the last 5 rows; CORPUS.md SOURCES contract at /home/vgpnk/Projects/shokunin/CORPUS.md §SOURCES.md). source = title + ' — ' + bare pinned URL ({PIN}/tests/test_outputs.py etc.), kind code/docs, tier A, scope (maintainer's task-grader code for this one task), anchor (lines), teaches, status mined, opened 2026-10-25, recheck 180d, used-by corpus/knowledge/tb2-protein-assembly-grader.md. No literal or escaped `|` in any cell. Also draft the lesson `## Gate` source block: per row URL, access date 2026-10-25, a ≤25-word located quote you verify with grep -nF against {CAP}. Validate in scratch: copy {L}/corpus/ to {B}/R35RowsDraft/validate/corpus/, insert rows at the end of the Registry table, run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file {B}/R35RowsDraft/validate/corpus/SOURCES.md` (exit must be 0; paste output).",
  "VERDICT: rows-drafted-census-<exit>"),
 ("R35ReadmeDraft", "scribe", ["coverage"],
  f"Draft {L}/corpus/README.md additions for C1 (do not edit the file): (1) one index row in the knowledge table, exact form `| `knowledge/tb2-protein-assembly-grader.md` | <what> | S105, S106, S107 (terminal-bench-2 @ 2fd12b88) |`, placed after the benchmark-grader-semantics row; (2) one `## Coverage map` bullet in the style of the round-31/33 bullets naming knowledge/tb2-protein-assembly-grader.md and stating exactly what is and is not discharged; (3) a `*Partly discharged round 35*` sub-bullet for the §Frontier task-spec item; (4) a `### Round-35 evidence` subsection listing corpus/evidence/round35/ files and corpus/defects.jsonl. Bound every sentence to what the probe receipt and captures show. Output the draft with line anchors (which existing line each insertion follows).",
  "VERDICT: readme-draft-<n>-insertions"),
 ("R35LessonDraft", "scribe", ["calibration", "coverage"],
  f"Draft {B}/R35LessonDraft/round-35.md (the lane lesson corpus/lessons/round-35.md). Sections: header (baseline 58a19f37, freeze 11d64530); `## Gate` table (C1 entry admit-candidate; S105–S107 rows; ≥1 reject from the assimilation set — read {R34}/build/R34ReconPackage.md and /home/vgpnk/Projects/shokuknow/merge/kengaku/MERGE-REPORT.md; S091/S105 quarantine dispositions); `## Mistakes` as a markdown TABLE `| class | evidence pointer | captured-by | fix |` with rows for: (1) S091 false refusal (round-34 refused on the first 418-byte Access Denied fetch while its own reopen capture nec-s091-reopen.html holds the quote — spot-check D5); (2) committed recursive scratch mirrors (D2, 1650.6 MiB logical); (3) round-34 capture report claiming hashes in SHA256SUMS that were absent (D3) — each with captured-by and a fix shown able to fail (the ledger check red at freeze, claims/control-c2-nothing.txt); `## Assimilation record`; `## Census` placeholders the L1 fills with real outputs. Leave numbers you cannot verify as `<L1>`.",
  "VERDICT: lesson-drafted"),
 ("R35RepairTexts", "scribe", ["calibration"],
  f"Draft the exact repair texts for C2 (read {L}/plans/defect_ledger.py r34_d3/r34_d4/r34_d5 for the patterns they must satisfy): (D4) one SCORECARD line starting `- **D4 correction (round 34 C2):**` stating the counter draft's selftest was green (`R34C2CounterDraft.md:8`, `cases=10 failed=0`) and the red selftest was the mutation harness (`R34MutC2Harness.md:12`, `SELFTEST green failed (1)`) — verify both lines with sed -n; (D5) one line for {L}/corpus/lessons/round-34.md starting `Erratum (round 35):` saying the staged S091 quote is present in `nec-s091-reopen.html` (verify yourself: strip tags + whitespace, search the quote from {L}/corpus/lessons/round-34-verifier-spotcheck.md:64) and that the 'opened NEC response was unavailable' line refers only to the first 418-byte fetch; (D3) the two sha256 lines for test_outputs.py and test.sh. Write all to {B}/R35RepairTexts/.",
  "VERDICT: repair-texts-3"),
 ("R35ConsiderMine", "scribe", ["calibration"],
  f"Mine {L}/considerthese/2026-10-25.md proposal 2 against what round 35 actually implements ({L}/plans/defect_ledger.py + {L}/corpus/defects.jsonl): which of (a) re-run every closed defect's check at tip forever, (b) block pre-registration when a class recurs twice, (c) tip-receipt validator are implemented, which are not, and why. Open the r30/r31/r32/r33 defect counters ({L}/plans/round3[0-3]_defects.py) and list which of their defect classes recur in round 34's D1–D5 (e.g. D1 vs round-32 N2 untracked wave paths). Draft a QUALITY.md criterion (`## Round35 criterion — routed defects live in one ledger`) with its lesson pointer, in the style of {L}/corpus/QUALITY.md lines 255+. Also check the other two proposals of that file for anything round 35 should note as not-implemented.",
  "VERDICT: considerthese-mined-<implemented>/3"),
 # ---- simplifier (1) ----
 ("R35SimplifyTools", "simplifier", ["operability"],
  f"Review {L}/plans/round35_c1_verify.py, {L}/plans/tb2_grader_probe.py and {L}/plans/defect_ledger.py for dead code, duplicated logic and needless complexity WITHOUT changing frozen behaviour (predicates and output lines are frozen). Propose diffs only (write them to {B}/R35SimplifyTools/*.diff); for each, state why output is byte-identical (run old vs new on the lane read-only and cmp outputs). Flag any behaviour you believe is a bug instead of simplifying it.",
  "VERDICT: simplify-<n>-diffs-<n>-bugs"),
 # ---- scouts (4) ----
 ("R35ScoutMergePkg", "scout", ["coverage", "adjacency"],
  f"Screen /home/vgpnk/Projects/shokuknow/merge/kengaku/ (read-only: MERGE-REPORT.md, knowledge/, SOURCES.append.md) for ONE theme matching C1 (benchmark graders / Terminal-Bench / verifier semantics) and the lane's PROVINCE ({L}/PROVINCE.md). For each candidate entry: does it duplicate ground already held ({L}/corpus/README.md index), cite rows that would collide, or need sources the lane has not opened? Give admit-candidate / refuse verdicts with reason + flip condition. Compare with round 34's screen {R34}/build/R34ReconPackage.md.",
  "VERDICT: package-<n_admit_candidates>-admit-<n_refuse>-refuse"),
 ("R35ScoutPriorArt", "scout", ["novelty", "coverage"],
  "Prior-art check for the C1 instrument: executing a benchmark task's own grader on synthetic, requirement-targeted outputs (mutants) to map which instruction requirements the grader enforces. Search for: Agentic Benchmark Checklist (ABC, outcome validity), Terminal-Bench oracle/null-agent checks, SWE-bench test-validity audits, mutation testing of test suites applied to benchmark graders, 'grader hacking' / reward-hacking audits of agent benchmarks. Fetch each hit (URL + ≤25-word quote + location). Verdict: is the instrument pattern novel, incremental, or established? Do not claim novelty without evidence.",
  "VERDICT: priorart-<n>-hits-novelty-<established|incremental|novel>"),
 ("R35ScoutTB2Oracle", "scout", ["coverage", "depth"],
  f"At pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 of harbor-framework/terminal-bench-2, open protein-assembly's solution (e.g. {PIN}/solution/solve.sh — list the task tree via the GitHub API https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1). Does the oracle's gBlock use GS linkers, FLAG first, SNAP last, codon choices meeting GC windows? Does anything in the task tree read pdb_ids.txt/antibody.fasta at grading time? Report URLs, sizes, ≤25-word located quotes. Do not run the oracle (it calls external APIs).",
  "VERDICT: oracle-<found|absent>-consistent-<yes|no|n/a>"),
 ("R35ScoutQuarantine", "scout", ["calibration", "freshness"],
  f"Observation for C2 D5: strip tags from {R34}/assimilation/captures/nec-s091-reopen.html (python html.unescape + re.sub('<[^>]+>','') + remove whitespace) and test whether the staged quote in {L}/corpus/lessons/round-34-verifier-spotcheck.md:64 is present; record its approximate line in the raw HTML. Then re-fetch https://jpn.nec.com/techrep/journal/g23/n02/230212.html live (curl -sSL with a browser UA) into {B}/R35ScoutQuarantine/ and repeat. Also verify {R34}/assimilation/captures/quarantine-SHA256SUMS with sha256sum -c.",
  "VERDICT: s091-quote-capture-<present|absent>-live-<present|absent|unreachable>"),
 # ---- connectors (2) ----
 ("R35ConnSibling", "connector", ["adjacency"],
  "Sibling-overlap scan for round 35 surfaces: which other fleet lanes (/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md, corpus/README.md) claim benchmark grader code, Terminal-Bench, routed-defect ledgers or receipt validators (e.g. tameshi, kotoba, kumitate, chousa)? Read-only. For each hit: contested / adjacent / none, with file:line evidence. Note any sibling instrument kengaku should cite rather than duplicate.",
  "VERDICT: sibling-<contested>-contested-<adjacent>-adjacent"),
 ("R35ConnDefectClasses", "connector", ["calibration", "adjacency"],
  f"Cross-round pattern: map every routed defect in {L}/corpus/lessons/round-{{29,30,31,32,33,34}}-verifier-spotcheck.md (read-only) to a class (untracked work, receipt/manifest mismatch, scorecard misstatement, false refusal, scratch bloat, phantom hash, report-before-commit, ...). Count recurrences per class and say which round-34 D1–D5 are recurrences (populate a proposed `recurrence_of` value per row of {L}/corpus/defects.jsonl). Flag classes that recur ≥2 times with no standing check.",
  "VERDICT: classes-<n>-recurring-<n>"),
 # ---- reviewers (3) ----
 ("R35RevClaims", "reviewer", ["calibration"],
  f"Review the frozen claims {L}/plans/round-35-claims.md against both counters ({L}/plans/round35_c1_verify.py, {L}/plans/defect_ledger.py) and controls ({W}/claims/). Is each predicate the same sentence in plan, code and receipt label? Can any check pass on a state that does not deliver the claimed surface (false green)? Is any check unpassable on a truthful landing (false red: e.g. V4 42/42, V6 lane-vs-clone, D1 working tree)? Are C1/C2 causally separable as stated? Cite file:line.",
  "VERDICT: claims-review-<n>-false-green-<n>-false-red"),
 ("R35RevProbePred", "reviewer", ["coverage", "calibration"],
  f"Review the 18 frozen probe cases in {L}/plans/tb2_grader_probe.py build_cases against {CAP}/instruction.md and {CAP}/test_outputs.py: is each requirement label faithful to the instruction bullet; does each mutant isolate one requirement (check the receipt's assertion= column in {L}/corpus/evidence/round35/tb2-grader-probe.txt — e.g. donor-repeated fails on the length cap, not a repeat rule); is any 'pass' case (uppercase, G-only linker, 20-aa linker) an instruction violation the grader accepts? Recompute max_passing_nt=2766 from the component lengths. Which instruction bullets have NO case?",
  "VERDICT: probe-review-<n>-confounded-<n>-uncovered"),
 ("R35RevLedger", "reviewer", ["calibration"],
  f"Review {L}/plans/defect_ledger.py + {L}/corpus/defects.jsonl against the routed defects {L}/corpus/lessons/round-34-verifier-spotcheck.md:75-79. Does each check measure what the spot-check routed (D1: 1423 untracked incl. plans/round34_*.py; D2: mut-entries-scratch 106,323 blobs — the ledger also covers build/R34MutRegistry/{{mirror,mut}}; D3: evaluator files absent from SHA256SUMS; D4: SCORECARD misattribution; D5: S091 refusal reason false)? Is the mismatch logic (closed+fail, open+pass) a calibration count per addendum §9 ('count mismatches between the lane's self-assessment and observed repo state')? Is the row schema sufficient for considerthese proposal 2?",
  "VERDICT: ledger-review-<n>-findings"),
 # ---- critics (3) ----
 ("R35CritScope", "critic", ["adjacency", "coverage"],
  f"Attack C1's scope against {L}/PROVINCE.md (round-28/29/29a2 paragraphs: 'static LLM-evaluation interpretation', 'does not run a benchmark, certify a task, or own ... runtime task validity'). Does executing the pinned grader on synthetic gBlocks cross that line, or is it the same class as round 29's offline generator projection? What wording must the entry/PROVINCE use so it does not claim task validity, biological correctness or model performance? Also: is 'coverage' the right axis name for this surface (addendum §9: name the axis by the surface changed)?",
  "VERDICT: scope-<inside|crosses>-<n>-wording-fixes"),
 ("R35CritC2", "critic", ["calibration"],
  f"Attack C2 as a calibration claim. Can the D4/D5 checks be passed by text that is labelled correctly but says something false (token co-occurrence, the round-34 mutant class)? Is D1 (working-tree) re-derivable by a closure over committed bytes? Does closing D2 by deleting mirrors from the tip (history keeps them) honestly answer 'mutants must run in a temp clone outside the repo'? Would a do-nothing control or a flip-only control ({W}/claims/control-c2-flip.txt) reach the target? Propose concrete fixes the L1 can still make WITHOUT changing the frozen predicate.",
  "VERDICT: c2-critic-<n>-findings"),
 ("R35CritControls", "critic", ["calibration"],
  f"Attack the C1 controls ({W}/claims/control-c1-skip.sh, control-c1-skip.txt, control-c1-nothing.txt). Find the cheapest package that passes `plans/round35_c1_verify.py` WITHOUT the claimed work (e.g. an entry whose located quotes are trivial one-word strings, a receipt produced by a modified probe, rows whose teaches cell is junk, quotes all from one line). Build it in a fixture clone and score it. If any junk package scores checks=6 defects=0, that is a decisive finding: report it with the exact bytes.",
  "VERDICT: cheapest-junk-<defects>-defects"),
 # ---- mutation-testers (3) ----
 ("R35MutC1V4V5", "mutation-tester", ["calibration"],
  f"Mutation-test C1 checks V4 and V5 in a fixture clone where a passing package exists (build one: copy the lane's uncommitted round-35 evidence, add an index row + coverage bullet + entry carrying the receipt summary line; you may reuse {B}/R35EntryDraft/ if present, else a minimal entry). Mutants: index row without S106; coverage bullet removed; a 43rd knowledge file; index row duplicated; one byte changed in the receipt; receipt line reordered; summary line removed from the entry; probe file altered to print mismatches=0 always. Report kill/survive per mutant.",
  "VERDICT: v4v5-killed-<n>/<total>"),
 ("R35MutC1V1V6", "mutation-tester", ["calibration"],
  f"Mutation-test C1 checks V1 and V6 in a fixture clone: SHA256SUMS missing instruction.md; digest of test.sh altered; extra listed file absent on disk; test_outputs.py replaced with the round-34 copy (same bytes → must stay green) vs a one-byte edit (must go red); a malformed SOURCES row (10 cells) for V6 via the clone's --file path. Also confirm V6 in the live lane uses `--root ... kengaku` and in a clone uses `--file` (read the code, run both). Report kill/survive.",
  "VERDICT: v1v6-killed-<n>/<total>"),
 ("R35MutLedgerRobust", "mutation-tester", ["calibration"],
  f"Mutation-test {L}/plans/defect_ledger.py robustness in a fixture clone: unknown check name; malformed JSON line; missing corpus/defects.jsonl; duplicate row ids; status typo ('Closed'); a sixth row added; empty file. For each: does the checker crash, pass, or fail closed? A pass or an unhandled crash that exits 0 is a finding. Paste outputs and exit codes.",
  "VERDICT: ledger-robust-<n_fail_closed>/<total>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = f"{GS}# Target\nkengaku round 35 wave 1 item {name} ({role}).\n# Task\n{task}\n# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n"
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r35 wave 1 (build + first falsifiers)"})
    assert len({i["name"] for i in items}) == len(items) == 32, len(items)
    spec = {"wave": "kengaku-r35-build", "milestone": "kengaku round 35 wave 1: C1 TB2 grader admission + probe, C2 defect ledger, frontier step",
            "reportDir": ".ufo/waves/round-35/build", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/build-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    from collections import Counter
    print(Counter(i["role"] for i in items))


main()
