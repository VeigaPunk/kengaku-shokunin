# R31SrcS100a — terminal-bench-2 root tree at the pin (S100)

Scout seat, round 31, lane `kengaku-shokunin`. Read-only source evidence; no production edits.
Pinned revision for every fetch: `2fd12b88aafdd04a52c298e3940bcb189f9766d6`.
Access date: **2026-10-25**. No clone performed; one contents call plus per-file `curl`.

## Fetch identity (observed, not inferred)

| step | observed |
|---|---|
| requested URL | `https://api.github.com/repos/laude-institute/terminal-bench-2/contents/?ref=2fd12b88aafdd04a52c298e3940bcb189f9766d6` |
| first response | `HTTP/2 301`, `location: https://api.github.com/repositories/1063848495/contents/?ref=2fd12b88…` (268 B body, no listing) |
| followed response | `HTTP/2 200`, 96537 B, `etag: "ec7c02c7f0b59ce8ed2f7c88d1e70cda7427edfa"` |
| repo slug in every entry | `url` fields → `api.github.com/repos/**harbor-framework/terminal-bench-2**/…`; `html_url` fields → `github.com/harbor-framework/terminal-bench-2/tree/2fd12b88…` |
| pin honoured in body | `all_ref_match=True` — all 92 `url` fields carry `ref=2fd12b88aafdd04a52c298e3940bcb189f9766d6` |
| commit object | `sha=2fd12b88aafdd04a52c298e3940bcb189f9766d6`, committer date `2026-04-30T05:53:30Z`, message `Add task metadata to task manifests`, **tree `ec7c02c7f0b59ce8ed2f7c88d1e70cda7427edfa`** |
| listing↔commit binding | the contents ETag equals the commit's tree sha (`ec7c02c7…`) — the listing I counted is the tree of the pinned commit, not of a default branch |

The repository named in the citation (`laude-institute/terminal-bench-2`) is a **301 alias**; the live
repository is `harbor-framework/terminal-bench-2` (numeric id `1063848495`). This matters for C3's
`--url-map` binding — see "Consequences for C1/C3" below.

## Captures (all under `/tmp/r31-R31SrcS100a/`, 328 KB total)

| file | source | sha256 | bytes |
|---|---|---|---|
| `contents.json` | root contents at the pin, followed through the 301 (HTTP 200) | `111e4365b7176f7ad03aa494c62edc22f1ab5c180b2ef29b83345d2aefb04f6a` | 96537 |
| `commit.json` | `api.github.com/repos/harbor-framework/terminal-bench-2/commits/2fd12b88…` (200) | `4a5e25d52fcc013ac29401cc75596d432cbb9ced80a23b502a9eb08ac222d822` | 164705 |
| `tags.json` | `…/tags?per_page=5` (200, body `[]`) | `2ba33ca0557f1bb5b7ba88d67f9d0093c7185a36ec51fe2b7bd9372d3e001d6d` | 5 |
| `README.md` | `raw.githubusercontent.com/…/2fd12b88…/README.md` (200) | `7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364` | 4574 |
| `protein-task.toml` | `…/2fd12b88…/protein-assembly/task.toml` (200) | `d714960681ec921a9247b382dfa0d8e97a9d13a3fe170a6ebd934ebe82398f24` | 973 |

## (a) Number of top-level entries, split by type

**92 entries: 89 directories, 3 files, 0 of any other type.**

## (b) The non-directory entries

Three, with their API-reported sizes:

| name | type | size (B) |
|---|---|---|
| `.gitignore` | file | 4561 |
| `LICENSE` | file | 11357 |
| `README.md` | file | 4574 |

No symlinks, no submodule entries, no `"type": "other"` rows. All 92 entries carry a `size` key
(directories report `0`, the contents-API convention).

## (c) Truncation

**Not truncated.** Three independent observations:

1. `grep -c '^link:' headers2.txt` → `0` — no `Link:` pagination header on the 200 response.
2. `grep -oE '"(truncated|incomplete)"[^,]*' contents.json` → no match; the contents endpoint has no
   truncation flag (that field belongs to the *git trees* endpoint, which I did not call).
3. 92 entries is far below the contents API's 1000-entry-per-directory cap, and the body is valid
   JSON with 92 balanced objects (`grep -c '^  {'` → 92).

The 301 response body (268 B) is **not** a listing and must not be counted; only the followed 200 body
was parsed.

## (d) Command and its output line

```bash
cd /tmp/r31-R31SrcS100a && python3 -c 'import json;d=json.load(open("contents.json"));print("top_level_entries=%d dirs=%d files=%d other=%d"%(len(d),sum(x["type"]=="dir" for x in d),sum(x["type"]=="file" for x in d),sum(x["type"] not in ("dir","file") for x in d)))'
```

output line:

```
top_level_entries=92 dirs=89 files=3 other=0
```

Fetch command that produced `contents.json`:

```bash
curl -sSL -D headers2.txt -o contents.json \
  "https://api.github.com/repos/laude-institute/terminal-bench-2/contents/?ref=2fd12b88aafdd04a52c298e3940bcb189f9766d6"
```

## What this count can establish

- The pinned tree's **root fan-out**: 89 top-level directories and exactly 3 top-level files, so the
  root carries no second namespace (no `tasks/`, `docs/`, `scripts/`, `.github/` directory at top level).
  Every top-level directory is therefore a candidate task package, not a project folder.
- The **registry numbers already recorded for this pin are correct**: S079's anchor
  (`corpus/SOURCES.md:101`) states "92 root entries at that commit, of which 89 are task directories",
  and the staged S100 row states "「89 task directories, plus .gitignore, LICENSE and README.md, i.e.
  92 top-level tree entries」". Both strings are satisfied by the bytes I fetched — the count clause of
  S100's anchor is present at the pinned revision and is not a paraphrase.
- That the repository **carries no git tags**: `GET …/tags?per_page=5` returned `200` with body `[]`
  (5 B), matching S100's "the repository carries **no** git tags". (Only the *absence* is established;
  the row's further claim that `harbor-framework/terminal-bench` is tagged `v3.0.0`/`v4.0.0` is a
  different repository and was not fetched by this seat.)
- The pinned `README.md` states **no task count** anywhere in its 100 lines (read in full): it points to
  `uv run harbor run --dataset terminal-bench@2.0` and to the repository URL (lines 46, 51). So the
  benchmark's own front page does not supply the number this count supplies — the count is a tree fact,
  not a published release fact.

## What this count cannot establish

- **It is not a count of valid tasks.** 89 directories is a *tree* fact; validity is a property of each
  package's `task.toml`, `instruction.md`, `tests/test.sh` and the oracle/nop runs against them. Nothing
  in a root listing inspects any of that. A directory named like a task may be incomplete, may lack a
  verifier, or may fail its own oracle.
- **It is not a count of graded items.** The harness runs a *dataset* (`terminal-bench@2.0`, README:46),
  and nothing in this tree says which of the 89 directories that dataset resolves, or whether the
  dataset is built from this commit at all.
- **It does not establish per-directory shape.** I enumerated the root only. Probed **1 of 89**
  directories (`headless-terminal`): `task.toml` 200, `instruction.md` 200, `tests/test.sh` 200;
  `run-tests.sh` 404, `Dockerfile` 404 at the task root. So the observed layout at this pin is
  `task.toml` + `instruction.md` + `tests/test.sh` (+ `tests/test_outputs.py` referenced at
  `tests/test.sh:14`), **not** the `run-tests.sh` convention. Whether all 89 share that shape is
  **unresolved** — it would take 89 more directory listings or one recursive tree call, both outside
  this seat's one-call bound.
- **It says nothing about the verifier's own correctness.** The one verifier I read shows why the count
  is blind to this: `headless-terminal/tests/test.sh:4-5` is
  `# Install curl` followed by `apt-get install -y vim` — a comment/action mismatch inside a shipped
  grading script. The count is identical whether that line is right or wrong.

## Corroboration for the C1 entry (S100-side, in scope)

The staged entry `knowledge/corpus/knowledge/benchmark-verifier-execution-model.md` cites S100 as
`# task tree at 2fd12b8` and puts the tree to work in its table row at entry line 31:
`| Terminal-Bench 2.0, protein-assembly/task.toml | timeout_sec = 1800.0 only | allow_internet = true | shared |`.
That located quote is **present at the pin** — `protein-assembly/task.toml`:

```
21:[verifier]
22:timeout_sec = 1800.0
24:[agent]
25:timeout_sec = 1800.0
27:[environment]
34:allow_internet = true
```

The `[verifier]` table holds `timeout_sec` **and nothing else** — in particular no `environment` key —
which is exactly the condition S092's `VerifierConfig.environment_mode` docstring resolves to `shared`.
Second sample agrees: `headless-terminal/task.toml` `[verifier]` at line 21 holds only
`timeout_sec = 900.0` (line 22), `allow_internet = true` at line 34. n = 2 of 89 configs read.

Two defects this seat can see in the staged entry, both outside its own repair scope:

1. **`verified-at` does not match the frozen predicate.** Entry line 5 reads `verified-at: 2026-10-23`
   and line 6 `recheck: … (ran 2026-10-23)`. C1's frozen predicate requires `verified-at: 2026-10-25`
   and `opened=2026-10-25` on the three rows. As staged, the entry would fail C1's own clause.
2. **S100 and S079 are the same document at the same pin.** `corpus/SOURCES.md:101` (S079) cites
   `https://github.com/laude-institute/terminal-bench-2` at `2fd12b88…`; the staged S100 row cites the
   identical URL at the identical commit, differing only in declared scope (`spec` vs `dataset`). C1's
   predicate needs "three distinct" ids, which the ids are — but a reviewer should decide whether a
   second row over one document at one commit is an admissible distinct source or a split row.

## Consequences for C3's URL binding (observed, for the lane)

The citation URL 301s. A capture bound literally to `laude-institute/terminal-bench-2` and compared
against a fetch made without `-L` yields a 268-byte redirect body, not the document — the gate would
either match nothing (a false refusal) or, if the mapping compares only the requested URL string, accept
a capture whose final URL is `harbor-framework/terminal-bench-2`. `--url-map` should therefore bind to
the **final** URL after redirects (`curl -L -w '%{url_effective}'`) and the map should be able to carry
an alias → canonical pair. This is the S100-side instance of exactly the gap round 30 disclosed.

## Confidence and remaining unknowns

- Observed, high confidence (verbatim bytes above, hashed): 92/89/3 split, the three file names and
  sizes, no truncation, ETag = tree sha, the 301 to repo id `1063848495`, zero tags, `[verifier]` blocks
  in two task configs, the `# Install curl` / `apt-get install -y vim` mismatch.
- [INFERENCE]: that the `[verifier]`-without-`environment` shape generalises to the other 87 configs
  (n = 2 only); that `/logs/verifier/reward.txt` written at `tests/test.sh:17-19` is the directory
  S092's `_remove_reward_files()` clears (Harbor's code is not this seat's source and was not read).
- Unresolved: per-directory manifest completeness for the other 87 dirs; whether the
  `terminal-bench@2.0` dataset resolves this commit; the other repository's `v3.0.0`/`v4.0.0` tag claim;
  the "first commit with exactly 89 task directories is f8f596a0…" clause (needs commit-list history,
  not fetched).
- No tool installed or upgraded this seat; nothing outside `/tmp/r31-R31SrcS100a/` was written.

VERDICT: PASS — the pinned root at `2fd12b88` holds **92 top-level entries (89 dirs, 3 files: `.gitignore`, `LICENSE`, `README.md`), response not truncated** (no `Link:` header, ETag `ec7c02c7…` equals the commit's tree sha), fetched through a **301 from `laude-institute/` to `harbor-framework/terminal-bench-2` (id 1063848495)**; the count confirms S079's and S100's recorded `92 / 89` clause and S100's "no git tags" clause, but it establishes only root fan-out — it is **not** a count of valid tasks, and the staged entry's `verified-at: 2026-10-23` fails C1's required `2026-10-25`.
