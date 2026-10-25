# R30FxC3CLI — quote mode over S081–S086 against fresh captures

Seat: `L1Kengaku30.R30FxC3CLI-3` (leaf). Round 30 falsify wave, hyaku run 6, 2026-10-25.
Scope: attack the six landed registry rows S081–S086 with the landed quote gate, on captures
I made myself. No lane edits (only this report). Scratch: `/tmp/r30fx-c3cli/`.
Nothing installed: no `uv tool`, `npx`, binary download or package transaction was run.

Candidate path: `corpus/knowledge/contamination-transparency-card.md`

VERDICT: FAIL

(The FAIL is about the six rows' anchors, not about the gate's own selftest, which passes.
Three of thirteen quoted spans cannot be located byte-wise in any capture I produced; one
row carries two numeric anchor errors. Details in §4 and §6.)

Tool identity under test
- `plans/sources_adopt.py` sha256 `e9b6bc044bd5337565d78701c13287eba163c90b13199f4cf8610d27d191a195`
- `python3 -V` → `Python 3.14.8`; `pdftotext -v` → `pdftotext version 26.08.0` (Poppler)
- `plans/sources_adopt.py --selftest` → `SELFTEST cases=14 failed=0` (exit 0, re-run by me)

## 1. Exact commands

Row extraction (lane read-only; six rows kept byte-identical, sorted by id):

```
python3 - <<'PY'
from pathlib import Path
src = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md')
want = {f'S08{i}' for i in range(1,7)}
rows = [l for l in src.read_text(encoding='utf-8').splitlines(keepends=True)
        if l.startswith('| S') and l.split('|')[1].strip() in want]
rows.sort(key=lambda l: l.split('|')[1].strip())
Path('/tmp/r30fx-c3cli/rows/S081-S086.txt').write_text(''.join(rows), encoding='utf-8')
PY
```
→ 6 rows, each 11 cells, sha256 `d84fdd4e30b245749bbf2a167555ce80e4aa6c92235c6cb857dc80d695184e35`.
Per-row files `/tmp/r30fx-c3cli/rows/single/S08{1..6}.txt` are one line each (same bytes).

Captures (`curl -sSL --max-time …`, then PDF text extraction):

```
curl -sSL -o cap/S081/raw/arxiv-abs-2608.29463.html              https://arxiv.org/abs/2608.29463
curl -sSL -o cap/S082/raw/arxiv-html-2607.01254v2.html           https://arxiv.org/html/2607.01254v2
curl -sSL -o cap/S082/raw/arxiv-abs-2607.01254.html              https://arxiv.org/abs/2607.01254
curl -sSL -o cap/S083/raw/eacl-353.pdf                           https://aclanthology.org/2026.findings-eacl.353.pdf
curl -sSL -o cap/S084/raw/opencompass-contamination_eval.html    https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html
curl -sSL -o cap/S085/raw/caict-P020240711534708580017.pdf       https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711534708580017.pdf
curl -sSL -o cap/S086/raw/anlp-Q2-11.pdf                         https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf
pdftotext cap/S083/raw/eacl-353.pdf                     cap/S083/text/paper.txt
pdftotext cap/S085/raw/caict-P020240711534708580017.pdf cap/S085/text/report.txt
pdftotext cap/S086/raw/anlp-Q2-11.pdf                   cap/S086/text/paper.txt
```

PDF extraction record — exact command, version, flags, exit:
| row | PDF | command | flags | pdftotext exit | stderr |
|---|---|---|---|---|---|
| S083 | `eacl-353.pdf` | `pdftotext <in> <out>` (26.08.0) | none (default, UTF-8, form feeds kept) | 0 | — |
| S085 | `caict-P020240711534708580017.pdf` | `pdftotext <in> <out>` (26.08.0) | none | 0 | — |
| S086 | `anlp-Q2-11.pdf` | `pdftotext <in> <out>` (26.08.0) | none | 0 | `Syntax Error (366527): insufficient arguments for Marked Content` (warning only; text produced) |

Gate invocation (per row, and once over all six):

```
python3 plans/sources_adopt.py --quote-file rows/single/S081.txt --artifact cap/S081/raw
python3 plans/sources_adopt.py --quote-file rows/S081-S086.txt  --artifact cap/all
```

Capture hashes (sha256, my bytes):
```
S081/raw/arxiv-abs-2608.29463.html            4c81bd3c180736318ed03e31968fa4d109b94025ec596203dbc4e963b396908a
S082/raw/arxiv-html-2607.01254v2.html         82a5c5c6e9de647ee3fa7fb4c13c6d7b6decbaef5ed717b59c18d457d1371ed5
S083/raw/eacl-353.pdf                         662c2235680e475c1880b1a4486a8e001eb746c6d992384e1400d01287b3dfe4
S084/raw/opencompass-contamination_eval.html  c4447d93c6945d2c68dbffac8274b3adc4aa2b6e510120c33eea1de966b7ec23
S085/raw/caict-P020240711534708580017.pdf     e551e2e0956c314507ab240b3ca19ce47aed88640a98e6c316bd4efc6bbc131c
S086/raw/anlp-Q2-11.pdf                       c3706aca80aa8aeee7fa39d3a5988f238a138c508c0ca5fe5c107c50d7feb303
S083/text/paper.txt                           1c2292a8c37045bc0954752deaf037cfbc45e1305d11e633d9c8dbf2eb71ddb6
S085/text/report.txt                          bc6a20d6216b453075cac294281754513c8c536aa1e356a0c328925cfcce1ae4
S086/text/paper.txt                           88b4201d81b2d867c7de66390b2bbeee120bc6779f83df10956362391160fc1f
```

## 2. Per-row exit class (real captures)

| row | artifact class | exit | class name | gate line 1 |
|---|---|---|---|---|
| S081 | HTML abs page | 0 | EXIT_OK | `rows=1 spans=3 located=3 found=3 overlong=0 absent=0 malformed=0` |
| S082 | HTML full text (v2) | 0 | EXIT_OK | `rows=1 spans=2 located=2 found=2 overlong=0 absent=0` |
| S083 | raw PDF bytes | 2 | EXIT_QUOTE_UNREADABLE | `--artifact holds no UTF-8 text (unreadable: eacl-353.pdf)` |
| S083 | pdftotext text | 7 | EXIT_QUOTE_ABSENT | `spans=2 located=0 found=0 absent=2` |
| S084 | HTML docs page | 0 | EXIT_OK | `spans=3 located=3 found=3` |
| S085 | raw PDF bytes | 2 | EXIT_QUOTE_UNREADABLE | `--artifact holds no UTF-8 text (unreadable: caict-…pdf)` |
| S085 | pdftotext text | 7 | EXIT_QUOTE_ABSENT | `spans=2 located=1 found=1 absent=1` |
| S086 | raw PDF bytes | 2 | EXIT_QUOTE_UNREADABLE | `--artifact holds no UTF-8 text (unreadable: anlp-Q2-11.pdf)` |
| S086 | pdftotext text | 0 | EXIT_OK | `spans=1 located=1 found=1` |
| all six | six distinctly named captures in one dir | 7 | EXIT_QUOTE_ABSENT | `rows=6 spans=13 located=10 found=10 overlong=0 absent=3 malformed=0 cap=25` |

Exit 6 (`EXIT_QUOTE_TOO_LONG`) never fired: the longest span in the six rows is S081 span 1 at
22 words; the cap is 25. Exit 4 (`EXIT_MALFORMED`) never fired: every anchor cell has balanced
`"` (S086 has exactly one span, S081 three).

Rows the gate refuses on real captures: **S083** (both spans, on pdftotext text) and **S085**
(span 1, on pdftotext text). Under a raw-bytes artifact, S083, S085 and S086 are refused at the
artifact layer (exit 2) before any row is read.

## 3. Span-level verdicts (13 spans, own capture, own extraction)

| row | span | words | chars | CJK chars | verdict | evidence |
|---|---|---|---|---|---|---|
| S081 | 1 | 22 | 119 | 0 | located | abs HTML line 124 (`<span class="descriptor">Abstract:</span>`); also lines 30 (`og:description`) and 41 |
| S081 | 2 | 6 | 58 | 0 | located | same file |
| S081 | 3 | 18 | 134 | 0 | located | same file |
| S082 | 1 | 11 | 96 | 0 | located | v2 HTML line 855, inside §7.3 (heading at line 746) |
| S082 | 2 | 17 | 133 | 0 | located | v2 HTML line 901, directly under §8.2 heading |
| S083 | 1 | 14 | 113 | 0 | **ABSENT** | default extraction has `contaminationresistant` (hyphen dropped at the line break); `-layout` has `contamination-` + newline — no mode yields `contamination-resistant` |
| S083 | 2 | 19 | 128 | 0 | **ABSENT** | present in default text only after deleting the newline between `threat` and `model`; also absent in `-layout` (column padding) |
| S084 | 1 | 3 | 18 | 11 | located | HTML line 344 |
| S084 | 2 | 7 | 42 | 12 | located | HTML line 397 |
| S084 | 3 | 1 | 24 | 24 | located | HTML line 315 |
| S085 | 1 | 3 | 57 | 25 | **ABSENT** | sentence exists but wraps over extraction lines 1041→1042→1043; locates only when newlines are deleted |
| S085 | 2 | 1 | 24 | 23 | located | exact, one line |
| S086 | 1 | 3 | 26 | 17 | located | text line 3; PDF p.1, footer `― 797 ―` |

Overlong spans: **none** (0/13). Absent spans: **3/13** (S083×2, S085×1), all three caused by
line wrapping or end-of-line hyphenation in the extracted text, not by paraphrase.

Cross-document bleed check: each row was also run against a directory holding only the *other
five* captures. All six exited 7 with `located_elsewhere=0`, so no span in these rows is
satisfied by a sibling source and the aggregate run's 10 `ok` lines are genuine.

## 4. Findings

F1 — The gate's newline normalization does not do what its docstring claims.
`locates()` docstring: "Both sides are newline-normalised, so a quote taken across a line break
in an LF capture still locates in the same document captured with CRLF." True only for CRLF↔LF.
A quote whose *document text* contains a hard newline (every PDF and every wrapped sentence) is
refused, because the needle carries a space where the haystack carries `\n`. Measured: S083
span 2 and S085 span 1 both locate after `t.replace("\n","")` and are absent without it. This
is the largest real-capture refusal class (2 of 3 absences) and it is invisible in the receipt:
the row is reported "absent", which reads as "the author paraphrased".

F2 — The verdict depends on unpinned extraction flags, and the gate pins nothing.
Same PDF, same quote, different flags: default → `contaminationresistant`; `-layout` →
`contamination-` + newline; `-raw` → the `-layout` behaviour. S083 span 1 is refused in every
mode tested, but for a different reason per mode. Nothing in `sources_adopt.py` records a
`pdftotext` version, flags, or a dehyphenation policy, and nothing in the row records which
extractor its quote was read from. A row's byte verdict is therefore a verdict on an unnamed
renderer.

F3 — A raw-bytes artifact can never test a PDF row, and the refusal is at the artifact layer.
All three PDFs fail UTF-8 decoding — at byte 10 in each (`0xd0`, `0xe2`, `0xe2`) — so a raw run
exits 2 with no row read at all. Honest answer to the assigned question: **yes**, a raw-bytes run
refuses exactly the bytes a text-extraction run accepts (S086: exit 2 raw vs exit 0 on text),
and no cheaper path exists in the gate to close that gap.

F4 — Unreadable files are silently dropped when anything else loads.
`load_artifact()` reports `skipped` only inside `if not loaded`. Demonstrated: a directory with
`paper.txt` (S086 text) plus two real PDFs exits 0 and prints `artifacts=paper.txt` with no
mention of the two skipped PDFs. A caller cannot tell from the receipt that part of the artifact
set was unreadable.

F5 — The gate does not bind a row to its own artifact.
`--artifact` is caller-supplied and every UTF-8 file under it is one search space, so the only
evidence of correct binding is the `at <name>` in the detail line. In the six-row aggregate run
that binding happened to be correct for all 10 located spans (verified by the bleed test in §3),
but a quote present in the wrong sibling document would be reported `ok`. Per-row invocations
are the only safe form; the aggregate form cannot detect mis-binding.

F6 — The 25-word cap is toothless on CJK, exactly as S084's teaching says.
Measured word counts for the CJK spans: 3, 7, 1 (S084), 3, 1 (S085), 3 (S086) — max 7. S085
span 1 is 57 characters / 25 CJK characters and still counts as 3 words, so a quote an order of
magnitude longer than the "25-word" limit passes. The cap is a whitespace-token counter, not a
length limit; S084's anchor states this correctly and it survives falsification.

F7 — The location prefix in an anchor cell is never checked.
Quote mode reads only `"…"` spans (column 5). `p.1 (printed 6710)`, `line 855`, `p.32 (printed
27)` are never validated, so a row could cite a wrong page and still exit 0. I checked them by
hand (§6); one of them is wrong.

## 5. Gate behaviours that hold up (not falsified)

- Exit-code ordering and separability: 2 before 4 before 6 before 7, observed directly (2 on
  raw PDFs, 7 on absent spans, 0 on located), and every refused row is still named.
- `--selftest`: `cases=14 failed=0` on my own run, including `quote-overlong-refused`,
  `quote-absent-refused`, `quote-located-accepted`, `quote-boundary-25-accepted`.
- Byte-substring strictness: no paraphrase passes. All three absences are wrapping artifacts,
  which means the gate is strict where it should be strict; it is blind where text is wrapped.
- Locate determinism: `rglob` + sorted order gives a stable `at <name>` (verified by re-running
  the aggregate twice with identical output).
- Registry facts used by the claims: `corpus/SOURCES.md` has 88 rows, 88 unique ids, S081–S086
  each exactly once; `corpus/knowledge/contamination-transparency-card.md` exists (15 901 bytes)
  and cites all six ids.

## 6. Anchor fidelity re-check (does the *location* survive?)

| row | claimed | my capture | holds? |
|---|---|---|---|
| S081 | abs page HTML line 124 | line 124 contains the full 22-word span (first textual occurrence is line 30 in `<meta property="og:description">`, abstract body at 124) | yes |
| S082 | §7.3 line 855 | line 855, §7.3 heading at 746 | yes |
| S082 | §8.2 line 901 | line 901, §8.2 heading immediately above | yes |
| S082 | "the abs page for 2607.01254 carries neither phrase" | captured abs page (43 552 B): neither phrase, and not even the strings `item-level transparency` / `procedural transparency` case-insensitively | yes |
| S083 | p.1 (printed 6710) | PDF page 1 of 16, footer `6710` | yes |
| S084 | html lines 344 / 397 / 315 | 344 / 397 / 315 exactly | yes |
| S085 | p.32 (printed 27) | PDF page 32 of 53; the report's own TOC puts §(二)"方升"自适应动态测试方法 at printed 27; the footer digit itself is not cleanly recoverable from the text layer (page 32 ends with a lone `2`) | page yes, printed number consistent-by-TOC |
| S086 | p.1 (printed 797) | PDF page 1 of 7, footer `― 797 ―` | yes |
| S086 | caveat "spans extraction lines 78-81" | the sentence `一致したものを一律に混入とみなして除去することには疑問が残る` occupies extraction lines **80–81** (offset 1419 in the newline-stripped text) | **no — 2-line drift** |
| S086 | caveat "(1 whitespace token, 23 CJK characters)" | 30 characters (all CJK/kana: 一致したものを一律に混入とみなして除去することには疑問が残る) | **no — undercounted by 7**; 23 is S085 span 2's count, apparently copied |
| S081/S082/S083/S085 | "N words" per span | 22/6/18, 11/17, 14/19, 3/1 — all as printed by the gate | yes |
| S084 | "3 / 7 / 1 whitespace tokens" | 3 / 7 / 1 | yes |

S086 has one further coverage hole: its caveat sentence is deliberately left **outside** the
quotes, and its title span is the only quoted span. Quote mode therefore reported S086 green
(`spans=1 located=1`) while the second half of the same anchor cell — the half the row's
`teaches` cell actually leans on for the false-positive caveat — was never tested. A green
`located=found` for a row proves only that the quoted spans locate, never that the anchor cell
is verified.

## 7. What would repair the two real refusals (not applied; lane is read-only here)

1. Give `locates()` a second, recorded comparison mode: newline-and-hyphen-normalised
   (`\n` → nothing, `-\n` → nothing) reported as a **separate, labelled** result (`located-wrapped`)
   so the strict byte result stays strict and the wrapping artifact stops masquerading as a
   paraphrase.
2. Require the row (or the run) to name its extractor: `pdftotext 26.08.0, default flags` is the
   missing half of every PDF verdict.
3. Surface `skipped` unconditionally in the receipt line.
4. Fix S083 spans 1–2 and S085 span 1 to their byte-exact forms, or re-anchor them on a
   text-extraction receipt that is committed alongside; fix S086's `23 CJK characters` → 30 and
   `lines 78-81` → `lines 80-81`.

## 8. Limits of this falsification

- Captures are 2026-10-25 fetches; the arXiv abs page and the documents are live and can change.
  Line-number anchors on live HTML (S081, S082, S084) are stable today, not permanently.
- I did not test an alternate PDF extractor (no `mutool` on this host; `qpdf` only rewrites, it
  does not lay out text). The claim that another extractor would preserve `contamination-` rests
  on `pdftotext -layout`, which does.
- I did not run the six rows against the whole 88-row registry, nor judge the C1 card's prose;
  this report covers quote-mode operability and the six rows' anchors only.
- The three absences are all wrapping/hyphenation artifacts, so I judge the quote *content*
  faithful and the byte *anchor* unverifiable — that distinction is the finding, not a verdict on
  whether each paraphrase is a fair reading of the source.
