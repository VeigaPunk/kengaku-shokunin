# R30FxGateRegression — the gate's pre-existing behaviour is unchanged

Seat: `L1Kengaku30.R30FxGateRegression-3` (leaf, falsify wave). Date 2026-10-25.
Item: attack the C3 surface by showing whether `plans/sources_adopt.py` still behaves identically on
every invocation that existed before the change. Nothing in the lane was edited; every mutant and
every derived fixture lives in `/tmp/r30fx-GateRegression/`.

**Verdict: no behavioural change on any pre-existing invocation.** The landed file is a strict
superset: 14 pre-existing functions/classes are byte-identical, `selftest` and `main` gained lines and
lost none, the ten original selftest cases keep their exact names, order and `PASS` verdicts, and all
five assigned invocations reproduce stdout byte-for-byte and the same exit code on both versions.
The change *is* behaviour-visible — through two new options only, on invocations the old file could
not run at all. Three named deltas in §8; none reaches an invocation the old file accepted.

Tools installed: **none**. `python3` 3.14.8 (system). No package manager touched.

---

## 1. Bytes compared

| object | path / source | sha256 |
|---|---|---|
| pre-change gate | `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 363a4ebf:plans/sources_adopt.py` → `old_sources_adopt.py` | `6fe6e762ab0c61da4ddbf029a2aa1a38cb64732ebd1ccbee4773c5eadcf7ead2` |
| landed gate | `plans/sources_adopt.py` (working tree) → `new_sources_adopt.py` | `e9b6bc044bd5337565d78701c13287eba163c90b13199f4cf8610d27d191a195` |
| pre-append registry copy | `git show 363a4ebf:corpus/SOURCES.md` → `pre-registry.md`, 138 lines, 82 `S###` rows | `e18b32d9b2e3b19053a3d431eb4586713fe057d04477651e6d02be51e8908236` |
| real package (landed six rows) | header + separator + `corpus/SOURCES.md` rows S081–S086 as they now stand → `package-real.md` | `66dfab73658a13f690d1049944c9a306a5f3d174dc5f71152b653aa9298fa76f` |
| the six rows alone | `live-rows.txt` | `84288618427032dbab008588ab9d53c0e989b5e3a93176307a3073f56bef397d` |

`pre-registry.md` is byte-identical to `git show HEAD:corpus/SOURCES.md` (same sha256) and has 82 rows,
so it is a genuine pre-append registry, not the live 88-row file. The landed gate is run from the lane
path as-is; the pre-change gate is `363a4ebf`, the baseline the lesson's own Gate section names.

## 2. What the five assigned invocations are

Shared arguments: `--registry pre-registry.md`, `ENTRY=corpus/knowledge/contamination-transparency-card.md`.

| id | invocation |
|---|---|
| (a) | `--package package-real.md` — the real package **strictly** (no `--scope-to-admit`, no `--admit-ids`) |
| (b) | `--package package-real.md --admit-ids S081,…,S086 --entries $ENTRY --access-date 2026-10-25 --scope-to-admit --out block.txt` — scoped to the six landed ids on the pre-append registry |
| (c) | as (b) but `--admit-ids S081,…,S086,S087` — a **missing requested id** |
| (d) | as (b) but `--package package-dup.md` — S081's row present twice — **duplicate staged id** |
| (e) | as (b) but `--package package-pipe.md` — S081's scope cell carrying a literal `\|` — **malformed escaped-pipe row** |

`block.txt` was written into two separate working directories so the `wrote <path>` line is the same
string on both sides; for (a), (c), (d), (e) no `--out` was given, so stdout is the report only.

## 3. Result table

| id | old exit | new exit | stdout identical? | block file identical? |
|---|---|---|---|---|
| (a) real package, strict | 0 | 0 | **yes** (77 B) | n/a (no `--out`) |
| (b) scoped to six landed ids | 0 | 0 | **yes** (100 B) | **yes** `84288618…` |
| (c) missing requested id `S087` | 5 | 5 | **yes** (93 B) | none written |
| (d) duplicate staged id `S081` | 4 | 4 | **yes** (96 B) | none written |
| (e) escaped-pipe row | 4 | 4 | **yes** (108 B) | none written |

Raw pairs follow. Anything not quoted is exactly as printed by `python3 <script> …`; `EXIT=` is `$?`
captured immediately after the run.

### (a) real package, strict

```
$ python3 old_sources_adopt.py --registry pre-registry.md --package package-real.md
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
EXIT=0

$ python3 new_sources_adopt.py --registry pre-registry.md --package package-real.md
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
EXIT=0
```

Landed rows carry `recheck=180d` and `opened=2026-10-25`, so strict mode has no defect to refuse:
`prose=0`, `defects=0` on both. This is the re-adoption guard: the appended block, fed back in
strictly, is clean.

### (b) scoped to the six landed ids on the pre-append registry

```
$ (cd bo && python3 ../old_sources_adopt.py --registry pre-registry.md --package package-real.md \
    --admit-ids S081,S082,S083,S084,S085,S086 \
    --entries corpus/knowledge/contamination-transparency-card.md \
    --access-date 2026-10-25 --scope-to-admit --out block.txt)
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote block.txt rows=6
EXIT=0

$ (cd bn && python3 ../new_sources_adopt.py --registry pre-registry.md --package package-real.md \
    --admit-ids S081,S082,S083,S084,S085,S086 \
    --entries corpus/knowledge/contamination-transparency-card.md \
    --access-date 2026-10-25 --scope-to-admit --out block.txt)
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote block.txt rows=6
EXIT=0
```

Both `block.txt` files hash `84288618427032dbab008588ab9d53c0e989b5e3a93176307a3073f56bef397d`
and are byte-identical to `live-rows.txt`, i.e. re-running the gate on the pre-append registry
regenerates exactly the rows the lane carries (`diff` clean). `used-by` projection, `recheck`
handling and the append-block writer are therefore unchanged end to end.

### (c) missing requested id

```
$ python3 old_sources_adopt.py --registry pre-registry.md --package package-real.md \
    --admit-ids S081,S082,S083,S084,S085,S086,S087 \
    --entries corpus/knowledge/contamination-transparency-card.md \
    --access-date 2026-10-25 --scope-to-admit
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
  missing: S087
EXIT=5

$ python3 new_sources_adopt.py … same arguments …
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
  missing: S087
EXIT=5
```

`EXIT_REQUEST=5`, and no block is written (`code != EXIT_OK` short-circuits before the block build).

### (d) duplicate staged id

```
$ python3 old_sources_adopt.py --registry pre-registry.md --package package-dup.md \
    --admit-ids S081,S082,S083,S084,S085,S086 \
    --entries corpus/knowledge/contamination-transparency-card.md \
    --access-date 2026-10-25 --scope-to-admit
registry=82 staged=7 collisions=0 malformed=0 duplicates=1 defects=0 prose=0
  duplicates: S081
EXIT=4

$ python3 new_sources_adopt.py … same arguments …
registry=82 staged=7 collisions=0 malformed=0 duplicates=1 defects=0 prose=0
  duplicates: S081
EXIT=4
```

`staged=7` on both: the duplicate is counted, named once, and refused as `EXIT_MALFORMED=4`.

### (e) malformed escaped-pipe row

```
$ python3 old_sources_adopt.py --registry pre-registry.md --package package-pipe.md \
    --admit-ids S081,S082,S083,S084,S085,S086 \
    --entries corpus/knowledge/contamination-transparency-card.md \
    --access-date 2026-10-25 --scope-to-admit
registry=82 staged=5 collisions=0 malformed=1 duplicates=0 defects=0 prose=0
  malformed: S081:escaped-pipe
EXIT=4

$ python3 new_sources_adopt.py … same arguments …
registry=82 staged=5 collisions=0 malformed=1 duplicates=0 defects=0 prose=0
  malformed: S081:escaped-pipe
EXIT=4
```

The mutant was built by inserting ` \| ` into S081's scope cell only; `staged=5` on both because a
row that fails `split_cells` becomes a malformed entry rather than a staged row — the pre-existing
counting rule, preserved.

## 4. The ten original selftest cases

`python3 <script> --selftest` on both, exit 0 both (and `SELFTEST cases=14 failed=0` on the new one).

```
$ grep '^CASE' old_selftest.out > cases-old.txt
$ grep '^CASE' new_selftest.out | head -10 > cases-new-first10.txt
$ diff cases-old.txt cases-new-first10.txt
(no output)
```

| # | case name (both files, same order) | old | new |
|---|---|---|---|
| 1 | `collision-zero-indent` | PASS | PASS |
| 2 | `collision-one-space` | PASS | PASS |
| 3 | `collision-three-space` | PASS | PASS |
| 4 | `four-space-not-a-row` | PASS | PASS |
| 5 | `escaped-pipe-refused` | PASS | PASS |
| 6 | `prose-recheck-normalized` | PASS | PASS |
| 7 | `usedby-projected` | PASS | PASS |
| 8 | `duplicate-staged-id` | PASS | PASS |
| 9 | `clean-package-passes` | PASS | PASS |
| 10 | `missing-requested-id` | PASS | PASS |

Trailing summary lines, whole file:

```
old: SELFTEST cases=10 failed=0      (exit 0)
new: SELFTEST cases=14 failed=0      (exit 0)
new-only cases: quote-overlong-refused, quote-absent-refused, quote-located-accepted, quote-boundary-25-accepted — all PASS
```

The four new cases are appended after case 10; no original case is renamed, reordered, retitled or
re-scoped. `corpus/evidence/round30/gate-selftest-after.txt` (`SELFTEST cases=14 failed=0`, `exit=0`)
and `.ufo/waves/round-30/claims/gate-before.txt` (`SELFTEST cases=10 failed=0`, `selftest_exit=0`)
both reproduce on my own runs of the two files.

## 5. Structural proof that the change is additive only

Whole-file `diff` has exactly 3 removed lines, all prose in the module docstring (capability 4's
sentence and the two-line `Scope:` paragraph, rewritten to mention quote validation). Everything else
is `+`.

Function-level, by comparing each definition's source segment (`ast` lineno/end_lineno) between the
two files:

| class | members | result |
|---|---|---|
| byte-identical | `Row`, `Row.__init__`, `Row.cell`, `collect`, `check`, `collisions`, `duplicate_ids`, `ids`, `parse_rows`, `print_report`, `row_defects`, `split_cells`, `build_block`, `selftest.case` (14) | identical |
| absent from new | — | none |
| new only | `words`, `normalize_text`, `quoted_spans`, `load_artifact`, `locates`, `quote_check`, `print_quote_report` | additions |
| present, extended | `selftest` (143 → 265 lines, **0 removed**), `main` (66 → 82 lines, **0 removed**) | additive |

Module constants: `ROW_RE`, `ISO_DATE_RE`, `CADENCE_RE`, `SYMBOLIC_CADENCE`, `STATUSES`, `COLUMNS`,
`EXIT_OK`, `EXIT_COLLISION`, `EXIT_MALFORMED`, `EXIT_REQUEST`, `HEADER`, `GOOD_ROW`, `PROSE_ROW` are
all unchanged; the only new constants are `QUOTE_WORDS=25`, `ANCHOR_COLUMN=5`, `QUOTE_SPAN_RE`,
`EXIT_QUOTE_UNREADABLE=2`, `EXIT_QUOTE_TOO_LONG=6`, `EXIT_QUOTE_ABSENT=7`. No pre-existing exit
constant changed value.

The added `main` lines are two `parser.add_argument` blocks and one branch placed immediately after
`if args.selftest: return selftest()`:

```python
    if args.quote_file or args.artifact:
        if not (args.quote_file and args.artifact):
            parser.error("--quote-file and --artifact must be given together")
        code, report = quote_check(args.quote_file, args.artifact)
        print_quote_report(report)
        return code
```

`args.quote_file` and `args.artifact` are `None` on every invocation the old file could parse, so this
branch is unreachable for them.

## 6. The retained ten cases still bind (they are not vacuous in the new file)

Three mutants of the **new** file, each in `/tmp/r30fx-GateRegression/mut/`, run through its own
`--selftest`:

| mutant | edit | result |
|---|---|---|
| `M1-no-escaped-pipe-check` | `if "\|" in stripped:` → `if False:` | `CASE escaped-pipe-refused FAIL`, `cases=14 failed=1`, exit 1 |
| `M2-no-duplicate-detect` | `duplicate_ids` returns `[]` | `CASE duplicate-staged-id FAIL`, `cases=14 failed=1`, exit 1 |
| `M3-column-zero-anchor` | `ROW_RE` leading-space group `{0,3}` → `{0,0}` | `CASE collision-one-space FAIL`, `CASE collision-three-space FAIL`, `cases=14 failed=2`, exit 1 |

So the ten carried-over cases still discriminate: the new code did not neuter them, it only appended
to the file that contains them.

## 7. Supplementary invocations (not in the five, run for pre-existing-behaviour coverage)

| # | invocation | old exit | new exit | stdout |
|---|---|---|---|---|
| (f) | `--registry corpus/SOURCES.md` (live, 88 rows) + landed rows, scoped | 3 | 3 | identical (121 B): `collisions=6` / `collisions: S081 S082 S083 S084 S085 S086` — the post-append collision guard still fires |
| (g) | `--quote-file qfile.md --artifact artifact.txt` | 2 (argparse `unrecognized arguments`) | 0 (`QUOTE rows=1 spans=1 located=1 …`) | **differs by design** — see §8.1 |
| (h) | strict on the escaped-pipe package (no `--scope-to-admit`) | 4 | 4 | identical (108 B): `malformed: S081:escaped-pipe` |
| (i) | strict on a package whose S081 `recheck` is prose | 4 | 4 | identical (106 B): `defect S081: recheck-prose` (`prose=1`) |
| (j) | `--registry … --package … --quote-file … --artifact …` | 2 | 0 | **differs** — see §8.2 |
| (k) | `--quote-file` without `--artifact` | 2 (`unrecognized arguments`) | 2 (`--quote-file and --artifact must be given together`) | same code, different message |
| (l) | staged distribution package `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`, scoped + `--attest-opened` | 0 | 0 | identical (740 B): `staged=173`, `attested: …`, six `normalized recheck` lines, `wrote` line |
| (m) | staged distribution package, scoped, no attest | 5 | 5 | identical (117 B) — reproduces `R30BuildAppend.md` §4a byte-for-byte: `registry=82 staged=173 … prose=6` + `missing: S081:not-opened-this-round` |
| (n) | staged distribution package, **strict** | 3 | 3 | identical (5019 B report) |
| (o) | bad `--access-date 25-10-2026` | 2 | 2 | error text identical; usage listing gains the two options |
| (p) | bad `--recheck weekly` | 2 | 2 | same |
| (q) | no arguments | 2 | 2 | same (`--registry and --package are required unless --selftest`) |
| (r) | `--admit-ids S081` without `--entries` | 2 | 2 | same (`--entries is required …`) |

For (o)–(r) the two scripts were copied to the *same* filename `sources_adopt.py` in separate
directories before running, so the only textual difference is the usage listing gaining
`[--quote-file QUOTE_FILE] [--artifact ARTIFACT]`:

```
<                         [--recheck RECHECK] [--out OUT] [--attest-opened]
<                         [--scope-to-admit]
---
>                         [--recheck RECHECK] [--out OUT]
>                         [--quote-file QUOTE_FILE] [--artifact ARTIFACT]
>                         [--attest-opened] [--scope-to-admit]
```

Error sentences (`--access-date must be an ISO date (YYYY-MM-DD)`, `--recheck must be an ISO date,
<N>d, or a known symbolic cadence`, `--registry and --package are required unless --selftest`,
`--entries is required when --admit-ids is given (used-by has no fallback)`) are unchanged.

The new exit codes are reachable from the CLI, not just from the selftest:

```
$ python3 new_sources_adopt.py --quote-file q-over.md   --artifact art26.txt
QUOTE rows=1 spans=1 located=0 found=1 overlong=1 absent=0 malformed=0 cap=25 artifacts=art26.txt
  REFUSED S081 overlong words=26 cap=25 at art26.txt quote="w1 … w26"
EXIT=6

$ python3 new_sources_adopt.py --quote-file q-absent.md --artifact art26.txt
QUOTE rows=1 spans=1 located=0 found=0 overlong=0 absent=1 malformed=0 cap=25 artifacts=art26.txt
  REFUSED S082 absent words=7 quote="this sentence is nowhere in the artifact"
EXIT=7

$ python3 new_sources_adopt.py --quote-file q-over.md --artifact /nonexistent/path
QUOTE cap=25 problem=--artifact names no file or directory: /nonexistent/path
EXIT=2
```

C3's frozen predicate is therefore satisfied on the part this seat measured: `cases=14 failed=0`
exit 0, the two refusals carry distinct non-zero exits (6 and 7) and are shown failure-capable above,
and the pre-change bytes reject the same invocation with argparse exit 2 ((g), (j), (k)).
I do **not** score C3 — that is the wave's call; I only report that its `--selftest` and control
clauses reproduce on my own runs.

## 8. Named behavioural deltas (all additive; none reachable by an invocation the old file accepted)

1. **New capability surface.** `--quote-file`/`--artifact` select a quote-validation mode with exits
   6/7 (structural → 4, unreadable artifact → 2). On the pre-change bytes the same arguments are
   `argparse` failures at exit 2, which is exactly the control C3 records
   (`.ufo/waves/round-30/claims/gate-before.txt`). This is the intended change; it is not a change to
   pre-existing behaviour.
2. **Branch order.** The quote branch sits *before* the `--registry/--package` guard, so supplying
   registry/package arguments **together with** quote arguments no longer errors: invocation (j) was
   exit 2 and is now exit 0 running only the quote check, silently ignoring `--registry` and
   `--package`. No old invocation can reach this (it needs a new argument), but a caller that adds a
   quote check to an existing adoption command will lose the adoption check without any diagnostic.
   Cheap hardening, if the lane wants it: `parser.error` when quote arguments arrive with
   `--registry`/`--package`, or run the quote check only when neither is given. I have not edited the
   file — this report's only write in the lane is itself.
3. **Exit-code 2 is now overloaded.** `EXIT_QUOTE_UNREADABLE = 2` shares its value with `argparse`'s
   usage-error exit. A caller that distinguishes "I passed bad arguments" from "the artifact could
   not be read" by exit code alone cannot do so in quote mode. The docstring states the choice
   deliberately ("same class as argparse usage errors: caller/env, not bytes"), so this is a
   documented design decision rather than a defect — recorded so the behaviour is not mistaken for
   an argparse failure. It changes no pre-existing path: exit 2 was already reachable there.

There is no fourth delta. The whole-file diff contains no other edit, and every invocation in §3 and
§7 either matches byte-for-byte or differs only in the two additions named above.

## 9. Adjacent freshness finding (outside this item's verdict)

The six rows the lane carries are **not** the bytes `R30BuildAppend.md` measured. That report proves
`BLOCK_INSERTED_BYTE_IDENTICAL` against `/tmp/r30-BuildAppend/block.txt`
(`sha256 2ec3a83b06c7ef2a59ea7dac55e6b2c6187ff3312b7b965e539ca74f177d1529`); the live rows hash
`84288618…` and differ cell by cell:

| row | cells that differ (build block → landed) |
|---|---|
| S081 | scope 359→292 B, anchor 278→426 B, teaches 297→197 B |
| S082 | source 119→122, scope 238→180, anchor 281→349, teaches 272→183 |
| S083 | scope 222→211, anchor 372→289, teaches 241→159 |
| S084 | scope 199→185, anchor 115→194, teaches 257→206 |
| S085 | source 156→163, scope 307→213, anchor 145→230, teaches 278→185 |
| S086 | source 201→195, scope 239→109, anchor 103→284, teaches 240→160 |

So either the rows were re-grounded after that receipt was taken (the lesson's own
"staged text's claims this round refused to carry" paragraph describes exactly such re-grounding of
S081/S082/S085), or the insertion was not block-identical. **Either way the build report's
byte-identity receipt no longer describes the registry bytes on disk**, and a reader who takes it as
the landing receipt is reading a claim about different bytes. This does not affect §3: I re-derived
the package from the live rows and the gate regenerates them byte-identically (`block.txt ==
live-rows.txt`), so the gate is self-consistent with what landed. Flagged for the seat that owns the
admission narrative; not scored here.

## 10. Scope statement

- Lane writes by this seat: this report only. All fixtures, mutants, extracted scripts and outputs
  are under `/tmp/r30fx-GateRegression/`.
- No verdict line is carried: this item is neither a source re-read nor the complete-set review, and
  no Gate-admit row in `corpus/lessons/round-30.md` names this report
  (the cited falsify reports are `R30FxEntryCompleteSet`, `R30FxEntryQ1Q3`, `R30FxEntryQ4Q6`,
  `R30FxQuotes`, `R30FxSrcS081`…`R30FxSrcS086`). Emitting a pass verdict here would fabricate a
  second-seat return on `corpus/knowledge/contamination-transparency-card.md` that this seat did not
  perform, so it is deliberately omitted.
- No build, lint or formatter gate was run: the editing wave's gate is the parent's to execute. The
  only executions recorded are the `--selftest` and CLI invocations above.
