# R29a2RevQuoteS079 — S079 task-schema re-verification and independent task-directory count, 2026-10-25

Role: reviewer (leaf). Question: independently verify the S079 fields at the pinned commit, and
independently count the top-level task directories against the staged claim of 92.
Read-only outside this report; nothing edited under the lane, `shokuknow`, or any sibling lane.

**Verdict: 3 of 3 schema fields PASS. The staged claim of 92 FAILS as a task-directory count — the
pinned tree holds 89.** `92` is the root *entry* count (89 directories + 3 files). The lane's landed
entry has already restated this correctly; my independent measurement confirms its corrected numbers
**exactly**, including which three files. Three defects remain in the landed entry: the S079 locator
cites lines `1, 21, 22` and so cannot locate three of the five fields row H quotes (F3); the axis-H
sentence generalises "both time baselines" to any task directory although 1 of 89 carries neither
(F4); and the entry's own reproducing command for the count is a metered API call that today returns a
403 error body rather than the tree (F6).

## 0. Verdict table

| # | Field | Staged claim | Observed at pin | Verdict | Raw line |
|---|---|---|---|---|---|
| 1 | `schema_version` | `"1.1"` | `"1.1"` | **PASS** | task.toml:1 |
| 2 | `expert_time_estimate_min` | `60.0` | `60.0` | **PASS** | task.toml:18 |
| 3 | `junior_time_estimate_min` | `300.0` | `300.0` | **PASS** | task.toml:19 |
| 4 | top-level task dirs | `92` | **`89`** | **FAIL** | delta **−3** (claim overstates) |

Note on #4: the *landed* lane entry (`corpus/knowledge/benchmark-task-validity-checklist.md:54-56`)
already states `92 root entries … leaving 89 task directories and 89 task.toml files`. That is
**correct and my counts confirm it**. The FAIL attaches to the staged package text
(`SOURCES.append.md:9` and the staged copy's §Honest limits:66), which still reads as 92 *task
directories*.

## 1. Pin and fetch — three independent channels, one identity

Pinned commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`. Access date **2026-10-25**.

`git ls-remote https://github.com/laude-institute/terminal-bench-2` (2026-10-25) returned:

```
2fd12b88aafdd04a52c298e3940bcb189f9766d6	HEAD
2fd12b88aafdd04a52c298e3940bcb189f9766d6	refs/heads/main
```

The pin **is** current `main` as of the access date, so drift for this source is zero today and no
finding below can be attributed to a stale pin.

The same file was obtained over three channels:

| channel | sha256 |
|---|---|
| `git clone` + `git checkout 2fd12b8` | `d714960681ec921a9247b382dfa0d8e97a9d13a3fe170a6ebd934ebe82398f24` |
| `raw.githubusercontent.com/.../2fd12b8/protein-assembly/task.toml` (HTTP **200**) | `d714960681ec921a9247b382dfa0d8e97a9d13a3fe170a6ebd934ebe82398f24` |
| `codeload.github.com/.../tar.gz/2fd12b8` (40357259 B, HTTP **200**) | `d714960681ec921a9247b382dfa0d8e97a9d13a3fe170a6ebd934ebe82398f24` |

`diff` raw-API vs clone → identical, exit 0. File is **973 bytes, 41 lines**. The tarball is a
materialised tree independent of both the blobless partial clone and the single-file CDN route, so the
bytes are not an artifact of one retrieval path.

**No redirect hazard on the raw channel** (the hazard a sibling flagged for its own source):
`curl -sS -o /dev/null -w '%{http_code} %{num_redirects} %{url_effective}'` →
`code=200 redirects=0 effective=<the pinned URL itself>`, and the first response is `HTTP/2 200` with
no `Location` header. So the bytes above came from the pinned path directly, not via a redirect to a
mutable `main` URL. (Sibling `R29a2SrcS079` independently reproduced the same hash over four further
channels, including two raw hosts and a git blob-API decode; agreement is coincident, not shared.)

## 2. Field verification — raw lines, located

Source: `protein-assembly/task.toml` @ `2fd12b8`. Relevant lines verbatim:

```
 1  schema_version = "1.1"
...
12  [metadata]
15  difficulty = "hard"
18  expert_time_estimate_min = 60.0
19  junior_time_estimate_min = 300.0
21  [verifier]
22  timeout_sec = 1800.0
```

Byte-exact confirmation — `grep -Fxc '<quote>' protein-assembly/task.toml`, one hit each:

```
schema_version = "1.1"                   -> 1
expert_time_estimate_min = 60.0          -> 1
junior_time_estimate_min = 300.0         -> 1
difficulty = "hard"                      -> 1
timeout_sec = 1800.0                     -> 1
```

All requested fragments are **present verbatim** and typed as floats/string. Each is 3
whitespace-split tokens; the row's composite rendering is 9 tokens (≤25). The staged row joins three
separate lines with "beside" — correctly marked as composite, and it must not be collapsed into a
single pseudo-contiguous quote.

No kill-rule branch triggers for S079: the source opened on 2026-10-25 and every requested field was
located in the opened bytes.

## 3. Directory count — independent count, delta, root cause

Counted three ways at the pinned commit:

```
$ git ls-tree -d --name-only 2fd12b88aafdd04a52c298e3940bcb189f9766d6 | wc -l          -> 89
$ ls -d */ | wc -l                                                                    -> 89
$ find <tarball>/terminal-bench-2-2fd12b8... -mindepth 1 -maxdepth 1 -type d | wc -l   -> 89
```

Every one of the 89 is a genuine task package: **89 `task.toml` in the whole tree**, and all 89 at
depth 2 (`find . -name task.toml | awk -F/ 'NF!=3'` → empty), so "top-level task directories" =
"task packages" = **89** under every reading. No nested `tasks/` directory (`ls -d tasks` →
`No such file or directory`).

**Own count: 89. Delta from the staged 92: −3 (claim overstates by 3).**

### Root cause — proven, not inferred

```
$ git ls-tree --name-only 2fd12b8 | wc -l          -> 92      # ALL root entries
$ git ls-tree -d --name-only 2fd12b8 | wc -l       -> 89      # directories only
FILE: .gitignore
FILE: LICENSE
FILE: README.md
dirs=89 files=3 total=92
```

`92 = 89 task directories + .gitignore + LICENSE + README.md`. The staged figure is the **total root
tree-entry count**, not the task-directory count. The repo's own history shows the confusion:
between `ba06af1` and `2ef6e27` the total moved `91 -> 92` while directories stayed `89` — the only
change was adding `.gitignore` (introduced in `13946e7`), which is not a task.

**Stale-pin hypothesis excluded.** Directory counts over the last 25 commits:

```
2fd12b8 dirs=89 total=92   8773c98 dirs=89 total=92   53ff2b8 dirs=89 total=92
f5b891c dirs=89 total=92   a5b64de dirs=89 total=92   2ef6e27 dirs=89 total=92
ba06af1 dirs=89 total=91   b3418b6 dirs=90 total=92   7b0cccc dirs=91 total=93
0a3c2f7 dirs=94 total=96   2e2b23c dirs=102 total=103
```

`dirs=92` never occurs in this range, so `92` is not an earlier tree's task count carried forward —
it is the entry-count method applied at the correct pin.

## 4. Findings by severity

### F1 — MEDIUM (staged package only): "92 top-level task directories" is wrong; correct value 89

Still present in the adoption inputs, as a *task-directory* count:

- `…/merge/kengaku/SOURCES.append.md:9` (S079 artefact cell): "**92 top-level task directories** in
  the tree at that commit".
- `…/merge/kengaku/knowledge/corpus/knowledge/benchmark-task-validity-checklist.md:66` (§Honest
  limits): "**92 task directories** in `laude-institute/terminal-bench-2` at commit `2fd12b8`".

Independent measurement: 89 (§3). Correction must be applied in **both** places, to the wording the
lane has already adopted: "89 task directories, plus `.gitignore`, `LICENSE` and `README.md`, i.e. 92
top-level tree entries". The landed lane entry already uses that form, so this is a reconcile-to-
canonical-wording fix, not a new judgement.

### F2 — POSITIVE confirmation: the landed entry's corrected counts are exactly right

`corpus/knowledge/benchmark-task-validity-checklist.md:54-56`:

```
- S079 repository at `2fd12b8`: **92 root entries**, of which 3 are files (`.gitignore`,
  `LICENSE`, `README.md`), leaving **89 task directories and 89 `task.toml` files**
```

Every element matches my independent measurement: 92 non-recursive root entries; 89 directories; **89
`task.toml`**; and the three non-directory entries are precisely `.gitignore`, `LICENSE`, `README.md`
(named identically, no more, no fewer). The entry also attaches the producing command
("`git/trees/2fd12b8` non-recursive, then `task.toml` count over the recursive tree"), which is the
right remedy for a count that was previously unit-ambiguous. No action needed on these numbers.

### F3 — MEDIUM (landed entry, new): the S079 locator cites `lines 1, 21, 22` and cannot locate three of the five fields row H quotes

Landed `source:` line (entry line 3):

```
source: S079 — https://github.com/laude-institute/terminal-bench-2 — `protein-assembly/task.toml` lines 1, 21, 22 — commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`
```

Row H (entry line 33) quotes five fields from that file. Resolving the locator against the pinned
bytes:

| field quoted by row H | actual line | cited by locator? |
|---|---|---|
| `schema_version = "1.1"` | 1 | **yes** |
| `difficulty = "hard"` | 15 | **no** |
| `expert_time_estimate_min = 60.0` | 18 | **no** |
| `junior_time_estimate_min = 300.0` | 19 | **no** |
| `timeout_sec = 1800.0` | 22 | yes |

and the middle cited number is not a field at all:

```
  21: [verifier]
```

So the locator points at a bare table header and omits the three declared-field lines (15, 18, 19)
that carry the row's load. As written, a reviewer following the pointer would land on `[verifier]` and
two of five quotes, then have to search for the rest — which is exactly the failure mode the entry
elsewhere rules out ("a row that carries a count must carry the command that produced it"; here, a
row that carries a quote must carry the line that produces it).

Fix: cite `lines 1, 15, 18, 19, 22` (or the span `1, 15-19, 22`). The two time baselines are the
fields my acceptance centres on and they are the ones currently unlocated, so this is not cosmetic.

### F4 — LOW (landed entry, new): the axis-H sentence generalises "both time baselines" to *a* task directory, but 1 of 89 carries neither

Landed entry lines 44-46:

```
- S079 shows the fields axis H depends on are authored, not inferred: a task directory
  carries `schema_version = "1.1"` and both time baselines, so a reviewer reads the claim
  instead of guessing it.
```

Measured over all 89 `task.toml` in the pinned tarball:

```
$ ls -1 */task.toml | wc -l                                                  -> 89
$ grep -l '^expert_time_estimate_min' */task.toml | wc -l                    -> 88
$ grep -l '^junior_time_estimate_min' */task.toml | wc -l                    -> 88
(tasks carrying BOTH)                                                        -> 88
# per-file count of *_time_estimate_min lines; every file has 2 except:
$ for f in */task.toml; do n=$(grep -c '_time_estimate_min' "$f"); [ "$n" -ne 2 ] && echo "$f -> $n"; done
caffe-cifar-10/task.toml -> 0
$ grep -n -E 'schema_version|time_estimate' caffe-cifar-10/task.toml
1:schema_version = "1.1"
```

`caffe-cifar-10` (840 bytes, 39 lines) is the **unique** counterexample: it carries `schema_version`,
`[task]`, `[[task.authors]]`, `[metadata]` (with `difficulty`/`category`/`tags` at lines 15-17) and
`[verifier]`/`[agent]` (each `timeout_sec = 1200.0`, lines 20 and 23), but it has **zero**
`*_time_estimate_min` lines anywhere in the file (`grep -c` → 0), while each of the other 88 has
exactly two. So "a task directory carries … both time baselines" is false for exactly 1 of 89 — the
exact counterexample to the sentence. The sentence is true of the task S079 actually evidences
(`protein-assembly`, lines 18-19) and false as a statement about task directories in general. Minimal
truthful fixes: scope it ("**this** task directory", or name `protein-assembly`), or state the split
("88 of 89 carry both; `caffe-cifar-10` carries neither"). This matters because the sentence is the
entry's whole justification for axis H being an authored, readable field rather than an inferred one —
and the instrument must not overstate what the maintainers publish.

Related, and fatal to any *mechanical* axis-H check (in scope as a consequence, not a claim I
adjudicate): exactly **6 field lines across 3 tasks** write integer literals rather than floats, and in
each task the deviation is the *pair* at lines 18-19 —

```
count-dataset-tokens/task.toml:18:expert_time_estimate_min = 30   :19:junior_time_estimate_min = 120
reshard-c4-data/task.toml:18:expert_time_estimate_min = 30        :19:junior_time_estimate_min = 60
train-fasttext/task.toml:18:expert_time_estimate_min = 30         :19:junior_time_estimate_min = 90
```

so a float-only parser, or a `grep '= [0-9]*\.[0-9]'` check, would fail the **task** (3 of 89), not
an isolated line — `protein-assembly` itself is a clean float on both fields, so this does not touch
my acceptance.

### F5 — RESOLVED in the landed entry; still true of the staged copy: access-date re-grounding

Landed entry now carries `verified-at: 2026-10-25` and
`recheck: 180d — re-fetch … (next due 2027-04-23)`; `grep -o '2026-10-2[0-9]'` over the landed file →
**3 × `2026-10-25`, 0 × `2026-10-23`**. Re-grounding is discharged for S079 on my evidence (§1–§2).

The staged copy (`…/merge/kengaku/…checklist.md`, mtime `2026-10-24 23:33:20`) still holds
`verified-at: 2026-10-23` and three `2026-10-23` dates. If the merge package is what is later
compared back, its dates must be re-synced to `2026-10-25`, or the two artefacts will disagree.

### F6 — MEDIUM (landed entry, operability): the entry's stated reproducing command for the S079 count is a metered API call that currently returns an error body, not the source

Entry line 67 offers, as the reproduction of a load-bearing count:
"(`git/trees/2fd12b8` non-recursive, then `task.toml` count over the recursive tree)" — an
`api.github.com` call. Measured 2026-10-25 from this host:

```
$ curl -sS -o api-trees-noL.txt -w 'code=%{http_code} redirects=%{num_redirects} bytes=%{size_download}\n' \
    https://api.github.com/repos/laude-institute/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6
code=403 redirects=0 bytes=280
$ head -c 300 api-trees-noL.txt
{"message":"API rate limit exceeded for 179.218.13.209. (But here's the good news: Authenticated
 requests get a higher rate limit. …
$ curl -sS https://api.github.com/rate_limit        # unmetered
{'limit': 60, 'remaining': 0, 'reset': 1792913923, 'used': 60}
```

The command the entry publishes returns a **403 whose 280-byte body is a rate-limit message with zero
source bytes** — unauthenticated quota is 60/hr per IP and was exhausted. Two consequences:

1. A Gate that pipes that response into a parser either crashes or, worse, silently counts zero
   `task.toml` and reports a false small number — precisely the "count without a reproducible command"
   failure the entry's own rule ("a row that carries a count must carry the command that produced it")
   exists to prevent. The command is right in shape and wrong in robustness.
2. Sibling `R29a2SrcS079` separately measured this same endpoint returning **301 Moved Permanently**
   (264-byte body, redirect to the numeric repository id) on the legacy path form. I did not
   reproduce the 301 — quota was already exhausted, and GitHub meters before redirecting — so I record
   that half as their observation, not mine. Either way the endpoint is redirect- and quota-fragile.

Quota-free routes that reproduce the identical numbers, both used for §3:

```
$ git ls-tree -d --name-only 2fd12b8 | wc -l                                   -> 89   # on a clone
$ git ls-tree --name-only 2fd12b8 | wc -l                                      -> 92
$ find <codeload-tarball>/terminal-bench-2-2fd12b8… -mindepth 1 -maxdepth 1 -type d | wc -l  -> 89
```

Recommendation: cite `git ls-tree` on a pinned clone (or the codeload tarball) rather than
`git/trees/…`; those need neither a token nor `-L` and cannot return an error body in place of the
tree. Entry line 69's companion command for S080 (`contents/tasks/finalpool?ref=9be8d8f`) is the same
class of metered endpoint with the same risk; the S080 seat owns that row, so I flag rather than
adjudicate it.

This is the only finding here that touches *operability* directly: the count is correct (F2), but the
method the entry publishes is not re-runnable from a clean host without a token.

## 5. Residual risk and verification gaps

- **Out of scope, not verified by me:** the sibling count `109 entries under tasks/finalpool` /
  `108 directories` for `hkust-nlp/Toolathlon` at `9be8d8f` (landed entry line 57-58). I did not fetch
  Toolathlon. Note that entry line 69's reproducing command for it
  (`contents/tasks/finalpool?ref=9be8d8f`) is the same metered `api.github.com` class as F6's, so it
  carries the same quota/redirect fragility — the S080 seat should check both the number and the
  command.
- S077/S078/S080/S090 line citations in the landed entry were not verified by me (sibling seats own
  them); I read them only as context.
- Drift assessed solely as "pin == `main` HEAD on 2026-10-25". The pin remains the correct citation
  anchor today; the 180d recheck has nothing to catch yet.
- The axis-H fleet caveat (baselines absent on one task; three tasks use integer literals) was
  raised by sibling `R29a2SrcS079` and **I independently verified both halves** in F4 from the pinned
  tarball (88/89 carry both baselines; `caffe-cifar-10` carries none; 6 integer-literal lines across
  3 tasks). It does not affect the S079 row, which is scoped to one clean-float task, but it does bear
  on any claim that axis H is mechanically checkable fleet-wide.
- I make no claim about C1 admission or about the benchmark's own correctness — only that these bytes
  exist at this commit and that the directory count is 89.
- No `lsp` server applies (no code under review; the objects are a pinned external tree and staged
  markdown), so caller/definition checks were done with `git ls-tree` on the commit object and
  `grep -Fxc` byte matching rather than semantic queries.

## 6. Tooling record

No installs or upgrades were needed or performed — `git`, `curl`, `tar`, `find`, `sha256sum`, `diff`,
`wc`, `grep`, `stat` only. No pacman, `uv`, npm or cargo transaction was attempted, so the host-wide
pacman pause was not engaged and no update-safety gate was reached.

Scratch (all outside the lane): `/tmp/r29a2-RevQuoteS079/` — `tb2/` (blobless clone at the pin),
`protein-api.toml` (raw-API copy), `tb2.tar.gz` + `tar/` (codeload materialisation), `topdirs.txt`,
`intlines.txt`.

**Durability:** every number in this report is inlined with the command that produced it (§1 channel
hashes, §2 raw lines, §3 counts and history, F4 distribution). The `/tmp` scratch is a convenience
copy only — no finding here depends on it surviving, and nothing here cites a volatile `scratch/`
tree. A reader can re-derive all of it from the pin with the commands shown.

Report path: `.ufo/waves/round-29/attempt2/build/R29a2RevQuoteS079.md`.
