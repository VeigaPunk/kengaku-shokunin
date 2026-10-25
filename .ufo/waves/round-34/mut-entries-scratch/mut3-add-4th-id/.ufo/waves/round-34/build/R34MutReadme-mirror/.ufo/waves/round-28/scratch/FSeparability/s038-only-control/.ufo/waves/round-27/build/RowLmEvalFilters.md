# RowLmEvalFilters — round 27 (accessed 2026-10-21)

Scope: lm-evaluation-harness answer-selection filters, for SOURCES row + gate receipt only. Leaf seat; no subagents; no lane files written besides this report.

## Fetched sources (read directly from GitHub raw, main)
- https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/lm_eval/filters/extraction.py
  sha256 `eb976bb36d5d3e93faafe6d065678e24b4474e78cd4fce1e730e2b8f49b9fda0` (saved /tmp/kengaku-r27-RowLmEvalFilters/extraction.py, HTTP 200)
- https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/lm_eval/filters/selection.py
  sha256 `5f8264dce91dd1282b84487d703e7e2bb11bef5fd6c93f91b4e51342a4fb76ab` (saved /tmp/kengaku-r27-RowLmEvalFilters/selection.py, HTTP 200)
- Upstream commit: `main` = `d6de81643928d653435c431bae19945d41d32520` (`git ls-remote`, 2026-10-21).
- Last-changing commit per file (GitHub API `commits?path=`): extraction.py `29270297165f7260a1f56f56c5c13f7414412306` (2026-08-26); selection.py `f724be699e8adf7ca8004ea0e519dfac83a06f18` (2025-01-19).

## What the code does (observed, not run)
- `RegexFilter.apply` (extraction.py:39-58): `findall`, then `match[self.group_select]` (:49). Default `group_select=0` (:27) = first findall match. Python indexing means a negative `group_select` reaches later matches [INFERENCE from code; not exercised].
- Tuple (multi-group) matches collapse to the first non-empty group (:50-52). No match returns `fallback` (default `"[invalid]"`, :28), not None.
- The regex filter is not fence-aware and not JSON-aware; nothing in it reads code fences or decodes JSON.
- `TakeFirstFilter` (selection.py:13-23) returns `r[0]` per doc: it chooses among repeated samples (`resps` is one list of responses per doc), not among candidate answers inside one response.

## (1) SOURCES.md row draft (contract-v1 header has 11 names; existing rows have 11 cells, checked: 48 of 48 `| S0NN |` rows)
Note: the assignment says "13 pipe-delimited cells"; the file's header and every existing row have 11. Draft follows the file (11 cells). Kind `code` is a new value (existing kinds seen: paper, docs, tool, own-work).

| S0xx | lm-evaluation-harness regex and take_first filters — https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/filters/extraction.py ; https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/filters/selection.py | code | A | the harness's own regex and take_first selection rules for which response span is kept, not any grader, score, or extraction accuracy | main d6de8164; extraction.py:27-28,39-58 (RegexFilter), :147 (MultiChoiceRegexFilter docstring); selection.py:13-23 (TakeFirstFilter) | `group_select` picks the Nth `findall` match (default 0 = first); no match returns fallback "[invalid]", not None; the regex is fence- and JSON-blind; take_first keeps the first of repeated samples per doc, not a span inside one response | queued | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |

## (2) gate.md receipt line (one quote per line; located text copied from /tmp file)
| S0xx | https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/lm_eval/filters/extraction.py | lm_eval/filters/extraction.py:147 (MultiChoiceRegexFilter.__init__ docstring, `group_select`); also :49 code | “Selects the (group_select)th match from the findall result.” | build/RowLmEvalFilters.md; main d6de8164, file last changed 29270297; HTTP 200, sha256 eb976bb36d5d3e93faafe6d065678e24b4474e78cd4fce1e730e2b8f49b9fda0 |

Second quote available if the row is widened to selection.py (not in this row): selection.py:21 “Assuming each entry of `resps` is a list of model responses, we discard all but the first response.” (18 words); sha256 5f8264dc…b76ab.

## (3) Pre-registered policy grounding
- E0–E8: **none grounded by name.** The harness filter has no fence stage (E1, E5, E6 unsupported), no JSON decoding (E4, E7, E8 unsupported), and its `BARE_RE`-equivalent is a user-supplied regex.
- Closest analog: the first-vs-last *match-selection rule* (`group_select`), at the level of E3 (bare-first) and E2 (bare-last). Use only as context for that axis, never as the source of an E-policy's semantics. A knowledge entry must not cite this row as validation of E2/E3.
- take_first: grounds nothing in E0–E8 (selects across repeats, not inside a response). Exclude from the extraction-policy knowledge entry or cite as scope boundary only.

## Findings
- F1 (file:line): extraction.py:49 `match = match[self.group_select]` — first-match default is code, not documentation.
- F2 (file:line): extraction.py:28 fallback `"[invalid]"` — a non-match is a string sentinel in the harness, so it is not comparable to the lane's `None`; any cross-comparison must map it explicitly.
- F3 (file:line): selection.py:21 — take_first is a repeat-sample selector; it is out of C1's within-response scope.
- F4: 11-vs-13 cell discrepancy between the assignment and SOURCES.md (above). Not resolved by editing; the lane owner must decide the column count before the row is written.

Installs/updates this seat: none (curl used, already present).
Files written by this seat: `.ufo/waves/round-27/build/RowLmEvalFilters.md` (this report). Scratch: /tmp/kengaku-r27-RowLmEvalFilters/{extraction.py,selection.py}.

VERDICT: source opened at main d6de8164 with hashes recorded; row drafted at 11 cells (file's column count, not the 13 in the assignment); no pre-registered E1–E8 policy is grounded by name, only context for the E2/E3 first-vs-last axis.
