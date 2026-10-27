# R45HoConfigKeys — config-key probe

Lane measured: `master` = `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (fresh scratch clone verified by `git -C "$S/lane-a3" rev-parse --show-toplevel` = `$S/lane-a3`). The landed fence SHA-256 was `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`; round-44 builder SHA-256 was `6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad`.

## Mutant / detector

Hostile module: `configkeys.py`, SHA-256 `72c98faed9637d779ed6ae01668ae7494786d444e30dfa0c631b202b574b5dab`, stored in this seat's a3w1 directory. It creates a regular `outside-attributes` file beside its fixture directory (inside the module build root), then configures `[core] attributesFile = <that outside file>` in the fixture repository's `.git/config`.

Expected detector: import the pinned round-44 builder and round-45 counter `build_module`, then run the copied landed `fixture_fence.py` through `round45_c1_verify.py`'s `run_fence` (bwrap + strace open/openat/openat2/creat), and separately use `git check-attr` to determine whether Git honors the setting.

## Measured command and output

Command:

```sh
S=/fast/scratch/hyaku/kengaku-r45/R45HoConfigKeys
mkdir -p "$S/w-a5"
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoConfigKeys/probe.py "$S/lane-a3" "$S/w-a5" /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoConfigKeys/configkeys.py
```

Output:

```text
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45HoConfigKeys/env /fast/scratch/hyaku/kengaku-r45/R45HoConfigKeys/env --bind /fast/scratch/hyaku/kengaku-r45/R45HoConfigKeys/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoConfigKeys/probe.py /fast/scratch/hyaku/kengaku-r45/R45HoConfigKeys/lane-a3 /fast/scratch/hyaku/kengaku-r45/R45HoConfigKeys/w-a5 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoConfigKeys/configkeys.py
ENVELOPE start 01:09:29 cwd=/home/vgpnk/Projects/shokunin
FIXTURE config-core-attributes-file-outside /fast/scratch/hyaku/kengaku-r45/R45HoConfigKeys/w-a5/fx/R45HoConfigKeys-configkeys/f000
FENCE ('ADMIT', '', 0)
TOOL_CHECK_ATTR rc=0 stdout=marker: hostile: outside stderr=
ENVELOPE end 01:09:31 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

## Result

The fence **admits** the fixture and records zero outside opens for its own decision; it does not inspect `core.attributesFile`. The Git behavior probe returns `marker: hostile: outside`, demonstrating that Git honors the external attributes file when attributes are queried. This is a concrete admitted-config-key gap: the key is not inert for Git generally, though this fence's limited rev-parse/config/cat-file legs did not read it. Earlier runner attempts failed before the decision (`FileExistsError` for reused `empty`/`fx` scratch dirs, then missing `harness.py`); they are setup failures, not measurements. The successful run above used a fresh work root and completed with envelope integrity unchanged.

VERDICT: configkey-modules-1-admitted-1-read-0
