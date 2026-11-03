# FreezeReview — scoped findings (round 63, w1)

Full review with quoted lines, commands and the amendment draft: `.ufo/waves/round-63/w1/attack/freeze-review.md`.

Verdict: **freeze-needs-amendment**. Counts: blocker 2, major 14, minor 8 (24 findings).

| id | severity | finding (doc line) |
|---|---|---|
| FR-01 | blocker | C2 pass criterion stated three ways: "every backticked path resolves" (l.102) vs "≥ 90 %" (l.103) vs counter share ≥ 0.90 plus per-row pointer |
| FR-02 | blocker | C1 coverage counter `CLASS network-service executed=1` is a fixed literal in the probe receipt; satisfied regardless of K1 (l.63) |
| FR-03 | major | C1 predicate sentence differs between doc (l.56–59), `--check-receipt` (spec) and the claim's "same sentence" claim (l.56) |
| FR-04 | major | K1 receipt check is "non-empty" only; "re-derivable" overstated (l.58–62) |
| FR-05 | major | K2 stderr clause "names localhost:8080" is satisfied by pip's own `Looking in indexes:` line and by the argv echo in control-k2.txt:5 (l.57) |
| FR-06 | major | "no network beyond loopback" (l.43) contradicted by shared network namespace in the sandbox design |
| FR-07 | major | "Any seat finds … foreign service" (l.70) not enumerated; SETUP exit 2 outcome undefined |
| FR-08 | major | receipt paths disagree: doc `corpus/evidence/round63/…` (l.62, 63, 81, 109) vs wave `.ufo/waves/round-63/w1/…` |
| FR-09 | major | 41-character base hash in wave spec does not resolve (`git cat-file -t`); doc is correct; spec fix only |
| FR-10 | major | C2 "share no artifact" false: network-service cell and recipe read the C1 probe (l.17–19, 92–96) |
| FR-11 | major | executed-status column has no rule and no check (l.91–92) |
| FR-12 | major | trio gate checks key presence only; fleet CORPUS.md (l.163–170) requires values and S### row |
| FR-13 | major | control receipt control-k2.txt has no producing command (l.72–76) |
| FR-14 | major | ss -ltnp before-state receipt absent from recon/ (l.35–36, 148) |
| FR-15 | major | a K1 server left running makes K2 return P and fires the kill rule spuriously (l.66–67) |
| FR-16 | minor | "committed receipt" (l.126) for trio-red: no such file at freeze |
| FR-17 | minor | CORPUS.md citations (l.21, 124): not in lane; "§2b" not found |
| FR-18 | minor | test.sh pin (SHA256SUMS l.135) omitted from doc |
| FR-19 | minor | control and doc share commit 9ebde3a7; ordering unverifiable |
| FR-20 | minor | S229 unpinned (l.142–143); sha 5b97cb7e… |
| FR-21 | minor | placement wording (l.88–89) differs from wave |
| FR-22 | minor | pip cache/HOME not isolated per case (wave spec) |
| FR-23 | minor | degenerate receipt pointers (same file on all rows) pass C2 |
| FR-24 | major | counter path set (extension whitelist, `/` required) narrower than "every backticked repo-relative path" (l.102) |

Passed checks (with commands): control-k2.txt sha256 `73f1fa33…100c9` and content match doc l.74–75; grader sha256 `82c63517…650be4c` equals doc l.31 and SHA256SUMS l.134; test.sh sha256 `d2b1220e…e7784e` equals SHA256SUMS l.135; census has 16 CLASS lines; network-service count 8; pip accepts `http://localhost` index with no trusted-host flag (own loopback server on 8081, killed by its PID).

Doc amendment needed before data: all blockers and majors except FR-09 (wave spec fix). Draft: `attack/freeze-review.md`, section "Amendment A1 — 2026-11-03, pre-data (FreezeReview)".

Not run: the probe, gate checker and trio gate are not built at this review; the grader was not executed; no K-case was run. Port 8080 untouched.
