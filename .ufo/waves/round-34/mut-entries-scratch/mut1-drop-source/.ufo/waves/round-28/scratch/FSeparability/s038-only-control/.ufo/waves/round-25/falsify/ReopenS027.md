ATTACKS: SOURCES S027 (SciPy `proportion_ci`) — independent re-fetch of the gate URL, byte-quote and location check, anchor-cell check against page meta and example, tier/scope honesty, sha256 comparison.

Re-open: `curl -sS -L` (default UA and Mozilla UA, two fetches) on the exact URL in `corpus/SOURCES.md:49` / `corpus/evidence/round25-sources/gate.md:11`
→ HTTP 200, 29658 bytes, effective URL unchanged, sha256 `f814ec0f37b40bee7d8165fa589d48b810c64b7dd2706284d27da5364a95a5e8`
twice = gate sha exactly. Headers: `Last-Modified: Fri, 19 Jun 2026 15:55:28 GMT`, `ETag "73da-6549d52527c00"`, `Content-Length: 29658` — static page, no dynamic mismatch to excuse.

Per-cell verdicts (AGREE unless marked):
- source/URL — AGREE: same URL, 200, no redirect; page title "SciPy v1.18.0 Manual".
- kind `docs` — AGREE.
- tier `A` — AGREE: `corpus/SOURCES.md:11-13` names "official docs" as tier A; tier is scoped, not global.
- scope — AGREE: narrow ("documented definition of method='exact' as Clopper–Pearson and its numeric example; not proof of any other implementation's correctness"); page says exactly that and no more.
- anchor — AGREE: raw HTML has `<dt>‘exact’ :</dt><dd><p>Use the Clopper-Pearson exact method <a …>[1]</a>.</p></dd>` under the `method` parameter field; meta `docsearch:version=1.18.0`, `docbuild:last-update=Jun 19, 2026` match "v1.18.0 manual, build Jun 19 2026".
- teaches — AGREE: Examples block `binomtest(k=7, n=50, p=0.1)` → `statistic 0.14`, `proportion_ci()` → `ConfidenceInterval(low=0.05819170033997342, high=0.26739600249700846)`; row's `7/50 → 0.0581917…–0.2673960…` matches. "Tested against" is real wiring, not prose: `plans/attrib_calibration.py:687-688` (`CP_ANCHORS`, tol 1e-9) and selftest A1 at `:848`; reference [1] on the page is Clopper & Pearson 1934, Biometrika 26(4):404-413.
- gate quote `gate.md:11` — AGREE with a caveat: the quote is the dt term cell + space + dd definition cell, so it is not a contiguous substring of the HTML/visible text (browser shows two columns). Word-for-word and punctuation-exact: `"‘exact’ :"+" "+"Use the Clopper-Pearson exact method [1]." ==` the gate string (asserted True); 8 words ≤25; only one "Clopper-Pearson" occurrence on the page, so no ambiguous bullet.
- sha256 — AGREE, byte-identical (two fetches, two UAs).
- status/opened/recheck/used-by — AGREE: `mined`, 2026-10-20, `on-release` fits a version-pinned manual; `corpus/knowledge/attribution-interval-calibration.md:52` cites S027 only as "the documented reference", inside scope; recheck line `:3` re-opens S027/S028 on-release.
- downstream copy (`corpus/knowledge/attribution-interval-calibration.md:53`) — CAVEAT: renders `'exact'` with ASCII apostrophes where the page has ‘exact’ (U+2018/U+2019). Typographic only; substance identical.

ID collision check: landed registry has S027 = SciPy (`SOURCES.md:49`) and the r23 stream log as S036 (`:58`); the only "S027 = stream log" text is an unlanded build-review draft (`.ufo/waves/round-25/build/RevF7.md:23`), not the registry.

Nothing else fetched or executed; no lane files touched; no pacman/uv/network installs (none needed).

VERDICT: SURVIVES — all cells agree on independent re-open with matching sha256; only cosmetic quote serialization (two definition cells) and downstream ASCII-quote typography, neither falsifies the row. Installs: none.
