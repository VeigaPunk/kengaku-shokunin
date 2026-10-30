## Round 54 — externally anchored freeze and entry-truth calibration (DRAFT)

Frozen claims: `plans/round-54-claims.md`; base `6c919180260ea545589c2c0a007a06f554b529d3`; stage-1 freeze `17f90355c3ec17dcf15f7980d83f1943ae428fe5`. Claims anchor sha256 `d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8` (assignment-provided, not scribe-recomputed). Axes: novelty and calibration; lowest coverage 7 remains capped by open L0 round-25/33/51 questions, no stagnation waiver.

Measured landing revision/cleanliness: MEASURED-TBD — commands `git rev-parse HEAD` and `git status --porcelain` in the authorized clean landing clone; retain source revision and clean status from both counters too.

| claim / axis | before → observed after | counting command | predicate / score disposition |
|---|---|---|---|
| R54-C1 / novelty | MEASURED-TBD — command B1 below retrieves frozen before receipt (anchor absent, exit 1); after TBD — command C1 below supplies BINDING, ATTESTATION, EXTERNAL PIN, controls and exit | C1 below | MEASURED-TBD — C1 supplies predicate, V supplies outside verdict. Target 8→9, not awarded; published prior practice requires replication/instrument-new and hold at 8. |
| R54-C2 / calibration | MEASURED-TBD — command B2 below retrieves frozen before receipt (registry 78, ledger 0, exit 1); after TBD — commands C2/C2D below supply every entry declaration/execution, migration, laundering, mismatch, timeout and evidence count | C2 and C2D below | MEASURED-TBD — C2/C2D supply predicates, V supplies outside verdict. Target 9→10, not awarded. Truthfully red declarations are allowed; matching exits do not prove gate soundness. |

Fill commands (from lane root, not executed by this scribe):

- B1: `cat corpus/evidence/round54/c1-before.txt`.
- B2: `cat corpus/evidence/round54/c2-before-dry.txt`.
- C1: `python3 plans/round54_c1_anchor.py verify --anchor corpus/evidence/round54/anchor --claims plans/round-54-claims.md --source "$CLEAN_CLONE" --work "$SCRATCH/c1" --controls`.
- C2: `python3 plans/round54_c2_entrytruth.py --lane . --source "$CLEAN_CLONE" --work "$SCRATCH/c2" --jobs 3 --timeout 900`.
- C2D: `python3 plans/round54_c2_entrytruth.py --lane . --dry`.
- V: `find .ufo/waves/round-54 -type f -iname '*verdict*' -print -exec cat {} \;`; use only canonical outside adjudication for score admission, never a seat's recommendation. If unavailable, retain TBD.

CLEAN_CLONE must be clean at landing tip; SCRATCH must be under the authorized executor's `/fast/scratch/hyaku/kengaku-r54/` directory. C1 verify requires the declared OpenTimestamps Python library. Executions and receipts belong to authorized executor/L1 seats, not this scribe.

Controls already inspected: `claims/c2-route-r53.txt` under `.ufo/waves/round-54/` is the red-before laundering demonstration; `c2-route-closed.txt` shows truthful fixture pass and laundered fixture fail; `c2-env-poison.txt` shows inherited-env leakage and r54 blocking. No full-registry measurement follows from those controls alone. C1 internal-only control/prior-art source verdicts: TBD — command `find .ufo/waves/round-54 -type f \( -iname '*internal*' -o -iname '*PriorArt*' \) -print -exec cat {} \;`.

No-harm / other axes: TBD — command `find .ufo/waves/round-54/w1 -type f -iname '*noharm*' -print -exec cat {} \;`. Baseline depth/operability/freshness/adjacency are 9 and coverage 7; no change is proposed, but absence of harm is not pre-certified. Frozen-file byte preservation: TBD — command `git diff 17f90355c3ec17dcf15f7980d83f1943ae428fe5 -- plans/round53_c2_tipstate.py plans/round53-tipstate.json plans/round53_c1_triage.py SKILL.md plans/round-54-claims.md`.

Round shape: TBD — command `find .ufo/waves/round-54 -maxdepth 2 -type f \( -iname '*dispatch*' -o -iname '*results*' -o -iname '*policy*' \) -print -exec cat {} \;`. Frozen plan: one v2 build+attack wave, 64 seats, ≥25% attack roles. Count actual dispatch, qualifying attacks, settled outputs and residual calls from receipts; contract-only seats and provider failures never count as executed clearance.

Frontier-step census and source changes: TBD — commands `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` and `git diff 17f90355c3ec17dcf15f7980d83f1943ae428fe5 -- corpus/SOURCES.md`. Assimilation TBD — command `cat .ufo/waves/round-54/w1/E5CensusGate.md .ufo/l0-questions.md`; expected none — mass id drift, pending final L1 routing. Mistake selected-argv-laundering is counted once only, supported by the observed failing closed-route fixture. No new coverage or independent admission is inferred from documentation or receipt inspection.
