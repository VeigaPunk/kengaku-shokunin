# F39IndepProbe — six extra end states for the TB2 `git-leak-recovery` grader: predictions vs observed

Wave 2 (falsify), kengaku round 39, seat `F39IndepProbe`. Lane tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`
(clone verified: `git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r39/F39IndepProbe/lane`,
`rev-parse HEAD` → the tip; receipt `F39IndepProbe/prediction-order.txt`). Nothing in the lane was written; every
number below comes from one of the receipts in `F39IndepProbe/`.

**Axes.** A1 prediction fidelity (my static reading vs measurement); A2 verdict direction (does each unclaimed state
get caught or pass with the secret alive); A3 instrument (host git 2.56.0 vs the image's apt git 2.43.0 vs 2.39.5);
A4 false-negative surface beyond the frozen 25; A5 determinism of the letters.

## 1. What was run

Predictions were frozen **before** the first run: `F39IndepProbe/predictions-before-run.txt`
(sha256 `7b6b5978…`, mtime 04:45:21; the first probe output `run1.txt` is 04:46:42 — `prediction-order.txt`).

The probe is the lane's own frozen `plans/git_leak_probe.py` (sha256 `4961a50f28ae85e8d8b687d3623aef29b59d4db14c0e62e5244e48cfef8cf68c`),
imported rather than rewritten: `probe_extra.py` reuses its `PINS` check, `sandbox_argv()` (bwrap
`--unshare-net --unshare-pid --unshare-ipc`, `/usr` and `/etc` read-only, private `/tmp`, fresh writable `/app`,
`/cap` holding only the three pinned captures, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`), its `Case`,
`run_case()`, `TESTS` and `overall()`. Only two things are added: six cases outside the frozen 25, and an
*independent* sweep appended to the harness **after** the five grader calls (`PROBE` lines: every object body via
`cat-file --batch-all-objects --batch`, tree entry names via `cat-file -p` per tree, plaintext files under `/app`,
the exact T5 `find … sha256sum` command, `fsck --lost-found` dangling count, `git log --reflog -p -S 'secret['`,
`for-each-ref`, whether `.git` is a gitfile). The grader is called exactly as the frozen probe calls it — the five
functions in file order, `AssertionError` = F, any other exception = F.

Commands (host: git 2.56.0, bubblewrap 0.13.1, Python 3.14.8):

```
python3 "$S/probe_extra.py" "$S/lane" "$S/work" > run-final.txt     # 6 cases × 2 runs
python3 "$S/evidence.py"    "$S/lane" "$S/work" > evidence.txt      # mechanism per test
```

Instrument check on the **task image's git**: `Dockerfile:3` is `FROM ubuntu:24.04` and `:7` installs git from apt,
so the six recipes + `challenge-setup.sh` were replayed in `ubuntu:24.04` with **apt git 2.43.0** and the five pinned
test functions called by the container's `python3` (`image43.txt`, 30 `TEST` lines, no `FAIL`). A third git
(2.39.5, `node:22`, already local) was used only for the `--all`/worktree mechanism cross-check.

Probe summary line (host, verbatim):

```
cases=6 predicted_pass=3 predicted_fail=3 agree=5 mismatch=1
determinism run1_vs_run2=identical
```

Header of the same receipt: `plans/git_leak_probe.py sha256=4961a50f…` plus the three capture digests
(`test_outputs.py dc7b01c1…`, `challenge-setup.sh a0a19652…`, `solve.sh 791a7eb2…`), so the grader bytes are the
frozen ones.

## 2. Predictions vs observed

Letters are the five tests in file order: T1 flag, T2 `log --all --grep` + `log --all -p -S`, T3 init message,
T4 `fsck --lost-found` + `cat-file -p`, T5 checksum.

| # | case | predicted | observed host 2.56.0 | observed image git 2.43.0 | agree |
|---|---|---|---|---|---|
| 1 | `replace-ref-pins-secret-commit` | PFPPP | **PFPPP** | PFPPP | yes |
| 2 | `packed-refs-only-leak` | PFPPP | **PFPPP** | PFPPP | yes |
| 3 | `detached-worktree-secret` | PPPPP | **PFPPP** | PFPPP | **NO** |
| 4 | `gitfile-separate-store-dangling-blob` | PPPFP | **PPPFP** | PPPFP | yes |
| 5 | `tree-name-secret` | PPPPP | **PPPPP** | PPPPP | yes |
| 6 | `deleted-branch-reflog` | PPPPP | **PPPPP** | PPPPP | yes |
| + | `worktree-added-then-removed` (*post-hoc*, §4 finding 5) | PPPPP | **PPPPP** | — | yes (post-hoc) |

`indep-extra-agree-5/6` — the one miss is mine, not the grader's (§4, finding 1). Every letter is identical on the
host's git 2.56.0 and on the task image's git 2.43.0 (`image43.txt` vs `run-final.txt`, compared case by case).

## 3. Evidence per case (independent sweep, host run quotes `evidence.txt`)

| case | refs at end | T2 queries | fsck --lost-found | secret still in the repository | T5 digest |
|---|---|---|---|---|---|
| 1 replace-ref | `refs/heads/master,refs/replace/<id>` | grep 0 / **pickaxe 11** | 1 (commit) | 1 object body (`blob=1`) | pinned |
| 2 packed-refs | `refs/heads/keep,refs/heads/master` (no loose ref) | grep 0 / **pickaxe 11** | 0 | 1 object body | pinned |
| 3 worktree | `refs/heads/master` only | grep 0 / **pickaxe 11** | 0 | 1 object body **+ `/app/wt/secret.txt`** | pinned |
| 4 gitfile | `refs/heads/master`, `.git` is a file → `/app/meta` | grep 0 / pickaxe 0 | **1 (blob)** | 1 object body **+ `/app/meta/lost-found/other/52d18a09…`** | pinned |
| 5 tree name | `refs/heads/keep,refs/heads/master` | grep 0 / pickaxe 0 | 0 | 1 object body, **tree entry name = the literal** | pinned |
| 6 deleted branch | `refs/heads/master` only | grep 0 / pickaxe 0 | 1 (commit) | 1 object body, `--reflog` view hits (11 lines) | pinned |

Decisive command receipts (`quotable-receipts.txt`, reproduced in a scratch fixture):

- Case 5 — the literal lives in the tree, and neither search sees it:
  `git ls-tree -r keep` → `100644 blob 587be6b4…\tsecret[lost_and_found_in_git]`;
  `git log --all --grep 'secret\[' --regexp-ignore-case | wc -l` → `0`;
  `git log --all -p -S 'secret[' | wc -l` → `0` (the file's content is `x`; the path header is not counted).
- Case 6 — the branch is gone, `.git/logs/refs/heads/tmp` is gone (`find .git/logs -type f` → `.git/logs/HEAD`,
  `.git/logs/refs/heads/main`), `git log --all -p -S 'secret[' | wc -l` → `0`, while
  `git log --reflog -p -S 'secret[' | grep -c 'secret\['` → `1` and `git fsck --lost-found` prints
  `dangling commit 22a4eb7…` whose `cat-file -p` text is tree/parent/author + `chore: notes` — no file content.
- Case 1 — the replace ref is in the ref namespace: `PROBE refs=refs/heads/master,refs/replace/<id>`; `--grep` 0,
  `-S` 11 lines; fsck lists only the replacement commit, whose text carries no secret (T4 P).
- Case 4 — fsck follows the gitfile: `PROBE gitdir=/app/meta`, `PROBE dangling=1`, `PROBE object_hits=blob=1`, and T4 is
  the failing test; the checksum is still the pinned one.

## 4. Findings

**1. My only wrong prediction: a linked worktree is *not* a `log --all` blind spot (A1, A2).** I predicted T2 P
because `git log --all` is documented as the ref namespace plus `HEAD` — `git-log.1.gz:546-549` (git 2.56.0, zcat)
reads “Pretend as if all the refs in refs/, along with HEAD, are listed on the command line”. Measured, `rev-list
--all` also takes **each linked worktree's HEAD**: `worktree-all-mech-{2.56,2.43,2.39}.txt`, three gits, same triple —
without a worktree `rev-list --all=1`, with a detached worktree at a commit no ref names `rev-list --all=2`,
`for-each-ref` unchanged (`refs/heads/main` or `…/master`), `rev-parse --all=1`, `fsck --lost-found` dangling `1→0`,
`log --all -p -S 'secret['` 11 lines; `git worktree remove` returns it to `rev-list --all=1` / dangling `1`.
So the worktree shape is caught **while the worktree exists** and becomes the ordinary dangling-commit shape once
removed (§4, finding 5). The documentation sentence understates the behaviour; my reading followed the sentence.

**2. Two new measured false-negative shapes beyond the frozen 25 (A4).** `tree-name-secret` (`PPPPP`, case 5) and
`deleted-branch-reflog` (`PPPPP`, case 6) both end with the literal still in the repository (`objects_secret=1`) and
both pass all five tests. Mechanism, from `test_outputs.py`: `--grep` reads commit messages
(`test_outputs.py:22-38`), `-S` is a pickaxe over the changed lines of a diff (`:41-48`), so a **tree entry name** is
read by neither (case 5: grep 0, pickaxe 0, `tree_names=secret[lost_and_found_in_git]`); `fsck --lost-found` plus
`cat-file -p` reads each *dangling* object's own text (`:69-92`), so a commit that carries the secret only in its
blobs is invisible (case 6: dangling commit text has no secret); and no test reads a reflog, which is the only view
that still finds case 6's commit (`--reflog` hits 11 lines). This is the same direction as the entry's finding 4 but
two shapes it does not carry.

**3. Three of the six shapes are caught, and the entry's “not covered” list resolves toward covered for them (A2).**
`refs/replace` and `packed-refs-only` fire T2 (`pickaxe_lines=11`; the replace ref and packed-refs are both in the
`refs/` namespace `--all` walks), and the gitfile shape fires T4 (the grader's `git -C /app/repo` follows
`gitdir: /app/meta`). No lane claim is contradicted: the entry lists these as unclaimed, and the measurement says
“caught on 2.56.0 and 2.43.0”.

**4. T5 is a work-tree digest, and the six states show it (A2).** The computed checksum is the pinned
`2c3d6389133b6f9fffae5d3428ec1250c3b1cab5573c716d580dc1d4fa2f4adb` in **all six** receipts, including case 4 where the
whole object store was moved to `/app/meta` and `.git` is a one-line file. `find /app/repo -type f -not -path
'*/\.*'` (`test_outputs.py:101`) matches `/.git` as a dot path, so neither the store's location nor its contents
matter to T5 — the mechanism behind the frozen `files-untouched` label, unchanged.

**5. Post-hoc addendum (disclosed): the removed-worktree state is a third new false negative.** Prediction written
*after* the six-case run (`addendum.txt`): `worktree-added-then-removed` → `PPPPP` observed, `object_hits blob=1`,
`dangling=1`, `work_hits=0`. Adding then removing a linked worktree leaves an ordinary dangling commit with a clean
message, i.e. the `echo-only` mechanism — so “a worktree” is caught or blind depending only on whether a worktree HEAD
names the commit at grading time.

**6. Side effect of the grader's own T4: `--lost-found` materialises dangling objects in the git dir.** In case 4 the
sweep found the secret in plaintext at `/app/meta/lost-found/other/52d18a091cd9755bacb8eaccab2882a24b080dc7` **after**
the five tests ran; that file is written by `git fsck --lost-found` (`test_outputs.py:69`) for the dangling blob. It is
a dot path (invisible to T5) and only appears when T4 already fails, so it is not a verdict channel — it is a fact
about what grading writes.

## 5. Impacted axes and the smallest safe correction

- **A1**: 1/6 predictions wrong (worktree). Corrected by measurement on three gits; the prediction file is not edited.
- **A2/A4**: three new measured end states for the `secret-gone` tag, two of them blind (`tree-name-secret`,
  `deleted-branch-reflog`) plus one post-hoc (`worktree-added-then-removed`); three shapes confirmed caught
  (replace ref, packed-refs, gitfile).
- **A3**: no instrument sensitivity in these six — host git 2.56.0 and image apt git 2.43.0 agree on all 30 verdicts;
  the 2.39.5 run was used only for the `--all`/worktree mechanism and agrees there too.
- **A5**: two host runs byte-identical (`determinism run1_vs_run2=identical`).

**Smallest safe correction** (this seat is read-only, so it is proposed, not applied): replace the bare
“worktree clones” item in the C2 entry's *What the probe does not show* list with one sentence, and leave the frozen
25-case table and its receipt untouched:

> A linked worktree's HEAD is read by `--all` and counted reachable by `fsck` (measured on git 2.39.5, 2.43.0 and
> 2.56.0: `rev-list --all` 1→2 on `git worktree add`, back to 1 on `git worktree remove`), so a worktree is caught
> while it exists and blind once removed; a tree entry **name** carrying the literal is read by neither `--grep` nor
> `-S`; and a deleted branch's commit survives only in the reflog, which no test reads.

Next round (not this frozen table) should add the three cases `tree-name-secret`, `deleted-branch-reflog`,
`worktree-added-then-removed`.

## 6. Limits

- The host run is the frozen probe's instrument: host git 2.56.0, host bash and coreutils, the probing user, bwrap
  sandbox; the declared image `alexgshaw/git-leak-recovery:20251031` (`task.toml:30`) is **never pulled**.
- The image-git run is a version cross-check, not an image run: `ubuntu:24.04` + apt git 2.43.0, the container's
  `python3` 3.12 calling the five functions directly, no pytest 3.13/`uvx`, no `/logs/verifier`, no bwrap, root.
- All six recipes are constructed end states that begin from the task's own `challenge-setup.sh` output; they are not
  agent trajectories and say nothing about whether an agent would reach them.
- The wrapper reuses the frozen probe's sandbox and `run_case()` but not its case-table validator or receipt printer;
  my sweep had two authoring bugs fixed before the final receipt (a mistyped helper name, and a tree-name parse that
  read raw tree bodies where 20-byte ids can contain `0x0a`) — neither touches what the grader is asked, and the
  final receipts are from the fixed wrapper.
- Determinism is claimed for letters only; object ids are date-dependent and are not printed anywhere (the one id in
  the receipts, `52d18a09…`, is the content address of the fixed secret line, so it repeats).
- Tooling: nothing was installed or upgraded on the host (no pacman transaction was attempted). `docker pull
  ubuntu:24.04` reported “Image is up to date” — the image was already local — and `git`/`python3` were installed
  only inside throw-away `--rm` containers; no container or scratch directory is left behind.
- This does not falsify any line of the C2 entry: its falsifier (b)/(d) is untouched, the frozen 25-case receipt
  still stands, and the six states sit inside the entry's own disclosed negative space. It narrows one disclosure
  (worktree) and adds two blind shapes.

VERDICT: indep-extra-agree-5/6
