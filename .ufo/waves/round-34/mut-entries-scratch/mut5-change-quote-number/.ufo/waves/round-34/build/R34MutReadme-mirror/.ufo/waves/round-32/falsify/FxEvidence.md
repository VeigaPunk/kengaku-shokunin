# FxEvidence — round-32 evidence-packaging review (leaf)

Seat: `L1Kengaku32.FxEvidence` · 2026-10-25 · lane `kengaku-shokunin` @ `6084cd3` (freeze `0d32691d` parent; working tree carries the planned uncommitted land).

Scope per assignment: (a) captures + SHA256SUMS.txt under `.ufo/waves/round-32/assimilation/captures/`; (b) `corpus/evidence/round32/` after-count receipts (adoption, defects, catalogs, V-checks) + catalogs probe JSON; (c) fidelity build reports under `.ufo/waves/round-32/build/`; (d) freeze controls under `.ufo/waves/round-32/claims/`; plus any receipt the claims or Q20 require.

## (a) Captures — PRESENT and internally consistent

- `.ufo/waves/round-32/assimilation/captures/` holds exactly two captures + `SHA256SUMS.txt`:
  - `toolathlon-ab-testing-evaluation-main.py` (14 138 B) — pin `9be8d8fe`
  - `arxiv-2412.05579v2-abs.html` (43 647 B) — pin `2412.05579v2`
- `sha256sum` re-run matches both entries in `SHA256SUMS.txt` byte-for-byte: `3bad26b6…` and `851b03db…`; byte counts also match. Consistent.
- Coverage matches the C1 kill rule: S094 and S097 must resolve this round and are captured; S093's quotes were already pinned in the live row (round 31) — no new S093 capture is required.
- No third/fourth "S093 capture" file is needed; the two captures are the complete required set.

## (c) Fidelity build reports — PRESENT

- `.ufo/waves/round-32/build/` contains 34 `R32*.md` reports (CatProbe, CollisionGuard, ConnSibling, Considerthese, CountersPreflight, CritC1/C2/C3, DraftEntry/Errata/Lesson/Mistakes/Report/Rows/Scorecard, Frontier, GateBlock, LearnC1, MirrorCensus, MutCounters/MutRows, PlanWalk, Quarantine, QuoteMode, ReconPackage, RevClaims/Entry/Fixes/Gate, Sentinel, SentinelScope, SrcS094a/b, SrcS097) + `swarm-registry.json`. 34 fidelity reports present.

## (d) Freeze controls — PRESENT and verified

- `.ufo/waves/round-32/claims/` has all four controls: `adoption-expect.json` (sources S093/S094/S097, access_date 2026-10-25), `control-nothing.txt`, `defects-before.txt`, `catalogs-before.txt`.
- `R32CountersPreflight` verified all three counters reproduce the committed controls byte-identically with matching exit codes (`VERDICT: controls-match`). I re-read the controls: contents match preflight captures.

## Draft state (on-disk, uncommitted) — present and predicate-shaped

- Entry `corpus/knowledge/benchmark-grader-semantics.md`: `verified-at: 2026-10-25`, exactly three `source:` lines (S093/S094/S097, distinct), `writer` line, extends-naming, "What this does not establish" negative space, falsifier. Re-verified against the recon hazards (0.05 call-site tolerance, fail-open log-bucket branch, `LLMs-as-judges` quote) — the draft already incorporates the H3/H5/H7 repairs.
- Rows in `corpus/SOURCES.md`: S094/S097 new (`status=mined`, `opened=2026-10-25`, `used-by` = the entry); S093 live row now carries `used-by` = `benchmark-verifier-execution-model.md, benchmark-grader-semantics.md`; S101/S102 new rows (opened 2026-10-25). Row count 91 → 95.
- `corpus/README.md`: exactly one index row for the entry (line 67); frontier bullets at 255/279 are not index rows.
- `corpus/knowledge/open-model-catalogs.md`: `verified-at: 2026-10-25`, S101/S102 citations, receipt pointer `corpus/evidence/round32/catalogs/after.txt`.

## (b) `corpus/evidence/round32/` — ABSENT (the gap)

The directory does not exist and no file under it exists anywhere in the lane (git status: not created; no seat assigns creating them; the counters do NOT write receipts — `catalog_probe.py`, `round32_defects.py`, `round32_c1_verify.py`, `adoption_check.py` only print stdout). The only plan for these files is the scorecard draft naming them. Missing receipts required by the claims' after-counts and by this assignment:

1. `corpus/evidence/round32/adoption-after.txt` — C1 after-count (`entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0). Plan: scorecard draft line 36. **Missing.**
2. `corpus/evidence/round32/c1-verify-after.txt` — C1 V-checks receipt (`checks=6 defects=0`, exit 0). Plan: scorecard draft line 61. **Missing.**
3. `corpus/evidence/round32/defects-after.txt` — C2 after-count (`checks=7 defects=0`, exit 0). Plan: scorecard draft line 37. **Missing.**
4. `corpus/evidence/round32/catalogs/` — C3 receipts. **Naming mismatch:** the draft entry and the S101/S102 row anchors cite `corpus/evidence/round32/catalogs/after.txt`, while the scorecard plan names `catalogs/catalog-probe-after.txt`. No file exists under either name. A file must land at the cited path (`after.txt`) and the references must agree; the counter only checks the pointer's existence in the entry, not the file, so a missing receipt would still pass `entry_ok` — the receipt must be independently committed. **Missing.**
5. Catalogs probe JSON — the three raw probe bytes (`hf_models_limit50.json` 27 771 B, `openrouter_models.json` 791 130 B, `hf_models_full3.json` 9 238 B) exist only in `/tmp/r32-R32CatProbe/` (plus a copy in `/tmp/r32f-FxC3DiffTruth/`). `R32CatProbe` states it cleaned its tmp dir after handoff — these are the only surviving copies and are not in the repo. Nothing plans copying them into `corpus/evidence/round32/catalogs/`. **Missing from the lane.**

## Q20 — landing gate receipt required, not yet present

- Q20 (QUALITY.md:198-212): a commit touching `plans/*.py` / `corpus/SOURCES.md` must carry a mechanical gate run made in a landing tree (`git archive <sha>`) printing exit codes + pinned count lines, committed with the landing as `.ufo/waves/round-<N>/gate-receipt.txt`.
- The planned landing touches `plans/catalog_probe.py`, `plans/round32_defects.py`, `plans/round32_c1_verify.py`, and `corpus/SOURCES.md` rows → Q20 applies.
- The existing `.ufo/waves/round-32/gate-receipt.txt` covers only the freeze commit `0d32691d` (committed at `6084cd3`); no build/falsify report assigns producing the landing-tree receipt, and it is not in the working tree. The landing must update it, including the touched tools' own rows (catalog_probe/round32_defects/round32_c1_verify/adoption_check selftests) and a fresh `CHECKS n=` line — note `CHECKS n=733` may change because the landing adds registry rows, so the receipt must explain any old→new delta. **Missing (to be produced at land).**

## Additional evidence-consistency observations

- Scorecard draft line 36 says "Registry 91 → 93 rows (S094 and S097 new)" — the actual append is 4 rows (S094/S097/S101/S102) → 95 (`corpus/SOURCES.md` row count 95). The final scorecard/report must state 95, not 93, or the committed corpus contradicts the report.
- `corpus/evidence/round31/gate-cli-exits.txt` (C2 R3 repair) is already modified in the working tree — present on disk.

## VERDICT: gaps
