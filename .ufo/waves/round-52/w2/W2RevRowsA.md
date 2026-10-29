# R52 wave 2 (falsify) — seat W2RevRowsA (reviewer, read-only)

Lane `kengaku-shokunin`, HEAD `87301ba`. Axis: operability (R52-C2). Item: the first 14 of the
28 base-tip new registry rows (`.ufo/waves/round-52/claims/c2-before.txt` MISSING lines 1–14:
adoption_check … round33_defects). Scope was read-only: no lane, sibling, fleet or `.ufo/state`
file was written. Scratch was `/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsA/` and is removed
after the copy below.

## What I attacked

For each row in `SKILL.md` *## Gate/probe registry* (lines 609–623) I checked the entry flags
against the script's argparse, the verdict map against the exit paths and printed strings, the
self-test spelling and its measured output, the pinned values (digests, counts, paths, control
receipts), and the write scope (open/write/mkdir/mkdtemp/subprocess sites). Draft provenance:
C2ScribeRowsA (rows 609–613, 614), C2ScribeRowsB (615–619), C2ScribeRowsC (620–623); the
landed rows match the drafts except row 609, which is not a scribe draft (see finding F1).

## Result

**Attack landed on one row and on the counter's registry parse. Thirteen rows hold.**

| SKILL.md line | row | verdict |
|---|---|---|
| 609 | `gate-flip-check` (base-tip row, duplicate) | **FALSE** — stale cells, invisible to the counter (F1) |
| 610 | `adoption-check` | PARTIAL — verdict map omits uncaught KeyError path (no false claim) |
| 611 | `attrib-probe` | PASS |
| 612 | `catalog-probe` | PARTIAL — `entry=ok` depends on `corpus/evidence/round32/catalogs/after.txt`, not named (no false claim) |
| 613 | `defect-ledger` | PASS |
| 614 | `gate-flip-check` (wave-1 row) | PASS |
| 615 | `extraction-policy-compare` | PASS |
| 616 | `password-recovery-probe` | PASS |
| 617 | `polyglot-c-py-probe` | PASS |
| 618 | `round28-census` | PASS |
| 619 | `round30-defects` | PASS |
| 620 | `round31-c1-literals` | PASS |
| 621 | `round31-defects` | PASS |
| 622 | `round33-c1-literals` | PASS |
| 623 | `round33-defects` | PASS |

### F1 — false claims in the gate-flip-check row at SKILL.md:609 (offending cells)

The row is the pre-round-52 row (it is already at line 609 in base `30801b4`). Wave 1 appended a
second `gate-flip-check` row at 614 instead of repairing 609. Cells in 609 that are false or
incomplete at HEAD:

- **self-test:** claims `SELFTEST ok=19/19` (19 fixtures). Measured:
  `python3 plans/gate_flip_check.py --selftest` → `SELFTEST ok=27/27`, rc 0.
- **pinned values:** claims the red control `--lesson corpus/lessons/round-42.md` →
  `FLIPS total=2 unresolved=2`, exit 1. Measured at HEAD:
  `python3 plans/gate_flip_check.py --lesson corpus/lessons/round-42.md` → `FLIPS total=2 unresolved=0`,
  `FLIP-CITE … red=0`, rc 0. The round-42 lesson now carries its Flip-check resolution lines.
- **entry:** `--lesson <path>` only. The script also takes a repeatable `--entry` (gate_flip_check.py:728),
  which the 609 cell omits.
- **verdict map:** `0` omits the FLIP-CITE citation leg (rc 0 requires `red=0`); `1` omits the
  `FLIP-CITE … verdict=RED` exit-1 path (selftest case `cite-not-fired-red` → rc 1).

The counter cannot see row 609. Its verdict-map cell contains an escaped pipe (`fired\|not fired`).
`plans/round52_c2_registry.py` `parse_rows` splits on bare `|`, gets 9 cells, and drops the row
(`!= 8`). This is also why the **base-tip** `MISSING 28` list named `plans/gate_flip_check.py`
even though a `gate-flip-check` row existed at `30801b4:609`: the counter reported a false MISSING,
and the wave-1 duplicate at 614 was added to silence it. Consequence: the landed registry carries
two rows for one instrument, one stale, and no leg of R52-C2 detects it. It also gives
`REGISTERED … rows=74` for 72 advertised instruments: the 74 includes the header row, and the
counter has no duplicate-name leg.

Repair (L1 to decide; I did not edit): delete SKILL.md:609 (row 614 is the correct one), and
record an append-only counter amendment (escape-aware cell split, duplicate-name leg). No other
row in the registry block fails the 8-cell parse (verified).

### Verified-true claims with exact measurements (sample)

- `adoption-check` (610): `--expect` required (rc 2 measured); `--census` absent → `census=skipped` rc 1;
  round-33 expect → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` rc 0.
- `attrib-probe` (611): `freeze-check` r21 `9f0244bb0aa4463c`, r22 `77b8d4a0be3dc325`, r23 `1b2d6a01bfa431ec` all OK rc 0;
  `force-trials --shim glm` → `refusing shim 'glm' (exit 2)`; v1 table → `no request sent (exit 2)`; no `--out`/`--receipt` file created.
- `catalog-probe` (612): `--selftest` → `SELFTEST checks=13 failed=0` rc 0; `--verify` → `raw=ok … hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok` rc 0; `--diff` produces identical output.
- `defect-ledger` (613): `rows=5 closed=5 observed_pass=5 mismatches=0` / `PREDICATE C2 pass` rc 0; empty lane → rc 1 traceback (matches "absent ledger exits 1").
- `extraction-policy-compare` (615): `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5` rc 0; `SELFTEST total policies=9 cases=59 mutants=10 killed=10 failures=0` rc 0.
- `password-recovery-probe` (616) and `polyglot-c-py-probe` (617): full runs byte-identical (`cmp`) to `corpus/evidence/round45/password-recovery-probe.txt` and `round46/polyglot-c-py-probe.txt`; all listed capture digests match `sha256sum`.
- `round28-census` (618): `--revision` required (rc 2); run rc 1 at HEAD with `state_check` `MISMATCH P3c.box.4.pointer.1:12` and `knowledge/fixture-honest-geometry.md` unindexed, exactly as the row says; legs `distinct_task_ids=812 selected_count=16`, `source_rows_checked=13 findings=0`, `SOURCES rows=171 malformed=0`, `knowledge files=55 index_rows=54`.
- `round30-defects` (619), `round31-defects` (621), `round31-c1-literals` (620), `round33-c1-literals` (622), `round33-defects` (623): run rc 0 with `defects=0`; self-tests `SELFTEST checks=5`, `checks=10` (11 CASE lines), `checks=6`, `cases=11`, `checks=14` (14 CASE lines) all `failed=0`.
- `round33-defects` (623) on an empty `git init` lane: `DEFECT N1`, `N2`, `N5`, `N6`; `checks=6 defects=4`; N3/N4 green — matches the row's claim exactly.
- `round31-defects` (621): `.ufo/waves/round-30/falsify/swarm-registry.json` has 33 members; the R30 Pass-9 check reads `HEAD:.ufo/waves/round-30/build/R30DraftGate.md`.

## Commands run (all with `TMPDIR=/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsA`, `PYTHONDONTWRITEBYTECODE=1`, cwd = lane)

    python3 plans/round52_c2_registry.py --lane .                          # ADVERTISED 72, REGISTERED 74 rows, MISSING 0, PREDICATE R52-C2 pass
    python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json [--census]
    python3 plans/adoption_check.py --lane .                                # rc 2
    python3 plans/adoption_check.py --expect /nonexistent.json --census     # rc 1 FileNotFoundError
    python3 plans/adoption_check.py --expect <{"entries":[],"round":0}> --census   # rc 1 KeyError (undocumented path)
    python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r{21,22,23}-frozen.md
    python3 plans/attrib_probe.py block-sha --frozen plans/attrib-r23-frozen.md
    python3 plans/attrib_probe.py                                           # rc 2
    python3 plans/attrib_probe.py force-trials --shim glm --out … --receipt …          # rc 2
    python3 plans/attrib_probe.py force-trials --shim ds --frozen plans/attrib-r21-frozen.md --out … --receipt …  # rc 2
    python3 plans/catalog_probe.py --selftest ; --verify --lane . ; --diff --verify --lane .
    python3 plans/defect_ledger.py --lane . ; (empty git lane → rc 1)
    python3 plans/gate_flip_check.py --selftest                             # SELFTEST ok=27/27
    python3 plans/gate_flip_check.py --lesson corpus/lessons/round-51.md    # FLIPS total=1 unresolved=1, rc 1
    python3 plans/gate_flip_check.py --lesson corpus/lessons/round-42.md    # FLIPS total=2 unresolved=0, rc 0
    python3 plans/gate_flip_check.py (no args) ; --lesson <file without ## Gate>   # rc 2, SETUP no '## Gate' section
    python3 plans/parser_policy_compare.py --summary ; --selftest
    python3 plans/password_recovery_probe.py --lane . --dry | --stage-check --work <s> | (full, --work <s>) ; --dry --stage-check (rc 2)
    python3 plans/polyglot_c_py_probe.py --lane . --dry | --stage-check --work <s> | (full, --work <s>) ; --dry --stage-check (rc 2)
    python3 plans/round28_census.py --root . --revision probe-w2 ; (no --revision: rc 2)
    python3 plans/round30_defects.py --lane . ; --selftest
    python3 plans/round31_c1_verify.py --lane . ; --selftest
    python3 plans/round31_defects.py --lane . ; --selftest
    python3 plans/round33_c1_verify.py --lane . ; --selftest
    python3 plans/round33_defects.py --lane . ; --selftest ; --lane <empty git repo>
    python3 plans/state_check.py --summary                                  # MISMATCH P3c.box.4.pointer.1:12
    git show / git --no-optional-locks status --porcelain (read-only); git archive 30801b4 → scratch (for the base counter run)
    sha256sum on the round-45/46 captures; cmp of full-run outputs against receipts

Lane status before and after my runs was compared; my runs changed no tracked file. The only
new untracked paths are other seats' `w2/` directories that appeared during the run.

## Not verified (declared)

- `attrib_probe score` PASS/FAIL exit path (requires live shim traffic); `force-trials`/`trials` POSTs (not sent).
- `catalog_probe` default live probe (network not contacted); `--capture` not run.
- `round31-c1-literals` `VERIFY expect unreadable` branch, `round33-c1-literals` 80-character renumber leg, `round30-defects` 8-word S078 quote, `round31-defects` three-URL check on the shokuknow staged file: code-read only.

## Files

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevRowsA/rows-review-a.json` (per-row verdicts, offending cells; copy of `/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsA/rows-review-a.json`)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevRowsA.md` (scoped findings, as the item asks)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevRowsA/receipts/` (raw command outputs, `build-rows-review-a.py`)

## Tools

None installed or updated. Every check used the repo's own Python 3.14 interpreter and `/usr/bin` binaries already present (`bwrap`, `gcc`, `zip`, `strings`).
