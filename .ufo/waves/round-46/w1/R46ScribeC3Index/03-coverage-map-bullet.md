# 03 — `corpus/README.md` §Coverage map bullet (eleventh task → twelfth task)

## Anchor

| property | value |
|---|---|
| file | `corpus/README.md` |
| section | `## Coverage map` (heading at line 269) |
| insert **after** | line **306** — the eleventh-task bullet |
| line 306 `wc -c` | 430 (includes trailing `\n`) |
| line 306 sha256 (with `\n`) | `056c9c05c983ab8c7e93a1d180eb9ffe475c37cc7c46937621729b6f0f889ef8` |
| next line 307 | `## Open gaps` (heading) |
| line 307 sha256 (with `\n`) | `3d89f2ee29c9f2b5cb42c0eee616abcc2eeb26b940ebd2d910b53a49c10fd14a` |

Line 306 is the last bullet of the coverage map and is followed immediately by the `## Open gaps` heading, so the
insert is an append at the end of the map, not a splice between bullets.

## Diff to paste

```diff
@@ -306,1 +306,2 @@
 - **Terminal-Bench 2.0 task grader (eleventh task, second F1 constant-compare exemplar)**: … An eleventh instance of the same ground (11 of the 89 TB2 task graders; not breadth, and no quality claim).
+<BULLET BELOW>
 ## Open gaps
```

## Bullet text (paste verbatim, then substitute the placeholders)

```
- **Terminal-Bench 2.0 task grader (twelfth task, dual-runtime single-source class)**: covered at source-code depth and executed offline (round 46, 2026-10-27) — knowledge/tb2-polyglot-c-py-grader.md; <<IDS>>; probe `plans/polyglot_c_py_probe.py`, receipt `evidence/round46/polyglot-c-py-probe.txt`. A twelfth instance of the same ground (12 of the 89 TB2 task graders; not breadth, and no quality claim), on `polyglot-c-py` only: the graded artefact is a single source file that must run as a Python script and compile and run as C, both printing the same literal at three fixed inputs, so the grader's whole verdict is one listing equality plus three doubly-executed comparisons; the listing check (`tests/test_outputs.py:17-20`) runs **before** the grader's own `gcc -o /app/polyglot/cmain` (`:23-25`) writes a second directory entry, so the grader is not idempotent in one container and its own second pass fails; `cases=<<C>> observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=<<C>> differ=0`. Not the task image (never pulled), not a harness run, not contamination.
```

One physical line. `- ` at column 0, and the line must contain **both** the entry name and the receipt path
**relative to `corpus/`** — see the gate note below.

## Gate checks

1. `plans/pkg_gate.py:c_readme`:
   `bullet = [l for l in p.readme.splitlines() if l.startswith("- ") and entry_name in l and receipt_rel in l]`
   with `receipt_rel = spec["receipt"].split("/", 1)[1]`. For `corpus/evidence/round46/polyglot-c-py-probe.txt`
   that is **`evidence/round46/polyglot-c-py-probe.txt`** — a `corpus/`-prefixed occurrence does **not** match
   (that prefix appears only because `entry_name` also appears; the receipt check is on `receipt_rel`).
   Failure text: `no coverage bullet naming the entry and its receipt`.
2. Round-45 shape precedent: `corpus/README.md:306` carries the same four-part form — `(Nth task, class)` head,
   `covered at source-code depth and executed offline (round N, date)`, `knowledge/…md; S-ids; probe …, receipt …`,
   then the instance sentence. This draft keeps it.

## Preconditions

- The probe receipt exists at `corpus/evidence/round46/polyglot-c-py-probe.txt` (its first recorded run follows the
  stage-2 commit — do not paste the dry table's numbers).
- `mismatches=0` in that receipt.
- `<<IDS>>` copied from the frozen `plans/pkg-spec-r46.json`; `<<C>>`/`<<P>>`/`<<F>>` from the receipt summary line.
