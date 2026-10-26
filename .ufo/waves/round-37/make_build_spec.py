#!/usr/bin/env python3
"""Renders .ufo/waves/round-37/build-spec.json (wave 1 of 2, policy v1, 40 seats)."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-37"
B = f"{W}/build"
SCR = "/fast/scratch/hyaku/kengaku-r37"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
CAP = f"{L}/corpus/evidence/round37/tb2-git-webserver"
E37 = f"{L}/corpus/evidence/round37"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAWRL = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/configure-git-webserver"
C1 = f"{L}/plans/round37_c1_verify.py"
C2 = f"{L}/plans/round37_c2_verify.py"
PROBE = f"{L}/plans/git_webserver_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
CLONE = (f'Fixture rule: S={SCR}/<YourSeatName>; mkdir -p "$S"; trap \'rm -rf -- "$S"\' EXIT; export TMPDIR="$S"; '
         f'D="$S/fx"; git clone -q --shared {L} "$D/lane"; verify `git -C "$D/lane" rev-parse --show-toplevel` equals "$D/lane" '
         f'before any write; every git call names -C "$D/lane"; never commit (index-only `git add` inside your clone is fine); '
         f'copy uncommitted lane files you need into the clone. Remove "$S" before you finish (copy receipts into your report dir first).')

CONTEXT = f"""# Goal
kengaku round 37 (hyaku run 8, 2026-10-26), WAVE 1 of 2 (build + first falsifiers). Lane repo: {L}.
The two claims are FROZEN at {L}/plans/round-37-claims.md (freeze commit ca790460e9b74d4dc5870c878affd13cc9c4437a; first recorded probe
run 5c7b34e9223f460a440596e3a76bdae8bfdd37d8) — read it first, in full. Nothing frozen may change: not the gate {GATE}, not the
counters, not the probe, not the mutant list.
- C1 calibration: the round-36 package gate {GATE} advertises defect classes (its docstring, corpus/QUALITY.md Q24, SCORECARD capability
  row `package-gate`). The frozen counter {C1} silences one gate branch at a time (55 frozen mutants M01-M55, listed in the counter with
  clause and advertised class) and counts a class demonstrated only when its mutant changes the gate's result — (exit code, set of clause
  ids printing `DEFECT`) — on some battery fixture. At freeze the round-36 battery kills 5/55 (M01 M05 M40 M47 M54); 50 survive. The work:
  battery modules plans/battery37/*.py with SINGLE-DEFECT fixtures until `python3 plans/round37_c1_verify.py --lane .` prints
  `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`. Fixture API (read the counter docstring and the example
  {W}/claims/example_battery/ex_p3_words.py): a module exports FIXTURES = [{{"fid", "expect": "accept"|"reject", "defects": [exact clause ids
  that must print DEFECT], "build": build}}]; build(ctx, d) fills the EMPTY directory d and returns the gate argv tail (never `--spec`):
  ctx.genuine_package(d) git-inits d and copies the genuine round-35 package (spec {L}/plans/pkg-spec-r35.json); ctx.git_add(d) stages it
  index-only; ctx.r36 is {L}/plans/round36_c1_verify.py (rewrite_quotes, QUOTE_ROW, mut_teaches, stub_probe, copy_package, build_line_fixtures);
  ctx.d4_line(), ctx.d5_line(), ctx.d5_capture_dir(), ctx.spec. Package argv: ["package", "--root", str(d), "--require-clean-tree"] plus
  "--rerun" when P10 must run; line argv: ["d4-line", "--file", F] / ["d5-line", "--file", F, "--capture-dir", DIR] with F/DIR inside d.
  A fixture must never be recognisable by name: the counter re-runs every fixture under another directory name (renamed_disagree must be 0).
  Develop with `python3 {C1} --lane {L} --battery-dir <your battery dir> --only <your mutant ids> --work "$S"` (read-only on the lane; it
  prints `PREDICATE C1 n/a` in that mode); a fixture is right only when its FIXTURE line ends `ok` and its mutants print `killed`.
- C2 coverage: pinned Terminal-Bench 2.0 `configure-git-webserver` grader (terminal-bench-2 @ {PIN}) admitted as
  corpus/knowledge/tb2-git-webserver-grader.md with rows S111 (tests/test_outputs.py), S112 (tests/verify.sh), S113 (instruction.md); the
  executed offline probe {PROBE} (22 frozen cases, bubblewrap sandbox per case; receipt {E37}/git-webserver-probe.txt:
  `cases=22 observed_pass=9 observed_fail=13 mismatches=0`, a second run byte-equal). Counter: `python3 plans/round37_c2_verify.py --lane .`
  (V1-V7, docstring; V2 runs the gate over the frozen spec template {L}/plans/pkg-spec-r37.json; V7 checks a `## Requirement map` table
  whose rows look like | `instruction.md:1-6` | unenforced | `static-file-no-git` | and whose labels must agree with the receipt).
  Captures (byte-identical to the pinned raw files, SHA256SUMS beside them): {CAP}/ (test_outputs.py, verify.sh, test.sh, instruction.md,
  task.toml, solve.sh = the oracle). Headline observations of the receipt: a file served on :8080 with no git repository, hook or push
  passes (verify.sh never reads the expect step's status); a body that merely contains the text `TEST PASSED` passes even though verify.sh
  prints `TEST FAILED` (test_outputs.py:13 checks a substring of stdout that echoes the body); status and content come from two separate
  requests; curl runs without -L and without a timeout; trailing newlines are stripped, other whitespace/case/CR/BOM are not.
- Controls (all red at freeze): {W}/claims/control-*.txt; census before {W}/claims/census-before.txt (exit 0, 15 W04).
- Round-36 non-author spot-check routed items: {L}/corpus/lessons/round-36-verifier-spotcheck.md section 5.

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report dir is {B}/; drafts and receipts go under {B}/<YourSeatName>/ (create it). Never copy a corpus/ or plans/
  tree, a lane mirror, or a clone into {B}/.
- Scratch (operator directive 2026-10-25): clones, fixtures and work trees live ONLY under {SCR}/<YourSeatName>/ (NVMe), never under /tmp;
  pass it explicitly (export TMPDIR, --work); delete it before you finish (`trap 'rm -rf -- "$S"' EXIT`).
- Write ONLY inside {B}/ (your report + your own subdir) and your scratch dir. NEVER edit the lane's corpus/, plans/, SCORECARD.md, LOG.md,
  README.md, SKILL.md, PROVINCE.md, SHONEN.md or any other lane file — draft for the L1, who integrates. Never write into {F} (fleet root),
  sibling lanes, the lane's jj state, or the lane's Git index. Never run git add/commit/stash/checkout/reset/push/pull or any mutating jj
  command in the lane.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY: never write/commit/fetch there; run none of its campaign tools.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide: install via
  `uv tool` / `npx` / an official binary into ~/.local/bin, or file nothing and say so. Never run pacman -Sy/-Syu/-U/-R, never name an
  already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat probe).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location (file:line or URL+section) and
  is <= 25 words. Do not fabricate output; if something cannot be fetched or run, say so.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""


def bat(name, module, mids, hints):
    return (name, "executor", ["calibration", "operability"],
            f"Write the C1 battery module {B}/{name}/battery/{module}.py (stdlib only; fid prefix `{module}-`) whose SINGLE-DEFECT fixtures "
            f"kill the frozen mutants {mids} of {C1} (read each mutant's `old -> new` text there and the gate branch it silences in {GATE}). "
            f"One fixture per mutant unless one fixture provably kills several without losing single-defect clarity; each fixture's "
            f"`defects` must be the exact set of clause ids the UNMODIFIED gate prints as DEFECT on it (often one clause; a second clause may "
            f"fire when unavoidable — say why). Hints: {hints} Prove it: "
            f"`python3 {C1} --lane {L} --battery-dir {B}/{name}/battery --only {mids} --work \"$S\"` must print every FIXTURE line of your "
            f"module `ok`, `renamed_disagree=0`, `null_detected=0`, and each of your mutants `killed by=<your fid>`. Paste that output in full. "
            f"Then mutate your own fixtures (delete one at a time) and confirm the matching mutant flips to SURVIVED (shows each fixture is "
            f"load-bearing); paste the table. Report the module's sha256.",
            f"VERDICT: battery-{module}-killed-<k>/<n>-wrong-<w>")


ITEMS = [
    # ---- C1 battery executors (9) ----
    bat("R37BatP23", "p23", "M02,M03,M04,M06,M07,M08",
        "M02 receipt file deleted (staged deletion); M03 one receipt byte changed; M04 the '## Located quotes' heading renamed; M06 "
        "seven distinct quote texts at >=8 distinct lines (repeat one verbatim quote at a second line where it is also verbatim, or accept "
        "P4 also firing and declare it); M07 eight distinct quotes at seven distinct (capture,line) locations; M08 one quote cut to two words "
        "(see the example fixture)."),
    bat("R37BatP4", "p4", "M09,M10,M11,M12",
        "M09 Located-quotes table with header but zero data rows (P3 fires too); M10 one quote citing a capture name that does not exist "
        "(P5 fires too: 'quote capture not pinned' — that is a different clause, fine); M11 one quote citing line 9999; M12 one quote with "
        "one changed character at its correct line."),
    bat("R37BatP5", "p5", "M13,M14,M15,M16,M17,M18,M19",
        "the capture dir is the spec's capture_dir with SHA256SUMS. M13 SHA256SUMS removed; M14 an extra garbage line in SHA256SUMS; M15 a "
        "capture byte changed while SHA256SUMS keeps the old digest (P4 may also fire if a quoted line changes — change an unquoted line); "
        "M16 a row's capture line removed from SHA256SUMS; M17 SHA256SUMS digest changed consistently with changed bytes so it differs from "
        "the spec pin; M18 a quote citing a new capture file present on disk but not in SHA256SUMS; M19 an extra uncovered file in the "
        "capture dir."),
    bat("R37BatP6", "p6", "M20,M21,M22,M23,M24,M25,M26,M27",
        "edit corpus/SOURCES.md rows S105-S107 in the fixture only. M20 duplicate one row; M21 a row with 10 or 12 cells; M22 a URL off the "
        "pinned raw path; M23 tier B; M24 status queued; M25 used-by another path; M26 one teaches cell of 5 distinct words (keep the three "
        "pairwise distinct); M27 two teaches cells made identical but >=8 words each."),
    bat("R37BatP7", "p7", "M28,M29,M30,M31,M32,M33",
        "edit the entry corpus/knowledge/tb2-protein-assembly-grader.md in the fixture only. M28 entry deleted (many clauses fire; declare "
        "the exact set); M29 one `source:` line's URL changed; M30 verified-at date changed; M31 recheck line removed; M32 '## Negative "
        "space' heading removed; M33 the falsifier word removed from that section."),
    bat("R37BatP8", "p8", "M34,M35,M36,M37,M38",
        "edit corpus/README.md in the fixture only. M34 README deleted; M35 the entry's index row duplicated; M36 an index row missing one "
        "S-id; M37 the coverage bullet naming entry+receipt removed; M38 one extra knowledge file not indexed."),
    bat("R37BatP910", "p910", "M39,M41,M42,M43",
        "M39 a package dir that is NOT a git repo (do not git init; make sure the dir is not inside any other git worktree); M41 receipt "
        "deleted with --rerun (P2 also fires); M42 the probe plans/tb2_grader_probe.py edited to exit 1 after printing (P1 also fires) with "
        "--rerun; M43 the receipt changed by one byte with --rerun (P2 also fires). P10 re-runs the round-35 probe; time one run."),
    bat("R37BatD4", "d4", "M44,M45,M46",
        "use ctx.d4_line(). M44 --file pointing to a path that does not exist; M45 a file of two lines whose first is the genuine line; M46 "
        "the genuine line with its label prefix altered but every pattern still matching."),
    bat("R37BatD5", "d5", "M48,M49,M50,M51,M52,M53,M55",
        "use ctx.d5_line() and copy ctx.d5_capture_dir() into d when you alter captures. M48 --file missing; M49 two lines; M50 label "
        "altered; M51 the required token removed without adding the forbidden one; M52 the forbidden token added while the required one "
        "stays; M53 a capture dir lacking the capture file; M55 a capture whose bytes no longer contain the quote AND whose digest is in a "
        "manifest you rewrite consistently (so only the quote branch fires)."),
    # ---- C2 executors (5) ----
    ("R37DockerOracle", "executor", ["coverage", "freshness"],
     f"Run the task in its REAL image to test the probe's claims outside the sandbox. `docker pull alexgshaw/configure-git-webserver:20251031` "
     f"(task.toml {CAP}/task.toml:29; you are in group docker). In a throwaway container (`docker run --rm`, name it k37-<yours>, never "
     f"--privileged, never mount the lane read-write; copy {CAP}/verify.sh and test_outputs.py in with docker cp): (A) oracle path: run "
     f"{CAP}/solve.sh, then `bash verify.sh` as /tests/verify.sh would run (it apt-installs expect; internet is allowed by task.toml), "
     f"record stdout and whether `TEST PASSED` appears; (B) static-file cheat: fresh container, NO git: write hello.html with 'hello world' "
     f"under any dir and serve it on :8080 (python3 -m http.server if present, else busybox httpd/nginx from apt), run verify.sh, record; "
     f"(C) token cheat: serve a body 'TEST PASSED', run verify.sh, record; (D) run pytest on test_outputs.py the way tests/test.sh does if uv "
     f"works in the container (else say why) for B and C. Paste exact outputs (trim apt noise). Remove containers and the image afterwards "
     f"if you pulled it (`docker rmi`), report disk used.",
     "VERDICT: real-image-oracle-<pass|fail|blocked>-static-<pass|fail>-token-<pass|fail>"),
    ("R37IndepVerdicts", "executor", ["coverage", "calibration"],
     f"Independent check of the receipt {E37}/git-webserver-probe.txt WITHOUT the probe's sandbox: write {B}/R37IndepVerdicts/indep.sh (or .py) "
     f"that re-creates each of the 22 cases' server behaviour from the frozen table ({E37}/git-webserver-dry-cases-freeze.txt) using a "
     f"DIFFERENT isolation (e.g. `unshare -rn` with `ip link set lo up`, or a docker network namespace) and runs {CAP}/verify.sh with a "
     f"scratch HOME/cwd and PATH lacking apt-get/expect (and lacking curl for the wget cases), then applies test_outputs.py's rule "
     f"(substring 'TEST PASSED' in stdout). NEVER run verify.sh with your real HOME (it overwrites ~/.ssh/config). Compare pass/fail per case "
     f"with the receipt; any disagreement is a finding against the probe. Also run 3 extra cases of your own with predictions written first: "
     f"(a) a body containing 'xx TEST PASSED yy' on one line, (b) a server returning 200 for HEAD but 404 for GET, (c) 'hello world' served "
     f"with Content-Encoding: gzip.",
     "VERDICT: indep-agree-<n>/22-extra-<n_matched>/3"),
    ("R37ProbeRerun", "executor", ["operability", "freshness"],
     f"Determinism and environment sensitivity of the frozen probe {PROBE}: run `python3 plans/git_webserver_probe.py --lane {L} --work \"$S\"` "
     f"twice and cmp with {E37}/git-webserver-probe.txt; run it the way the gate's P10 does (`uv run --no-project --with biopython==1.85 "
     f"python3 plans/git_webserver_probe.py --lane .` with cwd {L}); with TMPDIR set to two different dirs; with LANG=C and LC_ALL unset in "
     f"the parent env; from a different cwd. Record each byte difference and its cause. Time a full run. Then run the C2 counter read-only "
     f"against the lane `python3 {C2} --lane {L} --work \"$S\"` and paste the output (expected red: entry/rows absent, untracked wave files).",
     "VERDICT: probe-deterministic-<yes|no>-uv-<same|diff>-runtime-<s>"),
    ("R37ReopenPins", "executor", ["coverage", "freshness"],
     f"Independently re-open {RAWRL}/{{tests/test_outputs.py,tests/verify.sh,tests/test.sh,instruction.md,task.toml,solution/solve.sh}} "
     f"with curl -fsSL into {B}/R37ReopenPins/; cmp each against {CAP}/ (tests/ files and solve.sh by basename); `cd {CAP} && sha256sum -c "
     f"SHA256SUMS`. Confirm the commit via https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/{PIN} (date/message); "
     f"list configure-git-webserver/ in the tree at that commit (git/trees ?recursive=1) and name any file not captured (e.g. environment/ "
     f"Dockerfile) and whether it matters to the grader. Check whether main differs for the six files (fetch main raw URLs, cmp) — a drift "
     f"note, not a defect. Locate and quote (<=25 words, file:line) for the entry: test_outputs.py:13, verify.sh:49, :57, :60, :62, :63, :75, "
     f"instruction.md:1, :7, :9.",
     "VERDICT: reopen-<n_identical>/6-drift-<yes|no>"),
    ("R37AnchorSweep", "executor", ["calibration", "freshness"],
     f"Frontier mistake fix (round-36 spot-check routed item 1: S110's anchor digest has 63 hex digits). Write {B}/R37AnchorSweep/"
     f"anchor_digest_check.py (stdlib, read-only, `--lane DIR`, honours TMPDIR, exit 0 clean / 1 defects / 2 usage): for every row of "
     f"corpus/SOURCES.md (0-3 leading spaces, as the census parses) collect each `sha256 <hex>` token in the anchor cell (6th cell); a token "
     f"is a defect unless it is exactly 64 lowercase hex AND equals the digest of some committed file under corpus/evidence/ or a digest "
     f"listed in a SHA256SUMS there — UNLESS a lesson line beginning `Erratum (round 37): S<id> anchor sha256` carries both the wrong token "
     f"and a 64-hex correct digest that is itself in a manifest. Print one line per defect and `rows=<n> tokens=<n> defects=<n>`. Show it "
     f"can fail: on the lane as it is, it must flag S110 (paste); in a fixture clone with the erratum line added to a copy of a lesson it "
     f"must pass; and five mutants must each be caught (erratum with a wrong correct digest; correct digest not in any manifest; S108 "
     f"anchor digest shortened; uppercase hex; token in another cell — decide and document). Draft the exact erratum line.",
     "VERDICT: anchor-sweep-before-<n>-after-<n>-mutants-<caught>/5"),
    ("R37LedgerTip", "executor", ["calibration", "operability"],
     f"considerthese/2026-10-25.md proposal 2(a) (`{L}/considerthese/2026-10-25.md:39-45`): re-run every closed routed defect's check at the "
     f"tip. Write {B}/R37LedgerTip/ledger_tip.py that, on a clean shared clone of the lane tip, runs every row of {L}/corpus/defects.jsonl "
     f"(checks in {L}/plans/defect_ledger.py) and {L}/corpus/defects-round35.jsonl (checks in {L}/plans/round36_c1_verify.py) and prints "
     f"per row `id status observed agree` plus `rows=… closed=… observed_pass=… mismatches=…`. Run it and paste. A closed row whose check now "
     f"fails is a finding (say whether the check is a freeze-only pin, e.g. a 42-file count, or a real regression). Do not edit any ledger.",
     "VERDICT: ledger-tip-rows-<n>-mismatches-<n>"),
    ("R37TipSweep", "executor", ["freshness", "operability"],
     f"No-harm baseline BEFORE landing, on a clean shared clone of the lane tip: run and record exit code + last output line of `python3 "
     f"grader.py`, `python3 grader.py --selftest`, `python3 plans/round36_c1_verify.py --lane .`, `python3 plans/round36_c2_verify.py --lane .`, "
     f"`python3 plans/regex_log_probe.py --lane .` (cmp with corpus/evidence/round36/regex-log-probe.txt), `python3 plans/pkg_gate.py package "
     f"--root . --spec plans/pkg-spec-r35.json --rerun --require-clean-tree`, `{F}/scripts/sources-census.sh validate --file corpus/SOURCES.md`, "
     f"and every gate listed in {L}/SKILL.md's gate/probe registry table (read it; run each listed command once). Table: command, exit, last "
     f"line, green/red, and for red: known/expected (cite) or new.",
     "VERDICT: tip-sweep-<n_green>/<n_total>"),
    # ---- scribes (8) ----
    ("R37PkgDraft", "scribe", ["coverage", "depth"],
     f"Draft the whole C2 package for the L1 to integrate, and prove it against the frozen counter in a fixture clone. (1) Entry "
     f"{B}/R37PkgDraft/entry.md for corpus/knowledge/tb2-git-webserver-grader.md: lines 1-3 `source: S111 — {RAWRL}/tests/test_outputs.py — "
     f"<anchor>`, S112 tests/verify.sh, S113 instruction.md (bare pinned URL, no fragment, nothing after the URL that the gate regex would "
     f"swallow — read c_provenance in {GATE}); `verified-at: 2026-10-26`; `recheck: 180d — <action>`. Sections: summary; what the grader "
     f"checks (static reading); `## Requirement map` table rows exactly like | `instruction.md:1-6` | unenforced | `static-file-no-git` | "
     f"covering instruction lines 1-9, labels agreeing with {E37}/git-webserver-probe.txt (read {C2} v7); the executed probe (summary line "
     f"verbatim; what each case group shows); what the probe does NOT show (oracle not run, no real git push, sandbox lacks apt/expect) ; "
     f"`## Negative space` with an explicit falsifier; `## Located quotes` table `| claim | “quote” | `file:line` |` with >= 10 distinct "
     f"quotes of 3-25 words, each verbatim on its cited line of the captures in {CAP} (check every one with `sed -n <n>p`). (2) Three "
     f"SOURCES rows S111-S113 in the 11-column schema of {L}/corpus/SOURCES.md (read the header and S105-S110), tier A, status mined, opened "
     f"2026-10-26, recheck 180d, used-by corpus/knowledge/tb2-git-webserver-grader.md, anchor cell containing `sha256 <the 64-hex pin>` exactly "
     f"once (copy from {CAP}/SHA256SUMS, never retype), teaches >= 8 words and pairwise distinct, no `|` inside a cell. (3) README additions: "
     f"one index row after the tb2-regex-log-grader row and one `- ` coverage-map bullet naming knowledge/tb2-git-webserver-grader.md and "
     f"evidence/round37/git-webserver-probe.txt (read c_readme). Then in your fixture clone apply all three, `git add -A` (index only), and "
     f"run `python3 plans/round37_c2_verify.py --lane \"$D/lane\" --work \"$S\"`; iterate until `checks=7 defects=0`; paste the final output.",
     "VERDICT: c2-package-checks-7-defects-<n>"),
    ("R37LessonDraft", "scribe", ["calibration", "coverage"],
     f"Draft {B}/R37LessonDraft/round-37.md (the lane lesson corpus/lessons/round-37.md) in the shape of {L}/corpus/lessons/round-36.md: "
     f"header (baseline 3ea9a1d9, freeze ca790460, first probe run 5c7b34e9); `## Gate` table (C2 entry admit-candidate; S111-S113 with URL, "
     f"access date 2026-10-26 and a <=25-word located quote each — verify each with sed -n against {CAP}; rejected candidates: tests/test.sh "
     f"and task.toml and solve.sh captured but not rows, with reasons; the assimilation line for considerthese/2026-10-25.md proposal 2(a)); "
     f"`## Mistakes` rows (class · evidence pointer · captured-by · fix): (1) S110 anchor digest truncated "
     f"({L}/corpus/lessons/round-36-verifier-spotcheck.md:71,88) — fix: anchor sweep + C2 V3 (shown able to fail); (2) the round-36 battery "
     f"demonstrated 5 of 55 advertised gate classes ({W}/claims/control-c1-nothing.txt) — captured-by none; (3) the C2 skip-control executed the "
     f"probe before the first recorded run (disclosed in {L}/plans/round-37-claims.md:3-10) — class: order-of-operations; plus any you find; "
     f"`## Census` (before: {W}/claims/census-before.txt); `## Spot-check` list for the non-author closure (cheapest-first). Leave numbers the "
     f"wave has not produced as `<pending: seat>`.",
     "VERDICT: lesson-drafted"),
    ("R37QualityDraft", "scribe", ["calibration"],
     f"Draft the next QUALITY.md criteria (read {L}/corpus/QUALITY.md, especially Q22-Q25 and their lesson citations): Q26 — every "
     f"`sha256` token in a SOURCES anchor is 64 hex and equals a committed manifest digest, checked mechanically (lesson round-37 Mistakes 1; "
     f"round-36 spot-check :71,:88); Q27 — a gate's advertised defect class counts as held only when a single-defect fixture kills that "
     f"class's silence mutant (lesson round-37 Mistakes 2; {C1}; control-c1-nothing.txt killed=5/55); a Limits paragraph for each "
     f"(observational demonstration, excluded branches named in {L}/plans/round-37-claims.md). Each criterion names the lesson that produced "
     f"it and the row it supersedes, if any. Output paste-ready markdown.",
     "VERDICT: quality-drafted-<n>-criteria"),
    ("R37SkillDraft", "scribe", ["operability", "depth"],
     f"Draft additions to {L}/SKILL.md (do not edit): (1) gate/probe registry rows in the exact table format already there (find it: grep -n "
     f"'pkg_gate' {L}/SKILL.md) for `git-webserver-probe` ({PROBE}; exit 0/2; needs /usr/bin/bwrap; runtime), `round37-c1-mutants` ({C1}), "
     f"`round37-c2` ({C2}), `anchor-digest-check` (draft by R37AnchorSweep, path plans/anchor_digest_check.py); (2) a short section "
     f"`## Service-class TB2 grader — round 37` with a decision table: when a grader's verdict is a substring of a helper script's stdout, "
     f"what to probe (echo of untrusted content, unread exit statuses, split requests, missing timeouts/redirect flags) and how to sandbox it "
     f"(network namespace, scratch HOME — verify.sh writes ~/.ssh/config). Cite file:line for every claim.",
     "VERDICT: skill-drafted-<n>-rows"),
    ("R37ProvinceDraft", "scribe", ["adjacency", "coverage"],
     f"Draft PROVINCE.md changes (do not edit): (1) a round-37 paragraph (<=140 words) in the style of the round-35/36 paragraphs: what the "
     f"service-class probe adds (offline execution of one pinned grader against synthetic HTTP states in a sandbox), what it never claims (task "
     f"validity, nginx/git/ssh administration, agent performance, the oracle path); (2) absorb the round-36 critic's unabsorbed wording fixes: "
     f"read {L}/.ufo/waves/round-36/build/R36CritScope.md findings F3-F6, F8, F10 and {L}/.ufo/waves/round-36/build/R36CritScope/"
     f"province-rewrite.txt, and draft each fix as an exact old→new pair against current {L}/PROVINCE.md lines (cite line numbers) or say why a "
     f"fix should not land. Adjacent lanes touched (read their PROVINCE.md heads; cite file:line).",
     "VERDICT: province-drafted-<n>-fixes"),
    ("R37R36Absorb", "scribe", ["calibration", "depth"],
     f"Absorb round-36 leftovers as append-only errata (draft only): (a) `R36RevProbePred` ({L}/.ufo/waves/round-36/build/R36RevProbePred.md): "
     f"cases ip-no-left-boundary and ip-no-right-boundary fail on lines other than the boundary line they name — draft an `## Errata (round 37)` "
     f"section for {L}/corpus/knowledge/tb2-regex-log-grader.md saying exactly which rows of its `What decides it` table are not independent "
     f"evidence (verify against {L}/corpus/evidence/round36/regex-log-probe.txt); (b) anchor drift: the entry's S110 `lines 1–11` vs the row's "
     f"`:1-19`, and round-36 lesson 'lines 71-81' vs list lines 72-82 in {L}/corpus/evidence/round36/tb2-regex-log/test_outputs.py — verify "
     f"each with sed -n and draft the erratum lines; (c) the S110 anchor digest erratum line `Erratum (round 37): S110 anchor sha256 …` with "
     f"the wrong and the correct digest copied from {L}/corpus/SOURCES.md and {L}/corpus/evidence/round36/tb2-regex-log/SHA256SUMS.",
     "VERDICT: absorb-drafted-<n>-errata"),
    ("R37PlanNext", "scribe", ["calibration", "coverage"],
     f"Draft `### Planned (round 38)` for SCORECARD.md and the matching LOG.md next-iteration line. Inputs: {L}/SCORECARD.md (round-36 planned "
     f"block and the round-37 frozen claims), {L}/.ufo/waves/round-36/build/R36PlanNext.md (TB2 class census: 9 of 89 tasks grade a live "
     f"service), and whatever wave-1 reports exist under {B}/ when you finish (read last). Two candidate directions with the opened source and "
     f"a do-nothing control each: e.g. a fourth TB2 grader class (file-tree/git-state: fix-git or sanitize-git-repo), or a gate clause the "
     f"round-37 mutants could not demonstrate; keep coverage capped by the L0 question in the text.",
     "VERDICT: plan-drafted"),
    ("R37ScorecardLogDraft", "scribe", ["calibration"],
     f"Draft the round-37 SCORECARD.md section and LOG.md entry (do not edit). Read the round-36 section of {L}/SCORECARD.md (from `## Round 36`) "
     f"and the last LOG.md entry for style. Table rows for C1 (calibration 8: mismatch count advertised-but-undemonstrated gate classes, "
     f"before 50 at freeze ca790460, after `<pending: integration>`) and C2 (coverage 7 capped by L0: before `checks=7 defects=4`, after "
     f"`<pending>`), counting commands verbatim from {L}/plans/round-37-claims.md, capability rows proposed (`gate-mutation-harness`, "
     f"`service-grader-sandbox-probe`) with demonstration commands, other axes held. Do not invent after-values.",
     "VERDICT: scorecard-log-drafted"),
    # ---- scouts (3) ----
    ("R37ScoutPriorArt", "scout", ["novelty", "coverage"],
     "Prior-art check for the C2 observations: (1) graders whose verdict is a substring of output that echoes agent-controlled content (verdict "
     "token injection / output spoofing) — in Terminal-Bench, SWE-bench, or reward-hacking literature; (2) shell-script verifiers that ignore "
     "intermediate exit statuses (no `set -e`); (3) audits of Terminal-Bench 2.0 tasks reporting broken or weak tests (search the TB2 paper "
     "arXiv 2601.11868, the harbor-framework/terminal-bench-2 GitHub issues and PRs, especially any naming configure-git-webserver). Fetch each "
     "hit (URL + <=25-word located quote + location). Verdict per observation: published / incremental / not found.",
     "VERDICT: priorart-<n>-hits-token-injection-<published|not-found>"),
    ("R37ScoutUpstream", "scout", ["freshness", "coverage"],
     f"Upstream state of the task: search https://github.com/harbor-framework/terminal-bench-2 issues/PRs/commits touching "
     f"configure-git-webserver (GitHub API search, unauthenticated is fine) and the older laude-institute/terminal-bench repo's version of the "
     f"same task (does its tests/ differ? fetch and diff test_outputs.py and any verify script). Also: is the task in the TB2 leaderboard "
     f"task list, and what resolution rate do public runs report for it if published? URLs + <=25-word quotes; record dates.",
     "VERDICT: upstream-<n>-items-diff-<yes|no>"),
    ("R37ScoutMergePkg", "scout", ["coverage", "adjacency"],
     f"Assimilation screen (read-only): /home/vgpnk/Projects/shokuknow/merge/kengaku/ (MERGE-REPORT.md, knowledge/, SOURCES.append.md). Is any "
     f"staged entry about service/process graders, shell verifiers, or Terminal-Bench task tests that fits C2 or the PROVINCE ({L}/PROVINCE.md)? "
     f"Re-check the held admit-candidate `grader-predicate-input-types.md` ({L}/corpus/lessons/round-36.md Gate row) — has anything changed; "
     f"does staged id space collide with S111-S113 (run the §10 0-3-space id extraction into {W}/assimilation/ — mkdir -p; the scratch "
     f"lists are wave evidence)? Verdict per candidate: admit-candidate / refuse / hold with reason + flip condition. Adopt nothing.",
     "VERDICT: package-<n_admit>-admit-<n_refuse>-refuse-<n_hold>-hold"),
    # ---- connectors (3) ----
    ("R37ConnSibling", "connector", ["adjacency"],
     "Sibling-overlap scan (read-only) for round-37 surfaces: which fleet lanes (/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md, "
     "corpus/README.md, SKILL.md) claim Terminal-Bench task graders, service/sysadmin task verification (nginx/git/ssh), sandboxing graders "
     "(bubblewrap, network namespaces), or mutation testing of their own gates/counters? For each hit: contested / adjacent / none with "
     "file:line. Name any sibling instrument kengaku should cite rather than duplicate (e.g. a sibling mutation harness).",
     "VERDICT: sibling-<contested>-contested-<adjacent>-adjacent"),
    ("R37ConnPattern", "connector", ["calibration", "coverage"],
     f"Cross-claim pattern finder: C1 measures whether the lane's own gate checks are observable (silence mutants vs fixtures); C2 finds that a "
     f"benchmark grader's check is spoofable because its verdict is a substring of output that echoes the input. Read {GATE}, {C1}, {C2}, "
     f"{CAP}/verify.sh and the round-35/36 entries ({L}/corpus/knowledge/tb2-protein-assembly-grader.md, tb2-regex-log-grader.md). Does the "
     f"lane's own gate or counters have the C2 failure class (a verdict read from text that the checked artefact controls — e.g. a counter "
     f"grepping `PREDICATE … pass` in output an instrument could print)? List every such site with file:line and whether a fixture could "
     f"spoof it. Also: across the three TB2 graders, which grader classes recur, and what is the smallest cross-grader rule they share?",
     "VERDICT: pattern-<n>-spoofable-sites-<n>-shared-rules"),
    ("R37ConnDefects", "connector", ["calibration", "adjacency"],
     f"Cross-round defect-class map (read-only): every routed defect in {L}/corpus/lessons/round-3[0-6]-verifier-spotcheck.md; classify "
     f"(counter-accepts-junk, digest/anchor transcription, receipt drift, scratch leaks, report-before-commit, wave-2 not run, ...); count "
     f"recurrences; state which classes this round's C1/C2/anchor sweep address with a mechanical check and which recur with none. "
     f"considerthese/2026-10-25.md proposal 2(b) (block pre-registration at the second recurrence): what is the smallest honest implementation?",
     "VERDICT: classes-<n>-recurring-<n>-unchecked-<n>"),
    # ---- critics (4) ----
    ("R37CritC1Battery", "critic", ["calibration"],
     f"Attack the C1 counter {C1} as a measurement: can a battery reach `killed=55` WITHOUT single-defect fixtures that test the advertised "
     f"class? Try: fixtures that make the gate crash or time out only under a mutant; fixtures that exploit the renamed run; fixtures whose "
     f"probe (P10 re-run executes fixture code!) can see the mutated gate via /proc and change output; a fixture whose declared defect set is "
     f"right but whose kill comes from a different clause than the mutant's. Build each attempt as a battery module under {B}/R37CritC1Battery/ "
     f"and run the counter with --battery-dir/--only in dev mode. Report what the counter catches (null_detected, invalid(mutant file changed), "
     f"wrong) and what it does not.",
     "VERDICT: c1-counter-gameable-<yes|no>-<n>-attacks"),
    ("R37CritC2Counter", "critic", ["calibration"],
     f"Attack the C2 counter {C2}: find the cheapest package that passes V1-V7 WITHOUT the claimed understanding — e.g. an entry whose quotes "
     f"are verbatim but whose prose claims the opposite of the receipt, a requirement map that labels consistently with the receipt but maps the "
     f"wrong instruction lines, teaches cells of distinct filler. Build it in a fixture clone (copy the real receipt; it is committed) and score "
     f"it. Then try a receipt-side attack: a receipt edited consistently with V4 but not reproducible (V2's P10 must catch it). Report exact "
     f"bytes and outputs; a passing filler package is a decisive limit finding, not a failure of your seat.",
     "VERDICT: cheapest-filler-c2-<defects>-defects"),
    ("R37CritCases", "critic", ["coverage", "calibration"],
     f"Attack the 22 frozen probe cases ({PROBE} CASES; receipt {E37}/git-webserver-probe.txt): does each case isolate ONE grader mechanism or "
     f"requirement, or are some confounded (e.g. wrong-port-8081 is also 'nothing on :8080', identical to no-server; trailing-space vs crlf)? "
     f"Is any `requirement` label wrong about which verify.sh line decides it (open {CAP}/verify.sh with cat -n)? Which instruction.md lines and "
     f"which verify.sh branches have NO case (e.g. the HEAD/GET split, :62 echo of a multi-line body, a body of 'hello world' plus a second "
     f"line)? Write predictions for 4 uncovered cases first, then run them with the probe's machinery (import run_case/Case from the probe in a "
     f"script under {B}/R37CritCases/; scratch under {SCR}/R37CritCases).",
     "VERDICT: cases-<n>-confounded-<n>-uncovered-extra-<n_matched>/4"),
    ("R37CritScope", "critic", ["adjacency", "coverage"],
     f"Attack C2's axis and scope: is a third TB2 grader new surface (coverage) or the same instrument on new inputs (quality work — "
     f"addendum §9: name the axis by the surface changed)? The claim says the new surface is the grader CLASS (verdict = stdout substring over "
     f"a helper script probing a live service). Test that against the round-35/36 entries and {L}/corpus/README.md coverage map. Does running "
     f"a sysadmin task's verifier in a sandbox cross {L}/PROVINCE.md refusals? What wording must the entry use so it claims no task validity, "
     f"no exploit recipe beyond what the receipt shows, and no agent performance? Give exact wording fixes.",
     "VERDICT: scope-<inside|crosses>-<n>-wording-fixes"),
    ("R37MutProbeHarness", "mutation-tester", ["calibration", "operability"],
     f"Mutation-test the frozen probe harness {PROBE} in COPIES under {SCR}/R37MutProbeHarness/ (a mini lane tree: plans/ + "
     f"corpus/evidence/round37/; never edit the lane): (a) flip one case's prediction — mismatches=1 and the CASE line says match=NO; "
     f"(b) tamper one byte of the copied verify.sh — the probe must refuse with exit 2 before any case; (c) drop `--unshare-net` — does any "
     f"verdict change, and could a host service on :8080 leak into a case (check `ss -ltn` first; do not start anything on the host's :8080); "
     f"(d) put a stub `apt-get` and a stub `expect` that exits 0 into the case PATH — do verdicts change (they should not: verify.sh never "
     f"reads those statuses); (e) make the server write the ready file before binding — does any case go flaky over 3 runs; (f) remove the "
     f"HOME override in a copy run inside an extra throwaway HOME you set — confirm verify.sh writes <HOME>/.ssh/config (never use your real "
     f"HOME). Report detected/undetected per mutant with outputs.",
     "VERDICT: probe-harness-mutants-<detected>/6"),
    # ---- reviewers (4) ----
    ("R37RevClaims", "reviewer", ["calibration"],
     f"Review {L}/plans/round-37-claims.md against both counters ({C1}, {C2}) and the controls in {W}/claims/: is each predicate the same "
     f"sentence in plan, code and receipt label? Can any check pass on a state that does not deliver the claimed surface (false green), or "
     f"fail a truthful landing (false red: P9 clean tree on the landing clone, P10 under uv, V6 census --file, C1's dependence on knowledge/README "
     f"parity — see Separability)? Is the disclosure about the control-time probe run adequate? Are the excluded branches honestly excluded "
     f"(could the battery reach any of them)? Cite file:line.",
     "VERDICT: claims-review-<n>-false-green-<n>-false-red"),
    ("R37RevMutants", "reviewer", ["calibration"],
     f"Review the 55 frozen mutants in {C1} against {GATE}: for each, is it the branch its label names; is it killable by some single-defect "
     f"fixture under the counter's kill criterion (exit code + DEFECT clause set) — or equivalent (no fixture can change the observable result, "
     f"e.g. M10 if P4's unreadable branch is shadowed)? Prove killability claims by building the fixture or by reasoning from code with "
     f"file:line. List the equivalent ones: under the frozen kill rule they make C1 unreachable, which the report must state before the battery "
     f"lands.",
     "VERDICT: mutants-<n_killable>/55-equivalent-<n>"),
    ("R37RevProbeCode", "reviewer", ["operability", "coverage"],
     f"Code review of the frozen probe {PROBE} (sandbox, server, harness): does the bubblewrap sandbox actually isolate the host (network "
     f"namespace, HOME, /tmp, /tests read-only, ~/.ssh untouched — check `stat ~/.ssh/config` before/after a run in your scratch)? Is the "
     f"harness's direct call of test_hello_html_exists() equivalent to pytest's verdict (assertion rewriting, import side effects)? Is the "
     f"receipt deterministic by construction (no timing/path leak; the BOM/CRLF repr lines)? Any case whose server could race the grader "
     f"(ready-file before serve_forever)? Cite file:line.",
     "VERDICT: probe-review-<n>-defects-<n>-risks"),
    ("R37RevC2Counter", "reviewer", ["calibration"],
     f"Code review of {C2} against {L}/plans/round-37-claims.md: V1-V7 each — what it reads (committed bytes vs working tree), what it cannot "
     f"see, false-green/false-red paths (e.g. V3 regex on a row with two sha256 tokens; V4 when the entry names a case id as a substring of "
     f"another; V7 citing a case id in prose outside backticks; V6 --file vs --root). Cite file:line.",
     "VERDICT: c2-counter-review-<n>-false-green-<n>-false-red"),
    # ---- mutation-tester (1) ----
    ("R37MutC2Counter", "mutation-tester", ["calibration"],
     f"Mutation-test C2 checks in a fixture clone where a passing package exists (build one from {B}/R37PkgDraft/ drafts if present when you "
     f"start, else a minimal real package: entry with >=8 verbatim quotes checked by sed -n, rows S111-S113, README row+bullet, the committed "
     f"receipt). Mutants one at a time, each run with `python3 plans/round37_c2_verify.py --lane <clone>`: SHA256SUMS line removed; verify.sh "
     f"one byte; receipt one byte; receipt CASE line deleted; summary off by one; a `match=NO` line not named; probe one byte; dry table one "
     f"byte; S112 anchor digest with 63 hex; S112 with two sha256 tokens; requirement map row `enforced` citing a passing case; map missing "
     f"line 7; map citing an unknown case; quote off by one line. Report kill/survive per mutant with the DEFECT line.",
     "VERDICT: c2-mutants-<caught>/<total>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 37 wave 1 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r37 wave 1 (build + first falsifiers)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    spec = {"wave": "kengaku-r37-build",
            "milestone": "kengaku round 37 wave 1: C1 gate-mutant battery, C2 TB2 configure-git-webserver admission, frontier step",
            "reportDir": ".ufo/waves/round-37/build", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/build-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c))
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"]
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
