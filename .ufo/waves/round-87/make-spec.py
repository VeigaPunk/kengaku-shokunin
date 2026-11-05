#!/usr/bin/env python3
"""Render the round-87 v1 wave spec (12 seats) — wave evidence, not a production gate."""
import json
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
W = f"{L}/.ufo/waves/round-87/w1"
SCR = "/fast/scratch/hyaku/kengaku-r87"
WAVE = f"{L}/.ufo/waves/round-87"
BASE = "b9be687774e6b559470f5b0d9b936315b51ff311"
INSTR = "21da383b44a399f40faf346eed89210c9114848d"
TIP = "10de494d14abf0b77979225f51b3b72e73c0d2ed"
FREEZE = "b0f076518dad55f62a89183c5a873957ad3cf6a5"

CONTEXT = f"""# Goal and frozen contract
Kengaku round 87, ONE v1 wave, 12 seats. L1 KengakuR87 owns integration and holds the planner seat; you are a leaf seat: never spawn subagents, never call task.
Read {L}/plans/round-87-claims.md IN FULL first. Frozen at commit {FREEZE} (claims and case table); instruments frozen at {INSTR}; measured tip {TIP}; base {BASE}. Never change a predicate, target, case table, control set, kill rule or leg list. If a frozen element looks wrong, say so in your output; do not edit it.
Claims: R87-C1 coverage — a fifth located offline replay of the captured `mteb-retrieve` grader over eight frozen cases; counter `plans/round87_c1_replay.py` (`--rev`), receipt `corpus/evidence/round87/mteb-retrieve-probe.txt`, ledger row executed; BASE `defects=3`, tip `defects=0`, `executed_rows` 30 -> 31. R87-C2 calibration — the live current-state wording of the round-86 case set in `corpus/README.md`, `PROVINCE.md`, `SKILL.md` against the table-derived split; counter `plans/round87_c2_wording.py` (`--rev`); BASE `mismatches=1 defects=2`, tip `mismatches=0 defects=0`.
Pointer checker: `plans/round87_report_paths.py` (mined mistake reference-drift). Source rows: S275 (admitted, mined) and S276 (rejected) in `corpus/SOURCES.md`; Gate and Mistakes in `corpus/lessons/round-87.md`.
Lane tip for the tip measurement is {TIP}; all instrument bytes are unchanged between {INSTR} and {TIP} (verify with git diff).

# Hard bounds
- Write scope: ONLY your own directory {W}/<YourSeatName>/ inside the lane repo, plus scratch under {SCR}/<YourSeatName>/. Production files ({L}/plans, {L}/corpus, {L}/SKILL.md, {L}/SCORECARD.md, {L}/LOG.md, {L}/SHONEN.md, {L}/PROVINCE.md, {L}/.ufo/waves/round-87/L1) are READ-ONLY to you. Never edit, add or delete a production file.
- Never commit, push, stage, stash, checkout, reset or run any mutating git/jj command, in any repo. Read-only git (log, show, cat-file, status, diff, ls-files, rev-parse, archive, merge-base) is fine. Never touch the fleet repo /home/vgpnk/Projects/shokunin, sibling lanes, lane jj state, lane Git index, .ufo/state, .ufo/watchdog.log or .scratch.
- Git fixtures: `D=$(mktemp -d -p {SCR}/<YourSeatName>) && git -C "$D" init -q`; every later git call names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before any commit. A clone of the lane is allowed only under {SCR}/<YourSeatName>/ with `git clone --no-hardlinks`; never commit into the lane.
- Scratch: everything under {SCR}/<YourSeatName>/ with `mkdir -p`; pass `--work` explicitly; never rely on an inherited TMPDIR; delete the scratch tree before you yield (`trap 'rm -rf -- "$S"' EXIT`); copy receipts into your wave dir first. /tmp is for files under 50 MB only; never cite a /tmp path as evidence.
- Network: at most the pinned raw.githubusercontent.com fetches your item names. No credentials, cookies, tokens or auth state are read or used.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your output). pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are PAUSED host-wide; install via `uv tool`, `npx` or an official binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R/downgrade/restart a host service.
- Do not file the round report; the L1 does. Do not message other seats or agent://all. Do not edit the instruments; report defects instead.
- Your final message ends with exactly one line: `SEAT <YourSeatName> VERDICT <PASS|FINDINGS|BLOCKED> findings=<n>` where findings is the count of defects you actually found (0 for PASS)."""


def item(name, role, task):
    return {"name": name, "role": role, "prompt": "/skill:godspeed\n\n" + task}


def build():
    items = [
        item("ScoutR87", "scout", f"""# Item ScoutR87 — member recon and class arithmetic (read-only)
Read {L}/plans/round-87-claims.md section R87-C1 and {L}/corpus/evidence/round52/graders/mteb-retrieve/tests/test_outputs.py.
# Target
Write {W}/ScoutR87/scout-map.md with:
1. Every `def test_*` in the captured grader, its line range, and the acceptance predicate, quoted literally with line numbers. Name every import and say whether it is stdlib (`python3 -c 'import sys; print(sys.stdlib_module_names)'` or the stdlib list).
2. The member's ledger row at {BASE} and at {TIP} (`git -C {L} show <rev>:plans/grader-population-ledger.json`), and the per-class executed/total for `file-artifact` at both revisions, computed by you with a stated command.
3. Verify the frozen claim sentences "executed 30 -> 31" and "file-artifact 22 of 76 -> 23 of 76" by your own count. State the command.
4. List every UNEXECUTED member whose captured grader is single-file and stdlib-only, with its test count and assert count (command shown). Confirm or refute that mteb-retrieve is the cheapest such candidate under the rule the lesson states (`corpus/lessons/round-87.md` Gate). Name the disqualifying line for each alternative you reject.
Every claim carries path:line or command output. Do not edit production files."""),
        item("ScribeR87", "scribe", f"""# Item ScribeR87 — source re-open and gate-record check (frontier step, read-only)
Read {L}/corpus/SOURCES.md rows S275 and S276, and {L}/corpus/lessons/round-87.md section Gate.
# Target
1. Re-open the two pinned sources yourself (one fetch each, `curl -sSL -o <scratch file> -w '%{{http_code}} %{{size_download}}'`): https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/mteb-retrieve/tests/test_outputs.py and https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/mteb-leaderboard/tests/test_outputs.py. Record HTTP status, bytes, sha256, and `cmp` against the matching round-52 capture under {L}/corpus/evidence/round52/graders/.
2. For each quote in S275 and S276, check it appears verbatim at the cited line, counts <= 25 whitespace-split words, and carries no `|` character.
3. Check every new registry row (S275, S276): exactly 11 cells between the outer pipes, legal enum values (tier A, kind code, status mined/rejected), recheck format, used-by path existence (`corpus/lessons/round-87.md` exists for S275). Check that the lesson Gate table agrees with each row (id, URL, access date, quote, decision).
4. Check the statement in the lesson that S276 is "rejected" and that a REJECTED row carries a `flip:` clause.
Write {W}/ScribeR87/source-check.md with a row per check and a PASS/FAIL. Delete your scratch files before yielding."""),
        item("ExecBaseR87", "executor", f"""# Item ExecBaseR87 — independently re-run both counters at BASE and at the tip, and the probe re-run
Read-only on {L}. Scratch under {SCR}/ExecBaseR87/.
# Target
Run from {L}, copy each command's full stdout+stderr and exit code to {W}/ExecBaseR87/replay.txt as `$ command` / output / `rc=<n>` blocks:
1. `python3 plans/round87_c1_replay.py --lane . --rev {BASE} --work <scratch>/c1base`
2. `python3 plans/round87_c1_replay.py --lane . --rev {TIP} --work <scratch>/c1tip`
3. `python3 plans/round87_c2_wording.py --lane . --rev {BASE} --work <scratch>/c2base`
4. `python3 plans/round87_c2_wording.py --lane . --rev {TIP} --work <scratch>/c2tip`
5. Independent probe re-run: `git -C {L} archive {TIP} | tar -x -C <scratch>/tree`, then `python3 <scratch>/tree/plans/round87_mteb_probe.py --lane <scratch>/tree --work <scratch>/probe`. Diff its OBSERVATIONS block against the block in {L}/corpus/evidence/round87/mteb-retrieve-probe.txt (`diff`, rc shown).
6. Verify the receipt's pins with plain commands: `git -C {L} show {TIP}:plans/round87_mteb_probe.py | sha256sum` equals TOOL_SHA; `git -C {L} show {FREEZE}:plans/round87-cases.json | sha256sum` equals CASE_TABLE_SHA; `git -C {L} show {TIP}:corpus/evidence/round52/graders/mteb-retrieve/tests/test_outputs.py | sha256sum` equals SUBJECT_SHA; `git -C {L} merge-base --is-ancestor <LANE_TIP> {TIP}` exits 0.
7. Verify the frozen claims file and case table are unchanged between the freeze and the tip, and the instruments are unchanged between {INSTR} and {TIP}: `git -C {L} diff --stat {FREEZE} {TIP} -- plans/round-87-claims.md plans/round87-cases.json` and `git -C {L} diff --stat {INSTR} {TIP} -- plans/round87_mteb_probe.py plans/round87_c1_replay.py plans/round87_c2_wording.py plans/round87_report_paths.py`. Record the output.
Verdict per check (match / mismatch) in {W}/ExecBaseR87/summary.md. Delete scratch before yielding."""),
        item("ExecCtrlR87", "executor", f"""# Item ExecCtrlR87 — rebuild the control fixtures independently and add two controls of your own
Read-only on {L}. Scratch under {SCR}/ExecCtrlR87/.
# Target
Rebuild each control from a fresh `git clone --no-hardlinks {L} <scratch>/<name>` checked out at {TIP} (verify the clone toplevel with `git -C "$D" rev-parse --show-toplevel`). Commit fixture edits only inside those clones with `-c user.name=fixture -c user.email=fixture@scratch.local`. Run the counters with `--rev HEAD`. Record `$ command`, output and rc in {W}/ExecCtrlR87/controls.txt.
1. ledger-only: remove the receipt in the clone; expect a defect at L1-receipt and no other leg.
2. forged LANE_TIP: replace the LANE_TIP line of the receipt with the hash of a parentless orphan commit created by `git commit-tree`; expect L3-tip.
3. C2 canon-wrong: in a fresh `git init` repo, plans/round86-cases.json from {BASE}, and a corpus/README.md whose lessons/round-86.md row says "eight case shapes, five schema-drift and three controls"; expect a CANON defect.
4. Your own control A: in a clone, change ONE CASE observed value in the receipt's OBSERVATIONS block so that observed != predicted, leaving the summary line `mismatches=0`. Predict which leg fires (L5 by name or L6 via re-run) BEFORE running; then run and report.
5. Your own control B: in a clone, change one byte of plans/round87-cases.json (e.g. a predicted vector) and commit. Predict the leg (L4) BEFORE running; run and report.
Each row: PREDICTED leg, OBSERVED DEFECT lines, rc. Delete scratch before yielding."""),
        item("ExecCensusR87", "executor", f"""# Item ExecCensusR87 — registry census before and after, and the pointer checker's red and green
Read-only on {L}. Scratch under {SCR}/ExecCensusR87/.
# Target
1. Census BEFORE: `git -C {L} archive {BASE} corpus | tar -x -C <scratch>/base`; run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/base/corpus/SOURCES.md`, record its rc and the W04 line count. Census AFTER: the same with `git -C {L} archive {TIP} corpus` and `--file`. Also run the round-end form `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` and record rc (must be 0).
2. Row count, tier histogram, status histogram, duplicate ids, malformed rows (NF != 13), enum violations and tier inflation, for both revisions, using the frozen awk commands in {L}/CORPUS.md section "Census — run from the lane root" (copy them exactly; run against the extracted files). Record each output and the expected value (BEFORE 266 rows; AFTER 268 rows; status mined 242 -> 243; rejected 16 -> 17; queued 8).
3. Ledger arithmetic by plain Python: executed count and file-artifact executed/total at BASE and TIP (`json.load` of plans/grader-population-ledger.json at each revision).
4. Pointer checker red-before: `python3 {L}/plans/round87_report_paths.py --lane {L} --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-86/kengaku.md` — record rc and the DEFECT line (must be 1 and name outside-gates.txt). Do NOT run it on any report that is not yet filed; green-after is the L1's job.
Write {W}/ExecCensusR87/census.md with every command, output and rc. Delete scratch before yielding."""),
        item("ReviewerR87a", "reviewer", f"""# Item ReviewerR87a — correctness attack on the R87-C1 counter and probe (read-only)
Read {L}/plans/round87_c1_replay.py and {L}/plans/round87_mteb_probe.py in full, and {L}/plans/round-87-claims.md section R87-C1.
# Target
1. For each leg L1–L8, state the exact code path that produces its DEFECT line and quote it (path:line). Say whether each leg can be satisfied by a receipt that the probe did not produce at the measured tree.
2. L6 compares the whole observation block (line equality). Confirm by quoting the comparison, and state what a receipt with an extra or reordered CASE line would do.
3. L5 requires the frozen tuple in the frozen order. Confirm, and state whether a receipt with a duplicate case id can pass.
4. Find any way to make the counter exit 0 at a measured revision that does not carry a real execution of the captured grader. Name the attempt, the command and the output. If none found, say which leg is the sole reason and why.
5. Check the probe's sandbox: does the bwrap argv bind anything writable outside the case directory? Does any case write outside the case directory?
Each finding: path:line, severity (BLOCKER/MAJOR/MINOR/NONE), and the command that would show it. Write {W}/ReviewerR87a/report.md."""),
        item("ReviewerR87b", "reviewer", f"""# Item ReviewerR87b — claim/predicate consistency and frozen-text attack (read-only)
Read {L}/plans/round-87-claims.md, {L}/plans/round87_c2_wording.py, {L}/plans/round87_c1_replay.py, and the SCORECARD rubric for calibration in {L}/SCORECARD.md (search for "calibration" rubric language).
# Target
1. The claim file's "before" numbers: check each against the counter's own BASE output in {L}/.ufo/waves/round-87/L1/base-runs.txt. Name every number that disagrees and quote it. Say whether the predicate or target sentence is affected.
2. The C2 control text says a fixture with "five schema-drift and three controls" must report `mismatches>=1`. Run the counter on such a fixture (you may build it in scratch: a git init repo with the table copied from {BASE}) and report what it returns. Say whether the frozen text is met as written.
3. The claim file says each predicate is "the same sentence in the plan, the counter's PREDICATE line and the report". Compare the three for C1 and C2 and quote them.
4. Quote the SCORECARD calibration rubric and state whether a mismatch-count move 1 -> 0 at score 10 is an axis move under that rubric, or a held-score restoration. Use the round-86 precedent in {L}/SCORECARD.md as a comparison, quoting its wording.
5. Confirm with git that the frozen claim file and case table are unchanged between {FREEZE} and {TIP}, and that the instruments are unchanged between {INSTR} and {TIP} (use `git diff --stat`; quote output).
Each finding: path:line, severity and the command. Write {W}/ReviewerR87b/report.md."""),
        item("ReviewerR87c", "reviewer", f"""# Item ReviewerR87c — non-author discernment spot-check of this round's gate decisions (LEARNING.md)
Read {L}/corpus/lessons/round-87.md section Gate, {L}/corpus/SOURCES.md rows S275 and S276, and {L}/corpus/QUALITY.md criteria Q66 (and Q63–Q65 for context).
# Target
1. Admit decision (S275, mteb-retrieve as the member replay). Re-open the source yourself (one fetch: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/mteb-retrieve/tests/test_outputs.py) and decide agree / disagree with the admit, with a reason tied to the QUALITY bar and to the scope "member replay only".
2. Reject decision (S276, mteb-leaderboard). Re-open its source (one fetch: .../mteb-leaderboard/tests/test_outputs.py) and decide agree / disagree with the reject, with the flip condition stated in the row. Say whether the reason is sound or a taste call.
3. Check Q66 in {L}/corpus/QUALITY.md: is it a criterion with a grounding, and does it claim an executable half it does not have? Quote.
4. Name any candidate that the lesson omits but should have considered, with the reason.
Write {W}/ReviewerR87c/spotcheck.md as a table: decision | source re-opened | agree/disagree | reason. End with one line `SPOTCHECK admit=<agree|disagree> reject=<agree|disagree>`."""),
        item("CriticR87", "critic", f"""# Item CriticR87 — adversarial review of both frozen claims (read-only)
Read {L}/plans/round-87-claims.md in full, the counters {L}/plans/round87_c1_replay.py and {L}/plans/round87_c2_wording.py, the README row in {L}/corpus/README.md, and {L}/corpus/QUALITY.md Q66.
# Target
Attack each claim against: (a) the do-nothing control (can a change that does no real work pass the predicate?), (b) the section 9 sizing rules (no universal clauses, one count per claim, no narrowing after landing), (c) the admission bar (a measured improvement on a distinct axis, no axis harmed).
1. R87-C2: can the predicate be satisfied by editing only the README row text, without any derivation from the table? If so, is the claim a calibration move or a wording repair, and does the claim text say which? Quote.
2. R87-C1: is a fifth member replay a real coverage move, or a re-scored class? Check the class arithmetic in the lesson against the ledger; say whether the frontier moves or only a count does.
3. Separability: does R87-C2 depend on R87-C1 landing, or the reverse? Show the command that proves it or refutes it.
4. Any further frozen-text imprecision besides the BASE figure (predicate vs counter, control vs counter behaviour). Quote.
Give every finding a severity (BLOCKER/MAJOR/MINOR/FINDING) and say what would falsify your own reading. Write {W}/CriticR87/critique.md."""),
        item("MutTesterR87", "mutation-tester", f"""# Item MutTesterR87 — mutation battery on both counters (read-only on production)
Build mutants under {SCR}/MutTesterR87/ (copy the counter files from {L}/plans/ into scratch; never edit production). Write results to {W}/MutTesterR87/mutants.md.
# Target
1. Invent at least SIX mutants of {L}/plans/round87_c1_replay.py that each disable one guard (e.g. skip the L3 ancestor check; accept any LANE_TIP; compare only the summary line in L6; skip the L7 receipt field check; count executed rows as a constant; read the table from the measured tree instead of FREEZE_REV). Run the unmutated and mutated counter against the fixture each mutant should let through (reuse the fixture method: clone at {TIP} under scratch, commit with fixture identity). Report: the unmutated counter's rc and DEFECT line, the mutant's rc.
2. At least FOUR mutants of {L}/plans/round87_c2_wording.py (e.g. a regex that misses "frozen"; derive schema count from the wrong field; drop the canonical-row check; scope that omits README).
3. For each mutant: killed (mutant rc differs from the unmutated rc on the fixture) or survived. Declare each mutant necessary (the removed check is the only catcher) or redundant (another leg catches the same fixture), and name the catching leg for redundant ones.
Never edit the committed counters. Delete scratch before yielding."""),
        item("SentinelR87", "sentinel", f"""# Item SentinelR87 — isolation and confidentiality review of this round's evidence path (read-only)
Threat-model {L}/plans/round87_mteb_probe.py, {L}/plans/round87_c1_replay.py, {L}/plans/round87_c2_wording.py, {L}/plans/round87_report_paths.py and the receipt {L}/corpus/evidence/round87/mteb-retrieve-probe.txt.
# Target
1. Isolation: list every bwrap flag the probe uses and state what the case harness can and cannot reach (host /app, network, the lane tree, environment, /etc). Prove the host /app is not written by a probe run (`ls -ld /app` before and after, if it exists; otherwise state absence).
2. Confidentiality: does any new file read credentials, env vars, cookies, tokens, network, or $HOME? Does the receipt leak anything beyond the work path and hashes? Grep the four scripts and the receipt for `HOME`, `token`, `secret`, `key`, `cookie`, `http`, and quote the hits.
3. Integrity: can a case's staged `/app/result.txt` influence anything beyond the eight frozen cases? Can the graded module import from the staged tree? Quote the bind list.
4. Fabrication surface: state exactly what an adversary who can write the lane tree could forge and which leg would still refuse.
Severities per finding; the command or output for every claim; route findings you cannot remediate in-lane. Write {W}/SentinelR87/report.md."""),
        item("ConnectorR87", "connector", f"""# Item ConnectorR87 — sibling-overlap scan (read-only across sibling lanes; never write there)
# Target
1. Search the sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin (read-only: grep and git show only) for: (a) another replay of the same grader (`mteb-retrieve` or `mteb-leaderboard`); (b) a receipt that pins a LANE_TIP ancestor and re-runs its probe (the same mechanism as R87-C1 L3/L6); (c) a counter that derives a count from a table to check live-doc wording (the R87-C2 mechanism). Cite file:line.
2. For each hit, classify DUPLICATE (the mechanism already exists there) or NEW-MECHANISM, with a two-sentence description. Do not absorb anything.
3. State which instrument is the fleet-first, if either, and which owning lane would hold a shared standard.
Write {W}/ConnectorR87/overlap.md. Report only; no edits anywhere."""),
    ]
    return {
        "wave": "kengaku-r87-w1",
        "milestone": "R87 fifth executed TB2 member (mteb-retrieve, located offline replay) and the round-86 live-doc case-set wording repaired against the table-derived split",
        "maxLanes": 12,
        "axes": ["coverage", "calibration"],
        "context": CONTEXT,
        "items": items,
    }


if __name__ == "__main__":
    spec = build()
    out = f"{WAVE}/w1-spec.json"
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(spec, handle, indent=1)
    print(out, len(spec["items"]), dict(Counter(i["role"] for i in spec["items"])))
