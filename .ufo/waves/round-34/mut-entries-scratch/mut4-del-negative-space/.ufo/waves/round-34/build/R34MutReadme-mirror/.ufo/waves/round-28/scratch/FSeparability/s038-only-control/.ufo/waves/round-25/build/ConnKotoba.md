# ConnKotoba — kotoba-shokunin overlap scan (read-only)

Scope: kotoba's judge/ACES work and any judge-vs-ground-truth calibration, against kengaku C1's S011
application. Sibling tree read only; no git/jj mutation; no installs; scratch was /tmp only.

## Findings

| # | Kotoba anchor | What it is | Ruling | Kengaku disposition |
|---|---|---|---|---|
| K1 | `kotoba-shokunin/corpus/SOURCES.md:77` (section `## Leads (unopened)` at `:68`) | "ACES (arXiv 2608.20614) — Skill Lift via paired live trials; scans vs LLM-judge correlate at ρ 0.14." No URL, fetch log, quote, or Registry row: explicitly unopened. | adjacent-report-out | Weak prior art: judge-vs-static-scan *correlation*, no sens/spec, no interval. If C1 opens ACES, fetch and quote it in kengaku's own SOURCES row; NEVER import ρ 0.14 from this line (kotoba has not opened it either). |
| K2 | `kotoba-shokunin/corpus/SOURCES.md:24` vs `kengaku-shokunin/corpus/SOURCES.md:33` | kotoba S011 = Agentman community post, status `rejected`; kengaku S011 = "How to Correctly Report LLM-as-a-Judge Evaluations", ICML 2026 PMLR 306, `mined`. | none (content); identifier collision | Lane-qualify as "kengaku S011" in the new knowledge entry, the C1 SCORECARD row, and any handoff. Unqualified "S011" resolves in kotoba to a rejected blog post, not the correction paper. |
| K3 | `kotoba-shokunin/PROVINCE.md:29` | "kengaku — LLM/model evaluation and route telemetry." (kotoba's `## Adjacent`, report-don't-absorb) | none; ownership confirms C1's placement | Cite as the boundary that keeps K1 a lead, not a competing measurement; kotoba will not re-derive judge calibration. |
| K4 | `kotoba-shokunin/corpus/knowledge/harness-independent-round37.md:110`, `:307`, `:424` | Judge-free instrument agreement as point fractions ("agreement 24/24 (mode-aware protocol headline; 28 live checks, 4 scoped out)", "28/28 mode-semantics"); `:424` "Agreement falsifies implementations, never specs." | adjacent-report-out | Cite `:424` as C1's scope limit: an accuracy interval is conditional on the receipt GT, and kengaku's GT is journal-derived, not human-labelled (`kengaku-shokunin/corpus/evidence/attrib-r22-legs.log:312-313` `journalctl --user -u ds-flash-shim`, `gt_class` = served). Do not claim S011's human-calibration guarantee (`corpus/knowledge/llm-judge-calibration.md:42`). |
| K5 | `kotoba-shokunin/corpus/knowledge/harness-independent-round37.md:314-316` | "A null instrument … collects 15/28 … 54% of the headline is available for zero content." | adjacent-report-out | Best sibling motivation that a point fraction is gameable. Different remedy, same class: kotoba added a second predicate column + adjudication table; C1 adds an interval rule. Cite, do not re-derive. |
| K6 | `kotoba-shokunin/verifiers/verify_corpus_integrity.py:6-13`, `:28-34` | Bidirectional index check: `corpus.index.unindexed` (file→row, zero) and `index.stale_patterns`/`index.missing_paths` (row→file, zero); reads only column 2 of `corpus/README.md`. | adjacent-report-out (prior art for C2 P2e) | C2's P2e re-implements this shape; kengaku in-lane precedent already at `corpus/evidence/round13-coverage/coverage_census.py:13,169`. Name both in `plans/state_check.py`'s docstring so P2e is not read as a new construct (C2 claims no novelty — correct). |

## Novelty sweep — is C1's construct already in kotoba?

```
grep -rlniE 'clopper|wilson|binomial interval|confidence interval' kotoba-shokunin/{corpus,plans,verifiers}  → exit 1, no matches
grep -rlniE 'rogan|gladen|sensitivity|specificity'                   (same roots)                             → exit 1, no matches
grep -rlniE 'brier|log.?loss|calibration curve'                      (same roots)                             → exit 1, no matches
grep -rn 'INDETERMINATE\|UNTESTED'                                   (same roots)                             → exit 1, no matches
grep -rn 'accuracy' kotoba-shokunin/verifiers/*.py                                                            → exit 1, no matches
```

Ruling: **none** — kotoba has no interval estimator, no sensitivity/specificity correction, and no
statistical verdict vocabulary. C1's construct is not duplicated there. Consistent with peer
`ConnKagiKama.md:17`: typed verdicts are not the novelty; the CP interval + Rogan–Gladen bound is.

## Axis-mapping precedent (novelty → coverage)

- The fleet rule kengaku cites is real: `../PROTOCOL.md:514-516` — a legacy axis row must carry its mapping to one of the six `AXES.md` axes in the same row.
- kotoba hit the same mismatch first: `kotoba-shokunin/SCORECARD.md:11-15` declares `consistency` a sub-axis of `calibration` and routes the `AXES.md`↔`MISSION.md` mismatch to the protocol lane; `corpus/lessons/round-10.md:60-61` names `novelty` among the six-axes mismatch, "routed back out".
- Ruling: **none** on content, but the mapping is fleet convention, not a construct. Keep the C1 novelty
  claim on the interval rule alone (pre-registration already says this — hold that line in the SCORECARD row).
  Do NOT file a second L0 question on the AXES mismatch; kotoba's route is open since round 10 — reference it.

## Offline cross-checks against the committed receipts (not overlaps; grounded, run this scan)

- P2 **resolves YES**: `attrib-r22-legs.log` last block (`:312`) and `attrib-r22-opencode-trials.log` last block (`:204`) hold field-identical 20-row tables (throwaway /tmp parser, all 7 columns compared).
- P1 **resolves YES**: hyper 10/10 at `attrib-r22-legs.log:344` → CP lower `0.025^(1/10)=0.6915`, upper 1.0 → INDETERMINATE.
- Power ask confirmed: `0.025^(1/16)=0.7941`, `0.025^(1/17)=0.8049`, `0.025^(1/20)=0.8316` (pre-reg's 0.7940 rounds down by 1e-4).
- RG bound at n=10/leg (`se_lo=sp_lo=0.6915`, q=0.50, frozen min/max box) = **[0.2769, 0.7231]**, width 0.446;
  width is NOT monotone in n (n=17 → 0.515) because the numerator moves with `sp_lo`. Report the bound **and
  its width**; never print a point share from it, and do not read a wider bound at higher n as worse evidence.
- Parse hazard: `attrib-r22-legs.log` holds TWO `## GT + scoring at close` blocks — `:260` (hyper 9/9 → FAIL at
  `:292`) and `:312` (hyper 10/10 → PASS at `:344`). Concatenating blocks or taking the first flips a stored
  verdict; "last block per file" is load-bearing, and the dedup clause must not merge these two (tables differ).

VERDICT: No kotoba duplicate of C1's S011 application — ACES is an unopened lead, kotoba's judge material is governance-only, and CP/Rogan–Gladen prior art is absent; cite K4/K5 as scope limits, lane-qualify "kengaku S011", and keep novelty on the interval rule, not the axis mapping.
installs: none.
