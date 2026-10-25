# R31FxQualityBar — did this round's failures become QUALITY.md criteria or named debt?

Seat: `L1Kengaku31.R31FxQualityBar` (leaf, read-only). Round 31 wave 2 (falsify). Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Landed commit `dbb07364`, baseline `0883e72`.
Scope: QUALITY.md (landed + delta), wave-1 build reports (all 36 under `.ufo/waves/round-31/build/`),
the landed entry/registry/gate, LOG.md/SCORECARD.md deltas, and the in-flight lesson draft
(`corpus/lessons/round-31.md`, untracked). Nothing under the lane was written except this report;
scratch `/tmp/r31fx-qualitybar/` (extracted landed tree, < 1 MB).

## 0. The three questions, answered directly

1. **Any criterion added this round?** No. `git diff --exit-code 0883e72..dbb07364 -- corpus/QUALITY.md` → unchanged (QUALITY.md is byte-identical between baseline and landing). **Criterion-added-this-round-unsupported-by-a-lesson: none exists** (vacuously satisfied at `dbb07364`). Caveat: the *in-flight* lesson draft asserts "grounded as `QUALITY.md` **Q21**" (`corpus/lessons/round-31.md` §Assimilation, "considerthese"); Q21 does not exist in QUALITY.md in the landed tree or the worktree. When Q21 lands it must cite that lesson — its support is a measured absence (5/40 entries name a pinned revision), so it is not an unsupported criterion yet, only a pending one.
2. **Which of the round's mistakes have a criterion behind them?** The entry-level failures do (Q1–Q8/Q10: staged `verified-at: 2026-10-23`, 28-word quote, missing falsifier, missing source-label paragraph, unnamed "round-1 checklist" premise, unmatched "partly observable" premise, overlong/escaped/wrong quote spans, prose recheck, dangling used-by). Every one was caught pre-admit and fixed at landing. **The instrument failures do not**: no QUALITY.md criterion governs counting-instrument adequacy (adoption counter content-blindness, defect-counter self-greening, selftest-only detectors). Q20 governs gate-landing *runs*, not counter substance.
3. **Which mistakes have neither a criterion nor a debt name at the landed commit?** Three reviewer-flagged closure gaps (item 7 unchecked, kill-rule 2/3 branch unreachable, calibration count 8+2 split), one unresolved registry contradiction carried from round 30 (`round-30.md:66`), and two count drifts in the landed SCORECARD itself (round shape 68 vs 72; index 40→40 vs measured 39→40). See §3.

## 1. Evidence re-run (commands, paths, outputs)

- `git diff --exit-code 0883e72..dbb07364 -- corpus/QUALITY.md` → no output (unchanged).
- `git ls-tree --name-only dbb07364 corpus/lessons/ | grep -c '^round-31'` → **0** — no round-31 lesson in the landed tree. The draft exists only untracked in the worktree.
- `git show dbb07364:SCORECARD.md | grep -n 'round-31.md'` → lines **1056** and **1075** (plus the truncated C2 row line ~1050) cite `corpus/lessons/round-31.md` §Mistakes — a path absent from the commit that contains them.
- `git show 0883e72:corpus/README.md | grep -cE '^\| `knowledge/.*\.md` '` → 39; `git show dbb07364:corpus/README.md | grep -cE …` → 40. Landed SCORECARD C1 row states "index 40 → 40" (`SCORECARD.md` round-31 section) — should be 39 → 40.
- `awk '/^## Round 31/,0' SCORECARD.md` → "36 build + 32 falsify seats (68 total)". `python3 -c "import json;d=json.load(open('.ufo/waves/round-31/falsify/swarm-registry.json'));print(len(d))"` → **36** (falsify registry); the in-flight lesson says 36+36=72. Landed shape count is stale.
- Extracted `dbb07364` to `/tmp/r31fx-qualitybar/`: `python3 plans/sources_adopt.py --selftest | tail -2` → `SELFTEST cases=17 failed=0`, exit 0 — C3 selftest survives on the landed bytes. (C1/C2 counters on the extraction are environment-limited: census lacks `shokunin.conf`, C2 needs the `.git` baseline — matches the known Q20/round-29 M93 caveats; the committed receipts `corpus/evidence/round31/adoption-after.txt` (`entries=1 … census=ok`) and `c1-verify-after.txt` (`checks=6 defects=0`) stand.)
- `git grep -n -i 'item 7\|kill rule\|2/3\|copyedit' dbb07364 -- LOG.md SCORECARD.md plans/round-31-claims.md corpus/lessons/round-30.md` → only the frozen claims text, no disclosure of item 7 or the 2/3 branch.

## 2. Mistake → criterion/debt map (the round's own failures, from the 36 build reports)

| # | mistake (seat that proved it) | criterion behind it? | named as debt at `dbb07364`? |
|---|---|---|---|
| 1 | Staged entry failed the bar as staged (Q1 date, Q3 28-word quote, Q4 no falsifier, Q5 no label paragraph, Q6/Q7 wrong/missing premise) — `R31EntryScope`, `R31DraftGate` | **yes** Q1–Q8; fixed by re-grounding before admit | n/a (fixed; recorded in lesson Gate) |
| 2 | Staged rows non-conformant (S093 escaped pipe, prose `recheck`, stale `opened`, dangling `used-by`, S092 28-word span, S100 corner-quote invisible) — `R31ReconPackage`, `R31DraftRows` | **yes** Q1/Q3/Q7 + census E01/E09/E11; normalized at landing | n/a (normalized; named in lesson "Staged-row normalization") |
| 3 | C1 counter content-blind: 63-byte stub prints the frozen pass line — `R31CritC1` V1/V2b/V3/V4b, `R31RevClaims` | **no** (no counter-adequacy criterion) | fixed operationally by landed second receipt `plans/round31_c1_verify.py` (receipt `c1-verify-after.txt`); named in SCORECARD capability row + draft lesson "vacuous" |
| 4 | C2 counter greened its own repair (R6 substring trap, R6 `.pdf` locator, R7 two-string guard, R2 wrap, C3 `elif` unreachable) — `R31DefR6/7`, `R31CritC2`, `R31SimplGate`, `R31GateFixture` | **no** | **yes** — SCORECARD "Calibration corrections carried this round rather than smoothed" lists all five (lines ~1066–1075); also lesson Mistakes "survivor"/"landing" |
| 5 | C2 counter mutation survivors m3/m4/m5 (R9 reduced to "HEAD has the path", R6 substring, vacuous `FROZEN`) — `R31MutCounter` | **no** | only in the *unlanded* lesson draft ("disclosed debt"); **not named in the landed tree** |
| 6 | C1 kill-rule 2/3-admissible branch unreachable (`plans/round-31-claims.md:40-42` vs the predicate's `cited_rows=3`) — `R31RevClaims` §b1 | **no** | **not named anywhere landed** |
| 7 | C2 §5 item 7 (report ordering) has no check and is not reported open — `R31RevClaims` §b5 | **no** | **not named anywhere landed**; the closure still says "ten … mismatches closed" |
| 8 | C2 calibration composition: 8 mismatches + 2 copyedit (R4/R5), not 10 — `R31RevClaims` §e1 | **no** | **not stated** in the landed SCORECARD C2 row (says "ten self-assessment/repo mismatches closed") |
| 9 | `corpus/lessons/round-30.md:66` "S081/S082 preprints vs S083/S086 peer-reviewed" contradicts registry S086's own scope cell ("the society publishes these proceedings without peer review", `corpus/SOURCES.md:110`) — `R31DefR2R3` §Finding | **no** (Q3/Q4 govern entries, not lesson prose) | **not recorded anywhere landed** |
| 10 | Five round-30 seat reports uncommitted through round-30 closure (R9) — `R31Revenger`, `R31DefR9` | **no** | committed as authored in `dbb07364` (R9 green on the landed tree per fixture); structural fix routed operator-side; named in lesson "landing" |
| 11 | Round-30 stale falsify receipt (A 79/B 7 vs A 78/B 8) — `R31ReconCensus` | **no** | recorded+routed in lesson "number-drift" (not fixed — rewriting another seat's verdict is out of scope) |
| 12 | `/tmp` full at round start — `R31DefR9`/lesson "provider" | **no** | named in lesson "provider"; cleanup done |
| 13 | SCORECARD round shape "36 build + 32 falsify (68)" vs actual 36+36=72 | **no** | **stale in the landing**; corrected in the lesson draft/registry |

## 3. Findings by severity

- **H1 — landed SCORECARD cites a lesson file absent from the landed tree.** `SCORECARD.md:1056,1075` (and the C2 row) point to `corpus/lessons/round-31.md` §Mistakes; `git ls-tree dbb07364 corpus/lessons/` has no such file. The commit is self-inconsistent: its own closure record rests on a path it does not contain. The untracked worktree draft will cure it when landed, but as of `dbb07364` it is a dangling reference (the same class Q13's inventory rule polices for Gate cells, applied here to SCORECARD).
- **H2 — three reviewer-flagged closure gaps have neither a criterion nor a debt name at landing:** (a) §5 item 7 unchecked and unnamed; (b) C1 kill-rule 2/3 branch unreachable and undisclosed; (c) the 8+2 calibration/copyedit split not stated. All three were explicit must-change items in `R31RevClaims.md`; none appears in the landed LOG/SCORECARD/lesson. Item 7 is the strongest: the C2 claim "ten routed defects R1–R10 closed" is asserted while §5 item 7 never had a check and is not reported open.
- **H3 — mutation-survivor debt (m3/m4/m5) is named only in the unlanded lesson.** The landed tree contains no record that `checks=10 defects=0` is not by itself evidence R6/R9 still test what they claim (`R31MutCounter` verdict).
- **M1 — unresolved round-30 lesson contradiction carried into the landing** (`round-30.md:66` vs `SOURCES.md:110`), flagged by `R31DefR2R3` as "outside the frozen ten … report it"; never reported in the landed record.
- **M2 — two count drifts inside the landed SCORECARD:** round shape 68 vs 72 (falsify registry already holds 36 rows), and "index 40 → 40" vs measured 39 → 40.
- **L1 — the proposal for a new criterion (Q21) is pending, not landed;** the lesson's claim that it is "grounded as QUALITY.md Q21" is currently false for both trees. Not a defect yet (no criterion added without a lesson), but the lesson must land Q21 with its citation or drop the sentence.

## 4. What survived

- **C3 gate survived:** on the extracted landed tree, `--selftest` → `SELFTEST cases=17 failed=0` exit 0; committed receipts show the exit ladder 0/8/9/2 and the neutered-binding failure case (`gate-cli-exits.txt`, `gate-binding-neutered.txt`). The first-artifact-binding residual (F2 of `R31CritC3`/`R31GateAdv`) is disclosed in the row/lesson and is a scope limit, not a silent gap.
- **Entry quality survived:** the landed entry's every quote is located at pinned revisions (S092 two-span split, S100 README line 46, S093 test.sh spans), the "unconditional upload" overclaim was qualified (`skip_tests_upload`/`bundled_tests`), the sample-vs-exhaustive boundary is stated, and the 731-manifest sweep is attributed to its seat (`R31DraftEntry`) rather than claimed as the entry's own — the Q2-bound fix is real.
- **Disclosure of counter fixes survived:** the five "corrected four times" items are named in the landed SCORECARD (even though their §Mistakes destination is absent).

## VERDICT

VERDICT: the round's entry-level failures are all behind existing criteria and were fixed before admit; its **instrument failures have no criterion behind any of them** (no QUALITY rule governs counter adequacy), and at the landed commit `dbb07364` **three closure gaps (item 7 unchecked, kill-rule 2/3 branch unreachable, 8+2 calibration split), the round-30 lesson contradiction, and the mutation-survivor debt are neither codified nor named**, while the landed SCORECARD cites an absent `corpus/lessons/round-31.md` and carries stale shape/index counts (68 vs 72; 40→40 vs 39→40). Survived: the C3 gate on landed bytes, the entry's re-grounding/quoting, and the counter-fix disclosures; no criterion was added this round, so the unsupported-criterion defect is absent (pending Q21 must cite the round-31 lesson when it lands).
