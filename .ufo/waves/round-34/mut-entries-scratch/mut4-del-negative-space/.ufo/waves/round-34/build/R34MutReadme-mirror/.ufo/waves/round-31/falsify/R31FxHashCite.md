# Round 31 hash and citation falsification

## Commit identity and landing

- **Observed:** `dbb07364` resolves to commit `dbb0736459e0540a169a6d421ec6231734547378`. Command: `git cat-file -t dbb07364` returned `commit`; `git show -s --format=fuller dbb07364` returned the full hash and identities.
- **Observed author/committer:** both `kengaku-shokunin <kengaku@shokunin.local>`. Author date `Sun Oct 25 05:05:22 2026 -0300`; committer date `Sun Oct 25 06:01:14 2026 -0300`. Command: `git show -s --format=fuller dbb07364`.
- **Observed parent:** `0883e72ef8474ca42ac1a54eb0273079f1507035`. Command: `git rev-parse dbb07364^@`.
- **Observed ancestry:** `git merge-base --is-ancestor dbb07364 master` exited 0.
- **Observed files:** `git show --stat --format=medium dbb07364` includes `corpus/knowledge/benchmark-verifier-execution-model.md`, `corpus/SOURCES.md`, `corpus/README.md`, `plans/round31_defects.py`, and `plans/sources_adopt.py`. The same names were confirmed by `git show --format= --name-only dbb07364 -- <paths>`.
- **Observed local tip:** `git rev-parse master` → `dbb0736459e0540a169a6d421ec6231734547378`.
- **Observed local/remote equality:** `git rev-parse refs/heads/master` and `git rev-parse origin/master` both returned `dbb0736459e0540a169a6d421ec6231734547378`; equality test exited 0. Remote URL is `https://github.com/VeigaPunk/kengaku-shokunin.git` (`git remote -v`). This compares the local tracking ref, not a fresh network fetch.
- **Caveat:** checkout is detached at `dbb0736`, not on `master`; `git rev-parse '@{u}'` fails because HEAD is detached. `git status -sb` also showed working-tree changes/untracked files, including `corpus/SOURCES.md`, `plans/sources_adopt.py`, evidence files, and `.ufo/waves/round-31/falsify/`. Thus commit and branch refs are evidenced; current working tree is not clean and is not identical to committed content.

## Citation check

- **Observed entry citation bytes:** `corpus/knowledge/benchmark-verifier-execution-model.md:1-5` cites S092, S093, S100 with the three pinned commit IDs and `verified-at: 2026-10-25`. The source check is an observed read of the worktree entry; `git show --stat` confirms the entry file exists in `dbb07364`.
- **Not established by this assignment:** whether the quoted source spans actually occur in those pinned repositories, or whether the full R1-R10 closure and citation-bound gate behave correctly. The frozen claim source is `plans/round-31-claims.md:28-45` (C1), `:47-72` (C2), and `:74-95` (C3); these are not validated by commit identity alone.

VERDICT: Commit identity, ancestry, named file inclusion, and local-master/origin-master ref equality survived; source-quote validity, R1-R10 correctness, and citation-bound gate behavior remain untested here. The local working tree is dirty, so only committed bytes are covered by the hash checks.
