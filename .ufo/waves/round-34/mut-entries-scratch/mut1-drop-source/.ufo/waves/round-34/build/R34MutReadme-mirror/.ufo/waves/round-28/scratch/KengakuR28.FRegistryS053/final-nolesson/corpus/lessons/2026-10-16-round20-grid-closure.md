# Round 20 — a battery with unrun probes is an open battery: what closing the grid bought

2026-10-16. Round 20 was one axis-move (calibration): complete the r19 battery
(`plans/probe-battery-r19.md`, FROZEN 2026-10-16T07:55:58Z sha256 `e1a86777…`)
by executing its four UNRUN probes — P2/P3/P8/P9 — against the SAME prediction
set, then recompute the aggregate over all executed binaries. Receipts:
`corpus/evidence/probe-r19-{P2-servicetier,P3,P8-kimi-code-auth,P9-absent-port}.log`
(first requests 09:14:49–09:18:22Z, 9 HTTP requests, every one inside the
enumerated per-probe sets); scorer's extension `corpus/knowledge/probe-battery-r19.md`
§10 (grid 9/9, mean Brier 0.1495/20); template hardening
`plans/probe-battery-TEMPLATE.md` (§5 step 3 freeze-after-last-edit guard +
decoy scan, §7 rule 1 completion gate, lineage row 18). The freeze-chain
lessons are in `2026-10-16-round19-freeze-chain.md`; this note records what
the completion itself taught. Every number below was reproduced by this seat
from the §2/§10.2 component tables before citing it.

1. **The partial aggregate was not a smaller version of the true one — it was
   a different number, and the difference was selection, not sampling.** Runner
   seats self-picked the quota/transport probes (P1, P4–P7); the codex
   `service_tier` set and the two zero-cost auth/freshness probes stayed unrun
   (knowledge §8.3 names the skew). So r19's 0.1836/11 and its "mild
   overconfidence" read (predicted mean 0.8627 vs observed 0.8182, §4 iii)
   described the subset that happened to get seats. Completion moved the read:
   **0.1495/20** (completion wave alone 0.1078/9), overall predicted 0.8645 vs
   observed 0.8500 — near-flat — the 0.8–0.9 reliability band went 2/2 → 7/7,
   and the ≥0.9 band held 0.750 while its n grew 8 → 12 (§10.4; this seat
   recomputed 2.0197/11, 0.9700/9, 2.9897/20, miss-mass 2.4849/2.9897 = 83.1%).
   Rule: an aggregate over an open grid is a moving number. State
   `executed/total` beside it, and draw no reliability conclusion until every
   probe is executed or NOT-RUN-reasoned. (The lane's own honesty made the
   hazard visible: the r19 close never presented 0.1836 as final — §0 said
   "all executed: NO", §8.3 carried the coverage limit. The failure mode this
   guards is the quiet version, where the partial number just gets quoted.)

2. **Completion is legal only against the SAME freeze; a frozen-unrun probe is
   a claim on future evidence, and closing the grid must not re-open the
   predictions.** All four receipts carry `battery_sha256_at_start ==
   e1a86777…` verified before each seat's first request (09:14:36–09:19:25Z,
   §10.1); the scorer re-verified the freeze byte-unmodified before scoring
   (battery mtime 08:06:37Z — before any completion request); and this seat's
   independent recompute reproduces
   `e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1` exactly
   (`sed -n '1,/FROZEN-PREDICTIONS-ANCHO[R]/p' plans/probe-battery-r19.md |
   sha256sum`). No re-freeze, no prediction edits: the ~1.3-hour-old frozen
   predictions absorbed four new outcome sets intact, and §0's rule (no outcome
   precedes its prediction) survived a cross-wave hand-off. Corollary on
   budgets: P2's 7 enumerated POSTs exceed the wave's generic
   ≤2-requests-per-probe rule, and the receipt discloses the supersession
   (`probe-r19-P2-servicetier.log:10`) — a pre-registered set governs its own
   budget; the battery §2 rule 5 (never widen the enumerated set) is what kept
   that honest, not the generic cap. The inverse case stays prohibited: a
   "completion" that edits predictions first is a new battery, not a closure.

3. **Price does not dispatch: the cheapest probe was among the unrun, and its
   freshness value waited for a second wave.** P9 — one zero-quota localhost
   GET — sat UNRUN through r19 while costlier probes ran (knowledge §5 finding
   7, §8.3); r20 realized the value in 3 ms (curl exit 7, http 000 — absence
   re-confirmed same-day and corroborated by zero-traffic reads: `ss -ltn`
   count 0, no llama-server process; `probe-r19-P9-absent-port.log`). An
   absence re-confirmation is a real scored outcome (9a HIT, Brier 0.0400),
   not a null result. Named-UNRUN is what made r20 a work list instead of a
   discovery project: the r19 close listed all nine unrun rows with reasons
   (§2 UNRUN block) and flagged P9 by name (§5 finding 7), so the completion
   seats executed exactly that list. The template's new completion gate
   (TEMPLATE:261) makes the ordering mechanical for every future instantiation:
   run unrun probes cheapest-first in-round while budget and freeze allow →
   else carry them named against the SAME freeze → else record NOT-RUN with
   reason and destination; the closing note must state the grid.

4. **The only new falsification is a design lesson: never freeze an
   absolute-level threshold that a meter is guaranteed to move.** 3c predicted
   `x-codex-primary-used-percent` ≤ 2 (p=0.90) off r18's same-day read of 1;
   observed **7/7/7** — the weekly plan window had consumed 7% between rounds
   (window 10080 min, reset-at 1792649629 = 2026-10-22T06:13:49Z), not a tier
   effect: the inertness claim itself held exactly (7/7/7 static across the
   three serviced legs, countdown fields moving per response
   507327/507323/507318; `probe-r19-P3.log` [3c]). Across both waves the
   battery's binary/vector/range idiom absorbed every other kind of drift it
   met — status vectors (2a exact), echo sequences (3a), token counts (4f
   exact), refusals (P8), absences (P9) — absolute levels are the one shape
   that cannot cross a meter boundary. Next instantiation: pin levels per-run
   or predict deltas (scorer §10.5 finding 5). The frozen row stays as frozen —
   recorded, never patched; the miss costs 0.8100 and sits in the aggregate,
   which is the instrument pricing its own design honestly.

5. **Two waves, one battery: per-round provenance is what lets a grid close
   without laundering the rounds together.** The closing note scores all 20
   binaries against one prediction set while keeping the receipt rounds split
   (P1/P4/P5/P6/P7 executed in r19, 07:52–08:04Z; P2/P3/P8/P9 in r20,
   09:14:49–09:19:25Z; §10.4 iv) and leaves the r19-close record standing
   unedited as the honest partial (§ preamble: "§1–§9 stand unedited"). The
   completed grid is 7 PASS / 2 FAIL / 0 UNRUN — the first time the lane's
   calibration proxy closes a multi-probe battery with every probe executed
   (proxy history r8–r11: 0/1, 1/1, 0/0, 1/1, `SCORECARD.md:33-37`; the r12
   breach scored two rounds late; r19 closed 5/9). The parent's r20 proxy row
   is ready in §10.6: 9 executed / 9 scored, all against pre-registered
   predictions.

Named leftovers for the parent (recorded, not patched from this seat):

- TEMPLATE lineage row 17 (`plans/probe-battery-TEMPLATE.md:17`) says
  "(15 receipts; P2/P3/P8/P9 named UNRUN at close)" — accurate for the r19 row
  it annotates, but ambiguous after completion: the r19 evidence inventory is
  19 files and the probes are no longer UNRUN at *the* close. A lineage row for
  the completion event itself ("UNRUN probes completed against the same freeze |
  r20 | knowledge §10, receipts 09:14–09:19Z") would make the table
  self-describing. Owner: next template pass.
- No other new defects found: the completion receipts are gate-clean (all four
  hash-verified pre-request, §10.1), P9's in-flight pgrep self-match is
  disclosed and contained in-receipt, and the scorer's §10 arithmetic
  reproduces from the tables (this seat's recompute).
