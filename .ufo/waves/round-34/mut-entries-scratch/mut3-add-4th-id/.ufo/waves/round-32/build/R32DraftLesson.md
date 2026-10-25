# R32DraftLesson — Gate and assimilation draft

Date: 2026-10-25. Scope: draft-ready Gate/assimilation sections for `corpus/lessons/round-32.md`; no lesson/product file was written (leaf write boundary permits only this report). Evidence read: frozen claims, `R32GateBlock.md`, `R32CollisionGuard.md`, `R32Quarantine.md`, `R32Frontier.md`, `R32CountersPreflight.md`, `R32LearnC1.md`, staged `MERGE-REPORT.md`, and `.ufo/waves/round-32/assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}`. No tools installed/updated.

## Draft: Gate

| Candidate | Verdict | Reason | Flip condition |
|---|---|---|---|
| `benchmark-grader-semantics.md` | **admit** | C1 is the frozen lowest-axis coverage claim and closes the remaining Toolathlon scoring-code clause, while extending (not repeating) the round-31 verifier-execution entry. The entry is grounded in S093 (SWE-bench Pro V2, already held), S094 (Toolathlon `evaluation/main.py` at `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`), and S097 (arXiv 2412.05579v2); new rows S094/S097 were gate-built. | Reverse if the pinned-source quotes fail to resolve or fewer than the three frozen cited rows (S093/S094/S097) are present/mined/opened as required; specifically, failure of `python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census` or `python3 plans/round32_c1_verify.py --lane .` means C1 is not admitted. |
| `judge-calibration-thresholds.md` | **reject (carried)** | Q3 anchor failure: does not meet the admission bar for an adequately anchored candidate in this round; outside frozen claim surface. | Reconsider only with a Q3-satisfying source anchor and a future claim/gate explicitly scoped to it. |
| `card-publication-contracts.md` | **reject (carried)** | Below the tier-C floor; not admissible under the lane's quality bar. | Reconsider only if qualifying evidence raises it above the tier-C floor and the quality gate accepts it. |
| `terminal-bench-release-identity.md` | **defer (second theme)** | Distinct second theme, not the frozen Toolathlon grader-semantics theme; avoid widening this assimilation. | Reconsider in a separately scoped round that opens and verifies its release-identity sources. |

Gate mechanics: scoped adoption of S094/S097 succeeded (`registry=91 staged=173 collisions=0 malformed=0 duplicates=0 defects=0 prose=2`, `wrote ... rows=2`, exit 0); normalization and details below. The package-wide unscoped run refused because unrelated rows contain collisions/malformed/prose-recheck defects (exit 3), so scoped admission was necessary. Gate test command in `R32GateBlock.md`: `python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md --admit-ids S094,S097 --entries corpus/knowledge/benchmark-grader-semantics.md --access-date 2026-10-25 --recheck 180d --attest-opened --scope-to-admit --out /tmp/r32-R32GateBlock/block.md`. Its report records `SELFTEST cases=17 failed=0`.

## Draft: Assimilation record

- **Theme / entry:** one theme, one entry, `corpus/knowledge/benchmark-grader-semantics.md`; sources exactly S093, S094, S097. Pin S093 `66f92766bba642462d4bbe5479e83f91f9211862`; S094 `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`; S097 arXiv 2412.05579v2. Access date 2026-10-25. C1's frozen predicate requires `verified-at: 2026-10-25` (staged text was dated 2026-10-23).
- **IDs and collision census:** lane registry has 91 IDs (S001–S093 with gaps as recorded); staged append has 175 proposed IDs S077–S251. Intersection/collision list comprises 15 IDs: S077–S086, S090–S093, and S100. This count follows the explicit `collisions` file; note the scoped adoption tool reports 173 staged rows in its parsed package, while the staged ID census has 175 IDs. Do not conflate package staged count with unique proposed ID census.
- **Collision guard proof pointer:** `.ufo/waves/round-32/build/R32CollisionGuard.md`, `VERDICT: guard-proven`. It shows column-zero-only detection misses the 2-space indented row (zero collision) while the 0–3-space pattern catches it (one collision, S002); production `ROW_RE` patterns in `plans/adoption_check.py` and `plans/round32_c1_verify.py` use the latter form.
- **Staged-row normalization:** scoped adoption selected only S094/S097; `--attest-opened` sets both `opened=2026-10-25`; `--recheck 180d` normalizes both staged prose recheck cells to `180d`; `used-by` is projected to `corpus/knowledge/benchmark-grader-semantics.md`. Existing S093 stays held and gains this entry in `used-by`. The package report also records staged S141 used-by expanded to include `disclosure-vocabulary-bilingual.md`, S151 redirected to `post5g-plan-archive-coverage.md`, and S241/S242 redirected to `benchmark-card-shape-and-pending-outputs-r15.md`; these are package-wide normalization notes, not claims that they were appended in this scoped adoption.
- **Quarantine:** `.ufo/waves/round-32/build/R32Quarantine.md`; S091 and S105 are both `payload-absent`, both refused/unadopted. S091 fetched successfully with browser UA, but quoted payload was a collector-local command and absent from the NEC page. S105 snapshot/live page were reachable; quoted Japanese error text was absent from the archived METI results page. The slice pointer is `.ufo/waves/round-32/assimilation/quarantine-slice`.
- **Considerthese grounding:** C3 follows proposal 2 in `considerthese/2026-10-24.md` (two public catalogs, cheap refresh plus schema diff); the grounding/pointer is frozen claims §C3, lines 87–93. This is separate from C1 theme selection.

## Draft: census before → after

| Measure | Before | After | Command |
|---|---:|---:|---|
| Registry rows | 91 | 95 expected (+S094, S097, S101, S102; S093 held) | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` |
| Knowledge files | 40 | 41 expected | same |
| README index rows | 40 | 41 expected | same |
| Census outcome | exit 0, 15 W04 | after-state not observed in supplied evidence | same |

The before values (91 / 40 / 40 / exit 0 / 15 W04) are frozen lane facts. The after values are the report skeleton's expected values, not an executed census result; do not state them as measured until the command is run on the landed tree.

VERDICT: gate-drafted
