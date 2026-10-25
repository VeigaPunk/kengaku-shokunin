# R32DraftScorecard — SCORECARD §Round 32 draft (scribe, drafts2026-10-25)

Scope: draft the SCORECARD.md §Round 32 rows (three claims) with the before→after cells
and counting commands from `plans/round-32-claims.md` (freeze commit `0d32691d`).
Before states are the committed freeze control receipts under
`.ufo/waves/round-32/claims/*-before.txt` (read from disk, quoted verbatim below).
After states are the frozen predicates' target forms; the after-receipt files
(`corpus/evidence/round32/…`) do not exist yet at drafting time (round in flight), so
the after cells quote the predicate target shape and the receipt file each lands in —
no after bytes are invented. Baseline verified from disk: registry 91 rows, knowledge
40 files, index 40 rows, and `git show f20a1097:corpus/knowledge/open-model-catalogs.md`
carries no `verified-at: 2026-10-25` and no `S101`/`S102`.

---

## Draft — SCORECARD §Round 32

### Round header

## Round 32 (hyaku run 6, 2026-10-25): shokuknow assimilation round 4 (benchmark grader semantics), round-31 routed-defect closure, public model catalog re-probe

Baseline `f20a1097af900dc4595e0da0fa5e12e673f9ce7e` (local = remote, `ahead=0`);
frozen prereg `plans/round-32-claims.md` (freeze commit `0d32691d`). Lowest
non-retired axis: **coverage 7**, tied with novelty 7. Tie-break per the lane's
recorded rule: the claim most falsifiable with the sources an on-host tool can open —
C1 opens two pinned-commit trees plus a pinned preprint and lands a registry delta; a
novelty claim needs a phenomenon probe and no identity-verified endpoint exists
(`corpus/README.md` §Frontier bullet 4), so C1 carries the lowest-axis obligation. No
stagnation waiver is available (saturation line 8, novelty below it, a capability row
entered at round 31). Round shape: two v1 waves (`ufo-wave-policy.json`, band 32–64).

### Claims

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 shokuknow assimilation round 4 — the benchmark grader semantics entry | **coverage** (lowest non-retired, tie-break) | before: `python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census` → `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` exit 1 (`.ufo/waves/round-32/claims/control-nothing.txt`, hardened with the expect digest `a1a7e860…`) → after: same command → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` exit 0 (`corpus/evidence/round32/adoption-after.txt`). Registry 91 → 93 rows (S094 and S097 new; S093's `used-by` gains the entry); knowledge 40 → 41; index 40 → 41; second receipt `python3 plans/round32_c1_verify.py --lane .` → `checks=6 defects=0` exit 0 (`corpus/evidence/round32/c1-verify-after.txt`) | **7 → 7 held — improved (counts)**; coverage *surfaces* did not move (no new `PROVINCE.md` section), so the row records the ledger delta, not a raised number |
| C2 calibration — round-31 routed-defect closure, mismatch count 7 → 0 | **calibration** | before: `python3 plans/round32_defects.py --lane .` → seven `DEFECT` lines (R1 round31-report-phantom-hash, R2 round32-report-order-tip, R3 round31-cli-receipt-regenerated, R4 skill-registry-row, R5 round31-dead-seat-recorded, R6 lesson-locators-corrected, R7 round30-peer-review-erratum), `checks=7 defects=7`, exit 1 (`.ufo/waves/round-32/claims/defects-before.txt`) → after: same command → `checks=7 defects=0`, exit 0 (`corpus/evidence/round32/defects-after.txt`), with the seven checks exactly R1–R7 as defined in `plans/round-32-claims.md` (R1 erratum superseding the phantom hash `a44b5a8` and naming `ae95fe0`; R2 the round-32 report landing after the last lane commit citing the final tip; R3 the round-31 CLI receipt regenerated from the committed fixtures with the corrected relative path; R4 a `plans/sources_adopt.py` row in `SKILL.md` §Gate/probe registry; R5 the round-31 falsify seat `R31FxEntryBar` recorded dead in the round-32 lesson's seat ledger; R6 the `verifier_mode.py` precedence locator (`:35-38` → `:39-40`) and round-30 erratum entry-line refs (`:78-81` → `:72`/`:82-83`) corrected by appended notes; R7 S086 recorded as published without peer review) | **8 → 8 held** — seven self-assessment/repo mismatches closed; the counter is the committed `plans/round32_defects.py`, unchanged from freeze |
| C3 freshness — public model catalogs re-probed and the catalog entry refreshed | **freshness** | before: `python3 plans/catalog_probe.py --diff --lane .` → `probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=stale` exit 1 (`.ufo/waves/round-32/claims/catalogs-before.txt`; HF missing fields `author`, `sha`, `lastModified`, `gated`; the base entry carries no `verified-at: 2026-10-25`, `git show f20a1097:corpus/knowledge/open-model-catalogs.md`) → after: same command → `probed=2026-10-25 hf=ok openrouter=ok hf_models=<n> or_models=<n> hf_schema_delta=<n> or_schema_delta=<n>` exit 0 (`corpus/evidence/round32/catalogs/catalog-probe-after.txt`), with `corpus/knowledge/open-model-catalogs.md` carrying a `verified-at: 2026-10-25` line, citations of the two rows opened this round (`S101`, `S102`), and a receipt pointer under `corpus/evidence/round32/catalogs/` | **8 → 8 held** — re-probe landed with committed receipts and recorded schema-delta per source; the entry is refreshed, no raised number |

### Axes-held

| Axis | Held at | Note |
|---|---|---|
| depth | 9 | the grader-semantics entry adds new sourced corpus bytes (survey frame separating deterministic graders from LLM judges, plus a code-level reading of Toolathlon's task evaluation script), no new instrument claim |
| novelty | 7 | no novelty credit taken — the entry is a reading of published scoring code and a survey structure, not a phenomenon this lane measured; no prior-art verdict claimed either way (non-claims) |
| operability | 8 | no new gate or instrument is planned or landed by these claims; every counting command (`plans/adoption_check.py`, `plans/round32_c1_verify.py`, `plans/round32_defects.py`, `plans/catalog_probe.py`) pre-dates the round |
| adjacency | 8 | no sibling contest is claimed; these claims add no cross-domain surface and file no report-out |
| calibration | 8 | C2 (above) |
| coverage | 7 | C1 (above) — ledger delta, not a raised number |
| freshness | 8 | C3 (above) |

### Capabilities

No capability row is added this round — none planned in `plans/round-32-claims.md`.
The claims assimilate corpus bytes (C1), close routed defects (C2), and refresh a
catalog entry (C3); no new in-repo command or gate is introduced.

### Evidence status (honesty)

After-receipt files (`corpus/evidence/round32/adoption-after.txt`,
`c1-verify-after.txt`, `defects-after.txt`, `catalogs/catalog-probe-after.txt`) are
the frozen landing slots for the counters' live output; they did not exist when this
draft was written, so the after cells state the frozen predicate targets and the
receipt paths rather than unobserved bytes. The before cells quote the committed
freeze controls verbatim (`control-nothing.txt`, `defects-before.txt`,
`catalogs-before.txt`).

VERDICT: scorecard-drafted
