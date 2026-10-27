# R46CritC1SealPaths — sealed filesystem-shape modules

All three modules were run using the round-45 counter's `build_module` and `run_fence` against a scratch clone checked out at `64ba8385ea10af1b78d367dcb242b92d97062af7`. Base commit verified by `git -C "$S/lane" rev-parse HEAD` → `64ba8385ea10af1b78d367dcb242b92d97062af7`; base fence digest: `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`.

## Evidence

Command: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh "$S/env" /usr/bin/python3 "$S/driver.py" "$S/lane" "$S/proof" /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46CritC1SealPaths/sealed`

Output:

```text
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46CritC1SealPaths/env /fast/scratch/hyaku/kengaku-r46/R46CritC1SealPaths/env --bind /fast/scratch/hyaku/kengaku-r46/R46CritC1SealPaths/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r46/R46CritC1SealPaths/driver.py /fast/scratch/hyaku/kengaku-r46/R46CritC1SealPaths/lane /fast/scratch/hyaku/kengaku-r46/R46CritC1SealPaths/proof /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46CritC1SealPaths/sealed
ENVELOPE start 02:02:57 cwd=/home/vgpnk/Projects/shokunin
FENCE sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
FENCE-RUN info_redirect.py sealed-info-redirect ADMIT opens=0
MODULE info_redirect.py LEAKED fixtures=1 admitted=1 hung=0 opens=0
FENCE-RUN pack_redirect.py sealed-pack-redirect ADMIT opens=6
MODULE pack_redirect.py LEAKED fixtures=1 admitted=1 hung=0 opens=6
FENCE-RUN refs_redirect.py sealed-refs-redirect ADMIT opens=4
MODULE refs_redirect.py LEAKED fixtures=1 admitted=1 hung=0 opens=4
ENVELOPE end 02:03:00 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

## Base-fence verdicts

- `info_redirect.py` — LEAKED.
- `pack_redirect.py` — LEAKED.
- `refs_redirect.py` — LEAKED.

Mechanism notes are sealed at `R46CritC1SealPaths/sealed/NOTES.md`; module integrity digests are in `R46CritC1SealPaths/sealed/SHA256SUMS`.

Scratch cleanup: `python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r46 R46CritC1SealPaths /fast/scratch/hyaku/kengaku-r46/R46CritC1SealPaths` → `DELETE path=/fast/scratch/hyaku/kengaku-r46/R46CritC1SealPaths resolved=/fast/scratch/hyaku/kengaku-r46/R46CritC1SealPaths bytes=549899832 size=524.4MiB`.

VERDICT: sealed-paths-3-base-leaked-3-read-0
