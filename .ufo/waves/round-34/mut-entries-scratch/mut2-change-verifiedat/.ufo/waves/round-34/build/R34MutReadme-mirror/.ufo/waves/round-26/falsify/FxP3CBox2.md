# FxP3CBox2 — P3c `LOG.md:7` pointer mutation

## Scope and setup
- Tested the recorded integration revision `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` from `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26/integration-revision.txt`.
- Scratch allocated by `mktemp -d /tmp/kengaku-r26-fxp3c.XXXXXX` → `/tmp/kengaku-r26-fxp3c.5tPIAx`. Export command: `set -o pipefail && mkdir /tmp/kengaku-r26-fxp3c.5tPIAx/tree && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive --format=tar 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 | tar -xf - -C /tmp/kengaku-r26-fxp3c.5tPIAx/tree && cp /home/vgpnk/Projects/shokunin/PROTOCOL.md /tmp/kengaku-r26-fxp3c.5tPIAx/PROTOCOL.md && printf 'exported=%s\n' /tmp/kengaku-r26-fxp3c.5tPIAx/tree`; output `exported=/tmp/kengaku-r26-fxp3c.5tPIAx/tree` (exit 0). No lane source files changed (aside from this assigned report).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/state_check.py:218-226` freezes box 2 as `LOG.md:7` and token `round 4: executed first authored eval`. Lines `:1443-1497` check the actual pointer, unique occurrence, and target-line token.
- LSP unavailable: `xd://lsp` returned `No such tool`; no semantic caller/definition/diagnostics proof is claimed.

## Mutation and results
- Untouched command: `python3 /tmp/kengaku-r26-fxp3c.5tPIAx/tree/plans/state_check.py --root /tmp/kengaku-r26-fxp3c.5tPIAx/tree --json > /tmp/kengaku-r26-fxp3c.5tPIAx/baseline.json`; exit **1**. Summary: `assertions=275 match=267 mismatch=2 superseded=3 offline_unverifiable=3 out_of_population=17`. `P3c.box.2.pointer.1` was **MATCH** (`pointer=LOG.md:7`, `pointer_count=1`, `target_line=7`, `token_hits=1`).
- In `/tmp/kengaku-r26-fxp3c.5tPIAx/tree/SHONEN.md` only, changed line 8 from `LOG.md:7` to `LOG.md:8`. `/tmp/kengaku-r26-fxp3c.5tPIAx/tree/LOG.md:8` exists, so this is a different in-range line; no lane file was modified.
- Mutated command: `python3 /tmp/kengaku-r26-fxp3c.5tPIAx/tree/plans/state_check.py --root /tmp/kengaku-r26-fxp3c.5tPIAx/tree --json > /tmp/kengaku-r26-fxp3c.5tPIAx/mutated.json`; exit **1**. Summary: `assertions=275 match=266 mismatch=3 superseded=3 offline_unverifiable=3 out_of_population=17`.
- New mismatch: `P3c.box.2.pointer.1` (`pointer=LOG.md:8`, `pointer_count=0`, pinned `target_line=7`, target token still occurs once). Thus the wrong in-range relocation is rejected at the frozen P3c assertion.

## P2 population and residual
- P2 ID extraction commands (each exit 0):
  `jq -c '[.assertions[] | select(.id | startswith("P2")) | .id] | sort' /tmp/kengaku-r26-fxp3c.5tPIAx/baseline.json > /tmp/kengaku-r26-fxp3c.5tPIAx/baseline-p2ids.json`
  `jq -c '[.assertions[] | select(.id | startswith("P2")) | .id] | sort' /tmp/kengaku-r26-fxp3c.5tPIAx/mutated.json > /tmp/kengaku-r26-fxp3c.5tPIAx/mutated-p2ids.json`
- `cmp -s /tmp/kengaku-r26-fxp3c.5tPIAx/baseline-p2ids.json /tmp/kengaku-r26-fxp3c.5tPIAx/mutated-p2ids.json`; exit **0**. Both contain **252** IDs; SHA-256 of the sorted ID JSON is `f3d50f381c3e99c25353ee65af4d0d64c45e26ddb3dc110d9ded09b8dde22e9e`. `P2c.box.2.pointer.1` remains MATCH. P2 population is unchanged.
- The untouched run already exited 1 on two unrelated P3b assertions: `P3b.province.public-literature-registry.rows` and `P3b.province.round25-correction.rows` (claims 25 and 37 in `/tmp/kengaku-r26-fxp3c.5tPIAx/tree/PROVINCE.md` versus the 42-row exact census in `/tmp/kengaku-r26-fxp3c.5tPIAx/tree/corpus/SOURCES.md`; correction tokens contain `rows=42` only). Therefore this mutation did not create the process-level failure transition; it increased mismatches from 2 to 3 and added the P3c failure above. P3b remains outside this scoped attack.

VERDICT: P3c scoped pass — the in-range pointer relocation is caught, and P2 assertion-ID population is preserved; the integration tree still has the two pre-existing P3b mismatches.