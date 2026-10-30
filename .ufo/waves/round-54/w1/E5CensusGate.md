# E5CensusGate — round 54

## Assimilation id-collision receipt

The specified id extraction and `comm -12` pipeline produced 190 registry IDs, 175 staged IDs, and 114 collisions. The collision set is nonempty and exceeds 20; adoption is closed this round.

MASS-ID-DRIFT: adoption closed this round; L0 question owed

Top-5 colliding IDs: S077, S078, S079, S080, S081.

Receipts copied here: `reg-ids`, `staged-ids`, `collisions`.

## Census tooling receipt

See `census-mid.txt`: validation exited 0, final line was `kengaku\tok\t/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`, with 15 W04 warnings.

## Mini-registry guard proof

`mini-registry-proof.txt` records the command and output. A row with exactly three leading spaces and staged ID S077 was recognized by the same `^ {0,3}` extraction anchor and appeared in the `comm -12` collision output.

## Evidence and scope

Commands exercised: the assignment's exact three extraction/comm commands; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`; and the matching extraction/comm pipeline against the scratch mini-registry. No registry or external package file was modified. No tools installed. Scratch directory removed.
