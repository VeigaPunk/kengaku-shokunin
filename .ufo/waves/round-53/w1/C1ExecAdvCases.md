# C1ExecAdvCases — adversarial case set for the presence-only spec (round 53, wave 1)

Seat: executor `C1ExecAdvCases`. Blindness: I did not read, run or list anything under `C1ExecClassifier*`, any
`C1Label*` directory, or `plans/round53_c1_classify.py`. `expected` was derived by reading
`.ufo/waves/round-53/p1-spec.md` (and the frozen claims file) only. No classifier output was consulted. No tools installed.

## Files (absolute)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ExecAdvCases/cases.json` — 90 modules, 371 tests (175 `P1`, 196 `P0`)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ExecAdvCases/ambiguous.json` — 47 spec-silent modules, each with `reading_a` / `reading_b`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ExecAdvCases/check.py` — scorer
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ExecAdvCases/build_cases.py` — source of both JSON files (only `ast.parse` is used, to check syntax)

Format: `cases.json` = list of `{"id","source","expected"}` (`expected` = `{"test_x":"P1"|"P0","Class.test_y":...}`); two cases also carry
`must_not_include` (keys the classifier must not report: nested `test_inner`, non-`test_` names such as `tests_not_a_test`,
`testnounderscore`). Every module carries a common header (`os, glob, json, subprocess, Path, pytest`, `OUT`, `D`) unless stated;
the unused imports are deliberate (imports of `subprocess`/`json` must not change the class).

## Commands run
```
python3 build_cases.py      # cases=90 tests=371 ambiguous=47
python3 check.py <stub>     # stub = every test_* -> P0, in /fast/scratch only; proves plumbing: 175 test_fail = exactly the 175 P1 expectations
python3 (inline)            # ast-only check: expected keys == the set of test_*/Class.test_* defs in every case (0 mismatches)
rm -rf /fast/scratch/hyaku/kengaku-r53/C1ExecAdvCases
```
Usage for the L1: `python3 check.py plans/round53_c1_classify.py` (exit 0 iff every case passes; per-case pass/FAIL, per-clause totals,
unannotated `extra` keys, and an informational ambiguous section saying whether the classifier follows reading A or B).
I did **not** run `check.py` on any real classifier.

## Case counts per clause (id prefix → coverage)
| prefix | covers | cases | tests |
|---|---|---|---|
| `ex-` | the 8 worked examples one per module + all 8 in one module | 9 | 16 |
| `cl1-` | clause 1 (an assertion must be reachable): zero-assertion forms (pass, docstring, bare expr, `return exists`, commented/stringified assert, print, `...`), helper without assert, unconditional `pytest.fail`/`raise AssertionError`/`pytest.skip`, decorators, non-test names, vacuous second assert, path-less asserts | 8 | 23 |
| `cl2-` | clause 2 (existence/type only): pathlib & `os.path` forms, from-imports/aliases, `os.access(F_OK)`, listing membership (`listdir`/`iterdir`/`scandir`), glob non-empty vs counts, `and`/`or`, `assert exists or other_exists`, `== True`/`is True`/`bool()`, variable indirection, messages containing `in`/`==`/`%`, string-built paths, read-after/before ordering, `open` for write vs read, polling loops | 16 | 100 |
| `cl2n-` | look-alikes that are not existence: size/mtime/mode/`access(X_OK)`, computed value compares (`resolve()==`, `readlink==`, `len`, `.name==`) | 2 | 16 |
| `cl3-` | clause 3: subprocess in 10 spellings (alias, from-import, `__import__`, `os.system`, `os.popen`), 18 content readers, deliverable import+call vs import-only, network, value/process-state asserts | 5 | 42 |
| `reach-` | helpers depth 1–3 (clean and polluted at depth 3), mutual recursion (2- and 3-cycle, clean and dirty), self recursion, helper with own assert, uncalled helper, per-test attribution in one module, name-lies/shadowed `exists`/`is_file`, inner/lambda helpers, fixtures (clean, dirty, chain depth 3, yield, scope, params, in class), parametrize | 19 | 59 |
| `cls-` | class tests: plain/`Checks` class, same name at module and class level, `self.` helpers depth 2, `@staticmethod`, class attribute path, self-vs-module helper shadow, module helper from class, sibling-method pollution | 6 | 20 |
| `unittest-` | `assertTrue/assertIn` existence, content assertions (`assertEqual/Regex/CountEqual/Greater/AlmostEqual`), no-assert tests (`skipTest`), helper methods, classmethod helpers, module-level + class mix | 6 | 31 |
| `fail-` | `pytest.fail` / `raise AssertionError` in conditionals on existence vs content/size/returncode/count, in loops/else/elif, mixed with `assert`, via helpers | 4 | 17 |
| `code-` | comments/docstrings (module, class, method, trailing) containing `read_text`/`subprocess` must not flip a P1; docstring/comment/string `assert` must not make a P0 a P1; code in string literals and f-strings | 4 | 16 |
| `u-` | uncaptured imports: call result asserted (P0), unused/only-in-message (P1), relative/star imports, stdlib results, deliverable import unused vs used | 4 | 14 |
| `struct-` | nested defs not called, `with`/`try`, conditional expression, walrus, chained compare, module constants, decorators (`lru_cache`, `contextmanager`), `test_`/`test_1` vs `tests_…`/`testnounderscore` | 7 | 17 |

Total 90 cases / 371 tests (the task asked >=60).

## Decisions taken inside `cases.json` (each follows a spec sentence)
- Zero reachable assertions, including `return exists`, unconditional `pytest.fail`/`raise AssertionError` and `skip` → `P0` (clause 1 / N).
- `assert exists or other_exists`, `and`/`or`, `== True`, `is True`, `bool(...)`, `all/any(exists …)`, variable-carried bools → `P1` (clause 2).
- Any reachable read/subprocess even after the existence assertion, or in a fixture or helper at depth 3 → `P0` (clause 3: "no reachable code").
- `open(p, "w"/"wb"/"a")`, `.touch()`, `.mkdir()`, `write_text`, `Path.open("w")` are not reads → `P1` when only existence is asserted; `open(p)`, `open(p,"r"/"rb")`, `open(p, encoding=…)`, `Path.open()` are reads → `P0`.
- `time.sleep` polling loops are not in clause 3's list → `P1` when only existence is asserted.
- Imports of uncaptured modules that are not called are not reachable code → `P1`; an assertion on their call result → `P0` (U maps to P0).
- Helper names can lie (`check_exists` reading content → `P0`; `read_text_summary` checking existence → `P1`); a same-file `def exists(p)` shadows `os.path.exists`.
- Functions not named `test_*` (and names like `tests_x`, `testx`) are never keys; a nested `def test_inner` is not a test.

## Ambiguities (spec does not decide) — all in `ambiguous.json`, 47 modules
Grouped (reading A / reading B in the file):
1. **Negation vs the operational definition** (5): `assert not exists`, `"x" not in listdir`, `exists == False`, `not a or b`, `unittest assertFalse(exists)`. Clause 2 allows `not`, but the definition says touching the paths must satisfy every assertion — `assert not exists` fails when the path is created. This is the largest classification risk for the real population.
2. **Existence in disguise** (9): `missing == []`, `not missing`, `len(glob) >= 1`, `os.listdir(d)` truthy, `next(glob, None)`, `sum(exists) >= 1`, `exists(a) == exists(b)`, `any(name == "x")`/suffix predicates on listing names, `isinstance(exists, bool)`.
3. **Assertion forms not named in clause 1** (6): `self.fail(...)`, `assert False` under an existence guard, `raise RuntimeError` on missing, `pytest.skip`, `pytest.raises(FileNotFoundError)`, `assertEqual(exists, True)`, `Path.resolve(strict=True)` in try/except.
4. **Reach through implicit code** (8): autouse fixture, `setUp`, `setUpClass`, inherited helper (`class T(Base)`), inherited test method (which key?), module-level constant reading a file (used and unused), uncaptured fixture arg (conftest), built-in `tmp_path`.
5. **Predicates not in the clause 2 list** (6): `os.path.lexists`, `is_mount`, `is_socket`, `stat.S_ISREG(st_mode)`, `os.access(R_OK)`, bare `Path.stat()`, `shutil.which`.
6. **Dead/never-asserted effects** (4): constant-false branch containing a read, size computed but not asserted, read result discarded after an existence assert, read in the assertion message (evaluated only on failure).
7. **Process state feeding the path name** (2): `os.environ["HOME"]`, `os.getcwd()`; plus `os.fork`/`waitpid`, `async def test_*`, `assert True`, uncaptured constant imported as the path, parametrised conditional expression selecting the predicate.

Expected score for a classifier: it MUST pass all 90 cases; on `ambiguous.json` it has no pass/fail — the "follows A/B" tally is a map of which reading it chose.

## Risks / things I could not settle
- Cases `cl2-polling-loops` (`time.sleep`), `cl2-writes-are-not-reads` (writes via `open("w")`) and `cl3-deliverable-import-and-call::test_import_but_not_called` rest on the letter of clause 3, not on a stated example; if the labelers read "process state" widely they would disagree. I kept the letter-of-spec reading.
- `cl2-comparison-to-bool::test_ne_false` (`exists != False`) is `P1` by "comparison to True/False" while `exists == False` sits in the ambiguous list; both are consistent with clause 2 but diverge on the operational test.
- No classifier was run, so I do not know how many of the 90 cases a real classifier fails.

tool: none misbehaved.
