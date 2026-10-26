# R40BatLedgerRefuse — battery40 `l_refuse` (ledger refusal paths: L01, L11, L21)

Seat: executor, kengaku round 40 wave 1 (`hyaku` run 9). Ticket: write the C1 battery40 module whose
fixtures kill frozen ledger mutants **L01, L11, L21** in their declared direction (`error`) and are
wrong=0 / sidechannel=0 / null-detected=0, then prove it, measure which fixture is load-bearing, and
run the full default counter inside a clone of the lane.

Axes named: **calibration** (the three kills; the count this wave exists for) and **operability**
(contract-clean module, reproducible receipts, honest attribution of which fixture carries which kill).

## Artifact

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-40/build/R40BatLedgerRefuse/battery/l_refuse.py`
(3410 bytes, stdlib only, no imports at all)

```
sha256  19935495ca696330ba13c7de0ddbfb52ac8bdf8c15e735d4180ab8f0ac61f934
```

Three fixtures, one per advertised refusal path, each `expect=error` and `defects=[]` (a refusal prints
`REFUSE …` on stderr and, in control mode, the `TIP commit=` line on stdout; row lines are buffered and
dropped, so the exact class set is empty):

| fid | build | tool branch exercised |
|---|---|---|
| `l_refuse-source-not-a-repo` | `--source <d/plain, not a repo> --work {WORK}` | `clone_lane` l.109 `refuse("--source … is not a readable git repository")` |
| `l_refuse-work-lane-exists` | `--source <clone> --work {WORK:lane}` | `clone_lane` l.119 `refuse("will not reuse …")` |
| `l_refuse-stale-pin-ref` | control mode `--lane <clone>`, `checkout --detach`, `branch -f master HEAD~6` | `audit_pin_refs` l.160 `refuse("stale pin ref …")` |

Module source contains none of the counter's SIDECHANNEL tokens (checked directly:
`python3 -c` over `SIDECHANNEL` against the file → `[]`; the counter itself reports `sidechannel=0`).

## Mutants and why each fixture kills it (read from `plans/round40_c1_verify.py` MUTANTS)

| id | `old -> new` (plans/ledger_tip.py) | ref | mut | kill |
|---|---|---|---|---|
| L01 `error` | `raise SystemExit(2)\n\n\ndef load_module` → `raise SystemExit(1)…` (l.23-25, the single `refuse()` exit, docstring "`2` usage/clone/setup refusal") | 2 | 1 | any refusal fixture |
| L11 `error` | `if dest.exists():\n        refuse` → `if False:\n        refuse` (l.58 "The clone is created at `<work>/lane` (must not exist)") | 2 | 0 | `l_refuse-work-lane-exists` |
| L21 `error` | `if rev and rev != tip:\n            refuse(f"stale pin ref` → `if False:\n …` (l.44-45 stale pin ref REFUSE) | 2 | 0 | `l_refuse-stale-pin-ref` |

Direct measurement of the direction (independent of the counter; scratch clone `$S/proof`, ref tool =
the lane's pinned bytes, mutants = those exact `old -> new` replacements):

```
--- L01 ref  : rc=2  refuse=REFUSE --source …/plain is not a readable git repository
--- L01 mut  : rc=1  refuse=REFUSE --source …/plain is not a readable git repository      (exit relabelled only)
--- L11 ref  : rc=2  refuse=REFUSE will not reuse …/w3/lane; remove it first
--- L11 mut  : rc=0  first=TIP commit=3077adbc… clone=…/w4/lane  (clone into the existing empty dir);  rows=9 closed=9 observed_pass=9 mismatches=0
--- L21 ref  : rc=2  first=TIP commit=3077adbc… dirty=0 | REFUSE stale pin ref: refs/heads/master resolves to 9d3aff94…
--- L21 mut  : rc=0  9 `agree=` row lines, 1 `REF AUDIT`, summary rows=9 closed=9 observed_pass=9 mismatches=0
```

L21 reference prints exactly 1 stdout line (`TIP commit=…`); the mutant reports a *clean* 9-row ledger
against a commit the `TIP commit=` line does not name — the exact harm the refusal exists to prevent.

## Proof in my clone (partial counter, exactly as ticketed)

```
$ S=/fast/scratch/hyaku/kengaku-r40/R40BatLedgerRefuse; export TMPDIR="$S"
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ python3 plans/round40_c1_verify.py --lane "$S/lane" \
    --battery-dir "$PWD/.ufo/waves/round-40/build/R40BatLedgerRefuse/battery" \
    --only L01,L11,L21 --work "$S/w"
PINS total=3 mismatched=0
FIXTURE l_refuse-source-not-a-repo tool=ledger expect=error declared=- observed_rc=2 observed=- ok
FIXTURE l_refuse-work-lane-exists tool=ledger expect=error declared=- observed_rc=2 observed=- ok
FIXTURE l_refuse-stale-pin-ref tool=ledger expect=error declared=- observed_rc=2 observed=- ok
MUTANT L01 ledger error killed by=l_refuse-source-not-a-repo -- plans/ledger_tip.py:23-25 'Exit codes are the registry row's contract (SKILL.md:581): ... 
MUTANT L11 ledger error killed by=l_refuse-work-lane-exists -- plans/ledger_tip.py:58 'The clone is created at <work>/lane (must not exist)'
MUTANT L21 ledger error killed by=l_refuse-stale-pin-ref -- plans/ledger_tip.py:44-45 'REFUSE stale pin ref … (exit 2) the ref exists but resolves to 
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
exit=0   (real 0m10.691s)
```

Re-run on the same battery dir (`--work "$S/w3"`, then `--work "$S/w"` again): **byte-equal** output
(`diff` empty, `BYTE-EQUAL-PARTIAL`), same `killed=3 … null_detected=0` both times — the reference
result on these three fixtures is stable. Receipts: `receipts/partial-L01-L11-L21.txt`,
`receipts/partial-L01-L11-L21-rerun.txt`.

## Load-bearing table (each fixture removed in turn)

Variants were generated mechanically from the module (same build functions, `FIXTURES` without entry
*i*), each run with the same `--only L01,L11,L21`:

| dropped fixture | FIXTURE lines | MUTANT lines | BATTERY/MUTANTS | flips to SURVIVED |
|---|---|---|---|---|
| `l_refuse-source-not-a-repo` | work-lane-exists ok, stale-pin-ref ok | L01 killed by=l_refuse-work-lane-exists · L11 killed · L21 killed | `wrong=0 … sidechannel=0`, `killed=3 survived=0` | **none** |
| `l_refuse-work-lane-exists` | source-not-a-repo ok, stale-pin-ref ok | L01 killed by=l_refuse-source-not-a-repo · **L11 SURVIVED exhibits=none** · L21 killed | `wrong=0`, `killed=2 survived=1` | **L11** |
| `l_refuse-stale-pin-ref` | source-not-a-repo ok, work-lane-exists ok | L01 killed by=l_refuse-source-not-a-repo · L11 killed · **L21 SURVIVED exhibits=none** | `wrong=0`, `killed=2 survived=1` | **L21** |

Receipts: `receipts/drop-source-not-a-repo.txt`, `receipts/drop-work-lane-exists.txt`,
`receipts/drop-stale-pin-ref.txt`.

Honest attribution note: **L01's kill is not individually load-bearing.** Its mutation relabels the one
`refuse()` exit, so all three refusal fixtures exhibit it; dropping the source-not-a-repo fixture leaves
the other two fixtures suitably placed (L01 is still killed, by `l_refuse-work-lane-exists`). Only L11
and L21 have a single fixture each that carries their kill. That is a property of the mutant, not of a
missing fixture: no refusal-only fixture can exhibit L01 while another refusal fixture does not.

## Full default counter inside the clone

`cp battery/l_refuse.py "$S/lane/plans/battery40/"` — copy verified byte-identical
(`sha256sum` on both sides: `19935495…f934`), then

```
$ python3 plans/round40_c1_verify.py --lane "$S/lane" --work "$S/w2"
PINS total=3 mismatched=0
FIXTURE l_refuse-source-not-a-repo tool=ledger expect=error declared=- observed_rc=2 observed=- ok
FIXTURE l_refuse-work-lane-exists tool=ledger expect=error declared=- observed_rc=2 observed=- ok
FIXTURE l_refuse-stale-pin-ref tool=ledger expect=error declared=- observed_rc=2 observed=- ok
MUTANT A01 … A27   SURVIVED exhibits=none   (11 anchor mutants; no anchor fixture exists yet this wave)
MUTANT L01 ledger error killed by=l_refuse-source-not-a-repo
MUTANT L05 … L15   SURVIVED exhibits=none   (4 ledger mutants outside this module's three refusals)
MUTANT L11 ledger error killed by=l_refuse-work-lane-exists
MUTANT L21 ledger error killed by=l_refuse-stale-pin-ref
MUTANT O04, O12, O14 SURVIVED exhibits=none  (order mutants; no order fixture this wave)
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=3 survived=18 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
exit=1   (real 0m12.600s)
```

The full run's 18 survivors are the A- and O- mutants and L05/L06/L14/L15, i.e. every mutant whose
tool has no fixture in my module — expected for a wave-1 seat that lands one module; `PREDICATE C1
fail` is the honest state of the lane until the other battery40 modules land and L1 integrates.
`invalid=0 null_detected=0 tampered=0 wrong=0` in the full run too. Receipt:
`receipts/full-default-counter.txt`.

## Risks / limits

- **Redundant L01 kill** (above): a kill is recorded per mutant, so the counter is satisfied, but the
  source-not-a-repo fixture is not the reason L01 dies. If L1 prefers strict one-fixture-one-kill
  attribution, the module can drop that fixture without losing a kill — I kept it because it is the
  T08 witness the freeze names and it demonstrates the `clone_lane` source test itself.
- **Mutant runs are not refusals**, so the two refusal fixtures that reach past the refusal (L11's
  clone-into-existing-dir, L21's stale binding) execute the whole ledger under the mutant; that is
  ~9 s wall for the subset and reaches `rows=9 observed_pass=9 mismatches=0`. The tool runs keep the
  caller's PATH/HOME (frozen limit); if `uv` were unavailable, `r35_d1` would raise
  `CalledProcessError` → `refuse` → mutant exit 1, still inside the `error` direction (0 or 1), so the
  kill does not depend on `uv` being present.
- Fixtures copy the live lane corpus (`ctx.clone`), so their reference result is a landing-tip result,
  as the freeze requires; a later corpus change that makes a check raise `CalledProcessError` would turn
  a reference `2` into `2` only if it happens before the pin-ref audit — no action needed now, noted for
  re-measurement at landing.
- No fixture writes outside its own `d`; all git calls go through `ctx.git`/`ctx.clone` (toplevel
  checked by the counter), and no outside path appears in any argv (`path_ok` passed for all three).
- Nothing frozen was edited: `PINS mismatched=0` and `PINS-AFTER mismatched=0` in every run above; the
  lane clone's only addition was the untracked `plans/battery40/l_refuse.py` used for the full-default
  run. No tool installs, no pacman, no network, no writes in the lane outside my report dir.
- Scratch `/fast/scratch/hyaku/kengaku-r40/R40BatLedgerRefuse` removed before this report was filed
  (`trap 'rm -rf -- "$S"' EXIT`-equivalent, run explicitly); every receipt needed is copied into
  `receipts/` here.

Files changed (all inside my report dir): `battery/l_refuse.py` (new module, for L1 to land as
`plans/battery40/l_refuse.py`), `receipts/*.txt` (6 run receipts), this report.

VERDICT: battery40-l_refuse-killed-3/3-wrong-0
