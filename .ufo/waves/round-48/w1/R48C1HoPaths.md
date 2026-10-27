# R48C1HoPaths — benign repository layouts

Axes: calibration (primary); filesystem-path coverage (evidence family).

## Result

At frozen stage-1 revision `a543d92083557dd9b33ee674e9b99b03411f80af`, direct calls to the base fence on scratch-only ordinary Git fixtures gave:

- A nested repository beneath a non-repository fixture directory, selected as `--lane`: **ADMIT**.
- A regular tracked worktree file plus a relative symlink to that same file, both inside `d`: **REFUSE: `tracked-link.txt is a symlink`**.

The symlink is a benign, contained target; no outside path is involved. This is a concrete positive-control gap for calibration if that ordinary layout is part of the frozen honest population. The code explicitly refuses every symlink during `_tree`; this result is an implementation disposition, not a scored counter result or claim admission. The nested-repository observation shows that a nested repo alone is accepted when no outer repo is required. An additional diagnostic fixture with both an outer and nested repository was refused because the runner's inherited Git `rerere` behavior left `MERGE_RR`; that contaminated result is excluded from the disposition finding.

Smallest safe correction: include the contained-symlink case in the stage-2 honest fixtures and make the fence admit a symlink only after proving its resolved target remains inside `d` (while continuing to refuse escapes, dangling links, loops, and any traced outside access). Do not treat the nested-repository result as a guarantee for all nested layouts.

## Evidence and exact commands

Freeze verification, before measurements:

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
# git log --oneline -5
# git cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af
# git log -1 --format='%H %ci %s' a543d92083557dd9b33ee674e9b99b03411f80af
# git show a543d92083557dd9b33ee674e9b99b03411f80af:plans/round-48-claims.md | head -5
# git ls-tree a543d92083557dd9b33ee674e9b99b03411f80af plans/round-48-claims.md
```

Observed: `a543d92 round-48: stage-1 freeze...`; object type `commit`; commit time `2026-10-27 06:53:29 -0300`; the claims blob exists at that revision. Clone and measured revision:

```sh
S=/fast/scratch/hyaku/kengaku-r48/R48C1HoPaths
export TMPDIR="$S"
cd "$S"
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C "$S/lane" checkout --detach a543d92083557dd9b33ee674e9b99b03411f80af
TOP=$(git -C "$S/lane" rev-parse --show-toplevel)
test "$TOP" = "$S/lane"
git -C "$S/lane" rev-parse HEAD
```

Observed verbatim: `TOP=/fast/scratch/hyaku/kengaku-r48/R48C1HoPaths/lane`; `REV=a543d92083557dd9b33ee674e9b99b03411f80af`; fence SHA-256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`.

Disposition command (the script was scratch-only; it imported the cloned `plans/fixture_fence.py`, created commits in scratch fixtures using `git -C "$D" ...`, verified `rev-parse --show-toplevel` equalled each `$D` before every fixture write, then called `breach(d, ['--lane', str(lane)], 'anchor')` directly):

```sh
S=/fast/scratch/hyaku/kengaku-r48/R48C1HoPaths
export TMPDIR="$S"
python3 "$S/disposition.py"
```

Final output, verbatim:

```text
repo git-dir-entries: ['COMMIT_EDITMSG', 'HEAD', 'config', 'index', 'logs', 'objects', 'refs']
nested-repository-in-nonrepo-fixture: ADMIT
symlink5 git-dir-entries: ['COMMIT_EDITMSG', 'HEAD', 'config', 'index', 'logs', 'objects', 'refs']
in-tree-symlink-to-tracked-file: REFUSE: tracked-link.txt is a symlink
```

The script created the nested fixture with `git init -q --template=/dev/null`, local temporary identity and `rerere.enabled=false`; after commit it removed those temporary config keys. Its symlink fixture used the same process and `tracked-link.txt -> tracked.txt`. No counter, probe, strace envelope, or claimed-work execution was run. `REV` measured: `a543d92083557dd9b33ee674e9b99b03411f80af`.

Limits: only these two layout shapes were measured; no escaping, dangling, cyclic, absolute, directory, or cross-mount symlink case was tested. The nested-repository-in-nonrepo result does not establish acceptance when another enclosing repository is present. The initial enclosing-repo diagnostic was contaminated by environment-generated `MERGE_RR`/`rerere` state and is not used as evidence. No external sources were opened.

## Local sources opened

Access date for each: 2026-10-27. URLs are file URIs because the evidence sources are local repository files.

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — quote: “novel honest classes authored by wave-1 critic seats” (§C1 counter, stage-2 honest population).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — quote: “9/9 novel honest fixtures refused” (§Routed defects, C1).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w2/R46W2C1HoPaths.md` — quote: “The first three were rejected by the fence; the newline fixture was admitted.” (line 5).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixture_fence.py` — quote: “one walk of `d` proves the tree has no symlink and no special file anywhere” (line 22).

VERDICT: benign nested repository admitted; contained symlinked worktree file refused. This is a calibration-relevant honest-control counterexample for stage 2, not a scored verdict or admission claim.