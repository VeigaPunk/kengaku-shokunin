# E10NoharmRuns — scoped findings (round-55 w1)

Measured at lane tip `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (clean shared clone).
Full per-check table, commands, and outputs: `E10NoharmRuns/report.md` and the seven
`<name>.txt` receipts in this directory.

**No-harm verdict: round-55 bytes have harmed no standing gate that was green at base.**
6 of 7 standing checks green at tip (grader 733/733 PASS exit 0; grader selftest ALL
PASS; r52-c2 registry selftest cases=3 failures=0; r55-c2 controls selftest cases=4
failures=0; defect ledger rows=5 closed=5 mismatches=0 exit 0; r54-c2 entrytruth
selftest 7/7 PASS).

**Finding (pre-existing, not round-55 harm):** `plans/round51_surfaces.py --lane <clone>`
exits 1 with `PREDICATE R51-C1 fail` at tip — and byte-identically at base
`798f5e9ef30ef39291295565209b65a17343c00e` (receipt `r51-surfaces-base.txt`):
- `STALE SF20`: probe `http://127.0.0.1:1234/health` connection refused (live-service
  probe not running in this environment).
- `NUMBER-DRIFT SF14`: manifest row claims 171 SOURCES rows, probe counts 193 (row never
  re-baselined after later row additions; identical at base).
Anchors themselves are whole: `ANCHORS total=20 dup=0 missing=0`, sections 20/20 covered.
Consistent with the open L0 `kengaku | round-51` listed unanswered in
`plans/round-55-claims.md`.

No sibling-file defects observed. No lane writes; scratch deleted.
