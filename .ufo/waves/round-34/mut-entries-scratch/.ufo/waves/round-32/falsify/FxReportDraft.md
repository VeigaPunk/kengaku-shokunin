# FxReportDraft — round-32 report skeleton review (scribe)

Seat: `FxReportDraft` (falsify wave, kengaku round 32). Target reviewed:
`.ufo/waves/round-32/build/R32DraftReport.md` (build-wave scribe draft, 155 lines).
Contract reviewed: `.ufo/prompts/kengaku-round-32.md` §4 Report contract + §6 item 6
(report extras); precedent: `.ufo/reports/round-31/kengaku.md` and
`round-30/kengaku.md`.

## Review basis (all read, no inference)

- Skeleton `R32DraftReport.md` (full file, 155 lines).
- Contract §4 required sections, in order (prompt lines 99–129):
  Work performed → Landed changes → Before → after measurements → Sources & frontier →
  Trend verdicts → SHONEN → (extras: Stale-lane line, tool installs).
- Committed controls: `.ufo/waves/round-32/claims/{control-nothing.txt,defects-before.txt,catalogs-before.txt,adoption-expect.json}`.
- Gate receipt `.ufo/waves/round-32/gate-receipt.txt` — `CHECKS n=733 mismatches=0
  errata_pinned=1`, `VERDICT: PASS`, roster selftests incl. round-32 tools
  (`round32_defects: SELFTEST checks=7 failed=0`; `round32_c1_verify: SELFTEST
  checks=6 failed=0`; `catalog_probe: SELFTEST checks=6 failed=0`).
- Wave registries: build `swarm-registry.json` 34 members; falsify
  `swarm-registry.json` 34 members (keys: kind/agentId/role/item/axes/milestone).
- Staged entry `shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-grader-semantics.md`
  lines 1–6: `source:` S093/S094/S097 lines present; `verified-at: 2026-10-23`
  (line 5); `recheck: 180d — re-run the Gate commands … (ran 2026-10-23)`
  (line 6).
- Lane `SHONEN.md`: exactly 4 boxes (SKILL.md; LOG.md:7; coldrun.md:48;
  PROVINCE.md:129).
- Read-only git: baseline `f20a1097af900dc4595e0da0fa5e12e673f9ce7e` resolves;
  freeze `0d32691d` and gate-receipt commit `6084cd3` exist on `--all`; freeze's
  parent is `85a9695`; worktree has the planned uncommitted drafts (SKILL.md,
  corpus/README.md, corpus/SOURCES.md, open-model-catalogs.md, catalog_probe.py,
  round32_defects.py, benchmark-grader-semantics.md, wave dirs).

## Verdict

The skeleton is structurally sound: it carries all contract sections in the
required order, quotes the committed control and gate bytes correctly (verified
byte-for-byte above), and its factual claims (baseline, freeze commit, gate
receipt commit, 34 build seats, staged-entry stamp) all resolve. One required
**edit** and two recommended edits before the skeleton is landed:

- **F1 (edit, required):** Trend verdicts must be keyed to the canonical three
  axes — `expansion`, `quality`, `discernment` — one verdict each with evidence
  and no scalar (§4; precedent round 31 lines 105–123, round 30 lines 86–99).
  The skeleton keys by claim (`<VERDICT-C1/C2/C3>`). Re-key: expansion ← C1
  (new corpus bytes + 3 rows, score stays 7), quality ← C2 (R1–R7 closure) and
  C3 (re-probe receipts + schema deltas), discernment ← the round's refusals /
  counter-fakeability disclosure. This is the difference between conforming and
  minimum-content-defect.
- **F2 (recommended):** Sources & frontier must state "Rows added by tier"
  (A/B/C counts) and name the two census receipt files
  (`claims/census-before.txt`, `corpus/evidence/round32/census-after.txt`), per
  the contract's required content and round-31 precedent (round-31 lines
  86–99).
- **F3 (recommended):** Before → after rows must pin the commit each after-value
  was measured against (contract: "the commit it was measured against";
  round-30 used a `measured at` column). Add the column or fold the commit into
  each after-cell.

---

## Final ordered section list the round report must contain

Header preamble (lines 1–22 of the skeleton, above `## Work performed`): title
`# kengaku — round 32 (hyaku run 6, 2026-10-25)`; lane identity; baseline lane
tip `f20a1097` (local = remote, `ahead=0`); freeze commit `0d32691d` + the three
counters + committed controls; freeze gate receipt `6084cd3` (Q20 out-of-band,
`CHECKS n=733 mismatches=0 errata_pinned=1`, `VERDICT: PASS`); landed round work
`<LANE-TIP>`; report commit `<REPORT-COMMIT>` citing `<LANE-TIP>` (C2 R2);
round shape (two v1 waves, band 32–64): build wave seat count with
`build/swarm-registry.json` pointer, falsify wave seat count with
`falsify/swarm-registry.json` pointer.

1. **Work performed** — opens by naming the three declared claims (C1 coverage,
   C2 calibration, C3 freshness) and their axes; then one bullet per work item,
   each with an evidence pointer: (a) C1 entry + rows S093/S094/S097 (admit
   receipt `corpus/evidence/round32/adoption-after.txt`; pinned revisions
   `66f92766` / `9be8d8fe` / arXiv 2412.05579v2; re-stamped `verified-at:
   2026-10-25`; `<C1-FINDINGS>`); (b) assimilation mechanics — collision census
   ids, guard proof, quarantine slice (`assimilation/` outputs, `<ASSIMILATION-OUTCOME>`);
   (c) C2 repairs R1–R7, each naming the defect and the fix bytes
   (`<C2-REPAIRS>`); (d) C3 re-probe receipts + per-source schema deltas
   (`<C3-PROBE>`); (e) frontier step — census before→after, one mined mistake in
   the lesson, at least one sourced claim (S094/S097 opened this round); (f)
   Q20 gate receipt quote.
2. **Landed changes** — table: every change ↔ `LOG.md` §Round 32 entry ↔ commit
   hash; all non-report rows at `<LANE-TIP>`; final row = this report at
   `<REPORT-COMMIT>`; include the falsify-wave seat evidence row.
3. **Before → after measurements** — one row per claim plus the census row:
   C1 adoption (before `entries=0 … census=ok` exit 1 from
   `claims/control-nothing.txt`; after `entries=1 indexed=1 cited_rows=3
   rows_present=3 rows_mined=3 usedby_ok=1 census=ok` exit 0; command
   `plans/adoption_check.py --expect … --census`), C1 second receipt (before
   `<BEFORE-C1-VERIFY>`; after `checks=6 defects=0` exit 0; command
   `plans/round32_c1_verify.py --lane .`), C2 (before `checks=7 defects=7` exit
   1 from `claims/defects-before.txt`; after `checks=7 defects=0` exit 0;
   command `plans/round32_defects.py --lane .`), C3 (before `probed=2026-10-25
   hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4
   or_schema_delta=0 entry=stale` exit 1 from `claims/catalogs-before.txt`;
   after `probed=2026-10-25 hf=ok openrouter=ok` + counts + deltas exit 0;
   command `plans/catalog_probe.py --diff --lane .`), census (before 91 rows /
   40 knowledge files / 40 index rows / 15 `W04`; after 95 / 41 / 41 /
   `<N-W04>`; command `scripts/sources-census.sh validate --root … kengaku`).
   Every row carries the commit measured against (F3). Note the SUPERSEDED rule
   if a counter changed during the wave.
4. **Sources & frontier** — `SOURCES: 91 → 95 rows` with the counting command
   and both census receipts; rows added by tier (A/B/C: S094 A, S097 B,
   S101/S102 probe rows); rows touched old→new (S093 `used-by` gains the entry);
   frontier discharge: README §Frontier bullet 1's "scoring code … stays open"
   clause closed for Toolathlon's scoring code; assimilation Gate verdict with
   admit/reject, collision evidence and quarantine verdicts (lesson §Gate).
5. **Trend verdicts** — one verdict each for `expansion`, `quality`,
   `discernment` (`improved` / `harmed` / `unchanged` / `unprovable-but-better`),
   each with evidence and bounds, no scalar (F1). Expected: expansion improved
   (C1), quality improved (C2 + C3), discernment improved (wave refusals +
   counter-fakeability disclosures) — verdicts are for the landed tree to
   confirm, not assert in the skeleton.
6. **SHONEN** — four lines, one per SHONEN.md box, in box order: SKILL.md
   decision tables/error patterns/checklists/cited sources (pointer: SKILL.md
   gains the `sources_adopt.py` row, C2 R4; `<SKILL-POINTER>`); one end-to-end
   domain task executed and logged (pointer: `LOG.md` §Round 32 items 1–3 +
   receipts); instructions executable without oral context (pointer: copy-paste
   commands; `<COLD-RUN>`); no cross-domain bleed, PROVINCE.md accurate
   (pointer: seat `R32ConnSibling` finding; `<CONN-FINDING>`). `[x]` only with
   a named non-author verifier — none yet, so all `[~]`.
7. **Stale-lane** — respawn-per-round driver line: this mission dispatched, is
   the lane's only open mission, progressing not silent (commits `0d32691d`,
   `6084cd3` by lane identity; wave artifacts uncommitted); final lane state with
   `local=remote ahead=0` (`<LANE-FINAL-STATE>`).
8. **Disclosures, dead seats, open questions** — seats: build dispatched 34,
   `<DEAD-SEATS>` dead, `<BUILD-REPORTS-COMMITTED>` of 34 reports committed
   (registries `build/` + `falsify/` `swarm-registry.json`; seat ledger lands in
   the lesson per C2 R5); falsify `<FALSIFY-STATUS>`; D1 phantom hash
   `a44b5a8` superseded by appended erratum naming `ae95fe0` (C2 R1);
   peer-review erratum debt, S086 published without peer review (C2 R7); staged
   entry stamp `2026-10-23` → re-stamped `2026-10-25`; carried from round 31
   (C1 kill-rule branch unreachable under frozen `cited_rows=3`; C2 counter not
   self-proving — verdict rests on counter + byte-level review); open L0: none
   filed; tool installs: none (pacman paused, unused).

## The two placeholders the lane must fill

Only two placeholder tokens are hashes whose values only the landed tree can
supply, and both must be filled at landing:

- **`<LANE-TIP>`** — the final lane branch tip hash after all round-32 commits
  (C1 entry+rows, C2 repairs, C3 refresh, lesson/SCORECARD/QUALITY/LOG, falsify
  evidence), pushed with `local=remote ahead=0`. Appears in the header, the
  Landed changes table (all non-report rows) and the R2 citation.
- **`<REPORT-COMMIT>`** — the fleet report commit hash (`fleet-commit.sh --as
  kengaku`), landed after the last lane commit and citing `<LANE-TIP>`; the
  report's own Landed-changes row and header carry `<.

All other `<PLACEHOLDER>` tokens are data values (not hashes) that the lane must
resolve from wave receipts before writing the fleet report: `<FALSIFY-SEATS>`,
`<FALSIFY-REGISTRY>`, `<FALSIFY-STATUS>`, `<DEAD-SEATS>`,
`<BUILD-REPORTS-COMMITTED>`, `<AFTER-C1>`, `<BEFORE-C1-VERIFY>`,
`<AFTER-C1-VERIFY>`, `<AFTER-C2>`, `<AFTER-C3>`, `<AFTER-CENSUS>`,
`<N-W04>`, `<C1-FINDINGS>`, `<ASSIMILATION-OUTCOME>`, `<C2-REPAIRS>`,
`<C3-PROBE>`, `<SKILL-POINTER>`, `<COLD-RUN>`, `<CONN-FINDING>`,
`<LANE-FINAL-STATE>`; `<VERDICT-C1/C2/C3>` are superseded by the canonical
trend bullets (F1).

VERDICT: report-skeleton-final
