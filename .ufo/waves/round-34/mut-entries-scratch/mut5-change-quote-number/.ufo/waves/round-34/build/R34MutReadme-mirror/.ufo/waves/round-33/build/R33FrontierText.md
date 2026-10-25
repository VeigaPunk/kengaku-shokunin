# R33FrontierText — `corpus/README.md` coverage-map + frontier wording for round 33 (C1)

Seat: `R33FrontierText` (leaf; no subagent dispatch, no background jobs, no model pinning).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Access date for every source opened this round: **2026-10-25**.
Report path: `.ufo/waves/round-33/build/R33FrontierText.md`.
Production writes by this seat: **none**. This file is the only lane path written.
Tools installed/upgraded by this seat: **none** (no pacman / uv / npx / cargo action was taken; no
tool was needed — read-only byte extraction, hashing and diffing were done with stdlib `python3` and
read-only `git` plumbing). `/home/vgpnk/Projects/shokuknow` was not written and no campaign tool was
run there. The fleet repo `/home/vgpnk/Projects/shokunin` was not written. No git index in any lane was
mutated (read-only `git show` / `log` / `diff` / `ls-tree` only).

## 0. Baseline, tree state and one concurrent-commit event

| Fact | Value |
|---|---|
| `HEAD` at report time | `2b4cef2` — `round-33: renumbered assimilation (S103/S104), routed-defect closure N1-N6, catalog re-probe receipts` |
| Prior tip (at seat start) | `7895588` — `round-33: C2 routed-defect repairs (N2 scorecard section, N5/N6 lesson errata), Q22, defects-after receipt` |
| Freeze commits (claims) | `f0b20aea` (frozen claims/counters/controls) + `c227e486` (round-32 wave inheritance, defect N1) |
| **BEFORE anchor** used below | `c227e486:corpus/README.md` — the freeze tip. `git diff c227e486 HEAD --stat -- corpus/README.md` = `6 +++---` (3 insertions / 3 deletions), i.e. the round-33 patch and nothing else |
| **AFTER anchor** used below | `HEAD:corpus/README.md` = `2b4cef2:corpus/README.md` |
| README line count | `388` at the freeze tip and at `HEAD` (no rows added or removed) |
| `corpus/knowledge/*.md` files | `41` (at `f0b20aea`, `c227e486`, `7895588`, `2b4cef2`) |
| `^\| \`knowledge/…\` \|` index rows in README | `41` — unique `41`, `unindexed []`, `dangling []` |
| `S094` / `S097` in the README at `HEAD` | **0 hits** (they survive only in `corpus/SOURCES.md` as the round-32 refusal rows, which stand unchanged) |
| `corpus/SOURCES.md` rows at `HEAD` | `97` (`95` at the freeze tip; `+2` = the new `S103` / `S104` rows) |
| `git status --porcelain` at report time | ` M .ufo/waves/round-33/build/R33RowDrafts.md`, `?? .ufo/waves/round-33/build/R33FrontierText.md` (this file) |

**Observed, and material to the L1:** while this seat was reading, the integrator committed `2b4cef2`,
which carries the C1 README patch (3 hunks at lines `67`, `255`, `279`) into `HEAD`. The patch was
already present as an uncommitted working-tree edit at seat start; it is now committed and
byte-identical to what this seat had read. The before/after pair below is therefore anchored on
**freeze tip `c227e486` → current tip `2b4cef2`**, which is the same delta the seat read in the
working tree before the commit landed. This seat did not author the patch and does not claim it.

## (a) Exact current text of the frontier bullet and the coverage bullet

### (a1) Frontier sub-bullet — `corpus/README.md:279` (current, `HEAD` = `2b4cef2`)

len=574 chars, sha256=`89d0e4452c3dd57666b2c20b5c3242a9e631a48f3b2a717fad920f73d1321800`

```
  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads the one Toolathlon task whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and the LLM-as-judge survey frame (S104). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

### (a2) Frontier **header** bullet — `corpus/README.md:276` (current, `HEAD`)

**Locator note (a discrepancy in the task wording, resolved from bytes):** the bullet *titled*
"Agentic benchmark task-spec audits" is at **`:276`**, not `:279`. `:279` is the third **sub-bullet**
beneath it — the round-33 discharge line. Both are given verbatim so the L1 can address either.

len=442 chars, sha256=`6192b178d9bd7a4ce36dcdbd3b5a33c0012444658846d7e91c52f8d70577d869` — **byte-identical at the freeze tip** (`sha256=6192b178d9bd7a4ce36dcdbd3b5a33c0012444658846d7e91c52f8d70577d869`): untouched by round 33.

```
- **Agentic benchmark task-spec audits**: why — S005/S006 show lab self-audits finding task-level validity defects *after* publication; the lane has no instrument that audits a benchmark's task specs, graders, and contamination separately. Next source/instrument: the primary specs and scoring code for Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro (unopened leads in the ART dossier), turned into a per-benchmark task-validity checklist.
```

Where the literal clause lives (membership test on the current README):

| Line | contains the literal `and for Toolathlon` |
|---|---|
| `:276` (bullet header) | **False** |
| `:277` (round-29 attempt-2 sub-bullet) | False |
| `:278` (round-31 sub-bullet) | **True** — the still-open clause this round discharges |
| `:279` (round-33 sub-bullet) | True — quotes the clause while discharging it |

### (a3) Coverage-map bullet — `corpus/README.md:255` (current, `HEAD`)

len=802 chars, sha256=`4b12c15aa079060056a2622dcb0a695905baac76c94cbc1bf3226febf449b876`

```
- **Benchmark grader semantics**: covered at source-code depth (round 33, 2026-10-25, admitted under renumbered ids) — knowledge/benchmark-grader-semantics.md; S093, S103, S104. Discharges the round-31 frontier clause "and for Toolathlon" for the one task whose evaluation script is read (Toolathlon `ab-testing/evaluation/main.py` @ `9be8d8fe`): the grader is a deterministic state comparison — `record.csv` vs `expected_ratio.csv` within the executed 0.05% tolerance — preceded by two side-effect checks, the log-bucket one mixing fail-open exceptions with fail-closed credential absence; the S104 survey separates Meta-evaluation from methodology, so judge-based scoring owns its validation part. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.
```

### (a4) The three lines as raw bytes (for byte-equality checking by the L1)

| Line | freeze-tip len | freeze-tip sha256 | `HEAD` len | `HEAD` sha256 |
|---|---|---|---|---|
| `:67` | 386 | `d6019a8937969538f76e4b318be79610af58ce436b8e3c2951fbc40442400e3c` | 440 | `84ba661f8deaff3acb49c7f66e95435b66b4c409ee3a19fb981def937a15d3e2` |
| `:255` | 712 | `33cda93499fd7ad6485b8fed1c15cb27b0a808ea2bd706bc0a9fbdb99e64ad41` | 802 | `4b12c15aa079060056a2622dcb0a695905baac76c94cbc1bf3226febf449b876` |
| `:276` | 442 | `6192b178d9bd7a4ce36dcdbd3b5a33c0012444658846d7e91c52f8d70577d869` | 442 | `6192b178d9bd7a4ce36dcdbd3b5a33c0012444658846d7e91c52f8d70577d869` |
| `:279` | 574 | `1a7ab0b92be1529c95d3f61cc58bb23ef5ff7820e8736d74a854b939a1622ef8` | 574 | `89d0e4452c3dd57666b2c20b5c3242a9e631a48f3b2a717fad920f73d1321800` |

## (b) Paste-ready BEFORE → AFTER strings for C1's admission

`BEFORE` = `c227e486:corpus/README.md` (the freeze tip). `AFTER` = `HEAD:corpus/README.md`
(= `2b4cef2:corpus/README.md`). Both are copied programmatically out of the git objects — no retyping.

### (b1) Index row — `corpus/README.md:67`

BEFORE:

```
| `knowledge/benchmark-grader-semantics.md` | Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; a log-bucket check fails open) and the LLM-as-judge survey frame: meta-evaluation is its own part | S094 (Toolathlon @ 9be8d8fe), S097 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry |
```

AFTER:

```
| `knowledge/benchmark-grader-semantics.md` | Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; its log-bucket check mixes fail-open exceptions with fail-closed credential absence) and the LLM-as-judge survey frame: meta-evaluation is its own part | S103 (Toolathlon @ 9be8d8fe), S104 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry |
```

Span-level delta (as rendered): the description cell `a log-bucket check fails open` →
`its log-bucket check mixes fail-open exceptions with fail-closed credential absence`; the citation
cell `S094` → `S103` and `S097` → `S104`. Cell count `3` before and after; the leading cell stays
`` `knowledge/benchmark-grader-semantics.md` ``; the trailing clause `S093 restated from the
verifier-execution entry` is retained (S093 was mined in round 31 and only *gains* this entry in
`used-by`, so it is a restatement, not a new citation).

**Tolerance wording needs no change (checked, not assumed):** the freeze-tip `:67` and `:255` both
already say "the executed 0.05% tolerance" — the executed call-site value. The lane facts' second
misstatement ("0.1 signature default") appears only in the staged/registry wording, never in the
README. The **credential** misstatement ("fails open") was the one README defect, and it is what the
AFTER cell fixes. So the README needed no tolerance edit — only the credential clause.

### (b2) Coverage-map bullet — `corpus/README.md:255`

BEFORE:

```
- **Benchmark grader semantics**: covered at source-code depth (round 32, 2026-10-25) — knowledge/benchmark-grader-semantics.md; S093, S094, S097. Discharges the round-31 frontier clause "and for Toolathlon" for the one task whose evaluation script is read (Toolathlon `ab-testing/evaluation/main.py` @ `9be8d8fe`): the grader is a deterministic state comparison — `record.csv` vs `expected_ratio.csv` within the executed 0.05% tolerance — preceded by two side-effect checks, one of which fails open; the S097 survey separates Meta-evaluation from methodology, so judge-based scoring owns its validation part. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.
```

AFTER:

```
- **Benchmark grader semantics**: covered at source-code depth (round 33, 2026-10-25, admitted under renumbered ids) — knowledge/benchmark-grader-semantics.md; S093, S103, S104. Discharges the round-31 frontier clause "and for Toolathlon" for the one task whose evaluation script is read (Toolathlon `ab-testing/evaluation/main.py` @ `9be8d8fe`): the grader is a deterministic state comparison — `record.csv` vs `expected_ratio.csv` within the executed 0.05% tolerance — preceded by two side-effect checks, the log-bucket one mixing fail-open exceptions with fail-closed credential absence; the S104 survey separates Meta-evaluation from methodology, so judge-based scoring owns its validation part. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.
```

Span-level delta (as rendered): `round 32` → `round 33`; `, admitted under renumbered ids` inserted
inside the existing parenthesis (the house form used by the sibling bullets `:253` / `:254`);
`S094` → `S103`, `S097` → `S104` (two id sites); `one of which fails open` → `the log-bucket one
mixing fail-open exceptions with fail-closed credential absence`. The `0.05%` clause, the `PROVINCE`
refusal and the three trailing "Not …" disclaimers are byte-identical to the freeze tip.

### (b3) Frontier sub-bullet — `corpus/README.md:279`

BEFORE:

```
  - *Partly discharged round 32 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads the one Toolathlon task whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and the LLM-as-judge survey frame (S097). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

AFTER (as committed at `2b4cef2` — the minimum delta C1's admission wording requires):

```
  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads the one Toolathlon task whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and the LLM-as-judge survey frame (S104). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

Span-level delta (as rendered): `round 32` → `round 33`; `S097` → `S104`. Nothing else moves — the
scope limitation (**for that one task's scoring code only**), the two still-open clauses
(Terminal-Bench 2.0's scoring code; any SWE-bench Pro V2 grader beyond the round-31 task-level one)
and the `PROVINCE.md` refusal stay byte-identical to the freeze tip.

#### (b3.1) OPTIONAL strengthening — naming S103 in the frontier line

Observed gap: the AFTER text at `:279` names the Toolathlon read by **path and pinned commit**
(`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and names `S104` for the survey, but
**never names `S103`** — the id under which the Toolathlon document was admitted. A reader can follow
the commit to the file, but cannot tie the frontier discharge to the registry row that carries it.

Optional AFTER (the committed text + exactly one insertion, `, S103`, after the commit pin):

len=580 chars, sha256=`8b272f96160a5d98b269861ff5d1eda9b57005e761cf00d66487e2032e95d3b1`

```
  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads the one Toolathlon task whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`, S103) and the LLM-as-judge survey frame (S104). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

**Counter-gating (checked, not inferred):** the frozen C1 counter does **not** read the frontier
text. `plans/adoption_check.py` reads only the README **index row** (`^\| \`knowledge/<name>\` \|`,
exactly one, cells 2 and 3 non-empty — `plans/adoption_check.py:60-140`); `plans/round33_c1_verify.py`
check V4 (`check_v4`, `:105-118`) likewise reads only that index row. `grep -l Frontier plans/*.py
plans/*.sh` matches only `plans/round24_census.sh` (a read-only round-24 counter that counts frontier
rows, not their text). So the insertion is **wording quality, not a pass/fail gate** — the L1 may
take it or leave it. The minimum AFTER above already satisfies every counter.

## (c) Index-table row format from the nearest sibling rows

The patched entry sits in the `## What's here` knowledge table (header `:27`, separator `:28`).
Nearest siblings of the patched row, verbatim from `HEAD`:

`:64` — `knowledge/benchmark-task-validity-checklist.md`:

```
| `knowledge/benchmark-task-validity-checklist.md` | Ten-axis task-validity checklist read from four maintainers' own artefacts (canary, oracle/nop, cheat trials, grader isolation, declared task fields, dated release gate); counts re-derived, not copied; not task validity, contamination measurement or model performance | S077-S080, S090 (`corpus/SOURCES.md` rows, opened 2026-10-25); `plans/round-29-attempt2-claims.md`; round-29 attempt-2 Gate |
```

`:65` — `knowledge/contamination-transparency-card.md`:

```
| `knowledge/contamination-transparency-card.md` | The contamination transparency card as an **amendment** to the tabulated card designs: release-side R1-R5 and score-side S1-S2 fields mapped into the union table's columns, plus the CG1-CG8 answerability gate and each detector's stated blind spot; not a fourth card design, not a contamination measurement | S081–S086 (`corpus/SOURCES.md` rows, opened 2026-10-25); `corpus/knowledge/contamination-detection-and-transparency.md`; round-30 Gate |
```

`:66` — `knowledge/benchmark-verifier-execution-model.md`:

```
| `knowledge/benchmark-verifier-execution-model.md` | Where a benchmark's verifier actually runs (Harbor's per-task `environment_mode` resolution: shared by default) and what it restores before grading (stale rewards deleted, `/tests` re-uploaded unless the verifier image owns it), plus SWE-bench Pro V2's own git-based test-space reset and the log-scan grader that reads its PASSED set | S092 (Harbor @ 6099b8cf), S093 (SWE-bench Pro V2 @ 66f92766), S100 (terminal-bench-2 @ 2fd12b88) |
```

`:67` — the patched row itself:

```
| `knowledge/benchmark-grader-semantics.md` | Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; its log-bucket check mixes fail-open exceptions with fail-closed credential absence) and the LLM-as-judge survey frame: meta-evaluation is its own part | S103 (Toolathlon @ 9be8d8fe), S104 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry |
```

**Row format (derived from the three siblings above, which all land in the same table):**

```
| `knowledge/<file>.md` | <one-sentence scope of what the entry establishes, ending in what it is NOT> | <source cell> |
```

- **Cell 1** — a single backticked path relative to `corpus/`, exactly `knowledge/<file>.md`.
- **Cell 2** — one prose sentence naming the depth (`source-code depth`, `source-digest depth`, …), the
  thing established, and the exclusions. The round-31 sibling `:66` is the direct structural ancestor
  of the patched row and uses the identical `Not …, not …, not …` tail; the patched row preserves
  that tail verbatim.
- **Cell 3** — the source cell. Two sibling conventions coexist:
  - **id + label + short pin** (the `:66` convention, the one the patched row follows):
    `S092 (Harbor @ 6099b8cf), S093 (SWE-bench Pro V2 @ 66f92766), S100 (terminal-bench-2 @ 2fd12b88)`;
    the patched cell is `S103 (Toolathlon @ 9be8d8fe), S104 (arXiv 2412.05579v2); S093 restated from the
    verifier-execution entry` — same shape, with the `S093` clause flagged as a restatement.
  - **id range + provenance + date** (the `:65` convention): `S081–S086 (\`corpus/SOURCES.md\` rows,
    opened 2026-10-25); …; round-30 Gate`.
- **Row shape invariants (measured):** cell count `3`; cell 2 length `285` chars (non-trivial); cell 3
  non-empty; exactly one row matches `^\| \`knowledge/benchmark-grader-semantics.md\` \|`; the row lies
  inside the `## What's here` → `### \`lessons/\`` window (`:25`→`:97`) that
  `plans/state_check.py:1267-1290` (`readme_index_rows`) parses for the P2e index-parity check;
  `41` files ↔ `41` unique index rows, `unindexed []`, `dangling []`.
- **Placement:** the patched row is the last `knowledge/` row of the table, immediately after `:66` and
  before the `lessons/` rows begin at `:68` — the same table position the round-32 draft used, so the
  row is re-pointed in place, not re-inserted, and no index row is added or removed.

## Findings / observations for the L1

- **F-A1 (info):** the C1 README patch is committed at `2b4cef2` and already satisfies every
  counter that reads the README (one anchored index row, three non-empty cells). This seat's output
  is the byte-exact before/after pair plus the sibling row format, not new README bytes.
- **F-A2 (deliberate deviation carried by the committed patch):** the AFTER wording replaces the
  freeze-tip "fails open" phrasing with the fail-closed credential reading. The task wording asked for
  "same claim text"; leaving the old clause would make the coverage map contradict the entry it
  indexes, and the round-33 lane facts require the fail-closed semantics. **Not recommended** to
  subtract it.
- **F-A3 (optional, wording only):** the frontier line `:279` still does not name `S103` — see §(b3.1).
  Not counter-gated; the L1 may add `, S103` after the `9be8d8fe` pin.
- **F-A4 (anchor, outside this seat's write surface):** the entry cites `corpus/README.md:276` for the
  clause `"and for Toolathlon"`, but `:276` is the bullet **header** and does not contain that literal;
  the literal clause sits on `:278` (and is quoted on `:279`). The anchor points at the right bullet but
  not the right line. The entry owner (not this seat) should decide `:276` vs `:278`.
- **F-A5 (no action needed, recorded because the task wording implied otherwise):** the `0.1`-vs-`0.05`
  tolerance misstatement was never in the README — `:67` and `:255` already said "the executed 0.05%
  tolerance" at the freeze tip. The only README misstatement was the credential one.

## Commands run (all read-only; no lane writes, no git mutation)

- `git -C <lane> log --oneline -6`, `git rev-parse HEAD`, `git status --porcelain`,
  `git diff -- corpus/README.md`, `git diff -U0 -- corpus/README.md`, `git diff c227e486 HEAD --stat -- corpus/README.md`,
  `git show --stat 2b4cef2`.
- `git -C <lane> show <rev>:corpus/README.md` for revs `f0b20aea`, `c227e486`, `7895588`, `HEAD` — every
  quoted block in this report was extracted programmatically from those git objects.
- `git ls-tree --name-only <rev> corpus/knowledge/`; `git show <rev>:corpus/SOURCES.md` (row census;
  S093 / S103 / S104 cell dumps; refusal-row presence and `used-by` cells for S094/S097/S101/S102).
- `grep -n` over `corpus/README.md` for `S094|S097|benchmark-grader-semantics|and for Toolathlon|round 32`;
  `grep -l Frontier plans/*.py plans/*.sh`; `grep -n` over `plans/adoption_check.py`,
  `plans/round33_c1_verify.py`, `plans/state_check.py` for the README-reading code paths.
- `python3` (stdlib only) for: line hashes/lengths, non-ASCII inventory, index-row/file parity,
  the `## What's here` → `### \`lessons/\`` window membership, cell-shape counts, and the before/after
  string extraction that produced every quoted block here.
- Read (not run): `plans/adoption_check.py:60-140`, `plans/round33_c1_verify.py` (V1–V8, `check_v4`),
  `plans/state_check.py:1267-1290`, `plans/registry_check.py`, `plans/round28_census.py`,
  `plans/round24_census.sh:23-24`.
- Scratch: `/tmp/r33-R33FrontierText/` (`mk.py`) — well under 60 MB.

## Not claimed

- Not run by this seat: `plans/adoption_check.py --expect … --census`, `plans/round33_c1_verify.py`,
  `plans/round33_defects.py`, `plans/catalog_probe.py --verify`. Those receipts belong to the C1/C2/C3
  scorers; an unrun check has not passed.
- Not claimed: registry (`corpus/SOURCES.md`) correctness, entry prose correctness, admission,
  SCORECARD, lessons, fleet-report errata. This report covers README wording only.
- No production file was written by this seat; the only lane path written is this report.

VERDICT: frontier-read
