# R29a2 — province + coverage-map review of the adopted task-validity entry

- Seat: `R29a2RevEntryScope` (reviewer, leaf; no dispatch, no production edit).
- Round 29 attempt 2 (hyaku run 6), 2026-10-25. Baseline revision
  `1f3b0f1ec41ec297130e8944ff97968d32324632`.
- Bytes reviewed: `corpus/knowledge/benchmark-task-validity-checklist.md` (86 lines, untracked at
  review time), `corpus/SOURCES.md` rows S077/S078/S079/S080/S090 (lines 100-104,
  working-tree modification), `plans/sources_adopt.py` (working-tree diff),
  `plans/adoption_check.py`, `PROVINCE.md`, `corpus/README.md`, `corpus/QUALITY.md`.
  The shokuknow package copy (`/home/vgpnk/Projects/shokuknow/merge/kengaku/...`, 73 lines,
  `verified-at: 2026-10-23`) is **not** what I reviewed as the object under test; the lane copy
  re-grounded to `verified-at: 2026-10-25` exists and is the current candidate.
- Tooling: no install or upgrade was run — nothing was needed.

---

## (a) Does a published per-task-validity checklist stay inside kengaku's province? — YES, and it routes out five things

**Inside, on the charter's own words.** The lane's domain is `LLM/model research & evaluation`
(`PROVINCE.md:3`) and what it *owns* is "the domain knowledge, playbooks, error patterns, and
**checklists** above" (`PROVINCE.md:5`). A checklist of published validity instruments is exactly a
named owned object type, not a trespass. The source surface is also already owned: `Public literature …
GitHub issues` (`PROVINCE.md:20`), and the round-24 map narrowed that to "reachable-by-citation only —
documentation reads only this round, no live model/endpoint traffic" (`PROVINCE.md:115`). The five rows
are GitHub docs/spec trees plus one project page, so nothing in the check requires a live surface.

**Precedent with the identical object class.** `PROVINCE.md:194-196` admits "pinned WebArena
task-spec/scorer observability" and defines its limit as: "This owns static LLM-evaluation interpretation,
not the benchmark's web properties or runtime services." The checklist is the same object — static
interpretation of published artefacts — for three other benchmarks. `corpus/README.md:329` states the
same boundary for the sibling instrument ("not task-validity certification"), and
`corpus/README.md:331` for the admitted entry ("not task validity or model performance"). The entry
respects it at `corpus/knowledge/benchmark-task-validity-checklist.md:75-77` ("Not task validity itself …
it does not run a benchmark or certify any task").

**What it routes out (must not be absorbed):**

| Routed to | What, in this entry | Evidence |
|---|---|---|
| **kama** (+ integrator for flag authority) | any serving-plane / endpoint-identity remediation a "run the benchmark" reading would drag in; the entry's emitting a verdict about a *harness* does not license serving-plane work | `PROVINCE.md:136`; `PROVINCE.md:201-202` ("Serving-plane restoration stays operator/kama-owned") |
| **chousa** | research *method* — the entry may claim "a synthesis of primary maintainer documents, not a new research method" (`…checklist.md:18`) but not a method contribution; the question→source-hierarchy→citation-chain method is chousa's | `PROVINCE.md:137`; `corpus/QUALITY.md:7-8` |
| **kake** | the benchmarks' *web properties* — reading `tbench.ai`, `github.com/...` trees is literature access, not web-property ownership | `PROVINCE.md:143`; `PROVINCE.md:196` |
| **kotoba** | instruction-/prompt-craft as craft. Axis A reads whether a graded assertion traces to an instruction sentence; that is *validity of the spec*, and the reusable "how to write the instruction" implication goes out | `PROVINCE.md:138` |
| **kumitate** | operational failure taxonomy. Axis D (environment drift) is a maintainer *report* about a task, never OMP route/fallback semantics | `PROVINCE.md:141` |

Residual: anything genuinely cross-domain is reported out, not absorbed (`PROVINCE.md:6`). Two things
belong to **no** sibling lane and therefore must be *left open and stated*, not routed: actual
env_config-derived/deployment configs and runtime task validity (`PROVINCE.md:208-211`), and hosted
judges (`PROVINCE.md:200-201`, `:210`).

---

## (b) Does it cover frontier ground the lane did not hold? — YES, for one bullet, and it leaves the rest of that bullet open

**The bullet it advances** is `corpus/README.md:259` (Frontier bullet 1, "Agentic benchmark task-spec
audits"): "the lane has no instrument that audits a benchmark's task specs, graders, and contamination
separately. Next source/instrument: the primary specs and scoring code for Terminal-Bench 2.0,
Toolathlon, and SWE-bench Pro (unopened leads in the ART dossier), turned into a per-benchmark
task-validity checklist."

That ground was still open after round 28/29 attempt 1: `corpus/README.md:338-339` ("Terminal-Bench2.0,
Toolathlon and SWE-bench Pro primary specifications … remain open") and `PROVINCE.md:200-201` (same
sentence). The entry names all three families and builds the per-axis instrument, so it is new coverage,
not a restatement.

**What the lane actually held before (so the row can say "adds", not "first ever"):**

- `corpus/README.md:236` — "*Agentic time horizon and task validity*: covered at source-digest depth
  (round 24) … sources S013, S014, S005, S006" — external audits only (S006, `agent-time-horizon-and-task-validity.md:19`),
  no per-task instrument.
- `corpus/knowledge/benchmark-selection.md:18` — names Terminal-Bench 2.0 and SWE-Bench Pro as
  *selection* targets, with no validity instrument.
- `corpus/README.md:335` and `:362` — WebArena static schema/predicate observability and generated-config
  projection; different benchmark, different object.
- `grep -rl "Toolathlon\|SWE-bench Pro\|Terminal-Bench" corpus/knowledge/` → only `benchmark-selection.md`
  and `agent-time-horizon-and-task-validity.md`. No prior task-validity checklist exists.

**What the same bullet still does not get, so the row must not imply it:**
the bullet asks for "*the primary specs and **scoring code** … turned into*" a checklist. The entry reads
docs and task-package schemas; on Terminal-Bench 2.0 it explicitly refuses the grader-isolation axis
(`…checklist.md:66-67`: covers A, B, C, D, F, G; "J is open"; E is not claimed) and it derives axis E only
from S078 (`…checklist.md:30`, `:68-69`). Scoring-code execution and TB2.0/Toolathlon grader isolation
therefore remain open ground.

**Bullets deliberately untouched** (adjacent, not covered): `corpus/README.md:260` (contamination
transparency cards), `:261` (judge calibration applied inward), `:266` (identity-verified endpoint),
`:267` (non-karpathy wiki). Axis G (`…checklist.md:32`, `:78-79`) is a *canary-practice observable*; it is
not the card format `:260` asks for and it explicitly disclaims detector semantics.

---

## (c) The coverage-map row to add — and what it must not claim

### Required landing set (all in the admitting commit, per `corpus/QUALITY.md:56-58`)

1. **Index row** — the counter's `indexed` is a literal match on
   ``| `knowledge/benchmark-task-validity-checklist.md` |`` (`plans/adoption_check.py:75-76`). Observed
   now: `entries=1 indexed=0 … exit=1` (command below), i.e. **the coverage-map bullet alone will not
   make the frozen C1 target print `indexed=1`**. Add a row to the round-29 attempt-2 admitted-knowledge
   table, matching the round28/29 pattern at `corpus/README.md:331` / `:358`:

   ```
   | `knowledge/benchmark-task-validity-checklist.md` | Ten-axis validity checklist synthesised from four maintainers' published instruments and task-package schemas; axes mapped per benchmark with unconfirmed axes named; not task validity, grader execution or contamination measurement | S077, S078, S079, S080, S090; round29 attempt-2 Gate |
   ```

   (If the lane instead adds it to the main *What's here* table, insert after `corpus/README.md:63`; the
   counter is satisfied either way, but only by a pipe-row.)

2. **Coverage-map row** — §Coverage map bullet list, insert after `corpus/README.md:237`:

   ```
   - **Published per-task validity instruments (maintainer checklist)**: covered at source-digest depth
     (round 29 attempt 2) — knowledge/benchmark-task-validity-checklist.md; sources S077, S078, S079,
     S080, S090. Extends the *Agentic time horizon and task validity* row (round 24) from external audits
     to maintainer-published instruments for Terminal-Bench 2.0, SWE-bench Pro V2 and Toolathlon-Verified
     at pinned commits; static published artefacts only, axes per benchmark stated, unconfirmed axes
     named. Terminal-Bench 2.0 scoring code/grader isolation, runtime task validity, deployment config and
     contamination measurement stay open.
   ```

3. **Narrowing paragraph** — new "Round29 attempt-2 partial frontier advance" note after
   `corpus/README.md:367`, closing on the same pattern as `:364-367` ("narrows, not erases"): the three
   named benchmarks' instrument documentation and task-package schema are now held; their scoring
   code/execution, runtime validity, hosted judges and contamination stay open as written at `:338-339`
   and `:365`.

### What that row must NOT claim (one sentence, then the cells that enforce it)

**It must not claim deployment config, runtime validity, or contamination.** Each clause has a carried
line: deployment/env_config-derived configs and runtime task validity are open (`PROVINCE.md:209-210`;
`corpus/README.md:364-366`), hosted judges are open (`PROVINCE.md:201`, `:210`), and contamination is a
source-digest row plus an open card bullet, not a measurement (`corpus/README.md:230`, `:260`, `:339`).

Extended do-not-claim list for whoever writes the row:

- **not "task validity" / not certification** — `PROVINCE.md:196`; `corpus/README.md:329` ("not
  task-validity certification"); `corpus/README.md:331` ("not task validity or model performance");
  `…checklist.md:75-77`.
- **not contamination measurement, not the transparency card of `corpus/README.md:260`** —
  `…checklist.md:78-79` ("G reads a maintainer's canary practice; it is not a detector").
- **not model performance / capability / difficulty** — `…checklist.md:80-81`; `PROVINCE.md:3` scope is
  eval craft, and the claims file forbids "model performance" (`plans/round-29-attempt2-claims.md:90-92`).
- **not a new research method** — `…checklist.md:18`; `PROVINCE.md:137`; `corpus/QUALITY.md:7-8`.
- **not "four benchmarks"** — it is three benchmark families across four maintainer organisations, five
  source rows (`…checklist.md:13-14`, `:82`); write "three benchmark families", not "four benchmarks".
- **not grader isolation for Terminal-Bench 2.0 or Toolathlon** — axis E is held only from S078
  (`…checklist.md:30`, `:66-69`).
- **not a discharge of the other Frontier bullets** — `corpus/README.md:260-267`.

---

## Findings (severity order)

### F1 — MEDIUM (admission, Q6): the entry names no existing entry or coverage row it extends
`corpus/knowledge/benchmark-task-validity-checklist.md:11-20` cites only `corpus/README.md §Frontier`;
`grep -n "extend\|agent-time-horizon\|webarena\|WebArena" …checklist.md` → rc=1 (no match).
`corpus/QUALITY.md:50-52` requires "The entry names the existing entry or coverage row it extends".
Nearest owner row is `corpus/README.md:236` (S005/S006 task-validity digest). A coverage row that says
"Extends …" does **not** repair Q6, which binds the entry. Fix: one sentence in the entry naming
`knowledge/agent-time-horizon-and-task-validity.md` (and stating the WebArena rows are adjacent, not
extended).

### F2 — MEDIUM (operability): the five landed rows are due for recheck on landing day
Observed cells (all five rows): `opened=2026-10-25`, `recheck=2026-10-25`, `status=mined`,
`used-by=corpus/knowledge/benchmark-task-validity-checklist.md` (`corpus/SOURCES.md:100-104`), produced by
the gate's prose-normalization (`plans/sources_adopt.py:149-153`). Consequence, run read-only on the
current tree:

```
$ ./scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin --today 2026-10-25 kengaku-shokunin | tail -5
kengaku-shokunin	overdue	S090 0d recheck=2026-10-25 opened=2026-10-25
kengaku-shokunin	overdue	S080 0d recheck=2026-10-25 opened=2026-10-25
kengaku-shokunin	overdue	S079 0d recheck=2026-10-25 opened=2026-10-25
kengaku-shokunin	overdue	S078 0d recheck=2026-10-25 opened=2026-10-25
kengaku-shokunin	overdue	S077 0d recheck=2026-10-25 opened=2026-10-25
```

`census=ok` still holds (`./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kengaku-shokunin` → exit 0, final line `kengaku-shokunin  ok  …/corpus/SOURCES.md`; only pre-existing W04
warnings), so C1's exact target is not blocked. But the entry advertises `recheck: 180d … next due
2027-04-23` (`…checklist.md:7`) while the registry says due today — an internal inconsistency, and five
immediate `overdue` lines on the landing day. Fix: give the five staged cells `recheck=180d` (the gate
keeps a valid cadence — `plans/sources_adopt.py:149-151`; the census accepts `NNd` —
`scripts/sources-census.sh:663-666`), so registry and entry agree.

### F3 — MEDIUM (operability): `indexed=0` until a pipe-row exists in `corpus/README.md`
```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json
entries=1 indexed=0 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped
exit=1
```
`plans/adoption_check.py:75-76` matches the literal ``| `knowledge/<name>` |`` only. A §Coverage map
bullet (which writes `knowledge/<name>.md` without the surrounding pipes) does not satisfy it, and neither
does prose. The row in (c)(1) is the smallest fix; Q7 (`corpus/QUALITY.md:56-58`) additionally requires the
coverage row in the same commit.

### F4 — LOW (coverage wording): "Four benchmark maintainers" over-counts benchmark families
`…checklist.md:13-14` and `:82` say four maintainers; the five rows cover four *organisations*
(harbor-framework S077, scaleapi S078, laude-institute S079, hkust-nlp S080 — plus S090 on the same
Terminal-Bench project) across **three** benchmark families. Leave the maintainer count, but the coverage
row must say "three benchmark families" so no reader infers four independent benchmarks.

### F5 — LOW (coverage): axis E is S078-only and the row must keep it there
`…checklist.md:30` sources grader isolation to S078 alone; `:66-69` applies E to SWE-bench Pro V2 only.
A row that says "task-validity checklist for three benchmarks" without the per-axis caveat would convert a
declared gap into an implied result.

### F6 — LOW (coverage): axis G must not be read as the contamination-transparency-card bullet
`…checklist.md:32` (canary present + checked mechanically) and `:78-79` (not a detector) versus
`corpus/README.md:260` (card format recording detector access, tier tested, what a negative cannot rule
out). Different artefacts; the row must carry "contamination measurement" on the not-claimed side.

## What I verified vs what I did not

Verified by execution this seat: counter pre-state (`entries=1 indexed=0`, exit 1); gate selftest
(`python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=10 failed=0`, exit 0); fleet validate on the
lane (exit 0, `ok`); fleet overdue on 2026-10-25 (five `0d` lines); row cell values for S077-S080/S090;
absence of any extend/WebArena reference in the entry; S077 identity and its canary/oracle/nop/cheat-trial
lines by direct fetch of the pinned raw file (`HTTP 200`, 461 lines; `check-canary` heading at line 93,
the quoted canary sentence at line 95, `Oracle Validation — Solution passes all tests` at line 244).

Not verified here (other seats own it): quote fidelity and ≤25-word bounds (RevQuoteS077/S078/S079/S080/
S090), the 92/89 and 109/108 counts (Src seats), selftest mutant adequacy (FixtureMutations/GateAudit),
and whether the Gate's Q10/Q13 report set is complete (GateAudit). No verdict on admission is offered —
this report advises the L1 only.
