# W2ExecEntryDraft — independent audit of the 29 C1 candidates (R52-C1)

## What I attacked
The 29 `CANDIDATES` printed by `plans/round52_c1_grader_audit.py` at the landed tree, without using any wave-2 confirmation. For each I opened the captured bytes under `corpus/evidence/round52/graders/<task>/tests/test_outputs.py`, located the P1 test and its assert line, and recorded what else the same grader checks.

## Commands
- `python3 plans/round52_c1_grader_audit.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` (receipt `counter.out`): `TASKS 89 records=89 classified=88`, `CAPTURES expected=184 present=183 mismatched=0`, `CLASS V1=2 V4=0 V2=53 V3=31 V0=3`, `TESTCLASS presence_only_tests=33 tasks_with_presence_only=27`, `CANDIDATES total=29`, `CONFIRMED new=0`, `PRIOR-ART ok=False urls=0`, `PREDICATE R52-C1 fail`, `PREDICATE R52-C1-A5 fail` (expected: no confirmations or prior-art files in the tree at my read time).
- `ast_cmp.py` (independent classifier: AST of each top-level `test_*` function; P1 = every assert is only exists/is_file/is_dir/isfile/isdir calls, no comparison, no other call except Path/join/str/setup()) over all 88 captured primary graders. `why.py` prints which regex token flipped each disagreement. `build.py` writes the JSON. Hand reads of every P1 block (`p1.py`-style dump with line numbers) and of all assert lines of every candidate grader.

## Numbers
- Candidates: **29**. Candidates unread by the lane before round 52: 27 (`db-wal-recovery` and `password-recovery` have lane hand-read entries `tb2-*-grader.md`).
- Tasks with a **verified presence-only test: 28 of 29** (every candidate except `hf-model-inference`).
- Counter-vs-independent test counts: top-level test functions 305 (counter `test_count` also 305). Counter P1 = 33; independent AST P1 = **47** across 38 tasks (counter: 27).
- **Whole-grader limit**: in all 29 candidates a P1 test is a test-level finding. None of the 29 graders is presence-satisfiable as a whole: each also has at least one content, behaviour or value test (per-candidate list in the JSON, `what_else_grader_checks`). Closest to thin: `pytorch-model-cli` (3 of 6 tests presence-only, 3 compare output), `bn-fit-modify` (3 of 9), `sam-cell-seg` (2 of 9, plus a subprocess run).

## Counter-classification disagreements (found, all by quoting bytes)
1. **False P1:** `hf-model-inference::test_model_downloaded` (lines 8-22) asserts the dir exists **and** does `from_pretrained` for model + tokenizer — a load check, not presence-only. Counter P1 because `from_pretrained`/`is not None` match neither BEHAV_T nor VALUE. Candidate status for this task is unsupported (its only P1 is false).
2. **Missed presence-only (counter said P3/P2), inside the candidate set (3 tests):** `pytorch-model-recovery::test_model_file_exists` (103-108, assert line 108), `torch-tensor-parallelism::test_parallel_linear_exists` (18-25, assert line 25), `financial-document-processor::test_summary_csv_exists` (100-103). Both pytorch tasks are in `CANDIDATES` **only through the file-level V1 rule** (their `presence_only` column is `-`), so the A1 narrative (per-test candidate) is not what the counter shows for them.
3. **Missed presence-only, outside the candidate set (10 tasks, 12 tests):** circuit-fibsqrt, extract-moves-from-video, fix-code-vulnerability, gcode-to-text, llm-inference-batching-scheduler, merge-diff-arc-agi-task (2 tests), sparql-university, torch-pipeline-parallelism, tune-mjcf, video-processing (2 tests). Listed with def line numbers in `non_candidate_counter_misses`.
   *Root causes (measured with `why.py`):* (a) `VALUE` contains `\bin\b`, which matches the English word "in" in docstrings and comments ("exists in the current directory", "the WORKDIR in the Docker env") → P3; (b) `split_tests` cuts only at `^def test_`, so helper `def _x` and comment blocks that follow a test are folded into its block (`torch-tensor-parallelism`: `dist.init_process_group` → P2; `tune-mjcf`: `np.` from a helper → P3; `llm-inference-batching-scheduler`: `>` from a `-> None` annotation → P3); (c) the assert may live in a helper (`torch-tensor-parallelism` real tests labelled P0).
   Direction: counter undercounts presence-only tests (33 vs 47), with one overcount.

## Does the attack land?
- On "29 candidates are verified": lands partly — 28/29 verified; `hf-model-inference` is a counter false positive.
- On counter fidelity: lands — 1 false P1 and 15 missed P1 tests (3 in candidate tasks, 12 in 10 non-candidate tasks; 33 - 1 + 15 = 47), so the per-test rule is a lexical approximation, not a verdict.
- Not a whole-grader finding for any candidate; a confirmation must quote the weak test, not claim the grader is vacuous.

## Files
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ExecEntryDraft/candidate-audit.json` (one record per candidate: grader path, sha256, bytes, P1 test with def/assert line and quote, other tests, what else the grader checks, whole-grader verdict, disagreements; plus `non_candidate_counter_misses`)
- same dir: `counter.out`, `ast_cmp.py`, `why.py`, `build.py`.
- Tools installed: none. No edits outside my scratch and wave dir; scratch removed.
