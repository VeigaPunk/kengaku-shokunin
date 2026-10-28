# R49C1Overrefusal — C1 novel-honest fixture review

**Axis:** calibration. **Scope:** novel honest repository classes beyond the frozen honest set; base/do-nothing fence only. This is fixture evidence, not an admission judgment for R49-C1 or R49-C2.

## Freeze and measured revision

The required pre-measurement freeze check passed. Before running any fixture, `git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93` returned `commit`; `git log --format='%H %ci %s' -3 9d2900af41e4d1fc6022eff99010436fde6dbd93` showed the freeze commit dated `2026-10-28 09:14:40 -0300`; `git merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD` succeeded (`ANCESTOR-OK`). It is a committed ancestor, not a working-tree-only claim. Its stat says it adds only `plans/round-49-claims.md`.

`REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` — scratch clone checked out at this revision before measurement; its `plans/fixture_fence.py` blob is `a2b128ae007bf47d3aefdeda6321ae118c7e5958`, exactly the same blob as at the C1 base `3a548330c4899c6c5df34168a44a59f66828ce74`; source SHA-256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`. Measurement time: `2026-10-28T09:28:59-03:00`. Environment: Git 2.56.0, Python 3.14.8. No tools installed or updated.

## Novel fixtures and measured outcomes

Eight scratch-only round-44-contract modules were built twice under separate scratch parents, with normalized tree fingerprints, discovered-repo `rev-parse --show-toplevel`, `git fsck --strict`, and the frozen base `fixture_fence.breach()` measured. Each finished deterministic; each repository top-level matched its repo path; all `fsck --strict` return codes were 0.

```text
o01-replace-ref                  anchor det=True repos=1 fsck=[0] top=[True] :: REFUSE: repo/.git/refs/replace is not refs/heads or refs/tags
o02-shallow-clone                anchor det=True repos=2 fsck=[0, 0] top=[True, True] :: REFUSE: repo/.git/shallow is not a plain-init entry
o03-packed-refs-peeled           anchor det=True repos=1 fsck=[0] top=[True] :: ADMIT
o04-gitmodules-fresh-clone       anchor det=True repos=1 fsck=[0] top=[True] :: ADMIT
o05-stash-pop                    anchor det=True repos=1 fsck=[0] top=[True] :: ADMIT
o06-pack-keep                    anchor det=True repos=1 fsck=[0] top=[True] :: ADMIT
o07-fetch-head-url               anchor det=True repos=2 fsck=[0, 0] top=[True, True] :: REFUSE: repo/.git/FETCH_HEAD is not a plain-init entry
o08-order-replace-ref            order  det=True repos=1 fsck=[0] top=[True] :: REFUSE: repo/.git/refs/replace is not refs/heads or refs/tags
```

The candidate population contains four base refusals of eight fixture instances (three distinct refusal classes: replace refs, a depth-limited shallow clone, and `FETCH_HEAD`). The replace-ref case is deliberately repeated under the `order` argv shape, not a fourth distinct repository class. Four cases are admitted: packed refs with peeled annotated tags, a worktree `.gitmodules` file without an initialized submodule, a settled stash-pop result, and a pack with `.keep`.

**Do-nothing result:** the unchanged base fence does not reach the frozen honest target on this extended candidate set: it refuses four honest fixtures. Round 48 independently measured it refusing 8 of its frozen 120 honest fixtures (`HONEST fixtures=120 admitted=112 refused=8`); these candidates add falsifiable vectors, not a replacement for the frozen population. A fence that returns these honest refusals cannot meet the C1 `HONEST ... refused=0` predicate.

**Representativeness:** broad coverage of the explicitly requested Git store/worktree states, with both admissions and refusals; not a representative sample of repository prevalence. The repeat replace-ref fixture adds argv-shape discrimination rather than a new repository class. The `.gitmodules` case is only the committed metadata state: no gitlink, initialized submodule config, or checked-out submodule. The pack `.keep` file is operator-created because `git repack -k` means keep-unreachable, not create a `.keep`; `repack`-generated `.git/info/refs` and `.git/objects/info/packs` were removed so it isolates the pack-name leg. The actual depth-1 clone uses an in-boundary `file://` source; origin config/refs and clone reflogs were removed to eliminate scratch-path and wall-clock nondeterminism, leaving the real `.git/shallow` boundary and no parent object. Thus it demonstrates the shallow-specific refusal but is not byte-for-byte a default network clone. The stash-pop builder removes `.git/AUTO_MERGE` left by this host's Git so the measured outcome is the settled stash result, not an unrelated transient marker. These caveats are part of the fixture definition, not evidence that the fence admitted default clones or initialized submodules.

## Exact commands and observed outputs

Freeze check (from the lane):

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93 && git log --format='%H %ci %s' -3 9d2900af41e4d1fc6022eff99010436fde6dbd93 && git rev-parse HEAD && git status --porcelain | head -5 && git merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD && echo ANCESTOR-OK
```

Observed relevant output:

```text
commit
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)
3a548330c4899c6c5df34168a44a59f66828ce74 2026-10-27 09:58:06 -0300 round-48 verifier spot-check (integrator, hyaku): non-author admit/reject
...
ANCESTOR-OK
```

Scratch clone and source identity commands:

```sh
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1Overrefusal
cd /fast/scratch/hyaku/kengaku-r49/R49C1Overrefusal
git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
cd lane && git checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93
D=/fast/scratch/hyaku/kengaku-r49/R49C1Overrefusal/lane
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D" && echo TOPLEVEL-OK
git -C "$D" rev-parse HEAD
sha256sum "$D/plans/fixture_fence.py"
git -C "$D" rev-parse 3a548330c4899c6c5df34168a44a59f66828ce74:plans/fixture_fence.py
git -C "$D" rev-parse 9d2900af41e4d1fc6022eff99010436fde6dbd93:plans/fixture_fence.py
```

Observed: `TOPLEVEL-OK`; `HEAD=9d2900af41e4d1fc6022eff99010436fde6dbd93`; SHA-256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`; both source blob IDs `a2b128ae007bf47d3aefdeda6321ae118c7e5958`.

Final clean build-and-measure command (after clearing only scratch build outputs):

```sh
rm -rf /fast/scratch/hyaku/kengaku-r49/R49C1Overrefusal/out/build0 /fast/scratch/hyaku/kengaku-r49/R49C1Overrefusal/out/build1
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1Overrefusal
python3 /fast/scratch/hyaku/kengaku-r49/R49C1Overrefusal/driver.py
```

The verbatim measurement output is the table above. The driver replicated the round-44 `Ctx` environment/pins and fingerprint rule, checked each generated repo with `rev-parse` and `fsck --strict`, and called the checked-out base fence. This is a fixture characterization, not a run of the pinned round-49 counter; no C1 predicate or admission claim is made.

## Source notes

Official Git documentation opened 2026-10-28; quotes are verbatim and under 25 words each:

- https://git-scm.com/docs/git-replace — “Adds a *replace* reference in `refs/replace/` namespace.”
- https://git-scm.com/docs/git-clone — “creates remote-tracking branches for each branch in the cloned repository”
- https://git-scm.com/docs/git-pack-refs — “storing the refs in a single file, `$GIT_DIR/packed-refs`.”

## Limits

- This was a scratch characterization against the stage-1 frozen base fence, not the stage-2 v3 counter; no strace behavior, sealed/refusal battery, mutation floor, or candidate fence was measured.
- Candidate modules are not part of a frozen or committed population and do not imply C1 admission. L1 must choose/pin any useful subset at stage 2 with the other named literals/populations.
- This host's Git 2.56.0 behavior was measured; no cross-version claim is made.
- No production file was edited; no tests/build/linter were run.

**VERDICT: BASE FENCE FAILS THE DO-NOTHING HONEST TARGET ON THESE NOVEL CLASSES; THE SET IS BROADLY REPRESENTATIVE OF THE REQUESTED STORE-SHAPE FAMILIES, NOT A PREVALENCE SAMPLE. NO C1/C2 ADMISSION CLAIM.**

## Candidate fixture modules

Runnable build-function excerpts used for the results are included below; explanatory module docstrings are abridged. Each excerpt preserves the fixture-building code and `FIXTURES` declaration.

### `o01_replace_ref.py`

```python
"""Round-49 C1 NEW honest class `o01_replace_ref`: one `git replace` ref.

`git replace <old> <new>` writes refs/replace/<old-sha> and a replacement object. The base fence
allows only heads and tags at refs/, so this legal contained store shape is refused.
"""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "first line\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "original commit")
    old = ctx.git(r, "rev-parse", "HEAD").stdout.strip()
    ctx.write(r / "a.txt", "first line, rewritten\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "replacement commit")
    new = ctx.git(r, "rev-parse", "HEAD").stdout.strip()
    ctx.git(r, "replace", old, new)
    return ["--lane", "repo"]
FIXTURES = [{"fid": "o01-replace-ref", "tool": "anchor", "expect": None, "defects": None, "build": build}]
```

### `o02_shallow_clone.py`

```python
"""Round-49 C1 NEW honest class: actual local git clone --depth 1; origin metadata removed for
scratch-path determinism, leaving the real shallow boundary and no parent object.
"""
import shutil

def build(ctx, d):
    source = ctx.init(d / "source")
    ctx.write(source / "a.txt", "deep history\n")
    ctx.git(source, "add", "-A")
    ctx.git(source, "commit", "-q", "-m", "parent")
    ctx.write(source / "a.txt", "shallow tip\n")
    ctx.git(source, "add", "-A")
    ctx.git(source, "commit", "-q", "-m", "tip")
    clone = d / "repo"
    ctx.sh("git", "-C", str(d), "clone", "--quiet", "--depth", "1", "--no-local",
           "file://" + str(source), str(clone))
    ctx.git(clone, "remote", "remove", "origin")
    shutil.rmtree(clone / ".git/refs/remotes", ignore_errors=True)
    shutil.rmtree(clone / ".git/logs", ignore_errors=True)
    return ["--lane", "repo"]
FIXTURES = [{"fid": "o02-shallow-clone", "tool": "anchor", "expect": None, "defects": None, "build": build}]
```

### `o03_packed_refs_peeled.py`

```python
"""Round-49 C1 NEW honest class: packed heads/tags with peeled annotated-tag lines; base admits it."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "release candidate\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "tagged commit")
    ctx.git(r, "branch", "feature/work")
    ctx.git(r, "tag", "-a", "-m", "release v1", "v1")
    ctx.git(r, "tag", "-a", "-m", "release v1.1", "v1.1")
    ctx.git(r, "pack-refs", "--all")
    return ["--lane", "repo"]
FIXTURES = [{"fid": "o03-packed-refs-peeled", "tool": "anchor", "expect": None, "defects": None, "build": build}]
```

### `o04_gitmodules_fresh_clone.py`

```python
"""Round-49 C1 NEW honest class: committed .gitmodules worktree file without initialized submodule."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "main project\n")
    ctx.write(r / ".gitmodules",
              '[submodule "vendor/lib"]\n\tpath = vendor/lib\n\turl = ../lib.git\n')
    ctx.write(r / "src/main.py", "print('uses vendored lib at vendor/lib')\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "project with vendored dependency declared")
    return ["--lane", "repo"]
FIXTURES = [{"fid": "o04-gitmodules-fresh-clone", "tool": "anchor", "expect": None, "defects": None, "build": build}]
```

### `o05_stash_pop_reflog.py`

```python
"""Round-49 C1 NEW honest class: settled stash pop; distinct from the frozen live-stash class."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "committed base\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "base")
    ctx.write(r / "a.txt", "work in progress\n")
    ctx.git(r, "stash", "push", "-q", "-m", "wip")
    ctx.git(r, "stash", "pop", "-q")
    (r / ".git/AUTO_MERGE").unlink(missing_ok=True)
    return ["--lane", "repo"]
FIXTURES = [{"fid": "o05-stash-pop", "tool": "anchor", "expect": None, "defects": None, "build": build}]
```

### `o06_pack_keep.py`

```python
"""Round-49 C1 NEW honest class: a .keep beside an actual pack; generated server adverts removed."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    for i in range(3):
        ctx.write(r / f"blob{i}.txt", f"content {i}\n")
        ctx.git(r, "add", "-A")
        ctx.git(r, "commit", "-q", "-m", f"blob {i}")
    ctx.git(r, "repack", "-a", "-d")
    packdir = r / ".git/objects/pack"
    kept = sorted(p.name for p in packdir.iterdir() if p.name.endswith(".pack"))[0]
    ctx.write(packdir / (kept[:-5] + ".keep"), "pinned: LFS baseline pack\n")
    (r / ".git/info/refs").unlink(missing_ok=True)
    (r / ".git/objects/info/packs").unlink(missing_ok=True)
    return ["--lane", "repo"]
FIXTURES = [{"fid": "o06-pack-keep", "tool": "anchor", "expect": None, "defects": None, "build": build}]
```

### `o07_fetch_head_url.py`

```python
"""Round-49 C1 NEW honest class: explicit in-boundary fetch writes FETCH_HEAD without remote config."""
def build(ctx, d):
    dep = ctx.init(d / "dep")
    ctx.write(dep / "lib.txt", "vendored lib source\n")
    ctx.git(dep, "add", "-A")
    ctx.git(dep, "commit", "-q", "-m", "lib release")
    main = ctx.init(d / "repo")
    ctx.write(main / "a.txt", "consumer\n")
    ctx.git(main, "add", "-A")
    ctx.git(main, "commit", "-q", "-m", "consumer base")
    ctx.git(main, "fetch", "../dep", "master")
    return ["--lane", "repo"]
FIXTURES = [{"fid": "o07-fetch-head-url", "tool": "anchor", "expect": None, "defects": None, "build": build}]
```

### `o08_order_replace_ref.py`

```python
"""Round-49 C1 NEW honest class: same replace-ref store under the order argv form."""
CLAIMS = "plans/round-49-claims.md"
RECEIPT = "corpus/evidence/round49/fixture-order-receipt.txt"
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "# fixture claims\n\nWritten before the receipt.\n")
    ctx.write(r / ".ufo/waves/round-49/claims/control.txt",
              "no gate line and no case line was ever committed here\n")
    ctx.write(r / "a.txt", "original\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "freeze and original commit")
    old = ctx.git(r, "rev-parse", "HEAD").stdout.strip()
    ctx.write(r / RECEIPT, "cases=2 observed_pass=2 observed_fail=0 mismatches=0\n")
    ctx.write(r / "a.txt", "replaced\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "receipt and replacement")
    new = ctx.git(r, "rev-parse", "HEAD").stdout.strip()
    ctx.git(r, "replace", old, new)
    return ["--lane", "repo", "--claims", CLAIMS, "--receipt", RECEIPT]
FIXTURES = [{"fid": "o08-order-replace-ref", "tool": "order", "expect": None, "defects": None, "build": build}]
```
