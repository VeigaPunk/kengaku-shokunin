# Grounding note — considerthese 2026-10-26 proposal 2 (chosen for round 45)

**Proposal (verbatim, `considerthese/2026-10-26.md:44-48`):** "a single parametrised `tb2_grader_admit.py` that
digest-pins the spec, dry table and probe it reads (the r37 V2 hole), ships a committed filler package that must stay
red, and is re-run at every tip for all five admitted graders. A counter that admits filler should not appear in a
verdict cell as the admission basis."

## What it would land as (three artefacts, cheapest first)

1. **One QUALITY criterion** (round-45 slot, next free number after Q38 at `corpus/QUALITY.md:1025`):
   *An admission counter's filler control is a committed, counter-parameterised artefact re-run at the tip. A verdict
   cell that quotes `checks=N defects=0` names the receipt of a control that stays red on a content-free and an
   informed filler; a control that exists only inside one round's wave scratch is not a control.*
2. **One lesson row** in `corpus/lessons/round-45.md`, class calibration: "an admission basis without a control",
   pointing at the r42→r45 filler-control drift below.
3. **One code artefact** `plans/c2_filler_control.py` (generic; takes `--counter plans/round<NN>_c2_verify.py`,
   `--lane`, `--work`) plus a committed filler package under `plans/fixtures/`. Feasible without touching any frozen
   file: the r43 precedent imports the frozen counter by path and calls its checks —
   `.ufo/waves/round-43/claims/c2_filler_control.py:47` `spec_from_file_location("c2", lane / "plans/round43_c2_verify.py")`,
   `:89` `ok9, note9 = c2.v9(m)`.
4. **One routed row** `R45-C2-FILLER-CONTROL` in `corpus/routed-findings.jsonl` with a `check` (`test -f` on the
   control + its red receipt), so the gap is counted by `plans/routed_open.py` instead of dying in a report.

Not a SOURCES row: `corpus/SOURCES.md` rows are mined external artefacts (this round S149–S156).

## Evidence it points at (all measured; receipt `.ufo/waves/round-45/w1/R45Considerthese/considerthese-inventory.txt`)

- **Ten per-round copies, not one counter.** `ls -1 plans/round*_c2_verify.py | wc -l` → `10`; total `3518` lines /
  `164316` B; the round-45 copy is `591` lines / `27897` B (`plans/round45_c2_verify.py`). GNU `diff` drift
  r44→r45 = `355` lines, r43→r44 = `331`. No standing tool: `plans/tb2_grader_admit.py` **ABSENT**,
  `plans/grader_admit.py` **ABSENT**.
- **The filler control is a per-round throwaway.** `find plans -maxdepth 2 -iname '*filler*'` → `0` hits (nothing
  committed in the tree). Per-round claims: r42 `c2_filler_control.py` `3921B` + `control-c2-filler.txt` `318B`;
  r43 `c2_filler_control.py` `5979B` + `control-c2-informed-filler.txt` `1509B`; **r44 `0`, r45 `0`** (r44 kept its
  mirrors inside a wave sweep, `.ufo/waves/round-44/wave/R44MutC2Guards.md:15,44`). So **2 of the 10 counter rounds
  shipped a red filler receipt** (r42, r43), and the round 45 admission has none.
- **Round 45's plan does not add one.** `grep -rl filler .ufo/waves/round-45` → only this seat's own receipt and one
  connector table row (`.ufo/waves/round-45/w1/R45ConnPattern.md:15`, which names the readable-key hole, not the
  missing control). The wave-2 mutation seat's whole brief is content mutations (anchor sha, quote, requirement row,
  case rename, mechanism `line+1`) — `.ufo/waves/round-45/w2-spec.json` `items[13]`, no filler leg.
- **The lane's own record is stale.** `SCORECARD.md:1775` files "`considerthese/2026-10-26.md` proposal 2
  (filler-control half) → V9", but in the round-45 counter V9 is "content consistency" (`plans/round45_c2_verify.py:45`)
  and the mechanism leg is V10 (`:47`); the r43 control records the refusal living on V10
  (`control-c2-informed-filler.txt:3-4`, `V9 DEFECT case_rows=0/12`, `V10 DEFECT no '## Mechanism' section`).
  The counter's claim "no V1-V10 check is relaxed" (`:14`) is true of the checks and unsupported as evidence of the
  filler leg at r45.
- **The limit the proposal names is live.** an informed filler that copies the receipt passes V9-as-consistency
  (`SCORECARD.md:1748`: "V9 is a consistency check, not a content check"; `corpus/QUALITY.md:1030`), and the open-coded
  truth-table limit is stated by this round's own counter (`plans/round45_c2_verify.py:25-26`).

## Why not the standing counter this round

Every round freezes a C2 counter (`plans/round-45-claims.md`, frozen surface list), so the round-44 deferral
("a round with no frozen C2 counter", `.ufo/waves/round-44/wave/R44ConsiderThese.md` §3) is unfalsifiable: no such
round can occur. The refactor must therefore be **additive** — a net-new tool that reproduces the frozen counter's
V1–V10 verdicts on the same package and is proven not to weaken the filler leg. That proof needs the committed control
first, which is why artefact 3 is the precondition and not the whole proposal. Price: V1–V10 is ~500 lines of
package-shaped logic (holds, registry anchors, census, order gate, receipt, case table, mechanism) → a wave-2 or
next-round seat, not a wave-1 scribe job.

## What I opened to verify it

`considerthese/2026-10-25.md`, `considerthese/2026-10-26.md` (full); `plans/round-45-claims.md` (full);
`plans/round45_c2_verify.py:1-70`; docstrings of `plans/round42_c2_verify.py:14,30-42` and
`plans/round44_c2_verify.py:14-50`; all ten `plans/round{36..45}_c2_verify.py` (stat + line count + GNU diff);
`.ufo/waves/round-42|43/claims/c2_filler_control.py` (+ their receipts), `.ufo/waves/round-44/wave/R44MutC2Guards.md`;
`.ufo/waves/round-45/w2-spec.json` (items[13]); `corpus/QUALITY.md:1025-1040` and `:292`; `SCORECARD.md:1748,1775`;
`corpus/routed-findings.jsonl` (60 rows, parsed); `plans/routed_open.py:1-40,202-209`; fleet
`.ufo/l0-questions.md:163`; `.ufo/waves/round-43/build/R43ConsiderThese.md:4,133-137`; `corpus/lessons/round-40.md:31`;
`.ufo/waves/round-44/wave/R44ConsiderThese.md`.
