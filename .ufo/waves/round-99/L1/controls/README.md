# Round 99 prefreeze controls (P2; L1 KengakuR99)

All controls run against the P1 instrument bytes (`e219e785`) in fixture clones under
`/fast/scratch/hyaku/kengaku-r99/L1/ctl-<run>/` (never the lane). Each fixture first commits a fixture-only
`plans/round-99-claims.md` with the frozen-instruments block of the P1 bytes, so L4/L8/L11 and K1 resolve;
both counters run from the fixture root. Every battery ran TWICE (`-run1`, `-run2`) before F (Q80); the
`LEGS`/`TARGET`/`PREDICATE`/`rc`/`GATE` lines agree run1 = run2 for all 21 receipts (checked by md5 of those
lines). Runner: `run_controls.sh <run> <P1> <grader venv>`; `run_partial_fixed.sh` (see M2 below).
Candidate bytes tested are retained in `candidate/` (`ledger.json` lands as
`plans/grader-population-ledger.json`; `prov/corpus/evidence/round<N>/PROVENANCE.md` land at those paths).

## R99-C1 (`c1-*-run{1,2}.txt`)

| control | expected | run1 / run2 | failing legs |
|---|---|---|---|
| do-nothing (fixture freeze only) | fail | fail / fail | L1 L2 L3 L5 L6 L7 L9 L10 |
| positive (probe receipt + C1 candidate) | pass | pass / pass | — |
| extra-member forgery (`crack-7z-hash` also flipped) | fail | fail / fail | L7 only (`set_added` two members) |
| forged-receipt (C03's DETAIL `final=` digest zeroed) | fail | fail / fail | L3 L6 |
| counter-edit (counter bytes changed after the fixture freeze) | fail | fail / fail | L11 only (round-98 MutC1 survivor killed) |
| c2only (provenance files only) | fail | fail / fail | as do-nothing |
| both | pass | pass / pass | — |

Positive TARGET: `executed_rows=43 member=bn-fit-modify cells=file-artifact:34 set_equals_base_plus_member=1 located=1 executed=1 cases=13 legs=130 mismatches=0 new_rows=8 new_rows_flagged=0 defects=0`.

## R99-C2 (`c2-*-run{1,2}.txt`)

| control | expected | run1 / run2 | failing legs / finding |
|---|---|---|---|
| do-nothing | fail | fail / fail | K4 K5 (`still=12`) |
| positive (eight PROVENANCE.md files) | pass | pass / pass | `cleared=12 … outside_removed=0 outside_added=0 outside_rebound=0`; `GATE defects base=45 rev=33` |
| partial (`partial-run*`, HARNESS DEFECT) | fail | **pass / pass** | invalid control: `git rm` of an untracked copy failed, fixture equalled positive (lesson M2) |
| partial-fixed (round95 file absent) | fail | fail / fail | K4 K5 (`still=1`, S306) |
| url-channel (positive + a URL-column line) | fail | fail / fail | K3 K4 K5 K7 (`moved=S256`: the URL channel re-binds an outside row) |
| duplicate-line (second S180 line to its byte-identical round-82 copy) | fail | fail / fail | K4 (`lines=2`) K5 |
| sha-column (one sha cell zeroed) | fail | fail / fail | K4 only (round-98 MutC2 M05/M18 survivor killed) |
| outside-rebind (positive + a line binding non-population S210) | fail | fail / fail | K7 only (`moved=S210`) |
| row-edit (POP tokens elided from SOURCES, no provenance) | fail | fail / fail | K4 K5 K6 K7 |
| gate-edit | fail | fail / fail | K1 only |
| capture-edit (`round50/git-fetch.adoc` changed) | fail | fail / fail | K4 K5 K6 |
| c2counter-edit (counter bytes changed after the fixture freeze) | fail | fail / fail | K1 only |
| c1only (C1 candidate + receipt, no provenance) | fail | fail / fail | K4 K5; `GATE base=45 rev=45` (C1 adds no finding) |
| both | pass | pass / pass | — |

## Pre-freeze source gate

`candidate/sources-validate.txt`: `sources-census.sh validate --file` on a `git archive` mirror of P1 with
the candidate SOURCES.md → rc 0 (31 W04 warnings: the 30 pre-existing plus S334, whose URL equals S181's
across scopes).
