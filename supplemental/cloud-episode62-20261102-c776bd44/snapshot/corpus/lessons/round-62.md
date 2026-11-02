# Round 62 — repeated-trial estimands, with execution limits preserved

author: kengaku-shokunin-round62. Base c55a3f8868f352280538cf7d786135d34ac6542f.
Proposal8eeeb5301b885204d89a273c06dcb5121456d4f4; manual answer freeze
21d46b6c94cc4e0540e1b64a4c34219dcc35c7b7. No self-admission.

## Gate

All sources below opened 2026-11-02 and captured under
`corpus/evidence/round62/sources/`. Source rows queued pending independent review.

| row | URL and located quote (≤25 words) | decision and boundary |
|---|---|---|
| S226 | https://raw.githubusercontent.com/openai/human-eval/b9453e8f1865df0a0057a1383767caa400acfbcf/human_eval/evaluation.py line24: “Calculates 1 - comb(n - c, k) / comb(n, k).” | candidate tierA code; helper's estimator distinct from caller guard89–90; READ, not executed |
| S227 | https://raw.githubusercontent.com/sierra-research/tau-bench/59a200c6d575d595120f1cb70fea53cef0632f6b/tau_bench/run.py line198: “sum_task_pass_hat_k += comb(c, k) / comb(num_trials, k)” | candidate tierA code; global unique-trial denominator at184 and exception reward0 at92 matter; no benchmark/model run |
| S228 | https://arxiv.org/html/2406.12045v1 section3 Pass^k metric, S3.p7.1: “averaged across tasks” | candidate tierA original definitions; nearby equation S3.Ex1 defines both formulas and text states iid trials; paper's own model experiments not independently replicated |
| S229 | https://arxiv.org/html/2107.03374v2 Appendix A Figure13 caption: “underestimates the true value by a considerable margin” | candidate tierA canonical estimator/plug-in distinction, not novel theory/current capability finding |
| S230 | https://encoding.spec.whatwg.org/index-windows-1252.txt line105: “(LATIN SMALL LETTER A WITH CIRCUMFLEX)” | candidate tierA index; pointer98 maps byte0xE2; immutable S225 preserved, corrected by successor row |

Candidate admit: `plans/round62-knowledge-draft.md` (writer named in its header),
a sourced distinction between finite-panel proportions, iid estimation,
fixed-task aggregation and missing-outcome bounds. Independent reviewer
`/root/judge_kengaku_round62` is parent-appointed, not author-dispatched.
Review pending; no non-author verdict invented.

Candidate rejects (manual counterexamples in `corpus/evidence/round62/manual-answers.md`):
1. pass@k and pass^k interchangeable — rejected by case1's distinct events;
   flip: a restricted domain where the stated events/values coincide, explicitly
   restricted rather than a universal identification.
2. pooled trials estimate fixed-task macro reliability — rejected by case6;
   flip: declare a genuinely trial-pooled target instead, not rename the macro target.
3. dropping infrastructure errors yields an unconditional planned-panel point
   estimate — rejected by case7; flip: obtain valid outcomes for those planned
   slots or clearly change estimand/assumptions, never silently delete them.
4. unknown-outcome bounds are a95% confidence interval/model result — rejected;
   flip: a separately justified sampling inference procedure and real model data.

Flip check at answer freeze: none fired; the hand-worked inputs retain their
stated populations and no model run/inferential procedure exists. These are
rejects of interpretations, not rejected primary sources. Source registry
queued rows are not expansion credit. All changes of status/recheck/used-by
will be logged here when the review returns.

## Mistakes

| class | evidence pointer | captured-by | fix and failure evidence |
|---|---|---|---|
| number-drift: round61 claimed one incorrect table row where two data rows plus separator differ | round61 table-identity receipt; round62 precision-before.txt | independent round61 reviewer, Q10/R1 | append exact correction and retain old rows; preserved diff distinguishes the false one-row assertion from the three-line observation |
| attribution/number-drift: S225 pointer226 confused byte226 with pointer98 | fresh WHATWG line105; S230 | independent round61 reviewer, Q10/Q34 | new successor source row, not editing S225; pointer arithmetic identifies the false gloss |
| number-drift: old lesson273-lines and old reviewer511-diff-lines both inaccurate under measured command | literal blob counts and Git numstat in precision-before.txt | round62 author re-read, then independent reviewer agreed | append both corrections, preserve546 where actually reproduced; do not treat outside review as infallible |
| provider/environment: strict execution envelope unavailable | envelope-smoke.txt exit1 NETLINK_ROUTE denied | original Q32 envelope preflight | do not weaken/bypass; original execution proposal could-not-evaluate; revise scope before scoring to manual sourced knowledge, not execution credit |

No new QUALITY criterion invented: existing Q10, Q34, R1 and Q32 already cover
these classes. Q23's permanent executable defect checker remains a limitation;
manual corrections are not claimed to have implemented or passed it.

## Independent ordering

Parent-appointed reviewer froze revised manual challenge
sha2560db9d5bea16ef6ca665e5a08a6fca0cc05a2d848b1d7b87a7121a08a35cbb942
and sealed manual oracle
sha2564168ec0f4cfcc17e8711c43b226e95105b7d3fd7528c4b74985c3632b397d96a
before author answers. Answers committed21d46b6c, sha256
cd2961b8454d9bcebcd03cfdc59c743749316e8503bfb14cf2251b937acf4c08,
without reading either sealed oracle. Earlier283-case executable oracle is
excluded after reviewer disclosed its generator lacked the required envelope;
no laundering that procedural failure into this manual evidence.

## Returned independent source/answer review — 2026-11-02

Reviewer `/root/judge_kengaku_round62` returned
`.ufo/waves/round-62/review/REVIEW.md`, copied byte-identically from its audit
report (cmp exit0). Its candidate ADMIT and reject agreements were returned
before the knowledge-admission commit. Candidate writer is
kengaku-shokunin-round62, not the reviewer. All10 manual answers agree with the
separately hand-derived sealed oracle; report preserves the excluded original
machine oracle's procedural failure. No benchmark/runtime check is inferred.

Admit `corpus/knowledge/repeated-trial-estimands.md` on manual finite-panel
scope; outside admit/reject spot-check agrees, with reasons in the report.
D1–D3 factual corrections agree, including correcting the old review itself.
Q23 durable executable discharge is NOT established; no routed defect marked
closed and no overall round-admission claim.

Registry transitions, each after source reopening and returned review:
S226–S229 status queued→mined; used-by —→
`corpus/knowledge/repeated-trial-estimands.md, corpus/lessons/round-62.md`.
S230 status queued→mined; used-by —→`corpus/lessons/round-62.md`.
All five recheck cells unchanged180d. S225 all cells unchanged. No source
status falsely rejected to inflate discernment: rejected interpretations above
are grounded by the admitted primary sources and hand counterexamples.

## Q23 residual tracking — parent disposition, 2026-11-02

Final integration review found an additional gap: the canonical
`corpus/defects.jsonl` has no R61-D1/D2/D3 rows, not merely unexecuted checks.
Read-only inspection of `plans/defect_ledger.py` shows that unknown/missing
check names set ok=False and print observed=fail; with status=open the row
would even print agree=yes. That is NOT an honest pending/unexecuted state.
No gate semantics were modified and no fake canonical check was inserted.

Parent approved `corpus/defects-pending.jsonl` as durable **tracking only**:
three pending records, check=null, execution=not-run, canonical-insertion
blocked-by-schema, factual correction and independent review pointers. This
sidecar is NOT input to the existing gate, NOT a replacement canonical ledger,
and NOT Q23 conformance. Original stronger C2 durable discharge remains unmet.
The lack of a pending/could-not-evaluate schema is a future design issue,
not a fix claimed in this round. No gate result is invented.

Final independent integration report returned and retained byte-identically:
`.ufo/waves/round-62/review/FINAL-INTEGRATION.md`, reviewing content bdb936ee
and pending-sidecar45a662f9. C1 verified, old source rows/prefixes preserved,
C2 factual correction supported but durable-discharge unmet. Read-only source
validation before/after both exit0,218→223 rows (new5tierA), receipts in recon.
All original historical failure records unchanged. No executed metric or
permanent-check result is claimed at finalization.
