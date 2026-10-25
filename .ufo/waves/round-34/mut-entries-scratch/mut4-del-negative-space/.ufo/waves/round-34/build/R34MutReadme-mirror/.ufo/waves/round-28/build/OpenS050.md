# OpenS050 — reopen S050 and check its literal-reference coverage (round 28, C2)

Writer/seat: `KengakuR28.OpenS050-2` (read-only scout, author-side advice — not outside closure).
Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. No registry, knowledge, or production edits were made.
Scratch evidence: `.ufo/waves/round-28/scratch/OpenS050/` (`_pattern.py`, `_common.py`, `whl_pattern.py`, `whl_common.py`, `pypi.json`).

## Verdict

**PARTIAL**, scoped to S050 only.
- The source opens at its pinned commit, and the row's three anchors are located exactly. The narrow first-hit/no-fallback teaching holds.
- The row's unqualified "no hit is invalid_response_format" is inaccurate for empty or whitespace-only completions. S058 already supersedes it, so this is a known, disclosed defect and not a new discovery. Immutable cells stay as written.
- C2 finding: S050 is cited literally in one frozen knowledge file that its `used-by` does not list. One allowed-cell repair is proposed below.

## Row under check (unchanged at baseline b9b2479 and the current tree)

`corpus/SOURCES.md:72`:
`| S050 | inspect_ai pattern() — https://github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py | code | A | … | pattern() :62–64, :77–79, :119–124; source agrees with PyPI 0.3.282 | … | mined | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |`

`git diff --stat b9b2479 -- corpus/SOURCES.md corpus/knowledge/extraction-policy-comparison.md` is empty, so the row and the citing file are identical at baseline and in the current tree.

## Opening record

- URL (fetched as raw data): https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py. This is the same blob as the row's GitHub URL.
- Access date: 2026-10-21. File is 126 lines, sha256 `7974ddb436917ac97f78304ae071eef75115783938358a0578f8d2e30abaae6b`.
- Commit identity (GitHub API): `63e45cc52d39b873b944124613da21fdad6f6dcc`, committed 2026-10-21T11:24:54Z, titled "fix: share tool-execution classification between model and human agent paths (#4993)".
- Located quotes (each 25 words or fewer):
  - :62–64 (docstring): "If the pattern contains no capture groups, the full match is compared against the target."
  - :77–79: `match = re.search(pattern, state.output.completion, re.IGNORECASE if ignore_case else 0)`
  - :119–124, no-match branch: `return Score(value=INCORRECT, reason="no_response" if empty else "invalid_response_format", …` (the reason is on :121).
  - :86: `empty = no_response(state.output.completion or "")`. `_common.py:17–30` defines `no_response` as `return not completion.strip()` (sha256 `49460816…211b`).
- Scope: only scorer `pattern()` semantics at this commit. This says nothing about the lane's JSON policies or fence grammar.

### PyPI agreement (anchor clause "source agrees with PyPI 0.3.282")

- https://pypi.org/pypi/inspect-ai/0.3.282/json lists wheel `inspect_ai-0.3.282-py3-none-any.whl`, sha256 `0a074a75015eeecd8d7779511037dfad27eb4f9252ab4a22fc6aebda59bb9413`, uploaded 2026-10-19T21:37:31. The downloaded wheel matched that digest (`sha256sum -c` OK).
- The wheel members `inspect_ai/scorer/_pattern.py` and `_common.py` are byte-identical to the pinned-commit files (`diff` empty, same sha256).
- Limitation: the pinned commit is dated about 38 hours after the 0.3.282 upload. "Agrees" therefore means these two files are byte-identical. It does not mean the commit is the release tag.

## Claim-by-claim check

| Row claim | Observed | Status |
|---|---|---|
| `re.search` takes the leftmost hit | :77–79 is a single `re.search`. There is no second search and no `findall`/`finditer` fallback. | Confirmed (ordering and no-fallback precedent). |
| "first-regex-hit" | With several capture groups and `match_all=False`, `match_first` (:21–31) returns the first group that *equals a target*, not just the first group. With one group, a non-matching capture is still returned as `answer` (:100–105). | Confirmed for which match is chosen. The group-selection detail is extra and does not change the narrow teaching. |
| No-capture-group full match | :62–64 docstring; :89 `match.groups() or (match.group(0),)` | Confirmed. |
| "no hit is invalid_response_format" | :121 gives `no_response` when the completion is empty or whitespace-only, and `invalid_response_format` otherwise. Also, :112 gives `no_response` on the *match* branch for empty completions when the pattern is nullable. | **Inaccurate as written.** Already superseded by S058 (`SOURCES.md:80`; round-27 M60). The match-branch :112 case is extra detail that neither row states; it does not touch the narrow precedent. |
| "not the lane's fence grammar" / "not JSON-policy accuracy" | The scorer has no JSON or fence handling. | Scope disclaimer is appropriate. |

The immutable cells (source, kind, tier, scope, anchor, teaches, opened) must not be rewritten. The correction lives in S058, which is the existing pattern.

## C2 literal-reference coverage for S050

Method: Python stdlib applied the population's `reference_pattern` `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` to all 35 `knowledge_paths` in `plans/fixtures/r28/registry/population.json`. No checker or production script was run.

- citing_files: `corpus/knowledge/extraction-policy-comparison.md:18`, the text "inspect_ai `pattern()` (S058, correcting S050) takes a first regex hit; …". This line is the same at baseline b9b2479.
- used_by: `corpus/lessons/round-27.md`
- missing_used_by: `corpus/knowledge/extraction-policy-comparison.md`
- status: `mined`, which is valid for a cited row (not queued).
- Prior-round context: round-27 (`corpus/lessons/round-27.md:159`, `:203`) deliberately kept S050 "lesson-only as a superseded reason". Under the round-28 literal contract, historical and corrective mentions count (`round-28-claims.md` C2 interface; population `note`). So that disposition is a missing_used_by under C2. Listing the path is literal coverage, not endorsement; the citing sentence itself says "correcting S050".

### Suggested allowed mutable-cell change (only after this opening; L1 decides and applies)

- **used-by**: `corpus/lessons/round-27.md` → `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`
- **status**: keep `mined` (no change).
- **recheck**: no change needed (2027-01-19). Optional refresh only if L1 policy ties recheck to a reopen.
- Log it old→new in the round-28 lesson, as round-25 `:36` did for S011.
- Do not change immutable cells, and do not edit the knowledge prose to drop "correcting S050". Editing the prose would change frozen-population content instead of the registry.

## Out of scope for this seat

The S056 (own-work receipt) and S038 (DOI/publisher full text) instructions were not attempted. They belong to other seats (for example `KengakuR28.OpenS038-2`), and this seat claims no opening for them.

## Commands and tools observed

`rg`, `sed`, `git show/diff/log` (read-only), `curl` (GitHub raw, GitHub API, PyPI JSON, the PyPI wheel), `sha256sum`, `diff`, and Python stdlib (`json`, `re`, `zipfile`) to parse the population and read the wheel as data. No upstream code was imported or executed, no benchmark site was contacted, and nothing was installed or updated (`RULES.md` install gate not triggered). The temporary wheel was deleted after extraction.

## Limitations

- The check covers literal references only, not semantic citation support. It does not cover S050 uses outside the 35 frozen paths. Lesson used-by entries are allowed extras and were not audited.
- The PyPI agreement covers only the two files compared.
- Reported as author-side advice. The repair counts only after the delivered `registry_check.py` fails on baseline and passes with the allowed-cell delta.
