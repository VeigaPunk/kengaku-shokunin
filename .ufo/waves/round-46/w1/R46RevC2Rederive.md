# R46 C2 leg A — base anchor-line re-derivation

## Reproduction and scope

I cloned the lane into my seat scratch, verified the clone root, and detached it at freeze `fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f`. `git -C "$S/lane" diff --stat 64ba8385ea10af1b78d367dcb242b92d97062af7 fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f -- corpus/SOURCES.md` printed no diff; the audited registry is the round-45 base. `sha256sum plans/anchor_line_check.py` in that clone: `35d02dc55393bea18787e35cc2827cbab65f2d645b81a3c1946722065a4fdedf`, matching the frozen tool.

I ran the tool read-only on that base clone inside the required envelope; complete command, ENVELOPE start/end lines, all output, and exit status are preserved at `.ufo/waves/round-46/w1/R46RevC2Rederive/anchorline-base.txt`. The envelope ended `exit=1 ... unchanged`. Its summary is `ANCHORLINE rows=149 cited=39 captured=35 uncaptured=4 defective=8 repaired=0 live=8 cells=14`; it reports `UNCAPTURED S093, S103, S104, S110` and the eight `ROW` findings below.

Independent inventory command: `python3 /fast/scratch/hyaku/kengaku-r46/R46RevC2Rederive/inventory.py /fast/scratch/hyaku/kengaku-r46/R46RevC2Rederive/lane`. Output: 578 tracked evidence files / 505 distinct digests; SOURCES header has 11 columns; 149 census rows; 39 ASCII `:N "quote"` rows. The corresponding manual check invoked `sed -n Np` on digest-named captures and `wc -w` on the quote snippets; its bounded receipt is `.ufo/waves/round-46/w1/R46RevC2Rederive/hand-audit.txt`.

## Count comparison

All eight rows flagged by the gate agree with the manual line/range/word observations. But the gate misses a ninth defective captured row, S140; therefore the full hand-found defect-row agreement is **8/9**, not 8/8.

| Row | Manual check against digest-named capture | Gate comparison |
|---|---|---|
| S108 | `:87` quote is present; `wc -w` 5, claimed 6; range 8–90 is within 90 split lines. | agrees: words |
| S149 | `:18` quote present; 4 words as claimed; range ends at 19 while capture has 18 split lines. | agrees: range |
| S150 | `:9` quote present; 9 words, claimed 8; range 1–9 valid. | agrees: words |
| S151 | `:30` quote present; 3 words, claimed 4; range ends at 45 while capture has 43 split lines. | agrees: range + words |
| S152 | `:15` is blank; quote absent; 3 words, claimed 4. Human range 1–16 contains the citation and file has 20 split lines, but the gate's extension-required RANGE_RE does not parse bare `Dockerfile:1-16`. | agrees: line + words |
| S153 | `:28` is `echo 0 > /logs/verifier/reward.txt`, not the quoted `echo 1`; quote is 4 words, claimed 6; range ends at 31 while capture has 29 split lines. | agrees: line + range + words |
| S154 | quote has 5 words as claimed, but `:44` is beyond the 33-split-line capture; range ends at 46. | agrees: line + range |
| S155 | `:63` quote is present; 4 words, claimed 3; range ends at 70 while capture has 68 split lines. | agrees: range + words |
| **S140** | `:12` quote `keys = ["0x68e63", ...]` is not a substring of line 12 (`keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]`); quoted snippet is 4 whitespace words, claimed 9. | **missed**: no `ROW S140` output |

S140 is the concrete inner-quote regex failure. `QUOTE_RE` stops at the quote after `0x68e63` because the following comma satisfies its lookahead; the extracted group is only `keys = ["0x68e63`, and no `(9 words)` follows that partial match. Thus the partial substring passes the line test and its word claim is never checked. The regex probe output was `S140: quote_matches=[('12', 'keys = ["0x68e63', None)] range=('1', '97')`.

The other 26 captured rows recognized by the tool had no line/range/word defect on manual check. I also hand-checked the six curly-quoted captures S115–S120 (listed below as row-level false negatives); each line, stated range, and word count is correct.

## Rows the tool cannot parse as human line citations

I count a row-level false negative when its anchor clearly locates a quoted source passage at a line but the tool finds no `QUOTE_RE` citation for that row. This includes alternate line-locator syntax, not page-only citations. There are **18**:

- `corpus/SOURCES.md:99` S077 (`line 95`, `lines 29 and 31`); `:100` S078 (`line 99`, `line 75`); `:101` S079 (`task.toml line 1`, 15, 18–19, 22); `:102` S080 (`README.md line 27`); `:105` S081 (`line 124`); `:106` S082 (`lines 855, 901`); `:108` S084 (`html line 344, 397, 315`). These use `line N`/`lines N`, not `:N "quote"`; no full digest token is supplied in these anchors, so the named-capture check cannot be performed.
- `corpus/SOURCES.md:111` S092 has `verifier.py:168: "Discard stale rewards…"` and `verifier_mode.py:31` with a backtick quote; the extra colon/backticks defeat `QUOTE_RE`. No full digest token is supplied.
- `corpus/SOURCES.md:113` S100 uses `README.md line 46: "uv run harbor run …"`; no full digest token is supplied.
- `corpus/SOURCES.md:129` S114 uses `issue body line 39 "…"`. Unlike the preceding unpinned rows, it names a capture: its SHA is `c217d37253c89a71d6cc4d1c14f588c02ce49039cb1118dd3694150cf4c64193`; `sed -n 39p` contains the quote and `wc -w` gives 14. The tool still misses the row because the locator is `line 39`, not `:39`.
- `corpus/SOURCES.md:130-135` S115–S120 use curly opening/closing quotes around `:N` citations, which the ASCII-only `QUOTE_RE` does not match. Their capture line/range/word checks all pass: S115 `:46`, 7 words; S116 `:9`, 17; S117 `:16`, 9; S118 `:4`, 18; S119 `:98`, 12; S120 `:7`, 9.
- `corpus/SOURCES.md:139` S124 gives `pr245-body.md:11` in a locator parenthesis, then the quoted text later in the anchor. Its digest-named `corpus/evidence/round41/pr245-body.md` has 50 split lines; `sed -n 11p` contains the quote and `wc -w` gives 14. The separated locator/quote is not parsed.
- `corpus/SOURCES.md:143` S128 says `issue body ... (body line 3)` and then quotes the sentence. No SHA token is supplied, so there is no capture to follow.

Page locators such as S083/S085 (`p.1`, `p.32`, `p.34`) are not counted as line citations. S086's `lines 78-81` describes an unquoted sentence, so it is not a quoted-line false negative. Within S093 (already reported `UNCAPTURED` because `:33` and `:214` are parsed), the separate backtick citation at `:71` is also not parsed; it is an additional missed citation inside an already-counted row, not an extra row-level false negative.

## Additional range-parser gap

S112's anchor has `verify.sh:49, :57-63, :62 "echo …"`. The quote at `:62` is checked, but `RANGE_RE` returns no range: `:57-63` is detached from the filename. By eye, 57–63 contains 62 and the capture has 92 split lines (91 `wc -l` because there is no final LF), so this is not an additional bad range; it is a range the gate does not actually check. S152's bare `Dockerfile:1-16` similarly evades RANGE_RE, but its citation remains within range.

## Residual risk and verification gaps

The frozen tool's reported 8-row count is accurate for the rows its ASCII regex recognizes, but it is not a complete human line-citation census: S140 is an additional captured defect, 18 human line-citation rows are unparsed at row level, and some human range forms are not checked. Four tool-recognized rows remain uncheckable by digest (`UNCAPTURED`); S110's visible SHA token is not a full 64-hex token accepted by the digest index. I ran the requested anchor-line tool, not the full round46 C2 counter.

VERDICT: anchorline-base-rederived-agree-8/9-false-negatives-18
