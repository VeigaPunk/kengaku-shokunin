# F41CritPlanNext — attack on `SCORECARD.md` `### Planned (round 42)` (kengaku r41, wave 2, critic)

Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, read at `d7c77895752a2a5f317fa22f2362416ada50a04b` (`git rev-parse HEAD`; the
dispatch names `3d0058fb…`; the one commit between them, `d7c7789`, touches only
`.ufo/waves/round-41/falsify-{dispatch,spec}.json` (`git log --oneline 3d0058fb..HEAD --name-only`)). Nothing in the lane was
written. Only executable run: the read-only ledger printer `plans/routed_open.py`; no battery, counter, fixture build or sandbox run was
needed, so the bwrap envelope was not entered and no `~/.local/bin`/scratch write occurred. Report dir:
`.ufo/waves/round-41/falsify/F41CritPlanNext/`.

Axes named first (Godspeed): **A1** do-nothing reachability of a drafted predicate; **A2** axis/cap arithmetic (lowest non-retired axis, the
L0 cap); **A3** routed-item ownership; **A4** pointer resolution from the plan slot alone; **A5** staleness of tip-state facts. A1/A2/A3/A4
executed; A5 last.

## 0. Answers to the three questions

**Q1 — can a do-nothing control reach any candidate's predicate as drafted?** *Yes for two of the four candidates, and the question is
ill-posed for the other two because no predicate is drafted.*

| candidate | predicate in the plan slot | zero-work round-42 outcome |
|---|---|---|
| Calibration, "31 witnessed mutants over four tripwire tools" (`SCORECARD.md:1592`) | none: `total=31`→0 hits, `battery42`→0, `plans/round42`→0, `FLOORS`→0 | **reaches it verbatim.** The sentence is a tip-state: every one of the 31 witnesses is committed (`.ufo/waves/round-40/falsify/F40XMutAnchor/wit/`, `…/F40XMutLedgerOrder/wit-xo*.diff`, `…/build/R41PlanNext/res_*.json`), and the tools are pinned identical today (`sha256sum` → `11bb2cad87be…`, `853bcb2a5052…`, `948d5e1d2b34…`, equal to the plan's `11bb2cad…/853bcb2a…/948d5e1d…`), so the claim stays true with zero edits |
| `circuit-fibsqrt` (`:1599`) | none drafted | *red by construction but unnamed*: `grep -cE '^\| S12[567]' corpus/SOURCES.md` → `0`, and the round-41 C2 counter on a package-less tree gives `checks=8 defects=4` / `PREDICATE C2 fail` (`.ufo/…/R41PlanNext/c2-r41-counter-at-wave1-tip.txt`) |
| Novelty rider `input-crlf-rewrite` (`:1605`) | only "a dated prior-art receipt before the word novel" | **reaches it with no new probe bytes.** The measurement is already committed: `corpus/knowledge/tb2-constraints-scheduling-grader.md:247-248` ("a full CRLF rewrite of the inputs passes (`input-crlf-rewrite` `PPP`)"), `:36-37`, `:101-102`; the prior-art search already ran (`.ufo/waves/round-41/build/R41PlanNext.md` §8 ledger row "issue search": `universal newlines`, `CRLF integrity`, `read_text newline` → 0 hits) |
| fallback `openssl-selfsigned-cert` (`:1603`) | none | its own oracle is not green (`oracle 5/6`), so no admission predicate can be met as drafted |

**Q2 — is each candidate on the right axis with a stated reason?** *No: the plan slot states no axis value, no rule and no cap.*

- `sed -n '1575,1654p' SCORECARD.md | grep -c L0` → **0**; `… | grep -c lowest` → **0**. Round 41's own section carries both
  (`:1534` "Lowest non-retired axis: coverage 7, tied with novelty 7; … capped at 7 by the open L0 question `kengaku | round-33`"), and
  round 41's plan labelled candidates `Calibration (8)` / `Coverage (7, capped)` (`:1486`/`:1492`). The round-42 slot keeps the candidate list but
  drops the arithmetic.
- Axis arithmetic as measured: calibration **8** (`:729` re-derivation; unmoved since), coverage **7** *capped by L0*, novelty **7**.
  L0 `kengaku | round-33` is still open in the side channel (`.ufo/l0-questions.md:163`, verbatim: "what committed evidence lifts the
  round-25 L0 coverage cap … Candidate classes: (a) a PROVINCE.md coverage-surfaces section … (d) the cap stays"). Consequence the plan never
  states: **a round-42 coverage claim is score-dead (+0)** — its headline item 2 — while the only uncapped axis (novelty 7) is carried by the
  candidate that a do-nothing round also reaches. No candidate names the L0 as an item, so the cap enters its 10th round (33→42) unactioned.
- `Coverage/novelty` as a single label is not itself a defect (round 40 used `Coverage/novelty (tied 7)`, `:1417`); dropping `(tied 7)` and
  the universal `capped` mark from the one axis that is capped is.

**Q3 — is each routed item owned?** *No.*

`python3 plans/routed_open.py --lane .` → `ROWS total=10 open=4 blocked=1 closed=5 refused=0`, `routed_open=5 oldest_round=39`.
Named in the plan slot: **1 of 5** (`R40-R1`, `:1650`). Owned (a seat/acceptance that closes it): **0 of 5**. `grep -c 'R39-R' SCORECARD.md`
→ **0**, so `R39-R2` (open), `R39-R3` (blocked), `R39-R4` (open, with a `check` command) and `R40-R5` (open) appear nowhere in the file;
`R39-R3`'s substance survives only as the parenthetical "order class still blocked" inside the round-41 Frontier paragraph (`:1571`), outside
the plan slot. The scout's draft had a `Carried / routed:` bullet; `grep -c Carried` over the landed slot → **0**.

## 1. Defects (each: counterexample, evidence, impact, smallest safe correction)

**D1 — the calibration candidate's acceptance is do-nothing-reachable (high).** Counterexample: paste `:1592` unchanged into a round-42 claim;
it is a true tip-state, so an empty round scores. Evidence: the four predicate greps above return 0; the build report's own draft carried the
binding sentence and the control — `R41PlanNext.md:246-247` "Predicate: `MUTANTS total=31 killed=31 survived=0 invalid=0 null_detected=0`, per-tool
floors, `PREDICATE C1 pass`. Before (do-nothing control): no `plans/battery42` → `killed=0 survived=31`" — and that text is not in the plan
slot. Impact: A1; the same class `F40CritPlanNext` recorded for the round-41 plan (round-40 §Wave 2 outcome: "its predicate is reachable with
zero round-41 work as written"), recurring. Correction: restore the draft's predicate sentence verbatim plus the `no plans/battery42 →
killed=0 survived=31` control, and the carried `control-c1-no-mutants`/`TOTAL`/`FLOORS` non-vacuity leg (Q31).

**D2 — the one executed control the slot cites is `n/a`, and its pointer does not resolve in-repo (high).** Counterexample: follow
`:1598` "Do-nothing control executed: red (§4)". `sed -n '1575,1654p' SCORECARD.md | grep -nE '^#{1,4} '` lists only `§0 §1 §2 §2.1 §2.2`:
`§4`, `§2.3`, `§2.4`, `§2.5`, `§3.4`, `§8`, `§9` are all dangling, and the `Source:` line (`:1654`) names **only §6**. In the build report,
§4's first row executed as `MUTANTS total=20 killed=0 survived=20` … `PREDICATE C1 n/a (non-default battery or mutant subset)`
(`.ufo/…/R41PlanNext/near40_survivors_only.txt:44,46`) — i.e. *not* evaluated under a predicate. Impact: A4/A1 (calibration ceiling: "a gap
line contradicted by an artifact already in the repo"). Correction: cite `.ufo/waves/round-41/build/R41PlanNext.md` §4–§6 by name in `Source:`,
or restate the four control rows inline; replace "executed: red" with the red row that exists (`near-variants-r40-counter.txt:54,56`
`total=30 killed=10 survived=20` / `PREDICATE C1 fail`).

**D3 — the novelty rider is do-nothing-reachable and is already in the corpus (high).** Counterexample: a zero-work round-42 novelty claim
quoting `corpus/knowledge/tb2-constraints-scheduling-grader.md:247-248` plus the existing search receipt. Evidence: three committed locations
(`:36-37`, `:101-102`, `:247-248`); the scout's own control row concedes it — `R41PlanNext.md:219` "not executable until a counter exists …
the planner's call". Impact: A1/A2 — under the novelty rubric ("re-runs of known-shot batteries" cap) the single uncapped axis is carried by the
one candidate with no new measurement. Correction: either bind the rider to a new construct (a cross-grader instrument: how many of the seven
admitted graders' input-integrity checks compare decoded text — `grep -c integrity corpus/knowledge/tb2-*.md` → only the constraints entry
has any, `8`) with its own red control, or record it as carried, not a claim.

**D4 — `circuit-fibsqrt` has no counter/predicate line (medium).** Counterexample: the slot never names the admitting artefact; the draft did
("`plans/order_check.py`, V8", "Dry table written and frozen before the first recorded probe run", `R41PlanNext.md:247,254`). Evidence: `grep -c
plans/round42` → 0; the committed stand-in control (`checks=8 defects=4`, `V2 V3 V4 V7` red on missing spec/rows/receipt) is not cited.
Impact: A1/A4 — the candidate that is red-by-construction loses its receipt. Correction: restore the counter path, the V-check list and the
dry-table freeze order (V8) from the draft.

**D5 — the fallback's oracle is not green and no control is drafted (medium).** `:1603` "nop 0/6, oracle 5/6 on host OpenSSL 3.6.5". A
fallback whose reference run fails one case cannot yield a 100 % admission predicate; the plan states the number but neither prices nor
controls it. Correction: add "oracle 5/6 — admissible only with the failing case declared and excluded by id", or drop the fallback.

**D6 — the axis/cap arithmetic is absent (high; see Q2).** Evidence: `L0`→0, `lowest`→0 in the slot; `.ufo/l0-questions.md:163` still open;
`SCORECARD.md:1486`/`:1492` shows the convention the slot broke. Correction: one line per candidate with `(axis, current value)`, the frozen tie-break
paragraph, `coverage capped at 7 by the open L0 kengaku | round-33`, and either a priced L0 option (a) PROVINCE coverage-surfaces packet or
the statement that the round's score-bearing claim sits on novelty.

**D7 — the 31 is presented without its two limits (medium).** 17 of the 31 witnesses (8 `state_check` + 9 `round_close`) are the scout's own
command sets — `R41PlanNext.md:269` "The 46-command sources CLI set and the 9-command round_close set are my witnesses, not a frozen battery" —
and the 14 near-variant numbers come from the unedited round-40 counter, whose own draft says "the round-40 counter's tool runs are unsandboxed:
**not reused**" (`:246`). `grep -c unsandboxed` over the slot → **0**; `Q31`→0, `Q32`→0. Correction: add the two limit sentences and the
"witnesses re-derived on the landed bytes before freeze (Q29, Q30)" requirement to the candidate.

**D8 — routed ownership (high; see Q3).** Correction: restore the draft's `Carried / routed:` bullet, fenced as five rows with owner and
close-check, one per `R39-R2, R39-R3, R39-R4, R40-R1, R40-R5`.

**D9 — the R40-R1 repair list omits F2 (medium).** The bullet names six limits (`:1644-1650`: A1′ variant readable, T03/T04 dead-site, F2
AF_UNIX, F3 SysV IPC, F4 relative argv, F6 whole-file fingerprint) but the repair sentence covers content-binding, `--ro-bind-data`/hiding,
`--unshare-ipc`, `--tmpfs /run`, relative-token resolution and an attribution leg — F3, F4, F6, A1′, T03/T04 — and **no F2**: `--unshare-ipc`
and `--tmpfs /run` do not remove AF_UNIX sockets reachable through the `--dev-bind / /`. Correction: add "bind only the fixture root and
`/usr`,`/lib` (no host `/home`,`/run`,`/tmp` socket paths): F2", or mark F2 carried.

**D10 — a stale tip-state fact (medium).** `:1639-1640` (§2.1's note) "wave-1 batteries are in flight; the clone has no `plans/battery41`".
At the carrying commit `ls plans/battery41` → 7 modules and the landing measurement reads `BATTERY fixtures=48 … MUTANTS total=23 killed=23`
(`.ufo/waves/round-41/integrate/measure-final.txt:76-78`), so the instruction "re-derive after battery41 lands" is already actionable.
Correction: "battery41 landed at `74513c0` (48 fixtures, 23/23); whether its fixtures kill any of the 21 CLI-only kills is **unmeasured**" —
which is the honest state and keeps the price from being silently inherited.

## 2. What holds (measured, not assumed)

- **The 31 is arithmetically the selection the slot says**: 14 near-variants (9 anchor `X1 X3 X6 X7 X9 X12 X13 X14 X15` + 5 order `XO1 XO3 XO5
  XO6 XO7`) + 8 `state_check.main()` + 9 `round_close` = 31; over four tools (`anchor_digest_check`, `order_check`, `state_check`,
  `round_close`). The §2.1 table is internally consistent (27 = 9 standing + 6 witness kills + 12 survivors, of which 8 witnessed).
- **The tool pins re-derive exactly** (`11bb2cad/853bcb2a/948d5e1d`) and `git log -1 -- plans/anchor_digest_check.py plans/order_check.py
  plans/ledger_tip.py` → `34158b0` (round 39), so "unchanged since round 39" is true and the 20/30 number is not stale.
- **All 31 witness artifacts exist in-repo** (`F40XMutAnchor/wit/`, `F40XMutLedgerOrder/wit-xo{1..7}-basic.diff`, `R41PlanNext/res_state_main.json`,
  `res_round_close.json`) — only the citation shape differs between the two round-40 seats, so the pointer is recoverable.
- **`circuit-fibsqrt` is a genuinely new class against the seven admitted graders**: the only "sim"-shaped prior entry, `build-pmars`, grades an
  installed binary's existence and `ldd` (`grep -n sim corpus/knowledge/tb2-build-pmars-grader.md` → `src/sim.c` only as a directory-vs-file
  trick, `:34`), not a task-shipped simulator over a fixed input table. The "new class" phrase survives.
- **The CRLF phenomenon is not already a corpus pattern** beyond its own entry (`grep -c integrity corpus/knowledge/tb2-*.md` → one file, 8
  hits), so a cross-grader integrity instrument would be new — the defect is that the plan does not propose it.
- **`openssl-selfsigned-cert`'s 5/6 is reported, not hidden**, and the refused `schemelike-metacircular-eval` refusal is correctly motivated
  (TB2.1 #135/#235 publish its gaming surface).
- The two L1 bullets are honestly fenced: the hygiene item names itself unguardable ("unguarded until a round shows that check able to fail") and
  is owned by name (L1) — no defect.

## 3. Smallest safe correction set (one commit, no frozen file touched)

1. Import `.ufo/waves/round-41/build/R41PlanNext.md` §4, §5 and the §6 predicate/control/carried sentences into the plan slot (D1, D2, D4,
   D6, D8); keep the scout's `§0–§2` data as an appendix under the slot.
2. Fix the `Source:` line to `§0–§9` with the two control-receipt filenames (D2).
3. Replace the stale battery41 parenthetical with the landed numbers plus the one unmeasured clause (D10).
4. Add the F2 repair clause or mark F2 carried (D9).

## 4. Limits of this review

Text-and-artifact review only; I ran no counter, so I neither confirm nor dispute the 20/30, 12/27, 20/70 and 109-mutant figures beyond the pin
equality that makes them reproducible. Severity is a judgement about what a planner would get wrong, not a score. The dispatch tip `3d0058fb` differs from the read tip only by the one dispatch commit above; no lane file was edited by me.

VERDICT: plan42-defects-10
