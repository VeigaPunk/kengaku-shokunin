#!/usr/bin/env python3
"""Render the round-85 v1 wave spec (12 seats) — wave evidence, not a production gate."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
W = f"{L}/.ufo/waves/round-85/w1"
SCR = "/fast/scratch/hyaku/kengaku-r85"

CONTEXT = """# Goal and frozen contract
Kengaku round 85, ONE v1 wave, 12 seats. L1 KengakuR85 owns integration and the planner seat; you are a leaf seat: never spawn subagents, never call task.
Read {L}/plans/round-85-claims.md IN FULL first (frozen at commit 1a45aeb5e8706b1518ba58fd0fe882df1631e2a0; base 0de45354d7aff18e4a23a348ec13de3a1f707a44). Never change its predicate, target, case table, control set, kill rule or defect list. If a frozen element looks wrong, say so in your output; do not edit it.
Claims: R85-C1 coverage — first located offline replay of the base-unexecuted `sqlite-db-truncate` grader (eight frozen cases, two legs: set-intersection score and the `score > 6` verdict). R85-C2 calibration — the eight owner-routed round-84 defects (V1, V2, V3, V5, V6, V7, V8, V9; V4 is operator-owned) discharged with a base-sensitive gate.
Landed so far: freeze 1a45aeb5 (claims + plans/round85-cases.json + plans/round85-defects.json); instruments and repairs 99a7cb3b (plans/round85_sqlite_truncate_probe.py, plans/round85_c1_replay.py, plans/round85_c2_debt.py, QUALITY Q61, entry writer rename, round83 flag spelling); C1 receipt and executed ledger row ce5b9ef8.

# Hard bounds
- Write scope: ONLY your own directory {W}/<YourSeatName>/ inside the lane repo, plus scratch under {SCR}/<YourSeatName>/. Production files ({L}/plans, {L}/corpus, {L}/SKILL.md, {L}/SCORECARD.md, {L}/LOG.md) are READ-ONLY to you. Never edit, add or delete a production file.
- Never commit, push, stage, stash, checkout, reset or run any mutating git/jj command, in any repo. Read-only git (log, show, cat-file, status, diff, ls-files, rev-parse) is fine. Never touch the fleet repo /home/vgpnk/Projects/shokunin, sibling lanes, .ufo/state, .ufo/watchdog.log or .scratch.
- Any fixture repo you create is `D=$(mktemp -d -p {SCR}/<YourSeatName>) && git -C "$D" init -q` and every later git/jj call names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before any commit. Never run git commit/jj with a throwaway identity anywhere else.
- Scratch: everything under {SCR}/<YourSeatName>/ with `mkdir -p`; delete it before you yield (receipts first copied into your wave dir). /tmp is for files under 50 MB only.
- No network beyond the single pinned raw.githubusercontent.com fetch your item names; no credentials, cookies, tokens or auth state are read or used.
- Every `Report:` trailer path a rendered prompt shows is relative to {L} — write it at {L}/<that path>.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your output). pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R/downgrade/restart a host service.
- Do not file the round report; the L1 does. Do not message other seats or agent://all.
- End your final message with exactly one line: `SEAT <YourSeatName> VERDICT <PASS|FINDINGS|BLOCKED> findings=<n>` where findings is the count of defects you actually found (0 for PASS)."""


def item(name, role, task):
    return {"name": name, "role": role, "prompt": "/skill:godspeed\n\n" + task}


def build():
    items = [
        item("ScoutR85", "scout", f"""# Item ScoutR85 — member-selection recon against grader bytes (read-only)
Read {L}/plans/grader-population-ledger.json and {L}/plans/round-85-claims.md section R85-C1.
# Target
Write {W}/ScoutR85/scout-map.md with:
1. The ledger's `no-blocker` evidence shape: for 10 unexecuted members, open {L}/corpus/evidence/round52/graders/<member>/tests/test_outputs.py and record (a) third-party imports, (b) any binary the grader invokes by name through subprocess (Rscript, R, node, java, docker...), (c) whether the ledger note says `no-blocker`. Name every member whose `no-blocker` note is falsified by a binary requirement, with the exact source line.
2. The chosen member `sqlite-db-truncate`: confirm from its bytes only (do not read plans/round85-cases.json) that it imports only the standard library and reads /app/recover.json, quote its acceptance predicate with line numbers, and state the predicate literally.
3. Class histogram of the 59 unexecuted members by `classes`, and how many of the 9 `serialization-schema` members are executed after this round.
Every claim gets path:line. Do not edit production files."""),
        item("ExecBaseR85", "executor", f"""# Item ExecBaseR85 — independently reproduce both counter runs at BASE and tip
Read-only on {L}. Run, from {L}:
1. `python3 plans/round85_c1_replay.py --lane . --rev 0de45354d7aff18e4a23a348ec13de3a1f707a44 --work <scratch>` (expect exit 1 and `PREDICATE R85-C1 fail`).
2. `python3 plans/round85_c1_replay.py --lane . --rev master --work <scratch>` (expect exit 0 and `PREDICATE R85-C1 pass`).
3. `python3 plans/round85_c2_debt.py --lane . --rev master --work <scratch>` and `--sensitivity` (record exactly what it prints NOW, including any remaining defects).
4. `python3 plans/round85_c2_debt.py --lane . --check-only v5`, `--check-only v6`, `--check-only v8`.
Copy each command's full stdout+stderr and exit code to {W}/ExecBaseR85/replay.txt as `$ command` / output / `rc=<n>` blocks. Then verify the receipt's stamped values against the tree: SUBJECT_SHA, CASE_TABLE_SHA, TOOL_SHA, LANE_TIP, COMMAND, and confirm `git -C {L} cat-file -p <LANE_TIP>:plans/round85_sqlite_truncate_probe.py | sha256sum` equals TOOL_SHA. Note any mismatch. No edits to production."""),
        item("ExecDebtR85", "executor", f"""# Item ExecDebtR85 — out-of-band gate roster for the landing commit (QUALITY Q20)
Q20 requires a landing that touches a gate to cite a gate run made OUTSIDE the working copy, from a tree extracted from the commit.
# Target
1. Extract the current lane tip with `git -C {L} archive --format=tar <tip> | tar -x -C <scratch>/landing` (tip: `git -C {L} rev-parse master`).
2. In that extracted tree run and record exit codes and the pinned count lines: `python3 grader.py | grep -E 'CHECKS n=|VERDICT:'`; `python3 plans/sources_adopt.py --selftest | tail -1`; `python3 plans/registry_check.py --selftest | tail -1`; `python3 plans/config_projection.py --selftest | tail -1`; `python3 plans/benchmark_spec_audit.py --selftest | tail -1`; `python3 plans/gate_timing_check.py --selftest`; `python3 plans/state_check.py --selftest`.
3. Because round 85 edits `plans/round83_c2_debt.py`, run that tool's OWN row too: `python3 plans/round83_c2_debt.py --lane . --work <scratch> --selftest`.
4. Also run the new counters' own batteries from the extracted tree: `python3 plans/round85_c1_replay.py --lane . --work <scratch> --selftest` and `--mutants`, and `python3 plans/round85_c2_debt.py --lane . --work <scratch> --selftest`.
Write everything to {W}/ExecDebtR85/gate-receipt.txt as `$ command` / output tail / `rc=<n>`. If any line differs from the count the previous landing recorded (search {L}/LOG.md round-84 section), say so explicitly as a finding. Measure and transcribe; judging is not your job."""),
        item("ExecCensusR85", "executor", f"""# Item ExecCensusR85 — standing gates and the sources census before/after
# Target
1. `sh /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` from /home/vgpnk/Projects/shokunin; record the exit code and the final ok/FAIL line, plus `grep -c '^| S[0-9]' {L}/corpus/SOURCES.md` and the W04 count.
2. Index parity: find the R75 index parity tool with `grep -rl 'UNIVERSE knowledge' {L}/plans` and run it from {L}; record the UNIVERSE/PREDICATE lines and rc.
3. Population gate: find the R79 ledger gate with `grep -rl 'R79-C1' {L}/plans | head`, run it, record TARGET/DEFECTS/PREDICATE lines and rc.
4. `python3 plans/state_check.py --summary` from {L}: record rc and every MISMATCH line.
5. `python3 plans/defect_ledger.py --lane .` from {L}: record rc and any `agree=NO`.
6. `python3 plans/round82_c1_plans_registry.py --lane .`: record rc and PREDICATE.
Write all commands, outputs and rc values to {W}/ExecCensusR85/census.txt. Flag any gate red NOW as a finding with its exact defect line."""),
        item("SourceR85", "scribe", f"""# Item SourceR85 — open the pinned sqlite-db-truncate grader and draft the S272 row
# Target
1. Fetch with curl (write only under your scratch): https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-db-truncate/tests/test_outputs.py ; record HTTP status, byte count and sha256, and compare with {L}/corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py.
2. Read {L}/corpus/SOURCES.md header (lines 1-20) and rows S267-S271 (`grep -n '^| S26' ...` and `'^| S27'`) to copy the 11-column schema exactly, then write {W}/SourceR85/s272-row.md with ONE proposed row: id S272, kind code, tier A, scope "member replay only: this pinned grader's acceptance predicate", the exact anchor, a located quote of at most 25 words with its line number, status mined, opened 2026-11-04, a recheck value (ISO date or cadence), used-by naming the round-85 lesson, and no literal or escaped `|` inside any cell.
3. State the word count of your quote and how you counted it (`len(quote.split())`).
4. Also draft the Gate block the lesson needs for this row: URL, access date 2026-11-04, located quote, admit reason, and the flip condition. Write it to {W}/SourceR85/gate-block.md.
Do not edit corpus/SOURCES.md yourself."""),
        item("ScribeR85", "scribe", f"""# Item ScribeR85 — draft the round-85 lesson and the SCORECARD/LOG append blocks
Read {L}/corpus/lessons/round-84.md (Gate/Mistakes/corrections shape), {L}/corpus/lessons/round-84-verifier-spotcheck.md section Routed defects, {L}/corpus/QUALITY.md Q60/Q61 and {L}/plans/round-85-claims.md.
# Target
1. {W}/ScribeR85/round-85.md — lesson body: header (round, date, L1, base 0de45354, freeze 1a45aeb5); `## Gate` with the S272 table (admit/reject columns, access date, 25-word-max located quote, reason/flip) and a `| candidate | decision | reason |` decision table for the Q61 criterion and the held entry `tb2-code-from-image-offline.md`; `## Corrections` naming R84-V1/V2/V3/V5/V6/V7/V8/V9 with what each repair is; `## Mistakes` table with class / evidence pointer / captured-by / fix, including (a) the round-84 freeze-input-after-freeze defect (R84-V2) and (b) any mistake you can evidence from round 84's own bytes; `## Definition horizon` — a short section naming BASE 0de45354 as an existing revision and pricing the future-file condition (no check may read a file that does not exist at its before-revision); `## Sources and frontier` with `expansion: unchanged`, an explicit dated correction of the round-84 `expansion: improved` grade (R84-V7), SOURCES rows before -> after, and `Assimilation: none` plus why.
2. {W}/ScribeR85/scorecard-block.md — a `## Round 85` SCORECARD section: two claim rows (R85-C1 coverage, R85-C2 calibration) with before -> after, counting command and measured commit placeholders left as `<L1 fills>`, the other five axes as a held/no-change line, and a `### Planned (round 86)` list of three next moves.
3. {W}/ScribeR85/log-block.md — a `## Round 85` LOG section: header naming coverage as the lowest non-retired axis (score 7, L0 cap `kengaku | round-25/33/51`) and the tie-break line, the work items, the receipts and their commits, and the re-verification lines.
Facts you do not know must be written as `<L1 fills: ...>`, never invented. Do not edit SCORECARD.md or LOG.md."""),
        item("ReviewerC185", "reviewer", f"""# Item ReviewerC185 — independent derivation and replay attack on R85-C1
Attack seat. Read-only except your own directory.
# Target
1. WITHOUT reading {L}/plans/round85-cases.json or {L}/plans/round85_sqlite_truncate_probe.py, derive from the grader source alone ({L}/corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py) the predicted score/verdict for the eight case shapes named in {L}/plans/round-85-claims.md section R85-C1: exact8, seven, six, empty, extras, duplicates, string-values, int-values. Write the derivation, with the Python semantics you relied on (set intersection, int/float equality, str vs float), to {W}/ReviewerC185/derived.txt.
2. Compare with the frozen table and with `python3 plans/round85_sqlite_truncate_probe.py --lane . --work <scratch>` output. Any disagreement is a finding.
3. Run `python3 plans/round85_c1_replay.py --lane . --rev master --work <scratch>` and, in a scratch extraction of BASE (`git -C {L} archive 0de45354d7aff18e4a23a348ec13de3a1f707a44 | tar -x`), confirm the counter's before-state. Check that the frozen predicate sentence in plans/round-85-claims.md is the same sentence as the counter's `PREDICATE R85-C1` line and the report label; quote both.
4. Check the receipt for stamp completeness and the TOOL_SHA binding, and confirm `git -C {L} cat-file -p ce5b9ef8:corpus/evidence/round85/sqlite-db-truncate-probe.txt` equals the working-tree receipt.
Write findings to {W}/ReviewerC185/report.md, each with path:line or command output."""),
        item("ReviewerC285", "reviewer", f"""# Item ReviewerC285 — independent attack on R85-C2 (eight routed defects)
Attack seat. Read-only except your own directory.
# Target
For EACH of R84-V1, V2, V3, V5, V6, V7, V8, V9 as listed in {L}/corpus/lessons/round-84-verifier-spotcheck.md section Routed defects and {L}/plans/round-85-claims.md section R85-C2, determine from committed bytes whether the claimed repair is substantive (not a presence test) and whether it is red at BASE 0de45354:
- V1: are the four round-84 wave paths tracked at master? (`git -C {L} cat-file -e master:<path>`)
- V2: do plans/round85-cases.json and plans/round85-defects.json exist at the freeze commit 1a45aeb5 and are they byte-identical at master? Is the counter's anchor fail-closed (show it with a fixture where the freeze tree lacks the table)?
- V3: is the REPRODUCE leg unconditional in plans/round85_c1_replay.py, and does `--control-forged-receipt` reject the forged receipt, with which defect id?
- V5: read corpus/QUALITY.md Q61; is it the criterion the round-84 freeze promised, and does it have an executable half?
- V6: what is the entry's writer value now, and why can it no longer collide with a seat id? Does `plans/gate_timing_check.py --selftest` still pass?
- V7: does the round-85 lesson carry the correction? It may not exist yet; if it does not, report that as open, not as closed.
- V8: is `python3 plans/round82_c1_plans_registry.py --lane .` green now, and what exactly did the repair change in plans/round83_c2_debt.py?
- V9: does the C2 before-state read an existing revision, and is the future-file condition priced?
Write {W}/ReviewerC285/report.md with one row per id: repair / substantive? / red at BASE? / evidence. Also state whether any check is satisfied by prose alone (that is a finding)."""),
        item("CriticR85", "critic", f"""# Item CriticR85 — adversarial review of both frozen claims
Read-only attack. Read {L}/plans/round-85-claims.md in full; {L}/plans/round85-cases.json; {L}/plans/round85-defects.json; {L}/plans/round85_c1_replay.py; {L}/plans/round85_c2_debt.py; {L}/plans/round85_sqlite_truncate_probe.py; {L}/corpus/QUALITY.md Q61.
# Target
Attack each claim against its frozen predicate, target, kill rule, the lane's own admission bar (QUALITY Q1-Q24, Q60, Q61) and the section 9 claim-sizing rules (do-nothing control, one-artifact-one-claim, no narrowing after landing, the same sentence in plan/counter/label).
For R85-C1 ask: is a member replay a real coverage move or a re-scored class? Can the counter go green on ledger-only data, a forged receipt, or a table committed after the freeze? Is the two-leg vector genuinely discriminating, or is the verdict leg implied by the score leg (score determines verdict, so is the second leg vacuous)? Is duplicates=8 the right prediction under set semantics? Is int-values=6 right under int/float equality?
For R85-C2 ask: is each of the eight checks base-sensitive for the reason claimed, or only incidentally? Does any check assert the outcome it is supposed to observe? Is V4 honestly excluded rather than quietly waived? Is the repair set causally separable from R85-C1?
Give every finding a severity (BLOCKER/MAJOR/MINOR/FINDING) and say what would falsify your own reading. Write {W}/CriticR85/critique.md."""),
        item("MutTesterR85", "mutation-tester", f"""# Item MutTesterR85 — independent mutation battery on both new counters
Read-only on production; build mutants under {SCR}/MutTesterR85 and write results to {W}/MutTesterR85/mutants.md.
# Target
1. Read {L}/plans/round85_c1_replay.py and {L}/plans/round85_c2_debt.py. Invent at least SIX of your own mutants (not the shipped MUTANTS tuples) that disable a check or a guard: accept a receipt whose WORKTREE is dirty; ignore RECEIPT-EXIT; accept a table whose member differs; ignore the freeze-anchor SetupDefect; make indexed always true; make --check-only v8 ignore the exit code; skip the TABLE-SUBJECT check; accept a receipt whose observation block has no PREDICATE line.
2. For each mutant, construct the fixture the mutant should let through, and demonstrate: (a) the unmutated counter REJECTS that fixture, (b) the mutant accepts it. Copy the mutated counter and fixture under your scratch only.
3. Report which mutants are necessary (the removed check is load-bearing) and which are redundant (another leg catches the same fixture); redundancy is a finding about defence in depth, not a failure.
Never edit the committed counters."""),
        item("SentinelR85", "sentinel", f"""# Item SentinelR85 — security review of the new instruments and this round's evidence
Read-only. Threat-model {L}/plans/round85_sqlite_truncate_probe.py, {L}/plans/round85_c1_replay.py, {L}/plans/round85_c2_debt.py and the minted receipt {L}/corpus/evidence/round85/sqlite-db-truncate-probe.txt.
# Target
1. Isolation: list every bwrap flag and state what the case harness can and cannot reach (host /app, network, the lane tree, environment). Verify that the host /app is unchanged by a probe run and that no file outside the work dir changes.
2. Confidentiality: does any instrument read credentials, env vars, cookies, tokens or network? Do receipts leak anything beyond the work path?
3. Integrity: can a candidate (the graded end state) write the grader's verdict, the ledger or the receipt? Is receipt confinement satisfied — can a /tmp or working-copy-only artifact be cited as evidence by these counters?
4. Demonstrate at least one refusal: the probe exiting 2 on a changed subject sha or a missing table, and the counter exiting 2 on a missing freeze input, with exact output lines.
Write {W}/SentinelR85/report.md with a must-fix list (if any) and the commands you ran."""),
        item("ConnectorR85", "connector", f"""# Item ConnectorR85 — read-only sibling-overlap scan at current HEADs
Read-only. Do not modify anything outside {W}/ConnectorR85/.
# Target
Search sibling lane corpora and plans for coverage of the same ground, at their CURRENT commits (record each sibling's `git -C <repo> rev-parse master`):
1. the member `sqlite-db-truncate` and `recover.json`; the phrase `set intersection` and threshold graders; duplicates=8.
2. the Q61 idea (an admission counter with a committed filler/junk package that must stay red) — does any sibling already hold a criterion or gate by that name or shape? Check corpus/QUALITY.md and plans in each lane.
3. the R84-V8 class (a registry gate that requires a declared flag to appear literally in the instrument's bytes) — does a sibling own that gate or a duplicate of it?
4. whether the `merge/kengaku/` package at /home/vgpnk/Projects/shokuknow (read-only) stages anything about sqlite-db-truncate, TB2 graders or threshold-count graders.
Write {W}/ConnectorR85/overlap.md with `overlap: none|<list>`, each hit as repo:path:line and a one-line ruling (duplicate / adjacent / contest). Do not judge the lane's claims."""),
    ]
    return items


def main() -> None:
    items = build()
    assert len(items) == 12, len(items)
    spec = {
        "wave": "kengaku-r85-w1",
        "milestone": ("R85 first offline replay of sqlite-db-truncate (serialization-schema class) "
                      "and the eight routed-defect discharge with a base-sensitive gate"),
        "maxLanes": 12,
        "axes": ["coverage", "calibration"],
        "context": CONTEXT.replace("{L}", L).replace("{W}", W).replace("{SCR}", SCR),
        "items": [{"name": i["name"], "role": i["role"],
                   "prompt": i["prompt"].replace("{L}", L).replace("{W}", W).replace("{SCR}", SCR)}
                  for i in items],
    }
    out = pathlib.Path(f"{L}/.ufo/waves/round-85/w1-spec.json")
    out.write_text(json.dumps(spec, indent=2) + "\n")
    print("spec", out, "items", len(items), dict(Counter(i["role"] for i in items)))


if __name__ == "__main__":
    main()
