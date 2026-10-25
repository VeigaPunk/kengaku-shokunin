# R29a2 — province + coverage-map review of the adopted task-validity entry

- Seat: `R29a2RevEntryScope` (reviewer, leaf; no dispatch, no production edit, no `ask`).
- Round 29 attempt 2 (hyaku run 6), 2026-10-25. Baseline revision
  `1f3b0f1ec41ec297130e8944ff97968d32324632`.
- **Concurrency note:** the entry, the five registry rows, the README index/coverage rows and the
  lesson Gate landed *while this review was running* (entry 73 → 86 → 97 lines; `corpus/README.md`
  gained rows at 64/249/271). Every anchor below is therefore given as `line` **plus a quoted
  substring**, and the state I measured is stated with the command that produced it. Where a finding
  was overtaken by a sibling's edit I say so instead of deleting it.
- Bytes reviewed: `corpus/knowledge/benchmark-task-validity-checklist.md` (97 lines, untracked),
  `corpus/SOURCES.md:100-104` + row cells (working-tree modification),
  `plans/sources_adopt.py` (working-tree diff), `plans/adoption_check.py`, `PROVINCE.md`,
  `corpus/README.md`, `corpus/QUALITY.md`, `corpus/lessons/round-29.md` §Attempt 2.
- Tooling: **no install or upgrade was run** — nothing was needed.

Measured at review close:

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
rc=0
```

---

## (a) Does a published per-task-validity checklist stay inside kengaku's province? — YES; it routes out five owners and absorbs nothing

**Inside, on the charter's own words.** The lane's domain is `LLM/model research & evaluation`
(`PROVINCE.md:3`) and what it *owns* is "the domain knowledge, playbooks, error patterns, and
**checklists** above" (`PROVINCE.md:5`). A checklist is a named owned object type, not a trespass. The
source surface is owned too: `Public literature … GitHub issues` (`PROVINCE.md:20`), narrowed by the
round-24 map to "reachable-by-citation only — documentation reads only this round, no live
model/endpoint traffic" (`PROVINCE.md:115`). All five rows are GitHub docs/spec trees plus one project
page, so no live *model/endpoint* surface is needed — this seat read one of them over HTTP (the pinned
S077 raw file, HTTP 200) and made no model or endpoint request.

**Precedent with the identical object class.** `PROVINCE.md:194-196` ("**Core addition:** pinned WebArena
task-spec/scorer observability … This owns static LLM-evaluation interpretation, not the benchmark's web
properties or runtime services"). The checklist is the same object for three other benchmark families.
The lane's own wording precedent sits at `corpus/README.md:343` ("not task validity or model
performance") and `corpus/README.md:331` for `benchmark_spec_audit.py` ("not task-validity
certification"). The entry respects it at `…checklist.md` §"What this does not establish"
(`- **Not task validity itself.** … it does not run a benchmark or certify any task.`).

**What it routes out — must not be absorbed:**

| Routed to | What, in this entry | Evidence |
|---|---|---|
| **kama** (+ integrator for flag authority) | any serving-plane / endpoint-identity remediation a "run the benchmark" reading would drag in; a verdict about a *harness's* design is not licence for serving-plane work | `PROVINCE.md:136`; `PROVINCE.md:201-202` ("Serving-plane restoration stays operator/kama-owned") |
| **chousa** | research *method* — the entry may say "a synthesis of primary maintainer documents, not a new research method" but not claim a method contribution | `PROVINCE.md:137`; `corpus/QUALITY.md:7-8`; `…checklist.md:18` |
| **kake** | the benchmarks' *web properties* — reading `tbench.ai` and `github.com/...` trees is literature access, not web-property ownership | `PROVINCE.md:143`; `PROVINCE.md:196` |
| **kotoba** | instruction-/prompt-craft as craft. Axis A asks whether a graded assertion traces to an instruction sentence — *validity of the spec*; the reusable "how to write the instruction" implication routes out | `PROVINCE.md:138` |
| **kumitate** | operational failure taxonomy. Axis D (environment drift) is a maintainer *report* about a task, never OMP route/fallback semantics | `PROVINCE.md:141` |

**Absorb nothing cross-domain** (`PROVINCE.md:6`). Two things belong to no sibling and must stay
*stated-open*, not routed: actual env_config-derived/deployment configs and runtime task validity
(`PROVINCE.md:208-211`), and hosted judges (`PROVINCE.md:200-201`, `:210`).

**Judgement:** in province, with one honest seam. Axis E's caution — "Axis E is scoped to the harness
that publishes the claim … a harness that runs the verifier in a shared environment by default does not
inherit that property" (`…checklist.md:58-61`) — is a reasoning step about harness design, not a measured
harness fact. It is safe as written *because* it refuses generality; it must not later be quoted as an
observation about a harness the lane never ran.

---

## (b) Does it cover frontier ground the lane did not hold? — YES for one bullet's specification half; that bullet's scoring-code half and all other frontier bullets stay open

**The bullet it advances** is `corpus/README.md:270` ("Agentic benchmark task-spec audits"): "the lane has
no instrument that audits a benchmark's task specs, graders, and contamination separately. Next
source/instrument: the primary specs **and scoring code** for Terminal-Bench 2.0, Toolathlon, and
SWE-bench Pro (unopened leads in the ART dossier), turned into a per-benchmark task-validity checklist."

Ground still open before this attempt: `corpus/README.md:349-352` ("Terminal-Bench2.0, Toolathlon and
SWE-bench Pro primary specifications, generated eval-time configs, runtime DOM/helper/judge validity and
contamination checks remain open"), `corpus/README.md:376-379` (same list narrowed to generated configs
only), and `PROVINCE.md:200-201`. The entry names all three families and builds the per-axis instrument,
so this is new coverage, not a restatement.

**What the lane already held — so the rows say "moves", not "first ever":**

- `corpus/README.md:246` — "*Agentic time horizon and task validity*: covered at source-digest depth
  (round 24) … S013, S014, S005, S006": external audits only, no per-task instrument
  (`corpus/knowledge/agent-time-horizon-and-task-validity.md:19` = S006's ≈30%-broken line).
- `corpus/knowledge/benchmark-selection.md:18` — Terminal-Bench 2.0 and SWE-Bench Pro appear as
  *selection* targets only.
- `corpus/README.md:347` / `:374` — WebArena static-schema and generated-config observability: different
  benchmark, different object.
- `grep -rl "Toolathlon\|SWE-bench Pro\|Terminal-Bench" corpus/knowledge/` → only
  `benchmark-selection.md` and `agent-time-horizon-and-task-validity.md`. No prior task-validity
  checklist exists.

**What the entry adds beyond a restatement** (this is the part that makes the coverage claim credible):
re-derived counts with their unit correction (`…checklist.md:63-73`: 92 root entries = 89 task dirs + 3
files; 109 entries = 108 dirs + one `task_conflict.json`), a *partial* field-coverage finding for axis H
(`:49-53`: at the pin, 1 of 89 task dirs carries `schema_version` and `difficulty` but neither time
baseline; 6 lines across 3 tasks use integer literals where the schema elsewhere uses floats), and the
per-benchmark axis map (`:75-82`).

**What remains open in the same bullet, so the rows must not imply it:** the bullet asks for "*scoring
code*" as well. The entry reads documentation, task-package schema and a dated release gate; on
Terminal-Bench 2.0 it claims A, B, C, D, F, G and leaves J open with **no** grader-isolation claim
(`:77-78`), it derives axis E only from S078 (`:30`, `:79-80`), and it mentions the Toolathlon
`evaluation/` directory as *shipping beside the task* without reading it (`:54-55`). Scoring-code
execution therefore stays frontier.

**Bullets untouched** (adjacent, not covered): `corpus/README.md:272` (contamination transparency cards),
`:273` (judge calibration inward), and the endpoint/wiki bullets below them. Axis G is a canary-practice
observable and self-limits at `…checklist.md:89-90` ("G reads a maintainer's canary practice; it is not
a detector, and a canary's absence is not evidence of contamination").

---

## (c) The coverage-map row — landed, plus the five wording cells it must not cross

The three rows the round needed are now in the tree (line + quote so a later shift is recoverable):

| Row | Location | Content that matters for scope |
|---|---|---|
| Index row | `corpus/README.md:64` — `\| \`knowledge/benchmark-task-validity-checklist.md\` \| Ten-axis task-validity checklist …` | carries "counts re-derived, not copied; **not task validity, contamination measurement or model performance**" |
| Coverage-map row | `corpus/README.md:249` — `- **Benchmark task-validity instruments**: covered at primary-document synthesis depth (round 29 attempt 2, 2026-10-25)` | carries "Moves the round-24 frontier bullet from unopened lead to a checklist whose axes each name an artefact and a locus. **Not deployment config, not runtime task validity, not contamination measurement.**" |
| Frontier discharge | `corpus/README.md:271` — `- *Partly discharged round 29 attempt 2 (2026-10-25):*` | carries "supersedes only the `unopened leads` phrase for those three sources; contamination-transparency cards, runtime task validity and hosted judges remain open" |

**Verdict on the mandated exclusions:** the three required negatives are present and correctly worded —
deployment config (`:249`), runtime task validity (`:249`, `:271`), contamination measurement (`:64`,
`:249`). No row claims certification, judging, or a live run. The round-28/29 discharge lines
(`:349-352`, `:376-379`) are neither erased nor overwritten.

**One sentence for the record — the entry must not claim deployment config, runtime validity, or
contamination:** each is carried as open by `PROVINCE.md:208-211`, `corpus/README.md:349-352`/`:376-379`,
and `corpus/README.md:240` + `:272`, and the entry itself disclaims all three at `…checklist.md:86-90`
plus model performance at `:91-92`.

**Residual wording cells (not violations, but the row is the durable trace):**

1. Neither row nor entry states the *extends* relation (Q6) — see F1.
2. Neither row carves out **scoring code / grader execution** — see F5. `:249`'s "Moves the round-24
   frontier bullet from unopened lead" reads as wider than the entry's own evidence because the bullet
   names both specs *and* scoring code.
3. `:64`'s "read from four maintainers' own artefacts" plus the entry's "Four benchmark maintainers"
   (`:13-14`) and "Four maintainers were opened" (`:93`) is four *organisations* across **three**
   benchmark families (harbor-framework/S077, scaleapi/S078, laude-institute/S079+S090, hkust-nlp/S080)
   — see F4.
4. `:249` should say "not grader execution" beside "not runtime task validity", and must not convert
   the entry's "a reviewer **can** re-derive the release" (`:79-80`) into "the lane re-derived/re-ran the
   release gate". The only lane-executed check in scope is the count re-derivation (`:63-73`).
5. `:249` does not name the row it extends (`corpus/README.md:246`) — the cheapest place to satisfy Q6 if
   the entry itself is not edited.

---

## Findings (severity order)

### F1 — MEDIUM (admission, Q6): the entry still names no existing entry or coverage row it extends
`corpus/QUALITY.md:50-52`: "The entry names the existing entry or coverage row it extends."
`grep -n "extend\|agent-time-horizon\|Extends" corpus/knowledge/benchmark-task-validity-checklist.md`
→ **rc=1, no match** (re-verified on the current 97-line file). `…checklist.md:11-16` cites only the
Frontier text. Nearest owner row is `corpus/README.md:246` (S005/S006 task-validity digest).
A coverage row saying "Extends …" does not repair Q6 — Q6 binds the entry. Fix: one sentence naming
`knowledge/agent-time-horizon-and-task-validity.md` and stating the WebArena rows (`:347`, `:374`) are
adjacent rather than extended.

### F2 — MEDIUM (coverage precision): the shipped discharge is wider than the evidence on "scoring code"
`corpus/README.md:249` ("Moves the round-24 frontier bullet from unopened lead") and `:271`
("supersedes only the `unopened leads` phrase for those three sources") versus the bullet at `:270`
which names "the primary specs **and scoring code**". No scoring code was read: the entry's Terminal-Bench
row refuses axis E and leaves J open (`…checklist.md:77-78`), axis E is S078-only (`:30`, `:79-80`), and
the Toolathlon `evaluation/` directory is described as shipping, not opened (`:54-55`).
Fix: add "the specification/documentation half; scoring code and grader execution remain open" to `:249`
and/or `:271`.

### F3 — LOW (consistency/operability): entry recheck and registry recheck disagree, and five rows are due on landing day
Entry: `recheck: 180d … (next due 2027-04-23)` (`…checklist.md:6-7`). Registry, all five rows:
`recheck=2026-10-25`, `opened=2026-10-25`, `status=mined`,
`used-by=corpus/knowledge/benchmark-task-validity-checklist.md` (`corpus/SOURCES.md:100-104`), produced by
the gate's prose-normalization (`plans/sources_adopt.py:149-153`). Observed:

```
$ ./scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin --today 2026-10-25 kengaku-shokunin | tail -5
kengaku-shokunin	overdue	S090 0d recheck=2026-10-25 opened=2026-10-25
kengaku-shokunin	overdue	S080 0d recheck=2026-10-25 opened=2026-10-25
kengaku-shokunin	overdue	S079 0d recheck=2026-10-25 opened=2026-10-25
kengaku-shokunin	overdue	S078 0d recheck=2026-10-25 opened=2026-10-25
kengaku-shokunin	overdue	S077 0d recheck=2026-10-25 opened=2026-10-25
```

`census=ok` is unaffected (`validate` → exit 0, final line `kengaku-shokunin  ok  …/corpus/SOURCES.md`;
only pre-existing W04 warnings), and `corpus/lessons/round-29.md` §Attempt 2 states the ISO-date choice
deliberately ("each row's own `recheck` is that ISO date"). So this is a *decidable* inconsistency rather
than a defect of fact: `180d` in the five staged cells (a valid cadence is passed through by
`plans/sources_adopt.py:149-151` and accepted by `scripts/sources-census.sh:663-666`) would make registry
match entry and put the next due at 2027-04-23.

### F4 — LOW (coverage wording): "four maintainers" reads as four benchmarks
`corpus/README.md:64` ("read from four maintainers' own artefacts"), `…checklist.md:13-14`,
`…checklist.md:93`. Count: five rows, four organisations, **three** benchmark families
(S077 and S090 both concern Terminal-Bench). Fix: "three benchmark families" wherever the row's reader
could infer benchmark count.

### F5 — LOW (already satisfied — kept as the audited cell): contamination must stay out
`corpus/README.md:64` and `:249` both exclude contamination measurement; `…checklist.md:89-90` refuses
detector semantics; the card bullet `corpus/README.md:272` is untouched. No action; recorded so a later
editor does not "strengthen" axis G into a contamination claim.

### F6 — LOW (for the critic, not a scope defect): axis E's harness sentence is reasoning, not evidence
`…checklist.md:58-61` generalises about "a harness that runs the verifier in a shared environment by
default". Only S078's locked protocol is evidenced. The sentence is defensible as a caution and unsafe as
a quotation; if it is ever cited outside the entry, it must carry "reasoning step".

### Resolved during review (F7, withdrawn)
`indexed=0` when I first measured it — `plans/adoption_check.py:75-76` matches only the literal
``| `knowledge/<name>` |`` so a coverage bullet alone cannot satisfy it. A sibling landed the index row
(`corpus/README.md:64`) while I was writing; the counter now prints the frozen target line verbatim with
`census=ok` and exit 0. Withdrawn: nothing to fix.

## What I verified vs what I did not

Executed by this seat: the counter twice (before: `entries=1 indexed=0 … exit 1`; after: the exact frozen
line, exit 0) including the fleet-census subprocess; `python3 plans/sources_adopt.py --selftest` →
`SELFTEST cases=10 failed=0`, exit 0; fleet `validate` on the lane → exit 0/`ok`; fleet `overdue` on
2026-10-25 → five `0d` lines; row cell values for S077-S080/S090 (11 columns each, `status=mined`,
`opened=recheck=2026-10-25`, single `used-by`); absence of any extend/WebArena reference in the entry;
S077 identity by direct fetch of the pinned raw file at commit `e67a2cb7…` (`HTTP 200`, 461 lines;
`#### check-canary` heading line 93, the quoted canary sentence line 95, `Oracle Validation — Solution
passes all tests` line 244, `Adversarial reward-hack detection` line 31).

Not verified here (owned by other seats): quote fidelity and ≤25-word bounds (RevQuoteS077/S078/S079/S080/
S090); the 92/89 and 109/108 counts (Src seats); selftest mutant adequacy (FixtureMutations/GateAudit);
completeness of the Q10/Q13 report set (GateAudit). I give no admission verdict — this report advises
the L1.
