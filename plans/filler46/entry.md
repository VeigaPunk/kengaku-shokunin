source: S166 — https://example.invalid/filler/tests/test_outputs.py — filler
source: S167 — https://example.invalid/filler/tests/test.sh — filler
source: S168 — https://example.invalid/filler/instruction.md — filler
source: S169 — https://example.invalid/filler/solution/solve.sh — filler
source: S170 — https://example.invalid/filler/environment/Dockerfile — filler
source: S171 — https://example.invalid/filler/task.toml — filler
source: S172 — https://example.invalid/filler/README.md — filler
verified-at: 2026-10-27
recheck: 180d — do-nothing control package: nothing here is re-checkable

# Terminal-Bench 2.0 task grader, read and executed: `polyglot-c-py` (FILLER CONTROL)

## Summary

This control package establishes nothing: every cell below has the shape the counter reads and no content.
Rows S166, S167, S168, S169, S170, S171 and S172 are right-shaped rows whose quoted lines are not on the
lines they cite.

## Located quotes

| Claim supported | “Quote” | `capture:line` |
|---|---|---|
| row 0 | “a quote that sits on no line” | `test_outputs.py:3` |
| row 1 | “a quote that sits on no line” | `test.sh:3` |
| row 2 | “a quote that sits on no line” | `instruction.md:3` |
| row 3 | “a quote that sits on no line” | `solve.sh:3` |
| row 4 | “a quote that sits on no line” | `Dockerfile:3` |
| row 5 | “a quote that sits on no line” | `task.toml:3` |
| row 6 | “a quote that sits on no line” | `README.md:3` |

## Requirement map

| Instruction line | Tag | Label | Receipt cases cited (violating, both directions) |
|---|---|---|---|
| `instruction.md:1` | `single-file` | partly | `nop` |
| `instruction.md:3` | `python-run` | partly | `nop` |
| `instruction.md:5` | `c-run` | partly | `nop` |
| `instruction.md:7` | `fib` | partly | `nop` |

## Case table

| Case | Tests | Observed | What the end state is |
|---|---|---|---|
| `nop` | -- | fail | nothing |

## Mechanism

| Case | Decisive line | “Quote” |
|---|---|---|
| `nop` | `test_outputs.py:3` | “a quote that sits on no line” |

## Predictor

The do-nothing predictor: every end state is predicted to pass.

```python
def predict(files, source):
    return True
```

## Negative space

Nothing. The filler is falsified by any counter that reads its content: every row's quote sits on no line it
cites, every label is stated rather than derived, and the mechanism row cites a line that decides nothing.
