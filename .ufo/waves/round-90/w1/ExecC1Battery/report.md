# ExecC1Battery — R90-C1 control battery report

Seat: ExecC1Battery (executor, leaf). Measured revision for the counter: rev B `664435cfcb9419c4e8ac7828a55aec11a1f36ec4`; BASE `dcdd494ef4b4a6c0ae349ecb597527124ee54f91`. Counter: `plans/round90_c1_replay.py` (run from the clone, reads frozen inputs from git objects at `--rev`). Probe: `plans/round90_polydiff_probe.py` (bytes sha `2c4f0ab1…9be3` = TRUSTED_TOOL_SHA). Per-control lines: `controls.txt` (same directory). Raw outputs: `evidence/` (counter `.out`/`.err` per control, `summary.json`, driver `drive.py`, the positive probe receipt).

## Result

Every control's observed rc matches its expectation except one frozen-text mispredict (the C2 BASE line, below). No control that should fail passed. The positive probe smoke and the extra positive fixture both went green, so the counter can pass.

| Control | Expected | Observed | Note |
|---|---|---|---|
| 1 forged-tip (ledger unflipped) | rc1, L3-tip | rc1, `L3-tip` + L7 set | L3 is the expected leg; L7 also fires because the ledger is unflipped in this fixture |
| 1b forged-tip + ledger flipped | rc1, L3-tip | rc1, only `L3-tip` | isolates L3 |
| 2 ledger-only | rc1, L1-receipt | rc1, only `L1-receipt` | see finding F2 (L5/L6 absence defects are not produced) |
| 3 forged-probe (ledger unflipped) | rc1, L8-tool | rc1, `L8-tool` + L7 set | L1–L6 all pass on the forgery; L8 is the only catch |
| 3b forged-probe + ledger flipped | rc1, L8-tool | rc1, only `L8-tool` | isolates L8 |
| 4 positive probe smoke at B | rc0, 8 CASE observed==predicted, `cases=8 legs=40 mismatches=0` | rc0, exact | observation block pasted in `controls.txt` |
| 5a separation, pin files deleted from worktree | unchanged from B | rc1, byte-identical to B baseline | |
| 5b separation, pin files deleted in a commit | unchanged from B | rc1, identical after rev-hash strip | rev hash appears in the L1 detail line only |
| 5c C2 checker at B (C1 receipt absent, ledger unflipped) | rc0 pass | rc0, `PREDICATE R90-C2 pass` | |
| 5d C2 at the positive fixture (receipt + flip present) | (extra) rc0 pass | rc0 pass | C2 verdict unaffected by C1 receipt/flip |
| 6 do-nothing at BASE | rc1, `PREDICATE R90-C1 fail` | rc1, `PREDICATE R90-C1 fail` | TARGET + defects recorded verbatim in `controls.txt`; matches the BASE transcript modulo the rev hash |
| x positive C1 fixture (receipt at B + ledger flip) | (extra) rc0 pass | rc0, `PREDICATE R90-C1 pass`, `TARGET executed_rows=34 ... defects=0` | the counter can go green |
| x C2 at BASE | claims: rc1 `PIN-MISMATCH absent` | rc2 `DEFECT SETUP unreadable plans/counter-pins-r90.json`, `PREDICATE R90-C2 could-not-evaluate` | frozen mispredict, see F4; matches the rc2 in the BASE transcript |

### BASE do-nothing record (control 6, verbatim)

```
DEFECT L4-table plans/round90-cases.json absent at measured
DEFECT L8-tool plans/round90_polydiff_probe.py absent at dcdd494ef4b4
DEFECT L1-receipt corpus/evidence/round90/merge-diff-probe.txt absent at dcdd494ef4b4
DEFECT L7-ledger row {"classes": ["file-artifact", "git-plumbing", "serialization-schema", "stdout-inspection", "subprocess-exec"], "evidence": "no-blocker: tests/test_outputs.py sha256=2754ba6c5c5f75c9", "reason": "unattempted", "status": "unexecuted"}
DEFECT L7-ledger executed=33 members=88 != frozen 34 of 88
DEFECT L7-ledger cell git-plumbing 1 of 3 != frozen 2 of 3
DEFECT L7-ledger cell serialization-schema 3 of 10 != frozen 4 of 10
DEFECT L7-ledger cell file-artifact 24 of 76 != frozen 25 of 76
DEFECT L7-ledger cell stdout-inspection 9 of 29 != frozen 10 of 29
DEFECT L7-ledger cell subprocess-exec 11 of 45 != frozen 12 of 45
TARGET executed_rows=33 member=merge-diff-arc-agi-task located=1 executed=0 cases=0 legs=0 mismatches=0 defects=10
PREDICATE R90-C1 fail
rc=1
```

## Findings (frozen elements reported, not repaired)

- **F1 — TARGET `executed=` field ignores failing legs (counter defect, not a predicate defect).** In controls 2 and 3b the predicate correctly fails (`PREDICATE R90-C1 fail`, rc1), but the TARGET line still prints `executed=1`. The counter computes `executed` as `located and not any L7 defect`, so L1, L5, L6 and L8 failures do not reset it. Consequence: the TARGET line can say `executed=1` while the verdict is fail. The verdict itself is correct because it keys on the defect list. Not repaired; the frozen counter stays as pinned.
- **F2 — the ledger-only control's expected wording is not what the counter emits.** The control says "fail at L1-receipt (and L5/L6 absence defects)". L5 and L6 are gated on receipt presence by design, so with no receipt only `L1-receipt` fires. rc matches (1). The expectation wording is wrong; the counter is right.
- **F3 — do-nothing defect count mispredicted.** Claims predicted `defects=N` with N=5; measured N=10 (L4, L8, L1, one ledger-row defect, one executed-count defect, five cell defects). The BASE transcript also reads 10. Recorded as a mispredict.
- **F4 — C2 BASE mispredicted.** Claims predicted rc1 `PIN-MISMATCH absent`; measured rc2 `DEFECT SETUP unreadable plans/counter-pins-r90.json`, `PREDICATE R90-C2 could-not-evaluate`. This matches the rc2 SETUP the lead already recorded at BASE. The checker fails closed at setup before it reaches per-path absence checks, so the "PIN-MISMATCH absent" text in the frozen Before line is not what it prints.
- **F5 — by construction, L6 cannot catch a forged probe.** Control 3 shows L1–L6 all pass on a probe whose grader call echoes the predicted vectors, because the receipt and the re-run come from the same forged bytes. L8 (the TRUSTED_TOOL_SHA constant) is the sole catch, and that constant lives in the counter, which C2 pins externally. This confirms the round-88 hole closes only through the L8 + C2 pair and that the claim's honest limit (d) is load-bearing. Not a defect in the controls.

## Dead commands (rc and stderr tail)

- `drive.py` first run, control 4 (positive probe smoke): **rc 2**, stderr tail `python3: can't open file '/fast/scratch/hyaku/kengaku-r90/ExecC1Battery/plans/round90_polydiff_probe.py': [Errno 2] No such file or directory`. My driver passed the relative `PROBE` path instead of `L/PROBE`. The probe never ran. Re-run with the absolute path: rc 0, observation block recorded in `controls.txt`. The earlier direct run at B (same command, absolute path) was also rc 0. Not a lane issue.
- Control 6 extra (C2 at BASE): rc 2 `SETUP`. Expected for that revision, recorded as F4.

No other command returned non-zero.

## Installs / host

No tools installed, upgraded or removed. No host sysctl touched. `/usr/bin/bwrap` present and executed the probe sandbox normally; `/proc/sys/user/max_user_namespaces` read 122865 (not 0). No kernel-level need.

## Scratch, receipts, cleanup

- Clone: `$S/lane` (`git clone --no-hardlinks` from the fleet lane). `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane` (asserted before every write-ish step). The lane clone itself was never committed to.
- Fixtures: six `mktemp -d` clones under `$S` (tip, tip-ledger, ledger-only, probe, probe-ledger, positive, plus sep-worktree and sep-committed). Each asserted `rev-parse --show-toplevel` before commit; commits authored `t <t@t>`. Forged-probe fixtures were produced by `edit`-free script replacement of one line (asserted count==1), then the forged probe ran to produce its own receipt; both committed in one commit per fixture.
- Receipts and raw outputs copied into `.ufo/waves/round-90/w1/ExecC1Battery/evidence/` before deleting `$S`. Trap: `trap 'rm -rf -- "$S"' EXIT` set in the final cleanup call.
- Commit: none made in the lane. The per-control outputs are on disk in the wave dir for the lead to commit under `.ufo/waves/round-90/` before the measured tip is scored, as the claims require.

## For the main agent

Run after integration (not run by this seat): the same counter over the measured tip; `git diff --stat B tip -- plans/` must be empty; the positive counter at the tip must print `PREDICATE R90-C1 pass`. This seat did not run any gate at the tip.
