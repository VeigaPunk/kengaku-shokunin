# R38BatP3 — battery38 fixture for mutant N02 (P3, mirror)

Seat: executor R38BatP3, wave 1 of kengaku round 38. Lane `kengaku-shokunin`, freeze commit
`e0a378539a45cc9388c66cfba22f44275131de23`, first recorded probe run `e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b`.
No lane file was touched: the delivered artefact is `plans/battery38/p3m.py` **drafted** at
`.ufo/waves/round-38/build/R38BatP3/battery/p3m.py` for the L1 to integrate. Scratch was
`/fast/scratch/hyaku/kengaku-r38/R38BatP3` (clone of the lane, removed at the end).

## 0. Axes (godspeed)

- **calibration** — the axis the seat moves: N02 was one of 22 advertised gate behaviours with no attributed
  kill; this fixture is a calibration sample, not a claim about the gate.
- **operability** — kept cheap: one fixture, one mutant, stdlib only, no new helper surface, deterministic bytes.
- **no-harm** — zero edits to the frozen gate / counters / spec / probe / captures / dry table, and no lane write.

## 1. The mutant, read at the frozen digest

`plans/round38_c1_verify.py`, MUTANTS row N02 (`plans/pkg_gate.py` digest `ea63882240e6…`):

```
("N02", "P3", "mirror", "a package with exactly min_distinct_locations quote lines is accepted [Q24 'the genuine
 package must be accepted'; F37XMutP23 X2]",
 'len(locs) >= rules["min_distinct_locations"]', 'len(locs) > rules["min_distinct_locations"]'),
```

Gate branch (`plans/pkg_gate.py:132-136`): `locs = {(q.capture, q.start) for q in p.quotes}` then
`ok = len(texts) >= rules["min_quotes"] and len(locs) >= rules["min_distinct_locations"] and not short`.
Frozen round-35 spec (`plans/pkg-spec-r35.json`, `entry_rules`): `min_quotes=8`, `min_distinct_locations=8`,
`quote_words=[3,25]` — so the genuine package sits exactly on the boundary and `>=` → `>` flips it.

Attribution requirement (mirror): reference prints `P3 ok`, mutant prints `P3 DEFECT`, both exit 0/1, `argv[0]`
in the P-family. A red-side fixture cannot do this (it would need P3 to fail under the reference).

## 2. The fixture

`p3m.py` → `FIXTURES = [{"fid": "p3m-exact-min-distinct-locations", "expect": "accept", "defects": [], "build": build}]`

`build(ctx, d)`:
1. `ctx.genuine_package(d)` — git-inited clone of the genuine round-35 package (`corpus/` entry, receipt,
   sources, README, three frozen instruments, capture dir, knowledge + lessons files).
2. reads `min_distinct_locations` (8) from `ctx.spec["entry_rules"]` (never hardcoded).
3. `ctx.r36.rewrite_quotes(...)` cuts the entry's `## Located quotes` table to the first 8 genuine data rows
   with pairwise-distinct texts **and** pairwise-distinct `(capture, start)` locations. Rows are kept verbatim
   from the entry, so they are already verbatim on their cited line (3–25 words) — nothing is synthesised.
4. `ctx.git_add(d)` (index only) so P9 `--require-clean-tree` is green.
5. returns `["package", "--root", str(d), "--require-clean-tree"]` (no `--rerun`: P10 would need the pinned
   probe; no `--spec`: the counter appends the frozen r35 spec).

Genotype of the genuine table, measured (`python3` over the entry, header stripped): 22 data rows,
`distinct texts 22`, `distinct locs 22`, all rows 3–25 words — the first 8 rows (`test_outputs.py:13…28`)
satisfy 8/8/8, so the fixture is exactly the boundary case and every other clause is untouched.

Module source tokens: no `/proc`, `ppid`, `cmdline`, `psutil`, `environ` (counter `sidechannel=0`, see §3).

## 3. Kill evidence (exact output)

Command (from the fleet root; lane clone in scratch, battery dir = the drafted module's dir):

```
S=/fast/scratch/hyaku/kengaku-r38/R38BatP3; export TMPDIR="$S"; mkdir -p "$S/w"
python3 plans/round38_c1_verify.py --lane "$S/lane" \
  --battery-dir .../round-38/build/R38BatP3/battery --only N02 --work "$S/w"
```

Output (full receipt: `counter-n02.txt` beside this report):

```
FIXTURE p3m-exact-min-distinct-locations expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N02 P3 mirror killed by=p3m-exact-min-distinct-locations -- a package with exactly min_distinct_locations quote lines is accepted [Q24 'the genuine package must be accepted'; F37XMutP23 X2]
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

`fixtures=65` = round-36 battery + battery37 (64, unchanged, all `ok`) + this one module's single fixture.
`wrong=0 renamed_disagree=0 sidechannel=0 null_detected=0` on the whole 65-fixture set.

Direct reference/mutant clause lines on the same built fixture (driver in scratch, output kept as
`direct-p3-lines.txt`):

```
reference: rc=0 P3 ok rows=8 distinct_quotes=8 distinct_lines=8 out_of_word_range=0
N02: rc=1 P3 DEFECT rows=8 distinct_quotes=8 distinct_lines=8 out_of_word_range=0
```

Same `rows/distinct_*` note on both sides — the only difference is the verdict, i.e. the kill is the boundary
`>=` → `>` and nothing else.

## 4. Load-bearing table (fixture removed → mutant survives)

| state | BATTERY line | N02 result |
|---|---|---|
| `p3m.py` present | `BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0` | `killed by=p3m-exact-min-distinct-locations` |
| `p3m.py` absent (`--battery-dir "$S/empty"`) | `BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0` | `MUTANT N02 P3 mirror SURVIVED` |

Receipt: `counter-n02-fixture-removed.txt` (`MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0`).
The module has exactly one fixture, so "each fixture deleted in turn" is this single line; nothing else in the
module contributes a kill.

## 5. Artefact and digest

```
851d4e82829b9b8fa688180bcba6295e531267d58b05e32af0b088d6d95c57d8  .ufo/waves/round-38/build/R38BatP3/battery/p3m.py
```

60 lines, stdlib only (`pathlib`), no I/O outside the fixture dir the counter hands it. Intended landing path
`plans/battery38/p3m.py`; `fid` prefix `p3m-` per seat.

## 6. Risks and limits

- **Counter coincidence with sibling seats.** The kill was measured with only this module in `--battery-dir`
  (plus the pinned r36/r37 batteries). At landing, sibling battery38 modules coexist; the counter takes the
  *first* fitting fixture per mutant, and no sibling may reuse the `p3m-` fid prefix. A sibling fixture that
  also happens to kill N02 would not hurt, but if two modules define the same fid the counter exits 2
  (`SETUP duplicate fixture id`) — prefix discipline is the guard.
- **The fixture depends on the genuine entry having ≥8 unique rows.** Measured 22 unique today; if the L1
  ever rewrites the genuine quote table below 8 unique rows the builder raises, so it fails loud, not silent.
- **Attribution is clause+direction, not intent** (as the claims file names it): the kill is
  "reference P3 ok, mutant P3 DEFECT", which is exactly what N02 breaks; no other clause differs.
- Not run here by design: the full 22-mutant predicate, the no-harm round-37 run, pins and integration — parent
  gate work at landing tip.

## 7. Tooling

No install, upgrade or environment change was made. No pacman transaction attempted. Nothing was committed,
staged in the lane, or written outside this seat's report dir and scratch; scratch removed.

VERDICT: battery38-p3m-killed-1/1-wrong-0
