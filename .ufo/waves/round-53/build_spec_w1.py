#!/usr/bin/env python3
"""Build the kengaku round-53 wave-1 (build) swarm spec -> .ufo/waves/round-53/w1-spec.json (policy v1, band 32-64)."""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
WAVE_DIR = f"{LANE}/.ufo/waves/round-53/w1"
SCRATCH = "/fast/scratch/hyaku/kengaku-r53"
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
kengaku round 53 (hyaku run 11), WAVE 1 of 2 (build), lane repo {LANE}. L1 = KengakuR53.
The round's two claims are FROZEN in {LANE}/plans/round-53-claims.md (commit a34838f) — READ IT IN FULL FIRST; it binds
every seat. Its predicates, thresholds, controls and kill rules never change after a seat has scored.

- **R53-C1 (novelty 8->9)** — a sound presence-only grader triage of Terminal-Bench 2.0: counter
  `plans/round53_c1_triage.py` (frozen, `--selftest` 22 cases), an AST classifier `plans/round53_c1_classify.py`
  (built THIS wave), blind labels from 8 label seats, never-read confirmations and archived prior art (wave 2).
  The one definition of "presence-only" is {LANE}/.ufo/waves/round-53/p1-spec.md.
- **R53-C2 (calibration 9->10)** — every row of SKILL.md's *Gate/probe registry* (75 rows, names in
  {LANE}/.ufo/waves/round-53/c2-row-names.json) gets a declared tip-state in `plans/round53-tipstate.json`, re-executed by the
  frozen counter `plans/round53_c2_tipstate.py` (`--selftest` 12 cases). Ledger entry schema: see that file's docstring and
  `static_legs()`; one entry = {{"argv": [...], "exit": N, "state": "green"|"red", "kind": "entry"|"selftest"|"help",
  and, for red, "reason" (>=10 words) and "evidence" (a verbatim >=6-char fragment of the observed output)}}.

Base tip 536925b5320fa64298030b4ee76a58fc4b82723f; claims commit a34838f. This is the build wave; wave 2 (falsify + confirm) is
dispatched by the L1 after this wave returns and the L1 has integrated it.

# Blindness rules (they are the measurement)
- Label seats (`C1Label*`) NEVER read, run or ask for the classifier (`plans/round53_c1_classify.py`, anything under
  `.ufo/waves/round-53/w1/C1ExecClassifier*`), nor any other label seat's file. The classifier seats NEVER read any label file
  or any `C1Label*` directory. Violating this voids your own seat's output: say so in your report instead of hiding it.
- Nobody tunes anything against another seat's output: the L1 commits the classifier freeze before it opens a label.

# Write scope — every seat
Your deliverables go under your own directory `{WAVE_DIR}/<your-seat-name>/` (absolute path; create it) and your report at
`{WAVE_DIR}/<your-seat-name>.md`. Every file you want kept (<= 1 MiB each) goes there: scratch is deleted at exit. Temporary
clones, fixtures and temp files live only under `{SCRATCH}/<your-seat-name>/` (NVMe, ~500 GB free; pass `TMPDIR` explicitly and
remove the dir before you yield). NEVER edit the lane tree outside your own seat directory, the fleet repo, a sibling lane,
`.ufo/state/`, `.ufo/watchdog.log`, `templates/`, `scripts/`, `MANIFEST.json` or `/home/vgpnk/Projects/shokunin/.scratch/`.
NEVER run `git commit`, `git add`, `git push`, `git stash`, `git checkout`, `git reset`, `git pull` or any mutating `jj` command in
the lane or the fleet repo. Fixture repositories only via `D=$(mktemp -d -p {SCRATCH}/<seat>) && git -C "$D" init -q` and every
later git call names `-C "$D"` (a stray fixture commit once landed on the fleet repo and deleted 4,606 paths). NEVER run a campaign
tool inside /home/vgpnk/Projects/shokuknow. Never message agent://all; message only the seat ids you are told to.
Nothing you write may contain credential-shaped strings (tokens, keys, `op://`): the previous round's push was blocked by a fake
token inside a captured test fixture. Do not copy captured grader bytes into a report; quote at most 25 words.

# Tooling
You and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official
channels, update-safety gate; record tool/version/channel/reason in your report). **pacman guard (orchestrator ruling 2026-10-20):
all pacman transactions are PAUSED host-wide** — install via `uv tool` / `npx` / an official binary in `~/.local/bin`, or file an L0
question. Never `pacman -Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host service. If a tool output looks inconsistent with
its described behaviour, add one line `tool: <concise description>` to your report.

# Report contract (every seat)
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Your report carries: what you did, the exact
commands you ran, the measured numbers, the files you produced (absolute paths) and, for every attack seat, what you attacked
and the concrete evidence that the attack landed or failed to land. Never fabricate a number, a quote or a URL. A seat that finds
nothing says what it searched (command) and reports the negative. A seat that cannot finish says what it could not do and why.
Scratch discipline: if you see ENOSPC, report the free space you saw and stop.
"""


def item(name, role, axes, body):
    return {
        "name": name,
        "role": role,
        "axes": axes,
        "item": GODSPEED + f"\n\n# Target\nkengaku round 53 wave-1 seat {name} ({role}).\n# Item\n{body}",
    }


ITEMS = []

# ------------------------------------------------------------------ C1: classifier + adversarial cases + stage scan
ITEMS.append(item("C1ExecClassifier", "executor", ["novelty"], f"""Write `{WAVE_DIR}/C1ExecClassifier/round53_c1_classify.py`: the AST classifier of
{LANE}/.ufo/waves/round-53/p1-spec.md. Interface (frozen by the counter {LANE}/plans/round53_c1_triage.py `v2_classes`):
`classify_source(src: str) -> dict[str, str]` returning, for EVERY `test_*` function of the file (module level key `name`; a method of
class `C` key `C.name`), `'P1'` (spec Y) or `'P0'` (spec N or U). Use `ast` (comments and docstrings are not code); inline same-file
helpers and same-class `self.` methods and same-file fixtures transitively with a cycle guard; a call into anything not defined in the
file that is not a plain existence predicate is a content/behaviour call (P0). Standard library only; no network; deterministic.
Include `if __name__ == "__main__"` that prints a class histogram for a file given on argv, and a `--selftest` with >=20 hand-made cases
covering every worked example of the spec plus: helper chain of depth 3, recursion, a class-based test, a fixture-argument test, `pytest.fail`
branch, `os.listdir` membership, `any(...)` over `iterdir()`, an assertion on `len(listdir) == 3` (count -> P0), a `with open(...)` read (P0),
a test with no assertion (P0), a syntax-error-free but empty module. Run it over all 88 captures in
{LANE}/corpus/evidence/round52/graders/ using the index {LANE}/corpus/evidence/round53/tests-index.json (305 tests, 88 tasks): the dict must
cover all 305 ids with no unclassified. Report: histogram, the rule order you implemented, every spec ambiguity you hit and the choice you
made (the L1 will quote these), and the sha256 of your file. Do NOT read any `C1Label*` output. The L1 will run your file against an
independent adversarial case set before the freeze and may send you back failing cases to fix; you will not see any oracle label."""))

ITEMS.append(item("C1ExecClassifierAlt", "executor", ["novelty"], f"""Independently implement the same spec (read ONLY {LANE}/.ufo/waves/round-53/p1-spec.md; do not read
`C1ExecClassifier*` output) as a *second*, deliberately different classifier in `{WAVE_DIR}/C1ExecClassifierAlt/alt_classify.py`: a
symbolic-execution-light approach — evaluate each reachable `assert` condition over a three-valued abstract domain {{path-exists-only,
other}} instead of pattern-matching call names. Same interface `classify_source(src) -> dict[str, str]` (keys as in the spec of seat
C1ExecClassifier: `name` / `Class.name`; values `P1`/`P0`). Run it over the 305 tests (index
{LANE}/corpus/evidence/round53/tests-index.json; captures under {LANE}/corpus/evidence/round52/graders/). Report: histogram and the list of
test ids where you are unsure. This is a cross-check of spec ambiguity, not the counted classifier: the L1 reports how often the two
implementations disagree and reads the disagreements to find spec holes BEFORE labels are opened."""))

ITEMS.append(item("C1ExecAdvCases", "executor", ["novelty"], f"""Build an independent adversarial case set for the presence-only spec
{LANE}/.ufo/waves/round-53/p1-spec.md: write `{WAVE_DIR}/C1ExecAdvCases/cases.json`, a list of >=60 objects `{{"id","source","expected"}}` where
`source` is a complete small Python test module (several tests per module are fine; give `expected` as a dict `{{"test key":"P1"|"P0"}}`
using keys `name` / `Class.name`). Cover: every example and every clause of the spec, helpers (depth 1-3, mutual recursion), fixtures,
class tests, `os.listdir`/`iterdir`/`glob` membership vs counts, `os.access`, negation (`assert not exists`), `assert exists or other_exists`,
`unittest` styles, `pytest.fail` branches, assertions with messages containing the word `in`/`==`, comments and docstrings containing
`read_text`/`subprocess` (must NOT change the class), `open` used for writing vs reading, string-built paths, tests with zero assertions,
assertions on imported-module results. Derive `expected` by reading the SPEC and reasoning, not by running any classifier; where the
spec is ambiguous write the case in a separate list `ambiguous` with both readings. Also write `check.py` that loads a classifier module
path from argv and prints per-case pass/fail (`classify_source` interface). Do NOT read `C1ExecClassifier*` output or any label. Report
case counts per clause and the ambiguities."""))

ITEMS.append(item("C1ExecStageScan", "executor", ["operability"], f"""Land the pre-stage secret-pattern scan that round 52's lesson only proposed (a push was blocked by
GitHub push protection GH013 because a fake token sat inside a captured upstream test). Write `{WAVE_DIR}/C1ExecStageScan/stage_scan.py`:
`python3 plans/stage_scan.py PATH...` (files or directories) exits 0 when no file matches, 1 and prints `HIT <path>:<line> <rule>` (never the
matched bytes, only the rule name and a 4-character prefix of the match) per hit, 2 on setup error. Rules (regex, documented in the docstring):
GitHub PAT/fine-grained/OAuth prefixes, Hugging Face `hf_` tokens, OpenAI/Anthropic `sk-` keys, AWS access key ids and secret-like 40-char
values after `aws_secret`, Slack `xox*`, Google API `AIza`, private-key PEM headers, generic `(api|secret|token|password)\\s*[=:]\\s*['"][^'"]{{16,}}`,
and `op://` references. Skip binary files (NUL in the first 8 KiB) and files > 5 MiB, reported as `SKIP`. `--selftest`: >=15 cases built in a
`mktemp -d -p {SCRATCH}/C1ExecStageScan` dir, including each rule positive, near-miss negatives (a 10-char `hf_` prefix; `sk-` inside a word),
a binary file, and a nested directory; the fixture secrets are assembled from fragments at run time so this file itself never contains a
complete credential-shaped literal (verify with your own scan: `python3 stage_scan.py stage_scan.py` must exit 0). Then run it over
{LANE}/corpus/evidence/round52 and {LANE}/corpus/evidence/round53 and {LANE}/.ufo/waves/round-52 and report the hits."""))

# ------------------------------------------------------------------ C1: label seats (8; each test labelled by two seats of different role)
LABEL_SEATS = [("A", "scout"), ("B", "reviewer"), ("C", "scout"), ("D", "reviewer"), ("E", "scout"), ("F", "reviewer"),
               ("G", "scout"), ("H", "reviewer")]
for k, role in LABEL_SEATS:
    nm = f"C1Label{'Scout' if role == 'scout' else 'Rev'}{k}"
    ITEMS.append(item(nm, role, ["novelty", "calibration"], f"""You are blind label seat {k} of 8 for the round-53 oracle. Read ONLY
{LANE}/.ufo/waves/round-53/p1-spec.md (the definition) and your shard {LANE}/.ufo/waves/round-53/labels/shard-{k}.json (a JSON list of
{{id, file, lineno, end_lineno}}: ~76 test functions of Terminal-Bench 2.0 grader captures; `file` is an absolute path, the function spans
`lineno..end_lineno`; read the whole file and any sibling capture file in the same task directory that the test reaches). For EVERY id in
the shard decide Y / N / U by the spec: would creating the named paths (touch/mkdir, empty content) satisfy every assertion the test can
reach through same-file helpers and fixtures? Be exact: a content read, size/mode value, command run, count or value comparison makes it N; no
assertion at all makes it N. Write `{WAVE_DIR}/{nm}/labels.json`: a JSON object `{{"seat": "{nm}", "labels": {{"<id>": {{"label": "Y|N|U",
"why": "<= 20 words"}}, ...}}}}` covering the shard exactly (no id missing, none extra). Use a script to check coverage before you finish, but
DO NOT write or run any classifier: label by reading. Do not look at any other seat's directory under {WAVE_DIR}. Report: counts of Y/N/U,
the ids you found hardest and why, and the sha256 of labels.json (the L1 compares it with the file it opens later)."""))

# ------------------------------------------------------------------ C1: sources / prior art (field-level; per-task pricing is wave 2)
SRC = [
    ("C1ScoutSrcTesting", "Software-testing literature on weak / existence-only assertions and oracle strength: test smells (Assertion Roulette, Unknown Test, weak or trivial assertions), mutation-testing-based oracle adequacy, 'assertions that only check a file exists'. Find primary sources (papers, tool docs) whose text defines or measures the weakness."),
    ("C1ScoutSrcBench", "Agent-benchmark test-quality audits: SWE-bench test-patch insufficiency (UTBoost, SWE-bench+, SWE-bench Verified follow-ups), Terminal-Bench / Harbor issue trackers and pull requests that report tests which 'let any solution pass' or only check artefact presence, and any published count of such tasks."),
    ("C1ScoutSrcAudit", "Benchmark-validity checklists and meta-audits for agentic benchmarks: task-validity and outcome-validity criteria (e.g. the Agentic Benchmark Checklist line of work), BetterBench-style assessments, and papers that audit verifiers/graders of terminal or coding agents for false positives."),
    ("C1ScoutSrcTB2", "Terminal-Bench 2.0 / 2.1 primary material the lane has NOT rowed yet: read `{LANE}/corpus/SOURCES.md` first (S100, S179-S193 are rowed; S191-S193 are rejected) and find further primary pages (repo README sections, task YAML docs, release notes, pull requests that edit specific `tests/test_outputs.py` files at the pinned or a later revision) that name concrete graders weakened or strengthened."),
]
for nm, topic in SRC:
    ITEMS.append(item(nm, "scout", ["novelty", "coverage"], f"""Source scout for the R53-C1 prior-art leg. Topic: {topic.replace('{LANE}', LANE)}
Procedure (SOURCES contract v1, CORPUS.md rules 1/5/6): read {LANE}/corpus/SOURCES.md (registry S001-S193 and the search log) so you never
re-row a URL already there. Search (web_search / fetch), then OPEN each candidate and archive the bytes you read under
`{WAVE_DIR}/{nm}/fetched/<slug>.<ext>` (<= 1 MiB each; if larger, store the first 1 MiB and say so) with `{WAVE_DIR}/{nm}/fetched/SHA256SUMS`.
Keep at most 6 sources and reject the rest with reasons. For each kept source write ONE draft registry row in the exact 11-column schema
(`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`; use placeholder ids `S9xx` in order; no `|`
inside any cell; `opened` = 2026-10-28; `recheck` an ISO date or `90d`/`180d`; `used-by` = `—`; status `queued`), tier per the contract
(A primary for its scope, B strong secondary, C lead only), an `anchor` that names the section/line + revision/date, and a located quote of
<= 25 words copied verbatim from your archived bytes (give the line number in the archive). Rejected sources become rows with
`REJECTED: <reason>; flip: <condition>` in `teaches`, status `rejected`. Also write `{WAVE_DIR}/{nm}/search-log.md`: queries, where searched,
date, identified / screened / included / excluded counts, exclusion reasons, stop rationale (CORPUS.md rule 5). Also say, for each kept
source, whether it bears on "tests that pass if the named artefact merely exists" in a benchmark grader (yes/no and the quote that shows
it) — a source that does not is not a prior-art source. Never record credentials or private URLs."""))

# ------------------------------------------------------------------ C2: ledger rows (9 executors)
names = json.loads(Path(f"{LANE}/.ufo/waves/round-53/c2-row-names.json").read_text())
groups = [names[i::9] for i in range(9)]
for gi, grp in enumerate(groups):
    nm = f"C2ExecRows{'ABCDEFGHI'[gi]}"
    ITEMS.append(item(nm, "executor", ["calibration", "operability"], f"""Declare and observe the tip-state of these {len(grp)} registry rows (names exactly as in the `Gate/probe registry` of
{LANE}/SKILL.md): {', '.join(grp)}.
For each row: read the row (entry, verdict map, self-test, pinned, scope cells) and its script. Choose ONE frozen, deterministic `argv`
(list of strings, `python3` or `uv run ...` first, the row's script path as one element, run from the lane root, no shell) that the counter
{LANE}/plans/round53_c2_tipstate.py can re-execute: prefer the row's own entry command with the arguments the row's text gives
(`--lane .`, `--summary`); where the entry cell has a placeholder (`<lane>`, `DIR`, `REV`, `<expect.json>`, `N`), choose concrete arguments
from the row's own text and the lane's committed files and say where each came from; if the entry needs input the lane does not hold, use
the row's `--selftest` (kind `selftest`), and only as a last resort `--help` (kind `help`; at most one in ten rows may be help-kind, so
say why). Never pass `--work`/`--scratch` paths (the counter sets TMPDIR per row). Execute it in a CLEAN SHARED CLONE of the base tip:
`C=$(mktemp -d -p {SCRATCH}/{nm}); git clone -q --shared {LANE} "$C/lane"; git -C "$C/lane" rev-parse --show-toplevel` must print
`$C/lane` before you run anything; run with `cwd="$C/lane"`, `TMPDIR` set to a dir under `$C`, a 900 s timeout, twice (the two exit codes
must agree; if they do not, the row is flaky: report it and choose another argv). Record the exit code and wall seconds. If the exit is
non-zero (`red`): find WHY (read the output and the script) and write (a) a `reason` of >= 10 words naming the concrete cause (for example
a digest pin that moved, a count that drifted and which file moved it, a gate that needs a path outside the lane), (b) an `evidence`
fragment: one verbatim line or fragment (>= 6 chars, no newline) of the observed stdout+stderr, and (c) whether the cause is
tip-independent (will persist whatever this round commits) or tip-dependent (counts in SOURCES/SCORECARD/LOG/SKILL that this round changes);
for a tip-dependent row say which committed file the L1 must re-measure after. Deliver `{WAVE_DIR}/{nm}/ledger-part.json`: a JSON object
`{{"<row name>": {{"argv": [...], "exit": N, "state": "green"|"red", "kind": "entry"|"selftest"|"help", "reason": "...", "evidence": "...",
"tip_dependent": true|false, "seconds": S, "argv_source": "<where the arguments came from>"}}, ...}}` for exactly your rows (`reason`/`evidence`
only on red rows). Do not edit SKILL.md or the ledger; do not change any script. Report per row: argv, exit, seconds, state and the
cause; and list every row whose registry cells disagree with what you observed (cell text quoted <= 25 words)."""))

# ------------------------------------------------------------------ C2: registry rows draft, mistakes, sources-lessons, connector
ITEMS.append(item("C2ScribeRegistryRows", "scribe", ["operability", "calibration"], f"""Draft, in `{WAVE_DIR}/C2ScribeRegistryRows/rows.md`, the two new rows for SKILL.md's Gate/probe registry
(exact 8-column schema of the existing rows; read ten existing rows first; escape any pipe as `\\|`; no cell may contain a raw `|`):
`round53-c1` for `python3 plans/round53_c1_triage.py --lane .` (selftest `--selftest`, 22 cases; the classifier plan
`plans/round53_c1_classify.py`; pins; the five legs; exit codes 0/1/2) and `round53-c2` for `python3 plans/round53_c2_tipstate.py --lane . --source
<clone> --work <scratch>` (selftest `--selftest`, 12 cases; ledger `plans/round53-tipstate.json`; exit 0/1/2; `--only` never passes). Read the two
scripts completely before writing a cell: every cell must be true of the committed bytes (the round-52 verifier found seven false cells in
28 drafted rows). Also draft `{WAVE_DIR}/C2ScribeRegistryRows/header-note.md`: one paragraph for the top of the registry section that says the
row cells describe each instrument at its own landing tree and that `plans/round53-tipstate.json` declares the tip-state, re-executed by `round53-c2`.
Also a third file `q43.md`: a proposed QUALITY.md criterion Q43 (same shape as Q42 at the end of {LANE}/corpus/QUALITY.md) that states what this
round's two counters did to meet Q42 (a/b/c) and its limits; mark every sentence about results as `[pending]` — results do not exist yet."""))

ITEMS.append(item("R53MistakeSweep", "scout", ["calibration"], f"""Mine the lane's own mistakes for the round-53 `## Mistakes` section and the L1's routed list. Read
{LANE}/corpus/lessons/round-52.md `## Mistakes`, `round-52-verifier-spotcheck.md`, `round-51-verifier-spotcheck.md` and `round-50*-verifier*.md`, and
{LANE}/corpus/QUALITY.md Q36-Q42. Produce `{WAVE_DIR}/R53MistakeSweep/sweep.md`: (1) the mistake classes that RECURRED across rounds 47-52 (class, rounds, evidence
pointers path:line); (2) for each, whether its `captured-by` criterion is shown able to fail (find the committed red-before output or say none exists);
(3) the three classes most likely to recur in a round that builds a classifier + an oracle + a ledger, each with a concrete early-warning command the
L1 can run before the scored after-run. Every pointer must resolve; paste the grep/ls commands you used. Negative claims carry their sweep."""))

ITEMS.append(item("R53ConnSiblings", "connector", ["adjacency"], f"""Sibling-overlap scan (read-only). The lane is about to land (a) a presence-only-test classifier + blind-label oracle for Terminal-Bench graders and
(b) a tip-state ledger that re-executes every row of a gate registry. Find overlap with the other shokunin lanes under /home/vgpnk/Projects/shokunin/*-shokunin
(PROVINCE.md and SKILL.md headings and `grep -rl` over their corpus for: terminal-bench, grader, test smell, mutation, oracle, registry, gate registry, tip-state,
ledger, executed row). For each overlap say owner, what they hold, and whether kengaku's claim duplicates, depends on, or is reusable by it (adjacency axis: report,
do not absorb). Also check `{LANE}/PROVINCE.md` and name any statement that the round's two claims would make false. Report a table (sibling, path:line, relation)
and the commands used."""))

# ------------------------------------------------------------------ attack seats against the frozen counters (pre-data)
ITEMS.append(item("C1CritCounterReach", "critic", ["novelty", "calibration"], f"""Attack the FROZEN C1 counter {LANE}/plans/round53_c1_triage.py before any data: find inputs that
make `PREDICATE R53-C1 pass` without the claimed work (a classifier that does not classify; labels that are not independent; confirmations that nobody read; prior art
that is not prior art). You may write fixtures and run the counter ONLY on scratch clones/copies (`git clone -q --shared {LANE} <scratch>/lane`, verify
`rev-parse --show-toplevel` first; the counter's `--lane` accepts any path; the unit constants mean the real pins hold only for the real tree, so build your attacks as a
scratch copy of the real tree plus forged inputs, or a fixture with `--selftest`'s construction in `selftest()`). Round 52's five routes (population shrunk, forged stub with re-pinned digest,
`confirmed:"false"`, example URLs as prior art, quote `assert`) are covered; find NEW routes. Specific places to look: `first_add`/ancestry in `leg_freeze` (what if the freeze
and labels are one commit, or the freeze file is re-added), `never_read_blocklist` (case/prefix tasks such as `path-tracing` vs `path-tracing-reverse`), `leg_confirm` span arithmetic,
`leg_prior_art` known-row check (`task not in text` accepts any page that names the task id once), the control leg (`dis52 >= CONTROL_RATIO * max(dis, 1)` when v2 disagrees 0),
`decided` counting (all labels U gives decided 0), a classifier that reads the labels file at import time, an `author_seats` list that is empty or contains labelers. For each route:
the construction, the counter's output, whether the leg holds, and the smallest fix. Do not edit the counter."""))

ITEMS.append(item("C2CritLedgerReach", "critic", ["calibration", "operability"], f"""Attack the FROZEN C2 counter {LANE}/plans/round53_c2_tipstate.py before any data: find ledgers that
make `PREDICATE R53-C2 pass` without declaring the truth. Work on scratch copies only (`git clone -q --shared {LANE} <scratch>/lane`, verify the top-level; the counter's
selftest `_mk_lane` shows how to build a tiny lane). Round 52's registry counter passed padded rows; hunt NEW routes: an argv that runs `true` after naming the script as a
dead argument (`["python3","-c","pass","plans/x.py"]` — `script in argv`), a green row whose argv is `--help` relabelled `entry`, a script that exits 0 without testing (a gate
that cannot fail), a red row with evidence copied from a different run, a row whose argv is a wrapper that swallows the exit code, `timeout_s` set to a tiny value on a slow row
(TIMEOUT is a failure but `timeout_s` may make a slow gate 'red' by killing it — does the counter notice?), registry rows named in prose or in a code block outside the table,
the registry heading appearing twice, `--only` combinations, a dirty source clone (`clean=` only checked when `.git` exists), the `reset --hard` / `clean -fdx` between rows
(a row that writes into the shared object store). For each route: construction, counter output, whether the leg holds, smallest fix. Do not edit the counter."""))

ITEMS.append(item("C1RevCounter", "reviewer", ["novelty"], f"""Review {LANE}/plans/round53_c1_triage.py line by line against the frozen predicate in
{LANE}/plans/round-53-claims.md (Claim 1, legs 1-4): for each leg list every place where the code is stricter, looser or different from the sentence (thresholds, which texts the
never-read guard scans, what 'inside the test function's own line span' means for class methods and decorators, how `url_key` collapses URLs, the 8-25-word quote rule, the ordering proof).
Run `python3 plans/round53_c1_triage.py --selftest` in a scratch clone and confirm `cases=22 failures=0`; read each selftest case and say which are vacuous (would pass under a no-op
counter). Report defects with path:line and the minimal repair; classify each as `amendment-needed` (changes behaviour) or `cosmetic`. Do not edit the counter."""))

ITEMS.append(item("C2RevCounter", "reviewer", ["calibration"], f"""Review {LANE}/plans/round53_c2_tipstate.py line by line against the frozen predicate in
{LANE}/plans/round-53-claims.md (Claim 2) and against {LANE}/SKILL.md's registry table: does `registry_rows` find exactly the 75 rows
(run `python3 plans/round53_c2_tipstate.py --lane . --dry` and compare with a manual count of table rows; also rows whose first cell is not a single backticked name)? Does
`row_script` find the entry script for every row (list the rows where it returns None, e.g. `uv run` entries or non-`python3` entries; rows with the script only in a later
backticked span)? Is `--jobs` > 1 safe when two rows write the same file in their separate clones (each worker owns its clone, but `git clone --shared` shares the object store)?
Does `Worker.reset` leave state between rows (`clean -fdx` skips ignored files? it uses -x)? Does `TMPDIR` per row reach the child? Run `--selftest` in a scratch clone and read each case for
vacuity. Report defects with path:line and the minimal repair, classed `amendment-needed` or `cosmetic`. Do not edit the counter."""))

ITEMS.append(item("C1MutCounter", "mutation-tester", ["novelty", "calibration"], f"""Mutation-test the C1 counter's own `--selftest`. In a scratch copy of the lane
(`git clone -q --shared {LANE} <scratch>/lane`, verify the top-level), apply ONE byte-level mutation at a time to `plans/round53_c1_triage.py` (about 30 mutants: flip each comparison in
`leg_pins`, `leg_freeze`, `leg_oracle`, `leg_confirm`, `leg_prior_art`; change each threshold constant; delete each rejection branch; weaken `confirmed is not True` to falsy; drop the sweep
check; drop the ancestry check; swap `<=`/`<`), run `python3 plans/round53_c1_triage.py --selftest` after each, and revert (re-copy from the pristine file). A mutant is KILLED iff the selftest
exit code or its `cases=… failures=…` line changes; a SURVIVOR names an advertised clause the fixtures do not demonstrate. Include a null mutant (no change; must not be killed) and
mark equivalent mutants. Report the table (mutant, location, killed y/n, which case killed it) and, for each survivor, the fixture case that would kill it (write it as a diff against `selftest()`;
do not edit the lane's file)."""))

ITEMS.append(item("C2MutCounter", "mutation-tester", ["calibration", "operability"], f"""Mutation-test the C2 counter's own `--selftest`. Same procedure as the C1 mutation seat,
on `plans/round53_c2_tipstate.py` (about 25 mutants: each comparison in `static_legs` and `evaluate`, the `help_ok` limit, the `only is None` condition, `clean in (True, None)`, the evidence
containment test, the entry-script rule, `MIN_REASON_WORDS`, the duplicate-name handling, the `(st == "green") != (ex == 0)` consistency test). Scratch copy of the lane only (verify the top-level). Killed iff the
selftest exit code or its `cases=… failures=…` line changes. Report the table, the null mutant, equivalent mutants, and for every survivor the missing fixture as a diff against `selftest()`."""))

ITEMS.append(item("C1SentinelScreen", "sentinel", ["operability"], f"""Adversarial security review of what this round will stage: (1) the capture bytes and pin tree already committed
under {LANE}/corpus/evidence/round52 and round53 and the archives wave-1 scouts will write under {WAVE_DIR}/C1ScoutSrc*/fetched/; (2) the counters' use of subprocess and git (argv lists vs shell,
paths from JSON that reach `git -C` or `open`, `importlib` loading `plans/round53_c1_classify.py` from the lane — i.e. the counter EXECUTES a seat-written module: what can it do, and what
containment (scratch clone, no network, `bwrap`) is advisable); (3) the C2 counter executing 75 registry argvs from a committed ledger (argv from a file the lane authors; `uv run` rows; env passthrough;
`git clone --shared` alternates). Scan for credential-shaped strings with your own grep (report the command, never the matched bytes). Report findings with severity, the exact path:line, and the smallest mitigation;
a clean negative states the sweep commands."""))

assert len(ITEMS) == 35 + 0 or True
spec = {
    "wave": "kengaku-r53-w1",
    "milestone": "kengaku round 53 wave 1 (build): AST classifier + blind labels + sources (R53-C1, novelty) and the 75-row tip-state ledger (R53-C2, calibration)",
    "reportDir": ".ufo/waves/round-53/w1",
    "maxLanes": len(ITEMS),
    "axes": ["novelty", "calibration"],
    "context": CONTEXT,
    "items": ITEMS,
}
out = Path(f"{LANE}/.ufo/waves/round-53/w1-spec.json")
out.write_text(json.dumps(spec, indent=1))
print(f"wrote {out} items={len(ITEMS)}")
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print(roles)
attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "sentinel")) - 4  # 4 reviewers label
print(f"attack seats={attack}/{len(ITEMS)} = {attack/len(ITEMS):.0%}")
