# R34 EvidenceBoundary — wave-tree trackedness evidence (C2 N1 support)

Role: leaf seat, evidence-boundary item. Reproduce the N1-class wave-tree trackedness
evidence at lane tip for wave dirs round-32 and round-33.

## Run

Command (verbatim, one shell invocation):

```
for d in .ufo/waves/round-32 .ufo/waves/round-33; do echo $d; find /home/vgpnk/Projects/shokunin/kengaku-shokunin/$d -type f | wc -l; git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-files $d | wc -l; git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain $d; done
```

Output (verbatim):

```
.ufo/waves/round-32
89
89
.ufo/waves/round-33
129
129
```

`git status --porcelain` printed **zero lines for both dirs** (no untracked, no
modified, no staged entries). `git --version` -> `git version 2.56.0`.

## Results

| Wave dir | files on disk (find) | tracked (ls-files) | untracked | porcelain |
|---|---|---|---|---|
| .ufo/waves/round-32 | 89 | 89 | 0 | empty |
| .ufo/waves/round-33 | 129 | 129 | 0 | empty |

- Untracked paths beneath either wave dir: **none** (expected: none).
- Total tracked counts: 89 (round-32), 129 (round-33).
- Git version: 2.56.0.

## Evidence retention

- Receipt saved at `.ufo/waves/round-34/build/R34EvidenceBoundary/wave-tree.txt`
  (command, verbatim output, and summary).
- No tools installed/updated (none needed; no pacman transactions).

## Notes

- Both wave dirs show files-on-disk == tracked, so no stray/untracked artifacts
  exist at tip in either dir — the N1-class wave-tree trackedness evidence reproduces
  cleanly at tip (C2 N1 support).
- Read-only: no writes to lane corpus/plans/scores; only this report + receipt.

VERDICT: evidence-boundary (untracked 0)
