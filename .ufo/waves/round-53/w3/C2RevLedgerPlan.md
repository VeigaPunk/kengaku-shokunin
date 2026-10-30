# C2RevLedgerPlan — committed ledger review

## Scope and axes
Calibration/truthfulness, evidence specificity, reproducibility, and containment. Reviewed the committed 78-row ledger and registry at fresh-clone HEAD `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe`; read facts first and frozen claims including A1–A3. No lane implementation edited. This is a review recommendation, not admission.

## Findings, severity first

### Medium — round46-c3 reason mistakes rejected map rows for absent tags
`plans/round53-tipstate.json:723` says the requirement map lacks `both-print` and `toolchain`. Both tags actually occur in map rows at `corpus/knowledge/tb2-polyglot-c-py-grader.md:86,89`, marked not exercised. The fresh run reports both rows as unparsed before reporting missing tags (`C2RevLedgerPlan/round46-c3.txt:18`); the parser explicitly records unparsed rows at `plans/round46_c3_verify.py:389-390`. The declaration correctly predicts exit 1 and its evidence matches verbatim, but the stated cause hides the distinction between absence and rows rejected by the map grammar. Describe rejected/unexercised rows, not missing source content. V8's declared failure and V2's green state were independently reproduced.

### Low — weak fragments do not substantiate the detailed reasons by themselves
`adoption-check` evidence at ledger line 14 is only `census=fail`; `round28-census` evidence at line 371 is only a JSON mismatch count. Both match their own fresh output, but neither identifies the detailed cause claimed by its reason. Adoption's child stderr is captured and discarded (`plans/adoption_check.py:134-147`); a separate direct replay of that child reproduced missing configuration and unknown-lane errors, exit 2. Round28 emits the aggregate mismatch count, not the pointer id; the separate state-assertion sample and `PROVINCE.md:129-130` corroborate that pointer cause. These are evidence-quality limitations, not proven false declarations or frozen-predicate violations. Prefer row-specific diagnostic fragments when available; otherwise clearly distinguish cause derived from source/another instrument.

## Static receipt (verbatim)

```text
ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok
ARGV entry=74 selftest=4 help=0 help_limit=7.8
DRY static legs only: no predicate
```

Command exited 0. Static checks establish the registered script match, declaration consistency and reason-length threshold; they do not execute rows or certify causal prose. Canonical execution logic is `plans/round53_c2_tipstate.py:127-146,271-317`: each row is reset, run with filtered environment and its own TMPDIR, then exact exit and red evidence membership are checked. No full-counter predicate was claimed here.

## Every red row

All 12 reasons are specific rather than interchangeable boilerplate; all have at least 10 whitespace-delimited words. All declare exit 1 consistently with red. “Sample pass” means independently executed with exact declared argv and verbatim fragment comparison; “static only” does not certify the unexecuted row's runtime or every historical assertion.

| Row | Reason words | Verdict | Defect / qualification |
|---|---:|---|---|
| adoption-check | 46 | Sample pass; weak evidence | exit 1, fragment present; separate child replay supports cause, but fragment alone does not. Universal claim about any external clone is broader than this measurement. |
| anchor-digest-check | 27 | Sample pass | exit 1, fragment present; actual row-specific diagnostics identify S173–S193. |
| gate-flip-check | 31 | Static only | Instrument-shaped specific fragment; no thin/boilerplate reason found; runtime not sampled. |
| mutant-direction-check | 37 | Static only | Specific N21 fragment. Source docstring at `plans/mutant_direction_check.py:5-8` supports strict-prefix direction argument; runtime not sampled. |
| round28-census | 44 | Sample pass; weak evidence | exit 1, fragment present; output contains aggregate mismatch and 56/56 index counts, not pointer identity. Separate state sample supports pointer cause. |
| round35-c1-coverage | 47 | Static only | `plans/round35_c1_verify.py:153-155` really hard-codes 42/42; sample census confirms current 56/56. Runtime not sampled. |
| round38-c1-mutants | 42 | Static only | Specific summary, N21 mechanism supported by direction-check source. Historical landing equivalence and complete killed/battery counts were not independently replayed. |
| round40-c1-mutants | 50 | Static only | Specific battery summary; anchor sample corroborates 21 unbound rows. Seven-survivor and fixture-by-fixture causal claim not independently replayed; summary fragment alone cannot prove cause. |
| round46-c3 | 44 | Sample exit/evidence pass; reason defect | exit 1, fragment present; tags exist in rejected rows, not absent from source map. See medium finding. |
| round51-surfaces | 32 | Static only | `PROVINCE.md:113` still states 171; sampled census reports 186; `plans/round51_surfaces.py:207-208` emits drift. Runtime not sampled. |
| round52-c1 | 28 | Static only | Specific capture-count fragment; exclusion is documented in frozen claims. “Only” amended predicate passes is broader than this isolated evidence and was not independently replayed. |
| state-assertion-check | 31 | Sample pass | exit 1, fragment present; pointer target line 129 is blank and heading is line 130. |

## Green sample

| Row | Observed exit | Verdict |
|---|---:|---|
| attrib-probe | 0 | matches |
| benchmark-spec-audit | 0 | matches |
| catalog-probe | 0 | matches |
| config-projection | 0 | matches |
| hermetic-grader | 0 | matches |

Ten independent per-row clones: five red plus five green; 10/10 exact exit matches, 5/5 red fragments present, zero sample timeouts. Red sample selection deliberately covers host-dependent failure, row-specific diagnostics, nested aggregate, compound counter and pointer mismatch. It is not a random or population-wide measurement.

## Copyability and duplicate audit

Exact duplicate nonempty evidence strings across the 78 declarations: **0**. Cross-search of each of the 12 red fragments against the other nine/ten saved sample outputs: **0 cross-row hits**. No actual copied declaration demonstrated. The generic adoption/census fragments remain plausibly reusable in unrelated failures; the frozen counter checks only substring membership, not uniqueness or causal entailment (`round53_c2_tipstate.py:308-310`). Conversely, copying correct observed output is expressly permitted by frozen claim C2; duplication alone would not prove fabrication.

## Commands and artifacts

Commands executed (all execution TMPDIR paths explicitly confined):

```sh
/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
mkdir -p /fast/scratch/hyaku/kengaku-r53/C2RevLedgerPlan && git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/C2RevLedgerPlan/lane && git -C /fast/scratch/hyaku/kengaku-r53/C2RevLedgerPlan/lane rev-parse --show-toplevel && git -C /fast/scratch/hyaku/kengaku-r53/C2RevLedgerPlan/lane rev-parse HEAD
env TMPDIR=/fast/scratch/hyaku/kengaku-r53/C2RevLedgerPlan python3 plans/round53_c2_tipstate.py --lane . --dry
env TMPDIR=/fast/scratch/hyaku/kengaku-r53/C2RevLedgerPlan python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C2RevLedgerPlan/sample.py
env TMPDIR=/fast/scratch/hyaku/kengaku-r53/C2RevLedgerPlan /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /fast/scratch/hyaku/kengaku-r53/C2RevLedgerPlan adoption-check
rm -rf /fast/scratch/hyaku/kengaku-r53/C2RevLedgerPlan
```

Dry/sample command cwd was the initial scratch lane; child census cwd was the adoption-check sample clone. `sample.py` records the exact per-row clone/rev-parse/argv commands and filtering; `sample-results.json` records each argv, cwd, exit, fragment comparison and duration. The initial clone printed the required scratch top-level before its HEAD. Each sample clone's top-level was asserted before its argv ran. No fixture repositories or additional runtime were created beyond the prescribed instrument executions. Disk guard reported scratch 42% used and 467.6G free; no ENOSPC. No tools installed or updated.

Every produced file is under the following absolute directory, except this sibling report:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C2RevLedgerPlan/`

- `sample.py` (reproduction driver), `sample-results.json`, `static-dry.txt`.
- `adoption-check.txt`, `anchor-digest-check.txt`, `round28-census.txt`, `round46-c3.txt`, `state-assertion-check.txt`.
- `attrib-probe.txt`, `benchmark-spec-audit.txt`, `catalog-probe.txt`, `config-projection.txt`, `hermetic-grader.txt`.
- Report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C2RevLedgerPlan.md`.

## Residual risk and verification gaps

LSP device unavailable: `read xd://lsp` returned “No such tool”; therefore no semantic references/definition/diagnostics server was available. Literal grep and source reads were fallback evidence, not semantic proof. Seven red and 61 green declarations were not re-executed by this seat; the independent full measurement seats must supply population truth. No resume/rerouting implementation is changed or in scope, and no saturation/one-runtime claim is inferred from this ledger. Snapshot review is AS COMMITTED, not a review of unrelated live lane edits.

Self-evaluation: accuracy 4/5 (seven red runtime/historical details deliberately unverified); completeness 4/5 (requested 5+5 sampling complete, broader cause assertions remain explicitly bounded); clarity 4/5 (table separates static from runtime); actionability 4/5 (exact cause correction and artifacts provided); conciseness 4/5 (reproduction detail adds length). Overall 4.0/5. Improvement priority: combine this review with the independent full 78-row receipt before any C2 admission.
