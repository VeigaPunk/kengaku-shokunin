# R30RowSchema — exact registry rows S081–S086 for the kengaku round-30 append

Seat: L1Kengaku30.R30RowSchema (leaf scout, 2026-10-25). Question: the exact 11-cell `corpus/SOURCES.md`
lines this lane must append for S081–S086 under C1, and every cell that differs from the staged campaign
package. Scratch: `/tmp/r30-R30RowSchema/`. No tool installed or upgraded.

**Verdict.** The six rows below are schema-valid, census-clean, and accept-identical under the standing
adoption gate, and every quote in them is a strict byte-substring of an artifact I fetched today — verified
by the round's own new quote validator (23 spans, `located=23 found=23 absent=0 malformed=0`, exit 0), and
again against the landing seat's artifact set (exit 0). Four of the six staged rows could not have been
appended as shipped: `used-by` pointed at two knowledge entries that do not exist (permanent census `E11`),
and all six carried a prose `recheck` (`E09`).

**State changed under this seat.** When I started, `corpus/SOURCES.md` held 82 rows and no S081–S086. While
I worked, another seat landed the six ids (registry now 88 rows, S081–S086 at lines 107–112) and the entry
`corpus/knowledge/contamination-transparency-card.md`. §6 reports that landing state, the cell-level diff
against this derivation, and the two landed anchor cells the round's own quote gate **refuses** — with the
repair bytes, proven.

## 1. The six rows (exact bytes, as derived and verified by this seat)

```
| S081 | Benchmark Contamination: A Taxonomy Organized by Defeated Mitigation — https://arxiv.org/abs/2608.29463 | paper | B | the four-field contamination disclosure protocol (F1 strata, F2 elicitation, F3 five contamination types, F4 regeneration), its JSON Schema and validator, and the rule that evaluation-time acquired contamination is reported with the score rather than with the benchmark release — for the preprint's own text, which was not peer reviewed at the time of opening | arXiv 2608.29463 (preprint; abstract page and PDF fetched 2026-10-25), § Abstract: "because it is a property of one run, it must be recorded with the reported score rather than with the benchmark release" and, on the protocol's accepted entry values, "is a valid entry, released under CC BY 4.0 with a JSON Schema, a validator, and worked examples"; PDF Table 3, caption "The eight coded variables", variable rows "F1 Strata", "F2 Elicitation", "F3 t5 Acquired", "F4 Regeneration" | a contamination card needs four fields — strata, elicitation budget, contamination type, regeneration status — must accept unknown as a valid entry, and must separate the score-side artifact from the benchmark-release artifact, because contamination acquired during a run is a property of that run | mined | 2026-10-25 | 180d | corpus/knowledge/contamination-transparency-card.md |
| S082 | The Benchmark Ceiling: Human Judgment, Evaluation Economics and Benchmark Governance — https://arxiv.org/abs/2607.01254 | paper | B | the distinction between item-level transparency and procedural transparency in benchmark governance, and the disclosure fields a regulator would require — for the preprint's own argument, which was not peer reviewed at the time of opening | arXiv 2607.01254 (preprint; abstract page and PDF fetched 2026-10-25), § 8.2 Mandatory Transparency in Benchmark Design and Deployment: "transparency should attach primarily to procedures," then "governance, credentials, and validity testing, not necessarily to live item pools" — the break is the PDF's — and the section's required-disclosure list names "has been tested for training-data contamination" and "the credentials and compensation structure of evaluators who designed the hard-tail items"; PDF abstract: "while item-level transparency and procedural" then "transparency have opposite effects on benchmark validity" | a contamination card's fields should be procedural rather than item-revealing — whether the benchmark was tested for training-data contamination, the credentials of the item authors, and the date of the last substantive update are disclosable without publishing live items | mined | 2026-10-25 | 180d | corpus/knowledge/contamination-transparency-card.md |
| S083 | Cards Against Contamination: TCG-Bench for Difficulty-Scalable Multilingual LLM Reasoning — https://aclanthology.org/2026.findings-eacl.353.pdf | paper | A | a peer-reviewed benchmark paper's own contamination-resistant design — a public game engine separated from hidden card implementations — together with its threat model and refresh protocol, for the paper's own design claim | Findings of the Association for Computational Linguistics: EACL 2026, pp. 6710–6724, DOI 10.18653/v1/2026.findings-eacl.353 (PDF and anthology landing page fetched 2026-10-25), § Abstract: "We also formalize a practical threat model and refresh protocol that preserves evaluation integrity even if specific cards leak" and "separating the publicly released game engine from hidden card implementations" | contamination resistance can be engineered rather than asserted: separate the public engine from the hidden implementation, state a threat model, and publish a refresh protocol so a leaked card can be retired without rebuilding the benchmark | mined | 2026-10-25 | 180d | corpus/knowledge/contamination-transparency-card.md |
| S084 | 数据污染评估 (Data contamination evaluation), OpenCompass 0.4.0 documentation — https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html | docs | A | OpenCompass's own two documented contamination-evaluation procedures and their stated coverage limits, as documented in the Chinese 0.4.0 docs; not a claim about contamination in any particular model | § 数据污染评估 → subsection 基于自建同分布数据的污染数据标注: "目前该方案仅支持 GSM8K 数据集" and, on the case where only model parameters are public, "这些问题还没有被广泛接受的解决方案" (page fetched 2026-10-25) | a contamination card must record the detector's access level and its coverage — OpenCompass names both methods, ships them with the dataset splits they support, and states plainly that no widely accepted solution exists when only model parameters are public | mined | 2026-10-25 | 180d | corpus/knowledge/contamination-transparency-card.md |
| S085 | 大模型基准测试体系研究报告（2024年） (Large-Model Benchmark Testing System Research Report, 2024) — https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711534708580017.pdf | docs | B | the China Academy of Information and Communications Technology report's own account of the 方升 benchmark system — its four dimensions, its adaptive dynamic testing method, and its treatment of the dataset-contamination problem — for the report's own text; tier B because the record carries no document number | report dated 2024年6月 (PDF fetched 2026-10-25), § （二）“方升”自适应动态测试方法: "自适应动态测试（Adaptive Dynamic Testing，ADT）" with "动态测试数据库和高质量测试数据抽样算法"; § 5. 测试数据集的“污染”问题: "产学研各界需要研究数据“污染”的检测手段" | a national-level benchmark framework answers contamination by making the test bank dynamic rather than static — labelled test data, a dynamic test database and a sampling algorithm, offered as the answer to 刷榜 (leaderboard farming) and to a frozen evaluation set | mined | 2026-10-25 | 180d | corpus/knowledge/contamination-transparency-card.md |
| S086 | Code LLM 事前学習時の評価データ混入への対策 (Countermeasures against evaluation-data contamination in Code LLM pretraining), 言語処理学会 第31回年次大会 発表論文集 — https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf | paper | A | the paper's own contamination-detection method and its false-positive caveat for code benchmarks, in a Japanese peer-reviewed proceedings volume (2025年3月, p. 797); ANLP proceedings issue no DOI, so venue, year and page are recorded instead | 言語処理学会 第31回年次大会 発表論文集（2025年3月）, p. 797 (PDF fetched 2026-10-25), §概要: "検出に加えて、由来となるレポジトリの情報を用い" then "る手法を提案する。"; §1 はじめに: "混入とみなして除去することには疑問が残る。" | string overlap alone over-reports contamination — short generic code such as "return x+y" occurs in harmless training data, so a detector should add repository provenance to the string match and must state its false-positive regime | mined | 2026-10-25 | 180d | corpus/knowledge/contamination-transparency-card.md |
```

Append at the end of the `## Registry` table, before `## Paths`. Appending at EOF instead fails census
`E12 row outside Registry section` (measured, §5.6).

## 2. Cell count

`awk -F'|'` reports **NF=13** per row, i.e. 11 cells: the leading and trailing `|` are two empty fields. The
frozen contract says so twice — `SOURCES-CONTRACT-v1.md` §Census (`11 columns means NF=13`) and
`scripts/sources-census.sh` (`11 columns => NF=13`, with `E01` printing the cell count as `NF-2`). A literal
**12-field** row is the *failure* shape: `S081:not-a-table-row`, exit 4 from `plans/sources_adopt.py`
(measured, §5.5). So the acceptance reading is met as **11 cells = NF−2 = 11, NF=13**.

No cell in any of the six rows contains a literal or escaped `|`; `split_cells`' `escaped-pipe` defect never
fires. (`grep -F '\|'` on the campaign package hits only lines 23 and 31 — S093 and S101 — so no row in
S081–S086 needed a pipe rewrite; the prose rewrites below are byte-fidelity and location fixes.)

## 3. Per-cell change table (staged package → these rows)

Cells 0–4 (id, title+URL, kind, tier, scope) and cell 7 (`status=mined`) are unchanged. Every scope cell was
re-checked against this round's fetch: S081 Table 3's eight coded variables, S083's pages 6710–6724, S085's
four dimensions (指标体系/测试方法/测试数据集/测试工具), S086's printed p. 797.

| row | cell | old -> new | why |
|---|---|---|---|
| S081 | 5 `anchor` | arXiv 2608.29463, § Abstract: "We operationalize the taxonomy as a four-field disclosure protocol in which unk… -> arXiv 2608.29463 (preprint; abstract page and PDF fetched 2026-10-25), § Abstract: "because it is a property o… | staged 30-word sentence is not a byte-substring (source prints "unknown" with marks the row dropped) and is over the 25-word cap; re-cut to two spans that are strict substrings of the abstract page and carry the marks-free predicate |
| S081 | 8 `opened` | 2026-10-23 -> 2026-10-25 | campaign open date -> this round's access date (contract rule 1) |
| S081 | 9 `recheck` | 2026-10-23 — re-verify at the next upstream release (Gate S081) -> 180d | prose recheck -> cadence; census E09 refuses prose |
| S081 | 10 `used-by` | corpus/knowledge/contamination-transparency-card.md, corpus/knowledge/judge-calibration-thresholds.md -> corpus/knowledge/contamination-transparency-card.md | `judge-calibration-thresholds.md` does not exist (38 entries) -> permanent E11; projected to the admitted entry |
| S082 | 5 `anchor` | arXiv 2607.01254, § Benchmark Governance: "Item-level transparency and procedural transparency have opposite e… -> arXiv 2607.01254 (preprint; abstract page and PDF fetched 2026-10-25), § 8.2 Mandatory Transparency in Benchma… | no `Benchmark Governance` heading exists; the sentence is at the end of §8.2 and the disclosure list sits in the same section (the landing seat reached the same conclusion independently). Every span re-cut to a single PDF line, because the round's own quote gate matches strict bytes |
| S082 | 8 `opened` | 2026-10-23 -> 2026-10-25 | campaign open date -> access date |
| S082 | 9 `recheck` | 2026-10-23 — re-verify at the next upstream release (Gate S082) -> 180d | prose recheck -> cadence |
| S083 | 5 `anchor` | Findings of the Association for Computational Linguistics: EACL 2026, DOI 10.18653/v1/2026.findings-eacl.353; … -> Findings of the Association for Computational Linguistics: EACL 2026, pp. 6710–6724, DOI 10.18653/v1/2026.find… | page range and DOI verified; the two spans locate in the anthology HTML and in the PDF text (the PDF drops the hyphen in `contamination-resistant`, so only the HTML artifact proves the first one) |
| S083 | 8 `opened` | 2026-10-23 -> 2026-10-25 | campaign open date -> access date |
| S083 | 9 `recheck` | 2026-10-23 — re-verify at the next upstream release (Gate S083) -> 180d | prose recheck -> cadence |
| S084 | 5 `anchor` | § 数据污染评估, subsection 基于自建同分布数据的污染数据标注: "目前该方案仅支持 GSM8K 数据集"; and the section's framing sentence "这些问题还没有被广泛接受的… -> § 数据污染评估 → subsection 基于自建同分布数据的污染数据标注: "目前该方案仅支持 GSM8K 数据集" and, on the case where only model parameters are … | section path made explicit; both CJK spans were already strict substrings |
| S084 | 8 `opened` | 2026-10-23 -> 2026-10-25 | campaign open date -> access date |
| S084 | 9 `recheck` | 2026-10-23 — re-verify at the next upstream release (Gate S084) -> 180d | prose recheck -> cadence |
| S084 | 10 `used-by` | corpus/knowledge/contamination-transparency-card.md, corpus/knowledge/cjk-eval-venue-access.md -> corpus/knowledge/contamination-transparency-card.md | `cjk-eval-venue-access.md` does not exist -> permanent E11; projected to the admitted entry |
| S085 | 5 `anchor` | report dated 2024年6月, § （二）"方升"自适应动态测试方法: "自适应动态测试方法包含三个关键部分，即测试数据标签化管理、动态测试数据库和高质量测试数据抽样算法"; § 5. 测试数据集的"污染"问… -> report dated 2024年6月 (PDF fetched 2026-10-25), § （二）“方升”自适应动态测试方法: "自适应动态测试（Adaptive Dynamic Testing，ADT）" wit… | staged second span is truncated and uses ASCII quotes where the report prints “”; both spans re-cut to single lines |
| S085 | 6 `teaches` | a national-level benchmark framework answers contamination by making the test bank dynamic rather than static … -> a national-level benchmark framework answers contamination by making the test bank dynamic rather than static … | Q3 narrowing: `every sitting draws a different question set` is not in the report; the bank is dynamic rather than static |
| S085 | 8 `opened` | 2026-10-23 -> 2026-10-25 | campaign open date -> access date |
| S085 | 9 `recheck` | 2026-10-23 — re-verify at the next upstream release (Gate S085) -> 180d | prose recheck -> cadence |
| S085 | 10 `used-by` | corpus/knowledge/contamination-transparency-card.md, corpus/knowledge/cjk-eval-venue-access.md -> corpus/knowledge/contamination-transparency-card.md | `cjk-eval-venue-access.md` does not exist -> permanent E11; projected to the admitted entry |
| S086 | 5 `anchor` | §概要: "評価データと学習データの間の文字列の一致の検出に加えて、由来となるレポジトリの情報を用いる手法を提案する。"; §1 はじめに: "一致したものを一律に混入とみなして除去することには疑問が残る" -> 言語処理学会 第31回年次大会 発表論文集（2025年3月）, p. 797 (PDF fetched 2026-10-25), §概要: "検出に加えて、由来となるレポジトリの情報を用い" then "る手法を提案する… | staged spans cross 3-4 extracted lines and cannot be a strict substring; re-cut to single-line fragments with the break shown as adjacent spans |
| S086 | 6 `teaches` | string overlap alone over-reports contamination — short generic code such as "return x+y" occurs in harmless t… -> string overlap alone over-reports contamination — short generic code such as "return x+y" occurs in harmless t… | Q3 tightening: the paper proposes adding repository provenance to the string match, not merely using both |
| S086 | 8 `opened` | 2026-10-23 -> 2026-10-25 | campaign open date -> access date |
| S086 | 9 `recheck` | 2026-10-23 — re-verify at the next upstream release (Gate S086) -> 180d | prose recheck -> cadence |
| S086 | 10 `used-by` | corpus/knowledge/contamination-transparency-card.md, corpus/knowledge/cjk-eval-venue-access.md -> corpus/knowledge/contamination-transparency-card.md | `cjk-eval-venue-access.md` does not exist -> permanent E11; projected to the admitted entry |

Cells 8–10 are the campaign→fleet schema conversions the task names. Cells 5–6 are **evidence** changes:
each replaces a locator this round's fetch could not confirm, or narrows a claim the quote does not carry
(Q3, Q10).

## 4. Why the append must be scoped to S081–S086

The package as shipped cannot be appended wholesale:

```
$ python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package \
    /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
registry=82 staged=173 collisions=6 malformed=2 duplicates=0 defects=167 prose=167
  collisions: S077 S078 S079 S080 S090 S091
  malformed: S093:escaped-pipe S101:escaped-pipe
```

Six ids already existed in the live registry (and the package's `S091` is NEC 技報 while the live `S091` is
ABC), two rows carry `\|`, and all 167 staged rows carry prose `recheck`. S081–S086 are the only rows both
collision-free and inside C1's frozen id set.

## 5. Verification receipts (all 2026-10-25, all read-only outside `/tmp`)

### 5.1 Span check — every quote is a strict substring of a fetched artifact

Quotes are extracted from the delivered cells themselves (`"…"` spans), then required to be strict
byte-substrings of the named artifact, with an even ASCII-quote parity and no internal `"`:

```
S081 cells=11 NF=13 spans=7  max words=22
S082 cells=11 NF=13 spans=6  max words=12
S083 cells=11 NF=13 spans=2  max words=19
S084 cells=11 NF=13 spans=2  max words=3
S085 cells=11 NF=13 spans=3  max words=3
S086 cells=11 NF=13 spans=3  max words=1
BAD=0
```

Artifacts used (fetched today, HTTP 200): `arxiv.org/abs/2608.29463` + `/pdf/2608.29463`,
`arxiv.org/abs/2607.01254` + `/pdf/2607.01254` + `/html/2607.01254v2`,
`aclanthology.org/2026.findings-eacl.353.pdf` + the landing page, the OpenCompass 0.4.0 zh page, the CAICT
2024 report PDF, `anlp.jp/…/2025/pdf_dir/Q2-11.pdf`. Artifact text is the UTF-8 extraction (`pdftotext -enc
UTF-8`, tags stripped and entities unescaped for HTML) — the raw PDF is compressed and the raw HTML carries
markup, so neither can hold a prose quote as a byte run.

### 5.2 The round's own quote validator accepts every span

`/tmp/r30-GateQuote/sources_adopt.py --quote-file rows.md --artifact <extractions>`:

```
QUOTE rows=6 spans=23 located=23 found=23 overlong=0 absent=0 malformed=0 cap=25
exit=0
```

The same six rows against the landing seat's artifact set (raw HTML pages + `pdftotext` dumps): `exit=0`.

### 5.3 The standing adoption gate re-emits the rows unchanged

Run while the registry still had 82 rows:

```
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote block.md rows=6            exit=0
diff <(the rows) block.md     -> IDENTICAL
```

`prose=0` is the load-bearing field: nothing was re-dated or re-normalised, so the bytes I hand over are the
bytes the gate would emit. Re-run after the landing, the same command reports `collisions: S081 … S086` —
the append is already in the tree.

### 5.4 The fleet census accepts them, and refuses the staged rows

Both variants insert the six rows at the end of `## Registry` in a copy of the registry:

```
staged as shipped : E09 x6 (prose recheck) + E11 x10 (4 phantom entry paths + the not-yet-written entry)  exit=1
these six rows    : rowcheck-shokunin  ok  …/corpus/SOURCES.md                                            exit=0
these six rows, before the entry file exists : E11 x6 on corpus/knowledge/contamination-transparency-card.md
```

The last line is the ordering constraint: rows and entry must land in the same commit (Q7), or the census is
red in between.

### 5.5 C1's own counter

On a scratch tree with these rows and stubbed entry bytes, then on the live tree after the landing:

```
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok        exit=0
```

Two constraints this established for the C1 seat: the entry must write **one `source: S###` line per id**
(a comma list counts `cited_rows=1`, measured), and `usedby_ok` compares `used-by` path strings after
splitting on commas.

### 5.6 The 12-field row and the EOF append are both refused

```
sed 's/|$//' <row>; awk -F'|' '{print NF}'   -> 12
sources_adopt.py on it                          -> malformed: S081:not-a-table-row   exit=4
rows appended after the last line of the file   -> census E12 S081 … S086 row outside Registry section   exit=1
```

## 6. Live state: the landing, the diff, and two cells the quote gate refuses

Landed rows (registry lines 107–112) differ from §1 in 3–4 cells per row — mostly better locators
(`p.32 (printed 27)`, `html line 344`, `full text §7.3 line 855`) and entry-specific `teaches` wording. The
two derivations agree on the substantive findings: S082's staged `Benchmark Governance` heading does not
exist (both seats found it independently), S083's page range/DOI, S086's printed p. 797.

Running the round's quote validator over the landed rows, against artifacts named by their own anchors:

```
QUOTE rows=6 spans=12 located=11 found=11 overlong=0 absent=1 malformed=1
  ok      S081 x3, S082 x2, S083 x2, S084 x3, S086(title)
  REFUSED S085 no-quote
  REFUSED S086 absent  "一致したものを一律に混入とみなして除去することには疑問が残る"
exit=4
```

1. **S085 — structural refusal.** The anchor carries zero ASCII `"`, so the gate sees no span at all
   (`no-quote`, exit 4). Its quoted material is delimited by typographic `“ ”` or not delimited. One of its
   two quotes is a strict substring of the PDF text; the other (`“方升”测试体系提出自适应动态测试…方法对大模型进行评测`)
   is also line-broken across `方`/`法` and would be absent even with delimiters fixed.
2. **S086 — absent.** The 23-character caveat spans a line break in the PDF text (`…一律に` / `混入と…`); it
   is present only after whitespace is deleted.

Repair bytes, proven (`QUOTE rows=2 spans=4 located=4 absent=0 malformed=0`, exit 0):

```
S085 anchor: p.32 (printed 27): "自适应动态测试（Adaptive Dynamic Testing，ADT）"; p.34 (printed 29): "采用动态方式构建，保证每次参与测试题目的都不相同"
S086 anchor: p.1 (printed 797): "混入とみなして除去することには疑問が残る。"; printed title "Code LLM 事前学習時の評価データ混入への対策"
```

The landed `teaches`/`scope`/`source` cells need no change for this; only these two anchor cells do. Note
that C3's frozen predicate runs the gate's **selftest**, never the registry, so neither refusal is visible to
C3's counter — it surfaces only if someone points the gate at the round's own rows.

## 7. What the quote validator actually enforces (measured on the C3 deliverable)

1. **ASCII `"` pairing only** (`QUOTE_SPAN_RE = re.compile(r'"([^"]+)"')`). A row whose quotes use `「」` or
   `“”` yields `spans=0` and is refused structurally (`exit 4`) regardless of its evidence. My first draft
   used `「」`; it would have been refused, which is why §1 is all ASCII. Any row that must quote bytes
   containing ASCII `"` (S081's `"unknown"`) cannot do so under this rule — the quote is re-cut to the
   predicate (`is a valid entry, released under CC BY 4.0 …`) and the subject is named in locator prose.
2. **Strict bytes, newline-normalised only.** A span that crosses an extracted line is `absent` (exit 7),
   even when the source obviously contains it. Four of S082's five candidate spans were line-broken; every
   span in §1 is a single extracted line. This is not a defect in the gate — it is a house rule that
   changing the artifact changes the answer, so an anchor must name the artifact it was cut from.
3. **`words() = len(text.split())` makes the 25-word cap non-binding for CJK.** Every CJK span in §1 scores
   1–3 "words" while being 18–37 characters; the campaign package's own CJK quotes run 29–77 characters
   (staged S091 60, S095 29 and 32, S096 77). A 200-character Chinese paragraph would pass the cap. The two
   failure-capable cases C3 froze (26 words refused, absent quote refused) both hold, but neither can fire on
   a CJK row, so the cap's coverage is ASCII-only in practice. A character ceiling (~25 CJK characters) or a
   per-script word count would close it; every CJK span in §1 is already ≤22 characters, so such a rule
   would admit these rows unchanged.

## 8. Not verified here

- I did not write, and have not re-derived, the entry `corpus/knowledge/contamination-transparency-card.md`
  or its `corpus/README.md` index row — C1's seats own those. The counter in §5.5 used stubs; on the live
  tree the frozen line already prints with the real entry.
- The landed rows in §6 are audited for **quote bytes and anchor structure only**; I did not review their
  `scope`/`teaches` claims, which differ in wording from §1.
- Peer-review status is reported as the artifacts state it: S081/S082 are arXiv preprints (tier B), S083
  carries an EACL 2026 Findings page range and DOI, S086 is an ANLP 2025 proceedings paper with no DOI.
- `plans/registry_check.py` is scoped to a frozen 13-row population and prints `new files excluded`
  (`finding_count=0 exit=0` before the append), so it does not cover S081–S086.
- The quote validator I tested is the **/tmp deliverable** `/tmp/r30-GateQuote/sources_adopt.py`
  (sha256 prefix f26ed9bb), not the lane file `plans/sources_adopt.py` (6fe6e762); the lane file still has no
  quote mode, so its verdict on these rows is schema-only.
