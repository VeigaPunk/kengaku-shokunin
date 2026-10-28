# C1ExecPopulationCheck — R52-C1 frozen population

## Result

Independently re-derived the population from the recursive GitHub tree at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` and compared it entry-by-entry with `plans/round52-tasks.json`.

- Recomputed task count: **89** top-level task directories (all contain `task.toml`). Frozen count: **89**.
- Recomputed eligible capture count: **184** (`test_outputs.py` 94, `test.sh` 89, `verify.sh` 1). Frozen count: **184**.
- Task-name differences: **none** (89/89 common).
- Capture-path differences: **none** (184/184 common; per-task capture lists also identical).
- All capture files fetched from the pin returned HTTP 200; each downloaded size and Git blob SHA-1 matched its tree entry (**184/184**, zero mismatch).
- Pin reachability: tree API HTTP **200**, commit API HTTP **200**, raw-file probe HTTP **200**. Recursive tree was not truncated. The `main` tree request returned HTTP 200 and had the same 1,446 paths and per-entry type/blob-SHA/size as the pinned tree (zero differences); remote tree content is unchanged at `main`.

The frozen JSON stores path lists, not per-entry SHA-256 values. Its SHA-256 is `0230b68c666c1e0649b42d61d7121a30eedf247411642bbf397e3390436b5cfc`. I retained SHA-256 and Git blob SHA-1 for each of the 184 capture files in the artifact below.

## Population comparison

The frozen `tasks` lists total 356 files and exactly match all tree blobs under a `tests/` path component. The frozen `capture_population` is exactly that population filtered to basenames `test_outputs.py`, `test.sh`, and `verify.sh` under the task test directories. No out-of-manifest or missing paths were found. The capture basename breakdown matches the claims: 94 / 89 / 1.

## Counter/control observation

The live counter changed while this seat was running; I re-read it before testing. Its current capture loop enumerates `capture_population`, normalizes `./` in SHA256SUMS paths, and on a clean mini-lane populated from the fetch seat's artifacts printed `CAPTURES expected=184 present=184 mismatched=0`. Tampering with a primary grader produced `present=184 mismatched=1`.

One control-signature discrepancy remains: the frozen claim says dropping one captured grader must show `present=183 mismatched=1`. In a scratch mini-lane using the current counter, removing a primary capture file produced `present=183 mismatched=0`; removing a SHA256SUMS entry while retaining all files produced `present=184 mismatched=1`. Thus the control's stated pair of numbers does not match either single perturbation tested. The predicate still failed in both cases. No lane file was edited by this seat.

## Exact commands / method

Commands run (all work products and temporary files were under this seat's scratch directory; no package/tool installs):

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r52/C1ExecPopulationCheck/tmp
curl -sS -o tree.json -w '%{http_code} %{size_download}\\n' -H 'Accept: application/vnd.github+json' \
  'https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1'
curl -fsS 'https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1' -o tree_claims_cmd.json
curl -sS -o repo.json -w 'repo_meta %{http_code}\\n' -H 'Accept: application/vnd.github+json' 'https://api.github.com/repos/harbor-framework/terminal-bench-2'
curl -sS -o head.json -w 'head_tree %{http_code}\\n' -H 'Accept: application/vnd.github+json' 'https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/HEAD?recursive=1'
curl -sS -o commit.json -w 'commit_api %{http_code}\\n' -H 'Accept: application/vnd.github+json' 'https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/2fd12b88aafdd04a52c298e3940bcb189f9766d6'
curl -sS -o /dev/null -w 'raw_probe %{http_code}\\n' 'https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/adaptive-rejection-sampler/tests/test.sh'
python3 recompute.py
python3 verify.py
```

`recompute.py` derived task directories from top-level tree entries of type `tree`; selected capture blobs by the three frozen basenames under `<task>/tests/` or `<task>/environment/tests/`; flattened and compared task and capture sets and per-task lists against both frozen JSON maps. `verify.py` fetched each frozen capture path from `raw.githubusercontent.com` at the pin, calculated SHA-256 and Git blob SHA-1 (`sha1(b'blob '+len+b'\\0'+bytes)`), and compared Git blob SHA-1 and size to the recursive tree entries.

The full capture fetch used one `curl` per frozen path, with each HTTP status recorded. The final counter/control observations were run against scratch mini-lanes populated from the sibling fetch seat's retained capture artifacts, not against the lane tree.

During follow-up, unauthenticated GitHub API requests reached the core rate limit (HTTP 403, remaining 0); the pinned tree, commit, raw probe, and HEAD-tree results above had already been recorded successfully.

## Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecPopulationCheck/report.md` — this report.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecPopulationCheck/artifacts/capture-digests.json` — 184 path/size/SHA-256/Git-blob-SHA-1 records; SHA-256 `a33c06ad5728bc744fb8a00c2013b90f6f44fbf9fe3c7eda1d76b2d2eea90097`.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecPopulationCheck/artifacts/capture-SHA256SUMS` — 184 SHA-256/path lines; SHA-256 `d899604b1b259097b48eb2b9effb34c44220a77f8744d65429d470615fff77ae`.

No tools were installed or updated. Scratch directory was removed before handoff.