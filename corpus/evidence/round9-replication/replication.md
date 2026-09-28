# Round 9 probe-A replication

## Registration and ordering

Predictions were written before any endpoint request. Evidence: `predictions-r9.sha256` = `2a4f62ef20a65e7a7cb3b7414b54d0f995126209c3126ae674b7cc3af2bc1099  /tmp/kengaku-r9/predictions-r9.md`; `ordering.log` records `2026-09-28T21:17:48Z` before and after hashing; the first non-meta result record (`A-INC`, pid 101) has `request_ts=2026-09-28T21:17:58Z`. Thus timestamps side-by-side: hash-before/after **21:17:48Z / 21:17:48Z**; first request **21:17:58Z**.

Command evidence: `sha256sum /tmp/kengaku-r9/predictions-r9.md`; `cat /tmp/kengaku-r9/ordering.log`; Python scan of `results-r9.jsonl` selecting first record with `cell != meta`.

## Observed results

Final graded turn is turn 10. `results-r9.jsonl` contains 8 meta, 248 scored records, 28 fillers, no error records.

| Cell | Final passes / 8 | Mean final nwrong |
|---|---:|---:|
| A-INC | 4/8 | 0.500 |
| A-CKPT4710 | 2/8 | 0.875 |
| A-CKPT710 | 2/8 | 1.375 |
| A-MONO | 0/8 | 2.250 |

The ladder is INC > CKPT4710 = CKPT710 > MONO, not the preregistered strict dose ordering. INC final finish reasons were stop for 8/8; all other final graded calls also stop for 8/8. No final parse failures occurred.

## Paired exact sign tests

Ties are omitted; exact two-sided binomial p-values use `2*min(P[X<=wins],P[X>=wins])`, with `math.comb`, n = wins + losses.

| Pair (final pass) | INC/first wins | second wins | ties | p |
|---|---:|---:|---:|---:|
| INC vs CKPT4710 | 2 | 0 | 6 | 0.500 |
| CKPT4710 vs CKPT710 | 0 | 0 | 8 | 1.000 (undefined direction; all ties) |
| CKPT710 vs MONO | 2 | 0 | 6 | 0.500 |
| INC vs MONO | 4 | 0 | 4 | 0.125 |

## Onset and failures

INC first-error turns by pid 101–108: `None, 2, 7, 7, 3, 10, None, None`; mean among the 5 non-perfect trajectories = **5.8**. (Mean onset over all 8 is undefined because perfect trajectories have no onset.) Failure classes at final graded turn: parse fail 0/32; finish=length 0/32; state error (parsed but not exact) 12/32. The same parse/finish audit on MONO is parse 0/8, finish=length 0/8, state error 8/8.

Ack compliance audit (raw text stripped and lowercased, starts with `ok`): CKPT4710 32/56 = 57.1%; CKPT710 48/64 = 75.0%. These are ack turns only; checkpoint turns are graded JSON turns.

## Dose-response reading

Accuracy does **not** fall monotonically as checkpoints get sparser: CKPT4710 and CKPT710 both scored 2/8. However, mean final error increased (0.875 to 1.375), consistent with a weak error-severity dose signal but not a pass-rate dose response. The scaffold-assist claim receives directional support (INC > both checkpoint cells > MONO), but paired tests are underpowered and not conventionally significant at this n.

## Round-8 versus round-9

| Cell | Round 8 | Round 9 |
|---|---:|---:|
| A-INC | 7/10 | 4/8 |
| A-CKPT (4,7,10) / CKPT4710 | 1/10 | 2/8 |
| A-MONO | 0/10 | 0/8 |
| A-CKPT710 | not run | 2/8 |

R9 reproduces MONO failure and a higher INC pass rate than either checkpoint schedule, but does not reproduce the magnitude of the r8 INC advantage; the r8 ordering `7/10 > 1/10 ≈ 0/10` is not established out-of-sample by these 8 seeds.

## Prediction scoring

Point predictions (not probabilities) were preregistered, so score is `|predicted-observed|/8`, not a probabilistic Brier score.

| Cell | Predicted | Observed | Hit? | Absolute-error score |
|---|---:|---:|:---:|---:|
| A-INC | 6/8 | 4/8 | miss | 0.250 |
| A-CKPT4710 | 2/8 | 2/8 | hit | 0.000 |
| A-CKPT710 | 1/8 | 2/8 | miss | 0.125 |
| A-MONO | 0/8 | 0/8 | hit | 0.000 |

The predicted strict direction was a miss because the two checkpoint doses tied.

## Reproducibility and repository guard

Generation, scheduling, HTTP, and logging were run by `/tmp/kengaku-r9/run_r9.py`; source copy is `/tmp/kengaku-r9/replicate.py`. Core aggregation command was a Python snippet reading only `/tmp/kengaku-r9/results-r9.jsonl` and using `math.comb`; all records are JSONL and include `request_ts` on request-derived records. Final repository check command:

`git -C /home/vgpnk/projects/shokunin/kengaku-shokunin status --porcelain`

Output:

```text
?? corpus/evidence/
```

## Confidence

- Ordering evidence: **high** — hash, ordering log, and first-request timestamp are directly recorded.
- Cell pass counts and nwrong: **high** — directly aggregated from 248 scored JSONL records.
- Sign tests: **high** — exact combinatorial calculation; many pairs have six/eight ties.
- Ack compliance: **high** — directly counted from ack raw fields.
- Scaffold/dose interpretation: **medium** — directional replication is clear, but n=8 leaves wide uncertainty and checkpoint pass-rate dose is tied.

## Errata (round 10)

- The failure-classes sentence in §Onset and failures stores a defective
  state-error numerator (12 over the 32-record all-cells denominator).
  Recomputation from the committed `results-r9.jsonl` bytes — `grader.py`
  check id `r9.failure_classes.state_error`, run `python3 grader.py` at the
  repo root — gives final graded-turn passes A-INC 4 + A-CKPT4710 2 +
  A-CKPT710 2 + A-MONO 0 = 8 of 32 with 0 parse failures, hence state
  errors **24 of 32**. The stored 12 equals the two checkpoint cells'
  final failures (6 + 6) over the all-cells denominator; that provenance is
  conjectural, the corrected value is arithmetic on committed bytes. The
  original sentence stays unrevised per the append-only convention;
  `grader.py` pins the adjudicated (stored-defective, corrected) pair, so
  editing either side without a ruling fails the gate. Ruling recorded in
  `LOG.md` round-10 entry; parse-fail (0 of 32), finish=length (0 of 32)
  and the MONO audit sentence re-derive exactly and are unaffected.
