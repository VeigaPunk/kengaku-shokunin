# R42ConnSibling — sibling-overlap scan, kengaku round 42 wave 1

Seat: R42ConnSibling (connector, leaf). Date: 2026-10-26.
Scope: this round's five surfaces — (a) logic-gate circuits and their simulators,
(b) C programs compiled at grading time, (c) benchmark graders with fixed input
tables, (d) mutation testing of a lane's own gate tools, (e) bwrap sandboxes —
scanned across all 21 `*-shokunin` lanes, read-only, restricted to each lane's
`PROVINCE.md`, `SKILL.md`, `corpus/README.md`. Nothing was written outside this
report and the seat scratch (`/fast/scratch/hyaku/kengaku-r42/R42ConnSibling`,
trapped for removal on exit).

## Method (evidence)

Five case-sensitive `grep` scans over 20 sibling lanes + kengaku self, three files
per lane (two sibling `SKILL.md` files absent and skipped by the tool:
`audio-shokunin/SKILL.md`, `game-dev-2d-shokunin/SKILL.md`), plus one completeness
scan for the lanes truncated in the first pass (`lore`, `tsukuroi`, `mori`):

1. `circuit|logic.?gate|gates\.txt|fibsqrt|isqrt|fpga|verilog|netlist`
2. `grader|terminal.?bench|test_outputs|oracle|fixed input|fixed table|lookup table|benchmark`
3. `gcc|clang|compile|grading.time|\-O[0-9s]`
4. `mutant|mutation|battery|killed|survived|anchor_digest|order_check`
5. `bwrap|bubblewrap|sandbox|namespac` (+ combined completeness re-scan)

Result headline: surface (a) matched **nothing** anywhere (only false positive:
`mado-shokunin/SKILL.md:1655-1656` "short-circuit-vs-silent-tolerance", a
compositor/electrical-context phrase in the desktop lane). Surface (b) matched no
sibling claim of C-source or compile-time semantics. Surfaces (c)(d)(e) have
well-defined owners and practitioners, listed below.

## Ownership answers (the two named questions)

**Who owns 'circuit correctness'? — No lane.** No sibling's three files mention
logic gates, circuits, `gates.txt`, `fibsqrt`, `isqrt`, Verilog, FPGA or netlists.
The correctness oracle for `circuit-fibsqrt` lives inside kengaku's own pinned TB2
capture (`sim.c` compares against `fib(isqrt(N)) % 2^32`; receipt
`corpus/evidence/round42/fibsqrt-probe.txt`). Kengaku owns the *measured grader
record* only, under its standing TB2 pattern: "static interpretation and offline
synthetic-fixture execution of one pinned Terminal-Bench 2.0 grader function"
(`kengaku-shokunin/PROVINCE.md:232-238`, the round-35 frontier admission, repeated
rounds 36-41, `PROVINCE.md:244-262`). Disposition: **report out** the domain
absence — kengaku should claim grader behavior, not circuit expertise, and note
digital-logic correctness as an unowned fleet surface.

**Who owns 'C simulator semantics'? — No lane.** No sibling claims C-source
runtime semantics (scanf/argv/stdout ordering) or gcc `-O3` compile-at-grading
behavior. Nearest neighbors are different surfaces: `mado-shokunin/SKILL.md:1637-1641`
(version literals compiled into shipped binaries) and kaidoku's static build-metadata
reading (`kaidoku-shokunin/corpus/README.md:62`, inline Go build metadata in
`/usr/bin/docker`). Binary provenance/identity questions defer to
**kaidoku/revenger** (shipped-artifact reverse engineering; ownership anchor at
`tsukuroi-shokunin/PROVINCE.md:129` — "Revenger owns shipped-artifact reverse
engineering"). Kengaku's frozen `sim.c` capture is the fleet's only record of this
simulator. Disposition: **report out** (unowned), defer any binary-provenance
follow-up to kaidoku.

## Overlaps found (surface, file:line, disposition)

1. **Mutation-testing method ownership — tameshi-shokunin.** `PROVINCE.md:3-11`:
   "Domain: verification-fixture craft — the reusable method of honest checks:
   hermetic suites, mutation testing, fail-closed arms…"; `:7-11` names the fleet
   gates it documented, including kumitate/kagi/kaidoku audit patterns. Confirmed
   as the fleet's standing ownership anchor by `tsukuroi-shokunin/PROVINCE.md:130`:
   "Tameshi owns the reusable verification/mutation-testing method, applied to
   fleet gates as read-only primary surfaces; each lane keeps its own gate."
   Disposition: **defer** — round-42 C1 (`plans/battery42` + `round42_c1_verify.py`)
   is kengaku mutating its own gate tools; method questions route to tameshi,
   kengaku keeps its own gate. Already reported out in-kengaku at
   `kengaku-shokunin/PROVINCE.md:262`.

2. **Attributed-kill semantics — revenger-shokunin.** `SKILL.md:56-60`:
   "Attribution is exact. A mutant kill counts only if the mutant run exits
   non-zero **and** its last output line ends with the registered phrase… A crash
   or an unrelated assertion is not attributed." Negative control at
   `SKILL.md:282-285`: `C7_MUTANT_KILLED_ATTRIBUTED=1/1` while the spoofed-marker
   twin is killed but `C7_NEG_SPOOF_KILLED_ATTRIBUTED=0/1`. This is the direct
   fleet precedent for round-42 leg f (a kill counts only when a traced re-run
   reproduces it and executes the replaced span). Disposition: **cite** — kengaku
   should name revenger's attributed/unattributed distinction as sibling practice;
   note the rule differs (revenger: exit + last-line phrase + spoof control;
   kengaku: traced re-run + span coverage), so it is a citation, not a deferral.

3. **Own-gate mutation battery with invalid taxonomy and negative controls — kasegi-shokunin.**
   `SKILL.md:1063-1100`: `limb-mutation-check.py` per-row classes
   `invalid:live-baseline|find-count|noop|nocompile|timeout` → `killed|survivor`,
   with controls `CTL-noop/CTL-nocompile/CTL-equivalent/CTL-fake-killrule`
   (`:1067` — "a naive harness that only runs the mutant reports those as
   [valid]"), and `r-defect-closure.sh` + `kill-rule-check` gating the lane's
   own instruments (`:1097-1100`). Structurally the closest sibling to battery42 +
   the round-42 counter (invalid classes, equivalent-mutant handling, harness
   self-checks). Disposition: **cite** as the nearest structural sibling;
   kengaku's `invalid`/`null_detected`/`unattributed` legs map onto kasegi's
   taxonomy but stay lane-local.

4. **Gate counters with mutant batteries and independent-oracle differentials — chousa-shokunin.**
   `SKILL.md:106-133`: the research-gate counter series, each round shipping
   mutant batteries and do-nothing controls (e.g. `:129` r48 `mutation-check.py`
   `MUTANTS_KILLED=5/5`; `:107` r42 mutant register 23 vs 24 rows). Chousa also
   runs grader-vs-independent-oracle differentials (`corpus/README.md:60`,
   `round25-meta-oracle.py` `AGREE=54/54`), the method family of kengaku's
   probe-vs-grader `regrade` leg. Disposition: **defer** capture/citation method
   (already reported out, `kengaku-shokunin/PROVINCE.md:262`); **cite** the
   counter-with-mutants practice as sibling evidence the method generalizes.

5. **Own-gate mutation case + namespace-sensitive probe limits — tsukuroi-shokunin.**
   Mutation: `SKILL.md:552-632` — tameshi's runner applied to its own census gate,
   23 defects, kill-rate 13/23, hardened to 23/23 (`:611`), with adjudication
   rules (`:616-622`: "killed = suite red **and** the full case count still
   enumerated (exit-only is insufficient)"). Namespace: `corpus/README.md:315` and
   `PROVINCE.md:234-236` — "a census that detects the counter's namespace and
   behaves honestly only there cannot be told apart on this host", and an absent
   `/sys/fs/btrfs` under a namespace reads `HEALTHY 0/0/0`. Directly relevant to
   kengaku's Q32 nested-bwrap envelope (counter adds its own read-only sandboxes
   inside the seat envelope): a fixture or tool whose behavior changes inside a
   mount/PID namespace is tsukuroi's measured class. Disposition: **cite** both;
   route reusable-method questions per tsukuroi's own routing table
   (`PROVINCE.md:52`, ADJ-07 → tameshi).

6. **bwrap operational substrate — kumitate-shokunin.** `SKILL.md:618` and
   `:728`: `cap-run.mjs` runs children under "env -i + bwrap --unshare-pid
   --die-with-parent --new-session --clearenv" with a systemd-run cgroup cap;
   `corpus/README.md:145`: `knowledge/mount-order-and-bind-scope.md` —
   "Bubblewrap filesystem operation order, safe tmpfs-root versus subdirectory
   binds, and mountinfo field-5 limits"; `corpus/README.md:92-93`:
   `agent-isolation-substrates.md` (bwrap PID-1 environ among seven isolation
   mechanisms). Disposition: **defer** — kumitate owns bwrap mount/PID semantics
   on this host; kengaku's envelope (`bwrap --dev-bind / / --ro-bind
   ~/.local/bin ... --unshare-pid --die-with-parent`) and the C1 counter's nested
   read-only sandboxes should cite kumitate's mount-order knowledge rather than
   re-derive it (already reported out for seat arrangement at
   `kengaku-shokunin/PROVINCE.md:262`).

7. **Sandbox refusals and the bwrap adjacency note — kaidoku-shokunin.**
   `PROVINCE.md:101-105`: refuses "Malware triage at scale — verdict pipelines,
   sandbox detonation… (unowned)" and "Non-REA dynamic analysis"; `SKILL.md:790`:
   "No no-execution guard or OS sandbox is asserted." `SKILL.md:667` (carrier-guard
   limits): "bwrap 0.13.1 exists on the host but is not used." Kaidoku owns static
   RE of shipped binaries, not execution containment. Disposition: **report out**
   (negative boundary — kaidoku must not be cited as a sandbox owner); defer
   binary-provenance questions here per overlap tail of the ownership answer.

8. **Additional own-tool mutation practitioners — kama-shokunin, mori-shokunin.**
   `kama-shokunin/SKILL.md:888-889`: promisor/isolation mutation experiments, 11
   named mutations, "kills and survivors listed, not universal green", with an
   `--anchors` applicability check "without executing the grid".
   `mori-shokunin/SKILL.md:183-195`: mutant fixtures of mori's own counters
   (e.g. `:190` a `count-c1.py` mutant disabling duplicate-id detection read by
   its own selftest as `pass=15 fail=1`). Disposition: **cite** (weak) — more
   instances of the fleet-wide own-gate mutation pattern; no method transfer
   implied.

9. **Explicit "not a sandbox" boundaries — kotodama-shokunin, kagi-shokunin.**
   `kotodama-shokunin/SKILL.md:718-719`: "The battery runs trusted repo scripts
   in a copied working directory; it is not an operating-system sandbox."
   `kagi-shokunin/SKILL.md:303`: "This is a text guard, not a sandbox";
   `SKILL.md:779-780`: "author-side measurement, not independent admission or a
   hostile-program sandbox." Disposition: **report out** — negative boundaries
   that prevent mis-citation when the L1 words adjacency in PROVINCE/README.

Non-overlaps verified: `lore-shokunin` (narrative canon; matches were data-mutation
classes in its map gate, unrelated), `audio`/`game-dev-2d`/`game-dev-3d`
(`game-dev-3d/PROVINCE.md:69` and `corpus/README.md:168` already route
orchestration/LLM-evaluation questions away from themselves), `tabi-shokunin`
(`SKILL.md:1707-1710`: "no… sandbox-certification… claim is made… forensic work
remains revenger/kaidoku-owned" — a useful third-party confirmation of the RE
ownership split), `souji-shokunin` (uses bwrap+strace in one counter,
`SKILL.md:261`, and warns "Known namespace checks are not a universal defense",
`PROVINCE.md:105-107` — **cite** as a secondary namespace caution), `kake`,
`kotoba`, `chousa`'s non-gate rows.

## Effect on this round's claims

- **C1 (calibration):** no ownership conflict. battery42 mutates kengaku's own
  tools, which tameshi's anchor explicitly leaves to each lane. Cite revenger (2)
  and kasegi (3) in the round report as sibling precedent for attributed kills
  and invalid-class taxonomies; this strengthens adjacency without weakening the
  counter (leg f's traced re-run + span execution is kengaku's own rule, not
  borrowed).
- **C2 (coverage):** no sibling owns TB2 grader replay; kengaku's series
  (`corpus/README.md:66-74`, S100 + six admitted TB2 graders, now 8 of 89 with
  `circuit-fibsqrt`) is the fleet's only record. The unowned status of circuit
  correctness and C simulator semantics is itself an adjacency finding worth one
  PROVINCE sentence, so future lanes do not assume a digital-logic or C-semantics
  owner exists.
- **Host safety / Q32 envelope:** cite kumitate (6) for bwrap mount-order and
  tsukuroi/souji (5, non-overlap note) for namespace-sensitivity limits; no
  envelope change is implied — the citations are for the L1's adjacency wording.

No files outside `.ufo/waves/round-42/build/` and the seat scratch were touched;
no sibling lane file was modified (all scans read-only); no tools were installed.

VERDICT: sibling-overlap-9
