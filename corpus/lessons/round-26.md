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

### Source-location correction before admission (2026-10-21)

S048 supersedes S043's location, not its teaching. Independently reopened URL
https://aclanthology.org/2020.acl-main.442.pdf on 2026-10-21, SHA-256
98d15d259acf15136feed5cd5d4921b60cf313704a629901d115fe910fdb00e1.
Located quote (21 words): “An Invariance test (INV) is when we apply label-preserving perturbations to inputs
and expect the model prediction to remain the same.” Location: **§2.2, PDF p.3 / proceedings p.4904**,
not the p.2 / p.4903 printed in the initial Gate above. The re-read in
`.ufo/waves/round-26/falsify/FxSourceCheckList.md` caught this while the entry was still unadmitted.
The draft now cites S048; the historical S043 row/initial Gate stay as written and are superseded here.

### Admission after returned correction rereads (2026-10-21)

This supersedes the initial deferred decision, not its history. All cited reports have returned.
The complete reviewer re-opened the sources and counts, then actually re-read the corrected F1/F2 and
CP95 table; its original FAIL and final scoped PASS are both preserved. Q7 and Q13/14 are checked on the
prospective packaged tree before the real admission, then on the actual landed revision.

| candidate | decision | reason |
|---|---|---|
| `knowledge/grader-perturbation-audit.md` | **admit** | Q1 anchored triad/writer; Q2 scoped A/B sources; Q3 located short quotes; Q4 finite-population limits/falsifier; Q5 tooling self-report labelled; Q6 existing Judge calibration extended; Q7 entry/index/new coverage row together; Q8/Q9 rejects retained and checked; Q11/Q12 exact nominal lower bounds shown, D1 NOT_SCORED. Q10 complete/source/number rereads: `.ufo/waves/round-26/falsify/FxEntryAll.md`, `.ufo/waves/round-26/falsify/FxEntryNumbers.md`, `.ufo/waves/round-26/falsify/FxSourceCheckList.md`; Q13/Q14 structural support names those exact returned readers. FxEntryAll re-opened every load-bearing external source and independently rederived all counts, then re-read the corrected draft. Original PARTIAL/FAIL findings are resolved by the named pre-admission corrections, not recast as unconditional approvals. |

Source used-by changes logged old→new (no status/recheck changes): S044, S045, S046, S048 each
`corpus/lessons/round-26.md` → `corpus/lessons/round-26.md, corpus/knowledge/grader-perturbation-audit.md`.
S043/S047 remain lesson-only. S048 is a sixth added row (fifth tierA row plus one tierB across S043–S048),
not an additional external publication. The source-inventory support row's initial S043–S047 range is
superseded by **S043–S048**. Outside non-author spot-check is still the orchestrator's closure, not these seats.

## Wave record

Build: 72 distinct seats, one validated payload; 22 scout, 14 executor, 12 reviewer, 6 connector, 6 critic,
6 scribe, 4 revenger, 1 sentinel, 1 simplifier. L1 held planner. Three complete refusal attempts (72/72
unstarted each) preceded the successful unchanged dispatch at 03:50:27 -03; all 72 reports returned.
Initial 80-seat spec was reduced before any dispatch after Main's 64–72 packing instruction; no seat was
replaced. `.ufo/waves/round-26/build-dispatch-log.txt`, `build-assignments.json`, registry and all reports
are retained. `plans/state_check.cover` was trace scaffolding left by a build seat and removed; no permanent
coverage artifact is claimed.

## Mistakes — falsify addendum

| id | class | mistake and red evidence | captured-by | correction |
|---|---|---|---|---|
| M45 | reference-drift | S043 INV location off by one page; `falsify/FxSourceCheckList.md` independently found quote at p.4904, not p.4903 | Q10 ran before admission this time | S048 plus Gate/source-receipt errata; source seat re-read corrected draft and passed its scoped criterion |
| M46 | vacuous | four transform mutants survived selftest: F2 CRLF, D1 seq eligibility, G1 first-fence selection, G2 list no-op (`FxMutF2`, `FxMutD1`, `FxMutG1`, `FxMutG2`) | family-only selftests omitted branches | explicit CRLF/seq/multi/C/Latin-square cases; restored-script and mutant receipts in build/ExecPerturbCore.md |
| M47 | vacuous | P3a/P3b comparison deletions, P3c whole-file token removal and P3e spotcheck-path/file-existence regressions survived selftest (`FxMutP3A/B/C/E`, `FxP3EIndex`) | one mutation per class was insufficient | expected assertion-ID inventories, specific branch controls and deleted-file checks in v3 selftest |
| M48 | number-drift | correction code spans carried unrelated citations, then omitted the exact-ID-set token; `FxP3BInstruments`/`FxRepairRows` found two mismatches | exact-token contract correctly refused partial restatement | SCORECARD E5/E6 and PROVINCE E9/E10 carry only full derived value tokens; E7/E8 are superseded |
| M49 | landing | roleless/unsupported readers and contradictory declared authors could satisfy structural support (`FxGateGeneric`, `FxGatePlaceholder`, `FxGateWriter`) | Q13 “reviewer-like” was underspecified | Q14 explicit five-role allowlist and declared identity-conflict checks; no claim of cryptographic authorship or automatic admission-commit discovery |
| M50 | landing | validator retained eight null-id members from the abandoned pre-trim 80-seat draft (`FxRegistry`) | cumulative registry reuse | old registry retained as swarm-registry-pretrim-superseded.json; fresh render on final72 spec gives byte-equal taskCall and 72 assigned active members; no respawn |
| M51 | scope | independent oracle preserved F3 format rather than toggling it, and had out-of-population F1/F2/F4/F7 applicability differences (`FxFamilyF1/F2/F3/F4/F7`) | frozen aggregate counts alone did not test exact transform semantics | independent oracle corrected to Amendment-1 transform semantics; frozen counts retained, edge controls added |
| M52 | vacuous | G1 fixed replacement token could equal an existing string, so a generic-input mutation could be semantic no-op (`FxFamilyG1`) | frozen corpus did not contain that token | collision-safe alternate token and explicit G1-SEQ-COLLISION selftest; frozen count unchanged |

### R26-E11 — report-count units (supersedes R26-E4's 0/83/87 phrasing)

`FxRepairRows.md` distinguishes raw tree entries **0/83/88** from Markdown seat reports **0/82/87**
at `8ea41f9` / `8239a56` / `9d8a00d`. The first report landing held 82 reports plus its registry, not
83 reports. The historical absence at the admit commit is unchanged. Counting command:
`git ls-tree -r --name-only REV -- .ufo/waves/round-25/falsify/`, count all entries versus names ending `.md`.
This addendum supersedes the earlier lesson's “83” report wording and any pre-registration timing paraphrase.

### Falsify dispositions before admission

64 distinct seats dispatched in one validated call; role mix 39 reviewer, 10 mutation-tester, 7 scout,
4 critic, 2 executor, 2 connector. Eleven failed with the recorded Codex capacity error and were never
replaced; 53 report-bearing returns plus the failure record account for all64. L1 performs dead seats'
reachable residual checks. The two inherited waves total **136 unique dispatched seats**; three recovery
reviewers bring the round-wide total to **139**. Same-identity follow-ups did not add replacement seats.
Dead names and exact errors: `.ufo/waves/round-26/falsify-dead-seats.json`.

- The three Gate rejections survived `FxEntryRejects`; their reasons/flips remain.
- S044/S045/S047 source sentences survive re-open. Python docs are dynamic: current byte hash may differ;
  `FxSourceSelftest` re-opened the quote and confirmed it. A differing dynamic-page hash is not a false quote.
- S045's README anchor already covers both Blind spot and Brittle spot bullets. The draft triad adds the
  defect code locator (operators.py:255–328) beside equivalent code (:614–726); no immutable row is rewritten.
- `FxEntryProvenance`'s source-anchor correction was reported, not independently re-opened by that seat;
  it is not counted as a new complete re-read. The complete reviewer and actual source-opening seats are
  the Q10 evidence, never outside non-author closure.
- Fixture generator now includes registry/mention/verdict metadata and an explicit round26 generic-only
  heading, so its green and negative cases test the intended gate rather than setup failure.
- Strict P3d covers the actual axis-table anchor, not surrounding prose anchors. Cold-run heading pins
  do not prove current executability. New round26 assertions remain outside frozen P2/P3.
- Trace-cold state-check branches were not deleted: trace absence is not proof of dead generic code.
  Removing the live `find_protocol` path would break fleet drift checking; no cleanup score is claimed.

### Recovery disposition (same round/attempt, 2026-10-21)

KengakuR26 resumed KengakuR26-2's incomplete close at branch tip `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`;
the 72+64-seat waves are inherited, not newly dispatched. Three bounded read-only recovery reviewers
inspect the final package; no failed seat is replaced. No operator teaching file exists in this lane's
`corpus/lessons/operator-*` glob at recovery. Source S046 was re-opened by recovery L1; the located
Unicode-whitespace quote still includes CR (`corpus/evidence/round26-calibration/recovery-start.txt`).

| id | class | mistake · evidence | captured-by | fix |
|---|---|---|---|---|
| M53 | landing | inherited uncommitted knowledge copy still lacked the corrected draft's F1 definition and pooled CP95 lower-bound columns although FxEntryAll had re-read the corrected draft | Q10/Q13 require the reviewed candidate, not an earlier copied version | before admission, copied those exact reviewed spans into the candidate; the edit tool reports identical content snapshot hash `3A3A` for draft and candidate; recovery timing review checks the final candidate |

This is a pre-admission recovery fix, not an erratum to a landed knowledge entry. The original r25
landing failure is not repeated or relabeled as admitted. Fleet misroot sweep found driver-runtime
paths only; none was moved, deleted or committed. No tool install or update was performed.

Recovery reader-identity correction: `falsify/FxEntryRejects.md` retains its Q9 rejection-rationale
advice, but is not Q10/Q13/Q14 second-seat support: it explicitly declares the candidate writer's
identity. Removed that citation from the admitting Gate cell before admission.

The Gate's final qualifying set is FxEntryAll, FxEntryNumbers and FxSourceCheckList. FxFamilyD1,
FxSourceXFinder, FxSourceEvalmut and FxSourceSelftest remain bounded source/number evidence outside
the admitting cell: they reference a draft or basename, not the canonical candidate path required
by the structural gate. FxEntryAll itself covers all those sources and D1 counts. This narrows the
support list without weakening the Q10 complete re-read or misrepresenting report identities.

### Final suite and inherited-tail integration

The earlier worker's final `plans/state_check.py` artifact was not yet integrated. Recovery L1 reviewed
its full delta and installed the exact documented SHA-256
`32a684ffcb3fb222b0360333f83c2e4654c19ec1c3ad6ed47016052401428089`; P2 keyed records remain identical
to v2 on `f11bffbf` (`corpus/evidence/round26-calibration/p2-preservation.txt`). Two ordinary executor
dispatch attempts were refused at job cap100 (no new seat), separated by `sleep 180`; L1 integrated it
without replacing a dead wave seat.

| id | class | mistake · evidence | captured-by | fix and observed red/green |
|---|---|---|---|---|
| M54 | vacuous | P3 oracle selftest R8/R9/R10 inherited an already-valid correction in its scratch template; the intended negative controls stayed green | final L1 suite | remove only the target's inherited correction rows from the scratch template; `p3-oracle-selftest-final.txt` is red (14 checks, 3 failed), identical command after the sole fixture-setup change is green (14/14), `p3-oracle-selftest-repaired.txt` |

Final measured C1: 1964 candidates, 0 exclusions, 15168 MP/MC comparisons over nine interval-bearing
families, 909 separate policy captures. Selftest caught12 mutants; 278 synthetic cases had0 failures.
C2: v3 base `assertions=278 match=269 mismatch=5 superseded=1 offline_unverifiable=3`, exit1;
after `assertions=278 match=270 mismatch=0 superseded=5 offline_unverifiable=3`, exit0.
Independent P3 oracle has63 registered assertions,58 match,4 superseded,1 UNVERIFIED (no exit2
receipt); its two extension-only historical-range findings are already marked by README errata,
not silently included in the registered population. Separability compares C1 FAMILY/TOTAL records
and C2 summary/exit, unchanged both directions. Full keyed P2 and P3b S048-addition controls pass.
All receipts: `corpus/evidence/round26-calibration/`; no outside-admission verdict is claimed.
