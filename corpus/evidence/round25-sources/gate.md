# Round 25 — SOURCES gate receipts (S027–S037, S011 re-open)

Opened by round-25 wave-1 scribe seats (reports under `.ufo/waves/round-25/build/Src*.md`), integrated by
KengakuR25. Access: 2026-10-20 21:16 -03 = 2026-10-21T00:16Z (UTC date one day later; `opened` uses the
local round date, which `scripts/sources-census.sh validate` accepts — `RevengeCensusTZ.md`). Hashes are
access-time captures of the bytes fetched; dynamic or challenge-served pages may hash differently on re-fetch,
so re-verification of these rows is by quote and location, the hash being a receipt of what was read.

| row | URL actually opened | sha256 (fetched bytes) | quote (≤25 words) | location |
|---|---|---|---|---|
| S027 | https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html | f814ec0f37b40bee7d8165fa589d48b810c64b7dd2706284d27da5364a95a5e8 | "‘exact’ : Use the Clopper-Pearson exact method [1]." | Parameters → method → 'exact' bullet (v1.18.0) |
| S028 | https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html | 1d677c9b5ba15e3b4bbe135e547277fe489ff09f9e0fe9dfaf72733d712c61f2 | "Beta, the Clopper-Pearson exact interval has coverage at least 1-alpha, but is in general conservative." | Notes ¶1 (0.15.0 stable) |
| S028 | (same) | (same) | "the coverage will be only 1 - alpha/2 in the case of “beta”" | Notes ¶2 |
| S029 | https://repository.upenn.edu/bitstreams/c3690c8b-efaf-485b-a984-39cfc22aae13/download | 626d61d966ec920bb54e825399383cd0759450cae310c980298fac9beb0b76e0 | "chaotic coverage properties of the Wald interval are far more persistent than is appreciated" | Abstract ¶1, p.101 |
| S029 | (same) | (same) | "we recommend the Wilson interval or the equal-tailed Jeffreys prior interval for small n" | Abstract ¶2, p.101 |
| S030 | https://jhanley.biostat.mcgill.ca/c607/ch08/zero_numerator.pdf | e3150aecd069144dcd81004171348bb7a658852da6e52a2b4e257c23fd746d79 | "we can be 95% confident that the chance of this event is at most three in n (ie, 3/n)" | p.1, Making Inferences: The Rule of Three |
| S031 | https://www.jhanley.biostat.mcgill.ca/c607/ch08/wilson_jasa_1927.pdf | c2fc82b5c7c3fca821d8451dcaae82a047310b32b5bcfb2a4268362a1a438735 | "And this form of statement is not elliptical. It is the proper form of probable inference." | printed p.210, after the range formula (OCR of scan) |
| S032 | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9595616&retmode=xml | e914ec0c036df445fd9476e90a172d9f3bc0d04863df7ddf089da870a7d7ba30 | "Intervals based on tail areas and the simpler score methods are recommended for use." | Abstract, final sentence |
| S033 | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=623091&retmode=xml | f7abdc9070c541963124f8fdcce0c169305afa9c00f19696f50e2363460c41a2 | "frequency of positive tests is shown to be a bad estimate, and the necessary adjustmants are given." | Abstract (AbstractText; source typo kept) |
| S034 | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=24416798&rettype=abstract&retmode=xml | 50f5a105767d6b7ec9f66032a627c242d721254b2f092cd38b78237ad25f12dc | "we propose a new method to construct approximate confidence intervals for the true prevalence when sensitivity and specificity are estimated from independent samples" | Abstract |
| S035 | https://arxiv.org/pdf/2301.09633 | a16bf2c108fea9f559d00708c731d29d673c1dcce5d4acfd65e64a694b7ae17a | "without making any assumptions on the machine-learning algorithm that supplies the predictions" | v4 PDF p.1, Abstract |
| S036 | corpus/evidence/attrib-r23-stream.log (own-work) | afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131 | "STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL" | :239 |
| S037 | plans/attrib_calibration.py (own-work) | output receipt `corpus/evidence/round25-calibration/attrib-calibration-summary.txt` | "transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4" | TOTAL line |
| S011 re-open | https://raw.githubusercontent.com/mlresearch/v306/main/assets/lee26bl/lee26bl.pdf (from the PMLR page's citation_pdf_url) | c1645e31f0f1b6a183ef15ad201b123fb137447897adcea861420f213faa7752 | "Substituting estimates q̂1 and q̂0 into (4) gives the bias-corrected estimator (Rogan & Gladen, 1978; Lang & Reiczigel, 2014)." | §4.2, p.4, before eq. (5) |
| S011 re-open | (same) | (same) | "we construct a confidence interval for θ using the "add two successes and two failures" adjusted Wald approach" | §5.2, p.5 |

Not admitted as rows: Clopper & Pearson 1934 (publisher HTTP 403, JSTOR challenge, Unpaywall closed — lead);
Reiczigel, Földi & Ózsvári 2010 (seat not returned by integration time — not a row). Abstract-only rows S032–S034
are scoped to their abstracts in the `scope` cell; S029, S030, S031 were read from repository/author copies, named
in their `anchor` cells.
