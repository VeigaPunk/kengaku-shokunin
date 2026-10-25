# OpenS055 — reopen S055 (openai/simple-evals extraction call sites)

Writer/seat: KengakuR28.OpenS055-2 (read-only scout, author-side advice; not outside non-author closure).
Lane tree observed at HEAD f0ba09be0f3066daba2134b943d973ad1588f34a; baseline b9b24796277020d1b9b01923b45313d6a565e664.
Scope: S055 only. S038 and S056 have dedicated seats (OpenS038, OpenS056 in build-assignments.json); this
report does not open them or claim anything about them.

## Row under test (corpus/SOURCES.md:77, identical at baseline b9b2479 line 77)

`| S055 | openai/simple-evals extraction call sites — https://github.com/openai/simple-evals/tree/652c89d0ca9df547706735883097e9537d40dc47 | code | A | reference Answer-pattern extraction call sites, not JSON-policy semantics | math_eval.py:53–54; DROP:286–287; mmlu_eval.py:108–113 | first regex match and task-specific fallback are established harness choices; no lane JSON policy is a faithful simple-evals port | mined | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md |`

## Opening (accessed 2026-10-21, 13:57Z)

URL: https://github.com/openai/simple-evals/tree/652c89d0ca9df547706735883097e9537d40dc47 (HTTP 200).
The commit API returned sha 652c89d0ca9df547706735883097e9537d40dc47, committer date 2026-04-22T22:16:16Z, message
"Merge pull request #108 … HealthBench Professional options". I fetched the files as raw bytes from
`https://raw.githubusercontent.com/openai/simple-evals/652c89d0…/<file>` and kept them as data only, without
running or importing them. Scratch copies are in `.ufo/waves/round-28/scratch/OpenS055/`.

| file | bytes | SHA-256 |
|---|---|---|
| math_eval.py | 2774 | 845500fb5299620e158f12ae7d8618ca64a50dc69b5535cc793e8498bdcce136 |
| drop_eval.py | 11212 | 90cceebebe914fa4e58dc676940cdb500ff34f97a6a3db20278c2c8df19d57ae |
| mmlu_eval.py | 4956 | e9165b54137cff50bf0afe30bfb343812335edcb5ae3f13ec78898871239af6c |
| common.py | 10588 | 84616c52821a30ae3f55f153a763153fd833cb41b547b09f547b46e6337f8f35 |

The hash of `math_eval.py` matches the round-27 receipt in `corpus/evidence/round27-sources/gate.md:14`
(845500fb…6136). This means the pinned bytes are the same ones round 27 opened.

### Located quotes (each ≤25 words)

- math_eval.py:53–54: `match = re.search(ANSWER_PATTERN, response_text)` / `extracted_answer = match.group(1) if match else None`
- drop_eval.py:286–287: `match = re.search(ANSWER_PATTERN, response_text)` / `extracted_answer = match.group(1) if match else response_text`
- mmlu_eval.py:108–113: `for answer_regex in MULTILINGUAL_ANSWER_REGEXES:` … `match = re.search(regex, response_text)` / `if match:` … `break`
- common.py:27 (supporting context): `ANSWER_PATTERN = r"(?i)Answer\s*:\s*([^\n]+)"`

## Anchor and teaches check

- **Anchor `math_eval.py:53–54`: CONFIRMED** exactly. The code takes the first (leftmost) `re.search` hit and
  returns `None` when nothing matches.
- **Anchor `DROP:286–287`: CONFIRMED** in `drop_eval.py:286–287`. The cell uses the label "DROP" rather than
  the filename, which is slightly imprecise but not wrong. On no match, DROP falls back to the full
  `response_text`, which is the "task-specific fallback".
- **Anchor `mmlu_eval.py:108–113`: CONFIRMED** exactly. It first tries every regex in
  `MULTILINGUAL_ANSWER_REGEXES` (common.py:32–), in list order, and stops at the first regex that matches. The
  extracted answer stays `None` if no regex matches.
  - Nuance: in MMLU, "first" means the first regex in the list's priority order, using the leftmost hit for
    that regex. It does not mean the leftmost hit across all regexes. The teaches cell ("first regex match")
    still holds at this level of detail, and the knowledge entry does not depend on the MMLU case.
- **Teaches: CONFIRMED and narrow.** Within these three files, the code supports "first regex match and
  task-specific fallback are established harness choices": MATH returns `None`, DROP returns the full
  response, and MMLU returns `None` after the ordered regex list. Nothing in these call sites parses JSON, so
  the negative clause "no lane JSON policy is a faithful simple-evals port" is consistent with what I
  observed. This is my inference from the absence of JSON parsing in the cited call sites, not a claim about
  the whole repository.
- **Scope cell** ("call sites, not JSON-policy semantics") is appropriately bounded. **Tier A** is appropriate
  for this scope because it is primary source code at a pinned commit.

## Literal citations in the frozen 35-file population

I scanned the paths listed in `plans/fixtures/r28/registry/population.json` with its `reference_pattern`
`(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`. I ran this both on the working tree and with
`git show b9b2479:<path>`, and the results are identical:

- `corpus/knowledge/extraction-policy-comparison.md:1`: front-matter `source:` header, `S055 https://github.com/openai/simple-evals/tree/652c89d0… math_eval.py:53`
- `corpus/knowledge/extraction-policy-comparison.md:20`: `(S055 math_eval.py:53–54) uses a first \`Answer:\` match and returns None on no match.`

No other frozen knowledge file contains S055. That gives 1 citing file (2 mentions).

Outside the frozen population, the remaining mentions are allowed lesson and evidence uses:
`corpus/lessons/round-27.md:48,56,201` and `corpus/evidence/round27-sources/gate.md:14,19`.

Semantic spot-check, which goes beyond the literal-only C2 contract: line 20 limits its "returns None" claim to
math_eval.py:53–54. That matches the opened code, so it is not overstated. It does not generalize to DROP,
which would be wrong.

## Status / used-by comparison

| cell | current | required by C2 literal contract | finding |
|---|---|---|---|
| status | mined | mined (cited) | OK |
| used-by | corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md | must include every citing frozen path, i.e. extraction-policy-comparison.md | OK (`missing_used_by` = ∅); the extra lesson path is allowed |
| recheck | 2027-01-19 | — | not due; no change |

History: `corpus/lessons/round-27.md:201–202` records the used-by change from `corpus/lessons/round-27.md` to
`corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`, with status and recheck
unchanged. The current row matches that history.

## Suggested mutable-cell changes

**None.** Status, recheck and used-by are already consistent with the frozen literal references. Immutable
cells stay unchanged. The "DROP" label in the anchor is slightly imprecise (the file is `drop_eval.py`). I am
only noting it here, not proposing a change, because the anchor cell is not an allowed mutable cell. No new
source row and no knowledge admission are proposed.

## Commands observed

`git rev-parse HEAD`; an inline literal regex scan over the 35 paths, on the working tree and at baseline
`git show b9b2479`; `rg -n S055` over `corpus/`; `curl` raw/API/tree fetches of the pinned commit; `sha256sum`;
and line-range reads with `sed`/`awk`. I did not run any build, test, linter, the lane `registry_check.py`, or
any upstream code. I installed no tools.

## Limitations

- I only opened `math_eval.py`, `drop_eval.py`, `mmlu_eval.py` and `common.py` at the pinned commit. I did not
  inventory the rest of the repository's extraction call sites, such as gpqa or mgsm.
- The citation result is literal reference coverage only (C2 contract). It is not semantic endorsement of the
  whole knowledge entry.
- This is author-side seat advice, not outside closure.

## Verdict

**PASS (scoped to S055).** The pinned source reopened, all three anchors are confirmed with located quotes, and
the narrow teaches and scope cells are supported. The single frozen citing file is covered by used-by and the
status is `mined`. No mutable-cell change is warranted. This is not a verdict on round 28, C1, C2 as a whole,
S038, or S056.
