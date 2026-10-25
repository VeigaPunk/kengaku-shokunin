ATTACKS: the entry caveat at `corpus/knowledge/attribution-interval-calibration.md:85-88` — "request lines 37–160 for 20–30 trials" and "GT is a journal join".

1. BRACKET LOW END IS FALSE; true range 20–160. `grep -n '^# journal stdout' corpus/evidence/attrib-r2*.log` →
   impl-ds :132,:178,:224,:270 = `lines=40 request-lines=20 leg-rids=20`; impl-glm :144=99; legs :262=70,
   :314=37; opencode :206=68; r23 :196=152, :260=160. Ten blocks over six windows, seven distinct counter values: 20,37,68,70,99,152,160.
   Trial counts 20/20/20/20/22/20/20/20/30/30 → "20–30 trials" holds.
2. The stated lower bound 37 comes from the one block the calibration itself discards.
   `python3 plans/attrib_calibration.py --summary` (tip, all nine P1_SHA256 hashes verified first) →
   `unique_samples=4 … dup=[corpus/evidence/attrib-r22-legs.log:312-362=corpus/evidence/attrib-r22-opencode-trials.log:204-254]`.
   `:314` is that duplicate; the kept r22 sample is opencode `:206`=68. Verdict-bearing request-lines are **20, 99, 68, 160**.
3. "windows that also carried other traffic" is false for that minimum: impl-ds `:270` is 40 journal lines = 20 requests
   = 20 leg-rids for 20 trials, `allfail=0` — 1:1, no foreign traffic — and it carries PASS rows (accuracy 20/20,
   specificity 20/20, `--summary`). Contamination across the four unique samples spans 1.00×–5.33×, not 1.85×–5.33×.
   (That sample is join-invariant anyway: its 20 GT are all `alibaba-token-plan`, so no reassignment can move the label.)
4. QUALITATIVE claim survives: the join is not keyed on rid. `plans/attrib_probe.py:924-936` admits a candidate on
   `(bytes==body_len, stream==want_stream)` plus `epoch∈[t0-1,t0+3]` (fallback ±5 s) and takes greedy earliest-unused;
   the rid is an output, never an input. Journal stamps truncate to 1 s (`:850`), so a same-second foreign line earlier
   in journal order wins the tie.
5. Executable counterexample (`/tmp/k25w2-ScoutJournalCaveat/join_cx.py`, real records from impl-glm + the real scorer,
   fake `journalctl` on PATH — no network, no journal read): faithful synthetic journal → 22/22, GT {devin:9,zai:13},
   excluded=[] — reproduces `attrib-r21-impl-glm-trials.log:142-188` exactly, so the model is calibrated.
   One missing REQUEST line (T08): GT vector shifts; T10 flips devin→zai and scores NO, T14 becomes UNMATCHED, 20/22;
   T09/T11/T12/T13 also ride shifted rids but keep the same leg — 4 of 5 join errors invisible. 5/22 drops also change
   accuracy (UNMATCHED elsewhere + a relabelled survivor); the other 17 only exclude the dropped trial.
   A foreign same-bytes/stream line 0.25 s earlier steals the label on 9/20 trials (21/22) — exactly the nine
   devin-GT trials; the eleven zai-GT trials are stolen just as silently with no observable change.
6. That envelope is recorded, not hypothetical: `attrib-r23-stream.log:368-372` — 160 request-lines for 30 trials,
   "68 lines with the 269-byte stream-inspection body (this seat sent 24)", same bytes and same stream flag ⇒ 2.8×
   indistinguishable foreign requests inside the GT window.
7. WORSE THAN "invisible": the receipts show the matcher was re-fitted until 20/20. `attrib-r21-impl-ds-trials.log`
   holds FOUR blocks on the SAME window `@1792146059–@1792146169` with identical counters (40/20/20/0) and outcomes
   0/20 UNMATCHED (:130), 0/20 UNMATCHED (:176), 18/20 `AMBIGUOUS(2)` (:222), 20/20 (:268). `:314-330` names three
   post-trial matcher fixes ("window [t0-1.0,t0+3.0]", UTC-epoch, "greedy in-order 1:1"). The r21 blocks record no
   instrument sha, so `attrib_calibration.py` cannot see the matcher version — `mismatches=0`. The entry's "Any GT join
   error is invisible to the interval" omits that join error was visible in the receipt and retired by re-fitting.
8. Same surface, r23: `:3` pins instrument `cce53a1637…` but authoritative block `:262` was produced by `489f938a…`;
   block 1 (`:196`) was also read 12 s before `--until` (152 vs 160). Disclosed `:333-341` as verdict-path only;
   the calibration stores `instrument_sha256` but never flags a change.
9. GT is unverifiable, not merely error-prone: no r21–r23 receipt retains journal bytes (no `REQUEST model=` in the nine;
   only r19 probe logs have them) and `attrib_calibration.py` never reads a journal — it re-derives stored lines from
   the scored rows alone. So no future calibration run can refute a join error.

VERDICT: PARTIAL — the numeric bracket breaks (20–160; 37 is a dedup-dropped block) and the "invisible" limit hides a
recorded three-fix matcher fit to the same window, while "GT is a journal join" and its unverifiability survive.
Installs: none (python3 stdlib only).
