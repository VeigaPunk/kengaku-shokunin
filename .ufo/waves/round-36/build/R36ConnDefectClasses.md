# R36ConnDefectClasses — cross-round routed-defect class map (kengaku round 36, wave 1)

Seat: connector. Scope: map every routed defect in the round-29…round-35 non-author spot-checks to a
class, count recurrences, propose `recurrence_of` values for the four rows of
`corpus/defects-round35.jsonl`, flag recurring classes with no standing check, and say what the C1
battery's 14 fixtures cover of each. Read-only: I edited no lane file, ran no lane counter of record,
and invoked no runtime other than the read-only probes described in §6.

Sources read in full: `corpus/lessons/round-{29,30,31,32,33,34,35}-verifier-spotcheck.md`;
`corpus/defects.jsonl`; `corpus/defects-round35.jsonl`; `plans/defect_ledger.py`;
`plans/round36_c1_verify.py`; `plans/pkg_gate.py`; `plans/pkg-spec-r35.json`; `considerthese/2026-10-25.md`;
`corpus/QUALITY.md` (Q23/Q24); `corpus/lessons/round-35.md`; `SKILL.md` §Gate/probe registry.

---

## 1. Class map

Two granularities, both computed from the routed-defect sections (§5) of the seven spot-checks:

* **bullet level** — 35 routed bullets (r29:5, r30:8, r31:6+1 carried-debt bullet, r32:4, r33:2,
  r34:5, r35:5 lane-fixable + 1 operator item). r32's first bullet names five distinct defects
  (R1,R2,R5,R6,R7) and r31's carried-debt bullet names five, so bullet count understates defect count.
* **defect level** — 43 lane-fixable defect items (r29:5, r30:8, r31:10, r32:8, r33:2, r34:5, r35:5).
  r31's fifth carried-debt item ("wave-report sealing … routed to the protocol lane", `:168`) is not a
  lane-fixable defect and is excluded; r35's item 6 (SHONEN, operator-owned) is excluded.

23 distinct classes over the 43 defect items. 10 classes recur (≥2 items); 13 are singletons.

| # | class | items | rounds | routed items (file:line) |
|---|---|---|---|---|
| 1 | count-misstatement | 4 | 29,30,33 | r29 D3 (`:128`) · r30 §5-3 (`:171`) · r30 §5-8 (`:194`) · r33 (a) (`:100`) |
| 2 | untracked-work | 4 | 29,30,32,34 | r29 D4 (`:130`) · r30 §5-6 (`:184`) · r32 (`:90`) · r34 D1 (`:75`) |
| 3 | stale-record | 4 | 30,31,32 | r30 §5-1 (`:163`) · r30 §5-2 (`:168`) · r31 carried (`:168`) · r32 R6 (`:87`) |
| 4 | counter-accepts-junk | 4 | 31,32,35 | r31 carried "C2 counter survivors" (`:169`) · r31 carried "C1 kill-rule branch unreachable" (`:169`) · r32 R7 (`:87`) · r35 §5-1 (`:86`) |
| 5 | scope-misstatement | 3 | 29,30,34 | r29 D2 (`:125`) · r30 §5-5 (`:177`) · r34 D4 (`:78`) |
| 6 | report-before-commit | 3 | 30,31,32 | r30 §5-7 (`:190`) · r31 D2 (`:151`) · r32 R2 (`:87`) |
| 7 | receipt-path-mismatch | 2 | 29,31 | r29 D1 (`:120`) · r31 D3 (`:154`) |
| 8 | gate-row-omission | 2 | 31,35 | r31 D4 (`:159`) · r35 §5-4 (`:89`) |
| 9 | phantom-hash | 2 | 31,32 | r31 D1 (`:149`) · r32 R1 (`:87`) |
| 10 | seat-registry-mismatch | 2 | 31,32 | r31 D5 (`:162`) · r32 R5 (`:87`) |
| 11 | registry-relation-asymmetry | 1 | 29 | r29 D5 (`:133`) |
| 12 | duplicate-text | 1 | 30 | r30 §5-4 (`:174`) |
| 13 | pre-registration-ordering | 1 | 31 | r31 carried "claims freeze not committed before data" (`:168`) |
| 14 | locator-drift | 1 | 31 | r31 D6 (`:165`) |
| 15 | id-collision | 1 | 32 | r32 C1 (`:88`) |
| 16 | raw-payload-not-retained | 1 | 32 | r32 C3 (`:89`) |
| 17 | control-prose-mismatch | 1 | 33 | r33 (b) (`:100`) |
| 18 | scratch-bloat | 1 | 34 | r34 D2 (`:76`) |
| 19 | manifest-omission | 1 | 34 | r34 D3 (`:77`) |
| 20 | false-refusal | 1 | 34 | r34 D5 (`:79`) |
| 21 | working-tree+token-cooccurrence | 1 | 35 | r35 §5-2 (`:87`) |
| 22 | narrow-scratch-roots | 1 | 35 | r35 §5-3 (`:88`) |
| 23 | live-reachability-dependency | 1 | 35 | r35 §5-5 (`:90`) |

All 10 recurring classes recur across **≥2 distinct rounds** (none is a same-round double).

---

## 2. The blocker: recurrence is prose, not a key

The persistent ledger cannot answer "does this class recur?" today:

* `corpus/defects.jsonl` holds 5 rows (all `R34-*`); `corpus/defects-round35.jsonl` holds 4 (all
  `R35-*`). Their `class` strings are **9 distinct values over 9 rows** — no class repeats.
  Measured: `python3 -c` over both files → `classes with >1 row: NONE`; `R35 rows whose class has a
  prior row with same class: NONE`.
* `recurrence_of` is free prose. `plans/defect_ledger.py:119` reads only `corpus/defects.jsonl`;
  `plans/round36_c1_verify.py:41` (`LEDGER_REL`) and `:335` read only `corpus/defects-round35.jsonl`.
  **No single command re-runs all 9 rows.** `corpus/QUALITY.md:275-282` (Q23) claims "the ledger
  checker re-runs every row at every tip"; `corpus/README.md:407,417` repeats it per file. The claim
  is true per file, false for the ledger as a whole.
* Only 9 of the 43 defect items across rounds 29–35 have a ledger row. Rounds 29–33 contributed 24
  routed defects and **none** is in either ledger file (`grep -n "R3[123]-" corpus/defects*.jsonl` →
  only the `R34-D1` row's `recurrence_of` prose mentions `R33-N1`).
* `corpus/QUALITY.md:291` (Q23 limits) and `corpus/lessons/round-35.md:33` both state plainly that
  considerthese proposal 2(b) — "blocks pre-registration when a class recurs twice" — is **not
  implemented**: "`recurrence_of` is recorded, not enforced; checks are per-defect functions, so a new
  routed defect still needs code."

So "recurs twice" is currently undecidable from bytes: the class vocabulary does not repeat, and the
only linkage is prose that mixes two id namespaces (see §3).

---

## 3. Proposed `recurrence_of` for the four `corpus/defects-round35.jsonl` rows

Proposed values (the L1 owns the edit; the file's `id`/`class`/`check` names are frozen by
`plans/round-36-claims.md` §"Frozen instruments" and stay untouched):

**R35-D1 — class `counter-accepts-junk`**
* current: `"R34-D4/R34-D5 (labelled-but-false lines passed the frozen ledger checks; plans/round35_hardening.py H1-H6 post-hoc)"`
* problem: `R34-D4` and `R34-D5` are ledger **rows** whose `class` fields are `scorecard-misattribution`
  and `false-refusal-reason` — neither is `counter-accepts-junk`. A class-keyed recurrence detector
  therefore finds no predecessor, even though the class genuinely recurred three times (r31, r32, r35).
* proposed: `"R31-carried-debt 'C2 counter survivors' + 'C1 kill-rule branch unreachable' (corpus/lessons/round-31-verifier-spotcheck.md:169) + R32-R7 'Correct counter blind spots identified by round-32 mutation evidence; do not present a partial receipt or selftest as closure' (corpus/lessons/round-32-verifier-spotcheck.md:87) + round-34 mutation survivors R35MutC1Quotes M4 / R35MutC1V4V5 M8 (corpus/lessons/round-35.md:28) — class counter-accepts-junk, 3 earlier rounds; R34-D4/R34-D5 are the checks' row ids, their class fields are scorecard-misattribution / false-refusal-reason"`

**R35-D2 — class `working-tree-and-token-cooccurrence-checks`**
* current: `"R34-D1 (working-tree check) and R34-D4/R34-D5 (token co-occurrence)"`
* problem: `R34-D1`'s row class is `uncommitted-round-work`; the *check* `r34_d1` is the working-tree
  read and the *checks* `r34_d4`/`r34_d5` are the token matchers — the prose conflates row ids with
  check names. It also misses the idiom's origin: `near()` token co-occurrence is introduced in
  `plans/round32_defects.py` (10 `near(` sites) and carried by `plans/round33_defects.py` (9 sites).
* proposed: `"R34-D1 / r34_d1 (working-tree read: git ls-files --others over a subtree, plans/defect_ledger.py:37-45) + r34_d4 / r34_d5 (token co-occurrence: plans/defect_ledger.py:69-118) — idiom introduced in plans/round32_defects.py near() x10 and plans/round33_defects.py near() x9; 3 earlier rounds; the R34-D* row ids name different classes (uncommitted-round-work / scorecard-misattribution / false-refusal-reason)"`

**R35-D3 — class `narrow-scratch-roots`**
* current: `"R34-D2 (committed scratch mirrors; roots named too narrowly)"`
* keep the anchor, but it is one instance short of the truth: the same narrow-root defect survives
  inside the check that closes it (see §5, finding N1), and the class also recurred in r35's own
  measurement method (21 vs 28).
* proposed: `"R34-D2 (committed scratch mirrors; roots named too narrowly, corpus/defects.jsonl) + the round-36 check r35_d3 itself keeps a round-scoped regex NESTED_RE ^\\.ufo/waves/round-3[0-9]/.*/\\.ufo/waves/round- (plans/round36_c1_verify.py:42) which matches 0 committed paths at the tip while 912 committed round-28 nested wave paths remain invisible to it — the same narrow-root class recurring inside its own closure; plus r35's own 21-vs-28 method discrepancy (corpus/lessons/round-35-verifier-spotcheck.md:88)"`

**R35-D4 — class `gate-row-omission`**
* current: `null`
* problem: the class **did** recur, one round earlier, in almost the same shape: r31 D4
  ("`plans/sources_adopt.py` … has no row in `SKILL.md` §Gate/probe registry",
  `corpus/lessons/round-31-verifier-spotcheck.md:159-161`). `null` understates it.
* proposed: `"R31-D4 (plans/sources_adopt.py had no row in SKILL.md §Gate/probe registry, corpus/lessons/round-31-verifier-spotcheck.md:159-161) — same class, second occurrence; r35-D4's own instance is the round-36 lesson's ## Gate row citing only the own-work locator reason and omitting the 38-vs-37 denominator reason (corpus/lessons/round-35-verifier-spotcheck.md:89)"`

---

## 4. Recurring classes with no standing check

Definition used (stated so the count is reproducible): a class is **covered** if a check exists that
would fire on a *future* occurrence of that class (a check bound to one named artifact does not cover
its class). "Standing check" = a check that re-runs at every tip in a tool the tip actually runs
(`plans/defect_ledger.py`, `plans/round36_c1_verify.py`, `plans/pkg_gate.py`, `plans/sources_adopt.py`,
`plans/state_check.py`, `plans/registry_check.py`, `grader.py`) or a registered `SKILL.md` §Gate row.

| class | items | standing check? | verdict |
|---|---|---|---|
| count-misstatement | 4 | none — no check re-derives a number stated in one artifact from the artifact it names | **uncovered** |
| stale-record | 4 | none — no check re-derives a `LOG.md`/lesson claim against the bytes it describes | **uncovered** |
| scope-misstatement | 3 | `r34_d4` binds one SCORECORD line, `r35_d4` binds one lesson `## Gate` line — instance-scoped, not class-scoped | **uncovered** |
| report-before-commit | 3 | none — `plans/round32_defects.py:45-46` and `plans/round33_defects.py:41-42` read the fleet report but are one-round, unregistered scripts; no standing tool reads `/home/vgpnk/Projects/shokunin/.ufo/reports/` | **uncovered** |
| receipt-path-mismatch | 2 | `pkg_gate.c_receipt`/`c_captures` pin the *package* receipt's digest and manifest, but no check verifies that a path cited by a report/lesson/receipt resolves | **uncovered** (package sub-surface covered) |
| gate-row-omission | 2 | `r35_d4` binds the round-36 lesson row; nothing checks that every gate has a `SKILL.md` §Gate row | **uncovered** |
| phantom-hash | 2 | `plans/round32_defects.py:12` / `plans/round33_defects.py:17` are one-round scripts with no standing row | **uncovered** |
| seat-registry-mismatch | 2 | none | **uncovered** |
| untracked-work | 4 | `plans/round36_c1_verify.py:277` (`r35_d2`, whole-lane `git ls-files --others`) + `plans/defect_ledger.py:37` (`r34_d1`, subtree) | covered |
| counter-accepts-junk | 4 | `plans/pkg_gate.py` 10 clauses + `plans/round36_c1_verify.py` 14-fixture battery (r35_d1) | covered |

**8 of the 10 recurring classes have no standing check.** The two that do are exactly the two round 36
built. Note the asymmetry: the classes that recur most (count-misstatement, stale-record) are the ones
no tool re-derives, while the classes round 36 hardened are the ones with instruments.

Two further gaps, both verified in the lane tree:

* `plans/defect_ledger.py` — the standing checker that owns the round-34 ledger rows and the standing
  half of Q23 — has **no row in `SKILL.md` §Gate/probe registry**. The registry's 13 rows are
  `hermetic-grader`, `coverage-census`, `interval-reverdict`, `state-assertion-check`, `grader-perturb`,
  `gate-timing`, `benchmark-spec-audit`, `registry-reference-check`, `config-projection`,
  `sources-adopt`, `package-gate`, `round36-c1-battery`, `regex-log-probe`
  (`SKILL.md:564-576`); `grep -c defect_ledger SKILL.md` → 1, and that one hit is inside the
  `package-gate` row's prose, not a row of its own. `plans/round3[0-3]_defects.py` likewise have no rows
  (`grep -c "round3._defects" SKILL.md` → 0). This is the **gate-row-omission class (r31 D4, r35 D4)
  recurring a third time inside round 36 itself**, on the very checker that owns the ledger rows.
* no round-36 tool runs `plans/defect_ledger.py` and `plans/round36_c1_verify.py` together, so the two
  ledgers never meet (§2).

---

## 5. Does the C1 14-fixture battery cover each recurring class?

Short answer: it covers **2 of 10** recurring classes fully, 1 partially, and **not at all** the other 7.
The battery is a package-gate battery; 6 of the 10 recurring classes live on surfaces the gate never
touches (a fleet report, a lesson cell, a `SKILL.md` registry row, a registry row count).

Fixture → class, as measured (§6): P1/P2/P3 (quote shape), P4 (teaches cells), P5 (stub probe),
P6 (untracked file), P7 (all-junk) are all one class — *counter-accepts-junk*. L1–L3 are the D4
correction line, L4–L6 the D5 erratum line: *scope-misstatement* / *false-refusal* /
*narrow-scratch-roots* shapes of those two lines only.

| recurring class | covered by the 14 fixtures? | note |
|---|---|---|
| counter-accepts-junk | **yes** | P1–P5, P7, L2, L3, L5, L6 — the class the battery was built for |
| untracked-work | **yes** (partly outside the fixtures) | P6 covers the package-root case; the lane-wide case is ledger check `r35_d2`, not a fixture |
| scope-misstatement | partial | L2/L3 catch mis-cited D4 lines; nothing covers r29-D2's scope overstatement or r30-5's entry overclaim |
| count-misstatement | **no** | P2 (eight copies of one quote) is a duplicate mutant, not a two-artifact count disagreement. No fixture makes two committed artifacts disagree about a number |
| stale-record | **no** | no fixture edits a `LOG.md`/lesson claim |
| report-before-commit | **no** | the fleet report is outside the lane; a package-root battery cannot see it |
| receipt-path-mismatch | **no** | and, worse, the two clauses that would catch it are battery-blind (§6) |
| gate-row-omission | **no** | no fixture asserts a `SKILL.md` registry row or a lesson `## Gate` completeness |
| phantom-hash | **no** | no fixture cites a non-existent commit |
| seat-registry-mismatch | **no** | no fixture compares a registry count to a report count |

### Finding N1 — 6 of 10 gate clauses are battery-blind (mutation-surviving)

Read-only probe of the shipped `plans/pkg_gate.py` against the frozen 14 fixtures. For each clause I
neutered it (`return True, "NEUTERED"`) in a temp copy and re-ran the 8 package fixtures:

```
NEUTER c_instruments      false_green=1 false_red=0 -> killed
NEUTER c_receipt         false_green=0 false_red=0 -> SURVIVES(battery blind)
NEUTER c_quote_shape     false_green=3 false_red=0 -> killed
NEUTER c_quote_verbatim  false_green=0 false_red=0 -> SURVIVES(battery blind)
NEUTER c_captures        false_green=0 false_red=0 -> SURVIVES(battery blind)
NEUTER c_sources         false_green=1 false_red=0 -> killed
NEUTER c_provenance      false_green=0 false_red=0 -> SURVIVES(battery blind)
NEUTER c_readme          false_green=0 false_red=0 -> SURVIVES(battery blind)
NEUTER c_clean_tree      false_green=1 false_red=0 -> killed
NEUTER c_rerun           false_green=0 false_red=0 -> SURVIVES(battery blind)
```

Clause-level firing map (which fixture drives which clause to DEFECT):
`P1(c_instruments)←P5,P7` · `P2(c_receipt)←NONE` · `P3(c_quote_shape)←P1,P2,P3,P7` ·
`P4(c_quote_verbatim)←NONE` · `P5(c_captures)←NONE` · `P6(c_sources)←P4,P7` ·
`P7(c_provenance)←NONE` · `P8(c_readme)←NONE` · `P9(c_clean_tree)←P6,P7` · `P10(c_rerun)←NONE`.

This is an **observation, not a judgment of C1**: C1's frozen predicate is
`FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`, and the shipped gate does meet it. The
point is that the *predicate* is a weaker claim than "the gate is correct on every clause", because
six clauses are never driven to failure by any fixture. The class this instantiates is
counter-accepts-junk's sibling — a check that passes because nothing exercises it. The frozen claims
already name this shape as its own limit (Q24: "a junk class no fixture occupies survives").

Concretely, `c_receipt`, `c_captures`, `c_quote_verbatim`, `c_provenance`, `c_readme`, `c_rerun` are
the clauses that would fire on **receipt-path-mismatch**, **manifest-omission**, **scope-misstatement**
and **live-reachability-dependency** — i.e. four of the ten recurring classes are, in principle, inside
the gate's reach and currently unexercised.

### Finding N2 — the narrow-root class recurs inside its own closure

`plans/round36_c1_verify.py:42` `NESTED_RE = r"^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-"`.
Measured at the current tip (`refs/heads/master`):

```
git ls-tree -r --name-only refs/heads/master | grep -cE '^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-'   -> 0
git ls-tree -r --name-only refs/heads/master | grep -cE '^\.ufo/waves/round-28/.*/\.ufo/waves/round-'         -> 912
git ls-tree -r --name-only refs/heads/master | grep -cE '/\.ufo/waves/'                                        -> 912
```

`r35_d3` counts only the round-3x window, so it reports `committed_nested_wave_paths=0` while 912
committed nested wave paths (recursive scratch mirrors under `.ufo/waves/round-28/scratch/…`, e.g.
`.ufo/waves/round-28/scratch/FSeparability/s038-only-control/.ufo/waves/round-25/build/AwkOracleExec.md`)
remain — the same artifact shape R34-D2 was about, invisible to the check that claims to close the
class. `plans/round-36-claims.md` discloses this as a named limit ("912 round-28 nested scratch paths …
also match `/.ufo/waves/` but not the spot-check's `round-3x` pattern … R35-D3 claims the 21 round-34
paths only"), so it is disclosed rather than hidden — but the *class* still recurs, one level down.

### Finding N3 — the battery cannot exercise "reads committed bytes"

`plans/round36_c1_verify.py:55-62` (`copy_package`) copies the package with `shutil.copy2(lane / rel, …)`
— the lane **working tree** — and the fixture repos are built index-only (`git init` + `git add -A`, no
commit; `plans/round36_c1_verify.py:140-147`), so `git show <rev>:<path>` cannot work inside a fixture
at all (verified in a scratch repo: `git show HEAD:f.txt` → `fatal: invalid object name 'HEAD'`, exit
128). The `working-tree+token-cooccurrence` class (R35-D2) therefore has no fixture that could
distinguish a working-tree read from a committed-byte read; the class is real but untestable by this
battery shape. `r35_d3` (`git ls-tree … BRANCH`) is the one committed-byte read in round 36.

---

## 6. Smallest honest implementation of considerthese proposal 2(b)

Proposal 2 (`considerthese/2026-10-25.md:41-45`) asks for one ledger that "(a) re-runs every closed
defect's check at tip forever, (b) blocks pre-registration when a class recurs twice, and (c) includes
a tip-receipt validator". (a) is partly built (per-file, two readers), (c) is now partly built for the
round-36 package (the gate's `c_receipt`/`c_rerun`), (b) is **not built**.

The smallest honest implementation of (b) has two parts, and the first is the blocker:

**(1) A stable class vocabulary — the actual missing piece.** Add a canonical class id to every ledger
row, e.g. `corpus/defect-classes.json`:

```json
{"count-misstatement": {"label": "a number stated in one committed artifact disagrees with the artifact it names",
                        "check_kind": "cross-artifact re-derivation"},
 "stale-record":     {"label": "a committed record still states a retracted or superseded claim",
                      "check_kind": "append-only correction present"},
 "report-before-commit": {"label": "the round report is filed before, or does not cite, the round's last lane commit",
                      "check_kind": "commit-order assertion"},
 "gate-row-omission": {"label": "a required registry or Gate row is missing or omits a required reason",
                      "check_kind": "registry completeness"},
 "phantom-hash":     {"label": "a cited commit or path does not exist", "check_kind": "existence"},
 "receipt-path-mismatch": {"label": "a cited receipt path or digest does not resolve", "check_kind": "existence"},
 "seat-registry-mismatch": {"label": "a registry member count disagrees with the committed reports",
                      "check_kind": "cross-artifact re-derivation"},
 "scope-misstatement": {"label": "a record states a scope wider than its command measured",
                      "check_kind": "directional citation check"},
 "untracked-work":   {"label": "round work left uncommitted in the lane worktree", "check_kind": "worktree scan"},
 "counter-accepts-junk": {"label": "a frozen check passes junk or a labelled-but-false input",
                      "check_kind": "junk battery"},
 "working-tree+token-cooccurrence": {"label": "a check reads the worktree or matches tokens instead of a relation",
                      "check_kind": "committed-byte read"},
 "narrow-scratch-roots": {"label": "a check's path roots or regex are too narrow for the population",
                      "check_kind": "population-wide count"},
 "manifest-omission": {"label": "a manifest omits a file a receipt claims", "check_kind": "manifest digest"},
 "false-refusal":     {"label": "a refusal's stated reason is contradicted by the lane's own bytes",
                      "check_kind": "directional citation check"},
 "live-reachability-dependency": {"label": "a claim depends on live reachability instead of a committed capture",
                      "check_kind": "committed-byte read"},
 "scratch-bloat":     {"label": "committed recursive scratch mirrors", "check_kind": "population-wide count"},
 "id-collision":      {"label": "a staged source id collides with a live registry id", "check_kind": "registry completeness"},
 "raw-payload-not-retained": {"label": "a probe's raw bytes are not committed", "check_kind": "manifest digest"},
 "locator-drift":     {"label": "a citation points at lines that moved after an edit", "check_kind": "directional citation check"},
 "duplicate-text":    {"label": "duplicated residue in a committed file", "check_kind": "text check"},
 "registry-relation-asymmetry": {"label": "a registry row asserts a relation the artifact does not carry",
                      "check_kind": "cross-artifact re-derivation"},
 "pre-registration-ordering": {"label": "the frozen claims or instrument was not committed before the data",
                      "check_kind": "commit-order assertion"},
 "control-prose-mismatch": {"label": "a claims file's prose disagrees with the control it names",
                      "check_kind": "cross-artifact re-derivation"}}
```

Backfill the 9 existing rows to these ids (the round-35 rows' ids/classes stay frozen; add a
`class_id` field rather than renaming `class`, so the frozen predicate's check names and ids are
untouched). Also backfill the 24 round-29…33 routed defects as ledger rows — otherwise the ledger
counts only the two rounds it already covers and "recurs twice" can never fire for classes 1–10, 5–10.

**(2) A pre-freeze gate that actually blocks.** One script, ~60 lines:

```
python3 plans/prereg_recurrence.py --lane . --claims plans/round-N-claims.md
```

* reads every row of every `corpus/defects*.jsonl` (`glob`, not one hard-coded file) and groups by
  `class_id`;
* for each class with ≥2 rows, requires the round's claims file to name a **fixture id or check
  function** that exercises that class (a machine-readable pointer — e.g. a
  `## Recurrence preflight` table in the claims file mapping `class_id → fixture_id`, cross-checked
  against the counter's fixture registry, so the claim cannot be satisfied by a sentence);
* exits non-zero and prints `RECURRENCE-BLOCK class=<id> count=<n> unrouted` when any such class is
  unaddressed, so the **freeze commit cannot be made** — that is what "blocks pre-registration" means;
* runs *before* the claims freeze (the round-35 evidence that "before any seat scored" is otherwise
  unprovable from bytes: `corpus/lessons/round-29-verifier-spotcheck.md:63-64`).

Honest costs, stated rather than hidden:

* the vocabulary + backfill is the expensive half (24 unledgered routed defects, 10 recurring classes
  needing at least one class-keyed standing check each);
* the gate can only block on classes that are in the ledger — ledger completeness is a precondition,
  not an optional extra;
* the 14-fixture battery cannot serve as the class-coverage evidence for most classes (§5): eight of
  the ten recurring classes need a fixture on a surface the package battery never reads. Either the
  battery grows sub-batteries per class (a D4-line battery already exists — L1–L6 — and the D5-line one
  L4–L6; the pattern transfers) or those classes need their own standing checks;
* a class is not "covered" by a check bound to one artifact. `r34_d4` binds one SCORECORD line;
  `r35_d4` binds one lesson `## Gate` line; neither covers *scope-misstatement* as a class, and the
  round-35 lesson's own §Mistakes row 36 concedes exactly this ("none — round 34's D1 was narrowed to
  three paths and round 35's d4 pattern is a regex over one clause");
* the same clause-blindness that produced §5's six surviving mutants would produce false blocks if
  the pre-registration gate accepted "a check exists" instead of "a check is exercised by a named
  fixture".

The minimum honest slice, if only one thing ships this round: **the class vocabulary
(`corpus/defect-classes.json` + `class_id` on the 9 rows) and one reader that sees both ledgers.**
Without those, "recurs twice" is not decidable from bytes and proposal 2(b) stays unimplementable no
matter how much prose is added.

---

## 7. Adjacency and risk notes for wave 2

1. **Two ledgers, two readers, no joint command.** `plans/defect_ledger.py:119` reads
   `corpus/defects.jsonl`; `plans/round36_c1_verify.py:41,335` reads `corpus/defects-round35.jsonl`. A
   class recurring across the split (e.g. `untracked-work`: R34-D1's row vs R35-D2's row) is invisible
   to either checker alone. The round-36 tip sweep runs both
   (`.ufo/waves/round-36/build/R36TipSweep.md:48`), but that is a wave receipt, not a standing
   obligation.
2. **The standing ledger checker is unregistered.** `plans/defect_ledger.py` has no `SKILL.md` §Gate row
   (13 rows, none named `defect-ledger`; the single `defect_ledger` hit in `SKILL.md` is prose inside the
   `package-gate` row). This is the gate-row-omission class recurring on the checker that owns the
   gate-row-omission row. Cheap fix: one registry row.
3. **The round-35 rows' `recurrence_of` values are not class-consistent** (§3): two of four name row
   ids whose `class` fields are other classes; one is `null` although the class recurred in r31.
4. **Six gate clauses have no failing fixture** (§5, N1). The frozen predicate does not test them;
   `plans/round-36-claims.md` kill-rule treats a surviving mutant as "reported as a limit, never
   repaired into the frozen battery" — so this is a wave-2 reporting obligation, not a repair request.
5. **The narrow-root class recurs inside its own closure** (§5, N2) — 912 committed nested wave paths
   remain invisible to `r35_d3`'s round-3x regex. Disclosed in the claims as a named limit.
6. **"Reads committed bytes" is untestable by the current battery shape** (§5, N3): the fixture repos are
   index-only, so `git show` cannot run inside them.
7. **Two of my counts are classification-dependent and are labelled as such**: "recurring" counts defect
   items, not bullets (§1), and "covered" means a check that fires on a *future* occurrence, not one
   bound to a named artifact (§4). Both definitions are stated so the L1 can re-derive or re-cut them.

---

## 8. Evidence index (command → output)

All commands run from the lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, read-only.

| what | command | output |
|---|---|---|
| ledger row count | `wc -l corpus/defects.jsonl corpus/defects-round35.jsonl` | `5`, `4` |
| class repetition across both ledgers | python over both JSONL files | `rows: 9`; 9 distinct classes; `classes with >1 row: NONE`; `R35 rows whose class has a prior row with same class: NONE` |
| ledger readers | `grep -n "defects" plans/defect_ledger.py plans/round36_c1_verify.py` | `defect_ledger.py:119` → `corpus/defects.jsonl`; `round36_c1_verify.py:41` → `corpus/defects-round35.jsonl`, `:335` reads `LEDGER_REL` |
| 2(b) unimplemented (lane's own words) | `grep -n "recurs twice" corpus/QUALITY.md` | `:291` "part (b) of that proposal (block pre-registration when a class recurs twice) is not implemented — `recurrence_of` is recorded, not enforced" |
| same, lesson | `grep -n "recurrence blocking" corpus/lessons/round-35.md` | `:33` "(b) recurrence blocking is recorded (`recurrence_of`) but not enforced; (c) the tip-receipt validator is not built" |
| unledgered routed defects | `grep -n "R3[123]-" corpus/defects*.jsonl` | only the `R34-D1` row's `recurrence_of` prose mentions `R33-N1`; no R29/R30/R31/R32/R33 defect rows exist |
| nested-wave paths at tip | `git ls-tree -r --name-only refs/heads/master \| grep -cE '^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-'` | `0` |
| round-28 nested paths (invisible to `r35_d3`) | `git ls-tree -r --name-only refs/heads/master \| grep -cE '^\.ufo/waves/round-28/.*/\.ufo/waves/round-'` | `912` |
| any nested wave path | `git ls-tree -r --name-only refs/heads/master \| grep -cE '/\.ufo/waves/'` | `912` |
| `r35_d3` regex | `grep -n NESTED_RE plans/round36_c1_verify.py` | `:42` `r"^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-"` |
| SKILL gate registry rows | `awk 'NR>=560 && NR<=577' SKILL.md` | 13 rows: hermetic-grader, coverage-census, interval-reverdict, state-assertion-check, grader-perturb, gate-timing, benchmark-spec-audit, registry-reference-check, config-projection, sources-adopt, package-gate, round36-c1-battery, regex-log-probe |
| ledger checker unregistered | `grep -c defect_ledger SKILL.md` | `1` (prose inside the `package-gate` row, not a row of its own) |
| one-round defect counters unregistered | `grep -c "round3._defects" SKILL.md` | `0` |
| fixture repos are index-only | `git init` + `git add -A` (no commit) in a scratch repo; `git show HEAD:f.txt` | `fatal: invalid object name 'HEAD'`, exit `128` |
| battery copies the worktree | `sed -n '55,62p' plans/round36_c1_verify.py` | `shutil.copy2(lane / rel, dest / rel)` |
| clause firing map | read-only probe of `plans/pkg_gate.py` over the 8 package fixtures (P0 rc=0; P1–P7 rc=1) | P1←P5,P7 · P2←NONE · P3←P1,P2,P3,P7 · P4←NONE · P5←NONE · P6←P4,P7 · P7←NONE · P8←NONE · P9←P6,P7 · P10←NONE |
| mutation survival per clause | one neutered temp copy of `plans/pkg_gate.py` per clause, same 8 fixtures | c_instruments killed · c_receipt SURVIVES · c_quote_shape killed · c_quote_verbatim SURVIVES · c_captures SURVIVES · c_sources killed · c_provenance SURVIVES · c_readme SURVIVES · c_clean_tree killed · c_rerun SURVIVES |
| line fixtures behave as designed | read-only probe of `d4-line`/`d5-line` over L1–L6 | L1 rc=0 `D4 ok patterns=3 failed=0` · L2 rc=1 `failed=['pattern1','pattern2']` · L3 rc=1 `failed=['pattern2']` · L4 rc=0 `D5 ok directional=True digest_pinned=True` · L5 rc=1 `missing 'is present'` + `carries 'not present'` · L6 rc=1 `capture digest is not the one in the manifest` |
| D4 pattern semantics on the swapped fixture | python: apply `spec["d4"]["patterns"]` to genuine / swapped / no-token texts | genuine `[T,T,T]` · swapped `[F,F,T]` · no-token `[T,F,T]` — the fixture genuinely distinguishes the two |
| frozen spec pins still hold | python: sha256 of the three `frozen_instruments`, the receipt, and the three capture files vs `plans/pkg-spec-r35.json` | all `OK` (incl. `receipt 2359d906…`) |

Not verified here (no lane counter of record was executed): the round-36 predicate values themselves
(`FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`, `rows=4 closed=4 observed_pass=4
mismatches=0`), the C2 counter's six checks, and the census. Those belong to the C1/C2 seats and to
wave 2; this report deliberately re-derives only what the class map needs.

---

VERDICT: classes-23-recurring-10-uncovered-8
