writer: KengakuR29-2.FMutMarkers-2

# FMutMarkers: mutation test of config_projection.py tests (round 29, falsify)

Scope: C1 instrument tests against (a) runtime markers `__last_url__`/`__page__` counted as remaining known tokens and (b) WIKIPEDIA excluded from the six. Every mutant ran only in a `/tmp/fmut-markers/<name>/plans` copy; the lane was not edited.

Result: marker family 3/3 killed, and each is also detected by the frozen-data `--summary` (exit 1). WIKIPEDIA family partly killed: the ORDER, projection-loop and occurrence-census forms are killed. The decoded-census form (M2d) survives and changes findings. The text-census and changed-leaves forms (M2c, M2f) survive as output-only differences.

## 1. Method and independence
- Production source read: yes. I read `plans/config_projection.py` lines 1-548 to choose mutation sites. This is mutation work, not an oracle or re-derivation item.
- Copies: `cp -a /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans /tmp/fmut-markers/<name>/`. Run as `python3 /tmp/fmut-markers/<name>/plans/config_projection.py --selftest|--summary|--json --root /tmp/fmut-markers/<name>`. `--root` is the parent of `plans/`, which is also the `main()` default (`Path(__file__).resolve().parents[1]`); pinned paths start with `plans/`.
- Each mutant is one `edit` on one line of its copy. Revert: `cp` from the pristine control copy, then `diff -rq --exclude=__pycache__` against control. All 11 copies are identical after revert, including after a second apply/revert cycle used to re-run the differential.
- Lane: `sha256sum plans/config_projection.py` = `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` before and after. `diff -rq --exclude=__pycache__` of the lane `plans/` against the control copy: identical.
- Tooling: no installs or updates (no pacman, uv, cargo or npm). Interpreter: `python3 --version` = `Python 3.14.8`. No REA devices. No subagent dispatch.
- Files written: this report; `.ufo/waves/round-29/scratch/falsify/FMutMarkers/differential.py`; `/tmp/fmut-markers/` (copies, all reverted).

## 2. Reproduction of author receipts (observed)
- Control copy and lane `--selftest`: exit 0, `SELFTEST clean cases=20 six_tokens_and_non_url_field,...`. `diff` against `build-selftest.txt` differs only by the receipt wrapper line `exit=0` (receipt line 2).
- Control copy and lane `--summary`: `TOTAL findings=0 exit=0`. The 47 instrument lines match `build-summary.txt`. The receipt's line 48 `exit=0` is a wrapper.
- `--json | sha256sum` = `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` on the control copy and on the lane. This equals `build-json-sha256.txt`.
- Witness `wrong_order_reversed`, reproduced with my reading of its label (W1 below): selftest exit 1 with AssertionError, summary `TOTAL findings=0 exit=0`, matching the receipt. The failing line differs from my prediction (section 6, item 1).
- Witness `url_only_substitution` and `index_by_task_id`: NOT reproduced. The receipt records outcomes only. The lane holds build-seat specs and detectors, not instrument copies: `.ufo/waves/round-29/scratch/R29MutUrlOnly-2/` (mutant-spec.json, candidate.py, detector.py) and `.ufo/waves/round-29/scratch/KengakuR28.R29MutIndex-2/` (wrongoutputfilenamebasedontask_id.mutant.json). They are outside the two assigned families.

## 3. Frozen-data facts (observed; my own counts)
- Raw file: 880776 bytes; sha256 `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` (equals the manifest pin).
- Tasks: 812; task_id values equal `range(812)`.
- Six-token occurrences: GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133.
- Runtime markers: `__last_url__` 65, `__page__` 12. They are not in the six and survive projection.
- Escaped token spellings (`\u005f`): 0. Literal `WIKIPEDIA`: 0. Lowercase `wikipedia`: 23 occurrences; the substring `__WIKI` occurs 0 times.
- Projected-text sha256 per profile is the same for control and for every census-only mutant (for example `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4` for `distinct_origins`; observed in M2b and M2c summaries).

## 4. Mutants (each is one line in its copy)
| id | copy | line | exact change (old -> new) |
|---|---|---|---|
| M1 (assigned) | m1-census | 295 | `for token in tokens}}` -> `for token in tokens + ["__last_url__", "__page__"]}}` |
| M2 (assigned) | m2-order | 29 | `ORDER = (..., "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")` -> `ORDER = (..., "SHOPPING_ADMIN", "MAP")` |
| M1b (sibling) | m1b-global | 272 | `tokens = [... for name in ORDER]` -> `tokens = [... for name in ORDER] + ["__last_url__", "__page__"]` |
| M2b (sibling) | m2b-project | 143 | `for name in ORDER:` -> `for name in (n for n in ORDER if n != "WIKIPEDIA"):` |
| M2c (sibling) | m2c-census | 295 | `for token in tokens}}` -> `for token in tokens if token != "__WIKIPEDIA__"}}` |
| M2d (sibling) | m2d-decoded | 308 | `for token in tokens}` -> `for token in tokens if token != "__WIKIPEDIA__"}` |
| M2e (extra census) | m2e-occ | 279 | `for token in tokens},` -> `for token in tokens if token != "__WIKIPEDIA__"},` |
| M2f (extra census) | m2f-changed | 327 | `for token in tokens},` -> `for token in tokens if token != "__WIKIPEDIA__"},` |
| M1d (sibling) | m1d-decoded-markers | 308 | `for token in tokens}` -> `for token in tokens + ["__last_url__", "__page__"]}` |
| D1 (coverage control) | m2d-gitlab-ctl | 308 | `for token in tokens}` -> `for token in tokens if token != "__GITLAB__"}` |
| W1 (witness reproduction) | witness-order-reversed | 143 | `for name in ORDER:` -> `for name in reversed(ORDER):` |

Diffs against control were checked for M1, M1b, M2, M2b, M2c, M2d, M2e and M2f. Each shows exactly one changed line at the numbers above. M1d, D1 and W1 were confirmed through the edit responses.

## 5. Results (copy selftest, then copy `--summary` on the frozen inputs)
| id | selftest (exit; failing line) | summary (exit; output) | JSON sha256 | verdict | frozen data alone (exit/findings) |
|---|---|---|---|---|---|
| control | 0; 20 cases | 0; TOTAL findings=0 | c8da0c5a... | - | - |
| M1 | 1; AssertionError at line 448 | 1; TOTAL findings=3 (known_token_remaining x3) | 7684e498... | KILLED | YES |
| M1b | 1; AssertionError at line 448 | 1; TOTAL findings=6 (leaf_change_unexplained x3, known_token_remaining x3) | a769cc12... | KILLED | YES |
| M1d | 1; AssertionError at line 448 | 1; TOTAL findings=3 | not taken | KILLED | YES |
| M2 | 1; AssertionError at line 396 | 2; FINDING manifest_contract_mismatch; TOTAL findings=1 exit=2 | 2699080d... | KILLED | YES, via manifest pin (could-not-evaluate) |
| M2b | 1; AssertionError at line 396 | 0; TOTAL findings=0; applied_replacements lacks WIKIPEDIA | 57fa4c60... | KILLED | NO (exit 0) |
| M2c | 0; SURVIVED | 0; TOTAL findings=0; remaining_known_tokens_text lacks WIKIPEDIA | 50e3b76e... | SURVIVED | NO (findings identical) |
| M2d | 0; SURVIVED | 0; TOTAL findings=0; remaining_known_tokens_decoded lacks WIKIPEDIA | 755a8188... | SURVIVED | NO (exit 0) |
| M2e | 1; AssertionError at line 450 | 0; TOTAL findings=0; original_occurrences_by_token lacks WIKIPEDIA | e5fc6de5... | KILLED by selftest only | NO |
| M2f | 0; SURVIVED | 0; TOTAL findings=0; changed_leaves_by_token lacks WIKIPEDIA | 7a5c6174... | SURVIVED | NO |
| D1 (GITLAB) | 1; KeyError '__GITLAB__' at line 417 | 0; TOTAL findings=0 | not taken | KILLED by selftest only | NO |
| W1 (witness) | 1; AssertionError at line 416 | 0; TOTAL findings=0 exit=0 | not taken | KILLED | NO |

Failing assertions, exact text from the tracebacks:
- Line 448: `assert [t["projected_task"] for t in record["tasks"]] == url_expected["projection"] and not findings`
- Line 396: `assert not findings and [s["applied_replacements"] for s in record["steps"]] == [2] * 6`
- Line 416: `assert record["steps"][0]["applied_replacements"] == 1 and record["remaining_known_tokens_text"]["__GITLAB__"] == 0`
- Line 417: `assert record["remaining_known_tokens_decoded"]["__GITLAB__"] == 1 and ...` -> `KeyError: '__GITLAB__'`
- Line 450: `assert {k: v for k, v in result["population"]["original_occurrences_by_token"].items()} == url_expected["raw_replacement_occurrences_by_token"]`

I did not isolate which clause of lines 396 and 448 failed. I report the line.

## 6. Mismatches and surprises
1. W1 prediction versus observation. I predicted the cascade fixture (selftest lines 437-438) would fail first. The observed first failure is line 416, the escaped-token case, `record["steps"][0]["applied_replacements"] == 1`. In reversed order `steps[0]` is MAP, with 0 applications. Location: copy line 143 (`for name in reversed(ORDER):`), selftest line 416.
2. Unreproduced witness lines: `url_only_substitution` and `index_by_task_id` (section 2).
3. Lane artifact not in any receipt: `plans/__pycache__/config_projection.cpython-314.pyc`, mtime `2026-10-21 13:49:19.363592015 -0300`. My commands never imported the lane module. Lane scripts were run as `__main__`, which writes no bytecode, and every import I ran targeted `/tmp` copies. [INFERENCE] a concurrent process imported the lane module. I left the file untouched and did not delete it.
4. Coverage note: the real-data marker counts (65 and 12) appear only in the `--summary` output. The selftest's only marker-count assertion is line 451, on the synthetic hand fixture (expected `{"__last_url__": 1, "__page__": 1}`).

## 7. Survivors and frozen-data detectability
- F1, finding-changing survivor: M2d (decoded census drops WIKIPEDIA). Selftest exit 0. Frozen `--summary` exit 0, with the output key set changed. Random differential: 337 of 3000 findings differ. Probe P3 (escaped WIKIPEDIA produced by a MAP value): control `[known_token_remaining]`, M2d `[]`. Frozen data alone: NO. The frozen population has WIKIPEDIA count 0 and escaped-token count 0, so this census is identically 0 on it.
- F2, output-only survivor: M2c (remaining text census drops WIKIPEDIA). Selftest exit 0. Frozen exit 0 with findings identical. Random: 0 of 3000 findings differ, while the result JSON differs in 3000 of 3000. Real-data `--json` sha256 `50e3b76e...` differs from control `c8da0c5a...`. Frozen data alone: only a byte comparison against the pinned receipt would detect it. [INFERENCE] the text census never changes a finding on valid JSON, because text count is at most decoded count (section 8). This is observed in the sample, not proven.
- F3, output-only survivor: M2f (changed-leaves-by-token drops WIKIPEDIA). Selftest exit 0. Frozen exit 0. Random: 0 findings differ. Frozen data alone: NO, byte comparison only.
- Output-only kills by selftest: M2e (line 450) and D1 (line 417). Frozen data alone: NO for both.
- Projection-level mutant M2b: frozen data alone gives exit 0 and an identical projected text sha256. Only `applied_replacements` changes. The selftest kills it at line 396.

## 8. Random differential and probes (observed)
- `differential.py`: seed 29, 3000 random valid raw documents (0 invalid), one profile per document, values drawn from a 10-value pool. It compares every mutant with control on findings and on result JSON.
- Findings differ from control: M1 278; M1b 464; M2 752; M2b 353; M2c 0; M2d 337; M2e 0; M2f 0. No mutant raised exceptions.
- Control property: `remaining_known_tokens_text[t] > remaining_known_tokens_decoded[t]` occurred 0 times over 3000 profiles x 6 tokens. Text count > 0 with decoded count 0 occurred 0 times. [INFERENCE] general form: a token occurrence in valid JSON lies inside a string whose decoded form contains it.
- The saved script reproduces these numbers on the re-applied mutant copies; they match the evaluation cell. On reverted copies it reports zero differences for every mutant.
- Probes (findings ids per copy):
  - P1 (raw `\u005f\u005fWIKIPEDIA__`, all values `http://v.invalid`): control `[known_token_remaining, leaf_change_unexplained]`; M2d `[leaf_change_unexplained]`; M2 `[]`; all other copies match control.
  - P2 (MAP value contains literal `__WIKIPEDIA__`): control `[known_token_remaining]`; M1, M1b, M2b, M2c, M2d, M2e and M2f match control; M2 `[]`.
  - P3 (MAP value contains `\u005f\u005fWIKIPEDIA__`): control `[known_token_remaining]`; M2d `[]`; M2 `[]`; all others match control.
  - P4 (raw `__last_url__` only): control `[]`; M1 `[known_token_remaining]`; M1b `[known_token_remaining, leaf_change_unexplained]`; M2, M2b, M2c, M2d, M2e and M2f `[]`.
  - P5 (clean): `[]` for every copy.

## 9. WIKIPEDIA census-key coverage in the selftest (from its source, lines 385-521)
- Occurrence census (line 279): pinned, because the url-only expected JSON contains `"__WIKIPEDIA__": 0` and line 450 compares the whole dict. Killed (M2e).
- Remaining text census (line 295): not pinned. Line 416 asserts `__GITLAB__` only. Survived (M2c).
- Remaining decoded census (line 308): not pinned. Line 417 asserts `__GITLAB__` only. Survived (M2d). The same exclusion for GITLAB (D1) is killed at line 417, so the gap is specific to WIKIPEDIA.
- Changed-leaves-by-token (line 327): never asserted. Survived (M2f).

## 10. Limits of this attack
- Single-line mutants at each census point. Other single-line variants were not run.
- The random generator is mine and seeded. It is a sample, not exhaustive.
- Kill attribution is by the failing line of the traceback. Clauses were not isolated.
- Frozen-data conclusions cover the frozen raw population only. On that population, WIKIPEDIA has 0 occurrences, so no WIKIPEDIA-specific census change can alter a frozen finding by construction [INFERENCE from the observed counts].

VERDICT: PARTIAL
