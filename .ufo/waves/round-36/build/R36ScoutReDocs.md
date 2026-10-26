# R36ScoutReDocs — Python `re` docs quotes for the regex-log entry

Fetched 2026-10-26 01:12 UTC (host clock; task date 2026-10-25) with
`curl -sS -o re3.html https://docs.python.org/3/library/re.html` (scratch:
`.ufo/waves/round-36/build/R36ScoutReDocs/re3.html`, 257706 bytes,
`sha256 794184089c0d033dade072beab6238e51b9a375f4b23629ec6b5e51ddb7215ff`; HTTP 200,
`last-modified: Sun, 25 Oct 2026 23:58:36 GMT`, `etag "6ade97ac-3eeaa"`).

**Doc version string:** `<title>re — Regular expression operations — Python 3.15.1 documentation</title>`
(the `/3/` alias now resolves to 3.15.1; source link `github.com/python/cpython/blob/3.15/Doc/library/re.rst`).
Observed fact: `/3/` drifts. The same five quotes below were checked as a whitespace-normalised
substring of the tag-stripped, entity-unescaped page in all four of: `/3/` (3.15.1), `/3.14/`
(`Python 3.14.9`, sha256 prefix `8754089ba44b453e`), `/3.13/` (`3.13.17`, `5948bf28566e9fdf`), `/3.12/`
(`3.12.15`, `e2c3acab59d90751`) → all `True`. The probe ran under local `Python 3.14.8`
(`python3 --version`). If a row is ever added, pin `/3.14/library/re.html` (matches the probe's
interpreter line) and byte-capture it; `/3/` would change digest on every doc build.

Note on wording: the docs say **"fixed length"**, not "fixed-width". Quote (b) is therefore verbatim "fixed length".

## Quotes (all verified verbatim; word counts by `len(q.split())`)

All four are in the text of `https://docs.python.org/3/library/re.html`; fragment anchors are the page's `id=`s.

| # | Claim | Section heading (path) | Anchor | Quote (verbatim) | Words |
|---|---|---|---|---|---|
| a | `findall` → list of tuples for >1 group | Module contents › Functions › `re.findall(pattern, string, flags=0)` | `#re.findall` | "If multiple groups are present, return a list of tuples of strings matching the groups." | 15 |
| b | lookbehind needs fixed length | Regular expression syntax › Special characters › `(?<=...)` (positive lookbehind) | `#re-syntax-lookbehind` | "The contained pattern must only match strings of some fixed length, meaning that abc or a|b are allowed, but a* and a{3,4} are not." | 24 |
| b′ | same, negative lookbehind (shorter alt.) | same › `(?<!...)` | `#re-syntax-negative-lookbehind` | "the contained pattern must only match strings of some fixed length." (verbatim tail of "Similar to positive lookbehind assertions, the contained pattern must only match strings of some fixed length.", 16 words whole) | 11 / 16 |
| c | MULTILINE `^` | Module contents › Flags › `re.M` / `re.MULTILINE` | `#re.MULTILINE` | "When specified, the pattern character '^' matches at the beginning of the string and at the beginning of each line (immediately following each newline);" | 24 |
| c′ | default `^` (contrast) | same | `#re.MULTILINE` | "By default, '^' matches only at the beginning of the string" | 11 |
| d | `findall` includes empty matches | Module contents › Functions › `re.findall` | `#re.findall` | "Empty matches are included in the result." | 7 |

Supporting quotes for the first-date case (the receipt case `first-date-only`: `^(?=…IPv4…).*?DATE`, lazy
quantifier, observed `fail` — it returns the first date per line instead of the last):

| # | Claim | Section | Quote | Words |
|---|---|---|---|---|
| e | one match per `^` line because scan is non-overlapping, left-to-right | Functions › `re.findall` | "Return all non-overlapping matches of pattern in string, as a list of strings or tuples." | 15 |
| e′ | left-to-right ordering | Functions › `re.findall` | "The string is scanned left-to-right, and matches are returned in the order found." | 13 |
| f | lazy `.*?` stops at the first date | Regular expression syntax › Special characters › `*?`, `+?`, `??` | "Adding ? after the quantifier makes it perform the match in non-greedy or minimal fashion; as few characters as possible will be matched." | 23 |
| g | non-capturing groups do not change result shape (relevant to why the oracle's lookahead is `(?=…)`/`(?:…)`) | Functions › `re.findall` | "Non-capturing groups do not affect the form of the result." | 10 |

(`f` and `g` word counts checked by `len(q.split())`; `f` verified present, `g` verified present.)

## How each ties to the receipt (observed in the lane, not inferred)

- `corpus/evidence/round36/tb2-regex-log/test_outputs.py:86-87`: `# Apply regex with MULTILINE` /
  `matches = re.findall(pattern_text, log_text, re.MULTILINE)`; line 90 asserts
  `matches == expected_dates`. So quote (c) is the doc statement for why `^` anchors every line, and
  (a)/(d) are the doc statements for the result shape that `==` is then compared against.
- Receipt `corpus/evidence/round36/regex-log-probe.txt:23` (`extra-capture-group`): assertion shows
  `but got [('192.168.0..."` — tuples. Quote **(a)** is the doc for it. `g` explains the fix.
- Receipt line 20 (`empty-pattern`): `but got ['', '', '',...` — empty strings, one per position. Quote **(d)**
  is the doc for it (a `''` pattern matches empty at every position; the oracle's `^`-anchored real
  patterns never do).
- Receipt line 4 (`first-date-only`): lazy variant, observed `fail`. Quotes **(f)** + **(e)** are the doc
  basis (lazy ⇒ first date; non-overlapping ⇒ one match per anchored line).
- `plans/regex_log_probe.py:32` uses `(?<![A-Za-z0-9])` — a *negative lookbehind*, always one character, so
  it satisfies the fixed-length rule; quote **(b)/(b′)** is the doc statement for why the boundary guard can
  be a lookbehind but a variable-width guard (`(?<!\d+)`) would raise `re.error`. The probe has no
  variable-width lookbehind case (grep `(?<` in the probe: lines 32, 89 only, both single-char classes), so
  (b) explains a design choice, not an observed receipt line.

## Need vs optional (the entry already stands on the receipt)

- (a) extra-capture-group → tuples: **optional**; the receipt line 23 already shows the tuples (observed).
  Worth citing only to say the behaviour is documented, not an artefact of 3.14.8.
- (d) empty matches in findall → **optional**; receipt line 20 shows `['', '', ''`.
- (c) MULTILINE `^`: **optional but the best-value one** — the grader's own comment says MULTILINE; the
  entry's per-line framing (`^(?=.*IP).*DATE`) rests on this semantics, and the probe's passing cases
  exercise it, so the receipt already supports it.
- first-date (e, f): **optional**; explained by greedy/lazy semantics visible in the `pass` vs `fail` pair.
- (b) fixed-length lookbehind: **not needed**; no receipt case depends on it. Cite only if the entry
  discusses the digit-adjacent boundary and wants to say why the probe's guards are one-character.

Recommendation: the entry should not need any of these. If the lane wants one docs-backed sentence, use
(a) + (c) + (d) from one capture.

## Registry row (only if the entry cites it) — draft, not proposed unconditionally

No row exists yet in `corpus/SOURCES.md`; I did not read the exact 11-column header of the current
registry beyond the task statement's "11-column form (id S111, tier A, kind docs)". Draft (columns
as given: id | kind | tier | title | URL | opened | status | used-by | teaches | …), to be aligned by the
L1 to the header of `corpus/SOURCES.md` before use; the column order below is **[INFERENCE]** and
unverified against the registry:

```
| S111 | docs | A | Python `re` — Regular expression operations (3.14) | https://docs.python.org/3.14/library/re.html | 2026-10-25 | mined | corpus/knowledge/tb2-regex-log-grader.md | findall returns tuples with more than one capture group and includes empty matches; MULTILINE makes ^ match at each line start; lookbehind requires a fixed-length pattern | … |
```

Capture requirement if adopted: byte-copy `https://docs.python.org/3.14/library/re.html` to
`corpus/evidence/round36/tb2-regex-log/` (or a sibling `python-re-3.14.html`) with its sha256 in
`SHA256SUMS`; the 3.14 digest at fetch time was `8754089ba44b453e…` (prefix only; recompute full digest when
capturing — I saved only the `/3/`, 3.12, 3.13, 3.14 HTML in scratch). Caveat: C2's W1 pins the capture
manifest at digests and W3 requires ≥8 distinct located quotes at ≥8 distinct lines; adding S111 changes
the S108-S110 frozen row set (claims line 66-68 name S108-S110 only), so adding S111 is an unfrozen
addition — the claims say "no package row is appended unless an admitted entry cites it". Do not add S111
unless the entry cites it; the receipt alone supports every statement.

Unresolved: exact SOURCES.md column order (not read; outside the assigned question); the full sha256 of the
3.14 capture (only prefix printed).

VERDICT: redocs-4-quotes-located
