# R45PytestParity — real pytest parity

Axes: coverage (16/16 case states staged and graded); per-test-letter parity (14/16 exact matches).

## Method and evidence

Read the frozen claim file in full and followed the probe's `CASES`, `HARNESS_PY`, capture setup, seed, recipe, and `sandbox_argv` from `plans/password_recovery_probe.py`. For every case, created a fresh work directory under `/fast/scratch/hyaku/kengaku-r45/R45PytestParity/cases/<case-id>`, then ran the probe's stage harness inside its bubblewrap sandbox. Ran the captured `tests/test_outputs.py` with real pytest `-v` in a second bubblewrap sandbox over that same staged `/app` and captured `/tests`. The actual pytest environment was CPython 3.13.16 / pytest 9.1.1; `-p no:cacheprovider` disabled pytest cache writes. Both sandboxes were inside the required envelope; its `/home/vgpnk` was read-only and `~/.local/bin` remained unchanged.

**Final run envelope:**
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45PytestParity/env /fast/scratch/hyaku/kengaku-r45/R45PytestParity/env --bind /fast/scratch/hyaku/kengaku-r45/R45PytestParity/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r45/R45PytestParity/parity.py
ENVELOPE start 23:30:06 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 23:30:15 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

**Pytest runtime provisioning envelopes:** `uv venv --python 3.13 /fast/scratch/hyaku/kengaku-r45/R45PytestParity/pytest-venv` exited 0 at 23:28:29; `uv pip install --python .../pytest-venv/bin/python pytest` exited 0 at 23:28:33. Both had `local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged`. Installed in scratch: pytest 9.1.1, pluggy 1.7.0, pygments 2.21.0, packaging 26.3, iniconfig 2.3.1. Python 3.13.16 was available through existing uv Python; no shared PATH installation was made. An initial uvx attempt tried writing its default tool directory under read-only home and exited 2; redirected uv locations to scratch for successful setup. An initial parity-driver import and an initial pytest launch also failed before producing test verdicts; fixed the driver import registration and runtime mount, then the complete final run above passed all staging and test launches. These failures are not counted as observations.

The frozen receipt `corpus/evidence/round45/password-recovery-probe.txt` was not present at the specified path when checked. Thus comparisons below use `corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` only. Its 16 `tests=` predictions are cited as `dry` below.

## Per-case pytest -v output vs frozen probe letters

Each pair is the actual pytest verbose node line status, in test order (`test_recovery_file_exists`, `test_password_match`); `rc` is pytest's process exit code. The filenames and statuses are the captured grader's pytest output. The staged command printed `STAGE seed rc=0` and `STAGE recipe rc=0` for all 16 cases.

| Case | pytest -v node statuses | pytest letters / rc | dry letters | Match |
|---|---|---:|---:|:---:|
| nop | `../tests/test_outputs.py::test_recovery_file_exists FAILED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | FF / 1 | F- | no |
| oracle-solve-sh | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match PASSED [100%]` | PP / 0 | PP | yes |
| constant | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match PASSED [100%]` | PP / 0 | PP | yes |
| constant-crlf | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match PASSED [100%]` | PP / 0 | PP | yes |
| constant-joined | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | PF / 1 | PF | yes |
| dir-state | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | PF / 1 | PF | yes |
| empty-file | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | PF / 1 | PF | yes |
| wrong-23 | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | PF / 1 | PF | yes |
| prefix-decoy | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | PF / 1 | PF | yes |
| sub-first | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | PF / 1 | PF | yes |
| sub-last | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | PF / 1 | PF | yes |
| lower23 | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | PF / 1 | PF | yes |
| decoys-1000 | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match PASSED [100%]` | PP / 0 | PP | yes |
| password-eq | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | PF / 1 | PF | yes |
| crlf-line | `../tests/test_outputs.py::test_recovery_file_exists PASSED [50%]`; `../tests/test_outputs.py::test_password_match PASSED [100%]` | PP / 0 | PP | yes |
| under-varsea | `../tests/test_outputs.py::test_recovery_file_exists FAILED [50%]`; `../tests/test_outputs.py::test_password_match FAILED [100%]` | FF / 1 | F- | no |

## Finding and residual risk

There are 14 exact per-test-letter matches of 16. The two mismatches are `nop` and `under-varsea`: the probe harness exits after the first test failure and represents the unreached second test as `-`; real pytest continues collecting/executing the second test, whose file read also fails, so pytest reports `FF`. Both approaches return failure (pytest rc 1), consistent with the probe's documented overall-exit-status equivalence; this is a per-test-letter divergence, not an overall reward verdict divergence. No captured receipt was available for a three-way comparison.

Verification was exercised only with the captured grader under local CPython 3.13.16 / pytest 9.1.1, not the benchmark image or its `tests/test.sh` bootstrap. The final run observed all 16 stages successful and all pytest launches completed; no other verification was run.

VERDICT: pytest-parity-14/16
