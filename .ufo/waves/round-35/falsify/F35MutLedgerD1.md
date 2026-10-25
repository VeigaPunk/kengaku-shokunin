# F35MutLedgerD1 — mutation-test ledger check `r34_d1` (wave 2, falsify the landed round)

Seat: executor (leaf). Scope: only the D1 working-tree check in a disposable fixture clone in `/tmp`
(never the live lane). Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, tip
`dfee6fff631ebc5f623ba4506e5c7992a215401c` (branch master). No tools installed (used existing
`git`/`python3`); no labrat spawned; no commits made in or out of the clone; no lane refs touched.

## Axis framing (godspeed)

- Axis 1 — D1 working-tree observable: does `r34_d1` (`git ls-files --others --exclude-standard --`
  `plans/round34_c1_verify.py plans/round34_defects.py plans/round34_mutate.py .ufo/waves/round-34/`)
  catch an untracked round-34 wave path and an untracked round-34 plan-tool path?
- Axis 2 — D1 ignore handling: does `--exclude-standard` keep an ignored `__pycache__/` file inert
  (documented control, no flip)?
- Both improve on every cheap mutation; no hazards (all mutations confined to the clone, untracked
  files only — no commits, no object-store writes).

## Fixture baseline (clone, sparse, detached at landed tip)

```
D=$(mktemp -d /tmp/k35f-XXXX)
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone /corpus/ /plans/ /SCORECARD.md /.ufo/waves/round-34/
git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c
```

Verified: `toplevel=/tmp/k35f-DGbp/lane == $D/lane` (`TOPLEVEL_OK`) before any write;
`HEAD=dfee6fff631ebc5f623ba4506e5c7992a215401c`; `worktree_status_lines=0`;
`tracked_round34_defects=0` (all three D1-watched plan paths absent from the tracked tree at tip).
Every git call used `git -C "$D/lane"`.

Baseline run (`python3 plans/defect_ledger.py --lane "$D/lane"`):

```
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
EXIT=0
```

D1 green in the clean clone (untracked=0), matching the frozen C2 predicate.

## Mutants

### M1 — untracked `.ufo/waves/round-34/F35probe.tmp` → D1 must FAIL (caught)

```
echo "mutant-M1" > "$D/lane/.ufo/waves/round-34/F35probe.tmp"
git -C "$D/lane" status --porcelain
?? .ufo/waves/round-34/F35probe.tmp
python3 "$D/lane/plans/defect_ledger.py" --lane "$D/lane"; echo "EXIT=$?"
R34-D1 status=closed observed=fail agree=NO untracked=1
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=4 mismatches=1
PREDICATE C2 fail
EXIT=1
```

Created1 flipped green→red (`untracked=1`), agree=NO, predicate fail, exit 1. Probe removed after capture.

### M2 — untracked `plans/round34_defects.py` → D1 must FAIL (caught)

```
echo "mutant-M2" > "$D/lane/plans/round34_defects.py"
git -C "$D/lane" status --porcelain
?? plans/round34_defects.py
python3 "$D/lane/plans/defect_ledger.py" --lane "$D/lane"; echo "EXIT=$?"
R34-D1 status=closed observed=fail agree=NO untracked=1
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=4 mismatches=1
PREDICATE C2 fail
EXIT=1
```

D1 flipped green→red (`untracked=1`), agree=NO, predicate fail, exit 1. Mutant removed after capture.

### C1 — ignored `__pycache__/x.pyc` under the wave → D1 must stay green (documented, no flip)

```
mkdir -p "$D/lane/.ufo/waves/round-34/__pycache__"; echo pyc > "$D/lane/.ufo/waves/round-34/__pycache__/x.pyc"
git -C "$D/lane" check-ignore -v .ufo/waves/round-34/__pycache__/x.pyc
.gitignore:2:__pycache__/	.ufo/waves/round-34/__pycache__/x.pyc
git -C "$D/lane" status --porcelain | wc -l   # 0
python3 "$D/lane/plans/defect_ledger.py" --lane "$D/lane"; echo "EXIT=$?"
R34-D1 status=closed observed=pass agree=yes untracked=0
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
EXIT=0
```

`__pycache__/` (lane `.gitignore:2`) matches; `--exclude-standard` keeps the ignored file invisible
to `ls-files --others`, so D1 stays green. A non-ignored untracked file is exactly M1/M2 —
`--exclude-standard` is what keeps ignored files inert. Documented, no flip.

## Result tally

| Mutation | Check | Expected | Observed | Outcome |
|---|---|---|---|---|
| M1 untracked `.ufo/waves/round-34/F35probe.tmp` | D1 | fail | `untracked=1` fail, agree=NO, exit 1 | killed |
| M2 untracked `plans/round34_defects.py` | D1 | fail | `untracked=1` fail, agree=NO, exit 1 | killed |
| C1 ignored `__pycache__/x.pyc` (control, no flip) | D1 | stay green | `untracked=0` green, exit 0 | documented |

Flip-mutants: 2/2 killed. Baseline at the landed tip dfee6fff is green
(`rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`, exit 0); both mutations flip
D1 red and take the whole predicate to fail/exit 1. Controls behave as specified.

## Cleanup

`rm -rf /tmp/k35f-DGbp` performed (confirmed inside the script). Scratch script removed. No writes
outside the clone except this report. Live lane untouched (read-only `git status`/`rev-parse`
only; it shows 5 pre-existing uncommitted modified files, the L1's integration surface, not this
seat's).

## Risks / notes

- The `--shared` clone shares the object store, but this seat created no commits and no objects
  (untracked-file mutations only); the clone was deleted. Lane HEAD/refs unchanged.
- Not in scope: D2/D3/D4/D5 checks (all green at tip in the baseline run above; D2 confirmed
  `committed_mirror_paths=0` at the landed tip).

VERDICT: d1-killed-2/2
