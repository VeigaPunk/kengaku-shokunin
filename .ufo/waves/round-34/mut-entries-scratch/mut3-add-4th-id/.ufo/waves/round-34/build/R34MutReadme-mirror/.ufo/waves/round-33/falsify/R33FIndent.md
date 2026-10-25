# R33FIndent — duplicate id at four leading spaces vs the 0–3-space collision anchor

Seat: R33FIndent (executor, leaf). Date: 2026-10-25. Lane: kengaku-shokunin (tip `77ac8c1` at
measurement time; other seats' in-flight edits present and untouched — see §Notes).
Target: the C1 id-collision extractor's anchor, `^ {0,3}\|` —
`plans/sources_adopt.py:43` `ROW_RE = re.compile(r"^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|")`,
`plans/adoption_check.py:33`, `plans/round33_c1_verify.py:46`, `plans/round28_census.py:40`, and
the shell pipeline that *is* the round's guard (`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`).

Claim under test — `plans/round-33-claims.md` §C1 kill rule, verbatim:

> The scratch id-collision guard (0–3 leading spaces, both id lists) runs before any append and
> its proof fixture is committed under `.ufo/waves/round-33/assimilation/`.

plus its build receipt `.ufo/waves/round-33/build/R33IdGuard.md` F1 (§5 fixture is `  | S002`, two
spaces) and the build critic's row `.ufo/waves/round-33/build/R33C1KillRule.md:45` (row 6,
"0–3-space anchor missing an over-indented row", UNCAUGHT, medium), which this seat materializes.

## Method (all in /tmp; lane read-only)

Sandbox `/tmp/r33f-indent`. Fixtures are one 11-cell registry row
`| S001 | fixture source row | code | A | lane scope | anchor text | teaches thing | mined | 2026-10-25 | 180d | corpus/knowledge/x.md |`
under `## Registry` + the 11-column header, differing only in the leading bytes before the pipe
(`0`, `1`, `3`, `4` spaces; `\t`; `3 spaces + \t`). One harness (`/tmp/r33f-indent/run-all.sh`)
produces every number below into `/tmp/r33f-indent/transcript.txt` (123 lines); the C1-counter
probe is `/tmp/r33f-indent/c1-probe.sh` → `c1-probe.out`. No lane file was edited, staged or
committed; the only lane path this seat writes is this report.

Anchor used everywhere (documented form, `[|]` instead of `\|` for shell quoting safety — same
ERE):

```sh
ANCH='^ {0,3}[|][[:space:]]*S[0-9]{3,}'
LOOSE='^[[:space:]]*[|][[:space:]]*S[0-9]{3,}[[:space:]]*[|]'   # any indent, as a human reads it
```

## 1. The anchor boundary, measured (registry side; staged set is one column-zero `S001`)

```sh
grep -oE "$ANCH" staged.md | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > staged.ids
grep -oE "$ANCH" "$f.md"   | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > "$f.ids"
LC_ALL=C comm -12 "$f.ids" staged.ids | wc -l
```

| registry fixture | leading bytes (`cat -A`) | `grep -cE "$ANCH"` | reg-ids | guard collision lines | `grep -cE "$LOOSE"` |
|---|---|---|---|---|---|
| `reg-c0.md` | `\| S001 …$` | 1 | `S001` | **1** | 1 |
| `reg-1sp.md` | ` \| S001 …$` | 1 | `S001` | **1** | 1 |
| `reg-3sp.md` | `   \| S001 …$` | 1 | `S001` | **1** | 1 |
| `reg-4sp.md` | `    \| S001 …$` | **0** | **∅** | **0** | 1 |
| `reg-tab.md` | `^I\| S001 …$` | **0** | **∅** | **0** | 1 |
| `reg-3sp-tab.md` | `   ^I\| S001 …$` | **0** | **∅** | **0** | 1 |

Inside the declared window the guard holds at every tested boundary (0, 1, 3 spaces → collision).
At 4 spaces, at a tab, and at 3-spaces-plus-tab the guard's registry id list is **empty**, so the
collision set is empty while a loose row-shape probe still sees the row.

## 2. The staged side is blind in exactly the same way

```sh
python3 plans/sources_adopt.py --registry reg-c0.md --package staged-4sp.md   # package row at 4 spaces
```

| package fixture | `grep -cE "$ANCH"` | staged-ids | guard collision lines | gate |
|---|---|---|---|---|
| `staged.md` (column zero) | 1 | `S001` | 1 | `exit=3 registry=1 staged=1 collisions=1` |
| `staged-4sp.md` (4 spaces) | **0** | **∅** | **0** | `exit=0 registry=1 staged=0 collisions=0` |

So both id lists the claim names ("both id lists") are extracted with an anchor that drops the row.

## 3. End-to-end: the gate *writes* the duplicate and exits 0

Registry holds `S001` **only** at four spaces; the package row is column zero; the id is admitted:

```sh
python3 plans/sources_adopt.py --registry reg-4sp.md --package staged.md \
  --admit-ids S001 --entries corpus/knowledge/x.md --access-date 2026-10-25 --out out-block.md
registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote /tmp/r33f-indent/out-block.md rows=1
gate exit=0
```

The block it wrote (`cat -A`, appended verbatim into `reg-after-append.md`):

```
| S001 | fixture source row | code | A | lane scope | anchor text | teaches thing | mined | 2026-10-25 | 180d | corpus/knowledge/x.md |$
```

After the append the file contains the same id twice — `    | S001 …` (line 5) and `| S001 …`
(line 6) — yet:

```
anchor_rows=1   loose_rows=2
grep -oE "$LOOSE" reg-after-append.md | grep -oE 'S[0-9]{3,}' | sort | uniq -d   →  S001
```

## 4. The duplicate survives every C1 counter

| counter | command | result on the post-append registry |
|---|---|---|
| `adoption_check.py` (C1 counting command) | `python3 plans/adoption_check.py --lane /tmp/r33f-indent/c1lane --expect expect.json` | `entries=1 indexed=1 cited_rows=1 rows_present=1 rows_mined=1 usedby_ok=1 census=skipped` — every printed counter green with the duplicate present; `census=skipped` only because the fleet census subprocess was deliberately not run (see §Notes) |
| `round33_c1_verify.registry_cells` | in-process | `registry_cells=1 ids=['S001']` |
| `round28_census.py` | `--root root-reg-after-append --revision fixture` | `sources.rows=1 malformed=0` |
| gate `duplicates` field | `sources_adopt.py --registry reg-dup3.md --package staged-s002.md` | `registry=2 staged=1 collisions=0 … duplicates=0`, `exit=0` |

`adoption_check.registry_rows` keys rows into a `dict`, so a second row for the same id is
**silently collapsed**, not reported: a 2-row file yields `rows=1`.

## 5. One lane parser does see it — the fleet holds two definitions of "registry row"

`plans/registry_check.py:36` uses `if not active or not line.lstrip().startswith("|"): continue`
(unbounded indent, fenced blocks skipped) and flags repeats at `:48`.

| fixture | `adoption_check` rows | `sources_adopt` rows | `registry_check` rows | `registry_check` findings |
|---|---|---|---|---|
| `reg-c0` | 1 | 1 | 1 | `[]` |
| `reg-3sp` | 1 | 1 | 1 | `[]` |
| `reg-4sp` | **0** | **0** | **1** | `[]` |
| `reg-tab` | **0** | **0** | **1** | `[]` |
| `reg-3sp-tab` | **0** | **0** | **1** | `[]` |
| `reg-dup3` (col 0 + 3 sp) | 1 | 2 | 1 | `['duplicate_source_id']` |
| `reg-dup4` (col 0 + 4 sp) | 1 | 1 | 1 | `['duplicate_source_id']` |
| `reg-after-append` (§3) | 1 | 1 | 1 | `['duplicate_source_id']` |

Real CLI run (id `S038`, inside the frozen 13-id population, fixture at
`/tmp/r33f-indent/rc2` with the lane's own `population.json` copied in):

```
python3 plans/registry_check.py --root /tmp/r33f-indent/rc2 --json
registry_check exit=1
finding histogram: {'duplicate_source_id': 1, 'used_by_missing': 1, 'source_missing': 12}
duplicate findings: [{'id': 'duplicate_source_id', 'line': 6, 'source': 'S038'}]
census anchor rows on the same file: 1
```

So the four-space duplicate is simultaneously "a registry row with a duplicate id" (registry_check,
line 6) and "not a row at all" (guard, gate, census, both C1 receipts). The guard uses the
narrower definition; nothing reconciles the two.

## 6. The evading behaviour is an asserted expectation, not an accident

`plans/sources_adopt.py:658-664` — the gate's own selftest:

```python
        # 4. 4-space indentation is outside the clause: no row, so no collision
        ...
        case(
            "four-space-not-a-row",
            code == EXIT_OK and report["staged"] == 0 and report["collisions"] == [],
        )
```

```
python3 plans/sources_adopt.py --selftest | grep -E 'CASE (collision|four-space)|SELFTEST'
CASE collision-zero-indent PASS
CASE collision-one-space PASS
CASE collision-three-space PASS
CASE four-space-not-a-row PASS
SELFTEST cases=17 failed=0
```

A "green = caught" fix at the anchor therefore fails the committed suite; the selftest has to move
with the predicate.

## 7. The committed proof fixture covers only two spaces

`.ufo/waves/round-33/assimilation/id-guard-fixture-registry.md`, `cat -A`:

```
7:  | S002 | indented fixture row that a column-zero anchor cannot see | docs |$
8:| S900 | registry-only row | docs |$
```

Republication with the documented anchor: `committed-fixture collision_lines=1 ids=[S002 ]`. The
proof reproduces, but it exercises neither the 3-space boundary nor the 4-space exclusion; only the
gate selftest covers 0/1/3 and asserts 4 as "not a row".

## 8. Live exposure today: zero

```
lane tip=77ac8c1
real registry anchor_rows=97 loose_rows=97
real registry 4+space rows: 0
real registry tab-leading rows: 0
real registry duplicate ids (loose shape): (none)
```

The landed `S103`/`S104` rows are column zero; the registry's two row definitions currently agree
row-for-row. The gap is latent, not active.

## 9. Even inside the anchor, the guard never inspects the registry for internal duplication

Registry `S001` at column 0 **and** at 3 spaces (both matched by the anchor), package names `S002`
only:

```
python3 plans/sources_adopt.py --registry reg-dup3.md --package staged-s002.md
registry=2 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
exit=0
```

`collisions()` is `registry_ids ∩ staged_ids` (`sources_adopt.py:129-130`) and `duplicate_ids()`
runs on the **staged** list only (`:133`); `adoption_check` collapses the pair to one row. A
duplicate already in the registry is therefore invisible to every C1 counter except
`registry_check`'s `duplicate_source_id`.

## Evidence retained

- `/tmp/r33f-indent/transcript.txt` (123 lines) — every table above, produced by
  `/tmp/r33f-indent/run-all.sh` in one run, exit 0.
- `/tmp/r33f-indent/c1-probe.sh`, `/tmp/r33f-indent/c1-probe.out` — §4 `adoption_check` and
  `round33_c1_verify` runs.
- `/tmp/r33f-indent/{reg-c0,reg-1sp,reg-3sp,reg-4sp,reg-tab,reg-3sp-tab,reg-dup3,reg-dup4,staged,staged-4sp}.md`
  — fixtures; `reg-after-append.md`, `out-block.md` — §3 append materialization;
  `rc2/` — §5 registry_check CLI root; `c1lane/`, `expect.json` — §4.
- Lane reads only: `plans/sources_adopt.py:43,95-113,129-140,658-664`, `plans/adoption_check.py:33,42-50`,
  `plans/registry_check.py:36,48`, `plans/round33_c1_verify.py:46,56`, `plans/round28_census.py:40`,
  `plans/round-33-claims.md` §C1, `.ufo/waves/round-33/build/R33IdGuard.md` §5, `R33C1KillRule.md:45`,
  `.ufo/waves/round-33/assimilation/id-guard-fixture-{registry,staged}.md`.

## Verdict

**UNCAUGHT — materialized, scope-bounded.** A duplicate id placed at four leading spaces evades the
collision extractor: the guard's registry id list is empty (`anchor_rows=0`, `collision_lines=0`),
the lane gate returns `exit=0 registry=0 staged=1 collisions=0`, and it *writes an append block*
for an id the registry already holds — after which the registry contains the id twice while
`anchor_rows=1`, `round28_census sources.rows=1`, `round33_c1_verify registry_cells=1` and
`adoption_check`'s six printed counters stay green. The same evasion holds for a tab-led row and
for three spaces plus a tab. Only `plans/registry_check.py` (unbounded-indent anchor) sees the row
and reports `duplicate_source_id`.

Caveat that keeps C1's literal predicate intact: the frozen claim scopes the guard to "0–3 leading
spaces", and inside that window the guard fires at every boundary tested (0, 1, 3) — the claim's
own sentence is not falsified. What is falsified is the guard's sufficiency as the round's
double-registration control: it is a 0–3-space extractor in a file format whose other parser reads
any indentation, and the gate's suite asserts the blind case as correct. This confirms
`R33C1KillRule.md` row 6 (UNCAUGHT, medium) with end-to-end evidence the critic did not have: not
"would double-register invisibly" but "does, and the gate emits the row".

## Risks / notes

- **Severity today: latent.** 0 out-of-anchor rows and 0 duplicate ids in the registry at
  `77ac8c1`; the landed C1 rows are column zero. The path becomes live for any append produced by a
  hand edit, a different renderer, or a registry table nested under a list item — CommonMark allows
  a table inside a list item at 4+ spaces of content indent, so "4 spaces is a code block" is not a
  universal defence [INFERENCE — not measured here].
- **Fix direction (not implemented, out of this seat's scope):** give the guard and the census the
  same row predicate `registry_check.py` already uses (`line.lstrip().startswith("|")` inside
  `## Registry`, fenced blocks skipped), or add an explicit duplicate-id check to
  `adoption_check.registry_rows`; changing the anchor alone fails the committed
  `four-space-not-a-row` selftest and must move with it.
- **Fleet census not executed.** `plans/adoption_check.py`'s `--census` invokes
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, which lives in the fleet repo (off-limits
  to this seat); the probe in §4 therefore prints `census=skipped` and exits 1 for that reason only.
  The lane's own audit records the fleet anchor as `^ {0,3}\|` followed by
  `sub(/^ {0,3}/,"",line)` (`.ufo/waves/round-29/attempt2/build/R29a2GateAudit.md:298-299`), so the
  fleet census is expected to be blind at 4 spaces as well [INFERENCE]. The two lane-owned parsers
  carrying the identical anchor (`adoption_check`, `round28_census`) were measured directly.
- **Lane integrity.** No lane file was edited, staged, committed or reverted; no `plans/`, `corpus/`
  or `.ufo` mutation besides this report; no git command beyond read-only `rev-parse`/`status`.
  Observed in-flight from sibling seats and left alone: `D .ufo/waves/round-33/assimilation/append-package.md`,
  `M .ufo/waves/round-33/assimilation/gate-receipts.txt`, `D .ufo/waves/round-33/assimilation/quotes-rows.txt`,
  `M .ufo/waves/round-33/build/R33L0Packet.md`, `M SCORECARD.md`. The guard report's base commit `7895588` is no longer the tip (`77ac8c1`); that
  ordering fact is R33IdGuard's F4, not re-litigated here.
- **Tooling:** no install, no upgrade, no package transaction. Used system `grep`/`cat`/`comm`/`sort`/
  `wc`/`cp`/`tee` and Python 3.14 with the lane's own modules imported read-only.
- **Not in scope:** quote binding/url-map (siblings), the `--attest-opened` path, census W04
  duplicate-URL warnings. One negative result worth recording because it *looks* like a second
  indentation defect and is not: `adoption_check.registry_rows` strips the indent before splitting
  cells (`body = raw.strip()`, `:44-45`), so 1–3-space rows parse with all 11 cells there
  (`reg-1sp`/`reg-3sp` → `rows=1`). The loss at ≥4 spaces is the anchor alone, not the cell slicer.
