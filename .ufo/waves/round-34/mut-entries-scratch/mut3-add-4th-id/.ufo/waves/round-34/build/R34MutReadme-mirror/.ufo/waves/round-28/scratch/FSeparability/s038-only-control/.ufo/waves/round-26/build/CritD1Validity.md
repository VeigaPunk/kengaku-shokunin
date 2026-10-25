# CritD1Validity — round 26 build, critic (read-only seat)

Target: D1 = "append a second fenced JSON block restating the *previous* turn's truth as 'for reference'", MP, expected "unchanged" (plans/round-26-claims.md:65; metric :69-73). Tree: lane HEAD e0037a8da268. The 4 result files, grader.py and critic-defects.md are byte-identical to base f11bffbf (`git diff --quiet f11bffbf e0037a8 -- <6 paths>` → exit 0). Offline only. Numbers come from `python3 /tmp/critd1-validity/d1_check.py` (imports grader.py by path) and the lane's `clopper_pearson`.

## What the prompts require
- All graded responses ran under one system prompt: "Reply with exactly one fenced ```json code block and no other text — unless the user asks you to reply 'ok'."
  - Sources: horizon.py:18-19 (r8); replicate.py:18-19 (r9, every call routed through it, run_r9.py:3,9,13); probe_r11.py:27-28 (run_r11.py:55-56); probe_r12.py:31-32 (run_r12.py:80-81).
  - Stored verbatim as `system_prompt` in results-r11.jsonl:1 and results-r12.jsonl:1. The C prompts repeat "fenced json block" (horizon.py:248,:293); B cells ask "output the FINAL state" after an assistant prefill of per-op fenced blocks (horizon.py:199-205).
- The mandate serves parse reliability, not a graded construct: critic-defects.md:49-51 (#13), "format compliance is the top parse risk".
- The same r8 review pre-registered the extractor (critic-defects.md:37-39, #10): "prefer the last fenced ```json block, fall back to last balanced {...}". It was adopted because first-block extraction grades "preamble prose or an illustrative fence" wrong. horizon.py:7 calls it the "last-fence parser"; grader.py:24-26 ports it verbatim for REPLAY.

## Findings
- **F1. Not enforcement.**
  - grader.py:122-125 takes `blocks[-1]` without checking block count or "no other text"; the fallback (:128-133) content-grades unfenced text.
  - Script output: graded=1964, noncompliant=176 (unfenced=145, multiblock=31), noncompliant_storedPASS=43. An enforcing grader would turn those 43 stored PASS verdicts into FAIL. The lane reports parse-fail as its own class and tracks compliance only for ack turns (analysis_r12.md:44, :45-49).
  - The grader also passes D1 output whenever the appended block equals want: D1_noop_FAIL_to_PASS=14 of 19 no-op turns. Enforcement would never pass a wrong answer because a block was appended.
- **F2. Not a defect against the grader's own spec.**
  - The case the r8 rule targets is in the stored data: all 31 multi-block responses are r8 B cells shaped "After operation 8/9/10:" with three ```json blocks.
  - multiblock_storedPASS=17 and multiblock_storedPASS_firstblock_FAIL=17: every stored multi-block PASS exists only under last-block selection.
  - Under the pre-registered rule the trailing block *is* the answer, so D1 changes meaning for this grader. Calling D1 "meaning-preserving" depends on the English label "for reference", which neither the prompt contract nor critic-defects.md:39 gives any meaning.
- **F3. A tradeoff, not something to fix in grader.py.**
  - No position-based extractor can be invariant both to leading intermediate fences (31 stored, 17 PASS) and to a trailing distractor (D1).
  - Making grader.py D1-invariant by position flips those 17 stored PASS to FAIL and breaks REPLAY (stored ok must equal a fresh re-parse; grader.py:24-26).
  - A "skip blocks labelled 'for reference'" rule passes D1 only by keying on the perturbation's own label (Goodhart), and it would be a new, never pre-registered policy.
- **F4. Counterexample: D1's invariance metric is an identity of the probed model's accuracy, not a property of the grader.**
  - On D1-applicable records whose distractor differs from want, every regrade is FAIL: D1_n=1815, D1_basePASS=983, D1_invariant=832, D1_capture_of_basePASS=983. The script confirms `IDENTITY D1_invariant == D1_n - D1_basePASS: True`.
  - CP95(832,1815)=[0.4353,0.4817] → FAIL. D1 would verdict PASS only if basePASS ≤ 72/1815 (3.97%), so a near-always-wrong probe model would make the grader "pass" D1.
  - P8 (claims:115, p=0.03) therefore forecasts the r8–r12 model's pass rate, which the committed bytes already fix.
- **F5. 231 records the claims leave unruled or degenerate.** 130 single-turn records have no previous turn (A-MONO 82, B/C 48). 82 turn-1 INC records have "previous = init" only by assumption. 19 no-op turns have previous truth == want, so the distractor is not a distractor; 14 of them would score FAIL→PASS as non-invariance.
- **F6. The real format sensitivity is fence precedence, which D1 cannot isolate.**
  - Mirror D1′ prepends the same block. Fenced records: 1675/1675 invariant, CP95 [0.9978,1]. Unfenced records: 114/140, with D1m_capture_unfenced_basePASS=26/26.
  - Any fenced block anywhere overrides a correct unfenced answer (grader.py:122-128), contradicting the rule's own "final answer comes last" rationale. This, not D1, is the format-dependence finding.

## Ruling
A last-block misgrade under D1 is **neither a grader defect nor correct enforcement**. It is the r8 pre-registered answer-selection rule (critic-defects.md:39) applied to a response that breaks the probes' contract (horizon.py:18-19 and the other three probes). The defect is in the round-26 pre-registration:
- claims:65 files D1 as MP with "unchanged" expected. That makes a second authority on multi-block answer selection, contradicting r8 (a duplicate authority).
- claims:69-73 scores D1 as invariance over mixed baselines, which turns its verdict into an identity of model accuracy (F4).

## Impacted axes
- **novelty → coverage/constructs:** the "0 → 10 families with interval verdict" observable (claims:89-90) counts one family whose interval measures the probe model's failure rate. A C1 knowledge entry reporting "D1 FAIL = grader format-fragility" would be false provenance.
- **calibration:** P8 is non-diagnostic. claims:103-104 already takes no credit; it must not be rescored as a grader forecast.

## Smallest safe correction (fixable now; append-only; before the first grader_perturb.py run)
Append `## Amendment N` to plans/round-26-claims.md:
- (a) Reclassify D1 from MP to policy-conformance, expected "trailing block captured per critic-defects.md:39". Metric: capture rate over baseline-PASS records whose distractor ≠ want (same conditioning as G1/G2, so the base rate drops out; 983/983 here).
- (b) Applicability: not applicable for A-MONO, B-*, C-* and wherever previous truth == want. For turn 1, state previous truth = meta `init` explicitly or mark it not applicable.
- (c) The knowledge entry and SCORECARD must not cite D1 as a defect. (d) Optional: add mirror D1′ as the MP family the rule is built for, reporting fenced and unfenced separately (F6).

**The judge must reject:** any edit to grader.py `extract_json_block` that makes D1 pass (regresses 17 stored verdicts and REPLAY), and any admit that counts D1-as-invariance toward the observable or cites it as a grader defect.

Files written: this report only. Scratch: /tmp/critd1-validity/d1_check.py, sha256 99e358839386ea83f30c6674b3e9bc86d7df91e9c4ac1a0877aa70162c3962fc (reproduces every number above; only reads lane files). Installs: none.

VERDICT: D1 is construct-invalid as an MP invariance family. Its flip is the pre-registered r8 last-block rule (neither defect nor enforcement), and its rate is the identity 1815−983 = 832. Fix it with a pre-run Amendment (policy kind, PASS-conditioned capture, explicit applicability). Reject any grader.py "fix" and any D1-based defect claim.
