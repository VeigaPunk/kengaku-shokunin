# R34 mutation probe: README/knowledge parity

VERDICT: mut-readme (parity caught for frozen rows; new-row/file parity not caught by state_check)

## Detector baseline

Command: `python3 plans/state_check.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --summary`.
Output: `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`; `VERDICT: PASS — all comparable frozen assertions match`; exit 0. The command and output were observed on the lane before probing.

A 105M mirror was created under `.ufo/waves/round-34/build/R34MutReadme-work/`: lane files plus `.git` and `.ufo/waves/round-26`, excluding `.jj` and the very large `.ufo` tree. Its pristine detector output was identical: `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`; PASS; exit 0. Its initial `corpus/README.md` SHA-256 was `2b5d278c1e154b1a95a7cb2d57abfb5c52cc1f7a56c586f8985288d47c41e776`; knowledge directory contained 41 files.

## Patch + entries

Applied proposed patch blocks from `.ufo/waves/round-34/build/R34ReadmePatch/patch.md` and copied the proposed TB2/provider entries from `R34EntryTB2/entry.md` and `R34EntryProvider/entry.md` into the mirror only. Patch adds two index rows, coverage/frontier text; entries are `terminal-bench-task-grader.md` and `provider-selfreport-eval-limits.md`. The patched detector remained green: `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`; PASS; exit 0. It reported both new index rows and both new files as `OUT_OF_POPULATION` (four new disclosures); knowledge count 43. Patched-byte SHA-256 values:

- README: `d17da3721bcb0f6e460e5f64e6d6f5bf61a79ca41c24721f72ba9dc78afd2f9f`
- TB2 entry: `304312ad1c4a996dbd61387c22bd0373b468e920519eff8a20a3a8e04f50b298`
- provider entry: `224a64aa44e3eaf7ae64af6ab167de351238c616d5e39d7843f5dabd6647bf75`

## Mutants

1. **Delete an index row (frozen population):** removed the `knowledge/benchmark-selection.md` table row from the patched mirror. Command: `python3 plans/state_check.py --root "$W" --summary`. Output: `assertions=329 match=317 mismatch=1 superseded=6 offline_unverifiable=5`; `MISMATCH: P2e.file-to-row.knowledge/benchmark-selection.md:25 — {"exists": true, "indexed": false, "path": "knowledge/benchmark-selection.md", "row_lines": []}`; `VERDICT: FAIL — at least one frozen assertion mismatches`; exit 1. **Killed.**
2. **Delete a new landing row:** removed only the exact `| `knowledge/terminal-bench-task-grader.md` |` index row. Same detector: `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`; PASS; exit 0. **Survived**: the new landing row is outside state_check's frozen population.
3. **Add an unindexed file:** created `corpus/knowledge/r34-parity-probe-unindexed.md`. Same detector: `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`; PASS; exit 0, with `OUT_OF_POPULATION: P2e.out-of-population.file.knowledge/r34-parity-probe-unindexed.md`. **Survived**: state_check discloses but does not fail on an unindexed new file.

Supplementary N8 probe: while that file existed, ran the proposed `R34C2CounterDraft/round34_defects.py --lane "$W"`. It reported `DEFECT N8 knowledge-readme-bidirectional-parity: knowledge/index parity failure; missing rows=['r34-parity-probe-unindexed'], missing files=[], duplicate rows=[]` and `checks=8 defects=5`. N8 detected the mutation; the other four defects were N1/N3/N4/N7 because this lean mirror omitted their historical wave/report inputs. This was draft-counter evidence, not a clean counter run.

## Restoration

Removed the unindexed probe file and restored the patched README snapshot after each row mutation. Final detector: `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`; PASS; exit 0. Final SHA-256 values exactly match the patched values above; knowledge count returned to 43. No lane source files were modified.
