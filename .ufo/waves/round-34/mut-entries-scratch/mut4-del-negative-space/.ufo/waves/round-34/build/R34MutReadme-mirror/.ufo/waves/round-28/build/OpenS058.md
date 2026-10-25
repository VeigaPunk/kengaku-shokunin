# OpenS058 — re-opening of source row S058 (C2, author-side)

Writer/seat: KengakuR28.OpenS058-2 (read-only scout). Author-side advice, not outside closure.
Scope: exactly row S058 in `corpus/SOURCES.md` and its literal mentions in the frozen 35-path
population (`plans/fixtures/r28/registry/population.json`, base b9b24796277020d1b9b01923b45313d6a565e664).
No registry, knowledge, or lesson edits. No upstream code was executed or imported; the fetched files were read as text.

## Row under check (current tree is byte-identical to the base row)

`| S058 | inspect_ai pattern() no-match reasons (corrects S050 blanket reason) — https://github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py | code | A | exact no-hit reason including empty/whitespace completion exception, not JSON-policy correctness | pattern :86,:119–124 and scorer/_common.py:16–30; independent reread FSourceS050 | … | mined | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md |`

## Opening (access date 2026-10-21, fetched 2026-10-21T13:57:15Z)

| file | URL | HTTP | sha256 (raw bytes) |
|---|---|---|---|
| `_pattern.py` | https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py | 200, 4569 B | 7974ddb436917ac97f78304ae071eef75115783938358a0578f8d2e30abaae6b |
| `_common.py` | https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_common.py | 200, 6471 B | 49460816379d5cbbf48d1090ab854b243a83b652fb711f2c849dc1ff2292211b |

- The row's own blob URL `https://github.com/…/blob/63e45cc…/src/inspect_ai/scorer/_pattern.py` returned HTTP 200, and so did the `_common.py` blob.
- GitHub API `commits/63e45cc52d39b873b944124613da21fdad6f6dcc` resolves to that full SHA (committer date 2026-10-21T11:24:54Z), so the pin is a real immutable commit.
- Scratch copies: `.ufo/waves/round-28/scratch/OpenS058/{_pattern.py,_common.py}`.

### Located quotes (≤25 words each)

1. `_pattern.py:121` (no-match branch, inside the cited :119–124): `reason="no_response" if empty else "invalid_response_format",`
2. `_pattern.py:86` (the cited :86): `empty = no_response(state.output.completion or "")`
3. `_common.py:20–22` (inside the cited :16–30): "An empty or whitespace-only completion never produced output that could violate a format, so `no_response` is the correct `ScoreReason`"
4. `_common.py:30`: `return not completion.strip()`
5. `_pattern.py:77–79`, supporting the first-hit scope that is unchanged from S050: `match = re.search(pattern, state.output.completion, re.IGNORECASE if ignore_case else 0)`

## Anchor and teaches check

- **Anchor `pattern :86`: CONFIRMED.** Line 86 computes `empty` once, before the branch.
- **Anchor `:119–124`: CONFIRMED.** Lines 119–124 are exactly the no-match `Score(value=INCORRECT, reason=…, explanation=…)` return.
- **Anchor `_common.py:16–30`: CONFIRMED.** `no_response` is defined at lines 17–30, and line 16 is blank, so the range is inclusive but correct.
- **Teaches: CONFIRMED within the no-hit scope.** A nonempty unmatched completion gets `invalid_response_format`, while an empty or whitespace-only completion gets `no_response`. Python `str.strip()` defines what counts as whitespace. The first-hit scope still holds: `re.search` returns the leftmost match, and `match_first` returns the first group that equals the target, with no fallback search.
- **Scope note (observation, no change needed).** On the *match* path, `_pattern.py:112` also sets `reason="no_response"` for an empty completion: a nullable pattern can match an empty string (comment at :81–85). This lies outside the row's "no-hit reason" scope and does not contradict it. The row's scope cell "not JSON-policy correctness" stays accurate.
- **Lesson anchor drift (not a registry cell).** The round-27 lesson Gate row at `corpus/lessons/round-27.md:51` locates the quoted reason expression at "no-match branch:122". At this pinned commit the expression is on **line 121**, and line 122 is the `explanation=` line. This is a one-line drift in the lesson's gate locator; the registry anchor range :119–124 still covers it. This seat makes no edit. L1 may disclose it in round-28 notes. The registry row needs no change for it.

## Literal citations in the frozen 35-file population (base revision via `git show`; current tree identical)

The count applies pattern `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` and keeps only exact `S058` tokens.

| path | lines (base = current) |
|---|---|
| `corpus/knowledge/extraction-policy-comparison.md` | 1 (`source:` header: S058 with `_pattern.py:62–79,119–124` and `scorer/_common.py:16–30`), 18 ("`pattern()` (S058, correcting S050)") |

The other 34 frozen paths have 0 literal mentions of S058.

**Comparison with the existing mutable cells:**
- **status:** `mined`, which is correct because the row is cited.
- **used-by:** `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`. This covers the only citing frozen path. The lesson entry is an allowed extra path (the lesson cites S058 at :51, :152–159, :198, :201).
- **missing_used_by:** none.
- **recheck:** `2027-01-19`, which is 90 days after the opened date and not stale.

The knowledge file's `:62–79` anchor (docstring plus `re.search`) is consistent with the pinned source.

## Suggested allowed mutable-cell changes for S058

**None.** Status, recheck, and used-by already satisfy the C2 contract for S058, and the re-opening confirms the anchor and teaches cells. The immutable cells (id, source, kind, tier, scope, anchor, teaches, opened) need no change.

## Adjacent observation (outside the assigned ID; for the S050 owner or L1)

The same knowledge line 18 literally mentions **S050** ("correcting S050"). Under the declared literal contract, which counts historical and supersession mentions, S050 is therefore cited by `corpus/knowledge/extraction-policy-comparison.md`. Yet S050's used-by is only `corpus/lessons/round-27.md`, while its status `mined` is fine. A conforming `registry_check.py` should flag S050 `missing_used_by=[corpus/knowledge/extraction-policy-comparison.md]` on baseline. This would be a second baseline mismatch beyond S038, which bears on forecast F5. The allowed repair would append that path to S050's used-by. That is a historical correction mention, not endorsement of S050's superseded reason. This seat did not open S050 for that purpose, and the S050 seat or L1 owns the decision.

The `sources-census.sh` warning in `corpus/evidence/round28-calibration/before.txt:11` ("W04 S058 duplicate url … across scopes") is expected: S058 deliberately reuses S050's URL with a narrower superseding scope. It is a warning with exit 0, not a C2 finding.

## S056 / S038 clauses

They do not apply to this seat. S058 is neither the own-work row S056 nor the S038 paper. This seat did not open them and makes no claim about either.

## Observed commands (all read-only)

- `git show b9b24796…:<path>` over the 35 population paths, plus a stdlib Python regex count. The same for S050.
- `diff` of the base and current S058 row: ROW_UNCHANGED.
- `curl` raw fetches of `_pattern.py` and `_common.py`, HTTP checks of both blob URLs, the GitHub commit API lookup, and `sha256sum`.
- `rg` over the lesson, the evidence, and `before.txt`.

No installs or updates. No tests, builds, or linters were run.

## Limitations

- This is a literal reference check only, not semantic citation support.
- The source was read at the pinned commit; current upstream `main` was not compared.
- The whitespace semantics come from Python's documented `str.strip()`. Edge characters were not tested empirically.
- The S050 observation was derived from the frozen population text. The S050 source was not re-opened here.

## Verdict

**PASS (scoped to S058):** the source was opened at its pinned commit, and anchor, teaches, and scope are confirmed. The literal citations in the frozen population are fully covered by used-by, and status is `mined`. No mutable-cell change is suggested. Disclosed non-blocking items: the lesson's `:122` locator is off by one (actual `:121`), and S050 is literally cited by the frozen knowledge file but its used-by lacks that path. This is not a round PASS.
