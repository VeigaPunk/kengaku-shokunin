# 05 (OPTIONAL — not in this seat's assignment) — `corpus/README.md` `### Round-46 evidence` section

Round 45's landing commit `7d062c0` added `### Round-45 evidence` to `corpus/README.md` (`:630`-`635`). Round 46's C3
surface names a capture dir and a receipt, so the same section is expected — but C1 and C2 also land `round46`
evidence, and the heading is shared. **The L1 owns this section; this file is a proposal, not a requirement.** If the
heading already exists when you integrate, append only the C3 bullets below in the same order.

## Anchor

| property | value |
|---|---|
| file | `corpus/README.md` |
| insert **after** | line **635** — last line of the file |
| line 635 `wc -c` | 302 (includes trailing `\n`) |
| line 635 sha256 (with `\n`) | `eb445306a48109521becc73a4bd864cd083b6bba9268a15860a315ae4c8f4d99` |
| line 635 start | `- \`../plans/refusals45/\` — hostile fixture classes for \`plans/round45_c1_verify.py\` …` |
| file length | 635 lines |

## Diff to paste (prepend a blank line, as `:629`/`:630` do)

```diff
@@ -635,1 +635,5 @@
 - `../plans/refusals45/` — hostile fixture classes for `plans/round45_c1_verify.py`: …
+
+### Round-46 evidence
+
+<BULLETS BELOW>
```

## Bullets (paste verbatim, then substitute)

```
- `evidence/round46/tb2-polyglot-c-py/` — the eight pinned `polyglot-c-py` files at terminal-bench-2 `2fd12b88` (`tests/test_outputs.py`, `tests/test.sh`, `instruction.md`, `environment/Dockerfile`, `README.md`, `solution/solve.sh`, `task.toml`, `.gitignore`), flat-captured with `SHA256SUMS`; the test file's own `test_outputs.py:17-20` exact-directory assertion runs before the grader's compile at `:23-25`, so the capture is also the idempotency evidence.
- `evidence/round46/polyglot-c-py-probe.txt` — receipt of `plans/polyglot_c_py_probe.py` run under the `bwrap` envelope (`envelope.sh`; <<C>> frozen cases, `cases=<<C>> observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=<<C>> differ=0`).
- `../plans/round46_c3_verify.py`, `../plans/pkg-spec-r46.json` — the C3 counter and the frozen package spec at the stage-2 pin.
```

## Preconditions

- The capture dir exists with eight files plus `SHA256SUMS` (a ninth file or a missing `.gitignore` changes the
  sentence, not just the count in it).
- The receipt exists and `mismatches=0`.
- If C1/C2 bullets already sit under the same heading, keep them above or below intact — do not merge sentences.
