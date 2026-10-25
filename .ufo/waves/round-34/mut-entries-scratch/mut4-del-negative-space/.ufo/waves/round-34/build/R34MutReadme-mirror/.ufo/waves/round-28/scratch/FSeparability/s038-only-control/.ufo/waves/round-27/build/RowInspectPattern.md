# Round 27 — RowInspectPattern (inspect_ai `pattern()` scorer, answer-extraction policy)

Axes: novelty (coverage of extraction policies E1–E8) + calibration (source scoped to what it shows).
Base: kengaku-shokunin 11a7fc8c64dc. Read-only seat; only this report written in the lane.

## Opened source (2026-10-21)
- Local install: inspect-ai 0.3.282, `src/inspect_ai/scorer/_pattern.py`, sha256 `7974ddb436917ac97f78304ae071eef75115783938358a0578f8d2e30abaae6b`.
- Upstream raw `main` (https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/src/inspect_ai/scorer/_pattern.py, HTTP 200): same sha256.
- PyPI sdist `inspect_ai-0.3.282.tar.gz` (sha256 `bf221c760f48fbaafdd01a99a2d5ffede9ff46cd97bad660ad0e91ddc34e98cd`, uploaded 2026-10-19): member `scorer/_pattern.py` same sha256.
- Last upstream commit touching the file (GitHub API commits?path=, newest first): c9f5dd050a46 (2026-09-23 "Tag empty completions with reason=no_response"), then 253d38f2 (2026-08-31, #4829 no-capture-group full-match fallback), 402290090a (2026-08-26, #4629).
- Scratch copies: /tmp/r27-rowpat/_pattern_0.3.282.py, _pattern_main.py (sha as above), sdist.tgz.

## Behavior read from source (path:line, _pattern.py)
- L77: `re.search(pattern, completion, ...)` — leftmost match only; no finditer, so a later restatement is never considered.
- L89: `groups = match.groups() or (match.group(0),)` — no capture groups → full match is the candidate.
- L96–98 (default match_all=False): `match_first` returns the first string group equal to a target entry (L28); L100–105: single-group miss sets `answer=groups[0]` but `value` stays INCORRECT (L110). Reporting fallback only, not a verdict fallback.
- L90–94 (match_all=True): every string group must match; unmatched optional groups are skipped; zero string groups → None (L50–51).
- L119–124: no regex hit → INCORRECT, `reason=invalid_response_format` (or `no_response` if empty, L86/L121). No second extraction is attempted.
- L14–16, L78: ignore_case (default True) applies to both the regex and the target comparison.
- L18 `match in target`: Target is `Sequence[str]` (_target.py:4); `in` is element-wise `==`, so the comparison is exact string equality, not substring.

## Located quotes (≤25 words)
- Docstring, _pattern.py:62–64: “If the pattern contains no capture groups, the full match is compared against the target.” (16 words)
- No-match comment, _pattern.py:117–118: “an instruction-following failure charged to the model under test (see #4567)” (12 words)

## (1) SOURCES.md draft row
Note: the file header and every existing row have **11** pipe cells (id … used-by), not 13 as the brief states; the draft follows the existing schema. Flagged for Main.

| S0xx | inspect_ai pattern() scorer source (UKGovernmentBEIS/inspect_ai v0.3.282, src/inspect_ai/scorer/_pattern.py) — https://github.com/UKGovernmentBEIS/inspect_ai/blob/main/src/inspect_ai/scorer/_pattern.py | source | A | the framework's regex answer-extraction code path (first regex hit, group selection, no-match verdict); what the scorer does, not whether first-match extraction is valid | _pattern.py:56–124 (pattern, match_first, match_all_groups); re.search L77; sha256 7974ddb4…aae6b; main raw and PyPI sdist identical | re.search keeps only the leftmost match; no capture groups → full match is the candidate; default match_all=False takes the first group equal to a target entry; no regex hit → INCORRECT invalid_response_format with no second extraction attempt; single-group miss reports groups[0] as answer without changing the verdict | queued | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |

## (2) gate.md line (draft; not written to corpus/evidence — no round-27 gate file exists yet)
| S0xx | https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/src/inspect_ai/scorer/_pattern.py (= PyPI inspect-ai 0.3.282 sdist member; last upstream touch c9f5dd050a46, 2026-09-23) | src/inspect_ai/scorer/_pattern.py:62–64, pattern() docstring | “If the pattern contains no capture groups, the full match is compared against the target.” | access 2026-10-21; HTTP 200; sha256 7974ddb436917ac97f78304ae071eef75115783938358a0578f8d2e30abaae6b |

## (3) Policy grounding
- **E3 bare-first** (ignore fences; first parseable candidate): closest structural match — framework takes the first regex hit over the whole completion, fence-agnostic. Grounds the *first-occurrence* choice only as a framework precedent for regex extraction, not for JSON.
- **E5 fence-only** (no bare fallback): secondary, for the no-fallback-on-miss behavior (L119–124). Scope carefully: L100–105 `groups[0]` fallback is reporting-only.
- **E1 first-fence**: not grounded — the source has no fence concept; it is first-match but fence-specific policy is not addressed.
- **E0, E2, E8 (last-occurrence)**: not grounded; this source documents only leftmost-match semantics.
- **E4, E6, E7**: none.
- Limits: the source documents what pattern() does; it is not evidence that any policy is correct against the frozen 1964-response population. No lane file edited; no E-policy verdict changed by this row.

## Installs / tools
- `uv run --no-project --with inspect-ai` using uv 0.13.0 (already present); inspect-ai 0.3.282 resolved into the uv cache (python 3.13). No system-wide install, no pacman, no service change. Channel: PyPI via uv. Reason: read the exact upstream source bytes.
- curl fetches: GitHub raw, GitHub API (commits), PyPI JSON, files.pythonhosted.org sdist.

## Findings / conflicts
- Schema mismatch: brief says 13 cells; SOURCES.md header and rows carry 11. Draft uses 11 — Main to confirm.
- used-by `corpus/lessons/round-27.md` does not exist yet in the lane (lessons dir has round-26 and earlier only).

VERDICT: pattern() source opened and hashed (3 identical copies); draft row S0xx (11-cell schema, flagged), gate quote located at _pattern.py:62–64, grounds E3 (primary) and E5 (secondary) only.
