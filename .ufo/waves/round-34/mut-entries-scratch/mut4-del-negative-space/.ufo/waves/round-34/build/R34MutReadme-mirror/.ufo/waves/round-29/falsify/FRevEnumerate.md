writer: KengakuR29-2.FRevEnumerate-2
item: FRevEnumerate — upstream enumerate-index output naming and consumers of config_files/<n>.json at pinned revision
date: 2026-10-21
scope: static source reading only; no upstream code executed; round 29 only

# Godspeed axes

1. Naming rationale — why upstream names outputs by enumerate index.
2. Consumer census — every consumer of `config_files/<n>.json` at revision dce04686a56253aefba7b18a4fa0937cf1dc987b.
3. Identity assumption — whether any consumer assumes file index == task_id, and what breaks if it fails.
4. Artifact cross-check — round-29 prereg/draft/source-row statements vs the pinned upstream bytes.

# Attack

Downloaded all 88 tracked blobs of web-arena-x/webarena at the pinned commit into my scratch
(`.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/`, tree from GitHub API
`git/trees/dce04686a56253aefba7b18a4fa0937cf1dc987b?recursive=1`, `truncated: False`, 88 blobs), then
grepped them for `config_files`, `task_id`, `test.json`, `[Result]`, `range(812)`, `run_batch`. Byte
identity of the two manifest-pinned inputs verified after download:

- `src/scripts/generate_test_data.py` sha256 `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` = manifest value.
- `src/config_files/test.raw.json` sha256 `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` = manifest value.
- `src/README.md` sha256 `081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287` = S072 row's recorded value.
- `src/prepare.sh` sha256 `97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2`, 120 bytes = S073 row's recorded values.

All quotes below are from those pinned-byte copies; word counts were computed programmatically
(`len(quote.split())`), values in parentheses.

# Producer — why outputs are named by enumerate index

`scripts/generate_test_data.py` (838 bytes, pin verified):

- line 19: `# split to multiple files` (5 words)
- line 21: `for idx, item in enumerate(data):` (5 words)
- line 22: `with open(f"config_files/{idx}.json", "w") as f:` (5 words)

The loop variable is the list position; the string `task_id` occurs 0 times in this file (programmatic
grep count over the pinned bytes). Line 20 (`data = json.loads(raw)`) parses after the whole projected
text is written (lines 11–17), so filenames are positions in parse order of the same text the aggregate
`config_files/test.json` (line 17: `with open("config_files/test.json", "w") as f:` (5 words)) received.

What makes positional names useful — the consumer side:

- `run.py:142-143` — `parser.add_argument("--test_start_idx", type=int, default=0)` (3 words) /
  `parser.add_argument("--test_end_idx", type=int, default=1000)` (3 words); `run.py:422-423` —
  `for i in range(st_idx, ed_idx):` + `test_file_list.append(f"config_files/{i}.json")` (1 word):
  file address == loop position enables integer-range slicing.
- `parallel_run.sh:38` — `until python run.py --test_start_idx $2 --test_end_idx $3` (7 words) with
  `parallel_run.sh:71-73` — `run_batch 0 100 200 300 380` … `run_batch 770 812` (3 words for :73):
  the shipped parallelization batches by position ranges 0–812.
- `run.py:393-403` (`get_unfinished`) keys resume dedup on the filename stem: line 396
  `os.path.basename(f).split(".")[0].split("_")[1] for f in result_files` (5 words), line 400
  `task_id = os.path.basename(config_file).split(".")[0]` (3 words), line 401
  `if task_id not in task_ids:` (5 words).
- `run.py:341` — `logger.info(f"[Result] (PASS) {config_file}")` (3 words): result logs carry the
  filename (index), which downstream parsers turn back into an "example id".

[INFERENCE] No upstream file read (README.md, prepare.sh, generate_test_data.py, minimal_example.py —
all read in full) states a rationale. The naming exists so that file address equals loop position for
range slicing (`--test_start_idx/--test_end_idx`), shipped parallel batching, and filename-keyed
resume/log analytics; equality of that position with `task_id` is incidental to the raw file happening
to be task_id-ordered.

# Consumer census of config_files/<n>.json (pinned revision, 88 blobs grepped)

| consumer | location | what it consumes |
|---|---|---|
| run.py | :422-423 | builds `config_files/{i}.json` list from `range(test_start_idx, test_end_idx)` |
| run.py | :393-403 | resume dedup keyed on filename stem |
| run.py | :244-247, :253 | opens each file; reads content `intent`, `task_id` (`task_id = _c["task_id"]` (3 words)) |
| run.py | :346-347 | trace zip named by content task_id: `Path(args.result_dir) / "traces" / f"{task_id}.zip"` (5 words) |
| browser_env/helper_functions.py RenderHelper | :125, :129-131 | render file named by content task_id: `task_id = _config["task_id"]` (3 words), `Path(result_dir) / f"render_{task_id}.html", "a+"` (4 words) |
| minimal_example.py | :58, :61 | `assert os.path.exists("config_files/0.json")` (2 words); opens 0.json, asserts SHOPPING_ADMIN in `start_url` |
| minimal_example.py | :97-98 | `# example 156 as an example` + `config_file = "config_files/156.json"` (3 words) — positional addressing |
| README.md | :66, :99-101 | walkthrough `config_file = "config_files/0.json"` (3 words); generation step; line 101: "You will see `*.json` files generated in [config_files](./config_files) folder. Each file contains the configuration for one test example." (18 words) |
| parallel_run.sh | :38, :71-73 | positional ranges feeding run.py |
| .gitignore | :149-159 | ignores `config_files/*0.json` … `*9.json` (line 149: `config_files/*0.json` (1 word)) and line 159 `config_files*/test.json` (1 word) — generated artifacts |
| tests/ | none | `tests/` has no consumer of `config_files/<n>.json`; only `tests/test_browser_env/test_auth_cookie.py:34,58` reset a self-written `/tmp/config.json` (`env.reset(options={"config_file": "/tmp/config.json"})` (2 words)); `tests/conftest.py` defines env fixtures only |
| aggregate test.json | writer only | written at generate_test_data.py:17-18; 0 readers among the 88 blobs (programmatic grep `test\.json`) |

Content consumers that never touch the filename: `browser_env/envs.py` reset and
`evaluation_harness` evaluators receive the (possibly rewritten temp) path from run.py and read content.

# Does any consumer assume file index == task_id? Yes — three, plus one positional hardcode

1. **run.py `get_unfinished`** (`run.py:393-403`). Resume keys are the filename stem (`run.py:400`),
   compared against ids parsed from result HTMLs named by the CONTENT task_id
   (`browser_env/helper_functions.py:125,130`). The two identities are equated only while
   enumerate index == task_id. On a reordered raw file every config is "unfinished" forever (its stem
   never appears in result names) — completed work silently reruns; no error is raised.
2. **scripts/html2json.py**. `results` is keyed by the FILENAME index parsed from run.py's
   `[Result]` log lines (line 42: `id = line.strip().split(".")[-2].split("/")[-1]` (3 words), line 43
   `results[int(id)] = ...`), while `data_configs` is keyed by CONTENT task_id from test.raw.json
   (line 18: `data_configs = {int(item["task_id"]): item for item in data_configs}` (8 words)) and the
   render filename yields the content task_id (line 50: `task_id = int(render_file.split("_")[-1].split(".")[0])`
   (3 words)). Join at line 108: `"success": results.get(task_id, False),` (3 words) — under a reorder,
   success flags attach to the wrong examples (filename key vs content key).
3. **scripts/check_error_runs.py**. Error recovery maps the `[Config file]` filename stem to a render
   file: line 95 `example_idx = line.split("/")[-1].split(".")[0]` (3 words) → line 97
   `error_examples.append(int(example_idx))` → line 107/108 `os.path.exists(f"{args.result_folder}/render_{idx}.html")`
   + delete. Render files are content-task_id-named, so under a reorder this deletes the wrong render
   file. Additionally lines 62 (`for i in range(812):` (4 words)) and 78-79
   (`i for i in range(0, 812) if str(i) not in merged_results` (11 words)) hardcode the positional
   identity range.

Static check on the pinned raw bytes (my script, read-only): 812 items, `index != task_id` count **0**,
812 distinct ids — the assumption holds exactly on the frozen input, matching the draft's
"output ordinal == task_id 812/812" and prereg forecast F4.

# Mismatches (exact location and value)

- **M1 — upstream default range overruns the population.** `run.py:143` default
  `--test_end_idx` = 1000 vs 812 generated files (indices 0..811): `range(0, 1000)` requests
  `config_files/812.json` … `config_files/999.json` — 188 nonexistent paths. With the default
  `--result_dir` "" (`run.py:146`) the debug guard `run.py:424` does not filter, `get_unfinished`
  keeps all 1000, and each phantom file fails in `test()`, logged at `run.py:353`
  (`logger.info(f"[Unhandled Error] {repr(e)}]")` (2 words)). Harmless in the documented flows
  (README uses 0/1; parallel_run.sh passes explicit bounds ≤812) but it is a real index-space vs
  population mismatch baked into positional naming. Upstream observation only; nothing in round-29
  artifacts asserts otherwise.
- **M2-M4 — latent identity mismatches** (run.py:400 vs helper_functions.py:130; html2json.py:42-43 vs
  :18/:50/:108; check_error_runs.py:95→107): all reduce to "filename index == content task_id", true
  for the pinned order, silently false under any raw reordering. These are exactly the failure modes
  the round's shuffled-ID hand witness (`corpus/evidence/round29-calibration/mutation-witness.txt`:
  `index_by_task_id selftest exit 1 killed AssertionError`, exit=0 overall) demonstrates offline.
- **No mismatch found against round-29 artifacts on my scope.** S070's located ranges
  (main 8–23, replacements 11–16, parse 20, enumerate-index 21–23) verified against my pinned-byte
  copy line-for-line; S072/S073 sha256 values match my downloads; README documents no replacement
  order and its env export order (README.md:86-92: SHOPPING, SHOPPING_ADMIN, REDDIT, GITLAB, MAP,
  WIKIPEDIA, HOMEPAGE) differs from the generator's replacement order (generate_test_data.py:11-16:
  GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP), which is what S072/draft already state;
  prepare.sh (6 lines, 120 bytes) contains no generator call, confirming S073.

# Instrument cross-check (read-only runs only)

`python3 plans/config_projection.py --summary` exit 0; `--json` exit 0, `findings` 0.
`--json` reports `index_mapping = {index_equals_task_id: 812, output_index_rule: "enumerate position",
violations: []}` and `population` 812/812/3/2436 with token occurrences 385/336/281/300/0/133 —
consistent with my independent reading of the upstream bytes and my static index check.
The consumer-side evidence above (run.py resume + html2json join + check_error_runs) is upstream
corroboration that the round's `output_index_rule` name ("enumerate position") is the actual upstream
mechanism, and that the draft's operational rule "(3) compare per-task filenames with `task_id`
whenever the raw order may differ" targets a real upstream assumption, not a hypothetical.

# Independence and tooling

- I did NOT read or import `plans/config_projection.py` source; I only executed it read-only
  (`--summary`, `--json`) and compared its output. [INFERENCE] none of my verdicts depend on its code.
- Tooling: nothing installed or upgraded (host pacman transactions paused; preexisting curl and
  python3 used for static download/grep/counting only). No linters/formatters run.

# Evidence files (scratch)

`.ufo/waves/round-29/scratch/falsify/FRevEnumerate/`: `src/` (88 pinned blobs), `tree.json`,
`paths.txt`, `instrument-summary.txt`, `instrument-json.txt`. Commands and outputs quoted inline above.

VERDICT: PASS
