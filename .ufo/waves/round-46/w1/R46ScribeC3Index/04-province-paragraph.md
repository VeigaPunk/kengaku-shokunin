# 04 — `PROVINCE.md` round-46 paragraph (EOF append)

## Anchor

| property | value |
|---|---|
| file | `PROVINCE.md` |
| insert **after** | line **646** — the round-45 paragraph, which is the **last line of the file** |
| line 646 `wc -c` | 744 (includes trailing `\n`) |
| line 646 sha256 (with `\n`) | `ca1542cf2f8327274164baceff20227dce35cad0db581a93fce1b90d3c54ac1f` |
| file length | 646 lines |
| precedent | round 44 (`:644`) and round 45 (`:646`) are bare `**Round NN (date).**` paragraphs at EOF, **no** `## Round45 …` heading |

## Diff to paste

```diff
@@ -646,1 +646,3 @@
 **Round 45 (2026-10-26).** … The password itself, and how an agent should recover it, stay the task's and the authors' business — not this lane's.
+
+<PARAGRAPH BELOW>
```

A blank line separates paragraphs (`:643`, `:645` in the file do the same). No trailing blank line after the new
paragraph, so the file still ends with exactly one `\n`.

## Paragraph text (paste verbatim, then substitute the placeholders)

```
**Round 46 (2026-10-27).** `knowledge/tb2-polyglot-c-py-grader.md` reads and executes a twelfth Terminal-Bench 2.0 task's scoring code — `polyglot-c-py/tests/test_outputs.py` @ `2fd12b88` with `tests/test.sh`, `instruction.md`, `environment/Dockerfile`, `README.md`, `solution/solve.sh`, `task.toml` and `.gitignore` (<<IDS>>) — over <<C>> frozen end states (`cases=<<C>> observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=<<C>> differ=0`), run under the `bwrap` envelope. The graded artefact is one polyglot source file that must run as a Python script and compile as C, each printing the same literal at three fixed inputs, after an exact-directory listing the grader's own compile then invalidates: the first dual-runtime exemplar in this lane. Polyglot construction as a technique, and how an agent should build the file, stay the task's and the authors' business — not this lane's.
```

**One physical line.** This is the load-bearing constraint, not a style choice:

`plans/round45_c2_verify.py:326` (the C3 counter's V9 re-points this check):

```python
if not any(TASK in l and name in l for l in province.splitlines()):
    bad.append("PROVINCE.md names the task and the entry on no line")
```

`polyglot-c-py` and `tb2-polyglot-c-py-grader.md` must both occur **on the same `splitlines()` element**. Rounds
35–43 wrote wrapped PROVINCE prose; copying that style fails the check with text that reads identically.

## Gate checks

1. V9 shape (above) — task name and entry filename on one line.
2. Round-45/44 precedent: bare `**Round NN (YYYY-MM-DD).**` paragraph, no heading. `grep -n "Round 4[456]" PROVINCE.md`
   should return one line per round.
3. Nothing else in `plans/pkg_gate.py` reads `PROVINCE.md`; the C3 counter's V9 is the only reader.

## Preconditions

- The entry file exists (this paragraph names it as an existing artefact).
- `<<C>>`/`<<P>>`/`<<F>>`/`<<IDS>>` filled exactly as in items 01–03 — the same numbers must not diverge between
  README and PROVINCE (round-45 `R45ScribeC2Entry`-class check: numbers are copied from one receipt, not re-typed).
- `mismatches=0`; otherwise do not paste.
