# C1CritUndated — C1 control 4 (`undated-absence`), round 51

Seat: `C1CritUndated` (critic, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Measured revision: `4090c3db79d11279ab5e5121ba25e74aa316e6e7` (lane HEAD). Stage-1 freeze
`e07f131cf7037e58a21db6e1f3986cf401ad257c` is its parent; `git diff --stat e07f131..HEAD` touches
only `.ufo/waves/round-51/{build_spec.py,w1-dispatch.json,w1-spec.json}`, so `PROVINCE.md`,
`plans/round51_surfaces.py` and `plans/round51-surfaces.json` are the freeze artifacts.

**Axes named.** **Freshness** (R51-C1, 8 → 9): "every surface `PROVINCE.md` declares is
machine-checked". I attacked one seam of it — the `UNVERDICTED` leg, i.e. the only part of the
predicate that speaks about *when* an absence was established. **Adjacency (C2) was not touched**:
no C2 file read for scoring, no C2 control run, no ledger row inspected. Coverage was not touched.

## Result in one line

Control 4 **fails as required** (exit 1, `PREDICATE R51-C1 fail`, `UNVERDICTED` names the stripped
row). But two things the item/claims assert are not true as written at this revision: (a) the
literal one-edit recipe prints `UNVERDICTED 2` (SF04 **and** SF05), not `UNVERDICTED 1` naming SF05 —
`UNVERDICTED 1` requires the after-shape, where SF04 is already dated; and (b) the date leg is a
**presence-and-shape** check, not a freshness check — a stale `ABSENT 2019-01-01` and a future
`ABSENT 9999-12-31` both pass it, and a full-pass fixture carrying a 2019 date reaches
`PREDICATE R51-C1 pass`, exit 0.

## Commands run

```
S=/fast/scratch/hyaku/kengaku-r51/C1CritUndated ; export TMPDIR=$S
mkdir -p $S
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane
git -C $S/lane rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r51/C1CritUndated/lane
git -C $S/lane rev-parse HEAD              -> 4090c3db79d11279ab5e5121ba25e74aa316e6e7
git -C $S/lane log --oneline -8            -> 4090c3d … e07f131 … 297e179 …
git -C $S/lane merge-base --is-ancestor e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD -> true
git -C $S/lane diff --stat e07f131..HEAD   -> 3 files, all .ufo/waves/round-51/ spec+dispatch
cd $S/lane && python3 plans/round51_surfaces.py --lane .        # baseline, equals c1-before.txt
cp -a --reflink=auto lane lane-a ; cp -a --reflink=auto lane lane-b ; cp -a --reflink=auto lane lane-undated
git -C $S/lane-a rev-parse --show-toplevel -> $S/lane-a          (same for -b, -undated)
# section A: lane-a, PROVINCE.md:16  **ABSENT 2026-10-20** -> **ABSENT**
cd $S/lane-a && python3 plans/round51_surfaces.py --lane .
# section B: lane-b, PROVINCE.md:15  **ABSENT** -> **ABSENT 2026-10-28**,
#            PROVINCE.md:16  **ABSENT 2026-10-20** -> **ABSENT**,
#            plans/round51-surfaces.json:57  anchor "`~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT**"
#                                            -> "`~/Projects/bounties/ledger/telemetry.jsonl` — "
cd $S/lane-b && python3 plans/round51_surfaces.py --lane .
# date-leg probes: lane-undated (anchor shortened) with SF04 = **ABSENT** 2026-10-28 / 2019-01-01
cd $S/lane-undated && python3 plans/round51_surfaces.py --lane .
# fixtures: $S/fx-{dated-today,stale-2019,stale-future,undated}/{PROVINCE.md,m.json}
python3 lane/plans/round51_surfaces.py --lane fx-stale-2019 --manifest fx-stale-2019/m.json --province fx-stale-2019/PROVINCE.md   (and the other three)
```

Baseline at the clone tip reproduces `claims/c1-before.txt` line for line except `REV`
(`DRIFT 3`, `UNVERDICTED 1` SF04, `NUMBER-DRIFT 1`, `RESOLVE present=13 floor=13 verdict=met`,
exit 1) — the freeze artifacts are intact.

Receipt written: `.ufo/waves/round-51/claims/control-c1-undated.txt` (item-named path; the
directory held only `c1-before.txt` and `c2-before.txt` before this write). It carries sections A
and B verbatim plus the three attack probes.

## Section A — the item's literal recipe, verbatim

One edit: `PROVINCE.md:16` `**ABSENT 2026-10-20**` → `**ABSENT**` (word kept, date stripped).

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
STALE 0
UNVERDICTED 2
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
  DETAIL UNVERDICTED SF05 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

**The item's expected `UNVERDICTED 1` naming SF05 is a post-landing expectation.** At the frozen
tip SF04 (`PROVINCE.md:15`, `**ABSENT**, reconfirmed round 14`) is still undated and already
supplies the baseline's single `UNVERDICTED`. Two undated rows ⇒ `UNVERDICTED 2`. The control is
still a valid negative (the leg fires), but a receipt that promised `1` and delivered `2` would
read as an instrument failure unless the claims say which shape they mean.

## Section B — the item's expected line, reproduced in the after-shape

SF04 dated `**ABSENT 2026-10-28**`, SF05 stripped, **and** the SF04 manifest anchor shortened to its
stable prefix (see attack 2 for why the anchor edit is mandatory):

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF05 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

`UNVERDICTED 1` naming SF05, exit 1 — the item's expected line, reached only with two edits the
item does not name.

## Attack 1 (blocking for the landing) — the SF04 anchor embeds the marker the landing must date

The frozen manifest's SF04 anchor is, literally:

```
"anchor": "`~/Projects/bounties/ledger/telemetry.jsonl` \u2014 **ABSENT**"
```

Dating the row in place (`**ABSENT**` → `**ABSENT 2026-10-28**`) destroys that anchor:

```
ANCHORS total=19 dup=0 missing=1
ROWS section="## Surfaces" rows=9 entries=9 uncovered=1
UNVERDICTED 1
  DETAIL ANCHOR-MISSING SF04 anchor not found: `~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT**
  DETAIL UNCOVERED ## Surfaces row line 15 has no manifest entry
PREDICATE R51-C1 fail
```

The two natural landing edits therefore both fail:

| landing edit | anchor | `UNVERDICTED` |
|---|---|---|
| `**ABSENT 2026-10-28**` (date inside the bold) | MISSING 1 + UNCOVERED 1 | 0 |
| `**ABSENT** 2026-10-28` (date after the bold, anchor intact) | ok | 1 (SF04) — measured, below |
| `**ABSENT 2026-10-28**` **+ anchor shortened** | ok | 0 → the only passing shape |

The second row is worth stating because it is the *minimal* edit that preserves the frozen
manifest, and it fails:

```
== real tree, SF04 marker written as '**ABSENT** 2026-10-28' (date present, wrong shape; frozen anchor intact)
ANCHORS total=19 dup=0 missing=0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
PREDICATE R51-C1 fail
EXIT=1
```

So the frozen instrument+manifest pair, exactly as frozen, makes C1's after-target
(`UNVERDICTED 0` + coverage 19/19) unreachable without a `plans/round51-surfaces.json` edit, and
the claims' after-target does not name one. This is a **landing constraint, not a counter defect** —
`ANCHOR-MISSING` is doing its job — but it is a hidden dependency between two files the claims
describe as independent of the row edit.

**Corroboration, not novelty:** `C1MutRows.md` §D0 records the same anchor break, and its §D0b
reaches pass by *appending* `" — **ABSENT 2026-10-28** (round 51 re-probe: still absent)"` after the
row's closing pipe, keeping the undated `**ABSENT**` in the cell. That works because `ABSENT_RE`
searches the whole line, but it leaves the row with two markers — one undated in the cell, one dated
outside it — which is a prose regression a freshness claim should not carry. My delta on this point
is the third row of the table: the anchor fix, which leaves exactly one marker per row.

## Attack 2 — the date leg is a presence-and-shape check, not a freshness check

`plans/round51_surfaces.py:40`:

```python
ABSENT_RE = re.compile(r"ABSENT\s+(\d{4}-\d{2}-\d{2})")
```

and the leg (`check()`):

```python
if e["state"] == "absent":
    line = text[anchor_line[e["id"]]] if e["id"] in anchor_line else ""
    if not ABSENT_RE.search(line):
        problems["UNVERDICTED"].append("%s row has no ABSENT <ISO date> marker" % e["id"])
```

The captured group is never read. Nothing compares it to today, to the round start, or to the
manifest. Consequences, all measured:

1. **A seven-year-stale date passes.** Real tree, SF04 = `**ABSENT 2019-01-01**`, SF05 dated:
   `UNVERDICTED 0`, exit 1 only from the unrelated `DRIFT 3` + `NUMBER-DRIFT 1`.
2. **A future date passes.** Fixture `fx-stale-future` (`ABSENT 9999-12-31`): `UNVERDICTED 0`,
   `PREDICATE R51-C1 pass`, exit 0.
3. **A stale date cannot stop the claim.** Fixture `fx-stale-2019`, every other leg consistent:

   ```
   -- fx-dated-today
   UNVERDICTED 0 / PREDICATE R51-C1 pass / EXIT=0
   -- fx-stale-2019
   UNVERDICTED 0 / PREDICATE R51-C1 pass / EXIT=0
   -- fx-stale-future
   UNVERDICTED 0 / PREDICATE R51-C1 pass / EXIT=0
   -- fx-undated
   UNVERDICTED 1 / DETAIL UNVERDICTED SF02 row has no ABSENT <ISO date> marker
   PREDICATE R51-C1 fail / EXIT=1
   ```

   The landing could date SF04 `ABSENT 2019-01-01` and still print `pass`.
4. **The leg is shape-sensitive, not date-sensitive.** `**ABSENT** 2026-10-28` fails (measured
   above); `ABSENT — 2026-10-28`, `ABSENT (2026-10-28)` and `ABSENT** 2026-10-28` also fail by
   construction — `\s+` must be followed immediately by the digits. Only `ABSENT <ISO date>` in
   one run passes, which is precisely why the frozen anchor and the frozen regex are in tension.

**What the leg actually buys.** It forbids an absence from being *asserted without a date at all*.
That is a documentary requirement (a reader can see how old the verdict is), and it is the round-25
QUALITY-R4 convention this lane already applies to five rows. It is not evidence that the surface is
still absent today — that is `STALE` (probe vs recorded state) and `DRIFT` (recorded state vs row
prose), and both of those *are* machine checks against the host. The freshness move therefore rests
on `STALE`/`DRIFT`/`NUMBER-DRIFT`; `UNVERDICTED` must not be cited as a re-verification check.

**What a stricter rule would cost** (if `UNVERDICTED` were made an age check):

- **A clock in the predicate.** Today `check()` is a pure function of (tree, host state), so a
  receipt's `REV` plus its lines are replayable. A max-age rule makes "REV X passes" true only
  inside a window; the before/after receipts carry `REV` but no measurement date, so they would
  silently expire. The instrument would have to print the reference date in every receipt and the
  claims would have to name the window.
- **An unruled threshold.** `2026-10-20` markers on SF05/SF06 are 8 days old today. A
  "this-round" rule rejects two rows nobody disputes; a 30-day rule accepts `ABSENT 2026-09-29` on
  SF04 — i.e. the knob, not the check, decides the verdict. Choosing that knob now would be a
  parameter introduced after data, which this round's stage discipline forbids.
- **A manifest field.** The date lives in `PROVINCE.md` prose and is parsed by regex. Comparing it
  to a clock needs `confirmed_at` per absent entry (6 of 19 today) plus a rule
  `row date == confirmed_at AND confirmed_at >= now - N` — a manifest schema change and therefore
  a new instrument version, not a freeze-compatible edit.
- **Per-round row churn.** All six absent rows would have to be re-dated every round (6
  `PROVINCE.md` edits + 6 anchor checks, and SF04's anchor breaks unless shortened), replacing one
  honest "absent since <date>" with a treadmill of re-confirmation dates.
- **False verdicts on state the lane cannot change.** `~/.bailian` and `~/Projects/bounties` have
  been absent since rounds 25 and 11; an age rule would fail the predicate every round for host
  state this lane has no authority over, and "re-confirmed" would be a date with no re-probe behind
  it unless the `state` leg's probe runs (it already does).

Marginal gain of a stricter rule: it stops a stale date from *looking* current. That is real for a
reader, but it is a prose property; the evidential work is already done by `STALE`/`DRIFT`.

## Smallest safe correction

- **F1 (landing, blocking for C1's after-target).** Shorten the SF04 anchor in
  `plans/round51-surfaces.json:57` to the stable prefix
  `` "`~/Projects/bounties/ledger/telemetry.jsonl` — " `` (or the path cell alone; both are unique
  inside `## Surfaces`) **in the same landing change** that dates the row. Without it the after
  measurement prints `ANCHOR-MISSING 1` + `UNCOVERED 1`. Verified: with the shortened anchor the
  row stays covered through the dating edit (section B, `ANCHOR-DUP 0 / ANCHOR-MISSING 0 /
  UNCOVERED 0`). Prefer this over the out-of-cell append route (`C1MutRows` §D0b): one marker per
  row.
- **F2 (claims text, documentation).** §C1 control 4's expectation `UNVERDICTED 1` is the
  after-shape. At the frozen tip the same one-edit recipe prints `UNVERDICTED 2` (SF04+SF05). The
  receipt records both (sections A and B); the claims line should say so, or the control will be
  re-run by a later verifier and read as a regression.
- **F3 (semantics, documentation).** Record that `UNVERDICTED` is presence-and-shape, not age:
  the landing must not present `UNVERDICTED 0` as "every absent row was re-verified this round",
  and must not claim a stale date cannot pass. (Independent of `C1CritDeclareAllAbsent` §F4, which
  reaches the same reading from the marker inventory; my delta is the measured counterexample and
  the full-pass fixture.)
- **F4 (defer, not this round).** If the operator wants freshness 9 to mean "re-confirmed this
  round", that is a manifest `confirmed_at` field plus a max-age rule — a new instrument version
  declared before data (round 52), not a landing edit.

## Out-of-item observation (not investigated; for the L1)

While verifying that my writes were the only lane changes, `git status --porcelain` in the lane
showed two modifications that are **not mine** and are outside this item:

```
 M plans/round51_routing.py          (13 insertions, 5 deletions; mtime 2026-10-28 15:33:21 -0300)
?? corpus/evidence/round51/
```

`plans/round51_routing.py` is C2's frozen stage-1 instrument. With that edit uncommitted, the frozen
C2 command `python3 plans/round51_routing.py --lane . --run-checks` executes working-tree code, not
the freeze artifact, so `claims/c2-before.txt` no longer describes what the command now runs. I did
not read, diff or modify that file, and I ran no C2 measurement — flagging only because a
working-tree edit to a frozen counter during the wave is exactly the class the freeze exists to
prevent (and it may equally be the L1's own integration work; the L1 is the owner and can judge).

## Limits

- Measured at `4090c3d`, not at the freeze hash itself. `PROVINCE.md`, the manifest and the counter
  are byte-identical across the two by `git diff --stat e07f131..HEAD` (only `.ufo/waves/round-51/`
  spec files differ); I did not `cmp` them against the freeze blobs.
- Section B is a **simulated** after-shape, not the landed tree (it does not exist yet). The
  landing's own measurement in a clean clone is still required by the claims.
- The counter prints `REV` but **no dirty-tree marker** (the round-50 counter printed `TREE
  dirty=1`). A control receipt therefore cannot show by itself that it was measured on an edited
  tree; mine records each edit in its header. Landing receipts should be taken from a clean clone.
- Probe state (`:34113`, `~/.bailian`, `~/Projects/bounties`, `:8791`) is point-in-time at
  2026-10-28 and was not re-probed by this seat beyond what the counter does.
- Fixture runs use the instrument's own `--lane/--manifest/--province` overrides and test the date
  leg only; they are not evidence about the lane's real surfaces.
- I ran only this item: controls 1/2/3/5, the C2 counter and C2 controls were not run. No sibling
  report was used as evidence except where cited by name.
- Read-only against the lane: I wrote only the item-named receipt
  `.ufo/waves/round-51/claims/control-c1-undated.txt` and this report. No commit, push, or mutating
  git/jj command anywhere; every fixture write stayed inside the scratch clones whose
  `rev-parse --show-toplevel` I asserted first.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C1CritUndated` (2.3G, four reflink clones) was removed
  after this report and the receipt were written; the directory no longer exists
  (`ls` → "No such file or directory"), so no scratch tree is left on disk. `/fast` free space seen
  at start and after cleanup: `548–554G free, 32% used`.
- No tool installed or upgraded; no pacman transaction attempted; no model endpoint or route was
  used.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

VERDICT: CONTROL 4 FAILS AS REQUIRED (exit 1; `UNVERDICTED` names the stripped row) — but the item's `UNVERDICTED 1` naming SF05 is only the after-shape (`UNVERDICTED 2`, SF04+SF05, at the frozen tip), and the `UNVERDICTED` date leg is a presence-and-shape check, not a freshness check: `ABSENT 2019-01-01` and `ABSENT 9999-12-31` both pass, and a full-pass fixture with a 2019 date reaches `PREDICATE R51-C1 pass`, exit 0. Blocking for the landing: the frozen SF04 anchor embeds `**ABSENT**`, so dating the row without shortening `plans/round51-surfaces.json:57` yields `ANCHOR-MISSING 1` + `UNCOVERED 1`; with the anchor shortened, coverage holds and the after-shape is reachable.
