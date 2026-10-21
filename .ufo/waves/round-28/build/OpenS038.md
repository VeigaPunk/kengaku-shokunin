# OpenS038 — re-opening S038 (and S056) for C2, round 28

Writer/seat: `KengakuR28.OpenS038-2` (read-only scout, author-side; not outside non-author closure).
Scope: re-open the existing row S038 from the original publisher text, open own-work S056 (implementation and committed receipt, not re-run), find literal citations of both IDs in the frozen 35-file C2 population at base `b9b24796277020d1b9b01923b45313d6a565e664`, and suggest changes to allowed mutable cells only. No registry, knowledge or production edits. No new source rows. No installs or updates.
Scratch evidence: `.ufo/waves/round-28/scratch/OpenS038/` (`wb20261004.pdf`, `wb.txt`, `epmc.json`, `unpaywall.json`, `oa.json`, the HTTP 429 bodies `doi.html`/`paper.pdf`/`article.html`).

## S038 — opening record

Row (SOURCES.md:60, identical to base): Reiczigel, Földi & Ózsvári, *Epidemiol. Infect.* 138(11):1674–1678 (2010), https://doi.org/10.1017/S0950268810000385; status `queued`, opened `2026-10-20`, recheck `180d`, used-by `—`.

### Attempts (access date 2026-10-21)

| # | route | result |
|---|---|---|
| 1 | `curl -L` to https://doi.org/10.1017/S0950268810000385 (resolves to Cambridge `product/identifier/...`) | **HTTP 429** "Too many automated requests from this network" |
| 2 | `curl` to the publisher's OA PDF URL (`.../0644C396D4364B292419FB0BA1A30BA2/S0950268810000385a.pdf/div-class-title-...-div.pdf`) | **HTTP 429**. The body is 363 bytes, matching the challenge page in the round-25 spotcheck |
| 3 | headless `chromium --dump-dom` of the Cambridge article page | **HTTP 429** title, 1496 bytes |
| 4 | Europe PMC REST (DOI query) | metadata only: PMID 20196903, no PMCID, `isOpenAccess=N`. No repository full text |
| 5 | Unpaywall / OpenAlex / Semantic Scholar | all report `is_oa=true`, `oa_status=bronze`, publisher `publishedVersion`, and the same Cambridge PDF URL as the only full-text location. OpenAlex reports `any_repository_has_fulltext=false` |
| 6 | **Wayback Machine raw capture** `https://web.archive.org/web/20261004190246id_/<publisher PDF URL>` | **OPENED.** HTTP 200 `application/pdf`, 5 pages, 108614 bytes, sha256 `fc935f40a6f58cb7fea9407490a768fd63078eaf46ccd3b40b260d109de82e8c`. The base32 SHA-1 `GWYEXRXGLWELYZ5D4M3HDN4ZA4K6VJJS` equals the archive CDX digest for that capture. PDF metadata: Creator 3B2 Total Publishing System 7.51g/W, CreationDate 2010-08-18. The page header reads "Epidemiol. Infect. (2010), 138, 1674–1678 … doi:10.1017/S0950268810000385". The footer is the publisher stamp "Downloaded from https://www.cambridge.org/core … on 04 Oct 2026 at 19:02:46" |
| 7 | Cursor WebFetch (isolated server) of the live Cambridge article HTML `https://www.cambridge.org/core/journals/epidemiology-and-infection/article/exact-confidence-limits-for-prevalence-of-a-disease-with-an-imperfect-diagnostic-test/0644C396D4364B292419FB0BA1A30BA2` | **OPENED**: full publisher HTML (Summary, INTRODUCTION, METHODS, SIMULATION RESULTS, EXAMPLE, DISCUSSION, CONCLUSION, References). The tool says it *may* serve cached content, so this is treated as a corroborating second read and not a hashed artifact |

The round-25 gate (`corpus/evidence/round25-sources/gate.md:36`) recorded sha256 `55baba7b…`, which differs from today's `fc935f40…`. [INFERENCE] The mismatch is expected and not a content discrepancy: Cambridge stamps each downloaded copy with a per-download IP and timestamp footer (visible on every page of today's copy). The located quote below is byte-for-byte the round-25 gate quote.

Disclosure: the hashed copy is the publisher's own PDF URL as captured by the Internet Archive on 2026-10-04. It is not a live publisher download from this network, which is rate-limited. The live publisher HTML (attempt 7) gives the same text.

### Located quotes (≤25 words) and verified anchors

- **Introduction, p.1675 (PDF p.2, left column)**, which is the row's anchor: "This method results in incorrect CIs, whose actual coverage at a nominal level of 95 % can be as low as 60 %, even for large samples." (25 words; `wb.txt` lines 80–86, below the page header "… 1675" at line 73.) "This method" is the naive approach that adjusts by Rogan–Gladen "and then calculating a CI using the adjusted prevalence as if that were observed directly".
- **Methods, p.1675**: "Both Blaker's and Sterne's CIs are derived by inverting the corresponding tests." Located by the METHODS header at `wb.txt:110` on p.1675.
- **Discussion, p.1677**: "a 95 % two-sided CI constructed in this way has an actual coverage probability of <60 %, regardless of whether an asymptotic or an exact CI calculation method is applied." This is at Se=85%, Sp=90%, prevalence 3%.
- **Conclusion, p.1677**: "In case of known sensitivity and specificity CIs are easy to adjust by applying the Rogan & Gladen transformation to the CI endpoints." Located by the CONCLUSION header at `wb.txt:256`.

### Narrow scope/teaches check against the opened text

- **Scope** ("exact two-sided intervals for sensitivity/specificity-adjusted (Rogan–Gladen) prevalence as this paper reports them"): **confirmed.** The Summary says "we proposed exact two-sided confidence intervals for the prevalence of disease, taking into account sensitivity and specificity".
- **Anchor** (Introduction p.1675 PDF p.2 left column; Methods p.1675; Conclusion p.1677): **confirmed** by the page headers in the PDF text.
- **Teaches, first clause** (a naive CI on the adjusted estimate can cover as little as 60% at nominal 95%): **confirmed** by the Introduction quote above, with a concrete instance in the Discussion.
- **Teaches, second clause** ("test-inversion (Blaker, Sterne) limits on the adjusted scale fix it"): **confirmed only under known Se/Sp.** The paper's own Discussion caveat (p.1677) reads: "the proposed methods assume that sensitivity and specificity are known exactly … currently it has not been developed for exact intervals" (about estimated Se/Sp).
- **Teaches, third clause** ("a lead for replacing the lane's conservative corner bound"): this is the lane's interpretation, not something the paper says. [INFERENCE] It is weaker than it reads. The citing entry's own setting estimates se/sp "from the same rows" at n = 20–30 (`attribution-interval-calibration.md:143`), which is exactly the case the paper excludes. That entry also already records that calling the bound "conservative" was wrong (line 139ff; CritRgBound). This is in an immutable cell, so the only action is disclosure here or in the lesson. S039 (Lang & Reiczigel 2014, estimated Se/Sp) is the row that covers that case.
- Tier A for this scope (original paper, publisher version): **holds.**

## S056 — own-work opening (not re-run)

- **Implementation:** `plans/parser_policy_compare.py` (595 lines; sha256 `c4296935ed40…5a27`, byte-identical to base; last touched by commit `6356b0b`).
  - `compared_verdicts = sum(tallies[pid]["n"] for pid in alt)` and `disagreements = sum(flips.values())`, where `flips[pid] = flip_pf + flip_fp` over the eight non-`E0` policies (lines 312–319).
  - The TOTAL line is formatted at lines 348–350.
- **Committed receipt:** `corpus/evidence/round27-calibration/policy-final-summary.txt` (sha256 `2c4a9948…15b6`, identical at base; commit `6356b0b`). Its final lines are "`TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`" then "`exit=0`".
  - The flips sum as 17+0+17+1012+26+0+17+0 = 1089 events over E1–E8, and 8 × 1964 = 15712.
  - A single response can flip under several policies (the matrix row E0 lists 17 under each of E1, E3 and E7), so the teaches cell "disagreement events, not 1089 distinct responses" is consistent with the receipt.
- The round-27 lesson gate (`corpus/lessons/round-27.md:49`) quotes the same TOTAL line.

## Literal citations in the frozen 35-file population (base `b9b2479…`)

The citations were recomputed with the population's `reference_pattern` `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` over `git show <base>:<path>` for all 35 paths. All 35 exist at base.

| ID | citing frozen file:line | status | used-by | literal gap |
|---|---|---|---|---|
| S038 | `corpus/knowledge/attribution-interval-calibration.md:144` — "S038 (Reiczigel et al. 2010, Introduction) warns the naive adjusted interval can cover 60% at nominal 95%." | `queued` | `—` | `cited_not_mined` and `missing_used_by` for that path. This is the drift already disclosed in round 27 (`round-27.md:18`), not a new discovery |
| S056 | `corpus/knowledge/extraction-policy-comparison.md:1` (front-matter `source:` line) | `mined` | `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md` | none: the only frozen citing path is listed and the status is `mined` |

Other frozen-file mentions of "Reiczigel" or "Rogan" without the ID (`attribution-interval-calibration.md:35,67,94,115,139,148`) are not literal S038 references and are outside the C2 literal contract. `:67` cites Lang & Reiczigel 2014, which is S039's paper, not S038.

Semantic note (outside C2's literal scope): the line-144 citation matches the opened Introduction (it shortens "can be as low as 60%" to "can cover 60%" but does not overstate it). [INFERENCE] It is used by analogy: the lane's `rg_cond` held the observed share fixed, whereas the paper's warning is about naively treating the adjusted estimate as observed.

## Suggested allowed-cell changes (do not apply here; L1 integrates)

The suggestion is permitted only because the original source was opened today, through the archived publisher PDF with a digest that matches the archive, corroborated by the live publisher HTML.

| ID | cell | old | suggested new |
|---|---|---|---|
| S038 | status | `queued` | `mined` |
| S038 | used-by | `—` | `corpus/knowledge/attribution-interval-calibration.md`, plus `corpus/lessons/round-28.md` if that lesson records the reopen (additional lesson paths are allowed) |
| S038 | recheck | `180d` | unchanged |
| S038 | opened | `2026-10-20` | unchanged. The reopen date 2026-10-21 and today's URL/quote belong in the round-28 lesson Gate, not in this row |
| S038 | id/source/kind/tier/scope/anchor/teaches | — | **unchanged (immutable)**. The scope limit of the teaches clause on estimated Se/Sp (above) should be disclosed in the lesson; if a correction is needed, it is a future superseding row and not an edit |
| S056 | all | — | no change needed |

Expected effect [INFERENCE, not run]: with only these S038 cells changed, the delivered `plans/registry_check.py` logic (lines 72–85: `cited_not_mined` when citing and status ≠ mined; `missing_used_by` for citing minus used-by) would clear both S038 findings. That covers S038 and S056 only. F5 (all 13 rows) depends on the other seats.

## Commands observed

These were read-only and run inside the scratch directory or as git reads: `rg`, `sed`, `awk`, `git show <base>:<path>`, `git diff --stat/--quiet <base>`, `git log --oneline`, `sha256sum`, `pdftotext -layout`, `pdfinfo`, `file`, `curl` (doi.org, Cambridge, Europe PMC, Unpaywall, OpenAlex, Semantic Scholar, Wayback availability/CDX/raw `id_`), one `chromium --headless=new --dump-dom`, and one Cursor WebFetch. No builds, tests, linters, or upstream or benchmark code were executed. No benchmark sites were contacted. No tools were installed or updated.

## Limitations

- The hashed full text is an Internet Archive capture of the publisher PDF URL (2026-10-04), not a live download. The live Cambridge text came through a third-party fetcher that may serve cached content.
- The page and column locations come from `pdftotext -layout`, which shows two-column text side by side. Left-column placement was inferred from the indentation.
- The S056 numbers were opened from the committed receipt and code and were not re-executed (as assigned).
- This is literal-reference completeness for two of the 13 frozen IDs, not a semantic-support or whole-registry check.

## Verdict

**PASS (scoped):**
- S038 was opened from the original publisher text, and its scope, anchor and first teaches clause are confirmed. The second clause holds only for known Se/Sp, and the third is lane interpretation (disclose, do not edit).
- The baseline literal drift for S038 is confirmed at one frozen file, and the allowed-cell repair is suggested (status `mined`, used-by adds the citing knowledge path).
- S056 is opened and consistent with no change needed.

This is not a round-level PASS and not outside closure.
