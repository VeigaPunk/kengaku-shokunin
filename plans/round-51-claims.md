# Round 51 — frozen claims (written before any scored measurement)

L1 `KengakuR51`, hyaku run 11, 2026-10-28. Lane: `kengaku-shokunin`. Base tip:
`297e17927ba9342a87ba27a48cc5270a001de7cb` (branch `master`).

Two claims, each one axis-move against a distinct axis, causally separable (different files,
different counter, neither needs the other to land). The lowest non-retired axis is **coverage 7**;
it is **not** claimed this round because its own recorded cap is open (`../.ufo/l0-questions.md`
lines 72 and 163, `kengaku | round-25` and `kengaku | round-33`: coverage stays capped at 7 until
the operator rules). The next-lowest band is the 8s — novelty, operability, freshness, adjacency.
This round works **freshness** and **adjacency**; the remaining 8s and the 9s are untouched.

Prior-art / instrument note: no model endpoint is available for a novelty probe. `:34113` is
absent (measured below); the only live OpenAI-compatible servers on this host are
operator-owned and belong to the serving plane this lane refuses (`PROVINCE.md` §Refusals,
`kama` owner). Round 51 is therefore an instrument-and-truth round, not a model round.

## C1 — freshness 8 → 9: every surface PROVINCE.md declares is machine-checked at the tip

**Surface changed:** `PROVINCE.md`'s two surface tables (`## Surfaces`, `### Core`) — the
document that tells a reader which host paths, endpoints, digests and counts this lane can
actually reach today.

**Instrument (frozen):** `plans/round51_surfaces.py` + `plans/round51-surfaces.json`.
The manifest carries one entry per table row: an anchor into the row, the truthful probed
`state` (`present`/`absent`), the recorded reading of what the row asserts (`prose`), the probe
spec, and an optional `count_claim` for rows that state a number. `prose` values are recorded
readings, audited row by row by wave seats; they are not inferred by the counter.

**Counting command (frozen):**

```sh
python3 plans/round51_surfaces.py --lane .
```

**Predicate:** exit 0 and final line `PREDICATE R51-C1 pass`, iff
`ANCHOR-DUP 0`, `ANCHOR-MISSING 0`, `UNCOVERED 0`, `SECTION-MISSING 0`,
`STALE 0` (probe agrees with recorded state),
`DRIFT 0` (recorded state agrees with what the row asserts),
`UNVERDICTED 0` (every absent row carries an `ABSENT <ISO date>` marker),
`NUMBER-DRIFT 0` (every `count_claim` equals the probed count),
and `RESOLVE observed_present >= resolve_floor` (floor `13`, the pre-repair count).

**Before (measured with this command at the base tip, receipt
`.ufo/waves/round-51/claims/c1-before.txt`):**
`ANCHORS 19/19`, `ROWS 9+10 covered`, `PROBES present=13 absent=6`,
`DRIFT 3` (SF01 llm-wiki, SF02 bench-arena, SF03 served model — rows still assert they resolve),
`UNVERDICTED 1` (SF04 route telemetry: `ABSENT` with no ISO date), `NUMBER-DRIFT 1`
(SF14: the Core row says the registry holds **25** rows, the probe counts **170**),
`RESOLVE present=13 floor=13 verdict=met`, `PREDICATE R51-C1 fail`, exit 1.

**After target:** `DRIFT 0`, `UNVERDICTED 0`, `NUMBER-DRIFT 0`, `STALE 0`, coverage 19/19 plus
one new declared surface (the live served endpoint found this round), `RESOLVE present>=13`,
`PREDICATE R51-C1 pass`, exit 0 — measured at the landing tip in a clean clone.

**Kill rule:** the claim fails if any control below passes the predicate, if the after
measurement does not print `pass` at the landing tip, or if the landing edit deletes a surface
row instead of dating it (`ROWS` per section must not fall below 9 and 10).

**Controls (each must fail; receipts under `.ufo/waves/round-51/claims/`):**
1. **declare-all-absent** — every entry `state=absent`, rows untouched: probes disagree with the
   recorded state (`STALE`) and the resolve floor is violated.
2. **drop-one-entry** — one row left uncovered: `UNCOVERED 1`.
3. **stale-pin** — an entry pins a digest that no longer matches: `STALE 1`.
4. **undated-absence** — an absent row stripped of its ISO date: `UNVERDICTED 1`.
5. **do-nothing** — the base tip itself: `PREDICATE fail` (measured above, exit 1).

## C2 — adjacency 8 → 9: every routed finding names its owner and its disposition

**Surface changed:** `corpus/routed-findings.jsonl` — the lane's record of cross-domain
evidence. Before this round a row records `id/class/source/opened_round/status/close/blocker/
check/note`: nothing says **which lane owns** the finding, nor whether this lane absorbed it or
routed it out. That is exactly the axis's signal (`AXES.md`: "cross-domain evidence is named
with its owner and routed, not absorbed"), and its cap ("unruled overlaps").

**Instrument (frozen):** `plans/round51_routing.py`.

**Counting command (frozen):**

```sh
python3 plans/round51_routing.py --lane . --run-checks
```

**Predicate:** exit 0 and final line `PREDICATE R51-C2 pass`, iff every row carries the full
field set (`id, class, source, opened_round, status, owner, disposition, close, blocker, check,
note`); every `owner` names a fleet lane from `../shokunin.conf` (or `unowned:integrator`);
every `disposition` is one of `fixed-verified | fixed-historical | routed | referral |
accepted-risk | refused-out-of-scope`; every `source` pointer resolves in the lane; every
`check` is a non-empty command; every `fixed-verified` row's check exits 0 **in this run**;
every `fixed-historical` row's `close` names a commit or path that resolves; and every
`routed`/`referral` row names a non-`kengaku` owner plus a `next` field.

**Before (measured at the base tip, receipt `.ufo/waves/round-51/claims/c2-before.txt`):**
`LEDGER rows=71`, `FIELDS complete=0 incomplete=71`, `OWNERS attributed=0 unattributed=71`,
`DISPOSITIONS set=0 bad=71`, `CHECKS present=61 absent=10`, `PREDICATE R51-C2 fail`, exit 1.

**After target:** `rows=71` (no row deleted, no row added without an owner),
`unattributed=0`, `bad=0`, `SOURCE missing=0`, `CHECKS absent=0`,
`CHECK_FAILED 0` over every `fixed-verified` row, `CLOSE_REF missing=0`, `NEXT violations=0`,
`PREDICATE R51-C2 pass`, exit 0 — measured at the landing tip in a clean clone.

**Kill rule:** the claim fails if any control passes, if the row count drops below 71 (rows are
state records; they are re-attributed, never deleted), if any `fixed-verified` check fails in the
run, or if the after measurement does not print `pass` at the landing tip.

**Controls (each must fail; receipts under `.ufo/waves/round-51/claims/`):**
1. **strip-owner** — one row without `owner`: `OWNERS unattributed=1`.
2. **fake-fix** — a row marked `fixed-verified` whose check is `false`: `CHECK_FAILED 1`.
3. **absorbed-routed** — a row marked `routed` but owned by `kengaku`: `NEXT violations=1`.
4. **empty-check** — a row with `check: ""`: `CHECKS absent=1`.
5. **do-nothing** — the base tip itself: `PREDICATE fail` (measured above, exit 1).

## Causality and separability

C1 touches `PROVINCE.md`, `plans/round51_surfaces.py`, `plans/round51-surfaces.json` and
`corpus/evidence/round51/`. C2 touches `corpus/routed-findings.jsonl`, `plans/round51_routing.py`
and `corpus/evidence/round51/`. Neither counter reads the other's files; either can land alone
and be scored alone.

## Stages

- **Stage 1 (this file, frozen before data):** claims, instruments, predicates, controls, kill
  rules, floors. Committed with both counters and the manifest.
- **Stage 2 (wave):** one v2 build-and-attack wave (64 seats) probes every surface independently,
  re-reads every `prose` value, attributes every ledger row with sibling evidence, runs every
  check, and attacks both counters.
- **Stage 3 (landing):** the L1 integrates the wave's evidence, lands the PROVINCE corrections
  (append-only: dated markers plus a new correction section), the ledger attribution, the
  knowledge entry and the lesson, then measures both predicates at the landing tip in a clean
  clone.

## Limits (declared before data)

- The counters measure **this lane's own declarations**. A surface nobody declared is invisible
  to C1; a finding nobody opened is invisible to C2. Neither claims completeness of the domain.
- `prose` is a recorded reading. A wrong reading is a wrong row, and the wave's critic seats are
  asked to falsify readings one by one.
- Endpoint probes are point-in-time: `:34113` was absent at measurement and may return; the
  counter's recorded state would then go `STALE` — that is the intended behaviour, not a defect.
- `--run-checks` executes 71 short shell commands from the ledger with a 60 s timeout each in a
  scratch cwd; a check that needs a network or a live model counts as failed.
- C1's resolve floor is a floor, not a target: adding a resolving surface raises the count, it
  never lowers it.

## Instrument amendment A1 — 2026-10-28, written before the scored after-measurement

Append-only. Three wave seats (`C2ExecG`, `C2ExecH`, `C2MutLedger`) and the survivor critic
(`CritSurvivor`) measured the frozen C2 counter against the real ledger before any scored
after-run, and found four instrument defects. The predicate legs are unchanged — none was added,
removed or weakened; only the environment the existing legs run in, and the owner universe they
validate against, are corrected. The C1 instrument is unchanged.

1. **Check cwd.** `check()` ran each `fixed-verified` row's check with `cwd=<scratch tmp>`, while
   61 of 61 pre-existing ledger checks are lane-relative. Measured: 6 pass under the scratch cwd,
   **43 pass under the lane root** (`C2MutLedger`, `CritSurvivor`). The counter now runs checks
   with `cwd=<lane>`; `$LANE` stays exported so a check that re-roots itself still works.
2. **Check timeout.** 60 s → 90 s. No check in the ledger came near either bound; the change
   removes a false-fail class for the two checks that shell out to a probe.
3. **Owner universe.** `load_owners()` matched `name: {` against `../shokunin.conf`, whose lane
   rows are `id|repo|axes`: measured **0 matches**, so seven real lane directories (`tsukuroi`,
   `revenger`, `mado`, `lore`, `audio`, `game-dev-2d`, `game-dev-3d`) were rejected as owners.
   The universe is now the curated set ∪ the `id|` rows of `shokunin.conf` ∪ every
   `*-shokunin` directory on disk (24 owners at measurement).
4. **`--ledger` path.** A relative `--ledger` raised `ValueError` in `relative_to`; the path is
   resolved first.

Disclosed consequence: the committed before-receipt (`claims/c2-before.txt`) is unaffected —
it recorded `VERIFIED ran=0`, because no row carried a disposition at that point, so no check ran
under either cwd. The after-measurement is the first run in which any check executes, and it runs
under this amendment.

## Ledger amendment A2 — 2026-10-28, written before the scored after-measurement

Append-only. §C2's after-target says `rows=71`. The landed ledger carries **75**: the 71 base rows
(all present, none deleted — verified as a subset by id) plus four rows this round opens for its own
cross-domain findings:

| id | finding | owner | disposition |
|---|---|---|---|
| R51-R1 | serving-plane identity pin for the live LFM3 server pair | `kama` | `routed` |
| R51-R2 | no sibling routed-findings ledger carries owner/disposition | `protocol` | `routed` |
| R51-R3 | three domain source trees absent operator-side | `unowned:integrator` | `routed` |
| R51-R4 | `qwen-coder.service` unit absent; `:34113` dead | `kama` | `routed` |

The predicate has no row-count leg, so the number is reconciled here, in the claim text, rather
than by shrinking the artifact: the C2 target is "every row attributed", and 75 rows are attributed.

Known survivors of the frozen predicate (measured by `C2MutLedger`, recorded, **not** fixed this
round because a rule changed after data is not the claim's rule): duplicate `id`, row deletion,
`check: "true"` as a `fixed-verified` check, `fixed-verified` on a `status: open` row, and a
`source` that names a directory. Next round's amendment adds the legs; the landed artifact contains
no instance of any of them (asserted in the round report).
