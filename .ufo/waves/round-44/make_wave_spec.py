#!/usr/bin/env python3
"""Renders .ufo/waves/round-44/wave-spec.json (ONE v2 wave, policy v2, band 64-128). L1 KengakuR44.

Shape (round-43 closure R4: meet the 64-seat floor; orchestrator note 20:07 -03): one v2 wave carrying build and
attack items together, plus at most one residual call of <=8 reviewer/critic seats after it (battery44 honesty
review, which needs the built battery). The generator asserts the run-9 route mix before writing: m_flash-routed roles
(executor/labrat/scribe/sonic/simplifier/revenger/sentinel — critic now routes to m_kfc and does not count) carry at
least half of the wave and attack roles (reviewer/critic/mutation-tester/labrat) at least a quarter."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-44"
B = f"{W}/wave"
SCR = "/fast/scratch/hyaku/kengaku-r44"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
TASK = "feal-linear-cryptanalysis"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/{TASK}"
CAP = f"{L}/corpus/evidence/round44/tb2-{TASK}"
RCPT = f"{L}/corpus/evidence/round44/feal-linear-probe.txt"
DRY = f"{L}/corpus/evidence/round44/feal-linear-dry-cases-freeze.txt"
C1 = f"{L}/plans/round44_c1_verify.py"
C1OLD = f"{L}/plans/round43_c1_verify.py"
C2 = f"{L}/plans/round44_c2_verify.py"
PROBE = f"{L}/plans/feal_linear_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
SPEC = f"{L}/plans/pkg-spec-r44.json"
CLAIMS = f"{L}/plans/round-44-claims.md"
ANC = f"{L}/plans/anchor_digest_check.py"
ORD = f"{L}/plans/order_check.py"
CL = f"{W}/claims"
WIT = f"{CL}/witness/w_u.py"
ENV = f"{CL}/envelope.sh"
FREEZE = "5f16ed04b04a80a17a5a1a060c12093d9a152a64"
FIRST = "45dc0bc81e42e02ecd272712086c372c8844b108"
B43 = f"{L}/.ufo/waves/round-43/build"
SPOT43 = f"{L}/corpus/lessons/round-43-verifier-spotcheck.md"
LESSON43 = f"{L}/corpus/lessons/round-43.md"
ENTRY43 = f"{L}/corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md"
ENTRY = f"{L}/corpus/knowledge/tb2-{TASK}-grader.md"
ROUTED = f"{L}/corpus/routed-findings.jsonl"
FLIP = f"{L}/plans/gate_flip_check.py"

HOST_RULE = (
    "Host safety: run any battery, counter attack, fixture build or probe that can write files inside a bwrap sandbox in "
    "which `/home/vgpnk/.local/bin` is read-only (the envelope below does this). Never write to a shared PATH directory, "
    "`/usr`, `/etc`, or `$HOME` outside scratch. (Round 40: a seat planted a `git` shim in `~/.local/bin` and broke other "
    "lanes' git for minutes.)")
ENVELOPE = (f"Envelope for every counter/battery/fixture/probe run: `{ENV} \"$S/env\" <command...>` (home read-only, ~/.cache "
            f"overlaid from scratch, `date +%T` start/end, a CONTENT digest of ~/.local/bin before/after; exit 4 + `INVALID` "
            f"when the digest changes — then the measurement does not count; re-run once, report both). Paste the ENVELOPE "
            f"lines with every result (QUALITY Q32).")
SCRATCH = (f"Scratch rule (operator directive 2026-10-25): S={SCR}/<YourSeatName>; mkdir -p \"$S\"; export TMPDIR=\"$S\"; pass "
           f"\"$S\" explicitly as --work / mkdtemp(dir=...). Delete it before you finish with `python3 {L}/plans/scratch_guard.py "
           f"safe-rm {SCR} <YourSeatName> \"$S\"` (or `rm -rf -- \"$S\"` only after checking the target string equals \"$S\"). "
           f"Never delete {SCR}, its `.ROUND-ROOT-SENTINEL` or another seat's dir. /tmp only for files under 50 MB; a /tmp path is "
           f"never evidence — copy receipts into your report subdir first.")
CLONE = (f'Clone rule: git clone -q --shared {L} "$S/lane"; verify `git -C "$S/lane" rev-parse --show-toplevel` equals "$S/lane" '
         f'before any write; every git call names -C "$S/lane"; never commit there. Any other fixture repo: D=$(mktemp -d -p "$S") '
         f'&& git -C "$D" init -q, verify `git -C "$D" rev-parse --show-toplevel` = $D, and every git call names -C "$D". Never '
         f'run `git commit`/jj with a throwaway identity anywhere else.')

CONTEXT = f"""# Goal
kengaku round 44 (hyaku run 9, 2026-10-26), ONE v2 wave (build + attack together). Lane repo: {L}.
Two claims are FROZEN at {CLAIMS} (freeze commit {FREEZE}; first recorded probe run {FIRST}) — read it first, in full.
Nothing frozen may change: not the tools {ANC} / {ORD}, not the counters {C1} / {C2}, not the probe {PROBE}, not the spec
{SPEC}, not the gate {GATE}, not the dry table {DRY}, not the captures {CAP}/, not the receipt {RCPT}, not {CL}/.
- C1 calibration: 5 frozen mutants (anchor_digest_check.py U5 U6 U7 U9; order_check.py U14c; MUTANTS table in {C1}: id, tool,
  class, direction, adv_kind, advertised sentence with file:line, source, `old -> new`). They are unmutated advertised behaviours
  priced by round-43 seat R43PlanNext ({B43}/R43PlanNext.md §B). At freeze no battery44 exists ({CL}/control-c1-nothing.txt
  `killed=0 survived=5`) and battery42+battery43 run as one battery kill none of them ({CL}/control-c1-standing-batteries.txt). The
  work: plans/battery44 modules until `python3 plans/round44_c1_verify.py --lane .` prints `MUTANTS total=5 killed=5 survived=0
  invalid=0 null_detected=0 unattributed=0` and `MUTANTS-BY-TOOL anchor=4/4 order=1/1`. A kill counts only when ATTRIBUTED: the
  traced mutant re-run reproduces the result AND runs a line of the replaced span (leg f) AND its SITE RECORD (next line + locals
  digest, or return value) differs from the reference's (leg g). Build-time refusals (SETUP): symlink escape (h), order argv blob
  (i), R1-R4, and NEW round-44 fences F1-F6: `.git` must be a directory and `--absolute-git-dir` inside d (F1); no depth cap
  (F2); EXACT argv shape — order `["--lane", v, "--claims", v, "--receipt", v]`, anchor only `--lane V`/`--evidence-ref V`/
  `--verbose` (F3); 30 s timeout on parent git (F4); no include / alternates (F5); the repo git discovers from `--lane` must
  live inside d (F6). Module contract (counter docstring): module-level FIXTURES = [{{"fid", "tool": "anchor"|"order", "expect":
  "accept"|"reject"|"error", "defects": [exact class set the UNMODIFIED tool prints — anchor: every `class=<C>` of a `DEFECT ` line;
  order: always []], "build": build}}]; build(ctx, d) fills the EMPTY directory d and returns the argv tail. ctx: ctx.init(dest),
  ctx.git(repo, *args), ctx.write(path, text|bytes), ctx.sh(*argv, cwd=); every path inside d. NO lane clone is offered: build
  every repo from nothing. Module source must not contain any SIDECHANNEL token (case-insensitive, also in comments/strings):
  `/proc ppid cmdline psutil environ fsmonitor hookspath filter. gitattributes core. alias. setsid daemon fork nohup socket /home/
  .local __file__ inspect importlib sys.path ctypes chmod witness settrace /run`. Pre-freeze direction module: {WIT}
  ({CL}/witness-run.txt: 5/5 killed, value=differs). The battery may NOT import, copy or read that module and must not be a
  re-spelling of it: write your own fixtures with DIFFERENT shapes. Develop with `python3 {C1} --lane "$S/lane" --battery-dir
  <your battery dir> --only <ids> --work "$S/w"` (prints `PREDICATE C1 n/a`; a few seconds), always inside the envelope.
- C2 coverage: pinned Terminal-Bench 2.0 `{TASK}` grader (terminal-bench-2 @ {PIN}; raw base {RAW}/) to be admitted as
  {ENTRY} with rows S138 (tests/test_outputs.py), S139 (instruction.md), S140 (environment/task-deps/gen.py), S141
  (environment/Dockerfile), S142 (tests/test.sh), S143 (README.md), S144 (solution/solve.sh), S145 (environment/task-deps/
  decrypt.c), S146 (task.toml); tier A, status mined, opened 2026-10-26 (L1 fetched all eleven files 20:10:09 -03; captures +
  SHA256SUMS in {CAP}/, digests pinned in {SPEC}). Receipt {RCPT}: 14 cases, `cases=14 observed_pass=8 observed_fail=6
  mismatches=0`, `regrade cases=14 differ=0`. Grader facts: test_outputs.py:4-103 hold 100 decimal constants; :120 `data =
  open("/app/plaintexts.txt").read()`; :121-122 `for c in soln.split(): assert c in data` (substring of the whole file; no
  count, order, format or exactness check); test.sh:22-26 rewards pytest's exit status; gen.py:12 prints the four round keys and
  gen.py:18-28/:57-62 derive every plaintext as sha256(seed+counter) — gen.py is deleted from the image (Dockerfile:12-13) but
  published in the repo; instruction.md names no output format. Passing without an attack (measured): decrypt with the public
  gen.py keys; replay the public gen.py hash chain; copy the constants from the public test file. Also passing: concatenated,
  reversed, zero-padded, plus 100 wrong-key decoys. Failing: no file, one missing, hex, wrong key, pairs plaintexts,
  ciphertexts copied. Counter {C2} = round-43 V1-V10 re-pointed + V11: the entry's `## Predictor` section holds ONE ```python
  block defining `predict(text)` (text = file content or None if absent) that must agree with the EXECUTED captured grader on 48
  generated states. Entry must have sections `## Case table` (`| `<cid>` | <P|F> | <pass|fail> | <text> |`, receipt order),
  `## Mechanism` (`| `<cid>` | `<capture>:<line>` | “<quote>” |`, line from the counter's DECISIVE map, quote >=2 words verbatim
  on that line), `## Requirement map` (`| `instruction.md:<L>` | `<tag>` | <enforced|unenforced|partly> | `case`, ... |`, label
  derived from all receipt cases carrying the tag), `## Located quotes` (pkg_gate.py QUOTE_ROW shape, >=10 quotes / >=10
  locations, 3-25 words), `## Predictor`; a `source:` first line citing S138; every S138-S146 id outside the `source:` line.
- Round-43 closure routed items: {SPOT43} §5 (R1-R5). Routed ledger: {ROUTED} (`python3 {L}/plans/routed_open.py --lane <clone>
  --list` / `--observe`).

# Host-safety rule (orchestrator; binding for every seat)
{HOST_RULE}
{ENVELOPE}

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report is {B}/<YourSeatName>.md; drafts and receipts go under {B}/<YourSeatName>/ (create it). Never copy
  a corpus/ or plans/ tree, a lane mirror, or a clone into {B}/; no receipt file over 1 MiB (quote it, give its sha256, delete it).
  Every seat MUST leave its report file (round-43 closure D3: one seat returned output only in the results JSON).
- {SCRATCH}
- Write ONLY inside {B}/ (your report + your own subdir) and your scratch dir. NEVER edit the lane's corpus/, plans/,
  SCORECARD.md, LOG.md, README.md, SKILL.md, PROVINCE.md, SHONEN.md or any other lane file — draft for the L1, who integrates.
  Never write into {F} (fleet root), sibling lanes, the lane's jj state, or the lane's Git index. Never run git
  add/commit/stash/checkout/reset/push/pull or any mutating jj command in the lane. Seats never commit or push anywhere.
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
  URL+section) and is <= 25 words. Do not fabricate output; if something cannot be fetched or run, say so.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""


def bat(name, module, mid, hints):
    return (name, "executor", ["calibration", "operability"],
            f"{HOST_RULE}\n\nWrite the C1 battery44 module {B}/{name}/battery/{module}.py (stdlib only; every fid starts "
            f"`{module}-`) whose fixtures ATTRIBUTABLY kill frozen mutant {mid} of {C1} in its declared direction (read the "
            f"mutant's tool, class, direction, `old -> new` there, and the tool branch it changes). Each fixture's `defects` must "
            f"equal the exact class set the UNMODIFIED tool prints on it, and its `expect` must match the reference exit code. At "
            f"least TWO fixtures with different shapes (e.g. a realistic multi-row registry or multi-commit history, a second "
            f"trigger of the same branch), none a re-spelling of {WIT} (another seat writes a second module for {mid}; do not "
            f"coordinate, independence is the point). One-line comment per fixture naming what it demonstrates. Hints: {hints} "
            f"Prove it in your clone, inside the envelope: `python3 {C1} --lane \"$S/lane\" --battery-dir {B}/{name}/battery "
            f"--only {mid} --work \"$S/w\"` must print every FIXTURE line of your module `ok`, `wrong=0 tampered=0 sidechannel=0`, "
            f"`null_detected=0 unattributed=0`, and `{mid} killed by=<your fid> attributed=... value=differs`. Paste that output. "
            f"Then remove each fixture in turn and record whether {mid} still dies (load-bearing table). Finally copy your module "
            f"into \"$S/lane/plans/battery44/\" and run the FULL default counter (`python3 {C1} --lane \"$S/lane\" --work \"$S/w2\"`); "
            f"paste its MUTANT and summary lines (other mutants surviving there is expected). Name every limit you hit.",
            f"VERDICT: battery44-{module}-{mid}-killed-<yes|no>-fixtures-<n>")


ITEMS = [
    # ---- C1 build: two independent modules per mutant ----
    bat("R44BatU5a", "u5_short_a", "U5", "a 63-hex anchor token is `digest-short`; the mutant relabels it `digest-long`."),
    bat("R44BatU5b", "u5_short_b", "U5", "vary the short length (8..63 hex, no ellipsis) and the row shape."),
    bat("R44BatU6a", "u6_long_a", "U6", "a 65+-hex anchor token is `digest-long`; the mutant relabels it `digest-short`."),
    bat("R44BatU6b", "u6_long_b", "U6", "vary the long length and put several rows in the registry."),
    bat("R44BatU7a", "u7_twin_a", "U7", "a row naming two byte-identical captures with ONE token is not a defect "
        "(anchor_digest_check.py:94-101); the mutant claims only the first capture, so the twin becomes capture-unanchored."),
    bat("R44BatU7b", "u7_twin_b", "U7", "three identical captures, or a twin pair named via different routes in one row."),
    bat("R44BatU9a", "u9_worktree_a", "U9", "an `Erratum (round 37): S<id> anchor sha256 <wrong> ...` line present only in "
        "the WORKING TREE copy of a committed lesson (anchor_digest_check.py:105-108); the mutant reads HEAD instead."),
    bat("R44BatU9b", "u9_worktree_b", "U9", "a lesson whose committed text differs from its working-tree text in another way "
        "that changes the verdict."),
    bat("R44BatU14a", "u14c_name_a", "U14c", "a claims file whose name is not `round-NN-claims.md` (order_check.py:159-163) "
        "is a setup error, exit 2; with the guard off the tool proceeds. The argv must be the exact 6-token contract shape."),
    bat("R44BatU14b", "u14c_name_b", "U14c", "a different unparseable name (e.g. round-xx, a suffix, nested dir) and history."),
    # ---- C1 attacks on the frozen counter ----
    ("R44SentinelFences", "sentinel", ["calibration", "safety"],
     f"{HOST_RULE}\n\nAttack the round-44 fence repairs F1-F6 in {C1} (`pin_git`, `repo_breach`, `argv_shape_breach`, `lane_breach`, "
     f"`order_argv_breach`; compare with {C1OLD} and {B43}/R43SentinelCounter.md). For each repair, try to build a module in "
     f"scratch that the round-44 counter ADMITS (no SETUP refusal) while the measured scenario still lives outside d or a parent git "
     f"call reads/executes outside d. Known weak spot to measure, not assume: `lane_breach` runs rev-parse WITHOUT `--no-includes` "
     f"(an include file outside d is read before `repo_breach` refuses it). Paste each vector, the counter output and envelope lines.",
     "VERDICT: fence-bypasses-<n>-of-<tried>"),
    ("R44CritC1Counter", "critic", ["calibration"],
     f"{HOST_RULE}\n\nFalsify C1's admission rule: build dishonest batteries in scratch (fixtures that kill by side effect, by "
     f"exploiting the tracer, by a declared direction that differs from the one witnessed, by tampering, by timing) and run them "
     f"through {C1} with `--battery-dir`. Does any reach `killed=5 ... PREDICATE`-shaped lines for a mutant without a fixture that "
     f"genuinely demonstrates the advertised behaviour? Also check that the witness-as-battery pass ({CL}/control-c1-witness-as-"
     f"battery.txt) is the only cheap route. Paste every run.",
     "VERDICT: dishonest-battery-vectors-<blocked>/<tried>"),
    ("R44MutC1Fences", "mutation-tester", ["calibration", "operability"],
     f"{HOST_RULE}\n\nMutation-test the NEW code of {C1} (pin_git, repo_breach, argv_shape_breach, lane_breach, order_argv_breach; "
     f"`diff {C1OLD} {C1}` shows it): generate single-edit mutants of those functions in a scratch copy, and for each run the six "
     f"hostile modules {CL}/hostile/f*.py plus {WIT} (development mode, envelope). A guard mutant is caught when a hostile module is "
     f"admitted or an honest witness fixture is refused. Table: mutant, caught-by, survived. Draft the missing hostile fixture for each "
     f"survivor.",
     "VERDICT: fence-mutants-caught-<k>/<n>"),
    ("R44CritEquivU", "critic", ["calibration"],
     f"For each of U5 U6 U7 U9 U14c in {C1}: is the mutant equivalent, redundant with another, or does its `adv` cell misquote the "
     f"docstring line it cites ({ANC} / {ORD})? Re-read the tool code paths; for U7 and U9 check the docstring sentence really "
     f"advertises what the mutant breaks. Also re-check the claim that battery42+battery43 kill none of the five "
     f"({CL}/control-c1-standing-batteries.txt) — and run the older batteries ({L}/plans/battery40, battery41 if present, in a "
     f"clone) through {C1} with `--battery-dir`: does ANY committed battery kill one (a do-nothing control reaching the target)?",
     "VERDICT: equivalent-<n>-misquoted-<m>-older-battery-kills-<k>"),
    ("R44RevMutRows", "reviewer", ["calibration", "quality"],
     f"Review the MUTANTS rows of {C1} line by line: `old` occurs exactly once in the pinned tool; `new` is a single minimal "
     f"replacement; the cited file:line ranges hold the quoted words verbatim (paste `sed -n` output); direction labels match "
     f"{CL}/witness-run.txt. Report each row ok/defect.",
     "VERDICT: mutant-rows-<ok>/5"),
    ("R44LabratControls", "executor", ["calibration"],
     f"{HOST_RULE}\n\nHypothesis (falsifiable): every C1 freeze control in {CL} (control-c1-*.txt) re-derives on a clean --no-local "
     f"clone at {FREEZE}. Re-run {CL}/c1_controls.sh's commands one by one against your clone (adapt its paths to your $S; never "
     f"write to the lane) and diff the verdict lines with the committed files. Report confirmed/falsified per control.",
     "VERDICT: c1-controls-reproduce-<k>/<n>"),
    ("R44LabratSiteStable", "executor", ["calibration"],
     f"{HOST_RULE}\n\nHypothesis: {C1}'s verdict on {WIT} is invariant under `--jobs 1/8/16`, the counter's own PYTHONHASHSEED, and "
     f"two different --work roots. Run each combination in your clone inside the envelope and diff MUTANT/summary lines.",
     "VERDICT: site-stable-<confirmed|falsified>-runs-<n>"),
    ("R44CritPredicate", "critic", ["calibration"],
     f"Q-sentence check (closure rule: one predicate = same sentence in plan, same condition in code, same label in receipt): compare "
     f"the frozen predicates in {CLAIMS} with the docstrings and the `good`/`PREDICATE` code of {C1} and {C2}. Any wording that "
     f"differs, any universal clause the counter does not enumerate, any after-state a do-nothing control reaches (build the "
     f"cheapest one you can think of beyond the committed controls)? Also judge axis naming (surface vs number).",
     "VERDICT: predicate-drift-<n>-cheap-control-reaches-<yes|no>"),
    ("R44XMutNearU", "mutation-tester", ["calibration"],
     f"{HOST_RULE}\n\nRound-45 data: generate near-variants of U5 U6 U7 U9 U14c (other single edits on the same lines/branches of "
     f"{ANC} / {ORD}) and run them against {WIT} and against battery42+battery43 (copied into a scratch battery dir) through a "
     f"scratch copy of {C1} with your mutants as MUTANTS (development mode). Table: variant, direction witnessed, killed by which "
     f"battery. Never edit the frozen counter.",
     "VERDICT: near-variants-<n>-alive-after-standing-<k>"),
    ("R44LabratLaneInclude", "executor", ["calibration", "safety"],
     f"{HOST_RULE}\n\nHypothesis (falsifiable): {C1}'s `lane_breach` makes the counter's own process read a file OUTSIDE d when a "
     f"fixture's .git/config carries include.path=<outside file> (it calls rev-parse without --no-includes before repo_breach "
     f"refuses the include). Build the fixture in scratch, run the counter under `strace -f -e trace=openat` (if strace is "
     f"installed; else inotifywait or an atime check) and report whether the outside file is opened by the PARENT. Report only.",
     "VERDICT: lane-breach-reads-outside-<confirmed|falsified>"),
    # ---- C2 build ----
    ("R44PkgEntry", "scribe", ["coverage", "depth"],
     f"Draft the knowledge entry {B}/R44PkgEntry/tb2-{TASK}-grader.md (the L1 integrates it as {ENTRY}). Read every capture in "
     f"{CAP}/ and the receipt {RCPT}. Follow {ENTRY43} for structure (first lines `source: S138 …`, `verified-at: 2026-10-26`, "
     f"`recheck: 180d …`), and satisfy the counter {C2} exactly: `## Case table` = receipt rows; `## Mechanism` one row per case "
     f"citing a line from {C2}'s DECISIVE map with a >=2-word verbatim quote; `## Requirement map` derived from the receipt (tags "
     f"and lines in {DRY}); `## Located quotes` (>=10 quotes at >=10 distinct capture lines, 3-25 words, verbatim, pkg_gate.py "
     f"QUOTE_ROW shape — read {GATE} QUOTE_ROW); `## Predictor` with one ```python block `def predict(text):` (substring rule) — "
     f"self-check it: copy the lane to a clone, place your draft at the entry path and run `python3 {C2} --lane \"$S/lane\"`; paste "
     f"the V4/V7/V9/V10/V11 lines (V2/V3 need rows; others may be red). Findings to state with line evidence: substring semantics; "
     f"three attack-free passes from PUBLIC pin files (gen.py keys, gen.py hash chain, test constants); no format stated in "
     f"instruction.md vs decimal-only grader; class difference from the round-43 feal-differential entry (constant compare of a file "
     f"vs imported module). Every sentence that rests on task.toml or solve.sh must cite S146/S144. No novelty claim.",
     "VERDICT: entry-drafted-c2-legs-ok-<k>/5"),
    ("R44PkgRows", "scribe", ["coverage", "discernment"],
     f"Draft the nine registry rows S138-S146 for {L}/corpus/SOURCES.md (read its header and the S129-S137 rows for the 11-cell "
     f"schema; anchor cell `sha256 <the spec pin from {SPEC}>` + a locator; status mined; tier A; opened 2026-10-26; recheck a valid "
     f"ISO date or `180d`; used-by the entry path; no `|` inside a cell) and the lesson `## Gate` block: per row the URL "
     f"({RAW}/<upstream>), access date+time (re-fetch each with curl now and `cmp` against {CAP}/<capture>; record the time), and a "
     f"<=25-word located quote. Add Gate REJECT rows for captured-but-not-row files (feal.c, gitignore) with reason + flip condition "
     f"stated so it can be checked against the entry (closure R1). Validate in scratch: a copy of corpus/ with your rows appended → "
     f"`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <copy>/SOURCES.md` exit 0; and the anchor tool "
     f"`python3 {ANC} --lane <clone with rows+captures>` defects 0. Paste both.",
     "VERDICT: rows-drafted-9-census-exit-<e>-anchor-defects-<d>"),
    ("R44PkgProse", "scribe", ["coverage", "adjacency"],
     f"Draft the integration prose for the C2 package: (a) {L}/corpus/README.md: knowledge index row for the entry, a coverage-map "
     f"bullet, and the `## Frontier` TB2 clause narrowed to 10 of 89 naming `{TASK}`; (b) {L}/PROVINCE.md: one paragraph whose one "
     f"line names both `{TASK}` and `tb2-{TASK}-grader.md`, plus a routing clause (what is unowned: cryptanalysis technique; what "
     f"sibling owns what — check sibling PROVINCE files under {F}/*-shokunin/PROVINCE.md); (c) {L}/SKILL.md: a short section "
     f"'Constant-compare TB2 grader — round 44' with a decision table citing receipt cases. Paste-ready blocks + where each goes "
     f"(read the current tail of each file).",
     "VERDICT: prose-blocks-<n>"),
    ("R44PytestParity", "executor", ["coverage", "calibration"],
     f"{HOST_RULE}\n\nReal-pytest parity for the C2 receipt: rebuild each of the 14 case end states the way {PROBE} does (read it; "
     f"you may import its CASES/SEED/recipes in a scratch copy), then run the captured {CAP}/test_outputs.py under `uvx -p 3.13 -w "
     f"pytest==8.4.1 pytest` (test.sh's harness, minus network) with /app mapped by bwrap, and compare pytest's exit status per case "
     f"with the receipt's verdicts. Report 14 rows and any mismatch.",
     "VERDICT: pytest-parity-<k>/14"),
    ("R44CritIndep", "critic", ["coverage", "calibration"],
     f"Independent re-derivation: WITHOUT running {PROBE}, predict each of the 14 receipt verdicts from the captures alone (read "
     f"test_outputs.py, gen.py, decrypt.c, solve.sh, Dockerfile), then check against {RCPT}. Then design and run three cases of your "
     f"own the probe lacks (e.g. CRLF line endings, a 2 GB-ish/very large file, non-UTF-8 bytes, a trailing NUL, a file that is a "
     f"directory, a symlink to /dev/zero) in your own bwrap harness, and report what the grader does.",
     "VERDICT: rederived-<k>/14-own-cases-<n>"),
    ("R44CritCases", "critic", ["coverage"],
     f"Attack the probe's case set ({DRY}, {PROBE}): which grader behaviours does it NOT exercise that the entry may later claim "
     f"(read-error exceptions, encoding, size, timing of the verifier, the canary line, pytest collection)? Which cases are "
     f"redundant? Is any `violates=` tag wrong given instruction.md's exact words? Is the /pub modelling (public files at the pin) "
     f"honest? List defects with evidence.",
     "VERDICT: case-set-defects-<n>"),
    ("R44MutC2V11", "mutation-tester", ["calibration", "coverage"],
     f"{HOST_RULE}\n\nMutation-test V11 of {C2} (STATE_KINDS, states(), v11(), sandboxed(), GRADE_PY, PREDICT_PY): single-edit "
     f"mutants in a scratch copy; for each run {CL}/c2_predictor_control.py (adapted to import your mutant copy) — a mutant is caught "
     f"when the control's required verdicts flip. Table: mutant, caught, survived; draft a control for each survivor.",
     "VERDICT: v11-mutants-caught-<k>/<n>"),
    ("R44CritV11", "critic", ["calibration"],
     f"Falsify V11 of {C2}: write predictors (scratch only) that pass V11 WITHOUT the substring reading — e.g. a lookup keyed on "
     f"hashes of the 48 seeded states (how would an author get the verdicts without running the grader?), a predictor that reads "
     f"files inside its sandbox, one that times out or prints extra lines. Run each through `c2.v11()` on a mirror like "
     f"{CL}/c2_predictor_control.py does. Also: is 48 states with seed 44 enough — which grader behaviours never appear among them?",
     "VERDICT: v11-bypasses-<n>-of-<tried>"),
    ("R44SentinelSandbox", "sentinel", ["safety", "operability"],
     f"{HOST_RULE}\n\nSandbox review of the C2 instruments: {PROBE} (sandbox_argv: /app bind, /pub ro, /tests ro, recipes) and "
     f"{C2} `sandboxed()` (the predictor runs entry-supplied code). Can a recipe or predictor write outside its dirs, read the lane, "
     f"reach the network, leave a process behind, or make the counter print ok? Try concrete vectors in scratch copies.",
     "VERDICT: sandbox-escapes-<n>"),
    ("R44ScoutPriorArt", "scout", ["novelty", "coverage"],
     f"Prior art for the C2 findings (dated receipt; nothing asserted 'unpublished' without a search): search GitHub issues/PRs of "
     f"harbor-framework/terminal-bench-2 and laude-institute/terminal-bench (`gh search issues`/`gh api`), the TB2 paper/site, and the "
     f"web for: `{TASK}` grader weaknesses; answer keys or keys recoverable from published task files (gen.py keys, hash-chain "
     f"plaintexts); substring/constant-compare graders in agent benchmarks. Per finding: published / adjacent / not found, with URL "
     f"and access time.",
     "VERDICT: prior-art-published-<p>-adjacent-<a>-not-found-<n>"),
    ("R44ScoutRefetch", "scout", ["freshness"],
     f"Freshness: re-fetch all eleven captures from {RAW}/<upstream path> (paths in {SPEC} rows + feal.c, .gitignore), `cmp` each with "
     f"{CAP}/, and check whether the terminal-bench-2 default branch has changed any of these files since the pin (`gh api "
     f"repos/harbor-framework/terminal-bench-2/commits?path={TASK}`). Report times, results, drift.",
     "VERDICT: refetch-identical-<k>/11-upstream-drift-<n>"),
    ("R44CritSeparability", "critic", ["calibration"],
     f"Separability: verify each counter passes with the other's work wholly absent and fails without its own — reason from the code "
     f"of {C1} and {C2} which files each reads (grep), and test one direction cheaply (e.g. run {C2} on a clone with plans/battery44 "
     f"deleted is trivially fine; run {C1} on a clone without the C2 package). Any shared input?",
     "VERDICT: separable-<yes|no>-shared-inputs-<n>"),
    ("R44RevProbe", "reviewer", ["coverage", "quality"],
     f"Review {PROBE}'s fidelity to the task: does SEED replay Dockerfile:6-11 exactly (order, rm of orig_plaintexts.txt and gen.py)? "
     f"Is /tests honest (the real harness copies the tests dir at verification time)? Is reading /pub honest about what an agent can "
     f"see? Is the harness's exit-status mapping right for test.sh? Does the receipt leak host info? Line-referenced defects.",
     "VERDICT: probe-defects-<n>"),
    ("R44LabratRerun", "executor", ["coverage", "calibration"],
     f"{HOST_RULE}\n\nHypothesis: the C2 receipt {RCPT} is byte-equal on re-run in a clean --no-local clone (3 runs: normal, `env -i "
     f"PATH=/usr/bin:/bin`, a different --work root), and its oracle case does not depend on -O3 (rebuild decrypt/attack at -O0 in a "
     f"scratch copy of the probe). Report cmp results and envelope lines.",
     "VERDICT: rerun-byte-equal-<k>/3-opt-sensitive-<yes|no>"),
    ("R44CritGateRows", "critic", ["discernment"],
     f"Pre-empt the round-43 discernment disagreement (closure {SPOT43} §3: a `not fired` flip that had fired). For the round-44 C2 "
     f"package: which captured files are not rows (feal.c, gitignore) and which entry sentences could later rest on them alone? Which "
     f"proposed rows (S144 solve.sh, S145 decrypt.c, S146 task.toml) are worth a tier-A row vs tier B? Write the Gate reject rows with "
     f"falsifiable flip conditions and the exact check command that decides each flip.",
     "VERDICT: gate-flips-defined-<n>"),
    ("R44LabratF1Leak", "executor", ["novelty", "coverage"],
     f"Hypothesis (falsifiable, static, no task run): among the 14 TB2 F1 constant-compare tasks listed in "
     f"{B43}/R43ConsiderThese.md (or re-derive the list), at least 3 others have their expected answer derivable from files "
     f"published in the task directory at pin {PIN} (a generator with fixed seed/keys, the answer in the tests, a solution file). "
     f"Fetch each task's files via raw URLs into scratch and classify: leak-in-tests / leak-in-generator / no-leak. Table with line "
     f"evidence.",
     "VERDICT: f1-answer-leaks-<k>/14"),
    ("R44RevenGenIntent", "revenger", ["coverage", "novelty"],
     f"Reverse-engineer intent: why does `{TASK}` grade by substring and leave gen.py's keys in the published repo? Read the "
     f"terminal-bench-2 git history for this task (`gh api 'repos/harbor-framework/terminal-bench-2/commits?path={TASK}'`, each "
     f"commit's diff), the terminal-bench (v1) original if it exists (laude-institute/terminal-bench), and the README. Report the "
     f"design history with commit URLs; is the leak deliberate (e.g. keys were in the instruction once) or an oversight?",
     "VERDICT: intent-<deliberate|oversight|unknown>"),
    # ---- routed: round-43 closure R1-R5 ----
    ("R44FlipVerdict", "executor", ["discernment", "operability"],
     f"Closure R1 fix: extend {FLIP} (copy it to {B}/R44FlipVerdict/gate_flip_check.py; never edit the lane) so a `Flip check "
     f"(round N): <item> — not fired — …` line that names a file is RED when the entry the lesson's Gate concerns carries a "
     f"`<file>:<line>` citation of that file (the round-43 case: `task.toml:22` cited in {ENTRY43} while {LESSON43} says `not "
     f"fired`). Keep the old checks and its --selftest; add selftest cases red/green; show it RED on the committed {LESSON43} and "
     f"green on a scratch copy with corrected lines. Paste outputs and a QUALITY criterion draft (next free Q-number).",
     "VERDICT: flip-verdict-check-red-on-r43-<yes|no>-selftest-<k>/<n>"),
    ("R44FlipLines", "scribe", ["discernment", "quality"],
     f"Closure R1 drafts: (a) appended `Flip check (round 44): task.toml — fired — …` and `… solve.sh — fired — …` lines for "
     f"{LESSON43} (append only; evidence = the entry lines citing them, re-read with grep -n); (b) an appended `## Errata (round "
     f"44)` block for {ENTRY43} that re-sources or withdraws finding 11's 'only time bound' sentence, the Mechanism rows "
     f"`slow-oracle-45s`→task.toml:22 and finding 12's solve.sh:90 claim (choose: admit task.toml/solve.sh as tier-B rows of the "
     f"round-43 package with Gate quotes, or withdraw — justify), reconciled with the entry's own provenance paragraph (:72-74). Never "
     f"in place.",
     "VERDICT: r1-drafts-<n>"),
    ("R44S134Erratum", "scribe", ["quality"],
     f"Closure R2: draft an appended erratum for {ENTRY43}: its `source:` line says README.md 'lines 1-34' while the S134 row anchor "
     f"and Gate quote are at `:1-35`/`:35` (the capture lacks a final newline: `wc -l` 34, `awk 'END{{print NR}}'` 35). Re-verify with "
     f"commands on {L}/corpus/evidence/round43/tb2-feal-differential-cryptanalysis/README.md; propose the exact appended text.",
     "VERDICT: s134-erratum-drafted"),
    ("R44RevFlipAudit", "reviewer", ["discernment"],
     f"Audit every `Flip check (round N): … — not fired — …` line in {L}/corpus/lessons/*.md: for each, is the verdict TRUE against "
     f"the entry/rows it concerns (grep the entry for citations of the refused item)? Table: lesson:line, item, verdict, true/false, "
     f"evidence. This is the outside check of the closure's discernment disagreement, independent of R44FlipVerdict's tool.",
     "VERDICT: not-fired-lines-<n>-false-<f>"),
    ("R44EnvelopeV3", "executor", ["operability", "safety"],
     f"Routed (R43ReviewEnvelope): the envelope {ENV} misses a mode-only change and a rewrite of a mode-000 (unreadable) file. Draft "
     f"{B}/R44EnvelopeV3/envelope.sh that digests mode bits and records unreadable entries (stat-based), keeping exit 4 on change; "
     f"test on a COPY whose target dir is a scratch dir you mutate (never touch ~/.local/bin): content rewrite, new file, symlink "
     f"retarget, chmod, rewrite of a mode-000 file, xattr. Red/green table for old vs new.",
     "VERDICT: envelope-v3-detects-<k>/<n>-old-<m>/<n>"),
    ("R44RevEnvelope", "reviewer", ["operability"],
     f"Review {ENV} independently of any draft: list its remaining blind spots (hardlinks, ACLs, xattrs, a race between before/after, "
     f"/fast/scratch writes, writes to ~/.cache through the overlay surviving the run) with a cheap demonstration each in scratch.",
     "VERDICT: envelope-blind-spots-<n>"),
    ("R44ReadmeIndex", "scribe", ["coverage", "quality"],
     f"Routed: README index parity. `ls {L}/corpus/lessons | wc -l` vs `grep -c '^| `lessons/' {L}/corpus/README.md` (62 vs 33 "
     f"today); same for knowledge/ and evidence dirs. Draft the missing index rows (one line each, what the file is, from reading "
     f"it) and the evidence-section rows for rounds 41-44, as paste-ready blocks. Do not invent descriptions — read each file's head.",
     "VERDICT: index-rows-drafted-<n>"),
    ("R44RevIndexParity", "reviewer", ["coverage"],
     f"Independent parity audit of {L}/corpus/README.md vs disk, both directions (every index row resolves; every file has a row) "
     f"for knowledge/, lessons/, evidence/; also PROVINCE.md surfaces that no longer resolve. Commands + counts; a checker command "
     f"the L1 can paste into a routed row `check`.",
     "VERDICT: parity-missing-<m>-dangling-<d>"),
    ("R44RoutedObserve", "scout", ["calibration", "quality"],
     f"considerthese/2026-10-26.md proposal 1 (routed-findings burn-down): on a clean clone of the lane tip run `python3 "
     f"{L}/plans/routed_open.py --lane \"$S/lane\" --observe` and `--list`; for every open row, say whether its `check` passes now, "
     f"is null, or is stale; propose a burn-down line format (opened/closed per round) and compute it from the ledger history "
     f"(`git log -p -- corpus/routed-findings.jsonl`). Paste-ready closure field values for rows that pass.",
     "VERDICT: routed-open-<n>-closable-now-<k>"),
    ("R44RoutedLesson", "scribe", ["quality"],
     f"Routed rows R42-R3-11..17 (sources {L}/.ufo/waves/round-42/falsify/F42RevLesson.md lines named in each row of {ROUTED}): "
     f"re-check each defect against the current {L}/corpus/lessons/round-42.md; draft the appended correction for each still-true "
     f"defect and a `check` command for its ledger row; say which are already fixed (with evidence).",
     "VERDICT: lesson-defects-fixed-<k>-of-7"),
    ("R44RoutedQuality", "scribe", ["quality"],
     f"Routed rows R42-R3-18/19/20/23 (F42RevQuality.md) and R42-R3-31/32 (F42CritScorecard.md, F42ConnClaims.md): re-check each "
     f"against current {L}/corpus/QUALITY.md / SCORECARD.md; draft appended corrections + `check` commands; mark refuted ones.",
     "VERDICT: quality-scorecard-defects-fixed-<k>-of-6"),
    ("R44RoutedPackage", "scribe", ["quality", "coverage"],
     f"Routed rows R42-R3-02/05/06/07/08/09 (F42RevC2Package.md) and R42-R3-38/39/40 (F42EntryQuotes.md, circuit-fibsqrt entry): "
     f"re-check each against {L}/corpus/knowledge/tb2-circuit-fibsqrt-grader.md and its rows; draft appended errata + `check` "
     f"commands; mark the ones the round-43 errata already fixed (run each row's current `check`).",
     "VERDICT: package-defects-fixed-<k>-of-9"),
    ("R44RoutedRiders", "executor", ["operability"],
     f"{HOST_RULE}\n\nRouted rows R39-R2 (git_leak_probe.py `--work` absent dir), R42-R3-26/27 (F42RevRiders.md) and R42-R6 "
     f"({L}/plans/scratch_guard.py:17): reproduce each in a clone, draft the minimal fix as a patch file under {B}/R44RoutedRiders/ "
     f"(never edit the lane), with a check command that is red before and green after the patch (paste both).",
     "VERDICT: rider-fixes-<k>-of-4-red-green-<m>"),
    ("R44RoutedPlan", "critic", ["calibration"],
     f"Routed rows R42-R3-33..37 (F42CritPlanNext.md) and R40-R1/R40-R5/R39-R4: are they satisfied, superseded or still open at the "
     f"lane tip (read SCORECARD `### Planned (round 44)`, the round-43/44 claims)? For each: verdict + evidence + a `check` command.",
     "VERDICT: plan-rows-closable-<k>-of-<n>"),
    ("R44MutC1Guards", "mutation-tester", ["calibration"],
     f"{HOST_RULE}\n\nRouted (R43MutC1Counter: 7/15 counter guards survived). Re-run that mutation set (see "
     f"{B43}/R43MutC1Counter.md and its subdir) against {C1} (guards carried from round 43) with the committed round-44 controls "
     f"({CL}/control-c1-*.txt inputs, hostile f1-f6, witness): which guards are now caught, which still survive? Draft a red "
     f"control for each survivor.",
     "VERDICT: c1-guards-caught-<k>/<n>"),
    ("R44MutC2Guards", "mutation-tester", ["calibration"],
     f"{HOST_RULE}\n\nRouted (R43MutC2Counter: 7/13 V9/V10 guards survived). Re-run that mutation set (see "
     f"{B43}/R43MutC2Counter.md) against V9/V10 of {C2} using mirrors built from the receipt and a drafted entry shape; which "
     f"survive? Draft a red control per survivor.",
     "VERDICT: c2-guards-caught-<k>/<n>"),
    # ---- frontier step / hygiene / assimilation ----
    ("R44LessonMistakes", "scribe", ["discernment", "quality"],
     f"Draft {B}/R44LessonMistakes/round-44-mistakes.md: the `## Mistakes` block for corpus/lessons/round-44.md — class · evidence "
     f"pointer · captured-by · fix — for (1) the round-43 false `not fired` flip ({SPOT43} §3); (2) round 43 closing at 38 seats "
     f"(D1); (3) one seat with no report file (D3); (4) round-44 freeze drafting U3, which the standing batteries already kill "
     f"({CL}/control-c1-standing-batteries-six-mutant-draft.txt) — caught by the standing-battery control before freeze; (5) any "
     f"mistake you find by sweeping round-43/44 artefacts (paste the sweep command). A fix counts only once shown able to fail.",
     "VERDICT: mistakes-drafted-<n>"),
    ("R44QualityQ", "scribe", ["discernment", "quality"],
     f"Draft QUALITY.md criteria (read {L}/corpus/QUALITY.md tail for numbering and shape): (a) flip verdicts are checked against "
     f"entry citations (closure R1); (b) a do-nothing control includes the lane's standing batteries (the U3 lesson); (c) a content "
     f"leg's key must come from executing the source, not from the instrument (V11). Each with its evidence pointer and the check "
     f"that shows it able to fail.",
     "VERDICT: criteria-drafted-<n>"),
    ("R44ConsiderThese", "scout", ["quality"],
     f"considerthese (read-only operator input): read all of {L}/considerthese/*.md; list every 'proposals only … not implemented' "
     f"item, whether a later round implemented it (grep lessons/SCORECARD), and confirm proposal 1 of 2026-10-26.md (routed burn-down) "
     f"is the best fit for this round vs proposal 2 (one standing TB2 admission counter). Lesson-ready block citing file + date.",
     "VERDICT: proposals-open-<n>-chosen-<id>"),
    ("R44MergeRescreen", "scout", ["coverage", "discernment"],
     f"Assimilation re-screen (read-only on /home/vgpnk/Projects/shokuknow): has merge/kengaku/ changed since 2026-10-24? Run the "
     f"id-collision check into {B}/R44MergeRescreen/ with the 0-3-space pattern `grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}'` "
     f"(registry {L}/corpus/SOURCES.md vs merge/kengaku/SOURCES.append.md; `comm -12`); prove the guard on a scratch registry with "
     f"an indented `  | S002 |` row; any staged entry in PROVINCE scope on uncovered ground (LLM eval / benchmark graders)? "
     f"Recommend adopt/none.",
     "VERDICT: merge-<changed|unchanged>-collisions-<n>-recommend-<adopt|none>"),
    ("R44Quarantine", "executor", ["discernment"],
     f"Quarantine slice: derive the kengaku data rows of /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/"
     f"absent-defect-register.md (lane cell `kengaku`, round cell, S-id cell — never the summary rows); for each row fetch the "
     f"cited source and try to locate the quote; verdict fabrication / unverifiable / present-with-anchor. Read-only on shokuknow.",
     "VERDICT: quarantine-rows-<n>-present-<p>-absent-<a>"),
    ("R44ScoutMisroot", "scout", ["safety", "hygiene"],
     f"Hygiene watch: record `ls -la --time-style=full-iso /home/vgpnk/.local/bin` + dir mtime at start and end; `git -C {F} status "
     f"--porcelain --untracked-files=all` — any file a kengaku round-44 seat wrote into the fleet root? Scratch dirs under {SCR} "
     f"with sizes; {SCR}/.ROUND-ROOT-SENTINEL present at start/end? Report only; touch nothing.",
     "VERDICT: misroot-<n>-host-writes-<h>-sentinel-<present|missing>"),
    ("R44PlanNext", "scout", ["calibration", "coverage"],
     f"Round-45 data walk (read-only): (a) calibration: price the 17 reachable `round_close.py` survivors ({B43}/R43PlanNext.md "
     f"§A.3) under the round-44 counter contract (exact argv shape F3, stub order tool + stub census needs) — which are reachable "
     f"from nothing?; (b) coverage: the next uncovered TB2 class from {B43}/R43ConsiderThese.md (D1 query-optimize needs a 50.6 MB "
     f"download; O1/W1/V1?) or a second F1 task with a different grader shape — check offline feasibility from pinned files. Write "
     f"numbers and commands.",
     "VERDICT: plan45-calibration-<n>-coverage-<task>"),
    ("R44ExecNoHarm", "executor", ["calibration", "operability"],
     f"{HOST_RULE}\n\nNo-harm baseline at the receipt commit {FIRST}: in a clean `--no-local` clone, inside the envelope, adapt "
     f"{L}/.ufo/waves/round-43/integrate/measure.sh into {B}/R44ExecNoHarm/measure.sh (round-44 counters first: round44_c1_verify.py, "
     f"round44_c2_verify.py, order_check.py round 44; then everything round 43 measured: rounds 36-43 counters, anchor check, census, "
     f"frozen digests r39-r44, ledger_tip, tip_receipts, routed_open, the db_wal/constraints/fibsqrt/feal probes byte-equal, "
     f"round_close.py --round 42/43/44, gate_flip_check on round-42/43 lessons) and run it; paste every verdict line + exit. Expect "
     f"round-44 counters red here. The script must take the clone path and a --work dir as arguments.",
     "VERDICT: no-harm-baseline-<k>-green-of-<n>"),
    ("R44ExecShapeDiff", "executor", ["calibration"],
     f"Write {B}/R44ExecShapeDiff/shape_diff.py (stdlib): given a battery dir and {WIT}, report for every fixture function a "
     f"normalised-AST similarity to every witness fixture (difflib ratio on ast.dump with names/constants normalised) and flag "
     f"pairs above 0.8 — the non-author 're-spelling' screen the counter cannot do. Selftest: the witness against itself (flags all), "
     f"against {L}/plans/battery43 (expect low). Paste outputs.",
     "VERDICT: shape-diff-selftest-<ok|fail>"),
    ("R44SimplifyCounters", "simplifier", ["operability"],
     f"YAGNI review (no edits): the C2 counters {L}/plans/round3*_c2_verify.py ... {C2} are near-copies per round "
     f"(considerthese/2026-10-26.md proposal 2). Measure the duplication (diff line counts round42→43→44), and sketch the smallest "
     f"standing counter (spec-driven) that would replace the per-round copies without relaxing any leg; list what must stay "
     f"per-round (DECISIVE, predicates). Report only.",
     "VERDICT: c2-counter-duplication-<pct>"),
    # ---- connectors ----
    ("R44ConnSibling", "connector", ["adjacency"],
     f"Sibling overlap scan: do sibling lanes ({F}/*-shokunin/PROVINCE.md, corpus/README.md) own cryptanalysis, benchmark-grader "
     f"auditing, answer-leak detection, or mutation-attributed gate testing? Name owners, overlaps, and what kengaku should route "
     f"rather than absorb for the round-44 package and counters.",
     "VERDICT: sibling-overlap-<n>"),
    ("R44ConnPattern", "connector", ["calibration", "quality"],
     f"Cross-claim pattern: C1's 'advertised-vs-demonstrated' count and C2's 'the grader checks less than the instruction states' "
     f"are the same shape (a self-description vs observed behaviour). Find other sites in the lane (gates, probes, SCORECARD rows) "
     f"where a docstring/README advertises a check no test demonstrates; list with file:line. Cheap static evidence only.",
     "VERDICT: pattern-<n>-sites"),
    ("R44ConnFrontier", "connector", ["coverage"],
     f"Frontier map: from {L}/corpus/README.md (coverage map, `## Frontier`) and the ten TB2 graders read so far, which grader "
     f"classes remain uncovered and what would a 64-seat round need to cover two of them? Cross-check against "
     f"{B43}/R43ConsiderThese.md's histogram; say whether `{TASK}` is genuinely new ground (not a re-read of feal-differential).",
     "VERDICT: frontier-<new|not-new>-uncovered-<n>"),
    ("R44ConnClaims", "connector", ["calibration"],
     f"Cross-document drift: compare {CLAIMS}, the counters' docstrings, {CL}/frozen-digests.txt, the SCORECARD `### Planned (round "
     f"44)` block and this wave's context for contradictions (mutant counts, case counts, row ids, predicates, envelope wording). "
     f"List each drift with both locations. You MUST write your report file.",
     "VERDICT: drift-<n>"),
    ("R44DistillRouted", "simplifier", ["quality"],
     f"Deduplicate the open rows of {ROUTED} (`python3 {L}/plans/routed_open.py --lane {L} --list`): group rows that describe the "
     f"same defect or would be closed by one fix; output groups with row ids and the single fix each needs. Read-only.",
     "VERDICT: routed-groups-<g>-from-<n>"),
]

FLASH = {"executor", "labrat", "scribe", "sonic", "simplifier", "revenger", "sentinel"}
ATTACK = {"reviewer", "critic", "mutation-tester", "labrat"}


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 44 wave item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r44 wave (build + attack, v2)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    c = Counter(i["role"] for i in items)
    flash = sum(n for r, n in c.items() if r in FLASH)
    attack = sum(n for r, n in c.items() if r in ATTACK)
    assert 64 <= len(items) <= 128, len(items)
    assert flash * 2 >= len(items), f"m_flash share {flash}/{len(items)} below half"
    assert attack * 4 >= len(items), f"attack share {attack}/{len(items)} below a quarter"
    spec = {"wave": "kengaku-r44-wave",
            "milestone": "kengaku round 44 v2 wave: C1 battery44 for 5 u-row mutants under fences F1-F6, C2 TB2 feal-linear "
                         "admission with V11, closure R1-R5, routed burn-down",
            "reportDir": ".ufo/waves/round-44/wave", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/wave-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    print(len(items), dict(c))
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
