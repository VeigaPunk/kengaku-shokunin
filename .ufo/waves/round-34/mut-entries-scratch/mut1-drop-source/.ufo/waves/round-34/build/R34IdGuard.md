# R34 id-collision guard

The assigned collision guard was executed before any registry append. `reg-ids` contains the sorted registry identifiers; `staged-ids` contains the sorted staged-package identifiers; `collisions` is their sorted intersection.

Command: `comm -12 reg-ids staged-ids | wc -l` (the equivalent pipeline wrote `assimilation/collisions`); output: `21`.

Exact colliding IDs (from `.ufo/waves/round-34/assimilation/collisions`): `S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S090 S091 S092 S093 S094 S097 S100 S101 S102 S103 S104`.

This collision is expected: staged package names S105/S106/S107 designate different documents from the lane's intended C1 artifacts, while the lane's new adopted rows S105–S109 continue the lane registry per CORPUS.md rule 2. The intersection identifies reuse in other staged ids too; do not append colliding package rows under their existing identifiers.

Fixture attack: `assimilation/id-guard-proof.txt` records the same extraction/intersection pipeline over an indented `  | S002 |` row on both sides. The produced `reg-ids` and `staged-ids` each contain `S002`; `collisions` contains `S002`; `COUNT=1`. Thus the 0–3 leading-space guard recognizes an indented row and fails closed on collision.

Evidence-producing command for the real collision inventory: `grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' <registry> | grep -oE 'S[0-9]+' | sort` and the same command on the staged file, followed by `comm -12 ...`; raw lists and intersection are retained in `.ufo/waves/round-34/assimilation/{reg-ids,staged-ids,collisions}`. Proof command output is retained verbatim in `assimilation/id-guard-proof.txt`.

VERDICT: id-guard-proven.
