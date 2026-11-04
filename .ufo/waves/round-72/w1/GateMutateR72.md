# GateMutateR72 — R72-C2 mutant metric attack: six fresh semantic mutants, five blind fixtures, and a semantic `null` that reproduces the frozen green line

**Verdict in one line.** The shipped `--mutants` is non-invariant and its six shipped mutants are
genuinely killed by fixture escape, but the matrix is bounded by a seven-fixture red set: the six
fresh semantic mutants below yield five `null` and one `invalid`; four of the nulls (G1, G2, G3,
G6) plus the extra G7 pass `DEFECTS n=0 / PREDICATE R72-C2 pass` on bespoke lanes the pristine gate
refuses, and the fifth (G4) is a builder edit the harness never executes. Replacing the deliberate
comment no-op with G1 prints the exact frozen line `MUTANTS total=7 killed=6 survived=0 invalid=0
null_detected=1` and rc 0. That is a fixture-set defect of the metric, reported, not edited.

## Item attacked and scope

R72-C2's second instrument is `plans/round72_c2_routed_defects.py`: the `MUTANTS` table, `run_mutants`,
and the fixture builder. This seat attacks the **metric**, not the checks' correctness and not the
frozen table. No predicate, case table, vector, digest, kill rule or target was edited. All mutants
are copies in `/fast/scratch/hyaku/kengaku-r72/GateMutateR72/`; the lane script was only read.

The shipped design is clear in its docstring: a mutant is `killed` when it *accepts* a red fixture
the pristine gate refuses (the fixture set detects the weakened clause), `survived` when it refuses
every red fixture, `invalid` when it refuses the green fixture or the edit does not apply, and
`null` when its verdict vector equals the pristine gate's. Fixtures are built **once by the driver**
and each mutant is invoked only as `--lane <fixture>` (`run_mutants`, `:403-470`).

## Pinned bytes

Lane `master` tip `b6336136e0e891522b113a94d8e0bd65e0eae8de` (round-72 freeze commit). Python 3.14.8,
stdlib only.

| file | sha256 |
|---|---|
| `plans/round72_c2_routed_defects.py` | `2d81ad806cb3177463f013d5a5390cf7c4162fc99bd19dd86a1ceec437c78758` |
| `SKILL.md` | `a1440637…` at battery time → `ed12760b…` at final read (sibling drift, below) |
| `plans/round-71-claims.md` | `20a83829c619ce308fa2f3f942cf23712715c205c87085654dad3f9ebce907b0` |

The gate's sha256 was recorded before the battery and is identical after; `plans/round-71-claims.md`
is also unchanged and matches the tip. **Drift.** A sibling rewrote the four `SKILL.md` registry
rows while this report was being written: `SKILL.md` moved `a1440637…` (battery time) →
`ed12760b…` (final read), a diff confined to those rows' kind cell (`round71-c1` and `round72-c1`
are now `gate`) and their verdict-map/self-test prose. All four rows are still eight cells, their
entry cells still name their scripts, and their owner is still `kengaku`; `--lane .` at
`ed12760b…` still prints `E1a ok … DEFECTS n=0 / PREDICATE R72-C2 pass` (rc 0), and `--mutants`
still prints the same seven `MUTANT` lines and `total=7 killed=6 … null_detected=1` (rc 0). The
mutant battery never reads `SKILL.md` — `run_mutants` builds its fixtures under `--work` — so no
mutant result in this report depends on the drift. The only lane writes are this report and
`corpus/evidence/round72/c2-gate-mutants.txt`.

## What was run (commands, rc)

| # | command | rc | output |
|---|---|---|---|
| 1 | `python3 plans/round72_c2_routed_defects.py --lane .` | 0 | `E1a ok` `E1b ok` `E1c ok` `E2 ok` `DEFECTS n=0` `PREDICATE R72-C2 pass` |
| 2 | `… --selftest --work S/selftest-work` | 0 | `SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True positional-arm=True parser-arm=True ok=True` |
| 3 | `… --mutants --work S/shipped-work` | 0 | §1: 6 `killed`, 1 `null`, `total=7 … null_detected=1` |
| 4 | `python3 S/driver.py` (copy with the seat's 8-row table; shipped `run_mutants` unchanged) | 0 | site uniqueness 9/9, `gate_mine --mutants` rc 1: `killed=1 survived=0 invalid=1 null_detected=6` |
| 5 | `python3 S/iso.py` | 0 | 5 isolation fixtures × 11 gate columns; decisive pairs |
| 6 | `python3 S/swap.py`; then `mut-swap/M7-semantic-null-one-label.py --lane iso/iso-G1-one-label` | 0 | §5: exact frozen line; mutant `DEFECTS n=0 / pass`, pristine `DEFECT E2 … / fail`; mutant `--selftest` rc 0 |
| 7 | `python3 S/stale.py`, `python3 S/stale2.py` | 0 | §6: stale-red probes S1/S2 |
| 8 | `sha256sum` of the three lane files; `git status` | — | gate and claims identical; `SKILL.md` moved by a sibling (§Pinned bytes drift note) |

`S` = `/fast/scratch/hyaku/kengaku-r72/GateMutateR72`. The full raw runs are in
`corpus/evidence/round72/c2-gate-mutants.txt` (354 lines, sha256
`18157a9d8a0ce5668fbcfa26f21f39cd0b5ab6eddd02471ec549a9872fba08c9`).

## 1. The shipped metric is not invariant — the seven lines

```
MUTANT M1-registry-columns target=E1a accept_green=True escapes=1 attribution_ok=True null=False verdict=killed
MUTANT M2-registry-owner target=E1a accept_green=True escapes=1 attribution_ok=True null=False verdict=killed
MUTANT M3-errata-labels target=E1b accept_green=True escapes=1 attribution_ok=True null=False verdict=killed
MUTANT M4-errata-revisions target=E1b accept_green=True escapes=1 attribution_ok=True null=False verdict=killed
MUTANT M5-errata-positional target=E2 accept_green=True escapes=1 attribution_ok=True null=False verdict=killed
MUTANT M6-errata-last-section target=E2 accept_green=True escapes=1 attribution_ok=True null=False verdict=killed
MUTANT M7-null-comment target=E1a accept_green=True escapes=0 attribution_ok=True null=True verdict=null
ARM accept-green=ok refuse-red=ok attribution=ok
MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1
```

The metric is **not** invariant over the table: six semantic rows are `killed` because each flips
exactly one target-owned red fixture to rc 0, and the comment-only row is `null`. That is a real
advance over R71-R5's "the `DEFECT` line disappeared" metric. The rest of this report shows what
the same machinery cannot see.

## 2. Six fresh semantic mutants (the required table)

Each `old` string was asserted to occur exactly once in the source head before the run
(`SITE … count=1 ok=True` ×10: nine edits across the eight-row seat table, one in P1). `observed`
is the exact token `run_mutants` printed for that row;
`iso` is the bespoke fixture built to isolate the weakened clause (pristine rc → mutant rc) and
the defect line the pristine gate prints on it.

| id | clause rewritten (line) | declared target | fixture that should catch it | hand prediction | observed | shipped matrix caught? | isolation (pristine → mutant) |
|---|---|---|---|---|---|---|---|
| **G1** | `check_e2_positional` `for label in SUPERSEDED:` (`:163`) → `SUPERSEDED[:1]` | E2 | `iso-G1-one-label`: first label above the erratum, **only the second** below | survived | **null** | **no** | 1 → 0; pristine `DEFECT E2 superseded-below-erratum:Red-before (committed at freeze)`, `n=1`; mutant `E2 ok / n=0 / pass` |
| **G2** | `check_e1_registry` kind whitelist (`:122`) → `if False:` (accept any kind) | E1a | `iso-G2-kind-note`: one row with `kind=note` | survived | **null** | **no** | 1 → 0; pristine `DEFECT E1a row-kind:round71-c1-hf-probe=note`; mutant `E1a ok / n=0 / pass` |
| **G3** | `check_e1_errata` wording arm (`:152-153`) → `if False:` (no `supersed` required) | E1b | `iso-G3-no-wording`: both labels quoted, both revisions named, the word `supersed` absent | survived | **null** | **no** | 1 → 0; pristine `DEFECT E1b no-supersedes-wording`; mutant `E1b ok / n=0 / pass` |
| **G4** | `build_fixture` full-mode rows (`:295`) → `registry_row(…, columns=6)` | E1a | accept-green arm, **if** the harness used the mutant's builder | null | **null** | **no** | mutant builder emits `[6,6,6,6]` cells; metric green `[8,8,8,8]`; mutant gate rc 0 on metric green, rc 1 on its own 6-column green |
| **G5** | `parse_count` regex (`:183`) + `WORD_NUMBERS` (`:72`) → accept `sixteen` as 16 | E1c | E1c's own `COUNT_CASES` (`:196`, `("sixteen Mistakes rows", None)`) | invalid | **invalid** | **no** (no E1c red fixture exists) | E1c is lane-independent; mutant green stdout: `DEFECT E1c parse:'sixteen Mistakes rows'=16 want=None`, `n=1`, `accept_green=False` |
| **G6** | `check_e2_positional` length floor (`:173`) `< 3` → `< 1` | E2 | `iso-G6-short-erratum`: quotes + revisions packed into one non-empty errata line | survived | **null** | **no** | 1 → 0; pristine `DEFECT E2 erratum-too-short`; mutant `E2 ok / n=0 / pass` |

Calibration of my own predictions: 6/6 correct on the killed-vs-not class, 2/6 correct on the exact
token. I predicted `survived` for G1/G2/G3/G6 before reading the verdict order; the metric's
`is_null` test precedes `escapes` (`:438-447`), so a mutant that flips **no** fixture is `null`, not `survived`.
`null` is the stronger miss: the fixture set does not merely fail to detect the weakening, it
records no difference at all.

### Extras (clearly outside the six; not replacements)

| id | edit (line) | target | fixture | hand prediction | observed | shipped matrix caught? | isolation |
|---|---|---|---|---|---|---|---|
| **G0** (positive control) | `if len(cells) != REGISTRY_COLUMNS:` (`:118`) → `not in (6, REGISTRY_COLUMNS)` | E1a | shipped `red-E1a-cols` | killed | **killed** (`escapes=1`) | **yes** | pristine 1 → mutant 0 on `red-E1a-cols` |
| **G7** | `if cells is None: row-absent` (`:115-117`) → bare `continue` | E1a | `iso-G7-row-dropped`: one required registry row removed | null | **null** | **no** (`--mutants` rc 0); the mutant's own `--selftest` rc 1 | 1 → 0; pristine `DEFECT E1a row-absent:round72-c2-routed-defects`; mutant `E1a ok / n=0 / pass` |
| **P1** (metric meta-probe) | shipped M5 edit (`:167`), declared target **E1a** instead of E2 | E1a | shipped `red-E2-moved` (flips, but is not target-owned) | survived | **survived** | **no** | same edit as M5, which the shipped table kills when declared E2 |

G0 is the control that proves the harness still kills a fresh mutant when a target-owned red
isolates the clause. G7 and P1 are metric probes, not coverage counts: G7 shows the mutant red set
is not a superset of the selftest's fake-red shape; P1 shows the verdict is a function of the
author-declared `target`.

## 3. Why the six are missed — the fixture inventory against the clauses

The mutant matrix's red set is exactly seven fixtures (`REDS`, `:313-321`):
`red-E1a-cols`, `red-E1a-owner`, `red-E1b-paraphrase`, `red-E1b-norev`, `red-E2-top`,
`red-E2-trailing`, `red-E2-moved`. The eight-fixture verdict vector is those seven plus the green.
Against the checks' clause inventory:

- **G1 (one-label positional).** No fixture moves *one* label. `red-E2-moved` strips
  `(committed at freeze)` from **both** body sentences, so both labels are found only in the
  erratum quote; `SUPERSEDED[:1]` still reds on the first. The fixture cannot distinguish "both
  labels above" from "the first label above".
- **G2 (kind).** No fixture has a non-`gate`/`probe` kind. `cols` and `owner` isolate the columns
  and owner cells only; every row's kind is `gate`. E1a's `row-kind` arm has no red at all.
- **G3 (wording).** Every claims fixture's erratum contains the fixed sentence "The two labels
  above are superseded;" — including `paraphrase` and `norev`. There is no fixture that quotes
  both labels and names both revisions while omitting the word.
- **G6 (erratum length).** Every erratum in the fixture set has ≥3 non-empty lines. No fixture
  packs the required quotes and revisions into fewer lines.
- **G7 (row absence).** `registry="missing"` is built only as `fake-red` inside `--selftest`
  (`run_selftest`, `:343`), never in `REDS`. The mutant matrix therefore cannot see a deleted
  row-absence clause; the selftest catches it (rc 1, `defects-in-fake=2 want=3`), but the two arms
  use different fixture sets and only one of them is scored per mutant.
- **G4 (fixture builder).** Structural: `run_mutants` calls the **driver's** `build_fixture`
  (`:408-409`) and invokes each mutant only as `--lane`. A mutation to `build_fixture`,
  `claims_fixture` or `registry_row` is never executed by the metric. Verified: the G4 mutant's
  builder produces `[6,6,6,6]` cells, while the green fixture the metric uses has `[8,8,8,8]`;
  the mutant's gate accepts the metric's green (rc 0) and rejects its own (rc 1). The `--selftest`
  arm does import the mutated builder and fails (rc 1, `all-fail=False`), but that is a separate
  command, not the mutant metric.
- **G5 (E1c).** `REDS` contains no E1c entry, so `target_reds` for an E1c mutant is empty and
  `killed` is unreachable. E1c's only detector is its own `COUNT_CASES`; a weakening that breaks a
  case makes `accepts_green=False` → `invalid`. That does fail the metric's rc, but it is a
  validity rejection, not a kill, and it says nothing about the fixture set.

`survived` is not the common miss here; `null` is. That matters for how the frozen line should be
read: `null_detected=1` is satisfied only because the table contains exactly one row that flips no
fixture. The counter cannot distinguish "deliberate no-op" from "semantic clause the fixtures
cannot isolate" — both produce the identical token.

## 4. What the metric can and cannot certify

**It can certify** that each of M1-M6, as edited in the shipped table, is accepted by at least one
red fixture that the pristine gate refuses; and that the comment-only M7 changes no fixture verdict.
Those six kills are real under the metric's own definition (each `escapes=1`, `accept_green=True`,
`attribution_ok=True`).

**It cannot certify** that the fixture set covers the checks' clauses. Four of the six fresh rows
(G1, G2, G3, G6) and the extra G7 have lane witnesses: on
`iso-G1`/`iso-G2`/`iso-G3`/`iso-G6`/`iso-G7` the mutated gate prints `DEFECTS n=0 / PREDICATE
R72-C2 pass`, while the pristine gate prints a named defect and `fail` on the same bytes. The
remaining null (G4) is blind for a different reason — the harness never imports the mutant's
builder — so its witness is the builder's own 6-column output, not a lane. A `null` in this metric
is therefore a coverage claim about the fixture set, not evidence that the edit is inert.

### 4.1 The swap probe: the frozen green line with a semantic null (headline)

Take the shipped 7-row table and replace only the deliberate comment no-op M7 with G1 (same row
count, same target E2):

```
MUTANT M7-semantic-null-one-label target=E2 accept_green=True escapes=0 attribution_ok=True null=True verdict=null
ARM accept-green=ok refuse-red=ok attribution=ok
MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1
```

`rc=0`. The exact string the frozen predicate pins is reproduced. The generated mutant file then:

- on `iso-G1-one-label`: `E1a ok / E1b ok / E1c ok / E2 ok / DEFECTS n=0 / PREDICATE R72-C2 pass`,
  rc 0 (pristine on the same bytes: `DEFECT E2 superseded-below-erratum:Red-before (committed at
  freeze)`, `n=1`, `fail`, rc 1);
- on its own `--selftest`: `SELFTEST … all-fail=True append-only-arm=True positional-arm=True
  parser-arm=True ok=True`, rc 0;
- its only check-function difference from the shipped gate is the single hunk
  `- for label in SUPERSEDED:` / `+ for label in SUPERSEDED[:1]:` (the `MUTANTS` block is also
  reformatted by the probe builder; the seven rows are the shipped six plus the semantic null).

This does **not** falsify the shipped run: the table is frozen, and the shipped M7 really is a
comment-only edit. It falsifies the inference that `null_detected=1` certifies the null is a no-op,
and it shows the frozen mutant arm is satisfiable by a gate that accepts an erratum for only one of
the two labels. That is the calibration defect this seat reports.

## 5. Metric self-consistency: the declared target and the stale red

Two further properties are visible in `run_mutants` and were run as probes.

**5.1 `killed` is a function of the author-declared `target`, not of the edit.** `escapes` is
computed over `target_reds = [fx for (c, _m), fx in reds.items() if c == target]` (`:433`), and no
code checks that the edit touches the check named by `target`. The same M5 edit:

- declared `target=E2` → `killed` (shipped row);
- declared `target=E1a` → `survived` (`P1-relabelled-M5`, rc 1, `escapes=0`), even though it flips
  `red-E2-moved` from rc 1 to rc 0.

Attribution is likewise a single cross-check fixture: `other = next(c for c in ("E1a","E1b","E2")
if c != target); attr_fx = next(fx for (c,_m), fx in reds.items() if c == other)` (`:434-435`) —
the *first* red of the *first* other check, not the full cross-check set. The shipped rows all
print `attribution_ok=True`, but that is one fixture per kill.

**5.2 The kill rule does not verify the fixture was red under pristine.** `escapes` counts
`fixture_verdict(mp, fx) == 0` without comparing `pristine_vec` for that fixture (`:433`), although
the docstring says "accepts a red fixture **the pristine gate refuses**". Probes:

- **S1** — a single `E1a` "red" fixture built from the green kwargs (pristine rc 0), plus a
  comment-only no-op: the row prints `escapes=1 … null=True verdict=null`. The escape count and
  the null flag contradict each other; the aggregate is still `null_detected=1`, rc 0.
  `--selftest` prints `RED-NOT-RED E1a stale-green` but returns `ok=True`, rc 0 — the warning is
  non-fatal.
- **S2** — the same stale `E1a` fixture plus one genuine `E2` red, with the M5 edit declared
  `target=E1a`: `escapes=1 … verdict=killed`, rc 1. The kill is manufactured entirely by a fixture
  the pristine gate accepts. (The rc is 1 here only because a one-row table expects
  `killed=total-1`; the decisive field is `verdict=killed`.)

So a broken red fixture can both corrupt `escapes` and manufacture a `killed`. The selftest's
`RED-NOT-RED` line is the only guard and it is a print, not a failure.

## 6. Verdict

1. **The shipped `--mutants` is non-invariant at the table level and its six kills are real.**
   `total=7 killed=6 survived=0 invalid=0 null_detected=1`, rc 0, reproduced in §1. Nothing here
   contradicts the printed line or R72-C2's `--mutants` clause as written.
2. **The metric is not a coverage certificate for the fixture set.** Five of six fresh semantic
   mutants are `null`; four (G1, G2, G3, G6) and the extra G7 have a witness where the mutated gate
   prints `DEFECTS n=0 / PREDICATE R72-C2 pass` on bytes the pristine gate reds; the fifth (G4) is
   the harness-design blind spot in §3. The lane witnesses are **fixture-set defects**: the
   matrix has no one-label positional fixture, no kind fixture, no wording-absent fixture, no
   short-erratum fixture, and no row-absence fixture in `REDS`.
3. **`null` is doing two jobs.** The comment-only M7 and a semantic clause the matrix cannot see
   are the same token. Replacing M7 with G1 reproduces the exact frozen line and rc 0, and the
   resulting gate passes both the isolating lane and its own `--selftest`. The `null_detected=1`
   pin therefore proves "exactly one row flipped nothing", not "the null row is inert".
4. **Two classes are structurally ungradeable by this metric.** E1c has no red fixture, so no E1c
   weakening can ever be `killed` (G5 is `invalid`); the fixture builder is never imported from the
   mutant, so builder edits are inert by construction (G4 is `null`, while a manual `--selftest` on
   the mutant does fail). G7 shows the mutant red set is not a superset of the selftest's fake-red.
5. **Two self-consistency gaps.** `target` is author-declared and unchecked (P1: same edit,
   `killed` vs `survived`); `escapes` does not require the pristine gate to refuse the fixture
   (S1/S2: a stale green fixture produces `escapes=1` on a no-op and manufactures a `killed`).
6. **Report-only recommendations** (none applied; the frozen rules are not mine to edit): add red
   fixtures for kind, one-label position, wording, erratum length and row absence; build fixtures
   with the mutant's own builder or refuse builder edits; require `pristine_vec[fx] != 0` before
   counting an escape; verify the edit's `old` string touches the declared target check; give E1c
   a fixture/vector detector so a weakened `parse_count` can be killed rather than invalid; and
   have `--selftest` fail on `RED-NOT-RED` rather than print it.

## 7. Non-mutation and scratch discipline

- No `git`/`jj` mutating command was run. The only lane reads were `rev-parse`, `status`, `diff`,
  `sha256sum`, and file reads. `plans/round72_c2_routed_defects.py` and
  `plans/round-71-claims.md` are byte-identical before and after; `SKILL.md` moved once by a sibling
  (drift note in §"Pinned bytes"), and the gate is green at both revisions. `git status
  --porcelain` for the gate and claims paths is empty.
- The only lane writes are this report and `corpus/evidence/round72/c2-gate-mutants.txt`. No fleet
  root, sibling lane, `.ufo/state/`, `.scratch/` or `corpus/` path outside those two was touched.
- No port was bound; `--port-lock` was not applicable (no battery/probe binding 5000). No tool was
  installed or upgraded; pacman was not invoked.
- All mutants, fixtures and copies lived under
  `/fast/scratch/hyaku/kengaku-r72/GateMutateR72/` (1.8 MB) and were removed after the evidence
  file was written. `/tmp` was checked for owner-created files in the last 30 minutes: none. The
  raw command/output pairs are preserved in the evidence file, so the battery is reproducible from
  the report's one-line edits.
