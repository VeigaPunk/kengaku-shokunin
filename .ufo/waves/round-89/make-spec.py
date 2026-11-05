"""Render the round-89 v1 wave spec (11 seats) — wave evidence, not a production gate."""
import json
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
W = f"{L}/.ufo/waves/round-89/w1"
SCR = "/fast/scratch/hyaku/kengaku-r89"
WAVE = f"{L}/.ufo/waves/round-89"
BASE = "192e809d582ecbd544798cbc03da1666a0de23f7"
FREEZE = "d1c4f1b04bb39d18967075974b5984238b7c97f7"
INSTR = "0e6bb05f3a6c2d9a96bb26db31a4fd39f58c2619"
TIP_C = "000b7d1cdbbadb8086f6bb41149c3d32744105ad"
TIP = "a9b8a1a00b6a5ab5206be4d377dba439e02f8244"

CONTEXT = f"""# Goal and frozen contract
Kengaku round 89, ONE v1 wave, 11 seats. L1 KengakuR89 owns integration and holds the planner seat; you are a leaf seat: never spawn subagents, never call task.
Read {L}/plans/round-89-claims.md IN FULL first. Frozen at commit {FREEZE} (claims and case table `plans/round89-cases.json`); instruments committed at {INSTR} (`plans/round89_polyglot_probe.py`, `plans/round89_c1_replay.py`, `plans/round89_claim_figures.py`, `plans/round89-q66-records.json`, probe receipt); fixes and ledger flip at {TIP_C}; measured tip {TIP}; base {BASE}. Never change a predicate, target, case table, control set, kill rule, leg list, pinned record table or the frozen KNOWN set. If a frozen element looks wrong, say so in your output; do not edit it.
Claims: R89-C1 coverage — a seventh located offline replay of the captured `polyglot-rust-c` grader over eight frozen cases; counter `plans/round89_c1_replay.py` (`--rev`, nine legs L1–L9, `TRUSTED_TOOL_SHA` pins the probe); probe `plans/round89_polyglot_probe.py`; receipt `corpus/evidence/round89/polyglot-rust-c-probe.txt`; ledger row executed in round 89. R89-C2 calibration (ceiling) — the Q66 v2 counter `plans/round89_claim_figures.py` (`--rev`, `--controls`, `--selftest`, `--freeze-records`): record multiset pinned to `plans/round89-q66-records.json`, KNOWN check on (claim, key, claimed, measured), selftest in the predicate path, four control fixtures red and tip green.
Measured figures at the tip: C1 `TARGET executed_rows=33 member=polyglot-rust-c located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0`, `PREDICATE R89-C1 pass`. C2 `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0`, `DEFECTS n=0`, `PREDICATE R89-C2 pass`; controls `PREDICATE R89-C2-CONTROLS pass red=4 of 4 tip=green`.

# Hard bounds
- Write scope: ONLY your own directory {W}/<YourSeatName>/ inside the lane repo, plus scratch under {SCR}/<YourSeatName>/. Production files ({L}/plans, {L}/corpus, {L}/SKILL.md, {L}/SCORECARD.md, {L}/LOG.md, {L}/SHONEN.md, {L}/PROVINCE.md, {L}/.ufo/waves/round-89/L1) are READ-ONLY to you. Never edit, add or delete a production file. Do not run a counter with `--lane {L}` on a write path; run counters only on scratch clones unless the item says read-only at the lane is fine (`--rev` reads git objects only).
- Never commit, push, stage, stash, checkout, reset or run any mutating git/jj command in the lane or the fleet repo. Scratch clones may be committed inside (throwaway identity `-c user.name=seat -c user.email=seat@scratch` only inside your own clone, after `git -C "$C" rev-parse --show-toplevel` equals `$C`). Read-only git (log, show, cat-file, status, diff, ls-files, rev-parse, archive, merge-base) is fine. Never touch the fleet repo /home/vgpnk/Projects/shokunin, sibling lanes, lane jj state, lane Git index, .ufo/state, .ufo/watchdog.log or .scratch.
- Clones: `git clone --no-hardlinks {L} {SCR}/<YourSeatName>/lane` only; never clone the whole fleet.
- Scratch: everything under {SCR}/<YourSeatName>/ with `mkdir -p`; pass `--work` explicitly; never rely on an inherited TMPDIR; delete the scratch tree before you yield (`trap 'rm -rf -- "$S"' EXIT`); copy receipts and transcripts into your wave dir first. /tmp is for files under 50 MB only; never cite a /tmp path as evidence.
- Network: none beyond the pinned raw.githubusercontent.com fetch your item names, if any. No credentials, cookies, tokens or auth state are read or used.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your output). pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are PAUSED host-wide; install via `uv tool`, `npx` or an official binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R/downgrade/restart a host service.
- Do not file the round report; the L1 does. Do not message other seats or agent://all. Do not edit the instruments; report defects instead.
- Your final message ends with exactly one line: `SEAT <YourSeatName> VERDICT <PASS|FINDINGS|BLOCKED> findings=<n>` where findings is the count of defects you actually found (0 for PASS). Every finding names its command and its output."""


def item(name, role, task):
    return {"name": name, "role": role, "prompt": "/skill:godspeed\n\n" + task}


def build():
    items = [
        item("ExecCtrlC1", "executor", f"""# Item ExecCtrlC1 — R89-C1 control battery (scratch clones only)
Write {W}/ExecCtrlC1/controls.txt (one line per control: `CONTROL <name> <expected> <observed rc> <DEFECT lines>`) and {W}/ExecCtrlC1/report.md.
Set S={SCR}/ExecCtrlC1; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT. Clone the lane: `git clone --no-hardlinks {L} "$S/lane"`.
1. Positive: `python3 "$S/lane/plans/round89_c1_replay.py" --lane "$S/lane" --rev {TIP} --work "$S/w0"` — expect exit 0 and `PREDICATE R89-C1 pass`.
2. do-nothing: the same counter at `--rev {BASE}` — expect exit 1 and `PREDICATE R89-C1 fail`; list each DEFECT leg and detail verbatim.
3. ledger-only: in the clone, remove `corpus/evidence/round89/polyglot-rust-c-probe.txt` and commit (throwaway identity). Run the counter at the new HEAD — expect a DEFECT L1-receipt line and exit 1.
4. forged-receipt: in a second clone, on an orphan branch make one empty commit (`git checkout -q --orphan forge`), then replace the receipt's `LANE_TIP` line with that commit's hash and commit. Run the counter at the new HEAD — expect DEFECT L3-tip and exit 1.
5. forged-probe (Sentinel F1 case): in a third clone, replace `plans/round89_polyglot_probe.py` with a script that prints the receipt observation block with every observed value equal to its predicted value (no grader call), regenerate the receipt stamp by hand so its TOOL_SHA equals the forged bytes, commit, run the counter at the new HEAD. Expect DEFECT L9-tool and exit 1. Report separately whether L6 alone (without L9) would have passed — run the counter with the L9 line disabled in a fourth scratch copy of the counter file ONLY to report that fact; the lane's counter must not be edited.
Acceptance: every control's expected verdict is observed (predicted: 1,2,3,4,5 all exit 1 with the named defect); report any mismatch as a finding with the verbatim output. Do not repair the counter.""", ),
        item("ExecCtrlC2", "executor", f"""# Item ExecCtrlC2 — R89-C2 before-measurement: the round-88 counter on the same control fixtures (scratch only)
Write {W}/ExecCtrlC2/round88-baseline.txt and {W}/ExecCtrlC2/report.md.
Set S={SCR}/ExecCtrlC2; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT. Clone the lane at {TIP}: `git clone --no-hardlinks {L} "$S/lane"`.
Load `plans/round88_claim_figures.py` from the clone as a Python module (`importlib`). Its `run_check(lane, rev, work)` reads claims via `git(lane, "show", f"{{rev}}:{{rel}}")`. Monkeypatch that module-level `git` function so that `show` for `plans/round-87-claims.md` or `plans/round-85-claims.md` returns FIXTURE bytes, all other calls delegate to the real `git`. Fixtures, derived from the tip bytes:
 (a) doctored-claimed: R87 `defects=7` replaced by `defects=9` (first occurrence);
 (b) deleted-figure: the R85-C1 line that begins `Before (BASE` and contains `TARGET` removed;
 (c) doctored-key: R87 `defects=7` replaced by `defect=7`;
 (d) selftest-in-path: round-88 has no hook; run its `selftest(lane, rev, work)` and `run_check` separately and report whether a selftest failure can change the round-88 predicate (quote the code lines).
For each of (a)–(c): run `run_check` and print the PREDICATE line the round-88 counter emits (`PREDICATE R88-C2 pass|fail`), plus rc. Also run round-88 `run_check` at the unmodified tip for the sanity predicate.
Predicted by the frozen claim (R89-C2 Before): round-88 green on (a) and (b); (c) is a prediction you must test — record the observed result. Write the transcript exactly; no interpretation in the transcript itself. Report each observed verdict versus the prediction; a mismatch is a finding.""", ),
        item("ExecProbeR89", "executor", f"""# Item ExecProbeR89 — probe reproducibility and containment (read-only at the lane; scratch only)
Write {W}/ExecProbeR89/report.md with the commands and verbatim outputs.
Set S={SCR}/ExecProbeR89; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
1. Run the probe three times at the tip: `python3 {L}/plans/round89_polyglot_probe.py --lane {L} --work "$S/run$i"` for i in 1 2 3 (lane path read only). Extract the OBSERVATIONS block of each and `cmp` them pairwise; report the result.
2. Record `ls -ld /app 2>&1` before and after one run; record `ls /tmp | wc -l` before and after (informational only).
3. TMPDIR containment: run with `TMPDIR=/nonexistent/x python3 ...` and report whether it fails at setup or writes anywhere outside its --work tree; report the exit code.
4. Grep the three instrument files for `/tmp`, `HOME`, `environ`, `shell=True`, `os.popen`, `curl`, `http`; quote every hit with file:line (`grep -n`).
5. Wall time of one run (`time`).
Acceptance: observation blocks identical across the three runs (or a named difference); host /app untouched; no /tmp path or HOME read in the instruments (or each hit classified).""", ),
        item("ReviewerR89a", "reviewer", f"""# Item ReviewerR89a — blind prediction attack on the eight frozen vectors
Write {W}/ReviewerR89a/agreement.md.
Set S={SCR}/ReviewerR89a; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
1. Read the captured grader IN FULL: {L}/corpus/evidence/round52/graders/polyglot-rust-c/tests/test_outputs.py.
2. Read {L}/plans/round89-cases.json, but make a scratch copy with every `predicted` field deleted (`python3 -c` in $S, never editing the lane). Do NOT read the `predicted` values from the lane file.
3. For each of the eight cases in the scratch copy, stage its `files` under `$S/case-<id>/app` (exact bytes, no edits), then derive the predicted vector by reasoning from the grader's own code, and CONFIRM it by running the captured module as the probe would (the probe itself is off-limits for predictions; you may use `bwrap` directly — the same argv shape as {L}/plans/round89_polyglot_probe.py `sandbox_argv`, copied into your scratch, not imported from the lane). Record your derived vector per case with the grader line number that decides it.
4. Compare to the frozen `predicted` values (read them only after step 3 is written). Report agree/disagree per case. A disagreement is a finding; quote the line numbers.
5. Also verify the honest-limit claim in {L}/plans/round-89-claims.md (three distinct predicted vectors P, F, E) by counting them from the file.
Acceptance: a table of eight rows with derived vector, frozen vector, agreement, grader line.""", ),
        item("ReviewerR89b", "reviewer", f"""# Item ReviewerR89b — Q66 v2 attack with new fixtures (scratch clone only)
Write {W}/ReviewerR89b/fixtures.txt (one line per fixture: id, PREDICTED verdict written BEFORE running, OBSERVED rc and first DEFECT line) and {W}/ReviewerR89b/report.md.
Set S={SCR}/ReviewerR89b; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT. Clone the lane at {TIP}: `git clone --no-hardlinks {L} "$S/lane"`.
Import `plans/round89_claim_figures.py` from the clone and call `run_check(lane, rev, work, overrides={{path: text}})` (the function accepts an overrides dict of claims-file text). Write each fixture's PREDICTED verdict (red or green, with the reason in one line) into fixtures.txt BEFORE calling run_check. Fixtures (each is one edit to the tip bytes of the named claims file):
 F1 R84-C1 prose: change one word in the body of a sentence with no figure (predicted green);
 F2 R86-C1 before-figure `located=0` changed to `located=1` (predicted red);
 F3 R80-C1 before-figure line duplicated verbatim (predicted green — dedupe; state why);
 F4 R87-C1 `defects=7` changed to `defects=3` (the measured figure) (predicted red: record claimed changes);
 F5 R80-C2 a new `Before (BASE` line with `TARGET x=1` appended to its claim section (predicted red: record extra);
 F6 R84-C2 digit `4` in `ids=8` changed to `ids=9` (predicted red);
 F7 R85-C2 whole `## R85-C2` section body replaced by one prose line (predicted red: records missing).
Then for each: observed rc and the first DEFECT line. A predicted-green fixture that goes red, or a predicted-red that stays green, is a finding. Any fixture that takes more than 10 minutes is reported as a timeout finding.
Acceptance: fixtures.txt has 7 rows with predicted before observed.""", ),
        item("CriticR89", "critic", f"""# Item CriticR89 — falsify the frozen text against the measured figures (read-only)
Write {W}/CriticR89/findings.md, one line per finding: `F<n> <severity> <claim-or-file:line> <what is wrong> <evidence command and output>`.
Read {L}/plans/round-89-claims.md IN FULL and {L}/corpus/lessons/round-89.md IN FULL.
1. Recompute every ledger figure in the claims and lesson with `git -C {L} show {BASE}:plans/grader-population-ledger.json` and `git -C {L} show {TIP}:plans/grader-population-ledger.json` (python3 counting, class by class). Report any figure that is wrong.
2. Check that the predicate sentence for R89-C1 is identical in the claims file, the counter's `PREDICATE R89-C1` line area (`plans/round89_c1_replay.py` docstring and code legs) and the lesson; quote the three occurrences. Same for R89-C2.
3. Check the R89-C2 Before paragraph: it predicts the round-88 counter's green on fixtures (a) and (b); check whether the claim's `KNOWN` text and the counter's `KNOWN` set agree literally.
4. Check the lesson's Mistakes 1–4 against the commit history (`git -C {L} log --oneline -12`): is each Mistake's fix in the commit named, and is any claimed disclosure missing (e.g., the instrument fixes after commit A)?
5. Check the claims' kill-rule wording against what the counter actually enforces (e.g., does the counter check `located` only through L1–L4,L5,L6,L8,L9? Is L7 'executed' a claim-level dependency?). Quote the code.
6. Severity: CRITICAL (a frozen figure or predicate wrong), MAJOR (wording that changes what is claimed), MINOR (cosmetic). Report every finding even if minor; do not repair anything.""", ),
        item("MutTesterR89", "mutation-tester", f"""# Item MutTesterR89 — mutate both counters on scratch copies (never edit the lane)
Write {W}/MutTesterR89/mutants.md: one row per mutant with: id, file, one-line change, killed or survived, killing check (leg or control name) and the command.
Set S={SCR}/MutTesterR89; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT. Clone the lane at {TIP} as $S/lane; create one copy of each counter per mutant under $S/m<id>/ and run it FROM THE CLONE with the clone's repo as --lane (the clone is at the tip, so the rev is {TIP}).
C1 mutants (run `python3 <mutant> --lane "$S/lane" --rev {TIP} --work "$S/w<id>"`; killed = exit != 0): M1 drop the L9 check; M2 L5 vector compare keyed on case id only; M3 L3 ancestor check replaced by `True`; M4 L7 check removed; M5 L6 comparison removed; M6 FROZEN vector for `neither-compiles` changed to `P`; M7 EXIT check removed.
C2 mutants (run `python3 <mutant> --lane "$S/lane" --rev {TIP} --work "$S/w<id>" --controls`; killed = PREDICATE R89-C2-CONTROLS fail OR the plain predicate exits 1): N1 KNOWN compare drops `claimed`; N2 F7 missing-record check removed; N3 selftest removed from run_check; N4 vacuity guard removed from controls; N5 `_drop_before` marker reverted to `**Before`; N6 the `work.mkdir` line removed.
Each mutant must be a one-line change applied with a script in your scratch. Acceptance: 13 rows; each survived mutant is a finding naming what check is missing.""", ),
        item("SentinelR89", "sentinel", f"""# Item SentinelR89 — adversarial security review of the round-89 instruments (read-only)
Write {W}/SentinelR89/report.md with severities (High/Medium/Low/Info) per finding and the command or code line for each.
Read {L}/plans/round89_polyglot_probe.py, {L}/plans/round89_c1_replay.py, {L}/plans/round89_claim_figures.py in full.
1. Containment: list every bwrap flag in `sandbox_argv`; state what the case harness can read, write, or reach (host /app, /tmp, network, lane tree, environment, /etc, HOME). Confirm the staged files cannot escape the case directory (`stage()` path validation: `..` and absolute paths rejected — quote the code; a symlink in the case table is impossible because content is str only — confirm).
2. Forgery surface: an adversary who can write the lane tree can alter the counter file itself. Is any counter byte pinned (C1: TRUSTED_TOOL_SHA pins the probe only; C2: no pin of the counter)? State which leg refuses each forgery you construct in a scratch clone (e.g., a counter with `PREDICATE R89-C1 pass` hard-coded).
3. Confidentiality: does any file read credentials, env, cookies, tokens or HOME? Does a receipt leak anything beyond paths and hashes? Grep and quote hits.
4. Integrity of the observation: can the grader's stdout or stderr inject a `PAYLOAD` line that the harness mis-parses? (The harness redirects test stdout and prints one PAYLOAD line; test an adversarial grader in scratch — a case whose staged file makes the grader print a fake PAYLOAD line before the real one; report whether the probe accepts it, and state the consequence.)
5. Report any High finding as a finding; route the rest.""", ),
        item("ScoutR89", "scout", f"""# Item ScoutR89 — next-round candidates (read-only recon, no claims)
Write {W}/ScoutR89/next.md with: (a) every unexecuted ledger member whose classes include `shell-exec` or `stdout-inspection`, from `git -C {L} show {TIP}:plans/grader-population-ledger.json` (python3 counting); (b) for each, the blocker stated in its ledger row and whether the captured grader bytes (`git -C {L} show {TIP}:corpus/evidence/round52/graders/<member>/tests/test_outputs.py`) require network, ssh, a VM, a browser, a LaTeX toolchain or docker (grep for `http`, `ssh`, `qemu`, `selenium`, `pdflatex`, `docker`, `requests`, `urllib`), with the grep line numbers; (c) the top three offline candidates by class arithmetic, with the sha256 of each captured grader and the fetch command that would pin it (no fetch performed here).
Read-only: no clones are required; `git show` only.""", ),
        item("ConnectorR89", "connector", f"""# Item ConnectorR89 — sibling-overlap scan (read-only across sibling lanes; never write there)
Write {W}/ConnectorR89/overlap.md.
Search the sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin (read-only: grep and git show only; exclude this lane) for: (a) a claims-figure extractor that re-runs historical counters (the R89-C2 mechanism); (b) a counter that pins its probe by sha256 constant (the R89-C1 L9 mechanism); (c) a receipt with OBSERVATIONS_BEGIN/OBSERVATIONS_END markers; (d) another replay of `polyglot-rust-c` or of a grader with two toolchains. Cite file:line for each hit.
For each hit, classify DUPLICATE (mechanism already present there) or NEW-MECHANISM, with two sentences. Name the fleet-first instrument if any, and the lane that would hold a shared standard. Absorb nothing; report only.""", ),
        item("ScribeR89", "scribe", f"""# Item ScribeR89 — draft prose for the round's knowledge entry (drafts only; the L1 applies them)
Write {W}/ScribeR89/knowledge-draft.md: a full draft of `corpus/knowledge/tb2-polyglot-rust-c-offline.md` in this order: `source:` (the S278 URL and the pinned commit), `verified-at:` (2026-11-05, commit {TIP}), `recheck:` (the exact command: `python3 plans/round89_c1_replay.py --lane . --rev HEAD --work <scratch>`); then a 40–70 line body that states: what the captured grader grades (one listing assertion at :19, two silent compiles at :24-25, five sizes under `subprocess.run(check=True)` at :27-44 and :30-44), the eight frozen vectors with their predicted values (read `plans/round89-cases.json` predicted fields and the receipt `corpus/evidence/round89/polyglot-rust-c-probe.txt`), the honest limit that the table gives three distinct vectors (P, F, E), and the E-versus-F distinction (CalledProcessError is outside the two graded refusals). Every number carries its command in the form `<number> — <command> <date>`. No credential material. No pipe characters inside table cells.
Also write {W}/ScribeR89/gate-note.md: the 25-word-max quote and the access date for S278, re-verified by you with `curl -sS -m 30 -o /dev/null -w '%{{http_code}} %{{size_download}}\\n' <url>` (record the output); do not re-fetch more than once.
Do not write anything under the lane except your own wave directory.""", ),
    ]
    return {
        "wave": "kengaku-r89-w1",
        "milestone": "R89 seventh executed TB2 member (polyglot-rust-c, located offline replay with a probe pin) and the Q66 v2 counter with a pinned record table and four control fixtures",
        "maxLanes": 16,
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
