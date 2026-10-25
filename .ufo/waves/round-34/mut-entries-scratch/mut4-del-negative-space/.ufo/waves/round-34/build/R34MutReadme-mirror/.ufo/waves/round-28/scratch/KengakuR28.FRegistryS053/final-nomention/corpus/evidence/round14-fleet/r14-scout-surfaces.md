# r14 live-surface re-verification (ScoutSurfaces, 2026-09-29)

Scope: re-run every live host surface this lane cites — the served-model endpoint,
the `llama-server` process pin, `~/Projects/bounties/` route telemetry,
`~/bench-arena/`, `~/Projects/webzites/repos/llm-wiki`, the `~/.bailian/` state
files, and the on-disk gguf. Every row below was produced by a command run in the
**audit window 2026-09-29T03:26:19Z – 2026-09-29T03:29:40Z**; nothing is quoted
from memory, and no number is copied from a prior artifact. Host: `plazir27`, kernel
linux 7.1.8-arch1-3, repo root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(local TZ `-03:00`; all artifact rows are UTC).

**Headline: one live surface is FALSIFIED as cited.** `~/bench-arena/` — recorded
`NO-DRIFT` by round 12 and re-affirmed by the round-11 PROVINCE row — **no longer
exists at its cited path: the whole tree was relocated to `~/archive/bench-arena`**
(pinned below, tree content byte-frozen and every cited member now md5-pinned).
Everything else re-verifies: endpoint identity `MATCH`, process pin `EXACT_MATCH`
(41/41 tokens *and* md5-identical to the r12 committed capture),
`~/Projects/bounties/` `ABSENT` (corroborated, no resurrection),
llm-wiki `MATCH`, bailian state files `MATCH`.

---

## 1. Verdict table (acceptance shape: command · observed · verdict · timestamp)

| # | Surface | Command | Observed | Verdict | Timestamp (UTC) |
|---|---|---|---|---|---|
| S1 | `/v1/models` served id | `curl -s -m5 http://127.0.0.1:34113/v1/models \| python3 -c '…data[0]["id"]'` | `/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf` | **MATCH** | 2026-09-29T03:29:19Z |
| S2 | `/health` | `curl -s -m5 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health` | `200` (body `{"status":"ok"}`) | **MATCH** | 2026-09-29T03:29:19Z |
| S3 | Process pin | `md5sum /proc/1299/cmdline; wc -c < /proc/1299/cmdline` | `e6642361e60173c15705a8108e547efa`, `632` bytes | **MATCH** (== r12 committed pin) | 2026-09-29T03:29:19Z |
| S4 | Sole listener | `ss -ltnp \| grep 34113` | `LISTEN … 127.0.0.1:34113 … users:(("llama-server",pid=1299,fd=16))` | **MATCH** (pid 1299 as expected) | 2026-09-29T03:29:19Z |
| S5 | Competing clients | `ss -tan 'sport = :34113' \| grep -c ESTAB` | `0` | **MATCH** (no other client) | 2026-09-29T03:29:19Z |
| S6 | Route telemetry tree | `test -e /home/vgpnk/Projects/bounties` | `ABSENT` | **ABSENT** (confirmed) | 2026-09-29T03:29:19Z |
| S7 | Route telemetry sweep | `find /home/vgpnk/Projects -maxdepth 2 -name 'bounties*'` | `0` hits | **ABSENT** (no relocation) | 2026-09-29T03:29:19Z |
| S8 | Ledger search | `find /home/vgpnk -xdev -maxdepth 6 -name telemetry.jsonl -path '*ledger*'` | `0` hits; `0` dirs named `ledger` | **ABSENT** | 2026-09-29T03:29:20Z |
| S9 | Bench tree at cited path | `test -d ~/bench-arena` | `ABSENT` | **DRIFT** | 2026-09-29T03:29:20Z |
| S10 | Bench freeze at cited path | `find ~/bench-arena -newermt '2026-09-28 18:00' -type f \| wc -l` | `0` files **+ stderr** `find: '/home/vgpnk/bench-arena': No such file or directory` | **DRIFT** (path error, not a frozen tree) | 2026-09-29T03:29:20Z |
| S11 | Bench tree, relocated | `find ~/archive/bench-arena -newermt '2026-09-28 18:00' -type f \| wc -l`; `stat -c %y` | `0` files; dir mtime `2026-08-29 03:58:10.451962237 -0300` | **MATCH-content / DRIFT-path** | 2026-09-29T03:29:20Z |
| S12 | llm-wiki resolves | `git -C ~/Projects/webzites/repos/llm-wiki log -1 --format='%h %cI %s'` | `e66e614 2026-08-08T21:40:55-03:00 Add product ship evidence…` | **MATCH** | 2026-09-29T03:29:20Z |
| S13 | llm-wiki churn | `find ~/Projects/webzites/repos/llm-wiki -newermt '2026-09-28' -type f -not -path '*/.git/*'` | `0` hits | **MATCH** (no eval-relevant churn) | 2026-09-29T03:29:20Z |
| S14 | Bailian telemetry | `stat -c '%s %y' ~/.bailian/telemetry.jsonl; wc -l` | `1119225` B, mtime `2026-09-16 18:52:37.721248773 -0300`, `4274` lines | **MATCH** (present; stale by design) | 2026-09-29T03:29:20Z |
| S15 | Bailian sync state | `stat -c '%s %y' ~/.bailian/wiki-sync-state.json` | `117` B, mtime `2026-09-11 10:58:29.062481971 -0300` | **MATCH** | 2026-09-29T03:29:20Z |
| S16 | On-disk gguf | `stat -c '%s %y' /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf` | `10333691040` B, mtime `2026-08-29 02:39:38.068184831 -0300` | **MATCH** (r12 §3 holds) | 2026-09-29T03:29:20Z |
| S17 | Endpoint idleness | `journalctl --user -u qwen-coder.service --since @1790640000 -o short-iso \| grep 'slot .*release' \| tail -1` | last inference `2026-09-28T22:58:03-03:00` (= `01:58:03Z`) | **MATCH-now**, see §9 caveat | 2026-09-29T03:29:20Z |

---

## 2. Endpoint identity — `MATCH`

Command (S1, re-run 2026-09-29T03:29:19Z) and the byte-exact body it returned
(872 B, `md5 b876b1c292e5882c7c680683cacee6cc`,
`sha256 444d248e2d2cafaa682a90aac65609d647cc2549c0e60e0020d2497dce4d3869`,
`created=1790652579`):

```json
{"models":[{"name":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf","model":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf","modified_at":"","size":"","digest":"","type":"model","description":"","tags":[""],"capabilities":["completion"],"parameters":"","details":{"parent_model":"","format":"gguf","family":"","families":[""],"parameter_size":"","quantization_level":""}}],"object":"list","data":[{"id":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf","aliases":["/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf"],"tags":[],"object":"model","created":1790652579,"owned_by":"llamacpp","meta":{"vocab_type":true,"n_vocab":151936,"n_ctx":16384,"n_ctx_train":262144,"n_embd":2048,"n_params":30532122624,"size":10327717888,"ftype":"IQ2_XXS - 2.0625 bpw"}}]}
```

- **V1.** `data[0].id` == the committed string
  `/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`
  **byte-for-byte** (Python `==` on the decoded string → `True`), and
  `sha256(id) = e9c3d81ffee6e6d5833bd725f4f214ee8a3b905d8abcd645ab75711b6e1101eb`.
  The same string is `data[0].id` in `corpus/evidence/round10-fleet/models-34113.json`
  (md5 `66a610dbc260dcc67e6c3ea38ef9f632`) and in the committed `descriptors` cells of
  both `corpus/evidence/round11-power/results-r11.jsonl` (md5 `c42fe3d10b6d7a1ed14c4485af03357b`)
  and `corpus/evidence/round12-ladder/results-r12.jsonl` (md5 `9dd8aa2b6a7aa7890aa802c37d5af0f9`).
  → **MATCH**, no drift, three-way (live = r10 = r11 = r12).
- **V2. Full-body equality.** Live body is 872 B, exactly the committed r10 body's
  length. Raw bytes differ; **normalized bytes are identical**:
  `re.sub(rb'"created":\d+', b'"created":<CREATED>', …)` → `identical: True`, and the
  only differing byte offsets are `676–680` (5 bytes, all inside the 10-digit
  `created` value). So the *entire* delta between a fresh capture and every stored
  capture is the `created` integer.
- **V3. `created` semantics — upgraded from inference to fact.** Two successive
  requests, each compared against `date +%s`:

  | request | wall clock (epoch) | `created` |
  |---|---|---|
  | 1 | `1790652445` | `1790652445` |
  | 2 | `1790652447` | `1790652447` |

  and, from committed bytes: r11 `created=1790638137` ↔ `request_ts=2026-09-28T23:28:57Z`
  (= epoch `1790638137`) — exact to the second; r12 `created=1790644799` ↔
  `request_ts=2026-09-29T01:19:59Z` (= `1790644799`) — exact. `corpus/evidence/round12-fleet/r12-endpoint-freshness.md`
  §1.3 carried this as `[INFERENCE-moderate] on the mechanism ("server stamps now")`;
  it is now **[certain]**: `created` is stamped at request time, so `/v1/models` is
  byte-reproducible across captures **iff `created` is masked**. Recommended mask for
  any future re-pin: `"created":<CREATED>`.
- **V4.** Auxiliary surfaces agree: `/props` → `model_path` = `model_alias` = the same
  string, `build_info=b1-d7bd3bf`, `model_ftype="IQ2_XXS - 2.0625 bpw"`, `n_ctx=16384`,
  `total_slots=2`; `/slots` → 2 slot objects, both `n_ctx=16384`, both
  `is_processing=false`; `/health` → `200`, body `{"status":"ok"}`; `/v1/models` → `200`.

## 3. Process pin — `EXACT_MATCH` (strongest available level)

- **V5.** Listener: `ss -ltnp | grep 34113` → a single row,
  `LISTEN 0 512 127.0.0.1:34113 0.0.0.0:* users:(("llama-server",pid=1299,fd=16))`.
  **pid 1299** — equal to the expected value in the brief, and to the pid in
  `corpus/evidence/round12-fleet/r12-endpoint-freshness.md` (md5 `d5cdeea7677eb814b83d3d913420ba95`,
  sha256 `343429d45c48860d079016a7fc6d02cdfb74ce2bdc45367800ad95a0ead655b5`).
- **V6.** Token compare vs the unit. Parsing
  `~/.config/systemd/user/qwen-coder.service` `ExecStart` (line continuations joined)
  gives **41 tokens**; `/proc/1299/cmdline` (NUL-split) gives **41 tokens**;
  `unit == proc` → **`EXACT_MATCH`, zero deltas** (no `difflib` output emitted).
- **V7.** Byte pin: `md5sum /proc/1299/cmdline` →
  `e6642361e60173c15705a8108e547efa`, `632` bytes. This is **identical** to the raw
  cmdline md5 committed by round 12 (`r12-endpoint-freshness.md` §2.1), and the live
  argv is token-identical to the committed `server.argv` in **both** r11 and r12
  `descriptors` records (checked programmatically: `argv == live` → `True`, 41 tokens,
  pid 1299 in both). Triple agreement: **live process == r12 committed capture == systemd unit**.
- **V8.** Required flags, all `PRESENT` in the 41-token argv:

  | Flag | Present | Corroboration beyond argv |
  |---|---|---|
  | `--cache-type-k q4_0` / `--cache-type-v q4_0` | yes / yes | argv only (llama.cpp exposes no runtime KV-type getter; `/metrics` shows `llamacpp:requests_processing 0`, `requests_deferred 0`) |
  | `--kv-unified` | yes | argv only |
  | `--parallel 2` (no literal `-np`) | yes | `/props total_slots=2`; `/slots` → 2 objects |
  | `--no-context-shift` | yes | argv only |
  | `--chat-template-file …/qwen-coder-godspeed.jinja` | yes | `/props chat_template` renders a custom non-upstream template (`{# Copyright 2025-present Unsloth …`) — consistent with the file, not with the model's built-in template |

  Also present: `--ctx-size 16384`, `--cont-batching`, `--flash-attn on`, `--fit off`,
  `--n-gpu-layers 999`, `--no-webui`, `--no-agent`, `--jinja`, `--alias <same gguf>`,
  `--model <same gguf>`, `--host 127.0.0.1`, `--port 34113`, `--metrics`, `--slots`,
  `--timeout 900`, `--split-mode none`.
- **V9.** Same process as r11/r12: `/proc/1299` mtime = start = `2026-09-28 02:55:28.657887574 -0300`
  (= `05:55:28Z`), i.e. up through every stored r11/r12 request; `readlink /proc/1299/exe`
  → `/home/vgpnk/.local/bin/llama-server`. A fresh capture therefore reproduces the r11/r12
  *unit*, not a restarted near-neighbour.
- **V10.** Config-file pins (new, for future drift detection):
  `~/.config/systemd/user/qwen-coder.service` md5 `1920195761aa624a2e9b8b4e0782cc2a`;
  `~/.config/llama/qwen-coder-godspeed.jinja` md5 `14666868f011f84fa3560a950b6c64f0`.

## 4. Route telemetry `~/Projects/bounties/` — `ABSENT` (confirmed, no resurrection)

- **V11.** `test -e /home/vgpnk/Projects/bounties` → `ABSENT` (S6).
- **V12.** `find /home/vgpnk/Projects -maxdepth 2 -name 'bounties*'` → **0 hits** (S7).
  `ls -A /home/vgpnk/Projects | wc -l` → 36 entries, `grep -c bounties` → 0
  (nearest neighbours are `the-bounty-hunter` and `origin-work/`).
- **V13.** No relocation, and specifically **not into the new archive dir**:
  `find /home/vgpnk/archive -maxdepth 3 -iname '*bount*'` → 0 hits;
  `find /home/vgpnk -xdev -maxdepth 6 -name telemetry.jsonl -path '*ledger*'` → **0 hits**;
  `find /home/vgpnk -xdev -maxdepth 6 -type d -name ledger` → **0 dirs** (S8).
  No `~/.local/share/Trash` directory exists.
- **V14.** Remaining traces are stale and are **not** the tree:
  `~/.grok/memory/bounties-17da6cb9/` (mtime `2026-09-05 14:14`, `MEMORY.md` content is a
  2-line stub: `# Project Memory — /home/vgpnk/Projects/bounties` + an auto-populated
  note) and `~/.grok/sessions/%2Fhome%2Fvgpnk%2FProjects%2Fbounties/` (mtime `2026-09-05 14:14`).
  `~/Projects/the-bounty-hunter/` (mtime `2026-09-05 09:03`) carries no `ledger/telemetry.jsonl`;
  `~/Projects/origin-work/open-bug-bounties/` (git HEAD `1307b8b6f8361cfa338de9bee903f4810020f320`,
  `2026-09-14T13:33:56-03:00`) has **no `ledger/`** directory and is a distinct Next.js
  codebase. Neither is the `bounties` project tree.
- **V15.** Timestamp bound (new, and *weaker* than the sibling report — recorded so it is
  not over-claimed): the only structural stamp available is the parent directory mtime.
  `stat -c %y /home/vgpnk/Projects` → `2026-09-29 00:13:18 -0300` (= **`03:13:18Z`**), which
  bounds the *last child-level change* in `~/Projects`, not the deletion instant itself
  (a later sibling create/rename bumps the same mtime; `~/Projects/magga` also carries
  `00:13`). The task brief (and the round-11/12 record) put the disappearance at
  `~23:51Z 2026-09-28`; nothing in this audit contradicts that, and nothing here can pin it
  more precisely. `~/.bash_history` (mtime `2026-09-28 20:04`) contains `cd bounties`
  (lines 377/390/450/527) followed later by `cd open-bug-bounties` (534/539/545/555), but
  **no `mv`/`rm` line** — `[INFERENCE]` operator-side lineage only, not evidence of deletion.
- **V16.** `PROVINCE.md` already marks this row ABSENT (round 11). **Still absent — no
  resurrection, no relocation.** Round-11/12 census counts (`7,226` / `7,218` lines) remain
  historical and must stay labelled so.

## 5. `~/bench-arena/` — **DRIFT: relocated to `~/archive/bench-arena`**

This is the round's falsification. The brief's premise for item 4 ("expect 0 = frozen;
spot-check `tasks/` dir and `grade.sh` exist") does not hold at the cited path:

- **V17.** `test -d ~/bench-arena` → `ABSENT` (S9). The prescribed `find` therefore does
  **not** report "0 = frozen" as a fact; it reports an **error** and a vacuous 0:
  ```
  $ find ~/bench-arena -newermt '2026-09-28 18:00' -type f | wc -l
  0
  $ # stderr: find: '/home/vgpnk/bench-arena': No such file or directory
  ```
  At the cited path `tasks/` and `grade.sh` **do not exist**:
  `ls: cannot access '/home/vgpnk/bench-arena/tasks': No such file or directory`, same for `grade.sh`.
- **V18. Identification.** `find /home/vgpnk -maxdepth 4 -name 'bench-arena*'` →
  exactly one hit: **`/home/vgpnk/archive/bench-arena`**. Its `ls -la` is *token-identical*
  to the verbatim `ls -la ~/bench-arena` body committed in `r12-endpoint-freshness.md` §5.1
  (`total 76`; the same 11 entries with the same sizes and mtimes:
  `generate_new_domains.py 43187`, `grade.sh 1199` (mode `x`), `graded/`, `loop.sh 4379`,
  `out/`, `report-grok45.csv 1017`, `report-qwenlocal-v2.v2.csv 3388`,
  `report-qwenlocal.csv 1017`, `staging/`, `tasks/`, `telemetry-qwenlocal-v2.csv 4501`).
  The **only** difference from r12's verbatim block is the `..` line — r12 recorded
  `.. = drwx------ … 4590 Sep 27 20:07` (home); now it is
  `.. = drwxr-xr-x … 666 Sep 29 00:13` (`~/archive`). That is exactly the signature of a
  relocation into a new parent.
  Also, `~/archive/bench-arena/tasks` holds **33 task dirs with 33 `test.sh`** — the same
  count the r3/r4/r5 knowledge entries use (21/33, 20/33, 19/33 …).
- **V19. Still frozen.** `find ~/archive/bench-arena -newermt '2026-09-28 18:00' -type f | wc -l`
  → **0**; newest file remains `telemetry-qwenlocal-v2.csv` at `2026-08-29 03:30:59 -0300`.
  So the *content* claim ("frozen since 2026-08-29 03:30:59", r12 `NO-DRIFT`) is **true**;
  only the *path* claim broke. Verdict split: **content MATCH / path DRIFT**.
- **V20. Every cited member resolves under the archive root** (old path → all MISSING,
  new path → all EXISTS):

  | Cited member | `~/bench-arena/…` | `~/archive/bench-arena/…` |
  |---|---|---|
  | `grade.sh`, `loop.sh` | MISSING | EXISTS |
  | `tasks/` (33 dirs, 33 `test.sh`) | MISSING | EXISTS |
  | `tasks/27-rwlock-writer-pref/test.sh` | MISSING | EXISTS |
  | `telemetry-qwenlocal-v2.csv` | MISSING | EXISTS |
  | `report-qwenlocal-v2.v2.csv`, `report-qwenlocal.csv`, `report-grok45.csv` | MISSING | EXISTS |
  | `generate_new_domains.py`, `graded/`, `out/`, `staging/` | MISSING | EXISTS |

  → the transformation is a clean **prefix relocation** `~/bench-arena/ → ~/archive/bench-arena/`.
- **V21. New durable md5 pins** (of the archived tree):

  | File | md5 |
  |---|---|
  | `~/archive/bench-arena/grade.sh` | `a15b02f52d4459d0d198bf70b333d357` |
  | `~/archive/bench-arena/loop.sh` | `44427e241574ba23a712faae661484f3` |
  | `~/archive/bench-arena/telemetry-qwenlocal-v2.csv` | `dac11874502f7f3f05fb725035294d4e` |
  | `~/archive/bench-arena/report-qwenlocal-v2.v2.csv` | `c3bd7efe22630dcc6c47e8fa26f66235` |
  | `~/archive/bench-arena/report-qwenlocal.csv` | `57aab8982dcfc18c9d4b29b61acc380e` |
  | `~/archive/bench-arena/report-grok45.csv` | `e0a42a2f1ab649f4430ebc5b2e380959` |

  `grade.sh` remains executable and its interface matches the knowledge entries
  (`LABEL=${1:?label}; ROOT=${BENCH_ROOT:-.}`), and `loop.sh` still emits the 12-field header
  the `telemetry_source=journal` erratum is about (`…,telemetry_source,telemetry_available`).
- **V22. Relocation time bound.** The child dir mtime is *preserved* at
  `2026-08-29 03:58:10 -0300` (unchanged from r12) — `mv` on one filesystem preserves
  mtimes `[INFERENCE-strong]`, whereas a fresh copy would not. Only parents are stamped:
  `stat -c %y /home/vgpnk/archive` → `2026-09-29 00:13:38.313672884 -0300`
  (= **`03:13:38Z`**); `/home/vgpnk` → `00:14:07` (= `03:14:07Z`). So the move happened at
  or just before **2026-09-29T03:13:38Z** — i.e. *after* round 12's `NO-DRIFT` audit and
  *after* the r12 ladder run (last request `01:31:41Z`). Not in `~/.bash_history`
  (mtime `2026-09-28 20:04`, no `archive`/`mv` line) → the acting shell was not the one
  writing that history file; the operator/agent attribution is not determinable from this
  evidence. Note `~/Projects` mtime is `03:13:18Z`, 20 s earlier — see V15.
- **V23. Blast radius (durable impact).** **25 pre-existing files** cite `~/bench-arena`
  (26 once this artifact is counted; all counts in this bullet exclude this artifact):
  **14 durable prose** — `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`,
  `corpus/README.md`, `corpus/knowledge/{local-bench-arena,bench-arena-fresh-run,bench-arena-round5-battery,bench-arena-round6-stability,bench-arena-round7-scaffold-ablation,bench-arena-task27-timeout-anatomy}.md`,
  `corpus/lessons/{round-3,round-4-aggregator-audit,round-8-aggregator-box3-coldrun}.md`
  — plus **11 frozen evidence records** (round9/10/11/12 fleet files; historical, fine to
  leave as-is). Member occurrence breakdown: 11 hits on `~/bench-arena/grade.sh`, 5 on
  `loop.sh`, 3 on `telemetry-qwenlocal-v2.csv`, 3 on `report-qwenlocal-v2.v2.csv`,
  6 occurrences targeting `tasks/` paths (`tasks/`, `tasks`, `tasks/*/`, `tasks/$t`,
  `tasks/27-rwlock-writer-pref/test.sh`).
  Reproduce: ``grep -rho --include='*.md' '~/bench-arena[^ `),;]*' $(grep -rl --include='*.md' '~/bench-arena' . | grep -v round14-fleet) | sort | uniq -c | sort -rn``
  (file count: `grep -rl --include='*.md' '~/bench-arena' . | grep -v round14-fleet | wc -l` → `25`).
  **Consequence:** the *runner commands* in the knowledge entries
  (`cd ~/bench-arena && BENCH_ROOT=/tmp/X bash grade.sh <label>`;
  `BENCH_ROOT=<scratch> bash ~/bench-arena/grade.sh <label>`) are no longer reproducible
  as written. The fix is a one-token path suffix per citation
  (`~/bench-arena` → `~/archive/bench-arena`) plus a PROVINCE surface-row update; **not
  applied here** (this artifact is read-only outside its own file). Flagged for the landing.
- **V24. The r12 novelty claim is *not* affected.** `bench-arena` is cited only in
  round-12/14 *documentation*, never in the ladder itself: the r12 run used its in-repo
  harness (`corpus/evidence/round12-ladder/run_r12.py`, `probe_r12.py`), and
  `grep -rn 'bench-arena' corpus/evidence/round12-ladder corpus/evidence/round13-ack-state`
  → 0 hits. `LADDER / DISSOCIATION / TRANSPORT` rest on the endpoint + process pins, both
  re-verified above as `MATCH`. Only the citation hygiene is damaged.

## 6. `~/Projects/webzites/repos/llm-wiki` — `MATCH`

- **V25.** Resolves as a directory (`drwxr-xr-x`, mtime `2026-09-20 22:50`). All eight
  eval-relevant subpaths named in the PROVINCE row are `PRESENT`:
  `wiki/ai/agents-and-engineering`, `wiki/karpathy`, `wiki/ai/foundations`,
  `wiki/ai/alignment-and-training`, `wiki/ai/books`, `wiki/ai/scaling-and-forecasting`,
  `Home.md`, `raw`.
- **V26.** `git log -1` → `e66e614372ee1e72108faffa5c615b3fc27f4e57`,
  committer date `2026-08-08T21:40:55-03:00`, subject
  `Add product ship evidence for the static site pipeline.` Working tree clean
  (`git status --porcelain` empty).
- **V27.** Freshness: `find … -newermt '2026-09-28' -type f -not -path '*/.git/*'` → **0 hits**.
  Newest content file is `wiki/psychology/intelligence-analysis/…` at `2026-09-20 22:50`
  — same date r12 recorded. **No eval-relevant file newer than 2026-09-28**; the
  research-notes surface is unchanged and remains safe to digest.

## 7. Client CLI telemetry `~/.bailian/` — `MATCH` (present; stale, as its own entries say)

- **V28.** `~/.bailian/telemetry.jsonl` — **1,119,225 B**, **4,274 lines**, mtime
  `2026-09-16 18:52:37.721248773 -0300` (= `2026-09-16T21:52:37Z`). Last record's own
  timestamp is `2026-09-16T21:52:37.712Z` (`{"command":"auth status","success":true,…}`) —
  mtime and last-record time agree to the millisecond. `corpus/knowledge/bailian-cli-telemetry.md:3`
  claims "4,274 JSONL records" and `corpus/lessons/round-6-aggregator-audit.md:36` pins the
  same count → **reproduced exactly**. No new telemetry for 13 days, so the quota-vs-auth
  split stays a historical analysis; **no in-repo entry claims a dated freshness** for this
  file, so nothing is falsified.
- **V29.** `~/.bailian/wiki-sync-state.json` — **117 B**, mtime
  `2026-09-11 10:58:29.062481971 -0300` (= `2026-09-11T13:58:29Z`), content
  `{"lastChecked":1789135109062,"contentHash":"sha256:21a2692a7c2ffe0d0f15cd458407a60a213ecb5e8da029b8a3980f4026c6907d"}`.
  `lastChecked` epoch ms converts to `2026-09-11T13:58:29.062Z` — **identical to the file
  mtime**; the state file is internally consistent.
- **V30.** The PROVINCE "Model catalogs" row also resolves: `~/.bailian/skills/bailian-docs-llm-wiki/models/`
  contains `index.md`, `index.json`, `families.jsonl`, `models.jsonl` (+ `groups/`), all
  mtime `2026-09-11 10:58`; `index.md` header reads "共 180 个模型家族 · 413 个主干模型 · 更新于
  2026-09-11", matching `SKILL.md:561`. **MATCH.**

## 8. On-disk gguf — `MATCH` (r12 §3 artifact claim holds)

- **V31.** `stat` on `/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`
  → **`10333691040` B**, mtime `2026-08-29 02:39:38.068184831 -0300` (unchanged).
  Arithmetic re-checked: `data_offset 5 973 152 + Σ tensors 10 327 717 888 = 10 333 691 040`
  == on-disk size, and `meta.size` from the live endpoint is `10327717888` == the Σ-tensor
  term, `meta.n_params = 30532122624` == the Σ `ne` term r12 recorded. The r12 closure
  ("residual 0, no 10 GB hash needed") **re-derives**. `[INFERENCE]` note: I re-checked the
  *arithmetic and the size*, not r12's tensor-by-tensor re-derivation (that re-derivation is
  r12's committed evidence, not re-run here).

## 9. Contention / idleness caveat

- **V32.** At audit time there is **no competing client**: `ss -tan 'sport = :34113' | grep -c ESTAB`
  → `0`, and `ss -tan 'sport = :34113'` returns only the `LISTEN` row. The 8 `TIME-WAIT`
  rows with `dport = :34113` observed during the audit are this audit's own closed curls
  (client-side ephemeral ports). *Methodological warning:* the naive
  `ss -tan | grep -c 34113` → `10` is a trap (it counts `LISTEN` + `TIME-WAIT` peers); only
  the state-qualified form is meaningful. Round 12's command
  (`ss -tan state established | grep -c 34113` → 0) is correct and reproduces.
- **V33.** New fact r12 could not have seen: the endpoint **was used after the r12 run**.
  `journalctl --user -u qwen-coder.service --since @1790645501` (after r12's last request
  `01:31:41Z`) → **7** `slot release` lines, spanning `01:47:09Z`–`01:58:03Z`
  (last: `task 266634, n_tokens = 9`) — a short burst (~7 inferences in 11 min), not a
  battery run. Since then: **idle 1 h 31 m** at audit (last inference
  `2026-09-29T01:58:03Z`, now `03:29Z`). Any r14 run must therefore re-assert idleness at
  its own start time rather than inheriting r12's "idle since the r11 tail" premise.
- **V34.** `/tmp/bench-r8` still exists at audit time (the r8 harness scratch). It is
  `/tmp`-resident and therefore **not** durable evidence; entries that cite it remain debt
  under this lane's own rule ("nothing cited from `/tmp` … alone").

---

## 10. Discrepancies against stored claims (verbatim)

| Stored claim (verbatim, shortened) | Source | Observation |
|---|---|---|
| "`~/bench-arena/` \| **NO-DRIFT** \| present, 0 files newer than 2026-09-28 20:00, newest 2026-08-29 03:30:59" | `corpus/evidence/round12-fleet/r12-endpoint-freshness.md` §7 row 5 | **FALSIFIED at the path level** as of `2026-09-29T03:13:38Z`. Tree content claim survives; path claim does not (S9/S10 vs S11). |
| "Local benchmark battery \| `~/bench-arena/` — `tasks/`, `grade.sh`, `loop.sh`, … " | `PROVINCE.md:13` (§Surfaces, "re-verified round 11") | Cited path no longer resolves; members resolve under `~/archive/bench-arena/`. Needs a PROVINCE row update. |
| "`BENCH_ROOT=<scratch> bash ~/bench-arena/grade.sh <label>`" | `SKILL.md:330` (also `:567`, knowledge entries) | Command is no longer runnable as written; valid form is now `~/archive/bench-arena/grade.sh`. |
| "`~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT as of round 11**" | `PROVINCE.md:15` | **REPRODUCES** (S6–S8); no resurrection, no relocation. |
| "`created` … `[INFERENCE-moderate]` on the mechanism ('server stamps now')" | `r12-endpoint-freshness.md` §1.3 | **Confirmed [certain]** — 4 independent exact-to-the-second matches (S1/V3). |
| "`/proc/1299/cmdline` … 41 tokens, `EXACT_MATCH`" + "md5 … `e6642361e60173c15705a8108e547efa`" | `PROVINCE.md:14` (Served local model row), `r12-endpoint-freshness.md` §2 | **REPRODUCES exactly** (V6/V7). |
| "the two host surfaces that do not resolve are explicitly documented: bounties + `~/wikillm/llm-wiki`" | `r12-review-baseline.md:79` | **Now three** — `~/bench-arena` joined them (via relocation, not deletion). |
| "`~/.bailian/telemetry.jsonl` — 4,274 JSONL records" | `corpus/knowledge/bailian-cli-telemetry.md:3` | **REPRODUCES** (4,274; V28). |

## 11. Gaps

- **Relocation instant/actor**: bounded only by parent mtime `2026-09-29T03:13:38Z`;
  no shell-history record, no inotify trace exists. Operator-vs-agent attribution open.
  Affects: any claim of *when*/*by whom* `~/bench-arena` moved.
- **bounties deletion instant**: unpinned (only `~/Projects` mtime `03:13:18Z` as a loose
  upper bound). Whether the same event that moved bench-arena also removed bounties is
  `[INFERENCE]` only. Affects: the round-11/12 date narrative ("gone ~23:51Z").
- **`mv` vs copy+delete**: cannot be proven from the surviving tree (child mtime preserved
  is consistent with `mv`); the pre-move inode was never recorded by r12. Affects: nothing
  operational — content equality is established either way.
- **Host-wide (outside `/home/vgpnk`) search** for a `bench-arena` mirror or a `bounties`
  relocation was **not** run (searches were confined to `/home/vgpnk`, `xdev` for `/home`).
  Affects: "no relocation found" is scoped to the `/home` device, as in r11/r12.
- **GGUF tensor-by-tensor re-derivation** not re-run (size + arithmetic only). Affects: the
  strength of the `meta.size` closure (V31) — bounded to `[INFERENCE]` for the Σ-tensor leg.
- **`--cache-type-k/v q4_0`** is argv-only evidence (no runtime getter exists). Affects:
  the KV-quantization materiality claim remains process-argv-pinned, as in r10/r11/r12.

## 12. Reproduction (copy-paste, in order)

```bash
# 1-2. endpoint identity + health  (mask `created` to compare captures byte-for-byte)
curl -s -m5 http://127.0.0.1:34113/v1/models
curl -s -m5 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:34113/health
curl -s -m5 http://127.0.0.1:34113/props   # n_ctx, total_slots, build_info, chat_template
curl -s -m5 http://127.0.0.1:34113/slots   # 2 slot objects
# 3. process pin
ss -ltnp | grep 34113
md5sum /proc/1299/cmdline; wc -c < /proc/1299/cmdline
python3 - <<'EOF'   # 41/41 token compare vs unit
import re
u=open('/home/vgpnk/.config/systemd/user/qwen-coder.service').read()
block=re.search(r'ExecStart=(.*?)\n\n\[Install\]',u,re.S).group(1)
unit=re.sub(r'\\\s*\n\s*',' ',block).split()
proc=[t.decode() for t in open('/proc/1299/cmdline','rb').read().split(b'\0') if t]
print(len(unit),len(proc),'EXACT_MATCH' if unit==proc else 'DELTA')
EOF
# 4. route telemetry
test -e /home/vgpnk/Projects/bounties && echo PRESENT || echo ABSENT
find /home/vgpnk/Projects -maxdepth 2 -name 'bounties*'
find /home/vgpnk -xdev -maxdepth 6 -name telemetry.jsonl -path '*ledger*'
# 5. bench-arena  (NOTE: now at ~/archive/bench-arena)
find /home/vgpnk -maxdepth 4 -name 'bench-arena*'
find ~/archive/bench-arena -newermt '2026-09-28 18:00' -type f | wc -l
stat -c '%y' ~/bench-arena ~/archive/bench-arena ~/archive ~/Projects 2>&1
md5sum ~/archive/bench-arena/{grade.sh,loop.sh,telemetry-qwenlocal-v2.csv}
# 6. llm-wiki
git -C ~/Projects/webzites/repos/llm-wiki log -1 --format='%H %cI %s'
find ~/Projects/webzites/repos/llm-wiki -newermt '2026-09-28' -type f -not -path '*/.git/*'
# 7. bailian
stat -c '%s %y %n' ~/.bailian/telemetry.jsonl ~/.bailian/wiki-sync-state.json
wc -l ~/.bailian/telemetry.jsonl
# 8. gguf + contention + journal
stat -c '%s %y' /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf
ss -tan 'sport = :34113' | grep -c ESTAB
journalctl --user -u qwen-coder.service --since @1790640000 -o short-iso | grep 'slot .*release' | tail -3
```

**Net for the landing gate.** The r12 novelty claim (LADDER ESTABLISHED / DISSOCIATION
ESTABLISHED / TRANSPORT DIRECTIONAL) is **unaffected** — its two load-bearing live
surfaces (endpoint identity, process pin) re-verify at `MATCH`/`EXACT_MATCH` with byte- and
token-level pins, and the ladder never touched `bench-arena` (V24). The landing must,
however, either (a) update the 14 durable-prose citations of `~/bench-arena` to
`~/archive/bench-arena` and record the relocation in the PROVINCE surface row, or (b) record
the relocation as a dated host-drift with the path left as a historical citation — in both
cases the relocation is now md5-pinned (V21) so a future auditor can detect a further move
with one `find /home/vgpnk -maxdepth 4 -name 'bench-arena*'`.