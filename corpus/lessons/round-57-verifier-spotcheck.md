# Round 57 — kengaku verifier spotcheck (non-author closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Closed 2026-11-01. Lane head verified `e8e08b0120123e5634326eed2b1cc67ac13c12d5` (= local
`refs/heads/master` = `ls-remote origin refs/heads/master`); base
`c9ce9a713de770b2cb0c594fe3f9ad5019b64e0f` (the round-56 verifier spot-check tip). All
re-measurements below were run by this judge inside WSL2 Ubuntu-24.04 (python 3.12.3, git,
bwrap, numpy, biopython present; **uv absent**, **pytest absent** — the canonical r56 A3.4
counter environment preserved) on fresh clones of the lane repo checked out as **master**
(ref-sensitive rows require it, per R56-F2), exits captured per the round's relay lesson.
Nothing in the lane repo or fleet repo was mutated; the one tamper below (the sha-refusal
kill re-run) was applied to a judge-owned scratch clone only. The judge's scratch clones on
both filesystems are removed after this closure.

**Verdict up front: admitted.** Both declared claims verify at their named measured
revisions; the four R56 routed defects (V1 load-bearing, V2, V3, V4) are all discharged and
re-verified; the laundering the R56-V1 diagnosis exposed is gone — the full entry-truth
counter prints `laundered=0` at the pushed tip. No owned axis harmed.

## 1. Step-1 conformance

| check | command (abridged) | observed | result |
|---|---|---|---|
| report committed by lane identity | `git -C <fleet> log --format='%an %ae %H' -1 -- .ufo/reports/round-57/kengaku.md` | `kengaku-shokunin kengaku@shokunin.local 56ebe9efc3c696f57b8dc69780822d87e18b792b` | PASS |
| committed report bytes = filed report | `git show 56ebe9ef:<report>` diff vs worktree file | no diff | PASS |
| report lands last | report commit `56ebe9ef` dated 2026-11-01 09:31:47 -0800 (17:31:47Z) vs lane tip `e8e08b01` 17:12:10Z | report after tip | PASS |
| SHONEN heading | read report | `## SHONEN` (report line 145), four `[~]` lines with pointers, no `[x]`; `SHONEN.md` itself: 0 `[x]`, 4 `[~]` | PASS |
| cited commits exist + ancestors + in-range | `merge-base --is-ancestor` for `f754593b`, `c0e7e100`, `44ae8046`, `ca63378d`, `e8e08b01` | all five exist, all ancestors of master, all inside `c9ce9a71..e8e08b01` | PASS |
| branch pushed | `ls-remote origin refs/heads/master` vs local `rev-parse refs/heads/master` | both `e8e08b0120123e5634326eed2b1cc67ac13c12d5` | PASS |
| dispatch/complete digest | orchestrator watchdog `.ufo/watchdog.log:211,239` | `2026-11-01T06:00:10-08:00 launch kengaku round=57 base=c9ce9a713de7 (zcode run14)` / `2026-11-01T09:31:46-08:00 complete kengaku round=57 head=e8e08b012012 pushed=True` | PASS |
| prompt embeds the contract | read `.ufo/prompts/kengaku-round-57.md` | report path + filename, commit-before-report, SHONEN heading, hash-citation rule, write scope all present; no L2 route map quoted | PASS |
| L0 lines durable | `git show HEAD:.ufo/l0-questions.md \| grep -c 'kengaku \| round-56'` | 2 (L2-surface; ledger-schema-v2) — standing disclosure unchanged; no round-57 L0 filed (none needed) | PASS |

Observations (status-neutral, not defects): the watchdog `complete` line (09:31:46 -0800)
precedes the report commit (09:31:47 -0800) by one second — the driver's signal fired on the
report file's appearance, the orchestrator committed a second later; ancestry + authorship,
the binding tests, both pass (same class as r54's timing observation).

## 2. Claim re-checks

### R57-C1 — operability 9→10 — RE-MEASURED, verifies

Before-state re-derived by this judge at base `c9ce9a71` (WSL, fresh master checkout, /mnt/c
clone) — matches the committed before-receipts `.ufo/waves/round-57/fix/c1-before-*.txt`:

```
=== registry at base ===          (this judge, exit 1)
ADVERTISED total=83
REGISTERED total=82 rows=84
MISSING 1
  MISSING plans/round56_landcheck.py
PREDICATE R52-C2 fail
REG-EXIT=1
```

Full entry-truth at base (this judge, WSL native-fs clone, jobs 6, timeout 900):
`laundered=2` with `LAUNDERED round52-c2` + `LAUNDERED routed-findings`,
`PREDICATE R55-C2 fail`, exit 1 — see the observed block at the end of §2 (BASE run).

After-state re-derived by this judge at the pushed tip `e8e08b01` (WSL, fresh master
checkouts) — all three instruments the CLOSURE-PREP names reproduce green:

```
=== registry at tip ===           (this judge)
ADVERTISED total=84
REGISTERED total=84 rows=86
MISSING 0
PREDICATE R52-C2 pass
REG-EXIT=0

=== landcheck at tip ===          (this judge)
[PASS] L-reg registry closure (MISSING 0, PREDICATE R52-C2 pass)
[PASS] L-chess chess probe re-run == committed receipt (cases=12 observed_pass=5 observed_fail=7 mismatches=0)
[PASS] L-selftest entryargv selftest (4/4 PASS)
[PASS] L-grader grader replay+selftest (CHECKS n=733 mismatches=0, ALL PASS)
LANDCHECK PASS n=4
LC-EXIT=0

=== entryargv full at tip ===     (this judge, jobs 6, timeout 900)
ROWS registry=85 ledger=85 missing=0 extra=0 argv_defect=0 wrapper_defect=0 abbrev_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
BINDING l1=0 l2=0 l3=0
SOURCE rev=e8e08b0120123e5634326eed2b1cc67ac13c12d5 clean=yes lane_rev_equal=yes
RUN executed=85 timeout=0 mismatched=0 evidence_missing=0 laundered=0
TIPSTATE entry_declared_green=51 entry_declared_red=34 observed_green=51 observed_red=34
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R55-C2 pass
TIP-FULL-EXIT=0
```

Byte-equivalent in every predicate field to the committed
`.ufo/waves/round-57/integrate/tipd-*.txt` (whose SOURCE rev names the earlier close tip
`ca63378d`; this judge re-derived at the final pushed tip `e8e08b01` — the round-56
closure's "re-derive at lane head" instruction now reproduces at the pushed head, which is
exactly the property C1 claims). The tip-C receipts (`.ufo/waves/round-57/integrate/tipc-*`)
honestly hold the intermediate red state the round's own machinery caught
(`LAUNDERED round50-c2`, `EVIDENCE-MISSING round35-c1-coverage`, `PREDICATE R55-C2 fail`,
exit 1) before the `ca63378d` fix — the capture-before-closure chain is committed.

**Verdict: improved (9→10).** The property "every advertised command is registered and
green at the branch tip" is what the two counters measure; at 9 the r56 close held it only
at its measured revision (R56-V1 is exactly that gap). Do-nothing control holds: the
committed before-receipts and this judge's base re-runs show the same commands red at base;
the fix is byte-level rows (registry row, ledger row, source-cell correction) — a no-op
cannot turn them green.

### R56-V1 root causes — BOTH verified landed, laundering stopped

- **Root cause 1 (unregistered advertisement):** `SKILL.md:647` at the tip now carries the
  full `round56-landcheck` gate row (entry command, verdict map 0/1/2 with measured
  fragments, self-test spelling, pinned-value paths, write scope, owner). The registry
  counter's `ADVERTISED total=84 / REGISTERED total=84` and `MISSING 0` re-derived above is
  the direct measurement.
- **Root cause 2 (findings-row source shape):** `corpus/routed-findings.jsonl` R56-F2 row
  now reads `"source": "corpus/lessons/round-56.md:60"` (strict `<path>:<line>`), with the
  correction history appended inside the row's `note` ("Round-57 correction: the source
  field was landed as 'corpus/lessons/round-56.md:Corrections' at d834d89d … corrected to
  the strict shape"). The `LAUNDERED routed-findings` line is gone from the tip counter.
- The wave-A diff (`c9ce9a71..f754593b`) touches exactly the bytes the fix names: SKILL +1
  line (the landcheck row), entrytruth ledger +10 (landcheck row), routed-findings 1 line
  rewritten (R56-F2), PROVINCE 1 cell, SCORECARD +16, LOG +51, before-receipts.

### R56-V2/V3/V4 — verified landed

- **V2:** `PROVINCE.md:113` SF14 cell now reads "197 rows (round 57 re-count 2026-11-01:
  … → 197, incl. S203/S204; the round-56 re-count wrote 195 — that round's BEFORE count …
  corrected in place, dated, per the round-56 non-author closure's R56-V2…". Re-counted by
  this judge: the cell's 197 was true when written (wave A predates wave B's four new rows);
  the tree at the tip counts 201, named correctly in the round-57 section and registry.
- **V3:** `SCORECARD.md` (round-56 section, appended block dated 2026-11-01, cells above
  stay as written): "seventeen" decomposed as **14 literal green→red flips + 2 already-red
  fragment refreshes + stage-scan's argv re-declaration**; "sixteen declared-green rows
  false" corrected to **14 declared-green-measured-false + 2 rows declared red at base**.
  Matches this judge's r56 re-derivation exactly.
- **V4:** the round's writers are byte-stable over existing rows — re-verified by diff:
  `c9ce9a71..f754593b` re-encodes nothing (routed-findings: exactly one line changes, the
  R56-F2 row itself; entrytruth: pure insertion plus the dated fragment refresh). The
  lesson's `## Mistakes` landing row records the brace-indent bug the pre-commit
  `json.load` validation caught before any commit.

### R57-C2 — coverage, held at its L0 cap, predicate met — RE-MEASURED + RE-OPENED, verifies

**Freeze ordering (predictions before captures) — verified.** The claims freeze
`plans/round-57-claims.md` at `c0e7e100` carries the 24-case prediction table (22 P/F + 2
U) with per-case static readings, states the plumbing was proven on a toy grader only, and
states the capture was never executed before the freeze. The instrument
`plans/round57_c2_eigen_probe.py` in the same commit embeds the same frozen `CASES` table
and self-pins its own sha256 in the claims file. This judge re-hashed the probe at both
`c0e7e100` and `e8e08b01`: `4f2b8bebb451c5f67d26dc06c76dbd99f3a459f41d9e8a8d555af12d15e0f105`
— matches the freeze's pin at both tips. The first-run receipt's `predicted=` column can
only come from that frozen table, and a post-hoc table fitted to observations would not
carry two U designations whose observed values split across runs — the structural evidence
is consistent with predictions-before-data and inconsistent with the contrary.

**First run — re-measured.** This judge re-ran the probe green at `e8e08b01` (WSL, bwrap,
judge-owned clone):

```
SELFTEST cases=2 failures=0 (toy grader + toy candidates; TB2 capture untouched) exit 0
cases=24 observed_pass=14 observed_fail=10 mismatches=0 setup=0
OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=F
PREDICATE R57-C2 pass
PROBE-EXIT=0
```

(This judge's re-run observed 14/10 with both U cases F — a third distinct split across the
three recorded runs; `mismatches=0` holds under every split because U cases are
observed-only by design. The committed first-run receipt — `cases=24 observed_pass=15
observed_fail=9 mismatches=0 setup=0`, U split F/P — is byte-equal to the pinned
`corpus/evidence/round57/eigen-probe.txt`, sha256 re-derived
`463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784` = the registry row's
pin. The committed bare re-run receipt `.ufo/waves/round-57/claims/c2-bare-run.txt` shows
the 14/10 F/F flip, `rc=0 sec=6.23`.)

**U-case honesty — verified.** In every committed receipt and both judge re-runs the two
timing-equal cases print `predicted=U … (observed-only)` and are excluded from the
mismatch count; the runs' flips (F/P, then F/F, then F/F) are recorded as the grader-class
finding "timing-equal is host noise" in the report/knowledge entry/PROVINCE — never
laundered into a P/F prediction.

**Sha-refusal kill — re-fired by this judge.** Committed receipt
`claims/c2-sha-kill.txt`: `SETUP grader sha256 418ba750… != frozen pin cdc58e3a…`,
KILL-RC=2. This judge re-tampered a judge-owned clone (one byte substituted inside
`tests/test_outputs.py`, length unchanged):

```
SETUP grader sha256 544ee12e397b3fd931d2abac9d9572490b8c3ae3c9b600b3e82436ec1243587e != frozen pin cdc58e3aa0960dac2e12a12b1cfa4131237d697762a6a78ebf33f80d2eb168ce
KILL-EXIT=2
```

**Capture identity — re-opened live.** All four pinned sources re-fetched at pin
`2fd12b88aafdd04a52c298e3940bcb189f9766d6` (curl GET, 2026-11-01), sha256 over fetched
bytes — all four match the claims-freeze pins and the committed capture bytes exactly:

| file | sha256 (this judge) | match |
|---|---|---|
| `task.toml` (S205) | `f7b9b7dda446f969a3ce88f61039d216f4d58b5fc5c10ff9faa24e2403bbd830` | YES |
| `tests/test_outputs.py` (S206) | `cdc58e3aa0960dac2e12a12b1cfa4131237d697762a6a78ebf33f80d2eb168ce` | YES |
| `solution/solve.sh` (S207) | `8f414e50ce29f21ae26c423d74949b257073e95318ca5f5a95c2d9a90bfe93c2` | YES |
| `instruction.md` (S208) | `6fa938389f99648508e5a9772e0d5e95d1102738c68d1ff61bd65469d76c52ab` | YES |

Located quotes re-verified byte-true at the cited lines: `task.toml:6` contains the 16-word
performance-objective quote; `tests/test_outputs.py:111` is
`assert dt < ref_dt, f"…"` and `:15` is `_np_linalg_eig = np.linalg.eig` (the
anti-monkeypatch pre-capture — a corpus first, correctly read); `solution/solve.sh:14` is
`solver = eigenpy.EigenSolver(matrix)` (the maintainer oracle);
`instruction.md:4`/`:5` carry the speed requirement and the median protocol.

**Ground moved — re-counted.** `grep -c 'fourteenth' PROVINCE.md` → 3 at the tip; at base
the same command returns **1**, not the 0 the report/claims/SCORECARD cite — the base
occurrence is the round-56 section's own negation ("this round adds the oracle, **not a
fourteenth task**", `PROVINCE.md:683`), so the before→after by the plain cited command is
1→3, and 0→3 only for occurrences this round added (see the R57-W1 observation below —
status-neutral; the load-bearing before-controls all verify: `grep -c S205
corpus/SOURCES.md` → 0 at base, re-derived; the probe instrument absent at base,
re-derived; SOURCES rows 197 → 201, base recount by this judge: 197); knowledge entry
`corpus/knowledge/tb2-largest-eigenval-grader.md` carries the full provenance trio (four
pinned S-rows with sha256, `verified-at` with the receipt hash, `recheck: 180d` naming both
re-verification commands); `corpus/README.md:85` index row present; PROVINCE names 14 of 89
with the refusal list unchanged; capability `timing-gate-grader-probe` enters the
SCORECARD table with the probe as its evidence pointer and first-working round 57.

**Verdict: predicate met, score HELD at 7** — the claim's own L0 design (the unanswered
`kengaku | round-25/33/51` cap), the admitted r56-C3 shape; graded **unchanged** on the
score with the expansion credited in the trend (§4), honestly declared by the lane.

### Before/after counting commands (C2) — re-run by this judge

- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`: base 197 → tip 201.
- `grep -c 'fourteenth' PROVINCE.md`: base 1 (the r56 section's "not a fourteenth task"
  negation, `PROVINCE.md:683`) → tip 3 — the report/claims/SCORECARD cite 0 at base; see
  R57-W1 below.
- `git show c9ce9a71:plans/round57_c2_eigen_probe.py` → absent; present at tip.
- `grep -c S205 corpus/SOURCES.md`: base 0 → tip 1.

## 3. Census (re-run)

`bash <fleet>/scripts/sources-census.sh validate --root <fleet> kengaku` → **exit 0**,
verdict `ok`, the same 15 pre-existing W04 duplicate-url warnings — byte-consistent with
the committed `integrate/census-end.txt` (exit 0) and `census-start.txt`. S205–S208 rows
are shape-clean (11 columns, tier A on spec/docs/code kinds, mined with used-by paths that
resolve).

## 4. Trend + axis verdicts (this judge)

- **expansion: improved** — agreed. Ground moved where the coverage map did not hold: the
  fourteenth TB2 grader read and executed, and it is a class the corpus lacked (a
  wall-clock cost predicate — the executed corpus's first non-content gate). Registry
  197→201, frontier 13→14 of 89, one capability enters, one knowledge entry admitted citing
  four mined tier-A rows. The score stays 7 by the lane's own standing L0 design and the
  report says so instead of moving a capped number — the honest form.
- **quality: improved** — agreed and re-measured: the pushed tip re-runs its whole
  advertised self-assessment surface green from one command per counter (registry
  `PREDICATE R52-C2 pass`, entry-truth `executed=85 … laundered=0` / `PREDICATE R55-C2
  pass`, `LANDCHECK PASS n=4` — all at `e8e08b01`, all by this judge); the writers that
  landed data are byte-stable over existing rows (diff-verified); the probe refuses drifted
  captures (kill re-fired, exit 2).
- **discernment: improved** — agreed: predictions frozen before the first capture run with
  an honest U class for the two cases static reading cannot decide (the runs then
  demonstrated the flip empirically — recorded, not laundered); the round-56
  self-assessment's overcounting labels corrected by a dated precision block at an
  unchanged score (V3); the V1 fix extended to the second root cause (the F2 source shape)
  instead of stopping at the named one; and the round's own tip counters caught its own
  wave-C mistakes (the 40-hex pin, the stale r35 fragment) before any closure — the
  captured mistake is mined in the lesson with a reusable rule (grep `[0-9a-f]{40}` before
  landing corpus-ground prose).

Axis verdicts: operability **improved** (9→10, re-measured), coverage **unchanged**
(predicate met, score held 7 by L0 design; the new ground counts under the expansion trend),
depth/freshness/novelty/adjacency/calibration **unchanged** (SCORECARD diff base→tip is
append-only — zero removed lines; the r56 numbers stand: depth 9, freshness 9, adjacency 9,
novelty 8, calibration 10). **No axis harmed.**

Re-measured by this judge: registry + landcheck + full entry-truth at the tip; registry +
full entry-truth at base; probe selftest, probe green re-run, sha-refusal kill (judge-owned
tamper); all four source re-fetches + hashes + quotes; census validate; SOURCES/PROVINCE/
SCORECARD/LOG/SKILL/entrytruth/routed-findings diffs; probe and freeze sha pins.
Evidence-verified from committed bytes: the before-receipts' internal consistency, the
freeze document, the tipc red capture, the LOG round-57 entries (both waves), the knowledge
entry, the lesson's Gate/Mistakes tables, assimilation cross-check (`considerthese/` 8
files; `plans/round_close.py` and `plans/tip_receipts.py` exist = the two "already
implemented" proposals; the r52-repair refusal stands on the round-54 records).

## 5. Spot-check table (LEARNING.md discernment — ≥1 admit + ≥1 reject-equivalent)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S205 `task.toml` | admit A (spec) | pinned raw URL re-fetched live 2026-11-01, sha256 match, `:6` quote byte-true (16 words ≤ 25) | **agree** | the task's machine-readable self-definition declares a PERFORMANCE objective — the first such task this lane has read; tier A is correct for the task's own spec |
| S207 `solution/solve.sh` | admit A (code) | pinned raw URL re-fetched live, sha256 match, `:14` = `solver = eigenpy.EigenSolver(matrix)` | **agree** | the oracle is read from maintainer code, not inferred: the intended fast-correct answer is the same eigensolve behind a C++ binding — exactly what the probe's `eig-bare` candidate tests |
| eig-bare-speed U at freeze | honest-undecidable mark (reject-equivalent: declined to guess P or F) | claims freeze prediction table + three runs' OBSERVED-U lines (F/P, F/F, F/F) | **agree** | a candidate identical to the reference algorithm makes `dt < ref_dt` a coin-flip of host noise — not derivable from the grader's static semantics; the empirical flips vindicate the U; laundering it into a prediction would have been the calibration failure |
| r52-repair proposal refusal (assimilation) | standing reject (proposal refused on its demonstrated regression) | `considerthese/2026-10-26.md`; round-54 records (round52-c2 regression receipt advertised79/registered77/missing2/exit1) | **agree** | the regression it would re-land is exactly what this round's C1 repairs and re-measures green; refusal stays correct |

No new rejection rows this round (all four opens admitted; the lesson says so) — the U-mark
decision and the standing proposal refusal are sampled as the round's reject-equivalents.

## 6. Findings, SHONEN, routed items

- **R57-W1 (number-drift, status-neutral — named, not barring).** The C2 before-count as
  cited in the report, the claims freeze, and the SCORECARD C2 row —
  `grep -c 'fourteenth' PROVINCE.md` → 0 at base — re-measures as **1** at base
  `c9ce9a71`: the round-56 PROVINCE section already contained the word inside its own
  negation ("this round adds the oracle, not a fourteenth task", `PROVINCE.md:683`). The
  before→after by the plain cited command is 1→3; the round's real controls
  (S205 absent at base, probe instrument absent at base, SOURCES 197 at base) all verify.
  Likely cause: counting occurrences in the round-57 section only, or writing the freeze
  before re-running the grep against the base bytes. Fix next round: re-run each cited
  before-command against the base commit's bytes (`git show <base>:<path> | …`) before
  freezing it, and put a dated erratum line in the round-58 report naming the superseded
  0.
- **No other new routed defects.** All four R56 routed items (V1–V4) are discharged and
  re-verified above. Carried open, named by the lane and unchanged by this closure:
  `round50-c1` population-pin root cause (125/126 fixture identities under host rebuilds);
  R56-F1 `anchor_line_check.py` QUOTE_RE repair as its own frozen claim with falsifier
  fixtures (routed twice; planned r58); L0 questions `kengaku | round-25/33/51` (coverage
  cap) and `kengaku | round-56` (L2 surface; ledger-schema-v2 host column) — nothing
  assumed answered.
- **Minor conformance observations (status-neutral):** (1) the lesson's `## Mistakes`
  evidence column cites this round's scratch transcripts, which the round contract's own
  finish rule deletes; the durable per-class evidence exists in committed receipts
  (`tipc-entryargv-full.txt` captures the same trap's effect for the 40-hex mistake) —
  future lessons should cite committed paths for mistake evidence. (2) The PROVINCE SF14
  cell says 197 while the tip tree holds 201 — the cell is dated and scoped to its
  re-count moment (wave A) and the round-57 section carries 201; a one-word refresh next
  time the file is touched would remove the ambiguity.
- **SHONEN:** all four boxes `[~]` with resolvable pointers, no `[x]` anywhere in
  `SHONEN.md` or the report. Spot-checks: SKILL.md carries the registry (85 rows incl. the
  landcheck and the eigen probe, both measured this round — re-verified) and decision
  tables; LOG round-57 entries present (both waves); box 3 is evidenced by this closure
  itself — every measurement above ran from committed instructions alone, fresh session,
  fresh clones; PROVINCE round-57 section dated. All four look fully checkable by a
  non-author — the operator may want to run that gate; this judge did not write `[x]`.

## 7. Judge-run receipts (summary)

Tip `e8e08b01`, WSL Ubuntu-24.04, master checkouts, uv/pytest absent: registry
`PREDICATE R52-C2 pass` (exit 0); landcheck `LANDCHECK PASS n=4` (exit 0); entryargv full
`executed=85 timeout=0 mismatched=0 evidence_missing=0 laundered=0`, TIPSTATE 51g/34r
declared equal to observed, `PREDICATE R55-C2 pass` (exit 0). Base `c9ce9a71`: registry
`ADVERTISED total=83 / REGISTERED total=82 rows=84`, `MISSING plans/round56_landcheck.py`,
`PREDICATE R52-C2 fail` (exit 1); entryargv full:

```
ROWS registry=83 ledger=83 missing=0 extra=0 argv_defect=0 wrapper_defect=0 abbrev_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
BINDING l1=0 l2=0 l3=0
SOURCE rev=c9ce9a713de770b2cb0c594fe3f9ad5019b64e0f clean=yes lane_rev_equal=yes
  LAUNDERED round52-c2 declared green, entry exit=1
  LAUNDERED routed-findings declared green, entry exit=1
RUN executed=83 timeout=0 mismatched=0 evidence_missing=0 laundered=2
TIPSTATE entry_declared_green=49 entry_declared_red=34 observed_green=47 observed_red=36
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R55-C2 fail
BASE-FULL-EXIT=1
```

— byte-equivalent in every predicate field to the committed before-receipt
`fix/c1-before-entryargv-full.txt`. The base block above was re-derived by this judge; the
same red state also reproduced on an /mnt/c clone (registry leg). Both scratch clone sets
(/mnt/c and native-fs) are removed after closure.
