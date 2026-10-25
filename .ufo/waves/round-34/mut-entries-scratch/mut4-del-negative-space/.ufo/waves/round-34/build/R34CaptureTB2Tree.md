# Terminal-Bench 2.0 pinned tree census

Captured API response at `.ufo/waves/round-34/assimilation/captures/tb2-tree.json`.

- Command: `curl -fsSL 'https://api.github.com/repositories/1063848495/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6' -o /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/tb2-tree.json`
- Output: no stdout; command returned successfully.
- Command: `jq -r '"sha=" + .sha, "total=" + (.tree|length|tostring), "task_dirs=" + ([.tree[] | select(.type=="tree" and (.path as $p | [".gitignore","LICENSE","README.md"] | index($p) | not))] | length | tostring), "owner_url=" + (.url // "")' /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/tb2-tree.json`
- Output:
```text
sha=2fd12b88aafdd04a52c298e3940bcb189f9766d6
total=92
task_dirs=89
owner_url=https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6
```

The captured `sha` matches the pinned commit. API URL identifies canonical owner/repository as `harbor-framework/terminal-bench-2`. The tree has 92 top-level entries total and 89 top-level `tree` task entries after excluding `.gitignore`, `LICENSE`, and `README.md` from task-dir counting.

VERDICT: tb2-tree-89
