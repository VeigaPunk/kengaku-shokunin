# R46CritC1SealArgv — sealed argv modules

Axis: calibration. Tested the frozen base `64ba8385ea10af1b78d367dcb242b92d97062af7` using `build_module` and `run_fence` from the round-45 counter through the local driver. Base fence digest: `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`.

Per-module base-fence outcomes:
- `newline_anchor.py` — LEAKED.
- `phantom_anchor.py` — LEAKED.
- `phantom_order.py` — LEAKED.

Measured command:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh /fast/scratch/hyaku/kengaku-r46/R46CritC1SealArgv/env /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46CritC1SealArgv/driver.py /fast/scratch/hyaku/kengaku-r46/R46CritC1SealArgv/lane /fast/scratch/hyaku/kengaku-r46/R46CritC1SealArgv/run2 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46CritC1SealArgv/sealed`

Observed output: all six fixtures returned `ADMIT`, `opens=0`; each module roll-up was `LEAKED fixtures=2 admitted=2 hung=0 opens=0`. The harness's module verdict defines ADMIT/ERROR as admitted. Envelope receipt: `ENVELOPE start 02:02:44 cwd=/home/vgpnk/Projects/shokunin`; `ENVELOPE end 02:02:48 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`.

Digests are recorded in `sealed/SHA256SUMS`; mechanism notes are in `sealed/NOTES.md`. Scratch removed with `scratch_guard.py safe-rm`; output: `DELETE path=/fast/scratch/hyaku/kengaku-r46/R46CritC1SealArgv resolved=/fast/scratch/hyaku/kengaku-r46/R46CritC1SealArgv bytes=549805251 size=524.3MiB`.

VERDICT: sealed-argv-3-base-leaked-3-read-0
