# W2ExecCounterRun — raw frozen-counter run at the lane tree as it stands (2026-10-28)

Attack: run both frozen counters + both selftests, unmodified, against the lane; report legs. Counters were not edited.
Landed? This is a measurement seat, not an attack with a target. Result: **C2 passes; C1 fails (literal and A5)**.

## Commands (cwd = my scratch dir, TMPDIR set there)
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
1. python3 $L/plans/round52_c1_grader_audit.py --lane $L          -> exit 1
2. python3 $L/plans/round52_c1_grader_audit.py --selftest         -> exit 0
3. python3 $L/plans/round52_c2_registry.py --lane $L              -> exit 0
4. python3 $L/plans/round52_c2_registry.py --selftest             -> exit 2 (`SETUP no SKILL.md under <cwd>`: it defaults --lane to "." and I ran from scratch; not a counter defect)
5. python3 $L/plans/round52_c2_registry.py --lane $L --selftest   -> exit 0

## 1. C1 full output (exit 1)
```
TASKS total=89 records=89 classified=88
CAPTURES expected=184 present=183 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=31 V0=3
TESTCLASS presence_only_tests=33 tasks_with_presence_only=27
CANDIDATES total=29
  CANDIDATE bn-fit-modify class=V3 presence_only=test_bn_sample_exists,test_learned_dag_structure_exists,test_intervened_dag_structure_exists grader=bn-fit-modify/tests/test_outputs.py
  CANDIDATE build-cython-ext class=V2 presence_only=test_repo_cloned grader=build-cython-ext/tests/test_outputs.py
  CANDIDATE caffe-cifar-10 class=V2 presence_only=test_prototxt_files_exist grader=caffe-cifar-10/tests/test_outputs.py
  CANDIDATE cancel-async-tasks class=V2 presence_only=test_run_py_file_exists grader=cancel-async-tasks/tests/test_outputs.py
  CANDIDATE code-from-image class=V3 presence_only=test_output_file_exists grader=code-from-image/tests/test_outputs.py
  CANDIDATE crack-7z-hash class=V3 presence_only=test_solution_file grader=crack-7z-hash/tests/test_outputs.py
  CANDIDATE db-wal-recovery class=V3 presence_only=test_recovered_json_exists grader=db-wal-recovery/tests/test_outputs.py
  CANDIDATE extract-elf class=V2 presence_only=test_extract_js_exists grader=extract-elf/tests/test_outputs.py
  CANDIDATE financial-document-processor class=V3 presence_only=test_directories_created grader=financial-document-processor/tests/test_outputs.py
  CANDIDATE hf-model-inference class=V2 presence_only=test_model_downloaded grader=hf-model-inference/tests/test_outputs.py
  CANDIDATE kv-store-grpc class=V2 presence_only=test_protobuf_generation grader=kv-store-grpc/tests/test_outputs.py
  CANDIDATE large-scale-text-editing class=V2 presence_only=test_apply_macros_exists grader=large-scale-text-editing/tests/test_outputs.py
  CANDIDATE log-summary-date-ranges class=V3 presence_only=test_summary_file_exists grader=log-summary-date-ranges/tests/test_outputs.py
  CANDIDATE mteb-leaderboard class=V3 presence_only=test_result_exists grader=mteb-leaderboard/tests/test_outputs.py
  CANDIDATE mteb-retrieve class=V3 presence_only=test_result_exists grader=mteb-retrieve/tests/test_outputs.py
  CANDIDATE multi-source-data-merger class=V3 presence_only=test_output_files_exist grader=multi-source-data-merger/tests/test_outputs.py
  CANDIDATE openssl-selfsigned-cert class=V2 presence_only=test_directory_structure grader=openssl-selfsigned-cert/tests/test_outputs.py
  CANDIDATE password-recovery class=V3 presence_only=test_recovery_file_exists grader=password-recovery/tests/test_outputs.py
  CANDIDATE path-tracing class=V2 presence_only=test_image_c_exists grader=path-tracing/tests/test_outputs.py
  CANDIDATE path-tracing-reverse class=V2 presence_only=test_image_c_exists grader=path-tracing-reverse/tests/test_outputs.py
  CANDIDATE prove-plus-comm class=V2 presence_only=test_proof_file_exists,test_compiled_proof_exists grader=prove-plus-comm/tests/test_outputs.py
  CANDIDATE pytorch-model-cli class=V2 presence_only=test_weights_file_exists,test_cli_tool_exists,test_prediction_file_exists grader=pytorch-model-cli/tests/test_outputs.py
  CANDIDATE pytorch-model-recovery class=V1 presence_only=- grader=pytorch-model-recovery/tests/test_outputs.py
  CANDIDATE raman-fitting class=V3 presence_only=test_result_file_exists grader=raman-fitting/tests/test_outputs.py
  CANDIDATE sam-cell-seg class=V2 presence_only=test_python_file_exists,test_csv_output_exists grader=sam-cell-seg/tests/test_outputs.py
  CANDIDATE torch-tensor-parallelism class=V1 presence_only=- grader=torch-tensor-parallelism/tests/test_outputs.py
  CANDIDATE vulnerable-secret class=V3 presence_only=test_results_file_exists grader=vulnerable-secret/tests/test_outputs.py
  CANDIDATE winning-avg-corewars class=V2 presence_only=test_warrior_exists grader=winning-avg-corewars/tests/test_outputs.py
  CANDIDATE write-compressor class=V2 presence_only=test_compressed_file_exists grader=write-compressor/tests/test_outputs.py
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
LABELS agree=0 of 0
PREDICATE R52-C1 fail
A5 EXCLUDED listed=1 digest_pinned=1 tasks=['sanitize-git-repo']
A5 CAPTURES present+pinned_excluded=184 of 184
A5 TASKS classified+excluded=89 of 89
PREDICATE R52-C1-A5 fail
exit 1
```

## 2. C1 --selftest (exit 0)
```
SELFTEST classify cases=4 failures=0
SELFTEST classify_test cases=4 failures=0
SELFTEST cases=6 failures=0
exit 0
```

## 3. C2 full output (exit 0)
```
ADVERTISED total=72
REGISTERED total=72 rows=74
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
PREDICATE R52-C2 pass
exit 0
```

## 4/5. C2 --selftest
```
# run 4 (no --lane, cwd=scratch):
SETUP no SKILL.md under /fast/scratch/hyaku/kengaku-r52/w2-W2ExecCounterRun
exit 2
# run 5 (--lane $L --selftest):
SELFTEST ok clean-fixture
SELFTEST ok missing-fixture
SELFTEST ok incomplete-fixture
SELFTEST cases=3 failures=0
exit 0
```

## Leg-by-leg: what still fails (C1)
The C1 `ok` expression (verdict(), lines ~330-340) ANDs: present==expected, mismatched==0, records==89, all 89 without error, all 89 with features, len(conf_new)>=2, pa_ok. Status:

| leg | measured | status | artefact needed |
|---|---|---|---|
| 1 CAPTURES present==184 | present=183, mismatched=0 | FAIL (by 1, literal) | `graders/sanitize-git-repo/tests/test_outputs.py` — deliberately absent per operator exclusion / A5 (GH013); do NOT re-add. Digest is pinned in SHA256SUMS; A5 line shows 184 of 184 with pinned exclusion |
| mismatched==0 | 0 | ok | — |
| 2 records==89 | records=89 | ok | — |
| 2 classified==89 (no `error`) | classified=88 | FAIL (by 1, literal) | same excluded file (the task `sanitize-git-repo` records an error as its grader is absent); A5 line: 89 of 89 |
| features for all 89 | not printed separately; inferred part of ok | not independently measured | — |
| 3 CONFIRMED new>=2 | new=0 [] | FAIL | `corpus/evidence/round52/confirmations.json` — absent from the lane tree. Needs >=2 entries {task, quote, reader, confirmed:true} for tasks not in the 12 hand-read, that are instrument candidates (29 listed, incl. 27 P1 tasks), with quote a verbatim substring of the captured grader bytes. Wave-1 candidate material exists only in `.ufo/waves/round-52/w1/C1ExecReadFindings/read-findings.json` (not integrated; I did not evaluate it) |
| 4 PRIOR-ART ok, urls>=3 | ok=False urls=0 | FAIL | `corpus/evidence/round52/prior-art.md` — absent from lane tree; wave-1 draft at `.ufo/waves/round-52/w1/C1ScoutPriorArt/prior-art.md` (not integrated; contents not checked by me) with >=3 distinct URLs |
| 5 LABELS (evidence only, not a predicate leg) | agree=0 of 0 | n/a | `corpus/evidence/round52/labels.json` — absent from the lane tree; draft at `.ufo/waves/round-52/w1/C1ExecBlindLabels/labels.json` (not integrated) |

Terminal lines: `PREDICATE R52-C1 fail` (exit 1) and `PREDICATE R52-C1-A5 fail`. A5 predicate fails too: A5 only repairs legs 1-2 (184/184 and 89/89 with the pinned exclusion); legs 3 and 4 still fail, so closing the exclusion question would not by itself flip C1. `ls corpus/evidence/round52/` shows only `graders/` (with EXCLUDED.md, SHA256SUMS, per-task dirs).

Other numbers: classes V1=2 V4=0 V2=53 V3=31 V0=3 (sum 89); presence_only_tests=33 across 27 tasks (matches A4's wave-1 re-measure P1=33/27); CANDIDATES total=29 (27 P1 tasks + 2 file-level V1 tasks `pytorch-model-recovery`, `torch-tensor-parallelism`, whose presence_only list prints `-`).

## C2
`ADVERTISED 72, REGISTERED 72 (rows=74), MISSING 0, INCOMPLETE 0, ENTRY-MISSING 0, SELFTEST-UNBACKED 0, PREDICATE R52-C2 pass`, exit 0. No failing leg. Rows=74 vs total=72 means 2 rows duplicate or share a script path (not a counter leg; not investigated).

## Files produced
- this report; scratch outputs were copied inline above and the scratch dir removed.
Tools installed: none.
