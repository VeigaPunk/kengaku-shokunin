# C2RevRecount — independent recount of the round-51 C2 ledger candidate

Seat: `C2RevRecount` (reviewer, leaf). Wave `kengaku-r51-w1`, lane `kengaku-shokunin`.
Axes named: **adjacency** (primary — the C2 axis: "cross-domain evidence is named with its owner
and routed, not absorbed"); **freshness** (C1 axis) — I measured nothing that bears on it.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

Lane HEAD I cloned and measured against; the stage-1 freeze is
`e07f131cf7037e58a21db6e1f3986cf401ad257c`. The C2 artifact and the C2 instrument both moved
while I measured — the artifact was rewritten four times (table below) and
`plans/round51_routing.py` plus `plans/round-51-claims.md` carry uncommitted working-tree edits
(amendments A1/A2). Every number below is bound to a sha256 and an mtime, and I state which
revision of the instrument produced it.

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
   the lane (`--ledger` outside `--lane` still crashes — F6), first with the committed instrument
   at REV 4090c3d, then with the amended working-tree instrument.

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

## The artifact moved four times while I measured

`.ufo/waves/round-51/w1/C2ExecLedgerMerge.jsonl`:

| # | sha256 (first 12) | mtime | rows | owners | dispositions | counter (committed instrument) |
|---|---|---|---|---|---|---|
| a | `60de71131ce1` | 15:22:44 | 71 | kengaku 9, unattributed 62 | fv 6 / ar 3 | `FIELDS complete=9 incomplete=62` → fail |
| b | `db970426d370` | 15:33:36 | 75 | 4 | fv 38 / ar 24 / fh 7 / routed 4 / refused 2 | `SOURCE missing=2` (at that instant) |
| c | `dfed00196319` | 15:34:04 | 75 | 4 | fv 41 / ar 28 / routed 4 / refused 2 | clean clone: `SOURCE missing=2`, `CHECK_FAILED 1` → **fail** |
| d | `08a8d2b0f5c1` | 15:38:13 | 71 | kengaku 71 | fv 42 / ar 24 / fh 3 / refused 2 | pristine clone, amended instrument: **pass** |

Revision (d) is the artifact at the time of writing. My recount of (d), in-lane:

```
ROWS 71
PARSE-BAD 0 []
IDS unique=71 duplicate=0
OWNERS distinct=1 unattributed=0
  OWNER kengaku 71
DISPOSITIONS distinct=4 unset=0 off-enum=none
  DISP fixed-verified 42
  DISP accepted-risk 24
  DISP fixed-historical 3
  DISP refused-out-of-scope 2
CHECK-EMPTY 0 []
SOURCE-MISSING 0 []
ROUTED-OR-REFERRAL-NO-NEXT 0 []
EXTRA-FIELDS {'owner': 71, 'disposition': 71, 'next': 28}
```

Revision (c), the last 75-row revision, recounted against the lane working tree:

```
ROWS 75   IDS unique=75   OWNERS distinct=4 (kengaku 71, kama 2, protocol 1, unowned:integrator 1)
DISPOSITIONS fixed-verified 41, accepted-risk 28, routed 4, refused-out-of-scope 2
CHECK-EMPTY 0   SOURCE-MISSING 1 [('R51-R2', 'corpus/lessons/round-51.md')]
ROUTED-OR-REFERRAL-NO-NEXT 0   next on 32 rows
```

Status × disposition (my cross-tab; the counter never computes it): in (c) `closed` 41 =
`fixed-verified`, `open` 31 = 27 `accepted-risk` + 4 `routed`, `blocked` 1, `refused` 2 — no
`open`+`fixed-verified` pair. An earlier revision (`db970426…`) had four: `R42-R3-33`,
`R42-R3-34`, `R45-S5-7b`, `R45-S5-7d`.

## Findings, by severity

### F1 — BLOCKER for the 75-row revision: its four new rows break the lane's own ledger reader, and the failure cascades into a `fixed-verified` check

`plans/routed_open.py` (the lane's round-close counter; its docstring fixes `source` as
`<lesson file>:<line>`) refuses a row whose `source` carries no `:line`. On revision (c):

```
$ python3 plans/routed_open.py --lane . --list ; echo rc=$?
DEFECT line=73 source must read <path>:<line>
DEFECT line=74 source must read <path>:<line>
ROWS total=75 invalid=2
rc=1
```

Lines 73 and 74 are `R51-R2` (`"source": "corpus/lessons/round-51.md"`) and `R51-R3`
(`"source": "corpus/evidence/round51/surfaces/paths.txt"`). `routed_open.py` withholds every
`ROW …` line when the file is invalid, so `R42-R2`'s check —
`cd "$LANE" && python3 plans/routed_open.py --lane . --list | grep -qE '^ROW R42-R2\.[12] status=closed' && test -f plans/scratch_guard.py`
— exits 1 while `R42-R2` is `fixed-verified`. That is the `CHECK_FAILED 1` in the (c) run, and it
is the C2 predicate failing for a reason unrelated to attribution. Reproduced directly:

```
$ LANE=$PWD bash -lc 'cd "$LANE" && python3 plans/routed_open.py --lane . --list | grep -E "^ROW R42-R2" ; echo "grep-rc=$?"'
grep-rc=1
```

The C2 counter cannot see this: its `SOURCE` leg only asks whether the file exists. Fix before
landing if the four rows return: give `R51-R2` and `R51-R3` `<path>:<line>` sources (`R51-R1`/
`R51-R4` already use `PROVINCE.md:14`/`:15`).

### F2 — HIGH: amendment A2 reconciles `rows=75`; the artifact now carries 71 rows and none of the four rows A2 tabulates

`plans/round-51-claims.md` (uncommitted, +27 lines) adds **A2**: the landed ledger "carries 75 …
the 71 base rows … plus four rows this round opens", with a table of `R51-R1..R4`
(`kama`/`protocol`/`unowned:integrator`, all `routed`). Revision (d), written at 15:38:13, has
**71 rows and zero `R51-*` ids**. One of the two is wrong at landing. A2's reasoning is sound and
the counter indeed has no row-count leg — but the artifact must match the amendment, or the
amendment must be withdrawn.

This matters beyond bookkeeping: the four `R51-*` rows are the **only** `routed`/`referral` rows
in any revision. In (d) distinct owners is back to **1** (`kengaku` 71/71) and the routing half of
the schema — `next` for routed rows, control 3 `absorbed-routed` — is exercised by nothing. The
adjacency gain then rests on a constant column, which cannot distinguish a right attribution from
a wrong one. Keep the rows (repaired per F1); do not ship (d).

### F3 — HIGH (pre-amendment, now addressed): the owner leg was enforced against a hardcoded list

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

A *correct* attribution to `tsukuroi` (host operability) or `revenger` (evidence discipline)
failed the predicate, so the claim's sentence "every `owner` names a fleet lane from
`../shokunin.conf`" was not what the counter checked. Amendment A1.3 replaces the regex with
`id|` parsing plus a `*-shokunin` directory glob and names the same seven lanes — my measurement
and the amendment agree independently. `FALLBACK_OWNERS` still lists `kumitate` three times.

### F4 — MEDIUM: the 57 `check` rewrites are now unnecessary and should be reverted

Base vs. revision (d): `check` identical on 4 rows (`R45-S5-4..7a`), authored on the 10 that were
empty, and **changed on 57**. Most are path qualification (`"$LANE/…"`, `cd "$LANE" &&`, added
`test -f … &&` guards); at least four change the predicate itself:

- `R39-R5`: `test ! -e /fast/scratch/hyaku/kengaku-r39` → `test -z "$(ls -d /fast/scratch/hyaku/kengaku-r39* 2>/dev/null)"`
- `R42-R3-21`: appended `&& [ "$(awk -F'|' '/^\| S[0-9]+/ && NF!=13' "$LANE/corpus/SOURCES.md" | wc -l)" -eq 0 ]`
- `R42-R3-22`: appended `&& sed -n 25p "$LANE/plans/registry_check.py" | grep -q "def parse_registry"`
- `R42-R3-25`: `grep … corpus/routed-findings.jsonl` → a `python3 -c` parse of the ledger itself

Those rewrites compensated for the old `cwd=<scratch>`; amendment A1.1 moves the check cwd to the
lane root, so they are no longer needed. Measured: a variant of (d) that keeps **the 61 base
`check` values verbatim** (only the 10 empty ones authored) passes under the amended instrument —

```
VERIFIED ran=42 passed=42 failed=0
PREDICATE R51-C2 pass
```

So the ledger can be re-attributed without rewriting a single frozen check. Recommendation:
revert the 57, keep the 10. This removes the "the seat that authored the check also certified it"
problem (`C2RevFieldLoss` owns the ruling; this is the measurement it needs).

### F5 — MEDIUM: amendment A1.4 is a partial fix — an outside `--ledger` still crashes

A1.4 says "A relative `--ledger` raised `ValueError` in `relative_to`; the path is resolved
first." Resolving helps only inside the lane. Measured against the amended instrument:

```
$ python3 plans/round51_routing.py --lane <clone> --ledger /fast/scratch/…/snap-1538.jsonl
  File "…/plans/round51_routing.py", line 77, in check
    print("LEDGER %s rows=%d" % (ledger.relative_to(lane), len(rows)))
ValueError: '/fast/scratch/…/snap-1538.jsonl' is not in the subpath of '…/lane2'
```

Traceback, no `PREDICATE … fail` line. A candidate outside the lane still cannot be measured, and
a crash is distinguishable from a failing predicate only by the missing final line. A
`try/except` around `relative_to` (or printing the absolute path) would close it.

### F6 — MEDIUM: amendments A1 and A2 are uncommitted edits to the frozen instrument and the frozen claims

At 15:39 the working tree showed `M plans/round51_routing.py`, `M plans/round-51-claims.md`,
`M corpus/SOURCES.md`, plus untracked `corpus/lessons/round-51.md`,
`corpus/evidence/round51/`, `corpus/knowledge/served-endpoint-identity-pin.md`. A1.1 changes the
*environment* the `fixed-verified` leg runs in (`cwd=<scratch>` → `cwd=<lane>`, timeout 60 → 90 s)
— the legs are unchanged but their meaning is not: the before-receipt recorded `VERIFIED ran=0`,
so no check ever ran under the frozen cwd, and the after-measurement will be the first run under
the amended one. That is disclosed in A1, and the ordering claim ("written before the scored
after-measurement") is not something I can verify from inside the wave. What I can verify: both
amendments must be committed with the landing, and the landing measurement must name which
instrument revision it used.

I checked one consequence of `cwd=<lane>`: whether running the checks dirties the measured tree.
After a full `--run-checks` pass in my clone, `git status --porcelain` showed only the files I had
copied in myself — no check wrote into the tree. So the measurement is non-mutating for this
ledger, measured, not assumed.

### F7 — LOW: two source pointers depend on files that were untracked at measurement time

`corpus/evidence/round51/surfaces/paths.txt` (15:35) and `corpus/lessons/round-51.md` (15:38)
existed only in the working tree. A clean clone sees neither: the counter reports
`SOURCE missing=2` for revision (c) in a clone, while my in-lane recount of (c) reports 1. For
revision (d) this is moot (no `R51-*` rows, `SOURCES resolved=71` in a pristine clone, measured).
If the four rows return, those two files must be committed, or the rows must point at committed
evidence.

## Limits

- I measured no C1 surface, digest or probe; nothing here bears on freshness.
- My source leg is file-existence only, the counter's rule. Line-level resolution (`path:line`
  really carries the finding) is `C2ExecSourceResolve`'s item and I did not repeat it.
- Check execution ran in my own `git clone --shared` of REV 4090c3d, not a clean `--no-local`
  clone of a landing tip (none exists). Host-dependent checks (`/fast/scratch/hyaku/kengaku-r39*`,
  network paths) reflect this host and this moment.
- The artifact was live while I measured; the merge seat had no report file at 15:36 and was still
  running. Revision (d) is the state at 15:38:13 and my numbers are bound to that sha; a later
  rewrite invalidates the numbers, not the method.
- I did not run `--run-checks` against revision (a): 62 rows were unattributed, so `FIELDS` fails
  before any check runs.
- I did not re-run the counter's `--selftest` against the amended instrument.

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r51/C2RevRecount` (NVMe), `TMPDIR` exported there;
`recount.py`, `merge.py`, the `--shared` clones, the snapshots and the counter runs lived there
and were removed before this seat yielded. Nothing citable was left behind: every number above is
re-derivable from the lane paths and the commands quoted verbatim.

VERDICT: RECOUNT CONFIRMS the mechanical legs — base 71 rows / 71 unique ids / 10 empty checks / 0 unresolved sources; my own merge of the eight fragments 71 rows, 71 unique ids, 0 unattributed, 0 empty `check`, 0 unresolved `source`, 0 `routed`/`referral` without `next`, base order preserved, fragments A..H contiguous with no gap or overlap — and REJECTS both live candidates as they stand. Revision `dfed0019` (75 rows) fails the frozen predicate in a clean clone (`SOURCE missing=2`, `CHECK_FAILED 1` on `R42-R2`) because its two new rows break `plans/routed_open.py` (`invalid=2`, `source must read <path>:<line>`), which the C2 counter's file-existence leg cannot see. Revision `08a8d2b0` (71 rows) passes the amended predicate (42/42 checks in a clone, `SOURCES resolved=71` in a pristine clone) but contradicts amendment A2, which tabulates four `R51-*` rows it no longer contains, and it drops the only `routed` rows — leaving a single distinct owner and no exercised routing leg. Also open: A1.4 still crashes on an outside `--ledger`; the 57 rewritten `check` values are unnecessary under A1.1 (a base-check variant passes 42/42) and should be reverted; A1 and A2 are uncommitted edits to a frozen instrument and a frozen claims doc and must land with the measurement that cites them.
