# E2LedgerRefine findings

- Refined ledger: `.ufo/waves/round-54/w1/E2LedgerRefine/round54-entrytruth-refined.json`.
- Executed all 16 `entry_state=red` rows in separate shared clones of the lane's current tip, calling the declared argv under `round54_c2_entrytruth.py`'s `hermetic_env` (scrubbed GIT config, scratch HOME). Captured stdout+stderr; refined only `reason` and `evidence` for red rows. Schema/JSON sanity succeeded; red-row count: 16.
- Mismatch list (name, declared, observed): `scratch-root-guard`, 2, 1. Observed output ended `CHECK red reason=sentinel-missing round=None want=* seats=5`; the declared argv is `python3 plans/scratch_guard.py check .`. The declared ledger fields were left unchanged as required. All other 15 red rows matched their declared exits.

Three before/after reason examples:
1. `adoption-check` — before: “the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output” → after: “The adoption census reports census=fail despite three indexed cited rows being present; this gate returns nonzero because the round-level adoption census condition is unsatisfied.” Evidence: `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=fail`.
2. `anchor-digest-check` — before: “the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output” → after: “The digest audit finds source rows whose anchor tokens lack capture locators; its 21 anchor-unbound defects in SOURCES.md cause the failed audit exit.” Evidence: `rows=190 tokens=92 defects=21`.
3. `gate-flip-check` — before: “the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output” → after: “The round-52 lesson records three flip decisions with unresolved no-line resolutions; these unresolved flips and missing citations make the gate fail.” Evidence: `FLIPS total=3 unresolved=3`.

Observed command results: all 16 invocations completed; 15 matched and one mismatch above. `python3 refine.py` loaded the refined JSON, counted red rows and printed the mismatch list and examples. No software/tool installations.
