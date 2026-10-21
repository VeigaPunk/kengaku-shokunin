# Round 26 — repair-first; grader perturbations and content-pinned self-assertions

Round 26 attempt 1, hyaku block 25–34, L1 KengakuR26-2 (frozen planner seat).
Base `f11bffbf`; pre-registration `plans/round-26-claims.md` landed `e0037a8` before wave dispatch.
Round 25 remains REJECTED-HONEST-STOP; this round does not revise its outside adjudication.

## Mistakes

| id | class | mistake · evidence | captured-by | fix and failure-capable evidence |
|---|---|---|---|---|
| M39 | landing | `round-25.md:29` as landed at `8ea41f9` said Q10 numbers were checked "by wave-2 seats" before those reports existed; `git ls-tree -r 8ea41f9 -- .ufo/waves/round-25/falsify/` has 0 files; first reports committed `8239a56` | Q10 required before-admission timing but no command enforced it | Q13 plus `plans/gate_timing_check.py`; red at `8ea41f9` is missing named report support (also red at round-25 tip); a sandbox late-report/same-commit pair separately tests temporal presence |
| M40 | number-drift | round-25 new capability cells said selftest 14 instead of 18, base mismatches 11 instead of 10; PROVINCE correction said 37 registry rows instead of 42 at tip; outside spot-check `:96-105` | P2 intentionally excluded round-25 additions | R26-E1/E2 in SCORECARD, R26-E3a/b in PROVINCE; v3 on frozen base reports these four assertions MISMATCH; v2 could not see them |
| M41 | scope | frozen P2's PASS was not a census of the whole current tree: base has `OUT_OF_POPULATION` additions, including an unindexed round-25 outside spot-check | R12 did not state the population limitation where PASS was interpreted | P3 adds those fixed base assertions without changing P2; README gains the missing row; P3e red fixture deletes it |
| M42 | scope | C1 pre-registration treated D1 appended previous-state JSON as meaning-preserving; the original probes explicitly chose the last block, and D1's aggregate invariance mostly counted model baseline failures (`build/CritD1Validity.md`) | none | Amendment 1 labels D1 policy-conformance, excludes ambiguous cases, conditions on baseline PASS; no grader-defect claim follows from it |
| M43 | vacuous | F1 "the code fence" was ambiguous; stripping every fence masked 17 flips on the 31 multi-block B responses (`build/ExecFamilyEdges.md`) | no exact transform-span rule | Amendment 1 fixes the last matched answer fence as the transform span; multi-block stratum is printed separately; independent oracle must agree |
| M44 | survivor | pooled per-record CP95 would overstate generalization precision for repeated turns/pids and duplicated raw strings (`build/CritIndependence.md`) | Q11 alone does not justify an iid sampling model | nominal/descriptive finite-population intervals, format strata and pid-composite sensitivity; no independent-future-response coverage claim |

### R26-E4 — landing-time Gate erratum (appended 2026-10-21)

Supersedes `corpus/lessons/round-25.md:29`'s claim of completed checks "by wave-2 seats" at landing `8ea41f9`.
Those checks happened later. The source-location and reject-reason defects are already marked by M33/M34;
the outside expansion:harmed verdict stands. The round-25 spot-check's filesystem-mtime value is not used
as fresh proof: current copies have different mtimes. Durable tree evidence is 0 falsify reports at `8ea41f9`,
83 at first falsify landing `8239a56`, and 87 at round-25 close (`build/RevengeLandingTimeline.md`,
`build/ScribeQ13.md`). Generic "wave-2 seats" also lacks explicit paths even at the later tip.

## Gate

Admission bar: Q1–Q13. This section initially records **deferred**, not admit, for the round-26 draft;
no new knowledge file or knowledge index row is landed before its second-seat re-read is on record.

| candidate | decision | reason |
|---|---|---|
| grader-perturbation audit draft outside corpus | deferred | waiting for returned second-seat source/number/entry reviews; Q10/Q13 must precede admission |
| D1 appended previous-state block as a meaning-preserving robustness test | reject | conflicts with the registered last-block answer policy; measures baseline model error mixture; flip: a task contract declaring reference blocks semantically ignorable with independent polarity proof |
| novelty +1 for the perturbation method | reject | evalmut 0.1.0 already ships equivalent/defect response mutations against graders (S045); flip: a distinct construct beyond that published method, not this lane-specific population |
| pooled CP95 as a confidence guarantee for future independent responses | reject | deterministic transforms, duplicated raws, correlated turns and model-specific format mix; flip: a registered sampling model and independently sampled units |

Q13 is a structural timing/support check, not an endorsement interpreter: the author still resolves every
load-bearing reviewer finding under Q9/Q10. Lane-dispatched seats are advisory, not the outside non-author
spot-check of one admit and one reject; that belongs to the orchestrator closure.

### Sources opened this round (access date 2026-10-21 for every row)

| row | URL / path | location | quote (≤25 words) |
|---|---|---|---|
| S043 | https://aclanthology.org/2020.acl-main.442.pdf | ACL 2020 §2.2, PDF p.2 / p.4903 | “An Invariance test (INV) is when we apply label-preserving perturbations to inputs and expect the model prediction to remain the same.” |
| S044 | https://arxiv.org/pdf/2405.11874 | v3 (2025-02-25), Abstract, PDF p.1 | “As evaluation frameworks commonly use Regular Expression (RegEx) for answer extraction, models may adjust their responses to fit formats easily handled by RegEx.” |
| S045 | https://pypi.org/pypi/evalmut/json | 0.1.0 README §The two ways an eval lies, lines 61–63 in release tarball | “Inject an equivalent change (a trailing disclaimer after a complete answer, cosmetic whitespace, a JSON code fence); a sound grader must still pass it.” |
| S046 | https://docs.python.org/3/library/re.html | Python 3.15.0, Regular expression syntax, backslash-s | “This includes `[ \t\n\r\f\v]`” |
| S047 | corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt | final result line, f11bffbf | “selftest: 18 checks, 0 failed” |

Hashes, scope/tier rationale and bounded search counts are in `corpus/evidence/round26-sources/gate.md`.
S043–S046 teach the method/limits and S047 supersedes S037's stale selftest count; all are mined by this
lesson. New rows added only after opening. At this repair stage, used-by is solely `corpus/lessons/round-26.md`.

## Wave record

Build: 72 distinct seats, one validated payload; 22 scout, 14 executor, 12 reviewer, 6 connector, 6 critic,
6 scribe, 4 revenger, 1 sentinel, 1 simplifier. L1 held planner. Three complete refusal attempts (72/72
unstarted each) preceded the successful unchanged dispatch at 03:50:27 -03; all 72 reports returned.
Initial 80-seat spec was reduced before any dispatch after Main's 64–72 packing instruction; no seat was
replaced. `.ufo/waves/round-26/build-dispatch-log.txt`, `build-assignments.json`, registry and all reports
are retained. `plans/state_check.cover` was trace scaffolding left by a build seat and removed; no permanent
coverage artifact is claimed.
