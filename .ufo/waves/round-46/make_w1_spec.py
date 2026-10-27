#!/usr/bin/env python3
"""Renders .ufo/waves/round-46/w1-spec.json (v1 wave 1 — build + pre-data attacks, policy v1 band 32-64).
L1 KengakuR46. Two v1 waves this round (64-128 directive): wave 1 builds the C1 counter/modules/fence variants,
the C2 repairs, the C3 package and its counter, and attacks the frozen C2 counter and the stage-1 freeze; wave 2
falsifies the landed tree."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-46"
B = f"{W}/w1"
SCR = "/fast/scratch/hyaku/kengaku-r46"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/polyglot-c-py"
BASE = "64ba8385ea10af1b78d367dcb242b92d97062af7"
FREEZE = "fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f"
CLAIMS = f"{L}/plans/round-46-claims.md"
CL = f"{W}/claims"
ENV = f"{CL}/envelope.sh"
C45_1 = f"{L}/plans/round45_c1_verify.py"
C45_2 = f"{L}/plans/round45_c2_verify.py"
K44 = f"{L}/plans/round44_c1_verify.py"
FENCE = f"{L}/plans/fixture_fence.py"
R45 = f"{L}/.ufo/waves/round-45"
HO = f"{R45}/a3w1"
CRIT = f"{R45}/w1/R45CriticPredicate.md"
C2V = f"{L}/plans/round46_c2_verify.py"
ALC = f"{L}/plans/anchor_line_check.py"
ENTRY45 = f"{L}/corpus/knowledge/tb2-password-recovery-grader.md"
CAP45 = f"{L}/corpus/evidence/round45/tb2-password-recovery"
SRC = f"{L}/corpus/SOURCES.md"

HOST_RULE = (
    "Host safety: run any fixture build, counter run or probe that can write files inside a bwrap sandbox in which "
    "`/home/vgpnk/.local/bin` is read-only (the envelope below does this). Never write to a shared PATH directory, "
    "`/usr`, `/etc`, or `$HOME` outside scratch.")
ENVELOPE = (f"Envelope for every counter/fixture/probe run: `{ENV} \"$S/env\" <command...>` (home read-only, ~/.cache "
            f"overlaid from scratch, start/end times, a CONTENT digest of ~/.local/bin before/after; exit 4 + `INVALID` when "
            f"the digest changes — then the measurement does not count). Paste the ENVELOPE lines with every result.")
SCRATCH = (f"Scratch rule (operator directive 2026-10-25): S={SCR}/<YourSeatName>; mkdir -p \"$S\"; export TMPDIR=\"$S\"; pass "
           f"\"$S\" explicitly as --work / mkdtemp(dir=...). Delete it before you finish with `python3 {L}/plans/scratch_guard.py "
           f"safe-rm {SCR} <YourSeatName> \"$S\"`. Never delete {SCR}, its `.ROUND-ROOT-SENTINEL` or another seat's dir. /tmp only "
           f"for files under 50 MB; a /tmp or scratch path is never evidence — copy receipts into your report subdir first.")
CLONE = (f'Clone rule: git clone -q --shared {L} "$S/lane"; verify `git -C "$S/lane" rev-parse --show-toplevel` equals "$S/lane" '
         f'before any write; every git call names -C "$S/lane"; never commit there unless your item says a scratch commit is '
         f'needed, and then only inside "$S/lane". Any other fixture repo: D=$(mktemp -d -p "$S") && git -C "$D" init -q, verify '
         f'`git -C "$D" rev-parse --show-toplevel` = $D, every git call names -C "$D". Never run `git commit`/jj with a throwaway '
         f'identity anywhere else.')

CONTEXT = f"""# Goal
kengaku round 46 (hyaku run 9, 2026-10-27), WAVE 1 of two v1 waves (build + pre-data attacks). Lane repo: {L}.
Read the frozen claims FIRST, in full: {CLAIMS} (stage-1 freeze commit {FREEZE}; base = round-45 closure tip {BASE}).
The round-45 non-author closure that routed this round: {L}/corpus/lessons/round-45-verifier-spotcheck.md (§2, §5).
Frozen and never edited by any seat: {CLAIMS}, {C2V}, {ALC}, {CL}/, {C45_1}, {C45_2}, {K44}, plans/battery42|43|44,
plans/refusals45/, every corpus/evidence/ capture.

Three claims:
- C1 calibration — the fixture fence ({FENCE}, contract `breach(d: pathlib.Path, argv: list[str], tool: str) -> str|None`,
  None admits) vs what the lane advertises, under a NEW counter `plans/round46_c1_verify.py` that hides its own names (QUALITY
  Q39, {L}/corpus/QUALITY.md:1059-1087) and closes the round-45 counter bypasses B1/B3/B4/B5/B6 ({CRIT}). Refusal modules =
  plans/refusals45/ f1-f10 + the round-45 held-out modules the base fence admits/reads ({HO}/R45HoIncludeIf, R45HoSymlinks,
  R45HoArgvEnv, R45HoCommondir2, R45HoConfigKeys and their .md reports); SEALED = new hostile modules wave-1 critics write that NO
  fence-writing seat may read. ORDER RULE: the new counter is pinned at a stage-2 amendment BEFORE any repaired fence is scored by
  it — so no seat runs a repaired fence through a draft of plans/round46_c1_verify.py, and no fence-writing seat opens another
  seat's files under {B}/ (sealed modules live there).
- C2 depth — FROZEN WHOLE. `python3 {C2V} --lane .` at base prints `A anchorline live=8` (S108 words; S149 range; S150 words;
  S151 range+words; S152 line+words; S153 line+range+words; S154 line+range; S155 range+words), `B predictor disagree=6`
  (the entry's `## Predictor` converts only CRLF; the captured grader reads universal newlines), `C entry source_ranges_bad=4
  errata_marks=0/5`. Work: superseding rows S157-S165 (QUALITY Q34: a NEW row whose `teaches` opens `supersedes S0NN —`; never
  edit an old row's immutable cells), the entry's predictor/source ranges/`## Errata (round 46)`. Gate tool {ALC} (`--selftest`).
- C3 coverage — the pinned Terminal-Bench 2.0 `polyglot-c-py` grader (terminal-bench-2 @ {PIN}; raw base {RAW}/) admitted as
  {L}/corpus/knowledge/tb2-polyglot-c-py-grader.md with rows from S166, a probe `plans/polyglot_c_py_probe.py`, spec
  `plans/pkg-spec-r46.json`, counter `plans/round46_c3_verify.py`. ORDER RULE (QUALITY Q30): before the stage-2 freeze the probe
  runs ONLY `--dry` / stage-check — no seat executes a graded case of this task, and no seat runs `plans/pkg_gate.py --rerun`
  on the package. Template: the round-45 package — {C45_2}, {L}/plans/password_recovery_probe.py, {L}/plans/pkg-spec-r45.json,
  {ENTRY45}, {L}/corpus/evidence/round45/ (captures + receipts), and the round-45 claims {L}/plans/round-45-claims.md §C2.

# Host-safety rule (binding for every seat)
{HOST_RULE}
{ENVELOPE}

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report is {B}/<YourSeatName>.md; drafts and receipts go under {B}/<YourSeatName>/ (create it). Never copy
  a corpus/ or plans/ tree, a lane mirror or a clone into {B}/; no receipt file over 1 MiB (quote it, give its sha256, delete it).
  Every seat MUST leave its report file.
- {SCRATCH}
- Write ONLY inside {B}/<YourSeatName>.md, {B}/<YourSeatName>/ and your scratch dir. NEVER edit the lane's corpus/, plans/,
  SCORECARD.md, LOG.md, README.md, SKILL.md, PROVINCE.md, SHONEN.md or any other lane file — draft for the L1, who integrates.
  Never write into {F} (fleet root), sibling lanes, the lane's jj state or Git index. Never run git add/commit/stash/checkout/
  reset/push/pull or any mutating jj command in the lane. Seats never commit or push anywhere.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY. considerthese/ in the lane is operator-authored: read, never edit.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide:
  install via `uv tool` / `npx` / an official binary into ~/.local/bin (outside any bwrap run), or install nothing and say so.
  Never run pacman -Sy/-Syu/-U/-R, never name an already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat probe).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location (file:line or
  URL+section) and is <= 25 words. Do not fabricate output; if something cannot be fetched or run, say so.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""

MODULE_RULE = (f"A hostile module is one Python file in the contract of {L}/plans/refusals45/f7_commondir.py (read it, f1, f10 and "
               f"{K44} `builder_source`/`Ctx` first): `build_accept(ctx, d)` / `build_reject(ctx, d)` return an argv list for tool "
               f"`order`, or whatever the r44 builder expects — mirror an existing module exactly. Prove each module with the "
               f"round-45 counter's own machinery on a clone at {BASE} (the driver pattern of {HO}/R45HoCommondir2/driver.py: "
               f"`build_module` + `run_fence` from {C45_1}) and report per module LEAKED / READ / clean under the BASE fence. "
               f"Keep only modules that are LEAKED or READ under the base fence.")

SEAL = (f"SEALED module authoring: write NEW hostile modules (not variants of {HO}/R45Ho* or plans/refusals45/) into "
        f"{B}/<YourSeatName>/sealed/<short_name>.py plus a SHA256SUMS file there; the fence-writing seats are forbidden to read "
        f"them, so state nothing about their mechanism in your report beyond one line per module (class name + base-fence verdict). "
        f"Mechanism notes go in {B}/<YourSeatName>/sealed/NOTES.md. {MODULE_RULE}")

FENCE_SPEC = (
    f"Implement a repaired `plans/fixture_fence.py` in your own clone (start from {FENCE} @ {BASE}; read its docstring, {C45_1} "
    f"docstring, and {CRIT}). It must REFUSE every module of plans/refusals45/ and every held-out module under {HO}/R45HoIncludeIf/, "
    f"R45HoSymlinks/, R45HoArgvEnv/, R45HoCommondir2/modules/, R45HoConfigKeys/ (their .md reports name which the base fence admits), "
    f"ADMIT all 104 honest fixtures of plans/battery42|43|44, and never open, stat or readlink a path outside d while deciding. Test "
    f"it ONLY with the round-45 counter {C45_1} (run on your clone) and the R45Ho* drivers (point them at your clone) — NEVER with "
    f"any draft of plans/round46_c1_verify.py, and NEVER open anything under {B}/ except your own subdir (sealed held-out modules "
    f"live there). Generalize: the closure ruled round 45's denylist fence unprovable because 9 of 14 held-out modules got through, "
    f"so prefer a design that refuses whatever it cannot prove safe over one that names attack classes. Deliver "
    f"{B}/<YourSeatName>/fixture_fence.py, the counter output (`PREDICATE C1 pass` expected under the r45 counter), a per-held-out-"
    f"module table under the r45 driver, and your design's limits. Use stdlib only; one-line reason strings.")

ITEMS = [
    # ---------------- C1 calibration ----------------
    ("R46ExecC1Counter", "executor", ["calibration"],
     f"Write `plans/round46_c1_verify.py` in your clone, derived from {C45_1} and {R45}/claims/dev_blind_c1_verify.py, to the "
     f"contract in {CLAIMS} §C1 (a)-(i), and its docstring = the full rule, ending with the frozen predicate lines verbatim from the "
     f"claims file (`PINS total=<P> …`, `REFUSALS …`, `SEALED …`, `HONEST …`, `CALIBRATION advertised=<R+S> contradicted=0`, "
     f"`PREDICATE C1 pass`). Take REFUSAL dir `plans/refusals46` and SEALED dir `plans/sealed46` as constants (add `--refusals DIR` "
     f"/ `--sealed DIR` overrides for testing only). Closes: B2 random per-run names (`secrets.token_hex`) + shuffled jobs; B1 log "
     f"outside the fence's writable namespace (e.g. run strace OUTSIDE bwrap, or deliver by fd) and tamper = READ; B3 whole scratch "
     f"root counted except harness + fence copy; B4 verdict by harness exit status (10 BREACH / 11 ADMIT, anything else ERROR); B5 "
     f"stat/lstat/newfstatat/statx/access/faccessat/readlink(at) traced and counted; B6 pending/resumed opens decoded with their "
     f"stored text, dirfd-relative paths resolved. Test ONLY with controls: no fence, the BASE fence ({FENCE} @ {BASE}) with "
     f"refusals = plans/refusals45 (+ the R45HoCommondir2 modules dir as a second refusal dir if that helps), {R45}/claims/fences/*.py, "
     f"and the forged fences in {R45}/w1/R45CriticPredicate/ (if present) — every one must print `PREDICATE C1 fail`; report each "
     f"control's REFUSALS/HONEST/CALIBRATION lines. Never run a repaired fence through it. Deliver {B}/<YourSeatName>/round46_c1_verify.py "
     f"and receipts; name remaining bypasses honestly (B7 io_uring etc).",
     "VERDICT: c1-counter-drafted-controls-failing-<k>/<n>"),
    ("R46ExecC1Modules", "executor", ["calibration"],
     f"Convert the round-45 held-out modules into the refusal-module contract for `plans/refusals46/` (names f11_*.py, f12_*.py, …): "
     f"every module from {HO}/R45HoIncludeIf/, R45HoSymlinks/, R45HoArgvEnv/, R45HoCommondir2/modules/, R45HoConfigKeys/ that the BASE "
     f"fence admits or reads (read each .md report's table/VERDICT). Some are drivers that build several fixtures in one file — split "
     f"so one file = one hostile class. {MODULE_RULE} Also byte-copy f1-f10 from plans/refusals45/ into your draft dir and confirm "
     f"sha256 equality. Deliver {B}/<YourSeatName>/refusals46/ (complete dir) + SHA256SUMS + a table module -> source report -> base "
     f"verdict -> opens, and the r45-counter run over the whole dir (`--refusals` is not a flag of the r45 counter: run it on a clone "
     f"where plans/refusals45 is replaced by your dir and REFUSAL_TOTAL edited, and say so).",
     "VERDICT: refusals46-modules-<n>-base-leaked-<a>-read-<r>"),
    ("R46ExecC1FenceA", "executor", ["calibration"],
     f"{FENCE_SPEC} Variant A — ALLOWLIST: refuse unless `.git` is a real directory whose entries, config sections/keys and refs "
     f"match a small allowlist of what a plain `git init` + commits produce; lstat only, never follow a symlink; git called only after "
     f"the static proof, with the pinned env.",
     "VERDICT: fenceA-r45-pass-<yes|no>-heldout-refused-<k>/<n>"),
    ("R46ExecC1FenceB", "executor", ["calibration"],
     f"{FENCE_SPEC} Variant B — NO GIT: decide every fixture by reading only files inside d (loose objects via zlib, packed refs, "
     f"HEAD), refusing every store shape it cannot parse itself; never spawn git.",
     "VERDICT: fenceB-r45-pass-<yes|no>-heldout-refused-<k>/<n>"),
    ("R46ExecC1FenceC", "executor", ["calibration"],
     f"{FENCE_SPEC} Variant C — ISOLATED GIT: run every git probe inside an inner sandbox that binds only d (bwrap/unshare if nested "
     f"namespaces work under the counter's sandbox — test that first and report), so any reference outside d fails and is refused; "
     f"keep a static pre-check for symlinks/argv. If nesting is impossible, say so with the error and fall back to variant A ideas.",
     "VERDICT: fenceC-r45-pass-<yes|no>-heldout-refused-<k>/<n>"),
    ("R46CritC1Forged", "critic", ["calibration"],
     f"Build the C1 stage-2 control panel: port each forged fence of {CRIT} (B1 log erasure, B2 keyed path, B3 host read and module-"
     f"source read, B4 stdout spoof, B5 stat channel, B6 killed blocked open) into standalone fence files, plus NEW keyed fences that "
     f"key on whatever a name-hiding counter may still expose (sibling-dir count via stat of d.parent, argv absolute-path shape, "
     f"fixture count, inode/mtime order, env). Each file states which bypass it exercises and the verdict a sound counter must print. "
     f"Prove each still forges a pass under the round-45 counter {C45_1} on a clone (receipts). Deliver {B}/<YourSeatName>/fences/ + "
     f"SHA256SUMS + table.",
     "VERDICT: forged-fences-<n>-r45-forged-pass-<k>"),
    ("R46CritC1SealConfig", "critic", ["calibration"], f"{SEAL} Family: git CONFIG surfaces not yet covered (other include forms, "
     f"core.* path keys, url.*, safe.directory, extensions.*, worktree config, config-file encodings). Target 3-5 modules.",
     "VERDICT: sealed-config-<n>-base-leaked-<a>-read-<r>"),
    ("R46CritC1SealPaths", "critic", ["calibration"], f"{SEAL} Family: filesystem shape (symlinks/hardlinks inside .git and the work "
     f"tree, special files, path length, case/Unicode tricks, objects/info/* files, packed-refs, shallow). Target 3-5 modules.",
     "VERDICT: sealed-paths-<n>-base-leaked-<a>-read-<r>"),
    ("R46CritC1SealArgv", "critic", ["calibration"], f"{SEAL} Family: argv/env shape for tools `anchor` and `order` (token forms "
     f"`--opt=value`, brace prefixes (`R45CritIntent`), relative escapes, NUL/newline tokens, duplicate options). Target 3-5 modules.",
     "VERDICT: sealed-argv-<n>-base-leaked-<a>-read-<r>"),
    ("R46CritC1SealStore", "critic", ["calibration"], f"{SEAL} Family: git STORE indirection (gitfile variants, GIT_DIR-like files, "
     f"worktrees/ metadata, alternates in other forms, refs pointing out, replace refs, grafts). Target 3-5 modules.",
     "VERDICT: sealed-store-<n>-base-leaked-<a>-read-<r>"),
    ("R46CritC1Freeze", "critic", ["calibration"],
     f"Attack the STAGE-1 freeze of C1 in {CLAIMS} before any data: is the predicate reachable without the work (Q31/Q37/Q39)? Is the "
     f"two-stage freeze sound — what could the L1 tune at stage 2 that the stage-1 text fails to forbid? Is `contradicted` the right "
     f"calibration count against the advertisement (SCORECARD capability `fenced-fixture-discovery`, the fence docstring)? Does the "
     f"kill rule on wave-2 held-out modules bind? Name each gap and the exact sentence that would close it.",
     "VERDICT: c1-freeze-gaps-<n>-verdict-changing-<k>"),
    ("R46RevC1Advert", "reviewer", ["calibration"],
     f"List every statement the lane makes about the fence and its counter (SCORECARD.md capability rows and round-44/45 cells, "
     f"{FENCE} docstring, {C45_1} docstring, corpus/lessons/round-44.md, round-45.md, QUALITY Q37-Q39, SKILL.md) with file:line, and "
     f"for each say observed-true / observed-false / untested at base {BASE}, citing the round-45 wave receipts. This is the "
     f"advertised list the round-46 calibration count is about. Deliver a table and the count of observed-false statements.",
     "VERDICT: fence-advertisements-<n>-observed-false-<k>"),
    # ---------------- C2 depth ----------------
    ("R46ScribeC2Rows", "scribe", ["depth"],
     f"Draft superseding registry rows S157-S165 (QUALITY Q34, {L}/corpus/QUALITY.md:759-822; precedent rows S036, S064 in {SRC}) "
     f"for, in order, S108, S149, S150, S151, S152, S153, S154, S155, S156. Each is a full 11-cell row: same source URL/pin, `teaches` "
     f"opening `supersedes S1NN — ` then the corrected teaching, anchor with the RIGHT line, a `<file>:1-<n>` range equal to the real "
     f"line count (or a range that holds the line), and `(K words)` = whitespace tokens; S150/S154/S156 kind `docs` (precedent S139, "
     f"S143, S146); S154 `teaches` quotes only text the README holds (closure D6). Verify every cell against the committed captures "
     f"({CAP45}/, corpus/evidence/round36/tb2-regex-log/ for S108) AND re-open each URL live (curl, sha256 = registry). Then prove "
     f"them: on a clone, append your rows and run `python3 {ALC} --lane \"$S/lane\"` (must print `live=0` and these 8 `repaired`) and "
     f"`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file \"$S/lane/corpus/SOURCES.md\"` (exit 0). Also propose "
     f"`status`/`used-by` old->new for the superseded rows (mutable cells only). Deliver {B}/<YourSeatName>/rows.md (rows only, "
     f"ready to append) + a per-row ≤25-word located quote table for the lesson Gate (closure D2).",
     "VERDICT: c2-rows-9-live-<n>-census-exit-<rc>"),
    ("R46ScribeC2Entry", "scribe", ["depth"],
     f"Draft the repaired {ENTRY45}: (1) `## Predictor` reads universal newlines (e.g. `text.replace(\"\\r\\n\", \"\\n\").replace(\"\\r\", "
     f"\"\\n\")`) under the r45 lint (no `{{`, `}}`, import, open, …: {C45_2} PRED_LINT_TOKENS) and its prose (:191-194) says what the "
     f"code does; (2) `source:` lines' ranges equal real line counts (setup.sh 43, test.sh 29, README 33, solve.sh 68, test_outputs 18, "
     f"Dockerfile 20 — re-count yourself); (3) a `## Errata (round 46)` section naming each corrected statement with its old text "
     f"and evidence: the lone-CR predictor gap (closure §2 C2 row), the prose overclaim (:150, :194), S152/S153/S154 wrong anchors "
     f"(superseded by S161/S162/S163), the `empty-file` Mechanism row that names :16 where :18 decides, and the range cells. Prove it "
     f"on a clone: `python3 {C2V} --lane \"$S/lane\"` legs B and C ok, AND the frozen round-45 counter `python3 {C45_2} --lane "
     f"\"$S/lane\"` still prints `checks=11 defects=0` (no-harm; if any V leg turns red say which and why, do not hide it). Deliver "
     f"{B}/<YourSeatName>/tb2-password-recovery-grader.md + a unified diff vs base.",
     "VERDICT: c2-entry-legB-<ok|defect>-legC-<ok|defect>-r45-counter-<pass|fail>"),
    ("R46RevC2Rederive", "reviewer", ["depth"],
     f"Independently hand re-derive leg A's base count: for every row of {SRC} whose anchor cites `:N \"quote\"`, open the capture "
     f"its sha256 names (find it under {L}/corpus/evidence/ by digest) and check line, range, `(K words)` by eye/`sed -n`/`wc -w`. "
     f"Compare with `python3 {ALC} --lane {L}` (8 live rows). Report every disagreement, every row the tool cannot parse that a human "
     f"reads as a line citation (false negatives), and whether the quote regex mis-splits quotes holding inner quotes.",
     "VERDICT: anchorline-base-rederived-agree-<k>/<n>-false-negatives-<m>"),
    ("R46CritC2Counter", "critic", ["depth"],
     f"Attack the FROZEN C2 counter {C2V} and gate {ALC} (pre-data): find any tree that prints `PREDICATE C2 pass` without the "
     f"routed repair being real — e.g. a superseding row that passes leg A but is false in another cell, a predictor that passes the "
     f"16 states but disagrees with the grader elsewhere (try BOM, NUL, surrogates, very long lines, trailing whitespace variants), "
     f"errata text that satisfies the 5 tokens without correcting anything, deleting the `## Predictor` prose, a capture swap. "
     f"Demonstrate each on a clone (receipts). Rank verdict-changing ones.",
     "VERDICT: c2-counter-bypasses-<n>-verdict-changing-<k>"),
    ("R46MutC2Gate", "mutation-tester", ["depth"],
     f"Mutation-test {ALC} and {C2V} in scratch copies: each single-edit mutant (drop the line check, off-by-one line index, range "
     f"`<=`→`<`, words check removed, supersede regex loosened, base-row comparison skipping a cell, leg B state list trimmed, errata "
     f"token removed) — does `--selftest` or one of the frozen controls in {CL}/control-c2-*.txt (re-run them per mutant on clones "
     f"built like the L1's: `--shared` clone of {BASE} + the two tools) catch it? Table mutant -> killed-by.",
     "VERDICT: c2-mutants-killed-<k>/<n>"),
    ("R46ExecC2States", "executor", ["depth"],
     f"Independent ground truth for leg B: in a bwrap sandbox, execute the CAPTURED grader {CAP45}/test_outputs.py's two test "
     f"functions on each of the 16 STATE_SHAPES in {C2V} (write the file with newline=''), and on 30 more newline/whitespace states you "
     f"choose (BOM, NUL, \\x1c-\\x1f, U+0085, U+2028, trailing \\r, \\r\\r\\n). Report the grader verdict per state and which simple "
     f"predictors (CRLF-only, universal-newline replace, splitlines, strip-per-line) agree. Is the universal-newline predictor exact "
     f"on all of them? If not, give the exact predictor and its lint status under {C45_2} PRED_LINT_TOKENS.",
     "VERDICT: grader-newline-states-<n>-universal-predictor-disagree-<k>"),
    # ---------------- C3 coverage ----------------
    ("R46ExecC3Capture", "executor", ["coverage"],
     f"Capture every file of the task directory `polyglot-c-py` at terminal-bench-2 {PIN} (list it via the GitHub tree API or a "
     f"shallow `git clone --filter=blob:none` of harbor-framework/terminal-bench-2 in scratch at that commit): curl each raw file, flat "
     f"basenames like {CAP45}/ (round-45 convention: tests/test_outputs.py -> test_outputs.py, environment/Dockerfile -> Dockerfile; "
     f"a dotfile `.gitignore` -> `gitignore`), write SHA256SUMS, re-fetch once and `cmp`, and fetch the same paths at upstream HEAD to "
     f"report drift. Deliver {B}/<YourSeatName>/tb2-polyglot-c-py/ (captures + SHA256SUMS) and a table path -> bytes -> lines -> sha256.",
     "VERDICT: polyglot-captures-<n>-refetch-identical-<k>/<n>-head-drift-<d>"),
    ("R46ScoutC3Grader", "scout", ["coverage"],
     f"Read the polyglot-c-py grader and its harness at the pin ({RAW}/tests/test_outputs.py, tests/test.sh, instruction.md, "
     f"solution/solve.sh, environment/Dockerfile, task.toml): list each DECISIVE line (file:line + ≤25-word quote) and what it decides; "
     f"the instruction requirements (instruction.md:line) and whether the grader enforces each (e.g. 'kth Fibonacci' for ANY N vs three "
     f"fixed points; 'single file'; python 3.12.3/gcc 13.2.0); the listing check's non-idempotence (the grader's own gcc writes cmain into "
     f"/app/polyglot); exit-status/stdout subtleties (`check=True`, `.strip()`). Compare with the lane's eleven exemplars "
     f"({L}/corpus/README.md coverage map) and name the class. No graded execution.",
     "VERDICT: polyglot-decisive-lines-<n>-requirements-<m>-unenforced-<u>"),
    ("R46ExecC3Probe", "executor", ["coverage"],
     f"Write `plans/polyglot_c_py_probe.py` in your clone modelled on {L}/plans/password_recovery_probe.py: a frozen case table "
     f"(~14-18 cases: oracle solve.sh output, a lookup-table polyglot that hardcodes 42/10/0, python-only, C-only, extra file in "
     f"/app/polyglot, leftover cmain before grading, wrong value, trailing whitespace/newlines in stdout, non-zero exit, stderr noise, "
     f"N parsed differently, compile warning, a re-grade of the same state (non-idempotence), absent dir) each with a PREDICTED verdict "
     f"and the instruction line it violates; `--dry` prints the table byte-stably; `--stage-check` validates the recipes WITHOUT running "
     f"the grader; a real run (no flag) executes the CAPTURED grader's test function in a bwrap sandbox with host gcc + python3, /app "
     f"remapped. ORDER RULE: you may run only --dry and --stage-check. Deliver {B}/<YourSeatName>/polyglot_c_py_probe.py, its --dry "
     f"output as polyglot-c-py-dry-cases-freeze.txt, and the stage-check receipt.",
     "VERDICT: polyglot-probe-cases-<n>-stagecheck-failed-<k>"),
    ("R46ExecC3Counter", "executor", ["coverage"],
     f"Write `plans/round46_c3_verify.py` in your clone from {C45_2} (read it fully) re-pointed at the polyglot package per {CLAIMS} "
     f"§C3: V1-V11 (gate = `plans/pkg_gate.py` run from its round-45 bytes — fail if its digest differs from {C45_2} GATE_SHA256; spec "
     f"`plans/pkg-spec-r46.json`; probe/dry/captures pinned by placeholders the L1 fills at stage 2; V8 order check against "
     f"{CLAIMS} with receipt `corpus/evidence/round46/polyglot-c-py-probe.txt`; V11 held-out predictor over generated end states of "
     f"`/app/polyglot` — the predictor gets the file listing + the source text and predicts the grader verdict; refuse lookup shapes "
     f"per {R45}/a3w1/R45CritV11Bypass.md), V12 its own anchor-line rule (line/range/words, the {ALC} semantics, re-implemented, not "
     f"imported) on the package's rows, V13 the filler package: a committed do-nothing entry+rows of the right shape under "
     f"`plans/filler46/` must make V1-V12 print ≥1 DEFECT. Test ONLY on controls (base tree, filler package, an echo receipt = the dry "
     f"table copied as the receipt): each must print `PREDICATE C3 fail`. No graded run, no `pkg_gate --rerun`. Deliver the counter, "
     f"the filler package and control receipts under {B}/<YourSeatName>/.",
     "VERDICT: c3-counter-checks-<V>-controls-failing-<k>/<n>"),
    ("R46ExecC3Spec", "executor", ["coverage"],
     f"Write `plans/pkg-spec-r46.json` for the polyglot package in the schema of {L}/plans/pkg-spec-r45.json (read {L}/plans/pkg_gate.py "
     f"to learn what P1-P10 check): rows S166.. for each admitted capture (test_outputs.py, test.sh, instruction.md, solve.sh, "
     f"Dockerfile, task.toml, any other file the grader or oracle depends on), entry path, receipt path, captures dir "
     f"`corpus/evidence/round46/tb2-polyglot-c-py`, probe path. Fetch the captures yourself at {RAW}/ for digests. Run `python3 "
     f"{L}/plans/pkg_gate.py --help` and the gate's spec-only checks if it has any; never `--rerun`. Deliver the spec + a note on "
     f"every field.",
     "VERDICT: pkg-spec-r46-rows-<n>-fields-checked-<k>"),
    ("R46ScribeC3Rows", "scribe", ["coverage"],
     f"Draft SOURCES rows from S166 for the polyglot captures in the 11-cell schema of rows S149-S156 of {SRC}, kind `code` for code "
     f"and `docs` for instruction.md/README/task.toml (precedent S139/S143/S146), tier A, status mined, opened 2026-10-27, recheck "
     f"180d, used-by `corpus/knowledge/tb2-polyglot-c-py-grader.md`. Every anchor: `commit {PIN}, <file>:1-<real line count>, :N "
     f"\"<verbatim ≤25-word quote>\" (<whitespace token count> words); sha256 <64 hex>` — verify line, range and count yourself with "
     f"`sed -n Np`/`wc -l`/`wc -w`, and prove them with `python3 {ALC}` on a clone with the rows appended and the captures placed at "
     f"corpus/evidence/round46/tb2-polyglot-c-py/ (scratch only): these rows must not appear as defective. Re-open each URL live. "
     f"Deliver rows.md + the Gate table (candidate, verdict, reason+flip, URL, access date, ≤25-word located quote), incl. at least "
     f"one REJECT with reason.",
     "VERDICT: c3-rows-<n>-anchorline-defective-<k>-census-exit-<rc>"),
    ("R46ScribeC3Entry", "scribe", ["coverage"],
     f"Draft `corpus/knowledge/tb2-polyglot-c-py-grader.md` in the structure of {ENTRY45} (provenance trio `source:`/`verified-at:`/"
     f"`recheck:`, `## Summary`, `## Located quotes`, `## Requirement map`, `## Case table` (placeholder rows the L1 fills from the "
     f"receipt after the stage-2 freeze — mark them TBD), `## Mechanism`, `## Findings`, `## Negative space`, `## Predictor` (one "
     f"```python block `predict(listing, source)` or the shape R46ExecC3Counter's V11 defines — coordinate by reading only its "
     f"report when it exists, never its files), `## Limits`). Everything from reading the captured sources at {RAW}/; no graded run. "
     f"Name the class against the lane's eleven exemplars.",
     "VERDICT: c3-entry-sections-<n>-tbd-<k>"),
    ("R46ScribeC3Index", "scribe", ["coverage"],
     f"Draft the index lines for C3: the README coverage-map bullet + index row + §Frontier narrowing (`11 of 89 read` -> `12 of 89`, "
     f"{L}/corpus/README.md ~:430) and the PROVINCE.md paragraph naming `polyglot-c-py` and the entry path on one line (round-45 V9 "
     f"style). Read the round-45 additions first (`git -C {L} show 7d062c0 -- corpus/README.md PROVINCE.md`). Deliver exact "
     f"insertion text with anchors (the line after which each goes).",
     "VERDICT: c3-index-lines-<n>"),
    ("R46ScoutC3Prior", "scout", ["coverage", "novelty"],
     f"Prior art / upstream record for polyglot-c-py and the dual-runtime output-compare grader class: search GitHub issues/PRs of "
     f"harbor-framework/terminal-bench-2 and laude-institute/terminal-bench for polyglot-c-py (lookup-table cheats, cmain "
     f"non-idempotence, gcc/python version drift), and published notes on fixed-point output graders. Open every hit (not search "
     f"snippets) and give URL, access date, ≤25-word located quote; mark synthesised answers as not citable. Propose SOURCES rows "
     f"(tier, scope) only for opened primary sources.",
     "VERDICT: polyglot-prior-art-opened-<n>-row-candidates-<k>"),
    ("R46CritC3Freeze", "critic", ["coverage"],
     f"Attack C3's stage-1 freeze in {CLAIMS} and the round-45 template counter {C45_2} as the C3 counter will inherit it: which V "
     f"legs an echo/filler/do-nothing package can satisfy; whether V8/Q30 binds the first recorded run; whether the case table can be "
     f"tuned after reading the grader (it can — say what prevents tuning to verdicts rather than mechanisms); what a V11 predictor "
     f"over (listing, source) can memorize. Each gap with the sentence that closes it at stage 2.",
     "VERDICT: c3-freeze-gaps-<n>-verdict-changing-<k>"),
    ("R46SentC3Sandbox", "sentinel", ["coverage", "safety"],
     f"Design-review the polyglot probe sandbox before it runs: compiling and executing agent-shaped C and Python on the host — what "
     f"must the bwrap invocation unshare/bind (net, /home, /fast, $HOME, ~/.local, /tmp), resource limits (fork bombs, infinite loops, "
     f"huge output), and how the round-45 `R45SentinelC2Sandbox` HOME escape ({R45}/w1/R45SentinelC2Sandbox.md) applies. Test a "
     f"hostile main.py.c (writes outside /app, opens network, forks) in YOUR OWN sandbox draft — not the grader, not a case of the probe.",
     "VERDICT: polyglot-sandbox-risks-<n>-mitigated-in-draft-<k>"),
    # ---------------- routed / frontier ----------------
    ("R46ExecLogAppendOnly", "executor", ["calibration"],
     f"Mined mistake (closure D1): two committed round-45 LOG.md lines were rewritten in place at 3d9ea54 (`git -C {L} diff -U0 "
     f"fbad1c5 3d9ea54 -- LOG.md`). Write `plans/log_appendonly.py` (stdlib, read-only, TMPDIR honoured): walk `git log --format=%H "
     f"-- LOG.md` and report every commit that deletes or changes a line of LOG.md committed earlier (pure additions are fine), "
     f"`LOG-APPENDONLY commits=<n> violations=<k>`, exit 1 iff k>0; `--since <rev>` to bind from a revision forward. Show it able to "
     f"fail: two-commit fixture repos (green = append only, red = edit a line) under $S, plus the lane's own history (list every "
     f"violation it finds, incl. 3d9ea54). Deliver tool + receipts in {B}/<YourSeatName>/.",
     "VERDICT: log-appendonly-lane-violations-<k>-fixture-red-green-<ok|fail>"),
    ("R46ScribeMistakes", "scribe", ["calibration"],
     f"Draft `## Mistakes` rows (class · evidence pointer · captured-by · fix) for corpus/lessons/round-46.md from the round-45 "
     f"closure ({L}/corpus/lessons/round-45-verifier-spotcheck.md D1-D6, §2) and the round-45 lesson: at least the LOG in-place "
     f"rewrite (D1), the Gate without per-row quotes (D2), receipts without the measured revision (D3), the unnamed post-freeze edit "
     f"(D4), the predictor prose overclaim. Each row's captured-by names the QUALITY criterion that should have caught it or `none`, "
     f"and the fix says how it is shown able to fail. Also draft a LOG.md correction entry (append-only) for D1 quoting both old and "
     f"new lines with the diff command.",
     "VERDICT: mistakes-rows-<n>-captured-by-none-<k>"),
    ("R46RevRouted", "reviewer", ["calibration"],
     f"Re-check the carried routed items at base {BASE}: `R45SentC2Grader` F1/F2/F3 ({R45}/a3w1/R45SentC2Grader.md), "
     f"`R45CritV11Bypass` ({R45}/a3w1/R45CritV11Bypass.md), `R45CritIntent` brace-prefix ({R45}/a3w1/R45CritIntent.md), the "
     f"routed ledger `python3 {L}/plans/routed_open.py --lane {L}` (if that is its CLI; read its docstring). For each: still "
     f"reproducible (command + output) / fixed / not reproducible, and whether this round's frozen claims touch it.",
     "VERDICT: routed-items-<n>-still-open-<k>"),
    ("R46ConnSibling", "connector", ["adjacency"],
     f"Sibling-overlap scan for this round's three surfaces: do sibling lanes under {F}/*-shokunin hold a fixture fence / sandbox "
     f"decision-procedure counter, an anchor-line or quote-location check over SOURCES rows, or a Terminal-Bench grader knowledge entry "
     f"(polyglot-c-py or dual-runtime)? Read-only greps over sibling repos (never write there). For each hit: path:line, same/adjacent/"
     f"different, and whether kengaku should report out, cite, or ignore.",
     "VERDICT: sibling-overlaps-<n>-report-outs-<k>"),
    ("R46ConnClaims", "connector", ["calibration", "depth", "coverage"],
     f"Cross-claim map for {CLAIMS}: which files each claim's work and counters touch, where C2 leg A and C3's rows interact, whether "
     f"C1's new counter shares code paths with C2/C3 tools, and the cross-claim patterns (all three are 'a gate that certified "
     f"something false' repairs?) worth one SKILL.md line. Flag any separability break with the concrete file.",
     "VERDICT: cross-claim-couplings-<n>-separability-breaks-<k>"),
    ("R46RevClaimsFile", "reviewer", ["calibration"],
     f"Review {CLAIMS} against the round contract ({F}/.ufo/prompts/kengaku-round-46.md §2, §6 item 9) and QUALITY Q30/Q31/Q37/Q39: "
     f"one predicate sentence per claim, identical in claims/counter/receipt label; do-nothing controls; no universal clauses the "
     f"counters do not enumerate; axis named by surface. Re-run the five C2 control receipts ({CL}/control-c2-*.txt) on fresh clones "
     f"and confirm byte-equal verdict lines.",
     "VERDICT: claims-file-defects-<n>-c2-controls-reproduced-<k>/5"),
]

FLASH = {"executor", "labrat", "scribe", "sonic", "simplifier", "revenger", "sentinel"}
ATTACK = {"reviewer", "critic", "mutation-tester", "labrat"}


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 46 wave-1 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r46 wave 1 (build, v1)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    c = Counter(i["role"] for i in items)
    attack = sum(n for r, n in c.items() if r in ATTACK)
    assert 32 <= len(items) <= 64, len(items)
    assert attack * 4 >= len(items), f"attack share {attack}/{len(items)} below a quarter"
    spec = {"wave": "kengaku-r46-w1",
            "milestone": "kengaku round 46 wave 1: C1 counter/modules/fence variants/sealed held-out, C2 rows+entry repair and "
                         "counter attacks, C3 polyglot-c-py package drafts + counter, frontier drafts",
            "reportDir": ".ufo/waves/round-46/w1", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    print(len(items), dict(c))
    print(f"attack={attack}/{len(items)}")


main()
