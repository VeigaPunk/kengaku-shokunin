# R31FxSweep731 — independent manifest sweep

## Scope and method

I independently re-enumerated both pinned Git trees and fetched **all 731 task manifests** (not a sample): Terminal-Bench 2.0 at `2fd12b88aafdd04a52c298e3940bcb189f9766d6` and SWE-bench Pro V2 at `66f92766bba642462d4bbe5479e83f91f9211862`.

Commands, run from `/tmp/r31fx-Sweep731/`:

- `gh api --paginate "/repos/laude-institute/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1" > tb2_tree.json` and the equivalent `gh api --paginate "/repos/scaleapi/SWE-bench_Pro-os/git/trees/66f92766bba642462d4bbe5479e83f91f9211862?recursive=1" > swe_tree.json`; both returned `truncated: false`, with 1,446 and 16,077 entries respectively.
- Python enumeration of `type == 'blob'` paths ending in `task.toml` found **89** TB2 manifests and **642** SWE-bench manifests. The extra `.toml` files were `modernize-scientific-stack/environment/pyproject.toml` in TB2 and `v2/tooling/configs/codex_config.toml` in SWE-bench; neither is a `task.toml`.
- A Python `urllib.request` sweep fetched raw `task.toml` bytes at each pinned revision using 24 concurrent workers. Output: `fetched: 731 errors: 0` (`TOTAL 731 SUCCESS 731`). The script scanned line-anchored TOML declarations for `environment_mode =`, `[verifier.environment]`, `[steps.verifier]`, and `[[steps]]`.

## Results

| Manifest field/table | Hits / fetched manifests |
|---|---:|
| `environment_mode` assignment | **0 / 731** |
| `[verifier.environment]` | **0 / 731** |
| `[steps.verifier]` | **0 / 731** |
| `[[steps]]` | **0 / 731** |

This reproduces the entry’s claim at `corpus/knowledge/benchmark-verifier-execution-model.md:112-117`: the entry says the sweep covered all 731 pinned `task.toml` files and found no `environment_mode`, `[verifier.environment]`, or `[steps.verifier]`. It does **not** overstate the measured count or coverage: I fetched and checked every enumerated task manifest, not merely a sample. The sweep establishes these absences at those two pinned trees only; it does not establish anything about later revisions or task behavior at runtime.

## VERDICT: The 731-manifest sweep survived; the entry's sentence does not overstate what was measured at the stated pins.
