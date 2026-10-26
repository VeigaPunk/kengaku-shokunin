# R39R38Integrate — round-38 wave-2 → round-39 dispositions (scribe)

Round-39 closure item **R1** ("wave-2 outputs uncommitted and unintegrated; commit the falsify tree and
integrate the findings"). Read-only seat: no lane file, Git index, jj state, fleet-root file, sibling lane or
`corpus/`/`plans/` tree was written; no clone or scratch dir was created (none was needed — every source is a
lane file read in place).

## 1. Behaviour

Mapped **every** round-38 wave-2 report to a disposition and grouped the map by the closure's routed items R1–R7,
with one explicit extension group R8 for findings the closure could not route (they come from reports written
after its read snapshot).

| quantity | value |
|---|---|
| reports mapped | 34 (34 seat dirs, 0 without a `.md`) |
| findings | 97 |
| `R39:<ITEM>` — decided this round by a wave-1 seat (draft/measure; L1 integrates) | 21 |
| `R40` — routed to round 40 (no round-39 item owns it) | 58 |
| `LIMIT` — record only (frozen instrument or append-only document) | 9 |
| `NONE` — no action, reason given | 9 |
| findings from the 14 reports the closure read | 36 |
| findings from the 20 reports that landed after its 03:21 -03 snapshot | 61 |
| by group | R1 1 meta-row (DONE, 0 findings) · R2 30 · R3 3 · R4 4 · R5 8 · R6 17 · R8 35 |

Deliverable: `.ufo/waves/round-39/build/R39R38Integrate/dispositions.md` (per-finding rows with the report id,
the finding's own label, the disposition, and the owner/reason), plus the §9 per-report inventory
(role, axes, verdict token, findings, groups).

### 1.1 R1 is satisfied at the tree level, before this seat

```
$ git ls-files .ufo/waves/round-38/falsify | wc -l
428
$ git log -1 --format='%h %cI %s' -- .ufo/waves/round-38/falsify/
ef2fba0 2026-10-26T03:37:53-03:00 round-38: wave-2 reports and results (34/34), outcome appended to lesson
$ git ls-files .ufo/waves/round-38/falsify.ready.dispatched
.ufo/waves/round-38/falsify.ready.dispatched
$ git status --porcelain -- .ufo/waves/round-38
(empty)
$ git ls-tree -r --name-only HEAD .ufo/waves/round-38/falsify | grep -c '\.md$'
37
```

37 = the 34 reports + `F38CritSkipControls/filler-entry-tb2-build-pmars-grader.md` (the control entry),
`F38EntryQuotes/receipts.md`, `F38RevLesson/receipts.md`. So R1's commit half is **DONE**; its integration half
is this map. Note for the L1: the closure's R2–R6 were written from **14** reports — `F38AnchorFix, F38C1Rerun,
F38C1RerunPy313, F38C2Rerun, F38CritBatD, F38CritBatE, F38CritNoHarmDiff, F38LedgerTip, F38MapV7Control,
F38MutDirection, F38ReopenRows, F38RevLesson, F38ScoutMisroot, F38XMutP` — so 61 of the 97 findings entered the
record only now.

## 2. Gates (what bit, what this seat checked)

No registered gate was executed and no frozen instrument was touched (nothing frozen was even opened for write).
The two checks this seat ran are fact pipelines over committed/readable bytes:

| check | command | observed |
|---|---|---|
| exhaustive report set, no unpaired seat dir | `for d in $(find . -maxdepth 1 -mindepth 1 -type d -printf '%f\n' \| sort); do [ -f "$d.md" ] \|\| echo "NO-MD: $d"; done` (in `.ufo/waves/round-38/falsify/`) | empty output → 0 |
| R6 scratch clause | `du -sh /fast/scratch/hyaku/kengaku-r38; ls -A /fast/scratch/hyaku/kengaku-r38 \| wc -l` | `0`, `0` — the 22 seat dirs (20 G at the round-38 sweep) are gone; empty directory remains |
| inventory total reconciles with the disposition rows | table parse over `dispositions.md` | 34 inventory rows, findings sum `97`; disposition rows `98` = 97 findings + 1 DONE meta-row; by code `R39 21 / R40 58 / LIMIT 9 / NONE 9` |

The closure's own gates (C1 `PREDICATE C1 fail` honest stop, C2 `PREDICATE C2 pass`) are unchanged by this map.

## 3. Touched surfaces

Written (new files only, inside this seat's report dir):

- `.ufo/waves/round-39/build/R39R38Integrate/dispositions.md`
- `.ufo/waves/round-39/build/R39R38Integrate.md` (this report)

Not written: the lane's `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md`,
`SHONEN.md`, `.ufo/waves/round-38/**`, Git index, jj state; the fleet root; sibling lanes; `/home/vgpnk/Projects/shokuknow`.
No `git add/commit/stash/checkout/reset/push/pull` and no jj command ran. No scratch dir was created or left behind.

## 4. What the map says, by routed item

- **R1** — `DONE` (`ef2fba0`, 34/34 reports + `falsify.ready.dispatched`); integration is this map. Residual: 20
  late reports were never routed by the closure.
- **R2 (C1 re-freeze) — 30 findings, the largest routed group.** Three of the closure's named survivors now have
  round-39 battery modules: `F38XMutP` X01 (P1 first pin only) → `R39BatP1` (M02), X05 (P3 quote above the range)
  → `R39BatP3` (M03), X15 (P7 second `source:` line) → `R39BatP7` (M04); `F38XMutRerunMain` #4 (`d5m` tag-strip
  gap) → `R39BatD5` (M07). Three wording/evidence items are drafted this round (`R39AdvErrata` for `F38CritBatE`
  D1/D2, `R39DirCheckLeg` for `F38MutDirection` m1/m2, `R39CritC1Equiv` for the Q29 pre-integration check).
  **Fourteen** R2 findings route to round 40 because they need a new freeze: pin completeness (`F38CritBatF`
  D1/D2, `F38RevBatB` residual 2, `F38SentinelBattery` F2), the ATTRIBUTED rule's exit-code blind spot
  (`F38XMutRerunMain` #2, `F38RevBatB` residual 1), the MAIN direction cell being inert (`F38C1Rerun`),
  `ctx.spec`/`sys.argv` harness doors, and the `uv`/locale host dependencies.
- **R3 (order-of-operations) — 3 findings, all decided this round.** `F38RevLesson` Defect 1/2 →
  `R39LessonErrata`; `F38C2Rerun` #4 ("not falsifiable from the tree") → `R39OrderGate` (+ `R39QualityQ30`).
- **R4 (recheck command) — 4 findings.** `F38ReopenRows` F38R-2/F38R-3 → `R39RecheckFix`; F38R-1 (a SOURCES row's
  quote is checked by nothing) and F38R-4 route to round 40 (a V3 extension / one entry clause).
- **R5 (D3/D4 residuals) — 8 findings.** `F38AnchorFix` F1 → `R39AnchorUnion`; `F38LedgerTip` F1/F2 →
  `R39LedgerProvenance`; F1's sibling F2 (deleting a claim silences the check) and `F38CritNoHarmDiff` R1 (the
  stale round-37 map row) are limits; `F38AnchorFix` F3 (`QUALITY.md` Q26 advertises the closed hole) and
  `F38CritNoHarmDiff` R3 route to round 40.
- **R6 (carried) — 17 findings.** The round-38 in-process patch (`F38CritSkipControls` b′, `F38SentinelBattery`
  F3) is answered by the round-39 counter's out-of-process fixture build, with `R39CritC1Counter` as the attacker;
  the informed-filler control (a) routes to round 40 (a V8) and is re-tested this round by `R39CritSkipC2`. The
  five-instance `--work` family (`F38C1Rerun` §8, `F38C2Rerun` #3, `F38NoHarmSweep` O-3, `F38SentinelBattery` F7,
  plus `F38MutDirection` #4's rc collision) routes to round 40 as one fix. **One live recurrence found here:**
  the shipped `pkg-spec-r39.json` carries `receipt_sha256: null`, exactly as `F38NoHarmSweep` O-1 reported for
  round 38 — §5 below.
- **R8 (extension, 35 findings)** — C2 counter mutants (`F38MutC2Counter`), the build-pmars entry prose and
  apparatus (`F38CritOverclaim` O1–O6, `F38EntryQuotes`, `F38RevQuality`), the tag/calibration gap
  (`F38CritTags`), separability claim text (`F38CritSeparability`), self-report disputes (`F38RevScorecard`), and
  all eight `plans/tip_receipts.py` attacks (`F38TipReceipts` F1–F8). One lands this round (`F38CritOverclaim`
  O7 → `R39AdvErrata`); the rest route to round 40. `F38IndepProbe`, `F38MapV7Control`, `F38ConnClaims` #1 and
  `F38CritN21` C1/C2 are counted as confirmations (0 findings) — the map records them anyway.
- **R7 (SHONEN, operator-owned)** — no wave-2 finding. `F38RevScorecard` §7 checked all four pointers resolve and
  found 0 mismatches; the four `[~]` remain honest partials. Not touched.

## 5. Findings (this seat's own; nothing re-run)

1. **R1's integration was never blocked on the reports — it was blocked on the *read*.** All 34 reports were in
   the tree by 03:37 -03 (`ef2fba0`), i.e. ~16 minutes after the closure's read snapshot; the closure's honest
   statement ("the remaining ~20 seats' reports were not available") is exactly 61 findings. Grouping by R1–R7
   alone would therefore have silently dropped 35 of them; R8 exists to prevent that. The L1 should treat R8 as
   part of the round-38 retrodiction, not as round-39 scope creep.
2. **`pkg-spec-r39.json` ships `receipt_sha256: null`, reproducing `F38NoHarmSweep` O-1 in round 39.**
   ```
   $ python3 -c "import json;d=json.load(open('plans/pkg-spec-r39.json'));print(repr(d.get('receipt_sha256')))"
   None
   $ python3 -c "import json;d=json.load(open('plans/pkg-spec-r38.json'));print(repr(d.get('receipt_sha256')))"
   None
   ```
   Round 38's measured consequence (`P2 DEFECT receipt_sha256=…`, rc 1, when the documented gate entry is run over
   the shipped spec) therefore applies to the round-39 package as well, while the C2 counter fills the field in a
   temp spec so its own `V2` is green. Disposition: `R39RevFreeze`/`R39RevCounters` should record it; the fix
   (populate the field, or state that P2 is a presence check) is round 40. I did not run the gate to reproduce the
   P2 line — that would be the frozen instrument's execution, not this seat's job.
3. **The round-38 closure's R2 list and the reports disagree in count, not in substance.** `F38XMutP` names three
   survivors (X01 P1, X05 P3, X15 P7) and `F38XMutRerunMain` adds a fourth killing shape (X15 D5 tag-strip) plus
   the `rc`-flip pair X07/X10; the closure's R2 wording ("the `F38XMutP` survivors … and the round-37/38 extra
   survivors") covers these, but the D5 tag-strip shape is the one round-39 turns into M07 — it comes from
   `F38XMutRerunMain` #4, a report the closure never saw, and **is the frozen witness cell of M07**:
   `plans/round39_c1_verify.py` M07 row cites `…/F38XMutRerunMain/survivor-probeB.txt (ref D5 ok rc=0 -> mutant
   D5 DEFECT rc=1)`. Recorded so the round-39 receipt credits the right seat.

## 6. Out of scope

- Round-38 **wave-1** build reports (`.ufo/waves/round-38/build/*.md`) and the closure's own §1–§4 findings, except
  where a routed item cites them (R1–R7 only).
- Any lane integration of the drafts (`R39BatP1/P3/P7/D5`, `R39AdvErrata`, `R39DirCheckLeg`, `R39LessonErrata`,
  `R39OrderGate`, `R39RecheckFix`, `R39AnchorUnion`, `R39LedgerProvenance`) — those seats write under
  `.ufo/waves/round-39/build/`; the L1 owns landing.
- Executing any frozen instrument (gate, counters, probe, `anchor_digest_check.py`, `ledger_tip.py`,
  `tip_receipts.py`). No tool was installed or upgraded; pacman is paused host-wide and nothing was needed
  (stdlib `python3`, `git`, `sha256sum`, `find`, `du`).

## 7. Artifact paths

- `.ufo/waves/round-39/build/R39R38Integrate/dispositions.md` — the map: §0 coverage/method/convention, §1 counts,
  §2–§7 R1–R6 tables, §8 R8 tables, §9 per-report inventory (34 rows, verdict tokens), §10 limits.
- `.ufo/waves/round-39/build/R39R38Integrate.md` — this report.

VERDICT: r38-wave2-mapped-34-findings-97
