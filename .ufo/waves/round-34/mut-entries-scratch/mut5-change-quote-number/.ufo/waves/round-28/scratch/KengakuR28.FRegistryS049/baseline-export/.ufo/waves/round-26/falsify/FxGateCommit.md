# FxGateCommit — selected-revision timing falsification

Axes: calibration (Q13); novelty/coverage unchanged. Scope: `plans/gate_timing_check.py`, `corpus/QUALITY.md:97-109`, and the candidate `corpus/knowledge/grader-perturbation-audit.md` only. Integration receipt: `.ufo/waves/round-26/integration-revision.txt` names `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; checker SHA-256 observed: `4a270d3ca31ddd64b829a079f96aadfad088e97c9b197630d0c31ede0a138512`.

## Finding — HIGH: `--commit` is caller-selected, not verified as the admission commit

At `plans/gate_timing_check.py:541,568,580,596`, the CLI accepts a revision string and uses that same value for `git show`/`git ls-tree`; it has no admission-event identity input or validation. Thus it checks the selected tree, not whether that revision is where the candidate was actually admitted. Reproduction used only a disposable Git repo and the current checker; candidate/Gate stayed admitted between the two tested commits.

Reproduce: `python3 /tmp/fxgatecommit_repro.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py`
Scratch repo: `/tmp/fxgatecommit-sbx-ykggany6`; actual-admission fixture commit `05d03ce983520e79a70544afafcf228ec4463b20`; later report commit `921b91570938104eda5887c4642938354c25fcb7`.

Observed checker runs (the script prints full commands):
- `--repo /tmp/fxgatecommit-sbx-ykggany6 --lesson corpus/lessons/round-26.md --commit 05d03ce983520e79a70544afafcf228ec4463b20` → `FAIL`; cited report absent from this tree; `passed=0 failed=1`; exit **1**.
- Same command with `--commit 921b91570938104eda5887c4642938354c25fcb7` → `PASS`; later-added cited report exists and is registered/returned; `passed=1 failed=0`; exit **0**.
- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --selftest` → `[selftest] ALL PASS`; exit **0**.

The counterexample establishes a structural limit: supplying the later tree can turn a failing actual-admission tree green. It does not show that an operator who supplies the authentic landing SHA gets a wrong tree result. To rely on Q13, independently establish the admission SHA, then pass that SHA; checker PASS alone cannot prove the argument is that SHA.

## Q13 wording and current admission state

`corpus/QUALITY.md:101-107` says to run with `<admitting commit>` and describes tree-based timing evidence; this is a caller precondition, not an identity check implemented by the tool. Keep any Q13 summary bounded to “the selected commit tree contains the cited report”; do not say this checker establishes that the selected commit is the admission commit. Existing `.ufo/waves/round-26/build/ExecGateTimingCheck.md:4` accurately says “as of the supplied commit.” The round-26 Gate is still `deferred` (`corpus/lessons/round-26.md:29-34`), and the integration receipt says the knowledge entry is draft-only (`integration-revision.txt:5`); this synthetic result is not evidence of a real admission.

## Verification and residual risk

LSP is unavailable (`read xd://lsp` returned “No such tool”; no LSP status/references/definition/diagnostics server mounted). Findings above are direct reads and controlled scratch execution, not grep-based semantic proof. Python 3.14.8 and Git 2.56.0 were present; no installs/updates. Only `/tmp/fxgatecommit_repro.py`, `/tmp/fxgatecommit-sbx-ykggany6`, and this report were written; no live lane Git/jj operations or production edits.

VERDICT: Q13 tree checking is conditional on independently supplying the actual admission revision; later-tree PASS does not establish admission-time support.