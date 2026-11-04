# SourceR85 — findings

Seat `SourceR85`, kengaku round 85, wave 1, 2026-11-04. Source seat: open the pinned
`sqlite-db-truncate` grader, draft the S272 row and the lesson's Gate block.

**Verdict: FINDINGS — 1 defect found** (the fetch, the row and the Gate block this seat was
asked for are correct; the defect is in the S272 row and Gate row another seat already landed in
this round).

## F1 — the landed S272 row and the landed round-85 Gate row cite a blank line and miscount the quote

**Where.** `corpus/SOURCES.md` line 288 (row `S272`, committed at `e7b44805`) and
`corpus/lessons/round-85.md` line 18 (the `## Gate` table row).

**What the landed bytes say.** Both state:

- quote line `:30`
- quote word count `(6 whitespace-split words)` / `(6 words)`

**What the subject bytes say.** `corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py`
(1097 B, sha256 `8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881`, byte-identical
to the live pinned fetch, HTTP 200):

```
 29|    score = len(matches)
 30|
 31|    assert score > 6, "Did not load data correctly"
```

- **Line 30 is blank.** The quoted assertion is on **line 31**.
- **The quote is 9 whitespace-split words**, not 6. Counted as `len(quote.split())` — the same
  counter `plans/sources_adopt.py` `words()` and `plans/round30_defects.py` `words()` use — giving
  `['assert', 'score', '>', '6,', '"Did', 'not', 'load', 'data', 'correctly"']`.

So the landed row's `teaches` cell also carries the wrong line: it says the grader "asserts the
intersection exceeds six at `:30`", which is the blank line, not the assertion.

**Why it matters.** The anchor cell is the row's only pointer back to the source. A reader who
follows `:30` finds nothing; a reader who trusts `(6 whitespace-split words)` has the wrong count.
Both are the defect class the lane has a standing gate for, and the defect is a *record* defect,
not a substantive one: the row's tier, scope, kind, status, opened, recheck and used-by cells are
right, and the digest it names is the right digest.

**Evidence (all reproducible, receipts in `receipts.txt`).**

- Recomputed from the capture: `line-30 holds the quote: False | len(split)= 9`.
- Rendering the landed row's own numbers in the shape `plans/anchor_line_check.py` parses
  (`:30 "…" (6 words)`) against a fixture lane carrying the real capture:
  `ROW S272 state=live defects=line:1,words:1` → exit 1.
- The same fixture with the corrected numbers (`:31 "…" (9 words)`):
  `ANCHORLINE rows=1 cited=1 captured=1 defective=0 repaired=0 live=0 cells=0` → exit 0.
- The two neighbouring rows in the same family are correct under the same recomputation, so the
  convention the landed row broke is the house one: **S267** cites `:25` with 3 claimed /
  3 actual and the quote is on that line; **S271** cites `:17` with 5 claimed / 5 actual and the
  quote is on that line. **S272** is the only one of the three that is off.

**Note on why no standing gate caught it.** `plans/anchor_line_check.py`'s `QUOTE_RE` recognises
only the `:N "…"` (double-quoted) anchor shape. S267, S271 and S272 use the backtick shape
``:N quote `…` (N whitespace-split words)``, so the checker does not parse them at all — it reports
`cited=72` of 264 rows and never examines these three. That blind spot is the lane's own routed
open finding **R82-F1** (`corpus/lessons/round-83.md` line 59, `corpus/lessons/round-84.md` line 55:
"stays open and is not called repaired by these count annotations"). F1 is therefore the **same
blind spot R82-F1 already names**, newly reached by a row landed in this round. It is not a new
gate defect; it is the first time the blind spot has admitted a row whose numbers are wrong.

**Correction path (not taken by this seat).** SOURCES contract v1 rule 2 (append-only; a
correction is a new row whose `teaches` opens `supersedes S0NN —`) and QUALITY Q34 forbid editing
the landed row's anchor or teaches cells in place. The repair is:

1. a new `corpus/SOURCES.md` row whose `teaches` opens `supersedes S272 —`, carrying the corrected
   anchor (`test_outputs.py:8-31; :31 quote … (9 whitespace-split words)`) and the corrected
   `teaches` line (`:31`), and whose `used-by` names `corpus/lessons/round-85.md`; and
2. a dated correction in `corpus/lessons/round-85.md` §Corrections naming the corrected `:31` and
   the 9-word count.

The corrected row text is ready to copy from `s272-row.md` / `proposed-s272.txt`; this seat does not
apply it, because `corpus/SOURCES.md` and `corpus/lessons/round-85.md` are read-only to a leaf seat.

**Verbatim landed cells (for the canonical judge).**

`corpus/SOURCES.md:288` anchor cell:

```
test_outputs.py:8-30; :30 quote `assert score > 6, "Did not load data correctly"` (6 whitespace-split words); accessed 2026-11-04; live 1097 B SHA256 8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881 equals the round-52 capture
```

`corpus/lessons/round-85.md:18`, located-quote cell:

```
`:30` `assert score > 6, "Did not load data correctly"` (6 words)
```

## What this seat found correct

- The pinned fetch is **HTTP 200**, **1097 bytes**, sha256
  `8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881`, and `cmp` against the
  committed round-52 capture is exit 0 — **byte-identical**. The live digest therefore equals the
  frozen claim's subject pin (`plans/round-85-claims.md` §R85-C1) and the committed receipt's
  `SUBJECT_SHA` (`corpus/evidence/round85/sqlite-db-truncate-probe.txt`).
- The capture is git-tracked and is listed in `corpus/evidence/round52/graders/SHA256SUMS` under
  the same digest, so the digest claim resolves to a committed capture.
- The landed row's tier/scope/kind/status/opened/recheck/used-by cells are all correct; only the
  anchor's line and word count are wrong. The row's URL is unique in the registry (1 row cites
  `sqlite-db-truncate/tests/test_outputs.py`), so there is no E04 duplicate-URL collision.
- The proposed row in `s272-row.md` passes every lane gate applied to it: the source-adoption quote
  gate (located, bound to the cited URL, under the 25-word cap), the source-adoption schema gate
  (11 cells, no literal or escaped `|`, valid status and recheck, no collision against the base
  registry), the anchor-line check on a fixture lane (`live=0`), and the fleet census
  (`sources-census.sh validate`, E-code set identical to the landed registry's).

## Frozen elements

`plans/round-85-claims.md` was read in full and **not edited**. Nothing in it looks wrong for this
seat's scope: the subject pin, the quoted grader semantics ("builds `{(word, value)}` sets from the
hardcoded eight-item `soln` list and from the data, and asserts `len(soln_tuples & data_tuples) > 6`")
and the "Sourced claim: … row S272" sentence all match the bytes this seat fetched. The only
mismatch is in the row and Gate row another seat landed, not in the frozen claim.

## Scope and bounds honoured

- Wrote only inside `.ufo/waves/round-85/w1/SourceR85/` and this seat's scratch. No production
  file (`plans/`, `corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`) was edited, added or deleted.
- No commit, push, stage, stash, checkout or reset, in any repo. Only read-only git
  (`log`, `show`, `ls-files`, `status`, `rev-parse`, `cat-file`) was used. The fixture repos under
  scratch were `git init`-ed only to satisfy `anchor_line_check.py`'s `git ls-files` index lookup;
  each was asserted with `git -C "$D" rev-parse --show-toplevel` before use, and nothing was
  committed.
- One network fetch: the single pinned raw URL this item names. No credentials, cookies, tokens or
  auth state were read or used.
- No subagents spawned; no `task` call.
- Tool installs: **none** — curl 8.23.0, Python 3.14.8, git and bash were already present. No
  pacman transaction was run (the host-wide pacman guard is respected).
