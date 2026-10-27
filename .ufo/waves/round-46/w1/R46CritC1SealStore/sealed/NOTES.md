# Sealed store-indirection modules

All fixtures use the round-45 `build(ctx, d)` module contract, create a valid committed lane repo, then move one internal Git store component to a sibling of the fixture directory and symlink its original location there. The fence's `os.walk` deliberately prunes `.git`, and its explicit store checks do not cover these paths. Git invoked by the fence follows the symlinks.

- `objects_link.py`: relocate `.git/objects` as a directory symlink; fence's probes and order blob checks open object storage outside `d`.
- `refs_link.py`: relocate `.git/refs` as a directory symlink; fence's Git probes follow refs outside `d`.
- `packed_refs.py`: replace `.git/packed-refs` by a symlink to a sibling file; fence's Git probes read packed refs outside `d`.

The `.git/HEAD` symlink experiment was not retained: under the base counter it was refused (Git could not describe the worktree), so it was clean, not an advertised breach.
