#!/usr/bin/env python3
"""Build the kengaku round-53 wave-2 (falsify + confirm + draft) swarm spec -> .ufo/waves/round-53/w2-spec.json (policy v1)."""
import json
import sys
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
W = f"{LANE}/.ufo/waves/round-53"
WAVE_DIR = f"{W}/w2"
SCRATCH = "/fast/scratch/hyaku/kengaku-r53"
INT = sys.argv[1] if len(sys.argv) > 1 else "UNSET"          # the integration commit wave 2 attacks (full hash)
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
kengaku round 53 (hyaku run 11), WAVE 2 of 2 (falsify, confirm, draft), lane repo {LANE}. L1 = KengakuR53.
Frozen claims: {LANE}/plans/round-53-claims.md (read it in full, amendment A1 included). Facts of the round so far, with exact numbers and
pointers, are in {W}/facts.md — READ IT FIRST. The integration commit wave 2 attacks is `{INT}` (check with `git -C <your clone> rev-parse HEAD`).

- **R53-C1 (novelty 8->9)**: counter `plans/round53_c1_triage.py`, classifier `plans/round53_c1_classify.py` (frozen, sha256 935db122…), oracle = eight
  blind label files, never-read candidates (28 tasks, `{W}/claims/c1-candidates.txt`), confirmations and prior art (this wave).
- **R53-C2 (calibration 9->10)**: counter `plans/round53_c2_tipstate.py`, ledger `plans/round53-tipstate.json` (77 registry rows), re-executed in a clean clone.

# Write scope — every seat
Your deliverables go under your own directory `{WAVE_DIR}/<your-seat-name>/` (absolute path; create it) and your report at
`{WAVE_DIR}/<your-seat-name>.md`. Every file you want kept (<= 1 MiB each) goes there: scratch is deleted at exit. Temporary clones,
fixtures and temp files live only under `{SCRATCH}/<your-seat-name>/` (NVMe; pass `TMPDIR` explicitly and remove the dir before you yield). Clone the lane
for any run: `git clone -q --shared {LANE} {SCRATCH}/<seat>/lane && git -C {SCRATCH}/<seat>/lane rev-parse --show-toplevel` must print that path before anything else.
NEVER edit the lane tree outside your own seat directory, the fleet repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `templates/`, `scripts/`,
`MANIFEST.json` or `/home/vgpnk/Projects/shokunin/.scratch/`. NEVER run `git commit`, `git add`, `git push`, `git stash`, `git checkout`, `git reset`, `git pull`
or any mutating `jj` command in the lane or the fleet repo. Fixture repositories only via `D=$(mktemp -d -p {SCRATCH}/<seat>) && git -C "$D" init -q` with every
later git call naming `-C "$D"` (a stray fixture commit once landed on the fleet repo and deleted 4,606 paths). NEVER run a campaign tool inside
/home/vgpnk/Projects/shokuknow. Never message agent://all; message only seat ids you are told to. Nothing you write may contain credential-shaped strings
(tokens, keys, `op://`); do not copy captured grader bytes wholesale into a report (quote <= 25 words). If you use `gh api`, never print or store the token.

# Tooling
You and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record
tool/version/channel/reason in your report). **pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide** — install via `uv tool` /
`npx` / an official binary in `~/.local/bin`, or file an L0 question. Never `pacman -Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host service. If a tool output looks
inconsistent with its described behaviour, add one line `tool: <concise description>` to your report.

# Report contract (every seat)
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Your report carries: what you did, the exact commands you ran, the measured numbers, the files
you produced (absolute paths) and, for every attack seat, what you attacked and the concrete evidence that the attack landed or failed to land. Never fabricate a number, a quote
or a URL. A seat that finds nothing says what it searched (command) and reports the negative. A seat that cannot finish says what it could not do and why. If you see ENOSPC,
report the free space you saw and stop.
"""


def item(name, role, axes, body):
    return {"name": name, "role": role, "axes": axes,
            "item": GODSPEED + f"\n\n# Target\nkengaku round 53 wave-2 seat {name} ({role}).\n# Item\n{body}"}


ITEMS = []

# ---- candidates: 28 never-read tasks with their P1 test names, from claims/c1-candidates.txt
cand = []
for line in Path(f"{W}/claims/c1-candidates.txt").read_text().splitlines():
    if line.startswith("CANDIDATE "):
        _, task, tests = line.split(" ", 2)
        cand.append((task, tests.removeprefix("tests=").split(",")))
assert len(cand) == 28, len(cand)
groups = [cand[i::7] for i in range(7)]
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"


def glist(g):
    return "; ".join(f"`{t}` (test(s): {', '.join(ts)}; test id(s): " + ", ".join(f"`{t}::{x}`" for x in ts) + ")" for t, ts in g)


# ---- C1: confirmation readers (7)
for gi, g in enumerate(groups):
    nm = f"C1ConfRead{'ABCDEFG'[gi]}"
    role = "executor" if gi < 4 else "scout"
    ITEMS.append(item(nm, role, ["novelty"], f"""You are an independent second reader for R53-C1's CONFIRM leg (claims file, Claim 1 leg 3). Your tasks (never read by this lane; the v2 classifier puts the
named test(s) in P1): {glist(g)}.
For each task: (1) read the whole capture {LANE}/corpus/evidence/round52/graders/<task>/tests/test_outputs.py (and the sibling tests/test.sh) — NOT any label file, NOT the classifier
({LANE}/plans/round53_c1_classify.py) and NOT any output of seats whose names start `C1Label`, `C1Exec`, `C1Crit`, `C1Mut`; (2) fetch the task's own instruction at the pin:
`gh api -H 'Accept: application/vnd.github.raw' 'repos/harbor-framework/terminal-bench-2/contents/<task>/instruction.md?ref={PIN}'` (or curl the raw URL
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/<task>/instruction.md`) and say in one sentence what real work the instruction asks for; (3) decide
whether the named test would pass if the path(s) it names merely existed (touch/mkdir, arbitrary or empty content) per {W}/p1-spec.md — answer `confirmed: true` only if so, and
`confirmed: false` (with why) if you find any reachable content, command or value check the classifier missed; (4) pick `quote`: a verbatim fragment of >= 20 characters taken from
one or more consecutive source lines of the test function's own span (lines `lineno..end_lineno` of `{LANE}/corpus/evidence/round53/tests-index.json` for that id) — whitespace is
normalised by the counter; (5) state what the rest of the grader does check (other tests in the file) so the weakness is not overstated: a presence-only test beside a real content check is
a weakness of that test, not of the whole grader.
Deliver `{WAVE_DIR}/{nm}/confirmations-part.json`: a JSON list with one object per task `{{"task","test_id","quote","reader":"{nm}","confirmed":true|false,"line":<first line of the quote>,"why":"<=30 words"}}`
(when a task has two or three P1 tests, confirm the single clearest one; list the others in your report). Your report `{WAVE_DIR}/{nm}.md` MUST name every task id of your group
as a whole token (the counter checks it) and must not be copied from another seat. Your reader name is exactly `{nm}`."""))

# ---- C1: prior-art pricing (7)
for gi, g in enumerate(groups):
    nm = f"C1PriorArt{'ABCDEFG'[gi]}"
    role = "scout"
    ITEMS.append(item(nm, role, ["novelty", "coverage"], f"""Prior-art pricing for R53-C1's PRIOR-ART leg (claims file, Claim 1 leg 4; counter `leg_prior_art` in {LANE}/plans/round53_c1_triage.py — read it first).
Your tasks: {glist(g)} (these are CANDIDATES; the L1 keeps only the rows of tasks that readers confirm).
For each task decide, from archived public primaries, whether a presence-only (artefact-existence) weakness of THAT task's grader is already documented: look in the issue and pull-request
trackers of `harbor-framework/terminal-bench-2` and `harbor-framework/terminal-bench-2-1` (use `gh api` — the host is authenticated; search API budget is 30/min shared with six other seats, so
space queries; never print the token) and, if useful, the TB2.1 release notes. Rows: (a) `phenomenon-known`: an archive that names the task id or the test name and describes an existence-only or let-anything-pass
verifier; the quote (8-25 words, verbatim from the archive) must itself name the task id or a test name; (b) `phenomenon-new`: no tracker item names that weakness for this task — then the row's
own archive is a general primary on the phenomenon that does NOT name the task or its tests (for example the TB2.1 notice, a PR body about tests that let any solution pass, or a paper) with an 8-25-word
quote, and the row carries `sweep`: >= 2 DISTINCT archived search results (one per tracker repo, e.g. `gh api 'search/issues?q=repo:harbor-framework/terminal-bench-2+<task>'` and the same for -2-1, plus a
code-search or title search if available) whose BODY does not contain the task id or its test names. Every archive file's FIRST line must be `SOURCE-URL: <public url>` (for a search result use the API URL you called; for an
issue use its html URL), followed by the fetched bytes verbatim; the row's `url` must equal the first archive's header URL. Save archives under `{WAVE_DIR}/{nm}/fetched/` with a `SHA256SUMS`. A task for which you cannot establish either
verdict gets `unclear` in your report and NO row. Deliver `{WAVE_DIR}/{nm}/prior-art-part.json`: a JSON list of rows
`{{"task","verdict","url","fetched":"<path of the archive relative to the lane>","fetched_sha256","quote","sweep":[{{"file":"<path relative to the lane>","file_sha256"}},…]}}` (omit `sweep` for known rows; paths are your seat directory paths — the L1 rewrites them
into corpus/evidence/round53/fetched/). Also list every URL you opened and every rejected candidate with the reason. Do not read the label files or classifier output."""))

# ---- C1: touch-run executors (3)
tgroups = [cand[i::3] for i in range(3)]
for gi, g in enumerate(tgroups):
    nm = f"C1ExecTouch{'ABC'[gi]}"
    ITEMS.append(item(nm, "executor", ["novelty", "operability"], f"""Mechanical check of presence-only on the real bytes. For each of these never-read tasks: {glist(g)} — build the smallest stub world in which ONLY the
paths the named test(s) assert on exist as empty files / empty directories (create the absolute paths the test names under a bubblewrap sandbox: `bwrap --unshare-net --ro-bind / / --dev /dev --tmpfs /app --tmpfs /tests …` or a
mount-namespace of your choice; some tests name other roots such as /logs or /workspace — read the test), copy the captured test file from {LANE}/corpus/evidence/round52/graders/<task>/tests/test_outputs.py into the sandbox, and run exactly
that one test with pytest (`uv run --no-project --with pytest python -m pytest <file>::<test> -q -p no:cacheprovider`; add `--with` for any import the file needs at module level — numpy, requests… — and say so; do not
run the agent's task, do not fetch task images). Record per task: the stub paths you created, the command, the pytest outcome (`passed` | `failed` | `blocked: <why>`), and — for context only — the outcome of the other tests in the file under the same stub world.
`passed` means the test passes on empty artefacts: the mechanical confirmation of its presence-only status; `failed` is evidence AGAINST the classifier and the oracle — report it with the failing assertion line. Deliver `{WAVE_DIR}/{nm}/touch-run.json`
(`[{{"task","test_id","stub_paths","cmd","outcome","detail"}}]`) and the table in your report. Do not read label files or classifier output. Scratch only under {SCRATCH}/{nm}/."""))

# ---- C1: blind re-labelers (4)
for k in range(1, 5):
    nm = f"C1RelabelRev{k}"
    ITEMS.append(item(nm, "reviewer", ["novelty", "calibration"], f"""Blind re-label seat {k} of 4, a third-party check of the oracle. Read ONLY {W}/p1-spec.md (the definition) and your shard {W}/relabel/shard-R{k}.json (20 test ids with absolute file path and line span;
a mix the L1 chose — you are not told which are likely Y or N) and the capture files they point to (read each whole file and the same-task sibling captures such as tests/test.sh). For every id decide Y / N / U exactly as the spec says (touch-sufficient or not, helpers and fixtures reached, no assertion = N).
Write `{WAVE_DIR}/{nm}/labels.json`: `{{"seat":"{nm}","labels":{{"<id>":{{"label":"Y|N|U","why":"<=20 words"}}}}}}` covering the shard exactly. You MUST NOT open any file under {LANE}/.ufo/waves/round-53/w1/ (label seats and classifier seats), {LANE}/plans/round53_c1_classify.py, {LANE}/plans/round53-c1-freeze.json, or run the counter; you write no classifier. Report: counts, the ids you found hardest and the exact clause of the spec that decided each."""))

# ---- C1: attacks
ITEMS.append(item("C1CritOracle", "critic", ["novelty", "calibration"], f"""Attack the ORACLE leg's result. At `{INT}` the counter prints `ORACLE tests=305 … decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52 … disagree=0 per_label_agree=1.000` and `ORACLE-CONTROL r52_classifier_disagree=23`.
A perfect 305/305 with sixteen independent labels and a classifier built from the same prose spec is a result that needs a reason. Investigate (read the eight label files {LANE}/.ufo/waves/round-53/w1/C1Label*/labels.json, their reports `C1Label*.md`,
the classifier, the spec, the adversarial cases {LANE}/.ufo/waves/round-53/w1/C1ExecAdvCases/cases.json): (1) how many of the 305 tests are "hard" (same-file helper reached, fixture, class method, listing, size/stat, import of a deliverable, teardown, write-then-exists) and how did the labels and the classifier treat each category;
(2) are there signs the labellers are not independent (identical `why` phrasing across seats, identical rare mistakes, sibling-directory reads claimed or visible); (3) which tests would flip under the second reading of the spec's ambiguous clauses (the 47 `ambiguous.json` patterns that occur in the population) and what would `disagree` be then;
(4) a forged oracle: build labels from the round-52 classifier's output (scratch clone, honest freeze/commit order) and show what the counter prints; (5) what claim the oracle can and cannot support, in one paragraph. Deliver numbers, commands and a verdict (`oracle supports / does not support the claim "the v2 classifier reproduces independent labels on the 305 tests"`), never edit the lane."""))

ITEMS.append(item("C1CritConfirmSemantics", "critic", ["novelty"], f"""Attack the CONFIRM and PRIOR-ART legs as semantics, not as parsers (the parsers were attacked in wave 1 and rewritten under A1). Read {LANE}/plans/round53_c1_triage.py `leg_confirm`, `candidates`, `leg_prior_art`, the 28 candidate
tasks in {W}/claims/c1-candidates.txt, the captures of their P1 tests, and the knowledge entry the lane landed in round 52 ({LANE}/corpus/knowledge/tb2-grader-vacuity-triage.md). Questions: (1) for each of the 28 candidates, is the P1 test a weakness of the GRADER or only
a presence precondition that a later test in the same file checks properly (so confirming it would overstate the finding)? classify each of the 28 as `grader-weak`, `precondition-only` or `unclear` with the quote that decides it; (2) does the counter's `confirmed is True` + quote-in-span rule let a precondition-only test count as a confirmation, and what one sentence must the knowledge entry carry so the claim is not overstated; (3) can `phenomenon-new` be produced by a lazy sweep (search term misspelled, wrong repo), and what check would catch it;
(4) is 'never-read' honest for tasks named in the round-52 critic's receipt `.ufo/waves/round-52/w2/W2CritC1Reach/receipts/live_tests.json` or in other wave directories. Deliver the 28-row table, the three sharpest defects and the smallest repair for each. Do not edit the lane."""))

ITEMS.append(item("C1Crit2Counter", "critic", ["novelty", "calibration"], f"""Re-attack the AMENDED C1 counter ({LANE}/plans/round53_c1_triage.py at `{INT}`, amendment A1 in the claims file). Wave 1's attacks (reports `.ufo/waves/round-53/w1/C1CritCounterReach.md`, `C1MutCounter.md`, `C1SentinelScreen.md`) are listed in A1 as closed;
verify each closure with a fixture on a scratch clone (`git clone -q --shared`, verify the top-level) and then find NEW routes to `PREDICATE R53-C1 pass` without the claimed work: the freeze/ordering leg (rebase/amend history, a second file added to the freeze commit, a tag, a replace ref, a shallow clone hiding history — the counter reads `git log -- path`), the label merge (shards mutated and re-pinned together, a label seat file whose `seat` field matches but whose directory is another seat's), `names_task`/header handling,
`inside()` path rules (symlinked directories above the file, case-folding), `candidates` with an unavailable base tip, the control leg when `disagree` is 0 (`dis52 >= 2*max(dis,1)` and >= 10), the `per_label_agree` and balance legs. Each route: construction, counter output, whether a leg holds, smallest fix. Do not edit the counter."""))

ITEMS.append(item("C2Crit2Counter", "critic", ["calibration", "operability"], f"""Re-attack the AMENDED C2 counter ({LANE}/plans/round53_c2_tipstate.py at `{INT}`, amendment A1). Verify each wave-1 closure (reports `.ufo/waves/round-53/w1/C2CritLedgerReach.md`, `C2MutCounter.md`, `C1SentinelScreen.md` M1-M3) with a fixture on a scratch clone, then find NEW routes: a row whose script is a thin wrapper that
always exits 0 while the registry cell advertises a real gate (the counter cannot tell — measure which rows of the REAL ledger are gates that cannot fail: run each green row's script with its main check mutated in a scratch copy if cheap, or read the script, and list the rows whose green declaration is vacuous), `timeout_s` abuse, evidence fragments that are common to green and red output of the same row, a red row whose reason is
untrue (read the 10 longest reasons in `plans/round53-tipstate.json` and check them against the script), a worker clone sharing the object store (`git clone --shared`) and a row that runs `git gc`/`git prune`, `uv run` rows reaching the network, argv entries that are paths outside the clone. Deliver constructions, outputs and fixes; never edit the counter."""))

ITEMS.append(item("C1MutClassifier", "mutation-tester", ["novelty", "calibration"], f"""Mutation-test the ORACLE: how many single-rule mutants of the classifier does the committed label set kill? Scratch copy of the lane ({SCRATCH}/C1MutClassifier/lane; verify the top-level). The classifier is {LANE}/plans/round53_c1_classify.py (read it; ~1.5k lines); the oracle is the eight
{LANE}/.ufo/waves/round-53/w1/C1Label*/labels.json merged over the pinned shards exactly as `merge_labels` in plans/round53_c1_triage.py does (import that function; the counter's FREEZE leg would reject a modified classifier, so score each mutant with your own harness: mutated `classify_source` over the 305 ids vs the merged decided labels).
Produce >= 40 mutants, each ONE edit that removes or flips a rule (an allowed existence method dropped, a violation class ignored, helper inlining off, fixture reach off, class-method reach off, a count comparison tolerated, `os.access` mode check dropped, write-then-exists flipped, depth guard 40 -> 1, cycle guard off …). A mutant is KILLED iff its P1/P0 vector differs from the oracle on >= 1 decided test; a SURVIVOR names a rule the 305-test population + labels do not exercise. Include the null mutant. For each survivor say whether it is equivalent on the
population, or a rule only the adversarial cases (C1ExecAdvCases/cases.json) exercise (run those too and report which survivors the adversarial set kills). Report kill ratio and the table; the survivors are the honest statement of what the oracle does not test."""))

ITEMS.append(item("C1MutCounter2", "mutation-tester", ["novelty", "calibration"], f"""Re-run the wave-1 mutation battery against the AMENDED C1 counter. The wave-1 driver is {LANE}/.ufo/waves/round-53/w1/C1MutCounter/mutate.py (read it and `mutants.md`): its mutants are exact-string replacements on the pre-A1 file, so
adapt every pattern to {LANE}/plans/round53_c1_triage.py at `{INT}` (scratch copy; never edit the lane) and add mutants for the clauses A1 introduced (freeze single-commit, label pins, strictly-later label commits, shard coverage, per_label_agree, balance, R52_AUDIT_SHA, `inside()`, header URL equality, distinct sweep digests, whole-token report naming, BASE-TIP fail-closed, `names_task` header strip). >= 60 mutants incl. a null mutant.
Killed iff `--selftest` exit code or its `cases=… failures=…` line changes. Report the table, the survivors split into equivalent vs missing-fixture, and a diff that adds the missing fixtures to `selftest()` (a proposal; the L1 decides)."""))

ITEMS.append(item("C2MutCounter2", "mutation-tester", ["calibration", "operability"], f"""Re-run the wave-1 mutation battery against the AMENDED C2 counter. Driver: {LANE}/.ufo/waves/round-53/w1/C2MutCounter/mutate_c2.py and `mutation-table.md` (read them); adapt every pattern to {LANE}/plans/round53_c2_tipstate.py at `{INT}`
(scratch copy; never edit the lane) and add mutants for what A1 introduced (heading regex, `row_set_pinned` digest and EXTRA_NAMES, `argv_ok` interpreter/uv rules, SHELLS, `kind_ok`, duplicate-key hook, `SECRET_ENV` pattern, `reset` check=True, `lane_rev_equal`, `clean`, `headings == 1`, `bad_table_lines`, `static_ok` terms, `ok` conjunction). >= 60 mutants incl. a null mutant.
Killed iff `--selftest` exit code or its `cases=… failures=…` line changes. Report the table, survivors split into equivalent vs missing-fixture, and a diff proposing the missing fixtures."""))

# ---- C2: reruns and row review
ITEMS.append(item("C2ExecRerunA", "executor", ["calibration", "operability"], f"""Independent full run of the C2 counter. `S={SCRATCH}/C2ExecRerunA; git clone -q --shared {LANE} $S/lane; git -C $S/lane rev-parse --show-toplevel` (must be `$S/lane`), then check `git -C $S/lane rev-parse HEAD` equals `{INT}` (if the lane has moved on, check out nothing: report both hashes and run at the lane's current HEAD).
Run `python3 plans/round53_c2_tipstate.py --lane . --source $S/lane --work $S/work --jobs 4 --timeout 900` (about 15-25 minutes; this is why the call is long — run it detached with `nohup setsid … > $S/out.txt 2>&1 &` and read the file, do not poll in a tight loop). Report the full output, exit code, wall time, and for every `MISMATCH`/`EVIDENCE-MISSING`/`TIMEOUT` line the row's output (run the argv alone to see why). Do not edit the ledger."""))

ITEMS.append(item("C2ExecRerunB", "executor", ["calibration", "operability"], f"""Second independent full run of the C2 counter, with a different job count and from a different clone, to check determinism: `S={SCRATCH}/C2ExecRerunB; git clone -q --shared {LANE} $S/lane` (verify the top-level and HEAD = `{INT}` as in a sibling seat),
`python3 plans/round53_c2_tipstate.py --lane . --source $S/lane --work $S/work --jobs 2 --timeout 900` detached (`nohup setsid … > $S/out.txt 2>&1 &`; about 25-40 minutes at two jobs). Report the output, exit code, wall time and, for every row whose observed exit differs from the ledger or from what your sibling `C2ExecRerunA` reports
(read `{WAVE_DIR}/C2ExecRerunA.md` once it exists), the reason. Then pick the three slowest rows (the counter prints `sec=` only for mismatches: time them yourself with `/usr/bin/time -v`) and report their wall time under load. Do not edit the ledger."""))

LEDGER_NAMES = json.loads(Path(f"{W}/c2-row-names.json").read_text()) + ["round53-c1", "round53-c2"]
LEDGER_NAMES.sort()
rgroups = [LEDGER_NAMES[i::3] for i in range(3)]
for gi, grp in enumerate(rgroups):
    nm = f"C2RevRows{'ABC'[gi]}"
    ITEMS.append(item(nm, "reviewer", ["calibration"], f"""Review the truth of these {len(grp)} ledger entries of {LANE}/plans/round53-tipstate.json (rows: {', '.join(grp)}). For each row: (1) read the registry row in {LANE}/SKILL.md and the ledger entry; check the argv is the row's real entry (not a weaker one) and say whether the ledger's `kind` is honest;
(2) re-execute the argv yourself in a CLEAN shared clone (`git clone -q --shared {LANE} {SCRATCH}/{nm}/lane`, verify the top-level; run from its root; `TMPDIR` under {SCRATCH}/{nm}/; your own driver, NOT the counter) and compare the exit code; (3) for every red row read the `reason` (is it TRUE of the script and its output? is the cause as stated?), and the `evidence` fragment (is it a line of the observed output?);
(4) for every green row say in one line whether the instrument can fail at all (does the script have a path to a non-zero exit for the condition the row's verdict map names? — read it; a green row that cannot fail is declared truthfully but is weak evidence, report it). Report a table (row, observed exit, ledger exit, agree y/n, reason true y/n/na, can-fail y/n/unknown) and every disagreement with the exact output fragment. Do not edit the ledger."""))

ITEMS.append(item("C1ExecControls", "executor", ["novelty", "calibration"], f"""Run the frozen real-tree controls of the round. `S={SCRATCH}/C1ExecControls; mkdir -p $S; git clone -q --shared {LANE} $S/src; git -C $S/src rev-parse --show-toplevel HEAD` (top-level must be `$S/src`; HEAD should be `{INT}` or a descendant: report which).
Read {W}/controls.py first, then `python3 {W}/controls.py --src $S/src --out {WAVE_DIR}/C1ExecControls/receipts --scratch $S/work --which all` (the C2 half runs a few real rows through the counter with `--only`; budget ~10 minutes; run detached with `nohup setsid` if it exceeds a minute). The script is the L1's; if a control errors for a script bug (not for the counter behaving), report the traceback, fix a COPY of the script in your seat directory and rerun that copy — do not edit {W}/controls.py.
Report each control line (`CONTROL <label> exit=… marker=… -> ok|FAIL`), the baseline exit codes, and any control that does not fail the counter on its named leg (that is a defect in the counter or the control: say which, with the output). Receipts must be the files `c1-control-*.txt`/`c2-control-*.txt`/`c1-baseline.txt` written by the script."""))

# ---- sources: scribes and reviewers
ITEMS.append(item("C1ScribeSourcesA", "scribe", ["coverage", "novelty"], f"""Finalise registry rows for SOURCES.md from the wave-1 scouts' drafts, group A: {W}/w1/C1ScoutSrcTesting.md and {W}/w1/C1ScoutSrcAudit.md (rows and archives under their `fetched/` dirs).
CORPUS.md rule 1 binds: re-open EVERY source yourself today (2026-10-28), not the archive: fetch the live URL, confirm HTTP 200 and that your <=25-word quote is located in what you fetched; record the access date, the location (line/section) and the sha256 of your fetch in your report's table.
Keep only sources that bear on tests that pass if an artefact merely exists (or on grader/test-suite strength for agent benchmarks) — reject the rest as `rejected` rows with `REJECTED: <reason>; flip: <condition>`. Tier per contract v1 (A primary for its scope; B strong secondary; C lead only; `community` never A). Write `{WAVE_DIR}/C1ScribeSourcesA/rows.md`: one row per kept/rejected source in the exact 11-column schema (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`),
ids `T01…` (the L1 renumbers from S194 by document), no `|` inside any cell, `opened` 2026-10-28, `recheck` ISO date or `90d`/`180d`, `used-by` `—`, status `queued`/`rejected`. Also `{WAVE_DIR}/C1ScribeSourcesA/gate.md`: for every row the URL, access date, the located <=25-word quote with its location. Read {LANE}/corpus/SOURCES.md first so no row duplicates an existing URL (the census flags duplicate URLs across scopes as W04)."""))

ITEMS.append(item("C1ScribeSourcesB", "scribe", ["coverage", "novelty"], f"""Finalise registry rows for SOURCES.md from the wave-1 scouts' drafts, group B: {W}/w1/C1ScoutSrcBench.md and {W}/w1/C1ScoutSrcTB2.md (rows and archives under their `fetched/` dirs; note the TB2 scout's rows are tracker items S941-S946 drafted as a table — turn the ones that name a TB2/TB2.1 task grader into registry rows, tier B for tracker items).
Same procedure as the sibling seat (`C1ScribeSourcesA`): re-open every source live today and locate your <=25-word quote in what you fetched; keep only sources bearing on existence-only / let-anything-pass tests for agent benchmarks or on the specific tasks in {W}/claims/c1-candidates.txt; rejected rows with `REJECTED: <reason>; flip: <condition>`;
exact 11-column schema; temporary ids `U01…` (the L1 renumbers); no `|` in any cell; deliver `{WAVE_DIR}/C1ScribeSourcesB/rows.md` and `{WAVE_DIR}/C1ScribeSourcesB/gate.md` (URL, access date, located quote, location, sha256 of your fetch). Read {LANE}/corpus/SOURCES.md first; no duplicate URLs."""))

for k, who in ((1, "A"), (2, "B")):
    ITEMS.append(item(f"C1RevSources{who}", "reviewer", ["coverage", "calibration"], f"""Attack the new SOURCES rows (non-author spot check, in advance of the closure's). Rows come from `C1ScribeSources{who}`'s `{WAVE_DIR}/C1ScribeSources{who}/rows.md` and `gate.md` (they exist when your sibling scribe has finished; if not yet, read the wave-1 scout drafts
{W}/w1/C1ScoutSrc*.md for the rows you will meet and come back — your own work may begin with the existing registry {LANE}/corpus/SOURCES.md rows S100, S179-S193, whose conventions the new rows must follow). For EVERY row: open the live URL yourself, locate the quote verbatim (or say it is absent: fabrication class), check the tier is scoped and not inflated (`community` never A; a PR or issue is B at best; an open PR is mutable),
the anchor is exact (section/line + revision/date), `teaches` is a grounded learner benefit, status/recheck/used-by conform, no `|` in cells, no duplicate URL with the registry (census W04). Report a table (row, opened ok y/n, quote found y/n, tier ok y/n, defect). Also run `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <a scratch copy of SOURCES.md with the new rows appended to the Registry table under renumbered S-ids>` and paste its output and exit code. Never edit the lane."""))

# ---- scribes: entry, lesson, scorecard/log, quality
FACTS = f"{W}/facts.md"
ITEMS.append(item("C1ScribeEntry", "scribe", ["novelty", "coverage"], f"""Draft the round-53 knowledge entry `corpus/knowledge/tb2-presence-only-triage-v2.md` as `{WAVE_DIR}/C1ScribeEntry/entry.md` (shape of {LANE}/corpus/knowledge/tb2-grader-vacuity-triage.md: first lines `source:`, `verified-at:`, `recheck:`; then the finding).
Read {FACTS} (numbers and pointers are there; every figure you write must appear there or be derived by a command you paste with its output), the round-52 entry, the claims file and the wave-1 reports. The entry must state, with a located pointer for each: what the instrument now is (AST classifier + blind labels + pins), what the oracle measured and what it cannot support, the 28 never-read candidates and how many were confirmed (use `[pending: confirmations]` where facts.md says pending — the L1 fills it), the prior-art verdicts (pending), the limits (a presence-only test beside a real content check is a weakness of that test; labellers are LLM seats sharing one written spec),
and a `## Re-run` section (commands). `source:` cites SOURCES rows by the placeholder ids `T01…`/`U01…` the source scribes use (the L1 maps them to S-ids by document). No prose claim without a pointer; counts carry their command."""))

ITEMS.append(item("R53ScribeLesson", "scribe", ["calibration"], f"""Draft `corpus/lessons/round-53.md` as `{WAVE_DIR}/R53ScribeLesson/lesson.md` following {LANE}/corpus/lessons/round-52.md (sections `## Gate`, `## Mistakes`, `## Limits`, plus `## Assimilation`: none). Read {FACTS}, the round-52 lesson and verifier spot-check, wave-1 reports `R53MistakeSweep.md` and the five attack reports (C1CritCounterReach, C1MutCounter, C1SentinelScreen, C2CritLedgerReach, C2MutCounter), `C2ExecRows*.md`.
`## Mistakes` rows (class · evidence pointer · captured-by · fix; a fix counts only once shown able to fail — cite the committed red-before output): at least `counter-reachable-without-the-work` (repaired by A1: cite `.ufo/waves/round-53/claims/c1-selftest.txt` and `c2-selftest.txt` forged cases), `rule-unit-leak` (the AST classifier + the adversarial set), `false-registry-cell`/`stale-registry-claims` (the C2 ledger found N rows red at the base tip: facts.md has the count; the unindexed knowledge file `fixture-honest-geometry.md`, repaired in the lane), `instrument-attacked-before-data` (wave 1 attacks landed on frozen counters: this is a capture, not a miss), and any further class `R53MistakeSweep` names with a resolvable pointer. `## Gate`: the SOURCES decisions are the source scribes' (placeholder ids); you leave a table skeleton with the columns id · verdict · URL · located quote · location and fill what is in their `gate.md` files if they exist. Every pointer must resolve — paste the `ls`/`grep` that proves it."""))

ITEMS.append(item("R53ScribeScoreLog", "scribe", ["calibration", "operability"], f"""Draft, from {FACTS} and the committed receipts, `{WAVE_DIR}/R53ScribeScoreLog/scorecard-section.md` (a `## Round 53` section for SCORECARD.md in the shape of the round-52 section: claim table with the frozen counting commands, before/after, verdicts, axis state carried, capabilities table additions only for capabilities that RAN this round with a pointer, `### Planned (round 54)`), `{WAVE_DIR}/R53ScribeScoreLog/log-entry.md` (a LOG.md entry in the shape of the round-52 entry: motivating evidence, outcome, evidence pointers) and `{WAVE_DIR}/R53ScribeScoreLog/readme-rows.md` (the corpus/README.md index row for the new knowledge entry and bullets for the round-53 receipts, shape of the existing rows).
Rules: no verdict the facts do not support — leave `[pending: <what>]` for anything the L1 has not measured (confirmations, prior art, C2 final run, controls); coverage stays 7 (L0 questions `kengaku | round-25`, `round-33`, `round-51` unanswered) and is not claimed; do not set any score change before the facts file says the claim verified. Every number: command + output or a pointer."""))

ITEMS.append(item("R53ScribeQuality", "scribe", ["calibration", "adjacency"], f"""Draft `{WAVE_DIR}/R53ScribeQuality/q43.md`: the QUALITY.md criterion Q43 (the same shape as Q42 at the end of {LANE}/corpus/QUALITY.md; it must say what this round's two counters did to meet Q42 (a)/(b)/(c), what wave 1's attacks showed was still reachable and how A1 closed it, and the limits: independence of labellers is a protocol property, a green ledger row can be a gate that cannot fail, never-read is not never-examined). Read {FACTS}, the claims file amendments and the wave-1 attack reports.
Also `{WAVE_DIR}/R53ScribeQuality/skill-notes.md`: the lines to add to SKILL.md (a short `## Presence-only grader triage` decision table and an entry in the error-pattern list: classifier-vs-oracle, forged-complete controls, ledger tip-state) — cite committed paths; do not invent commands. And `{WAVE_DIR}/R53ScribeQuality/province-note.md`: whether PROVINCE.md needs any change (surfaces added: classifier, labels, ledger) or says nothing changes, with the grep that shows it; and the fix for the PROVINCE SF14 row that the registry probe flags (`python3 plans/round51_surfaces.py --lane .` → `NUMBER-DRIFT SF14 row claims 171, probe says SOURCES rows=…`): print the exact row line and the exact replacement the L1 should apply once the final SOURCES row count is known (give it as a template with `<N>`)."""))

assert len(ITEMS) == len({i['name'] for i in ITEMS})
spec = {
    "wave": "kengaku-r53-w2",
    "milestone": "kengaku round 53 wave 2 (falsify+confirm): confirm/price never-read presence-only tasks, re-label and mutate the oracle, re-attack both amended counters, re-run the tip-state ledger, finalise sources, draft entry/lesson/log",
    "reportDir": ".ufo/waves/round-53/w2",
    "maxLanes": len(ITEMS),
    "axes": ["novelty", "calibration"],
    "context": CONTEXT,
    "items": ITEMS,
}
out = Path(f"{W}/w2-spec.json")
out.write_text(json.dumps(spec, indent=1))
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print(f"wrote {out} items={len(ITEMS)}", roles)
attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "sentinel"))
print(f"attack seats (incl. 4 relabel reviewers)={attack}/{len(ITEMS)}")
