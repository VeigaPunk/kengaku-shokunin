# ScoutHostR81 — round-81 w1 per-surface reconnaissance (read-only)

Seat: `ScoutHostR81` (scout, leaf). Date: 2026-11-04. Scratch: `/fast/scratch/hyaku/kengaku-r81/ScoutHostR81`.
Measured tree: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at tip
`ca9bfe791422597e4d5ce0ab032c9eed7eac40c8` (`git rev-parse master` and `git rev-parse HEAD` agree;
`git rev-parse --abbrev-ref HEAD` prints `HEAD`, i.e. detached at the `master` tip).
Freeze commit `4d896e0daf8831ef7a0016bf3c944d11ba465f70` is an ancestor of the tip
(`git merge-base --is-ancestor … && echo yes` → `freeze-reachable=yes`).
Host: `python3 -V` → `Python 3.14.8`; `openssl version` → `OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)`.

Scope discipline: this seat ran no write outside its scratch and this report; no git/jj mutation
anywhere; no counter re-run (the counters are other seats' instruments and are not trusted here).

---

## 1. Declared surfaces — exact command and result

All commands were run from `/fast/scratch/hyaku/kengaku-r81/ScoutHostR81`.

```
for p in ~/Projects/webzites/repos/llm-wiki ~/archive/bench-arena \
         ~/Projects/bounties/ledger/telemetry.jsonl ~/Projects/ufo-fsd-alpha \
         ~/Projects/shokuknow; do
  if test -e "$p"; then echo "PRESENT $p"; else echo "ABSENT $p"; fi
done
```

```
ABSENT /home/vgpnk/Projects/webzites/repos/llm-wiki
ABSENT /home/vgpnk/archive/bench-arena
ABSENT /home/vgpnk/Projects/bounties/ledger/telemetry.jsonl
PRESENT /home/vgpnk/Projects/ufo-fsd-alpha
PRESENT /home/vgpnk/Projects/shokuknow
```

```
curl -s -m5 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:34113/health   # → 000, rc=7
curl -s -m5 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:1234/health    # → 200, rc=0
ss -ltn 'sport = :1234'                                                      # → LISTEN 127.0.0.1:1234
ss -ltn 'sport = :34113'                                                     # → header only, no row
```

| Surface | Probe | Result | PROVINCE canonical map | Moved? |
|---|---|---|---|---|
| `~/Projects/webzites/repos/llm-wiki` | `test -e` | **absent** | `absent **ABSENT 2026-11-04**` (map line 1023) | no |
| `~/archive/bench-arena` | `test -e` | **absent** | `absent **ABSENT 2026-11-04**` (map line 1025) | no |
| `~/Projects/bounties/ledger/telemetry.jsonl` | `test -e` | **absent** | `absent **ABSENT 2026-11-04**` (map line 1030) | no |
| `http://127.0.0.1:34113/health` | `curl` | **absent** (`000`, rc 7, 0.000098 s) | `absent **ABSENT 2026-11-04**` (map line 1027) | no |
| `http://127.0.0.1:1234/health` | `curl` | **present**, body `{"status":"ok"}` | `present — llama.cpp router, lfm3-server.service` (map line 1029) | no |
| `127.0.0.1:1234` | `ss -ltn` | **LISTEN** | same row | no |
| `~/Projects/ufo-fsd-alpha` | `test -e` | **present** (git branch `main`, `.git` present, mtime 2026-10-27 17:10) | **not a canonical map row**; prose only, PROVINCE:114 (round 75) says "present" | no (still present) |
| `~/Projects/shokuknow` | `test -e` | **present** (git branch `master`, `.git` present, mtime 2026-10-27 14:35) | **no occurrence in PROVINCE.md at all** (`grep -n 'shokuknow' PROVINCE.md` → 0 lines) | n/a — never carried |

Extra, same sweep: `ss -ltn '( sport = :34113 or sport = :45669 or sport = :8791 )'` →
one row only, `LISTEN 0 512 127.0.0.1:8791`. So `:34113` and `:45669` have no listener and `:8791`
(the ds-flash-shim row, map line "Live probe endpoint") is listening.

**Nothing moved against the canonical map.** Two surfaces exist that the map does not carry as rows
(§4).

## 2. Source census and frozen row count

Census, exact contract spelling:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin kengaku
```

stdout (27 lines, verbatim; tab-separated `lane<TAB>code<TAB>value`):

```
kengaku	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
kengaku	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
kengaku	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
kengaku	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
kengaku	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
kengaku	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
kengaku	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
kengaku	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
kengaku	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
kengaku	W04	S213 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/tests/test_outputs.py across scopes
kengaku	W04	S214 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/test_outputs.py across scopes
kengaku	W04	S215 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/verify.sh across scopes
kengaku	W04	S216 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/instruction.md across scopes
kengaku	W04	S217 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/environment/task-deps/gen.py across scopes
kengaku	W04	S222 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/openssl-selfsigned-cert/instruction.md across scopes
kengaku	W04	S227 duplicate url encoding.spec.whatwg.org/index-windows-1252.txt across scopes
kengaku	W04	S234 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py across scopes
kengaku	W04	S237 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py across scopes
kengaku	W04	S243 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test_outputs.py across scopes
kengaku	W04	S256 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```

stderr: **empty**. Exit code: **0**.

Reading of the verdict (from the script's own header, `scripts/sources-census.sh:30-33`):
`exit: 0 clean or warnings`; `W04 same URL across scopes (warnings do not affect clean lanes)`.
So `kengaku ok` + rc 0 with 27 `W04` warnings is a **clean lane with warnings**, not a failure —
there is no `E..` code in the output.

Frozen row count, exact command:

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```
→ **250** (`grep` rc 0).

Both numbers, with their derived revisions (the R80-U3 values independently re-derived here):

| Source | Command | Value |
|---|---|---|
| measured tree / HEAD | `grep -cE … corpus/SOURCES.md` | **250** |
| `git show HEAD:corpus/SOURCES.md \| grep -cE …` | same pattern | 250 |
| `git show 507d249b:corpus/SOURCES.md \| grep -cE …` | same pattern | 250 |
| `git show dce7c275:corpus/SOURCES.md \| grep -cE …` | same pattern | 249 |
| PROVINCE canonical map, "Public-literature registry" | declared cell | **249** (`rows=249`) |

Census `census` mode (not part of the contract ask; run to reconcile the declared count):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kengaku
```
→ `kengaku rows 250`, `FLEET rows 250`, `FLEET.tier.invalid 0`, `FLEET.status.invalid 0`,
`FLEET missing 0`, rc 0. Tier split: A=220, B=24, C=6. Status split: mined=228, queued=8, rejected=14.

**Discrepancy to record:** the canonical map says `rows=249`; the measured tree is 250 (250 at
`507d249b` too). `S258` ("kengaku round-80 located replays") is present exactly once
(`grep -cE '^\|[[:space:]]*S258[[:space:]]*\|' corpus/SOURCES.md` → 1), appended after the map cell
was written. The map cell's parenthetical ("247 superseded … by round 79's S256/S257 appends",
247+2=249) is therefore one round behind: 248+2 = 250. Stale-by-one, not a census failure.

## 3. Pinned Terminal-Bench fetches (access 2026-11-04T08:26:13Z, `curl -sS -m 20`)

Base: `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6`

| Path at the pinned tree | HTTP | Bytes | sha256 |
|---|---|---|---|
| `README.md` | **200** | 4574 | `7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364` |
| `tasks/log-summary-date-ranges/task.yaml` | **404** | 14 | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` |
| `tasks/vulnerable-secret/task.yaml` | **404** | 14 | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` |

The two `task.yaml` fetches are **failed fetches** and their 14-byte bodies are the literal string
`404: Not Found` (identical sha256 for both, i.e. no content).

Why they 404 — resolved against the tree itself, not guessed. Recursive listing of the pinned tree:

```
curl -sS -m30 -o tree-r.json -w '%{http_code}' \
  'https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1'
```
→ HTTP 200, 453523 bytes, `truncated: false`, 1446 entries.

- `task.yaml` files in the whole pinned tree: **0**. Task metadata is `task.toml` in this tree.
- Members are **top-level** directories, not under `tasks/`: each has 12 entries, namely
  `.gitignore`, `README.md`, `environment/Dockerfile`, `environment/log_generator_deterministic.py`
  (log task) / `environment/vulnerable.c` (secret task), `instruction.md`, `solution/solve.sh`,
  `task.toml`, `tests/test.sh`, `tests/test_outputs.py`.

So the requested spine `tasks/<member>/task.yaml` is wrong twice (`tasks/` prefix absent, `.toml`
not `.yaml`). Corrected fetches, same base and access time:

| Path at the pinned tree | HTTP | Bytes | sha256 |
|---|---|---|---|
| `log-summary-date-ranges/task.toml` | **200** | 988 | `9a9593673d6805ef3a301ea734e9c4dbaf80da1b37c0fe9d1f2ceea2a8c57e18` |
| `vulnerable-secret/task.toml` | **200** | 925 | `51079626e4c76445e616eff8723efc53af7f1cf8d9c64d15aab2f4f0ecd6df3c` |
| `log-summary-date-ranges/instruction.md` | **200** | 1391 | `c1d4516ad4ec2238209740eaf01291df9ab48b0028a3fc5df383c6f831453484` |
| `vulnerable-secret/instruction.md` | **200** | 432 | `d43c72e6c39cdeb1141a9c8eae8357df1b0901383ee2beedacf828bf017d7a2f` |
| `log-summary-date-ranges/tests/test_outputs.py` | **200** | 1655 | `2fc06a6ce1944ad82f84fb437395fa75ed8c0eadd385b92e375c27e5bc9cb2b4` |
| `vulnerable-secret/tests/test_outputs.py` | **200** | 1346 | `f2b65f63ac81acd1e80e1ad4c59c1022131a0f9eb20f8ab3212c4ef8d8f0c753` |

### Located quotes (premise the offline replay stages)

- `README.md:24` (13 words): "Tasks include assembling proteins for synthesis, debugging async code,
  and resolving security vulnerabilities." — benchmark-level only; the README names no per-task
  artifact.
- `log-summary-date-ranges/instruction.md:9` (14 words): "Write a CSV file /app/summary.csv with the
  following structure (including the header):"
- `log-summary-date-ranges/instruction.md:28`: "The current date is 2025-08-12. Use this as the
  reference date for all calculations." — the replay's determinism premise: the reference date is
  pinned, so the offline replay need not consult a clock.
- `log-summary-date-ranges/task.toml:6`: "Evaluates the ability to analyze date-stamped log files,
  calculate counts across multiple date ranges, and generate structured CSV output."
- `vulnerable-secret/instruction.md:1` (17 words): "The goal is to extract this secret key and save
  it to `/app/results.txt`."
- `vulnerable-secret/task.toml:6`: "Evaluates the agent's ability to analyze a binary executable,
  identify and exploit a buffer overflow vulnerability to bypass authentication, and extract a
  hidden secret flag."

### Cross-check worth carrying into R81-C1

The remote grader bytes at the pinned tree are **byte-identical** to the committed round-52 capture
at the measured tree (`git show HEAD:<path> | sha256sum` vs the curl sha256):

| member | remote sha256 | committed `corpus/evidence/round52/graders/<m>/tests/test_outputs.py` | bytes | `^\s*assert\b` count |
|---|---|---|---|---|
| `log-summary-date-ranges` | `2fc06a6c…c2b4` | `2fc06a6c…c2b4` (**equal**) | 1655 | 5 |
| `vulnerable-secret` | `f2b65f63…c753` | `f2b65f63…c753` (**equal**) | 1346 | 5 |

Both carry 5 asserts — the frozen selection rule's maximum (11 candidates, max 5). This confirms the
round-52 capture is the pinned-tree grader and that the two members are the max-assert pair, without
trusting the counter.

Both `task.toml` files set `allow_internet = true` and pin `docker_image = alexgshaw/<member>:20251031`;
neither is needed by an offline replay, but a replay that stages network access would not be
reproducing the declared environment.

## 4. Disk state and PROVINCE.md changes to record

```
/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status   # rc 0
```

```
root                             use%     free
/tmp                              27%    93.6G
/var/tmp                          24%   711.0G
/fast/scratch/hyaku               55%   362.2G
```

Top consumers (reported, not acted on — no seat owns cleanup of another round's scratch):
`/tmp/polish61-m47tumble-cache` 27.7G (idle 1355 s), `/tmp/.mount_alma.AFFvYd1` 1.5G,
`/tmp/r80-tip` 698.7M, `/tmp/r80-decl` 688.0M, `/tmp/r80-base` 687.3M;
`/fast/scratch/hyaku/kaidoku-r53` 10.3G, `kake-r75` 10.2G, `kengaku-r80` 9.9G.
`/fast/scratch/hyaku/kengaku-r81` is 1.3G during this round. Guard reports no pressure; rc 0.

**Lane worktree state** (observation for the C1 seats, whose receipts require `WORKTREE clean`):
`git status --porcelain` prints 5 untracked lines, 0 modified:
`.ufo/waves/round-81/w1.ready`, `.ufo/waves/round-81/w1.ready.dispatched`,
`.ufo/waves/round-81/w1/w1-run.err`, `corpus/evidence/round81/census-rows.txt`,
`corpus/evidence/round81/r80-u4-red-before.txt` (the last two are R81-C2 repairs in flight).
A receipt minted now would report a non-clean worktree.

### Proposed PROVINCE.md records (L1 to integrate; this seat did not edit it)

1. **Stale count — must be corrected.** Canonical map row "Public-literature registry" declares
   `rows=249`; measured 250 at tip `ca9bfe79` and at `507d249b` (command in §2). Cause: `S258`
   (round-80 replays) appended after the cell was written. Correction: `rows=250`, and the
   parenthetical should read 248 superseded by round-79's S256/S257 appends (248+2=250).
2. **`~/Projects/ufo-fsd-alpha` — present, unrowed.** Exists only as prose (PROVINCE:114, round 75)
   and in the round-14 scope note (PROVINCE:57). It is present today (git `main`, `.git`, mtime
   2026-10-27). If the map is meant to catalogue every tree the lane reads from, it needs a `path`
   row; absent that intent, the prose is still accurate and nothing is owed.
3. **`~/Projects/shokuknow` — present, entirely unreferenced.** `grep -n 'shokuknow' PROVINCE.md`
   returns zero lines, yet the tree exists (git `master`, `.git`, mtime 2026-10-27, top-level
   `MANIFEST.json`, `doctrine/`, `lanes/`, `merge/`, `tabi-shokunin/`). This is a surface the map
   does not carry at all — a new row (or an explicit "not a surface" note) is the honest fix.
4. **No regression to record.** The four previously-absent surfaces (`llm-wiki`, `bench-arena`,
   `telemetry.jsonl`, `:34113`) are still absent and their `ABSENT 2026-11-04` cells are accurate;
   `:1234` and `:8791` are still listening and their `present` cells are accurate. Today's sweep
   adds no new absence and no relocation.

## 5. What I could not establish

- **`task.yaml` does not exist at the pinned tree** (0 of 1446 entries), so no quote can be located
  in it. The premise quotes above come from `instruction.md` and `task.toml` instead. Anyone
  scripting a `task.yaml` fetch for these members will get a 404, not a parse error.
- **PROVINCE.md intent is not derivable from bytes.** Whether `ufo-fsd-alpha`/`shokuknow` *belong*
  in the canonical map (versus the prose/scope note) is an L1/operator decision; I report presence
  and the exact absence of rows, not a verdict.
- **No remote fetch of the two `README.md` per-task files** was requested and none was made; only the
  paths in §3 were fetched.

Confidence: surface, socket, census, row-count and fetch results are **high** (direct command output,
pasted above). The "wrong spine" reading of the 404s is **high** (resolved by the pinned tree's own
recursive listing, `truncated: false`). The byte-identity of the remote grader to the committed
capture is **high** (independent sha256 on both sides). Nothing here is inferred from a counter.
