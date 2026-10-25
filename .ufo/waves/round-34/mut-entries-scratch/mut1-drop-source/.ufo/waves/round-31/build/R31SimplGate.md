# R31SimplGate — dead weight the C3 URL binding must not inherit

Seat `R31SimplGate` (simplifier). Claim reviewed: **C3** of `plans/round-31-claims.md`
(operability). Date 2026-10-25. Read-only: no lane byte was edited by this seat.

**Artifacts, keyed by hash** (the lane file moved six times while this seat ran:
815 → 873 → 939 → 996 → 997 → 1040 lines):

| label | sha256 | lines | prod / selftest | note |
|---|---|---|---|---|
| `HEAD` = baseline `0883e72` | `47e60021…ef7922` | 815 | 448 / 367 | byte-identical to the file round-30's simplifier reviewed; its delete list was **not** applied |
| `71a90ec0` | `71a90ec0…b60d5` | 997 | 560 / 437 | C3 landed, `cases=17 failed=0` |
| `39ba62b2` = live when this report was written | `39ba62b2…9bc71` | 1040 | 574 / 466 | adds `locating_artifacts` (any-containing-artifact rule), the decoy case and the `--url-map` pairing guard |

All line numbers below are `39ba62b2` (1040 lines) unless a label says otherwise.
Selftest on `39ba62b2`: `SELFTEST cases=17 failed=0`, exit 0 (re-run by me,
`/tmp/r31-simplgate/live2_st.txt`). Branch coverage of the counting command
(`coverage run --branch … --selftest`, coverage 7.17.0): 484 statements, 84 uncovered,
154 branches, 60 partial.

---

## 1. (a) Duplicated logic between `check()` and `quote_check()`

| element | `check()` | `quote_check()` | verdict |
|---|---|---|---|
| row parsing | `collect()` → `parse_rows` (`181`, called at `198`) | `parse_rows(quote_file.read_text())` (`478`) | **already one path.** `collect()` cannot serve: it reads two files and returns the registry rows too. No change |
| `bad` → `<id>:<reason>` projection | `201` `malformed = [f"{row_id}:{reason}" for _, row_id, reason in bad]` | `477` — **the identical expression, character for character** (`grep -c` = 2) | **the only real duplicate.** One 2-line helper (`malformed_entries(bad)`) removes it; both sites become `malformed_entries(bad)` |
| defect collection | `row_defects()` into `defects` (`199`) | its own buckets `overlong/absent/mismatch/unmapped/malformed` | **keep separate.** `row_defects` answers "is this registry row admissible"; `quote_check` answers "does this span hold". One generic bucket engine over both would be a second convention, not a simplification |
| exit ladder | `malformed/dupes/defects → COLLISION-or-MALFORMED`, then `clash`, then `REQUEST` (`228-235`) | straight chain `4 → 6 → 7 → 8 → 9` (`536-545`) | **keep separate.** Different precedence (collision outranks malformed in `check`; nothing outranks malformed in `quote_check`) and different code sets. A shared ladder would have to be parameterised by precedence, which is exactly the abstraction this file avoids |
| report shape | `report: dict` then `.update(...)` | same idiom | keep; it is the file's existing convention, not a new one |

Two smaller duplications the C3 change **created**:

- `locating_artifacts` (`387-395`) and `locates` (`398-407`) contain the same predicate:
  `[name for name, text in loaded if needle in text]` (`395`) vs
  `next((name for name, text in loaded if needle in text), "")` (`407`). Two readings of one
  rule. `locates` becomes `return next(iter(locating_artifacts(quote, loaded)), "")` — one
  predicate, two views, −1 line, both cases still green (measured, §4).
- the **inherited** triple pass over `row_defects` in `check()`: `199` (dict), `206`
  (`prose_recheck_total`), `223` (`prose_recheck`) each re-derive every row's defects; two
  of them are recomputed from scratch. `print_report` then reads *either* key
  (`251` `report.get("prose_recheck", report.get("prose_recheck_total", 0))`). C3 does not
  touch this region and must not copy the pattern — `quote_check` correctly does a single
  pass, so nothing to do here beyond "don't".

**Answer:** the binding can reuse exactly one path — the `bad`-projection — and needs no
shared path with `check()` at all: it lives inside `quote_check`'s located branch and
`check()` has neither an artifact nor a quote.

## 2. (b) Functions and branches with no caller and no selftest case

**No function lacks a caller.** Every `def` line is executed by `--selftest` (coverage
missing-line set starts at `86`, i.e. inside `split_cells`, never at a `def`), and `main`
is the entry point. The dead weight is at *branch* level, and it splits cleanly:

| line | branch | owner | status |
|---|---|---|---|
| `360` | `normalize_url`: `if not match: return text` | **C3** | unreachable for any cited URL (`URL_RE` guarantees the shape) and, for a map value, reachable only to produce the same `url-mismatch` the main path produces. No case. **delete** |
| `375-376` | `load_url_map`: unreadable / bad JSON → `(…, problem)` | C3 | no case; the only consumer is `main:989-994`, which no case drives. Keep the branch, drop the duplicate below |
| `378` | `load_url_map`: top-level not an object | C3 | no case. Merged with the strings-to-strings refusal in §4 (one shape refusal) |
| `379-383` | `load_url_map`: `mapping` copy + `not isinstance(key, str)` | C3 | the key conjunct is **provably false** — `json.loads` object keys are always `str` — and the copy is a second dict. **delete** |
| `419-421` | `bind_failure`: `cites-no-url` | C3 | third verdict, no case, same exit 8 and same `mismatch` bucket as `url-mismatch` (verified both ways, §4). **delete** |
| `550-553`, `570-571` | `print_quote_report` body | inherited | no case; CLI-only. Exercised by receipts (`R30SimplGate.md` §6 ran it end-to-end) — **keep** |
| `242-263` | `print_report` body | inherited | no case; `main`-only caller, stdout pinned by round-30 receipts — **keep** |
| `86`, `114`, `119`, `152`, `155`, `166`, `317-330`, `469` | `not-a-table-row`, `status=`/`source-empty` defects, `duplicate-request`/`missing`/`not-mined`, the unreadable-artifact channel, `EXIT_QUOTE_UNREADABLE` | inherited | uncased, but `114/119/317-330/469` are pinned by committed receipts (§3) and `152/155/166` are the refusal classes capability 3/4 name. Not C3's surface; **keep**, do not re-copy |

**The CLI blind spot is not theoretical.** At `39ba62b2` the whole quote-mode dispatch
(`989-997`) is unreachable: the new pairing guard was written as

```
985:        if args.url_map and not (args.quote_file and args.artifact):
986:            parser.error("--url-map needs --quote-file and --artifact")
987:    elif args.url_map:
988:        parser.error("--url-map needs --quote-file and --artifact")
989:        url_map = None            <- the rest of the quote branch became the elif's body
```

so a *correct* invocation falls through to the registry-required check. Measured, same
fixture, same argv:

```
39ba62b2:  python3 … --quote-file fx/rows_bound.txt --artifact fx/art.txt --url-map fx/map_ok.json
           → error: --registry and --package are required unless --selftest        exit 2
71a90ec0:  → QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 mismatch=0 unmapped=0
             malformed=0 cap=25 artifacts=art.txt                                  exit 0
```

and `--selftest` prints `cases=17 failed=0` on both. The guard at `985-986` is also
provably dead (inside this branch `976-977` has already required both flags), which is what
made the mis-indentation look harmless. This is the one **operability break** this seat
found; it is a fix, not a simplification, and it is the strongest argument for the point in
§5: the suite is green while the mode has no reachable entry.

## 3. (c) Can `print_quote_report` carry the new refusals without a second printer?

**Yes, and `39ba62b2` already does it.** The summary line (`555-557`) carries
`mismatch={mismatch} unmapped={unmapped}`, and each refusal is named through the existing
`quotes` channel (`508-517` appends `("REFUSED", "<id> <verdict> words=… at … quote=…")`,
printed at `570-571`). No third printer, no new report key beyond the two buckets that
`quote_check` already initialises (`461-462`) and updates (`530-533`). Two nits, both
mechanical:

- `563-564` `mismatch=len(report.get("mismatch", [])),` / `unmapped=len(report.get(…))` —
  a default that cannot fire (`quote_check` always sets both) and a second reading of the
  same contract while the neighbouring fields (`report["overlong"]`, `report["malformed"]`)
  index directly. Index them.
- **field placement.** Inserting the two fields mid-line changes a format a committed
  receipt pins. `corpus/evidence/round30/quote-mode-six-rows.txt:6,13,19,26,32,38` and
  `R30GateQuote.md:215-263` record `QUOTE rows=1 spans=3 located=3 found=3 overlong=0
  absent=0 malformed=0 cap=25 artifacts=…`; `39ba62b2` now prints `absent=0 mismatch=0
  unmapped=0 malformed=0 …`. Measured prefix test on the same fixture:

```
39ba62b2 (mid-line):  PREFIX-BROKEN   QUOTE … absent=0 mismatch=0 unmapped=0 malformed=0 cap=25 …
reduced (appended):   PREFIX-IDENTICAL QUOTE … absent=0 malformed=0 cap=25 artifacts=art.txt mismatch=0 unmapped=0
```

  Moving the two fields after `artifacts={arts}` keeps every round-30 line a byte-prefix of
  the new one at zero cost. No lane script parses this line (`grep -rn "QUOTE rows"` finds
  only the printer itself in `plans/sources_adopt.py` and historical docs), so this is
  cheap insurance for a round-31 "no harm" seat that re-runs quote mode and diffs against
  those bytes.

## 4. (d) The smallest diff that adds the binding

C3's measured footprint at `39ba62b2`: production **+126** lines (448 → 574), selftest
**+99** (367 → 466), 5 lines rewritten. What the claim's predicate actually needs
(three cases, exits 8/9, a map, a normaliser that does not confuse formatting with a
different document):

| region | `39ba62b2` | minimal shape |
|---|---|---|
| docstring capability 6 | `24-26` | keep (the file's per-capability convention) |
| `EXIT_URL_MISMATCH`/`EXIT_URL_UNMAPPED` | `55-56` | keep (2) |
| `URL_RE`, `SOURCE_COLUMN`, `cited_urls` | `337-345` | keep (case 15 asserts on `cited_urls`) |
| `normalize_url` | `348-361` (14) | **3 code lines**: `scheme,_,rest = url.strip().split("#",1)[0].partition("://")` / `host,slash,path = rest.partition("/")` / return `f"{scheme.lower()}://{host.lower()}{slash}{path}".rstrip("/")`. Keeps all three documented properties (fragment+trailing slash are formatting; subpath and `http`≠`https` are not) — case 15 still green |
| `load_url_map` | `364-384` (21) | **one shape refusal**: `if not isinstance(data, dict) or not all(isinstance(v, str) for v in data.values()): return {}, "--url-map must be a flat JSON object of artifact name to URL"` / `return data, ""` |
| `locating_artifacts` + `locates` | `387-407` | keep `locating_artifacts`; `locates` = `next(iter(locating_artifacts(…)), "")` |
| `bind_failure` | `410-428` (19) | drop `cites-no-url`; `cited_keys = {normalize_url(u) for u in cited_urls(row.cell(SOURCE_COLUMN))}`, then `mapped = [url_map[n] for n in artifact_names if n in url_map]`, `if not mapped: return "unmapped"`, `return "" if any(normalize_url(u) in cited_keys for u in mapped) else "url-mismatch"` |
| `quote_check` | buckets `461-462`, locals `475-476`, branch `508-517`, ladder `542-545` | unchanged — 2 keys, 6 branch lines, 2 ladder lines |
| printer | `555-557`, `563-564` | append the two fields after `artifacts={arts}`; index both keys |
| `main` | arg `955-960`, guard `985-987`, load `989-994` | **one** guard after the quote branch (`if args.url_map: parser.error("--url-map needs --quote-file and --artifact")`), quote body dedented back under the `if` |
| selftest | `844-930` (3 cases + decoy/guard assertions) | keep all three cases and both in-case probes |

**Measured.** I applied exactly the deletions above plus the dispatch fix to a scratch copy,
`/tmp/r31-simplgate/min3.py` (`sha256=72270b2a739ee049c6e4e9321527d6b3be21cec251d442d4b50a7912fea33a40`,
1028 lines, **−12 vs `39ba62b2`**, no lane byte touched):

- `--selftest` → `SELFTEST cases=17 failed=0`, exit 0; the fourteen round-30 case names
  unchanged and in order.
- CLI verdict matrix, live `71a90ec0` vs `min3`, nine map shapes (bound / trailing slash /
  upper-case host + fragment / other document / other map key / non-URL value / bad JSON /
  non-object / nested): **exit codes identical on all nine** (0,0,0,8,9,8,2,2,2). A no-URL
  row is 8 on both, the detail word differing (`cites-no-url` → `url-mismatch`); a subpath
  citation is 8 on both; no `--url-map` is 0 on both.
- Dispatch: quote mode works again (`exit 0`, summary printed); `--url-map` alone and
  `--url-map --registry --package` both `error: --url-map needs --quote-file and --artifact`,
  exit 2.
- Failure capability retained, five mutants on `min3` copies, all killed:
  binding block removed `failed=2`; `bind_failure` always `""` `failed=2`; `unmapped`
  returned as `url-mismatch` `failed=1`; first-artifact-only `failed=1`; pairing guard
  removed `failed=1`.

Rejected, not built: folding `bind_failure` into `quote_check`'s located branch (~17 lines
less) — it trades a named single-purpose helper for a 4-level nesting and a 3-way verdict
inside the loop. `cited_urls` inlined into `bind_failure` — case 15 asserts on it directly.

## 5. Delete / keep table

| # | item (`39ba62b2`) | action | why / what pins it |
|---|---|---|---|
| D1 | `normalize_url` fallback `359-360` | **delete** | unreachable for a cited URL; reachable for a map value only to yield the same `url-mismatch`. No case (`360` uncovered) |
| D2 | `load_url_map` key-copy `379-383` | **delete** | `not isinstance(key, str)` is provably false for JSON objects; the copy is a second dict |
| D3 | `bind_failure` `cites-no-url` `419-421` | **delete** | third verdict, no case, same exit 8 / same bucket; docstring clause "or the row cites none" goes with it |
| D4 | duplicate predicate `407` | **delete** | `locates` = `next(iter(locating_artifacts(…)), "")` |
| D5 | printer `.get` defaults `563-564` | **delete** | keys always set; neighbours index |
| D6 | mid-line summary fields `555-557` | **move** | breaks the round-30 pinned prefix; append after `artifacts={arts}` |
| D7 | dead guard `985-986` + `elif` `987` | **delete + dedent** | quote mode is unreachable at `39ba62b2`; measured exit 2 on a correct invocation |
| K1 | the fourteen round-30 cases and every assertion in them (`qreport["found"]`, `qreport["artifacts"] == ["capture.txt","notes.md"]`, `qreport["cap"] == 25`, the directory artifact, the `normalize_text` unit assertion) | **keep** | `R30GateQuote.md:72-75`; `corpus/evidence/round30/quote-mode-six-rows.txt:6,13,19,26,32,38`; `R30RevGate.md:181` ("names/verdicts **yes**"); `R30MutGate.md:50-53` maps each mutant to its case. Round-30's D2/D3/D4 delete list would have falsified all of these — that is why it stayed unapplied |
| K2 | `EXIT_QUOTE_UNREADABLE`, `load_artifact`'s problem channel (`317-330`), `quote_check:469`, the printer's problem branch (`550-552`) | **keep** | `R30GateQuote.md:240-242` pins the exact bytes `QUOTE cap=25 problem=--artifact names no file or directory: /tmp/r30-GateQuote/nope.txt` / `EXIT=2`; `R30RevGate.md:131` (G13). Round-30's D1 must **not** be applied |
| K3 | `print_report` / `print_quote_report` whole bodies (no case) | **keep** | `main`-only callers; `R30SimplGate.md` §5 compared their stdout byte-for-byte on five invocations and the summary line is quoted in committed evidence |
| K4 | `--quote-file`/`--artifact` pairing guard (`976-977`) and the mode-exclusivity guard (`980-981`) | **keep** | round-30 regression seat's finding, quoted in the comment; `R30SimplGate.md` §7.4 |
| K5 | `url_map: dict | None = None` default and `if url_map is not None:` (`508`) | **keep** | cases 11-14 call without a map; an empty `{}` map must refuse, so truthiness would silently disable the check |
| K6 | `locating_artifacts` (any-containing-artifact rule) and the decoy + `guard_exit` assertions in case 15 | **keep** | they are the only killers of the "first locating artifact" mutant (`failed=1`) and of the removed-guard mutant (`failed=1`) — measured on `min3` |
| K7 | `row_defects` `status=`/`source-empty` (`114`, `119`), `build_block` `152/155/166` | **keep** (uncased) | documented refusal classes (capabilities 2-4); not C3's surface, and removing an uncased refusal class is a claim change, not a simplification |

## 6. Non-claims and tooling

- This seat does not judge the C3 claim's truth, does not re-derive `cases=17`, and does not
  score any axis. The `39ba62b2` dispatch break is reported because it is operability, not
  because it is dead weight.
- Nothing in the lane was written except this file; the gate was never edited, only copied
  to `/tmp/r31-simplgate/` (largest file 40 KB; no clone, no campaign tool, no network
  fetch). No pacman transaction (host pause respected). No new install: `coverage` 7.17.0
  was already present via `uv tool` (`~/.local/bin/coverage`), used read-only.
- Scratch inventory: `head_sources_adopt.py`, `live_sources_adopt.py`,
  `live2_sources_adopt.py`, `min_bind.py`, `min_bind2.py`, `min3.py`, `mut_*.py`,
  `nm_*.py`, `fx/` fixtures, coverage data files.

VERDICT: DELETE the six uncased/duplicated C3 additions (normalize_url fallback, load_url_map key copy, cites-no-url verdict, the duplicated `locates` predicate, the two printer `.get` defaults, the dead inner dispatch guard whose `elif` makes quote mode unreachable) and MOVE the two summary fields to the end of the pinned line; the binding duplicates no logic that needs a second path beyond the one `bad`→`malformed` projection, `print_quote_report` already carries both refusals so no second printer is needed, and the fourteen round-30 case names plus `found=`/`cap=25`/`artifacts=`/`EXIT=2`-problem bytes must NOT be deleted because `corpus/evidence/round30/quote-mode-six-rows.txt`, `R30GateQuote.md:72-75,215-263` and `R30RevGate.md:131,181` are committed against them.
