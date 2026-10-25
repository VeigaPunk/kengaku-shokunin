# R25 CritNoveltyLegit — is offline re-analysis of receipts a novelty "+1 probe"?

Read-only leaf. Base `6180e4f`; claims at `plans/round-25-claims.md` (landed `3f371d2`). Rubric: `SCORECARD.md:244` — novelty +1 needs (a) a probe measuring a construct the lane could not previously observe, (b) instrument inspectable in-repo, (c) prior-art verdict with fetched URL. Caps: re-runs of known-shot batteries; already-published phenomena; constructs measured below the critic's pre-registered power ask.

## F1 — the literal "before" statement is false (fixable defect, calibration not novelty)

`plans/round-25-claims.md:59` asserts "0 interval estimates / 0 interval verdicts exist for the instrument" and the sweep at `:60` greps only `corpus/evidence/attrib-* plans/attrib*`. But `corpus/knowledge/attrib-r21.md:139` carries Wilson 95% `[0.839,1.000]` on ds 20/20, `:154` Wilson `[0.851,1.000]` on glm 22/22, `:156` pooled `[0.916,1.000]`, `:374` repeats both, and `:549,551,557,561` add r23 Wilson CIs — descriptive intervals on this instrument's accuracy the lane already produced. The claim survives only in the narrowed reading NoveltySweepScout.md:27,42 gives: 0 *exact CP* intervals, 0 *per-leg* intervals, 0 *interval-driven verdicts*, 0 *in-repo instrument*. Writing "0 interval estimates" where the lane's own note holds five is the same provenance falsity the round is built to catch (SCORECARD.md:245 leg (e)); C1's own instrument re-verdicting stored lines while its before-statement overclaims would be self-refuting.

## F2 — leg (a) is met under the narrowed reading; the re-run cap is the live attack

All 9 receipts and `plans/attrib_probe.py` are interval-free (grep `Wilson|Clopper|interval|binom|betai` over `plans/attrib_probe.py` → 0 hits; receipts carry only `ACCURACY k/n -> PASS/FAIL` lines, e.g. `attrib-r22-legs.log:290`, `:344`; `attrib-r22-opencode-trials.log:234`; `attrib-r23-stream.log:234,298`; `attrib-r21-impl-ds-trials.log:297`; `attrib-r21-impl-glm-trials.log:173`). No re-verdicts, no per-leg CIs, no Rogan–Gladen bound, no dedup count exist anywhere. So the composite construct — exact-CP interval verdicts, per-leg recall/specificity intervals, RG leg-share bound, re-verdicted stored lines — is genuinely unobserved, which is what the round-13→14 precedent (`SCORECARD.md:271-274`) counted. Counter-reading that fails: "re-verdicting old receipts is a re-run of a known-shot battery" — the data are fixed but the measured quantity (interval verdicts, not point fractions) was never observable before, so the construct, not the battery, is new. This leg holds *only* if the row claims the narrowed construct.

## F3 — leg (b) holds; offline + receipt-only is not a defect

`grader.py:879 _betacf`, `:915 betai`, `:945 _binom_cdf_le` exist already, so the instrument is implementable stdlib-only and inspectable (`plans/attrib_calibration.py` lands in-repo, not /tmp — operability cap at `SCORECARD.md:248` satisfied). The rubric's prior novelty +1 (r14, `SCORECARD.md:271`) and the round-24 census round are offline; "could not previously observe" never required live traffic. A probe that measures a static artifact (the receipts) measures the construct fine — the receipts are committed, hash-pinned (`frozen table re-verified at scoring: sha256 …` per block), and blind-ordered (`attrib-r21.md:120-123`).

## F4 — leg (c): the phenomenon is already published in-corpus; the verdict must scope or the row caps

`corpus/SOURCES.md:33` (S011, lee26bl) already registers "plug-in correction of judge sensitivity/specificity bias with CIs" and `:41` (S019) registers CIs "for model accuracy … with valid frequentist coverage". CP/Wilson/Rogan–Gladen are textbook (scribes opening them this round). If the SCORECARD row narrates "interval-calibrated classifier accuracy" as the novel phenomenon, `SCORECARD.md:244` cap "a phenomenon already published" fires and the row must record *replication, not contribution*. The defensible framing: the construct is the *lane-local datum* (this instrument's interval verdicts on P1, a fixed receipt set nobody else has) — method replicated from S011-style bias accounting, construct new because the instrument and receipts are lane-internal.

## F5 — power ask: met on overall accuracy, not on most legs (note, not defect)

Per-block n: authoritative blocks are `r22-legs` run-2 n=20 (`:341-342`), `r22-opencode` n=20 (`:234`), `r23-stream` 2×n=30 dedup→1 (`:234`,`:298`), `r21-impl-ds` n=20 (`:297`), `r21-impl-glm` n=22 (`:173`) — all ≥17, CP-lo for k=n ≥ 0.8316 > 0.80 → interval PASS re-derives each stored PASS, so the construct *is* measured at power on the headline construct. Legs below 17 re-verdict INDETERMINATE (`TARGET hyper n=9 → FAIL` at `r22-legs:292` and `n=10 → PASS` at `:344`/`r22-opencode:236` must flip INDETERMINATE; zai n=13, devin n=9 legs same). `n=0` stored `-> FAIL` lines (`r22-legs:293`, `r23-stream:239`) re-verdict UNTESTED, not FAIL — the stored verdicts encode a min-n refuse-to-score rule, not a measurement. Edge: the four non-authoritative logs (`r23-stream-trials` has a `§D Verdict` block at `:179-180` but no `## GT + scoring at close`) contribute 0 scored rows per claims:30-31 — the instrument must still name their stored verdicts as out-of-population, or "every stored point verdict re-verdicted" (`plans/round-25-claims.md:26`) is unmet.

## F6 — registered-claim stricter than rubric (observation)

`:66` makes "the power ask is met" a +1 gate; `SCORECARD.md:244` only *caps below 10* for under-power constructs — a 7→8 under-power +1 is rubric-legal. The claim self-registers the tighter rule, and the wave rule permits tightening only, so it stands — but the row's honest `improved`-vs-`+1` verdict then hinges on it.

## Smallest safe correction

In `plans/round-25-claims.md:59` (or the SCORECARD row built from it) replace "0 interval estimates" with "0 exact-CP / per-leg / verdict-carrying intervals; 3 descriptive Wilson CIs exist at `corpus/knowledge/attrib-r21.md:139,154,156`", and state in the row's prior-art verdict: "method = published (S011/S019/CP/Rogan–Gladen); construct = new lane datum on frozen P1". One-sentence each; no other change needed — every other rubric leg survives.

## Falsifiable condition

`grep -nE 'Wilson|Clopper|confidence interval' corpus/knowledge/attrib-*.md` returning ≥1 hit (it returns 8) falsifies any row text claiming "0 interval estimates existed" — run it against the landed row; zero hits on `corpus/knowledge/` is the condition under which the broader wording would have been legitimate.

## Installs

None.

VERDICT: +1 is legitimate IF the row claims the narrowed construct (exact/per-leg/verdict-carrying intervals on frozen P1) with prior-art scoped to method-not-datum; as literally drafted (`:59` "0 interval estimates") the before-statement is falsified by `corpus/knowledge/attrib-r21.md:139-156` — fix the wording, do not drop the claim.
