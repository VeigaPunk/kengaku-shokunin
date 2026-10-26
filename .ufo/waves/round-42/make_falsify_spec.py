#!/usr/bin/env python3
"""Renders .ufo/waves/round-42/falsify-spec.json (wave 2 of 2, policy v1). L1 KengakuR42."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-42"
B = f"{W}/build"
FX = f"{W}/falsify"
SCR = "/fast/scratch/hyaku/kengaku-r42"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
CAP = f"{L}/corpus/evidence/round42/tb2-circuit-fibsqrt"
RCPT = f"{L}/corpus/evidence/round42/fibsqrt-probe.txt"
DRY = f"{L}/corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt"
C1 = f"{L}/plans/round42_c1_verify.py"
C2 = f"{L}/plans/round42_c2_verify.py"
PROBE = f"{L}/plans/fibsqrt_probe.py"
CLAIMS = f"{L}/plans/round-42-claims.md"
ENTRY = f"{L}/corpus/knowledge/tb2-circuit-fibsqrt-grader.md"
BAT = f"{L}/plans/battery42"
ANC = f"{L}/plans/anchor_digest_check.py"
ORD = f"{L}/plans/order_check.py"
LESSON = f"{L}/corpus/lessons/round-42.md"
FREEZE = "bc856d803576e182b6c3c12afc6b23f392071c25"
FIRST = "523b27806be0df26d2235089d845265a29f8cedf"
LAND = "ff14d76d32d662f7b7073a2acb049594cb740d84"
DOCS = "508434ad55c709337065611691c426f05875492d"

HOST_RULE = (
    "Every seat must run any battery, counter attack or fixture build that can write files inside a bwrap sandbox in which "
    "`/home/vgpnk/.local/bin` is read-only (`--ro-bind`). Never write to a shared PATH directory, `/usr`, `/etc`, or `$HOME` "
    "outside scratch. (Round 40: a seat planted a `git` shim in `~/.local/bin` and broke other lanes' git for minutes.)")
ENVELOPE = ("Envelope for every counter/battery/fixture run: `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin "
            "/home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>` (the C1 "
            "counter adds its own read-only sandboxes inside; nesting works). Your receipt carries that envelope line, `date +%T` "
            "before and after, and `ls -A /home/vgpnk/.local/bin | sha256sum` before and after (QUALITY Q32). Do NOT make "
            "/home/vgpnk read-only as a whole: the C2 gate's P10 runs `uv`, which needs a writable cache (round-42 L1 mistake).")
SCRATCH = (f"Scratch rule (round-41 closure R2): S={SCR}/<YourSeatName>; mkdir -p \"$S\"; trap 'rm -rf -- \"$S\"' EXIT; export "
           f"TMPDIR=\"$S\". Delete ONLY inside your own \"$S\" (`python3 {L}/plans/scratch_guard.py safe-rm {SCR} <YourSeatName> "
           f"<path>` refuses anything else); never delete {SCR} itself, its `.ROUND-ROOT-SENTINEL`, or another seat's dir. Never use "
           f"/tmp for anything over 50 MB.")
CLONE = (f'Clone rule: git clone -q --no-local {L} "$S/lane" && git -C "$S/lane" checkout -q {DOCS}; verify `git -C "$S/lane" '
         f'rev-parse --show-toplevel` equals "$S/lane" before any write; every git call names -C "$S/lane"; never commit there. '
         f'Any other fixture repo: D=$(mktemp -d -p "$S") && git -C "$D" init -q, and every git call names -C "$D".')

CONTEXT = f"""# Goal
kengaku round 42 (hyaku run 9, 2026-10-26), WAVE 2 of 2 (FALSIFY). Lane repo: {L}. Attack what wave 1 and the L1 landed.
Frozen claims {CLAIMS} (freeze {FREEZE}; first probe run {FIRST}); landing {LAND}; docs {DOCS} (lane tip when this wave was
cut). Wave-1 reports: {B}/*.md. Landing measurement: {W}/integrate/measure-final.txt (clean clone of {LAND}): C1 `BATTERY
fixtures=29 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`,
`MUTANTS-BY-TOOL anchor=9/9 order=5/5`, `PREDICATE C1 pass`; C2 `checks=9 defects=0`, `PREDICATE C2 pass`; probe re-run
byte-equal; no-harm diff vs {W}/integrate/measure-baseline.txt shows only the expected changes.
- C1 (calibration): {C1} over {ANC} and {ORD}, 14 near-variant mutants, battery {BAT}/ (5 modules, 29 fixtures). A kill counts
  only when ATTRIBUTED (traced re-run reproduces the result and executes a line of the replaced span). Known wave-1 limits:
  `R42CritC1Counter` reached the predicate with three substitute fixtures (XO1 receipt-is-directory, XO3 emptied-directory, X13
  staged-manifest); `R42CritAttribution`: the span check is vacuous for 8/14 (lines that run on every invocation);
  `R42SentinelCounter` V1 HIGH: `log.showSignature`+`gpg.program` in a fixture `.git/config` runs a program in the order tool's
  run (contradicting the frozen sentence "these two tools run no fixture code"); V2 builder copy readable; V3 hidden lane is a
  writable tmpfs; `R42CritC1Counter` V1b `core.worktree` redirect; `R42MutC1Counter` counter guards caught 7/22 by controls;
  `R42RevMutRows` 12/14 adv cells verbatim. The frozen counter is NOT edited this round; admission of C1 rests on the counter
  AND a non-author review that battery42 demonstrates the advertised behaviours honestly.
- C2 (coverage): pinned TB2 `circuit-fibsqrt` grader, entry {ENTRY}, rows S125 S126 S127 (tier A) + S128 (OpenAgents issue #9645,
  tier B), captures {CAP}/, receipt {RCPT} (`cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0`),
  dry table {DRY}, counter {C2} (V1-V8 + V9 content). Wave-1 limits: `R42CritProbe` D1-D5 (mechanism correction folded into the
  entry), `R42CritClaims`: an informed filler passes 7/9; prior art 2/6 (`R42ScoutPriorArt`); Harbor verifier cwd = /app
  (`R42ScoutHarborCwd`); pytest parity 16/16; independent re-derivation 16/16 + 3.
- Landed surfaces to attack: {L}/corpus/SOURCES.md rows S125-S128; {L}/corpus/README.md (index row, coverage bullet, §Frontier
  round-42 sub-bullet "8 of 89"); {L}/PROVINCE.md §Round42; {L}/SKILL.md registry rows round42-c1-mutants/round42-c2/fibsqrt-probe,
  the round-42 addendum and §Simulator-executed data-artefact TB2 grader — round 42; {L}/corpus/QUALITY.md Q33/Q34;
  {LESSON}; {L}/SCORECARD.md §Round 42; {L}/LOG.md §Round 42; {L}/corpus/routed-findings.jsonl (+6 rows);
  {L}/plans/round_close.py (R5 re-run fix); {L}/plans/scratch_guard.py (R2).

# Host-safety rule (orchestrator; binding for every seat)
{HOST_RULE}
{ENVELOPE}

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report dir is {FX}/; drafts and receipts go under {FX}/<YourSeatName>/ (create it). Never copy a corpus/
  or plans/ tree, a lane mirror, or a clone into {FX}/; no receipt file over 1 MiB (quote it, give its sha256, delete it).
- {SCRATCH}
- Write ONLY inside {FX}/ (your report + your own subdir) and your scratch dir. NEVER edit any lane file — findings and drafts
  for the L1, who integrates. Never write into {F} (fleet root), sibling lanes, the lane's jj state, or the lane's Git index.
  Never run git add/commit/stash/checkout/reset/push/pull or any mutating jj command in the lane. Seats never commit or push.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY: never write/commit/fetch there; run none of its campaign tools.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide:
  install via `uv tool` / `npx` / an official binary into ~/.local/bin (outside any bwrap run), or install nothing and say so. Never
  run pacman -Sy/-Syu/-U/-R, never name an already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat probe).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location (file:line or
  URL+section) and is <= 25 words. Do not fabricate output; if something cannot be fetched or run, say so. Name what you attack.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""


def rev_bat(module, mids):
    return (f"F42RevBat{module.replace('_', '').capitalize()}", "reviewer", ["calibration", "discernment"],
            f"{HOST_RULE}\n\nNon-author honesty review of {BAT}/{module}.py (it kills {', '.join(mids)} in the landing run). For "
            f"EACH fixture: does it build the shape the advertised sentence of the mutant it kills describes (read the mutant's `adv` "
            f"cell and `old -> new` in {C1}), or is it a substitute that reaches the declared direction another way (wave-1 "
            f"`R42CritC1Counter` §1 shows three substitute shapes: a receipt that is a directory, an emptied directory, a staged "
            f"manifest only)? Does it read, import or copy {W}/claims/witness/ (compare structure with w_anchor.py / w_order.py — "
            f"a renamed copy is a defect)? Any repo-local git config, symlink, `core.worktree`, gpg/signature trick? Run the "
            f"counter in your clone inside the envelope with `--battery-dir <dir holding only this module> --only "
            f"{','.join(mids)}` and paste the MUTANT lines. Table: fixture, mutant(s) killed, honest/substitute/incidental, reason.",
            f"VERDICT: battery42-{module}-honest-<h>/<n>-substitute-<s>")


ITEMS = [
    # ---- C1 attacks ----
    ("F42C1Rerun", "executor", ["calibration", "operability"],
     f"{HOST_RULE}\n\nRe-measure C1 at {DOCS} on a clean clone inside the envelope: `python3 {C1} --lane \"$S/lane\" --work "
     f"\"$S/w\"` twice with `PYTHONHASHSEED=1 --jobs 1` and `PYTHONHASHSEED=99 --jobs 8`; diff the MUTANT/BATTERY/summary lines "
     f"(byte-equal?) and against {W}/integrate/measure-final.txt. Then remove each battery42 module in turn (copy the lane to "
     f"scratch) and record which mutants flip — every module load-bearing?",
     "VERDICT: c1-rerun-<equal|differ>-modules-loadbearing-<k>/5"),
    rev_bat("a_route", ["X1", "X3", "X12"]),
    rev_bat("a_class", ["X6", "X7", "X14"]),
    rev_bat("a_row", ["X9", "X13", "X15"]),
    rev_bat("o_clause", ["XO1", "XO3"]),
    rev_bat("o_scan", ["XO5", "XO6", "XO7"]),
    ("F42C1StrongAttrib", "critic", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nStronger attribution for the 8 mutants whose span check is vacuous (`R42CritAttribution`): for each of "
     f"X13, XO1, XO3, XO5, XO6, XO7 and the other two it names, show on the battery42 KILLING fixture (the `killed by=` id in "
     f"{W}/integrate/measure-final.txt) that the mutated expression evaluates differently between reference and mutant (e.g. "
     f"instrument a COPY of the tool in scratch to log the regex match / condition value / argparse default at that site). A kill "
     f"whose site value does not differ is not attributable to the mutation. Table: mutant, fixture, site value ref vs mut.",
     "VERDICT: strong-attribution-<k>/8"),
    ("F42GpgVector", "critic", ["calibration", "safety"],
     f"{HOST_RULE}\n\nAdjudicate the conflict between `R42SentinelCounter` V1 (a fixture `.git/config` with `log.showSignature=true` "
     f"+ `gpg.program=<exe>` runs that program inside `order_check.py`'s `git log`) and `R42CritC1Counter` V1 (\"a fake gpgsig "
     f"commit … left GPG-LOG-RC 0\"). Reproduce both in scratch under {C1}'s exact `Runner.env` and `ro_sandbox`; can the program "
     f"observe which variant is running, and can it change a verdict in any of the 14 declared directions? Then draft the "
     f"smallest counter remediation (GIT_CONFIG_* pins) and show it blocks the vector — draft only, in your dir.",
     "VERDICT: gpg-vector-<real|not-real>-verdict-change-<possible|impossible>"),
    ("F42C1Hardened", "executor", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nWrite a hardened COPY of {C1} in {FX}/F42C1Hardened/ carrying the wave-1 remediations: pin gpg.program/"
     f"log.showSignature (R42SentinelCounter V1), hide `root/bin` from builds (V2), make the lane hide read-only (V3), reject a "
     f"fixture repo whose `rev-parse --show-toplevel` or `core.worktree` leaves d (R42CritC1Counter V1b). For each repair write one "
     f"hostile module that is green on the frozen counter and red on the copy. Then run landed battery42 through the copy: still "
     f"`killed=14`? Paste the matrix. Mutant list, predicate and floors untouched (segment-compare with the frozen file).",
     "VERDICT: hardened-copy-battery42-<k>/14-repairs-biting-<r>/4"),
    ("F42MutBattery", "mutation-tester", ["calibration"],
     f"{HOST_RULE}\n\nFixture-level mutation of battery42: for each of the 29 fixtures, a single-edit mutant of its build (drop a "
     f"commit, change one byte of a capture, flip expect) — does the counter notice (`wrong`, a mutant flips to SURVIVED)? Which "
     f"fixtures are redundant (removing them changes nothing)? Table with the counter lines.",
     "VERDICT: fixture-mutants-caught-<k>/<n>-redundant-<r>"),
    ("F42XMutNear", "mutation-tester", ["calibration", "coverage"],
     f"{HOST_RULE}\n\nNear-variants OUTSIDE the frozen 14 over {ANC} and {ORD} (>=20, single replacements in the same branches: "
     f"alternate comparisons, dropped routes, widened regexes) run through a COPY of {C1} with MUTANTS swapped (dev mode) against "
     f"battery40+battery42 together? (battery40 needs a lane clone: run battery42 alone and say so.) Kill rate; survivors with a "
     f"one-line witness each — round-43 candidates.",
     "VERDICT: near-variants-killed-<k>/<n>"),
    ("F42CritAdv", "critic", ["calibration", "discernment"],
     f"Adjudicate `R42RevMutRows`' two misquoted `adv` cells and the XO5/XO6 relabel: quote each cited docstring line verbatim "
     f"({ANC}, {ORD} at {DOCS}), say whether the frozen cell misquotes, misattributes or merely paraphrases, and draft the "
     f"erratum sentence for {LESSON} (no frozen file edited). Is `indirect` right for XO6 and wrong for any other?",
     "VERDICT: adv-errata-<n>"),
    ("F42CritSeparability", "critic", ["calibration", "coverage"],
     f"{HOST_RULE}\n\nSeparability: in two scratch mirrors of {DOCS} — one with C2's work removed (entry, S125-S128 rows, README/"
     f"PROVINCE/SKILL round-42 text, receipt) and one with C1's work removed (plans/battery42) — run the OTHER claim's counter: does "
     f"each pass with the other's work absent? Paste outputs. Any shared file whose change could move both?",
     "VERDICT: separable-<yes|no>"),
    # ---- C2 attacks ----
    ("F42C2Rerun", "executor", ["coverage", "freshness"],
     f"Re-measure C2 at {DOCS} on a clean clone: `python3 {C2} --lane \"$S/lane\" --work \"$S/w\"` (paste every V line and the gate "
     f"lines); then the probe three times — plain, `env -i PATH=/usr/bin:/bin`, and with `--work` on a fresh dir — each `cmp` with "
     f"{RCPT}. Byte-equal 3/3?",
     "VERDICT: c2-rerun-<pass|fail>-probe-byte-equal-<k>/3"),
    ("F42EntryQuotes", "reviewer", ["coverage", "depth"],
     f"Check every row of {ENTRY} `## Located quotes`: verbatim at the cited capture line in {CAP}/ (count words, 3-25)? Check the "
     f"`## Requirement map` labels against the receipt (derive yourself) and the `## Case table` against {RCPT} row by row. Then "
     f"read the Findings and the appended `## Wave-1 integration` section: list every sentence the receipt or the captures do not "
     f"support (wrong / unsupported / overclaim), with the line.",
     "VERDICT: entry-quotes-ok-<k>/<n>-bad-sentences-<b>"),
    ("F42ReopenRows", "scout", ["freshness", "coverage"],
     f"Re-open S125, S126, S127 (raw URLs in {L}/corpus/SOURCES.md, `cmp` with {CAP}/) and S128 "
     f"(https://github.com/OpenAgentsInc/openagents/issues/9645 via `gh api`) live now: access time, the anchor quote located at the "
     f"cited place, state words (closed, closed_at). Any cell wrong? Draft corrections as NEW `supersedes S12N —` rows only (CORPUS "
     f"rule 2; Q34), never in place.",
     "VERDICT: rows-reopened-4-wrong-cells-<w>"),
    ("F42CritOverclaim", "critic", ["coverage", "discernment"],
     f"Overclaim hunt across the round-42 C2 prose: {L}/corpus/README.md (index row, coverage bullet, §Frontier round-42 sub-bullet), "
     f"{L}/PROVINCE.md §Round42, {L}/SKILL.md §Simulator-executed data-artefact TB2 grader — round 42 and the round-42 addendum, "
     f"{L}/SCORECARD.md §Round 42, {L}/LOG.md §Round 42. Every number against {RCPT} / {W}/integrate/measure-final.txt; every "
     f"mechanism against {CAP}/sim.c and test_outputs.py; every 'new class'/'first' against the seven earlier TB2 entries. List "
     f"wrong / unsupported / overclaim with file:line.",
     "VERDICT: overclaims-<o>-wrong-<w>"),
    ("F42CritV9", "critic", ["coverage", "calibration"],
     f"Attack V9 of {C2}: build (a) an informed filler that copies the receipt into a `## Case table` and adds the PROVINCE/README "
     f"lines but no analysis, (b) a case table whose letters disagree with the receipt in one row, (c) a case table in the wrong "
     f"order, (d) row ids only inside a code fence. Which pass V9 (call `v9()` on scratch mirrors)? Say plainly what V9 certifies "
     f"and what it cannot see; draft one more V9-style check that would separate (a) from the landed entry, with a control.",
     "VERDICT: v9-admits-<k>/4"),
    ("F42MutC2V9", "mutation-tester", ["coverage", "soundness"],
     f"Mutation-test V9 of {C2} only (single-line mutants of CASE_ROW, the receipt regex, the equality, the `source:` exclusion, the "
     f"PROVINCE and README checks), each against {W}/claims/c2_filler_control.py reproduced in your clone and against the landed "
     f"tip. Table: mutant, caught-by, survived; a control per survivor (draft).",
     "VERDICT: v9-mutants-caught-<k>/<n>"),
    ("F42CritCwd", "critic", ["coverage", "freshness"],
     f"Verify `R42ScoutHarborCwd` ({B}/R42ScoutHarborCwd.md): re-read the cited Harbor source at its pin(s) and confirm the verifier "
     f"runs test.sh with cwd /app; reproduce the claim 'under any other writable cwd nine of sixteen verdicts move' with a COPY of "
     f"{PROBE} in scratch (cwd parameterised). Which nine? Is the entry's cwd sentence right?",
     "VERDICT: cwd-claim-<confirmed|refuted>-moved-<k>/16"),
    ("F42CompilerSens", "executor", ["coverage", "freshness"],
     f"Compiler sensitivity of the receipt: the grader compiles sim.c with host gcc 16 `-O3`; the image uses Debian bookworm gcc. "
     f"In scratch, compile {CAP}/sim.c with `-O0`, `-O2`, `-O3` (and clang if installed) and run each binary on the 28 graded inputs "
     f"plus 208/20000 for the oracle circuit, the lookup circuit and the trailing-space circuit (generate them with a COPY of the "
     f"probe's `lookup()`/solve.sh). Do outputs differ by flag/compiler (UB in sim.c: uninitialised gates, out-of-range indices)?",
     "VERDICT: compiler-sensitive-<yes|no>"),
    ("F42CritPriorArt", "scout", ["novelty", "discernment"],
     f"Widen `R42ScoutPriorArt`'s search for the lookup construct and the parse/ordering/cwd/whitespace mechanics of circuit-fibsqrt: "
     f"web search, arXiv (TB2 audits, benchmark-gaming papers), HF dataset discussions, agent trajectory dumps that mention gates.txt "
     f"lookup tables. For each finding: published (URL, <=25-word quote, access time) or not found (queries). Does S128 say what the "
     f"entry says it says?",
     "VERDICT: prior-art-wider-published-<p>/6"),
    ("F42RevC2Package", "reviewer", ["coverage", "operability"],
     f"Review the C2 package as a whole at {DOCS}: README index row cites S125-S128 and the receipt; coverage bullet; §Frontier "
     f"'8 of 89'; PROVINCE line carries both `circuit-fibsqrt` and the entry name on one line; SKILL rows match what the commands "
     f"print (run `--dry`, `--stage-check`, the counter); census `validate --root` exit 0. List defects with file:line.",
     "VERDICT: c2-package-defects-<n>"),
    # ---- frontier / docs ----
    ("F42RevLesson", "reviewer", ["discernment"],
     f"Review {LESSON}: each `## Mistakes` row has class, evidence pointer (resolve it), captured-by, and a fix shown able to fail "
     f"(name the receipt that shows it failing)? `## Gate` has >=1 admit and >=1 reject with reason + flip? Routed dispositions "
     f"true at {DOCS}? List defects.",
     "VERDICT: lesson-defects-<n>"),
    ("F42RevQuality", "reviewer", ["discernment", "calibration"],
     f"Review {L}/corpus/QUALITY.md Q33 and Q34 (appended this round): is each criterion checkable, does each cite real evidence, can "
     f"each fail (run the seat scripts in {B}/R42QualityDraft/ on a clone and on a mutated copy)? List defects.",
     "VERDICT: quality-q33-q34-defects-<n>"),
    ("F42CritScorecard", "critic", ["calibration"],
     f"Calibration count for this round's self-assessment: every claim in {L}/SCORECARD.md §Round 42 and {L}/LOG.md §Round 42 and "
     f"{L}/SHONEN.md against repo state at {DOCS} (resolve each pointer, re-run each cheap command). Count mismatches; list each with "
     f"both locations and a corrected sentence.",
     "VERDICT: scorecard-mismatches-<n>"),
    ("F42NoHarm", "executor", ["calibration", "operability"],
     f"{HOST_RULE}\n\nNo-harm check: run {W}/integrate/measure.sh's command list yourself on a clean clone of {DOCS} (inside the "
     f"envelope, home writable cache) and diff every verdict line against {W}/integrate/measure-final.txt. Also confirm "
     f"`R42ExecNoHarm` ({B}/R42ExecNoHarm.md) baseline agrees with {W}/integrate/measure-baseline.txt. Any verdict that moved "
     f"other than the round-42 counters?",
     "VERDICT: no-harm-verdicts-equal-<k>/<n>"),
    ("F42RevRiders", "reviewer", ["operability"],
     f"{HOST_RULE}\n\nReview the three riders: {L}/plans/round_close.py R5 fix (diff vs {FREEZE}; run --selftest twice on one --work; "
     f"gate path unchanged for rounds 41/42), {L}/plans/scratch_guard.py (selftest; try escapes it should refuse), and the six rows "
     f"appended to {L}/corpus/routed-findings.jsonl (each `check` command runs and matches its status?). List defects.",
     "VERDICT: riders-defects-<n>"),
    ("F42ScoutMisroot", "scout", ["safety", "hygiene"],
     f"Hygiene watch for wave 2: `ls -la --time-style=full-iso /home/vgpnk/.local/bin` at start and end; `git -C {F} status --porcelain "
     f"--untracked-files=all` — any file a kengaku round-42 seat wrote into the fleet root? Is {SCR}/.ROUND-ROOT-SENTINEL present at "
     f"start and end? Scratch dirs under {SCR} with sizes. Report only.",
     "VERDICT: misroot-<n>-host-writes-<h>-sentinel-<present|missing>"),
    ("F42CritPlanNext", "critic", ["calibration", "coverage"],
     f"Attack the round-43 plan data: {B}/R42PlanNext.md (and the `### Planned (round 43)` block in {L}/SCORECARD.md if present when "
     f"you read it). For each candidate claim: can a do-nothing control reach its predicate? Is the predicate bound to literals (Q31)? "
     f"Are directions witnessed (Q29/Q33)? Is the coverage candidate a new class vs the eight TB2 graders? Does the plan carry the "
     f"wave-1 counter remediations (R42SentinelCounter V1-V3, V1b)? List defects D1..Dn with fixes.",
     "VERDICT: plan43-defects-<n>"),
    ("F42ConnClaims", "connector", ["calibration"],
     f"Cross-document consistency at {DOCS}: every number and hash in {CLAIMS}, the counters' docstrings, {W}/claims/*.txt, "
     f"{W}/integrate/*.txt, {L}/SCORECARD.md §Round 42, {L}/LOG.md §Round 42, {LESSON}, the entry and README rows — freeze/landing "
     f"hashes, 14 = 9+5, 29 fixtures, 16 cases, 7/9, 117→121 rows, 48→49 files. List every drift with both locations.",
     "VERDICT: drift-<n>"),
    ("F42ConnPatterns", "connector", ["calibration", "quality"],
     f"Cross-claim pattern: wave 1 found (a) a counter whose sandbox sentence was written from a command list (git config executes), "
     f"(b) attribution vacuous where the mutated line always runs, (c) a content check that is really a consistency check (V9), (d) a "
     f"grader that checks one path and executes another. Which earlier lane instruments (plans/round3*_*.py, round4*_*.py, pkg_gate.py, "
     f"order_check.py, tip_receipts.py) share each shape? file:line and a one-line fixture each.",
     "VERDICT: patterns-<n>-sites"),
    ("F42ConnFrontier", "connector", ["coverage", "adjacency"],
     f"Frontier and sibling check after landing: does {L}/PROVINCE.md §Round42's routing clause hold (any sibling lane that owns "
     f"digital-logic, simulator or compiler semantics — read their PROVINCE.md/SKILL.md)? Does README §Frontier now say exactly what "
     f"changed (8 of 89)? Is 'grader-compiled simulator over a data artefact' new vs the seven earlier graders (cite their entries)?",
     "VERDICT: frontier-<new|not-new>-routing-<holds|fails>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 42 wave 2 (falsify) item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {FX}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r42 wave 2 (falsify)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    spec = {"wave": "kengaku-r42-falsify",
            "milestone": "kengaku round 42 wave 2: falsify C1 battery42 and counter limits, C2 circuit-fibsqrt package, docs",
            "reportDir": ".ufo/waves/round-42/falsify", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/falsify-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c))
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"] + c["sentinel"]
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
