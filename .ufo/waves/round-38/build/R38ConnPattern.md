# R38ConnPattern — cross-claim pattern scan: do the counters/probe carry the C1-survivor shapes?

Seat: R38ConnPattern (connector, leaf). Wave 1, kengaku r38.
Axes touched: calibration (primary — the C1 counter is the instrument being calibrated), coverage
(secondary — C2's V7/receipt parsing), operability (the findings are one-line fixtures wave 2 can run).

## Question and method

The four survivor shapes from the round-37 wave-2 extra-mutant seats are: (a) check applied to the
first item only, (b) off-by-one threshold, (c) loosened compare, (d) pass side never exercised.
Do the frozen round-38 instruments themselves — `plans/round38_c1_verify.py`,
`plans/round38_c2_verify.py`, `plans/build_pmars_probe.py` — and the earlier lane counters
(`plans/round2*_*.py`, `plans/round3*_*.py`) contain any of these shapes?

Method: read the three round-38 files in full; grep + read every round-28..round-37 counter; verified
suspected parses against the committed receipts (`corpus/evidence/round36/regex-log-probe.txt`,
`corpus/evidence/round38/build-pmars-dry-cases-freeze.txt`) so that no "dead check" claim rests on
assumed formats. Lane read-only; no fixtures executed; no scratch needed.

## Findings — round-38 files (frozen)

| # | Site | Shape | State | Exposure fixture (one line) |
|---|------|-------|-------|------------------------------|
| 1 | `plans/round38_c2_verify.py:222` — v7 `sec = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", entry, re.S\|re.M)` | first item only — LIVE | Only the FIRST `## Requirement map` section is parsed; a second, contradictory map section lower in the entry is never examined, and v7's missing-tag check only sees the first. | Entry whose first map section is fully correct (all frozen tags, receipt-derived labels) plus a second `## Requirement map` section labelling every tag `enforced` — V7 still prints ok. |
| 2 | `plans/round38_c2_verify.py:154` — `receipt_cases`: `re.match(r"^CASE (\S+) predicted=(pass\|fail) observed=(pass\|fail) .*?\bviolates=(\S*)", l)` | loosened compare — LATENT | `.*?\bviolates=` takes the FIRST `violates=` in the line; any future field before the tag list containing that token silently corrupts the parsed tag set and hence V7's derived labels. Under the frozen probe format the tag list is always first (requirement text follows ` -- `), so unreachable today. | Hand-typed receipt line with a pre-tag field containing `violates=forged` (e.g. a probe v2 `note=` field): parsed tag set becomes `{forged}`, V7 mis-derives. |
| 3 | `plans/round38_c1_verify.py:168` — side-channel scan `hits = [t for t in SIDECHANNEL if t in text]` | loosened token match (fail-closed) | Raw substring scan over the whole module source INCLUDING docstrings: token `environ` matches "environment". Disclosed in the claims docstring as "a heuristic, not a proof"; errs toward false rejection of honest fixtures, cannot admit a real side-channel fixture. | A battery38 module whose docstring contains the word "environment" is counted `sidechannel>0` → predicate red. |
| 4 | `plans/build_pmars_probe.py:327-328` — verdict dict `got[parts[1]] = (...)` | first item only (last-wins) — LATENT | Duplicate `TEST <name>` lines in harness output overwrite; the frozen harness prints each test exactly once. | A grader test that prints `TEST test_pmars_works P` to stdout of its own would shadow the harness verdict; unreachable with the pinned capture. |
| 5 | `plans/build_pmars_probe.py:317` — smoke check `"SMOKE out=Results: 12 34 78" in out` | loosened compare | Substring containment, but `--smoke` exercises plumbing only and is outside the frozen predicate; the graded receipt parse (`set(got) != set(TESTS)`, line 329) is full-set. | None needed; not predicate-bearing. |

Checked and NOT found in the round-38 instruments: (i) V4's summary regex
(`plans/round38_c2_verify.py:65`) is fully anchored `^...$` and cross-checked against per-case parses —
the hinted "V4 summary regex" is sound; the looseness sits one function below it (site 2). (ii) No
off-by-one threshold exists in either counter — all bounds come from the pinned spec/table and are
compared as exact sets (`round38_c1_verify.py:264` `res[1] == frozenset(declared)`;
`round38_c2_verify.py:137-146` summary cross-check). (iii) The C1 pass side IS exercised:
`run_gate` records the `ok` set (`round38_c1_verify.py:177-186`) and the mirror kill rule reads it
(`round38_c1_verify.py:204`), which is precisely the round-37 fix. (iv) `first={mism[0]}`
(`round38_c1_verify.py:218`) prints only the first pin mismatch but the count still gates — cosmetic.

## Findings — earlier lane counters

| # | Site | Shape | State / fate | Exposure fixture (one line) |
|---|------|-------|--------------|------------------------------|
| 6 | `plans/round37_c1_verify.py:270-277` (`run_gate` returns `(rc, bad)` only), `:347-351` (`differs`) | pass side never exercised — HISTORICAL | The round-37 observable result has no `ok` set, so a mutant whose only effect is on `ok` output (or any non-declared difference) was invisible unless rc changed — the gameability shown in `.ufo/waves/round-37/build/R37CritC1Battery.md` and closed by the round-38 attributed rule (site: `round38_c1_verify.py:191-204`). | A mutant renaming the ok token (`P3 okay` for `P3 ok`): round-37 fixtures all still match (rc, DEFECT set) → survives; round-38 reference `ok` set loses P3 → fixture-declared mismatch → red. |
| 7 | `plans/round37_c2_verify.py:193` — `verdicts = {observed.get(c) for c in cited}` | loosened to one convenient witness — HISTORICAL (mined D2) | The round-37 map label was checked only against the cases the row CITES, so `enforced` beside a passing violating case passed — the round-37 closure item D2; fixed by round-38 V7 deriving the label from ALL receipt cases whose `violates=` carries the tag (`round38_c2_verify.py:223-232`). | Receipt where tag T is violated by one observed-fail and one observed-pass case; entry row `T enforced` citing only the failing case → round-37 green, round-38 red (derives `partly`). |
| 8 | `plans/round37_c2_verify.py:202` — `missing = sorted(set(range(1, 10)) - covered)` | off-by-omission (first 9 lines only) — HISTORICAL | Hard-coded coverage of instruction.md lines 1-9; a requirement on line ≥10 needed no map row. Round-38 V7 iterates the dry table's TAG lines instead, so any frozen tag forces a row. | instruction.md with a 10th-line requirement and a map covering lines 1-9 → round-37 `missing` empty → green; round-38 red (unmapped frozen tag). |
| 9 | `plans/round31_c1_verify.py:79-81`, `plans/round32_c1_verify.py:83-85`, `plans/round33_c1_verify.py:89-91` — `line = next((raw for raw in entry.splitlines() if re.match(rf"^source: {sid}\b", raw)), "")` | first item only — HISTORICAL | Only the FIRST `source: <sid>` line of the entry was ever validated; a duplicate, stale source line was invisible. Round-35 moved to positional header cells (`round35_c1_verify.py:109`), which does not scan duplicates either but pins the expected position. | Entry with two `source: S094` lines, the first stale/wrong → rounds 31-33 green; a wave-2 control with a contradictory second line exposes it. |
| 10 | `plans/round31_c1_verify.py:56-66`, `plans/round32_c1_verify.py:58-68`, `plans/round33_c1_verify.py:62-71` — `rows[match.group(1)] = ...` dict build | first/last item only — HISTORICAL | Duplicate registry rows for one sid silently collapsed (later overwrites earlier); only one row per sid was ever checked. Fixed in round-35: `if len(got) != 1: return ...` (`round35_c1_verify.py:84-85`), kept in r36/r37/r38 V3 (`round38_c2_verify.py:142`). | SOURCES.md with two S094 rows (one wrong) → rounds 31-33 validate the survivor only; round-35+ red. |
| 11 | `plans/round36_c1_verify.py:91,99` — `for l in data[:8]`, `[data[0]] * 8` | first-N items only — LATENT | The quote mutators touch only the first 8 data rows of the Located-quotes table; the genuine round-35 entry has exactly 8, so the fixtures are exact today. A 9-row table would leave row 9 verbatim and could mislabel the fixture intent. | A genuine entry whose Located-quotes table grows to 9 rows: P2 (`mut_one_word`) leaves the 9th quote intact → the intended P3 rejection may not fire. |
| 12 | `plans/round36_c1_verify.py:82` — `first, last = rows[1], rows[-1]` (comment "rows[0] is the header") | first-item assumption — LATENT | `quote_table` assumes the first `|`-line of the section is the header; a data-first section would have its first data row skipped by every `rewrite_quotes` consumer. Pinned genuine entry always has the header. | Located-quotes section with the header line removed: `rows[0]` is data, `rows[1]..` mutates everything except the first genuine row. |
| 13 | `plans/round30_defects.py:185` — `frontmatter = entry.split("\n\n", 1)[0]` | first item only — LATENT | check_d5 scans only the FIRST paragraph for the `source: S091` repair; the same line anywhere later in the entry is invisible and the check falls through to the used-by-note branch. | Entry satisfying the S091 repair with `source: S091` in its second paragraph → check_d5 red unless the asymmetry note is also present. |

## Synthesis (connector move)

1. The round-38 instruments already absorbed three of the four shapes as *fixes*: the attributed kill
   rule with the recorded `ok` set (kills shape d, site 6), V7's all-violating-cases derived labels
   (kills shape c-as-witness, site 7), and the tag-driven map (kills shape a/b at the map level,
   site 8). What survives in the frozen counters is one live first-only shape (site 1, V7 first
   section) and a latent first-match looseness one function away from the hinted site (site 2).
2. No off-by-one threshold instance exists in any lane counter; the off-by-one shape lives in the
   gate mutants themselves (N02 `> min_distinct_locations`, N06 `+1`, N09 `-1`) and in the probed
   TB2 grader (`one-address`: the >=2 debugger-lines threshold). The counters compare exact sets.
3. Cross-claim mirror worth a wave-2 note: `build_pmars_probe.py`'s CASES table is a catalogue of
   the same four shapes as found in the pinned grader — `results-trailing-text` (loosened compare,
   `re.match` prefix), `one-address` (off-by-one threshold), `pmars-dir-elsewhere` (one-level glob =
   first-only depth), `canned-shape` pass side (the grader's pass side exercised by a canned
   artefact). C2's coverage claim and C1's calibration shapes are the same finding read in opposite
   directions: the lane's instruments hunt in graders the very shapes their own predecessors had.
4. Cheapest hardening moves (for the L1, no edits made): (i) v7: iterate ALL `^## Requirement map`
   sections or reject a second occurrence (`re.findall`); (ii) `receipt_cases`: anchor the tag list
   to a field boundary (` r"violates=(\S*)"` preceded by ` match=\S+ `) or split on ` -- ` first;
   both are one-line changes but the files are frozen — propose as wave-2 controls instead.

## Verification

- `grep -n -E 're.search\(r"\^## Requirement map|receipt_cases|SUMMARY = ' plans/round38_c2_verify.py` →
  sites at lines 65, 154, 222 (output reproduced in session).
- `sed -n '55,115p' plans/round31_c1_verify.py` / `round32_c1_verify.py` / `sed -n '70,95p' round35_c1_verify.py` →
  dict-overwrite rows in r31/r32/r33, `len(got) != 1` fix in r35.
- `head -12 corpus/evidence/round36/regex-log-probe.txt` → round-36 receipt lines are `case=<id> ... match=yes|NO`,
  so `round36_c2_verify.py:193` `re.match(r"case=(\S+) .* match=NO ")` matches its own receipt format;
  a suspected dead-check instance there was investigated and RETRACTED.
- `grep -o 'violates=[^ ]*' corpus/evidence/round38/build-pmars-dry-cases-freeze.txt` → 22 tag lists, none
  containing a second `violates=` token; site 2 is latent under the frozen probe format.

VERDICT: pattern-13-sites
