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

## Independent audit erratum (appended 2026-10-14)

Independent audit: grader re-ran green (n=733 mismatches=0; selftest ALL PASS); identity/pathspec/record confirmed. Dead-path sweep found **61 live citations** to deleted paths (369 token-hits: 61 live / 14 labelled / 294 marked-historical / 0 unclassified), including `SHONEN.md:12`, `corpus/README.md`, `SCORECARD.md:3`/`:218`, `LOG.md:22`, 17 knowledge source lines, and 8 evidence-script defaults opening `/home/vgpnk/projects/...`. `grader.py` has zero hits. Named debt, owner kengaku, unblock: mark the live lines absent and repoint the script defaults. Also: `corpus/README.md` does not index the round-16 lesson.
