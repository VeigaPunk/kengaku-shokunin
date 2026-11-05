#!/usr/bin/env python3
"""Render the round-86 v1 wave spec (12 seats) — wave evidence, not a production gate."""
import json
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
W = f"{L}/.ufo/waves/round-86/w1"
SCR = "/fast/scratch/hyaku/kengaku-r86"
WAVE = f"{L}/.ufo/waves/round-86"

CONTEXT = f"""# Goal and frozen contract
Kengaku round 86, ONE v1 wave, 12 seats. L1 KengakuR86 owns integration and the planner seat; you are a leaf seat: never spawn subagents, never call task.
Read {L}/plans/round-86-claims.md IN FULL first (frozen at 61b0e074a44259c8c022aa2fda257182a0708346; base 88651a72ef112ed9f5361e1c8c197babec691f96). Never change its predicate, target, case table, control set, kill rule or leg list. If a frozen element looks wrong, say so in your output; do not edit it.
Claims: R86-C1 coverage — one more executed member (`raman-fitting`) via a located offline replay of its pinned captured grader over eight frozen schema-drift cases; counter `plans/round86_c1_replay.py`, target `defects=0`, BASE `defects=7`. R86-C2 calibration — the lane's own self-assessment mismatch count 1 -> 0, with `SHONEN.md` box 4's `PROVINCE.md:129` pointer re-derived to line 151 from bytes; counter `plans/round86_c2_repin.py`, target `defects=0`, BASE `defects=3`.
Instruments are frozen at 316811fa604eeef1d157bdbf62b5595891dc015a; the pre-data battery and both BASE runs are committed at .ufo/waves/round-86/L1/freeze-battery.txt and base-runs.txt. Any instrument byte changed after the tip run voids both claims — report it if you find it.

# Hard bounds
- Write scope: ONLY your own directory {W}/<YourSeatName>/ inside the lane repo, plus scratch under {SCR}/<YourSeatName>/. Production files ({L}/plans, {L}/corpus, {L}/SKILL.md, {L}/SCORECARD.md, {L}/LOG.md, {L}/SHONEN.md, {L}/PROVINCE.md, {L}/.ufo/waves/round-86/L1) are READ-ONLY to you. Never edit, add or delete a production file.
- Never commit, push, stage, stash, checkout, reset or run any mutating git/jj command, in any repo. Read-only git (log, show, cat-file, status, diff, ls-files, rev-parse, archive, merge-base) is fine. Never touch the fleet repo /home/vgpnk/Projects/shokunin, sibling lanes, .ufo/state, .ufo/watchdog.log or .scratch.
- Any fixture repo you create is `D=$(mktemp -d -p {SCR}/<YourSeatName>) && git -C "$D" init -q` and every later git/jj call names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before any commit. Never run git commit/jj with a throwaway identity anywhere else.
- Scratch: everything under {SCR}/<YourSeatName>/ with `mkdir -p`; delete it before you yield (receipts first copied into your wave dir). /tmp is for files under 50 MB only; never cite a /tmp path as evidence.
- Network: at most the single pinned raw.githubusercontent.com fetch your item names. No credentials, cookies, tokens or auth state are read or used.
- Every `Report:` trailer path a rendered prompt shows is relative to {L} — write it at {L}/<that path>.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your output). pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R/downgrade/restart a host service.
- Do not file the round report; the L1 does. Do not message other seats or agent://all.
- End your final message with exactly one line: `SEAT <YourSeatName> VERDICT <PASS|FINDINGS|BLOCKED> findings=<n>` where findings is the count of defects you actually found (0 for PASS)."""


def item(name, role, task):
    return {"name": name, "role": role, "prompt": "/skill:godspeed\n\n" + task}


CAP = "corpus/evidence/round52/graders/raman-fitting/tests/test_outputs.py"


def build():
    items = [
        item("ScoutR86", "scout", f"""# Item ScoutR86 — member-byte recon and class arithmetic (read-only)
Read {L}/plans/grader-population-ledger.json and {L}/plans/round-86-claims.md section R86-C1.
# Target
Write {W}/ScoutR86/scout-map.md with:
1. Open {L}/corpus/evidence/round52/graders/raman-fitting/tests/{'test_outputs.py'} yourself. List every `def test_*` in source order with its line range, and quote — literally, with line numbers — the acceptance predicate of each. State which of the three legs can raise a non-AssertionError exception and on which input shape.
2. Name every `import` in that file; say for each whether it is stdlib. Name any subprocess/binary it invokes. The frozen claim replays it offline: state from the bytes whether that is possible without a service, a GPU or a third-party package.
3. From the ledger: the executed/unexecuted split, the per-class executed/total for `serialization-schema`, `file-artifact` and `numeric-band`, and the exact member list of `serialization-schema` with each member's status. Confirm or refute the claim sentence's "grows by exactly one member" with the numbers you derived yourself (state the command).
4. Report whether any *other* unexecuted member's captured grader is stdlib-only and single-file (cheapest next candidate), naming the member and the disqualifying line if not.
Every claim gets path:line. Do not edit production files."""),
        item("ExecBaseR86", "executor", f"""# Item ExecBaseR86 — independently reproduce both counters at BASE and tip
Read-only on {L}. Use scratch under {SCR}/ExecBaseR86.
# Target
Run from {L} and copy each command's full stdout+stderr and exit code to {W}/ExecBaseR86/replay.txt as `$ command` / output / `rc=<n>` blocks:
1. `python3 plans/round86_c1_replay.py --lane . --rev 88651a72ef112ed9f5361e1c8c197babec691f96 --work <scratch>`
2. `python3 plans/round86_c1_replay.py --lane . --rev master --work <scratch>`
3. `python3 plans/round86_c2_repin.py --lane . --rev 88651a72ef112ed9f5361e1c8c197babec691f96 --work <scratch>`
4. `python3 plans/round86_c2_repin.py --lane . --rev master --work <scratch>`
5. `python3 plans/state_check.py --summary` and `python3 plans/state_check.py --summary --root <BASE extraction>` (base tree: `git -C {L} archive 88651a72ef112ed9f5361e1c8c197babec691f96 | tar -x -C <scratch>/base`).
Then verify the C1 receipt against committed bytes yourself, with plain commands (no library beyond pathlib/hashlib):
- `git -C {L} cat-file -p <LANE_TIP>:plans/round86_raman_probe.py | sha256sum` equals the receipt's `TOOL_SHA`;
- `git -C {L} cat-file -p 61b0e074a44259c8c022aa2fda257182a0708346:plans/round86-cases.json | sha256sum` equals `CASE_TABLE_SHA`;
- `git -C {L} cat-file -p master:{CAP} | sha256sum` equals `SUBJECT_SHA`;
- `git -C {L} merge-base --is-ancestor <LANE_TIP> master` exits 0.
Record each as `CHECK <name> ok|FAIL <observed>`. No edits to production."""),
        item("ExecGatesR86", "executor", f"""# Item ExecGatesR86 — standing gate roster from an extracted tree
QUALITY requires a landing that touches a gate to cite a gate run made OUTSIDE the working copy.
# Target
1. Extract the tip: `git -C {L} archive --format=tar master | tar -x -C <scratch>/tip` (record `git -C {L} rev-parse master`).
2. In that extracted tree run and record exit codes plus the count lines: `python3 grader.py | grep -E 'CHECKS n=|VERDICT:'`; `python3 plans/sources_adopt.py --selftest | tail -1`; `python3 plans/registry_check.py --selftest | tail -1`; `python3 plans/config_projection.py --selftest | tail -1`; `python3 plans/benchmark_spec_audit.py --selftest | tail -1`; `python3 plans/gate_timing_check.py --selftest`; `python3 plans/state_check.py --selftest`.
3. Run the round-86 counters' own batteries from the extracted tree: `--selftest` and `--mutants` for both `plans/round86_c1_replay.py` and `plans/round86_c2_repin.py` (pass `--lane {L} --repo {L}` for c1 so the frozen table resolves from the real repo).
4. Compare each printed count with the count the previous landing recorded (grep {L}/LOG.md for the round-85 gate block). Any difference is a finding; name the line.
Write everything to {W}/ExecGatesR86/gate-receipt.txt as `$ command` / output tail / `rc=<n>`. Measure and transcribe; judging is not your job."""),
        item("ExecCensusR86", "executor", f"""# Item ExecCensusR86 — sources census and index parity, before and after
# Target
1. `sh /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` from /home/vgpnk/Projects/shokunin; record exit code, the final ok/FAIL line and the `kengaku` verdict line.
2. Row arithmetic from committed bytes only: `git -C {L} show master:corpus/SOURCES.md` piped to `grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|'`; the tier column histogram and the status column histogram (11 cells, `awk -F'|'`); the highest S id; and the W04 warning count from step 1. State the next free id.
3. Index parity: find the R75 tool with `grep -rl 'UNIVERSE knowledge' {L}/plans | head -1`, run it from {L}, record the UNIVERSE/PREDICATE lines and rc.
4. Population gate: `grep -rl 'R79-C1' {L}/plans | head -1`, run it, record TARGET/DEFECTS/PREDICATE and rc.
5. `python3 plans/defect_ledger.py --lane .` from {L}: record rc and any `agree=NO`. `python3 plans/round82_c1_plans_registry.py --lane .`: record rc and PREDICATE.
Write commands, outputs and rc values to {W}/ExecCensusR86/census.txt. Flag any gate red NOW as a finding with its exact defect line."""),
        item("SourceR86", "scribe", f"""# Item SourceR86 — open the pinned raman-fitting grader and draft the S274 row
# Target
1. Fetch with curl (write only under your scratch): https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/raman-fitting/tests/test_outputs.py ; record HTTP status, byte count and sha256, and compare with {L}/{CAP}. If the sha256 differs, say so loudly — the claim's `SUBJECT_SHA` depends on it.
2. Read {L}/corpus/SOURCES.md lines 1-20 and the rows S271-S273 (`grep -n '^| S27' ...`) to copy the 11-column schema exactly, then write {W}/SourceR86/s274-row.md with ONE proposed row: id S274, the same kind/scope vocabulary as its neighbours, the exact anchor URL, a located quote of at most 25 words with its line number, status mined, opened 2026-11-04, a recheck value (ISO date or `NNd`), `used-by` naming the round-86 lesson, and no literal or escaped `|` inside any cell.
3. State the word count of your quote and how you counted it (`len(quote.split())`).
4. Draft the Gate block the lesson needs: URL, access date 2026-11-04, located quote, admit reason, flip condition. Write it to {W}/SourceR86/gate-block.md.
Do not edit corpus/SOURCES.md yourself."""),
        item("ScribeR86", "scribe", f"""# Item ScribeR86 — draft the round-86 lesson and the SCORECARD/LOG append blocks
Read {L}/corpus/lessons/round-85.md (Gate/Mistakes/Definition-horizon shape), {L}/corpus/lessons/round-85-verifier-spotcheck.md (what the outside check rejected), {L}/corpus/QUALITY.md and {L}/plans/round-86-claims.md.
# Target
1. {W}/ScribeR86/round-86.md — lesson body: header (round, date, L1, base 88651a72, freeze 61b0e074, instrument 316811fa); `## Gate` with the S274 table (admit/reject columns, access date, <=25-word located quote, reason/flip); `## Corrections` for anything this round repairs; `## Mistakes` table with class / evidence pointer / captured-by / fix, including the two instrument defects the round found at its own pre-data battery (the `freeze-anchor-fails-closed` leg that tested the measured tree while the counter reads the repo, and the `state_check` re-derivation that made two C2 legs mutation-redundant) and any error you can evidence from rounds 85's own bytes; `## Definition horizon` — what a future file could make this lesson wrong about.
2. {W}/ScribeR86/scorecard-block.md — a `## Round 86` SCORECARD section: two claim rows (R86-C1 coverage, R86-C2 calibration) with before -> after, counting command and measured commit placeholders left as `<L1 fills>`, the other five axes as a held/no-change line, and a `### Planned (round 87)` list of three next moves.
3. {W}/ScribeR86/log-block.md — a `## Round 86` LOG section: header naming coverage as the lowest non-retired axis (score 7, L0 cap `kengaku | round-25/33/51`), the work items, the receipts and their commits, and the re-verification lines.
Facts you do not know must be written as `<L1 fills: ...>`, never invented. Do not edit SCORECARD.md or LOG.md."""),
        item("ReviewerC186", "reviewer", f"""# Item ReviewerC186 — independent derivation and replay attack on R86-C1
Attack seat. Read-only except your own directory.
# Target
1. WITHOUT reading {L}/plans/round86-cases.json or {L}/plans/round86_raman_probe.py, derive from the grader source alone ({L}/{CAP}) the predicted three-leg vector for each of the eight case shapes named in {L}/plans/round-86-claims.md section R86-C1: exact, missing-2D-key, g-amplitude-string, extra-schema-keys, absent-file, g-key-renamed, 2D-null-value, g-amplitude-just-outside. Write the derivation, with the Python/json semantics you relied on, to {W}/ReviewerC186/derived.txt.
2. Compare with the frozen table and with `python3 plans/round86_raman_probe.py --lane . --work <scratch>` output. Any disagreement is a finding.
3. Run `python3 plans/round86_c1_replay.py --lane . --rev master --work <scratch>`; then confirm the counter's BASE state in a scratch extraction of 88651a72.
4. Check that the frozen predicate sentence in plans/round-86-claims.md is the same sentence as the counter's `PREDICATE R86-C1` line and the label the report will carry; quote both.
5. Attack L6: does `reproduce` compare the whole observation block, or only the summary line? Quote the comparison. Attack L3: what receipt can satisfy it without being minted at this tip?
Write findings to {W}/ReviewerC186/report.md, each with path:line or command output."""),
        item("ReviewerC286", "reviewer", f"""# Item ReviewerC286 — is the box-4 re-pin a repair or a laundering? (attack on R86-C2)
Attack seat. Read-only except your own directory.
# Target
1. Read {L}/corpus/lessons/round-85.md §Closing erratum and the round-25/26 correction history for `P3c.box.4.pointer.1` (`git -C {L} log -S'P3c.box.4' --oneline -- plans/state_check.py`, then read the commits). State what the pin was, and every time it moved.
2. Read {L}/plans/round86_c2_repin.py. Decide, with quotes: does `P1-derive` read the line from bytes or from a constant? Can the counter pass on a tree where the pointer is stale but the pin was hand-moved to a *different* wrong line? Demonstrate with your own fixture.
3. Run the four controls and both base/tip runs yourself; record whether any control reaches the target.
4. Attack the claim's honesty: the repair moved a *frozen* pin from 129 to 151. Name the condition under which that is a repair (the pointer and the token moved together in the same commit for an unrelated reason) and the condition under which it is laundering (the pin followed the pointer). Say which one the committed history shows, with commit hashes.
5. `STALE_LINE = 129` is retained. Is that enough retention, or does the record need the round-26 correction line quoted? State what is missing, if anything.
Write {W}/ReviewerC286/report.md with one row per question and an explicit verdict per question."""),
        item("CriticR86", "critic", f"""# Item CriticR86 — adversarial review of both frozen claims
Read-only attack. Read {L}/plans/round-86-claims.md in full; {L}/plans/round86-cases.json; {L}/plans/round86_c1_replay.py; {L}/plans/round86_c2_repin.py; {L}/plans/round86_raman_probe.py; {L}/corpus/QUALITY.md; {L}/corpus/lessons/round-85-verifier-spotcheck.md.
# Target
Attack each claim against its frozen predicate, target, kill rule, the lane's admission bar and the section 9 claim-sizing rules (do-nothing control, one-artifact-one-claim, no narrowing after landing, the same sentence in plan/counter/label, name the axis by the surface changed).
For R86-C1 ask: is a member replay a real coverage move or a re-scored class (db-wal-recovery and sqlite-db-truncate are already `serialization-schema`)? Does the counter go green on ledger-only data, a forged receipt, or a table committed after the freeze? Is the `E` verdict (uncaught exception) a graded observation or a harness artefact — i.e. is the vector discriminating about the grader, or about the harness? Would a strict-type grader mutant still produce the frozen vector?
For R86-C2 ask: is 1 -> 0 a real calibration move or a bookkeeping repair that the SCORECARD's own rubric already counts as "restore, not extend"? Is the claim separable from C1? Is the axis named by the surface (self-assessment mismatch) or by the number?
Give every finding a severity (BLOCKER/MAJOR/MINOR/FINDING) and say what would falsify your own reading. Write {W}/CriticR86/critique.md."""),
        item("MutTesterR86", "mutation-tester", f"""# Item MutTesterR86 — your own mutation battery on both new counters
Read-only on production; build mutants under {SCR}/MutTesterR86 and write results to {W}/MutTesterR86/mutants.md.
# Target
1. Read {L}/plans/round86_c1_replay.py and {L}/plans/round86_c2_repin.py. Invent at least SIX of your own mutants (not the shipped `MUTANTS` tuples) that disable a check or a guard: accept a receipt whose WORKTREE says dirty; ignore `EXIT`; accept a table whose `member` differs from the frozen one; make the freeze anchor `SetupDefect` non-fatal; make `executed` always 1; make `P1-derive` return `STALE_LINE`; skip `P5-selftest`; accept a receipt whose observation block lacks the `PREDICATE R86-PROBE` line.
2. For each mutant, construct the fixture it should let through and demonstrate (a) the unmutated counter REJECTS that fixture and names the leg, (b) the mutant accepts it. Copy the mutated counter and the fixture under your scratch only.
3. Report which mutants are necessary (the removed check is load-bearing) and which are redundant (another leg catches the same fixture) — redundancy is defence in depth, not a failure, and must be named with its catcher.
Never edit the committed counters."""),
        item("SentinelR86", "sentinel", f"""# Item SentinelR86 — isolation and confidentiality review of this round's evidence path
Read-only. Threat-model {L}/plans/round86_raman_probe.py, {L}/plans/round86_c1_replay.py, {L}/plans/round86_c2_repin.py and the receipt {L}/corpus/evidence/round86/raman-fitting-probe.txt.
# Target
1. Isolation: list every bwrap flag the probe uses and state what the case harness can and cannot reach (host `/app`, network, the lane tree, environment). Prove the host `/app` is unchanged by a probe run (`ls -ld /app` and a content hash before/after, if `/app` exists) and that no file outside the work dir is written (run with a read-only-ish watch, e.g. compare `find` output over the lane before/after).
2. Confidentiality: does any instrument read credentials, env vars, cookies, tokens, network or `$HOME`? Does the receipt leak anything beyond a work path? Note that `c1_replay.py` passes a stripped `env` to subprocesses — verify that and say what it does not cover.
3. Integrity: can a candidate-controlled file at `/app/results.json` influence the counter's verdict beyond the eight frozen cases? Can the graded module import anything from the candidate's staged tree (check the harness's `sys.path` and cwd)?
4. Fabrication surface: the counter's `L6` re-runs the tool from the measured tree. State exactly what an adversary who can write the lane tree could forge, and which leg (if any) would still refuse.
Write {W}/SentinelR86/report.md with severities and the command/output for every claim; route findings you cannot remediate in-lane."""),
        item("ConnectorR86", "connector", f"""# Item ConnectorR86 — sibling-overlap scan for the two primitives this round uses
Read-only across sibling lane repos under /home/vgpnk/Projects/shokunin (never write there).
# Target
1. Search the sibling lanes for a **derived self-assessment pin** (a frozen pointer whose target line is computed from bytes rather than hardcoded) and for a **replay receipt bound to a resolvable ancestor tip**. Suggested greps: `grep -rln 'merge-base.*--is-ancestor' /home/vgpnk/Projects/shokunin/*-shokunin/{{scripts,tools,plans}} 2>/dev/null | head -20`; `grep -rln 'derived_line\\|derive.*pointer\\|re-derive' /home/vgpnk/Projects/shokunin/*-shokunin/{{scripts,tools,plans}} 2>/dev/null | head -20`.
2. For each hit, classify DUPLICATE (the same mechanism already exists there) or NEW-MECHANISM (a different resolution path), with the file:line and a two-sentence description. Do not absorb anything.
3. State which of this lane's two instruments is a fleet-first, if either, and which is the cheapest candidate for a shared standard. Name the owning lane when one exists (protocol/integrator for a fleet-wide standard).
Write {W}/ConnectorR86/overlap.md. Report only; no edits anywhere."""),
    ]
    return {"wave": "kengaku-r86-w1",
            "milestone": "R86 one more executed TB2 member (raman-fitting, schema-drift replay) and the lane's last self-assessment mismatch repaired by derivation",
            "maxLanes": 12, "axes": ["coverage", "calibration"],
            "context": CONTEXT, "items": items}


if __name__ == "__main__":
    spec = build()
    out = f"{WAVE}/w1-spec.json"
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(spec, handle, indent=1)
    print(out, len(spec["items"]), dict(Counter(i["role"] for i in spec["items"])))
