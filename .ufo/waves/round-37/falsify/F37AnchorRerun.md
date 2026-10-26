# F37AnchorRerun — anchor digest check, before/after recall and four mutants

Seat: F37AnchorRerun (executor, kengaku round 37 wave 2). Target: `plans/anchor_digest_check.py` as landed on
`357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`. All runs on throwaway clones under
`/fast/scratch/hyaku/kengaku-r37/F37AnchorRerun/` (deleted before this seat finished); lane never written.
Environment: `python3 -VV` → `Python 3.14.8 (main, Oct 2 2026) [GCC 16.2.1 ...]`. No tools installed (nothing needed).

Receipts in `.ufo/waves/round-37/falsify/F37AnchorRerun/`: `run-after-tip.txt`, `run-after-tip-index-ref.txt`,
`run-before-3ea9a1d9.txt`, `mutant-M1-erratum-deleted.txt`, `mutant-M2-erratum-digit-flipped.txt`,
`mutant-M3-S108-shortened.txt`, `mutant-M4a-S111-second-token-fabricated.txt`,
`mutant-M4b-S111-second-token-real-digest.txt`, `mutant-M5-S111-digest-substituted-real.txt`,
`mutant-tip-verbose.txt`,
`probe-index-manifest-mint.txt`.

## 1. After — clean clone of the tip (357deceb)

```
$ git clone -q --no-local …/kengaku-shokunin S/fx/lane && git -C S/fx/lane checkout -q 357deceb…
$ git -C S/fx/lane rev-parse --show-toplevel        # → /fast/scratch/…/fx/lane
$ cd S/fx/lane && python3 plans/anchor_digest_check.py --lane .
rows=107 tokens=15 defects=0
EXIT=0
```

`--evidence-ref index` on the same clean tree: `rows=107 tokens=15 defects=0`, `EXIT=0` — the docstring's claim
that index and head agree in a clean tree holds here (receipt `run-after-tip-index-ref.txt`).

`--verbose` (receipt `mutant-tip-verbose.txt`) resolves 14 tokens and shows the one exemption:
`EXEMPT S110 anchor=4f7ac05e…96f9c by=corpus/lessons/round-37.md:32 correction=4f7ac05e70cf9220ea0f…96f9c`.
S070/S072/S073/S074 resolve `via=corpus/evidence/round37/anchor-captures/SHA256SUMS`; S111/S112/S113 via
`corpus/evidence/round37/tb2-git-webserver/SHA256SUMS`; S114 via `…/round37/prior-art/SHA256SUMS`.

Manifest honesty spot-checked (this seat, not the tool): all five `anchor-captures/SHA256SUMS` lines hash to the
committed blobs beside them, e.g. `S070-generate_test_data.py listed=45ddba7be490 actual=45ddba7be490 OK bytes=838`.

## 2. Before — clean clone of 3ea9a1d9, tool copied in

Clone at `3ea9a1d9005cc07d0a5ce69f4ebf53a81fbcecdd` (round-36 verifier spot-check); `plans/` there has no
checker (`git status --porcelain` → `?? plans/anchor_digest_check.py` only), so the tip tool was copied in
byte-identical (`sha256(tool)` equal in both clones).

```
$ cd S/fx/before && python3 plans/anchor_digest_check.py --lane .
DEFECT S070  … class=digest-unknown … loc=corpus/SOURCES.md:92
DEFECT S072  … class=digest-unknown … loc=corpus/SOURCES.md:94
DEFECT S073  … class=digest-unknown … loc=corpus/SOURCES.md:95
DEFECT S074  … class=digest-unknown … loc=corpus/SOURCES.md:96
DEFECT S110 anchor token=4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c class=digest-short detail=63-hex loc=corpus/SOURCES.md:125
rows=103 tokens=11 defects=5
EXIT=1
```

So the counter is not vacuous on this lane's own history: **before 5 defects / exit 1, after 0 defects / exit 0**.
The five are exactly what round 37 repaired — four anchors that had no committed capture (fixed by committing
real bytes under `corpus/evidence/round37/anchor-captures/`, verified above) and S110's 63-hex transcription
defect (still in the row at tip, exempted by the append-only erratum). Nothing at 3ea9a1d9 is caught that tip
now hides: each before-defect has a landed repair in the diff, not a suppressed check.

## 3. Four mutants (my clone, tip)

Method: back up `corpus/SOURCES.md` and `corpus/lessons/round-37.md`, apply one edit, run
`python3 plans/anchor_digest_check.py --lane .`, then restore; `git -C S/fx/lane diff --stat` before each run
showed exactly the one intended line (`1 file changed, 1 insertion(+), 1 deletion(-)` / `1 deletion(-)`), and it
was empty after restore, with a re-run at `defects=0`. No git write beyond the index; nothing committed.

| # | mutant | tool output (defects) | verdict |
|---|---|---|---|
| M1 | delete line `Erratum (round 37): S110 anchor sha256 …` from `corpus/lessons/round-37.md` | `DEFECT S110 … class=digest-short detail=63-hex`, `defects=1` | **caught** |
| M2 | last hex digit of the erratum's correction digest `…96f9c`→`…96f9d` | `erratum-digest-unresolved` + `erratum-incomplete` + `digest-short` on S110, `defects=3` | **caught** |
| M3 | shorten S108's anchor by one digit (`…e8f72`→`…e8f7`, 63 hex) | `DEFECT S108 … class=digest-short detail=63-hex`, `defects=1` | **caught** |
| M4a | second token `sha256 dead00beef…dead` added to S111's anchor cell (unresolvable) | `DEFECT S111 … class=digest-unknown`, `defects=1` | **caught** |
| M4b | same insertion, but the second token is **S108's real committed digest** | `rows=107 tokens=15 defects=0`, `EXIT=0` | **MISSED** |
| M5 | (extra) S111's digest **replaced** by S108's real digest | `defects=0`, `EXIT=0` | **MISSED** |

Count under the strict reading of the assigned mutant: **3/4**. The assignment fixes the shape of M4 ("add a
second sha256 token") but not its value, and the value decides the outcome: the tool tests *bad digests*, not
*extra claims*. If the wave counts M4 by the fabricated-token variant it is 4/4; the survivor is stated here
rather than assumed away.

## 4. Findings

**F37A-1 (limit of the landed claim, no repair made).** Anchor resolution is membership in one global set, not
row-scoped. `check()` builds `allowed = set(files) | set(manifests)` and asks only `tok not in allowed`, so a row's
digest may be swapped for any other committed capture's digest and still pass (M5: S111 carries S108's digest,
`defects=0`). The docstring's motivation sentence — "nothing in the lane compared a row's digest with the capture
manifest" / "This check does that comparison for every row" — reads row-scoped while the implemented test is
global; per-token the doc is accurate ("must be a member of A"). This is the *second half* of the S110 defect
family: round 36's dropped `0` makes 63 hex (caught), but a mis-transcription that lands on a *real* sibling digest
is invisible. Tightening, if a later round freezes it: locate the row's capture from its own locator
(`corpus/evidence/round37/anchor-captures/S070-…`, `…/tb2-git-webserver/SHA256SUMS`) and require the digest there.

**F37A-2 (index mode is self-certifying).** `--evidence-ref index` exists so seats that may not commit can show a
green tree, and manifest listings are never tied to blob bytes: a seat stages one `SHA256SUMS` line naming a
fabricated digest and points a row at it → `defects=0` in index mode while head mode still prints
`digest-unknown` (receipt `probe-index-manifest-mint.txt`; the named blob was left unstaged on purpose). The
docstring's control C6 claims only that an *uncommitted* manifest cannot launder — correct, but the same hole is
open to any staged manifest, which is precisely the authority a fixture seat has. Suggested shape: when
`ref=index`, accept a manifest digest only if the tree also stages/commits a blob of that digest.

Neither finding contradicts the after-run numbers; both narrow what "every sha256 claim resolves" buys.

## 5. Not verified here

- No run against a lane-side erratum for a *different* sid, nor a repaired-row-plus-stale-erratum case (the
  docstring says no stale-erratum defect is raised; not tested by this seat).
- No attempt to falsify the census regex agreement between `plans/round37_c2_verify.py` and this tool.
- Nothing about `plans/round37_c1_verify.py`, the C2 corpus rows or the probe — outside this seat.

VERDICT: anchor-before-5-after-0-mutants-3/4
