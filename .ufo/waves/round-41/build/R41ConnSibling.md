# R41ConnSibling — sibling-overlap scan (kengaku round 41, wave 1)

Seat: R41ConnSibling (connector, leaf). Date: 2026-10-26.
Scan surfaces (read-only): all 20 sibling lanes' `PROVINCE.md`, `SKILL.md`, `corpus/README.md` under
`/home/vgpnk/Projects/shokunin/*-shokunin`, for this round's four surfaces: calendar/ICS and
scheduling-constraint graders; RFC 5545 conformance; mutation testing of a lane's own receipt/registry
tools; bwrap sandboxes. Round-41 claims read first, in full (`plans/round-41-claims.md`).

Method: pattern sweeps over the 20 lanes × 3 files, then targeted reads of every hit's context. All
citations below are to committed bytes at the scan time.

## Summary of the scan

- **No sibling lane contains ICS/iCalendar/RFC 5545/DTSTART/RRULE/Terminal-Bench content** in any of the
  three scanned files. A combined sweep (`(?i)(5545|icalendar|dtstart|rrule|terminal-bench|tb2|
  constraints-scheduling)`) over 40 sibling province/skill files returned zero hits. This confirms and
  extends kengaku's own round-38 verification — only `kumitate-shokunin/corpus/knowledge/
  multi-agent-coordinator-topologies.md` and `corpus/lessons/round-63.md` mention TB2 fleet-wide, as
  coordinator-topology data citations, already ruled not grading claims
  (`kengaku-shokunin/PROVINCE.md:351-356`).
- **Every overlap found is either (a) a same-class precedent already ruled in rounds 37–40, or (b) a
  word-level homonym with disjoint semantics.** None changes the frozen claims' separability.

## Named overlaps

O1. **tameshi owns the reusable fixture/mutation method — kengaku's C1 is kengaku's own instrument.**
`tameshi-shokunin/PROVINCE.md:3-18` (domain: "verification-fixture craft — the reusable method of honest
checks: hermetic suites, mutation testing, fail-closed arms…"; Owns list of sibling gates as primary
surfaces; service-optin protocol at `corpus/knowledge/service-optin-protocol.md`). kotoba's sibling census
records the split: "tameshi owns the reusable fixture and mutation method while each lane's gate stays its
own" (`kotoba-shokunin/PROVINCE.md:74`; whole census at `corpus/knowledge/sibling-overlap-census-round49.md`).
kengaku's round-40 C1 adjacency already resolved exactly this: "the mutation test of the lane's own tripwire
tools (plans/round40_c1_verify.py, plans/battery40/) is kengaku's instrument for its own self-assessment,
not the mutation-testing method, which stays tameshi's (tameshi-shokunin/PROVINCE.md:1-17; its
tools/mutate-and-run.sh carries no kengaku leg)" (`kengaku-shokunin/PROVINCE.md:461-464`).
→ **Cite** tameshi (method) in the C1 entry/province; do not defer the battery itself. The round-41
`plans/battery41` fixtures are kengaku's own gate work.

O2. **kumitate `gate-mutants.mjs` — precedent for mutating a lane's own gate.** Named in kengaku's
round-37 reported-out block: "mutation testing of a lane's own gate is a fleet-wide pattern, not kengaku
ground — tameshi's `tools/mutate-and-run.sh` and kumitate's `gate-mutants.mjs` are the precedents"
(`kengaku-shokunin/PROVINCE.md:282-283`). kumitate's current registry rows confirm the class
(`kumitate-shokunin/SKILL.md:617-625`: `omp-census`, `cap-run`, `receipt-evidence`, `counter-rerun`,
`bind-oracle`, `receipt-attest`, `counter-pins` — several with mutant arms).
→ **Cite** as prior art in the C1 admission text (same as rounds 37–40).

O3. **bwrap substrate: kumitate `cap-run.mjs` / `bind-oracle.mjs` are the sibling sandbox precedents.**
`kumitate-shokunin/SKILL.md:618`: cap-run launches the child under `env -i` + `bwrap --unshare-pid
--die-with-parent --new-session --clearenv`, cwd bound read-write, caller `--bind`…
`SKILL.md:622`: bind-oracle builds *runner mutants* from cap-run source — "drop the request binds, add
`--bind /etc /etc`, remove `--tmpfs /tmp`". So kumitate both builds bwrap sandboxes and mutation-tests the
sandbox argv construction. This is the exact substrate class of the round-41 C1 envelope
(`bwrap --ro-bind / /`, `--tmpfs /run/user/1000`, `--proc`, `--unshare-pid`, `--die-with-parent`).
kengaku's round-40 adjacency already flagged kumitate's `cap-run.mjs` (`--ro-bind / /`) as "the cited
stronger form a round-41 counter would need to close the writable-host-fs limit (R40SentinelCounter F1/F2)"
(`kengaku-shokunin/PROVINCE.md:465-466`).
→ **Cite** as fleet prior art; the sandbox construction itself is not novel ground. No deferral needed —
kengaku's own envelope is a stricter (read-only) instance.

O4. **kaidoku sandbox alternatives — bwrap noted but unused; systemd-run chosen.**
`kaidoku-shokunin/SKILL.md:635` (carrier-guard limits): "bwrap 0.13.1 exists on the host but is not used"
— kaidoku documents bwrap availability and deliberately uses systemd-run instead. `SKILL.md:637`
(revexec): systemd-run `PrivateNetwork=yes`, `ProtectSystem=strict`, `ProtectHome=read-only`, work dir rw,
with the caveat "Not a security boundary: same uid, AF_UNIX sockets reachable". `SKILL.md:619`
(jj-red-before): sandbox clone with origin remote removed, HOME/XDG isolated.
→ **Report out** (informational): kaidoku's named limits (same-uid AF_UNIX reachable; direct-execve-only
bypass list) are useful caveats for the round-41 envelope's `--unshare-pid`/`--die-with-parent` claims;
not absorbed.

O5. **mado consumes tameshi's `mutate-and-run.sh` read-only — the fleet consumption pattern.**
`mado-shokunin/PROVINCE.md:20` ("the reusable mutation-testing method stays with tameshi (tools/mado-verify.sh
consumes tameshi's mutate-and-run.sh read-only and prints its revision as provenance, never patching it and
never gating it)"); `PROVINCE.md:28` (`tools/mado-verify.sh --regression` "hands the spec to tameshi's
mutate-and-run.sh read-only"). tameshi's own province records the opt-in protocol and the recorded legs
(`tameshi-shokunin/PROVINCE.md:28-38,50-117`).
→ **Report out** (informational): confirms the fleet rule that mutation-method use is read-only service
consumption; kengaku's C1 builds its own fixtures (as its own gate), and does not invoke tameshi's runner.

O6. **Fleet-wide self-mutation of own gates/instruments — same class as C1, all sibling-internal.**
The pattern "mutate your own tool, assert kills" is pervasive and lane-internal: kaidoku
`round19-postfix-mutations.py` (committed sandbox mutants, `SKILL.md:632`) and round-27/29 counters with
killed/survived mutants (`SKILL.md:981-992`); chousa round-48 `mutation-check.py` (`MUTANTS_KILLED=5/5`,
`SKILL.md:129`) and round-31/33-40 counter families; kama `promisor-mutants.py` (`SKILL.md:1020-1021`);
mori thirteen sandbox mutants (`SKILL.md:665`); kagi `--falsify` 18/18 mutations (`PROVINCE.md:51`);
game-dev-3d r101 mutation matrix (`SKILL.md:46`); kumitate bind-oracle runner mutants (O3). This is
kengaku's own round-37 ruling verbatim ("fleet-wide pattern, not kengaku ground").
→ **Cite** in the C1 entry as the fleet precedent class; no sibling owns C1's specific pair of tools
(`plans/tip_receipts.py`, `plans/sources_adopt.py`), which are kengaku's.

O7. **kama "per-slot capacity" vs C2's minute-granularity slot scan — homonym, disjoint domains.**
`kama-shokunin/PROVINCE.md:105-107`: "Context declaration versus effective per-slot capacity is not model
quality. Kengaku's technique overlap is acknowledged, not absorbed." kama's slots are llama-server serving
slots; the round-41 C2 slot scan is an embedded scheduling model over three ICS calendars. Same word,
different semantics. kama's province also records the serving-plane split: kumitate's watcher posts as a
consumer and "kengaku excludes the model-serving plane (`.ufo/waves/round-31/w1/out/ConnSibling/overlap.md`)"
(`kama-shokunin/PROVINCE.md:143-144`); kengaku's province agrees the serving plane is not owned by kengaku
(`kengaku-shokunin/PROVINCE.md:24-25`), with restoration operator/kama-owned (`PROVINCE.md:202`).
→ **Report out** (to L1 when authoring the C2 entry): add one "Adjacent: model-serving slot capacity stays
kama's" line to the entry (mirrors the S119 homonym handling in kotoba's census) to prevent cross-lane
confusion. No substantive overlap.

O8. **kotodama/lore fictional-world calendars — word-only overlap.**
`lore-shokunin/PROVINCE.md:28`: "Kotodama also owns name generation (… `naming-systems.md`, …) and
calendar/era design (`kotodama-shokunin/corpus/knowledge/culture-material/calendar-festival-systems.md`, `…/
culture-material/era-periodization-models.md`)". These are fictional-world calendar systems, not machine-readable
ICS; no scheduling-constraint semantics.
→ **Report out** (informational; optional adjacent mention in the entry).

O9. **chousa calendar-valid date checks — deadline semantics, not scheduling.**
`chousa-shokunin/SKILL.md:143` ("scheduled recheck dates must be calendar-valid (`verified-at` stays
shape-only)"), `SKILL.md:547` (`--as-of YYYY-MM-DD` … "Calendar-valid explicit dates … define deadlines"),
`corpus/README.md:64` (`knowledge/recheck-due-r26.md` — "Schedule-derived deadline semantics, explicit as-of
date, event/unknown classifications"), `corpus/README.md:871` ("The generic schedule and registry policy are
the lane's design, not Cochrane, Python or PROV requirements").
→ No conflict — chousa validates dates on its own metadata; kengaku grades a TB2 grader's verdict model.
Report out only as a named non-overlap if desired.

O10. **game-dev-3d "tick schedule" — engine loop semantics.**
`game-dev-3d-shokunin/corpus/README.md:181` ("run the same fixed contact/joint fixture and tick schedule
under both backends"). Disjoint from calendar scheduling. Also `corpus/README.md:173` re-affirms the
adjacency split: "LLM/model evaluation | adjacent | … kengaku model research and evaluation".
→ No action.

## Negative findings (no overlap)

- **RFC 5545 conformance:** zero sibling instances; the only RFC 5545-adjacent surface in the fleet is the
  round-41 C2 probe itself (kengaku-internal). No citation needed, no owner elsewhere.
- **Scheduling-constraint/ICS graders:** no sibling reads, scores or claims any calendar/ICS grader or
  Terminal-Bench grader execution; kengaku's TB2-grader line (rounds 35–41) remains the sole instance in the
  fleet. The "remaining 83 of 89 TB2 task graders" frontier clause narrows only inside kengaku.

## Who owns "what a correct schedule is"?

- **Fleet-wide: no lane claims scheduling-semantics authority.** The closest split is already recorded:
  kama owns serving-plane slot *capacity* semantics (`kama-shokunin/PROVINCE.md:105-107,143-144`);
  kotodama owns fictional-world calendar/era design (lore `PROVINCE.md:28`); chousa owns recheck-deadline
  date validity (`chousa-shokunin/SKILL.md:143,547`); nobody owns calendar scheduling or ICS semantics.
- **kengaku owns, for this round and per its province pattern: which TB2 grader is captured, how it is
  called offline, what its verdict answers, and the C1/C2 counters** (round-38 wording,
  `kengaku-shokunin/PROVINCE.md:351-352`). It explicitly refuses runtime task validity and deployment
  configuration (`PROVINCE.md:404,202`). The source of "correct schedule" for the graded artefact is the
  upstream terminal-bench-2 repository's own task (`tests/test_outputs.py` + `instruction.md`); kengaku
  claims a probed instance of that grader, not scheduling correctness as such (claims file C2 limits).

## Recommendations to L1

1. In the C2 entry, add an "Adjacent" sentence: model-serving slot capacity stays kama's; fictional calendar
   design stays kotodama's; recheck-deadline semantics stay chousa's (O7–O9). This mirrors the homonym
   handling precedent in kotoba's census.
2. In the C1 admission text, keep the standing citations: tameshi (method), kumitate `gate-mutants.mjs`
   and `cap-run.mjs` (precedents) — rounds 37–40 rulings, reaffirmed here (O1–O3).
3. No sibling surface requires deferral or absorption; the frozen claims' separability (claims file §
   Separability) is unaffected.

VERDICT: sibling-overlap-10
