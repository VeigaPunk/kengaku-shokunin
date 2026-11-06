# ScribeLesson — draft `SKILL.md` `## Gate/probe registry` row for the round-95 census and counter

Seat ScribeLesson (leaf scribe). Draft only; the L1 integrates. Nothing here is committed
by me. The lane was read-only.

## Where the row goes

`SKILL.md:592` holds `## Gate/probe registry (PROTOCOL §Gate standard)` and `SKILL.md:594`
the table header:

```
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
```

Eight columns; a row splits into ten pipe-separated cells (the empty first and last). The
round-94 row (`freeze-integrity`, `SKILL.md:698`) sits at the **end of the first table
block**; the second block runs `SKILL.md:700`–`SKILL.md:760` and ends with
`round89-claim-figures` (`SKILL.md:760`). Prose boundary notes begin at `SKILL.md:762`.

**Placement.** The round-95 rows are round-95 instruments and the registry's second block
is where the recent rounds live, so append them at the end of the second block, after
`SKILL.md:760` and before the prose at `SKILL.md:762` — i.e. the registry's last row
becomes the round-95 census. (The alternative, putting them beside `freeze-integrity` at
`SKILL.md:698`, is also defensible: the census is the round-95 successor of the
round-94 counter that row names, and adjacency makes the supersession visible. The L1
should pick one and not both.)

**Two rows, not one.** The task asks for a row for `plans/round95_false_gate_census.py`
**plus** `plans/round95_c2_counter.py`. These are two instruments with two different
entry points, two different verdict maps and two different write scopes, and the
registry registers one entry point per row (`round37-c2` and `regex-log-probe` are
separate rows; `round41-c1-mutants` and `round41-c2` are separate rows). Two rows it is.
The census row names the counter in its `pinned values` cell, mirroring how the
`freeze-integrity` row names `plans/round94_c2_counter.py` in its own `pinned values` cell.

**No name collision.** Measured with the lane's own cell splitter
(`re.compile(r"(?<!\\)\|")`, the same `CELLSPLIT` the ledger gate uses):
`grep -c -F "| \`round95-false-gate-census\` |" SKILL.md` = 0 and the same for
`round95-c2-counter`; `grep -c "round95" SKILL.md` = **0** — the registry has no
round-95 row at all, which is why this draft supplies two.

The `freeze-integrity` row's shape, verified with that splitter: **8 content cells**
(`name`, `kind`, `entry`, `verdict map`, `self-test`, `pinned values`, `write scope`,
`owner`), split into 10 pipe-separated fields by a naive `awk -F'|'` because the `entry`
cell contains an escaped `\|` (`--claims … \| --paths …`). The two rows below are written
in the same escaped form, so a reader splitting them naively sees the same 10 fields the
existing row produces.

## Proposed row 1 — the census

```
| `round95-false-gate-census` | probe | `python3 plans/round95_false_gate_census.py --lane . --rev REV --work DIR [--counter PATH]` | `0` every known false gate is red at its designated leg and the honest gate passes (`FALSEGATES total=14 passing=0 designated_red=14 honest=pass`, then `PREDICATE R95-C2 pass`) · `1` any of: a known false gate still passes (`passing>0`), a designated leg is not red (`designated_red<14`), or the honest gate fails (`honest=fail`) → `PREDICATE R95-C2 fail` · `2` could-not-evaluate (`DEFECT SETUP <reason>` then `PREDICATE R95-C2 could-not-evaluate`: `--work` inside the lane, unresolved revision, counter absent at the revision, the false-gates table absent at the revision, a row's file absent / sha-mismatched / undesignated, or a population that is not the 14 rows) | none declared at write time: no `--selftest` flag exists (measured — the parser rejects `--selftest` with rc 2); the census's own battery is its 14-row population plus the honest run, and the counter it drives carries the W1–W5 legs | the 14 rows of `plans/round95-false-gates.tsv` (id, path, sha256) read at `--rev`, every row's file re-hashed against the table; the counter under test `plans/round95_c2_counter.py` read at `--rev` (its sha256 printed on the `COUNTER … sha256=… REV …` line); the honest gate `plans/round94_freeze_integrity.py` (sha256 `8574b4d5dca7f38…`, unchanged since round 94) | none in the lane — read-only git; the counter and the 14 gate files are copied into `--work`, and a `--work` inside the lane is refused with rc 2 | kengaku |
```

## Proposed row 2 — the counter

```
| `round95-c2-counter` | gate | `python3 plans/round95_c2_counter.py --lane . --rev REV --work DIR [--tool-file PATH]` | `0` W1–W5 all pass → `TARGET legs_passed=5 of 5` then `PREDICATE R95-C2 pass` · `1` any leg red (a `W1 fail`…`W5 fail` line) or the gate under test absent at the revision (`TOOL absent at <rev>`, every leg `fail tool-absent`, `TARGET legs_passed=0 of 5`) → `PREDICATE R95-C2 fail` · `2` could-not-evaluate (`DEFECT SETUP --work inside the lane` / `DEFECT SETUP unresolved-revision`, then `PREDICATE R95-C2 could-not-evaluate`) | none declared at write time: no `--selftest` flag exists (measured — the parser rejects `--selftest` with rc 2); the battery is in-process and prints as the run proceeds — `W1 pass`, `W2 pass fixtures=20 ok=20`, `W3 pass probes=3`, `W4 pass freeze=<sha> rc=0 summary=(11, 11, 0)`, `W5 pass mutants=10 killed=10`, with `W5 null ok fixtures_ok=20 of 20` guarding the null copy | the gate under test `plans/round94_freeze_integrity.py` at `--rev` (or the file named by `--tool-file`); the round-92 and round-93 history windows and their freeze/tip revisions (W1); the round-95 claims file `plans/round-95-claims.md` (W4, whose freeze is the single commit that added it); the ten CLI-path mutants K1–K10 and the three gate-battery probes P1–P3, each with its designated W2 fixture | none in the lane — read-only git; fixture repos and the gate copy live under `--work`, and a `--work` inside the lane is refused with rc 2 | kengaku |
```

## Column-by-column, with the source of every claim

**name** — `round95-false-gate-census`, `round95-c2-counter`. No collision with the
registry's 164 existing rows (measured, above); the registry had no round-95 row.

**kind** — `probe` for the census, `gate` for the counter. The registry's convention,
read off the existing rows: a **probe** reports a measurement and its verdict map names
`0`/`2` outcomes (`coverage-census`: "`0` census completed even with gaps · `2`
could-not-evaluate"; `db-wal-probe`: "`0` all 28 cases produced seven test verdicts twice
each, exit `2` a setup failure"). The census is a **count** over a population whose
`PREDICATE` line is read by the claims file, so it is probe-shaped. The **counter**
decides a predicate and returns 0/1/2 on `PREDICATE R95-C2 pass|fail` with a red battery
case distinguishable from a breach — the same shape as the `freeze-integrity` gate it
replaces as the round-95 judge of the freeze-integrity gate, and the same shape as
`round40-c2`, `round41-c2` and their siblings.

**entry** — read from each script's own argparse, not paraphrased:
`plans/round95_false_gate_census.py:80-84` declares `--lane` (default `.`), `--rev`
(default `HEAD`), `--work` (**required**), `--counter` (optional, default: the counter
read at `--rev`); `plans/round95_c2_counter.py:299-303` declares `--lane` (default `.`),
`--rev` (default `HEAD`), `--work` (**required**), `--tool-file` (optional: the gate
under test, else `plans/round94_freeze_integrity.py` at `--rev`). The census's `--counter`
is what lets the round's do-nothing control score a *different* counter with the same
harness — measured on the committed do-nothing receipt, whose `COUNTER` line reads
`round94_c2_counter.py sha256=17d2a7d5…`, and `git show HEAD:plans/round94_c2_counter.py |
sha256sum` is exactly `17d2a7d52fbd703db1c4df661168f22a36481f289962ea66d5e98a0466190b98`.

**verdict map** — read from each script's exit paths:
- census `plans/round95_false_gate_census.py:146-147` prints
  `FALSEGATES total=14 passing=<n> designated_red=<n> honest=<pass|fail>` then
  `PREDICATE R95-C2 pass` iff `passing == 0 and designated_red == 14 and honest == "pass"`,
  else `PREDICATE R95-C2 fail`; return 0 / 1.
- census rc 2 comes from exactly six `DEFECT SETUP` sites, each printing
  `PREDICATE R95-C2 could-not-evaluate` (lines 76-77, 82-83, 91-92, 99-100, 109-110,
  116-117): `--work` inside the lane; unresolved revision; counter absent at the
  revision; the tsv absent at the revision; a row's file absent / sha-mismatched /
  undesignated; a population that is not 14 rows. The draft names all six.
- counter `plans/round95_c2_counter.py:428-429` prints `TARGET legs_passed=<n> of 5` then
  `PREDICATE R95-C2 pass|fail`, return 0/1; rc 2 from lines 307-309 (`--work` inside the
  lane) and 313-315 (unresolved revision); the `TOOL absent at <rev>` path (lines
  325-330) prints `TOOL absent at <rev>`, one `<leg> fail tool-absent` per leg and
  `TARGET legs_passed=0 of 5`, and returns **1** — a fail, not a setup — which the draft
  states.
- The `PREDICATE R95-C2` predicate name is shared by both scripts (`grep -n "PREDICATE
  R95-C2"`), so a reader who greps for it sees the census's line and the counter's line;
  the registry row for each names which script emits it.

**self-test** — measured, both scripts: `python3 plans/round95_false_gate_census.py
--selftest …` and `python3 plans/round95_c2_counter.py --selftest …` both exit **2** with
the parser's `unrecognized arguments: --selftest`. Neither script has a `--selftest`
flag, so the cell must not claim one. The draft instead names what the instruments
actually print, because that is the reproducible spelling a reader can check:
- census: `GATE <id> sha=<12> rc=<rc> passes=<0|1> designated=<leg> designated_red=<0|1>`
  per population row, `HONEST rc=<rc> predicate=<pass|fail>`, then the `FALSEGATES …`
  summary. The committed receipt `.ufo/waves/round-95/L1/c2-tip.txt` carries exactly
  these lines.
- counter: the W-leg lines are printed as the run proceeds, not by a separate flag —
  `W1 pass`, `W2 pass fixtures=20 ok=20`, `W3 pass probes=3`,
  `W4 pass freeze=d9cd18a7519a rc=0 summary=(11, 11, 0)`, `W5 pass mutants=10 killed=10`,
  and `W5 null ok fixtures_ok=20 of 20` (the null copy that must stay green). Read from
  the committed receipt `.ufo/waves/round-95/L1/c2-tip-honest-counter.txt`.
The registry's own convention for a tool with no `--selftest` flag is to name the printed
tally: `round28-census` names "the census entry point"; `coverage-census` says "none
declared at write time (spelling owned by the census seat)". The draft follows the second.

**pinned values** — census: `plans/round95-false-gates.tsv` (15 lines: a 3-line header
comment plus `id path sha256`, 14 rows — measured: `grep -vc "^#" plans/round95-false-gates.tsv`
= 15, so 1 header line `id\tpath\tsha256` plus 14 rows), the counter under test, and the
honest gate `plans/round94_freeze_integrity.py` whose sha256 `8574b4d5dca7f38…` is the
**frozen-table** value in `plans/round-95-claims.md` (row 7 of the `frozen-instruments`
block) and is unchanged since round 94 — the census reads it from `--rev`, so a change to
it would change what the census judges. counter: the gate under test at `--rev` (or
`--tool-file`), the two history windows (W1: `R92_FREEZE f0018773…` / `R92_TIP 1df76536…`
and `R93_FREEZE d8d0a4b8…` / `R93_TIP 7b8719f3…`), the round-95 claims file (W4) and its
frozen table, and the ten CLI mutants K1–K10 plus three battery probes P1–P3 with their
designated W2 fixtures (`plans/round95_c2_counter.py`: `MUTANTS` at `:70-88`, ten entries;
`BATTERY_PROBES` at `:92-96`, three entries).

**write scope** — measured for both scripts: each refuses a `--work` inside the lane with
`DEFECT SETUP --work inside the lane <path>` and rc 2 (census `:75-78`, counter `:307-309`;
measured: `python3 plans/round95_false_gate_census.py --lane . --rev <T> --work ./inlane2`
→ `DEFECT SETUP --work inside the lane …/inlane2`, rc 2; the counter likewise, rc 2).
Both write only under `--work`: the census copies the counter-under-test and the 14 gate
files there and writes `out-<id>.txt` per gate; the counter copies the gate under test to
`gate-under-test.py` and builds its fixture repos under `--work`. Neither mutates the
lane: the census's git calls are `rev-parse` and `show` only, and the counter's are the
same plus `log --diff-filter=A` for the W4 freeze commit.

**owner** — `kengaku`, like every other row of this table.

## What the draft deliberately does not claim

- It does not claim the census is a *gate* in the sense of the freeze-integrity gate it
  judges. The census scores a population of gates through the counter's CLI; the gate
  under test (`plans/round94_freeze_integrity.py`) keeps its own registry row, unchanged.
- It does not claim the round-95 counter supersedes `plans/round94_c2_counter.py` in the
  lane's instruments. The round-94 counter is still the judge named in the
  `freeze-integrity` row and is still in the tree; the round-95 counter is the round-95
  judge, and the claims file freezes both by sha256. If the L1 wants the supersession
  visible, the change belongs in the `freeze-integrity` row's `pinned values` cell, not
  in the new rows — and that cell is not mine to edit.
- It does not claim the census is a clean cutover. The round-95 census's own scope
  statement calls the fourteen false gates "the recorded set the counter was built
  against" (in-sample), and the L1's own report says so. A registry row is an interface
  description; the scope belongs in the claims file, where it already is.
