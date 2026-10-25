# F35MutEntryQuotes — entry mutation probe (round 35, wave 2 falsify)

Seat: mutation-tester. Target: the LANDED entry `corpus/knowledge/tb2-protein-assembly-grader.md`
as committed at `dfee6fff631ebc5f623ba4506e5c7992a215401c`. Detector: the frozen C1 counter
`python3 plans/round35_c1_verify.py --lane .` (frozen predicate: `checks=6 defects=0`,
`PREDICATE C1 pass`, exit 0). Method: fixture clone, one mutant at a time, restore exact bytes
between runs, post-restore green re-run.

## Fixture

- `D=/tmp/k35f-f2YZ`; `git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"`;
  `git -C "$D/lane" sparse-checkout set --no-cone …`; `git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c`.
- `git -C "$D/lane" rev-parse --show-toplevel` → `/tmp/k35f-f2YZ/lane` (TOPLEVEL-OK); HEAD = `dfee6fff…`.
- Pinned entry sha256 `06cd91c1b5917df43a57b097b3708120e60b15116257113841f0f7391a858713`
  (= `git show dfee6fff…:corpus/knowledge/tb2-protein-assembly-grader.md`); receipt sha256
  `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8` (identical to live lane's copy).
- No commits made anywhere; all mutants were uncommitted worktree edits restored byte-exact from a
  pristine copy. Only the fixture and this seat's scratch dir were written.
- **Baseline (pristine):** `V1 ok / V2 ok / V3 ok / V4 ok / V5 ok / V6 ok / checks=6 defects=0 / PREDICATE C1 pass / exit=0`.

Calibration notes (baseline was initially red, then made green — no mutant judged on a red baseline):

1. With a minimal sparse checkout the counter printed `V6 DEFECT census exit 1`: the census
   (`scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md`) emits **E11 "used-by path
   missing on disk"** for registry rows whose used-by files are absent from the worktree. Widening the
   fixture to a full checkout of the same commit (`sparse-checkout set --no-cone '/*'`, re-checkout of
   `dfee6fff…`) made V6 green. The counter is fixture-sensitive via V6's on-disk used-by requirement —
   a calibration fact, not an entry defect.
2. The **live lane worktree** entry currently carries an uncommitted `## Errata (appended round 35,
   falsify wave, 2026-10-25)` section (`git -C <lane> status --porcelain` → ` M corpus/knowledge/tb2-protein-assembly-grader.md`;
   worktree sha256 `0e1739d4…` ≠ committed `06cd91c1…`). That is a sibling seat's in-progress edit;
   this probe attacked only the committed frozen bytes in the fixture and touched no live lane file.

## Mutants (all in the fixture copy; counter run after each; restore between)

Pristine entry sha256 before every mutant: `06cd91c1…`. Restoration after every mutant: `cp` of the
pristine copy, hash re-checked to `06cd91c1…` (printed in each run below). Detector expectation per
mutant derived from counter source: V3 byte-checks each quote inside the cited capture line span and
requires "falsif" in `## Negative space`; V5 requires the receipt summary line verbatim in the entry.

| # | Mutant (entry line) | Expected detector | Actual counter output (defect line) | Verdict |
|---|---|---|---|---|
| M1a | quote 1, one char: `“…Path("/app/gblock.txt")”` → `…txT` (L110) | V3 quote-no-longer-verbatim | `V3 DEFECT quote not on test_outputs.py:13-13: gblock_path = Path("/app/gblock.txT")` · `checks=6 defects=1` · `PREDICATE C1 fail` · exit 1 · restored `06cd91c1…` | **killed** |
| M1b | quote 2, one char: `rstrip()` → `rstriq()` (L111) | V3 quote-no-longer-verbatim | `V3 DEFECT quote not on test_outputs.py:16-16: lines = [line.rstriq() for line in f]` · `checks=6 defects=1` · exit 1 · restored `06cd91c1…` | **killed** |
| M1c | quote 3, one char: `echo 1 >` → `echo 2 >` (L126) | V3 quote-no-longer-verbatim | `V3 DEFECT quote not on test.sh:27-27: echo 2 > /logs/verifier/reward.txt` · `checks=6 defects=1` · exit 1 · restored `06cd91c1…` | **killed** |
| M2 | location shifted one line: `` `test_outputs.py:13` `` → `` `:14` ``, quote untouched (L110) | V3 span-check fails | `V3 DEFECT quote not on test_outputs.py:14-14: gblock_path = Path("/app/gblock.txt")` · `checks=6 defects=1` · exit 1 · restored `06cd91c1…` | **killed** |
| M3 | drop Negative-space falsifier paragraph `**Falsifier:** this entry is falsified if …` (L98–101) | V3 "no falsifier" | `V3 DEFECT negative space absent or has no falsifier` · `checks=6 defects=1` · exit 1 · restored `06cd91c1…` | **killed** |
| M4 | remove receipt summary line `` `cases=18 observed_pass=5 observed_fail=13 mismatches=0` `` (L20) | V5 entry-must-carry-summary | `V5 DEFECT entry does not carry the receipt summary line verbatim` · `checks=6 defects=1` · exit 1 · restored `06cd91c1…` | **killed** |

M2 pre-check: capture `tb2-eval/test_outputs.py` line 13 holds the quote, line 14
(`assert gblock_path.exists(), …`) does not — the kill shows V3 really reads the cited span, not the
whole file. M4 note: V5's fresh-probe-vs-receipt byte compare still passed under M4 (receipt untouched);
the defect fired on the entry-carry check — the two V5 legs are independently exercised.

## Restoration evidence

- After each mutant: `sha256sum` of the restored entry = `06cd91c1b5917df43a57b097b3708120e60b15116257113841f0f7391a858713` (printed per run above).
- Post-restore final run on pristine bytes: `V1…V6 ok / checks=6 defects=0 / PREDICATE C1 pass / exit=0`;
  receipt sha256 `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8` (unchanged);
  `git status --porcelain` in the fixture → 0 lines (clean).
- Teardown: `rm -rf /tmp/k35f-f2YZ` (own exact path only; no `/tmp/k35f-*` glob) — path now absent.
  Live lane, its jj/Git state, and all sibling files untouched.

## Result

6 mutants (3 single-character quote corruptions, 1 one-line location shift, 1 dropped Negative-space
falsifier, 1 removed receipt summary line) — every one flipped the frozen predicate to
`PREDICATE C1 fail` with exit 1. No surviving mutant; no coverage gap found in the
quote/location/falsifier/receipt-summary surface of the C1 counter.

VERDICT: entry-mutants-killed-6/6
