# ScoutQualityChecklist — round 27 admission and closure map (read-only scout)

Scope: Q1–Q14 for `corpus/knowledge/extraction-policy-comparison.md`; R1–R14 with R15 superseding R11. Lane tree, git and fleet untouched (read-only `git log`, `grep`, `cmp`, `curl` into `/tmp/kengaku-r27-ScoutQualityChecklist/`). Public reads 2026-10-21, UTC 11:44–11:50. Absent at base (`test -e`): the entry, `corpus/lessons/round-27.md`, `corpus/evidence/round27-sources/gate.md`, `plans/parser_policy_compare.py`, `plans/fixtures/r27/`, `plans/round27_census.sh`, `.ufo/waves/round-27/falsify/`, `.ufo/reports/round-27/` (lane). `^## Round 27` count in LOG.md and SCORECARD.md: 0 and 0.

## Q1–Q14 admission checklist
| Q | artifact that satisfies it |
|---|---|
| Q1 | entry lines 1–3: `source:` (S049+ ids, URL, anchor with commit pin) / `verified-at: 2026-10-21` / `recheck: 90d — <re-run + re-open>`; line 4 `writer: <seat>` (gate_timing_check.py:53 reads it); precedent `corpus/knowledge/grader-perturbation-audit.md:1-4` |
| Q2 | each load-bearing claim → SOURCES A/B row for its scope: lm-eval `extraction.py` and `gsm8k.yaml` (A), inspect `_match.py`/`_pattern.py` (A), simple-evals `common.py`/`mmlu_eval.py` (A, self-report), S044 (A), S045 (B, support only); Python `re` first-match needs a new docs row (S046 scopes `\s` only); `used-by` lists the entry |
| Q3 | `corpus/evidence/round27-sources/gate.md` in the round-26 layout (row / URL / location / quote ≤25 words / receipt+sha256); every load-bearing sentence maps to a row |
| Q4 | `## What this does not establish`: no bar, no future-response guarantee, E1–E8 operationalize documented rules (no harness executed), `re.search` first-match inferred from call shape unless quoted; falsifier: E0 fails stored-verdict replay (exit 1), or a pinned rule selects a different unit than its E-row |
| Q5 | labels in rows and text: simple-evals = OpenAI self-description of its own harness; lm-eval/inspect = maintainer code, not independent evaluation; xFinder = its authors' result; S045 = community tool; 1964 records = committed historical runs, not a live model |
| Q6 | names `knowledge/grader-perturbation-audit.md` (extends) and the grader bullet of `corpus/README.md` §Coverage map (:230); README:260 gets a dated amendment, not an in-place edit |
| Q7 | one commit: entry + README §What's here row (table :27) + coverage-map bullet + new SOURCES rows; `git show --stat <admit>` lists all four; `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` exit 0 |
| Q8 | `reject` Gate rows with `flip:` text: novelty +1 (flip: published cross-policy verdict-agreement measurement); OpenCompass `text_postprocessors` (MCQ letter extraction, not JSON; RowOpenCompassLast); pooled CP95 guarantee (r26 reject re-listed); any grader-defect claim (r26 D1 precedent) |
| Q9 | reason cites the property it asserts: S044 abstract reports extraction accuracy (RegEx 74.38% vs xFinder 93.42%), so a "verdict agreement already measured" reject cannot cite S044 |
| Q10 | `.ufo/waves/round-27/falsify/<Seat>.md` per reader: re-opens each quote at the pinned commit (sha256 + line), re-derives counts against `plans/fixtures/r27/policy_oracle.py`, names the entry path, ends `VERDICT:`; writer ≠ seat; connector seats never qualify |
| Q11 | C1 states "no bar-PASS claimed"; any bar wording needs the exact CP95 lower bound from `clopper_pearson` (`plans/attrib_calibration.py:144`) |
| Q12 | `python3 plans/attrib_calibration.py --selftest` exit 0 (A3 anchors :907); `plans/fixtures/r25/power_table.tsv`: zero errors n=17 → CP95 lower 0.804936 (PASS-capable), n=16 → 0.794093 (INDETERMINATE); 0-trial cells UNTESTED |
| Q13 | `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-27.md --commit <admit>` exit 0: reason cites full `.ufo/waves/round-27/falsify/*.md` paths (build/ does not count), each registered with role in {reviewer,scout,critic,sentinel,revenger}; no GENERIC_RE phrase (:39–48); candidate path contains no `_` (plain_cell strips it) |
| Q14 | `python3 plans/gate_timing_check.py --selftest` exit 0 (`ALL PASS`); round-27 late-report/same-commit pair with byte-identical lesson files (`cmp` exit 0) and expected `FAIL,FAIL,PASS,FAIL` (cf. r26 `recreate.sh:92`) |

## Verified facts behind the artifacts
- lm-eval `lm_eval/filters/extraction.py` (sha256 eb976bb3…): `group_select: int = 0` :27 and `match = match[self.group_select]` :49 (index 0 first; -1 last by Python indexing); last commit 29270297 (2026-08-26).
- lm-eval `lm_eval/tasks/gsm8k/gsm8k.yaml` (sha256 82eb1780…): strict `#### …` regex :36 (first) vs `group_select: -1` :41 (last); last commit b7335985 (2026-01-27). The harness names first and last as separate filters.
- inspect `_match.py` (sha256 46519227…): `location` default `"end"` :10; :18–20 `"exact"` = output exactly equal to target, so end/exact, not first/last. `_pattern.py` (sha256 7974ddb4…): `re.search` :77–78 (first). Last commits 2a15ec5c (2026-05-28), c9f5dd05 (2026-09-23).
- simple-evals `common.py` (sha256 84616c52…) :26–27 regex constants; `mmlu_eval.py` (sha256 e9165b54…) :110 `re.search` in a loop; gpqa/math/drop sites per RowSimpleEvals.md:10–15 (sibling, not re-verified); last commit 5e623c2b (2025-05-12).
- Python re docs (https://docs.python.org/3/library/re.html, opened 2026-10-21, sha256 453e9e17…) line 1073: "Scan through string looking for the first location where the regular expression" — S046 scopes `\s` only.
- Novelty: the harness code publishes the policy axis (gsm8k strict-first vs flexible-last). No source opened here measures verdict agreement across those policies; that absence needs a logged search before any +1 (not re-run here).

## Round-closure rows (R1–R14; R15 supersedes R11)
| R | applies? | check command / artifact |
|---|---|---|
| R1 | yes (C2 corrections) | `grep -c '<old>' SCORECARD.md` → 1, old line unchanged; new line in the state_check.py:260–262 form `- **R27-E<n> (date)** supersedes …` |
| R2 | yes, open | `grep -c '^## Round 27' LOG.md SCORECARD.md` → `1 1`; `test -f .ufo/reports/round-27/kengaku.md` run from the FLEET root (r26 report exists only there); this report is untracked: name it in the manifest |
| R3 | yes | same counts; the section names the `corpus/evidence/round27-calibration/` receipt and a verdict token, also on FAIL |
| R4 | superseded by R14 | field-2 awk cannot see `## Surfaces`; use R14 |
| R5 | yes | `grep -n 'separately designed parser-policy comparison' corpus/README.md` hits :260 → dated amendment naming the entry; `grep -nE 'Partly discharged round 27\|superseded'` hits |
| R6 | yes (one admit + one reject) | non-author line names an id outside the dispatch roster; `grep -rn '<id>' /home/vgpnk/Projects/shokunin/.ufo/prompts/` empty |
| R7 | N/A (offline round) | `grep -rl request_ts corpus/evidence/round27-*` empty; no `FROZEN:` line exists in r26/r27 receipts |
| R8 | yes | `awk '/^## Round 27/,0' LOG.md \| grep -nE 'lowest axis\|tie-break\|waiver'` hits (novelty 7 tied with coverage 7; no stagnation waiver) |
| R9 | N/A (no coverage claim) | `awk '/^## Round 27/,0' LOG.md \| grep -niE 'coverage (leg\|claim)'` empty; any hit activates R9 |
| R10 | yes | `grep -lE '^## Gate$' corpus/lessons/*.md \| wc -l` = 4 at base, 5 after; unanchored `grep -l '## Gate'` = 5 at base (extra: `round-8-aggregator-box3-coldrun.md:33` "## Gated steps"); name the gap |
| R11 | superseded by R15 | see R15 |
| R12 | yes | `python3 plans/state_check.py --summary` exit 0 with `mismatch=0`; `superseded=` counted separately |
| R13 | yes | `corpus/evidence/round27-calibration/revert-test.txt` in the r26 layout (`C1 comparison=UNCHANGED`, `C2 comparison=UNCHANGED`, `RESULT=UNCHANGED`, exit 0); `grep -c 'RESULT=UNCHANGED'` → 1 |
| R14 | yes | `python3 plans/state_check.py --summary` exit 0; PROVINCE.md:12–17 rows with absent local paths keep `**ABSENT <date>**`; endpoint-first rows reported offline |
| R15 | yes | fleet root: `sh kengaku-shokunin/plans/l0_filed_check.sh .ufo/reports/round-27/kengaku.md .ufo/l0-questions.md` exit 0; the report needs a `## L0 questions` heading even if empty (exit 2 otherwise, l0_filed_check.sh:88–91) |

## Defects and gaps to fix before any admit
1. Round-26 Q14 pair is not byte-identical: `cmp plans/fixtures/r26/gate_timing/late-report.md plans/fixtures/r26/gate_timing/same-commit-report.md` differs at char 34, line 1 (exit 1). The round-27 pair must be cmp-identical.
2. R10 gap: anchored 4 vs unanchored 5 at base; the receipt must name it.
3. R2/R15 root: the round-26 report exists only at fleet root; the lane has only `.ufo/reports/round-17`.
4. Q9: S044 cannot ground a verdict-agreement reject; keep the novelty +1 reject to the property S044 measures.
5. Pins conflict: lm-eval d6de8164 (RowGsm8kYaml, RowLmEvalFilters, SrcLmEvalDocs), simple-evals 652c89d0 (RowSimpleEvals), inspect 0.3.282 (RowInspectMatch); RowInspectPattern cites `_pattern.py:62–64` where main has :77–78. One pin per row, re-opened at that pin.
6. The pre-registration's "13-column" = awk NF=13 for 11 cells (`scripts/sources-census.sh:3`): consistent. Its "inspect match/pattern implement first/last" holds only for `pattern`; `match` is end/exact.

VERDICT: Q1–Q14 and R1–R15 mapped to concrete artifacts and commands; no blocker, but fixture byte-identity, R10 naming, the fleet-root R2 path, S044's Q9 wording and one pin per row must land before admission. Installs: none.
