# R30DraftEntry — leaf report (C1 scaffold: amendment entry draft)

Role: leaf scribe (`L1Kengaku30.R30DraftEntry`), godspeed frame. No subagents, no writes
outside the two permitted paths.

## Deliverables

- Draft entry file: `/tmp/r30-DraftEntry/entry.md` (26221 bytes → 27028 after fixes; 266 lines).
  This is the only entry body I produce. It is an **amendment** to
  `corpus/knowledge/contamination-detection-and-transparency.md`.
- This report: `.ufo/waves/round-30/build/R30DraftEntry.md`.

## What I fetched (all on 2026-10-25, stored in /tmp/r30-DraftEntry/)

| id | URL | capture | sha256 | size |
|---|---|---|---|---|
| S081 | https://arxiv.org/abs/2608.29463 (abs) + https://arxiv.org/html/2608.29463v1 (full text) | s081.html / s081.txt / s081.full.txt | 4c81bd3c180736318ed03e31968fa4d109b94025ec596203dbc4e963b396908a (abs) | 44646 |
| S082 | https://arxiv.org/abs/2607.01254 (abs) + https://arxiv.org/html/2607.01254v2 (full text) | s082.html / s082.txt / s082.full.txt | 6ef2093990f95ec7297a0e29656a825a2730b5a6ab24d477ab4f56a37206571c (abs) | 43552 |
| S083 | https://aclanthology.org/2026.findings-eacl.353.pdf | s083.pdf / s083.raw.txt | 662c2235680e475c1880b1a4486a8e001eb746c6d992384e1400d01287b3dfe4 | 2697379 |
| S084 | https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html | s084.html / s084.txt | c4447d93c6945d2c68dbffac8274b3adc4aa2b6e510120c33eea1de966b7ec23 | 32762 |
| S085 | https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711534708580017.pdf | s085.pdf / s085.raw.txt | e551e2e0956c314507ab240b3ca19ce47aed88640a98e6c316bd4efc6bbc131c | 1949572 |
| S086 | https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf | s086.pdf / s086.raw.txt | c3706aca80aa8aeee7fa39d3a5988f238a138c508c0ca5fe5c107c50d7feb303 | 371155 |

No tool installed; `curl`, `pdftotext` (present at /usr/bin), `python3` sufficed. No pacman
transaction (also paused host-wide).

## Verification method

Every quote in the draft is a byte substring of the fetched capture. Two normalizations are
declared in the entry's map header:

- `c` = substring after collapsing whitespace runs to one space (HTML rendering, PDF line-wrap);
- `s` = substring after removing *all* whitespace — only for CJK/Japanese quotes where the PDF
  extraction breaks a sentence across lines (no glyph added/removed).

All 39 map quotes pass their declared check, and every count in the map matches the actual
token count. `FAILS: []` on the final run. Where the abstract page and the full-text HTML
differ in wording (S081), I quote the **abs page** bytes (that is the URL's served surface) and
say so in the source line.

## Claim-to-quote map (compact)

39 rows, ids c1–c39. S081: c1–c20 (abstract abs page: c1,c2,c3,c5,c18,c19,c20; §3: c4; §2:
c6; §4: c7–c16; abstract taxonomy: c17). S082: c21–c24 (§7.3, §8.2). S083: c25–c27
(abstract). S084: c28–c31, c39 (数据污染评估; the two method sections). S085: c32–c34
(§(二), §2 动态更新). S086: c35–c38 (概要, §1 はじめに p.797). Full table with locations and
counts is in the entry's §Claim-to-quote map.

## Staged-card re-grounding: what survived, what was refused

The staged package card was checked quote-by-quote against my fetches. Survivors: S081's split
rule and four-field protocol, S082's procedural-transparency rule, S083's engine/card split and
refresh protocol, S084's coverage limits, S085's dynamic bank, S086's string-match caveat.
Three staged items were **refused or re-anchored** (recorded in the entry's §Rejected and
refused):

1. Staged R5 "instrument currency — date of the benchmark's last substantive update" attributed
   to S082: S082 has no such disclosure field in the fetched bytes (it argues renewal economics).
   Re-anchored as R5 protection-and-refresh on S083 + S085; card-Q8 narrowed to regeneration
   only. Flip recorded.
2. Staged S081 anchor `Table tab:instrument`: absent from the fetched v1 HTML (tables are
   numbered 1 and 2). Replaced by Table 2 + §4 anchors.
3. Staged S082 title "…Evaluation Economics and Benchmark Governance": the served title is "The
   Benchmark Ceiling: Human Judgment, Evaluation Scarcity, and the Political Economy of AI
   Capability Measurement". Flagged for the registry row.

Also: S081's own audit — agreement κ runs 0.00–0.35 (median 0.21), and the two variables below
the pre-registered threshold are **strata reporting and the acquired type** (R1 and S1 of this
card) — I put this in the negative-space section, since the card's two most load-bearing fields
are the two the sources' own audit least validated.

## Frozen-predicate alignment

- `source:` lines: exactly six distinct ids S081–S086, one per line (the adoption gate's regex
  extracts one id per `source:` line; a single line with six ids would lose five).
- `verified-at: 2026-10-25` exact. `recheck: 2027-04-23 (180d)` with an action.
- README index row, registry rows (mined / opened 2026-10-25 / recheck 180d / used-by naming the
  entry) are **landing duties** of the admitting commit, outside my write scope (Q7 row in the
  entry states exactly that). Q10/Q13/Q14 (non-writer second-seat re-read) are not satisfied by
  this draft and are stated as such.

## Observations for the round (not adjudicated)

- A sibling/landed file `corpus/knowledge/contamination-transparency-card.md` exists in the lane
  worktree (untracked; writer: KengakuR30). It and this draft are independent. Differences:
  the landed card's S081 abstract quote "Two variables fall below the prevalence-robust
    threshold registered in advance: strata reporting and the acquired type introduced here" is
    present on the abs page (verified). Its S083 quote "a contamination-resistant design by
    separating the publicly released game engine from hidden card implementations" is **not** a
    byte substring of my PDF extraction (the PDF's text run has `contaminationresistant`,
    without the hyphen, so the bite cannot be byte-located there); it **is** present verbatim in
    the aclanthology HTML landing page (`https://aclanthology.org/2026.findings-eacl.353/`,
    fetched 2026-10-25) — the quote is real, but the landed card's cited location ("PDF p.1,
    printed 6710") does not byte-match the surface it is quoted from. Q10-relevant nit, not
    fabrication. The landed
  card's S085 ADT quote verifies under the `s` normalization. The landed card cites "html lines
  344 and 397" for S084; my fetch's line numbers differ (page reflow) — I cannot confirm that
  line numbering. Its S082 URL is the HTML full text (https://arxiv.org/html/2607.01254v2),
  while my source line uses the abs URL with HTML-forwarded anchors.
- Title check: arXiv 2608.29463 "Benchmark Contamination: A Taxonomy Organized by Defeated
  Mitigation"; arXiv 2607.01254 "The Benchmark Ceiling: Human Judgment, Evaluation Scarcity, and
  the Political Economy of AI Capability Measurement"; S083 "Cards Against Contamination:
  TCG-Bench for Difficulty-Scalable Multilingual LLM Reasoning" (Findings of EACL 2026,
  pp.6710–6724).
- D5 (S091 used-by asymmetry) does not touch this entry: the frozen predicate demands exactly six
  cited rows, so S091 must **not** be added as a `source:` line, and its registry `used-by`
  must not name this entry.

## Gates

Frozen C1 predicate is decidable at landing by `adoption_check.py --expect … --census`; this
leaf cannot run it (no landing, no census write). This draft's claim is narrower: the entry
body, the six source lines, verified-at/recheck, the Q1–Q8 gate table, design rules, Q4 negative
space, Q6 extension statement, and the claim-to-quote map — all present in `/tmp/r30-DraftEntry/entry.md`.
