writer: KengakuR29-2.FReopenS070-2

# FReopenS070 — live re-open of source row S070 and cell audit

Seat: `KengakuR29-2.FReopenS070-2` (actual writer: same). Item: re-open S070
(`scripts/generate_test_data.py` at pinned `dce04686a56253aefba7b18a4fa0937cf1dc987b`), record access
date / HTTP status / byte size / sha256, audit every cell (`source`, `kind`, `tier`, `scope`, `anchor`,
`teaches`, `status`, `opened`, `recheck`, `used-by`) against the live bytes, re-locate the build seat's
≤25-word quote, and count its words programmatically.

Independence: I did **not** read, import, or run `plans/config_projection.py`; its source and logic were
never consulted. The only inputs were the SOURCES row text, the build report
`.ufo/waves/round-29/build/R29SourceGenerator.md`, `plans/fixtures/r29/manifest.json`, the pinned fixture,
and network bytes/API responses. Tool installs: none (python3 stdlib, curl, coreutils only).

## What was attacked

1. Live availability and byte identity of the recorded URL, fetched twice.
2. The row's `live bytes 838` and sha256.
3. Every line number in the `anchor` cell, by 1-based listing plus per-literal containment checks.
4. Every clause of `scope` and `teaches`, by locating the construct in the live text.
5. The `source` URL string against the manifest URL and the fetch URL.
6. Registry hygiene: duplicate S070 ids, committed-row equality at the admission commit and at HEAD.
7. The `status`/`used-by` pair against corpus citations of S070.
8. The build seat's quote: exact bytes, line span, and word count by three independent counters.

## Observed facts

### Fetch record (read-only, network)

```
$ curl -sS -D headers.live.txt -o gen.live.py --max-time 60 \
    -w 'http_code=%{http_code}\nsize_download=%{size_download}\ncontent_type=%{content_type}\n' \
    'https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py'
http_code=200
size_download=838
content_type=text/plain; charset=utf-8
$ date -u '+%Y-%m-%dT%H:%M:%SZ'
2026-10-21T16:47:23Z
$ sha256sum gen.live.py
45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd  gen.live.py
$ wc -c -l -w gen.live.py
 27  87 838 gen.live.py
```

Response header `date: Wed, 21 Oct 2026 16:47:23 GMT`; `content-length: 838`; `x-cache: HIT`;
`source-age: 9`. Access date **2026-10-21** (UTC), matching the row's `opened` cell.

Second fetch at `2026-10-21T16:49:42Z`: `http_code=200 size=838`, same sha256,
`cmp gen.live.py gen.live2.py` → `FETCH_IDENTICAL`. Bytes are LF-only: `CRLF 0`, `BOM False`,
`final_byte b'\n'`, 27 newlines, 87 whitespace words.

### Byte-pin cross-checks

```
$ cmp gen.live.py plans/fixtures/r29/generate_test_data.py && echo CMP_IDENTICAL
CMP_IDENTICAL
$ sha256sum plans/fixtures/r29/generate_test_data.py plans/fixtures/r29/manifest.json
45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd  plans/fixtures/r29/generate_test_data.py
f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87  plans/fixtures/r29/manifest.json
```

GitHub API cross-pins (all HTTP 200):

- Commit `dce04686a56253aefba7b18a4fa0937cf1dc987b` exists; committer date `2025-11-26T21:15:59Z`;
  message first line `Merge pull request #183 from alzambranolu13/patch-2`.
- `compare/main...dce04686a5…`: `status identical`, `ahead_by 0`, `behind_by 0`.
- `contents/scripts/generate_test_data.py?ref=dce04686a5…`: `sha 0da10ffc7478d0a8febf14bddce1ed7becaba2c4`,
  `size 838`; locally computed git blob sha1 of the fetched bytes is the same
  `0da10ffc7478d0a8febf14bddce1ed7becaba2c4`.
- Manifest URL for `plans/fixtures/r29/generate_test_data.py` is character-identical to the row URL and
  to the fetch URL; manifest sha256 equals the row's anchor hash.

### Row cells, checked individually

Row parsed with `line.strip('|').split('|')` → 11 fields; S070 rows in `corpus/SOURCES.md`: 1.

| # | cell | evidence from live bytes / registry | result |
|---|---|---|---|
| 0 | `id` S070 | unique row id (count 1) | OK |
| 1 | `source` title+URL | URL char-identical to manifest URL and fetch URL; 200 `text/plain` | OK |
| 2 | `kind` `code` | file is Python source; `code` is the registry kind used for source files (S069, S073) | OK |
| 3 | `tier` `A` | SOURCES header defines A to include source code, scoped to `scope` | OK |
| 4 | `scope` | four positives located: replacements 11–16, aggregate write 17–18, parse 20, enumerate filenames 21–23; exclusions match what the 27-line file does not contain | OK |
| 5 | `anchor` | every literal at its claimed line; revision prefix and hash match; 838 bytes match both fetches | OK |
| 6 | `teaches` | all five clauses confirmed (below) | OK |
| 7 | `status` `queued` | valid registry enum; no corpus file cites S070 | OK |
| 8 | `opened` 2026-10-21 | two fetches today, both 200 | OK |
| 9 | `recheck` `on-release` | registry policy token, used by sibling rows (S005, S006, S023, S026); not a source fact | OK |
| 10 | `used-by` `—` | grep for `S070` over `corpus/` matches only `corpus/SOURCES.md:92`; `corpus/knowledge/webarena-config-projection.md` does not exist; the draft citation is outside corpus | OK |

Clause checks for `teaches` (line numbers from `nl -ba` on the live file):

- Six global `str.replace` passes: whole file contains exactly 6 `.replace(` occurrences, all at 11–16,
  none with a `count` argument (lines 11–16 each read `raw = raw.replace("__TOKEN__", NAME)`).
- On serialized text, in listed order: `raw` is read from `config_files/test.raw.json` in text mode
  (lines 9–10) and each pass reassigns `raw` to the previous pass's output; token order is
  `__GITLAB__`, `__REDDIT__`, `__SHOPPING__`, `__SHOPPING_ADMIN__`, `__WIKIPEDIA__`, `__MAP__`
  (lines 11–16, regex-extracted RHS names `GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP`).
- Before any parse: the only parse is `json.loads` at line 20 (no `json.load(` anywhere); the aggregate
  write at lines 17–18 precedes it.
- Aggregate write first: lines 17–18 open `config_files/test.json` and `f.write(raw)`.
- No visible repair step: `try:` count 0, `except` count 0 in the file; `json.loads` is called directly.
- Enumeration index, not `task_id`: line 21 `for idx, item in enumerate(data):`; line 22 writes
  `config_files/{idx}.json`; `task_id` occurs 0 times in the file; `idx` occurs 2 times (both in 21–22).
- Full anchor-literal containment check over 19 named positions (def main 8, read 9–10, six replacements
  11–16, aggregate 17–18, comment 19, `json.loads` 20, enumerate 21, filename 22, dump 23, guard 26,
  call 27, wildcard import 5) → `all True`.

### Build-seat quote re-located and counted

Quote block extracted from `R29SourceGenerator.md` (`### Located quote`, fenced `text`):

```
    raw = raw.replace("__GITLAB__", GITLAB)
    raw = raw.replace("__REDDIT__", REDDIT)
    raw = raw.replace("__SHOPPING__", SHOPPING)
    raw = raw.replace("__SHOPPING_ADMIN__", SHOPPING_ADMIN)
    raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)
    raw = raw.replace("__MAP__", MAP)
```

- Byte equality with live lines 11–16: `True` (exact, including 4-space indentation).
- Lines: 6; per-line whitespace words `[4, 4, 4, 4, 4, 4]`.
- Word counts, three methods: Python `len(quote.split())` = **24**; `wc -w quote.txt` = **24**;
  `awk '{n+=NF}'` = **24**. 24 ≤ 25, so the build seat's count and the ≤25-word rule both hold.
- The build seat's claim "each line contributes 4 whitespace-delimited words" and "27 lines; `wc -w` 87"
  both reproduce exactly.

### Independent semantic witness for the `global`/`order` clause

Synthetic string, Python `str.replace` default only (no production code): after replacing `__GITLAB__`
with a value containing `__MAP__`, the later `__MAP__` pass consumed 3 occurrences (2 original + 1
inserted), `total_replacements 4`. This confirms that no-count `str.replace` is global per pass and
that a listed order can cascade, matching the row's clause without relying on the instrument.

## Mismatches found

None. 11 of 11 cells are supported by the live bytes or by the registry convention that defines them;
0 clauses of `scope`/`teaches` contradict the live text; the quote is exact and 24 words.

Two wording ambiguities, neither a false claim:

1. `anchor` "main:8–23" can be read as branch `main` or as function `main()`; both hold as observed
   (`compare` reports `main` identical to the pinned commit; `def main()` is line 8 and its body ends
   at line 23).
2. `teaches` "the aggregate text is written first" is elliptical; only the "before `json.loads`"
   reading is true, and the row's own first clause ("before any parse") fixes that reading.

## Boundaries

- `browser_env/env_config.py` was never fetched, imported, or executed; replacement values remain
  unobserved and are explicitly excluded by the row's `scope`.
- The build seat's 2026-10-21 access cannot be re-observed; my own two fetches are the access record
  here. Raw.githubusercontent served `x-cache: HIT`; identity to the pinned commit is independently
  pinned by the contents-API git blob sha.
- `main`-head equality was observed once, at `2026-10-21T16:47Z`; it is a time-dependent fact, while
  the pin itself is immutable.
- No production, fixture, corpus, SOURCES, SCORECARD, or candidate file was edited; no lane git
  mutation; my writes are limited to this report and
  `.ufo/waves/round-29/scratch/falsify/FReopenS070-2/`.

VERDICT: PASS
