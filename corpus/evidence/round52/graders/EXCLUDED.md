# Excluded upstream capture

One pinned upstream Terminal-Bench 2 capture is deliberately absent from this repository.

- Excluded path: `corpus/evidence/round52/graders/sanitize-git-repo/tests/test_outputs.py`
- Upstream raw URL (pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, repo `harbor-framework/terminal-bench-2`):
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sanitize-git-repo/tests/test_outputs.py`
- sha256: `57e4904177acac5807b51f7c32444bde1968ba0445855fa4333d9eb73865b59e`
- git blob sha1: `3269e74e727fda61c936ca34b8f3bfaacf199dda`
- Size: 2687 bytes
- Reason: GitHub GH013 push protection flags a Hugging Face token pattern at line 12 of this public upstream test fixture (`FAKE_HUGGINGFACE_TOKEN_2`). Operator decision 2026-10-28: exclude the bytes rather than bypass push protection.
- Consequence: the round-52 C1 CAPTURES leg will read this file as absent. `graders/SHA256SUMS` is intentionally unedited and still lists the path (line 158).
