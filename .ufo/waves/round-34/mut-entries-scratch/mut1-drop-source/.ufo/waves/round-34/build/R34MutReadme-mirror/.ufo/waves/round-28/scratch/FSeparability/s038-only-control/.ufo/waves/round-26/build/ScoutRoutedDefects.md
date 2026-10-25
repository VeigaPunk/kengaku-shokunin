# Round-25 routed-defect and number sweep

Scope: read-only audit of base `f11bffbf9caa9c9e286fb32c568b81b97719656a`; diff `6180e4f..f11bffbf` for SCORECARD.md, PROVINCE.md, SKILL.md, corpus/README.md, LOG.md. Judged axis: calibration.

## Routed defects verified

- `SCORECARD.md:558`: current capability token `14 checks` is stale; true is **18 checks**. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show f11bffbf:corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt | grep '^selftest:'` → `selftest: 18 checks, 0 failed`. The v1 receipt records 14, so that value is the initial-run output, not the revised capability.
- `SCORECARD.md:559`: current base `mismatch=11` should be **10** under registered P2. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show f11bffbf:corpus/evidence/round25-calibration/state-check-before-6180e4f-v2.txt | grep '^assertions='` → `assertions=241 match=228 mismatch=10 superseded=0 offline_unverifiable=3`. v1 really printed 11; the later correction is `SCORECARD.md:719` (`mismatch=10`).
- `PROVINCE.md:119`: `37 after round 25` should be **42**. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show f11bffbf:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3,} *\|'` → `42`; `round25-census-after.txt` reports `sources_rows=42`, `sources_new_rows_r25=16` (S027–S042).

## Additional round-25-added text inventory drift

- `corpus/README.md:167` describes the `round25-sources` directory only through `S037`; its committed `gate.md` has later addenda for **S038–S042** (lines 36, 44–47), and the census counts 16 new rows, S027–S042. The listed range is a true subset, but as a directory-contents inventory it is incomplete; use `S027–S042` if intended exhaustive.
- `corpus/README.md:182` lists the claims file as `+ Amendment 1`; committed `plans/round-25-claims.md` has **2** amendments (`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show f11bffbf:plans/round-25-claims.md | grep -c '^## Amendment'` → `2`). This is likewise an incomplete contents description, not a false statement that Amendment 1 exists.

## Disambiguation and sweep remainder

- The repeated `mismatch=11` at `SCORECARD.md:668` and `LOG.md:286` records the v1 run; v1 receipt confirms 11, while the v2 P2 receipt above establishes the corrected base value 10. `LOG.md:304–305` records the correction. These are historical snapshots, unlike the current capability cell at :559.
- Other checked measurements agree with committed receipts: v1/v2 summaries both report 119 stored checks, 35 estimates and the same transition counts; v2 revises PASS 12→7 by removing five non-firing specificity verdicts. The power table supports 17/26/34 for 0/1/2 errors at bar 0.80. Committed wave report counts are 92 build and 87 falsify (`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree -r --name-only f11bffbf .ufo/waves/round-25/build | grep -E '^\.ufo/waves/round-25/build/[^/]+\.md$' | wc -l` → 92; same command with `build` replaced by `falsify` → 87).
- Adjacent unchanged R24 assertions `SCORECARD.md:557` and `PROVINCE.md:112` still say 25 registry rows; base census says 26. They are outside the specified added-text diff; the newly added R25 correction correctly records 26 at base.
- `lsp` is not mounted in this session. Git diff/show and grep were used only as literal text/receipt evidence, not semantic-reference proof. No installs.

VERDICT: Three routed defects confirmed; two additional README inventory descriptions are incomplete; no other numeric disagreement found in the requested added-text sweep. Installs: none.