ATTACKS: lesson row M24 (`corpus/lessons/round-25.md:15`) — its three evidence pointers, the diagnosis/class, and the named red run. Pristine copy of tip 8ea41f9ed at `/tmp/k25w2-LessonM24`; every mutation only there.

POINTERS — all three resolve exactly, plus the rule
- `corpus/evidence/attrib-r22-opencode-trials.log:236` = `TARGET hyper: on-target GT n=10, correct 10/10 = 1.000 (bar 0.80, min on-target n 10) -> PASS`. Exact.
- `corpus/evidence/attrib-r22-legs.log:344` = the same clause inside block 312-362. Exact.
- `SCORECARD.md:541` = `**improved** (hyper validated; ...`; its recorded basis is `SCORECARD.md:533` `run-2: 10/10 on-target = 1.000, bar 0.80`. Exact.
- `corpus/QUALITY.md:82` Q11 exists and repeats the numbers; `SKILL.md:468-476` MR14 also landed; `plans/attrib_calibration.py` (967 lines) exists.
- `SkillRuleScout.md` (`.ufo/waves/round-25/build/`) exists but its sweeps are SKILL.md-only (`grep -n -i quality` → 0 hits). It supports the SKILL half of "no SKILL/QUALITY rule", not the QUALITY half. I checked that half: `git show 6180e4f:corpus/QUALITY.md | grep -niE 'clopper|wilson|confidence|interval|lower bound'` → empty, so the claim is true but one half is uncited.

NUMBERS
- `python3 plans/attrib_calibration.py --summary` (pristine): `target:hyper 10/10 ... stored=PASS interval=INDETERMINATE need_n=17`; totals `transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4`, `mismatches=0`, exit 0.
- Independent: `clopper_pearson(10,10)[0] = 0.6915028921812392` (= 0.025^(1/10)) → the row's 0.691503 is exact; `need_n(0,0.8)=17`; 16 → 0.7940928, 17 → 0.8049357. Two-sided α=0.05 as frozen, not one-sided (which would be 0.7411).
- Class `survivor` is in the fleet vocabulary (`CORPUS.md:173-175` → `.ufo/waves/kaika-w1/mistakes.md:447`); that list carries no per-class definition, so class is judgment; precedent `kama-shokunin/corpus/lessons/round-11.md:85` uses it for a defect that survived review. Apt for a point-PASS that stood r22→r25.

RED RUN — goes red; one conformance caveat
- `--selftest`: 14 checks, 0 failed. R1 `exit 1, MISMATCH ... rows:correct`; R1b `exit 1, ... gt_counts stored={'a': 17} recomputed={'a': 16, 'b': 1}`; R4 `exit 1, ... accuracy stored=[10,20,'0.500','PASS'] recomputed=[10,20,'0.500','FAIL']`. Genuine non-clean exits, not just printed.
- Red path on the real receipt: in the /tmp copy I flipped the cited clause PASS→FAIL; `--summary` → exit 1, `MISMATCH corpus/evidence/attrib-r22-opencode-trials.log:236 target:hyper: stored=[10,10,10,'1.000','FAIL',{'hyper':10}] recomputed=[...,'PASS',...]`.
- Caveat: the M24-specific red (re-verdict INDETERMINATE) is exit 0 by design — `plans/attrib_calibration.py:47` "INDETERMINATE is a finding, not an error". Only receipt-consistency/fixture mutations exit non-clean. Q11 has no executable gate: `grep -n attrib_calibration grader.py plans/state_check.py` → 0 hits; enforcement is a runnable manual command.

COUNTEREXAMPLE to the implied diagnosis (population)
- `corpus/evidence/attrib-r22-legs.log` holds TWO distinct scored runs: `:260` (journal @1792151401-539; GT hyper 9 / alibaba 10 / opencode 1; T03 GT=opencode-go) and `:312` (@1792151616-737; GT hyper 10 / alibaba 10; T03 GT=hyper). Its own addendum says (`:376-378`) "both score blocks above are this seat's authoritative adjudication"; `plans/attrib-r22-frozen.md:286`: "hyper 19/19 = 1.000 across both runs".
- `clopper_pearson(19,19)[0] = 0.8235330881930345 ≥ 0.80` → PASS (trial-level; the lane prints `bodies=2 iid-fragile` for r22).
- The INDETERMINATE is produced by `plans/round-25-claims.md:29` last-block rule, whose cited warrant (`attrib-r21-impl-ds-trials.log:316-318`) is "the earlier score blocks are the debugging trail of three instrument defects"; legs.log has no AUTHORITATIVE line (`grep -n AUTHORITATIVE corpus/evidence/attrib-r22-legs.log` → empty). Amendment 1 item 5 (`plans/round-25-claims.md:133`) labels `:260` non-authoritative by fiat. Independently already reported at `falsify/CritAuthoritativeBlock.md` findings 1-3.
- Net: the stored line was point-gated on 10/10 (row true), but `hyper validated` is not interval-false on the receipt's full authoritative evidence; the defect is the verdict rule/basis, not the claim's evidence base.

AGREE: pointers, numbers, class, selftest reds, and the real-receipt red path all verify.
DISAGREE: the row's implied reading that r22 hyper was under-powered is population-dependent and contradicted by the receipt's own both-authoritative adjudication (19/19 → 0.823533); and the "no SKILL/QUALITY rule" pointer evidences only the SKILL half.

VERDICT: PARTIAL — every literal claim and both red mechanisms verify, but the INDETERMINATE generalization rests on a last-block rule the receipt contradicts, so "hyper validated" was not interval-false; Q11 stays prose-only.
Installs: none (python3 stdlib + repo grader betai; no packages needed).
