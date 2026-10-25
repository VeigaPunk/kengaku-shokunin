# R33FN1Index — C2/N1 tracked-versus-committed distinction (falsify)

Round 33, hyaku run 7, 2026-10-25. Seat: `KengakuR33.R33FN1Index`.
Target: N1 of `plans/round33_defects.py` (sha256 `6ef17abc…64d5b6`, on-disk bytes
unchanged by this seat), frozen predicate `plans/round-33-claims.md:87-88`.
Method: isolated `/tmp/r33-fn1-index/` git repos only; all git commands `-C`
scoped to `/tmp`. No lane/fleet file touched (verified: lane plans file sha256
unchanged before/after; `plans/__pycache__/round33_defects.cpython-314.pyc`
mtime `14:23:27` predates this seat — no write).

## 1. The named defect, restated

Round 32 left **ten uncommitted round-32 wave paths at a pushed tip**
(`plans/round-33-claims.md:78`). The repair per the claim's own words is that the
tree "is committed under this round's entry via N1" (`:158`) — the check registry
label is `round32-wave-tree-committed` (`plans/round33_defects.py:167`) and N1's
docstring says "Every file under .ufo/waves/round-32/ is tracked; nothing
untracked remains" (`:68-69`). The frozen predicate sentence itself reads
"every file under `.ufo/waves/round-32/` is git-tracked and no untracked path
remains beneath it" (`:87-88`). **"git-tracked" ≠ "committed"**: a file that is
staged (in the index) but absent from HEAD is tracked but uncommitted — exactly
the round-32 defect class.

## 2. Counterexample (exact commands and outputs)

Sandbox `laneA`: `git init` + baseline commit (README only), then one wave file
staged, never committed:

```
$ git -C /tmp/r33-fn1-index/laneA commit -qm 'baseline tip (no wave tree)'   # README only
$ printf 'seat report\n' > /tmp/r33-fn1-index/laneA/.ufo/waves/round-32/seat.md
$ git -C /tmp/r33-fn1-index/laneA add .ufo/waves/round-32/seat.md            # STAGED, NO COMMIT
$ git -C /tmp/r33-fn1-index/laneA ls-files -- .ufo/waves/round-32
.ufo/waves/round-32/seat.md
$ git -C /tmp/r33-fn1-index/laneA ls-tree -r --name-only HEAD -- .ufo/waves/round-32
$ git -C /tmp/r33-fn1-index/laneA status --porcelain -- .ufo/waves/round-32
A  .ufo/waves/round-32/seat.md
$ git -C /tmp/r33-fn1-index/laneA diff HEAD --stat -- .ufo/waves/round-32
 .ufo/waves/round-32/seat.md | 1 +
 1 file changed, 1 insertion(+)
```

`git ls-tree HEAD` output is empty — the file is **not in the committed tree** —
while `git ls-files` lists it. Now the N1 checker (real production code, imported
read-only from the lane file):

```
$ python3 -B -c '... import check_n1 ...' --laneA
check_n1 => GREEN ("")
```

N1 returns `''` (green) on a tree whose only wave file is staged-not-committed.
The control lane (`laneB`, same file left untracked) reddens:

```
check_n1 => RED 1 untracked files remain under .ufo/waves/round-32: seat.md
```

So staging is precisely the difference between red and green — and staging is
precisely the "uncommitted work at the tip" state the defect names.

## 3. Why: the check compares disk vs the *index*, not vs HEAD

`plans/round33_defects.py:77`: `git(lane, "ls-files", "--", WAVE32)`.
`git ls-files` enumerates the **index** (staged + committed), not the commit.
Additional observed shapes (same sandbox):

| lane | wave-tree state | check_n1 |
|---|---|---|
| laneA | file staged, absent from HEAD | **GREEN** |
| laneB | file untracked (control) | RED `1 untracked files remain` |
| laneC | tracked file modified + re-staged (index≠HEAD content) | **GREEN** |
| laneD | staged **and** committed (positive control) | GREEN (correct) |
| laneE | `git add -N` intent-to-add only | **GREEN** |
| laneF | no commit at all, `git add .` only (selftest green fixture's own shape) | **GREEN** |

`laneC` shows the same blind spot for content: `git status --porcelain` =
`M  .ufo/waves/round-32/seat.md` and `git diff HEAD` non-empty, yet N1 is green.

`laneF` deserves a line: N1's **own selftest green fixture** does `git init -q`
then `git add .` with **no commit** (`plans/round33_defects.py:227-229`). The
artifact's self-evidence literally models the exploit — the check is green before
any commit exists. (`git ls-tree HEAD` returns rc=128 on an unborn HEAD; the
check never looks.)

## 4. Full C2 receipt is green on the uncommitted tree

Fabricated lane `laneG` (in `/tmp`): baseline commit; wave file **staged only**;
N2/N5/N6 fixtures satisfied; mock fleet reports in `/tmp` with the N3/N4 tokens
(module globals `R31_REPORT`/`R32_REPORT` overridden in-process only):

```
$ python3 ... main(['--lane', '/tmp/r33-fn1-index/laneG'])
checks=6 defects=0
exit= 0
$ git -C /tmp/r33-fn1-index/laneG ls-tree -r --name-only HEAD -- .ufo/waves/round-32
$ git -C /tmp/r33-fn1-index/laneG status --porcelain -- .ufo/waves/round-32
A  .ufo/waves/round-32/seat.md
```

The C2 counting command prints `checks=6 defects=0` and exits 0 while the wave
tree is still uncommitted at the tip — the receipt cannot certify the half of N1
its own label promises ("committed").

## 5. Verdict

**Caught (mutation gamed the counter).** The staged-not-committed mutation is
invisible to N1. The frozen predicate's literal wording ("git-tracked") is
ambiguous, but the check's label (`round32-wave-tree-committed`), docstring, and
the claim's §Inherited-state sentence ("is committed under this round's entry via
N1") bind N1 to commit membership, and the check does not test it. A C2
`defects=0` receipt therefore does not prove the routed defect is closed; an
index-only tree satisfies the counter.

**Not claimed:** the live landing is fake. Build-wave evidence (R33ScorecardPatch
`:74`, R33MistakeMine `:35`) records the actual closure commit `c227e486`
committing 89 files; this seat did not read lane git (off-limits). This falsify
result attacks the counter's condition, not the observed landing.

## 6. Smallest safe correction (verified in scratch)

Replace the left side of the set-difference with the committed tree:

```
git(lane, "ls-tree", "-r", "--name-only", "HEAD", "--", WAVE32)
```

(handling rc != 0 — unborn HEAD — as a defect: nothing is committed). Verified in
scratch against all six sandbox lanes:

```
HEAD-variant on laneA: 1 uncommitted files remain under .ufo/waves/round-32: seat.md
HEAD-variant on laneB: 1 uncommitted files remain under .ufo/waves/round-32: seat.md
HEAD-variant on laneC: GREEN
HEAD-variant on laneD: GREEN
HEAD-variant on laneE: 1 uncommitted files remain under .ufo/waves/round-32: seat.md
HEAD-variant on laneF: no HEAD tree to compare against: fatal: Not a valid object name HEAD
```

If the narrative "commits the whole tree" is also meant to cover modified-staged
*content* (laneC), add a `git status --porcelain -- .ufo/waves/round-32`
empty check rather than the DIFF alone; the named defect ("no untracked path
remains") needs only the HEAD comparison.

## 7. Impacted axes

- **Calibration (C2)**: N1's discriminator is index-based; the six-check receipt
  cannot distinguish a staged tree from a committed one. The claim as written
  (predicate + label + narrative) is satisfiable by a state the claim itself
  names as uncommitted.
- **Unchanged**: C1, C3, registry, routes, model names (none touched).
- **Reported in build wave for cross-reference**: R33CounterAttack E1/B1 and
  R33ClaimsReview `:19` flagged this same blind spot; this seat provides the
  executed reproduction and a verified correction.

## 8. Environment / hygiene

- No tool installed; no lane/fleet write; sandbox `/tmp/r33-fn1-index/` only.
- Lane plans file sha256 constant (`6ef17abc…`) throughout.
