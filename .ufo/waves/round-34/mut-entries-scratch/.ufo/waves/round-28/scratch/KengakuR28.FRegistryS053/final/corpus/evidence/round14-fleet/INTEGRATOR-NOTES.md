# Round-14 integrator notes — debt landing, adjudications, closeout

Owner: kengaku L1. L2 artifacts are retained verbatim; corrections live here,
`SCORECARD.md`, and `LOG.md`, never as silent rewrites of the r12/r13 evidence.

## Axis ruling

Lowest owned axis at the start was novelty 6. The round-12 evidence earns
**novelty 6→7** only when landed in round 14:

1. new-to-lane construct: a powered ordered four-arm density ladder, plus a
   batching/emission dissociation;
2. inspectable instrument: hashed bundle, probe/runner/recompute machinery,
   and four-tree replay gate;
3. fetched-URL pricing: C1/C2/C4/C5/C6 INCREMENTAL and C3 NOVEL-instrument.

The second-family contrast is directional at a 2/48 floor and corroborates
scope; it is not a separate novelty basis. Calibration holds at 8 because the
in-round landing clause was violated. Coverage holds at 7 because route
telemetry remains a declared unresolved surface. Operability 7→8 and freshness
7→8 are ancillary verified movements.

## Nine-agent batch

| Role | Artifact / landing | Accepted result |
|---|---|---|
| critic | `r14-critic-landed.md` | 25/28 REPRODUCE, 3 PARTIAL, 0 FALSIFY |
| reviewer | `r14-review-priorart.md` | 14 fetched URLs rechecked; 6/6 pricing verdicts survive |
| scout | `r14-scout-surfaces.md` | endpoint/process exact; bounty absent; bench tree relocated |
| connector | `r14-connector.md` | no sibling duplicate; two report-outs |
| mutation-tester | `r14-mutation.md` | S0–S7 pass; 4/4 fresh mutations killed |
| revenger | `r14-revenger-r13.md` | r13 scripts reproduce; G1–G6 landing gaps named |
| executor | `corpus/knowledge/bench-arena-round12-ladder.md`, `drafts/` | independent recomputation + corpus drafts |
| scribe | `r14-scribe-drafts.md` | quote-checked LOG/SCORECARD/README deltas |
| planner | `r14-landing-gate.md` | novelty +1 approved narrowly on C1; file dispositions audited |

## Adjudications and errata

1. **Analysis byte pin — fixed.** R12 drafts record stale md5 `ddfe60d2…` (and
   a third intermediate value). Landed `analysis_r12.md` is md5
   `029c3bcdcf11209d575734742bf239f6`; round 14 adds it to `R12_PINS`, taking
   the clean gate from 732 to 733 checks.
2. **Regeneration — partial.** A fresh analysis differs only at the absolute
   `Generator source` path (`projects` vs `Projects`). All statistics match.
   Keep the landed bytes; future generators must emit path-independent
   provenance.
3. **Ordering — partial.** Hashes at `01:16:08Z` strictly precede first request
   `01:19:59Z`. `main-run-launch` and first request both serialize at
   `01:19:59Z`; evidence proves nondecreasing order, not strict launch-before-
   request at subsecond resolution.
4. **McNemar labels — erratum.** Stored E2 says `b=12,c=5`; under the critic's
   explicit convention (b = 710 pass / 4710 fail), the orientation is
   `b=5,c=12`. The unordered pair and exact p=`0.1435` are unchanged; no verdict
   depends on orientation.
5. **Forecast denominator — erratum.** `r12-prior-art-transport.md` says 448
   pass events five times. Hashed plan amendment, prediction JSONL, and analysis
   establish 416 = 5×64 + 2×48.
6. **Mock wording — erratum.** `r12-review-citations.md` calls `/tmp` mock output
   committed. Only `mock_server_r12.py` landed. Mock/real separation and the
   real run remain verified; do not cite mock JSONL as durable evidence.
7. **Round-12 mutation blocker — superseded.** Its RL3 parser defect was real at
   report time and fixed later in-tree. Current `recompute_r12.py --selftest`
   is 165/165 PASS; round-14 fresh mutations killed 4/4.
8. **Round-13 completeness — capped.** Scripts are valid, but no prior-art,
   connector, durable analysis, route evidence, or closeout docs existed in
   that round. The round-14 reconstruction lands the measurement without
   retroactively awarding novelty.
9. **Surface drift — fixed living pointers.** `~/bench-arena` no longer exists;
   the intact content is at `~/archive/bench-arena`. Living docs now use the
   archive path; frozen historical evidence is not rewritten.
10. **Scope violation — disclosed.** An r12 endpoint scout made two read-only
    metadata GETs outside its brief. Run evidence is unchanged; the violation
    remains in `r12-scope-audit.md` and LOG.

## Report-outs

- **kotoba:** derive prompt intent from runner code, not a storage suffix;
  separate state fidelity from literal output-contract compliance.
- **aggregator/protocol:** require commit + LOG + SCORECARD + index parity before
  closeout; respawn causing the orphan is `[INFERENCE]`, not established.
- **serving plane:** no new action; endpoint id, pid 1299, 41-token argv, q4_0
  KV, `--kv-unified`, and `--parallel 2` remain exact matches.
- **OMP fallback relay:** effective `m_swe` is `devin/swe-2:max` but its
  configured fallback chain is null, not Daybreak. This is orchestration scope
  and is reported in the main-repo round report only; no config was changed and
  no failure was forced.

## Closeout checks

```text
python3 grader.py
  CHECKS n=733 mismatches=0 errata_pinned=1
  VERDICT: PASS — stored evidence fully re-derives offline
python3 grader.py --selftest
  S0–S7 PASS; ALL PASS
python3 corpus/evidence/round12-ladder/recompute_r12.py --selftest
  SELFTEST 165/165 PASS
round13 scripts --selftest
  4/4 PASS; 8/8 PASS
README parity
  knowledge 23/23; lessons 17/17; evidence 10/10
```
