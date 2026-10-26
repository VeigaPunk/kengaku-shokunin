#!/usr/bin/env python3
"""Renders .ufo/waves/round-40/build-spec.json (wave 1 of 2, policy v1)."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-40"
B = f"{W}/build"
SCR = "/fast/scratch/hyaku/kengaku-r40"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/db-wal-recovery"
CAP = f"{L}/corpus/evidence/round40/tb2-db-wal-recovery"
RCPT = f"{L}/corpus/evidence/round40/db-wal-probe.txt"
DRY = f"{L}/corpus/evidence/round40/db-wal-dry-cases-freeze.txt"
C1 = f"{L}/plans/round40_c1_verify.py"
C2 = f"{L}/plans/round40_c2_verify.py"
PROBE = f"{L}/plans/db_wal_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
SPEC = f"{L}/plans/pkg-spec-r40.json"
CLAIMS = f"{L}/plans/round-40-claims.md"
ANCH = f"{L}/plans/anchor_digest_check.py"
LEDG = f"{L}/plans/ledger_tip.py"
ORD = f"{L}/plans/order_check.py"
P39 = f"{L}/.ufo/waves/round-39/build/R39PlanNext"
B39 = f"{L}/.ufo/waves/round-39/build"
F39 = f"{L}/.ufo/waves/round-39/falsify"
SPOT = f"{L}/corpus/lessons/round-39-verifier-spotcheck.md"
WIT = f"{W}/claims/witness"
FREEZE = "bbb109505670192035ef63d7c8b37733e99fa1a3"
FIRST = "055748f78a3335434f2a4070bb3fb1cf8d0eba1f"
CLONE = (f'Fixture rule: S={SCR}/<YourSeatName>; mkdir -p "$S"; trap \'rm -rf -- "$S"\' EXIT; export TMPDIR="$S"; '
         f'git clone -q --shared {L} "$S/lane"; verify `git -C "$S/lane" rev-parse --show-toplevel` equals "$S/lane" before any '
         f'write; every git call names -C "$S/lane"; never commit there (index-only `git add` inside YOUR clone is fine — the gate\'s '
         f'P9 needs drafts staged). Any other fixture repo: D=$(mktemp -d -p "$S") && git -C "$D" init -q, and every git call names '
         f'-C "$D". Remove "$S" before you finish (copy receipts into your report dir first).')

CONTEXT = f"""# Goal
kengaku round 40 (hyaku run 9, 2026-10-26), WAVE 1 of 2 (build + first falsifiers). Lane repo: {L}.
Two claims are FROZEN at {CLAIMS} (freeze commit {FREEZE}; first recorded probe run {FIRST}) — read it first, in full.
Nothing frozen may change: not the three tripwire tools {ANCH} / {LEDG} / {ORD}, not the counters {C1} / {C2}, not the
probe {PROBE}, not the spec {SPEC}, not the gate {GATE}, not the dry table {DRY}, not the captures {CAP}/, not the receipt
{RCPT}, not {W}/claims/.
- C1 calibration: 21 frozen mutants of the three tripwire tools (MUTANTS table in {C1}: id, tool, class, direction, advertised
  sentence with file:line, pre-freeze witness, `old -> new`). At freeze no committed fixture kills any of them ({W}/claims/
  control-c1-nothing.txt: `killed=0 survived=21`). The work: plans/battery40 modules until `python3 plans/round40_c1_verify.py
  --lane .` prints `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`. Module contract (counter docstring):
  module-level FIXTURES = [{{"fid", "tool": "anchor"|"ledger"|"order", "expect": "accept"|"reject"|"error", "defects": [exact
  class set the UNMODIFIED tool prints: anchor `class=` tokens; ledger `NO:<row id>` per `agree=NO` row; order `hit:<kind>` per
  `ORDER HIT` and `fail:<name>` per named `ORDER FAIL` line], "build": build}}]; build(ctx, d) fills the EMPTY directory d and
  returns the tool argv tail. ctx (counter class Ctx): ctx.lane (read-only shared clone of the lane HEAD), ctx.clone(dest) (`git
  clone --shared` of it, dest inside d), ctx.init(dest), ctx.git(repo, *args) (commits as `fixture`), ctx.sh(*argv, cwd=). Every
  absolute path in the argv must lie inside d; `{{WORK}}` is replaced per run by a fresh absent scratch path, `{{WORK:lane}}` by a
  fresh path already holding an empty `lane/` dir. Modules are built in a child inside `bwrap --unshare-pid`; module source must
  not contain any SIDECHANNEL token of the counter (`/proc`, `ppid`, `cmdline`, `psutil`, `environ`, `fsmonitor`, `hookspath`,
  `filter.`, `gitattributes`, `core.`, `alias.`, `setsid`, `daemon`, `fork`, `nohup`, `socket`; case-insensitive, also inside
  comments and strings). Kill rule: the mutant's result on a fixture of the same tool must match its declared direction
  (silence / rc-silence / rc-mirror / error / rc-error — docstring). Pre-freeze witnesses: {P39}/h_anchor.py + out_anchor_r5.txt
  (fixture builders X01..X22 for the anchor mutants), {P39}/h_ledger.py + out_ledger_r5.txt (T00..T12), {WIT}/*.py (A27, L01,
  L11, L21, O04, O12, O14) and {W}/claims/witness-run.txt. Develop with `python3 {C1} --lane "$S/lane" --battery-dir <your
  battery dir> --only <ids> --work "$S/w"` (prints `PREDICATE C1 n/a`). A full run takes ~1 min.
- C2 coverage: pinned Terminal-Bench 2.0 `db-wal-recovery` grader (terminal-bench-2 @ {PIN}) to be admitted as
  corpus/knowledge/tb2-db-wal-recovery-grader.md with rows S119 (tests/test_outputs.py) and S120 (instruction.md). Captures
  {CAP}/ (test_outputs.py, instruction.md, solve.sh = oracle, test.sh, task.toml, Dockerfile, main.db, main.db-wal.encrypted) +
  SHA256SUMS. Receipt {RCPT}: 28 cases, `cases=28 observed_pass=8 observed_fail=20 mismatches=0`, `regrade cases=28 differ=0`,
  second run byte-equal. Counter {C2} = round-39's V1-V7 re-pointed (docstring): V2 runs the gate with --rerun
  --require-clean-tree over {SPEC}; V7 derives each requirement-map label from ALL receipt cases whose `violates=` carries the
  tag (all fail → enforced, all pass → unenforced, mixed → partly); map row | `instruction.md:<L>` | `<tag>` | <label> |
  `case-id`, ... | with the tag's frozen line from the dry table's TAG lines. Headline observations: the grader pins only 22 of 33
  id/name/value cells (values of ids 1-2, names of ids 3-11), so hand-typed JSON that never opens the database passes 7/7;
  "Fix the WAL file" is never checked; a plain read-write sqlite3 open first destroys the undecryptable WAL, after which even the
  task's own solve.sh fails 2 tests; wrong-key XOR leaves 5 base rows; `True` passes as an int value; float ids 1.0..11.0 fail
  only the structure test; an extra field passes.
- Round-39 closure routed items: {SPOT} §5 (R1-R5).

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


def bat(name, module, mids, hints):
    ids = ",".join(mids)
    return (name, "executor", ["calibration", "operability"],
            f"Write the C1 battery40 module {B}/{name}/battery/{module}.py (stdlib only; every fid starts `{module}-`) whose "
            f"fixtures ATTRIBUTABLY kill frozen mutants {ids} of {C1} in their declared directions (read each mutant's tool, class, "
            f"direction, `old -> new` and witness there, and the tool branch it changes). Each fixture's `defects` must equal the "
            f"exact class set the UNMODIFIED tool prints on it, and its `expect` must match the reference exit code (0 accept, "
            f"1 reject, 2 error). One fixture per behaviour; name what each fixture demonstrates in a one-line comment. Hints: "
            f"{hints} Prove it in your clone: `python3 {C1} --lane \"$S/lane\" --battery-dir {B}/{name}/battery --only {ids} "
            f"--work \"$S/w\"` must print every FIXTURE line of your module `ok`, `wrong=0 tampered=0 sidechannel=0`, "
            f"`null_detected=0`, and each of {ids} `killed by=<your fid>`. Paste that output. Then remove each fixture in turn and "
            f"record which mutant flips to SURVIVED (load-bearing table). Finally copy your module into \"$S/lane/plans/battery40/\" "
            f"and run the FULL default counter (`python3 {C1} --lane \"$S/lane\" --work \"$S/w2\"`); paste its MUTANT and summary "
            f"lines. Report the module's sha256.",
            f"VERDICT: battery40-{module}-killed-<k>/{len(mids)}-wrong-<w>")


ITEMS = [
    # ---- C1 battery40 executors (7) ----
    bat("R40BatAnchorTok", "a_tok", ["A01", "A02", "A03"],
        f"anchor tool, token shape: an uppercase 64-hex anchor token (A01 silence on class digest-uppercase: R39PlanNext X01), a "
        f"7-hex abbreviation `sha256 afaae9d…` (A02: X03), a 64-hex token followed by `…` (A03: X05). Edit the SOURCES.md of "
        f"ctx.clone(d / 'lane') in its working tree (no commit needed; the tool reads SOURCES.md from the work tree and evidence "
        f"from HEAD); argv [\"--lane\", str(lane)]. Builders: {P39}/h_anchor.py lines 103-117."),
    bat("R40BatAnchorRow", "a_row", ["A06", "A08", "A09"],
        f"anchor tool, row shape: a 4-space-indented copy of row S111 carrying a wrong digest (A06 rc-mirror: the reference does "
        f"not parse it as a row, exit 0; X09), a digest token placed in the teaches cell (A08 rc-silence: X06), a 12-cell row (A09 "
        f"rc-silence: X07). Builders: {P39}/h_anchor.py lines 118-137."),
    bat("R40BatAnchorBind", "a_bind", ["A15", "A17", "A27"],
        f"anchor tool, binding: two committed/staged task.toml files naming the same task slug so a row's URL binds ambiguously "
        f"(A15 rc-silence, index mode `--evidence-ref index`: X17), a staged-but-uncommitted capture plus a row anchored to it read "
        f"in index mode (A17 rc-mirror: X15), a second pinned URL in S111's source cell with S108's digest (A27 silence on "
        f"capture-unanchored: {WIT}/w_anchor.py). Builders: {P39}/h_anchor.py lines 138-211 (stage_capture/add_row)."),
    bat("R40BatAnchorManifest", "a_man", ["A21", "A22"],
        f"anchor tool, manifest views (index mode): a capture whose SHA256SUMS entry is written in UPPERCASE hex and whose row "
        f"anchors the lowercase digest (A21 rc-mirror: X21), and a capture whose committed bytes changed while the manifest entry "
        f"still lists the digest the row anchors (A22 rc-mirror: X20). Builders: {P39}/h_anchor.py lines 220-239."),
    bat("R40BatLedgerRows", "l_rows", ["L05", "L06", "L14", "L15"],
        f"ledger_tip control mode (`--lane <clone>`): a closed corpus/defects.jsonl row flipped to `open` whose check still passes "
        f"(L05 rc-silence: T05), both ledgers emptied (L06: T06), a check that crashes (L14: T10 deletes a file a r34 check reads), "
        f"a row whose `check` names no CHECKS entry (L15: T07). Builders: {P39}/h_ledger.py lines 55-95. Note the reference must "
        f"exit 1 on each and `defects` lists every `NO:<id>` row the reference prints — read the FIXTURE line from your dev run. "
        f"Tool runs inherit your PATH/HOME (R35-D1 needs `uv` from ~/.local/bin)."),
    bat("R40BatLedgerRefuse", "l_refuse", ["L01", "L11", "L21"],
        f"ledger_tip refusals (exit 2): `--source <dir in d that is not a repo> --work {{WORK}}` (L01 error: T08), `--source "
        f"<clone> --work {{WORK:lane}}` (L11 error: work/lane exists), control mode on a clone whose master was moved to HEAD~6 "
        f"with HEAD detached (L21 error: stale pin ref). Witnesses {WIT}/w_ledger.py."),
    bat("R40BatOrder", "o_gate", ["O04", "O12", "O14"],
        f"order_check on small fixture repos built with ctx.init/ctx.git (claims file plans/round-NN-claims.md, one file under "
        f".ufo/waves/round-NN/claims/, receipt committed after): a claims/ file carrying `P10 ok receipt unreadable` (O04 "
        f"rc-silence), a gitlink (mode 160000) entry under claims/ (O12 rc-error), a claims file named `round-NN-claims.md.bak` "
        f"(O14 error). Witnesses {WIT}/w_order.py. Use a round number other than 50 and your own file texts."),
    # ---- C1 attacks ----
    ("R40CritC1Counter", "critic", ["calibration"],
     f"Attack {C1} (round-39 R39CritC1Counter A1-A5 were the routed repairs): can a battery40 module reach `killed=21` (or kill one "
     f"mutant) without a fixture that honestly exhibits the behaviour? Try: a process that escapes the build child's pid namespace "
     f"(double fork, `systemd-run --user`, a cron/at job, a file watcher started via another service); a fixture whose git "
     f"config/attributes make the TOOL's git calls execute fixture code (filters, textconv, diff drivers, `include.path`) and tell "
     f"reference from mutant (e.g. by reading the bound tool file); writes outside d during build; argv paths smuggled past "
     f"`path_ok` (relative paths, `--x=` forms, symlinks inside d pointing out); `{{WORK}}` abuse; fingerprint holes (files under "
     f".git excluded? mtime-preserving rewrites). Build each attack as a module in YOUR clone's plans/battery40/ and run the full "
     f"counter; report each attack's BATTERY/MUTANTS lines and whether the token scan flags it.",
     "VERDICT: c1-counter-attacks-<reached>/<tried>"),
    ("R40CritC1Equiv", "critic", ["calibration"],
     f"Q29 audit: for each of the 21 mutants in {C1}, re-derive from the tool source whether its declared direction is reachable "
     f"and try to prove it observationally equivalent at (exit code, class set) granularity. Re-run the round-39 witness harness "
     f"evidence where cheap ({P39}/h_anchor.py, h_ledger.py — copy to your scratch, repoint S/BASE) and the round-40 witnesses "
     f"({WIT}, {W}/claims/witness-run.txt). Check the withdrawn O13 equivalence argument in the counter docstring. Report per "
     f"mutant: reachable / equivalent / unclear with the evidence.",
     "VERDICT: c1-directions-reachable-<k>/21-equivalent-<e>"),
    ("R40CritClaims", "critic", ["calibration"],
     f"Attack the claims' framing in {CLAIMS}: is C1 a calibration move (self-assessment vs observed state) — check each of the 21 "
     f"`adv` cells quotes a sentence that exists at the cited file:line and actually advertises the mutated behaviour (count "
     f"direct / indirect / not-advertised); is the do-nothing control meaningful; is C2's class (binary database file pair + "
     f"JSON export) new against {L}/corpus/README.md's coverage map; separability; universal clauses; any number in the claims "
     f"that does not reproduce from the committed controls.",
     "VERDICT: claims-attack-<n>-defects-adv-direct-<k>/21"),
    ("R40RevCounters", "reviewer", ["calibration", "operability"],
     f"Code review of {C1}, {C2} and {PROBE}: correctness bugs, false-green/false-red paths, determinism, TMPDIR/--work honoured "
     f"(no /tmp), pins complete (C1 pins only the three tools — what else does it read?), the child/sandbox contract (what a module "
     f"still controls), thread-safety of the parallel runner, the fingerprint exclusions, `classes()` parsing per tool, the probe "
     f"sandbox (writable /app bind, recipe failure → exit 2, nothing host-specific printed, regrade logic). Cite file:line.",
     "VERDICT: review-<n>-defects"),
    ("R40RevFreeze", "reviewer", ["calibration"],
     f"Freeze-order audit: `git -C {L} log --format='%H %cI %s' d3a6277f..master`; confirm {FREEZE} carries claims, counters, probe, "
     f"spec, dry table, captures and controls and NO receipt (`git cat-file -e {FREEZE}:corpus/evidence/round40/db-wal-probe.txt` "
     f"must fail); the receipt landed in {FIRST}; `sha256sum -c` of {W}/claims/frozen-digests.txt at the freeze; re-run "
     f"control-c1-nothing and control-c2-nothing on a clean clone of {FREEZE} and diff with the committed files; run "
     f"`python3 {ORD} --lane <clone> --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt`.",
     "VERDICT: freeze-audit-<ok|n-defects>"),
    ("R40SentinelCounter", "sentinel", ["operability"],
     f"Security review of the round-40 instruments: {C1} builds battery modules with `bwrap --dev-bind / /` (the whole host fs "
     f"writable) and runs tool variants the same way; {PROBE} runs captured solve.sh and per-case bash recipes inside bwrap with a "
     f"writable /app. Can a module/case write outside its scratch, reach the network, read ~/.ssh or the lane's .git, or leave "
     f"processes behind (test `systemd-run --user`, double fork + setsid inside the pid namespace)? Test cheaply in your scratch; "
     f"cite file:line; say which finding needs a counter change (frozen: route it) vs a review rule.",
     "VERDICT: sentinel-<n>-findings"),
    ("R40MutC1Counter", "mutation-tester", ["calibration"],
     f"Mutation-test {C1} itself in a copy (never the lane file): exhibits() direction legs swapped/loosened, `wrong` check "
     f"dropped, fingerprint skipped, path_ok always True, sandbox() without --unshare-pid, PINS-AFTER skipped, null run skipped, "
     f"invalid-needle check dropped, TOTAL changed. For each, do the committed controls ({W}/claims/*.txt re-run with the mutated "
     f"copy) or the witness battery ({WIT}) expose it? Report caught/survived per mutant with the line that changed.",
     "VERDICT: c1-counter-mutants-<caught>/<total>"),
    # ---- C2 package ----
    ("R40PkgEntry", "scribe", ["coverage", "depth"],
     f"Draft the C2 package for the L1 under {B}/R40PkgEntry/: (1) entry.md = corpus/knowledge/tb2-db-wal-recovery-grader.md "
     f"(follow the shape of {L}/corpus/knowledge/tb2-git-leak-recovery-grader.md: `source: S119 <raw url>` / `source: S120 <raw url>` "
     f"lines with the EXACT pinned raw URLs {RAW}/tests/test_outputs.py and {RAW}/instruction.md, `verified-at: 2026-10-26`, ONE "
     f"`recheck:` line whose command runs green AS WRITTEN from the lane root (`(cd corpus/evidence/round40/tb2-db-wal-recovery && "
     f"sha256sum -c SHA256SUMS)`); sections: Summary, What is graded (static reading), `## Located quotes` table rows | claim | "
     f"“quote” | `capture:line` | with >=8 distinct verbatim 3-25-word quotes at >=8 distinct lines of {CAP}/test_outputs.py and "
     f"instruction.md (check each with sed -n); `## Requirement map` with exactly one row per TAG in {DRY} in the frozen format, "
     f"label DERIVED from {RCPT} as V7 does, citing violating case ids; findings each tied to receipt case ids; the regrade column "
     f"(28/28 same; why: the grader only reads /app/recovered.json); limits (host sqlite3 3.54.0 vs the image's Ubuntu 24.04 "
     f"packages, recipes unprivileged, image never pulled, seven pilot-copied predictions); prior art from {B}/R40ScoutPriorArt.md "
     f"if present when you write (else a marked placeholder line for the L1) — claim a probed instance only; `## Negative space` "
     f"with an explicit falsifier. (2) rows.md = two 11-cell SOURCES rows S119/S120 in {L}/corpus/SOURCES.md's exact column order "
     f"(read its header and S117/S118), tier A, status mined, opened 2026-10-26, anchor cell `sha256 <pin>` + a <=25-word located "
     f"quote, teaches >= 8 distinct words, used-by = corpus/knowledge/tb2-db-wal-recovery-grader.md. (3) readme.md = the index row + "
     f"one coverage bullet naming the entry and `round40/db-wal-probe.txt`. PROVE it: in your clone place the drafts, `git -C "
     f"\"$S/lane\" add -A`, run `python3 {C2} --lane \"$S/lane\" --work \"$S/w\"` (create $S/w first) → paste output; iterate "
     f"until `checks=7 defects=0`.",
     "VERDICT: c2-package-draft-checks-7-defects-<n>"),
    ("R40PkgProse", "scribe", ["coverage", "depth", "adjacency"],
     f"Draft paste-ready lane prose for C2 under {B}/R40PkgProse/: (a) a PROVINCE.md round-40 paragraph (read {L}/PROVINCE.md "
     f"round-35..39 paragraphs; same admission limits: grader probe only, image not pulled; binary database file pair → JSON export "
     f"as the new graded-state class); (b) the corpus/README.md §Frontier TB2 sub-bullet narrowed by one task (read the current "
     f"clause; 6 of 89 read); (c) a SKILL.md section 'Database-recovery TB2 grader — round 40' as a decision table (what the grader "
     f"reads → what passes → what a reviewer should check instead), every row citing a receipt case id in {RCPT}. Observations "
     f"only; no class claims beyond the receipt.",
     "VERDICT: c2-prose-drafted-<n>-rows"),
    ("R40RegistryRows", "scribe", ["operability", "calibration"],
     f"Round-39 closure R1/R2 + this round's tools: draft SKILL.md gate/probe registry rows (read the registry table in {L}/SKILL.md "
     f"— grep -n 'registry' — and copy its exact column shape) for: `plans/order_check.py` (gate, exit 0 PASS / 1 FAIL / 2 setup, "
     f"Q30), `plans/round39_c1_audit.py` (post-hoc audit; its verdict lines and exit codes from its source), `plans/round40_c1_verify.py`, "
     f"`plans/round40_c2_verify.py`, `plans/db_wal_probe.py`. Each row: command as runnable from the lane root, exit-code map read "
     f"from the source (cite file:line), self-test/control spelling if any. R2: `plans/git_leak_probe.py --work <absent dir>` → "
     f"traceback exit 1 (closure D3). That probe is pinned by plans/round39_c2_verify.py PROBE_SHA256 and plans/pkg-spec-r39.json "
     f"frozen_instruments, so it cannot be edited without reding the round-39 counter: verify that claim (run the r39 C2 counter "
     f"in a clone with a one-line edit), and draft the corrected registry text for its row (`--work` must exist) instead. Run each "
     f"command you write once in a clone and paste the exit code.",
     "VERDICT: registry-rows-<n>-r2-<pinned|editable>"),
    ("R40ScoutPriorArt", "scout", ["novelty", "coverage"],
     f"Prior art for the db-wal-recovery grader findings. OPEN (not search snippets): sqlite.org/wal.html (what happens to the WAL "
     f"when the last connection closes; WAL header magic/checksum and invalid-WAL handling), sqlite.org/fileformat2.html WAL "
     f"section; terminal-bench-2 / terminal-bench-2-1 / harbor issues+PRs (gh api / gh search) for db-wal-recovery, 'WAL', "
     f"'recovered.json'; the JonathanGabor/terminal-bench-2-audit repo's entry for db-wal-recovery if any; any third-party write-up "
     f"of this task (the round-39 planner saw an unopened snippet about the destructive read). For each hit: URL, date, state, "
     f"<=25-word quote with location, and whether it reports this grader's permissiveness (22/33 cells pinned, hand-typed JSON "
     f"passes, fix-wal unchecked) or the destructive-read trap. Propose at most one SOURCES row for the strongest primary source "
     f"(the sqlite.org WAL doc is a candidate for the trap's mechanism), or say none qualifies.",
     "VERDICT: prior-art-<n>-hits-row-<yes|no>"),
    ("R40ScoutUpstream", "scout", ["freshness", "coverage"],
     f"Upstream state of db-wal-recovery: compare all eight captures in {CAP}/ with terminal-bench-2 main (curl raw + sha256sum, "
     f"gh api commits?path=db-wal-recovery), check terminal-bench-2-1 for the same task, the docker image tag in task.toml, and "
     f"whether Ubuntu 24.04's sqlite3 version (packages.ubuntu.com noble sqlite3) differs materially from host 3.54.0 for WAL "
     f"handling (release notes). Report drift (none/where) with commands and outputs.",
     "VERDICT: upstream-drift-<none|n>"),
    ("R40CritPytest", "critic", ["coverage"],
     f"Parity: run the REAL pytest 8.4.1 (uv venv -p 3.13 in your scratch, PyPI via uv) over {CAP}/test_outputs.py for each of the "
     f"28 case states of {PROBE} (reuse its sandbox: copy the probe into your scratch and replace the harness's grader call with "
     f"`python -m pytest /cap/test_outputs.py -rA` inside the same bwrap, the venv bound read-only), and compare per-test letters "
     f"with {RCPT}. Report agree/disagree per case.",
     "VERDICT: pytest-parity-<agree>/28"),
    ("R40CritIndep", "critic", ["coverage", "calibration"],
     f"Independent recompute: WITHOUT reading the probe's predicted letters, derive from {CAP}/test_outputs.py and SQLite "
     f"documentation alone the expected seven test outcomes for each of the 28 case descriptions (the `-- requirement` text + "
     f"recipe/mk.py variant in {PROBE}) and compare with {RCPT}. Then build 3 EXTRA cases of your own (e.g. NaN/negative values, "
     f"ids as booleans, a symlinked recovered.json, a UTF-8 BOM) in a copy of the probe in your scratch, predict first, run, report.",
     "VERDICT: indep-agree-<k>/28-extra-<j>/3"),
    ("R40CritProbe", "critic", ["coverage", "calibration"],
     f"Attack {PROBE} and {RCPT}: is each case's `violates=` tag set right (contestable tags: does a hand-typed but correct export "
     f"violate fix-wal/extract-all? does `truth-extra-field` violate record-format?); does each case text describe what its recipe "
     f"actually builds (run setup + recipe yourself and inspect /app: is main.db-wal really gone after `plain-read-then-solve`? "
     f"what does the wrong-key WAL look like to sqlite?); is the docstring's ground truth right (re-derive from the captures); "
     f"which requirement-map labels would change under a contestable tag. List label changes and wording defects.",
     "VERDICT: probe-attack-<n>-defects-labels-change-<k>"),
    ("R40CritSkipC2", "critic", ["calibration"],
     f"Post-first-run skip-controls for C2 (the first recorded run {FIRST} landed, so running the gate with --rerun is now allowed): "
     f"in your clone build (a) a junk entry/rows/README with correct anchors and a hand-typed receipt copied from `--dry` with "
     f"observed=predicted → `python3 {C2} --lane \"$S/lane\"` must stay red (which V?); (b) a probe copy whose CASES all predict "
     f"PPPPPPP must print mismatches>0 against the grader; (c) the informed-filler shape ({B39}/R39CritSkipC2.md) — does it reach "
     f"checks=7 defects=0 here too? Keep every receipt.",
     "VERDICT: c2-skip-controls-red-<k>/<n>"),
    ("R40CritSqlite", "critic", ["coverage", "freshness"],
     f"Host-vs-image limit: the receipt was produced with host sqlite3 3.54.0 / python 3.14.8; the task image is Ubuntu 24.04 "
     f"(sqlite3 3.45.x). For the cases whose verdict depends on SQLite behaviour (plain-read-then-solve, xor-wrong-key, "
     f"decrypt-checkpoint-truncate, decrypt-then-extract, oracle-solve-sh), test with an older SQLite you can get without pacman "
     f"(e.g. `uv run --python 3.12` interpreters bundle their own sqlite3 — report sqlite3.sqlite_version; or docker ubuntu:24.04 "
     f"if docker runs rootless here). Report whether any verdict would differ.",
     "VERDICT: sqlite-version-<same|n-differ>"),
    ("R40MutProbe", "mutation-tester", ["coverage"],
     f"Mutation-test the probe's sensitivity in a copy (never the lane file): harness maps every exception to P; seeding skipped "
     f"for every case; wrong WAL file name in seeding; recipe failures ignored; /app bound read-only; regrade compares the first "
     f"grading with itself; one case's recipe swapped with another's; TRUTH value of id 1 changed. For each, does the receipt "
     f"change and would C2 V4/V5/V2-P10 catch it? Report.",
     "VERDICT: probe-mutants-<caught>/<total>"),
    ("R40MutC2Counter", "mutation-tester", ["calibration"],
     f"Mutation-test {C2}'s checks in a clone where a passing package exists (use {B}/R40PkgEntry/ drafts if present when you "
     f"start; else build a minimal genuine package yourself from {CAP} and {RCPT}). One mutant at a time: map label flipped; map "
     f"row citing a non-violating case; tag duplicated; tag missing; map line number wrong; S119 anchor token replaced by S120's "
     f"digest; one CASE line deleted from the receipt; spec one byte; dry table one byte; probe one byte; a capture one byte. "
     f"Report caught/survived per mutant with the DEFECT line.",
     "VERDICT: c2-mutants-<caught>/<total>"),
    ("R40RegradeSweep", "executor", ["novelty", "coverage"],
     f"Re-run stability across the lane's admitted TB2 graders (considerthese/2026-10-26.md proposal 3 rider): for each of the "
     f"five earlier probes (plans/tb2_grader_probe.py or the per-task probes: grep -l 'terminal-bench-2' {L}/plans/*probe*.py) take "
     f"the oracle case and two failing cases, build the end state once in that probe's sandbox (copy the probe to your scratch, "
     f"never edit the lane), grade it twice without rebuilding, and record same/DIFF per case. Report a per-task table with the "
     f"commands; say which graders mutate the graded state (polyglot-c-py's compile-into-cwd shape, {P39}/../R39PlanNext.md §4).",
     "VERDICT: regrade-sweep-<tasks>-diff-<n>"),
    # ---- frontier / routed ----
    ("R40TipReceipts", "executor", ["operability", "freshness"],
     f"Round-39 routed residual (F39TipReceipts): `plans/tip_receipts.py` skips the round-39 receipt (no committed re-run command "
     f"it recognises) and would skip round 40's. Write a fixed copy {B}/R40TipReceipts/tip_receipts.py that maps "
     f"corpus/evidence/round39/git-leak-probe.txt and corpus/evidence/round40/db-wal-probe.txt to their committed probes (read how "
     f"RECEIPTS and `Run as:` resolution work), show red-before (`--only round39` skip/boundary) and green-after (equal) on a clean "
     f"clone, keep the tamper control `differ`, and confirm no previously-equal receipt changes status. Paste receipts.",
     "VERDICT: tip-receipts-r39-<equal|skip>-r40-<equal|skip>"),
    ("R40CloseCheck", "executor", ["operability", "calibration"],
     f"Round-39 routed residual (F39CritQ30): QUALITY Q30 says the order class is 'closed by a gate' while nothing invokes "
     f"`plans/order_check.py`. Draft {B}/R40CloseCheck/round_close.py (stdlib; proposed lane path plans/round_close.py): given "
     f"`--lane . --round N`, it finds plans/round-N-claims.md and the receipt(s) the claims name, runs order_check.py for each, "
     f"runs the sources census validate command for the lane, and exits 0 only when all pass (1 on a FAIL, 2 on setup). Show it "
     f"RED on round 38 and GREEN on rounds 39 and 40 in a clean clone; paste receipts. Do not edit order_check.py (pinned by C1).",
     "VERDICT: round-close-r38-<red|green>-r40-<red|green>"),
    ("R40LessonDraft", "scribe", ["calibration", "quality"],
     f"Mistake mining for corpus/lessons/round-40.md `## Mistakes` (class · evidence pointer · captured-by · fix, a fix counts "
     f"only once shown able to fail). Candidates to verify against files: (1) {P39}/../R39PlanNext.md:126 asserted O13 'reachable "
     f"with one new fixture'; the round-40 pre-freeze witness ({W}/claims/witness-run.txt, w-o13-quoted-case) shows it equivalent "
     f"— reachability asserted, not witnessed; (2) the round-39 closure D3 (`--work` absent → traceback) recurs in "
     f"{C2} (TemporaryDirectory under an absent --work: see {W}/claims/control-c2-nothing.txt history) — check whether the "
     f"committed control shows it; (3) any other from {SPOT} §1/§5 or {F39}/*.md. Sweep: list the commands you ran. Draft rows; "
     f"the L1 decides.",
     "VERDICT: mistakes-drafted-<n>"),
    ("R40SourcesRecheck", "scout", ["freshness"],
     f"SOURCES curation: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin "
     f"kengaku` (or read {L}/corpus/SOURCES.md recheck cells) — rows due on or before 2026-10-26; open up to 4 due rows (else the 4 "
     f"highest drift-risk rows) live this round (URL, access date, <=25-word located quote, sha256 where the row pins one) and "
     f"draft each row's status/recheck change old→new with the evidence.",
     "VERDICT: sources-rechecked-<n>-changes-<k>"),
    ("R40MergeRescreen", "scout", ["coverage", "adjacency"],
     f"Assimilation re-screen of /home/vgpnk/Projects/shokuknow/merge/kengaku/ (READ-ONLY): changed since round 39's screen "
     f"({B39}/R39MergeRescreen.md)? `git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %cI' -- merge/kengaku`. Run the id "
     f"collision check exactly as the round prompt gives it (0-3-space pattern) with outputs under {B}/R40MergeRescreen/ (reg-ids, "
     f"staged-ids, collisions) and prove the guard on a scratch registry with an indented `  | S002 |` row; derive the quarantine "
     f"slice from /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (data rows only). Is any "
     f"staged entry about SQLite/WAL, database recovery or mutation testing (fits this round)? Verdict per entry admit/hold/refuse.",
     "VERDICT: merge-rescreen-admit-<a>-hold-<h>-refuse-<r>"),
    ("R40PlanNext", "scout", ["calibration", "coverage", "novelty"],
     f"Round-41 planning data walk (the L1 holds the planner seat; you supply data): price two candidates with a control executed "
     f"now — calibration: the next undemonstrated surface (tip_receipts.py, mutant_direction_check.py, round39_c1_audit.py, "
     f"sources_adopt.py, state_check.py — pick by advertised-vs-demonstrated gap, measured with a cheap mutant harness); "
     f"coverage/novelty: the next TB2 grader class not yet read (openssl-selfsigned-cert fallback, constraints-scheduling's "
     f"embedded solver, others; {P39}/tb2_census.json) with offline executability and quote supply measured; and "
     f"considerthese/2026-10-26.md proposal 1 (routed-findings burn-down) priced. Draft a paste-ready `### Planned (round 41)` block.",
     "VERDICT: plan41-drafted"),
    ("R40ConnSibling", "connector", ["adjacency"],
     f"Sibling-overlap scan for this round's surfaces (SQLite/WAL recovery and forensics graders, JSON export graders, mutation "
     f"testing of a lane's own gates, bwrap sandboxes) across /home/vgpnk/Projects/shokunin/*-shokunin (read-only: PROVINCE.md, "
     f"SKILL.md, corpus/README.md) — data/db lanes, security research, test-tooling lanes. Name each overlap with file:line and "
     f"whether kengaku should cite, defer or report it out.",
     "VERDICT: sibling-overlap-<n>"),
    ("R40ConnPattern", "connector", ["calibration", "quality"],
     f"Cross-claim pattern finding: the db-wal grader pins only a subset of cells (22/33) and never checks the repair step; the "
     f"tripwire survivors are 'bound loosened by one', 'prefix vs exact', 'one mode never exercised', 'refusal folded into a "
     f"verdict'. Do the lane's own instruments (plans/round40_*.py, plans/db_wal_probe.py, plans/round39_*.py, "
     f"plans/tip_receipts.py, plans/sources_adopt.py) carry any of these shapes (check only a subset, skip a mode, fold a setup "
     f"error into a verdict)? List with file:line and a one-line fixture that would expose each.",
     "VERDICT: pattern-<n>-sites"),
    ("R40ConnFrontier", "connector", ["coverage", "calibration"],
     f"Frontier/coverage check: read {L}/corpus/README.md (coverage map + §Frontier) and {L}/PROVINCE.md; is 'binary database "
     f"file pair → JSON export' ground the lane did not hold (vs the five TB2 graders already admitted)? Which frontier clause "
     f"narrows and what should it read after; does any self-assessment line in SCORECARD/SHONEN/README now mismatch the repo "
     f"state (count them, file:line) — the round's calibration denominator outside C1.",
     "VERDICT: frontier-<new|not-new>-mismatches-<n>"),
    ("R40ConnClaims", "connector", ["calibration"],
     f"Cross-document consistency: every number and hash in {CLAIMS}, the C1/C2 counter docstrings, {W}/claims/*.txt and "
     f"{W}/first-run/first-run.txt — do they agree with each other and with `git -C {L} log` (freeze/receipt hashes, 21 vs 22 "
     f"mutants, 28 cases, 8/20 split, witness kills 7)? List every drift with both locations.",
     "VERDICT: drift-<n>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 40 wave 1 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r40 wave 1 (build + first falsifiers)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    spec = {"wave": "kengaku-r40-build",
            "milestone": "kengaku round 40 wave 1: C1 battery40 for 21 tripwire mutants, C2 TB2 db-wal-recovery admission, frontier step",
            "reportDir": ".ufo/waves/round-40/build", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/build-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c))
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"] + c["sentinel"]
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
