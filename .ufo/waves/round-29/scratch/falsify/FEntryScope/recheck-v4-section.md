
## Final re-check of candidate v4 (locator-only follow-up)

This is a second-seat re-read for the same item, FEntryScope. Everything above is left unedited. This
section covers only the v4 line-1 locator change, plus a byte comparison of the rest against the v3 I passed.

- **Candidate path:** `.ufo/waves/round-29/drafts/webarena-config-projection.md`
- **Canonical path:** `corpus/knowledge/webarena-config-projection.md`
- **sha256, printed first:** `9d11f44bf22d357758a5988b514d23cca84d4061816d3c3d65294974dd506e74`
  (99 lines, 8772 bytes). These are the exact bytes I reviewed.
- **Production source:** NOT read.
- **Writes:** this appended section and `scratch/.../recheck-v4-section.md`.
- **No lane, git or jj mutation.** Installs: none.
- **`/tmp`:** I used one copy, `/tmp/FEntryScope-json.html`, fetched twice and deleted both times.
  After the final delete, `test -e` returned 1 (absent).

### Byte comparison against v3 (observed)

- I kept no v3 copy, so I rebuilt v3 from v4. I put the old S071 text (`S071 https://docs.python.org/3/library/json.html Character Encodings §576-591, invalid-document402, duplicate names624-625`)
  back in place of v4's `S071/S075 …` segment in line 1, keeping everything else.
- The rebuilt line 1 hashes to `889d53f2…71ac9`, equal to the v3 line-1 hash I recorded earlier.
- The rebuilt file hashes to `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`, equal
  to the v3 I passed and to `candidate-freeze-v3.json`.
- **So v4 differs from v3 only in that one segment of line 1.** Lines 2–99 are byte-identical to v3
  (their sha256 is `9148a503…4f4a`). The body, numbers and decision rule are unchanged, and my v3
  findings carry over intact.

### The locator correction, reopened (observed)

I fetched `https://docs.python.org/3/library/json.html` on 2026-10-21. The page sha256 was
`8271280b…01d5`, and its title reads "Python 3.15.1 documentation", matching the S071/S075 version.

| v4 locator | anchor present | content at the anchor | status |
|---|---|---|---|
| `#character-encodings` ensure_ascii paragraph | yes | "this module's serializer sets ensure_ascii=True by default, thus escaping the output so that the resulting strings only contain printable ASCII characters" | exact |
| `#repeated-names-within-an-object` opening paragraph/example | yes | "it ignores all but the last name-value pair for a given name", with the example `json.loads('{"x": 1, "x": 2, "x": 3}')` giving `{'x': 3}` | exact; supports v3 lines 34–36 (last value wins) |
| `#json.loads` invalid-document exception | yes | the block says only "Identical to load() …"; the sentence "When the data being deserialized is not a valid JSON document" appears under `#json.load` ("Raises: JSONDecodeError") and under `#json.JSONDecoder` | fact correct, **anchor one hop off** |

**Non-blocking locator note L1.** The `#json.loads` locator in line 1 and in the S075 row does not hold
the invalid-document sentence itself. `json.loads` inherits it through "Identical to load()", so the fact
in v4 line 34 is correct and the anchor is stable.

- Smallest fix, if wanted: "#json.load invalid-document exception (json.loads: 'Identical to load()')".

This is a locator-precision issue, not an overclaim, so my scope verdict does not depend on it.

### Scoped verdict

- The single changed line is confirmed. Two of the three stable anchors are exact, and the third is a
  correct fact reached through the documented "Identical to load()" link (note L1).
- Byte-identity of lines 2–99 with v3 is proved by the hash reconstruction above.
- Every scope, source, number and decision-rule conclusion from my v3 re-check therefore holds for v4
  unchanged.
- The optional residuals R1 and R2 from earlier stand as non-blocking.
- This verdict covers this exact v4 re-read, not round admission.

VERDICT: PASS
