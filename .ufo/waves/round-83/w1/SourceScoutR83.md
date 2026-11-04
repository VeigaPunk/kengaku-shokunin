# SourceScoutR83

Axes: coverage and calibration. Source opening complete; no replay scoring or task-solving claim.

- **Observed, high confidence:** both pinned source URLs opened HTTP 200 on 2026-11-04. Live grader SHA256 `b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a` (935 B) is byte-identical to the round52 capture at BASE and frozen commit. Instruction SHA256 `8c3af6483e409defef9786da51f318ae2ca71afe2327b94471d2f0e2e367442c` (321 B).
- **Static inference, high confidence:** `test_output_file_exists` (:10, assert :15) and `test_output_is_correct` (:18, prefix :25, equality :28-31) predict frozen cases `missing F/F; empty P/F; correct P/P; whitespace P/P; prefix-only P/F; wrong-prefix P/F; suffix P/F; uppercase P/F`. Prefix-only reaches/fails equality after passing prefix; wrong-prefix independently fails prefix. Both legs have P/F witnesses. No grader executed by this seat.
- **Draft ready:** `SourceScoutR83/source-draft.md` contains S267 append-row bytes and Gate text, URL/access/located three-word quote. Rejected candidate: instruction as evidence of image solving, with located quote, reason and flip. Offline grader coverage is not image understanding or model execution.
- **Evidence:** `SourceScoutR83/source-receipts.json`, `live-test_outputs.py`, `live-instruction.md`, `frozen-round83-cases.json`, `static-case-derivation.json`; full findings in `SourceScoutR83/report.txt` (all relative to this report's parent).
- **Unknowns:** shared replay/counter/C2 drafts were absent at one observation; no validation of them claimed. `xd://lsp` unavailable; source/AST fallback only. Actual replay, controls and predicate scoring remain L1's responsibility. Frozen contracts unchanged; no production edits, git mutations, installs or general tests. Scratch cleaned.

Report: .ufo/waves/round-83/w1/SourceScoutR83.md
