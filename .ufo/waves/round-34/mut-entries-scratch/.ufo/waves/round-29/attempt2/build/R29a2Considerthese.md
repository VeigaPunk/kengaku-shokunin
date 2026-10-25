# R29a2Considerthese — mining `considerthese/2026-10-21.md`

Role: leaf scout (kengaku round 29 attempt 2, hyaku run 6). Question asked: which single proposal in
`considerthese/2026-10-21.md` is still unimplemented and cheapest to ground this round, where it is named, and what
evidence the lane would need to open. **Findings only — nothing implemented, no production file touched.**

Measured at lane HEAD `8c14a5d` ("round-29: freeze attempt-2 claims, adoption gate, counter and control receipt",
`2026-10-25T03:39:15-03:00`); claims baseline `1f3b0f1` per `plans/round-29-attempt2-claims.md`.

## Verdict — proposal 3, the seat-yield ledger

**Named at `considerthese/2026-10-21.md:44`** (`3. **Seat-yield ledger and wave budget.**`), operative ask at
`:48-49`: "Proposal: append-only `.ufo/waves/yield.tsv` with one row per seat (role family, report path, whether it caused
a landed correction/supersede/verdict change, with the commit). Report yield per role family each round, and cut or merge
families that score zero for two rounds."

Chosen because it is the only fully-unimplemented proposal whose entire input set is already committed in-repo, is
offline, has no ordering constraint against the attempt-2 freeze, and needs no new gate code. Every column the proposal
asks for is derivable today from dispatch JSONs, report paths, `falsify-dead-seats.json`, and `git log -S` (§4–§5).
Confidence: high.

## 1. What the document offers (line map)

| # | Heading | Lines | Ask in one line |
|---|---|---|---|
| 1 | Push the grader-perturbation findings back into history | `:29-33` | frozen extractor-policy counterfactual listing every *historical* stored verdict (r12–r23) that flips |
| 2 | Prior-art preflight as a pre-registration gate | `:35-42` | required `## Prior-art preflight` block with dated PyPI/GitHub/arXiv log, committed **before** the freeze; plus a Q-row |
| 3 | Seat-yield ledger and wave budget | `:44-51` | append-only `.ufo/waves/yield.tsv`, one row per seat, yield per role family, cut/merge zero-yield families |
| 4 | Blind forecasters | `:53-59` | a seat seeing only claim text, probabilities hash-pinned **before** the build wave, scored at close |

Its own status block (`:9-21`) declares the predecessor suggestions partly/not delivered; the four above sit under
`## Self-improvement suggestions (proposals only; nothing acted on)` (`:23`).

## 2. Implementation status at HEAD (commands and observed output)

**#1 — partly implemented; residual real.** Landed in r27: `plans/parser_policy_compare.py` (commit `6356b0b`), a
five-policy comparison over the pinned population. But it emits only aggregate `flip_pf`/`flip_fp` tallies
(`plans/parser_policy_compare.py:192`, `:205`, `:294`, `:312-318`) and never writes a per-round list back into the
r12–r23 records. `considerthese/2026-10-22.md:15`: "What's still missing is a per-round list of *stored* historical
conclusions that flip, written back into those rounds' records." Not the pick: it is not wholly unimplemented.

**#2 — unimplemented.**
```
$ grep -c 'Prior-art preflight' plans/round-{24,25,26,27,28,29}-claims.md plans/round-29-attempt2-claims.md
→ 0 for all seven files
$ grep -nE 'Q[0-9]+' corpus/QUALITY.md   # last row
→ 179:- **Q18 — a forecast freezes its resolution criterion.**   (file is 182 lines; no Q19 preflight row)
```
Status text agrees: `considerthese/2026-10-22.md:16` "not done, and the pattern repeated"; `2026-10-24.md:13-14` lists it
still open. **Costly this attempt, not cheap:** (a) the instance must be committed *before* the freeze, and attempt-2
claims froze at `8c14a5d` (`2026-10-25T03:39:15-03:00`) with the build wave already live — inserting the block now is
exactly the "post-freeze preflight" the proposal calls a closure failure (`:41`); (b) the block needs live dated Pixy/
PyPI/GitHub/arXiv searches the lane's source discipline prices as opened primaries; (c) a Q-row means prose **plus**
enforced checking (the Q13–Q16 precedent is code: `plans/gate_timing_check.py`), i.e. a new checker + failure-capable
selftest.

**#3 — unimplemented at HEAD.**
```
$ test -e .ufo/waves/yield.tsv; echo $?
→ 1
$ git log --all --oneline -- .ufo/waves/yield.tsv | wc -l
→ 0
$ grep -rniE 'seat.?yield|yield\.tsv' plans/ corpus/ AGENTS.md SHONEN.md PROVINCE.md SCORECARD.md LOG.md | wc -l
→ 0
```
Status text: `2026-10-22.md:18` "not done. Waves got bigger, not smaller"; `2026-10-24.md:14` still open. **No blocker
applies:** `.ufo` is tracked except `.ufo/interactive-sessions/` and `__pycache__/` (`.gitignore:1-2`), so a new
`yield.tsv` is committable; nothing in `plans/` reads or forbids the path.

**#4 — unimplemented and ordering-blocked this attempt.**
```
$ grep -ciE 'predict|forecast|Brier' plans/round-29-attempt2-claims.md
→ 0
$ ls .ufo/waves/round-29/attempt2/build/
→ R29a2FixtureMutations.md R29a2RevQuoteS077.md R29a2RevQuoteS079.md R29a2SrcS077.md
  R29a2SrcS078.md R29a2SrcS079.md R29a2SrcS080.md swarm-registry.json
```
Attempt-2 carries no predictions/filed-probability section at all, and its build wave is already reporting (seven seat
reports on disk when this was measured, and growing; `build-spec.json` `items` = 36, `build-dispatch.json`
`counts.spawn` = 36). The proposal requires the
hash-pinned file *before* the build wave (`:56-57`); anything filed now is post-hoc and not blind. `corpus/QUALITY.md:179`
(Q18) already governs forecast resolution criteria, so the remaining work is the blindness/hash-pin mechanism — viable
next round, not groundable honestly in this one.

## 3. Cheapest-to-ground comparison

| Proposal | New bytes | Network | Freeze/ordering conflict | Gate code + selftest | Verdict |
|---|---|---|---|---|---|
| 1 residual | per-round flip table into r12–r23 records | no | no | no | more work than #3; also "mostly delivered" |
| 2 preflight | claims block + QUALITY Q19 | **yes** (PyPI/GitHub/arXiv) | **yes** — freeze at `8c14a5d` | **yes** (checker precedent) | most expensive |
| **3 seat-yield** | **one TSV** | **no** | **no** — history already landed | **no** | **cheapest** |
| 4 blind forecaster | predictions block + hash-pinned file + close scoring | no | **yes** — build wave live, no predictions section | no | blocked this attempt |

## 4. Minimal evidence the lane would need to open for #3

All paths verified present at HEAD; each is the ground for one ledger column.

1. **Seat roster (machine-readable, beats filename scraping)** — `.ufo/waves/round-25/build-dispatch.json` `counts`
   `{"spawn": 92, …}`, `.ufo/waves/round-25/falsify-dispatch.json` `{"spawn": 87, …}`,
   `.ufo/waves/round-26/build-dispatch.json` `{"spawn": 72, …}`, `.ufo/waves/round-26/falsify-dispatch.json`
   `{"spawn": 64, …}`. These exactly reproduce the document's own numbers at `:45` ("92 build seats plus 87 falsify
   seats") and `:46` ("64-seat falsify wave").
2. **Delivered-report inventory** — `.ufo/waves/round-25/build/*.md` = 92, `round-25/falsify/*.md` = 87 (total 179 =
   "~180 lane seats", `:48`); `.ufo/waves/round-26/build/*.md` = 72, `round-26/falsify/*.md` = 53.
3. **Dead seats** — `.ufo/waves/round-26/falsify-dead-seats.json`: 11 named seats, `"replaced": false`, shared
   provider error `turn_rate_limit_exceeded`. Arithmetic closes exactly: 64 spawn − 11 dead = 53 reports on disk.
4. **Wave-budget evidence for the dispatch half** — `.ufo/waves/round-26/build-dispatch-log.txt:2-5` records the three
   refusals verbatim: `attempt 1 ~03:41:27 -03: all 72 refused 'Background job limit reached (100)'`,
   `retry at 03:44:27 -03: refused=72`, `retry at 03:47:27 -03: refused=72`, `retry at 03:50:27 -03: refused=0`. This is
   the document's "three refused 72-seat dispatch attempts" (`:45`) confirmed from committed bytes.
5. **Landing commits for the `commit` column** — r25 `710409f`, `8ea41f9`, `8239a56`, `9d8a00d`; r26 `9b0567f`,
   `3a2aeb1`, `d4dfdb0`, `b571944` (`git log --oneline <range>`).
6. **Role families** — derivable from report stems; measured distribution: r26 `Fx*` families (Fx 11, FxMut 10,
   FxFamily 10, FxGate 7, FxEntry 6, FxSource 2, FxConn 2), plus Rev 3, Crit 4, Conn 5, Exec/ExecPerturb/ExecGateTiming;
   r25 Rev 24, Reopen 11, Tally 9, Lesson 8, Corr 7, Crit 6, Conn 4, Src 3, Sentinel 2.
7. **Precedent for a multi-round view** — five committed waves exist (`round-25`…`round-29`), so the "zero for two
   rounds" cut/merge rule (`:50`) can actually fire for the first time. Report counts per wave (build/falsify):
   r25 92/87, r26 72/53, r27 65/46, r28 59/64, r29 41/77. `round-29/attempt2` = 36 spawned so far.
8. **Note for whoever builds it:** r28's recursive `*.md` count is 3456 because `.ufo/waves/round-28/scratch/` is
   committed; the ledger must read dispatch JSONs plus the `build/`/`falsify/` subdirs, never `find … -name '*.md'`.

## 5. The yield column is mechanically derivable (measured, not assumed)

The proposal's hardest column is "whether it caused a landed correction/supersede/verdict change, with the commit".
Committed bytes already carry that signal: 14 tracked files cite r25/r26 report paths
(`corpus/evidence/round25-sources/gate.md`, `round26-sources/gate.md`, `corpus/knowledge/attribution-interval-calibration.md`,
`corpus/knowledge/grader-perturbation-audit.md`, `corpus/lessons/round-25.md`, `round-26.md`, `corpus/QUALITY.md`,
`corpus/SOURCES.md`, …). `git log -S` on a cited report path resolves the landing commit — verified:

```
$ git log --oneline -S"waves/round-26/falsify/FxSourceCheckList.md" -- corpus/lessons/round-26.md corpus/evidence
→ b571944 round-26: record actual admission checks and final measurements
→ d4dfdb0 round-26: admit reviewed grader audit and frozen self-assertion repairs
```

First-pass yield numbers from that rule (unique reports cited in tracked bytes ÷ reports present): **r25 1/179**,
**r26 11/125**. That is the measurement the proposal exists to expose — the r25 outside reject came from the integrator,
not from any of ~180 seats (`:47-48`) — and it is reproducible offline with `grep` + `git log -S`.

## 6. Remaining unknowns (not resolved here)

1. Citation is a **proxy for yield, not proof of causation**: a seat whose report is never cited may still have moved a
   verdict through a relaying seat. I did not trace relay chains.
2. The `commit` column is well-defined only for rounds whose landings already cite reports; for a **live** round the
   column must stay empty until close, so ledger v1 is honestly a backfill of r25–r29 plus append-at-close thereafter.
3. I verified dispatch/report arithmetic for r25 and r26 only; r27–r29 counts were taken as directory counts, not
   reconciled against their own dispatch JSONs.
4. No LSP server was available for this repo (text search only); the findings above are file/line and command-output
   evidence, so no semantic-proof claim is implied.
5. Nothing here judges the proposal's value or whether the L1 should adopt it — only its status, cost, and groundability.

## 7. Bounds and tooling

- No production edit: the only bytes written are this report. All reads read-only; no commit, fetch, push, or write into
  any sibling lane; no campaign tool invoked.
- No `task` dispatch (leaf), no background jobs, no `ask` call, no pacman transaction.
- No tool installed or upgraded: the whole investigation used the existing `git`, `grep`, `find`, `python3` — so there is
  no tool/version/channel entry to record.
