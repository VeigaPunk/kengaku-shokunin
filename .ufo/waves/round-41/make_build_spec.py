#!/usr/bin/env python3
"""Renders .ufo/waves/round-41/build-spec.json (wave 1 of 2, policy v1). L1 KengakuR41."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-41"
B = f"{W}/build"
SCR = "/fast/scratch/hyaku/kengaku-r41"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/constraints-scheduling"
CAP = f"{L}/corpus/evidence/round41/tb2-constraints-scheduling"
RCPT = f"{L}/corpus/evidence/round41/constraints-probe.txt"
DRY = f"{L}/corpus/evidence/round41/constraints-dry-cases-freeze.txt"
C1 = f"{L}/plans/round41_c1_verify.py"
C2 = f"{L}/plans/round41_c2_verify.py"
PROBE = f"{L}/plans/constraints_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
SPEC = f"{L}/plans/pkg-spec-r41.json"
CLAIMS = f"{L}/plans/round-41-claims.md"
TIP = f"{L}/plans/tip_receipts.py"
SRC = f"{L}/plans/sources_adopt.py"
ENTRY40 = f"{L}/corpus/knowledge/tb2-db-wal-recovery-grader.md"
SPOT = f"{L}/corpus/lessons/round-40-verifier-spotcheck.md"
P40 = f"{L}/.ufo/waves/round-40/build/R40PlanNext"
B40 = f"{L}/.ufo/waves/round-40/build"
F40 = f"{L}/.ufo/waves/round-40/falsify"
WIT = f"{W}/claims/witness"
FREEZE = "8ef8b4fc7c6302c527db90244d69aa18f53e83bf"
FIRST = "f774a87ad071122acd39ba02a9901b5b56d9910a"

HOST_RULE = (
    "Every seat must run any battery, counter attack or fixture build that can write files inside a bwrap sandbox. In "
    "that sandbox `/home/vgpnk/.local/bin` is read-only (`--ro-bind`). Never write to a shared PATH directory, `/usr`, "
    "`/etc`, or `$HOME` outside scratch.\n\n"
    "Round 40's R40CritC1Counter planted a `git` shim in `~/.local/bin`, and it broke other lanes' git for minutes. The "
    "neutralized modules `crit_git_shim.py` and `crit_ledger_selfread.py` must stay neutralized.")
ENVELOPE = ("Envelope to use for every counter/battery/fixture run: `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin "
            "/home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>` (the C1 "
            "counter adds its own read-only sandboxes inside it; nesting works).")
CLONE = (f'Fixture rule: S={SCR}/<YourSeatName>; mkdir -p "$S"; trap \'rm -rf -- "$S"\' EXIT; export TMPDIR="$S"; '
         f'git clone -q --shared {L} "$S/lane"; verify `git -C "$S/lane" rev-parse --show-toplevel` equals "$S/lane" before any '
         f'write; every git call names -C "$S/lane"; never commit there (index-only `git add` inside YOUR clone is fine — the '
         f'gate\'s P9 needs drafts staged). Any other fixture repo: D=$(mktemp -d -p "$S") && git -C "$D" init -q, and every git '
         f'call names -C "$D". Remove "$S" before you finish (copy receipts into your report dir first).')

CONTEXT = f"""# Goal
kengaku round 41 (hyaku run 9, 2026-10-26), WAVE 1 of 2 (build + first falsifiers). Lane repo: {L}.
Two claims are FROZEN at {CLAIMS} (freeze commit {FREEZE}; first recorded probe run {FIRST}) — read it first, in full.
Nothing frozen may change: not the two tools {TIP} / {SRC}, not the counters {C1} / {C2}, not the probe {PROBE}, not the
spec {SPEC}, not the gate {GATE}, not the dry table {DRY}, not the captures {CAP}/, not the receipt {RCPT}, not {W}/claims/.
- C1 calibration: 23 frozen mutants (receipts T01-T13 of tip_receipts.py; sources S01-S09, S11 of the sources_adopt.py CLI;
  MUTANTS table in {C1}: id, tool, class, direction, adv_kind, advertised sentence with file:line, witness, `old -> new`).
  At freeze no committed fixture kills any of them ({W}/claims/control-c1-nothing.txt: `killed=0 survived=23`). The work:
  plans/battery41 modules until `python3 plans/round41_c1_verify.py --lane .` prints `MUTANTS total=23 killed=23 survived=0
  invalid=0 null_detected=0` and `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`. Module contract (counter docstring):
  module-level FIXTURES = [{{"fid", "tool": "receipts"|"sources", "expect": "accept"|"reject"|"error"|"exit-3".."exit-9",
  "defects": [exact class set the UNMODIFIED tool prints — receipts only: `map:<rel>:<origin>`, `skip:<rel>:<reason>`,
  `equal:<rel>`, `differ:<rel>`, `control:<verdict>`; sources: always []], "build": build}}]; build(ctx, d) fills the EMPTY
  directory d and returns the tool argv tail as a list of str. ctx: ctx.init(dest) (git init -b master), ctx.git(repo, *args)
  (commits as `fixture`), ctx.write(path, text), ctx.sh(*argv, cwd=); every path inside d. NO lane clone is offered. Every
  absolute argv path must lie inside d; `{{WORK}}` → a fresh absent scratch path, `{{WORK}}/<rel>` → a path in a fresh empty dir.
  Builds run in `bwrap --ro-bind / /` with the lane hidden; tool runs in `bwrap --ro-bind / /` with a fixed system PATH (no
  `uv`). Module source must not contain any SIDECHANNEL token of the counter (case-insensitive, also in comments/strings):
  `/proc ppid cmdline psutil environ fsmonitor hookspath filter. gitattributes core. alias. setsid daemon fork nohup socket
  /home/ .local __file__ inspect importlib sys.path ctypes chmod`. Directions: silence / rc-silence / rc-mirror / error and
  exact exit pairs `A>B` (docstring). Pre-freeze witnesses: {WIT}/w_receipts.py, {WIT}/w_sources.py, {W}/claims/witness-run.txt
  (23/23 killed). The battery may NOT import, copy or read the witness modules at run time, and must not be a renamed copy of
  them: write your own fixtures (reading the witnesses to learn reachability is fine). The silence classes name fixed paths
  (T09/T10: `corpus/evidence/r/foo-probe.txt`; T11: `corpus/evidence/round35/tb2-grader-probe.txt`; T12:
  `corpus/evidence/r/foo-probe.log`), so those fixtures must use them. Develop with `python3 {C1} --lane "$S/lane"
  --battery-dir <your battery dir> --only <ids> --work "$S/w"` (prints `PREDICATE C1 n/a`); a full run takes ~5 s.
- C2 coverage: pinned Terminal-Bench 2.0 `constraints-scheduling` grader (terminal-bench-2 @ {PIN}) to be admitted as
  corpus/knowledge/tb2-constraints-scheduling-grader.md with rows S122 (tests/test_outputs.py, sha256 1422b345…) and S123
  (instruction.md, sha256 342def78…), tier A, status mined, opened 2026-10-26; S124 = TB2.1 PR #245 (tier B, open it live).
  Captures {CAP}/ (test_outputs.py, instruction.md, solve.sh = oracle, test.sh, task.toml, Dockerfile, README.md, three input
  calendars) + SHA256SUMS. Receipt {RCPT}: 25 cases, `cases=25 observed_pass=6 observed_fail=19 mismatches=2` (the two pilot
  mismatches `later-valid-wed-1105`, `seconds-30`, carried verbatim), `regrade cases=25 differ=0`, second run byte-equal.
  Counter {C2} = round-40's V1-V7 re-pointed plus V8 (order gate). V7 derives each requirement-map label from ALL receipt cases
  whose `violates=` carries the tag (all fail → enforced, all pass → unenforced, mixed → partly); map row
  | `instruction.md:<L>` | `<tag>` | <label> | `case-id`, ... | with the tag's frozen line from the dry table's TAG lines.
  Headline observations (receipt): the only valid 1-hour slots are Wed 11:00 and Thu 11:00 (L1 hand reading, probe docstring);
  `decoy-first-vevent` passes 3/3 with the attendee meeting at Fri 15:00 (published: TB2.1 PR #245); the earliest test passes
  invalid earlier slots (`bob-start-0900-wed`, `wed-1059-overlaps-alice`: tests=PFP); rewriting all three input calendars with
  CRLF line ends passes 3/3 (`input-crlf-rewrite`) although instruction.md:17-18 says any modification fails, because the
  integrity check compares `read_text()` (universal newlines); RFC 5545-valid forms fail the structure test (`folded-attendee-
  line`, `lowercase-property-names`: FPP; `dtstart-value-datetime`: FFF) while CRLF output passes; `duration-90min` fails only S.
- Round-40 closure routed items: {SPOT} §5 (R1-R5).

# Host-safety rule (orchestrator, verbatim; binding for every seat that touches the C1 counter, and for all seats)
{HOST_RULE}
{ENVELOPE}

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report dir is {B}/; drafts and receipts go under {B}/<YourSeatName>/ (create it). Never copy a corpus/ or
  plans/ tree, a lane mirror, or a clone into {B}/.
- Scratch (operator directive 2026-10-25): clones, fixtures and work trees live ONLY under {SCR}/<YourSeatName>/ (NVMe), never
  under /tmp; pass it explicitly (export TMPDIR, --work); delete it before you finish (`trap 'rm -rf -- "$S"' EXIT`).
- Write ONLY inside {B}/ (your report + your own subdir) and your scratch dir. NEVER edit the lane's corpus/, plans/,
  SCORECARD.md, LOG.md, README.md, SKILL.md, PROVINCE.md, SHONEN.md or any other lane file — draft for the L1, who integrates.
  Never write into {F} (fleet root), sibling lanes, the lane's jj state, or the lane's Git index. Never run git
  add/commit/stash/checkout/reset/push/pull or any mutating jj command in the lane. Seats never commit or push anywhere.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY: never write/commit/fetch there; run none of its campaign tools.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide:
  install via `uv tool` / `npx` / an official binary into ~/.local/bin (outside any bwrap run), or file nothing and say so. Never
  run pacman -Sy/-Syu/-U/-R, never name an already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat probe).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location (file:line or
  URL+section) and is <= 25 words. Do not fabricate output; if something cannot be fetched or run, say so. Timestamp (date
  +%T) any write you make outside your report dir and scratch dir — there should be none.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""


def bat(name, module, mids, hints):
    ids = ",".join(mids)
    return (name, "executor", ["calibration", "operability"],
            f"{HOST_RULE}\n\nWrite the C1 battery41 module {B}/{name}/battery/{module}.py (stdlib only; every fid starts "
            f"`{module}-`) whose fixtures ATTRIBUTABLY kill frozen mutants {ids} of {C1} in their declared directions (read each "
            f"mutant's tool, class, direction, `old -> new` there, and the tool branch it changes). Each fixture's `defects` must "
            f"equal the exact class set the UNMODIFIED tool prints on it, and its `expect` must match the reference exit code. One "
            f"fixture per behaviour, plus at least one fixture per mutant whose shape differs from the witness's (a different "
            f"receipt/registry layout, a realistic lane-shaped tree, a second trigger of the same branch); name what each fixture "
            f"demonstrates in a one-line comment. Hints: {hints} Prove it in your clone, inside the envelope: `python3 {C1} --lane "
            f"\"$S/lane\" --battery-dir {B}/{name}/battery --only {ids} --work \"$S/w\"` must print every FIXTURE line of your "
            f"module `ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0`, and each of {ids} `killed by=<your fid>`. Paste "
            f"that output. Then remove each fixture in turn and record which mutant flips to SURVIVED (load-bearing table). Finally "
            f"copy your module into \"$S/lane/plans/battery41/\" and run the FULL default counter (`python3 {C1} --lane "
            f"\"$S/lane\" --work \"$S/w2\"`); paste its MUTANT and summary lines (other mutants surviving there is expected). "
            f"Report the module's sha256.",
            f"VERDICT: battery41-{module}-killed-<k>/{len(mids)}-wrong-<w>")


ITEMS = [
    # ---- C1 battery41 executors (7) ----
    bat("R41BatRcvSetup", "r_setup", ["T01", "T02", "T05", "T07"],
        f"tip_receipts setup refusals (expect=error, reference exit 2): a lane without corpus/evidence/ (T01, T02), "
        f"`--tamper` naming an unmapped receipt (T05: the mutant dies with KeyError, exit 1), and a lane path that is a "
        f"subdirectory of a git work tree that itself carries corpus/evidence/ (T07). Witness builders: {WIT}/w_receipts.py "
        f"b_no_evidence, b_tamper_unknown, b_subdir."),
    bat("R41BatRcvRun", "r_run", ["T03", "T04", "T13"],
        f"tip_receipts re-run verdicts: a mapped probe that prints the receipt bytes but exits non-zero (T03 rc-silence, expect "
        f"reject, class `differ:<rel>`), a RECEIPTS-table `temp-paths` receipt (`corpus/evidence/round36/regex-log-probe-first-"
        f"run.txt` → `plans/regex_log_probe.py`) whose fresh output differs only in a mkdtemp path (T04 rc-mirror; class "
        f"`skip:<rel>:declared-nonreproducible-absolute-scratch-paths`), and a byte-equal receipt whose auto control answers "
        f"differ (T13 rc-mirror; classes `equal:<rel>`, `control:differ`). Probe stubs are committed `plans/<x>_probe.py` files "
        f"whose docstring carries the `python3 plans/<x>_probe.py --lane .` line. Witness builders: b_exit3, b_temp_paths, "
        f"b_control."),
    bat("R41BatRcvCtl", "r_ctl", ["T06", "T08"],
        f"tip_receipts control/dependency: an equal receipt whose control cannot run (an EMPTY committed receipt reproduced by a "
        f"probe printing nothing: `control:unavailable`, exit 1, expect reject — T06), and a mapped receipt whose `Run as:` line "
        f"starts `uv run` while `uv` is absent from the counter's fixed PATH (T08 rc-mirror: reference `skip:<rel>:dependency-"
        f"missing` exit 0, mutant runs it and exits 1). Witness builders: b_empty, b_uv."),
    bat("R41BatRcvMap", "r_map", ["T09", "T10", "T11", "T12"],
        f"tip_receipts population and mapping in `--list` mode (expect accept, silence classes with FIXED paths — see context): "
        f"one receipt stem shared by two scripts stays unmapped (T09), a derived mapping `foo-probe.txt` → `plans/foo_probe.py` "
        f"(T10), a RECEIPTS-table receipt keeps origin=table even when a derived match exists (T11), a `*probe*.log` receipt "
        f"enters the population (T12). Witness builders: b_two_scripts, b_derived, b_table, b_log."),
    bat("R41BatSrcUsage", "s_usage", ["S02", "S03", "S05", "S06"],
        f"sources_adopt.py CLI usage refusals in registry mode (expect error = exit 2): no --registry/--package (S02, mutant "
        f"exit 1), a non-ISO --access-date with --admit-ids (S03, mutant 5), --admit-ids without --entries (S05, mutant 0), an "
        f"invalid --recheck (S06, mutant 0). Registry/package files are 11-cell markdown tables (header in {SRC}:612; a real row "
        f"shape in {L}/corpus/SOURCES.md). Witness builders: {WIT}/w_sources.py b02, b03, b05, b06."),
    bat("R41BatSrcModes", "s_modes", ["S01", "S04", "S08", "S09"],
        f"sources_adopt.py mode exclusivity (expect error = exit 2): quote mode combined with --registry (S01, mutant 0), "
        f"--url-map in registry mode (S04, mutant 0), --quote-file without --artifact (S08, mutant 1), an unreadable --url-map in "
        f"quote mode (S09, mutant 9: an empty map leaves the located quote unmapped). Quote mode reads the anchor cell (index 5) "
        f"`\"...\"` spans and locates them as byte substrings of --artifact. Witness builders: b01, b04, b08, b09."),
    bat("R41BatSrcExit", "s_exit", ["S07", "S11"],
        f"sources_adopt.py refusal exits: a staged id that collides with the registry while --admit-ids asks for it (S07: "
        f"expect exit-3, mutant 0), and a requested row whose status is `queued` (valid for check(), refused by main() as "
        f"`not-mined`: S11 expect exit-5, mutant 0). Add a second S11 fixture using the other main() refusal (`not-opened-this-"
        f"round`: opened cell != --access-date, no --attest-opened). Witness builders: b07, b11."),
    # ---- C1 first falsifiers ----
    ("R41CritC1Counter", "critic", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nAttack {C1}: can a DISHONEST battery reach `MUTANTS total=23 killed=23` with `wrong=0 tampered=0 "
     f"sidechannel=0` without demonstrating the advertised behaviours (e.g. a fixture whose probe stub detects the mutant by "
     f"reading the slot file it is run beside, a probe stub that reads /proc or the variant path through the read-only root, an "
     f"argv token that escapes d, a symlink in d pointing at host paths, a build that defeats the content fingerprint)? Every "
     f"attack module lives ONLY under {B}/R41CritC1Counter/ and your scratch, and runs ONLY inside the envelope; any shim you try "
     f"must target a path inside your scratch, never a PATH directory. Report each vector: works / blocked (by which line of the "
     f"counter) with the run output. Round-40 vectors to re-try first: {B40}/R40CritC1Counter.md (A1 self-reading check, A2 PATH "
     f"git shim — the latter only as a scratch-path shim).",
     "VERDICT: c1-counter-dishonest-green-<reached|blocked>-vectors-<n>"),
    ("R41SentinelCounter", "sentinel", ["safety", "soundness"],
     f"{HOST_RULE}\n\nSecurity review of {C1}'s sandboxes (`ro_sandbox`, `build_battery`, `Runner.run`): can a build child or a "
     f"tool run (including a probe stub that tip_receipts executes from a fixture lane) write anywhere outside its work/tmp/"
     f"fixture dirs, reach the network, keep a process alive after the counter exits, read the hidden lane, or affect another "
     f"module's fixtures? Test each claim with a minimal module in your scratch, inside the envelope. Also review "
     f"{W}/claims/control-c1-hostile.txt and its module {W}/claims/hostile/h_host_writes.py: does it prove what the claims file "
     f"says? List findings with severity and the counter line that holds or fails.",
     "VERDICT: c1-sandbox-findings-<n>-high-<h>"),
    ("R41MutC1Counter", "mutation-tester", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nMutation-test the C1 counter {C1} itself: single-line mutants of its guards (`exhibits` pair/silence "
     f"branches, `path_ok`, `WORK_TOKEN`, the floors/TOTAL check, `fingerprint` content digest, sidechannel scan, the build "
     f"type check, PINS-AFTER, null run) run against the committed controls ({W}/claims/control-c1-*.txt reproduced in your "
     f"clone with the witness modules as battery, as `control-c1-witness-as-battery.txt` did) — which counter mutants does any "
     f"committed control catch? Table: mutant, caught-by, survived. Draft one extra control for each surviving guard (in your "
     f"report dir only).",
     "VERDICT: c1-counter-mutants-caught-<k>/<n>"),
    ("R41RevWitness", "reviewer", ["calibration", "discernment"],
     f"{HOST_RULE}\n\nReview the 23 frozen mutant rows of {C1} against the tools {TIP} and {SRC} and {L}/SKILL.md:573: is each "
     f"`adv` quote verbatim at its cited file:line (count words, cite misses), is each `adv_kind` right (direct vs indirect vs "
     f"none), is each declared direction what the witness run shows ({W}/claims/witness-run.txt — note T06 is killed there by "
     f"w-t03 not w-t06: is that attribution sound?), and is S10 truly rc-equivalent ({W}/claims/s10_equivalence.py/.txt)? "
     f"Re-run the witness run in your clone inside the envelope and compare byte-for-byte. Output: a per-mutant table and the "
     f"recount of the `ADVERTISED direct=21 indirect=2 none=0` line.",
     "VERDICT: mutant-rows-ok-<k>/23-adv-misquoted-<m>"),
    ("R41CritEquiv", "critic", ["calibration"],
     f"{HOST_RULE}\n\nHunt equivalents and incidental kills among the 23 frozen mutants of {C1}: for each, is there an input "
     f"where reference and mutant differ in the declared direction for the advertised reason (not a crash side effect)? Which "
     f"kills are 'incidental' (e.g. T07's mutant dying in `git clone` of a subdirectory, S02/S08 dying with tracebacks)? Is "
     f"any mutant reachable only through a crash rather than the advertised branch? Also: which advertised behaviours of the two "
     f"tools have NO mutant in the list (count them with file:line) — the claim's denominator honesty.",
     "VERDICT: equivalents-<e>-incidental-<i>-unlisted-advertised-<u>"),
    ("R41CritClaims", "critic", ["calibration", "discernment"],
     f"{HOST_RULE}\n\nAttack the frozen claims file {CLAIMS} and controls {W}/claims/: can a do-nothing or a junk artifact reach "
     f"either frozen predicate (C1 or C2)? Is `control-c1-no-mutants` really discriminating? Is the C2 before-state honest (V8 "
     f"red because the receipt was absent at freeze)? Are the claims causally separable? Is the lowest-axis choice and the "
     f"novelty sentence honest? Build the cheapest junk C2 package (filler entry + rows + README row) in your clone and run {C2}: "
     f"which checks does it pass? Report with outputs.",
     "VERDICT: claims-attack-defects-<n>-junk-c2-<checks-passed>/8"),
    # ---- C2 build ----
    ("R41PkgEntry", "scribe", ["coverage", "depth"],
     f"Draft the C2 knowledge entry at {B}/R41PkgEntry/tb2-constraints-scheduling-grader.md modelled on {ENTRY40} (same "
     f"header lines `source:` S122/S123, `verified-at:`, `recheck:`; sections Summary, Source labels, What is graded (static "
     f"reading), Located quotes, Requirement map, Findings each tied to receipt cases, Regrade, What the probe does not show, "
     f"Prior art, Negative space). Rules the gate enforces: read {GATE} (entry/quote clauses) and {SPEC} entry_rules — >=8 "
     f"located quotes at >=8 distinct locations, each 3-25 words, verbatim on the cited line of a capture in {CAP}/; the "
     f"`## Requirement map` must have exactly one row per TAG line in {DRY} with the label DERIVED per the context rule from "
     f"{RCPT}, citing only violating case ids; name BOTH match=NO cases in backticks. Every claim cites receipt case ids. No "
     f"novelty claimed for the decoy (TB2.1 PR #245). Paste your derived-label table with the receipt lines it rests on.",
     "VERDICT: entry-drafted-quotes-<n>-tags-<t>/11"),
    ("R41PkgRows", "scribe", ["coverage", "freshness"],
     f"Draft the three SOURCES.md rows for C2 in {L}/corpus/SOURCES.md's exact 11-cell schema (read rows S119-S121 as the "
     f"template; no `|` inside a cell): S122 = {RAW}/tests/test_outputs.py (code, A, anchor cell carries exactly one `sha256 "
     f"<64 hex>` token = the capture digest, a <=25-word quote with its line), S123 = {RAW}/instruction.md (docs, A), S124 = "
     f"https://github.com/harbor-framework/terminal-bench-2-1/pull/245 (docs, B; open it LIVE now with `gh api` or curl, record "
     f"state/merged/closed_at, quote <=25 words from the body). status mined, opened 2026-10-26, recheck 180d, used-by "
     f"corpus/knowledge/tb2-constraints-scheduling-grader.md. Re-fetch both raw URLs and `cmp` with the captures; paste the "
     f"digests. Then validate the three rows in a scratch copy of the registry with `/home/vgpnk/Projects/shokunin/scripts/"
     f"sources-census.sh validate --file <scratch>/SOURCES.md` and with `python3 {SRC} --quote-file <rows> --artifact <capture>`; "
     f"paste exits. Also draft the lesson `## Gate` lines (URL, access date+time, quote) for the three rows.",
     "VERDICT: rows-drafted-3-census-exit-<e>"),
    ("R41PkgProse", "scribe", ["coverage", "adjacency"],
     f"Draft the C2 prose updates (drafts only, as diffs or paste blocks under {B}/R41PkgProse/): (a) the {L}/corpus/README.md "
     f"knowledge index row for the new entry and one coverage-map bullet (read the round-40 row/bullet); (b) the §Frontier TB2 "
     f"sub-bullet narrowed to '7 of 89 read'; (c) a {L}/PROVINCE.md round-41 paragraph naming the surface and its routing "
     f"clause (what a correct schedule / RFC 5545 conformance is belongs elsewhere: name the owner or say unowned; read the "
     f"round-40 SQLite routing clause); (d) a {L}/SKILL.md decision-table section 'Scheduling-constraint TB2 grader — round 41' "
     f"citing receipt cases (read the round-40 db-wal section). Every number cites {RCPT}.",
     "VERDICT: prose-drafted-4-blocks"),
    ("R41CritProbe", "critic", ["coverage", "soundness"],
     f"Attack the C2 probe {PROBE} and receipt {RCPT}: does each case build the end state its `requirement` text says (read "
     f"`Case` rows and `apply_edit`)? Is the sandbox faithful to the task image where it matters (/app contents, the "
     f"`Path(__file__).resolve().parent.parent / 'inputs'` branch: /inputs absent in the image too? read {CAP}/Dockerfile, "
     f"test.sh, task.toml)? Are the `violates=` tags right per instruction line (contestable tags)? Is 'input-crlf-rewrite passes "
     f"although instruction.md:17-18 says any modification fails' true (re-derive by hand)? Is the probe's ground truth (valid "
     f"slots Wed/Thu 11:00 only) right? List defects with file:line.",
     "VERDICT: probe-defects-<n>"),
    ("R41CritPytest", "executor", ["coverage", "freshness"],
     f"Real-runner parity for C2: in your scratch, with `uv` (Python 3.13 as test.sh uses: `uvx -p 3.13 -w pytest==8.4.1 "
     f"pytest`), rebuild each of the 25 case end states of {PROBE} (reuse its Case table and apply_edit by importing a COPY of "
     f"the probe from your clone, writing /app into a scratch dir bound as /app in a bwrap like the probe's) and run real pytest "
     f"on {CAP}/test_outputs.py; compare per-test verdicts with {RCPT}. Paste the table and any differences. Network may be "
     f"needed to fetch the interpreter/wheels: do that OUTSIDE the case sandbox.",
     "VERDICT: pytest-parity-<k>/25"),
    ("R41CritIndep", "executor", ["coverage", "calibration"],
     f"Independent re-derivation for C2 without importing the grader: from {CAP}/*.ics compute every valid 1-hour slot under "
     f"instruction.md's constraints (your own parser), and for each of the 25 cases in {DRY} predict S/C/E from your reading of "
     f"{CAP}/test_outputs.py by hand; compare with {RCPT}. Then add 3 cases of your own (not in the table), predict, and run them "
     f"through a scratch copy of the probe (a modified COPY in your scratch, never the lane file). Paste everything.",
     "VERDICT: indep-agree-<k>/25-extra-<m>/3"),
    ("R41ScoutPriorArt", "scout", ["novelty", "coverage"],
     f"Prior art for the C2 findings: open TB2.1 PR #245 (https://github.com/harbor-framework/terminal-bench-2-1/pull/245) and "
     f"search harbor-framework/terminal-bench-2 and terminal-bench-2-1 issues/PRs (gh api search) plus public TB2 audits "
     f"(e.g. JonathanGabor/terminal-bench-2-audit) for: (1) the first-DTSTART decoy; (2) the earliest test passing an invalid "
     f"earlier slot; (3) the input-integrity check being blind to CRLF/line-ending rewrites (read_text universal newlines); (4) "
     f"RFC 5545-valid output (folding, lowercase names, VALUE=DATE-TIME) failing the grader; (5) DTEND ignored by two tests. For "
     f"each: published (URL + <=25-word quote + access time) / not found (queries listed).",
     "VERDICT: prior-art-published-<p>/5"),
    ("R41SentinelProbe", "sentinel", ["safety"],
     f"Security review of {PROBE}'s sandbox: the task's solve.sh and the grader run inside bwrap — can a case recipe or the "
     f"grader write outside /app and /tmp, reach the network, or leave a process? Check the bind list and `--die-with-parent`. "
     f"Run the probe once in your clone (`--work \"$S/w\"`) inside the envelope and diff its stdout with {RCPT} (must be "
     f"byte-equal). Report findings with severity.",
     "VERDICT: probe-sandbox-findings-<n>"),
    ("R41RevC2Counter", "reviewer", ["coverage", "soundness"],
     f"Review {C2} against plans/round40_c2_verify.py (`diff`): is the re-pointing faithful (no V1-V7 check relaxed), is V8 "
     f"sound (can a receipt committed BEFORE the claims or a pre-freeze probe run pass it? read plans/order_check.py), is the "
     f"`--work` fix right? Run it in your clone (`--work \"$S/absent/x\"` too) and paste outputs.",
     "VERDICT: c2-counter-defects-<n>"),
    ("R41MutC2Counter", "mutation-tester", ["coverage", "soundness"],
     f"Mutation-test {C2}: single-line mutants of V1-V8 (digest pins, summary agreement, mismatch naming, map derivation, order "
     f"check), each run against the committed control {W}/claims/control-c2-nothing.txt reproduced in your clone and against a "
     f"filler package you build in scratch. Table: mutant, caught-by, survived.",
     "VERDICT: c2-counter-mutants-caught-<k>/<n>"),
    ("R41MutProbe", "mutation-tester", ["coverage", "calibration"],
     f"Mutation-test the probe {PROBE} and its receipt: mutants of a case's meeting text or edit (a COPY in your scratch), of the "
     f"harness's verdict mapping, and of the grader capture (copy) — does {C2} (V2's P10 rerun, V4, V5) catch each? Table with "
     f"outputs. Also check: does the probe's `match=` column compare letters exactly?",
     "VERDICT: probe-mutants-caught-<k>/<n>"),
    # ---- frontier / routed / rider ----
    ("R41RoutedRider", "executor", ["operability", "discernment"],
     f"considerthese/2026-10-26.md proposal 1 (routed-findings burn-down) as a rider, per {F40}/F40CritPlanNext.md D7: write "
     f"{B}/R41RoutedRider/routed_open.py (stdlib; reads ONE append-only JSONL file `corpus/routed-findings.jsonl`, never "
     f"corpus/defects*.jsonl which plans/ledger_tip.py reads and round-40 C1 pins) and a seed {B}/R41RoutedRider/routed-findings.jsonl: "
     f"one row per routed item R1-R5 of {SPOT} §5 and of {L}/corpus/lessons/round-39-verifier-spotcheck.md §5 (id, source "
     f"file:line, opened_round, status open|closed|refused|blocked, closing evidence/commit or blocker, and a `check` shell "
     f"command where one exists). It prints `routed_open=<n> oldest_round=<r>` and exits 0; `--selftest` shows it able to fail "
     f"(a malformed row, a duplicate id, a closed row without evidence → exit 1). Measure each row's status at the lane tip by "
     f"command; paste outputs.",
     "VERDICT: rider-rows-<n>-open-<o>-oldest-<r>"),
    ("R41RegistryRows", "scribe", ["operability", "calibration"],
     f"Draft SKILL.md gate/probe registry rows (exact column shape of {L}/SKILL.md rows near line 573-590) for: "
     f"`round41-c1-mutants` ({C1}), `round41-c2` ({C2}), `constraints-probe` ({PROBE}), `round-close-check` "
     f"(plans/round_close.py — round-40 closure R3/D2: it is gate-shaped and has no row), and a registry note for "
     f"tip_receipts.py's derived mapping (R3). Each row's verdict map, self-test/controls, pinned values and write scope must be "
     f"verified by running the command in your clone (paste outputs; the C1 counter only inside the envelope).",
     "VERDICT: registry-rows-drafted-<n>-verified-<k>"),
    ("R41RoundCloseMut", "mutation-tester", ["operability", "calibration"],
     f"Price round-40 closure R3's residuals: plans/round_close.py's surviving mutants ({F40}/F40RoundClose.md: 6/14 caught) and "
     f"tip_receipts.py's 6 `F40TipReceipts` defects ({F40}/F40TipReceipts.md) — re-measure each at the lane tip (rounds 38/40/41 "
     f"for round_close: `python3 {L}/plans/round_close.py --lane \"$S/lane\" --round 41`), and draft the smallest fixture or "
     f"fix per item (drafts in your dir). Which can a round-42 claim freeze?",
     "VERDICT: residuals-remeasured-<n>-still-open-<o>"),
    ("R41QualityDraft", "scribe", ["discernment", "calibration"],
     f"Draft a {L}/corpus/QUALITY.md criterion from this round's mined mistake (round-41 plan predicate satisfiable with zero "
     f"work: {F40}/F40CritPlanNext.md D1/D2; fix = TOTAL/FLOORS binding shown able to fail by {W}/claims/control-c1-no-mutants.txt) "
     f"in QUALITY.md's existing criterion format (read Q27-Q30), plus a second criterion draft from round-40 closure R2 "
     f"(host-safety: attack seats run inside a read-only-PATH sandbox and timestamp host writes). Cite the evidence for each.",
     "VERDICT: quality-criteria-drafted-<n>"),
    ("R41LessonDraft", "scribe", ["discernment"],
     f"Draft {L}/corpus/lessons/round-41.md modelled on {L}/corpus/lessons/round-40.md: `## Mistakes` (class · evidence pointer · "
     f"captured-by · fix, shown able to fail) for the vacuous-predicate mistake and any other this round's freeze shows (read "
     f"{CLAIMS} §Frontier step and {W}/claims/), `## Gate` (admit/reject per source opened this round with URL, access date, "
     f"<=25-word located quote: S122 S123 opened 2026-10-26 15:19 -03; S124 pending), and a `## Routed` list from {SPOT} §5 "
     f"with each item's disposition this round. Draft only; the L1 fills the final numbers.",
     "VERDICT: lesson-drafted"),
    ("R41SourcesRecheck", "scout", ["freshness"],
     f"Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin kengaku` (or read "
     f"{L}/corpus/SOURCES.md recheck cells): rows due on or before 2026-10-26; open up to 4 due rows (else the 4 highest drift-risk "
     f"TB2 rows S105-S121) live (URL, access date, <=25-word located quote, sha256 where the row pins one) and draft each row's "
     f"status/recheck change old→new with the evidence. Also count the census W04 warnings now and say which rows cause them.",
     "VERDICT: sources-rechecked-<n>-changes-<k>-w04-<w>"),
    ("R41MergeRescreen", "scout", ["coverage", "adjacency"],
     f"Assimilation re-screen of /home/vgpnk/Projects/shokuknow/merge/kengaku/ (READ-ONLY): changed since round 40's screen "
     f"({B40}/R40MergeRescreen.md)? `git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %cI' -- merge/kengaku`. Run the id "
     f"collision check exactly as the round prompt gives it (0-3-space pattern) with outputs under {B}/R41MergeRescreen/ "
     f"(reg-ids, staged-ids, collisions) and prove the guard on a scratch registry with an indented `  | S002 |` row; derive the "
     f"quarantine slice from /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (data rows "
     f"only). Is any staged entry about scheduling/calendar graders, benchmark grader audits or mutation testing (fits this "
     f"round)? Verdict per entry admit/hold/refuse.",
     "VERDICT: merge-rescreen-admit-<a>-hold-<h>-refuse-<r>"),
    ("R41PlanNext", "scout", ["calibration", "coverage", "novelty"],
     f"Round-42 planning data walk (the L1 holds the planner seat; you supply data): price two candidates with a control executed "
     f"now — calibration: the next undemonstrated surface (mutant_direction_check.py, state_check.py main() exit-2 paths, "
     f"round_close.py, the rest of sources_adopt.py's library survivors, the anchor/ledger near-variants {F40}/F40XMutAnchor.md, "
     f"F40XMutLedgerOrder.md) measured with a cheap mutant harness; coverage/novelty: the next TB2 grader class not yet read "
     f"({P40}/tb2_screen.json; circuit-fibsqrt, schemelike-metacircular-eval, openssl-selfsigned-cert) with offline "
     f"executability, quote supply and prior art measured, and whether any C2 finding of this round is unpublished (a novelty "
     f"candidate). For each candidate state the do-nothing control that must be red. Draft a paste-ready `### Planned (round 42)`.",
     "VERDICT: plan42-drafted"),
    ("R41ExecNoHarm", "executor", ["calibration", "operability"],
     f"{HOST_RULE}\n\nNo-harm baseline at the freeze: in a clean `--shared` clone at {FIRST}, inside the envelope, run the "
     f"standing instruments and paste each verdict line + exit: plans/round40_c1_verify.py, round40_c2_verify.py, "
     f"round39_c1_verify.py, round39_c2_verify.py, round38_c2_verify.py, round37_c1_verify.py, round37_c2_verify.py, "
     f"round36_c2_verify.py, anchor_digest_check.py --lane, ledger_tip.py --source/--work, tip_receipts.py, order_check.py for "
     f"rounds 39/40/41, round_close.py --round 40/41, db_wal_probe.py (byte-compare with its receipt). Also run "
     f"`sha256sum -c {W}/claims/frozen-digests.txt` from the clone root. Write a re-runnable {B}/R41ExecNoHarm/measure.sh.",
     "VERDICT: no-harm-baseline-<k>-green-of-<n>"),
    ("R41ScoutMisroot", "scout", ["safety", "hygiene"],
     f"Host-safety and hygiene watch (round-40 closure R2): record `ls -la --time-style=full-iso /home/vgpnk/.local/bin` and its "
     f"directory mtime at start and again at the end of your run (any change? name it with its time); `git -C {F} status "
     f"--porcelain --untracked-files=all` — any file a kengaku round-41 seat wrote into the fleet root (content names kengaku/"
     f"round 41)? List scratch dirs under {SCR} with sizes and owners; any `/tmp` path a round-41 seat created? Report only; "
     f"touch nothing.",
     "VERDICT: misroot-<n>-host-writes-<h>"),
    # ---- connectors ----
    ("R41ConnSibling", "connector", ["adjacency"],
     f"Sibling-overlap scan for this round's surfaces (calendar/ICS and scheduling-constraint graders, RFC 5545 conformance, "
     f"mutation testing of a lane's own receipt/registry tools, bwrap sandboxes) across /home/vgpnk/Projects/shokunin/*-shokunin "
     f"(read-only: PROVINCE.md, SKILL.md, corpus/README.md). Name each overlap with file:line and whether kengaku should cite, "
     f"defer or report it out; who owns 'what a correct schedule is'?",
     "VERDICT: sibling-overlap-<n>"),
    ("R41ConnPattern", "connector", ["calibration", "quality"],
     f"Cross-claim pattern finding: the constraints grader reads ICS with regexes (first DTSTART in the file, case-sensitive "
     f"SUMMARY, unfolded lines) and compares inputs via text-mode reads; the tools' survivors were 'a guard removed', 'a mode "
     f"never exercised', 'a population regex'. Do the lane's OWN instruments (plans/round41_*.py, plans/constraints_probe.py, "
     f"plans/pkg_gate.py, plans/order_check.py, plans/tip_receipts.py, plans/sources_adopt.py, plans/round_close.py) carry these "
     f"shapes (first-match-wins parsing, text-mode digest, case-sensitive tokens)? List with file:line and a one-line fixture that "
     f"would expose each.",
     "VERDICT: pattern-<n>-sites"),
    ("R41ConnFrontier", "connector", ["coverage", "calibration"],
     f"Frontier/coverage check: read {L}/corpus/README.md (coverage map + §Frontier) and {L}/PROVINCE.md; is 'a grader that embeds "
     f"its own scheduling model over pinned inputs, reading ICS by regex' ground the lane did not hold (vs the six TB2 graders "
     f"admitted)? Which frontier clause narrows and how should it read; does any self-assessment line in SCORECARD/SHONEN/README "
     f"now mismatch the repo state (count them, file:line) — the round's calibration denominator outside C1.",
     "VERDICT: frontier-<new|not-new>-mismatches-<n>"),
    ("R41ConnClaims", "connector", ["calibration"],
     f"Cross-document consistency: every number and hash in {CLAIMS}, the C1/C2 counter docstrings, {W}/claims/*.txt and "
     f"{W}/first-run/ — do they agree with each other and with `git -C {L} log` (freeze/receipt hashes {FREEZE} / {FIRST}, 23 "
     f"mutants 13+10, 21 direct + 2 indirect, 25 cases, 6/19 split, 2 mismatches, 22 witness fixtures)? List every drift with "
     f"both locations.",
     "VERDICT: drift-<n>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 41 wave 1 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r41 wave 1 (build + first falsifiers)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    spec = {"wave": "kengaku-r41-build",
            "milestone": "kengaku round 41 wave 1: C1 battery41 for 23 tool mutants, C2 TB2 constraints-scheduling admission, frontier step",
            "reportDir": ".ufo/waves/round-41/build", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/build-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c))
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"] + c["sentinel"]
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
