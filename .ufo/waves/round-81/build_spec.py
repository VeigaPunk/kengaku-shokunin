#!/usr/bin/env python3
"""Build the round-81 v1 wave spec (14 seats) and print the path."""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
SCRATCH = "/fast/scratch/hyaku/kengaku-r81"
BASE = "4e833e9fee8022d24559535178c6fe32b2cd62f1"
FREEZE = "4d896e0daf8831ef7a0016bf3c944d11ba465f70"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = f"""# Goal
Kengaku lane, round 81 — wave w1 (v1, 14 seats: build + attack). You are ONE seat of this wave.
The round's two claims are FROZEN at /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-81-claims.md (freeze commit `{FREEZE}`); read it in full before any command. Never re-open a frozen predicate, universe rule, control or kill rule.

R81-C1 (coverage, lowest non-retired axis, held at its L0 cap) = the two members the frozen selection rule derives at the base revision — `unattempted`, stdlib-only, file-artifact/serialization-schema population members whose round-52 grader capture carries the maximum assert count: `log-summary-date-ranges` and `vulnerable-secret` — become `executed`: each names a tracked receipt `corpus/evidence/round81/<member>-probe.txt` whose first line is `# tb2 <member> grader probe`, whose stamp block pins SUBJECT_CAPTURE/SUBJECT_SHA (the committed round-52 capture and its sha256 at the measured tree), TOOL/TOOL_SHA, HOST_PYTHON (`python3 -V`), HOST_OPENSSL (`openssl version` or `absent`), LANE_TIP (reachable), WORKTREE clean, COMMAND, EXIT 0, MINTED_BY/MINTED_BY_SHA, whose OBSERVATIONS block equals the instrument's stdout at the measured tree, and whose ledger row is `executed` with `subject=tb2-header`, the receipt's own form as `verdict`, `round=81`. Counter: `python3 plans/round81_c1_new_members.py --lane .` (before at `{BASE}`: `DEFECTS n=2`, rc 1).

R81-C2 (calibration, held at ceiling 10, exercised) = the round-80 verifier spot-check's six routed defects `U1`…`U6` (`corpus/lessons/round-80-verifier-spotcheck.md` §5) are discharged as `corpus/routed-findings.jsonl` rows `R80-U1`…`R80-U6`: status closed, a `source` resolving to the line that carries the short id, a `close` naming a tracked repair artifact (never the spot-check) whose bytes carry the id and the row's `evidence_literal`, and a `check` that exits 0 at the tip and FAILS when the repair is reverted to `{BASE}`. Counter: `python3 plans/round81_c2_spotcheck_debt.py --lane .` (before: six `DEBT-UNREGISTERED` + `INDEX-MISSING`, `DEFECTS n=7`, rc 1).

# Rules (binding on every seat)
- Write scope: your OWN scratch dir `$HYAKU_SCRATCH/kengaku-r81/<your-seat-name>/` with `HYAKU_SCRATCH` defaulting to `/fast/scratch/hyaku` (mkdir -p it; delete it before you yield — `trap 'rm -rf -- "$S"' EXIT`), the single report file named by your `Report:` trailer, and (only where your item names one) one deliverable file under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-81/w1/`. Everything else is READ-ONLY: never write, commit, push or run a mutating git/jj command in /home/vgpnk/Projects/shokunin/kengaku-shokunin, in the fleet repo, in a sibling lane, or in any domain source tree. Never edit `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `corpus/QUALITY.md`, the ledger or any plan/gate — the L1 integrates; you deliver bytes and a report.
- Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/kengaku-shokunin — write it at /home/vgpnk/Projects/shokunin/kengaku-shokunin/<that path>. Report file names are given per item.
- Scratch: one `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/clone` per seat where a clone is needed (never a full clone, never a mirror of the lane); no `build/` trees; no `/tmp` path is citable evidence.
- Fixture repos: `D=$(mktemp -d -p $HYAKU_SCRATCH/kengaku-r81/<seat>) && git -C "$D" init -q`; every later git/jj call names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit. Never run `git commit`/`jj` with a throwaway identity anywhere else.
- Measure at the current lane tip (`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master`). The freeze commit is `{FREEZE}`; the base revision every "before" state names is `{BASE}`.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate, record tool/version/channel/reason in your report). **pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide**; install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or file an L0 question. Never `pacman -Sy/-Syu/-U/-R`.
- Never call the `ask` tool: the round is unattended. Leaf member: no subagent dispatch (executors may spawn one read-only labrat probe; every other role stays a leaf; no seat runs its own swarm).
- Do not trust the counters: read bytes yourself. An unrun check has not passed; never invent a number. Report every failure with its exact command and output.

# Judging
Every claim, number and gate in this lane is judged on committed bytes; a report line without a command and its output is not evidence. Attack seats: state what you attacked and what you could not break."""


def item(name, role, report, body):
    return {"name": name, "role": role,
            "prompt": GODSPEED + f"\n\n# Item {name} — role {role}\n\n" + body.strip() +
                      f"\n\nReport: .ufo/waves/round-81/w1/{report}\n"}


ITEMS = [
    item("ProbeLogSummaryR81", "executor", "ProbeLogSummaryR81.md", f"""
Write the offline replay instrument for the Terminal-Bench 2.0 `log-summary-date-ranges` grader.

1. Read the capture `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/log-summary-date-ranges/tests/test_outputs.py` (51 lines, sha256 in `corpus/evidence/round52/graders/SHA256SUMS`) and the frozen claims `plans/round-81-claims.md` §R81-C1.
2. Model the instrument on the executed file-artifact recipe: `plans/db_wal_probe.py` and `plans/round59_c1_openssl_probe.py` show the bwrap pattern (bind the capture read-only at `/tests`, a writable `/app`, import the capture's test functions from `/tests` and call them in file order, no pytest runner; a normal return is P, AssertionError or any other escaping exception is F).
3. Frozen case table, >= 8 cases with at least 4 P and 4 F, each staging a different `/app/summary.csv` end state: exact 15-row table (P); missing file (F); empty file (F); wrong header (F); 14 rows (F); 16 rows (F); one count changed (F); two rows swapped while the row count stays 15 (F); CRLF line endings (P); extra trailing blank line (P). Predictions are DERIVED from the case definitions in code (`predict_legs()`), never retyped.
4. Output exactly: one `CASE <id> predicted=<P|F> observed=<P|F> rc=<0|1>` line per case, then `cases=<n> observed_pass=<n> observed_fail=<n> mismatches=0`, then `PREDICATE R81-C1 pass`; first line `REV <hex commit>` from git. Exit 0 iff mismatches=0. Support `--lane`, `--work`, `--receipt`, `--selftest`.
5. Determinism: run it twice and paste both stdout hashes in your report. If bwrap is absent, report that instead of faking a run.
6. Deliver the instrument as `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-81/w1/ProbeLogSummaryR81.py` (that is the ONE deliverable path you may write outside scratch) and state its sha256 and a full run's stdout in your report. Do not edit `plans/`.
"""),
    item("ProbeVulnSecretR81", "executor", "ProbeVulnSecretR81.md", f"""
Write the offline replay instrument for the Terminal-Bench 2.0 `vulnerable-secret` grader.

1. Read the capture `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/vulnerable-secret/tests/test_outputs.py` (39 lines; three test functions, five asserts: existence, exact stripped equality with `FLAG{{...}}`, prefix/suffix/length) and the frozen claims `plans/round-81-claims.md` §R81-C1.
2. Same bwrap recipe and leg rule as `plans/db_wal_probe.py` / `plans/round59_c1_openssl_probe.py`: capture bound read-only at `/tests`, staged writable `/app`, the capture's own test functions called in file order.
3. Frozen case table, >= 8 cases with at least 4 P and 4 F, each staging `/app/results.txt`: exact flag (P); exact flag with a trailing newline and surrounding spaces (P — the grader strips); missing file (F); wrong flag (F); `FLAG{{` only (F: endswith); `FLAG{{x}}` (F: len>10); flag plus a trailing second line (F: stripped equality); truncated flag (F). Predictions DERIVED in code from the case definitions.
4. Output exactly: `CASE <id> predicted=<P|F> observed=<P|F> rc=<0|1>` per case, then `cases=<n> observed_pass=<n> observed_fail=<n> mismatches=0`, then `PREDICATE R81-C1 pass`; first line `REV <hex commit>`. Exit 0 iff mismatches=0. Support `--lane`, `--work`, `--receipt`, `--selftest`.
5. Determinism: run twice, paste both stdout hashes. If bwrap is absent, report that instead of faking a run.
6. Deliver as `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-81/w1/ProbeVulnSecretR81.py` (the ONE deliverable path you may write outside scratch) and state its sha256 plus a full run's stdout in your report. Do not edit `plans/`.
"""),
    item("EnvPinR81", "executor", "EnvPinR81.md", f"""
Measure the host state the two round-81 replays depend on, and the eigen probe's declared-unpredictable cases.

1. Produce `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-81/w1/host-state.txt` (the ONE deliverable path you may write outside scratch): the exact stdout of `python3 -V`, `openssl version`, `bwrap --version`, `uname -r`, `python3 -c 'import sys;print(sys.executable)'`, and the sha256 of `/usr/bin/bwrap` when it exists — each line labelled.
2. Re-measure the round-80 A2 finding: run `python3 plans/round57_c2_eigen_probe.py --lane . --work $S/eigen-<n>` six times and report the full-stdout sha256 of each run plus the projection hash under the frozen A2 rule (`REV` lines, `cases=`, `OBSERVED-U`, and `predicted=U` case lines excluded). State whether the two `predicted=U` speed cases are still the only varying lines, and whether any predicted case varies.
3. Read `plans/round-81-claims.md` §R81-C1's environment-pin paragraph and state, in one sentence, which host facts a round-81 receipt pins and which it does not.
4. Report every command with its output; a claim without a command is not evidence.
"""),
    item("C2ChecksR81", "executor", "C2ChecksR81.md", f"""
Write the repair-check machinery for R81-C2's six routed defects.

1. Read `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-80-verifier-spotcheck.md` §5 (defects `U1`…`U6`, lines 157-198) and `plans/round-81-claims.md` §R81-C2 (the repair table).
2. Write `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-81/w1/C2ChecksR81.py` (the ONE deliverable path you may write outside scratch): one subcommand per id (`u1`…`u6`) plus `--all`, each exiting 0 exactly when its repair holds **as described in the frozen table**, and non-zero otherwise. The checks must be repo-relative (run from the lane root) and must be able to fail: design each against the artifact the table names (`corpus/SOURCES.md` + `corpus/lessons/round-81.md` for U1, `SCORECARD.md` for U2, `corpus/evidence/round81/census-rows.txt` for U3, `corpus/evidence/round81/r80-u4-red-before.txt` + `corpus/QUALITY.md` for U4, `SKILL.md` for U5, `corpus/lessons/round-81.md` + `corpus/README.md` for U6).
3. Prove each check can fail: for every id, write a red fixture under your scratch where the repair is absent and show the check exits non-zero there and 0 on a green fixture you build from the frozen table's text (a small fixture tree is enough). Paste the transcript.
4. Also state the exact one-line `check` command string you recommend for each routed-findings row (`bash -lc`-compatible, repo-relative, no absolute lane path), and its `evidence_path` and `evidence_literal`. Do not register rows — the L1 integrates.
"""),
    item("U4RedBeforeR81", "executor", "U4RedBeforeR81.md", f"""
Show M80-1's claimed failure actually failing (R80-U4).

1. Read `corpus/lessons/round-80.md` M80-1 and `corpus/routed-findings.jsonl`'s R79-V1 row's neighbourhood for the claim: "removing the probe table's `prefix` makes the protein leg die with `ModuleNotFoundError: No module named 'Bio'` and the gate report `REPRODUCTION-EXIT`".
2. Reproduce it: read `plans/round80_probes.json`'s `protein-assembly` entry (its `prefix` names an interpreter), then run that probe's exact argv in your scratch with the prefix removed (i.e. with the system `python3`) and capture the exact failure text and exit code. If the probe insists on the prefix, run it with a prefix that points at a python without the dependency and say exactly what you changed.
3. Write `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-81/w1/r80-u4-red-before.txt` (the ONE deliverable path you may write outside scratch) containing `R80-U4` in its first line, the command, the exit code, and the failure text verbatim. If the failure does NOT reproduce on this host, say so plainly in the receipt and in the report — that is a finding, not a failure of your seat.
4. In your report state whether a committed selftest case already covers `REPRODUCTION-EXIT` (grep `plans/round80_c1_located_replay.py`), and whether a `QUALITY.md` criterion cites M80-1 today.
"""),
    item("U1AnchorR81", "executor", "U1AnchorR81.md", f"""
Compute the corrected S258 anchor data (R80-U1).

1. Read `corpus/SOURCES.md` row S258 and `corpus/lessons/round-80.md` lines 18-20 (the current, stale anchor: six sha256 prefixes `7923b6dc…, b32f4b37…, fd337d12…, 9179d62d…, 08c10b0d…, 82b910af…`, "lines 1-10 (subject at line 1, stamp at 3-10)").
2. Run `sha256sum corpus/evidence/round80/*-probe.txt` at the lane tip and record every full sha256 plus the first 8 hex of each, in the same member order S258 lists (`cancel-async-tasks`, `chess-best-move`, `distribution-search`, `largest-eigenval`, `openssl-selfsigned-cert`, `protein-assembly`).
3. Measure the real stamp range of those receipts today: the last `[A-Z_]+ ` stamp line's number and the `OBSERVATIONS_BEGIN` line number per receipt (`grep -n`), and state the range that covers the stamp block across all six.
4. Write `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-81/w1/r80-u1-anchors.txt` (the ONE deliverable path you may write outside scratch) with `R80-U1` on its first line, the six member→sha256 lines, the stamp range, and the exact command that produced them. Then state in your report the exact replacement `anchor` cell text a superseding SOURCES row should carry (<= 40 words of prose plus the data), and the sentence a lesson correction should carry.
"""),
    item("SourcesScribeR81", "scribe", "SourcesScribeR81.md", f"""
Draft the round-81 SOURCES rows and the frontier evidence, after opening the sources yourself.

1. Read `corpus/SOURCES.md`'s header (contract v1 tiers, registry table, 11 columns), the S255–S258 rows, `CORPUS.md` §SOURCES (the census contract), and `corpus/QUALITY.md` Q2/Q4.
2. Row A (R80-U1 repair): a superseding row `S259` whose `teaches` cell OPENS `supersedes S258 —` and states the corrected round-80 receipt anchors. Take the six sha256 values and the stamp range from `U1AnchorR81`'s deliverable if it exists at `.ufo/waves/round-81/w1/r80-u1-anchors.txt`; if it does not, compute them yourself with `sha256sum` — never invent a digest.
3. Row B (this round's own-work source): `S260` = the round-81 located-replay instrument set (`plans/round81_log_summary_probe.py`, `plans/round81_vulnerable_secret_probe.py`, `plans/round81_probes.json`, `plans/round81_c1_new_members.py`, `corpus/evidence/round81/<member>-probe.txt`), tier A own-work, scope and anchor written from the bytes, a <=25-word located quote from the receipts' first line.
4. Open at least one external primary source this round for the two new graders' class and record URL, access date, and a <=25-word located quote: the Terminal-Bench 2.0 repository at the pinned tree `2fd12b88` (`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md` and, if reachable, the task directories `tasks/log-summary-date-ranges/` and `tasks/vulnerable-secret/`) — a fetch that fails is reported as a failed fetch, not guessed. Give it a row (`S261`) only if it is actually opened; else say why not.
5. Draft the rows as a markdown table block in your report (`| S259 | … |` …), state each row's tier, status (`mined` only if it supports an entry), opened date, recheck, and used-by (planned `corpus/knowledge/tb2-file-artifact-replay-classes.md` for S260, `corpus/lessons/round-81.md` for S259/S261). Do not append them: the L1 integrates.
"""),
    item("LessonScribeR81", "scribe", "LessonScribeR81.md", f"""
Draft `corpus/lessons/round-81.md`.

1. Read `corpus/lessons/round-80.md` (shape: Mistakes table M80-1/M80-2, Gate blocks, corrections), `corpus/lessons/round-80-verifier-spotcheck.md` §5, and `plans/round-81-claims.md`.
2. Draft the lesson in the shape CORPUS v1 requires: a `## Gate` block for every SOURCES row this round opens (URL, access date, <=25-word located quote) — coordinate with `SourcesScribeR81`'s report if it exists at `.ufo/waves/round-81/w1/SourcesScribeR81.md`; a `## Mistakes` section with exactly two rows: `M81-1` = the round-81 class of defect you can actually evidence this round (candidate: an instrument or gate shipped without a registry row — same class as R80-U5, and say what criterion should have caught it, `captured-by`), `M81-2` = the round-80 dirty-worktree receipt class (R80-U2: a receipt whose `WORKTREE dirty` line contradicted the tip it cited; captured-by `none` unless you find one); a `## Corrections` block carrying `R80-U1` (superseded S258 anchor text) and `R80-U6` (the `REMINT minted=6 failed=0` line is not a receipt; cite the six committed receipts instead) with the old→new text.
3. Keep every statement to bytes you have read; an empty Mistake section is a failure of the round's frontier step, and a fabricated one is worse. If you cannot evidence a second mistake, say so and paste the sweep you ran.
4. Deliver the draft as markdown in your report; the L1 lands it.
"""),
    item("ReviewerC1R81", "reviewer", "ReviewerC1R81.md", f"""
Independently re-derive R81-C1 from committed bytes (read-only; do not run the lane's gates).

1. From `plans/grader-population-ledger.json` at `{BASE}` and the round-52 captures, re-derive the universe yourself: the `unattempted` stdlib-only file-artifact/serialization-schema members at the maximum assert count. State the candidate set, the counts, and whether the counter's printed universe matches.
2. Once `corpus/evidence/round81/<member>-probe.txt` exists at the lane tip, recompute each receipt's `SUBJECT_SHA` and `TOOL_SHA` with `sha256sum`, check `LANE_TIP` with `git merge-base --is-ancestor`, and re-run each instrument once in your own scratch clone, comparing the projection under the frozen A2 rule. Paste the comparison.
3. Verify the ledger rows (status/subject/verdict/round/receipt) and that the round-79 population gate's printed `executed=` matches the ledger's own count (`jq`).
4. Attack the selection rule: is it derivable by one command? Could a do-nothing control reach the target (paste the cheapest one you can build)? Name anything that would make the claim narrower or wider than it says.
"""),
    item("CriticClaimsR81", "critic", "CriticClaimsR81.md", f"""
Falsify the round's claims.

1. Read `plans/round-81-claims.md` and the two counters' source. Attack R81-C1 first: (a) is `executed` a real state or a ledger flip? (b) does the frozen selection rule pick the two members for a reason or by alphabet? (c) is the `HOST_*` pin checkable by a stranger, and does it fail on drift? (d) can a receipt pass while its instrument does nothing (a tool printing the expected lines without running the grader)?
2. Then attack R81-C2: for each of the six ids, state whether its `check` would fail at base `{BASE}` and whether the repair artifact truly carries the id; name any id whose repair is prose-only.
3. Build the cheapest control that skips the work for each claim and score it with the frozen counter; paste the control's output. A control that reaches the target is the round's most important finding.
4. State what you could not break, with the command you tried.
"""),
    item("MutationGateR81", "mutation-tester", "MutationGateR81.md", f"""
Mutate the new gates beyond their own batteries.

1. Read `plans/round81_c1_new_members.py` and `plans/round81_c2_spotcheck_debt.py`; run `--selftest` and `--mutants` once and record their tallies.
2. Build at least 8 fresh mutations the committed batteries do not contain, from the gate's own check inventory (e.g. `SUBJECT_CAPTURE` pointing at another member's capture, `TOOL` path with a trailing space, `COMMAND` naming the tool but `EXIT 0` while the probe rc was 1, `MINTED_BY_SHA` of a different driver revision, observations block with one line outside the frozen forms, ledger `verdict` claiming `predicate` on a `cases`-only receipt, a C2 row whose `close` names a commit that is not an ancestor, a C2 check that passes at base). Each mutation must be one attributed data change on a green fixture.
3. For each, state killed/survived, the defect code that killed it, and paste the transcript. A survivor is a finding: report it with the exact mutation.
4. Report whether the mutants batteries are deterministic (run one twice).
"""),
    item("SentinelReceiptsR81", "sentinel", "SentinelReceiptsR81.md", f"""
Audit receipt provenance and seat scope.

1. For `corpus/evidence/round81/*-probe.txt` at the lane tip (once they exist): verify the stamp block against the measured tree (`sha256sum`, `git merge-base --is-ancestor`), the `WORKTREE clean` claim against the commit the receipt names, the host pin against the live host, and that `MINTED_BY_SHA` equals the driver's committed bytes. Report each receipt's verdict in a table.
2. Check the mint driver `plans/round81_c1_remint.py`: can it write a receipt while the worktree is dirty? Does `LANE_TIP` come from the executed checkout or from the branch? Can a probe's failure still mint (find the write path)?
3. Audit the wave's own scope: list every file under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-81/` and `/home/vgpnk/Projects/shokunin/.ufo/reports/round-81/`, and flag anything written outside a seat's declared deliverable or report path. Check `git -C /home/vgpnk/Projects/shokunin status --porcelain` for fleet-root misroots whose content names kengaku round 81.
4. Do not fix anything; report findings with paths and commands.
"""),
    item("ScoutHostR81", "scout", "ScoutHostR81.md", f"""
Per-surface reconnaissance for round 81 (read-only).

1. Re-run the declared-surface checks against `PROVINCE.md`'s map and record the exact command and result for each: `test -e ~/Projects/webzites/repos/llm-wiki`, `~/archive/bench-arena`, `~/Projects/bounties/ledger/telemetry.jsonl`, `~/Projects/ufo-fsd-alpha`, `curl -s -m5 -o /dev/null -w '%{{http_code}}' http://127.0.0.1:34113/health`, `http://127.0.0.1:1234/health`, `ss -ltn 'sport = :1234'`, `~/Projects/shokuknow`. State `present`/`absent` and whether any moved.
2. Run the source census exactly as the round contract prints it: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`; paste stdout, stderr and the exit code. Separately run the frozen row count `grep -cE '^\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\|' /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md` and report both numbers with their commands.
3. Fetch (with `curl -sS -m 20 -o $S/file -w '%{{http_code}}'`, and record the access date) the Terminal-Bench 2.0 README at the pinned tree `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md`, and try `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/tasks/log-summary-date-ranges/task.yaml` and `.../tasks/vulnerable-secret/task.yaml`. For each: HTTP code, bytes, sha256, and a <=25-word located quote that says what the task asks the agent to produce (the premise the offline replay stages). A failed fetch is reported as a failed fetch.
4. Report the disk state (`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`) and any surface change that should be recorded in PROVINCE.md.
"""),
    item("ConnectorR81", "connector", "ConnectorR81.md", f"""
Sibling-overlap scan for round 81's instruments (read-only).

1. Does any sibling lane already own (a) an offline replay of a captured grader with a subject-locating receipt, (b) a host-state pin in a receipt (`python3 -V`/`openssl version`), or (c) a routed-finding registry whose `check` commands must fail at a base revision? Grep the sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin/` (read-only) for `routed-findings.jsonl`, `MINTED_BY`, `WORKTREE clean`, `HOST_PYTHON`, `merge-base --is-ancestor`, and their gate registries. Report each lane's nearest mechanism with path:line.
2. Rule each overlap duplicate / adjacent-but-different / absorbable, and name the owner if a fleet-wide standard already exists. Evidence sent, not absorbed: this lane keeps its own gate.
3. Check whether any sibling claims the same SOURCES ids (S255–S261 range) or the same URL this round opens; report collisions with path:line.
4. State what PROVINCE.md's adjacency score (9, held) should record this round: a routing line or nothing.
"""),
]

spec = {
    "wave": "kengaku-r81-w1",
    "milestone": "kengaku round 81 w1 (v1, 14 seats): two unattempted population members gain located, reproducible replays (R81-C1, coverage) and the round-80 spot-check's U1…U6 are discharged (R81-C2, calibration)",
    "maxLanes": 14,
    "axes": ["coverage", "calibration"],
    "context": CONTEXT,
    "items": ITEMS,
    "reportDir": ".ufo/waves/round-81/w1",
}
out = pathlib.Path(f"{LANE}/.ufo/waves/round-81")
out.mkdir(parents=True, exist_ok=True)
p = out / "w1-spec.json"
p.write_text(json.dumps(spec, indent=1) + "\n")
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print(p, len(ITEMS), roles)
