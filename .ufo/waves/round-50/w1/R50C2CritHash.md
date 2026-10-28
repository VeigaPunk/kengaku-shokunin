# R50C2CritHash — critic, R50-C2 (calibration), hash half of the pointer audit

REV ../kengaku-shokunin@d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78 (lane tip at measurement; `master`==`HEAD`==d45c5bb)
Freeze: `git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD` → rc 0 ("FREEZE-IS-ANCESTOR-OF-d45c5bb ok").
Instrument measured: `plans/round50_c2_audit.py` sha256 `b911d03a08e396e5efdfaa434841300ccb5a452965c9d21c0c5fa56ea5dcaaef` (identical at c3372a9 and d45c5bb — `git diff --stat c3372a9 d45c5bb -- plans/round50_c2_audit.py` prints nothing).
All work on `git clone --shared` copies in `/fast/scratch/hyaku/kengaku-r50/R50C2CritHash` (lane, lane2, attacker, attacker2, shallow8, shallow200), never the live checkout; every fixture write preceded by a `rev-parse --show-toplevel` assertion. No production file touched; no commit, push, checkout, stash or mutating git in the lane.

## Axes named

C2 = calibration, sub-axis **hash-pointer resolution soundness**. Decomposed into five probes, one per attack class the item names plus two environment axes that the same two plumbing commands inherit:

| # | axis | question |
|---|---|---|
| A1 | commit-not-ancestor | does `cat-file -e` + `merge-base --is-ancestor` reject a real commit that is not an ancestor |
| A2 | substring/lexical | does the tokenizer extract a 40-hex substring of a longer hash, and is a fenced 40-hex token resolved the same as inside a run |
| A3 | object type | gitlink (mode 160000), blob, tree, annotated tag |
| A4 | environment | clone depth (shallow) and tip-name resolution — the two inputs the classifier silently trusts |
| A5 | forgery | `refs/replace` rewriting the ancestry graph (the round's own hostile corpus class) |

## Method (exact commands)

```
S=/fast/scratch/hyaku/kengaku-r50/R50C2CritHash
git clone --shared -q <lane> $S/lane2                    # at d45c5bb
(cd $S/lane2 && python3 plans/round50_c2_audit.py --lane .)
git clone --shared -q $S/lane2 $S/attacker2              # injects one token per class into SCORECARD.md,
python3 $S/hash_attack.py                                 # commits, then runs the REAL audit with --lane
git clone -q --depth 8   "file://$S/lane2" $S/shallow8
git clone -q --depth 200 "file://$S/lane2" $S/shallow200
# per token: git cat-file -e <t>; git cat-file -t <t>; git merge-base --is-ancestor <t> <tip>
```

Baseline at REV (unmodified clone):

```
TIP d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78 branch=master
POINTERS total=279 paths=219 hashes=60 resolved=279 exists=207 superseded=3 never-landed=9 unresolved=0
RC=0
```

Object-type census of all 60 audited tokens (`cat-file -t` each): `{'commit': 60}`, zero non-commit tokens, zero `refs/tags` in the lane (`for-each-ref refs/tags | wc -l` → `0`), zero gitlinks (`git ls-tree -r HEAD | awk '$1=="160000"' | wc -l` → `0`; index modes are 17030×`100644` + 1017×`100755`).

## Attack matrix (injected into a scratch clone; audit run with the real script)

Audit output on the injected clone (verbatim):

```
TIP a65bc1179f50fbed16dd3f009db2bf85bcbe7aab branch=master
POINTERS total=288 paths=219 hashes=69 resolved=280 exists=207 superseded=3 never-landed=9 unresolved=8
UNRESOLVED-HASH 080521a79e2c794751b8a9ad7b43e79d95e230cb not-ancestor
UNRESOLVED-HASH 0a3cad6d9cbb7a3340b71ce9e33275385adf0567 missing
UNRESOLVED-HASH 315d1c9deb7334ef5d75786848ef510e90cc7a01 not-ancestor
UNRESOLVED-HASH 73a72f86dc3612ece7568ace027c997d236cd6d8 missing
UNRESOLVED-HASH adcc503ab8d1c59ed1da086c3e975072a0e8bd18 not-ancestor
UNRESOLVED-HASH bad3b49334ff195b8ffcc51aaa8523d3ea474392 not-ancestor
UNRESOLVED-HASH ea88355364b67906078b24cba1c249f9f8a3aecf not-ancestor
UNRESOLVED-HASH f3dfcb11e71b75afef5b550dcb56d29252cf4342 missing
RC=1
```

Raw plumbing per class (`cat-e` = `cat-file -e`, `isanc` = `merge-base --is-ancestor <t> <tip>`, type = `cat-file -t`):

| class | token | type | cat-e | isanc | audit verdict | correct? |
|---|---|---|---|---|---|---|
| control: ancestor commit | `d6f2fce9…bedf5cd` | commit | 0 | 0 | resolved | yes |
| **commit, dangling (not ancestor)** | `adcc503a…0e8bd18` | commit | 0 | 1 | `not-ancestor` | **yes** |
| **commit, descendant of tip** | `bad3b493…474392` | commit | 0 | 1 | `not-ancestor` | **yes** |
| **blob object** | `080521a7…95e230cb` | blob | 0 | 128 | `not-ancestor` | verdict yes, **label wrong** |
| **tree object** | `ea883553…8a3aecf` | tree | 0 | 128 | `not-ancestor` | verdict yes, **label wrong** |
| **annotated tag object → ancestor** | `83dd5d2d…19639632` | tag | 0 | 0 | **resolved** | **no — false accept** |
| **gitlink sha absent from superproject** | `0a3cad6d…fd0567` | absent | 1 | 128 | `missing` | yes (per spec text) |
| tree containing a gitlink entry | `315d1c9d…cc7a01` | tree | 0 | 128 | `not-ancestor` | verdict yes, label wrong |
| ghost 40-hex never written (negative control) | `73a72f86…366cd6d8` | absent | 1 | 128 | `missing` | yes (detector works) |
| 64-hex sha256, bare | `4d3ff561…5f2b` (64 chars) | — | 128 | 128 | **not extracted** | yes |
| `SHA256`+40-hex (46-char run) | `SHA2564d3ff5…` | — | 128 | 128 | **not extracted** | yes |
| `SHA256`+62-hex (68-char run) | `SHA2564d3ff5…` | — | 128 | 128 | **not extracted** | yes |
| **uppercase 40-hex of the tip** | `05DD6A9E…` | commit | **0** | **0** | **not extracted** | **no — lexical escape** |
| 40-hex prefix of a sha256, separated | `4d3ff561…` (40) | absent | 1 | 128 | `missing` | spurious pointer, see F5 |

`cat-file -t` stderr for the non-commit rejects (verbatim, from `merge-base`):

```
error: object 080521a79e2c794751b8a9ad7b43e79d95e230cb is a blob, not a commit
error: object ea88355364b67906078b24cba1c249f9f8a3aecf is a tree, not a commit
fatal: Not a valid commit name 0a3cad6d9cbb7a3340b71ce9e33275385adf0567
```

Extraction is case- and boundary-exact: of the 14 injected strings exactly 10 became audited tokens (the three >40-char runs and the uppercased tip were not extracted); `hashes=69 = 60 baseline + 9 new distinct tokens` — the ancestor control `d6f2fce9…` was already cited in `SCORECARD.md`, so 10 injected tokens add 9 — and 69 − 8 unresolved = 61 resolved hashes, the tag object among them.

## Real-file evidence for the substring axis

`SCORECARD.md:843` at the tip already carries a digest concatenated to its label:

```
843:Commands/revision: delivered checker SHA25629c5d716a53e77bf4a82d2155775dda3e94385e058b4700af54cb3a23d031f32,
```

That is a 68-char run (`A256` + 64-hex digest); the lowercase-hex run is 67 chars, so no 40-window has a non-hex neighbour on both sides. Independent check over the three files: every regex-extracted token is *not* a substring of any ≥41-char hex run (`extracted tokens that are substrings of >40 runs: []`), and the only ≥41-char lowercase run in the three files is that one. **A2 is structurally safe for contiguous runs.**

## Findings

**F1 (A3, false accept, latent).** `cat-file -e` accepts any object type and `merge-base --is-ancestor` peels tags, so an annotated-tag object sha is counted as "exists and is an ancestor of the branch tip" although it is not a commit. Witnessed: `type=tag cat-e=0 isanc=0` → counted in `resolved=280`, no `UNRESOLVED-HASH`. Not live today (60/60 audited tokens are commits, 0 tags), so it does not affect the C2 predicate at this REV.
Smallest safe correction (scratch proposal, not applied): classify with `git cat-file -t` first and only run `--is-ancestor` for `commit` (and, if tag objects are to remain legal pointers, for `tag` after `rev-parse --verify -q <h>^{commit}`); print the observed type in the reason field. Two extra git calls per hash, output unchanged on the current 60 tokens.

**F2 (A3, wrong diagnosis).** Blob and tree tokens are reported as `not-ancestor` because both `merge-base` exit 1 (not an ancestor) and exit 128 (not a commit / fatal) collapse into `!= 0`. The verdict is correct and fail-closed, but a maintainer reading `not-ancestor` would try to fix the wrong thing. Same correction as F1; if the type check is added, also split the reason into `not-a-commit (<type>)` vs `not-ancestor`.

**F3 (A4, false red, high impact).** The classifier trusts clone depth. Same REV, same docs:

```
--depth 8 : POINTERS total=279 paths=219 hashes=60 resolved=220 … unresolved=59   RC=1   (all 59 "missing")
--depth 200: POINTERS total=279 paths=219 hashes=60 resolved=268 … unresolved=11   RC=1
```

59/60 then 11/60 hashes are reported `missing` purely because history is truncated — `cat-file -e` cannot see unreached objects and `--is-ancestor` cannot walk past a shallow boundary. Any seat or CI auditing a `--depth` clone (or a `git worktree` of a shallow clone) gets `unresolved>0` with no indication that the environment, not the docs, is wrong. Smallest safe correction: before the hash loop, `if git rev-parse --is-shallow-repository` → `SETUP shallow-clone` and exit 2 (a setup error is not a predicate failure). One call, no change on a full clone.

**F4 (A4, silent tip shadowing).** The tip is `rev-parse <branch>` after `rev-parse --abbrev-ref origin/HEAD | split("/")[-1]`, and git's ref precedence lets `refs/tags/master` shadow `refs/heads/master`. Witnessed in the scratch clone after `git tag master HEAD~2`:

```
warning: refname 'master' is ambiguous.
TIP d6f2fce9889f429162c12f851bae41891bedf5cd branch=master
POINTERS total=288 paths=219 hashes=69 resolved=279 … unresolved=9   RC=1     (was 8)
```

The audit's `git()` helper captures stderr and never looks at it, so the ambiguity warning is swallowed; the failure surfaces only as an unexplained extra `UNRESOLVED-HASH`. Direction is false-red only (a shadowing tag can only move the ancestor set), so it cannot admit a bad pointer. Smallest safe correction: `git rev-parse --verify refs/heads/<branch>` and fail `SETUP` on a non-zero rc instead of silently falling back to `HEAD`.

**F5 (A2, spurious red).** The tokenizer cannot tell a git hash from a sha256 fragment: the 40-hex *prefix of a sha256 written as its own token* (line-wrapped digest, or a digest copy-pasted in two pieces) is extracted and reported `missing` (`4d3ff561…` → `missing`). No live instance: all 40-hex tokens in the three files are commits, and the one 64-hex digest in `SCORECARD.md:843` is inert because it sits inside a 68-char run. Cheap guard if wanted: assert no extracted 40-hex token is a prefix of any ≥41-char hex run in the same file, or exempt tokens within N characters of a `sha256`/`SHA256` marker. Not required by the frozen surface (which counts 40-hex hashes only).

**F6 (A1 and A5, negative results — the classifier is sound where it matters).**
- Commit-not-ancestor: both shapes (dangling orphan, child of the tip) are rejected with `isanc=1` → `not-ancestor`, exit 1. No false accept.
- `refs/replace` forgery is **not** a channel: `merge-base --is-ancestor` ignores replace refs in both directions. Witnessed: orphan `9649458…` with `refs/replace/9649458… → c3372a9…` stays `rc=1`, and an ancestor `c3372a9…` with `refs/replace/c3372a9… → <orphan>` stays `rc=0` (`GIT_NO_REPLACE_OBJECTS=1` gives the same rc). So the round's own replace-ref hostile class cannot rewrite C2's ancestry answers.
- Sibling-branch shape: the lane's other heads are ancestors of `master` (`hyaku/s3-kengaku-containment 6a2c2df7…` ancestor, `round29/R29ExecCore 31934e56…` ancestor), so no false positive from them today; a commit cited from an *unmerged* branch would be (correctly, per the frozen text) rejected.

## Impact on the R50-C2 kill rule

None of the probes reaches the kill rule at this REV: the audit on a full `--shared` clone at d45c5bb prints `unresolved=0` and exits 0, and every misclassification I could produce is either latent (F1: 0 tag objects in the lane), cosmetic (F2), or environment-induced (F3, F4) — all in the **false-red** direction. No probe produced a false green from a not-an-ancestor commit, a substring of a longer hash, or a gitlink. The C2 claim survives the hash half; the tool has three cheap hardening moves (F1/F3/F4) that cost nothing on the current corpus.

## Limits

- Fixtures are hand-built git states; a real submodule (`git submodule add`) was not created — the gitlink was exercised as a committed `160000` tree entry plus a commit object present only in a separate repo, which is the same object-database relation (0 gitlinks in the lane make the distinction moot today).
- Clone-depth and tag-shadow probes were run on scratch clones; I did not test a partial/promisor clone (`--filter=blob:none`), which would hit the `cat-file -e` missing branch for the same reason as F3.
- Cross-repo citations (a 40-hex of another repository) would be `missing`; the lane's 60 tokens are all lane-lane commits.
- The audit was not modified; the four corrections above are proposals only, recorded here as the smallest safe changes and not applied to any production file.
- I did not re-run `--selftest` (owned elsewhere); I did not measure the C1 legs.

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50C2CritHash` (lane, lane2, attacker, attacker2, shallow8, shallow200, hash_attack.py, attack*.json) — **removed before yield**; every receipt cited above is quoted verbatim in this file, so no /tmp or scratch path is load-bearing evidence.

VERDICT: **R50-C2 hash half is sound on all three named classes at d45c5bb — no false resolution from a non-ancestor commit, no extraction of a 40-hex substring of a longer hash (confirmed against the live 68-char run at SCORECARD.md:843), and no false accept from a gitlink sha. One latent false accept exists (annotated-tag object, F1), two mislabels (F2), and two environment false-reds (shallow clone 59/60 and 11/60; tag-shadowed tip, F3/F4); none reaches the predicate at this REV, and the smallest safe corrections are the four one-line guards above.**
