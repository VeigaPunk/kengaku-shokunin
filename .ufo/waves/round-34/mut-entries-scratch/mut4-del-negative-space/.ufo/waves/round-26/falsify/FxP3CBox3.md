# FxP3CBox3 — P3c cold-run heading pin

Scope: P3c `SHONEN.md` box-3 evidence pointer to `round-8-aggregator-box3-coldrun.md:48`; integration snapshot `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`. All mutation work was in `/tmp/kengaku-r26-fxp3cbox3.6n6975`, never the lane.

## Findings (severity order)

None in the assigned P3c check. The checker detects a stale line-48 heading pointer after the heading moves.

## Evidence

- `read xd://lsp` returned `No such tool`; no LSP status/references/definition/diagnostics were available. Literal search located the code anchors only; conclusions below come from direct source reads and the controlled run.
- `plans/state_check.py:218-225` freezes `P3c` box 3 to the pointer `...coldrun.md:48` and token `## Box-3 verdict`; `:1443-1497` checks the pointer and token on that exact line. Selftest `:2026-2037` mutates the token and asserts `P3c.box.3.pointer.1` becomes `MISMATCH`.
- Export: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive --format=tar 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 | tar -xf - -C /tmp/kengaku-r26-fxp3cbox3.6n6975`; exit 0.
- Baseline `python3 /tmp/kengaku-r26-fxp3cbox3.6n6975/plans/state_check.py --root /tmp/kengaku-r26-fxp3cbox3.6n6975 --summary`: exit 1 overall, 275 assertions; P3c box 3 was `MATCH` (`target_text="## Box-3 verdict"`, `token_hits=1`). The two existing mismatches were P3b rows `:112` and `:119`, outside this attack.
- Baseline `python3 /tmp/kengaku-r26-fxp3cbox3.6n6975/plans/state_check.py --root /tmp/kengaku-r26-fxp3cbox3.6n6975 --selftest`: exit 0; output included `selftest ok   P3c: red mutation (P3c.box.3.pointer.1)` and `[selftest] ALL PASS`.
- Scratch-only mutation inserted one line before the heading, moving it from line 48 to 49. `python3 /tmp/kengaku-r26-fxp3cbox3.6n6975/plans/state_check.py --root /tmp/kengaku-r26-fxp3cbox3.6n6975 --json`: exit 1 overall; `P3c.box.3.pointer.1` changed to `MISMATCH`, with line 48 `Moved heading in scratch only.` and `token_hits=0`.
- P2 population/status stayed fixed: both JSON snapshots contain 252 `P2*` assertions. SHA-256 of the jq projection `[[id, verdict], ...]` was `fa55d886907a5b6fb8b1770d1b9f045ca41de739f9fc56e9e4f7e8fcdbeb5abe` in both. `P2c.box.3.pointer.1` remains `MATCH`; its observed target length changes 118→119 because the test inserted one line.
- P2 comparison: `jq -c '[.assertions[] | select(.id | startswith("P2")) | [.id,.verdict]]' baseline.json | sha256sum` and the same command with `heading-shift.json`; both completed 0 and emitted the digest above. The matching `jq -r '[.assertions[] | select(.id | startswith("P2"))] | length'` counts were 252/252.

## Residual risk and verification gaps

This is a historical heading/pointer pin, not a replay of the historical verdict or proof of current executability: the check validates the frozen token at line 48, not the old commands’ present behavior. No current execution of those historical commands was attempted. The overall baseline still has the two noted P3b mismatches; those are outside this seat’s scope. No tools installed.

VERDICT: SURVIVES — P3c correctly fails when the cold-run heading shifts off its frozen target line; P2 assertion population/status is unchanged.