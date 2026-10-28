# C1ConnectSiblings — round 52 wave 1

## Findings

**Disposition:** R52-C1 and R52-C2 are inside kengaku's province on the inspected boundaries. No registered `*-shokunin` sibling claims whole-population Terminal-Bench grader auditing or benchmark task-validity auditing. The fleet-wide registry schema is not kengaku-owned: it is the PROTOCOL §Gate standard; kengaku's work is limited to its own registry home. Closest sibling analogues are lane-local tools, not duplicates of kengaku's task/population.

### Benchmark graders and task validity

- **kasegi** explicitly routes “kengaku — LLM evaluation and benchmarks” as adjacent/report-only (`kasegi-shokunin/PROVINCE.md:43-52`, specifically `:50`). **Class (a):** supports kengaku ownership; no contest.
- **kumitate** says “kengaku evaluates agents, this lane arranges the seats around that judgment” (`kumitate-shokunin/PROVINCE.md:24`). Its Terminal-Bench references are benchmark results in an orchestration-topology study, not grader inspection (`kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md:29,53,83`; README index `:187`). **Class (a):** evaluation routes to kengaku; the cited study is not a duplicate grader audit.
- **chousa** owns research method/source hierarchy/claim-vs-source verification and refuses evaluation claims to kengaku (`chousa-shokunin/PROVINCE.md:5-15`). **Class (a)** for evaluation ownership; **report-out:** C1's prior-art pricing method should remain chousa's method, while the benchmark-specific findings/application remain kengaku's. Kengaku already records chousa as research-method owner (`PROVINCE.md:138`).
- **souji**'s round-31 connector already identifies the Terminal-Bench git-leak grader as kengaku-held ground (`souji-shokunin/census/round-31/waves/w2/SwarmConnector28.md:21`). This is a routing precedent, not a competing owner.
- Searches of sibling `PROVINCE.md`, `SCORECARD.md`, and `corpus/README.md` for `grader`, `Terminal-Bench`, `task-validity`, and `task-spec` found no sibling ownership claim for grader-population or task-validity auditing. The few keyword hits were not such claims: kumitate's paper summary above; tsukuroi's `b2_ok` EFI column (`tools/boot-chain-audit.sh:761`); kaidoku's “vacuous” discussion is about its own evidence/gate defects, not benchmark graders (`corpus/lessons/round-16.md:58`, rounds 17–23). These are **not** duplicates or contests.
- Kengaku's existing scope is explicit: benchmark task-spec audits are Frontier (`kengaku-shokunin/PROVINCE.md:124-128`); the published-maintainer task-validity checklist is admitted at `:214-223`; individual TB2 grader readings are narrowed to specific tasks (`:231-241` and later append-only admissions). The existing WebArena `plans/benchmark_spec_audit.py` is explicitly a static spec inventory, not task-validity verdict (`kengaku-shokunin/plans/benchmark_spec_audit.py:1,16-23`; registry row `SKILL.md:570`). Thus C1's whole-TB2 grader population triage extends the lane's own task-specific work; it is not a sibling duplicate. The lane's `plans/registry_check.py` checks frozen literal source references, not gate rows (`SKILL.md:571`; `corpus/README.md:496`).

### Gate/probe registry

- **Fleet standard:** `PROTOCOL.md:375-423`; specifically `:398-406` says the schema belongs to this section and a child lane's registry home is its own `SKILL.md`. Therefore **C2 is class (a)** for kengaku's own rows, not authority to set a fleet-wide standard. Kengaku already routed a fleet-wide standard to protocol/integrator (`kengaku-shokunin/SCORECARD.md:138`; `PROVINCE.md:140`).
- **kama** is the closest sibling instrument analogue: `tools/gate-registry-check.py` grades occurrence and row meaning (thin row, empty entry/exit map, missing paths; source docstring lines 1-60); its PROVINCE says the tool is lane-internal (`kama-shokunin/PROVINCE.md:152-158`), and its registry home is its own `SKILL.md:296`. Its prior art overlaps conceptually with C2's row/cell/path checks, but uses kama's own registry and population. **Class (b) only if C2 is represented as a fleet-wide registry standard; otherwise adjacent, not a duplicate.** Report out the prior art; do not absorb or claim kama's general method as new.
- **kasegi** maintains its own 8-cell `Gates & probes registry` table (`kasegi-shokunin/SKILL.md:977-980`) and a D3 closure limb that checks two named instrument rows (`corpus/instruments/r35-defect-closure.sh:275-277,310,335-337`; fixture shape `corpus/instruments/r35-fixtures/D1/SKILL.md:6-11`). This is lane-local row-presence precedent, not a whole advertised-instrument census. **Adjacent, not duplicate.**
- **tameshi** owns reusable gate-audit craft, not sibling gate code (`tameshi-shokunin/PROVINCE.md:7-18,44-47`). `tools/registry-check.py:1-30` replays its own JSON `tameshi-entry-registry-v1` entries; it is not a SKILL table registry. **Adjacent/report out; not duplicate.**
- Other siblings visibly maintain their own registry homes: revenger `SKILL.md:281` (explicitly cites PROTOCOL); lore `SKILL.md:48-50`; kumitate `SKILL.md:587-591`; kaidoku `SKILL.md:771-775`; kama `SKILL.md:296`; kasegi `SKILL.md:977-980`. These are their own rows, not ownership of a separate fleet standard.
- **kotoba** owns the standing fleet sibling-overlap census and its checker (`kotoba-shokunin/PROVINCE.md:17`; `corpus/README.md:69,146`; `corpus/knowledge/sibling-overlap-census-round74.md`; `verifiers/check_sibling_census.py` and `check_sibling_reread.py`). This assignment's bounded, claim-specific scan is **not** a new standing census instrument. **Class (c) for the general census method/artifact**; report out to kotoba and keep this receipt scoped to R52-C1/C2.

### Clone/duplicate hazard

`/home/vgpnk/Projects/shokunin/lane3` is not a sibling lane: its git remote `origin` is `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; its HEAD is `297e17927ba9342a87ba27a48cc5270a001de7cb` (round-50) and is an ancestor of kengaku's current HEAD; the directory is absent from MANIFEST's lane roster and `git ls-files lane3` reports no tracked paths. It contains the same 12 `tb2-*-grader.md` files as kengaku and the same `SKILL.md:560` registry heading, but no round-52 population file. **Class (c): duplicate of this lane's own older artifacts, not a sibling claim.** Fleet-root searches that include `lane3/` can double-count the 12 grader notes or mistake the duplicate registry heading for an independently owned sibling surface; exclude it from sibling counts and report the stray clone to the integrator. I did not modify it.

## Report-outs to record in kengaku PROVINCE.md

1. R52 C1/TB2 grader-population and benchmark task-validity work remains kengaku-owned; sibling routing evidence: kasegi `PROVINCE.md:50`, kumitate `PROVINCE.md:24`, and souji's prior handoff `SwarmConnector28.md:21`.
2. C1 prior-art/source-hierarchy method remains chousa-owned; kengaku owns only its benchmark-specific application (`PROVINCE.md:138`).
3. C2 fills kengaku's own `SKILL.md` registry only; fleet registry schema/standard remains protocol/integrator-owned (`PROTOCOL.md:398-406`; prior kengaku routing `SCORECARD.md:138`). Record kama's meaning-grading registry checker, kasegi's row-presence limb, and tameshi's registry-monitor/craft as lane-local precedents, not duplicates or a new fleet standard.
4. General sibling-overlap census remains kotoba-owned; this is a one-round scoped scan, not a competing census capability (`kotoba-shokunin/PROVINCE.md:17`, `corpus/README.md:69,146`).
5. `lane3/` is an unregistered stale clone of kengaku at round 50, not a sibling; flag for integrator awareness and exclude it from any fleet sibling/population counts.

## Commands and measured observations

Read the frozen assignment first: `read /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-52-claims.md` (whole file; claims specify R52-C1, R52-C2 and frozen populations/rules). Read sibling `PROVINCE.md`, `SCORECARD.md`, and `corpus/README.md` evidence through targeted reads/searches; targeted commands included:

```sh
cd /home/vgpnk/Projects/shokunin
ls -d /home/vgpnk/Projects/shokunin/*-shokunin
grep -rn -iE 'terminal-bench|terminal_bench|tb2-|harbor-framework' --include=*.md --include=*.py --include=*.json --include=*.sh .
grep -rn -iE 'grader|task[- ]valid|task[- ]spec|registry' --include=PROVINCE.md --include=SCORECARD.md --include=README.md .
grep -rn -iE 'vacuit|vacuous' --include=*.md --include=*.py .
grep -rn '^## Gate/probe registry' --include=SKILL.md .
git -C lane3 remote -v
git -C lane3 rev-parse HEAD
git -C kengaku-shokunin rev-parse HEAD
git -C kengaku-shokunin merge-base --is-ancestor 297e17927ba9342a87ba27a48cc5270a001de7cb HEAD
git -C /home/vgpnk/Projects/shokunin ls-files lane3
git check-ignore -v lane3
python3 plans/round52_c2_registry.py --lane .
```

The exact claim-file base tip is `30801b479e3418c11089b8586178b6960216f364`. The observed working HEAD had advanced to `07ea2084053f5112ea797a653e6a3a96e8cf4a64` (round-52 A1), so I did **not** treat a current-tree counter run as a base-tip measurement. At observed HEAD, the read-only C2 counter printed `ADVERTISED total=72`, `REGISTERED total=44 rows=46`, `MISSING 28`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1` (`order-check`), `PREDICATE R52-C2 fail`. (The shell command piped through `head`, so its displayed `EXIT=0` is the pipeline status, not a verified counter exit; no exit claim is made.)

Other measured facts: 12 `tb2-*-grader.md` entries in kengaku and 12 in lane3; lane3 has no `round52-tasks.json`; the frozen population JSON is present only in kengaku among searched tree paths. No sibling TB2 grader-population instrument was found. No tools were installed or updated.

## Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ConnectSiblings.md` — this read-only scan report.
- Scratch directory `/fast/scratch/hyaku/kengaku-r52/C1ConnectSiblings/` was created for this seat; no clone, fixture, or other artefact was placed there. It will be removed before handoff.
