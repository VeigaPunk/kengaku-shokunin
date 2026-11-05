# SentinelForge — round 91 (adversarial forgeries, scratch clones only)

Full forgery log with recipes, commands, rc and output lines: `.ufo/waves/round-91/w1/SentinelForge/forgeries.md`. Lane tip measured: `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0`. BASE `59764383d4dd33d58faa50daad4c06d0cde410aa`. Scratch deleted at exit; lane not mutated.

## Measured verdicts at tip (pinned tip counters, `--rev a8de3e69`)

| claim | command | rc | predicate line |
|---|---|---|---|
| R91-C1 | `python3 plans/round91_c1_replay.py --lane <lane> --rev a8de3e69 --work <S>` | 1 | `PREDICATE R91-C1 fail` (`executed=0`, ten L5 defects) |
| R91-C2 | `python3 plans/round91_counter_pin.py --lane <lane> --rev a8de3e69 --work <S>` | 0 | `PREDICATE R91-C2 pass` (16/16 pins, selftest 8/8) |
| R91-C3 | `python3 plans/round91_burndown.py --lane <lane> --rev a8de3e69 --work <S> --freeze-round 92` | 1 | `freeze=refused … pending=30` `PREDICATE R91-C3 fail` |
| R91-F1 | `python3 plans/round91_f1_counter.py --lane <lane> --work <S>` | 0 | `PREDICATE R91-F1 pass` |
| C3 selftest | `python3 plans/round91_burndown.py --lane <lane> --work <S> --selftest` | 0 | `SELFTEST cases=13 red-green-ok=13` |
| do-nothing C1 | same as C1 at `59764383` | 1 | `PREDICATE R91-C1 fail` (matches prediction class) |
| do-nothing C2 | same as C2 at `59764383` | 2 | `DEFECT SETUP unreadable plans/counter-pins-r91.json`, could-not-evaluate (matches) |
| do-nothing C3 | same as C3 at `59764383` | 1 | identical to tip output (see D3) |

Two of three frozen claims do not pass at the measured tip. R91-C1 fails at tip because the counter cannot parse its own receipt (finding F1). R91-C3 is refused at tip because the triage never landed (finding F2).

## Forgery verdicts

| # | forgery | rc | verdict |
|---|---|---|---|
| 1a | ledger member flipped to executed, receipt never created (from BASE) | 1 | held at L1 |
| 1b | ledger flip kept, receipt removed at tip | 1 | held at L1 |
| 2 | receipt with copied stamp (TOOL_SHA, CASE_TABLE_SHA, HOST_*) and fabricated observations | 1 | held at L6 (L5 also fails for every receipt, so it does not isolate L6) |
| 3 | C3 supersede of open R89-D2 (opened 89): closed, `check:"true"`, one-sentence override_reason | 0 (clean-room fixture) | **admitted, hole** |
| 4 | C3 supersede of open R89-D3: blocked, `owner:"x"` | 0 (clean-room fixture) | **admitted, hole** |
| 5a | checker silences pin defects, checker pin rewritten in one commit | 1 | held by the in-path selftest (red-green-ok=0) |
| 5b | checker skips the probe pin while counting it matched; checker and pin ledger rewritten in one commit | 0 | **C2 passes: yes, hole (the disclosed residual)** |
| 6 | `plans/anchor_line_check.py` edited only | 1 | held: `DEFECT PIN-MISMATCH bytes plans/anchor_line_check.py` |
| 7 | curly-quoted anchor, cites line 3, quote on line 2, via production CLI | 1 | held: `ROW S991 state=live defects=line:1` |

## Findings (ranked)

**F1 — R91-C1 fails at tip; the counter cannot read its own receipt (coverage, blocking).** `parse_receipt` in `plans/round91_c1_replay.py` reads `parts.get("id")` from `CASE <id> predicted=…` lines. The id is the second token with no `id=` key, so all ten cases parse as `?`, every case becomes an L5 `unknown case ?` defect, and the TARGET line prints `executed=0`. The receipt's own probe prints `mismatches=0 PREDICATE R91-PROBE pass`, so the receipt and the counter disagree. Under the frozen predicate this claim cannot pass at any receipt written in the current format. Per the frozen rule, reported, not repaired.

**F2 — R91-C3 freeze refused at tip; triage has not landed (operability, blocking).** `corpus/routed-findings.jsonl` is byte-identical at BASE and tip (213 lines, sha256 prefix `9079b8d3450c8627`). The tip gate prints `freeze=refused oldest_pending_round=82 pending=30 parked=7`, `check-failed R82-V8`, and three `override-unjustified` rows. The predicted `freeze=admitted` is a mispredict at tip.

**F3 — C3 admits a row closed by fiat (hole, forgery 3).** A supersede row with `status:"closed"` and `check:"true"` is admitted with no evidence check. The override branch that requires `override_reason` is entered only when the base row carries a `check` that differs from the override's. An open row with no base `check` therefore takes the ordinary check path, and `override_reason` is never read. Clean-room control: `freeze=refused` without the row, `freeze=admitted` with it. The `close` string is free text. Kill-rule relevance: a closed row whose work is absent is the claim's named fabrication-class defect, and the gate does not detect it.

**F4 — C3 admits a blocked row whose owner names nothing (hole, forgery 4).** The gate requires only a non-empty `owner` string. `owner:"x"` clears `unowned_blocked`. Clean-room control: `freeze=refused` without the row, `freeze=admitted` with it. The claim's owner requirement ("naming the lane or seat that holds the fix") has no roster check.

**F5 — C2 passes a one-commit checker-plus-pin rewrite that skips a pinned entry (hole, forgery 5b; disclosed residual).** Yes: the forged commit exits 0 with `PREDICATE R91-C2 pass`. The checker skips the probe pin while counting it matched, and the self-pin is rewritten in the same commit. The in-path selftest does not exercise the skipped path. This is the residual the claim discloses (checker and pin entry rewritten together), so it is not new, but it is still open. The blatant version (5a) is caught by the selftest, so the selftest does discriminate against silenced verdicts. Forgery 6 is held by the pin: a single edit to `anchor_line_check.py` without a pin update fails with `PIN-MISMATCH bytes plans/anchor_line_check.py`.

**F6 — C1 L9 crashes instead of exiting 2 when `openssl` is absent (operability, diagnostic).** `plans/round91_c1_replay.py` line 243 calls `subprocess.run(["openssl","version"])` without a `FileNotFoundError` guard. With openssl off PATH the counter dies with an uncaught traceback, exit 1, no `PREDICATE` line. The frozen contract is `could-not-evaluate` with exit 2. Fail-closed on the exit code, but not the frozen contract.

**F7 — C3's default predicate never runs the selftest (operability, predicate gap).** `main` runs `selftest()` only under `--selftest`. The default run that prints `PREDICATE R91-C3` does not execute the 13-case battery. The claim's predicate names the battery as a clause, so the predicate is not computed as written. This is the M5 class that C2 closed in-path and C3 did not carry. The C3 selftest has no case for forgery 3 or 4.

**F8 — C3 check results read the working tree, not `--rev` (operability, do-nothing control).** `run_check` runs each command with `cwd=lane_root`. The do-nothing control at BASE therefore measures the checks against whatever is checked out at `--lane`. The BASE-worktree run printed the same 114 checks and the same R82-V8 failure as tip. This is not disproved here (the BASE and tip ledgers are identical), but the control does not measure BASE checks unless `--lane` is at BASE.

**F9 — C1 and C2 frozen predictions (calibration mispredicts, recorded not repaired).**
- C1 predicted `executed=1` at tip. Measured `executed=0` (F1).
- C2 predicted C=6 selftest cases. Measured 8. K=16 matched the prediction.
- C3 predicted `freeze=admitted`, `SELFTEST cases=9`. Measured `freeze=refused` (F2) and 13 cases (F7's battery).
- F1 wrong-line control: the frozen control calls `row_defects` directly rather than the CLI. The production CLI (`plans/anchor_line_check.py --lane`) also catches the curly-quoted wrong-line row (forgery 7 held), so the claim holds through production. The control's coverage gap is that the CLI route is untested by the counter itself.

## Scope and limits

- No subagents spawned. No commits, pushes or mutating git in the lane. All forged commits, fixtures and worktrees under `$S`, removed at exit.
- Tooling: no installs, upgrades or host changes. `/usr/bin/bwrap` and `openssl` were used read-only as shipped.
- The counters at BASE do not exist (instruments added at commit B). Every BASE control ran the tip counter against `--rev 59764383…`.
- Forgery 2 rc=1 is not evidence of L6 in isolation, because L5 fails for every receipt (F1). The discriminating leg is L6, shown by its `rerun rc=0 obs=10 want=10` line.
- Forgeries 3 and 4 were judged on clean-room fixtures because the tip gate is already refused for unrelated reasons (F2). Tree-level forged-commit runs are in the log.

## Coordination

Integrator (`KengakuR91`) was messaged the headline (F1, F2, F3, F4) at the start of the write-up.
