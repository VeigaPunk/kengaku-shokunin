# R46W2Census — census falsification

- Measured lane revision: `42d5043afac952fcb43bf4798757785dd258cf85` (assigned TIP; verified by `git rev-parse HEAD` in setup).
- Validate command: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh /fast/scratch/hyaku/kengaku-r46/R46W2Census/env /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
- Validate exit: **0**. Full output, including envelope lines: [receipt](R46W2Census/census-at-tip.txt). Envelope ended `exit=0 ... unchanged`; output consists of 15 W04 duplicate-URL warnings (S040, S048, S057–S059, S064–S069, S071, S075–S076, S100) and `kengaku ok .../corpus/SOURCES.md`. This matches `claims/census-before.txt` exactly: same W04 rows, ok line and `exit=0`.
- Row-count commands use `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\\| *S[0-9]{3}'`. Before (round baseline `64ba8385ea10af1b78d367dcb242b92d97062af7`): **149**. After (TIP `42d5043afac952fcb43bf4798757785dd258cf85`): **165**. Difference: +16 row-shaped registry lines. The immediate TIP parent `85a40be5333e7210fe7acf44637010bc621bd007` also counts 165 (the final two commits are bookkeeping/results, not row additions).

VERDICT: census-exit-0-rows-149-to-165
