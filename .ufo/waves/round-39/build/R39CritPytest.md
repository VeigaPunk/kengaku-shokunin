# R39CritPytest — real pytest 8.4.1 parity over the 25 frozen git-leak-recovery states

Seat: R39CritPytest (critic), round 39 wave 1. Lane under test: `kengaku-shokunin` @ 750473847af9c7a461487ba3a589b5519fac5ed8
(shared clone). Frozen references were read, never written.

## 1. Assignment and what ran

Asked: run the *real* pytest 8.4.1 (uv venv, CPython 3.13) over the captured grader
`corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py` for all 25 case states of `plans/git_leak_probe.py`,
inside the probe's own bubblewrap sandbox, and compare per-test letters with
`corpus/evidence/round39/git-leak-probe.txt` (sha256 `d7f3a465ccc411572c96fc039235854093d1eb52ccd685b618a28a10de609b5f`).

Done exactly that. The frozen probe (sha256 `4961a50f28ae85e8d8b687d3623aef29b59d4db14c0e62e5244e48cfef8cf68c`, byte-identical
in the clone) was copied to `plans/git_leak_probe_pytest.py` inside my scratch clone and given **three** surgical
changes, nothing else:

1. bind the venv and the uv CPython install read-only into the existing sandbox:
   `argv += ["--ro-bind", str(VENV), "/venv", "--ro-bind", str(UV_PY_ROOT), str(UV_PY_ROOT)]` (inserted after
   `--dir /cap`); the sandbox's `/usr/bin/python3` is untouched.
2. harness grading step replaced: instead of `importlib`-loading `/cap/test_outputs.py` and calling the five
   functions, run `["/venv/bin/python", "-m", "pytest", "/cap/test_outputs.py", "-rA", "--tb=no",
   "-p", "no:cacheprovider"]` with `cwd="/app"` and the probe's own env, then map `PASSED`/`FAILED`/`ERROR`
   short-summary lines back to the five `TEST <name> P|F` lines so the untouched `main()` comparison and
   `cases=` summary still work.
3. `import importlib.util` dropped from the harness (unused).

Everything else — cases, recipes, setup staging, bwrap mounts (`--unshare-net/pid/ipc`, ro `/usr` `/etc`, tmpfs
`/tmp`, writable `/app`, `/cap` with only the three pinned captures, `GIT_CONFIG_NOSYSTEM=1`,
`GIT_CONFIG_GLOBAL=/dev/null`), the letter convention, and the receipt format — is the frozen code.

Instrument copy for audit: `.ufo/waves/round-39/build/R39CritPytest/git_leak_probe_pytest.py`
(scratch sha256 `9bc5780ba1a88622e7760d81acd809fe78b9a0bdee548f53c82751481c393f1d`).

Commands (scratch `S=/fast/scratch/hyaku/kengaku-r39/R39CritPytest`, `TMPDIR=$S`):

```
git clone -q --shared <lane> "$S/lane"          # rev-parse --show-toplevel == "$S/lane" checked
uv venv -p 3.13 "$S/venv"                        # CPython 3.13.16
uv pip install --python "$S/venv/bin/python" pytest==8.4.1   # + pluggy 1.7.0, pygments 2.21.0
KENGAKU_PYTEST_VENV="$S/venv" python3 plans/git_leak_probe_pytest.py --lane "$S/lane" --work "$S/work"
KENGAKU_PYTEST_VENV="$S/venv" python3 plans/git_leak_probe_pytest.py --lane "$S/lane" --work "$S/work2"   # 2nd run
python3 plans/git_leak_probe.py --lane "$S/lane" --work "$S/work3"                                        # live ref
```

Environment: uv 0.13.0, CPython 3.13.16 (uv-managed), pytest 8.4.1, pluggy 1.7.0, bubblewrap 0.13.1, git 2.56.0.
No tool was installed into the host (uv was already present); the venv lives only in scratch.

## 2. Result — 25/25 per-test vectors agree

`tests=` is the five-letter vector in the probe's `TESTS` order; `overall` is pass iff all five are `P`.

| case | frozen tests | pytest tests | agree | frozen/pytest overall |
|---|---|---|---|---|
| empty-app | FFFFF | FFFFF | yes | fail/fail |
| untouched | FPPPP | FPPPP | yes | fail/fail |
| oracle-solve-sh | PPPPP | PPPPP | yes | pass/pass |
| echo-only | PPPPP | PPPPP | yes | pass/pass |
| echo-reflog-expire | PPPPP | PPPPP | yes | pass/pass |
| echo-gc-only | PPPPP | PPPPP | yes | pass/pass |
| clean-echo | PPPPP | PPPPP | yes | pass/pass |
| dangling-secret-blob | PPPFP | PPPFP | yes | fail/fail |
| dangling-secret-commit | PPPFP | PPPFP | yes | fail/fail |
| branch-keeps-leak | PFPPP | PFPPP | yes | fail/fail |
| blob-ref-keeps-secret | PPPPP | PPPPP | yes | pass/pass |
| tag-message-secret | PPPPP | PPPPP | yes | pass/pass |
| commit-message-secret | PFPPP | PFPPP | yes | fail/fail |
| notes-secret | PFPPP | PFPPP | yes | fail/fail |
| stash-secret | PPPPP | PPPPP | yes | pass/pass |
| dotfile-in-worktree | PPPPP | PPPPP | yes | pass/pass |
| untracked-file-secret | PPPPF | PPPPF | yes | fail/fail |
| config-secret | PPPPP | PPPPP | yes | pass/pass |
| readme-edited | PPPPF | PPPPF | yes | fail/fail |
| message-rewritten | PPPPP | PPPPP | yes | pass/pass |
| history-rebuilt | PPPPP | PPPPP | yes | pass/pass |
| flag-extra-text | FPPPP | FPPPP | yes | fail/fail |
| flag-padded-crlf | PPPPP | PPPPP | yes | pass/pass |
| flag-is-directory | FPPPP | FPPPP | yes | fail/fail |
| flag-in-repo-only | FPPPF | FPPPF | yes | fail/fail |
| **totals** | 13 pass / 12 fail | 13 pass / 12 fail | **25/25** | `mismatches=0` both |

Both receipts end `cases=25 observed_pass=13 observed_fail=12 mismatches=0`; the pytest run adds
`PYTEST rc=<0|1>` per case inside the harness stdout (rc 0 exactly on the PPPPP rows), which the frozen `main()`
does not print.

## 3. Determinism and live-reference cross-check

- My instrument run 2 is **byte-equal** to run 1 (`cmp` clean) — no object ids, paths or timings leak into the output,
  same guarantee the frozen probe claims.
- Re-running the **frozen** probe live in the same scratch produced output **byte-equal to the frozen receipt**
  (`cmp` clean), and its per-case letters match both the receipt and pytest 25/25. So pytest does not merely agree
  with a stale text: it agrees with a fresh run of the import-based harness on this host state.

## 4. Critic notes (limits, counterexamples tried, what would falsify)

- **Letter granularity only.** The import-based harness records the exception class for non-assertion failures
  (`flag-is-directory ... test_flag_file_exists_and_correct:error=IsADirectoryError`, receipt line 28); pytest's
  short summary records only `FAILED`. So the parity claim is exact for the P/F vectors — the comparison unit the
  C2 receipt and the requirement map use — and slightly lossy for that one annotation. No aggregate (13/12,
  `mismatches=0`, per-tag labels) depends on the class name.
- **Why the apparatus change cannot move a verdict here.** The grader has no fixtures, parametrization, module-level
  state, or side effects at import (`cat corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py:1-113`: only
  `subprocess`/`pathlib` imports and five plain test functions). pytest therefore runs exactly the same five
  functions in file order that the harness calls; the two red-letter cases (`empty-app`, `flag-is-directory`) confirm
  that both an assertion failure and a raised non-`AssertionError` map to `F` under pytest.
- **Ordering hazard tested and absent.** `test_repository_contents_checksum` runs last and hashes the work tree;
  pytest is the only new writer in `/app`, so `-p no:cacheprovider` plus the inherited `PYTHONDONTWRITEBYTECODE=1`
  is load-bearing. If a future grader run showed `untracked-file-secret`-style checksum failures on otherwise clean
  states, that flag pair is the first suspect. With the flags as run, all five checksum rows match.
- **Sandbox fidelity.** The venv (pytest + pluggy + pygments, ~15 MB of site-packages) is mounted read-only at
  `/venv`, and the uv CPython tree read-only at its real path so `pyvenv.cfg`'s `home` resolves; `/cap` remains the
  only grader source and stays read-only, so the checksum test cannot be contaminated. The task image is still not
  pulled — the pytest apparatus is host pytest 8.4.1 on CPython 3.13.16, the same versions `environment/tests/test.sh`
  pins (`-p 3.13 -w pytest==8.4.1`).
- **Scope not claimed.** This checks grader evaluation only; it says nothing about the Ubuntu-24.04/root/dash
  differences or about agent behaviour, and it does not re-derive the requirement-map labels.

## 5. C2 implication

The pinned grader's verdicts, as a real pytest run computes them, are identical to the frozen receipt's 25 per-test
vectors, so the receipt's 13-pass/12-fail split and the `violates=` tags that wave-1 requirement labelling derives
from it survive the strongest cheap substitute available for the task image's `uvx ... pytest` step.

VERDICT: pytest-parity-25/25
