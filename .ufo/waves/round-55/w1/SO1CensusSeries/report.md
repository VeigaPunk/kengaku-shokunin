# SO1CensusSeries — report

Seat: `SO1CensusSeries` · round 55 wave 1 (v2, build+attack) · lane
`kengaku-shokunin` · date 2026-10-30 (UTC).

## What this seat did

Ran the frozen `CORPUS.md` §Census command block (the "contract v1" manual census, seven
command lines) twice — once on a clean tree at the round's base tip
`798f5e9ef30ef39291295565209b65a17343c00e`, once on the working tree as it stands — and
pasted both blocks with their command lines and exit codes. The maintained
`scripts/sources-census.sh validate` CLI was deliberately **not** run, per seat scope
("the raw commands only, so the series is comparable").

Two extra read-only data points were added so the delta is attributable rather than
merely stated: a clean tree at HEAD (`80afa613`, the claims freeze) and a landing
simulation (HEAD tree + the working tree's `corpus/SOURCES.md`, but without the
untracked knowledge entry).

## Frozen numbers

| leg | base `798f5e9e` (clean tree) | working tree now | delta |
|---|---|---|---|
| rows | 193 | 195 | +2 (S201, S202) |
| malformed rows | 0 | 0 | 0 |
| tier histogram | `A=164 B=24 C=5` | `A=166 B=24 C=5` | +2 A |
| status histogram | `mined=172 queued=8 rejected=13` | `mined=174 queued=8 rejected=13` | +2 mined |
| duplicate ids | (empty) | (empty) | none |
| enum violations / tier inflation | (empty) | (empty) | none |
| mined-used-by missing paths | (empty) | (empty) | none (see D1) |

Intermediate point: the clean HEAD tree (`80afa613`) is census-identical to base —
193 rows, `A=164 B=24 C=5`, `mined=172 queued=8 rejected=13`, all four "print nothing"
legs empty. `corpus/SOURCES.md` is byte-identical between base and HEAD
(sha256 `82e2228c4674143b56cd3af7c6494a0a7a8f1b0c28d12987711513478687f4f1`), so the
whole +2 row delta is the uncommitted round-55 C3 pair.

## Commands run (all exit codes observed)

| # | command | exit |
|---|---|---|
| 1 | `cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && git archive 798f5e9ef30ef39291295565209b65a17343c00e \| tar -x -C /fast/scratch/hyaku/kengaku-r55/SO1CensusSeries/base` | 0 |
| 2 | same, `git archive 80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb \| tar -x -C …/head` | 0 |
| 3 | `cp -a …/head …/landsim && cp <lane>/corpus/SOURCES.md …/landsim/corpus/SOURCES.md` | 0 |
| 4 | `awk '/^### Census — run from the lane root/{f=1} f&&/^```sh/{s=1;next} s&&/^```/{exit} s&&!/^#/{print}' /home/vgpnk/Projects/shokunin/CORPUS.md > cmds.sh` | 0 (7 lines) |
| 5 | `…/run-census.sh …/base cmds.sh` | 0 (all 7 legs exit 0) |
| 6 | `…/run-census.sh /home/vgpnk/Projects/shokunin/kengaku-shokunin cmds.sh` | 0 (all 7 legs exit 0) |
| 7 | `…/run-census.sh …/head cmds.sh` | 0 (all 7 legs exit 0) |
| 8 | `…/run-census.sh …/landsim cmds.sh` | 0 (all 7 legs exit 0; leg 7 prints 2 lines) |
| 9 | `sha256sum corpus/SOURCES.md` vs `git show 798f5e9e…:corpus/SOURCES.md \| sha256sum` | 0 (identical for base export) |
| 10 | `git diff --stat 798f5e9e… 80afa613 -- corpus/` | 0 (empty ⇒ SOURCES.md unchanged base→HEAD) |
| 11 | `git ls-files --error-unmatch` over the 37 distinct mined `used-by` paths | 0 |
| 12 | id-contiguity check (`awk` over sorted ids) | 0 |

Read-only git only: `archive`, `show`, `rev-parse`, `status`, `diff`, `ls-files`. **No**
mutating git/jj command was run anywhere — no `add`/`commit`/`push`/`stash`/`checkout`/
`reset`. No network calls. No tool installs. No writes outside this seat's wave dir and
the seat scratch root.

## Files written

- `.ufo/waves/round-55/w1/SO1CensusSeries/census-series.txt` — the deliverable: both
  census blocks verbatim (with command lines and exit codes), the HEAD intermediate
  point, the landing-simulation block, the three-line delta summary, the findings, and
  the command/exit-code table.
- `.ufo/waves/round-55/w1/SO1CensusSeries/report.md` — this file.
- `.ufo/waves/round-55/w1/SO1CensusSeries.md` — the scoped findings for the `Report:`
  trailer.

Nothing else was written. The scratch root
`/fast/scratch/hyaku/kengaku-r55/SO1CensusSeries/` was deleted after the receipts were
copied into the deliverable.

## Defects found

- **D1 — landing ordering (blocks the frozen mined-used-by leg at the landing
  revision).** `corpus/knowledge/tb2-chess-best-move-grader.md` is **untracked** in the
  working tree (`git status` → `?? corpus/knowledge/tb2-chess-best-move-grader.md`) yet
  it is the `used-by` target of both new rows S201 and S202. It is the only one of the
  37 distinct mined `used-by` paths in the registry that is not git-tracked. The
  working-tree census passes leg 7 only because the file is present on disk. A landing
  revision that commits `corpus/SOURCES.md` without the knowledge entry prints
  `missing: corpus/knowledge/tb2-chess-best-move-grader.md` twice — reproduced in block
  (d) of the deliverable (the leg's contract is "print nothing"; it still exits 0).
  **Action for L1:** land `corpus/knowledge/tb2-chess-best-move-grader.md` in the same
  commit as, or before, the SOURCES rows.
- **D2 — pre-existing id-sequence gaps (not a round-55 regression, reported not
  fixed).** Source ids skip S087–S089, S095–S096 and S098–S099 (195 rows, max S202).
  The identical gaps are present at base (193 rows, max S200), so this is historical.
  The frozen census block does not test id contiguity, so it is invisible to the census.
- **D3 — context (not a defect).** The round's before-receipt
  `.ufo/waves/round-55/claims/census-before.txt` is the output of the **maintained CLI**
  (`scripts/sources-census.sh validate`): it ends with `kengaku ok …/corpus/SOURCES.md`
  and lists 13 `W04 duplicate url` warnings. The frozen manual census block has no
  duplicate-URL leg, so the two artifacts are not directly comparable. This seat's
  series is the manual-census series only, as scoped.

## Honest limits / dead ends

- **Shared-`/tmp` side effect (self-reported).** While debugging my fence-splitting
  verification script I ran a throwaway `awk` test whose output path was
  `/tmp/f1.txt`; it wrote 4 bytes (`a\nb\n`) into that path. `/tmp` is shared on this
  host and other seats use `f*.txt` names, so if a sibling seat had a `/tmp/f1.txt` it
  was overwritten by my debug write. No lane file, no scratch of another seat's
  registered directory, and no `.ufo/` path was affected. I did not touch
  `/tmp/f2.txt` (verified unchanged: 1491 bytes, mtime Aug 27). My own `/tmp`
  leftovers (`f1.txt`, `fence-test.txt`, `so1*.txt`) were removed.
- The base tree is a `git archive` export rather than a `git clone --shared`: the seat
  contract forbids mutating git commands (`checkout`/`reset`/`worktree add` are
  mutating), and the census commands need only the file tree. Fidelity was verified
  explicitly (base export `corpus/SOURCES.md` sha256 == the base blob sha256), and the
  export contains no untracked files, so it is a faithful clean tree at the base tip.
  `[INFERENCE]` the census output is independent of `.git` presence, so this is
  equivalent to a clean clone for these seven commands.
- The `census --validate` CLI was **not** run (seat scope). No statement is made here
  about the CLI's own verdict on either tree.
- No claim was scored and no axis was moved by this seat; the deliverable is a
  measurement receipt only. The coverage-axis score stays L0-capped at 7 per
  `plans/round-55-claims.md` regardless of what this census shows.
- The working-tree block reflects the tree as of 2026-10-30T15:47:17Z; sibling seats
  landing changes to `corpus/SOURCES.md` after that timestamp are not reflected.
