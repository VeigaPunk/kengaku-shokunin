# FxDefectsFixD3 — D3 CLI-receipt regeneration review

Round 32, 2026-10-25. Leaf seat review of the planned D3 repair: regenerated round-31 CLI
receipt `corpus/evidence/round31/gate-cli-exits.txt`. Read-only review; no production files
edited (verification runs executed below wrote nothing).

## 1. Current (broken) receipt — confirmed at lane tip

Committed tip copy (`git show f20a1097:corpus/evidence/round31/gate-cli-exits.txt`) runs
`../../../plans/sources_adopt.py` from `.ufo/waves/round-31/c3-fixtures`, which resolves to the
absent `.ufo/plans` path. All five runs print missing-file invocations — e.g.

```
python3: can't open file '/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-31/c3-fixtures/../../../plans/sources_adopt.py': [Errno 2] No such file or directory
url-map map-ok -> exit=2
```

and likewise map-bad, map-unmapped, no-map, registry-path — every exit recorded as `exit=2`,
including `no map -> exit=2` (which is not the tool's no-map behavior).

## 2. Draft plan (R32DraftErrata.md §(b)) — matches the required shape

- Regeneration **replaces** the receipt wholesale from the committed fixtures, using
  `../../../../plans/sources_adopt.py` run from `.ufo/waves/round-31/c3-fixtures` (the run
  header does `cd .ufo/waves/round-31/c3-fixtures`). Resolve check: from
  `c3-fixtures/` → `../` = `round-31`, `../../` = `waves`, `../../../` = `.ufo`,
  `../../../../` = lane root, so `../../../../plans/sources_adopt.py` = `plans/sources_adopt.py`. ✓
- Five runs specified: map-ok, map-bad, map-unmapped, no-map, `--url-map` with
  `--registry`/`--package`; expected exits 0/8/9/0/2. ✓
- Explicit constraint: the stale `can't open file` block "must not survive"; correction note
  appended records old failure, new exits, and the argparse exit-2 guard. ✓

## 3. Exact execution from the fixtures (my run) — exits match

Ran from `.ufo/waves/round-31/c3-fixtures`:

```sh
for m in map-ok map-bad map-unmapped; do python3 ../../../../plans/sources_adopt.py --quote-file rows.txt --artifact cap.txt --url-map $m.json; rc=$?; echo "url-map $m -> exit=$rc"; done
python3 ../../../../plans/sources_adopt.py --quote-file rows.txt --artifact cap.txt; echo "no map -> exit=$?"
python3 ../../../../plans/sources_adopt.py --registry ../../../../corpus/SOURCES.md --package ../../../../corpus/SOURCES.append.md --url-map map-ok.json; echo "url-map on registry path -> exit=$?"
```

Measured exits: **map-ok → 0, map-bad → 8, map-unmapped → 9, no-map → 0, registry path → 2**
(0/8/9/0/2, exactly as claimed). Full produced lines:

```
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=cap.txt mismatch=0 unmapped=0 urlmap=map-ok.json entries=1
  ok S900 words=6 at cap.txt quote="the verifier shares the agent container" bound=cap.txt->https://example.invalid/docs/verifier.html
url-map map-ok -> exit=0
QUOTE rows=1 spans=1 located=0 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=cap.txt mismatch=1 unmapped=0 urlmap=map-bad.json entries=1
  REFUSED S900 url-mismatch words=6 at cap.txt quote="the verifier shares the agent container"
url-map map-bad -> exit=8
QUOTE rows=1 spans=1 located=0 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=cap.txt mismatch=0 unmapped=1 urlmap=map-unmapped.json entries=1
  REFUSED S900 unmapped words=6 at cap.txt quote="the verifier shares the agent container"
url-map map-unmapped -> exit=9
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=cap.txt
  ok S900 words=6 at cap.txt quote="the verifier shares the agent container"
no map -> exit=0
usage: sources_adopt.py [-h] [--selftest] [--registry REGISTRY]
                        [--package PACKAGE] [--admit-ids ADMIT_IDS]
                        [--entries ENTRIES] [--access-date ACCESS_DATE]
                        [--recheck RECHECK] [--out OUT]
                        [--quote-file QUOTE_FILE] [--artifact ARTIFACT]
                        [--url-map URL_MAP] [--attest-opened]
                        [--scope-to-admit]
sources_adopt.py: error: --url-map needs --quote-file and --artifact
url-map on registry path -> exit=2
```

These match the historical valid receipt at commit `634ded8` (map-ok 0, map-bad 8,
map-unmapped 9, no-map 0, registry-path 2, with `error: --url-map needs --quote-file and
--artifact`).

## 4. Planned receipt state (on-disk, uncommitted) — satisfies R3

Current on-disk receipt content:
- `can't open file` occurrences: **0**.
- Exit tokens: `exit=0` ×2 (map-ok, no-map), `exit=8` ×1, `exit=9` ×1, `exit=2` ×1 — all
  five runs recorded with the correct codes.
- `../../../../plans/sources_adopt.py` present in the run header.

Counter `plans/round32_defects.py` check_r3 (no `can't open file`; tokens exit=0/8/9/2;
corrected `../../../../plans/` path) passes on this tree: running
`python3 plans/round32_defects.py --lane .` reports `defects=5` and **R3 is not among the
defects** (R1/R2/R5/R6/R7 remain open pending the other draft repairs — out of D3 scope).

## 5. Minor residual note (non-blocking)

The on-disk planned receipt records only the first 4 argparse usage lines for the registry-path
run and omits the `sources_adopt.py: error: --url-map needs --quote-file and --artifact` line,
which the real tool prints and which both the historical receipt (`634ded8`) and the errata
draft's verified-grounds section include. This does not affect the recorded exit codes, the R3
tokens, or the absence of `can't open file`; it is a cosmetic truncation of the run output.

## VERDICT: d3-closable
