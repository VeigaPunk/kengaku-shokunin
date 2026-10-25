# CritPredictionsHonesty — round 26 build wave (critic, read-only; judged on novelty)

Target: P1–P10, `plans/round-26-claims.md:101-117` (caveat at `:103-104`). Method: reasoning over `grader.py:121-134` and the equality graders it feeds, plus a raw-shape census of the four C1 population files. Neither `grader.py` nor the draft `plans/grader_perturb.py` was executed.

## Census (stored bytes; stdlib python3, no grader import)
`cd corpus/evidence && python3 -c '<count "```" per raw; ok/turn tallies over the 4 files>'` →
`graded 1964 pass 1021 {'bare_single_json_block': 1788, 'fences=1': 57, 'fences=6': 31, 'fences=0': 88} got_types {'dict': 1720, 'list': 244} turn>=2 1752 pass 914`
- 1788 raws are exactly "```json\n<JSON>\n```" with no prose. 57 are "<JSON>\n```" (closing fence only), 88 are bare JSON, and 31 are r8 B "After operation 8/9/10" triple blocks (`round8-horizon/results.jsonl:221-242,244-252`; 17 stored PASS; the op-10 block differs from the op-9 block in all 31). No stored parse failures. Answers nest at most 2 deep: flat dicts, flat token lists, C dict→list→list, C-MONO list→list.

## Re-derivation (when k=n, CP95 lower = 0.025^(1/n), which is ≥0.95 iff n≥72: n=71 gives 0.94937, n=72 gives 0.95006)
- **P1 F1 (filed 0.75 → mine 0.98).** Without a fence, `:122` finds nothing and extraction falls to `:128`. The `{` branch accepts brackets and the `[` branch accepts one inner level, so every census shape re-extracts the identical object. Only the 31 triple-block raws can flip, and only if just the last fence is stripped. At n=1819, PASS tolerates 72 flips (worst case, 31 flips: CP lower 0.9759). The draft strips every fence (`/tmp/kengaku-r26-ExecPerturbCore/plans/grader_perturb.py:380-381`, read only), which gives 0 flips.
- **P2 F2 (0.85 → 0.98, must equal P1).** `(?:json)?` at `:122` is case-sensitive (no `re.I`). "```JSON\n" fails `\s*\n` at the "J", so all 1788 single blocks take the same `:128` fallback as F1. On triple blocks, a global relabel (draft `:386`) pairs each closing fence with the next opener, capturing only "After operation N:" prose. That fails `json.loads`, so `:128` returns the last JSON: 0 flips. **Filing P2 above P1 contradicts the code it cites.**
- **P3 F3 (0.95 → 0.99), P4 F4 (0.97 → 0.99).** `json.loads(dumps(x)) == x`, and dict `==` ignores key order (`:225`, `:2121`; grade_c reads keys with `.get` at `:252`). So k=n by identity, with n≤1964 for F3 and ≤1720 dicts for F4.
- **P5 F5, P6 F6 (0.95 → 0.99).** The family text forbids brackets (claims `:62-63`) and adds no backtick fence. `:122` keys only on backtick fences and `:128` only on brackets and braces, so neither path can see the added line. PASS holds **by definition**.
- **P7 F7 (0.90 → 0.99).** Greedy `\s*` backtracks so `\n` still matches after `\r`, and JSON whitespace includes `\r`. Identity.
- **P8 D1 (0.03 → 0.005).** `:125` takes `blocks[-1]`, which is the distractor. Every baseline PASS flips except no-op turns (≈0.5%: 4 of 738 consecutive graded pairs share a stored `want`). FAIL stays FAIL. Invariance ≈ 1 − pass rate = 838/1752 = 0.478, CP95 ≈ [0.455, 0.502], so the verdict is FAIL.
- **P9 G1, P10 G2 (0.97 → 0.99).** Grading is exact equality (`:225`, `:2121`, `:267`; `valid_latin` `:236-238`), so +1, token replacement, or key/element deletion on a got==want answer always FAILs. I checked the hard case: in C-norule, `rows_perm_only` (`:244`) breaks when one leaf is replaced. n≤1021 PASS records gives CP lower 0.9964.

## Findings
1. **All ten outcomes are fixed before measurement.** P3–P7, P9 and P10 follow from `:121-134` plus `==`. P1, P2 and P8 additionally need only the census above. The 0.03–0.25 residual mass prices instrument defects, not grader behaviour, so "code-derivable forecasts" (`:103`) overstates them: they are expected outputs.
2. **Scored as filed, they would yield a meaningless Brier.** If the derived outcomes hold, mean Brier = 0.0106 (P1 0.0625, P2 0.0225, P7 0.0100, all others ≤0.0025). That looks excellent but is earned by construction. Even with "no calibration credit", a close line such as "predictions 10/10 direction-correct" would be false provenance.
3. **P2 > P1 is a derivation error, not a hedge.** Both families route to `:128` on 1788 of the 1819 records F2 applies to.
4. **The derivation basis is cited incompletely.** `:103` cites only `:121-134`, but P3, P4, P9 and P10 rest on `grader.py:221-225`, `:2115-2121` and `:247-267`. Also, claims `:50` names grade_c for "r8 C-cells", while C-MONO is graded by `valid_latin` (`grader.py:498-501`). Under grade_c, its 4 stored PASS records would fail baseline reproduction; the draft special-cases them at `grader_perturb.py:248`.
5. **Information content of the verdicts (novelty).**
   - With k=n, the CP verdict for F1–F7, G1 and G2 says only that n≥72.
   - F1/F2 PASS comes from the `:128` fallback recovering a fence-blind miss on a population that is 91% bare single blocks. It does not show the fence path is robust.
   - F5/F6 PASS is guaranteed because the "no brackets" clause excludes the one input class `:128` reacts to.
   - So the 0 → 10 interval-verdict observable adds about 0 bits beyond code plus census.

**Strongest counterexample:** F1 combined with a bracketed sign-off (append "\nTotals: [5]") flips every PASS: `:128` returns `[5]`, and `grade_state` `:222` FAILs a non-dict, while `grade_seq` gets a wrong list. Plain F6 cannot flip by definition. No registered family leaves the provably invariant region. This outcome is equally derivable, so no family in C1 is a genuine forecast target.

**Impacted axes:**
- novelty → coverage/constructs: the family verdicts cannot back a +1.
- calibration: P1–P10 must carry zero forecast weight.

## Smallest safe correction (fixable; no instrument output is committed in the lane tree yet)
Append `## Amendment 1` to `plans/round-26-claims.md` before any `grader_perturb.py` output lands:
- (a) Relabel P1–P10 as "derived expectations" and replace p(PASS) with the expected (n, k):
  - F1–F7, G1, G2: k=n.
  - D1: k = baseline-FAIL records with previous≠want, plus PASS no-op turns.
  - F1/F2: flips ⊆ r8 lines 221-242 and 244-252.
- (b) Make (a) an acceptance check that the independent oracle (`plans/fixtures/r26/`) must reproduce. A miss is an instrument bug, not a forecast miss.
- (c) The C1 entry should say that the F1/F2 and F5/F6 PASS verdicts come from the `:128` fallback and the "no brackets" clause.
- (d) No Brier, hit-rate or "predictions confirmed" line at close.

**Not fixable by wording (canonical judge):** reject any novelty +1 argued from the ten family verdicts, because all of them were derivable before measurement. At most the instrument itself (a mechanized regression check) can be credited.

VERDICT: P1–P10 are not forecasts. All ten verdicts follow from grader.py:121-134 + exact-equality graders + a raw-shape census (PASS F1–F7/G1/G2, FAIL D1). Rescore P1/P2 0.75/0.85 → 0.98 (P2>P1 contradicts :122), P3–P7/P9/P10 → 0.99, P8 → 0.005, and score none as forecasts. This is fixable by an appended amendment; a novelty +1 resting on the verdicts must be rejected.
Installs: none. The host's `jq` is jaq 3.1.1 (unchanged); the census used python3 stdlib. No writes besides this report.
