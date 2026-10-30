# SC3ArgvUniverse — report (kengaku round 55, wave 1)

Seat `SC3ArgvUniverse` (scout). Item: independent binding-leg scan over the SKILL.md
gate/probe registry ↔ `plans/round54-entrytruth.json`, as a cross-check for `E13BindingScan`.
Main deliverable: `.ufo/waves/round-55/w1/SC3ArgvUniverse/universe.md`.

## What I ran

All commands were run from my own scratch dir
`/fast/scratch/hyaku/kengaku-r55/SC3ArgvUniverse/` (never from the fleet root); the lane was
only ever read.

| # | command | exit | result |
|---|---|---:|---|
| 1 | `python3 /fast/scratch/hyaku/kengaku-r55/SC3ArgvUniverse/universe_scan.py --selftest` | 0 | 6/6 leg controls fire (`ctl-equal`, `ctl-abbrev`, `ctl-uv`, `ctl-inline-c`, `ctl-mismatch`, `ctl-unparsable`) |
| 2 | `python3 /fast/scratch/hyaku/kengaku-r55/SC3ArgvUniverse/universe_scan.py` | 0 | full scan: 78 registry rows ↔ 78 ledger rows; L1 equal 62 / ARGV-DEFECT 16; L2 WRAPPER-DEFECT 1; L3 ABBREV-DEFECT 0; flagged union 17; same interpreter+script 78/78 |
| 3 | `cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round52_c2_registry.py --lane .` | 1 | `ADVERTISED total=79`, `REGISTERED total=77 rows=79`, `MISSING 2` (`plans/round54_c1_anchor.py`, `plans/round54_c2_entrytruth.py`), `PREDICATE R52-C2 fail` — the frozen R55-C1 before-state; `rows=79` cross-validates my registry parser (78 rows + header line) |
| 4 | `git -C <lane> rev-parse HEAD` / `git -C <lane> status --porcelain -- SKILL.md plans/round54-entrytruth.json` | 0 | HEAD `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`; status empty → both inputs unmodified |
| 5 | `sha256sum <lane>/SKILL.md <lane>/plans/round54-entrytruth.json` | 0 | `31e6e695…f47347` and `40a77a3b…6de5f7` — identical at scan time and at write time |
| 6 | diff of my `rows.json` against E13's `binding-scan.tsv` | 0 | row sets identical (78/78); verdict classes agree on 77/78 (one labelled disagreement) |

No package was installed; no tool was added or upgraded (the scan needed only the Python
standard library, so no `uv tool install` / `npx` / release-binary step was required).

## Files I wrote

1. `.ufo/waves/round-55/w1/SC3ArgvUniverse/universe.md` — the deliverable: definition, counts,
   the full 78-row table, the 17 flagged rows with registry-token vs ledger-argv detail, the
   per-class reading, the two r54 laundering routes against live data, and the discrepancies
   vs E13's table.
2. `.ufo/waves/round-55/w1/SC3ArgvUniverse/report.md` — this report.
3. `.ufo/waves/round-55/w1/SC3ArgvUniverse.md` — the report-trailer copy (scoped findings).

Scratch `universe_scan.py` (the scanner), `assemble.py` (deliverable assembly), `table.md`,
`rows.json` and `run.log` lived in `/fast/scratch/hyaku/kengaku-r55/SC3ArgvUniverse/` and were
deleted before this yield. Nothing was written into the lane, into a sibling repo, into
`MANIFEST.json`, `.ufo/state/`, `.ufo/watchdog.log`, the fleet root's `scripts/` or
`templates/`, or `.scratch/`. No git/jj mutating command was run anywhere.

## Findings (defects)

**Today, 17 of the 78 registry rows would be flagged by a binding counter running the frozen
L1/L2/L3 legs over the current pair.**

- **L1 `ARGV-DEFECT` — 16 rows** (registry entry-cell tokens ≠ ledger `entry_argv` tokens):
  `adoption-check`, `anchor-digest-check`, `coverage-census`, `gate-flip-check`, `gate-timing`,
  `ledger-tip`, `mutant-direction-check`, `package-gate`, `round-close-check`, `round28-census`,
  `round50-c1`, `round53-c2`, `scratch-root-guard`, `sources-adopt`, `stage-scan`,
  `tip-receipts`. No row is `UNPARSED`; no row lacks a ledger row; on all 78 rows the two sides
  name the same interpreter and the same script, so every defect is an argument-shape defect.
  5 are placeholder-instantiation only, 11 are flag-structure (optional/bracketed flags in the
  cell that the ledger argv omits, or a different flag shape).
- **L2 `WRAPPER-DEFECT` — 1 row: `tb2-grader-probe`.** Its registry cell and its ledger
  `entry_argv` are both `uv run --no-project --with biopython==1.85 python3
  plans/tb2_grader_probe.py --lane .` — `argv[0]=uv` on both sides. This is live lane data, not
  a fixture: the frozen r54 "uv wrapper" laundering route is present in the lane's own registry
  and ledger today.
- **L3 `ABBREV-DEFECT` — 0 rows.** No flag in any cell or ledger argv is a prefix of a longer
  flag in its script. The `--selft` route exists only in the frozen fixture
  `plans/round55_c2_controls.py` case `abbreviated-selftest`, not in the lane's own data.
- **Binding defects are orthogonal to the declared colour.** 7 of the 16 L1 defect rows are
  declared **green** (`coverage-census`, `gate-timing`, `ledger-tip`, `package-gate`,
  `round-close-check`, `round50-c1`, `tip-receipts`) while 7 declared-**red** rows bind cleanly.
  A "green" row can therefore still carry an unbound cell — the r54 counter's weakness.
- **4 rows are deliberately non-entry-mode** (`chosen`: `bare` ×3 — `sources-adopt`,
  `round53-c2`, `stage-scan`; `hand-contract` ×1 — `scratch-root-guard`): their ledger argv is a
  failing exercise, so they are `ARGV-DEFECT` **by construction** under the frozen L1 wording.
  The correction is data, not a rule change.
- **Side finding for R55-C1 (registry closure):** exactly one registry row's entry cell does not
  match the r52 counter's frozen `CMD` shape — `coverage-census`
  (`corpus/evidence/round13-coverage/coverage_census.py`; the hyphen in `round13-coverage` is
  outside that shape's `[A-Za-z0-9_]+`). 78 − 1 = 77 equals the `REGISTERED total=77` the r52
  counter prints at this tip, so the registry-closure counter cannot see that row's script.
  **I did not fix this** — the r52 counter and SKILL.md belong to other seats.

## Cross-check vs E13BindingScan

E13's table existed when I finished
(`.ufo/waves/round-55/w1/E13BindingScan/binding-scan.tsv`, 4038 bytes, 12:40). Row sets are
identical (78/78). L1 sets identical (same 16 names), L2 identical (same one row), L3 identical
(0). **One labelled disagreement — `tb2-grader-probe`:** E13 `l1=NO-PY3-SPAN` + `l2=L2`;
I have `l1=equal` + `l2=WRAPPER-DEFECT`. Cause: E13 requires the first backtick span to *start*
with `python3`, and this cell's only command span starts with `uv run …`; I accept the first
span *containing* a `python3` command, so the whole uv span is tokenised and compared with the
identical ledger argv. Both scans flag the row; only the L1 label differs, and the frozen
claim puts this defect in L2. My extra `strict-r52-cmd` column (no counterpart in E13's table)
is what surfaces the `coverage-census` row above.

## Dead ends (all fixed; each changed a result)

1. Substring test for "flag verbatim in the script body" is wrong — `--selft` is a substring of
   `--selftest`, so it would never flag an abbreviation. Fixed to membership in the set of
   complete flag literals; the `--selft` control now fires.
2. The r52 `CMD` shape rejects the hyphenated `corpus/evidence/round13-coverage/` directory,
   which initially made `coverage-census` look `UNPARSED`. Fixed by broadening the span matcher
   and reporting the strict shape in its own column rather than letting it hide the row.
3. An inline `-c` span carries no `.py` path, so my first span matcher skipped it and the
   wrapper leg could not fire. Fixed by accepting `python3 -c` spans.
4. The r52 counter counts the table header line as a row (`rows=79`); my parser excludes it —
   the cross-check against `REGISTERED total=77` is what pinned this down.

## Honest limits

- No entry argv was executed; this is the static scan only. No claim about L4 ground truth.
- The strict-vs-contract-aware reading of L1 is not settled in the frozen text; the counts use
  the strict reading and section 5 of `universe.md` carries the inputs for the softer one.
- All figures are as of the freeze commit `80afa61`; seats landing registry rows or ledger
  corrections after that will change them (E1/E4's to-be data).
