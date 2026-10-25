# SrcReiczigelExact — round 25 frontier source (C1 prior art)

Scope: open Reiczigel, Földi & Ózsvári 2010 (doi 10.1017/S0950268810000385) and draft ONE SOURCES row + Gate receipt. No lane file written; no git/jj mutation; no live model/endpoint request. Scratch only in /tmp/kengaku-r25-SrcReiczigelExact.

## Outcome: OPENED (full text), row drafted

Opened via the managed browser tab (omp `browser` tool, headless, hidden, shared) on the publisher's bronze open-access PDF (OpenAlex `best_oa_location`, Semantic Scholar `openAccessPdf`, status BRONZE). Full 5-page text extracted with pdftotext.

## Attempts (what did and did not open)

- `https://doi.org/10.1017/S0950268810000385` via `read`: CrossRef metadata + abstract only (not the article body).
- Cambridge Core PDF `…/0644C396D4364B292419FB0BA1A30BA2/S0950268810000385a.pdf/…` via curl and `read`: HTTP 429 on ~25 attempts over ~25 min (sleep/backoff loop, both before and after cool-down); Cambridge `/core/` probe also 429 (IP-level rate limit).
- PubMed 20196903 via curl: HTTP 203 (bot challenge page); Europe PMC: `isOpenAccess=N`, "Subscription required"; EPMC fullTextXML 404.
- Semantic Scholar landing 202; core.ac.uk 403; europepmc.org article page 403; PMC search page 200 but no article.
- SUCCESS: same Cambridge PDF URL fetched from inside the managed browser tab (`page.evaluate(fetch)`), which the rate limiter did not block.

## Gate receipt

- URL actually opened: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0644C396D4364B292419FB0BA1A30BA2/S0950268810000385a.pdf/div-class-title-exact-confidence-limits-for-prevalence-of-a-disease-with-an-imperfect-diagnostic-test-div.pdf
- Access date/time: 2026-10-20 21:47 local (-03:00; file mtime 2026-10-20 21:47:08 -03:00). Fetched in managed Chromium, hidden tab "reiczigel".
- Bytes: 104191 (PDF 1.3, 5 pages). sha256 of fetched bytes: `55baba7ba660298c34e95cf87f1957113324398e099cddc948397f1c1bd783b3`
  (scratch copy: /tmp/kengaku-r25-SrcReiczigelExact/reiczigel2010-browser.pdf; extracted text rz2010.txt)
- Quote (≤25 words), location: journal p.1675, INTRODUCTION, left column (PDF p.2, line 10–14):
  "This method results in incorrect CIs, whose actual coverage at a nominal level of 95 % can be as low as 60 %, even for large samples." (25 words; text verbatim as printed in the PDF, `95 %` spacing kept)
- Second verified location (not used as the row's quote): journal p.1675, METHODS (PDF p.2): "Blaker's CI has the advantage that it is always contained in the Clopper–Pearson interval"; journal p.1677 CONCLUSION (PDF p.4): "Estimates of disease prevalence may be seriously biased if sensitivity and specificity of the diagnostic test are disregarded."

## Draft SOURCES row (contract v1, 11 columns; NOT written to the lane)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0?? | Exact confidence limits for prevalence of a disease with an imperfect diagnostic test — https://doi.org/10.1017/S0950268810000385 | paper | A | exact two-sided CIs for the sensitivity/specificity-adjusted (Rogan–Gladen) prevalence as this paper reports them | Epidemiol. Infect. 138(11):1674–1678, first published online 2010-03-03; Introduction p.1675, Methods p.1675, Conclusion p.1677 | the naive procedure (Rogan–Gladen-adjusted estimate, then a CI as if observed) can have coverage as low as 60% even for large samples; test-inversion CIs (Blaker, Sterne) on the adjusted scale; Blaker's CI is always contained in the Clopper–Pearson interval, Sterne's may be wider | queued | 2026-10-20 | 2027-04-18 | — |

Column check: 11 cells, no `|` inside any cell; `kind` ∈ enum (paper); `tier` A is the original paper for its own scope; `status` queued (opened, worth mining; no `used-by` path yet, so not `mined`).

## Relevance to C1 (for the integrator; not a claim)

- Supplies the Rogan–Gladen form (eq. 1, p.1674: prevadj = (prevobs + Sp − 1)/(Se + Sp − 1)) and the warning that CIs on the naive adjusted scale are wrong — relevant to the leg-share bound's Se/Sp-interval construction in the frozen C1 rule.
- Does NOT give a CI for accuracy itself; the Clopper–Pearson per-leg intervals are not sourced here.
- Its CP-containment statement supports reporting CP as the conservative exact interval, not a tighter one.

## Failures and gaps

- Only one source opened this assignment; no Wilson/Newcombe rows (other seats).
- Cambridge rate limit persists for curl/read from this host; the browser route is the one that worked.
- The row's `recheck` ISO date (2027-04-18) is 180 days from opened; change to `180d` if the integrator prefers cadence form.

## Tooling

- No installs or updates. Used: omp `browser` (managed Chromium, auto-installed by the tool on first use; version not captured), `pdftotext`/`pdfinfo` from poppler 26.08.0 (preinstalled, `pdftotext -v`), curl, OpenAlex/Semantic Scholar/Europe PMC APIs (read-only metadata).

VERDICT: source opened (full text, 5 pp.) via browser tab after Cambridge curl/read returned 429; one A-tier row drafted with gate receipt, id left S0??; no lane files written.
