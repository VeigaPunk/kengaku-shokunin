# R45Considerthese — considerthese mining and the round-45 slot (scribe, read-only)

Lane tip read: `05b02e2b` (2026-10-26, wave 1 in flight; 25 dirty paths, none mine). Files read in full:
`considerthese/2026-10-26.md`, `considerthese/2026-10-25.md`, `plans/round-45-claims.md`.
Nothing in the lane was edited; no counter, probe, fixture or battery was run by this seat (scribe scope, and
`do not rerun work merely to decorate the report`). Scratch `/fast/scratch/hyaku/kengaku-r45/R45Considerthese`
(emptied at the end, §7).

Every count below comes from one read-only inventory run inside the round-45 envelope
(`.ufo/waves/round-45/w1/R45Considerthese/considerthese-inventory.txt`):

```
ENVELOPE start 23:28:46 cwd=/home/vgpnk/Projects/shokunin
...
ENVELOPE end 23:28:48 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

## 1. Every proposal in the two files, and what the lane has for it

Six proposals: three in `2026-10-25.md`, three in `2026-10-26.md` ("proposals only; not acted on" heading in both).

| # | proposal (file:line) | status | artefact found at tip (grep/ls, absolute paths, lane-relative shown) |
|---|---|---|---|
| 25-1 | model-diverse verification: second model on a seeded ≥5-item discernment sample, agreement + disagreement log in SCORECARD (`2026-10-25.md:34-38`) | **OPEN** | `grep -rn "second model" SCORECARD.md corpus/QUALITY.md` → `0` hits; no seeded-sample log; `corpus/lessons/round-33.md:67` and `.ufo/waves/round-44/wave/R44ConsiderThese.md` §1 both rule it operator-side (routing table + scoring policy, not lane-reachable) |
| 25-2 | one persistent routed-defect ledger with (a) every closed defect re-run at tip, (b) block pre-registration on a twice-recurring class, (c) tip-receipt validator (`2026-10-25.md:39-44`) | **IMPLEMENTED** (b) weak | (a) `plans/defect_ledger.py` `7064B` + `plans/ledger_tip.py` `13221B` re-run `corpus/defects.jsonl` `1163B` and `corpus/defects-round35.jsonl` `1111B` (`ledger_tip.py:6-7,72-73`); (c) `plans/tip_receipts.py` `18778B` (docstring: "A receipt is only evidence if something re-runs it at the tip"); (b) `plans/order_check.py` `10300B` + QUALITY Q30, wired by `plans/round_close.py` `16418B` — but `corpus/QUALITY.md:292` states "`recurrence_of` is recorded, not enforced", so (b) is bookkeeping, not a block |
| 25-3 | decision packet for the round-25 L0 coverage cap (`2026-10-25.md:46-52`) | **IMPLEMENTED** | packet written: `.ufo/waves/round-33/build/R33L0Packet.md` `18844B`; landed in the fleet queue, read-only check `grep -c "kengaku \| round-33 \| decision packet" /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` → `1` (line 163). The cap ruling itself stays operator-owned; the proposal asked for the packet, and the packet exists |
| 26-1 | routed-findings burn-down: per-finding ids/rows, `routed_open` + age in SCORECARD, **and the freeze refuses a new coverage claim while the oldest open finding is >2 rounds old** (`2026-10-26.md:37-43`) | **PARTIAL** | ledger + tool + scorecard lines landed: `corpus/routed-findings.jsonl` 60 rows (`closed=34 open=23 refused=2 blocked=1`), `plans/routed_open.py` prints `routed_open=<n> oldest_round=<r>`. The **enforcement clause is absent**: `grep -n "max.age\|max_age" plans/routed_open.py plans/round_close.py corpus/QUALITY.md` → `0` hits; `--observe/--list/--selftest/--timeout` are the only flags (`routed_open.py:204-209`). Measured state: `rows=60 pending=24 oldest=39 by_round=[(39,3),(40,1),(42,20)]` → oldest is 6 rounds behind round 45 |
| 26-2 | one standing parametrised `tb2_grader_admit.py`, digest-pinned inputs, **a committed filler package that must stay red**, re-run at every tip; "a counter that admits filler should not appear in a verdict cell as the admission basis" (`2026-10-26.md:44-48`) | **PARTIAL** (chosen, §3) | ten per-round copies instead of one: `plans/round{36..45}_c2_verify.py` = `10` files, `3518` lines, `164316` B (r45 copy `591` lines / `27897` B); `plans/tb2_grader_admit.py` **ABSENT**, `plans/grader_admit.py` **ABSENT**; filler control is per-round and uncommitted — `find plans -maxdepth 2 -iname '*filler*'` → `0`, while r42 shipped `c2_filler_control.py` `3921B` + `control-c2-filler.txt` `318B` and r43 `c2_filler_control.py` `5979B` + `control-c2-informed-filler.txt` `1509B`, and **r44 and r45 claims ship `0` filler files** (r44 kept mirrors inside `.ufo/waves/round-44/wave/R44MutC2Guards.md:15,44`) |
| 26-3 | batch the TB2 sweep (oracle passes offline, nop fails, byte-equal re-runs) + class histogram + which tasks admit an offline probe; fold in the per-task flake rate (`2026-10-26.md:50-54`) | **PARTIAL** | static histogram landed: `.ufo/waves/round-43/build/R43ConsiderThese.md:12` "## Histogram (89 tasks, 11 classes)", fetched 89/89 graders, `LOG.md:1331-1332`; flake rider landed on 5 graders: `corpus/lessons/round-40.md:31` "15 end states graded twice without rebuilding, 15/15 same verdicts". The **executed screen across the tree was not run** — same file `:4`: "No task was run; only static reads"; `:133-137` is a candidate plan (F1 14 tasks, D1 wall-clock), not a sweep |

Tally, with "implemented" = the proposal's mechanism exists at the tip and something exercises it:
**implemented 2** (25-2 with the (b) caveat, 25-3) · **partial 3** (26-1, 26-2, 26-3) · **open 1** (25-1,
operator-side). Not fully implemented = 4; lane-actionable = 3.

## 2. Axes

1. **Frozen-surface collision** — round 45 freezes `plans/round45_c1_verify.py`, `plans/round45_c2_verify.py`,
   `plans/round44_c1_verify.py`, the probe, the spec, the gate, the dry table, the captures, `plans/refusals45/`,
   battery42–44, `.ufo/waves/round-45/claims/` (`plans/round-45-claims.md:6-12`).
2. **Cost inside one wave.** 3. **Does it close a measured, still-open defect.** 4. **Is the red control live today**
   (a rule with no red control is the r39 lesson's failure mode, `considerthese/2026-10-26.md:24-29`).
5. **Does it bear on this round's own admission basis** (C2 coverage claim + C1 fence), not on next round's.

| axis | 26-2 remainder (filler control + standing counter) | 26-1 remainder (routed age gate) | 26-3 remainder (executed sweep) |
|---|---|---|---|
| 1 frozen collision | none if additive: a control/QUALITY row/routed row; the frozen counter is only *imported* (r43 precedent `c2_filler_control.py:47,89`) | none (`routed_open.py`, `QUALITY.md`, `round_close.py` are unfrozen) | high: the sweep executes graders, and `plans/round-45-claims.md:20-23` (Q30) forbids grading this round's task pre-freeze; 89 tasks ≈ a wave of its own |
| 2 cost | 1 script + 1 committed fixture + 1 receipt + 1 QUALITY row (standing counter deferred, priced at ~500 lines) | 1 flag + 1 QUALITY row + 1 `round_close.py` leg | 89 task builds; image/network cost; largest job of the three |
| 3 measured defect | yes, and it grew: 2 of 10 counter rounds shipped a red filler receipt (r42, r43), r44/r45 shipped none | yes: `pending=24 oldest=39` (6 rounds), grew 5→10→52→39→24 across r41–r44 with no gate | yes, but partial by design: r43 chose to defer, and r44/r45 picked graders from its F1 recommendation |
| 4 live red control | yes: the current admission has no filler receipt, so "add the control" is red on today's tree by construction | yes: the live ledger (`oldest_round=39`) is the red | **no cheap red**: a red needs a second, flaked grader run |
| 5 bears on r45 | yes — it is the admission basis of the round's coverage claim (`plans/round45_c2_verify.py:14` "no V1-V10 check is relaxed") | yes but *against* the round: the clause would refuse this round's own C2 coverage claim (a coverage claim is what the proposal names) | no — it is a scouting job, and this round already has its grader |

## 3. Chosen: 26-2, scoped to the half that can land without touching frozen bytes

Full grounding note (the deliverable the seat asked for):
**`.ufo/waves/round-45/w1/R45Considerthese/grounding-note-26-2.md`**. In brief:

- **Lands as**: one QUALITY criterion (round-45 slot after Q38, `corpus/QUALITY.md:1025`) + one
  `corpus/lessons/round-45.md` calibration row + one generic `plans/c2_filler_control.py` (`--counter`, `--lane`,
  `--work`) with a committed filler package + one routed row `R45-C2-FILLER-CONTROL` so `plans/routed_open.py`
  counts it. **Not** a SOURCES row (those are mined external rows, S149–S156 this round).
- **Evidence**: the ten copies and their drift, the `plans/` filler-hit count of `0`, the r42/r43/r44/r45 filler
  receipts, the wave-2 mutation seat's content-only brief (`.ufo/waves/round-45/w2-spec.json` `items[13]`), and the
  stale filing at `SCORECARD.md:1775` (see §4).
- **Why it fits round 45**: the round's coverage claim is admitted by `plans/round45_c2_verify.py` — a tenth copy,
  the largest (`27897` B), on a tree where no red filler control exists. The proposal's own sentence ("a counter that
  admits filler should not appear in a verdict cell as the admission basis") is exactly this round's exposure, and
  the control that would answer it is a one-seat job that imports the frozen counter instead of editing it.
- **What I did not claim**: I ran no counter, so I do not assert `defects=0`/`defects=8` for round 45 beyond what
  `claims/control-c2-nothing.txt:23` (`checks=11 defects=8`) already records at the freeze.

Rejected runner-up, stated plainly: **26-1's age gate is the cheaper rule and it was already selected at round 44**
(`.ufo/waves/round-44/wave/R44ConsiderThese.md` §2–3, verdict `proposals-open-23-chosen-26P1`) and did not land
(`0` hits for `max.age|max_age`). Re-selecting it would be the second consecutive pick of the same remainder, and its
first act on this tree is to refuse the round's own frozen C2 — a rule whose only witness is the work it forbids is
not a wave-1 landing. It stays routed as the recommendation for round 46, where it can refuse the *next* freeze.
**26-3** is the right next round's steering job (r43 priced it), not a build-wave item, and `25-1` is not lane-actionable.

## 4. Findings

- **F1 — `SCORECARD.md:1775` states a landing that no longer holds.** "`considerthese/2026-10-26.md` proposal 2
  (filler-control half) → V9", but in the round-45 counter V9 is "content consistency"
  (`plans/round45_c2_verify.py:45`) and the mechanism leg is V10 (`:47`); the r43 control records the filler refusal
  on V10 (`control-c2-informed-filler.txt:3-4`). The capability survives in V9(a) (`## Case table` equality), the
  *control* does not.
- **F2 — the round-45 freeze file carries no considerthese clause.** `grep -n considerthese plans/round-45-claims.md`
  → 0 hits, while `plans/round-44-claims.md:122` carries "at most one considerthese proposal lands". This seat's
  "at most one" therefore rests only on its own brief and the L1's integration.
- **F3 — measurement hazard, my own first numbers.** In this session's shell `diff` resolves to `diff (pi-uu-diff)
  0.8.0`; inside the envelope it is `/usr/bin/diff` GNU 3.12, and the two disagree on the same bytes (r36→r37:
  `410` vs `421` lines). All drift numbers in this report and the grounding note are GNU `diff` inside the envelope.
  A seat quoting `diff | wc -l` without naming the binary is quoting an unknown program.
- **F4 — the filler receipt exists for 2 of 10 counter rounds** (r42, r43), was uncommitted in all of them
  (`plans/` filler hits `0`), and round 45's wave specs assign no filler leg (`w2-spec.json` `items[13]`).

## 5. Out of scope / deliberately not done

- No counter, probe, fixture or battery executed (scribe: reruns are the executor's job; §Q32 envelope used for the
  read-only inventory only).
- No edits to `plans/`, `corpus/`, `SCORECARD.md`, `LOG.md` or any lane file; the draft note lives in this seat's
  subdir for the L1.
- No git/jj mutation; no subagents; no tool installs (nothing needed; `diff`, `python3`, `find`, `stat` suffice).

## 6. Limits

- Statuses are reads of the tip `05b02e2b`, not executions; where a number would need a run I cite the frozen receipt
  instead (`claims/control-c2-nothing.txt:23`) rather than producing one.
- "Implemented" is my judgement from artefact presence plus one exercise path; 25-2(b) is explicitly recorded-not-
  enforced (`corpus/QUALITY.md:292`) and I count it as implemented with that caveat rather than upgrading it.
- The grounding note prices the standing counter but does not build it; feasibility rests on the r43 precedent's
  import-by-path pattern, which I read but did not re-run.

## 7. Files

- This report: `.ufo/waves/round-45/w1/R45Considerthese.md`
- Envelope receipt (`3728B`): `.ufo/waves/round-45/w1/R45Considerthese/considerthese-inventory.txt`
- Grounding note (`5911B`): `.ufo/waves/round-45/w1/R45Considerthese/grounding-note-26-2.md`
- Measurement script (scratch, deleted): `/fast/scratch/hyaku/kengaku-r45/R45Considerthese/measure.sh`
- Tooling installed: none.

VERDICT: proposals-6-implemented-2-chosen-26-2-filler-control
