# Round 58 — kengaku verifier spotcheck (non-author closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Closed 2026-11-02T04:21Z. Lane head verified `46fe53981572865698017b22abea3572e6ebeee2` (=
local `refs/heads/master` = `ls-remote origin refs/heads/master`); base
`a6b209cf434dae69f924858b4ea9a1bcf015eecc` (the round-57 verifier spot-check tip). All
re-measurements below were run by this judge inside WSL2 Ubuntu-24.04 (python 3.12.3,
bwrap 0.9.0, git 2.56.0, numpy 2.5.4; uv/pytest absent — the canonical r56 A3.4 counter
environment preserved) on judge-owned clones taken from a git bundle of the lane repo
checked out as master at the pushed head, plus a base clone detached at `a6b209cf`; exits
captured from script files (the relay lesson). Nothing in the lane repo or fleet repo was
mutated; the one tamper (the sha-refusal kill re-fire) was applied to a judge-owned clone
only. All judge scratch clones are removed after this closure.

**Verdict up front: admitted.** All three declared claims verify — C1 and C2 re-measured at
BOTH ends (base red, tip green) by this judge; C3 re-measured live (probe re-run 48/48 on
the frozen zero-U table, kill re-fired). The closure chain the host note names holds:
125/126 deterministic drift with sole matcher `n10-empty-repo`, double-build discriminator
`match_b1=1 unstable=0`, re-pin `f41db91b` dated with rows byte-preserved outside the tree
column, `PREDICATE R50-C1 pass` re-derived at the tip. The repaired r46 instrument's
selftest re-runs 6/6 and the four supersessions S213–S217 are contract-shaped Q34
correction rows. The prediction table structurally predates the capture run (freeze
commit). Five of the six repair-cascade breaks verified with committed evidence. No owned
axis harmed (SCORECARD diff is 47 insertions, 0 deletions; every axis-history row
byte-identical base→tip).

## 1. Step-1 conformance

| check | command (abridged) | observed | result |
|---|---|---|---|
| report committed by lane identity | `git -C <fleet> log --format='%an %ae %H %cI' -1 -- .ufo/reports/round-58/kengaku.md` | `kengaku-shokunin kengaku@shokunin.local cc463ef80579f0465194dda0e3dfa85074e5fb9f 2026-11-01T18:34:41-08:00` | PASS |
| committed report bytes = filed report | `git show cc463ef8:<report>` diff vs worktree file | no diff | PASS |
| SHONEN heading | read report | `## SHONEN` (report line 157), four `[~]` lines with pointers, no `[x]`; `SHONEN.md` itself: 0 `[x]`, 4 `[~]`, untouched in range | PASS |
| cited commits exist + ancestors + in-range | `rev-parse --verify` + `merge-base --is-ancestor` for `d6bc6027`, `0e60ec31`, `f58c0d6a`, `c39d0e40`, `b0b1d729`, `201a6a08`, `9defcad6`, `f93db89b`, `3cf16a42`, `bf48fd2072`, `46fe5398` | all eleven exist, all ancestors of master, all inside `a6b209cf..46fe5398` | PASS |
| branch pushed | `ls-remote origin refs/heads/master` vs local `rev-parse refs/heads/master` | both `46fe53981572865698017b22abea3572e6ebeee2` | PASS |
| dispatch/complete digest | fleet `.ufo/watchdog.log:263,305` | `2026-11-01T12:06:52-08:00 launch kengaku round=58 base=a6b209cf434d (zcode run14)` / `2026-11-01T18:34:40-08:00 complete kengaku round=58 head=46fe53981572 pushed=True` — matches the contract's digest | PASS |
| prompt embeds the contract | read `.ufo/prompts/kengaku-round-58.md` | report path + filename, commit-before-report, SHONEN heading, hash-citation rule, write scope, push scope, L0 channel all present | PASS |
| L0 questions durable + unassumed | `git show HEAD:.ufo/l0-questions.md \| grep 'kengaku \| round'` | `round-25` (x2, coverage cap + novelty conversion), `round-33`, `round-51`, `round-56` (x2) all still open — nothing assumed answered; the coverage score is held at 7 again with the cap named | PASS |

Observation (status-neutral, same class as r57): the watchdog `complete` line
(18:34:40 -0800) precedes the report commit (18:34:41 -0800) by one second — the driver's
signal fired on the report file's appearance; ancestry + authorship, the binding tests,
both pass.

## 2. Claim re-checks

### R58-C1 — operability, the R56-F1 QUOTE_RE repair — RE-MEASURED at both ends, verifies

Before-state re-derived by this judge at base `a6b209cf` (WSL, fresh checkout):

```
=== anchor_line_check at base ===   (this judge, exit 1)
ROW S201 state=live defects=line:1
ANCHORLINE rows=201 cited=59 captured=52 uncaptured=7 defective=9 repaired=8 live=1 cells=1
ANCHOR-BASE-EXIT=1

=== round46_c2_verify at base ===   (this judge, exit 1)
A anchorline live=1 repaired=8 base_rows=149 base_missing=0 base_changed=0 DEFECT
B predictor states=16 grader_pass=10 grader_fail=6 disagree=0 ok
C entry source_ranges=9 source_ranges_bad=0 errata_marks=5/5 ok
D selftest exit=0 ok
checks=4 defects=1
PREDICATE C2 fail
R46C2-BASE-EXIT=1
```

Byte-equivalent in every predicate field to the committed before-receipts
`.ufo/waves/round-58/recon/anchor-before.txt` and the claims doc.

After-state re-derived by this judge at the pushed head `46fe5398`:

```
=== anchor_line_check --selftest ===  (this judge, exit 0) — 6/6
SELFTEST RED      rc=1 want_rc=1 ok
SELFTEST GREEN    rc=0 want_rc=0 ok
SELFTEST JUNK     rc=1 want_rc=1 ok
SELFTEST ESC-GOOD rc=0 want_rc=0 ok   (the pre-repair false positive — now clean)
SELFTEST ESC-RED  rc=1 want_rc=1 ok   (true positive retained: line:1)
SELFTEST ESC-WORDS rc=1 want_rc=1 ok  (the exposed miscount class: words:1)
SELFTEST pass / SELFTEST-EXIT=0

=== anchor_line_check --lane . ===   (this judge, exit 0)
ROW S201 state=repaired by=S213 defects=words:1
ANCHORLINE rows=210 cited=64 captured=57 uncaptured=7 defective=9 repaired=9 live=0 cells=0
ANCHOR-EXIT=0

=== round46_c2_verify --lane . ===   (this judge, exit 0)
PINS total=3 mismatched=0
A anchorline live=0 repaired=9 base_rows=149 base_missing=0 base_changed=0 ok
B predictor states=16 grader_pass=10 grader_fail=6 disagree=0 ok
C entry source_ranges=9 source_ranges_bad=0 errata_marks=5/5 ok
D selftest exit=0 ok
checks=4 defects=0
PREDICATE C2 pass
R46C2-EXIT=0
```

**S213–S217 supersessions — verified in the committed bytes.** S213's `teaches` opens
`supersedes S201 —` (contract-shape Q34 correction), carries the SAME capture sha256
`a540714e…8f286` as S201 and the corrected `(5 words)` anchor (the quote
`assert sorted(move) == sorted([\"g2g4\", \"e2e4\"])` is 5 tokens by whitespace split —
re-counted by this judge); S201's landed cells stay untouched (corrections are new rows,
never rewrites — correct discipline). S214/S215/S216 supersede S111/S112/S113
(configure-git-webserver, unescaped inner quotes) and S217 supersedes S140 (elided quote),
same source URLs and captures. The repair exposed real defects and the round declared them
as born-closed findings R58-F1 (S201 words miscount) and R58-F2 (the four
unescaped/elided anchors) rather than silently fixing the cells — the honest form.

Falsifier receipts (committed, evidence-verified): `recon/esc-falsifier.txt` shows the OLD
checker false-positiving `line:1` on fx-good and hiding the words defect on fx-words —
measured at base BEFORE the fix. One receipt bug found, see §5 defect (b): the
fixed-checker receipt's per-fixture `exit=` labels contradict its own selftest `rc=` lines
(payloads correct).

**Verdict: improved (operability held at ceiling 10, as the freeze itself predicted).**
The gate's verdict is now correct on the full registry sample with falsifier fixtures in
both directions. Do-nothing control holds: the committed before-receipts AND this judge's
base re-runs show the same commands red at base; the fix is a regex + fixtures + supersession
rows — a no-op cannot turn them green.

### R58-C2 — freshness 9→10, the round50-c1 root cause + re-pin — RE-MEASURED at both ends, verifies

The closure chain, verified piece by piece:

- **125/126 drift at base** — re-derived by this judge (full run, WSL native-fs clone at
  `a6b209cf`): `POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69
  mismatched=125 build_errors=0`, `HONEST fixtures=126 admitted=126 refused=0 error=0`,
  `REFUSALS total=20 clean=20`, `SEALED total=12 clean=12` + `SEALED total=20 clean=20`,
  `MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met`, `PREDICATE R50-C1 fail` —
  byte-equivalent in every predicate field to the committed `recon/round50-before.txt`
  (including the 8 named `POPULATION-MISMATCH` lines; exit 1 per the gate's frozen verdict
  map). Every other leg green — the drift is the pin, not the fixtures.
- **Sole matcher `n10-empty-repo`** — the committed discriminator
  `recon/r50-ev2n/table2.txt` reads `TOTAL rows=126 match_b1=1 unstable_b1v b2=0` with
  exactly 125 `DRIFT det=Y` lines, one `MATCH det=Y n10-empty-repo
  plans/honest50/modules/novel48/n10_empty_repo.py` (line 106), and an empty `UNSTABLE:`
  section (re-counted by this judge from the committed bytes). `recon/r50-ev3n/stability.txt`:
  `STABILITY stable n10-empty-repo EQ-pin builds=18993be1,18993be1,18993be1` — stable and
  EQ-pin across 3 rebuilds. The root-cause claim (the pin froze git-plumbing store bytes no
  cross-host rebuild reproduces; n10-empty-repo is the only fixture whose build runs no git
  plumbing beyond `git init`) is consistent with all committed tables.
- **Re-pin `f41db91b`, dated, rows byte-preserved** — `sha256(population.txt @ c39d0e40)` =
  `f41db91b8dc430f2d4137d47cf71ea10474fdc4988982cdab03ba57cd7fd26c3` = `POPULATION_SHA` in
  `plans/round50_c1_verify.py:72` (recomputed by this judge); the old file hashes to
  `b5197f94…fae69` at base (the stale pin, as named). Diff base→re-pin: ONLY the tree-sha
  column changes plus a dated header block (2026-11-01, receipts named); every row's other
  columns are byte-identical (this judge's column-wise diff: `ALL-OTHER-COLUMNS-IDENTICAL`).
  SKILL registry cell and the ledger row name both pins with the root cause (read).
- **`PREDICATE R50-C1 pass` at tip** — re-derived by this judge (full run at `46fe5398`):
  `POPULATION fixtures=126 pin=f41db91b… mismatched=0 build_errors=0`, `HONEST
  fixtures=126 admitted=126 refused=0 error=0`, `REFUSALS total=20 clean=20`, `SEALED
  total=12 clean=12` + `SEALED total=20 clean=20`, `MUTANTS total=15 caught=15 broken=0
  floor=12 verdict=met`, `PREDICATE R50-C1 pass`, `R50-TIP-EXIT=0`.

**Verdict: improved (freshness 9→10).** The last stale pinned expectation is root-caused
from measurements (branch A chosen from the discriminator's data, not hope) and re-resolves
in-repo on the live host. Do-nothing control: the base run red with 125 mismatches is
committed AND re-derived by this judge.

### R58-C3 — coverage (lowest owned axis, L0-capped), the fifteenth grader — RE-MEASURED + RE-OPENED, verifies

**Freeze ordering (prediction table predates the capture run) — verified structurally.**
The freeze commit `d6bc6027` adds `plans/round-58-claims.md` (the 12-case × 4-leg, zero-U
prediction table with per-case static readings), the probe `plans/round58_c2_kl_probe.py`,
the oracle note, and the four capture files — but NOT the run receipt: `kl-probe.txt` first
lands at `b0b1d729` (two commits later; `git log --diff-filter=A` re-derived). The probe's
frozen self-pin sha256 `51c192f2…760` in the claims doc equals the probe's sha256 at the
freeze, at wave P, and at the tip (recomputed at all three revisions). A post-hoc table
fitted to observations would not match a re-run 48/48 with zero U — and this judge's
independent re-run reproduces the frozen table cell-for-cell (below).

**Probe re-run — re-measured green by this judge at `46fe5398`:**

```
SELFTEST toy-ok got=P/P want=P/P ok / toy-off got=P/F want=P/F ok / SELFTEST pass (exit 0)
CASE sol predicted=P/P/P/P observed=P/P/P/P ok
CASE uniform predicted=P/P/P/F observed=P/P/P/F ok
CASE kb-only-m7 predicted=P/P/P/F observed=P/P/P/F ok
CASE minzero predicted=P/P/F/F observed=P/P/F/F ok
CASE negatom predicted=P/P/F/F observed=P/P/F/F ok
CASE nanatom predicted=P/P/F/F observed=P/P/F/F ok
CASE sumdrift predicted=P/P/F/P observed=P/P/F/P ok
CASE wrongvocab-m5 predicted=P/F/P/F observed=P/F/P/F ok
CASE twod predicted=P/F/P/P observed=P/F/P/P ok
CASE maxover predicted=P/P/F/F observed=P/P/F/F ok
CASE tolbnd predicted=P/P/P/P observed=P/P/P/P ok
CASE intcounts predicted=P/P/F/P observed=P/P/F/P ok
cases=12 legs=48 mismatches=0 setup=0 predicted_u=0
PREDICATE R58-C3 pass / KL-EXIT=0
```

All 48 predictions match the frozen table (compared cell-by-cell against the claims doc).
Committed receipt `corpus/evidence/round58/kl-probe.txt` sha256 re-derived =
`3c93e06a88a6ec8e77b0ed1b81ad298a492513e3f5e7c9f20d6641da5ee53c1f` = the registry row's
pin.

**Sha-refusal kill — re-fired by this judge** (one comment line appended to the capture in
a judge-owned clone): `SetupError: grader sha256 4c016c84…d6c != frozen pin
02bca54d…b4ed`, `KILL-EXIT=1` — matching the dated correction exactly (the freeze wrote
exit 2; measured 1; the drifted capture is never materialized nor executed).

**Capture identity — re-opened live** (curl GET at TB2 pin `2fd12b88`, 2026-11-02): all
four fetched sha256s match both the committed capture bytes and the S209–S212 anchors:

| file | sha256 (this judge) | committed capture | row anchor | match |
|---|---|---|---|---|
| `task.toml` (S209) | `70c8e73cafd0a75306375bec2c2e1e4d82e0cb969fd7e38a63e7c344de43b681` | same | `70c8e73cafd0a753…` | YES |
| `tests/test_outputs.py` (S210) | `02bca54db4849b7c911253fb92f941e21db8b1eea13261a7e5a9871fca68b4ed` | same | `02bca54db4849b7c…` | YES |
| `solution/solve.sh` (S211) | `19daaee18d534f36679854b0ba5727290df389ee023ebb67846cb89579d38bbe` | same | `19daaee18d534f36…` | YES |
| `instruction.md` (S212) | `aba2e1835b2f827686402c3d3ff9b309aab8c9cbac26e23fc46aaeb34e958915` | same | `aba2e1835b2f8276…` | YES |

**Located quotes — re-verified byte-true at the cited lines:** `task.toml:6` carries the
17-word dual-KL description; `tests/test_outputs.py:80` is `assert kf_error <= TOL, (` and
`:10` is `TOL = 1e-3`; `solve.sh:122` is the 19-word backward-KL residual
`E2 = A * lh + B * lm + C * ll + V * (LOG_V + TARGET)`; `instruction.md:3` opens with the
15-word LLM-confidence sentence. All ≤ 25 words.

**Ground moved — re-counted.** `git show a6b209cf:PROVINCE.md \| grep -c fifteenth` → 0
(rc 1, this judge); at tip `grep -c fifteenth PROVINCE.md` → 2 (lines 734/736, both in the
round-58 section, neither a negation — checked); `git show a6b209cf:corpus/SOURCES.md \|
grep -c S209` → 0 (rc 1); `git cat-file -e a6b209cf:plans/round58_c2_kl_probe.py` →
absent; SOURCES rows 201 → 210 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`, this
judge, both ends). Knowledge entry `corpus/knowledge/tb2-distribution-search-grader.md`
carries the provenance trio (four S-rows, `verified-at` with the receipt hash, `recheck:
180d` naming the re-run command); PROVINCE names **15 of 89**; capability
`tolerance-band-grader-probe` enters the SCORECARD table with first-working round 58.

**Verdict: predicate met, score HELD at 7** — the standing unanswered L0 cap
(`kengaku | round-25/33/51`, still open in the committed l0-questions file — nothing
assumed answered), the r56-C3/r57-C2 shape; graded **unchanged** on the score with the
ground and class line credited under the expansion trend, honestly declared by the lane.

### The repair cascade — five of six breaks verified with committed evidence (requirement: ≥3)

| # | break (surface) | evidence re-checked by this judge | verdict |
|---|---|---|---|
| 1 | round36-c2 W4 row-counting (doubled README/PROVINCE rows from a non-idempotent edit script) | lesson mistake row (class landing, idempotence rule mined); the tip entry-truth re-run by this judge executes the round36-c2 row green (`executed=87 mismatched=0`) — the designed capture story is consistent; the intermediate receipt itself is uncommitted (defect (a) below) | evidence-verified |
| 2 | round51-routing disposition vocabulary (R56-F1 `routed-to-future-claim`, R56-F2 `captured-as-amendment` out of vocabulary) | both findings rows read: dispositions normalized to `fixed-verified` with dated correction history inside the rows; `plans/round51_routing.py --lane .` re-run by this judge at tip → `CHECKS present=79 absent=0`, `PREDICATE R51-C2 pass`, exit 0 | re-measured |
| 3 | two broken landed check fields (R56-F1's greped `of-output`, a file that never existed, AND greped for the removed live state; R56-F2's held prose) | R56-F1's `check` now the runnable `python3 plans/anchor_line_check.py --lane . \| grep -c 'ROW S201 state=repaired by=S213'`; R56-F2's `check` now the runnable `grep -q '"source": "corpus/lessons/round-56.md:60"' corpus/routed-findings.jsonl`; both with dated notes | verified from bytes |
| 4 | r40 `a_tok` fixture uniqueness (S214 duplicates S111's capture sha) | `plans/battery40/a_tok.py` diff read: edit scoped to the `\| S111 \|` row line via a new `_edit_row` that raises on 0 or >1 hits, dated in-file note (round-58 scoping 2026-11-01); S214 row carries the same sha as S111 as claimed | verified from bytes |
| 5 | round-close E11 used-by paths (held until the knowledge entry landed) | `corpus/knowledge/tb2-distribution-search-grader.md` exists with resolving used-by paths; the fleet census validate passes with only the 20 W04 warnings | verified |
| 6 | the registry advertisement of the repaired checker itself (`ADVERTISED 86 / REGISTERED 85`) | the repaired checker is now a first-class gate row (read at `SKILL.md` `anchor-line-check`, with verdict map + selftest + pins); `plans/round52_c2_registry.py --lane .` re-run by this judge at tip → `ADVERTISED total=86 / REGISTERED total=86`, `MISSING 0`, `PREDICATE R52-C2 pass`, exit 0 | re-measured |

The cascade's honesty marker holds at the tip: the full entry-truth counter re-derived by
this judge prints `laundered=0` — no declared-green row is false.

## 3. CLOSURE-PREP instruments at the pushed head — all three re-derived green

Registry `PREDICATE R52-C2 pass` (ADVERTISED 86 / REGISTERED 86, exit 0); landcheck
`LANDCHECK PASS n=4` (L-reg/L-chess/L-selftest/L-grader all `[PASS]`, exit 0); full
entry-truth at `46fe5398` itself:

```
ROWS registry=87 ledger=87 missing=0 extra=0 argv_defect=0 wrapper_defect=0 abbrev_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
BINDING l1=0 l2=0 l3=0
SOURCE rev=46fe53981572865698017b22abea3572e6ebeee2 clean=yes lane_rev_equal=yes
RUN executed=87 timeout=0 mismatched=0 evidence_missing=0 laundered=0
TIPSTATE entry_declared_green=56 entry_declared_red=31 observed_green=56 observed_red=31
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R55-C2 pass
FULL-EXIT=0
```

Byte-equivalent in every predicate field to the committed
`waveR/final-tip-receipts-r3.txt` (which was measured at `bf48fd2072`, the parent of the
receipt commit) — the round-57 closure property ("re-derive at lane head") reproduces at
the pushed head, with the declared TIPSTATE equal to observed.

## 4. Census (re-run) + trend and axis verdicts (this judge)

`bash <fleet>/scripts/sources-census.sh validate --root <fleet> kengaku` → **exit 0**,
verdict `ok`, exactly **20 W04** duplicate-url warnings — re-counted; the 5 new ones are
S213–S217 carrying their originals' URLs (the Q34 correction convention's cost, declared in
the lesson). S209–S212 rows shape-clean, all tier A on spec/docs/code kinds, mined with
resolving used-by paths.

- **expansion: improved — agreed.** The frontier moved 14 → 15 of 89 TB2 graders and the
  new grader is a CLASS the corpus lacked (a numeric tolerance band on two aggregated
  functionals — dual KL ≤ 1e-3; every previously executed grader decided exact
  predicates); the probe enters the capabilities table; SOURCES 201→210. The score stays 7
  by the lane's standing L0 design and the report says so rather than moving a capped
  number — the honest form.
- **quality: improved — agreed and re-measured.** The pushed tip re-runs its whole
  advertised surface green from this judge's own runs (registry `PREDICATE R52-C2 pass`,
  `LANDCHECK PASS n=4`, entry-truth `executed=87 … laundered=0` with TIPSTATE declared ==
  observed at the pushed head itself); the repair cascade's breaks were captured by the
  designed tip counters BEFORE closure (five of six verified above); the writers that
  landed data are byte-stable where required (LOG/PROVINCE/SOURCES/lesson: 0 removed
  lines; the two SKILL registry-cell refreshes and the two findings-row repairs are the
  round's declared, dated, correction-history-carrying rewrites).
- **discernment: improved — agreed.** 48/48 full-commitment predictions confirmed on the
  first capture run with zero U marks (re-run by this judge, cell-for-cell identical) —
  the honest contrast with r57's timing-U cases, recorded as a class finding rather than
  laundered; the falsifier fixtures pinned both directions BEFORE the fix (old-checker
  receipts committed); the branch-A re-pin decision was made from the discriminator's
  measurements; the kill-exit misprediction is dated-corrected in the freeze instead of
  papered over; the repair exposed real anchor defects and the round declared them
  (R58-F1/F2 born closed) instead of silently editing the cells.

Axis verdicts: operability **improved** (held at ceiling 10 with the gate's verdict now
correct; re-measured), freshness **improved** (9→10, re-measured both ends), coverage
**unchanged** (predicate met, score held 7 by standing L0 design; the ground counts under
the expansion trend), depth/adjacency/novelty/calibration **unchanged** (SCORECARD diff
base→tip is 47 insertions, 0 deletions — zero removed axis-history lines; the r56/r57
numbers stand: depth 9, adjacency 9, novelty 8, calibration 10). **No axis harmed.**

Re-measured by this judge: registry, landcheck, full entry-truth at the pushed head;
anchor selftest 6/6 + anchor scan + round46-c2 at BOTH ends; round50-c1 full runs at BOTH
ends; KL probe selftest + full re-run + sha-refusal kill (judge-owned tamper);
round51-routing at tip; census validate; all four live source re-fetches + hashes + quotes;
all counting commands at both ends; the population pin hashes; probe/freeze sha pins;
discriminator and stability tables re-counted from committed bytes; SCORECARD/LOG/
PROVINCE/SOURCES/findings/fixture diffs.
Evidence-verified from committed bytes: the falsifier receipts, the findings correction
history, the knowledge entry, the lesson Gate/Mistakes tables, the claims freeze document
and its dated corrections, the LOG round-58 entries, the L0 file, the commit-message
capture chain of the intermediate red states (R2/R3), assimilation cross-check
(`considerthese/` 8 files unchanged in range; `round_close.py` and `tip_receipts.py` exist
= the "already implemented" proposals).

## 5. Spot-check table (LEARNING.md discernment — ≥1 admit + ≥1 reject-equivalent)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S211 `solution/solve.sh` (maintainer oracle) | admit A (code) | pinned raw URL re-fetched live 2026-11-02, sha256 `19daaee1…8bbe` match, `:122` quote byte-true (19 words ≤ 25) | **agree** | the oracle is read from the maintainer's own solver and its accepted point was frozen as literals BEFORE the probe ran — this judge's 48/48 re-run (including `sol` P/P/P/P and `tolbnd` P/P/P/P, both derived from those constants) is independent confirmation that the frozen oracle point is real |
| S209 `task.toml` (task definition) | admit A (spec) | pinned raw URL re-fetched live, sha256 match, `:6` quote byte-true (17 words ≤ 25) | **agree** | the task's machine-readable self-definition declares the dual-KL construction objective — the exact property the probe's four legs decompose; tier A is correct for the spec of the graded surface |
| zero-U prediction table (48 full-commitment predictions) | reject-equivalent (declined the honest-undecidable class; full commitment) | the frozen table at `d6bc6027` vs this judge's re-run: 48/48 observed, zero U | **agree** | the grader is numeric-deterministic (tolerance bands on computed KL values, no timing, no host noise) — unlike r57's timing-equal cases, every leg is decidable from static semantics; committing to all 48 was the calibrated call, and the first-run confirmation vindicates it |
| r52-repair proposal refusal (assimilation, standing reject) | standing reject | `considerthese/` unchanged in range (8 files, diff empty); the r52-repair regression records stand | **agree** | the proposal would re-land the demonstrated regression the round's own counters exist to catch; nothing new was adoptable and the round says so |

No new rejection rows this round (all four opens admitted; the lesson says so) — the
zero-U full-commitment decision and the standing proposal refusal are sampled as the
round's reject-equivalents.

## 6. Findings, SHONEN, routed items

- **(a) Receipt-pointer defects (conformance, status-neutral — route to the lane for
  round 59).** Five receipt paths cited in landed prose do not resolve at the tip (checked
  with `git cat-file -e` against `46fe5398`): `.ufo/waves/round-58/wavep/r50-after.txt`
  (cited in the round58-c2 ledger flip reason — the load-bearing green state is instead
  covered by the committed final receipts AND re-derived by this judge),
  `.ufo/waves/round-58/wavec/kl-sha-kill.txt` (mistakes row + claims dated correction),
  `.ufo/waves/round-58/wavec-tip/entryargv-full.txt` and
  `.ufo/waves/round-58/waveR/final-tip-receipts.txt` (lesson mistakes rows; the `-r3`
  suffixed file IS committed), and `fix/r46c2-after.txt` (claims doc). Same class as the
  r57 closure's observation (lesson evidence citing scratch paths) — recurring. Fix next
  round: commit every cited receipt at landing, or re-point the citations at committed
  paths.
- **(b) Minor receipt bug (status-neutral).** `recon/esc-falsifier-fixed-checker.txt`
  prints `exit=0` under fx-red and fx-words where the checker exits 1 (its own ANCHORLINE
  lines show `live=1`, and the same file's selftest records `rc=1 want_rc=1 ok` for both
  classes). Payload correct; the exit labels are a capture bug (the r56 relay lesson's
  exact hazard). The red-direction exit evidence is carried by the selftest receipts and
  this judge's re-runs.
- **Cosmetic observations (status-neutral).** (1) The report's Assimilation-adjacent prose
  says the lesson mines "three rows"; the landed lesson has four (the SCORECARD-advertisement
  row was added at wave F2, after the report prose was drafted — honest progression, and
  the LOG close entry says "four admits" correctly for the Gate). (2) The report's trend
  section says the cascade "broke six tip-counter surfaces" while the LOG close entry says
  "four tip counters" — surfaces vs counter legs; consistent under its own counting unit,
  but one word choice would prevent the misread. (3) Timing: watchdog complete line
  precedes the report commit by one second (same class as r54/r57).
- **No other new routed defects.** All R56 routed items are discharged (R56-F1 closed
  fixed-verified with the repair landed; R56-F2 normalized + check repaired). Carried
  open, named by the lane and unchanged by this closure: L0 questions `kengaku |
  round-25/33/51` (coverage cap) and `kengaku | round-56` (L2 surface + ledger host
  column) — nothing assumed answered.
- **SHONEN:** all four boxes `[~]` with resolvable pointers, no `[x]` anywhere in
  `SHONEN.md` or the report. Spot-checks: SKILL.md carries the registry (86 advertised /
  86 registered incl. the round-58 KL probe and the first-class anchor-line-check row,
  both re-measured this closure) and decision tables; LOG round-58 entries present (freeze
  + measured close + wave entries); box 3 is evidenced by this closure itself — every
  measurement above ran from committed instructions alone, fresh session, judge-owned
  clones; PROVINCE round-58 section dated (15 of 89; refusal list unchanged). All four
  look fully checkable by a non-author — the operator may want to run that gate; this
  judge did not write `[x]`.

## 7. Judge-run receipts (summary)

Tip `46fe5398`, WSL Ubuntu-24.04, master checkout from a bundle taken of the lane repo
(uv/pytest absent): registry `PREDICATE R52-C2 pass` (exit 0); landcheck `LANDCHECK PASS
n=4` (exit 0); entryargv full `executed=87 timeout=0 mismatched=0 evidence_missing=0
laundered=0`, `BINDING l1=0 l2=0 l3=0`, TIPSTATE 56g/31r declared==observed, `PREDICATE
R55-C2 pass` (exit 0); anchor selftest 6/6 + scan `live=0` (exit 0); round46-c2 `PINS
total=3 mismatched=0`, `PREDICATE C2 pass` (exit 0); round50-c1 full `mismatched=0`,
`PREDICATE R50-C1 pass` (exit 0); KL probe `cases=12 legs=48 mismatches=0 setup=0
predicted_u=0`, `PREDICATE R58-C3 pass` (exit 0); kill re-fire `KILL-EXIT=1`; routing
`PREDICATE R51-C2 pass` (exit 0). Base `a6b209cf`: anchor scan `live=1` (exit 1);
round46-c2 `PREDICATE C2 fail` (exit 1); round50-c1 full `mismatched=125`, `PREDICATE
R50-C1 fail` (exit 1 per the frozen verdict map). Both judge scratch clone sets are
removed after this closure.
