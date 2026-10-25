# FxClassics — round 32 claim-set attack (UFO-FSD critic, leaf)

Seat: `L1Kengaku32.FxClassics` · 2026-10-25 · lane `kengaku-shokunin` (read-only).
Target: the round-32 claim set as a joint object — (a) R13 double-count, (b) axis
distinctness/labels, (c) measurability, (d) all-three-green-while-lane-false.
Method: read the freeze commit `0d32691d` claims/counters/controls, the current working-tree
drafts, 34 build-wave reports, and ran the three counters live on the draft tree; fetched the
pinned sources (SWE-bench_Pro-os `66f92766` test.sh, Toolathlon `9be8d8fe` main.py + retry.py,
arXiv 2412.05579v2) and byte-checked the quoted spans. Scratch `/tmp/r32f-FxClassics/` (< 1 MB).
No production bytes touched; no tools installed (pacman paused host-wide; nothing needed).

---

## Execution log (evidence)

| Run | Command | Result |
|---|---|---|
| C1 receipt 1 | `python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census` | `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0 |
| C1 receipt 2 | `python3 plans/round32_c1_verify.py --lane .` | `checks=6 defects=0`, exit 0 |
| C2 counter | `python3 plans/round32_defects.py --lane .` | R1, R2, R5, R6, R7 DEFECT; R3, R4 pass; `checks=7 defects=5`, exit 1 |
| C3 counter | `python3 plans/catalog_probe.py --diff --lane .` | `probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=ok`, `HF missing fields: author, sha, lastModified, gated`, **exit 1** |
| Fleet census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | `kengaku ok`, exit 0, 15 `W04` |
| Pin quotes | raw.githubusercontent @ `9be8d8fe…` main.py (14,138 B) + `utils/evaluation/retry.py` (4,519 B); raw.githubusercontent @ `66f92766…` test.sh (7,864 B); arxiv.org/abs/2412.05579 (43,647 B) | all quoted spans resolve (details §E) |
| Receipts | `corpus/evidence/round32/` + `corpus/evidence/round32/catalogs/` | **both directories absent from disk** (not committed, not untracked) |

---

## (a) R13 — double-count / cross-claim artifact reads

1. **C1↔C3 shared-registry coupling (conditional).** C1's `--census` gate runs the fleet
   validator over the whole `corpus/SOURCES.md`, which C3 also appends (S101/S102). C1 green
   therefore depends on C3's new rows being census-clean (an E-level malformed row from C3
   reddens C1 even with C1 bytes perfect). This is a one-way precondition entanglement, not a
   double count of an outcome; the claim's "reads only its own corpus files" phrasing does not
   disclose that its gate sweeps the registry C3 edits.
2. **C1↔C3 share the same append targets** (`SOURCES.md` rows, `README.md` index rows). The
   counters' row-level checks are disjoint (C1 cites S093/S094/S097; C3 cites S101/S102), so
   no measured number is double-counted; the shared *file* is not a shared *artifact read*.
3. **C2 separability holds.** Verified from source (`round32_defects.py` reads only the fleet
   round-31/round-32 reports, `corpus/evidence/round31/gate-cli-exits.txt`, `SKILL.md`,
   lessons 30/31/32) and corroborated by the sentinel. No C1 or C3 byte is read.
4. **C3 reads no C1/C2 artifact** (entry + live APIs only). Its receipt directory
   (`corpus/evidence/round32/catalogs/`) is C3-owned and currently nonexistent (§c).
5. **Freeze controls are shared but read only by C1's V6** (expect-digest pin); C2/C3
   controls are informational. No cross-claim control coupling.
6. **C2 R2's subject is the round-32 fleet report** — itself the lane's delivery vehicle for
   the round story (including C1/C3 narrative). The counter only tests that the final tip
   string appears; it does not read C1/C3 bytes.

**R13 verdict:** no claim double-counts another's measured artifact; one asymmetrical
dependency exists (C1 census gate ⊃ C3 row validity). C2's separability, is the claim, is true.

## (b) Axis distinctness and labels

7. C1→coverage, C2→calibration, C3→freshness; three distinct SCORECARD axes, each mapped to
   that axis's own definition (coverage gap-closure; calibration self-assessment-mismatch
   ledger; freshness re-probe). No two claims share an axis.
8. C1 stays at score 7 with an `improved` ledger trend — consistent with the anti-overclaim
   rubric.
9. C2 records "mismatch count 7 → 0" and holds calibration at 8 — mapping defect-closure onto
   the calibration axis is defensible only because round-31's mismatches *were* self-assessment
   calibration failures; labelled as such, fine.
10. The drafted SCORECARD after-cell for C3 expects `… hf_schema_delta=4 … exit 0` — this is
    **internally inconsistent with the counter**: the counter exits 1 whenever any delta is
    nonzero (§c.1). Draft and code disagree on what "after" looks like.
11. C3's label "freshness" is right; its *metric* is not (§c.3/4/6).
12. No claim duplicates the "novelty" axis or takes credit the non-claims section forbids.

## (c) Measurability

### C3 — not measurable as frozen; the counter cannot exit 0 under any honest landing

13. **Empirical counterexample (strongest).** Live run on the draft tree (entry already
    carries `verified-at: 2026-10-25`, S101/S102, receipt pointer): prints `entry=ok` but
    exits 1 because `hf_schema_delta=4` is non-empty and `main()` requires `not hf_missing`.
    The delta is a property of the live HF default projection (author/sha/lastModified/gated
    absent from 0/50 items), not of the entry. Therefore the repaired state — the state that
    *records* the delta — is exactly the state the counter rejects. `catalogs-before.txt`
    (freeze control) and the draft-tree run print the identical line and identical exit 1:
    before and after are indistinguishable at the exit-code level. The frozen predicate
    ("exits 0") is unsatisfiable unless HF restores the four fields (an API-side event
    outside lane control). **C3 can never go green under any landing that honestly records
    the delta it promised to record.**
14. The counter's exit condition contradicts the claim's own substance: the entry's schema
    delta is the *finding*; exit 0 should require the entry to record the observed deltas,
    not that the deltas be zero.
15. `hf_models=50` is a constant page size (`?limit=50`), not a model count — the predicate's
    `hf_models=<n>` is non-informative for freshness.
16. Schema-delta is sampled from `data[0]` only (both parsers); a heterogeneous catalog is
    certified from one object.
17. One shared status variable drives both `hf=`/`openrouter=` flags; a single API failure
    labels both sources `fail` and zeros both counts — the kill rule's "reachable source
    still counts" cannot be honored (RevClaims already noted this).
18. `--diff` is accepted but performs no comparison (no diff against the 09-28 description,
    no base-file comparison); the counting command's name overstates its function.
19. Receipts are not verified: `entry_ok` checks only that the string
    `corpus/evidence/round32/catalogs/` appears in the entry. The directory does not exist on
    disk; the counter writes no receipts and validates none. The claim can pass with zero
    receipt bytes present.
20. Live-network exit condition: an offline/firewalled host makes the counter exit 1
    regardless of landed state; no pinned-capture replay exists, so the freeze "before"
    control is not reproducible offline.

### C2 — measurable in form, but `defects=0` is not evidence of closure for six of seven checks

21. R1 is token-proximity: explicit negation, wrong-commit, non-erratum "superseded", and
    rewrite+re-supplying-token variants all pass; the counter never runs
    `git cat-file -t` on `a44b5a8` (missing) or `ae95fe0` (commit) though it owns `git()`.
22. R2 is a substring test anywhere in the report (draft denial, stale fence, prefix of a
    longer token all pass); "report exists after the last lane commit" is never evidenced
    (no mtime, no ancestry, no receipt) — it forces a manual re-edit after every lane commit.
23. R2 does not re-derive the routed item: the round-31 report never citing its final commits
    is not checked; R2 scores the *next* round's discipline.
24. R3 checks only the blessed path string and four exit tokens; the executed command can
    still be the wrong path (receipt is a text file with no provenance/run binding).
25. R4's heading scan is first-match-race: an earlier `## …probes` prose section wins over the
    real registry heading; a row can be absent while green, and a correct row can be red if
    earlier prose mentions exist. No table-row/section anchoring.
26. R5 matches `dead` inside `deadline` (`width=160` proximity); explicit negation passes; no
    wave-registry cross-check that the seat has no committed report.
27. R6 tokens are unanchored (`:72` is 3 chars); a question or denial passes; append-only is
    proxied by token presence, so a rewrite plus a note that re-supplies the stale token is
    green.
28. R7 requires only "S086" near "without peer review"/"not peer-reviewed" and a label;
    "S086's erratum is not peer-reviewed either" (the opposite meaning) passes; the registry's
    S086 cell is never cross-read (truth could be wrong in both places).
29. The frozen-seven guard is a self-comparison (`FROZEN` derived from `CHECKS`); deleting R7
    prints `checks=6 defects=0` on an unrepaired tree and exits 0 (mutation M1 survivor —
    independently confirmed by R32MutCounters and R32CritC2).
30. The selftest has no non-empty violating fixture for any check; `near()`→True and guard
    deletions survive (M2/M3/M4), and crash==red (`except Exception: red=True`) hides
    regressions.
31. The working-tree fix skips R1/R2 in the selftest loop entirely — their predicates now
    have zero automated coverage.
32. Both C2 and C3 counters were edited post-freeze (selftest seams; empty-list guards) with
    no committed before-state regeneration; the report skeleton acknowledges for C2 that
    before-controls must be regenerated from final counter bytes — the frozen controls at
    `claims/*-before.txt` are still the original freeze bytes.
33. False-reds exist for honest repairs (R1/R7 natural multi-line markdown fails because
    `near()` cannot cross newlines) — the counter selects for the degenerate one-liner.

### C1 — measurable and green on the true content; truth is process-held, not counter-held

34. The two receipts pass on the draft (adoption exit 0; c1_verify 6/0). The genuine entry's
    quotes resolve at the pins (§E) — C1's state is currently true.
35. Neither counter fetches pins or resolves quotes: the kill rule ("quote must be found at
    the pinned revision") is unreachable mechanically; a cited row whose quote does not exist
    still counts as present/mined/opened/used-by (critic routes B/C).
36. Identity check compares only registry URL host+path against the entry's source line; the
    anchor fragment (e.g. `# README.md` vs `evaluation/main.py`) is spoofable; a ≥3000-byte
    filler body with the right URLs and pin fragments passes all six V-checks.
37. V6 pins the expect digest to the committed control receipt only within the landed tree; an
    actor who mutates both the expect file and the control receipt in the same tree passes V6
    (the pin is a git-history witness, not a counter).
38. Index-row verification is shape-only (title ≥20 chars, description non-empty); a title +
    one-char description cell passes both receipts.
39. Census gate = out-of-lane dependency (§a.1); additionally the census only scans the
    registry, not the entry body.
40. Registry cell access is positional (`[7]/[8]/[10]`) — robust only because the census
    validates the same file; a column reflow breaks both, silently or loudly.

## (d) Can the round report all three green while the lane state is false?

41. **C1: yes.** A counterfeit-but-well-formed entry (fake anchors, unverifiable quotes,
    ≥3KB filler) passes both receipts; the only bars are process (kill rule / second-seat
    re-read), none executable by any counter.
42. **C2: yes.** Minimal-token repairs (negation/redirect lines that leave the defects
    standing) pass; the M1 mutant prints `defects=0` while R7 is untouched.
43. **C3: currently the inverse failure.** The truth state cannot go green (exit 0
    unreachable). After any patch that accepts nonzero deltas, the remaining escapes are live:
    absent receipts, first-item-only sampling, single-status probe, substring-only entry check
    — a green with no evidence bytes.
44. The round as drafted cannot honestly print three green: C3's counter exits 1 on the
    draft, so the scorecard/report after-cells that expect exit 0 with delta 4 cannot be
    realized without changing the counter (freeze discipline: a predicate changed after a seat
    scored is not this claim's predicate) or mislabeling the run.
45. Even the C1/C2 pair needs byte-level review beyond the counters; the report skeleton
    already concedes this for C2 ("counter alone is not self-proving").

## E. Ground-truth positives (verified at pins, 2026-10-25)

46. S093: `test.sh:33` `echo "Resetting test-space to base state (full test-code surface)..."`
    (8 words); `:71` `T) git checkout HEAD -- "$path"`; `:214` `success = all_required <=
    passed_tests` — all resolve at `66f92766…`.
47. S094: `main.py:58` `def validate_record_data(actual_records: dict, expected_records:
    dict, tolerance_pct: float = 0.1) -> None:`; `:70/:72` Missing/Unexpected scenarios;
    `:100` `raise ValueError(f"Record validation failed:\n{error_msg}")`; `:134-139` bucket
    prefix listing; `:217-218` `return True  # Don't fail evaluation if we can't check logs`;
    `:279-280` `# Validate with 0.05% tolerance` + `validate_record_data(…,
    tolerance_pct=0.05)`; `utils/evaluation/retry.py:44-45` `DEFAULT_MAX_ATTEMPTS = 3` /
    `DEFAULT_POLL_S = 5` — all resolve at `9be8d8fe…`.
48. S097: arXiv 2412.05579v2 abstract contains the five-part sentence verbatim (double-LL
    "LLMs-as-judges"); the staged package's one-letter "LMs" typo has been corrected in the
    current draft row and entry.
49. C1 counters green on the draft; census exit 0 with the same 15 W04 as the claim's
    baseline; baseline `open-model-catalogs.md` has no `verified-at: 2026-10-25` and no
    S101/S102; adoption-expect digest matches the control pin `a1a7e860…`.
50. Registry S101/S102 rows exist, mined, opened 2026-10-25, used-by → the catalog entry
    (census-clean). S086's registry cell already records "published without peer review",
    consistent with the intended R7 direction.

## Verdicts

- **C1 (coverage):** axis correct and distinct; measurable; counters green on genuine draft
  bytes with pinned quotes verified. Attackable (not currently falsified): kill rule is not
  machine-enforced, identity/anchor spoofable, census gate couples to C3's registry rows.
  Smallest safe correction: make the second receipt verify anchor-fragment identity and pin
  quote resolution (or at least require the row's located-quote span to be present in a
  committed capture); scope the census flag or validate the registry once per round outside
  the claim gate.
- **C2 (calibration):** axis correct; separability holds; form-measurable, but six of seven
  checks are token-proximity escapes and the frozen-seven guard is a tautology — `defects=0`
  is not closure evidence. Smallest safe correction: word-boundary + no-negation `near()`;
  literal frozen tuple + `len(CHECKS)==7`; at least one non-empty violating fixture per check;
  R2 must evidence order (mtime/commit ancestry), not a substring.
- **C3 (freshness):** axis correct; **unmeasurable as frozen** — the counter cannot exit 0
  while honestly recording the observed delta; before and after are exit-indistinguishable;
  receipts are unvalidated and absent; metrics are page-size/one-item samples. Smallest safe
  correction: exit 0 iff the entry records the observed deltas (match probe) and real receipt
  files exist with digests; probe endpoints independently; drop `hf_models=50` as a count.

**Joint:** no R13 double-count of measured artifacts; one asymmetric registry-census
coupling (C1⊃C3 rows). All three can report green while state is false only after C3's
counter is patched; as frozen, the lone honest C3 result is red, and calling it green would
violate the freeze.

VERDICT: attack-finished
