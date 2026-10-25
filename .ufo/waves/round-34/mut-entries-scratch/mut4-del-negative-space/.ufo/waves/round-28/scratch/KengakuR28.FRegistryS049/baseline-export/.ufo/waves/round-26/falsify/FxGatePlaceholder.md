# FxGatePlaceholder — Q13 report-support falsification

Axes: calibration (Q13); novelty/coverage unchanged. Scope: `plans/gate_timing_check.py` and `corpus/QUALITY.md:97-107`, in scratch Git only. Tested integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`.

## Finding — HIGH: Q13 accepts non-reviewer report seats

Q13 requires a nonempty regular report from a registered reviewer-like seat (`corpus/QUALITY.md:105-106`). `plans/gate_timing_check.py:328-329` rejects only `scribe` and `executor`; other roles are accepted. The round-26 falsify registry contains `connector`, `critic`, `scout`, and `mutation-tester` seats as well as `reviewer` seats. A registered `connector` report naming `knowledge/grader-perturbation-audit.md` and carrying `VERDICT: PASS` therefore falsely satisfies the gate.

Reproduction harness: `/tmp/kengaku-r26-gate-fxplaceholder.AiekC5/q13_falsify.py`; sandbox checker cloned at `/tmp/kengaku-r26-gate-fxplaceholder.AiekC5/repo/plans/gate_timing_check.py` from integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`. Run `python3 /tmp/kengaku-r26-gate-fxplaceholder.AiekC5/q13_falsify.py` → `HARNESS_RESULT=MISMATCH`, exit **1** (expected because non-reviewer rejection cases pass). Each fixture commits the Gate admit of `knowledge/grader-perturbation-audit.md`; the harness prints the exact CLI command and result.

| Fixture commit / role | Checker output | Exit |
|---|---|---:|
| `624e1876141baea4bf2405580e5da69204b6aa2f` / reviewer, empty blob | `invalid cited ... (mode=100644, size=0)`; `passed=0 failed=1` | 1 |
| `f43982d7ab64bb99487a49aa40d0d48b2efbddc5` / unregistered seat | `seat is not in the committed wave registry`; `passed=0 failed=1` | 1 |
| `fa21fa6ae6dd170045dc548d2ba074da8433d86f` / reviewer, symlink | `invalid cited ... (mode=120000, size=16)`; `passed=0 failed=1` | 1 |
| `3f728bab4f631de1b6b240adee2ca560a9bb7b77` / connector | `PASS ... passed=1 failed=0` | **0** |
| `1d9d7f485acb343c1bf0cf52ab97e86fbb123b11` / critic | `PASS ... passed=1 failed=0` | **0** |
| `976d96b38ac75186eaeec578402ff7e2ad5c18d4` / scout | `PASS ... passed=1 failed=0` | **0** |
| `510b3dbeb7578fdadf9dd6178218512aab20be1b` / mutation-tester | `PASS ... passed=1 failed=0` | **0** |

A valid registered reviewer control passed (commit `f0102b3f9826c37162d4bbb60d402e73c11da9a6`, exit 0). A late-report pair behaved tree-wise: cited report absent at `3c8ea38ff05413a1c6b9aad1c6e3db6c579319e6` → FAIL/exit 1; after report was added at `1a5678cd6fcac78180cb7bb2c7c3f4e2a5ee5606` → PASS/exit 0. `python3 /tmp/kengaku-r26-gate-fxplaceholder.AiekC5/repo/plans/gate_timing_check.py --selftest` → `[selftest] ALL PASS`, exit 0; its fixtures do not include a registered non-reviewer role.

## Residual risk and verification gaps

The checker validates the caller-selected `--commit` tree; the late-pair confirms a later tree can pass, so the actual admission SHA must be established independently. Round-26 Gate is currently `deferred` and the receipt says the knowledge entry is draft-only (`corpus/lessons/round-26.md:29-34`; `.ufo/waves/round-26/integration-revision.txt:5`): no real admission was exercised. LSP is unavailable: `read xd://lsp` returned “No such tool”; no LSP status/references/definition/diagnostics server was mounted. No production or lane Git/jj files were changed; no tools installed.

VERDICT: Q13 has a surviving false-pass: registered non-reviewer seats satisfy the current report-role check; empty, unregistered, and symlink controls correctly fail in the scratch trees.