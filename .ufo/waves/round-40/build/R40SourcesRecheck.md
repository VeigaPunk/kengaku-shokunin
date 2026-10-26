# R40SourcesRecheck — SOURCES live recheck (kengaku r40 wave 1)

Access date for every fetch below: 2026-10-26.

## Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin kengaku` printed
only `cadence` lines (symbolic `on-release` rows S005 S006 S023 S026 S027 S028 S046 S052 S061–S076 …) and **zero `overdue`
lines** (`... | grep -v cadence` → empty, count 0). No dated/NNd row is due by 2026-10-26 (earliest 90d rows,
opened 2026-10-19, fall due 2027-01-17). So the 4 rows were chosen by drift risk: live pages whose version/date can move
without notice — S046, S052 (Python docs pinned "3.15.0"), S005 (OpenAI, challenge-served), S027 (SciPy manual version).
S006, S065, S071 were checked as free by-products (same pages).

## Row 1 — S046 (Python `re`) — CHANGE (locator only; claim holds)
- URL https://docs.python.org/3/library/re.html ; page title now "re — Regular expression operations — Python 3.15.2 documentation".
- Quote (§Special sequences, `\s`): "Matches Unicode whitespace characters (as defined by str.isspace()). This includes [ \t\n\r\f\v]" — `\r` present, claim holds.
- Drift: row anchor says "Python 3.15.0 docs"; live is 3.15.2. sha256 of fetched bytes `a99c3e85983a8aba2073827e0e34ee3b0925ddd57b4251584da7a8e9a46877cd` (257,706 B, curl). Row pins no hash.
- Draft: anchor `Python 3.15.0 docs, Regular expression syntax, special sequence backslash-s; opened 2026-10-21` → `…; opened 2026-10-21; rechecked 2026-10-26 against Python 3.15.2 docs, same text`. status `mined`→`mined`; recheck `on-release`→`on-release` (unchanged).

## Row 2 — S052 (json `raw_decode`) — CHANGE (locator only; claim holds)
- URL https://docs.python.org/3/library/json.html#json.JSONDecoder.raw_decode ; title "json — JSON encoder and decoder — Python 3.15.2 documentation".
- Quote: "return a 2-tuple of the Python representation and the index in s where the document ended. This can be used to decode a JSON document from a string that may have extraneous data at the end." (≈ 35 words in source; the quoted span is the second sentence: "may have extraneous data at the end".)
- sha256 of fetched bytes `1af0ba1d859bb4134d23b26446bb53735d0b48769a6947d36958ff1937aec8b7` (116,112 B). Row pins no hash.
- Draft: anchor `Python 3.15.0 documentation, JSONDecoder.raw_decode` → `Python 3.15.0 documentation, JSONDecoder.raw_decode; rechecked 2026-10-26 on 3.15.2, same text`. status/recheck unchanged.

## Row 3 — S005 (OpenAI, SWE-bench Verified) — NO CHANGE to claim; gate-evidence note
- URL https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ ; reader fetch OK (curl alone = 403, 9,843 B Cloudflare challenge, sha `ba992e72…`, i.e. same byte count as the gate's recorded `8bd40cbc…`, already disclosed in gate.md §Access-time capture caveat — hash mismatch is not a finding).
- Located quote (§"Too narrow and too wide tests"): "We found that 59.4% of the 138 problems contained material issues in test design and/or problem description" — verbatim match. Date line "February 23, 2026" and H1 "Why SWE-bench Verified no longer measures frontier coding capabilities" match the row.
- Retirement claim confirmed: "This is why we have stopped reporting SWE-bench Verified scores" (intro).
- Draft: none required. Optional: note in row `rechecked 2026-10-26 via reader, quote verbatim`.

## Row 4 — S027 (SciPy BinomTestResult.proportion_ci) — NO CHANGE
- URL https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html ; page title "proportion_ci — SciPy v1.18.0 Manual"; footer date "Jun 19, 2026"; sha256 `f814ec0f37b40bee7d8165fa589d48b810c64b7dd2706284d27da5364a95a5e8` (29,658 B).
- Quote: "'exact': Use the Clopper-Pearson exact method [1]." and example `ConfidenceInterval(low=0.05819170033997342, high=0.26739600249700846)` for binomtest(k=7, n=50, p=0.1) — matches row's 0.0581917…–0.2673960….
- Release check: https://docs.scipy.org/doc/scipy/release.html lists 1.18.0 as newest ("SciPy 1.18.0 Release Notes" first, then 1.17.1) → the manual in the row is still current; recheck=on-release not yet triggered.

## By-products (same Python json page, 3.15.2)
- S065 (NaN/Infinity): "Infinite and NaN number values are accepted and output" — holds; row says "Python3.15.1" → live 3.15.2, optional locator note.
- S071: "this module's serializer sets ensure_ascii=True by default, thus escaping the output so that the resulting strings only contain printable ASCII characters"; BOM: "This module's deserializer raises a ValueError when an initial BOM is present"; repeats: "ignores all but the last name-value pair for a given name" — all hold. Row's line-number anchors (§576-591, 581-582, 402, 254, 624-625) refer to a source rendering not reproduced here; I did NOT verify them (page text is HTML; line numbers not comparable) — unresolved, not a finding.
- S006 (OpenAI, Pro audit; reader fetch OK): "we estimate that ~30% of SWE-bench Pro tasks are broken" and "we retract our earlier recommendation to adopt SWE-Bench Pro"; date July 8, 2026 — row holds.

## Changes drafted (for L1)
1. S046 anchor: add `; rechecked 2026-10-26 on Python 3.15.2 docs` (version 3.15.0→3.15.2).
2. S052 anchor: add `; rechecked 2026-10-26 on Python 3.15.2 docs`.
Status/recheck/tier/used-by unchanged on all rows; no row rejected. Optional same-style note on S065 (3.15.1→3.15.2).
Row-census caveat: `sources-census.sh` validate reads `opened` only; recheck dates live in anchor text, so no column edit is needed.

Scratch `/fast/scratch/hyaku/kengaku-r40/R40SourcesRecheck` removed on completion. No lane files edited.

VERDICT: sources-rechecked-4-changes-2
