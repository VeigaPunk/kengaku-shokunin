# C1LabelRevH — round 53 wave 1, blind label seat H

## What I did

Read the one definition of presence-only (`.ufo/waves/round-53/p1-spec.md`, frozen with
`plans/round-53-claims.md` @ a34838f) and my shard
`.ufo/waves/round-53/labels/shard-H.json` (76 ids, 64 distinct grader capture files).
For every id I read the **whole** capture file (`:raw`, in full, including the parts
outside the id's line span) and the sibling capture files the test reaches
(`tests/test.sh`; the `environment/tests/test_outputs.py` duplicates for
`break-filter-js-from-html`, `circuit-fibsqrt`, `large-scale-text-editing`,
`overfull-hbox` were byte-identical to the `tests/` copies — verified with `diff -q`).
Labels were decided **by reading only**. I did not write, run or consult any
classifier (`plans/round53_c1_classify.py`), and I did not open any other seat's
directory under `.ufo/waves/round-53/w1` (`C1Label*`, `C1ExecClassifier*`). No
blindness violation occurred.

Deliverable: `.ufo/waves/round-53/w1/C1LabelRevH/labels.json`

```
sha256(labels.json) = 3b9fc7deebbb4222bf55eeb6b4ed41123b6f01f1f60536c4156bd9b88db52e39
size                = 11386 bytes
labels              = 76 (exactly the shard; no missing id, no extra id)
```

## Exact commands I ran

```
python3 -c "import json; d=json.load(open('.../labels/shard-H.json')); ..."      # shard listing
find .ufo/../corpus/evidence/round52/graders -type f | grep -v test_outputs.py   # sibling capture inventory
diff -q <task>/tests/test_outputs.py <task>/environment/tests/test_outputs.py    # duplicate-capture check
read .../<task>/tests/test_outputs.py:raw                                        # full file, per task (64 files)
python3 - <<'EOF'  ...                                                         # coverage check of labels.json
sha256sum .ufo/waves/round-53/w1/C1LabelRevH/labels.json
rm -rf /fast/scratch/hyaku/kengaku-r53/C1LabelRevH                              # scratch cleanup
```

No tools were installed or upgraded for this seat (the task needed only `read`,
`bash`, `python3`, `json`; all already present), so there is no tool/channel/
version entry to record.

## Measured numbers

| label | count |
|-------|-------|
| Y (P1, presence-only) | **16** |
| N (P0)               | **60** |
| U (undecidable)      | **0**  |

Y ids (16):

```
build-cython-ext::test_repo_cloned
caffe-cifar-10::test_prototxt_files_exist
extract-elf::test_extract_js_exists
financial-document-processor::test_directories_created
gcode-to-text::test_hello_file_exists
log-summary-date-ranges::test_summary_file_exists
merge-diff-arc-agi-task::test_algo_py_exists
modernize-scientific-stack::test_dependency_file_exists
mteb-retrieve::test_result_exists
openssl-selfsigned-cert::test_directory_structure
prove-plus-comm::test_proof_file_exists
pytorch-model-cli::test_weights_file_exists
raman-fitting::test_result_file_exists
torch-pipeline-parallelism::test_pipeline_parallel_exists
video-processing::test_test_video_exists
winning-avg-corewars::test_warrior_exists
```

Every Y body is one of: a single `assert path.exists()`; `assert exists() and
is_dir()`; `assert exists() and is_file()`; or `assert any(Path(f).exists() for f in
[…])` over a two-element candidate list. None of them reads content, runs a
command, or compares a value.

## Hardest ids and why

- `build-cython-ext::test_ccomplexity_cython_extension` — hardest boundary in the
  shard. It uses `importlib.util.find_spec("pyknotid.spacecurves.ccomplexity")` and
  asserts `spec is not None` plus `isinstance(spec.loader, ExtensionFileLoader)`.
  "Type of a path" in the spec means path type (`is_file`/`is_dir`), not module-loader
  type; the assertion also reaches into the task's own deliverable package. Labelled
  **N** (P0), not Y.
- `hf-model-inference::test_model_downloaded` — begins with a pure
  `assert os.path.exists(model_path)` but then loads model + tokenizer from that
  directory and asserts the objects are non-null. The existence assertion alone would
  be presence-only; the reachable load makes the whole test N. Labelled **N**.
- `sam-cell-seg::test_run_script` — runs `subprocess.run([...], check=True)` and
  contains **no** assertion at all. The spec says a test that reaches no assertion is
  N. Labelled **N**.
- `mailman::test_mlist_exists` — `assert mlist` on a mailman-core object obtained via
  `getUtility(IListManager)`. Not a path condition; also the deciding code
  (`mailman.core.initialize`, `IListManager`) is outside the captures, but the
  captured bytes already decide the verdict (the condition is not a path-existence
  condition), so it is N rather than U.
- `modernize-scientific-stack::test_dependency_file_exists` — a disjunction over two
  candidate paths (`requirements.txt`, `pyproject.toml`). Creating either satisfies
  it, and the condition is purely existence-based, so **Y**.
- `prove-plus-comm::test_proof_file_exists` — the only Y whose path is *relative*
  (`plus_comm.v`, cwd-relative). It is still a bare `os.path.exists`, so **Y**.
- `llm-inference-batching-scheduler::test_input_data_integrity` — the file has a
  relative import `from .cost_model_for_tests import …` whose module is not in the
  captures (a U trigger in general). Here the id's own body only hashes input files
  and compares digests, so the verdict is decidable from the captured bytes → **N**.
- `portfolio-optimization::test_correctness_small` — imports the uncaptured
  `portfolio_baseline_protected`, but its assertions are numeric risk/return
  comparisons, decidable from the captured bytes → **N**.
- `install-windows-3.11::test_qemu_running_with_correct_params` — depends on three
  same-file fixtures (`qemu_pid`, `cmdline`, `img_path`), all of which run
  subprocesses / read `/proc`, plus a SHA-256 of the disk image → **N**.

## U analysis

Zero U ids. In every case where an uncaptured module is imported
(`cost_model_for_tests`, `portfolio_baseline_protected`, `mailman.core.*`, the
deliverable packages `pyknotid`, `eigen`, `parallel_linear`, `algo`), the id's own
assertions are enough to decide the label, so the "captured bytes do not let you
decide" condition of the spec is never met.

## Residual risk / notes for wave 2

- 16/76 = 21% presence-only in this shard. The shard is dominated by Terminal-Bench
  graders that run the agent's program and compare outputs, so a high N rate is
  expected; the Y rate is not evidence about the population.
- Two of my Y calls are single-`exists()` graders where the grader is trivially
  satisfiable by `touch` — that is the point of the claim, but it means a
  classifier that misses `assert p.exists()` will lose them.
- `build-cython-ext::test_repo_cloned` is a Y whose assertions include
  `path.is_dir()` and `(path/".git").exists()` — a classifier must treat
  `is_dir()` + `.exists()` as still presence-only, and must not treat the `.git`
  suffix as a content check.

## Scratch discipline

Scratch dir `/fast/scratch/hyaku/kengaku-r53/C1LabelRevH` was created and has been
removed (`rm -rf`). No git mutation was performed anywhere; nothing outside my seat
directory and my seat report was written. No credential-shaped strings appear in any
file I produced (no tokens, keys or `op://` references), and no grader bytes were
copied into the report — the only quoted material is my own 20-word "why" strings.
