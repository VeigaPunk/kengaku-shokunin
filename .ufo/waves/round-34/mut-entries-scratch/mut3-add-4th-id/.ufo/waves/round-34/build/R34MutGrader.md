# R34MutGrader — standing grader regression probe

**Mutant:** In a scratch copy of `corpus/evidence/round12-ladder/results-r12.jsonl`, changed only the stored `ok` value to `false` for record `{cell:"A-INC", pid:201, turn:1}` (pristine value was `true`). The source tree and committed fixture were not modified. Scratch files are under `.ufo/waves/round-34/build/R34MutGrader.scratch/`.

**Expected detector:** `python3 grader.py --r12-jsonl <scratch JSONL>` should pass on pristine bytes, report `MISMATCH r12.replay.A-INC.ok` and exit 1 on the mutation, then pass after restoration.

## Actual outputs

`python3 grader.py --selftest; echo "SELFTEST_EXIT=$?"`:

```text
[selftest] PASS S0 control (clean copies): exit 0, expected 0
[selftest] PASS S1 stored-ok flip (record layer): exit 1, expected 1 + check-id r8.replay.A-INC.ok (flip applied: True, id fired: True)
[selftest] PASS S2 run.log SUMMARY edit (summary layer): exit 1, expected 1 + check-id r8.summary.A-INC (id fired: True)
[selftest] PASS S3 raw-digit bump (re-parse layer): exit 1, expected 1 + check-id r9.replay.A-MONO.got (mutation applied: True, id fired: True)
[selftest] PASS S4 r11 stored-ok flip (record layer): exit 1, expected 1 + check-id r11.replay.A-CKPT4710.ok (flip applied: True, id fired: True)
[selftest] PASS S5 r11 run.log SUMMARY edit (summary layer): exit 1, expected 1 + check-id r11.summary.A-CKPT4710 (id fired: True)
[selftest] PASS S6 stats anchors (betai/t_crit known values): all known-value assertions hold
[selftest] PASS S7 r12 stats anchors (Page L / grade_seq / Brier-BSS / Newton): all known-value assertions hold
[selftest] ALL PASS
SELFTEST_EXIT=0
```

`python3 grader.py; echo "BASELINE_EXIT=$?"`:

```text
CHECKS n=733 mismatches=0 errata_pinned=1
VERDICT: PASS — stored evidence fully re-derives offline
BASELINE_EXIT=0
```

Scratch pristine detector (`python3 grader.py --r12-jsonl <pristine.jsonl>`):

```text
[pin] r12_jsonl: SKIPPED (overridden path, treated as mutated copy)
CHECKS n=732 mismatches=0 errata_pinned=1
VERDICT: PASS — stored evidence fully re-derives offline
PRISTINE_EXIT=0
```

Mutation construction was one JSONL-streaming `jq` update of the selected record's `ok` field. `sha256sum <mutated.jsonl>`:

```text
d093ecab950fc34164d951f7e366f4dd50089e04a45fcd29b43341d55317afd2  .ufo/waves/round-34/build/R34MutGrader.scratch/mutated.jsonl
```

Mutated detector (`python3 grader.py --r12-jsonl <mutated.jsonl>`):

```text
[pin] r12_jsonl: SKIPPED (overridden path, treated as mutated copy)
MISMATCH r12.replay.A-INC.ok: 1/640 records differ (first: (201, 1, 'ok'))
CHECKS n=732 mismatches=1 errata_pinned=1
VERDICT: FAIL
MUTATED_EXIT=1
```

Restoration copied the pristine scratch bytes back to `mutated.jsonl`. `sha256sum <pristine.jsonl> <mutated.jsonl>` and `cmp -s <pristine.jsonl> <mutated.jsonl>` produced:

```text
ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1  .ufo/waves/round-34/build/R34MutGrader.scratch/pristine.jsonl
ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1  .ufo/waves/round-34/build/R34MutGrader.scratch/mutated.jsonl
RESTORE_BYTE_COMPARE_RC=0
```

Restored detector (`python3 grader.py --r12-jsonl <restored mutated.jsonl>`):

```text
[pin] r12_jsonl: SKIPPED (overridden path, treated as mutated copy)
CHECKS n=732 mismatches=0 errata_pinned=1
VERDICT: PASS — stored evidence fully re-derives offline
RESTORED_EXIT=0
```

**Verdict:** detector baseline passed; the single stored-value corruption was killed by the replay check; restored bytes matched pristine and passed again.

VERDICT: mut-grader (regression ok)
