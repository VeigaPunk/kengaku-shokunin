# R37ReopenPins — independent reopen of the pinned TB2 `configure-git-webserver` sources

Seat: executor, kengaku round 37 wave 1 (2026-10-26). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: re-open the six pinned upstream files from the network (not from the lane's captures), byte-compare,
verify the capture manifest, confirm the pin, list the task directory at the pin, check `main` drift, and
quote the entry's anchors against the reopened bytes.

Artifacts in this directory: `instruction.md`, `task.toml`, `tests/{test_outputs.py,verify.sh,test.sh}`,
`solution/solve.sh` (fresh `curl -fsSL` bytes, 2026-10-26 04:37Z) and `reopen-verify.txt` (transcript of the
commands whose output is quoted below). Scratch `/fast/scratch/hyaku/kengaku-r37/R37ReopenPins/` was removed
after copying `reopen-verify.txt`.

## 1. Fetch — 6/6 files retrieved

```
$ B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver
$ curl -fsSL --max-time 40 "$B/$f" -o "$f"
OK tests/test_outputs.py 547
OK tests/verify.sh 2681
OK tests/test.sh 553
OK instruction.md 451
OK task.toml 932
OK solution/solve.sh 2354
```
Sizes equal the lane-capture sizes (`ls -la corpus/evidence/round37/tb2-git-webserver/`: 547, 2681, 553, 451,
932, 2354).

## 2. Byte identity — 6/6 identical, manifest clean

```
$ for f in ...; do cmp -s "$f" "$C/$(basename $f)" && echo "IDENTICAL $b"; done
IDENTICAL test_outputs.py
IDENTICAL verify.sh
IDENTICAL test.sh
IDENTICAL instruction.md
IDENTICAL task.toml
IDENTICAL solve.sh

$ cd corpus/evidence/round37/tb2-git-webserver && sha256sum -c SHA256SUMS
instruction.md: OK      solve.sh: OK      task.toml: OK
test.sh: OK             test_outputs.py: OK   verify.sh: OK
exit=0
```

Stronger than a content diff: the reopened bytes hash to the **git blob ids of the tree at the pin**
(`git ls-tree -r 2fd12b88 -- configure-git-webserver/`), so they are the commit's own objects, and the
sha256 values equal the `SHA256SUMS` entries:

| file | bytes | git blob (tree at pin) | sha256 (= SHA256SUMS) |
|---|---|---|---|
| tests/test_outputs.py | 547 | 8036593f765683db7b05911aa13e0730b8192e85 | 526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37 |
| tests/verify.sh | 2681 | 14240adce74367a816e1a24827e0b97bfa8886f2 | 1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05 |
| tests/test.sh | 553 | 44b2368195a38a62131438cda072ad6f6d52a055 | afafc3ffdaf911f7a93003c0746f217188099c174e5d3eb7dada17133df15895 |
| instruction.md | 451 | 2c2f4e6f81b08f7041250143d59ca8c6dafab828 | 62151b7371bc364277a3c118bba755334c640fb0cefc7a5af106e6e763cf1d97 |
| task.toml | 932 | f2e7ecdee53ae81d5afa928333908e3e7945f386 | ebb40d72f689512cbd90d865d88ef966b6665ab215544f9247b898b7fa94751b |
| solution/solve.sh | 2354 | f73a50bebd374ff6d0a0322fa991d5fc37dce4d0 | c31cd92ecb1b357d8c0abcf4821717e83a1770cf58f028620cd0ee3e6b1e4c62 |

Byte-level details the captures preserved correctly: `tests/verify.sh` has **no final newline** (last 16 bytes
`225465737420636f6d706c6574656422` = `"Test completed"`); `tests/test_outputs.py` and `instruction.md` end with
`\n`. The captures are the upstream bytes, not a re-serialisation.

## 3. Commit confirmation

`https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/2fd12b88…` returned **HTTP 403, API
rate limit exhausted** for this egress IP — not a repository defect:

```
HTTP/2 403
x-ratelimit-limit: 60   x-ratelimit-remaining: 0   x-ratelimit-used: 60
x-ratelimit-reset: 1792991234      ($ date -u -d @1792991234 -> 2026-10-26T05:07:14Z)
{"message":"API rate limit exceeded for 179.218.13.209. ..."}
```
No token was available (credentials are shape-only for this seat), so the commit was confirmed from two
GitHub-served, non-API sources that carry the same object identity:

```
$ git fetch --depth 1 --filter=blob:none origin 2fd12b88aafdd04a52c298e3940bcb189f9766d6   # fetch_exit=0
$ git cat-file commit 2fd12b88… | git hash-object -t commit --stdin
recomputed_commit_hash=2fd12b88aafdd04a52c298e3940bcb189f9766d6     # self-hash matches: content unmodified
$ git cat-file commit 2fd12b88… | sed -n '1,6p'
tree ec7c02c7f0b59ce8ed2f7c88d1e70cda7427edfa
parent 8773c988e24ef3ce9773073036892897de260014
author Alex Shaw <alexgshaw64@gmail.com> 1777528410 -0700
committer Alex Shaw <alexgshaw64@gmail.com> 1777528410 -0700

Add task metadata to task manifests
```
and `https://github.com/harbor-framework/terminal-bench-2/commit/2fd12b88….patch` (`bytes=113174`):
```
From 2fd12b88aafdd04a52c298e3940bcb189f9766d6 Mon Sep 17 00:00:00 2001
From: Alex Shaw <alexgshaw64@gmail.com>
Date: Wed, 29 Apr 2026 22:53:30 -0700
Subject: [PATCH] Add task metadata to task manifests
```
**Date 2026-04-29 22:53:30 −0700, message "Add task metadata to task manifests", author/committer Alex Shaw.**
Commit object date is 1777528410 −0700 = 2026-04-29T22:53:30−07:00. The commit is a repo-wide metadata sweep
(the `.patch` index starts with `adaptive-rejection-sampler/task.toml` … `build-pov-ray/task.toml`), i.e. the pin
is not a task-specific edit.

## 4. Directory listing at the pin — 9 files, 3 not captured

```
$ git ls-tree -r --full-tree 2fd12b88… -- configure-git-webserver/
100644 blob ecd089e8ac7767b9bdb6f3ac247c8d033f7565ab  configure-git-webserver/.gitignore
100644 blob eb6037662039089afc3552694545bd9a719e0894  configure-git-webserver/README.md
100644 blob 56406ebd3e6fb8a5483551c27356000f6dd5e1d2  configure-git-webserver/environment/Dockerfile
100644 blob 2c2f4e6f81b08f7041250143d59ca8c6dafab828  configure-git-webserver/instruction.md
100644 blob f73a50bebd374ff6d0a0322fa991d5fc37dce4d0  configure-git-webserver/solution/solve.sh
100644 blob f2e7ecdee53ae81d5afa928333908e3e7945f386  configure-git-webserver/task.toml
100644 blob 44b2368195a38a62131438cda072ad6f6d52a055  configure-git-webserver/tests/test.sh
100644 blob 8036593f765683db7b05911aa13e0730b8192e85  configure-git-webserver/tests/test_outputs.py
100644 blob 14240adce74367a816e1a24827e0b97bfa8886f2  configure-git-webserver/tests/verify.sh
(9 entries)
```
Captured: 6/9 (the six above). **Not captured, and whether it matters to the grader** (all three were fetched
too; blob ids match `ecd089e8…`, `eb603766…`, `56406ebd…`):

1. `.gitignore` (177 B) — repo hygiene only (`.git/`, `.DS_Store`, `__pycache__/`, `node_modules/`, `.env`,
   `dist.tar.gz`). **No grader impact**: nothing in `tests/` reads it.
2. `README.md` (1772 B) — prose. Says base image Ubuntu 24.04, "Pre-installed tools: curl", internet enabled,
   timeout 15 minutes, and describes verification as "Verifies that `http://localhost:8080/hello.html` returns
   `hello world` with HTTP 200 status". **No verdict impact** (never read at grading), but it is the upstream
   statement that curl is preinstalled — see item 3.
3. `environment/Dockerfile` (195 B) — `FROM ubuntu:24.04`, `WORKDIR /app`, `RUN apt update -y && apt install -y
   curl` (lines 2–5). **Matters to interpreting the grader, not to the verdict path**: the only content it
   installs is curl, so in this image `command -v curl` at `verify.sh:55` is always true and the wget fallback
   (`verify.sh:73-89`) is unreachable during real grading. Caveat: `task.toml:29` pins
   `docker_image = "alexgshaw/configure-git-webserver:20251031"`, so the built-at-grading image is the published
   artifact, not necessarily this Dockerfile; the Dockerfile still documents the intended environment (apt +
   network, which `verify.sh:5-6` depends on for `expect`).

Consequence for the receipt: its three `tools=wget` cases (`wget-static-file`, `wget-404`, `wget-token-in-body`;
`grep -c 'tools=wget' …probe.txt` → `3`, against 19 `tools=curl`) exercise a branch that is **counterfactual
under the official image** (it needs curl removed).
They remain valid as readings of `verify.sh:73-89`; they are not the path the graded run takes. The `curl`
branch is the graded one.

## 5. Drift against `main` — none

```
$ git ls-remote origin refs/heads/main HEAD
2fd12b88aafdd04a52c298e3940bcb189f9766d6	HEAD
2fd12b88aafdd04a52c298e3940bcb189f9766d6	refs/heads/main
$ git fetch --depth 1 origin main:refs/remotes/origin/main && git rev-parse refs/remotes/origin/main
2fd12b88aafdd04a52c298e3940bcb189f9766d6
$ git diff --stat 2fd12b88… refs/remotes/origin/main -- configure-git-webserver/     # empty, exit 0
$ for f in ...; curl -fsSL https://raw.githubusercontent.com/…/main/configure-git-webserver/$f | cmp -s - $f
MAIN==PINNED tests/test_outputs.py
MAIN==PINNED tests/verify.sh
MAIN==PINNED tests/test.sh
MAIN==PINNED instruction.md
MAIN==PINNED task.toml
MAIN==PINNED solution/solve.sh
```
`main` (11 heads; default HEAD is `main`) is **at the pinned commit itself**, so the six files are identical on
`main` and the drift count is 0/6. Drift note, not a defect: because the pin is the branch tip, this check
cannot distinguish "pinned to an old commit" from "pinned to today's branch"; it does establish that nothing in
this task changed upstream between the pin (2026-04-29) and today (2026-10-26). Pin freshness today is maximal.

## 6. Anchors for the entry, quoted from the reopened bytes

Line numbers verified with `cat -n` on the freshly fetched files (identical to the captures); each quote ≤25
words, `file:line`.

| anchor | quote | what it supports |
|---|---|---|
| `tests/test_outputs.py:13` | `assert "TEST PASSED" in result.stdout, "Did not pass test"` | the whole verdict is one substring test over `verify.sh` stdout |
| `tests/verify.sh:49` | `./git_test.exp` | the expect driver is invoked and its **exit status is never read** (branch at :51 tests only the web server) |
| `tests/verify.sh:57` | `HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/hello.html)` | the first request: status only, body discarded, no `-L`, no `--max-time` |
| `tests/verify.sh:60` | `CONTENT=$(curl -s http://localhost:8080/hello.html)` | the second, separate request; command substitution strips trailing newlines |
| `tests/verify.sh:62` | `echo "Content: $CONTENT"` | the body is echoed into stdout, where the substring test at `test_outputs.py:13` reads it |
| `tests/verify.sh:63` | `if [ "$CONTENT" = "hello world" ]; then` | the only content comparison: exact, case- and whitespace-sensitive |
| `tests/verify.sh:75` | `wget -q -O test_output.html http://localhost:8080/hello.html` | the curl-absent branch (unreachable on the official image, §4 item 3) |
| `instruction.md:1` | `Configure a git server so that I can run on my computer` | the instruction's first requirement: a *git server* |
| `instruction.md:7` | `And have this data then be pushed to a webserver running on port 8080 so if I run` | the push → port-8080 deployment requirement, untested by the grader |
| `instruction.md:9` | `then I see the output "hello world".` | the literal body expectation the grader enforces (and the only requirement it does enforce end-to-end) |

Cross-check of the receipt's own anchors: `grep -o 'verify\.sh:[0-9,-]*\|test_outputs\.py:[0-9]*\|instruction\.md:[0-9,-]*' corpus/evidence/round37/git-webserver-probe.txt | sort -u` yields
`verify.sh:49 57 57-59 57,60 59 60 62 63 73-80 75-76 79`, `test_outputs.py:13`, `instruction.md:1-6 7 9`.
Every one lands on the construct the receipt describes in the reopened bytes (e.g. `:59` is
`if [ "$HTTP_RESPONSE" = "200" ]`, `:79` is `echo "Content: $CONTENT"`, `:73-80` is the wget branch plus its
content compare). No anchor is off by a line.

Adjacent facts the entry may want (all read off the reopened bytes, none contradicting the receipt):
- `verify.sh:4-6`: the comment says "Install curl for testing" but the install line adds only `expect`; curl
  comes from the image — consistent with §4 item 3 and with the probe running `apt-get`/`expect`-less.
- `tests/test.sh:4,14-18`: the harness path installs uv over the network and runs pytest 8.4.1 via `uvx` on
  `/tests/test_outputs.py`, writing `/logs/verifier/reward.txt` (1/0 at :21-25); `task.toml:21-25` gives 900 s to
  verifier and agent. The probe bypasses `test.sh` and calls `test_outputs.py` directly — so the probe measures
  the assertion, not the uv/pytest transport.
- `instruction.md:2` says `git clone user@server:/git/server` while `verify.sh:21` clones
  `git@localhost:/git/server`; `instruction.md:10` excuses the login setup. The instruction never says "nginx"
  or "hook" (the README does), so the requirement map's label for `instruction.md:1-6` should stay about a
  reachable git repository and a push, not about a hook.

## 7. Axes and limits

- Coverage (axis): 6/6 reopened from the network, 9/9 files in the task directory accounted for (the 3 extras
  now characterised), 10/10 anchors quoted. No upstream file relevant to the grader verdict is unaccounted.
- Freshness (axis): commit metadata and tree read at the pin today; `main` re-read today via `ls-remote`
  (no local staleness); captures proven to be the pin's own blobs, so the C2 anchors cannot have drifted.
- Limit 1: the GitHub REST commit endpoint was rate-limited (403, 60/60 used, reset 2026-10-26T05:07:14Z) and no
  token is available to this seat; commit metadata came from the git object store (self-hash verified) and
  GitHub's `.patch` endpoint instead. Functionally equal, different transport — recorded, not hidden.
- Limit 2: the drift check is trivially satisfied because `main` == pin; a future upstream change after today
  would not be detected by this seat's evidence.
- Limit 3: the published image `alexgshaw/configure-git-webserver:20251031` was not pulled or inspected (docker
  not exercised by this seat), so "curl preinstalled at grading" rests on `environment/Dockerfile:5` +
  `README.md` ("Pre-installed tools: curl") + `verify.sh:4` assuming curl, not on the image contents.
- No lane file was written outside this report directory; no lane git index operation; scratch removed.

## 8. Verdict

`reopen-<n_identical>/6`: 6 of 6 bytes identical, plus sha256 manifest clean (6 OK, exit 0) and 6/6 blob-id
match to the tree at `2fd12b88`. `drift-<yes|no>`: **no** — `main` is at the pin and all six files are
byte-equal across them.

VERDICT: reopen-6/6-drift-no
