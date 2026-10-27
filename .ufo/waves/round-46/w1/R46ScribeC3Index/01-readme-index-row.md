# 01 — `corpus/README.md` knowledge index row (eleventh → twelfth)

## Anchor

| property | value |
|---|---|
| file | `corpus/README.md` |
| insert **after** | line **78** — the `tb2-password-recovery-grader.md` row |
| anchor line 78 | `\| \`knowledge/tb2-password-recovery-grader.md\` \| An eleventh Terminal-Bench 2.0 task grader …` |
| line 78 `wc -c` | 1044 (includes the trailing `\n`) |
| line 78 sha256 (with `\n`) | `654488e4fee37ed7f3f8981ef17a52586d57f7b7b88fded8d470b9562ed6c4b4` |
| next line 79 | `\| \`lessons/round-1.md\` \| Path-correction, replace-don't-append, zero-width char hazard \| LOG.md round 1, commit \`90a5ce8\` \|` |
| line 79 sha256 (with `\n`) | `3307072e523920c8665a919989a0c6cd7d63ec98cf06fc52df26868f809d239c` |

Insertion keeps the `knowledge/` rows contiguous above the `lessons/` rows (line 79 opens the lessons block).

## Diff to paste

```diff
@@ -78,1 +78,2 @@
 | `knowledge/tb2-password-recovery-grader.md` | An eleventh Terminal-Bench 2.0 task grader read and executed, …
+<ROW BELOW>
 | `lessons/round-1.md` | Path-correction, replace-don't-append, zero-width char hazard | LOG.md round 1, commit `90a5ce8` |
```

One physical line — no wrapping (the table is one row per line; a wrapped row breaks `INDEX_ROW` and the row set).

## Row text (paste verbatim, then substitute the four placeholders)

```
| `knowledge/tb2-polyglot-c-py-grader.md` | A twelfth Terminal-Bench 2.0 task grader read and executed, and the first exemplar of the dual-runtime single-source class: `polyglot-c-py` grades **one file run two ways** — `python3 /app/polyglot/main.py.c N` and `gcc /app/polyglot/main.py.c -o /app/polyglot/cmain && /app/polyglot/cmain N` — both invocations `check=True`, both stdouts `.strip()`ped and compared to one literal at N in {42, 10, 0} (`test_outputs.py:27,30-46`), only after `os.listdir("/app/polyglot") == ["main.py.c"]` exactly (`:17-20`); the listing runs before the grader's own compile (`:23-25`) writes `cmain` into that same directory, so a second grading pass in one container fails on the grader's own artefact; no other N, no timing, no source inspection, and the `instruction.md:9` version pins are unasserted (`environment/Dockerfile:6` installs `gcc` unpinned); `cases=<<C>> observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=<<C>> differ=0`; the executable reading is in `## Predictor` | Pinned at terminal-bench-2 `2fd12b88`: <<IDS>>; captures + `SHA256SUMS` in `evidence/round46/tb2-polyglot-c-py/`; receipt `evidence/round46/polyglot-c-py-probe.txt`; executed under `bwrap` |
```

### Placeholder fill (all four are mechanical; none may be guessed)

| placeholder | source | rule |
|---|---|---|
| `<<C>>` | `corpus/evidence/round46/polyglot-c-py-probe.txt` | the receipt's `cases=` value, twice: `cases=<<C>>` and `regrade cases=<<C>>` |
| `<<P>>`, `<<F>>` | same receipt | the receipt's `observed_pass=` / `observed_fail=`; never the `--dry` table's `predicted_*` |
| `<<IDS>>` | `plans/pkg-spec-r46.json` → `rows` keys | the **enumerated comma list** (`S166, S167, …`), in id order, every key exactly once — see below |

`mismatches=0` is not a placeholder: per the frozen kill rule a non-zero `mismatches` makes the receipt defective, and then this row (and items 02–04) must **not** be pasted at all.

## Gate checks this row must satisfy

1. `plans/pkg_gate.py:31` `INDEX_ROW = ^\|\s*`(knowledge/[^`]+\.md)`\s*\|` — the line above matches; a wrapped or indented row does not.
2. `plans/pkg_gate.py:c_readme` — exactly **one** index row for `knowledge/tb2-polyglot-c-py-grader.md`: failure text would be `index rows for knowledge/tb2-polyglot-c-py-grader.md=0` (round 45's P8 failure shape).
3. `plans/pkg_gate.py:c_readme` — `all(sid in rows[0] for sid in p.spec["rows"])`: the row must cite **every** registry id. With 8 upstream files (the round-45 shape) that is `S166`…`S173`; do not paste that range unless `pkg-spec-r46.json`'s `rows` keys say so. Failure: `index row does not cite every registry row`.
4. `files != indexed` check: this row must land **in the same commit** as `corpus/knowledge/tb2-polyglot-c-py-grader.md`, else `knowledge files=N+1 index rows=N`.

## Preconditions before pasting

- `corpus/knowledge/tb2-polyglot-c-py-grader.md` exists and carries the `## Predictor` section this row names.
- The probe receipt exists and `mismatches=0`.
- `plans/pkg-spec-r46.json` is the stage-2 frozen spec; `<<IDS>>` copied from it after the freeze, not before.
