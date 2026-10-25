# F35RunC2 — C2 calibration falsify (round 35 wave 2)

Seat: F35RunC2 (executor, leaf). Target: C2 calibration predicate (`plans/defect_ledger.py`).
Lane HEAD verified: `dfee6fff631ebc5f623ba4506e5c7992a215401c` (master).

## 1. Lane working-tree re-run

`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain --untracked-files=all | wc -l` → `4`:

```
?? .ufo/waves/round-35/falsify-dispatch.json
?? .ufo/waves/round-35/falsify-spec.json
?? .ufo/waves/round-35/falsify.ready
?? .ufo/waves/round-35/falsify/swarm-registry.json
```

All four untracked files live under `.ufo/waves/round-35/` (wave-2 scaffold). None falls inside the
four paths D1 inspects (`plans/round34_c1_verify.py`, `plans/round34_defects.py`,
`plans/round34_mutate.py`, `.ufo/waves/round-34/`), so D1 observes `untracked=0`.

`cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/defect_ledger.py --lane .` → exit 0:

```
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
```

## 2. Fixture clone at the landed commit

Fixture rule applied verbatim (clone `--no-checkout --shared`, `sparse-checkout set --no-cone`
with `corpus/ plans/ SCORECARD.md .ufo/waves/round-34/`, checkout `dfee6fff…`):

```
FIXTURE=/tmp/k35f-ZYQC
TOPLEVEL=/tmp/k35f-ZYQC/lane        # rev-parse --show-toplevel verified before any use
HEAD=dfee6fff631ebc5f623ba4506e5c7992a215401c
MATERIALIZED=9193                    # git ls-files count in sparse cone
```

Required inputs all materialized: `corpus/defects.jsonl`, `plans/defect_ledger.py`,
`SCORECARD.md`, `.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS`,
`.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html`,
`.ufo/waves/round-34/build/R34C2CounterDraft.md`, `.ufo/waves/round-34/build/R34MutC2Harness.md`,
`corpus/lessons/round-34.md`, `corpus/lessons/round-35.md`.

`python3 $D/lane/plans/defect_ledger.py --lane $D/lane` → exit 0, **byte-identical output** to the lane run:

```
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
```

Fixture `git status --porcelain --untracked-files=all | wc -l` → `0` (pristine).
Fixture D1 measurement `git ls-files --others --exclude-standard -- <D1 paths> | wc -l` → `0`.
Cleanup: `rm -rf /tmp/k35f-ZYQC` done.

## 3. Which rows pass on committed bytes alone

| Row | Check | Committed-bytes-only? | Fixture observation |
|---|---|---|---|
| D1 | `r34_d1` — `git ls-files --others` over 4 paths | **No — working-tree scan** | pass (vacuous, see below) |
| D2 | `r34_d2` — `git ls-tree -r refs/heads/master` over 3 mirror roots | Yes | pass, `committed_mirror_paths=0` |
| D3 | `r34_d3` — SHA256SUMS manifest vs digest of materialized files | Yes | pass, `listed=6 evaluator_listed=True bad=0` |
| D4 | `r34_d4` — draft:8/harness:12 lines + SCORECARD correction line | Yes | pass, `correction_lines=1` |
| D5 | `r34_d5` — tag-stripped nec-s091-reopen.html quote + lesson erratum/Mistakes rows | Yes | pass, `erratum_lines=1 r35_mistake_row=True` |

D2–D5 read only committed bytes at the pinned commit; the fixture (which has exactly those bytes
and nothing else) reproduces the lane's observations 1:1. Those four rows are fully re-derivable
from a fresh clone.

**D1 is the working-tree check.** Its fixture pass is vacuous: a pristine clone has zero untracked
files anywhere, so `untracked=0` holds even if round-34 hygiene were broken — there is no
round-34 work-in-progress in the clone for D1 to detect. The lane's D1 pass is meaningful: the
only untracked files in the live lane are the four round-35 falsify-scaffold files, all outside
D1's path scope. A closure re-deriving the round-34 wave from a fresh clone would see the same
observable (`untracked=0`) **only** if its re-derivation leaves no untracked files under D1's four
paths — which is exactly the hygiene property R34-D1 encodes (round-34 wave work left untracked at
tip), so D1 cannot be re-derived from committed bytes alone and the static-clone pass proves
nothing for it. For the frozen predicate, the outputs are identical in both environments.

## 4. Falsification attempt result

No disagreement found. The C2 predicate holds in the live lane and is byte-identically reproduced
in a fresh fixture clone at the landed commit. The only non-reproducible-from-bytes row is D1,
whose observable matches in both environments; its vacuous fixture pass is flagged as a limitation,
not a mismatch. No defects in the ledger's five rows, its observations, or the checker's output
were falsified.

VERDICT: c2-lane-pass-clone-5/5
