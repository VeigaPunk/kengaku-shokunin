# R40BatLedgerRows — `battery40/l_rows.py` (ledger row accounting)

Seat: round-40 wave 1 executor. Lane read-only; nothing in `plans/`, `corpus/` or the lane Git index touched.
Frozen inputs read, not modified: `plans/round-40-claims.md`, `plans/round40_c1_verify.py` (MUTANTS L05, L06, L14,
L15), `plans/ledger_tip.py`, `plans/defect_ledger.py`, `plans/round36_c1_verify.py`, `plans/pkg_gate.py`.

## Files changed

| path | change |
|---|---|
| `.ufo/waves/round-40/build/R40BatLedgerRows/battery/l_rows.py` | new, 4 fixtures, stdlib-only (no imports at all) |
| `.ufo/waves/round-40/build/R40BatLedgerRows.md` | this report |

Module sha256: `55fb079eacc659d1d88da942d95c77ded1014baf1a4cfd2464d3592d251d6ad5`
(`sha256sum .ufo/waves/round-40/build/R40BatLedgerRows/battery/l_rows.py`). SIDECHANNEL scan: `sidechannel=0` on
every run below. Scratch `/fast/scratch/hyaku/kengaku-r40/R40BatLedgerRows` removed at the end; lane HEAD used was
`3077adbc7145726519f60f01426a5d03381ad444` (master, `git -C "$S/lane" rev-parse HEAD`), pins `mismatched=0`.

## Fixtures (one behaviour each)

Every fixture clones the lane via `ctx.clone(d / "lane")` and runs `ledger_tip.py --lane <clone>` (control mode), so
the advertised accounting rules are exercised on a real tip tree; `argv` holds only that one absolute path inside
`d`. Reference result = all 9 ledger rows evaluated at tip with exactly one broken fact.

| fid | breaks | advertised rule / mutant | expect | declared defects (reference) |
|---|---|---|---|---|
| `l_rows-open-row` | R34-D2 relabelled `open` although its check passes | `ledger_tip.py:20-21` mismatches counts open rows whose check passes · **L05** | reject (rc 1) | `NO:R34-D2` |
| `l_rows-empty-ledgers` | both ledgers truncated | `ledger_tip.py:23-24` `0` needs rows (`return 0 if (rows and mism == 0)`) · **L06** | reject (rc 1) | none (zero rows) |
| `l_rows-check-crashes` | `.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS` unlinked, so `r34_d3` raises `FileNotFoundError` | `ledger_tip.py:228` "a crash is an observed failure, never a pass" · **L14** | reject (rc 1) | `NO:R34-D3` |
| `l_rows-unknown-check` | R34-D5 `check` → `r34_d6` (no `CHECKS` entry) | `ledger_tip.py:20-21` + `:220` unknown check is a failed check · **L15** | reject (rc 1) | `NO:R34-D5` |

Note the Hints' T10 shape was kept but re-expressed on a lane clone (the counter's `ctx.lane` is a clone of the lane,
so a clone-of-clone is the only writable tree); deletions/edits of tracked files leave no untracked path, which
keeps `r35_d2` (`untracked_anywhere`) green — confirmed by `observed_pass=8`/`declared=NO:R34-D3` rather than a
second `NO:R35-D2`.

## Targeted run (dev mode, `--only`)

```
python3 plans/round40_c1_verify.py --lane "$S/lane" \
  --battery-dir .../build/R40BatLedgerRows/battery --only L05,L06,L14,L15 --work "$S/w"
```
```
PINS total=3 mismatched=0
FIXTURE l_rows-open-row tool=ledger expect=reject declared=NO:R34-D2 observed_rc=1 observed=NO:R34-D2 ok
FIXTURE l_rows-empty-ledgers tool=ledger expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE l_rows-check-crashes tool=ledger expect=reject declared=NO:R34-D3 observed_rc=1 observed=NO:R34-D3 ok
FIXTURE l_rows-unknown-check tool=ledger expect=reject declared=NO:R34-D5 observed_rc=1 observed=NO:R34-D5 ok
MUTANT L05 ledger rc-silence killed by=l_rows-open-row -- plans/ledger_tip.py:20-21 'mismatches counts every closed row whose check fails plus every
MUTANT L06 ledger rc-silence killed by=l_rows-empty-ledgers -- plans/ledger_tip.py:23-24 '`0` no mismatch · `1` a ledger row genuinely disagrees' (exit 0
MUTANT L14 ledger rc-silence killed by=l_rows-check-crashes -- plans/ledger_tip.py:228 '# a crash is an observed failure, never a pass'
MUTANT L15 ledger rc-silence killed by=l_rows-unknown-check -- plans/ledger_tip.py:20-21 (as L05: a closed row whose check fails is a mismatch; an unknow
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```
24.8 s wall (`time`). Every FIXTURE line `ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0`.

## Load-bearing table (leave-one-out)

Method: each variant module = this module with exactly one `FIXTURES` entry removed (generated under `$S/variants`,
scratch only), counter invoked with `--battery-dir "$S/variants/<fid>" --only L05,L06,L14,L15`. Each run printed
`BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0` and `MUTANTS total=4 killed=3 survived=1 invalid=0
null_detected=0`.

| fixture removed | mutant that flips to SURVIVED | surviving line |
|---|---|---|
| `l_rows-open-row` | L05 | `MUTANT L05 ledger rc-silence SURVIVED exhibits=none` |
| `l_rows-empty-ledgers` | L06 | `MUTANT L06 ledger rc-silence SURVIVED exhibits=none` |
| `l_rows-check-crashes` | L14 | `MUTANT L14 ledger rc-silence SURVIVED exhibits=none` |
| `l_rows-unknown-check` | L15 | `MUTANT L15 ledger rc-silence SURVIVED exhibits=none` |

Each removal flips exactly its own mutant and leaves the other three killed: 1:1 attribution, no fixture works only
by co-presence of another.

## Full default run

Module copied to `"$S/lane/plans/battery40/l_rows.py"` (sha256 identical to the deliverable), then
`python3 plans/round40_c1_verify.py --lane "$S/lane" --work "$S/w2"`:

```
PINS total=3 mismatched=0
FIXTURE l_rows-open-row tool=ledger expect=reject declared=NO:R34-D2 observed_rc=1 observed=NO:R34-D2 ok
FIXTURE l_rows-empty-ledgers tool=ledger expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE l_rows-check-crashes tool=ledger expect=reject declared=NO:R34-D3 observed_rc=1 observed=NO:R34-D3 ok
FIXTURE l_rows-unknown-check tool=ledger expect=reject declared=NO:R34-D5 observed_rc=1 observed=NO:R34-D5 ok
MUTANT L05 ledger rc-silence killed by=l_rows-open-row -- plans/ledger_tip.py:20-21 'mismatches counts every closed row whose check fails plus every
MUTANT L06 ledger rc-silence killed by=l_rows-empty-ledgers -- plans/ledger_tip.py:23-24 '`0` no mismatch · `1` a ledger row genuinely disagrees' (exit 0
MUTANT L14 ledger rc-silence killed by=l_rows-check-crashes -- plans/ledger_tip.py:228 '# a crash is an observed failure, never a pass'
MUTANT L15 ledger rc-silence killed by=l_rows-unknown-check -- plans/ledger_tip.py:20-21 (as L05: a closed row whose check fails is a mismatch; an unknow
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=4 survived=17 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```
30.6 s wall. The 17 survivors are the other seats' mutants: this clone carries only `l_rows.py` in
`plans/battery40`, and `PREDICATE C1 fail` is the honest state of a single-module battery, not a defect of this one.
All 17 surviving lines read `exhibits=none`, so no fixture of mine exhibits a direction it was not declared in.

## Behaviour / contract notes for the L1 integration

- `defects` are exact class sets printed by the unmodified tool: `NO:<row id>` per row line with `agree=NO`; the
  empty-ledger fixture declares `[]` because the reference prints no row statement at all.
- `expect=reject` (rc 1) on all four: `rows=0` exits 1 via `return 0 if (rows and mism == 0) else 1`, so the
  empty-ledger fixture reaches L06's branch and not a refusal.
- The crash fixture raises `FileNotFoundError` (an `Exception`, not `CalledProcessError`), so it lands in the
  generic handler L14 mutates and not in the exit-2 refusal path.
- No `{WORK}` token is used and no fixture writes outside its own `d`; tool runs inherit PATH/HOME (`uv` from
  `~/.local/bin` reached: `r35_d1`'s `tip_package_rc` passed, since every row shows `observed=pass` except the one
  fixture breaks).
- Side-channel heuristic: `sidechannel=0` (module contains none of the counter's SIDECHANNEL tokens; the words it
  uses are `clone`, `ledger`, `check`, `manifest`, `status`, `open`).

## Risks

1. Four fixtures exercise four of the seven ledger mutants only; L01, L11, L21 (exit-2 directions) remain
   `SURVIVED` in my clone and belong to other wave seats (`w_l21-control-stale-master`, `w-l11-work-exists` in
   `claims/witness/w_ledger.py` already show rc=2 for L21/L11 — someone must land them as fixtures).
2. Both `l_rows-open-row` and `l_rows-unknown-check` reach the same `rc-silence` predicate (ref 1 → mutant 0); their
   attribution is separated only by which row the fixture breaks (verified by the 1:1 leave-one-out table).
3. Cost: each ledger tool run evaluates all 9 rows, including the round-35 gate battery (14 gate fixtures + tip
   `--rerun`). Measured 24.8 s targeted / 30.6 s full with `--jobs 8`; a full 21-mutant run with all seats' modules
   will scale with the number of ledger fixtures, not with mutants alone.
4. The three ledger fixtures that mutate a tracked file leave the fixture clone dirty (`dirty=<n>` on the TIP line,
   as designed for control mode); the counter accepts this, but a future fixture that must show `dirty=0` needs a
   commit (not done here).

No blockers. No tools installed (nothing needed; `bwrap`, `git`, `python3` present, pacman untouched).

VERDICT: battery40-l_rows-killed-4/4-wrong-0
