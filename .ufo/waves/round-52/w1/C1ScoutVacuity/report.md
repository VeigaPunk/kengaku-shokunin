# C1ScoutVacuity — R52-C1 grader presence probe

## Result

Fetched all **89/89 primary `tests/test_outputs.py` graders** from Terminal-Bench 2.0 at frozen commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`. The grader paths were selected with the frozen counter's `primary_grader()` function; downloaded Git blobs were SHA-1 verified against Git object IDs. All 89 parsed as Python.

The literal frozen §C1 marker scan finds **6/89 tasks with no content or behaviour marker**; 5/6 also contain a presence marker. This is a *marker-defined zero-content/behaviour population*, not evidence that six graders are actually satisfiable by an artefact's presence alone. Manual inspection found substantial checks in those six graders; details below.

For assertion counts, I used Python AST `Assert` nodes and separately counted (a) assertions whose test expression reduces to existence predicates (`exists`, `is_file`, `is_dir`, including boolean combinations/negation and `all`/`any` wrappers), and (b) asserts containing those literal call tokens. On this population the pure-existence and token counts are both **148 asserts across 66 tasks**; no mixed existence asserts were observed. **798 total assert statements** across all 89 graders. This syntactic probe does not prove a task's overall grader is satisfiable merely by existence: other assertions in the same grader can be substantive.

### Five largest tasks by total assert statements

| Task | Total asserts | Pure existence asserts |
|---|---:|---:|
| `db-wal-recovery` | 26 | 1 |
| `llm-inference-batching-scheduler` | 26 | 2 |
| `caffe-cifar-10` | 25 | 7 |
| `install-windows-3.11` | 25 | 3 |
| `openssl-selfsigned-cert` | 24 | 6 |

For the existence-assert view, the top five are `query-optimize` (12), `caffe-cifar-10` (7), `large-scale-text-editing` (6), `openssl-selfsigned-cert` (6), and `headless-terminal` (5). Full rows and hashes are in `per-task.jsonl`.

## Three located presence-only-looking assertions

These are examples of individual assertions whose predicate checks existence only; **they are not three whole presence-only graders**. The surrounding grader may impose stronger checks.

1. `pytorch-model-recovery`, `tests/test_outputs.py:88`: `assert weights_path.exists(), f"File {weights_path} does not exist"`.
2. `pytorch-model-recovery`, `tests/test_outputs.py:108`: `assert hello_path.exists(), f"File {hello_path} does not exist"`.
3. `torch-tensor-parallelism`, `tests/test_outputs.py:25`: `assert parallel_linear_path.exists(), f"File {parallel_linear_path} does not exist"`.

The first two are outweighed by other checks in that grader: lines 90–100 load and compare weights; lines 114–116 load a model and state dict; lines 123–136 compare state dictionaries; lines 142–167 compare model losses. The third is followed by distributed process setup and test functions (e.g. lines 28–40 and 187–211). They are presence-only *assertions*, not presence-only task graders.

## Marker-set review / false positives

The six raw-claims-marker zero-content/behaviour tasks are `bn-fit-modify`, `distribution-search`, `largest-eigenval`, `portfolio-optimization`, `pytorch-model-recovery`, and `torch-tensor-parallelism`.

- `bn-fit-modify` and `portfolio-optimization` are not actual zero-marker cases under the frozen counter: its `assert.*\bin\b` content alternative classifies them V3 (the prose-only scan classified them zero-marker). This illustrates why the instrument classifier, not the prose marker paraphrase, is used for the frozen population.
- `distribution-search` loads `/app/dist.npy` and asserts shape, vocabulary size, validity, sum and KL divergence (e.g. `tests/test_outputs.py:27`, `36`, `39`, `42`, `49`, `52`, `55`, `58`, `62`, `69`, `80`, `86`). Its calls use `np.load`, not the enumerated content marker spellings, hence the raw-marker false positive.
- `largest-eigenval` has eigenpair, dominance and speedup checks (e.g. `tests/test_outputs.py:50–67`, `71–81`, `85–111`). The frozen behaviour regex hits `import os` at line 6, so the frozen classifier places it V2; no grader-file content marker is needed for this note.
- `pytorch-model-recovery` and `torch-tensor-parallelism` carry substantive content/behaviour tests even though the frozen marker rules classify them V1; see the located checks above and `pytorch-model-recovery` lines 90–100, 114–167. These are actual classifier false positives for whole-grader presence-only.

Thus the empirically supported answer is **0 manually confirmed whole graders satisfiable by mere artefact presence among the six marker-defined candidates reviewed**, while **6/89** is the frozen-prose zero-content/behaviour marker count and **2/89** is the frozen counter's V1 class count. The two V1 classifications are not validated as true presence-only by this probe; they include content/behaviour missed by the frozen regex. This probe is a locator for wave-2 confirmation, not a replacement for independent confirmation or a change to frozen claim rules.

## Counts and caveats

- AST assertions: 798 total; 148 pure existence; 0 mixed existence; 148 token-matched existence; 66 tasks with at least one.
- Frozen counter class histogram on these exact bytes: V2=53, V3=32, V1=2, V0=2; V4=0.
- Frozen prose markers (not the instrument classifier): 6 tasks with zero content and behaviour; 5 of those with presence.
- One grader has an `os.path.isfile(...)` assert (not in the seat's three literal tokens); counted separately, not added to the seat token total.
- AST structure is a static approximation: it does not follow aliased helper functions or variables. Thirteen graders have existence-call expressions outside `assert` nodes; the per-task JSONL records these.

## Commands run

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r52/C1ScoutVacuity/tmp /fast/scratch/hyaku/kengaku-r52/C1ScoutVacuity/graders
# Initial raw URL/API check (raw returned HTTP/2 200; GitHub API returned 403 rate limit)
curl -fsSI --max-time 30 'https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/adaptive-rejection-sampler/tests/test_outputs.py'
curl -fsS --max-time 60 'https://api.github.com/repos/harbor-framework/terminal-bench-2/contents/?ref=2fd12b88aafdd04a52c298e3940bcb189f9766d6' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(type(d).__name__, len(d)); print("\\n".join(x.get("type","")+"\\t"+x.get("name","") for x in d[:40]))'
# Download exact pin into seat-owned scratch; no checkout or lane mutation
 git init tb2
 git -C tb2 rev-parse --show-toplevel
 git -C tb2 remote add origin https://github.com/harbor-framework/terminal-bench-2.git
 git -C tb2 fetch --filter=blob:none --depth 1 origin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
 git -C tb2 rev-parse FETCH_HEAD
 git -C tb2 ls-tree -r FETCH_HEAD
# The probe asserts git toplevel equals its scratch clone, checks FETCH_HEAD equals pin,
# reads 89 chosen blobs with git cat-file --batch, and verifies every git blob SHA-1.
export TMPDIR=/fast/scratch/hyaku/kengaku-r52/C1ScoutVacuity/tmp
python3 /fast/scratch/hyaku/kengaku-r52/C1ScoutVacuity/probe.py
```

A prior probe-script attempt fetched the GitHub recursive-tree API and stopped on its HTTP 403 rate-limit response; no result from that failed attempt was used. The successful run used only the pinned git objects. No tools were installed or updated.

## Produced files

- `/fast/scratch/hyaku/kengaku-r52/C1ScoutVacuity/probe.py` — reproducible read-only probe and AST classifier.
- `/fast/scratch/hyaku/kengaku-r52/C1ScoutVacuity/summary.json` — summary and six marker-defined candidates.
- `/fast/scratch/hyaku/kengaku-r52/C1ScoutVacuity/per-task.jsonl` — all 89 task records, grader path, SHA-256 and git blob verification, classes, markers, assert counts and located existence asserts.
- `/fast/scratch/hyaku/kengaku-r52/C1ScoutVacuity/graders/` — all 89 primary grader bytes.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutVacuity/summary.json`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutVacuity/per-task.jsonl`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutVacuity/report.md`
