# SrcStatsmodelsConfint — round 25, axis C1 (novelty), source opening

## Behavior
Opened the primary statsmodels docs page for `proportion_confint` (stable, version 0.15.0) and drafted ONE candidate SOURCES row. No lane file written; no live model/endpoint requests; scratch fetch only in /tmp.

## Gate receipt
- URL opened: https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html (HTTP 200, `curl -sSL`, UA Mozilla/5.0; reader view also returned the page).
- Access date: 2026-10-20 (local, `date +%Y-%m-%d`); UTC fetch stamp 2026-10-21T00:16:13Z.
- Bytes: 87351 B, sha256 `1d677c9b5ba15e3b4bbe135e547277fe489ff09f9e0fe9dfaf72733d712c61f2`, saved as /tmp/kengaku-r25-sm-proportion_confint.html (scratch, not committed). Hash is of raw HTML, not of rendered text.
- Revision: raw bytes contain the string `0.15.0` (4 hits, `grep -c`). The reader view also shows `meta-docbuild:last-update: Aug 27, 2026`; that string is NOT in the raw bytes (reader metadata only), so it is not used as anchor.

## Verbatim quotes (verified in raw bytes)
1. "Beta, the Clopper-Pearson exact interval has coverage at least 1-alpha, but is in general conservative." (15 words) — Notes, paragraph 1 (line-wrapped after "1-alpha,"); `grep -c` = 1.
2. "the coverage will be only 1 - alpha/2 in the case of “beta”" (13 words) — Notes, paragraph 2, sentence beginning "In the extreme case when count is zero or equal to nobs," (`<cite>` markup inside the sentence; confirmed by tr-joined grep).
3. "Clopper-Pearson interval based on Beta distribution" (6 words) — Parameters, `method` list item for "beta"; `grep -c` = 1.
Also confirmed in raw: "The “beta” and “jeffreys” interval are central, they use alpha/2 in each" (Notes, paragraph 2).

## Draft SOURCES row (contract v1, 11 columns, id left as S0??)
```
| S0?? | statsmodels.stats.proportion.proportion_confint — https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html | docs | A | statsmodels' definition of method='beta' (Clopper–Pearson) and its boundary-coverage caveat; not a proof of CP correctness | Parameters, `method` 'beta' item; Notes ¶1–2; statsmodels 0.15.0 stable page, raw sha256 1d677c9b…61f2 | 'beta' is the central Clopper–Pearson interval (alpha/2 per tail, alpha not adjusted at boundaries), so at count=0 or count=nobs its coverage is only 1 − alpha/2; a stdlib exact-CP needs boundary tests against this reference | queued | 2026-10-20 | on-release | — |
```
Column check: 11 cells, no `|` inside any cell. Tier A is scoped to statsmodels' documented definition only (official docs); it does not grant A for CP's statistical properties.

## Findings for C1 (not admitted; for the integrator)
- Opened-date note: the assignment says `opened 2026-10-20`; that matches the local date. The UTC fetch stamp is 2026-10-21T00:16:13Z. Integrator should keep 2026-10-20 or record the UTC stamp in the round Gate.
- Boundary caveat (quote 2) means a stdlib CP implementation must be checked at count=0 and count=nobs against statsmodels' numeric output before the lane claims agreement. This was NOT run here (scribe scope); it is a check for the executor/integrator.
- Quote 2 documents statsmodels' stated coverage at the boundary; it does not itself state the mathematical CP limit. Do not cite it as proof of the CP coverage figure.
- Tier rule (SOURCES rule 1): non-author verification must re-open a sample; the Gate line above gives URL, access date, sha256 and quotes for that re-open.

## Search log (single bounded search: one primary source)
- Query: statsmodels `proportion_confint` docs, stable. Identified 1 (primary docs page). Screened 1. Included 1. Excluded 0. Stop rationale: primary page opened and quotes verified; no secondary source was needed for this row.

## Installs / updates
None. Used pre-installed `curl`, `sha256sum`, `grep`, `tr`, `date`. No pacman, uv or npm transactions.

## Out of scope / not done
- No lane file written (no SOURCES.md edit, no plans/* edit, no git/jj mutation).
- No statsmodels source-module (`_modules/.../proportion.html`) fetch; not required for the docs-scope row.
- No live model or endpoint requests.

VERDICT: statsmodels docs page opened (HTTP 200, sha256 1d677c9b…61f2, 87351 B, 2026-10-20); one queued tier-A docs row drafted for scope "method='beta' definition and boundary caveat"; quotes verified in raw bytes; row id left S0??.
