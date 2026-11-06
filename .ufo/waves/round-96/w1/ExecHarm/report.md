# ExecHarm — harm check of round-96 changes on other lane gates

Axes: (1) no PASS→FAIL flip on unrelated gates (grader, R68-A3/C1, R91-F1,
anchor-line) between BASE `45740a61` and T `09717e49`; (2) sources census
validates at T; (3) standing freeze-integrity gates (R94 v2 and R95-C2 counter,
run the way rounds 94/95 ran them for their own claims) — do the seven
repaired counters (rounds 87, 90–95 C1 replays) now read as broken freezes,
and is that a harm or an expected post-closure maintenance touch?

## 1. Unrelated gates — BASE vs T, no flip

| gate (cwd=clone root) | BASE receipt | T receipt | verdict |
|---|---|---|---|
| `python3 grader.py` | `VERDICT: PASS — stored evidence fully re-derives offline` rc=0 | identical rc=0 | PASS→PASS |
| `python3 plans/anchor_line_check.py --lane .` | `ANCHORLINE rows=301 cited=111 captured=98 uncaptured=13 defective=10 repaired=10 live=0 cells=0` rc=0 | `rows=308 cited=117 captured=104 uncaptured=13 defective=10 repaired=10 live=0 cells=0` rc=0 | PASS→PASS (rows/cited/captured grow by exactly the 7 new S310–S316 rows; defective/repaired/live/cells unchanged) |
| `python3 plans/round68_c1_pypi_finish.py --lane . --work <scratch>` | `PREDICATE R68-C1 pass` rc=0 | `PREDICATE R68-C1 pass` rc=0 | PASS→PASS (only stderr_sha256 values for K1/K3 vary run-to-run; verdict stable) |
| `python3 plans/round91_f1_counter.py --lane . --work <scratch>` | `PREDICATE R91-F1 pass` rc=0, `WRONG-LINE-CAUGHT True` | identical rc=0 | PASS→PASS |

Round-95 baseline (`lane-gates-end.txt`) ran the same gates the same way
(round-91 needed the `--work` the round-95 receipt's argparse error showed
missing; fixed here). No PASS→FAIL flip on — or harm to — any other lane
gate. Raw receipts: `receipts/grader-{base,t}.txt`, `anchor-{base,t}.txt`,
`r68-{base,t}.txt`, `r91-{base,t}.txt`.

## 2. Sources census at T

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
→ `rc=0`, `kengaku ok …/corpus/SOURCES.md`, 30 `W04 duplicate url … across
scopes` warnings only (pre-existing cross-scope duplicates; no errors).
Receipt: `receipts/census-t.txt`.

## 3. Standing freeze-integrity gates after the seven repairs

### 3a. Gate v2 directly (`round94_freeze_integrity.py`)

Rounds 87 and 90–92 have no ```` ```frozen-instruments ```` block in their
claims files (the table format lands in round 93), so gate v2 correctly
returns `DEFECT SETUP frozen-instruments table absent or empty /
PREDICATE freeze-integrity could-not-evaluate` rc=2 at their freeze revs —
it cannot judge them, it does not report them broken. Receipts
`freeze-r{87,90,91,92}-t.txt`.

For the rounds that do carry the table (93, 94, 95), run with each round's
own freeze rev and claims file, `--rev T`:

- r93 (freeze `d8d0a4b8`): `FREEZE-INTEGRITY instruments=9 intact=8 broken=1`,
  `PREDICATE freeze-integrity fail` — the one broken instrument is
  `plans/round93_c1_replay.py table=89153db6e525 freeze=89153db6e525
  rev=78edd3a6abb6 touched=1 verdict=broken:rev-bytes-differ+touched-after-freeze=1`.
- r94 (freeze `844c504e`): instruments=11 intact=10 broken=1, fail —
  `plans/round94_c1_replay.py … rev=44e38899bbbb touched=1 …broken…`.
- r95 (freeze `d9cd18a7`): instruments=11 intact=10 broken=1, fail —
  `plans/round95_c1_replay.py … rev=110d7fd72608 touched=1 …broken…`.

At BASE the same three runs are intact= all, `PREDICATE … pass` rc=0
(`freeze-r{93,94,95}-base.txt`). So the gate flips PASS→FAIL at T, but
solely on the instruments round 96 itself repaired. Every other frozen
instrument in those tables stays intact.

### 3b. Round-95 C2 counters through their public CLI (`round95_c2_counter.py`)

Run as rounds 95 ran it (`--lane . --rev <rev> --work <scratch>`, default
tool file `plans/round94_freeze_integrity.py`):

- BASE `45740a61`: `W4 pass freeze=d9cd18a7 rc=0 summary=(11,11,0)`,
  `W4 INSTRUMENT plans/round95_c1_replay.py … rev=c7e13dc9146e … intact`.
- T `09717e49`: `W4 fail freeze=d9cd18a7 rc=1 summary=(11,10,1)`,
  `W4 INSTRUMENT plans/round95_c1_replay.py … rev=110d7fd72608 touched=1
  verdict=broken:rev-bytes-differ+touched-after-freeze=1`,
  `TARGET legs_passed=4 of 5`, `PREDICATE R95-C2 fail` rc=1.

(The W1 r92 leg already fails at BASE — `W1a r92 rc=1 (4,1,3)` — that is the
round-92 freeze's pre-existing state, unchanged by round 96. The T-run is
otherwise identical: W2 `fixtures=20 ok=20`, W3 `probes=3`, W5
`mutants=10 killed=10`.)

Receipts: `receipts/r95c2-base.txt`, `receipts/r95c2-t.txt`.

## 4. Harm or expected maintenance touch?

The freeze-integrity gate's contract (its own docstring): a tabled
instrument is `intact` only if its bytes at the freeze hash to the table
*and* `git rev-list --full-history freeze..rev` never touches the path.
The seven repaired counters are frozen instruments of rounds 87 and 90–95,
and the repair is by design a byte-replace in round 96's commit C. The
gate therefore reports them broken — a true positive under its own
definition, not a false alarm.

Is it a harm? Under the rules in force at those freezes, yes-if-unannounced:
the claims files say "a frozen element that looks wrong is reported, not
repaired" and "editing … after commit A/B voids the claim". Round 96 repairs
them after closure and re-pins nothing, so a *standing* freeze-integrity
check run at T reports r93/r94/r95 freezes broken — rounds 87/90–92 cannot
be judged by gate v2 at all (no table). This is the correct reading for the
grader at T: the freezes are broken on the ledger.

Whether that is a *harm* to the lane is a judgement for L1/round 97, not
this seat: R96-C2's claim is precisely that the seven counters were red
while SCORECARD recorded met (six self-assessment mismatches at BASE), and
its repair keys L7 to each round's BASE executed SET. The freeze-integrity
breakage is the disclosed cost of that maintenance touch and is exactly what
`round96_standing_battery.py` says is intentional. What the table does show
plainly: there is currently no standing gate that reads the repaired
counters as "intact" — any freeze-integrity consumer at T gets 3× `fail`
(r93/r94/r95) plus 4× `could-not-evaluate`. Round 96 does not add such a
gate; nothing in the round-96 frozen-instruments table covers the repairs.
Route to round 97: either re-freeze the repaired counters as new baseline
instruments, or record the r93–r95 breaks as an adjudicated erratum in the
gate's ERRATA layer, else every future standing-check consumer flips red.

One non-blocker note for the record: at T the anchor line gains the S310–S316
rows (`rows 301→308, captured 98→104`) with defective/repaired unchanged —
the S315/S316 rejected rows are not flagged by the anchor gate. That is the
census's call (W04 warnings only), not the anchor check's job.

## 5. Tool installs

None. No tools installed or upgraded (scratches only; `uv` venvs not needed
for these gates).

## Exact commands

```sh
S=/fast/scratch/hyaku/kengaku-r96/ExecHarm
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane-base" && git -C "$S/lane-base" checkout -q --detach 45740a616028015b5dfcf9900753e3bb5e6fe689
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane-t"   && git -C "$S/lane-t"    checkout -q --detach 09717e49ff46fad5b255619d671aaaae52dfc180
git -C "$S/lane-base" rev-parse --show-toplevel   # /fast/scratch/hyaku/kengaku-r96/ExecHarm/lane-base
git -C "$S/lane-t"    rev-parse --show-toplevel   # /fast/scratch/hyaku/kengaku-r96/ExecHarm/lane-t
cd "$S/lane-base" && python3 grader.py                                          # receipts/grader-base.txt
cd "$S/lane-t"    && python3 grader.py                                          # receipts/grader-t.txt
cd "$S/lane-base" && python3 plans/anchor_line_check.py --lane .                # receipts/anchor-base.txt
cd "$S/lane-t"    && python3 plans/anchor_line_check.py --lane .                # receipts/anchor-t.txt
cd "$S/lane-base" && python3 plans/round68_c1_pypi_finish.py --lane . --work "$S/receipts/w-base68"
cd "$S/lane-t"    && python3 plans/round68_c1_pypi_finish.py --lane . --work "$S/receipts/w-t68"
cd "$S/lane-base" && python3 plans/round91_f1_counter.py --lane . --work "$S/receipts/w-base91"
cd "$S/lane-t"    && python3 plans/round91_f1_counter.py --lane . --work "$S/receipts/w-t91"
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
cd "$S/lane-t" && python3 plans/round94_freeze_integrity.py --lane . --freeze d8d0a4b8 --rev 09717e49ff46fad5b255619d671aaaae52dfc180 --claims plans/round-93-claims.md --work "$S/receipts/w-freeze/r93"
cd "$S/lane-t" && python3 plans/round94_freeze_integrity.py --lane . --freeze 844c504e --rev 09717e49ff46fad5b255619d671aaaae52dfc180 --claims plans/round-94-claims.md --work "$S/receipts/w-freeze/r94"
cd "$S/lane-t" && python3 plans/round94_freeze_integrity.py --lane . --freeze d9cd18a7 --rev 09717e49ff46fad5b255619d671aaaae52dfc180 --claims plans/round-95-claims.md --work "$S/receipts/w-freeze/r95"
cd "$S/lane-base" && python3 plans/round95_c2_counter.py --lane . --rev 45740a616028015b5dfcf9900753e3bb5e6fe689 --work "$S/receipts/w-base95b"
cd "$S/lane-t"    && python3 plans/round95_c2_counter.py --lane . --rev 09717e49ff46fad5b255619d671aaaae52dfc180 --work "$S/receipts/w-t95c2"
```

FINDING freeze-integrity major The seven repaired counters read as broken freezes under gate v2 at T (r93/r94/r95 fail, W4 r95 fail); r87/r90-92 unjudgeable (no table) — expected maintenance cost, route to round 97
FINDING other-gates info No PASS->FAIL flip on grader.py, anchor_line, R68-C1, R91-F1 between BASE and T; census rc=0 at T
