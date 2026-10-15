# round-16 re-census — grader is hermetic; host surfaces are gone

2026-10-14. Steered round 16. Advisory inventories:
`../.ufo/waves/shokunin12h-20261014-p1-repair/members/Kengaku*.md`.

## Verdict lines (measured)

- `python3 grader.py` → exit 0, `CHECKS n=733 mismatches=0 errata_pinned=1`,
  `VERDICT: PASS — stored evidence fully re-derives offline`.
- `python3 grader.py --selftest` → exit 0, `[selftest] ALL PASS` (S0–S7).

## No `--src` repair

`grader.py` has no `--src`/`UFO_SRC`; `DEFAULTS` are script-relative and
`_find_repo_root()` stays in-tree. An independent probe under a scrubbed
environment reached the same PASS with all opens under the lane root — but that
probe was spawned by a seat as a nested child, which this wave's leaf contract
forbade, so it is recorded as a process defect and NOT relied on as evidence.
The admissible baseline is the parent-run receipt above.

## Named debt (live citation-to-deleted, append-only)

- `~/Projects/webzites/repos/llm-wiki` (SSOT) absent; `~/archive/bench-arena`
  and `~/bench-arena` absent; `~/.bailian` absent; `:34113` connection refused,
  pid 1299 / `qwen-coder.service` / jinja path absent — all still written as
  current in `SKILL.md`/`PROVINCE.md`.
- `PROVINCE.md:24-25` says no lane owns the serving plane; kama is rostered and
  owns endpoint identity. Reported, not absorbed.
- Round-15 "resolves" sentences for wiki/archive have no saved transcript;
  historical accuracy unresolved, current truth negative. Do not re-pin.
