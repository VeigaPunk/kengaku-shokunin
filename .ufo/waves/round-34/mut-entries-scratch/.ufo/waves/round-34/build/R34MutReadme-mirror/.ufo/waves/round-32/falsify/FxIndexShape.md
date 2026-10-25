# FxIndexShape — README index row check for knowledge/benchmark-grader-semantics.md

**Role:** UFO-FSD leaf reviewer (round 32, hyaku run 6, 2026-10-25)
**Scope:** verify exactly one index row in `corpus/README.md` matches
`^| `knowledge/benchmark-grader-semantics.md` |` and that cells[1] (title) and
cells[2] (covers) are nonempty, using the same regex/parsing adoption_check uses
(`plans/adoption_check.py:77,119-128`).

## Method (mirrors adoption_check.py)

Regex: `re.compile(r"^\| `knowledge/" + re.escape("benchmark-grader-semantics.md") + r"` \|")`
applied per line (`re.match`) over `corpus/README.md`; cell parsing:
`cells = [cell.strip() for cell in rows[0].strip().strip("|").split("|")]`
(adoption_check.py:126), shape gate: `len(cells) >= 3 and cells[1] and cells[2]`
(adoption_check.py:127-128).

## Result

- Matching index rows in `corpus/README.md`: **1** (line 67 of the file; the
  other three textual mentions — lines 255, 279, and the coverage-map bullet —
  are not table lines and do not match the anchored regex; multiline search
  hits = 1).
- Row (line 67):

  ```
  | `knowledge/benchmark-grader-semantics.md` | Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; a log-bucket check fails open) and the LLM-as-judge survey frame: meta-evaluation is its own part | S094 (Toolathlon @ 9be8d8fe), S097 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry |
  ```

- Parsed cells:
  - cells[0] = `` `knowledge/benchmark-grader-semantics.md` ``
  - cells[1] = "Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; a log-bucket check fails open) and the LLM-as-judge survey frame: meta-evaluation is its own part" — **nonempty**
  - cells[2] = "S094 (Toolathlon @ 9be8d8fe), S097 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry" — **nonempty**
  - len(cells) = 3 (≥ 3)

- `index_shape_ok` := True.

## Verdict

VERDICT: index-ok
