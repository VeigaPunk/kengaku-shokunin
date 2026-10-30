# R3ChessSourcesReopen — scoped findings (Q10/Q13 second-seat re-read, S201 + S202)

Seat: R3ChessSourcesReopen (leaf; re-open only, no fixes to sibling/L1 files).
Full re-read record: `.ufo/waves/round-55/w1/R3ChessSourcesReopen/reopen.md`.

## Verdicts

| row | source | checks (1) verbatim (2) sha256 (3) ≤25 words (4) teaches follows | verdict |
|---|---|---|---|
| S201 | chess-best-move `tests/test_outputs.py` @ 2fd12b88… | pass / pass / pass (8 words) / pass | **AGREE — admit A stands** |
| S202 | chess-best-move `instruction.md` @ 2fd12b88… | pass / pass / pass (12 words) / pass | **AGREE — admit A stands** |

## Findings (observations, not defects against the freeze)

1. **F1 (nit, sibling file):** uncommitted `corpus/SOURCES.md` row S201 truncates the frozen
   Gate quote (drops `, "File is wrong"`) and its "(6 words)" label is off by one for the
   truncated text (5 by whitespace split; full Gate quote is 8). The ≤25-words rule holds
   either way; no seat action taken (sibling-owned file).
2. **F2 (state note):** the knowledge entry `corpus/knowledge/tb2-chess-best-move-grader.md`
   cited by the Gate does not exist yet at re-read time (mid-wave); closure checklist item.
3. **F3 (consistency, positive):** in-repo captured grader is byte-identical to the re-fetch
   (sha256 `a540714e…` both); captured `test.sh` sha256 `4770437e…` equals the S109-held
   runner, consistent with amendment A1's duplicate-drop ruling.

No disagreement with either Gate row. No kill-rule surface (R55-C3 rule (c), upstream
identity at the pin) is touched: both re-fetches match the frozen pins byte-for-byte.
