# FxRegistry — round 26 dispatch/registry audit

Axis: calibration (seat and identity accounting only; no judgment of novelty or routing).

## Findings

**Low — build registry retains eight pre-trim seats.** Final `build-spec.json` and `build-assignments.json` each name 72 seats; the build report directory contains exactly those 72 report stems. The post-dispatch `build/swarm-registry.json` has 80 member keys, however: `ConnSiblingQuality`, `CritRepairCompleteness`, `RevLowestAxis`, `RevSpotcheckR24`, `ScribeGateTable`, `ScribeLogEntry`, `ScribeSearchLog`, `SimplPerturbDesign` are extra and all have null `agentId`. `build-dispatch-log.txt:7` records that an 80-seat draft was trimmed to 72 before dispatch. These are stale/deferred rows, not missing dispatched agents, but consumers must not treat the registry's raw member count as the final roster.

**Build roster otherwise reconciles; actual IDs are recorded.** Spec ↔ assignments and assignments ↔ report stems have empty symmetric differences; all 72 assignment IDs match the 72 dispatch-log job/agent IDs and 72 unique non-null IDs in the post-dispatch registry. Role counts in the final spec are executor 14, scout 22, connector 6, reviewer 12, critic 6, revenger 4, scribe 6, simplifier 1, sentinel 1; no spec/registry role mismatch or duplicate actual ID. The dispatch JSON's embedded plan registry has 72 entries with null IDs; actual IDs are in `build/swarm-registry.json` and the dispatch log.

**Refusal history is not a missing-seat defect.** `build-dispatch-log.txt:1-6`: plan/run exit 0; the first three attempts refused all 72 with “Background job limit reached (100)” and spawned nothing; the 03:50:27 attempt refused 0, with the same payload. The final log enumerates 72 spawned IDs (`:10-82`); 72 reports exist. No build dead seat is recorded.

**Falsify roster IDs and dead-seat accounting reconcile; report return is still in flight.** Falsify spec/assignments each have 64 names; all 64 assignment IDs equal the 64 unique actual-registry IDs and 64 dispatch-log IDs, with no null IDs, duplicate IDs, or role mismatches. Roles: reviewer 39, mutation-tester 10, scout 7, critic 4, executor 2, connector 2. `falsify-dispatch-log.txt:1-2` says all 64 started with no dispatch refusals. `falsify-dead-seats.json:1` explicitly records six post-start dead seats (FxNoHarm, FxTrends, FxSeparability, FxCensus, FxHonesty, FxLowestAxis), `replaced:false`; these IDs remain in the registry/log. At this check, 29 assigned-seat `.md` reports existed: 35 report names were absent, six accounted for by the dead-seat file and 29 other returns not yet observed. Do not classify those 29 as dead or missing from this snapshot.

## Evidence / verification

Read-only cross-ledger command (exit 0):
```sh
python3 -c 'import json,pathlib,re;R=pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26");
for w in ("build","falsify"):
 s=json.load(open(R/(w+"-spec.json")))["items"];a=json.load(open(R/(w+"-assignments.json")));g=json.load(open(R/w/"swarm-registry.json"))["members"];L=[x for x,y in re.findall(r"- `([^`]+)` [(]job `([^`]+)`[)]",(R/(w+"-dispatch-log.txt")).read_text())];N={x["name"] for x in s};F={x.stem for x in (R/w).glob("*.md") if x.stem!="FxRegistry"};I={v["agentId"] for v in g.values() if v.get("agentId")};print(w,"items/assignments/seat_reports/registry/IDs/log/uniqueIDs/spec^assign/assign^reports/assign^log/log^registry",len(s),len(a),len(F),len(g),len(I),len(L),len(set(L)),len(N^set(a)),len(set(a)^F),len(set(a.values())^set(L)),len(set(L)^I))'
```
Output: `build ... 72 72 72 80 72 72 72 0 0 0 0`; `falsify ... 64 64 29 64 64 64 64 0 35 0 0` (fields as named in command). Role totals were read from each spec; dead/refusal evidence from the paths cited above.

LSP unavailable: `read xd://lsp` returned `No such tool`; no LSP status/references/definition/diagnostics could be obtained. No grep fallback was used. No route claim made from memory. No installs.

## Residual risk / verification gap

Falsify report closure was incomplete at the observed snapshot (29 non-dead assigned returns unobserved); re-check before admission. The eight build-registry extras are bookkeeping residue only insofar as final assignments/logs remain authoritative.

VERDICT: Low-severity stale build-registry roster residue; all 72 build IDs and report names reconcile, all 64 falsify IDs are recorded, and 29 non-dead falsify returns remain unobserved.
