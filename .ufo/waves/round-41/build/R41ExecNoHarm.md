# R41ExecNoHarm — no-harm baseline at the round-41 freeze (wave 1)

Seat: executor, leaf. Scope: run the standing instruments on a clean clone of the frozen probe-run commit
`f774a87ad071122acd39ba02a9901b5b56d9910a`, inside the ruled host-safety envelope, and leave a re-runnable
`measure.sh`. No lane file touched; the two frozen tools, both round-41 counters, the probe, spec, gate, dry
table, captures, receipts and `claims/` are read-only inputs here.

Re-runnable driver (this seat's own subdir, sha256 `ea4e79f64050f0686f58d548047d557f4afca5ad5e78a257d697b02326f3169c`):

```
.ufo/waves/round-41/build/R41ExecNoHarm/measure.sh          # ~280 s, prints GREEN/RED tally, removes its scratch
```

Full per-instrument logs are committed with this report under `.ufo/waves/round-41/build/R41ExecNoHarm/logs/`.

## Method

```
S=/fast/scratch/hyaku/kengaku-r41/R41ExecNoHarm        (TMPDIR=$S/tmp; trap removes $S)
git clone -q --shared <lane> "$S/lane"; git -C "$S/lane" checkout -q -B master f774a87…
[ "$(git -C "$S/lane" rev-parse --show-toplevel)" = "$S/lane" ]   # asserted before any write
```

Envelope for **every** instrument (verbatim from the wave rule, nesting-safe):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent  <command>
```

Operability detail worth carrying into the landing measurement: a `--shared` clone left **detached** hands every
*child* clone (each counter clones the lane) the source's `master`, i.e. the wave-1 dispatch tip `fc79f2a`, not
the measured commit. `measure.sh` therefore pins `master` to `COMMIT` (`checkout -q -B master`), so child clones
check out the frozen bytes. With `--detach` alone, `round40_c1` observed `PINS-AFTER mismatched=3` on the first
(15:42) attempt; the two causes are separated in the interruption note below.

## Result: 18 green of 18 (exit 0 + verdict line in each log)

| # | instrument (cwd = clone root) | exit | verdict line (log) |
|---|---|---|---|
| 1 | `plans/round40_c1_verify.py --lane . --work $S/w/r40_c1` | 0 | `PINS total=3 mismatched=0` / `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0` / `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0` / `PINS-AFTER mismatched=0` / `PREDICATE C1 pass` (`r40_c1.log`) |
| 2 | `plans/round40_c2_verify.py …` | 0 | `checks=7 defects=0` / `PREDICATE C2 pass` (`r40_c2.log`) |
| 3 | `plans/round39_c1_verify.py …` | 0 | `PINS total=26 mismatched=0` / `BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0` / `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0` / `PREDICATE C1 pass` (`r39_c1.log`) |
| 4 | `plans/round39_c2_verify.py …` | 0 | `checks=7 defects=0` / `PREDICATE C2 pass` (`r39_c2.log`) |
| 5 | `plans/round38_c2_verify.py …` | 0 | `checks=7 defects=0` / `PREDICATE C2 pass` (`r38_c2.log`) |
| 6 | `plans/round37_c1_verify.py …` | 0 | `BATTERY fixtures=64 wrong=0 renamed_disagree=0` / `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0` / `PREDICATE C1 pass` (`r37_c1.log`) |
| 7 | `plans/round37_c2_verify.py …` | 0 | `checks=7 defects=0` / `PREDICATE C2 pass` (`r37_c2.log`) |
| 8 | `plans/round36_c2_verify.py --lane . --fleet /home/vgpnk/Projects/shokunin` | 0 | `checks=6 defects=0` / `PREDICATE C2 pass` (`r36_c2.log`) |
| 9 | `plans/anchor_digest_check.py --lane .` | 0 | `rows=114 tokens=21 defects=0` (`anchor.log`) |
| 10 | `plans/ledger_tip.py --source $S/lane --work $S/lt` | 0 | `REF AUDIT ref=refs/heads/master rev=f774a87… tip=f774a87… state=match` / `rows=9 closed=9 observed_pass=9 mismatches=0` (`ledger_tip.log`) |
| 11 | `plans/tip_receipts.py --lane . --work $S/tr` | 0 | `tip f774a87…` / `note compared=7 declared_bounded=1 no_command=19` / `receipts=27 byte_equal=7 differ=0 skipped=20`; auto control `receipt=corpus/evidence/round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ` (`tip_receipts.log`) |
| 12 | `plans/order_check.py --lane . --claims plans/round-39-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt` | 0 | `ORDER RESULT PASS` (`order39.log`) |
| 13 | same, `round-40-claims.md` + `corpus/evidence/round40/db-wal-probe.txt` | 0 | `ORDER RESULT PASS` (`order40.log`) |
| 14 | same, `round-41-claims.md` + `corpus/evidence/round41/constraints-probe.txt` | 0 | `ORDER RESULT PASS` (`order41.log`) |
| 15 | `plans/round_close.py --lane . --round 40 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | 0 | `receipts=1` / `order receipt=corpus/evidence/round40/db-wal-probe.txt exit=0 verdict=PASS` / `census exit=0 warnings=15 verdict=PASS` / `ROUND-CLOSE RESULT PASS exit=0` (`close40.log`) |
| 16 | same, `--round 41` | 0 | `receipts=1` / `order receipt=corpus/evidence/round41/constraints-probe.txt exit=0 verdict=PASS` / `census exit=0 warnings=15 verdict=PASS` / `ROUND-CLOSE RESULT PASS exit=0` (`close41.log`) |
| 17 | `plans/db_wal_probe.py --lane . --work $S/w/dbwal` (stdout byte-compared) | 0 | `cases=28 observed_pass=8 observed_fail=20 mismatches=0` / `regrade cases=28 differ=0`; **byte_equal=yes**, receipt and fresh stdout both `sha256=c74c6b91c8c49b1788f2dd7aa0d66edce0db0b52b549baf89ce69cfa8e2a730e` (`db_wal_probe.out`, `.err` empty) |
| 18 | `sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt` (clone root) | 0 | `files=11 ok=11 failed=0` (`frozen_digests.log`) |

`round_close` was given `--census` explicitly: a scratch clone's parents hold no fleet census, and the tool's
documented fallback (`$SHOKUNIN_ROOT`, lane parents) is absent there — setup error, not a pass.

Independent cross-check on the live lane (read-only, 15:45:19): `sha256sum -c …frozen-digests.txt` → exit 0, all
11 `OK`, so the clone's frozen bytes equal the current lane's.

## Host-safety receipts (post-run, printed by `measure.sh`)

- `pathdir_new_entries=0` — `find /home/vgpnk/.local/bin -newermt @<start>` is empty: nothing in the shared PATH
  dir was created or modified during the 280 s run.
- `pathdir_git_entry=absent` before **and** `pathdir_git_entry_after=absent` — no `git` shim in `~/.local/bin`;
  the round-40 vector stays closed. File count `pathdir_files=52` before, `52` re-counted at 15:49:31 after the
  run (`find /home/vgpnk/.local/bin -maxdepth 1 -type f | wc -l`); `measure.sh` now prints `pathdir_files_after`
  too.
- Neutralized attack modules unchanged and inert: `sha256sum` `f532423bd90bd752f7880bdba88f53df931ba7cdc184af87d5d295512fff3b9e`
  (`crit_git_shim.py`) and `7c4f434b750b3a7e480681ef7729a0e509d159bd3cc29403949564a1a9bd96f7` (`crit_ledger_selfread.py`);
  the neutralization banner is present in both (e.g. `.ufo/waves/round-40/build/R40CritC1Counter/crit_git_shim.py:10`:
  "NEUTRALIZED by the round-40 L1 (orchestrator host-safety ruling 2026-10-26)"), and
  `neutralized_referenced_by_plans=0` — no `plans/` file names either module, so no instrument imports them.
- `clone_dirty_after=0`, `lane_head_after=f774a87ad071122acd39ba02a9901b5b56d9910a` — no instrument mutated the
  measured tree; the clone's index was untouched too (git calls in the clone are `clone`/`checkout`/`rev-parse`/
  `status` only).
- Scratch `S` removed on exit (`trap`); only `measure.sh` and `logs/` (100 KB) remain in this report dir.

## External interruption (recorded, superseded)

At **15:42:24 -03** seat `R41CritIndep` ran `rm -rf -- /fast/scratch/hyaku/kengaku-r41` (the whole round root)
while this seat's first smoke run was executing; the L1 confirmed it by IRC and instructed affected seats to
recreate `$S` and re-run. That run is **not** the baseline: mid-run tree deletion explains its artifacts —
`TAMPERED` on 3 fixtures, `PINS-AFTER mismatched=3`, 4 `SURVIVED` ledger mutants (anchor/ledger fixtures whose
directory and whose lane tool file had vanished). `[INFERENCE]` on the causal link: the three counts coincide and
the run's clone root no longer existed when it finished. The clean re-run above (15:44–15:48) is the recorded
baseline and is 21/21 mutants killed, `tampered=0`, `PINS-AFTER mismatched=0`.

Two follow-ons for the orchestrator, not this seat's to fix: the deletion was host-wide (it also removed live
sibling scratch trees), and the wave rule's `trap 'rm -rf -- "$S"' EXIT` is only safe while every seat's `$S` is
strictly below `/fast/scratch/hyaku/kengaku-r41/<SeatName>` — a seat that expands `$S` to the round root wipes
other seats' work.

## Limits

- Measured at `f774a87`, not at the wave-1 landing tip. `round41_c1_verify.py` / `round41_c2_verify.py` are
  deliberately **out** of this baseline (the C1/C2 seats own their verdicts); `order_check --round 41` and
  `round_close --round 41` are in, and pass at this commit.
- `tip_receipts` reproduces 7 of 27 receipts byte-equal, 1 declared-bounded skip, 19 `no-committed-re-run-command`
  — the tool's own population statement, recorded as-is (not a defect of this baseline).
- Host `python3` / `git` / `bwrap` stand in for any image; the sandboxes are the instruments' own.
- `anchor_digest_check` prints `rows=114 tokens=21` at this commit; recorded as the pre-wave-1 count, no
  interpretation added.
- No tool was installed, upgraded or removed (`pacman` untouched; `~/.local/bin` not written). No background job,
  no subagent, no commit, no `git add`, no mutating `jj`.

VERDICT: no-harm-baseline-18-green-of-18
