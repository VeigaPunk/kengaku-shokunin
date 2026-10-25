## 1. [blocks]
PREAMBLE — INC-vs-MONO does not isolate planning horizon. The binding confound is not chat-format familiarity and not token length (MONO's single prompt is only a few hundred tokens at 10 ops): it is the SELF-COPY SCAFFOLD. In INC the immediately preceding assistant message is the full previous state, so each turn degenerates to copy-and-patch of one's own output — context re-reading, not cross-turn maintenance. MONO forces latent chaining. The INC−MONO delta therefore measures scaffold assist vs latent chaining, i.e., a protocol difference, not a horizon difference. (Token-length effects are second-order here; format-familiarity is real but subsumed by the same scaffold.)
**Fix:** Sparse-checkpoint INC: turns 1..k-1 acknowledge-only ('ok'), full-state emission required only at 1–2 checkpoints plus the end. Forces internal maintenance between checkpoints while keeping the transcript shape. (MONO-CHAIN — all ops one message, emit state after each op — is a useful complementary cell but adds a scaffold in the other direction; checkpointing is the cheaper single fix.)

## 2. [bends]
No arithmetic calibration: ADD/SUB/MOV chains at UD-IQ2_XXS (~2-bit quant) conflate state-tracking failure with quant-arithmetic failure; the onset curve would misattribute both.
**Fix:** Clamp operands to single digits (|delta|<=9) so arithmetic sits inside quant competence, and report a 10-probe single-op arithmetic sanity number alongside as covariate. Cheapest: clamping alone.

## 3. [bends]
Op semantics edge cases unpinned: ADD/SUB on a missing key (0 vs error), MOV from a missing key, MOV a a, NEW on an existing key (overwrite vs error), DEL-then-NEW same key, negatives allowed? Any generator emitting these produces spec-ambiguity failures graded as capability failures.
**Fix:** Pin semantics in the shared rules text; constrain the generator to unambiguous instances. If edge cases are deliberate, make them a labeled stratum, not background noise.

## 4. [bends]
Metric asymmetry + coarseness: the error-onset curve exists only for INC (MONO is final-only), so the curve is a within-INC description and cannot enter the cross-protocol comparison. And dict-level exact match makes onset coarse: one wrong key marks the whole state wrong, so recovery is invisible.
**Fix:** Dual grading per turn: dict-exact AND per-key accuracy; onset = first key-mismatch; add a recovery-rate stat (wrong key returning to correct). Pre-register that curve claims are INC-internal.

## 5. [bends]
Output schema convention unpinned: after DEL must the JSON drop the key or emit null? Key order? ints vs floats? Systematic conventions differing from the grader produce stable scoring misses that look like state errors.
**Fix:** One rules sentence: 'output exactly the keys currently present, any order, integer values'; grader parses to dict so key order/whitespace are already non-issues.

## 6. [blocks]
Probe B structural hole: if none of ops 8..10 touches the corrupted key, plain-cell has no opportunity to detect the inconsistency, and the pass/fail meaning flips by seed mix. Propagation rate becomes a function of seed luck, not capability.
**Fix:** Design-time constraint: at least one of ops 8..10 must touch the corrupted key in every trial; report the touched/untouched split if untouched trials are kept.

## 7. [blocks]
Missing cell that flips the B conclusion: hint x CLEAN. With only plain/corrupt, hint/corrupt, control/clean, you cannot see whether the hint induces false-positive 'corrections' of a correct state. If hint-on-clean underperforms plain-on-clean, 'the hint helps recovery' must be netted against benign-case damage — the exact pattern of last round's missing {no-system x high-temp} cell.
**Fix:** Run the 4th cell of the 2x2 (hint x clean) — same harness, zero new machinery.

## 8. [bends]
B outcome coding collapses mechanisms: final==simulation-from-correct can mean 'caught the inconsistency' or 'ignored the intermediate and recomputed from init+all ops'. If plain ~= clean-control, the manipulation never bound and B says nothing about recovery. Corruption magnitude is also unconstrained: +/-1 on a hot key is near-undetectable, a wild value is trivially caught.
**Fix:** Pre-register 3-way outcome coding: propagated (==sim-from-wrong), corrected (==sim-from-correct), other; headline = propagation rate, control bounds the recompute baseline. Pin corruption shape: corrupted value = an earlier historical value of that key (off-by-one-op) — plausible yet verifiable.

## 9. [blocks]
Probe C: violations=[3] is grader-conventional, not model-derivable. Under 'columns must also be permutations', rows 1–3 pairwise conflict in that column; electing row3 silently bakes in an earliest-rows-have-priority rule the prompt never states. A model answering [2] or [1,2,3] is defensible but graded wrong.
**Fix:** One rules sentence: 'rows are kept in emission order; a row is a violation iff it conflicts with the already-kept rows; earlier rows are never removed.' Then [3] follows logically.

## 10. [bends]
Extraction rule is the real grading risk, not dict brittleness. Existing grade.sh extracts the FIRST closed fenced block; an INC turn with preamble prose or an illustrative fence grades the wrong block, and parse-failure gets conflated with state failure.
**Fix:** Pre-registered parser: prefer the last fenced ```json block, fall back to last balanced {...}; json.loads only, no repair; parse-fail logged as its own failure class (per digest-3, per-failure-class reporting), with a sensitivity run counting them as zero.

## 11. [cosmetic]
C symbol choice: multi-byte glyphs tokenize messily on this quant and hazard exact string-compare for 'non-violated rows preserved'.
**Fix:** ASCII 1–4/A–D; grade rows as tuples.

## 12. [blocks]
Missing C baseline: benign (rule arrives, changes nothing) vs monolithic control differ in BOTH rule-integration cost and transcript-shape cost (fabricated assistant turns, instruction accumulation). If benign < monolithic you cannot attribute the gap.
**Fix:** Add benign-minus-rule: same fabricated transcript shape, no new rule, asked for row4. benign vs that isolates rule-integration; that vs monolithic isolates transcript overhead.

## 13. [bends]
System-prompt presence unpinned. r7 ablation proved system-prompt presence flips strategy (task 13, 9/9); the tools+tool_choice trap is moot (no tools here) but scaffold inconsistency would put a scaffold delta inside every cell contrast. (r7 also showed temp is non-causal and enable_thinking is a no-op on this template — do not spend cells on either.)
**Fix:** Pin one minimal system prompt across ALL cells, and since format compliance is the top parse risk, have it mandate the exact output block ('respond with only the JSON block').

## 14. [blocks]
Statistical scope is the biggest defect: 4 seeds x n=2 cannot support ANY comparative claim at alpha=0.05. r7-n25 measured lag-1 +0.26/+0.32 with a 5–10 request burst horizon and near-deterministic same-seed replays, so 8 draws carry ESS ~= 4–5: an 8/8 sign-unanimous result is p~0.004 iid but ~0.06–0.12 at that ESS. Reps of the same seed are the wrong unit (replay is near-deterministic; consecutive draws burst-couple) — distinct seeds dominate reps. Also the onset curve must use the RUN (problem) as unit, never pooled turns as independent points.
**Fix:** Drop n=2, buy seeds: 12–16 distinct seeds x n=1, interleaved across cells with filler requests between same-condition draws to break burst adjacency; pre-register a paired sign test across seeds (problem = unit); if signs split, report descriptive-only. Budget-neutral: same call count.

## 15. [bends]
Op-mix difficulty unstratified: 4 seeds with free op-type sampling means one MOV/DEL-heavy seed can dominate the paired delta.
**Fix:** Constrain the generator to a fixed op-type histogram per problem (e.g., 3 SET/2 ADD/2 SUB/1 MOV/1 DEL/1 NEW, small jitter); report the per-problem table regardless.

## 16. [cosmetic]
Truncation artifact: this endpoint has a known finish=length family (r5 task 06 at max_tokens 4096); MONO's single long answer and C's full-square emission can auto-fail as harness artifacts.
**Fix:** max_tokens >= 8192 for MONO/C, log finish_reason, classify finish=length separately from state errors.

