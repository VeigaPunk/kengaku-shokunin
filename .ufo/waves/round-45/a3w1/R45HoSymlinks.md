# R45HoSymlinks — held-out link probes

Measured lane tip: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD`). Landed fence copy SHA-256: `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`.

Hostile module: `R45HoSymlinks/link_hostiles.py` (five fixtures). Detector: counter `build_module` builder from `plans/round45_c1_verify.py`, followed by its `run_fence` under strace; a successful ADMIT or any successful open outside fixture d is a finding. This module was run directly against the copied landed fence.

Measured command:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh /fast/scratch/hyaku/kengaku-r45/R45HoSymlinks/env /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoSymlinks/run_probe.py /fast/scratch/hyaku/kengaku-r45/R45HoSymlinks/env/w2`

Actual output:
```text
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45HoSymlinks/env /fast/scratch/hyaku/kengaku-r45/R45HoSymlinks/env --bind /fast/scratch/hyaku/kengaku-r45/R45HoSymlinks/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoSymlinks/run_probe.py /fast/scratch/hyaku/kengaku-r45/R45HoSymlinks/env/w2
ENVELOPE start 00:34:26 cwd=/home/vgpnk/Projects/shokunin
FENCE sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
FENCE-RUN link-objects-symlink-out ADMIT opens=8
FENCE-RUN link-git-symlink-in BREACH opens=0 -- lane/.git/.git is a symlink
FENCE-RUN link-claims-symlink-out BREACH opens=0 -- --claims value 'lane/claims.md' resolves outside the fixture
FENCE-RUN link-objects-hardlink-out ADMIT opens=0
FENCE-RUN link-include-chain-in BREACH opens=0 -- lane/.git/config carries an include
SUMMARY modules=1 fixtures=5 admitted=2 read=1 errors=0
ENVELOPE end 00:34:28 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
COMMAND_EXIT=0
```

Findings: `.git/objects` symlinked to the module build root outside `d` was ADMIT with 8 outside opens (strong fence defect). Hardlinked object files into an outside store were ADMIT with zero outside opens; this is not an open-path escape and is recorded as a coverage result, not an additional defect. `.git` symlink resolving inside d, external claims symlink, and an include chain were refused with zero outside opens. `link-claims-symlink-out` points to a claims file outside d; factored argv resolution detects it before opening it.

Two earlier envelope attempts were inconclusive setup failures (missing generated harness; then indentation error), not detector results. Each output recorded unchanged PATH-directory digest; the successful result above is valid. No tools installed.

Scratch cleanup: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r45 R45HoSymlinks /fast/scratch/hyaku/kengaku-r45/R45HoSymlinks` (run after report write).

VERDICT: link-modules-5-admitted-2-read-1