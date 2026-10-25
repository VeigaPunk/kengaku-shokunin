# FxP3CBox1 — P3c Box 1 whole-file content-pin mutation

Round 26 attempt 1; 2026-10-21; advisory falsification, not an admission or outside verification.
Axes: calibration (does the frozen pin fail on content loss), specificity (P2 stays unchanged), isolation (scratch only).
Scope: `plans/state_check.py` P3c Box 1 `SKILL.md` whole-file pins. Read `plans/round-26-claims.md` through Amendment 2, `corpus/lessons/round-26.md`, the draft, and `integration-revision.txt`.
Integrated snapshot: `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; scratch export: `/tmp/kengaku-r26-FxP3CBox1-9d7c61`.

## Evidence and commands

- `P3C_PINS` declares four Box-1 whole-file tokens (`state_check.py:218-222`); `check_p3c` counts target-file tokens and emits `.needle.N` IDs (`:1472-1493`). The registered requirement is claims `:134-146`.
- LSP status/references/definition/diagnostics unavailable: `read xd://lsp` returned `No such tool`; no semantic LSP result is claimed. Literal source reads/search were used only as fallback.
- `test ! -e /tmp/kengaku-r26-FxP3CBox1-9d7c61 && mkdir -p /tmp/kengaku-r26-FxP3CBox1-9d7c61 && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive --format=tar 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 | tar -x -C /tmp/kengaku-r26-FxP3CBox1-9d7c61` → exit 0, no output.
- `python3 -B /tmp/kengaku-r26-FxP3CBox1-9d7c61/plans/state_check.py --selftest` → exit 0; output includes `selftest ok P3c: red mutation (P3c.box.3.pointer.1)` and `[selftest] ALL PASS`.
- Pristine: `python3 -B /tmp/kengaku-r26-FxP3CBox1-9d7c61/plans/state_check.py --json > /tmp/kengaku-r26-FxP3CBox1-9d7c61/pristine.json` → checker exit 1. Summary: 275 assertions, 267 match, 2 mismatch, 3 offline_unverifiable, 17 out_of_population, 3 superseded. All four Box-1 P3c needle IDs and `P2c.box.1.pointer.1` were MATCH. P2: 252 records, 0 mismatch, SHA-256 `269450e0a362faa68393c590059e00d2830bf3629929f5ceadb3a7c169dce641`.
- Scratch-only mutation: removed `SKILL.md:23`, `## Decision table — benchmark selection`; no checker/P2 input changes.
- Mutant: `python3 -B /tmp/kengaku-r26-FxP3CBox1-9d7c61/plans/state_check.py --json > /tmp/kengaku-r26-FxP3CBox1-9d7c61/mutated.json` → checker exit 1. Summary: 275 assertions, 266 match, 3 mismatch, 3 offline_unverifiable, 17 out_of_population, 3 superseded.
- Mutant JSON: `P3c.box.1.pointer.1.needle.1` = MISMATCH, `target=SKILL.md:whole-file`, `token_hits=0`; Box-1 needle.2/.3/.4 remain MATCH with `token_hits=1`. The range-only `P2c.box.1.pointer.1` remains MATCH (`exists=true`, `anchor=null`).
- `python3 -B /tmp/kengaku-r26-FxP3CBox1-9d7c61/compare_p2.py /tmp/kengaku-r26-FxP3CBox1-9d7c61/pristine.json /tmp/kengaku-r26-FxP3CBox1-9d7c61/mutated.json` → exit 0: `P2_records_identical=True baseline=252 mutant=252`; `P2_changed_ids=[]`; sole verdict delta is `P3c.box.1.pointer.1.needle.1 MATCH → MISMATCH`.

## Findings and residual risk

No defect in the tested P3c Box-1 runtime behavior: removing its required heading makes the correct content-pin assertion red while the P2 path/range assertion stays green and the full P2 population is byte-for-byte record-identical. The integrated pristine run itself is not clean: its two existing P3b mismatches are `P3b.province.public-literature-registry.rows` (`PROVINCE.md:112`) and `P3b.province.round25-correction.rows` (`:119`); outside this slice.

Residual test-coverage gap: `--selftest` only mutates `P3c.box.3.pointer.1` (`state_check.py:2031-2037`), so it does not regression-test the whole-file Box-1 branch. This direct scratch mutation validates the present behavior, not that missing selftest case.

VERDICT: SCOPED PASS — Box-1 content loss is detected by the intended P3c assertion; P2 is unchanged. Not a whole-checker pass or admission recommendation.