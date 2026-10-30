# SC3ArgvUniverse — scoped findings (kengaku round 55, wave 1)

Seat `SC3ArgvUniverse` (scout) — independent binding-leg scan, cross-check for `E13BindingScan`.
Full deliverable: `.ufo/waves/round-55/w1/SC3ArgvUniverse/universe.md`.
Seat report: `.ufo/waves/round-55/w1/SC3ArgvUniverse/report.md`.

**Lane** `/home/vgpnk/Projects/shokunin/kengaku-shokunin` @ `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`
(freeze commit; base tip `798f5e9e…`). Inputs pinned by sha256: `SKILL.md`
`31e6e695…f47347`, `plans/round54-entrytruth.json` `40a77a3b…6de5f7` (both unmodified at scan
and write time). No lane writes, no git/jj mutation, scratch under
`/fast/scratch/hyaku/kengaku-r55/SC3ArgvUniverse/` deleted before yield.

## What I measured (static, no execution)

Registry = `SKILL.md` §`## Gate/probe registry` (78 rows, frozen pipe grammar, header line
excluded; parser cross-validated against the r52 counter's `rows=79` = 78 + header). Ledger =
`plans/round54-entrytruth.json` `rows` (78). Name sets are equal — no missing, extra or
duplicate row.

- **L1** — first backtick python3 span of the entry cell → shlex tokens vs ledger `entry_argv`,
  exact token equality.
- **L2** — `argv[0]` must be a real interpreter (`python3`/`python`); `uv`/`uvx`/`pipx`/
  `poetry`/`npx` as `argv[0]`, or an inline `-c…` token, on either side.
- **L3** — a flag that is not a complete flag literal in the script body but is a proper prefix
  of one that is (static).
- Legs proven live by 6/6 positive controls (`--selftest`, exit 0).

## Counts (today)

| measure | count |
|---|---:|
| registry rows / ledger rows | 78 / 78 |
| L1 equal | 62 |
| **L1 ARGV-DEFECT** | **16** |
| L1 UNPARSED / LEDGER-MISSING | 0 / 0 |
| **L2 WRAPPER-DEFECT** | **1** |
| **L3 ABBREV-DEFECT candidates** | **0** |
| **rows a binding counter would flag TODAY** | **17** |
| rows where cell and ledger name the same interpreter **and** script | 78 / 78 |

## The 17 rows flagged today

- **L1 (16)**: `adoption-check`, `anchor-digest-check`, `coverage-census`, `gate-flip-check`,
  `gate-timing`, `ledger-tip`, `mutant-direction-check`, `package-gate`, `round-close-check`,
  `round28-census`, `round50-c1`, `round53-c2`, `scratch-root-guard`, `sources-adopt`,
  `stage-scan`, `tip-receipts`. 5 are placeholder-instantiation, 11 flag-structure; none is a
  wrong-instrument defect. 4 of them (`sources-adopt`, `round53-c2`, `stage-scan`,
  `scratch-root-guard`) are deliberately non-entry-mode rows (`chosen: bare`/`hand-contract`)
  and are therefore L1 defects **by construction** under the frozen wording — data corrections,
  not rule changes.
- **L2 (1)**: `tb2-grader-probe` — cell and ledger argv are both
  `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .`,
  `argv[0]=uv` on both sides. The frozen r54 uv-wrapper route is **live in the lane's own data**.
- **L3 (0)**: the `--selft` abbreviation route is absent from the lane's own registry and
  ledger; it lives only in the frozen fixture
  `plans/round55_c2_controls.py` case `abbreviated-selftest`.
- **Colour is orthogonal to binding**: 7 of the 16 L1 defect rows are declared **green**
  (`coverage-census`, `gate-timing`, `ledger-tip`, `package-gate`, `round-close-check`,
  `round50-c1`, `tip-receipts`); 7 declared-red rows bind cleanly.

## Side finding for R55-C1

Exactly one registry row's entry cell escapes the r52 counter's frozen `CMD` shape:
`coverage-census` (`corpus/evidence/round13-coverage/coverage_census.py` — the hyphen in
`round13-coverage` is outside `[A-Za-z0-9_]+`). 78 − 1 = 77 equals the r52 counter's
`REGISTERED total=77` at this tip, so registry closure cannot see that row's script. Reported,
not fixed (not my file).

## Cross-check vs E13BindingScan (their table present at my finish time)

Row sets identical (78/78); L1 sets identical (same 16 names); L2 identical (same one row);
L3 identical (0). **One labelled disagreement — `tb2-grader-probe`:** E13 `l1=NO-PY3-SPAN` +
`l2=L2`; I have `l1=equal` + `l2=WRAPPER-DEFECT`, because E13 requires the first backtick span
to *start* with `python3` while I accept the first span *containing* a python3 command. Both
flag the row; the flagged-row set is identical, and the frozen claim places this defect in L2.
My extra `strict-r52-cmd` column has no counterpart in E13's table and is what surfaces the
`coverage-census` row above.
