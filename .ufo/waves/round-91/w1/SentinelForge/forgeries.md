# SentinelForge — round 91 forgeries (scratch only)

Scratch: `S=/fast/scratch/hyaku/kengaku-r91/SentinelForge`. Lane clone `$S/lane` (`git clone --shared`) at `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0`. Every forged commit is a `git worktree add --detach` off that clone, committed with `git -c user.name=forge -c user.email=forge@invalid`; every worktree and fixture lives under `$S` and is removed on exit. Lane not mutated (`git status` clean at start; no commit, add, checkout or reset in the lane).

Counter entry points: the pinned tip copies `$S/lane/plans/round91_*.py` run against each forged revision (`--rev <forged>`), because the C1–C3 instruments are absent at BASE (added at commit B). Forged checkers (5a, 5b, 6) and the forged gate tree (3, 4) run from their own worktrees. Exit codes are the shell `$?` after the counter returned.

Toolchain: python 3.14.8, bwrap 0.13.1 at `/usr/bin/bwrap`, openssl 3.6.5. No tools installed or upgraded.

## Baselines (measured, rc in brackets)

- C1 at BASE `59764383` [rc=1]:
  `TARGET executed_rows=34 member=modernize-scientific-stack located=1 executed=0 cases=0 legs=0 mismatches=0 defects=9`, `DEFECT L1 receipt absent at revision …`, … , `PREDICATE R91-C1 fail`. Matches the predicted fail-closed class.
- C2 at BASE [rc=2]: `DEFECT SETUP unreadable plans/counter-pins-r91.json`, `PREDICATE R91-C2 could-not-evaluate`. Matches prediction.
- C1 at tip `a8de3e69` [rc=1] — **fails at the measured tip**:
  `TARGET executed_rows=35 member=modernize-scientific-stack located=1 executed=0 cases=10 legs=20 mismatches=10 defects=10`
  ten × `DEFECT L5 receipt names unknown case ?`, `PREDICATE R91-C1 fail`.
  Cause (read from source): `parse_receipt` (plans/round91_c1_replay.py) reads `parts.get("id")` from `CASE <id> predicted=…`; the id is the second token with no `id=` key, so every case parses as `?`. The receipt's own probe reports `mismatches=0 PREDICATE R91-PROBE pass`; C1 disagrees with its own receipt.
- C2 at tip `a8de3e69` [rc=0]: 16 × `PIN-OK <path>`, `SELFTEST cases=8 red-green-ok=8`, `PINS checked=16 matched=16 mismatched=0`, `PREDICATE R91-C2 pass`. Predicted K=16 (matches), C=6 (measured 8, mispredict).
- C3 at BASE `59764383` [rc=1]: `freeze=refused oldest_pending_round=82 pending=30 parked=7 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=34 checks_run=114 overrides=3`, `PREDICATE R91-C3 fail`.
- C3 at tip `a8de3e69` [rc=1]: identical lines. `corpus/routed-findings.jsonl` is byte-identical at BASE and tip (sha256 prefix `9079b8d3450c8627`, 213 lines), so the burn-down triage has not landed at tip. Predicted `freeze=admitted`; measured refused.
- C3 selftest `--selftest` [rc=0]: `SELFTEST cases=13 red-green-ok=13` (predicted 9; mispredict). None of the 13 cases covers supersede-closed-by-fiat or owner-roster validation.
- F1 counter at tip [rc=0]: `PARSED S260=1,S261=2,S265=1,S266=2`, `ANCHORLINE … live=0`, `WRONG-LINE-CAUGHT True`, `PREDICATE R91-F1 pass`.

## Forgery 1 — forged ledger row, receipt does not exist — HELD

Recipe 1a: worktree at BASE; copy the tip's `members["modernize-scientific-stack"]` entry into the BASE ledger (status executed, round 91, receipt `corpus/evidence/round91/modernize-probe.txt`). Receipt never created. Commit `6ec23d47`. Run:
`python3 $S/lane/plans/round91_c1_replay.py --lane $S/f1a --rev 6ec23d47ae7eeb6166df363d178b6fc6429e6b43 --work $S/out/f1a-work`

Output [rc=1]:
```
TARGET executed_rows=35 member=modernize-scientific-stack located=1 executed=0 cases=0 legs=0 mismatches=0 defects=9
DEFECT L1 receipt absent at revision: corpus/evidence/round91/modernize-probe.txt
DEFECT L2 subject sha mismatch (cap=0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977 receipt=absent)
DEFECT L3 LANE_TIP absent not an ancestor of 6ec23d47ae7e
DEFECT L4 case table not byte-identical to freeze commit (rev=absent A=89fab14b457364826065b77435626e0a16669abeebe67afe93ce6d2fe198ddf8)
DEFECT L5 case coverage 0 of 0
DEFECT L6 rerun rc=2 obs=0 want=0
DEFECT L7 ledger member=executed executed_total=35 cells_ok=True
DEFECT L8 probe pin unreadable vs bytes absent
DEFECT L9 stamp fields mismatch (tool=None table=None python=None openssl=None userns=None)
PREDICATE R91-C1 fail
```
Recipe 1b (tip minus receipt, ledger flip kept): `git rm corpus/evidence/round91/modernize-probe.txt`, commit `f7eba7eb`. Run as above [rc=1]: `DEFECT L1 receipt absent …`, `DEFECT L2 …`, `DEFECT L3 LANE_TIP absent …`, `DEFECT L5 case coverage 0 of 10`, `DEFECT L6 rerun rc=0 obs=10 want=0`, `DEFECT L9 …`, `PREDICATE R91-C1 fail`.

Verdict: **held** at L1 (1a and 1b both). Note: the ledger leg L7 accepts the flip by itself (`cells_ok=True`); only the receipt legs stop it.

## Forgery 2 — forged receipt, consistent stamp, fabricated observation block — HELD (at L6; masked by L5)

Recipe: tip's receipt kept byte-for-byte in its stamp block (`TOOL_SHA d70210cb…`, `CASE_TABLE_SHA 89fab14b…`, `HOST_PYTHON Python 3.14.8`, `HOST_OPENSSL OpenSSL 3.6.5 …`, `HOST_USERNS 122865`, `LANE_TIP b836a862…`). Every observation line rewritten to `observed=<predicted>` with `test_modernized_code_runs=ok,test_dependency_file_exists=ok` (all ten cases claim both pass). Commit `98eafa5d`. Run `python3 $S/lane/plans/round91_c1_replay.py --lane $S/f2 --rev 98eafa5dadfedbcf2da0f861e4a48c96faa098f5 --work $S/out/f2-work` [rc=1]:
```
TARGET executed_rows=35 member=modernize-scientific-stack located=1 executed=0 cases=10 legs=20 mismatches=10 defects=11
DEFECT L5 receipt names unknown case ?   (×10)
DEFECT L6 rerun rc=0 obs=10 want=10
PREDICATE R91-C1 fail
```
Verdict: **held**. L6 fires on the fabricated classes text (the re-run's observation lines differ from the forged block). Caveat: L5 fails on every receipt because of the `id=` parse defect above, so this rc=1 is not evidence that L5 caught the forgery; L6 is the leg that discriminates here. L1–L4, L7–L9 pass on the forged commit, so the stamp checks do not stop a copied stamp (by design; the observation re-run is the only discriminator).

## Forgery 3 — C3 supersede row closed by fiat, check `true`, one-sentence override_reason, against open R89-D2 (opened 89) — HOLE (admitted)

Recipe: append to `corpus/routed-findings.jsonl` (append-only; no R89 row edited):
`{"id":"F3-R89-D2-SUP","class":"control-name-drift","source":"corpus/lessons/round-89-verifier-spotcheck.md:111","opened_round":89,"status":"closed","supersedes":"R89-D2","close":"forged: resolved by fiat, no evidence located","check":"true","override_reason":"Forgery: the row is resolved by this one sentence alone."}`
Commit `49c98789`. R89-D2 has no base `check`, so the gate's override branch (which requires `override_reason`) is never entered; the forged `check` runs as an ordinary check.

Tree-level, forged commit [rc=1]: `freeze=refused oldest_pending_round=82 pending=29 parked=7 … resolutions=35 checks_run=115 overrides=3`; pending fell 30 → 29, and the other failures (R82-V8, three override-unjustified) keep the verdict refused.

Clean-room fixture (`--file`, 6 closed seeds 83–88 plus the R89-D2 row) —
control (no forgery) [rc=1]: `ROWS total=7 valid=7 invalid=0 superseded=0`, `freeze=refused oldest_pending_round=89 pending=1 parked=0 …`, `PREDICATE R91-C3 fail`.
forged [rc=0]: `ROWS total=8 valid=8 invalid=0 superseded=1`, `freeze=admitted oldest_pending_round=- pending=0 parked=0 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=7 resolutions=1 checks_run=1 overrides=0`, `PREDICATE R91-C3 pass`.

Verdict: **admitted by the counter (hole)**. A row closed by a bare `true` with a one-sentence reason flips `freeze=refused` to `freeze=admitted`. The `override_reason` is never read because the override branch requires a base check. The `close` string is free text; no located evidence is required.

## Forgery 4 — C3 blocked row, owner `x` naming nothing — HOLE (admitted)

Recipe: append `{"id":"F4-R89-D3-BLK","class":"before-count-two-ways","source":"corpus/lessons/round-89-verifier-spotcheck.md:112","opened_round":89,"status":"blocked","supersedes":"R89-D3","blocker":"held upstream, no named holder","owner":"x"}`. Commit `b780088f`.

Tree-level [rc=1]: `… pending=29 parked=8 unowned_blocked=0 …`; parked rose 7 → 8, the owner check passes.

Clean-room fixture (6 seeds + R89-D3 open): control [rc=1] `freeze=refused oldest_pending_round=89 pending=1 parked=0 …`; forged [rc=0] `freeze=admitted oldest_pending_round=- pending=0 parked=1 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=7 resolutions=1 checks_run=0 overrides=0`, `PREDICATE R91-C3 pass`.

Verdict: **admitted by the counter (hole)**. The gate requires only a non-empty `owner`; it does not check it names a lane or seat (the claim says "naming the lane or seat that holds the fix").

## Forgery 5 — one-commit rewrite of plans/round91_counter_pin.py AND plans/counter-pins-r91.json — 5a HELD, 5b HOLE

5a (blatant): `check_pins` returns `[], checked, checked` (every pin defect silenced); checker's own pin entry updated to the new bytes; one commit `7fb599d1`. Run `python3 $S/f5a/plans/round91_counter_pin.py --lane $S/f5a --rev 7fb599d1852a4865059480b2dc29c41686af6b6f --work $S/out/f5a-work` [rc=1]:
```
SELFTEST counter-byte-mutated rc=0 want=1 defect-ok=False ok=False
SELFTEST path-absent rc=0 want=1 defect-ok=False ok=False
SELFTEST tampered-pin rc=0 want=1 defect-ok=False ok=False
SELFTEST blob-mutated rc=0 want=1 defect-ok=False ok=False
SELFTEST self-pin-mismatch rc=0 want=1 defect-ok=False ok=False
SELFTEST blob-anchor-missing rc=0 want=1 defect-ok=False ok=False
SELFTEST-DETAIL cases=8 red-green-ok=2
SELFTEST cases=8 red-green-ok=0
PREDICATE R91-C2 fail
```
Verdict: **held** by the in-path selftest (M5 closed). Every red case turns green; the predicate fails.

5b (sharp): the checker skips the probe pin while counting it matched (`if path == "plans/round91_modernize_probe.py": matched += 1; continue`); checker's own pin updated; `plans/counter-pins-r91.json` rewritten in the same commit. Commit `77b785af`. Run `python3 $S/f5b/plans/round91_counter_pin.py --lane $S/f5b --rev 77b785af2f841b139f6e07c49aa06bfbf13b18f6 --work $S/out/f5b-work` [rc=0]:
```
SELFTEST-DETAIL cases=8 red-green-ok=8
SELFTEST cases=8 red-green-ok=8
PINS checked=16 matched=16 mismatched=0
PREDICATE R91-C2 pass
```
Verdict: **C2 passes — yes, the forged commit passes (rc 0, `PREDICATE R91-C2 pass`)**. The selftest battery does not exercise the skipped entry, and the checker's self-pin is updated in the same commit. This is the residual the claim discloses ("one commit rewriting the checker and its pin entry together"), so it is a known residual, not a new class; it remains a hole.

## Forgery 6 — anchor_line_check.py edited only — HELD

Recipe: the line check in `row_defects` replaced by `if False:` (one-line edit); no pin update; commit `4ede0191`. Run `python3 $S/f6/plans/round91_counter_pin.py --lane $S/f6 --rev 4ede01917fb08fa40991962a001b911c9a3d1436 --work $S/out/f6-work` [rc=1]:
```
DEFECT PIN-MISMATCH bytes plans/anchor_line_check.py
PINS checked=16 matched=15 mismatched=1
PREDICATE R91-C2 fail
```
Verdict: **held**. C2 fails and names `plans/anchor_line_check.py` as the mismatched entry; the selftest stays green (8/8), so the pin is the sole discriminator here.

## Forgery 7 — F1 wrong-line curly-quote through the production checker — HELD

Recipe: fixture repo `D=$(mktemp -d -p "$S")`, `git -C "$D" init -q`, toplevel asserted equal to `$D`. Capture `corpus/evidence/fixture/notes.md` = `# notes`, `first line`, `second line`, tracked and committed. `corpus/SOURCES.md` rows:
- `S991`: anchor `notes.md:3 quote “first line” (2 words); sha256 <digest>` (curly quotes, cites line 3; quote sits on line 2) — the forgery.
- `S992`: `:2 quote “first line”` (curly, right line) — positive control.
- `S993`: `:3 "first line" (2 words)` (straight, wrong line) — second wrong-line control.

Run `python3 $S/lane/plans/anchor_line_check.py --lane $D --verbose` [rc=1]:
```
ROW S991 state=live defects=line:1 capture=corpus/evidence/fixture/notes.md
ROW S993 state=live defects=line:1 capture=corpus/evidence/fixture/notes.md
ANCHORLINE rows=3 cited=3 captured=3 uncaptured=0 defective=2 repaired=0 live=2 cells=2
```
S992 is clean. Direct `row_defects` on all three rows: `S991 (True, …, ['line'])`, `S992 (True, …, [])`, `S993 (True, …, ['line'])`.

Verdict: **held**. The production checker catches the curly-quoted wrong-line row. F1's own wrong-line control (`round91_f1_counter.py`, step 3) calls `row_defects` directly rather than the CLI; the CLI path was exercised here separately and also catches it.

## Diagnostics (not forgeries; recorded for the integrator)

- D1 C1 L9 crash: with `openssl` absent from PATH, `round91_c1_replay.py` raises an uncaught `FileNotFoundError` at line 243 (`subprocess.run(["openssl","version"])` is unguarded) and exits 1 with no `PREDICATE` line; the frozen contract is exit 2 `could-not-evaluate`. Output tail: `FileNotFoundError: [Errno 2] No such file or directory: 'openssl'`, `rc=1`.
- D2 C3 predicate does not run the selftest: `main` calls `selftest()` only under `--selftest`; the default run that prints `PREDICATE R91-C3` never executes the 13-case battery. The claim's predicate names the selftest battery; the C2 path (in-path selftest) was the M5 fix that C3 did not carry.
- D3 C3 check results come from the working tree at `--lane`, not from `--rev` (`run_check` uses `cwd=lane_root`). The BASE-worktree run (`--lane $S/bx --rev 59764383…`) printed the same 114 checks and the same R82-V8 failure as tip; the do-nothing control therefore does not measure BASE checks unless `--lane` is at BASE.
- D4 C1 `parse_receipt` id defect (see Baselines): C1 cannot pass against the receipt format as written.
- D5 C3 `--file` route ignores `--rev` by design (fixture route); used here only for the clean-room controls.

## Summary

| # | forgery | rc | verdict |
|---|---|---|---|
| 1a | ledger flip, receipt absent (from BASE) | 1 | held (L1) |
| 1b | ledger flip, receipt removed at tip | 1 | held (L1) |
| 2 | forged receipt, copied stamp, fabricated observations | 1 | held (L6; L5 masked) |
| 3 | supersede closed by `true` + one-sentence reason vs R89-D2 | 0 (fixture) | **admitted — hole** |
| 4 | blocked, owner `x`, vs R89-D3 | 0 (fixture) | **admitted — hole** |
| 5a | checker silences pin defects + pin rewrite | 1 | held (selftest) |
| 5b | checker skips probe pin + pin rewrite, one commit | 0 | **C2 passes: yes — hole (disclosed residual)** |
| 6 | anchor_line_check.py edited, no pin | 1 | held (`PIN-MISMATCH bytes plans/anchor_line_check.py`) |
| 7 | curly-quote wrong-line via production CLI | 1 | held (S991 `line:1`) |
