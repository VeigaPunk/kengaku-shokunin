#!/usr/bin/env python3
"""Renders .ufo/waves/round-37/falsify-spec.json (wave 2 of 2, policy v1): fresh seats attack what wave 1 and the
integration produced. Every item names what it attacks."""
import json
import pathlib
import sys
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-37"
B1 = f"{W}/build"
B = f"{W}/falsify"
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
BAT = f"{L}/plans/battery37"
ENTRY = f"{L}/corpus/knowledge/tb2-git-webserver-grader.md"
TIP = sys.argv[1] if len(sys.argv) > 1 else "<tip>"
CLONE = (f'Fixture rule: S={SCR}/<YourSeatName>; mkdir -p "$S"; trap \'rm -rf -- "$S"\' EXIT; export TMPDIR="$S"; '
         f'D="$S/fx"; git clone -q --no-local {L} "$D/lane"; git -C "$D/lane" checkout -q {TIP}; verify '
         f'`git -C "$D/lane" rev-parse --show-toplevel` equals "$D/lane" before any write; every git call names -C "$D/lane"; never commit '
         f'(index-only `git add` inside your clone is fine). Remove "$S" before you finish (copy receipts into your report dir first).')

CONTEXT = f"""# Goal
kengaku round 37 (hyaku run 8, 2026-10-26), WAVE 2 of 2 (falsify). Lane repo: {L}; integration tip {TIP} (pushed, branch master).
Frozen claims: {L}/plans/round-37-claims.md (freeze ca790460). Wave-1 reports: {B1}/*.md. You attack what wave 1 and the L1's integration
produced; every item names its target. A finding against the landing is a success of your seat, not a failure.
- C1 calibration: frozen counter {C1} (55 gate-silencing mutants M01-M55 against the unedited gate {GATE}); battery modules {BAT}/*.py
  (single-defect fixtures written in wave 1). Predicate: `python3 plans/round37_c1_verify.py --lane .` prints
  `BATTERY fixtures=<n> wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`,
  exit 0, on a clean clone of the tip. Receipt: {W}/integrate/measure-final.txt.
- C2 coverage: {ENTRY}, rows S111-S113 in {L}/corpus/SOURCES.md, README index row + coverage bullet, captures {CAP}/ (SHA256SUMS), probe
  {PROBE} (22 frozen cases), receipt {E37}/git-webserver-probe.txt. Predicate: `python3 plans/round37_c2_verify.py --lane .` prints
  `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0, on a clean clone of the tip.
- Frontier: plans/anchor_digest_check.py (S110 anchor digest erratum), corpus/lessons/round-37.md, QUALITY.md new criteria, SKILL.md,
  PROVINCE.md, SCORECARD.md, LOG.md round-37 sections.

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report dir is {B}/; drafts and receipts go under {B}/<YourSeatName>/ (create it). Never copy a corpus/ or plans/
  tree, a lane mirror, or a clone into {B}/.
- Scratch (operator directive 2026-10-25): clones, fixtures and work trees live ONLY under {SCR}/<YourSeatName>/ (NVMe), never under /tmp;
  pass it explicitly (export TMPDIR, --work); delete it before you finish.
- Write ONLY inside {B}/ and your scratch dir. NEVER edit any lane file (corpus/, plans/, SCORECARD.md, LOG.md, README.md, SKILL.md,
  PROVINCE.md, SHONEN.md ...). Never write into {F} (fleet root), sibling lanes, the lane's jj state, or the lane's Git index. Never run git
  add/commit/stash/checkout/reset/push/pull or any mutating jj command in the lane. Run counters on YOUR clone, not on the lane.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY: never write/commit/fetch there; run none of its campaign tools.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide: install via
  `uv tool` / `npx` / an official binary into ~/.local/bin. Never run pacman -Sy/-Syu/-U/-R, never name an already-installed package to
  pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task`.
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location and is <= 25 words. Do not
  fabricate output; if something cannot be fetched or run, say so.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""


def extra_mut(name, module, mids, clause):
    return (name, "critic", ["calibration"],
            f"Attack battery module {BAT}/{module}.py beyond the frozen mutants {mids} (clause {clause} of {GATE}): write 4 NEW non-frozen "
            f"mutants of the same clause that a correct battery should also catch (off-by-one thresholds, `>=`→`>`, a check applied to the "
            f"first row only, a branch reordered so a later check shadows it, a regex loosened), each as an exact `old -> new` pair that occurs "
            f"once in the gate. Run each against the full battery with a small harness under {B}/{name}/ that reuses the counter's machinery "
            f"(import {C1} as a module: load_r36, Ctx, r36_fixtures, battery37_fixtures, run_gate; build the fixtures once, run the reference "
            f"and each mutant). Report killed/survived per new mutant with the killing fixture. Survivors are limits of the battery (reported, "
            f"never repaired into the frozen claim). Also say whether each fixture of {module}.py isolates one defect as its docstring says.",
            f"VERDICT: extra-mutants-{module}-killed-<k>/4")


ITEMS = [
    # ---- re-measure (executors) ----
    ("F37C1Rerun", "executor", ["calibration"],
     f"Re-run C1 on a clean clone of {TIP}: `python3 plans/round37_c1_verify.py --lane .` (TMPDIR in your scratch). Paste the BATTERY and "
     f"MUTANTS lines, PREDICATE and exit; diff the full output against {W}/integrate/measure-final.txt (C1 part). Then `sha256sum "
     f"plans/pkg_gate.py` and compare with the frozen digest in {L}/plans/round-37-claims.md.",
     "VERDICT: c1-rerun-<pass|fail>-killed-<k>/55"),
    ("F37C1RerunPy313", "executor", ["calibration", "operability"],
     f"Re-run C1 on a clean clone of {TIP} under a different interpreter: `uv run --no-project -p 3.13 python3 plans/round37_c1_verify.py "
     f"--lane .` and `-p 3.12`; with PYTHONHASHSEED=1 and 99. Any difference in the BATTERY/MUTANTS lines is a determinism finding; name it.",
     "VERDICT: c1-rerun-interpreters-<same|diff>"),
    ("F37C2Rerun", "executor", ["coverage"],
     f"Re-run C2 on a clean clone of {TIP}: `python3 plans/round37_c2_verify.py --lane .`; paste all V lines and the gate lines; then re-run "
     f"the probe `python3 plans/git_webserver_probe.py --lane .` and cmp with the committed receipt; time both.",
     "VERDICT: c2-rerun-<pass|fail>-probe-byte-equal-<yes|no>"),
    ("F37NoHarmSweep", "executor", ["freshness", "operability"],
     f"No-harm sweep on a clean clone of {TIP}: run every gate/probe in the SKILL.md registry table (grep the table in {L}/SKILL.md) plus "
     f"`python3 grader.py`, `python3 grader.py --selftest`, `python3 plans/round36_c1_verify.py --lane .`, `python3 plans/round36_c2_verify.py "
     f"--lane .`, census `--file corpus/SOURCES.md`. Compare with the wave-1 pre-landing sweep {B1}/R37TipSweep.md: any command green before "
     f"and red now is a harm finding; name it.",
     "VERDICT: no-harm-<n_same>/<n>-new-red-<n>"),
    ("F37AnchorRerun", "executor", ["calibration"],
     f"Re-run `python3 plans/anchor_digest_check.py --lane .` on a clean clone of {TIP} and on a clean clone of 3ea9a1d9 (before) with the "
     f"tool copied in; paste both. Then 4 mutants in your clone: delete the Erratum (round 37) line; change one hex digit of its correct "
     f"digest; shorten S108's anchor digest; add a second sha256 token to S111's anchor. Report caught/missed.",
     "VERDICT: anchor-before-<n>-after-<n>-mutants-<caught>/4"),
    ("F37ProbeOnTip", "executor", ["coverage", "operability"],
     f"Run the gate exactly as V2 does on a clean clone of {TIP} (copy the template spec, set receipt_sha256 to the receipt's digest, `python3 "
     f"plans/pkg_gate.py package --root . --spec <yours> --rerun --require-clean-tree`) and under uv (the P10 path when Bio is missing). Then "
     f"run 3 adversarial probe environments: a host process already listening on 127.0.0.1:8080 OUTSIDE the sandbox in your scratch-only "
     f"network namespace (`unshare -rn`), HOME unset, and a PATH lacking bwrap — the probe must still be byte-equal or refuse with exit 2.",
     "VERDICT: probe-on-tip-<byte-equal|diff>-adversarial-<n_ok>/3"),
    # ---- battery attacks (critics, extra mutants) ----
    extra_mut("F37XMutP23", "p23", "M02-M08", "P2/P3"),
    extra_mut("F37XMutP4", "p4", "M09-M12", "P4"),
    extra_mut("F37XMutP5", "p5", "M13-M19", "P5"),
    extra_mut("F37XMutP6", "p6", "M20-M27", "P6"),
    extra_mut("F37XMutP7", "p7", "M28-M33", "P7"),
    extra_mut("F37XMutP8", "p8", "M34-M38", "P8"),
    extra_mut("F37XMutP910", "p910", "M39-M43", "P9/P10"),
    extra_mut("F37XMutD4", "d4", "M44-M47", "D4"),
    extra_mut("F37XMutD5", "d5", "M48-M55", "D5"),
    ("F37CritOverfit", "critic", ["calibration"],
     f"Attack the C1 measurement's meaning: write {B}/F37CritOverfit/overfit_gate.py, a gate that matches every battery declaration in "
     f"{BAT}/*.py and the round-36 battery (same exit code and DEFECT set on every fixture) while implementing as few real checks as "
     f"possible (keys on fixture properties). If such a gate exists cheaply, the battery's declarations do not pin the advertised classes. "
     f"Run it through the counter's reference path (import {C1}). Report the cues it needed.",
     "VERDICT: overfit-gate-<matches|fails>-cues-<n>"),
    ("F37CritRenamed", "critic", ["calibration"],
     f"Attack the renamed run in {C1}: does copying a fixture under another directory name actually test name-independence (fixture ids "
     f"never appear in paths; the gate sees only paths)? Find a way a gate could still key on a fixture (file names inside the fixture, "
     f"argv shapes, content markers like 'junk') and test whether the battery modules in {BAT} carry such cues. Propose a stronger "
     f"renaming (content-preserving) and say whether the round-37 battery would survive it.",
     "VERDICT: renamed-run-<adequate|weak>-cues-<n>"),
    ("F37CritC1Axis", "critic", ["calibration"],
     f"Attack C1's axis: the claim calls the 50→0 count a calibration mismatch (advertised-but-undemonstrated gate classes between "
     f"self-assessment — gate docstring, {L}/corpus/QUALITY.md Q24, SCORECARD capability row `package-gate` — and observed tests). Is that a "
     f"calibration move (addendum: a calibration claim counts mismatches between self-assessment and observed repo state) or "
     f"operability/test-coverage work? Check that every mutant label maps to an advertised sentence in those three self-assessment texts "
     f"(cite file:line per mutant group); mutants with no advertising sentence do not count as calibration mismatches.",
     "VERDICT: c1-axis-<calibration|other>-unadvertised-<n>"),
    ("F37CritC2Map", "critic", ["coverage"],
     f"Attack the entry's `## Requirement map` in {ENTRY} semantically (V7 checks only label/verdict consistency): is each instruction.md line "
     f"({CAP}/instruction.md) mapped to the right label, and does each cited case actually test that line (e.g. does `wrong-port-8081` test "
     f"line 7's port requirement or only 'nothing on :8080')? Give a per-row agree/disagree with reasons and exact wording fixes.",
     "VERDICT: req-map-<agree>/<rows>"),
    ("F37CritC2Overclaim", "critic", ["coverage", "adjacency"],
     f"Attack {ENTRY} for overclaims: task validity, agent behaviour, 'exploit' language beyond the receipt, statements about the real "
     f"container (the probe never ran it — unless {B1}/R37DockerOracle.md shows a real-image run; check what it actually showed), statements "
     f"about pytest equivalence. Every sentence that the receipt, the captures or a wave-1 report does not support: quote it and give the fix.",
     "VERDICT: overclaims-<n>"),
    ("F37CritNoHarmDiff", "critic", ["calibration"],
     f"No-harm audit by diff: `git -C {L} diff 3ea9a1d9 {TIP} --stat` and the full diff of SCORECARD.md, LOG.md, corpus/README.md, "
     f"corpus/QUALITY.md, SKILL.md, PROVINCE.md, corpus/SOURCES.md, corpus/knowledge/. Any removed or rewritten line (append-only rule), any "
     f"score raised without a counter, any axis stated harmed or silently lowered? Paste counts of +/- lines per file and every '-' line.",
     "VERDICT: no-harm-removed-lines-<n>"),
    ("F37CritCalibStatements", "critic", ["calibration"],
     f"Calibration audit of the round-37 self-assessment text at {TIP}: every number in the round-37 sections of SCORECARD.md and LOG.md, the "
     f"lesson corpus/lessons/round-37.md and the capability rows — re-derive each from committed bytes or receipts (cite the command). Count "
     f"mismatches; list each with the corrected value.",
     "VERDICT: statements-<n_checked>-mismatches-<n>"),
    ("F37MutAttribution", "mutation-tester", ["calibration"],
     f"Attack the post-hoc audit {L}/plans/round37_c1_attribution.py (not the frozen rule; receipts {W}/integrate/c1-attribution.txt "
     f"`ATTRIBUTED 55/55` and c1-attribution-hostile.txt `6/55`). In your clone: (a) 4 code mutants of the audit (drop the family check; "
     f"drop the declared-defects check; accept rc not in 0/1; drop the 'clause in reference DEFECT set' check) — run each against the landed "
     f"battery and against the hostile side-channel battery in {B1}/R37CritC1Battery/sidechannel/ (copy into your clone's plans/battery37/); "
     f"report which mutants the hostile battery exposes; (b) design one hostile fixture that the audit would still attribute wrongly, if any.",
     "VERDICT: attribution-mutants-<caught>/4-residual-<n>"),
    # ---- reviewers ----
    ("F37ReopenRows", "reviewer", ["coverage", "freshness"],
     f"Re-open S111-S113 live at {RAWRL}/(tests/test_outputs.py, tests/verify.sh, instruction.md): sha256 vs the row anchors and {CAP}/SHA256SUMS; "
     f"each row's located quote verbatim at its stated line (sed -n); <=25 words; tier/kind/scope sensible; teaches grounded. Also check the "
     f"lesson's ## Gate quotes for the three rows.",
     "VERDICT: rows-<n_ok>/3-quotes-<n_ok>/<n>"),
    ("F37RevEntryQuotes", "reviewer", ["coverage", "depth"],
     f"Re-verify every `## Located quotes` row of {ENTRY} against the captures (sed -n per row) and every claim sentence in the entry against "
     f"the receipt {E37}/git-webserver-probe.txt and {CAP}/verify.sh line numbers. Flag each quote whose claim cell says more than the quote.",
     "VERDICT: entry-quotes-<n_ok>/<n>-claims-<n_unsupported>"),
    ("F37RevBatteryCode", "reviewer", ["calibration", "operability"],
     f"Code review of every module in {BAT}: fixture isolation (one branch per fixture as declared), no reliance on lane working-tree state "
     f"beyond ctx helpers, scratch hygiene (nothing outside d), determinism (no time/random), no `--spec`, no network. Cite file:line.",
     "VERDICT: battery-code-<n>-defects"),
    ("F37RevLesson", "reviewer", ["calibration"],
     f"Review {L}/corpus/lessons/round-37.md: Gate rows (≥1 admit, ≥1 reject, quotes located), Mistakes rows (class · evidence pointer · "
     f"captured-by · fix, and each fix shown able to fail with a pointer), Census before/after, Spot-check list. Every pointer resolves?",
     "VERDICT: lesson-<n>-defects"),
    ("F37RevQuality", "reviewer", ["calibration"],
     f"Review the new {L}/corpus/QUALITY.md criteria added this round: each cites the lesson that produced it, names what it supersedes, is "
     f"testable, and its Limits are honest. Does any criterion overstate what the round-37 tools check?",
     "VERDICT: quality-<n>-defects"),
    ("F37RevSkillReadme", "reviewer", ["operability", "coverage"],
     f"Review round-37 additions to {L}/SKILL.md (registry rows: commands exist and run as written; exit maps true) and {L}/corpus/README.md "
     f"(index row, coverage bullet, evidence listing; knowledge files == index rows). Run each registry command once on your clone.",
     "VERDICT: skill-readme-<n>-defects"),
    ("F37RevScorecardLog", "reviewer", ["calibration"],
     f"Review the round-37 SCORECARD.md section and LOG.md entry at {TIP}: counting commands verbatim from the claims file; before/after values "
     f"equal the committed receipts ({W}/claims/, {W}/integrate/); capability rows carry a demonstration command; no score raised beyond the "
     f"rubric; coverage cap stated.",
     "VERDICT: scorecard-log-<n>-defects"),
    ("F37RevProvinceErrata", "reviewer", ["adjacency", "calibration"],
     f"Review the round-37 PROVINCE.md paragraph and every append-only erratum landed this round (regex-log entry errata, S110 anchor erratum, "
     f"round-36 lesson line drift): each verified against the bytes it corrects (sed -n), nothing rewritten in place.",
     "VERDICT: province-errata-<n>-defects"),
    # ---- mutation-testers ----
    ("F37MutC2Counter", "mutation-tester", ["calibration"],
     f"Mutation-test the C2 counter on the LANDED package in your clone of {TIP}: 10 single mutants (one quote off by a line; S112 anchor "
     f"digest 63 hex; requirement-map row relabelled; map row citing an unknown case; receipt CASE line removed; receipt one byte; a "
     f"`match=NO` not named; SHA256SUMS line removed; README bullet removed; extra knowledge file). Each must turn the counter red; paste the "
     f"DEFECT line per mutant.",
     "VERDICT: c2-landed-mutants-<caught>/10"),
    ("F37MutAnchorTool", "mutation-tester", ["calibration"],
     f"Mutation-test {L}/plans/anchor_digest_check.py itself: 5 code mutants (drop the 64-length check; accept uppercase; skip indented rows; "
     f"accept the erratum without checking the correct digest is in a manifest; search only the round36 dir) — run each against the lane "
     f"state of 3ea9a1d9 (must flag S110) and of {TIP}; report which mutants the tool's own selftest (if any) or the before/after pair catches.",
     "VERDICT: anchor-tool-mutants-<caught>/5"),
    ("F37MutProbeCases", "mutation-tester", ["coverage", "calibration"],
     f"Mutation-test the receipt's discriminating power: in copies of {PROBE} (scratch only), change single server behaviours (e.g. "
     f"`token-in-body` body to 'TEST PASSE', `status-then-content-split` order swapped, `slow-server-3s` delay 0) and check the receipt changes "
     f"exactly where the prediction says it should; a case whose verdict does not depend on its distinguishing feature is not independent "
     f"evidence.",
     "VERDICT: probe-case-mutants-<as-predicted>/<n>"),
    # ---- scouts / connectors ----
    ("F37ScoutMisroot", "scout", ["calibration"],
     f"Hygiene sweep (read-only): `git -C {F} status --porcelain` — list every untracked fleet-root file whose content names kengaku round 37 "
     f"(misroot candidates); list leftovers under {SCR}/ and under /tmp named k37-*/cgw-*; `git -C {L} status --porcelain` at the time you "
     f"run. Report paths only; delete nothing.",
     "VERDICT: misroot-<n>-scratch-leftovers-<n>"),
    ("F37ConnCrossCheck", "connector", ["calibration", "coverage"],
     f"Cross-check across artefacts: the lesson's Mistakes → QUALITY criteria (each criterion has a lesson row and vice versa); the claims' "
     f"limits → the report-facing SCORECARD text (no limit dropped); wave-1 findings in {B1}/*.md with VERDICTs naming defects → each "
     f"either fixed at {TIP}, recorded as a limit, or left unaddressed (list the unaddressed ones).",
     "VERDICT: crosscheck-unaddressed-<n>"),
    ("F37ConnSiblingCite", "connector", ["adjacency"],
     f"Given {B1}/R37ConnSibling.md and the landed PROVINCE.md round-37 paragraph: is every adjacent sibling named with file:line, any contested "
     f"scope reported rather than absorbed, and would any sibling's instrument (mutation harness, sandbox, TB2 audits) have been cited? "
     f"Read-only.",
     "VERDICT: sibling-cite-<n>-gaps"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 37 wave 2 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r37 wave 2 (falsify)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    spec = {"wave": "kengaku-r37-falsify",
            "milestone": "kengaku round 37 wave 2: falsify C1 battery, C2 package, frontier and docs",
            "reportDir": ".ufo/waves/round-37/falsify", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/falsify-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"]
    print(len(items), dict(c), f"attack={attack} flash={flash}")


main()
