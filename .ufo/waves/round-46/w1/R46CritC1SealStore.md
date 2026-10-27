# R46CritC1SealStore — sealed Git-store modules

**Axis:** calibration (C1). Tested only against the frozen base fence at `64ba8385ea10af1b78d367dcb242b92d97062af7`, using the round-45 counter's `build_module`/`run_fence` machinery on a clone. No repaired-fence evaluation was performed.

- `objects_link.py` — object-store symlink: **LEAKED** (ADMIT, 15 outside opens).
- `packed_refs.py` — packed-refs file symlink: **LEAKED** (ADMIT, 2 outside opens).
- `refs_link.py` — refs-directory symlink: **LEAKED** (ADMIT, 4 outside opens).

Counter evidence: the envelope-bracketed base-counter run printed `FENCE plans/fixture_fence.py sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`; each retained module's `FENCE-RUN` was `ADMIT` with the open count above and `HELDOUT ... LEAKED`. Both envelope runs ended `exit=0 ... unchanged` (first: before/after `ff187bb5c98aa6b5`; second: before/after `ff187bb5c98aa6b5`). The second run also confirmed the two initially tested modules and measured packed-refs. Commands were the two envelope invocations of `/usr/bin/python3 <scratch>/driver.py <scratch>/lane <scratch>/run[2] <sealed-dir>`; the driver's pattern imports round-44 `builder_source` through `round45_c1_verify.build_module` and calls `run_fence` for each fixture.

- `head_link.py` — HEAD symlink variant: base verdict **clean** (BREACH, zero opens; Git could not describe the worktree); excluded from the sealed set.

The canonical counter is frozen to be pinned after wave 1; these are pre-data attacks only. The small safe correction indicated by this evidence is to inspect store contents recursively without following symlinks, rejecting any symlink/special indirection inside `.git` whose target leaves the fixture before invoking Git. This mirrors the existing outside-symlink rule for the ordinary fixture tree and closes the demonstrated object/ref paths.

Artifacts: `sealed/objects_link.py`, `sealed/packed_refs.py`, `sealed/refs_link.py`; SHA256 digests are in `sealed/SHA256SUMS`; mechanism details are in `sealed/NOTES.md`.

VERDICT: sealed-store-3-base-leaked-3-read-0