author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 97 — non-author verifier spot-check

Reviewed lane tip: `3d52d89e25da2719e1138a95aa41644e83add422` (BASE `4992cd0e32b8db23ca20310deb7de12d485f8bcc`; P0 `5b41c1c3`; P1 `b2352135`; P2 `e40fd0c2`; freeze F `8d9d271306c4e7e2d586e51cd546652249d286cb`; measured T `f1083da60e7ff6b88f7420aae7424f7762d14700`; integration `2227bcf1`).
Report: fleet `.ufo/reports/round-97/kengaku.md`; prompt: fleet `.ufo/prompts/kengaku-round-97.md`.

Driver digest (`.ufo/watchdog.log`, copied 2026-11-06):
- `2026-11-06T00:59:17-03:00 launch kengaku round=97 pgid=3888144 driver=hyaku-inline attempt=1`
- `2026-11-06T01:32:12-03:00 complete kengaku round=97; hyaku-inline attempt=1`

Method. Plain measurements over committed bytes (`git show <rev>:<path>`, `jq`, `sha256sum`, `git merge-base --is-ancestor`, an independent Python registry census written by this reviewer), live re-opens with `curl`, one independent grader-semantics probe (`uvx -p 3.13 --with rdflib==7.1.4`, ephemeral uv cache only). No lane gate or claim instrument was executed (PROTOCOL §Gate standard, Closure consequence): their committed receipts were verified instead.

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report landed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-97/kengaku.md` (fleet) | `kengaku-shokunin aadd10fc669cb7f0ac638b01b3a53f876a370b4c` | ok |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]` with pointers | ok |
| cited hashes exist and are ancestors of `master` | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for all 7 cited hashes | all rc 0, all authored `kengaku-shokunin` | ok |
| lane pushed | `scripts/hyaku/jj-lane.sh state …` | `branch=master local=remote=3d52d89e… ahead=0 behind=0 tracked=0 untracked=2` | ok |
| leftovers | `git status --porcelain` | `?? .ufo/waves/round-97/w1.ready`, `?? …/w1.ready.dispatched` — orchestrator wave-dispatch handoff markers (`{"lane":"kengaku","round":97,"wave":"w1",…}`), not lane round work | non-lane leftover, noted |
| prompt carries template contract | grep §1 MISSION/AXES, §2 1–3 claims + lowest axis, §2b frontier, §3 L2 floor, §4 report path/sections/SHONEN/hash, §5 commit-then-push, push scope, L0 | all present | ok |
| marker vs report | report names 7 real committed hashes, evidence pointers, LOG `3673-3685` | real report | status `ok` |

Defects (status-neutral): the fleet prompt file was committed by `kengaku-shokunin` (`2083f14b`) rather than the integrator — attribution note only.

## 2. Claims re-check

### R97-C1 — coverage (lowest non-retired axis): fifteenth located replay `sparql-university`

Re-measured (not the lane instrument):
```
jq over plans/grader-population-ledger.json at each rev
4992cd0e len=88 executed=40 fa_total=76 fa_exec=31 sparql="unexecuted"
f1083da6 len=88 executed=41 fa_total=76 fa_exec=32 sparql="executed"
3d52d89e len=88 executed=41 fa_total=76 fa_exec=32 sparql="executed"
```
Matches reported ledger 40→41 / file-artifact 31→32 of 76. Freeze integrity re-derived: all 13 sha256 lines in `plans/round-97-claims.md` match `git show f1083da6:<p>` and `git show 3d52d89e:<p>` (instruments, captured grader bytes, SKILL.md, ledger, SOURCES.md) — no frozen byte changed after F. Replay verdict evidence-verified, not re-executed: `L1/c1-tip.txt` `LEGS L1..L9=pass`, `TARGET executed_rows=41 … cases=18 legs=72 mismatches=0 defects=0`, `PREDICATE R97-C1 pass`; negative controls `controls/c1-do-nothing.txt`, `c1-c2only.txt` (`executed_rows=40 … defects=7`) fail as declared. Independent semantics probe (below, §4) reproduces the knowledge entry's core finding. **Verified. coverage: improved.**

### R97-C2 — calibration: registry gate-kind/no-self-test mismatches 44→0

Re-measured with my own census (regex row parse of `SKILL.md`, first script in entry cell, loose spelling grep `--self-?test|run_selftest|'selftest'`):
```
base rows 168 gates 127 gate_no_selftest 42 probes 41
T    rows 171 gates 84  gate_no_selftest 0  probes 87
head rows 171 gates 84  gate_no_selftest 0  probes 87
flipped gate->probe 44; scripts changed among base rows: []
new rows: round97-sparql-probe (probe), round97-c1-replay (probe), round97-gate-selftest-census (gate, has --selftest)
```
My loose grep marks two of the 44 flipped rows as having a spelling (`round41-c1-mutants`, `round46-c2`); reading the bytes, both are false positives of my grep (`round41_c1_verify.py:194` quotes another tool's usage string; `round46_c2_verify.py:193` invokes `anchor_line_check.py --selftest`). Corrected count 44, matching `L1/c2-base.txt` `MISMATCH_TOTAL n=44` and `L1/c2-tip.txt` `n=0`. The registry effect is real and harmless (zero scripts changed, zero other cells changed).

**Not admitted, agreeing with the lane's honest stop.** The frozen predicate string requires `ROWS base=168 rev=171`; the committed `controls/c2-c2only.txt` (P2 `e40fd0c2`) prints `rev=169` — the two extra rows are C1's registry rows, and `n=0` at T also depends on C1 typing its two new rows `probe`. The declared C2 predicate therefore cannot be verified without C1 having landed (AXES "causally separable"). Additionally, lane criterion Q80 (two committed agreeing prefreeze runs per counter) was missed (lesson M3). MutC2 (`w1/MutC2.md`) shows the detector does not discriminate forged exact-block output; the finite 44→0 still stands on my own census. **Claim does not verify as declared. calibration axis: improved** (registry self-assessment now matches script bytes in 44 rows, nothing worsened), with admission withheld at round level.

### Harm check

`git diff 4992cd0e 3d52d89e -- SCORECARD.md`: append-only Round-97 section; scores coverage 7→7 (L0 cap), calibration 10→10, novelty 8 / depth 10 / operability 10 / freshness 10 / adjacency 9 held. Spot reads: SOURCES rows removed 0 (`git diff … corpus/SOURCES.md | grep -c '^-|'` → 0); `anchor-digest-check` already red, 80→86 findings because six new nested-path captures (S317–S322 layout) are not bound by the url-task rule (`w1/ScoutSources.md:142-147`) — the same bytes are pinned by C1's L2 and re-opened 9/9 live, so I rule this disclosed gate-layout debt, not freshness harm; historical r82 sweep 27→28 is a frozen-declaration delta that any new member produces (`w1/ConnectorOverlap.md:122-127`). No owned axis harmed.

| axis | verdict |
|---|---|
| coverage | improved |
| calibration | improved |
| novelty | unchanged |
| depth | unchanged |
| operability | unchanged |
| freshness | unchanged |
| adjacency | unchanged |

Round verdict: **rejected-honest-stop** (C2 does not verify as declared; no axis harmed).

## 3. Discernment spot-check (`corpus/lessons/round-97.md` §Gate)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S317 `tests/test_outputs.py` | admit (mined, A) | `curl …/2fd12b88…/sparql-university/tests/test_outputs.py` → 200, 2399 B, sha256 `ecf15840…07b39` (= row); `grep -n` line 79 `assert result_set == reference_set, (` | agree | Primary grader bytes; quote located at stated line; I independently ran a hardcoded `VALUES` query with a duplicate row and an extra projected column against the live `tests/university_graph_test.ttl` under rdflib 7.1.4: the test's set comparison passes (`True`, 5 rows) — C10/C11/C12 reproduced |
| S325 `README.md` | reject (B) | `curl …/README.md` → 200, 1697 B, sha256 `947086de…08d05` (= row); line 24 quote present verbatim (17 words) | agree | README §Verification restates instruction/test behaviour; no byte the grader or replay reads |
| S324 `task.toml` | reject (A) | `curl …/task.toml` → 200, 1007 B, sha256 `47a6f6dd…c9585` (= row); line 29 `docker_image = "alexgshaw/sparql-university:20251031"` | agree | Replay never pulls the prebuilt image; flip condition stated; tier A is right for an upstream manifest |

SOURCES row re-open: S317 row quote “assert result_set == reference_set, (” — 5 words (≤25), located `tests/test_outputs.py:79`, sha and size match live bytes. Rows 308→317 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` at 4992cd0e/3d52d89e), 8 A / 1 B, 6 mined / 3 rejected — matches report.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → only the 30 pre-existing W04 duplicate-url warnings (S040…S270) plus `kengaku ok …/corpus/SOURCES.md`, rc 0.

## 4. Trend verdicts

- **expansion: improved** — new `corpus/knowledge/tb2-sparql-university-grader.md` (`source: S317–S322`, `verified-at`, `recheck`) on ground the coverage map did not hold, indexed by the new Round-97 row in `corpus/README.md`; every cited row is `mined`; ledger 40→41 re-measured.
- **quality: unchanged** — no older entry re-verified or superseded; S318's time-stale mechanism sentence and S323 wording are marked by dated corrections in `corpus/lessons/round-97.md` (not left unmarked).
- **discernment: improved** — this outside spot-check agrees with the gate on one admit and two rejects; Q81 is grounded in lesson M1/M4.

## 5. Routed defects (lane fixes next round)

1. `anchor-digest-check` red 80→86: bind nested capture paths (or flatten captures) without editing frozen tools; the six round-97 captures are uncertified by the digest gate.
2. Successor calibration freeze must declare predicates over claim-local populations (no exact global row counts that embed a sibling claim) and commit two agreeing prefreeze runs per counter (Q80).
3. MutC2 survivors: detector must reject exact-block forgeries and the `add_parser` deletion mutant before any discrimination credit.
4. S318 mechanism wording (NOW() pass rests on undated students) and S323 wording: carry the dated correction into the next SOURCES-touching round without rewriting immutable rows.
5. Orchestrator markers `.ufo/waves/round-97/w1.ready{,.dispatched}` sit untracked in the lane repo; operator/orchestrator to decide whether to ignore or commit them.

SHONEN: all four boxes `[~]` with pointers; they look checkable by a non-author (replay receipts, LOG pointer, PROVINCE ruling) — promotion stays operator-owned.
