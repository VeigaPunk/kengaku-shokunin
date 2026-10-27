
## Errata (round 44, closure R2: S134 source span; nothing above edited)

Appended 2026-10-26 (round 44, one v2 wave, closure item R2). Every number below was measured on the pinned capture
in this lane (`corpus/evidence/round43/tb2-feal-differential-cryptanalysis/`, `sha256sum -c SHA256SUMS` → 12/12
`OK`) and re-checked against a fresh fetch of the pinned raw URL (HTTP 200, 1603 bytes, `cmp` identical); the
commands and their output are filed with `.ufo/waves/round-44/wave/R44S134Erratum/`. The erratum is provenance-only:
no predicted, observed or `regrade` value, DECISIVE line, requirement label, Mechanism row or quote changes.

**Erratum (round 44): S134's span is `README.md:1-35`, not "lines 1-34".** The pinned `README.md` is 1603 bytes with
**no final newline** (last byte `t`, `tail -c 1 README.md | od -An -c`), so `wc -l` prints 34 while
`awk 'END{print NR}'` and `grep -c ''` both report 35 and `sed -n '35p'` prints
`4. Confirms the attack completes within the time limit`. The `source:` line counts newline-terminated lines only, so
it undercounts the file's extent by its last line and disagrees with the S134 row anchor
(`corpus/SOURCES.md:149`, `README.md:1-35`) and with this entry's own citations of `README.md:35` (`:42`, `:148`,
`:186` — the Located quotes row "the authors claim the test enforces the time limit"). Read S134's span as
`README.md:1-35`. The capture, its digest
`887407c78513837d93f02231998419a0ce9b0cc0a0c600ed86cd30df5cb24e7f` (`SHA256SUMS:2`, `plans/pkg-spec-r43.json`
`rows.S134`) and every quote above are unchanged.
