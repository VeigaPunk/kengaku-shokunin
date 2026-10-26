#!/usr/bin/env python3
"""Renders .ufo/waves/round-38/falsify-spec.json (wave 2 of 2, policy v1). Usage: make_falsify_spec.py <landed tip hash>"""
import json
import pathlib
import sys
from collections import Counter

TIP = sys.argv[1]
L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-38"
B = f"{W}/falsify"
BLD = f"{W}/build"
SCR = "/fast/scratch/hyaku/kengaku-r38"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
CAP = f"{L}/corpus/evidence/round38/tb2-build-pmars"
RCPT = f"{L}/corpus/evidence/round38/build-pmars-probe.txt"
DRY = f"{L}/corpus/evidence/round38/build-pmars-dry-cases-freeze.txt"
C1 = f"{L}/plans/round38_c1_verify.py"
C2 = f"{L}/plans/round38_c2_verify.py"
PROBE = f"{L}/plans/build_pmars_probe.py"
GATE = f"{L}/plans/pkg_gate.py"
CLAIMS = f"{L}/plans/round-38-claims.md"
ENTRY = f"{L}/corpus/knowledge/tb2-build-pmars-grader.md"
BAT = f"{L}/plans/battery38"
LESSON = f"{L}/corpus/lessons/round-38.md"
CLONE = (f'Clone rule: S={SCR}/<YourSeatName>; mkdir -p "$S"; trap \'rm -rf -- "$S"\' EXIT; export TMPDIR="$S"; '
         f'git clone -q --no-local {L} "$S/lane" && git -C "$S/lane" checkout -q {TIP}; verify `git -C "$S/lane" rev-parse '
         f'--show-toplevel` equals "$S/lane" before any write; every git call names -C "$S/lane"; never commit. Remove "$S" before '
         f'you finish (copy receipts into your report dir first).')

CONTEXT = f"""# Goal
kengaku round 38 (hyaku run 8, 2026-10-26), WAVE 2 of 2 (FALSIFY). Lane repo: {L}; landed tip under attack: {TIP}.
Frozen claims: {CLAIMS} (freeze e0a378539a45cc9388c66cfba22f44275131de23; first recorded probe run e95cf550). Read it first.
- C1 calibration: 22 frozen gate mutants N01-N22 in {C1}, killed only ATTRIBUTABLY by fixtures in {BAT}/*.py (12 modules written by
  wave-1 executors, integrated by the L1). Before (freeze, {W}/claims/control-c1-nothing.txt): `MUTANTS total=22 killed=0
  survived=22`. Landing receipt: {W}/integrate/measure-final.txt — `MUTANTS total=22 killed=21 survived=1`, `PREDICATE C1 fail`
  (N21 frozen as `silence` but only killable as a mirror; the L1 reports C1 as an honest stop, not relabelled; lesson Mistakes
  row 1, plans/mutant_direction_check.py). Attack both the 21 kills and the N21 explanation.
- C2 coverage: TB2 `build-pmars` grader (terminal-bench-2 @ {PIN}) admitted as {ENTRY}, rows S115/S116, receipt {RCPT}
  (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`), counter {C2} (V1-V7; V7 derives requirement-map labels from all
  violating cases). Before: `checks=7 defects=4` ({W}/claims/control-c2-nothing.txt).
- Frontier/routed work landed this round: QUALITY Q28 + erratum on corpus/knowledge/tb2-git-webserver-grader.md (round-37 D2),
  plans/anchor_digest_check.py binding (D3), ledger-tip in detached clones (D4), plans/tip_receipts.py (considerthese 2(c)),
  lesson {LESSON}. Wave-1 reports: {BLD}/*.md.
Your job is to ATTACK: re-run, re-open, break. Every item names what it attacks. A finding is only as good as its command+output.

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report dir is {B}/; receipts go under {B}/<YourSeatName>/ (create it). Never copy a corpus/ or plans/ tree,
  a lane mirror, or a clone into {B}/.
- Scratch (operator directive 2026-10-25): clones and work trees live ONLY under {SCR}/<YourSeatName>/ (NVMe), never under /tmp;
  pass it explicitly (export TMPDIR, --work); delete it before you finish.
- Write ONLY inside {B}/ and your scratch dir. NEVER edit any lane file, the fleet root {F}, sibling lanes, the lane's jj state or
  Git index. Never run git add/commit/stash/checkout/reset/push/pull or any mutating jj command in the lane.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide:
  install via `uv tool` / `npx` / an official binary into ~/.local/bin, or file nothing and say so. Never run pacman
  -Sy/-Syu/-U/-R, never name an already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat probe).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output; quotes <= 25 words with location. Never fabricate.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""


def revbat(name, role, modules):
    mods = ", ".join(f"{BAT}/{m}.py" for m in modules)
    return (name, role, ["calibration"],
            f"Attack battery38 modules {mods}: for each fixture, does it demonstrate the ADVERTISED behaviour its mutant names (the `adv` "
            f"cell in {C1} MUTANTS), or does it kill incidentally (tailored `defects` declaration, a spec the gate would never see, a "
            f"second clause doing the work)? Look for side channels the token scan misses (reading the gate file, timing, env via "
            f"os.getenv, argv inspection) and fixture-name keying. In your clone run `python3 {C1} --lane \"$S/lane\" --only <those "
            f"mutants> --work \"$S/w\"`, then delete each fixture in turn (in the clone) and confirm its mutant SURVIVES. Paste outputs.",
            f"VERDICT: battery-{'-'.join(modules)}-attack-<n>-defects")


ITEMS = [
    ("F38C1Rerun", "executor", ["calibration"],
     f"Re-run the frozen C1 counter on a clean clone of {TIP}: `python3 plans/round38_c1_verify.py --lane . --work \"$S/w\"`; paste "
     f"PINS/BATTERY/MUTANT/MUTANTS/PREDICATE lines; diff against {W}/integrate/measure-final.txt. Also confirm the round-37 counter "
     f"still passes (`python3 plans/round37_c1_verify.py --lane .`).",
     "VERDICT: c1-rerun-<pass|fail>-killed-<k>/22"),
    ("F38C1RerunPy313", "executor", ["calibration", "operability"],
     f"Interpreter independence: run the C1 counter on a clean clone of {TIP} under a different Python (e.g. `uv run --no-project -p "
     f"3.13 python plans/round38_c1_verify.py --lane .`; the gate runs as sys.executable). Compare with the host-python receipt "
     f"{W}/integrate/measure-final.txt line by line.",
     "VERDICT: c1-interpreters-<same|differ>"),
    ("F38C2Rerun", "executor", ["coverage"],
     f"Re-run the frozen C2 counter on a clean clone of {TIP} (`python3 plans/round38_c2_verify.py --lane .`) and the probe twice "
     f"(`python3 plans/build_pmars_probe.py --lane .`), cmp both runs with {RCPT}; `--dry` cmp with {DRY}; `sha256sum -c` the capture "
     f"manifest.",
     "VERDICT: c2-rerun-<pass|fail>-probe-byte-equal-<yes|no>"),
    revbat("F38RevBatA", "reviewer", ["b1run", "mainx"]),
    revbat("F38RevBatB", "reviewer", ["p10a", "p10b"]),
    revbat("F38RevBatC", "reviewer", ["p3m", "p5m"]),
    revbat("F38CritBatD", "critic", ["p4a", "p4b"]),
    revbat("F38CritBatE", "critic", ["p6m", "p7m"]),
    revbat("F38CritBatF", "critic", ["d4m", "d5m"]),
    ("F38XMutP", "mutation-tester", ["calibration"],
     f"Extra (non-frozen) mutants against {GATE} clauses P1-P8 beyond N01-N22 and M01-M55 (read both lists): first-item-only, off-by-"
     f"one, loosened compare, reordered branch, mirror (force DEFECT on a pass branch). >=8 mutants, each `old` occurring once; run "
     f"them over the FULL landed battery (round-36 + battery37 + battery38) with the round-38 attributed rule (reuse the counter's "
     f"functions by importing {C1} in a harness in your report dir). Report kill/survive; survivors are round-39 candidates.",
     "VERDICT: xmut-p-killed-<k>/<n>"),
    ("F38XMutRerunMain", "mutation-tester", ["calibration"],
     f"As F38XMutP but for P9, P10, run_checks, main() and the D4/D5 line subcommands: >=8 extra mutants, attributed rule, full "
     f"battery. Report kill/survive.",
     "VERDICT: xmut-rest-killed-<k>/<n>"),
    ("F38MapV7Control", "mutation-tester", ["calibration", "quality"],
     f"Show the mined-mistake fix can fail: in your clone relabel ONE row of {ENTRY} `## Requirement map` (e.g. a `partly` row to "
     f"`enforced` citing only failing cases — the round-37 witness-picking shape), `git -C \"$S/lane\" add -A`, run C2 → V7 must be "
     f"DEFECT; then 4 more variants (row citing a non-violating case; tag duplicated; tag missing; wrong line). Also apply the derived "
     f"rule to the round-37 entry's map (see {BLD}/R38MapRetro*) and confirm the instruction.md:9 disagreement.",
     "VERDICT: v7-controls-<caught>/<total>"),
    ("F38MutC2Counter", "mutation-tester", ["calibration"],
     f"Mutation-test {C2} itself (copies in your clone): weaken V3 to any-row digest; V4 summary off-by-one tolerated; V7 derive "
     f"ignoring all-but-first violating case; V2 drop --rerun; V1 ignore extra files. For each, does any committed control in "
     f"{W}/claims/ or a cheap fixture of yours turn it red? Report which counter weaknesses have no killing control.",
     "VERDICT: c2-counter-mutants-<killed>/<n>"),
    ("F38ReopenRows", "critic", ["freshness", "coverage"],
     f"Re-open S115 and S116 live at the pin ({PIN}): `curl -sS <url> | sha256sum` vs the row anchor and {CAP}/SHA256SUMS; `sed -n "
     f"<line>p` vs each row's quote; also re-check upstream main and terminal-bench-2-1 `tasks/build-pmars` for grader drift.",
     "VERDICT: rows-<k>/2-quotes-<k>/2"),
    ("F38EntryQuotes", "reviewer", ["depth", "coverage"],
     f"Every `## Located quotes` row of {ENTRY}: verbatim at its cited capture line (sed -n), 3-25 words; every finding sentence: "
     f"backed by the receipt case it cites (observed verdict + tests letters). List each unsupported or misstated sentence with "
     f"file:line.",
     "VERDICT: entry-quotes-<k>/<n>-claims-unsupported-<m>"),
    ("F38CritOverclaim", "critic", ["calibration", "coverage"],
     f"Overclaims across round-38 prose: {ENTRY}, PROVINCE.md round-38 paragraph, SKILL.md build-provenance section, corpus/README.md "
     f"changes, SCORECARD/LOG round-38 sections. Each statement vs the receipt and frozen claims; class claims (vs 'probed instance') "
     f"and universal clauses flagged.",
     "VERDICT: overclaims-<n>"),
    ("F38CritTags", "critic", ["coverage", "calibration"],
     f"Contest the frozen `violates=` tags in {DRY}: for each case, is each tag defensible from instruction.md's text? Propose the "
     f"strongest alternative tagging and recompute V7's derived labels under it (script it); say which map rows would change. The "
     f"frozen tags stay — this is a limit, not an edit.",
     "VERDICT: tags-contestable-<n>-labels-change-<m>"),
    ("F38CritSeparability", "critic", ["calibration"],
     f"Separability: in one clone of {TIP} revert C2's package (entry, rows, README lines, receipt) and run C1; in another remove "
     f"plans/battery38 and run C2. Each predicate must still hold for the untouched claim. Paste outputs.",
     "VERDICT: separable-<yes|no>"),
    ("F38CritSkipControls", "critic", ["calibration"],
     f"Cheapest controls against the LANDED counters: (a) an informed filler entry reusing the receipt with false prose — does C2 "
     f"pass? (b) a battery38 whose fixtures each kill by a clause other than the advertised one — does C1 pass? Build both in your "
     f"clone; paste outputs; rank how much each counter alone proves.",
     "VERDICT: skip-controls-c1-<red|green>-c2-<red|green>"),
    ("F38NoHarmSweep", "executor", ["operability", "freshness"],
     f"No-harm sweep: on a clean clone of {TIP} re-run every command in {W}/integrate/measure-before.txt (or {W}/integrate/measure.sh) "
     f"plus the registered probes/gates listed in {L}/SKILL.md's registry that ran green at the freeze parent 21e6251b; compare. Any "
     f"new red "
     f"is a harm finding.",
     "VERDICT: no-harm-<green>/<n>-new-red-<k>"),
    ("F38CritNoHarmDiff", "critic", ["calibration"],
     f"`git -C {L} diff --numstat 21e6251b {TIP} -- SCORECARD.md LOG.md SKILL.md PROVINCE.md SHONEN.md corpus/` : any removed line in "
     f"lane-authored append-only docs? Any score moved without its claim? Any frozen file changed after e0a37853?",
     "VERDICT: no-harm-removed-lines-<n>"),
    ("F38AnchorFix", "executor", ["calibration", "operability"],
     f"Verify the D3 fix in plans/anchor_digest_check.py at {TIP}: tip `defects=0`; build the cross-row fixture (a row whose anchor "
     f"carries another row's real committed digest) in your clone → defect; the round-37 version (git show 3ea9a1d9.. or e0a37853:"
     f"plans/anchor_digest_check.py) → passes it. Paste outputs.",
     "VERDICT: anchor-cross-row-<caught|missed>"),
    ("F38LedgerTip", "executor", ["operability"],
     f"Verify the D4 fix: run plans/ledger_tip.py from a detached-HEAD `git clone --shared` of {TIP} and from a normal clone; expect "
     f"pass (or the declared exit-2 refusal), never `agree=NO`. Paste both.",
     "VERDICT: ledger-tip-detached-<ok|red>"),
    ("F38TipReceipts", "executor", ["operability", "freshness"],
     f"Re-run plans/tip_receipts.py at {TIP} on a clean clone; then tamper one byte of one receipt in the clone and re-run (must report "
     f"differ); check it honours TMPDIR/--work (strace -f -e trace=mkdir,openat or a TMPDIR under your scratch).",
     "VERDICT: tip-receipts-<k>/<n>-tamper-<caught|missed>"),
    ("F38RevQuality", "reviewer", ["calibration", "quality"],
     f"Review QUALITY.md Q28 and the round-38 erratum on corpus/knowledge/tb2-git-webserver-grader.md against "
     f"{L}/.ufo/waves/round-37/falsify/F37CritC2Map.md and the round-37 receipt: are the corrections right, complete, append-only? "
     f"Is Q28's check executable and shown able to fail?",
     "VERDICT: quality-<n>-defects"),
    ("F38RevLesson", "reviewer", ["calibration"],
     f"Review {LESSON}: every Gate/Mistakes row's pointer resolves (path:line, commit, receipt), the order-of-operations recurrence is "
     f"stated honestly, each fix 'shown able to fail' has a receipt. List defects with line numbers.",
     "VERDICT: lesson-<n>-defects"),
    ("F38RevScorecard", "reviewer", ["calibration"],
     f"Calibration of the self-report: compare SCORECARD.md/LOG.md round-38 text and SHONEN.md with observed repo state at {TIP} "
     f"(counts, hashes, verdicts, capability rows each with a passing demonstration). Count mismatches.",
     "VERDICT: self-report-mismatches-<n>"),
    ("F38ScoutMisroot", "scout", ["adjacency"],
     f"Misroot/scratch sweep: `git -C {F} status --porcelain --untracked-files=all` — any file a kengaku round-38 seat wrote at the fleet "
     f"root (content names kengaku/round 38/R38/F38)? Leftover dirs under {SCR}/ (du -sh each)? Report only; delete nothing.",
     "VERDICT: misroot-<n>-scratch-leftovers-<k>"),
    ("F38ConnClaims", "connector", ["calibration"],
     f"Cross-claim consistency: the same numbers (22 mutants, 22 cases, 7/15, S115/S116, hashes) across claims, SCORECARD, LOG, "
     f"lesson, entry, receipts; any drift between documents.",
     "VERDICT: cross-doc-drift-<n>"),
    ("F38ConnFrontier", "connector", ["coverage", "adjacency"],
     f"Frontier read: does corpus/README.md §Frontier and the coverage map at {TIP} now reflect four TB2 grader classes correctly, and "
     f"which sibling lanes (read-only /home/vgpnk/Projects/shokunin/*-shokunin) hold adjacent material the round should cite? Pointers.",
     "VERDICT: frontier-<ok|n-gaps>"),
    ("F38SentinelBattery", "sentinel", ["operability"],
     f"Security: battery38 fixtures own specs whose probe_cmd the gate executes; the probe compiles and runs host-built binaries. "
     f"Check for host writes outside scratch, network use, leftover processes after a full C1 + C2 run in your clone (ps, ss, find "
     f"-newer).",
     "VERDICT: sentinel-<n>-findings"),
    ("F38CritN21", "critic", ["calibration"],
     f"Attack the L1's N21 explanation: is the frozen `silence` direction of N21 (`sums.splitlines()` -> `sums.splitlines()[:1]` in "
     f"cmd_d5 of {GATE}) truly unreachable? Argue it from the code (is mutant DEFECT ⊇ reference DEFECT on every input?) and try to "
     f"BUILD a d5-line fixture where the reference prints D5 DEFECT and the mutant prints D5 ok (multi-line manifests, duplicate names, "
     f"digest collisions, unreadable capture). Then hand-run N21 outside the counter on plans/battery38/d5m.py's "
     f"`d5m-n21-manifest-row-2` and confirm the mirror kill. Report whether C1's honest stop is real or a missing fixture.",
     "VERDICT: n21-silence-<unreachable|reachable>"),
    ("F38MutDirection", "mutation-tester", ["calibration"],
     f"Mutation-test {L}/plans/mutant_direction_check.py (copies in your clone): make it ignore mirror; make it accept any observed "
     f"direction; make UNWITNESSED count as ok... For each, does the landed run (N21 MISLABELLED, exit 1) still distinguish? Also "
     f"relabel N21 to mirror in a scratch copy of {C1} and confirm the checker exits 0 and the counter kills 22/22 (this is a "
     f"diagnostic, never the frozen claim).",
     "VERDICT: direction-check-mutants-<caught>/<n>"),
    ("F38IndepProbe", "critic", ["coverage"],
     f"Independent probe reimplementation: without importing {PROBE}, write your own minimal runner (different sandbox flags or "
     f"none — an unprivileged chroot-free run with PATH tricks is fine) for 8 cases (canned-shape, canned-x11-linked, canned-x11-dlopen,"
     f" results-trailing-text, canned-exit-nonzero, path-split, debian-is-file, c-is-dir) and compare per-test letters with {RCPT}.",
     "VERDICT: indep-probe-agree-<k>/8"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 38 wave 2 (falsify) item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r38 wave 2 (falsify)"})
    assert len({i["name"] for i in items}) == len(items)
    spec = {"wave": "kengaku-r38-falsify", "milestone": "kengaku round 38 wave 2: falsify C1/C2 and the frontier work",
            "reportDir": ".ufo/waves/round-38/falsify", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/falsify-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c))
    print(f"attack={c['reviewer'] + c['critic'] + c['mutation-tester']}/{len(items)} "
          f"flash={c['executor'] + c['scribe'] + c['critic'] + c['sentinel']}/{len(items)}")


main()
