# C1CritDeclareAllAbsent — C1 control 1 (`declare-all-absent`), round 51

Seat: `C1CritDeclareAllAbsent` (critic, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Lane tip measured: `4090c3d` (stage-1 freeze `e07f131` + `4090c3d` "v2 wave spec (64 seats) +
validated dispatch payload"; `git diff e07f131..4090c3d` touches only `.ufo/waves/round-51/`
spec/dispatch files, so the frozen instrument and manifest are the freeze artifacts).

**Axes named.** C1's axis is **freshness** (8 → 9): "every surface `PROVINCE.md` declares is
machine-checked". I attacked that axis at three seams: (a) declaration vs probe (can a dishonest
manifest satisfy the predicate?), (b) the resolve floor's actual discriminating power, (c) the
`UNVERDICTED` leg's marker semantics. **Adjacency (C2) was not touched** — no C2 file was read
for scoring, no C2 control was run.

## Result in one line

Control 1 **fails as required**: exit 1, `PREDICATE R51-C1 fail`, `STALE 13` — one STALE for
each of the 13 surfaces the probe observes present. The claim is **not** dead. But the claims
file's *stated* expectation for this control is half wrong: the **resolve floor is not violated**
(`RESOLVE observed_present=13 floor=13 verdict=met`), because the counter counts *probes*, not
declarations.

## Fixture construction (scratch clone, uncommitted files only)

```
S=/fast/scratch/hyaku/kengaku-r51/C1CritDeclareAllAbsent
export TMPDIR=$S
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane
git -C $S/lane rev-parse --show-toplevel      -> $S/lane          (asserted before any write)
git -C $S/lane rev-parse master               -> 4090c3db79d11279ab5e5121ba25e74aa316e6e7
cmp lane/{PROVINCE.md,plans/round51-surfaces.json,plans/round51_surfaces.py}  -> all identical
sha256 lane/plans/round51_surfaces.py        = edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e
sha256 lane/plans/round51-surfaces.json      = 60d05a0a3f5b099061a902fac7612cd178c8dda01680ac04b84611a77fcf2dd8
sha256 lane/PROVINCE.md                      = 5e00336ff4ce2edb79346c4021e5bec24e5a6490ef5ccc53bd81fe5b6f7a5298
```

Control manifest (`plans/round51-surfaces-all-absent.json`, generated in scratch): every one of
the 19 entries had `state` and `prose` set to `absent`; `probe`, `count_claim`, `anchor`,
`sections`, `resolve_floor` untouched. Manifest diff vs the frozen file = 30 changed lines: 13
entries went `present/present` → `absent/absent` (2 lines each = 26), 3 entries (SF01–SF03) were
already `state=absent` so only their `prose` line changed (= 3), and 1 line is the control note
(= 30). The other 3 entries (SF04–SF06) were already `absent/absent` and are unchanged.

Control province (`PROVINCE-all-absent.md`): the row set was computed with the counter's **own**
`section_rows()` (imported from the frozen file), so the marked rows are exactly the rows the
counter polices; each of the 19 rows got `**ABSENT 2026-10-28**` appended inside its last cell.
Diff vs the lane file = 19 lines changed, 19 removed, 0 added — i.e. **append-only, no row
added, deleted or reordered**.

## Command and verbatim output (the receipt)

```
cd $S/lane
python3 plans/round51_surfaces.py --lane . \
  --manifest plans/round51-surfaces-all-absent.json --province PROVINCE-all-absent.md
```

Saved verbatim at `.ufo/waves/round-51/claims/control-c1-declare-all-absent.txt`
(30 lines, sha256 `5deaa1b737de9fe6eb04aefbe94541079530232e2e8ce935c2b42fd8a97a67d4`):

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces-all-absent.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 0
STALE 13
  DETAIL STALE SF07 probe=present state=absent (all 5 targets resolve)
  DETAIL STALE SF08 probe=present state=absent (all 1 targets resolve)
  DETAIL STALE SF09 probe=present state=absent (all 1 targets resolve)
  DETAIL STALE SF10 probe=present state=absent (digest 90c87c88… matches pin)
  DETAIL STALE SF11 probe=present state=absent (all 7 targets resolve)
  DETAIL STALE SF12 probe=present state=absent (digest 489f938a… matches pin)
  DETAIL STALE SF13 probe=present state=absent (all 1 targets resolve)
  DETAIL STALE SF14 probe=present state=absent (SOURCES rows=170)
  DETAIL STALE SF15 probe=present state=absent (digest 42d86d99… matches pin)
  DETAIL STALE SF16 probe=present state=absent (LISTEN on 127.0.0.1:8791)
  DETAIL STALE SF17 probe=present state=absent (all 2 targets resolve)
  DETAIL STALE SF18 probe=present state=absent (all 1 targets resolve)
  DETAIL STALE SF19 probe=present state=absent (all 1 targets resolve)
UNVERDICTED 0
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

### Exact failing lines

The predicate fails on exactly two legs, and only the first is attributable to the control:

- `STALE 13` + the 13 `DETAIL STALE …` lines above — **this is the control's own signal**: every
  surface whose probe resolves was declared absent. 13 STALE == `PROBES present=13`. The expected
  leg fired completely (13/13 actually-present surfaces, no misses).
- `NUMBER-DRIFT 1` (`SF14 row claims 25, probe says SOURCES rows=170`) — **inherited from the base
  state**, not caused by the control; it is present in the do-nothing baseline too (below).
- `PREDICATE R51-C1 fail` / exit 1.

Not failing: `DRIFT 0` (the control sets `prose` equal to `state` by construction),
`UNVERDICTED 0` (rows dated), `ANCHOR-* 0`, `UNCOVERED 0`, `SECTION-MISSING 0`, and —
**contrary to the claims text** — `RESOLVE verdict=met`.

Note the control is not a superset of the base failure: it *trades* the base's `DRIFT 3` for
`STALE 13`. Failing for a different set of legs is still failing; the kill rule is satisfied.

## Baseline (faithfulness check, same clone, frozen command unmodified)

```
cd $S/lane && python3 plans/round51_surfaces.py --lane .
-> exit 1; REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
   PROBES run=19 present=13 absent=6 errors=0
   DRIFT 3 (SF01, SF02, SF03)   UNVERDICTED 1 (SF04)   NUMBER-DRIFT 1 (SF14)
   RESOLVE observed_present=13 floor=13 verdict=met   PREDICATE R51-C1 fail
```

Byte-for-byte the same verdicts as `claims/c1-before.txt`, differing only in the `REV` line
(`297e179` → `4090c3d`). So the freeze instrument reproduces its own before-receipt on the current
tip, and the control's delta is exactly the two control files.

## Auxiliary probe (not a control receipt): what the floor actually catches

Same dated province copy, but a third manifest whose probes were also neutered — every entry's
probe replaced by a `paths` probe of a nonexistent scratch target, `count_claim` dropped,
`state=prose=absent`:

```
python3 plans/round51_surfaces.py --lane . \
  --manifest plans/round51-surfaces-neutered.json --province PROVINCE-all-absent.md
-> exit 1
   PROBES run=19 present=0 absent=19 errors=0
   DRIFT 0   STALE 0   UNVERDICTED 0   NUMBER-DRIFT 0
   ANCHOR-DUP 0   ANCHOR-MISSING 0   UNCOVERED 0   SECTION-MISSING 0
   RESOLVE observed_present=0 floor=13 verdict=violated
   PREDICATE R51-C1 fail
```

Every leg is clean except `RESOLVE`. This isolates the two guards: **STALE** stops declaration
flipping; **RESOLVE** stops probe weakening. They are disjoint, and the claims file conflates them.

## Findings

**F1 — the claims' control-1 expectation is false on the floor leg (freshness).** §C1 control 1
says the failure legs are "probes disagree with the recorded state (`STALE`) **and** the resolve
floor is violated". Measured: `RESOLVE observed_present=13 floor=13 verdict=met`. Cause: in
`check()` the counter increments `present` from `probe()` results, never from `e["state"]`
(`if observed == "present": present += 1`), so flipping declarations cannot move the floor. The
same false claim is asserted inside the frozen instrument's own docstring
(`plans/round51_surfaces.py`, module docstring): "declaring everything absent would drive
observed-present below the floor recorded before any repair" — it would not.
*Smallest safe correction (prose only, no code change):* in `plans/round-51-claims.md` §C1 control
1, state the expected legs as "`STALE` = every actually-present surface (13 at this tip), `DRIFT 0`,
`RESOLVE` unchanged/`met`", and correct the docstring sentence to "the floor bounds how many
surfaces may disappear from the host; it is not a declaration control — flipping entries to absent
leaves observed-present unchanged and is caught by STALE." **Do not** make `present` count declared
state: that would turn the floor into a tautology over the manifest and delete the guard F2 shows.

**F2 — the floor is load-bearing, but for the other attack (freshness).** F2 evidence is the
auxiliary run above: a manifest that neuters probes is caught by `RESOLVE` alone. Correct framing
for the landing write-up: `STALE` guards declaration honesty, `RESOLVE` guards probe honesty, and
neither substitutes for the other.

**F3 — nothing binds probe specs to the freeze (freshness; bounded, not blocking).** The predicate
constrains `state` and `prose` against the probe, and the probe against nothing. A landing could
redefine a probe and stay consistent. The bound is tight: to pass you need `present >= 13` **and**
zero STALE, so with the planned extra declared surface (→ 14 present) at most **one** existing
probe may be neutered, and none at all if the new surface does not probe present. Frozen probe-block
digest, computed over the sorted `(id, probe, count_claim)` tuples of all 19 entries:

```
REV e07f131cf703  probe-block sha256=f25436d8f3634f87426fd643bb7e15dff11d9cfa6388cf0e0d0a4b29b39c119b entries=19 floor=13
REV 4090c3db79d1  probe-block sha256=f25436d8f3634f87426fd643bb7e15dff11d9cfa6388cf0e0d0a4b29b39c119b entries=19 floor=13
```

*Smallest safe correction:* the landing receipt recomputes the per-id `(probe, count_claim)` map and
shows the 19 existing ids unchanged against `f25436d8…` (only a new entry may be appended). No
instrument change.

**F4 — `UNVERDICTED` is a presence-of-date check, not a this-round check (freshness; documentation
only).** Five of the six absent-state rows already carried dated markers before this control: rows
12/13/14 (SF01–SF03) carry `ABSENT 2026-10-20`, rows 16/17 (SF05, SF06) likewise; only SF04 (row 15,
`**ABSENT**` undated) lacked one — which is exactly the baseline's `UNVERDICTED 1`. So the control's
`UNVERDICTED 0` rests on pre-existing markers for SF01–SF03 and on my appended markers for the other
16. Predicate text is satisfied as written; the landing must not present `UNVERDICTED 0` as proof
that every absent row was re-dated this round.

**F5 — 10 of 19 probes resolve against the process cwd, not `--lane` (freshness; operational
fragility).** `paths`/`sha256` targets go through `expand()` (only `~`/`$` expanded) and are tested
with `Path.exists()`; only the `count` kind joins `lane`. Measured from `cwd=/` with `--lane` still
pointing at the clone:

```
PROBES run=19 present=3 absent=16 errors=0
STALE 10   (SF07, SF08, SF09, SF10, SF11, SF12, SF13, SF17, SF18, SF19)
RESOLVE observed_present=3 floor=13 verdict=violated
PREDICATE R51-C1 fail
```

A landing measurement taken from the wrong directory therefore produces a spurious `STALE 10` plus a
floor violation that *looks* like real drift. *Smallest safe correction for this round (prose):* the
frozen command's contract is `cd <clone> && python3 plans/round51_surfaces.py --lane .` — say so in
§C1, and have the landing receipt record the cwd. *Proposed for r52 (code, 2 lines):* resolve
`paths`/`sha256` targets against `lane` so `--lane` is authoritative; that is behaviour-preserving
under the frozen command (identical results at `cwd=lane`) and removes the trap. Not done here —
the instrument is frozen and a mid-round edit would break `c1-before` comparability.

## Limits

- One host, one point in time (2026-10-28): SF10/SF12/SF15 digests, SF14's 170 rows and SF16's
  `127.0.0.1:8791` listener were all present at `4090c3d`; a later probe may flip and would then
  legitimately report `STALE`.
- I ran only C1 control 1 and the one auxiliary variant. Controls 2–5 (drop-one-entry, stale-pin,
  undated-absence, do-nothing) are other seats' items; `claims/control-c1-drop-entry.txt` and
  `claims/control-c1-stale-pin.txt` appeared in the claims dir while I worked, but I did not read or
  rely on them.
- I did not audit any `prose` reading against its row text (the wave's per-row critic seats own that);
  my claim about `prose` is structural (it is a manifest field, so setting it alongside `state`
  makes `DRIFT` blind by construction), not a reading audit.
- The aux variant changes probes, so it is a demonstration of the floor's power, not a control the
  claims list; it is reported as auxiliary and is not filed as a control receipt.
- Read-only against the lane: I wrote only `claims/control-c1-declare-all-absent.txt` and this
  report. No commit, push, or mutating git/jj command anywhere; every fixture write was inside the
  scratch clone whose `rev-parse --show-toplevel` I asserted first.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C1CritDeclareAllAbsent` was removed before this report
  was written (`SCRATCH-REMOVED`); the receipt was copied out first and verified byte-identical
  (`cmp` clean). Free space seen at start: `/fast` 555G free (31% used).
- No tool installed or upgraded; no pacman transaction attempted.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

VERDICT: CONTROL 1 FAILS AS REQUIRED (exit 1, `PREDICATE R51-C1 fail`, `STALE 13` = all 13 actually-present surfaces) — the C1 claim is NOT dead; but the claims' stated expectation that the resolve floor is violated is FALSE (`RESOLVE observed_present=13 floor=13 verdict=met`, since the floor counts probes not declarations), so §C1 control 1 and the instrument docstring need the prose correction in F1 before landing.
