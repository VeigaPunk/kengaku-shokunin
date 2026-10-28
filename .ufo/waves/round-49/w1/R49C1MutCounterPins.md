# R49C1MutCounterPins — C1 frozen-input pin mutation probe

Axes: calibration (R49-C1); counter integrity / stale-input detection.

## Freeze and measured revision

Verified stage-1 freeze commit `9d2900af41e4d1fc6022eff99010436fde6dbd93` with `git cat-file -t` and `git log -1 --format='%H %ci %s'`: commit timestamp `2026-10-28 09:14:40 -0300`, subject `round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)`. Measurements began at 09:26:00 -0300. Clone HEAD and `git rev-parse --show-toplevel` were verified as the frozen revision and `/fast/scratch/hyaku/kengaku-r49/R49C1MutCounterPins/lane`; clone porcelain was empty.

**Important limitation:** `plans/round49_c1_verify.py` is absent from that frozen commit (confirmed by `git cat-file -e <REV>:plans/round49_c1_verify.py`; output `fatal: path ... does not exist`, `COUNTER_ABSENT`). Therefore this probe exercised the committed predecessor contract `plans/round46_c1_verify.py` at REV `9d2900af41e4d1fc6022eff99010436fde6dbd93`, not the not-yet-pinned R49 v3 counter. This is evidence about the imported PINS mechanism, not a verification of the R49 implementation or an admission claim.

## Detector and mutations

The frozen R46 counter declares 65 pins covering the builder, refusal-source and refusal/sealed inputs, and all 22 honest fixture modules. In default mode it also flags unpinned `.py` entries under refusals/sealed directories. Its output includes `PINS total=65 mismatched=…`, `REASON …`, and `PREDICATE C1 …`; it checks pins again after scoring. The counter binds refusal/sealed totals and `HONEST_TOTAL=104`.

Scratch-only isolated `plans/` snapshots were made from the shared clone. Detector command for each: `python3 <snapshot>/plans/round46_c1_verify.py --lane <snapshot> --work <scratch>/work/<case> --jobs 4` (no overrides; default pin and inventory checks active). The same bounded detector ran on pristine, each mutant, and restored pristine bytes.

| Case | Scratch mutation | Observed detector output (verbatim key lines) | Exit / result |
|---|---|---|---|
| BASE | pristine frozen inputs | `PINS total=65 mismatched=0`; `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`; `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `CALIBRATION advertised=32 contradicted=0`; `REASON -`; `PREDICATE C1 pass` | 0; baseline passes |
| M1 | one byte changed in sealed46/s_packed_refs.py | `PINS total=65 mismatched=1 first=plans/sealed46/s_packed_refs.py`; `REASON pins=1,pins-after=1,sealed-not-clean,contradicted=1`; `PREDICATE C1 fail` | 1; killed |
| M2 | deleted refusals46/f7_commondir.py | `PINS total=65 mismatched=1 first=plans/refusals46/f7_commondir.py`; `COPY f7_commondir.py ABSENT`; `MODULES refusal total=19`; `REASON pins=1,pins-after=1,refusals-total=19!=20,refusals-not-clean,contradicted=1`; `PREDICATE C1 fail` | 1; killed |
| M3 | added sealed46/zz_pinned_check.py copied from a sealed module | `PINS total=65 mismatched=1 first=plans/sealed46/zz_pinned_check.py:unpinned`; `MODULES sealed total=13`; `REASON pins=1,sealed-total=13!=12`; `PREDICATE C1 fail` | 1; killed |
| M4 | one byte changed in honest battery43/a_url.py | `PINS total=65 mismatched=1 first=plans/battery43/a_url.py`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `REASON pins=1,pins-after=1`; `PREDICATE C1 fail` | 1; killed (content pin, independent of count) |
| M5 | deleted honest battery44/u7_twin_b.py | `PINS total=65 mismatched=1 first=plans/battery44/u7_twin_b.py`; `MODULES honest total=21`; `HONEST fixtures=101 admitted=101 refused=0 read=0 hung=0 build_errors=0`; `REASON pins=1,pins-after=1,honest-not-admitted`; `PREDICATE C1 fail` | 1; killed (pin and expanded fixtures-count predicate) |
| M6 | changed first hex digit of the counter's pinned digest for sealed46/s_refs_link.py | `PINS total=65 mismatched=1 first=plans/sealed46/s_refs_link.py`; `REASON pins=1,pins-after=1`; `PREDICATE C1 fail` | 1; killed (stale pin) |
| M7 | one byte changed in round44_c1_verify.py builder | `PINS total=65 mismatched=1 first=plans/round44_c1_verify.py`; `SETUP the round-44 counter (builder) is not at its pinned digest` | 2; killed before scoring |
| M8 | one byte changed in refusals45/f1_gitfile.py | `PINS total=65 mismatched=1 first=plans/refusals45/f1_gitfile.py`; `COPY f1_gitfile.py DIFFERS`; `REASON pins=1,refusals-not-clean,contradicted=1`; `PREDICATE C1 fail` | 1; killed |
| RESTORED | all mutant snapshots restored from pristine BASE | `PINS total=65 mismatched=0`; `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`; `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `CALIBRATION advertised=32 contradicted=0`; `REASON -`; `PREDICATE C1 pass` | 0; restored detector pass |

M7 exited 2 before scoring because the pinned builder digest was stale. The M1 byte change caused one sealed build error as well as the pin mismatch; the counter still detected it. M2/M5 are inventory removals and M3 is inventory growth; each was rejected. M4 directly changed honest fixture bytes while preserving fixture count, and the PINS leg detected the tamper.

## Exact setup / execution commands

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r49/R49C1MutCounterPins/work
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1MutCounterPins/work
git clone --quiet --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r49/R49C1MutCounterPins/lane
git -C /fast/scratch/hyaku/kengaku-r49/R49C1MutCounterPins/lane checkout --quiet --detach 9d2900af41e4d1fc6022eff99010436fde6dbd93
# Verified git -C ... rev-parse --show-toplevel and HEAD before making snapshots.
# cp -a lane/plans to BASE and M1..M8 scratch snapshots; mutations were confined to those snapshots.
python3 SNAP/plans/round46_c1_verify.py --lane SNAP --work SCRATCH/work/CASE --jobs 4
```

The mutations were isolated to individual scratch snapshots. Each was subsequently replaced in full with pristine `BASE/plans`; `diff -qr BASE/plans snap-X/plans` reported byte-identical for M1–M8. The pristine/re-restored SHA-256 values (matching the clone's pre-mutation hashes) were:

```text
round44_c1_verify.py  6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad
refusals45/f1_gitfile.py  bac0df8aa55e35de2964f0e98a8c461aa6eeeba9daa2f18ca113a383f24a4c8d
refusals46/f7_commondir.py  c828c1010e38e17812374e8d5383d4fb04e8e37d0ad38915f46723b726eaa0f3
sealed46/s_packed_refs.py  3f7d4e08bc7c2c5ba4a42b6ac376344942cc70d2b23ef6873f4f1dafccc08fda
sealed46/s_refs_link.py  b25d66ea8fb8a595c8b339d6741e14b72f26040e4e16388c2662b0c76d779084
battery43/a_url.py  6a3d4732162c46a4eeabf8f5274860cab5373ffa6eabfa16a5c259524697e5fd
battery44/u7_twin_b.py  6bee837959584e12577647fb280d1ea50228edf03106868ec2c4cb11087f4d89
round46_c1_verify.py  ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508
fixture_fence.py  05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
```

No external source was opened; URL/access-date/quote: not applicable. No tools were installed. The base fence passed this R46 104-fixture population; this is not the extended R49 population and is not an R49 claim result.

Limits: the R49-specific counter and stage-2 frozen inputs are not present at the stage-1 revision, so its newly added inventory/pin code could not be exercised here. The R46 predecessor's digest and inventory checks were exercised; full R49 v3 mutation behavior remains unverified by this seat.

VERDICT: **INCONCLUSIVE for R49-C1 implementation** (counter absent at measured freeze); **8/8 R46 predecessor pin/inventory mutants killed**, with pristine and restored inputs passing. No R49-C1 admission claim.
