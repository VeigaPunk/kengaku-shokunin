# bench-arena round-9 — pre-registered replication of probe A + checkpoint-dose cell

**Source basis:** `corpus/evidence/round9-replication/{predictions-r9.md,predictions-r9.sha256,predictions-r9.sha256.repo,ordering.log,run_r9.py,replicate.py,results-r9.jsonl,replication.md}`.
Same endpoint/model/settings as round 8 (`127.0.0.1:34113`,
Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS, pinned system prompt, temp 0.2,
max_tokens 8192, no tools, strictly sequential). Run: 284 records = 8 `meta`
+ 248 scored + 28 `filler`, **0 error records**.

This is the lane's first probe since round 6 with predictions filed *before*
the first request, and the first with a mechanical ordering proof. Round 8
filed none (`test -e /tmp/bench-r8/predictions.md` → MISSING;
`grep -ril predict` over both r8 probe dirs → 0 hits) even though
`SKILL.md`'s production checklist item 1 and anti-pattern 4 require it — the
regression this round exists to repair.

## Registration and ordering proof

| Step | Evidence | Value |
|---|---|---|
| predictions written | `predictions-r9.md` (12 lines, per-cell counts + a falsifier per cell) | – |
| content hash before any request | `predictions-r9.sha256` | `2a4f62ef20a65e7a7cb3b7414b54d0f995126209c3126ae674b7cc3af2bc1099` |
| hash timestamps | `ordering.log` (before/after `sha256sum`) | `2026-09-28T21:17:48Z` / `2026-09-28T21:17:48Z` |
| first endpoint request | first non-`meta` record's `request_ts` in `results-r9.jsonl` (`A-INC`, pid 101) | `2026-09-28T21:17:58Z` |
| committed copy identical to hashed original | `cmp corpus/evidence/round9-replication/predictions-r9.md /tmp/kengaku-r9/predictions-r9.md` → clean; `sha256sum predictions-r9.md` re-run in-repo → `predictions-r9.sha256.repo` | same `2a4f62ef…` |

Re-verify at any time without `/tmp`:
`cd corpus/evidence/round9-replication && sha256sum -c predictions-r9.sha256.repo`.

## Design deltas vs round 8

- **Fresh problems**: pids 101–108, seeds `2000 + pid*29` (r8 used
  `700 + pid*13`, pids 1–10) → disjoint seed bases; generator and its
  rejection resample unchanged.
- **New dose cell**: `A-CKPT710` (acks except turns 7,10) alongside r8's
  `A-CKPT4710` (acks except 4,7,10) → a 3-point emission-granularity ladder
  INC ⊃ CKPT4710 ⊃ CKPT710 ⊃ MONO.
- **Burst decorrelation**: 28 filler requests (`cell:"filler"`, "Reply with
  the single word: ready.") between consecutive same-cell draws across pids —
  critic defect #14's unpaid half. Cells still interleaved per pid.

## Observed

| Cell | Final (turn 10) exact /8 | Mean final `nwrong` | Graded records |
|---|---|---|---|
| `A-INC` | **4/8** | 0.500 | 80 |
| `A-CKPT4710` | **2/8** | 0.875 | 24 |
| `A-CKPT710` | **2/8** | 1.375 | 16 |
| `A-MONO` | **0/8** | 2.250 | 8 |

Failure classes at the final graded turn: parse failures **0/32**, MONO parse
failures **0/8**, `finish=length` **0/32** and **0/8**, state errors 12/32
(+8/8 MONO). All finals `finish=stop`.

Paired exact sign tests (problem = unit, ties dropped, `2·min(P[X≤w],P[X≥w])`
via `math.comb`):

| Pair | wins | losses | ties | p |
|---|---|---|---|---|
| INC vs CKPT4710 | 2 | 0 | 6 | 0.500 |
| CKPT4710 vs CKPT710 | 0 | 0 | 8 | 1.000 (no direction) |
| CKPT710 vs MONO | 2 | 0 | 6 | 0.500 |
| INC vs MONO | 4 | 0 | 4 | **0.125** |

INC first-error turns (pids 101→108): `None, 2, 7, 7, 3, 10, None, None` →
mean onset **5.8** over the 5 imperfect trajectories (undefined over all 8;
perfect trajectories have no onset).

**Ack compliance degraded vs r8** (leak = an ack turn emitting a state instead
of `ok`): `A-CKPT4710` 32/56 compliant (24 leaks, **16 beyond turn 1**, all 8
pids affected); `A-CKPT710` 48/64 (16 leaks, **8 beyond turn 1**, all 8 pids).
r8 by contrast had 10 leaks and *all* were the harness-demanded turn-1 state
(0 beyond turn 1). Consequence: the r9 checkpoint cells carried **more**
self-copy scaffold than r8's and still scored 2/8 → the scaffold-assist
reading is conservative, and "checkpoint" is not a clean latent-maintenance
arm on this model. Any future dose-response claim needs a compliance filter
per pid, not per cell.

## Prediction scoring

Point counts were pre-registered, so the score is `|predicted − observed|/8`
(explicitly not a probabilistic Brier score):

| Cell | Predicted | Observed | Hit | Abs error |
|---|---|---|---|---|
| `A-INC` | 6/8 | 4/8 | miss | 0.250 |
| `A-CKPT4710` | 2/8 | 2/8 | **hit** | 0.000 |
| `A-CKPT710` | 1/8 | 2/8 | miss | 0.125 |
| `A-MONO` | 0/8 | 0/8 | **hit** | 0.000 |
| INC mean onset | 5.0 | 5.8 | – | 0.8 turns |

Cell hits **2/4**; mean absolute error **0.094** of n. Both misses are
over-confident in the *direction the lane wanted*: INC was over-predicted by
2 problems, the sparser checkpoint cell under-predicted by 1.

**Directional falsifiers (4, written in `predictions-r9.md` before the run) —
none fired:**

| Falsifier | Observed | Fired? |
|---|---|---|
| "if `A-INC` is not higher than both checkpoint cells, the scaffold-assist claim is dead" | 4 > 2, 2 | no |
| "if `A-CKPT4710` is no better than `A-MONO`, the scaffold-assist claim is dead" | 2 > 0 | no |
| "if `A-CKPT710` exceeds `A-CKPT4710`, the scaffold-dose claim is dead" | 2 = 2 (tie, not exceed) | no |
| "if `A-MONO` reaches or exceeds `A-INC`, the scaffold-assist claim is dead" | 0 < 4 | no |

**Critic's independent pre-registered decision rule**
(`corpus/evidence/round9-fleet/critic.md` §4.1, written before the replication
landed): *blocks* claim (i) if CKPT4710 or CKPT710 ≥5/8 with MONO ≤2/8;
*survives replication* if CKPT ≤2/8 **and** INC ≥5/8. Observed: CKPT legs at
2/8 (≤2 ✓), MONO 0/8 (≤2 ✓), **INC 4/8 (< 5 ✗)** → **neither branch fires:
indeterminate.** Secondary pre-registered check — a CKPT710 < CKPT4710
gradient implying forced-maintenance length matters — also fails on pass rate
(2/8 = 2/8) and appears only in severity (mean `nwrong` 0.875 → 1.375).

## Round 8 vs round 9

| Cell | r8 (pids 1–10) | r9 (pids 101–108) |
|---|---|---|
| `A-INC` | 7/10 | 4/8 |
| `A-CKPT(4,7,10)` | 1/10 | 2/8 |
| `A-CKPT710` | not run | 2/8 |
| `A-MONO` | 0/10 | 0/8 |

**Ordering replicates, magnitude does not.** MONO failure is exact in both
(0/10, 0/8); INC stays above both checkpoint cells in both; but r8's
`7/10 vs 1/10` gap (Δ=6 problems) shrinks to `4/8 vs 2/8` (Δ=2), and the
`CKPT ≈ MONO` identity that carried r8's headline becomes `2/8 vs 0/8`. No
paired contrast reaches α=0.05 even before ESS discounting (best p=0.125,
n=8, ESS≈4.3 at r7's ρ≈0.3).

## What this licenses

- **Licensed:** on this endpoint and quantization, emitting the full state
  every turn beats emitting it sparsely or never, in both seed batches
  (7/10 > 1/10 ≈ 0/10; 4/8 > 2/8 = 2/8 > 0/8); monolithic 10-op chaining
  failed 0/18 problems across both rounds with no truncation involved.
- **Not licensed:** a *magnitude* for the scaffold effect (r8's Δ=6 did not
  survive fresh seeds); a checkpoint *dose-response* (pass rates tie, only
  severity moves); any inferential claim at n=8 with burst-adjacent draws;
  claim (i) as "replicated" — the pre-registered rule returned indeterminate
  because INC landed one problem below its own threshold.
- **Methodological carry-forward:** the ordering proof (hash + timestamps +
  first-request `request_ts`) costs two commands and makes the
  predict→observe→score loop auditable; ack compliance must be measured per
  pid before any checkpoint cell is used as a latent-maintenance control.
