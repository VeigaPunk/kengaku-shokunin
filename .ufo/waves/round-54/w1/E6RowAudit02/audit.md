# Round 54 entry-truth independent row audit

Clone revision: `62e9bba5e4a0bed376890299aa6a09039db7e68e`. Hermetic environment imported from `plans/round54_c2_entrytruth.py:hermetic_env`; each subprocess ran with cwd=clone, timeout 600 seconds, and `TMPDIR` set to its seat-scratch directory.

## benchmark-spec-audit

```sh
python3 plans/benchmark_spec_audit.py --summary
```

Declared exit: 0; observed exit: 0; entry-mode flags clean: True; script exists in clone: True; evidence: `none declared (green row)`; fragment-match: True; verdict: **CONFIRMED**. TMPDIR: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit02/tmp-benchmark-spec-audit`.

Observed output tail:
```text
LIMIT WebArena repository snapshot dce04686a56253aefba7b18a4fa0937cf1dc987b (2025-11-26), not its 2023-07-25 release or WebArena-Verified.
LIMIT Static schema and predicate inventory is not semantic task validity, actual task success or contamination evidence.
LIMIT No upstream code imports/execution, model calls, browser actions, benchmark site traffic or auth material opened.
LIMIT Selected16 are minimum IDs of first16 lexicographic site/evaluator strata, not a representative/random sample.
LIMIT Live DOM/API state, fixture resets, navigation and external LLM judge outcomes are unverified.
LIMIT Schema findings follow declared field shapes, not full native equivalence or semantic/vacuity analysis; empty predicate containers may be compatible.
EVAL_TYPE_SETS {"program_html": 282, "program_html,url_match": 129, "string_match": 325, "string_match,url_match": 10, "url_match": 66}
SITE_SETS {"gitlab": 180, "gitlab,reddit": 18, "gitlab,wikipedia": 6, "map": 109, "map,shopping_admin": 2, "map,wikipedia": 17, "reddit": 106, "reddit,shopping": 5, "shopping": 187, "shopping_admin": 182}
STRING_OPERATORS {"exact_match": 45, "fuzzy_match": 118, "must_include": 176}
URL_RULES {"GOLD in PRED": 205}
URL_NOTE_ORIGIN {"defaulted": 9, "explicit": 196}
HTML_OPERATORS {"exact_match": 188, "must_include": 463}
LOCATOR_CLASSES {"full_page": 105, "helper": 22, "javascript": 524}
TOTAL task_count=812 distinct_task_ids=812 site_eval_strata=27 selected_count=16 program_html_targets=651 findings=0 exit=0
```

## build-pmars-probe

```sh
python3 plans/build_pmars_probe.py --lane .
```

Declared exit: 0; observed exit: 0; entry-mode flags clean: True; script exists in clone: True; evidence: `none declared (green row)`; fragment-match: True; verdict: **CONFIRMED**. TMPDIR: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit02/tmp-build-pmars-probe`.

Observed output tail:
```text
FPPP match=yes violates=from-source,debian-source,extract-to-app,debugger-works,install-path test_pmars_works:error=CalledProcessError -- binary installed without the execute bit: exists() holds, the shell cannot run it
CASE silent-binary predicted=fail observed=fail tests=FPPP predicted_tests=FPPP match=yes violates=from-source,debian-source,extract-to-app,debugger-works,install-path -- installed binary prints nothing
CASE path-split predicted=pass observed=pass tests=PPPP predicted_tests=PPPP match=yes violates=from-source,debian-source,extract-to-app,debugger-works,install-path -- /usr/local/bin/pmars prints nothing; a canned script at /usr/local/sbin/pmars (earlier on PATH) answers the behaviour checks, ldd reads the silent one
CASE no-debian-dir predicted=fail observed=fail tests=PPFP predicted_tests=PPFP match=yes violates=from-source,debian-source,extract-to-app,debugger-works -- source tree without debian/
CASE debian-is-file predicted=pass observed=pass tests=PPPP predicted_tests=PPPP match=yes violates=from-source,debian-source,extract-to-app,debugger-works -- debian is a zero-byte regular file: Path.exists() holds
CASE src-no-c predicted=fail observed=fail tests=PPPF predicted_tests=PPPF match=yes violates=from-source,debian-source,extract-to-app,debugger-works -- src/ holds a header only
CASE c-is-dir predicted=pass observed=pass tests=PPPP predicted_tests=PPPP match=yes violates=from-source,debian-source,extract-to-app,debugger-works -- src/sim.c is a directory: glob('*.c') matches it
CASE no-src-dir predicted=fail observed=fail tests=PPPF predicted_tests=PPPF match=yes violates=from-source,debian-source,extract-to-app,debugger-works -- source tree without src/
CASE pmars-dir-elsewhere predicted=fail observed=fail tests=PPFF predicted_tests=PPFF match=yes violates=from-source,debian-source,extract-to-app,debugger-works -- tree under /app/src/pmars-0.9.4, not /app/pmars-*: the glob is one level deep
cases=22 observed_pass=7 observed_fail=15 mismatches=0
```

## catalog-probe

```sh
python3 plans/catalog_probe.py --verify --lane .
```

Declared exit: 0; observed exit: 0; entry-mode flags clean: True; script exists in clone: True; evidence: `none declared (green row)`; fragment-match: True; verdict: **CONFIRMED**. TMPDIR: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit02/tmp-catalog-probe`.

Observed output tail:
```text
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
HF missing fields: author, sha, lastModified, gated
```

