#!/usr/bin/env python3
"""Renders .ufo/waves/round-38/build-spec.json (wave 1 of 2, policy v1, 40 seats)."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-38"
B = f"{W}/build"
SCR = "/fast/scratch/hyaku/kengaku-r38"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/build-pmars"
CAP = f"{L}/corpus/evidence/round38/tb2-build-pmars"
RCPT = f"{L}/corpus/evidence/round38/build-pmars-probe.txt"
DRY = f"{L}/corpus/evidence/round38/build-pmars-dry-cases-freeze.txt"
C1 = f"{L}/plans/round38_c1_verify.py"
C2 = f"{L}/plans/round38_c2_verify.py"
PROBE = f"{L}/plans/build_pmars_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
SPEC = f"{L}/plans/pkg-spec-r38.json"
CLAIMS = f"{L}/plans/round-38-claims.md"
F37 = f"{L}/.ufo/waves/round-37/falsify"
CLONE = (f'Fixture rule: S={SCR}/<YourSeatName>; mkdir -p "$S"; trap \'rm -rf -- "$S"\' EXIT; export TMPDIR="$S"; '
         f'git clone -q --shared {L} "$S/lane"; verify `git -C "$S/lane" rev-parse --show-toplevel` equals "$S/lane" before any '
         f'write; every git call names -C "$S/lane"; never commit (index-only `git add` inside YOUR clone is fine — the gate\'s P9 '
         f'needs drafts staged). Copy your drafts into the clone to test them. Remove "$S" before you finish (copy receipts into '
         f'your report dir first).')

CONTEXT = f"""# Goal
kengaku round 38 (hyaku run 8, 2026-10-26), WAVE 1 of 2 (build + first falsifiers). Lane repo: {L}.
Two claims are FROZEN at {CLAIMS} (freeze commit e0a378539a45cc9388c66cfba22f44275131de23; first recorded probe run
e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b) — read it first, in full. Nothing frozen may change: not the gate {GATE}, not the
counters {C1} / {C2}, not the probe {PROBE}, not the spec {SPEC}, not the dry table {DRY}, not the captures {CAP}/, and not
any file the C1 counter pins (its PINS dict: round36/round37 counters, battery37 modules, pkg-spec-r35.json, attribution audit).
- C1 calibration: 22 frozen mutants N01-N22 of the gate (each = one advertised behaviour; MUTANTS table in {C1}, each with
  clause, direction silence|mirror, `old -> new`). At freeze the round-36+37 battery kills 0/22 under the ATTRIBUTED kill rule
  ({W}/claims/control-c1-nothing.txt). The work: battery modules for plans/battery38/ until
  `python3 plans/round38_c1_verify.py --lane .` prints `MUTANTS total=22 killed=22 survived=0 invalid=0 null_detected=0`. Read
  the counter docstring: fixture API = module-level FIXTURES = [{{"fid", "expect": "accept"|"reject"|"error", "defects": [exact
  DEFECT clause ids; [] for accept/error], "build": build}}]; build(ctx, d) fills the EMPTY directory d and returns the gate argv
  tail. ctx is the round-37 counter's Ctx ({L}/plans/round37_c1_verify.py:189-217): ctx.genuine_package(d) git-inits d and
  copies the genuine round-35 package (spec {L}/plans/pkg-spec-r35.json, ctx.spec is that dict), ctx.git_add(d) stages
  index-only, ctx.r36 = {L}/plans/round36_c1_verify.py module (rewrite_quotes, QUOTE_ROW, copy_package, stub_probe, d4_line,
  d5_line, build_line_fixtures), ctx.d4_line(), ctx.d5_line(), ctx.d5_capture_dir(). Package argv: ["package", "--root", str(d),
  "--require-clean-tree"] (+ "--rerun" for P10). A battery38 fixture MAY add "--spec", <a json file it wrote INSIDE d> (derive it
  from dict(ctx.spec)); otherwise the frozen r35 spec is appended. Kill = attributed: silence → reference prints the clause
  DEFECT, the fixture declares it, the mutant does not print it; mirror → reference prints the clause `ok`, mutant prints it
  DEFECT (so a mirror needs an ACCEPT-side fixture where that clause runs and passes); RUN → a declared DEFECT clause stops being
  DEFECT; MAIN → fixture expect=error, reference exit 2, mutant exit 0/1. Module source must not contain the tokens `/proc`,
  `ppid`, `cmdline`, `psutil`, `environ` (counter's sidechannel scan). Develop with
  `python3 {C1} --lane "$S/lane" --battery-dir <your battery dir> --only <your ids> --work "$S/w"` (prints `PREDICATE C1 n/a`).
  Seat battery dirs hold ONE module each; fid prefixes are given per seat and must be unique.
- C2 coverage: pinned Terminal-Bench 2.0 `build-pmars` grader (terminal-bench-2 @ {PIN}) to be admitted as
  corpus/knowledge/tb2-build-pmars-grader.md with rows S115 (tests/test_outputs.py) and S116 (instruction.md). Captures
  {CAP}/ (test_outputs.py, instruction.md, test.sh, task.toml, solve.sh = oracle) + SHA256SUMS. Receipt {RCPT}
  (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`; second run byte-equal). Counter {C2} V1-V7 (docstring): V2 runs the
  gate with --rerun --require-clean-tree over spec {SPEC}; V7 derives each requirement-map label from ALL receipt cases whose
  `violates=` carries the tag (all fail → enforced, all pass → unenforced, mixed → partly); map row format
  | `instruction.md:<L>` | `<tag>` | <label> | `case-id`, ... | with the tag's frozen line from the dry table's TAG lines.
  Headline observations of the receipt: a canned 14-line C program + empty debian/ dir + zero-byte src/dummy.c passes all four
  tests; `ldd` string scan misses a dlopen()ed libX11; `Results:` checked by re.match prefix only; non-zero exit ignored when
  output is non-empty; a canned script earlier on PATH answers the behaviour checks while ldd reads the installed binary;
  debian/ may be a file; a directory named *.c counts as C source.
- Round-37 closure routed items: {L}/corpus/lessons/round-37-verifier-spotcheck.md section 5 (D1-D7). Round-37 wave-2 reports
  (untracked, some seats may still be writing): {F37}/*.md.

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
    return (name, "executor", ["calibration", "operability"],
            f"Write the C1 battery38 module {B}/{name}/battery/{module}.py (stdlib only; every fid starts `{module}-`) whose "
            f"fixtures ATTRIBUTABLY kill the frozen mutants {mids} of {C1} (read each mutant's `old -> new` and direction there and "
            f"the gate branch in {GATE}). One fixture per mutant unless one fixture provably kills several; each fixture's `defects` "
            f"must equal the exact DEFECT clause set the UNMODIFIED gate prints on it. Hints: {hints} Prove it in your clone: "
            f"`python3 {C1} --lane \"$S/lane\" --battery-dir {B}/{name}/battery --only {mids} --work \"$S/w\"` must print every FIXTURE "
            f"line of your module `ok`, `renamed_disagree=0 sidechannel=0`, `null_detected=0`, and each of your mutants "
            f"`killed by=<your fid>`. Paste that output. Then delete each fixture in turn and confirm its mutant flips to SURVIVED "
            f"(load-bearing table). Report the module's sha256.",
            f"VERDICT: battery38-{module}-killed-<k>/<n>-wrong-<w>")


ITEMS = [
    # ---- C1 battery38 executors (12) ----
    bat("R38BatP1Run", "b1run", "N01,N16",
        "N01: a fixture-owned spec (copy ctx.spec, set frozen_instruments to {}) over the genuine package — reference P1 DEFECT "
        "pinned=0 (declare exactly what else fires; ideally nothing). N16: a fixture-owned spec whose entry_rules.quote_words is [3] "
        "(one value) makes P3 crash inside run_checks → reference `P3 DEFECT clause error ValueError` (R37PlanNext B6, "
        f"{L}/.ufo/waves/round-37/build/R37PlanNext.md:260-261); the mutant turns the crash into ok."),
    bat("R38BatP3", "p3m", "N02",
        "mirror: an ACCEPT fixture whose Located-quotes table has exactly min_distinct_locations (8) distinct (capture,line) "
        "locations and >= min_quotes distinct texts, all verbatim and 3-25 words — reference P3 ok and exit 0; the mutant (`>`) "
        "prints P3 DEFECT. Start from the genuine package and drop/merge quote rows."),
    bat("R38BatP4a", "p4a", "N03,N04",
        "N03: a P4 defect on a quote row that is NOT the first (e.g. the second row cites line 9999 or one char changed) — every "
        f"battery37 P4 fixture defaces row 1 (F37XMutP4 F1, {F37}/F37XMutP4.md). N04: a quote whose text is verbatim elsewhere in "
        "its capture but not on its cited lines (F37XMutP4 F2)."),
    bat("R38BatP4b", "p4b", "N05,N06",
        "N05: a quote that matches its cited line only case-insensitively. N06: a quote cited as `capture:N-(N+1)` where N is the "
        "capture's last line and the text is on line N (range end one past the end) — reference P4 DEFECT 'outside', mutant ok. "
        "Keep P3 green (distinct texts/locations)."),
    bat("R38BatP5", "p5m", "N07,N08",
        "N07: change the bytes of the capture of a registry row that is NOT the first in ctx.spec['rows'] (consistent SHA256SUMS "
        f"line, unquoted line) so only that row's 'manifest digest differs from the spec pin' fires (F37XMutP5, {F37}/F37XMutP5.md). "
        "N08 mirror: an ACCEPT fixture whose SHA256SUMS contains a blank line (reference P5 ok; mutant: unparsed line → DEFECT)."),
    bat("R38BatP6", "p6m", "N09,N10",
        "N09: a teaches cell with exactly min_teaches_words-1 distinct words (off-by-one; F37XMutP6 X1). N10: a row URL with "
        "`http://` instead of `https://` (scheme-blind compare survives; F37XMutP6 X4). Fixture-only edits of corpus/SOURCES.md."),
    bat("R38BatP7", "p7m", "N11,N12",
        "N11: the entry's recheck line present but empty (`recheck:` with nothing after; F37XMutP7 X4). N12: the FIRST registry "
        "row's `source:` line URL changed (F37XMutP7 D1: every battery37 P7 fixture defaces S106/second row)."),
    bat("R38BatP10a", "p10a", "N13,N14",
        "Both P10 silences (`--rerun`): N13 a receipt differing from the fresh probe output only in trailing whitespace (extra "
        "trailing newline) — note P2 also fires when the receipt changes unless you own the spec and set receipt_sha256 to the new "
        "digest (then declare exactly what fires). N14 a receipt differing only after its first line. P10 runs the r35 probe "
        "through `uv run --with biopython==1.85` when Bio is absent (slow; fine)."),
    bat("R38BatP10b", "p10b", "N15",
        "mirror of the P10 pass side (R37PlanNext B5: no fixture ever sees `probe_rerun=byte-equal`): an ACCEPT fixture run with "
        "`--rerun` whose fresh probe output is byte-equal to its receipt. A fixture-owned spec may point probe_cmd at a tiny "
        "deterministic script inside the package and pin receipt/receipt_sha256/frozen_instruments consistently (see "
        f"{L}/.ufo/waves/round-37/build/R37PlanNext.md:256-257). The gate runs `[sys.executable] + probe_cmd` when `import Bio` works, "
        "else `uv run --no-project --with biopython==1.85 python3 <probe_cmd>`, cwd = root."),
    bat("R38BatMain", "mainx", "N17,N18",
        "MAIN shapes (expect=error, defects=[]): N17 `--root` pointing at a path inside d that does not exist → reference exit 2 "
        "`setup: root not a directory`; N18 a fixture-owned spec file with invalid JSON (or a spec missing a key that crashes setup) "
        "→ reference exit 2 via the crash handler; mutant returns 0. Check the mutant exit is 0/1, not 2."),
    bat("R38BatD4", "d4m", "N19,N20",
        "d4-line fixtures (ctx.d4_line() is the genuine line; spec['d4']['patterns']): N19 a line failing ONLY the last directional "
        "pattern; N20 a line whose pattern token differs only in case. Argv ['d4-line', '--file', F] with F inside d."),
    bat("R38BatD5", "d5m", "N21,N22",
        "d5-line fixtures (ctx.d5_line(), ctx.d5_capture_dir(); copy the capture dir into d): N21 a manifest whose matching row is "
        "NOT the first row (first row some other file); N22 a capture whose text contains only the first 20 non-space chars of the "
        f"quote (F37XMutD5 X3/X4, {F37}/F37XMutD5.md)."),
    # ---- C2 package (scribes) ----
    ("R38PkgEntry", "scribe", ["coverage", "depth"],
     f"Draft the C2 package for the L1 under {B}/R38PkgEntry/: (1) entry.md = corpus/knowledge/tb2-build-pmars-grader.md (follow the "
     f"shape of {L}/corpus/knowledge/tb2-git-webserver-grader.md: frontmatter-like `source: S115 <raw url>` / `source: S116 <raw url>` "
     f"lines with the EXACT pinned raw URLs {RAW}/tests/test_outputs.py and {RAW}/instruction.md, `verified-at: 2026-10-26`, "
     f"`recheck: 180d …`; sections: what is graded; `## Located quotes` table rows | claim | “quote” | `capture:line` | with >=8 "
     f"distinct verbatim 3-25-word quotes at >=8 distinct lines of {CAP}/test_outputs.py and instruction.md (check each with sed -n); "
     f"`## Requirement map` with exactly one row per TAG in {DRY} in the frozen format, label DERIVED from {RCPT} as V7 does, citing "
     f"violating case ids; findings each tied to receipt case ids; limits (host bash vs Debian dash, host ldd, oracle never run, "
     f"canned artefacts host-compiled); prior art (TB2 issue #59 is about oracle pins, not the grader; class published per "
     f"{L}/.ufo/waves/round-37/build/R37ScoutPriorArt.md — claim 'first probed instance' only); `## Negative space` with an explicit "
     f"falsifier). (2) rows.md = two 11-cell SOURCES rows S115/S116 in {L}/corpus/SOURCES.md's exact column order (read its header), "
     f"tier A, status mined, opened 2026-10-26, anchor cell `sha256 <pin>` + a <=25-word located quote, teaches >= 8 distinct words, "
     f"used-by = corpus/knowledge/tb2-build-pmars-grader.md. (3) readme.md = the index row + one coverage bullet naming the entry and "
     f"`round38/build-pmars-probe.txt`. Then PROVE it: in your clone place the three drafts, `git -C \"$S/lane\" add -A`, and run "
     f"`python3 {C2} --lane \"$S/lane\" --work \"$S/w\"` → paste output; iterate until `checks=7 defects=0`.",
     "VERDICT: c2-package-draft-checks-7-defects-<n>"),
    ("R38PkgProse", "scribe", ["coverage", "depth", "adjacency"],
     f"Draft paste-ready lane prose for C2 under {B}/R38PkgProse/: (a) a PROVINCE.md round-38 paragraph (read {L}/PROVINCE.md "
     f"round-35..37 paragraphs; same admission limits: grader probe only, task image and oracle not run; build-provenance as a new "
     f"graded-state class); (b) the corpus/README.md §Frontier TB2 sub-bullet narrowed by one task (read the current clause); (c) a "
     f"SKILL.md section 'Build-provenance TB2 grader — round 38' as a decision table (what the grader reads → what passes → what a "
     f"reviewer should check instead), every row citing a receipt case id in {RCPT}. Observations only; no class claims.",
     "VERDICT: c2-prose-drafted-<n>-rows"),
    # ---- scouts ----
    ("R38ScoutPriorArt", "scout", ["novelty", "coverage"],
     f"Prior art for the build-pmars grader findings: re-open https://github.com/harbor-framework/terminal-bench-2/issues/59 (gh api), "
     f"search terminal-bench / terminal-bench-2 / terminal-bench-2-1 / harbor issues+PRs for pmars, build-pmars, 'ldd', 'X11', "
     f"'built from source', and https://github.com/harbor-framework/terminal-bench/issues/631 (tb3 hardening audit of tb2.1 fixes) for "
     f"build-pmars mentions. For each hit: URL, date, state, <=25-word quote with location, and whether it reports a grader "
     f"permissiveness (canned output, ldd scan, shape test) or something else. Propose at most one tier-B SOURCES row (S117) for the "
     f"strongest prior report, or say none qualifies. Reuse the hit list of {L}/.ufo/waves/round-37/build/R37ScoutPriorArt.md.",
     "VERDICT: prior-art-<n>-hits-row-<yes|no>"),
    ("R38ScoutUpstream", "scout", ["freshness", "coverage"],
     f"Upstream state of build-pmars: compare all five captures in {CAP}/ with terminal-bench-2 main (curl raw + sha256sum, gh api "
     f"commits?path=build-pmars), check whether terminal-bench-2-1 carries the task (it returned 404 at build-pmars/tests/"
     f"test_outputs.py — find whether it was renamed/removed: gh api repos/harbor-framework/terminal-bench-2-1/contents), and the "
     f"docker image tag in task.toml. Report drift (none/where) with commands and outputs.",
     "VERDICT: upstream-drift-<none|n>"),
    ("R38MergeRescreen", "scout", ["coverage", "adjacency"],
     f"Assimilation re-screen of /home/vgpnk/Projects/shokuknow/merge/kengaku/ (READ-ONLY): has anything changed since round 37's "
     f"screen ({L}/.ufo/waves/round-37/build/R37ScoutMergePkg.md)? List packages with git -C /home/vgpnk/Projects/shokuknow log -1 "
     f"--format=%H -- merge/kengaku; for each knowledge entry give a verdict admit/hold/refuse with PROVINCE ({L}/PROVINCE.md) scope "
     f"reason and flip condition — at least one admit candidate and one refuse if the package supports it (say so if it cannot). Run "
     f"the id-collision check (0-3 leading spaces) of lane SOURCES vs merge/kengaku/SOURCES.append.md into {B}/R38MergeRescreen/ "
     f"(reg-ids, staged-ids, collisions) and the quarantine slice of "
     f"/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md for lane kengaku.",
     "VERDICT: merge-rescreen-admit-<n>-hold-<n>-refuse-<n>"),
    ("R38PlanNext", "scout", ["calibration", "coverage", "novelty"],
     f"Planning data-walk for round 39 (the L1 holds the planner seat; this is a bounded data walk): read {CLAIMS}, SCORECARD "
     f"`### Planned (round 38)`, the round-37 closure §5 and the wave-2 reports in {F37}/. Price 2 candidate claims for round 39 "
     f"(one on the lowest axis coverage/novelty 7, one other), each with a measured do-nothing control (run it), a counter sketch and "
     f"the cheapest skip-control. Paste-ready `### Planned (round 39)` block.",
     "VERDICT: plan39-drafted"),
    # ---- frontier / routed (executors + scribes) ----
    ("R38MapRetro", "executor", ["calibration", "quality"],
     f"Mined mistake evidence (round-37 closure D2): write {B}/R38MapRetro/map_label_retro.py that applies round-38 C2 V7's derived-"
     f"label rule to the ROUND-37 entry {L}/corpus/knowledge/tb2-git-webserver-grader.md `## Requirement map` against its receipt "
     f"{L}/corpus/evidence/round37/git-webserver-probe.txt, given a violates-mapping file you write ({B}/R38MapRetro/violates-r37.tsv: "
     f"case id → instruction.md lines it violates, derived from each case's own `-- requirement` text and instruction.md; justify "
     f"each). Expected per the closure: row instruction.md:9 `enforced` disagrees (token-in-body observed=pass). Print each row "
     f"labelled vs derived; also run it on a corrected map and show it passes. See {F37}/F37CritC2Map.md.",
     "VERDICT: map-retro-disagree-<n>-rows"),
    ("R38MapErratum", "scribe", ["calibration", "quality"],
     f"Draft under {B}/R38MapErratum/: (1) an append-only `## Errata (round 38)` section for {L}/corpus/knowledge/tb2-git-webserver-"
     f"grader.md correcting the requirement-map rows the round-37 closure falsified (D2: :107/:122 row 9 enforced→partly; :106,:119-121 "
     f"row 8 witness; :116 'port half is enforced' by-construction qualifier) — read {F37}/F37CritC2Map.md and "
     f"{F37}/F37CritC2Overclaim.md and fold in every overclaim they verify (cite each); (2) a QUALITY.md criterion Q28 (read "
     f"{L}/corpus/QUALITY.md Q24-Q27 for form): a requirement-map label is derived from every executed case that violates the "
     f"requirement, never from one witness; check = round38_c2_verify.py V7; shown able to fail = the round-37 map row 9.",
     "VERDICT: erratum-<n>-rows-q28-drafted"),
    ("R38AnchorBind", "executor", ["calibration", "operability"],
     f"Routed D3: {L}/plans/anchor_digest_check.py accepts a row whose anchor carries ANOTHER row's real committed digest "
     f"({F37}/F37AnchorRerun.md M4b/M5). Write a fixed copy at {B}/R38AnchorBind/anchor_digest_check.py binding each sha256 token to "
     f"the capture its own row names (by the row's URL/upstream path ↔ capture file, or the capture manifest entry for that file); "
     f"keep CLI/output format. Show: lane at tip → defects=0 (or list true defects); M4b/M5 cross-row fixtures (rebuild in your clone) "
     f"→ defect; old checker → defects=0 on the same fixtures. Receipts in {B}/R38AnchorBind/.",
     "VERDICT: anchor-bind-cross-row-caught-<yes|no>"),
    ("R38LedgerTip", "executor", ["operability"],
     f"Routed D4: `plans/ledger_tip.py` is red in detached-HEAD clones because {L}/plans/defect_ledger.py:29 (and "
     f"plans/round36_c1_verify.py:38) hard-code refs/heads/master ({F37}/F37NoHarmSweep.md §3). round36_c1_verify.py is PINNED by the "
     f"frozen C1 counter — do NOT propose edits to it. Draft fixed copies of defect_ledger.py and/or ledger_tip.py at "
     f"{B}/R38LedgerTip/ so a detached --shared clone either resolves the right commit or refuses with exit 2 as declared; show "
     f"before/after in a detached clone and a normal clone.",
     "VERDICT: ledger-tip-detached-<fixed|refuses|red>"),
    ("R38TipReceipts", "executor", ["operability", "freshness"],
     f"Assimilation of considerthese/2026-10-25.md proposal 2(c) ({L}/considerthese/2026-10-25.md:39-45): write "
     f"{B}/R38TipReceipts/tip_receipts.py — enumerate committed probe receipts under {L}/corpus/evidence/** that have a re-run command "
     f"in the lane (at least: round35 tb2 grader probe, round36 regex-log probe, round37 git-webserver probe, round38 build-pmars probe; "
     f"find their commands in SKILL.md's registry / plans/), re-run each on a clean clone at the tip and byte-compare; print one line "
     f"per receipt and `receipts=<n> byte_equal=<k> differ=<d> skipped=<s>` (skips named with reason). Controls: a one-byte-tampered "
     f"receipt is reported `differ`. Honour TMPDIR/--work (no hardcoded /tmp).",
     "VERDICT: tip-receipts-<k>/<n>-equal"),
    ("R38R37Integrate", "scribe", ["calibration", "quality"],
     f"Routed D1: read EVERY report in {F37}/ (*.md; note any seat still writing) and produce {B}/R38R37Integrate.md: one row per "
     f"report: seat, VERDICT line, its strongest finding (file:line), disposition (closed-by-round-38-item <name> / routed-to-round-39 "
     f"/ refused with reason / already-closed by round-37 closure). Draft LOG.md and lesson text summarising wave-2 of round 37.",
     "VERDICT: r37-falsify-integrated-<n>-reports"),
    ("R38SiblingCite", "scribe", ["adjacency"],
     f"Routed D6 ({F37}/F37ConnSiblingCite.md): find with file:line the sibling prior art for sandboxed grader probes — tameshi's bwrap "
     f"defect-probes, kumitate's cap-run.mjs, and any other lane under /home/vgpnk/Projects/shokunin/*-shokunin that runs graders or "
     f"binaries in bwrap/ldd checks (read-only). Draft a PROVINCE.md adjacency note naming each with pointer and the split (who owns "
     f"what), report-out only — never absorb.",
     "VERDICT: sibling-cites-<n>"),
    ("R38LessonDraft", "scribe", ["calibration"],
     f"Draft {B}/R38LessonDraft/round-38.md in the shape of {L}/corpus/lessons/round-37.md: header (baseline fc1174f5, freeze e0a37853, "
     f"first run e95cf550, controls), `## Gate` rows for S115, S116, the captured-not-rowed files, any prior-art row, the assimilation "
     f"decisions (≥1 admit, ≥1 reject if any), `## Mistakes` rows: (1) order-of-operations RECURRENCE — the C2 skip-control executed "
     f"the frozen probe before the first recorded run ({CLAIMS} disclosure; round-37.md §Mistakes row 3 had the same class) — "
     f"captured-by, fix that can fail; (2) witness-picked requirement-map label (closure D2); `## Census`; `## Spot-check` list for the "
     f"closure. Mark every landing number `<L1 fills>`.",
     "VERDICT: lesson-drafted"),
    ("R38ScorecardDraft", "scribe", ["calibration"],
     f"Draft paste-ready SCORECARD.md `## Round 38` section (claims table: claim | axis | before→after with counting command | score/"
     f"verdict), capability-row candidates (only if demonstrated this round — mark `pending demonstration`), and the LOG.md round-38 "
     f"entry, in the style of {L}/SCORECARD.md:1266-1312 and the LOG tail. Landing numbers as `<L1 fills>`.",
     "VERDICT: scorecard-log-drafted"),
    # ---- first falsifiers ----
    ("R38CritC1Counter", "critic", ["calibration"],
     f"Attack {C1}: find a battery38 that reaches `PREDICATE C1 pass` (or kills a mutant) WITHOUT demonstrating the advertised "
     f"behaviour — e.g. via the fixture-owned --spec loophole, the RUN or MAIN attribution rules, a mirror killed by an unrelated "
     f"accept fixture, a side channel that dodges the token scan, a fixture whose `defects` declaration is tailored. Build hostile "
     f"modules in your scratch clone and run the counter; paste outputs. Rank each hole by cost.",
     "VERDICT: c1-counter-holes-<n>"),
    ("R38CritC2Counter", "critic", ["calibration", "coverage"],
     f"Attack {C2}: build the cheapest package that reaches `checks=7 defects=0` without being a real admission (informed filler: "
     f"verbatim quotes with false claims, a map that copies derived labels, rows with correct anchors). Also probe V3's binding, V4's "
     f"`match=NO` naming via backticks, V7 row parsing (tag duplicates, extra rows, prose outside the table). Paste outputs.",
     "VERDICT: c2-counter-holes-<n>"),
    ("R38CritProbe", "critic", ["coverage", "calibration"],
     f"Attack the probe {PROBE} and its receipt {RCPT}: does each case test what its requirement text says (e.g. canned-x11-dlopen: "
     f"does the binary actually call dlopen at run time — check with ltrace/strace or LD_DEBUG in your scratch; path-split: which "
     f"pmars runs)? Are the `violates=` tag assignments defensible (list contestable ones)? Does the harness's direct call equal "
     f"pytest's verdict? Re-run the probe in your clone twice and cmp.",
     "VERDICT: probe-attack-<n>-contestable"),
    ("R38CritPytest", "critic", ["coverage"],
     f"Fidelity attack: run the captured grader under REAL pytest 8.4.1 (e.g. `uvx -p 3.13 -w pytest==8.4.1 pytest`; record uv/python "
     f"versions) inside the same bwrap layout as {PROBE} for at least 6 cases (empty-tree, canned-shape, canned-x11-dlopen, "
     f"canned-exit-nonzero, path-split, c-is-dir) — copy the probe into your clone and adapt its harness there — and compare pytest's "
     f"exit code and per-test outcomes with the receipt's tests= letters.",
     "VERDICT: pytest-agree-<k>/<n>"),
    ("R38CritIndep", "critic", ["coverage", "calibration"],
     f"Independent recompute: WITHOUT reading the probe's CASES predictions, derive from {CAP}/test_outputs.py alone the expected four "
     f"test outcomes for each of the 22 case descriptions in {DRY} (the `-- requirement` text + violates) and compare with the receipt. "
     f"Then build 3 EXTRA cases of your own (e.g. results line with leading spaces, debian as symlink, binary named pmars in /app) in "
     f"a copy of the probe in your clone, predict first, run, report.",
     "VERDICT: indep-agree-<k>/22-extra-<j>/3"),
    ("R38CritClaims", "critic", ["calibration"],
     f"Attack the claims' framing in {CLAIMS}: is C1 a calibration move (count of self-assessment vs observed mismatch) — map each "
     f"N01-N22 `adv` cell to the exact advertising sentence (file:line) or mark it unadvertised (round-37 F37CritC1Axis found 6 such "
     f"in M01-M55); is C2's class (build provenance) actually new against {L}/corpus/README.md coverage map; separability; can a "
     f"do-nothing or junk control reach either predicate; universal clauses.",
     "VERDICT: claims-attack-<n>-defects-unadvertised-<k>"),
    ("R38RevCounters", "reviewer", ["calibration", "operability"],
     f"Code review of {C1}, {C2} and {PROBE}: correctness bugs, false-green/false-red paths, determinism, TMPDIR/--work honoured (no "
     f"/tmp), pins complete (does C1 read any unpinned input? does C2?), attribution logic vs its docstring. Cite file:line.",
     "VERDICT: review-<n>-defects"),
    ("R38RevFreeze", "reviewer", ["calibration"],
     f"Freeze-order audit: `git -C {L} log --format='%H %cI %s' fc1174f5..HEAD`; confirm e0a37853 carries claims, counters, probe, dry "
     f"table, captures and controls; the receipt landed later (e95cf550); frozen-digests.txt entries match `git show e0a37853:<path> | "
     f"sha256sum`; the controls are reproducible (re-run control-c1-nothing and control-c2-nothing on a clean clone of e0a37853 and "
     f"diff); the disclosure in the claims is accurate.",
     "VERDICT: freeze-audit-<ok|n-defects>"),
    ("R38MutC2Counter", "mutation-tester", ["calibration"],
     f"Mutation-test {C2}'s checks in a clone where a passing package exists (use {B}/R38PkgEntry/ drafts if present when you start; "
     f"else build a minimal genuine package yourself from {CAP} and {RCPT}). One mutant at a time: map label flipped to `enforced`; "
     f"map row citing a non-violating case; tag duplicated; tag missing; map line number wrong; anchor token of S115 replaced by "
     f"S116's digest; receipt one CASE line deleted; `match=NO` line not named; spec one byte; dry table one byte; probe one byte. "
     f"Report caught/survived per mutant with the DEFECT line.",
     "VERDICT: c2-mutants-<caught>/<total>"),
    ("R38MutProbe", "mutation-tester", ["coverage"],
     f"Mutation-test the probe's sensitivity in a copy (never the lane file): harness maps every exception to P; PATH drops "
     f"/usr/local/sbin; canned DEBUG has one address; dlopen variant links -lX11; sandbox omits --unshare-net. For each, does the "
     f"receipt change and would C2 V4/V5/V2-P10 catch it? Report.",
     "VERDICT: probe-mutants-<caught>/<total>"),
    ("R38ConnSibling", "connector", ["adjacency"],
     f"Sibling-overlap scan for this round's surfaces (TB2 build-provenance grader, ldd/X11 checks, bwrap grader sandboxes, gate "
     f"mutation batteries) across /home/vgpnk/Projects/shokunin/*-shokunin (read-only: PROVINCE.md, SKILL.md, corpus/README.md). "
     f"Name each overlap with file:line and whether kengaku should cite, defer or report it.",
     "VERDICT: sibling-overlap-<n>"),
    ("R38ConnPattern", "connector", ["calibration", "quality"],
     f"Cross-claim pattern finding: the C1 survivors are 'check applied to the first item only', 'off-by-one threshold', 'loosened "
     f"compare', 'pass side never exercised'. Do the round-38 counters {C1} {C2} and the probe {PROBE} themselves contain any of these "
     f"shapes (e.g. V7 only reading the first table, V4 summary regex)? Do earlier lane counters (plans/round3*_*.py)? List with "
     f"file:line and a one-line fixture that would expose each.",
     "VERDICT: pattern-<n>-sites"),
    ("R38SentinelProbe", "sentinel", ["operability"],
     f"Security review: {PROBE} compiles C and runs host-built binaries in bwrap; {C1} runs battery38 fixture code with the counter's "
     f"privileges and lets fixtures own a spec whose probe_cmd the gate executes. Can a case or fixture write outside its scratch, "
     f"reach the network, read ~/.ssh or the lane's .git, or leave processes behind? Test cheaply in your scratch; cite file:line.",
     "VERDICT: sentinel-<n>-findings"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 38 wave 1 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r38 wave 1 (build + first falsifiers)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    spec = {"wave": "kengaku-r38-build",
            "milestone": "kengaku round 38 wave 1: C1 attributed gate-mutant battery38, C2 TB2 build-pmars admission, frontier step",
            "reportDir": ".ufo/waves/round-38/build", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/build-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c))
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"] + c["sentinel"]
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
