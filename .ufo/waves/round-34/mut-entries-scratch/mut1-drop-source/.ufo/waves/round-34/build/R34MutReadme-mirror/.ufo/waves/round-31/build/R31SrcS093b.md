# R31SrcS093b — SWE-bench Pro V2 reward block (S093), pinned `66f92766`

Lane: kengaku round 31, leaf seat. Scope: the reward block of one `instance_internetarchive__openlibrary-*`
task's `tests/test.sh` and its `tests/parser.py`. No production edit was made; scratch is `/tmp/r31-R31SrcS093b/` (6.8 MB).
Tool installs: none.

## 0. Capture (observed)

Repo `scaleapi/SWE-bench_Pro-os`, commit `66f92766bba642462d4bbe5479e83f91f9211862`, access date **2026-10-25**.
Instance: `instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26`
(URL pattern `https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766…/v2/tasks/<instance>/tests/<file>`).

| file | bytes | lines | sha256 |
|---|---|---|---|
| `tests/test.sh` | 7864 | 234 | `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` |
| `tests/parser.py` | 4229 | 157 | `303ceda2c97816c27383b767baa9e2f28f8e9b0cebed4dd5d6159c6760770b66` |
| `tests/config.json` | 2447 | 4 | `5ccf4e7ea83fd6c1b2e6542b3ace8c49b2493f168d8d4e8948eb227b8cba4498` |
| `tests/run_script.sh` | 670 | 33 | `fb718e857bfa0f770097ed6a1278935ccb52c256db782f13b8e70ae9db4a5b9f` |
| `task.toml` | 889 | 41 | `b9c19d0309e910aa6acac8167ddac9c60f05aecb0d7abe1243c271c882393ad0` |

`config.json` holds `fail_to_pass` = 5 node ids, `pass_to_pass` = 15, `selected_test_files_to_run` =
`["openlibrary/plugins/importapi/tests/test_import_validator.py"]`; required set = 20 ids in one file.

## 1. (a) The reward computation, verbatim

The reward is one integer written by an `EXIT` trap from the script's own exit status — there is no other reward path:

- `test.sh:11` — `# Ensure reward file is always created, even on early exit`
- `test.sh:16` — `echo 1 > /logs/verifier/reward.txt`
- `test.sh:18` — `echo 0 > /logs/verifier/reward.txt`
- `test.sh:24` — `trap cleanup_and_reward EXIT`

The exit status that trap reads is the exit status of the evaluation heredoc, which is the whole grader:

- `test.sh:213` — `all_required = fail_to_pass | pass_to_pass`
- `test.sh:214` — `success = all_required <= passed_tests`
- `test.sh:221` — `print("\nRESULT: PASSED")` → `test.sh:222` `sys.exit(0)`
- `test.sh:225` — `missing = all_required - passed_tests` → `test.sh:228` `sys.exit(1)`
- `test.sh:234` — `exit "${EVAL_EXIT_CODE}"`

So the entire reward function is `reward = 1 iff (fail_to_pass ∪ pass_to_pass) ⊆ {name : status == "PASSED"}`,
evaluated over `/tmp/output.json` (`test.sh:175`) and `/tests/config.json` (`test.sh:179`). `task.toml:21` sets
`collect = []`, so this single scalar is the only verifier output; there is no per-test signal.

Two observations about the surrounding block:

- `test.sh:140` — `RUN_EXIT_CODE=$?` is assigned and **never read again** (grep over the file finds only that one
  occurrence). A pytest session that crashes after printing all required results still earns reward 1.
- `test.sh:165-166` read `fail_to_pass` / `pass_to_pass` into shell variables `FAIL_TO_PASS` / `PASS_TO_PASS` that
  are likewise never used: the heredoc re-reads `config.json` itself. Dead code, harmless.
- `test.sh:147` — `if [ ! -f /tmp/output.json ]; then` guards only *existence*; the parser's exit status is not
  checked. A stale `/tmp/output.json` left in a shared container is accepted if the parser dies before rewriting.

## 2. (b) How `fail_to_pass` and `pass_to_pass` are read

Read twice, from `/tests/config.json`, and the two readings are independent:

1. Shell side (`test.sh:165-166`) loads them as JSON text into unused variables.
2. The grader (`test.sh:183-184`) does `config.get('fail_to_pass', [])` / `config.get('pass_to_pass', [])`, then
   `parse_tests` (`test.sh:187`) accepts either a JSON string or a real list — `json.loads` first, `ast.literal_eval`
   as fallback "for strings with single quotes", `[]` on double failure. Both are then coerced to sets:
   `test.sh:203` `fail_to_pass = set(parse_tests(fail_to_pass_raw))` and `test.sh:204` for `pass_to_pass`.

In this instance both values are **JSON-encoded strings of lists**, so the `json.loads` branch is the live one; a
second sampled instance (`…03095f26…`) stores them single-quoted, exercising the `ast.literal_eval` branch. If a
value is neither, it silently becomes the empty set — an empty `fail_to_pass` makes the task pass vacuously.

`fail_to_pass` and `pass_to_pass` are treated identically at grading time: unioned at `test.sh:213`. The distinction
is documentary only; nothing checks that the `fail_to_pass` ids actually failed before the patch.

## 3. (c) `parser.py`: what counts as passing, and what happens to an unparseable name

- `parser.py:68` — `test_pattern = r'^([^\s]+\.py::[^\s]+)\s+(PASSED|FAILED|SKIPPED|ERROR)'`
- `parser.py:71` — `match = re.match(test_pattern, line.strip())` — anchored at the start of each **stripped** line.
- `parser.py:70` walks stdout, `parser.py:88-89` (`# Also check stderr for any additional test results`) walks stderr
  with the same pattern; both append (`parser.py:86`, `parser.py:105`).
- `parser.py:121` — `unique_results = {result.name: result for result in results}.values()` — dedupe by name,
  **last occurrence wins**.

A test "passes" only if a line, after leading whitespace is stripped, begins with `<path>.py::<id>` followed by
whitespace and the literal token `PASSED`; the grader then compares that name against the required set. `SKIPPED`,
`ERROR`, `FAILED`, `XFAIL`, `XPASS` and the `short test summary info` form (`FAILED path::test - …`, name not at line
start) are all non-passing for this variant.

A name it cannot parse produces **no record at all** — there is no `else` on `if match:` (`parser.py:72`), and the
`else: continue` at `parser.py:83-84` is unreachable because the regex alternation admits only the four tokens. The
line is silently dropped: no warning, no counter, no entry in `output.json`. Consequences:

- Fail-closed if the dropped name is required: absent ⇒ not in `passed_tests` ⇒ whole task fails (reward 0).
- Fail-open if the dropped line was a real `FAILED` for a name that also appears elsewhere as `PASSED`, because of
  the last-write-wins dedupe at `parser.py:121`.
- Structurally invisible: parametrized ids containing a space (`…::test_with space PASSED`), xdist-prefixed lines
  (`[gw0] [ 30%] path::test PASSED`), and collection-time `ERROR path::test` lines are all unparseable by this
  variant. Verified by execution (below).

`run_script.sh` supplies the log shape: `pytest "${test_files[@]}" -v --tb=short`, with
`PYTEST_XDIST_AUTO_NUM_WORKERS=4` exported (that variable alone does not enable xdist; no `-n` is passed).

## 4. Checks I ran (executed, not inferred)

Scratch copies only; `eval_body.py` is `test.sh:170-228` with the two literal paths substituted and nothing else.

1. `python3 parser.py` on a crafted log: `test_with space`, `[gw0]`-prefixed and `short test summary` lines produced
   no records; a bare `forged.py::test_x PASSED` on **stderr** produced a PASSED record. Confirmed.
2. A required test reported `FAILED` on stdout and the same name `PASSED` on stderr ⇒ `output.json` holds a single
   record for that name with status `PASSED` (`parser.py:121`), and the real grader logic printed
   `Required tests: 20 / Passed tests: 20 / RESULT: PASSED`, exit 0.
3. Full forgery from **stdout only**: all 20 required ids printed as `FAILED` by `-v`, then a failing test's
   *captured stdout* section printing each required id followed by ` PASSED`. The 8-space indentation is removed by
   `line.strip()` (`parser.py:71`); the injected records come later and win at `parser.py:121`.
   Result: `records 20 Counter({'PASSED': 20})`, grader printed `RESULT: PASSED`, exit 0 — **reward 1 with every
   required test failing**.
4. Collateral damage is invisible: 20 required `PASSED` plus 500 unrelated `FAILED` ⇒ `RESULT: PASSED`, exit 0.
5. One required id absent, or one required id `SKIPPED` ⇒ `RESULT: FAILED`, exit 1 (fail-closed on both).

## 5. Population check — one reward rule, many parsers

- `tests/test.sh` is a **single shared file**, not per-task: 9 of 10 sampled instances across 7 repositories
  (`openlibrary` ×3, `NodeBB`, `ansible`, `flipt`, `qutebrowser`, `tutanota`, `vuls`) hash to
  `b6f26ee…`. The one exception, `instance_gravitational__teleport-005dcb16…` (8024 B), differs by exactly two
  inserted lines (`apt-get … linux-libc-dev libudev-dev`) above `set -uo pipefail`; `diff` shows the reward block and
  the grader identical. The reward rule is therefore benchmark-wide, not per-task.
- `tests/parser.py` is **per-instance**. All 82 openlibrary tasks fetched: **21 distinct sha256** variants
  (largest cluster 15). Every one of the 82 scans stderr, and every one uses the same last-write-wins
  `{result.name: result …}` dedupe. The variants differ in strictness: **13 of 82** use the strict anchored
  `re.match(line.strip())` form (the target instance's `303ceda…` among them); the other 69 parse with
  `re.findall`/`re.finditer` over concatenated stdout+stderr, several adding a second
  `(FAILED|PASSED|…)\s+(path::test)` summary pass, and one (`86c163ab…`, 4 tasks) requires *two*
  `::` separators (`[^:\s]+\.py::[^:\s]+::[^:\s]+`) so it cannot match the module-level function ids that this
  instance's own config uses. Nothing in the repository cross-checks parser and config: a parser/config mismatch is
  a silent reward-0.

## 6. What the grader is, and what it cannot detect

**The grader is set containment**: a binary check that the union of `fail_to_pass` and `pass_to_pass` is a subset of
the set of names the parser recorded as `PASSED` (`test.sh:213-214`) — 100 % of the required ids, no threshold, no
partial credit, no weighting, and no look at anything outside that set.

What a grader of that shape cannot detect, in one sentence: it cannot distinguish a `PASSED` token emitted by pytest
from one emitted by the code under test — the evidence is a regex over a log the tested code writes into, deduped
last-write-wins (`parser.py:71`, `parser.py:89`, `parser.py:121`) — and it cannot see damage outside the declared
set, so a submission that breaks the rest of the suite, or whose runner crashes after the required lines are
printed (`test.sh:140` unused), still earns reward 1.

## 7. Bearing on the C1 entry (`benchmark-verifier-execution-model.md`, S093 row)

Additions the entry currently lacks, all citable at the pinned commit:

1. **Grader shape is now nameable.** The entry says nothing about how S093 converts a run into a score. It is
   containment, binary, single-scalar (`test.sh:213-214`, `test.sh:16/18`, `task.toml:21` `collect = []`).
2. **A second, in-repo protection the entry does not record.** Beyond Harbor's tests-directory re-upload, S093's own
   `test.sh` re-materialises the test surface inside the container before running: `git checkout HEAD` for tracked
   test code (`test.sh:71`, `test.sh:89`), `rm -f` for untracked test code (`test.sh:72`), then
   `git apply --verbose /tests/test_patch.patch` (`test.sh:108`). So "the agent's edits to the test files are
   overwritten" holds for S093 twice over.
3. **A correction to the entry's "the fixtures, the data — are not overwritten".** For S093 that is only partly true:
   any path in `git diff --name-only HEAD` matching `*testdata/*|*test_data/*|*fixtures/*|*fixture/*|*mocks/*|*mock/*|*__snapshots__/*`
   is reset with `git checkout HEAD -- "$p"` (`test.sh:97-104`). Fixture data *is* reverted; the source tree and
   non-fixture data are not. (The `grep -qE '(__NONE__)'` guard at `test.sh:101` is a no-op placeholder.)
4. **The sharpest support for the entry's thesis, and a caveat on it.** Shared mode matters concretely here because
   the reward evidence is a log that agent-modified code writes into: I produced reward 1 with all 20 required tests
   failing (§4.3). The entry's "what the framework guarantees anyway" should therefore not be read as "the reward is
   evidence-independent" — for S093 it is evidence-*adjacent*.
5. **Nuance for the S092 (Harbor) seat, flagged not resolved here.** `task.toml:23-24` contains an **empty**
   `[verifier.env]` table. Harbor's rule is "defaults to 'separate' if a verifier 'environment' is set, otherwise
   'shared'", so whether an empty-but-present `[verifier.env]` counts as "set" decides the effective mode for this
   task. The entry's table records `[environment]` (the top-level one, `task.toml:29-30`) and asserts shared; that
   assertion should be confirmed against `VerifierConfig` in Harbor at `6099b8cf`, not against the TOML alone.

## 8. Remaining unknowns

- Whether pytest-xdist is installed in the image and whether openlibrary's `addopts` passes `-n`: if so, `[gwN]`
  prefixes would make every line unparseable for the target variant and pin reward at 0. Not observable from the
  repository at the pinned commit (image-provided config).
- The 21 parser variants were clustered, not read line by line; the per-variant statements in §5 are for the target
  variant and, for the others, for the features their bytes exhibit.
- Only 10 `test.sh` files were sampled; "single shared file" is a 9/10 observation (teleport differs by a 2-line
  environment fix outside the reward block), not a 642-task census.

VERDICT: S093's reward is binary set containment (`test.sh:213-214`) over a log-derived, last-write-wins, agent-writable PASSED set (`parser.py:71/89/121`) — the entry may record "grader = set containment, not a threshold", but MUST NOT present it as evidence-independent, since I reproduced reward 1 with all 20 required tests failing.
