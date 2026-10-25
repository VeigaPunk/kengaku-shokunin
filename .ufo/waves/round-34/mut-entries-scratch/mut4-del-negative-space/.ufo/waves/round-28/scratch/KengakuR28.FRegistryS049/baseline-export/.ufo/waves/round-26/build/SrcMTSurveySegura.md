# SrcMTSurveySegura — C1 prior art: Segura, Fraser, Sanchez, Ruiz-Cortés, "A Survey on Metamorphic Testing" (IEEE TSE 42(9), 2016)

## Fetch provenance (bytes opened this round)
- URL: https://eprints.whiterose.ac.uk/id/eprint/110335/1/segura16-tse.pdf
- Cmd: `curl -sSL --max-time 90 -w '...' -o /tmp/kengaku-r26-srcmt/segura16-tse_whiterose.pdf <URL>`
- Out: `HTTP=200 URL=<same> BYTES=928560 TYPE=application/pdf`; `file`: PDF 1.7, 21 pages
- sha256(fetched bytes): `69014375eab2316bc5d98f4754be5bcc30eaddd43db3f7b251d949511e4c3376`
- Accessed: 2026-10-21T06:52:49Z (UTC)
- Version: **Accepted Version** (p.1 header: "Changes were made to this version by the publisher prior to publication"); record of record: IEEE TSE 42(9):805–824, Sept 2016, DOI 10.1109/TSE.2016.2532875; deposited via Univ. of Sheffield, White Rose Research Online eprint 110335
- 2nd-copy attempt: https://www.isa.us.es/sites/default/files/segura16-tse_1.pdf → `curl: (60) SSL certificate ... unable to get local issuer certificate (20)`, HTTP=000, 0 bytes (unreachable from this host; not retried with weakened TLS)
- Text: `pdftotext -layout` (pdftotext 26.08.0, poppler, preinstalled — no installs) → /tmp/kengaku-r26-srcmt/segura16-tse.txt sha256 `3a70748b535452425ab6acf8a35684452bf678758b992406e279e0e2516a4f42`; line refs below = that file.

## Verbatim quote — definition of metamorphic relation
> "In general, a metamorphic relation for a function f is expressed as a relation among a series of function inputs"

20 words, verbatim and contiguous (the original sentence continues with the input/output variables and citation).
- Location: **Section 2 "Metamorphic Testing", opening paragraph, manuscript p. 3, left column** (accepted version; extracted lines 144–148; page verified by form-feed split + printed footer "3"). Accepted-version pagination ≠ version of record (805–824); no mapping claimed.
- Companion process sentence (same p.3, lines 136–138): "If the outputs of a source test case and its follow–up test case violate the metamorphic relation, the metamorphic test case is said to have failed, indicating that the program under test contains a bug."

## SOURCES tier
- **A (primary).** The paper itself via publisher DOI (IEEE Xplore doc 7422146, paywalled) and author-affiliated institutional repositories (White Rose/Sheffield = fetched bytes; isa.us.es = authors' ASERG group site, TLS-broken here). Institutional ≠ community; ResearchGate/scispace hits exist and stay ≤B.
- Caveat to carry: bytes are the accepted version, not the IEEE version of record.

## Teaches (one line)
When no oracle exists, test an expected relation among several program executions — transform a source input into follow-up inputs and check the relation linking their outputs, never a single output.

## Prior-art verdict for C1 (verdict-invariance testing of an answer grader/extractor under response-format perturbation)
- **NO — this survey publishes neither the method nor tooling for it.** Term sweep over fetched text (`grep -ci`): grader 0, LLM 0, extractor 0, perturb 0; "answer" 5 (survey prose, e.g. line 245 "based on the answer to the previous questions"); "invarian" 4 (all program-invariant/Daikon sense, lines 163, 1062, 1149, 1495); "judged" 1 (line 871, metamorphic fault-tolerance trustworthiness — not grading).
- Closest published analogues, all targeting the program under test, none a grader/extractor audit: search-engine MRs `Count(q) ≥ Count(q+k)` on Google/Yahoo (lines 167–175); ML-classifier MRs, Murphy et al. six relations + Xie et al. supervised classifiers (lines 737–760); compiler "equivalent variant" relations (lines 809–810). Nearest to a judge: Amsterdam's heuristic test oracle — a function deciding whether outputs are "close enough" to equal, used as an oracle helper inside MT of *other* programs (lines 584–586) — still not verdict-invariance of an answer grader under response-format perturbation.
- Tooling named: METRIC, KABU/MDT, Corduroy, Amsterdam; "Only two of the papers (2%) presented a tool as their main contribution" (lines 370–371). None perturbs stored answers and rechecks a grader's verdicts; no CP-style invariance intervals.
- Relation to C1 construct: the lane's audit *is* metamorphic testing with grader.py as the program under test — source case = stored `raw` response, follow-up = perturbed response, relation = extracted verdict invariant (meaning-preserving families; G1–G2 as expected-change controls). The survey supplies exactly this vocabulary/framework (verified above) but does not anticipate the application, so it grounds the audit's method framing without blocking the C1 +1. Honesty note: 2016 ML-classifier MRs are adjacent (relations over learned-function inputs) — they test the learned algorithm, not a judge's invariance under output-format mutation of stored responses.

## Installs
None (pdftotext/poppler 26.08.0 and curl preinstalled; pacman untouched per host pause).

VERDICT: Opened accepted-version PDF (White Rose, HTTP 200, sha256 69014375…3376); MR definition quoted from §2 p.3; tier A; teaches relation-based oracle replacement; does NOT publish grader/extractor verdict-invariance under response-format perturbation → no C1 blocker, framework citation only.
