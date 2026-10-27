#!/usr/bin/env python3
"""Renders .ufo/waves/round-46/w2-spec.json (v1 wave 2 — falsify, policy v1 band 32-64). L1 KengakuR46.
Every item attacks one thing wave 1 produced and the L1 landed at TIP; every item names what it attacks."""
import json
import pathlib
import sys
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-46"
B = f"{W}/w2"
SCR = "/fast/scratch/hyaku/kengaku-r46"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
TIP = sys.argv[1]
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
BASE = "64ba8385ea10af1b78d367dcb242b92d97062af7"
CLAIMS = f"{L}/plans/round-46-claims.md"
CL = f"{W}/claims"
ENV = f"{CL}/envelope.sh"
C1V = f"{L}/plans/round46_c1_verify.py"
C2V = f"{L}/plans/round46_c2_verify.py"
C3V = f"{L}/plans/round46_c3_verify.py"
ALC = f"{L}/plans/anchor_line_check.py"
FENCE = f"{L}/plans/fixture_fence.py"
K44 = f"{L}/plans/round44_c1_verify.py"
C45_1 = f"{L}/plans/round45_c1_verify.py"
C45_2 = f"{L}/plans/round45_c2_verify.py"
SRC = f"{L}/corpus/SOURCES.md"
E45 = f"{L}/corpus/knowledge/tb2-password-recovery-grader.md"
E46 = f"{L}/corpus/knowledge/tb2-polyglot-c-py-grader.md"
CAP46 = f"{L}/corpus/evidence/round46/tb2-polyglot-c-py"
PROBE = f"{L}/plans/polyglot_c_py_probe.py"
RCPT = f"{L}/corpus/evidence/round46/polyglot-c-py-probe.txt"
RAW46 = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/polyglot-c-py"
RAW45 = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/password-recovery"
LESSON = f"{L}/corpus/lessons/round-46.md"
INTEG = f"{W}/integrate"

HOST_RULE = ("Host safety: run any fixture build, counter run or probe that can write files inside a bwrap sandbox in which "
             "`/home/vgpnk/.local/bin` is read-only (the envelope does this). Never write to a shared PATH directory, `/usr`, "
             "`/etc`, or `$HOME` outside scratch.")
ENVELOPE = (f"Envelope for every counter/fixture/probe run: `{ENV} \"$S/env\" <command...>`; paste its ENVELOPE lines; exit 4 + "
            f"`INVALID` means the measurement does not count.")
SCRATCH = (f"Scratch rule: S={SCR}/<YourSeatName>; mkdir -p \"$S\"; export TMPDIR=\"$S\"; pass \"$S\" as --work. Delete it before you "
           f"finish with `python3 {L}/plans/scratch_guard.py safe-rm {SCR} <YourSeatName> \"$S\"`. Never delete {SCR}, its "
           f"`.ROUND-ROOT-SENTINEL` or another seat's dir. A /tmp or scratch path is never evidence — copy receipts into your report "
           f"subdir first (no file over 1 MiB).")
CLONE = (f'Clone rule: git clone -q --no-local {L} "$S/lane" && git -C "$S/lane" checkout -q {TIP}; verify `git -C "$S/lane" '
         f'rev-parse --show-toplevel` equals "$S/lane" and `git -C "$S/lane" rev-parse HEAD` equals {TIP}, and put that HEAD line in '
         f'every receipt (closure D3: a receipt names the revision it measured). Any other fixture repo: D=$(mktemp -d -p "$S") '
         f'&& git -C "$D" init -q and every git call names -C "$D". Never commit outside such scratch repos.')

CONTEXT = f"""# Goal
kengaku round 46 (hyaku run 9, 2026-10-27), WAVE 2 of two v1 waves — FALSIFY. Lane repo: {L}; landed TIP `{TIP}`.
Wave 1 built; the L1 integrated and landed three claims frozen in {CLAIMS} (read it in full, incl. the stage-2 `Freeze
amendments` paragraph). Your job: attack ONE named item and report what survives. Every item names what it attacks.
- C1 calibration: {FENCE} (repaired) judged by {C1V} (pinned at stage 2; plans/refusals46/, plans/sealed46/).
- C2 depth: {C2V} + gate {ALC}; superseding rows S157-S165 in {SRC}; repaired {E45}.
- C3 coverage: {E46}, rows from S166, captures {CAP46}/, probe {PROBE}, receipt {RCPT}, counter {C3V}.
Frozen and never edited by any seat: everything under {L}. Integration receipts: {INTEG}/.

# Host-safety rule (binding)
{HOST_RULE}
{ENVELOPE}

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Your report is {B}/<YourSeatName>.md; receipts go under {B}/<YourSeatName>/. Every seat MUST leave its report.
- {SCRATCH}
- Write ONLY inside {B}/<YourSeatName>.md, {B}/<YourSeatName>/ and your scratch dir. NEVER edit any lane file; never write into
  {F} (fleet root), sibling lanes, the lane's jj state or Git index; never run a mutating git/jj command in the lane. Seats never
  commit or push anywhere.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide:
  install via `uv tool` / `npx` / an official binary into ~/.local/bin (outside any bwrap run), or install nothing and say so.
  Never run pacman -Sy/-Syu/-U/-R, never name an already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task`.
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location and is <= 25 words.
  Do not fabricate output; if something cannot be fetched or run, say so.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""

HO = (f"A held-out module is one Python file in the contract of {L}/plans/refusals46/f7_commondir.py (read two refusals46 files "
      f"and {K44} `builder_source`/`Ctx`). Write NEW hostile modules (not variants of plans/refusals46/ or plans/sealed46/ — read "
      f"both lists first) against the LANDED fence {FENCE} @ {TIP}, run them with the pinned counter's own machinery "
      f"({C1V}: its build and fence-run functions, one module at a time, or the counter with `--refusals` pointed at a scratch dir), "
      f"and report per module LEAKED / READ / clean / HUNG with receipts. Count: modules written, admitted, read.")

ITEMS = [
    # C1
    ("R46W2C1Rerun", "reviewer", ["calibration"],
     f"Re-run the frozen C1 counter `python3 {C1V} --lane \"$S/lane\" --work \"$S/w\"` on a clean clone at TIP inside the envelope, "
     f"twice; compare every summary line with {INTEG}/tip-c1.txt and with the predicate in {CLAIMS}; `sha256sum -c` the frozen "
     f"digests named in the claims' stage-2 amendment.", "VERDICT: c1-rerun-predicate-<pass|fail>-matches-L1-<yes|no>"),
    ("R46W2C1Forge", "critic", ["calibration"],
     f"Forge a pass: write fences that inspect nothing (or key on a name/structure/timing/env channel) and try to make {C1V} print "
     f"`PREDICATE C1 pass`; try every round-45 bypass B1-B7 (.ufo/waves/round-45/w1/R45CriticPredicate.md) against the pinned "
     f"counter and any new channel (sibling stat, argv shape, fixture count, order). Receipts per attempt.",
     "VERDICT: c1-forged-pass-<n>-of-<m>"),
    ("R46W2C1HoConfig", "critic", ["calibration"], f"{HO} Family: git configuration surfaces.", "VERDICT: heldout-config-<n>-admitted-<a>-read-<r>"),
    ("R46W2C1HoPaths", "critic", ["calibration"], f"{HO} Family: filesystem shape (links, special files, names).",
     "VERDICT: heldout-paths-<n>-admitted-<a>-read-<r>"),
    ("R46W2C1HoStore", "critic", ["calibration"], f"{HO} Family: git store indirection and refs.",
     "VERDICT: heldout-store-<n>-admitted-<a>-read-<r>"),
    ("R46W2C1HoArgv", "mutation-tester", ["calibration"], f"{HO} Family: argv/env tokens for `anchor` and `order`.",
     "VERDICT: heldout-argv-<n>-admitted-<a>-read-<r>"),
    ("R46W2C1HoHonest", "reviewer", ["calibration"],
     f"Over-refusal check: write 6-10 NEW honest fixtures (plain repos a lane tool would legitimately see: packed refs after gc, "
     f"annotated tags, a detached HEAD, a merge commit, a repo with a .gitignore, a long history) and report how many the landed "
     f"fence refuses — a fence that refuses all novelty passes refusal legs but is useless. Run through {C1V}'s machinery.",
     "VERDICT: honest-novel-<n>-refused-<k>"),
    ("R46W2C1MutFence", "mutation-tester", ["calibration"],
     f"Mutation-test the landed fence {FENCE}: 15+ single-edit mutants (drop each check, invert a comparison, follow a symlink, "
     f"widen an allowlist); for each, does the pinned counter {C1V} print a fail (which line)? Table mutant -> caught-by.",
     "VERDICT: fence-mutants-caught-<k>/<n>"),
    ("R46W2C1MutCounter", "mutation-tester", ["calibration"],
     f"Mutation-test the pinned counter {C1V} (closure D5: round 45's C1-instrument mutation item went unattacked): mutate the name "
     f"hiding, tamper detection, root-wide counting, stat tracing, pending-open decode, exit-status verdict; does any frozen control "
     f"receipt in {CL}/ (re-run per mutant) or the landed fence catch it? Table mutant -> killed-by.",
     "VERDICT: c1-counter-mutants-killed-<k>/<n>"),
    ("R46W2C1Intent", "reviewer", ["calibration"],
     f"Non-author source review of the landed fence {FENCE} against its docstring and the advertisement (SCORECARD round-46 C1 "
     f"cell, capability rows): does it refuse what it cannot prove safe, or does it name attack classes? Any check keyed to a "
     f"refusals46/sealed46 module rather than a property? Cite lines.", "VERDICT: fence-intent-defects-<n>"),
    ("R46W2C1Sealed", "reviewer", ["calibration"],
     f"Audit the sealed set plans/sealed46/: digests vs the stage-2 pin, each module's base-fence verdict receipt, whether any "
     f"fence-writing seat of wave 1 could have read it (read .ufo/waves/round-46/w1/R46ExecC1Fence*.md for paths they cite), and "
     f"whether any sealed module duplicates a refusals46 class.", "VERDICT: sealed-modules-<n>-integrity-defects-<k>"),
    ("R46W2C1Advert", "critic", ["calibration"],
     f"Calibration check of the lane's own text: does SCORECARD.md round-46 C1 cell, the capability table, {LESSON} and the fence "
     f"docstring claim more than the receipts show (held-out results, limits like io_uring)? Count overclaims with the refuting command.",
     "VERDICT: c1-self-assessment-overclaims-<n>"),
    # C2
    ("R46W2C2Rerun", "reviewer", ["depth"],
     f"Re-run `python3 {C2V} --lane \"$S/lane\"` and `python3 {ALC} --selftest` on a clean clone at TIP; compare with "
     f"{INTEG}/tip-c2.txt; re-run the five frozen controls in {CL}/control-c2-*.txt per their headers.",
     "VERDICT: c2-rerun-predicate-<pass|fail>-controls-failing-<k>/5"),
    ("R46W2C2Rows", "reviewer", ["depth"],
     f"Re-open live every URL of rows S157-S165 in {SRC} (curl, sha256 = registry) and check every cell: quote verbatim at the cited "
     f"line, range, word count, kind, `teaches` opening `supersedes S1NN —` and saying only what the source says, status/used-by; and "
     f"the old rows' mutable-cell changes logged old->new in {LESSON}.", "VERDICT: c2-rows-verified-<k>/9-defects-<n>"),
    ("R46W2C2Entry", "reviewer", ["depth"],
     f"Review the repaired {E45}: is the `## Errata (round 46)` true and complete (each item vs the round-45 closure §2/§3), is the "
     f"predictor exact against the captured grader beyond the 16 frozen states (run 200 random newline/whitespace states in a bwrap "
     f"sandbox), do the prose sentences match the code, are source ranges right?", "VERDICT: c2-entry-defects-<n>-predictor-disagree-<k>"),
    ("R46W2C2Bypass", "critic", ["depth"],
     f"Find a tree that passes {C2V} while the repair is false: cell defects leg A cannot see, a predictor tuned to the 16 states, "
     f"errata tokens without corrections. Demonstrate on clones of TIP.", "VERDICT: c2-bypasses-<n>-verdict-changing-<k>"),
    ("R46W2C2Mut", "mutation-tester", ["depth"],
     f"Mutation-test {ALC} and {C2V} (closure D5: round 45's C2-check mutation item went unattacked) — single-edit mutants; is each "
     f"killed by --selftest, by a frozen control, or by the landed tree? Table.", "VERDICT: c2-mutants-killed-<k>/<n>"),
    ("R46W2NoHarm", "reviewer", ["depth", "operability"],
     f"No-harm set at TIP on a clean clone: `python3 {C45_2} --lane .` (must stay `checks=11 defects=0`), `python3 {C45_1} --lane .` "
     f"(report its verdict with the repaired fence and say whether a change is expected), `python3 {L}/plans/round44_c1_verify.py` and "
     f"`round44_c2_verify.py` per their docstrings, `python3 {L}/plans/routed_open.py`, `python3 {L}/plans/round_close.py --lane . "
     f"--round 45`, `python3 {L}/plans/anchor_digest_check.py --lane .`, census. Compare each with base {BASE}.",
     "VERDICT: noharm-legs-<n>-red-at-tip-<k>-red-at-base-<b>"),
    # C3
    ("R46W2C3Rerun", "reviewer", ["coverage"],
     f"Re-run `python3 {C3V} --lane \"$S/lane\"` on a clean clone at TIP inside the envelope, twice; compare with {INTEG}/tip-c3.txt; "
     f"re-run the probe `python3 {PROBE} --lane \"$S/lane\"` and diff with {RCPT}.", "VERDICT: c3-rerun-predicate-<pass|fail>-probe-equal-<yes|no>"),
    ("R46W2C3Rows", "reviewer", ["coverage"],
     f"Re-open live every C3 row (S166..) URL at the pin ({RAW46}/…): sha256, quote verbatim at the cited line, range, word count, "
     f"kind, tier scope, teaches faithful; Gate quotes in {LESSON}.", "VERDICT: c3-rows-verified-<k>/<n>-defects-<d>"),
    ("R46W2C3Entry", "reviewer", ["coverage"],
     f"Non-author review of {E46}: every claim vs the captured sources and the receipt; requirement map labels derived from cases; "
     f"mechanism lines decisive; negative space honest; class vs the lane's eleven exemplars.", "VERDICT: c3-entry-defects-<n>"),
    ("R46W2C3Predictor", "critic", ["coverage"],
     f"Attack C3's held-out predictor leg in {C3V}: write lint-clean predictors that memorize (lookup shapes, call-order, keyed "
     f"tables per .ufo/waves/round-45/a3w1/R45CritV11Bypass.md) and see if any passes; also run the entry's predictor on extra "
     f"states you generate.", "VERDICT: c3-predictor-bypasses-<n>"),
    ("R46W2C3Cases", "critic", ["coverage"],
     f"Attack the probe's case table {PROBE} + receipt {RCPT}: are cases tuned to verdicts rather than mechanisms, is any instruction "
     f"requirement untested, does any case's recipe fail to produce the state it names (inspect the sandbox output), is the "
     f"non-idempotence finding real (re-grade the same state)?", "VERDICT: c3-case-defects-<n>"),
    ("R46W2C3Filler", "critic", ["coverage"],
     f"Attack V13/the filler control in {C3V}: build the strongest do-nothing or echo package (right shapes, copied receipts, "
     f"plausible rows) and try to reach `PREDICATE C3 pass`.", "VERDICT: c3-filler-forged-pass-<yes|no>-legs-fooled-<k>"),
    ("R46W2C3Mut", "mutation-tester", ["coverage"],
     f"Mutation-test {C3V}: single-edit mutants per V leg; killed by the landed package, a control, or nothing? Table.",
     "VERDICT: c3-mutants-killed-<k>/<n>"),
    ("R46W2C3Sandbox", "sentinel", ["coverage", "safety"],
     f"Audit the probe sandbox as landed in {PROBE}: run 3 hostile main.py.c programs (write outside /app, network, fork bomb, huge "
     f"output) through its sandbox function (not the receipt cases) and report containment; check HOME/~/.local writes.",
     "VERDICT: c3-sandbox-escapes-<n>"),
    ("R46W2C3Oracle", "executor", ["coverage"],
     f"Independent replication: without reading the probe's recipes, write your own minimal harness that runs the captured grader "
     f"({CAP46}/test_outputs.py) on 4 states (oracle solve.sh output, lookup-table polyglot for 42/10/0, extra file, leftover cmain) "
     f"and compare verdicts with {RCPT}.", "VERDICT: c3-independent-verdicts-agree-<k>/4"),
    # frontier / calibration bookkeeping
    ("R46W2Census", "reviewer", ["coverage"],
     f"Run `{F}/scripts/sources-census.sh validate --root {F} kengaku` at TIP (exit code + full output) and compare with "
     f"{CL}/census-before.txt; row counts before/after `git -C {L} show <rev>:corpus/SOURCES.md | grep -cE '^ {{0,3}}\\| *S[0-9]{{3}}'`.",
     "VERDICT: census-exit-<rc>-rows-<before>-to-<after>"),
    ("R46W2Lesson", "reviewer", ["calibration"],
     f"Review {LESSON}: `## Mistakes` rows each with class/evidence/captured-by/fix shown able to fail; `## Gate` with URL, access "
     f"date, ≤25-word located quote for every NEW row (closure D2), ≥1 admit and ≥1 reject; old->new log of mutable-cell changes.",
     "VERDICT: lesson-defects-<n>"),
    ("R46W2Scorecard", "critic", ["calibration"],
     f"Calibration attack on {L}/SCORECARD.md round-46 section and LOG.md round-46 entry: every number vs its receipt (re-run the "
     f"command), every verdict vs the wave-2 reports on disk, every receipt names the revision measured (closure D3). Count "
     f"mismatches with refuting commands.", "VERDICT: scorecard-mismatches-<n>"),
    ("R46W2LogAppend", "reviewer", ["calibration"],
     f"Attack `plans/log_appendonly.py`: run it on the lane at TIP and on fixture repos (edit, delete, reorder, CRLF change, whitespace-"
     f"only edit, rename of LOG.md); does it catch each? Is the round-46 D1 correction entry in LOG.md append-only and accurate "
     f"(`git -C {L} diff {BASE} {TIP} -- LOG.md` shows additions only)?", "VERDICT: log-appendonly-misses-<n>-d1-entry-<ok|defect>"),
    ("R46W2Conn", "connector", ["calibration", "depth", "coverage"],
     f"Cross-claim pattern finder over the landed round: which wave-2 findings share a root cause across C1/C2/C3, and which one "
     f"SKILL.md or QUALITY.md line would prevent the class next round? Read the other w2 reports that exist when you run.",
     "VERDICT: cross-claim-patterns-<n>"),
]

FLASH = {"executor", "labrat", "scribe", "sonic", "simplifier", "revenger", "sentinel"}
ATTACK = {"reviewer", "critic", "mutation-tester", "labrat"}


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 46 wave-2 item {name} ({role}) — attacks the landed round at {TIP}.\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r46 wave 2 (falsify, v1)"})
    assert len({i["name"] for i in items}) == len(items), len(items)
    c = Counter(i["role"] for i in items)
    attack = sum(n for r, n in c.items() if r in ATTACK)
    assert 32 <= len(items) <= 64, len(items)
    assert attack * 4 >= len(items)
    spec = {"wave": "kengaku-r46-w2", "milestone": "kengaku round 46 wave 2: falsify the landed C1/C2/C3 and the round bookkeeping",
            "reportDir": ".ufo/waves/round-46/w2", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/w2-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    print(len(items), dict(c), f"attack={attack}/{len(items)}")


main()
