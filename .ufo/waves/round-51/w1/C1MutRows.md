# C1MutRows — mutation test of the frozen C1 surface counter (round 51, hyaku run 11)

Seat: `C1MutRows` (mutation-tester). Lane: `kengaku-shokunin`. Judged axis: **freshness**
(R51-C1). Read first: `plans/round-51-claims.md` (full), then
`plans/round51_surfaces.py` (all 364 lines) and `plans/round51-surfaces.json`.

## Axes named

1. **freshness / R51-C1** — does the frozen counter actually machine-check what `PROVINCE.md`
   declares? (judged axis)
2. **instrument fidelity** — does a document-level defect reach a fired leg, or does the
   counter only ever re-read its own manifest?
3. **landing reachability** — can the *legitimate* repair (what the L1 must land) reach
   `PREDICATE R51-C1 pass` without deleting rows?

## Setup (scratch, disposable)

```sh
S=/fast/scratch/hyaku/kengaku-r51/C1MutRows; export TMPDIR=$S
mkdir -p "$S"; git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
D="$S/lane"; test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"   # -> TOPLEVEL_OK
git -C "$D" checkout -q -B master e07f131cf7037e58a21db6e1f3986cf401ad257c
```

Pristine hashes in the clone (before any mutation, and again after restore):

```
5e00336ff4ce2edb79346c4021e5bec24e5a6490ef5ccc53bd81fe5b6f7a5298  PROVINCE.md
60d05a0a3f5b099061a902fac7612cd178c8dda01680ac04b84611a77fcf2dd8  plans/round51-surfaces.json
edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e  plans/round51_surfaces.py
```

Content identity to the measured tree, proven not assumed:

- `git diff --stat 297e1792 e07f131c -- PROVINCE.md` → empty (the base tip the `c1-before`
  receipt was measured on has the **same** `PROVINCE.md` bytes).
- `git diff --stat e07f131c 4090c3d -- PROVINCE.md plans/round51_surfaces.py
  plans/round51-surfaces.json` → empty (HEAD differs from the freeze commit only by
  `.ufo/waves/round-51/*`).

Each case: `git -C "$D" checkout -- PROVINCE.md plans/round51-surfaces.json`, apply exactly one
mutation with a python one-shot, then run the frozen command from `$D`:

```sh
python3 plans/round51_surfaces.py --lane .
```

No tool was installed or upgraded (no pacman, no `uv tool`, no binary fetch).

## Baseline reproduction (deterministic, matches the committed receipt)

`00-baseline-pristine.txt` — verbatim:

```
EXIT 1
REV e07f131cf7037e58a21db6e1f3986cf401ad257c
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
STALE 0
UNVERDICTED 1
NUMBER-DRIFT 1
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

Identical legs to `.ufo/waves/round-51/claims/c1-before.txt` (DRIFT 3, UNVERDICTED 1,
NUMBER-DRIFT 1, present 13 / absent 6, exit 1). Because the baseline already fails, a mutant is
**killed** only when it fires a leg that the baseline does not — every verdict below is a delta
against this run.

## The five assigned mutants

| # | mutation | fired legs (delta vs baseline) | verdict |
|---|---|---|---|
| 1 | delete the SF08 row (`\| In-repo gate \| \`grader.py\` (repo root;`) | `ANCHOR-MISSING 1` (`SF08 anchor not found`), `ROWS ## Surfaces rows=8 entries=9` | **killed** |
| 2 | duplicate the SF09 row in place | `ANCHOR-DUP 1`, `UNCOVERED 2` (lines 20 **and** 21) | **killed** |
| 3a | SF14 row `25 rows` → `170 rows` (row text only) | **none** — `NUMBER-DRIFT 1` unchanged | **survived** (row number is never read) |
| 3b | 3a **plus** manifest `SF14.count_claim` 25 → 170 | `NUMBER-DRIFT −1` → `NUMBER-DRIFT 0` | leg cleared |
| 4 | append `**ABSENT 2026-10-28**` to the SF13 row (target present) | **none** | **survived** |
| 5 | swap the SF07 and SF08 rows | **none** | **survived** (benign) |

Verbatim legs:

`01-delete-SF08-row.txt`
```
ANCHORS total=19 dup=0 missing=1
ROWS section="## Surfaces" rows=8 entries=9 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
  DETAIL ANCHOR-MISSING SF08 anchor not found: | In-repo gate | `grader.py` (repo root;
PREDICATE R51-C1 fail
```

`02-dup-SF09-row.txt`
```
ANCHORS total=19 dup=1 missing=0
ROWS section="## Surfaces" rows=10 entries=9 uncovered=2
  DETAIL ANCHOR-DUP SF09 anchor appears 2 times
  DETAIL UNCOVERED ## Surfaces row line 20 has no manifest entry
  DETAIL UNCOVERED ## Surfaces row line 21 has no manifest entry
PREDICATE R51-C1 fail
```

`03a-count-170-row-only.txt` — the row now says `170 rows`, probe says `SOURCES rows=170`, and
the counter still prints:
```
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
```
`03b-count-170-row+manifest.txt` → `NUMBER-DRIFT 0` (same `DRIFT 3`/`UNVERDICTED 1` remain).

**Answer to "does NUMBER-DRIFT clear?" — No, not from the row.** `check()` compares
`e["count_claim"]` against the probe detail only (`plans/round51_surfaces.py:214-217`); the row's
own digits are never parsed. Editing the document to the truthful `170 rows` leaves
`NUMBER-DRIFT 1` standing, and the landing must change `count_claim` in
`plans/round51-surfaces.json` (3b). The inverse also holds — `03c` (manifest `count_claim` 170,
row deliberately wrong at `999 rows`) prints `NUMBER-DRIFT 0`: **a row whose number contradicts
the probe is invisible.** `DRIFT` is present/absent-only (`prose != state`), so no leg reads a
row's count.

`04-absent-marker-on-present.txt` and `05-reorder-SF07-SF08.txt` are byte-identical in legs to
the baseline (`ANCHORS total=19 dup=0 missing=0`, `ROWS 9/10 uncovered=0`, `DRIFT 3`,
`UNVERDICTED 1`, `NUMBER-DRIFT 1`). `UNVERDICTED` is one-directional
(`plans/round51_surfaces.py:207-211`: only `state == "absent"` rows are searched for an ISO date),
so a dated-absence marker on a *present* row is unverifiable, and row order is not pinned at all
(coverage is by line index, anchors by substring).

## Deletion probes — can row deletion ever pass?

All on top of a *repaired* manifest (the landing's edits, reproduced in scratch:
`SF01–SF03.prose = absent`, `SF14.count_claim = 170`).

**D0 — the obvious date rewrite breaks the anchor.** `repair()` + `**ABSENT**` →
`**ABSENT 2026-10-28**` in the SF04 row:
```
ANCHORS total=19 dup=0 missing=1
ROWS section="## Surfaces" rows=9 entries=9 uncovered=1
UNVERDICTED 1
  DETAIL ANCHOR-MISSING SF04 anchor not found: `~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT**
  DETAIL UNCOVERED ## Surfaces row line 15 has no manifest entry
PREDICATE R51-C1 fail
```
SF04's frozen anchor **embeds the literal `**ABSENT**`** (manifest entry `SF04.anchor`), so the
in-place date rewrite destroys the anchor. This is a landing constraint, not a counter defect:
the date must be appended while `**ABSENT**` survives.

**D0b — anchor-preserving repair reaches pass.**
`ls[i].rstrip() + " — **ABSENT 2026-10-28** (round 51 re-probe: still absent)"`:
```
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
DRIFT 0 / STALE 0 / UNVERDICTED 0 / NUMBER-DRIFT 0 / ANCHOR-DUP 0 / ANCHOR-MISSING 0 / UNCOVERED 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass
```
The predicate is reachable without deleting a row. (Receipt `D0b-repaired-anchor-preserved.txt`,
exit 0.)

**D1 — delete the undated absent row (SF04) *and* its entry: PASS.**
```
MANIFEST plans/round51-surfaces.json entries=18 sections=2
ROWS section="## Surfaces" rows=8 entries=8 uncovered=0
PROBES run=18 present=13 absent=5 errors=0
DRIFT 0 / UNVERDICTED 0 / NUMBER-DRIFT 0 / all anchors clean
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass
```
exit 0. This is the cheapest way to clear the only `UNVERDICTED` leg: drop the row and its
manifest entry instead of dating it. The claims' kill rule ("`ROWS` per section must not fall
below 9 and 10") is **not implemented in the counter** — it prints `rows=8` and passes.

**D2b — delete a dated absent row (SF05) + entry on a passing tree: PASS**, `rows=8`,
`present=13`, exit 0. (D2 shows the same deletion *failing* only because it reused the
anchor-breaking date edit from D0 — evidence that the anchor leg, not the deletion, is what fires.)

**D3 — delete a *present* row (SF08) + entry: fail, on the floor only.**
```
PROBES run=18 present=12 absent=6 errors=0
RESOLVE observed_present=12 floor=13 verdict=violated
PREDICATE R51-C1 fail
```
Every other leg is clean. So present-row deletion is blocked by `resolve_floor`, i.e. by a
**count**, not by identity.

**D4 — swap: delete SF05 (absent) *and* SF08 (present), add one new present surface
(`| Live shim endpoint | http://127.0.0.1:8791` + entry `SF20`, probe `port 8791`): PASS.**
```
MANIFEST plans/round51-surfaces.json entries=18 sections=2
ROWS section="## Surfaces" rows=8 entries=8 uncovered=0
PROBES run=18 present=13 absent=5 errors=0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass
```
exit 0, `rows=8`. A present surface can be deleted as long as some other present surface is
declared in the same edit; the counter cannot tell a correction from a swap.

**Answer: yes, row deletion can pass.** Precisely:
- deleting the row **alone** fires `ANCHOR-MISSING 1` (mutant 1) — the manifest entry is what
  makes a bare deletion visible;
- deleting the row **and its entry** passes whenever the surface is absent (D1, D2b) — and it
  *clears* the `UNVERDICTED` leg that the round's own claim exists to fix;
- deleting a **present** row and its entry fails only through `RESOLVE` (D3), and passes again if
  any other present surface is declared (D4).

The only guard against deletion in the *claim* is prose — the `ROWS >= 9 and 10` kill rule — and
the counter never evaluates it. If the L1 wants that kill rule machine-checked, it must be a new
leg (row-count floor per section), not a review step.

## Findings handed to the L1

1. **Land the SF14 number in the manifest, not (only) in the row.** `NUMBER-DRIFT` reads
   `count_claim`; the row's `25 rows → 170 rows` edit is decorative (3a). Land both.
2. **Do not rewrite `**ABSENT**` in the SF04 row.** Append the ISO date at the row tail (D0b
   recipe); rewriting in place fires `ANCHOR-MISSING 1` + `UNCOVERED 1` (D0).
3. **Dating is the only repair the counter rewards**; deletion is the cheaper one it also
   rewards (D1). The kill rule must be applied by the integrator, since the instrument cannot.
4. **`UNVERDICTED` is one-directional** (mutant 4): a stray `ABSENT <date>` on a present row is
   invisible. If the landing adds a "correction" marker to a resolving row, the counter will not
   complain and will not confirm.
5. **Duplicate rows fire two legs** (`ANCHOR-DUP 1` + `UNCOVERED 2`), because a duplicated
   entry never enters `anchor_line` (`plans/round51_surfaces.py:178-190`); the legs are not
   independent counts, so do not sum them as distinct defects.
6. **Row order is unconstrained** (mutant 5). Reordering is safe for the predicate and can never
   be detected, so the landing may reorder freely — and so may a defect.

## Limits

- One host, one point in time (2026-10-28). Port/HTTP probes (`:34113`, `:8791`) are
  point-in-time; the mutant verdicts do not depend on them (all runs reported
  `PROBES present=13 absent=6` except where a surface was added/removed by the probe itself).
- I mutated `PROVINCE.md` and (for D-cases and 3b/3c) the scratch copy of
  `plans/round51-surfaces.json` only. The counter source was never mutated — its own selftest was
  not re-run; that is `C1ExecSelftest`'s item, not mine.
- The D-case "repaired manifest" is my candidate reading of the landing, not the landing: the
  `prose` values I set are `absent` for SF01–SF03 because that is what the probes observed, and
  `count_claim=170` because that is what the SF14 probe counts. If the L1's landed `prose`
  differs, only the D-cases change, never the five assigned mutants.
- No C2 file was read beyond the claims text; the routing counter was not run.
- Baseline already fails, so "killed" here means "fires a leg the baseline does not"; a mutant
  that reproduces the baseline legs exactly is recorded as survived, even where the baseline
  failure is itself the reason the predicate is red.

## Restoration

After the last case the driver ran `git -C "$D" checkout -- PROVINCE.md
plans/round51-surfaces.json` and re-hashed: `PROVINCE.md 5e00336f…` and manifest `60d05a0a…` —
identical to the pre-mutation hashes above. The scratch clone at
`/fast/scratch/hyaku/kengaku-r51/C1MutRows` was removed before yield (disposable; the verbatim
run outputs are embedded above, so nothing citable lives outside this wave dir).

REV e07f131cf7037e58a21db6e1f3986cf401ad257c
VERDICT: 2 of 5 assigned mutants killed (1 delete-row-alone via ANCHOR-MISSING; 2 duplicate-row via ANCHOR-DUP+UNCOVERED) and 3 survived (3a row-only number edit — NUMBER-DRIFT does NOT clear; 4 dated marker on a present row — invisible; 5 reorder — benign); row deletion CAN pass the frozen predicate (D1 delete-undated-absent+entry exit 0, D2b delete-dated-absent+entry exit 0, D4 delete-present+add-present exit 0, all at rows=8 with the claims' ROWS>=9 kill rule unevaluated), the legitimate anchor-preserving repair reaches PREDICATE R51-C1 pass (D0b, exit 0), and the in-place `**ABSENT**` rewrite the landing would reach for first fires ANCHOR-MISSING 1 + UNCOVERED 1.
