# C1ExecPopulationCheck — R52-C1 frozen population

Independently re-derived the population from the recursive GitHub tree at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` and compared it entry-by-entry with `plans/round52-tasks.json`.

- Recomputed task count: **89** top-level task directories (all contain `task.toml`). Frozen count: **89**.
- Recomputed eligible capture count: **184** (`test_outputs.py` 94, `test.sh` 89, `verify.sh` 1). Frozen count: **184**.
- Task-name differences: **none** (89/89 common).
- Capture-path differences: **none** (184/184 common; per-task capture lists also identical).
- All capture files fetched from the pin returned HTTP 200; each downloaded size and Git blob SHA-1 matched its tree entry (**184/184**, zero mismatch).
- Pin reachability: tree API HTTP **200**, commit API HTTP **200**, raw-file probe HTTP **200**. Recursive tree was not truncated. The `main` tree request returned HTTP 200 and had the same 1,446 paths and per-entry type/blob-SHA/size as the pinned tree (zero differences); remote tree content is unchanged at `main`.

The frozen JSON stores path lists, not per-entry SHA-256 values. Its SHA-256 is `0230b68c666c1e0649b42d61d7121a30eedf247411642bbf397e3390436b5cfc`. Per-entry SHA-256 and Git blob SHA-1 records for all 184 files are retained in `C1ExecPopulationCheck/artifacts/capture-digests.json` and the SHA256SUMS-format list in `C1ExecPopulationCheck/artifacts/capture-SHA256SUMS`.

The frozen `tasks` lists total 356 files and exactly match all tree blobs under a `tests/` path component. `capture_population` exactly matches those files filtered to the three frozen basenames under `<task>/tests/` or `<task>/environment/tests/`.

## Counter/control observation

The live counter changed while this seat was running; I re-read it before testing. Its current capture loop enumerates `capture_population`, normalizes `./` in SHA256SUMS paths, and on a clean scratch mini-lane populated from the fetch seat's artifacts printed `CAPTURES expected=184 present=184 mismatched=0`. Tampering with a primary grader produced `present=184 mismatched=1`.

One control-signature discrepancy remains: the frozen claim says dropping one captured grader must show `present=183 mismatched=1`. In a scratch mini-lane using the current counter, removing a primary capture file produced `present=183 mismatched=0`; removing a SHA256SUMS entry while retaining all files produced `present=184 mismatched=1`. Thus the stated pair does not match either single perturbation tested. The predicate failed in both cases. No lane file was edited by this seat.

## Exact commands / method

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r52/C1ExecPopulationCheck/tmp
curl -sS -o tree.json -w '%{http_code} %{size_download}\\n' -H 'Accept: application/vnd.github+json' 'https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1'
curl -fsS 'https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1' -o tree_claims_cmd.json
curl -sS -o repo.json -w 'repo_meta %{http_code}\\n' -H 'Accept: application/vnd.github+json' 'https://api.github.com/repos/harbor-framework/terminal-bench-2'
curl -sS -o head.json -w 'head_tree %{http_code}\\n' -H 'Accept: application/vnd.github+json' 'https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/HEAD?recursive=1'
curl -sS -o commit.json -w 'commit_api %{http_code}\\n' -H 'Accept: application/vnd.github+json' 'https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/2fd12b88aafdd04a52c298e3940bcb189f9766d6'
curl -sS -o /dev/null -w 'raw_probe %{http_code}\\n' 'https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/adaptive-rejection-sampler/tests/test.sh'
python3 recompute.py
python3 verify.py
```

`recompute.py` compared task names, all per-task capture paths, and the flattened capture set. `verify.py` fetched every frozen capture path at the pin and compared file size and Git blob SHA-1 (`sha1(b'blob '+len+b'\\0'+bytes)`) against the recursive tree. The full per-path fetch returned 200 for all 184 files. Final counter/control observations ran only in scratch mini-lanes. Unauthenticated GitHub API rate limit later returned HTTP 403 (remaining 0); the pin and HEAD results had already been recorded.

No tools were installed or updated. Scratch directory was removed before handoff.