#!/usr/bin/env python3
"""Renders .ufo/waves/round-36/build-spec.json (wave 1 of 2, policy v1, 40 seats)."""
import json
import pathlib

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-36"
B = f"{W}/build"
GS = "/skill:godspeed\n\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md").read() + "\n"
CAP = f"{L}/corpus/evidence/round36/tb2-regex-log"
E36 = f"{L}/corpus/evidence/round36"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAWRL = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/regex-log"
CLONE = (f'Fixture rule: D=$(mktemp -d /tmp/k36-XXXX); git clone -q --no-checkout --shared {L} "$D/lane"; '
         f'git -C "$D/lane" sparse-checkout set --no-cone <patterns>; git -C "$D/lane" checkout -q master; verify '
         f'`git -C "$D/lane" rev-parse --show-toplevel` equals "$D/lane" before any write; every git call names -C "$D/lane"; '
         f'never commit (index-only `git add` inside a mktemp fixture repo is fine); copy uncommitted lane files you need into the clone. rm -rf "$D" at the end.')

CONTEXT = f"""# Goal
kengaku round 36 (hyaku run 7, 2026-10-25), WAVE 1 of 2 (build + first falsifiers). Lane repo: {L}.
The two claims are FROZEN at {L}/plans/round-36-claims.md (freeze commit 3241b86cde0e9a3b9363a0d4c7fff12ec5d5f5e2, Amendment 1 at
acbda2f3936838ba4849f14937fbecb8aed461e5) — read it first, in full.
- C1 calibration: write and prove a hardened gate `plans/pkg_gate.py` so that `python3 plans/round36_c1_verify.py --lane .`
  prints `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` (the battery of 8 package + 6 line fixtures it builds) and closes the
  four round-35 routed defects R35-D1..D4 ({L}/corpus/defects-round35.jsonl). The gate CLI contract is in the docstring of
  {L}/plans/round36_c1_verify.py; the package it checks is defined by {L}/plans/pkg-spec-r35.json. Gate semantics (hardened):
  frozen-instrument sha256 pins; receipt sha256 pin; every `## Located quotes` row parses (an unparsed row is a defect), >=8 distinct
  quotes of 3..25 words at >=8 distinct located lines, each verbatim on the cited capture line(s); SOURCES rows S105-S107 once each,
  11 cells, tier A, status mined, pinned URL, used-by = the entry, teaches >=8 words and pairwise distinct; capture SHA256SUMS pinned;
  entry provenance trio + `## Negative space` with a falsifier; README index row + coverage bullet and knowledge files == index rows;
  `--require-clean-tree` = no untracked file (`git -C ROOT ls-files --others --exclude-standard` empty); `--rerun` re-runs the probe
  command and byte-compares the receipt; d4-line / d5-line directional checks per the spec. A gate must never recognise fixtures by name,
  path, or marker string (that is overfitting and will be attacked in wave 2).
- C2 coverage: pinned Terminal-Bench 2.0 `regex-log` grader (terminal-bench-2 @ {PIN}) admitted as
  corpus/knowledge/tb2-regex-log-grader.md with rows S108 (tests/test_outputs.py), S109 (tests/test.sh), S110 (instruction.md) and the executed
  offline probe {L}/plans/regex_log_probe.py (24 frozen cases; receipt {E36}/regex-log-probe.txt:
  `cases=24 observed_pass=8 observed_fail=16 mismatches=0`). Counter: `python3 plans/round36_c2_verify.py --lane .` (W1-W6, docstring).
  Captures (byte-identical to the pinned raw files, SHA256SUMS beside them): {CAP}/ (test_outputs.py, test.sh, instruction.md, task.toml,
  solve.sh = the task oracle). Headline findings of the receipt: the grader's fixed 25-line log lets a literal
  alternation of the nine expected dates pass; leading-zero IPv4 octets (instruction forbids), digit-adjacent dates (`1134-12-1234` example),
  5/other-width years, month-length validity (Feb 30 / Apr 31 sit only on invalid-IP lines) and the permitting side of Feb 29 are not enforced.
- Controls already scored (all red at freeze): {W}/claims/control-*.txt. The round-35 package (S105-S107, tb2-protein-assembly) is the
  genuine package of the C1 battery.

# Rules for every seat
- Your tools start at the fleet root. EVERY path is absolute. Every `Report:` trailer path is relative to {L} — write it at
  {L}/<that path>. Any scratch/draft files go under {B}/<YourSeatName>/ (create it).
- Write ONLY inside {B}/ (your report + your own scratch dir) or a mktemp dir under /tmp. NEVER edit corpus/, plans/, SCORECARD.md, LOG.md,
  README.md, SKILL.md, PROVINCE.md, SHONEN.md or any other lane file — draft for the L1, who integrates. (Assimilation/id-guard scratch goes
  under {W}/assimilation/.) Never write into {F} (fleet root), sibling lanes, the lane's jj state, or the lane's Git index.
  Never run git add/commit/stash/checkout/reset/push/pull or any mutating jj command in the lane.
- {CLONE}
- Source repo /home/vgpnk/Projects/shokuknow is READ-ONLY: never write/commit/fetch there; run none of its campaign tools.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
  first (official channels, update-safety gate; record tool/version/channel/reason). pacman transactions are PAUSED host-wide: install via
  `uv tool` / `npx` / an official binary into ~/.local/bin, or file an L0 question. Never run pacman -Sy/-Syu/-U/-R, never name an
  already-installed package to pacman, never restart a host service.
- You are a leaf seat: no subagents, no background jobs, no `task` (an executor may spawn at most one read-only labrat probe).
- Godspeed posture: name the axes, iterate cheap and in parallel, keep moves that improve any axis and harm none, never stall in
  clarifying-question loops.
- Evidence: every number carries the command that produced it and its output. A quote carries its location (file:line or URL+section).
  Do not fabricate output; if something cannot be fetched or run, say so.
- End your report with exactly one `VERDICT: <line>` terminal line.
"""

GATE_TASK = (
    f"Write the C1 gate candidate `{{S}}/pkg_gate.py` (Python 3 stdlib only, no network, <= 400 lines) implementing the contract in the wave "
    f"context and the docstring of {L}/plans/round36_c1_verify.py, reading {L}/plans/pkg-spec-r35.json. Subcommands: `package --root DIR "
    f"[--require-clean-tree] [--rerun] --spec SPEC`, `d4-line --file F --spec SPEC`, `d5-line --file F --capture-dir D --spec SPEC`; print one "
    f"`P<n> ok|DEFECT <reason>` / `D4|D5 ok|DEFECT` line per check and a `defects=<n>` line; exit 0 accept, 1 reject, 2 usage/setup (never exit 0 or 1 "
    f"on a crash). Prove it: make a fixture clone per the fixture rule (sparse patterns `/corpus /plans /SCORECARD.md /.ufo/waves/round-34/assimilation "
    f"/.ufo/waves/round-34/build`), copy {L}/plans/regex_log_probe.py, round36_c1_verify.py, round36_c2_verify.py, pkg-spec-r35.json, "
    f"{L}/corpus/defects-round35.jsonl, and {E36}/ into it, install your gate as plans/pkg_gate.py there, and run `python3 plans/round36_c1_verify.py "
    f"--lane \"$D/lane\"`. Paste the full output. Target: FIXTURES total=14 false_green=0 false_red=0 unevaluated=0 (the four ledger rows may still read red "
    f"for reasons outside your gate: R35-D2 untracked files in the clone, R35-D3 nested paths, R35-D4 lesson). Also run your gate on the REAL lane: "
    f"`python3 {{S}}/pkg_gate.py package --root {L} --rerun --spec {L}/plans/pkg-spec-r35.json` and report the exit code (the lane has untracked wave files, so omit "
    f"--require-clean-tree here). Report the gate's sha256, line count, and which battery fixture each clause kills (one-line table)."
)

ITEMS = [
    # ---- executors (13) ----
    ("R36GateA", "executor", ["calibration", "operability"],
     GATE_TASK.replace("{S}", f"{B}/R36GateA") + " Style: one function per clause, a table-driven clause list, compact output.",
     "VERDICT: gateA-false_green-<n>-false_red-<n>-unevaluated-<n>"),
    ("R36GateB", "executor", ["calibration", "operability"],
     GATE_TASK.replace("{S}", f"{B}/R36GateB") + " Style: parse once into a small dataclass of the package (rows, quotes, captures) and run every clause over it; different structure from a flat check list.",
     "VERDICT: gateB-false_green-<n>-false_red-<n>-unevaluated-<n>"),
    ("R36GateC", "executor", ["calibration", "operability"],
     GATE_TASK.replace("{S}", f"{B}/R36GateC") + " Style: smallest correct gate; prefer re-deriving values from the committed capture bytes over trusting any text in the entry.",
     "VERDICT: gateC-false_green-<n>-false_red-<n>-unevaluated-<n>"),
    ("R36GateD", "executor", ["calibration", "operability"],
     GATE_TASK.replace("{S}", f"{B}/R36GateD") + " Style: fail-closed; any parse exception is a DEFECT line plus exit 1, a usage error exit 2; add a `--selftest` that builds three tiny fixtures in a temp dir (pass, one-word-quote junk, unparsed-row junk) and asserts exit codes.",
     "VERDICT: gateD-false_green-<n>-false_red-<n>-unevaluated-<n>"),
    ("R36IndepRegexGrader", "executor", ["coverage", "calibration"],
     f"Write an INDEPENDENT checker {B}/R36IndepRegexGrader/indep.py that re-implements the grader's assertions from your own reading of {CAP}/test_outputs.py and {CAP}/instruction.md (own sample-log list copied by hand from the grader source, own findall comparison; do NOT import the grader or the probe's run_grader). Import only `build_cases` from {L}/plans/regex_log_probe.py to get the 24 candidate regexes and their modes; score each; compare pass/fail and the failing-assertion class (missing file / invalid regex / wrong matches) with the `observed=` and `assertion=` fields of {E36}/regex-log-probe.txt. Any disagreement is a finding against the probe or the receipt. Also report, per case, the exact set of (log line index, got-vs-expected) differences for the 16 failing cases so the entry can say WHICH sample line each mutant dies on.",
     "VERDICT: indep-agree-<n>/24"),
    ("R36OracleRun", "executor", ["coverage", "depth"],
     f"Extract the oracle regex from the heredoc in {CAP}/solve.sh (bytes between `cat << 'EOF' > /app/regex.txt` and `EOF`) and run it (a) through the real grader via plans/regex_log_probe.py's run_grader (import it; the grader path is {CAP}/test_outputs.py) and (b) through a table of 40 hand-built probe lines you write: IPv4 with leading zero (`01.2.3.4`, `192.168.001.1`), Feb 29/30, Apr 31, year `12345-06-07`, digit-adjacent dates (`1134-12-1234`, `x2020-01-01`), IPv6-ish, two IPs, date before IP, etc. For each report oracle-match vs the instruction's stated rule. Key question: does the task's own oracle violate any instruction requirement (the oracle has `1?\\d?\\d` octets)? Report line numbers in solve.sh for each quoted fragment (<=25 words each).",
     "VERDICT: oracle-passes-grader-<yes|no>-violations-<n>"),
    ("R36ReopenPins", "executor", ["coverage", "freshness"],
     f"Independently re-open the pinned files {RAWRL}/{{tests/test_outputs.py,tests/test.sh,instruction.md,task.toml,solution/solve.sh}} with curl -fsSL into {B}/R36ReopenPins/. cmp each against {CAP}/ (solve.sh is stored there as solve.sh, tests/ files by basename); `cd {CAP} && sha256sum -c SHA256SUMS`. Confirm via https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/{PIN} that the commit exists (record date/message), and list the regex-log tree at that commit (git/trees ?recursive=1, filter regex-log/). Also check whether main has since changed regex-log/tests/test_outputs.py (fetch the main raw URL, cmp) — a drift note, not a defect.",
     "VERDICT: reopen-<n_identical>/5-drift-<yes|no>"),
    ("R36ProbeRerun", "executor", ["operability", "freshness"],
     f"Re-run the frozen probe: `cd {L} && python3 plans/regex_log_probe.py --lane .` twice (cmp each to {E36}/regex-log-probe.txt), then under `uv run --no-project -p 3.13 python3 ...` (the version tests/test.sh pins) and `-p 3.12` and `-p 3.11`, with PYTHONHASHSEED=1 and 99, and from a different cwd with `--lane {L}`. Record every byte difference and its cause (Python re behaviour, message text, path). Run `python3 plans/round36_c2_verify.py --lane .` read-only in the lane and paste its output (expected: defects remain, W5 may read the entry absent).",
     "VERDICT: probe-deterministic-<yes|no>-py313-<same|diff>-py312-<same|diff>-py311-<same|diff>"),
    ("R36ProbeHarnessMut", "executor", ["calibration", "operability"],
     f"Attack the probe HARNESS ({L}/plans/regex_log_probe.py run_grader monkeypatches the grader module's Path). In copies under {B}/R36ProbeHarnessMut/ (a mini lane tree with plans/ and corpus/evidence/round36/tb2-regex-log/): (a) break the Path patch so the grader reads the real /app/regex.txt — valid cases must turn fail (/app/regex.txt does not exist on this host; confirm); (b) give every case the reference regex — mismatches must become >0 and exit 1; (c) flip one prediction in the copied cases — mismatches=1; (d) tamper one byte of the copied test_outputs.py — the probe must REFUSE exit 2; (e) make the temp directory name leak into an assertion again (revert Amendment 1's .replace) — receipts must differ between two runs. Paste outputs and exit codes.",
     "VERDICT: harness-mutants-<detected>/5"),
    ("R36IdGuard", "executor", ["coverage", "calibration"],
     f"Run the addendum §10 id-collision check exactly, with A={W}/assimilation (mkdir -p): reg-ids from {L}/corpus/SOURCES.md and staged-ids from /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md using the 0-3-space pattern `^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}`, comm -12 → $A/collisions. Prove the guard: a scratch registry under $A/guard-proof/ with an indented `  | S002 |` row and a staged copy containing S002 must yield nonempty collisions. Derive the quarantine slice with the §10 awk (R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md, lane `kengaku`) into $A/quarantine-slice. Paste counts and the first/last staged id. Then state whether S108-S110 (this round's rows) collide with any staged id and what a renumber map would look like if the held round-35 package were adopted later.",
     "VERDICT: collisions-<n>-guard-<ok|broken>-slice-<n>"),
    ("R36NestedPaths", "executor", ["calibration", "operability"],
     f"Enumerate the 21 committed paths at the lane branch tip matching `^\\.ufo/waves/round-3[0-9]/.*/\\.ufo/waves/round-` (`git -C {L} ls-tree -r --name-only master | grep -E ...`; paste the list). Grep every lane doc ({L}/LOG.md, SCORECARD.md, README.md, SKILL.md, PROVINCE.md, corpus/README.md, corpus/QUALITY.md, corpus/lessons/*.md, corpus/defects*.jsonl, plans/*.py|md) for any citation of those paths, of `R34ReviewCounterC1Attacks` and of their basenames' parent dirs; report each hit with file:line and whether deleting the paths from the tip would break an evidence pointer. Read {F}/scripts/hyaku/jj-lane.sh (read-only; do not run commit/recover) to say whether `jj-lane.sh commit … -- <deleted tracked path>` stages deletions of tracked files and what its deletion guard requires. Also count the 912 round-28 nested paths (`.ufo/waves/round-28/scratch/…/.ufo/waves/…`) and list which lane docs cite them.",
     "VERDICT: nested-21-pointer-safe-<yes|no>-hits-<n>"),
    ("R36TipSweep", "executor", ["freshness", "operability"],
     f"No-harm baseline BEFORE landing. Make a clean shared clone of the lane tip (fixture rule; sparse everything except `/.ufo/waves` — use patterns `/corpus /plans /SCORECARD.md /grader.py /SKILL.md /PROVINCE.md /LOG.md /README.md /AGENTS.md /SHONEN.md /.ufo/waves/round-34 /.ufo/waves/round-35 /considerthese`) and run, recording exit code and last output line of each: `python3 grader.py`, `python3 grader.py --selftest`, `python3 plans/defect_ledger.py --lane .`, `python3 plans/round35_c1_verify.py --lane .`, `python3 plans/round35_hardening.py --lane . --skip H6`, `python3 plans/state_check.py --summary`, `python3 plans/registry_check.py --summary`, `python3 plans/benchmark_spec_audit.py --summary`, `python3 plans/config_projection.py --summary`, `{F}/scripts/sources-census.sh validate --root {F} kengaku`. Anything non-zero is a pre-existing condition to report with its cause (missing ignored file, working-tree dependency, host drift), not a defect of this round.",
     "VERDICT: tip-sweep-<n_green>/<n_total>"),
    ("R36ToolathlonRecount", "executor", ["calibration"],
     f"Recount the denominators in {E36}/toolathlon-package.md (byte copy of /home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/toolathlon-grader-behaviour-probe-2026-10-23.md — cmp them and record the sha256) with your own script: parse the `## Outcome` table, sum the three leaf rows (callable 13 + not-callable 23 + exec-failed 1), compare with the stated `of 38`; check every other numeric claim in the package that sums or divides (4 + 9 = 13 etc.). Open the staged S130 row in /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md (file:line) and quote its locator (<=25 words). Draft the exact erratum line the round-36 lesson `## Gate` must carry, starting `Erratum (round 36):`, containing `S130`, the expression `13 + 23 + 1 = 37` and `denominator 38`, and prove it satisfies {L}/plans/round36_c1_verify.py `r35_d4` by running that function (import the module, point `lane` at a mktemp lane tree holding the committed package copy and a fixture lesson with the line under a `## Gate` heading).",
     "VERDICT: recount-<sum>-vs-<stated>-erratum-line-verified"),
    # ---- scribes (9) ----
    ("R36EntryDraft", "scribe", ["coverage", "depth"],
     f"Draft the C2 knowledge entry at {B}/R36EntryDraft/entry.md. It must satisfy counter W3/W5 exactly (read {L}/plans/round36_c2_verify.py): lines 1-3 `source: S108 — {RAWRL}/tests/test_outputs.py — <anchor>` / S109 test.sh / S110 instruction.md (bare pinned URL, no fragment); line 4 `verified-at: 2026-10-25`; line 5 `recheck: 180d — <action>`. Sections: summary; what the grader checks (static reading of {CAP}/test_outputs.py: the single test, the fixed 25-line log, the expected nine dates, `re.findall` with MULTILINE, pattern read+strip, compile check); the instruction-requirement → enforcing-assertion map built from the receipt {E36}/regex-log-probe.txt (include its summary line `cases=24 observed_pass=8 observed_fail=16 mismatches=0` verbatim; name which of the 24 cases are the unenforced-requirement findings: leading-zero IPv4 octets, digit-adjacent dates, other-width years, Feb-29 permitting side, month-length validity on valid-IP lines, hard-coded alternation of the nine expected dates); test.sh reward mapping (read {CAP}/test.sh); the oracle (solve.sh) as a tier-C/own-reading note — only claims you can locate; `## Negative space` (what this does NOT show: task validity, hidden tests, agent behaviour, any other TB2 task; include a `falsif`-able line: which re-run would falsify each claim); `## Located quotes` table `| Claim supported | “quote” | `file:line` |` with >=10 rows, every quote 3-25 words, byte-verified by `grep -nF` against {CAP} (paste the grep outputs in your report), distinct lines. No literal mismatch claims: the receipt says mismatches=0; if a case line you cite differs, say so.",
     "VERDICT: entry-drafted-<n_quotes>-quotes"),
    ("R36RowsDraft", "scribe", ["coverage"],
     f"Draft the three registry rows S108-S110 for {L}/corpus/SOURCES.md in its exact 11-column schema (read its header and the last 5 rows; CORPUS.md SOURCES contract at {F}/CORPUS.md §SOURCES.md). source = title + ' — ' + bare pinned URL ({RAWRL}/tests/test_outputs.py etc.), kind code/docs, tier A, scope (the maintainer's task-grader code / runner / specification for this one task at the pinned commit), anchor (line range + commit), teaches (>=8 words, three DISTINCT cells, one grounded learner benefit each), status mined, opened 2026-10-25, recheck 180d, used-by corpus/knowledge/tb2-regex-log-grader.md. No literal or escaped `|` in any cell. Also draft the lesson `## Gate` source block: per row URL, access date 2026-10-25, a <=25-word located quote verified by grep -nF against {CAP}. Validate in scratch: copy {L}/corpus/ to {B}/R36RowsDraft/validate/corpus/ plus a stub entry file at the used-by path, append your rows to the Registry table, and run `{F}/scripts/sources-census.sh validate --file {B}/R36RowsDraft/validate/corpus/SOURCES.md`; report exit code and any E/W finding.",
     "VERDICT: rows-drafted-census-<exit>"),
    ("R36ReadmeDraft", "scribe", ["coverage"],
     f"Draft {L}/corpus/README.md additions for C2 (do not edit the file): (1) one index row in the knowledge table, exact form `| `knowledge/tb2-regex-log-grader.md` | <what> | S108, S109, S110 (terminal-bench-2 @ 2fd12b88) |`, placed after the tb2-protein-assembly-grader row (line 68); (2) one `## Coverage map` bullet in the style of the round-35 bullet (line 257) naming knowledge/tb2-regex-log-grader.md and stating exactly what is and is not discharged; (3) a `*Partly discharged round 36*` sub-bullet for the §Frontier task-spec item (after the round-35 sub-bullet at line 282); (4) a `### Round-36 evidence` subsection listing corpus/evidence/round36/ files, corpus/defects-round35.jsonl and plans/pkg_gate.py (describe it as landing this round only if it exists at integration — mark that line `[if landed]`). Bound every sentence to what the receipt and captures show. Output the draft with line anchors (which existing line each insertion follows).",
     "VERDICT: readme-draft-<n>-insertions"),
    ("R36LessonDraft", "scribe", ["calibration", "coverage"],
     f"Draft {B}/R36LessonDraft/round-36.md (the lane lesson corpus/lessons/round-36.md). Sections: header (baseline b662a5d6, freeze 3241b86c, Amendment 1 acbda2f3); `## Gate` table (C2 entry admit-candidate; S108-S110 rows with URL/access date/<=25-word located quote; assimilation set: considerthese/2026-10-25.md proposal 2(c) mined as a lesson/QUALITY criterion citing the file and date; >=1 reject and >=1 admit from the merge/kengaku set — read /home/vgpnk/Projects/shokuknow/merge/kengaku/MERGE-REPORT.md and use round 35's lesson {L}/corpus/lessons/round-35.md Gate rows as the pattern; leave the final admit/reject cells as `<scout verdict: R36ScoutMergePkg>` placeholders only for facts you cannot yet know); one line starting `Erratum (round 36):` (S130 package denominator 38 vs 13 + 23 + 1 = 37, denominator 38) — copy it from {B}/R36ToolathlonRecount.md if present, else write it to this exact form; `## Mistakes` as a markdown TABLE `| class | evidence pointer | captured-by | fix |` with rows for: (1) round-35 frozen counters accepted junk (class vacuous; evidence round35-verifier-spotcheck.md:86 and plans/round35_hardening.py; captured-by none; fix pkg_gate + battery — show red-before via claims/control-c1-legacy.txt LEGACY accepted=7/7); (2) frozen probe was not byte-deterministic (class reference-drift; evidence regex-log-probe-first-run.txt:21-22, claims Amendment 1; captured-by none; fix: `<tmp>` normalisation and a W5 re-run); (3) round-35 D1 working-tree check; (4) ledger rows split per opened round (corpus/defects-round35.jsonl) so the frozen r35 checker keeps passing — class scope; plus a round-36 disposition table for the six routed items of round-35-verifier-spotcheck.md §5; `## Census` (before: {W}/claims/census-before.txt); `## Spot-check` placeholder for the non-author closure. Do not claim any result not yet measured; mark unmeasured numbers `<TBD at landing>` explicitly.",
     "VERDICT: lesson-drafted"),
    ("R36QualityDraft", "scribe", ["calibration"],
     f"Draft the next QUALITY.md criteria as `## Round36 criterion — a counter of record is attacked by its own junk` with ids Q24 (and Q25 if a second is warranted), in the style of {L}/corpus/QUALITY.md lines 255-295 (read them and Q22/Q23). Q24: a counter of record for an admitted-entry package must reject a frozen battery of single-property junk mutants built from the genuine package AND accept the genuine package, and a seat-built cheapest-junk must be scored by it BEFORE any data; cite lessons/round-36.md §Mistakes (1), claims/control-c1-legacy.txt (LEGACY accepted=7/7), plans/round36_c1_verify.py, the considerthese/2026-10-25.md proposal 2(c) tip-receipt clause. Q25 (only if you can ground it): a frozen instrument that fails its own determinism on first run is amended only before any seat scores, with a digest-pinned amendment note and a byte-identical `--dry` case table (claims Amendment 1; open L0 questions revenger round-68/69, kumitate round-63/64). Each criterion needs an executable check and a stated limit. Do not edit QUALITY.md.",
     "VERDICT: quality-drafted-<n>-criteria"),
    ("R36SkillDraft", "scribe", ["operability", "depth"],
     f"Draft additions to {L}/SKILL.md (do not edit): (1) registry rows in the exact column format of the `## Gate/probe registry` table (lines ~562-575; read them) for `package-gate` (`python3 plans/pkg_gate.py package --root DIR --spec plans/pkg-spec-r35.json [--rerun] [--require-clean-tree]`, exit map 0 accept / 1 reject / 2 usage-setup, self-test = `python3 plans/round36_c1_verify.py --lane .` battery), `round36-c1-battery` (gate) and `regex-log-probe` (probe; `python3 plans/regex_log_probe.py --lane .`, exit 0 all predictions matched / 1 mismatch / 2 grader digest refused; pinned values: grader sha256 345c3bd0…, probe digest in plans/round36_c2_verify.py); (2) a short section `## TB2 regex-log grader — round36` under the existing task-spec observability sections (read lines ~676-704 for style) that states, with file:line pointers to the receipt, what the pinned grader enforces and what it does not, plus what an agent should do (read tests/ before trusting a pass; a pass on the fixed log is not evidence of instruction compliance). Mark any line that depends on pkg_gate.py existing `[if landed]`.",
     "VERDICT: skill-drafted-<n>-rows"),
    ("R36ProvinceDraft", "scribe", ["adjacency", "coverage"],
     f"Draft the PROVINCE.md round-36 paragraph (do not edit the file): read {L}/PROVINCE.md (the round-28/29/35 paragraphs for style and the refusal wording 'does not run a benchmark, certify a task, or own … runtime task validity'). State exactly what the regex-log probe adds (offline execution of one pinned grader on synthetic candidate patterns), what it never claims (task validity, agent performance, hidden tests, other tasks), and which sibling lanes are adjacent (tameshi/kotoba/kumitate/chousa — verify by reading their PROVINCE.md heads; cite file:line). Keep it to one paragraph of <= 140 words plus one `Reported out` line if a sibling owns anything touched.",
     "VERDICT: province-drafted"),
    ("R36ConsiderMine", "scribe", ["calibration"],
     f"Mine {L}/considerthese/2026-10-25.md against round 35's and this round's actual implementations: proposal 2 clauses (a) re-run every closed defect's check at tip forever [{L}/plans/defect_ledger.py], (b) block pre-registration when a class recurs twice, (c) tip-receipt validator [round 36: plans/pkg_gate.py `--rerun` + R35-D1]. For each clause: implemented / partly / not, with file:line, and what is still missing. Check proposals 1 and 3 for anything round 36 can honestly claim or must leave open (proposal 3's decision packet exists as L0 `kengaku | round-33` — find its line in {F}/.ufo/l0-questions.md and quote it, <=25 words). Draft the lesson paragraph and the SCORECARD/LOG sentence that states which clause this round mines and the remaining debt, with no overclaim.",
     "VERDICT: considerthese-mined-<implemented>/3"),
    ("R36PlanNext", "scribe", ["calibration", "coverage"],
     f"Draft `### Planned (round 37)` for SCORECARD.md and the matching LOG.md next-iteration line. Inputs: {B}/R36ScoutNextTasks.md and {B}/R36ScoutMergePkg.md if they exist by the time you finish (read them last; if absent, plan from {L}/SCORECARD.md `### Planned (round 36)` and the C1/C2 frozen limits). Two candidate directions, each with the opened source that would ground it and a do-nothing control named: (a) a third TB2 grader of a different class (service/process or file-tree grader), (b) a novelty claim on the thin-mutant instrument measured across two tasks (which requirement classes graders leave unenforced: boundary adjacency, validity-by-month, leading zeros, hard-coded fixed inputs) with a prior-art-checked construct. Keep the frozen-predicate/control sentence discipline.",
     "VERDICT: plan-drafted"),
    # ---- scouts (5) ----
    ("R36ScoutMergePkg", "scout", ["coverage", "adjacency"],
     f"Screen /home/vgpnk/Projects/shokuknow/merge/kengaku/ (read-only: MERGE-REPORT.md, knowledge/, SOURCES.append.md) for ONE theme matching C2 (benchmark graders / fixture probes / predicate input types) and the lane's PROVINCE ({L}/PROVINCE.md). Specifically re-screen the round-35 HELD candidates `grader-predicate-input-types.md` and `grader-fixture-probe-stage3.md` (see {L}/corpus/lessons/round-35.md Gate rows and {L}/.ufo/waves/round-35/build/R35ScoutMergePkg.md): does either duplicate ground already held ({L}/corpus/README.md index), cite rows that collide with the registry (S001-S107), or need sources the lane has not opened? Give admit-candidate / refuse / hold verdicts with reason + flip condition; for any admit-candidate list the staged row ids and the URL of each cited source you opened yourself (URL + <=25-word located quote). Do NOT bulk-append anything.",
     "VERDICT: package-<n_admit_candidates>-admit-<n_refuse>-refuse-<n_hold>-hold"),
    ("R36ScoutPriorArt", "scout", ["novelty", "coverage"],
     "Prior-art check for the C2 instrument pattern: executing a benchmark task's own grader on synthetic, requirement-targeted candidate artefacts to map which instruction requirements it enforces, here for a pattern-valued answer (a regex file) graded against a fixed public test log. Search for: graders that can be satisfied by memorising the visible test fixtures (hard-coded answers, 'test-set leakage' in verifier tests), benchmark task-validity audits that count unenforced requirements, regex/pattern-synthesis benchmark graders and their false-accept rates, Terminal-Bench / Harbor guidance on hidden vs visible tests, mutation testing of verifiers. Fetch each hit (URL + <=25-word located quote + location). Verdict: is the observation (a fixed-log pattern grader accepts a literal alternation of its expected outputs and leaves boundary/validity requirements unenforced) novel, incremental, or established? Do not claim novelty without evidence; list the 6 strongest hits only.",
     "VERDICT: priorart-<n>-hits-novelty-<established|incremental|novel>"),
    ("R36ScoutTB2Visibility", "scout", ["coverage", "depth"],
     f"Open the Terminal-Bench 2.0 / Harbor docs and paper sections that say whether a task's `tests/` directory is visible to the agent during the run and when it is copied in (e.g. https://arxiv.org/html/2601.11868v1, harbor docs on verifier/tests, the TB2 README at {PIN}, harbor source `Verifier` upload of tests). The C2 entry says 'the nine expected dates are visible in the test file' — is that visible to the agent or uploaded only at verification? Report URLs + <=25-word located quotes. Also check whether the task's canary string and `[verifier] timeout_sec` in {CAP}/task.toml matter to the claim. Verdict decides how strongly the entry may phrase the hard-coded-alternation finding.",
     "VERDICT: tests-visibility-<hidden-until-verify|visible|unclear>"),
    ("R36ScoutNextTasks", "scout", ["coverage"],
     f"Survey 14 other TB2 tasks at the pin for the NEXT round's coverage move: via https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/{PIN}?recursive=1 pick tasks whose tests/test_outputs.py is small, python-only and offline-executable (examples to check: constraints-scheduling, count-dataset-tokens, distribution-search, dna-insert, extract-elf, filter-js-from-html, fix-git, cancel-async-tasks, log-summary-date-ranges, hf-model-inference — verify existence). For each: size of test_outputs.py, whether it needs a service/network/container state, what its grader is fed (string, file tree, process), and a one-line probe idea. Rank the top 3 with reasons. Fetch with curl; record sizes and sha256 of the three top files.",
     "VERDICT: next-tasks-<n>-surveyed-top-<name>"),
    ("R36ScoutReDocs", "scout", ["depth", "freshness"],
     "Open the Python `re` module documentation (https://docs.python.org/3/library/re.html) and locate <=25-word quotes for: (a) `re.findall` returning a list of tuples when the pattern has more than one group; (b) lookbehind requires a fixed-width pattern; (c) the MULTILINE flag behaviour of `^`; (d) `re.findall` returns empty matches as part of the result. Report URL + section heading + the quote for each, plus the doc's version string. These are candidate support for the regex-log entry's explanation of the extra-capture-group, empty-pattern and first-date cases; say whether each quote is needed (the entry already stands on the receipt) or optional. Do not propose a registry row unless the entry will cite it; if you do, draft the row in 11-column form (id S111, tier A, kind docs).",
     "VERDICT: redocs-<n>-quotes-located"),
    # ---- connectors (3) ----
    ("R36ConnSibling", "connector", ["adjacency"],
     "Sibling-overlap scan for round 36 surfaces: which other fleet lanes (/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md, corpus/README.md) claim benchmark grader code, Terminal-Bench tasks, regex/pattern graders, package gates, or routed-defect ledgers (e.g. tameshi, kotoba, kumitate, chousa, kama, mori)? Read-only. For each hit: contested / adjacent / none, with file:line evidence. Note any sibling instrument kengaku should cite rather than duplicate, and whether any sibling already ships a junk-battery/mutation gate for admission counters (kumitate cap-run, revenger gates).",
     "VERDICT: sibling-<contested>-contested-<adjacent>-adjacent"),
    ("R36ConnDefectClasses", "connector", ["calibration", "adjacency"],
     f"Cross-round pattern: map every routed defect in {L}/corpus/lessons/round-{{29,30,31,32,33,34,35}}-verifier-spotcheck.md (read-only) to a class (untracked work, receipt/manifest mismatch, scorecard misstatement, false refusal, scratch bloat, phantom hash, report-before-commit, counter-accepts-junk, ...). Count recurrences per class and populate proposed `recurrence_of` values for the four rows of {L}/corpus/defects-round35.jsonl. Flag classes that recur >=2 times with no standing check, and say whether the C1 battery's 14 fixtures cover each recurring class (the 'block pre-registration at second recurrence' clause of considerthese proposal 2(b) is not implemented — say what the smallest honest implementation would be).",
     "VERDICT: classes-<n>-recurring-<n>-uncovered-<n>"),
    ("R36ConnAmendment", "connector", ["calibration", "adjacency"],
     f"Cross-lane pattern: this round amended a frozen probe before any seat scored (Amendment 1 in {L}/plans/round-36-claims.md). Read the open L0 questions about frozen-instrument repair in {F}/.ufo/l0-questions.md (revenger round-68 and round-69, kumitate round-63 and round-64, tabi round-22) and the sibling lanes' corresponding reports (read-only: {F}/.ufo/reports/round-6[3-9]/*.md and any `ratchet`/`amend` text) to extract the common rule they each applied and how each report worded the verdict. Recommend precise wording for kengaku's report: is Amendment 1 a ratchet within the declared rule, a new revision, or a rule change? Cite file:line for each sibling precedent. Do not append to l0-questions.md.",
     "VERDICT: amendment-precedents-<n>-recommend-<ratchet|revision|rule-change>"),
    # ---- reviewers (3) ----
    ("R36RevClaims", "reviewer", ["calibration"],
     f"Review the frozen claims {L}/plans/round-36-claims.md against both counters ({L}/plans/round36_c1_verify.py, {L}/plans/round36_c2_verify.py) and controls ({W}/claims/). Is each predicate the same sentence in plan, code and receipt label? Can any check pass on a state that does not deliver the claimed surface (false green)? Is any check unpassable on a truthful landing (false red: e.g. R35-D2 untracked_anywhere on the landing clone, R35-D1 --rerun needing uv/biopython, W4 `>=43`, W6 census)? Are C1/C2 causally separable as stated? Is Amendment 1 correctly bounded? Cite file:line for every finding.",
     "VERDICT: claims-review-<n>-false-green-<n>-false-red"),
    ("R36RevProbePred", "reviewer", ["coverage", "calibration"],
     f"Review the 24 frozen probe cases in {L}/plans/regex_log_probe.py build_cases against {CAP}/instruction.md and {CAP}/test_outputs.py: is each requirement label faithful to the instruction text; does each mutant isolate ONE requirement (check the receipt's assertion= column {E36}/regex-log-probe.txt: e.g. does `ip-no-right-boundary` die on the invalid-IP lines for a reason other than the missing boundary?); is any 'pass' case (reference-lenient-days, ip-leading-zeros-allowed, date-boundary-letters-only, hardcoded-expected-dates, year-any-digit-count, padded-file, feb-29-rejected) an instruction violation the grader accepts, and is that described correctly; which instruction sentences have NO case. Verify by running the pass cases yourself against your own copy of the 25 log lines.",
     "VERDICT: probe-review-<n>-confounded-<n>-uncovered"),
    ("R36RevBattery", "reviewer", ["calibration"],
     f"Review the C1 battery in {L}/plans/round36_c1_verify.py (build_package_fixtures, build_line_fixtures, battery, r35_d1..d4) against the four routed items {L}/corpus/lessons/round-35-verifier-spotcheck.md:86-89. Does each fixture isolate one defect class; can a gate satisfy `false_green=0` without implementing the class (e.g. by rejecting anything whose entry differs from the genuine bytes)? Is the `P0 genuine accepted` + `L1/L4 genuine accepted` set enough to stop a reject-everything gate (see {W}/claims/control-c1-reject-all.txt: false_red=3)? Is the R35-D2 observation (untracked_anywhere on the real lane) satisfiable at the landing tip by honest means (all wave evidence committed)? Name any fixture that would not be a fair test of a correct hardened gate.",
     "VERDICT: battery-review-<n>-unfair-<n>-gameable"),
    # ---- critics (3) ----
    ("R36CritC2Counter", "critic", ["calibration"],
     f"Attack the C2 counter {L}/plans/round36_c2_verify.py: find the cheapest package that passes W1-W6 WITHOUT the claimed work (e.g. an entry whose located quotes are distinct 3-word fragments from one boilerplate line each, rows whose teaches cells are distinct filler of 8 words, a receipt produced by the real probe but an entry that contradicts it, an entry that names no mismatch because the receipt has none). Build it in a fixture clone (sparse /corpus /plans; copy {E36}/) and score it. If any junk package scores checks=6 defects=0, that is a decisive finding: report the exact bytes. Also test whether W5's `match=NO` naming rule can be dodged.",
     "VERDICT: cheapest-junk-c2-<defects>-defects"),
    ("R36CritBattery", "critic", ["calibration"],
     f"Attack the C1 battery as an overfitting trap: write {B}/R36CritBattery/overfit_gate.py, a gate that passes `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` WITHOUT hardening anything — by recognising fixtures (marker strings such as `junk`, the stray file name `round35_scratch.py`, the stub-probe shape, the swapped citation order, the altered capture's tiny size, git state). Install it in a fixture clone (see the gate task in the wave context for how: copy plans/regex_log_probe.py, round36_c1_verify.py, pkg-spec-r35.json, defects-round35.jsonl, {E36}/) and run the battery. If it scores clean, the battery is gameable: list each recognised cue and say which fixture property removes it. Report exact output.",
     "VERDICT: overfit-gate-<clean|caught>-cues-<n>"),
    ("R36CritScope", "critic", ["adjacency", "coverage"],
     f"Attack C2's scope against {L}/PROVINCE.md (round-28/29/29a2/35 paragraphs: 'static LLM-evaluation interpretation', 'does not run a benchmark, certify a task, or own … runtime task validity'). Does executing the pinned regex-log grader on synthetic candidate regexes cross that line, or is it the same class as round 35's protein-assembly probe and round 29's projection? What wording must the entry/PROVINCE use so it does not claim task validity, regex correctness for log processing, or model performance? Is 'coverage' the right axis name for this surface (addendum: name the axis by the surface changed — a second task's grader is new surface, but the instrument is re-used: could a reader call it quality work on new inputs)? Give the wording fixes.",
     "VERDICT: scope-<inside|crosses>-<n>-wording-fixes"),
    # ---- mutation-testers (3) ----
    ("R36MutC2W2W3", "mutation-tester", ["calibration"],
     f"Mutation-test C2 checks W2 and W3 ({L}/plans/round36_c2_verify.py) in a fixture clone where a passing package exists (build one: sparse /corpus /plans; copy {E36}/; append three rows S108-S110 passing W2; write an entry passing W3 — reuse {B}/R36EntryDraft/entry.md and {B}/R36RowsDraft/ if present, else minimal real ones with quotes you verify with grep -nF against {CAP}). Mutants one at a time: row with 10 cells; escaped `\\|`; /tasks/ in URL; #L fragment on URL; tier B; status queued; used-by with second path; duplicate S108 row; row indented 4 spaces (must be IGNORED by the census regex — document); two rows with identical teaches; teaches of 7 words; quote off by one line; quote with one changed char; 26-word quote; 2-word quote; a straight-quote row (unparsed); eight copies of one quote; missing falsifier; recheck without cadence; swapped source lines. Report killed/survived; any survivor is a false-green finding.",
     "VERDICT: w2w3-mutants-<caught>/<total>"),
    ("R36MutC2W4W5", "mutation-tester", ["calibration"],
     f"Mutation-test C2 checks W1, W4 and W5 in the same kind of fixture clone with a passing package: SHA256SUMS missing instruction.md; digest of test.sh altered; listed file absent; test_outputs.py one byte edited (must go red); index row without S109; coverage bullet removed; a 44th knowledge file not indexed; index row duplicated; receipt one byte changed; receipt line order swapped; summary line removed from the entry; receipt with a `match=NO` line not named in the entry; probe file edited (digest) ; probe stub printing the receipt (must be caught by the frozen probe digest). Report kill/survive per mutant; run each with `python3 plans/round36_c2_verify.py --lane <clone>` and paste the DEFECT line.",
     "VERDICT: w1w4w5-mutants-<caught>/<total>"),
    ("R36MutLedgerChecks", "mutation-tester", ["calibration"],
     f"Mutation-test the four ledger checks r35_d1..r35_d4 and the row/predicate logic in {L}/plans/round36_c1_verify.py in a fixture clone: d3 — add one extra committed nested path under .ufo/waves/round-34/…/.ufo/waves/round-34/x in a fixture commit (fixture repo identity `fixture <fixture@invalid>`, `-C` the fixture only), a path at round-28 (must NOT count), and a path at depth 1 (must NOT count); d4 — a lesson whose erratum line has the wrong sum (36), omits S130, sits outside `## Gate`, appears twice, or states the right numbers with a different denominator; the committed package copy edited so the table sums to 38 (the line must then be a defect); ledger file — unknown check name, status `Closed`, a fifth row, an empty file, a missing file, malformed JSON (the counter must fail closed, never exit 0). Paste exit codes and the counted `mismatches`.",
     "VERDICT: ledger-mutants-<caught>/<total>"),
    # ---- critic hypothesis probe (1) ----
    ("R36CritUnenforced", "critic", ["coverage", "novelty"],
     f"Hypothesis H: the pinned regex-log grader leaves at least 3 instruction requirements unenforced beyond the probe's frozen cases. Test it with 12 NEW candidate regexes you design (not the frozen 24; write them in {B}/R36CritUnenforced/extra_cases.py with predictions written BEFORE running, then run them through the grader via plans/regex_log_probe.py's run_grader): e.g. accept Feb 30 on valid-IP lines, accept `2000-02-30` explicitly, accept 5-digit years, accept an IPv4 with a 4th-octet `00`, treat `.` after the IP as part of an alnum boundary, ignore the MULTILINE flag, match dates across a line break, depend on a trailing newline in the file. Report predicted vs observed per case and the final count of unenforced requirements with the minimal witness regex for each. State clearly these are supplementary, outside the frozen C2 predicate.",
     "VERDICT: unenforced-<n>-new-mismatches-<n>"),
]


def main():
    items = []
    for name, role, axes, task, verdict in ITEMS:
        prompt = (f"{GS}# Target\nkengaku round 36 wave 1 item {name} ({role}).\n# Task\n{task}\n"
                  f"# Acceptance\nReport at your `Report:` path (absolute: {B}/{name}.md); end with {verdict}.\n")
        items.append({"name": name, "role": role, "axes": axes, "prompt": prompt,
                      "milestone": "kengaku r36 wave 1 (build + first falsifiers)"})
    assert len({i["name"] for i in items}) == len(items) == 40, len(items)
    spec = {"wave": "kengaku-r36-build",
            "milestone": "kengaku round 36 wave 1: C1 hardened package gate + routed defects, C2 TB2 regex-log grader admission + probe, frontier step",
            "reportDir": ".ufo/waves/round-36/build", "context": CONTEXT, "items": items}
    pathlib.Path(f"{W}/build-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    from collections import Counter
    print(Counter(i["role"] for i in items))


main()
