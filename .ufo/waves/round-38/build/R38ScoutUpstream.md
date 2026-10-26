# R38ScoutUpstream — upstream state of build-pmars (2026-10-26)

## Result: no drift in terminal-bench-2 (pin == main HEAD); terminal-bench-2-1 is a *different, modified* copy (2 of 5 files differ).

### 1. terminal-bench-2 main vs the five captures
- `gh api repos/harbor-framework/terminal-bench-2/commits/main --jq '.sha,.commit.committer.date'` -> `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, `2026-04-30T05:53:30Z` = the frozen pin. `git/ref/heads/main` same. No newer commit.
- `commits?path=build-pmars`: newest `2fd12b88` 2026-04-30 "Add task metadata to task manifests" (touches only build-pmars/task.toml); `8773c988` 2026-04-30 "Add task README and gitignore files" (adds .gitignore, README.md, task.toml); older: b3418b60 2025-10-31 "Update docker deployments", bb56a046, abd7e85f, 02550aa1, 090f4b12, 22a360eb, 13946e71, 50a87f95, 27799640, 38ca7295, 3dbbcbbe (12 commits total).
- Tree of `build-pmars` at pin and at main are identical (same 15 entries, same blob shas).
- curl raw from `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/main/build-pmars/<p>` + `cmp` vs capture dir:

| file | sha256 (main == capture == SHA256SUMS) | cmp | git blob (`git hash-object` of capture == upstream tree sha) |
|---|---|---|---|
| tests/test_outputs.py | d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85 | BYTE-EQUAL | 77b1730371cae257dda81ef4bca06a4f1bcb4399 |
| instruction.md | 1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82 | BYTE-EQUAL | c0a5ee023b498050537b075612850bb85ebb455c |
| tests/test.sh | 4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334 | BYTE-EQUAL | cb4a41a45e4b23f4d1f1392fd68f6e47c5dbbf57 |
| task.toml | 7ee2eac27b99fd462e0760552a430454db693f86608af5bb570b020270e4c9cd | BYTE-EQUAL | c8f00c82d45aa3168833b9f8f989bee7656f9060 |
| solution/solve.sh | 105292ca0e8bc399831550fc54c451002bd300644eb9beef1760dbfa7f8b7543 | BYTE-EQUAL | 870323f274603df6069ed709dcce284feffd785f |

`sha256sum *` in the capture dir reproduces SHA256SUMS lines for all five (the SHA256SUMS file itself is 3fd9de04…0bc). Drift: **none**.

### 2. terminal-bench-2-1 (404 explained)
- Repo exists: `harbor-framework/terminal-bench-2-1`, default `main`, HEAD `7131e4375048a0e408a8fb404b5f499d726b695b` (2026-08-11). Root contents: `.github .gitignore LICENSE README.md configs leaderboard tasks`.
- The 404 is a **path move, not a removal**: commit `5fc7d3b91d27ef0304b4eabe5002e6578160b817` (2026-05-05T19:27:44Z, "Move dataset files under tasks") moved `build-pmars/` -> `tasks/build-pmars/`. Earlier commit `320a8be8…` (2026-05-05 "Initial Terminal-Bench 2.1 snapshot") had it at the root. `curl .../main/build-pmars/tests/test_outputs.py` -> 404; `curl .../main/tasks/build-pmars/tests/test_outputs.py` -> 200. `contents/build-pmars` -> 404; `git/trees/HEAD?recursive=1` lists `tasks/build-pmars/...` (15 paths).
- README: "Terminal-Bench 2.1 is a more verified iteration… 26 tasks were modified" — build-pmars is one of the modified ones.
- Compare 2.1 `tasks/build-pmars` to the captures (cmp):
  - tests/test_outputs.py EQUAL (blob 77b17303… same), tests/test.sh EQUAL, task.toml EQUAL (blob c8f00c82…), environment/Dockerfile and warriors blobs equal to 2.0.
  - **instruction.md DIFF** (blob 11024115… vs c0a5ee02…). Only line 3 differs. Captured: "Extract the source to `/app` and build without X11 support. Install…". 2.1: "Extract the source to `/app/pmars-<version>/` and build from there without X11 support. Leave the source tree in place. Install…". Line numbering unchanged (same line count), so `instruction.md:<L>` anchors remain valid but line 3's text differs.
  - **solution/solve.sh DIFF** (blob 3eaec43d… vs 870323f2…): captured pins apt versions (`build-essential=12.12`, `libncurses-dev=6.5+20250216-2`, `ca-certificates=20250419`, `dpkg-dev=1.22.21`, `devscripts=2.25.15+deb13u1`) and has no trailing newline; 2.1 is unpinned and has a trailing newline. Oracle only; not graded.
- Implication: the grader (test_outputs.py) is identical in 2.0 and 2.1; the 2.1 instruction adds "source tree in place" but the tests contain no check of it, so it widens the instruction-vs-test gap (not the frozen claim).

### 3. Docker image tag
- captured task.toml:29 and 2.1 task.toml: `docker_image = "alexgshaw/build-pmars:20251031"` (same).
- Docker Hub `alexgshaw/build-pmars/tags`: `20260403` and `20260402` (digest sha256:5a975940…, pushed 2026-04-03), `20251031` (digest sha256:57a82706…, pushed 2025-10-31), `20251029` (same digest), `20251028` (b08ca032…). The task pins `20251031`; newer tags exist but neither upstream task.toml references them. [INFERENCE] the newer 2026-04 image is not what the pinned task uses.

### Commands (all run from /fast/scratch/hyaku/kengaku-r38/R38ScoutUpstream, since removed)
`gh api repos/harbor-framework/terminal-bench-2/commits/main`, `…/commits?path=build-pmars`, `…/git/trees/{main,2fd12b88…}:build-pmars?recursive=1`; `curl -sfL` raw + `cmp`/`sha256sum`/`git hash-object`; `gh api repos/harbor-framework/terminal-bench-2-1/{contents,commits,git/trees}`; `curl https://hub.docker.com/v2/repositories/alexgshaw/build-pmars/tags`.

VERDICT: upstream-drift-none (terminal-bench-2 pin==main, 5/5 byte-equal; terminal-bench-2-1 moved to tasks/ and carries a revised instruction.md + solve.sh, grader identical)
