# R39ScoutUpstream — upstream state of `git-leak-recovery` (2026-10-26)

Question: do the seven captures in `corpus/evidence/round39/tb2-git-leak-recovery/` still match terminal-bench-2 `main`, terminal-bench-2-1, and what is the task.toml image tag.
Read-only; scratch `/fast/scratch/hyaku/kengaku-r39/R39ScoutUpstream` (fetched files only). Nothing in the lane written except this report.

## Result: no drift in the pinned task files. Three provenance notes below.

### 1. terminal-bench-2 `main` vs pin (observed)
```
$ gh api repos/laude-institute/terminal-bench-2/commits/main --jq '.sha+" "+.commit.committer.date'
2fd12b88aafdd04a52c298e3940bcb189f9766d6 2026-04-30T05:53:30Z      # == pinned S117/S118 commit
$ gh api 'repos/laude-institute/terminal-bench-2/commits?path=git-leak-recovery&per_page=20' ...
2fd12b88 2026-04-30 Add task metadata to task manifests   (newest; touches the task dir)
8773c988 2026-04-30 Add task README and gitignore files
b3418b60 2025-10-31 Update docker deployments
bb56a046 2025-10-30 Fix dockerfiles.
abd7e85f 2025-10-29 Update tests and task.toml's.  ... (12 commits total, back to 3dbbcbbe 2025-09-25)
$ gh api repos/laude-institute/terminal-bench-2 --jq '.full_name+" "+.pushed_at+" "+.default_branch'
harbor-framework/terminal-bench-2 2026-04-30T05:53:32Z main
```
`main` HEAD **is** the pinned commit; no commit after it exists. Note: the repo has been renamed/transferred — `laude-institute/terminal-bench-2` resolves to `harbor-framework/terminal-bench-2` (the API reports the new full_name; old URL still serves).

### 2. Byte comparison of the seven captures (observed)
Raw files fetched from `https://raw.githubusercontent.com/laude-institute/terminal-bench-2/main/git-leak-recovery/{instruction.md,task.toml,environment/Dockerfile,environment/challenge-setup.sh,solution/solve.sh,tests/test.sh,tests/test_outputs.py}`, `sha256sum`, then `diff main.sums SHA256SUMS` → `IDENTICAL`; `sha256sum -c SHA256SUMS` in the capture dir → 7× `OK`.
```
006bf5d2…cc112  Dockerfile
a0a19652…2b23e2 challenge-setup.sh
54ac693f…a5861  instruction.md      (S118)
791a7eb2…14dd   solve.sh
d7f23fda…3044   task.toml
4770437e…6334   test.sh
dc7b01c1…c775   test_outputs.py     (S117)
```
Independent git-blob check: `git hash-object` of each capture equals the blob sha in the tree of pinned commit 2fd12b88 (`gh api …/git/trees/2fd12b88…?recursive=1`): Dockerfile 0d82d9dc, challenge-setup.sh a3d6ab23, instruction.md c1fe9cb6, solve.sh 2e744693, task.toml 139ada99, test.sh cb4a41a4, test_outputs.py 30ee951b — all 7 equal. Tree for `git-leak-recovery/` on `main` is `dffced9d…`, same blobs. Upstream task dir additionally holds `.gitignore` (ecd089e8) and `README.md` (e69bd204), both added 2026-04-30 by 8773c988 and not captured (neither is a grader input).

### 3. terminal-bench-2-1 (observed)
Location: `harbor-framework/terminal-bench-2-1` (not `laude-institute/…`, which 404s), `main` = `7131e437` 2026-08-11, path `tasks/git-leak-recovery/`. Its README: "26 tasks were modified … to fix bugs … or improve robustness to reward hacking" — git-leak-recovery is **not** among the modified ones as far as the files show.
```
tasks/git-leak-recovery            dffced9d…   (same tree sha as TB2 main)
tasks/…/{Dockerfile 0d82d9dc, challenge-setup.sh a3d6ab23, instruction.md c1fe9cb6, solve.sh 2e744693,
         task.toml 139ada99, test.sh cb4a41a4, test_outputs.py 30ee951b, README e69bd204, .gitignore ecd089e8}
```
Raw-fetched 2.1 files, `sha256sum | diff - main.sums` → `2.1-IDENTICAL-TO-CAPTURES`. Only commit touching the path: `5fc7d3b9` 2026-05-05 "Move dataset files under tasks" (pure move). So the grader the lane pins is byte-identical in TB 2.1.

### 4. Docker image tag
`task.toml` (capture, TB2 main and TB2.1 alike): `docker_image = "alexgshaw/git-leak-recovery:20251031"`.
Docker Hub (`hub.docker.com/v2/repositories/alexgshaw/git-leak-recovery/tags`):
```
20260403  2026-04-03  sha256:e925c4db…1ca9
20260402  2026-04-03  sha256:e925c4db…1ca9   (same digest)
20251031  2025-10-31  sha256:62160e52…e586   <- referenced by task.toml
20251029  2025-10-29  sha256:62160e52…e586   (same digest)
20251028  2025-10-28  sha256:09bb8f20…429d
```
**Note A:** two newer tags (20260402/03, one digest) exist on the registry, but no tracked task.toml references them; not pulled (the lane never pulls the image), so whether their content differs is unknown. The pin `20251031` still exists and is not moved (amd64 digest above).

### 5. Variant elsewhere (not drift of the pin)
`zai-org/terminal-bench-2-verified` (HF dataset) carries its own `git-leak-recovery/` with the same `instruction.md`, `challenge-setup.sh`, `solve.sh`, `test.sh`, `test_outputs.py` (sha256 identical to captures) but a different `Dockerfile` (adds `RUN apt-get update && apt-get install -y procps python3 python3-pip`, sha ab9c1416…0594) and `task.toml` (`version = "1.0"`, image `xiangyangli/git-leak-recovery:20260204`, sha 580306fc…5b3b). Graded files are unchanged.

## Drift tally
- Pinned-commit vs `main`: 0 files differ (HEAD == pin).
- vs TB 2.1: 0 files differ.
- Items worth a provenance line in the entry (non-drift): repo transfer to `harbor-framework/` (**Note B**); TB2.1 carries the identical task (**Note C**); newer unreferenced image tags (Note A).

Limits: Docker Hub tag list read for the five newest tags only (page_size=20 returned 5); image never pulled; HF zai copy fetched from `resolve/main` (floating ref, not pinned).

VERDICT: upstream-drift-none
