# Round 68 attempt 2 — A2 gate green fixture (seat ReportGateVerify)

## Work performed

Attempt 2 re-derived the frozen A2 report-contract predicate on the committed lane
bytes with `plans/round68_report_contract.py` (`0e52fb5d` lineage, sha recorded in
the seat receipts): red on the attempt-1 report bytes, `--selftest` five fixtures,
green on this skeleton, plus three edge cases (missing report path, duplicate
`## SHONEN`, out-of-order headings). Sibling seats re-derived R68-C1 with
`plans/round68_c1_pypi_finish.py` and R68-C2 with `plans/round68_c2_correction_gate.py`.

## Landed changes

| change | commit |
|---|---|
| report-contract gate `plans/round68_report_contract.py` | `0e52fb5d` |
| claims amendment A2 `plans/round-68-claims.md` | `a8883187` |

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — evidence: registry rows `round67_c1_pipeline_probe` and `round65-c1-sqlite-probe --strict` in `SKILL.md`
- [~] At least one end-to-end domain task executed and logged in LOG.md — evidence: `corpus/evidence/round68/pypi/receipt.txt` verdict P/F/F/F
- [~] Instructions executable by an agent without oral context — evidence: `plans/round-68-claims.md` Amendment A2 items 1–4
- [~] No cross-domain bleed (PROVINCE.md still accurate) — evidence: `PROVINCE.md` untouched by the round-68 landing `0e52fb5d`

## Before → after measurements

| claim | before | after | command | verdict |
|---|---|---|---|---|
| R68-C1 | round-68 receipt absent at `d2ed4ca3` | `PREDICATE R68-C1 pass` at `0e52fb5d` | `python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt` | pass |
| R68-C2 | `DEFECTS n=5` at `a8883187` | `DEFECTS n=0` at `0e52fb5d` | `python3 plans/round68_c2_correction_gate.py` | pass |
| A2 gate | attempt-1 report fails S1/S2/S3 | selftest `red-refused=4 green-ok=1` | `python3 plans/round68_report_contract.py --selftest` | pass |

## Sources & frontier

S240 re-sourced (urllib3 `HTTPConnection.__str__` at tag 2.7.0 renders host and
port as separate fields; registry row `corpus/SOURCES.md`) — C1's corrected K2
stderr clause rests on it. The round's own mistake (fleet report without the
required sections) is mined to `corpus/lessons/round-68.md` and now enforced by
`plans/round68_report_contract.py`.

## Trend verdicts

- expansion: improved (`corpus/SOURCES.md` gains S240; SKILL class `network-service` executed 2 of 8)
- quality: improved (`plans/round68_report_contract.py` closes the unenforced report contract)
- discernment: unchanged (`corpus/lessons/round-67-verifier-spotcheck.md` defects corrected as dated errata, no new harm recorded)
