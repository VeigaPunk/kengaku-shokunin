# Round 25 — SrcScipyBinomtest (C1 frontier source)

Seat: KengakuR25.SrcScipyBinomtest · leaf scribe · no lane file written · no git/jj mutation · no delegation.

## Behavior
Opened the primary SciPy 1.18.0 reference pages for `scipy.stats.binomtest` and `BinomTestResult.proportion_ci`. Both opened on the first attempt; no fallback sources were needed.

## Gate receipt
| field | value |
|---|---|
| URL opened (method) | https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html (read via reader; raw bytes via curl -sSL) |
| second page opened | https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html (raw bytes via curl) |
| access time (system clock, UTC) | 2026-10-21T00:16:22Z (contract "today" is 2026-10-20; the row's `opened` field uses the contract date as instructed) |
| HTTP | 200 both; 29658 B (proportion_ci), 33798 B (binomtest) |
| sha256 proportion_ci raw bytes | f814ec0f37b40bee7d8165fa589d48b810c64b7dd2706284d27da5364a95a5e8 |
| sha256 binomtest raw bytes | 0f161b5a7127b6616c8ba13fe39bbe73ac73abfe2633e2c5e93626bb39bfa5cb |
| doc version | `meta-docsearch:version: 1.18.0`, page title "proportion_ci — SciPy v1.18.0 Manual", build stamp Jun 19, 2026 |
| grep proof | `grep -n "Use the Clopper-Pearson exact method" <raw proportion_ci html>` → line 546 |

Quote (≤25 words), location = `BinomTestResult.proportion_ci` page, **Parameters → method → `'exact'` bullet**, body text (not a header or frontmatter):
> "‘exact’ : Use the Clopper-Pearson exact method [1]." — 7 tokens including the `‘exact’` label, 6 words after it.

Also confirmed on the same page: `method` default is `'exact'`, and the `wilson`/`wilsoncc` options are Wilson score with/without continuity correction (cites Wilson 1927 and Newcombe 1998), so a `wilson()` cross-check in `plans/attrib_calibration.py` can be pinned to the same documented formula family. The `binomtest` page's own example gives `binomtest(k=7, n=50, p=0.1).proportion_ci()` = `ConfidenceInterval(low=0.05819170033997342, high=0.26739600249700846)`. That is a usable external numeric anchor for a `clopper_pearson(7,50)` unit test (verify against the implementation, not against this report).

## Draft SOURCES.md row (contract-v1, 11 columns; NOT written to the lane)
```
| S0?? | SciPy — `scipy.stats.binomtest` and `BinomTestResult.proportion_ci` (v1.18.0 manual), https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html | docs | A | exact (Clopper–Pearson) two-sided binomial proportion CI as implemented by a mainstream stats library; `method='exact'` is the documented default | proportion_ci → Parameters → method → `'exact'` bullet; v1.18.0, build Jun 19 2026 | Names the reference implementation for the Clopper–Pearson interval and its `wilson`/`wilsoncc` siblings, giving an external numeric anchor (`binomtest(k=7,n=50,p=0.1).proportion_ci()` = 0.0581917…–0.2673960…) to test our `clopper_pearson` against | queued | 2026-10-20 | 180d | — |
```

Tier note: A is scoped to the claim "SciPy's documented method='exact' is Clopper–Pearson" only. It is not evidence that our implementation is correct; that requires our own numeric test against the anchor above. A second non-author check should re-open the sample.

## Findings
- `proportion_ci` docs state the exact method is Clopper–Pearson, citing Clopper & Pearson 1934 (Biometrika 26(4):404–413), with Wilson/Newcombe as the other two methods. This matches the lane's round-25 pre-registration intent (exact CP intervals for overall, per-leg recall and specificity).
- `binomtest` docs example numbers above are a checkable anchor. I did not compute them locally in this seat (scope: open source, draft row). The main agent or a verifier should run `clopper_pearson(7,50)` once to confirm the interval matches to ~1e-9.
- No existing SOURCES.md row cites SciPy or Clopper–Pearson (`grep -n -i "clopper\|binomtest\|scipy" corpus/SOURCES.md` → no output), so this is not a duplicate.
- Frontier: no SOURCES row written by this seat; the id stays `S0??` for the integration owner to assign.

## Installs
None. Used only curl, sha256sum, grep, date (preinstalled).

## Out of scope / not done
- Did not write `corpus/SOURCES.md`, any lane file, or any knowledge entry (per contract).
- Did not open Wilson 1927 or Newcombe 1998 primary sources; cited only as the SciPy docs cite them.

VERDICT: SciPy 1.18.0 `binomtest`/`proportion_ci` docs opened (200, sha256 recorded), `method='exact'` = Clopper–Pearson quoted with location; one draft row (S0??, A-tier scoped to the documented method only) ready for integration.
