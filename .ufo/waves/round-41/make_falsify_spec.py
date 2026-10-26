#!/usr/bin/env python3
"""Renders .ufo/waves/round-41/falsify-spec.json (wave 2 of 2, policy v1): attacks on what wave 1 and the L1 landed."""
import json
import pathlib
import subprocess
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-41"
B = f"{W}/build"
FX = f"{W}/falsify"
SCR = "/fast/scratch/hyaku/kengaku-r41"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
TIP = subprocess.run(["git", "-C", L, "rev-parse", "refs/heads/master"], capture_output=True, text=True,
                     check=True).stdout.strip()
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
CAP = f"{L}/corpus/evidence/round41/tb2-constraints-scheduling"
RCPT = f"{L}/corpus/evidence/round41/constraints-probe.txt"
DRY = f"{L}/corpus/evidence/round41/constraints-dry-cases-freeze.txt"
C1 = f"{L}/plans/round41_c1_verify.py"
C2 = f"{L}/plans/round41_c2_verify.py"
PROBE = f"{L}/plans/constraints_probe.py"
CLAIMS = f"{L}/plans/round-41-claims.md"
ENTRY = f"{L}/corpus/knowledge/tb2-constraints-scheduling-grader.md"
LES = f"{L}/corpus/lessons/round-41.md"
BAT = f"{L}/plans/battery41"
TOOLT = f"{L}/plans/tip_receipts.py"
TOOLS = f"{L}/plans/sources_adopt.py"
FREEZE = "8ef8b4fc7c6302c527db90244d69aa18f53e83bf"
FIRST = "f774a87ad071122acd39ba02a9901b5b56d9910a"
LAND = "74513c0625df7886357b866074104a0cf4bf9cc1"
MEAS = f"{W}/integrate/measure-final.txt"
BASE = f"{W}/integrate/measure-baseline.txt"

HOST_RULE = (
    "Every seat must run any battery, counter attack or fixture build that can write files inside a bwrap sandbox. In "
    "that sandbox `/home/vgpnk/.local/bin` is read-only (`--ro-bind`). Never write to a shared PATH directory, `/usr`, "
    "`/etc`, or `$HOME` outside scratch.\n\n"
    "Round 40's R40CritC1Counter planted a `git` shim in `~/.local/bin`, and it broke other lanes' git for minutes. The "
    "neutralized modules `crit_git_shim.py` and `crit_ledger_selfread.py` must stay neutralized.")
ENVELOPE = ("Envelope to use for every counter/battery/fixture run: `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin "
            "/home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>` (the C1 "
            "counter adds its own read-only sandboxes inside it; nesting works).")
CLONE = (f'Fixture rule: S={SCR}/<YourSeatName> — exactly your seat name; mkdir -p "$S"; trap \'rm -rf -- "$S"\' EXIT; '
         f'export TMPDIR="$S"; git clone -q --shared {L} "$S/lane"; verify `git -C "$S/lane" rev-parse --show-toplevel` equals '
         f'"$S/lane" before any write; every git call names -C "$S/lane"; never commit there. Any other fixture repo: '
         f'D=$(mktemp -d -p "$S") && git -C "$D" init -q, and every git call names -C "$D". Before ANY `rm -rf`, check the '
         f'target is "$S" or inside it (`case "$T" in "$S"|"$S"/*) ;; *) echo refuse; exit 1;; esac`): in wave 1 a seat '
         f'deleted the whole round root {SCR} and broke every running seat. Copy receipts into your report dir first.')

CONTEXT = f"""# Goal
kengaku round 41 (hyaku run 9, 2026-10-26), WAVE 2 of 2 (falsify). Lane repo: {L}, branch master, tip {TIP}.
Two claims are FROZEN at {CLAIMS} (freeze {FREEZE}; first recorded probe run {FIRST}); wave 1 landed at {LAND} and the
round's docs (lesson {LES}, SCORECARD.md `## Round 41`, LOG.md round-41 entry, `### Planned (round 42)`) at the tip.
Landing measurement {MEAS} (clean clone): C1 `BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=23
killed=23 survived=0 invalid=0 null_detected=0`, `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, `PREDICATE C1 pass`;
C2 `checks=8 defects=0`, `PREDICATE C2 pass`; baseline {BASE}. Your job: ATTACK what landed. Every item names its target;
report what holds and what breaks, with commands and outputs. Nothing frozen may change ({W}/claims/frozen-digests.txt).
- C1: 23 frozen mutants of {TOOLT} (T01-T13) and the {TOOLS} CLI (S01-S09, S11) in {C1}; standing battery {BAT}/ (7
  modules r_setup r_run r_ctl r_map s_usage s_modes s_exit, 48 fixtures, written by wave-1 executors). Known counter
  limits from wave 1 (the frozen counter is NOT edited; admission rests on non-author battery review): a probe stub can
  read the bound mutant variant from inside its sandbox and steer the verdict ({B}/R41CritC1Counter.md A1′, {B}/
  R41SentinelCounter.md F1); T03/T04 can then be credited on fixtures where the mutated line never runs (dead-site,
  R41CritC1Counter §3); relative argv tokens escape the fixture dir (F4/A3); AF_UNIX sockets and SysV IPC are not
  isolated (F2/F3); the sidechannel scan is source-text only (A8). A landed module that uses ANY of these vectors is a
  C1 admission failure — that is the key question for the battery reviewers.
- C2: TB2 `constraints-scheduling` @ {PIN}: entry {ENTRY} (with `## Corrections at integration (round 41, wave 1)`),
  rows S122/S123/S124 in {L}/corpus/SOURCES.md, README index row + coverage bullet + §Frontier sub-bullet, PROVINCE
  round-41 paragraph, SKILL `## Scheduling-constraint TB2 grader — round 41`; probe {PROBE}, receipt {RCPT} (25 cases,
  `cases=25 observed_pass=6 observed_fail=19 mismatches=2`), dry table {DRY}, captures {CAP}/, counter {C2} (V1-V8).
  Known: the frozen V1-V8 pass a content-free filler package ({B}/R41CritClaims.md §1), so the prose surfaces need
  non-author review.
- Wave-1 reports: {B}/*.md (38 seats). Frontier/rider: {L}/plans/routed_open.py + {L}/corpus/routed-findings.jsonl;
  QUALITY Q31/Q32 at the end of {L}/corpus/QUALITY.md; registry rows near {L}/SKILL.md:595-598 + `Round-41 registry
  addendum`.

# Host-safety rule (orchestrator, verbatim; binding for every seat that touches the C1 counter, and for all seats)
{HOST_RULE}
{ENVELOPE}

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report dir is {FX}/; drafts and receipts go under {FX}/<YourSeatName>/ (create it). Never copy a
  corpus/ or plans/ tree, a lane mirror, or a clone into {FX}/.
- Scratch (operator directive 2026-10-25): clones, fixtures and work trees live ONLY under {SCR}/<YourSeatName>/ (NVMe), never
  under /tmp; pass it explicitly (export TMPDIR, --work); delete ONLY your own dir before you finish.
- Write ONLY inside {FX}/ (your report + your own subdir) and your scratch dir. NEVER edit the lane's corpus/, plans/,
  SCORECARD.md, LOG.md, README.md, SKILL.md, PROVINCE.md, SHONEN.md or any other lane file — report for the L1, who
  integrates. Never write into {F} (fleet root), sibling lanes, the lane's jj state, or the lane's Git index. Never run git
  add/commit/stash/checkout/reset/push/pull or any mutating jj command in the lane. Seats never commit or push anywhere.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide:
  install via `uv tool` / `npx` / an official binary into ~/.local/bin (outside any bwrap run), or file nothing and say so. Never
  run pacman -Sy/-Syu/-U/-R, never name an already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat probe).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location and is <= 25
  words. Do not fabricate output; if something cannot be fetched or run, say so. Timestamp (date +%T) any write you make
  outside your report dir and scratch dir — there should be none.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""


def rev(name, role, module, mids):
    return (name, role, ["calibration", "discernment"],
            f"{HOST_RULE}\n\nNon-author honesty review of the landed battery module {BAT}/{module}.py (it claims kills of "
            f"{', '.join(mids)} of {C1}). For each fixture: (1) does it demonstrate the advertised behaviour its comment names, "
            f"or does it reach its verdict by any wave-1 counterexample vector (reading the counter's scratch root, `variants/` "
            f"or the slot file; /proc; relative `../` argv; sockets; IPC; reading tool or counter program text; a probe stub "
            f"that branches on anything but its own committed bytes)? Read every line, including the probe-stub strings it "
            f"writes. (2) Attribution: in your clone, inside the envelope, run `python3 {C1} --lane \"$S/lane\" --battery-dir "
            f"<dir holding only this module> --only {','.join(mids)} --work \"$S/w\"` and confirm each mutant dies by THIS "
            f"module; then, for each mutant, confirm the mutated line actually executes on its killing fixture (e.g. a copy of "
            f"the tool with a print/trace beside the changed line, run on the fixture you rebuilt in scratch). (3) Is each "
            f"fixture independent of the witness modules ({W}/claims/witness/)? Verdict per fixture: honest / incidental / "
            f"dishonest, with evidence.",
            f"VERDICT: battery41-{module}-honest-<h>/<n>-mutated-line-executed-<e>/{len(mids)}")


ITEMS = [
    rev("F41RevBatSetup", "reviewer", "r_setup", ["T01", "T02", "T05", "T07"]),
    rev("F41RevBatRun", "reviewer", "r_run", ["T03", "T04", "T13"]),
    rev("F41RevBatCtl", "reviewer", "r_ctl", ["T06", "T08"]),
    rev("F41RevBatMap", "reviewer", "r_map", ["T09", "T10", "T11", "T12"]),
    rev("F41RevBatSrcUsage", "critic", "s_usage", ["S02", "S03", "S05", "S06"]),
    rev("F41RevBatSrcModes", "critic", "s_modes", ["S01", "S04", "S08", "S09"]),
    rev("F41RevBatSrcExit", "critic", "s_exit", ["S07", "S11"]),
    ("F41C1Rerun", "executor", ["calibration", "operability"],
     f"{HOST_RULE}\n\nRe-measure C1 at the tip {TIP} on a clean `--no-local` clone, inside the envelope: run `python3 {C1} "
     f"--lane \"$S/lane\" --work \"$S/w1\"` twice (PYTHONHASHSEED=1 and 99; `--jobs 1` and `--jobs 8`) and byte-compare the "
     f"outputs with each other and with {MEAS}'s C1 block. Then remove each of the 7 modules in turn and record which mutants "
     f"flip to SURVIVED (load-bearing table); report any module that kills nothing alone.",
     "VERDICT: c1-rerun-byte-equal-<yes|no>-load-bearing-<k>/7"),
    ("F41C1Attribution", "executor", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nAttribution re-run (wave-1 dead-site finding): for each of the 23 frozen mutants, find its killing "
     f"fixture in the landed battery ({MEAS} `killed by=` ids) and show whether the MUTATED line executes in the mutant run "
     f"on that fixture. Method: in scratch, build a traced copy of each tool variant (insert `sys.stderr.write('HIT <id>\\n')` "
     f"immediately before the mutated statement, same semantics) and run it on that fixture's built tree with the fixture's "
     f"argv (a counter COPY in your scratch may be modified to keep fixture dirs and print stderr; never the lane file). "
     f"Table: mutant, killer, mutated-line-executed yes/no, evidence. Any `no` is a non-attributable kill.",
     "VERDICT: attributable-<k>/23"),
    ("F41C1Hardened", "executor", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nHardened re-measure: copy {C1} into your scratch and repair the wave-1 limits WITHOUT touching its "
     f"mutant list, predicate or directions: (a) the variant and slots dir not readable from a tool run (bind the variant with "
     f"`--ro-bind-data` or hide `root/variants` and `root/slots` behind the bind), (b) `--unshare-ipc`, (c) `--tmpfs /run`, "
     f"(d) `path_ok` resolving relative tokens against d, (e) streaming fingerprint. Show each repair bites (one small hostile "
     f"module per repair, red under the copy, green under the frozen counter). Then run the LANDED battery {BAT} under the "
     f"hardened copy: does it still print `MUTANTS total=23 killed=23` and `PREDICATE C1 pass`? Paste diff and outputs.",
     "VERDICT: hardened-copy-battery-killed-<k>/23-repairs-biting-<r>/5"),
    ("F41MutBattery", "mutation-tester", ["calibration"],
     f"{HOST_RULE}\n\nFixture-level mutants of the landed battery {BAT}: for each fixture, one mutant that breaks what it "
     f"demonstrates (wrong `defects` set, wrong `expect`, the trigger input removed, the probe stub's bytes changed) in a "
     f"scratch copy; run the counter (`--battery-dir`) and record whether the counter flags it (`WRONG` line, a mutant "
     f"flipping to SURVIVED, or SETUP). Table: fixture, mutant, caught-by, survived.",
     "VERDICT: fixture-mutants-caught-<k>/<n>"),
    ("F41XMutReceipts", "mutation-tester", ["calibration", "operability"],
     f"{HOST_RULE}\n\nGeneralisation probe: near-variant mutants of {TOOLT} OUTSIDE the frozen list (other guards, the "
     f"`kind` branches, `first_diff`, `tamper_one_byte`, the auto-control choice `min(equal, ...)`, `--only` filtering, "
     f"`usage_argv` parsing) — 12-20 single-line mutants run against the landed battery through a counter copy whose MUTANTS "
     f"list you replace in scratch. How many does battery41 kill? Which advertised sentence does each survivor break? These "
     f"are round-42 candidates, not this round's claim.",
     "VERDICT: near-variants-killed-<k>/<n>"),
    ("F41XMutSources", "mutation-tester", ["calibration", "operability"],
     f"{HOST_RULE}\n\nSame as a near-variant probe for the {TOOLS} CLI (`main()` and the exit-code returns of `check()` / "
     f"`quote_check()` not in the frozen list: S10's neighbours, `--attest-opened`, `--scope-to-admit`, `--out` writing, "
     f"EXIT_QUOTE_TOO_LONG/ABSENT/URL_MISMATCH precedence): 12-20 mutants through a counter copy in scratch against the "
     f"landed battery. Kill count; advertised sentence per survivor.",
     "VERDICT: near-variants-killed-<k>/<n>"),
    ("F41CritC1Count", "critic", ["calibration", "discernment"],
     f"Recount the C1 calibration denominator: list every behaviour {TOOLT}'s docstring and the `sources-adopt` registry row "
     f"(SKILL.md near :573) advertise (wave-1 {B}/R41CritEquiv.md found 30 advertised behaviours without a mutant — "
     f"confirm or correct with file:line), which of them the 23 frozen mutants cover, and whether `ADVERTISED direct=21 "
     f"indirect=2 none=0` holds. Also judge the SCORECARD round-41 erratum on the C1 wording (\"no `plans/battery41` "
     f"fixture\").",
     "VERDICT: advertised-<a>-covered-<c>-direct-<d>-indirect-<i>"),
    ("F41SentinelBattery", "sentinel", ["safety"],
     f"{HOST_RULE}\n\nSecurity scan of the landed battery {BAT}/*.py and of the probe stubs and registry files it writes: any "
     f"host write, network or socket use, process persistence, IPC, symlink tricks, or reads outside its fixture dir? "
     f"Re-run the full counter once inside the envelope and confirm no file appears outside your scratch "
     f"(`find /home/vgpnk -newer <stamp> -not -path '*/.cache/*'` limited sensibly; `ipcs` before/after). Findings with "
     f"severity.",
     "VERDICT: battery-security-findings-<n>"),
    ("F41C2Rerun", "executor", ["coverage", "freshness"],
     f"Re-measure C2 at the tip {TIP} on a clean clone: `python3 {C2} --lane \"$S/lane\" --work \"$S/absent/w\"` twice; the "
     f"probe `python3 {PROBE} --lane \"$S/lane\" --work \"$S/p\"` three times (one under `env -i PATH=/usr/bin:/bin`) "
     f"byte-compared with {RCPT}; `--dry` byte-compared with {DRY}. Paste outputs.",
     "VERDICT: c2-pass-<yes|no>-probe-byte-equal-<k>/3"),
    ("F41ReopenRows", "reviewer", ["freshness", "discernment"],
     f"Re-open S122, S123 and S124 ({L}/corpus/SOURCES.md) live: fetch both raw URLs at the pin and `cmp` with the captures; "
     f"open TB2.1 PR #245 via `gh api` (state, merged, closed_at); check each row's quote is verbatim at its stated location "
     f"and <=25 words, the anchor digest equals the capture, tier/status/opened/recheck/used-by are right, and "
     f"{L}/corpus/evidence/round41/pr245-body.md is what the PR body says. Run the census on the lane. Per-row verdict.",
     "VERDICT: rows-ok-<k>/3"),
    ("F41EntryQuotes", "critic", ["depth", "discernment"],
     f"Sentence-level support check of {ENTRY}: for every factual sentence in §Summary, §What is graded, §Findings and "
     f"§Corrections, find the receipt line ({RCPT}), capture line ({CAP}/) or wave report that supports it; list "
     f"unsupported or wrong sentences with the smallest correction. Verify the `## Located quotes` rows are verbatim "
     f"(quote, capture:line).",
     "VERDICT: entry-unsupported-<u>-wrong-<w>"),
    ("F41CritOverclaim", "critic", ["discernment"],
     f"Overclaim hunt across the round-41 C2 prose: {ENTRY}, the README row/bullet/§Frontier sub-bullet ({L}/corpus/README.md, "
     f"grep constraints-scheduling), PROVINCE round-41 paragraph, SKILL `## Scheduling-constraint TB2 grader — round 41`, "
     f"LOG/SCORECARD round-41 text. Universal words, 'class new', 'unpublished', 'computed not asserted', numbers — each "
     f"overclaim with location and the receipt fact that bounds it.",
     "VERDICT: overclaims-<n>"),
    ("F41MapControl", "mutation-tester", ["coverage", "calibration"],
     f"Red controls for C2's V7/V4 on the landed entry: in a scratch clone, mutate the entry's `## Requirement map` (wrong "
     f"label, a cited non-violating case, a missing tag, a wrong line) and the mismatch naming (drop one `match=NO` id), and "
     f"run {C2}; each must go red. Also: does V3 go red on a wrong anchor digest? Table with outputs.",
     "VERDICT: map-controls-red-<k>/<n>"),
    ("F41IndepProbe", "critic", ["coverage"],
     f"Independent re-run of the non-frozen end states the entry's §Corrections cites from wave-1 R41CritProbe "
     f"(`crlf-folded`, `crlf-lowercase-summary`, `crlf-value-datetime`, `lowercase-attendee-only`, `input-cr-only`): build "
     f"each yourself (a scratch COPY of the probe with extra cases), grade, and compare with the claimed verdicts.",
     "VERDICT: indep-agree-<k>/5"),
    ("F41CritPriorArt", "critic", ["novelty"],
     f"Widen the prior-art search for the two C2 observations wave 1 found unpublished ({B}/R41ScoutPriorArt.md rows 2 and 3): "
     f"(a) the earliest test passing an invalid earlier slot; (b) the input-integrity check being blind to newline "
     f"rewrites (decoded-text comparison). Search TB2/TB2.1 issues and PRs, harbor-framework repos, TB2 audits, papers on "
     f"benchmark grader audits (arXiv), blog posts. Published (URL + quote + access time) / not found (queries). This prices "
     f"a round-42 novelty claim; nothing is claimed now.",
     "VERDICT: unpublished-<k>/2"),
    ("F41CritSkill", "critic", ["depth", "operability"],
     f"Verify every row of {L}/SKILL.md `## Scheduling-constraint TB2 grader — round 41` decision table and its 'what a green "
     f"means' paragraph against the receipt and capture lines it cites; and run every command in the four new registry rows "
     f"(SKILL.md:595-598) and the Round-41 registry addendum in a clean clone (C1 only inside the envelope): does each "
     f"verdict map match?",
     "VERDICT: skill-rows-verified-<k>/<n>-registry-<r>/4"),
    ("F41RevRider", "reviewer", ["operability", "discernment"],
     f"Review the rider {L}/plans/routed_open.py and {L}/corpus/routed-findings.jsonl: run `--observe` and `--selftest`; is "
     f"each row's status honest at the tip (closing evidence real, check commands meaningful, R40-R1 'open' and R40-R3 "
     f"'closed' right)? Which routed items from {L}/corpus/lessons/round-39-verifier-spotcheck.md and round-40 §5 are missing? "
     f"Can the file be gamed (a closed row with a vacuous check)?",
     "VERDICT: rider-rows-honest-<k>/<n>"),
    ("F41RevQuality", "reviewer", ["discernment"],
     f"Review QUALITY Q31 and Q32 (end of {L}/corpus/QUALITY.md): is every cited line/receipt accurate at the tip, is each "
     f"'Check' executable as written (run it), is each 'Shown able to fail' leg actually red? Smallest corrections.",
     "VERDICT: quality-defects-<n>"),
    ("F41RevLesson", "reviewer", ["discernment"],
     f"Review {LES}: each `## Mistakes` row (class, evidence pointer resolvable, captured-by honest, fix shown able to fail or "
     f"honestly not), each `## Gate` admit/reject (re-open at least S124 and the refused PR test file), the `## Routed` "
     f"dispositions against the tip, the census numbers. List defects.",
     "VERDICT: lesson-defects-<n>"),
    ("F41CritScorecard", "critic", ["calibration", "discernment"],
     f"Attack {L}/SCORECARD.md `## Round 41` (and its capability rows) and the LOG.md round-41 entry: every number against "
     f"{MEAS}, {RCPT}, wave reports; is 'held' honest for each axis; do the three capability rows each have a passing "
     f"demonstration (run their commands)? Smallest corrections (they will be appended as errata).",
     "VERDICT: scorecard-defects-<n>"),
    ("F41CritNoHarmDiff", "critic", ["calibration"],
     f"No-harm diff: `git -C <clone> diff e50c134556b4ba48e29dc7ff364e90d6ef07a3f3 {TIP} --stat` and every REMOVED line in "
     f"lane files outside .ufo/waves — list them; does any removal or rewrite harm an earlier round's text, registry row or "
     f"instrument? Compare {BASE} and {MEAS} verdict lines.",
     "VERDICT: removed-lines-<n>-harm-<h>"),
    ("F41NoHarm", "executor", ["operability", "freshness"],
     f"{HOST_RULE}\n\nRe-run the landing measurement script {W}/integrate/measure.sh yourself against the tip (it clones into "
     f"its own scratch under {SCR}/L1/measure — instead copy it to your scratch and point its S at {SCR}/F41NoHarm/measure) "
     f"inside the envelope, and compare every verdict line with {MEAS}. Report any drift.",
     "VERDICT: no-harm-verdicts-equal-<k>/<n>"),
    ("F41ScoutMisroot", "scout", ["safety", "hygiene"],
     f"Host-safety and hygiene watch for wave 2: `ls -la --time-style=full-iso /home/vgpnk/.local/bin` + dir mtime at start "
     f"and end; `git -C {F} status --porcelain --untracked-files=all` (any kengaku round-41 file in the fleet root?); scratch "
     f"dirs under {SCR} with sizes; any /tmp path a kengaku r41 seat created; `ipcs` residue; the wave-1 round-root deletion "
     f"(15:42:24) — any recurrence? Report only; touch nothing.",
     "VERDICT: misroot-<n>-host-writes-<h>"),
    ("F41ConnClaims", "connector", ["calibration"],
     f"Cross-document drift: every number and hash across {CLAIMS}, the counters' docstrings, {W}/claims/*, {MEAS}, "
     f"SCORECARD/LOG round-41 text, {LES}, the entry and README rows — 23/13/10, 21/2, 48 fixtures, 25/6/19/2, 114→117, "
     f"47→48, freeze/first/landing hashes. Every disagreement with both locations.",
     "VERDICT: drift-<n>"),
    ("F41ConnFrontier", "connector", ["coverage", "calibration"],
     f"After landing: does any self-assessment line in {L}/SCORECARD.md, {L}/SHONEN.md, {L}/corpus/README.md (coverage map, "
     f"§Frontier, open gaps) or {L}/PROVINCE.md now mismatch the repo state (count them, file:line)? Is the '7 of 89' and "
     f"'class new to the lane' wording right against the six earlier TB2 entries?",
     "VERDICT: mismatches-<n>"),
    ("F41CritSeparability", "critic", ["calibration", "coverage"],
     f"{HOST_RULE}\n\nSeparability at the tip: in one clean clone delete C2's work product (entry, S122-S124, README/PROVINCE/"
     f"SKILL round-41 C2 text, receipt) and run {C1}; in another delete {BAT} and run {C2}. Each must still pass. Paste "
     f"outputs.",
     "VERDICT: separable-<both|c1-only|c2-only|neither>"),
    ("F41CritPlanNext", "critic", ["calibration", "discernment"],
     f"Attack {L}/SCORECARD.md `### Planned (round 42)`: can a do-nothing control reach any candidate's predicate as "
     f"drafted? Is each candidate on the right axis with a stated reason (lowest non-retired axis rule, the L0 cap)? Are the "
     f"routed items ({L}/corpus/routed-findings.jsonl rows with status open/blocked) each owned? Measure what you can.",
     "VERDICT: plan42-defects-<n>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 41 wave 2 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {FX}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r41 wave 2 (falsify)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    spec = {"wave": "kengaku-r41-falsify",
            "milestone": "kengaku round 41 wave 2: falsify battery41, the C2 package, the rider and the round's docs",
            "reportDir": ".ufo/waves/round-41/falsify", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/falsify-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c))
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"] + c["sentinel"]
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)} tip={TIP}")


main()
