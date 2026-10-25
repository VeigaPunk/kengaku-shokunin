# R30FxQuotes — quote bookkeeping of the six admitted rows and the entry's six `source:` lines

Seat: `L1Kengaku30.R30FxQuotes-3` (leaf; no dispatch, no background jobs). Round 30 FALSIFY wave,
hyaku run 6, 2026-10-25. Item: **the entry's and the six registry rows' quote bookkeeping** — token and
CJK counts per span, whether the 25-word cap is honestly declared for CJK, and nested-quote hazards for
a quote-pair extractor.

Lane writes: this file only. All mutation ran on `/tmp/r30fx-quotes/` copies. No installs, no upgrades,
no pacman transaction. Sources were **not** fetched by this seat; the one capture I read is another
seat's retained scratch (§5).

## 0. Snapshots — the bytes moved under me four times

Both files are untracked/modified, so there is no `git diff` for the entry; every row below is a text
diff against my own copy. **All fourteen quoted spans stayed byte-identical in both files across every
snapshot, and every token count was invariant.** The churn is in the annotations only.

| snapshot (-03) | `corpus/knowledge/contamination-transparency-card.md` | `corpus/SOURCES.md` | what moved since the previous row |
|---|---|---|---|
| S1 04:38→04:40 (measurements) | `9dd5ff1b…a6ce680c` | `1be35142…f60a61e1134` | baseline |
| S2 04:42:08 | `28f5bbda…f7dc75b37e687e` | `43d3e37e…02d17eac4bb94284` | entry S085 legend `23 CJK characters` → `24 characters incl. the fullwidth comma`; **S086 legend `23` → `30` in entry *and* row**; row S081 scope cell rewritten; row S082 title corrected |
| S3 04:43 | `0f2e1614…c5d479d2af7880` | `094e5c18…3b1181b3a78e92b` | **S084 teaches cell `1-13` → `1-7`**; row S083 anchor gains two normalization caveats |
| S4 04:44:46 (final, certified) | `df0b6d41…d29317a0ee251a4` | `094e5c18…3b1181b3a78e92b` | entry S083 line gains the same two normalization caveats |

`plans/sources_adopt.py` (gate) did **not** change: `e9b6bc04…f8610d27d191a195`,
`--selftest` → `SELFTEST cases=14 failed=0`, exit 0.

Certification pass on S4: all 14 spans found verbatim in both the entry's `source:` line and the row's
anchor cell; token counts 22, 6, 18, 11, 17, 14, 19, 3, 7, 1, 3, 1, 3, 1 (identical at S1 and S4).

**Four repairs landed by other seats while I measured** (S086's numeral in both files, the entry's S085
legend, S084's `1-13` range, and the S083 normalization caveats in both files); §1a separates those from
what is still live at S4, which is §2 (the CJK cap is undeclared and does not bind), §3 (the nested-pair
hazard and the entry's unquoted S085 spans), and §4 (four things a green receipt does not cover).

---

## 1. Per-span table (14 documented spans, S4 labels)

`tokens` = `len(s.split())` on the span exactly as the row/entry carries it. `CJK` = ideograph count
(`U+4E00–U+9FFF`) / all-CJK-script count (ideographs + kana + CJK punctuation + fullwidth forms).
`stated` = the parenthetical the anchor cell prints.

| row.span | span (as carried) | tokens | CJK | stated | verdict |
|---|---|---|---|---|---|
| S081.1 | `because it is a property of one run, it must be recorded with the reported score rather than with the benchmark release` | 22 | 0 / 0 | 22 words | **right** |
| S081.2 | `direct, derivative, temporal, distributional, and acquired` | 6 | 0 / 0 | 6 words | **right** |
| S081.3 | `Two variables fall below the prevalence-robust threshold registered in advance: strata reporting and the acquired type introduced here` | 18 | 0 / 0 | 18 words | **right** |
| S082.1 | `Item-level transparency and procedural transparency have opposite effects on benchmark validity.` | 11 | 0 / 0 | 11 words | **right** |
| S082.2 | `transparency should attach primarily to procedures, governance, credentials, and validity testing, not necessarily to live item pools` | 17 | 0 / 0 | 17 words | **right** |
| S083.1 | `a contamination-resistant design by separating the publicly released game engine from hidden card implementations` | 14 | 0 / 0 | 14 words + hyphen-blind caveat (S3) | **right** as a count; locator caveat is real (§4) |
| S083.2 | `We also formalize a practical threat model and refresh protocol that preserves evaluation integrity even if specific cards leak.` | 19 | 0 / 0 | 19 words + whitespace-collapse caveat (S3) | **right** as a count; §4 |
| S084.1 | `目前该方案仅支持 GSM8K 数据集` | 3 | 11 / 11 | 3 whitespace tokens | **right** |
| S084.2 | `目前该方案仅支持 C-Eval, MMLU, HellaSwag 和 ARC 数据集` | 7 | 12 / 12 | 7 whitespace tokens | **right** |
| S084.3 | `但如今开源社区往往只会公开模型参数而非训练数据集` | 1 | 24 / 24 | 1 whitespace token | **right** (no character claim) |
| S085.1 | `“方升”测试体系提出自适应动态测试（Adaptive Dynamic Testing，ADT）方法对大模型进行评测` | 3 | 25 / 28 | 3 whitespace tokens | **right** |
| S085.2 | `采用动态方式构建，保证每次参与测试题目的都不相同` | 1 | 23 / 24 | row: `1 whitespace token, 23 CJK characters`; entry: `1 whitespace token, 24 characters incl. the fullwidth comma` | **right under each file's own counter**, but the row's phrase and the entry's phrase denote different quantities (§1a) |
| S086.1 | `Code LLM 事前学習時の評価データ混入への対策` | 3 | 11 / 17 | 3 whitespace tokens, printed title, one contiguous byte run | **right** (byte-run status is the S086 build report's claim, verified against the capture in §5) |
| S086.2 | `一致したものを一律に混入とみなして除去することには疑問が残る` | 1 | 11 / **30** | S1–S2: `23 CJK characters` (entry **and** row); S3+: `30 CJK characters` | **wrong at S1, repaired at S3**; 30 characters = 11 kanji + 19 kana, no punctuation, so 23 matched no counter (§1a) |

Literal receipts, `python3 -c 'print(len(s.split()))'`: `22`, `1`, `3`, `7`.
`python3 -c 'print(len(s), len(s2))'` → `30 24` for the S086 caveat and the S085.2 sentence — i.e. the
S085 ideograph count (23) plus its fullwidth comma.

### 1a. Numeric defects: two repaired, one definitional defect left standing

**Repaired while I measured (live at S1).** `23 CJK characters` was attached to the S086 caveat in both
files. The caveat is 30 characters (11 kanji, 19 kana, no CJK punctuation), so no reading of "CJK
characters" yields 23 — it was S085.2's ideograph count copied into a span it does not describe, and
`R30SrcS086.md` itself measured "30 chars". Both files now say 30. The S084 **teaches** cell's "CJK
quotes count 1-13 whitespace tokens" was likewise wrong at S1 and now reads `1-7`; my census of every
quoted CJK span in the registry (all 88 rows) returns exactly six spans with token counts 3, 7, 1, 3, 1,
3 — **range 1–7**. The retired `13` is the token count of S084 target (b)'s *untruncated* sentence
(`R30SrcS084.md`: "13 tokens"), a sentence the row deliberately replaces with its 7-token
byte-contiguous prefix.

**Surviving at S4: one phrase, two definitions, adjacent rows.**

- S086's `30 CJK characters` can only mean *all* CJK-script characters (kanji + kana); S085's row's
  `23 CJK characters` can only mean *ideographs only*, because that span's 24th character is `，`
  U+FF0C — a fullwidth/CJK-punctuation character. Under a single definition one of the two rows is
  off: as all-CJK characters S085 should read 24; as ideographs S086 should read 11. The entry's S085
  line now uses a third, unambiguous phrasing (`24 characters incl. the fullwidth comma`); its S086
  line does not, and keeps the ambiguous phrase.
- Neither legend is consumed by anything: the gate counts tokens only (`words()` at
  `plans/sources_adopt.py:272-273`). They are human-facing, and a rechecker diffing entry against row
  now sees agreement on S086 and an unexplained 7-character gap between S085 and S086.

Token counts — the only numbers that enter the cap — are correct in all fourteen spans at every snapshot.

---

## 2. Verdict: is the 25-word cap honestly declared for CJK?

**No. The counts are honest; the rule is not declared where it governs, and it does not bind.**

- The contract has no CJK clause: `corpus/QUALITY.md:31-33` — "an anchored quote (≤25 words, with
  location; the length rule is SOURCES contract v1 rule 1)"; `corpus/SOURCES.md:7` — "a ≤25-word quote
  per row"; the gate pins `QUOTE_WORDS = 25` (`:265`) and `words(text) = len(text.split())`
  (`:272-273`) with no script or locale branch.
- The entry states no general rule. It labels each CJK span "(N whitespace tokens)" — three of six
  `source:` lines, and two of those also carry a character legend — which names the counter but not the
  consequence, and never says the cap fails to constrain a Chinese or Japanese quote.
- The one registry cell that does state the consequence (S084 teaches, now `1-7`) is a `teaches` cell,
  not a contract line, and it is where the wrong `1-13` lived until S3.
- **Measured inertness.** The live gate accepts a **1200-character** pure-CJK span with
  `words=1 overlong=0`, exit 0 (`/tmp/r30fx-quotes/cjk1200-row.txt` + `cjk1200-art.txt`). A 147-character
  mixed span with seven Latin dataset names counts 12 tokens; a 289-character span counts 1. So
  "≤25 words" bounds a CJK quote's *length* at nothing and bounds only the Latin tokens it embeds. Any
  future gate that claims the Q3 cap coverage should state the character ceiling it actually enforces;
  none is stated in the entry, the contract, or the gate.

---

## 3. Verdict: nested-quote hazards

**No nested ASCII quote pair exists in any of the six anchor cells at S4** — all six are parity-clean
and the extractor returns the intended spans: S081 6 marks/3 spans, S082 4/2, S083 4/2, S084 6/3,
S085 4/2, S086 **2/1**. S085 is the only cell that nests a quote inside a quote, and it nests
**fullwidth** marks (`“方升”`), which survive ASCII pairing; NFKC leaves them as U+201C/U+201D (in that
cell NFKC changes only `（`→`(` and `，`→`,`). So the hazard is **latent in the tool, not realized in
these rows**.

Two reasons not to dismiss it:

1. **The gate's only structural guard is parity.** It refuses an odd `"` count (`:288-289`) and nothing
   else, then pairs greedily at `:290`. A nested ASCII pair is *even*, so it is mis-paired and each
   fragment is validated separately. Mutant receipt (`/tmp/r30fx-quotes/mut/rows6-nested.txt`, S083.2
   rewritten to `"We also formalize a "practical" threat model … leak."`, artifact holding both
   fragments):

   ```
   QUOTE rows=6 spans=14 located=2 found=2 … cap=25
     ok S083 words=4  at fragpair.txt quote="We also formalize a "
     ok S083 words=14 at fragpair.txt quote=" threat model and refresh protocol that preserves evaluation integrity even if specific cards leak."
   ```

   The 19-word sentence is split into 4 + 14 words, both `ok`; the lost word (`practical`) and the
   18-of-19 coverage are invisible in a receipt that counts spans, not sentences.
2. **The entry's S085 spans carry no ASCII quotes at all** (`source: S085` uses `“…”` directly), so a
   quote file built from the entry's own lines yields **0 spans for S085** and 1 for S086 — 11 of 14.
   The entry's counts are unreachable by the extractor its own `recheck:` line invokes.

---

## 4. What a green gate receipt does NOT cover on these six rows

Four measured gaps, each with a receipt. These are the bookkeeping consequences a reader must know
before treating `EXIT=0` as evidence.

1. **13 of 14 spans are gate-visible.** `--quote-file` over the six rows, `--artifact` over a directory
   holding all fourteen spans verbatim → `QUOTE rows=6 spans=13 located=13 found=13 … EXIT=0`. The
   missing one is S086.2: the caveat is unquoted in both the entry and the row (the row says it is
   "located but not byte-contiguous"), so the CG4-load-bearing quote is the single span the C3 gate
   cannot check, and the entry's `recheck:` line would emit a green that says nothing about it.
2. **A zero-row quote file greens silently.** `--quote-file` over the entry's six `source:` lines prints
   `QUOTE rows=0 spans=0 … EXIT=0`; an empty file prints the same, exit 0. No selftest case covers
   `rows=0`, so "the gate was re-run and passed" is indistinguishable, by exit code, from "the gate was
   handed a file that is not a registry".
3. **The S083 spans are not locatable by the matcher the gate implements.** The row and entry now
   declare it (S3/S4): S083.1 needs a "hyphen-blind compare" and S083.2 a "whitespace collapse". The
   gate does neither — `normalize_text` is CRLF-only (`:274-276`) and `locates` is a plain substring
   test. Against the retained capture (`/tmp/r30-R30SrcS083/`): `p1raw.txt` prints the sentence
   hyphenated across line breaks (`a contamination-\nresistant … publicly re-\nleased … imple-\nmentations`),
   `p1.dehy.txt`/`p1.join.txt` delete the hyphen (`contaminationresistant`), so the span **as carried**
   (which keeps the hyphen) is absent from every extracted text file.
4. **…and it "locates" only in the verifying seat's own script.** Running the gate over that whole
   scratch directory returns
   `ok S083 words=14 at verify.py` and `ok S083 words=19 at p1.dehy.txt` (exit 7 overall, the other rows
   absent). `verify.py` is the seat's verification script, which embeds the sentence as a string
   literal: `q1 in verify.py` is `True` while `q1 in p1.txt/p1raw.txt/p1.dehy.txt/p1.join.txt` is
   `False` for all four. A receipt that prints `at verify.py` has validated the lane's own copy, not
   the source — the laundering loop QUALITY Q5 forbids. The remedy is a rule, not a code change: a
   quote-mode receipt must name a file whose bytes are the fetched capture.

---

## 5. Entry ↔ row drift that survives, and what I did not test

- Span text is byte-identical between entry and row for every ASCII-quoted span at S4 (S081 3, S082 2,
  S083 2, S084 3, S086 1). Remaining annotative differences: the entry's S084 locator says "html lines
  344 and 397" and gives **no locator for its third quote** (the row has `line 315`); the entry's S085
  drops the row's "the fullwidth quotes are the report's own"; the entry's S086 says "text-layer lines
  80-81, located only on newline-unwrapped extraction" where the row says "spans extraction lines
  78-81, so it is reported as located but not byte-contiguous".
- That S086 line-range difference is **not** a defect: against the capture, the full sentence
  `しかし、表 1 のように … 疑問が残る。` (85 chars) occupies raw lines **78–81** and the quoted caveat
  clause occupies **80–81**. Each file is right about its own object; neither names the object.
- Capture provenance, checked because it is the only external byte set I touched:
  `/tmp/r30-R30SrcS086/Q2-11.raw.txt` sha256 `88b4201d…60fc1f` and `Q2-11.unwrapped.txt`
  `887adab8…2b8a9c` match `R30SrcS086.md`; `Q2-11.pdf` md5 `08d383fbd3faf659ac16f666dd0a5de6` at
  371155 bytes matches the build report's md5 and size; `Q2-11.refetch.pdf` is byte-identical. Caveat:
  `len=30`, `in raw: False`, `in unwrapped: True`, lines 80–81.
- Not tested here: whether any span is present in its source (other seats' claims; §4.3 is the one
  place I could test it, and it failed for S083.1 under the gate's matcher); whether the S085/S086
  character legends are consumed by any check (they are not); anything about the other 82 rows beyond
  the CJK-span census in §1a.

---

## 6. Reproduce

```
python3 plans/sources_adopt.py --selftest                                  # cases=14 failed=0, exit 0
python3 plans/sources_adopt.py --quote-file /tmp/r30fx-quotes/rows6-final.txt \
        --artifact /tmp/r30fx-quotes/art                                   # spans=13 (not 14), exit 0
python3 plans/sources_adopt.py --quote-file /tmp/r30fx-quotes/empty.txt \
        --artifact /tmp/r30fx-quotes/art                                   # rows=0, exit 0
python3 plans/sources_adopt.py --quote-file /tmp/r30fx-quotes/mut/rows6-nested.txt \
        --artifact /tmp/r30fx-quotes/mut/fragpair.txt                       # 19-word span → 4+14 fragments
python3 plans/sources_adopt.py --quote-file /tmp/r30fx-quotes/cjk1200-row.txt \
        --artifact /tmp/r30fx-quotes/cjk1200-art.txt                        # 1200-char CJK span: words=1
python3 plans/sources_adopt.py --quote-file /tmp/r30fx-quotes/rows6-final.txt \
        --artifact /tmp/r30-R30SrcS083                                      # S083.1 located only at verify.py
```

`/tmp/r30fx-quotes/` holds: `S08*.row.txt` (S1 rows), `rows6.txt` (S1 six rows), `rows6-final.txt` (S4),
`entry-sources.txt` (the entry's six `source:` lines), `art/all14.txt` (all fourteen spans),
`mut/` (the nested-pair mutant and its two artifacts), `cjk*/` (the cap probes). Every span in
`art/all14.txt` was verified verbatim in **both** its entry `source:` line and its row's anchor cell at
S4 (§0 certification); runs 2 and 5 above were re-executed against the S4 rows and printed
`spans=13 located=13` (exit 0) and `words=1` (exit 0) respectively.

No `VERDICT:` line is emitted here: this seat is neither the source re-read nor the complete-set
review, the two seats `plans/gate_timing_check.py` machine-reads.
