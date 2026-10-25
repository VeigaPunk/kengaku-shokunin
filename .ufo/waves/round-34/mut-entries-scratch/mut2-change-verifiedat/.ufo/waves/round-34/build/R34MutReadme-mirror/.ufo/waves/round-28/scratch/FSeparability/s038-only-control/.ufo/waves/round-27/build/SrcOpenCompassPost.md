# SrcOpenCompassPost — round 27 (OpenCompass text_postprocessors: first vs last; json/fence)

Seat: KengakuR27.SrcOpenCompassPost (leaf scout, read-only; no clone, no lane writes). Access date: 2026-10-21.

## Source + commit
- File: `opencompass/utils/text_postprocessors.py` @ `a78a5f283c628f39ca4a6ba32a140e1deb486099` — the most recent commit touching it (2026-10-13, PR #2018 MaritimeBench; GitHub API `commits?path=...` row 1).
- URL: https://github.com/open-compass/OpenCompass/blob/a78a5f283c628f39ca4a6ba32a140e1deb486099/opencompass/utils/text_postprocessors.py
- `curl -sL https://codeload.github.com/open-compass/OpenCompass/tar.gz/a78a5f2...` + `tar -xzf` → `/tmp/oc-r27` (exit 0, EXTRACT_OK).
- `sha256sum` → `1a5cd455f5a4e435205098f877854d98ac027377df8b0124fb5cb9d02dce2317` (292 lines) — byte-identical to sibling RowOpenCompassLast's main-HEAD pin `ce6a506220f48f473217b1630cefde812acf16c6` (2026-10-21, PR #2690); all path:lines below hold at both commits.

## First-match family
- :73-151 `first_option_postprocess` — ordered pattern list :77-129; cushion patterns `([{options}]):` and `([{options}])` at :130-133, appended at :138-139; selection loop :140-150: `match = re.search(pattern, text, re.DOTALL)` (:142) — first pattern in list order wins; inside a match the first option char found in the capture returns (:148-150). Docstring :74: `"""Find first valid option for text."""`
- Defect (verified bytes via `sed -n '88,95p'`): :92 `f'故选?\s*([{options}])'` has no trailing comma, so Python concatenates it with :93 (`f'只有选?项?\s?([{options}])\s?是?对',`) — one intended pattern silently unreachable.
- Catch-all :128 `f'1.\s?(.*?)$'` captures arbitrary text; the option-char loop then scavenges it.
- :46-51 `first_capital_postprocess` (first uppercase char); :155-159 `first_capital_postprocess_multi` (re.search first `[A-D]+` run); :169-178 `first_number_postprocess` — docstring :170 `"""Return the first number in a string."""`, re.search first number; :62-69 `think_pred_postprocess` (re.search, first capture); :242-245 `match_answer_pattern` (re.search, caller-supplied pattern, first capture).

## Last-match family
- :162-166 `last_option_postprocess`: `match = re.findall(rf'([{options}])', text)` (:163); `return match[-1]` (:165). No word boundary — last option char anywhere, even inside words.
- :54-58 `last_capital_postprocess` (iterates `text[::-1]`).
- :188-212 `xml_tag_postprocessor` (registry `'specific-xml-tag'`): findall `{tag}(.*?)</{tag[1:-1]}>` re.DOTALL; :206 `# Only keep the last one`; :207 `output = matches[-1].strip(...)`. Delimiter-parameterized, keeps LAST span.
- :279-280 `extract_non_reasoning_content` (registry `'extract-non-reasoning-content'`): `return text.split(think_end_token)[-1].strip()` — last span after the end delimiter.
- :289-292 `parse_bracketed_answer`: first-match `re.search(rf'<({options})>', text)` (single-tag, first).

## json / fence extraction: verified negative
- `grep '```' /tmp/oc-r27/opencompass/utils` → No matches found; `grep 'fence|backtick|`{3}|json_block|parse_json'` same tree → No matches found.
- No `json.loads`/`JSONDecoder` anywhere in text_postprocessors.py; repo-wide grep shows json.loads only in dataset loaders/format checkers (e.g. `datasets/IFEval/instructions.py:918`, `datasets/PMMEval/mgsm.py:45`) — the core extraction layer has NO JSON-block or fence-aware policy.

## Mapping to round-27 E-policies (plans/round-27-claims.md:33-45)
- First-vs-last ships as named, user-selectable registry entries (`'first-capital'` :45 / `'last-capital'` :53) plus the first_option/last_option pair: public-tooling precedent that extraction policy is an explicit knob — the claims' prior-art expectation, in kind.
- `first_option_postprocess` (priority list + cushion fallback) ≈ E1/E3 first-match axis; `last_option_postprocess` / `xml_tag_postprocessor` / `split[-1]` ≈ E0/E2/E5/E8 last-match axis. `xml_tag_postprocessor` is the closest fence analogue: delimiter-bounded span with the delimiter as a parameter (E6 any-label analogy).
- No analogue for E4 strict-whole (nothing requires the whole output to parse) and E7/E8 raw_decode scans (no JSONDecoder in the extraction layer).
- No agreement/verdict-counting code in this file — no cross-policy verdict-agreement measurement here; consistent with "novelty held at 7" (measurement construct remains the lane's own).
- Caveat (agrees with sibling RowOpenCompassLast): these are option-letter/tag-span policies, not JSON extraction; they support the ordering axis as prior art, they do not ground any E0-E8 semantics directly.

## Quotes (≤25 words each; URL above; accessed 2026-10-21)
- :74 `"""Find first valid option for text."""` · :165 `return match[-1]` · :206 `# Only keep the last one` · :170 `"""Return the first number in a string."""`

## Tools / installs
- None installed. Used existing curl, tar, grep, sed, sha256sum; public GitHub raw + API only. No pacman, no services.

VERDICT: OpenCompass a78a5f2 (byte-identical at main ce6a506) implements first-vs-last option/tag extraction (:73-151, :162-166, :206-207, :279-280) but no json/fence extraction — it grounds the first/last ordering axis (E1/E3 vs E0/E2/E5/E8) as published-in-kind, grounds no E4/E7/E8, and carries a silent regex-concat defect at :92-93.
