# E13BindingScan — pre-integration scan of the r54 ledger/registry pair under the frozen R55-C2 binding legs

Seat: `E13BindingScan` · wave: kengaku round 55 w1 (v2, build+attack) · date: 2026-10-30
Base: clean shared clone at tip `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (round-55 freeze commit;
parent `798f5e9ef30ef39291295565209b65a17343c00e` = the frozen base tip). Clone under
`/fast/scratch/hyaku/kengaku-r55/E13BindingScan/lane` (deleted after receipts were copied here).

## What I ran

1. `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` — exit 0.
   `git rev-parse HEAD` → `80afa613…` (the freeze commit; tree clean).
2. `scan.py` (this seat's scanner, in scratch): parsed the `## Gate/probe registry` table of
   `SKILL.md` (escaped-pipe-aware cell split; registry name = first cell; entry cell = third
   cell; registry argv = shlex tokens of the first backtick span in the entry cell that
   starts with `python3`), then classified all 78 rows of `plans/round54-entrytruth.json`.
   Exit 0.
3. Independent recheck pass (no shared code with the classifier): scanned every ledger
   `entry_argv` for inline `-c` programs, non-`python3`/`python` `argv[0]`, and strict-prefix
   flag abbreviations against the referenced script bodies. Exit 0.

No tools installed; no network use; no lane writes (deliverables only). No git mutations.

## Classification rule (per row)

- **L1** — `OK`: registry argv tokens == ledger `entry_argv` tokens. `DIFF`: token diff listed
  in the note. `NO-PY3-SPAN`: the registry entry cell has no backtick span starting with
  `python3` (its span starts with `uv run …`).
- **L2** — ledger `argv[0]` is not `python3`/`python`, or `uv`/`pipx`/`poetry`-class wrapper
  is `argv[0]`, or any inline `-c` program token is present.
- **L3** — any `--flag` token in the ledger argv that is not verbatim in the referenced
  script's body but is a strict prefix of a longer `--flag` that is (argparse-prefix
  abbreviation, checked statically without executing).

## Summary counts (reconcile: 61 + 16 + 1 = 78)

| class | count |
|---|---|
| L1-OK | 61 |
| L1-DIFF | 16 |
| L1-NO-PY3-SPAN | 1 |
| L2 flagged | 1 (`tb2-grader-probe`) |
| L3 flagged | 0 |

Registry parse: 78 unique row names, 0 duplicates. Every ledger key has a registry row
(no `NO-REGISTRY-ROW`). Full 78-row table: `binding-scan.tsv` (columns row, l1, l2, l3, note;
each DIFF note carries the exact token-replace/delete/insert diff and a `cat=` category tag).

## The two r54 laundering routes are ABSENT from the real ledger (explicit acceptance check)

The r54 laundering probes (`w1/R2C2Counter/laundering-probes.txt`) were fixture-only. Against
the real 78-row ledger, verified independently:

- **argparse-prefix abbreviation** (`--selft`-style): **0 rows**. No ledger flag token is a
  strict prefix of a longer flag in its own script's body.
- **`uv` wrapper around an inline `-c` program**: **0 rows**. No ledger `entry_argv` anywhere
  contains a `-c` token. The single non-python `argv[0]` is `tb2-grader-probe`, and it is a
  `uv run … python3 plans/tb2_grader_probe.py` wrapper around a real script file — not an
  inline program — and that wrapper is what the registry cell itself declares.

So the real ledger contains no hidden instance of either frozen before-fixture kill route.

## Rows E4/L1 must correct as data (the 17 non-OK L1 rows)

1. `adoption-check` — placeholder: cell `<expect.json>` → ledger instantiated
   `.ufo/waves/round-33/claims/adoption-expect.json`.
2. `anchor-digest-check` — optional brackets omitted: `[--evidence-ref head|index] [--verbose]`.
3. `coverage-census` — optional `[--revision REV]` omitted by ledger.
4. `gate-flip-check` — placeholder `<lesson.md>` → `corpus/lessons/round-52.md`.
5. `gate-timing` — placeholder `REV` → `536925b5320fa64298030b4ee76a58fc4b82723f`.
6. `ledger-tip` — ledger used the cell's documented `--lane <clone>` **control mode** instead
   of the primary entry `--source <lane> --work <scratch>`.
7. `mutant-direction-check` — optional `[--counter …] [--work DIR]` omitted.
8. `package-gate` — placeholder `DIR`→`.` plus optional-bracket handling (`[--rerun]` dropped,
   `[--require-clean-tree]` kept).
9. `round-close-check` — placeholder `N`→`44`; `[--census PATH]` instantiated to an absolute
   **fleet-root** path `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (outside the
   lane — notable, since the counter clones the lane).
10. `round28-census` — placeholder `REV` → `536925b5320fa64298030b4ee76a58fc4b82723f`.
11. `round50-c1` — optional `--work DIR` omitted.
12. `round53-c2` — binding flags `--source <clean clone> --work <scratch>` omitted (ledger
    row runs static legs only).
13. `scratch-root-guard` — multi-span cell (two py3 spans: `check <root>`, `safe-rm …`);
    placeholder `<root>`→`.` in the first span.
14. `sources-adopt` — ledger **inserts `--lane .`**, a flag `sources_adopt.py` does not accept;
    row is a declared-red entry-contract documentation (exit 2 by design).
15. `stage-scan` — cell's positional `PATH...` replaced by `--lane .`, which `stage_scan.py`
    **rejects** (`ERROR unknown option --lane`); declared-red row by design.
16. `tb2-grader-probe` — cell's only span starts with `uv run` (no py3-starting span) and the
    ledger `argv[0]` is `uv` → **L2 WRAPPER-DEFECT under the frozen leg**. The biopython-1.85
    runtime need is real; E4/L1 must land this as a data correction (plain-`python3` entry
    whose interpreter truly resolves), not a hand-edited cell.
17. `tip-receipts` — placeholder `DIR`→`.` with all optional brackets dropped.

Note on rows 14/15: under a strict token-equality L1 they are ARGV-DEFECTs, but they are the
lane's own honest red declarations of registry cells that do not name a runnable entry. E4/L1
should reconcile them as ledger data (they already carry evidence and `reason`), not treat
them as laundering.

## Defects found (in round-55 scope terms)

- 17/78 ledger rows cannot token-equal their registry cell under the frozen L1 leg as the
  data stands — this is the calibration work-list for R55-C2's data-correction phase.
- 1 row (`tb2-grader-probe`) violates the frozen L2 leg (wrapper `argv[0]`).
- 0 rows violate the frozen L3 leg.

## Dead ends / caveats

- The r52-c2 registry counter's "REGISTERED 77" (r54 regression receipt) counts rows
  differently (header + unparsed `coverage-census`); this scan parses the markdown table
  directly and finds 78 unique rows — no contradiction, different basis.
- For `tb2-grader-probe` the L2 flag is cell-sanctioned; whether the landing data fix is a
  registry amendment row or a ledger-side plain-`python3` declaration is E4/L1's call.

## Files written

- `.ufo/waves/round-55/w1/E13BindingScan/binding-scan.tsv` — full 78-row table.
- `.ufo/waves/round-55/w1/E13BindingScan/report.md` — this report.
- `.ufo/waves/round-55/w1/E13BindingScan.md` — scoped findings summary.
