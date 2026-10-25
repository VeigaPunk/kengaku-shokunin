# RowCommonMarkFence — CommonMark fenced-code source opening (round 27, build)

Access date 2026-10-21. Seat: KengakuR27.RowCommonMarkFence (leaf, read-only; no clone writes, no lane writes).

## 1. Opened source

- Current version resolves: `https://spec.commonmark.org/current/` → 302 to `//spec.commonmark.org/0.31.2/` (fetched 2026-10-21; the reader returned the redirect stub, so the bytes were fetched with curl).
- Saved: `/tmp/kengaku-r27-CommonMark/spec-0.31.2.html`, 514698 bytes, sha256 `c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d`.
- Version 0.31.2 dated 2024-01-28 (index page, same host).
- Section: §4.5 Fenced code blocks, anchor `#fenced-code-blocks`.

## 2. Draft SOURCES row (for lane integration; id left as S0xx)

Flag: the registry header at `corpus/SOURCES.md:21` has **11** columns, not 13, and every existing row has 11 cells. The draft therefore uses the 11-column header as it actually exists. Integrator should confirm the contract count before merging.

```
| S0xx | CommonMark Spec 0.31.2, §4.5 Fenced code blocks — https://spec.commonmark.org/0.31.2/#fenced-code-blocks | spec | A | fenced-block boundaries (opening fence, info string, closing fence) as CommonMark defines them; no answer-extraction policy | §4.5 Fenced code blocks, spec-0.31.2 HTML :2726-2765, :3193-3194, :3285 | a closing fence must use the same character and be at least as long as the opening fence; closing fences carry no info string; the first info-string word is typically the language but is not mandated | queued | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |
```

## 3. gate.md line (for `corpus/evidence/round27-sources/gate.md`)

```
| S0xx | https://spec.commonmark.org/0.31.2/#fenced-code-blocks | access 2026-10-21; CommonMark 0.31.2 (2024-01-28); fetched via curl, sha256 c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d | §4.5 Fenced code blocks, spec HTML line 3194 (section text after Example 142) | “the first word is typically used to specify the language of the code block.” | build receipt: this file; verified by python normalization of tags/entities, match at line 3194 |
```

Supporting quotes, all verified in the same saved file:
- line 2742: "closing code fence of the same type as the code block began with" (13 words), supports the closing-length and closing-character rule.
- line 3285: "Closing code fences cannot have info strings" (7 words), with Example 147.

## 4. Policy grounding

- **None** of E1–E8 is grounded as an extraction-policy choice. CommonMark defines rendering, not answer extraction; it does not say which block a harness should pick.
- **Boundary note (not a policy grounding):** E0, E1, E5 and E6 all assume a "fenced block" is the lane regex span, not the CommonMark block. Two spec-level divergences, observed in the lane code:
  - `grader.py:122` and `plans/grader_perturb.py:35` use `` ```(?:json)?\s*\n(.*?)``` `` (re.S). The regex closes at any triple backtick, not only a same-character fence at least as long as the opening. Content with a 4-backtick fence, or a literal ``` inside a block, is cut short by the regex and would be parsed differently under CommonMark.
  - E6's label class `[A-Za-z0-9_+-]*` is narrower than CommonMark's info string, which is any trimmed text. A fence such as ```` ```json title="x" ```` is a valid CommonMark block but not matched by E6's pattern.
- These are candidate facts for the lead's ruling on E1/E5/E6 fence semantics. I did not alter any frozen policy text.

## 5. Findings with locations

- F1 `corpus/SOURCES.md:21`: header is 11 columns; the task requested 13. Existing rows match 11 (checked `S001` row, line 23).
- F2 `grader.py:122`: lane fence regex, closing rule diverges from spec §4.5 (see §4).
- F3 `plans/grader_perturb.py:35`: `FENCED_RE` identical in shape to F2.
- F4 spec §4.5 line 2736: info string trimmed of leading and trailing spaces or tabs. The regex in E6 does not model trimming beyond `[ \t]*`.

## 6. Installs

None. Used `curl` (system binary) and python3 stdlib to fetch and normalize the spec. No pacman, no uv, no npm.

## 7. Files written

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/build/RowCommonMarkFence.md` (this report; sha256 not computed by this seat; integrator may hash it).
- `/tmp/kengaku-r27-CommonMark/spec-0.31.2.html` (scratch, source copy).

VERDICT: CommonMark 0.31.2 §4.5 opened and saved (sha256 c85f56cc…); draft row and gate line provided, grounds no E1–E8 policy but flags two fence-boundary divergences in the lane regex for the E1/E5/E6 ruling; SOURCES header is 11 columns, not 13.
