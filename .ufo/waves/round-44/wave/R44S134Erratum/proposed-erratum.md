
## Errata (round 44, closure R2: source-span counting; nothing above edited)

Appended 2026-10-26 (round 44, one v2 wave, closure item R2). Every number below was measured on the pinned capture
in this lane (`corpus/evidence/round43/tb2-feal-differential-cryptanalysis/`, `sha256sum -c SHA256SUMS` → 12/12
`OK`) and re-checked against a fresh fetch of the pinned raw URL (HTTP 200, 1603 bytes, `cmp` identical); the
commands and their output are filed with `.ufo/waves/round-44/wave/R44S134Erratum/`. Both errata are provenance-only:
no predicted, observed or `regrade` value, DECISIVE line, requirement label, Mechanism row or quote changes. A sweep
of the 19 `source:` lines in `corpus/knowledge/*.md` that carry a `lines A-B` against their `corpus/SOURCES.md` row
finds these two as the only disagreements (15 agree, 2 whose row carries no span for that file).

| `source:` line | as filed | measured lines | SOURCES row anchor |
|---|---|---|---|
| S132 `feal.c` | "lines 1-99" | **100** (`wc -l` 99; last byte `}`) | `feal.c:1-100` (`corpus/SOURCES.md:147`) |
| S134 `README.md` | "lines 1-34" | **35** (`wc -l` 34; last byte `t`) | `README.md:1-35` (`corpus/SOURCES.md:149`) |

**Erratum (round 44): S134's span is `README.md:1-35`, not "lines 1-34".** The pinned `README.md` is 1603 bytes with
**no final newline** (last byte `t`, `tail -c 1 README.md | od -An -c`), so `wc -l` prints 34 while
`awk 'END{print NR}'` and `grep -c ''` both report 35 and `sed -n '35p'` prints
`4. Confirms the attack completes within the time limit`. The `source:` line counts newline-terminated lines only, so
it undercounts the file's extent by its last line and disagrees with the S134 row anchor and with this entry's own
citations of `README.md:35` (`:42`, `:148`, `:186` — the Located quotes row "the authors claim the test enforces the
time limit"). Read S134's span as `README.md:1-35`. The capture, its digest
`887407c78513837d93f02231998419a0ce9b0cc0a0c600ed86cd30df5cb24e7f` (`SHA256SUMS:2`, `plans/pkg-spec-r43.json`
`rows.S134`) and every quote above are unchanged.

**Erratum (round 44): S132's span is `feal.c:1-100`, not "lines 1-99".** Same defect, same measurement: the pinned
`feal.c` ends with an unterminated last line (`wc -l` 99, `awk 'END{print NR}'` 100, last byte `}`) and the S132 row
anchor at `corpus/SOURCES.md:147` already reads `feal.c:1-100`. Read the span as `feal.c:1-100`; no citation of
`feal.c` in this entry falls on `:100` (the highest is `:88`), so no finding, case or Gate quote rests on the
undercounted line.
