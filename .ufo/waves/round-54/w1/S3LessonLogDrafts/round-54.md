# Round 54 — externally anchored freeze and entry-truth calibration (DRAFT)

L1 KengakuR54; hyaku run 12. Axes: novelty and calibration. Frozen claims: `plans/round-54-claims.md`, stage-1 commit `17f90355c3ec17dcf15f7980d83f1943ae428fe5`; base `6c919180260ea545589c2c0a007a06f554b529d3`. Claims sha256: `d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8` (assignment provenance, not recomputed by this scribe). Draft only; no admission or score change asserted.

## Gate

Candidates/admissions/rejections remain pending. Source counts are not expansion credit. Every adopted row needs a fetched URL, access date, located quote of at most 25 words and bounded reason. C1 needs prior-art verdicts from at least two fetched public sources; published Bitcoin-anchored preregistration practice means replication/instrument-new, not an automatic novelty bump.

| category | rows / URL / location / access date / quote | decision and reason |
|---|---|---|
| candidates | TBD — command G below | TBD — command G; distinguish candidate material from admitted rows |
| admitted | TBD — command G below | TBD — command G; cite source-specific relevance and outside spot-check |
| rejected | TBD — command G below | TBD — command G; cite rejection reason and evidence that could change it |

Command G (receipt inspection, from lane root): `find .ufo/waves/round-54/w1 -type f \( -name '*gate*.md' -o -name '*rows*.md' -o -name '*fetch*.tsv' -o -name '*Sources*.md' -o -name '*PriorArt*.md' \) -print -exec cat {} \;`. Use the resulting fetched-source receipts and review decisions, not filenames alone, to fill each row. Keep proposals unadmitted until L1 integration/outside closure.

Existing-row status/recheck/used-by edits, old→new: TBD — command `git diff 17f90355c3ec17dcf15f7980d83f1943ae428fe5 -- corpus/SOURCES.md`; reconcile every change against Gate receipts. Census before is 190 rows per frozen claims; `claims/census-start.txt` records validation exit 0 and W04 duplicate-URL warnings. Census after: TBD — command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`; row/tier/status deltas: TBD — command `git diff 17f90355c3ec17dcf15f7980d83f1943ae428fe5 -- corpus/SOURCES.md` plus that census receipt. Commands here are fill instructions, not executions by this seat.

## Mistakes

| class | evidence pointer | captured-by | fix / measured limit |
|---|---|---|---|
| selected-argv-laundering | `.ufo/waves/round-53/w3/C2CritPredicate2.md`; `.ufo/waves/round-54/claims/c2-route-r53.txt` (red-before) | Q42/Q43 | `plans/round54_c2_entrytruth.py`. Red-before receipt: unmodified r53 counter accepts the selected-selftest fixture (`PREDICATE R53-C2 pass`, `ROUTE laundering demonstrated (r53 rc=0)`), although the fixture's entry exits 1 per receipt header/frozen claims. Count the mistake once, only because the fix is shown able to fail: `.ufo/waves/round-54/claims/c2-route-closed.txt` shows truthful fixture pass, then `LAUNDERED fixture-gate declared green, entry exit=1`, `PREDICATE R54-C2 fail`, `ROUTE closed=yes (truthful rc=0, laundering flagged=True)`. This bounded control is not a full-registry or outside-admission verdict. |

Environment control is separate supporting evidence, not a second count of this mistake: `claims/c2-env-poison.txt` reports inherited-env LEAKED and r54 hermetic-env BLOCKED. These are inspected existing receipts, not scribe reruns.

## Limits

Frozen predicates and kill rules remain binding. C1 pending-only proof is not Bitcoin confirmation; an OTS stamp alone is not the required header plus independent explorer receipts. Internal git pins are not an external witness. Any forged/pending proof passing, explorer disagreement or inability to confirm/verify is an honest stop, not permission to revise the target. C2 matching declared exits does not establish gate soundness or semantic correctness; surviving entry-laundering, failed environment discrimination or timeout kills the claim. Neither frozen r53 instruments nor SKILL.md may be changed to obtain a pass.

Coverage stays capped at 7 by the open round-25/33/51 L0 questions; no coverage move, exploratory claim or stagnation waiver. Nonclaimed-axis no-harm: TBD — command `find .ufo/waves/round-54/w1 -type f -iname '*noharm*' -print -exec cat {} \;`; do not infer clearance from absence. Outside novelty/calibration decisions: TBD — command `find .ufo/waves/round-54 -type f -iname '*verdict*' -print -exec cat {} \;`; only the canonical outside judgment can fill these decisions.

## Assimilation

TBD — expected **none — mass id drift**. Command `cat .ufo/waves/round-54/w1/E5CensusGate.md .ufo/waves/round-54/w1/E5CensusGate/collisions` supplies the inspected evidence: E5 reports 190 registry IDs, 175 staged IDs and 114 collisions and states verbatim, `MASS-ID-DRIFT: adoption closed this round; L0 question owed`. This is E5's report, not an independently rerun census. Final adoption/L0 routing remains TBD — command `cat .ufo/l0-questions.md` together with the L1's closing report; adopt nothing on the strength of a proposal. Any considerthese QUALITY criterion: TBD — command `git diff 17f90355c3ec17dcf15f7980d83f1943ae428fe5 -- corpus/QUALITY.md`; require citation of `considerthese/2026-10-26.md` and date before claiming assimilation.

## Measured close

- R54-C1: TBD — command `python3 plans/round54_c1_anchor.py verify --anchor corpus/evidence/round54/anchor --claims plans/round-54-claims.md --source "$CLEAN_CLONE" --work "$SCRATCH/c1" --controls`; retain revision, wall clock, all predicate legs and exit in `corpus/evidence/round54/c1-after.txt`.
- R54-C2: TBD — commands `python3 plans/round54_c2_entrytruth.py --lane . --source "$CLEAN_CLONE" --work "$SCRATCH/c2" --jobs 3 --timeout 900` and `python3 plans/round54_c2_entrytruth.py --lane . --dry`; retain entry counts, redeclarations, timeouts, mismatches, evidence misses, laundering and environment evidence.
- Wave shape: TBD — command `find .ufo/waves/round-54 -maxdepth 2 -type f \( -iname '*dispatch*' -o -iname '*results*' -o -iname '*policy*' \) -print -exec cat {} \;`. Frozen plan is one v2 build+attack wave of 64 seats, at least 25% attack roles; actual dispatched/settled counts and residual calls must come from dispatch/results, never the plan.

Measurement commands are for L1/authorized executors only: CLEAN_CLONE must be clean at landing tip; SCRATCH must be under the executing seat's `/fast/scratch/hyaku/kengaku-r54/` root. No command in this draft was run by the scribe.
