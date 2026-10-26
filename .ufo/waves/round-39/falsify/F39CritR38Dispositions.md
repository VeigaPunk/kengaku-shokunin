# F39CritR38Dispositions — are the round-38 dispositions true at the tip?

Seat: critic (leaf), round-39 wave 2 (FALSIFY), 2026-10-26. Target:
`.ufo/waves/round-39/build/R39R38Integrate/dispositions.md` (34 reports, 97 findings; 21 `R39:<ITEM>`, 58 `R40`,
9 `LIMIT`, 9 `NONE`). Frozen claims `plans/round-39-claims.md` (freeze `088f7c36…`); landing measurement
`.ufo/waves/round-39/integrate/measure-final.txt` (TIP `34158b0`). All checks are against a clean
`--no-local` clone of lane tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (master is now `acf4375`, two
commits later; `git diff --stat 34158b0 a6832f53 -- plans/ corpus/` = only `corpus/lessons/round-39.md`, so
`measure-final`'s numbers transfer). Host: Python 3.14.8, git 2.56.0. Scratch
`/fast/scratch/hyaku/kengaku-r39/F39CritR38Dispositions` (`TMPDIR` there, removed at exit). No lane or fleet-root
file written; receipts beside this report.

**Axes named before the work.** (1) **calibration** — does each finding coded "fixed this round" have an
artifact at the tip that a reader can run? (2) **quality** — does the cited artifact actually contain the claim
attributed to it (provenance), and does the disposition code mean what its own legend says? (3) **operability** —
do the landed tools still run at the tip? (4) **freshness** — is an `R40` route a real route (named in
`SCORECARD.md` §Planned (round 40) or the lesson) or a dead letter?

## 0. Legend problem the whole check rests on

The map's own legend says `R39:<ITEM>` = "decided this round by a round-39 wave-1 seat (the item drafts or
measures; the L1 integrates — no lane file is written by these seats)" (`dispositions.md:34-35`), and §10
repeats "Whether the L1 lands the draft is outside this map" (`:262-263`). So the file never literally claims
"fixed". It is nonetheless the round's only closure ledger, and five of its 21 `R39:` rows are not closed even
at that weaker bar (an item decided *not* to fix, or an item that never addressed the finding). The single
count I found most load-bearing: **16 of 21 `R39:` rows hold at the tip; 0 of 58 `R40:` rows are named in
`Planned (round 40)` or the lesson.** The two questions in the assignment cover 21 + 58 = **79** rows, so the
terminal count is `16/79`; the `LIMIT` (9) and `NONE` (9) rows are outside both questions and are not scored.

## 1. The 21 `R39:` rows — command and output at the tip

`S=/fast/scratch/hyaku/kengaku-r39/F39CritR38Dispositions`; every command below ran in `$S/lane` except where
noted. Numbers in the table are the outputs, not summaries.

| # | finding (report) | item | check at `a6832f53` | verdict |
|---|---|---|---|---|
| 1 | F38XMutP X01 — P1 checks only the first pin | R39BatP1 | `plans/battery39/p1m.py` = seat copy (`a82fa251…`); counter prints `MUTANT M02 … killed by=p1m-second-pin-appended-bytes` | **verified** |
| 2 | F38XMutP X05 — P3 accepts a quote one word over | R39BatP3 | `p3m39.py` (`fd16681e…`); `MUTANT M03 … killed by=p3m39-quote-one-word-above-upper-bound` | **verified** |
| 3 | F38XMutP X15 — P7 tolerates a second `source:` | R39BatP7 | `p7m39.py` (`2c228ba8…`); `MUTANT M04 … killed by=p7m39-s105-two-source-lines` | **verified** |
| 4 | F38CritBatE D1 — N11 `adv` overstates | R39AdvErrata | `SCORECARD.md:1407-1409` names it: "N09's and N11's `adv` sentences overstate what the frozen gate enforces (`F38CritBatE` D1/D2)" | **verified** (erratum only; the reword is neither at the tip nor in `Planned (round 40)`, see §3.4) |
| 5 | F38CritBatE D2 — N09 `adv` credits "distinct" | R39AdvErrata | same sentence | **verified** |
| 6 | F38MutDirection #2 — one-path mislabel signal | R39DirCheckLeg | `plans/mutant_direction_check.py` = fixed copy (`e471630a…`); tip run prints `LEGS mutants=22 disagree=0 invalid=0`, and the seat's receipts show m1/m2 (`old` survives, `new` exit 1) — byte-identical source | **verified** |
| 7 | F38CritN21 D2 — Q29's check could not run at freeze | R39CritC1Equiv | measurement row, no lane file expected; `measure-final.txt:542` ran the check at landing, and my tip run reproduces it (`DIRECTIONS total=22 mislabelled=1`, N21 the known honest stop) | **verified** (measurement) |
| 8 | F38RevBatA residual 2 — a fixture mutating `ctx.spec` poisons later fixtures | R39RevCounters | the item prescribes "verify the child-process contract isolates it"; its finding 1 (MEDIUM) answers **no**: "a battery39 module can therefore rewrite a pinned lane input mid-run and the counter neither notices nor aborts" (`R39RevCounters.md:40-41`), recommendation "post-freeze errata or round-40" (`:51`) | **NOT fixed** |
| 9 | F38XMutRerunMain #4 — D5 tag-strip half unshown | R39BatD5 | `d5m39.py` (`cb2edc67…`); `MUTANT M07 … killed by=d5m39-tagged-quote-span` | **verified** |
| 10 | F38RevLesson Defect 1 — half-quoted round-37 fix | R39LessonErrata | `corpus/lessons/round-38.md:94` `## Errata (round 39…)`, row-2 correction with the missing rule-forward | **verified** |
| 11 | F38RevLesson Defect 2 — `census-before.txt` inside "all red" | R39LessonErrata | same block, header sentence superseded, "no measurement is wrong — the label is" | **verified** |
| 12 | F38C2Rerun #4 — order-of-operations not falsifiable | R39OrderGate | `plans/order_check.py` = draft (`948d5e1d…`), `corpus/QUALITY.md:522` Q30; tip run: round 38 `ORDER RESULT FAIL` exit 1, round 39 `ORDER RESULT PASS` exit 0 | **verified** |
| 13 | F38ReopenRows F38R-2 — `sha256sum -c` reds from lane root | R39RecheckFix | errata blocks landed on three entries (`tb2-regex-log-grader.md:320`, `tb2-git-webserver-grader.md:448`, `tb2-build-pmars-grader.md:344`); the four corrected `(cd … && sha256sum -c SHA256SUMS)` legs are all `OK` at the tip | **verified** |
| 14 | F38ReopenRows F38R-3 — TB2.1 comparison unpinned | R39RecheckFix | `tb2-build-pmars-grader.md:357-373` pins `7131e437…` with six digests and a one-liner | **verified** (pin text; I did not re-fetch upstream — see §5) |
| 15 | F38AnchorFix F1 — digest bound by union of locators | R39AnchorUnion | `plans/anchor_digest_check.py` = draft (`11bb2cad…`); tip `rows=111 tokens=19 defects=0` exit 0; the seat's union fixture D at the tip → `TIP exit=1 … class=capture-unanchored`, restore verified | **verified** |
| 16 | F38LedgerTip F1 — stale `refs/heads/master` read silently | R39LedgerProvenance | `plans/ledger_tip.py` = draft (`853bcb2a…`); on master tip `REF AUDIT ref=refs/heads/master … state=match`, `rows=9 … mismatches=0` exit 0; stale fixture → one `REFUSE stale pin ref …` exit 2 | **verified** |
| 17 | F38LedgerTip F2 — refusal mid-ledger prints false `agree=NO` | R39LedgerProvenance | stale-fixture output has exactly two lines (`TIP`, `REFUSE`); `grep -E '^(R34|R35|LEDGER)'` empty | **verified** |
| 18 | F38CritSkipControls b′ — in-process patch reaches `PREDICATE C1 pass` | R39CritC1Counter | reproduced at the tip: drop the critic's `zz_inproc.py` into `plans/battery37/` → counter prints `BATTERY fixtures=92 wrong=0 …`, `MUTANTS total=7 killed=7`, `PREDICATE C1 pass`, **exit 0**, with `M02/M03/M04/M07` killed by `a3z-forged-*` fixtures | **NOT fixed** |
| 19 | F38SentinelBattery F3 — fixtures are arbitrary in-process code | R39CritC1Counter | same run: the class survives one directory left (`plans/round37_c1_verify.py:258-267` `exec_module`); and the four battery39 kill carriers are pinned **0** times (`PINS` 26 = 12 battery38 + 0 battery39) | **NOT closed** (battery38/39 out-of-process only) |
| 20 | F38NoHarmSweep O-1 — shipped spec has `receipt_sha256: null` → gate red at P2 | R39RevFreeze | `plans/pkg-spec-r39.json:6` `"receipt_sha256": null`; `pkg_gate.py package --root . --spec plans/pkg-spec-r39.json` → `P2 DEFECT receipt_sha256=d7f3a465…`, `defects=1`, exit 1. The cited report never mentions it (`grep -n 'null\|receipt' R39RevFreeze.md` → only `null_detected=0` at `:64`) | **NOT fixed** |
| 21 | F38CritOverclaim O7 — "attributed 21/22" precedes the review it needs | R39AdvErrata | the item's own 12-item list is `F38CritBatE` D1/D2, `R38CritClaims` §1, `F38CritBatF` D1/D2, `F38SentinelBattery` F1–F7 (`R39AdvErrata.md:21-33`) — **no O7**; `grep -nE '21/22\|title\|O7' R39AdvErrata.md` empty; the tip erratum paragraph does not mention it | **NOT addressed** |

**Row counts.** 16 verified / 21. Five rows fail. Two of the failures (#20, #21) are provenance failures — the
cited artifact does not contain the fact attributed to it; two (#18, #19) are closure failures — the wave-1
item attacked the mitigation and the attack still passes at the tip; one (#8) is an item that answered its own
question "no" and was nonetheless coded as decided.

Supporting tip output (full files in the receipt directory):

```
$ python3 plans/round39_c1_verify.py --lane . --work "$S/work-c1"        # rc=0
PINS total=26 mismatched=0
BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M02 P1 silence killed by=p1m-second-pin-appended-bytes …
MUTANT M03 P3 silence killed by=p3m39-quote-one-word-above-upper-bound …
MUTANT M04 P7 silence killed by=p7m39-s105-two-source-lines …
MUTANT M07 D5 mirror killed by=d5m39-tagged-quote-span …
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

## 2. The 58 `R40:` rows — named anywhere?

Method: extract the `Planned (round 40)` block (`SCORECARD.md:1411-1420`) and the whole round-39 lesson
(`corpus/lessons/round-39.md`, 67 lines), then test each routed finding's distinctive token and each report id.
Receipt `r40-naming-test.txt`.

| document | what it names | of the 58 |
|---|---|---|
| `SCORECARD.md` §Planned (round 40) | three bullets: C1 re-freeze with four soundness repairs, tripwire-mutation tests (anchor/ledger-tip/`order_check`), `db-wal-recovery` + `openssl-selfsigned-cert` fallback + `polyglot-c-py` rider, and a frozen `defect_ledger` check. The only ids are `R39CritC1Counter` and `R39PlanNext`. | **0** |
| `corpus/lessons/round-39.md` | no `F38…` id appears at all (`grep -c 'F38'` → 0); no "Forward"/"round 40" rule list | **0** |

Token probe, per finding family (all zero in both documents unless noted): `sys.argv` (F38RevBatA r1),
`UTF-8|encoding|LC_ALL` (Py313 F3), `pin the probe interpreter` (Py313 F4 / Sentinel F1),
`Q26` (F38AnchorFix F3), `13+1+6` (NoHarmDiff R3), `--work` (the five-row `--work` family), `stricter on every
input` (N21 D1), `ldd` (Overclaim O1), `pmars-dir-elsewhere` (ReopenRows F38R-4), `fourth grader`
(RevScorecard d1), `TipReceipts`, `no-committed-re-run-command` (TipReceipts F1). The three nonzero-looking hits
(`filler`, `violates=`, `89`) are pre-existing round-37/38/39 claim text (`SCORECARD.md:1277,1345,1355,1397,1016`),
not a naming of any routed finding.

**Three of the 58 are contradicted, not routed.** `R39AdvErrata.md:15` says "Three are already fixed by the
round-39 freeze"; its items 4, 5, 7 are `F38CritBatF` D1, `F38CritBatF` D2 and `F38SentinelBattery` F2 — the map
codes all three `R40` (`dispositions.md:87,88,143`). Tip agrees with the seat, not the map: `PINS` = 26 with 12
`plans/battery38/*.py` digests, and the counter prints `SETUP … failed to build` for an unbuildable fixture.

**Net for question 2: 0 of 58 named; 3 of 58 already resolved; 55 live and unplanned.** Two of the 55 are
demonstrably live at the tip by this seat's own runs: the `--work` family (`F38SentinelBattery` F7,
`F38C1Rerun` §8, `F38C2Rerun` #3, `F38NoHarmSweep` O-3 — `FileNotFoundError`, exit 1, no `PREDICATE` line;
receipt `work-absent-crash.txt`) and the unpinned kill carriers (§3.2).

## 3. Counterexamples (each is a receipt, not an opinion)

### 3.1 The in-process attack survives the round's stated mitigation (rows 18, 19)

`round39_c1_verify.py:38-40` says "each module is imported and built in a CHILD process … A module therefore
cannot patch this counter's `run_gate`". That sentence is true for `battery38`/`battery39` only; the frozen
round-37 loader is still executed in-process (`plans/round37_c1_verify.py:258-267`), and the pin set is a name
list, so a tenth file is unpinned. Reproduced verbatim from the wave-1 attack artifact:

```
$ cp …/build/R39CritC1Counter/zz_inproc.py plans/battery37/zz_inproc.py
$ python3 plans/round39_c1_verify.py --lane . --work "$S/work-a3"        # rc=0
PINS total=26 mismatched=0
BATTERY fixtures=92 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M01 … killed by=a3z-forged-d5-accept
MUTANT M02 … killed by=a3z-forged-reject
MUTANT M03 … killed by=a3z-forged-reject
MUTANT M04 … killed by=a3z-forged-reject
MUTANT M07 … killed by=a3z-forged-d5-accept
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

The L1's separate audit does catch it — `PINS total=26 mismatched=1 first=plans/battery37/zz_inproc.py`,
`AUDIT unpinned battery module present; refusing to import it`, exit 2 — but `round39_c1_audit.py` is not the
frozen rule: the frozen predicate still prints `pass`, exit 0. A reader who takes "the out-of-process build is
the round-39 mitigation" as the closure of `F38SentinelBattery` F3 is taking the audit's coverage for the rule's.

### 3.2 The round's own four kills ride unpinned files (recurrence of `F38SentinelBattery` F2, coded `R40`)

`PINS` = 26 entries: 12 `battery38`, **0 `battery39`** (`receipt-fixes-at-tip.txt`). M02/M03/M04/M07 are killed
by `plans/battery39/{p1m,p3m39,p7m39,d5m39}.py`, none of which any pin covers; `R39AdvErrata.md` item 4 states
this as an unnamed residual. So F2's class ("the kills are carried by unpinned fixture files") is fixed for
`battery38` and recurs on the round's own kill carriers — and it is routed to round 40 without being named there.

### 3.3 A live, unnamed `R40` row, reproduced: the `--work` parent family

```
$ python3 plans/round39_c1_verify.py --lane . --work "$S/work-absent2"   # directory absent; rc=1
  File ".../plans/round39_c1_verify.py", line 268, in main
    root = pathlib.Path(tempfile.mkdtemp(prefix="k39-c1-", dir=a.work))
FileNotFoundError: [Errno 2] No such file or directory: '…/work-absent2/k39-c1-…'
```

No `PREDICATE` line, exit 1 where SKILL's taxonomy says 2. Five map rows point here; `Planned (round 40)` and the
lesson mention `--work` zero times.

### 3.4 Round-39's own gate entry is red at the tip (row 20)

```
$ python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r39.json   # rc=1
P1 ok pinned=2 mismatched=0
P2 DEFECT receipt_sha256=d7f3a465ccc411572c96fc039235854093d1eb52ccd685b618a28a10de609b5f
…
defects=1
```

The C2 counter's V2 hides this by filling the pin in an *effective* copy (`round39_c2_verify.py:120-122`
`s["receipt_sha256"] = sha256(...)`), so `checks=7 defects=0` is green while the shipped spec stays red. That is
the same shape `F38NoHarmSweep` O-1 recorded for round 38, re-observed this round and then coded `R39` with a
citation ("see report") the report does not support.

### 3.5 Where the fix is real, it is byte-identical to the wave-1 draft

All four landed script fixes are byte-identical to their seat drafts (`receipt-fixes-at-tip.txt`): anchor
`11bb2cad…`, ledger-tip `853bcb2a…`, direction `e471630a…`, order `948d5e1d…`; the four battery39 modules are
identical to their seat copies too. So the 16 verified rows are landings of what wave 1 measured, not
re-implementations — the gap between 16/21 and 21/21 is in the disposition codes, not in the L1's integration.

## 4. Root cause and smallest safe correction

**Root cause.** One code (`R39:`) means three different things — *fixed at the tip*, *measured by an item*, and
*the item decided to defer* — and one code (`R40`) means "routed" without a route. The map's legend admits the
first ambiguity (`:34-35`) but the rest of the round reads it as closure: `SCORECARD.md:1400-1405` lists the
routed work as done — "round-38 closure R2 (N21 relabelled, rc legs, out-of-process build; direction check gains
a redundant leg …)" — while the "out-of-process build" half is exactly rows 18/19, which the in-process battery37
attack still passes (§3.1).

Smallest corrections, in order of value:

1. **Re-code the five rows** (map lines for #8, #18, #19, #20, #21) as `LIMIT` or `R40` with the exact open
   property; in particular state for #18/#19 that the frozen predicate is still gameable through
   `plans/battery37/`, and that `round39_c1_audit.py` is a separate instrument, not the frozen rule.
2. **Pin the four `battery39` modules** (`PINS` 26 → 30) or record "the round's kills rest on unpinned bytes" as
   a limit in the lesson — one line either way; this is the recurrence of F2 on the round's own carriers.
3. **Fix or declare `receipt_sha256`** in `plans/pkg-spec-r39.json` (one line), otherwise the documented gate
   entry stays red and the C2 green is an effective-copy green.
4. **Drop the `R39AdvErrata` attribution for O7**; the item's 12-item list has no O7. Route it or record `NONE`
   with a reason.
5. **Replace `R40` with a named target**: either add the 58 findings to `Planned (round 40)` (impossible at 3
   bullets — use one line naming the map + the group codes) or state in the map that `R40` is an intake pool and
   not a commitment. As written, 55 live findings have no named successor.

## 5. Limits of this check

- No network: row 14's TB2.1 pin is verified as text at the tip, not by re-fetching `7131e437`.
- Row 7 is a measurement row; "verified" means the check named in Q29 was executed at the landing and
  reproduces at the tip, not that a lane file changed.
- The 58-row naming test is keyword/report-id based; a paraphrase that names a finding without any of its
  tokens would be missed. I read both documents in full as a guard, and both are short (10 and 67 lines).
- I did not re-run the C2 predicate or the probe; C1, the audit, the four tripwires, the gate's shipped spec and
  the two ledger modes were re-run from the clone.
- The dispositions file itself is a wave-1 build artifact; I did not edit it (out of scope for a critic).

Axes touched: calibration (16/21 closure, 0/58 routes), quality (2 provenance failures), operability (working:
anchor, ledger, order, direction, C1; not re-run: C2; broken: `--work` taxonomy, shipped spec entry), freshness (the round-40
plan names none of the carried work).

VERDICT: dispositions-verified-16/79
