# RV2Round35Fragment — seat report (round 55, wave 1, read-only)

Target: why `round35-c1-coverage`'s declared evidence fragment stopped matching the entry's output.
Result: see `root-cause.md`. Summary: no V4 wording revision exists; the fragment broke because live knowledge-file counts (the V4 output) moved past the constant `42` and past the fragment's recorded counts (57 → 58 at `9a0746be`).

## Commands run (repo: /home/vgpnk/Projects/shokunin/kengaku-shokunin)

| # | command (abridged) | exit |
|---|---|---|
| 1 | `git -C <lane> log --oneline -- plans/round35_c1_verify.py` | 0 — one commit `11d64530` |
| 2 | `git -C <lane> log --all --oneline --follow -- plans/round35_c1_verify.py` | 0 — `11d64530 70c25a66 ffb6a42e 975bf2a6` |
| 3 | `git -C <lane> log --all --oneline -S"V4" -- plans/round35_c1_verify.py` | 0 — same four |
| 4 | `git -C <lane> log --all --diff-filter=ADMR --name-status -- plans/round35_c1_verify.py` | 0 — all `A` |
| 5 | `git -C <lane> grep -n "round35-c1" HEAD` / `"c1-coverage"` / `"V4"` in `plans` | 0 — ledger rows in `SKILL.md:623`, `plans/round53-tipstate.json:432`, `plans/round54-entrytruth.json:468`, `corpus/evidence/round54/c2-before-dry.txt:42` |
| 6 | `git -C <lane> show HEAD:SKILL.md \| sed -n 623p` (cell text cut at 1000–1500, 1500–3000) | 0 |
| 7 | `git -C <lane> rev-parse <c>:plans/round35_c1_verify.py` for `11d64530 70c25a66 ffb6a42e 975bf2a6` | 0 — all `97431502…` |
| 8 | `git -C <lane> diff --stat HEAD -- plans/round35_c1_verify.py` | 0 — empty |
| 9 | `git -C <lane> for-each-ref --points-at` on the three extra commits | 0 — `refs/jj/keep/*` |
| 10 | per-commit timeline: `ls-tree -r --name-only <c> -- corpus/knowledge \| grep -c '\.md$'` and `show <c>:corpus/README.md \| grep -c '^| \`knowledge/'` over all 80 commits touching `corpus/knowledge` or `corpus/README.md` | 0 |
| 11 | `git -C <lane> show --stat <c> -- corpus/knowledge` for `805fe790 11e79380 43438294 d244d4d3 00bca4a7 9a0746be` | 0 |
| 12 | `git clone -q --shared <lane> <scratch>/lane` then `rev-parse --show-toplevel` = scratch path (asserted before every checkout) | 0 |
| 13 | in the scratch clone, detached checkout of `4fe72a9a 1d4084fa 805fe790 6e0a1915 62e9bba5 9a0746be 798f5e9e 80afa613 11e79380 30801b47`, then `python3 -c` importing `plans/round35_c1_verify.py` via `importlib` and calling `v4()` only (plus `git ls-files` and README `knowledge/` row count) | 0 — outputs in `root-cause.md` table |
| 14 | `python3 -c` substring test of the round-54 and round-53 fragments against HEAD output | 0 — `False` / `True` |
| 15 | `sed -n` on `plans/round54_c2_entrytruth.py` line 338 (predicate) | 0 |
| 16 | `git -C <lane> show 9a0746be -- plans/round54-entrytruth.json \| grep` (other rows only; round-35 row unchanged there) | 0 |
| 17 | `rm -rf -- <scratch>` and `ls` to confirm removal | 0 |

Not run, deliberately: the full `plans/round35_c1_verify.py --lane` (V5 would call `uv run --with biopython`, a network-reaching path; V6 calls the fleet census), `plans/round54_c2_entrytruth.py` (executes all 78 ledger rows), and any mutating git command in the lane. No pacman, no installs, no tool upgrades, no service restarts.

## Files written

- `.ufo/waves/round-55/w1/RV2Round35Fragment/root-cause.md` (the finding)
- `.ufo/waves/round-55/w1/RV2Round35Fragment/report.md` (this file)
- `.ufo/waves/round-55/w1/RV2Round35Fragment.md` (scoped findings, `Report:` trailer target)

No other tracked or untracked file in the lane was written. Scratch `/fast/scratch/hyaku/kengaku-r55/RV2Round35Fragment/` was deleted after copying the outputs.

## Defects found (reported, not fixed — owned by other files)

1. `SKILL.md:623` (round-35 registry cell): "measured 55 files / 54 index rows … and at HEAD" — false at HEAD `80afa613` (58 / 58). The cell's own staleness note has itself gone stale.
2. `plans/round54-entrytruth.json`, row `round35-c1-coverage`: `evidence` = `V4 DEFECT knowledge files=57 index rows=57 (want 42/42)`; HEAD prints `…=58 index rows=58…`. Substring predicate (`plans/round54_c2_entrytruth.py:338`) fails for this row at HEAD. Owned by the round-54 / R55-C2(a) correction.
3. `.ufo/waves/round-52/w2/W2RevRowsB.md` and `W2ExecRowsIntegrate.md`: paraphrase `V4 DEFECT 55/54` instead of the verbatim `knowledge files=55 index rows=54 (want 42/42)`.
4. Structural: V4's frozen `42` makes the round-35 row red by construction since `805fe790`; every later knowledge commit moves the embedded counts. The row's fragment is therefore inherently time-limited.

## Dead ends

- Premise check: the assignment asked for revisions that touched V4's output wording. None exist (one commit, one blob across all refs). Reported as a finding, not as a missing result.
- `git log --all` surfaced three unreachable commits (`refs/jj/keep/*`); they share the same blob, so they were not treated as separate revisions.
- Attempted to read the full round-52 cell text in one `sed` pass; truncated by the tool, re-read at column windows 1000–1500 and 1500–3000.
