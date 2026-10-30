# SO1CensusSeries — scoped findings

Round 55 wave 1 (v2, build+attack). Lane `kengaku-shokunin`, 2026-10-30 UTC.
Item: the frozen `CORPUS.md` §Census numbers, before vs working-tree-now.

## Numbers (frozen manual census, `CORPUS.md:131-148`, all legs exit 0)

| leg | base `798f5e9e` clean tree | working tree now | delta |
|---|---|---|---|
| rows | 193 | 195 | +2 (S201, S202) |
| malformed | 0 | 0 | 0 |
| tiers | `A=164 B=24 C=5` | `A=166 B=24 C=5` | +2 A |
| statuses | `mined=172 queued=8 rejected=13` | `mined=174 queued=8 rejected=13` | +2 mined |
| duplicate ids | empty | empty | — |
| enum violations / tier inflation | empty | empty | — |
| mined-used-by missing paths | empty | empty | — (see D1) |

Attribution: the clean tree at HEAD `80afa613` is census-identical to base
(`corpus/SOURCES.md` byte-identical, sha256 `82e2228c…`), so the entire +2 is the
uncommitted round-55 C3 pair S201/S202, both tier A / status mined. No tier-mix or
status-mix shift; all four "must print nothing" legs stay empty in both blocks.

Full blocks with command lines and exit codes:
`.ufo/waves/round-55/w1/SO1CensusSeries/census-series.txt`.

## Finding the L1 must act on

- **D1 (landing ordering).** `corpus/knowledge/tb2-chess-best-move-grader.md` is
  **untracked** in the working tree but is the `used-by` target of both S201 and S202
  (the only untracked path among the 37 distinct mined `used-by` paths). The
  working-tree census passes the mined-used-by leg only because the file exists on disk.
  A landing revision that commits the SOURCES rows without that entry prints
  `missing: corpus/knowledge/tb2-chess-best-move-grader.md` twice (reproduced in the
  deliverable's block (d); the leg still exits 0). Land the knowledge entry in the same
  commit as, or before, the SOURCES rows.
- **D2 (pre-existing, not a round-55 regression, not fixed by me).** Source-id gaps at
  S087–S089, S095–S096, S098–S099 exist identically at base; invisible to the frozen
  census block.
- **D3 (context).** `.ufo/waves/round-55/claims/census-before.txt` is the *maintained
  CLI* output (`scripts/sources-census.sh validate`, 13 `W04 duplicate url` warnings),
  not the frozen manual census; the two are not directly comparable. Per seat scope the
  CLI was not run here.

## Scope compliance

Read-only git only (`archive`, `show`, `rev-parse`, `status`, `diff`, `ls-files`); no
mutating git/jj command anywhere; no network; no installs; no writes outside
`.ufo/waves/round-55/w1/SO1CensusSeries/`, `.ufo/waves/round-55/w1/SO1CensusSeries.md`
and the seat scratch (deleted before yield). Files written: the deliverable
`census-series.txt`, `report.md`, and this file. Nothing else touched.
