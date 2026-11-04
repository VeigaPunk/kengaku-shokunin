# SourceR85 — Gate block for the round-85 lesson's S272 row

Seat `SourceR85`, kengaku round 85, wave 1, 2026-11-04. Drafted by the source seat; **not** applied
to `corpus/lessons/round-85.md` (production files are read-only to this seat; the L1 owns the
landing). Shape follows `corpus/lessons/round-84.md` §Gate (the `id and decision | URL | access date
| located quote | reason / flip` table).

## Gate table row (copy-paste ready)

```
| S272 admit, A for this pinned grader's acceptance predicate (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-db-truncate/tests/test_outputs.py | 2026-11-04 | `:31` `assert score > 6, "Did not load data correctly"` (9 whitespace-split words) | The pinned grader supplies the acceptance rule: a set intersection of `(word, value)` pairs must exceed six of the eight hardcoded rows (`:8-17`, `:24-25`, `:31`), so the predicate is a strict `> 6` threshold on the intersection cardinality. It does not prove an agent solved the task. Flip: a revision whose grader bytes differ from the pin is opened and anchored, or a solved-task claim is made from it as a separate claim (not made here). Live fetch: HTTP 200, 1097 B, sha256 `8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881`, byte-identical to the committed round-52 capture `corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py`. |
```

## The five required fields

- **URL** — `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-db-truncate/tests/test_outputs.py`
  (pinned commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, the same pin the frozen claim and the
  committed round-52 capture carry).
- **Access date** — `2026-11-04`.
- **Located quote** — `:31` `assert score > 6, "Did not load data correctly"` — **9 words**, counted
  as `len(quote.split())` (the `wc -w` convention used by `plans/sources_adopt.py` `words()` and
  `plans/round30_defects.py` `words()`); under 25, so inside the SOURCES contract v1 rule 1 cap and
  QUALITY Q3. The quote is a byte-exact substring of the capture's line 31.
- **Admit reason** — the pinned upstream grader is primary and authoritative (tier A) for exactly
  one scope: the acceptance predicate this round's offline member replay reproduces. The bytes
  state the rule without the round having to reimplement it: the grader loads
  `/app/recover.json` (`:22`), builds `(word, value)` sets from the hardcoded eight-row `soln`
  list (`:8-17`) and from the file's data (`:24-25`), intersects them (`:28`), and asserts the
  intersection cardinality exceeds six (`:31`). That is the two-leg predicate the frozen R85-C1
  case table exercises (set-intersection score; `score > 6` verdict).
- **Flip condition** — a revision whose grader bytes differ from the pin is opened and anchored
  (as a new superseding row), or a solved-task/model claim is made from this source as a separate
  claim (not made here). Until then the row's scope stays member replay only.

## Scope statement the Gate must carry

The row's scope is **member replay only**: this pinned grader's acceptance predicate. It is not a
solved-task, model, image or serving-plane claim. Matching bytes do not prove an agent solved the
task; they only fix what the grader would have returned for a given staged `/app/recover.json`.

## Evidence behind this Gate block

- Fetch (single pinned URL, output written only to this seat's scratch): **HTTP 200**, **1097
  bytes**, sha256 `8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881`.
- `cmp` against `corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py`:
  exit 0, **byte-identical**. The capture is git-tracked and is listed in
  `corpus/evidence/round52/graders/SHA256SUMS` under the same digest.
- The live digest equals the frozen claim's subject pin
  (`plans/round-85-claims.md` §R85-C1) and the committed receipt's `SUBJECT_SHA`
  (`corpus/evidence/round85/sqlite-db-truncate-probe.txt`).
- The quote's line and word count were recomputed from the bytes, not carried over from another
  row: `len(quote.split()) == 9`; line 30 of the capture is blank, line 31 holds the assertion.

Full command transcript: `receipts.txt` in this directory.

## Note for the L1 — the landed Gate row repeats the same two numbers

The Gate row already committed to `corpus/lessons/round-85.md` at `e7b44805` states `:30` and
`(6 words)`. The bytes give `:31` and 9 words. The correction is a dated correction in the lesson
(a new superseding `corpus/SOURCES.md` row per SOURCES contract v1 rule 2, plus a lesson
correction), not an edit of the committed Gate table. This seat does not touch production files;
the discrepancy is reported in `findings.md`.
