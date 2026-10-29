# C1ConfReadD — R53-C1 CONFIRM leg, second reader (wave 2)

Tasks of this group (all four read in full, never read before by the lane): `gcode-to-text`, `mteb-leaderboard`, `pytorch-model-recovery`, `tune-mjcf`.
I read only the captured `tests/test_outputs.py` and `tests/test.sh` of each task (`corpus/evidence/round52/graders/<task>/tests/`), `p1-spec.md`, `facts.md`, the claims file and
`tests-index.json` spans. I did not open any label file, the classifier, or any `C1Label*/C1Exec*/C1Crit*/C1Mut*` output.
Instructions fetched with `curl -sL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<task>/instruction.md` (pin 2fd12b88), saved under `.ufo/waves/round-53/w2/C1ConfReadD/<task>.instruction.md`.
All four `test.sh` files are the stock harness (install uv, run pytest with `--ctrf`, write reward 1/0 from pytest's exit); none adds a check. Each task runs all tests in the file, so reward needs every test to pass.

| task | test id | instruction asks for | confirmed | quote (line) | rest of the grader |
|---|---|---|---|---|---|
| `gcode-to-text` | `gcode-to-text::test_hello_file_exists` | Work out what text a Prusa MK4s print of `text.gcode` would show and write it to `/app/out.txt`. | true | `assert hello_path.exists(), f"File {hello_path} does not exist"` (10) | `test_hello_file_content` (same file) reads the file and compares with the exact flag string: real content check. |
| `mteb-leaderboard` | `mteb-leaderboard::test_result_exists` | Name the top Scandinavian-MTEB model (Mean (Task), Aug 2025) in `org/name` form into `/app/result.txt`. | true | `assert os.path.exists("/app/result.txt"), "result.txt file does not exist"` (7) | `test_data_matches` reads the file, needs one line equal to `GritLM/GritLM-7B`: real content check. |
| `pytorch-model-recovery` | `pytorch-model-recovery::test_model_file_exists` | Recover the architecture from `weights.pt`, retune only `output_layer`, save a TorchScript model to `/app/model.pt`. | true | `assert hello_path.exists(), f"File {hello_path} does not exist"` (108) | `test_weights_file_unchanged` (torch.load, allclose vs ground truth), `test_model_loads_weights` (jit.load + load_state_dict), `test_state_dicts_match` (keys and allclose except output_layer), `test_model_loss` (agent MSE < original MSE): four real checks. |
| `tune-mjcf` | `tune-mjcf::test_tuned_model_exists` | Tune the MuJoCo MJCF so it simulates in <= 60 % of the reference time with the same final state, saved as `/app/model.xml`. | true | `assert model_path.exists(), "Tuned model file does not exist"` (28) | `test_model_ref_unchanged` (text compare), `test_correctness` (final-state allclose atol 1e-5), `test_model_speed` (time ratio <= 0.6): three real checks. |

## Reasoning per task (spec section "Y requires all of")
- Reach: each named test body is one `assert` on a path-existence call; no helper, no fixture, no subprocess, no read, no size/value comparison. `pytorch-model-recovery` and `tune-mjcf` import `torch` / `mujoco` / `numpy` at module top, but those are library imports (not the task's deliverable) and run at collection, not in the test; module-level constants (`app_dir`, `test_dir`) in `tune-mjcf` are plain Path values. Creating the named file (`touch /app/out.txt`, `/app/result.txt`, `/app/model.pt`, `/app/model.xml`) satisfies the test; arbitrary or empty content passes.
- I looked for anything the classifier could have missed (decorators, autouse fixtures, conftest, parametrisation, `test.sh` post-checks): none exist in the captured files; no `conftest.py` captured in any of the four task dirs (`ls -R` shows only `tests/test.sh`, `tests/test_outputs.py`). Uncaptured files that the tests reference (`/tests/weights_gtruth.pt`, `/tests/model_ref.xml`) are only read by the sibling tests, not by the named ones. So `confirmed: true` for all four.

## Weakness bound (not overstated)
Each presence-only test sits beside at least one real content or behaviour check in the same file, so the task's grader as a whole is not presence-only: the weakness is that one test (a redundant existence gate), and an agent that only creates the file still fails the content test and gets reward 0. Two or three P1 tests per task: none seen in this group beyond the one named test per task (I did not enumerate other tests as P1 for these tasks: all other tests read content or run code).

## Commands run
- `cat -n` of the four `test_outputs.py` and `test.sh` under `corpus/evidence/round52/graders/<task>/tests/`.
- `python3` check that each quote is >= 20 chars, lies in a single source line inside the `tests-index.json` span (6-10, 6-7, 103-108, 25-28) and that each `why` is <= 30 words; then wrote `.ufo/waves/round-53/w2/C1ConfReadD/confirmations-part.json`.
- No scratch clone or fixture was needed; nothing under `/fast/scratch` was created. No tools installed.

## Files
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w2/C1ConfReadD/confirmations-part.json` (4 objects, reader `C1ConfReadD`, all `confirmed: true`)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w2/C1ConfReadD/<task>.instruction.md` (four fetched instructions)
