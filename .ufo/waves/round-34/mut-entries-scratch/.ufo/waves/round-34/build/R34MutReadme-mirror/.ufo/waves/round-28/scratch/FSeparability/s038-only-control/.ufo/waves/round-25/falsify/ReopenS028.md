ATTACKS: SOURCES row S028 (statsmodels `proportion_confint` docs) — non-author re-open: fetch the gate.md URL, re-verify both quotes verbatim + location, anchor, tier/scope, sha256, and try to falsify the teaches-cell boundary assertion.

FETCH (2026-10-20 21:48 -03): `curl -sSL https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html` → HTTP 200, 87351 B, sha256 `1d677c9b5ba15e3b4bbe135e547277fe489ff09f9e0fe9dfaf72733d712c61f2` = gate.md:12-13 byte-for-byte. Second fetch → same hash, `etag: "6ad738fd-15537"`, `last-modified: Tue, 20 Oct 2026 09:48:45 GMT`, `content-length: 87351`; page is static, so the "dynamic page" caveat is not in play here.

QUOTE 1 (gate.md:12, "Notes ¶1 (0.15.0 stable)"): page text contains the exact substring `Beta, the Clopper-Pearson exact interval has coverage at least 1-alpha, but is in general conservative.` (15 words, ASCII hyphen in "Clopper-Pearson", period present). Paragraph count in the `<p class="rubric">Notes</p>` block: ¶1 is that sentence + "Most of the other methods…". AGREE.

QUOTE 2 (gate.md:13, "Notes ¶2"): exact substring `the coverage will be only 1 - alpha/2 in the case of “beta”` (13 words, curly quotes U+201C/201D preserved, spaces around `-` preserved). Page context: "In the extreme case when count is zero or equal to nobs, then the coverage will be…" — ¶2 is "The “beta” and “jeffreys” interval are central, …". AGREE. Non-breaking clip: the quote starts after "then", so the boundary condition lives in ¶2 but outside the quoted span; the SOURCES teaches cell restores it ("at count 0 or count = nobs"), so nothing is mis-scoped.

ANCHOR (SOURCES.md:50, "Parameters → method 'beta'; Notes ¶1–2; statsmodels 0.15.0 stable page"): `<dt class="field-odd">Parameters:` exists; under `method` the bullet list has `beta : Clopper-Pearson interval based on Beta distribution`; h1 + title read `…proportion_confint — statsmodels 0.15.0`; Notes rubric precedes the two quoted paragraphs. AGREE.

TIER/SCOPE (SOURCES.md:50: `docs | A | statsmodels' definition of method='beta' (Clopper–Pearson) and its boundary-coverage note`): contract v1 (`corpus/SOURCES.md:10-15`) lists "official docs" under A, so `docs`+A is correct; the scope names statsmodels as the authority and claims no numeric agreement or general CP correctness. AGREE.

TEACHES (SOURCES.md:50): "central" ← ¶2 ("The “beta” and “jeffreys” interval are central"); "conservative in general" ← ¶1; boundary coverage ← ¶2. Trailing clause "exactly where every stored attribution verdict sits" checked against `corpus/evidence/round25-calibration/attrib-calibration-summary.txt:49`: `stored_verdicts=7` = 5 PASS at k=n (20/20, 22/22, 20/20, 30/30, 10/10) + 2 FAIL at 0/0; every TARGET/STREAM TARGET line (9/9, 10/10, 0/0) is also a boundary. AGREE.

COUNTEREXAMPLE HUNT (failed): grepped `probe-r19-*.log` and all other `corpus/evidence/*.log` for a stored/target verdict at 0<k<n — none exist (r19 probes are health probes, not accuracy verdicts), so "every stored attribution verdict" survives a broad reading, not just the nine-receipt one.

NON-BREAKING DELTAS: (1) the integrated scope dropped the wave-1 scribe's hedge `; not a proof of CP correctness` (`.ufo/waves/round-25/build/SrcStatsmodelsConfint.md:20`), while sibling S027 keeps its analogous "not proof of any other implementation's correctness" — a scope-guard asymmetry, but the integrated text still attributes both facts to statsmodels, so no overclaim; (2) SOURCES teaches renders `1 − alpha/2` with U+2212 vs the source's ASCII `1 - alpha/2` — typography only, and teaches is not a quote field.

Per cell: quote1 agree · quote2 agree (clip noted) · location agree · anchor agree · tier agree · scope agree · sha256 agree. No lane file written; scratch only in /tmp/k25w2-ReopenS028.

VERDICT: SURVIVES — every required S028 cell re-derives from independently re-fetched bytes; only two cosmetic/integration deltas, neither a false statement.
Installs: none (curl + python3 already present; no pacman/uv/npm).
