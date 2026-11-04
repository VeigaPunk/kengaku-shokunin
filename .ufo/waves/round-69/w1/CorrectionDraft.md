# CorrectionDraft — round 69 w1, C2 correction texts (drafts only)

- **Seat:** CorrectionDraft (leaf; no subagent dispatch). **Lane:** `kengaku-shokunin`.
- **Base:** `a518980e` per the frozen claims doc; HEAD at measurement `b288e8e0` (the round-69 freeze
  commit). Working tree was **dirty with sibling landings** during this seat — `git status --porcelain`
  at measurement:
  ```
   M SKILL.md
   M corpus/QUALITY.md
   M corpus/knowledge/tb2-network-service-offline-grader.md
   M corpus/lessons/round-68.md
  ?? .ufo/waves/round-69/w1.ready
  ?? .ufo/waves/round-69/w1.ready.dispatched
  ?? .ufo/waves/round-69/w1/
  ?? corpus/evidence/round69/
  ```
  I did not author those edits and did not touch them. This seat wrote only
  `.ufo/waves/round-69/w1/drafts/{registry-rows,quality-q50,lesson-corrections}.md` and this report.
- **Scope:** draft the three C2 correction texts; do not land them (the L1 lands). No predicate, case
  table, vector, kill rule or target edited.

## 1. What I ran (exact argv)

All read-only; cwd = lane root unless stated. Scratch root
`/fast/scratch/hyaku/kengaku-r69/CorrectionDraft` (created, used, deleted before yield).

| # | argv | purpose |
|---|---|---|
| 1 | `grep -n '## Gate/probe registry' SKILL.md` | registry home `:587` |
| 2 | `grep -n '^## \|^### ' corpus/QUALITY.md \| tail -40` | criterion numbering: last is Q49 (round 64) |
| 3 | `for f in plans/round68_{c1_pypi_finish,c2_correction_gate,report_contract,capability_table}.py; do grep -n 'add_argument\|^def main' $f; done` | flag sets verbatim |
| 4 | `python3 - <<'EOF' …` (the gate's own `registry_rows` + E1 thin logic over `SKILL.md`) | E1 state |
| 5 | `python3 plans/round69_c2_routed_defects.py --root .` | the frozen C2 gate on the working tree |
| 6 | `python3 -c` over `.ufo/waves/round-68/w1-results.json` (agents, output types, notes) | E5/E6 facts |
| 7 | `grep -o '"output": [^,]*' .ufo/waves/round-68/w1-results.json \| sort \| uniq -c` | the `null` fact |
| 8 | `ls .ufo/waves/round-68/w1/` + `ls .ufo/waves/round-68/w1/*.md \| wc -l` | twelve per-seat reports |
| 9 | `grep -c 'receipt-exists' plans/round68_c1_pypi_finish.py` → `0`; `grep -c 'port-8080-occupied' plans/round68_c1_pypi_finish.py` → `0`; `grep -n 'port-8080-occupied' plans/round63_c1_pypi_probe.py` → `:280` | C1 kill-rule token check |
| 10 | `python3 validate_drafts.py` (scratch): apply the three drafts to scratch copies of `SKILL.md`, `corpus/QUALITY.md`, `corpus/lessons/round-68.md`, then run the frozen gate's own `registry_rows`, `count_section`, `section`, and the E5/E6 line filters | draft conformance |
| 11 | `python3 mutate_drafts.py` and `python3 mutate2.py` (scratch): seven mutation arms | draft checkability |

### Raw verdict lines

(4) E1 on the working tree, via the gate's own parser:
```
round68_c1_pypi_finish cells=8 problems= none | kind= probe | owner= kengaku
round68_c2_correction_gate cells=8 problems= none | kind= gate | owner= kengaku
round68_report_contract cells=8 problems= none | kind= gate | owner= kengaku
round68_capability_table cells=8 problems= none | kind= gate | owner= kengaku
```

(5) the frozen C2 gate, working tree, HEAD `b288e8e0`:
```
E1 ok rows=4/4 missing=[] thin=[]
E2 ok headings=1 q50=True round68-lesson=True spotcheck=True
E3 ok inputs=6 differs=['SKILL.md'] problems=[]
E4 ok verified-at-lines=2 last-names-landing=True
E5 ok strict-lines=1
E6 ok rerecord-lines=1
E7 ok problems=[]
DEFECTS n=0
PREDICATE R69-C2 pass
rc=0
```
This is the state a sibling's uncommitted landings produced, **not** a landing by this seat. E7's fresh
runs (`plans/round63_gate_checks.py depth …`, `… trio …`) were executed by the gate itself as part of
this command.

(7) the results-file fact:
```
     12 "output": null
```

(8) per-seat reports — `ls .ufo/waves/round-68/w1/*.md | wc -l` → `13`, which is the twelve seat
reports plus `erratum-draft.md`; the twelve seat names are exactly the `results[*].name` values of
`w1-results.json`:
```
PypiReplicate GateRedRun SelftestTally RegistryRows SourcesRows SourceOpen
ReceiptReview ClaimFalsify CounterMutate ForgeScan RenderingTrace SiblingOverlap
```

(10) draft conformance, drafts applied to scratch copies only:
```
draft rows: 4
E1 rows=4/4 missing=[] thin=[]
E2 headings=1 q50=True round68-lesson=True spotcheck=True
E5 strict-lines=1
E6 rerecord-lines=1
DUPLICATE-CHECK strict phrase occurrences: 1
```

(11) mutation arms (each must fail, and does):
```
as-drafted            : strict-lines=1 rerecord-lines=1
m1 drop 3/12          : strict-lines=0 rerecord-lines=1
m2 widen role set     : strict-lines=1 rerecord-lines=1     <-- NOT caught, see F3
m3 duplicate E5 line  : strict-lines=1 rerecord-lines=2     <-- caught by exactly-one
m4 drop empty-output  : strict-lines=1 rerecord-lines=0
m5 drop per-seat      : strict-lines=1 rerecord-lines=0
as-drafted             : thin=[]
m7 bad entry path      : thin=['round68_c1_pypi_finish:no-entry']
m8 no `1` in verdict   : thin=['round68_c1_pypi_finish:no-verdict-map']
m9 owner blank (not checked by E1): thin=[]                 <-- NOT caught, see F2
as-drafted: headings=1 section-found=True
m10 titled heading: headings=0 section-found=False
```

## 2. The drafts (exact text)

Files: `.ufo/waves/round-69/w1/drafts/registry-rows.md`, `…/quality-q50.md`, `…/lesson-corrections.md`
(paths lane-root-relative). Each carries a grounding table; the paste-ready blocks are repeated here.

### 2a. Four registry rows (`SKILL.md` `## Gate/probe registry`, appended after `round64-trio-sweep`)

```
| `round68_c1_pypi_finish` | probe | `python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt` (lane root; flags implemented: `--lane --work --receipt --evidence-dir --check-receipt --selftest --green-receipt --render-table`; the battery form `--lane . --work <scratch> --receipt <path> --evidence-dir <dir>` runs the four frozen cases in bwrap; `--render-table` prints the case table and `FROZEN-VECTOR`/`DERIVED-VECTOR` without running) | `0` pass (`CHECK ok cases=4 vector=P/F/F/F`, `CHECK stored-predicate=pass derived=pass`, `PREDICATE R68-C1 pass`) · `1` fail (any clause or vector defect, `CHECK defect <name>`, `PREDICATE R68-C1 fail`) · `2` setup (`SETUP receipt-missing`, `grader-sha-mismatch`, `bwrap-absent`, `work-dir-required`, `lane-required`) | `--selftest --work <dir> --green-receipt <receipt>` → `SELFTEST red_refused=5/5 green_ok=1 ok=True` | grader sha `82c63517…` (round-52 pypi-server capture), base-probe sha `2ebaf54e…` (`plans/round63_c1_pypi_probe.py`), TB2 pin `2fd12b88`, frozen vector `P/F/F/F`, receipt `corpus/evidence/round68/pypi/receipt.txt`, per-case stderr captures `corpus/evidence/round68/pypi/stderr/` | writes the `--work`/`--evidence-dir` paths and the receipt; bwrap sandbox, no network beyond 127.0.0.1:8080 | kengaku |
| `round68_c2_correction_gate` | gate | `python3 plans/round68_c2_correction_gate.py` (lane root; flags implemented: `--root --selftest --work`) | `0` pass (`E1..E5 ok`, `DEFECTS n=0`, `PREDICATE R68-C2 pass`) · `1` fail (any `E<n> defect` line) · `2` setup (`SETUP work-dir-required`) | `--selftest --work <dir>` → `SELFTEST defects-in-fake=5 want=5 all-fail=True` | inputs re-hashed in-gate: `plans/round-67-claims.md`, `corpus/evidence/round68/r67-probe-selftest.txt`, `plans/round67_c1_pipeline_probe.py` sha `03793f4f…`, wrongly-cited sha `32bacf1d…`, `corpus/evidence/round67/pipe/a1-mutants.txt`, `SKILL.md` | read-only; fixtures under `--work` | kengaku |
| `round68_report_contract` | gate | `python3 plans/round68_report_contract.py <report.md> --shonen SHONEN.md` (lane root; flags implemented: `--lane --shonen --selftest --work`; `--shonen` defaults to `<lane>/SHONEN.md`) | `0` pass (`DEFECTS n=0`, `PREDICATE R68-A2 pass`) · `1` fail (one `S<n>` defect per missing or malformed required section, S1–S6) · `2` setup (`SETUP could-not-evaluate …`: missing, non-regular, oversized or unreadable input) | `--selftest --work <dir>` → `SELFTEST n=14 red-refused=13 green-ok=1` | the six required `##` headings, the `## Trend verdicts` verdict words, and the four-box SHONEN set (`EXPECTED_BOXES = 4`) read from `SHONEN.md` | read-only over the report and `SHONEN.md`; fixtures under `--work` | kengaku |
| `round68_capability_table` | gate | `python3 plans/round68_capability_table.py --lane .` (lane root; flags implemented: `--lane --scorecard --selftest --work`) | `0` pass (`MISMATCH n=0`, `PREDICATE R68-A3 pass`) · `1` fail (T1 a declared capability has no row, T2 the first-working-round cell does not name the declaring round, T3 the evidence path is absent, T4 a duplicate capability name) · `2` setup (`SETUP could-not-evaluate …`) | `--selftest --work <dir>` → `SELFTEST n=5 red-refused=4 green-ok=1` | `SCORECARD.md` `## Capabilities` table against `DECLARED` (four capabilities, first-working rounds 64–67) | read-only | kengaku |
```

Delta vs the rows already in the working tree: this draft adds the TB2 pin `2fd12b88`, the frozen vector,
`--render-table`, the `stderr/` capture dir, `CHECK stored-predicate=…`, `lane-required`, the wrongly-cited
sha `32bacf1d…`, the `SELFTEST ` prefix on the c2 spelling, `--lane`/`--shonen` on the report-contract row,
and the T1–T4 class names plus the four `DECLARED` capabilities.

### 2b. `corpus/QUALITY.md` Q50

Heading must be the **bare** `## Round69 criterion` (see F4). Paste between the markers in the draft file:

```
## Round69 criterion

A report citation is re-hashed from the committed bytes before it is written.

- **Q50 — a report cites a digest, a count or a revision-bound claim only after re-deriving it from the committed bytes at citation time, and the citation carries the command that re-derives it.**
  Round 68 cited a probe sha (`32bacf1d…`) that the committed file does not carry (`03793f4f…`) and counted 8 killed A1 mutants where the committed tally shows 7 refused plus 1 accepted by design — both `captured-by: none` in `corpus/lessons/round-68.md` `## Mistakes` rows 1–2, routed by `corpus/lessons/round-67-verifier-spotcheck.md` §5 items 1–2. The same round's C2 receipt pair named the pre-landing `SKILL.md` (`3fe9a6d0…`) while the landing tree carries `544ad892…` (`corpus/lessons/round-68-verifier-spotcheck.md` §5 item 3), and its w1 attack line counted 6/12 over a wider role set than the run-15 definition's 3/12 (§5 item 5). Admission: `sha256sum <path>` for a digest, the counting command for a count, and `git show <rev>:<path>` at both revisions for a revision-bound claim; a mismatch is a dated erratum, never an in-place edit. First instance: `corpus/evidence/round69/c2-receipts/provenance-erratum.txt` (`TREE 27f649f8`, `LANDING 1ec2e60a`, every bound input's sha256 at both revisions, `DIFFERS SKILL.md`), re-derived by gate E3 of `plans/round69_c2_routed_defects.py`.
  Source: `corpus/lessons/round-68.md` `## Mistakes` rows 1–3; `corpus/lessons/round-68-verifier-spotcheck.md` §5 items 3 and 5. This criterion does not rewrite the Q-series criteria above.
```

### 2c. `corpus/lessons/round-68.md` — two one-line additions

Append as a dated section; **if the section already exists, replace its bullets, do not append a second
copy** (E5 is exactly-one).

```
## Corrections (round 69, dated; the round-68 text above is not edited)

- **Strict attack share.** The round-68 report's w1 line counted sentinel, revenger and scout as attack seats (6/12 = 50 %); the run-15 definition is the strict set {reviewer, critic, mutation-tester, labrat}, so the strict attack share is 3/12 = 25 % (floor met exactly) — the wider set is named here and is never counted as attack share again.
- **`w1-results.json` record.** That file carries twelve entries with no seat output — the frozen clause words it `output: ""`, the committed bytes say `"output": null` — under the kernel-restart note; the output record is the twelve per-seat reports under `.ufo/waves/round-68/w1/`, and `results.json` must not be read as the seat-output record for any round.
```

## 3. Findings a claim's attacker should use

**F1 — the routed defect's `output: ""` is not what the committed file says (E6 literal vs bytes).**
`corpus/lessons/round-68-verifier-spotcheck.md` §5 item 6 states 12 entries with `output: ""`. The
committed `.ufo/waves/round-68/w1-results.json` has `"output": null` in all twelve entries
(`grep -o '"output": [^,]*' … | sort | uniq -c` → `12 "output": null`; JSON load → `Counter({'NoneType': 12})`).
Frozen E6 (`plans/round69_c2_routed_defects.py:247-250`) requires the literal `output: ""` in the lesson
line, so a correction line that states the truth alone (`null`) would fail the gate, and a line that states
`""` alone would be false about the bytes. The draft quotes the clause as frozen wording and names the
committed value in the same line; that satisfies E6 and stays true. This is a defect in the routed item's
wording and in the frozen literal — reported, not edited.

**F2 — E1 does not price three of the seven cells the frozen sentence names.** E1
(`:141-167`) checks: cell count ≥ 8, entry path present in cell 2 and file exists, `` `0` `` and `` `1` ``
in cell 3, cell 4 non-empty. It never reads cell 5 (pinned values), cell 6 (write scope) or cell 7 (owner).
Arm m9 (blank owner) → `thin=[]`: a row with an empty owner and empty pinned values passes E1. The frozen
predicate says "a complete row: name, kind, an entry file that exists in the lane, a verdict map naming `0`
and `1`, a self-test cell, pinned values and write scope" — the pass path prices four of seven.

**F3 — E5's role clause is presence-only, so the drift it corrects can still pass.** E5
(`:236-245`) requires all four strict role names to appear on the line; it does not require that no other
role appears. Arm m2 (role list widened to `{reviewer, critic, mutation-tester, labrat, sentinel}`) →
`strict-lines=1`, pass. A line that keeps the phrase "strict attack share" and `3/12` but also names
`sentinel` as attack passes the gate.

**F4 — the Q50 heading cannot carry the round-63/64 title, by construction.** `section()` and
`count_section()` (`:78-96`) match with `ln.strip() == heading`. Arm m10 (heading
`## Round69 criterion — a report citation is re-hashed`) → `headings=0`, section not found. The house-voice
title is therefore in the lead sentence; this is a forced deviation from the round-63/64 heading shape, not
a style choice.

**F5 — the C1 kill rule names two `SETUP` paths the round-68 instrument does not emit.** (Out of this
seat's C2 scope; recorded for the C1 attacker.) `grep -c 'receipt-exists' plans/round68_c1_pypi_finish.py`
→ `0`; the battery writes the receipt unconditionally. `grep -c 'port-8080-occupied' …` → `0`; the literal
lives only in the base probe (`plans/round63_c1_pypi_probe.py:280`, `raise SetupError(...)`), which the
wrapper calls at `plans/round68_c1_pypi_finish.py:145` (`m.require_port_free`) inside `run_battery`, and
`run_battery` has no `except SetupError` — so a busy port surfaces as an uncaught traceback (rc 1), not
`SETUP port-8080-occupied` (rc 2). The claims doc's kill rule names both tokens.

**F6 — the working tree already satisfied all seven C2 checks when this seat ran, uncommitted.** The gate
printed `DEFECTS n=0` / `PREDICATE R69-C2 pass` at HEAD `b288e8e0` with four tracked files dirty. Whether
that state is the landing the L1 will commit is not this seat's call; the drafts here are the conformance
copies (2a adds grounded detail the working-tree rows omit; 2b/2c match the landed shape).

**Grounded as stated, no finding:** strict attack share `3/12` re-derives from the committed results file
(`results[*].agent` → reviewer 1, critic 1, mutation-tester 1, of 12; no labrat seat) — so E5's number is
independently checkable from `w1-results.json`, not only from the spot-check's prose. The twelve per-seat
reports exist as 12 `.md` files in `.ufo/waves/round-68/w1/`.

## 4. Commands I did NOT run

- No C1 battery and no `--check-receipt` on `corpus/evidence/round69/nginx/receipt.txt`; no port-8080
  bind, no `ss -ltnp` probe (this seat's item does not run the battery).
- No `plans/round68_c2_correction_gate.py --selftest` (the frozen round-68 gate's own selftest).
- No `plans/round69_c2_routed_defects.py --selftest` (the round-69 gate's fake-lane arm).
- No separate `plans/round63_gate_checks.py depth|trio` run of my own; those two commands ran only inside
  the gate's E7 as part of command (5).
- No `--render-table` run, no probe/gate selftests of the four round-68 instruments; their self-test
  spellings are quoted from their `print` statements, not from a run.
- No `git`/`jj` write command of any kind; no commit, push, stage, stash, checkout, switch; no edit to any
  tracked file; no `pacman`, `uv`, `npm` or other install (no tool installed this seat).
- No subagent dispatch (leaf).

## 5. Artifacts

- `.ufo/waves/round-69/w1/drafts/registry-rows.md` — four rows + cell-level grounding + deltas.
- `.ufo/waves/round-69/w1/drafts/quality-q50.md` — Q50 paste block + grounding + the heading constraint.
- `.ufo/waves/round-69/w1/drafts/lesson-corrections.md` — two one-line additions + grounding + F1.
- `.ufo/waves/round-69/w1/CorrectionDraft.md` — this report.
- Scratch `/fast/scratch/hyaku/kengaku-r69/CorrectionDraft` (validator + mutation scripts) deleted before
  yield; their raw output is quoted in §1.
