# ConnectorOverlap — round 97 province, overlap and coupling scan

Seat: connector (leaf). Axes: **coverage**, **calibration**. Read-only on the lane; no production
edits, no commits, no task calls. Scratch clone and venv under
`/fast/scratch/hyaku/kengaku-r97/ConnectorOverlap/` (removed after receipts were copied).
Receipts: `.ufo/waves/round-97/w1/ConnectorOverlap/`.

Measured tip `T = f1083da60e7ff6b88f7420aae7424f7762d14700`; freeze
`F = 8d9d271306c4e7e2d586e51cd546652249d286cb`; BASE `4992cd0e`.

## Verdict

**PROVINCE holds for both claims; neither kill rule is triggered.** I reproduced both frozen
predicates independently from a clean `--shared` clone detached at T, with my own grader venv
(CPython 3.13.16, rdflib 7.1.4, pytest 8.4.1), and audited the two instruments' scope against the
claims and against each other. C1 passes all nine legs and the TARGET line byte-for-byte; C2 passes
with 44 kind cells changed and nothing else. The findings below are round-98 routes, not repairs:
none of them makes a frozen predicate false at T.

## Evidence

### C1 — coverage (pass, reproduced)

Command (clone root, cwd = clone root as the counter requires):

```
python3 plans/round97_c1_replay.py --lane . --rev f1083da6… --work <scratch>/rerun \
  --grader-venv <scratch>/G
```

Observed (`ConnectorOverlap/c1-replay-at-T.txt`, rc 0, 19.4 s):

```
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass
TARGET executed_rows=41 member=sparql-university cells=file-artifact:32 set_contains_base=1 located=1 executed=1 cases=18 legs=72 mismatches=0 defects=0
PREDICATE R97-C1 pass
```

Independent accounting from the ledger at T (`province_walk.json`): 88 members, 41 executed,
76 `file-artifact`, 32 of them executed, executed set ⊇ BASE's plus `sparql-university`, none
removed. `F..T` changes exactly four files: `SKILL.md`, `corpus/SOURCES.md`,
`plans/grader-population-ledger.json`, `corpus/evidence/round97/sparql-probe.txt`. The three
candidate-byte shas at T equal the frozen candidate-bytes table (`739fb58b…` SKILL, `567a26bb…`
ledger, `c54a0ece…` SOURCES); the receipt sha is `acfaacf7…` (not tabled by design). All ten
frozen instruments hash to their tabled values at T.

The replay's own controls behave as declared: do-nothing fails L1/L2/L3/L5/L6/L7/L9; forged receipt
fails L6 only (`obs=36 want=18`); wrong cwd exits 2 (`DEFECT SETUP cwd … is not the lane root`).

**Independent graph walk** (`graph-walk.txt`, rdflib over
`tests/university_graph_test.ttl`): six full professors; per-department enrolled counts are
Alex Dimakis 11 (US) + 0 + 0, Aristotle Tympas 12 (GR), Chrysoula Zerva 0 + 12 (GR), Giorgos
Stamou 12 (GR) + 0, John Smith 7 (US), Marie Dubois 6 (FR). The reference four are exactly the
per-department `>10` set; the aggregate set is identical (only one department per professor has any
students), and the no-EU set is identical (the only non-EU professor, John Smith, fails `>10`
anyway). This independently confirms C05, C09 and the C06 mechanism without trusting the probe's
own case table.

### C2 — calibration (pass, reproduced)

```
python3 plans/round97_gate_selftest_census.py --lane . --rev f1083da6…
```

Observed (`c2-census-at-T.txt`, rc 0): `ROWS base=168 rev=171 removed=0 duplicate=0
cells_changed=0`; `GATES total=84 with_selftest=84 without=0 demoted_with_selftest=0
scripts_changed=0`; `MISMATCH_TOTAL n=0`; `PREDICATE R97-C2 pass`.
`--selftest --work <scratch>` → `SELFTEST cases=8 failed=0`, rc 0 (`c2-selftest.txt`).

Independent cell accounting (`province_walk.py`, reads `git show` only): exactly 44 rows differ
between BASE and T, every one `gate → probe`, no other cell differs anywhere in the registry, and
the 44 names are set-equal to the BASE receipt's `MISMATCH` list. Three rows were added (C1's two
`probe` rows, C2's one `gate` row); one paragraph was added at `SKILL.md:773`. The SKILL diff is
therefore exactly: 44 kind cells + 3 new rows + 1 class-table cell (`SKILL.md:74`) + 1 paragraph,
with no other prose and no `.py` change.

**Detector audit of the 44.** I scanned every demoted entry script at BASE for any self-invocation
spelling, not only the census's six regexes. All 44 are true positives: the only mentions are
output text (`SELFTEST green failed`, `SELFTEST cases=…`), a quoted SOURCES row
(`plans/round41_c1_verify.py:194`), or a subprocess call to *another* tool's `--selftest`
(`round46_c2_verify.py:193` calls `plans/anchor_line_check.py --selftest`). No demoted script has
its own `--selftest`/`--self-test`/`run_selftest` entry point. This corroborates the ExecC2
assignment independently.

**Detector shape (finding F3, non-blocking).** The detector is a lexical presence check, and the
lane already named that failure mode in round 72 (`corpus/lessons/round-72.md:126`, "a presence
check read as an attribution check"; `corpus/knowledge/instrument-registry-derivation.md:41`).
Three surviving gates — `round85-c1-replay`, `round86-c1-replay`, `round86-c2-repin` — are counted
as "with self-test" only because of the incidental tuple literal
`for flag in ("--selftest", …): parser.add_argument(flag, …)`
(`plans/round85_c1_replay.py:567-569`). They *do* have a genuine self-test, so the conclusion is
right, but a conforming gate that registers the flag indirectly on separate lines
(`FLAGS = ("--selftest",)` then `add_argument(FLAG)`) would be a false negative and would be
demoted. The census's `--selftest` fixtures do not cover that shape: `WITH` is the literal
`p.add_argument("--selftest", …)` (`plans/round97_gate_selftest_census.py:167`). No false positives
were found among the 84 gates at T (my classifier: 81 strong matches, 3 indirect-but-genuine,
0 prose-only).

### Coupling C1 ↔ C2 (finding F1/F2, non-blocking)

1. **Shared candidate byte.** `SKILL.md` has one sha in the candidate-bytes table (`739fb58b…`)
   covering both claims' edits. A defect in either claim's SKILL edit fails *both* claims' "C lands
   exactly these three files" clause. The `c1-only`/`c2-only` controls use fixture commits with
   different SKILL bytes, so they demonstrate **instrument** separability, not **candidate-byte**
   separability.
2. **Predicate string.** C2's frozen line names `ROWS base=168 rev=171`; the `c2-only` control
   prints `ROWS base=168 rev=169` (`controls/c2-c2only.txt`) and still exits 0. The instrument is
   separable; the declared predicate *string* embeds C1's two new rows. At T the line is 171, so
   the claim is met, but a c2-only replay cannot reproduce the frozen line.
3. **Semantic dependency.** C2's `MISMATCH_TOTAL n=0` at T depends on C1 registering its two new
   rows as `probe` (neither has a self-test; typed `gate` they would be two MISMATCHes). The
   c2-only fixture reaches `GATES total=84 with_selftest=84` because C1's rows are *absent*, not
   because they are correctly typed.
4. **Disjoint otherwise.** C1's class cell is at `SKILL.md:74`, outside the registry section that
   starts at `SKILL.md:592`; the census reads only rows after the heading, which is why
   `cells_changed=0` cannot see C1's class edit. C2 does not read the ledger; C1's L7 does not read
   SKILL. The 44 kind rows and C1's two rows are disjoint.

### Second-order effect on the historical sweep (finding F5)

`plans/round82_c3_sweep.py --check` is red at both revisions, but the flip adds exactly one defect
line (`r82-sweep-at-BASE.txt` 27 defects → `r82-sweep-at-T.txt` 28):

```
BASE: HISTOGRAM-CLASS file-artifact declared=18 recomputed=31 ; TARGET members=40 …
T:    HISTOGRAM-CLASS file-artifact declared=18 recomputed=32 ; STATUS-LINE-MISSING sparql-university
```

No verdict change (already red; the SKILL round-83 boundary paragraph declares this instrument
historical). It is not in the pre-freeze harm list, and it does not need to be: the delta is the
ledger flip itself, which the claim owns.

## Cross-source pattern: labels as quotients

The round's four named elements — literal answer, set comparison, unused EU criterion, taxonomy —
are not four gaps. They are **one mechanism with six witnesses**: the lane records a *quotient* of
the object it claims to describe, and the quotient is invisible until an instrument compares it to
the un-quotiented bytes.

- `tests/test_outputs.py:70-79` builds `set[(professorName, sorted-countries)]` and asserts equality
  with `REFERENCE_RESULTS`. That single observation surface produces:
  - **C10 literal answer** — the query text is never inspected, only its output;
  - **C11 set comparison** — duplicates collapse (`8 rows, 4 distinct` passes);
  - **C12 extra column** — only two attributes are read, so an extra projection is invisible;
  - **C05 unused EU criterion** — the reference set is invariant to criterion 2 (my graph walk: the
    only non-EU professor fails `>10` anyway);
  - **C06 NOW() date** — Student17's 2026-06-12 graduation is in a 6-student department, so the
    reference-date literal is unobservable;
  - **C09 per-department vs aggregate** — every professor has at most one department with students,
    so the instruction-faithful reading and the solution's aggregate `HAVING` are indistinguishable.
- **Taxonomy (`SKILL.md:74`)** is the same quotient applied to the evaluation surface. The
  `file-artifact` row says "the grader then reads and parses those files itself". For
  `sparql-university` the grader *executes* the artifact against a graph the agent never sees:
  `test_outputs.py:12` reads `/tests/university_graph_test.ttl`; the probe binds the capture's
  `tests/` read-only at `/tests` (`plans/round97_sparql_probe.py:285`) and the grader evaluates
  `/app/solution.sparql` against it (`:167-168`); the agent graph names `Orfeas Menis` and
  `Pepe Attanasio`, the test graph replaces them (C17). The class count (32 of 76) is true; the
  class *description* is a quotient of the member's province.
- **C2** is the same quotient on the registry: `kind=gate` stood for a self-test capability the
  script's bytes did not expose. C2 un-quotients 44 rows — but with a *spelling* check, which is
  itself a quotient of the capability (F3).

So the two claims are one move in opposite directions: C2 repairs a false label; C1 admits a true
count under a label that under-describes the member. That asymmetry is the connector finding.

## Proposed move (one, bounded)

**Round 98: a `hidden-input` surface census — apply C2's declared-vs-observed method to the
evaluation surface, with C1's new member as the first witness.**

- New read-only instrument `plans/round98_surface_census.py` (reads `git show REV:` only, like the
  C2 census). For each ledger member with `status=executed`, read its registered probe's sandbox
  bind recipe and the grader's data paths, and classify the observed surface: `bytes` (grader parses
  the artifact), `bytes-executed` (grader evaluates it), `hidden-input` (the verdict depends on a
  path the agent cannot see), `stdout`, `network`, `process`, `timing`, `crypto`, `numeric`.
- Add an **additive per-member `surface` key** to the ledger, set from the census observation, not
  from prose. Do **not** add a `classes` token: C1's L7 compares `member["classes"] ==
  ["file-artifact"]` exactly, so a second class token would break a frozen predicate; a new
  top-level key is ignored by L7.
- Predicate: `SURFACE members=41 declared=… observed=… unknown=… mismatch=0`. Red-before at T:
  `sparql-university` declared `file-artifact:bytes`, observed `bytes-executed+hidden-input`.
- Detection rule: a member whose probe binds a capture path under `/tests` that is not staged in
  `/app`, and whose grader reads it, is `hidden-input`; a probe with no parseable bind recipe is
  `unknown`, never `false`. The behavioral cross-check is the case-table witness (C17), not the
  bind path alone.
- Kill rule: a member whose declared surface omits an observed surface, or an `unknown` counted as
  declared.

**Axes.** Coverage: adds a countable property across the 41 executed members — how many graders
depend on agent-invisible inputs — that the population census cannot currently see. Calibration:
makes the class/ledger self-assessment falsifiable by the same declared-vs-observed method C2 uses,
and would have caught the `file-artifact` under-description that C1's own C17 witness demonstrates.

**No harm.** New file, read-only, no frozen instrument edited, no closed row re-typed, no class
token added, round-97's member row untouched (Q79). No existing predicate changes.

## Risks

- **Probe-specific binds.** Not every probe uses bwrap; `unknown` must be a first-class outcome or
  the census repeats the quotient error it measures.
- **Exact-key validators.** Before landing the `surface` key, check `round82_c1_plans_registry.py`
  and `round78_c1` for exact-key or exact-cell assertions on ledger rows.
- **Syntactic hidden-input detection.** A grader that reads a hidden input via an env var or a
  generated file would be missed; the census must report `unknown` and cite the case-table witness,
  never claim completeness.
- **Class token temptation.** Adding `hidden-input` to `classes` would break C1's L7; the key must
  stay outside `classes`.

## Verification

1. C1: `cd <clean clone at T> && python3 plans/round97_c1_replay.py --lane . --rev T --work
   <scratch> --grader-venv <G>` → the three lines above, rc 0 (reproduced: 19.4 s).
2. C2: `python3 plans/round97_gate_selftest_census.py --lane . --rev T` → four lines, rc 0;
   `--selftest --work <scratch>` → `SELFTEST cases=8 failed=0`.
3. Proposal red-before: a fixture where `sparql-university` declares `surface: bytes` and the
   census prints `SURFACE … mismatch=1`; green: the declaration `bytes-executed+hidden-input`.
4. Proposal harm check: re-run the registry and ledger gates named in the round-97 harm list at the
   fixture tip; every exit code and DEFECT line must be unchanged, as in
   `controls/harm-pre-freeze/`.

## Sibling overlap

Sibling seats were in flight at read time (their `w1/` directories were empty); this report does not
depend on them. Overlap with the ExecC2 assignment is deliberate and corroborative: I independently
verified the 44 demotions are true positives. The connector's marginal contribution is the
detector's false-negative shape (F3), the C1/C2 couplings (F1/F2), and the taxonomy/surface finding
that neither executor's scope covers.

## Receipt index (`.ufo/waves/round-97/w1/ConnectorOverlap/`)

| file | what |
|---|---|
| `c1-replay-at-T.txt` | independent C1 replay from a clean clone at T, rc 0 |
| `c2-census-at-T.txt` | independent C2 census at T, rc 0 |
| `c2-selftest.txt` | C2 `--selftest`, 8/8 |
| `province_walk.py` / `province_walk.json` | read-only cell accounting, detector audit, ledger counts |
| `graph_walk.py` / `graph-walk.txt` | rdflib walk of the hidden graph (C05/C09/C06 mechanisms) |
| `r82-sweep-at-BASE.txt` / `r82-sweep-at-T.txt` | historical sweep delta (27 → 28 defects) |
