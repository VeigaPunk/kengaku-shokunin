#!/usr/bin/env python3
"""Build the kengaku round-52 wave-1 (build) swarm spec.

Run from the lane root; writes .ufo/waves/round-52/w1-spec.json.  The spec is validated by
scripts/ufo-swarm-wave.mjs under policy v1 (band 32-64) and dispatched by the orchestrator
through .ufo/waves/round-52/w1.ready.
"""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
WAVE_DIR = f"{LANE}/.ufo/waves/round-52/w1"
SCRATCH = "/fast/scratch/hyaku/kengaku-r52"
GODSPEED = (
    "/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim — let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in "
    "large batches. Do not serialize what can run in parallel. Do not output philosophical "
    "reasoning or verbose plans. Act directly via tool calls."
)

CONTEXT = f"""# Goal
kengaku round 52 (hyaku run 11), WAVE 1 of 2 (build), lane repo {LANE}.
The round's two frozen claims live at {LANE}/plans/round-52-claims.md — READ IT IN FULL FIRST;
it binds every seat, and its predicate, thresholds, populations, controls and kill rules are
frozen (a change after scoring is a new round, never a patch).

- **R52-C1 (novelty 8->9)** — a whole-benchmark grader-vacuity triage for Terminal-Bench 2.0:
  frozen population `plans/round52-tasks.json` (89 tasks, 184 grader files at pin
  2fd12b88aafdd04a52c298e3940bcb189f9766d6); frozen counter `plans/round52_c1_grader_audit.py`;
  frozen classification rules in the claims file, section C1.
- **R52-C2 (operability 8->9)** — every advertised verdict instrument gets a truthful row in
  SKILL.md's *## Gate/probe registry*; frozen counter `plans/round52_c2_registry.py`
  (MISSING 28, SELFTEST-UNBACKED 1 at the base tip).

Base tip 30801b479e3418c11089b8586178b6960216f364. Two waves: this is the build wave (32 seats);
wave 2 (32 falsify seats) is dispatched by the L1 after this wave returns.

# Write scope — every seat
Work ONLY inside your own scratch dir `{SCRATCH}/<your-seat-name>/` and your own wave report
file `{WAVE_DIR}/<your-seat-name>/report.md`. Put every artefact you produce under your scratch
dir; the L1 is the single integration owner and copies what it accepts into the lane tree.
NEVER edit the lane tree, the fleet repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`,
`templates/`, `scripts/`, `MANIFEST.json`, or `/home/vgpnk/Projects/shokunin/.scratch/`.
NEVER run `git commit`, `git add`, `git push`, `git stash`, `git checkout`, `git reset`,
`git pull`, or any mutating `jj` command anywhere — the L1 commits through the lane helper only.
NEVER run a campaign tool inside /home/vgpnk/Projects/shokuknow (read it only).
Never message agent://all; message only the seats you are told to address, by id.

# Scratch discipline (operator directive 2026-10-25)
Every clone, work tree, fixture and temp file of this seat lives under
`{SCRATCH}/<your-seat-name>/` (NVMe, ~536 GB free). Create it with `mkdir -p` and pass it
explicitly (`TMPDIR={SCRATCH}/<your-seat-name>/tmp`, `--work`); never rely on an inherited
TMPDIR and never write to /tmp except files under 50 MB. Remove your scratch dir before you
yield (`rm -rf -- {SCRATCH}/<your-seat-name>/`) after copying any receipt you want kept into
your wave report dir. A seat that ends with its tree still on disk reports that as its own
defect. If you see ENOSPC, report the free space you saw and stop; do not retry blindly.

# Tooling
You and every seat may install or upgrade tools that help the task — read
/home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record
tool/version/channel/reason in your report). **pacman guard (orchestrator ruling 2026-10-20):
all pacman transactions are PAUSED host-wide** — install via `uv tool` / `npx` / an official
binary in `~/.local/bin`, or file an L0 question. Never `pacman -Sy`, `-Syu`, `-U`, `-R`,
downgrade, or restart a host service.

# Report contract (every seat)
Write your report to `{WAVE_DIR}/<your-seat-name>/report.md` — that path is absolute; if a tool
renders a relative `Report:` trailer for you, it is relative to {LANE} — write it at
{LANE}/<that path>. Your report must carry: what you did, the exact commands you ran, the
measured numbers, the files you produced (absolute paths), and — for every attack seat — what
you attacked and the concrete evidence that your attack landed or failed to land. A seat that
finds nothing says what it searched and reports the negative; a seat that cannot finish says
what it could not do and why. Never fabricate a number, a quote or a URL.
"""


def item(name, role, axes, body):
    return {
        "name": name,
        "role": role,
        "axes": axes,
        "item": GODSPEED + f"\n\n# Target\nkengaku round 52 wave-1 seat {name} ({role}).\n# Item\n{body}",
    }


ITEMS = []

# ---------------------------------------------------------------- executors
ITEMS.append(item("C1ExecFetchGraders", "executor", ["novelty"], f"""Fetch every file of the FROZEN population in `{LANE}/plans/round52-tasks.json` (89 tasks, 184 files) from
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<path>`.
Write them byte-exact under `{SCRATCH}/C1ExecFetchGraders/graders/<path>` (keep the relative path),
and write `{SCRATCH}/C1ExecFetchGraders/SHA256SUMS` in `sha256sum` format (`<hex>  <path>`).
Verify: every expected path present, each digest matches, and the count of files equals
`capture_file_count` (184). Record every 404 or empty response verbatim. Do not modify the
capture bytes (no trailing-newline edits). Report: fetched count, mismatched count, missing
paths, total bytes, and the sha256 of your SHA256SUMS file."""))

ITEMS.append(item("C1ExecClassifier", "executor", ["novelty"], f"""Implement the FROZEN classifier of `{LANE}/plans/round-52-claims.md` §C1 as a standalone module in
`{SCRATCH}/C1ExecClassifier/classify.py` (read `{LANE}/plans/round52_c1_grader_audit.py` and mirror its
`classify()` exactly — presence/content/behaviour markers, `def test_` count, class order
V1,V2,V3,V4,V0 — do not change the rules). It must read the frozen population plus a captures dir
(argv `--captures DIR`) and emit one JSON record per task: task, grader path, sha256, bytes, the
four feature booleans/count, and the class. Then run it over the captures fetched by
`C1ExecFetchGraders` if that directory already exists (it may not yet — in that case run it over
whatever captures exist and say so). Report: the class histogram, the per-task records file path,
and any rule case you could not decide (state the class you assigned and why)."""))

ITEMS.append(item("C1ExecCounterRun", "executor", ["novelty"], f"""Run the FROZEN counter `{LANE}/plans/round52_c1_grader_audit.py --lane .` inside a scratch clone of the lane
(`git clone --shared -b master {LANE} {SCRATCH}/C1ExecCounterRun/lane`; verify
`git -C {SCRATCH}/C1ExecCounterRun/lane rev-parse --show-toplevel` equals that path before any git
command) with the captures of `C1ExecFetchGraders` copied to
`corpus/evidence/round52/graders/` inside the clone, and report its stdout and exit code
verbatim. Also run `--selftest` and report. Do NOT change the counter; if a leg fails, say which
leg and what evidence is missing. Report: the counter's full output, exit codes, and the list of
predicate legs that still fail."""))

ITEMS.append(item("C2ExecRowFacts", "executor", ["operability"], f"""For each of the 28 instruments the frozen counter reports as MISSING (run
`python3 {LANE}/plans/round52_c2_registry.py --lane .` and read its MISSING list), extract
MECHANICAL facts from the script bytes: argparse flags declared, exit codes it returns, whether
it declares a `--selftest` flag and what that selftest prints, every file path it writes, whether
it needs network, and the first line of its docstring. Write `{SCRATCH}/C2ExecRowFacts/facts.json`
as one object per instrument. Do not write registry prose — the scribes do that from your facts.
Report: the facts file path, the instruments whose facts you could not derive, and any script
whose exit-code behaviour contradicts its own docstring."""))

ITEMS.append(item("C2ExecRowRuns", "executor", ["operability"], f"""Measure, do not guess, how each of the 28 missing instruments behaves when a stranger runs it.
Clone the lane (`git clone --shared -b master {LANE} {SCRATCH}/C2ExecRowRuns/lane`), and in the clone
run each instrument with the command its own `--help`/docstring implies, with
`TMPDIR={SCRATCH}/C2ExecRowRuns/tmp` and a per-instrument `--work`/scratch dir. Record exit code,
wall time, the verdict line it prints, and whether it wrote anything into the clone.
Never run one instrument inside the real lane tree. Report: one table row per instrument
(name, command, exit code, verdict line, writes?) plus every instrument that crashed with a
traceback (paste the last 5 lines)."""))

ITEMS.append(item("C1ExecBlindLabels", "executor", ["novelty"], f"""Produce a BLIND label set for the frozen classifier: choose a deterministic sample of 24 tasks
from `plans/round52-tasks.json` (take every task whose index in sorted order is a multiple of 3,
and say exactly which), fetch each task's primary grader bytes, read them yourself and assign a
class label per the frozen rules in `plans/round-52-claims.md` §C1 (V1 presence-only, V2
behavioural, V3 content-check, V4 assertion-sparse, V0 other). Do NOT look at
`plans/round52_c1_grader_audit.py`'s output or at any other seat's labels. Write
`{SCRATCH}/C1ExecBlindLabels/labels.json` as `{{"labels": [{{"task": ..., "class": ..., "why": "<=20 words"}}]}}`.
Report: the sampled task ids, the label histogram, and every task whose class you found hard to
decide (with the reason)."""))

ITEMS.append(item("C1ExecReadFindings", "executor", ["novelty"], f"""Read the lane's 12 hand-read TB2 grader entries (`{LANE}/corpus/knowledge/tb2-*-grader.md`) and extract,
per task, the lane's own recorded finding in one line each: what the grader actually checks, the
vacuity or weakness class the lane found, and the exact file:line anchor it cites. Write
`{SCRATCH}/C1ExecReadFindings/read-findings.json` (task -> a dict with keys task, checks, weakness, anchor, source_entry).
Report: the 12 task ids with their recorded weakness class, and any entry whose weakness class
cannot be stated from the entry text."""))

ITEMS.append(item("C2ExecOrderCheckFact", "executor", ["operability"], f"""The frozen counter reports one registry row as SELFTEST-UNBACKED: `order-check`. Establish the
FACTS: does `{LANE}/plans/order_check.py` declare a `--selftest` flag? what flags does it declare?
what does its own registry row in `SKILL.md` claim? What is the truthful self-test cell text for
that row (options: name a flag the script really accepts, or state plainly that the instrument has
no self-test and why)? Evidence: quote the script's argparse block and the row's cells with
line numbers. Report: the facts, the exact truthful replacement cell text you recommend, and any
other row in the registry whose self-test claim you can already disprove from the script bytes."""))

ITEMS.append(item("C2ExecRegistryAudit", "executor", ["operability"], f"""Audit the 46 EXISTING registry rows in `SKILL.md`'s *## Gate/probe registry* for factual truth, not
completeness: does each row's entry script exist? does the verdict map match the exit codes the
script actually returns (read the `return`/`sys.exit` sites)? does the self-test cell name a flag
the script accepts? Report every row whose text is factually wrong, with the script evidence and
the corrected cell text. Write `{SCRATCH}/C2ExecRegistryAudit/audit.json`. Do not edit SKILL.md."""))

ITEMS.append(item("C1ExecPopulationCheck", "executor", ["novelty"], f"""Independently re-derive the frozen population: fetch
`https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1`
and recompute the task list and the grader-file list (files under `<task>/tests/` or
`<task>/environment/tests/` named test_outputs.py, test.sh or verify.sh). Compare with
`{LANE}/plans/round52-tasks.json` row by row. Report: the recomputed task count, the recomputed
capture-file count, every task or file in one and not the other, and whether the pin is still
reachable (HTTP status). If the remote tree has changed, say so and report the frozen file's
sha256 per entry — the frozen file does not change either way."""))

# ---------------------------------------------------------------- scribes
ROW_SETS = {
    "C2ScribeRowsA": ["plans/adoption_check.py", "plans/attrib_probe.py", "plans/catalog_probe.py", "plans/defect_ledger.py", "plans/gate_flip_check.py"],
    "C2ScribeRowsB": ["plans/parser_policy_compare.py", "plans/password_recovery_probe.py", "plans/polyglot_c_py_probe.py", "plans/round28_census.py", "plans/round30_defects.py"],
    "C2ScribeRowsC": ["plans/round31_c1_verify.py", "plans/round31_defects.py", "plans/round33_c1_verify.py", "plans/round33_defects.py", "plans/round35_c1_verify.py"],
    "C2ScribeRowsD": ["plans/round35_hardening.py", "plans/round36_c2_verify.py", "plans/round45_c1_verify.py", "plans/round45_c2_verify.py", "plans/round46_c1_verify.py"],
    "C2ScribeRowsE": ["plans/round46_c2_verify.py", "plans/round46_c3_verify.py", "plans/round50_c1_verify.py", "plans/round50_c2_audit.py", "plans/round51_routing.py"],
    "C2ScribeRowsF": ["plans/round51_surfaces.py", "plans/routed_open.py", "plans/tb2_grader_probe.py"],
}
for name, scripts in ROW_SETS.items():
    lst = ", ".join(f"`{s}`" for s in scripts)
    ITEMS.append(item(name, "scribe", ["operability"], f"""Draft the missing SKILL.md *## Gate/probe registry* rows for these {len(scripts)} instruments: {lst}.
Read each script yourself (docstring, argparse block, exit codes, what it writes) and, when
`C2ExecRowFacts`/`C2ExecRowRuns` scratch artefacts are present under
`{SCRATCH}/C2ExecRowFacts/facts.json` and `{SCRATCH}/C2ExecRowRuns/`, use their measurements —
if they are absent, derive the facts yourself and say so. Write your rows to
`{SCRATCH}/{name}/rows.md` as markdown table rows with EXACTLY the eight registry columns
(name | kind | entry | verdict map | self-test | pinned values | write scope | owner), one row per
instrument, each cell non-empty and each claim true of the script. Use `kind` = `gate` or `probe`;
the self-test cell must name a spelling the script really accepts, or state plainly that the
instrument has no self-test and why. Report: your rows file path, each row's kind, and any row
you could not fill truthfully (and what blocked it)."""))

ITEMS.append(item("C1ScribeSources", "scribe", ["novelty"], f"""Prepare the SOURCES-registry curation for this round. Read
`{LANE}/corpus/SOURCES.md` (contract v1: 13 columns; see `/home/vgpnk/Projects/shokunin/CORPUS.md`
section *SOURCES.md — where a shokunin learns*) and the census parser at
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. Draft, in
`{SCRATCH}/C1ScribeSources/sources-draft.md`, THREE candidate rows for sources this round will
open: (1) the Terminal-Bench 2.0 repository tree at pin
2fd12b88aafdd04a52c298e3940bcb189f9766d6 (tier A, kind `code`, status `mined`), (2) the raw
`build-pmars/tests/test_outputs.py` capture at that pin (tier A), (3) a placeholder row shape for
the prior-art primary the scout seat fetches (do NOT invent a URL — write the row shape with a
`__PRIOR_ART_ROW__` placeholder and say so). Every row must be 13 columns, carry the id the
registry will assign next, a valid ISO date in `recheck`, and a `used-by` naming exactly the
entry that cites it. Also draft the `## Gate` block skeleton for
`corpus/lessons/round-52.md` (candidates + verdict + reason/flip columns). Report: the draft
path, the exact id you propose for each row, and any census column rule you could not satisfy."""))

# ---------------------------------------------------------------- scouts
ITEMS.append(item("C1ScoutPriorArt", "scout", ["novelty"], f"""PRICE THE PRIOR ART of R52-C1 with fetched public primaries — this is the novelty claim's
evidence. Fetch (with `curl`/`web_search`; record HTTP status and the fetched URL) at least FIVE
public sources that bear on the claim: published audits of Terminal-Bench 2.0 task graders, tools
that statically audit benchmark graders/tests for vacuity or weak assertions, and benchmark
validity/audit literature. For each source give: URL, HTTP status, the ≤25-word located quote
(with the anchor or line), and what it says about (a) whole-benchmark grader triage and (b) the
two weakness classes the lane will look for. Write `{SCRATCH}/C1ScoutPriorArt/prior-art.md` with
the sources and a per-finding novelty verdict line of the form
`FINDING <task-id> verdict=phenomenon-new|phenomenon-known|unclear because <evidence>`.
Report: the draft path, the number of sources fetched with status 200, and your overall verdict
on whether a whole-benchmark grader-vacuity triage at instrument level is novel."""))

ITEMS.append(item("C1ScoutTaskShapes", "scout", ["novelty"], f"""Reconnaissance of the frozen population's shape (read-only; fetch into your scratch dir): for the
89 tasks in `{LANE}/plans/round52-tasks.json`, report how the score is actually decided —
pytest `tests/test_outputs.py`, a shell `tests/test.sh`/`verify.sh`, both, or neither — and how
many tasks have a `task.toml` and an `instruction.md` at the pin. Use the GitHub tree API and raw
fetches only; do not run any grader. Write `{SCRATCH}/C1ScoutTaskShapes/shapes.json`. Report: the
histogram of score-deciding mechanism, the count of tasks with a task.toml, and any task whose
shape the frozen classifier's rules cannot speak to (that is a finding — name it)."""))

ITEMS.append(item("C1ScoutLaneHistory", "scout", ["novelty"], f"""Reconnaissance of the lane's own history with this benchmark series (read-only): read
`{LANE}/corpus/knowledge/tb2-*-grader.md` (12 entries), `{LANE}/corpus/lessons/round-3*.md` and
`round-4*.md`, and the `## Frontier` section of `{LANE}/corpus/README.md`. Report what question
each of the 12 hand-read graders answered, which frontier clauses the series has discharged and
which are still open, and the exact wording of the still-open clauses a whole-benchmark triage
would close. Write `{SCRATCH}/C1ScoutLaneHistory/frontier-open.md`. Report: the open clauses
verbatim (with file:line) and the per-round question list."""))

# ---------------------------------------------------------------- connectors
ITEMS.append(item("C1ConnectSiblings", "connector", ["novelty"], f"""Sibling-overlap scan (read-only) for R52-C1: do any sibling lanes
(`/home/vgpnk/Projects/shokunin/*-shokunin`) already own benchmark-grader auditing, task-validity
audits, or a gate-registry standard? Read their PROVINCE.md, SCORECARD.md and
corpus/README.md (do not write to them). Report per sibling: what it owns, the exact file:line
of the claim, and whether the round-52 work is (a) inside this lane's province, (b) contested
(must be reported out, not absorbed), or (c) a duplicate of an existing sibling artifact. Name
the report-outs this lane should record in PROVINCE.md."""))

ITEMS.append(item("C2ConnectIndex", "connector", ["operability"], f"""Corpus-index reconnaissance for both claims (read-only): which rows of
`{LANE}/corpus/README.md` must change when the round lands (a new knowledge entry, a new
evidence dir `corpus/evidence/round52/`, a new lesson `corpus/lessons/round-52.md`, a new
instrument `plans/round52_c1_grader_audit.py` and `plans/round52_c2_registry.py`)? Check the index
in BOTH directions: every row points at a file that exists, every new file gets a row. Also
report whether any existing row conflicts with the round's new artefacts. Report: the exact rows
to add, the exact rows to touch, and any conflict."""))

# ---------------------------------------------------------------- reviewers
ITEMS.append(item("C1RevClaimsFreeze", "reviewer", ["novelty"], f"""Review the FROZEN claims file `{LANE}/plans/round-52-claims.md` against the round contract
(PROTOCOL §9 in `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md`): are the
two claims causally separable, is each after-state one concrete re-derivable value, is every
control able to fail, is the target one a do-nothing control cannot reach, and is any clause
universal ("all", "every", "complete") without a command that enumerates the set? Attack the
FREEZE: can the after-state be met without doing the claimed work (e.g. by writing a
confirmations.json by hand, or by writing 28 registry rows that say nothing true)? For each
attack, say whether the frozen predicate would catch it, and if not, name the smallest amendment
that would — but do NOT amend anything (the L1 decides). Report: a per-claim verdict
(sound | unsound + why) and the amendment list."""))

ITEMS.append(item("C1RevCounterRule", "reviewer", ["novelty"], f"""Attack the FROZEN counter `{LANE}/plans/round52_c1_grader_audit.py` for vacuous legs (this is the
instrument the novelty claim is measured with). For each leg (CAPTURES present/mismatched, TASKS
classified, CONFIRMED new, PRIOR-ART urls, LABELS agreement) ask: what input makes it pass
without the claimed work? Probe the `classify()` rules on hand-written byte fixtures in your
scratch dir: a file that exists-checks AND reads content; a file with 3 asserts and no markers; a
shell-only task; a grader whose only marker is the string `subprocess` inside a comment. Report:
per-leg verdict (vacuous | sound), the fixture you used, its expected and observed class, and any
leg whose predicate should have been tighter."""))

ITEMS.append(item("C2RevCounterRule", "reviewer", ["operability"], f"""Attack the FROZEN counter `{LANE}/plans/round52_c2_registry.py` for vacuous legs. Build fixture
lanes in your scratch dir: (a) a lane whose registry has 8-cell rows for every advertised script
but whose rows are all `x`; (b) a lane whose self-test cell names a script+flag that the script
does not accept, spelled so the counter's "exactly one script and one flag" test does not fire;
(c) a lane that advertises a script only in `LOG.md`; (d) a lane whose registry table is missing
the heading line. For each, report whether the counter's four legs would still pass. Report:
per-leg verdict (vacuous | sound) and the smallest tightening that closes each hole — do not
amend the counter yourself."""))

# ---------------------------------------------------------------- critics
ITEMS.append(item("C1CritTrustBoundary", "critic", ["novelty"], f"""Falsify R52-C1's CONFIRMED leg. It trusts `corpus/evidence/round52/confirmations.json`
(task, quote, reader, confirmed). Show, by construction in your scratch dir, at least TWO ways a
round could satisfy `CONFIRMED new >= 2` without a real second reader having confirmed a real
weakness (e.g. a self-written confirmation, a quote not present in the grader bytes, a reader id
that is the author). For each, state whether the frozen counter would accept it, and what the
smallest check is that would reject it. Report: your constructions, the counter's actual answer to
each (run it), and your recommended hardening — the L1 decides, do not change the counter."""))

ITEMS.append(item("C2CritPadding", "critic", ["operability"], f"""Falsify R52-C2: is the after-state reachable by padding? Build in your scratch dir a set of 28
registry rows that are syntactically complete (8 non-empty cells) but say nothing true (e.g. all
cells `x`), and show what the frozen counter reports for that lane. Then ask the harder question:
the counter cannot judge whether a row is TRUE — so what measurable evidence must accompany the
rows for the claim to be honest (a run receipt? a quote from the script? a digest?). Propose the
cheapest measurable evidence the L1 can demand per row, and name the rows for which you cannot
propose one. Report: the padding fixture's counter output, and your per-row evidence proposal."""))

ITEMS.append(item("C1CritRoundShape", "critic", ["novelty"], f"""Attack the ROUND, not the code. Check the round contract in
`/home/vgpnk/Projects/shokunin/.ufo/prompts/kengaku-round-52.md` §1-§5 against what this round
will land: (a) is the lowest-axis obligation met or properly waived (coverage 7 is capped by open
L0 questions — verify they are still open in `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`);
(b) does the frontier step (§2b) have a sourced claim and a mined mistake; (c) will the report
carry every required section; (d) is any claim actually a re-scoring of a rule the lane already
holds. Report: per-item verdict (conformant | defect + the exact defect), with file:line
evidence, and the missing items the L1 must still produce."""))

# ---------------------------------------------------------------- mutation-tester
ITEMS.append(item("C1MutCounters", "mutation-tester", ["operability"], f"""Mutation-test the two FROZEN counters `{LANE}/plans/round52_c1_grader_audit.py` and
`{LANE}/plans/round52_c2_registry.py` — WITHOUT editing the originals. Copy them into your scratch
dir and mutate the copies: for C1 flip one marker regex, change one class boundary, drop the
`mismatched` check, raise the CONFIRMED threshold to 0; for C2 drop one leg, widen the ADVERTISED
regex to match everything, make MISSING count only scripts under `plans/`. For each mutant say
which control in `{LANE}/plans/round-52-claims.md` should kill it, then RUN that control against
the mutant and report whether it was actually killed (a mutant that survives is a defect in the
frozen predicate — report it as such; do not fix the counter). Report: a mutant table (mutant,
expected killer control, killed yes/no, observed output)."""))

# ---------------------------------------------------------------- labrats
ITEMS.append(item("C1ScoutAgreement", "scout", ["novelty"], f"""EMPIRICAL PROBE (read-only): does the frozen classification scheme actually separate the graders
into distinguishable classes? Pick 15 tasks deterministically from `{LANE}/plans/round52-tasks.json`
(every task whose sorted index is a multiple of 5, say which ones), fetch their primary grader
bytes, read them, and assign a class per the frozen rules in the claims file §C1. Compare your
labels with the frozen counter's classes for those tasks (run the counter in a scratch clone with
the captures you fetched). Do NOT write any label file (you are read-only) — report the table:
task, your label, the counter's label, agree yes/no, and the byte evidence for every disagreement.
Report: agreement count out of 15 and every disagreement with its evidence."""))

ITEMS.append(item("C1ScoutVacuity", "scout", ["novelty"], f"""EMPIRICAL PROBE (read-only): how many of the 89 graders can be satisfied by the mere presence of
an artefact? Fetch every task's primary grader bytes into your scratch dir and count, per task,
the assert statements that reduce to existence checks (`exists(`, `is_file(`, `is_dir(`) and
whether the file contains ANY content read or behaviour marker. Report the distribution
(how many tasks have zero content/behaviour markers = the presence-only population), the largest
five by number of asserts, and three tasks that look presence-only to you with the located line
that makes you say so. This is a probe, not the claim: a number here is evidence for the wave-2
confirmation seats, and a negative result is a valid result."""))

# ---------------------------------------------------------------- revengers
ITEMS.append(item("C2RevRowIntent", "revenger", ["operability"], f"""Reverse-engineer the INTENT of the 28 unregistered instruments (read-only): for each, what did the
round that built it claim it did? Read its docstring, the SCORECARD.md/LOG.md paragraph that
names it, and its round's lesson under `{LANE}/corpus/lessons/`. Produce one line per instrument:
what it is FOR, whether it is still live or superseded by a later counter, and the truthful
`kind` (gate/probe) and owner for its registry row. Report the table and name every instrument
that looks superseded (a superseded instrument still needs a row saying so — the registry records
history, it does not prune it)."""))

ITEMS.append(item("C1RevSeriesIntent", "revenger", ["novelty"], f"""Reverse-engineer the intent of the lane's 12-round hand-reading series of TB2 graders (read-only):
rounds 35-46 each read one task grader. What was the series trying to establish, what did it
conclude, and what would a whole-benchmark triage have to preserve to keep that series's
conclusions true? Look at `{LANE}/corpus/knowledge/tb2-*-grader.md`, the lessons of those rounds,
and `{LANE}/corpus/README.md`'s `## Frontier`. Report: the series' question, its running
conclusion, the per-task weakness classes it found, and the specific property a triage must not
lose (name it)."""))


ITEMS.append(item("C1RevCaptureProvenance", "reviewer", ["novelty"], f"""Review the CAPTURE provenance (read-only): the round captures 184 grader files from a pinned
GitHub raw URL. Establish whether that procedure can yield wrong bytes, and what would detect it.
Re-fetch FIVE deterministically chosen paths from the frozen population (every 30th path in sorted
order) yourself into your scratch dir and compare their sha256 with what the frozen population's
digest pin says they should be (the pin is in the lane's own captures once they land; until then,
compare the two fetches byte-for-byte and report the pin the L1 must record). Check specifically
for: an HTML error page stored as a grader, an empty file, a redirect body, a rate-limit body, and
a path that exists at another pin but not this one. Report: the five paths with both digests, the
failure modes you could construct, and the minimal digest/format checks the L1 must add to the
capture manifest."""))

ITEMS.append(item("C1RevPriorArtProtocol", "reviewer", ["novelty"], f"""Review the PRIOR-ART protocol this round must follow (read-only): read
`{LANE}/corpus/knowledge/eval-prior-art-calibration.md` and `{LANE}/corpus/knowledge/attrib-prior-art-r21.md`
and say what a compliant prior-art file for R52-C1 must contain: how many fetched primaries, what
counts as a fetched URL, how a "phenomenon-new vs phenomenon-known" verdict must be justified, and
what a located quote is. Then apply that standard to the NOVELTY claim itself and state the
acceptance checklist the L1 will use when the scout's prior-art file arrives (and what would make
the verdict `unclear`, which does not move the score). Report the checklist and the standard's
source lines."""))

assert len(ITEMS) == 35, len(ITEMS)
spec = {
    "wave": "kengaku-r52-w1",
    "milestone": "kengaku round 52 wave 1 (build): fetch+classify the Terminal-Bench 2.0 grader population (R52-C1, novelty) and derive the 28 missing gate-registry rows (R52-C2, operability)",
    "reportDir": ".ufo/waves/round-52/w1",
    "maxLanes": 35,
    "axes": ["novelty", "operability"],
    "context": CONTEXT,
    "items": ITEMS,
}
out = Path(f"{LANE}/.ufo/waves/round-52/w1-spec.json")
out.write_text(json.dumps(spec, indent=1))
print(f"wrote {out} items={len(ITEMS)}")
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print(roles)
attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "labrat"))
print(f"attack seats={attack}/{len(ITEMS)} = {attack/len(ITEMS):.0%}")
