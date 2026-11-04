# EntryFalsifyR73 — round 73 w1, role reviewer

Seat verdict on the held knowledge entry `corpus/knowledge/tb2-hf-model-inference-offline.md`
(`admission: hold`, :6, writer `KnowledgeEntryDraft`). Full review with the line-by-line test:
`corpus/evidence/round73/w1/entry-hold-review.md` (the item's assigned evidence write; the only
lane file this seat wrote).

## Verdict: `hold`

**Deciding line: Q13/Q14.** The admission bar (`corpus/QUALITY.md`, `## Admission bar`) is
conjunctive; the entry's bytes clear every byte-level row (Q1 triad at :1-3, Q2 tier-A rows
S245/S246 at `corpus/SOURCES.md:260-261`, Q3 anchored claims, Q4 limits + falsifier at
:206-239, Q5 labelling at :237-239, Q6 extends at :241-245, Q7 index rows at
`corpus/README.md:95,460`, Q21 pin in `recheck:` at :3), but the process row fails: no returned
second-seat re-read from a `falsify`/`wave[-_ ]?2` directory exists in rounds 71, 72 or 73
(each dispatched `w1` only — wave dirs listed 2026-11-03), and the lane's own gate prints the
red at the reviewed tip:

```
$ python3 plans/gate_timing_check.py --lesson corpus/lessons/round-71.md --commit master
gate_timing_check: FAIL: no admit rows in ## Gate of corpus/lessons/round-71.md at master
gate_timing_check: admissions=0 passed=0 failed=1
rc=1
```

Discharge evidence (exactly): one report from a Q14-role seat ≠ `KnowledgeEntryDraft` under a
w2 directory, re-opening S245/S246 and re-reading every quote location/number, cited by
repo-relative path in the admitting lesson's `## Gate`, committed in the admitting commit's
tree, `gate_timing_check` rc 0. The round-71 lesson promised this for round 72; round 72
shipped one wave and its lesson records the miss ("No `w2`/`falsify` directory exists at draft
time"); round-73's frozen non-claim 3 pre-commits the hold again. Next round must add the w2
report — the byte-level work is done.

## Findings

1. **(the verdict, above)** `hold` — Q13/Q14; bytes pass, process row fails.
2. **Minor — record imprecision in the frozen claims doc.** `plans/round-73-claims.md`
   non-claim 3 names `corpus/knowledge/tb2-hf-model-inference-offline.md` but calls it "the
   round-72 knowledge entry"; the named file is the round-71 entry (hold recorded in
   `corpus/lessons/round-71.md` `## Gate`). The round-72 entry is
   `tb2-hf-model-inference-provenance.md` (writer `KengakuR72`), also on hold under the same
   gate. The non-claim's operative fact is true for the named path; the round label is off by
   one. Frozen doc — finding, not an edit.
3. **Minor — the item's "2–4 seat falsify second wave" plan is not in the committed record.**
   Searched `plans/round-72-claims.md`, `corpus/lessons/round-72.md`, `LOG.md` round-72
   section, `.ufo/waves/round-72/w1-spec.json`: round-71's lesson carries the one-line promise
   ("Round 72 dispatches the falsify wave that admits the entry") but no committed byte states
   a seat count for it. The checkable fact — no second wave in rounds 71-73 — is verified.
4. **Informational — the hold is now a two-round-old promise slipping to a third.** The entry
   is indexed (`corpus/README.md:95`) and built upon (the round-72 provenance entry extends it)
   while formally unadmitted; the gate is doing its job, but a round that wants the corpus
   consistent should either dispatch the falsify wave or record the slip as open debt in the
   lesson.

## What was run (all read-only; no git mutation)

- `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-71.md --commit master` →
  rc 1, `no admit rows … failed=1` (the measured red behind the verdict).
- `sha256sum` both captures → `29151c5b…dcc1` / `61a686d6…87857` (match :1-2); `wc -lc` grader
  → `107 4239` (match :11-12).
- Three instruction probes `grep -c` → `0 0 0` (matches :45-49); `grep -c 'executed 4 of 8'
  SKILL.md` → `1`, `'executed 3 of 8'` → `0` (class row as claimed at :201-204); the six
  literals verbatim at `test_outputs.py:36-44` including text 2's split.
- Wave-dir listings for rounds 71/72/73: `w1` only in each.

## Residual risk / gaps

- This seat did not re-verify every number in the entry against the captures — that full
  re-read **is** Q10, the very artefact whose absence is the hold; producing it from a w1
  reviewer seat would not satisfy Q13's directory/timing gate and could mislead the L1 into
  reading the hold as discharged. The four cheap spot-checks above are recorded as
  spot-checks, not as the second-seat re-read.
- The `.ufo/waves/round-72/w1-results.json` blob was sampled, not exhaustively searched, for a
  planned-w2 mention; finding 3 is bounded by the four named committed sources.

Scratch `/fast/scratch/hyaku/kengaku-r73/EntryFalsifyR73` was created and removed empty; no
tools installed; no pacman transaction.
