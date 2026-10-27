# R46CritC1Forged — C1 forged-fence panel

**Axes:** calibration (primary), operability (reproducible receipt set). Work stayed within this seat's report directory and `/fast/scratch/hyaku/kengaku-r46/R46CritC1Forged`; no lane files were changed.

## Method and evidence

Read the frozen `plans/round-46-claims.md` in full before making artifacts. Used a verified `git clone -q --shared` of the lane in the seat scratch and ran `plans/round45_c1_verify.py` against separate clone copies with each fence installed as `plans/fixture_fence.py`. Every measurement ran through `.ufo/waves/round-46/claims/envelope.sh`; full stdout/stderr, including `ENVELOPE` start/end lines, is in `R46CritC1Forged/receipts/`. The r45 counter digest line was `PINS total=33 mismatched=0` throughout.

`fences/` contains 13 standalone variants, each with its bypass and expected sound-r46-control verdict in its header. `SHA256SUMS` hashes the fence files; `receipts/SHA256SUMS` hashes the complete run receipts.

| Fence | Bypass / keyed exposure | r45 counter result |
|---|---|---|
| `b1_log_erasure.py` | B1 trace-log unlink | pass |
| `b2_keyed_path.py` | B2 refusal-family path key | pass |
| `b3_host_read.py` | B3 host `/etc`/`/proc` reads | pass |
| `b3_module_read.py` | B3 read module-source copy outside counted fx/btmp | pass |
| `b4_stdout_spoof.py` | B4 spoof `BREACH` on shared stdout | pass |
| `b5_stat_channel.py` | B5 stat/readlink channel | pass |
| `b6_killed_open.py` | B6 child blocked on f4's sibling FIFO, then killed | pass |
| `keyed_sibling_count.py` | `d.parent` stat/nlink exposure | pass |
| `keyed_argv_shape.py` | absolute argv-path shape exposure | pass (final version) |
| `keyed_fixture_count.py` | fixture-path/stat exposure | pass |
| `keyed_inode_mtime_order.py` | inode/mtime metadata exposure | pass |
| `keyed_env.py` | inherited env exposure | pass |
| `keyed_build_order.py` | strace slot index from tracer argv | pass |

Each passing receipt contains `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass`, exit 0, and `ENVELOPE end ... unchanged`. The first `keyed_argv_shape.py` attempt failed (`clean=4 leaked=6`, `PREDICATE C1 fail`); the final receipt is the repaired version and passes. Its failed first run is not represented as a successful fence receipt.

## Important calibration caveat

The six `keyed_*` submissions are useful *channel probes*, but only `keyed_build_order.py` has a coherent proposed name-independent discriminator: it extracts the `sNNNNN` slot from strace's command line and uses the r45 refusal-before-honest job order. The other keyed probes currently retain the r45 `/refusals45-` path predicate as their actual refusal selector; their stat/argv/env predicates are auxiliary conditions, not demonstrated independent classification keys. In particular, the r45 pass receipts do **not** establish that those individual channels alone split refusal from honest fixtures or that a sound stage-2 counter must reject them. Don't treat these receipts as proof that the r46 name-hiding controls fail. Smallest safe correction for stage-2 judging: require each proposed channel control to remove the path fallback and prove its own refusal/honest split; reject or replace any that cannot do so. This is material because a passing r45 counter is the task's forged-pass criterion, while independently attackable controls are what the name-hiding claim needs.

`b6_killed_open.py` exercises the sibling FIFO created by f4; its path-only fallback still refuses the other refusal fixtures. The harness's `open` observation for the killed child is not separately asserted in this full counter receipt, so the receipt proves the overall forge, not a per-syscall trace autopsy.

## Measured outputs and envelope

For every passing row above, the individual full receipt under `receipts/<fence>.txt` is the command output. The measured command was:

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh "$S" /usr/bin/python3 "$D/plans/round45_c1_verify.py" --lane "$D" --work "$S/work-<fence>"`

where each `$D` is a verified shared clone and `$S=/fast/scratch/hyaku/kengaku-r46/R46CritC1Forged`. For example, `b2_keyed_path.txt` records `ENVELOPE start 02:01:26`, the full predicate lines above, and `ENVELOPE end 02:01:34 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`. `b1_log_erasure.txt` through `keyed_env.txt` record analogous envelope brackets; `keyed_build_order.txt` records end `02:04:02 ... unchanged`; corrected `b3_module_read.txt` records end `02:05:05 ... unchanged`; final `keyed_argv_shape.txt` records end `02:06:55 ... unchanged`. These strings are copied from the receipts, not reconstructed measurements.

No tool was installed or updated.

VERDICT: forged-fences-13-r45-forged-pass-13
