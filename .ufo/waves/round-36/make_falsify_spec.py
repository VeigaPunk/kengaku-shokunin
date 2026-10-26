#!/usr/bin/env python3
"""Renders .ufo/waves/round-36/falsify-spec.json (wave 2 of 2, policy v1, 34 seats)."""
import json
import pathlib
import subprocess

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-36"
B = f"{W}/build"
X = f"{W}/falsify"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
TIP = subprocess.run(["git", "-C", L, "rev-parse", "master"], capture_output=True, text=True, check=True).stdout.strip()
CAP = f"{L}/corpus/evidence/round36/tb2-regex-log"
E36 = f"{L}/corpus/evidence/round36"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAWRL = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/regex-log"
SPARSE = ("/corpus /plans /SCORECARD.md /LOG.md /SKILL.md /PROVINCE.md /considerthese /.ufo/waves/round-34/assimilation "
          "/.ufo/waves/round-34/build /.ufo/waves/round-36/claims /.ufo/waves/round-36/integrate")
CLONE = (f'Fixture rule: D=$(mktemp -d /tmp/k36f-XXXX); git clone -q --no-checkout --shared {L} "$D/lane"; '
         f'git -C "$D/lane" sparse-checkout set --no-cone {SPARSE}; git -C "$D/lane" checkout -q master; verify '
         f'`git -C "$D/lane" rev-parse --show-toplevel` equals "$D/lane" and `git -C "$D/lane" merge-base --is-ancestor {TIP} master` exits 0 (master may carry later evidence-only or errata commits) '
         f'before any write; every git call names -C "$D/lane"; never commit (index-only `git add` inside a mktemp fixture repo is fine; a fixture '
         f'commit needs identity `fixture <fixture@invalid>` and a `-C` naming the fixture only); rm -rf "$D" at the end.')

CONTEXT = f"""# Goal
kengaku round 36 (hyaku run 7, 2026-10-25), WAVE 2 of 2 (falsify). Lane repo: {L}. Landed tip under attack: {TIP}
(master may carry later evidence-only or errata commits; `git -C {L} rev-parse master` is authoritative for your clone — do not rewrite or reset it).
Frozen claims: {L}/plans/round-36-claims.md (freeze 3241b86c, Amendment 1 acbda2f3). Wave-1 reports (what you attack) are at {B}/R36*.md.
- C1 calibration: hardened gate {L}/plans/pkg_gate.py (installed from candidate R36GateB), battery + ledger counter {L}/plans/round36_c1_verify.py,
  package spec {L}/plans/pkg-spec-r35.json, ledger {L}/corpus/defects-round35.jsonl (R35-D1..D4 `closed`). Measured at the tip in a clean sparse clone:
  `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`, `rows=4 closed=4 observed_pass=4 mismatches=0`, `PREDICATE C1 pass`
  ({W}/integrate/measure.sh runs it).
- C2 coverage: entry {L}/corpus/knowledge/tb2-regex-log-grader.md, rows S108-S110 in {L}/corpus/SOURCES.md, probe {L}/plans/regex_log_probe.py,
  receipt {E36}/regex-log-probe.txt, captures {CAP}/, counter {L}/plans/round36_c2_verify.py (`checks=6 defects=0`, `PREDICATE C2 pass` at the tip).
- Also landed and attackable: {L}/corpus/lessons/round-36.md, corpus/QUALITY.md Q24/Q25, SKILL.md registry rows `package-gate`/`round36-c1-battery`/
  `regex-log-probe` + section `## TB2 regex-log grader — round36`, PROVINCE.md `## Round36 partial frontier admission`, corpus/README.md additions
  (index row, coverage bullet, frontier sub-bullet, `### Round-36 evidence`), SCORECARD.md `## Round 36`, LOG.md `## Round 36`.
- Known wave-1 limits (do not re-discover; extend or falsify them): battery gameable by fixture-keyed gate (R36CritBattery), eight clauses without a fixture
  (R36RevClaims FG1), C2 counter admits a junk package (R36CritC2Counter), one counter survivor M09b (R36MutC2W2W3), stale frozen-digest block (FG3).

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Scratch under
  {X}/<YourSeatName>/ (create it); NEVER leave a copy of lane `corpus/` or `plans/` trees under {X}/ (use mktemp dirs under /tmp, delete them after).
- Write ONLY inside {X}/ (your report + small scripts/receipts, each file < 200 KB) or a mktemp dir under /tmp. NEVER edit corpus/, plans/, SCORECARD.md, LOG.md,
  README.md, SKILL.md, PROVINCE.md, SHONEN.md or any lane file — draft corrections for the L1, who integrates. Never write into {F} (fleet root), sibling lanes,
  the lane's jj state, or the lane's Git index. Never run git add/commit/stash/checkout/reset/push/pull or any mutating jj command in the lane.
- Every claim you make names what it attacks: start each finding with `ATTACKS: <file:line or claim>`; give the command and its observed output; classify
  `survivor | defect | limit | no-finding`.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY. No campaign tools.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels,
  update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide: install via `uv tool` / `npx` / an official binary into
  ~/.local/bin, or file an L0 question. Never run pacman -Sy/-Syu/-U/-R, never name an already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat probe).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location. Do not fabricate output; if something cannot be
  fetched or run, say so.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""

GATE = f"{L}/plans/pkg_gate.py"
BAT = f"{L}/plans/round36_c1_verify.py"


def mutgate(area, detail):
    return (f"Mutation-test the installed gate {GATE} for {area}. Method: make a fixture clone (fixture rule), build the battery's package fixtures with "
            f"`python3 -c 'import sys; sys.path.insert(0,\"plans\"); import round36_c1_verify as c; ...'` (see build_package_fixtures in {BAT}) or hand-copy the package "
            f"files named by {L}/plans/pkg-spec-r35.json into a mktemp fixture repo (index-only `git add`), then apply ONE byte-level mutation at a time and run "
            f"`python3 plans/pkg_gate.py package --root DIR --spec plans/pkg-spec-r35.json --require-clean-tree` (add `--rerun` where relevant); record exit code and the "
            f"DEFECT line. A mutation that violates the clause but exits 0 is a SURVIVOR (false green); a harmless/benign edit that exits 1 is a false red. First confirm the "
            f"unmutated copy exits 0. Mutants: {detail} Report a table (mutant | expected | exit | defect line | verdict) and the survivor list with exact bytes.")


ITEMS = [
    # ---- executors (9): re-run every counting command, no-harm, determinism ----
    ("F36ReRunC1", "executor", ["calibration"],
     f"ATTACKS the C1 measurement. In a fresh clean sparse clone of master {TIP[:8]} run EXACTLY `python3 plans/round36_c1_verify.py --lane .` and paste the complete output twice "
     f"(second run after `rm -rf` of any __pycache__), then under `uv run --no-project -p 3.13 python3 plans/round36_c1_verify.py --lane .`. Report FIXTURES, rows and PREDICATE lines and "
     f"exit codes; any difference between runs or Pythons. Also run `python3 plans/round36_c1_verify.py --lane . --legacy` and say whether it still reads accepted=7/7 at the tip "
     f"(the round-35 counter demands 42/42 knowledge files and is freeze-only). Then commit-tree check: `git -C \"$D/lane\" ls-tree -r --name-only master | grep -cE '^\\.ufo/waves/round-3[0-9]/.*/\\.ufo/waves/round-'` (want 0).",
     "VERDICT: c1-rerun-<pass|fail>-runs-<n>-identical-<yes|no>"),
    ("F36ReRunC2", "executor", ["coverage", "calibration"],
     f"ATTACKS the C2 measurement. In a fresh clean sparse clone of master {TIP[:8]} run EXACTLY `python3 plans/round36_c2_verify.py --lane .` (paste output twice), then under "
     f"`uv run --no-project -p 3.11/3.12/3.13/3.14 python3 plans/regex_log_probe.py --lane .` with each output `cmp`-compared to corpus/evidence/round36/regex-log-probe.txt, with "
     f"PYTHONHASHSEED=1 and 99, and `python3 plans/regex_log_probe.py --lane {L}` from /tmp. Report every byte difference and cause. Finally `sha256sum plans/regex_log_probe.py` against the "
     f"pin `PROBE_SHA256` in plans/round36_c2_verify.py, and `cd corpus/evidence/round36/tb2-regex-log && sha256sum -c SHA256SUMS`.",
     "VERDICT: c2-rerun-<pass|fail>-probe-identical-<n>/<m>"),
    ("F36NoHarm", "executor", ["freshness", "operability"],
     f"ATTACKS the no-harm admission clause. Re-run, in a clean sparse clone of master {TIP[:8]} (patterns `/corpus /plans /SCORECARD.md /grader.py /SKILL.md /PROVINCE.md /LOG.md /README.md /AGENTS.md /SHONEN.md /.ufo/waves/round-34 /.ufo/waves/round-35 /considerthese`), "
     f"each command the wave-1 baseline {B}/R36TipSweep.md ran, and diff every exit code/last line against it: `python3 grader.py`, `grader.py --selftest`, `plans/defect_ledger.py --lane .`, "
     f"`plans/round35_c1_verify.py --lane .` (expected to change: it pins 42 knowledge files — report the exact V4 text), `plans/round35_hardening.py --lane . --skip H6`, state_check, registry_check, "
     f"benchmark_spec_audit, config_projection, sources-census. Classify each difference as caused-by-round-36, pre-existing, or environment; a round-36-caused regression of a gate the lane registers "
     f"is a harm finding (name the owner and a repair).",
     "VERDICT: no-harm-<n_same>/<n_total>-regressions-<n>"),
    ("F36CensusAfter", "executor", ["freshness", "calibration"],
     f"ATTACKS the Sources & frontier numbers. Compute the census AFTER the round on a clean clone of master {TIP[:8]} and BEFORE at the baseline commit b662a5d6 (`git archive`/clone), "
     f"with the CORPUS.md frozen commands (rows, malformed, tier histogram, status histogram, duplicate ids, enum violations, missing used-by) and `{F}/scripts/sources-census.sh validate --root {F} kengaku` "
     f"on the live lane. Report before→after for: registry rows (expect 100→103), tier A count, status mined count, knowledge files and README index rows (42→43), W04 warning count and the three newest rows' "
     f"census lines. Write the exact paragraph (counts + commands) the report's Sources & frontier section should carry, into {X}/F36CensusAfter/sources-frontier.md.",
     "VERDICT: census-<rows_before>-to-<rows_after>-exit-<code>"),
    ("F36VerifyOracleClaims", "executor", ["coverage", "depth"],
     f"ATTACKS the entry's executed claims. Re-run every executed snippet/number the entry {L}/corpus/knowledge/tb2-regex-log-grader.md prints or relies on, from the captures only: the AST walk "
     f"(`sample_logs: 25 expected_dates: 9`, `feb29 anywhere: 0`, `leading-zero-octet lines: []`), the oracle table (`x 10.1.1.1 on 2000-04-31 -> []` … `octet group on 01: True | 007: False`, extracting the "
     f"regex from {CAP}/solve.sh), the oracle's byte count (267), `grep -n '1134' {CAP}/test_outputs.py` (exit 1), and the post-hoc claims (`'1.2.3.4\\n2020-01-01'` → `['2020-01-01']`, "
     f"`'1.2.3.4 2020-01-01\\n2020-01-02'` → `['2020-01-02']`, 5 of 6 multi-line probes). Paste each command and output next to the entry text; any line that does not reproduce is a defect with the "
     f"corrected text.",
     "VERDICT: entry-claims-<n_reproduced>/<n_total>"),
    ("F36GateCompare", "executor", ["calibration", "operability"],
     f"ATTACKS the choice of gate. Four candidates exist: {B}/R36GateA/pkg_gate.py, R36GateB/ (installed as {GATE}), R36GateC/, R36GateD/. Build one mutant corpus of >= 30 single-property mutants of "
     f"the genuine package (reuse the wave-1 mutant scripts under {B}/R36Mut*/ and {B}/R36Gate*/ if present, plus your own) in a fixture clone and run each candidate on each mutant plus the genuine "
     f"package and the six D4/D5 line fixtures. Report a candidate × mutant exit-code matrix, the mutants on which candidates disagree, and whether the installed candidate is dominated (accepts something "
     f"another rejects that is genuinely junk, or rejects something genuine). Do not edit {GATE}.",
     "VERDICT: gate-compare-<n>-disagreements-installed-dominated-<yes|no>"),
    ("F36EntryXcheck", "executor", ["calibration", "coverage"],
     f"ATTACKS the C2 counter's weakness (R36CritC2Counter: a junk package passes W1-W6). Write {X}/F36EntryXcheck/entry_receipt_xcheck.py (stdlib, post-hoc, outside the claim): parse the entry's "
     f"`## Instruction requirement → enforcing assertion` table and `The six findings`, extract each probe case name and its stated `Observed` verdict, and compare with the receipt "
     f"{E36}/regex-log-probe.txt; check every `lines N–M` cited for the grader against {CAP}/test_outputs.py (line exists); check that every case named in the entry exists in the receipt and vice versa "
     f"(24 cases, none unmentioned or invented); check each located-quote row quote is verbatim at its line (independently of the counter). Run it on the landed entry (expect all consistent or list the "
     f"inconsistencies) and on R36CritC2Counter's junk package (read {B}/R36CritC2Counter.md for its bytes; expect it to be rejected). Report exact output.",
     "VERDICT: xcheck-landed-<ok|n_inconsistent>-junk-<rejected|accepted>"),
    ("F36OfflineRun", "executor", ["operability", "freshness"],
     f"ATTACKS the false-red risk R36RevClaims FR1: the tip check `r35_d1` runs `pkg_gate.py package --rerun`, which needs Biopython 1.85 (uv). In a clean sparse clone of master {TIP[:8]} run the "
     f"gate's `package --root . --spec plans/pkg-spec-r35.json --rerun --require-clean-tree` (a) normally, (b) with `UV_OFFLINE=1`, (c) with an empty `UV_CACHE_DIR=$(mktemp -d)` and no network "
     f"(`unshare -rn` if available, else `HTTPS_PROXY=http://127.0.0.1:9`), (d) with `PATH` stripped of uv. Record exit code and DEFECT/error text each time. Then state which environment a non-author "
     f"closure on a fresh host would need (python3 + uv + network once) and draft the one-line prerequisite sentence for the report. Do not modify the gate.",
     "VERDICT: rerun-env-<n_pass>/4-prereq-<uv|biopython|network>"),
    ("F36SkillCmds", "executor", ["operability", "depth"],
     f"ATTACKS the new SKILL.md/QUALITY.md executable claims. In a clean sparse clone of master {TIP[:8]} run VERBATIM every command named in the three new `## Gate/probe registry` rows "
     f"(`package-gate`, `round36-c1-battery`, `regex-log-probe`), in the section `## TB2 regex-log grader — round36`, and in the `Check (executable …)` lines of QUALITY.md Q24 and Q25 (including the "
     f"name-blind leg and the `git show 3241b86:plans/regex_log_probe.py … cmp` leg; adapt `/tmp` paths only). Record command, exit code, and whether the stated output/verdict map holds. Any command that "
     f"does not run as written, or whose exit code differs from the row's verdict map, is a defect with the corrected text. Also verify each file:line pointer in the new SKILL section "
     f"(`corpus/evidence/round36/regex-log-probe.txt:26`, `test_outputs.py:65,67`, `instruction.md:3`, `test.sh:26-28`) resolves to what the sentence says.",
     "VERDICT: cmds-ok-<n_ok>/<n_total>-pointers-bad-<n>"),
    # ---- critics (7, m_flash) ----
    ("F36CritScorecardLog", "critic", ["calibration"],
     f"ATTACKS the lane's self-assessment (calibration = mismatches between self-assessment and repo state). Count every checkable statement in {L}/SCORECARD.md `## Round 36` + the two new capability rows + "
     f"`### Planned (round 37)`, {L}/LOG.md `## Round 36`, {L}/corpus/lessons/round-36.md, and {L}/corpus/README.md round-36 insertions against repo state: each number, hash, path, count, line pointer, "
     f"command output. Produce a table (statement | command | observed | match yes/NO) of >= 40 rows and a final `mismatches=<n>`; cite the exact line of each wrong statement and draft the corrected "
     f"sentence. Include: registry 100→103, knowledge 42→43, 21→0 nested paths, `deterministic across Python 3.11/3.12/3.13`, `five harness mutants detected`, `four candidates scored 0/0/0`, "
     f"`R36GateB was installed`, every `R36*.md` path named, the `measure-final.txt` pointer (does it exist at the tip?).",
     "VERDICT: selfassess-mismatches-<n>/<rows>"),
    ("F36CritAmendment", "critic", ["calibration"],
     f"ATTACKS Amendment 1 and the frozen-digest block of {L}/plans/round-36-claims.md. Read {B}/R36ConnAmendment.md (recommendation: revision) and {B}/R36RevClaims.md FG3. Verify with `git show 3241b86:…` and "
     f"`sha256sum` which of the five frozen-digest rows are stale at the tip and which commit changed each; verify the claim 'before any seat dispatch' (commit times vs build.ready.dispatched); verify no seat "
     f"scored the probe before Amendment 1 (wave-1 seats only started after f9efce3). Then draft the exact appended `### Amendment 1 digest correction` text (new digest of plans/round36_c2_verify.py at the tip, "
     f"the table of the five digests at the tip, wording `revision` vs `ratchet` justified by the sibling precedents) so the report can cite it. Say whether the C2 verdict can stand if the operator rules "
     f"the amendment a rule change (what the counter would read at the freeze-commit probe: run it).",
     "VERDICT: amendment-<bounded|unbounded>-stale-digests-<n>"),
    ("F36CritOverfit2", "critic", ["calibration"],
     f"ATTACKS the installed gate for name/path/marker-keyed behaviour (Q24's name-blind leg; R36CritBattery found 8 cues for an overfit gate). Take the six package fixtures P0,P1,P4,P5,P6,P7 built by "
     f"`build_package_fixtures` and re-run the INSTALLED gate {GATE} on each after: (1) copying the fixture root to a neutral dir name; (2) renaming the stray file `plans/round35_scratch.py` to "
     f"`notes/todo.txt`; (3) replacing the junk marker word with other 1-word/low-content strings; (4) reordering the genuine rows; (5) changing the stub probe's shape (still prints the receipt); (6) wrapping "
     f"the one-word quotes in distinct 3-word junk phrases from one boilerplate line. The first five must keep the same verdict; (6) is the honest limit probe — report whether the gate rejects it (it should "
     f"only reject via a genuinely checked clause). Read {GATE} for any string literal that matches a fixture marker (`grep -n 'junk\\|scratch\\|k36\\|stray' {GATE}`).",
     "VERDICT: overfit-installed-<clean|keyed>-variants-<n>"),
    ("F36CritEntry", "critic", ["depth", "coverage"],
     f"ATTACKS the C2 entry as a knowledge entry against {L}/corpus/QUALITY.md (every criterion Q1..Q25). Read {L}/corpus/knowledge/tb2-regex-log-grader.md in full. For each QUALITY criterion say "
     f"met/not-met with the entry line; look especially for: sentences that outrun the receipt ('visible in the test file' vs R36ScoutTB2Visibility's `hidden-until-verify`), a negative claim without a sweep command, "
     f"the tier-C oracle section vs the claim it supports, tool-only claims (AST walk) with no committed script, numbers without commands, mislabelled quote locations, the `Source labels` self-report wording, "
     f"and whether the six findings are bounded to this capture. Draft exact replacement sentences for every defect, as an appended `## Errata` block the L1 can paste.",
     "VERDICT: entry-critic-<n>-defects-<n>-errata-lines"),
    ("F36CritLesson", "critic", ["calibration"],
     f"ATTACKS {L}/corpus/lessons/round-36.md. Check: every `<TBD at landing>` still present (list them; each must be replaced by a measured value or removed); the `## Gate` rows against facts "
     f"(S108-S110 quote words/locations via grep -nF on the captures; sha256 prefixes; the assimilation set has >=1 admit and >=1 reject — which rows are they, are they from the assimilation set); the "
     f"Erratum line satisfies `r35_d4` and is honest; the `## Mistakes` table: class vocabulary per CORPUS.md, evidence pointers resolve, `captured-by`, `fix` shown able to fail (red-before pointers exist); "
     f"the six-item disposition table vs round-35-verifier-spotcheck.md §5; the `## Spot-check` section. Add the mistakes wave 1 found but the lesson omits (battery gameable R36CritBattery; counter admits junk R36CritC2Counter; "
     f"stale digest block FG3; FG1 clause gaps; the seat's own prediction misses in R36CritUnenforced; scratch mirrors left in lane — R36ProbeHarnessMut/RowsDraft). Draft each missing `## Mistakes` row in table form.",
     "VERDICT: lesson-critic-<n>-tbd-<n>-missing-mistakes"),
    ("F36CritQuality", "critic", ["calibration", "depth"],
     f"ATTACKS the new QUALITY.md criteria Q24 and Q25 ({L}/corpus/QUALITY.md tail). For each: is it a criterion (a test a future entry/counter can fail), not a diary? Does every `Shown able to fail` claim "
     f"point at a committed receipt that exists at the tip (`ls`), and does the quoted number match it? Does its executable check run (coordinate with F36SkillCmds' results if present; else run the cheap ones)? "
     f"Is it duplicated by Q22/Q23 or QUALITY earlier text (grep -n 'junk\\|battery\\|amend' corpus/QUALITY.md)? Does Q24's `Limits` paragraph already admit the overfit surface that "
     f"{B}/R36CritBattery.md measured (8 cues) and the FG1 clause gaps? Draft the exact appended `Q24 limit addendum` (a new row, never an in-place rewrite) that names those measured limits with pointers.",
     "VERDICT: quality-critic-<n>-defects-<n>-addenda"),
    ("F36CritReadme", "critic", ["coverage", "freshness"],
     f"ATTACKS the README additions ({L}/corpus/README.md: index row, coverage bullet, `Partly discharged round 36`, `### Round-36 evidence`). Check every path in the evidence list exists at the tip "
     f"(`ls`), the index parity with `ls corpus/knowledge/*.md | wc -l`, that the coverage bullet and sub-bullet claim no more than the receipt shows (the bullet's 'which instruction.md bullets no assertion enforces' list vs the "
     f"eight observed-pass cases), that earlier README lines the round contradicts are not left standing (grep the README, SKILL, PROVINCE, corpus/QUALITY for 'other 88 TB2 tasks', '42 knowledge', "
     f"'42/42', '100 rows', 'Terminal-Bench 2.0's' — the protocol's 'corrections sweep every mention'), and that the 'Round-36 evidence' list names `plans/pkg_gate.py` accurately. Draft appended correction lines "
     f"(never in-place rewrites) for each stale mention.",
     "VERDICT: readme-critic-<n>-stale-mentions-<n>"),
    # ---- scribe (1, m_flash) ----
    ("F36ErrataDraft", "scribe", ["calibration"],
     f"Draft the errata/addenda the round needs, as paste-ready appended blocks, from the facts already in the repo (read-only; do not wait for other wave-2 seats): (1) SCORECARD.md `### Round-36 errata` "
     f"(stale frozen-digest block: the five rows of plans/round-36-claims.md vs `sha256sum` at the tip; the separability sentence's C1-reads-C2's-README coupling and the order it forces: C2 index row before the C1 "
     f"measurement; `--legacy` freeze-only after C2 lands because plans/round35_c1_verify.py V4 pins 42/42; FR1's Biopython/uv prerequisite; N3 nested-regex footgun for round-36 seat mirrors; N2 `closed_round` "
     f"unchecked), (2) a LOG.md `### Round 36 — errata` stub with the same facts, (3) the claims-file `### Amendment 1 digest correction` table. Every number must come with the command you ran; use "
     f"`git -C {L} show 3241b86:plans/round36_c2_verify.py | sha256sum` etc. Mark any statement you could not verify `[unverified]`.",
     "VERDICT: errata-drafted-<n>-blocks"),
    # ---- reviewers (3, m_zfl) ----
    ("F36RevSkillProvince", "reviewer", ["adjacency", "depth"],
     f"ATTACKS the SKILL.md additions and the PROVINCE.md round-36 paragraph. SKILL: the three registry rows have all eight columns and the verdict maps match what the scripts actually return "
     f"(run `python3 plans/pkg_gate.py package --root /nonexistent --spec plans/pkg-spec-r35.json; echo $?` → 2? usage/setup vs crash; `d4-line` with an unreadable file; `regex_log_probe.py` exit 2 on a "
     f"tampered grader copy), the pinned values named exist at the tip, the `## TB2 regex-log grader — round36` section's enforced/not-enforced split matches the receipt. PROVINCE: the paragraph stays inside the "
     f"refusals of the round-28/29/35 paragraphs; every sibling citation `file:line` resolves to its quoted claim (open each sibling PROVINCE.md under {F}/*-shokunin/); word count <= 140 for the body. "
     f"Cite file:line for each finding and draft the repair.",
     "VERDICT: skill-province-<n>-defects"),
    ("F36RevProbeCases", "reviewer", ["coverage", "calibration"],
     f"ATTACKS the probe's frozen case table via {B}/R36RevProbePred.md's two confounded cases and five uncovered instruction sentences. Re-derive independently (own script, own copy of the 25 log lines): for each "
     f"of the 16 failing cases, the FIRST sample line whose result differs from expected, and whether that line is the one the case's requirement label names (e.g. `ip-no-right-boundary`, "
     f"`ip-octets-unbounded`, `empty-pattern`). List every case whose death is explained by a different requirement than its label (confounded), and verify the entry's `What decides it` column (lines named) "
     f"against your result. Report a table and the corrected `What decides it` cells for any wrong row.",
     "VERDICT: probe-cases-<n>-confounded-<n>-wrong-cells"),
    ("F36ReopenQuotes", "reviewer", ["coverage", "freshness"],
     f"ATTACKS the located quotes. Independently of plans/round36_c2_verify.py: write your own script that, for every row of the entry's `## Located quotes` table "
     f"({L}/corpus/knowledge/tb2-regex-log-grader.md) and every quote in the three SOURCES rows' anchor cells and the lesson `## Gate` S108-S110 rows, (a) finds the quote in the committed capture at the cited "
     f"line, (b) finds it in the LIVE raw file ({RAWRL}/<path>, curl -fsSL), (c) counts words (<= 25), (d) checks the cited line number is the line of first occurrence. Output a table with columns "
     f"row | capture-line-ok | live-ok | words | first-occurrence-line. Any quote that is not byte-exact live is a defect.",
     "VERDICT: quotes-ok-<n>/<n_total>-live-mismatch-<n>"),
    # ---- mutation-testers (8, m_zfl) ----
    ("F36MutGateQuotes", "mutation-tester", ["calibration"],
     mutgate("its quote clauses", "quote off by one line; one changed char; 26-word; 2-word; straight-quote row; eight copies of one quote; seven distinct quotes (one short); eight quotes at seven distinct locations; a location citing a file outside the capture dir; `a-b` span instead of one line; quote present only on an adjacent line; the quote table header removed; the quotes section duplicated; a quote containing `|`."),
     "VERDICT: gate-quotes-mutants-<caught>/<total>-survivors-<n>"),
    ("F36MutGateRows", "mutation-tester", ["calibration"],
     mutgate("its SOURCES row clauses (S105-S107)", "10 cells; 12 cells; escaped `\\|` in a cell; /tasks/ in the URL; #L fragment on the URL; a second URL in the source cell; tier B; status queued; opened 2026-10-24; used-by with a second path; used-by absent; a duplicate S106 row; a row indented 2 spaces (counts) and 4 spaces (code block: does it change the verdict?); teaches 7 words; two rows with identical teaches; teaches 8 words of filler; an extra row S108 present or absent (must not matter)."),
     "VERDICT: gate-rows-mutants-<caught>/<total>-survivors-<n>"),
    ("F36MutGateCapture", "mutation-tester", ["calibration"],
     mutgate("its pin clauses (capture manifest, frozen instruments, receipt)", "SHA256SUMS missing instruction.md; test.sh digest altered; a listed file deleted; a capture file edited by one byte with its SHA256SUMS line regenerated (pinned digest must catch it); an unlisted extra direct file in the capture dir; a listed file with `*` binary marker; manifest line with CRLF; plans/tb2_grader_probe.py edited by a comment; plans/defect_ledger.py edited by a space; plans/round35_c1_verify.py replaced by an empty file; receipt one byte changed; receipt trailing newline removed; receipt_sha256 in the spec edited (spec tampering: does the gate read the spec from the fixture or from --spec?)."),
     "VERDICT: gate-pins-mutants-<caught>/<total>-survivors-<n>"),
    ("F36MutGateEntry", "mutation-tester", ["calibration"],
     mutgate("its entry/index clauses", "drop the S106 source line; swap the order of source lines; verified-at 2026-10-24; recheck without cadence; `## Negative space` renamed; Negative space present but no `falsif`; the receipt summary line removed from the entry (does the gate require it?); README index row without S107; coverage bullet removed; a 43rd knowledge file not indexed; index row duplicated; the index row moved out of the knowledge table; entry file empty; entry file binary garbage; entry with Windows line endings."),
     "VERDICT: gate-entry-mutants-<caught>/<total>-survivors-<n>"),
    ("F36MutGateLines", "mutation-tester", ["calibration"],
     mutgate("its d4-line and d5-line clauses", "D4: swapped citations (frozen L2); missing harness token (L3); citation present but token before the citation; both tokens in a later sentence; the label line duplicated (two lines in the file); label changed to round 35; an extra false sentence appended after a correct clause; leading whitespace before `- **D4`; D5: `is not present` (L5); `is present` inside a different clause; capture altered (L6); capture correct but manifest line removed; manifest digest wrong; quote absent from the capture although digest is pinned (can that happen?); capture-dir argument pointing at a dir with only the capture and no manifest; two erratum lines."),
     "VERDICT: gate-lines-mutants-<caught>/<total>-survivors-<n>"),
    ("F36MutGateRerunTree", "mutation-tester", ["calibration"],
     mutgate("`--rerun` and `--require-clean-tree`", "receipt differs by one byte while its sha256 pin is also edited in a copied spec (tamper both: which clause catches?); probe prints a stub receipt (digest pin catches); probe_cmd failing with exit 3; probe producing the receipt plus a trailing warning on stderr only; probe non-deterministic output; an untracked file at depth 3; an untracked file listed in .gitignore (must not count); an untracked directory only containing an empty dir; a tracked-but-modified file (does the gate see it? report honestly — `--require-clean-tree` is untracked-only by contract); a staged-but-uncommitted new file (index-only add) must NOT count as untracked; the root not being a git repo (exit?)."),
     "VERDICT: gate-rerun-tree-mutants-<caught>/<total>-survivors-<n>"),
    ("F36MutGateCrash", "mutation-tester", ["calibration"],
     f"Fail-closed attack on the installed gate {GATE} (Gate standard: an undeclared nonzero code reads could-not-evaluate, and a crash must never read as accept). Using a fixture clone (fixture rule), run "
     f"the gate with: missing --spec; spec file absent; spec malformed JSON; spec missing each top-level key in turn (entry, capture_dir, receipt, rows, frozen_instruments, entry_rules, d4, d5); root nonexistent; root a file; "
     f"entry a directory; entry unreadable (chmod 000); entry non-UTF8 bytes; huge entry (50 MB of `a` — time it, <= 60 s?); a quote row with a 1 MB cell; `--rerun` with uv absent; `d4-line --file` nonexistent; `d5-line` without --capture-dir. "
     f"Record exit code and message for each; exit 0 on any malformed input is a SURVIVOR; Python traceback exit 1 is a limit (a crash read as `reject`) — report which exit codes the gate uses for crashes versus declared rejects "
     f"and whether `round36_c1_verify.py`'s `unevaluated` classification can tell them apart.",
     "VERDICT: gate-crash-cases-<n>-exit0-survivors-<n>-crash-as-reject-<n>"),
    ("F36MutBatteryAblation", "mutation-tester", ["calibration"],
     f"Source-level mutation of the installed gate to measure which battery fixtures kill which clause (R36RevClaims FG1 says eight advertised clauses have no fixture). In a fixture clone, make >= 20 single-"
     f"edit source mutants of {GATE} — one per clause (disable/invert each: frozen-instrument pin, receipt pin, row parse, 3-word minimum, 25-word maximum, distinctness, location distinctness, verbatim-on-line, "
     f"teaches >= 8 words, teaches distinct, capture manifest pin, row URL pin, used-by, provenance trio, negative space, falsifier, index row, coverage bullet, parity, clean tree, rerun compare, d4 patterns, d5 `is present`, "
     f"d5 capture digest) — and run `python3 plans/round36_c1_verify.py --lane <clone>` with each mutant installed as plans/pkg_gate.py. Report a clause × `FIXTURES false_green/false_red` table: which clauses the "
     f"frozen battery detects (kills the mutant: false_green>0 or false_red>0) and which it cannot (survivors = clauses the battery leaves unfalsified). This is the measured form of FG1; do not edit the battery.",
     "VERDICT: ablation-mutants-<n>-battery-detects-<n>-unfalsified-<n>"),
    # ---- scouts (4, m_mim) ----
    ("F36ScoutReopenRows", "scout", ["coverage", "freshness"],
     f"ATTACKS the three new registry rows S108-S110 ({L}/corpus/SOURCES.md). Re-open each URL live on the access date (curl -fsSL), hash it (sha256 must equal the digest in the row's anchor cell and "
     f"{CAP}/SHA256SUMS), and for every `sed`-able anchor in the row (line ranges, quoted fragments, the '(N words)' counts) verify against the live bytes: line numbers, word counts, quote text. Check the "
     f"'opened', 'tier', 'kind', 'scope' semantics against the CORPUS.md SOURCES contract ({F}/CORPUS.md §SOURCES.md): is tier A right for each (primary for its scope?); is `teaches` one grounded benefit; is the "
     f"anchor a section/line plus revision. Report per-row verdict agree/disagree with reasons.",
     "VERDICT: rows-reopen-agree-<n>/3"),
    ("F36ScoutSibling", "scout", ["adjacency"],
     f"ATTACKS the adjacency claims: re-open the sibling PROVINCE.md files cited by the PROVINCE paragraph and the wave-1 {B}/R36ConnSibling.md (if present) under {F}/*-shokunin/ and confirm each cited "
     f"`file:line` says what the paragraph says it says (<=25-word quote + location each). Then scan for any sibling that has since (this session, today) added Terminal-Bench / regex / grader-probe surface "
     f"(`git -C <sibling> log --since=2026-10-25 --stat -- PROVINCE.md corpus/README.md`) that would make the lane's claim contested. Report contested / adjacent / none per sibling.",
     "VERDICT: sibling-cites-<n>-ok-<n>-wrong-contested-<n>"),
    ("F36ScoutPriorArtReopen", "scout", ["novelty", "freshness"],
     f"ATTACKS the prior-art verdict (`incremental`) from {B}/R36ScoutPriorArt.md. Re-open its six strongest hits (URL each) and verify the <=25-word quotes and locations byte-exactly against the live pages; "
     f"state per hit whether it supports `a fixed-log pattern grader accepts a literal alternation of its expected outputs and leaves boundary/validity requirements unenforced` or only the generic thin-mutant / "
     f"leakage idea. Is `incremental` the right word, or `established` (for the instrument) with `novel only in the task-specific findings`? One paragraph with evidence; no novelty claim is made by this round — "
     f"the verdict decides only how the report words the novelty axis (unchanged).",
     "VERDICT: priorart-reopen-<n>-ok-verdict-<established|incremental|novel>"),
    ("F36ScoutVisibility", "scout", ["coverage", "depth"],
     f"ATTACKS the entry's visibility wording: the entry says the 25-line log and nine expected dates are 'visible in the test file' and a hard-coded alternation 'scores 1'. Open {B}/R36ScoutTB2Visibility.md "
     f"(verdict hidden-until-verify) and re-open its cited sources (TB2 paper / Harbor docs / the pinned README) yourself: quote (<=25 words + URL + section) whether `tests/` is uploaded only at verification. "
     f"Then read every sentence of the entry and the README/SKILL/PROVINCE/lesson text that implies an agent could see the fixed log, and say which wording is unsupported; draft exact replacement sentences "
     f"(`the grader's fixed log is in the task's test file, which Harbor uploads at verification [source]`; the finding is about what the grader *can* distinguish, not about agent behaviour).",
     "VERDICT: visibility-wording-<n>-defects-sources-<n>"),
    # ---- connectors (2, m_antigravity) ----
    ("F36ConnCrossClaim", "connector", ["adjacency", "calibration"],
     f"Cross-claim and cross-source pattern scan of the landed round. Read the claims, entry, lesson, SCORECARD/LOG sections, QUALITY Q24/Q25 and the wave-1 reports {B}/R36*.md and find: (a) statements in one "
     f"artefact contradicted by a wave-1 finding that no artefact absorbed (list: finding → report:line → artefact that should carry it); (b) the same failure class across C1 and C2 (both counters accept junk by "
     f"their own controls — what single rule would have caught both, and is it in QUALITY?); (c) overlaps between this round's lessons and rounds 33-35 (recurring classes: counter-accepts-junk, stale digest "
     f"block, evidence scratch left in the lane) — count recurrences with `grep -n` over the round-3x lessons; (d) any claim in the report-to-be that would be a `universal clause`.",
     "VERDICT: crossclaim-<n>-unabsorbed-<n>-recurring-classes"),
    ("F36ConnL0", "connector", ["adjacency", "calibration"],
     f"Decide which operator questions this round must append to {F}/.ufo/l0-questions.md (you may NOT append; draft lines only, format `kengaku | round-36 | <question>`, no newlines inside a line). Read the "
     f"file (grep kengaku, revenger round-68/69, kumitate round-63/64, tabi round-22) and {B}/R36ConnAmendment.md, {B}/R36ConnSibling.md (if present). Candidates: (1) Amendment 1 — a pre-scoring mechanical "
     f"repair of a frozen instrument: revision or rule change? (2) Does the gameable-by-construction 14-fixture battery (R36CritBattery) still admit C1 under the frozen kill rule? (3) the round-25/33 coverage "
     f"cap: another round of net-new entries on uncovered ground with 7→7 held — restate the decision packet or is the existing line enough? Each draft question must be answerable yes/no/choose-A-B, cite evidence "
     f"paths, and not duplicate an existing open line (cite the line you checked). Return at most 3 lines.",
     "VERDICT: l0-drafts-<n>-duplicates-<n>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 36 wave 2 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {X}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r36 wave 2 (falsify)"})
    assert len({i["name"] for i in items}) == len(items) == 34, len(items)
    spec = {"wave": "kengaku-r36-falsify",
            "milestone": "kengaku round 36 wave 2: attack the landed gate, entry, counters, lesson, QUALITY, SKILL, README, SCORECARD and LOG",
            "reportDir": ".ufo/waves/round-36/falsify", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/falsify-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    from collections import Counter
    print(TIP, Counter(i["role"] for i in items))


main()
