#!/usr/bin/env python3
"""Renders .ufo/waves/round-45/w1-spec.json (v1 wave 1 — build, policy v1 band 32-64). L1 KengakuR45.

Two v1 waves this round (round-size directive 64-128): wave 1 builds the fence implementation, the C2 package
drafts and evidence, and first attacks on the frozen instruments; wave 2 falsifies what wave 1 produced on the
landed tree. m_flash-routed roles must carry >= half, attack roles >= a quarter."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-45"
B = f"{W}/w1"
SCR = "/fast/scratch/hyaku/kengaku-r45"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
TASK = "password-recovery"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/{TASK}"
CAP = f"{L}/corpus/evidence/round45/tb2-{TASK}"
RCPT = f"{L}/corpus/evidence/round45/password-recovery-probe.txt"
DRY = f"{L}/corpus/evidence/round45/password-recovery-dry-cases-freeze.txt"
C1 = f"{L}/plans/round45_c1_verify.py"
C2 = f"{L}/plans/round45_c2_verify.py"
K44 = f"{L}/plans/round44_c1_verify.py"
PROBE = f"{L}/plans/password_recovery_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
SPEC = f"{L}/plans/pkg-spec-r45.json"
CLAIMS = f"{L}/plans/round-45-claims.md"
CL = f"{W}/claims"
ENV = f"{CL}/envelope.sh"
FREEZE = "b4fcd35141acda5fa0980a34dd29ab880b702ee6"
ENTRY = f"{L}/corpus/knowledge/tb2-{TASK}-grader.md"
ROUTED = f"{L}/corpus/routed-findings.jsonl"

HOST_RULE = (
    "Host safety: run any fixture build, counter run or probe that can write files inside a bwrap sandbox in which "
    "`/home/vgpnk/.local/bin` is read-only (the envelope below does this). Never write to a shared PATH directory, "
    "`/usr`, `/etc`, or `$HOME` outside scratch. (Round 40: a seat planted a `git` shim in `~/.local/bin` and broke other "
    "lanes' git for minutes.)")
ENVELOPE = (f"Envelope for every counter/fixture/probe run: `{ENV} \"$S/env\" <command...>` (home read-only, ~/.cache "
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
kengaku round 45 (hyaku run 9, 2026-10-26), wave 1 of two v1 waves (build). Lane repo: {L}.
Two claims are FROZEN at {CLAIMS} (freeze commit {FREEZE}) — read it first, in full.
Nothing frozen may change: not the counters {C1} / {C2}, not the round-44 counter {K44} the instrument imports,
not the probe {PROBE}, not the spec {SPEC}, not the gate {GATE}, not the dry table {DRY}, not the captures {CAP}/,
not the modules {L}/plans/refusals45/ or the standing batteries plans/battery42|43|44, not {CL}/.

- C1 calibration: the fence. Subject file `plans/fixture_fence.py` DOES NOT EXIST yet (control
  {CL}/control-c1-nothing.txt: every refusal module LEAKED). The round-44 counter's fence (`{K44}` functions
  argv_shape_breach / lane_breach / repo_breach / symlink_breach / order_argv_breach, composed in `build_battery`
  order) contradicts the advertisement on 7 of 10 modules (`{CL}/control-c1-fence-r44.txt`: f7 commondir, f8
  config.worktree, f9 refuse-to-describe LEAKED; f1 gitdir-outside, f6 repo-above-d, f10 lane-include, f4 fifo
  READ outside d while deciding). The fence contract: `breach(d: pathlib.Path, argv: list[str], tool: str) ->
  str | None` where d is the fixture dir (absolute, resolved), argv the module's argv, tool `anchor` or `order`;
  a non-empty string refuses, None admits. It is judged by `python3 {C1} --lane <clone>` (docstring = the full
  rule): all 10 `plans/refusals45/` modules CLEAN (refused AND no successful or never-returned open under the
  build scratch outside d — the counter traces every fence run with `strace -f -y` inside a read-only bwrap
  sandbox), all 104 honest fixtures of battery42+43+44 ADMITTED with zero outside opens, `PREDICATE C1 pass`.
  Required design (frozen): pure-filesystem legs first (walk d, `.git` file/dir, symlinks, commondir,
  config.worktree, `[include]`/`[includeIf]`/`extensions.worktreeConfig` in any `.git/config*`, alternates,
  a `.git` found ABOVE d among ancestors up to the module build root), git-calling legs second (bounded
  `pin_git` with ceiling, timeout, no stdin; `rc != 0` from a store/lane probe is a breach, never "clean").
  Before/after state: r44-fence control contradicted=7; a passed counter prints `contradicted=0`.
- C2 coverage: pinned Terminal-Bench 2.0 `{TASK}` grader (terminal-bench-2 @ {PIN}; raw base {RAW}/) to be
  admitted as {ENTRY} with rows S149 (tests/test_outputs.py), S150 (instruction.md), S151 (environment/setup.sh),
  S152 (environment/Dockerfile), S153 (tests/test.sh), S154 (README.md), S155 (solution/solve.sh), S156
  (task.toml); tier A, status mined, opened 2026-10-26 (captures + SHA256SUMS in {CAP}/, all 9 files re-fetched
  `cmp`-identical at the pin ~23:0x -03; `gitignore` is rejected — repo hygiene, not content). Receipt {RCPT}:
  `plans/password_recovery_probe.py --lane .`, 16 cases. Grader facts (captured test_outputs.py):
  `test_recovery_file_exists` asserts `Path("/app/recovered_passwords.txt").exists()` (:8-10);
  `test_password_match` reads the file, `.strip().split("\\n")` into guesses (:14), dead `len(guesses) > 0`
  assert (:16, cannot fire), and asserts `"8XDP5Q2RT9ZK7BV4WW54" in guesses` — the ACTUAL constant is
  `8XDP5Q2RT9ZK7VB3BV4WW54` (:18) — exact line membership of one 23-char constant; no format, case, order,
  count or uniqueness check. setup.sh builds /app/varsea with a 4MB disk image (launchcode.txt zipped, split
  into two fragments dd'd at the 1MB and 3MB offsets); solve.sh is the oracle. Counter {C2}: V1-V10 re-pinned
  round-44 checks + V11 hardened (predictor lint <=4000B no table/IO/hash tokens, count-only disagreement,
  `random.Random(45)` 48 states). Entry needs sections `## Case table`, `## Mechanism`, `## Requirement map`,
  `## Located quotes`, `## Predictor` (one ```python block, `predict(text) -> bool`, text = file content or
  None), a `source:` line citing S149, and every S149-S156 id in body text outside the `source:` line.
- Frontier step rides both: one mined-mistake row (attempt 1's do-nothing battery C1 draft is the prime row;
  the probe docstring garble and the spec's extra row are two more), Gate blocks record >=1 admit and >=1
  reject (gitignore). Routed ledger: {ROUTED}.

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

FENCE_SPEC = (
    f"{HOST_RULE}\n\nImplement `plans/fixture_fence.py` in your own clone of the lane (read {C1} fully first — its docstring is the "
    f"frozen contract, and the 10 hostile modules at {L}/plans/refusals45/ each name the class they must defeat). Write the module to "
    f"\"$S/lane/plans/fixture_fence.py\", then run the counter `{C1} --lane \"$S/lane\" --work \"$S/w\"` inside the envelope and iterate "
    f"until it prints `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0 "
    f"read=0 hung=0 build_errors=0`, `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass`, exit 0. Design notes: use ONLY "
    f"stdlib; every parent git call must run under a ceiling, a timeout and no stdin; treat any git probe `rc != 0` as "
    f"unverifiable = breach; resolve every argv token against d; refuse a `.git` FILE, a `.git` above d (walk ancestors up to the "
    f"module root = the fixture dir's parent), `commondir`, `config.worktree`, any include surface (also `[includeIf]`), alternates, "
    f"symlinks escaping d, an order argv whose `--claims`/`--receipt` names a non-blob at HEAD, and any argv shape outside the "
    f"contract; keep the reason strings one line each. The harness invokes `breach(d, argv, tool)` with cwd=d under strace inside a "
    f"read-only sandbox — never open anything outside d yourself (the frozen design requires pure-filesystem legs before any git call, "
    f"and `GIT_CEILING_DIRECTORIES` on every git call). Paste the full counter output and ENVELOPE lines. Finally write your module to "
    f"{B}/<YourSeatName>/fixture_fence.py (the L1 picks one for the lane) and say what its limits are.")


def it(name, role, axes, task, verdict):
    return (name, role, axes, task, verdict)


ITEMS = [
    # ---- C1 build: three INDEPENDENT fence implementations (the L1 picks one; the rest are cross-checks) ----
    it("R45FenceOwn", "executor", ["calibration", "operability"], FENCE_SPEC +
       " You are the PRIMARY candidate; your module is the default pick unless a variant lands a cleaner pass.",
       "VERDICT: fixture-fence-primary-pass-<yes|no>-clean-<n>"),
    it("R45FenceVarA", "executor", ["calibration", "operability"], FENCE_SPEC +
       " You are an INDEPENDENT second implementation — do not copy the primary seat's approach; a different structure "
       "(e.g. one pass that collects every repo first) is the point.",
       "VERDICT: fixture-fence-variant-a-pass-<yes|no>-clean-<n>"),
    it("R45FenceVarB", "executor", ["calibration", "operability"], FENCE_SPEC +
       " You are an INDEPENDENT third implementation — minimal-code style; every extra line is a mutation target.",
       "VERDICT: fixture-fence-variant-b-pass-<yes|no>-clean-<n>"),
    # ---- C1 attack/verification on the frozen instrument ----
    ("R45CriticPredicate", "critic", ["calibration"],
     f"Falsify the C1 claim wording in {CLAIMS} and the counter docstring of {C1}: is `contradicted` the right count; can a "
     f"fence reach `PREDICATE C1 pass` while still violating 'no file outside d is parsed' (e.g. reading an outside path "
     f"with a syscall not traced — read()/mmap of an already-open fd, an open elsewhere in the tree, a subprocess it spawns "
     f"outside bwrap's view); is `clean` per-module vs per-fixture right; does the HONEST leg allow a fence keyed on "
     f"fixture-id text? Enumerate every bypass of the FROZEN predicate you find; rank by whether it changes the verdict.",
     "VERDICT: c1-predicate-bypasses-<n>-verdict-changing-<k>"),
    ("R45CriticSeparability", "critic", ["calibration", "coverage"],
     f"Check causal separability of the two frozen claims in {CLAIMS}: can C1 land without C2 and vice versa; do they share "
     f"a file, a capture, a counter input or a commit? Also check the frozen predicate is THE SAME SENTENCE in the claims "
     f"file and the counter docstring of {C1} and {C2} (kumitate r42 lesson), and that every input each counter pins exists "
     f"at the pinned digest (`{CL}/frozen-digests.txt`).",
     "VERDICT: separable-<yes|no>-predicate-identical-<yes|no>-defects-<n>"),
    ("R45RevHostiles", "reviewer", ["calibration"],
     f"Review the ten modules of {L}/plans/refusals45/ against their routed reports ({L}/corpus/lessons/round-44-verifier-"
     f"spotcheck.md §4, {L}/.ufo/waves/round-44/wave/R44SentinelFences.md, R44LabratLaneInclude.md): does each module actually "
     f"build the scenario its docstring claims; does f10's include really sit outside d; does f9's repo really make "
     f"rev-parse fail; are f1-f6 byte-identical copies of {L}/.ufo/waves/round-44/claims/hostile/ (sha256 compare). Build "
     f"each in scratch via the counter's builder ({C1} `--battery-dir` is refusal-only — use the r44 counter's dev path or a "
     f"manual build in a sandbox) and verify the scenario exists.",
     "VERDICT: hostile-modules-faithful-<n>/10-defects-<k>"),
    ("R45MutParser", "mutation-tester", ["calibration", "operability"],
     f"{HOST_RULE}\n\nMutation-test the NEW instrument {C1} (it was never attacked; the builder is inherited-pinned). In a "
     f"scratch copy generate single-edit mutants of its NEW code: the OPEN_RE/DONE_RE/UNFINISHED/RESUMED parsing, the "
     f"outside-open region test (`scratch` vs `d`), the per-module verdict roll-up, run_fence's sandbox argv, the HONEST/ "
     f"REFUSALS accounting, `main`'s `good` conjunction. For each mutant run the r44-fence control (a fixture fence = "
     f"{K44} + the adapter tail at {CL}/fences/r44_tail.py) with a stub admit_all/refuse_all ({CL}/fences/) as needed so "
     f"the run is cheap, and see whether the instrument still prints the same verdict lines. A mutant is caught when the "
     f"printed verdict flips vs the unmutated run. Table mutant, caught/survived, why.",
     "VERDICT: instrument-mutants-caught-<k>/<n>"),
    ("R45SentFenceDesign", "sentinel", ["calibration", "safety"],
     f"{HOST_RULE}\n\nEnumerate (no implementation) every git-config and repo-layout vector that could make a fence read "
     f"or trust something outside the fixture d beyond the frozen f1-f10: `includeIf gitdir:`/`onbranch:` conditions, "
     f"`.git/config` `[include]` with a ~ or env path, `core.attributesFile`, `core.hooksPath`, `mailmap`, `submodule` "
     f"with absolute URL, `core.fsmonitor`, `objects/info/alternates` relative, `commondir` relative path, linked "
     f"worktree metadata (`worktrees/<name>/`), `GIT_DIR`/`GIT_WORK_TREE`/`GIT_OBJECT_DIRECTORY` in env, gitdir: file "
     f"variants (relative target, `gitdir : ` spacing), `.git` being a symlink, hardlinked objects. For each: does a git "
     f"command parse it (paste the command + proof in scratch), and which frozen leg catches it? This list feeds the "
     f"wave-2 held-out hostile authors.",
     "VERDICT: fence-design-vectors-<n>-uncovered-<k>"),
    ("R45LabratGitAPIs", "executor", ["calibration"],
     f"{HOST_RULE}\n\nProbe git's actual behaviour in scratch (never the lane): does `git config --local --no-includes` "
     f"really skip `[include]` while `rev-parse` still parses it; does `extensions.worktreeConfig=true` + `config.worktree` "
     f"reach `rev-parse`/status; does a relative `commondir` resolve against the git dir; does `GIT_CEILING_DIRECTORIES` "
     f"stop discovery above a directory that is itself a repo's parent; does an `[includeIf gitdir:]` trigger on a fixture "
     f"path; does `rev-parse --git-common-dir` resolve a commondir. Paste each probe + output; state which fence leg each "
     f"result demands.",
     "VERDICT: git-behaviours-verified-<n>-leg-mapped-<k>"),
    ("R45RevC1Instrument", "reviewer", ["calibration"],
     f"Read {C1} end to end as a reviewer: is every pinned input actually a lane path that exists; is `scratch=(fx,btmp)` "
     f"the right outside region (what about `mods/` copies — a module source under mods can name any file); can a hostile "
     f"module's build() make an honest-looking fixture that still trips the real vulnerability the class represents; does "
     f"run_fence's read-only sandbox let the fence write anywhere (writable=(logdir,) — is logdir outside d but inside the "
     f"region?); is HONEST_TOTAL 104 right (`find plans/battery4* -name '*.py' | xargs grep -c 'fid'`). List defects by "
     f"severity.",
     "VERDICT: instrument-review-defects-<n>-predicate-changing-<k>"),
    ("R45ExecControls", "executor", ["calibration"],
     f"{HOST_RULE}\n\nReproduce every C1 control receipt from {CL}/ (control-c1-nothing.txt, control-c1-fence-r44.txt, "
     f"-admit_all.txt, -refuse_all.txt, -static_only.txt) in a clean `--shared` clone at the freeze commit {FREEZE}: for "
     f"each fence stub in {CL}/fences/ (r44 adapter = `cat {K44} {CL}/fences/r44_tail.py > clone/plans/fixture_fence.py`), "
     f"run `{C1} --lane <clone> --work \"$S/w\"` inside the envelope and byte-compare the REFUSALS/HONEST/CALIBRATION/"
     f"PREDICATE lines with the committed receipts. Also re-run {C2} `--lane <clone>` and compare with "
     f"{CL}/control-c2-nothing.txt and {CL}/control-c2-predictor.txt (rerun its control script). Report any drift.",
     "VERDICT: controls-reproduced-<n>/<t>-drift-<k>"),
    ("R45ExecHarnessRO", "reviewer", ["calibration", "safety"],
     f"{HOST_RULE}\n\nVerify run_fence's sandbox in {C1} really is read-only and isolated: instrument a fixture_fence.py "
     f"that (a) tries to write into d, (b) into the fixture's parent, (c) opens /etc/shadow, (d) opens a file outside d "
     f"deliberately and returns ADMIT — run each through the counter's FENCE-RUN path in a clone and paste the strace-"
     f"counted results. A deliberate outside open must be counted (read>0). Also try a fence that exec()s /usr/bin/git with "
     f"argv pointing outside d, and one that sleeps past FENCE_TIMEOUT.",
     "VERDICT: harness-confinement-holds-<yes|no>-details-<n>"),
    ("R45LabratControls", "reviewer", ["calibration"],
     f"{HOST_RULE}\n\nIndependently verify the claim's before-state count WITHOUT the counter: replay the r44-fence control "
     f"(`{CL}/control-c1-fence-r44.txt`) by hand — build f7, f8, f9, f10 fixtures in scratch with the module builders, run "
     f"the r44 fence's five functions ({K44}) under your own strace, and confirm each leaks or reads as the receipt says. "
     f"Report per module the syscall evidence.",
     "VERDICT: before-state-confirmed-<n>/7"),
    # ---- C2 build ----
    ("R45ProbeFirst", "executor", ["coverage"],
     f"{HOST_RULE}\n\nMake the FIRST recorded run of {PROBE} (claims order-of-operations: only --dry and --stage-check ran "
     f"pre-freeze): in your clone `{C2.replace('/round45_c2_verify.py','')}` run `python3 {PROBE} --lane \"$S/lane\" --work "
     f"\"$S/w\"` inside the envelope, save stdout as the receipt draft {B}/R45ProbeFirst/password-recovery-probe.txt, and "
     f"paste its summary `cases= observed_pass= observed_fail= mismatches=` line, the `regrade` summary and every CASE line "
     f"whose observed verdict differs from the frozen prediction in {DRY}. If the receipt shows mismatches>0 the claim is "
     f"honest-stop — say so plainly.",
     "VERDICT: probe-first-cases-<n>-mismatches-<m>"),
    ("R45ExecStageCheck", "executor", ["coverage"],
     f"{HOST_RULE}\n\nIndependently reproduce the probe's --dry (byte-equal to {DRY}) and --stage-check (`stagecheck "
     f"cases=16 failed=0`) in a clone, inside the envelope; then read every recipe in {PROBE} and say whether any case "
     f"recipe could have run pre-freeze on this host (it may not).",
     "VERDICT: stage-check-reproduced-<yes|no>"),
    ("R45PkgEntry", "scribe", ["coverage", "quality"],
     f"Draft the knowledge entry {ENTRY} in your report subdir (never in the lane): sections `## Case table` (16 rows, "
     f"receipt order `| `<cid>` | <P|F>`-letters | <pass|fail> | <text> |`), `## Mechanism` (one row per case citing a "
     f"frozen DECISIVE line — see DECISIVE in {C2} — with a verbatim >=2-word quote in curly quotes from that exact capture "
     f"line), `## Requirement map` (one row per frozen tag in {DRY}: `| `instruction.md:<L>` | `<tag>` | <enforced|"
     f"unenforced|partly> | `case`, ... |` label derived from the receipt), `## Located quotes` (pkg_gate.py QUOTE_ROW "
     f"shape: >=10 quotes, >=10 distinct `file:line` locations, each 3-25 words verbatim from the captures at {CAP}/ or "
     f"upstream {RAW}/), `## Predictor` (ONE ```python block: `predict(text) -> bool` — the grader's exact rule: text None "
     f"-> False; else answer in `text.replace('\\r\\n','\\n').strip().split('\\n')` — no table/IO/hash tokens, <=4000 "
     f"bytes), a `source:` first line citing S149, and body text that mentions each of S149-S156 at least once outside the "
     f"source line. Re-open every cited capture line yourself (file:line + sha256 of the capture); never quote a line you "
     f"did not open. Predicted case letters come ONLY from {DRY} (the receipt may not exist yet — draft against the frozen "
     f"dry table and mark the row cells `P`/`F` from its `predicted=` column).",
     "VERDICT: entry-draft-sections-5-quotes-<n>"),
    ("R45PkgRows", "scribe", ["coverage"],
     f"Draft the nine SOURCES rows S149-S156 for {L}/corpus/SOURCES.md in your subdir (8 rows + the 9th is NOT a row: "
     f"gitignore is rejected). Match the lane's frozen schema exactly (11 cells; see rows S138-S146 for shape and the "
     f"census script {F}/scripts/sources-census.sh validate --file for conformance): tier A, status mined, opened "
     f"2026-10-26, recheck a valid cadence, `used-by` = the entry's repo-relative path, scope/anchor cells per the spec "
     f"{SPEC} rows map (each row's anchor = its own sha256). For each row write the `## Gate` block lines the lesson needs: "
     f"URL, your access date, a located quote <=25 words FROM THE CAPTURE YOU OPENED (path + line + sha256). Also write "
     f"gitignore's rejection row (reason: repo hygiene, not graded content; flip condition). Validate your rows by "
     f"appending them to a scratch copy of SOURCES.md and running the census validate --file — paste the output.",
     "VERDICT: rows-drafted-8-valid-<yes|no>-reject-1"),
    ("R45PkgProse", "scribe", ["coverage", "adjacency"],
     f"Draft, in your subdir, the prose deltas the package needs: (1) README index row for {ENTRY} following the shape of "
     f"the tb2-feal-linear-cryptanalysis-grader row (read {L}/corpus/README.md); (2) the §Frontier narrowing line — the "
     f"TB2 clause goes from '10 of 89' to '11 of 89' (find the exact current wording first); (3) one coverage-map bullet; "
     f"(4) a PROVINCE.md paragraph for the new grader class following the round-44 paragraph's shape (read the tail of "
     f"{L}/PROVINCE.md); (5) a LOG.md bullet block for the round-45 C2 entry. Paste-ready diffs only, byte-level context.",
     "VERDICT: prose-drafts-5"),
    ("R45PkgGateDry", "executor", ["coverage"],
     f"{HOST_RULE}\n\nDry-run the package gate against a mirror BEFORE the entry exists: in your clone write a stub entry "
     f"(the frozen structure without content), the drafted rows from your own reading of {SPEC}, and run `{GATE} package "
     f"--root <mirror> --spec {SPEC} --rerun --require-clean-tree` to enumerate exactly what P1-P10 demand beyond the "
     f"drafts (so the wave's scribes hit it once). Paste the full gate output and a checklist keyed to the spec.",
     "VERDICT: gate-demands-enumerated-<n>"),
    ("R45PytestParity", "reviewer", ["coverage"],
     f"{HOST_RULE}\n\nReal-pytest parity: stage each of the 16 case end-states the probe builds (or at least the 11 "
     f"non-trivial ones) inside your own bwrap sandbox exactly as {PROBE} does, then run REAL pytest (uvx -p 3.13 pytest, "
     f"or the host's) on the captured {CAP}/tests/test_outputs.py against each, and compare per-test letters (P/F/-) with "
     f"the probe's frozen dry table and (if the first run landed) the receipt. Paste per-case pytest -v output vs the "
     f"probe letters.",
     "VERDICT: pytest-parity-<n>/16"),
    # ---- frontier / quality ----
    ("R45Lesson", "scribe", ["quality", "discernment"],
     f"Draft {L}/corpus/lessons/round-45.md in your subdir: `## Gate` (>=1 admit — S149-S156 rows with per-row quote "
     f"blocks; >=1 reject — gitignore with reason+flip), `## Mistakes` (the mined rows: attempt-1's do-nothing C1 design — "
     f"a battery45 re-killing the five battery44 mutants, class do-nothing-control, captured-by 'the standing-battery "
     f"control' — this is the round's mined mistake; the garbled probe docstring; the gitignore-as-row spec bug caught by "
     f"the Gate rule), `## Predictions` table mirroring the frozen claims. Read {L}/corpus/lessons/round-44.md for shape "
     f"and the r44 spotcheck §4 for the routed items this round fixes. Also draft the SCORECARD round-45 section row and "
     f"LOG.md entry in the same file's shape (read their round-44 sections).",
     "VERDICT: lesson-draft-sections-3"),
    ("R45Considerthese", "scribe", ["discernment"],
     f"Mine {L}/considerthese/2026-10-26.md and 2026-10-25.md: list every proposal; mark which are already implemented "
     f"(grep the lane for their artifact); pick the ONE still-unimplemented proposal most fitting this round and write "
     f"its grounding note (what it would land as: lesson / QUALITY criterion / SOURCES row, what evidence it points at, "
     f"and what you opened to verify it). At most one per round.",
     "VERDICT: proposals-<n>-implemented-<k>-chosen-<name|none>"),
    ("R45MergeRescreen", "reviewer", ["coverage"],
     f"{HOST_RULE}\n\nAssimilation rescreen for the report's `Sources & frontier` line: (a) run the id-collision check "
     f"exactly per the round prompt (grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' over {L}/corpus/SOURCES.md and "
     f"/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md, comm -12 -> collisions); paste reg-ids count, "
     f"staged-ids count, collisions count. (b) Prove the guard on a scratch fixture with an indented `  | S002 |` row. "
     f"(c) The lane's quarantine slice: read /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-"
     f"register.md data rows for lane `kengaku` (awk per the prompt) — list each S-id, hand-check ONE cited source for "
     f"ONE row (fetch upstream, locate the quote) and give verdicts for what you can verify. Report verdicts per row; "
     f"adopt nothing.",
     "VERDICT: merge-rescreen-collisions-<n>-quarantine-<k>-rows"),
    ("R45ConnSibling", "connector", ["adjacency"],
     f"Sibling-overlap scan for the PROVINCE paragraph: which sibling lanes' corpora/counters touch git-fixture "
     f"containment, sandbox fences, mutation-attributed gate testing, or answer-leak detection? Check {F}/<sibling>-"
     f"shokunin/PROVINCE.md and their plans/ for fence-like code; also confirm the feal-linear grader entry doesn't "
     f"already cite this task family in a way that makes the new entry redundant. Name owners and overlap; say what the "
     f"PROVINCE paragraph must disclaim.",
     "VERDICT: sibling-overlap-<n>-disclaim-<k>"),
    ("R45ConnPattern", "connector", ["quality"],
     f"Cross-claim pattern scan for the lesson: read the last three lessons ({L}/corpus/lessons/round-42..44.md) and "
     f"spotchecks: which routed findings recur (fence-class, predictor-memorization, do-nothing controls); which QUALITY "
     f"criteria already cover them; what is still uncaptured. Also compare this round's C1 shape (subject-as-file, "
     f"instrument frozen) with rounds 40-44's counter-instrument shape — is it precedent or a new class; note the "
     f"attempt-1 invalid_prompt failure mode for the mistakes table.",
     "VERDICT: patterns-<n>-new-class-<yes|no>"),
    ("R45RevengerOrder", "revenger", ["calibration"],
     f"Reverse-engineer why the round-43/44 counters call lane_breach BEFORE repo_breach ({K44} build_battery:758 area; "
     f"git log -p the counter family plans/round4*_c1_verify.py and the wave reports R42CritC1Counter, R43SentinelCounter): "
     f"was the ordering chosen to let discovery see what the tool sees (as the docstring claims), and does moving "
     f"pure-filesystem legs first (this round's design) lose any behaviour the order was protecting? Cite commits and "
     f"report sections.",
     "VERDICT: order-origin-<named>-behaviour-lost-<yes|no>"),
    ("R45ScoutTB2", "scout", ["coverage"],
     f"Per-surface reconnaissance for the round-46 data walk: in terminal-bench-2 @ {PIN}, enumerate the remaining "
     f"unclaimed grader shapes (compare {L}/corpus/README.md §Frontier task list against the repo's task dirs) — how many "
     f"of the 89 tasks now sit in the executed sample, which candidate tasks have an F1-like constant grader vs a "
     f"genuinely different shape, and name 2-3 next-round candidates with file:line evidence (fetch raw files at the "
     f"pin). Also confirm password-recovery is task #11 for the Frontier line.",
     "VERDICT: frontier-<n>-of-89-candidates-<k>"),
    ("R45ScoutRefetch", "scout", ["freshness"],
     f"Refetch all nine upstream files at {RAW}/ (curl, one per path) and byte-compare with the captures in {CAP}/ "
     f"(sha256sum both sides); also check whether the task dir moved upstream at a newer commit (fetch the repo's "
     f"tree listing HEAD — does the pin {PIN} still resolve and does HEAD differ). Report any drift.",
     "VERDICT: refetch-identical-9/9-pin-ok-<yes|no>"),
    ("R45DistillRouted", "scout", ["quality"],
     f"Deduplicate the open rows of {ROUTED} (`python3 {L}/plans/routed_open.py --lane {L} --list`): group rows describing "
     f"the same underlying defect (the fence findings V1-V3 and LaneInclude should cluster with any older fence rows); "
     f"report groups with their row ids so the round-45 closure lines can close a whole class at once.",
     "VERDICT: routed-groups-<g>-from-<n>"),
    ("R45NoHarmBaseline", "executor", ["operability"],
     f"{HOST_RULE}\n\nBaseline no-harm measurement BEFORE the claim lands: in a clean `--shared` clone of {FREEZE} run the "
     f"round-44 measure set — `python3 {L}/plans/round44_c1_verify.py --lane <clone> --work \"$S/w\"` (PREDICATE C1), "
     f"`{L}/plans/round44_c2_verify.py --lane <clone>` (C2), `python3 {L}/plans/anchor_digest_check.py --lane <clone>` "
     f"(rows/tokens/defects), `python3 {L}/plans/routed_open.py --lane <clone> --list` count, census "
     f"{F}/scripts/sources-census.sh validate --root {F} kengaku, and `{L}/plans/round_close.py --round 44` if it exists "
     f"— inside the envelope, output to {B}/R45NoHarmBaseline/measure-baseline.txt. These are the expected-red lines the "
     f"final measure must not regress beyond.",
     "VERDICT: baseline-recorded-lines-<n>"),
    ("R45SimplifierCounter", "simplifier", ["operability"],
     f"Review {C1} for dead code and needless complexity without changing behaviour: unused imports/vars, the unused "
     f"`first` variable chains, duplicated verdict logic, the keep-log env hook (is it documented). Report a patch-ready "
     f"list (no edits to the lane).",
     "VERDICT: simplifications-<n>"),
    ("R45ScoutFenceArt", "scout", ["calibration"],
     f"Prior-art recon for the fence design: how do real tools confine git config parsing (git -c include.path=/dev/null, "
     f"GIT_CONFIG_NOSYSTEM, --no-includes semantics, isolated home); what does git documentation say config.worktree "
     f"requires to be honoured (extensions.worktreeConfig + the file); are there published notes on commondir delegation "
     f"surprises. Cite docs/git-config and gitcore docs at kernel.org or git-scm with section names.",
     "VERDICT: prior-art-<n>-applicable-<k>"),
    ("R45SonicPinCheck", "reviewer", ["calibration"],
     f"Verify the frozen digest table `{CL}/frozen-digests.txt`: recompute every listed sha256 over the lane files, list "
     f"any mismatch; also verify every PINS entry in {C1} maps to an existing lane path and every CAPTURES entry in {C2} "
     f"has a file in {CAP}/. Report counts only, with the commands.",
     "VERDICT: pins-verified-<n>/<t>-mismatch-<k>"),
    ("R45ExecR45CounterDocs", "executor", ["operability"],
     f"{HOST_RULE}\n\nCheck both counters run from a clean clone EXACTLY as the claims promise: clone at {FREEZE} under "
     f"scratch; `python3 plans/round45_c1_verify.py --lane .` and `python3 plans/round45_c2_verify.py --lane .` with cwd "
     f"INSIDE the clone (not --lane flag), inside the envelope; confirm identical verdict lines to the committed controls. "
     f"Also verify `--work` and `--jobs` flags behave (run C1 with --jobs 2 once).",
     "VERDICT: counters-clone-runnable-<yes|no>"),
    ("R45PlanNext", "scout", ["calibration", "coverage"],
     f"Data walk for round 46 (the SCORECARD `### Planned (round 46)` row): read {L}/SCORECARD.md round-44/45 sections, "
     f"{L}/.ufo/waves/round-44/wave/R44PlanNext.md, and this round's state; price the `round_close.py` survivors as a "
     f"third-tool claim (stub order tool + stub census — how many survivors, which classes); coverage candidates from "
     f"R45ScoutTB2's output if delivered, else walk the TB2 task list yourself; novelty: the F1 answer-leak census draft "
     f"under {W}/attempt1-unclaimed/ — is it a viable claim next round (does it need a do-nothing control?). Written for "
     f"the L1.",
     "VERDICT: r46-candidates-<n>"),
    ("R45CriticC2Instrument", "critic", ["coverage"],
     f"Falsify the C2 counter {C2}: (a) can the probe receipt be faked by a receipt file the counter cannot distinguish "
     f"(V4 receipt checks — is a hand-written receipt with matching CASE lines accepted); (b) V11 lint bypass — write a "
     f"predictor that answers via a disguised table under the token ban (split strings, arithmetic, chr()) that still "
     f"passes disagree=0 — demonstrate in scratch by loading the counter's v11 on a mirror; (c) does V8's ORDER RESULT "
     f"PASS require a real receipt; (d) any FROZEN digest that pins content the claim does not need (over-pinning) or "
     f"misses (under-pinning).",
     "VERDICT: c2-instrument-bypasses-<n>-verdict-changing-<k>"),
    ("R45MutV11States", "mutation-tester", ["coverage"],
     f"{HOST_RULE}\n\nMutation-test V11's state generator in {C2}: mutate each STATE_KINDS branch (drop the constant, "
     f"mutate the format-decoy shape, remove '\\ufeff'/'\\r' kinds) in a scratch copy and check whether the r44-style "
     f"memorized predictors ({CL}/c2_predictor_control.py's five) would now pass when they should fail — i.e. does the "
     f"kind list still distinguish the six control predictors. Also check `answer()`'s regex against adversarial grader "
     f"files (two 23-char tokens). Table mutant -> still-distinguishes?",
     "VERDICT: v11-state-mutants-distinguished-<k>/<n>"),
    ("R45SentC2Sandbox", "sentinel", ["coverage", "safety"],
     f"{HOST_RULE}\n\nAudit the probe's bwrap sandbox in {PROBE}: can a recipe or the grader reach the host (network "
     f"unshared? /home bound? writable paths?); does the zeros-for-urandom substitution change any grader-visible "
     f"behaviour besides file content (setup.sh uses `date +%s%N` and dd counts); is `/pub` truly read-only; can a case "
     f"recipe's writes leak outside its /app. Paste strace evidence for at least the setup.sh run.",
     "VERDICT: probe-sandbox-escapes-<n>"),
    ("R45ExecWitnessFence", "executor", ["calibration"],
     f"{HOST_RULE}\n\nWrite the C1 WITNESS fence for the claims' reachability argument (analogous to round-44's "
     f"witness-as-battery): a minimal correct `plans/fixture_fence.py` written ONLY from this prompt's contract "
     f"(static legs first; pin_git with ceiling+timeout; include/config.worktree/commondir/alternates/above-d/argv "
     f"checks). Run it through {C1} in your clone; if it passes `PREDICATE C1 pass` the target is reachable-by-"
     f"witnessed-work. Compare with the control fences in {CL}/fences/ and name the minimal delta.",
     "VERDICT: witness-fence-pass-<yes|no>"),
]

FLASH = {"executor", "labrat", "scribe", "sonic", "simplifier", "revenger", "sentinel"}
ATTACK = {"reviewer", "critic", "mutation-tester", "labrat"}


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 45 wave-1 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r45 wave 1 (build, v1)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    c = Counter(i["role"] for i in items)
    flash = sum(n for r, n in c.items() if r in FLASH)
    attack = sum(n for r, n in c.items() if r in ATTACK)
    assert 32 <= len(items) <= 64, len(items)
    assert flash * 2 >= len(items), f"m_flash share {flash}/{len(items)} below half"
    assert attack * 4 >= len(items), f"attack share {attack}/{len(items)} below a quarter"
    spec = {"wave": "kengaku-r45-w1",
            "milestone": "kengaku round 45 wave 1: C1 fixture_fence implementations + instrument attacks, "
                         "C2 password-recovery package drafts + first probe run, frontier/lesson drafts",
            "reportDir": ".ufo/waves/round-45/w1", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    print(len(items), dict(c))
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
