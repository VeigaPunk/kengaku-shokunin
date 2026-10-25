# Round 32 — routed errata draft

Scope: exact append-only correction text drafts for D1, D6, and R7, plus the D3 CLI-receipt regeneration (the receipt is regenerated wholesale from the committed fixtures, not appended to). These are proposed text only; no fleet report, lane receipt, or lesson was edited here. Grounds: frozen claims `plans/round-32-claims.md` lines 53–83; routed findings `corpus/lessons/round-31-verifier-spotcheck.md` lines 147–170; and `plans/round32_defects.py` checks R1, R3, R6, R7. The receipt's existing tip copy has the broken `../../../plans/sources_adopt.py` command and `can't open file`/exit=2 lines; the valid historical receipt at commit `634ded8` records map-ok 0, map-bad 8, map-unmapped 9, no-map 0, registry-path 2.

## (a) Round-31 report erratum — D1

Append to `.ufo/reports/round-31/kengaku.md`:

> **Erratum (appended 2026-10-25, round-32 closure D1).** The "Erratum addendum (2026-10-25,
> trend-verdict seat)" above cites the entry-locator fixes as landed at "lane tip `a44b5a8`-class
> commits". That `a44b5a8`-class citation is bogus: `a44b5a8` identifies no commit (`git cat-file -t
> a44b5a8` → missing), and it is superseded. The real locator-fix commit is `ae95fe0` (round-31:
> entry locator corrections — verifier_mode.py:18-21, :39-40 — and final falsify evidence).

## (b) Round-31 CLI receipt regeneration — D3

Regeneration **replaces** `corpus/evidence/round31/gate-cli-exits.txt` wholesale from the committed fixtures: the file becomes the self-describing `# run:` header with the corrected path, then the executed output below, then the correction note — the stale `can't open file` block of the tip copy must not survive:

```sh
cd .ufo/waves/round-31/c3-fixtures && for m in map-ok map-bad map-unmapped; do python3 ../../../../plans/sources_adopt.py --quote-file rows.txt --artifact cap.txt --url-map $m.json; echo exit=$?; done
python3 ../../../../plans/sources_adopt.py --quote-file rows.txt --artifact cap.txt; echo no map -> exit=$?
python3 ../../../../plans/sources_adopt.py --registry ../../../../corpus/SOURCES.md --package ../../../../corpus/SOURCES.append.md --url-map map-ok.json; echo url-map on registry path -> exit=$?
```

Execution note: run the block with `set +e` (or without errexit); under `set -e` the loop aborts at
map-bad's exit 8 and writes a truncated receipt.

Append the following correction note to `corpus/evidence/round31/gate-cli-exits.txt` after the regenerated command output:

```text
# Correction (appended 2026-10-25, round-32 closure D3): the previous tip copy ran
# `../../../plans/sources_adopt.py` from .ufo/waves/round-31/c3-fixtures, which resolves to the
# absent .ufo/plans path; every line there printed a missing-file invocation failure and `exit=2`.
# Regenerated from the committed fixtures with the corrected `../../../../plans/sources_adopt.py`.
# Measured exits: map-ok exit=0, map-bad exit=8, map-unmapped exit=9, no-map exit=0 (the old
# `no map -> exit=2` was the missing-file failure, not the tool), and --url-map with
# --registry/--package exit=2 (argparse refuses before any file is opened). The regenerated output
# shape matches the valid historical receipt at commit `634ded8`.
```

## (c) Round-31 lesson locator correction — D6

Append to `corpus/lessons/round-31.md`:

> **Correction (round 32):** The `verifier_mode.py` precedence locator in the Gate source table is `:39-40`, not `:35-38`; the earlier `:35-38` reference is superseded.

## (d) Round-30 lesson corrections — D6 and R7

Append to `corpus/lessons/round-30.md`:

> **Correction (round 32):** The earlier erratum's entry line references `corpus/knowledge/contamination-transparency-card.md:78-81` are stale. The relevant entry locations are `:72` and `:82-83` in that entry; these corrected references supersede `:78-81`.
>
> **Erratum (round 32):** The `:66` grouping “S083/S086 peer-reviewed” is incorrect for S086. The registry cell records that the society publishes S086 without peer review. S086 is therefore not peer-reviewed; the grouping does not apply to S086.

## Verified grounds (read-only, this report)

- `a44b5a8`: `git cat-file -t a44b5a8` → `fatal: Not a valid object name` (phantom; D1).
- `ae95fe0`: exists (`type=commit`), subject "round-31: entry locator corrections
  (verifier_mode.py:18-21, :39-40) and final falsify evidence" — the real locator-fix commit.
- Valid receipt bytes at commit `634ded8` (`git show 634ded8:corpus/evidence/round31/gate-cli-exits.txt`):
  map-ok exit=0, map-bad exit=8, map-unmapped exit=9, no-map exit=0, url-map-on-registry-path exit=2
  with `error: --url-map needs --quote-file and --artifact`.
- Counter clauses satisfied by the drafts above: R1 (a44b5a8 kept, "superseded" in range,
  ae95fe0 named); R3 (corrected `../../../../plans/` path, tokens exit=0/8/9/2, no "can't open file");
  R6 (`verifier_mode.py` + `:39-40` within 300 chars and labelled; `:78-81` kept, `:72`/`82-83`
  added within 300 chars and labelled); R7 (S086 + "without peer review" within 250 chars, labelled
  erratum).
- Stale strings the append-only counters require to remain are left untouched in the target files;
  none of these drafts edits any production file.

VERDICT: errata-drafted
