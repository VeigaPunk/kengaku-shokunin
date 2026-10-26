#!/usr/bin/env python3
"""Renders .ufo/waves/round-39/falsify-spec.json (wave 2 of 2, policy v1): attacks on what wave 1 and the L1 landed."""
import json
import pathlib
import subprocess
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-39"
B = f"{W}/build"
FX = f"{W}/falsify"
SCR = "/fast/scratch/hyaku/kengaku-r39"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
TIP = subprocess.run(["git", "-C", L, "rev-parse", "refs/heads/master"], capture_output=True, text=True, check=True).stdout.strip()
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/git-leak-recovery"
CAP = f"{L}/corpus/evidence/round39/tb2-git-leak-recovery"
RCPT = f"{L}/corpus/evidence/round39/git-leak-probe.txt"
DRY = f"{L}/corpus/evidence/round39/git-leak-dry-cases-freeze.txt"
C1 = f"{L}/plans/round39_c1_verify.py"
AUD = f"{L}/plans/round39_c1_audit.py"
C2 = f"{L}/plans/round39_c2_verify.py"
PROBE = f"{L}/plans/git_leak_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
CLAIMS = f"{L}/plans/round-39-claims.md"
ENTRY = f"{L}/corpus/knowledge/tb2-git-leak-recovery-grader.md"
LES = f"{L}/corpus/lessons/round-39.md"
BAT = f"{L}/plans/battery39"
FREEZE = "088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8"
FIRST = "6a1eb5e1da4a435940b821e28530c31f3411549c"
MEAS = f"{W}/integrate/measure-final.txt"
CLONE = (f'Fixture rule: S={SCR}/<YourSeatName>; mkdir -p "$S"; trap \'rm -rf -- "$S"\' EXIT; export TMPDIR="$S"; '
         f'git clone -q --no-local {L} "$S/lane" && git -C "$S/lane" checkout -q {TIP}; verify `git -C "$S/lane" rev-parse '
         f'--show-toplevel` equals "$S/lane" before any write; every git call names -C "$S/lane"; never commit. Any other '
         f'fixture repo: D=$(mktemp -d -p "$S") && git -C "$D" init -q, every git call names -C "$D". Remove "$S" before you '
         f'finish (copy receipts into your report dir first).')

CONTEXT = f"""# Goal
kengaku round 39 (hyaku run 8, 2026-10-26), WAVE 2 of 2 (FALSIFY). Lane repo: {L}. Attack what wave 1 and the L1 landed,
measured at lane tip {TIP} (branch master). Every item names what it attacks; a finding is a receipt, not an opinion.
Frozen claims: {CLAIMS} (freeze {FREEZE}; first recorded probe run {FIRST}). Landing measurement on a clean clone of the
tip: {MEAS}. Lesson: {LES}. Wave-1 reports: {B}/*.md.
- C1 calibration: 7 frozen gate mutants M01-M07 in {C1}; battery {BAT}/ (4 modules, one per surviving mutant: p1m M02,
  p3m39 M03, p7m39 M04, d5m39 M07). Frozen predicate: `PINS total=26 mismatched=0`, `BATTERY fixtures=<n> wrong=0
  renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`.
  Wave 1 (`{B}/R39CritC1Counter.md`) showed the frozen counter is gameable (A1 mid-run fixture flip by a daemon, A3 an
  unpinned battery37 file imported in-process, A4 pins hashed once, A5 child-reported dirs trusted); the L1 added a post-hoc
  audit {AUD} (NOT the frozen rule) that re-checks each kill, closes the battery37/38 name sets, re-hashes pins after the
  run and confines fixture dirs, printing `AUDIT C1 clean|dirty`.
- C2 coverage: TB2 `git-leak-recovery` @ {PIN} admitted as {ENTRY} (S117 tests/test_outputs.py, S118 instruction.md;
  captures {CAP}/; receipt {RCPT}; frozen dry table {DRY}; counter {C2}, frozen predicate `checks=7 defects=0`,
  `PREDICATE C2 pass`).
- Routed fixes landed this round: plans/order_check.py (Q30), plans/anchor_digest_check.py, plans/ledger_tip.py,
  plans/mutant_direction_check.py, errata appended to corpus/lessons/round-38.md and three TB2 entries, QUALITY Q30.

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report dir is {FX}/; receipts go under {FX}/<YourSeatName>/ (create it). Never copy a corpus/ or
  plans/ tree, a lane mirror, or a clone into {FX}/.
- Scratch (operator directive 2026-10-25): clones and work trees live ONLY under {SCR}/<YourSeatName>/ (NVMe), never under
  /tmp; pass it explicitly (export TMPDIR, --work); delete it before you finish (`trap 'rm -rf -- "$S"' EXIT`).
- Write ONLY inside {FX}/ and your scratch dir. NEVER edit any lane file; never write into {F} (fleet root), sibling lanes,
  the lane's jj state or Git index; never run git add/commit/stash/checkout/reset/push/pull or a mutating jj command in the lane.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide:
  install via `uv tool` / `npx` / an official binary into ~/.local/bin, or file nothing and say so. Never run pacman
  -Sy/-Syu/-U/-R, never name an already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat probe).
  Never leave a process running when you finish.
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output; quotes carry file:line and are <= 25 words.
  Do not fabricate output; if something cannot be run, say so.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""

ITEMS = [
    ("F39C1Rerun", "executor", ["calibration"],
     f"Re-run `python3 {C1} --lane .` and `python3 {AUD} --lane .` on your clean clone of {TIP} under two interpreters "
     f"(host python3 and `uv run -p 3.13 --no-project python`), two PYTHONHASHSEED values; diff the MUTANT/summary lines against {MEAS}.",
     "VERDICT: c1-rerun-<pass|fail>-audit-<clean|dirty>-agree-<yes|no>"),
    ("F39RevBatP1", "reviewer", ["calibration"],
     f"Code review of {BAT}/p1m.py: does its one fixture honestly exhibit M02's advertised behaviour (a non-first frozen "
     f"instrument off its pin) with no state that changes between the counter's phases, no side channel, exact declared "
     f"defects? Run it alone (`--battery-dir`, `--only M02`) and with the fixture's edit removed. Cite file:line.",
     "VERDICT: p1m-<honest|n-defects>"),
    ("F39RevBatP3", "reviewer", ["calibration"],
     f"Same review for {BAT}/p3m39.py (M03, a 26-word quote one above the bound): is the reference's P3 DEFECT caused by the "
     f"word count alone (not by P4 or another clause), and does the mutant's `hi + 1` silence it on that fixture only?",
     "VERDICT: p3m39-<honest|n-defects>"),
    ("F39RevBatP7", "reviewer", ["calibration"],
     f"Same review for {BAT}/p7m39.py (M04, two source lines for one sid): is the P7 DEFECT caused by the duplicate line alone; "
     f"would the fixture still kill if the second line were the pinned URL vs another URL; any dependency on corpus bytes "
     f"that a later round's corpus edit would break (round-39 lesson Mistakes row on load-bearing genuine-package bytes)?",
     "VERDICT: p7m39-<honest|n-defects>"),
    ("F39RevBatD5", "reviewer", ["calibration"],
     f"Same review for {BAT}/d5m39.py (M07, markup inside the quote span, manifest re-pinned, mirror): reference `D5 ok`, "
     f"mutant `D5 DEFECT` — caused by the tag strip alone? Does the fixture own its capture dir and spec inside d?",
     "VERDICT: d5m39-<honest|n-defects>"),
    ("F39MutBattery", "mutation-tester", ["calibration"],
     f"Fixture-level mutation of battery39: for each of the 4 modules apply 3 one-line mutants in a copy (declared defects "
     f"changed, the defining edit removed, the edit moved to the first item / below the bound) and run the counter with "
     f"`--battery-dir` on the copy; report which mutants the counter's `wrong`/kill lines catch.",
     "VERDICT: battery39-mutants-caught-<k>/<n>"),
    ("F39XMut", "mutation-tester", ["calibration"],
     f"Extra non-frozen mutants near M02/M03/M04/M07 (e.g. P1 `[:2]` or last-pin-only; P3 lower bound `lo - 1`; P7 last line "
     f"only / set compare; D5 a different tag regex) — write them as (old,new) pairs against {GATE}, run them over the full "
     f"landed battery with a harness modelled on {C1}'s kill rule (copy into your clone; never edit the lane), report "
     f"killed/survived with witnesses for survivors (round-40 candidates).",
     "VERDICT: xmut-killed-<k>/<n>"),
    ("F39CritAudit", "critic", ["calibration"],
     f"Attack {AUD}: replay wave 1's A1/A3/A4/A5 modules ({B}/R39CritC1Counter/*.py) against it in your clone — does it print "
     f"`AUDIT C1 dirty` (or refuse) for each; can a new attack keep it `clean` with a dishonest battery; does it false-red on "
     f"the honest landed battery? Diff it against {C1} and check it changes nothing but the four repairs.",
     "VERDICT: audit-attacks-caught-<k>/<n>-false-red-<yes|no>"),
    ("F39CritC1Count", "critic", ["calibration"],
     f"Recount C1's calibration denominator: wave 1 (`{B}/R39CritClaims.md` §1, `{B}/R39AdvErrata.md`) says only M02, M03, M05, "
     f"M06 have a reaching advertising sentence and M01/M04/M07 do not. Verify each tier against {GATE} docstring, "
     f"{L}/corpus/QUALITY.md Q24/Q27, {L}/SCORECARD.md:564; check the lesson's and SCORECARD's stated before/after mismatch "
     f"counts against that recount.",
     "VERDICT: c1-advertised-<k>/7-stated-count-<ok|wrong>"),
    ("F39MutDirection", "mutation-tester", ["calibration"],
     f"Mutation-test the landed {L}/plans/mutant_direction_check.py (wave-1 R39DirCheckLeg added a redundant leg; "
     f"{B}/R39DirCheckLeg.md): replay the three F38MutDirection mutants and 3 new ones; does it still print `N21 ... "
     f"MISLABELLED` at the tip; can it load the round-39 list (R39CritClaims §7 says Q29's tool cannot)?",
     "VERDICT: direction-check-mutants-<k>/<n>-r39-list-<loads|no>"),
    ("F39NoHarmC1", "critic", ["calibration"],
     f"No-harm on earlier C1 instruments at the tip: `plans/round37_c1_verify.py` must print `killed=55`, "
     f"`plans/round38_c1_verify.py` its landed `killed=21 survived=1`; `git diff --stat {FREEZE} {TIP} -- plans/battery37 "
     f"plans/battery38 plans/round3[678]_c1_verify.py plans/pkg_gate.py plans/pkg-spec-r35.json` must be empty. Also: did any "
     f"round-39 corpus edit change a byte the round-36..38 batteries copy (genuine package = round-35 entry and its rows)?",
     "VERDICT: no-harm-c1-<ok|n>"),
    ("F39C2Rerun", "executor", ["coverage", "calibration"],
     f"Re-run `python3 {C2} --lane .` on your clean clone (needs the fleet census script; note it) and `python3 {PROBE} "
     f"--lane .` three times (one under `env -i PATH=/usr/bin:/bin HOME=$S`); cmp each probe output with {RCPT}; run "
     f"`(cd corpus/evidence/round39/tb2-git-leak-recovery && sha256sum -c SHA256SUMS)`.",
     "VERDICT: c2-rerun-<pass|fail>-probe-byte-equal-<k>/3"),
    ("F39ReopenRows", "reviewer", ["freshness", "coverage"],
     f"Re-open S117 and S118 live ({RAW}/tests/test_outputs.py, {RAW}/instruction.md): sha256 vs the rows' anchor cells and "
     f"{CAP}/SHA256SUMS, quote verbatim at the stated line and <= 25 words, 11 cells, tier/status/used-by right "
     f"({L}/corpus/SOURCES.md rows S117/S118).",
     "VERDICT: rows-<k>/2-quotes-<j>/2"),
    ("F39EntryQuotes", "critic", ["depth", "calibration"],
     f"Every `## Located quotes` row of {ENTRY}: quote verbatim at `capture:line` (sed -n), and does the quote support its "
     f"claim cell? Then every prose sentence in Summary/Findings that states a grader behaviour: is it tied to a receipt case "
     f"or a capture line that shows it? List unsupported sentences.",
     "VERDICT: entry-quotes-<ok>/<n>-unsupported-<k>"),
    ("F39CritOverclaim", "critic", ["calibration"],
     f"Overclaim hunt across {ENTRY}, the README round-39 lines, the PROVINCE round-39 paragraph and the SKILL "
     f"'Repository-history TB2 grader — round 39' section: class claims, universal clauses, 'first', anything the receipt or "
     f"captures do not show. Quote each with file:line and the narrower wording.",
     "VERDICT: overclaims-<n>"),
    ("F39MapControl", "mutation-tester", ["calibration"],
     f"V7 controls on the landed entry in your clone: relabel each map row to each other label, cite a non-violating case, "
     f"duplicate a tag, drop a tag, wrong line number — each must turn `python3 {C2}` V7 red. Also: the entry's 'reviewer should "
     f"prefer' paragraph says messages-untouched is `unenforced` without empty-app — re-derive it.",
     "VERDICT: v7-controls-<k>/<n>"),
    ("F39IndepProbe", "critic", ["coverage"],
     f"Independent extra states not among the 25 (refs/replace, packed-refs only, a worktree, .git as a gitfile, secret in a "
     f"tree object name, reflog of a deleted branch): predict per test from {CAP}/test_outputs.py first, then run each in a "
     f"copy of {PROBE} in your clone; report predictions vs observed. Limits only, no lane edit.",
     "VERDICT: indep-extra-agree-<k>/<n>"),
    ("F39CritSkill", "critic", ["depth"],
     f"The SKILL.md section 'Repository-history TB2 grader — round 39' and the three registry rows (git-leak-probe, "
     f"round39-c1-mutants, round39-c2): does every decision-table row cite a receipt case that shows it; are the exit-code "
     f"semantics of each registry row true (run each tool's failure paths cheaply)?",
     "VERDICT: skill-rows-<ok>/<n>"),
    ("F39CritPriorArt", "critic", ["novelty", "coverage"],
     f"Re-open each prior-art source the entry's `## Prior art` cites (TASK_REVIEW_AUTOMATION.md:244, "
     f"JonathanGabor audit.txt:1485 @ 35f11039, Evan-Kim2028 tb21_census_verdicts.jsonl:33, laion README.md:107, TB2.1 #239, "
     f"TB2 #84/#86): quote present at the stated location, dates/states right, and does any of them already report "
     f"`echo-only` / reflog retention (which would void 'first probed instance')?",
     "VERDICT: prior-art-<ok>/<n>-voids-<yes|no>"),
    ("F39OrderGateMut", "mutation-tester", ["calibration", "operability"],
     f"Mutation-test {L}/plans/order_check.py: 6 one-line mutants (drop the P10 exemption check, skip the freeze-contains-receipt "
     f"leg, scan only the freeze commit, accept any P10, read the work tree, swallow git errors); for each, does the red pair "
     f"(round 37 and 38) / green (round 39) still discriminate?",
     "VERDICT: order-gate-mutants-<caught>/<n>"),
    ("F39AnchorFix", "executor", ["calibration", "operability"],
     f"Re-run the landed {L}/plans/anchor_digest_check.py at the tip and on wave-1's multi-locator fixture "
     f"({B}/R39AnchorUnion/); review the diff vs `git show {FREEZE}:plans/anchor_digest_check.py`: false reds, lost "
     f"round-38 behaviours (cross-row substitution, S110 63-hex)?",
     "VERDICT: anchor-fix-<ok|n-defects>"),
    ("F39LedgerTip", "executor", ["operability"],
     f"Re-run the landed {L}/plans/ledger_tip.py at the tip (`--lane .` and `--source <clone> --work`), in a detached clone, "
     f"and with a stale local master; review its diff vs {FREEZE}; does it print which revision it audits?",
     "VERDICT: ledger-tip-<ok|n-defects>"),
    ("F39CritQ30", "critic", ["calibration"],
     f"Attack QUALITY Q30 ({L}/corpus/QUALITY.md, last criterion): every command in its Check reproduces as written; its "
     f"limits are honest; is it a gate or still a rule (does anything run it automatically)? Is the 'no recurrence=2 ledger row' "
     f"note consistent with {CLAIMS}'s frontier-step sentence?",
     "VERDICT: q30-<ok|n-defects>"),
    ("F39RevErrata", "reviewer", ["quality"],
     f"Review the appended errata: {L}/corpus/lessons/round-38.md `## Errata (round 39)`, and the `## Errata (round 39)` "
     f"blocks of tb2-regex-log/tb2-git-webserver/tb2-build-pmars entries: append-only (git diff vs {FREEZE} shows 0 removed "
     f"lines), each corrected recheck command green as written from a clean clone root. Verify the lesson's claim that "
     f"appending to tb2-protein-assembly-grader.md breaks battery38 p7m (do it in your clone and run the round-38 counter).",
     "VERDICT: errata-<ok>/<n>-protein-claim-<confirmed|refuted>"),
    ("F39RevLesson", "reviewer", ["calibration"],
     f"Review {LES}: every number re-derivable from committed files; Gate rows (admits/refusals) have reasons and flip "
     f"conditions; each Mistakes row's fix is shown able to fail; header baseline drift (ef2fba0) stated correctly.",
     "VERDICT: lesson-<n>-defects"),
    ("F39RevScorecard", "reviewer", ["calibration"],
     f"Calibration count of the self-report: compare every factual statement in SCORECARD.md's round-39 section, the LOG.md "
     f"round-39 entry and SHONEN.md against repo state at {TIP} (commands). Count mismatches.",
     "VERDICT: self-report-mismatches-<n>"),
    ("F39CritNoHarmDiff", "critic", ["quality"],
     f"No-harm diff: `git diff --numstat b2bdd425 {TIP}` over lane-authored docs (SCORECARD, LOG, SKILL, PROVINCE, SHONEN, "
     f"corpus/SOURCES, README, QUALITY, knowledge, lessons): any removed line? For the three edited plans tools, list removed "
     f"behaviours. Run every round-36..38 counter at the tip (`.ufo/waves/round-39/integrate/measure.sh` lists them).",
     "VERDICT: no-harm-removed-lines-<n>"),
    ("F39ScoutMisroot", "scout", ["operability"],
     f"Misroot and scratch audit: `git -C {F} status --porcelain --untracked-files=all` — any file a kengaku round-39 seat wrote "
     f"(content names kengaku r39)? `du -sh {SCR}/*` — leftover seat dirs; `ps -eo pid,etime,cmd | grep -E 'kengaku-r39|k39-'` — "
     f"leftover processes (wave-1 sentinel reported `sleep 5311` survivors). Report, do not delete.",
     "VERDICT: misroot-<n>-scratch-leftovers-<k>-procs-<j>"),
    ("F39ConnClaims", "connector", ["calibration"],
     f"Cross-document drift: the same fact stated in {CLAIMS}, {LES}, SCORECARD round-39 section, LOG round-39 entry, "
     f"{ENTRY}, README/PROVINCE round-39 text and {MEAS} — counts, hashes, verdicts, case names. List disagreements.",
     "VERDICT: cross-doc-drift-<n>"),
    ("F39ConnFrontier", "connector", ["coverage"],
     f"Frontier consistency after integration: README §Frontier round-39 sub-bullet, coverage-map bullet, index row, PROVINCE "
     f"round-39 paragraph, and the count '5 of 89' everywhere; do older sub-bullets still say '4 of 89' in a way that now "
     f"contradicts; is any self-assessment line stale?",
     "VERDICT: frontier-<ok|n-defects>"),
    ("F39SentinelAudit", "sentinel", ["operability"],
     f"Trusted-boundary review of the new tools: {AUD} (child processes, nonce), {L}/plans/order_check.py (git reads), and "
     f"the wave-1 sentinel's C1 findings ({B}/R39SentinelProbe.md) — which remain open at the tip, which does the audit close? "
     f"Test cheaply in scratch; cite file:line.",
     "VERDICT: sentinel-<n>-open"),
    ("F39CritSeparability", "critic", ["calibration"],
     f"Separability: in clones, (a) remove the whole C2 package (entry, rows, README lines, receipt) and run {C1}; (b) remove "
     f"plans/battery39 entirely and run {C2}; (c) remove only the README index row. Report which predicate moves; compare with "
     f"{CLAIMS} §Separability and the lesson's correction.",
     "VERDICT: separable-<yes|partly|no>"),
    ("F39TipReceipts", "executor", ["freshness", "operability"],
     f"Run `python3 {L}/plans/tip_receipts.py --lane <clone> --work $S/tr` at the tip: does it pick up "
     f"corpus/evidence/round39/git-leak-probe.txt (it looks for probe* receipts with a committed re-run command)? Report "
     f"receipts/byte_equal/differ/skipped and a tamper control.",
     "VERDICT: tip-receipts-<k>/<n>-git-leak-<covered|skipped>"),
    ("F39CritR38Dispositions", "critic", ["calibration", "quality"],
     f"Check {B}/R39R38Integrate/dispositions.md: for every round-38 wave-2 finding marked fixed this round, is the fix at the "
     f"tip (command + output)? For every 'routed to round 40', is it named in SCORECARD's Planned (round 40) or the lesson?",
     "VERDICT: dispositions-verified-<k>/<n>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 39 wave 2 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {FX}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r39 wave 2 (falsify)"})
    assert len({i["name"] for i in items}) == len(items)
    spec = {"wave": "kengaku-r39-falsify",
            "milestone": f"kengaku round 39 wave 2: falsify C1 battery39/audit, C2 git-leak package, routed fixes at {TIP[:8]}",
            "reportDir": ".ufo/waves/round-39/falsify", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/falsify-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c), TIP)
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"] + c["sentinel"]
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
