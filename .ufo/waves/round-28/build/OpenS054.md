# OpenS054 — round-28 C2 source reopen (author-side)

Writer/seat: KengakuR28.OpenS054-2 (read-only scout; author-side advice, not outside non-author closure).
Lane tree: jj working copy on top of f0ba09be0f3066daba2134b943d973ad1588f34a (baseline b9b24796277020d1b9b01923b45313d6a565e664).
`corpus/SOURCES.md` and `corpus/knowledge/extraction-policy-comparison.md` are byte-unchanged since the baseline (`git diff --quiet b9b2479 -- …` exit 0).
Writes: this report plus scratch `.ufo/waves/round-28/scratch/OpenS054/{commonmark-0.31.2.html,s4.5.txt}`. I edited no registry, knowledge, or production file. I installed no tools.

## Scope of this seat

The ID is S054 only. The template's S056 (own-work) and S038 (DOI) clauses belong to the sibling seats `OpenS056` and `OpenS038`, which are listed in `.ufo/waves/round-28/build-assignments.json`. I did not open those sources here and make no claim about them.

## Row under check (SOURCES.md:76, identical at baseline)

`| S054 | CommonMark 0.31.2 fenced blocks — https://spec.commonmark.org/0.31.2/#fenced-code-blocks | spec | A | code-fence rendering grammar, not answer selection | §4.5 Fenced code blocks; examples on closing fences | closing fences have no info strings and must match opening type/length; the lane's regexes are deliberately narrower/different, not CommonMark parsers | mined | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md |`

## Source opening

- URL: https://spec.commonmark.org/0.31.2/ (anchor `#fenced-code-blocks`, `<h2 id="fenced-code-blocks">` at HTML line 2726).
- Access: 2026-10-21T13:57:14Z, `curl -sS -L`, HTTP 200, 514698 bytes.
- Version banner: `Version 0.31.2 (2024-01-28)` (HTML line 117).
- SHA-256 `c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d`. This equals the round-27 gate hash for S054 in `corpus/evidence/round27-sources/gate.md:13`, so the pinned spec bytes have not drifted.
- Located quotes (§4.5, tag-stripped text in `scratch/OpenS054/s4.5.txt`):
  1. “Closing code fences cannot have info strings” — lead-in sentence to Example 147, the last example in §4.5. This matches the round-27 quote.
  2. “until a closing code fence of the same type as the code block began with (backticks or tildes), and with at least as many backticks or tildes as the opening code fence” — §4.5 definitional paragraph. This passage is 25 words.
  3. “The closing code fence must be at least as long as the opening fence” — lead-in to Examples 124–125.
- Scope: the spec is a rendering grammar for fenced code blocks. It says nothing about which block an answer grader should select. That matches the row's scope cell.

## Teaches/anchor confirmation

- Anchor "§4.5 Fenced code blocks; examples on closing fences": **confirmed**. §4.5 spans Examples 119–147. Closing-fence behaviour is covered by Examples 122–125 (type and length) and Example 147 (no info strings).
- Teaches, "closing fences have no info strings": **confirmed** by quote 1.
- Teaches, "must match opening type/length": **partially confirmed, with one imprecision**.
  - Type: confirmed. The closing fence must be the same type as the opening one (quote 2).
  - Length: the spec only requires the closing fence to be *at least as long* as the opening fence (quotes 2 and 3). Examples 124 and 125 close four-character fences with longer runs (six backticks and four tildes respectively), and three-character runs inside the block do not close it. "Match … length" reads as "equal length", which is stricter than the spec.
  - This is a calibration nit in an immutable cell, and it does not affect the lane's claim. Disposition is below.
- Teaches, "the lane's regexes are deliberately narrower/different, not CommonMark parsers": **confirmed from static code reading only; I executed nothing**.
  - `plans/parser_policy_compare.py:36` defines ``FENCE_ANY = re.compile(r"```[A-Za-z0-9_+-]*[ \t]*\r?\n(.*?)```", re.S)``. It accepts exactly three backticks and no tildes.
  - Its label class is narrower than CommonMark info strings, which may contain spaces and other characters.
  - The non-greedy close is not line-anchored and enforces neither the length rule nor the no-info-string rule.
  - There is no indentation handling. An unclosed fence is not matched, whereas CommonMark runs an unclosed block to the end of the document.
  - So the knowledge sentence at `extraction-policy-comparison.md:51`, "E6 is not a CommonMark parser: it omits valid info strings and fence-length rules (S054)", is supported as a limit statement.
  - [INFERENCE] I did not inspect the lane grader's `gp.FENCED_RE`, which drives E0, E1 and E5. The row's plural "regexes" is supported here only for `FENCE_ANY`.

## C2 literal-reference check (frozen 35-path population)

- Method: I applied `population.json` `reference_pattern` `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` line by line to all 35 `knowledge_paths` with an ad hoc stdlib scan. This is not the delivered `registry_check.py`.
- Hits for S054: exactly 2, both in one file.
  - `corpus/knowledge/extraction-policy-comparison.md:1`, in the frontmatter `source:` list: "S054 https://spec.commonmark.org/0.31.2/#fenced-code-blocks §4.5".
  - `corpus/knowledge/extraction-policy-comparison.md:51`, in the E6 limit sentence quoted above.
- None of the other 34 frozen knowledge files mention S054.
- Citing files are {`corpus/knowledge/extraction-policy-comparison.md`}.
- The used-by cell is `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`. That leaves `missing_used_by` = ∅. The extra lesson path is permitted under the contract.
- Status `mined` with ≥1 citing file is consistent: the source is cited and not left queued.
- File hash at check: extraction-policy-comparison.md SHA-256 `b77b7db4ecfcf843ab521631de1b4f31c06253464ff28e9d491c83a3cc794a67`.

## Suggested mutable-cell changes (status / recheck / used-by only)

None.
- Status `mined` is correct.
- Used-by already covers every frozen citing file.
- Recheck `2027-01-19` is opened + 90 days. The spec URL is version-pinned, and today's bytes equal the round-27 hash, so there is no reason to move it.

The expected `registry_check.py` row for S054 is: citing_files=[extraction-policy-comparison.md], missing_used_by=[], status=mined, no finding.

## Immutable-cell observation (advice only, no change proposed this round)

The teaches wording "must match opening type/length" overstates the spec's length rule, which is "at least as many". Immutable cells must stay unchanged in round 28, and seats may not add rows. If L1 wants to fix it, the lane precedent is a later superseding correction row (as S039, S040 and S042 did for S034, S035 and S030), saying "same type and at least as long". The C2 literal check is unaffected either way.

## Limitations

- The scan is a literal standalone-ID match. It is not semantic citation support and does not validate other claims in `extraction-policy-comparison.md`.
- E6 behaviour is inferred from reading the regex, not from running `parser_policy_compare.py`, which was not run here.
- The quote locations come from tag-stripped HTML text. Quote 1 does not match the raw HTML literally because of inline markup.

## Verdict

**PASS for S054 only.**
- The source was reopened at the pinned version with a byte-identical hash.
- Anchor and scope are confirmed.
- Teaches is confirmed, apart from one disclosed length-wording imprecision in an immutable cell.
- Literal C2 coverage for S054 is complete, and no mutable-cell change is needed.

This is not a C2-wide or round-28 PASS.
