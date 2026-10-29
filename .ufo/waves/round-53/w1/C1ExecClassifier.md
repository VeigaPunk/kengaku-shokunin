# C1ExecClassifier — round 53 wave 1 report

Seat: executor, builds the AST classifier. Blindness: I read no `C1Label*` file or directory and no oracle label
(I listed `w1/` once with `ls`, which printed sibling directory names only; I opened nothing in them).

## Deliverables
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ExecClassifier/round53_c1_classify.py`
  sha256 `b7842119c296ce4170f49be338f5b3e58161e0db15735291c401a54342406e40` (stdlib-only, deterministic; `classify_source`,
  `classify_detail` (adds P0 reasons), `--selftest`, `<file>... [--why]` histogram).
- `.../w1/C1ExecClassifier/classes-305.json` — the 305 `{id: P1|P0}` the file produced (for the L1's diff; not an oracle).

## Commands and numbers
- `python3 round53_c1_classify.py --selftest` -> `cases=68 failures=0` (>=20 required; covers all 8 spec examples, helper chain depth 3
  (Y and N), recursion (Y, and a cycle that ends in content), class method / unittest `self.assertTrue` / setUp, fixture argument
  (Y, fixture running a command, fixture chain, unknown conftest fixture), `pytest.fail` and `raise AssertionError` branches,
  `os.listdir` membership, name set from `iterdir()`, `any(...)` over `iterdir()`, `glob` non-empty, `len(listdir)==3` / `>=3`
  (P0), `with open(...)` read (P0), no assertion, empty module, module without tests, syntax error (-> `{}`), plus parametrize, tmp_path,
  monkeypatch, write-then-exists, universal loop/`all()`, staticmethod, negated exists).
- Population: `classify_source` on the 88 task files named by `corpus/evidence/round53/tests-index.json`, keyed as the counter's
  `v2_classes` does: **305 / 305 ids covered, unclassified = 0, no extra keys in any file**.
- Histogram over the 305: **P1 = 52, P0 = 253** (P1 spread over 41 tasks). Identical output under `PYTHONHASHSEED` 1, 2, 3.
- Robustness: ran over 199 CPython/site-packages `test_*.py` files (7,686 tests): no exception, 0 P1 (smoke only, not a measure).
- Toggling `IMPLICIT_SETUP` changes 0 of the 305 results (only `overfull-hbox` has setup code).
- Not run: the counter itself (not my assignment).

## Rule order implemented (abstract interpretation over `ast`, kinds K/N/L/W/E/Q/V/B/C/X)
1. Parse (a `SyntaxError` returns `{}`); collect imports, module functions, classes, fixtures, autouse fixtures, module/class constants.
2. For each `test_*` (module level `name`, class method `Class.name`): bind parameters (parametrize -> pure; same-file fixture ->
   its return kind; `tmp_path`-family -> pure; any other argument = unknown fixture -> X).
3. Reach: run implicit setup (`setup_module/function`, `setUpClass/setup_class/setUp/setup_method`, autouse fixtures), then the body;
   inline module helpers, `self.`/`cls.`/`Class.` methods (in-file base classes too), nested defs, requested fixtures (up to the first
   `yield`), referenced module/class constants; cycle guard returns a neutral value; depth 40.
4. Any reachable operation that is not in the existence/path-arithmetic tables is a violation: subprocess/os.system/popen, `open`,
   `read_*`/`write_*`/`stat`/`unlink`/`touch`..., json/yaml/pickle/hash/network/numpy/..., unknown or undefined callee, non-stdlib
   in-test `import`, same-file class construction, builtins computing values (`min`, `int`, ...), count/size/value comparisons,
   listing equality, `os.access` with a non-`F_OK` mode, `pytest.raises/approx`.
5. Assertions: `assert`, `self.assert*`, and `pytest.fail` / `self.fail` / `raise` guarded by an `if` or an `except` after a
   body that touched a path. Condition kind must be fs-dependent (existence/type/listing-name membership, `and/or/not`, `== True`,
   `len(L) > 0` / `>= 1` / `!= 0`, truthiness of a listing, `any(...)`); a condition with no path state (constant/computed), or
   X, is a violation. Assertion messages and exception arguments are not evaluated (failure path only).
6. P1 iff no violation and >= 1 fs-dependent assertion; otherwise P0 (this covers "no assertion" -> P0).

## Spec ambiguities and the choice made (L1 may quote)
1. **Emptiness / `== 0`**: `len(L) == 0`, `< 1`, `listing == []` are counts -> P0, but `assert not <glob/listing>` (negated non-empty) -> P1
   (spec allows `not`). Affects `financial-document-processor::test_original_documents_dir_empty` (P0).
2. **Universal over a listing** (`for f in listdir: assert ...`, `all(... for p in iterdir())`): P0 — passes only if no other entries
   exist, so not satisfied by "merely exist". `any(...)` over a listing and a flag set under a listing loop stay P1.
3. **Picking from a listing** (`list(glob)[0] / "x"` then `.exists()`): P1 (named path chain still existence). Affects the two
   `build-pmars` tests that call `source_dirs[0] / ...`.
4. **Constant-only assertion** (`assert 1+1==2`, `assert Path(x).suffix == ".py"`): P0 (no path state tested); literal `assert True` is neutral.
5. **Unconditional `raise`/`pytest.fail`**: P0 (never passes). Handler-guarded failure counts only if the `try` body touched a path
   (so `try: import grpc / except ImportError: assert False` is P0; `try: os.listdir(d) / except: pytest.fail` is P1).
6. **In-test import of a non-stdlib module** (numpy, pytest-external deliverable, `grpc`...): violation even without a call ("imports
   ... code from the task's own deliverable / environment"). Module-level imports matter only if the test uses the name; an imported
   name that is not stdlib is X, any call on it P0 (U -> P0).
7. **Setup/teardown**: setUp/setUpClass/setup_*/autouse fixtures ARE reached (spec lists only helpers, `self.` methods, requested
   fixtures); teardown and code after a fixture's `yield` are NOT. Zero effect on the 305; flag `IMPLICIT_SETUP` exists.
8. **Process-state path naming** (`os.environ.get`, `os.getenv`, `os.getcwd`, `Path.home()`, `Path.resolve()`, `os.path.realpath`) is
   treated as pure path naming, not as state compared; `readlink`, `shutil.which`, `stat`, `Path.owner` are P0.
9. **Unknown conftest fixtures** (argument not defined in the file, not `tmp_path`): X -> P0 only if used in a call/assertion, else
   inert. `tmp_path` is a pure empty dir.
10. **Cross-file helpers** (captured sibling `.py` files) are not inlined; `classify_source` gets one string. Calls into them are P0 (U).
11. **Side-effecting existence setup** (`write_text` then `exists`, `mkdir`, `shutil.copy`): P0 (not a plain existence predicate).
12. **Module-level code** outside referenced constants is not executed/reached (e.g. a top-level `subprocess.run` is ignored unless a
   referenced constant contains it).
13. **Unittest `assertEqual(exists(), True)`-style** is mapped onto the same comparison rules as `assert a == b`; `assertRaises`,
   `assertRegex`, `assertAlmostEqual` -> P0.
14. A string-kind result of a name predicate (`f.endswith(".py")` on a listing name) is treated as boolean-like when asserted (suffix/
   name checks on listing entries are name membership).
15. An analyser exception on any test yields `P0` with reason `U: analyser error` (never drops an id); none occurred.

## Tools / issues
No tool installed or updated. No tool output looked inconsistent.

---

## Fix round (round 53 pre-freeze, L1 request from `KengakuR53-2`)

The frozen spec (`.ufo/waves/round-53/p1-spec.md`) is unchanged; the deliverable was corrected to
follow it. Deliverable rewritten **in place**:
`.ufo/waves/round-53/w1/C1ExecClassifier/round53_c1_classify.py`, new sha256
`0dfa2fbe0359789bc7937fc65b36742866d4962dd7f20bff79b6e7e8e10b09b6` (was
`b7842119c296ce4170f49be338f5b3e58161e0db15735291c401a54342406e40`).
Final file after the dead-code removal (`until_yield`, `foreign_module`): sha256
`935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6` — this is the hash to freeze.

### Numbers

| measurement | before the fix round | after |
|---|---|---|
| `python3 round53_c1_classify.py --selftest` | `cases=68 failures=0` | **`cases=83 failures=0`** (15 new cases) |
| `python3 .ufo/waves/round-53/w1/C1ExecAdvCases/check.py round53_c1_classify.py` | `TOTAL cases=90 case_fail=14 tests=371 test_fail=22` | **`TOTAL cases=90 case_fail=0 tests=371 test_fail=0`** (every clause line `case_fail=0 test_fail=0`) |
| ambiguous set (informational) | `follows_A=30 follows_B=16 of 47` | `follows_A=29 follows_B=17 of 47` (only `amb-len-glob-ge-1` flipped to the count reading) |
| 305-id coverage (`coverage305.py`, this seat) | `305/305 covered, unclassified=0, extra keys=0` | `IDS total=305 covered=305 unclassified=0 · EXTRA KEYS 0` (unchanged) |
| histogram over the 305 | `P1=52 P0=253` | **`P1=52 P0=253`** (P1 over 41 of 88 tasks) — *no population id changed* |

`CHANGED 0` against the previous `classes-305.json` (the mapping is identical; the new file is
byte-different only in JSON formatting). Receipts: `C1ExecClassifier/fix-round-receipt.txt`,
coverage driver `C1ExecClassifier/coverage305.py` (added this round).

### What changed, and why (one line per decision)

1. **`cl2-os-access / test_f_ok_kw` → P1** — clause 2 names `os.access(p, os.F_OK)`; the keyword
   form `mode=os.F_OK` was not recognised (only the positional form was).
2. **`cl2-listing-counts / test_len_gt` → P0** — the N clause lists "a count"; `len(listdir) > 0`
   is a count, and operationally an empty directory fails it, so it is not presence-satisfiable.
3. **`cl2-boolean-combinators / test_all_list` → P1** — clause 2 allows combining path conditions;
   `all([exists, exists])` is a conjunction of path conditions (the generator form was already
   accepted).
4. **`cl2-writes-are-not-reads` (8 tests) → P1** — clause 3 forbids *reads*/parses, not writes, and
   the operational definition names `touch`/`mkdir` as the way presence is created; a write
   followed by a content read still ends in P0 because the read itself is the violation.
5. **`cl2-polling-loops / test_poll_for_else` → P1** — the `else` branch runs exactly when the loop
   was not broken, i.e. when the path is absent, so the failure there is still path-dependent
   (clause 1). Implemented as a break-guard: a `break` under a path condition guards the loop's
   `else`.
6. **`cl3-deliverable-import-and-call / test_import_but_not_called` → P1** — clause 3 forbids
   importing **and calling** the deliverable; an unused import does not decide the verdict, and U
   requires the verdict to depend on uncaptured code.
7. **`cl3-value-and-state-asserts / test_arith_with_path` → P0** — clause 2 allows only path
   conditions in an assertion's condition; `2 * 2 == 4` is a value comparison (clause 3).
8. **`cl3-value-and-state-asserts / test_enum_count` → P0** — `len([...]) == 2` is a count (same
   rule as 2); a value comparison inside the condition breaks clause 2.
9. **`reach-lambda-helper / test_lambda_clean` → P1** — a lambda bound to a name is a same-file
   helper (reach paragraph), so it is inlined like a function.
10. **`reach-fixture-yield-and-scope / test_yield_dirty` → P0 (my decision, spec-backed)** — the
    reach paragraph names the *requested fixture function* as reachable code and clause 3 forbids
    reachable content reads; operationally a decode error in the teardown makes the outcome depend
    on the content. **Flag for wave 2**: pytest runs teardown *after* the assertion, so a reader
    could argue the outcome is decided by the assertion alone (P1). I kept P1→P0 because the
    spec's reach paragraph and clause 3 are the frozen text and the case expects P0.
11. **`reach-fixture-value-assertions / test_fixture_with_params` → P1** — `request.param` is a
    fixture parameter value (a name), not filesystem state; the assertion still only tests
    existence (clause 2).
12. **`unittest-content-styles / TestV.test_true_len` → P0** — same count rule as 2
    (`assertTrue(len(listdir) > 0)`).
13. **`fail-branches-existence / test_fail_return_early` → P1** — after `if path.exists(): return`
    the failure is reached exactly when the path is absent, so it is path-dependent (clause 1);
    implemented as a negated guard carried to the following statements of the block.
14. **`u-imported-stdlib-results / test_stdlib_compare` → P0** — `fnmatch.fnmatch("out.txt",
    "*.txt")` compares constant strings: a value comparison (clause 3), and ANDed with an existence
    check it breaks clause 2.
15. **`struct-with-and-try / test_with_ctx` → P1** — `contextlib.suppress` is a context manager,
    not a read/command/value comparison, and the assertion inside it is still reached (clause 1).
    **Flag for wave 2**: `suppress(Exception)` around an assertion makes the test pass
    unconditionally — a *stronger* vacuity than presence-only; the spec's clause 1 only demands
    that the assertion be reached, and the case expects P1.

Two of my own selftest expectations were corrected to the same spec reading (documented, not
silently changed): "glob via len > 0" P1 → **P0** (count) and "write then exists" P0 → **P1**
(write). 15 new selftest cases were added, one per fixed rule.

### Rules that changed in the analyser (for the freeze note)

* counts are never existence (`len(...) > 0` included);
* writes are not reads: `open(..., "w"/"wb"/"a")`, `Path.write_text/write_bytes/touch/mkdir/unlink`,
  `os.mkdir/remove/rename/...`, and file-handle `write/flush/close` are side effects;
* an in-test import of a non-stdlib/deliverable module is a violation only when it is **called**;
* a lambda bound to a name is inlined as a same-file helper;
* `request.param` is a pure value;
* the statements after a fixture's `yield` are reachable code (teardown included);
* a failure guarded by the *negation* of a path condition (early `return`, `for/else`) is
  path-dependent;
* `contextlib.suppress` is neutral; `fnmatch.fnmatch` over constant strings is a value comparison.

The population classification is unchanged by all of this (P1=52, P0=253; 0 ids changed), so the
fix round moves no lane number — it only makes the instrument agree with the frozen spec text.
No tool was installed; no tool output looked inconsistent.
