# RowOpenCompassLast — round 27 (OpenCompass option-postprocess source)

Seat: KengakuR27.RowOpenCompassLast (leaf, read-only; no clone writes, no lane writes).
Date: access 2026-10-21.

## Source opened
- URL (blob): https://github.com/open-compass/opencompass/blob/ce6a506220f48f473217b1630cefde812acf16c6/opencompass/utils/text_postprocessors.py
- Raw fetched: https://raw.githubusercontent.com/open-compass/opencompass/ce6a506220f48f473217b1630cefde812acf16c6/opencompass/utils/text_postprocessors.py
- Pinned commit: ce6a506220f48f473217b1630cefde812acf16c6 (main HEAD via GitHub API, committer 2026-10-21T11:31:45Z, "[Dataset] Add LG-Bench dataset (#2690)").
- Saved bytes: /tmp/kengaku-r27-RowOpenCompassLast/text_postprocessors_ce6a506.py
  sha256 1a5cd455f5a4e435205098f877854d98ac027377df8b0124fb5cb9d02dce2317 (292 lines)
- Note: a main-branch fetch (/tmp/.../text_postprocessors.py) returned the same sha256; the pin is confirmed by identical bytes.

## Observed behavior (ground truth from the bytes)
- `first_option_postprocess` (:73-151): ordered list of ~45 regexes; `re.search` each in order; the first match wins. It returns the first option letter found inside the capture group (or whole match if group empty). Cushion patterns `([{options}]):` and `([{options}])` (:131-139) are appended only when `cushion=True`; the last one matches any option letter anywhere.
- `last_option_postprocess` (:162-166): `re.findall(rf'([{options}])', text)`; returns `match[-1]`. No word boundary, so any option letter inside any word counts.
- Defect (:92-93): line 92 `f'故选?\s*([{options}])'` lacks a trailing comma, so Python concatenates it with line 93 into one pattern; two intended patterns silently merge.
- Catch-all (:128): `1.\s?(.*?)$` captures arbitrary text; the option-letter loop then runs on it.

## SOURCES.md contract-v1 row (draft, 13 cells as the header; id left S0xx)
| S0xx | OpenCompass `opencompass/utils/text_postprocessors.py` at ce6a506 (OpenCompass text_postprocessors.py — https://github.com/open-compass/opencompass/blob/ce6a506220f48f473217b1630cefde812acf16c6/opencompass/utils/text_postprocessors.py) | source code | A | multiple-choice option-letter answer extraction only (first_option_postprocess, last_option_postprocess) at the pinned commit; not JSON-block extraction | :73-151 (first_option_postprocess, ordered regex priority + cushion), :162-166 (last_option_postprocess, findall[-1]) | first-match over an ordered priority list returns the first option letter inside the first matched capture; last-option policy takes the last option letter anywhere (no word boundary); a missing comma at :92-93 silently merges two patterns | queued | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |

Tier A is scoped to this row only: the code is the implementation's own behavior, not evidence that its extraction is correct.

## gate.md line (draft, for corpus/evidence/round27-sources/gate.md)
S0xx | https://github.com/open-compass/opencompass/blob/ce6a506220f48f473217b1630cefde812acf16c6/opencompass/utils/text_postprocessors.py | accessed 2026-10-21 | commit ce6a506220f48f473217b1630cefde812acf16c6 | text_postprocessors.py:74 (first_option_postprocess docstring) | quote: `"""Find first valid option for text."""`

Second located line if the gate needs a second quote: text_postprocessors.py:165 `return match[-1]` (last_option_postprocess).

## Policy mapping
NONE of E1–E8 is grounded by this source. E0–E8 (round-27-claims.md:37-45) are JSON-block extraction policies (fenced/bare/whole/decode-scan). This source is multiple-choice option-letter extraction. The closest conceptual analogue is first-match vs last-match ordering (E1/E3 vs E2/E0), but that is an analogy across domains, not support for any pre-registered policy. Using it to support E1–E8 would be a claim the source does not make.

## Installs / tools
- None. Used curl (existing), python3 stdlib, and the GitHub API via curl. No package installs, no pacman, no upgrades.

## Files written (sha256)
- /tmp/kengaku-r27-RowOpenCompassLast/text_postprocessors.py (main-branch fetch) sha256 1a5cd455f5a4e435205098f877854d98ac027377df8b0124fb5cb9d02dce2317
- /tmp/kengaku-r27-RowOpenCompassLast/text_postprocessors_ce6a506.py sha256 1a5cd455f5a4e435205098f877854d98ac027377df8b0124fb5cb9d02dce2317
- /tmp/kengaku-r27-RowOpenCompassLast/commit.json (GitHub API response; sha not computed, not cited)
- This report file (lane .ufo/waves/round-27/build/RowOpenCompassLast.md); sha256 of this file not computed, not cited.

## Out of scope / not done
- No edits to SOURCES.md, gate.md, grader, state_check, or plans (integration owner is KengakuR27 L1).
- No live model/endpoint requests. No verification run.

VERDICT: OpenCompass text_postprocessors.py at ce6a506 is pinned and opened, the S0xx row and gate line are drafted, and it grounds none of E1–E8 because it is MCQ option-letter extraction, not JSON-block extraction.
