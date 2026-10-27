# R46CritC1SealConfig

Base commit: `64ba8385ea10af1b78d367dcb242b92d97062af7`. Candidate modules were built and tested using the round-45 held-out driver (which calls `build_module` and `run_fence`) against a clone checked out at that commit. Three candidates admitted; non-admitted exploratory candidates were discarded. No fence-writing seat module or round-46 C1 counter was consulted.

- core-excludes-file fixture — LEAKED.
- url-insteadof-path fixture — LEAKED.
- core-attributes-path fixture — LEAKED.

Command: `envelope.sh "$S/env" python3 .../R45HoCommondir2/driver.py "$S/lane" "$S/work" "$S/mods"`.

Output: `FENCE ... sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`; `FENCE-RUN g1_excludes.py sealed-core-excludes-file ADMIT opens=0`; `FENCE-RUN g2_url.py sealed-url-insteadof-path ADMIT opens=0`; `FENCE-RUN g3_attributes.py sealed-core-attributes-path ADMIT opens=0`; corresponding `HELDOUT ... LEAKED fixtures=1 admitted=1 hung=0 opens=0`. The redundant fourth scratch probe failed to build because it attempted to reuse the destination; it is not retained or counted.

Envelope:
```
ENVELOPE start 02:02:17 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 02:02:21 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Retained files: `.ufo/waves/round-46/w1/R46CritC1SealConfig/sealed/` (three modules, `SHA256SUMS`, and mechanism notes in `NOTES.md`).

VERDICT: sealed-config-3-base-leaked-3-read-0
