# Round 26 — pre-registration (frozen before wave 1, 2026-10-21)

Base: lane `master` = `f11bffbf9caa9c9e286fb32c568b81b97719656a` (jj-colocated; `jj-lane.sh state` →
`ahead=0 behind=0 tracked=0 untracked=0` at readiness). Round 25 closed REJECTED-HONEST-STOP
(`corpus/lessons/round-25-verifier-spotcheck.md`; MANIFEST rounds[376]).
Author: KengakuR26-2 (L1; holds the frozen planner seat — the wave validator rejects `planner`).
Amendments are appended below as `## Amendment N`, never edited in place.

## 0. Repair first (routed by the round-25 closure; not claims)

Append-only fixes, each a dated `R26-E*` row naming the superseded text:

| id | superseded text | observed today | fix |
|---|---|---|---|
| R26-E1 | `SCORECARD.md:558` (`interval-reverdict`) "`--selftest` 14 checks" | `corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt` ends `selftest: 18 checks, 0 failed`; SKILL registry says 18 | SCORECARD correction row against the capability cell |
| R26-E2 | `SCORECARD.md:559` (`state-assertion-check`) "base `6180e4f` `mismatch=11`" | v2 receipt `state-check-before-6180e4f-v2.txt` → `mismatch=10` | SCORECARD correction row against the capability cell (not only revision prose) |
| R26-E3 | `PROVINCE.md:119` "holds 37 after round 25" | `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 42 at base | appended PROVINCE correction naming S038–S042 |
| R26-E4 | `corpus/lessons/round-25.md:29` Gate Q10 cell "and by wave-2 seats" as landed at `8ea41f9` (commit 21:44:48 -03; first wave-2 report 21:49:53 -03) | evidence cited before it existed | appended erratum in `corpus/lessons/round-26.md`; new QUALITY criterion **Q13** + check (below) |

**Q13 (new, from M39 below).** An entry is admitted only in a commit whose tree already contains the
second-seat (Q10) re-read report(s) its Gate row cites; the Gate cell names each such report by path, and a
generic seat reference ("wave-2 seats", "falsify seats") supports nothing. Check:
`python3 plans/gate_timing_check.py --lesson corpus/lessons/round-<N>.md --commit <landing>` exits 0;
red-before: the same command on `8ea41f9` / `corpus/lessons/round-25.md` must exit 1, naming the Q10 cell.
Consequence for this round's own process: the C1 knowledge entry is drafted outside `corpus/` and is
admitted only in a commit that also lands the wave-2 re-read reports it cites.

## Axis state at base (SCORECARD.md §Round 25 falsify-wave revision, re-derived line)

novelty 7 · coverage 7 (capped) · calibration 8 · operability 8 · freshness 8 · adjacency 8 · depth 9.
Lowest non-retired: **novelty 7, tied with coverage 7**. No stagnation waiver (novelty < saturation line 8).
Tie-break: coverage stays capped by the declared-but-unresolvable-surface clause until the operator rules the
filed L0 (`.ufo/l0-questions.md:72`); its number cannot move, novelty's can. `novelty` keeps its recorded
mapping → canonical coverage (constructs) (round-25 Amendment 1 item 2); this round makes no separate
coverage claim.

## C1 — novelty (→ coverage/constructs; lowest): metamorphic perturbation audit of the lane's own grader

Construct (new to the lane): **verdict invariance of `grader.py`'s response grader under perturbations of the
stored model responses** — the frontier's remaining half of "judge calibration applied inward"
(`corpus/README.md` §Frontier; S010-style perturbation audit on grader outputs). Today every stored probe
verdict is re-derived from `raw` by `extract_json_block` + `grade_state`/`grade_seq` (`grader.py:121`, `:221`,
`:2115`; replay at `:367`, `:1006`, `:2489`), but nothing measures whether those verdicts depend on response
*format* rather than content.

Frozen population P1 (sha256-pinned in the instrument): every record in
`corpus/evidence/round8-horizon/results.jsonl`, `round9-replication/results-r9.jsonl`,
`round11-power/results-r11.jsonl`, `round12-ladder/results-r12.jsonl` (base bytes) that carries `raw` and a
stored `ok` and whose verdict the instrument's baseline re-grade reproduces exactly (graders: `grade_state`
for dict states, `grade_seq` for r12 family-2 lists, `grade_c` for r8 C-cells). Records whose baseline does
not reproduce are counted and excluded, never perturbed. The truth/want for each record is taken exactly as
`grader.py` takes it (stored `want` cross-checked against meta truth).

Perturbation families (applied to `raw`; the extracted object is the one the baseline grader extracted):

| id | family | intent | expected behaviour of a format-robust grader |
|---|---|---|---|
| F1 | strip the code fence (keep the JSON text) | meaning-preserving | verdict unchanged |
| F2 | relabel the fence (```` ```json ```` → ```` ```JSON ````) | meaning-preserving | unchanged |
| F3 | re-serialize the extracted JSON compact ↔ indented (same object) | meaning-preserving | unchanged |
| F4 | reverse key order of the extracted object (dicts only) | meaning-preserving | unchanged |
| F5 | prepend a one-line prose lead-in with no brackets | meaning-preserving | unchanged |
| F6 | append a one-line prose sign-off with no brackets | meaning-preserving | unchanged |
| F7 | CRLF line endings | meaning-preserving | unchanged |
| D1 | append a second fenced JSON block restating the *previous* turn's truth as "for reference" | meaning-preserving for a human reader, adversarial for a last-block extractor | unchanged |
| G1 | change one value of the extracted answer (int +1 / list element swapped for a distinct token) | meaning-changing | a baseline-PASS record must become FAIL |
| G2 | delete one key / element from the extracted answer | meaning-changing | a baseline-PASS record must become FAIL |

Metrics: per MP family (F1–F7, D1) **invariance** = records whose re-graded `ok` equals baseline / records the
family applies to; per MC family (G1, G2) **sensitivity** = baseline-PASS records re-graded FAIL / baseline-PASS
records. Each with the exact two-sided 95% Clopper–Pearson interval (reuse `clopper_pearson` from
`plans/attrib_calibration.py`, round 25) and a verdict against bar **0.95**: PASS if CP95 lower ≥ 0.95, FAIL if
CP95 upper < 0.95, else INDETERMINATE; a family applicable to 0 records is UNTESTED (QUALITY Q11/Q12).

Instrument: `plans/grader_perturb.py` (stdlib, offline; imports grader functions from `grader.py`; never
contacts an endpoint). CLI `python3 plans/grader_perturb.py [--root DIR] [--summary|--json] [--selftest]`;
exit 0 = ran, population pins match and baseline reproduces; 1 = pin/baseline inconsistency or selftest
failure; 2 = usage. A FAIL family is a finding, not an error. An independent oracle (separate code path,
`plans/fixtures/r26/`) must reproduce every per-family count.

Counting command (C1): before — the widened sweep `grep -rnE 'perturb|metamorph' grader.py plans/*.py corpus/knowledge`
hits 4 files at base (receipt `corpus/evidence/round26-calibration/round-start.txt`), none of them this construct:
`grader.py:4351-4362` `_perturb_dict`/`_perturb_list` mutate *synthetic* answers for the grader's own selftest
fixtures (plus one synthetic bare-brace fallback fixture, `:4478`); `grader.py:5130-5226` perturb stored
*analysis numbers* (mutation self-checks M40–M78); `plans/attrib_calibration.py:993` perturbs a CP anchor;
`knowledge/llm-judge-calibration.md:25-27,89` and `bench-arena-round11-power.md:91` describe *others'*
perturbations. So the before-state is: **0 per-family invariance or sensitivity rates measured over stored model
responses** (the instrument is absent: `git cat-file -e f11bffbf:plans/grader_perturb.py` fails, exit 128);
after — `python3 plans/grader_perturb.py --summary`, observable = perturbation-audited stored-response verdicts
(family × record) and the number of families carrying an interval verdict (0 → 10).

Rubric legs (`SCORECARD.md:244`): (a) a construct the lane could not previously observe — measured by the
before sweep; (b) instrument in-repo; (c) prior-art verdict with fetched URLs, **including tooling registries**
(PyPI, GitHub) per round-25 M38, searched *before* the +1 is claimed. If the construct is published as method
or tooling (e.g. CheckList INV tests, metamorphic testing of graders, perturbation suites), novelty is held at 7
and the observable is recorded (the r24/r25 ruling: a held score stands when the declared observable moved).

Sourced: the C1 knowledge entry (`corpus/knowledge/grader-perturbation-audit.md`, drafted outside `corpus/`
until Q13 holds) cites SOURCES rows opened this round.

### Predictions (filed before any instrument output; scored at close; probability that the family's verdict is PASS)

These are reasoned from the extractor code (`grader.py:121-134`), so they are **code-derivable forecasts**, not
blind ones (round-25 CritBrierHonesty); no calibration credit is taken from their score.

| id | event | p(PASS) |
|---|---|---|
| P1 | F1 fence-strip invariance PASS | 0.75 |
| P2 | F2 fence-relabel invariance PASS | 0.85 |
| P3 | F3 re-serialize invariance PASS | 0.95 |
| P4 | F4 key-order invariance PASS | 0.97 |
| P5 | F5 prose lead-in invariance PASS | 0.95 |
| P6 | F6 prose sign-off invariance PASS | 0.95 |
| P7 | F7 CRLF invariance PASS | 0.90 |
| P8 | D1 distractor-block invariance PASS | 0.03 |
| P9 | G1 one-value change sensitivity PASS | 0.97 |
| P10 | G2 deletion sensitivity PASS | 0.97 |

## C2 — calibration: state_check population extended to the lane's round-25 self-assertions, content-pinned

The round-25 closure found three stale self-assertions in the round's own new text (R26-E1–E3) that
`plans/state_check.py` could not see: the two new capability rows are `OUT_OF_POPULATION`, PROVINCE's
§Province-map counts are not in P2, and SHONEN/axis anchors are pinned by range, not content (only
`AXIS_ANCHOR_CONTENT = {":162": …}`).

Frozen population P3 (enumerated at base `f11bffbf`, ids fixed in the instrument; anything added after base is
out of population):
- **P3a** the two round-25 capability cells (`interval-reverdict`, `state-assertion-check`): every numeric
  token in each cell compared with the committed receipt it names (`attrib-calibration-summary-v2.txt`,
  `attrib-calibration-selftest-v2.txt`, `state-check-before-6180e4f-v2.txt`, `state-check-after-v2.txt`).
- **P3b** PROVINCE §Province map count/outcome assertions: the "Public-literature registry" row (`:112`) and its
  round-25 correction (`:119`) against the SOURCES census at the measured tree; the two round-25 instrument rows
  (`:116`, `:117`) against their receipts.
- **P3c** content pins for every SHONEN evidence pointer: the target line must carry a frozen content token
  recorded at base (e.g. the cold-run verdict heading at `round-8-aggregator-box3-coldrun.md:48`).
- **P3d** content pins for every backticked `:NNN` anchor in the §Round 24 and §Round 25 re-derived axis tables.
- **P3e** the corpus/README index rows and files listed `OUT_OF_POPULATION` by the base run (round-25 entry,
  lessons, evidence dirs), both directions.

Supersession: a stale P3 assertion is closed only by an appended `R26-E*` correction carrying the full
re-derived value (the R25-E rule, regex widened to `R2[5-9]-E`).

Counting command (C2): `python3 plans/state_check.py --summary` (v3). Before = v3 run over the base tree
(`git archive f11bffbf | tar -x -C /tmp/kengaku-r26-base`), `mismatch` on P2∪P3; prediction: **≥3** (R26-E1–E3).
After = v3 on the landed tree: `mismatch=0` with each R26-E row counted `SUPERSEDED`. The v3 selftest must
show each P3 class red on a mutated fixture. The P2 results of v2 must stay identical under v3 on the base
tree (no silent re-scoping). Score: held at 8 unless the rubric's scored-probe leg is met (it is not this
round); the observable is the claim.

## Separability (QUALITY R13)

C1's population is the four probe result files; C2's is P3 enumerated at base. C1 adds files (instrument,
fixtures, knowledge entry, README rows, SOURCES rows) that are all out of P3 by construction; C2 changes
SCORECARD/PROVINCE correction rows and `plans/state_check.py`, none of which C1 counts. Revert test at close:
each claim's count re-run with the other claim's paths reverted must not move
(`corpus/evidence/round26-calibration/revert-test.txt`).

## Frontier step

SOURCES rows only after opening (URL, access date, ≤25-word located quote in
`corpus/evidence/round26-sources/gate.md`); prior-art search over papers **and** tooling registries; census
before/after via `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
(round start: `kengaku ok`, exit 0, one W04 warning). Mistakes mined into `corpus/lessons/round-26.md`
(M39 landing/future-dated evidence; M40 number-drift in round-25's own new text), each fix with a red run.

## Waves

Wave 1 build (64–100 seats) and wave 2 falsify (64–100 seats, after wave 1 returns and the instruments are
integrated); round total ≤ 200. Writers work only in private clones `/tmp/kengaku-r26-<Seat>`; KengakuR26-2 is
the sole integrator.

## Amendment 1 — after wave-1 output, before integration/admission (2026-10-21)

**Timing disclosure:** build seats already ran competing implementations and reported their counts. This is
not a pre-output amendment; no prediction is retrospectively rescored as ex ante. Motivating evidence:
`build/ExecFamilyEdges.md`, `CritD1Validity.md`, `CritIndependence.md`, `ExecPopulationManifest.md`,
`RevSeparability.md`, `CritPredictionsHonesty.md`, `SrcToolingPyPI.md`.

1. Population remains the same four byte-pinned files, exactly **1964** raw+ok records, **0 excluded**;
   mismatched baseline/pins or an unexpected exclusion exits 1. C-MONO uses `valid_latin`, labeled grader `c`
   with an explicit cell-specific branch; all other C cells use `grade_c`. Meta-derived want is checked, not
   accepted just because stored ok agrees.
2. F1/F2 act on **only the last matched answer fence**, leaving earlier fences in place; unmatched closing
   fences are not applicable. This is the informative narrow reading, not a move to maximize PASS. It
   exposes 17 PASS→FAIL flips among multi-block responses. F3/F4 serialize the parsed object, so duplicate
   JSON keys are resolved before key reversal. G1/G2 require baseline PASS and change an actually graded
   value, not an ignored extra key or an equal-token swap.
3. D1 is **PC (policy-conformance)**, not MP or evidence of a grader defect. Apply only to baseline-PASS
   ordinary state/sequence operation records with turn>1, excluding A-MONO, B and C, where previous truth
   differs from want. k counts the extractor capturing the appended previous truth, not invariance of
   model correctness. A PASS says the last-block policy was followed; do not mix it into robustness.
4. Keep nominal per-record CP95 against bar 0.95 as the registered descriptive reference, **not** an iid
   generalization guarantee. Print format strata FJ1/FJM/MULTI/DANGLE/BARE and pid-composite worst-case
   sensitivity (file+pid, C file+cell+rep), and raw+want duplication. Pooled PASS never erases a failing
   stratum. F1/F2 on the MULTI stratum are a concrete observed counterexample, not proof about future inputs.
5. P1–P10 are **code-derived expectations**, not blind forecasts. Preserve filed probabilities as history;
   no Brier score, hit rate or calibration credit. The ten audit families measure scoped behavior, not ten
   independent empirical discoveries.
6. Prior art: evalmut 0.1.0 (S045; PyPI release and GitHub opened) directly ships equivalent and defect
   response mutations against answer graders. Novelty held **7**, not +1. C1's finite-corpus observable
   remains independently verifiable; this is a lane-specific instantiation, not a new method.
7. P3b's dated census is **S001–S042 with exact id-set verification**, not total rows at round-26 tip.
   New C1 sources S043+ are outside it. P3e is the exact base-frozen path list, never a live expanded glob.
   Strict P3d means anchors **inside axis tables** (only `:162`); anchors in surrounding prose are listed
   as outside this claim. The wider D14 `:305` drift is already corrected by R25-E3, not silently counted.
8. Q13's red at `8ea41f9` is specifically missing named report support (also red at later round-25 tip);
   tree counts and a controlled late-report/same-commit fixture establish timing. Require actual registered,
   nonempty reviewer-like reports, candidate mentions, verdict lines and a candidate writer identity.
   Q13 checks structural support only; it never interprets a contradictory review as approval.
9. Base v3 has **5 mismatches** (two capability values, two dated PROVINCE row counts, unindexed round-25
   outside spot-check). The first four are routed repairs, not discoveries. C2 is an observability move,
   calibration score held **8**; it does not claim all current-state assertions are now covered.

## Amendment 2 — metric accounting after Amendment-1 implementation (2026-10-21)

The amended core and independent oracle agree on F1/F2 1802/1819 and D1 capture 909/909.
Removing D1 from MP also removes it from the robustness-verdict denominator: C1 now measures
**0 → 9 MP/MC interval-verdict families**, **0 → 15168 audited verdicts**, plus **909 separately
NOT_SCORED policy checks**. This supersedes the original “0 → 10” interval-verdict target, not by
dropping a failed family: D1 remains present as PC with its rate/interval, and its original FAIL is retained
in build evidence. The construct separation was required by task-defined polarity (M42), not score gain.
F1/F2 pooled PASS does not erase MULTI 14/31 or pid-composite 187/194 INDETERMINATE. C1 score held7.
