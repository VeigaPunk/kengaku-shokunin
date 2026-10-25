# R31SrcS093a — SWE-bench Pro V2 `tests/test.sh` execution model (S093)

Scout seat, round 31, lane `kengaku-shokunin`. Read-only source evidence; no production edits.
Pinned revision for every fetch: `scaleapi/SWE-bench_Pro-os@66f92766bba642462d4bbe5479e83f91f9211862`.
Access date: **2026-10-25**. No clone performed; per-file `curl` only.

## Captures (all under `/tmp/r31-R31SrcS093a/`)

| file | source URL | sha256 | bytes |
|---|---|---|---|
| `contents.json` | `api.github.com/repos/scaleapi/SWE-bench_Pro-os/contents/v2/tasks?ref=66f92766…` (HTTP 200) | `fa0acffb604e80dbb40fe96d43586356fb6b4ce2af885b7045ba2fc8a9e233a1` | 956505 |
| `tests-contents.json` | `…/contents/v2/tasks/<task>/tests?ref=66f92766…` (HTTP 200) | `fd4c9c1825ae7434589c198acf666d8bf0a553d932e0f20a08d3580ebd080f8f` | 9459 |
| `test.sh` | `raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766…/v2/tasks/<task>/tests/test.sh` (HTTP 200) | `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` | 7864 |
| `run_script.sh` | same dir (HTTP 200) | `fb718e857bfa0f770097ed6a1278935ccb52c256db782f13b8e70ae9db4a5b9f` | 670 |
| `config.json` | same dir (HTTP 200) | `5ccf4e7ea83fd6c1b2e6542b3ace8c49b2493f168d8d4e8948eb227b8cba4498` | 2447 |
| `xcheck-test.sh` | second openlibrary task, same path (HTTP 200) | `b6f26eec…976d0` (byte-identical) | 7864 |

Task chosen: `instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26`
(82 `instance_internetarchive__openlibrary-*` tasks of 642 in the `v2/tasks` listing).
Enumerated `tests/` holds 5 files: `config.json` (2447), `parser.py` (4229), `run_script.sh` (670),
`test.sh` (7864), `test_patch.patch` (2355). `test.sh` is 234 lines.

Test surface for this task (`config.json`): `selected_test_files_to_run` =
`["openlibrary/plugins/importapi/tests/test_import_validator.py"]`; `fail_to_pass` is a
JSON-encoded **string** (575 B, hence the `isinstance(test_files_raw, str)` branch at `test.sh:121-122`).

## (a) The test-space reset block

Three stages, lines 29-105, all inside the task script after `cd /app` (`test.sh:27`).

**Stage 0 — caches and git lock (`test.sh:29-32`)**

```
29:find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
30:find . -name '*.pyc' -delete 2>/dev/null || true
32:rm -f .git/index.lock 2>/dev/null || true
```

**Stage 1 — test-code surface vs `HEAD` (`test.sh:33-74`)** — intent declared at line 33:
`echo "Resetting test-space to base state (full test-code surface)..."`.

An inline `PYRESET` Python heredoc (`test.sh:34-66`) classifies paths with two literal sets
(`test.sh:37-38`): `CODE_DIRS = {'tests', 'test', '__tests__', 'spec', 'specs'}` and
`DATA_DIRS = {'testdata', 'test_data', 'fixtures', 'fixture', 'mocks', 'mock', '__snapshots__'}`.
A path under any `DATA_DIRS` segment is **not** test code (`test.sh:43-44`:
`if any(s in DATA_DIRS for s in parents):` / `return False`), which takes precedence over the
`CODE_DIRS` match at `test.sh:45`. It then emits one `kind path` line per candidate from two git
queries — `for p in git(['ls-files']):` (`test.sh:60`, kind `T`) and
`for p in git(['ls-files', '--others', '--exclude-standard']):` (`test.sh:63`, kind `U`).

The driver loop (`test.sh:68-74`) then does exactly two things:

```
71:        T) git checkout HEAD -- "$path" 2>/dev/null || true ;;
72:        U) rm -f -- "$path" 2>/dev/null || true ;;
```

i.e. **tracked** test-code files are restored *from the container's own git `HEAD`*; **untracked**
test-code files are deleted. Source of truth is the image's object store, not a harness upload.

**Stage 2 — the test patch's own file set (`test.sh:77-105`)**

- Files the patch creates are pre-deleted so `git apply` cannot collide (`test.sh:77-79`:
  `grep -E '^--- /dev/null' -A1 /tests/test_patch.patch | grep -E '^\+\+\+ b/' …` then
  `[ -n "$p" ] && rm -f -- "$p" 2>/dev/null || true`).
- Union of every path the patch touches, plus renames, into `/tmp/v5_paths.txt` (`test.sh:81-82`);
  the patch-created subset into `/tmp/v5_created.txt` (`test.sh:83-85`).
- Per path: tracked → `git checkout HEAD -- "$p"` (`test.sh:89`); else if patch-created →
  `rm -f -- "$p"` (`test.sh:90-91`). Everything else is deliberately kept, per the in-file comment
  `# untracked files the patch merely MODIFIES are left alone (image-provided context)` (`test.sh:93`).
- Finally every **modified-vs-`HEAD`** file whose path contains a data directory is restored
  (`test.sh:97-105`), selector at `test.sh:100`:
  `*testdata/*|*test_data/*|*fixtures/*|*fixture/*|*mocks/*|*mock/*|*__snapshots__/*)` →
  `git checkout HEAD -- "$p" 2>/dev/null || true ;;` (`test.sh:102`).

**Stage 3 — re-apply the gold patch (`test.sh:106-108`)**

```
107:echo "Applying test patch..."
108:git apply --verbose /tests/test_patch.patch || { echo "ERROR: Failed to apply test patch"; exit 1; }
```

Net: the reset *deletes* untracked test-code files and patch-created files, and *restores* tracked
test-code and test-data files from git `HEAD` of the working tree at `/app` (fallback `/testbed`).

## (b) Whose reset is it — harness re-upload or the task's own script?

**The task's own script.** Every restore in the block is a local `git checkout HEAD -- <path>`
(`test.sh:71, 89, 102`) or a local `rm -f` (`test.sh:72, 91`); no stage copies a test tree in from
`/tests/`, and nothing in `test.sh` writes into the repo except the patch application at `test.sh:108`.
The harness contributes exactly four mounted inputs read by absolute path — `/tests/test_patch.patch`
(`test.sh:77-85, 108`), `/tests/config.json` (`test.sh:118, 165-166, 179`), `/tests/run_script.sh`
(`test.sh:136, 138`), `/tests/parser.py` (`test.sh:144`) — and `run_script.sh` itself runs
`pytest` in place (`run_script.sh:10, 19`: `pytest . --ignore=infogami …`, `pytest "${test_files[@]}" -v`).
So re-uploading tests is **not** a precondition of this reset; the gold *patch* is, and it is applied
after the reset, not instead of it.

Bounds on that statement, from the same bytes:

- The restore target is `HEAD`, not a pinned base commit. If an agent committed its own test edits, the
  reset would faithfully restore *those*. Correctness therefore rests on the image shipping the base
  commit as `HEAD` and on agent edits staying uncommitted — **[INFERENCE]**, not stated in `test.sh`.
- The v6 selector guard at `test.sh:101`, `echo "$p" | grep -qE '(__NONE__)' && continue`, can never
  match a real path, so the `continue` is dead and *every* listed test-data path is restored.
- Untracked files under `DATA_DIRS` are never deleted: `is_test_code` returns `False` for them at
  `test.sh:43-44`, and the v6 block only walks `git diff --name-only HEAD` (`test.sh:97`), which
  excludes untracked files. Fixture-side residue from an agent is not cleared by this block.
- The reset is not total for non-test code: application-source edits are only ever applied, never
  reverted, by `test.sh` — consistent with the agent's patch being the thing under test.

## (c) The `find … -prune -exec rm -rf` cache lines

**There is exactly one such line in this `test.sh`, not two** (`grep -c 'prune' test.sh` → `1`;
`grep -n 'rm -rf' test.sh` → line 29 only):

```
29:find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
```

Its companion cache-clearing line is the `-delete` form, not a second prune:

```
30:find . -name '*.pyc' -delete 2>/dev/null || true
```

The premise "two `find … -prune -exec rm -rf` lines" is **not satisfied at this revision** for this
task. It is not a per-task sampling artefact either: the second openlibrary task sampled
(`…-03095f26…-v8717e18…`) returns a byte-identical `test.sh`
(`cmp` clean, sha256 `b6f26eec…976d0`), so any task sharing these bytes has one prune line.
Whether some *other* task family under `v2/tasks` carries a second prune line is **unresolved** —
not sampled, and out of this seat's assigned scope.

## Confidence and remaining unknowns

- Observed, high confidence (verbatim bytes at the pinned commit, line-numbered above): reset stages,
  restore sources, patch application order, one prune line, the dead `(__NONE__)` guard, the mounted
  `/tests/` inputs, the single-file test surface.
- [INFERENCE]: `HEAD` == base commit in the shipped image; agent edits are uncommitted in practice.
- Unresolved: contents of `test_patch.patch` (not fetched — only its size, 2355 B, and its role);
  whether any non-openlibrary task family has two prune lines; whether the image's `/app` `.git`
  retains full history (only affects whether `HEAD` is reachable, not the reset logic).

VERDICT: PASS — reset is task-local (`git checkout HEAD` + `rm -f`, gold patch re-applied from `/tests/`), not a harness re-upload; the "two prune lines" premise is FALSE at 66f92766 (one `-prune -exec rm -rf` at `test.sh:29`, plus a `-delete` at `test.sh:30`, identical bytes across the openlibrary family).
