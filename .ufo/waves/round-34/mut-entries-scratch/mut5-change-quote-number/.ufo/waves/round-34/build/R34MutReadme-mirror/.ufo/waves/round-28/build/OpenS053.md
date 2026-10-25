# OpenS053 — round 28 reopen of S053 (RFC 8259 JSON grammar)

Writer/seat: `KengakuR28.OpenS053-2` (read-only scout, author-side advice — not outside non-author closure).
Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Lane HEAD observed `f0ba09be0f3066daba2134b943d973ad1588f34a` (preregistration); baseline `b9b24796277020d1b9b01923b45313d6a565e664`.
Writes: this report plus scratch copies under `.ufo/waves/round-28/scratch/OpenS053/` only. I made no registry or production edits, did not commit, and installed or updated no tools.

## Row under review (`corpus/SOURCES.md:75`, identical at baseline)

`| S053 | RFC 8259 JSON grammar — https://www.rfc-editor.org/rfc/rfc8259 | spec | A | JSON text grammar and permitted insignificant whitespace | §2 JSON Grammar | a JSON text is whitespace then one value then whitespace; Unicode strip is broader than the RFC's four whitespace characters | mined | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md |`

## Opening (access date 2026-10-21)

| URL | Result | Scratch copy | SHA-256 |
|---|---|---|---|
| https://www.rfc-editor.org/rfc/rfc8259 (the row URL) | HTTP 200, but it redirects to `https://www.rfc-editor.org/info/rfc8259/`, whose title is "RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format \| RFC Editor" | `scratch/OpenS053/rfc8259.html` | `c813c1125b9ba21d4c485f4e59376d84243176a5ed3ae417f80a91bf9f869f57` |
| https://www.rfc-editor.org/rfc/rfc8259.txt (authoritative text) | HTTP 200, 899 lines; the header names T. Bray (editor), IETF Standards Track, December 2017, and says it obsoletes RFC 7159 | `scratch/OpenS053/rfc8259.txt` | `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` |

The `.txt` hash is byte-identical to the round-27 hash recorded in `corpus/evidence/round27-sources/gate.md:47`. The text has not drifted since round 27.

Located quotes, all from §2 "JSON Grammar" (`.txt` lines 246–294):
- line 257: "JSON-text = ws value ws" (5 tokens; same quote as `corpus/evidence/round27-sources/gate.md:12`).
- lines 287–288: "Insignificant whitespace is allowed before or after any of the six structural characters." (14 words)
- lines 290–294: `ws = *( %x20 / %x09 / %x0A / %x0D )`, annotated Space, Horizontal tab, Line feed or New line, Carriage return.

## Do the teaches and anchor cells hold?

- **Anchor `§2 JSON Grammar`: confirmed.** The heading is at `.txt` line 246, and every quote above falls inside §2.
- **Scope, and the first clause of teaches ("a JSON text is whitespace then one value then whitespace"): confirmed.** This is exactly `JSON-text = ws value ws`.
- **"the RFC's four whitespace characters": confirmed.** The `ws` rule allows exactly U+0020, U+0009, U+000A and U+000D.
- **"Unicode strip is broader": the RFC does not say this.** RFC 8259 never mentions Python `str.strip()`. This half of the clause is a comparison the lane made, and it depends on Python semantics. I checked it against the Python documentation, but that check is corroboration only, not a new source row and not a change to S053:
  - Page: https://docs.python.org/3/library/stdtypes.html, accessed 2026-10-21. The live docs report Python 3.15.1. Scratch copy `scratch/OpenS053/py-stdtypes.html`, SHA-256 `7dcb450d84d0176f7d7d996853d7be8b19b3e9a49479f67c5f8efc74627e1ff2`.
  - `str.strip` entry: "If omitted or None, the chars argument defaults to removing whitespace." It then says whitespace is defined by `str.isspace`.
  - `str.isspace` entry: "either its general category is Zs (“Separator, space”), or its bidirectional class is one of WS, B, or S." That set is a strict superset of the RFC's four characters (for example, U+3000 is listed in the docs).
  - Isolated local probe, stdlib only, no upstream code: `python3` 3.14.8 evaluated `'\u00a0\u2003\x0b\x0c\u3000x\u2028'.strip()` and printed `'x'`.
- **Kind `spec` and tier A, scoped to the JSON text grammar: appropriate.** RFC 8259 is the IETF Standards Track specification. Tier is scoped to the row's scope only, not to Python behaviour and not to the NaN/Infinity rule in §6, which S059 covers.

## Literal citations in the frozen 35-file population

I applied the population's `reference_pattern` (narrowed to `S053`) to all 35 `knowledge_paths` in `plans/fixtures/r28/registry/population.json`, both at the baseline revision and in the current worktree. All 35 files were present in both.

The only citing file is `corpus/knowledge/extraction-policy-comparison.md`, identical in both trees, with 2 mentions:
- line 1, the `source:` front matter list.
- line 51: "E4's Unicode `strip()` is broader than RFC 8259 whitespace (S053)".

The other 34 frozen files have no S053 mention.

Comparison with the registry row:
- Status is `mined`. The cited row must be `mined`, so this is correct.
- Used-by contains the single citing frozen path, so nothing is missing.
- The extra used-by entry `corpus/lessons/round-27.md` is a lesson path, which the C2 contract permits. That lesson cites S053 at lines 46, 57, 154, 197 and 201.

Semantically, line 51 matches the row's scope and teaches cells. The "RFC 8259 whitespace" half is supported by §2. The "Unicode `strip()` is broader" half is supported by the Python docs, not by the RFC, which is the same caveat as above.

## Allowed mutable-cell suggestion

Change nothing. Status `mined`, recheck `2027-01-19` and used-by are all consistent with today's opening and the frozen literal population. Immutable cells (id, source/URL, kind, tier, scope, anchor, teaches) must stay unchanged.

Two disclosures, neither a cell change:
1. The row URL now redirects to the `/info/rfc8259/` landing page. The `/rfc/rfc8259.txt` text is the stable byte-identical opening.
2. The second half of the teaches clause depends on Python `str.isspace` semantics, which are outside RFC 8259.

## Template clauses that do not apply

The dispatch template includes instructions for own-work S056 (open the implementation and committed receipt) and for S038 (original DOI/publisher full text, Introduction coverage warning). They do not apply to this seat. S053 is an external IETF spec, not own work, and not S038. Those IDs belong to sibling seats (for example `scratch/OpenS038`). I did not attempt them and claim no opening for them.

## Observed commands

- `curl -sSL` of the three URLs above into scratch.
- `sha256sum` of the scratch copies.
- `grep` and `sed` on the RFC text, and a Python regex/HTML-strip extraction from the Python docs page.
- A Python script running the population regex over the 35 paths via `git show <baseline>:<path>` and the worktree.
- The one-line `str.strip` probe above.

I ran no builds, tests, linters or formatters, and contacted no benchmark sites.

## Limitations

- This is literal-reference and anchor verification only. It is not an endorsement of the knowledge entry's empirical result ("no difference in the pinned population"), which I did not re-run.
- Live Python docs (3.15.1) and the local interpreter (3.14.8) may not match the Python version used for the round-27 population run. `str.isspace` semantics are long-stable, so this risk is low. [INFERENCE]
- This is author-side advice from a roster seat, not outside closure.

## Verdict

**PASS (scoped to S053)**:
- RFC 8259 was reopened on 2026-10-21, and its text matches the round-27 hash.
- The §2 anchor, scope and four-character whitespace claim hold, with located quotes.
- The literal citation set in the frozen 35 files is exactly one file, and it is already in used-by with status `mined`.
- No mutable-cell change is needed.

Carried caveat: the "Unicode strip is broader" half of the teaches clause is supported by Python's documentation, not by RFC 8259.
