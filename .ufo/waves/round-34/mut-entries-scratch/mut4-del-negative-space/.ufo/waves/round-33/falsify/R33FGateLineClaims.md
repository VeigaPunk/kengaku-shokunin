# R33 falsify — quote gate line-number and section claims

Seat: `KengakuR33.R33FGateLineClaims` (leaf, falsify wave 36, hyaku run 7).
Target: `plans/sources_adopt.py` — `quote_check`, `locates`, `quoted_spans`, `load_artifact`.
Artifact pin: `sha256 38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0`,
1083 lines. Read-only against the gate: no plan, registry, capture, or wave file was edited,
staged, or committed by this seat; the only lane write is this report.
All fixtures live under `/tmp/r33-lineclaims.h4k2Du` (fresh `mktemp -d`); every run below was
executed with `cwd=/tmp/r33-lineclaims.h4k2Du` and the gate addressed by absolute path.

## Question

Does an anchor cell's **quoted bytes** have to occur at the **line numbers** or **sections** its
**unquoted prose** names?

## Answer: no. The prose is never parsed.

`quote_check` (`:442`) reads exactly one column, `ANCHOR_COLUMN = 5` (`:276`), and passes it to
`quoted_spans` (`:289`), which returns the contents of every `"…"` pair and nothing else. The
prose between and around the spans — `:58`, `:279`, `§Gate`, `line 27`, `p.1677`, the commit pin —
is discarded before any comparison. Locatedness is then
`needle in text` over the whole artifact (`locating_artifacts` `:393`, `locates` `:404`), with
only newline normalisation in front of it (`normalize_text` `:284`). There is no line index, no
heading parser, no offset arithmetic, and no code path that could reject a false location claim.

The gate's *only* structural demands on the anchor cell are: at least one `"…"` pair, and an even
number of quote characters (`:296-300`). A cell with a location and no quote is refused
(`no-quote`, exit 4); a cell with a quote and any location whatsoever is judged on the quote alone.

## Probes

Command form (all probes):

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py \
  --quote-file /tmp/r33-lineclaims.h4k2Du/<probe>.rows.txt \
  --artifact   /tmp/r33-lineclaims.h4k2Du/<artifact> \
  --url-map    /tmp/r33-lineclaims.h4k2Du/<probe>.urlmap.json
```

Rows are 11-cell table rows; the anchor cell is the real registry cell unless the probe says it
was mutated. Control artifacts are copies of
`.ufo/waves/round-33/assimilation/captures/toolathlon-ab-testing-evaluation-main.py`
(`sha256 3bad26b61448f1f0…a9b9ad`, 297 newline-terminated lines) and `arxiv-2412.05579v2-abs.html`.

| # | attack on the prose claim | expected if lines/sections bound | observed | verdict |
|---|---|---|---|---|
| F0 | control: live S103 anchor, real capture | 0 | `EXIT=0`, `spans=5 located=5 found=5` | baseline |
| F1 | every label falsified: `:58→:9001`, `:279→:9002`, `:280→:9003`, `:218→:9004`, `:234→:9005` (file has 297 lines) | 7 | **`EXIT=0`**, `located=5` | uncaught |
| F2 | artifact shifted by 40 lines (bytes now at `:98`, `:319`, `:320`, `:258`, `:274`), prose still claims `:58`, `:279`, `:280`, `:218`, `:234` | 7 | **`EXIT=0`**, `at main-shifted.py` | uncaught |
| F3 | prose says `§Gate`; the only occurrence is inside `## Appendix: quotations we do not endorse` | 7 | **`EXIT=0`**, `ok S103 words=11 at sections.md` | uncaught |
| F4b | artifact is a unified diff; the bytes occur only on the **removed** `-def validate_record_data(…)` line; prose claims `main.py:58` | 7 | **`EXIT=0`**, `ok S103 words=11 at main.patch` | uncaught |
| F5 | label/span association swapped: the `:58` label now sits on the `:234` quote and vice versa | 7 | **`EXIT=0`**, `spans=5 located=5` | uncaught |
| F6 | no location syntax at all — anchor cell is the bare quote | 4 (if a location is mandatory) | **`EXIT=0`** | uncaught (no syntax requirement exists) |
| F7 | prose names `utils/evaluation/retry.py:58`; bytes are in `main.py` | 7 | **`EXIT=0`**, `at main.py` | uncaught |
| F8 | malformed `:abc` and out-of-range `:99999-100000` labels | 4/7 | **`EXIT=0`**, `located=5` | uncaught |
| F9 | live S104 anchor, real arXiv capture | 0 | `EXIT=0`, `spans=3 located=3` | baseline |
| F10 | S104 labels crossed (`:124` on the title, `:41` on the abstract) | 7 | **`EXIT=0`** | uncaught |
| F12 | one of the five labelled spans deleted from the cell (5 claims, 4 quotes) | 4 | **`EXIT=0`**, `spans=4` | uncaught (no label↔quote cardinality) |
| F13 | prose names `§Gate`; the artifact contains no such heading anywhere | 7 | **`EXIT=0`** | uncaught |
| F15 | artifact is a log; the bytes occur on a line beginning `2026-10-25 diff -def validate_record_data(…)`; prose claims `main.py:58` | 7 | **`EXIT=0`**, `at run.log` | uncaught |
| F16 | verbatim live S103+S104 rows over the committed `captures/` dir and committed `url-map.json` | 0 | `EXIT=0`, `rows=2 spans=8 located=8` | reproduces the round's receipt |
| **F17** | **verbatim live rows, every `:NN` label shifted by +7000** | 7 | **`EXIT=0`**, `rows=2 spans=8 located=8` | **uncaught on the landed bytes** |
| F22 | commit pin `9be8d8fe…` in the anchor prose replaced by `deadbeef…` | 7 | **`EXIT=0`**, `located=5` | uncaught (pin is prose too) |
| F19 | location with **no** quote (`main.py:58 (signature default)`) | 4 | `EXIT=4`, `REFUSED S103 no-quote` | caught (structural only) |
| F20 | the location itself quoted (`"tasks/…/main.py:58"`) | 7 | `EXIT=7`, `absent` | caught (it became the span) |
| F21 | `§Gate, lines 58 and 279` with no quote | 4 | `EXIT=4`, `no-quote` | caught (structural only) |
| **F18** | reverse direction: capture wraps the quote across two lines at a space; prose claims `main.py:10` | 0 (bytes present) | **`EXIT=7`**, `absent=1` | **false-negative** |

Decisive stdout, verbatim (F17 — the landed registry rows, all eight labels falsified):

```
QUOTE rows=2 spans=8 located=8 found=8 overlong=0 absent=0 malformed=0 cap=25 artifacts=SHA256SUMS.txt,arxiv-2412.05579v2-abs.html,swebench-pro-tests-test.sh,toolathlon-ab-testing-evaluation-main.py,toolathlon-utils-evaluation-retry.py mismatch=0 unmapped=0 urlmap=url-map.json entries=3
  ok S103 words=11 at toolathlon-ab-testing-evaluation-main.py quote="def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:" bound=toolathlon-ab-testing-evaluation-main.py->https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py
  … (7 more `ok` lines)
EXIT=0
```

Note the receipt shape: `ok S103 words=11 at <artifact> quote="…" bound=<artifact>-><url>`. It
prints the artifact name and a word count — **never a line number or a section**. The printed
receipt therefore cannot be audited against a line claim mechanically, in either direction.

## How wide the unverified surface is

Measured on the live `corpus/SOURCES.md` (97 rows in `## Registry` after this round's S103/S104
landing; the freeze counted 95):

- 42 of 97 anchor cells carry a line/page token (`:58`, `:279-280`, `line 27`, `p.1677`,
  `txt:377-378`, `printed 6710`); 49 `:NN` tokens in total.
- 25 of 97 carry a `§` section reference.
- The gate parses **0** of them. Every one is an assertion by the row's author.

Two further measurements, on the honest rows this round admitted:

- S103's five labels are exactly true and unique in the capture: `:58`, `:279`, `:280`, `:218`,
  `:234` each match exactly one line (297-line file).
- S104's labels are **not unique even when honest**: the title bytes occur at page lines
  4, 21, 23, 33, 41, 98, 116, 117, 177, 243, 248 (11 occurrences); the abstract bytes occur at
  30, 41, 124 (3 occurrences). A hypothetical "does the quote occur at the claimed line?" check
  would pass on a wrong occurrence, which is why the missing check is not a one-line repair.

## Verdict

**Uncaught.** An anchor's quoted bytes are required to occur *somewhere* in the artifact's
normalised text; they are not required to occur at the line, page, section, file, or revision the
anchor's unquoted prose names. F17 is the load-bearing result: the exact registry rows this round
landed, with all eight line labels falsified, still produce `located=8 found=8` and exit 0.

**False-negative, opposite direction.** F18: a capture that legitimately wraps a quote across a
line break is refused with exit 7, because locatedness is a raw byte substring after newline
normalisation only (no whitespace-insensitive or hyphen-blind compare — the gate's own docstring
at `:404` says this is deliberate, and `corpus/knowledge/contamination-transparency-card.md:8`
records that S083's span needs a human hyphen-blind compare the gate cannot perform). Line
structure therefore affects the gate only as a byte obstacle, never as a claim to check: a true
line claim buys nothing, a false one costs nothing.

## Cross-check against the build wave

- `.ufo/waves/round-33/build/R33C1KillRule.md:40` (row 1) states the same defect as UNCAUGHT
  ("no line/section/scope check", "asserted, not gated", severity medium). This seat **confirms**
  it and supplies the run the build report asserted rather than executed: F1, F2, F3, F5, F7, F8,
  F10, F12, F13, F15, F17, F22 all exit 0 with false prose.
- `.ufo/waves/round-33/build/R33GateMutants.md` tested overlong (exit 6) and absent (exit 7) only;
  it did not test location prose. No contradiction.
- `.ufo/waves/round-33/build/R33SourcesAdoptDry.md:216-218` already discloses the adjacent truth
  ("The gate cannot check attribution, only membership … It does not prove the prose around the
  quote is true") and hand-verified the two statements. That disclosure is accurate, so the frozen
  C1 predicate's word "located" is honest **at gate level**.
- What remains uncovered by any counter: C1's §Sourced claim says "S103/S104's Gate records carry
  this round's access date and ≤25-word located quotes", and `.ufo/waves/round-33/build/R33RowDrafts.md:121,124`
  describe the anchors as "line-labelled `:58`, `:279`, `:280`, `:218`, `:234`". No counter reads
  a line label. `plans/round33_c1_verify.py` reads `source:` lines and host paths
  (`:89-95`) and the entry's literals; `plans/adoption_check.py` reads ids, status, dates and
  `used-by`. Neither opens `sources_adopt.py` quote mode (also kill-rule row 9). So the line labels
  in the landed rows rest on the build seat's hand check — which I independently reproduced as
  true for S103 — not on any executable check.
- Adjacent, not this seat's item: the C2 counters treat `:35-38` / `:72` / `82-83` as literal
  substrings in a lesson file (`plans/round33_defects.py` `check_n5`, `check_n6`) and never resolve
  them against the file they name; the same prose-is-not-parsed shape appears there.

## Limitations

- One capture set (this round's five committed files); the registry-wide count of unverified
  location tokens is a token census, not a per-row re-open of 97 anchors.
- F18's false-negative is measured for a newline-at-a-space wrap only; CRLF↔LF is genuinely
  normalised and was not tested as a failure (the docstring's claim there is consistent with the
  code).
- Fixtures are ephemeral (`/tmp`). The probe set is regenerable from this report: each row is an
  11-cell table row with the named anchor mutation, run with the three flags above; F17's mutation
  is `re.sub(r":{n}\b", f":{n+7000}", row)` over the live `S103`/`S104` lines of `corpus/SOURCES.md`.
- No lane Git/JJ state, index, or sibling repository was read or touched; no tool was installed.
