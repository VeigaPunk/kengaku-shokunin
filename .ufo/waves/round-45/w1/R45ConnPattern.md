# R45ConnPattern — cross-claim pattern scan (connector, round 45 wave 1)

Reads: `corpus/lessons/round-42.md`, `round-43.md`, `round-44.md` and their `-verifier-spotcheck.md`
siblings; `corpus/QUALITY.md` Q30–Q38; `corpus/routed-findings.jsonl` (60 rows, measured by
`python3` json parse: `status` = closed 34 / open 23 / refused 2 / blocked 1; `opened_round` ∈ {39:5,
40:6, 42:49} — zero rows opened by rounds 43 or 44); `plans/round-45-claims.md` (frozen at
`b4fcd351`); `plans/round45_c1_verify.py` / `round45_c2_verify.py` docstrings. `corpus/defects.jsonl`
is 5 rows and ends at R34-D5 (`wc -l` → 5); the durable ledger is `routed-findings.jsonl`.

## 1. Routed findings that recur across the three lessons

| class | occurrences (evidence) | state |
|---|---|---|
| **fence-class** — a counter's fixture fence is narrower than the purpose the lane states for it | r43 lesson row 5: `R43SentinelCounter` F1 (`.git` FILE pointing outside), F2 (depth cap), F3 + `R43CritC1Counter` V2′ (absolute argv); r44: `R44SentinelFences` V1 `.git/commondir` (HIGH), V2 second-config include, V3 refuse-to-describe, `R44LabratLaneInclude` (`lane_breach` reads an include outside d *while refusing it*); r45 spotcheck §4 routed all four | **open**; this round's C1 is the discharge instrument (frozen `plans/round-45-claims.md:32-68`) |
| **predictor-memorization / readable-key** | r43 lesson row 4: V10's `DECISIVE` map readable in the counter → copycat filler passes (`R43CritClaims` §1); r44 lesson row "a content leg whose sample is memorizable": `R44CritV11` 4/7 lookup predictors pass the fixed-seed 48 states; `R44SentinelSandbox` F1 | **open**; r45 counter hardens V11 (`plans/round45_c2_verify.py:14-26`: ≤4000 B lint, count-only `disagree`, `random.Random(45)`), and names the next hole itself — an open-coded 48-bit truth table still passes the lint (`:25-26`) |
| **do-nothing controls** — work booked that standing instruments already demonstrate | r44 lesson: U3 priced into the mutant draft while battery43 already kills it → became Q37; r45 inheritance: attempt-1's C1 draft asked `plans/battery45` to re-kill the same five mutants battery44 already kills — DISCARDED (`round-45-claims.md:14-16`), caught at freeze review, never committed | **recurred at attempt-1, captured at freeze** |
| **seat-without-report-file** | r43 D3 (`R43ConnClaims`, `build/` has 37 files / 38 results); r44 (`R44ScoutMisroot`, no `.md` anywhere in the fleet tree) | **recurred twice** — see §3 item 4 |
| **flip-verdict falsity** | r43 `not fired` written from belief, not from reading the entry (task.toml/solve.sh); closed by Q36 (`QUALITY.md:941`) + extended `gate_flip_check.py`, red→green shown (`round-44-verifier-spotcheck.md:96-99`) | **closed as criterion** |
| **envelope/PATH-dir drift** | r42 D5 `local_bin_listing … CHANGED` names-only digest (`F42NoHarm` §3); fixed for r45: `claims/envelope.sh` now digests content (r43 R6) and exit-4 + `INVALID` on change is in every seat's rule block | **closed for content; mode-only blind spot remains open** (`R43ReviewEnvelope`: mode-only change and mode-000 rewrite missed) |
| **`--work` traceback** | r40 class; confirmed absent r42–r44 (counters create `--work`, print `receipt unreadable`) | **closed, did not recur** |

## 2. Which QUALITY criteria already cover them

- **Q31** (`QUALITY.md:573`) — non-vacuous predicate denominator: covers the *vacuous* half of do-nothing
  controls (predicate satisfiable without the work). Still mutant-shaped (`MUTANTS total=<n>`).
- **Q37** (`:985`) — standing-battery do-nothing control: covers a mutant the standing batteries already
  kill; shown able to fail by the six-mutant draft. This round's analogue is
  `claims/control-c1-fence-r44.txt` (the prior instrument as subject → `contradicted=7` = the
  already-done half) and `control-c1-fence-refuse_all.txt` / `static_only` (vacuous-refusal = the
  `refuse_all` analogue of `killed=0`). The *shape* is covered, but the *vocabulary* is mutant-shaped —
  see §4.
- **Q38** (`:1027`) — executed-key content leg: covers the readable-key half (V10). The *memorizable
  sample* half (R44CritV11) is named in Q38's own Limits (`:1048-1054`) as tunable to the generator;
  the r45 V11 hardening repairs it in the counter, not as a criterion.
- **Q35/Q36** (`:872`, `:941`) — flip-obligation existence + flip-verdict truth: the false-`not-fired`
  class is closed end-to-end.
- **Q30** (`:522`) — recurrence-twice → gate over committed history. Covers the *rule* for closing
  recurring classes; does not itself name fence, predictor, or report-file classes.
- **Q32** (`:626`) — sandbox/envelope for counter runs: covers the *environment* the fence runs in
  (the r45 counter traces the fence under `strace -f -y` inside read-only bwrap), not whether the
  fence's answer is complete.

## 3. What is still uncaptured

1. **Round-44's routed defects never entered the ledger.** `routed-findings.jsonl` has zero rows with
   `opened_round` 43 or 44 (json parse above), and `grep -niE 'commondir|SentinelFence|LaneInclude|
   CritV11|predictor|refuse-to-describe'` over the file returns nothing. The r44 spotcheck §4 routes
   four items (`R44SentinelFences` V1–V3, `R44LabratLaneInclude`, `R44CritV11`, flip-check keep) —
   they live only in the spotcheck §4 and the r45 freeze's inheritance paragraph. The durable-queue
   habit (r43 R3, burn-down `open=23` maintained by `R44RoutedObserve`) lapsed exactly when the
   routed items became the next claim's input. Q23/Q30 name no ledger-row requirement for *closure*
   routings once they become claims. Uncaptured: nothing mechanically asks "did every §4 routed item
   land in the ledger or in a freeze's work list".
2. **Fence-class has no criterion — it has a claim.** The class recurred r43→r44→r45 (three rounds),
   satisfying Q30's "recurs twice" gate condition, yet it is being closed by C1's instrument rather
   than a Q-criterion over committed history. That is a legitimate discharge path (the instrument
   *is* the gate: PINS + REFUSALS + HONEST + CALIBRATION literals), but QUALITY.md records no row
   naming it, so a future round could regress the fence without any history-reading check noticing.
   Same gap applies to **memorizable-sample V11**: the named limit ("open-coded 48-bit truth table
   still passes the lint", `round45_c2_verify.py:25-26`, `round-45-claims.md:97-98`) is written to
   recur — its third occurrence lands in a claims file again, not in a criterion.
3. **`READ` as a contradiction verdict is new and uncaptured anywhere else.** Rounds 40–44 counted
   LEAKED-style failures only (refuse-or-admit). The r45 counter's `READ`/`HUNG` verdicts — a fence
   that *refuses* while its own process tree opens or blocks on a path outside d (`strace -f -y`,
   `round45_c1_verify.py:30-40`) — catch `R44LabratLaneInclude`'s exact defect: refusal text correct,
   observation wrong. No prior counter or criterion binds a verdict to the subject's *own* opens.
4. **`seat-without-report-file` recurred twice and is still a prose rule.** Round-43 D3 + round-44
   recurrence = two occurrences → Q30 says a class that recurs twice closes by a gate over committed
   history, "never by a second prose rule". The r45 prompt carries the prose rule again ("Every seat
   MUST leave its report file"); `ls plans/report_file_check.py` → No such file. The r44 lesson's own
   fix (`report_file_check.py --reports … --results …` comparing lists) exists only as a quoted
   command in `round-44.md` §Mistakes. A counted history gate (`git ls-tree` report files vs
   results-JSON names) is the still-uncaptured form.
5. **`invalid_prompt` orchestrator-death (attempt-1 inheritance).** `.ufo/watchdog.log:1618`
   `lane-dead-no-report kengaku round=45`: attempt 1 died on an invalid_prompt policy refusal
   ~22:27–22:48, spawned nothing, committed nothing — but left *uncommitted* drafts. The r45 freeze's
   capture is claims-file text: REUSED (captures re-fetched `cmp`-identical, probe docstring
   repaired, counter digests filled, f7–f9 re-verified) vs DISCARDED (do-nothing C1 draft, C3 draft,
   empty battery45), moved to `.ufo/waves/round-45/attempt1-unclaimed/` (`round-45-claims.md:9-17`).
   This is a new failure surface: not a seat error, not a counter defect — an orchestrator kill
   leaving byte debt. Nothing in QUALITY.md or the routed ledger names it; the only capture is the
   freeze's prose split. Reusable capture for the mistakes table: *an attempt that dies invalid_prompt
   leaves uncommitted work that must be re-verified (digests, re-fetch) and explicitly split
   reuse/discard before the next attempt freezes anything on top of it.*
6. **`host-dependent` result rows** (R42-R3-37 `plan-host-dependent-cheat`, r43 `cheat-clock-seed`
   host=libc-rand) stay open in the ledger; r45's probe discloses the same shape (host python3 stands
   in for the image's uvx python, `round-45-claims.md:95-96`) — the disclosure convention exists, no
   criterion bounds when a host fact is acceptable vs must be re-derived in-image.

## 4. C1 shape: precedent or new class?

Rounds 40–44 share one shape — **mutant-kill counters**: pinned tools (subject pinned by sha256), a
frozen literal mutant table (`MUTANTS total=<n> killed=<n> survived=0 unattributed=0`), and a battery
authored during the wave whose kills must be attributed in a declared direction (`round40_c1_verify.py`,
`round41`, `round42`, `round43`, `round44` docstrings, all `BATTERY fixtures=<n>` + `MUTANTS` +
`PINS-AFTER` line sequences).

Round 45 changes the subject, not the instrument: the frozen counter evaluates an **unfrozen
subject-file** (`plans/fixture_fence.py`, authored this wave; the counter docstring says "Subject (not
pinned, it is the work)") against two fixed corpora — 10 hostile `plans/refusals45/` modules and 104
honest standing-battery fixtures — and counts *advertised-vs-observed contradictions*
(`CALIBRATION advertised=10 contradicted=0`). Elements are precedent: hostile battery modules (r43
`h1-h6` controls, r44 f1–f6 byte-copied), honest-vs-adversarial admission both-ways (the r44
witness-as-battery control; refuse_all/admit_all/static_only controls mirror no-battery/always-red
controls), strace observation (r42's `--ro-bind-data` tracing), advertised-behaviour counting
(`ADVERTISED direct=…` since r40). But the predicate grammar is new: `REFUSALS … clean|leaked|read|hung`
and `CALIBRATION … contradicted=0` replace `MUTANTS … survived=0`; Q27–Q37's vocabulary (mutant, kill,
direction, battery) does not literally bind this claim — the do-nothing control here is
`control-c1-fence-r44.txt`, which Q37 does not reach (no mutant list). **Verdict: a new class** —
"subject-as-file refusals contract" alongside "mutant-kill battery". Practical consequence for wave 2:
criterion citations Q27/Q29/Q31/Q33/Q37 need translation when applied to this counter, and the
admission basis rests on refusal-corpus review where the old shape rested on battery review.

## 5. Frontier-step note

The freeze already mines attempt-1's do-nothing draft as the prime mistake row; the two named
companions (probe docstring garble — repaired pre-freeze; the spec's extra row) fit the same class:
*draft artefacts that survive an orchestrator kill must be re-derived, not trusted*. Row for the
mistakes table: `attempt-1 invalid_prompt death → uncommitted drafts → split REUSED (digest/fetch
re-verified) / DISCARDED (do-nothing, unclaimed) → claims-file record`.

VERDICT: patterns-7-new-class-yes
