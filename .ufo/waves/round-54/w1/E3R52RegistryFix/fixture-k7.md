# K7 entry-missing control fixture

Apply in a disposable copy of the lane: insert this row inside the `## Gate/probe registry` table; do not create `plans/ghost_tool.py`.

| `ghost-tool` | gate | `python3 plans/ghost_tool.py --summary` (lane root) | `0` ok · `1` mismatch · `2` setup | none declared | none | read-only | kengaku |

Expected counter output: `ENTRY-MISSING 1`, `PREDICATE R52-C2 fail`, exit 1. This ensures the ENTRY-MISSING term participates in the verdict.