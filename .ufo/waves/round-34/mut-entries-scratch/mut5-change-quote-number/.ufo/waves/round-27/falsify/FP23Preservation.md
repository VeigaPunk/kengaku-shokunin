# Round 27 P2/P3 preservation falsification

Reviewer: `KengakuR27.FP23Preservation` (not candidate writer `KengakuR27`). Scope: full keyed P2/P3 record and order preservation only.

## Evidence

- Candidate scratch clone HEAD observed: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`. Base lane tree was exported with `git archive b5719440e5eee46c1886fddbdf7bdc1624829454`. Old checker: base-export `plans/state_check.py`, SHA-256 `32a684ffcb3fb222b0360333f83c2e4654c19ec1c3ad6ed47016052401428089`. New checker: candidate `plans/state_check.py`, SHA-256 `29c5d716a53e77bf4a82d2155775dda3e94385e058b4700af54cb3a23d031f32`.
- The exported root was `/tmp/kengaku-r27-FP23Preservation-fleet/kengaku-shokunin`, with the fleet `PROTOCOL.md` beside it; its observed SHA-256 was `886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a`, matching the preregistration's recorded frozen prefix `886e459b`.
- Command (cwd `/tmp/kengaku-r27-FP23Preservation`): `python3 plans/fixtures/r27/p23_preservation.py --old /tmp/kengaku-r27-FP23Preservation-fleet/kengaku-shokunin/plans/state_check.py --new plans/state_check.py --root /tmp/kengaku-r27-FP23Preservation-fleet/kengaku-shokunin` — exit **0**.
- Output: old exit=0, P2=255, P3=43, summary `assertions=278 match=270 mismatch=0 offline_unverifiable=3 out_of_population=20 superseded=5`; new exit=0, P2=255, P3=43, summary `assertions=327 match=318 mismatch=0 offline_unverifiable=3 out_of_population=20 superseded=6`; `compared: ids=298 record_pairs=298 differences=0 order=same`; `VERDICT: IDENTICAL - 298 old and 298 new P2/P3 records match on every field, in the same order`.
- Coverage: `plans/fixtures/r27/p23_preservation.py:5-9,74,78-86,117-127` selects every P2/P3-prefixed record (without filtering verdict), serializes full records, keys repeated IDs by occurrence, and compares sequence order. Thus `OUT_OF_POPULATION` records are included; each run reports 20. The run found no changed P2/P3 fields, counts, IDs, or order.

## Setup correction / verification limits

An initial comparison using the old checker copied to a standalone `/tmp/...old-state_check.py` showed a P2c.seed source-line difference (`canonical_seed_start_line` 441 vs 3; exit 1). That was not a valid comparison: the old checker resolves `SEED_FIXTURE` relative to `__file__` (`base plans/state_check.py:199`, fixture-first selection at `:2515-2524`), so moving the script detached it from its fixture. The final command above uses the old checker at its archived path and resolves the same fixture as the candidate; do not count the standalone-path difference as a code finding.

LSP unavailability: `read xd://lsp` returned `No such tool: xd://lsp` (not mounted). A text search was used only to locate source lines; semantic conclusion rests on the preservation check output and the wrapper's record-comparison implementation, not grep output. No build, lint, or unrelated checks were run.

Installs: none.

VERDICT: PASS — the frozen base checker and candidate state_check.py preserve all 298 full P2/P3 records, including OUT_OF_POPULATION, in identical order on the exported base tree.