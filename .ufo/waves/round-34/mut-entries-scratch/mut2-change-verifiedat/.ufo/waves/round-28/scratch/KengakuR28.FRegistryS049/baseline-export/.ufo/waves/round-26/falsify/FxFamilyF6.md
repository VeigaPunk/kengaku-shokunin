# FxFamilyF6 — bounded F6 audit

Scope: only F6 against Amendment 1; no production files changed. `read xd://lsp` returned “No such tool: xd://lsp” and enumerated the mounted devices, so no LSP server/status/references/definition/diagnostics were available. I used exact source reads and executions below; grep was only a locator, not semantic evidence.

## Applicability and independent recomputation

`plans/grader_perturb.py:401-432` has no F6-specific applicability predicate: each included baseline-replayed raw gets `raw.rstrip("\\r\\n") + "\\nFinal answer."`. The suffix is a single bracket-free line. Amendment 1’s candidate/pin/baseline conditions yield 1964 records, and the direct raw pass below confirms no exclusions. The implementation would remove terminal CR/LF before appending, so I explicitly counted this edge: none of the 1964 frozen raws ends in CR/LF; no existing bytes were trimmed in this population.

Commands and relevant exact output (all exit 0):

1. `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/grader_perturb.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --summary`
   - `FAMILY F6 kind=MP n=1964 k=1964 rate=1.000000 cp95_nominal=[0.998124,1.000000] verdict=PASS composite=210/210@1.000000 cp95_nominal=[0.982587,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS`
   - `CLASSES F6 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=88/88@1.000[9/9;79/79]cp95_nominal=[0.959,1.000]`
   - `DEDUP raw+want+grader unique_raw_want_grader=1451 duplicate_groups=294 records_in_duplicate_groups=807 excess_duplicate_records=513`
2. `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r26/perturb_oracle.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin`
   - `POPULATION candidates=1964 included=1964 excluded=0`; `EXCLUDED baseline=0 missing_want=0 meta_truth=0`; `F6 kind=MP n=1964 k=1964`.
   - Oracle is independent (does not import either grader module); its F6 uses `raw + "\\nThe response is complete."` (`perturb_oracle.py:302-303`), a distinct literal but the same bracket-free sign-off transform class.
3. `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/fx_f6_independent.py` (one-off independent frozen-raw parser/replay; hashes all four pinned files and derives truth/replays from grader.py, without calling either audit population/statistics routine)
   - `PINS=4/4 candidates=1964 baseline_replay=1964 excluded=0`
   - `F6 kind=MP n=1964 k=1964 rate=1.000000`; `FJ1 n=1296 k=1296`; `FJM n=492 k=492`; `MULTI n=31 k=31`; `DANGLE n=57 k=57`; `BARE n=88 k=88`
   - `PID_COMPOSITE unit=file+pid;C=file+cell+rep n=210 k=210`; `RAW_TERMINAL_CRLF records=0 stripped_bytes=0 first=None`; `RAW_WANT_GRADER unique=1451 excess_duplicates=513`.

## Interpretation and draft review

All five observed strata and all 210 family composite units preserve the baseline verdict. This demonstrates invariance on the pinned finite population, including MULTI; it is not an iid/future-response guarantee (1451 unique raw+want+grader inputs, 513 excess duplicates). The nominal record CP95 lower bound is .998124 and composite lower bound .982587; both are descriptive PASS under the registered bar, not independent-sample claims. No F6 counterexample survives the specified bracket-free suffix on these raws.

The draft’s F6 result at `drafts/grader-perturbation-audit.md:45,67,73-79` agrees with the independent counts, format strata, and composite caveat. Amendment 1 requires printing the strata/composite and treating these intervals descriptively; this report finds no F6 correction needed. D1 is separate: current code labels it PC and counts previous-answer capture, not MP verdict invariance; its guard is baseline PASS, state/sequence, turn>1, excludes A-MONO/B/C, and requires previous truth != want (`grader_perturb.py:442-446`). The draft correctly states this policy-conformance distinction (`:50-52`), not a grader-correctness claim.

VERDICT: **Scoped invariance supported for F6** — direct frozen-raw recomputation and the independent oracle agree at 1964/1964 with zero exclusions; every printed format stratum and the file+pid/C composite is 100% invariant. Residual risk is limited to unobserved response formats and the non-generalizing, duplicate/correlated corpus; terminal-newline normalization was not exercised because no frozen raw has terminal CR/LF.
