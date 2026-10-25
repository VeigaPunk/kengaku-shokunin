# F35SeparabilityC1 — Causal separability of C2 surfaces from C1 (kengaku r35 wave 2, falsify)

Seat: F35SeparabilityC1 (executor, leaf). Target: item F35SeparabilityC1 — in a fixture clone at
`dfee6fff631ebc5f623ba4506e5c7992a215401c`, revert ONLY C2's surfaces to freeze `11d64530179b78e33ba6074fc77d63d36ee7ac31`, fixture-commit, and run the C1 counter — it must stay `checks=6 defects=0`, `PREDICATE C1 pass`.

## Method

Fixture per the wave-2 rule:

```
D=$(mktemp -d /tmp/k35f-XXXX)            # /tmp/k35f-K8Tp
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone '*'
git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c
git -C "$D/lane" rev-parse --show-toplevel   # -> /tmp/k35f-K8Tp/lane (== $D/lane, TOPLEVEL_OK)
git -C "$D/lane" rev-parse HEAD               # dfee6fff631ebc5f623ba4506e5c7992a215401c
git -C "$D/lane" status --porcelain           # empty
```

## Files reverted (exactly four, to freeze bytes)

Freeze→tip deltas were identified with `git diff 11d64530 dfee6fff -- <path>`; only these C2 surfaces were reverted:

1. **corpus/defects.jsonl — statuses.** Tip flips all five ledger rows' `status` open→closed (diff: 5 insertions / 5 deletions). Restored whole file from freeze: `git diff 11d64530` for this path is **empty** (byte-identical to freeze).
2. **SCORECARD.md — D4 correction line.** Tip appended the block `## Corrections recorded in round 35 …` + `- **D4 correction (round 34 C2):** …` (lines 1174–1177 at tip). Removed exactly those 4 lines from the fixture; the remaining tip-vs-freeze diff for SCORECARD.md is only the non-C2 round-35 additions (two capability table rows at ~line 559 and the `## Round 35 …` section). The D4 region is again byte-identical to freeze.
3. **corpus/lessons/round-34.md — round-34 lesson erratum.** Tip appended the 4-line `## Erratum (appended round 35, …)` tail (D5). Restored whole file from freeze: diff vs freeze **empty**.
4. **.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS — round-34 manifest.** Tip appended the two evaluator entries `test_outputs.py` / `test.sh` (D3). Removed those two lines; diff vs freeze **empty**.

Fixture-commit (clone only, identity `fixture <fixture@invalid>`): `a8936870d09b0c6a408ee469616c71867d987535`, 4 files changed, 5 insertions(+), 15 deletions(-); post-commit working tree clean.

## Evidence

### Baseline (agreement side, same detector, pre-revert, fixture at tip dfee6fff)

```
$ python3 plans/round35_c1_verify.py --lane .
V1 ok
V2 ok
V3 ok
V4 ok
V5 ok
V6 ok
checks=6 defects=0
PREDICATE C1 pass
$ echo $?
0
```

### After reverting the four C2 surfaces (fixture commit a893687)

```
$ python3 plans/round35_c1_verify.py --lane .
V1 ok
V2 ok
V3 ok
V4 ok
V5 ok
V6 ok
checks=6 defects=0
PREDICATE C1 pass
$ echo $?
0
```

Identical output, identical exit code, pre- and post-revert.

### The revert is real (perturbation bites C2, not C1)

Same fixture, C2 ledger, after the revert:

```
$ python3 plans/defect_ledger.py --lane .
R34-D1 status=open observed=pass agree=NO untracked=0
R34-D2 status=open observed=pass agree=NO committed_mirror_paths=0
R34-D3 status=open observed=fail agree=yes listed=4 evaluator_listed=False bad=0
R34-D4 status=open observed=fail agree=yes correction_lines=0
R34-D5 status=open observed=fail agree=yes erratum_lines=0 r35_mistake_row=True
rows=5 closed=0 observed_pass=2 mismatches=2
PREDICATE C2 fail
$ echo $?
1
```

The four-surface revert flips D3/D4/D5 red (the three checks whose observation bytes are the reverted
files), while D1 (working-tree check by design) and D2 (committed scratch-mirror deletions — outside
this assignment's four named surfaces) still observe pass. C2's predicate goes fail; C1's predicate is
unchanged.

### Verification that the reverted surfaces equal freeze bytes

```
$ git diff 11d64530179b78e33ba6074fc77d63d36ee7ac31 -- \
    corpus/defects.jsonl corpus/lessons/round-34.md \
    .ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS
(no output — byte-identical)
```

## Conclusion

C1's counter is causally separable from C2's surfaces: reverting all four named C2 surfaces to the
freeze bytes leaves `V1–V6 ok, checks=6 defects=0, PREDICATE C1 pass, exit 0` — exactly the frozen
C1 predicate — while the same revert demonstrably changes C2's ledger observations (D3/D4/D5 flip to
fail, C2 predicate fail). Agreement is supported by the disagreement evidence that would have shown
coupling: the identical detector output before and after a real, C2-reddening perturbation.

## Notes / risks

- V5 ran via `uv run --no-project --with biopython==1.85 python3` (system python3 lacks Bio), the counter's documented fallback; output matched the frozen receipt byte-for-byte in both runs.
- No lane file outside the fixture was written; no git/jj mutating command ran in the live lane; fixture `rm -rf /tmp/k35f-K8Tp` executed after the runs.
- No tool installs were performed (used existing git 2.56.0, python3, uv).
- Scope note: the assignment enumerates four C2 surfaces; the round-35 lesson Mistakes row and the round-34 scratch-mirror deletions (other C2-touched areas per `plans/round-35-claims.md` §Separability) were intentionally left as landed — neither is read by the C1 counter.

VERDICT: c1-separable-yes
