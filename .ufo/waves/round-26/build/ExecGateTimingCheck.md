# ExecGateTimingCheck — Q13 implementation

- **Scope:** `plans/gate_timing_check.py` in `/tmp/kengaku-r26-ExecGateTimingCheck-4`; clone base observed `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`. No live lane code was edited.
- **Behavior:** reads lesson/tree at the supplied commit; handles arbitrary lesson basenames and corpus-relative candidates. Only second-wave reports registered with roles `reviewer`, `scout`, `critic`, `sentinel`, or `revenger` qualify. It rejects generic/unresolved citations, report `writer:`/`author:` declarations or registry `agentId` matching the candidate writer, and missing writer metadata on the candidate. If a report omits writer/author declarations, identity checks rely on seat name and registry `agentId`, not proof of human authorship. In-memory cases cover role and writer conflicts. Code: `plans/gate_timing_check.py`.
- **Q10 source:** `corpus/lessons/round-25.md:27-29`; the admit reason cites only “by wave-2 seats”.

## Retained command evidence

`python3 plans/gate_timing_check.py --selftest` — exit **0**:
```text
[selftest] ALL PASS (five allowed roles; connector/mutation-tester/simplifier and unknown roles rejected; declared writer/author/agentId conflicts red; missing report identity with registered reader green)
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

- **Private clone file:** `plans/gate_timing_check.py` — SHA-256 `1b748e52a35a5bd900462cd34d0cc3660d06a770b8d06cf05e22b348c4b3f69d`.
- **Lane report:** `.ufo/waves/round-26/build/ExecGateTimingCheck.md`.
- **Risk:** round-25 tip remains red because its Gate cites generic seats and no report path. Its knowledge entry has no `writer:` field, so explicit report evidence fails closed. When report writer/author metadata is absent, the checker uses committed seat name and `agentId`; this is not proof of human authorship. Verdict disposition and uncited-prompt completeness remain outside the timing interface.
- **Blockers:** none for the requested implementation. LSP is not mounted; this new module introduces no existing-symbol refactor.

Installs: none.

VERDICT: Q13 checker hardening complete; in-memory role and writer-conflict selftest passed.
