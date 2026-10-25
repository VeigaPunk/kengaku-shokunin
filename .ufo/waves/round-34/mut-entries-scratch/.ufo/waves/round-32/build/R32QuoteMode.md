# R32QuoteMode — quote validation of drafted S094/S097 rows (round 32 C1)

Seat: executor (leaf). Assignment: validate the drafted S094/S097 rows' quotes against the
captures with `plans/sources_adopt.py --quote-file/--artifact/--url-map`; paste the `QUOTE ...`
summary and exit codes; confirm exit 8 on a deliberately mismatched URL and exit 9 on an unmapped
artifact. Access date for every source opened this round: 2026-10-25.

## Inputs

- Drafted rows: the staged S094 and S097 rows, extracted verbatim (grep on the row-id anchor) from
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` lines 24 and 27 (read-only package) —
  identical to the draft adoption block `/tmp/r32-R32GateBlock/block.md` lines 1–2.
- Captures (scouts' fetches, copied into my scratch, byte-identical):
  - `main.py` — Toolathlon `evaluation/main.py` at pinned commit
    `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb` (14,138 B; md5 `2d1c1a167200534c50c084a9c83f76f7`;
    `/tmp/r32-R32SrcS094a/main.py` = `/tmp/r32-R32SrcS094b/main.py`).
  - `arxiv-2412.05579v2.html` — arXiv 2412.05579v2 abs page (43,661 B; md5
    `6b8d311e3ffa9123441b9c2c0641cdba`; page carries `2412.05579v2` at lines 4/21/24/109/118–119,
    "Submitted on 7 Dec 2024" at line 115).
- Scratch: `/tmp/r32-R32QuoteMode/` (captures in `captures/` subdir; total ≈ 60 KB).
- Url map (`map.json`): `main.py` → `https://github.com/hkust-nlp/Toolathlon`; `arxiv-2412.05579v2.html`
  → `https://arxiv.org/abs/2412.05579` (the URLs the rows cite).

## (a)+(b) Main run — full drafted rows, capture dir, url map

Command:
```
python3 plans/sources_adopt.py --quote-file /tmp/r32-R32QuoteMode/rows.txt --artifact /tmp/r32-R32QuoteMode/captures --url-map /tmp/r32-R32QuoteMode/map.json
```

Output:
```
QUOTE rows=2 spans=3 located=2 found=2 overlong=0 absent=1 malformed=0 cap=25 artifacts=arxiv-2412.05579v2.html,main.py mismatch=0 unmapped=0 urlmap=map.json entries=2
  ok S094 words=9 at main.py quote="def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1)" bound=main.py->https://github.com/hkust-nlp/Toolathlon
  REFUSED S097 absent words=20 quote="This paper presents a comprehensive survey of the LMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations."
  ok S097 words=6 at arxiv-2412.05579v2.html quote="60 pages, comprehensive and continuously updated" bound=arxiv-2412.05579v2.html->https://arxiv.org/abs/2412.05579
exit=7
```

`QUOTE ...` summary line: `QUOTE rows=2 spans=3 located=2 found=2 overlong=0 absent=1 malformed=0 cap=25 artifacts=arxiv-2412.05579v2.html,main.py mismatch=0 unmapped=0 urlmap=map.json entries=2`.
Exit code: **7** (`EXIT_QUOTE_ABSENT`).

Findings:
- S094: quote locates in `main.py` (byte substring; file line 58 holds `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:`) and binds to the cited repo URL → **ok**.
- S097 span 1 (Abstract): **absent** at the pinned v2 revision. The capture (line 30) reads
  "...a comprehensive survey of the **LLMs-as-judges** paradigm..." (two Ls); the drafted row quotes
  "...the **LMs-as-judges** paradigm..." (one L). The quote is therefore not a byte substring of the
  capture; the gate refuses it (exit 7).
- S097 span 2 (Comments): locates in the capture (line 131: `60 pages, comprehensive and continuously updated`)
  and binds to the cited arXiv abs URL → **ok**.

Cross-check of the S097 wording (my own fetch): `curl -fsSL 'https://arxiv.org/abs/2412.05579v2'`
→ `This paper presents a comprehensive survey of the LLMs-as-judges paradigm` (double L) — the capture
is faithful; the draft quote has a one-letter defect. No standalone "LMs-as-judges" exists in either
capture or live page (all occurrences are substrings of "LLMs-as-judges").

## (c) Deliberately mismatched URL → exit 8

Command (S094-only rows, map maps `main.py` to the arXiv URL instead of the Toolathlon repo URL):
```
python3 plans/sources_adopt.py --quote-file /tmp/r32-R32QuoteMode/rows94.txt --artifact /tmp/r32-R32QuoteMode/captures --url-map /tmp/r32-R32QuoteMode/map-bad.json
```
Output:
```
QUOTE rows=1 spans=1 located=0 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=arxiv-2412.05579v2.html,main.py mismatch=1 unmapped=0 urlmap=map-bad.json entries=2
  REFUSED S094 url-mismatch words=9 at main.py quote="def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1)"
exit=8
```
Confirmed: **exit 8** (`EXIT_URL_MISMATCH`).

## (d) Unmapped artifact → exit 9

Command (same S094 row, empty url map `{}` — `main.py` has no map entry):
```
python3 plans/sources_adopt.py --quote-file /tmp/r32-R32QuoteMode/rows94.txt --artifact /tmp/r32-R32QuoteMode/captures --url-map /tmp/r32-R32QuoteMode/map-empty.json
```
Output:
```
QUOTE rows=1 spans=1 located=0 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=arxiv-2412.05579v2.html,main.py mismatch=0 unmapped=1 urlmap=map-empty.json entries=0
  REFUSED S094 unmapped words=9 at main.py quote="def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1)"
exit=9
```
Confirmed: **exit 9** (`EXIT_URL_UNMAPPED`).

## Methodology note

The capture directory must contain only the capture files: a first attempt that also held `rows.txt`
inside the artifact dir made the S097 abstract quote "locate" inside rows.txt itself (the row text
contains the quote), yielding a misleading `unmapped` (exit 9) instead of `absent` (exit 7). With a
clean captures dir the verdict is unambiguous.

## Tools

No tools installed or updated; the gate ran on the repo's existing Python 3 stdlib. (No pacman
transactions; none needed.)

## Verdict

**VERDICT: broken**

As drafted, the S094/S097 rows do not pass quote binding: S094 binds cleanly, but the S097 abstract
quote ("...the LMs-as-judges paradigm...") is not a byte substring of the pinned v2 capture (which
reads "...the LLMs-as-judges paradigm..."), so the row is refused (exit 7). A one-letter correction in
the draft (LMs → LLMs) would make the S097 quote locate and bind, at which point both rows would be
quote-bound.

### Risks / blockers

- The S097 draft quote must be corrected before the row can be admitted under C1 (the C1 kill rule
  refuses a source whose located quote cannot be found at the pinned revision).
- No other issues observed: exit 8 and exit 9 behaviors match the documented gate contract.
