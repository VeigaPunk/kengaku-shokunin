# MutTesterGate — mutation test of the v2 freeze-integrity gate through the frozen C2 counter (round 94, wave 1)

Seat: MutTesterGate (leaf, no subagents). Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin @ master.
Detector rev T = 90c7677f0ba95d0930d93bda6a14aa50605ebe2e; freeze F = 844c504e5147ce767a146af98e4d9b2cacb4258d.
Date: 2026-11-05. Tool installs: **none** (host python3 + git only; no pacman, no uv, no binaries).

## Method

- One `git clone --shared` of the lane into `$S/lane` ($S=/fast/scratch/hyaku/kengaku-r94/MutTesterGate),
  `checkout -q --detach 90c7677f…`. All counter runs executed from that clone; lane untouched
  (no git/jj mutations; lane file bytes verified unchanged after all runs, see Restoration).
- Pristine gate `plans/round94_freeze_integrity.py` @ T verified against the frozen table:
  sha256 8574b4d5dca7f3817f1beb42c024c80791a0b958b04da94361e9e2a6cc4964de (= claims row 4). Counter
  `plans/round94_c2_counter.py` = 17d2a7d52fbd703db1c4df661168f22a36481f289962ea66d5e98a0466190b98 (= row 5).
- 20 byte-level mutants generated from the pristine bytes, each a single-site replacement
  (M19 two sites, M20 three sites — one logical defect each), **none coinciding with the counter's
  own K1–K7** (K1 t→HEAD, K2 f→rev~1, K3 claims blob at t, K4 CNE→pass/0, K5 drop --full-history,
  K6 blocks>99, K7 dups→False). Anchors asserted count==1 before replacement; every mutant
  py_compiles. Generator: receipt `mutants/manifest.json` (anchor + replacement + sha256 per mutant).
- Detector (identical for pristine/mutated bytes), from `$S/lane`:

```
python3 plans/round94_c2_counter.py --lane "$S/lane" --rev 90c7677f0ba95d0930d93bda6a14aa50605ebe2e \
  --work "$S/w-<mut>" --tool-file <mutant.py>
```

- Verdict rule: **killed** iff exit rc ≠ 0 or `TARGET legs_passed < 5 of 5`; **survived** iff
  `TARGET legs_passed=5 of 5` + `PREDICATE R94-C2 pass` + rc 0. Killing legs = the W legs printed `fail`.
- 21 detector runs (null + 20 mutants), ~37–45 s wall each, 4-way parallel, total ≈ 6 min.
  Raw stdout of every run (with `EXIT rc=` appended) is in `receipts/<mutant>.txt`.

## Baseline (pristine bytes — detector sanity)

`N00-null-copy.py` (sha256 = pristine): `W1 pass`, `W2 pass fixtures=12 ok=12`,
`W3 pass` (echo `SELFTEST cases=15 ok=15` ×2), `W4 pass freeze=844c504e5147 rc=0 summary=(11, 11, 0)`,
`W5 pass mutants=7 killed=7`, `TARGET legs_passed=5 of 5`, `PREDICATE R94-C2 pass`, rc 0.
Detector is sound; all mutant verdicts below are informative.

## Results — 11 killed, 9 survived (of 20)

| mutant | site (one line) | sha256-12 | verdict | failed legs | killing evidence |
|---|---|---|---|---|---|
| M01 paths-dup-guard-dropped | evaluate: `if len({p for _,p in table}) != len(table):` → `if False and …` | 64e61594fd2d | **SURVIVED** | – | no leg passes duplicate `--paths` (F1) |
| M02 unterminated-block-accepted | parse_table: `if inside:` (not terminated) → `if False and inside:` | a0b48be368db | **SURVIVED** | – | no battery case / fixture has an unterminated block (F2) |
| M03 revlist-merges-only | evaluate: rev-list gets extra `--merges` | d9d458f953ee | killed | W1 W2 W3 W4 W5 | battery B03 RED (wants `touched-after-freeze=2`, got intact); `W2 w2-edit-revert RED rc=1 summary=(1,1,0)`; W5 null RED |
| M04 rev-vs-freeze-bytes | evaluate: `elif sha(at_t) != want:` → `!= sha(at_f)` | 01a3a0405fbb | **SURVIVED** | – | semantically absorbed — see F5 |
| M05 summary-counts-swapped | main: `intact={len(broken)} broken={len(rows)-len(broken)}` | 8587424c9deb | killed | W1 W2 W4 W5 | `W2 w2-intact RED summary=(1,0,1) want=(1,1,0)`; W1a/W1b summary mismatch; W3 green |
| M06 battery-truncated-14 | battery: B15 `case(...)` call deleted → cases=14 | 9c609170d398 | killed | W3 | `W3 echo SELFTEST cases=14 ok=14` ≠ required `cases=15 ok=15`; all other legs green |
| M07 battery-nonfatal | main: `passed = not broken and bat_ok == len(bat)` → `passed = not broken` | 85eac59030f2 | **SURVIVED** | – | indistinguishable on a green battery; reds still surface via W3 echo unless the echo lies too (F4) |
| M08 inside-never-set | parse_table open branch: `inside = True` → `inside = False` | 8bf2549f5a44 | killed | W1 W2 W3 W4 W5 | every claims-mode run CNE; battery 9 cases RED (`ok=6`); `W2 w2-intact RED rc=2 summary=None` |
| M09 ancestry-check-dropped | evaluate: merge-base `--is-ancestor` rc check → `if False and …` | 4035e6ea2576 | killed | W1 W2 W3 W4 W5 | battery B07 RED (wants could-not-evaluate, got broken); `W2 w2-not-ancestor RED` (wants rc 2); W5 null RED |
| M10 revlist-rc-ignored | evaluate: `if log.returncode != 0:` → `if False and …` | 412267818da1 | **SURVIVED** | – | rev-list never fails with resolve()-validated revs in any leg (F6) |
| M11 freeze-bytes-check-weakened | evaluate: `if at_f is None or sha(at_f) != want:` → `if at_f is None:` | f22873a469ec | killed | W1 W2 W3 W4 W5 | battery B04/B15 RED (wants `freeze-bytes-differ-from-table`); `W2 w2-lying-table RED rc=0 summary=(1,1,0)` |
| M12 rev-bytes-check-dropped | evaluate: `elif sha(at_t) != want:` → `elif False:` | 074e130873e2 | killed | W1 W2 W3 W4 W5 | battery B02 RED (wants `rev-bytes-differ` in verdict) → gate rc flips to 1 globally → `W1b RED rc=1`, `W2 w2-intact RED rc=1` |
| M13 touched-threshold-2 | evaluate: `if touched:` → `if touched > 1:` | f4ef335743df | killed | W1 W2 W3 W4 W5 | battery B02 RED (wants `touched-after-freeze=1`); `W2 w2-edited RED rc=0 summary=(1,1,0)` |
| M14 exit-polarity-flipped | main: `return 0 if passed else 1` → `return 1 if passed else 0` | 1c3c68b237ba | killed | W1 W2 W4 W5 | `W1b RED rc=1 summary=(9,9,0)`; `W2 w2-intact RED rc=1`, `w2-edited RED rc=0`; W4 rc 0→1 |
| M15 predicate-always-pass | main: gate prints `PREDICATE freeze-integrity pass` unconditionally | 40ae33052b89 | **SURVIVED** | – | counter never parses the gate's PREDICATE line (F3) |
| M16 blob-ignores-rc | blob(): `return proc.stdout if proc.returncode == 0 else None` → `return proc.stdout` | 4ab05d1cecfa | killed | W1 W2 W3 W4 W5 | battery B05 RED (deleted path gives b"", verdict `rev-bytes-differ` not `absent-at-rev`) → gate rc 1 → `W2 w2-intact RED rc=1` |
| M17 empty-table-accepted | parse_table: `if not rows:` raise → `if False and not rows:` | 0c1fe3460995 | killed | W1 W2 W3 W4 W5 | battery B08 RED (wants could-not-evaluate, got `[]`); cascade rc flips |
| M18 resolve-no-peel | resolve(): drops `^{commit}` peel | 7e1b5da2b6a1 | **SURVIVED** | – | every counter-passed rev is a raw commit sha; peeling unobservable (F7) |
| M19 battery-red-concealed | main: `passed = not broken` **and** `ok={bat_ok}` → `ok={len(bat)}` | 333263120991 | **SURVIVED** | – | green battery ⇒ identical observable; proves nothing alone (F4 preamble) |
| M20 battery-broken-and-concealed | battery B02 want→`lambda v: False` **and** `passed = not broken` **and** forged `ok={len(bat)}` | 23061c2fca72 | **SURVIVED** | – | battery genuinely red, counter blind — F4 |
| N00 null-copy | pristine bytes | 8574b4d5dca7 | BASELINE OK | – | `TARGET legs_passed=5 of 5`, rc 0 |

W5 note: for mutants whose site lives inside `evaluate`/`parse_table` (M03, M04, M08, M09, M10,
M11, M12, M13, M16, M17, M18) the counter's own W5 machinery re-derives K1–K7 from the mutated
bytes and the inherited null copy inherits the mutation too — so those kills are doubled (W5 null RED
plus the direct leg). Main-line mutants (M05, M14, M15, M07, M19, M20) leave W5 green: K1–K7 are
killed exactly as designed while the gate's own main-line forgery goes unpoliced.

## Survivors — equivalence arguments and findings

- **M04** — equivalence argument: given the gate's other checks, any table-vs-rev byte difference
  implies `touched-after-freeze ≥ 1` (freeze is a resolved ancestor and the count uses
  `--full-history`), so `broken` and the FREEZE-INTEGRITY summary are invariant; verdict strings
  differ only when a row has a lying table **and** an edited path simultaneously, which no W2
  fixture or battery case constructs (B04/B15/w2-lying-* keep probe bytes stable). → FINDING F5.
- **M18** — equivalence argument: every rev the counter passes (R92_FREEZE/TIP, R93_FREEZE/TIP,
  W2 fixture heads, W4 freeze/rev) is a raw commit id; `^{commit}` peeling is never exercised.
- **M10** — equivalence argument: rev-list is only invoked after both revs resolve and with the
  freeze an ancestor; no leg constructs a failing rev-list (no shallow/partial clone, no corrupt
  alternates), so the rc guard is unreachable in this harness. → info F6.
- **M07** — equivalence argument on green-battery inputs; but see F4: combined with a forged
  SELFTEST echo the concealment becomes total (M19/M20 receipts).
- **M01** — FINDING F1 (coverage gap).
- **M02** — FINDING F2 (coverage gap).
- **M15** — FINDING F3 (unpoliced output line).
- **M19+M20** — FINDING F4 (battery truth unpoliced; demonstrated concealment).

## Findings (scoped; none flips the frozen R94-C2 verdict at T)

- **F1 minor (calibration coverage)** — `M01-paths-dup-guard-dropped` survives 5/5: no counter leg
  or battery case passes duplicate `--paths`, so the round-93 W-6 defect (duplicate rows double
  counted) is only closed for claims mode (K7); a gate that silently accepts dup `--paths` in paths
  mode is admitted. Route to round 95: add a battery case / W2 fixture running `--paths probe.py probe.py`
  and expecting rc 2.
- **F2 minor (calibration coverage)** — `M02-unterminated-block-accepted` survives 5/5: the gate
  docstring promises could-not-evaluate for an unterminated frozen-instruments block, but neither
  the 15-case battery nor any counter fixture contains one. Route: add such a case.
- **F3 minor (calibration)** — `M15-predicate-always-pass` survives 5/5: the counter polices rc,
  the FREEZE-INTEGRITY summary and INSTRUMENT lines, but never the gate's own
  `PREDICATE freeze-integrity …` line; a gate that prints `pass` while exiting 1 on a broken lane
  is indistinguishable to the counter (humans and lane receipts do read that line).
- **F4 minor (calibration; the sharp one)** — `M20-battery-broken-and-concealed` survives 5/5
  (`TARGET legs_passed=5 of 5`, `PREDICATE R94-C2 pass`, rc 0) while its own stdout — captured at
  `receipts/direct/M20-direct-gate.txt` — shows `BATTERY B02 RED got=['broken:rev-bytes-differ+touched-after-freeze=1']`,
  `SELFTEST cases=15 ok=15` (forged), `PREDICATE freeze-integrity pass`, rc 0. The counter's only
  window into the in-process battery is the gate's own SELFTEST echo (W3 checks the line's format,
  not its truth) and W5's mutant set contains no battery-path attack, so a gate that breaks its own
  battery *and* controls its echo passes every leg. Does **not** flip R94-C2 at T (the real gate's
  battery is green and its echo honest; no W leg fails at T). Route to round 95: add a K8 battery-path
  mutant (e.g. B02-want-always-False + forged ok) to W5, and/or have the counter re-derive
  `ok=` from the echoed BATTERY lines.
- **F5 info (equivalence + coverage note)** — M04 absorbed; discriminating input (lying table +
  post-freeze edit) absent from fixtures; reason-string fidelity for that combo is unverified.
- **F6 info** — M10: rev-list rc handling unobservable in-harness.
- **F7 info** — M18: commit peeling unobservable (all revs raw commit ids).

No finding changes any tabled instrument; the frozen rule is respected — nothing in the lane was
repaired or edited. All routes above go to round 95.

## Restoration evidence

- Lane working-tree bytes before == after: `plans/round94_freeze_integrity.py` =
  8574b4d5dca7f3817f1beb42c024c80791a0b958b04da94361e9e2a6cc4964de;
  `plans/round94_c2_counter.py` = 17d2a7d52fbd703db1c4df661168f22a36481f289962ea66d5e98a0466190b98.
  No git/jj/index/jj-metadata mutation was performed in the lane at any point (all detector runs
  used the detached `--shared` clone at T; clone HEAD re-verified 90c7677f0ba95d0930d93bda6a14aa50605ebe2e).
- Mutant bytes are preserved in the wave dir (`mutants/*.py` + `mutants/manifest.json`), so nothing
  experiment-critical lives in scratch.
- Scratch `$S` (clone + 21 work dirs + generator/tabulator scripts) removed before yield.

## Files written by this seat

- `.ufo/waves/round-94/w1/MutTesterGate.md` — scoped findings (this seat's Report entry point)
- `.ufo/waves/round-94/w1/MutTesterGate/report.md` — this report
- `.ufo/waves/round-94/w1/MutTesterGate/mutants/` — N00 + M01–M20 gate mutants + manifest.json (sha256, anchors)
- `.ufo/waves/round-94/w1/MutTesterGate/receipts/` — raw counter stdout per run (with EXIT rc), `evidence-digest.txt`, `direct/M20-direct-gate.txt`
- `.ufo/waves/round-94/w1/MutTesterGate/tabulation.json` — machine-readable verdicts
