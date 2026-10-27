# R48C1MutOrder — C1 order/seed probe

Axes named: calibration (assigned); test-order/seed invariance and first-match sensitivity (item).

## Freeze and scope

`REV a543d92083557dd9b33ee674e9b99b03411f80af` (stage-1 freeze). Verified the committed tree contains `plans/round-48-claims.md` (blob `3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5`); stage-1 commit time `2026-10-27T06:53:29-03:00`; claims content is unchanged through lane HEAD `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`. The freeze therefore predates this probe. Scratch clone was checked out at the frozen revision. This is a detector/order probe of the frozen base fence using the round-46 C1 detector, not a scored R48 claim run; no stage-2 R48 counter or claimed/repaired work was measured.

## Commands and observed outputs

Scratch: `/fast/scratch/hyaku/kengaku-r48/R48C1MutOrder`; clone top-level verified as `/fast/scratch/hyaku/kengaku-r48/R48C1MutOrder/lane`. Runtime prerequisites existed: `/usr/bin/strace`, `/usr/bin/bwrap`, `/usr/bin/python3`; Python 3.14.8.

Pristine run command (repeated for each seed):

```sh
export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1MutOrder
python3 plans/round46_c1_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r48/R48C1MutOrder/work --seed SEED
```

Eight seeds: `0000000000000001`, `deadbeefcafe0001`, `1234567890abcdef`, `ffffffffffffffff`, `00000000abcdef01`, `5555aaaa5555aaaa`, `13579bdf2468ace0`, `aaaaaaaa00000001`; seed `0000000000000001` was repeated. Also ran once without `--seed` (SystemRandom). All nine runs exited 0. Each printed the same classified counts:

```text
PINS total=65 mismatched=0
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=32 contradicted=0
REASON -
PREDICATE C1 pass
```

Sorted per-module verdict lines had identical MD5 `db5424fb8d74a8e71e36fe764c6070f5` across all nine runs. Each had 153 `FENCE-RUN` entries and 153 `touches=0`; differences were only the intentionally fresh temporary root path. Same seed with `--jobs 1` and `--jobs 16` also exited 0 with identical classified counts and normalized per-fixture FENCE-RUN lines (`JOBS-DIMENSION-IDENTICAL`). The base population here is the 104 committed battery fixtures; it does not include the later-frozen R48 honest additions.

### Mutation probe

Plausible order mutant: replaced `rng.shuffle(jobs)` with `jobs.reverse()` at the round-46 counter's execution-order step. Same detector command and seed `0000000000000001`; actual output was `EXIT=0`, `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`, `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, `CALIBRATION advertised=32 contradicted=0`, `REASON -`, `PREDICATE C1 pass`.

Verdict: **SURVIVED** — execution-order reversal did not alter classified counts or predicate. This is a coverage finding, not a change to the frozen contract. The same-seed detector was rerun after restoration and produced the pristine output above, exit 0.

## Restoration evidence and limits

Before mutation SHA-256: `plans/round46_c1_verify.py` `ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508`; `plans/fixture_fence.py` `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`; `plans/round44_c1_verify.py` `6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad`. After restoration, all three hashes matched exactly. No production file changed. This samples eight deterministic seeds, a stochastic run, and two job-parallelism values; it is not exhaustive over seeds, does not test stage-2 frozen additions, and does not establish the R48 v3 counter's behavior. Scratch was removed before report completion.

## Sources opened (accessed 2026-10-27)

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — quote: “name-hiding (Q39) retained: fixture dirs, build dirs and module copies are named by a per-run random token, fence jobs run in shuffled order” (C1 counter delta).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — quote: “repair over-refusal (9/9 novel honest controls refused) and broaden positive controls”.
- `file:///fast/scratch/hyaku/kengaku-r48/R48C1MutOrder/lane/plans/round46_c1_verify.py` at `REV a543d92083557dd9b33ee674e9b99b03411f80af` — quote: “rng.shuffle(jobs) # rule (b): run order carries no signal”.
- `file:///fast/scratch/hyaku/kengaku-r48/R48C1MutOrder/lane/plans/fixture_fence.py` at the same revision — quote: “Return (repos, reason): every directory holding a real `.git` dir”.

VERDICT: SURVIVED — no order/seed-dependent classified-count change observed in the tested base-counter permutations; R48 C1 admission not assessed.