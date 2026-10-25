# R33FMap — S103 row vs committed URL-map binding consistency (falsify probe)

Seat: `KengakuR33.R33FMap` (reviewer, leaf). Date: 2026-10-25. Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: S103 row (landed registry, canonical quote file, appended block) vs the
committed `url-map.json`; quote-gate re-run; root-only counterfactual. No lane
mutation; fixtures confined to `/tmp/r33-fmap-iemI/`.

## Evidence (all commands re-run on the current tree)

### 1. S103 source-cell URLs (three artifacts, identical URL sets)

| file | S103 `source` cell URLs |
|---|---|
| `corpus/SOURCES.md:118` (landed registry) | `https://github.com/hkust-nlp/Toolathlon` + `https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py` |
| `.ufo/waves/round-33/assimilation/append-rows.md:1` (canonical quote file) | same two URLs |
| `.ufo/waves/round-33/assimilation/append-block.md:1` (appended block) | same two URLs |

Cell-level diff of registry vs append-rows shows only anchor (cell 6) and teaches
(cell 7) prose differ; the `source` cell (cell 1) is identical. The landed row is
**not** root-only — it explicitly cites the pinned blob URL.

### 2. Committed map

`assimilation/url-map.json` (3 entries, matches the 3 captures):

```json
"toolathlon-ab-testing-evaluation-main.py": "https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py",
"arxiv-2412.05579v2-abs.html": "https://arxiv.org/abs/2412.05579",
"toolathlon-utils-evaluation-retry.py": "https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/utils/evaluation/retry.py"
```

### 3. Quote-gate re-run on the canonical `append-rows.md` (committed map)

```
$ python3 plans/sources_adopt.py --quote-file .ufo/waves/round-33/assimilation/append-rows.md --artifact .ufo/waves/round-33/assimilation/captures --url-map .ufo/waves/round-33/assimilation/url-map.json
QUOTE rows=2 spans=8 located=8 found=8 overlong=0 absent=0 malformed=0 cap=25 artifacts=SHA256SUMS.txt,arxiv-2412.05579v2-abs.html,swebench-pro-tests-test.sh,toolathlon-ab-testing-evaluation-main.py,toolathlon-utils-evaluation-retry.py mismatch=0 unmapped=0 urlmap=url-map.json entries=3
  ok S103 words=11 at toolathlon-ab-testing-evaluation-main.py … bound=toolathlon-ab-testing-evaluation-main.py->https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py
  … (all 5 S103 spans ok, all bound to the blob URL)
EXIT=0
```

### 4. Same gate on the **landed registry row** (extracted via the lane's own parser)

```
$ # /tmp/r33-fmap-iemI/row-registry-s103.md = S103 row from corpus/SOURCES.md:118
$ python3 plans/sources_adopt.py --quote-file /tmp/r33-fmap-iemI/row-registry-s103.md --artifact .ufo/waves/round-33/assimilation/captures --url-map .ufo/waves/round-33/assimilation/url-map.json
QUOTE rows=1 spans=5 located=5 found=5 … mismatch=0 unmapped=0 urlmap=url-map.json entries=3
  ok S103 … bound=…->https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py
EXIT=0
```

The committed map binds to the pinned blob URL **explicitly cited by the landed
S103 row**, not to a stale root-only citation.

### 5. Counterfactual: stale root-only S103 row under the committed map

A rebuilt row whose `source` cell cites *only* `https://github.com/hkust-nlp/Toolathlon`:

```
QUOTE rows=1 spans=5 located=0 found=5 … mismatch=5 unmapped=0 urlmap=url-map.json entries=3
  REFUSED S103 url-mismatch words=11 at toolathlon-ab-testing-evaluation-main.py …
  … (all 5 S103 spans REFUSED url-mismatch)
EXIT=8
```

So the committed map *does* distinguish blob-citing rows from root-only rows: a
root-only S103 would be refused (exit 8). The current row passes because it cites
the blob URL the map declares — this is precisely the binding the task asked to
verify.

### 6. Capture integrity and quote placement

- `sha256sum -c .ufo/waves/round-33/assimilation/captures/SHA256SUMS.txt` from the
  lane root → `OK` for all three listed captures (exit 0).
- Captures match `quotes.json` digests: `main.py` `3bad26b6…`, arxiv
  `44195c5f…`, retry `db11e66e…`.
- All five S103 quotes exist in the capture at the claimed lines: `main.py:58`,
  `:279`, `:280`, `:218`, `:234` (printed verbatim).

### 7. Committed receipt consistency

`assimilation/gate-receipts.txt` (committed) prints `mismatch=0 unmapped=0` and
each S103 `ok` line is bound to the **blob URL** — matching the re-run in §3. The
wave reports' claim that the green receipt was root-bound does not match the
committed receipt bytes.

## Findings (by severity)

| # | Finding | Severity |
|---|---|---|
| F1 | **The committed map binds to a URL explicitly cited by S103** (the pinned blob URL), in the canonical `append-rows.md` *and* the landed registry row; quote-gate re-run exits 0 with `mismatch=0`. The build-wave attack ("committed map is stale; fails exit 8; row is root-only") does **not** reproduce on the current tree. | resolved (attack refuted) |
| F2 | Build reports `R33C1KillRule.md` / `R33GateMutants.md` describe a prior state that disagrees with current committed bytes in three places: (a) "landed S103 source cell cites the root only" — current row cites root **and** pinned blob; (b) "gate-receipts.txt bound to the root URL" — committed receipt lines bind to the blob URL; (c) "quote mode with committed url-map.json exits 8" — current re-run exits 0. If those reviews predated final integration, they should not be cited as describing the committed artifacts. | informational (stale report) |
| F3 | `url-map.json` contains a third entry (`toolathlon-utils-evaluation-retry.py` → retry.py blob) cited by no S103/S104 row; `quotes.json` records it as the intentional `uncited_capture` for the entry's retry paragraph. No effect on S103 binding. | low (by design) |

## Residual risk / verification gaps

- The gate's binding rule is existential over any cited URL vs any mapped containing
  artifact (`bind_failure`, `sources_adopt.py:415-439`) — it is a citation-membership
  check, not provenance. Removing the blob URL from S103's `source` cell would
  instantly trip exit 8 (demonstrated in §5), so the current tight binding is
  enforced by the committed artifact.
- The gate checks whole-artifact byte-substring presence for each quote, not
  section/line claims; I manually verified the five claimed lines exist at
  `main.py:58/279/280/218/234` in the committed capture, but no automated counter
  enforces line numbers.
- No network probe performed (off-claim); capture freshness rests on the committed
  `fetch_check` text in `quotes.json` and the digest-bound bytes.

## Verdict

**No defect reproduced.** The committed `url-map.json` binds to the pinned blob URL
that S103 explicitly cites in both the canonical `append-rows.md` and the landed
registry row (`SOURCES.md:118`); the quote gate exits 0 with `mismatch=0` on both,
and a reconstructed stale root-only row is refused (exit 8). The map is consistent
with the S103 row; the "stale earlier root-only row" state described by the build
wave is not present in the current committed bytes.

## L1 integration update

The final S103 source cell was narrowed to the pinned blob URL only (the broader repository-root URL was removed), and S104's URL was pinned to `/abs/2412.05579v2`. `url-map.json` now matches both exact pinned URLs; the final quote-gate receipt re-runs against byte-identical staged and landed rows and passes 8/8.
