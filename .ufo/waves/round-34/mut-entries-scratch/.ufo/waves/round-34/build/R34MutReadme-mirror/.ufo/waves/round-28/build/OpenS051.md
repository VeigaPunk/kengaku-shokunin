# OpenS051 — reopen S051 (openai/evals JsonMatch), round 28 C2 source-use check

Writer/seat: `KengakuR28.OpenS051-2` (read-only scout, leaf, author-side advice — not outside closure).
Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; lane HEAD observed `f0ba09be0f3066daba2134b943d973ad1588f34a`.
Writes: this report plus scratch copies under `.ufo/waves/round-28/scratch/OpenS051/` only. Registry not edited.
Tools installed/updated: none.

## Scope

Only S051. The assignment's S056 (own-work) and S038 (DOI) clauses belong to other seats' targets and are not
addressed here. This is literal-reference completeness plus a source reopening for one row, not semantic citation
support for the whole knowledge entry.

## Row under test (unchanged between baseline and current tree)

`corpus/SOURCES.md:73` at both `b9b24796…` (via `git show`) and the working tree, byte-identical:

| S051 | openai/evals JsonMatch — https://github.com/openai/evals/blob/main/evals/elsuite/basic/json_match.py | code | A | whole-completion JSON parsing in this harness | eval_sample :76, :80–83; last file change 4b7a66bd; source hash in round27-sources/gate.md | json.loads consumes the whole sampled completion and decode failure cannot match; E4 is the same policy class with a disclosed Unicode strip difference | mined | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md |

## Opening (observed 2026-10-21)

- URL opened: https://raw.githubusercontent.com/openai/evals/main/evals/elsuite/basic/json_match.py (HTTP 200),
  the raw form of the row URL. Access date 2026-10-21.
- SHA-256 `6cc971f9a360a89b628595f1de5b030bd38969f2160cca75bcf11ee7aa0795e8`, 106 lines. That equals the hash
  recorded in `corpus/evidence/round27-sources/gate.md:10`.
- GitHub API `commits?path=evals/elsuite/basic/json_match.py` returns exactly one commit:
  `4b7a66bd45f06156656e021e170e7574f6cde3f5` (2023-10-27, "Added Icelandic inflection eval; JsonMatch eval
  function (#1387)"). The raw blob at that commit and at current `main` = `8eac7a7de5215c907fbddc30efdaf316913eccdd`
  (2026-04-14) both hash to the same value (`cmp` identical). The row's "last file change 4b7a66bd" holds.
- Located quote (12 words), `eval_sample` line 82:
  “If the sampled string is not valid JSON, it will never match”
- Supporting lines, read directly:
  - :76 `sampled = result.get_completions()[0]`. The whole first completion is taken.
  - :80 `sampled_json = json.loads(sampled)`. The whole string is parsed, with no slicing, fence or regex extraction.
  - :81–83 `except ValueError:` → comment → `sampled_json = None`.
  - :15–17 `json_match`: `if sampled_json is None or correct_json is None: return False`. This is the mechanism that
    makes a decode failure unable to match. The row anchor cites the :80–83 assignment, not this line.
- Scratch copies: `.ufo/waves/round-28/scratch/OpenS051/json_match.{main,4b7a66bd,pinnedmain}.py`, `commits.json`,
  `main.json`. These were fetched as data only and never imported or executed.

## Teaches/anchor/scope verdict

- The scope "whole-completion JSON parsing in this harness" is confirmed and narrow enough. Lines :76 and :80 show
  that the whole sampled completion goes into `json.loads`.
- The anchor `eval_sample :76, :80–83` is confirmed line-exact. The gate's quote is at :82.
- The teaches clause "json.loads consumes the whole sampled completion and decode failure cannot match" is confirmed.
- The teaches clause "E4 is the same policy class with a disclosed Unicode strip difference" is confirmed for the
  disclosed difference. `plans/parser_policy_compare.py:87–88` `e4_strict_whole` runs `_loads(raw.strip())`. A
  stdlib-only check (Python 3.14.8, no upstream code) showed that `json.loads` rejects `'\x0c{"a":1}\x0c'` and
  `'\xa0{"a":1}'` but accepts JSON whitespace `' \n{"a":1}\t'`. So `str.strip()` is broader, as
  `extraction-policy-comparison.md:51` discloses. The same file reports that source-exact `json.loads(raw)` showed
  no difference on the pinned population.
- One additional difference is not stated in the row: exception breadth. Upstream catches only `ValueError` (:81).
  E4's `_loads` (`parser_policy_compare.py:41–45`) catches every `Exception`. As a result, a non-`ValueError`
  failure such as `RecursionError` on deeply nested input would propagate upstream but become `None` in E4.
  [INFERENCE] This does not change "same policy class". Given the knowledge file's no-difference replay, it is
  unlikely to affect the pinned population. The row's word "disclosed" is accurate for what is disclosed but not
  exhaustive. Teaches is an immutable cell, so this is a disclosure note for the lesson, not a cell change.
- Also observed and consistent with the row: a valid JSON `null` completion also decodes to `None` and can never
  match (:15). E4 likewise returns `None` for `null` (`extraction-policy-comparison.md:48`).

## Literal citations in the frozen 35-file population

Method: applied the persisted `reference_pattern` `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` line by line to all
35 `knowledge_paths` in `plans/fixtures/r28/registry/population.json`, both in the working tree and at baseline
`b9b24796…` via `git show`. All 35 files are present. S051 hits are identical in both trees:

- `corpus/knowledge/extraction-policy-comparison.md:1` (the `source:` header, `S051 openai/evals …json_match.py:76–83`)
- `corpus/knowledge/extraction-policy-comparison.md:21` (“openai/evals JsonMatch (S051) parses the whole completion;”)

The citing set is `{corpus/knowledge/extraction-policy-comparison.md}`, one file with two mentions.
Outside the population, the lesson references are `corpus/lessons/round-27.md:44,57,201` and the evidence is
`corpus/evidence/round27-sources/gate.md:10,20`.

Comparison with the registry under the C2 contract (cited ⇒ `mined` and used-by lists every citing frozen path):

- The status is `mined`, which satisfies the contract.
- used-by is `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`. It covers the only
  citing frozen path, so `missing_used_by` is ∅. The extra lesson path is permitted by the contract.
- No duplicate S051 row exists, because only one registry line matches `^\| S051`.
- The used-by history matches `corpus/lessons/round-27.md:201–202` (lesson-only → lesson + knowledge, with
  status/recheck unchanged).
- The recheck value 2027-01-19 equals opened 2026-10-21 plus 90 days, which is consistent with the entry's `recheck: 90d`.

## Suggested mutable-cell changes (status / recheck / used-by only)

None required. S051 is already clean under the C2 literal contract. The reopening found no drift: the hash, the
single-commit history and the line anchors all reproduce.
[OPTIONAL, not required by C2] If L1 treats this reopening as a recheck, the only allowed-cell move would be to
recompute recheck from the reopening date. That date is the same day (2026-10-21), so it yields the identical
2027-01-19. No change is therefore recommended. Immutable cells (source, kind, tier, scope, anchor, teaches, opened)
stay as they are. The exception-breadth note above belongs in round-28 lesson prose if L1 wants it, not in the row.

## Commands observed

- `rg`/`git show b9b24796…:<path>` with the persisted regex over the 35 paths (baseline and current tree).
- `curl` raw `main`, raw `4b7a66bd`, raw `8eac7a7d`; `sha256sum`; `cmp`; GitHub REST `commits?path=…` and `commits/main`.
- A stdlib `python3 -c` probe of `json.loads` whitespace, NaN and null behavior. No upstream or lane code was executed.

## Limitations

- I reopened GitHub's raw file and API metadata, not a signed release. The `main` URL is a moving target, and the
  current identity is pinned here by the hash and commit SHAs above.
- The literal-mention check does not evaluate whether the knowledge entry's other S051-adjacent claims, such as the
  E4 replay result, are semantically supported. I read that replay claim but did not rerun it.
- No benchmark sites were contacted. No REA MCP was used.

## Verdict

**PASS, scoped to S051 only.** The source reopened at the recorded hash and commit, and the scope, anchor and
teaches cells are confirmed line-exact. The only literal frozen-population citer is listed in used-by and the status
is `mined`. No allowed-cell change is needed. One advisory: the exception-breadth difference between upstream
`ValueError` and E4's `Exception` is not covered by "disclosed Unicode strip difference" and could be noted in the
round-28 lesson. This is not a blanket round-28 PASS.
