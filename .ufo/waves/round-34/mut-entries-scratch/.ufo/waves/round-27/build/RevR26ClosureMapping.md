# RevR26ClosureMapping — round-26 closure items vs round-27 pre-registration

Axes: calibration (judged). Novelty and coverage appear only where the pre-registration ties a closure item to them.
Read-only review. Paths: lane = `kengaku-shokunin/…`; fleet = `.ufo/…` and `PROTOCOL.md`. Sources: closure `.ufo/reports/round-26/kengaku-closure-evidence.json`; report `.ufo/reports/round-26/kengaku.md`; pre-registration `plans/round-27-claims.md` at master `11a7fc8` (153 lines, no amendments); base `b5719440`. Base export `/tmp/kengaku-r27-RevR26-base` (git archive, read-only). Lane index and jj untouched.
Key: ADDRESSED = pre-reg clause present. PARTIAL = clause with a stated gap. DEFERRED = explicit defer or disclaimer. IGNORED = no pre-reg mention.

## A. Closure limitations (closure :562-568)
| # | Item (closure line) | Disposition | Evidence / gap |
|---|---|---|---|
| L1 | P2/P3 miss r26 assertions; 3 offline-unverifiable disclosed (:563) | PARTIAL | C2/P4a-e answer the first clause (pre-reg :102-124). The offline clause is unanswered; its class is `plans/state_check.py:1119-1122` (P2d), unmentioned. |
| L2 | P3 oracle: 2 extension-only historical-range mismatches "marked by README errata" (:564) | IGNORED | Pre-reg never names the P3 oracle. Errata NOT located: grep finds no such wording in corpus/README.md, LOG.md, SCORECARD.md or plans/fixtures/r26; only the claim at `corpus/lessons/round-26.md:184`. |
| L3 | Intervals are nominal descriptive, not future guarantees (:565) | ADDRESSED | Pre-reg :52-54. Residual gap G2. |
| L4 | Lane-dispatched reports are not outside verification (:566) | IGNORED | Pre-reg silent; only :5-7 name the r26 closure. Governed by QUALITY R6 (`corpus/QUALITY.md:132`) and the close rule (:125). Gap G3. |
| L5 | r25 stays rejected-honest-stop; ledger not edited (:567) | ADDRESSED | Implicit: append-only (pre-reg :11; QUALITY R1 :127); SCORECARD.md:743-744 says R26-E4 does not admit r25. |

## B. Outside spot-check (closure :532-561; 4 rows, all `agree`)
| # | Row (closure lines) | Disposition | Evidence / gap |
|---|---|---|---|
| S1 | admit grader-perturbation-audit (:533-539) | ADDRESSED | C1 uses the same frozen population (pre-reg :29-31). |
| S2 | reject novelty +1 (:540-546) | ADDRESSED | Novelty held at 7; +1 needs prior art and critic agreement (pre-reg :73-78). |
| S3 | reject D1 as robustness (:547-553) | PARTIAL | "robust" has zero hits in pre-reg. The rule lives only in `corpus/knowledge/grader-perturbation-audit.md:54,:87,:101`. Gap G4. |
| S4 | reject pooled CP95 as guarantee (:554-560) | ADDRESSED | Pre-reg :52-54. |

Contract answer: r26 has zero closure disagreements (4/4 agree; pre-reg :5-7 says so). Precedent: r24 reason disagreement became Q9/Q10 (`corpus/lessons/round-24-verifier-spotcheck.md:13`); r25 disagreement became Q13/Q14 (`corpus/QUALITY.md:97-121`). No new QUALITY row is mandated. L2, L4 and S3 still need a row or a stated why-not (G1-G4).

## C. Routed and open items (kengaku.md; L0 queue; r25 closure)
| # | Item (source) | Disposition | Evidence / gap |
|---|---|---|---|
| R1 | "Four numeric defects already routed" (kengaku.md:10,:14) | CLOSED in r26 | R26-E1/E2 SCORECARD.md:739-740; R26-E3a/b PROVINCE.md:180-181; R26-E4 `corpus/lessons/round-26.md:18-21`. |
| R2 | r25 routed item 5, out-of-population capability rows (`corpus/lessons/round-25-verifier-spotcheck.md:160-161`) | CLOSED in r26 | Supersession targets P3a.capability.* (SCORECARD.md:739-740, :749-750). Pre-reg silent; P4 covers round 26 only. |
| R3 | Parser-policy comparison open (`corpus/README.md:260`) | ADDRESSED | C1, pre-reg :21-23. |
| R4 | New formats open (README:260; kengaku.md:19) | IGNORED | "new format" has zero hits; C1 holds responses fixed. Needs a defer line. |
| R5 | Future generalization open (README:260) | DEFERRED | Disclaimed, pre-reg :52-54. |
| R6 | Routed to tameshi/chousa/kama/kumitate (kengaku.md:19) | IGNORED | "tameshi" has zero hits; pre-reg keeps state_check v4 lane-local without a routing decision. |
| R7 | L0 coverage cap (`.ufo/l0-questions.md:72`) | DEFERRED | Pre-reg :17-19 defers to operator. |
| R8 | L0 novelty conversion (`.ufo/l0-questions.md:73`) | PARTIAL | Holds 7 with no conversion (:17-19, :73-78) but never cites or defers :73. |
| R9 | 11 falsify dead seats; refusals (kengaku.md:30-36); Main connector-routing FYI | IGNORED | Pre-reg :151-152 allows 64-100 falsify seats with no fallback. Q13 blocks admission without returned re-reads (QUALITY.md:97-107). |
| R10 | W04 duplicate URLs S040/S048 (kengaku.md:109-114) | ADDRESSED | Pre-reg :140-147 acknowledges "two W04 warnings". |
| R11 | SHONEN four boxes author-asserted (kengaku.md:132-137) | IGNORED | No R27 SHONEN claim, which is correct (PROTOCOL.md:66-68). |
| R12 | Mistakes M39-M54 (kengaku.md:18,:120) | ADDRESSED | Selftest kill/red rules (pre-reg :63-66, :124); mistake mining (:140-147). |
| R13 | Misroot notice to KaidokuR21-2 (kengaku.md:47) | IGNORED | Outside lane scope; no action. |

## D. Findings by severity (not in closure)
- HIGH G1 P4 window. P4a-e cover five artifacts (pre-reg :107-119); LOG.md §Round 26 (:321-327) and README:276-285 sit outside. Stale tokens just outside P4b: README:277 "Q1-Q13" vs QUALITY.md:111 Q14; README:280 says Q1-Q14 without line-named erratum (R5); PROVINCE.md:111 says Q1-Q8 without erratum. Widen P4b to README:264-285, add LOG §Round 26, or list exclusions.
- HIGH G2 CP95 unchecked independently. C1 reuses lane `clopper_pearson` (pre-reg :52-53; `plans/attrib_calibration.py:144`); oracle emits counts only (round-27 Shared interfaces). R26 closure recomputed CP by 60-step bisection (:139). Add oracle CP recompute or state why not.
- MED G3 No outside step in pre-reg: no roster-external admit+reject sample; QUALITY.md:125 says an unshown row is open. Name R6 in pre-reg.
- MED G4 C1 lacks a non-robustness clause (S3); the rule exists only in `corpus/knowledge/grader-perturbation-audit.md:54,:87,:101`. State policy spread is dependence/conformance, never a robustness PASS.
- LOW G5 Citation hazard. Pre-reg :47 calls BARE_RE byte-identical to `grader.py:128` (inline same pattern); `grader.py:2460` `_BARE_RE` has a different pattern. Cite the literal and assert string equality in selftest.
- LOW G6 Pre-reg :7-8 truncates L1's offline clause yet says C2 "answers exactly that limitation". Quote it in full.

## E. Checks run (read-only)
- `git diff --stat b5719440 11a7fc8 -- grader.py plans/state_check.py plans/grader_perturb.py plans/attrib_calibration.py SCORECARD.md corpus/README.md PROVINCE.md corpus/QUALITY.md corpus/SOURCES.md` → no output. Tree-wide: 3 files, +287.
- Anchors confirmed: grader.py:121,:122,:221; grader_perturb.py:35,:36,:54,:187,:259; state_check.py:197 (SUPERSEDE_RE R2[5-9]-E), :2502 (--selftest). Pre-reg E0 text matches grader.py:121-134 (last fence, then reversed bare candidates).
- Prediction "base P4 mismatch ≥1" (p=0.55): no stale token inside P4a/P4b windows; the visible stale tokens lie outside. No update.
Verification gap: no R27 instrument/base-P4 run or independent oracle run; errata lookup was grep-level, not exhaustive.
Residual risk: alleged README errata remains unlocated; P4 coverage is scoped, not a census of all r26 numeric claims.
Installs: none. Files written: this report only.
VERDICT: Pre-reg covers L3, L5, S1/S2/S4 and part of L1; L2/L4 are unaddressed, S3 partial; r26 has no disagreement needing a QUALITY row. G1-G6 require resolution or explicit disposition before R27 closes.
