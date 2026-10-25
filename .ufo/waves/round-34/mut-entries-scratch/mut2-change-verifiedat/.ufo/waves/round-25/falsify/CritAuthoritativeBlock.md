ATTACKS: P1 last-block rule discards `attrib-r22-legs.log:260-310` run-1 — its own addendum (:378) declares BOTH blocks authoritative — suppressing a real UNTESTED->INDETERMINATE migration and a pooled hyper-recall PASS.

FINDINGS
1. Authority mismatch (premise falsified). P1's last-block rule (claims:29-30) cites
   `attrib-r21-impl-ds-trials.log:316` "AUTHORITATIVE SCORING SECTION: the LAST block above" — which exists
   because its earlier blocks are "the debugging trail of three instrument defects" (:317-318).
   `attrib-r22-legs.log` instead says (:378-379): "both score blocks above are this seat's authoritative
   adjudication". Amendment 1 item 5 explicitly rules `attrib-r22-legs.log:260` "non-authoritative and
   never re-verdicted" — a deliberate but premise-wrong choice: it applies a defect-supersession rule to a
   file whose seat declared two distinct scored executions (run-1 freeze-2 pin 3d7861f8 vs run-2 freeze-3
   pin 77b8d4a0; :366-369). Neither is a debugging artifact.
2. Evidence discarded, GT population falsified. `grep '| opencode-go | opencode-go' corpus/evidence/
   attrib-r2[123]-*.log` → ONE row in the whole P1: legs.log:270 (run-1 T03, GT opencode-go, correct).
   Under the frozen rule `recall:opencode-go` re-verdicts UNTESTED (summary:28) and the knowledge entry
   (:33-35) asserts "5 UNTESTED (0 GT trials)" — for opencode-go this is false: a scored GT trial exists
   and was suppressed. Amendment 5 defends `0/0 FAIL -> UNTESTED` as honest label migration; this is the
   inverse corruption — `1/1 observed -> UNTESTED` hides evidence and weakens the entry's own falsifier
   hook (any NO on an opencode-go trial).
3. Pooled PASS manufactured into INDETERMINATE. Hyper recall pooled run-1+run-2 = 19/19:
   CP95 lo = 0.025^(1/19) = 0.823533 >= 0.80 -> PASS. Taken separately, 9/9 and 10/10 are both
   INDETERMINATE (need_n=17). The last-block rule discards exactly the trials that would PASS hyper
   recall; "never re-verdicted" is not "conservative" — it silently suppresses a PASS (claims only
   promised counting identical tables once :31-32; run-1's table DIFFERS from run-2's, so the dedup
   clause cannot cover it — only Amendment 5's fiat does).
4. Understated population totals + truncated sensitivity line. TOTAL reports scored_trials=92,
   unique_samples=4 (summary:49). Under the receipt's own both-authoritative adjudication it would be
   unique_samples=5, scored_trials=112. The `pooled-if-distinct 40/40` sensitivity line (summary:24)
   pools run-2 + opencode-trials only; the fullest evidence read is 60/60 (CP95 lo 0.940371) — the
   printed sensitivity omits a third of the available trials.
5. What survives. No stored PASS re-verdict flips to FAIL; every flip is conservative
   (PASS>INDETERMINATE, FAIL>UNTESTED), so the claim's novelty rubric legs (new construct, in-repo
   instrument, prior-art verdicts) are not overturned by this defect. Amendment 4's "conservative
   direction" defense covers identical-table dedup, NOT distinct-block suppression.

SMALLEST SAFE CORRECTION: in the instrument, honor a receipt's explicit multi-block adjudication
(`attrib-r22-legs.log:378`) over the last-block default: take each `## GT + scoring at close` block as a
sample unless the receipt's adjudication names it superseded (r21 defect-trail form). Effects:
unique_samples 4->5, scored_trials 92->112, recall:opencode-go UNTESTED->INDETERMINATE 1/1,
knowledge entry UNTESTED count 5->4 and its falsifier hook covers the real opencode-go trial.
Per-block (unpooled) keeps hyper INDETERMINATE; whether the two runs of one file pool is a second-order
question needing its own frozen rule — flag, don't decide.

VERDICT: PARTIAL — frozen rule misadjudicates authority in exactly this file: a scored GT trial and 20
scored trials are erased from the population and a pooled PASS is suppressed; verdicts bend only
conservatively so the claim stands, but the report's GT census and UNTESTED labels are factually wrong.
Installs: none (python3 stdlib math for CP bounds; grep; no packages needed).
