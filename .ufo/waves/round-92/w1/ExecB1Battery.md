# ExecB1Battery — R92-C1 control battery (seat ExecB1Battery, leaf)

Scope: scratch clones only; lane untouched except this wave directory. Lane clone at B2
`f0018773f507f363854123856990f8ff8a87eb8c` (`git clone --shared`, detached). Scratch
`/fast/scratch/hyaku/kengaku-r92/ExecB1Battery/` removed before yield; receipts copied to
`receipts/` in this directory. Lane HEAD at run time: `288511d8` (later than B2; not measured).

## Results

| control | expected rc | observed rc | verdict |
|---|---|---|---|
| do-nothing-tip (`round92_c1_replay.py --rev f0018773`) | 1 | 1 | matches (L1, L2, L3 defects first) |
| forged-receipt (commit b631e120) | 1 | 1 | rc matches; expected L3/L4 not raised — FINDING F2 |
| forged-target (commit 717c0be4 = control 2 + ledger flip) | 1 | 1 | rc matches; ledger flip gives executed_rows=36 and L7 passes — FINDING F3 |
| positive-dry (`round92_bs_probe.py` from `git archive f0018773`) | 0 | 0 | matches: `PREDICATE R92-PROBE pass`, mismatches=0 |
| sandbox-red (control 4 command, PATH=/usr/local/bin:/usr/local/sbin) | 2 | 0 | MISMATCH — FINDING F1 |

Runtime: 184 s / 183 s / 205 s / 192 s / 186 s. Host: python 3.14.8, OpenSSL 3.6.5,
`max_user_namespaces` 122865 (read only; no sysctl touched), `/usr/bin/bwrap` present.

## Detail

**do-nothing-tip** — `TARGET executed_rows=35 ... executed=0 cases=10 legs=0 mismatches=0 defects=8`.
Defects: L1 receipt absent at `corpus/evidence/round92/bs-probe.txt`; L2 sha mismatch (receipt=absent);
L3 LANE_TIP absent; L5 case coverage 0 of 10; L6 rerun rc=0 obs=10 want=0; L7 member unexecuted,
executed_total=35; L8 probe pin unreadable (see F4); L9 stamp mismatch. `PREDICATE R92-C1 fail`.
Receipt not fabricated.

**forged-receipt** — the round-91 `corpus/evidence/round91/modernize-probe.txt` copied to
`corpus/evidence/round92/bs-probe.txt` with `MEMBER` → `llm-inference-batching-scheduler` and
`PREDICATE` → `R92-PROBE pass`. Observed defects: L2 (receipt SUBJECT_SHA = modernize's
`0c24195f…`), L5 (9 unknown case ids, `full-pass` predicted=PP vs frozen PPPPPP; `TARGET … mismatches=10`),
L6 (rerun obs ≠ forged obs), L7 (ledger unflipped), L8, L9. `PREDICATE R92-C1 fail`, rc 1.

**forged-target** — control 2 plus a scratch ledger commit setting
`llm-inference-batching-scheduler` to `status=executed, round=92` (reason removed). Result:
`TARGET executed_rows=36 … executed=0 … defects=14`. L7 passes (executed_total 36; class cells
crypto-credential 4, file-artifact 27, filesystem-metadata 4, serialization-schema 5 — exactly
`AFTER_CELLS`). Still fails on L2, L5, L6, L8, L9 → rc 1. A ledger edit alone does not satisfy the predicate.

**positive-dry** — `python3 plans/round92_bs_probe.py --lane <git archive extract> --work …`:
`MEMBER …`, `CASE_TABLE_SHA 2249d5c0…` (= A), `TOOL_SHA 13e41e91…` (= pin at lane HEAD), `CASES 10 LEGS 60`,
`mismatches=0`, `PREDICATE R92-PROBE pass`, rc 0, 192 s. Stamp fields `LANE_TIP` and `WORKTREE` degrade
(archive has no `.git`): `LANE_TIP fatal: not a git repository…`, `WORKTREE dirty` (see F5).
Last 3 CASE lines (verbatim):

```
CASE bad-hidden-b2 predicted=PPFFPF observed=PPFFPF ok=True test_output_files_exist=ok,test_input_data_integrity=ok,test_generate_and_schema=AssertionError,test_solution_shape_feasibility_and_batch_consistency=AssertionError,test_solution_coverage_no_duplicates=ok,test_performance_thresholds=AssertionError
CASE batch-mismatch-b2 predicted=PPPFPF observed=PPPFPF ok=True test_output_files_exist=ok,test_input_data_integrity=ok,test_generate_and_schema=ok,test_solution_shape_feasibility_and_batch_consistency=AssertionError,test_solution_coverage_no_duplicates=ok,test_performance_thresholds=AssertionError
CASE empty-plan-b2 predicted=PPFPFP observed=PPFPFP ok=True test_output_files_exist=ok,test_input_data_integrity=ok,test_generate_and_schema=AssertionError,test_solution_shape_feasibility_and_batch_consistency=ok,test_solution_coverage_no_duplicates=AssertionError,test_performance_thresholds=ok
```

**sandbox-red** — same command with `env PATH=/usr/local/bin:/usr/local/sbin` and absolute `python3`.
Result: rc 0, `PREDICATE R92-PROBE pass`, 10/10 cases matching, `HOST_OPENSSL absent` and `LANE_TIP absent`
in the stamp (guarded probes degrade, no defect raised). Expected rc 2 not produced. No sysctl touched.

## Findings

- **F1 (sandbox-red, unexpected rc 0).** The probe (and the counter's L6) tests `Path("/usr/bin/bwrap").exists()`
  with an absolute path; PATH manipulation cannot hide it. The `DEFECT SETUP sandbox-unavailable` branch is
  therefore reachable only if /usr/bin/bwrap is actually absent. The literal control was not reproducible
  without host mutation (moving /usr/bin/bwrap or touching sysctls, both forbidden). Supplementary check, in
  scratch only: copy of the probe with `BWRAP = "/nonexistent/bwrap"` → `DEFECT SETUP sandbox-unavailable
  /nonexistent/bwrap`, `PREDICATE R92-PROBE could-not-evaluate`, rc 2. The branch works; the gate is the path.
  Not patched.
- **F2 (forged-receipt, expected L3/L4 not raised).** L3 only checks that the receipt's LANE_TIP is an ancestor of
  the measured rev. The copied tip `b836a862` is an ancestor of the forged commit (verified
  `merge-base --is-ancestor`), so a receipt from any historical commit passes L3. L4 checks only the case-table
  bytes against A; the table is unchanged, so it passes. Coverage of receipt provenance therefore rests on L2/L5/L6/L8/L9,
  not on L3/L4. Reported, not repaired (frozen predicate).
- **F3 (forged-target, ledger-only edit).** The ledger flip alone reaches `executed_rows=36` and the exact
  AFTER_CELLS (L7 green). The counter still returns rc 1 through the receipt legs, as the contract requires.
  Recorded as confirmation that L7 is arithmetically satisfiable by a ledger edit; the receipt legs are the guard.
- **F4 (L8 at B2).** `plans/counter-pins-r91.json` at B2 has no entry for `plans/round92_bs_probe.py` (grep count 0),
  so L8 reports `probe pin unreadable` on every B2-based run, including the do-nothing control. The entry was added
  later at `b62ea270` (commit D) with sha `13e41e91…`, which matches the probe bytes at B2 and at lane HEAD
  (`288511d8`). The probe bytes are unchanged B2→HEAD (`git diff --stat` on the probe, cases, C1 counter and
  receipt path shows only the official receipt `corpus/evidence/round92/bs-probe.txt` and the ledger changed).
  Not in the expected lists; not an rc change at B2.
- **F5 (stamp degradation in extract, minor).** `stamp()` takes the first line of stdout-or-stderr, so a non-repo
  archive gives `LANE_TIP fatal: not a git repository…` and `WORKTREE dirty` (any stderr). The counter does not
  compare these fields for archive runs; they are cosmetic in the receipt but misleading.

## Notes for main agent

- These controls ran at B2 per the spec. Lane HEAD `288511d8` has the official receipt (`42bd5104`, C), the pin (`b62ea270`, D),
  and later E/F commits. Verdicts at HEAD were not measured here.
- Ledger flip arithmetic verified: B2 has 35 executed; one flip gives 36 with the four class cells at the
  frozen AFTER_CELLS values.
- No tools installed or updated (system git, python3 3.14.8, bwrap, openssl already present). No sysctls touched.
- Lane writes: only this directory (`.ufo/waves/round-92/w1/ExecB1Battery/`) and `…/w1/ExecB1Battery.md`. No git
  mutation in the lane; all commits (forged-receipt, ledger flip) were in the scratch clone, removed at exit.
- Checks the main agent should run: none from this seat (verification is the main agent's job). The controls
  themselves are the checks; reproduce with `plans/round92_c1_replay.py --lane . --rev <rev> --work DIR` after the
  official receipt is confirmed at the tip.
