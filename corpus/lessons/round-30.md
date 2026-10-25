# Round 30 — assimilation round 2, routed-defect closure, quote-validating gate (2026-10-25)

Lane: kengaku (LLM/model research & evaluation). Round shape: two v1 waves (36 build, 34 falsify).
Frozen claims: `plans/round-30-claims.md`. Baseline lane tip `363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db`.

## Gate

Admission of one entry, `corpus/knowledge/contamination-transparency-card.md`, as the amendment
round 29's refusal demanded. Both flip loci in `corpus/lessons/round-29.md` are discharged in one
commit: the `:227`/`:241-243` flip (amendment, not a rival design) and the `:180` attempt-2 Gate
flip (open S081–S086 as this round's one theme and pass the admission bar). Table cells are
frontmatter triad + the mapping/extend sections; the Q10 second-seat row cites a report path that
lands in the same commit (§Round 30 admission).

|candidate|decision|reason|read|
|---|---|---|---|
|`corpus/knowledge/contamination-transparency-card.md` | **admit as an amendment** | the design-vs-rival flip is met by mapping every field into the round-6 union table's own columns and declaring the delta (S1, S2 fields; R1's value set) instead of presenting a format; all six cited sources re-opened 2026-10-25 with ≤25-word located quotes; Q1 triad rebuilt (`verified-at: 2026-10-25`, `writer: KengakuR30`); the staged table the mapping reads is labelled unlanded, so no load-bearing claim rests on it (Q2). Second-seat re-reads for this admission: `.ufo/waves/round-30/falsify/R30FxSrcS081.md`, `.ufo/waves/round-30/falsify/R30FxSrcS082.md`, `.ufo/waves/round-30/falsify/R30FxSrcS083.md`, `.ufo/waves/round-30/falsify/R30FxSrcS084.md`, `.ufo/waves/round-30/falsify/R30FxSrcS085.md` and `.ufo/waves/round-30/falsify/R30FxSrcS086.md` | `plans/round-30-claims.md` C1; `.ufo/waves/round-30/build/R30SrcS081.md` … `R30SrcS086.md`; the falsify reports named in this cell |
|`judge-calibration-thresholds.md` (package) | reject this round | not the round's one theme; and the staged bytes at `:75` no longer claim a missing threshold, so round 29's premise against it does not describe them — the surviving objection is Q3: its kappa 0.46 / ceiling 0.84 figures at `:40-42` appear in none of its three anchor cells | `.ufo/waves/round-30/build/R30DraftGate.md`; staged file read in-package |
|`contamination-mitigation-comparative-evidence-2026-10-23.md` (package) | reject this round | a second theme (the round-4 ledger correction) with sources S120/S121 not opened this round; CORPUS rule 4 — no row is appended that no admitted entry cites | `.ufo/waves/round-30/build/R30DraftGate.md` |
|`card-publication-contracts.md` (package) | reject this round | a load-bearing claim rests on a tier-C mirror of a row the staging campaign already holds at tier B (Q2 tier floor) | `.ufo/waves/round-30/build/R30DraftGate.md` |
|remaining 63 staged entries and 169 staged rows | reject this round | CORPUS rule 4 (expansion is knowledge, not rows) plus the campaign-schema defects the gate counts: 2 escaped-pipe rows, 167 prose `recheck` cells, 6 id collisions with this lane's registry | `.ufo/waves/round-30/assimilation/{reg-ids,staged-ids,collisions}`; `.ufo/waves/round-30/build/R30BuildAppend.md` |
|register `kengaku round2 S091` (`payload-absent`) | quote-present at row level, not a fabrication | the register's payload is a 180-character Python one-liner lifted from the lane's own staging file, with 0 occurrences in the cited page; the row's real anchor is present once, and the page served 200 this round (a repeat request in the same minute got a 403 shell). The read pointer is the register row plus the seat's fetch, never this lane's S091 row, which is the ABC paper | `.ufo/waves/round-30/falsify/R30FxQuarantine.md`; register `lanes/kengaku/round2/SOURCES-PROPOSED.md:43` |
|register `kengaku round3 S105` (`payload-absent`) | quote-present at row level; `unreachable` is false | both the memento snapshot and the live page served 200 this round; the register's payload appears only in METI's 403 error shell, while the row's anchor (`ホールド・アウトデータ`) is present once. Error-shell misbinding, not fabricated evidence; the lane appends nothing | `.ufo/waves/round-30/falsify/R30FxQuarantine.md`; `/.ufo/reports/round-29/kengaku.md` §60-62 |
|`considerthese/2026-10-24.md` proposal 1 (gates on every push) | landed as criterion Q20 | proposal is unimplemented in this lane (`.github/` absent on every branch; `LOG.md:372` says receipts are "author-observed, never non-author closure"); drafted against 15 gates that run offline in ≤2 s, with the three limits the seat measured (exit-code-only loses; the pinned integer detects shrinkage; a tautologised assertion passes) | `corpus/QUALITY.md` Q20; `.ufo/waves/round-30/build/R30Considerthese.md` |

## Round 30 admission

- Entry: `corpus/knowledge/contamination-transparency-card.md` — six `source:` lines (S081–S086,
  no other id anywhere in the body), `verified-at: 2026-10-25`, `recheck: 180d` with its action,
  `writer: KengakuR30`.
- Q10 second seat: `.ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md` (a `reviewer` seat that
  did not write the entry re-opened all six sources and re-derived every number); per-source
  re-reads are `.ufo/waves/round-30/falsify/R30FxSrcS081.md` through
  `.ufo/waves/round-30/falsify/R30FxSrcS086.md`, and the six-row schema re-read is
  `.ufo/waves/round-30/falsify/R30FxRowsCensus.md`. The falsify wave registry that carries their
  roles is `.ufo/waves/round-30/falsify/swarm-registry.json`. Q13 is checked by the closure with
  `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit <the admitting commit>`;
  the round can only prove the shape in a sandbox (`.ufo/waves/round-30/falsify/R30FxQ13Fixture.md`), and
  says so rather than recording an unrun command as a check.
- Per-criterion record for the landed entry (required by `QUALITY.md` Q1's section, one row per bar row):
  Q1 pass (triad at lines 1-9: six `source:` lines, `verified-at: 2026-10-25`, `recheck:` with date and
  action, `writer: KengakuR30`); Q2 **pass for the entry's own claims** (S081 B, S082 B, S083 A, S084 A,
  S085 B, S086 A) and **not load-bearing for the field mapping**, which is labelled as this entry's
  reading of a staged document; Q3 pass (every quoted span ≤22 words with a location, and the two
  deductive sentences — the S081 prevalence sentence and the S085 complement sentence — each trace to
  their own quote); Q4 pass (§What this does not establish, six bullets including the two-delta-field
  concession and a named falsifier); Q5 pass (S082 labelled a working paper, S084 vendor documentation,
  S085 a self-report, S081/S082 preprints vs S083/S086 peer-reviewed); Q6 pass (§Extends names both
  objects; the delta is stated as one field, one placement, one value set); Q7 pass (entry + index row +
  coverage row + frontier discharge in one commit); Q8 pass (this Gate: one admit, four rejects, each with
  a flip); Q9 pass (each rejection's reason addresses the property it rejects — Q2/Q3/Q4 as named), Q10-Q15
  by the falsify reports cited above. Q2 on the *mapping* is the one bar row that fails and it is disclosed
  in the entry rather than asserted away.
- The staged text's own claims that this round refused to carry: the S082 anchor `# Benchmark
  Governance` does not exist in v2 (the quotes are in the full-text HTML §7.3/§8.2); the S081
  anchor quote was 30 words and occurs in neither HTML fetch; the S085 anchor flattened fullwidth
  quotes to ASCII so it was not a byte substring. Each is corrected by a located quote in the
  entry's own triad, not by a re-derivation of the staged cell.

## Sources opened this round

Access date 2026-10-25 for all six; every row is `mined` with `opened=2026-10-25` and
`recheck=180d`. Word counts are whitespace tokens, the counter the gate prints and the one D3 uses.

| row | URL opened | located quotes (words / location) | fetch identity |
|---|---|---|---|
| S081 | https://arxiv.org/abs/2608.29463 | "because it is a property of one run, it must be recorded with the reported score rather than with the benchmark release" (22, abs line 124); "direct, derivative, temporal, distributional, and acquired" (6); "Two variables fall below the prevalence-robust threshold registered in advance: strata reporting and the acquired type introduced here" (18) | abs 44646 B sha256 `4c81bd3c…`; full HTML and 18-page PDF also captured |
| S082 | https://arxiv.org/html/2607.01254v2 | "Item-level transparency and procedural transparency have opposite effects on benchmark validity." (11, §7.3 line 855); "transparency should attach primarily to procedures, governance, credentials, and validity testing, not necessarily to live item pools" (17, §8.2 line 901) | full text 212631 B sha256 `82a5c5c6…`; the abs page carries neither phrase |
| S083 | https://aclanthology.org/2026.findings-eacl.353.pdf | "a contamination-resistant design by separating the publicly released game engine from hidden card implementations" (14, p.1 = printed 6710); "We also formalize a practical threat model and refresh protocol that preserves evaluation integrity even if specific cards leak." (19) | 2697379 B sha256 `662c2235…` |
| S084 | https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html | 目前该方案仅支持 GSM8K 数据集 (3 tokens, line 344); 目前该方案仅支持 C-Eval, MMLU, HellaSwag 和 ARC 数据集 (7, line 397); 但如今开源社区往往只会公开模型参数而非训练数据集 (1, line 315) | 32762 B sha256 `c4447d93…` |
| S085 | https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711534708580017.pdf | “方升”测试体系提出自适应动态测试（Adaptive Dynamic Testing，ADT）方法对大模型进行评测 (3, p.32 = printed 27); 采用动态方式构建，保证每次参与测试题目的都不相同 (1 token / 23 CJK chars, p.34 = printed 29) | 1949572 B sha256 `e551e2e0…` — round 29's first fetch returned HTTP 000, this round 200 twice, `cmp` identical |
| S086 | https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf | 一致したものを一律に混入とみなして除去することには疑問が残る (1 token / 30 CJK chars, p.1 = printed 797, text-layer lines 80-81); title Code LLM 事前学習時の評価データ混入への対策 | 371155 B sha256 `c3706aca…` |

Cell transitions: S081–S086 did not exist before this round (`git show <baseline>:corpus/SOURCES.md`
→ 82 rows, last ids S077–S080, S090, S091); they enter `mined`, tier A 76 → 79, tier B 4 → 7,
`used-by` exactly `corpus/knowledge/contamination-transparency-card.md`. No existing row changed
(`git diff --numstat <baseline> -- corpus/SOURCES.md` → 6 insertions, 0 deletions). Census: exit 0,
the same 14 `W04` duplicate-URL warnings as at baseline (`.ufo/waves/round-30/assimilation/`,
`corpus/evidence/round30/census-before.txt`).

## Mistakes

- **Class: a repair that prints green while making the check unsatisfiable.** Evidence: this
  round's own narrowing of the D2 kappa sentence. The first repair added a markdown-emphasis strip
  `re.sub(r"[*_\`]", "", raw)` before testing the measured scope — which deletes the `*` inside
  `corpus/knowledge/*.md`, so the scope test could never pass and D2 was red for *any* lesson bytes.
  Caught by falsify seat `R30RevCounter` at counter revision `e565468`
  (`.ufo/waves/round-30/build/R30RevCounter.md`), not by the counter itself. **Captured-by: none** —
  `plans/round30_defects.py` had no selftest and printed a bare `defects=1`, indistinguishable from
  the genuine pre-repair state. **Fix:** the emphasis strip now applies only to the banned phrase
  (`re.sub(r"\*\*|__", "", raw)`) while the scope test reads the raw line; the count is re-derived in
  the lesson command's own unit (`grep -rn` line counts, singular `hit` accepted); and the D-items
  gained their own failure-capable assertions (D1 judges the committed HEAD blob, D4 requires the
  addendum in `HEAD:`, D5 accepts either repair branch, an empty note is a defect). A counter whose
  only output is a total cannot show which of its own edits broke it.
- **Class: an adjacent repair that records the mismatch instead of answering it.** Evidence: D1's
  first receipt planted the wave file's eight-field line at the cited path, while the report quotes
  the counter's seven-field line; a reader re-deriving the report's line got no match.
  Caught by `R30RevDefects` and by the falsify wave. **Captured-by:** the routed defect's own
  wording ("commit the receipt under the cited name"), which names the bytes, not the path.
  **Fix:** the receipt carries both lines, each labelled, plus the provenance header; D1's check
  requires the quoted seven-field line verbatim in the committed blob.

## Counter blind spots (recorded, not smoothed)

C1's counter is `plans/adoption_check.py`, unchanged since round 29, and a falsify critic
enumerated what it cannot see: registry cell 8 (`opened`) is never read, so a staged
`opened=2026-10-23` row would pass behind a rewritten `verified-at`; it compares the *cardinality*
of cited ids, not their identity, so an entry citing six already-held rows would pass; the entry
body and the coverage-map row are never read, so a six-line stub passes. What covers each gap here,
named so the closure can check it rather than trust the counter: the six rows' `opened` cells are
re-derived in `corpus/evidence/round30/rows-opened.tsv` from `awk` over the committed rows and the
six ids are the ones the registry did not hold at baseline (`git diff --numstat <baseline> --
corpus/SOURCES.md` → 6 insertions, 0 deletions); quote truth is carried by the six falsify
re-reads, not by the counter; the coverage-map and frontier rows are named in the Gate row above and
audited by `.ufo/waves/round-30/falsify/R30FxEntryQ7Q9.md`. The predicate itself stays exactly as
frozen in `plans/round-30-claims.md` — a blind spot recorded is not a target moved.

C2's counter has two known survivors, both found by falsify seats and disclosed rather than closed this
round: D2's assertion is literal-phrase (a paraphrase that says "clean across the whole lane" passes
although it widens the scope), and D1 validates the receipt's two lines, not the provenance header, so a
three-line proofless receipt would pass. Tightening either is next round's work; the routed wording is
answered by the landed bytes regardless.

D2's counter had the same shape of hole in the other direction: its only output was a total, so its
own broken repair read as a genuine defect (see §Mistakes).

## Measured

- C1: `python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census`
  → `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok`, exit 0;
  the do-nothing control at freeze is `entries=0 …` exit 1
  (`.ufo/waves/round-30/claims/control-nothing.txt`).
- C2: `python3 plans/round30_defects.py --lane .` → `defects=5` exit 1 at freeze
  (`.ufo/waves/round-30/claims/defects-before.txt`) → `defects=0` exit 0 after the commit that lands
  D1's receipt and D4's wave evidence.
- C3: `python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=14 failed=0` exit 0; the
  pre-change body has no quote mode at all (`--quote-file … --artifact …` → argparse exit 2,
  `.ufo/waves/round-30/claims/gate-before.txt`).

## Wave accounting

Wave 1 (build) 36 seats: 10 scout, 7 reviewer, 6 executor, 4 scribe, 3 critic, 2 connector,
2 mutation-tester, 1 revenger, 1 simplifier. Wave 2 (falsify) 33 seats, 16/33 attack roles (48% under the fleet's reviewer+critic+mutation-tester+revenger+connector reading; a narrower reviewer-only reading is reported in `.ufo/waves/round-30/falsify/R30FxDeadSeats.md`).
Seat-level yield: `.ufo/waves/yield.tsv` round-30 rows. No seat died before wave 2; dead-seat
detail is in the round report.
