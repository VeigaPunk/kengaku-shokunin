#!/usr/bin/env python3
"""Renders .ufo/waves/round-43/falsify-spec.json (wave 2 of 2, policy v1). L1 KengakuR43.

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

import subprocess
FX = f"{W}/falsify"
BAT = f"{L}/plans/battery43"
ENTRY = f"{L}/corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md"
ENTRY42 = f"{L}/corpus/knowledge/tb2-circuit-fibsqrt-grader.md"
LESSON = f"{L}/corpus/lessons/round-43.md"
LAND = open(f"{W}/integrate/LANDING").read().split()[0]
DOCS = open(f"{W}/integrate/DOCS").read().split()[0]

CONTEXT = f"""# Goal
kengaku round 43 (hyaku run 9, 2026-10-26), WAVE 2 of 2 (FALSIFY). Lane repo: {L}. Your job is to ATTACK what wave 1
produced and the L1 landed. Frozen claims {CLAIMS} (freeze {FREEZE}, first recorded probe run {FIRST}); landing commit
{LAND}; docs commit {DOCS} (SCORECARD/LOG round-43 sections). Measure on a clean clone of {DOCS} unless told otherwise.
- C1 calibration: counter {C1}, battery {BAT}/ (7 modules, 42 fixtures, one wave-1 seat each), 9 frozen mutants
  (NA1 NA5 NA7 NA18 NA20 NA21 NO5 NO7 NO22). Landing measurement {W}/integrate/measure-final.txt: `MUTANTS total=9 killed=9
  survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=6/6 order=3/3`, `PREDICATE C1 pass`. A kill is
  attributed by span (leg f) AND by a differing site record (leg g). Wave-1 limits: {W}/build/R43SentinelCounter.md F1-F6
  (separate git dir, depth cap, argparse abbreviation, no timeout, include.path/alternates reads), {W}/build/R43CritC1Counter.md
  V2' (absolute argv bypasses leg i). The counter cannot see intent: the freeze module copied as battery passes
  ({W}/claims/control-c1-witness-as-battery.txt), so non-author review of battery43 is part of admission.
- C2 coverage: counter {C2} (V1-V10), entry {ENTRY}, rows S129-S134 (tier A, spec-pinned) + S136/S137 (tier B, flips executed),
  probe {PROBE}, receipt {RCPT} (`cases=12 observed_pass=8 observed_fail=4 mismatches=0`, `regrade cases=12 differ=0`), captures
  {CAP}/. Landing: `checks=10 defects=0`, `PREDICATE C2 pass`. Wave-1 limit: V10's DECISIVE map is readable in the counter
  ({W}/build/R43CritClaims.md §1).
- Routed work landed: fibsqrt entry errata + S135 block ({ENTRY42} tail), S128 Gate row + flip checks in
  {L}/corpus/lessons/round-42.md, {L}/plans/gate_flip_check.py + Q35, 44 new rows in {L}/corpus/routed-findings.jsonl,
  appended round-42 corrections in lesson/QUALITY/SCORECARD, round-43 lesson {LESSON}.
- Wave-1 reports: {W}/build/*.md (38 seats); results {W}/build-results.json.

# Host-safety rule (orchestrator; binding for every seat)
{HOST_RULE}
{ENVELOPE}

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report dir is {FX}/; drafts and receipts go under {FX}/<YourSeatName>/ (create it). Never copy a corpus/ or
  plans/ tree, a lane mirror, or a clone into {FX}/; no receipt file over 1 MiB (quote it, give its sha256, delete it).
- {SCRATCH}
- Write ONLY inside {FX}/ (your report + your own subdir) and your scratch dir. NEVER edit the lane's corpus/, plans/,
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

ITEMS = [
    ("F43C1Rerun", "executor", ["calibration", "operability"],
     f"{HOST_RULE}\n\nRe-measure C1 on a clean `--no-local` clone of {DOCS} inside the envelope: `python3 plans/round43_c1_verify.py --lane "
     f"\"$S/lane\" --work \"$S/w\"` with `--jobs 1` and `--jobs 8`, and under two PYTHONHASHSEED values for the counter process. Then make "
     f"each of the 7 battery43 modules absent in turn (in YOUR clone) and record which mutants lose their last killer (load-bearing table). "
     f"Paste every summary line and diff the runs.",
     "VERDICT: c1-rerun-<pass|fail>-byte-equal-<k>/<n>-modules-load-bearing-<m>/7"),
] + [
    ("F43RevBat" + "".join(x.capitalize() for x in m.split("_")), "critic", ["calibration", "discernment"],
     f"{HOST_RULE}\n\nAdversarial honesty review of battery module {BAT}/{m}.py against {C1} and the tools {ANC} / {ORD}: for each "
     f"fixture, does its kill demonstrate the ADVERTISED behaviour of the mutant's `adv` cell (not a substitute shape, not a crash, not a "
     f"fence-gap shape — separate git dir, `.git` file, deep repo, include.path/alternates, absolute or abbreviated argv, symlinks), is "
     f"its `expect`/`defects` what the unmodified tool prints, is it a re-spelling of {WIT}/w_near.py? Run the module alone in your clone "
     f"(`--battery-dir`, inside the envelope) and paste the MUTANT lines. Per-fixture table: honest / substitute / incidental.",
     f"VERDICT: battery-{m}-honest-<k>/<n>-substitutes-<s>")
    for m in ("a_row", "a_url", "a_err", "a_alt", "o_scan", "o_excuse", "o_alt")
] + [
    ("F43MutBattery", "mutation-tester", ["calibration"],
     f"{HOST_RULE}\n\nMutation-test battery43 itself: remove each of the 42 fixtures in turn (copy of {BAT} in your clone, development "
     f"mode) and record which fixture removal makes any of the 9 mutants survive (single points of failure); then write 10+ NEW "
     f"near-variants of the same tool branches (as {L}/.ufo/waves/round-42/falsify/F42XMutNear.md did) in a copy of {C1}, run them against "
     f"battery43, and table killed/survived — the survivors are round-44 data.",
     "VERDICT: battery43-spof-<s>-near-variants-killed-<k>/<n>"),
    ("F43C1FenceForge", "critic", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nUsing the wave-1 fence gaps ({W}/build/R43SentinelCounter.md F1-F3, {W}/build/R43CritC1Counter.md V2'), try to "
     f"FORGE an attributed kill of any of the 9 frozen mutants of {C1} with a fixture that does not demonstrate the advertised behaviour "
     f"(e.g. git dir outside d serving a crafted history, a repo deeper than 3 levels, abbreviated `--rec`). Attack modules only in your "
     f"report dir/scratch, runs inside the envelope. Report forged/blocked per vector with the counter lines.",
     "VERDICT: c1-forged-kills-<n>-vectors-<v>"),
    ("F43ValueLegForge", "critic", ["calibration", "soundness"],
     f"{HOST_RULE}\n\nAttack leg g of {C1}: build a fixture where the mutant's replaced span runs, its site record differs from the "
     f"reference's for an INCIDENTAL reason (a value that differs but does not cause the rc flip), and the rc flips for a different "
     f"reason — does the counter credit it? Also: is leg g ever the deciding leg on battery43 (count hits where span ran but records were "
     f"equal, via a copy of the counter that prints both legs)? Paste runs.",
     "VERDICT: value-leg-incidental-credit-<yes|no>-deciding-<n>"),
    ("F43C2Rerun", "executor", ["coverage", "freshness"],
     f"{HOST_RULE}\n\nRe-measure C2 on a clean `--no-local` clone of {DOCS} inside the envelope: `python3 plans/round43_c2_verify.py --lane "
     f"\"$S/lane\" --work \"$S/w\"`; then run `python3 plans/feal_probe.py --lane \"$S/lane\" --work \"$S/p\"` three times (one under "
     f"`env -i PATH=/usr/bin:/bin`) and `cmp` each against {RCPT}. Paste verdict lines and cmp results.",
     "VERDICT: c2-rerun-<pass|fail>-probe-byte-equal-<k>/3"),
    ("F43EntryQuotes", "reviewer", ["coverage", "depth"],
     f"Review {ENTRY}: every located quote verbatim at its cited capture line ({CAP}/), every case-table/mechanism row equal to {RCPT} "
     f"and on a DECISIVE line ({C2}), and every factual sentence checked against the captures and the receipt — list wrong or "
     f"overclaiming sentences with line, the evidence line, and the correction (counts of quotes ok / sentences bad).",
     "VERDICT: entry-quotes-ok-<k>/<n>-bad-sentences-<b>"),
    ("F43ReopenRows", "scout", ["freshness", "coverage"],
     f"Re-open every new registry row S129-S137 in {L}/corpus/SOURCES.md (raw URLs at pin 2fd12b88; `curl`, sha256, `cmp` with the "
     f"capture; S135 against corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile): is each cell right (kind, tier, anchor quote verbatim "
     f"at its line, sha256, teaches, used-by)? Paste access times and digests.",
     "VERDICT: rows-reopened-<k>/9-wrong-cells-<w>"),
    ("F43CritOverclaim", "critic", ["coverage", "discernment"],
     f"Overclaim hunt in the new prose: {ENTRY}, the round-43 paragraphs of {L}/PROVINCE.md, {L}/SKILL.md §'In-process module-import TB2 "
     f"grader — round 43', {L}/corpus/README.md (index row, coverage bullet, §Frontier round-43 sub-bullet, Round-43 evidence) and {LESSON}. "
     f"Every number must re-derive from {RCPT} or a capture; every 'new class'/'first' sentence must be worded as module import + call "
     f"(regex-log executes an agent regex in-process). List wrong/overclaiming sentences with file:line.",
     "VERDICT: overclaims-<n>-wrong-<w>"),
    ("F43CritV10", "critic", ["coverage", "calibration"],
     f"Attack V10 of {C2} beyond {W}/build/R43CritClaims.md: how many of the 12 DECISIVE sets can a filler satisfy by quoting ANY two "
     f"words of the cited line without understanding (e.g. `import attack`)? Build 3 filler shapes in your clone and run v9/v10. Then "
     f"propose (draft only) a content leg whose key is not readable from the instrument, with a red control.",
     "VERDICT: v10-fillers-passing-<k>/3-draft-<yes|no>"),
    ("F43ClockSeed", "executor", ["coverage", "soundness"],
     f"{HOST_RULE}\n\nMeasure the `cheat-clock-seed` case's robustness: in a COPY of {PROBE} in your clone, add a variant that sleeps "
     f"0/5/9/11/15 s between `create_random_keys()` and the replay (wrap attack), run each 3x inside the envelope, and report the pass "
     f"rate; confirm the 10 s window is the only failure mode (wave-1 {W}/build/R43CritProbe.md finding 1).",
     "VERDICT: clock-seed-pass-<k>/<n>-window-<s>s"),
    ("F43PriorArtCheck", "critic", ["novelty", "discernment"],
     f"Re-open every URL the entry's `## Prior art` section ({ENTRY}) cites and every claim of {W}/build/R43ScoutPriorArt.md: is each "
     f"quote verbatim at its location, each date right, each published/adjacent/not-found verdict honest? Search once more for (a) "
     f"always-true __eq__ returns defeating `==` graders and (b) os._exit inside pytest-graded tasks in TB2/TB2.1 issues.",
     "VERDICT: prior-art-ok-<k>/<n>-wrong-<w>"),
    ("F43RevErrata", "reviewer", ["quality", "calibration"],
     f"Review the appended `## Errata (round 43 …)` and `### S135 …` blocks at the end of {ENTRY42}: re-derive every correction E1-E7 from "
     f"{L}/corpus/evidence/round42/tb2-circuit-fibsqrt/ and the round-42 receipt; is anything above the appended blocks edited (`git diff "
     f"317148c4 {DOCS} -- <entry>` deletions)? Count correct / wrong.",
     "VERDICT: errata-correct-<k>/<n>-in-place-edits-<e>"),
    ("F43RevGateFlip", "reviewer", ["discernment", "operability"],
     f"Review {L}/plans/gate_flip_check.py and Q35 ({L}/corpus/QUALITY.md tail): run it on every lesson with a `## Gate` (sweep), on "
     f"{L}/corpus/lessons/round-42.md and {LESSON} (should be `unresolved=0`); are the round-42/43 `Flip check` lines TRUE (did each "
     f"flip fire as stated — check the cited entry lines and rows)? Is any refusal with a flip missed by the parser?",
     "VERDICT: flip-check-true-<k>/<n>-missed-<m>"),
    ("F43MutFlipCheck", "mutation-tester", ["operability", "soundness"],
     f"Mutation-test {L}/plans/gate_flip_check.py: 15+ single-line mutants of its parser and resolution rules run against its own "
     f"`--selftest` and against the real round-42/43 lessons. Table caught/survived; draft a fixture per survivor.",
     "VERDICT: flip-check-mutants-caught-<k>/<n>"),
    ("F43RevRoutedLedger", "reviewer", ["calibration", "quality"],
     f"Review {L}/corpus/routed-findings.jsonl as landed: the 44 new rows and the two field changes (R42-R4 closed, R42-R2 check nulled) "
     f"and any rows the L1 closed at docs time — run `python3 plans/routed_open.py --lane \"$S/lane\" --observe` on a clean clone of "
     f"{DOCS}; is every `closed` honest (its check passes, its close pointer resolves) and every `open` row's check red?",
     "VERDICT: routed-rows-honest-<k>/<n>-mismatched-<m>"),
    ("F43RevR42Corrections", "reviewer", ["discernment"],
     f"Review the round-42 corrections appended in round 43: tails of {L}/corpus/lessons/round-42.md, {L}/corpus/QUALITY.md (Round42 "
     f"criteria corrections), {L}/SCORECARD.md (Round-42 corrections appended in round 43), and the S128 Gate row inside the round-42 "
     f"Gate table. Is each correction right against its evidence? Did anything get edited in place (`git diff 317148c4 {DOCS}` deletions)?",
     "VERDICT: r42-corrections-right-<k>/<n>-in-place-<e>"),
    ("F43RevLesson", "reviewer", ["discernment"],
     f"Review {LESSON}: every Mistakes row (evidence pointer resolves, captured-by honest, fix shown able to fail), every Gate row (URL, "
     f"time, quote ≤25 words verbatim, tier), the Routed dispositions against {L}/corpus/lessons/round-42-verifier-spotcheck.md §5 R1-R6, "
     f"the falsifier summary against the wave-1 reports. List defects with line.",
     "VERDICT: lesson43-defects-<n>"),
    ("F43CritScorecard", "critic", ["calibration"],
     f"Attack the round-43 SCORECARD section ({L}/SCORECARD.md, `## Round 43`) and the LOG.md round-43 entry: every number against its "
     f"evidence file, every score move justified by the rubric (`## Scoring rubric`), any self-assessment that mismatches the repo "
     f"(count mismatches, file:line).",
     "VERDICT: scorecard-mismatches-<n>"),
    ("F43NoHarm", "executor", ["calibration", "operability"],
     f"{HOST_RULE}\n\nNo-harm check: diff the verdict lines (`$ `, PREDICATE, RESULT, exit=, rows=, defects=, checks=, routed_open, "
     f"registry_rows, byte_equal) of {W}/integrate/measure-baseline.txt (@ d33350fd) against {W}/integrate/measure-final.txt; then run "
     f"{W}/integrate/measure.sh yourself on {DOCS} (inside the envelope; it needs `$HYAKU_SCRATCH` pointing at a dir you own: set "
     f"HYAKU_SCRATCH=$S and create $S/kengaku-r43/.ROUND-ROOT-SENTINEL containing 'kengaku r43 round root') and diff again. Explain every "
     f"differing line.",
     "VERDICT: no-harm-<k>/<n>-equal-explained-<e>"),
    ("F43ScoutMisroot", "scout", ["safety", "hygiene"],
     f"Host-safety and hygiene watch for wave 2: `ls -la --time-style=full-iso /home/vgpnk/.local/bin` start/end; `git -C {F} status "
     f"--porcelain --untracked-files=all` — any file a kengaku round-43 seat wrote into the fleet root? Scratch dirs under {SCR} with "
     f"sizes; sentinel present start/end? Report only.",
     "VERDICT: misroot-<n>-host-writes-<h>-sentinel-<present|missing>"),
    ("F43CritSeparability", "critic", ["calibration", "coverage"],
     f"Causal separability of C1 and C2: on a clean clone of {DOCS}, remove C2's work product (entry, rows S129-S137, receipt) and run "
     f"{C1}; remove battery43 and run {C2}. Each must keep its own verdict. Paste both.",
     "VERDICT: separable-<yes|no>"),
    ("F43CritPlanNext", "critic", ["calibration", "coverage"],
     f"Attack the `### Planned (round 44)` block of {L}/SCORECARD.md and {W}/build/R43PlanNext.md: do-nothing reachability, literal "
     f"binding, witnessed directions, coverage-class novelty against the nine admitted graders and {W}/build/R43ConsiderThese/hist.md.",
     "VERDICT: plan44-defects-<n>"),
    ("F43EnvelopeV2", "executor", ["operability", "safety"],
     f"Draft {FX}/F43EnvelopeV2/envelope.sh, a v2 of {ENV} whose PATH-dir digest also covers mode bits and unreadable entries "
     f"({W}/build/R43ReviewEnvelope.md: mode change and mode-000 rewrite missed). Show it on a scratch target dir (never ~/.local/bin): "
     f"each of the 4 change kinds + the two misses → CHANGED, no false CHANGED on a quiet dir. Paste runs.",
     "VERDICT: envelope-v2-detects-<k>/6-false-<f>"),
    ("F43ConnClaims", "connector", ["calibration"],
     f"Cross-document consistency after landing: numbers and hashes across {CLAIMS}, {LESSON}, the SCORECARD round-43 section, LOG.md "
     f"round 43, README/PROVINCE/SKILL round-43 text, {W}/integrate/*.txt and `git -C {L} log` (freeze {FREEZE}, first run {FIRST}, "
     f"landing {LAND}, docs {DOCS}; 9 mutants, 42 fixtures, 12 cases, 8/4, rows 121→130). List every drift with both locations.",
     "VERDICT: drift-<n>"),
    ("F43ConnPatterns", "connector", ["calibration", "quality"],
     f"Cross-claim pattern: C1 and C2 both rest on an answer key the instrument carries (C1's witness-as-battery passes; C2's DECISIVE is "
     f"readable). Where else in the lane's gates does the expected answer live inside the checker (plans/*.py)? List sites with file:line "
     f"and one fixture each that would show the checker admitting a copier.",
     "VERDICT: answer-key-sites-<n>"),
    ("F43ConnFrontier", "connector", ["coverage", "adjacency"],
     f"Frontier after landing: does {L}/corpus/README.md §Frontier now read '9 of 89', is the new class worded as module import + call, "
     f"and does any self-assessment line in SCORECARD/SHONEN/README mismatch the repo state (count, file:line)? End with exactly one "
     f"VERDICT line.",
     "VERDICT: frontier-<ok|defects>-mismatches-<n>"),
]

FLASH = {"executor", "labrat", "scribe", "sonic", "simplifier", "critic", "revenger", "sentinel"}
ATTACK = {"reviewer", "critic", "mutation-tester", "labrat"}


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 43 wave 2 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {FX}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r43 wave 2 (falsify)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    c = Counter(i["role"] for i in items)
    flash = sum(n for r, n in c.items() if r in FLASH)
    attack = sum(n for r, n in c.items() if r in ATTACK)
    assert 32 <= len(items) <= 64, len(items)
    assert flash * 2 >= len(items), f"m_flash share {flash}/{len(items)} below half (closure R6)"
    assert attack * 4 >= len(items), f"attack share {attack}/{len(items)} below a quarter"
    spec = {"wave": "kengaku-r43-falsify",
            "milestone": "kengaku round 43 wave 2: falsify battery43, the C1/C2 counters, the feal package and the routed landings",
            "reportDir": ".ufo/waves/round-43/falsify", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/falsify-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    print(len(items), dict(c))
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
