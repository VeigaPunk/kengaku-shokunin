#!/usr/bin/env python3
"""Renders .ufo/waves/round-39/build-spec.json (wave 1 of 2, policy v1)."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-39"
B = f"{W}/build"
SCR = "/fast/scratch/hyaku/kengaku-r39"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/git-leak-recovery"
CAP = f"{L}/corpus/evidence/round39/tb2-git-leak-recovery"
RCPT = f"{L}/corpus/evidence/round39/git-leak-probe.txt"
DRY = f"{L}/corpus/evidence/round39/git-leak-dry-cases-freeze.txt"
C1 = f"{L}/plans/round39_c1_verify.py"
C2 = f"{L}/plans/round39_c2_verify.py"
PROBE = f"{L}/plans/git_leak_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
SPEC = f"{L}/plans/pkg-spec-r39.json"
CLAIMS = f"{L}/plans/round-39-claims.md"
F38 = f"{L}/.ufo/waves/round-38/falsify"
B38 = f"{L}/.ufo/waves/round-38/build"
SPOT = f"{L}/corpus/lessons/round-38-verifier-spotcheck.md"
LES38 = f"{L}/corpus/lessons/round-38.md"
FREEZE = "088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8"
FIRST = "6a1eb5e1da4a435940b821e28530c31f3411549c"
CLONE = (f'Fixture rule: S={SCR}/<YourSeatName>; mkdir -p "$S"; trap \'rm -rf -- "$S"\' EXIT; export TMPDIR="$S"; '
         f'git clone -q --shared {L} "$S/lane"; verify `git -C "$S/lane" rev-parse --show-toplevel` equals "$S/lane" before any '
         f'write; every git call names -C "$S/lane"; never commit (index-only `git add` inside YOUR clone is fine — the gate\'s P9 '
         f'needs drafts staged). Any other fixture repo: D=$(mktemp -d -p "$S") && git -C "$D" init -q, and every git call names '
         f'-C "$D". Remove "$S" before you finish (copy receipts into your report dir first).')

CONTEXT = f"""# Goal
kengaku round 39 (hyaku run 8, 2026-10-26), WAVE 1 of 2 (build + first falsifiers). Lane repo: {L}.
Two claims are FROZEN at {CLAIMS} (freeze commit {FREEZE}; first recorded probe run {FIRST}) — read it first, in full.
Nothing frozen may change: not the gate {GATE}, not the counters {C1} / {C2}, not the probe {PROBE}, not the spec {SPEC},
not the dry table {DRY}, not the captures {CAP}/, not the receipt {RCPT}, and not any file the C1 counter pins (its PINS
dict: round36/round37 counters, battery37 and battery38 modules, pkg-spec-r35.json, attribution audit).
- C1 calibration: 7 frozen mutants M01-M07 of the gate (MUTANTS table in {C1}: clause, direction, advertised behaviour,
  pre-freeze witness, `old -> new`). At freeze the round-36/37/38 battery kills 3/7 (M01, M05, M06) under the ATTRIBUTED kill
  rule ({W}/claims/control-c1-nothing.txt); M02 (P1 silence), M03 (P3 silence), M04 (P7 silence), M07 (D5 mirror) survive. The
  work: battery39 modules until `python3 plans/round39_c1_verify.py --lane .` prints `MUTANTS total=7 killed=7 survived=0
  invalid=0 null_detected=0`. Module contract (counter docstring, = battery38's): module-level FIXTURES = [{{"fid", "expect":
  "accept"|"reject"|"error", "defects": [exact DEFECT clause ids the UNMODIFIED gate prints; [] for accept/error], "build":
  build}}]; build(ctx, d) fills the EMPTY directory d and returns the gate argv tail. ctx is the round-37 counter's Ctx
  ({L}/plans/round37_c1_verify.py:189-217): ctx.genuine_package(d) git-inits d and copies the genuine round-35 package
  (ctx.spec = {L}/plans/pkg-spec-r35.json as a dict), ctx.git_add(d) stages index-only, ctx.r36 = the round-36 counter module,
  ctx.d4_line(), ctx.d5_line(), ctx.d5_capture_dir(). Package argv: ["package", "--root", str(d), "--require-clean-tree"]; a
  fixture MAY add "--spec", <a json file it wrote INSIDE d> (derive it from a deep copy of ctx.spec), else the frozen r35 spec is
  appended. Modules are imported and built in a CHILD process; only JSON (fid, expect, defects, argv) comes back. Module source
  must not contain `/proc`, `ppid`, `cmdline`, `psutil`, `environ`. Battery38 examples: {L}/plans/battery38/*.py. Develop with
  `python3 {C1} --lane "$S/lane" --battery-dir <your battery dir> --only <your ids> --work "$S/w"` (prints `PREDICATE C1 n/a`).
- C2 coverage: pinned Terminal-Bench 2.0 `git-leak-recovery` grader (terminal-bench-2 @ {PIN}) to be admitted as
  corpus/knowledge/tb2-git-leak-recovery-grader.md with rows S117 (tests/test_outputs.py) and S118 (instruction.md). Captures
  {CAP}/ (test_outputs.py, instruction.md, challenge-setup.sh, solve.sh = oracle, test.sh, task.toml, Dockerfile) + SHA256SUMS.
  Receipt {RCPT}: `cases=25 observed_pass=13 observed_fail=12 mismatches=0`, second run byte-equal. Counter {C2} = round-38's
  V1-V7 re-pointed (docstring): V2 runs the gate with --rerun --require-clean-tree over {SPEC}; V7 derives each requirement-map
  label from ALL receipt cases whose `violates=` carries the tag (all fail → enforced, all pass → unenforced, mixed → partly); map
  row | `instruction.md:<L>` | `<tag>` | <label> | `case-id`, ... | with the tag's frozen line from the dry table's TAG lines.
  Headline observations of the receipt: the untouched initial repo fails only the flag test (4/5 pass); writing the literal
  alone passes 5/5 while the secret commit stays in the reflog/object store (`echo-only`, `echo-gc-only`, `echo-reflog-expire`);
  a ref pinning the secret blob, an annotated tag message, a stash, a dot file, .git/config all pass 5/5; a dangling blob or a
  dangling commit whose message carries the secret fails test 4; rewritten tip message and a rebuilt one-commit history pass.
- Round-38 closure routed items: {SPOT} section 5 (R1-R7). Round-38 wave-2 reports (uncommitted; a few seats may still be
  writing): {F38}/*.md. Round-38 wave-1 reports: {B38}/*.md.

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report dir is {B}/; drafts and receipts go under {B}/<YourSeatName>/ (create it). Never copy a corpus/ or
  plans/ tree, a lane mirror, or a clone into {B}/.
- Scratch (operator directive 2026-10-25): clones, fixtures and work trees live ONLY under {SCR}/<YourSeatName>/ (NVMe), never
  under /tmp; pass it explicitly (export TMPDIR, --work); delete it before you finish (`trap 'rm -rf -- "$S"' EXIT`).
- Write ONLY inside {B}/ (your report + your own subdir) and your scratch dir. NEVER edit the lane's corpus/, plans/,
  SCORECARD.md, LOG.md, README.md, SKILL.md, PROVINCE.md, SHONEN.md or any other lane file — draft for the L1, who integrates.
  Never write into {F} (fleet root), sibling lanes, the lane's jj state, or the lane's Git index. Never run git
  add/commit/stash/checkout/reset/push/pull or any mutating jj command in the lane.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY: never write/commit/fetch there; run none of its campaign tools.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide:
  install via `uv tool` / `npx` / an official binary into ~/.local/bin, or file nothing and say so. Never run pacman
  -Sy/-Syu/-U/-R, never name an already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat probe).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location (file:line or
  URL+section) and is <= 25 words. Do not fabricate output; if something cannot be fetched or run, say so.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""


def bat(name, module, mid, hints):
    return (name, "executor", ["calibration", "operability"],
            f"Write the C1 battery39 module {B}/{name}/battery/{module}.py (stdlib only; every fid starts `{module}-`) whose "
            f"fixtures ATTRIBUTABLY kill frozen mutant {mid} of {C1} in its declared direction (read its `old -> new`, direction and "
            f"witness there, and the gate branch in {GATE}). Each fixture's `defects` must equal the exact DEFECT clause set the "
            f"UNMODIFIED gate prints on it, and its `expect` must match the reference exit code. Hints: {hints} Prove it in your clone: "
            f"`python3 {C1} --lane \"$S/lane\" --battery-dir {B}/{name}/battery --only {mid} --work \"$S/w\"` must print every FIXTURE "
            f"line of your module `ok`, `renamed_disagree=0 sidechannel=0`, `null_detected=0`, and `{mid} ... killed by=<your fid>`. "
            f"Paste that output. Then delete each fixture in turn and confirm {mid} flips to SURVIVED (load-bearing table). Finally run "
            f"the FULL default counter in your clone with your module copied to \"$S/lane/plans/battery39/\" and paste its MUTANT and "
            f"summary lines. Report the module's sha256.",
            f"VERDICT: battery39-{module}-{mid}-<killed|survived>-wrong-<w>")


ITEMS = [
    # ---- C1 battery39 executors (4) ----
    bat("R39BatP1", "p1m", "M02",
        f"P1 checks `frozen_instruments` pins; every existing fixture corrupts only the FIRST pin (round36 stub_probe on "
        f"spec['probe_cmd'][0]). Corrupt a NON-first pinned instrument (fixture-owned spec over the genuine package whose second pin "
        f"names a file in d with a wrong digest, or a staged second instrument file whose bytes differ). Witness W-X01: "
        f"{F38}/F38XMutP/witness.py and witness-run.txt."),
    bat("R39BatP3", "p3m39", "M03",
        f"P3 bounds quote word counts by entry_rules.quote_words [3, 25]; the only word-range fixture is below the bound. Build a "
        f"quote of exactly 26 words (one above the upper bound) — note that P4 (verbatim) may also fire unless the 26-word text is "
        f"verbatim on its cited capture lines; declare exactly what the reference prints. Witness W-X05 in {F38}/F38XMutP/."),
    bat("R39BatP7", "p7m39", "M04",
        f"P7 requires `prov.get(sid) == [pinned url]` — exactly one `source: S### <url>` line per spec row. Give one sid TWO source "
        f"lines (the pinned URL twice, or pinned then another), so the reference prints P7 DEFECT and the mutant (first line only) "
        f"does not. Witness W-X15 in {F38}/F38XMutP/."),
    bat("R39BatD5", "d5m39", "M07",
        f"M07 is a MIRROR: an ACCEPT d5-line fixture whose capture carries markup (e.g. `<b>`...`</b>`) INSIDE the quote span, with "
        f"the manifest re-pinned to the new capture digest, so the reference prints `D5 ok` (tags stripped before the flat compare) "
        f"and the mutant prints `D5 DEFECT`. The fixture must own its capture dir inside d (argv d5-line --file <line> --capture-dir "
        f"<dir in d> [--spec <spec in d>]); see {L}/plans/battery38/d5m.py and {F38}/F38XMutRerunMain/survivor-probeB.txt."),
    # ---- C1 attacks ----
    ("R39CritC1Counter", "critic", ["calibration"],
     f"Attack {C1}: (1) can a battery39 module reach `killed=7` without a fixture that honestly exhibits each behaviour — e.g. write "
     f"into the counter's scratch after its child exits (a forked/daemonised process, an atexit hook, a file planted where a later "
     f"gate copy or fixture dir lands), poison `--spec` paths, exploit the rc-silence/rc-mirror legs with a fixture whose declared "
     f"expect disagrees with its intent, or reuse an fid? Build each attack as a module in YOUR clone's plans/battery39/ and run the "
     f"full counter; (2) does the out-of-process build actually prevent the round-38 in-process `run_gate` patch (freeze control "
     f"{W}/claims/control-c1-hostile-inproc.txt) — try a stronger variant; (3) are the 26 pins all inputs the counter reads? Report "
     f"each attack's MUTANTS line.",
     "VERDICT: c1-counter-attacks-<reached>/<tried>"),
    ("R39CritC1Equiv", "critic", ["calibration"],
     f"Q29 check at the first integration, before battery39 lands: for M02, M03, M04, M07 re-run the round-38 witness inputs "
     f"({F38}/F38XMutP/witness.py, {F38}/F38XMutRerunMain/survivor-probes.txt, survivor-probeB.txt) against the frozen gate and the "
     f"{C1} mutant text (apply `old -> new` yourself in your clone) and confirm each declared direction is reachable; try to prove "
     f"any of the 7 observationally equivalent at (exit code, DEFECT set) granularity. Also re-check M01/M05/M06's control kills "
     f"(`killed by=` fixtures in {W}/claims/control-c1-nothing.txt) are honest exhibits of their direction, not artefacts.",
     "VERDICT: c1-directions-reachable-<k>/7-equivalent-<e>"),
    ("R39CritClaims", "critic", ["calibration"],
     f"Attack the claims' framing in {CLAIMS}: is C1 a calibration move — map each M01-M07 `adv` cell to the exact advertising "
     f"sentence (file:line in {GATE} docstring, {L}/corpus/QUALITY.md Q24/Q27, {L}/SCORECARD.md:564) or mark it unadvertised; are "
     f"3 of 7 already killed at control a sign the target is soft; is C2's class (repository-history state) new against "
     f"{L}/corpus/README.md's coverage map; separability; universal clauses; any number in the claims that does not reproduce.",
     "VERDICT: claims-attack-<n>-defects-unadvertised-<k>"),
    ("R39RevCounters", "reviewer", ["calibration", "operability"],
     f"Code review of {C1}, {C2} and {PROBE}: correctness bugs, false-green/false-red paths, determinism, TMPDIR/--work honoured (no "
     f"/tmp), pins complete, the C1 child-process contract (what a module still controls), the rc legs vs the docstring, the probe "
     f"sandbox (writable /app bind, GIT_CONFIG_* isolation, setup/recipe failure → exit 2, nothing host-specific printed). Cite "
     f"file:line.",
     "VERDICT: review-<n>-defects"),
    ("R39RevFreeze", "reviewer", ["calibration"],
     f"Freeze-order audit: `git -C {L} log --format='%H %cI %s' b2bdd425..master`; confirm {FREEZE} carries claims, counters, probe, "
     f"dry table, captures and controls and NO receipt (`git cat-file -e {FREEZE}:corpus/evidence/round39/git-leak-probe.txt` must "
     f"fail); the receipt landed in {FIRST}; frozen-digests.txt matches `git show {FREEZE}:<path> | sha256sum`; re-run "
     f"control-c1-nothing and control-c2-nothing on a clean clone of {FREEZE} and diff with the committed files; check the claims' "
     f"order-of-operations disclosure (did any committed control execute the probe? `P10` lines).",
     "VERDICT: freeze-audit-<ok|n-defects>"),
    # ---- C2 package ----
    ("R39PkgEntry", "scribe", ["coverage", "depth"],
     f"Draft the C2 package for the L1 under {B}/R39PkgEntry/: (1) entry.md = corpus/knowledge/tb2-git-leak-recovery-grader.md "
     f"(follow the shape of {L}/corpus/knowledge/tb2-build-pmars-grader.md: `source: S117 <raw url>` / `source: S118 <raw url>` lines "
     f"with the EXACT pinned raw URLs {RAW}/tests/test_outputs.py and {RAW}/instruction.md, `verified-at: 2026-10-26`, a `recheck:` "
     f"line whose command runs green AS WRITTEN from the lane root (`(cd corpus/evidence/round39/tb2-git-leak-recovery && sha256sum "
     f"-c SHA256SUMS)` — round-38 closure R4); sections: what is graded; `## Located quotes` table rows | claim | “quote” | "
     f"`capture:line` | with >=8 distinct verbatim 3-25-word quotes at >=8 distinct lines of {CAP}/test_outputs.py and "
     f"instruction.md (check each with sed -n); `## Requirement map` with exactly one row per TAG in {DRY} in the frozen format, label "
     f"DERIVED from {RCPT} as V7 does, citing violating case ids; findings each tied to receipt case ids; limits (host git 2.56 vs the "
     f"image's Ubuntu git, setup unprivileged, image never pulled, the oracle row's static-vs-pilot note); prior art from "
     f"{B}/R39ScoutPriorArt.md if present when you write (else leave a marked placeholder line for the L1) — claim a probed instance "
     f"only; `## Negative space` with an explicit falsifier). (2) rows.md = two 11-cell SOURCES rows S117/S118 in {L}/corpus/SOURCES.md's "
     f"exact column order (read its header and S115/S116), tier A, status mined, opened 2026-10-26, anchor cell `sha256 <pin>` + a "
     f"<=25-word located quote, teaches >= 8 distinct words, used-by = corpus/knowledge/tb2-git-leak-recovery-grader.md. (3) readme.md "
     f"= the index row + one coverage bullet naming the entry and `round39/git-leak-probe.txt`. PROVE it: in your clone place the "
     f"drafts, `git -C \"$S/lane\" add -A`, run `python3 {C2} --lane \"$S/lane\" --work \"$S/w\"` → paste output; iterate until "
     f"`checks=7 defects=0`.",
     "VERDICT: c2-package-draft-checks-7-defects-<n>"),
    ("R39PkgProse", "scribe", ["coverage", "depth", "adjacency"],
     f"Draft paste-ready lane prose for C2 under {B}/R39PkgProse/: (a) a PROVINCE.md round-39 paragraph (read {L}/PROVINCE.md "
     f"round-35..38 paragraphs; same admission limits: grader probe only, image not pulled; repository-history state as a new graded-"
     f"state class); (b) the corpus/README.md §Frontier TB2 sub-bullet narrowed by one task (read the current clause; 5 of 89 read); "
     f"(c) a SKILL.md section 'Repository-history TB2 grader — round 39' as a decision table (what the grader reads → what passes → "
     f"what a reviewer should check instead), every row citing a receipt case id in {RCPT}; (d) registry rows for the round-39 tools "
     f"in the shape of SKILL.md's existing gate registry (round39-c1, round39-c2, git-leak-probe). Observations only; no class claims.",
     "VERDICT: c2-prose-drafted-<n>-rows"),
    ("R39ScoutPriorArt", "scout", ["novelty", "coverage"],
     f"Prior art for the git-leak-recovery grader findings. OPEN (not search snippets): harbor-framework/terminal-bench "
     f"`checks/test-tasks/fail-validate-nop` (or wherever nop validation lives) and `docs/TASK_REVIEW_AUTOMATION.md`; search "
     f"terminal-bench-2 / terminal-bench-2-1 / harbor issues+PRs (gh api / gh search) for git-leak-recovery, 'git fsck', 'dangling', "
     f"'reflog', 'secret'; the JonathanGabor/terminal-bench-2-audit repo's entry for git-leak-recovery if any; any third-party write-up "
     f"of this task's grader. For each hit: URL, date, state, <=25-word quote with location, and whether it reports this grader's "
     f"permissiveness (literal-only flag, reflog/object retention, nop 4/5) or something else. Propose at most one tier-B SOURCES row "
     f"for the strongest prior report, or say none qualifies. Reuse {B38}/R38PlanNext.md §2.5.",
     "VERDICT: prior-art-<n>-hits-row-<yes|no>"),
    ("R39ScoutUpstream", "scout", ["freshness", "coverage"],
     f"Upstream state of git-leak-recovery: compare all seven captures in {CAP}/ with terminal-bench-2 main (curl raw + sha256sum, "
     f"gh api commits?path=git-leak-recovery), check terminal-bench-2-1 (tasks/git-leak-recovery?) for the same files, and the docker "
     f"image tag in task.toml. Report drift (none/where) with commands and outputs.",
     "VERDICT: upstream-drift-<none|n>"),
    ("R39CritPytest", "critic", ["coverage"],
     f"Parity: run the REAL pytest 8.4.1 (uv venv -p 3.13 in your scratch, PyPI via uv) over {CAP}/test_outputs.py for each of the 25 "
     f"case states of {PROBE} (reuse its sandbox: copy the probe into your clone and replace the harness's grader call with "
     f"`python -m pytest /cap/test_outputs.py -rA` inside the same bwrap, the venv bound read-only), and compare per-test letters with "
     f"{RCPT}. Report agree/disagree per case.",
     "VERDICT: pytest-parity-<agree>/25"),
    ("R39CritIndep", "critic", ["coverage", "calibration"],
     f"Independent recompute: WITHOUT reading the probe's predictions, derive from {CAP}/test_outputs.py and git documentation alone "
     f"the expected five test outcomes for each of the 25 case descriptions (the `-- requirement` text + recipe in {PROBE}) and compare "
     f"with {RCPT}. Then build 3 EXTRA cases of your own (e.g. secret in a packed ref's reflog only, secret in refs/replace, secret in "
     f".git/lost-found, secret.txt as a symlink) in a copy of the probe in your clone, predict first, run, report.",
     "VERDICT: indep-agree-<k>/25-extra-<j>/3"),
    ("R39CritFsckReflog", "critic", ["coverage", "depth"],
     f"Explain the `oracle-solve-sh` and `untouched` rows: the probe docstring says a static reading of git fsck (reflogs count as "
     f"reachable by default) predicts the oracle should FAIL the flag test, yet the receipt shows pass. In a fixture repo built with "
     f"{CAP}/challenge-setup.sh under your scratch, run `git fsck --lost-found`, `git fsck --no-reflogs`, inspect .git/logs, and "
     f"find which object fsck reports dangling and why (cite git docs/source: Documentation/git-fsck.txt, builtin/fsck.c, by URL and "
     f"line). Would Ubuntu 24.04's git 2.43 behave the same (release notes / source diff; do not pull the task image unless docker is "
     f"already usable without root)? Draft a 3-sentence entry paragraph the L1 can paste.",
     "VERDICT: fsck-reflog-<explained|open>"),
    ("R39CritProbe", "critic", ["coverage", "calibration"],
     f"Attack {PROBE} and {RCPT}: is each case's `violates=` tag set right (contestable tags, as round-38 R38CritProbe did); does each "
     f"case text describe what its recipe actually builds (inspect the repo state per case in your clone: run the setup + recipe "
     f"yourself and look); which requirement-map labels would change under a contestable tag; is the `stash-secret` reasoning right "
     f"(git log -p -S on merge commits). List label changes and wording defects.",
     "VERDICT: probe-attack-<n>-defects-labels-change-<k>"),
    ("R39CritSkipC2", "critic", ["calibration"],
     f"Post-first-run skip-controls for C2 (the first recorded run {FIRST} already landed, so running the gate with --rerun is now "
     f"allowed): in your clone build (a) a junk entry/rows/README with correct anchors and a hand-typed receipt copied from `--dry` "
     f"with observed=predicted → `python3 {C2} --lane \"$S/lane\"` must stay red (which V?); (b) a probe copy whose CASES all predict "
     f"PPPPP must print mismatches>0 against the grader; (c) the round-38 informed-filler shape (R38CritC2Counter §1, {B38}/R38CritC2Counter.md) "
     f"— does it reach checks=7 defects=0 here too? Keep every receipt.",
     "VERDICT: c2-skip-controls-red-<k>/<n>"),
    ("R39MutProbe", "mutation-tester", ["coverage"],
     f"Mutation-test the probe's sensitivity in a copy (never the lane file): harness maps every exception to P; setup skipped for "
     f"every case; GIT_CONFIG_NOSYSTEM dropped; recipe failures ignored; /app bound read-only; one case's recipe swapped with "
     f"another's. For each, does the receipt change and would C2 V4/V5/V2-P10 catch it? Report.",
     "VERDICT: probe-mutants-<caught>/<total>"),
    ("R39MutC2Counter", "mutation-tester", ["calibration"],
     f"Mutation-test {C2}'s checks in a clone where a passing package exists (use {B}/R39PkgEntry/ drafts if present when you start; "
     f"else build a minimal genuine package yourself from {CAP} and {RCPT}). One mutant at a time: map label flipped; map row citing a "
     f"non-violating case; tag duplicated; tag missing; map line number wrong; S117 anchor token replaced by S118's digest; one CASE "
     f"line deleted from the receipt; spec one byte; dry table one byte; probe one byte; a capture one byte. Report caught/survived "
     f"per mutant with the DEFECT line.",
     "VERDICT: c2-mutants-<caught>/<total>"),
    # ---- frontier / routed ----
    ("R39R38Integrate", "scribe", ["calibration", "quality"],
     f"Round-38 closure R1: map EVERY round-38 wave-2 report {F38}/*.md (and note seat dirs with no .md) to a disposition for the L1: "
     f"finding → (fixed this round by item X / routed to round 40 / limit only / no action, reason). Group by the closure's routed "
     f"items R1-R7 ({SPOT} §5). Output a table under {B}/R39R38Integrate/dispositions.md plus counts (reports, findings, by "
     f"disposition). Read-only.",
     "VERDICT: r38-wave2-mapped-<reports>-findings-<n>"),
    ("R39OrderGate", "executor", ["calibration", "operability"],
     f"Round-38 closure R3 + considerthese/2026-10-25.md proposal 2(b): write {B}/R39OrderGate/order_check.py (stdlib; proposed lane "
     f"path plans/order_check.py) — `python3 plans/order_check.py --lane . --claims plans/round-NN-claims.md --receipt <path>` reads "
     f"git history (read-only) and FAILS (exit 1) when any file committed under .ufo/waves/round-NN/claims/ at or before the first "
     f"commit adding <receipt> shows the frozen probe executed (a gate `P10` line other than `P10 DEFECT receipt unreadable`, or a "
     f"receipt-shaped `CASE ... observed=` line), and when the freeze commit (the commit adding the claims file) already contains the "
     f"receipt; exit 0 otherwise, exit 2 on setup errors. Show it RED on round 38 (claims plans/round-38-claims.md, receipt "
     f"corpus/evidence/round38/build-pmars-probe.txt — control-c2-skip.txt carries a P10 line) and GREEN on round 39 (receipt "
     f"corpus/evidence/round39/git-leak-probe.txt), both on a clean clone; also round 37 (corpus/evidence/round37/*probe*.txt — find "
     f"it). Draft the {L}/corpus/defects.jsonl row (read its schema first) for the class with recurrence=2 and the gate as its check.",
     "VERDICT: order-gate-r38-<red|green>-r39-<red|green>"),
    ("R39LessonErrata", "scribe", ["calibration"],
     f"Round-38 closure R3 text: `F38RevLesson` ({F38}/F38RevLesson.md) found the round-38 lesson ({LES38}) row 2 misstates the "
     f"round-37 fix (Defect 1) and lists census-before.txt among 'all red' controls (Defect 2). Verify both against the files and "
     f"draft an appended `## Errata (round 39)` block for the round-38 lesson (append-only, never rewrite) plus a 2-line Mistakes-row "
     f"draft for the round-39 lesson naming the recurrence and its gate.",
     "VERDICT: lesson-errata-<n>-verified"),
    ("R39RecheckFix", "scribe", ["freshness", "quality"],
     f"Round-38 closure R4: the recheck commands in the round-35..38 TB2 entries ({L}/corpus/knowledge/tb2-*.md) red as written from "
     f"the lane root (bare basenames in SHA256SUMS). For each entry: run its recheck line verbatim from a clean clone root (paste "
     f"output), write the corrected one-line command, run it (paste green output), and draft an appended `## Errata (round 39)` "
     f"line per entry. Also F38R-3 (TB2.1 comparison unpinned) — pin the comparison or say why not.",
     "VERDICT: recheck-red-<n>-fixed-<k>"),
    ("R39AnchorUnion", "executor", ["calibration", "operability"],
     f"Round-38 closure R5a: `plans/anchor_digest_check.py` unions digests over every locator a row names (`F38AnchorFix` F1, "
     f"{F38}/F38AnchorFix.md). Write a fixed copy {B}/R39AnchorUnion/anchor_digest_check.py binding each digest token to the capture "
     f"its own locator names; show the current tool green on a fixture where a multi-locator row carries the WRONG locator's digest "
     f"(red-before), your copy red on it, and your copy at the lane tip `rows=... defects=0` (no false red). Paste all receipts.",
     "VERDICT: anchor-union-red-before-<yes|no>-tip-defects-<n>"),
    ("R39LedgerProvenance", "executor", ["operability"],
     f"Round-38 closure R5b: `plans/ledger_tip.py --lane` reads an existing but stale `refs/heads/master` with no provenance line "
     f"(`F38LedgerTip` F1/F2, {F38}/F38LedgerTip.md). Write a fixed copy {B}/R39LedgerProvenance/ledger_tip.py that prints which "
     f"revision it audits and refuses (exit 2) a stale local master that is not the commit under audit; show red-before on a "
     f"fixture clone with a stale master and green at the lane tip (`rows=9 closed=9 ... mismatches=0`). The pinned check bodies "
     f"stay unedited.",
     "VERDICT: ledger-provenance-red-before-<yes|no>"),
    ("R39DirCheckLeg", "executor", ["calibration", "operability"],
     f"Round-38 closure R2 (last clause): `plans/mutant_direction_check.py` has one mislabel signal path (`F38MutDirection`, "
     f"{F38}/F38MutDirection.md: mutants m1, m2 survive). Write a fixed copy {B}/R39DirCheckLeg/mutant_direction_check.py with a "
     f"redundant leg so m1 and m2 are caught; show the three F38MutDirection mutants against the old and new copy, and the new copy "
     f"still prints `N21 ... MISLABELLED` (exit 1) at the lane tip.",
     "VERDICT: direction-check-mutants-<caught>/3"),
    ("R39AdvErrata", "scribe", ["calibration"],
     f"Round-38 closure R2 wording: `F38CritBatE` D1/D2 ({F38}/F38CritBatE.md) say N11's and N09's `adv` sentences overstate what the "
     f"frozen gate enforces; R38CritClaims ({B38}/R38CritClaims.md §1) found 3 of 22 `adv` cells name no advertising sentence; "
     f"`F38CritBatF` ({F38}/F38CritBatF.md) 2 defects; `F38SentinelBattery` ({F38}/F38SentinelBattery.md) findings. Verify each "
     f"against the files and draft (a) an appended round-39 erratum line per item for SCORECARD's round-38 section, (b) which of them "
     f"the round-39 C1 `adv` cells repeat (check {C1}).",
     "VERDICT: adv-errata-<n>-verified-<k>"),
    ("R39QualityQ30", "scribe", ["calibration", "quality"],
     f"Draft QUALITY.md Q30 for {L}/corpus/QUALITY.md (read Q24-Q29 shape: bold rule, evidence, an executable check shown able to "
     f"fail): 'a mistake class that recurs twice gets a gate that reads committed history, not another rule' — evidence: the order-"
     f"of-operations class in round-37 lesson row 3 and round-38 lesson row 2, the round-38 closure R3; check: the order gate from item "
     f"R39OrderGate (read {B}/R39OrderGate.md if present; else write the check sentence with the command it will have). Also scan "
     f"{SPOT} §3 for any disagreement needing a criterion (it reports 0; confirm).",
     "VERDICT: q30-drafted"),
    ("R39SourcesRecheck", "scout", ["freshness"],
     f"SOURCES curation: in {L}/corpus/SOURCES.md find rows whose `recheck` date is on or before 2026-10-26 (or whose cadence is due); "
     f"open up to 4 of them live this round (URL, access date, <=25-word located quote, sha256 where the row pins one) and draft each "
     f"row's status/recheck change old→new with the evidence. Also explain the 15 W04 census warnings "
     f"({W}/claims/census-before.txt): fix-worthy or by design (CORPUS.md census clause).",
     "VERDICT: sources-rechecked-<n>-changes-<k>"),
    ("R39MergeRescreen", "scout", ["coverage", "adjacency"],
     f"Assimilation re-screen of /home/vgpnk/Projects/shokuknow/merge/kengaku/ (READ-ONLY): changed since round 38's screen "
     f"({B38}/R38MergeRescreen.md)? `git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %cI' -- merge/kengaku`. Run the id "
     f"collision check exactly as the round prompt gives it (0-3-space pattern) with outputs under {B}/R39MergeRescreen/ (reg-ids, "
     f"staged-ids, collisions) and prove the guard on a scratch registry with an indented `  | S002 |` row; derive the quarantine "
     f"slice from /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (data rows only). Verdict per "
     f"entry admit/hold/refuse with PROVINCE scope reasons.",
     "VERDICT: merge-rescreen-admit-<a>-hold-<h>-refuse-<r>"),
    ("R39PlanNext", "scout", ["calibration", "coverage", "novelty"],
     f"Round-40 planning data walk (the L1 holds the planner seat; you supply data): price two candidates with a control executed "
     f"now — calibration: the tripwire-tool mutants ({B38}/R38PlanNext.md §3, re-priced after round-38 D3/D4 and this round's R5 "
     f"fixes); coverage/novelty: the next TB2 grader class not yet read (db-wal-recovery, openssl-selfsigned-cert, others from the 89 "
     f"tasks) with offline executability and quote supply measured; and a novelty candidate the round-38 seat did not price. Draft a "
     f"paste-ready `### Planned (round 40)` block.",
     "VERDICT: plan40-drafted"),
    ("R39ConnSibling", "connector", ["adjacency"],
     f"Sibling-overlap scan for this round's surfaces (git secret recovery/removal graders, git object-store forensics, bwrap grader "
     f"sandboxes, gate mutation batteries) across /home/vgpnk/Projects/shokunin/*-shokunin (read-only: PROVINCE.md, SKILL.md, "
     f"corpus/README.md) — secrets/vault (kagi), security research (kasegi), git tooling lanes. Name each overlap with file:line and "
     f"whether kengaku should cite, defer or report it out.",
     "VERDICT: sibling-overlap-<n>"),
    ("R39ConnPattern", "connector", ["calibration", "quality"],
     f"Cross-claim pattern finding: the git-leak grader inspects only dangling TIPS (not unreachable interiors), skips dot paths, and "
     f"`--all` never sees unreferenced objects; the gate survivors are 'first item only', 'off-by-one', 'loosened compare', 'pass side "
     f"never exercised'. Do the lane's own tools (plans/round39_*.py, plans/git_leak_probe.py, plans/anchor_digest_check.py, "
     f"plans/ledger_tip.py, plans/tip_receipts.py) carry any of these shapes (checks only the first/tip item, skips hidden files, "
     f"reads only referenced state)? List with file:line and a one-line fixture that would expose each.",
     "VERDICT: pattern-<n>-sites"),
    ("R39ConnFrontier", "connector", ["coverage", "calibration"],
     f"Frontier/coverage check: read {L}/corpus/README.md (coverage map + §Frontier) and {L}/PROVINCE.md; is 'repository-history "
     f"state' ground the lane did not hold (vs the four TB2 graders already admitted)? Which exact frontier clause narrows and what "
     f"should it read after; does any self-assessment line in SCORECARD/SHONEN/README now mismatch the repo state (count them, "
     f"file:line) — the round's calibration denominator outside C1.",
     "VERDICT: frontier-<new|not-new>-mismatches-<n>"),
    ("R39SentinelProbe", "sentinel", ["operability"],
     f"Security review: {PROBE} runs the captured solve.sh and per-case bash recipes inside bwrap with a WRITABLE /app bind; {C1} runs "
     f"battery module code in child processes with the counter's privileges. Can a case, recipe or module write outside its scratch, "
     f"reach the network, read ~/.ssh or the lane's .git, or leave processes behind? Test cheaply in your scratch; cite file:line.",
     "VERDICT: sentinel-<n>-findings"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 39 wave 1 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r39 wave 1 (build + first falsifiers)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    spec = {"wave": "kengaku-r39-build",
            "milestone": "kengaku round 39 wave 1: C1 battery39 for 4 surviving gate mutants, C2 TB2 git-leak-recovery admission, frontier step",
            "reportDir": ".ufo/waves/round-39/build", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/build-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c))
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"] + c["sentinel"]
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
