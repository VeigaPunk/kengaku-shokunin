# R43 connector — frontier/coverage check

## Axes

Coverage is the relevant declared axis (frozen round-43 claim selects coverage); adjacency is a constraint: keep runtime task validity, contamination, and benchmark execution out of kengaku's ownership. The claim does not assert a novelty move.

## Evidence and ruling

- The frozen claim identifies a distinct candidate ground: the submitted artifact is a Python module imported by the grader into its own interpreter beside a reference extension, then called to produce the answer. Frozen claims §C2, lines 85–95; specifically `feal_probe`/grader facts are at lines 92–95. The reference extension exposes the answer via `get_keys()` and the grader calls `attack.attack(feal_in_c.encrypt)` before comparing the returned value to the key (frozen claims lines 92–95; detailed frozen grader facts §C2 lines 87–95).
- This is **not** an entirely new umbrella beyond grader semantics or “agent code in-process”: the README already has eight admitted TB2 task graders, including `regex-log`, whose graded artifact is an agent-authored regex compiled/executed in process (corpus/README.md:69). The precise new edge is **agent-authored Python-module import and call in the grader interpreter alongside a reference module**, not the broader phrase “agent code in-process.” This is the ninth grader instance / an unheld mechanism-class ground, conditional on C2 admission; the frozen claim explicitly calls it a ninth grader class (round-43-claims.md:85–95).
- The frontier clause that narrows is the **Terminal-Bench 2.0 scoring-code** clause under `Agentic benchmark task-spec audits`, specifically the “other TB2 task graders” remainder. The extant chain says eight of 89 had been read and leaves the remaining TB2 graders open (corpus/README.md:362–376). On C2 admission it should read: “This round-43 entry covers `feal-differential-cryptanalysis` only: an agent-authored Python module imported and called inside the grader's interpreter beside `feal_in_c`; it does not establish agent-code-in-process generally, task validity, benchmark/image execution, or model performance. The remaining 80 of 89 TB2 task graders' scoring code remains open.” Keep unrelated clauses (SWE-bench Pro V2 graders, runtime task validity, contamination, hosted judges) open. `regex-log` was already the important boundary: its regex runs in-process, so do not claim the broad in-process category as new (README:69; claims:95).
- `PROVINCE.md` has an outdated Frontier summary: lines 123–127 still names “agentic benchmark task-spec audits” as unopened leads, despite subsequent explicit partial admissions documented in README lines 292–376. Narrow that summary to the remaining scoring-code coverage and retain its explicit still-open runtime validity / contamination / hosted-judge scope. The current sentence is too broad, not evidence that the round-43 work is already admitted.

## Self-assessment mismatch census

**0 mismatching self-assessment lines** in the requested `SCORECARD.md`, `SHONEN.md`, and `README.md` as of this checkout.

- `SCORECARD.md`: no current-round statement claims a different TB2 grader count or that the round-43 candidate is already landed. Older round rows are historical measurements, not present-state census claims.
- `SHONEN.md:3–12`: its four promotion checklist attestations and pointers do not assert a TB2 count or C2 admission state.
- `corpus/README.md:271` and `362–376` correctly describe eight admitted graders and “8 of the 89” remaining at the end of round 42. The ninth item is still a frozen claim/build-stage candidate, not yet an admitted knowledge entry in this tree; changing that denominator before admission would be premature. Thus these are not mismatches now. On successful round-43 integration, update the count to nine read / 80 remaining and add its entry/index row; update PROVINCE's stale frontier summary at the same time.

Evidence anchors: frozen assignment `plans/round-43-claims.md:85–119`; coverage map `corpus/README.md:69,271`; frontier chronology `corpus/README.md:287–376`; province summary `PROVINCE.md:121–127`; promotion checklist `SHONEN.md:3–12`. No commands or counter runs were performed.

VERDICT: frontier-new-mismatches-0
