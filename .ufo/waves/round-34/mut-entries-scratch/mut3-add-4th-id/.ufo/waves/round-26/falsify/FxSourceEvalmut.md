# FxSourceEvalmut — Q10 source re-read

Scope: S045 evalmut prior-art claim and the corresponding Gate quote; S047 local receipt hash also recorded. Read-only; no installs.

## S045 primary-source observations

- PyPI JSON URL: https://pypi.org/pypi/evalmut/json — independently fetched; HTTP 200, 14,248 bytes; SHA-256 `1595963783a1a76218a2325c2a911c531ebe7d9b34966c9165fbd61a6ef1ce18`.
- JSON metadata: `evalmut` version `0.1.0`; sdist upload time `2026-08-10T00:05:33`; sdist URL https://files.pythonhosted.org/packages/b0/42/d57ffbe3c5966b7563f077ba3eb6dd63c0b077a96f58cc79c17f529dedd9/evalmut-0.1.0.tar.gz — HTTP 200, 50,245 bytes, SHA-256 `b633c61734b94b33ad971be4b16951eb13524016b69115eeecc980766d03ad16`, matching the PyPI JSON sdist digest.
- Release README `/tmp/evalmut-x/evalmut-0.1.0/README.md:61-63`, §“The two ways an eval lies”; the located 24-word quote is: “Inject an equivalent change (a trailing disclaimer after a complete answer, cosmetic whitespace, a JSON code fence); a sound grader must still pass it.” The prose matches word-for-word after rendering Markdown emphasis (`*equivalent*` in source); the line location is exact.
- `corpus/SOURCES.md:67` S045 and `corpus/lessons/round-26.md:49` give the matching version/date and README location/quote. The lesson's source-table header at line 45 says access date 2026-10-21.
- The digest-verified sdist contains `evalmut/operators.py`. Its equivalent operators are declared at `:642-649` (trailing disclaimer), `:667-674` (whitespace), `:691-697` (JSON fence), and `:719-726` (case variant). Defect operators are declared at `:249-255` (near-miss number) and `:321-328` (garbage answer); `outcome.py:35-39` defines `DEFECT` as wrong/reject and `EQUIVALENT` as correct/accept. This supports the draft sentence “evalmut 0.1.0 (S045) already ships equivalent-response and defect-response mutations against answer graders.”
- Citation precision caveat: S045's SOURCES.md anchor names `operators.py:614–726`, which covers the equivalent section but not the defect operators/polarity lines. Those defect details are present in the same authenticated release tarball; make the extra locations explicit if the registry anchor is intended to support every clause. This is a locator gap, not a contradiction of the draft claim.

## Numbers and limits

- S045-dependent values checked: version `0.1.0`, upload date `2026-08-10`, README lines `61–63`, and cited equivalent-operator range `614–726`; all match observed source. The score `7` is not a PyPI fact: `plans/round-26-claims.md:199-201` records the lane's novelty decision (held 7, not +1) based on the verified prior art. S045 does not support the draft's separate population/family counts or CP95 results.
- S047 local source: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt`; SHA-256 `75db30f95088b9aa859cf80cc48430a13a3d42adb446410920413f9647f05f29`. Its final line is exactly `selftest: 18 checks, 0 failed` (the file also records `exit=0`); this matches `corpus/lessons/round-26.md:51`. No HTTP status applies to this local file.

## Command evidence

- `curl -sS -o /tmp/evalmut.json -w 'HTTP=%{http_code} SIZE=%{size_download}\n' 'https://pypi.org/pypi/evalmut/json' && sha256sum /tmp/evalmut.json` → `HTTP=200 SIZE=14248`; `1595963783a1a76218a2325c2a911c531ebe7d9b34966c9165fbd61a6ef1ce18  /tmp/evalmut.json` (chain completed successfully).
- `curl -sS -o /tmp/evalmut-0.1.0.tar.gz -w 'HTTP=%{http_code} SIZE=%{size_download}\n' 'https://files.pythonhosted.org/packages/b0/42/d57ffbe3c5966b7563f077ba3eb6dd63c0b077a96f58cc79c17f529dedd9/evalmut-0.1.0.tar.gz' && sha256sum /tmp/evalmut-0.1.0.tar.gz` → `HTTP=200 SIZE=50245`; `b633c61734b94b33ad971be4b16951eb13524016b69115eeecc980766d03ad16  /tmp/evalmut-0.1.0.tar.gz` (chain completed successfully).
- `sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt` → `75db30f95088b9aa859cf80cc48430a13a3d42adb446410920413f9647f05f29`.

VERDICT: PARTIAL — S045 prior-art support and the S047 local quote/hash check pass, with no contradicting source sentence found. The whole proposed entry is not cleared by this source-only seat; Q13 and the remaining admission re-reads are still required. S045's SOURCES anchor should pinpoint the defect-side code if it is meant to substantiate that subclaim.