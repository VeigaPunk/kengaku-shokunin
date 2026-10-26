# R40MutC1Counter — mutation test of `plans/round40_c1_verify.py` itself (wave 1)

Seat: R40MutC1Counter, 2026-10-26. Scratch: `/fast/scratch/hyaku/kengaku-r40/R40MutC1Counter` (removed at the end,
receipts copied to `.ufo/waves/round-40/build/R40MutC1Counter/`). The lane file was never edited: sha256 of
`plans/round40_c1_verify.py` was `4d47800e3551a0c7…cbd4642c` before the first run and is the same after the last
run (command: `sha256sum`, outputs in the setup log and the integrity check below). All mutants are single-line
edits of a scratch copy (`cnt/mNN-*.py`), each compiled with `python3 -m py_compile` before use.

## Axes (godspeed)

1. detector soundness — the committed controls must reproduce byte-for-byte on pristine bytes before any mutant runs;
2. caught/survived per mutant — does a committed control or the witness battery expose the mutation;
3. mechanism — for misses, name the smallest committed artifact that would expose them.

## Method

Lane clone at the freeze commit, `git -C "$S/lane" checkout bbb109505670192035ef63d7c8b37733e99fa1a3` (in the
scratch clone only); `plans/battery40` absent there (`test ! -e` → NO_BATTERY40_AT_FREEZE). Four detectors, each a
committed expectation diffed byte-for-byte against the mutated copy's stdout+exit:

- **D1** `python3 <copy> --lane "$S/lane" --work "$S/w"` vs `.ufo/waves/round-40/claims/control-c1-nothing.txt`
- **D2** `python3 <copy> --battery-dir "$CL/witness" --lane "$S/lane-edited" --work "$S/w"` vs
  `claims/control-c1-tool-edited.txt` (the edited clone is a scratch clone with one appended line in
  `plans/anchor_digest_check.py`, `git diff --stat`: `plans/anchor_digest_check.py | 2 ++`)
- **D3** `python3 <copy> --battery-dir "$S/bhostile" --only A01 --lane "$S/lane" --work "$S/w"` vs
  `claims/control-c1-hostile-daemon.txt` minus its trailing `COUNTERFACTUAL` line (that line was appended by the
  freeze harness outside the counter; module = `claims/control-c1-hostile-daemon-module.py`)
- **D4** `python3 <copy> --battery-dir "$CL/witness" --lane "$S/lane" --work "$S/w"` vs `claims/witness-run.txt`

`CL = "$S/lane/.ufo/waves/round-40/claims"`. Exit codes were captured and appended as `exit=N`; the committed files
end with the same `exit=N` line.

### Pristine baseline (detector on pristine bytes)

All four detectors on `cnt/pristine.py` (sha256 `4d47800e…cbd4642c`, identical to the lane file):
`D1_PRISTINE_MATCH`, `D2_PRISTINE_MATCH`, `D3_PRISTINE_MATCH`, `D4_PRISTINE_MATCH` — zero diff lines, exit codes 1
as recorded. The detector is sound before mutation.

## Mutants and verdicts

Sweep: `bash "$S/sweep.sh"` (10 mutants × D1–D4, sequential, `--jobs 8` default; 1219.9 s wall).
Summary (`sweep-summary.txt`, verbatim):

```
m01-exswap D1=MATCH D2=DIFF D3=MATCH D4=DIFF
m02-exloose D1=MATCH D2=MATCH D3=MATCH D4=MATCH
m03-wrong D1=MATCH D2=MATCH D3=MATCH D4=MATCH
m04-fprint D1=MATCH D2=MATCH D3=MATCH D4=MATCH
m05-nons D1=MATCH D2=MATCH D3=MATCH D4=MATCH
m06-after D1=MATCH D2=DIFF D3=MATCH D4=MATCH
m07-null D1=MATCH D2=MATCH D3=MATCH D4=MATCH
m08-needle D1=MATCH D2=MATCH D3=MATCH D4=MATCH
m09-total D1=MATCH D2=MATCH D3=MATCH D4=MATCH
m10-pathok D1=MATCH D2=MATCH D3=MATCH D4=MATCH
SWEEP_DONE
```

Line numbers refer to `plans/round40_c1_verify.py` at the freeze. "caught" = a committed control or the witness
battery exposed it; "survived" = no committed artifact did.

| # | id | changed line (`file:line`, `old -> new`) | D1 | D2 | D3 | D4 | verdict |
|---|----|------------------------------------------|----|----|----|----|---------|
| 1 | m01-exswap | `round40_c1_verify.py:395,397` — rc-silence and rc-mirror return lines of `exhibits()` swapped | MATCH | **DIFF** | MATCH | **DIFF** | **caught** |
| 2 | m02-exloose | `:404` — `return cls in ref[1] and cls in set(fx["defects"]) and cls not in mut[1]` -> same without `and cls not in mut[1]` | MATCH | MATCH | MATCH | MATCH | survived |
| 3 | m03-wrong | `:501` — `wrong += not ok` -> `wrong += 0` | MATCH | MATCH | MATCH | MATCH | survived |
| 4 | m04-fprint | `:323` — `return h.hexdigest()` -> `return "f" * 64` | MATCH | MATCH | MATCH | MATCH | survived |
| 5 | m05-nons | `:304` — `"--proc", "/proc", "--unshare-pid", "--die-with-parent"` -> drops `"--unshare-pid", ` | MATCH | MATCH | MATCH | MATCH | survived (see probe) |
| 6 | m06-after | `:561` — `after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]` -> `after = []` | MATCH | **DIFF** | MATCH | MATCH | **caught** |
| 7 | m07-null | `:510` — `if res != ref[fx["fid"]]:` -> `if False:` | MATCH | MATCH | MATCH | MATCH | survived |
| 8 | m08-needle | `:519` — drops `src.count(old) != 1 or ` from the invalid gate | MATCH | MATCH | MATCH | MATCH | survived |
| 9 | m09-total | `:225` — `TOTAL = 21` -> `TOTAL = 22` | MATCH | MATCH | MATCH | MATCH | survived |
| 10 | m10-pathok | `:329` — `return False` -> `pass` in `path_ok` | MATCH | MATCH | MATCH | MATCH | survived |

### The two catches (the line that changed)

- **m01, D4 vs `witness-run.txt`** (`m01-D4.diff`): line 29
  `MUTANT O04 order rc-silence killed by=w-o04-p10-ok-excuse` → `MUTANT O04 order rc-silence SURVIVED
  exhibits=rc-mirror`, and line 33 `MUTANTS total=21 killed=7 survived=14` → `killed=6 survived=15`. Swapping the
  legs loses the O04 witness kill (its fixture is `expect=reject`, ref rc=1, mutant rc=0, which only the true
  rc-silence leg accepts). D2 vs `control-c1-tool-edited.txt` shows the same O04 flip (`killed=6` → `killed=5`,
  `m01-D2.diff`). CAUGHT.
- **m06, D2 vs `control-c1-tool-edited.txt`** (`m06-D2.diff`): line 34 `PINS-AFTER mismatched=1` →
  `PINS-AFTER mismatched=0`. The tool-edited control is the only committed control whose pins are broken, so it is
  the only one that reads the post-run re-hash. CAUGHT.

### Survivors — each is a coverage finding, not a contract change

- **m02-exloose** — dropping `cls not in mut[1]` is invisible because no committed fixture declares a class that the
  reference prints AND the mutant still prints. Exposing it needs a fixture whose declared defects equal the
  reference's classes on some non-killing mutant of the same tool (a "declares-but-doesn't-kill" fixture).
- **m03-wrong** — `wrong` stays 0 in every committed control because every recorded FIXTURE line is `ok`; no control
  contains a fixture whose reference result contradicts its declaration. Exposing it needs one deliberately-wrong
  committed fixture with a recorded `WRONG` + `wrong=1` control.
- **m04-fprint** — every recorded control ends `tampered=0`, so a constant fingerprint is indistinguishable. Exposing
  it needs a committed control where the fixture tree provably changes during the run and the recorded output shows
  `tampered=1` (see m05 probe: the mechanism exists, the committed control never triggers it).
- **m05-nons** — the committed hostile-daemon control misses the escape by timing: its window is 3.049 s
  (`{ time python3 cnt/pristine.py --battery-dir bhostile --only A01 …; }` → `real 0m3.049s`), while the module's
  daemon fires 3 s after its spawn, which is ~3.5–3.8 s into the run (build clones the lane first). Bounded probe
  beyond the committed detectors: same command with `--only A01,A02,A03,A06,A08,A09,A15,A17,A21,A22,A27`
  (~6 s window) — m05 prints `TAMPERED hostile-late-uppercase fixture tree changed during the run` +
  `BATTERY fixtures=1 wrong=0 tampered=1 sidechannel=0`, pristine prints `tampered=0` on the identical command
  (`m05-ext2-probe.out` vs `pristine-ext2-contrast.out`). So the A1 repair is real and the tamper check works; the
  committed control just closes its window before the delayed write. Falsifier for the L1: widen the control's
  `--only` set (or shorten the daemon delay) so the recorded control shows `tampered=1` on a weakened sandbox and
  `tampered=0` on pristine.
- **m07-null** — all recorded controls print `null_detected=0`; no committed fixture is nondeterministic across two
  unmodified runs, so the null leg is unobserved. Exposing it needs a committed control with a recorded `NULL` line
  and `null_detected=1`.
- **m08-needle** — in every committed control, either the pins match (needle occurs exactly once anyway) or the pin
  mismatch alone forces `invalid`, so the `src.count(old) != 1` term never decides alone. Exposing it needs pins
  intact with a duplicated/absent needle (e.g. the tool-edited control appending a line that duplicates a mutant's
  `old` string — then pristine prints `invalid`, m08 prints a run of a no-op variant).
- **m09-total** — `TOTAL` only enters the non-dev `good` conjunction; the nothing-control records `PREDICATE C1
  fail` either way (both print `MUTANTS total=21` from `len(MUTANTS)`), and the dev branch never reads `TOTAL`. A
  changed TOTAL can only flip a passing run to fail (false negative), which no committed control exercises. Any
  committed full-pass receipt (the landing-tip C1 run) would expose it — none exists yet, by design of the freeze.
- **m10-pathok** — every committed fixture's argv satisfies the path rule, so `path_ok` returning always-True is
  unobserved. Exposing it needs a committed control with a fixture whose argv names an absolute path outside its
  directory and a recorded contract `ValueError`-style rejection (`SETUP fixture … breaks the contract`).

## Restoration evidence

- All 11 scratch copies re-hashed after the sweep; byte-identical to their before-sweep hashes
  (`hashes.txt`; before-hashes recorded in the setup log). No copy modified itself during runs.
- Restored-bytes leg: `cp cnt/pristine.py cnt/restored.py`, then D1 on the restored copy → `RESTORED_D1_MATCH`
  (byte-identical to `control-c1-nothing.txt` incl. `exit=1`); sha256 of pristine and restored both
  `4d47800e3551a0c7a39217987f436ffad9d69663d5f0efc840717edfcbd4642c`.
- Lane file `plans/round40_c1_verify.py` sha256 before first run and after all work:
  `4d47800e3551a0c7a39217987f436ffad9d69663d5f0efc840717edfcbd4642c` — unchanged. No lane file was written; the
  only lane-tree writes were inside the scratch clones.

## Receipts

`.ufo/waves/round-40/build/R40MutC1Counter/`: `sweep-summary.txt`, `pristine-D1-baseline.out`,
`restored-D1.out`, `m01-D2.diff`, `m01-D4.diff`, `m06-D2.diff`, `m05-ext2-probe.out`,
`pristine-ext2-contrast.out`, `hashes.txt`. Scratch `/fast/scratch/hyaku/kengaku-r40/R40MutC1Counter` deleted
after these copies. No tools were installed or upgraded.

VERDICT: c1-counter-mutants-2/10
