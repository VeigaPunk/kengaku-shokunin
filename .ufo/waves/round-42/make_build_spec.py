#!/usr/bin/env python3
"""Renders .ufo/waves/round-42/build-spec.json (wave 1 of 2, policy v1). L1 KengakuR42."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-42"
B = f"{W}/build"
SCR = "/fast/scratch/hyaku/kengaku-r42"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/circuit-fibsqrt"
CAP = f"{L}/corpus/evidence/round42/tb2-circuit-fibsqrt"
RCPT = f"{L}/corpus/evidence/round42/fibsqrt-probe.txt"
DRY = f"{L}/corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt"
C1 = f"{L}/plans/round42_c1_verify.py"
C2 = f"{L}/plans/round42_c2_verify.py"
PROBE = f"{L}/plans/fibsqrt_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
SPEC = f"{L}/plans/pkg-spec-r42.json"
CLAIMS = f"{L}/plans/round-42-claims.md"
ANC = f"{L}/plans/anchor_digest_check.py"
ORD = f"{L}/plans/order_check.py"
ENTRY41 = f"{L}/corpus/knowledge/tb2-constraints-scheduling-grader.md"
SPOT = f"{L}/corpus/lessons/round-41-verifier-spotcheck.md"
B41 = f"{L}/.ufo/waves/round-41/build"
F41 = f"{L}/.ufo/waves/round-41/falsify"
F40 = f"{L}/.ufo/waves/round-40/falsify"
WIT = f"{W}/claims/witness"
FREEZE = "bc856d803576e182b6c3c12afc6b23f392071c25"
FIRST = "523b27806be0df26d2235089d845265a29f8cedf"

HOST_RULE = (
    "Every seat must run any battery, counter attack or fixture build that can write files inside a bwrap sandbox in which "
    "`/home/vgpnk/.local/bin` is read-only (`--ro-bind`). Never write to a shared PATH directory, `/usr`, `/etc`, or `$HOME` "
    "outside scratch. (Round 40: a seat planted a `git` shim in `~/.local/bin` and broke other lanes' git for minutes.)")
ENVELOPE = ("Envelope for every counter/battery/fixture run: `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin "
            "/home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>` (the C1 "
            "counter adds its own read-only sandboxes inside; nesting works). Your receipt carries that envelope line, `date +%T` "
            "before and after, and `ls -A /home/vgpnk/.local/bin | sha256sum` before and after (QUALITY Q32).")
SCRATCH = (f"Scratch rule (round-41 closure R2: a round-41 seat ran `rm -rf` on the shared round root and destroyed other seats' "
           f"work): S={SCR}/<YourSeatName>; mkdir -p \"$S\"; trap 'rm -rf -- \"$S\"' EXIT; export TMPDIR=\"$S\". You may delete ONLY "
           f"inside your own \"$S\" — before ANY `rm -rf`, check the target starts with \"$S/\" or equals \"$S\"; never delete "
           f"{SCR} itself, its `.ROUND-ROOT-SENTINEL`, or another seat's dir. Never use /tmp for anything over 50 MB.")
CLONE = (f'Clone rule: git clone -q --shared {L} "$S/lane"; verify `git -C "$S/lane" rev-parse --show-toplevel` equals "$S/lane" '
         f'before any write; every git call names -C "$S/lane"; never commit there (index-only `git add` inside YOUR clone is fine). '
         f'Any other fixture repo: D=$(mktemp -d -p "$S") && git -C "$D" init -q, and every git call names -C "$D". Copy receipts '
         f'into your report subdir before you finish.')

CONTEXT = f"""# Goal
kengaku round 42 (hyaku run 9, 2026-10-26), WAVE 1 of 2 (build + first falsifiers). Lane repo: {L}.
Two claims are FROZEN at {CLAIMS} (freeze commit {FREEZE}; first recorded probe run {FIRST}) — read it first, in full.
Nothing frozen may change: not the tools {ANC} / {ORD}, not the counters {C1} / {C2}, not the probe {PROBE}, not the spec
{SPEC}, not the gate {GATE}, not the dry table {DRY}, not the captures {CAP}/, not the receipt {RCPT}, not {W}/claims/.
- C1 calibration: 14 frozen mutants (anchor_digest_check.py X1 X3 X6 X7 X9 X12 X13 X14 X15; order_check.py XO1 XO3 XO5 XO6 XO7;
  MUTANTS table in {C1}: id, tool, class, direction, adv_kind, advertised sentence with file:line, round-40 source, `old -> new`).
  They are the round-40 wave-2 near-variants battery40 left alive. At freeze no battery42 exists ({W}/claims/control-c1-nothing.txt:
  `killed=0 survived=14`). The work: plans/battery42 modules until `python3 plans/round42_c1_verify.py --lane .` prints `MUTANTS
  total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0` and `MUTANTS-BY-TOOL anchor=9/9 order=5/5`. NEW this round:
  a kill counts only when ATTRIBUTED — a traced re-run of the mutant on the killing fixture reproduces the result AND executes a
  line of the replaced span (else `UNATTRIBUTED`). Module contract (counter docstring): module-level FIXTURES = [{{"fid", "tool":
  "anchor"|"order", "expect": "accept"|"reject"|"error", "defects": [exact class set the UNMODIFIED tool prints — anchor: every
  `class=<C>` of a `DEFECT ` line; order: always []], "build": build}}]; build(ctx, d) fills the EMPTY directory d and returns the
  tool argv tail as a list of str (anchor: `["--lane", <repo>]` optionally `--evidence-ref head|index`; order: `["--lane", <repo>,
  "--claims", <rel>, "--receipt", <rel>]`). ctx: ctx.init(dest) (git init -b master), ctx.git(repo, *args) (commits as `fixture` at a
  fixed date), ctx.write(path, text|bytes), ctx.sh(*argv, cwd=); every path inside d. NO lane clone is offered: build every repo
  from nothing. Every argv path (absolute OR relative) must resolve inside d. Builds and tool runs are in `bwrap --ro-bind / /`
  with a fixed system PATH. Module source must not contain any SIDECHANNEL token of the counter (case-insensitive, also in
  comments/strings): `/proc ppid cmdline psutil environ fsmonitor hookspath filter. gitattributes core. alias. setsid daemon fork
  nohup socket /home/ .local __file__ inspect importlib sys.path ctypes chmod witness settrace /run`. Directions: silence /
  rc-silence / rc-mirror / error (docstring). Pre-freeze direction modules: {WIT}/w_anchor.py, {WIT}/w_order.py,
  {W}/claims/witness-run.txt (14/14 killed, attributed). The battery may NOT import, copy or read those modules at run time and
  must not be a renamed copy of them: write your own fixtures (reading them to learn reachability is fine). Develop with
  `python3 {C1} --lane "$S/lane" --battery-dir <your battery dir> --only <ids> --work "$S/w"` (prints `PREDICATE C1 n/a`; ~2 s).
- C2 coverage: pinned Terminal-Bench 2.0 `circuit-fibsqrt` grader (terminal-bench-2 @ {PIN}) to be admitted as
  corpus/knowledge/tb2-circuit-fibsqrt-grader.md with rows S125 (tests/test_outputs.py, sha256 6117b8ed…), S126 (instruction.md,
  sha256 a7f50026…), S127 (tests/sim.c, sha256 700645ac…), tier A, status mined, opened 2026-10-26 (L1 opened all three at 17:08 -03,
  raw digests equal to the captures). Captures {CAP}/ (test_outputs.py, sim.c, instruction.md, solve.sh = oracle, test.sh, task.toml,
  Dockerfile, README.md, gates.txt = the shipped example) + SHA256SUMS. Receipt {RCPT}: 16 cases, `cases=16 observed_pass=7
  observed_fail=9 mismatches=0`, `regrade cases=16 differ=0`. Counter {C2} = round-41's V1-V8 re-pointed plus V9 content: the entry's
  `## Case table` must equal the receipt row by row — `| `<cid>` | <tests letters> | <pass|fail> | <text> |` in receipt order — every
  row id S125-S127 occurs outside its `source:` line, PROVINCE.md has a line naming both `circuit-fibsqrt` and the entry file name, and
  corpus/README.md `## Frontier` names `circuit-fibsqrt`. V7 derives each requirement-map label from ALL receipt cases whose
  `violates=` carries the tag (all fail → enforced, all pass → unenforced, mixed → partly); map row
  | `instruction.md:<L>` | `<tag>` | <label> | `case-id`, ... | with the tag's frozen line from the dry table's TAG lines.
  Grader facts (captures): test 1 `/app/gates.txt` exists; test 2 counts every line `< 32000`; test 3 runs `gcc -O3 /tests/sim.c -o
  sim` IN THE CWD, then `/app/sim N` for 28 fixed N (1,4,8,12,41,42,107,220,209,366 and x², x²-1, x²+1 for x in 12,41,42,107,220,209;
  max 48401) and compares with fib(isqrt(N)) % 2^32. sim.c reads `gates.txt` RELATIVE to its cwd, skips lines that do not scan as
  `out%d = <op>`, sets signals 0-31 from argv[1] (instruction.md:8 says stdin), prints the 32 highest-INDEXED signals
  (instruction.md:9 says "the last 32 lines"). Receipt headlines: a 1195-line lookup circuit for exactly the 28 graded inputs passes
  3/3 (`lookup-28`) though it prints 0 for the instruction's own examples 208 and 20000; padding to 31999 blank lines passes, 32000
  fails only the size test; comment lines, reversed line order and CRLF pass; trailing spaces fail (copy lines stop scanning); a fake
  executable /app/sim is overwritten by the grader's compile (`fake-sim-script` PPF); a directory named gates.txt PFF.
- Round-41 closure routed items: {SPOT} §5 (R1-R5).

# Host-safety rule (orchestrator; binding for every seat)
{HOST_RULE}
{ENVELOPE}

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report dir is {B}/; drafts and receipts go under {B}/<YourSeatName>/ (create it). Never copy a corpus/ or
  plans/ tree, a lane mirror, or a clone into {B}/; no receipt file over 1 MiB (quote it, give its sha256, delete it).
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


def bat(name, module, mids, hints):
    ids = ",".join(mids)
    return (name, "executor", ["calibration", "operability"],
            f"{HOST_RULE}\n\nWrite the C1 battery42 module {B}/{name}/battery/{module}.py (stdlib only; every fid starts "
            f"`{module}-`) whose fixtures ATTRIBUTABLY kill frozen mutants {ids} of {C1} in their declared directions (read each "
            f"mutant's tool, class, direction, `old -> new` there, and the tool branch it changes). Each fixture's `defects` must "
            f"equal the exact class set the UNMODIFIED tool prints on it, and its `expect` must match the reference exit code. One "
            f"fixture per behaviour, plus at least one fixture per mutant whose shape differs from the freeze module's (a different "
            f"row/receipt layout, a realistic multi-row registry or multi-commit history, a second trigger of the same branch); name "
            f"what each fixture demonstrates in a one-line comment. Hints: {hints} Prove it in your clone, inside the envelope: "
            f"`python3 {C1} --lane \"$S/lane\" --battery-dir {B}/{name}/battery --only {ids} --work \"$S/w\"` must print every FIXTURE "
            f"line of your module `ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0 unattributed=0`, and each of {ids} "
            f"`killed by=<your fid> attributed=...`. Paste that output. Then remove each fixture in turn and record which mutant flips "
            f"(load-bearing table). Finally copy your module into \"$S/lane/plans/battery42/\" and run the FULL default counter "
            f"(`python3 {C1} --lane \"$S/lane\" --work \"$S/w2\"`); paste its MUTANT and summary lines (other mutants surviving there "
            f"is expected). Report the module's sha256.",
            f"VERDICT: battery42-{module}-killed-<k>/{len(mids)}-wrong-<w>")


ITEMS = [
    # ---- C1 battery42 executors (5) ----
    bat("R42BatAncRoute", "a_route", ["X1", "X3", "X12"],
        f"anchor binding routes, each an ACCEPT fixture the mutant rejects (rc-mirror): a row bound only through a committed "
        f"corpus/evidence/**/PROVENANCE.md table line carrying the row id and a ticked file name (X1); a row whose pinned "
        f"raw.githubusercontent URL is named by a PROVENANCE.md URL column while no task.toml slug matches (X3); a capture dir whose "
        f"task.toml has a slash-less `name = \"<slug>\"` matched by the URL's task component (X12). Read {ANC} binding section "
        f"(docstring lines 40-75) and the route code (around lines 250-350)."),
    bat("R42BatAncClass", "a_class", ["X6", "X7", "X14"],
        f"anchor DEFECT classes (silence): a row anchored on a sibling capture's committed digest prints class=digest-wrong-capture "
        f"(X6); a made-up 64-hex token prints class=digest-unknown (X7: the mutant relabels it digest-wrong-capture); an "
        f"`Erratum (round 37): S<id> anchor sha256 ...` line in a committed corpus/lessons/*.md carrying an UPPERCASE 64-hex token "
        f"that is no committed digest prints class=erratum-digest-unresolved (X14). Read {ANC} lines 440-540."),
    bat("R42BatAncRow", "a_row", ["X9", "X13", "X15"],
        f"anchor row/ref/erratum scope (rc-silence, expect reject): a census-shaped row with 10 cells (X9 row-malformed; the "
        f"mutant only flags >11); a capture changed and STAGED beyond HEAD with the row claiming the staged digest under the default "
        f"`--evidence-ref head` (X13: the mutant defaults to index); an erratum correction token that is a committed digest of a "
        f"SIBLING row's capture, not of the capture this row names (X15). Read {ANC} lines 440-580."),
    bat("R42BatOrdClause", "o_clause", ["XO1", "XO3"],
        f"order_check.py clauses (rc-silence, expect reject, defects []): the freeze commit (first commit adding "
        f"plans/round-NN-claims.md) already contains the receipt (XO1); the receipt's FIRST adding commit is an ancestor of the freeze "
        f"commit while the freeze tree itself does not carry it — add, remove, freeze, re-add (XO3: the mutant then passes; a plain "
        f"receipt-first repo is still caught by clause 1, so it does not kill XO3). Read {ORD} lines 1-60 and 140-214."),
    bat("R42BatOrdScan", "o_scan", ["XO5", "XO6", "XO7"],
        f"order_check.py scan (defects []): an ACCEPT repo whose claims/ dir gains a `gate: P10 ok ...` blob only AFTER the receipt "
        f"commit (XO5 rc-mirror: the mutant scans to HEAD); an ACCEPT repo whose freeze-time claims/ blob carries `P10 PASS receipt "
        f"unreadable` (XO6 rc-mirror: the mutant widens the verdict alternation); a REJECT repo whose freeze-time claims/ blob "
        f"carries `CASE c1 observed=timeout` (XO7 rc-silence: the mutant narrows observed= to pass|fail). Claims dir is "
        f".ufo/waves/round-NN/claims for claims file plans/round-NN-claims.md. Read {ORD} lines 45-130."),
    # ---- C1 first falsifiers ----
    ("R42CritC1Counter", "critic", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nAttack {C1}: can a DISHONEST battery reach `MUTANTS total=14 killed=14 unattributed=0` with `wrong=0 "
     f"tampered=0 sidechannel=0` without demonstrating the advertised behaviours? Vectors to try (attack modules ONLY under "
     f"{B}/R42CritC1Counter/ and your scratch, runs ONLY inside the envelope; any shim targets a path inside your scratch, never a "
     f"PATH dir): a fixture whose repo-local .git/config makes git execute code during the tool run (pager, external diff, "
     f"`include.path`, textconv, `core.sshCommand`) — note the counter's env pins only core.fsmonitor/hooksPath; a symlinked "
     f"capture pointing at host files; a fixture that satisfies the direction through a crash rather than the advertised branch; "
     f"repairs a-c (variant store hidden, ipc, /run) re-tested with the round-41 hostile modules adapted ({F41}/F41C1Hardened/"
     f"hostile-modules/). Report each vector works/blocked with the counter line and the run output.",
     "VERDICT: c1-counter-dishonest-green-<reached|blocked>-vectors-<n>"),
    ("R42CritAttribution", "critic", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nAttack the NEW attribution leg of {C1} (TRACER, `Runner.run(trace=True)`, the `span` check in main): (1) for "
     f"mutants whose replaced line runs on EVERY invocation (XO6/XO7 module-level regex compiles, X13 the argparse default) is the "
     f"span check vacuous — what would a stronger attribution be (e.g. the mutated regex's match() returning a different value on "
     f"the killing fixture)? Measure it for those three on {W}/claims/witness/ fixtures. (2) Can tracing change the tool's result "
     f"(settrace side effects, runpy `__main__` differences, sys.argv[0], exit-code mapping of SystemExit(None/str))? Compare traced "
     f"vs untraced (rc, classes) on every freeze fixture for reference and all 14 mutants. (3) Does a multi-line replacement (X6) "
     f"count a line-event on a continuation line correctly? (4) Show {W}/claims/control-c1-attribution.txt reproduces. Report with "
     f"outputs; drafts of stronger attribution only in your dir.",
     "VERDICT: attribution-vacuous-for-<n>/14-trace-divergence-<d>"),
    ("R42SentinelCounter", "sentinel", ["safety", "soundness"],
     f"{HOST_RULE}\n\nSecurity review of {C1}'s sandboxes (`ro_sandbox`, `build_battery`, `Runner.run` incl. the tracer bound by "
     f"`--ro-bind-data` at /run/k42-tracer.py): can a build child or a tool run write outside its work/tmp/fixture dirs, reach the "
     f"network, keep a process alive after the counter exits, read the hidden lane or variant store, or affect another module's "
     f"fixtures? Test each with a minimal module in your scratch, inside the envelope. Also: git reads the fixture repo's own "
     f".git/config — which config keys can run a program during `git ls-files`/`cat-file`/`rev-list`/`log`/`ls-tree`/"
     f"`merge-base` as anchor_digest_check.py and order_check.py call them? List findings with severity and the line that holds/fails.",
     "VERDICT: c1-sandbox-findings-<n>-high-<h>"),
    ("R42MutC1Counter", "mutation-tester", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nMutation-test the C1 counter {C1} itself: single-line mutants of its guards (`exhibits` branches, `path_ok`, "
     f"the floors/TOTAL check, the attribution `span`/trace comparison, `unattributed` accounting, fingerprint, sidechannel scan, "
     f"build type check, PINS-AFTER, null run) run against the committed controls ({W}/claims/control-c1-*.txt and patches, "
     f"reproduced in your clone with the freeze modules as battery as `control-c1-witness-as-battery.txt` did). Table: mutant, "
     f"caught-by, survived. Draft one extra control per surviving guard (in your report dir only).",
     "VERDICT: c1-counter-mutants-caught-<k>/<n>"),
    ("R42RevMutRows", "reviewer", ["calibration", "discernment"],
     f"{HOST_RULE}\n\nReview the 14 frozen mutant rows of {C1} against {ANC} and {ORD}: is each `adv` quote verbatim at its cited "
     f"file:line (count words, cite misses — the lines were carried from round 40's tables), is each `adv_kind` right, is each "
     f"declared direction what {W}/claims/witness-run.txt shows, and is the XO5/XO6 relabel (rc-silence → rc-mirror) right per "
     f"{F40}/F40XMutLedgerOrder.md and {W}/claims/control-c1-direction-mislabel.txt? Re-run the witness run in your clone inside "
     f"the envelope and compare byte-for-byte (ENVELOPE lines aside). Output: a per-mutant table and the recount of `ADVERTISED "
     f"direct=13 indirect=1 none=0`.",
     "VERDICT: mutant-rows-ok-<k>/14-adv-misquoted-<m>"),
    ("R42CritEquiv", "critic", ["calibration"],
     f"Hunt equivalents and incidental kills among the 14 frozen mutants of {C1}: for each, is there an input where reference and "
     f"mutant differ in the declared direction for the advertised reason? Which kills in {W}/claims/witness-run.txt are incidental? "
     f"Then the denominator: which advertised behaviours of {ANC} and {ORD} (docstring sentences, file:line) have NO mutant in "
     f"battery40's frozen 21 ({L}/plans/round40_c1_verify.py) nor in this list — count them; and are the round-40 near-variants "
     f"left out (X2 X4 X5 X8 X10 X11 X16 XO2 XO4, XL1-XL7) honestly excluded (killed by battery40 or text-only)?",
     "VERDICT: equivalents-<e>-incidental-<i>-unlisted-advertised-<u>"),
    ("R42CritClaims", "critic", ["calibration", "discernment"],
     f"Attack the frozen claims file {CLAIMS} and controls {W}/claims/: can a do-nothing or a junk artifact reach either frozen "
     f"predicate? Is every control discriminating (C1 nothing / no-mutants / attribution / tool-edited / hostile-escape / "
     f"direction-mislabel; C2 nothing / filler)? Build an INFORMED filler for C2 in your clone (entry that copies the receipt into a "
     f"case table, a one-line PROVINCE/README mention, rows with real digests, but no analysis) and run {C2}: which of V1-V9 does it "
     f"pass? Is V9 a content check or a format check — say what it cannot see. Are the claims causally separable? Is the lowest-axis "
     f"choice honest? Report with outputs.",
     "VERDICT: claims-attack-defects-<n>-informed-filler-<checks-passed>/9"),
    # ---- C2 build ----
    ("R42PkgEntry", "scribe", ["coverage", "depth"],
     f"Draft the C2 knowledge entry at {B}/R42PkgEntry/tb2-circuit-fibsqrt-grader.md modelled on {ENTRY41} (same header lines "
     f"`source:` S125/S126/S127 with the pinned raw URLs {RAW}/tests/test_outputs.py, {RAW}/instruction.md, {RAW}/tests/sim.c; "
     f"`verified-at: 2026-10-26`; `recheck:`; sections Summary, Source labels, What is graded (static reading of test_outputs.py AND "
     f"sim.c), Located quotes, Requirement map, Case table, Findings each tied to receipt cases, Regrade, What the probe does not show, "
     f"Prior art, Negative space with a falsifier). Rules the gate enforces: read {GATE} (entry/quote clauses) and {SPEC} entry_rules — "
     f">=8 located quotes at >=8 distinct locations, each 3-25 words, verbatim on the cited line of a capture in {CAP}/ (quote table "
     f"shape as in {ENTRY41}); the `## Requirement map` has exactly one row per TAG line in {DRY} with the label DERIVED per the "
     f"context rule from {RCPT}, citing only violating case ids; the `## Case table` equals the receipt's 16 CASE lines in order "
     f"(`| `<cid>` | <letters> | <pass|fail> | <what> |`). Every claim cites receipt case ids. No novelty claimed. Validate your "
     f"draft in your clone: copy it to corpus/knowledge/, run `python3 {GATE} package --root \"$S/lane\" --spec <effective spec>` "
     f"(fill receipt_sha256) and the C2 counter's V7/V9 functions; paste outputs.",
     "VERDICT: entry-drafted-quotes-<n>-tags-<t>/7-case-rows-<c>/16"),
    ("R42PkgRows", "scribe", ["coverage", "freshness"],
     f"Draft the three SOURCES.md rows for C2 in {L}/corpus/SOURCES.md's exact 11-cell schema (read rows S122-S124 as the "
     f"template; no `|` inside a cell): S125 = {RAW}/tests/test_outputs.py (code, A, anchor cell carries exactly one `sha256 <64 hex>` "
     f"token = the capture digest plus a <=25-word quote with its line), S126 = {RAW}/instruction.md (docs, A), S127 = {RAW}/tests/sim.c "
     f"(code, A). status mined, opened 2026-10-26, recheck 180d, used-by corpus/knowledge/tb2-circuit-fibsqrt-grader.md; teaches cells "
     f"pairwise distinct, >=8 words. Re-fetch the three raw URLs and `cmp` with the captures; paste digests and access time. Validate "
     f"the rows in a scratch copy of the registry with `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "
     f"<scratch>/SOURCES.md` and with {L}/plans/anchor_digest_check.py on your clone after staging; paste exits. Draft the lesson "
     f"`## Gate` lines (URL, access date+time, quote) for the three rows.",
     "VERDICT: rows-drafted-3-census-exit-<e>"),
    ("R42PkgProse", "scribe", ["coverage", "adjacency"],
     f"Draft the C2 prose updates (drafts only, as paste blocks under {B}/R42PkgProse/): (a) the {L}/corpus/README.md knowledge "
     f"index row for the new entry citing S125 S126 S127, and one coverage-map bullet naming the entry file and "
     f"`evidence/round42/fibsqrt-probe.txt` (read the round-41 row/bullet); (b) the `## Frontier` TB2 sub-bullet narrowed to '8 of 89 "
     f"read' naming circuit-fibsqrt; (c) a {L}/PROVINCE.md round-42 paragraph — ONE line must name both `circuit-fibsqrt` and "
     f"`tb2-circuit-fibsqrt-grader.md` — with a routing clause (digital-logic/circuit correctness and C simulator semantics belong "
     f"elsewhere: name the owner or say unowned; read the round-41 routing clause); (d) a {L}/SKILL.md decision-table section "
     f"'Simulator-executed data-artefact TB2 grader — round 42' citing receipt cases. Every number cites {RCPT}.",
     "VERDICT: prose-drafted-4-blocks"),
    ("R42CritProbe", "critic", ["coverage", "soundness"],
     f"Attack the C2 probe {PROBE} and receipt {RCPT}: does each case build the end state its `requirement` text says (read `Case` "
     f"rows, `lookup()`, `run_case`)? Is the sandbox faithful to the task image where it matters (cwd /app as Dockerfile WORKDIR and "
     f"test.sh; /app seeded with sim.c and gates.txt as the Dockerfile COPY lines; /tests holding sim.c; read {CAP}/Dockerfile, "
     f"test.sh, task.toml)? Are the `violates=` tags right per instruction line (contestable: `last-32-lines` on reversed lines, "
     f"`line-form` on comment lines, no tag on trailing spaces)? Re-derive by reading {CAP}/sim.c why trailing spaces break copies "
     f"and why CRLF does not. List defects with file:line.",
     "VERDICT: probe-defects-<n>"),
    ("R42CritPytest", "executor", ["coverage", "freshness"],
     f"Real-runner parity for C2: in your scratch, with `uv` (Python 3.13 as test.sh uses: `uvx -p 3.13 -w pytest==8.4.1 pytest`), "
     f"rebuild each of the 16 case end states of {PROBE} (import a COPY of the probe from your clone and reuse its Case table and "
     f"`run_case` staging, with /app bound in a bwrap like the probe's, cwd /app) and run real pytest on {CAP}/test_outputs.py bound "
     f"at /tests; compare per-test verdicts with {RCPT}. Paste the table and differences. Network for the interpreter/wheels OUTSIDE "
     f"the case sandbox.",
     "VERDICT: pytest-parity-<k>/16"),
    ("R42CritIndep", "executor", ["coverage", "calibration"],
     f"Independent re-derivation for C2 without the grader or sim.c binary: write your own Python model of {CAP}/sim.c semantics "
     f"(parse rules incl. sscanf behaviour on trailing spaces/CRLF/comments, event-driven steps, output = 32 highest-indexed signals) "
     f"and predict all 16 cases' three letters from your reading of {CAP}/test_outputs.py; compare with {RCPT}. Then add 3 cases of "
     f"your own (e.g. a 32-bit general circuit that is wrong only above 48401, an `out32000` line, a duplicate gate definition), "
     f"predict, and run them through a modified COPY of the probe in your scratch (never the lane file). Paste everything.",
     "VERDICT: indep-agree-<k>/16-extra-<m>/3"),
    ("R42ScoutPriorArt", "scout", ["novelty", "coverage"],
     f"Prior art for the C2 findings: search harbor-framework/terminal-bench-2 and terminal-bench-2-1 issues/PRs (`gh api -X GET "
     f"search/issues -f q='repo:<r> circuit-fibsqrt'` etc.), HF copies (zai-org/terminal-bench-2-verified) and public TB2 audits "
     f"(JonathanGabor/terminal-bench-2-audit) for: (1) a lookup/hard-coded circuit passing the 28 fixed inputs; (2) instruction.md "
     f"saying stdin where sim.c reads argv; (3) 'the last 32 lines' vs the 32 highest-indexed signals; (4) the instruction's examples "
     f"208/20000 not being graded; (5) the grader compiling sim into the cwd and running /app/sim; (6) whitespace sensitivity of "
     f"sim.c's parser. For each: published (URL + <=25-word quote + access time) / not found (queries listed). Also: is the "
     f"grader on TB2.1 main byte-identical to the pin (sha256)?",
     "VERDICT: prior-art-published-<p>/6"),
    ("R42ScoutHarborCwd", "scout", ["coverage", "freshness"],
     f"The probe assumes the verifier runs test.sh with cwd /app (Dockerfile `WORKDIR /app`; test.sh refuses `/`). sim.c reads "
     f"`gates.txt` relative to the cwd and the grader compiles `./sim` in the cwd but runs `/app/sim`. Find, in the Harbor/"
     f"terminal-bench harness source (github.com/laude-institute/harbor or the TB2 docs; read-only, cite file:line at a commit), how "
     f"the verifier invokes tests/test.sh: which working directory, which user, are /tests copied in after the agent finishes? "
     f"If the cwd can differ from /app, which receipt cases would change? Report with URLs, commit pins and quotes.",
     "VERDICT: harbor-cwd-<app|other|unknown>"),
    ("R42SentinelProbe", "sentinel", ["safety"],
     f"Security review of {PROBE}'s sandbox: the task's solve.sh, gcc and the compiled sim run inside bwrap — can a case recipe, a "
     f"gates.txt or the grader write outside /app and /tmp, reach the network, or leave a process? Check the bind list and "
     f"`--die-with-parent`. Run the probe once in your clone (`--work \"$S/w\"`) inside the envelope and `cmp` its stdout with {RCPT} "
     f"(must be byte-equal). Report findings with severity.",
     "VERDICT: probe-sandbox-findings-<n>-rerun-<equal|differ>"),
    ("R42RevC2Counter", "reviewer", ["coverage", "soundness"],
     f"Review {C2} against {L}/plans/round41_c2_verify.py (`diff`): is the re-pointing faithful (no V1-V8 check relaxed; every "
     f"capture pin right — recompute), is V9 sound (CASE_ROW regex, receipt parse, the `source:` exclusion, PROVINCE/README checks; "
     f"can V9 pass with a receipt and entry that disagree?), is V8 still sound for this round's file names? Run it in your clone "
     f"(`--work \"$S/absent/x\"` too) and paste outputs.",
     "VERDICT: c2-counter-defects-<n>"),
    ("R42MutC2Counter", "mutation-tester", ["coverage", "soundness"],
     f"Mutation-test {C2}: single-line mutants of V1-V9 (digest pins, summary agreement, mismatch naming, map derivation, order "
     f"check, V9 case-table equality and surface checks), each run against the committed controls {W}/claims/control-c2-nothing.txt "
     f"and {W}/claims/c2_filler_control.py reproduced in your clone. Table: mutant, caught-by, survived; draft a control per survivor.",
     "VERDICT: c2-counter-mutants-caught-<k>/<n>"),
    ("R42MutProbe", "mutation-tester", ["coverage", "calibration"],
     f"Mutation-test the probe {PROBE} and its receipt: mutants of a case's gates generator, `lookup()` (e.g. an off-by-one in the "
     f"equality chain), the harness verdict mapping and the grader capture (copies in your scratch) — does {C2} (V2's P10 rerun, V4, "
     f"V5) catch each? Table with outputs. Also check `match=` compares letters exactly and that `regrade=` really regrades the same "
     f"end state.",
     "VERDICT: probe-mutants-caught-<k>/<n>"),
    # ---- frontier / routed / riders ----
    ("R42RoutedRider", "executor", ["operability", "discernment"],
     f"Update the routed-findings burn-down: read {L}/plans/routed_open.py and {L}/corpus/routed-findings.jsonl; draft (in "
     f"{B}/R42RoutedRider/) the rows to APPEND for the round-41 closure routed items R1-R5 ({SPOT} §5), each with source file:line, "
     f"opened_round 42, status measured NOW at the lane tip by a `check` command, and closing evidence where this round's freeze "
     f"({W}/claims/, {C1}, {C2}) closes it (R1 counter repairs, R3 V9) — and status changes for older rows as appended rows (never "
     f"edit a row). Run `python3 {L}/plans/routed_open.py --selftest` and on a scratch copy with your appended rows; paste outputs.",
     "VERDICT: routed-rows-<n>-open-<o>-oldest-<r>"),
    ("R42RegistryRows", "scribe", ["operability", "calibration"],
     f"Draft SKILL.md gate/probe registry rows (exact column shape of the round-41 rows in {L}/SKILL.md: grep `round41-c1-mutants`) "
     f"for `round42-c1-mutants` ({C1}), `round42-c2` ({C2}) and `fibsqrt-probe` ({PROBE}). Each row's verdict map, controls, "
     f"pinned values and write scope must be verified by running the command in your clone (paste outputs; the C1 counter only "
     f"inside the envelope).",
     "VERDICT: registry-rows-drafted-<n>-verified-<k>"),
    ("R42QualityDraft", "scribe", ["discernment", "calibration"],
     f"Draft two {L}/corpus/QUALITY.md criteria in its existing format (read Q29-Q32): (1) from this round's mined mistake — a "
     f"carried mutant table's directions must be re-derived through the frozen counter before freeze (round-40 table labelled XO5/XO6 "
     f"rc-silence while its witness text recorded rc 0 → 1; fix shown able to fail by {W}/claims/control-c1-direction-mislabel.txt); "
     f"(2) from round-41 closure R4 — a SOURCES row's non-mutable cell is corrected only by a new row opening `supersedes S0NN —`. Cite "
     f"the evidence for each.",
     "VERDICT: quality-criteria-drafted-<n>"),
    ("R42LessonDraft", "scribe", ["discernment"],
     f"Draft {L}/corpus/lessons/round-42.md modelled on {L}/corpus/lessons/round-41.md: `## Mistakes` (class · evidence pointer · "
     f"captured-by · fix, shown able to fail) for the XO5/XO6 direction mislabel (read {CLAIMS} §Frontier step and {W}/claims/), "
     f"`## Gate` (admit/reject per source opened this round with URL, access date, <=25-word located quote: S125 S126 S127 opened "
     f"2026-10-26 17:08 -03; at least one REJECT — e.g. the TB2 README.md capture or environment/tests copies as non-rows, with "
     f"reason and flip condition), and a `## Routed` list from {SPOT} §5 with each item's disposition. Draft only.",
     "VERDICT: lesson-drafted"),
    ("R42SourcesRecheck", "scout", ["freshness"],
     f"Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin kengaku` (or read "
     f"{L}/corpus/SOURCES.md recheck cells): rows due on or before 2026-10-26; open up to 4 due rows (else the 4 highest drift-risk TB2 "
     f"rows S120-S124 incl. S124's live PR state) live (URL, access date, <=25-word located quote, sha256 where pinned) and draft each "
     f"row's status/recheck change old→new with evidence (status/recheck/used-by only change in place; anything else needs a new "
     f"`supersedes` row). Count census W04 warnings now and name their rows.",
     "VERDICT: sources-rechecked-<n>-changes-<k>-w04-<w>"),
    ("R42MergeRescreen", "scout", ["coverage", "adjacency"],
     f"Assimilation re-screen of /home/vgpnk/Projects/shokuknow/merge/kengaku/ (READ-ONLY): changed since round 41's screen "
     f"({B41}/R41MergeRescreen.md)? `git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %cI' -- merge/kengaku`. Run the id "
     f"collision check exactly as the round prompt gives it (0-3-space pattern) with outputs under {B}/R42MergeRescreen/ (reg-ids, "
     f"staged-ids, collisions) and prove the guard on a scratch registry with an indented `  | S002 |` row; derive the quarantine "
     f"slice from /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (data rows only). Is any "
     f"staged entry about logic-circuit/simulator graders, benchmark grader audits or mutation testing (fits this round)? Verdict "
     f"per entry admit/hold/refuse.",
     "VERDICT: merge-rescreen-admit-<a>-hold-<h>-refuse-<r>"),
    ("R42PlanNext", "scout", ["calibration", "coverage", "novelty"],
     f"Round-43 planning data walk (the L1 holds the planner seat; you supply data): price two candidates with a control executed "
     f"now — calibration: the next undemonstrated surface (state_check.py main() exit-2 survivors and round_close.py rc survivors "
     f"priced by {B41}/R41PlanNext.md §2.3-2.4; the 34 unpriced advertised rows of tip_receipts.py/sources_adopt.py, "
     f"{F41}/F41CritC1Count.md) re-measured at the tip with a cheap mutant harness; coverage/novelty: the next TB2 grader class not yet "
     f"read (openssl-selfsigned-cert, schemelike-metacircular-eval, others) with offline executability, quote supply and prior art "
     f"measured, and whether any C2 finding of this round is unpublished (a novelty candidate needing a dated prior-art receipt). "
     f"For each candidate state the do-nothing control that must be red. Draft a paste-ready `### Planned (round 43)`.",
     "VERDICT: plan43-drafted"),
    ("R42ExecNoHarm", "executor", ["calibration", "operability"],
     f"{HOST_RULE}\n\nNo-harm baseline at the receipt commit: in a clean `--shared` clone at {FIRST}, inside the envelope, run the "
     f"standing instruments and paste each verdict line + exit: plans/round41_c1_verify.py, round41_c2_verify.py, round40_c1_verify.py, "
     f"round40_c2_verify.py, round39_c1_verify.py, round39_c2_verify.py, round38_c2_verify.py, round37_c1_verify.py, "
     f"round37_c2_verify.py, round36_c2_verify.py, anchor_digest_check.py --lane, ledger_tip.py, tip_receipts.py, order_check.py for "
     f"rounds 39/40/41/42, round_close.py --round 41/42, constraints_probe.py and db_wal_probe.py (byte-compare with their receipts), "
     f"routed_open.py. Also `sha256sum -c {W}/claims/frozen-digests.txt` and `sha256sum -c` of round-41's frozen digests from the "
     f"clone root. Write a re-runnable {B}/R42ExecNoHarm/measure.sh (scratch via $1).",
     "VERDICT: no-harm-baseline-<k>-green-of-<n>"),
    ("R42ScoutMisroot", "scout", ["safety", "hygiene"],
     f"Host-safety and hygiene watch: record `ls -la --time-style=full-iso /home/vgpnk/.local/bin` and its directory mtime at start "
     f"and again at the end of your run; `git -C {F} status --porcelain --untracked-files=all` — any file a kengaku round-42 seat wrote "
     f"into the fleet root (content names kengaku/round 42)? List scratch dirs under {SCR} with sizes; is {SCR}/.ROUND-ROOT-SENTINEL "
     f"present at start and end? Any `/tmp` path a round-42 seat created? Report only; touch nothing.",
     "VERDICT: misroot-<n>-host-writes-<h>-sentinel-<present|missing>"),
    ("R42ScratchGuard", "executor", ["operability", "safety"],
     f"Round-41 closure R2 asks for a scratch-root guard seats cannot silently remove. Write {B}/R42ScratchGuard/scratch_guard.py "
     f"(stdlib): `check <root>` exits 0 iff `<root>/.ROUND-ROOT-SENTINEL` exists and names the round, printing each seat dir with "
     f"size; `safe-rm <root> <seat> <path>` deletes <path> only if it resolves inside <root>/<seat> (refuses the root, the sentinel, "
     f"another seat's dir, symlink escapes, `..`), else exit 2; `--selftest` builds a scratch root and shows every refusal able to "
     f"fail. Run the selftest and `check {SCR}` (read-only); paste outputs. Draft the SKILL.md registry row.",
     "VERDICT: scratch-guard-selftest-<k>/<n>"),
    ("R42R5Carried", "executor", ["operability", "calibration"],
     f"Round-41 closure R5 carried item: `python3 {L}/plans/round_close.py --lane <clone> --census <census> --selftest --work DIR` run "
     f"twice on the same DIR exits with a CalledProcessError traceback ({B41}/R41PlanNext/round_close-selftest-second-run-traceback.txt). "
     f"Re-measure at the tip in your clone (inside the envelope), find the cause (file:line), draft the smallest fix as a patch in "
     f"{B}/R42R5Carried/ with a check command that is red before and green after, and state whether any frozen digest list "
     f"(`.ufo/waves/round-*/claims/frozen-digests.txt`) pins round_close.py (grep) — if so, say the fix must wait.",
     "VERDICT: r5-round-close-rerun-<fixed-draft|blocked>"),
    # ---- connectors ----
    ("R42ConnSibling", "connector", ["adjacency"],
     f"Sibling-overlap scan for this round's surfaces (logic-gate circuits and their simulators, C programs compiled at grading time, "
     f"benchmark graders with fixed input tables, mutation testing of a lane's own gate tools, bwrap sandboxes) across "
     f"/home/vgpnk/Projects/shokunin/*-shokunin (read-only: PROVINCE.md, SKILL.md, corpus/README.md). Name each overlap with file:line "
     f"and whether kengaku should cite, defer or report it out; who owns 'circuit correctness' and 'C simulator semantics'?",
     "VERDICT: sibling-overlap-<n>"),
    ("R42ConnPattern", "connector", ["calibration", "quality"],
     f"Cross-claim pattern finding: the fibsqrt grader checks /app/gates.txt but sim.c reads cwd-relative `gates.txt`, compiles to "
     f"`./sim` but runs `/app/sim`, and scores a fixed input table; the C1 near-variants were 'a route dropped', 'a scan bound "
     f"widened', 'a regex alternation changed'. Do the lane's OWN instruments (plans/round42_*.py, plans/fibsqrt_probe.py, "
     f"plans/pkg_gate.py, plans/order_check.py, plans/anchor_digest_check.py, plans/routed_open.py) carry these shapes (a path checked "
     f"in one form and used in another, a fixed table standing in for a general property, an alternation never exercised)? List with "
     f"file:line and a one-line fixture that would expose each.",
     "VERDICT: pattern-<n>-sites"),
    ("R42ConnFrontier", "connector", ["coverage", "calibration"],
     f"Frontier/coverage check: read {L}/corpus/README.md (coverage map + §Frontier) and {L}/PROVINCE.md; is 'a data artefact executed "
     f"by a grader-owned simulator compiled at grading time, scored on a fixed table' ground the lane did not hold (vs the seven TB2 "
     f"graders admitted)? Which frontier clause narrows and how should it read; does any self-assessment line in SCORECARD/SHONEN/README "
     f"now mismatch the repo state (count them, file:line) — the round's calibration denominator outside C1.",
     "VERDICT: frontier-<new|not-new>-mismatches-<n>"),
    ("R42ConnClaims", "connector", ["calibration"],
     f"Cross-document consistency: every number and hash in {CLAIMS}, the C1/C2 counter docstrings, {W}/claims/*.txt and "
     f"{W}/first-run/ — do they agree with each other and with `git -C {L} log` (freeze/receipt hashes {FREEZE} / {FIRST}, 14 mutants "
     f"9+5, 13 direct + 1 indirect, 16 cases, 7/9 split, 0 mismatches, 14 freeze fixtures, 9 captures)? List every drift with both "
     f"locations.",
     "VERDICT: drift-<n>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 42 wave 1 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r42 wave 1 (build + first falsifiers)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    spec = {"wave": "kengaku-r42-build",
            "milestone": "kengaku round 42 wave 1: C1 battery42 for 14 near-variant mutants, C2 TB2 circuit-fibsqrt admission, frontier step",
            "reportDir": ".ufo/waves/round-42/build", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/build-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c))
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"] + c["sentinel"]
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
