# M3ChessProbeMutants — seat report

**Seat:** `M3ChessProbeMutants` (mutation-tester) · kengaku round 55, wave 1 (v2, build+attack) · 2026-10-30
**Lane:** `kengaku-shokunin` @ `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`
**Target:** `plans/round55_c3_chess_probe.py` (mutation; bounded-wait; scratch copies only)
**Claim under attack:** R55-C3 (coverage 7→8 attempt, L0-capped) — 13th TB2 grader
`chess-best-move` executed offline by `plans/round55_c3_chess_probe.py`.

Frozen claims `plans/round-55-claims.md` were read first; no predicate, counter, kill rule or
target was changed by this seat.

## Verdict

**The probe is sound on the three mandated mutants, with one coverage finding.**

| mutant | expectation | observed | verdict |
|---|---|---|---|
| M1 verdict mapping inverted (P↔F) | receipt must flip to `mismatches>0` / `PREDICATE fail` | `mismatches=12`, `PREDICATE R55-C3 fail`, exit 1 | **KILLED** (detected) |
| M2 mismatch counter skipped | summary must change, or case lines expose it | byte-identical to baseline on the frozen table; with a mispredicted case the counter flips `mismatches=1→0` and `fail→pass` | **SURVIVES on the frozen table** — leg is real but unexercised (finding below) |
| M3 null mutant: case order reversed | output equivalent (order-insensitive summary) | summary + predicate + exit identical; sorted case-line sets identical | **NULL CONFIRMED** (equivalent) |

Plus four auxiliary probes (broken bwrap path, broken sha256 pin, zero timeout, duplicate-token
case body) — all fail closed with distinguishable SETUP output, and the duplicate-token probe
confirms the grader's full-multiset semantics are genuinely exercised.

**Baseline is green and reproducible:** pristine copy → exit 0, `cases=12 observed_pass=5
observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass`; two runs byte-identical; and the pristine
receipt is byte-identical to the lane's own `corpus/evidence/round55/chess-best-move-probe.txt`
(sha256 `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca`).

## Commands run (all with exit codes)

```
mkdir -p /fast/scratch/hyaku/kengaku-r55/M3ChessProbeMutants            # scratch root, created
cp <lane>/plans/round55_c3_chess_probe.py  <scratch>/pristine/…         # copy, not move
sha256sum <lane>/plans/round55_c3_chess_probe.py                        # 7bd2863c… before
git -C <lane> clone --shared --no-checkout <lane> <scratch>/lane-clone  # (clone attempted; see dead ends)
sha256sum <lane>/corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py  # a540714e…f286 (== frozen pin)

python3 <scratch>/pristine/round55_c3_chess_probe.py --lane <lane> --work <scratch>/work-base \
        --receipt <scratch>/receipts/base.txt                            # exit 0
python3 <scratch>/pristine/… --selftest --work <scratch>/work-self-base  # exit 0, failures=0
/usr/bin/time python3 <scratch>/pristine/… --receipt …/base2.txt          # exit 0, WALL=0.40s MAXRSS=20512kB

python3 <scratch>/mut1/…  --lane <lane> --work …/work-mut1 --receipt …/mut1.txt   # exit 1
python3 <scratch>/mut2/…  --lane <lane> --work …/work-mut2 --receipt …/mut2.txt   # exit 0
python3 <scratch>/mut2b/… --lane <lane> --work …/work-mut2b --receipt …/mut2b.txt # exit 1 (control)
python3 <scratch>/mut2c/… --lane <lane> --work …/work-mut2c --receipt …/mut2c.txt # exit 0
python3 <scratch>/mut3/…  --lane <lane> --work …/work-mut3 --receipt …/mut3.txt   # exit 0
python3 <scratch>/mut4/…  --lane <lane> --work …/work-mut4 --receipt …/mut4.txt   # exit 2 (aux)
python3 <scratch>/mut5/…  --lane <lane> --work …/work-mut5 --receipt …/mut5.txt   # exit 2 (aux)
python3 <scratch>/mut6/…  --lane <lane> --work …/work-mut6 --receipt …/mut6.txt   # exit 2 (aux)
python3 <scratch>/mut7/…  --lane <lane> --work …/work-mut7 --receipt …/mut7.txt   # exit 1 (aux)
python3 <scratch>/{mut1,mut2,mut3}/… --selftest --work …/work-self-<m>         # exit 1 / 0 / 0

diff -u receipts/base.txt receipts/<m>.txt          # per-mutant diffs → receipts/diffs/
grep '^CASE' base.txt | sort  vs  mut3.txt | sort    # order-insensitive equality for M3
cmp  receipts/base.txt receipts/mut2.txt             # M2 byte-identity vs baseline
sha256sum lane/plans/round55_c3_chess_probe.py       # 7bd2863c… after — UNCHANGED
git -C <lane> status --porcelain -- plans/round55_c3_chess_probe.py   # "?? …" unchanged
```

Mutants were applied with the `edit` tool on the scratch copies (M4–M7 prepared by a one-shot
in-place rewrite of a single constant/line in their own scratch copy — no lane file touched).

## Files written

All under the lane repo, all in this seat's own namespace:

- `.ufo/waves/round-55/w1/M3ChessProbeMutants/mutants.md` — the mutation record with every
  observed diff, hash ledger and the independent upstream re-verification.
- `.ufo/waves/round-55/w1/M3ChessProbeMutants/report.md` — this file.
- `.ufo/waves/round-55/w1/M3ChessProbeMutants.md` — scoped findings (the `Report:` trailer path).
- `.ufo/waves/round-55/w1/M3ChessProbeMutants/receipts/` — 35 files: every receipt and stderr
  (`base`, `base2`, `mut1`…`mut7`, `selftest-base`), `diffs/` (10 unified diffs),
  `SHA256SUMS.txt`, `pristine-probe.py` + `pristine-probe.sha256`.

No other lane file was created or modified. `plans/round55_c3_chess_probe.py` is byte-identical
before and after (`7bd2863c…`) and remains untracked; no mutating git/jj command was run anywhere;
no fleet-root tracked file was written; no tool was installed.

## Defects found (reported, not fixed — not this seat's files)

1. **The mismatch leg is unexercised by the frozen case table (coverage finding).** All 12 frozen
   predictions are correct, so the committed `mismatches=0` receipt is *identical* whether the
   counter runs or is deleted (mut2 receipt sha256 == baseline sha256). The counter is genuinely
   load-bearing — with one deliberately mispredicted case, deleting it turns `mismatches=1 /
   PREDICATE fail / exit 1` into `mismatches=0 / PREDICATE pass / exit 0` — but that negative
   control exists only in this seat's scratch, not in the round's committed artefact. The round's
   kill rule (a) ("an observed≠predicted case is not counted as a mismatch") is therefore *not*
   exercised by the shipped battery: the counter is the only thing preventing a false
   `PREDICATE R55-C3 pass`, and the case lines alone do not expose its absence (M2c still prints
   `CASE single-move-only predicted=P observed=F rc=1` while the summary says `mismatches=0`).
   Closing this needs either a deliberately mispredicted case in the table or a negative-control
   case — amendment data for the frozen table, i.e. the L1's call, not mine.
2. **Receipt bytes are order-sensitive while the summary is order-insensitive.** Mutant M3 (case
   order reversed) leaves `cases=… observed_pass=… observed_fail=… mismatches=…` and the
   `PREDICATE` line identical, but reorders the `CASE …` lines, changing the receipt's sha256.
   Any check that pins the receipt by hash is brittle under a case-table reordering; a check that
   parses the summary line is not. The round's after-predicate quotes the summary form, so the
   claim is consistent with the probe — but the byte-hash form of the receipt should not be
   treated as order-stable.
3. **The pin does not resolve in the repos most readers will try.** `2fd12b88aafdd04a52c298e3940bcb189f9766d6`
   is a commit in `harbor-framework/terminal-bench-2`; in
   `laude-institute/terminal-bench` and `laude-institute/terminal-bench-datasets` it 404/422s.
   Anyone re-verifying the pin must use the harbor-framework repo (the lane's own
   `corpus/evidence/round53/pin-tree-2fd12b88.json` names it). Not a defect in the probe — an
   upstream-identity leg note for the round lesson.

## Independent upstream re-verification (read-only GETs)

- `harbor-framework/terminal-bench-2` @ the pin: tree HTTP 200, 1446 entries, `truncated:false`;
  `chess-best-move/tests/test_outputs.py` blob `6ec2300a…0a75` (971 B); raw bytes sha256
  `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` — **byte-identical to the
  lane capture and to the probe's frozen pin**.
- `laude-institute/terminal-bench@main` (`original-tasks/chess-best-move/tests/test_outputs.py`):
  same sha256 `a540714e…f286` — the file is unchanged between the pin and current main.
- The upstream grader's assertion is `assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"`,
  i.e. the probe's oracle derives only from the captured grader's own assertion (kill rule (b)
  checked by reading the upstream bytes, not the lane's paraphrase).
- A1 amendment verified: upstream `chess-best-move/tests/test.sh` at the pin =
  `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` = the lane's captured
  chess-best-move `test.sh` = `round52/graders/regex-log/tests/test.sh` = `round36/tb2-regex-log/test.sh`
  (S109's file). Dropping the third SOURCES row is correct — a new row would duplicate held ground.

## Dead ends

- `git clone --shared --no-checkout` of the lane produced a clone whose index had no entry for
  `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` (checkout of that path
  errored "did not match any file(s) known to git"). Abandoned: the probe only needs `--lane` to
  *read* the grader, and the pristine lane copy provides that. No clone was used for any measurement.
- `git -C <lane> ls-files --error-unmatch corpus/evidence/round55/chess-best-move-probe.txt` →
  "did not match any file(s) known to git". The round-55 receipt exists in the working tree but is
  **not yet tracked** (`?? corpus/evidence/round55/` in `git status`) — expected at this stage of
  the wave (the L1 commits it), noted for the record.
- Upstream pin hunting: `raw.githubusercontent.com` and `api.github.com` for
  `laude-institute/terminal-bench`, `terminal-bench/terminal-bench`, `-terminal-bench-datasets` and
  `laude-institute/harbor` all 404/422 for the pin SHA and for the guessed task paths
  (`tasks/chess-best-move/…`, `dataset/…`, `chess-best-move/…`). The path that resolves is
  `harbor-framework/terminal-bench-2` with the task at the repo root (`chess-best-move/tests/…`).
  Found by reading the lane's round-53 pin-tree record, not by guessing.

## Hygiene

Scratch root `/fast/scratch/hyaku/kengaku-r55/M3ChessProbeMutants/` was created, used for every
clone/copy/work dir (each probe run used its own `--work` subdir under it; the probe honours
`--work`/`--receipt` and never hardcodes `/tmp`), receipts were copied into
`.ufo/waves/round-55/w1/M3ChessProbeMutants/receipts/`, and the scratch dir was deleted on exit.
Lane restored/verified: `plans/round55_c3_chess_probe.py` sha256 `7bd2863c…` identical before and
after; `git status --porcelain -- plans/round55_c3_chess_probe.py` unchanged (`??`).
