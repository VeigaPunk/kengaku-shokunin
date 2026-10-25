ATTACKS: non-author re-open of SOURCES S033 (Rogan & Gladen 1978, PMID 623091) — refetched the gate URL myself, byte-compared quote/location/hash, cross-checked Europe PMC and publisher access, and read every lane cell that leans on the row.

Scratch: /tmp/k25w2-ReopenS033 (fetched bytes only). Live lane read-only: no git/jj, no file writes outside this report.

Re-fetch (gate.md:19 URL, verbatim):
`curl -L 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=623091&retmode=xml'`
→ HTTP 200, bytes=3323, sha256 `f7abdc9070c541963124f8fdcce0c169305afa9c00f19696f50e2363460c41a2` — **exact match** to gate.md:19, on two independent fetches (byte-identical, so the gate's "dynamic page may hash differently" caveat does not even apply here).

Per-cell verdicts:
- gate.md:19 quote — AGREE. Exact fixed-string match occurs **once** in the XML; 17 words (≤25); the source typo `adjustmants` is present in the bytes, so "source typo kept" is honest.
- gate.md:19 location "Abstract (AbstractText…)" — AGREE. The sentence sits inside the single `<AbstractText>` element (no Label); the typo token appears nowhere else in the record.
- SOURCES.md:55 identity — AGREE. EFetch `<ArticleTitle>` = "Estimating prevalence from the results of a screening test."; `<AuthorList>` = Rogan W J, Gladen B; `<Journal>` Am J Epidemiol; Volume 107, Issue 1, PubDate 1978 Jan; `<MedlinePgn>` 71-6 → "71–76"; `<ArticleId IdType="doi">` 10.1093/oxfordjournals.aje.a112510, identical to the row URL.
- SOURCES.md:55 anchor "EFetch cross-checked with Europe PMC" — AGREE, independently reproduced: EPMC `EXT_ID:623091 AND SRC:MED` returns 1 hit whose `abstractText` is **character-identical** to the EFetch abstract (python equality = True), same DOI/title.
- SOURCES.md:55 anchor "publisher full text HTTP 403" — AGREE. `curl -L https://doi.org/…a112510` → final academic.oup.com/aje/article/104051/ESTIMATING, **HTTP 403**; direct academic.oup.com/aje/article/107/1/71/97097 → **HTTP 403**. EPMC `isOpenAccess=N, inEPMC=N, inPMC=N, hasPDF=N`; EPMC's own `fullTextUrlList` marks the abstract "Free"/the DOI "Subscription required" — so no open full text existed to read; abstract-only is the maximum available access, not a shortcut.
- SOURCES.md:55 scope "the formula is not in the opened bytes" — AGREE and unavoidable: the abstract contains no equation/`se`/`sp` notation (regex `[=<>^]|\bse\b|\bsp\b` = no match). The row does not claim the formula from S033.
- SOURCES.md:55 tier A — AGREE with the in-repo contract (SOURCES.md:10-12: A includes "original paper") **and** the tier is bounded by the scope cell, as the repo requires; the anchor names the access route, so a reader cannot mistake an abstract read for a full-text read. Residual observation only: tier A on an abstract-only read is the most generous reading the contract permits, mitigated by the explicit scope.
- SOURCES.md:55 teaches "under an imperfect test … reported as bounds" — PARTIAL nuance, non-breaking: the abstract never uses "imperfect"/"sensitivity"/"specificity" and says nothing about bounds; it says positive-test frequency "is shown to be a bad estimate". The qualifier is an inference from the abstract's opening ("screening tests … separate people with disease from people without"), and the bounds application is the lane's own. Downstream prose keeps the attribution clean: corpus/knowledge/attribution-interval-calibration.md:63 quotes S033 only for the bias claim and at :67-68 assigns the adjustment formula to S011 §4.2, while :94 states the full text was not opened; :1 lists S033 as "Abstract".
- Landed-tip vs worktree — AGREE: `git show HEAD:corpus/SOURCES.md` (HEAD 8ea41f9ed) carries the same S033 row at :55 and `git show HEAD:…/gate.md` the same row at :19, byte-identical to the worktree lines verified above (the worktree's +2/+8-line diffs touch no S033 line).
- Registry hygiene — AGREE: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, rc=0; `used-by` path exists; `opened 2026-10-20` legal per RevengeCensusTZ (strict `>`, UTC-only).

What breaks: nothing. What survives: hash, quote, location, identity, anchor, scope honesty. Only soft spot is the "imperfect test"/"bounds" paraphrase in the `teaches` cell, which is a stated lane application, not a source quotation.

VERDICT: SURVIVES — S033 re-fetches byte-identical (sha256 f7abdc90…), quote verbatim at 17 words in AbstractText with the source typo intact, Europe PMC cross-check character-equal, publisher and EPMC full text confirmed unavailable (403 / not OA), tier and scope honest; teaches-cell paraphrase is inference but disclosed and not load-bearing.
Installs: none (curl, python3, sha256sum sufficed; no pacman/uv/npm transactions).
