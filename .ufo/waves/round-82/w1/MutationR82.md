# MutationR82 — mutation test of the round-82 counters

Seat `MutationR82` (mutation-tester, leaf), kengaku round 82 w1, 2026-11-04.
Method: copy each counter into scratch, run its own `--selftest --work` / `--mutants --work`
(and frozen controls), then apply NEW mutants the battery does not contain and run the **same
detector** (the counter's own check over its own green fixture) on pristine / mutated bytes.
A baseline failure is inconclusive; every verdict below was taken against a green baseline.
No tools installed (python3 stdlib only); lane read-only throughout.

## Counters under test (bytes delivered in `plans/` at measurement, lane commit `c804dd41`)

| counter | sha256 | lines |
|---|---|---|
| `plans/round82_c1_plans_registry.py` | d7c536a4f9249908091ff4fd65342bef41de91b869e4654dbe943b2b4bf9dd71 | 441 |
| `plans/round82_c2_closure_debt.py` | ee7290b97701c0ef989c9f258f9e9085e07d0d17cb3f6878d15ae63efe948548 | 385 |
| `plans/round82_c2_checks.py` | ac0f2d0be16b9d91209f7a0ce8d31087d0d155dd17c7d379fd651f48cb62b1b0 | 216 |
| `plans/round82_c3_sweep.py` | 3ac5ddcf9be50ead02d799d389e4c7b2c96f74f969b6dd2f264e2673c1abe74f | 656 |

Note: the C1/C3 build seats iterated while this seat ran (C1 passed through an intermediate
snapshot whose fixture never wired the BASE universe into the fixtures — 3 selftest cases and
3 of its own mutants falsely survived; that snapshot was never delivered and is superseded by
`d7c536a4`, on which everything below was measured). Final hashes re-verified after all runs.

## 1. Own-battery tallies (commands + outputs)

### R82-C1 — `round82_c1_plans_registry.py`
```
$ python3 counters/round82_c1_plans_registry.py --selftest --work work/c1s2
CASE green ok / missing-row ok / empty-cells ok / drop-entry ok / excluded-cli ok
CASE prose-only ok / selftest-unbacked ok / verdict-map ok
SELFTEST cases=8 red=7 failures=0            rc=0
$ python3 counters/round82_c1_plans_registry.py --mutants --work work/c1m2
MUTANTS real=7 killed=7 survived=0           rc=0
$ python3 counters/round82_c1_plans_registry.py --control-{empty-rows,exclude-cli,name-only} --work work/c1c2
CONTROL empty-rows caught=True target_reached=False
CONTROL exclude-cli caught=True target_reached=False
CONTROL name-only caught=True target_reached=False
```
No survivor in its own battery.

### R82-C2 — `round82_c2_closure_debt.py` (+ `round82_c2_checks.py`)
```
$ python3 counters/round82_c2_closure_debt.py --selftest --work work/c2s
CASE green ok / dropped-row ok / presence ok / no-index ok / status-open ok
CASE close-unresolved ok / check-trivial ok
SELFTEST cases=7 red=6 failures=0            rc=0
$ python3 counters/round82_c2_closure_debt.py --mutants --work work/c2m
MUTANTS real=6 killed=6 survived=0           rc=0
$ python3 counters/round82_c2_closure_debt.py --control-presence --work work/c2ctrl
CONTROL presence caught=True target_reached=False
```
Checks subcommands at the tip: `for u in u1..u7: python3 plans/round82_c2_checks.py $u` →
u1..u5,u7 rc=0; u6 rc=1 (in-flight: `.ufo/waves/round-82/w1-results.json` is written by the L1
after this wave; the matching `CHECK-FAIL R81-V6` in the live evaluate is the same pending
artifact, not a counter defect). Sensitivity leg on the real lane:
`python3 plans/round82_c2_closure_debt.py --lane . --sensitivity --work $S/work/c2sens` →
`SENSITIVITY n=7 failed_at_base=7` rc=0 (all seven checks fail at `a3a03ac…`, as the claim requires).

### R82-C3 — `round82_c3_sweep.py`
```
$ python3 counters/round82_c3_sweep.py --selftest --work work/c3s2
12 cases, all ok (green + missing-status-line, extra-member, histogram-sum, histogram-count,
command-mismatch, projection-unchecked, diff-count, diff-overflow, no-run, predicate-fail,
target-inconsistent)
SELFTEST cases=12 red=11 failures=0          rc=0
$ python3 counters/round82_c3_sweep.py --mutants --work work/c3m2
MUTANTS real=11 killed=11 survived=0         rc=0
$ python3 counters/round82_c3_sweep.py --control-{ledger-copy,exit-only,fabricated-line} --work work/c3ctrl
CONTROL ledger-copy caught=True target_reached=False
CONTROL exit-only caught=True target_reached=False
CONTROL fabricated-line caught=True target_reached=False
```
No survivor in its own battery.

## 2. New mutants per counter (not in its own battery)

Detector = the counter's own check over its own green fixture (C1: third commit on the fixture
tip; C2/C3: mutated fixture tree), exactly mirroring each `--mutants` mode.

### R82-C1 — 5 new mutants, **all 5 SURVIVED**

| mutant | construction | verdict | defect expected |
|---|---|---|---|
| `dup-name-diff-entry` | second row named `tool-a`, different valid entry | **SURVIVED** rc=0 | none exists |
| `dup-name-identical` | byte-identical duplicate of the `tool-b` row | **SURVIVED** rc=0 | none exists |
| `entry-not-claimed-file` | new row `fake-x` whose entry is the existing, parsing `plans/tool_b.py` | **SURVIVED** rc=0 | none exists |
| `exclusion-lie-registered` | EXCLUSIONS tables `plans/tool_a.py` (argparse+`__main__`) as `support-module` while its row stays | **SURVIVED** rc=0 | none examined |
| `exclusion-phantom` | EXCLUSIONS tables `plans/ghost.py`, which exists nowhere | **SURVIVED** rc=0 | none examined |

Survivor analysis (code paths and one-line fixes):
1. **Duplicate row names** — `evaluate()` never compares rows to each other; the row-quality leg
   (`row_defects`, line 130) validates cells of each row in isolation and the reverse leg collapses
   entries into a `set` (line 203). Code path: `for r in rows: … row_defects(r, …)` with no
   name-uniqueness check. Fix: `names = [r[0].strip("`") for r in rows]; defects += [("ROW-DUPLICATE", n) for n in names if names.count(n) > 1]`.
2. **Name↔entry mismatch** — the frozen row-quality rule only requires "an existing script that
   parses with `ast.parse`" (`row_defects` ENTRY branch); nothing binds the entry to the name, so a
   row for `fake-x` can point at `tool_b.py`. This is a **contract gap, not a counter defect**: the
   counter implements the frozen rule literally. If the L1 wants the binding, the fix is to derive
   the expected path from the name and compare.
3. **EXCLUSIONS never verified for registered instruments or phantoms** — the universe loop skips
   registered instruments *before* reading the exclusion table (`evaluate` line 218
   `if p in registered: continue`), and only universe members reach lines 219–224. A lying or
   phantom EXCLUSIONS entry for a registered path (or a nonexistent one) is never examined, though
   the counter's own docstring states the table invariant unconditionally ("a path here must prove
   it cannot be a CLI instrument from its own bytes at BASE_REV"). Fix: after the universe loop,
   `for p in EXCLUSIONS: body = base_body.get(p) or show(lane, base_rev, p) or ""; if not body or has_cli(body): defects.append(("EXCLUSION-CLI", p))`.

### R82-C2 — 6 new mutants, 2 killed / 4 SURVIVED

| mutant | construction | verdict |
|---|---|---|
| `check-true-on-empty-tree` | row check `python3 -c "pass"` (not matched by TRIVIAL) | **SURVIVED** evaluate rc=0; empty-tree probe rc=0 |
| `close-points-at-spotcheck` | `close` = the spot-check path, everything else good | killed (CLOSE-NOT-REPAIR) |
| `evidence-literal-absent` | `evidence_literal` not present in the close artifact's bytes | killed (CLOSE-NO-EVIDENCE) |
| `evidence-literal-empty` | `evidence_literal` set to `""` | **SURVIVED** rc=0 |
| `duplicate-row-id` | two identical rows for `R77-V1` | **SURVIVED** rc=0 |
| `source-prose-line` | `source` points at a prose line that mentions `R77-V1`, not the §5 routed-defect line | **SURVIVED** rc=0 |

Survivor analysis:
1. **`check-true-on-empty-tree`** — `evaluate()` only rejects checks matching `TRIVIAL`
   (line 55: `true|:|exit 0|echo .*|/bin/true`); `python3 -c "pass"` passes the filter, exits 0 at
   the tip, and — as probed — exits 0 in an empty directory, so it can never fail anywhere. It is
   killed **only** by the separate `--sensitivity` mode (`sensitivity()` reverts to BASE_REV and
   requires failure; a universally-0 check prints `PASSES-AT-BASE` and fails the mode). The frozen
   claim's sensitivity leg is thus enforced in a mode the main verdict does not run: if the L1's
   receipt ever runs only `--lane .`, this class sails. One-line fix: in `evaluate()`, also reject
   checks that do not reference any path/id from the row (e.g. require a literal from `close` or the
   id in the command), or fold the sensitivity run into the main verdict.
2. **`evidence-literal-empty`** — line 184: `if lit and lit not in body:` skips the leg entirely
   when the literal is empty, so a row with no evidence literal passes. Fix: `if not lit: defects.append(("NO-EVIDENCE", rid)) elif lit not in body: …`.
3. **`duplicate-row-id`** — `load_rows` (line 96) keys a dict by id and silently keeps the last row;
   the frozen claim says "exactly one row". Two identical rows are invisible to every leg, and
   `DEBT-TOTAL registered=` counts ids, not rows. Fix: count rows per id before dict-ing and emit
   `ROW-DUPLICATE` when any id appears more than once.
4. **`source-prose-line`** — line 171 requires only that the cited line *contains* the short id
   (`"V%d" % i in spot_lines[line_no-1]`), not that it is the §5 routed-defect line. This one is a
   **loose frozen sentence** ("the line that carries the short id"): a prose line does carry it.
   Severity low; fix if desired: require `ID_LINE` (`^- \*\*V<n> · `) to match the cited line.

### R82-C3 — 5 new mutants, 2 killed / 3 SURVIVED

| mutant | construction | verdict |
|---|---|---|
| `dup-member-identical` | `MEMBER m1` line duplicated adjacently, byte-identical | killed (MEMBER-DUPLICATE) |
| `histogram-class-sum-25` | `HISTOGRAM-CLASS file-artifact=24 numeric-band=1 sum=25` | killed (HISTOGRAM-CLASS-SUM + HISTOGRAM-CLASS) |
| `projection-compares-nothing` | `MEMBER m1 status=reproduced` with `PROJECTION m1 lines=0 sha256=sha256("")` | **SURVIVED** rc=0 |
| `projection-compares-nothing-diverged` | same empty projection on the `diverged:1` member | **SURVIVED** rc=0 |
| `map-extra-member` | map gains a 27th member `m9` not in the ledger | **SURVIVED** rc=0 |

Survivor analysis:
1. **`projection-compares-nothing` (both variants)** — `check()` validates a PROJECTION line's
   *presence* only (`if name not in proj:` → PROJECTION-UNCHECKED, line 219); the stored
   `lines=`/`sha256=` are never re-derived or even sanity-checked (a committed-bytes check cannot
   re-hash the past run, but it can check structure). A receipt can therefore claim `reproduced`
   while its projection compares nothing. A real `run()` never writes this pair for a reproduced
   member (empty stdout ⇒ `unrunnable:no-observations`), so the hole needs a hand-edited receipt —
   exactly what a laundered census would look like. One-line fix: in the member loop,
   `if st != "unrunnable" and proj[name][0] == 0: defects.append(("PROJECTION-EMPTY", name))`.
2. **`map-extra-member`** — `check()` derives `want` from the ledger (line 197) and never asserts
   `set(map.members) == set(executed)`; extra map keys are ignored (TARGET's `members=` is
   ledger-derived too). Latent, not exploitable under the frozen 26-member map. One-line fix:
   `if set(mmap) - set(led): defects.append(("MAP-EXTRA", …))` (and `MAP-MISSING` for the reverse).

## 3. Do the counters kill real corruption? Before/after on the lane itself

Materialised `a3a03ac31451e58f1742b9bccb73b72c2d90a95c` into a scratch worktree and ran each
counter against it (read-only), then against the live tip:

| counter | at BASE (before) | at tip (in-flight, c804dd41 + worktree) |
|---|---|---|
| C1 | `MISSING 4` (log_appendonly, round37_c1_attribution, round66_registry_check, round80_c1_remit) + `UNCLASSIFIED 2` (fixture_fence, policy_cases), `DEFECTS n=6`, rc=1 — exactly the frozen before-state | `missing=0 unclassified=0 excluded=2 rows=140 entry_missing=0`, `PREDICATE R82-C1 pass`, rc=0 |
| C2 | 7× `DEBT-UNREGISTERED` + `INDEX-MISSING`, `DEFECTS n=8`, rc=1 — exactly the frozen before-state | ids=7 closed=7, one `CHECK-FAIL R81-V6` (pending `w1-results.json`, written post-wave); sensitivity leg 7/7 fails-at-base |
| C3 | `SETUP map absent`, rc=2 — no target line printable, as frozen | `--check` → `TARGET members=26 located=26 status_lines=26 histogram_total=26 mismatches=0`, `PREDICATE R82-C3 pass`, rc=0; `--verify-at-tip` → `VERIFY-AT-TIP pass` |

## 4. What I attacked and what I could not break

- **Attacked**: all three counters' own batteries (no survivor), their frozen controls (all lose),
  16 new mutants across the three counters (5 C1, 6 C2, 5 C3), the C2 checks subcommands u1–u7, the
  C2 sensitivity mode, the C3 `--verify-at-tip` mode, and the before/after legs on the real lane.
- **Could not break**: the counters' own mutation batteries (C1 7/7, C2 6/6, C3 11/11 killed) and
  every frozen control; the before-state reproduction is exact for all three claims; C2's mandated
  mutants `close-points-at-spotcheck` and `evidence-literal-absent` die on the expected legs; C3's
  `dup-member-identical` and `histogram-class-sum-25` die on MEMBER-DUPLICATE / HISTOGRAM-CLASS-SUM.
- **Coverage findings (survivors), by severity**:
  1. C1: EXCLUSIONS table entries are verified only for *unregistered* universe members
     (`evaluate` line 218) — lying/phantom entries for registered instruments pass. Fix given above.
  2. C2: an always-0 check (`python3 -c "pass"`) passes the main verdict; only the separate
     `--sensitivity` mode kills it — the sensitivity leg must be part of the acceptance receipt.
  3. C1: duplicate registry row names pass both legs (no cross-row check).
  4. C2: duplicate routed-findings rows for one id are silently collapsed (frozen claim says exactly one).
  5. C2: an empty `evidence_literal` skips the evidence leg.
  6. C3: `reproduced`/`diverged` members may carry an empty projection (`lines=0 sha256=sha256("")`)
     — the presence check passes while the comparison compares nothing.
  7. Contract looseness (counters implement the frozen sentence literally; flag to L1, not code bugs):
     C1 name↔entry binding, C2 `source` may cite any line carrying the short id, C3 map may carry
     extra members.

No pacman/uv/npm installs were needed (stdlib only); nothing outside my scratch dir, the report
path, and read-only lane commands was touched. Scratch deleted.
