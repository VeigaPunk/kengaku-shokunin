# R31SrcS100b — do Terminal-Bench 2.0 / SWE-bench Pro V2 set `environment_mode` or `[verifier.environment]`? (S100, S093)

Scout seat, round 31, lane `kengaku-shokunin`. Read-only source evidence; no production edits, no
clone, per-file `curl` + `gh api` only. Scratch: `/tmp/r31-s100b/` (14 MB).
Access date: **2026-10-25**.

Pinned revisions (both verified to exist and to be the commit whose tree I enumerated):

| repo | commit | committer date | commit subject | tree |
|---|---|---|---|---|
| `laude-institute/terminal-bench-2` | `2fd12b88aafdd04a52c298e3940bcb189f9766d6` | 2026-04-30T05:53:30Z | "Add task metadata to task manifests" | `ec7c02c7f0b59ce8ed2f7c88d1e70cda7427edfa` |
| `scaleapi/SWE-bench_Pro-os` | `66f92766bba642462d4bbe5479e83f91f9211862` | 2026-09-22T21:00:20Z | "Merge pull request #119 from scaleapi/release/v2.0.0" | `beb15336e37995a2dc2e5908e2bde931d59cef1e` |

**This is a sample, not an exhaustive grep.** 6 of 731 task manifests were read in full:
3 of 89 in `terminal-bench-2` (3.4 %) and 3 of 642 in `SWE-bench_Pro-os` (0.47 %). The population
counts below are exact (git tree API, `truncated: false`); the *key-presence* finding is not.

## The sweep, verbatim

Population enumeration — one recursive tree call per repo, paths and blob ids only, no content:

```
gh api "repos/laude-institute/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1"
gh api "repos/scaleapi/SWE-bench_Pro-os/git/trees/66f92766bba642462d4bbe5479e83f91f9211862?recursive=1"
```

Sample selection, deterministic and stated before the read: **the task the staged entry itself cites
plus the alphabetically first and last task directory** in each repo.

```
# contents API, one call per sampled task directory (6 calls)
gh api "repos/laude-institute/terminal-bench-2/contents/adaptive-rejection-sampler?ref=2fd12b88…"
gh api "repos/laude-institute/terminal-bench-2/contents/protein-assembly?ref=2fd12b88…"
gh api "repos/laude-institute/terminal-bench-2/contents/write-compressor?ref=2fd12b88…"
gh api "repos/scaleapi/SWE-bench_Pro-os/contents/v2/tasks/instance_NodeBB__NodeBB-00c70ce7…-vnan?ref=66f92766…"
gh api "repos/scaleapi/SWE-bench_Pro-os/contents/v2/tasks/instance_internetarchive__openlibrary-00bec1e7…?ref=66f92766…"
gh api "repos/scaleapi/SWE-bench_Pro-os/contents/v2/tasks/instance_tutao__tutanota-f3ffe17a…?ref=66f92766…"

# raw fetch of each sampled task.toml at the pinned commit (6 fetches)
curl -sS "https://raw.githubusercontent.com/laude-institute/terminal-bench-2/2fd12b88…/<task>/task.toml"
curl -sS "https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766…/v2/tasks/<task>/task.toml"

# then: git-blob-sha1 recompute (sha1("blob <len>\0"+bytes)) compared against BOTH the contents-API
# `sha` and the tree-API `sha` for the same path; sha256 of the same bytes; tomllib.loads() parse.
```

Reproducer script: `/tmp/r31-s100b/sweep.sh` (idempotent, re-runs the whole sweep into a fresh dir).
Parse is `tomllib`, not a regex — the key sets below are parsed TOML tables.

## Sweep output (verbatim, exit 0)

```
POPULATION tb2@2fd12b88aafd: task.toml=89 distinct_blobs=89 tree_truncated=False
POPULATION swb@66f92766bba6: task.toml=642 distinct_blobs=642 tree_truncated=False
{"repo": "tb2", "path": "adaptive-rejection-sampler/task.toml", "bytes": 1089, "schema_version": "1.1", "verifier_keys": ["env", "timeout_sec"], "verifier_env_empty_table": true, "verifier_environment_section": false, "environment_mode_substring": false, "literal_verifier_environment": false}
   blob=cf4699bf288095a71e5bd6bc99ef88c198b5bdfe matches_tree=True sha256=6ed7b37f74beb46e9d47b0f5fad53025667c9548baff4e96d467b56d429fab1a
{"repo": "tb2", "path": "protein-assembly/task.toml", "bytes": 973, "schema_version": "1.1", "verifier_keys": ["env", "timeout_sec"], "verifier_env_empty_table": true, "verifier_environment_section": false, "environment_mode_substring": false, "literal_verifier_environment": false}
   blob=cbfcbbc4e00217a4c8e299caddfaffc2956ef32c matches_tree=True sha256=d714960681ec921a9247b382dfa0d8e97a9d13a3fe170a6ebd934ebe82398f24
{"repo": "tb2", "path": "write-compressor/task.toml", "bytes": 866, "schema_version": "1.1", "verifier_keys": ["env", "timeout_sec"], "verifier_env_empty_table": true, "verifier_environment_section": false, "environment_mode_substring": false, "literal_verifier_environment": false}
   blob=ef8bc825dced411ecc37c987bfa3774d08bcc060 matches_tree=True sha256=6066a509066433c97c417fea68c4e3e73996f698dcdcbabe07718835eea355a6
{"repo": "swb", "path": "v2/tasks/instance_NodeBB__NodeBB-00c70ce7b0541cfc94afe567921d7668cdc8f4ac-vnan/task.toml", "bytes": 787, "schema_version": "1.4", "verifier_keys": ["collect", "env", "network_mode", "timeout_sec"], "verifier_env_empty_table": true, "verifier_environment_section": false, "environment_mode_substring": false, "literal_verifier_environment": false}
   blob=18e4788c86ff850c3568153c21680643ca252d4f matches_tree=True sha256=e05817107e10163e3e903dd314a26abbae5dca429d2193f4884689c9f67ce926
{"repo": "swb", "path": "v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/task.toml", "bytes": 889, "schema_version": "1.4", "verifier_keys": ["collect", "env", "network_mode", "timeout_sec"], "verifier_env_empty_table": true, "verifier_environment_section": false, "environment_mode_substring": false, "literal_verifier_environment": false}
   blob=8692569efd715594bd98c44f5b2b9fc582f999be matches_tree=True sha256=b9c19d0309e910aa6acac8167ddac9c60f05aecb0d7abe1243c271c882393ad0
{"repo": "swb", "path": "v2/tasks/instance_tutao__tutanota-f3ffe17af6e8ab007e8d461355057ad237846d9d-vbc0d9ba8f0071fbe982809910959a6ff8884dbbf/task.toml", "bytes": 863, "schema_version": "1.4", "verifier_keys": ["collect", "env", "network_mode", "timeout_sec"], "verifier_env_empty_table": true, "verifier_environment_section": false, "environment_mode_substring": false, "literal_verifier_environment": false}
   blob=37a5ac46da0f0a15b4e30b4aed3e28ee7406fef3 matches_tree=True sha256=1617803a10b972b3f7395e9b6ba3dbc6bb6098de6d34e695ec1ae8603e010a2d

SAMPLED 6 files; environment_mode anywhere: False | [verifier.environment] section: False | literal "[verifier.environment": False
ALL BLOB IDS MATCH TREE: True
```

Every one of the 6 blobs is byte-identical to the blob id reported by **two independent API surfaces**
(contents API `sha` and tree API `sha`), so the bytes parsed are the bytes at the pinned commits —
not a branch tip, not a cache.

## (a) The keys the sampled `[verifier]` sections carry

TB2 — three of three identical in shape (`schema_version = "1.1"`):

```
21	[verifier]
22	timeout_sec = 1800.0        # protein-assembly; 900.0 in adaptive-rejection-sampler and write-compressor
37	[verifier.env]              # empty table
```

Parsed key set: **`env`, `timeout_sec`** — nothing else. `env` is an *empty* table, present only
because the file declares a bare `[verifier.env]` header.

SWE-bench Pro V2 — three of three byte-identical in this block (`schema_version = "1.4"`):

```
18	[verifier]
19	network_mode = "public"
20	timeout_sec = 3000.0
21	collect = []
23	[verifier.env]              # empty table
```

Parsed key set: **`collect`, `env`, `network_mode`, `timeout_sec`**.

`timeout_sec` is **not** uniform across TB2: 1800.0 for `protein-assembly`, 900.0 for the other two
samples. A card must not generalise the entry's single-task cell to the family.

## (b) `environment_mode` and `[verifier.environment]`

- `environment_mode` — **absent** in 6 of 6: absent as a parsed key anywhere in the document and
  absent as the literal substring (the string does not occur even in a comment).
- `[verifier.environment]` — **absent** in 6 of 6: `verifier.environment` is not a table in any
  parsed document, and the literal `[verifier.environment` does not occur.
- The near-misses that a careless grep could mistake for a hit, all in these same files:
  - `[verifier.env]` — an **empty** table (`tb2:37`, `swb:23`). `env` ≠ `environment`.
  - A sibling **directory** named `environment/` in every sampled task directory (contents API:
    TB2 dirs are `.gitignore, README.md, environment, instruction.md, solution, task.toml, tests`;
    SWE dirs are `environment, instruction.md, solution, task.toml, tests`). That is the image build
    context, not a TOML section.
  - `[environment]` / `[environment.env]` — the *agent* environment block, present in all 6.

So on this sample the claim holds, and it holds for a sharper reason than the entry states: the
verifier's only sub-table in every sampled manifest is the empty `env` table, so the
`"separate"`-triggering `[verifier.environment]` cannot be set without adding a section that no
sampled task has.

## (c) What the entry's table gets right and wrong against these bytes

| entry cell | bytes | note |
|---|---|---|
| TB2 `[verifier]`: "`timeout_sec = 1800.0` only" | `timeout_sec = 1800.0` (`protein-assembly:22`) + empty `[verifier.env]` (`:37`) | correct for non-empty keys; "only" is false for the parsed key set, which contains `env` |
| SWE `[verifier]`: "`network_mode`, `timeout_sec`, `collect = []`" | `:19-21` exactly | correct; omits the empty `[verifier.env]` at `:23` |
| TB2 `[environment]`: "`allow_internet = true`" | `:34`, plus `build_timeout_sec, docker_image, cpus, memory_mb, storage_mb, gpus, mcp_servers, env` | true but partial |
| SWE `[environment]`: "`network_mode = "public"`" | `:30`, plus 7 more keys | true but partial |
| "verified by grepping every `*.toml` in both trees" | tree API: TB2 has **90** `.toml` paths of which 89 are `task.toml` (the extra is `modernize-scientific-stack/environment/pyproject.toml`); SWE has **643** of which 642 are `task.toml` (the extra is `v2/tooling/configs/codex_config.toml`) | the stated method sweeps a slightly larger set than "task manifests"; the two non-manifest files are not task configs and would not affect the verdict, but the method sentence should say `task.toml` |
| entry cites SWE task as `instance_internetarchive__openlibrary-…` (elided) | 82 openlibrary instances exist; the sampled one (`00bec1e7…`) matches the entry's cell values exactly, as do the two other SWE samples | the elided path should be given in full in the entry |

**Substantive observation the entry omits** (observed bytes, not inference): the SWE manifests set
`[agent] network_mode = "no-network"` (`:26`) while `[verifier] network_mode = "public"` (`:19`).
The verifier's network policy differs from the agent's, in the same file, in the same task. That is
the exact asymmetry the entry's shared-mode argument turns on, and it is not in the entry's table.
[INFERENCE] How Harbor reconciles a verifier-level `network_mode` with the agent container in shared
mode is decided in `src/harbor/…` (S092's surface) and was **not** read by this seat.

## Scope statement (why this is a sample)

- Read in full: **6** task manifests. Enumerated by path and blob id only: 89 + 642.
- Not read: 83 TB2 manifests, 639 SWE manifests, the two non-manifest `.toml` files, and any nested
  toml inside each task's `environment/` build context.
- Therefore: the claim "no task in either repository sets `environment_mode` or a
  `[verifier.environment]` section" is **consistent with** this sample and **not established
  exhaustively** here. The entry's own sentence claims an exhaustive grep; this seat cannot confirm
  or refute that sentence, only the 6 files it read.
- Cheap path to closing it, if wanted: the tree API already returns all 731 blob ids in two calls, so
  a full raw sweep is 731 small `curl`s and ≈0.6 MB (the six sampled manifests average 911 B) — a
  future seat can make the claim exhaustive
  without a clone. Deliberately not done here (the assignment fixed a bounded sample).

## Remaining unknowns

- Whether `environment_mode` is even an accepted key in `task.toml` `schema_version` 1.1 / 1.4
  (Harbor's `TaskConfig`). If it is not, the negative is trivially true for reasons other than
  benchmark choice. S092's surface; not read here.
- The other 725 manifests.
- Whether a task's `environment/` build context or `solution/` carries a toml that sets either key.

## Confidence

- **High / observed**: population counts (89, 642, both `truncated: false`), the six key sets,
  absence of `environment_mode` and `[verifier.environment]` in the six files, blob-id identity of
  every fetched byte against two API surfaces, commit identities and dates, the `*.toml` population
  sizes (90 / 643), the `[agent] no-network` vs `[verifier] public` asymmetry.
- **[INFERENCE]**: that `[verifier.env]` being empty means no verifier environment override is in
  play (it follows from Harbor's stated resolution rule, which this seat did not re-read); that the
  empty `env` table is emitted by a serialiser rather than authored by hand.
- **Not established**: the exhaustive form of the claim.

Tooling: no installs or upgrades performed — `gh 2.102.0` (already present, keyring-auth as
`VeigaPunk`, 21 API calls: 3 exploration listings, 10 for the sample, 8 re-run by the end-to-end
sweep), `curl`, `python3 3.14.8` with `tomllib`.
Scratch 14 MB of the 60 MB allowance.

VERDICT: PASS (sample-scoped) — in 6 of 6 sampled `task.toml` at `terminal-bench-2@2fd12b88` and `SWE-bench_Pro-os@66f92766`, `environment_mode` does not occur and no `[verifier.environment]` section exists; the sampled `[verifier]` sections carry exactly `{env, timeout_sec}` (TB2, `env` empty) and `{collect, env, network_mode, timeout_sec}` (SWE, `env` empty). The claim survives on this sample; it is NOT verified exhaustively, and the entry's "grepping every `*.toml`" method sentence should read `task.toml`.
