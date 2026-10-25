# Round 29 — attempt 2 (hyaku run 6, 2026-10-25) — frozen claims

Role: in-session L1 lane subagent of the hyaku orchestrator, one steered round. Attempt 1 of
round 29 landed 2026-10-21 (lane commits `31934e5`..`1f3b0f1`, fleet report commit `2ae9ba1c`
plus erratum `17d58281`) and was then held by the operator on source-history/credential-copy
disposition. Run 6 re-dispatched round 29; this attempt adds two new claims and never re-claims
attempt 1's generated-config projection.

Baseline revision for every before-measurement: the lane branch tip before this attempt's first
edit, `1f3b0f1ec41ec297130e8944ff97968d32324632`. Frozen before any seat ran.

## C1 — shokuknow assimilation: one admitted task-validity instrument entry (axis: coverage, expansion)

**Claim type:** assimilation + coverage on frontier ground the lane did not hold
(`corpus/README.md` §Frontier bullet 1: "per-benchmark task-validity checklist … unopened leads";
`PROVINCE.md` §Round28/29 partial admission: "named Terminal-Bench/Toolathlon/SWE-bench Pro specs …
generated configs, runtime task validity … remain open").

**Theme (one):** published per-task validity instruments that benchmark maintainers run on their own
tasks. One entry adopted from `/home/vgpnk/Projects/shokuknow/merge/kengaku/`.

**Target (frozen):** after the round
`python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census`
prints exactly

```
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
```

and exits 0.

Object under test: `corpus/knowledge/benchmark-task-validity-checklist.md`, citing exactly
`S077` (Harbor task-review automation), `S078` (SWE-bench Pro V2 release notes), `S079`
(Terminal-Bench 2.0 task schema), `S080` (Toolathlon-Verified), `S090` (Terminal-Bench 2.0
announcement) — the five rows the entry cites, appended to `corpus/SOURCES.md` with
`status=mined` and `used-by` naming the entry.

**Re-grounding duty (CORPUS.md rule 1):** every one of the five sources is re-opened in this round;
the entry and its Gate block carry this round's access date `2026-10-25` and a ≤25-word located
quote located by this attempt, never the campaign's `opened` date or quote.

**Kill rule (frozen):** if any of the five sources cannot be opened on 2026-10-25, or a required
≤25-word quote cannot be located in the opened bytes, that row is refused and the entry is refused
as a whole (an unadmitted entry is not partially appended). A refused entry is recorded with reason
and flip condition in `corpus/lessons/round-29.md` §Attempt 2 Gate, C1 reports the honest count,
and no substitute entry/row is admitted to reach the target.

**Control (do-nothing), run and committed before data:**
`python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json`
on the frozen tree → `entries=0 …` exit 1 (receipt `.ufo/waves/round-29/attempt2/control.nothing.txt`).
A do-nothing round therefore cannot reach the target.

## C2 — a standing source-adoption gate (axis: operability, capability acquisition)

**Claim type:** capability acquisition. The §10 adoption contract currently lives as ad-hoc shell
run by hand each round; it has no lane-side implementation and no failure-capable selftest. This
round lands `plans/sources_adopt.py`.

**What it must do (all four, each separately verifiable):**
1. id-collision detection against the lane registry using the census parser's own 0–3-leading-space
   row anchor (a column-zero-only pattern false-greens an indented collision);
2. staged-row schema check: exactly 11 columns, no literal or escaped `|` inside a cell, `status` in
   `{queued, mined, rejected}`, `recheck` a valid ISO date, `<N>d`, or a symbolic cadence;
3. append-block construction: prose `recheck` cells are normalized to the frozen access date with the
   stripped prose reported separately; `used-by` is rewritten to exactly the admitted entries citing
   the row; a row naming an unadmitted entry never reaches the block;
4. refusal with a non-zero exit for a missing requested id, an escaped pipe, a duplicate staged id,
   or a nonempty collision set.

**Target (frozen):** `python3 plans/sources_adopt.py --selftest` exits 0 printing ten `PASS` cases,
including (a) a 1-space-indented collision fixture that must yield a nonempty collision set,
(b) a 4-space-indented row that must *not* count (outside the census clause), (c) an escaped-pipe row
that must be refused, (d) a prose-`recheck` row that must normalize to `2026-10-25`, (e) a
dangling-`used-by` row that must be rewritten to the admitted set only.

**Before:** the tool does not exist at the baseline revision
(`git cat-file -e 1f3b0f1ec41ec297130e8944ff97968d32324632:plans/sources_adopt.py` exit 128).

**Kill rule (frozen):** if any of the ten cases cannot be made to fail on a deliberately broken
implementation, the case is not a control and C2 reports the honest count.

## Shared rules

- Each claim is causally separable: C2's selftest runs on built-in fixtures with no admitted entry
  present; C1's counter reads committed registry/entry bytes and needs no gate run.
- Axes named by the surface changed, not by the number produced. No axis may be harmed: the lane's
  existing gates (`grader.py`, `plans/round28_census.py`, the fleet source census) must still exit 0.
- Nothing here is an outside admit; author-side measurements only. Separate non-author closure
  decides admission.
- Distinctions preserved: this is not deployment config, runtime task validity, model performance,
  contamination measurement, or a new research method. It is the published instrument a maintainer
  runs, read from primary documents.

## Scope clarification appended 2026-10-25 (before the first C2 score)

C2's clause 4 says "refusal with a non-zero exit for ... an escaped pipe". The kengaku package
holds 173 staged rows, of which 2 (S093, S101) carry an escaped pipe, and neither is a row this
round adopts. A global refusal therefore blocks every targeted append on rows the round cannot
fix. The implemented reading is: the refusal applies to the rows under adoption
(`--admit-ids`); an unrequested malformed row is counted in `malformed_total` and never enters
the block. This scoping was implemented in the same file before any seat scored C2 (the
mutation-tester reported on the scoped revision, `505478fd…`), and selftest case 9 encodes it.
The stronger global refusal is not implemented and is not claimed. Recorded so the closure can
rule on it rather than discover it.
