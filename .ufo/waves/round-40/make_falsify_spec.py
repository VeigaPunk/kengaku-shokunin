#!/usr/bin/env python3
"""Renders .ufo/waves/round-40/falsify-spec.json (wave 2 of 2, policy v1): attacks on what wave 1 and the L1 landed."""
import json
import pathlib
import subprocess
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-40"
B = f"{W}/build"
FX = f"{W}/falsify"
SCR = "/fast/scratch/hyaku/kengaku-r40"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
TIP = subprocess.run(["git", "-C", L, "rev-parse", "refs/heads/master"], capture_output=True, text=True, check=True).stdout.strip()
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
CAP = f"{L}/corpus/evidence/round40/tb2-db-wal-recovery"
RCPT = f"{L}/corpus/evidence/round40/db-wal-probe.txt"
DRY = f"{L}/corpus/evidence/round40/db-wal-dry-cases-freeze.txt"
C1 = f"{L}/plans/round40_c1_verify.py"
C2 = f"{L}/plans/round40_c2_verify.py"
PROBE = f"{L}/plans/db_wal_probe.py"
CLAIMS = f"{L}/plans/round-40-claims.md"
ENTRY = f"{L}/corpus/knowledge/tb2-db-wal-recovery-grader.md"
LES = f"{L}/corpus/lessons/round-40.md"
BAT = f"{L}/plans/battery40"
FREEZE = "bbb109505670192035ef63d7c8b37733e99fa1a3"
FIRST = "055748f78a3335434f2a4070bb3fb1cf8d0eba1f"
MEAS = f"{W}/integrate/measure-final.txt"
SANDBOX = (f'HOST-SAFETY RULE (orchestrator ruling, round 40): run every C1 counter invocation, every battery module and every '
           f'attack module ONLY inside `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 '
           f'--proc /proc --unshare-pid --die-with-parent <cmd>` (~/.local/bin read-only — uv stays usable, the ledger\'s R35-D1 check '
           f'needs it —; no user-bus, so systemd-run fails; L1-tested), with `--lane` on your own scratch clone. Never '
           f'write under $HOME outside your scratch, under /usr, /etc, /run/user, or into ANY directory on PATH; never start '
           f'`systemd-run`, cron, at or any user service. Never execute {B}/R40CritC1Counter/crit_git_shim.py or '
           f'crit_ledger_selfread.py (neutralized evidence: a wave-1 seat wrote a git shim into the shared ~/.local/bin and broke '
           f'other lanes\' runs).')
CLONE = (f'Fixture rule: S={SCR}/<YourSeatName>; mkdir -p "$S"; trap \'rm -rf -- "$S"\' EXIT; export TMPDIR="$S"; '
         f'git clone -q --no-local {L} "$S/lane" && git -C "$S/lane" checkout -q {TIP}; verify `git -C "$S/lane" rev-parse '
         f'--show-toplevel` equals "$S/lane" before any write; every git call names -C "$S/lane"; never commit. Any other '
         f'fixture repo: D=$(mktemp -d -p "$S") && git -C "$D" init -q, every git call names -C "$D". Remove "$S" before you '
         f'finish (copy receipts into your report dir first).')

CONTEXT = f"""# Goal
kengaku round 40 (hyaku run 9, 2026-10-26), WAVE 2 of 2 (FALSIFY). Lane repo: {L}. Attack what wave 1 and the L1 landed,
measured at lane tip {TIP} (branch master). Every item names what it attacks; a finding is a receipt, not an opinion.
Frozen claims: {CLAIMS} (freeze {FREEZE}; first recorded probe run {FIRST}). Landing measurement on a clean clone of the
tip: {MEAS}. Lesson: {LES}. Wave-1 reports: {B}/*.md.
- C1 calibration: 21 frozen mutants of the three tripwire tools (plans/anchor_digest_check.py, plans/ledger_tip.py,
  plans/order_check.py — unedited) in {C1}; battery {BAT}/ (7 modules: a_tok A01-A03, a_row A06/A08/A09, a_bind A15/A17/A27,
  a_man A21/A22, l_rows L05/L06/L14/L15, l_refuse L01/L11/L21, o_gate O04/O12/O14). Frozen predicate: `PINS total=3
  mismatched=0`, `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=21 killed=21 survived=0 invalid=0
  null_detected=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`. Wave 1 showed the frozen counter is gameable by a
  dishonest battery ({B}/R40CritC1Counter.md: A1 a ledger check body that reads its own program text, A2 a PATH git shim,
  A4 relative argv + symlink, A5 `.lock` names the fingerprint skips; {B}/R40SentinelCounter.md: whole host fs writable,
  cross-module fixture forgery; {B}/R40RevCounters.md F1-F6), so admission rests on the frozen predicate PLUS non-author
  review that the landed battery uses none of these.
- C2 coverage: TB2 `db-wal-recovery` @ {PIN} admitted as {ENTRY} (S119 tests/test_outputs.py, S120 instruction.md, S121
  TB2.1 PR #3 tier B; captures {CAP}/; receipt {RCPT}; frozen dry table {DRY}; counter {C2}, predicate `checks=7 defects=0`,
  `PREDICATE C2 pass`).
- Routed/frontier landed this round: plans/tip_receipts.py (derives a receipt's probe from its stem), plans/round_close.py
  (invokes order_check + census), SKILL registry rows + round-40 addendum + decision section, PROVINCE round-40 paragraph,
  README index/coverage/frontier/evidence lines, S046/S052 anchor notes.
- {SANDBOX}

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


def rev(name, module, mids):
    return (name, "reviewer", ["calibration"],
            f"Non-author honesty review of {BAT}/{module}.py (targets {mids} of {C1}). Read every line: does each fixture build an "
            f"input that exhibits the advertised behaviour honestly (the tool's own docstring sentence in the mutant's `adv` cell), "
            f"or does it rely on anything the wave-1 attacks used (reading the tool or its own program text at run time, writing "
            f"outside d — HOME, PATH dirs, other modules' fixture dirs —, relative argv tokens or symlinks pointing out of d, "
            f"`.lock`/`.git/index` names the fingerprint skips, phase detection, a bare-string build() return)? Run the module "
            f"under the HOST-SAFETY sandbox: `python3 {C1} --lane \"$S/lane\" --battery-dir <dir holding only this module> --only "
            f"{mids} --work \"$S/w\"` and paste FIXTURE/MUTANT lines; inspect one built fixture tree (copy the build logic into a "
            f"scratch script) and diff it against the lane. Verdict honest / dishonest per fixture with file:line.",
            f"VERDICT: battery-{module}-honest-<k>/<n>")


ITEMS = [
    ("F40C1Rerun", "executor", ["calibration"],
     f"Re-measure C1 at the tip on two clean clones under the HOST-SAFETY sandbox: `python3 plans/round40_c1_verify.py --lane . "
     f"--work \"$S/w1\"` with PYTHONHASHSEED=0 --jobs 1, and again with PYTHONHASHSEED=77 --jobs 8; diff the two receipts and diff "
     f"each with the C1 block of {MEAS}. Then the do-nothing control (remove plans/battery40 in a clone) and one module removed "
     f"at a time (7 runs): which mutants flip to SURVIVED (load-bearing table).",
     "VERDICT: c1-rerun-<pass|fail>-byte-equal-<yes|no>-loadbearing-<k>/7"),
    rev("F40RevBatTok", "a_tok", "A01,A02,A03"),
    rev("F40RevBatRow", "a_row", "A06,A08,A09"),
    rev("F40RevBatBind", "a_bind", "A15,A17,A27"),
    rev("F40RevBatMan", "a_man", "A21,A22"),
    rev("F40RevBatLRows", "l_rows", "L05,L06,L14,L15"),
    rev("F40RevBatLRefuse", "l_refuse", "L01,L11,L21"),
    rev("F40RevBatOrder", "o_gate", "O04,O12,O14"),
    ("F40MutBattery", "mutation-tester", ["calibration"],
     f"Fixture-level mutants of {BAT}/*.py (in a scratch copy, run with --battery-dir under the HOST-SAFETY sandbox): for each "
     f"module break the one edit that makes each fixture exhibit its behaviour (e.g. keep the token lowercase, keep 3-space "
     f"indent, keep 11 cells, drop the gitlink, name the claims file correctly, keep the ledger row closed) and confirm the "
     f"targeted mutant flips to SURVIVED or the fixture goes WRONG. Report caught/total per module.",
     "VERDICT: battery-fixture-mutants-caught-<k>/<n>"),
    ("F40XMutAnchor", "mutation-tester", ["calibration"],
     f"Near-variant mutants of plans/anchor_digest_check.py NOT in the frozen list (e.g. other bound edits, other class "
     f"emissions, erratum clauses, binding routes 1 and 3, `--verbose` path): write >=10 single-replacement mutants, run them "
     f"against battery40 + the tip run (copy the counter to scratch and swap its MUTANTS table, HOST-SAFETY sandbox), and list "
     f"survivors with a witness input for each — round-41 candidates; never edit the lane.",
     "VERDICT: anchor-xmut-killed-<k>/<n>"),
    ("F40XMutLedgerOrder", "mutation-tester", ["calibration"],
     f"As F40XMutAnchor for plans/ledger_tip.py and plans/order_check.py: >=10 near-variant mutants not in the frozen list "
     f"(summary counters, kind labels, REF AUDIT/BIND lines, freeze-contains-receipt, receipt-before-claims, scan bounds), run "
     f"against battery40 in a scratch copy of the counter under the HOST-SAFETY sandbox; list survivors with witnesses.",
     "VERDICT: ledger-order-xmut-killed-<k>/<n>"),
    ("F40CritC1Count", "critic", ["calibration"],
     f"Recount the calibration denominator: for each of the 21 `adv` cells in {C1} classify direct / indirect / not-advertised "
     f"against the cited file:line (wave-1 {B}/R40CritClaims.md §1 says 13/4/4); state the before→after count the report may "
     f"claim (standing counter: before {W}/claims/control-c1-nothing.txt, after {MEAS}) and whether the witness kills "
     f"({W}/claims/witness-run.txt, 7) change the before. Check the lesson's and SCORECARD's wording against your count.",
     "VERDICT: c1-count-direct-<d>-indirect-<i>-unadvertised-<u>"),
    ("F40SentinelBattery", "sentinel", ["operability"],
     f"Security scan of {BAT}/*.py and {W}/claims/witness/*.py: writes outside the fixture dir, PATH/HOME/env use, network, "
     f"subprocesses left running, git config that executes code. Run each module once under the HOST-SAFETY sandbox with "
     f"`strace -f -e trace=openat,execve,connect` (or `ls -lR` before/after of $HOME/.local/bin, ~/.config, /run/user) and report "
     f"every path written outside the module's fixture root.",
     "VERDICT: battery-security-<n>-findings"),
    ("F40CritCounterLimits", "critic", ["calibration", "operability"],
     f"The wave-1 counterexamples ({B}/R40CritC1Counter.md A1/A2/A4/A5, {B}/R40SentinelCounter.md F1-F5, {B}/R40RevCounters.md "
     f"F1-F6): for each, (1) does any LANDED battery40 module use that vector (grep + read), (2) what the smallest counter "
     f"repair is (clean PATH, `--ro-bind / /` with only the fixture root writable as kumitate's cap-run.mjs does, content "
     f"fingerprint, per-module isolation, type check of build() return) — draft it as a patch against a SCRATCH copy of the "
     f"counter and show the A2/A5 attack re-run REDS under the patched copy inside the HOST-SAFETY sandbox (rebuild the "
     f"attacks with SHIM_DIR under your scratch, never ~/.local/bin). Route-to-round-41 list.",
     "VERDICT: counter-limits-used-by-landed-<k>-repairs-drafted-<n>"),
    ("F40NoHarmC1", "critic", ["calibration"],
     f"No-harm at the tip on a clean clone: round-37/38/39 C1 counters (plans/round3{{7,8,9}}_c1_verify.py) and C2 counters "
     f"(round36-39) print what {MEAS} says and what the round-39 closure recorded (r37 killed=55 pass, r38 killed=21 survived=1, "
     f"r39 killed=7 pass, C2s pass); plans/anchor_digest_check.py and plans/ledger_tip.py green at the tip; `git diff "
     f"d3a6277f {TIP} -- plans/battery37 plans/battery38 plans/battery39 plans/round3*_verify.py plans/anchor_digest_check.py "
     f"plans/ledger_tip.py plans/order_check.py plans/pkg_gate.py` empty.",
     "VERDICT: no-harm-c1-<ok|n-harms>"),
    ("F40C2Rerun", "executor", ["coverage", "calibration"],
     f"Re-measure C2 at the tip: `python3 plans/round40_c2_verify.py --lane . --work \"$S/w\"` (create $S/w first) on a clean "
     f"clone; the probe three times (plain, `env -i PATH=/usr/bin:/bin HOME=$S`, PYTHONHASHSEED=1) and cmp each with {RCPT}; "
     f"`--dry` cmp {DRY}; `(cd {CAP} && sha256sum -c SHA256SUMS)`.",
     "VERDICT: c2-rerun-<pass|fail>-probe-byte-equal-<k>/3"),
    ("F40ReopenRows", "reviewer", ["freshness", "coverage"],
     f"Re-open S119, S120 (raw URLs at {PIN}, sha256 vs the row and the capture, quote at its line) and S121 (gh api "
     f"repos/harbor-framework/terminal-bench-2-1/pulls/3: state, merged, the §Reasoning quote) live; check each row's 11 cells, "
     f"tier, used-by, recheck; check S046/S052's appended notes against the live Python 3.15 docs.",
     "VERDICT: rows-reopened-<ok>/5"),
    ("F40EntryQuotes", "critic", ["depth", "calibration"],
     f"Verify every quote in {ENTRY} (located-quotes table and §Prior art) verbatim at its cited line/location and 3-25 words; "
     f"every finding's case ids and letters against {RCPT}; every `:line` reference against the captures. List unsupported "
     f"sentences with the smallest correction.",
     "VERDICT: entry-quotes-<ok>/<n>-unsupported-<k>"),
    ("F40CritOverclaim", "critic", ["calibration"],
     f"Overclaim hunt across the round-40 C2 text: {ENTRY}, the README index row/coverage bullet/frontier sub-bullet/evidence "
     f"lines, the PROVINCE round-40 paragraph, the SKILL 'Database-recovery TB2 grader — round 40' section and registry rows. "
     f"Compare each claim with the receipt and wave-1 critics ({B}/R40CritProbe.md D1-D8): regrade wording, fix-wal label, "
     f"wrong-key confound, 0-byte WAL, 'never opens' vs 'hand-typed with wrong values'. List overclaims with location.",
     "VERDICT: overclaims-<n>"),
    ("F40MapControl", "mutation-tester", ["calibration"],
     f"Red-control the requirement map: in a clone, flip each of the six map labels, cite a non-violating case, drop a row, "
     f"duplicate a tag, change a line number; run {C2} each time — V7 must red. Report caught/total.",
     "VERDICT: map-controls-red-<k>/<n>"),
    ("F40IndepProbe", "critic", ["coverage"],
     f"Independently re-run the four non-frozen cases the entry cites from {B}/R40CritProbe.md (exact `truth` export at the "
     f"default path; the same after deleting main.db and main.db-wal; XOR 0x42 + read-only extraction; XOR 0x43 + read-only "
     f"extraction) in a scratch copy of {PROBE}; predict first, run, report letters and /app end-state digests.",
     "VERDICT: indep-extra-agree-<k>/4"),
    ("F40CritSkill", "critic", ["depth"],
     f"Verify every row of the SKILL.md 'Database-recovery TB2 grader — round 40' decision table and the five new registry rows "
     f"(order-check, round39-c1-audit, round40-c1-mutants, round40-c2, db-wal-probe) by running or reading what each cites; "
     f"count verified / wrong.",
     "VERDICT: skill-rows-verified-<k>/<n>"),
    ("F40CritPriorArt", "critic", ["novelty", "coverage"],
     f"Attack the entry's §Prior art: re-open TB2.1 PR #3, terminal-bench #2218's comment, harbor #3607 and the sqlite.org "
     f"pages; is each quote located and ≤25 words; is 'TB2.1 carries the same task bytes' true (hash the three files on "
     f"terminal-bench-2-1 main); is the claim 'permissiveness not reported' honest (search once more: gh search issues/prs, "
     f"the zai-org verified fork); does any opened source already report 22/33 pinned cells.",
     "VERDICT: prior-art-attack-<n>-defects"),
    ("F40TipReceipts", "executor", ["operability", "freshness"],
     f"Attack the landed plans/tip_receipts.py: full run at the tip on a clean clone (`--work \"$S/w\"`), `--list` (every "
     f"`origin=derived` mapping correct?), a fixture repo where a receipt stem collides with two scripts or a `-first-run` "
     f"sibling exists, tamper controls on every equal receipt. Any previously-equal receipt changed status vs {W}/integrate/"
     f"measure-baseline.txt?",
     "VERDICT: tip-receipts-attack-<n>-defects"),
    ("F40RoundClose", "executor", ["operability", "calibration"],
     f"Attack the landed plans/round_close.py: `--selftest`; rounds 36-40 on a clean clone (expect 38 red, 39/40 green); "
     f">=6 single-line mutants of it in a scratch copy (receipt resolution rules a/b/c, exit mapping, census leg) — which do the "
     f"selftest and the round runs catch? Does it ever pass with zero receipts?",
     "VERDICT: round-close-mutants-caught-<k>/<n>"),
    ("F40RegradeRecheck", "executor", ["novelty", "coverage"],
     f"Re-check {B}/R40RegradeSweep.md's table on two tasks: configure-git-webserver and git-leak-recovery — rebuild one listed "
     f"state each in the lane's own probe sandbox (scratch copy), grade twice without rebuilding, record verdicts and the "
     f"files the grader wrote (find -newer). Does 'two of five graders mutate the graded state, no verdict flip' hold?",
     "VERDICT: regrade-recheck-<agree|disagree>"),
    ("F40RegistryRows", "critic", ["operability"],
     f"Run every command the round-40 SKILL registry rows and the 'Round-40 registry addendum' state (order-check, "
     f"round39-c1-audit, round40-c1-mutants — HOST-SAFETY sandbox —, round40-c2, db-wal-probe, round_close, tip-receipts) from "
     f"a clean clone root and compare exit codes and verdict lines with the rows' verdict maps.",
     "VERDICT: registry-commands-match-<k>/<n>"),
    ("F40RevLesson", "reviewer", ["calibration"],
     f"Review {LES}: every Gate row's evidence (access dates, quotes, digests), every Mistakes row (class, pointer resolves, "
     f"captured-by, fix shown able to fail — or honestly not), census numbers, the routed R1-R5 dispositions against "
     f"{L}/corpus/lessons/round-39-verifier-spotcheck.md §5. List defects with the smallest appended correction.",
     "VERDICT: lesson-review-<n>-defects"),
    ("F40CritScorecard", "critic", ["calibration"],
     f"Check {L}/SCORECARD.md's round-40 section and {L}/LOG.md's round-40 entry against the receipts ({MEAS}, "
     f"{W}/claims/*.txt, {RCPT}): every number, hash, verdict and 'held' score; any self-assessment that the repo state "
     f"contradicts (count mismatches, file:line).",
     "VERDICT: scorecard-mismatches-<n>"),
    ("F40CritNoHarmDiff", "critic", ["quality"],
     f"`git -C {L} diff d3a6277f {TIP} -- SCORECARD.md LOG.md SKILL.md PROVINCE.md SHONEN.md corpus/` — list every removed or "
     f"rewritten line (not appended) in a lane-authored doc and judge whether it is a harm; check corpus/SOURCES.md changes are "
     f"appends plus the two S046/S052 anchor notes only.",
     "VERDICT: removed-lines-<n>-harms-<k>"),
    ("F40ScoutMisroot", "scout", ["operability"],
     f"Misroot and host-write sweep for round-40 kengaku seats: `git -C {F} status --porcelain --untracked-files=all` (name any "
     f"file whose content names kengaku round 40); `ls -la /home/vgpnk/.local/bin` for files newer than 13:00 today and any "
     f"`git` there; `systemctl --user list-units --all` for crit-*/transient units; leftover dirs under {SCR}/ and processes "
     f"whose cwd is under it. Read-only: report, never delete.",
     "VERDICT: misroot-<n>-host-writes-<k>-scratch-left-<j>"),
    ("F40ConnClaims", "connector", ["calibration"],
     f"Cross-document consistency at {TIP}: claims, both counters' docstrings, controls, measure-final, lesson, SCORECARD/LOG "
     f"round-40 text, README/PROVINCE/SKILL round-40 text — every shared number (21 mutants, 28 cases, 8/20, 111→114 rows, "
     f"46→47 files, killed counts, hashes). List every drift with both locations.",
     "VERDICT: drift-<n>"),
    ("F40ConnFrontier", "connector", ["coverage"],
     f"Frontier check at {TIP}: does the README §Frontier TB2 clause now say 6 of 89; is the binary-database-pair class "
     f"recorded consistently in README coverage map, PROVINCE and SKILL; does any SHONEN/SCORECARD self-assessment line "
     f"mismatch the repo (count, file:line).",
     "VERDICT: frontier-consistent-<yes|no>-mismatches-<n>"),
    ("F40CritSeparability", "critic", ["calibration"],
     f"Separability test: in one clone remove the C2 package (entry, S119-S121 rows, README lines, receipt) and run the C1 "
     f"counter (HOST-SAFETY sandbox) — does C1 still pass? In another remove plans/battery40 and run the C2 counter — does C2 "
     f"pass? Report both receipts and whether the claims' separability sentence holds.",
     "VERDICT: separable-c1-<yes|no>-c2-<yes|no>"),
    ("F40CritPlanNext", "critic", ["calibration", "coverage"],
     f"Attack the round-41 plan ({B}/R40PlanNext.md if present, else SCORECARD `### Planned (round 41)`): re-run one priced "
     f"control cheaply, check each candidate against the lane's PROVINCE refusals and the routed list in {LES}, and say which "
     f"candidate a do-nothing control could reach.",
     "VERDICT: plan41-attack-<n>-defects"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 40 wave 2 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {FX}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r40 wave 2 (falsify)"})
    assert len({i["name"] for i in items}) == len(items)
    spec = {"wave": "kengaku-r40-falsify",
            "milestone": f"kengaku round 40 wave 2: falsify C1 battery40, C2 db-wal package, routed fixes at {TIP[:8]}",
            "reportDir": ".ufo/waves/round-40/falsify", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/falsify-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    c = Counter(i["role"] for i in items)
    print(len(items), dict(c), TIP)
    attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
    flash = c["executor"] + c["scribe"] + c["critic"] + c["sentinel"]
    print(f"attack={attack}/{len(items)} flash={flash}/{len(items)}")


main()
