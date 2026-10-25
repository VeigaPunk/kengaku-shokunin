ATTACKS: S009 v4 §4.2 Table 3 — column headers + Ref-5 flip-rate cells; test the correction "FLASK 40.53–48.58%" (corpus/knowledge/llm-judge-calibration.md:89-93).

Source opened: https://arxiv.org/html/2506.22316 -> arXiv:2506.22316v4 [cs.CL] 03 Feb 2026 (sha256 3aa84ebb…b55f3); PDF /pdf/2506.22316v4 (sha256 1ea7b239…b744). Abs page lists [v4] as latest. HTML table id `S4.T3`; PDF pdftotext -layout lines 443-479.

Headers (HTML `<th>` incl. spans; PDF lines 450-451 identical):
  Model[rowspan2] | Perturbation[rowspan2] | BiGGen Bench[colspan2] | FLASK[colspan2] | MT Bench[colspan2] | Vicuna Bench[colspan2]
  subheader under each dataset: FR | MAD   (i.e. four FR/MAD pairs)
Caption (S4.T3): "Stability metrics FP (%) and MAD … The perturbation method Ref-5 was only applied to BiGGen Bench and FLASK, as the other two datasets do not provide reference answers."
Naming note: header says FR, caption/Eq.(3) say FP, §4.2 prose says "FRs" — all denote the same flip fraction 1/n·ΣI(s⁽ᵖ⁾≠s⁽⁰⁾). Source-internal label mismatch only; the column is the flip rate.

Ref-5 rows (cell order: BiGGen FR, BiGGen MAD, FLASK FR, FLASK MAD, then four "-"):
  GPT-4o                     45.54  0.5604 | 45.58  0.7166 | - - - -   (HTML row 7; PDF:456)
  DeepSeek-V3-671B           38.99  0.4863 | 45.13  0.6742 | - - - -   (PDF:463)
  Qwen3-32B                  37.59  0.7674 | 44.58  0.6512 | - - - -   (PDF:468)
  Qwen3-8B                   36.48  0.4367 | 40.53  0.5712 | - - - -   (PDF:473)
  Mistral-Small-24B-Instruct 35.40  0.4065 | 48.58  0.6247 | - - - -   (PDF:478)

Counterexample search: 48.58 occurs exactly once in the v4 PDF (478) and once in the HTML — the FLASK/FR cell of Mistral. No text paragraph, figure or second table reports it; MT Bench/Vicuna Ref-5 cells are "-" in all five rows, matching the caption. HTML and PDF agree on all ten FR cells.

FALSIFIED (the W3 misread): "48 appears only in an unlabelled 4th column" (.ufo/waves/kaika-w3/kengaku-review.md F3). Each dataset header carries colspan=2; a colspan-blind parse yields 6 header cells against 8 metric cells and invents unlabelled columns. FLASK/FR is metric column 3 of 8, and 48.58 is its Mistral cell.

ANALYSIS: FLASK FR range = 40.53 (Qwen3-8B) to 48.58 (Mistral-Small-24B-Instruct); all five FLASK cells lie inside. BiGGen FR range = 35.40 (Mistral) to 45.54 (GPT-4o); all five inside. So "40.53–48.58% on FLASK" is correct, as is "35.40–45.54%"/"35–49%". No number is misattributed.

Caveats (not breaks): (1) Ref-5, FR/MAD and "Stability" occur only in v4 — v1/v2/v3 HTML counts are all 0 (no stability table at all); the unversioned URL and SOURCES.md:31 both pin v4, so the correction is valid but is version-scoped and should say "v4". (2) "Exact cells" labels a min–max range; the endpoints are exact cells, the range is derived. (3) Line 27's "~45–48%" remains committed and is superseded only by the append (append-only contract).

Downstream effect: RevF3.md:14 ("do not include 48.58% as Ref-5 unless … identified") is falsified — the column and cell are identified above. corpus/lessons/round-25.md:50 "48.58% column unverified" is stale; F3's numerical substance was already correct at `8ea41f9ed` (file clean, text verified via git show).

VERDICT: SURVIVES — "40.53–48.58% on FLASK" is the exact Ref-5 FLASK/FR min–max (min Qwen3-8B 40.53, max Mistral-Small-24B-Instruct 48.58) in S009 v4 Table 3, whose columns are FR/MAD under colspan-2 BiGGen Bench/FLASK/MT Bench/Vicuna Bench headers; only the W3 "unlabelled column" objection and the downstream "unverified" status break.
Installs: none (pdftotext /usr/bin/pdftotext pre-existing; no packages, uv, or binaries installed; no pacman run).
