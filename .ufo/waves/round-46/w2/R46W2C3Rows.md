# R46W2C3Rows — live C3 source-row review

## Scope and method
Reviewed S166–S172 and the C3 Gate at landing `42d5043afac952fcb43bf4798757785dd258cf85`. LSP device status route returned “Tool 'lsp' has no doc topics”; semantic references/diagnostics were unavailable. Live raw files were fetched directly from the specified `2fd12b88aafdd04a52c298e3940bcb189f9766d6` URLs and hashed with Python SHA-256. Each fetched file was byte-identical to its retained capture (7/7). Clone HEAD: `42d5043afac952fcb43bf4798757785dd258cf85`.

Command: `python3 -c 'import urllib.request,hashlib,pathlib; ...'` (fetch of seven enumerated URLs; report includes exact hashes and line counts below). The per-file output was:

| Row | Live file | SHA-256 | lines / bytes | Captured bytes identical | cited quote and assessment |
|---|---|---|---|---|---|
| S166 | `tests/test_outputs.py` | `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` | 46 / 1564 | yes | cited `:18 "assert polyglot_files == [\"main.py.c\"]"` is verbatim, 4 words; line and range 1–46 valid; kind `code`, tier A, task grader scope. `teaches` faithfully describes listing, gcc compile, and Python/C outputs across three cases. |
| S167 | `tests/test.sh` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` | 29 / 608 | yes | cited `:26 "echo 1 > /logs/verifier/reward.txt"` verbatim, 5 whitespace words (not 4 as Gate line 33 says only a quote, with no count there); line/range 1–29 valid; `code`, A, harness reward mapping scope. `teaches` accurately notes uvx/pytest 3.13 and exit-status mapping. |
| S168 | `instruction.md` | `a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96` | 9 / 339 | yes | Gate `:9 "I'm using python3 3.12.3 and gcc 13.2.0."` is verbatim, 9 words; valid line/range 1–9; `docs`, A, author request scope. Row quote at `:3` is verbatim and 3 words. `teaches` matches request. |
| S169 | `solution/solve.sh` | `e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0` | 57 / 1386 | yes | Gate `:14 "#define sdf b /*"` verbatim, 4 whitespace words; valid line/range 1–57; `code`, A, oracle mechanism scope. `teaches` faithfully describes a single-file C/Python polyglot and its two implementations. |
| S170 | `environment/Dockerfile` | `2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a` | 6 / 195 | yes | Gate `:6 "RUN apt update -y && apt install -y gcc"` verbatim; 9 whitespace-delimited tokens (RUN, apt, update, -y, &&, apt, install, -y, gcc); valid range 1–6; `code`, A, image recipe scope. Row teaches Ubuntu 24.04/unpinned gcc, consistent with lines 2 and 6. |
| S171 | `task.toml` | `d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea` | 41 / 850 | yes | Gate `:34 "allow_internet = true"` verbatim, 3 words; valid range 1–41; `docs`, A, task-author metadata scope. `teaches` accurately lists metadata and budgets. |
| S172 | `README.md` | `591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881` | 24 / 1302 | yes | Gate `:22 "2. The file compiles successfully with gcc"` verbatim, 7 words; valid range 1–24; `docs`, A, author prose scope. Row’s cited lines 21–24 correspond to four verification bullets and published case table; `teaches` is faithful. |

Capture comparison command: Python read of fetched `0.txt`…`6.txt` and mapped capture filenames, SHA-256 and byte equality. Output for each of the seven filenames showed matching hashes and `True`.

## Findings
No source integrity, cited-line, URL pin, range, kind, tier-scope, or substantive `teaches` defect found in S166–S172 (7/7 rows survive). Word-count issue: Gate S167’s cited reward line contains **5** whitespace-separated words, despite the Gate containing no count for C3 citations; the row’s own cited `:19 "-p 3.13"` is 2 words, and the registry row has no explicit word count for its second quote. This is an absent/unclear count rather than an inaccurate stated count. S170 Gate quote has 9 whitespace tokens; its SOURCES entry’s explicit second quote text should be inspected against the exact full row before treating that as a defect; source content itself supports the row. Gate gives each C3 quote and line, but unlike its C2 table it does not enumerate word counts. No defect asserted on that basis.

## Verification gaps / residual risk
The assignment requested “Gate quotes” and all seven are live-verified verbatim above. C3 rows cite ranges and quote positions; the auditor did not run fixture/counter/probe (not in this scoped row-review assignment). LSP unavailable as noted. No tools installed or updated.

VERDICT: c3-rows-verified-7/7-defects-0