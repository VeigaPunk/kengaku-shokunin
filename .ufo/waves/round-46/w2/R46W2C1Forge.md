# R46W2C1Forge — C1 falsification

## Axes
Calibration; robustness against name/structure/timing/env channels; honesty of the frozen measurement.

## Evidence
Two required-envelope runs of the pinned counter on clean clone 42d5043afac952fcb43bf4798757785dd258cf85, seeds 1111111111111111 and 2222222222222222. Both returned exit 0, PINS total=65 mismatched=0, REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0, SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0, HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0, CALIBRATION advertised=32 contradicted=0, PREDICATE C1 pass. Both ENVELOPE end lines report unchanged; second full captured output: R46W2C1Forge/seeded-base.out. Exact command: python3 plans/round46_c1_verify.py --lane $S/lane --work $S --seed <seed>.

Historical B1-B6 attack mechanisms appear addressed in the pinned design: external read-only trace log and fail-closed missing/empty logs; random opaque fixture/build/module names, padded siblings and shuffled order; scratch-root event accounting; verdict by exit status; expanded metadata syscall set; pending/resumed and dirfd parsing. No independently authored blind channel fence variant was run, so no new forged predicate pass is claimed. B7 io_uring is expressly unblocked and remains a bypass channel: SQE open/read need not emit traced open syscalls.

## Counterexample and smallest correction
Counter source explicitly limits touch accounting to scratch root, while the frozen advertisement says no reading outside d. Host paths outside scratch (/etc, /proc, /sys) are acknowledged uncounted, so a fence can read them without measurement impact. Also io_uring can evade the syscall set. These undermine measurement scope, though neither yielded a demonstrated forged pass in this seat. Smallest safe correction: narrow the advertised property to scratch-root touches or broaden containment/measurement to host paths; block/account for io_uring. Add a blind held-out fence keyed on any remaining exposed channel to test closure.

No tools installed.

VERDICT: c1-forged-pass-0-of-1
