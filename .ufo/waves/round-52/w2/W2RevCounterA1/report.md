# W2RevCounterA1 — attack on Amendment A1 and the amended C1 per-test classifier

Seat: W2RevCounterA1 (reviewer, read-only, leaf). Scope: `classify_test()` / `split_tests()` in
`plans/round52_c1_grader_audit.py` against Amendment A1's frozen wording; the two hardened CONFIRMED
checks; the candidate gate. Nothing in the lane tree, the fleet repo or a sibling lane was edited.
No git or jj command was run. No tool was installed (stdlib Python 3.14 only).

Disclosure: this seat read the two graders A1 names and the full 89-task population (through the
counter and an AST shadow). It is an attacker, not a blind labelling reader.

## Verdict

- **Attack landed.** A1's per-test rule does not hold as implemented. The counter does not reproduce
  A1's own two motivating presence-only tests: `pytorch-model-recovery::test_model_file_exists` is
  classified P3 and `torch-tensor-parallelism::test_parallel_linear_exists` is classified P2. Both are
  P1 when judged on their own bodies.
- **Wording needs fixes** (W1–W10 below) before the after-run is scored. Most of the failures are
  mechanical (block boundaries, comments and strings scanned as code, decorators) and one is the
  vocabulary (`is not None` is not a comparison; `glob`/`listdir` are not presence).
- **The hardened CONFIRMED checks do not close the hole.** In a scratch fixture lane, two receipts
  with quotes `"assert"` and `"mp.spawn("` make `PREDICATE R52-C1-A5 pass`. The `CONFIRMED` leg
  does not require a P1 test, a quote of any length, or a quote inside a presence-only test.
- **The candidate gate is looser than A1's text.** `candidate = bool(p1) or cls in ("V1","V4")`
  admits two tasks with zero P1 tests. A1 defines a vacuity candidate as "≥1 of its tests is P1".

## Commands run

```
cd /fast/scratch/hyaku/kengaku-r52/w2-W2RevCounterA1
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c1_grader_audit.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
# (copied counter to scratch and imported it with sys.dont_write_bytecode=True; classify_tests() called on fixtures)
# AST shadow classifier + attribution over the 89 primary graders (python, in scratch; read-only on the lane)
# fixture lane under scratch/fixture-lane: plans/ copy + graders copy + fixture confirmations.json + fixture prior-art.md
python3 <scratch>/fixture-lane/plans/round52_c1_grader_audit.py --lane <scratch>/fixture-lane
```

Counter output on the lane as it stands (read-only run, exit 1):

```
TASKS total=89 records=89 classified=88
CAPTURES expected=184 present=183 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=31 V0=3
TESTCLASS presence_only_tests=33 tasks_with_presence_only=27
CANDIDATES total=29          (27 with >=1 P1 test + 2 V1-only: pytorch-model-recovery, torch-tensor-parallelism)
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
PREDICATE R52-C1 fail        (expected: 183/184 per A5; CONFIRMED=0 at this stage)
A5 CAPTURES present+pinned_excluded=184 of 184 ; A5 TASKS classified+excluded=89 of 89
PREDICATE R52-C1-A5 fail     (only leg 3 open; no confirmations yet)
```

The counter's `TESTCLASS presence_only_tests=33 tasks_with_presence_only=27` matches A4's corrected figure.

## Attack 1 — per-test classifier on fixtures (A1 frozen wording vs observed)

Fixtures: `receipts/fixtures/<case>/test_outputs.py`; observed classes: `receipts/fixtures/results.json`.
"Expected" is the class the A1 wording gives when read literally (block asserts, and once presence
calls are removed compares nothing). Where the wording is ambiguous, the cell says so.

| case | test | expected | observed | holds? |
|---|---|---|---|---|
| A exists + comparison, same block | `test_a_exists_and_compare` | P3 | P3 | yes |
| B presence-only test, next test decorated `@pytest.mark.parametrize("name", ["in.txt"])` | `test_c0_prev_presence` | P1 | **P3** | **no**: decorator of the next test is absorbed; `in` token |
| B parametrised presence-only test | `test_c_param_exists` | P1 | P1 | yes |
| C `if exists: assert True` | `test_c1_if_assert_true` | P1 | P1 | yes |
| C `if exists: assert read_text()=="x"` | `test_c2_if_compare` | P3 | P3 | yes |
| C `if not exists: raise AssertionError` | `test_c3_if_raise_presence` | P1 | **P0** | **no**: `"assert" not in block` → P0 |
| C `if read_text()!="x": raise AssertionError` | `test_c4_if_raise_compare` | P3 | **P0** | **no**: comparison hidden by the same guard |
| D helper defined before, called in block, helper compares | `test_d1_helper_before` | P1 literal / P3 intent | P1 | wording gap (block-local scope not stated) |
| D helper defined after, called in block, helper compares | `test_d2_helper_after` | P1 literal / P3 intent | P3 | right class, wrong reason (helper absorbed into block) |
| D presence-only, then module helper that compares, then next test | `test_d3_presence_then_module_helper` | P1 | **P3** | **no**: module helper between tests absorbed into previous block |
| D next test | `test_d4_next` | P1 | P1 | yes |
| E `def test_e1_annotated(p: Path) -> None:` presence-only | `test_e1_annotated` | P1 | **P3** | **no**: `>` of `->` matches VALUE |
| E presence-only with docstring "...exists in /app" | `test_e2_doc_in` | P1 | **P3** | **no**: `\bin\b` matches prose in docstring |
| F presence-only test followed by an `async def test_` that compares | `test_f0_presence` | P1 | **P3** | **no**: async test absorbed (`^def` split) |
| F presence-only method in a class | `test_f1_method_exists` | P1 | NOT SPLIT | **no**: no record at all |
| F `async def test_` compare | `test_f2_async_compare` | P3 | NOT SPLIT | **no**: no record at all |
| G `read_text().startswith("#!/bin")` | `test_g1_startswith` | P3 | **P0** | **no**: content read is not in the P3 vocabulary |
| G `exists() and read_text()` (truthiness only) | `test_g2_read_truthy` | P3 (label) / P1 (literal) | P1 | ambiguous; label says "content", text says "compares" |
| G `re.match(r"^ok", read_text())` | `test_g3_re_match` | P3 | **P0** | **no**: `re.` not in the P3 vocabulary |
| H presence-only, next test decorated `@pytest.mark.skipif(sys.version_info < (3,10), ...)` | `test_h1_presence_only` | P1 | **P3** | **no**: decorator absorbed; `<` matches VALUE |
| H compare | `test_h2_compare` | P3 | P3 | yes |
| I `exists() and stat().st_size > 0` | `test_i1_size` | ambiguous | P3 | ambiguous (size check counted as comparison) |

Answer to the item's question. A presence-only test that also compares something, in the same
block, is classified P3 (case A, yes). It is misclassified in five ways: the comparison sits in a
helper (D1, D3); the comparison is in a decorator or absorbed code (B, H, D3, F); the comparison is
only a raise (C4, hidden as P0); the "compare" is prose (E2, E1, and the population cases below).

Consistency. The split is not applied consistently across:
- **blocks**: a block is `^def test_…(` to the next `^def test_…(`, so it absorbs helpers, module
  code, `if __name__` blocks and the decorators of the following test (cases D2, D3, F0, H1);
- **decorators**: the decorator of test N+1 belongs to test N (B, H);
- **parametrised tests**: the same leak (B); the parameter values are never in the test's own block;
- **`if` guards**: asserts are counted under a guard (C1, C2), but `raise` under a guard is P0 (C3,
  C4). `assert` is a substring test, so `pytest.fail` or `raise` tests fall into P0.

## Attack 2 — population: counter vs an AST shadow reference

The AST shadow is my reference, not the frozen rule: a test is "presence" if it calls
`exists/is_file/is_dir/isfile/isdir`; "compare" if the AST has any `ast.Compare` (including `is`,
`is not`, `in`) or a call named `allclose/isclose/equal/array_equal/approx/startswith/endswith/
match/search/fullmatch/findall/assertEqual/assertNotEqual/assertIn/assert_*`; "read" if it calls
`read_text/read_bytes/open/load/loads/decode/strip/splitlines/stat/keys/len`; "behaviour" if it
calls `subprocess/system/popen/Popen/run/check_output/socket/get/post/urlopen/spawn/call/check_call`.
P1-shadow = presence, and none of compare/read/behaviour.

Result on the 89 primary graders (`sanitize-git-repo` skipped: capture absent by design):

```
AST test functions: 305 | counter split tests: 305      (no class-based or async tests in the population)
counter P1: 33 | AST-shadow P1: 56 | both: 32
counter-only P1: 1   (hf-model-inference::test_model_downloaded)
shadow-only P1: 24
```

Attribution of the 25 disagreements (each re-checked on the raw function text and the cleaned text):

- **14 — comment / docstring / annotation / string text breaks P1** (the cleaned function is P1, the raw
  function is not): circuit-fibsqrt::test_gates_file_exists; custom-memory-heap-crash::test_program_compiles_debug
  and ::test_program_compiles_release; extract-moves-from-video::test_solution_file_exists;
  financial-document-processor::test_summary_csv_exists; fix-code-vulnerability::test_report_file_exists_example;
  gcode-to-text::test_hello_file_exists; llm-inference-batching-scheduler::test_output_files_exist;
  pytorch-model-recovery::test_model_file_exists; sparql-university::test_sparql_file_exists;
  torch-pipeline-parallelism::test_pipeline_parallel_exists; torch-tensor-parallelism::test_parallel_linear_exists;
  video-processing::test_example_video_exists and ::test_test_video_exists.
  Example (pytorch-model-recovery, `tests/test_outputs.py` line 105): the comment
  `# Reference the directory the agent operated in (the WORKDIR in the Docker env)` contains `in`,
  so `\bin\b` in VALUE classifies the whole test P3.
- **9 — `in` / `>` token in an assert-message string or a loop, not a comparison**: build-pmars::test_debian_source_used
  and ::test_built_from_source (`"No pmars source directory found in `/app`..."`), cobol-modernization::test_required_files_exist
  and ::test_data_files_exist, headless-terminal::test_cancel_command (`> /app/cancel.txt` inside a shell string),
  merge-diff-arc-agi-task::test_git_repo_init and ::test_algo_py_exists, modernize-scientific-stack::test_dependency_file_exists,
  rstan-to-pystan::test_output_files_exist. VALUE scans the raw block including string literals.
- **1 — absorbed following code**: tune-mjcf::test_tuned_model_exists (16 non-blank lines of `simulate_model`
  absorbed; compare found there).
- **1 — counter-only false P1**: hf-model-inference::test_model_downloaded. The test does
  `assert os.path.exists(model_path)` and then calls `AutoModelForSequenceClassification.from_pretrained`
  and `AutoTokenizer.from_pretrained`, asserting `is not None`. VALUE has no `is`/`is not`, and BEHAV_T
  has no `from_pretrained`, so the counter calls it presence-only. The test does perform a real load.

Absorption across the population: 21 of the 305 test functions have non-blank following code inside
their block. The largest are torch-tensor-parallelism::test_parallel_linear_exists (123 lines: the
`_setup_process_group` and `_test_*_parallel_linear` helpers, plus decorators), torch-pipeline-parallelism::
test_no_hooks_in_pipeline_parallel (100), install-windows-3.11::test_qemu_running_with_correct_params (122).

Measurement of A1's own examples on their own bodies:
- `pytorch-model-recovery::test_model_file_exists`: counter P3; own body P1 (comment-only cause, above).
- `torch-tensor-parallelism::test_parallel_linear_exists`: counter P2 (the absorbed helpers contain
  `mp.spawn`, which BEHAV_T treats as behaviour); own body P1 (its docstring contains `in`).
- Both tasks therefore have `presence_only=-` in the counter's own output. They are candidates only
  through the file-level V1 class (see W8).

## Attack 3 — the hardened CONFIRMED checks (A1, Changed (stricter))

Fixture lane: `scratch/fixture-lane` (copy of `plans/round52-tasks.json`, the captured graders, the
knowledge entries, the counter; a fixture `prior-art.md` with three placeholder `example.invalid` URLs,
labelled FIXTURE ONLY and not evidence; and two fixture confirmations). Receipts:
`receipts/fixture-lane-confirmations.json`, `receipts/fixture-lane-run.txt`.

```
CONFIRMED new=2 ['pytorch-model-recovery', 'torch-tensor-parallelism']
PRIOR-ART ok=True urls=3
PREDICATE R52-C1 fail        (literal; only because present=183, per A5)
A5 CAPTURES present+pinned_excluded=184 of 184
A5 TASKS classified+excluded=89 of 89
PREDICATE R52-C1-A5 pass
```

Holes shown by this run:
- the verbatim-quote check is a substring test with no minimum length: `"assert"` passes;
- the quote need not lie in a presence-only test: `"mp.spawn("` lies in `test_column_parallel_linear`, a P2 test;
- the candidate gate is the union P1 ∪ {V1,V4} (see W8), so a task with zero P1 tests is accepted;
- the "independent second reader" is a non-empty string, not checked;
- `lane_read_tasks()` reads only the twelve `tb2-*-grader.md` entries. `bn-fit-modify`,
  `pytorch-model-recovery` and `torch-tensor-parallelism` were hand-read by the L1 after the freeze
  (A1's text) and have no knowledge entry, so they pass the "never read by this lane" guard. They are
  the very tasks A1 uses to motivate the amendment.

## Wording fixes (proposed as new amendment text; nothing edited)

- **W1 Block boundary.** `^def test_<name>(` to the next `^def test_` absorbs helpers, decorators of the
  next test and module code (D2, D3, F0, H1, 21 population tests). Define the block as the AST span of the
  function, decorators excluded, comments, docstrings and annotations excluded.
- **W2 "compares".** Enumerate the comparators. Count `is`, `is not`, `in`, `not in`, ordering, equality,
  and the named comparison calls. Do not scan comments, docstrings or string literals. Today `is not None`
  is not a comparison (hf-model-inference) and `"in"` in prose is (14 + 9 cases).
- **W3 "presence".** Enumerate the presence vocabulary. Either it is the five calls the counter uses, and
  then `glob`/`listdir`/`iterdir` non-empty checks (build-pmars) are P0 by definition, or it is extended.
- **W4 Precedence.** State it. Today P2 > P3 > P1 is implicit. A presence-only test that runs an
  unasserted `subprocess` is P2 under the counter, and A1's P1 text ("compares nothing") does not exclude it.
- **W5 Helper calls.** Either resolve same-module helpers transitively, or state that P1 is block-local and
  require the second reader to check the helpers called from a P1 test (D1 is P1 under the literal text).
- **W6 "asserts".** Change to "asserts or raises", so that presence-only tests written with `raise` or
  `pytest.fail` are P1 (C3) and comparisons written with `raise` are P3 (C4).
- **W7 Read without compare.** Decide whether a content read with no comparison is P1 (presence) or P3
  (the class label says "content/value"). Today `exists() and read_text()` is P1 (G2) and
  `read_text().startswith()` is P0 (G1); the same content read changes class with an unrelated presence call.
- **W8 Candidate definition.** A1 says a vacuity candidate is a task with ≥1 P1 test. The counter's candidate
  is P1 ∪ {file-level V1, V4}, which admits pytorch-model-recovery and torch-tensor-parallelism (2 of 29).
  Pick one definition and state it.
- **W9 CONFIRMED receipt.** Require the quote to (a) meet a minimum length, (b) lie inside a P1 test span of
  the same task, and (c) state how reader independence is recorded (not checkable by the counter; say so).
- **W10 Guard.** Exclude from "new" every task the lane hand-read in this round before the after-run
  (bn-fit-modify, pytorch-model-recovery, torch-tensor-parallelism), or state that the A1 observation
  does not count as a reading for the guard.

## Limits of this attack

- The AST shadow is my reference, not the frozen rule. Its disagreements are attributed, but its
  vocabulary (listed above) is my choice; the shadow P1 count (56) is not a claim.
- I did not test `unittest`-style `assertEqual`, `pytest.raises`, or `glob`-only presence beyond build-pmars.
- I did not run `--selftest`; it writes nothing and was not needed for the cases above.
- The counter, the lane and the scratch fixtures are unchanged. The fixture lane was scratch-only.

## Receipts (under this seat's report dir)

- `receipts/fixtures/<case>/test_outputs.py` (nine fixture cases A–I)
- `receipts/fixtures/results.json` (observed per-test classes and expectations)
- `receipts/fixture-lane-confirmations.json`, `receipts/fixture-lane-run.txt`
