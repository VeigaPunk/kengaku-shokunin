# E6RowAudit07 — independent R54-C2 row audit

Clone: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit07/clone` (shared clone of current lane tip).
Runner imported `plans/round54_c2_entrytruth.py` from that clone and called `hermetic_env(tmp)` for each invocation; TMPDIR and helper temp dirs were under the seat scratch. Per-row timeout: 600 seconds. All commands are entry mode and each script exists in the clone. Evidence fragment is N/A for all three green declarations (ledger carries no `evidence` field; red-row-only requirement).

## git-webserver-probe

Declared exit: `0`; observed exit: `0`; entry mode: True; script exists: True; fragment-match: N/A; verdict: **CONFIRMED**; elapsed: 53.5s.

Exact argv: `python3 plans/git_webserver_probe.py --lane .`

Observed output tail (up to 5000 chars):
```text
" | "'" | 'Test completed'
CASE bom tools=curl predicted=fail observed=fail match=yes -- verify.sh:63 — a byte-order mark is part of the content
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | 'Web server test successful (HTTP 200)' | 'Content: \ufeffhello world' | '❌ TEST FAILED: Content does not match expected output' | "Expected: 'hello world'" | "Got: '\ufeffhello world'" | 'Test completed'
CASE empty-200 tools=curl predicted=fail observed=fail match=yes -- verify.sh:63 — an empty body is not 'hello world'
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | 'Web server test successful (HTTP 200)' | 'Content: ' | '❌ TEST FAILED: Content does not match expected output' | "Expected: 'hello world'" | "Got: ''" | 'Test completed'
CASE not-found tools=curl predicted=fail observed=fail match=yes -- verify.sh:59 — a 404 for /hello.html skips the content branch
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | '❌ TEST FAILED: Web server returned HTTP 404' | 'Test completed'
CASE http-500-right-body tools=curl predicted=fail observed=fail match=yes -- verify.sh:59 — the status must be exactly 200 even when the body is right
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | '❌ TEST FAILED: Web server returned HTTP 500' | 'Test completed'
CASE redirect-301 tools=curl predicted=fail observed=fail match=yes -- verify.sh:57 — curl runs without -L, so a redirect is a non-200 status
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | '❌ TEST FAILED: Web server returned HTTP 301' | 'Test completed'
CASE catch-all-200 tools=curl predicted=pass observed=pass match=yes -- verify.sh:57,60 — only /hello.html is requested; a server answering every path passes
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | 'Web server test successful (HTTP 200)' | 'Content: hello world' | '✅ TEST PASSED: Content matches expected output' | 'Test completed'
CASE wrong-port-8081 tools=curl predicted=fail observed=fail match=yes -- instruction.md:7 — 'a webserver running on port 8080'; nothing on :8080
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | '❌ TEST FAILED: Web server returned HTTP 000' | 'Test completed'
CASE token-in-body tools=curl predicted=pass observed=pass match=yes -- test_outputs.py:13 — the verdict is a substring of verify.sh's stdout, and verify.sh:62 echoes the body
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | 'Web server test successful (HTTP 200)' | 'Content: TEST PASSED' | '❌ TEST FAILED: Content does not match expected output' | "Expected: 'hello world'" | "Got: 'TEST PASSED'" | 'Test completed'
CASE status-then-content-split tools=curl predicted=pass observed=pass match=yes -- verify.sh:57,60 — status and content come from two separate requests; the first body is never compared
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | 'Web server test successful (HTTP 200)' | 'Content: hello world' | '✅ TEST PASSED: Content matches expected output' | 'Test completed'
CASE first-request-404 tools=curl predicted=fail observed=fail match=yes -- verify.sh:57-59 — the first request's status decides whether the content is fetched at all
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | '❌ TEST FAILED: Web server returned HTTP 404' | 'Test completed'
CASE slow-server-3s tools=curl predicted=pass observed=pass match=yes -- verify.sh:57,60 — curl is run without a timeout, so a slow answer still counts
  grader-stdout: 'Testing web server...' | 'Using curl to test web server...' | 'Web server test successful (HTTP 200)' | 'Content: hello world' | '✅ TEST PASSED: Content matches expected output' | 'Test completed'
CASE wget-static-file tools=wget predicted=pass observed=pass match=yes -- verify.sh:73-80 — the wget branch, taken when curl is absent, compares the same content
  grader-stdout: 'Testing web server...' | 'Using wget to test web server...' | 'Web server test successful' | 'Content: hello world' | '✅ TEST PASSED: Content matches expected output' | 'Test completed'
CASE wget-404 tools=wget predicted=fail observed=fail match=yes -- verify.sh:75-76 — wget exits nonzero on 404, so the content branch is skipped
  grader-stdout: 'Testing web server...' | 'Using wget to test web server...' | '❌ TEST FAILED: Web server could not be reached' | 'Test completed'
CASE wget-token-in-body tools=wget predicted=pass observed=pass match=yes -- test_outputs.py:13 with verify.sh:79 — the body echo carries the token on the wget branch too
  grader-stdout: 'Testing web server...' | 'Using wget to test web server...' | 'Web server test successful' | 'Content: TEST PASSED' | '❌ TEST FAILED: Content does not match expected output' | "Expected: 'hello world'" | "Got: 'TEST PASSED'" | 'Test completed'
cases=22 observed_pass=9 observed_fail=13 mismatches=0
```

## grader-perturb

Declared exit: `0`; observed exit: `0`; entry mode: True; script exists: True; fragment-match: N/A; verdict: **CONFIRMED**; elapsed: 0.5s.

Exact argv: `python3 plans/grader_perturb.py --summary`

Observed output tail (up to 5000 chars):
```text
[0/0;0/0]cp95_nominal=[0.000,1.000] BARE=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000]
FAMILY F2 kind=MP n=1819 k=1802 rate=0.990654 cp95_nominal=[0.985079,0.994547] verdict=PASS composite=194/187@0.963918 cp95_nominal=[0.927072,0.985372] unit=file+pid;C=file+cell+rep composite_verdict=INDETERMINATE
CLASSES F2 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/14@0.452[17/0;14/14]cp95_nominal=[0.273,0.640] DANGLE=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000] BARE=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000]
FAMILY F3 kind=MP n=1964 k=1964 rate=1.000000 cp95_nominal=[0.998124,1.000000] verdict=PASS composite=210/210@1.000000 cp95_nominal=[0.982587,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F3 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=88/88@1.000[9/9;79/79]cp95_nominal=[0.959,1.000]
FAMILY F4 kind=MP n=1720 k=1720 rate=1.000000 cp95_nominal=[0.997858,1.000000] verdict=PASS composite=158/158@1.000000 cp95_nominal=[0.976923,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F4 FJ1=1143/1143@1.000[703/703;440/440]cp95_nominal=[0.997,1.000] FJM=488/488@1.000[264/264;224/224]cp95_nominal=[0.992,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=54/54@1.000[16/16;38/38]cp95_nominal=[0.934,1.000] BARE=4/4@1.000[0/0;4/4]cp95_nominal=[0.398,1.000]
FAMILY F5 kind=MP n=1964 k=1964 rate=1.000000 cp95_nominal=[0.998124,1.000000] verdict=PASS composite=210/210@1.000000 cp95_nominal=[0.982587,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F5 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=88/88@1.000[9/9;79/79]cp95_nominal=[0.959,1.000]
FAMILY F6 kind=MP n=1964 k=1964 rate=1.000000 cp95_nominal=[0.998124,1.000000] verdict=PASS composite=210/210@1.000000 cp95_nominal=[0.982587,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F6 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=88/88@1.000[9/9;79/79]cp95_nominal=[0.959,1.000]
FAMILY F7 kind=MP n=1876 k=1876 rate=1.000000 cp95_nominal=[0.998036,1.000000] verdict=PASS composite=194/194@1.000000 cp95_nominal=[0.981165,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F7 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000]
FAMILY D1 kind=PC n=909 k=909 capture_rate=1.000000 cp95_nominal=[0.995950,1.000000] verdict=NOT_SCORED composite=129/129@1.000000 cp95_nominal=[0.971809,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=NOT_SCORED
CLASSES D1 FJ1=639/639@1.000[639/639;0/0]cp95_nominal=[0.994,1.000] FJM=244/244@1.000[244/244;0/0]cp95_nominal=[0.985,1.000] MULTI=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000] DANGLE=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] BARE=9/9@1.000[9/9;0/0]cp95_nominal=[0.664,1.000]
FAMILY G1 kind=MC n=1021 k=1021 rate=1.000000 cp95_nominal=[0.996394,1.000000] verdict=PASS composite=143/143@1.000000 cp95_nominal=[0.974534,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES G1 FJ1=710/710@1.000[710/710;0/0]cp95_nominal=[0.995,1.000] FJM=268/268@1.000[268/268;0/0]cp95_nominal=[0.986,1.000] MULTI=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] DANGLE=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] BARE=9/9@1.000[9/9;0/0]cp95_nominal=[0.664,1.000]
FAMILY G2 kind=MC n=1021 k=1021 rate=1.000000 cp95_nominal=[0.996394,1.000000] verdict=PASS composite=143/143@1.000000 cp95_nominal=[0.974534,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES G2 FJ1=710/710@1.000[710/710;0/0]cp95_nominal=[0.995,1.000] FJM=268/268@1.000[268/268;0/0]cp95_nominal=[0.986,1.000] MULTI=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] DANGLE=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] BARE=9/9@1.000[9/9;0/0]cp95_nominal=[0.664,1.000]
FORMATS FJ1=1296 FJM=492 MULTI=31 DANGLE=57 BARE=88
DEDUP raw+want+grader unique_raw_want_grader=1451 duplicate_groups=294 records_in_duplicate_groups=807 excess_duplicate_records=513
NOTE CP95 is nominal/descriptive; neither records nor pid-composites establish independent generalization.
TOTAL population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9
```

## hermetic-grader

Declared exit: `0`; observed exit: `0`; entry mode: True; script exists: True; fragment-match: N/A; verdict: **CONFIRMED**; elapsed: 0.4s.

Exact argv: `python3 grader.py`

Observed output tail (up to 5000 chars):
```text
CHECKS n=733 mismatches=0 errata_pinned=1
VERDICT: PASS — stored evidence fully re-derives offline
```
