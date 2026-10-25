# RevF5 — re-check of W3ReviewKengaku F5 (overstated self-verdict, round 24)

Axes: novelty (legacy→coverage) + calibration. This item: calibration (honest self-verdict / state-matching reporting). Read-only; no installs (none needed).

## F5 as filed (`.ufo/waves/kaika-w3/kengaku-review.md:134`)
"Report 'no admitted entry fails its re-check' and the Gate's 'Q1–Q8 pass' should name F2–F3 as open or fixed."
Two surfaces: (a) fleet report `.ufo/reports/round-24/kengaku.md:177-178` (commit `dec4b51`, fleet repo); (b) lane `corpus/lessons/round-24.md` §Gate rows `Q1–Q8 pass` (`:65-69`, commit `94da19e`).

## Timeline (verified by git log -S / show)
- `94da19e` — Gate rows land, each admitted entry ending "Q1–Q8 pass" (`corpus/lessons/round-24.md:65-69`); `git log -S "Q1–Q8 pass" -- corpus/lessons/round-24.md` → only `94da19e`.
- `e21f9ea` "round-24: post-review fixes" (33 s before the report commit) — fixes F2–F4 substance: `## Corrections` appended in `contamination-detection-and-transparency.md:85`, `llm-judge-calibration.md:84` (S009 exact cells 35.40–45.54 / 40.53–48.58; S012 Abstract→§3.3), `agent-time-horizon-and-task-validity.md:48` (S005 ×2); S026 supersedes S023; M21/M22 + QUALITY Q9/Q10 (`corpus/QUALITY.md:67,75`); 21 recheck cells logged old→new.
- `dec4b51` (fleet, 19:39:49) — report committed AFTER the fixes; same commit carries `## Post-review fixes` (`:244-270`) naming every slip as fixed.
- `a42bb40` / `517d3c1` — adjudication: ADMITTED after `e21f9ea`; disagreements became Q9/Q10 (`corpus/lessons/round-24-verifier-spotcheck.md:14-17`).

## Status: PARTIALLY FIXED
1. FIXED (substance): F2–F3 corrections are appended in the three entries (`## Corrections` headers cited above) and the outside-found slips are enumerated in `round-24.md:113-141` §Post-review corrections and in report `:244-270`. History not rewritten — append-only discipline held.
2. RESIDUAL (the verdict lines themselves were never marked superseded):
   - `corpus/lessons/round-24.md:66` — `llm-judge-calibration.md` Gate row still reads "Q1–Q8 pass" although the same file's §Post-review corrections (`:120-122`) records the spot-check as "disagree (partial)" for that entry (S009 range + S012 location wrong). Rows `:65` and `:68` (contamination, agent-time) likewise needed post-admission Corrections, yet still read as clean passes. Supersession is only implicit, two screens down.
   - `.ufo/reports/round-24/kengaku.md:177-178` — "No admitted entry fails its re-check … 7 agree, 1 location disagree, fixed" undercounts (outside check found 5 location slips + 1 unreproduced range across 4 sources; `round-24.md:32` M22). Mitigated in-file by `:244+` §Post-review fixes in the same commit, but the trend bullet was left stale in place.

## Smallest append-only fix (lane-owned; no rewrite of either committed file)
Append one line to `corpus/lessons/round-24.md` §Post-review corrections (after `:141`), e.g.:
"Supersession: the §Gate rows reading `Q1–Q8 pass` for `contamination-detection-and-transparency.md`, `llm-judge-calibration.md`, and `agent-time-horizon-and-task-validity.md` are superseded by this section — each entry needed a post-admission correction (Q10); the per-entry self-checks were not re-run after the spot-check."
For the fleet report (integrator-owned, single commit `dec4b51`): an EOF erratum line pointing at `:244-270` ("trend bullet `:177` predates the outside check; see §Post-review fixes") — or leave it: the same file already carries the corrections, and r25's lesson can record the residual. Do NOT edit lines 65-69/177 in place.
r24 learning applied (considerthese/2026-10-20.md:20,34): self-administered gates overpass exactly where writer and checker share context — Q10 second-seat re-read and R6's non-author bar are the standing fixes; the one-line supersession marker above closes F5's remaining honesty gap without touching history.

## VERDICT: F5 PARTIALLY FIXED — substance corrected in e21f9ea and recorded in both files; the Gate "Q1–Q8 pass" rows (round-24.md:65-68) and report trend bullet (kengaku.md:177) still lack an explicit supersession marker; smallest fix = one appended supersession line in round-24.md §Post-review corrections.
Installs: none.
