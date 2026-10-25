# R29a2 — capability census of the staged package

Seat: `L1Kengaku29.R29a2ConnCapability` (connector). Leaf: no subagents, no production edits.
Everything below is read-only except scratch under `/tmp/r29a2-concapability/` and this file.

**Axes named:** (1) *coverage* — does the lane gain an instrument it does not hold? (2)
*operability* — can that instrument be run, refused, and re-run from committed bytes?
No axis is harmed: nothing here adopts, edits, or re-verdicts C1/C2.

## Method

- Read `plans/round-29-attempt2-claims.md` (frozen claims) first, then
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/MERGE-REPORT.md` (113 lines) and the 65
  first-lines/titles under `merge/kengaku/knowledge/corpus/knowledge/`.
- Classified by **shape of the artefact**, not by round or title: coverage/maintenance records
  (per-benchmark dates, OSF/OEDO/NEDO/CJK access, card-maintenance r13–r16, coverage r13–r15)
  versus artefacts that are a *tool, gate, decision table or error-pattern list*. Only the
  second class can be run; at most five are named.
- Ran the gate that will judge the package (read-only, registry copied to `/tmp`):
  `plans/sources_adopt.py` with `--registry /tmp/r29a2-concapability/SOURCES.md`. The tool writes
  only `--out` (`plans/sources_adopt.py:379-397`), so no lane byte was written.

## The five named candidates

Each row: capability statement → evidence that would prove it runs → why the lane lacks it today.

### 1. `contamination-transparency-card.md` — card field table + Q1–Q8 answerability gate

**Capability.** A per-benchmark, per-release card schema (release-side R1–R5, score-side S1–S2;
`merge/.../contamination-transparency-card.md:20-43`) whose admission test is a *refusal table*:
each of Q1–Q8 names the question, the source it is answerable from, and the condition under which
it is **not** answerable (`:47-60`) — e.g. Q4, "what a negative does not rule out", is not
answerable when the report reads "no contamination found" as "no contamination".

**Evidence that would prove it runs.** `python3 plans/card_check.py --selftest` exits 0 with a
fixed PASS count over at least these mutants, each failing on a broken implementation: a card with
S2 absent (must refuse), a card answering Q4 from a single detector's negative (must refuse), a
card whose Q5 claim is filed release-side while the text says acquired-during-evaluation (must
refuse), and the clean fixture (must pass); plus a live run over one filled card at exit 0. Same
idiom the lane already uses: `plans/sources_adopt.py --selftest` prints `CASE … PASS` per control
(`plans/sources_adopt.py:257-267`, observed `SELFTEST cases=10 failed=0`, exit 0).

**Why the lane lacks it today.** `corpus/README.md:260` states it as the gap verbatim — "the lane
has no standard card format recording detector access, tier tested, and what a negative cannot rule
out". The lane's only contamination entry holds a prose Situation/Do/Don't table
(`corpus/knowledge/contamination-detection-and-transparency.md:68-73`); `grep -rl not_controlled
plans corpus/knowledge` → **0 files**, i.e. not even the declared-negative vocabulary exists.

Runs today: `--admit-ids S081,S082,S083,S084,S085,S086` → `malformed=0 … prose=6`, exit 0.

### 2. `benchmark-card-field-schema-2026-10-23.md` — an *external* schema + validator instead of a house design

**Capability.** Three published card forms side by side, of which one is machine-readable and
ships its own validator: `templates/disclosure.schema.json`, `docs/validate.py`, a versioned
`disclosure_version: "1.1"` at a pinned commit, with a **declared-negative decision rule** —
`"unknown"` and `"not_controlled"` are complete entries, so "we did not test this" is a valid card
(`:37-52`, `:47`), and a **do-not-merge rule**: S124's five dimensions and S123's four fields "are
**not** the same taxonomy" (`:91-92`). The lane's own field list is cross-tabbed against all three
at `:70-79`, which is the arbitration table a maintainer-facing card needs.

**Evidence that would prove it runs.** `python3 plans/card_schema_pin.py --check` resolving the
pinned schema from cache, validating a fixture disclosure record, and exiting non-zero on (a) a
missing required field, (b) a value outside the enumerated set, (c) a *blank* field used where the
form requires a declared `unknown`/`not_controlled` — i.e. proving the rule "a field left blank is
a field that cannot be checked" (`:30-31`) is enforced, not quoted.

**Why the lane lacks it today.** `grep -rl disclosure.yaml plans corpus/knowledge` → **0 files**.
The lane has never pinned a third-party schema; every existing gate validates lane-authored
bytes (`plans/registry_check.py`, `plans/adoption_check.py`). The distinct value is that the card
gate would stop being self-graded.

Runs today: `--admit-ids S122,S123,S124` → exit 0 (checked together with the S081–S086 set, above).

### 3. `benchmark-task-validity-checklist.md` — the A–J axis table, executed (C1 overlap, capability half)

**Capability.** A ten-axis audit table (A instruction–grader traceability … J reproducible
release, `:22-31`) where every axis states an **observable in published artefacts** and its
evidence, so each axis resolves to a mechanical verdict — PASS / observable-but-unpublished /
UNCONFIRMED-with-reason — instead of a prose judgement. The entry already does the per-benchmark
imputation honestly (`:45-52`): it names which axes remain unobservable per benchmark.

**Evidence that would prove it runs.** `python3 plans/task_validity_audit.py --selftest` exiting 0
with per-axis controls that *can fail*: axis B flips when the reference solution stops passing,
axis C flips when the empty patch passes, axis E refuses to print "isolated" for a task whose
`task.toml` omits the verifier environment, and axis H fails on a missing `schema_version`. Then one
live run over the pinned Terminal-Bench 2.0 tree at exit 0 printing ten axis verdicts.

**Why the lane lacks it today.** `corpus/README.md:259` names the missing instrument; the only
task-spec tool in the lane disclaims exactly this capability in its docstring:
`plans/benchmark_spec_audit.py:2` — "Static inventory of original WebArena task specs, **never a
task-validity verdict**". `plans/registry_check.py` checks literal reference coverage, not validity.

**C1 overlap, stated so it is not double-counted.** C1 adopts this entry this round; it does not
land the instrument. The capability gap that survives C1 is the executable axis table, not the
prose. Rows are gate-clean: `--admit-ids S077,S078,S079,S080,S090` → `malformed=0 defects=0
prose=5`, exit 0.

### 4. `benchmark-verifier-execution-model.md` — a per-task verifier-mode resolver (decision table)

**Capability.** A default-resolution rule plus an observed per-task table: `environment_mode` is
`separate` only when a `[verifier.environment]` section is set, otherwise **`shared`** — "the
verifier runs in the *same container the agent was working in*" (`:23-25`), and neither benchmark
opts in (`:27`, `:31-32`). It then states what survives regardless of mode: stale reward files
deleted, `tests` re-uploaded from the host, while **agent edits to fixtures and data are not
reverted** (`:35-52`). That is a decision table a gate can evaluate from a `task.toml`, and an
error-pattern list ("a card that records only the first overstates the second", `:58-63`).

**Evidence that would prove it runs.** `python3 plans/verifier_mode.py --tree <pinned TB2.0> --tree
<SWE-bench Pro V2>` exiting 0 and printing, per task, the resolved mode plus which protections
apply; the counter must refuse to label a task `isolated` when its `*.toml` has no
`[verifier.environment]`/`environment_mode`, and a one-line fixture mutation adding
`environment_mode = "separate"` must flip the verdict to `separate`.

**Why the lane lacks it today.** `grep -rl environment_mode plans corpus/knowledge` → **0 files**.
No lane tool reads a benchmark's harness config; axis E has only ever existed as prose.

**Operability caveat, measured.** Its source row `S093` is **refused by the gate C2 lands this
round** (finding F1 below), so the capability can be named but not staged until that row's anchor
cell is repaired. `--admit-ids S092,S100` → exit 0; adding `S093` → exit 4.

### 5. `grader-predicate-input-types.md` — typed-fixture dispatch + a four-convention error list

**Capability.** A measured error-pattern list that corrects the lane's own probe methodology: the
round-6 negatives were artefacts of *argument shape* (`:9-16`), and once fixtures carry the
functions' real types, **16 of 16** comparison functions separate an identical pair from a
one-unit-perturbed pair (`:23`). The reusable part is the taxonomy of return conventions — boolean
predicates, `(bool, str)` pairs, error lists that must be **empty** on a match, and graded scores
that must be compared to a threshold rather than for truthiness (`:26-29`) — plus the honest
boundary ("runs no task, touches no workspace", `:36-39`).

**Evidence that would prove it runs.** `python3 plans/grader_contract_probe.py --selftest` exiting 0
with a discriminating control per convention, including the *negative* control that a bare string
passed to a dict-indexing comparator is reported `fixture-rejected`, **never** `uninformative` —
the exact miscoding that produced the round-6 false negatives — and a re-run over the pinned
Toolathlon commit reporting a verdict per function with an explicit `not-attempted` list.

**Why the lane lacks it today.** `grep -rl compare_rating plans corpus/knowledge` → **0 files**;
`plans/grader_perturb.py:2` audits "the committed response-grader population", i.e. the lane's own
`grader.py` with `BAR = 0.95` (`:17`), not any foreign grader's argument contract. The lane has no
harness that dispatches on a comparator's signature.

**Operability caveat, measured.** Its grounding row `S144` cites the artefact path
`lanes/kengaku/round7/toolathlon-grader-fixture-probe.md`; `grep -rn lanes/kengaku` across the
lane → **0 hits**, and the package ships only `*.md` knowledge files, no artefact tree. So the
16/16 result is not re-openable from either the lane or the package: proving the capability runs
means *re-executing* the probe, not citing S144. `--admit-ids S143,S144` → exit 0.

## Considered, not named (capability-adjacent, deprioritised)

- `terminal-bench-release-identity.md` — genuinely an error-pattern list ("a dataset version
  cannot be pinned by tag"; "92 tree entries" ≠ "92 task directories"), and it is a *self-correction*
  of a lane count. Kept off the five because the lane already pins by commit and sha256 in its
  claims and gates, so the marginal capability is small.
- `judge-calibration-thresholds.md` — supplies per-variable reporting, a published test–retest
  ceiling and a pre-registered threshold; the lane already holds the judge Decision table
  (`corpus/knowledge/llm-judge-calibration.md:68-73`) and a pre-registered bar
  (`plans/grader_perturb.py:17`). Additive, not new.
- `toolathlon-grader-contract-2026-10-23.md` — the 108-grader source table that candidate 5 needs;
  it is candidate 5's input, not a second capability.
- The probe cluster (`grader-fixture-coverage`, `grader-fixture-probe-stage3`,
  `grader-candidate-coverage{,-r13,-r14,-r15}`, `grader-candidate-reconstruction`,
  `spreadsheet-grader-fixtures`, `grader-sheet-checks-real-pandas-r16`) is **one** capability
  restated across eight entries; counting them separately would inflate the census.
- The r13/r14/r15 card, OSF, post5G and coverage files are maintenance records; `diff`-ing
  `benchmark-card-maintenance-r13.md` against `-r14.md` after date-normalisation still shows 87
  changed lines, so they are distinct records, not duplicates — but they are coverage, not tools.

## The one proposed move (synthesis across two candidates)

**Do not write a third card design. Run S123's published validator and add S081's answerability
columns to it, keeping the two taxonomies split.**

Candidates 1 and 2 are the same axis reached from opposite directions: #1 builds a house card and
its Q1–Q8 refusal test; #2 finds a versioned schema, an actual `docs/validate.py`, and the
declared-negative rule already published. The synthesis keeps every strength and drops the
invention: adopt the *field enforcement* from S123 (external, versioned, not self-graded) and the
*answerability refusal* from S081 (which the schema cannot express, because "not answerable when"
is an evidence question, not a type question), and record S123's four fields beside S124's five
dimensions instead of merging them (`benchmark-card-field-schema-2026-10-23.md:91-92`). One gate,
two provenance chains, no third card prose. This improves coverage (a runnable card gate the lane
does not have) without harming operability (both sources are pinned and re-openable), and it leaves
C1 and C2 untouched.

## Contradictions found in the staged package — stated, not scored

**F1 — the package does not pass the gate that will admit it (175 claimed vs 173 stageable).**
Observed, exit 4:

```
$ python3 plans/sources_adopt.py --registry /tmp/r29a2-concapability/SOURCES.md \
      --package /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
registry=76 staged=173 collisions=0 malformed=2 duplicates=0 defects=171 prose=171
  malformed: S093:escaped-pipe S101:escaped-pipe
exit=4
```

`MERGE-REPORT.md:5` says "proposed rows accepted: **175**, refused: **0**". Two rows — `S093`
(14 pipe-fields) and `S101` (17 pipe-fields, a triple-quoted docstring containing table rows) —
carry a literal `|` inside a cell, which is precisely the defect
`plans/sources_adopt.py:63-70` calls "the real failure seen on the kengaku campaign package".
The other 173 rows are clean and stage individually (so C1's five rows are unaffected: exit 0).
Scoped mode is the lane's actual adoption path, so this is a package-level ledger error plus three
entries that cannot be staged as written — `benchmark-verifier-execution-model.md`,
`benchmark-grader-semantics.md`, `benchmark-grader-integrity-models-2026-10-23.md` all cite
`S093`/`S101`.

**F2 — the landed gate silently downgrades `on-commit` cadences.** `SYMBOLIC_CADENCE =
{"on-release", "on-request", "never"}` (`plans/sources_adopt.py:36`) omits `on-commit`, which the
staged package uses on **22 rows** (`awk` count over the 173 clean rows; `on-release` 7, `180d`
69, `90d` 24, dated 51). Observed consequence on a real row:

```
$ … --admit-ids S143,S144 --access-date 2026-10-25
  normalized recheck S143: on-commit
  normalized recheck S144: on-commit — `python3 lanes/kengaku/round7/… --fetch …`
exit=0
```

i.e. a re-check-on-commit row becomes a dated row and its cadence is only reported to stdout. For
candidate 5's own rows that turns "invalidate on commit" into "re-check in 0 days". This is a
C2-side design risk the L1 should weigh before the gate is declared standing: either `on-commit`
joins the cadence set, or rule 3's normalization must refuse rather than relocate a symbolic
cadence.

**F3 — two staged entries contradict each other on axis E, and C1 adopts only one of them.**
`benchmark-task-validity-checklist.md:26` states axis E's observable as "the verifier does not run
inside the agent's sandbox; … **agent edits to fixtures and snapshots are reverted**", and `:49-50`
records axis E for TB2.0 as "partly observable (the Harbor harness separates the verifier from the
agent)". The package's own `benchmark-verifier-execution-model.md:23-32` reads the same harness as
**shared by default with no task opting in**, and `:42-52` states the opposite of the axis-E cell
in as many words: the tests directory is re-uploaded, but "the agent's edits to the **environment
under test** — the source tree, the fixtures, the data — are **not** overwritten". `:58-63` then
qualifies S078's "never runs in the agent's sandbox" as true only of the locked replay path.

So if C1 lands the checklist alone, the lane will hold as a checklist *observable* a property that
the same package's S092 reading falsifies for the default path. Neither entry is wrong about its
own source; they are about different code paths and the checklist's cell does not say so. I am
not adjudicating which text is admitted — only recording that the pair cannot be read as
consistent, and that the sibling entry is the one that carries the qualifier.

**F4 — 17 of 65 entries ground on lane paths that exist in neither the package nor the lane.**
`grep -l lanes/kengaku merge/kengaku/knowledge/corpus/knowledge/*.md` → 17 files; `grep -rn
lanes/kengaku` in the lane → 0 hits, `ls lanes` → absent, and the package ships no artefact tree
(`ls -R merge/kengaku` → `MERGE-REPORT.*`, `SOURCES.append.md`, `knowledge/corpus/knowledge/*.md`).
Eight of those 17 are the grader-probe cluster. Their capability claims are therefore
**unverifiable from staged bytes** and need a re-run, not a citation — which is why candidate 5's
proof clause is an execution, not a reference.

## Verification ledger (commands actually run)

| command | exit | result |
|---|---|---|
| `plans/sources_adopt.py --selftest` | 0 | `SELFTEST cases=10 failed=0` |
| `… --package SOURCES.append.md` (package mode, /tmp registry) | 4 | `staged=173 malformed=2`, S093/S101 escaped-pipe |
| `… --admit-ids S077` | 0 | clean, prose recheck normalized |
| `… --admit-ids S077,S078,S079,S080,S090` | 0 | C1 row set clean (`malformed=0 defects=0 prose=5`) |
| `… --admit-ids S081…S086,S122,S123,S124` | 0 | card row set clean (`prose=9`) |
| `… --admit-ids S092,S100` | 0 | clean |
| `… --admit-ids S092,S100,S093` | 4 | `malformed: S093:escaped-pipe` |
| `… --admit-ids S143,S144` | 0 | clean; `on-commit` reported as prose |
| `grep -rl {environment_mode,compare_rating,disclosure.yaml,not_controlled} plans corpus/knowledge` | 1 | 0 files each |
| `awk` field census over `SOURCES.append.md` | 0 | 173×11 cells, 1×12, 1×15 |

No tools were installed or upgraded for this seat. No production file other than this report was
created, edited or deleted; scratch lives in `/tmp/r29a2-concapability/`.

This report body is the evidence locus, not the scratch copy: every ledger line quotes its command
and the bytes it printed, and the only scratch input the gate runs need is a read-only registry
copy, regenerable in one step —
`mkdir -p /tmp/r29a2-concapability && cp corpus/SOURCES.md /tmp/r29a2-concapability/`.
No claim here depends on an ephemeral file surviving.

Nothing was adopted, and no part of this report re-verdicts C1 or C2.
