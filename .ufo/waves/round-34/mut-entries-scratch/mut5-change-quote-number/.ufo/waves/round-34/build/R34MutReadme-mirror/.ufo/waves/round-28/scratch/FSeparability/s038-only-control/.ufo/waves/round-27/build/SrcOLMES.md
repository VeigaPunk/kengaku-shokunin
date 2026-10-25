# SrcOLMES: OLMES (arXiv 2406.08446) answer formats and extraction; prior-art check for C1

Access date for every source: 2026-10-21. Round 27, leaf scout. Only this file was written. Scratch files are in /tmp/kengaku-r27-SrcOLMES-scratch/ (PDFs, extracted text, shallow and blobless clones). No live model or endpoint calls.

## Sources
- S-A arXiv v2 PDF, https://arxiv.org/pdf/2406.08446v2. Latest arXiv version ("last revised 11 Feb 2025"); https://arxiv.org/abs/2406.08446v3 returns HTTP 404. 29 pp; sha256 769ceafbf5f99bf62e579b3b54630b5e0f95852493ef0284182b6f6ff583f8cf.
- S-B arXiv v1 PDF, https://arxiv.org/pdf/2406.08446v1. Submitted 12 Jun 2024; sha256 1b86a94bd3394a5473a72a9fd299257fba8e0552eea1f9c2e3cc7017977b2a1f.
- S-C Published: Findings of NAACL 2025, pp. 5020-5048, DOI 10.18653/v1/2025.findings-naacl.282, https://aclanthology.org/2025.findings-naacl.282/ (PDF sha256 3ca4698cbebdaea1a389cb174829b72f7aec9870f920236b8ce9a5b530c78793). Quotes 1-12 below also appear verbatim in S-C on the same PDF page.
- S-D Code, https://github.com/allenai/olmes at commit 5a51f502d463b8cdc4a2dcad7d7096c41ff1197e (2026-03-24).
- Page = PDF page index. Every quote was checked verbatim by per-page pdftotext search (apostrophes and whitespace normalized). Every quote is at most 25 words.

## What the paper says about answer formats and extraction
1. Output interpretation is an admitted choice. S-A p.1: "there are many choices in how the task is presented to the model and how the model outputs are interpreted before scoring" (22 w). S-B p.1 and S-C p.1 read the same.
2. MCF definition, S-A s.2.1 p.3: "presenting answer choices indicated by labels and scoring prediction of answer labels" (12 w).
3. MCF is scored by label log-likelihood, not by parsing generated text. S-A App. C.2 p.18: "the evaluation metric involves just scoring the log-likelihood corresponding to the answer choice label" (14 w). CF ranks answer strings after normalization (s.3.3 p.5).
4. Label formats. S-A s.3.1 p.4 lists label variants under "formatting the answer labels" ("A.", "(A)", "<mc>A</mc>"). OLMES fixes " A." with a leading space so the label token matches the answer token (p.4; App. C.3 p.22). Exact prompt formats are in App. H (p.25).
5. Extraction is deferred. S-A s.6 p.9: "This will include standardizing how answers are extracted for evaluation" (10 w). S-B p.9 reads "This encompasses standardizing how answers are extracted for evaluation" (9 w).
6. Scope. S-A Limitations p.10: "This paper focuses on design choices in evaluating language models with multiple-choice tasks" (13 w).
7. Processing claim. S-A s.1 p.2: "to processing models’ outputs, so there are no ambiguities in the evaluation procedure" (13 w). In context this covers MCQA scoring only (items 3, 5, 6).
8. Formulation gap. S-A s.3.4 p.6: "78.6% vs 60.2% for the 25-shot CF on the Hugging Face Open LLM Leaderboard" (14 w). S-B p.6 reads "78.6% vs 59.2%", so the paper's own figure changed between versions.
9. Best-of reporting. S-A s.3.4 p.7: "and the best performing one is used" (7 w). S-D README.md:57-58: "trying both multiple-choice and cloze formulations, and reporting the max".
10. Measured robustness. S-A App. A p.17: "the largest difference seen is 1.4%" (6 w). This is likelihood-scored MCQA under prompt-wording and shot variants only; the sentence is absent from S-B.
11. Adjacent. S-A Fig. 1 p.7: "the model starts gaining the ability on the MCF format" (10 w). The MCF signal depends on training stage.
12. Cited, not opened. S-A p.1: "claiming as much as an 80% difference in accuracy on a given task just from varying formatting" (17 w; Sclar et al. 2023).

## Code evidence (S-D @5a51f502; not in the paper)
- oe_eval/configs/regexes.py:1-13 OLMO_3_REGEXES: an ordered ladder, from "Therefore, the answer is" (l.2) to "anywhere in the text" (l.12).
- oe_eval/metrics/metric.py:505-531: when exact_match_flex is configured, answer_format_correct below the cutoff (default 0.5, l.507) blanks strict model_answer (l.531). Flex keeps the fallback answer (l.526).
- oe_eval/tasks/oe_eval_tasks/bbh.py:222-244: the first regex tier that matches wins. found[-1] takes the last match inside that tier.
- bbh.py:236 uses a non-raw literal "\b([A-Z])\b", which Python reads as a backspace. Replicated: findall on "The answer is B." returns [] (the raw pattern returns ['B']), so this tier cannot match ordinary text for BBH MC categories (gated at l.235). [verified by replication]
- bbh.py:224-237: .append mutates the config's shared template list. Replicated: 1 -> 7 entries after 3 calls. [INFERENCE: growth only; verdicts unchanged because duplicate tiers come last]
- oe_eval/tasks/oe_eval_tasks/mmlu.py:281-314: the strict format takes the last match (l.293); fallbacks use the first match (re.search, l.305); every fallback sets the flag to 0 (l.308); the nominal scores 0.5/0.25/0 are never read (l.304).
- oe_eval/configs/tasks.py:314-347, coqa_mc:0shot-chat::gen2mc: a generated letter is parsed via answer_format_regex (l.335). This is generative MC extraction, the area S-A defers.
- oe_eval/configs/tasks.py: primary_metric "exact_match_flex" on 20 configs (e.g., l.3067, 4620, 5781, 7421). Lenient extraction is the headline number for those tasks.
- oe_eval/tasks/base_task.py:607-637: the MC path issues one loglikelihood request per choice.
- Git (blobless clone; git log -S and --diff-filter=A): answer_format_correct_cutoff first appears in tasks.py at d3ef9bf (2025-03-24, sync commit), after S-A and before S-C. regexes.py was added at 1c8a3c9 (2025-07-09, sync commit), after S-C. These are sync dates, not design dates.

## Prior-art judgment for C1 (novelty)
- Not prior art for C1's measured construct. OLMES has no extraction variant, no re-parse of generated text, and no cross-policy verdict agreement. It names the gap as open (S-A p.9; S-C p.9). It does not refute a +1 for C1; that still depends on the wider prior-art search by the other seats.
- In-kind harness precedent only: ordered regex tiers, strict and flex dual metrics, and flex as primary in 20 configs (S-D). This supports "published in kind, unmeasured". It is not a published agreement measurement.
- Cautions: the 1.4-point variance (item 10) is likelihood-scored MCQA and does not transfer to generated-text extraction. Cite the paper with its version (59.2 in v1; 60.2 in v2 and S-C).
- Leads for SrcPriorArtPapers, cited by S-A and not opened: arXiv:2310.11324 (Sclar et al.), arXiv:2402.01781 (Alzahrani et al.), arXiv:2402.01349 (Wang et al., "Beyond the answers"), Mai and Liang 2024 (HELM MMLU).
- SOURCES gate material for the integrator (no row written): items 1-3 and 5-10 above with the S-A and S-C URLs, plus the S-D path:line evidence.

Installs: none. Tools used were already present: git 2.56.0, curl, poppler pdfinfo and pdftotext, Python stdlib. uv 0.13.0 is present and unused. No pacman, sudo, or host changes.

VERDICT: OLMES is not prior art for extraction-policy sensitivity. It defers answer-extraction standardization to future work (S-A p.9) and measures only formulation and prompt effects, while its released harness implements ordered regex tiers and strict/flex reporting without measuring cross-policy agreement.
