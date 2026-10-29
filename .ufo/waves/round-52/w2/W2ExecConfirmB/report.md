# W2ExecConfirmB — second independent reader, first five C1 CANDIDATE rows

Attacked: the C1 triage queue's first five rows (bn-fit-modify, build-cython-ext, caffe-cifar-10, cancel-async-tasks, code-from-image).
Command: `python3 plans/round52_c1_grader_audit.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` (CANDIDATES total=29; first five rows as above). Read each `corpus/evidence/round52/graders/<task>/tests/test_outputs.py` in full (`cat -n`), without opening W2ExecConfirmA's receipts. Each quote was checked in Python to be a verbatim substring of the captured grader and to sit at the stated line.

Result: 5 receipts written, 0 refusals (5/5 candidates have a presence-only test). Attack on the instrument's candidate flags: failed to land for these five (all true positives).

| task | test | line | quote | note |
|---|---|---|---|---|
| bn-fit-modify | test_bn_sample_exists | 17 | `assert bn_sample_path.exists(), ...` | also presence-only: test_learned_dag_structure_exists (l.24), test_intervened_dag_structure_exists (l.62). Later tests in the file read the same files and compare content. |
| build-cython-ext | test_repo_cloned | 33 | `assert path.exists(), ...` | body is exists / is_dir / (path/.git).exists() (l.33-35): presence and type only; a bare `mkdir -p /app/pyknotid/.git` passes it. Other tests in the file are behavioural. |
| caffe-cifar-10 | test_prototxt_files_exist | 51 | `assert solver_file.exists(), ...` | l.51-52 are two exists asserts, nothing else. Note test_cifar10_model_exists (l.27) is NOT presence-only (size>100000, header read) despite its name. |
| cancel-async-tasks | test_run_py_file_exists | 14 | `assert run_path.exists(), ...` | single assert; the remaining 5 tests are subprocess-behavioural. |
| code-from-image | test_output_file_exists | 15 | `assert output_path.exists(), ...` | single assert; test_output_is_correct (l.18) compares the full sha-like string. |

Caveat: per-test presence-only vacuity is a weakness of the individual test, not of the whole grader: in all five the same grader also contains content/behaviour tests that cover the artefact, so the whole-task pass condition is not vacuous. This matches Amendment A1's own per-test framing.

Files: /fast/scratch/hyaku/kengaku-r52/w2-W2ExecConfirmB/confirmations.json (copied to /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ExecConfirmB/confirmations.json); scratch removed.
Tools installed: none.
