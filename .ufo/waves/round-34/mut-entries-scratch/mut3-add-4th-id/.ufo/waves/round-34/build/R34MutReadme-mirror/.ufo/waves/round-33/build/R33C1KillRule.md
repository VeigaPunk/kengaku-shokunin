# R33C1KillRule — critical review of C1's kill rule and the adoption gate's binding modes

Seat: R33C1KillRule (critic, leaf). Date: 2026-10-25. Lane: kengaku-shokunin @ 2b4cef2.
Scope: `plans/round-33-claims.md` C1 kill rule, `plans/sources_adopt.py` (quote-file,
url-map, collision modes), `plans/adoption_check.py`, `plans/round33_c1_verify.py`,
and the materialized round-33 assimilation artifacts.

## Ground truth (all read-only)

- Landed registry: 97 rows, ids ≤ S104. S103 @ `SOURCES.md:118`, S104 @ `:119`, both inside
  `## Registry` (lines 19–119), just before `## Paths` (@120). S103 then S104, in want-order.
- S103's landed `source` cell cites **the repository root only**:
  `https://github.com/hkust-nlp/Toolathlon`. S104 cites `https://arxiv.org/abs/2412.05579`.
- Landed S093: `status=mined`, `opened=2026-10-25`, `usedby` lists **both**
  `corpus/knowledge/benchmark-verifier-execution-model.md` and
  `corpus/knowledge/benchmark-grader-semantics.md` (correct two-entry merge).
- Committed `url-map.json` maps artifacts to **blob URLs**:
  `toolathlon-ab-testing-evaluation-main.py -> …/blob/9be8d8fe…/tasks/finalpool/ab-testing/evaluation/main.py`,
  `arxiv-2412.05579v2-abs.html -> https://arxiv.org/abs/2412.05579`,
  `toolathlon-utils-evaluation-retry.py -> …/blob/9be8d8fe…/utils/evaluation/retry.py`.
- Committed `gate-receipts.txt` (the binding receipt) prints
  `bound=toolathlon-ab-testing-evaluation-main.py->https://github.com/hkust-nlp/Toolathlon`
  — i.e. the receipt bound to the **root URL**, not the blob the committed map currently declares.
- Captures committed: `arxiv-2412.05579v2-abs.html`, `swebench-pro-tests-test.sh`,
  `toolathlon-ab-testing-evaluation-main.py`, `toolathlon-utils-evaluation-retry.py`,
  + `SHA256SUMS.txt` inside the same artifact directory. Claims-dir SHA256SUMS covers
  test.sh (b6f26eec…) and the two round-33 captures; `retry.py` has a capture but no
  SHA256SUMS row.
- `python3 plans/adoption_check.py --expect …/adoption-expect.json --census` →
  `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` exit 0.
- `python3 plans/round33_c1_verify.py --lane .` → `checks=8 defects=0` exit 0.
- Freshest quote lines at pinned revision: `main.py:58` signature, `:279` call-site comment,
  `:280` sole call with `tolerance_pct=0.05`; `:218` `return True # Don't fail evaluation…`,
  `:234` `if not check_abtesting_logging_bucket_clean(…)`. All verified in the committed capture.

## Failure-mode table

| # | Degradation mode | C | Evidence / reproduction | Severity |
|---|---|---|---|---|
| 1 | **Quote found but in a different section than the anchor claims** — agent `locates` is a byte-substring test over the whole artifact; no line/section/scope check. | UNCAUGHT | The gate never compares the anchor's claimed line (:58/:279/:280) or section to where the substring actually occurs. The entry's prose claims (`main.py:213-218`, `main.py:234`) are asserted, not gated. | medium |
| 2 | **url-map maps a capture to a URL the row cites loosely (repo root vs file)** — `normalize_url` keeps subpaths distinct, but a row citing the root is satisfied by *any* capture mapped to that root. | UNCAUGHT BY DESIGN (materialized) | Proof: with a root map `{"toolathlon-utils-evaluation-retry.py": "https://github.com/hkust-nlp/Toolathlon"}`, a row whose source cell names `tasks/finalpool/ab-testing/evaluation/main.py` passes (exit 0) on the quote `"DEFAULT_MAX_ATTEMPTS = 3"`, which exists **only** in `retry.py`. `gate-receipts.txt` bound S103 through exactly this root-level map, and landed S103 cites the root. | **HIGH** |
| 3 | **Gate receipt vs landed bytes disagree** — the file validated (`--quote-file`) is not the bytes appended (`--package`/`--admit-ids`); no checksum binds them, and quoted + appended rows are separate artifacts. | UNCAUGHT (materialized) | Committed receipt: root-bound OK. Re-run of the *same command* against **landed** S103/S104 rows (SOURCES.md:118-119) with the committed blob map → `mismatch=2`, exit 8. `append-rows.md` passes (exit 0) only because its S103 source cell cites the blob; the landed row cites the root. A green binding receipt therefore does not characterize the registry rows. | **HIGH** |
| 4 | **used-by update clobbers an existing list** — `build_block` unconditionally overwrites cell 10 with the current round's entries; mined rows edited manually outside the gate are not diff-checked. | UNCAUGHT (did not materialize) | S093's registry `usedby` was edited by hand to merge both entries; no counter checks that prior entries survive. `adoption_check` checks only that *current* cited rows name the entry. | medium-high |
| 5 | **Append that reorders rows** — `build_block` emits rows in `want_ids` order; nothing checks sorted order or that the append lands inside `## Registry`. | PARTIALLY CAUGHT | This round landed S103, S104 in order before `## Paths` — fine. The order/section check itself does not exist (census E12 only catches rows outside the `## Registry` section; within-section ordering is unchecked). | low |
| 6 | **0–3-space anchor missing an over-indented row** — `ROW_RE` matches 0–3 leading spaces; 4+ spaces (indented code) are invisible to collision check, `adoption_check`, `round33_c1_verify.ROW_RE`, and the census. | UNCAUGHT | The committed id-guard proof itself shows the guard is anchored; an over-indented S103 (4 spaces) would be invisible to `parse_rows`, so an append would double-register invisibly. | medium |
| 7 | **Census passing on duplicate URLs (W04 only)** — duplicate URL+scope is E04, but same URL across different scopes is W04 → warnings never affect clean lanes. | UNCAUGHT | Landed S103 cites the same repo root already cited by S080/S102/S107/S108/S114 rows; census still `ok` (15 W04 before, exit 0). | medium |
| 8 | **Vacuous quote pass** — `quote_check` exits 0 if the quote file parses to zero rows, or if the row ids don't include the pinned ones; nothing requires the cited rows to be present. | UNCAUGHT (materialized in artifacts) | `quotes.json` exists but is **not** gate-consumable (`--quote-file` would parse 0 rows → exit 0); `quotes-rows.txt` is a 2-line skeleton with `scope`/`teaches` placeholders that *does* parse, passes schema, and would land placeholder garbage. No counter reads appended rows' scope/teaches/anchor cells. | medium |
| 9 | **Kill-rule exits not bound to the predicate** — `adoption_check` / `round33_c1_verify` never invoke `sources_adopt.py`; the kill rule is a process obligation. A hand-crafted append with unverified quotes passes all counters. | UNCAUGHT | `round33_c1_verify` checks entry substance, pins, refusal rows, renumber map — never the captured quote bytes. | **HIGH** |
| 10 | **`--attest-opened` launders a stale row** — re-dates `opened` to the access date without verifying the fetch. | UNCAUGHT (guarded by flag) | The flag exists for S103/S104; capture freshness is asserted in `quotes.json`'s `fetch_check` text, which no counter verifies. | low |
| 11 | **Helper artifact absorbed into quote search** — `load_artifact` treats *every* UTF-8 file under `captures/` as a quote candidate, including `SHA256SUMS.txt`. | UNCAUGHT | Receipt prints `artifacts=SHA256SUMS.txt,arxiv-…,swebench-pro-…,toolathlon-ab-…,toolathlon-utils-…` — the manifest is a candidate quote source. | low |
| 12 | **Multiple artifacts / sweep-first match** — `locates` returns the first containing artifact in sorted order; `bind_failure` accepts *any* mapped containing artifact. | UNCAUGHT | If a quote also occurs in a second capture (e.g. retry.py), the bound pair could point at the wrong file yet still pass; the pair is printed but not policed. | medium |
| 13 | **Extra cited URLs silently widen binding** — `cited_keys` is a set; any one match binds. A typo'd second URL broadens acceptance. | UNCAUGHT | `bind_failure` iterates all cited URLs; normalized equality is exact (http≠https, www≠non-www), so an over-loose citation set is never refused. | low |
| 14 | **Quote spans counted from the whole cell** — only `"…"` spans are measured; unquoted anchor prose is never checked against the capture. | UNCAUGHT | The gate measures 4–8 spans per row; the rest of the anchor cell (e.g. `:58, signature default`) is unexamined prose. | low |

## The two most dangerous uncaught paths

1. **Non-identity of validated bytes vs landed bytes + root-level binding (rows 2+3).**
   The binding receipt was produced against `append-rows.md` (blob-citing), but the landed
   S103 row cites the repo root; re-running the documented command against the landed registry
   yields exit 8. Because the landed citation is root-grained, the gate's own docs admit any
   capture declared against that root satisfies the row — and the root-map reproduction proves a
   quote from `retry.py` satisfies a row named for `main.py`. The kill rule can therefore be
   green while the cited quote lives in a different file of the same repository, and the
   currently committed url-map cannot reproduce the committed green receipt.

2. **The kill rule is not enforced by any counter (rows 8+9).** Neither frozen predicate
   command invokes `sources_adopt.py`; `quote_check` exits 0 on zero parsed rows; nothing binds
   the quote file to the appended block. A manifest whose `source:` lines, pins and registry rows
   are all fabricated passes every check. The only artifact that shows the gate ran is a wave
   receipt, which is not consumed by the predicate.

## Manual seat reviews required

- Verify the entry's section/line claims against the captured file (rows 1, 12): specifically
  `main.py:213-218` and `main.py:234` semantics, and that `:58`/`:279`/`:280` are the real
  lines (verified present in the committed capture — but not by any automated check).

## VERDICT

killrule-gap
