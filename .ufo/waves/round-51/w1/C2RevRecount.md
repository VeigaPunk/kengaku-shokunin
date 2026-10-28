# C2RevRecount — independent recount of the round-51 C2 ledger candidate

Seat: `C2RevRecount` (reviewer, leaf). Wave `kengaku-r51-w1`, lane `kengaku-shokunin`.
Axes named: **adjacency** (primary — the C2 axis: "cross-domain evidence is named with its owner
and routed, not absorbed"); **freshness** (C1 axis) — I measured nothing that bears on it.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

Lane HEAD I cloned and measured against; the stage-1 freeze is
`e07f131cf7037e58a21db6e1f3986cf401ad257c`. The C2 artifact and the C2 instrument both moved while
I measured: the artifact was rewritten **five** times (table below), and `plans/round51_routing.py`
plus `plans/round-51-claims.md` carry uncommitted working-tree edits (amendments A1/A2). Every
number below is bound to a sha256 and an mtime, and I say which instrument revision produced it.

## Method (mine, stated before the numbers)

I took no number from the L1 or from any executor. I derived:

1. **My own merge** — `corpus/routed-findings.jsonl` (71 rows) overlaid with the eight fragments
   `C2Exec{A..H}.jsonl`: a fragment row replaces every field it carries except `id`; fields the
   fragment does not carry keep the base value; fragment order A..H.
2. **My own recount rules** — rows = non-empty JSONL lines that parse as objects; unique ids =
   `len(set(id))`; owners = `Counter(owner)` over non-empty owners; dispositions =
   `Counter(disposition)` over non-empty values, off-enum counted separately; empty `check` =
   missing/null/whitespace-only; source resolve = the token before the first `:` must exist under
   the lane (the counter's own rule); routed/referral without `next` = disposition in
   `{routed, referral}` and `next` missing/empty.
3. **The frozen counter**, pointed at a candidate ledger inside a scratch `git clone --shared` of
   the lane (`--ledger` outside `--lane` still crashes — F5), first with the committed instrument
   at REV 4090c3d, then with the amended working-tree instrument, both with and without
   `--run-checks`.

## Commands run (verbatim) and observed output

Base ledger — the before state, my own recount:

```
$ python3 recount.py <LANE> <LANE>/corpus/routed-findings.jsonl
ROWS 71
PARSE-BAD 0 []
IDS unique=71 duplicate=0
OWNERS distinct=0 unattributed=71
DISPOSITIONS distinct=0 unset=71 off-enum=none
CHECK-EMPTY 10 ['R40-R5', 'R42-R3-09', 'R42-R3-33', 'R42-R3-34', 'R42-R3-35', 'R42-R3-37', 'R45-S5-7b', 'R45-S5-7c', 'R45-S5-7d', 'R45-S5-7e']
SOURCE-MISSING 0 []
ROUTED-OR-REFERRAL-NO-NEXT 0 []
EXTRA-FIELDS {}
```

My own merge of base + the eight fragments:

```
$ python3 merge.py my-merge-full.jsonl
FRAGMENTS present=8 ['C2ExecA.jsonl', 'C2ExecB.jsonl', 'C2ExecC.jsonl', 'C2ExecD.jsonl', 'C2ExecE.jsonl', 'C2ExecF.jsonl', 'C2ExecG.jsonl', 'C2ExecH.jsonl']
FRAGMENTS missing=[]
FRAGMENT unknown-ids=none
MERGE rows=71 ids-unique=71
MERGE order-identical-to-base=True
OWNERS distinct=1 unattributed=0
  OWNER kengaku 71
DISPOSITIONS distinct=4 unset=0
  DISP fixed-verified 38
  DISP accepted-risk 24
  DISP fixed-historical 7
  DISP refused-out-of-scope 2
DISP off-enum=none
CHECK empty=0 []
SOURCE unresolved=0 []
ROUTED/REFERRAL without next=0 []
NEXT field present on 3 rows
```

Fragment coverage, derived from base indices (independent of any executor report):

```
A rows=9 indices=0..8   contiguous=True dupes=False unknown=none
B rows=9 indices=9..17  contiguous=True dupes=False unknown=none
C rows=9 indices=18..26 contiguous=True dupes=False unknown=none
D rows=9 indices=27..35 contiguous=True dupes=False unknown=none
E rows=9 indices=36..44 contiguous=True dupes=False unknown=none
F rows=9 indices=45..53 contiguous=True dupes=False unknown=none
G rows=9 indices=54..62 contiguous=True dupes=False unknown=none
H rows=8 indices=63..70 contiguous=True dupes=False unknown=none
covered rows=71 overlap-rows=none uncovered=[]
```

Frozen counter (committed instrument, REV 4090c3d) on **my** merge, in the clone, all checks run:

```
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=71 absent=0
VERIFIED ran=38 passed=38 failed=0
CLOSE_REFS resolved=7 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
```

Counter selftest at REV 4090c3d: `[selftest] cases=11 failures=0` / `ALL PASS`.

## The artifact moved five times while I measured

`.ufo/waves/round-51/w1/C2ExecLedgerMerge.jsonl`:

| # | sha256 (first 12) | mtime | rows | owners | dispositions | measured outcome |
|---|---|---|---|---|---|---|
| a | `60de71131ce1` | 15:22:44 | 71 | kengaku 9, unattributed 62 | fv 6 / ar 3 | committed instrument: `FIELDS complete=9 incomplete=62` → **fail** |
| b | `db970426d370` | 15:33:36 | 75 | 4 | fv 38 / ar 24 / fh 7 / routed 4 / refused 2 | `SOURCE missing=2` |
| c | `dfed00196319` | 15:34:04 | 75 | 4 | fv 41 / ar 28 / routed 4 / refused 2 | committed instrument, clean clone: `SOURCE missing=2`, `CHECK_FAILED 1` → **fail** |
| d | `08a8d2b0f5c1` | 15:38:13 | 71 | kengaku 71 | fv 42 / ar 24 / fh 3 / refused 2 | amended instrument, pristine clone: **pass** (but drops all four `routed` rows) |
| e | `cc5acda17ad8` | 15:38:54 | 75 | 4 | fv 41 / ar 28 / routed 4 / refused 2 | amended instrument, landing tip simulated: **pass**, 41/41 checks |

Revision (e) is the artifact at the time of writing. My recount of (e), in-lane:

```
ROWS 75
IDS unique=75   duplicates none
OWNERS distinct=4 unattributed=0
  OWNER kengaku 71
  OWNER kama 2
  OWNER protocol 1
  OWNER unowned:integrator 1
DISPOSITIONS distinct=4 unset=0 off-enum=none
  DISP fixed-verified 41
  DISP accepted-risk 28
  DISP routed 4
  DISP refused-out-of-scope 2
CHECK-EMPTY []
SOURCE-MISSING []
ROUTED-OR-REFERRAL-NO-NEXT []
next present on 32 rows
STATUS closed 41 / open 31 / blocked 1 / refused 2
open+fixed-verified []   (an earlier revision, db970426, had four: R42-R3-33, R42-R3-34, R45-S5-7b, R45-S5-7d)
```

The four routed rows, exactly as amendment A2 tabulates them:

```
R51-R1 | PROVINCE.md:15                              | kama               | routed | open
R51-R2 | corpus/lessons/round-51.md:1                 | protocol           | routed | open
R51-R3 | corpus/evidence/round51/surfaces/paths.txt:1 | unowned:integrator | routed | open
R51-R4 | PROVINCE.md:14                              | kama               | routed | open
```

At a simulated landing tip (clone of REV 4090c3d + the candidate ledger + the two untracked source
files committed), amended instrument, all checks run:

```
FIELDS complete=75 incomplete=0
OWNERS attributed=75 unattributed=0
DISPOSITIONS set=75 bad=0
SOURCES resolved=75 missing=0
CHECKS present=75 absent=0
VERIFIED ran=41 passed=41 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
```

and the lane's own reader is healthy there:

```
$ python3 plans/routed_open.py --lane . --list ; echo rc=$?
ROW R51-R1 status=open opened=51 source=PROVINCE.md:15
…
ROWS total=75 open=31 blocked=1 closed=41 refused=2
routed_open=32 oldest_round=39
rc=0
```

## Findings, by severity

### F1 — RESOLVED in revision (e), was a blocker in (c): the four new rows broke the lane's own ledger reader

In revision (c) the two new rows carried line-less sources (`corpus/lessons/round-51.md`,
`corpus/evidence/round51/surfaces/paths.txt`). `plans/routed_open.py` fixes `source` as
`<lesson file>:<line>` and refuses the whole file:

```
DEFECT line=73 source must read <path>:<line>
DEFECT line=74 source must read <path>:<line>
ROWS total=75 invalid=2   rc=1
```

Because it then withholds every `ROW …` line, `R42-R2`'s `fixed-verified` check —
`cd "$LANE" && python3 plans/routed_open.py --lane . --list | grep -qE '^ROW R42-R2\.[12] status=closed' && test -f plans/scratch_guard.py`
— exited 1: that is the `CHECK_FAILED 1` measured on (c). The C2 counter cannot see this class at
all, because its `SOURCE` leg only asks whether the file exists. Revision (e) adds `:1` to both
sources and the reader returns `rc=0` at the simulated landing tip (quoted above). Keep it that way.

### F2 — HIGH, live: the two source files are untracked, so a clean clone fails

`corpus/lessons/round-51.md` (15:38) and `corpus/evidence/round51/surfaces/paths.txt` (15:35) exist
only in the working tree. In a pristine clone of REV 4090c3d with revision (e) as the ledger:

```
SOURCES resolved=73 missing=2
DETAIL SOURCE R51-R2 source 'corpus/lessons/round-51.md' does not resolve
DETAIL SOURCE R51-R3 source 'corpus/evidence/round51/surfaces/paths.txt' does not resolve
DEFECT line=73 source file missing: corpus/lessons/round-51.md
DEFECT line=74 source file missing: corpus/evidence/round51/surfaces/paths.txt
ROWS total=75 invalid=2   rc=1
```

The claim is measured "in a clean clone at the landing tip". Both files must be committed with the
ledger (or the rows must point at committed evidence), or the predicate and the lane's own reader
both fail at landing. This is the one landing dependency that is not yet satisfied.

### F3 — MEDIUM, live: the 57 rewritten `check` values are unnecessary and should be reverted

Base vs. revision (e): `check` identical on 4 rows (`R45-S5-4..7a`), authored on the 10 that were
empty, **changed on 57**. Most are path qualification (`"$LANE/…"`, `cd "$LANE" &&`, added
`test -f … &&` guards); at least four change the predicate itself:

- `R39-R5`: `test ! -e /fast/scratch/hyaku/kengaku-r39` → `test -z "$(ls -d /fast/scratch/hyaku/kengaku-r39* 2>/dev/null)"`
- `R42-R3-21`: appended `&& [ "$(awk -F'|' '/^\| S[0-9]+/ && NF!=13' "$LANE/corpus/SOURCES.md" | wc -l)" -eq 0 ]`
- `R42-R3-22`: appended `&& sed -n 25p "$LANE/plans/registry_check.py" | grep -q "def parse_registry"`
- `R42-R3-25`: `grep … corpus/routed-findings.jsonl` → a `python3 -c` parse of the ledger itself

Those rewrites compensated for the old `cwd=<scratch>`; amendment A1.1 moves the check cwd to the
lane root. Measured on revision (e) with **every base `check` restored verbatim** (only the 10
empty ones and the 4 new rows' checks authored):

```
VERIFIED ran=41 passed=41 failed=0
PREDICATE R51-C2 pass
```

So the ledger can be re-attributed without rewriting a single frozen check. Recommendation: revert
the 57, keep the authored ones. This removes the "the seat that authored the check also certified
it" problem; the ruling on whether a rewritten `check` is an allowed field addition belongs to
`C2RevFieldLoss`, and this is the measurement it needs.

### F4 — MEDIUM, addressed by amendment but verify it lands: the owner leg was enforced against a hardcoded list

With the committed instrument, `load_owners()` matched `^\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{`
against a `shokunin.conf` whose lane rows are `id|repo|axes`: **0 matches**, so the owner universe
was exactly `FALLBACK_OWNERS`. Measured:

```
fallback only? True
CONF LANES 23: aggregator audio chousa game-dev-2d game-dev-3d kagi kaidoku kake kama kasegi
kengaku kotoba kotodama kumitate lore mado mori protocol revenger souji tabi tameshi tsukuroi
ACCEPTED 17: aggregator chousa kagi kaidoku kake kama kasegi kengaku kotoba kotodama kumitate
mori protocol souji tabi tameshi unowned:integrator
CONF-LANES-REJECTED-BY-COUNTER: audio game-dev-2d game-dev-3d lore mado revenger tsukuroi
```

Proved with a fixture (my merge, one row's owner changed, counter re-run in the clone):

```
owner=tsukuroi -> DETAIL OWNER R39-R1 owner 'tsukuroi' not a fleet lane | PREDICATE R51-C2 fail
owner=revenger -> DETAIL OWNER R39-R1 owner 'revenger' not a fleet lane | PREDICATE R51-C2 fail
owner=kumitate -> OWNERS attributed=71 unattributed=0 | PREDICATE R51-C2 pass
```

A *correct* attribution to `tsukuroi` (host operability) or `revenger` (evidence discipline) failed
the predicate, so the claim's sentence "every `owner` names a fleet lane from `../shokunin.conf`"
was not what the counter checked. Amendment A1.3 replaces the regex with `id|` parsing plus a
`*-shokunin` directory glob and names the same seven lanes — my measurement and the amendment agree
independently. `FALLBACK_OWNERS` still lists `kumitate` three times (harmless).

### F5 — MEDIUM, live: amendment A1.4 is a partial fix — an outside `--ledger` still crashes

A1.4 says "A relative `--ledger` raised `ValueError` in `relative_to`; the path is resolved first."
Resolving helps only inside the lane. Measured against the amended instrument:

```
$ python3 plans/round51_routing.py --lane <clone> --ledger /fast/scratch/…/snap-1538.jsonl
  File "…/plans/round51_routing.py", line 77, in check
    print("LEDGER %s rows=%d" % (ledger.relative_to(lane), len(rows)))
ValueError: '/fast/scratch/…/snap-1538.jsonl' is not in the subpath of '…/lane2'
```

Traceback, no `PREDICATE … fail` line: a candidate outside the lane still cannot be measured, and a
crash is distinguishable from a failing predicate only by the missing final line. A `try/except`
around `relative_to`, or printing the absolute path, closes it.

### F6 — MEDIUM, live: amendments A1 and A2 are uncommitted edits to a frozen instrument and a frozen claims doc

At 15:39 the working tree showed `M plans/round51_routing.py`, `M plans/round-51-claims.md`,
`M corpus/SOURCES.md`, plus the untracked files of F2 and `corpus/knowledge/served-endpoint-identity-pin.md`.
A1.1 changes the *environment* the `fixed-verified` leg runs in (`cwd=<scratch>` → `cwd=<lane>`,
timeout 60 → 90 s): the legs are unchanged, their meaning is not. The before-receipt recorded
`VERIFIED ran=0`, so no check ever ran under the frozen cwd and the after-measurement is the first
run under the amended one — disclosed in A1, but the ordering claim ("written before the scored
after-measurement") is not verifiable from inside the wave. Both amendments must be committed with
the landing, and the landing measurement must name the instrument revision it used.

One consequence of `cwd=<lane>` I did check: after a full `--run-checks` pass in my clone,
`git status --porcelain` showed only the files I had copied in myself — no check wrote into the
measured tree. Non-mutating, measured, not assumed.

### F7 — observation: A2 and revision (e) agree; revision (d) did not

A2 reconciles `rows=75` in the claim text and tabulates the four `R51-*` rows; revision (e) matches
that table exactly (owners, dispositions, `next`). Revision (d), written between them, had 71 rows
and none of the four — had it landed, A2 would have described rows that were not there. The four
rows are also the only `routed`/`referral` rows in any revision: with them, distinct owners is 4 and
the routing leg (`next` on routed rows, control 3 `absorbed-routed`) is exercised by data; without
them it is back to a single constant owner column that cannot distinguish a right attribution from
a wrong one. Keep them.

## Limits

- I measured no C1 surface, digest or probe; nothing here bears on freshness.
- My source leg is file-existence only, the counter's rule. Line-level resolution (`path:line`
  really carries the finding) is `C2ExecSourceResolve`'s item and I did not repeat it.
- Check execution ran in my own `git clone --shared` of REV 4090c3d, not a clean `--no-local` clone
  of a landing tip (none exists). Host-dependent checks (`/fast/scratch/hyaku/kengaku-r39*`,
  network paths) reflect this host and this moment.
- The artifact was live while I measured; the merge seat had no report file at 15:36 and was still
  running. Revision (e) is the state at 15:38:54 and my numbers are bound to that sha; a later
  rewrite invalidates the numbers, not the method.
- I did not run `--run-checks` against revision (a): 62 rows were unattributed, so `FIELDS` fails
  before any check runs.
- I did not re-run the counter's `--selftest` against the amended instrument.

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r51/C2RevRecount` (NVMe), `TMPDIR` exported there;
`recount.py`, `merge.py`, the `--shared` clones, the five snapshots and the counter runs lived
there and were removed before this seat yielded. Nothing citable was left behind: every number
above is re-derivable from the lane paths and the commands quoted verbatim.

VERDICT: RECOUNT CONFIRMS every mechanical leg I derived myself — base 71 rows / 71 unique ids / 10 empty `check` / 0 unresolved `source`; my own merge of the eight fragments 71 rows, 71 unique ids, 0 unattributed, 0 empty `check`, 0 unresolved `source`, 0 `routed`/`referral` without `next`, base order preserved, fragments A..H contiguous with no gap or overlap; the current artifact `cc5acda1` (75 rows) 75 unique ids, owners kengaku 71 / kama 2 / protocol 1 / unowned:integrator 1, dispositions 41 fixed-verified / 28 accepted-risk / 4 routed / 2 refused-out-of-scope, 0 empty `check`, 0 unresolved `source` in-lane, 0 routed without `next`. At a simulated landing tip (clone of REV 4090c3d with the two source files committed) the amended predicate prints `PREDICATE R51-C2 pass` with `VERIFIED ran=41 passed=41 failed=0`, and `plans/routed_open.py --list` returns `rc=0`, `invalid=0`, `routed_open=32 oldest_round=39`. One landing dependency is unmet: `corpus/lessons/round-51.md` and `corpus/evidence/round51/surfaces/paths.txt` are untracked, so a pristine clone fails both readers (`SOURCE missing=2`, `invalid=2`). Also live: the 57 rewritten `check` values are unnecessary under amendment A1.1 (a variant with every base `check` restored passes 41/41) and should be reverted; A1.4 still crashes on an outside `--ledger`; A1 and A2 are uncommitted edits to a frozen instrument and a frozen claims doc and must land with the measurement that cites them.
