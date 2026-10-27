#!/usr/bin/env python3
"""Renders .ufo/waves/round-45/w2-spec.json (v1 wave 2 — falsify, policy v1 band 32-64). L1 KengakuR45(-2).

Dispatched only after wave 1 lands: attack seats attack THE LANDED `plans/fixture_fence.py` with held-out hostile
modules, the landed C2 package and receipt, and every new artifact wave 1 produced. Items are authored against the
freeze; seat prompts name the landed tree explicitly."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-45"
B = f"{W}/w2"
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
SPEC = f"{L}/plans/pkg-spec-r45.json"
CLAIMS = f"{L}/plans/round-45-claims.md"
CL = f"{W}/claims"
ENV = f"{CL}/envelope.sh"
FREEZE = "52d7486a8caf930855cd1f748032ac21648303f5"
ENTRY = f"{L}/corpus/knowledge/tb2-{TASK}-grader.md"
FENCE = f"{L}/plans/fixture_fence.py"
W1 = f"{W}/w1"

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
kengaku round 45 (hyaku run 9, 2026-10-26), wave 2 of two v1 waves (FALSIFY). Lane repo: {L}.
Wave 1 built and the L1 integrated: `plans/fixture_fence.py` exists at the lane tip; the C2 package ({ENTRY},
SOURCES rows S149-S156, README/PROVINCE edits, receipt {RCPT}) exists at the lane tip. The claims {CLAIMS} and
the counters {C1} / {C2} are FROZEN ({FREEZE}) — nothing frozen may change. Your job is to attack what wave 1
produced and what the L1 integrated: every verdict you return needs the measured command and its output, and
every hostile module you write goes in YOUR subdir {B}/<YourSeatName>/ (never the lane).
- C1's claim is `PREDICATE C1 pass` on a clean clone: `REFUSALS total=10 clean=10`, `HONEST fixtures=104
  admitted=104`, `CALIBRATION advertised=10 contradicted=0`. Attack surface: {FENCE} (read it first), the ten
  `plans/refusals45/` modules, the strace open-region rule, and the 104-fixture honest set.
- C2's claim is `PREDICATE C2 pass`: `checks=11 defects=0`. Attack surface: the receipt, the entry's five
  gated sections, the nine SOURCES rows, the predictor block, the probe's recipe fidelity to setup.sh.
- Frontier artifacts under attack too: {L}/corpus/lessons/round-45.md (Gate admits/rejects, Mistakes rows),
  the SCORECARD round-45 block, LOG.md round-45 entry, {L}/corpus/README.md index/frontier lines,
  {L}/PROVINCE.md paragraph.

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
  SCORECARD.md, LOG.md, README.md, SKILL.md, PROVINCE.md, SHONEN.md or any other lane file — report findings for the L1.
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

HOSTILE_NOTE = (
    f"A held-out hostile module is one Python file in the SAME contract as {L}/plans/refusals45/f7_commondir.py (read two "
    f"of them and {C1}'s `build_module`): module-level `FIXTURES = [{{'fid','tool','expect','defects','build'}}]`; "
    f"`build(ctx, d)` fills empty dir d and returns the argv tail; ctx.init/ctx.git/ctx.write/ctx.sh confine paths to d "
    f"except the deliberate outside artefact your class needs (write it under `pathlib.Path(d).parent`, which is still "
    f"the module's build root). Put the file in YOUR subdir; test it against THE LANDED {FENCE} via "
    f"`python3 {C1} --lane \"$S/lane\" --work \"$S/w\"` after copying {FENCE} into your clone (dev: point "
    f"REFUSAL_REL at a scratch dir? — no: copy YOUR module into \"$S/lane/plans/refusals45_dev/\" is NOT read; the "
    f"counter reads {L}/plans/refusals45 only. Instead run the fence directly: import your module, call "
    f"`build_module` machinery from {K44} as {C1} does, then call `breach(d, argv, tool)` yourself under strace and "
    f"report the verdict + outside opens). A held-out module wins only if the landed fence ADMITS it or READS outside "
    f"d; a refused module that was read still counts as a fence defect.")


def it(name, role, axes, task, verdict):
    return (name, role, axes, task, verdict)


ITEMS = [
    # ---- held-out hostile authors (wave-1 R45SentFenceDesign enumerated the vector space) ----
    ("R45HoIncludeIf", "mutation-tester", ["calibration"], HOSTILE_NOTE +
     f" Your class: `[includeIf]` variants — `gitdir:` matching the fixture path (glob and exact), `onbranch:`, "
     f"case tricks (`[IncludeIf]`), and an include whose file is a SYMLINK outside d. R45SentFenceDesign's wave-1 "
     f"report ({W1}/R45SentFenceDesign.md) may name more; use it.",
     "VERDICT: includeif-modules-<n>-admitted-<k>-read-<r>"),
    ("R45HoCommondir2", "mutation-tester", ["calibration"], HOSTILE_NOTE +
     " Your class: commondir RELATIVE path (resolved against the gitdir, escaping d via `..`), a `.git` FILE whose "
     "`gitdir:` line is relative/space-padded, and a `worktrees/<id>/` linked-worktree metadata dir pointing outside.",
     "VERDICT: commondir2-modules-<n>-admitted-<k>-read-<r>"),
    ("R45HoConfigKeys", "mutation-tester", ["calibration"], HOSTILE_NOTE +
     " Your class: config keys that name files outside d without an include: `core.attributesFile`, `core.hooksPath`, "
     "`core.fsmonitor`, `mailmap.file`, `core.worktree` RELATIVE (r44 f2 was absolute), `user.useConfigOnly`, "
     "credential/gpg helper keys — the fence's job is only to refuse paths it cannot verify inside d or to prove "
     "each key inert; measure which the landed fence misses and which the TOOL would honour.",
     "VERDICT: configkey-modules-<n>-admitted-<k>-read-<r>"),
    ("R45HoSymlinks", "mutation-tester", ["calibration"], HOSTILE_NOTE +
     " Your class: symlink and hardlink tricks — `.git` a symlink into a real repo inside d (resolves inside: "
     "honest-shaped but delegates?), `.git/objects` a symlink outside, a claims path that is a symlink to a blob "
     "outside, hardlinked objects to an outside store, `.git` itself a hardlink trick, an include target reached "
     "through a symlink chain inside d.",
     "VERDICT: link-modules-<n>-admitted-<k>-read-<r>"),
    ("R45HoArgvEnv", "mutation-tester", ["calibration"], HOSTILE_NOTE +
     " Your class: argv and environment vectors — `--lane` naming a path with `..`, a trailing-slash or `.` "
     "segment that dodges the inside-d compare, a claims/receipt arg that is a symlinked path, argv with extra "
     "value tokens, and (if the harness preserves env) GIT_DIR/GIT_WORK_TREE style tricks the fence must not "
     "inherit — check {C1}'s PIN_CHECK_ENV first.",
     "VERDICT: argvenv-modules-<n>-admitted-<k>-read-<r>"),
    # ---- direct counter/measure attacks ----
    ("R45CritLandedFence", "critic", ["calibration"],
     f"{HOST_RULE}\n\nFalsify the LANDED {FENCE} end to end: run {C1} in your clone (`--work \"$S/w\"`, envelope) "
     f"and paste the receipt; then read the fence source for (a) classes f1-f10 handled by name rather than by "
     f"mechanism (string-match on module artefacts vs the real git semantics), (b) unbounded walks or races, (c) "
     f"git calls without ceiling/timeout/stdin, (d) leg order that lets a git call precede the static scan, (e) "
     f"`is_relative_to` misuse on unresolved paths, (f) a fixture that makes `clean` while the vulnerability "
     f"stands — write it (HOSTILE module contract below) and demonstrate. {HOSTILE_NOTE}",
     "VERDICT: landed-fence-defects-<n>-demonstrated-<k>"),
    ("R45CritIntent", "critic", ["calibration"],
     f"Intent audit of the landed {FENCE}: does it (a) read fixture ids or module filenames to decide, (b) "
     f"hardcode the 10 fids or the 104 honest fixture shapes, (c) special-case `--lane` strings, (d) rely on "
     f"timing the counter tolerates. Read the source end to end; demonstrate any finding by renaming fids and "
     f"showing a verdict change. Also: is `breach()` pure (same input twice -> same answer)?",
     "VERDICT: fence-intent-clean-<yes|no>-findings-<n>"),
    ("R45MutLandedFence", "mutation-tester", ["calibration"],
     f"{HOST_RULE}\n\nMutation-test the LANDED {FENCE}: generate >=12 single-edit mutants (flip a comparison, "
     f"drop a leg, swap return, widen a regex, remove a ceiling, drop a resolve()) and for each run {C1} in a "
     f"clone. A mutant is caught iff a refusal module flips from clean to leaked/read or an honest fixture is "
     f"refused. Table mutant -> caught-by (module or honest set); a survivor means the frozen instrument has a "
     f"hole — name the missing hostile class.",
     "VERDICT: fence-mutants-caught-<k>/<n>"),
    ("R45RevC1Receipt", "reviewer", ["calibration"],
     f"{HOST_RULE}\n\nIndependently re-derive the C1 receipt on a clean `--shared` clone of the lane tip: run "
     f"{C1} end to end inside the envelope (paste every line), then re-verify ONE refused module and ONE honest "
     f"module by hand under your own strace (not the counter's): does the strace evidence support `clean` and "
     f"`admitted opens=0`.",
     "VERDICT: c1-receipt-reproduced-<yes|no>-handchecked-2"),
    ("R45LabratReadProof", "executor", ["calibration"],
     f"{HOST_RULE}\n\nProve or refute that the landed {FENCE}'s own decision path performs ZERO opens outside d on "
     f"f1, f4, f6, f10 (the r44 READ modules) AND admits honest fixtures without reading their siblings: strace "
     f"each under the counter's own harness (set K45_KEEP_STRACE to keep logs), cite the log lines. Also test a "
     f"pathological tree (a fixture with 100k empty files) against the walk bound and FENCE_TIMEOUT.",
     "VERDICT: read-proof-<4|k>-honest-clean-<yes|no>"),
    ("R45MutC1Instrument2", "mutation-tester", ["calibration"],
     f"{HOST_RULE}\n\nSecond mutation pass on {C1}, different surface than wave-1 R45MutParser: the REFUSALS "
     f"roll-up (per-module verdict choice order: what if a module both leaks AND reads), build_errors counting, "
     f"the `dev`/`--battery-dir` escape hatches (can a dev flag make the predicate print `pass` on a broken "
     f"lane?), PINS enforcement (drop a module file: does mismatched rise), `HONEST fixtures=` vs `admitted=` "
     f"accounting. Mutate, run the r44-fence control + admit_all stub, table caught/survived.",
     "VERDICT: instrument2-mutants-caught-<k>/<n>"),
    # ---- C2 falsification ----
    ("R45CritReceipt", "critic", ["coverage"],
     f"{HOST_RULE}\n\nRe-derive the receipt {RCPT}: run {PROBE} fresh in a clone (`--work \"$S/w\"`, envelope) and "
     f"diff every CASE line against the landed receipt; then run the same receipt THROUGH `regrade` mentally — "
     f"pick 3 cases, rebuild their end states by hand from setup.sh + the recipe, run the captured grader "
     f"yourself in bwrap, and compare verdicts. Any mismatch between the landed receipt and your independent "
     f"grade is a defect.",
     "VERDICT: receipt-rerun-mismatches-<n>-handcheck-<k>/3"),
    ("R45CritV11Bypass", "critic", ["coverage"],
     f"{HOST_RULE}\n\nAttack V11 as hardened in {C2}: write predictors that pass `disagree=0` without performing "
     f"the membership reading — a 48-bit truth table open-coded to dodge the lint (bitwise ops on an int "
     f"literal, chr() joins, arithmetic decoys), a predictor that returns the GRADER's output by replaying "
     f"its logic from the file the counter itself binds, a timing/purity exploit (predict() that detects the "
     f"count-only harness). Run each through the counter's v11() on a mirror (see {CL}/c2_predictor_control.py "
     f"for the harness shape). Verdict-changing = a table passes disagree=0.",
     "VERDICT: v11-bypasses-<n>-verdict-changing-<k>"),
    ("R45MutC2Checks", "mutation-tester", ["coverage"],
     f"{HOST_RULE}\n\nMutation-test {C2} checks V1-V10 on the LANDED package: remove a row's sha256 from its "
     f"anchor cell, swap a quote for a paraphrase, drop a requirement-map row, rename a case in the case table, "
     f"point a mechanism row at line+1 — each on a scratch copy of the package; the counter must say DEFECT on "
     f"the right V. Table mutation -> caught V -> expected V.",
     "VERDICT: c2-mutations-caught-<k>/<n>"),
    ("R45RevEntryQuotes", "reviewer", ["coverage"],
     f"Re-open every `## Located quotes` row of {ENTRY}: byte-compare each quote with the cited capture line "
     f"(report line-by-line OK/drift and sha256 of the capture); check each `## Mechanism` quote is verbatim on "
     f"its cited line; verify every S149-S156 id in the entry's `source:` line and body matches the spec "
     f"{SPEC} rows map; check the `## Predictor` block is exactly the rule the grader executes (line "
     f"membership after strip/split; does its CRLF handling match read_text's universal newlines — build a "
     f"counterexample state if it differs).",
     "VERDICT: entry-quotes-<n>/n-mechanism-<m>/16-predictor-<ok|mismatch>"),
    ("R45RevRowCells", "reviewer", ["coverage"],
     f"Verify each SOURCES row S149-S156 in {L}/corpus/SOURCES.md: its sha256 equals the capture, the quote is "
     f"verbatim at the cited line, `used-by` names only the admitted entry, the URL resolves at the pin (refetch "
     f"HEAD one), tier/status/scope cells match the registry's conventions (compare S138-S146). Check the census: "
     f"{F}/scripts/sources-census.sh validate --root {F} kengaku exit 0. Also the gitignore rejection: does the "
     f"lesson record it correctly (reason + flip).",
     "VERDICT: rows-verified-<n>/8-census-<ok|fail>-defects-<k>"),
    ("R45LabratRefetch", "executor", ["freshness"],
     f"{HOST_RULE}\n\nRefetch all nine pinned files at {RAW}/ plus the upstream .gitignore (the rejected row "
     f"candidate) into scratch, sha256-compare with {CAP}/ (byte-identical expected), and check whether upstream "
     f"HEAD moved the task since {PIN} (fetch the tree at HEAD for the task dir; list any differing file). Paste "
     f"commands + digests.",
     "VERDICT: refetch-identical-<n>/9-drift-<none|named>"),
    ("R45CritCaseFidelity", "critic", ["coverage"],
     f"{HOST_RULE}\n\nAttack the probe's recipe fidelity: read each of the 16 case recipes in {PROBE} and the "
     f"frozen `violates=` tags in {DRY}: (a) does any recipe fail to build the end state it claims (compare with "
     f"setup.sh's actual image seed); (b) is any tag wrong (a case tagged `violates=X` that does not in fact "
     f"violate X, or an untagged violation that changes a requirement-map label); (c) is `dir-state`'s read "
     f"really IsADirectoryError on this kernel. Demonstrate each finding against the receipt.",
     "VERDICT: case-fidelity-defects-<n>-label-changing-<k>"),
    ("R45SentC2Grader", "sentinel", ["coverage", "safety"],
     f"{HOST_RULE}\n\nSafety check of the C2 package path: does anything in the probe, gate or counter execute "
     f"upstream code on the HOST outside bwrap (solve.sh, setup.sh, the grader module)? Trace every subprocess "
     f"call in {PROBE}, {C2} and {L}/plans/pkg_gate.py and mark which sandbox each runs in; check "
     f"{CAP}/environment/setup.sh for a payload the sandbox does not contain (curl, rm outside /app, setuid).",
     "VERDICT: c2-unsafe-execs-<n>"),
    ("R45CritDryVsObserved", "critic", ["coverage"],
     f"Check every frozen prediction in {DRY} against the landed receipt {RCPT} case by case: `predicted=` vs "
     f"observed letter and pass/fail, and whether the frozen `violates=` sets still stand under the observed "
     f"outcome (a case that passed for a reason its tag set did not foresee changes a requirement-map label). "
     f"List disagreements.",
     "VERDICT: dry-vs-observed-mismatches-<n>"),
    # ---- integration, docs, frontier ----
    ("R45RevLesson", "reviewer", ["discernment"],
     f"Review {L}/corpus/lessons/round-45.md line by line: every Gate admit row's quote verified against the "
     f"cited capture (path:line + sha256), the reject's reason and flip, every Mistakes row's evidence pointer "
     f"resolvable (open each), and its `captured-by` honest (a criterion that exists vs `none`). Check the "
     f"attempt-1 do-nothing row really cites the discarded draft at {W}/attempt1-unclaimed/.",
     "VERDICT: lesson-defects-<n>"),
    ("R45RevScorecard", "reviewer", ["calibration"],
     f"Re-derive the SCORECARD round-45 block from committed bytes: rerun the counting commands it records for "
     f"C1 and C2 on the lane tip, check the row ids and deltas match, check the capability row's `First-working "
     f"round` and evidence lines resolve; also that `### Planned (round 46)` carries what R45PlanNext priced. "
     f"Compare with the round-44 section's conventions.",
     "VERDICT: scorecard-defects-<n>"),
    ("R45ExecNoHarm", "executor", ["operability"],
     f"{HOST_RULE}\n\nPost-landing no-harm measure on a clean clone of the lane TIP: round-44 counters "
     f"`{L}/plans/round44_c1_verify.py` and `round44_c2_verify.py` (expected pass), `anchor_digest_check.py` "
     f"(defects=0), `order_check.py`, `gate_flip_check.py`, census exit 0, frozen digests r39-r45 OK, "
     f"routed_open count vs baseline ({W1}/R45NoHarmBaseline/measure-baseline.txt), older probes byte-equal "
     f"where cheap. Output to your subdir as measure-final.txt; list every line that differs from baseline.",
     "VERDICT: no-harm-regressions-<n>"),
    ("R45CritC1Overclaim", "critic", ["calibration"],
     f"Read {CLAIMS} C1 wording against what the counter actually proves: does `clean=10` + `admitted=104` "
     f"support 'the fence does what the advertisement says' for ALL hostile classes (no — only the frozen 10 + "
     f"held-out found); does the claim overclaim by implying the round-44 counter is repaired (it is not — the "
     f"fence is a separate file the r44 counter never imports); is the strace region `(fx,btmp)` the right "
     f"definition of 'outside d' for a builder that could also write into root/mods. Report each over/underclaim "
     f"as a routed-line draft.",
     "VERDICT: c1-overclaims-<n>"),
    ("R45CritC2Overclaim", "critic", ["coverage"],
     f"Read {CLAIMS} C2 wording against the landed package: 'eleventh grader class exemplar' — is the "
     f"membership-of-one-constant class genuinely distinct from feal-linear's 100-substring class or a trivial "
     f"variant (is that a fair frontier move at all); is `allow_internet = true` on this task a material fact "
     f"the entry must disclose (the grader could be avoided by fetching the answer); does 'tier A' fit (host "
     f"execution + captures + probe)? Draft each correction the entry needs.",
     "VERDICT: c2-overclaims-<n>"),
    ("R45RevWave1Reports", "reviewer", ["quality"],
     f"Cross-read every {W1}/*.md report: check each verdict line against its pasted evidence (spot-check >=10 "
     f"claims at random — rerun the command in scratch where cheap); list reports whose verdict exceeds the "
     f"evidence, seats that filed no report, and any seat that claims a lane write (there must be none).",
     "VERDICT: w1-verdict-overshoots-<n>-reportless-<k>"),
    ("R45MutV11Lint", "mutation-tester", ["coverage"],
     f"{HOST_RULE}\n\nMutation-test V11's lint ({C2} lint_block + PRED_LINT_TOKENS): remove tokens one at a time "
     f"in a scratch copy and see which predictor classes sneak in; also evade the CURRENT lint with tokens not "
     f"in the ban list (dict literal via `dict(zip(...))` needs parentheses only? — `dict` is not banned; `zip` not "
     f"banned; a brace literal IS banned) and demonstrate a passing table if one exists. Table evasion -> passes-lint? -> "
     f"disagree.",
     "VERDICT: v11-lint-evasions-<n>-passing-<k>"),
    ("R45CriticMistakes", "critic", ["discernment"],
     f"Falsify the mined-mistake rows in {L}/corpus/lessons/round-45.md: is 'attempt-1 do-nothing C1' really a "
     f"mistake class the frozen controls catch (r44 standing-battery rule — but the discarded draft ALSO lacked "
     f"a standing-battery check; cite the draft's predicate); is 'a fix counts only once shown able to fail' "
     f"met by each fix named; is there a fourth mistake the round made that is not recorded (review the freeze "
     f"diff {FREEZE} vs baseline).",
     "VERDICT: mistake-rows-valid-<n>-missing-<k>"),
    ("R45RevReadmeFrontier", "reviewer", ["coverage"],
     f"Verify {L}/corpus/README.md landed edits: the index row for the new entry matches its convention and "
     f"target path exists; the §Frontier TB2 clause now reads 11 of 89 with the task named; knowledge count "
     f"cells agree with `find {L}/corpus/knowledge -name '*.md' | wc -l`; no older line was clobbered (diff "
     f"against baseline commit).",
     "VERDICT: readme-defects-<n>"),
    ("R45RevProvince", "reviewer", ["adjacency"],
     f"Verify the landed {L}/PROVINCE.md paragraph: cryptanalysis/file-recovery ownership consistent with "
     f"precedent paragraphs, sibling disclaimers still accurate (check {F}/<sibling>-shokunin/PROVINCE.md for "
     f"the named siblings), and that the paragraph doesn't overclaim the new class into siblings' ground "
     f"(R45ConnSibling's wave-1 output).",
     "VERDICT: province-defects-<n>"),
    ("R45ExecCensusPost", "executor", ["coverage"],
     f"{HOST_RULE}\n\nPost-landing census + row-count delta: `{F}/scripts/sources-census.sh validate --root {F} "
     f"kengaku` on the lane tip (exit, tail), `grep -cE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' "
     f"{L}/corpus/SOURCES.md` (expect 149), `find {L}/corpus/knowledge -name '*.md' | wc -l` (expect 52), "
     f"duplicate-id check per the round prompt's pattern. Paste all outputs to your subdir census-final.txt.",
     "VERDICT: census-final-ok-<yes|no>-rows-<n>"),
    ("R45CritAssimilation", "critic", ["coverage"],
     f"Re-check wave-1's R45MergeRescreen: rerun its collision command yourself (the 0-3-space pattern), "
     f"re-derive the quarantine slice awk, and hand-check ONE MORE quarantine row's cited source (fetch + locate "
     f"the quote). If its reg/staged counts drifted from what it reported, say which is right.",
     "VERDICT: rescreen-confirmed-<yes|no>-row-verdict-<v>"),
    ("R45SimplifierFence", "simplifier", ["operability"],
     f"Review the landed {FENCE} for dead code / over-general machinery vs the frozen predicate (functions never "
     f"reached, parameters ignored, a second fence API unused); keep behaviour identical — report a paste-ready "
     f"minimal diff in your subdir, never edit the lane.",
     "VERDICT: fence-simplifications-<n>"),
    ("R45ConnFrontiers", "connector", ["coverage"],
     f"Pattern-join the round: does the landed package + fence suggest a recurring gate class worth a QUALITY "
     f"criterion (e.g. 'fixture containment must be proven before any git call' or 'predictor legs must be "
     f"non-memorizable + lint-bounded')? Compare {L}/corpus/QUALITY.md Q29-Q38 for overlap and draft the "
     f"Q-numbered criterion text (max 2) with red/green evidence from this round.",
     "VERDICT: criteria-drafted-<n>-overlaps-<k>"),
    ("R45SentSeatAudit", "sentinel", ["safety"],
     f"Audit the round's seat hygiene: grep {W1}/*/ for any seat writing outside its subdir (lane tree, fleet "
     f"root, ~/.local/bin, /tmp receipts), any seat that ran jj/git mutations, and any committed lane file whose "
     f"hash differs from the freeze inputs unexpectedly (`git -C {L} diff {FREEZE} --name-only` vs the expected "
     f"claim surfaces). Fleet-root misroot check: `git -C {F} status --porcelain` for kengaku-named untracked "
     f"files.",
     "VERDICT: hygiene-violations-<n>-misroot-<k>"),
    ("R45MutHostileFixtures", "mutation-tester", ["calibration"],
     f"{HOST_RULE}\n\nWeaken each of the 10 `plans/refusals45/` modules one at a time (remove the hostile line, "
     f"make the outside path inside-d, strip the include) so each becomes honest-shaped; run the landed fence "
     f"over each in scratch and confirm it then ADMITS (a fixture that still fails means the fence refuses the "
     f"honest residue — over-refusal, a HONEST-leg failure mode). Table module -> admits-after-neutralization.",
     "VERDICT: neutralized-admitted-<n>/10"),
    ("R45CritFrozenDigest", "critic", ["calibration"],
     f"Audit every frozen digest vs the live lane: `{CL}/frozen-digests.txt` and the PINS of {C1}/{C2} — "
     f"recompute all; check no pinned file changed post-freeze (`git -C {L} diff {FREEZE} --` the pinned "
     f"paths); check the r44 PINS the instrument inherits ({K44} digest) still hold on the tip.",
     "VERDICT: digest-drift-<n>"),
    ("R45RevDispatch", "reviewer", ["operability"],
     f"Wave bookkeeping for the report: from {W1}/swarm-registry.json, {W}/w1-results.json and this wave's "
     f"dispatch, compute seats spawned, seats settled, seats with a report file vs results-only, dead seats and "
     f"their last error text, role mix vs the routing note; also verify no seat ran `model` overrides. Output a "
     f"paste-ready table for the report's round-shape paragraph.",
     "VERDICT: wave-table-ready-seats-<n>"),
    ("R45ExecTipRerun", "executor", ["calibration", "coverage"],
     f"{HOST_RULE}\n\nFinal re-measure on a clean `--no-local` clone of the lane TIP (the exact claim surface): "
     f"`python3 {C1} --lane <clone> --work \"$S/w\"` and `python3 {C2} --lane <clone> --work \"$S/w2\"` inside "
     f"the envelope; paste complete outputs to your subdir (c1-tip.txt, c2-tip.txt) — these are the report's "
     f"after-measurement receipts if green.",
     "VERDICT: tip-c1-<pass|fail>-c2-<pass|fail>"),
]

FLASH = {"executor", "labrat", "scribe", "sonic", "simplifier", "revenger", "sentinel"}
ATTACK = {"reviewer", "critic", "mutation-tester", "labrat"}


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 45 wave-2 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r45 wave 2 (falsify, v1)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    c = Counter(i["role"] for i in items)
    flash = sum(n for r, n in c.items() if r in FLASH)
    attack = sum(n for r, n in c.items() if r in ATTACK)
    assert 32 <= len(items) <= 64, len(items)
    assert attack * 4 >= len(items), f"attack share {attack}/{len(items)} below a quarter"
    spec = {"wave": "kengaku-r45-w2",
            "milestone": "kengaku round 45 wave 2 (falsify): held-out hostile modules vs landed fixture_fence, "
                         "landed C2 package + receipt attacks, instrument mutations, lesson/scorecard audit",
            "reportDir": ".ufo/waves/round-45/w2", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/w2-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    print(len(items), dict(c))
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
