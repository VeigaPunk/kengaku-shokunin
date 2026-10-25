# RowRFC8259 — round 27 source row draft (E4 grounding)

Scope: RFC 8259 grammar and whitespace only, as the grounding for E4 strict-whole. Leaf seat, no delegation, no edits outside this report. Not written: SOURCES.md, gate.md, knowledge entries.

## Opened source

- URL: https://www.rfc-editor.org/rfc/rfc8259 (reader view, Metadata: Published December 2017, Obsoletes RFC7159, Standards Track).
- Bytes: https://www.rfc-editor.org/rfc/rfc8259.txt, fetched 2026-10-21 with curl (exit 0), saved to /tmp/kengaku-r27-RowRFC8259/rfc8259.txt, 899 lines.
- sha256: 61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7
- Locations used (txt line numbers, verified with grep/sed):
  - L246–L257 §2 JSON Grammar: "JSON-text = ws value ws" at L257.
  - L287–L288 §2: "Insignificant whitespace is allowed before or after any of the six structural characters."
  - L290–L294 §2: ws = *( %x20 / %x09 / %x0A / %x0D ) (space, tab, LF, CR only).
  - L308 §3: value = false / null / true / object / array / number / string.
  - L377–L378 §6 Numbers: "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted."

## (1) Draft SOURCES.md row (S0xx)

Note: the brief says 13 cells, but the existing registry header and every existing row have 11 cells (id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by). This draft follows the 11-cell header. Census arbitrates.

| S0xx | RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format — https://www.rfc-editor.org/rfc/rfc8259 | spec | A | what RFC 8259 normatively says about the JSON text grammar and its whitespace, not how any harness extracts answers | §2 JSON Grammar, txt lines 246–294; §6 Numbers, txt lines 377–378 | a JSON text is one value wrapped only in insignificant whitespace (space, tab, LF, CR); numbers outside the grammar, such as Infinity and NaN, are not permitted | queued | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |

## (2) gate.md line (draft, not written)

- S0xx: https://www.rfc-editor.org/rfc/rfc8259 (txt: rfc8259.txt, sha256 61a5378f…d7); accessed 2026-10-21; RFC 8259, December 2017; §2 JSON Grammar, txt line 257: "JSON-text = ws value ws" (5 words, exact).
- Second located quote, §2, txt lines 287–288: "Insignificant whitespace is allowed before or after any of the six structural characters." (14 words, exact, line-wrapped in source).
- Third located quote, §6 Numbers, txt lines 377–378: "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted." (19 words, exact, line-wrapped in source).

## (3) Policy grounding

- Grounds: E4 strict-whole (`json.loads(raw.strip())`). The RFC grammar says a JSON text is exactly `ws value ws`, so E4 is the only pre-registered policy whose semantics mirror the whole-output rule.
- Gap, observed (python3 3.14.8, this host, offline):
  - `json.loads('NaN')` returns `nan`, and `json.loads('Infinity')` returns `inf`. RFC §6 says such values are not permitted, so the Python decoder is looser than the RFC.
  - `'\x0c{"a":1}\x0b'.strip()` followed by `json.loads` returns `{'a': 1}`. `str.strip()` removes form feed and vertical tab, which RFC ws (L290–294) excludes.
  - Consequence: E4 is strict relative to Python's decoder after `str.strip()`, not RFC-strict. The label "strict" in C1 should be scoped that way. E0–E3, E5–E8 use the same decoder, so the NaN/Infinity acceptance applies to all of them.
  - Not measured: whether any of the 1964 stored responses hits these cases. [INFERENCE] unlikely to move verdicts, but unobserved here.
- No other policy is grounded by this source. E1–E3, E5–E8 are fence or bare-match selection rules, not grammar rules.

## Sources cited (access date 2026-10-21)

- RFC 8259, §2 JSON Grammar and §6 Numbers, https://www.rfc-editor.org/rfc/rfc8259 (txt L257, L287–288, L290–294, L377–378).

## Installs

None. Used existing curl and python3 3.14.8. No pacman, no uv, no packages.

## Files written

- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/build/RowRFC8259.md (this report).
- /tmp/kengaku-r27-RowRFC8259/rfc8259.txt (scratch copy of the RFC bytes, sha256 above).

VERDICT: RFC 8259 drafted as an 11-cell queued row grounding E4; the RFC grammar is strict but E4's Python decoder accepts NaN/Infinity and strips \x0b/\x0c, so E4 should be labelled Python-strict, not RFC-strict.
