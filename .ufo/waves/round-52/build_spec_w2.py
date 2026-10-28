#!/usr/bin/env python3
"""Build the kengaku round-52 wave-2 (falsify) swarm spec.

Wave 2 attacks what wave 1 produced.  Every item names the wave-1 artefact it attacks.
Run from the lane root; writes .ufo/waves/round-52/w2-spec.json.
"""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
WAVE_DIR = f"{LANE}/.ufo/waves/round-52/w2"
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
kengaku round 52 (hyaku run 11), WAVE 2 of 2 (falsify), lane repo {LANE}.
Wave 1 (build, 35 seats) has returned; its outputs are in the lane tree and in
`{LANE}/.ufo/waves/round-52/w1/`.  This wave ATTACKS what wave 1 produced: every seat's item
names the artefact it attacks and what would make the attack land.

The round's two frozen claims live at {LANE}/plans/round-52-claims.md — READ IT IN FULL FIRST,
including **Amendment A1** (per-test classification, disclosed, dated before the scored
after-run).  The frozen counters are `plans/round52_c1_grader_audit.py` and
`plans/round52_c2_registry.py`.

- **R52-C1 (novelty 8->9)** — a whole-benchmark grader-vacuity triage for Terminal-Bench 2.0:
  frozen population `plans/round52-tasks.json` (89 tasks, 184 grader files at pin
  2fd12b88aafdd04a52c298e3940bcb189f9766d6); captures under
  `corpus/evidence/round52/graders/`; the counter must print `PREDICATE R52-C1 pass`.
- **R52-C2 (operability 8->9)** — every advertised verdict instrument has a truthful row in
  SKILL.md's *## Gate/probe registry*; the counter must print `PREDICATE R52-C2 pass`.

# Write scope — every seat
Work ONLY inside your own scratch dir `{SCRATCH}/w2-<your-seat-name>/` and your own wave report
file `{WAVE_DIR}/<your-seat-name>/report.md`. Put every artefact you produce under your scratch
dir; the L1 is the single integration owner and copies what it accepts into the lane tree.
NEVER edit the lane tree, the fleet repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`,
`templates/`, `scripts/`, `MANIFEST.json`, or `/home/vgpnk/Projects/shokunin/.scratch/`.
NEVER run `git commit`, `git add`, `git push`, `git stash`, `git checkout`, `git reset`,
`git pull`, or any mutating `jj` command anywhere — the L1 commits through the lane helper only.
If your attack needs to modify an artefact, COPY it into your scratch dir and mutate the copy.
Never message agent://all; message only the seats you are told to address, by id.

# Scratch discipline (operator directive 2026-10-25)
Every clone, work tree, fixture and temp file of this seat lives under
`{SCRATCH}/w2-<your-seat-name>/` (NVMe). Create it with `mkdir -p` and pass it explicitly
(`TMPDIR=...`, `--work`); never rely on an inherited TMPDIR; never write to /tmp except files
under 50 MB. Remove your scratch dir before you yield, after copying any receipt you want kept
into your wave report dir. If you see ENOSPC, report the free space you saw and stop.

# Tooling
You and every seat may install or upgrade tools that help the task — read
/home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record
tool/version/channel/reason in your report). **pacman guard: all pacman transactions are PAUSED
host-wide** — install via `uv tool` / `npx` / an official binary in `~/.local/bin`, or file an L0
question. Never `pacman -Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host service.

# Report contract (every seat)
Write your report to `{WAVE_DIR}/<your-seat-name>/report.md` — that path is absolute; if a tool
renders a relative `Report:` trailer for you, it is relative to {LANE} — write it at
{LANE}/<that path>. Your report must carry: what you attacked, the exact commands you ran, the
measured numbers, the files you produced (absolute paths), and whether your attack landed or
failed to land. A seat that finds nothing says what it searched and reports the negative; a seat
that cannot finish says what it could not do and why. Never fabricate a number, a quote or a URL.
"""

def item(name, role, axes, body):
    return {
        "name": name,
        "role": role,
        "axes": axes,
        "item": GODSPEED + f"\n\n# Target\nkengaku round 52 wave-2 seat {name} ({role}).\n# Item\n{body}",
    }


ITEMS = []

# ------------------------------------------------------------------ executors (9)
ITEMS.append(item("W2ExecCounterRun", "executor", ["novelty"], f"""Run the two FROZEN counters against the lane tree as it stands now and report the raw output:
`python3 {LANE}/plans/round52_c1_grader_audit.py --lane {LANE}` and
`python3 {LANE}/plans/round52_c2_registry.py --lane {LANE}` (plus both `--selftest`s). Do not
edit either counter. Report: both full outputs, both exit codes, and — line by line — which
predicate legs still fail and what artefact each failing leg needs."""))

ITEMS.append(item("W2ExecConfirmA", "executor", ["novelty"], f"""BE AN INDEPENDENT READER for R52-C1. Take the first FIVE tasks the C1 counter prints as
`CANDIDATE` (run `python3 {LANE}/plans/round52_c1_grader_audit.py --lane {LANE}` and read the
list). For each: open its captured grader bytes under
`{LANE}/corpus/evidence/round52/graders/`, find a test function whose ONLY assertion is the
presence of an artefact, and write a confirmation receipt as JSON:
`{{"task": "<id>", "test": "<test name>", "quote": "<the exact assert line, copied verbatim>",
"line": <line number in the captured file>, "reader": "W2ExecConfirmA", "confirmed": true}}`.
Write `{SCRATCH}/w2-W2ExecConfirmA/confirmations.json` (a JSON array), then copy that receipt to `{WAVE_DIR}/W2ExecConfirmA/confirmations.json` before you clean your scratch dir. If a candidate has NO such
test, do NOT write a confirmation for it — write your negative finding in the report instead, with
the located lines that show the test compares something. Report: the receipts written, the
candidates refused, and for every refusal the located line."""))

ITEMS.append(item("W2ExecConfirmB", "executor", ["novelty"], f"""BE AN INDEPENDENT READER for R52-C1, on the tasks the OTHER reader did not take.
Take the NEXT FIVE `CANDIDATE` tasks printed by `python3 {LANE}/plans/round52_c1_grader_audit.py --lane {LANE}`
(after the first five) and do exactly what the confirmation protocol says: open the captured
grader bytes under `{LANE}/corpus/evidence/round52/graders/`, locate a test function whose only
assertion is artefact presence, and write the receipt JSON
`{{"task", "test", "quote", "line", "reader": "W2ExecConfirmB", "confirmed": true}}` to
`{SCRATCH}/w2-W2ExecConfirmB/confirmations.json`. A candidate with no presence-only test gets no
receipt — report the negative with located lines. Report: receipts written, candidates refused
with their evidence."""))

ITEMS.append(item("W2ExecConfirmC", "executor", ["novelty"], f"""BE A THIRD INDEPENDENT READER for R52-C1, and cross-check the other two readers.
Take the NEXT FIVE `CANDIDATE` tasks after the first ten printed by
`python3 {LANE}/plans/round52_c1_grader_audit.py --lane {LANE}`, write receipts in the same JSON
shape to `{SCRATCH}/w2-W2ExecConfirmC/confirmations.json`, then copy that receipt to `{WAVE_DIR}/W2ExecConfirmC/confirmations.json` before you clean your scratch dir, and ALSO independently re-check every
receipt you can find from the other readers under `{SCRATCH}/w2-W2ExecConfirm*/confirmations.json`
(if present): for each, open the captured bytes and verify the quote is verbatim and the line
number is right. Report: your own receipts, and a table cross-checking every other reader's
receipt (task, quote verbatim yes/no, line correct yes/no)."""))

ITEMS.append(item("W2ExecCapturesVerify", "executor", ["novelty"], f"""Verify the capture set that landed under `{LANE}/corpus/evidence/round52/graders/`.
Re-fetch TEN deterministically chosen grader paths (every 19th path of the frozen population in
`{LANE}/plans/round52-tasks.json`) from the pin and compare sha256 with the committed bytes;
check the committed `SHA256SUMS` covers every file present and every file the population expects
(count both ways); check no committed file is an HTML/JSON error body, an empty file, or a
truncated response (report the byte length distribution and any file < 100 B). Write
`{SCRATCH}/w2-W2ExecCapturesVerify/capture-verification.json`. Report: the ten re-fetch digests,
the two-way count comparison, and any defective capture."""))

ITEMS.append(item("W2ExecRowsIntegrate", "executor", ["operability"], f"""Assemble the gate-registry rows for R52-C2 into ONE table. Read the rows wave 1 drafted
(each scribe's scratch dir `{SCRATCH}/C2ScribeRows*/rows.md`; if a seat's dir is missing, derive
the row yourself from the script) and the mechanical facts in
`{SCRATCH}/C2ExecRowFacts/facts.json` and the measured runs in `{SCRATCH}/C2ExecRowRuns/`.
Write `{SCRATCH}/w2-W2ExecRowsIntegrate/registry-rows.md` containing the 28 NEW rows in the
exact 8-column markdown format of SKILL.md's *## Gate/probe registry* table (name | kind | entry |
verdict map | self-test | pinned values | write scope | owner), in the order the counter prints
`MISSING`. Every cell must be non-empty and every claim true of the script — if a row would have
to be untrue, write the row with an explicit `unverified:` prefix in the cell and report it.
Report: the merged file path, the number of rows, and every row you marked unverified."""))

ITEMS.append(item("W2ExecLabelsMerge", "executor", ["novelty"], f"""Merge wave 1's blind labels into the file the C1 counter reads. Find the blind label set
wave 1 produced under `{SCRATCH}/C1ExecBlindLabels/labels.json` (and, if present,
`{SCRATCH}/C1ScoutAgreement/`); if the blind label file is missing, say so and do NOT invent
labels. Write `{SCRATCH}/w2-W2ExecLabelsMerge/labels.json` in the shape the counter reads:
`{{"labels": [{{"task": ..., "class": ..., "why": ...}}]}}` where `class` is the FILE-level class
the frozen rules define (V1/V2/V3/V4/V0) — the counter compares the blind label with the
file-level class. Report: the number of labels, their class histogram, and whether every label
came from a blind seat (quote the source path)."""))

ITEMS.append(item("W2ExecPriorArtCheck", "executor", ["novelty"], f"""Audit the prior-art file that landed at
`{LANE}/corpus/evidence/round52/prior-art.md` (if it exists): re-fetch EVERY URL it cites
(checklist: HTTP status, the exact quoted words present at the cited anchor, the fetch date).
Write `{SCRATCH}/w2-W2ExecPriorArtCheck/prior-art-audit.json`. If the file does not exist, fetch
the sources yourself: at least FIVE public primaries that bear on (a) whole-benchmark grader
triage instrumentation and (b) published audits of Terminal-Bench 2.0 task graders, and write a
`prior-art.md` draft into your scratch dir with a per-finding verdict line of the form
`FINDING <task-id> verdict=phenomenon-new|phenomenon-known|unclear because <evidence>`. Report:
the audit table (url, status, quote present yes/no) and your overall novelty verdict."""))

ITEMS.append(item("W2ExecEntryDraft", "executor", ["depth"], f"""Draft the knowledge entry that the round's C1 claim lands:
`{LANE}/corpus/knowledge/tb2-grader-vacuity-triage.md`. Read the frozen claims file
(`plans/round-52-claims.md`, including Amendment A1), the C1 counter, the captures under
`{LANE}/corpus/evidence/round52/graders/`, the confirmations, and the prior-art file. The entry
must open with the three provenance lines the lane's format requires (`source:`, `verified-at:`,
`recheck:`) naming the S### rows it rests on, then state: the population, the instrument, the
per-test classes, the measured numbers (from the counter's own output — run it), the confirmed
findings with their located quotes, the prior-art verdict, and the LIMITS (file-level classes are
kept but misdescribe graders whose comparisons are in memory; a presence-only test is a weakness
of that test, not of the whole grader; the triage says nothing about task validity).
Write the draft to `{SCRATCH}/w2-W2ExecEntryDraft/entry.md`. Do NOT create the file in the lane
tree — the L1 integrates. Report: the draft path and the numbers you quoted."""))

ITEMS.append(item("W2ExecLessonDraft", "executor", ["calibration"], f"""Draft the round lesson `{LANE}/corpus/lessons/round-52.md` for the L1 to integrate.
Read `{LANE}/plans/round-52-claims.md` (incl. Amendment A1), the A1 observation receipt
`{LANE}/.ufo/waves/round-52/claims/a1-observation.txt`, the round-51 verifier spot-check
`{LANE}/corpus/lessons/round-51-verifier-spotcheck.md` and the round-51 lesson
`{LANE}/corpus/lessons/round-51.md`. Write the file with the sections the lane uses: a header
naming the round, the two claims and the freeze commits; `## Gate` (candidates opened this round
with verdict and reason/flip, the census before/after, and at least one ADMIT and one REJECT);
`## Mistakes` (one row per mined mistake: class · evidence pointer · captured-by · fix); and
`## Limits`. Mine at least these three mistakes, each with a pointer and a fix that is shown able
to fail: (1) the frozen file-level classification rule was falsified by a two-grader hand-check
AFTER the freeze and after dispatch (class: instrument-falsified-after-freeze; captured-by: none
— nothing tested a frozen rule against a sample of the population before the freeze; fix: the
counter's `--selftest` now covers the per-test rule and a rule-behaviour probe on a sample of
graders is part of the freeze checklist); (2) 28 advertised instruments had no registry row for
years (class: advertised-but-unregistered; captured-by: none — no counter compared the advertised
universe with the registry table; fix: `plans/round52_c2_registry.py`); (3) the round-51 LOG
entry says 63 of 64 seats wrote a report while the committed results show 64 (class:
number-drift; captured-by: the ledger's `CHECKS`/count legs; fix: an append-only LOG correction
line in this round). Write the draft to `{SCRATCH}/w2-W2ExecLessonDraft/lesson.md`. Report: the
draft path and the mistakes you mined."""))

# ------------------------------------------------------------------ scribes (4)
ITEMS.append(item("W2ScribeRowsCheck", "scribe", ["operability"], f"""Check the 28 new gate-registry rows for TRUTHFULNESS (not completeness — the counter
does completeness). For each row in `{SCRATCH}/w2-W2ExecRowsIntegrate/registry-rows.md` (or the
wave-1 scribe scratch dirs): open the named script and verify each factual claim in the row —
the entry command's flags exist, the verdict map's exit codes match the script's `return`/`sys.exit`
sites, the self-test spelling is accepted by the script, the pinned values exist in the tree, the
write scope names what the script actually writes. Write `{SCRATCH}/w2-W2ScribeRowsCheck/row-truth.json`
with one object per row: row name, verdict `true`/`false`/`unverifiable`, and the evidence.
Report: the count of true/false/unverifiable rows and, for every false row, the corrected cell
text."""))

ITEMS.append(item("W2ScribeSourcesRows", "scribe", ["novelty"], f"""Prepare the SOURCES rows this round appends. Read the contract in
`/home/vgpnk/Projects/shokunin/CORPUS.md` (section *SOURCES.md — where a shokunin learns*), the
registry `corpus/SOURCES.md` (11 visible columns per row; the census parser wants NF=13), and the
lesson's `## Gate` block requirement (URL, access date, ≤25-word located quote). Draft rows for
the sources opened this round: the Terminal-Bench 2.0 README at pin
2fd12b88aafdd04a52c298e3940bcb189f9766d6, the `bn-fit-modify` grader, the `pytorch-model-recovery`
grader, the `torch-tensor-parallelism` grader, and any prior-art primary the scout fetched.
For every row: exact URL, HTTP status, the quote (≤25 words) with its line number, the sha256 of
the fetched bytes, `opened` = 2026-10-28, a valid `recheck` (ISO date or `NNd`), `status` =
`mined`, and `used-by` naming exactly the entry that cites it (the new knowledge entry
`corpus/knowledge/tb2-grader-vacuity-triage.md`). Write
`{SCRATCH}/w2-W2ScribeSourcesRows/sources-rows.md` with the rows in registry-table form.
Report: the draft path, the ids you propose, and any row you refused and why."""))

ITEMS.append(item("W2ScribeGateBlock", "scribe", ["novelty"], f"""Write the `## Gate` block for `corpus/lessons/round-52.md`: a table of the candidates
this round OPENED, each with its verdict (ADMIT -> the S### row it becomes, with tier, kind and
the ≤25-word located quote and its line anchor) or REJECT (with the reason and the flip
condition). The candidates are the Terminal-Bench 2.0 README at the pin, the three grader files
above, the pin's tree listing, and the prior-art primaries. Write it to
`{SCRATCH}/w2-W2ScribeGateBlock/gate-block.md`. Report: the draft path and the number of admits
and rejects."""))

ITEMS.append(item("W2ScribeIndexRows", "scribe", ["coverage"], f"""Prepare the corpus-index rows for the round's new artefacts (the lane's index lives in
`{LANE}/corpus/README.md`): the new knowledge entry, the new lesson, the new evidence dir
`corpus/evidence/round52/`, the two new instruments `plans/round52_c1_grader_audit.py` and
`plans/round52_c2_registry.py`, and the new frozen population `plans/round52-tasks.json`. Write
the exact index rows (markdown table rows in the file's existing style) to
`{SCRATCH}/w2-W2ScribeIndexRows/index-rows.md`. Also report the `## Frontier` clause this round
advances: the open clause in `corpus/README.md` about auditing a benchmark's task specs, graders
and contamination separately. Report: the draft path and the frontier clause you advance."""))

# ------------------------------------------------------------------ scouts (3)
ITEMS.append(item("W2ScoutPriorArtFresh", "scout", ["novelty"], f"""Independently price the prior art (read-only): fetch at least FIVE public primaries
that bear on whole-benchmark grader triage and on published audits of Terminal-Bench 2.0 graders
(GitHub issue threads, maintainer statements, papers). For each: URL, HTTP status, a ≤25-word
located quote, and what it says about the claim's two halves (the instrument, the findings).
Write `{SCRATCH}/w2-W2ScoutPriorArtFresh/prior-art.md` with per-finding verdict lines
`FINDING <task-id> verdict=phenomenon-new|phenomenon-known|unclear because <evidence>`.
Report: the number of sources fetched with status 200, the per-finding verdicts, and your
overall verdict on instrument-level novelty."""))

ITEMS.append(item("W2ScoutVerifyQuotes", "scout", ["novelty"], f"""Verify every quote and anchor the round's new SOURCES rows will carry (read-only).
Open each source at its pinned URL, confirm the quoted words appear verbatim at the cited line,
and record the sha256 of the fetched bytes: the Terminal-Bench 2.0 README at pin
2fd12b88aafdd04a52c298e3940bcb189f9766d6 (the "Terminal-Bench is a popular benchmark ..." line),
`bn-fit-modify/tests/test_outputs.py` (the `bn_sample_path.exists()` assert),
`pytorch-model-recovery/tests/test_outputs.py` (the `hello_path.exists()` assert) and
`torch-tensor-parallelism/tests/test_outputs.py` (the `parallel_linear_path.exists()` assert).
Write `{SCRATCH}/w2-W2ScoutVerifyQuotes/quote-check.json`. Report: per source the line number,
the verbatim quote, the sha256, and whether the quote is ≤25 words."""))

ITEMS.append(item("W2ScoutLaneReadSet", "scout", ["calibration"], f"""Verify the counter's `lane_read_tasks()` set (read-only): it decides which tasks count as
NEW for the CONFIRMED leg. Read the 12 files `{LANE}/corpus/knowledge/tb2-*-grader.md` and the
counter's regex in `{LANE}/plans/round52_c1_grader_audit.py`; report which of the 89 task ids
the regex actually recovers, which hand-read tasks it MISSES (a task the lane read but the
counter thinks is new is a way to claim novelty twice), and the fix you would propose (without
editing the counter). Write `{SCRATCH}/w2-W2ScoutLaneReadSet/lane-read-set.json`. Report: the
recovered set, the missed set, and your proposed fix."""))

# ------------------------------------------------------------------ connectors (2)
ITEMS.append(item("W2ConnectSiblings2", "connector", ["adjacency"], f"""Re-run the sibling-overlap scan for the LANDED round (read-only): do the sibling lanes
(`/home/vgpnk/Projects/shokunin/*-shokunin`) own any part of what this round landed (a grader
triage instrument, a gate-registry standard, a presence-only-test finding)? Name the report-outs
this lane must record in PROVINCE.md and the contested scope in your report."""))

ITEMS.append(item("W2ConnectIndexBoth", "connector", ["coverage"], f"""Check the corpus index in BOTH directions after the round (read-only): every row of
`{LANE}/corpus/README.md` points at a file that exists, and every new file of this round has a
row. Report the missing rows and the dangling rows with file:line evidence."""))

# ------------------------------------------------------------------ reviewers (7)
ITEMS.append(item("W2RevCounterA1", "reviewer", ["novelty"], f"""Review Amendment A1 and the amended C1 counter (read-only): the amendment moved the
classification unit from the grader file to the grader's test functions. Verify the counter's
`classify_test()` against the amendment's frozen wording: is a presence-only test that also
compares something misclassified? is the split applied consistently (blocks, decorators,
parametrised tests, `if` guards)? Build fixtures in your scratch dir for: a test with an
`exists()` plus a comparison; a parametrised test; a test whose assert is inside an `if`; a
test with a helper call that does the comparison. Report: per case the expected class, the
observed class, and whether the amended rule holds or needs a wording fix (do not edit)."""))

ITEMS.append(item("W2RevClassifierImpl", "reviewer", ["novelty"], f"""Review the instrument as a measurement (read-only): does
`{LANE}/plans/round52_c1_grader_audit.py` measure what the claims file says it measures? Check
the capture-count leg (184 expected vs the population's real capture set), the digest leg
(`SHA256SUMS` — are the recorded digests compared against the CAPTURED bytes or trusted from
the file?), the classification leg, the CONFIRMED leg's two new hardening checks (candidate
membership, quote verbatim in the captured bytes) and the PRIOR-ART leg (≥3 distinct URLs —
distinct how?). Name every place where a wrong input could pass. Report: per-leg verdict
(sound | vacuous) with the exact input that would pass it."""))

ITEMS.append(item("W2RevConfirmations", "reviewer", ["novelty"], f"""Independently re-read the C1 confirmations (read-only): for every receipt in the
confirmation files wave 2 produced under `{SCRATCH}/w2-W2ExecConfirm*/confirmations.json`, open
the captured grader bytes under `{LANE}/corpus/evidence/round52/graders/` and verify: the task is
a vacuity candidate, the named test exists, the quote is verbatim at the cited line, and the test
really asserts only artefact presence. Write
`{SCRATCH}/w2-W2RevConfirmations/confirmations-review.json` (one verdict per receipt, with the
located evidence). Report: the count of confirmed / refuted / unverifiable receipts, and every
refutation with its located line."""))

ITEMS.append(item("W2RevRowsA", "reviewer", ["operability"], f"""Review the first half of the 28 new registry rows (read-only): for each row in
`{SCRATCH}/w2-W2ExecRowsIntegrate/registry-rows.md` (or the wave-1 scribe scratch dirs), open the
named script and check the row against it: does the entry command exist with those flags? does
the verdict map match the script's exit codes? is the self-test spelling real? are the pinned
values in the tree? does the write scope name what the script writes? Write
`{SCRATCH}/w2-W2RevRowsA/rows-review-a.json`. Report: per row a verdict and the offending cell
for every false row."""))

ITEMS.append(item("W2RevRowsB", "reviewer", ["operability"], f"""Review the second half of the 28 new registry rows (read-only) and the EXISTING 46 rows
for factual drift (the counter's `SELFTEST-UNBACKED` leg found one: `order-check`). Write
`{SCRATCH}/w2-W2RevRowsB/rows-review-b.json`. Report: per row a verdict and the corrected cell
text for every false row, and whether the `order-check` self-test cell can be made true by
changing the row alone."""))

ITEMS.append(item("W2RevEntryLesson", "reviewer", ["depth"], f"""Review the round's prose artefacts (read-only): the knowledge entry draft
(`{SCRATCH}/w2-W2ExecEntryDraft/entry.md`) and the lesson draft
(`{SCRATCH}/w2-W2ExecLessonDraft/lesson.md`). Check every number in them against the counter's
own output (run it), check the entry's provenance lines (`source:`, `verified-at:`, `recheck:`)
name S### rows that exist, and check that the lesson's `## Gate` block carries the URL, the
access date and a ≤25-word located quote for every new row. Report: every number that does not
re-derive, every citation that does not resolve, and the sentence you would delete."""))

ITEMS.append(item("W2RevReportDraft", "reviewer", ["calibration"], f"""Pre-review the round report against its contract (read-only): the report lives at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/kengaku.md` — if the L1 has not written it
yet, review the REQUIREMENTS instead: read the round prompt
`/home/vgpnk/Projects/shokunin/.ufo/prompts/kengaku-round-52.md` §4 and list every required
section and every required item (the `## SHONEN` heading, one `[~]`/`[ ]` line per box of
SHONEN.md, the before->after counting commands with the commit each was measured against, the
sources & frontier rows before->after, the trend verdicts for expansion/quality/discernment).
Write `{SCRATCH}/w2-W2RevReportDraft/report-requirements.md` as a checklist the L1 can tick.
Report: the checklist and the items the L1 is most likely to miss."""))

# ------------------------------------------------------------------ critics (3)
ITEMS.append(item("W2CritA1Amendment", "critic", ["novelty"], f"""Attack Amendment A1 (read-only): it moved the classification unit after the freeze,
because the L1 hand-read three graders and fetched all 89 to test the frozen rule. Is the
amendment a correction of a falsified reading, or is it a rule fitted to the data it is supposed
to measure? Look for the tell: does the amendment change any threshold, target, population or
kill rule? does it make the predicate stricter or looser? could the claim have been met WITHOUT
the amendment? Then attack the amendment's own rule: is `P1` (presence-only) the right weakness
class for a benchmark grader, or is it a trivial one that says nothing about task validity? Write
`{SCRATCH}/w2-W2CritA1Amendment/a1-critique.md`. Report: your verdict (legitimate correction |
fitted rule | indeterminate) with the evidence, and what you would freeze instead."""))

ITEMS.append(item("W2CritC1Reach", "critic", ["novelty"], f"""Falsify R52-C1's after-state end to end (read-only): can the C1 counter print
`PREDICATE R52-C1 pass` without the claimed work being done? Enumerate every input that gets
there — an empty or partial capture set (what if only the graders of candidate tasks are
captured?), a confirmations file written by the L1 without a reader, a prior-art file with three
URLs that say nothing, labels that agree because both come from the same classifier. For each,
run the counter on a fixture lane in your scratch dir and report whether the leg holds. Report:
per construction the counter's actual answer and the smallest fix that would reject it."""))

ITEMS.append(item("W2CritRoundHonesty", "critic", ["calibration"], f"""Attack the ROUND's honesty (read-only): read the frozen claims file, the amendment, the
A1 observation receipt, the wave-1 seat reports under `{LANE}/.ufo/waves/round-52/w1/` and the
lane's SCORECARD.md. Is anything claimed that the evidence does not support? Is the novelty
score bump justified by the prior-art verdict, or by the instrument's existence? Is the
operability bump justified by registry rows that no one verified? Name every sentence the report
must not write, and every claim the round must report as unprovable or harmed. Report: a
per-claim verdict (admissible | not admissible) with reasons."""))

# ------------------------------------------------------------------ mutation-testers (2)
ITEMS.append(item("W2MutC1", "mutation-tester", ["novelty"], f"""Mutation-test the AMENDED C1 counter (read-only; mutate a COPY in your scratch dir):
flip one marker in `classify_test()`, change the split regex, drop the candidate rule, drop the
quote-verbatim check, drop the candidate-membership check, lower the CONFIRMED threshold. For
each mutant, name which control in `{LANE}/plans/round-52-claims.md` should kill it, then RUN
that control against the mutant in your scratch dir and report whether it was actually killed. A
survivor is a defect in the frozen predicate — report it as such; do not fix the counter.
Report: a mutant table (mutant, expected killer, killed yes/no, observed output)."""))

ITEMS.append(item("W2MutC2", "mutation-tester", ["operability"], f"""Mutation-test the C2 counter (read-only; mutate a COPY): widen the ADVERTISED regex so
it matches any file, drop the `INCOMPLETE` leg, make `SELFTEST-UNBACKED` require two scripts,
make the registry block extraction swallow the whole SKILL.md. For each mutant, name the control
that should kill it and RUN it. Report the mutant table."""))

# ------------------------------------------------------------------ revenger (1)
ITEMS.append(item("W2RevA1Intent", "revenger", ["calibration"], f"""Recover the intent behind the round-52 amendment and the lane's 12-round hand-reading
series (read-only): what question was the series answering, what did Amendment A1 preserve, and
what did it risk? Read `{LANE}/corpus/knowledge/tb2-*-grader.md`, the lessons of rounds 35-46 and
the A1 receipt. Report: the series' question, the invariant the amendment preserves, and the
invariant it may have lost."""))

# ------------------------------------------------------------------ sentinel (1)
ITEMS.append(item("W2SentinelScope", "sentinel", ["operability"], f"""Scope and safety review of the round's landed changes (read-only): what the wave wrote into
the lane tree, whether any seat wrote outside its scratch dir, whether any credential-shaped
string or host path leaked into a committed file, whether the capture set contains anything that
is not a public benchmark file, and whether the fleet repo / sibling lanes / `.ufo/state/` were
touched. Check `git -C {LANE} status --porcelain` (read-only) and
`git -C /home/vgpnk/Projects/shokunin status --porcelain`. Report: every out-of-scope write (with
path), every credential-shaped string (redacted — report the location and the shape, never the
value), and your verdict on scope discipline."""))

assert len(ITEMS) == 33, len(ITEMS)
spec = {
    "wave": "kengaku-r52-w2",
    "milestone": "kengaku round 52 wave 2 (falsify): attack the landed grader-triage instrument (R52-C1, novelty) and the 28 new gate-registry rows (R52-C2, operability)",
    "reportDir": ".ufo/waves/round-52/w2",
    "maxLanes": 33,
    "axes": ["novelty", "operability", "calibration"],
    "context": CONTEXT,
    "items": ITEMS,
}
out = Path(f"{LANE}/.ufo/waves/round-52/w2-spec.json")
out.write_text(json.dumps(spec, indent=1))
print(f"wrote {out} items={len(ITEMS)}")
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print(roles)
attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "labrat"))
print(f"attack seats={attack}/{len(ITEMS)} = {attack/len(ITEMS):.0%}")
