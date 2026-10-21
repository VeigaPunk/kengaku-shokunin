# ExecGateTimingCheck — Q13 implementation

- **Scope:** `plans/gate_timing_check.py` in `/tmp/kengaku-r26-ExecGateTimingCheck-4`; clone base observed `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`. No live lane code was edited.
- **Behavior:** reads lesson and wave tree as of the supplied commit (`git show`, `git ls-tree`); parses every `## Gate` admit; handles arbitrary lesson basenames by round-path/heading inference and corpus-relative candidate paths. A cite qualifies only if it resolves to a nonempty regular second-wave report, registered as a wave member outside scribe/executor roles, naming the candidate, containing an anchored `VERDICT:` line to establish return, and not matching the candidate's committed `writer:`. Any generic reference or unresolved bare report cite fails the admit. Exit 1 for failed admissions; input/usage errors exit 2. Main logic: `plans/gate_timing_check.py:129-180,187-228,269-362,365-382,455-534,537-622`.
- **Q10 source:** `corpus/lessons/round-25.md:27-29`; the admit reason cites only “by wave-2 seats”.

## Retained command evidence

`python3 plans/gate_timing_check.py --selftest` — exit **0**:
```text
[selftest] ALL PASS (arbitrary lesson basename, generic-only/variant red, explicit/bare citation, missing/unresolved citation, registry/mode/return/self-review/unknown-writer checks)
```

`python3 plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 8ea41f9` — exit **1**:
```text
FAIL line 29 Gate admit: candidate='knowledge/attribution-interval-calibration.md'
  cell[reason]: Q1 triad first; Q2 every load-bearing claim on tier-A rows S027–S030/S033/S034/S011 or own-work S036/S037; Q3 quotes ≤25 words with locations (`corpus/evidence/round25-sources/gate.md`); Q4 "What this does not establish" names clustering, journal GT, derived specificity, dedup undercount, unopened primaries and a falsifier; Q5 abstract-only and author/repository copies labelled in the rows; Q6 extends `attrib-r21.md` and `llm-judge-calibration.md`; Q7 index and coverage-map rows land in the same commit; Q8 two rejections below; Q10 numbers re-derived by a second parser (`plans/fixtures/r25/attrib_oracle.sh`) and by wave-2 seats
  cited seat-report paths: none
  generic seat reference(s) (not report support): 'wave-2 seats'
  missing: no .ufo/waves/round-25/falsify/ report exists in commit 8ea41f9
  reasons: no cited, existing, returned second-seat report for this round; generic seat references are not report evidence
gate_timing_check: commit=8ea41f9 lesson=corpus/lessons/round-25.md admissions=1 passed=0 failed=1 second-seat-reports=0
```

`python3 plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 9d8a00d` — exit **1**:
```text
FAIL line 29 Gate admit: candidate='knowledge/attribution-interval-calibration.md'
  cell[reason]: Q1 triad first; Q2 every load-bearing claim on tier-A rows S027–S030/S033/S034/S011 or own-work S036/S037; Q3 quotes ≤25 words with locations (`corpus/evidence/round25-sources/gate.md`); Q4 "What this does not establish" names clustering, journal GT, derived specificity, dedup undercount, unopened primaries and a falsifier; Q5 abstract-only and author/repository copies labelled in the rows; Q6 extends `attrib-r21.md` and `llm-judge-calibration.md`; Q7 index and coverage-map rows land in the same commit; Q8 two rejections below; Q10 numbers re-derived by a second parser (`plans/fixtures/r25/attrib_oracle.sh`) and by wave-2 seats
  cited seat-report paths: none
  generic seat reference(s) (not report support): 'wave-2 seats'
  missing: Gate does not name a valid second-seat report by path; the commit has 87 second-seat report(s)
  reasons: no cited, existing, returned second-seat report for this round; generic seat references are not report evidence
gate_timing_check: commit=9d8a00d lesson=corpus/lessons/round-25.md admissions=1 passed=0 failed=1 second-seat-reports=87
```

## Files, risks, blockers

- **Private clone file:** `plans/gate_timing_check.py` — SHA-256 `4a270d3ca31ddd64b829a079f96aadfad088e97c9b197630d0c31ede0a138512`.
- **Lane report:** `.ufo/waves/round-26/build/ExecGateTimingCheck.md`.
- **Risk:** round-25 tip remains red because its Gate cites generic seats and no report path. Its knowledge entry has no `writer:` field, so explicit report evidence fails closed; when present, the committed field remains self-asserted because no independent writer-identity authority is available. The checker does not decide whether a report's verdict is substantively resolved or enumerate uncited wave prompts; those exceed the frozen Q13 timing interface.
- **Blockers:** none for the requested implementation. LSP is not mounted; this new module introduces no existing-symbol refactor.

Installs: none.

VERDICT: Q13 checker implemented in the private clone; required selftest and red-before/tip commands produced the recorded outcomes.
