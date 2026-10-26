# R40BatOrder — battery40 order-gate module (C1, round 40 wave 1)

Seat: R40BatOrder (executor). Lane read-only; everything written below is my build subdir.

## Files changed
- `/.ufo/waves/round-40/build/R40BatOrder/battery/o_gate.py` — new, 62 lines, stdlib only.
  sha256 `ffc40e5e09698e3ec10ba7835e0b8a7b769341c3a8874214f0b79d9b915d27d8`.
  Intended integration path by the L1: `plans/battery40/o_gate.py` (not written by me in the lane).
- `/.ufo/waves/round-40/build/R40BatOrder.md` — this report.
- Scratch, deleted before finish: `/fast/scratch/hyaku/kengaku-r40/R40BatOrder/` (clone, fixture
  work dirs, single-fixture-removed variants, `plans/battery40/` test copy).

No lane file (`corpus/`, `plans/`, scorecards, `SKILL.md`, git index/jj) was touched; the three
tripwire tools and their pins are unmodified (`PINS total=3 mismatched=0` on every run below).

## Behaviour (one fixture per advertised behaviour, `o_gate-` prefix)
Each `build(ctx, d)` constructs a two-commit repository from scratch with `ctx.init` (commit 1
freezes `plans/round-42-claims.md` plus one file under `.ufo/waves/round-42/claims/`; commit 2 adds
`corpus/evidence/round42/probe.txt`) and returns
`["--lane", <d>/repo, "--claims", <rel>, "--receipt", <rel>]`. Round number 42 (not 50); file texts
are my own (`gate: P10 ok receipt unreadable`, a 28-case-shaped one-line receipt, a two-line
claims header). All absolute argv paths lie inside `d`; no `{WORK}` token is used; `ctx.lane` is
never read.

| fid | mutant (direction) | what it demonstrates | expect | defects |
|---|---|---|---|---|
| `o_gate-p10-ok-excuse` | O04 `rc-silence` | a claims blob shows `gate: P10 ok receipt unreadable`; only a `DEFECT` line may carry the executed-nothing excuse, so the reference reports a hit and exits 1, while the excuse-for-any-verdict mutant stays silent and exits 0 | reject (rc 1) | `hit:gate-p10` |
| `o_gate-claims-gitlink` | O12 `rc-error` | a gitlink (mode `160000`, absent commit id) under claims/ is a tree entry, not a blob: the reference skips it and the order holds, while the field-count-only mutant feeds the commit id to `cat-file blob` (no such object) and exits 2 | accept (rc 0) | — |
| `o_gate-claims-bak-name` | O14 `error` | claims file `plans/round-42-claims.md.bak` is not `round-NN-claims.md`; the anchored reference is a setup error (2), while the unanchored pattern accepts the prefix and prints a verdict | error (rc 2) | — |

Sidechannel scan over the module source (counter's 16-token heuristic, case-insensitive):
`sidechannel_tokens= []`. Which is also reported by the counter itself (`sidechannel=0`).

## Retained evidence (commands + output)

### 1. Restricted development run (all three mutants) — `S=/fast/scratch/hyaku/kengaku-r40/R40BatOrder`
```
python3 .../plans/round40_c1_verify.py --lane "$S/lane" \
  --battery-dir .../build/R40BatOrder/battery --only O04,O12,O14 --work "$S/w"
```
```
PINS total=3 mismatched=0
FIXTURE o_gate-p10-ok-excuse tool=order expect=reject declared=hit:gate-p10 observed_rc=1 observed=hit:gate-p10 ok
FIXTURE o_gate-claims-gitlink tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_gate-claims-bak-name tool=order expect=error declared=- observed_rc=2 observed=- ok
MUTANT O04 order rc-silence killed by=o_gate-p10-ok-excuse -- plans/order_check.py:15-16 'a gate `P10` line whose detail is anything other than `receipt
MUTANT O12 order rc-error killed by=o_gate-claims-gitlink -- plans/order_check.py:37 'it reads every blob under claims/' (non-blob tree entries are not
MUTANT O14 order error killed by=o_gate-claims-bak-name -- plans/order_check.py:26-27 'Exit: ... 2 setup error (..., unparseable round number, bad ar
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
exit=0
```
Every FIXTURE line is `ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0`, and each of
O04/O12/O14 is `killed by=<my fid>`.

### 2. Load-bearing table (each fixture removed in turn, re-run with the same `--only`)
Variants generated under `$S/no-*/o_gate.py` by deleting only the one fixture block (helper and
the other two fixtures unchanged).

| removed fixture | result |
|---|---|
| `o_gate-p10-ok-excuse` | `MUTANT O04 ... SURVIVED exhibits=none`; O12 and O14 still killed; `killed=2 survived=1` |
| `o_gate-claims-gitlink` | `MUTANT O12 ... SURVIVED exhibits=none`; O04 and O14 still killed; `killed=2 survived=1` |
| `o_gate-claims-bak-name` | `MUTANT O14 ... SURVIVED exhibits=none`; O04 and O12 still killed; `killed=2 survived=1` |

Each fixture is load-bearing for exactly its own mutant and for no other: a clean 3×3 diagonal.
Removal receipts also show `wrong=0 tampered=0 sidechannel=0` on the reduced batteries.

### 3. Full default counter with the module installed in a clone
`cp` of the module into `"$S/lane/plans/battery40/"` (scratch clone only), then:
```
python3 .../plans/round40_c1_verify.py --lane "$S/lane" --work "$S/w2"
```
```
FIXTURE o_gate-p10-ok-excuse ... ok
FIXTURE o_gate-claims-gitlink ... ok
FIXTURE o_gate-claims-bak-name ... ok
MUTANT O04 order rc-silence killed by=o_gate-p10-ok-excuse -- ...
MUTANT O12 order rc-error killed by=o_gate-claims-gitlink -- ...
MUTANT O14 order error killed by=o_gate-claims-bak-name -- ...
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=3 survived=18 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
exit=1
```
`survived=18` = the 11 anchor + 7 ledger mutants, which belong to the other wave-1 seats
(A27/L01/L11/L21 are among them because their fixtures are not in this module). `invalid=0`
confirms all 21 frozen mutants still apply to the pinned tool bytes from this module's module set;
`wrong=0 tampered=0 sidechannel=0 null_detected=0` is the module's own soundness record.
`PREDICATE C1 fail` at this point is expected: the claim needs all 21 modules.

## Risks / limits (named, not hidden)
- A kill records a result difference in the declared direction, not the fixture's intent (freeze
  limit, unchanged by this seat).
- `o_gate-p10-ok-excuse` uses the `gate: ` echo prefix form of the `P10` line, matching
  `GATE_P10`'s optional prefix; the mutant's `EXECUTED_EXCUSE` match is what silences it — the
  fixture does not depend on the prefix, the same text without it kills O04 identically.
- `o_gate-claims-gitlink` names an absent commit (`3`×40) so the mutant's `cat-file blob` fails
  deterministically; a mutant that tolerated a failed `cat-file` would not be O12, so this is the
  intended discriminator, not a fixture artefact.
- `o_gate-claims-bak-name` accepts mutant exit 0 or 1 per the frozen direction; measured mutant
  behaviour is a verdict print (the `.bak` repo has no hits), so it lands on the 0 branch.
- The module relies only on git (`init`, `add`, `update-index --cacheinfo`, `commit`); no network,
  no clone of the lane, no writes outside `d`.

## Tooling
No install or upgrade performed; no package manager invoked (pacman paused host-wide).

VERDICT: battery40-o_gate-killed-3/3-wrong-0
