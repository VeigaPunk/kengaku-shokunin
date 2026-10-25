# R31FxClaimsOrder — freeze vs. data ordering (round 31, wave 2)

Scout: L1Kengaku31.R31FxClaimsOrder. Question: verify the freeze preceded the data for the
round-31 claims (plans/round-31-claims.md). Read-only investigation; no production edits.

## 1. Commit that first carries `plans/round-31-claims.md`

Command: `git rev-list --all --format='%H %ci' -- plans/round-31-claims.md` (and
`git log --all --diff-filter=A -- plans/round-31-claims.md`).

Only four commits in all refs (incl. `refs/jj/keep/*`) ever contain the path, all created in the
landing minute, all carrying the **identical** blob `41a4bd1f4ad9089dc4d93c71c090a740a77caa96`:

| commit | time (commit date) | note |
|---|---|---|
| `7f8c286c37452e175dc08586316cdb58cf416ee7` | **2026-10-25 06:01:13 -0300** | **first carrier** (jj keep/snapshot; contains claims file, no receipts/build files) |
| `164a23f64c7ae46bc996fd06214efc5bc474caca` | 2026-10-25 06:01:13 -0300 | snapshot; adds receipts + artifacts |
| `57959c141a266b9710ba2820bd1d17f20ce84413` | 2026-10-25 06:01:14 -0300 | snapshot |
| `dbb0736459e0540a169a6d421ec6231734547378` | 2026-10-25 06:01:14 -0300 | **landed** round-31 commit (master HEAD) |

Parent of all four is the baseline `0883e72…` (2026-10-25 05:05:22 -0300). The claims file is
absent from the baseline tree (`git cat-file -e 0883e72:plans/round-31-claims.md` → fatal, MISSING).
So the freeze entered Version control only at 06:01:13, i.e. in the same minute as the landing and
~16 min after the first wave-1 artifact was written (see §3).

On-disk birth: `stat -c '%w %y' plans/round-31-claims.md` → birth **2026-10-25 05:45:26.202259825
-0300**, mtime identical (file never modified after creation). Current sha256
`2a4d89ec...8ad717` equals the committed blob (verified via `git cat-file`).

## 2. Timestamps: first wave-1 seat report and first landed production change

- First wave-1 seat report: `.ufo/waves/round-31/build/R31SrcS092a.md` (seat "leaf scout", S092
  Harbor `VerifierConfig.environment_mode`) — mtime **2026-10-25 05:51:08.988839307 -0300**
  (`find .ufo/waves/round-31 -type f -printf ... | sort`). 36 `build/R31*.md` seat/build reports
  exist, all written 05:51:08–06:00:21. Earlier wave-1 data: `claims/census-before.txt` 05:45:14,
  `claims/defects-before.txt` 05:45:56, `adoption-expect.json` 05:46:00, `claims/gate-before.txt`
  05:46:01, assimilation rows 05:46:04+.
- First landed production change: `git log --format='%H %ci %s' -1 dbb07364` →
  `dbb0736459e0540a169a6d421ec6231734547378 2026-10-25 06:01:14 -0300 round-31: verifier execution
  model entry, R1-R10 closure, citation-bound adoption gate` (master HEAD). It is the *only*
  commit between baseline and now; `git log --all --since='2026-10-25 05:05:23'
  --until='2026-10-25 06:01:10'` is empty and no jj keep ref exists between 05:05:22 and
  06:01:13 — the entire wave-1 output (receipts, seat reports, production changes) sat uncommitted
  until the landing minute.

## 3. Receipts under `.ufo/waves/round-31/claims/` vs. the claims commit

All four receipts **predate** the first claims commit `7f8c28` (06:01:13):

| receipt | birth | last mtime |
|---|---|---|
| `census-before.txt` | 05:45:14.050 | 05:45:14.177 |
| `defects-before.txt` | 05:45:56.905 | 05:45:56.942 |
| `control-nothing.txt` | 05:46:00.105 | 06:00:14.723 |
| `gate-before.txt` | 05:46:01.949 | 05:46:02.029 |

`census-before.txt` predates even the claims text's disk birth (05:45:26) by 12 s. The three
receipts named in the claims file as "control (committed at freeze)" (`control-nothing.txt` C1,
`defects-before.txt` C2, `gate-before.txt` C3; claims file lines 39, 65, 92) all postdate the
claims text's birth but predate its first commit.

## 4. Edits to the claims file after the commit

`git log -p --follow -- plans/round-31-claims.md` shows exactly the four commits of §1, all with
the identical blob; the empty snapshot child `ad30d10…` (06:01:14) changes no files
(`git show --name-only ad30d10` → nothing). On-disk content equals the committed blob. → **No
edits after the first commit** (nor between first snapshot and landing — content was final at
06:01:13).

## 5. Ordering analysis

Freeze vs. data on **disk**: claims text born 05:45:26 < all 36 seat reports (05:51:08+) and the
three named control receipts (05:45:56–05:46:02); census-before (05:45:14) is the sole exception,
12 s earlier.

Freeze vs. data in **git**: the freeze first entered version control at 06:01:13, i.e. ~6 min
after the first seat report and ~16 min after the first receipt, in the same minute as the landing.
Git does not show any committed freeze prior to the wave-1 data; the only evidence of ordering is
the machine-local inode birth time, which is not replicated/immutable.

## VERDICT
Survived: the claims text existed on disk (05:45:26) before any seat report (05:51:08) and before
its three named control receipts, and was never edited after its first commit (blob stable across
all four carriers and on disk). Fell: the freeze was not committed before the data — `plans/round-31-claims.md`
first enters git at 06:01:13 (`7f8c28…`, same minute as the landing `dbb07364…`), ~16 min after
the first receipt and ~6 min after the first wave-1 seat report (`build/R31SrcS092a.md`, 05:51:08);
`claims/census-before.txt` (05:45:14) predates even the claims text's birth; the entire round-31
wave-1 output and the claims share one atomic landing minute with no intermediate commits, so the
claims file's own statement "Frozen BEFORE any wave seat ran" (line 5) is verifiable only through
local inode times, not through commit history.
