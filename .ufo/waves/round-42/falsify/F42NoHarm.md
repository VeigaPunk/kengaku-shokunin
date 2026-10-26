# F42NoHarm — no-harm re-measurement at the docs tip (wave 2, falsify)

Seat: executor, leaf. Assignment: run `integrate/measure.sh`'s command list myself on a clean clone of
`508434ad55c709337065611691c426f05875492d` inside the ruled envelope (home-writable cache), diff every verdict
line against `integrate/measure-final.txt`, and confirm `build/R42ExecNoHarm.md`'s baseline agrees with
`integrate/measure-baseline.txt`.

What I attacked: the landing's no-harm claim itself, i.e. whether the 30-command set the L1 froze really emits the
same pass/fail statements at the docs tip as at `ff14d76`, and whether wave 1's "24 green of 24" is a report on the
same instrument set. No lane file was written, no `git`/`jj` mutation was issued in the lane, nothing was installed.

## Envelope, verbatim (Q32)

Both runs, wrapping the entire command list (the counters build their own read-only sandboxes inside it — nesting works):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --bind /fast/scratch/hyaku/kengaku-r42/F42NoHarm/home-cache /home/vgpnk/.cache \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent  bash <driver>.sh
```

`$HOME`/`$TMPDIR` are set *inside* the driver to `$S/home` / `$S/tmp`, so instrument writes land in my scratch; only
`.cache` is bound writable, which is what the C2 legs' `uv` needs (the round-42 L1 mistake: whole-`/home` `--ro-bind`).

| run | window | `ls -A ~/.local/bin \| sha256sum` before → after | files | new entries | driver exit | log |
|---|---|---|---|---|---|---|
| run-1, literal `measure.sh` checkout (`git checkout -q <tip>`) | 18:05:07→18:13:19, 492 s | `8cf5b151…d86d52` → `8cf5b151…d86d52` | 102 → 102 | 2 (dir + `omp`, see F4) | 0 | 952 lines, sha256 `e865ba75…f322` |
| run-2, master pinned to the measured commit (primary) | 18:14:14→18:22:21, 487 s | `8cf5b151…d86d52` → `8cf5b151…d86d52` | 102 → 102 | 0 | 0 | 936 lines, sha256 `9f77d809…7bb0` |

Same listing hash in all four readings above and in run-1↔run-2; no PATH entry appeared, vanished or was renamed by
either run. Drivers: `driver.sh` sha256 `05500580…cdce7`, `driver2.sh` sha256 `f84f8057…604d`, verdict extractor
`verdicts.py` sha256 `312b0901…2ff2`; `receipts.txt` `8a3aa19f…1ead`, `receipts2.txt` `7b2d8a1c…1dfd`. Every one of
these, with both full logs (87 KB / 86 KB) and both tier-1 extracts, is kept beside this report in
`.ufo/waves/round-42/falsify/F42NoHarm/` (264 KB total) under the shas just given; no receipt file exceeds 1 MiB. Clone assertions `git -C "$S/lane" rev-parse --show-toplevel` = `"$S/lane"` ran in both drivers;
`untracked_in_clone=0` in both.

## Result: the landing's verdict lines reproduce exactly at the docs tip

Run-2 normalises scratch roots, the three pinned-commit hexes and my own `BRANCH` echo, then compares whole logs:

```
$ diff verdicts.py(measure-final, --all) verdicts.py(run-2.log, --all)   → no output
FULL-LOG-IDENTICAL            (935 normalised lines each)
$ diff measure-final.t1.txt run-2.t1.txt                                 → no output
TIER1-IDENTICAL               277 of 277 tier-1 verdict lines identical
```

Tier-1 = every line that states a verdict or count: `exit=`, `PREDICATE`, `BATTERY`, `MUTANTS`, `MUTANTS-BY-TOOL`,
`ADVERTISED`, `PINS total=PINS-AFTER`, `checks=`, `gate: Pn`/`gate: defects=`, `V1…V9`, `ORDER …`, `ROUND-CLOSE …`,
`frozen …: OK`, `rows=… defects=`, `REF AUDIT`, `receipt(s)=`, `ROWS total=`, `routed_open=`, `registry_rows=`,
`*_probe exit=… byte_equal=…`, `untracked_in_clone=`. Both round-42 counters are green in my run at `508434a`:
`BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 survived=0 … unattributed=0`,
`MUTANTS-BY-TOOL anchor=9/9 order=5/5`, `PREDICATE C1 pass`; `gate: defects=0`, `V9 ok case_rows=16/16 bad=0`,
`checks=9 defects=0`, `PREDICATE C2 pass`. Probe byte-compares: `constraints_probe exit=0 byte_equal=yes`,
`fibsqrt_probe exit=0 byte_equal=yes`; `sha256sum -c` gives 12/12 and 11/11 `OK`, 0 `FAILED`.

### Any verdict that moved other than the round-42 counters? No.

Versus `measure-baseline.txt` (the pre-landing tree), run-2 differs in **17 blocks / 32 lines of 277**:

- 7 blocks are the round-42 counters themselves (C1 battery/mutants/by-tool/predicate/exit; C2 P3/P4/P6/P7/P8,
  `defects=5→0`, V2/V3/V4/V7/V9, `checks=9 defects=5→0`, `PREDICATE C2 pass`, `exit=1→0`) — the intended change;
- 10 blocks keep their status and move only a count tied to newly landed content:
  `gate: P8 ok index_rows=48 knowledge_files=48` → `49/49` (five older C2 legs, still `ok`),
  `rows=117 tokens=24 defects=0` → `rows=121 tokens=27 defects=0` (still `defects=0`),
  `receipt … doc=corpus/README.md:263+SKILL.md:574` → `:264+SKILL.md:574` and `…round42… doc=plans/fibsqrt_probe.py:4+plans/round-42-claims.md:77` → `doc=SKILL.md:600+SKILL.md:600` (still `equal bytes=`, same byte counts),
  `ROWS total=10 open=4 blocked=1 closed=5 refused=0` / `routed_open=5` → `16/9/1/6/0` / `routed_open=10` (the landing's six routed rows),
  `registry_rows=117 knowledge_files=48 index_rows=48` → `121/49/49`.

Every `exit=` in the list is unchanged except the two round-42 legs; the two pre-existing reds survive identically:
`order38` → `ORDER HIT .ufo/waves/round-38/claims/control-c2-skip.txt@e0a378539a45:11 kind=gate-p10 …`,
`ORDER RESULT FAIL`, `exit=1`, and `round38_c1` → `MUTANT N21 D5 silence SURVIVED`, `MUTANTS total=22 killed=21 survived=1`, `PREDICATE C1 fail`, `exit=1` (measure-baseline:497/261, measure-final:526/290 — same lines both sides).

## The literal `measure.sh` transcription differs in exactly one provenance line

Run-1 used measure.sh's own checkout form (`git checkout -q "$TIP"`), which was non-detaching only because the L1 ran
it at the branch tip. Pinned to `508434a` the clone detaches, and the ledger leg prints

```
REF BIND ref=refs/heads/master rev=508434ad… tip=508434ad… source_ref=445e81f8… why=clone-lacks-ref
```

instead of `REF AUDIT ref=refs/heads/master rev=… tip=… state=match`. Ledger row verdicts are untouched
(`rows=9 closed=9 observed_pass=9 mismatches=0` in both runs, plus the same nine `R34-Dx/R35-Dx status=closed
observed=pass agree=yes` lines). `source_ref=445e81f8…` is the *live lane master*, not the audited commit: the line
is `ledger_tip.py:172-175`'s documented detached-clone fallback ("the body is bound to the commit under audit",
`ledger_tip.py:39-43`), and the body does bind to `508434a` (`BRANCH=tip`), but the printed `source_ref` is a ref
from a different commit and is not marked as unaudited — a reader can misread it as the audited tree.

## `R42ExecNoHarm.md` agrees with `measure-baseline.txt` (24/24), with one denominator caveat

Its 24 counted legs carry the same verdict fields as the corresponding `measure-baseline` legs — spot-checked on the
whole table, all equal:

| wave-1 row | wave-1 value | measure-baseline evidence |
|---|---|---|
| r41_c1 / r40_c1 / r39_c1 / r37_c1 | 48/23·23 · 21/21 · 90/7 · 64/55 | `:133-134` `:214-215` `:355,363` `:590,646` |
| r41_c2 … r37_c2, r36_c2 | `checks=8/7/7/7/7` defects=0, `checks=6` | `:160` `:238` `:385` `:521` `:668` `:678` |
| anchor | `rows=117 tokens=24 defects=0` | `:682` |
| ledger_tip | `rows=9 closed=9 observed_pass=9 mismatches=0`, `REF AUDIT … state=match` | `:767`, `:755` |
| tip_receipts | `receipts=28 byte_equal=8 differ=0 skipped=20`, control `verdict=differ` | `:801`, `:799` |
| order39/40/41/42 | `ORDER RESULT PASS` ×4 | `:254` `:247` `:169` `:59` |
| close41 / close42 | `ROUND-CLOSE RESULT PASS exit=0`, `census … warnings=15 verdict=PASS` | `:875` `:906` |
| constraints_probe / db_wal_probe | `byte_equal=yes`; `regrade cases=28 differ=0`, `cases=28 … mismatches=0` | `:844`, `:845`, `:842` |
| routed_open | `ROWS total=10 open=4 blocked=1 closed=5 refused=0`, `routed_open=5` | `:804-805` |
| frozen42 / frozen41 | 12 OK / 11 OK, 0 FAILED | `:702-714` `:716-727` |

Its two *uncounted* observations also reproduce: `MUTANTS total=14 killed=0 survived=14 …` / `PREDICATE C1 fail` and
`checks=9 defects=5` — byte-identical to `.ufo/waves/round-42/claims/control-c1-nothing.txt` (`MUTANTS total=14
killed=0 survived=14`), and to measure-baseline `:22-27,:50`.

Caveat (calibration, not contradiction): "green=24 of 24" is counted against its own driver, which contains
**no** `order38`, `round38_c1`, `frozen40` or `frozen39` leg (`grep -nE 'order38|r38_c1|frozen40|frozen39|
round38_c1' …/build/R42ExecNoHarm/measure.sh` → no match). The two legs it omits are precisely the two that are red in
measure-baseline for pre-existing reasons, so nothing is hidden — but the report's tally denominator is 24 of its own
list, not 24 of measure.sh's 30 commands, and the omission is not stated there. Its driver also used
`checkout -q -B master "$COMMIT"`, so it never hit the `REF BIND` artifact above — its `REF AUDIT … state=match` row
is correct for its harness.

## Findings for the L1 (falsify, not fixes)

1. **`measure.sh` is not replayable once the branch moves.** `TIP=$(git -C "$L" rev-parse refs/heads/master)`; the
   live master is now `445e81f8…` ("wave-1 reports/results (39 seats), planned round 43, wave-2 spec and dispatch"),
   769 files after `508434a`. Re-running `measure.sh` today measures a different tree, not `measure-final`. Only a
   pinned driver (mine: `COMMIT` + `-B master`) reproduces the frozen receipt; measure.sh should take a `COMMIT=` like
   wave 1's driver does.
2. **Pinned runs detach and flip the ledger provenance line** (see above): same counted verdicts, different
   `REF` spelling. `-B master <commit>` is the fix; wave 1 already had it.
3. **`measure-final.txt`'s own Q32 line does not show a quiescent PATH dir:**
   `ENVELOPE end 17:52:40 exit=0 local_bin_listing_before=763032563d3739aa after=77408cab9a10361a CHANGED`
   (baseline, `:909`: `… before=763032563d3739aa after=763032563d3739aa unchanged`). The lane verdicts cannot be
   affected — every measured tool is digest-pinned (`PINS total=… mismatched=0`, 12/12 + 11/11 `frozen …: OK`) — but
   that receipt must not be cited as evidence that nothing was installed during the landing measurement.
4. **Names-only hashing is blind to content rewrites of PATH binaries.** `/home/vgpnk/.local/bin/omp` (276 MB ELF,
   inode unchanged) was rewritten at `18:10:45`, inside run-1's window, by a process outside my sandbox
   (mtime = ctime = 18:10:45.199, size 275970224 unchanged; `ls -A | sha256sum` identical before and after, so the
   mandated Q32 check cannot see it). Run-2's window is clean (`pathdir_new_entries=0`, `omp` mtime/size identical at
   both ends). Worth adding a `sha256sum` over the *contents* of the few binaries a measurement actually invokes.

## Limits

- I did not run `measure.sh` itself (it would measure `445e81f`); the command **list** is transcribed verbatim in
  `driver.sh`/`driver2.sh`, and its semantics — "the measured commit is the branch tip" — are reproduced by pinning
  `refs/heads/master` to `508434a` (run-2, primary) against the literal transcription (run-1, control).
- Per-fixture (`FIXTURE … ok`) and per-case (`CASE …`) lines were compared as part of the full-log identity, not
  individually re-derived; the aggregates (`BATTERY fixtures=… wrong=0 tampered=0 sidechannel=0`, `MUTANTS …`) and the
  runs' `exit=` agree, so no fixture or case flipped.
- The two pre-existing reds (`order38`, `round38_c1`) are outside round 42's no-harm surface; I record their survival,
  I do not adjudicate them.
- No tool was installed or upgraded (nothing was missing); no pacman/`uv tool`/binary fetch, no lane write, no commit.

VERDICT: no-harm-verdicts-equal-277/277
