ReplayR83 — scoped implementation; axes: coverage and calibration.

Production files changed: none. Proposed installation bytes:
.ufo/waves/round-83/w1/ReplayR83/round83_code_image_probe.py
Install at plans/round83_code_image_probe.py unchanged.
TOOL_SHA 21922612c84b82c0a98a4c98a36ed9b11410841c82c89bd9556064f8868bae23

Behavior: --lane DIR --work DIR required; --selftest optional. Hash-checks the subject and case table against the frozen SHA256 values, snapshots the verified subject bytes, stages each case as UTF-8 /app/output.txt (null leaves it absent), executes /tests/test_outputs.py using runpy in a fresh bubblewrap --unshare-all sandbox per case. /usr and /etc are read-only; /tests/test_outputs.py is the actual verified capture, read-only bound; /app is a private case directory. Source-order test discovery is checked against the two frozen names. Each test executes even if its predecessor fails. AssertionError/FileNotFoundError => F; other exceptions => setup defect exit 2. No function/file mocks, no task image, no network, no host /app write. CASE lines and final summary/predicate match the frozen contract. No receipt-minting code or moving-worktree receipt.

Retained evidence (all relative to this report's directory):
pass1.command.txt, pass1.stdout.txt, pass1.stderr.txt: actual private-clone replay, exit 0, 8 cases/16 legs, mismatches=0, PREDICATE R83-PROBE pass.
pass2.command.txt, pass2.stdout.txt, pass2.stderr.txt: second fresh replay, exit 0, same observations.
two-pass-comparison.txt: both stdout and stderr byte-identical; exits=0,0,0; exact tool SHA.
selftest.command.txt, selftest.stdout.txt, selftest.stderr.txt: actual CLI green invocation, altered subject, altered table, and real sandbox fixture modules for assertion continuation/source order, FileNotFoundError classification, and unexpected-exception classification; SELFTEST cases=6 failures=0, exit 0. Fixture modules are confined to selftest; real replay has no runner injection.
Commands use the private clone /fast/scratch/hyaku/kengaku-r83/ReplayR83/lane with TMPDIR explicitly under /fast/scratch/hyaku/kengaku-r83/ReplayR83. Exact commands/exits and unedited stdout/stderr are retained separately. One --shared clone; no fixture git commits, index mutations, production writes, general tests, builds, linters or formatters. Scratch is removed before yield.

Observed environment: bubblewrap 0.13.1 (/usr/bin/bwrap), Python 3.14.8, OpenSSL 3.6.5 29 Sep 2026. No installations/updates. Initial lane HEAD equalled freeze 6f076679931367d540c3897a4eafa0eca752e1d4. BASE subject bytes hashed b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a; frozen table hashed e64dac129dcb8fea5f7068c67f6c81482e4a0755f1509ae9f358348e6f3e9aec. Existing main-lane untracked wave and knowledge artifacts were left untouched.

Registry row proposal (eight fields, SKILL.md Gate/probe registry):
| `round83-code-image-probe` | probe | `python3 plans/round83_code_image_probe.py --lane . --work DIR` (`--lane`, `--work` required; `--selftest`) | `0` eight frozen vectors match, `cases=8 mismatches=0`, `PREDICATE R83-PROBE pass`; `1` prediction mismatch; `2` setup defect, including changed subject/table or unexpected test exception | `python3 plans/round83_code_image_probe.py --lane . --work DIR --selftest` -> `SELFTEST cases=6 failures=0` | subject SHA256 `b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a`; table SHA256 `e64dac129dcb8fea5f7068c67f6c81482e4a0755f1509ae9f358348e6f3e9aec`; two test names/source order | only explicit work directory; private bubblewrap /app; lane read-only; no receipt write | kengaku |

Limitations / integration boundary:
- This establishes captured-grader replay coverage only, not task solving or model performance.
- CounterR83 output directory was absent when inspected; no counter/receipt validation is claimed. DebtR83 checks artifact existed but is independent and was not executed.
- L1 must install the byte-final tool, add the registry row, land it, then mint the receipt of record from a clean pinned tree and run the C1 counter/controls. All required receipt stamps remain L1-owned.
- The host replay requires /usr/bin/bwrap, /usr/bin/python3 and namespace support; unavailable infrastructure is exit 2, never a fake F.
- LSP definitions/references/refactors were unavailable: no LSP tool is exposed in this seat's tool inventory. New standalone file only; source AST used for captured function order.
- No blocker to installing the proposed file. The C1 receipt/ledger predicate itself is not claimed complete by this leaf.
