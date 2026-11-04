#!/usr/bin/env python3
"""Build the round-82 v1 wave spec (12 seats) and print the path."""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
SCRATCH = "/fast/scratch/hyaku/kengaku-r82"
BASE = "a3a03ac31451e58f1742b9bccb73b72c2d90a95c"
FREEZE = "12f1029a45cf0097a3afd030d757bf93b87f8018"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = f"""# Goal
Kengaku lane, round 82 — wave w1 (v1, 12 seats: build + attack). You are ONE seat of this wave.
The round's three claims are FROZEN at {LANE}/plans/round-82-claims.md (freeze commit `{FREEZE}`); read it in full before any command. Never re-open a frozen predicate, universe rule, control or kill rule.

R82-C1 (coverage, lowest non-retired axis, held at its L0 cap) = every `plans/**/*.py` that exists at `{BASE}` outside `plans/fixtures/` and is referenced as a literal path by SCORECARD.md, LOG.md or corpus/README.md at that revision either has a row in SKILL.md's `## Gate/probe registry` at the tip, or sits in the counter's frozen EXCLUSIONS table with reason class `support-module` whose bytes prove it (no argparse + no `__main__`); and every registry entry cell names a script that exists at `{BASE}`. Counter: `python3 plans/round82_c1_plans_registry.py --lane .` — at BASE it must print `MISSING 4` + `UNCLASSIFIED 2` and exit 1; the round's target is `missing=0 unclassified=0 excluded=2 entry_missing=0`, `PREDICATE R82-C1 pass`, exit 0.

R82-C2 (calibration, held at ceiling 10, exercised) = the round-81 verifier spot-check's `V1`…`V7` (`corpus/lessons/round-81-verifier-spotcheck.md` §5) are discharged as `corpus/routed-findings.jsonl` rows `R81-V1`…`R81-V7`: status closed, a `source` resolving to the line that carries the short id, a `close` naming a tracked repair artifact (not the spot-check) whose bytes carry the id and the row's `evidence_literal`, a `check` that exits 0 at the tip and fails when its repair is reverted to `{BASE}`, and `corpus/README.md` indexing the spot-check. Counter: `python3 plans/round82_c2_closure_debt.py --lane .` (at BASE: seven `DEBT-UNREGISTERED`, rc 1).

R82-C3 (capability acquisition, freshness instrument, no axis-score move) = `sweep-at-one-tip`: one gate that maps every `executed` member of `plans/grader-population-ledger.json` through the frozen `plans/round82-sweep-map.json` (26 members, instrument + argv + receipt), runs each instrument once at one tip under a timeout, classifies each member `reproduced` | `diverged:<n>` | `unrunnable:<code>` under the frozen projection, and prints a per-class histogram; the receipt `corpus/evidence/round82/sweep.txt` carries one `MEMBER` line per member; two runs at one tip agree on statuses and divergence counts; every receipt `COMMAND` equals the reconstructed argv (`COMMAND-MISMATCH`); writes are staged until every member has a status line; `--verify-at-tip` re-runs its own `--selftest` battery at the measured tree. Counter: `python3 plans/round82_c3_sweep.py --lane . --check` → `TARGET members=26 located=26 status_lines=26 histogram_total=26 mismatches=0`, `PREDICATE R82-C3 pass`, exit 0.

# Rules (binding on every seat)
- Write scope: your OWN scratch dir `$HYAKU_SCRATCH/kengaku-r82/<your-seat-name>/` with `HYAKU_SCRATCH` defaulting to `/fast/scratch/hyaku` (mkdir -p it; delete it before you yield — `trap 'rm -rf -- "$S"' EXIT`), the single report file named by your `Report:` trailer, and (only where your item names one) the named deliverable(s) under `{LANE}/.ufo/waves/round-82/w1/`. Everything else is READ-ONLY: never write, commit, push or run a mutating git/jj command in `{LANE}`, in the fleet repo, in a sibling lane, or in any domain source tree. Never edit `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/routed-findings.jsonl`, the ledger, `plans/round82-sweep-map.json` or any existing gate — the L1 integrates; you deliver bytes and findings.
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Report file names are given per item.
- Scratch: one `git clone --shared {LANE} $S/clone` per seat where a clone is needed (never a full clone, never a mirror of the lane); no `/tmp` path is citable evidence; nothing under `/tmp` survives.
- Fixture repos: `D=$(mktemp -d -p $HYAKU_SCRATCH/kengaku-r82/<seat>) && git -C "$D" init -q`; every later git/jj call names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit. Never run `git commit`/`jj` with a throwaway identity anywhere else.
- Measure at the current lane tip (`git -C {LANE} rev-parse master`); the freeze commit is `{FREEZE}`, the base revision every "before" state names is `{BASE}`.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate, record tool/version/channel/reason in your report). **pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide**; install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or file an L0 question. Never `pacman -Sy/-Syu/-U/-R`.
- Never call the `ask` tool: the round is unattended. Leaf member: no subagent dispatch (executors may spawn one read-only labrat probe; every other role stays a leaf; no seat runs its own swarm).
- Do not trust the counters: read bytes yourself. An unrun check has not passed; never invent a number. Report every failure with its exact command and output.

# Judging
Every claim, number and gate in this lane is judged on committed bytes; a report line without a command and its output is not evidence. Attack seats: state what you attacked and what you could not break."""


def item(name, role, report, body, deliverables=None):
    trailer = f"\n\nReport: .ufo/waves/round-82/w1/{report}\n"
    if deliverables:
        trailer += "\nDeliverable path(s) you may write outside scratch:\n" + "\n".join(
            f"- {LANE}/.ufo/waves/round-82/w1/{d}" for d in deliverables) + "\n"
    return {"name": name, "role": role,
            "prompt": GODSPEED + f"\n\n# Item {name} — role {role}\n\n" + body.strip() + trailer}


ITEMS = [
    item("SweepGateR82", "executor", "SweepGateR82.md", f"""
Build the R82-C3 sweep gate: `plans/round82_c3_sweep.py`, delivered byte-final as
`.ufo/waves/round-82/w1/SweepGateR82.py` (the L1 installs it at `plans/`).

Read `{LANE}/plans/round-82-claims.md` §R82-C3 for the frozen predicate, the frozen projection and the
seven printed-line families, and `{LANE}/plans/round82-sweep-map.json` for the 26 members, argv and receipts.

Modes (all required; argparse, exit 0 pass / 1 fail / 2 setup):
- `--lane DIR --check` — over committed bytes only: read the map, the ledger and `corpus/evidence/round82/sweep.txt`; require one `MEMBER` line per ledger `executed` member, no extras, each line carrying `status=`, `exit=`, `secs=`, `argv=`; require the histogram lines to sum to 26; require each member's `argv=` to equal the map-derived argv with `<WORK>` substituted (`COMMAND-MISMATCH` otherwise). Print `MEMBERS total=26 status_lines=<n>`, `HISTOGRAM …`, `TARGET members=26 located=26 status_lines=26 histogram_total=26 mismatches=<n>`, `PREDICATE R82-C3 pass|fail`. Never re-runs an instrument.
- `--lane DIR --run --work DIR` — the sweep: for each member sequentially (port 8080/8081 are shared, so never in parallel), create `DIR/<member>/`, expand the map argv, run it with `subprocess.run(..., timeout=<map or 300>)` capturing stdout/stderr, then classify under the frozen projection against the member's committed receipt. Write the receipt only after every member has a status line (staging: collect all lines, then one write). `--receipt PATH` overrides the receipt path. Print the same `MEMBER`/`HISTOGRAM`/`TARGET` families plus `HISTOGRAM-CLASS <class>=<n>` (multi-label, with `sum=<m>` declared).
- `--lane DIR --verify-at-tip --work DIR` — make a clean `git clone --shared` of the lane at the measured tip, run this gate's own `--selftest` there and require `failures=0` (the round-80 plan item 4), then re-run `--check` over the tip's committed receipt and require the classification to match `DETERMINISM statuses_identical=yes divergence_counts_identical=yes`.
- `--selftest --work DIR` — >=10 cases over fixture trees: green fixture plus one red per defect family (missing status line, extra member, bad histogram sum, missing `argv=`, `COMMAND-MISMATCH`, `RECEIPT-MISSING`, `LOCATOR-MISS`, `PROJECTION-UNCHECKED`).
- `--mutants --work DIR` — >=8 attributed data mutations of the receipt/map; print `MUTANTS real=<n> killed=<n> survived=<n>`.
- `--control-ledger-copy --work DIR` (statuses copied from the ledger, nothing run -> `NO-RUN`), `--control-exit-only --work DIR` (exit codes only -> `PROJECTION-UNCHECKED`), `--control-fabricated-line --work DIR` (a `MEMBER` line whose observation the current instrument does not emit -> `VERIFY-MISMATCH`); each prints `target_reached=False`.

Constraints: stdlib only; honour `--work` (never a hardcoded `/tmp`); never write inside the lane except the receipt path you are given; strip no line silently — every unclassifiable line is a `DEFECT`.
Self-check: run `--selftest` and `--mutants` in your scratch and paste both tallies; do NOT run `--run` (the harvest seat measures the population; the L1 runs the sweep at close).
State the file's sha256 and line count in your report.
""", ["SweepGateR82.py"]),

    item("SweepHarvestR82", "executor", "SweepHarvestR82.md", f"""
Empirical harvest for R82-C3: run every one of the 26 members' frozen argv at the current lane tip.

Read `{LANE}/plans/round82-sweep-map.json` (26 members: instrument, argv with `<WORK>`/`<MEMBER>`
placeholders, receipt) and §R82-C3 of `plans/round-82-claims.md` (frozen projection).
In your own scratch: for each member, build `$S/work/<member>/`, substitute the placeholders, run the
argv sequentially (never in parallel — pypi and nginx both want port 8080) with a 300 s timeout, and
record: exit code, wall seconds, stdout sha256, the number of observation lines, whether the receipt
exists, and the projection comparison against the committed receipt (differing-line count and the
first three differing lines verbatim).
Deliver `.ufo/waves/round-82/w1/sweep-harvest.json` (machine-readable: member -> exit, secs, sha256,
status draft, diff_calls, first diffs) and the markdown report with a per-member table, the status
histogram (reproduced / diverged / unrunnable with codes), the per-class histogram over the ledger
classes, and every member that could not run with its exact error line.
Also: run the whole sweep twice for the members that ran and report whether statuses and divergence
counts agree (`DETERMINISM`), and measure `python3 -V`, `openssl version`, `bwrap --version` as the
environment pin. A member that hangs is a finding, not a failure of the harness — record `timeout`.
Do not write anywhere under `corpus/`; every `--receipt` goes into your scratch.
""", ["sweep-harvest.json"]),

    item("RegistryCounterR82", "executor", "RegistryCounterR82.md", f"""
Build the R82-C1 counter: `plans/round82_c1_plans_registry.py`, delivered byte-final as
`.ufo/waves/round-82/w1/RegistryCounterR82.py`.

Read `{LANE}/plans/round-82-claims.md` §R82-C1 in full (universe rule, row-quality rule, controls,
batteries, target lines). Model the code on `plans/round81_c2_spotcheck_debt.py` (Tree abstraction over
`git show`/worktree, `--rev`, selftest/mutants/controls) and `plans/round73_c2_registry_audit.py`
(eight-cell row parse, entry-cell script resolution, `ast.parse`).

Modes: `--lane DIR` (universe at `BASE_REV={BASE}`, rows at the tip), `--tip REV` (rows at another
revision), `--selftest --work DIR` (>=8 cases), `--mutants --work DIR` (>=6 attributed mutations, all
killed), and the three controls of §R82-C1 (`--control-empty-rows`, `--control-exclude-cli`,
`--control-name-only`), each printing `target_reached=False`.
Required printed lines: `UNIVERSE documents=3 instruments=<n> referenced=<n> registered=<n>`,
`MISSING <path>` per unregistered CLI instrument, `UNCLASSIFIED <path>` per unplaced support module,
`ROW <name> kind=<k> entry=<path> selftest=<ok|unbacked>` for each row added this round,
`EXCLUSION <path> class=support-module cli=no`, `ENTRY-MISSING <name> <path>`,
`ROWS registry=<n>`, `DEFECT <CODE> <detail>`, `DEFECTS n=<n>`, `TARGET missing=… unclassified=…
excluded=… rows=… entry_missing=…`, `PREDICATE R82-C1 pass|fail`.
At BASE the counter MUST print `MISSING 4`, `UNCLASSIFIED 2`, `DEFECTS n=6`, exit 1; after the round's
rows land it MUST print `missing=0 unclassified=0 excluded=2 entry_missing=0`, exit 0. Verify both:
run it against `--lane .` (tip) and against a scratch tree materialised from `{BASE}` (or your `--tip`
mode) and paste both outputs.
Constraints: stdlib only; honour `--work`; read-only over the lane; no hardcoded `/tmp`.
State the file's sha256 and line count in your report.
""", ["RegistryCounterR82.py"]),

    item("C2CounterR82", "executor", "C2CounterR82.md", f"""
Build R82-C2's counters: `plans/round82_c2_closure_debt.py` and `plans/round82_c2_checks.py`,
delivered byte-final as `.ufo/waves/round-82/w1/C2CounterR82.py` and
`.ufo/waves/round-82/w1/C2ChecksR82.py`.

Read `{LANE}/plans/round-82-claims.md` §R82-C2 and `plans/round81_c2_spotcheck_debt.py` +
`plans/round81_c2_checks.py` (the round-81 pair you are generalising). Differences you must build:
(1) the universe is DERIVED from the newest `corpus/lessons/round-*-verifier-spotcheck.md` by round
number and its `- **V<n> · ` lines — never hardcode round 81 or the id list; the id prefix is
`R<round>-V<n>`, derived from that file's name; (2) the sensitivity leg reverts each repair artifact to
`{BASE}` and requires the check to FAIL there; (3) the counter prints
`UNIVERSE spotcheck=<path> ids=7 <csv>`.

Checks (`plans/round82_c2_checks.py u1`…`u7`, one per id, each a shell-runnable subcommand that exits
0 at the tip and non-zero at `{BASE}`): u1 clean-tree `c2-after.txt` (`grep -q '^WORKTREE clean'
corpus/evidence/round81/c2-after.txt` plus a reachable `LANE_TIP`); u2 recomputed quote word-counts and
anchor ranges for the round-81 lesson and SOURCES S260/S261; u3 the knowledge entry's provenance trio;
u4 the r81 mutant-docstring count equal to the `real=` its own `--mutants` prints; u5 `test ! -e ./--lane`;
u6 the wave tally in `.ufo/waves/round-82/w1-results.json` (attack share >=25 % over
reviewer/critic/mutation-tester/labrat and a `mutation-tester` seat that is not dead); u7
`corpus/evidence/round81/determinism.txt` carrying `COMMAND` and `REV`.
Counter modes: `--lane DIR`, `--rev REV`, `--selftest --work DIR`, `--mutants --work DIR`,
`--control-presence --work DIR`; printed families `UNIVERSE`, `DEBT <id> …`, `DEBT-TOTAL`,
`INDEX <path> indexed=<yes|no>`, `DEFECT <CODE> <detail>`, `DEFECTS n=<n>`, `TARGET ids=7 closed=7
checks_passed=7 indexed=<yes|no>`, `PREDICATE R82-C2 pass|fail`.
Build the checks against the repairs the C2RepairR82/C2ProseR82 seats produce (their report names the
exact repaired bytes); where a repair is not yet on disk when you measure, say so and show the red.
Constraints: stdlib only; honour `--work`; never write into the lane.
State both files' sha256 and line counts in your report, with `--selftest`/`--mutants`/`--control-presence` tallies.
""", ["C2CounterR82.py", "C2ChecksR82.py"]),

    item("C2RepairR82", "executor", "C2RepairR82.md", f"""
Produce the repaired bytes for R82-C2's V1, V4, V5 and V7 (the prose repairs V2/V3/V6 belong to another seat).

Read `{LANE}/corpus/lessons/round-81-verifier-spotcheck.md` §5 (V1…V7) and §R82-C2 of
`plans/round-82-claims.md` first. Work in your own scratch; deliver each repaired file byte-exact under
`.ufo/waves/round-82/w1/repaired/` with the SAME relative path, plus a `MANIFEST` line per file
(`<sha256>  <path>`):

1. **V1** — `corpus/evidence/round81/c2-after.txt`: re-mint it by running
   `python3 plans/round81_c2_spotcheck_debt.py --lane .` from a CLEAN `git clone --shared` of the lane
   tip, so the receipt's stamp line reads `WORKTREE clean`; capture the counter's stdout verbatim as the
   receipt body, keeping the round-81 receipt's line order (stamp block first, then the counter output).
   Prove it: `grep -c '^WORKTREE clean'` = 1 and `grep -c '^WORKTREE dirty'` = 0 in the delivered file.
2. **V4** — `plans/round81_c2_spotcheck_debt.py`: its docstring/`MUTANTS` paragraph says six mutations
   while the battery prints `real=4`. Either add the two missing attributed mutants (preferred — show
   the new `real=6` from a real `--mutants` run in your scratch) or correct the docstring; the delivered
   file must make the stated number equal the printed number. Do NOT change any predicate or check.
3. **V5** — the stray `--lane/` directory in the lane root: confirm it exists (`ls -ld -- --lane`), that
   it is empty and untracked, and report it; deliver a `repaired/rmdir-command.txt` with the exact
   command the L1 runs (`rmdir -- '{LANE}/--lane'`) plus the before/after listing.
4. **V7** — `corpus/evidence/round81/determinism.txt`: append (never rewrite existing lines) the
   producing `COMMAND` line and the `REV` it was measured at, then re-run both instruments at the tip and
   record their stdout sha256 so the file's two-hash claim is re-derivable from a stated command.
Also confirm V5's `--lane` is truly empty — if it holds bytes, stop and report instead of deleting.
`MANIFEST` and every delivered file are your only lane writes.
""", ["repaired/MANIFEST", "repaired/corpus/evidence/round81/c2-after.txt",
      "repaired/plans/round81_c2_spotcheck_debt.py", "repaired/corpus/evidence/round81/determinism.txt",
      "repaired/rmdir-command.txt"]),

    item("PlansReconR82", "scout", "PlansReconR82.md", f"""
Read-only reconnaissance for R82-C1 (registry rows) and R82-C3 (sweep runnability).

1. For each of `plans/log_appendonly.py`, `plans/round37_c1_attribution.py`,
   `plans/round66_registry_check.py`, `plans/round80_c1_remint.py` measure, with the exact command and
   output: `--help` usage; the accepted flags; what the script writes to disk (grep its `Path(...)
   .write_text`/`open(...,'w')` calls and name the paths); its verdict map (which exit codes it can
   print and what each means — read the `sys.exit`/`return` sites, do not guess); whether it has a
   self-test flag and what that flag prints; whether it needs a clean tree or the live registry. Keep
   `round80_c1_remint.py` READ-ONLY: never run it against the lane (it writes receipts) — use `--help`
   and its source only, and say so.
2. For `plans/fixture_fence.py` and `plans/policy_cases.py` confirm the support-module class from
   bytes: no `argparse`, no `if __name__ == "__main__"`, and name what imports them (grep the lane) so
   the exclusion is not an opinion.
3. For the 26 members of `plans/round82-sweep-map.json`, report per member: does the instrument exist,
   is it stdlib-only by AST, and which external binary or service does it need (grep for `subprocess`,
   `shutil.which`, port numbers, `docker`, `nginx`, `grpc`, `torch`, `Bio`)? Rank the members most
   likely to land `unrunnable` and why. Do not run the sweep.
4. Report the current lane tip, the census (`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
   validate --root /home/vgpnk/Projects/shokunin kengaku`; paste stdout and exit code) and
   `disk-guard.sh status`.
Every claim carries its command; a guess is labelled a guess.
"""),

    item("RegistryRowsR82", "scribe", "RegistryRowsR82.md", f"""
Draft the R82-C1 registry rows, ready for the L1 to paste into `SKILL.md`'s `## Gate/probe registry`.

Read `{LANE}/plans/round-82-claims.md` §R82-C1 (row-quality rule: eight non-empty cells, `kind` in
`gate`/`probe`, entry cell naming an existing script, self-test cell naming a script + a flag that
really occurs in it or `none declared`, non-empty pinned-values and write-scope) and the registry table's
existing rows (`SKILL.md` §Gate/probe registry) for the house style.

Deliver, in your report:
1. Four complete markdown table rows, one per instrument — `plans/log_appendonly.py`,
   `plans/round37_c1_attribution.py`, `plans/round66_registry_check.py`, `plans/round80_c1_remint.py` —
   with names in the existing hyphenated style (`log-appendonly`, `round37-c1-attribution`,
   `round66-registry-check`, `round80-c1-remint`). Every cell must be TRUE: run each script's `--help`
   and, where a read-only run is possible, the run itself at the lane tip in your scratch; never run
   `round80_c1_remint.py` against the lane (it writes receipts). For `round80-c1-remint` declare the
   write scope explicitly (`corpus/evidence/round80/`, receipts only, clean tree required).
2. Two `EXCLUSIONS` table entries (`plans/fixture_fence.py`, `plans/policy_cases.py`) with
   `class=support-module`, the byte evidence that they carry no CLI (no `argparse`, no `__main__`) and
   who imports them.
3. A one-paragraph note stating, per row, which claim/round first referenced the instrument (path:line
   in SCORECARD.md/LOG.md/corpus/README.md) — the audit's forward direction.
Report the exact commands you ran to make each cell true; a cell you could not verify is marked
`UNVERIFIED` and named, never invented.
"""),

    item("C2ProseR82", "scribe", "C2ProseR82.md", f"""
Draft R82-C2's prose repairs (V2, V3, V6) as paste-ready text.

Read `{LANE}/corpus/lessons/round-81-verifier-spotcheck.md` §5 V2/V3/V6 first, and
`plans/round-82-claims.md` §R82-C2 for what each check will recompute.

1. **V2 — the miscounts.** In `corpus/lessons/round-81.md` §Gate the quotes are recorded as "14 words",
   "17 words", "9 words"; in `corpus/SOURCES.md` S260 the cell says "9 words" and "stamp 2-16,
   observations from 17", and S261 repeats 14/17. Recompute each count mechanically (whitespace-split
   words of the quoted text) and the actual line numbers in the named receipts, then deliver the exact
   corrected strings (old -> new, one line each) for: the lesson's Gate block, S260's cell, S261's cell.
   State the counting rule you used in one sentence so a reader can re-derive every number. Check every
   other quote count in both files the same way and report any further mismatch (do not fix by guess).
2. **V3 — the provenance trio.** `corpus/knowledge/tb2-file-artifact-replay-classes.md` lacks
   `source:`/`verified-at:`/`recheck:`. Deliver the three lines to prepend, with `source:` naming the
   SOURCES ids the entry rests on, `verified-at:` the round-82 tip, and `recheck:` a command that
   re-derives the entry's central claim (read the entry first; name the real counter, not a placeholder).
3. **V6 — the wave record.** Draft the paragraph (for `corpus/lessons/round-82.md`) that records this
   round's attack share: it must quote the role tally from `.ufo/waves/round-82/w1-results.json`
   (roles, attack seats over the campaign list reviewer/critic/mutation-tester/labrat, the live
   mutation-tester seat) and state the L1-holds-the-planner-seat mapping
   (orchestrator ruling 2026-10-19, the validator rejects `planner`). If the results file does not
   exist yet when you write, deliver the paragraph with the literal `TALLY_PENDING` in place of numbers
   and say so — never invent a tally.
Deliver plain text blocks in your report, each labelled by target file and insertion point.
"""),

    item("ConnectorR82", "connector", "ConnectorR82.md", f"""
Sibling-overlap scan for round 82's three instruments (read-only).

1. Does any sibling lane already own (a) a registry-completeness gate that audits a skill's gate table
   against the scripts a lane references, (b) a closure-debt discharge counter derived from the newest
   spot-check, or (c) a population sweep that re-runs a lane's own instruments at one tip and classifies
   the result? Grep the sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin/` (read-only)
   for `Gate/probe registry`, `routed-findings.jsonl`, `spotcheck`, `sweep`, `HISTOGRAM`, `UNIVERSE spotcheck`,
   plus their `SKILL.md` registries. Report each lane's nearest mechanism with path:line.
2. Rule each overlap duplicate / adjacent-but-different / absorbable, and name the owner where a
   fleet-wide standard already exists. Evidence sent, not absorbed: this lane keeps its own gates.
3. Check whether any sibling claims the same SOURCES ids (S262+ range) or the same URL this round opens;
   report collisions with path:line.
4. State what `PROVINCE.md`'s adjacency score (9, held) should record this round: a routing line or nothing.
"""),

    item("ReviewerR82", "reviewer", "ReviewerR82.md", f"""
Adversarial review of R82-C1 (coverage) — falsify the counter and the rows, not the prose.

Read `{LANE}/plans/round-82-claims.md` §R82-C1 and then, as they land, the counter
`plans/round82_c1_plans_registry.py` and the four draft rows in
`.ufo/waves/round-82/w1/RegistryRowsR82.md` and their installed form in `SKILL.md`.

Attack list (each with a command and its output):
1. Does the universe derivation really read `{BASE}` bytes, or does it silently read the worktree? Build a
   scratch tree where SCORECARD.md references a script that does not exist and check the counter's
   verdict (it must not change the denominator; a never-landed reference is not an instrument).
2. Can a stub row pass? Write a row whose cells are non-empty but false (a `gate` with no `1`/failed
   class; a self-test naming a flag the script does not contain; pins `n/a`) and show the counter red.
3. Can the exclusion table launder a CLI script? Put `plans/log_appendonly.py` in EXCLUSIONS and show
   `EXCLUSION-CLI`.
4. Is the reverse direction real? Delete a row's entry script (in scratch) and show `ENTRY-MISSING`.
5. Are the four installed rows TRUE? Independently run each one's declared entry argv (never
   `round80_c1_remint.py` against the lane — reason it out from source) and report every cell that
   misstates what the script does.
Report each attack as `HELD` / `BROKE` with the exact command and output; a claim you could not attack
is named as unattacked, never implied.
"""),

    item("CriticR82", "critic", "CriticR82.md", f"""
Falsify the round's three claims against their frozen text (adversarial, read-only over the lane).

Read `{LANE}/plans/round-82-claims.md` in full. For each claim, answer with commands:
1. **Causal separability.** Would C1's counter pass with C2 and C3 unlanded, and C2's with C1 and C3
   unlanded? Name any file one claim's universe reads that another claim writes.
2. **Do-nothing control.** Take `corpus/evidence/round82/freeze-controls.txt` and re-derive its four
   `MISSING`, two `UNCLASSIFIED`, seven `DEBT-UNREGISTERED` and three absences yourself; report any
   number the freeze receipt overstates.
3. **Target reachability.** Is `TARGET members=26 …` in C3 satisfiable without the sweep running (e.g.
   by writing the receipt by hand)? Is `histogram_total=26` the same sentence in the predicate, the
   counter and the receipt? Quote the three places.
4. **Projection laundering.** The C3 projection drops `cases=`, `OBSERVED-U` and `predicted=U` lines.
   Show one member whose divergence those drops would hide, if any, and say which; if none, say so with
   the count of dropped lines per member you can derive from committed receipts.
5. **C2 discharge quality.** For each of V1…V7 say what would make the repair a restatement rather than
   a repair, and whether the planned artifact clears it.
Report `CONFIRM`/`CONTEST` per item with the command and output; name what you could not break.
"""),

    item("MutationR82", "mutation-tester", "MutationR82.md", f"""
Mutation-test the round's gates: do the three counters kill real corruptions?

Inputs: `plans/round82_c1_plans_registry.py`, `plans/round82_c2_closure_debt.py` +
`plans/round82_c2_checks.py`, `plans/round82_c3_sweep.py` (delivered under
`.ufo/waves/round-82/w1/` and installed by the L1 into `plans/`), and each counter's own
`--selftest`/`--mutants` mode.

1. Copy each counter into your scratch, run its `--selftest --work` and `--mutants --work`, paste both
   tallies, and report every mutation that SURVIVES.
2. Write at least three NEW mutants per counter that its own battery does not contain — for C1: a row
   whose name duplicates an existing one, a row whose entry names a `.py` that parses but is not the
   claimed filename, an EXCLUSIONS entry whose reason contradicts its bytes; for C2: a `check` that
   returns 0 on an empty tree, a `close` pointing at the spot-check, an `evidence_literal` absent from
   the close artifact; for C3: a `MEMBER` line with a duplicated name, a histogram whose class counts
   sum to 25, a projection comparison that compares nothing — and report killed/survived per mutant.
3. For every survivor: name the code path that lets it through and the one-line fix.
Report commands and outputs; a mutant you could not kill is a finding, not a failure.
"""),
]

spec = {
    "wave": "kengaku-r82-w1",
    "milestone": "kengaku round 82 w1 (v1, 12 seats): registry completeness for claim-referenced instruments (R82-C1, coverage), the round-81 spot-check's V1…V7 discharged (R82-C2, calibration), and the sweep-at-one-tip capability (R82-C3, freshness instrument)",
    "maxLanes": 12,
    "axes": ["coverage", "calibration", "freshness"],
    "context": CONTEXT,
    "items": ITEMS,
    "reportDir": ".ufo/waves/round-82/w1",
}
out = pathlib.Path(f"{LANE}/.ufo/waves/round-82")
out.mkdir(parents=True, exist_ok=True)
p = out / "w1-spec.json"
p.write_text(json.dumps(spec, indent=1) + "\n")
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print(p, len(ITEMS), roles)
