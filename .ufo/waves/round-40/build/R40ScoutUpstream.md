# R40ScoutUpstream — upstream state of `db-wal-recovery` (2026-10-26)

Scope: compare the 8 captures in `corpus/evidence/round40/tb2-db-wal-recovery/` with upstream today; TB2.1; the docker image tag; Ubuntu 24.04 sqlite3 vs host 3.54.0. Read-only; nothing in the lane touched. Receipts: `.ufo/waves/round-40/build/R40ScoutUpstream/` (`diff.py`, `out-host.txt`, `out-ubuntu.txt`, registry manifests/configs).

## Verdict table

| Question | Result | Drift |
|---|---|---|
| 8 captures vs terminal-bench-2 `main` (raw) | byte-equal | none |
| terminal-bench-2 `main` vs pin `2fd12b88` | identical, ahead 0 behind 0 | none |
| Captures vs terminal-bench-2-1 `main` (`tasks/db-wal-recovery/`) | byte-equal (task exists there, unchanged) | none |
| Image tag in task.toml `alexgshaw/db-wal-recovery:20251031` | exists; baked `/app/main.db*` equal to captures | none (newer tags exist, see D1) |
| Ubuntu 24.04 sqlite3 vs host 3.54.0 | no observable difference on this task | none material (see D2) |
| Open upstream proposals | TB2.1 PR #3 (open, unmerged) changes the task | **D3: not drift, corroboration** |

Counted drift in the pinned artefacts: **0**. Three items to know about (D1-D3), none changes a capture, a hash or a frozen claim.

## 1. Captures vs upstream (commands + output)

`gh api repos/harbor-framework/terminal-bench-2/commits/main --jq .sha` → `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (= pin).
`gh api repos/harbor-framework/terminal-bench-2/compare/2fd12b88…...main --jq '[.status,.ahead_by,.behind_by]|@tsv'` → `identical 0 0`.
(`laude-institute/terminal-bench-2` resolves to the same repo; web URL `github.com/harbor-framework/terminal-bench-2`.)

History of the task path (`gh api "repos/…/commits?path=db-wal-recovery"`), newest first: `2fd12b88aafd 2026-04-30 Add task metadata to task manifests`; `8773c988e24e 2026-04-30 Add task README and gitignore files`; `b3418b600561 2025-10-31 Update docker deployments`; `bb56a0464c71 2025-10-30`; `abd7e85ffcfa 2025-10-29 Update tests and task.toml's`; `02550aa157a6 2025-10-28 Add docker images`; … `3dbbcbbedc34 2025-09-25 Initial commit`. The pin is the newest commit touching the task.

Fetch: `curl -sfL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/<main|2fd12b88…>/db-wal-recovery/<path>` for the 8 files (tests/→test.sh,test_outputs.py; environment/→Dockerfile,main.db,main.db-wal.encrypted; solution/→solve.sh; task.toml; instruction.md), then `sha256sum -c SHA256SUMS` from the capture dir's own SHA256SUMS:

```
Dockerfile: OK  instruction.md: OK  main.db: OK  main.db-wal.encrypted: OK
solve.sh: OK    task.toml: OK       test.sh: OK  test_outputs.py: OK      (main)
```
Same eight OK for the pinned-commit raw fetch and for the local capture dir. Per-file digests: test_outputs.py `88dc5c2a…2ba49`, instruction.md `5a203751…3b26`, main.db `68cb288e…d119`, main.db-wal.encrypted `68753bdc…9f5e8`... (full values in `SHA256SUMS`, unchanged).

Upstream tree size check: `gh api …/git/trees/2fd12b88…?recursive=1` lists the task as `.gitignore`(177), `README.md`(2040), the 8 captured files with the same byte sizes (Dockerfile 407, main.db 8192, wal 16512, solve.sh 3080, task.toml 926, test.sh 608, test_outputs.py 4263, instruction.md 658). **Upstream has two files the lane did not capture: `README.md` (2040 B) and `.gitignore` (177 B)** — metadata added 2026-04-30, not graded, not in the frozen "eight captures". Noted, not drift (the claim says 8 files).

## 2. terminal-bench-2-1

`harbor-framework/terminal-bench-2-1` exists (default branch main, pushed 2026-09-19; 91 tasks under `tasks/`). It contains `tasks/db-wal-recovery/` with the same 10 files/sizes. All eight captures verified against `…/terminal-bench-2-1/main/tasks/db-wal-recovery/*` with the lane's SHA256SUMS: **8/8 OK**. Its only commit on the task is `5fc7d3b91d27 2026-05-05 Move dataset files under tasks` (pure rename). README: "26 tasks were modified" for 2.1; this one is not among them. The task's `docker_image` is still `20251031` there.

**Bound for the entry:** the pin names TB2.0; the identical grader is also what TB2.1 serves today, so the entry can say so (observed 2026-10-26) without a second source row.

## 3. Image tag in task.toml

Docker Hub (`https://hub.docker.com/v2/repositories/alexgshaw/db-wal-recovery/tags`): tags and digests (amd64):

```
20251031 pushed 2025-10-31T02:52Z  sha256:0e33ea5ec823…  175272473 B   <- task.toml tag
20251029 / 20251028                sha256:1dfabf4908ad… / 0b91e31d2eb6…
20260403 / 20260402 pushed 2026-04-03 sha256:ca180acdafe7…  175448598 B
```
Manifest/config fetched with the anonymous registry token (no image pulled, no layer executed). Layers 4-5 of 20251031 are the two `COPY` steps; extracted and hashed: `/app/main.db 68cb288e…d119`, `/app/main.db-wal 68753bdc…9f5e8` = the captures exactly. Same for 20260403 (layers 4-5 hash identically). Config `history` shows `WORKDIR /app`, `COPY main.db /app/main.db`, `COPY main.db-wal.encrypted /app/main.db-wal`, `Cmd=/bin/bash`, base `ubuntu:24.04` — i.e. the captured Dockerfile.

**D1 — newer image tags exist but no upstream task file references them.** 20260402/20260403 are an April 2026 rebuild (same Dockerfile, newer Ubuntu base 2026-02-23): `dpkg` in the layer: sqlite3 and libsqlite3-0 `3.45.1-1ubuntu2.5` in BOTH tags; python3 `3.12.3-0ubuntu2` → `3.12.3-0ubuntu2.1`; xxd `2:9.1.0016-1ubuntu7.9` → `7.10`; python3-pip `24.0+dfsg-1ubuntu1.3` both. Task data bytes unchanged. Neither TB2 nor TB2.1 task.toml points at them (both say 20251031). Consequence: none for the grader or the sqlite behaviour; the entry should cite `:20251031` only.

## 4. Ubuntu 24.04 sqlite3 vs host 3.54.0

Facts: Ubuntu noble ships source `sqlite3 3.45.1`; Launchpad `getPublishedSources` for noble: `3.45.1-1ubuntu2.9` (proposed 2026-10-01), `…2.8` (updates/security 2026-09-16), `…2.5` (2025-09-15, the one in the 20251031 image, confirmed from the image's `/var/lib/dpkg/status`). `packages.ubuntu.com/noble/sqlite3` returned HTTP 500 at fetch time, so Launchpad was used. Host: `sqlite3 --version` → `3.54.0 2026-10-09 …`; host python 3.14.8, `sqlite3.sqlite_version` `3.54.0`. (Upstream has already shipped 3.54.1 on 2026-10-16: a 32-bit-only heap fix; host is one patch behind, irrelevant.)

Release-note scan (sqlite.org/changes.html, 3.45.1 < v <= 3.54.0, lines mentioning WAL/checkpoint): only
- 3.50.2: "Avoid writing frames with no checksums into the wal file if a savepoint is rolled back…" (write-side),
- 3.51.0: `PRAGMA wal_checkpoint=NOOP` / `SQLITE_CHECKPOINT_NOOP` (new, additive),
- 3.51.3 and 3.53.0: fix of the "WAL-reset bug" (wal.html#walresetbug: only with two or more connections writing/checkpointing at the same instant; backports to 3.44.6/3.50.7),
- 3.53.0: float-to-text rounding defaults to 17 significant digits (was 15) — affects text rendering of REAL values only; the task's values are INTEGER (probe below), so no effect, but a REAL-valued case would print differently on host 3.54 CLI vs Ubuntu 3.45.1 CLI.
Nothing changes WAL-header/salt/checksum validation, WAL recovery on open, or deletion of an invalid WAL at last-connection close.

Empirical differential (not just notes): the Ubuntu 3.45.1 `libsqlite3.so.0.8.6` extracted from the 20251031 layer was loaded in place of the host library (`LD_LIBRARY_PATH` to a dir holding only that lib) for host python, and the Ubuntu `sqlite3` CLI binary from the layer was run against it. `diff.py` (receipt dir) builds per-variant dirs from `main.db` + `main.db-wal.encrypted` (raw, XOR 0x42, XOR 0x41, XOR 0x00, truncated decrypted WAL) and opens each `mode=ro` and `mode=rw`:

```
$ diff <(sed 1d out-host.txt) <(sed 1d out-ubuntu.txt) && echo IDENTICAL-except-lib-line
IDENTICAL-except-lib-line
lib 3.54.0 / lib 3.45.1:  enc-none ro n=5  | enc-none rw n=5 and files after close = {main.db} only (WAL deleted)
xor42 ro n=11 (wal+shm remain) | xor42 rw n=11 (wal removed, main.db 8192) | xor41/xor00 n=5 | xor42-trunc-rw n=5
types: id integer, name text, value integer; journal_mode wal; page_size 4096
```
Both libraries agree row-for-row (hash `716723febb11` for 5 base rows, `92d53c65d741` for the 11 recovered rows), including the destructive-read behaviour (a plain read-write open of the encrypted WAL leaves only `main.db`) that C2's `plain-read-then-solve` rests on. The solve.sh CLI query `sqlite3 "file:main.db?mode=ro" "SELECT id,name,value …"` after XOR 0x42 printed byte-identical output (`cmp` → equal; 11 lines, `1|apple|150`).

**D2 — scope of this equivalence:** same-key behaviours on this one database/WAL pair on x86-64; it does not cover the python 3.12 (image) vs 3.14 (host) json/pytest versions, nor uvx's pytest 8.4.1 on python 3.13 (test.sh) — the probe uses the host interpreter, which is already a named limit in the claim.

## 5. Not-drift but relevant: open upstream PR corroborating the C2 trap

**D3 — terminal-bench-2-1 PR #3 (open, unmerged since 2026-05-21, updated 2026-06-11)** `fix(db-wal-recovery): Move encrypted WAL out of SQLite live sidecar path` by IsThatYou: changes `environment/Dockerfile` (`COPY main.db-wal.encrypted /app/main.db-wal.encrypted`) and `solution/solve.sh` (decrypt into `/app/main.db-wal`). Quote (PR body): "Opening the database with a normal read-write SQLite connection can truncate or remove that file…". It says the prompt and verifier are left unchanged, so the grader tests the probe measured are the same under it. This is independent upstream publication of the destructive-read trap and of agents losing "records 6 through 11 and the updated values for records 1 and 2". If merged, the live Dockerfile/solve.sh bytes of the task (not tests/instruction) would drift; the frozen pin is unaffected. Re-check before any later cite of "upstream main".

Also compared: Z.ai's `zai-org/terminal-bench-2-verified` (HF sha `2d28949d…`, lastModified 2026-08-24) carries `db-wal-recovery`: test_outputs.py, instruction.md, test.sh, solve.sh, main.db, main.db-wal.encrypted byte-equal to the captures; Dockerfile (+`procps python3 python3-pip`, "Claude Code KillShell" comment) and task.toml (own `xiangyangli/db-wal-recovery:20260204`, no schema 1.1 block) differ — a downstream variant, not the pinned source; the graded files S119/S120 match. `gh api "search/issues?q=repo:harbor-framework/terminal-bench-2+db-wal-recovery"` → 0 issues/PRs; TB2.1 → 15 hits, only #3 is about the task (rest are leaderboard submissions).

## Limits
Anonymous registry/Docker Hub metadata taken at fetch time; "no pull" held (two layers of ~145 MB were downloaded as blobs and read with tar, never run as an image). Network state, tags and PR status are as of 2026-10-26 ~13:40 -03 and can move. Scratch `/fast/scratch/hyaku/kengaku-r40/R40ScoutUpstream` removed at the end.

VERDICT: upstream-drift-none
