# Round 52 — frozen claims (kengaku, hyaku run 11, 2026-10-28)

L1 `KengakuR52a3`. Base tip `30801b479e3418c11089b8586178b6960216f364` (lane branch `master`,
`jj-lane.sh state` → `ahead=0 behind=0`, clean tree). Frozen **before** the round-52 wave was
dispatched; every number, predicate, control and kill rule below is fixed at this commit and is
not amended after any seat has scored (PROTOCOL append-only: a later change is new text, never
an in-place rewrite of a frozen rule).

## Axis choice

Lane axes per `../MISSION.md`: **novelty + calibration**. The six `../AXES.md` axes are the
lane's scoring surface. Current lane scores at the base tip: novelty **8**, calibration **9**,
depth 9, operability **8**, freshness 9, adjacency 9, coverage **7**.

**Lowest non-retired axis is coverage 7, and it is not claimed this round.** Coverage is capped
by an open operator decision — `kengaku | round-25` (does a surface retired to `PROVINCE.md`
§Historical still count as "declared-but-unresolvable"?) and `kengaku | round-33` (what committed
evidence lifts the cap) — plus `kengaku | round-51` (three declared surfaces are absent on this
host; restore or retire?). No L0 answer may be assumed (§6 run-10: route around open L0
questions, never treat them as answered). The round therefore works the next-lowest band (the
8s), exactly as rounds 48–51 did, and says so in the report.

Stagnation nudge: **not** invoked (coverage 7 is below the lane's saturation line of 8, and a
capability has entered the table in each of the last rounds).

## Claim 1 — R52-C1 (novelty 8 → 9)

**Surface moved.** A whole-benchmark grader-vacuity triage for Terminal-Bench 2.0: the lane has
read **12 of 89** task graders by hand, one per round, since round 35; it has no instrument that
audits a benchmark's graders as a population. This claim lands the first one and prices the
findings it produces against public prior art.

**Counting command (frozen).**

```sh
python3 plans/round52_c1_grader_audit.py --lane .
```

**Before (base tip `30801b47`, measured 2026-10-28).**

```
TASKS total=89 records=89 classified=0
CAPTURES expected=184 present=0 mismatched=0
CLASS V1=0 V4=0 V2=0 V3=0 V0=89
CANDIDATES total=0
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
PREDICATE R52-C1 fail        (exit 1)
```

Corroborating before-counts (same tip): hand-read TB2 graders = `ls corpus/knowledge/tb2-*-grader.md | wc -l`
→ **12**; captured grader files = **0**; `corpus/evidence/round52/` = absent.

**After target (all legs must hold; the command prints `PREDICATE R52-C1 pass`, exit 0).**

1. `CAPTURES expected=184 present=184 mismatched=0` — every grader file of the frozen
   population is captured byte-exact and digest-pinned in
   `corpus/evidence/round52/graders/SHA256SUMS`.
2. `TASKS total=89 records=89 classified=89` — every frozen task has a complete record
   (grader path, sha256, byte count, feature set, class).
3. `CONFIRMED new ≥ 2` — at least two tasks **never read by this lane before this round** are
   flagged by the instrument and confirmed by an **independent second reader** with a located
   quote (`corpus/evidence/round52/confirmations.json`: `task`, `quote`, `reader`,
   `confirmed`).
4. `PRIOR-ART ok=True urls ≥ 3` — `corpus/evidence/round52/prior-art.md` prices each confirmed
   finding against fetched public primaries (≥3 distinct URLs) and states, per finding, whether
   the weakness is already documented (phenomenon-known) or not (phenomenon-new).
5. `LABELS agree/total` — blind-label agreement against `corpus/evidence/round52/labels.json`
   is **reported** (evidence, not a predicate leg; the blind labrat seats labelled without
   seeing the classifier).

**Frozen classification rules** (applied to the primary grader `tests/test_outputs.py` bytes;
`environment/tests/test_outputs.py` when the task has no `tests/` grader). Presence marker
`exists(`/`is_file(`/`is_dir(`/`os.path.exists`; content marker
`read_text|read_bytes|open(|json.load|re.(search|match|findall|finditer)|.decode(|.strip()|.splitlines()`;
behaviour marker `subprocess|os.system|os.popen|Popen|socket|requests|urllib|http.client|docker|bwrap|curl`;
test count = number of `def test_` lines.

| class | rule (first match wins) |
|---|---|
| `V1` | presence marker present **and** no content marker **and** no behaviour marker — the grader can be satisfied by the mere presence of an artefact |
| `V2` | behaviour marker present — the grader executes something |
| `V3` | content marker present — the grader reads and compares content |
| `V4` | no marker class applies and ≤2 test functions — the graded surface is sparse relative to a task instruction |
| `V0` | otherwise |

`V1` and `V4` are the **triage queue** (`CANDIDATES`); a candidate becomes a *confirmed finding*
only when an independent second reader locates the weakness in the grader bytes.

**Kill rule.** If the after-run fails any of legs 1–4, R52-C1 is **not admitted**: the round
reports the measured failure as an honest stop. The novelty score then stays at 8 even if the
capability lands, and the SCORECARD row carries the measured numbers, not a bump.

**Score rule (frozen).** Novelty 8 → 9 only if the prior-art verdict prices at least one
confirmed finding as **phenomenon-new** (not previously documented in a fetched primary). If every
confirmed finding prices as phenomenon-known, the capability lands and novelty is **held at 8**
(reported honestly). The row records which case happened.

**Controls (each must fail the predicate; receipts under `.ufo/waves/round-52/claims/`).**

| control | what it does | must fail on |
|---|---|---|
| `c1-control-nothing` | base tip, no captures, no instrument output | `CAPTURES present=0`, `CONFIRMED new=0` |
| `c1-control-name-only` | a manifest that lists the 89 task names and no fields | `classified=0` / `TASKS records` incomplete |
| `c1-control-blind-class` | force every task to `V0` | `CANDIDATES total=0` → `CONFIRMED new=0` |
| `c1-control-drop-capture` | remove one captured grader from the manifest | `CAPTURES present=183 mismatched=1` |

**Frozen population.** `plans/round52-tasks.json` — repo `harbor-framework/terminal-bench-2`,
pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, **89 tasks**, **184 capture files**
(94 `test_outputs.py`, 89 `test.sh`, 1 `verify.sh`), each task's grader files listed. The
population is frozen here: it is the tree at the pin, re-derivable with
`curl -fsS "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1"`.

## Claim 2 — R52-C2 (operability 8 → 9)

**Surface moved.** The fleet's §Gate standard (and this lane's own round-51 closure) grades a
gate conformant only when its registry row exists — but the lane advertises **72** runnable
instruments in its self-assessment files while `SKILL.md`'s *Gate/probe registry* names **44**
of them. Twenty-eight advertised instruments have no row, and one row claims a self-test the
script does not have. A stranger reading the lane cannot tell which advertised command is a
gate, what its verdict map is, or how to exercise it.

**Counting command (frozen).**

```sh
python3 plans/round52_c2_registry.py --lane .
```

**Before (base tip `30801b47`, measured 2026-10-28).**

```
ADVERTISED total=72
REGISTERED total=44 rows=46
MISSING 28
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 1     (`order-check`)
PREDICATE R52-C2 fail        (exit 1)
```

**After target.** `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`,
`PREDICATE R52-C2 pass`, exit 0.

**Frozen universe and rules.** `ADVERTISED` = every path matching
`plans/<name>.py` (depth 1 — `plans/fixtures/**` is support code, not an advertised
instrument), `corpus/evidence/<dir>/<name>.py` or `grader.py` that (a) exists at the tip and
(b) appears as `python3 <path>` in `SCORECARD.md`, `SKILL.md`, `LOG.md`, `corpus/README.md` or a
`corpus/knowledge/*.md` entry. `REGISTERED` = the same extraction restricted to the
`SKILL.md` *## Gate/probe registry* table. A row is *incomplete* when any of its eight cells is
empty; a row is *entry-missing* when its entry script is not in the tree; a row is
*selftest-unbacked* when its self-test cell names exactly one script and one `--flag` that the
named script does not accept (ambiguous cells are not counted, and a cell that says the
instrument has no self-test is accepted).

**Kill rule.** If any leg is non-zero at the after-run, R52-C2 is **not admitted** and operability
stays 8.

**Controls (each must fail the predicate).**

| control | what it does | must fail on |
|---|---|---|
| `c2-control-nothing` | base tip | `MISSING 28` |
| `c2-control-empty-cells` | a registry whose 28 new rows have blank cells | `INCOMPLETE 28` |
| `c2-control-drop-row` | remove one of the 28 new rows again | `MISSING 1` |
| `c2-control-false-selftest` | one row claims `--selftest` on a script without it | `SELFTEST-UNBACKED 1` |

**Causal separability.** C1's predicate reads the grader captures, the classifications, the
confirmation receipts and the prior-art file; it never reads `SKILL.md`'s registry. C2's predicate
reads the self-assessment files and the registry table; it never reads the grader captures. Each
verifies without the other having landed.

## Frontier step (§2b) — inside the claim cap

1. `corpus/SOURCES.md` is curated this round: rows are written only for sources **opened this
   round** (the TB2 tree at the pin, the captured grader files, the prior-art primaries), each
   with URL, access date and a ≤25-word located quote in the lesson's `## Gate` block. Rejections
   stay as rows with reason and flip condition. Census command (run at round start and round
   end, exit 0 required at round end):
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
2. One mistake is mined into `corpus/lessons/round-52.md` `## Mistakes`
   (class · evidence pointer · captured-by · fix), and the fix is shown able to fail.
3. **C1 is the sourced claim**: it rests on `SOURCES.md` rows opened this round (the TB2 pin and
   the prior-art primaries), cited by id in the knowledge entry and the lesson's Gate block.

## Round-51 closure routed defects (all four, §5 of the round contract)

| defect | route this round |
|---|---|
| D1 — `round51_surfaces.py` / `round51_routing.py` have no registry row | closed by C2 (both are in the 28 missing) |
| D2 — LOG round-51 says "63 of 64 seats wrote a report"; the committed results show 64 | append-only LOG correction line this round (not a claim) |
| D3 — C2 gate survivors (duplicate id, row deletion, `check:"true"`, `fixed-verified` on an open row, `source` naming a directory) | named in the lesson; the round's own counter must not reproduce them (mutation-tester seat) |
| D4 — SF01 `prose` reading is a recorded reading, not truth | named in the lesson as the open `vacuous` class; not claimed this round |

## Wave shape and seats

Two v1 waves (policy v1, band 32–64), total **64 seats**: wave 1 *build* (32) and wave 2
*falsify* (32), each wave ≥25 % attack seats (reviewer, critic, mutation-tester, labrat). The
canonical §3 planner seat is held by the L1 (the wave validator rejects `planner` as a swarm
role — orchestrator ruling 2026-10-19); a bounded planning data-walk rides a scout/connector
item instead, and that mapping is recorded in the report.
