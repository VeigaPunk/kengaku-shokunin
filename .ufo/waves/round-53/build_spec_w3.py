#!/usr/bin/env python3
"""Build the kengaku round-53 wave-3 (completion: price/confirm-attack/touch/relabel/measure/draft) swarm spec -> w3-spec.json (policy v1)."""
import json
import sys
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
W = f"{LANE}/.ufo/waves/round-53"
WAVE_DIR = f"{W}/w3"
SCRATCH = "/fast/scratch/hyaku/kengaku-r53"
INT = sys.argv[1] if len(sys.argv) > 1 else "UNSET"          # integration tip wave 3 starts from (full hash)
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
kengaku round 53 (hyaku run 11 re-dispatch), WAVE 3 of 3 (completion: this round already ran wave 1 build (35 seats) and wave 2
falsify/confirm (42 dispatched, stopped by the 2026-10-28 operator wrap-up with 5 readers done)). Lane repo {LANE}. L1 = KengakuR53.
Frozen claims: {LANE}/plans/round-53-claims.md (read it in full, amendments A1-A3 included). Facts with exact numbers and pointers:
{W}/facts.md — READ IT FIRST. State at build time: tip `{INT}` (the lane advances while you work — clone fresh, record the hash you ran at,
and run at the lane's current HEAD; the L1 reconciles).

- **R53-C1 (novelty 8->9)**: counter `plans/round53_c1_triage.py`, classifier frozen (sha256 935db122…), oracle = eight blind label
  files (305/305, committed receipt `{W}/claims/c1-after-oracle.txt`), 28 never-read candidates (`{W}/claims/c1-candidates.txt`),
  confirmations LANDED in review (20 tasks confirmed by five wave-2 readers, `.ufo/waves/round-53/w2/C1ConfRead*/`); this wave prices
  prior art for the 20 confirmed tasks and mechanically touch-runs them.
- **R53-C2 (calibration 9->10)**: counter `plans/round53_c2_tipstate.py`, ledger `plans/round53-tipstate.json` (78 rows), re-executed
  in a clean clone; run 1 (committed `{W}/claims/c2-run1.txt`) had 18 mismatches; this wave re-measures independently so the L1 can
  re-declare truthfully.

# Write scope — every seat
Your deliverables go under your own directory `{WAVE_DIR}/<your-seat-name>/` (absolute path; create it) and your report at
`{WAVE_DIR}/<your-seat-name>.md`. Every file you want kept (<= 1 MiB each) goes there: scratch is deleted at exit. Temporary clones,
fixtures and temp files live only under `{SCRATCH}/<your-seat-name>/` (NVMe; pass `TMPDIR` explicitly and remove the dir before you
yield; check `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before a heavy pass). Clone the lane for any run:
`git clone -q --shared {LANE} {SCRATCH}/<seat>/lane && git -C {SCRATCH}/<seat>/lane rev-parse --show-toplevel` must print that path
before anything else. NEVER edit the lane tree outside your own seat directory, the fleet repo, a sibling lane, `.ufo/state/`,
`.ufo/watchdog.log`, `templates/`, `scripts/`, `MANIFEST.json` or `/home/vgpnk/Projects/shokunin/.scratch/`. NEVER run `git commit`,
`git add`, `git push`, `git stash`, `git checkout`, `git reset`, `git pull` or any mutating `jj` command in the lane or the fleet repo.
Fixture repositories only via `D=$(mktemp -d -p {SCRATCH}/<seat>) && git -C "$D" init -q` with every later git call naming `-C "$D"`
(a stray fixture commit once landed on the fleet repo and deleted 4,606 paths). NEVER run a campaign tool inside
/home/vgpnk/Projects/shokuknow. Never message agent://all; message only seat ids you are told to. Nothing you write may contain
credential-shaped strings (tokens, keys, `op://`); do not copy captured grader bytes wholesale into a report (quote <= 25 words).
If you use `gh api`, never print or store the token. The one exception to "your own directory": the touch-run and pricing seats write
ONLY inside their own seat dir too — the L1 integrates; you never write `corpus/evidence/round53/` yourself.

# Tooling
You and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels,
update-safety gate; record tool/version/channel/reason in your report). **pacman guard (orchestrator ruling 2026-10-20): all pacman
transactions are PAUSED host-wide** — install via `uv tool` / `npx` / an official binary in `~/.local/bin`, or file an L0 question.
Never `pacman -Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host service. If a tool output looks inconsistent with its described
behaviour, add one line `tool: <concise description>` to your report.

# Report contract (every seat)
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Your report carries: what you did, the exact
commands you ran, the measured numbers, the files you produced (absolute paths) and, for every attack seat, what you attacked and the
concrete evidence that the attack landed or failed to land. Never fabricate a number, a quote or a URL. A seat that finds nothing says
what it searched (command) and reports the negative. A seat that cannot finish says what it could not do and why. If you see ENOSPC,
report the free space you saw and stop.
"""


def item(name, role, axes, body):
    return {"name": name, "role": role, "axes": axes,
            "item": GODSPEED + f"\n\n# Target\nkengaku round 53 wave-3 seat {name} ({role}).\n# Item\n{body}"}


ITEMS = []

# ---- 1. prior-art pricing (5 scouts x 4 confirmed tasks) -------------------------------------------------------
GROUPS = {
    "A": [("cobol-modernization", "test_required_files_exist,test_data_files_exist"),
          ("log-summary-date-ranges", "test_summary_file_exists"),
          ("path-tracing-reverse", "test_image_c_exists"),
          ("sparql-university", "test_sparql_file_exists")],
    "B": [("extract-moves-from-video", "test_solution_file_exists"),
          ("merge-diff-arc-agi-task", "test_git_repo_init,test_algo_py_exists"),
          ("prove-plus-comm", "test_proof_file_exists,test_compiled_proof_exists"),
          ("torch-pipeline-parallelism", "test_pipeline_parallel_exists")],
    "C": [("fix-code-vulnerability", "test_report_file_exists_example"),
          ("modernize-scientific-stack", "test_dependency_file_exists"),
          ("pytorch-model-cli", "test_weights_file_exists,test_cli_tool_exists,test_prediction_file_exists"),
          ("torch-tensor-parallelism", "test_parallel_linear_exists")],
    "D": [("gcode-to-text", "test_hello_file_exists"),
          ("mteb-leaderboard", "test_result_exists"),
          ("pytorch-model-recovery", "test_model_file_exists"),
          ("tune-mjcf", "test_tuned_model_exists")],
    "E": [("llm-inference-batching-scheduler", "test_output_files_exist"),
          ("path-tracing", "test_image_c_exists"),
          ("sam-cell-seg", "test_python_file_exists,test_csv_output_exists"),
          ("winning-avg-corewars", "test_warrior_exists")],
}
PA_RULES = """Prior-art rules (counter `leg_prior_art` in /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round53_c1_triage.py — read it first; claims file Claim 1 leg 4 + A1 bullets):
(a) `phenomenon-known`: an archive that names the task id or one of that task's test names AND describes an existence-only /
let-anything-pass verifier for it; the 8-25-word verbatim `quote` must itself name the task id or a test name.
(b) `phenomenon-new`: no tracker/public item names that weakness for this task. Then the row's own archive is a general primary on
the phenomenon (benchmark graders that pass when an artefact merely exists; weak verifier checks; benchmark validity) that does NOT
name the task or ANY of its tests anywhere in the body — the counter greps the task id AND every test name of the task, and rejects
otherwise. Its first line must be `SOURCE-URL: <public url>` and the row's `url` must equal that header URL. The quote (8-25 words,
verbatim, whitespace-normalised) must appear in the archive and support the pricing. Every phenomenon-new row carries `sweep`: >= 2
DISTINCT archived fetches (different sha256, each with a `SOURCE-URL:` first line) whose bodies do NOT name the task or its tests —
e.g. `gh api 'search/issues?q=repo:laude-institute/terminal-bench-2+<task-id>'` and the same for other trackers/a code or title
search; if a search result body names the task, it is unusable as a sweep — pick a query that returns nothing and say so.
Search budget: the GitHub search API allows ~30 requests/min — space queries, batch tasks, and prefer the issue-trackers of
`laude-institute/terminal-bench-2` (and terminal-bench/terminal-bench for the 1.0 lineage) plus web/arXiv searches for general
primaries. Every archive file's FIRST line is `SOURCE-URL: <the public url you actually fetched>` followed by the fetched bytes
verbatim; save under `<your seat dir>/fetched/` with a `SHA256SUMS` file.
Deliver `<your seat dir>/prior-art-part.json`: a JSON list of rows
`{"task","verdict","url","fetched":"<archive path relative to the lane root>","fetched_sha256","quote","sweep":[{"file":"<path
relative to the lane root>","file_sha256"},…]}` (omit `sweep` for known rows). A task for which you cannot establish either verdict
gets `unclear` in your report and NO row (say what you searched). Also list every URL you opened and every rejected candidate with
the reason. Do not read the label files, the classifier output, or `.ufo/waves/round-53/w2/` reader parts."""
for g, tasks in GROUPS.items():
    tlist = "; ".join(f"`{t}` (test(s): {tests})" for t, tests in tasks)
    ITEMS.append(item(f"C1PriceScout{g}", "scout", ["novelty", "coverage"], f"""Prior-art pricing for R53-C1's PRIOR-ART leg for these CONFIRMED never-read presence-only tasks: {tlist}.
For each task decide, from archived public primaries, whether a presence-only (artefact-existence) weakness of THAT task's grader is
already documented anywhere public. {PA_RULES}"""))

# ---- 2. touch-run mechanical confirmation (2 executors x 10 tasks) --------------------------------------------
TOUCH = [(t, tests) for g in "ABCDE" for t, tests in GROUPS[g]]
for half, chunk in (("A", TOUCH[:10]), ("B", TOUCH[10:])):
    tlist = "; ".join(f"`{t}` ({tests})" for t, tests in chunk)
    ITEMS.append(item(f"C1TouchExec{half}", "executor", ["novelty", "operability"], f"""Mechanical check of presence-only on the real bytes. For each of these confirmed never-read tasks: {tlist}.
For each task's P1 test(s): create the stub paths the test asserts on as EMPTY files / empty directories under a bubblewrap sandbox
(read the captured test first: some name /logs, /workspace or other roots; create exactly what the assertions name, nothing more;
`bwrap --unshare-net --ro-bind / / --dev /dev --tmpfs /app --tmpfs /tests --tmpfs /logs …` or a mount namespace of your choice),
copy the captured test file from {LANE}/corpus/evidence/round52/graders/<task>/tests/test_outputs.py into the sandbox, and run
exactly the named test(s): `uv run --no-project --with pytest python -m pytest <file>::<test> -q -p no:cacheprovider` (add `--with`
for any module-level import the file needs — numpy, requests, … — and say so; do not run the agent's task, do not fetch task images).
Record per task+test: the stub paths you created, the command, the pytest outcome (`passed` | `failed` | `blocked: <why>`) and — for
context only — the outcome of the other tests in the file under the same stub world. `passed` on empty artefacts is the mechanical
confirmation of presence-only; `failed` is evidence AGAINST the classifier and the oracle — report it with the failing assertion line.
Deliver `<your seat dir>/touch-run.json` (`[{{"task","test_id","stub_paths","cmd","outcome","detail"}}]`) and the table in your
report. Do not read label files, classifier output or the wave-2 reader parts."""))

# ---- 3. blind re-label (4 reviewers, shards R1-R4) -------------------------------------------------------------
for i in (1, 2, 3, 4):
    ITEMS.append(item(f"C1RelabelRev{i}", "reviewer", ["novelty", "calibration"], f"""Blind re-label seat {i} of 4, a third-party check of the oracle. Read ONLY
{LANE}/.ufo/waves/round-53/p1-spec.md (the definition) and your shard {LANE}/.ufo/waves/round-53/relabel/shard-R{i}.json
(20 test ids with absolute file path and line span; a mix the L1 chose — you are not told which are likely Y or N) and the capture
files they point to (read each whole file and the same-task sibling captures such as tests/test.sh). For every id decide Y / N / U
exactly as the spec says (touch-sufficient or not, helpers and fixtures reached, no assertion = N). Write
`<your seat dir>/labels.json`: `{{"seat":"C1RelabelRev{i}","labels":{{"<id>":{{"label":"Y|N|U","why":"<=20 words"}}}}}}` covering the
shard exactly. You MUST NOT open any file under {LANE}/.ufo/waves/round-53/w1/ (label seats and classifier seats), {LANE}/.ufo/waves/round-53/w2/,
{LANE}/plans/round53_c1_classify.py, {LANE}/plans/round53-c1-freeze.json, or run the counter; you write no classifier. Report:
counts, the ids you found hardest and the exact clause of the spec that decided each."""))

# ---- 4. C1 attacks ---------------------------------------------------------------------------------------------
ITEMS.append(item("C1CritOracle2", "critic", ["novelty", "calibration"], f"""Attack the 305/305 oracle agreement (committed receipt {W}/claims/c1-after-oracle.txt; facts.md §C1). Angles, each with a concrete
command you ran: (1) spec ambiguity — read {W}/p1-spec.md and name clauses two careful readers could score differently; test your
reading against 5 capture files of your choice and say whether the classifier's class could flip under it; (2) shared-spec collusion —
the eight labellers share one written spec; look for a systematic misreading that yields perfect agreement on wrong labels (e.g. a
test that reads a fixture only when an env var is set): pick 10 Y-labelled tests and 10 N-labelled tests at random, read them
yourself against the spec, and report your own labels vs the oracle's; (3) the control — the round-52 classifier disagrees on 23
decided tests; check the disagreement direction (is v2 right on each of 5 sampled disagreements?); (4) freeze integrity — verify the
freeze-order leg is not forgeable (clone the lane, try to construct a label edit that survives `labels_after_freeze_and_untouched`).
Deliver a verdict: does the oracle survive, and what would falsify it. Do not edit anything outside your seat dir."""))

ITEMS.append(item("C1CritNeverRead", "critic", ["novelty", "calibration"], f"""Attack the CONFIRM leg's "never-read" property for the 20 confirmed tasks (list in {LANE}/corpus/evidence/round53/confirmations.json
after the L1 lands it; if absent, use the 20 task names in {W}/w2/C1ConfReadA.md and the candidates file {W}/claims/c1-candidates.txt).
The counter's blocklist greps only SCORECARD.md, LOG.md, SKILL.md, corpus/README.md, corpus/knowledge/* (minus the round-52 triage
entry) and the round-52 confirmations at the frozen base tip 536925b5320fa64298030b4ee76a58fc4b82723f. Widen the sweep: grep
PROVINCE.md, corpus/QUALITY.md, corpus/lessons/*, corpus/evidence/**, plans/** and .ufo/waves/round-52/** at the base tip
(`git show <rev>:<path> | grep -cw <task>`) for each of the 20 tasks, and report any hit with file:line and whether it shows the lane
had already examined that task before round 53 (a hit that merely lists task names in an unrelated census is not prior examination —
say which). Also check the round-52 confirmations for overlap and the reader reports' quotes for fabrication: re-locate 5 of the 20
quotes in the capture bytes yourself (line spans are in {LANE}/corpus/evidence/round53/tests-index.json). Verdict: is never-read
sound, and what would falsify it."""))

ITEMS.append(item("C1MutClassifier", "mutation-tester", ["novelty", "operability"], f"""Mutation-test the frozen classifier {LANE}/plans/round53_c1_classify.py (sha256 935db122…; do not edit it in place — copy to scratch).
Its own `--selftest` has 83 cases (receipt {W}/w1/C1ExecClassifier/fix-round-receipt.txt) and the counter's ORACLE leg re-scores the
305-test population. Build >= 15 mutants in scratch (flip one comparison, drop one helper-visit, confuse FunctionDef/AsyncFunctionDef,
treat decorators as body, off-by-one an end_lineno, drop the Constant-value check, etc.); for each: (a) does the classifier's
`--selftest` kill it, (b) does the 90-case adversarial set of `C1ExecAdvCases` kill it
(`python3 {W}/w1/C1ExecAdvCases/check.py <mutant>`), (c) does the population class of the 305 ids move (run the mutant over
{LANE}/corpus/evidence/round53/tests-index.json ids + capture bytes in scratch). Report the kill matrix and every survivor with the
case that should have killed it. Also re-run the pristine classifier's selftest and paste its tail."""))

ITEMS.append(item("C1MutCounter2", "mutation-tester", ["novelty", "operability"], f"""Mutation-test the AMENDED C1 counter {LANE}/plans/round53_c1_triage.py against the real evidence (copy the lane to scratch
(`git clone -q --shared {LANE} <scratch>/lane`), apply one mutant per run in the clone, keep the pristine copy). The wave-1 mutant
floor killed 77/81 with the extended suite; the frozen 47-case `--selftest` is what ships. Build >= 12 fresh mutants aimed at the
CONFIRM and PRIOR-ART legs specifically (accept a second row per task, drop the never-read check, accept `confirmed: "true"` string,
skip the report digest check, accept a sweep of the same file twice, accept a quote of 7 words, ignore the SOURCE-URL header mismatch,
count a rejected row as covered, drop the URL minimum, accept url example.org, allow `..` in fetched paths, treat a missing sweep as
empty); for each mutant report: killed by `--selftest` (yes/no, which case), killed on the REAL tree (run the counter in the clone —
expect `PREDICATE R53-C1 fail` via a REJECTED line), and the exact guard that fired. Deliver the matrix and, for every survivor, a
proposed selftest case as a unified diff to the selftest section. Do not modify the lane."""))

# ---- 5. C2 measure + attack ----------------------------------------------------------------------------------------------
for who in ("A", "B"):
    ITEMS.append(item(f"C2MeasureExec{who}", "executor", ["calibration", "operability"], f"""Independent full run of the C2 counter at the lane's current HEAD. `S={SCRATCH}/C2MeasureExec{who}; mkdir -p $S; git clone -q --shared {LANE} $S/lane;
git -C $S/lane rev-parse --show-toplevel` (must print `$S/lane`), record `git -C $S/lane rev-parse HEAD`. Run
`python3 plans/round53_c2_tipstate.py --lane . --source $S/lane --work $S/work --jobs 3 --timeout 900` (about 15-30 minutes; run it
detached: `nohup setsid … > $S/out.txt 2>&1 &`, then read the file — do not poll in a tight loop). Report the full output, exit code,
wall time, host load average before and after (`cat /proc/loadavg`), and for EVERY `MISMATCH`/`EVIDENCE-MISSING`/`TIMEOUT` line the
row's full output (read `<work>/disagreed-<row>.txt` and, if needed, run that row's argv alone in a fresh scratch clone to see why) —
the L1 needs the observed exit and a verbatim output fragment (one line, <= 200 chars) per disagreeing row to re-declare the ledger
truthfully. For the ~12 rows facts.md names as really red (round51-surfaces, state-assertion-check, round28-census, round35-c1-coverage,
round38-c1-mutants, mutant-direction-check, round46-c3, round52-c1, anchor-digest-check, gate-flip-check, adoption-check,
round40-c1-mutants), also state in one sentence whether the declared red reason in `plans/round53-tipstate.json` still matches what
you observed. Do not edit the ledger; do not edit anything outside your seat dir."""))

ITEMS.append(item("C2RevLedgerPlan", "reviewer", ["calibration"], f"""Review the C2 ledger `plans/round53-tipstate.json` AS COMMITTED (78 rows) against the registry in {LANE}/SKILL.md and the counter's
static legs (`python3 plans/round53_c2_tipstate.py --lane . --dry` in a scratch clone — paste output). For every `red` row: is the
reason >= 10 words, specific and truthful (not boilerplate), does the `evidence` fragment look like real instrument output (re-run 5
sampled rows' argv in your own scratch clone and compare the fragment verbatim), and is `exit` consistent with `state`? For every
`green` row sampled (5): re-run its argv and confirm exit 0. Flag any row whose declaration could have been copied from another row's
output, any duplicate evidence fragments across rows, and any reason that asserts a cause the output does not show. Report a table
(row, verdict, defect). Do not edit the lane."""))

ITEMS.append(item("R53CritDoNothing", "critic", ["calibration", "novelty"], f"""Do-nothing control duty (claim-sizing rule: a target a do-nothing control can reach is the wrong target). In a scratch clone at the
FROZEN BASE TIP (`git clone -q --shared {LANE} <scratch>/lane && git -C <scratch>/lane checkout --detach 536925b5320fa64298030b4ee76a58fc4b82723f`):
run `python3 plans/round53_c1_triage.py --lane .` (expect `PREDICATE R53-C1 fail` with `FREEZE absent`/`new_confirmed=0`/`PRIOR-ART
rows=0`) and `python3 plans/round53_c2_tipstate.py --lane . --dry` (expect `ledger=0 missing=75`, fail) — paste both outputs. Then in a
second clone at the CURRENT tip, delete the round's evidence inputs in scratch only (confirmations.json, prior-art.json, fetched/,
plans/round53-tipstate.json) and re-run both counters: each must fail, naming the leg. Also re-run the committed forged-complete
selftests at the current tip (`--selftest` on both counters; paste the `SELFTEST cases=… failures=…` lines). Verdict: does each frozen
predicate stay unreachable for a control that skips the claimed work; name any route a control could take that the counter cannot
distinguish from the work."""))

ITEMS.append(item("C2CritPredicate2", "critic", ["calibration"], f"""Attack the amended C2 counter + ledger pair for forgeable routes (A1/A3 closed the wave-1 list; find what remains). Clone the lane to
scratch; build >= 8 attacks as concrete commands: ledger with zero rows (heading renamed), 77 of 78 rows, argv `python3 -c pass <script>`
or a shell wrapper, `--source` pointing at a non-git dir or an older commit, a red row whose evidence fragment is a substring of ANY
row's output rather than its own, a ledger entry whose `timeout_s` exceeds the operator cap (A3), a row that commits inside its worker
and leaks into the next row (A3 reset), declared green for a gate that cannot fail (write a `always-exit-0` fixture script + registry
row + green ledger entry in the scratch clone only). For each: does the counter catch it (expected verdict line), and if it passes,
that is a FINDING — quote the output. Also run `--selftest` (52 cases) and report its tail. Do not edit the real lane."""))

# ---- 6. sources: literature scout + 2 scribes + 1 reviewer -------------------------------------------------
ITEMS.append(item("C1ScoutLitSrc", "scout", ["coverage", "novelty"], f"""Open the literature primaries this round's knowledge entry should cite, and record what a SOURCES row needs. Targets (open each,
fetch bytes, record sha256): (1) the Terminal-Bench 2.0 announcement/docs page or paper (whichever resolves; find the canonical URL);
(2) one peer-reviewed or widely-cited work on benchmark verifier weakness / reward hacking / tests that pass without solving the task
(search arXiv + ACL Anthology; e.g. verifier-gaming, benchmark saturation, test-quality audits — pick the TWO most on-point you can
actually fetch); (3) one primary on evaluation-harness test-quality practice (e.g. the SWE-bench or inspect_ai evaluation-harness docs
section on scorers). For each: URL fetched, HTTP status, access date 2026-10-30, sha256 of the bytes, and a <= 25-word verbatim quote
WITH its location (section heading/line) that grounds what it teaches this lane about presence-only graders or verifier strength.
Write `<your seat dir>/lit.json` (`[{{"url","status","sha256","quote","location","teaches","kind","suggested_tier","scope"}}]`).
Reject anything you cannot fetch with the reason. Do not duplicate a URL already in {LANE}/corpus/SOURCES.md (grep it first). These
are candidates: the L1 writes the rows. Do not read label files or classifier output."""))

SR_GROUPS = {"A": ["C1ScoutSrcTesting", "C1ScoutSrcAudit"], "B": ["C1ScoutSrcKaggle", "C1ScoutSrcPapers"]}
for who, groups in SR_GROUPS.items():
    gl = " and ".join(f"{W}/w1/{g}.md" for g in groups)
    alt = " or ".join(f"{W}/w1/{g}*.md" for g in groups)
    ITEMS.append(item(f"C1ScribeSources2{who}", "scribe", ["coverage", "novelty"], f"""Finalise registry rows for SOURCES.md from the wave-1 scouts' drafts, group {who}: {gl} (if a file is absent, `ls {W}/w1/C1ScoutSrc*.md` and take the
group-{who} ones). CORPUS.md rule 1 binds: re-open EVERY source yourself today (2026-10-30), not the archive: fetch the live URL,
confirm HTTP 200 and that your <= 25-word quote is located in what you fetched; record the access date, the location (line/section)
and the sha256 of your fetch in your report's table. Keep only sources that bear on tests that pass if an artefact merely exists (or
on grader/test-suite strength for agent benchmarks) — reject the rest as `rejected` rows with `REJECTED: <reason>; flip: <condition>`.
Tier per contract v1 (A primary for its scope; B strong secondary; C lead only; `community` never A). Write
`<your seat dir>/rows.md`: one row per kept/rejected source in the exact 11-column schema
(`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`), ids `T01…` (the L1 renumbers from
S194 by document), no `|` inside any cell, `opened` 2026-10-30, `recheck` ISO date or `90d`/`180d`, `used-by` `—`, status
`queued`/`rejected`. Also `<your seat dir>/gate.md`: for every row the URL, access date, the located <= 25-word quote with its
location. Read {LANE}/corpus/SOURCES.md first so no row duplicates an existing URL (the census flags duplicate URLs across scopes as
W04). Never edit the lane."""))

ITEMS.append(item("C1RevSources2", "reviewer", ["coverage", "calibration"], f"""Attack the new SOURCES row drafts (non-author spot check, in advance of the closure's). Rows come from `C1ScribeSources2A/B`'s
`<seat dir>/rows.md` + `gate.md` (they exist when your sibling scribes have finished; if not yet, read the wave-1 scout drafts
{W}/w1/C1ScoutSrc*.md for the rows you will meet and come back — your own work may begin with the existing registry
{LANE}/corpus/SOURCES.md rows S100 and S179-S193, whose conventions the new rows must follow) plus `C1ScoutLitSrc`'s `lit.json`.
For EVERY row: open the live URL yourself, locate the quote verbatim (or say it is absent: fabrication class), check the tier is
scoped and not inflated (`community` never A; a PR or issue is B at best; an open PR is mutable), the anchor is exact
(section/line + revision/date), `teaches` is a grounded learner benefit, status/recheck/used-by conform, no `|` in cells, no
duplicate URL with the registry (census W04). Report a table (row, opened ok y/n, quote found y/n, tier ok y/n, defect). Also run
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <a scratch copy of SOURCES.md with the new rows
appended to the Registry table under renumbered S-ids>` and paste its output and exit code. Never edit the lane."""))

# ---- 7. scribes: entry, lesson, scorecard/log, quality ------------------------------------------------------
FACTS = f"{W}/facts.md"
ITEMS.append(item("R53ScribeEntry2", "scribe", ["novelty", "coverage"], f"""Draft the round-53 knowledge entry `corpus/knowledge/tb2-presence-only-triage.md` as `<your seat dir>/entry.md` (shape of
{LANE}/corpus/knowledge/tb2-grader-vacuity-triage.md: first lines `source:`, `verified-at:`, `recheck:`; then the finding).
Read {FACTS}, the round-52 entry, the claims file (amendments included) and the wave-1 reports. The entry must state, with a located
pointer for each: what the instrument now is (AST classifier + eight blind labels + digest pins + freeze order), what the oracle
measured (305/305, control 23) and what it cannot support, the 28 never-read candidates, the 20 confirmations (five readers, quotes
located in test spans — `{W}/w2/C1ConfRead*.md`), `[pending: prior-art verdicts]` where you have no number, the limits (a
presence-only test beside a real content check is a weakness of that test; labellers are LLM seats sharing one written spec; the
counter cannot prove labeller independence), and a `## Re-run` section (the counting commands from the claims file). `source:` cites
SOURCES rows by the placeholder ids the source scribes use (`T01…`), plus `[pending: S-id mapping]`. No prose claim without a
pointer; counts carry their command."""))

ITEMS.append(item("R53ScribeLesson2", "scribe", ["calibration"], f"""Draft `corpus/lessons/round-53.md` as `<your seat dir>/lesson.md` following {LANE}/corpus/lessons/round-52.md (sections `## Gate`,
`## Mistakes`, `## Limits`, plus `## Assimilation`: none). Read {FACTS}, the round-52 lesson and verifier spot-check, the wave-1 attack
reports (C1CritCounterReach, C1MutCounter, C1SentinelScreen, C2CritLedgerReach, C2MutCounter under {W}/w1/), the run-1 C2 receipt
{W}/claims/c2-run1.txt and the wave-3 attack reports that exist when you write (C1CritOracle2, C1CritNeverRead, C2CritPredicate2,
C1MutClassifier, C1MutCounter2, C2MutLedger2 — read what is there, leave `[pending]` for the rest). `## Mistakes` rows (class ·
evidence pointer · captured-by · fix; a fix counts only once shown able to fail — cite the committed red-before output): at least
`counter-reachable-without-the-work` (second occurrence, repaired by A1: cite `{W}/claims/c1-selftest.txt` + `c2-selftest.txt` forged
cases), `rule-unit-leak` (the AST classifier fix round: {W}/w1/C1ExecClassifier/), `false-registry-cell` (the C2 ledger's run-1
mismatches: {W}/claims/c2-run1.txt), `operator-interruption-partial-wave` (the 2026-10-28 wrap-up stopped wave 2 with 5/42 seats
done: the round was re-dispatched; evidence: the round-53 report of attempt 1 at .ufo/reports/round-53/kengaku.md in the FLEET repo),
and any further class a wave-3 attack report names with a resolvable pointer. `## Gate`: the SOURCES candidates (group rows from the
scribes, placeholder ids), admits/rejects so far (`[pending]` where the L1 has not ruled), and the spot-check rows (`[pending:
non-author spot-check]`)."""))

ITEMS.append(item("R53ScribeScoreLog2", "scribe", ["calibration", "operability"], f"""Draft, from {FACTS} and the committed receipts, `<your seat dir>/scorecard-section.md` (a `## Round 53` section for SCORECARD.md in
the shape of the round-52 section: claim table with the frozen counting commands, before/after, verdicts, axis state carried,
capabilities table additions only for capabilities that RAN this round with a pointer, `### Planned (round 54)`),
`<your seat dir>/log-entry.md` (a LOG.md entry in the shape of the round-52 entry: motivating evidence, outcome, evidence pointers)
and `<your seat dir>/readme-rows.md` (the corpus/README.md index row for the new knowledge entry and bullets for the round-53
receipts/sources). Rules: no verdict the facts do not support — leave `[pending: <what>]` for anything the L1 has not measured
(confirmations are DONE: 20 confirmed, use that; prior art, C2 final run and the wave-3 attacks are `[pending]`); coverage stays 7
(L0 questions `kengaku | round-25`, `round-33`, `round-51` unanswered) and is not claimed; do not set any score change before the
facts say the claim verified. Every number: command + output or a pointer."""))

ITEMS.append(item("R53ScribeQuality2", "scribe", ["calibration", "adjacency"], f"""Draft `<your seat dir>/q43.md`: the QUALITY.md criterion Q43 (the same shape as Q42 at the end of {LANE}/corpus/QUALITY.md; it must
say what this round's two counters did to meet Q42 (a)/(b)/(c), what wave 1's attacks showed was still reachable and how A1 closed
it, and the limits: independence of labellers is a protocol property, a green ledger row can be a gate that cannot fail, never-read is
not never-examined). Read {FACTS}, the claims file amendments and the wave-1 attack reports. Also
`<your seat dir>/skill-notes.md`: the lines to add to SKILL.md (a short `## Presence-only grader triage` decision table and an entry
in the error-pattern list: classifier-vs-oracle, forged-complete controls, ledger tip-state) — cite committed paths; do not invent
commands. And `<your seat dir>/province-note.md`: whether PROVINCE.md needs any change (surfaces added: classifier, labels, ledger)
or says nothing changes, with the grep that shows it; and the exact replacement line for the PROVINCE row that the registry probe
flags (`python3 plans/round51_surfaces.py --lane .` in a scratch clone -> `NUMBER-DRIFT SF14 row claims 171, probe says SOURCES
rows=<observed>`): print the exact row line and the exact replacement — the L1 decides whether a frozen manifest may be amended."""))

# ---- 8. fleet hygiene: connector, surfaces scout, sentinel, revenger -----------------------------------------
ITEMS.append(item("R53ConnSiblings2", "connector", ["adjacency"], f"""Sibling-overlap scan for the round-53 claims and instruments. Check every sibling lane's current HEAD
(`ls /home/vgpnk/Projects/shokunin/ | grep shokunin`): does any sibling own or duplicate (1) a presence-only grader triage of an
agent benchmark, (2) a registry tip-state ledger re-executed per row, (3) a blind-label oracle over a frozen classifier, (4) SOURCES
literature on verifier weakness? Grep their SKILL.md/PROVINCE.md/plans/corpus for the concepts (not just the words) and report
owner-or-none per concept with the path you checked. Also collect one useful cross-lane pattern you saw this round that another lane
should know (report-out candidate, evidence sent not absorbed). Do not edit anything; do not message siblings."""))

ITEMS.append(item("R53ScoutSurfaces", "scout", ["freshness", "calibration"], f"""Per-surface reconnaissance at the lane's current HEAD. Run in a scratch clone (`git clone -q --shared {LANE} <scratch>/lane`):
`python3 plans/round51_surfaces.py --lane .` and paste the full output. For every non-clean line (DRIFT/UNVERDICTED/NUMBER-DRIFT/STALE),
state the exact manifest row, the observed truth (run the probe it names) and whether the manifest's expectation is stale because the
lane legitimately grew (new SOURCES rows, new registry rows) or because something broke. Check the three historical-absent surfaces
still absent (`test -e ~/Projects/webzites/repos/llm-wiki`, `test -e ~/archive/bench-arena`, `test -e ~/Projects/bounties`) and the
two live endpoints (`ss -ltn 'sport = :8791'`, `curl -s -m 5 http://127.0.0.1:45669/health`, `curl -s -m 5 http://127.0.0.1:1234/health`
— read-only, no model traffic). Deliver a verdict per surface: manifest-right / manifest-stale-growth / manifest-stale-broken / surface-moved,
with the command that shows it. Do not edit the lane."""))

ITEMS.append(item("R53SentinelFetch2", "sentinel", ["calibration", "adjacency"], f"""Security screen of the evidence this round lands. (1) Scan every file the wave-2 readers and wave-3 pricing/touch seats produced under
{W}/w2/ and {W}/w3/ (and the wave-1 scout archives {W}/w1/C1ScoutSrc*/) for credential-shaped strings (token/key/secret/password/op:///
Bearer/ghp_/AKIA), absolute host paths that would dangle, and prompt-injection payloads inside fetched third-party bytes (instructions
addressed to an AI reading the file). (2) The prior-art archives that will land in corpus/evidence/round53/fetched/ are third-party
bytes quoted into a committed corpus: flag any archive whose body embeds secrets, session URLs, or > 1 MiB of minimised JS. (3) Check
the captured grader bytes under {LANE}/corpus/evidence/round52/graders/ once more for live credentials (round-52 scan said clean;
confirm on a sample of 10 files). Report findings with file:line; class (credential / injection / privacy / none); and for each
finding whether it must block landing. Do not edit the lane."""))

ITEMS.append(item("R53RevengerCarried", "revenger", ["calibration", "operability"], f"""Reverse-engineer and verify the CARRIED routed defects from the round-52 closure (claims file §Frontier step, items 2-4). For each,
establish the current state at the lane's current HEAD with a command: (a) the untracked `tb2-paper-full.html` — find it
(`find {LANE} -name 'tb2-paper-full.html' -not -path '*/.git/*'`), report its size and sha256; the L1 deletes it before landing, so
confirm whether it still exists and whether anything cites it (`grep -rn 'tb2-paper-full' {LANE} --include='*.md' --include='*.json'
--exclude-dir=.git | head`); (b) absolute host paths in round-52 `corpus/evidence/round52/confirmations.json` — count them and confirm
the round-53 evidence files (confirmations.json once landed; the wave-2 reader parts) use repo-relative paths only; (c) the C2
`SELFTEST-UNBACKED` span fix and K5/K7 controls — locate the exact selftest lines in {LANE}/plans/round52_c2_registry.py that need
the span-scoped negation fix and the two named controls (read the round-52 closure's defect text in {LANE}/corpus/lessons/round-52.md
and the registry row), quote them, and propose the minimal diff the NEXT round should land (do not land it). Report each as
state / evidence / proposed action. Do not edit the lane."""))

assert len(ITEMS) == len({i["name"] for i in ITEMS})
spec = {
    "wave": "kengaku-r53-w3",
    "milestone": "kengaku round 53 wave 3 (completion): price the 20 confirmed tasks, touch-run and re-label the oracle, re-attack both counters, re-measure the tip-state ledger, finalise sources, draft entry/lesson/log",
    "reportDir": ".ufo/waves/round-53/w3",
    "maxLanes": len(ITEMS),
    "axes": ["novelty", "calibration"],
    "context": CONTEXT,
    "items": ITEMS,
}
out = Path(f"{W}/w3-spec.json")
out.write_text(json.dumps(spec, indent=1))
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print(f"wrote {out} items={len(ITEMS)}", roles)
attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "sentinel"))
print(f"attack seats={attack}/{len(ITEMS)}")
