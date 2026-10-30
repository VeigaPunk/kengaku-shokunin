# C2MeasureExecB — independent C2 measurement

## Run

- Cloned lane: `/fast/scratch/hyaku/kengaku-r53/C2MeasureExecB/lane`; `git rev-parse --show-toplevel` printed exactly that path.
- Source HEAD: `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe`.
- Commands:
  1. `S=/fast/scratch/hyaku/kengaku-r53/C2MeasureExecB; mkdir -p "$S"; git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`
  2. `git -C "$S/lane" rev-parse --show-toplevel`
  3. `git -C "$S/lane" rev-parse HEAD`
  4. `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` (before heavy pass)
  5. `mkdir -p "$S/tmp"; cd "$S/lane" && nohup setsid env TMPDIR="$S/tmp" python3 plans/round53_c2_tipstate.py --lane . --source "$S/lane" --work "$S/work" --jobs 3 --timeout 900 > "$S/out.txt" 2>&1 < /dev/null &`
- Invocation was detached. Run wall time: 270.65 seconds (as reported by the wait on the detached process watcher). Load average before pass: `12.35 7.98 5.85`; after: `4.50 10.98 8.46` (`/proc/loadavg`). Earlier initial capture was `7.04 6.77 5.43`, before the specified before-pass capture.
- Full counter output and detailed disagreeing row output are retained at the absolute paths below. Counter exit code: **1** (`PREDICATE R53-C2 fail`; single row mismatch, with no timeout).

## Measured result

```text
ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok
ARGV entry=74 selftest=4 help=0 help_limit=7.8
SOURCE rev=b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe clean=yes lane_rev_equal=yes
  MISMATCH round53-c1 declared exit=0 observed exit=1 sec=0.8
RUN executed=78 timeout=0 mismatched=1 evidence_missing=0
TIPSTATE declared_green=66 declared_red=12 observed_green=65 observed_red=13
PREDICATE R53-C2 fail
```

Disagreeing row's complete output (`work/disagreed-round53-c1.txt`): exit=1, sec=0.8; pins all `ok` (183 captured-file blob matches; excluded blob ok), freeze clean and pinned, oracle 305 tests / 0 disagreements / control ok, confirmation 0 new confirmed, prior-art 0 rows, `PREDICATE R53-C1 fail`. Thus `round53-c1` declared exit 0 but observed 1. One verbatim fragment under 200 characters: `  MISMATCH round53-c1 declared exit=0 observed exit=1 sec=0.8`.

## Named red reasons checked against observed work

The full run found no mismatch among the 12 entries declared red; these remain exit 1 and evidence fragments matched. The ledger reasons still describe the observed red cause for each:

- `round51-surfaces`: yes — declared `NUMBER-DRIFT SF14 row claims 171, probe says SOURCES rows=186`.
- `state-assertion-check`: yes — declared `MISMATCH: P3c.box.4.pointer.1:12`.
- `round28-census`: yes — detailed output retains the embedded state-check `"MISMATCH": 1,` evidence.
- `round35-c1-coverage`: yes — `(want 42/42)`.
- `round38-c1-mutants`: yes — `MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0`.
- `mutant-direction-check`: yes — `DIR N21 D5 declared=silence observed=mirror MISLABELLED`.
- `round46-c3`: yes — declared V7/V8 defect; evidence `V8 DEFECT order_exit=1 result=not-PASS`.
- `round52-c1`: yes — `CAPTURES expected=184 present=183 mismatched=0`.
- `anchor-digest-check`: yes — `class=anchor-unbound detail=row-carries-no-capture-locator`.
- `gate-flip-check`: yes — `FLIPS total=3 unresolved=3`.
- `adoption-check`: yes — `census=fail` remains consistent with clone-external hardcoded fleet path failure.
- `round40-c1-mutants`: yes — `BATTERY fixtures=21 wrong=8 tampered=0 sidechannel=0`.

## Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C2MeasureExecB.md` (this report)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C2MeasureExecB/output.txt`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C2MeasureExecB/disagreed-round53-c1.txt`

No tools installed or updated. No tool output inconsistent with its described behavior. No ledger edits. No row needed an individual fresh-clone rerun: the mismatch output identifies the cause as the current C1 predicate not meeting its own confirmation/prior-art thresholds.

Report: `.ufo/waves/round-53/w3/C2MeasureExecB.md`
