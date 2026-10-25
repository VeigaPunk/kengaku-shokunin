# R29 source-output ordering — test.json write precedes parse; ordinal write index, never task_id

Seat: `KengakuR28.R29ContractIndexAndWrites-2` (leaf; no dispatch). Actual writer: this seat.
Round: kengaku29 only. `plans/round-29-claims.md` read first. Base `ed26bdf5d924755697cd6812129be2fa441c42a3`;
lane HEAD `31934e5660f1814326c6472eefdfa0c41e642a2f` (preregistration); working tree only untracked
`.ufo/waves/round-29/`.

Slice (one question): in pinned `scripts/generate_test_data.py`, does the `config_files/test.json`
write precede `json.loads`, and are per-task output filenames the enumeration ordinal rather than
`item["task_id"]`? Static source reading only: AST/bytes, no upstream import/exec/eval, no network,
no `config_files/test.json` or numbered files created anywhere.

Godspeed axes: (1) ordering fidelity — every claim tied to a source line; (2) unit separation —
existence, count and content of artifacts never pooled; (3) no fabrication — hand cases labelled by
evidence tier, not presented as executed.

## Evidence inputs (opened, hashed, retained)

| path | bytes | sha256 | status |
|---|---:|---|---|
| `plans/fixtures/r29/generate_test_data.py` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | matches r29 manifest pin |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | 880776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | matches r29 manifest pin |
| `plans/fixtures/r29/profiles.json` | 1391 | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | matches manifest |
| `plans/fixtures/r29/manifest.json` | 1061 | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | matches declared pin |

Manifest-declared generator URL (opened 2026-10-21 per manifest `opened`):
`https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py`.
No network request was made (lane prohibition); the URL→bytes binding is the manifest pin plus the
recomputed sha256 above, not an online re-fetch this round. Generator has 27 lines, UTF-8 ASCII-only.

Commands: `sha256sum`, `wc -c`, `ast.parse` over the retained bytes, and one read-only `json.loads`
census of the frozen raw fixture. Nothing else executed.

## Static ordering evidence (source lines, exact)

`ast.parse` of the pinned bytes gives sole `main()` (lines 8–23) with this body order:

| # | node | lines | content |
|---:|---|---|---|
| 0 | With | 9–10 | `open('config_files/test.raw.json', 'r')` → `raw = f.read()` |
| 1–6 | Assign | 11–16 | six `raw = raw.replace(...)` in GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP order |
| 7 | With | 17–18 | `open('config_files/test.json', 'w')` → `f.write(raw)` |
| 8 | Assign | 20 | `data = json.loads(raw)` |
| 9 | For | 21–23 | `for idx, item in enumerate(data)` → `open(f'config_files/{idx}.json', 'w')` → `json.dump(item, f, indent=2)` |

Located quotes, word count computed as `len(span.split())` on the exact line span:

| Lines | Quote | Words |
|---|---|---:|
| 17–18 | `with open("config_files/test.json", "w") as f:` / `f.write(raw)` | 6 |
| 18–20 | `f.write(raw)` / `# split to multiple files` / `data = json.loads(raw)` | 9 |
| 22–23 | `with open(f"config_files/{idx}.json", "w") as f:` / `json.dump(item, f, indent=2)` | 8 |

All three are ≤25 words. Line 19 is a comment only; it produces no AST node and no behavior.

Derived ordering facts:

1. The `with` on 17–18 exits (file flushed and closed) before line 20 runs. So `test.json` is
   written and closed *before any JSON validation*; it is complete-but-unvalidated at parse time.
2. Line 20 parses the in-memory `raw` string written at line 18; `test.json` is never re-read.
   Therefore `test.json` content and parse input are the same `str`; any on-disk/parse divergence
   can only come from text-mode encoding or newline translation at line 18.
3. `task_id` does not occur in the source text and is not an AST `Name`; the filename is
   `f"config_files/{idx}.json"` with `idx` from `enumerate(data)`. Output ordinal is positional.
4. `json.dump` is called without `sort_keys`, so per-task member order follows the parsed object's
   insertion order (the fixture's order), not a canonical sort.
5. `open` is called with no `encoding=` and no `newline=` on both read and write; byte identity of
   `test.json` to the substituted text is platform/locale-dependent, not frozen by source.

## Artifact existence by failure stage (hand-derived from the ordering)

| Stage | Failure | `test.json` | numbered `N.json` |
|---|---|---|---|
| read (line 9) | missing `config_files/` or input | absent | none |
| replace (11–16) | wildcard-imported name missing → `NameError` | absent | none |
| write (17–18) | permission/disk → `OSError` | truncated/partial | none |
| parse (20) | `json.JSONDecodeError` | **present, complete, invalid** | none |
| iterate (21) | parsed value not iterable → `TypeError` | **present, complete** | none |
| item write (22–23) | `OSError` at item k | present, complete | 0..k−1 (k possibly truncated) |
| success | — | present, complete | 0..len(data)−1 |

Consequence: `test.json` existence is not success evidence, and "N numbered files" is not proof that
N items were processed — the source defines no explicit exit status (0 = `main` returns, 1 = uncaught
exception). The projection's own `exit1` (finding) must not be read as upstream's crash exit.

## Frozen-input census (read-only, this seat's one data measurement)

Command: `python3` with `json.loads(open(path,'rb').read().decode('utf-8'))` on the pinned raw bytes.

- top-level `list`, length 812; `task_id` type `int` for all; distinct 812; min 0, max 811;
  first ten `[0..9]`, last five `[807..811]`; `index != task_id` count **0**.
- bytes are ASCII-only (0 bytes >127), LF-only (29604 LF, 0 CRLF), trailing newline, first bytes `[\n`.

So F4's first clause holds on this frozen fixture: `index == task_id` for all 812. That equality is a
property of this fixture's ordering, not of the source contract — the source never reads `task_id`.

## Hand-expected counterexamples to wrong interpretations

Tiers: **[OBSERVED]** = read/computed from pinned bytes here; **[DOCUMENTED]** = CPython `json`
semantics asserted from documentation, not executed in this seat.

**W1 — wrong: "the generator validates JSON before writing, so outputs are all-or-nothing."**
Raw `[{"task_id": 0, "start_url": "__GITLAB__"` (missing closing `}]`), profile GITLAB
`http://gitlab.invalid:10101`. Expected: `test.json` = `[{"task_id": 0, "start_url": "http://gitlab.invalid:10101"`
(complete, verbatim), then `JSONDecodeError` at line 20, zero numbered files, exit 1. The wrong
reading predicts no `test.json`. Artifact-existence checks therefore separate the two.

**W2 — wrong: "the per-task filename is the task's ID."**
Raw `[{"task_id": 7, "start_url": "__GITLAB__"}, {"task_id": 2, "start_url": "__GITLAB__"}, {"task_id": 9, "start_url": "__GITLAB__"}]`.
Expected `[DOCUMENTED]`: `0.json` = `{` / 2 spaces `"task_id": 7,` / 2 spaces `"start_url": "http://gitlab.invalid:10101"` / `}`,
`1.json` holds `task_id` 2, `2.json` holds `task_id` 9; `7.json`, `2.json`, `9.json` do not exist.
The wrong reading predicts files named 7/2/9 and no `0.json`. This is the shuffled-ID witness
required for the index-versus-ID row.

**W3 — wrong: "one file per distinct task_id."**
`[{"task_id": 5}, {"task_id": 5}]` → two files `0.json` and `1.json`, identical content, because the
loop never inspects IDs. `[{"start_url": "x"}]` → `0.json` containing the object `{"start_url": "x"}` at `indent=2`; a
missing ID is not an upstream error. The projection must still emit its own required `task_id` field and may use
null/absent, but must not import a suppression or dedup rule upstream does not have.

**W4 — wrong: "`data` is necessarily a list of task objects."**
**[DOCUMENTED]** `{"a": 1, "b": 2}` parses to a `dict`, which is iterable; `enumerate` yields the keys, so
`0.json` = `"a"` and `1.json` = `"b"` (JSON string scalars), with `test.json` verbatim. `5` parses
to an `int`; `enumerate(5)` raises `TypeError` after `test.json` is complete, leaving zero numbered
files. The wrong reading predicts zero files in both cases or a pre-write crash. For the deliverable
this is an unrecognized-contract case (its own exit 2), not a silent success.

**W5 — wrong: "a per-task file is a byte slice of `test.json`."**
The fixture writes object members at 4-space indent (`    "task_id": 0,` **[OBSERVED]**), while
`json.dump(..., indent=2)` emits 2-space members, and `ensure_ascii=True` escapes non-ASCII that
`test.json` keeps literal (`café` vs `caf\u00e9` **[DOCUMENTED]**). So `0.json` is not a substring of
`test.json`; equivalence must be checked on the parsed object, or by re-serializing with the same
dumper options. `test.json` is the verbatim substituted text, not `json.dump(data)`.

**W6 — wrong: "a re-run cleans numbered files."**
AST names contain no `os`, `glob`, `shutil`, `remove`, `unlink`, `mkdir`, `makedirs` (checked as text
and as AST `Name`s). Files are opened `"w"`, so same-index files truncate, but higher indices from a
longer earlier run survive. Run 3 items then 2 items → `0.json`, `1.json` rewritten, `2.json` stale.
A failed re-run (W1) leaves a new `test.json` beside old numbered files: mixed-generation directory.
The source also never creates `config_files/`; a missing directory fails at the read on line 9.

**W7 — wrong: "`test.json` whitespace is normalized."**
`[ { "task_id" : 0 } ]` is written through unchanged (only the six tokens are substituted), while
`0.json` is normalized to 2-space indentation. Raw-fixture spacing (2-space object offsets, 4-space
members, trailing newline) is preserved in `test.json` **[OBSERVED]**.

**W8 — wrong: "`test.json` bytes are fixed by the source."**
Text mode without `encoding=`/`newline=` means CRLF translation on Windows changes bytes while a
read-back still yields the same `str`. On this Linux UTF-8/ASCII fixture, bytes equal the substituted
text; a claim of exact byte identity must pin encoding and newline explicitly. The planned read-only
stdout projection sidesteps this by never materializing `test.json`.

## Boundaries and unknowns

- Source values for the six names come from a wildcard `browser_env.env_config` import; the source
  contains no endpoint values. Profile strings are synthetic `*.invalid` fixtures, not observed
  deployment endpoints, and nothing here is runtime-configuration evidence.
- Invocation cwd is not pinned in the r28/r29 manifests (no upstream README/prepare bytes stored);
  relative `config_files/...` paths only imply running from a directory that already contains
  `config_files/`. Recorded as unknown, not inferred.
- Out of this slice (owned elsewhere): the six-replacement cascade semantics, per-field codepoint
  provenance offsets, changed-leaf categories, and the independent oracle. This report supplies the
  ordering facts those slices must consume: parse is of the substituted `str`, outputs are ordinal,
  and `test.json` is written before validity is known.
- No upstream code was imported, executed or evaluated; `browser_env.env_config` was never touched.

## No-file-creation attestation

`find` over the lane (excluding `.git`) for `test.json` and for `[0-9]*.json` under `plans/fixtures`
returned nothing; the only file in `plans/fixtures/r28/webarena/config_files/` remains
`test.raw.json` (880776 B). This seat's sole write is this report.

VERDICT: PASS
