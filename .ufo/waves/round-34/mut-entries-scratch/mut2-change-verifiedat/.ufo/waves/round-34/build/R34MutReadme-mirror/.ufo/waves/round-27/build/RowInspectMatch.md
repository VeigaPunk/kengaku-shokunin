# RowInspectMatch — round 27 (leaf, read-only; scratch in /tmp/r27-rim)

Scope: inspect_ai `match()` `location` parameter (begin/end/any/exact) → draft SOURCES row, gate line, E1–E8 mapping.

## Sources opened (access 2026-10-21)
- Main-branch raw read: https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/src/inspect_ai/scorer/_match.py (not byte-compared to the pin).
- Pinned: PyPI inspect-ai 0.3.282 wheel (uploaded 2026-10-19T21:37:31Z), sha256 0a074a75015eeecd8d7779511037dfad27eb4f9252ab4a22fc6aebda59bb9413 (= PyPI digest; /tmp/r27-rim/inspect_ai-0.3.282-py3-none-any.whl).
- Extracted, sha256: scorer/_match.py 46519227cf244e0904d77d8484b3b91fa95fd61948fa0ae9e5910c1536db94f7; scorer/_common.py 49460816379d5cbbf48d1090ab854b243a83b652fb711f2c849dc1ff2292211b (both in /tmp/r27-rim/).
- Tag URL .../blob/v0.3.282/... → HTTP 404 (no tag found); git commit NOT determined. Version + wheel digest is the pin.
- Docs: https://inspect.aisi.org.uk/scorers.html (.md form; unversioned page).

## Source facts (wheel 0.3.282)
- _match.py:10 `location: Literal["begin", "end", "any", "exact"] = "end"` — default is end.
- _match.py:18-20 docstring: "any" matches anywhere; "exact" requires the output be exactly equal to the target.
- _common.py:70-116 match_str numeric path (numeric=True): first/last number of whitespace-split words for begin/end (:99-104).
- _common.py:121-128 text path, after strip_punctuation (ignore_punctuation default True; _util/text.py `strip(whitespace+punctuation)`, ends only): begin → startswith (:121-122); end → endswith (:123-124); exact → == (:125-126); else (any) → `t in v` (:127-128).

## Executed (scratch venv: `uv venv` + `uv pip install inspect-ai==0.3.282`, PyPI via uv; calls match_str from the pinned package)
- end, 'The answer is 142' vs '42' → True (suffix false positive)
- end, '142' vs '42' → True
- end, '42 is the answer' vs '42' → False
- end, 'The answer is 42.' vs '42' → True
- exact, 'the answer is 42' vs '42' → False
- any, 'x 42 y' vs '42' → True
- begin, '42 apples' vs '42' → True
- numeric=True, end: 'The answer is 142' vs '42' → False; 'The answer is 42' vs '42' → True

## (1) Draft SOURCES row
File header and every existing row have 11 cells (not 13 as claims text says); followed the file. Id left as S0xx.

| S0xx | inspect_ai `match()` scorer, `location` parameter (begin/end/any/exact) — https://github.com/UKGovernmentBEIS/inspect_ai/blob/main/src/inspect_ai/scorer/_match.py (pinned PyPI wheel 0.3.282, sha256 0a074a75…bb9413; docs https://inspect.aisi.org.uk/scorers.html) | tool | A | the harness's own positional text-match rule for `location` as shipped in 0.3.282; not a first/last-match, fence, or JSON extractor | _match.py:10, :18-20; _common.py:121-128 text branch; opened 2026-10-21 | `location` is a whole-output position test on punctuation-stripped text (end = endswith, begin = startswith, exact = equality, any = substring), so non-numeric end accepts "142" for target "42"; numeric=True is the only location-sensitive extraction and grounds no E1–E8 policy | queued | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |

## (2) gate.md lines (draft only; corpus/evidence/round27-sources/ does not exist at base — lane integrator creates it)
S0xx | accessed 2026-10-21 | https://github.com/UKGovernmentBEIS/inspect_ai/blob/main/src/inspect_ai/scorer/_match.py ; pinned wheel inspect_ai-0.3.282 sha256 0a074a75015eeecd8d7779511037dfad27eb4f9252ab4a22fc6aebda59bb9413 | version 0.3.282, _match.py:19-20 (extracted sha256 46519227cf244e0904d77d8484b3b91fa95fd61948fa0ae9e5910c1536db94f7) | quote: "exact" requires the output be exactly equal to the target
S0xx (second, docs) | accessed 2026-10-21 | https://inspect.aisi.org.uk/scorers.html (match() entry, Overview) | unversioned page | quote: Check whether the `target` appears at a known position: `begin`, `end` (the default), or `any`.

## (3) Policy mapping: NONE
E1–E8 are JSON-extraction policies over fenced/bare candidates. match() performs no JSON, fence, or bare-candidate extraction; its only extraction is numeric first/last-number on word tokens. Its `exact` is kin to E4 by kind only; the row must not be cited as grounding E4 semantics. The suffix false positive above is a text-position behaviour outside the frozen E0–E8 table: recorded as a candidate for the lead, not added as a policy (that would be an amendment).

## Installs / tools
- uv venv /tmp/r27-rim/venv + `uv pip install inspect-ai==0.3.282` (PyPI via uv; scratch only; reason: execute match_str from the pinned source). No system, pacman, or host changes.

## Files written
- .ufo/waves/round-27/build/RowInspectMatch.md (this report; absolute path /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/build/RowInspectMatch.md).
- No lane-tree, SOURCES.md, or gate.md writes. Scratch only in /tmp/r27-rim (pypi.json, wheel, _match.py, _common.py, _match_tag.py = 404 body, venv).

VERDICT: match() row and gate quote drafted from the pinned 0.3.282 source and executed; grounds no E1–E8 policy; file uses 11 cells, not 13; suffix false-positive recorded as a lead for the integrator.
