# R39SourcesRecheck — SOURCES recheck + W04 census explanation (round 39, wave 1)

Seat: scout, read-only. Access date for every live open below: **2026-10-26** (curl, UTC ~06:53Z). Scratch `/fast/scratch/hyaku/kengaku-r39/R39SourcesRecheck` (removed at end); raw JSON receipts copied to `.ufo/waves/round-39/build/R39SourcesRecheck/` (cigate, evalmut, scipy PyPI JSON).

## 1. Is any row due?

No. Evidence:

- Registry has 109 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 109). `recheck` column histogram (`awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/{gsub(/ /,"",$11);print $11}' corpus/SOURCES.md | sort | uniq -c`): `49 180d`, `19 2027-01-17`, `8 2027-01-19`, `11 90d`, `22 on-release`. So 27 rows carry a future ISO date (none on/before 2026-10-26), 60 carry NNd, 22 `on-release`.
- `scripts/sources-census.sh overdue --file kengaku-shokunin/corpus/SOURCES.md --today 2026-10-26` → 0 `overdue` lines; 82 `cadence` lines (the 60 NNd + 22 on-release rows; the 27 ISO-dated rows are silent because not yet due), exit 0.
- Earliest NNd due date: 90d rows (S014, S024, S025, S036, S037, S041, S045, S047, S056, S060, S114) opened 2026-10-19…26 → due 2027-01-17…24. Same script with `--today 2027-01-17` → 22 `overdue` lines (the first wave). So the first genuine overdue date is **2027-01-17**.
- `on-release` rows (22) are reported, never judged overdue by the census; they are due only when the named upstream cuts a release.

Because nothing is due, I opened the 4 rows with the highest drift risk: two on-release/live-page rows with pinned hashes (S027, S014), and the two PyPI-release 90d rows (S041, S045).

## 2. Live re-opens

### S027 — SciPy `BinomTestResult.proportion_ci` (on-release) — **unchanged**
- URL: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html — HTTP 200, 29658 bytes, 2026-10-26.
- Located quote (page → Parameters → method): “‘exact’ : Use the Clopper-Pearson exact method [1]”. Example: `ConfidenceInterval(low=0.05819170033997342, high=0.26739600249700846)` for k=7, n=50 — matches the row's 7/50 → 0.0581917…–0.2673960… anchor.
- Page footer still `SciPy v1.18.0 Manual`, Sphinx 8.1.3.
- sha256 `f814ec0f37b40bee7d8165fa589d48b810c64b7dd2706284d27da5364a95a5e8` = the pin in `corpus/evidence/round25-sources/gate.md:11` (byte-identical, `sha256sum scipy.html`).
- Release check (the actual `on-release` trigger): `https://pypi.org/pypi/scipy/json` → latest **1.18.1**, uploaded 2026-08-21T23:23:44; 1.18.0 uploaded 2026-06-19T14:59:45 (matches “build Jun 19 2026” in the row anchor). A patch release has happened since the row was opened; the unversioned manual page was NOT rebuilt (still v1.18.0) and the versioned URL `docs.scipy.org/doc/scipy-1.18.1/...` is 404. Claim, quote and numbers unaffected.
- Change: status `mined`→`mined`; recheck `on-release`→`on-release`. No edit recommended. (Optional, not recommended: append “; 1.18.1 patch 2026-08-21, page still v1.18.0 on 2026-10-26” to the anchor — adds drift-prone text for no claim change.) Next trigger: SciPy 1.19.0 or a manual rebuild changing the 7/50 numbers.

### S014 — METR time horizons (90d) — **unchanged**
- URL: https://metr.org/time-horizons/ — HTTP 200, 685041 bytes, 2026-10-26.
- Located quotes: “This page is no longer actively updated.” and, directly beneath, “LAST UPDATED September 8, 2026” — both match the row's anchor (“LAST UPDATED (September 8, 2026)… no-longer-updated notice”). Also “Time Horizon 1.1 (Current)” present and “Measurements above 16 hrs are unreliable with our current task suite” present (row's “stated unreliability above 16h”).
- sha256 now `464067080d7cde66068b8dd28c34a266e5f8bcbfe45b8394d36aadfc092c4cfa` (685,041 B) vs the access-time capture `c5135c54ec56954655010d57fe17ad3b121c8b289c013821fa15be30228627ba` (682,272 B) in `corpus/evidence/round24-sources/gate.md:22`. This is expected: gate.md:112-116 already records that S014 re-hashed differently on 2026-10-20 and that “a hash mismatch alone is not a finding”; verification is by quote/location, which pass.
- Change: none. Page is frozen (“no longer actively updated”), so the 90d re-open is cheap; due 2027-01-17.

### S041 — cigate 0.2.0 PyPI (90d) — **unchanged**
- URL: https://pypi.org/pypi/cigate/json — HTTP 200, 15843 bytes, 2026-10-26. `releases` = `['0.1.0', '0.2.0']`; latest 0.2.0 (upload 2026-07-19T03:46:49); no newer release.
- Located quotes: summary “Eval-gated CI/CD for AI products: gate merges on the confidence-interval lower bound of a bias-corrected LLM-judge score” (info.summary); description: “If the judge is no better than chance (`TPR + TNR ≤ 1`)… CIGate **refuses to gate** that axis” (README, before “Try it in 60 seconds”).
- sha256 `318b81e582a65cab39e5f3011ba751875cbb143fe17c6aefe7e936d1e1bac151` = pin in `corpus/evidence/round25-sources/gate.md:46` (byte-identical).
- Change: none.

### S045 — evalmut 0.1.0 PyPI (90d) — **unchanged**
- URL: https://pypi.org/pypi/evalmut/json — HTTP 200, 14248 bytes, 2026-10-26. `releases` = `['0.1.0']` (upload 2026-08-10T00:05:32), latest 0.1.0 — no newer release.
- Located quote (README §The two ways an eval lies): “Inject an *equivalent* change (a trailing disclaimer after a complete answer, cosmetic whitespace, a JSON code fence)”.
- sha256 `1595963783a1a76218a2325c2a911c531ebe7d9b34966c9165fbd61a6ef1ce18` = pin in `corpus/evidence/round26-sources/gate.md:7` (byte-identical). The row's tarball line anchor (operators.py:614–726) was NOT re-opened (tarball not fetched this seat).
- Change: none.

### Summary table

| row | cadence | live result | hash vs pin | edit old→new |
|---|---|---|---|---|
| S027 | on-release | 1.18.1 patch exists (2026-08-21); page still v1.18.0; quote+numbers match | identical | none |
| S014 | 90d | quote+LAST UPDATED Sep 8 2026 match | differs (known, documented, not a finding) | none |
| S041 | 90d | still 0.2.0; quotes match | identical | none |
| S045 | 90d | still 0.1.0; quote matches | identical | none |

### On bumping `opened`
Considered setting `opened` 2026-10-19/20/21 → 2026-10-26 on S014/S041/S045 (the census derives due = opened + N). **Not recommended**: knowledge entries cite the old due date (`corpus/knowledge/agent-time-horizon-and-task-validity.md:3` “recheck: 2027-01-17 (90d)”), the round-24/25/26 gate.md receipts carry the original open dates, and bumping would make the row-derived due date disagree with the entries (2027-01-24 vs 2027-01-17). A re-open that finds no change is evidence for this report, not a registry edit.

## 3. The 15 W04 census warnings (`census-before.txt`)

Definition: `scripts/sources-census.sh:33` “W04 same URL across scopes (warnings do not affect clean lanes)”; logic at `:643-645`: emitted when a URL was already seen and the (URL, scope) pair is new. A same-URL/same-scope pair instead trips **E04** unless the row says `supersedes S###` (or the earlier row is rejected). `validate` run: `scripts/sources-census.sh validate --file kengaku-shokunin/corpus/SOURCES.md --today 2026-10-26` → exactly these 15 W04 lines, no E-codes, final `ok`, exit 0.

**Verdict: by design, not fix-worthy.** Tier is “scoped to `scope`, never global” (SOURCES.md preamble) and the registry's correction idiom is a *superseding row* with a rewritten scope (SOURCES.md search log: “corrections appended as superseding rows S039, S040, S042”). A superseding row necessarily shares the URL and necessarily changes the scope cell, so W04 fires. “Fixing” would mean merging scopes (destroying the scoped claim each row carries) or editing frozen superseded rows. Grouping (URL → flagged row; I derived this from the registry with a Python column parse):

- Supersession/correction of an earlier row (10): S040→S035, S048→S043, S058→S050, S064→S054, S066→S038, S067→S066, S068→S061, S069→S062, S075→S071, S076→S075 (each `teaches` cell begins `supersedes S###`).
- Extension of the same document on a new facet, no supersession (3): S057 (“extends S044’s abstract-only motivation”), S059 (“extends S053’s §2 grammar”), and S065/S071 (distinct stdlib-json sections: NaN/infinity vs escaping/rejection).
- Different facet of a pinned repo (1): S100 (task-tree entry count) vs S079 (task package schema) on `github.com/laude-institute/terminal-bench-2`.
- Net: 10 supersessions + S057 + S059 + S065 + S071 + S100 = 15.

Not warned (same scope, so no W04): supersession pairs where the scope cell was left identical — S026→S023, S039→S034, S042→S030. Those are legitimate because `teaches` carries `supersedes S###` (else E04).

Optional hygiene, not a defect: if the L1 wants zero warnings, the only mechanical route is census-script tolerance for `supersedes|extends` in `teaches` (fleet-wide script `scripts/sources-census.sh`, outside this lane's write scope; note SOURCES contract v1 is frozen text — PROVINCE.md:187). Rejected as unnecessary: the warning is documented to leave clean lanes clean.

Note on S100/S079: both anchor `github.com/laude-institute/terminal-bench-2`; round 39's C2 admits another TB2 grader row (S117/S118) — if those use the same repo URL with a new scope they will add W04 warnings (expected, by design; census-after should read 15 + that many, never an E-code).

VERDICT: sources-rechecked-4-changes-0
