# C1LabelRevD — blind label seat D (round 53, wave 1, R53-C1)

## What I did

Blind label seat D of 8 for the round-53 presence-only oracle. I read **only**:

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/p1-spec.md` (the one definition of presence-only),
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/labels/shard-D.json` (my shard: 77 test functions over 56 Terminal-Bench 2.0 task graders),
- the captured grader bytes themselves: every `corpus/evidence/round52/graders/<task>/tests/test_outputs.py` referenced by the shard, plus each task's sibling `tests/test.sh`.

**Blindness statement:** I did not read, run, grep or open `plans/round53_c1_classify.py`, anything under `.ufo/waves/round-53/w1/C1ExecClassifier*`, `.ufo/waves/round-53/w1/C1Label*` (no other seat's directory), or any classifier output. I did not write or run a classifier; every label below was decided by reading the captured bytes. No seat's output was used to tune mine — I did not consult any other label file at all.

## Exact commands run

Read (no side effects):

```
# spec + shard
read .ufo/waves/round-53/p1-spec.md
read .ufo/waves/round-53/labels/shard-D.json
# all 56 grader files + 56 test.sh siblings, via `read <path>:raw`
# (also read a few files with :N-M:raw where the file exceeded the display window:
#  adaptive-rejection-sampler 301-307, extract-elf 301-392, llm-inference 301-366)

# enumerate every capture file in every task directory of my shard
cd .../corpus/evidence/round52/graders && for d in <56 task dirs>; do find "$d" -type f | sort; done

# confirm the three "environment/" duplicate copies are byte-identical to tests/ copies
diff -u circuit-fibsqrt/environment/tests/test_outputs.py       circuit-fibsqrt/tests/test_outputs.py
diff -u large-scale-text-editing/environment/tests/test_outputs.py large-scale-text-editing/tests/test_outputs.py
diff -u overfull-hbox/environment/tests/test_outputs.py          overfull-hbox/tests/test_outputs.py
# all three diffs empty -> the environment/ copies add no reachable code

# span sanity: first and last line of every shard span
python3 -c "import json; ...print(r['id'], span[0], span[-1])"   # 77/77 spans start on the def and end on its last statement

# coverage check (labels only; no classifier)
python3 -c "import json,hashlib,collections; shard=...; lab=...; print(missing, extra, dupes, bad, Counter, sha256)"
```

No git, no `jj`, no writes outside my seat directory and my scratch. No packages installed or upgraded (nothing to install: the seat needed only `read`, `grep`-free reading and `python3` for the JSON coverage check — the toolchain already present). Tool/version/channel: none installed, so no install record applies.

## Measured numbers

- Shard size: **77** ids; labels written: **77** (0 missing, 0 extra, 0 duplicate ids; every `why` ≤ 20 words).
- Label distribution: **Y = 11**, **N = 66**, **U = 0**.
- `sha256(labels.json)` = `af97b41b2629a73bd12e8aee2ed9594e8c21e27e2b860bb6b6a1faac57451324`
  (computed over the exact bytes of the file at
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelRevD/labels.json`).

### The 11 Y labels

| id | why it is presence-only |
|---|---|
| `build-pmars::test_debian_source_used` | `Path("/app").glob("pmars-*")` non-empty + `debian` dir `.exists()` only |
| `cancel-async-tasks::test_run_py_file_exists` | one `.exists()` on `/app/run.py` |
| `code-from-image::test_output_file_exists` | one `.exists()` on `/app/output.txt` |
| `path-tracing::test_image_c_exists` | one `.exists()` on `/app/image.c` |
| `prove-plus-comm::test_compiled_proof_exists` | one `os.path.exists("plus_comm.vo")` |
| `pytorch-model-recovery::test_model_file_exists` | one `.exists()` on `/app/model.pt` |
| `sam-cell-seg::test_csv_output_exists` | one `.exists()` on `/app/test_output.csv` |
| `sparql-university::test_sparql_file_exists` | one `.exists()` on `/app/solution.sparql` |
| `tune-mjcf::test_tuned_model_exists` | one `.exists()` on `/app/model.xml` |
| `video-processing::test_example_video_exists` | one `.exists()` on `/app/example_video.mp4` |
| `vulnerable-secret::test_results_file_exists` | one `.exists()` on `/app/results.txt` |

## Ids I found hardest, and why

1. **`build-pmars::test_debian_source_used`** — the hardest Y. Two assertions, both on names: `assert source_dirs` from `Path("/app").glob("pmars-*")` and `assert debian_dir.exists()`. Rule 2 explicitly admits "glob non-empty" and `.exists()`, and rule 3 is not tripped (the module-level helper `run_shell_command` is *not* called from this test, and reach is transitive-call based). Creating `/app/pmars-x/debian` satisfies both. I judged it **Y**; a reader who treats any `glob` as a name-set comparison could argue either way, so this is the id most worth a second opinion.
2. **`mcmc-sampling-stan::test_posterior_beta_estimation`** and **`rstan-to-pystan::test_sigma_estimation_accuracy`** — closest calls to Y, and both **N**. Their assertions are guarded by `if os.path.exists(path):`, so with the file *absent* the test passes vacuously. But "passes in every execution state in which the paths merely exist, whatever they contain" fails: create the file empty and the body reads it (`content`/`len(content) > 0`, float parsing, range check) and the assertion fails. Existence-guarded ≠ presence-only.
3. **`headless-terminal::test_cancel_command`** — the assertion itself is pure existence (`assert not path.exists()`), but the reachable code imports and drives the task's own deliverable (`from headless_terminal import HeadlessTerminal`, `terminal.send_keystrokes(...)`), which rule 3 forbids. **N**.
4. **`headless-terminal::test_import`** — no assertion at all; rule "the test reaches no assertion at all" ⇒ **N** (not U: the verdict is decidable from the captured bytes).
5. **`kv-store-grpc::test_grpc_tools_installation`** — `try: import grpc … except ImportError: assert False`. The assertion is not a path-existence/type check (the allowed predicates are the listed path APIs only), and creating paths cannot satisfy it. **N**.
6. **`build-cython-ext::test_cinvariants_cython_extension`** — `importlib.util.find_spec(...)` plus a loader-class check. Tempting as "does the module exist", but `find_spec` is not in the spec's predicate list, and the test also imports the task's own deliverable. **N**.
7. **`polyglot-c-py::test_fibonacci_polyglot`** — starts with `os.listdir("/app/polyglot") == ["main.py.c"]`, i.e. a directory-listing *equality*, not mere membership; then compiles and runs binaries. **N**.
8. **`circuit-fibsqrt::test_gates_file_size`** — name says "size" but it is a *line count* read from file content, not a size value of the path; still content-dependent ⇒ **N** (contrast with the spec's `os.path.getsize` example, which is explicitly N).
9. **`write-compressor::test_compression_size`** — the `setup()` helper is a same-file helper reached by the test: it copies files and runs `gcc`. Reachable subprocess ⇒ **N**, even though the final assertion is a size comparison.
10. **`install-windows-3.11::test_network_status`** — the same-file pytest fixture `netstat_output` (requested by argument name, so reachable) runs `netstat`; the assertions match substrings of its output ⇒ **N**.

**No U in this shard.** Every candidate for U (uncaptured imported module: `portfolio_baseline_protected`, `attack`/`feal_in_c`, `algo`, `eigen`, `parallel_linear`, `headless_terminal`, `bottle`) still had a decidable verdict from the captured bytes alone — each of those tests runs a subprocess, imports the deliverable, or compares values, which is N regardless of what the uncaptured helper does. U is reserved for "captured bytes do not let you decide", and in no case here did the *presence-only* question hinge on the uncaptured code.

## Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelRevD/labels.json` (the deliverable; sha256 `af97b41b2629a73bd12e8aee2ed9594e8c21e27e2b860bb6b6a1faac57451324`)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelRevD.md` (this report)

Scratch: none was needed; no `/fast/scratch/hyaku/kengaku-r53/C1LabelRevD/` directory was created, so nothing to clean up there. Nothing was written outside my seat directory. No credential-shaped strings appear in my outputs.
