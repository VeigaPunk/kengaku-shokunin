# FxP3CBox4 — P3c PROVINCE adjacent pin

Round 26 attempt 1; advisory falsification. Axes: calibration (drift detection), specificity (append control), scope (P2 population stability).

## Method and commands

LSP unavailable: `read xd://lsp` returned “No such tool” and listed no LSP device. Grep was used only to locate the frozen constant; conclusions below are based on source reads and executed checks, not grep as semantic proof.

Exported base `f11bffbf9caa9c9e286fb32c568b81b97719656a` to `/tmp/kengaku-r26-p3cbox4-base`. First archive attempt omitted destination creation and failed: `tar: /tmp/kengaku-r26-p3cbox4-base: Cannot open: No such file or directory`; exit 2. Retry after `mkdir -p` with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive --format=tar f11bffbf9caa9c9e286fb32c568b81b97719656a | tar -x -C /tmp/kengaku-r26-p3cbox4-base` succeeded; exit 0. `cp -a /tmp/kengaku-r26-p3cbox4-base /tmp/kengaku-r26-p3cbox4-insertion && cp -a /tmp/kengaku-r26-p3cbox4-base /tmp/kengaku-r26-p3cbox4-append` succeeded; no output.

On insertion copy, inserted `<!-- P3cBox4 insertion fixture near line 119 -->` before PROVINCE.md:119. On control copy, appended `<!-- P3cBox4 append control -->` after the file's final line. No lane source or repository state was edited.

Commands used the integrated checker at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/state_check.py`:
- `python3 .../state_check.py --root /tmp/kengaku-r26-p3cbox4-base --summary` → exit 1; `assertions=275 match=266 mismatch=5 superseded=1 offline_unverifiable=3`. Five known base P3 mismatches; P2 has none.
- `python3 .../state_check.py --root /tmp/kengaku-r26-p3cbox4-base --json > /tmp/kengaku-r26-p3cbox4-base.json; rc=$?; printf 'base-json-exit=%s\n' "$rc"` → `base-json-exit=1`.
- `python3 .../state_check.py --root /tmp/kengaku-r26-p3cbox4-insertion --json > /tmp/kengaku-r26-p3cbox4-insertion.json; rc=$?; printf 'insertion-json-exit=%s\n' "$rc"` → `insertion-json-exit=1`.
- `python3 .../state_check.py --root /tmp/kengaku-r26-p3cbox4-append --json > /tmp/kengaku-r26-p3cbox4-append.json; rc=$?; printf 'append-json-exit=%s\n' "$rc"` → `append-json-exit=1`.
- `python3 .../state_check.py --selftest` → exit 0; printed `[selftest] ALL PASS`.

## Results

`state_check.py:218-227` freezes Box 4 as `PROVINCE.md:129` with target token `### Adjacent`; `:1443-1497` verifies the pointer and target-line token. In the base, P3c assertion `P3c.box.4.pointer.1` is MATCH (`target_line=129`, token hits 1).

Insertion at line 119 moves `### Adjacent` from line 129 to 130; line 129 is blank. `P3c.box.4.pointer.1` becomes MISMATCH (`token_hits=0`, observed target text empty); total mismatches rise 5→6. Thus the requested near-119 drift is caught.

Append control leaves `### Adjacent` at line 129; `P3c.box.4.pointer.1` remains MATCH (`token_hits=1`), and total mismatches remain 5. The overall CLI exit remains 1 only because the same five registered base P3 mismatches remain; the append control itself stays green.

Across base, insertion, and append JSON: P2 population is exactly 247 assertions each, with identical verdict counts: MATCH 231, OFFLINE_UNVERIFIABLE 3, OUT_OF_POPULATION 12, SUPERSEDED 1, MISMATCH 0. P2 population and results are preserved.

## Residual risk and verification gaps

The in-repo selftest's P3c red fixture targets Box 3 (`P3c.box.3.pointer.1`, `state_check.py:2026-2037`), not this Box-4 adjacent pin; Box 4 drift and append control were exercised in the requested scratch copies. No other P3 classes, C1 families, Q13 support, source claims, or admission entry were evaluated in this scoped seat. No tool installed or updated.

VERDICT: SCOPED PASS — P3c Box-4 insertion drift fails, append control matches, and the 247-assertion P2 population is unchanged; no concrete surviving defect found in this assigned behavior.