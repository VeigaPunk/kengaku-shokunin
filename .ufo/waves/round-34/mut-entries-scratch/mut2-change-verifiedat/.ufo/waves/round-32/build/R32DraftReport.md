# kengaku — round 32 report skeleton (scribe draft, 2026-10-25)

Target on landing: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-32/kengaku.md` (fleet).
This draft is the skeleton only: all required sections in order, control-receipt bytes quoted, and
placeholders for every value that only the landed tree can supply. Nothing here that is not read from the
frozen claims, the committed control receipts, the gate receipt, or the staged package is asserted as
measured; each unresolved value carries an explicit `<PLACEHOLDER>`.

---

# kengaku — round 32 (hyaku run 6, 2026-10-25)

Lane: `kengaku-shokunin` (coverage + calibration + freshness; LLM and model research and evaluation).
Baseline lane tip `f20a1097` (local = remote, `ahead=0`); freeze commit `0d32691d` — `plans/round-32-claims.md`,
the three counters, and the committed controls (freeze gate receipt filed at `6084cd3`, Q20 out-of-band:
`CHECKS n=733 mismatches=0 errata_pinned=1`, `VERDICT: PASS`, and round-32 tool selftests green).
**Landed round work `<LANE-TIP>`** (local = remote, `ahead=0` at the time of writing).
Report commit `<REPORT-COMMIT>` — the round-32 report lands after the last lane commit and cites
`<LANE-TIP>` (C2 R2).
Round shape: two v1 waves (`ufo-wave-policy.json`, band 32–64). Build wave dispatched with **34 seats**
(`.ufo/waves/round-32/build/swarm-registry.json`); falsify wave `<FALSIFY-SEATS>` seats, registry
`.ufo/waves/round-32/falsify/swarm-registry.json` `<FALSIFY-REGISTRY>`.

## Work performed

**Declared claims (frozen at `0d32691d` before any seat ran):** C1 **coverage** — shokuknow assimilation
round 4, the benchmark grader-semantics entry admitted (lowest non-retired axis, 7, tie-break over
novelty); C2 **calibration** — the seven routed defects R1–R7 closed (D1–D6 from round 31's non-author
spot-check §5, plus the peer-review erratum debt); C3 **freshness** — the public model catalogs re-probed
on 2026-10-25 and the catalog entry refreshed.

- **C1 · the entry and its rows.** `corpus/knowledge/benchmark-grader-semantics.md` (staged in
  `shokuknow/merge/kengaku/knowledge/corpus/knowledge/`), re-grounded on three sources at pinned
  revisions: S093 (SWE-bench Pro V2 `66f92766`, held), S094 (Toolathlon `evaluation/main.py` at
  `9be8d8fe`), S097 (arXiv 2412.05579v2). The staged draft carries `verified-at: 2026-10-23` and a
  `recheck: 180d` line dated 2026-10-23; the frozen predicate requires `verified-at: 2026-10-25`, so the
  admitted entry must carry the re-stamped line. Findings: `<C1-FINDINGS>`.
- **Assimilation mechanics (§10).** Collision census over the staged append vs the registry
  (`.ufo/waves/round-32/assimilation/{reg-ids,staged-ids,collisions}`), quarantine slice re-derived
  (`quarantine-slice`): `<ASSIMILATION-OUTCOME>`.
- **C2 · the seven repairs.** R1 round-31 report addendum phantom hash `a44b5a8` superseded by an
  appended erratum naming the real locator-fix commit `ae95fe0`; R2 this round's report exists after the
  last lane commit and cites the final lane tip; R3 the round-31 CLI receipt at lane tip regenerated from
  the committed fixtures with the corrected relative path (no `can't open file`); R4 `plans/sources_adopt.py`
  has a row in `SKILL.md` §Gate/probe registry; R5 the round-31 falsify seat `R31FxEntryBar` recorded dead
  in the round-32 lesson's seat ledger; R6 the round-31 lesson Gate's `verifier_mode.py` precedence locator
  (`:35-38` → `:39-40`) and the round-30 lesson erratum's entry line refs (`:78-81` → `:72`/`:82-83`)
  corrected by appended notes; R7 the round-30 lesson `:66` "S083/S086 peer-reviewed" grouping corrected so
  S086 is recorded as published without peer review. Repairs: `<C2-REPAIRS>`.
- **C3 · the re-probe.** `python3 plans/catalog_probe.py --diff --lane .` against Hugging Face
  `api/models` and OpenRouter `api/v1/models`; the entry gains a `verified-at: 2026-10-25` provenance
  block, receipts under `corpus/evidence/round32/catalogs/`, and recorded per-source schema deltas.
  Probe run: `<C3-PROBE>`.
- **Frontier step.** Census before→after recorded (below); one mistake mined per row into
  `corpus/lessons/round-32.md` §Mistakes; at least one claim is sourced — C1 rests on S094/S097 rows
  opened this round.
- **Q20 out-of-band gate receipt** at freeze: `.ufo/waves/round-32/gate-receipt.txt` — `CHECKS n=733
  mismatches=0 errata_pinned=1`, `VERDICT: PASS`, roster selftests green (`round32_defects: SELFTEST
  checks=7 failed=0`; `round32_c1_verify: SELFTEST checks=6 failed=0`; `catalog_probe: SELFTEST
  checks=6 failed=0`).

## Landed changes

| change | LOG entry | commit |
|---|---|---|
| `plans/round-32-claims.md`, `plans/round32_defects.py`, `plans/round32_c1_verify.py`, `plans/catalog_probe.py`, freeze controls | §Round 32 | `0d32691d` (freeze) |
| gate receipt | §Round 32 | `6084cd3` |
| C1 entry + S094/S097 rows + README index/coverage/frontier | §Round 32 item 1 | `<LANE-TIP>` |
| C2 R1–R7 repairs (report erratum, lesson errata/seat ledger, CLI receipt, SKILL row) | §Round 32 item 2 | `<LANE-TIP>` |
| C3 catalog refresh + probe receipts + S101/S102 rows | §Round 32 item 3 | `<LANE-TIP>` |
| `corpus/lessons/round-32.md`, `SCORECARD.md`, `QUALITY.md`, `LOG.md` | §Round 32 (final paragraph) | `<LANE-TIP>` |
| falsify-wave seat evidence | §Round 32 | `<LANE-TIP>` |
| this report | §Round 32 | `<REPORT-COMMIT>` |

## Before → after measurements

| claim | axis | before | after | counting command |
|---|---|---|---|---|
| C1 (adoption) | coverage | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok`, exit 1 (`claims/control-nothing.txt`) | `<AFTER-C1>` — expected `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0 | `python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census` |
| C1 (second receipt) | coverage | `<BEFORE-C1-VERIFY>` — no committed before-control; selftest `checks=6 failed=0` at freeze | `<AFTER-C1-VERIFY>` — expected `checks=6 defects=0`, exit 0 | `python3 plans/round32_c1_verify.py --lane .` |
| C2 | calibration | `checks=7 defects=7`, exit 1 (`claims/defects-before.txt`) | `<AFTER-C2>` — expected `checks=7 defects=0`, exit 0 | `python3 plans/round32_defects.py --lane .` |
| C3 | freshness | `probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=stale`, exit 1 (`claims/catalogs-before.txt`) | `<AFTER-C3>` — expected `probed=2026-10-25 hf=ok openrouter=ok` plus `hf_models=<n> or_models=<n>` and per-source schema-delta counts, exit 0 | `python3 plans/catalog_probe.py --diff --lane .` |
| census | — | 91 rows, 40 knowledge files, 40 index rows, exit 0, 15 `W04` | `<AFTER-CENSUS>` — expected 95 rows, 41 knowledge files, 41 index rows, exit 0, `<N-W04>` `W04` | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` |

C2's before-state is the committed freeze control (`claims/defects-before.txt`); if the counter changed
while seats attacked it, the before receipts must be regenerated from the **final** counter bytes and the
stale file marked SUPERSEDED, as in round 31.

## Sources & frontier

**SOURCES: 91 → 95 rows (expected).** Rows added: S094 (Toolathlon task evaluation script
`evaluation/main.py` at `9be8d8fe`, code, tier A), S097 (arXiv 2412.05579v2, paper, tier B under the
staged append's row-10 preprint rule), S101/S102 (this round's HF `api/models` and OpenRouter `api/v1/models`
probe rows). S093 is held and gains the entry in `used-by`. All new rows `status=mined`, `opened=2026-10-25`,
`used-by` naming the citing entry. Access date for every source opened this round: 2026-10-25. Pinned
revisions: SWE-bench Pro V2 `66f92766`; Toolathlon `9be8d8fe`; arXiv 2412.05579v2. Frontier:
`corpus/README.md` §Frontier bullet 1's "their scoring code was not read and stays open" clause, as
narrowed by round 31, is discharged **for Toolathlon's scoring code**; the entry adds the survey frame that
separates deterministic graders from LLM judges.

**Assimilation: one theme, one entry, three cited rows** (`merge/kengaku/`), with the admit/reject record,
collision evidence, and quarantine verdicts in `corpus/lessons/round-32.md` §Gate.

## Trend verdicts

- **coverage (C1): <VERDICT-C1>** — expected `improved`: the entry is new corpus bytes on ground the
  coverage map did not hold (the Toolathlon scoring-code clause); the canonical score stays 7 while the
  round-25 L0 coverage cap is open, so the row records the ledger delta, not a raised number.
- **calibration (C2): <VERDICT-C2>** — expected `improved` if `defects=0` plus the byte-level review of
  each of R1–R7 holds (counter alone is not self-proving, per round-31 `R31FxC2Survivors.md`).
- **freshness (C3): <VERDICT-C3>** — expected `improved` if both APIs were reachable at counter time and
  the entry carries `verified-at: 2026-10-25` with S101/S102 citations; a partial result (one API
  unreachable) is reported honestly per the kill rule.

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — pointer:
  `SKILL.md` gains the `sources_adopt.py` row (C2 R4); `<SKILL-POINTER>`.
- [~] At least one end-to-end domain task executed and logged in LOG.md — pointer: `LOG.md` §Round 32
  items 1–3 with receipts under `corpus/evidence/round32/`; the task was reading a published grader at
  two pinned commits plus a pinned survey and landing the entry through the lane's own gate.
- [~] Instructions executable by an agent without oral context — pointer: every command in this report and
  in the lesson is copy-pasteable and was run; `corpus/QUALITY.md` Q20/Q21 add executable checks.
  `<COLD-RUN>`.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — pointer: seat `R32ConnSibling`; `PROVINCE.md`
  unchanged, so the entry's ground is claimed under the existing surfaces. `<CONN-FINDING>`.

No box is `[x]`: a non-author verifier has not yet judged this round.

## Stale-lane

Respawn-per-round driver; this mission was dispatched and is the lane's only open mission. It is
progressing, not silent (commits `0d32691d`, `6084cd3` by the lane identity; wave artifacts uncommitted in
`.ufo/waves/round-32/`). Final state: `<LANE-FINAL-STATE>`.

## Disclosures, dead seats, open questions

- **Seats:** 34 build seats dispatched, **<DEAD-SEATS> dead** — `<BUILD-REPORTS-COMMITTED>` of 34 build
  reports committed; falsify wave `<FALSIFY-STATUS>`. The seat ledger lands in the round-32 lesson (C2 R5).
- **D1 phantom hash:** `a44b5a8` in the round-31 report addendum is superseded by an appended erratum
  naming the real locator-fix commit `ae95fe0` (C2 R1).
- **Peer-review erratum debt:** round-30 lesson `:66` "S083/S086 peer-reviewed" is corrected so S086 is
  recorded as published without peer review (C2 R7).
- **Staged entry stamp:** the staged `benchmark-grader-semantics.md` cites `verified-at: 2026-10-23`;
  the frozen predicate pins `2026-10-25`, so the admitted entry must carry the re-stamped line.
- **Carried from round 31:** C1's kill-rule branch ("fewer than two of the three survive") is unreachable
  under the frozen predicate because `cited_rows` must equal 3; the C2 counter's fakeability routes are
  disclosed and the verdict rests on the counter plus byte-level review; wave-report sealing is routed to
  the protocol lane.
- **Open L0 question:** none filed. No operator decision was needed to draft this skeleton.
- **Tool installs:** none (no `pacman` transaction; `pacman` is paused host-wide and was not used).

---

VERDICT: skeleton-ready
