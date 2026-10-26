# F40RevBatLRows — non-author honesty review of `plans/battery40/l_rows.py`

Lane tip ec1005a2a28bc5cfdde7723374368ed4cc956eed; review date 2026-10-26. Targets: mutants L05, L06, L14, L15
of `plans/round40_c1_verify.py` (tool `plans/ledger_tip.py`, pin 853bcb2a…, `PINS total=3 mismatched=0` on my
scratch clone before and after). I am not an author of the battery or the counter.

## Method

1. Read all 59 lines of `plans/battery40/l_rows.py` and the whole of `plans/ledger_tip.py` (254 lines),
   `plans/defect_ledger.py` CHECKS bodies, and the counter harness.
2. Verified the `adv` quotes sit where cited: `ledger_tip.py:20` ("mismatches counts every closed row whose
   check fails plus every open row whose check passes"), `:23` ("`0` no mismatch · `1` a ledger row genuinely
   disagrees"), `:220` (`ok, note = False, f"unknown check …"`), `:228` ("a crash is an observed failure, never
   a pass"), `:250` (`return 0 if (rows and mism == 0) else 1`).
3. Ran the module alone under the HOST-SAFETY sandbox (bwrap per orchestrator ruling, `--lane` on my scratch
   clone, scratch `/fast/scratch/hyaku/kengaku-r40/F40RevBatLRows`, no lane writes):
   `python3 plans/round40_c1_verify.py --lane "$S/lane" --battery-dir "$S/battery" --only L05,L06,L14,L15 --work "$S/w"`.
   Receipt: `.ufo/waves/round-40/falsify/F40RevBatLRows/run-l_rows-only-L05-L06-L14-L15.log` (run twice; second
   run reproduced below).
4. Rebuilt the fixture trees through the counter's own build child (`--build-module … --dest "$S/inspect"
   --pristine "$S/lane"`) and diffed each against the pristine tip. Receipt:
   `.ufo/waves/round-40/falsify/F40RevBatLRows/fixture-tree-inspection.log`.

## Run evidence (pasted FIXTURE/MUTANT lines, rc=0)

```
PINS total=3 mismatched=0
FIXTURE l_rows-open-row tool=ledger expect=reject declared=NO:R34-D2 observed_rc=1 observed=NO:R34-D2 ok
FIXTURE l_rows-empty-ledgers tool=ledger expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE l_rows-check-crashes tool=ledger expect=reject declared=NO:R34-D3 observed_rc=1 observed=NO:R34-D3 ok
FIXTURE l_rows-unknown-check tool=ledger expect=reject declared=NO:R34-D5 observed_rc=1 observed=NO:R34-D5 ok
MUTANT L05 ledger rc-silence killed by=l_rows-open-row
MUTANT L06 ledger rc-silence killed by=l_rows-empty-ledgers
MUTANT L14 ledger rc-silence killed by=l_rows-check-crashes
MUTANT L15 ledger rc-silence killed by=l_rows-unknown-check
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Each fixture's reference output equals its declared defect set exactly (single `NO:` row), and each mutant is
killed by exactly the fixture aimed at it.

## Per-fixture honesty verdicts

**l_rows-open-row — HONEST** (build `l_rows.py:12-21`, declaration `:51-52`, target L05).
Input: flips `"status": "closed"` → `"open"` on row R34-D2 (`l_rows.py:17-18`; occurrence count of the replace
target in `corpus/defects.jsonl` = 1, `grep -c` output "1"). R34-D2's check `r34_d2` is a pin that passes on the
untouched tip (reads only `git ls-tree` of three mirror roots, `defect_ledger.py:47-53`), so the tree holds
exactly "an open row whose check passes (stale self-assessment)". Tree diff vs tip: only `corpus/defects.jsonl`
line 2 differs (receipt). Reference rc=1 with `NO:R34-D2`; L05 (`agree = (is_closed and ok) or (st == "open" and
not ok)` → `agree = ok`, unique occurrence) loses precisely the open-and-passing half, mutant rc=0. Exactly the
advertised sentence at `ledger_tip.py:20`.

**l_rows-empty-ledgers — HONEST** (build `l_rows.py:24-29`, declaration `:53-54`, target L06).
Input: both ledger files written to 0 bytes (`l_rows.py:27-28`; inspection receipt shows `0` bytes each, no other
tree change). Reference: `rows=0`, `mismatches=0`, exit 1 via `ledger_tip.py:250` — the documented contract that
exit 0 needs at least one row; L06 (`return 0 if (rows and mism == 0) else 1` → `return 0 if mism == 0 else 1`)
returns the unearned 0. Declared defects `[]` matches the observed empty set. The `adv` cell itself quotes the
code line, so this is the advertised behaviour, not a weaker proxy.

**l_rows-check-crashes — HONEST** (build `l_rows.py:32-36`, declaration `:55-56`, target L14).
Input: unlinks only `.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS` (`l_rows.py:9,35`; inspection
receipt shows the other six capture files still present). The `r34_d3` body `read_text`s that manifest
(`defect_ledger.py:60`), so it raises FileNotFoundError, caught at `ledger_tip.py:227-228` → `ok=False` → closed
row R34-D3 disagrees → rc=1. No other check reads that path (`r34_d5` reads `nec-s091-reopen.html`,
`defect_ledger.py:90-92`), and the observed set is exactly `NO:R34-D3`. L14 flips the crash to `ok=True` → rc=0:
precisely "a crash is an observed failure, never a pass".

**l_rows-unknown-check — HONEST** (build `l_rows.py:39-47`, declaration `:57-58`, target L15).
Input: renames row R34-D5's `"check": "r34_d5"` → `"r34_d6"` (`l_rows.py:44`; occurrence count 1, `grep -c` "1").
`r34_d6` is in no CHECKS dict (`defect_ledger.py:113` has r34_d1..r34_d5; the row sits in `corpus/defects.jsonl`
so only that module's CHECKS is consulted, `ledger_tip.py:219-220`) → reference takes the `unknown check` path,
`ok=False`, closed row disagrees → rc=1. L15 flips `:220` to `ok=True` → rc=0. Tree diff vs tip: only
`corpus/defects.jsonl` line 5 differs (receipt).

## Wave-1 attack-vector checklist (all 59 lines read; none present)

- Reading the tool or its own program text at run time: no `open()` of `ledger_tip.py`/the counter/itself, no
  `__file__`, no `inspect`; only lane data files are read (`l_rows.py:16,43`). — clean
- Writes outside d (HOME, PATH dirs, other modules' fixture dirs): every write is under `ctx.clone(d / "lane")`
  (`l_rows.py:14,26,34,41`); `Ctx.clone` enforces `_inside` the fixture root (counter `:248-263`); `tampered=0`
  and the BUILT argv paths (`…/f000/lane`…`…/f003/lane`) confirm. — clean
- Relative argv tokens / symlinks out of d: all four returns are `["--lane", str(lane)]`, absolute inside d;
  `path_ok` accepted them; `find "$S/inspect" -type l` returned nothing. — clean
- `.lock`/`.git/index` fingerprint skips: module creates no `.lock` file and never touches `.git/index`; its
  edits are working-tree files whose size/mtime the fingerprint sees (post-build fingerprint, `tampered=0`). — clean
- Phase detection (telling reference from mutant): module has no imports, no environ/argv/time reads; fixtures
  are static trees built before any tool run; `null_detected=0`. — clean
- Bare-string `build()` return: all four return 2-element str lists; the counter's contract check
  (`isinstance(argv, list)`, counter `:460-464`) passed. — clean
- PATH git shim (A2): module never touches PATH or writes executables; the build child's env is counter-pinned. — clean
- Cross-module fixture forgery: build children get per-module dests (`root/fx/l_rows`), and every path stays in
  the module's own fNNN; `sidechannel=0` (token scan over the source). — clean

## Residual risk / verification gaps

- The kill rule records a result difference, not intent; my intent judgment rests on the tree diffs and the
  check-body reading above, which is exactly the admitted division of labour (frozen predicate + non-author
  review).
- My scratch lane clone carries `refs/heads/master` = c9c793ca (shared lane master has moved past the freeze
  tip), but fixture clones are detached at ec1005a2 and `audit_pin_refs` bound pin refs via its `clone-lacks-ref`
  path; no REFUSE occurred and all FIXTURE lines are `ok`. Not a battery defect; noted for reproducibility.
- I ran the four-target subset only (`--only L05,L06,L14,L15`, predicate `n/a` by design); the full frozen
  predicate run is wave-1/landing evidence, not re-verified here.

## Receipts

- `.ufo/waves/round-40/falsify/F40RevBatLRows/run-l_rows-only-L05-L06-L14-L15.log`
- `.ufo/waves/round-40/falsify/F40RevBatLRows/fixture-tree-inspection.log`

VERDICT: battery-l_rows-honest-4/4
