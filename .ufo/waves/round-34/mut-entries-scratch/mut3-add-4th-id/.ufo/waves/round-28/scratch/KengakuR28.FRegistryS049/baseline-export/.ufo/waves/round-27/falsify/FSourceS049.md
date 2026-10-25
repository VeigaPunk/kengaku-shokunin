# FSourceS049 — S049 source reread

Identity: FSourceS049; independent source reread, **not** candidate writer KengakuR27.
Canonical candidate path: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/extraction-policy-comparison.md`. I read the whole draft at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (110 lines).

## Findings

- Local registry `corpus/SOURCES.md:71` pins S049 to `lm_eval/filters/extraction.py` at commit `d6de81643928d653435c431bae19945d41d32520`; it describes first/last regex-match selection, explicitly not JSON-extraction validity. The URL opened was the same full-SHA commit.
- Quote verified: `match = match[self.group_select]` is the exact S049 quote in both `corpus/evidence/round27-sources/gate.md:8` and `corpus/lessons/round-27.md:40`. It is 4 lexical tokens (well under the 25-word limit). Lesson scope at `corpus/lessons/round-27.md:51-52` expressly says S049 is an ordering precedent, not a JSON-policy port.
- Direct pinned-source reads succeeded (static `read`; process exit code N/A). In `lm_eval/filters/extraction.py`, `group_select: int = 0` is line 25; `findall` followed by `match[self.group_select]` is lines 46-48, with the quoted statement at line 48. The same commit's `lm_eval/tasks/gsm8k/gsm8k-cot.yaml:51-54` shows strict-match omitting the option (therefore default 0) and flexible-extract setting `group_select: -1`. This substantiates first/last selection among regex matches.
- Citation precision note: the draft source header (`.ufo/waves/round-27/drafts/extraction-policy-comparison.md:1`) and registry include `extraction.py:27`; line 27 is `) -> None:`, not the `group_select` declaration (line 25). The substantive quote range `:47-49` is correct and contains the selector at line 48, and the YAML corroborates the mapping. Replace `:27` with `:25` if that citation is intended to locate the option declaration; this is a weak/redundant anchor, not a contradiction of the claim.
- The corresponding candidate prose is at draft `:17-20`: S049 is said to expose first/last `group_select` over regex matches, then grouped with ordering/selection precedents and explicitly distinguished from faithful JSON-policy implementations. That mapping is accurate and bounded: the source is a generic regex filter/configuration, not a port of the lane's JSON, fence, fallback, or E0–E8 policies.

No build, test, lint, formatter, shell command, or install was run; this assignment used static source/file reads only. No installs or updates.

VERDICT: PASS — S049 supports the candidate's ordering-precedent claim and the ≤25-word quote is accurate; retain the explicit non-port caveat and tighten the non-substantive `:27` anchor to `:25` if it is meant to locate `group_select`.