# C1MutCounter — round 51, wave 1 (mutation tester, C1 counter)

Seat: `C1MutCounter`. Item: mutate the C1 counter one leg at a time in scratch, run `--selftest`
and the real check for each mutant, name the killer selftest case (or the coverage hole).

## Axes named

- **A1 — leg liveness**: does each of the five behaviour-bearing legs of `plans/round51_surfaces.py`
  change an observable output when removed, and is that change an *exit-code* change or only a
  counter/detail change?
- **A2 — killer coverage**: which detector arm (`--selftest` case, or the frozen counting command)
  is the one that kills the mutant; a leg with no killer in either arm is a hole.
- **A3 — restoration fidelity**: the lane instrument is byte-identical before and after the probe
  (mutants live only in scratch).

## Revision measured

`REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` (lane `master`, working tree at
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`).

Instrument identity vs the stage-1 freeze commit `e07f131cf7037e58a21db6e1f3986cf401ad257c`:

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --stat e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD -- \
  plans/round51_surfaces.py plans/round51-surfaces.json PROVINCE.md
# (empty output)
sha256sum plans/round51_surfaces.py
# edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e  plans/round51_surfaces.py
```

So the mutated bytes are the frozen bytes: the instrument is unchanged between the freeze commit and
the measured tip.

## Baseline (pristine instrument, before any mutation)

```sh
export TMPDIR=/fast/scratch/hyaku/kengaku-r51/C1MutCounter
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 plans/round51_surfaces.py --selftest          # exit 0
python3 plans/round51_surfaces.py --lane .            # exit 1
```

`--selftest` tail:

```
[selftest] cases=9 failures=0
[selftest] ALL PASS
```

`--lane .` verbatim:

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

This reproduces the frozen before receipt (`.ufo/waves/round-51/claims/c1-before.txt`): `DRIFT 3`,
`UNVERDICTED 1`, `NUMBER-DRIFT 1`, `RESOLVE 13/13 met`, `fail`, exit 1. Baseline is **green for the
selftest arm and red for the counting arm**, which is the precondition for reading the mutant table
below (a red baseline cannot kill anything by exit code).

## Method

One scratch copy of the instrument per leg (`cp` of the frozen file), one minimal edit each, then both
arms run against the *real* lane tree with cwd = lane root, so the real arm is byte-for-byte the frozen
command with only the mutated body swapped in:

```sh
python3 /fast/scratch/hyaku/kengaku-r51/C1MutCounter/m<N>.py --selftest
python3 /fast/scratch/hyaku/kengaku-r51/C1MutCounter/m<N>.py --lane .
```

Selftest case numbering (order of `run()` calls in `_selftest`): case 1 = S0 consistent pass,
2 = S1 drift, 3 = S2 stale, 4 = S3 unverdicted, 5 = S4 number drift, 6 = S5 uncovered,
7 = S6 duplicate anchor, 8 = S7 floor violated, 9 = S8 missing anchor.

## Mutant table

| # | leg removed | mutant sha256 | `--selftest` | killer case | `--lane .` | real-arm delta |
|---|---|---|---|---|---|---|
| M1 | `prose != state` → `DRIFT` append | `1a9bb02a27884f2143db1839b4e70be55816e40a4e83e069daff7e45e30577b9` | exit 1, `failures=1` | **case 2 (S1 drift)** | exit 1, `fail` | `DRIFT 3 → 0` (exit unchanged) |
| M2 | `count_claim` comparison → `NUMBER-DRIFT` | `18307d122369ce3b3423e4f7bf120530f5626a583f16e97d769b78abe3d0655e` | exit 1, `failures=1` | **case 5 (S4 number drift)** | exit 1, `fail` | `NUMBER-DRIFT 1 → 0` (exit unchanged) |
| M3 | resolve-floor comparison (`present >= floor`, `if present < floor: ok = False`) | `eaef6fd04802b980d1bf5216e9d9fdc3d40ae6827eab6afe1ee50085acd14a1b` | exit 1, `failures=1` | **case 8 (S7 floor violated)** | exit 1, `fail` | **none — stdout byte-identical to baseline** |
| M4 | `ABSENT <ISO date>` check → `UNVERDICTED` | `f1beee996e9013896c6e83612211d4d8465e8f1d27f0f31a187e25e88aa44e96` | exit 1, `failures=1` | **case 4 (S3 unverdicted)** | exit 1, `fail` | `UNVERDICTED 1 → 0` (exit unchanged) |
| M5 | `section_rows` section boundary (`if started: break` on a heading) | `45348df67cd616e92247ff58f48a78062ad6986bcff089ff235df944feb4f2b1` | exit 1, `failures=1` | **case 1 (S0 consistent pass)** | exit 1, `fail` | **none — stdout byte-identical to baseline** |

Killed 5/5 by `--selftest`. Killed 0/5 by the frozen counting command's exit code.

### Per-mutant evidence

M1 (drift append deleted), selftest:

```
[selftest] cases=9 failures=1
[selftest] FAIL case 2 expected fail, got pass
[selftest] FAILED
```

M2 (count_claim comparison deleted):

```
[selftest] cases=9 failures=1
[selftest] FAIL case 5 expected fail, got pass
[selftest] FAILED
```

M3 (resolve floor deleted):

```
[selftest] cases=9 failures=1
[selftest] FAIL case 8 expected fail, got pass
[selftest] FAILED
```

M4 (ABSENT-date check deleted):

```
[selftest] cases=9 failures=1
[selftest] FAIL case 4 expected fail, got pass
[selftest] FAILED
```

M5 (section boundary ignored):

```
[selftest] cases=9 failures=1
[selftest] FAIL case 1 expected pass, got exit 1
[selftest] FAILED
```

Real arm, `diff baseline-real.txt m<N>-real.txt`:

- M1: `DRIFT 3` → `DRIFT 0`, detail lines gone; every other line identical; exit 1 both.
- M2: `NUMBER-DRIFT 1` + detail → `NUMBER-DRIFT 0`; exit 1 both.
- M3: **no diff** (`diff` empty).
- M4: `UNVERDICTED 1` + detail → `UNVERDICTED 0`; exit 1 both.
- M5: **no diff** (`diff baseline-real.txt m5-real.txt` → empty; `M5_REAL_IDENTICAL_TO_BASELINE`).

Diff hunks applied (one per file, nothing else touched):

```diff
--- M1
-        if e["prose"] != e["state"]:
-            problems["DRIFT"].append("%s prose=%s state=%s (%s)" % (e["id"], e["prose"], e["state"], e.get("why", "")[:80]))
+        # MUTANT-1: prose != state drift append deleted
--- M2
-        if "count_claim" in e:
-            m = re.search(r"(\d+)", detail)
-            if not m or int(m.group(1)) != int(e["count_claim"]):
-                problems["NUMBER-DRIFT"].append("%s row claims %s, probe says %s" % (e["id"], e["count_claim"], detail))
+        # MUTANT-2: count_claim comparison deleted
--- M3
-    verdict = "met" if present >= floor else "violated"
+    verdict = "met"  # MUTANT-3: resolve-floor comparison deleted
     print("RESOLVE observed_present=%d floor=%d verdict=%s" % (present, floor, verdict))
-    if present < floor:
-        ok = False
--- M4
-        if e["state"] == "absent":
-            line = text[anchor_line[e["id"]]] if e["id"] in anchor_line else ""
-            if not ABSENT_RE.search(line):
-                problems["UNVERDICTED"].append("%s row has no ABSENT <ISO date> marker" % e["id"])
+        # MUTANT-4: ABSENT-date check deleted
--- M5
-        if line.startswith("#"):
-            if started:
-                break
-            continue
+        if line.startswith("#"):
+            continue  # MUTANT-5: section boundary ignored
```

## Findings

**F1 — no leg is a coverage hole; `--selftest` is the sole killer for all five.** Each leg has a
dedicated selftest case, and each case is the *only* thing that changes exit code under its mutant:
M1↔S1, M2↔S4, M3↔S7, M4↔S3, M5↔S0. The mapping is one-to-one and non-overlapping: no leg relies on a
case that some other leg also trips, so the selftest suite is a genuine per-leg detector, not one
catch-all assertion.

**F2 — the frozen counting command kills 0/5, and cannot kill any of them at the after tip either.**
This is not an accident of the before tip being red. Two mechanisms, both measured or forced by the code:

- M1/M2/M4 only *append to a problem list*; their removal is unobservable exactly when the list is
  empty, i.e. at a tree where the predicate passes. At the before tip they show as counter deltas
  (`DRIFT 3→0`, `NUMBER-DRIFT 1→0`, `UNVERDICTED 1→0`) but the exit code is already 1.
- M3/M5 leave the real-arm stdout **byte-identical** even at the before tip, so no tree state
  distinguishes them through this arm.

Consequence for the claim, stated for the L1: `PREDICATE R51-C1 pass` at the landing tip is compatible
with a counter whose resolve-floor comparison (M3) and section-boundary guard (M5) have been deleted,
and with a counter that never appends DRIFT/NUMBER-DRIFT/UNVERDICTED (M1/M2/M4) — because at a passing
tree those appends produce no output. The claim's predicate therefore needs `python3
plans/round51_surfaces.py --selftest` (exit 0, `cases=9 failures=0`) recorded *in the same receipt* as
the `--lane .` pass, or the C1 after-measurement does not discriminate an enforcing counter from a
neutered one. I did not edit the claim, the counter, or the manifest — this is a finding for the L1.

**F3 — why M5 is invisible to the real arm (structural, measured).** `section_rows` has two stoppers:
`if started: break` on the next heading, and `elif started and line.strip(): break` on the first prose
line after the table. In `PROVINCE.md` the tables are terminated by prose *before* the next heading
(`## Surfaces` table ends at line 20, line 22 is `## Refusals…`, line 24 is the first prose bullet;
`### Core`'s table is likewise followed by the `*Round-25 correction …*` paragraph). The prose stopper
always fires first, so the heading-break branch is unreachable on the real document and deleting it
changes nothing. It is exercised only by the synthetic fixture in S0 (heading-separated tables, no
prose between them) — which is why the killer for M5 is the happy-path case and not an error case.
If a future edit ever removes the prose between two tables, M5 would become live in the real arm with
no selftest case shaped like that layout; today it is a dead branch in production and a live branch in
the fixture.

**F4 — lane working tree was not fully clean during measurement (pre-existing, not mine).**
`git status --porcelain plans/ PROVINCE.md corpus/` reports `M plans/round42_c1_verify.py`,
`M plans/routed_open.py`, `M plans/scratch_guard.py`. None of the three is imported, executed, or read
by `round51_surfaces.py` (stdlib-only; its read set is `plans/round51-surfaces.json`, `PROVINCE.md`,
`corpus/SOURCES.md`, host paths). `plans/round51_surfaces.py` itself is unmodified (sha above equals
the freeze). Recorded so the L1 can attribute those edits elsewhere.

## Restoration

The lane instrument was never written to. Mutants existed only under
`/fast/scratch/hyaku/kengaku-r51/C1MutCounter/`; the frozen file's sha256 is
`edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e` both before and after the probe
(first and last `sha256sum` of this seat agree), and `git diff` of the instrument against the freeze
commit is empty. The scratch directory, including the five mutants and their receipts, was removed
after the evidence above was transcribed into this file.

## Limits

- Probes in the real arm are point-in-time (port probes 1.5 s timeout, http probes 3 s timeout);
  the `present=13 absent=6` split matches the frozen receipt exactly at this tip, so no probe flapped
  during the runs.
- I mutated only the five legs named in the item. The other guards (`ANCHOR-DUP`, `ANCHOR-MISSING`,
  `UNCOVERED`, `SECTION-MISSING`, `STALE`, and the `errors` counter that is printed but never
  incremented) were not probed by this seat; `errors` is visibly dead in the code (`errors = 0` with no
  increment path) and is unclaimed by any selftest case — flagged for whoever owns the adjacent leg.
- Selftest case→leg mapping is read from the source ordering, not from labels (cases are unlabelled;
  the source comments call them S0–S8).
- No model endpoint was used; no network beyond the lane's own declared probes.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

VERDICT: C1 counter is mutation-sound under `--selftest` — 5/5 named legs killed, each by its own
dedicated case (M1→S1, M2→S4, M3→S7, M4→S3, M5→S0), no leg without a killer; but the frozen counting
command alone kills 0/5 and, at any passing tree, cannot kill M1/M2/M3/M4/M5 at all, so the C1 after
receipt must carry the `--selftest` line or the pass is not discriminating (finding F2). Lane
instrument byte-identical before and after; scratch removed.
