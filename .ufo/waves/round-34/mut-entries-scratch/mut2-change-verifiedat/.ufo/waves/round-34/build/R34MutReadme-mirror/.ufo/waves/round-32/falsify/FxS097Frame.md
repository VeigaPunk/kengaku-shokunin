# FxS097Frame — attack on the drafted entry's S097 section (C1, coverage)

Target: `corpus/knowledge/benchmark-grader-semantics.md` §S097 (uncommitted draft), source S097 = arXiv 2412.05579v2. Assignment: fetch the arXiv abstract page, verify the five-part sentence verbatim, attack the entry's inference ("meta-evaluation is its own part, so a grader's kind decides which validation protocol applies"), and report a verdict per sub-claim.

## Fetch identity (independent re-fetch)

- URL: `https://arxiv.org/abs/2412.05579v2`, fetched 2026-10-25 via `curl -sSL` (Mozilla UA).
- Saved copy: `/tmp/r32f-FxS097Frame/arxiv-2412.05579v2.html`
- SHA-256: `44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660` — byte-identical to the build seat's saved copy (`R32SrcS097.md` §Fetch identity). Byte count 43,661.
- Page metadata verified from my own fetch: TITLE `LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods`; AUTHORS `Haitao Li, Qian Dong, Junjie Chen, Huixue Su, Yujia Zhou, Qingyao Ai, Ziyi Ye, Yiqun Liu`; DATELINE `[Submitted on 7 Dec 2024 (v1), last revised 10 Dec 2024 (this version, v2)]`; COMMENTS `60 pages, comprehensive and continuously updated`; no `jref` cell present (`JREF-CLASS-FOUND: False`), only the arXiv DataCite DOI `10.48550/arXiv.2412.05579` (2 occurrences). Preprint identity confirmed.
- Tool installs: none (curl + Python stdlib; pacman paused host-wide).

## Sub-claim 1 — five-part sentence verbatim in the abstract: **PASS**

Abstract blockquote (`<blockquote class="abstract mathjax">`) of my fetched v2 page contains, byte-exact:

> `This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.`

- Byte-exact containment check: `QUOTE-PRESENT-BYTE-EXACT: True`, offset 471 in the abstract text, preceded by `...natural language. ` and followed by ` We begin by providing...` (full abstract read at `/tmp/r32f-FxS097Frame/abstract.txt:1`).
- Word count annotation in the draft (`— 20 words`): verified, 20 whitespace-words (177 chars).
- Casing check: quote uses `LLMs-as-judges` (lowercase j), matching the abstract exactly (the *title* caps it as `LLMs-as-Judges`; the draft quotes the abstract, not the title — same).
- The sentence sits inside a longer abstract (200 words); the draft quotes only the parts-naming sentence, which is the sentence that carries the claim.

## Sub-claim 2 — premise "meta-evaluation is its own part": **SUPPORTED by the abstract**

The abstract names five *key perspectives* and lists Meta-evaluation as one of them, separately from Methodology (same sentence, sub-claim 1). The abstract's continuation also allocates a distinct discussion to evaluating the judges: `...we investigate the potential domains for their application (Where to use LLM judges?) and discuss methods for evaluating them in various contexts (How to evaluate LLM judges?).` (full abstract, line 1). Enumeration and separate-treatment support "its own part" and "kept distinct from methodology". No contradiction found anywhere in the abstract.

## Sub-claim 3 — consequence "so a grader's kind decides which validation protocol applies": **NOT IN THE ABSTRACT (extrapolation)**

The abstract contains no statement about benchmark graders, validation protocols, deterministic comparisons vs LLM judges, or any rule that a grader's kind determines which meta-evaluation protocol applies. The abstract's only methodology-adjacent content is about *constructing* evaluation systems with LLMs (`Then we address methodology to construct an evaluation system with LLMs (How to use LLM judges?)`) — the mechanics of using LLMs as judges, not a taxonomy for classifying benchmark grading code. The causal link "meta-evaluation is its own part → a grader's kind decides which validation protocol applies" is the entry's own inference, not a paraphrase of the abstract. This is the strongest counterexample available: if the entry presented that consequence as abstract-derived, the quote would not support it.

## Sub-claim 4 — is the inference labelled as the entry's own framing? **YES**

The draft is explicit, twice: `This entry reads that structure as a taxonomic hint, not as a prescription` and `That classification is this entry's own framing; the abstract itself only separates the parts.` (draft lines 63-67). No misattribution to the survey; no false provenance.

## Sub-claim 5 — does the entry add intent the abstract lacks? **YES, but disclosed**

The prescriptive consequence (grader kind → validation protocol choice; deterministic comparison needs no judge meta-evaluation, LLM judge does) is added intent absent from the abstract. It is transparently flagged as the entry's own framing (sub-claim 4). Minor gloss worth noting: the heading `S097 — the survey frame: meta-evaluation is its own part` and the sentence `Meta-evaluation is kept distinct from methodology` are presented as readings of the survey rather than flagged as own framing — but both are faithful to the enumeration and the separate discussion clause, so this is not a distortion.

## Verdict per sub-claim

| Sub-claim | Verdict |
|---|---|
| 1. Five-part sentence verbatim | PASS (byte-exact, v2 page, 20 words as annotated) |
| 2. Abstract supports "meta-evaluation is its own part" | SUPPORTED (enumeration + separate discussion clause) |
| 3. Abstract supports "grader's kind decides validation protocol" | NOT SUPPORTED (entry's own extrapolation) |
| 4. Inference labelled as own framing | YES (explicit "This entry's own framing") |
| 5. Entry adds intent abstract lacks | YES — disclosed; no hidden source attribution |

Net: the S097 section survives this attack. The quote is verbatim and the inference is honestly self-attributed; the only material finding is that the causal consequence has no abstract basis — which the entry already declares. No falsification of C1's S097 row; kill-rule quote location resolves at the pinned v2 revision.

VERDICT: attack-finished
