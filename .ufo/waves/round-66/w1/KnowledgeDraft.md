# KnowledgeDraft — R66-C1 knowledge entry draft (seat report)

Seat: KnowledgeDraft (leaf member, no dispatch). Wave: kengaku r66 w1.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## What I did

Drafted the knowledge entry for R66-C1 in the seat dir only, per the frozen claims doc
(`plans/round-66-claims.md`, read in full) and the frozen probe
(`plans/round66_c1_tensor_probe.py`, sha256 `c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3`).
I wrote **no** lane file: `corpus/knowledge/tb2-torch-tensor-parallel-offline.md` is the L1's to
write. I changed no frozen case, no frozen table, no predicate, no kill rule.

## Files written (seat dir only)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-66/w1/KnowledgeDraft/tb2-torch-tensor-parallel-offline.md`
  — the knowledge entry draft (159 lines, cap 160).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-66/w1/KnowledgeDraft/verification.txt`
  — the observation receipt behind every number in the draft (76 lines).
- This report: `.ufo/waves/round-66/w1/KnowledgeDraft.md`.

Scratch used: `/fast/scratch/hyaku/kengaku-r66/KnowledgeDraft/` (two scratch fixtures: a
K2-only receipt and a hand-written full receipt). Nothing was written under `/tmp`.

## Entry shape (as specified)

1. Provenance trio opens the file, in order: `source:` (S183 row id, title, URL at pin
   `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, anchor `tests/test_outputs.py` lines 18-25 and
   43-211, sha256 `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`) →
   `verified-at: 2026-11-03 (receipt corpus/evidence/round66/tensor/receipt.txt)` →
   `recheck: python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt`.
2. Body sections: **What the grader checks** (existence check; twelve layer tests over
   bias × world size 1,2,4; gloo backend; `MASTER_PORT` 12355; the `master_weight` interface;
   child processes via `mp.spawn`) → **The five frozen cases and their vectors** (K1-K5 table
   lifted from `plans/round66_c1_tensor_probe.py`'s `frozen()`) → **The mutant design** (K4/K5
   one method body each; failure only at world sizes 2 and 4) → **Limits**.
3. Grader test names quoted exactly: `test_parallel_linear_exists`, `test_column_parallel_linear`,
   `test_row_parallel_linear`, plus all 13 junit node names verbatim.
4. No credentials, no `op://` references, no invented facts beyond the claims doc and the probe.

## Key observed values (each with its command; full transcript in `verification.txt`)

1. `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt; echo $?`
   → `CHECK ok cases=5` / `PREDICATE R66-C1 pass`, exit 0.
2. `python3 plans/round66_c1_tensor_probe.py --selftest --work <scratch>` →
   `SELFTEST {'good_accepted': True, 'mutated_refused': True}`, exit 0.
3. `sha256sum` on the committed grader and on the round-66 capture → both
   `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`; the same line is
   `corpus/evidence/round52/graders/SHA256SUMS` line 171; capture is 211 lines / 7171 bytes.
4. `sha256sum corpus/evidence/round66/tensor/cases/*/parallel_linear.py` → K1
   `1537da2a…`, K3 `316630cd…`, K4 `37a3c21b…`, K5 `edf7cab1…` (K2 is an empty `/app`,
   `case_sha=none`). All four match the receipt's `CASE` lines.
5. Parsing each committed junit XML → 13 `testcase` nodes for each of the five cases.
6. AST comparison of class-qualified method bodies (my own command, in `verification.txt` §8):
   `k4-col-nogather differing method bodies = ['ColumnParallelLinear.forward']`,
   `k5-row-noreduce differing method bodies = ['RowParallelLinear.forward']`;
   `k3-stub` differs in 4. This independently reproduces the claims doc's
   "each mutant differs from K1 by exactly one method body".
7. `diff <(grep '^VECTOR' receipt.txt) <(grep '^VECTOR' prefreeze-run2.txt)` → no output: the
   receipt of record and the pre-freeze control carry byte-identical vectors; the junit shas
   differ because the junit XML carries run-local paths and child-process ids.
8. Before-counts: `grep -c torch-tensor-parallelism corpus/evidence/round52/graders/executed17.lst`
   → `0`; `grep -n 'CLASS process-environment' corpus/evidence/round62/class-survey.txt` → line 14
   (`count=3 members=install-windows-3.11,torch-pipeline-parallelism,torch-tensor-parallelism`);
   line 21 still lists `process-environment` among `classes-uncovered`.
9. Host toolchain observed: `bubblewrap 0.13.1`, `uv 0.13.0`, venv `torch 2.15.0+cpu`,
   `is_gloo_available()` → `True`, python 3.14.8, pytest 9.2.0.

## Findings worth carrying to the L1

- **The receipt check's named limitation is real and I measured it.** A receipt written by hand in
  scratch that copies the committed `case_sha`/`junit_sha` values and the committed probe sha and
  states the frozen vectors verbatim passes `--check-receipt` with `CHECK ok cases=5`, exit 0
  (`verification.txt` §10). The gate refuses value-free and value-mismatched fabrication, not a
  fully value-copied receipt. The entry states this as a limit, as the claims doc requires.
- **A K2-only receipt is refused** (`verification.txt` §9): `CHECK defect: k1-ref has no VECTOR
  line` (and one each for K3/K4/K5), exit 1. The do-nothing control alone cannot satisfy the
  predicate.
- **Registry drift to reconcile (I did not edit the registry).** The frozen claims doc's
  frontier step says "S183 status `queued` → `mined` with `used-by` = the new knowledge entry".
  At HEAD (`2c1ef88a`) S183's row is *already* `status=mined`, `recheck=180d`,
  `used-by=corpus/knowledge/tb2-grader-vacuity-triage.md` (read with
  `git show HEAD:corpus/SOURCES.md`). So the planned flip is a no-op and the `used-by` must be
  repointed to the new entry (or a second path added) for the row to cite it. This is a report,
  not an edit — the L1 owns the registry change.
- **Triad shape note for the L1.** The entry's first three lines are `source:` / `verified-at:` /
  `recheck:` in that order, as my item specifies. Note that the historical lane census triad
  (`plans/round24_census.sh` line 28) requires line 2 to be *exactly* `verified-at: YYYY-MM-DD`
  and line 3 to *start* with `recheck: YYYY-MM-DD`; my lines carry the receipt path and the
  counting command after the date, so this file does not satisfy that older regex (5 of the
  existing 67 knowledge files do). The two sibling entries written this round
  (`corpus/knowledge/tb2-kv-store-grpc-offline.md`, `corpus/knowledge/tb2-sqlite-gcov-offline.md`)
  use the same non-conforming shape, so I followed the lane's current practice and my item's
  explicit wording rather than the round-24 regex. Flagging it so the L1 can decide.

## Not done / out of scope

- The lane file `corpus/knowledge/tb2-torch-tensor-parallel-offline.md` — written by the L1.
- No registry edit (S183 `used-by`, S236/S237), no `corpus/README.md` index row, no lesson row.
- No probe execution of my own beyond `--check-receipt` and `--selftest`; I did not bind
  12355 and did not run `--run` (the receipt of record already exists and is byte-bound to the
  committed junit).
- No tool installed this seat; nothing to record under the tooling sentence.

## Verdict

The draft is complete and every number in it carries the command that produced it. The R66-C1
counting command passes against the committed receipt of record (`CHECK ok cases=5`,
`PREDICATE R66-C1 pass`, exit 0), and the probe's own selftest passes. The entry is 159 lines
(cap 160) and lives only in the seat dir. One drift item (S183 `used-by` / status) and one shape
item (triad regex) are reported for the L1's decision; neither was edited by me.
