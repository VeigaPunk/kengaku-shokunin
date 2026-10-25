#!/usr/bin/env python3
"""Renders .ufo/waves/round-35/falsify-spec.json (wave 2 of 2, policy v1, 32 seats).
Usage: make_falsify_spec.py <landed-tip-hash>"""
import json
import pathlib
import sys
from collections import Counter

TIP = sys.argv[1]
L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
W = f"{L}/.ufo/waves/round-35"
F = f"{W}/falsify"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
CAP = f"{L}/corpus/evidence/round35/tb2-eval"
PIN = "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly"
E = f"{L}/corpus/knowledge/tb2-protein-assembly-grader.md"
C1 = "python3 plans/round35_c1_verify.py --lane ."
C2 = "python3 plans/defect_ledger.py --lane ."
CLONE = (f'Fixture rule: D=$(mktemp -d /tmp/k35f-XXXX); git clone -q --no-checkout --shared {L} "$D/lane"; '
         f'git -C "$D/lane" sparse-checkout set --no-cone <patterns>; git -C "$D/lane" checkout -q {TIP}; verify '
         f'`git -C "$D/lane" rev-parse --show-toplevel` equals "$D/lane" before any write; every git call names -C "$D/lane"; '
         f'fixture commits only inside the clone with identity `fixture <fixture@invalid>`. rm -rf "$D" at the end.')

CONTEXT = f"""# Goal
kengaku round 35 (hyaku run 7, 2026-10-25), WAVE 2 of 2 — FALSIFY. Lane repo: {L}. The round's integration has LANDED at
lane tip {TIP} (branch master). Frozen claims: {L}/plans/round-35-claims.md (freeze 11d64530). Wave-1 reports: {W}/build/.
- C1 coverage: {E} + rows S105/S106/S107 in {L}/corpus/SOURCES.md + probe {L}/plans/tb2_grader_probe.py + receipt
  {L}/corpus/evidence/round35/tb2-grader-probe.txt. Frozen counter `{C1}` must print `checks=6 defects=0`, `PREDICATE C1 pass`.
- C2 calibration: {L}/corpus/defects.jsonl + {L}/plans/defect_ledger.py; `{C2}` must print
  `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`.
Your job is to FALSIFY what landed: every item names what it attacks. A finding needs a reproducible command + output.
Agreement is a valid result only with the evidence that would have shown disagreement.

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Scratch goes under {F}/<YourSeatName>/ or a mktemp dir under /tmp.
- Write ONLY inside {F}/ or /tmp. NEVER edit any other lane file (corpus/, plans/, SCORECARD.md, LOG.md, README.md, SKILL.md,
  PROVINCE.md, SHONEN.md). Never write into /home/vgpnk/Projects/shokunin (fleet root), sibling lanes, the lane's jj state or Git
  index; never run git add/commit/stash/checkout/reset/push or mutating jj in the lane. Counters run read-only in the lane are fine.
- {CLONE}
- /home/vgpnk/Projects/shokuknow is READ-ONLY; run no campaign tools there.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read
  /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason).
  pacman transactions are PAUSED host-wide: install via uv tool / npx / an official binary into ~/.local/bin, or file an
  L0 question. Never run pacman -Sy/-Syu/-U/-R or name an already-installed package.
- Leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none,
  never stall in clarifying-question loops.
- Evidence: every number carries its command and output; quotes carry locations. Never fabricate; say what could not run.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""

ITEMS = [
 # ---- executors (13) ----
 ("F35RunC1", "executor", ["coverage", "calibration"], f"Re-run `cd {L} && {C1}` twice and in a fixture clone at {TIP} (copy nothing; the clone must pass on committed bytes alone — V6 uses --file there). Paste outputs/exit codes. Any difference between lane and clone is a finding (e.g. a check that depends on uncommitted files).", "VERDICT: c1-lane-<pass|fail>-clone-<pass|fail>"),
 ("F35RunC2", "executor", ["calibration"], f"Re-run `cd {L} && {C2}` and `git -C {L} status --porcelain --untracked-files=all | wc -l`. Then in a fixture clone at {TIP} (full checkout of corpus/ plans/ SCORECARD.md .ufo/waves/round-34/) run the checker: which rows pass on committed bytes alone? D1 is a working-tree check; say whether a closure re-deriving from a fresh clone would see the same result.", "VERDICT: c2-lane-<pass|fail>-clone-<n>/5"),
 ("F35PytestRunner", "executor", ["coverage", "operability"], f"Run the grader the way {CAP}/test.sh does (uvx -p 3.13 -w pytest==8.4.1 -w biopython==1.85 -w pytest-json-ctrf==0.3.5 pytest ... -rA) for three probe cases (valid-balanced, linker-g-only, linker-4aa): the test reads /app/gblock.txt, so use a user/mount namespace (bwrap --bind <tmp> /app, or `unshare -rm` + mount --bind) — never write /app on the host and never use sudo. Generate case contents by importing build_cases from {L}/plans/tb2_grader_probe.py. Compare pytest exit → reward 1/0 with the receipt's observed column. If no namespace tool works without root, say so and stop.", "VERDICT: pytest-agree-<n>/3-or-blocked"),
 ("F35IndepWindows", "executor", ["coverage"], f"Attack the probe's construction: for every case content in build_cases (import from {L}/plans/tb2_grader_probe.py), independently compute (a) translation with your own codon table, (b) min/max GC over all 50-nt windows, (c) whether exactly ONE requirement is violated as the case label claims. A case whose failure is confounded by a second violation is a finding (report which).", "VERDICT: cases-isolated-<n>/18"),
 ("F35MaxNt", "executor", ["coverage"], f"Falsify the entry's finding 2 ({E}: max passing gBlock = 3 × (842 + 80) = 2766 nt < 3000). Recompute component lengths from {CAP}/test_outputs.py literals; consider whether anything else could lengthen a passing gBlock (codons are 3 nt; linkers capped at 20; flag at 0, snap at end; could extra content hide anywhere?). Try to construct a passing gBlock > 2766 nt and run it through the probe's run_grader.", "VERDICT: maxnt-<confirmed|refuted>"),
 ("F35GOnlyLinker", "executor", ["coverage"], f"Falsify the entry's finding 1 (a G-only linker passes) and finding 3 (a one-residue subprotein error fails with the order message): re-run those cases with fresh content (different codon choices, different substituted position, substitution in acceptor/snap instead of donor) through the probe's run_grader (uv run --with biopython==1.85). Paste observed outcomes and assertion messages.", "VERDICT: findings13-<confirmed|refuted>"),
 ("F35MutLedgerD1", "executor", ["calibration"], f"Mutation-test ledger check r34_d1 in a fixture clone at {TIP} (sparse: /corpus/ /plans/ /SCORECARD.md /.ufo/waves/round-34/): run the checker (D1 green in a clean clone), then create an untracked file .ufo/waves/round-34/F35probe.tmp in the CLONE → D1 must go agree=NO, exit 1; an untracked plans/round34_defects.py → red; an ignored __pycache__/x.pyc → document. Never touch the lane working tree. Paste outputs.", "VERDICT: d1-killed-<n>/<total>"),
 ("F35MutLedgerD2", "executor", ["calibration"], f"Mutation-test r34_d2 in a fixture clone at {TIP}: restore one mirror file from the parent of the D2 deletion commit (find it: git -C \"$D/lane\" log --diff-filter=D --format=%H -1 -- .ufo/waves/round-34/mut-entries-scratch) and fixture-commit it in the clone; D2 must go red. Also check: is any OTHER committed recursive mirror left under .ufo/waves/round-34 (paths containing /corpus/SOURCES.md or /.ufo/waves/ below a seat dir)?", "VERDICT: d2-killed-<yes|no>-residual-<n>"),
 ("F35MutLedgerD3", "executor", ["calibration"], f"Mutation-test r34_d3 in a fixture clone at {TIP}: flip one hex digit of the test.sh line in .ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS → red; delete the test_outputs.py line → red; append a line for a missing file → red. Also `sha256sum -c` the landed manifest in the lane read-only.", "VERDICT: d3-killed-<n>/3"),
 ("F35MutLedgerD4D5", "executor", ["calibration"], f"Mutation-test r34_d4 and r34_d5 in a fixture clone at {TIP}: D4 — remove `cases=10 failed=0` from the SCORECARD correction line; duplicate the line; change R34C2CounterDraft.md line 8. D5 — remove `present` from the erratum; move the S091 Mistakes row out of the table in corpus/lessons/round-35.md; corrupt the quote in nec-s091-reopen.html. Every mutant must go red; also try one FALSE but well-labelled D4 line (says the harness was green) — does it pass?", "VERDICT: d4d5-killed-<n>/<total>"),
 ("F35Census", "executor", ["coverage", "calibration"], f"Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (paste output + exit). Count rows before/after: `git -C {L} show 58a19f37312e1b22fd2a7957bdfc6bb7832aadd0:corpus/SOURCES.md | grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|'` vs {TIP}; tier/status histograms; every mined row's used-by paths exist; NF==13 for every row.", "VERDICT: census-<exit>-rows-<before>-<after>"),
 ("F35SeparabilityC1", "executor", ["calibration"], f"Causal separability: in a fixture clone at {TIP}, revert ONLY C2's surfaces to the freeze commit 11d64530 (corpus/defects.jsonl statuses, SCORECARD D4 line, round-34 lesson erratum, round-34 SHA256SUMS) and fixture-commit; run the C1 counter → must stay checks=6 defects=0. List exactly which files you reverted.", "VERDICT: c1-separable-<yes|no>"),
 ("F35SeparabilityC2", "executor", ["calibration"], f"Causal separability: in a fixture clone at {TIP}, remove ONLY C1's surfaces (entry file, S105–S107 rows, README rows, corpus/evidence/round35/) and fixture-commit; run the C2 ledger → must stay rows=5 closed=5 observed_pass=5 mismatches=0 (D1 in a clone is trivially green — say so). Report any cross-dependency.", "VERDICT: c2-separable-<yes|no>"),
 # ---- scribes (2) ----
 ("F35ReportEvidence", "scribe", ["calibration"], f"Draft the evidence table for the round report: for each claim, the before receipt ({W}/claims/control-*-nothing.txt), the after command output at {TIP} (run both counters read-only), the commit hashes from `git -C {L} log --format='%H %s' 58a19f37..{TIP}`, the census before/after, and the wave-1 seat ledger from {W}/build-results.json (seat count, role histogram, dead seats with last error text). Write {F}/F35ReportEvidence/table.md. Every number with its command.", "VERDICT: evidence-table-<n>-rows"),
 ("F35LogDraft", "scribe", ["calibration"], f"Check the LOG.md round-35 entry ({L}/LOG.md tail) and SCORECARD round-35 section against the landed state at {TIP}: every number, hash and path must re-derive. Draft an appended errata block for anything wrong (never rewrite). Write {F}/F35LogDraft/errata.md.", "VERDICT: log-errata-<n>"),
 # ---- simplifier (1) ----
 ("F35SimplifyLanded", "simplifier", ["operability"], f"Review the landed instruments {L}/plans/tb2_grader_probe.py, {L}/plans/round35_c1_verify.py, {L}/plans/defect_ledger.py for dead code or needless complexity; propose diffs under {F}/F35SimplifyLanded/ with old-vs-new output cmp proof. Flag bugs separately.", "VERDICT: simplify-<n>-diffs-<n>-bugs"),
 # ---- scouts (3) ----
 ("F35ReopenS105", "scout", ["coverage", "freshness"], f"Re-open S105 at {PIN}/tests/test_outputs.py yourself; sha256 vs {CAP}/SHA256SUMS; locate the row's anchor quote (line 42) and every quote of {E} §Located quotes citing test_outputs.py at its line. Check the S105 row cells (scope, anchor, teaches) say nothing the file does not.", "VERDICT: s105-<ok|defect>-quotes-<n_ok>/<n>"),
 ("F35ReopenS106S107", "scout", ["coverage", "freshness"], f"Re-open S106 ({PIN}/tests/test.sh) and S107 ({PIN}/instruction.md); sha256 vs manifest; locate the rows' anchor quotes (test.sh:27, :21; instruction.md:29) and the entry's quotes citing them. Check S107's teaches cell ('fifteen requirement bullets') against the file.", "VERDICT: s106s107-<ok|defect>"),
 ("F35DanglingRefs", "scout", ["calibration"], f"After the D2 deletion, which committed lane files cite paths that no longer exist at {TIP} (e.g. .ufo/waves/round-34/build/R34MutRegistry/mirror/..., mut-entries-scratch/...)? `git -C {L} grep -n` for those prefixes. Is each such citation still resolvable through history (name the commit)? Is any of them load-bearing for an admitted claim?", "VERDICT: dangling-<n>-loadbearing-<n>"),
 # ---- connectors (2) ----
 ("F35ConnFrontier", "connector", ["coverage", "adjacency"], f"Frontier walk: compare {L}/corpus/README.md §Frontier and §Coverage map at 58a19f37 vs {TIP}. Which frontier clause moved, by exactly how much (one TB2 task)? Propose round-36 frontier candidates from wave-1 reports ({W}/build/R35ScoutPriorArt.md, R35ScoutTB2Oracle.md, R35ScoutMergePkg.md) with the source each needs.", "VERDICT: frontier-moved-<n>-candidates-<n>"),
 ("F35ConnSiblingCheck", "connector", ["adjacency"], f"Cross-lane check of the landed entry {E} and ledger against sibling lanes' PROVINCE/corpus (read-only, /home/vgpnk/Projects/shokunin/*-shokunin): does any sibling already hold a TB2 task-grader reading or a routed-defect ledger the lane should cite? Compare with wave-1 {W}/build/R35ConnSibling.md.", "VERDICT: sibling-<contested>-contested"),
 # ---- reviewers (5) ----
 ("F35RevEntryQ", "reviewer", ["coverage", "depth"], f"Review {E} against corpus/QUALITY.md Q1–Q7 ({L}/corpus/QUALITY.md). For every load-bearing sentence, name the quote or receipt line that supports it (Q3); flag any sentence wider than its source (e.g. claims about Harbor, the 88 other tasks, PDB literals).", "VERDICT: entry-q-<n_pass>/7-<n>-overclaims"),
 ("F35RevScorecard", "reviewer", ["calibration"], f"Calibration review: compare every round-35 statement in {L}/SCORECARD.md (round-35 section, capability rows, D4 correction) and {L}/SHONEN.md with observed state at {TIP} (run the counters/commands each cites). Count mismatches between self-assessment and observation; each is a finding.", "VERDICT: scorecard-mismatches-<n>"),
 ("F35RevLesson", "reviewer", ["calibration"], f"Review {L}/corpus/lessons/round-35.md: Gate has ≥1 admit and ≥1 reject from the assimilation set; every new SOURCES row has URL, access date and ≤25-word located quote; Mistakes rows are class · evidence pointer · captured-by · fix, and each fix is shown able to fail; census before/after pasted with exit codes. Also check the round-34 erratum and Q23 in {L}/corpus/QUALITY.md.", "VERDICT: lesson-<n>-defects"),
 ("F35RevReadme", "reviewer", ["coverage"], f"Review the README changes at {TIP} (`git -C {L} diff 58a19f37 {TIP} -- corpus/README.md`): index row, coverage bullet, frontier sub-bullet, round-35 evidence list. Every path must exist; every sentence must match {E} and the receipt; nothing claims more than one task.", "VERDICT: readme-<n>-defects"),
 ("F35RevDiffScope", "reviewer", ["calibration", "adjacency"], f"Review the full round diff `git -C {L} diff --stat 58a19f37 {TIP}` and `git -C {L} log 58a19f37..{TIP}`: every changed path is inside the round's declared surfaces (claims file Separability section); no frozen counter/probe changed after freeze 11d64530 (git diff 11d64530 {TIP} -- plans/round35_c1_verify.py plans/tb2_grader_probe.py plans/defect_ledger.py); deletions are only the round-34 mirror roots. Any post-freeze change to a frozen rule is a decisive finding.", "VERDICT: scope-<ok|violations-n>"),
 # ---- critics (3) ----
 ("F35CritC1", "critic", ["coverage", "calibration"], f"Attack C1 as declared: is 'coverage' the honest axis (frontier → core for one task's scoring code + a new instrument) or is this re-reading round 34's captures (quality work)? Could a do-nothing control reach it ({W}/claims/control-c1-*.txt)? Does V5's byte-equality make the receipt evidence or just self-consistency? Is the 18-case table enough to support 'instruction requirement → enforcing assertion'?", "VERDICT: c1-critic-<holds|falls>-<n>-findings"),
 ("F35CritC2", "critic", ["calibration"], f"Attack C2 as declared: does closing D1–D5 constitute a calibration move per addendum §9 (count mismatches between self-assessment and observed state)? Are D4/D5 checks still token co-occurrence (see wave-1 {W}/build/R35CritC2.md)? Is deleting 109,413 committed mirror paths from the tip an honest D2 close when history keeps them? Is there any axis harmed (e.g. operability lost by deleting round-34 evidence)?", "VERDICT: c2-critic-<holds|falls>-<n>-findings"),
 ("F35CritHarm", "critic", ["calibration", "adjacency"], f"No-harm audit across all six axes (depth, coverage, operability, freshness, calibration, adjacency) and novelty: compare SCORECARD axis rows, PROVINCE, SKILL.md, QUALITY.md, existing knowledge entries and gates at 58a19f37 vs {TIP}. Does any landed change make an existing claim false, break an existing gate (`python3 {L}/grader.py`, `python3 {L}/plans/state_check.py --summary`, `python3 {L}/plans/round33_defects.py --lane .` — run read-only), or remove evidence a prior admitted claim cites?", "VERDICT: harm-<none|n>"),
 # ---- mutation-testers (3) ----
 ("F35MutEntryQuotes", "mutation-tester", ["calibration"], f"In a fixture clone at {TIP}, mutate the LANDED entry {E.replace(L + '/', '')}: change one character inside each of 3 different quotes; shift one location by one line; drop the Negative space falsifier; remove the receipt summary line. Run the C1 counter after each (restore between). Report kill/survive.", "VERDICT: entry-mutants-killed-<n>/<total>"),
 ("F35MutReceipt", "mutation-tester", ["calibration"], f"In a fixture clone at {TIP}: flip one `observed=` value in corpus/evidence/round35/tb2-grader-probe.txt; change the probe to skip a case; change one prediction in plans/tb2_grader_probe.py so it mismatches (receipt regenerated from the changed probe); replace the capture test_outputs.py with a one-line-different copy. Run the C1 counter each time. Which mutants survive?", "VERDICT: receipt-mutants-killed-<n>/<total>"),
 ("F35MutRowsIndex", "mutation-tester", ["calibration"], f"In a fixture clone at {TIP}: S106 row used-by gains a second path; S107 opened date changed; S105 URL gets `?raw=1`; README index row loses S107; coverage bullet renamed; a stub 43rd knowledge file added and indexed. Run the C1 counter and the census (`--file` mode) each time. Kill/survive per mutant.", "VERDICT: rows-index-killed-<n>/<total>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = f"{GS}# Target\nkengaku round 35 wave 2 (falsify) item {name} ({role}).\n# Task\n{task}\n# Acceptance\nReport at your `Report:` path (absolute: {F}/{name}.md); end with {verdict}.\n"
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r35 wave 2 (falsify the landed round)"})
    assert len({i["name"] for i in items}) == len(items) == 32, len(items)
    spec = {"wave": "kengaku-r35-falsify", "milestone": "kengaku round 35 wave 2: falsify landed C1/C2, sources, lesson, scope, harm",
            "reportDir": ".ufo/waves/round-35/falsify", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/falsify-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    print(Counter(i["role"] for i in items))


main()
