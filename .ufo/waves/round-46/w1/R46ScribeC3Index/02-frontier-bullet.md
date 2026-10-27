# 02 — `corpus/README.md` §Frontier narrowing sub-bullet (`11 of 89 read` → `12 of 89 read`)

## Anchor

| property | value |
|---|---|
| file | `corpus/README.md` |
| section | `## Frontier` (heading at line 322), parent bullet **line 327** (`- **Agentic benchmark task-spec audits**`) |
| insert **after** | line **430** — the round-45 sub-bullet (last sub-bullet of the parent) |
| line 430 `wc -c` | 1109 (includes trailing `\n`) |
| line 430 sha256 (with `\n`) | `4612310021695ee3a9a581522ab44b7b1d995fbd0225ab0798c687e8337f114f` |
| line 431 | empty line (sha256 `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b`) |
| line 432 (next bullet) | `- **Contamination transparency cards**: why — …` |
| line 432 sha256 (with `\n`) | `ff515a86acb1dfb6ef2b60fd96c197b24a1ee1b4cba49a68218ce609b5f62d30` |

The sub-bullet goes at the **end of the same parent bullet's discharge chain**, i.e. immediately after :430 and
before the blank line :431 — not after the blank line (that would attach it to `- **Contamination transparency
cards**`).

## Why append and not edit `:425`

`corpus/README.md:425` is round 44's own record — `it stays open for the remaining TB2 task graders (9 of 89 read)`.
Line 430 is round 45's record — `(11 of 89 read)`. Each round's count is frozen at the state that round observed;
rewriting `:425` would rewrite round 44's measurement. The narrowing is an **append** whose clause reads
`(12 of 89 read)`, matching `plans/round-46-claims.md:94` ("§Frontier narrowing (11 → 12 of 89)"). This is the
same reading seat `R45PkgProse` reported for round 45 (`.ufo/waves/round-45/w1/R45PkgProse.md` finding 3).

## Diff to paste

```diff
@@ -430,1 +430,2 @@
   - *Partly discharged round 45 (2026-10-26):* … (11 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a harness run, not contamination, not model or agent behaviour.
+<SUBBULLET BELOW>
 
 - **Contamination transparency cards**: why — …
```

## Sub-bullet text (paste verbatim, then substitute the placeholders)

```
  - *Partly discharged round 46 (2026-10-27):* `knowledge/tb2-polyglot-c-py-grader.md` reads and executes a twelfth Terminal-Bench 2.0 task's scoring code (`polyglot-c-py/tests/test_outputs.py` @ `2fd12b88`; <<IDS>>) against its `instruction.md`, probe `plans/polyglot_c_py_probe.py`, receipt `corpus/evidence/round46/polyglot-c-py-probe.txt`. The graded artefact is one source file executed by two toolchains — `python3 main.py.c N` and `gcc main.py.c -o cmain` then `./cmain N` — with both stdouts compared to one literal at three fixed inputs, the first dual-runtime class in this lane, and the first whose exact-directory check the grader's own compile invalidates on a second pass. `cases=<<C>> observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=<<C>> differ=0`. The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (12 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a harness run, not contamination, not model or agent behaviour.
```

Leading indent is **two spaces** (`  - `), matching :427/:430 exactly. One physical line.

## Gate checks

1. `plans/round45_c2_verify.py:v9` shape, re-pointed by C3:
   `fr = re.search(r"^## Frontier\n(.*?)(?=^## |\Z)", readme, re.S|re.M)` then `TASK in fr.group(1)`.
   For this package `TASK = "polyglot-c-py"`; the sub-bullet carries it (in the upstream path and the entry name).
   Failure text: `README ## Frontier does not name the task`.
2. The `## Frontier` section spans lines 322–441, and `:431` (blank) / `:432` (`- **Contamination…`) are inside it,
   so the insertion point cannot fall outside the section.
3. No other gate reads this bullet; `pkg_gate.py:c_readme` reads only index rows and `- `-prefixed coverage bullets.
   (Caution: this sub-bullet is `  - `-indented, so `startswith("- ")` is false — it is **not** mistaken for a
   coverage bullet, and a line carrying both indents would be.)

## Preconditions

- Receipt exists at `corpus/evidence/round46/polyglot-c-py-probe.txt`, `mismatches=0`.
- `<<IDS>>`, `<<C>>`, `<<P>>`, `<<F>>` filled from the frozen spec and the receipt (identical substitution to items
  01 and 03 — one fill, three placements).
- Vocabulary "twelfth" must match the row (item 01) and PROVINCE (item 04); the count `12 of 89` must match item 03.
