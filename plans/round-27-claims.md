# Round 27 — pre-registration (frozen before wave 1, 2026-10-21)

Base: lane `master` = `b5719440e5eee46c1886fddbdf7bdc1624829454` (jj-colocated; `jj-lane.sh state` →
`ahead=0 behind=0 tracked=0` at readiness; receipts `corpus/evidence/round27-calibration/round-start.txt`).
Round 26 closed ADMITTED by the outside non-author closure CloseKengaku26
(`/home/vgpnk/Projects/shokunin/.ufo/reports/round-26/kengaku-closure-evidence.json`; four outside
admit/reject agreements, no routed defect). Its first limitation reads: "Frozen P2/P3 assertions do not cover
new round-26 assertions" — C2 below answers exactly that limitation. No `corpus/lessons/round-26-verifier-spotcheck.md`
and no `corpus/lessons/operator-*.md` exist at base (round-start receipt).
Author: KengakuR27 (L1; holds the frozen planner seat — the wave validator rejects `planner`).
Amendments are appended below as `## Amendment N`, never edited in place.

## Axis state at base (SCORECARD.md §Round 26)

novelty 7 · coverage 7 (capped) · calibration 8 · operability 8 · freshness 8 · adjacency 8 · depth 9.
Lowest non-retired: **novelty 7, tied with coverage 7**. No stagnation waiver (novelty < saturation line 8).
Tie-break as in rounds 25–26: coverage stays capped by the declared-but-unresolvable-surface clause until the
operator rules L0 `.ufo/l0-questions.md:72`; `novelty` keeps its recorded mapping → canonical
coverage/constructs. This round makes no separate coverage claim.

## C1 — novelty (→ coverage/constructs; lowest): frozen extraction-policy comparison on the pinned responses

Construct (named open by `corpus/README.md:260`, "a separately designed parser-policy comparison remain[s]
open"): **how much the lane's stored verdicts and reported pass rates depend on which answer-extraction policy
reads the response**, holding the graders and truths fixed. Round 26 perturbed *responses* under one
extractor; this round holds responses fixed and varies the *extractor* across policies that public evaluation
harnesses actually implement (first vs last match, fence-aware vs fence-agnostic, strict whole-output vs lenient).

Population: exactly the round-26 frozen population — the four sha256-pinned result files, **1964** raw+ok
records, 0 excluded — loaded through `plans/grader_perturb.py:build_population` (pins unchanged). Graders
unchanged: `grade_state`, `grade_seq`, `grade_c`, `valid_latin` per record exactly as `grader_perturb.regrade`.

Frozen policies (each a total function `raw -> parsed value | None`; the record's grader then decides PASS):

| id | policy | exact semantics |
|---|---|---|
| E0 | lane (reference) | `grader.extract_json_block`: last block of ```` ```(?:json)?\s*\n(.*?)``` ```` (re.S) if it parses, else last parseable `BARE_RE` candidate |
| E1 | first-fence | E0 with the **first** fenced block instead of the last (then the same bare-last fallback) |
| E2 | bare-last | ignore fences; last parseable `BARE_RE` candidate (fence-agnostic last match) |
| E3 | bare-first | ignore fences; first parseable `BARE_RE` candidate (fence-agnostic first match) |
| E4 | strict-whole | `json.loads(raw.strip())`, else None (whole output must be JSON) |
| E5 | fence-only | last fenced block (E0's regex) if it parses, else None (no bare fallback) |
| E6 | any-label-fence | E0 with the fence regex ```` ```[A-Za-z0-9_+-]*[ \t]*\r?\n(.*?)``` ```` (any language label) |
| E7 | decode-first | scan left→right; at each `{`/`[` try `json.JSONDecoder().raw_decode`; first success (unbounded nesting) |
| E8 | decode-last | the same scan; collect top-level decoded spans (skip starts inside an already-decoded span); last one |

`BARE_RE` is the byte-identical pattern in `grader.py:128` / `plans/grader_perturb.py:36`. No policy may read
`want`, `ok`, or the grader outcome. A policy that raises is a defect (exit 1), not a FAIL.

Metrics per policy Ei (i=1..8), over all 1964 records: `agree` = records whose Ei verdict equals the stored
verdict; `flip_pf` (stored PASS → FAIL), `flip_fp` (stored FAIL → PASS); `none` = extraction returned None;
overall PASS rate and its difference from E0 in percentage points; exact two-sided CP95 on agree/n (reuse
`clopper_pearson` from `plans/attrib_calibration.py`; nominal descriptive finite-population interval per
`knowledge/grader-perturbation-audit.md` — **not** a future-response guarantee); per-format-stratum
(`format_class`: FJ1/FJM/MULTI/DANGLE/BARE) and per-file/per-cell PASS rates and the largest absolute per-cell
PASS-rate shift vs E0; the full 9×9 pairwise verdict-disagreement matrix. E0 must reproduce the stored verdict on
all 1964 (sanity; otherwise exit 1).

Instrument: `plans/parser_policy_compare.py` (stdlib only, offline). CLI
`python3 plans/parser_policy_compare.py [--root DIR] [--summary|--json] [--selftest]`; exit 0 = ran, pins and E0
baseline reproduce; 1 = pin/baseline inconsistency, policy exception, or selftest failure; 2 = usage. `--summary`
ends with one line `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=<sum flips> policies_with_flips=<n>`.
Independent oracle `plans/fixtures/r27/policy_oracle.py`, written from this text only (never importing grader.py
extract code or the instrument), must reproduce every per-policy agree/flip_pf/flip_fp/none count. `--selftest`
must kill at least one seeded mutant per policy (e.g. E1↔E0 swap, E2 fence leak, E4 strip omitted, E7 nesting
limit, E8 contained-span reuse).

Counting command (C1). Before: `git cat-file -e b5719440:plans/parser_policy_compare.py` → exit 128 (absent);
0 alternative extraction policies compared on the stored responses (`corpus/README.md:260` names it open).
After: `python3 plans/parser_policy_compare.py --summary` → `compared_verdicts` 0 → 15712 (1964 × 8) and the
per-policy disagreement counts; observable = policy-attributed verdict disagreements made visible.

Prior art (searched over papers **and** tooling, round-25 M38 / round-26 S045 precedent, before any +1):
xFinder (S044) already compares RegEx extraction against a learned extractor; harness filters
(lm-evaluation-harness `regex` filter `group_select`, inspect_ai `match`/`pattern`, OpenAI simple-evals answer
regexes) implement first/last-match policies. Expected verdict: the construct is published in kind →
**novelty held at 7**, observable recorded; a +1 requires a prior-art search that finds no published
cross-policy *verdict-agreement* measurement and the critic's agreement. No method credit is taken here.

Sourced: the C1 knowledge entry `corpus/knowledge/extraction-policy-comparison.md` (drafted under
`.ufo/waves/round-27/drafts/` until Q13/Q14 hold) cites SOURCES rows opened **this round** for each harness
policy it names (each new row: URL, access date, ≤25-word located quote in
`corpus/evidence/round27-sources/gate.md`).

### Predictions (filed before any instrument output; scored at close by Brier)

Code-derivable forecasts reasoned from `grader.py:121-134` and the round-26 format strata (MULTI 31 records
known from `knowledge/grader-perturbation-audit.md`); recorded for calibration hygiene, no calibration credit
taken from their score.

| id | event (over the 1964 records) | p |
|---|---|---|
| Q1 | E1 first-fence has ≥1 disagreement with the stored verdict | 0.85 |
| Q2 | E4 strict-whole agrees with the stored verdict on < 50% of records | 0.70 |
| Q3 | E2 bare-last disagrees on ≤ 1% of records (≤ 19) | 0.60 |
| Q4 | E7 decode-first has strictly more disagreements than E3 bare-first | 0.40 |
| Q5 | at least one cell's PASS rate shifts by ≥ 10 points under some policy in {E1,E2,E3,E6,E7,E8} | 0.50 |
| Q6 | E6 any-label-fence has 0 disagreements | 0.70 |
| Q7 | max − min overall PASS rate across {E0,E1,E2,E3,E5,E6,E7,E8} ≥ 2 points | 0.45 |
| Q8 | E5 fence-only has ≥ 1 flip_pf (a stored PASS that relied on the bare fallback) | 0.55 |

## C2 — calibration: frozen P4 content pins over the round-26 landed self-assertions

The round-26 closure's first limitation: P2/P3 do not cover round-26's own new assertions. Frozen population P4,
enumerated at base `b5719440` (ids fixed in the instrument; anything added after base is out of population):

- **P4a** `SCORECARD.md` §Round 26 (lines 752–810 at base): every numeric token in the C1/C2 claim rows,
  the capability row, §final measured outcomes and §measured revision, compared with the committed receipt or
  command it names (`corpus/evidence/round26-calibration/*.txt`, `grader_perturb.py --summary`,
  `state_check.py --summary`, `round26_census.sh`).
- **P4b** `corpus/README.md` §Round-26 supporting artifacts table (base lines 264–275): every path row exists,
  every round-26 artifact path on disk under those dirs is listed (both directions), and its "Covers" count
  tokens re-derive.
- **P4c** `corpus/lessons/round-26.md` wave-record counts (build 72 seats and its role mix; falsify 64, role
  mix, 11 dead; 136 / 139 totals; 0/82/87 and 0/83/88 report units) against `.ufo/waves/round-26/`
  specs/assignments/dead-seats files and `git ls-tree` at the named revisions.
- **P4d** `corpus/knowledge/grader-perturbation-audit.md` population numerics (1964; 188/128/320/1328;
  1021/943; 1708/240/12/4; family n/k table) against `grader_perturb.py --json` and the oracle.
- **P4e** `corpus/SOURCES.md` S043–S048 `used-by` cells against files that actually cite each id.

Instrument: `plans/state_check.py` v4 — same CLI and exit map; P2/P3 keyed results byte-identical to v3 on the
base tree (no silent re-scoping); adds ids `P4a.*`–`P4e.*`. Supersession: a stale P4 assertion closes only via
an appended `R27-E*` correction carrying the full re-derived tokens (SUPERSEDE regex already `R2[5-9]-E`).
`--selftest` must show each P4 class red on a mutated fixture.

Counting command (C2): `python3 plans/state_check.py --summary`. Before = v4 on the base tree
(`git archive b5719440 | tar -x -C /tmp/kengaku-r27-base`): P4 assertions registered and their mismatch count
(v3 on base registers **0** P4 assertions — every round-26 row is OUT_OF_POPULATION or unregistered). After = v4
on the landed tree: `mismatch=0`, each R27-E counted `SUPERSEDED`. Prediction: base P4 mismatch ≥ 1
(p = 0.55). Score: held at 8 unless a scored-probe leg is met (it is not); the observable is the claim.

## Separability (QUALITY R13)

C1 counts only the four pinned result files through a new instrument; it changes no P4 location. C2's P4 is
enumerated at base and touches SCORECARD/README/lesson/SOURCES **correction rows** and `plans/state_check.py`;
C1's new files (instrument, fixtures, knowledge entry, new README/SOURCES rows) are out of P4 by construction.
Revert test at close: each claim's counter re-run with the other claim's paths reverted must not move
(`corpus/evidence/round27-calibration/revert-test.txt`).

## Frontier step

SOURCES rows only after opening (URL, access date, ≤25-word located quote in
`corpus/evidence/round27-sources/gate.md`); census before/after via
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
(round start: `kengaku ok`, exit 0, two W04 warnings). One mistake mined into `corpus/lessons/round-27.md`
`## Mistakes` with a fix shown able to fail. Knowledge admission under Q1–Q14 (Q13/Q14: the admitting commit
contains the cited returned falsify re-read reports).

## Waves

Wave 1 build (64–100 seats) and wave 2 falsify (64–100 seats, after wave 1 returns and the instruments are
integrated); round total ≤ 200. Writers work only in private clones `/tmp/kengaku-r27-<Seat>`; KengakuR27 is the
sole integrator.

## Amendment 1 — after build outputs, before knowledge admission (2026-10-21)

Timing disclosure: returned build seats and an L1 sanity computation have already revealed E-policy counts.
This is a post-output clarification, not an ex-ante change or a rescore of the predictions.

- E1 selects the first **matched**, not first parseable, fence; failed decode goes directly to the
  whole-response bare-last fallback. Successful JSON null ends extraction (no fallback).
- E2/E3 apply non-overlapping `re.findall(BARE_RE, raw)` to the original raw string as-is, including
  candidates inside fences. They neither strip delimiters nor exclude fenced spans.
- E5 tries only the last matched fence and has no fallback. E6 is the exact frozen regex, not a
  CommonMark implementation. E7/E8 start only at braces/brackets; E8 skips nested starts in successfully
  decoded spans. Policy equivalence on this corpus is not equivalence on arbitrary inputs.
- E4 retains `raw.strip()` as frozen. openai/evals JsonMatch uses `json.loads(raw)` without that strip:
  the source grounds the whole-output policy class, not source-exact implementation. Source probes find
  zero population differences. None of these lane-defined JSON variants is described as an actual
  end-to-end run of lm-eval, inspect_ai or simple-evals.
- C1's published-in-kind verdict is **held 7** (xFinder and fixed-output rescoring precedents); no +1.
  Q5 uses unrounded rates/counts, not a rounded `CELLSHIFT` token. Brier is descriptive bookkeeping only.
- P4a compares historical round-26 numerical assertions with their committed round-26 receipts, not
  live `round26_census.sh` totals or recursive live v4 output. A current source registry census would
  conflate C1 additions with a claim about the historical admitting tree (RevSeparabilityPlan).
- P4b treats a listed directory as recursively covering its base descendants; its reverse universe
  is the frozen base table's three directory trees, not new round-27 paths. The S043–S047 range retains
  the existing explicit S043–S048 erratum; do not manufacture an unresolved mismatch.
- P4e follows the registry's knowledge/lessons teaching-use convention, not every literal identifier
  in plans, receipts or source inventory. S043's supersession-only reference is not substantive use.
  Newly written round-27 citations cannot expand the frozen citing-file population.
- SOURCES contract has **11 content columns**, or **13 split fields including empty pipe edges**.
  Build-context “13-column” wording was erroneous; existing contract-v1 shape wins.
- Frozen P4 inventory must expose unmapped numeric assertions as offline-unverifiable, never silently
  discard them. Score/version/source/commit identifiers are distinguished from measured numeric claims.
  The inventory and its interpretation are delivered evidence, not a claim to check every current number.
- Untrusted-input cost probe found E7/E8 superlinear on repeated unmatched brackets (200K takes ~285s).
  CLI accepts only the byte-pinned population and rejects changed files before invoking these policies;
  pure policy helpers are research functions for bounded fixtures, not a production untrusted-input API.
  No arbitrary-input performance or parser-safety claim follows.

## Amendment 2 — mutation-driven completion after falsify outputs (2026-10-21)

Explicit post-output change: neither predictions nor the base population are retrospectively relabeled
as newly sampled. E0–E8 semantics,1964 population,8 alternatives and15712 comparisons remain unchanged.

- E6's first-versus-last mutant survived58 cases; the two-distinct-any-label-fences witness enters the
  permanent hand table (now59), and an additional mutant/control makes10 killed seeds. No output count moves.
- P4's named base-target classes remain fixed at b5719440;51 IDs replace the incomplete49-ID build
  implementation by adding two required disclosure groups (score tokens and adjacent audit numerics).
  The full existing48 comparable/grouped checks remain, one already-superseded source-range claim stays
  superseded, and two groups explicitly report offline-unverifiable rather than unsupported MATCH.
  Final class sizes P4a10/P4b8/P4c11/P4d15/P4e6 plus inventory1.
- P4a's four-numeric/one-index repair split is derived from the named base receipt; P4c derives recovery
  reviewer count from the committed recovery-start receipt and verifies assignment-ID uniqueness/disjointness.
  P4d independently reads the pinned JSONL breakdowns alongside manifest/live command/oracle authority.
  Correct full R27 family corrections work even when the original claim's denominator is false.
- Permanent selftests now attack deleted production comparisons/dispatch, denominators, actual summary
  disclosure rendering, exact prior erratum and R27 acceptance. Existing P2/P3 keyed records remain unchanged.
- Q16 extends the mined timing fix to two reports, complete tree traversal and isolated temporary Git writes.
  Its early0/later2 fixture supersedes the one-report example, preserving both generations' evidence.
- S058/S059 correct the source-reason exception and RFC§6 anchor before admission; S060 retains the opened
  json-repair rejection without adding an unfrozen policy. Final new-source set S049–S060 is12 rows,11A/1B.
- C2 is0→51 registered frozen assertions/disclosures, not a fabricated new-mismatch reduction: delivered
  checker sees0 mismatches at base and candidate; the p=.55 base-mismatch forecast is false. Scores stay7/8.
