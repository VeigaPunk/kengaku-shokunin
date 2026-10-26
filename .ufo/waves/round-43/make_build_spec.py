#!/usr/bin/env python3
"""Renders .ufo/waves/round-43/build-spec.json (wave 1 of 2, policy v1). L1 KengakuR43.

Round-42 closure R6 / D1: the generator asserts the run-8 route mix before writing — m_flash-routed roles carry at
least half of the wave and attack roles at least a quarter — so a wave under either floor is never written."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-43"
B = f"{W}/build"
SCR = "/fast/scratch/hyaku/kengaku-r43"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/feal-differential-cryptanalysis"
RAW42 = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/circuit-fibsqrt"
CAP = f"{L}/corpus/evidence/round43/tb2-feal-differential-cryptanalysis"
RCPT = f"{L}/corpus/evidence/round43/feal-probe.txt"
DRY = f"{L}/corpus/evidence/round43/feal-dry-cases-freeze.txt"
C1 = f"{L}/plans/round43_c1_verify.py"
C2 = f"{L}/plans/round43_c2_verify.py"
PROBE = f"{L}/plans/feal_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
SPEC = f"{L}/plans/pkg-spec-r43.json"
CLAIMS = f"{L}/plans/round-43-claims.md"
ANC = f"{L}/plans/anchor_digest_check.py"
ORD = f"{L}/plans/order_check.py"
ENTRY42 = f"{L}/corpus/knowledge/tb2-circuit-fibsqrt-grader.md"
LESSON42 = f"{L}/corpus/lessons/round-42.md"
SPOT = f"{L}/corpus/lessons/round-42-verifier-spotcheck.md"
F42 = f"{L}/.ufo/waves/round-42/falsify"
B42 = f"{L}/.ufo/waves/round-42/build"
WIT = f"{W}/claims/witness"
ENV = f"{W}/claims/envelope.sh"
FREEZE = "02753f260805e2e45b05af22145da00f91671364"
FIRST = "6b49694d2ff533135fc238a8400f3e0dc1c82026"

HOST_RULE = (
    "Every seat must run any battery, counter attack or fixture build that can write files inside a bwrap sandbox in which "
    "`/home/vgpnk/.local/bin` is read-only. Never write to a shared PATH directory, `/usr`, `/etc`, or `$HOME` outside "
    "scratch. (Round 40: a seat planted a `git` shim in `~/.local/bin` and broke other lanes' git for minutes.)")
ENVELOPE = (f"Envelope for every counter/battery/fixture/probe run: `{ENV} \"$S/env\" <command...>` (round-43 envelope: home "
            f"read-only, ~/.cache overlaid from scratch, `date +%T` start/end, a CONTENT digest of ~/.local/bin before/after; it "
            f"exits 4 and prints `INVALID` when that digest changes — then your measurement does not count; re-run once, report "
            f"both). Paste the ENVELOPE lines with every result (QUALITY Q32).")
SCRATCH = (f"Scratch rule (round-41 closure R2): S={SCR}/<YourSeatName>; mkdir -p \"$S\"; export TMPDIR=\"$S\"; delete it when you "
           f"finish with `python3 {L}/plans/scratch_guard.py safe-rm {SCR} <YourSeatName> \"$S\"` (or `rm -rf -- \"$S\"` after checking "
           f"the target equals \"$S\"). Never delete {SCR}, its `.ROUND-ROOT-SENTINEL` or another seat's dir. /tmp only for files "
           f"under 50 MB; a /tmp path is never evidence.")
CLONE = (f'Clone rule: git clone -q --shared {L} "$S/lane"; verify `git -C "$S/lane" rev-parse --show-toplevel` equals "$S/lane" '
         f'before any write; every git call names -C "$S/lane"; never commit there. Any other fixture repo: D=$(mktemp -d -p "$S") '
         f'&& git -C "$D" init -q, and every git call names -C "$D". Copy receipts into your report subdir before you finish.')

CONTEXT = f"""# Goal
kengaku round 43 (hyaku run 9, 2026-10-26), WAVE 1 of 2 (build + first falsifiers). Lane repo: {L}.
Two claims are FROZEN at {CLAIMS} (freeze commit {FREEZE}; first recorded probe run {FIRST}) — read it first, in full.
Nothing frozen may change: not the tools {ANC} / {ORD}, not the counters {C1} / {C2}, not the probe {PROBE}, not the spec
{SPEC}, not the gate {GATE}, not the dry table {DRY}, not the captures {CAP}/, not the receipt {RCPT}, not {W}/claims/.
- C1 calibration: 9 frozen mutants (anchor_digest_check.py NA1 NA5 NA7 NA18 NA20 NA21; order_check.py NO5 NO7 NO22; MUTANTS
  table in {C1}: id, tool, class, direction, adv_kind, advertised sentence with file:line, source, `old -> new`). They are the
  round-42 wave-2 near-variants battery42 left alive ({F42}/F42XMutNear.md §3-§4). At freeze no battery43 exists
  ({W}/claims/control-c1-nothing.txt: `killed=0 survived=9`). The work: plans/battery43 modules until `python3
  plans/round43_c1_verify.py --lane .` prints `MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0 unattributed=0` and
  `MUTANTS-BY-TOOL anchor=6/6 order=3/3`. A kill counts only when ATTRIBUTED twice: the traced mutant re-run reproduces the result
  AND runs a line of the replaced span (leg f) AND the SITE RECORD differs from the reference's (leg g: for every execution of a
  replaced-span line the tracer records the frame's next event — next line + digest of the frame's locals, or the returned value;
  reference traced twice must agree). New refusals at build time: a symlink under d resolving outside d (leg h); an order
  fixture whose `--claims`/`--receipt` exists at HEAD but is not a blob (leg i); plus R1-R4 (gpg/showSignature/fsmonitor/hooksPath
  pinned, builder by fd, read-only hides, repo toplevel/core.worktree must stay in d). Module contract (counter docstring):
  module-level FIXTURES = [{{"fid", "tool": "anchor"|"order", "expect": "accept"|"reject"|"error", "defects": [exact class set the
  UNMODIFIED tool prints — anchor: every `class=<C>` of a `DEFECT ` line; order: always []], "build": build}}]; build(ctx, d) fills the
  EMPTY directory d and returns the tool argv tail as a list of str (anchor: `["--lane", <repo>]`; order: `["--lane", <repo>,
  "--claims", <rel>, "--receipt", <rel>]`). ctx: ctx.init(dest), ctx.git(repo, *args) (commits as `fixture` at a fixed date),
  ctx.write(path, text|bytes), ctx.sh(*argv, cwd=); every path inside d. NO lane clone is offered: build every repo from nothing.
  Module source must not contain any SIDECHANNEL token (case-insensitive, also in comments/strings): `/proc ppid cmdline psutil
  environ fsmonitor hookspath filter. gitattributes core. alias. setsid daemon fork nohup socket /home/ .local __file__ inspect
  importlib sys.path ctypes chmod witness settrace /run`. Pre-freeze direction module: {WIT}/w_near.py ({W}/claims/witness-run.txt:
  9/9 killed, value=differs). The battery may NOT import, copy or read that module and must not be a re-spelling of it: write
  your own fixtures with DIFFERENT shapes (reading it to learn reachability is fine; a non-author reviewer compares).
  Develop with `python3 {C1} --lane "$S/lane" --battery-dir <your battery dir> --only <ids> --work "$S/w"` (prints `PREDICATE C1
  n/a`; ~2 s), always inside the envelope.
- C2 coverage: pinned Terminal-Bench 2.0 `feal-differential-cryptanalysis` grader (terminal-bench-2 @ {PIN}) to be admitted as
  corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md with rows S129 (tests/test_outputs.py, sha256 585780e7…), S130
  (instruction.md, b4093780…), S131 (tests/feal_module.c, 1ae1c8a3…), S132 (tests/feal.c, bd4e9fb3…), S133 (tests/test.sh,
  106c2739…), S134 (README.md, 887407c7…), tier A, status mined, opened 2026-10-26 (L1 fetched all twelve files 18:40 -03).
  Captures {CAP}/ (+ SHA256SUMS; also feal.py, feal.h, setup.py, solve.sh = oracle, task.toml, Dockerfile). Receipt {RCPT}: 12
  cases, `cases=12 observed_pass=8 observed_fail=4 mismatches=0`, `regrade cases=12 differ=0`. Grader facts: test_outputs.py:20
  builds the `feal_in_c` C extension into /tests (`python setup.py build_ext --inplace`), :22-23 append /app then /tests to
  sys.path, :24 `import attack` (the agent's module, in the grader's own interpreter), :25 `import feal_in_c`, :27
  create_random_keys() (feal.c:56-67: srand(time(NULL)) once per process, key[i] = (rand() & 0xFFFF) * 1234567), :29 `stolen =
  attack.attack(feal_in_c.encrypt)`, :30 `assert feal_in_c.get_keys()[5] == stolen`; feal_module.c:51 exports get_keys; test.sh:25
  rewards pytest's exit status; nothing times the call (instruction.md:3 asks < 30 s; README.md:35 says the test "Confirms the
  attack completes within the time limit"). Passing cheats measured: import feal_in_c and return get_keys()[5]; return an object
  whose __eq__ is always True; install a fake feal_in_c in sys.modules at import; rebind feal_in_c.get_keys; os._exit(0) inside
  attack(); replay srand(time) through libc; a 45 s oracle. Failing: no attack.py, return 0, oracle+1, oracle as str. Counter {C2}
  = round-42 V1-V9 re-pointed + V10: the entry's `## Mechanism` section holds one row per receipt case in receipt order, `|
  `<cid>` | `<capture>:<line>` | “<quote>” |`, the line one of the counter's frozen DECISIVE lines for that case and the quote >=2
  words verbatim on it. V9: `## Case table` rows `| `<cid>` | <P|F> | <pass|fail> | <text> |` equal to the receipt; every row id
  S129-S134 outside its `source:` line; PROVINCE.md has ONE line naming both `feal-differential-cryptanalysis` and the entry file
  name; corpus/README.md `## Frontier` names `feal-differential-cryptanalysis`. V7: requirement-map label derived from ALL receipt
  cases whose `violates=` carries the tag (all fail → enforced, all pass → unenforced, mixed → partly); row | `instruction.md:<L>`
  | `<tag>` | <label> | `case-id`, ... | with the tag's frozen line from the dry table's TAG lines.
- Round-42 closure routed items: {SPOT} §5 (R1-R6); round-42 wave-2 routed reports under {F42}/.

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
            f"{HOST_RULE}\n\nWrite the C1 battery43 module {B}/{name}/battery/{module}.py (stdlib only; every fid starts "
            f"`{module}-`) whose fixtures ATTRIBUTABLY kill frozen mutants {ids} of {C1} in their declared directions (read each "
            f"mutant's tool, class, direction, `old -> new` there, and the tool branch it changes). Each fixture's `defects` must "
            f"equal the exact class set the UNMODIFIED tool prints on it, and its `expect` must match the reference exit code. At "
            f"least TWO fixtures per mutant with different shapes (e.g. a realistic multi-row registry or multi-commit history, a "
            f"second trigger of the same branch), none a re-spelling of {WIT}/w_near.py; one-line comment per fixture naming what it "
            f"demonstrates. Hints: {hints} Prove it in your clone, inside the envelope: `python3 {C1} --lane \"$S/lane\" "
            f"--battery-dir {B}/{name}/battery --only {ids} --work \"$S/w\"` must print every FIXTURE line of your module `ok`, "
            f"`wrong=0 tampered=0 sidechannel=0`, `null_detected=0 unattributed=0`, and each of {ids} `killed by=<your fid> "
            f"attributed=... value=differs`. Paste that output. Then remove each fixture in turn and record which mutant flips "
            f"(load-bearing table). Finally copy your module into \"$S/lane/plans/battery43/\" and run the FULL default counter "
            f"(`python3 {C1} --lane \"$S/lane\" --work \"$S/w2\"`); paste its MUTANT and summary lines (other mutants surviving there "
            f"is expected). Name every limit you hit.",
            f"VERDICT: battery43-{module}-killed-<k>/{len(mids)}-wrong-<w>")


ITEMS = [
    # ---- C1 battery43 executors (7: each mutant gets two independent modules) ----
    bat("R43BatAncRow", "a_row", ["NA1"],
        f"row-malformed on the OVER-long side (silence; expect reject, defects include row-malformed): 12-, 13- and 20-cell rows, "
        f"one in a multi-row registry beside well-formed rows. Read {ANC} :34-35 and the row loop near :477."),
    bat("R43BatAncUrl", "a_url", ["NA5", "NA18"],
        f"URL binding (rc-mirror; expect accept): a task.toml `name = \"<org>/<task>\"` WITH a slash that the URL's task component "
        f"matches exactly (NA5: the mutant keeps the org prefix in the slug); a green row whose text also carries a raw URL with a "
        f"4-6-hex commit segment that the reference ignores but the mutant binds to a different capture (NA18). Read {ANC} :48-65 "
        f"and the URL_RAW / slug code near :154 and :258."),
    bat("R43BatAncErr", "a_err", ["NA7", "NA20", "NA21"],
        f"the erratum exemption on a GREEN lane (rc-mirror; expect accept): a committed corpus/lessons/*.md line `Erratum (round 37): "
        f"S<id> anchor sha256 <wrong>` that carries the row's exact wrong anchor token AND a committed digest of the capture that row "
        f"names (NA20: exemption never granted; NA21: wrong-token membership keyed on row ids; NA7: a committed token on the erratum "
        f"line is flagged when the `t not in allowed` guard is dropped). Read {ANC} :105-116 and code near :450-470."),
    bat("R43BatOrdScan", "o_scan", ["NO5", "NO22"],
        f"order_check.py scan (rc-silence; expect reject; defects []): a claims dir whose forbidden `P10 ok ...`/`P10 DEFECT fresh "
        f"probe exit=1` line enters in a SECOND or third claims commit before the receipt (NO5: the mutant scans only the oldest "
        f"commit); a reject repo whose only forbidden evidence is a gate P10 line (no CASE line) so only the gate branch can reject "
        f"(NO22). Claims dir is .ufo/waves/round-NN/claims for plans/round-NN-claims.md. Read {ORD} :12-60 and :95-130."),
    bat("R43BatOrdExcuse", "o_excuse", ["NO7"],
        f"order_check.py excuse (rc-mirror; expect accept): a claims blob carrying the P2-shaped echo `P10 DEFECT receipt "
        f"unreadable: <path>` (with and without the `gate: ` prefix, different paths), freeze before receipt. Read {ORD} :52-60."),
    bat("R43BatAncAlt", "a_alt", ["NA1", "NA5", "NA7", "NA18", "NA20", "NA21"],
        f"a SECOND independent module for all six anchor mutants with shapes unlike the other modules: registries of 5+ rows, "
        f"captures with SHA256SUMS manifests, multi-capture rows, provenance markdown beside the URL route. Read {ANC} in full."),
    bat("R43BatOrdAlt", "o_alt", ["NO5", "NO7", "NO22"],
        f"a SECOND independent module for the three order mutants: longer histories (5+ commits), several claims files, receipts "
        f"in nested dirs, the forbidden line inside a larger blob. Read {ORD} in full."),
    # ---- C1 first falsifiers ----
    ("R43CritC1Counter", "critic", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nAttack {C1}: can a DISHONEST battery reach `MUTANTS total=9 killed=9 unattributed=0` with `wrong=0 tampered=0 "
     f"sidechannel=0` without demonstrating the advertised behaviours? Re-try the round-42 substitutes ({B42}/R42CritC1Counter.md §1: "
     f"receipt-is-directory, emptied-directory, staged-manifest) against legs h/i, a symlink INSIDE d that resolves inside d but to a "
     f"file another fixture shares, `include.path`/`core.pager`/textconv/`diff.external` keys in a fixture .git/config, a fixture "
     f"that reaches a direction through a crash. Attack modules ONLY under {B}/R43CritC1Counter/ and your scratch, runs ONLY inside the "
     f"envelope. Report each vector works/blocked with the counter line.",
     "VERDICT: c1-counter-dishonest-green-<reached|blocked>-vectors-<n>"),
    ("R43CritValueLeg", "critic", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nAttack the NEW value-attribution leg g of {C1} (TRACER: `note`, `digest`, `K43_SPAN`; main: the two reference "
     f"traces and `SITE_EQUAL`). (1) Can a record DIFFER spuriously (per-run paths the RUN regex misses, set/dict order, object reprs, "
     f"time, fixture paths) so that any span-executing hit passes leg g? Measure: run the reference twice under different `--jobs`, "
     f"PYTHONHASHSEED and scratch roots on {WIT}/w_near.py fixtures and diff the records (copy the tracer into your scratch). (2) Is "
     f"leg g vacuous for module-level spans (NA18 URL_RAW, NO7 EXECUTED_EXCUSE: the compiled regex differs on EVERY fixture)? Say "
     f"what a discriminating record would be and measure it. (3) Can tracing change a tool result (traced vs untraced rc/classes on "
     f"every witness fixture, reference and all 9 mutants)? (4) Show {W}/claims/control-c1-value.txt reproduces.",
     "VERDICT: value-leg-spurious-<n>-vacuous-<v>/9-trace-divergence-<d>"),
    ("R43SentinelCounter", "sentinel", ["safety", "soundness"],
     f"{HOST_RULE}\n\nSecurity review of {C1}: the NEW parent-side git calls (`order_argv_breach`, `repo_breach` run `git -C <fixture "
     f"repo> cat-file/rev-parse/config` in the COUNTER's own process, outside bwrap, with PIN_CHECK_ENV) — can a fixture .git/config "
     f"make those parent-side calls run a program or read/write outside d (fsmonitor/hooksPath are pinned; try `core.sshCommand`, "
     f"`include.path`, `core.alternateRefsCommand`, `uploadpack.*`, `safe.directory`, `extensions.*`, a `.git` FILE pointing elsewhere "
     f"(gitdir:)? Also the tracer's env (`K43_SPAN`) and `symlink_breach` TOCTOU. Test each with a minimal module in your scratch, "
     f"inside the envelope; never point a vector at a real path outside your scratch. Findings with severity and the line.",
     "VERDICT: c1-sandbox-findings-<n>-high-<h>"),
    ("R43MutC1Counter", "mutation-tester", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nMutation-test the C1 counter {C1}: single-line mutants of its guards (the new `SITE_EQUAL`, the two reference "
     f"traces, the newline-count validity check, `symlink_breach`, `order_argv_breach`, `repo_breach`, plus `exhibits`, floors/TOTAL, "
     f"`unattributed` accounting, fingerprint, sidechannel scan, PINS-AFTER, null run) run against the committed controls "
     f"({W}/claims/c1_controls.sh, control-c1-*.txt, hostile/*.py), reproduced in your clone. Table: mutant, caught-by, survived. Draft "
     f"one extra control per surviving guard (in your report dir only).",
     "VERDICT: c1-counter-mutants-caught-<k>/<n>"),
    ("R43RevMutRows", "reviewer", ["calibration", "discernment"],
     f"{HOST_RULE}\n\nReview the 9 frozen mutant rows of {C1} against {ANC} and {ORD}: is each `adv` quote verbatim at its cited "
     f"file:line (count words, cite misses), is each `adv_kind` right (NA18 is `indirect`), is each declared direction what "
     f"{W}/claims/witness-run.txt shows, and does each row match {F42}/F42XMutNear.md §3 (id, site, replacement)? Re-run the witness "
     f"run in your clone inside the envelope and compare (ENVELOPE lines aside). Output: per-mutant table and the recount of "
     f"`ADVERTISED direct=8 indirect=1 none=0`.",
     "VERDICT: mutant-rows-ok-<k>/9-adv-misquoted-<m>"),
    ("R43CritEquiv", "critic", ["calibration"],
     f"Hunt equivalents and incidental kills among the 9 frozen mutants of {C1}: for each, is there an input where reference and "
     f"mutant differ in the declared direction for the ADVERTISED reason? Which kills in {W}/claims/witness-run.txt are incidental "
     f"(e.g. NA7 vs NA20 vs NA21 all killed by one erratum fixture)? Then the denominator: list the advertised behaviours of {ANC} "
     f"and {ORD} (docstring sentences, file:line) that still have NO frozen mutant in rounds 40, 42 or 43 ({L}/plans/round40_c1_verify.py, "
     f"round42_c1_verify.py, round43_c1_verify.py) — recount `u` (round 42 said 18, {B42}/R42CritEquiv.md §3).",
     "VERDICT: equivalents-<e>-incidental-<i>-unlisted-advertised-<u>"),
    ("R43CritClaims", "critic", ["calibration", "discernment"],
     f"Attack the frozen claims file {CLAIMS} and controls {W}/claims/: can a do-nothing or junk artifact reach either frozen "
     f"predicate? Is every control discriminating? For C2's NEW V10: build informed fillers smarter than "
     f"{W}/claims/c2_filler_control.py's (e.g. cite the first DECISIVE line per case copied from the counter source itself, quote two "
     f"words of it) — the DECISIVE map is public in {C2}: does V10 then measure reading or copying? Say what V10 cannot see and run "
     f"{C2}'s v9/v10 on your fillers in your clone. Are C1/C2 causally separable? Is the lowest-axis choice honest?",
     "VERDICT: claims-attack-defects-<n>-v10-filler-<pass|fail>"),
    ("R43MutC2Counter", "mutation-tester", ["coverage", "soundness"],
     f"{HOST_RULE}\n\nMutation-test the NEW V10 leg and the re-pointed V9 of {C2}: single-line mutants of `v10` (DECISIVE lookup, "
     f"`int(line) not in allowed`, capture pin check, `norm`, the 2-word floor, the ids-equal check, MECH_ROW) and of `v9`'s CASE_ROW "
     f"(one letter) run against the committed control {W}/claims/c2_filler_control.py (copy it and the counter into your clone; patch "
     f"the copy) — which mutants does the filler/informed/content triple catch? Table: mutant, caught-by, survived; draft one extra "
     f"control per survivor (your report dir only).",
     "VERDICT: c2-counter-mutants-caught-<k>/<n>"),
    # ---- C2 build ----
    ("R43PkgEntry", "scribe", ["coverage", "depth"],
     f"Draft the C2 knowledge entry at {B}/R43PkgEntry/tb2-feal-differential-cryptanalysis-grader.md modelled on {ENTRY42} (header "
     f"`source:` lines S129-S134 with the pinned raw URLs {RAW}/tests/test_outputs.py, {RAW}/instruction.md, {RAW}/tests/feal_module.c, "
     f"{RAW}/tests/feal.c, {RAW}/tests/test.sh, {RAW}/README.md; `verified-at: 2026-10-26`; `recheck:`; sections Summary, Source "
     f"labels, What is graded (static reading of test_outputs.py, feal.c, feal_module.c, setup.py, test.sh), Located quotes, "
     f"Requirement map, Case table, Mechanism, Findings each tied to receipt cases, Regrade, What the probe does not show, Prior art "
     f"(leave a slot the L1 fills from R43ScoutPriorArt), Negative space with a falsifier). Rules the gate enforces: read {GATE} "
     f"(entry/quote clauses) and {SPEC} entry_rules — >=10 located quotes at >=10 distinct locations, each 3-25 words, verbatim on "
     f"the cited line of a capture in {CAP}/; requirement map one row per TAG line in {DRY}, label DERIVED from {RCPT}; case table = "
     f"the receipt's 12 CASE lines in order; `## Mechanism` per the context rule (read DECISIVE in {C2}; the row shape is exactly three "
     f"cells — say WHY each line decides its case in the Findings section). Word the class as module "
     f"import + in-process call (regex-log already executes an agent regex in-process). No novelty claimed. Validate in your clone: "
     f"copy the draft to corpus/knowledge/, run `python3 {GATE} package --root \"$S/lane\" --spec <effective spec>` (fill "
     f"receipt_sha256) and the C2 counter's v7/v9/v10 functions; paste outputs.",
     "VERDICT: entry-drafted-quotes-<n>-tags-<t>/5-case-rows-<c>/12-mechanism-<m>/12"),
    ("R43PkgRows", "scribe", ["coverage", "freshness"],
     f"Draft the six SOURCES.md rows S129-S134 for C2 in {L}/corpus/SOURCES.md's exact 11-cell schema (read rows S125-S128 as the "
     f"template; no `|` inside a cell): S129 {RAW}/tests/test_outputs.py (code), S130 {RAW}/instruction.md (docs), S131 "
     f"{RAW}/tests/feal_module.c (code), S132 {RAW}/tests/feal.c (code), S133 {RAW}/tests/test.sh (code), S134 {RAW}/README.md (docs); "
     f"tier A, anchor cell carries exactly one `sha256 <64 hex>` token = the capture digest plus a <=25-word quote with its line; status "
     f"mined, opened 2026-10-26, recheck 180d, used-by corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md; teaches cells "
     f"pairwise distinct, >=8 words. Re-fetch the six raw URLs and `cmp` with the captures; paste digests and access time. Validate in "
     f"a scratch copy of the registry with `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/SOURCES.md` "
     f"and with {ANC} on your clone after staging; paste exits. Draft the lesson `## Gate` lines (URL, access date+time, quote) for "
     f"the six rows and >=1 reject (e.g. Dockerfile or feal.py — with a flip condition that is checkable at landing).",
     "VERDICT: rows-drafted-6-census-exit-<e>"),
    ("R43PkgProse", "scribe", ["coverage", "adjacency"],
     f"Draft the C2 prose updates (paste blocks under {B}/R43PkgProse/): (a) the {L}/corpus/README.md knowledge index row for the new "
     f"entry citing S129-S134, and one coverage-map bullet naming the entry file and `evidence/round43/feal-probe.txt` (read the "
     f"round-42 row/bullet); (b) the `## Frontier` TB2 sub-bullet narrowed to '9 of 89 read' naming feal-differential-cryptanalysis; "
     f"(c) a {L}/PROVINCE.md round-43 paragraph — ONE line must name both `feal-differential-cryptanalysis` and "
     f"`tb2-feal-differential-cryptanalysis-grader.md` — with a routing clause (cryptanalysis technique and Python import-system "
     f"semantics: name the owning sibling or say unowned; read the round-42 routing clause); (d) a {L}/SKILL.md decision-table "
     f"section 'In-process module-import TB2 grader — round 43' citing receipt cases. Every number cites {RCPT}.",
     "VERDICT: prose-drafted-4-blocks"),
    ("R43CritProbe", "critic", ["coverage", "soundness"],
     f"Attack the C2 probe {PROBE} and receipt {RCPT}: does each case build the end state its `requirement` says (read CASES, the "
     f"cheat module texts, the recipe heredocs, `run_case`, `letter`)? Is the sandbox faithful where it matters (cwd /app; /tests "
     f"writable and holding the five grader files the extension build needs; `python` on PATH; sys.path order; test.sh's `$?` rule "
     f"mapped to the harness exit status; os._exit inside the test)? Are the `violates=` tags right per instruction line (contestable: "
     f"`chosen-plaintext` on clock-seed, `return-uint32` on always-equal, `recover-key5` on exit-zero)? Is `cheat-clock-seed` "
     f"robust to a slow second (it tries now..now-9)? Defects with file:line.",
     "VERDICT: probe-defects-<n>"),
    ("R43PytestParity", "executor", ["coverage", "freshness"],
     f"Real-runner parity for C2: in your scratch, with `uv` (`uvx -p 3.13 -w pytest==8.4.1 -w setuptools==80.9.0 pytest`, as "
     f"{CAP}/test.sh does), rebuild each of the 12 case end states of {PROBE} (import a COPY of the probe from your clone and reuse its "
     f"CASES/run_case staging, /app and /tests bound in a bwrap like the probe's, cwd /app, network off inside) and run REAL pytest on "
     f"/tests/test_outputs.py; record pytest's exit status per case and compare with {RCPT} (especially cheat-exit-zero, "
     f"cheat-always-equal under pytest's assertion rewriting, cheat-sysmodules-shadow). Fetch the interpreter/wheels OUTSIDE the case "
     f"sandbox. Paste the table and differences; state the python/setuptools/gcc versions used.",
     "VERDICT: pytest-parity-<k>/12"),
    ("R43CritIndep", "executor", ["coverage", "calibration"],
     f"Independent re-derivation for C2: from {CAP}/test_outputs.py, feal.c, feal_module.c and test.sh alone (not the receipt), "
     f"predict each of the 12 cases' verdict in {DRY} with the line that decides it; compare with {RCPT}. Then add 3 cases of your own "
     f"(e.g. attack returning numpy-like int subclass with __eq__, attack calling feal_in_c.create_random_keys() then get_keys()[5], "
     f"attack raising SystemExit(0)), predict, and run them through a modified COPY of the probe in your scratch (never the lane file), "
     f"inside the envelope. Paste everything.",
     "VERDICT: indep-agree-<k>/12-extra-<m>/3"),
    ("R43ScoutPriorArt", "scout", ["novelty", "coverage"],
     f"Prior art for the C2 findings: search harbor-framework/terminal-bench-2 and terminal-bench-2-1 issues/PRs (`gh api -X GET "
     f"search/issues -f q='repo:<r> feal'` etc.), public TB2 audits, HF copies and the third-party repos {B42}/R42PlanNext/prior-art/ "
     f"names (elizaOS/eliza, minghinmatthewlam/openbench, gkroiz/agent-interp-envs) for: (1) importing feal_in_c / get_keys from "
     f"attack(); (2) an always-true __eq__ return defeating `==` asserts in TB graders; (3) sys.modules shadowing of a grader module; (4) "
     f"os._exit(0) inside a pytest-graded function (reward on exit status); (5) srand(time) key prediction; (6) the 30 s limit "
     f"unenforced / README:35 false. Per finding: published / adjacent / not found, with URL, date and a <=25-word quote. Write dated "
     f"receipts (command + output) under {B}/R43ScoutPriorArt/.",
     "VERDICT: prior-art-published-<p>-adjacent-<a>-not-found-<n>"),
    # ---- routed work (round-42 closure R1-R3, R6; frontier step) ----
    ("R43ErrataFibsqrt", "scribe", ["quality", "calibration"],
     f"Closure R1 ({SPOT} §5, D4): draft an appended `## Errata (round 43)` section for {ENTRY42} correcting each wrong or overclaiming "
     f"sentence found by {F42}/F42EntryQuotes.md (4) and {F42}/F42CritOverclaim.md (the lesson pointer `fibsqrt-probe.txt:6` → `:11`). "
     f"Re-derive every correction yourself from the captures {L}/corpus/evidence/round42/tb2-circuit-fibsqrt/ and the receipt (e.g. "
     f"`test_outputs.py:73-102` grades six inputs above 2^15: list them with arithmetic) — quote the wrong sentence with its line, the "
     f"correction, and the evidence line. Never edit in place: a block to append, plus the matching lesson-correction line for "
     f"{LESSON42}. Also list any further wrong sentence you find.",
     "VERDICT: errata-drafted-<n>-new-found-<m>"),
    ("R43GateRowsR2", "scribe", ["discernment", "coverage"],
     f"Closure R2 ({SPOT} §5, D2/D3): (a) draft the missing `## Gate` row for S128 (URL, access date+time, <=25-word quote — re-open "
     f"the issue with `gh api repos/OpenAgentsInc/openagents/issues/9645` and record the time); (b) execute the Dockerfile flip: draft "
     f"a tier-B mechanism row S135 for {RAW42}/environment/Dockerfile (re-fetch, `cmp` with "
     f"{L}/corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile, anchor `sha256 <digest>` + quote of line 3 `WORKDIR /app`, status "
     f"mined, used-by {ENTRY42}) and the appended entry sentence(s) citing S135 at the cwd claims (`:65`, `:89`, `:94`, `:435-438`); (c) "
     f"validate the row in a scratch copy of the registry (census exit, the anchor tool on a clone with the row staged). Drafts only.",
     "VERDICT: gate-rows-drafted-<n>-census-exit-<e>"),
    ("R43FlipCheck", "executor", ["calibration", "operability"],
     f"Mined mistake fix (round-42 D3: a Gate reject's flip condition fired at landing and was not executed). Write "
     f"{B}/R43FlipCheck/gate_flip_check.py (stdlib): `--lesson <path>` parses the `## Gate` section's REJECT rows that carry a flip "
     f"condition (read {LESSON42} §Gate and older lessons' Gate tables for the shapes: 'flip:', 'if … admit', 'flips when'), and "
     f"requires each such row to be resolved by a later line `Flip check (round N): <item> — fired|not fired — <evidence>`; prints "
     f"`FLIPS total=<n> unresolved=<u>` and exits 1 when u>0; `--selftest` shows it red and green on built fixtures. Show it RED on "
     f"{LESSON42} (the Dockerfile row) and green on a scratch copy with the resolution line appended. Draft a QUALITY.md criterion "
     f"(next free Q-number; read {L}/corpus/QUALITY.md tail) and a SKILL registry row. Paste outputs.",
     "VERDICT: flip-check-red-on-r42-<yes|no>-selftest-<k>/<n>"),
    ("R43RoutedQueue", "scribe", ["calibration", "quality"],
     f"Closure R3: draft new rows for {L}/corpus/routed-findings.jsonl (read its schema: id, class, source, opened_round, status, "
     f"close, blocker, check, note) for every round-42 wave-2 routed item — {F42}/F42RevC2Package.md (9), F42RevLesson.md (8), "
     f"F42RevQuality.md (6), F42RevRiders.md (5), F42CritAdv.md (2), F42CritScorecard.md (1), F42ConnClaims.md (1), "
     f"F42CritPlanNext.md (5), F42EntryQuotes.md (4) — one row each with a runnable `check` where one exists. Mark the ones this round "
     f"closes by plan (R1 errata, R2 gate rows, R4/R5 counters) as open with a note; never claim a close. Validate with `python3 "
     f"{L}/plans/routed_open.py` on a scratch copy; paste output.",
     "VERDICT: routed-rows-drafted-<n>-routed_open-<k>"),
    ("R43R42Defects", "scribe", ["quality", "calibration"],
     f"Draft APPENDED corrections (never in place) for the round-42 wave-2 defects in lane docs: {F42}/F42RevLesson.md → corrections "
     f"for {LESSON42}; F42RevQuality.md → corrections for Q33/Q34 in {L}/corpus/QUALITY.md; F42CritScorecard.md and F42CritAdv.md → "
     f"SCORECARD corrections; F42RevRiders.md → rider corrections. Re-check each defect against the current file first (it may be "
     f"wrong or already fixed) and say so. Output paste blocks per target file with the exact text to append.",
     "VERDICT: r42-defects-corrections-<k>-of-<n>-refuted-<r>"),
    ("R43ExecNoHarm", "executor", ["calibration", "operability"],
     f"{HOST_RULE}\n\nNo-harm baseline at the receipt commit: in a clean `--no-local` clone at {FIRST}, inside the envelope, adapt "
     f"{L}/.ufo/waves/round-42/integrate/measure.sh into {B}/R43ExecNoHarm/measure.sh (round-43 counters first: round43_c1_verify.py, "
     f"round43_c2_verify.py, order_check.py round 43; then everything round 42's measured: rounds 36-42 counters, anchor check, census, "
     f"frozen digests r39-r43, ledger_tip, tip_receipts, routed_open, db_wal/constraints/fibsqrt probes byte-equal, round_close.py "
     f"--round 42/43) and run it; paste every verdict line + exit. Expect round-43 counters red here (no battery43, no entry).",
     "VERDICT: no-harm-baseline-<k>-green-of-<n>"),
    ("R43ScoutMisroot", "scout", ["safety", "hygiene"],
     f"Host-safety and hygiene watch: record `ls -la --time-style=full-iso /home/vgpnk/.local/bin` and its directory mtime at start "
     f"and again at the end of your run; `git -C {F} status --porcelain --untracked-files=all` — any file a kengaku round-43 seat wrote "
     f"into the fleet root (content names kengaku/round 43)? List scratch dirs under {SCR} with sizes; is {SCR}/.ROUND-ROOT-SENTINEL "
     f"present at start and end? Any /tmp path a round-43 seat created? Report only; touch nothing.",
     "VERDICT: misroot-<n>-host-writes-<h>-sentinel-<present|missing>"),
    ("R43ConsiderThese", "scout", ["coverage", "quality"],
     f"considerthese (operator input, read-only): {L}/considerthese/2026-10-26.md proposal 3 ('Batch the TB2 grader sweep … class "
     f"histogram of graded state'). Without running any task: list the 89 task dirs of terminal-bench-2 @ {PIN} (`gh api "
     f"repos/harbor-framework/terminal-bench-2/git/trees/{PIN}`), fetch each tests/test_outputs.py (raw URLs) into your scratch, and "
     f"classify what each grader reads (files / service / repo history / built artefact / DB / imported agent module / other) with "
     f"the deciding line. Mark the 9 the lane has read (circuit-fibsqrt, constraints-scheduling, protein-assembly, regex-log, "
     f"configure-git-webserver, build-pmars, git-leak-recovery, db-wal-recovery, feal-differential-cryptanalysis). Output a table + "
     f"histogram + the 3 uncovered classes most worth a round, as a lesson-ready block citing considerthese/2026-10-26.md.",
     "VERDICT: tb2-class-histogram-<n>/89-classes-<c>"),
    ("R43MergeRescreen", "scout", ["coverage", "discernment"],
     f"Assimilation re-screen (read-only on /home/vgpnk/Projects/shokuknow): has /home/vgpnk/Projects/shokuknow/merge/kengaku/ changed "
     f"since 2026-10-24 (mtimes, MERGE-REPORT.md)? Run the id-collision check into {B}/R43MergeRescreen/: registry ids from "
     f"{L}/corpus/SOURCES.md and staged ids from merge/kengaku/SOURCES.append.md, both with the 0-3-space pattern "
     f"`grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}'`, `comm -12` collisions; prove the guard once on a scratch registry with an "
     f"indented `  | S002 |` row (nonempty collisions); derive the quarantine slice from the absent-defect register "
     f"(/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md, kengaku data rows). Is any staged entry "
     f"in PROVINCE scope and on uncovered ground? Recommend adopt/none with reasons.",
     "VERDICT: merge-<changed|unchanged>-collisions-<n>-recommend-<adopt|none>"),
    ("R43PlanNext", "scout", ["calibration", "coverage"],
     f"Round-44 data walk (read-only): price the next calibration list — the `round_close.py` survivors ({B42}/R42PlanNext/"
     f"res_round_close.json, wit_rc.txt: 9 witnessed of 20 per {F42}/F42CritPlanNext.md D1) and the `u` unmutated advertised "
     f"anchor/order behaviours ({B42}/R42CritEquiv.md §3) — which have a witnessed direction today? And the next coverage task: pick from "
     f"R43ConsiderThese's classes if available, else name one pinned TB2 task whose grader class is uncovered, check oracle-offline "
     f"feasibility from its files. Write {B}/R43PlanNext.md with numbers and commands.",
     "VERDICT: plan44-calibration-<n>-mutants-coverage-<task>"),
    ("R43ReviewEnvelope", "reviewer", ["operability", "safety"],
     f"Review closure R6/D5's fix {ENV}: does the content digest catch a content rewrite of an existing ~/.local/bin entry, a new "
     f"file, a symlink retarget, a mode change? Test on a COPY of the script with the target dir replaced by a scratch dir you mutate "
     f"(never touch ~/.local/bin). Does exit 4 fire on CHANGED? Any false CHANGED from unreadable entries or broken links? Paste runs.",
     "VERDICT: envelope-detects-<k>/4-false-changed-<f>"),
    ("R43RevSiteStable", "reviewer", ["calibration"],
     f"{HOST_RULE}\n\nHypothesis (falsifiable): the round-43 C1 counter's verdict on the freeze direction module is invariant under "
     f"`--jobs 1/8/16`, PYTHONHASHSEED (the counter pins 0 in tool runs; vary the COUNTER's own seed) and two scratch roots. Run "
     f"`python3 {C1} --lane \"$S/lane\" --battery-dir {WIT} --work <root> --jobs <j>` in your clone inside the envelope for each "
     f"combination and diff the MUTANT/summary lines. Report confirmed/falsified with the diffs.",
     "VERDICT: site-stable-<confirmed|falsified>-runs-<n>"),
    # ---- connectors ----
    ("R43ConnSibling", "connector", ["adjacency"],
     f"Sibling-overlap scan for this round's surfaces (cryptanalysis tasks, graders that import agent Python modules, pytest exit-status "
     f"rewards, mutation testing of a lane's own gate tools with traced value attribution, bwrap sandboxes) across "
     f"/home/vgpnk/Projects/shokunin/*-shokunin (read-only: PROVINCE.md, SKILL.md, corpus/README.md). Name each overlap with file:line and "
     f"whether kengaku should cite, defer or report it out; who owns cryptanalysis technique and Python import-system semantics?",
     "VERDICT: sibling-overlap-<n>"),
    ("R43ConnPattern", "connector", ["calibration", "quality"],
     f"Cross-claim pattern finding: the feal grader imports the graded module INTO its own interpreter beside the answer; the C1 counter "
     f"imports battery modules (sandboxed child) and traces tools; {L}/plans/pkg_gate.py re-runs probes; the C2 counter imports its "
     f"probe's dry output; {W}/claims/c2_filler_control.py imports the counter. Where do the lane's OWN instruments (plans/round43_*.py, "
     f"plans/feal_probe.py, plans/pkg_gate.py, plans/order_check.py, plans/anchor_digest_check.py, plans/routed_open.py) execute "
     f"untrusted or graded content in the same process as their verdict, compare with `==` against an object they did not construct, "
     f"or reward an exit status? List with file:line and a one-line fixture that would expose each.",
     "VERDICT: pattern-<n>-sites"),
    ("R43ConnFrontier", "connector", ["coverage", "calibration"],
     f"Frontier/coverage check: read {L}/corpus/README.md (coverage map + §Frontier) and {L}/PROVINCE.md; is 'an agent-authored Python "
     f"module imported and called inside the grader's interpreter beside the reference module' ground the lane did not hold (vs the "
     f"eight TB2 graders admitted)? Which frontier clause narrows and how should it read; does any self-assessment line in "
     f"SCORECARD/SHONEN/README now mismatch the repo state (count them, file:line)? End with exactly one VERDICT line.",
     "VERDICT: frontier-<new|not-new>-mismatches-<n>"),
    ("R43ConnClaims", "connector", ["calibration"],
     f"Cross-document consistency: every number and hash in {CLAIMS}, the C1/C2 counter docstrings, {W}/claims/*.txt and "
     f"{W}/first-run/ — do they agree with each other and with `git -C {L} log` (freeze/receipt hashes {FREEZE} / {FIRST}, 9 mutants "
     f"6+3, 8 direct + 1 indirect, 12 cases, 8/4 split, 0 mismatches, 6 freeze fixtures, 12 captures, S129-S134)? List every drift with "
     f"both locations.",
     "VERDICT: drift-<n>"),
]

FLASH = {"executor", "labrat", "scribe", "sonic", "simplifier", "critic", "revenger", "sentinel"}
ATTACK = {"reviewer", "critic", "mutation-tester", "labrat"}


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 43 wave 1 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r43 wave 1 (build + first falsifiers)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    c = Counter(i["role"] for i in items)
    flash = sum(n for r, n in c.items() if r in FLASH)
    attack = sum(n for r, n in c.items() if r in ATTACK)
    assert 32 <= len(items) <= 64, len(items)
    assert flash * 2 >= len(items), f"m_flash share {flash}/{len(items)} below half (closure R6)"
    assert attack * 4 >= len(items), f"attack share {attack}/{len(items)} below a quarter"
    spec = {"wave": "kengaku-r43-build",
            "milestone": "kengaku round 43 wave 1: C1 battery43 for 9 near-variant mutants, C2 TB2 feal admission, routed R1-R6",
            "reportDir": ".ufo/waves/round-43/build", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/build-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    print(len(items), dict(c))
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
