# R49C1MutOrder — C1 permutation/order probe

## Axes

- **Classification-order invariance:** seed-controlled shuffled build/job order and concurrency must not change the per-leg classified counts.
- **Seed/hash-seed sensitivity:** RNG and `PYTHONHASHSEED` changes must not change counts.
- **First-match/order mutation sensitivity:** removing the job shuffle must not change classifications; the same detector should expose any change.

## Freeze and measured revision

Before any counter execution, checked the committed lane tree. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93` printed `commit`; its log line was `9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims`; `merge-base --is-ancestor ... HEAD` printed `ANCESTOR-OF-HEAD yes`. Freeze preceded all measurements.

Measured the committed **round-46 C1 contract base** at `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93`, cloned `--shared` into this seat's scratch and checked `git -C "$D" rev-parse --show-toplevel` was `$D`. Stage-2 `round49_c1_verify.py` was not present in the committed tree, so this is a contract-base robustness probe, not a scored R49-C1 receipt. SHA-256 before test: `plans/round46_c1_verify.py ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508`; imported builder `plans/round44_c1_verify.py 6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad` (matches its pin); fence `plans/fixture_fence.py 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`.

No external URL/source was opened; hence no external-source URL/access-date/quote applies. I read the local frozen claims, routed spotcheck, and round-48 lesson.

## Commands run

Freeze checks (against lane):

```sh
D=/home/vgpnk/Projects/shokunin/kengaku-shokunin
git -C "$D" rev-parse HEAD
git -C "$D" cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C "$D" log --format='%H %ci %s' -1 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C "$D" merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD
```

Created one scratch clone: `git clone --shared --no-hardlinks file:///home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/clone"`, then `git -C "$D" checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93`; verified top-level and `HEAD` both identify the clone and freeze respectively. Counter availability prerequisites observed: `/usr/bin/bwrap ok`, `/usr/bin/python3 ok`, `/usr/bin/strace ok`.

Permutation matrix used this exact invocation template, sequentially (each command ran from the clone):

```sh
TMPDIR="$S" PYTHONHASHSEED="$hs" python3 plans/round46_c1_verify.py --lane "$C" --work "$S/runs" [--seed "$seed"] --jobs "$jobs"
```

Cases: `(PYTHONHASHSEED, seed, jobs)` = `(1,1,8)`, `(1,0,8)`, `(1,a5a5a5a5,8)`, `(1,deadbeef,8)`, `(0,1,8)`, `(1,1,8)` repeat, `(1,1,1)`, `(1,1,16)`, `(1, omitted,8)` (SystemRandom token/order run). Each process exit code was `0`.

Mutation detector was the full counter invocation above with `PYTHONHASHSEED=1`, `--seed 1 --jobs 8`, collecting `PINS`, all leg rollups, `CALIBRATION`, and `PREDICATE`. Mutation: scratch-only deletion of the single `rng.shuffle(jobs)` statement (`round46_c1_verify.py` line 553 at the pre-edit snapshot); no other byte changed. Ran detector on pristine (matrix `r0`), mutated, restored bytes, and detector again on restored bytes. Restored via `cp` from an exact pristine backup.

## Observed output

All nine permutation runs produced the same classification summary (verbatim):

```text
PINS total=65 mismatched=0
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=32 contradicted=0
REASON -
PREDICATE C1 pass
```

The per-fixture `FENCE-RUN` records, sorted for comparison against `r0`, had no differences across the nine runs. The mutation run and restored run each printed the same six summary lines above, and both exited `0` (`mutant_exit=0`, `restored_exit=0`). Mutation before/after file hashes:

```text
pristine counter: ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508
mutant counter:   0a1eef35d7bb09b6199bde9355db77d212ff5502ddf638c827e10fcb7329fc9f
restored counter: ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508
RESTORE cmp=identical
```

The counter's source uses `rng.shuffle(order)` and `rng.shuffle(jobs)`; its `rollup` classification is per module, and honest counts aggregate per-fixture verdicts. Static fence scan showed sorted directory walks (`dirs[:] = sorted(keep)`) and sorted results (`return sorted(out)`); config parsing is sequential, returning on the first disallowed section/key. I did not separately fabricate/reorder config contents, so no claim is made about verdict sensitivity to config byte-order on synthetic stores.

## Limits and verdict

- Probe population is the round-46 committed base (20 refusal modules, 12 sealed modules, 104 honest fixtures); it does not include wave-1 novel honest/sealed populations or the not-yet-committed v3 counter.
- `--seed` runs are explicitly testing overrides, not receipts for a frozen R49-C1 scored run. `PYTHONHASHSEED` and `--jobs` were varied as listed; no claim beyond this tested matrix.
- Removing the job shuffle was a plausible ordering mutant; the detector **survived** it because all classifications/counts remained invariant. This is a coverage finding, not evidence to alter the frozen contract. No order/seed-induced classification change was found in the exercised matrix.
- No tools installed or updated.

**VERDICT: SURVIVED / NO ORDER-DEPENDENT CLASSIFICATION FOUND in the tested round-46 contract-base matrix; mutant is a coverage finding. Not an R49-C1 admission or stage-2 counter result.**
