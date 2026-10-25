# R31GateRegress — the C3 gate's pre-existing behaviour, measured before and after an additive `--url-map`

Seat: `L1Kengaku31.R31GateRegress` (leaf, round 31). Date 2026-10-25. Access date 2026-10-25.
Item: prove that the `--url-map` addition does not move anything the gate already did — the 14
pre-existing `--selftest` cases and the five pre-existing invocation shapes round 30's regression
receipt names. Nothing under `/home/vgpnk/Projects/shokunin/kengaku-shokunin` was edited by this
seat; the only lane write is this report. Every script, fixture and output lives in
`/tmp/r31-GateRegress/` (1.6 MB, no clone, no network).

**VERDICT: PASS — with an additive `--url-map` the gate's pre-existing behaviour is unchanged: the five pre-existing invocation shapes reproduce stdout byte-for-byte and the same exit codes (0,0,5,4,4) plus a byte-identical append block, the four pre-existing quote-mode invocations reproduce byte-for-byte with the same exits (6,0,0,2), and the 14 original `--selftest` case lines are byte-identical in name, order and PASS verdict. The only deltas the addition introduces are (i) three appended selftest cases (14 → 17, `failed=0`, exit 0), (ii) `[--url-map URL_MAP]` appearing in argparse's usage listing, and (iii) four source lines mechanically re-wrapped/extended with no logic removed. Named separately in §7: the lane's *working-tree* candidate (sha256 `4e49a3e2…`) does **not** hold that line — it rewrites the QUOTE summary line on pre-existing quote invocations and writes a usage block to stderr on every `--selftest`.**

---

## 1. Bytes compared

| object | how obtained | sha256 |
|---|---|---|
| **unmodified copy** (the C3 baseline) | `git -C <lane> show HEAD:plans/sources_adopt.py` → `head_sources_adopt.py`, 815 lines | `47e60021966318c9f36d4cab8e1464a8cd333db114eca3c1689d206cdfef7922` |
| **additive copy** (this seat's change) | `head_sources_adopt.py` + `--url-map` only → `new_sources_adopt.py`, 1006 lines | `757a1d6e9c29c3c9b3e772b9dd0cc8cc574912ddb5f7b3489e3db4c8ab5f6dad` |
| pre-append registry fixture | `git show 363a4ebf:corpus/SOURCES.md`, 138 lines, 82 rows — the same commit and the same hash round 30 used | `e18b32d9b2e3b19053a3d431eb4586713fe057d04477651e6d02be51e8908236` |
| `package-real.md` | the 11-column header + the six **live** rows S081–S086 copied verbatim out of `corpus/SOURCES.md` | `a5e2e54dc72f9113afbe339b609054cc24428fb937c07c5ced22d356518a0424` |
| `package-dup.md` | `package-real.md` with S081's row repeated | `cdb427efd0ac3b74404395210307afc35e3391d0615a4db2b79d530c493309ed` |
| `package-pipe.md` | `package-real.md` with ` \| appended` inserted into S081's scope cell | `eb09e8f51c7c4f0d2ed6e34535cb7d0b7941113ae96b77e2b9ae5209e30cee1f` |
| lane working tree at 15:0x UTC (landed candidate, mid-wave) | `cp plans/sources_adopt.py` → `wt_sources_adopt.py` | `39ba62b22915bdcf6943dc2a860bd338a77cbd1d9b92064ab75edd54cda9bc71` |
| lane working tree, later snapshot | → `wt2_sources_adopt.py` | `4e49a3e23253beb2c46dfa6dc4da6e1792eb472cd283e81d6089f21fe9f5573f` |

The baseline is `HEAD` (`0883e72`), not the pre-quote bytes round 30 used: `HEAD` already carries the
quote capability and the 14 cases, so `HEAD` is the set C3 must not disturb. `git status` shows
`M plans/sources_adopt.py` — the lane file is the sibling's in-flight edit; this seat read it, never
wrote it.

## 2. (a) `--selftest` on the unmodified copy

```
$ python3 head_sources_adopt.py --selftest
CASE collision-zero-indent PASS
CASE collision-one-space PASS
CASE collision-three-space PASS
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id PASS
CASE clean-package-passes PASS
CASE missing-requested-id PASS
CASE quote-overlong-refused PASS
CASE quote-absent-refused PASS
CASE quote-located-accepted PASS
CASE quote-boundary-25-accepted PASS
SELFTEST cases=14 failed=0
EXIT=0
```

478 bytes, stderr 0 bytes, 14 `CASE` lines, all `PASS`.

The two summary lines are exactly the ones the lane's own round-30 receipt carries:
`corpus/evidence/round30/gate-selftest-after.txt` ends `SELFTEST cases=14 failed=0` / `exit=0`, and
`diff` of my non-`CASE` stream against that file's two lines is clean (that file records no `CASE`
lines, so only the summary is comparable — and it matches).

## 3. (c) The five pre-existing invocation shapes, unmodified copy

Shared: `--registry pre-registry.md` (82 rows) and `ENTRY=corpus/knowledge/contamination-transparency-card.md`.
Shapes (a)–(e) are the five `R30FxGateRegression.md` §2 names. Each run's stdout is quoted exactly;
`EXIT=` is `$?` taken immediately after.

### (a) real package, strict (no `--scope-to-admit`, no `--admit-ids`)

```
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
EXIT=0        (77 B, sha256 8ed940b84027adc261e73b34cd5d92210d3e0b1c5c48f6f477a17af03337ae53)
```

### (b) scoped to the six landed ids, `--out block.txt`

```
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote block.txt rows=6
EXIT=0        (100 B, sha256 d08ba2f2a1fc33a3e733436234b30eea81569aa5a61392a7d3d067ede784566b)
block.txt 6424 B, sha256 9790949e27078fa60f279dcd7ffa5bc9ef2ec71b4e8082500cb24ae501e9c528
```

### (c) a missing requested id (`…,S087`)

```
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
  missing: S087
EXIT=5        (93 B, sha256 f200bcc88ccc039942992bf45f8834fd6c84c444d0ce889b1395a42cbc6bf95e)
```

### (d) a duplicate staged id (`S081` twice)

```
registry=82 staged=7 collisions=0 malformed=0 duplicates=1 defects=0 prose=0
  duplicates: S081
EXIT=4        (96 B, sha256 2cf4acb03f7c1aaa65a23c22582f56605aecb28300a9c49f7fe9249032812822)
```

### (e) a malformed escaped-pipe row

```
registry=82 staged=5 collisions=0 malformed=1 duplicates=0 defects=0 prose=0
  malformed: S081:escaped-pipe
EXIT=4        (108 B, sha256 d30c619c51f88183bbfc08bfa1a058feddd30be4485c7fc32a3737758bff8ba3)
```

Exits and every report line match `R30FxGateRegression.md` §3 exactly. The block hash does **not**
match round 30's `84288618…`, and the reason is not the gate: I compared `block.txt` cell by cell
against the live rows and **only cell 10 (`used-by`) differs** on all six rows — the live rows have
since gained citations, while `build_block` deliberately projects `used-by` down to exactly the
admitted entry. The other ten cells are identical on every row, so the package is the real live row
set and the gate is deterministic on it.

## 4. (d) The additive change, and the same two runs on it

Only an `--url-map` option was added to `head_sources_adopt.py`; every existing code path is
untouched (§6 proves it structurally). The addition is:

- `import json`; `EXIT_URL_MISMATCH = 8`, `EXIT_URL_UNMAPPED = 9`; `SOURCE_COLUMN = 1`, `URL_RE`;
- new functions `cited_urls`, `normalize_url`, `load_url_map`, `bind_failure`;
- `quote_check(..., url_map: dict[str, str] | None = None)` — when the map is supplied, a located
  quote is also bound to the URL the row's `source` cell cites (`url-mismatch` → 8, `unmapped` → 9,
  `cites-no-url` → 8); without the map the function is byte-presence only, exactly as before;
- `print_quote_report` appends ` mismatch=… unmapped=…` **only when a map was supplied**, so the
  pre-existing summary line is unchanged without one;
- `main`: one `parser.add_argument("--url-map", type=Path, …)`, a `load_url_map` call in the quote
  branch, and a guard that refuses `--url-map` with no quote inputs (a flag the run would otherwise
  silently ignore);
- three selftest cases appended after case 14 (`quote-url-bound-accepted`,
  `quote-url-mismatch-refused`, `quote-url-unmapped-refused`).

### (a′) `--selftest` on the additive copy

```
$ python3 new_sources_adopt.py --selftest
CASE collision-zero-indent PASS
… (cases 2-14 byte-identical to §2) …
CASE quote-boundary-25-accepted PASS
CASE quote-url-bound-accepted PASS
CASE quote-url-mismatch-refused PASS
CASE quote-url-unmapped-refused PASS
SELFTEST cases=17 failed=0
EXIT=0
```

587 bytes, stderr **0 bytes**, 17 `CASE` lines, all `PASS`.

### (c′) The five shapes on the additive copy

| id | unmodified exit | additive exit | stdout | bytes | block |
|---|---|---|---|---|---|
| (a) strict | 0 | 0 | **byte-identical** (`cmp` clean, sha `8ed940b8…`) | 77 | n/a |
| (b) scoped, `--out` | 0 | 0 | **byte-identical** (sha `d08ba2f2…`) | 100 | **byte-identical** `9790949e…` |
| (c) missing `S087` | 5 | 5 | **byte-identical** (sha `f200bcc8…`) | 93 | none written on both |
| (d) duplicate `S081` | 4 | 4 | **byte-identical** (sha `2cf4acb0…`) | 96 | none written on both |
| (e) escaped pipe | 4 | 4 | **byte-identical** (sha `d30c619c…`) | 108 | none written on both |

Side by side, verbatim (left = unmodified, right = additive; both runs used separate working
directories so the `wrote block.txt` line is the same string on both sides):

```
$ python3 head_sources_adopt.py --registry pre-registry.md --package package-real.md
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
EXIT=0
$ python3 new_sources_adopt.py  --registry pre-registry.md --package package-real.md
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
EXIT=0

$ python3 head_sources_adopt.py --registry pre-registry.md --package package-real.md \
    --admit-ids S081,S082,S083,S084,S085,S086 \
    --entries corpus/knowledge/contamination-transparency-card.md \
    --access-date 2026-10-25 --scope-to-admit --out block.txt
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote block.txt rows=6
EXIT=0
$ python3 new_sources_adopt.py  … same arguments …
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote block.txt rows=6
EXIT=0

$ … --admit-ids …,S087 --scope-to-admit
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
  missing: S087
EXIT=5        (identical on both)

$ … --package package-dup.md --scope-to-admit
registry=82 staged=7 collisions=0 malformed=0 duplicates=1 defects=0 prose=0
  duplicates: S081
EXIT=4        (identical on both)

$ … --package package-pipe.md --scope-to-admit
registry=82 staged=5 collisions=0 malformed=1 duplicates=0 defects=0 prose=0
  malformed: S081:escaped-pipe
EXIT=4        (identical on both)
```

## 5. Pre-existing quote mode and the usage-error paths, both sides

Quote mode existed before this change (round 30 added it), so it is a pre-existing invocation and is
measured the same way.

| id | invocation | unmodified | additive | stdout |
|---|---|---|---|---|
| (g) | `--quote-file q-over.md --artifact art26.txt` (26-word span) | 6 | 6 | **byte-identical** (254 B, `1e027cce…`) |
| (g2) | `--quote-file q-edge.md --artifact artedge.txt` (exactly 25 words) | 0 | 0 | **byte-identical** (233 B, `cf26a074…`) |
| (g3) | `--quote-file q-absent.md --artifact artabs.txt` | 0 | 0 | **byte-identical** (199 B, `3161fd21…`) |
| (g4) | `--quote-file q-over.md --artifact /nonexistent/path` | 2 | 2 | **byte-identical** (78 B, `685fe88d…`) |
| (j) | quote args **plus** `--registry/--package` | 2 | 2 | identical except usage listing (§7.2) |
| (k) | `--quote-file` without `--artifact` | 2 | 2 | identical except usage listing |
| (o) | `--access-date 25-10-2026` | 2 | 2 | identical except usage listing |
| (p) | `--recheck weekly` | 2 | 2 | identical except usage listing |
| (r) | `--admit-ids S081` without `--entries` | 2 | 2 | identical except usage listing |
| (q) | no arguments | 2 | 2 | identical except usage listing |

For (j)–(q) both scripts were copied to the **same** basename `sources_adopt.py` in separate
directories first, so `prog` is the same string and the only textual difference is the usage listing:

```
<                         [--attest-opened] [--scope-to-admit]
---
>                         [--url-map URL_MAP] [--attest-opened]
>                         [--scope-to-admit]
```

Every error sentence is unchanged (`--quote-file/--artifact cannot be combined with --registry/--package`,
`--quote-file and --artifact must be given together`, `--access-date must be an ISO date (YYYY-MM-DD)`,
`--recheck must be an ISO date, <N>d, or a known symbolic cadence`, `--entries is required when
--admit-ids is given (used-by has no fallback)`, `--registry and --package are required unless
--selftest`).

New-only shapes, additive copy only (the unmodified copy rejects all of them as
`unrecognized arguments: --url-map …`, exit 2):

| shape | additive exit | first line |
|---|---|---|
| map value == the row's cited URL | 0 | `QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 mismatch=0 unmapped=0 malformed=0 cap=25 artifacts=artedge.txt` |
| map value differs by case + trailing `/#frag` only | 0 | same (normalisation is formatting, not a document) |
| map value is another document | **8** | `… located=0 found=1 … mismatch=1 unmapped=0 …` / `  REFUSED S018 url-mismatch …` |
| artifact absent from the map | **9** | `… mismatch=0 unmapped=1 …` / `  REFUSED S018 unmapped …` |
| `--url-map` names no file | 2 | `QUOTE problem=--url-map is unreadable: [Errno 2] No such file or directory: '/nonexistent.json'` |
| `--url-map` nested (`{"a": {"b": "c"}}`) | 2 | `QUOTE problem=--url-map must map strings to strings` |
| `--url-map` with `--registry/--package`, no quote args | 2 | `sources_adopt.py: error: --url-map needs --quote-file and --artifact` |

## 6. Structural proof that the change is additive only

`diff head_sources_adopt.py new_sources_adopt.py` removes exactly **4** lines, and each is a
mechanical extension of a line the addition has to touch — no statement, no branch and no exit
constant is removed anywhere:

| removed line | why |
|---|---|
| `     as a byte substring of the named artifact, with its own exit codes.` | docstring sentence now ends `;` and gains capability 6 below it |
| `def quote_check(quote_file: Path, artifact: Path, cap: int = QUOTE_WORDS) -> …:` | signature spread over four lines to take `url_map=` |
| `        "absent={absent} malformed={mal} cap={cap} artifacts={arts}".format(` | format string gains the conditional `{extra}` slot |
| `        code, report = quote_check(args.quote_file, args.artifact)` | call gains `url_map=url_map` |

Function-level comparison by AST source segment (name → sha256 of its own segment):

| class | members | result |
|---|---|---|
| byte-identical (21) | `Row`, `Row.__init__`, `Row.cell`, `collect`, `check`, `collisions`, `duplicate_ids`, `ids`, `parse_rows`, `print_report`, `row_defects`, `split_cells`, `build_block`, `load_artifact`, `locates`, `normalize_text`, `quoted_spans`, `words`, `selftest.case`, `selftest.write`, `selftest.quote_row` | identical |
| absent from additive | — | none |
| new only (4) | `cited_urls`, `normalize_url`, `load_url_map`, `bind_failure` | additions |
| present, extended | `selftest` (265 → 322 lines), `quote_check` (84 → 117), `print_quote_report` (20 → 27), `main` (86 → 103) | additions only; the 4 removed lines above are the whole subtraction |

Module constants: every pre-existing constant keeps its exact value (`ROW_RE`, `ISO_DATE_RE`,
`CADENCE_RE`, `SYMBOLIC_CADENCE`, `STATUSES`, `COLUMNS`, `EXIT_OK`, `EXIT_QUOTE_UNREADABLE`,
`EXIT_COLLISION`, `EXIT_MALFORMED`, `EXIT_REQUEST`, `EXIT_QUOTE_TOO_LONG`, `EXIT_QUOTE_ABSENT`,
`HEADER`, `GOOD_ROW`, `PROSE_ROW`); the only new ones are `EXIT_URL_MISMATCH = 8`,
`EXIT_URL_UNMAPPED = 9`, `SOURCE_COLUMN = 1`, `URL_RE`. No pre-existing exit code changed value, and
8/9 were unclaimed at `HEAD`.

Because `diff` shows all 4 removed lines outside the `selftest` body, the `selftest` body itself is
pure addition — which is why the first 14 `CASE` lines reproduce byte-for-byte (§4, `diff` of the two
`CASE` streams is clean, and `diff` of the non-`CASE` lines is exactly the one summary line).

## 7. Every difference named

1. **`--selftest` summary line.** `SELFTEST cases=14 failed=0` → `SELFTEST cases=17 failed=0`
   (exit 0 both; stderr 0 bytes both). This is the intended additive growth: three new cases
   appended after case 14, nothing renamed, reordered or re-scoped.
2. **argparse usage listing.** Gains `[--url-map URL_MAP]`, which re-wraps the listing from 7 to 8
   lines. It appears only in usage-error output (exit 2 paths (j)–(q)); it cannot appear on any
   invocation that succeeds, and every error sentence and exit code is unchanged.
3. **Source lines.** The 4 mechanical re-writes in §6. Nothing else.

No other difference exists: all five pre-existing shapes and all four pre-existing quote-mode shapes
are `cmp`-clean, and the append block is byte-identical.

## 8. What the lane's working-tree candidate does differently (measured, not assumed)

This seat also ran the same suite against the sibling's in-flight `plans/sources_adopt.py`, read-only,
to see whether the *landed* shape holds the same line. It does not — two differences reach invocations
that existed before the change:

| snapshot | sha256 | five shapes | pre-existing quote mode | `--selftest` stderr |
|---|---|---|---|---|
| earlier (mid-edit) | `39ba62b2…` | identical, exits 0/0/5/4/4 | **broken**: all four exit 2 with `error: --registry and --package are required unless --selftest` (the quote branch's body had been made unreachable — `url_map = None … return code` sat after an unconditional `parser.error` inside `elif args.url_map:`) | 530 B usage block |
| later | `4e49a3e2…` | identical, exits 0/0/5/4/4, block `9790949e…` | exits restored (6/0/0/2) but **stdout differs**: the QUOTE summary line gains two fields on *every* quote run, e.g. `… overlong=1 absent=0 mismatch=0 unmapped=0 malformed=0 cap=25 urlmap=none artifacts=art26.txt`, and the problem line gains `urlmap=none` | 538 B usage block, exit 0 |

Concretely, on `4e49a3e2…`:

```
unmodified : QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=artedge.txt
candidate  : QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 mismatch=0 unmapped=0 malformed=0 cap=25 urlmap=none artifacts=artedge.txt
unmodified : QUOTE cap=25 problem=--artifact names no file or directory: /nonexistent/path
candidate  : QUOTE cap=25 urlmap=none problem=--artifact names no file or directory: /nonexistent/path
```

Both are avoidable without touching any existing code path: gate the new fields on "a map was
supplied" (as this seat's copy does), and exercise the `main()` guard in the selftest by asserting on
`SystemExit.code` through `contextlib.redirect_stderr` so `--selftest` does not print a usage block to
stderr. Neither is a C3 regression in the *five* shapes the round-30 receipt names — those are
byte-identical on `4e49a3e2…` — but both change pre-existing invocations (quote mode, and
`--selftest` under `2>&1`, which is how round 30's own `gate-before.txt` captures were taken). The
sibling may still be editing; the shas above are what this seat read at 15:1x UTC, and the lane file
changed twice during the measurement, so re-measure at integration rather than trusting either sha.

## 9. Scope statement

- Lane writes by this seat: **this report only**. `git status` on the lane shows no file touched by
  me; the one `M` on `plans/sources_adopt.py` is the sibling's.
- Everything else is under `/tmp/r31-GateRegress/` (~1.6 MB): two scripts, six fixtures, per-run
  stdout/exit captures (`out-*`, `qout-*`, `qexit-*`, `sameout-*`, `sameexit-*`), the two selftest
  captures and their stderr, and the three working-tree snapshots.
- No clone, no network fetch, no read of `/home/vgpnk/Projects/shokuknow`, no pacman transaction.
  Tools installed: **none** — `python3` 3.14.8 (system) only.
- No build/lint/formatter gate was run; the editing wave's gate is the parent's. The only executions
  recorded are the `--selftest` and CLI invocations quoted above.
