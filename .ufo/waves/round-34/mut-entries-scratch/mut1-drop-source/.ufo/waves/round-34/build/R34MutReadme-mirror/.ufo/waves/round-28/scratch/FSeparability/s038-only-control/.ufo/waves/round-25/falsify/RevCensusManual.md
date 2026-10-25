ATTACKS: Frozen SOURCES.md manual census at landed tip 8ea41f9ed

- Pristine copy: `git archive 8ea41f9ed` extracted to `/tmp/k25w2-RevCensusManual` (lane root). `corpus/SOURCES.md` SHA-256 matched `git show 8ea41f9ed:corpus/SOURCES.md`: `b9eb8ca643f06d73212b3da48b33f4ae79cc8396e4762871c5bee22470bf6ed1`.
- Ran the frozen commands in `CORPUS.md:134-147` from that copy's root.
- Rows (`grep -cE ...`): `37`.
- Malformed rows (`awk ... NF!=13`): `0`.
- Tier histogram: `A=34 B=1 C=2`.
- Status histogram: `mined=26 queued=8 rejected=3`.
- Duplicate IDs: no output.
- Enum violations / tier inflation: no output.
- Mined `used-by` paths missing from the pristine tree: no output.
- Installations/updates: none.

VERDICT: SURVIVES — Every requested frozen census check is clean against the exact landed-tip SOURCES.md and its corresponding tree.