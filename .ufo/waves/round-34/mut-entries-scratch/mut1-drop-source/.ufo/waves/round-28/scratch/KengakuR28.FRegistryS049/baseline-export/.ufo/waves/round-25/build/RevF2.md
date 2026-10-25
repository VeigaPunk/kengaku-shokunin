# RevF2 — W3ReviewKengaku F2 (quote-location errors a–d) re-check at lane tip 3f371d2

Axes (godspeed): **calibration** (judged — second-seat re-verification of admitted-entry locations) + **novelty** (owned, legacy label → canonical coverage; not exercised by this item). This is a read-only re-check; the axis-relevant fact is that the F2 fix is fully offline-verifiable from committed text + lesson log.

## F2 status: **FIXED** (all four sub-items), fixing commit `e21f9ea` "round-24: post-review fixes" (parent `06872d4` — one commit after the W3-audited tip)

Fix mechanism is exactly the sanctioned append-only path: appended `## Corrections (round 24 post-review, 2026-10-19)` sections + lesson old→new log + new QUALITY criterion. No history rewritten.

| sub-item | finding (kaika-w3/kengaku-review.md:127-131) | fix at 3f371d2 | verdict |
|---|---|---|---|
| (a) | "Table 2" for the 156-GRPO-step AUROC; is S002 Figure 2 §3.1 | `corpus/knowledge/contamination-detection-and-transparency.md:90-94` ("shown in **Figure 2** (§3.1 …), not Table 2. Table 2 reports the clean-vs-contaminated GRPO comparison") | fixed |
| (b) | "repetitive list" attack attributed to Abstract; is S012 §3.3 | `corpus/knowledge/llm-judge-calibration.md:94-97` ("is in **§3.3 Limitations of LLM-as-a-Judge** (verbosity bias), not the Abstract"); `source:` line :1 now reads "S012 … — Abstract, §3.3" | fixed |
| (c) | "almost all the detection approaches…" cited §4; is S002 §1 Intro | `contamination-detection-and-transparency.md:95-98` ("is in **§1 Introduction**, not §4; §4 / Table 5 carry the supporting results"); anchor reading restated at :99-100 | fixed |
| (d) | S005 "at least 59.4%…" placed under "Too narrow and too wide tests"; is intro numbered list | `corpus/knowledge/agent-time-horizon-and-task-validity.md:53-58` ("in the post's **opening summary, item 1 'Tests reject correct solutions'**, not in 'Too narrow and too wide tests'") | fixed |

Commands + output (ground truth):
- `git -C kengaku-shokunin log -S"repetitive list" --all -- 'corpus/knowledge/*'` → `e21f9ea`, `94da19e` (same for "almost all the detection approaches"). `e21f9ea` diff-stat vs parent: `agent-time-horizon +16, contamination +17, llm-judge-calibration +15, round-24.md +32, QUALITY.md +15, SOURCES.md 43 changed, gate.md +1` — **48 insertions across the three knowledge files, 0 deletions**: `git diff -U0 06872d4 3f371d2 -- corpus/knowledge | grep -cE '^-[^-]'` → `0`.
- Correction blocks exist verbatim at tip: pinned via `git grep` at `3f371d2` (contamination :91/:97/:100; judge :96; horizon :53-55). `e21f9ea` is an ancestor of tip (`git log` chain `3f371d2 → 4e57f14 → 6180e4f → a42bb40 → e21f9ea`).
- Lesson log old→new: `corpus/lessons/round-24.md:127-133` — "Other location slips (S002 ×2, S005 ×2): appended §Corrections in contamination… and agent-time-horizon…" and :125-126 spot-check disagree (partial) for S009 range + S012 location, class M22.
- Criterion codified: `corpus/QUALITY.md:75` **Q10 — "locations and numbers are re-read by a second seat."** — closes the W3 §7 "becomes harmed if not learned" branch for this finding class.

## Original body text left in place (by design, not a defect)
The wrong sentences remain at `contamination-detection-and-transparency.md:29,31-33` and `agent-time-horizon-and-task-validity.md:17` with the correction appended below — append-only discipline; the `source:` anchor `:1` is likewise unedited and re-read via :99-100. No in-place rewrite occurred (verified: 0 deletions). Any future mechanical location checker must consult the entry's own §Corrections as the final word.

## Incidentally verified sibling fixes (same commit)
- F1: recheck cells repaired in place with old→new logged (`lessons/round-24.md:130-135`: S001–S022 `2027-01-17 (90d)`→`2027-01-17`; S024/S025 `each round`→`90d`); new S026 uses `on-release` (`corpus/SOURCES.md:48`).
- F3: `llm-judge-calibration.md:89-92` restates exact Table 3 cells (Ref-5 FR: BiGGen Bench 35.40–45.54%, FLASK 40.53–48.58%) instead of the unreproducible "~45–48%".
- F4: superseding row S026 (`corpus/SOURCES.md:48`, "supersedes S023 — … S006 does not bear on it") + gate.md receipt row appended (`e21f9ea`, gate.md +1).

## Residual risk / verification gaps
- The correction blocks quote source sentences (S002 Fig. 2 caption "As shown in Fig. 2, AUROC consistently decreases…"; S002 §1 sentence; S012 §3.3) that are **not byte-backed by committed receipts** — `corpus/evidence/round24-sources/` stores only `gate.md` (one quote + sha per row; S002 sha 3eef8073…, S012 sha a1768d34…, full HTML not in lane). Offline I can confirm only internal consistency (e.g. gate.md:13 S005 row's own sentence "We found that 59.4% of the 138 problems…" matches the correction's counter-quote exactly). The S002-caption fragment "simply after 156 steps" was live-verified by W3ReviewKengaku; the longer caption sentence is lane-author-attested only. No offline instrument (attrib_calibration.py / state_check.py scope, P1/P2) covers these web-quote locations today.
- `plans/attrib_calibration.py`, `plans/state_check.py`, `plans/fixtures/r25/` do not exist yet at tip — shared-interface writers (not this seat) still owe them; F2 status is independent of that gap.
- Not checked: whether any S002/S012 re-fetch would still resolve (no network requests permitted this round).

## Installs
None (no tool installed or updated; pacman guard respected, uv/npx untouched).

VERDICT: F2 FIXED at e21f9ea (all of a–d via appended §Corrections + lesson old→new + QUALITY Q10, 0 deletions, ancestor of tip 3f371d2); residual: corrected source locations rest on lane-author attestation, not stored bytes.
