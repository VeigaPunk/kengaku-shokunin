# R30DraftGate — the round-30 `## Gate` block, second revision

Seat: scribe, leaf. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Access date 2026-10-25.
No production edits: the only lane-tree file I write is this report.

Draft: `/tmp/r30-DraftGate/gate.md`, 12 457 B, sha256 `d9699050…446c` (copy
`/tmp/r30-R30DraftGate/gate.md`, identical). Supersedes the `a4f60e21` draft.

## Behavior

1. Read the frozen authority (`plans/round-30-claims.md`), the shape sources
   (`corpus/lessons/round-29.md` §Attempt 2 Gate and §Rejected candidates, `corpus/QUALITY.md`
   Q1–Q13, `MERGE-REPORT.md`), and the six source receipts.
2. Measured the staged package myself: anchor word counts, row well-formedness, `used-by`
   multiplicity, tier spread, duplicate-target hashes, duplicate-source URLs.
3. Read `plans/gate_timing_check.py` and derived Q13's mechanics from its source; then **ran its own
   regexes and dataclasses over my admit row** (imported read-only, no lane writes) instead of
   trusting a description of them. Two defects in my own cell surfaced that way (G16).
4. Inventoried the second wave: 31 reports, verdict tally, per-citation existence, anchored
   `VERDICT:` line, and candidate-path naming — the four conditions `audit_admission` applies.
5. Rebuilt the admit row on the five seats that actually return PASS, removed every citation the
   check would reject, and stated the one open source defect (S086) outside the reason cell, because
   naming a failing path inside the cell registers it as a citation and fails the row.

## Gates I ran (commands and outcomes)

| # | command | outcome |
|---|---|---|
| G1 | cell-split each staged row of `SOURCES.append.md` on the pipe character | 175 rows; **S093 = 12 cells, S101 = 15**, both with an escaped pipe |
| G2 | quoted-segment word count per staged anchor cell | S081 **30** (over 25), S082 11+17, S083 14+19, S084 3+1, S085 1-word runs, S086 1+1 |
| G3 | `sha256` of both copies of `benchmark-task-validity-checklist.md` | staged 7 239 B `7b73f175…`; lane 12 643 B `2cd9dca5…` |
| G4 | tier scan of staged rows | two tier-C rows: S145, S167; S167 mirrors staged S126 at `arxiv.org/abs/2606.09809` |
| G5 | kappa grep in the staged judge entry and its three anchor cells | figures at `:40-42`; **no kappa text in any anchor cell** |
| G6 | read the six build receipts `R30SrcS081.md` … `R30SrcS086.md` | all targets located; S085 `http=200` after round 29's `HTTP 000`; S081's 30-word staged quote is 0-occurrence in both HTML fetches |
| G7 | current registry: row count and S081–S086 cells | **88 rows**; `:107-112`, each `mined`, `opened 2026-10-25`, 11 cells, `used-by` the card alone |
| G8 | read `plans/gate_timing_check.py` | candidate resolved as a path (`:314-317`); only an admit row's reason cell scanned (`:330`); second wave = `falsify` or `wave-2` (`:241-243`); an invalid citation fails the row; generic phrases void it (`:45`); each citation needs existence, a registry seat with an allowed role, an anchored `^VERDICT:` line (`:56`,`:360`) and the candidate path in the body (`:358`) |
| G9 | `ls .ufo/waves/round-30/falsify/*.md` | **31 report files** — the wave landed while this review ran |
| G10 | verdict tally over those 31 | **PASS 7, FAIL 9, no anchored `VERDICT:` line 15** |
| G11 | per-citation check of the five seats I cite | `R30FxSrcS081…S085`: exist, anchored PASS verdict, candidate path present — all five valid. `R30FxC3Gate` PASSes but names **no** candidate path (`grep -c` → 0), so it cannot serve; `R30FxSrcS086` is FAIL |
| G12 | `ls R30FxEntryCompleteSet.md R30FxRowsCensus.md` | RowsCensus appeared mid-review; **EntryCompleteSet still absent**, so no complete-set re-read exists |
| G13 | import the checker read-only and run `extract_citations` / `extract_generic_references` / `valid_repo_path` on my own admit row | first run flagged a **bare `QUALITY.md`** citation (unresolvable) and showed that naming the failing S086 path registers a citation the row must then reject. Both fixed; re-run returns five full-path citations, `generic: ()`, candidate a valid repo path |
| G14 | URL comparison, staged S120 against lane S001 | same document (`2026.gem-main.50.pdf` vs `2026.gem-main.50/`) |
| G15 | current tree markers | entry 15 779 B, triad `:1-9`, `writer: KengakuR30`, CG1–CG8 `:73`; README index `:65`, bullet `:274`, discharge `:275`; `QUALITY.md:198` Q20; lesson Gate `:6` |
| G16 | `test -d .github`; `grep -n author-observed LOG.md` | absent; `372: Receipts are author-observed, never non-author closure.` |

## Findings

1. **The admission is in the working tree, not in the package.** Entry, six `mined` rows, README
   index and discharge, `QUALITY.md` Q20 and a round-30 lesson all exist uncommitted. The block reads
   the landed bytes; a Gate written against the staged package would have mis-stated Q1, the anchor
   quotes and the `used-by` cells.
2. **Q13 now passes mechanically on five citations.** The five per-source scout seats return PASS with
   anchored verdicts and name the candidate path (G11). Everything else in the wave either FAILs or
   carries no anchored verdict, and `R30FxC3Gate` — a PASS — names no candidate path, so it is not
   admissible evidence for this row. My reason cell cites the five and nothing else.
3. **One source defect stays open and blocks the row's honesty, not its mechanics.** `R30FxSrcS086`
   is FAIL at `:149`: the entry's S086 line states 23 CJK characters and lines 78–81 where the seat
   measured 30 characters and text-layer lines 80–81, and `corpus/SOURCES.md:112` repeats 78–81. Both
   spans are verbatim and located, so the repair is a number and a range and C1's kill rule is not
   touched. The row lands once the entry's line, the registry cell and the seat agree; then that
   path enters the reason cell and Q10 covers all six sources.
4. **A failing path mentioned in the reason cell is a citation, not a caveat** (G13). Prose that says
   "not cited, see X.md" still registers X and the row fails on it. The caveat therefore lives in the
   report and in the paragraph below the table; the cell stays clean.
5. **Counts are derived, not asserted.** 175 staged rows − 6 admitted = 169. 65 staged entries − 1
   admitted − 4 rejected (judge calibration, comparative mitigation evidence, card publication
   contracts, the validity-checklist fold) = 60. The lesson's row set drops the fold row, so its own
   arithmetic gives 61; either number is defensible, but only if the row set and the arithmetic match.
6. **Two reasons were wrong and are gone.** The `used-by` collision is not Q6 — lane S005's cell names
   three paths — and the landed append already made S081–S086 single-entry. The 12/15-cell split is a
   row-schema property, not Q3, and is filed under the deferred row.
7. **Two lesson cells contradict the record and need a supersession pointer, not a silent edit.** S105
   "unverifiable" against the fleet report's quote-present; S091 "re-read this round" against a wave
   in which no round-30 fetch of that page appears. Both of my rows name the lesson line they
   supersede.
8. **The wave is still moving.** Report count went 10 → 28 → 31 during this review, so any hand-count
   in prose is stale within minutes; the checker re-derives it at commit time, which is the only count
   that matters.

## What the lesson Gate needs (paste-ready)

| lesson cell | state | what my draft supplies |
|---|---|---|
| `corpus/lessons/round-30.md:17` admit row | reason cell cites 6 paths, 3 absent + 1 verdictless → FAIL | five valid citations only (`R30FxSrcS081`…`S085`), with the failing sixth moved to prose |
| `corpus/lessons/round-30.md:21` counts | "63 staged entries" while its own table records 4 of 65 → 61 | derivation written out; 60 for my five-row set |
| `corpus/lessons/round-30.md:22` S091 | "re-read this round", no round-30 receipt | "round 29's hand-check, carried forward", with a supersession pointer |
| `corpus/lessons/round-30.md:23` S105 | "unverifiable" against fleet quote-present | "quote-present in the archived snapshot", with a supersession pointer |
| the whole table | 4 columns, no flip cell | 5 columns: `candidate | decision | reason | flip condition | read pointers`, flip cell filled for every non-admitted row |
| bare `R30FxSrcS086.md` mention | resolves by luck | every report written as a full path, or not at all |

## Conflicts — verbatim, for the canonical Rust judge

- `corpus/lessons/round-29.md:183`:
  "`| register \`kengaku round3 S105\` (\`payload-absent\`) | see the second hand-check verdict in the round report | the quoted Japanese text reads like a fetch-failure page; confirming it is the campaign register's unchecked family rather than a claim in this lane's corpus | a re-fetch that renders the article rather than an error page |`"
- `.ufo/reports/round-29/kengaku.md:60-62`:
  "`kengaku round3 S105` → **quote-present**; the quoted Japanese text is METI's WAF error shell returned to a bare client, and the row's hold-out quote is present in the 200 snapshot."
- `corpus/lessons/round-30.md:23`:
  "`|register \`kengaku round3 S105\` (payload-absent) | unverifiable, not a fabrication | …`"
- `.ufo/waves/round-30/falsify/R30FxSrcS086.md:149`:
  "`VERDICT: FAIL — \`corpus/knowledge/contamination-transparency-card.md\` line 6 misstates its own S086 evidence (caveat measured at 30 CJK characters, stated as 23; the quoted clause sits at text-layer lines 80–81, not 78–81), and it contradicts the \`S086\` row of \`corpus/SOURCES.md\`, which states 30.`"
- `corpus/lessons/round-29.md:228-230` against staged `judge-calibration-thresholds.md:75`:
  lesson: "it claims the pre-registered threshold is missing inward" / staged: "It does not claim that any specific kappa threshold is".

## Touched surfaces

- Written: `.ufo/waves/round-30/build/R30DraftGate.md`; `/tmp/r30-DraftGate/gate.md`;
  `/tmp/r30-R30DraftGate/gate.md`.
- Read-only: `plans/round-30-claims.md`; `plans/gate_timing_check.py` (read and imported without
  writes); `corpus/QUALITY.md`; `corpus/SOURCES.md:1-30,23,106-112`; `corpus/README.md:65,241,270-278`;
  `corpus/knowledge/contamination-transparency-card.md:1-9,13-166`;
  `corpus/knowledge/contamination-detection-and-transparency.md:1-100`;
  `corpus/knowledge/benchmark-task-validity-checklist.md` (bytes only, for the hash);
  `corpus/lessons/round-29.md:175-190,218-244`; `corpus/lessons/round-29-verifier-spotcheck.md:108-139`;
  `corpus/lessons/round-30.md:1-63`; `considerthese/2026-10-24.md:1-40`; `LOG.md:372`;
  `.ufo/waves/round-30/assimilation/{quarantine-slice,collisions,reg-ids,staged-ids}`;
  `.ufo/waves/round-30/falsify/*.md` (31 reports: verdict tally, and the five cited bodies in full);
  `.ufo/waves/round-30/falsify/swarm-registry.json`; `.ufo/waves/round-30/build-spec.json`;
  `.ufo/waves/round-30/build/R30SrcS081.md` … `R30SrcS086.md`, `R30CritC2.md`, `R30CritC3.md`,
  `R30ConnSibling.md`, `R30Considerthese.md` where read; `MERGE-REPORT.md`; `SOURCES.append.md`;
  staged `knowledge/corpus/knowledge/*`; `lanes/kengaku/round6/DOMAIN.md:40-50`;
  `.ufo/reports/round-29/kengaku.md:56-70`.

## Out of scope / not claimed

- I fetched none of S081–S086; every source-level statement cites a seat receipt.
- I did not run `plans/gate_timing_check.py` as a CLI (it needs a commit and a lesson path in the
  tree); I read it and exercised its own functions on my row. I ran none of `round30_defects.py`,
  `sources_adopt.py --selftest`, `adoption_check.py`.
- I did not create report files in the second wave, edit the lesson, or touch the registry.
- No tool was installed or upgraded.

## Artifact paths

- `/tmp/r30-DraftGate/gate.md` — the block (sha256 `d9699050…446c`, 12 457 B).
- `/tmp/r30-R30DraftGate/gate.md` — byte-identical copy.
- `.ufo/waves/round-30/build/R30DraftGate.md` — this report.
