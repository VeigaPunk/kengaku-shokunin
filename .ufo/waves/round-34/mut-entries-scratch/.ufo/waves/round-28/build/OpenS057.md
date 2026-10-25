# OpenS057 — reopen of S057 (xFinder extraction-method comparison) and C2 literal-use check

Writer/seat: KengakuR28.OpenS057-2 (read-only scout; author-side advice, not outside closure).
Lane root: /home/vgpnk/Projects/shokunin/kengaku-shokunin. Lane HEAD observed f0ba09be0f3066daba2134b943d973ad1588f34a.
Scratch evidence: `.ufo/waves/round-28/scratch/OpenS057/` (`xfinder-v3.pdf`, `x.txt` pdftotext -layout, `abs.html`, `abs-unversioned.html`).
No registry, knowledge, lesson or production file edited. No installs or updates. No upstream code executed.

## Scope of this seat

Target is S057 only. The assignment's template clauses about own-work S056 and about S038 do not apply to the S057 row:
its teaches cell extends S044, not S056 or S038. Neither was reopened here, and no claim is made about either.

## Opening record

| field | value |
|---|---|
| URL (row) | https://arxiv.org/abs/2405.11874 — HTTP 200; the unversioned page reports "this version, v3" (versions v1–v3 only, no v4) |
| URL (opened full text) | https://arxiv.org/pdf/2405.11874v3 — HTTP 200, 1,231,485 bytes, sha256 `4b1a8c60b6350c1dfd7fdf578b1d82ff7ca8e04a1bdfb033a69ee77ce0b28f74`, 44 pages |
| Version | arXiv:2405.11874v3 [cs.CL] 25 Feb 2025; header "Published as a conference paper at ICLR 2025"; abs page: submitted 20 May 2024 (v1), last revised 25 Feb 2025 (v3) |
| Access date | 2026-10-21 |
| Located quote 1 (§5.3 Setup, PDF p.9) | "we replicated only the RegEx methods on each framework and ensured consistency in other settings." |
| Located quote 2 (§5.3 RQ1, PDF p.10) | "The graph reveals significant discrepancies in the rankings of LLMs obtained using different evaluation frameworks." |
| Located quote 3 (§5 Baselines, PDF p.7) | "OpenCompass … LM Eval Harness … and UltraEval … all of which rely on RegEx-based extraction methods." |

Quote 1 matches word for word the S057 quote already in `corpus/lessons/round-27.md:50`, including its §5.3/PDF p.9 location.

## Anchor and teaches confirmation (row cells, read-only)

- **Anchor "v3 §5.1 Tables1–2 PDFpp7–8; §5.3 PDFpp9–10" — confirmed.** Table 1 (KAF test set, extraction accuracy, frameworks vs xFinder) is on PDF p.7. Table 2 (KAF generalization set, with GPT-4 as extractor) is on p.8. §5.3 starts on p.9; its Setup is on pp.9–10, and Figure 4 (rank bump charts) plus RQ1–RQ3 are on p.10.
- **Teaches "framework RegEx versus learned extraction changes scores/rankings" — confirmed.** On the same KAF test set (Table 1), Overall accuracy is 0.5722 for UltraEval, 0.7937 for OpenCompass, 0.8113 for LM Eval Harness, and 0.9661–0.9712 for xFinder. Figure 4 and RQ1 report changed LLM ranks across extractors; for example, InternLM2-1.8B-Chat is ranked first in UltraEval but fifth in OpenCompass on CommonsenseQA (alphabet), p.10.
- **"Exact rule versions … unresolved" — confirmed.** The framework baselines are cited only as OpenCompass (2023), Gao et al. (2021) and He et al. (2024). A search of the full text for commit/version strings found no framework release or commit pin, only GitHub URLs (lines 47, 792, 821, 823, 846–847 of `x.txt`).
- **"§5.3 item pairing … unresolved" — confirmed.** The Setup says RegEx methods were replicated with uniform preprocessing, consistent zero-shot prompts and the same decoding settings ("temperature to 0, top_p to 0.9, and top_k to 5", p.10). It never says that every extractor scored the same saved response per item. Same settings ≠ same records `[INFERENCE: top_k=5 sampling is reported alongside temperature 0; the paper does not state the generation was single-pass/reused]`.
- **"some aggregate denominators remain unresolved" — confirmed, and now more specific.** I recomputed each Overall cell as a sample-weighted mean over the key-answer types the table reports, using the per-type counts in Appendix B: test set 1887/821/1590/663 (Table 15) and generalization set 1280/962/1600/640 (Table 19).
  - Every Overall in Table 1 and Table 3 matches.
  - In Table 2, the OpenCompass, LM Eval Harness, GPT-4 and both xFinder Overall cells match.
  - Table 2's UltraEval Overall (0.3978) does not match. The weighted mean over its two reported types is 0.4557. Counting the unreported types as zero gives 0.1952, and an unweighted mean gives 0.3863. I found no denominator that reproduces it.
  - Separately, the OpenCompass and UltraEval Overall cells average only two of the four types ("/" for short text and categorical label), so their Overall values are not on the same denominator as the four-type rows.

  This is an arithmetic observation from published cells, not a claim that the paper is wrong.
- **Scope "not proof of paired item identity in §5.3" — appropriate.** Nothing in §5.3 or the D.3 headers establishes item-level pairing.
- **Tier A:** this is the original paper (arXiv v3 matching the ICLR 2025 camera-ready header), used for its own reported comparisons. Tier A is appropriate for the row's scope.

## C2 literal-reference comparison (frozen 35-file population)

Command: Python regex scan of every `knowledge_paths` entry in `plans/fixtures/r28/registry/population.json`, using its `reference_pattern` and collecting lines whose matches include exactly `S057`.

| citing frozen file | lines |
|---|---|
| corpus/knowledge/extraction-policy-comparison.md | 1 (source header: "S057 xFinder https://arxiv.org/abs/2405.11874 v3 §5.1/§5.3"), 16 ("xFinder (S057, reopened this round)"), 24 ("remain unresolved (S057)") |

No other file among the 35 contains a standalone S057.

The current row (`corpus/SOURCES.md:79`) has status `mined` and used-by `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`. Every citing frozen file is covered, so missing_used_by is empty. The extra lesson path is allowed by the contract. The round-27 lesson (:201–202) records the used-by change old→new, with status/recheck unchanged.

The knowledge file's use agrees with the row's scope. It treats xFinder as prior art for extractor-dependent outcomes, and explicitly not as proof of paired-record provenance, exact rule variants or comparable denominators (lines 16–17, 23–25). The new Table 2 UltraEval mismatch is consistent with that caveat; it does not contradict it.

**Suggested mutable-cell changes: none.** Status `mined`, recheck `180d` and used-by are all consistent with the literal citations and with the reopened source. Immutable cells (source/kind/tier/scope/anchor/teaches/opened) need no change, and I propose none. If a later round wants the denominator caveat made concrete, it belongs in lesson or knowledge prose (Table 2 UltraEval Overall 0.3978 not reproducible from Table 19 counts), not in a row edit.

## Commands observed

`curl -sSL` for the v3 PDF, the v3 abs page and the unversioned abs page (all HTTP 200); `sha256sum`; `pdftotext -layout`; `rg` over the extracted text; a Python stdlib regex scan of the frozen population; Python arithmetic for the weighted means; `git rev-parse HEAD` and `git log --oneline -3` (read-only).

## Limitations

- I read §1 (p.1), §5–§6 (pp.7–10) and the Appendix B count tables plus the D.3 header and first table. I did not read the full appendix or Figures 5+ (Appendix E).
- The pairing finding is an absence in the main text, not proof that pairing is absent.
- The arithmetic check takes the published per-type counts as each method's denominator. UltraEval could have used an undisclosed subset.
- The pdftotext extraction was spot-read against the table layout, not compared visually with the rendered PDF.
- Literal-reference coverage only: this is not a judgement that the knowledge file's claims are supported semantically.

## Verdict

**PASS (scoped):** S057 reopened from the original arXiv v3/ICLR 2025 full text on 2026-10-21. The anchor, teaches, scope and tier are confirmed, and so are all three stated unresolved limits; the denominator limit is now made concrete by the Table 2 UltraEval mismatch. The C2 literal citations (one frozen file, three lines) are fully covered by used-by with status `mined`, and no mutable-cell change is warranted. This verdict covers S057 only, not S056, S038 or the round.
