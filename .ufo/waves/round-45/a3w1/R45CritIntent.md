# R45CritIntent — fixture fence intent audit

Measured lane: `master` / `HEAD` `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` → that hash). No lane files changed. Scratch: `/fast/scratch/hyaku/kengaku-r45/R45CritIntent`.

## Findings

1. **Brace-prefix bypass for non-lane path arguments.** `fixture_fence.py:103-110` skips *all* path validation whenever a value starts with `{`; unlike `--lane`, `--claims`, `--receipt`, and anchor `--evidence-ref` do not receive a later `_inside` check. In the envelope experiment, the same order argv shape with `--claims ../../etc` returned `BREACH --claims value '../../etc' resolves outside the fixture`, while `--claims {T}/../../etc` returned `ADMIT`. This is a real verdict change from one argument-string special case; the counter’s `run_fence` passes the serialized argv verbatim to the harness (`round45_c1_verify.py:174-230`), so this tested fence invocation does not itself resolve `{T}`. The fence comment says the harness resolves the placeholder, but that is not true of this call path. Smallest safe correction: resolve/validate the complete placeholder-expanded path in the fence (or remove the carve-out); do not treat a leading `{` as proof of containment.

2. **Uninspected symlinked Git-store descendants are admitted.** `_collect` prunes each real `.git` directory at lines 130-139, then fact 5 checks only named markers/config; it does not reject symlinks such as `.git/objects`. An envelope-built repo whose `.git/objects` was moved to `lab/fx/stash_objects` and replaced by a symlink returned `ADMIT`; same when the store was moved to `outside_objects/store`. In the captured `strace` for the first case, successful reads include `.git/objects/d3/...` and `.git/objects/41/...` (receipt `R45CritIntent/exp-receipt.txt` documents verdict; scratch trace was inspected before cleanup). This contradicts the documented self-contained-store intent. Smallest safe correction: during collection, inspect every entry below `.git` without following symlinks and refuse symlinks/special files or any resolved target outside the fixture. Note: the C1 counter’s region rule only attributes paths under its `root/fx` and `root/btmp` regions; it does not establish that a relative `.git/objects/...` open resolves within the fixture.

## Requested intent checks

- **Fids / module filenames:** no references to fixture IDs or module filenames occur in `fixture_fence.py`; its public function takes only `(d, argv, tool)`. Measured rename control: envelope experiment A returned `ADMIT` for `fx/mod_h/f000`; A2 copied the identical tree to `fx/refusals45_f1_gitfile/f000` and returned `ADMIT`. B gave the deliberately hostile separate-git-dir tree a battery-family path and returned `BREACH .git/.git is a file (gitdir redirect), not a directory`. Thus paths/labels do not determine the decision; tree/argv do. (This is a directory-label control; fids are not inputs to `breach` at all.)
- **Hardcoded 10 fids / 104 honest shapes:** none in the fence. It has general structural checks and bounded constants; the 10/104 totals and module list are in the frozen counter, not the fence.
- **`--lane` strings:** it is parsed as a path, not matched against named lane strings. The leading-`{` carve-out is generic and `--lane` is subsequently checked with `_inside`; envelope experiment E showed `--lane {T}/../../etc` returns `BREACH --lane resolves outside the fixture`. The carve-out is still unsafe for other path-valued options (finding 1).
- **Timing:** fence uses per-git-call `GIT_TIMEOUT = 30`; counter wraps a whole fence call in `FENCE_TIMEOUT = 120` and maps expiry to HUNG. This is a fail-closed latency tradeoff, not a tolerance that admits a timed-out fence. Experiment with copied source patched to `GIT_TIMEOUT = 0.001` still returned `ADMIT` for the fast fixture, so I did not observe a timing flip. Worst-case duration can exceed the counter’s 120-second bound across multiple sequential probes; the counter then records HUNG, not ADMIT.
- **`breach()` purity:** repeated calls on each of the honest and symlinked fixtures returned the same verdict (honest `ADMIT` twice; symlink case `ADMIT` twice). It is deterministic for stable filesystem/process conditions, but not a pure function in the strict sense: it reads live filesystem state, spawns Git, and has a 30-second wall-clock timeout, so environmental changes or scheduling can change the answer. No nondeterministic verdict was observed in these repeats.

## Measured command and envelope output

Command:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh /fast/scratch/hyaku/kengaku-r45/R45CritIntent/env bash /fast/scratch/hyaku/kengaku-r45/R45CritIntent/exp.sh`

Captured `R45CritIntent/exp-receipt.txt` envelope lines:
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45CritIntent/env /fast/scratch/hyaku/kengaku-r45/R45CritIntent/env --bind /fast/scratch/hyaku/kengaku-r45/R45CritIntent/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- bash /fast/scratch/hyaku/kengaku-r45/R45CritIntent/exp.sh
ENVELOPE start 00:31:32 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 00:31:35 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```
Key output, from that command:
```
A ADMIT
A2 ADMIT
B BREACH .git/.git is a file (gitdir redirect), not a directory
C ADMIT
D ADMIT
-- --claims ../../etc : BREACH --claims value '../../etc' resolves outside the fixture
-- --claims {T}/../../etc : ADMIT
-- --lane {T}/../../etc : BREACH --lane resolves outside the fixture
GIT_TIMEOUT = 0.001; ADMIT
```
Receipt path is relative to lane: `.ufo/waves/round-45/a3w1/R45CritIntent/exp-receipt.txt`.

The initial run (argv-construction bug) was discarded and is not used as evidence. No tools installed.

VERDICT: fence-intent-clean-no-findings-2
