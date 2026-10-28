# R49C2ConnCross — C1/C2 hidden coupling scan

Axes: **coverage** (C2, assigned axis); **calibration** (C1, cross-axis harm check). This is a read-only separability scan, not an admission judgment.

## Freeze and evidence basis

Stage-1 freeze verified in the committed lane tree before this scan: `9d2900af41e4d1fc6022eff99010436fde6dbd93`, timestamp `2026-10-28 09:14:40 -0300`; `git show -s` subject: `round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims`. Inspected frozen-base clone REV: `9d2900af41e4d1fc6022eff99010436fde6dbd93`. Live lane HEAD at inspection: `af88aab193e6034cb9b386472064e3c18fa90128`. No scored counter/probe was run.

Primary evidence read in full: `plans/round-49-claims.md` and `corpus/lessons/round-48-verifier-spotcheck.md`. Frozen claims §148–153 say counters share no input and receipts are disjoint. Counter/source inspection gives two material qualifications:

1. **C2 V8 scans a shared claims-receipt namespace, so C1 receipts can affect C2.** The frozen claims §117–122 locates C2's `plans/order_check.py` ordering check; `plans/order_check.py` `scan_claims()` enumerates every committed blob under `.ufo/waves/round-NN/claims/` up through the receipt commit, and `blob_hits()` fails on a non-exempt `P10 DEFECT|ok` line or `CASE … observed=` line. C1's controls and committed per-mutant outputs are also required under `.ufo/waves/round-49/claims/` (claims §80–84, §65–72); therefore an otherwise C1-scoped receipt whose literal content matches either pattern becomes a C2 V8 input. The scan also retains distinct historical blobs, so deleting or replacing a triggering receipt does not erase that historical blob from the scanned commit range.

   Evidence that the collision class is real, not hypothetical regex drift: frozen-base history contains round-46 claims blob `a593613205db4794d7dcdf205d6b9c985a37cbb7`, whose line 15 is `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`; the same history also contains `ca436e848a8ce36496ac6645625e283b03522cbb`, line 15 `gate: P10 DEFECT receipt unreadable` (the latter is the narrowly exempt form). `order_check.py`'s patterns and round-49 common claims-receipt directory are direct evidence of the dependency. Round-49 claims text does not guarantee receipt-output formatting avoids those patterns.

2. **Shared host per-UID process/thread budget couples concurrent scoring.** Round-48 routed spotcheck §42 records the C2 probe's `--nproc=48` stage-check failure at roughly 1100 host threads; the detailed frozen-base report `.ufo/waves/round-48/w1/R48C2ExecProbe.md` §3.2 says `RLIMIT_NPROC` is charged against the real UID's host-wide thread count, reports ~1100–1150 threads, and records `bwrap: Creating new namespace failed: Resource temporarily unavailable` at limits 512/1024, with success at 1536/2048. C1's round-46 counter uses concurrent fixture jobs and launches traced, sandboxed subprocesses (`plans/round46_c1_verify.py` lines 103–115, 494–526; its harness runs `strace -f` and bwrap). C2's probe uses bwrap (`plans/polyglot_c_py_probe.py` line 84) and the round-48 evidence specifically establishes the load-sensitive sandbox failure. Simultaneous C1 work can consume the same UID budget and change C2's probe outcome; this is a runtime/substrate dependency, not a file-pin overlap.

The source documents are local; no external URL was opened (so no URL/access date/quote applies).

## Counter/file boundary check

At the frozen base, `round49_c1_verify.py`, `round49_c2_verify.py`, `plans/mutants49/`, `plans/honest49/`, `plans/sealed49/`, and `corpus/evidence/round49/` are absent, as expected before stage 2/3. The C1 parent counter's explicit digest PINS (round46 C1 lines 123–216) cover round44 C1 counter and C1 fixture populations, not the C2 package/probe. The C2 parent counter explicitly refers to its package/probe/gate/order-check inputs and reimplements V12; no C1 counter import was found. Thus I found no evidence that the staged per-claim file pins themselves overlap.

There is a shared *directory* convention worth preserving: C1 uses `plans/mutants49/c1-mutants.json`, C2 uses `plans/mutants49/plan.json` (claims §65–68, §125–128). They are distinct named manifests; I found no evidence either counter glob-loads that directory. Do not describe this as an observed cross-read.

## One bounded move

Add a **C1 receipt-format guard before committing any blob under `.ufo/waves/round-49/claims/`**: apply the exact frozen `order_check.py` `blob_hits()` predicates to each proposed C1 control/mutant receipt, and reject any hit (or encode quoted output so it cannot be parsed as a standalone matching line). This is a narrow coverage protection: it makes C1 receipt production unable to poison C2 V8, without changing C1's fence predicate, C1 evidence populations, or C2's predicate. Separately, run the resource-sensitive C2 sandbox checks outside the C1 counter's concurrent scoring window; this is an execution discipline, not a counter change.

Risks/limits: the receipt guard must use the frozen parser semantics, not a looser approximation; it must not alter evidence needed to judge C1. The process-budget evidence is from round 48 and host state varies; this scan did not execute either counter or establish current C1/C2 concurrency. File-level pin disjointness is supported by frozen parent-counter inspection, but stage-2/3 files and actual new receipts are not present at the frozen base, so their eventual contents remain unverified.

## Exact commands run

- `git log --oneline -3 9d2900af41e4d1fc6022eff99010436fde6dbd93`; `git rev-parse HEAD`; `git show -s --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93`.
- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane`; `git checkout 9d2900af41e4d1fc6022eff99010436fde6dbd93`; `git rev-parse --show-toplevel`; `git rev-parse HEAD`.
- `ls plans/`; `ls -la` on the two round-46 counters, `order_check.py`, `polyglot_c_py_probe.py`, `fixture_fence.py`; `ls plans/sealed46/`; `ls plans/refusals46/`.
- `head -80 plans/round46_c1_verify.py`; `head -80 plans/round46_c3_verify.py`; `grep -n` for imports, PINS, digest checks, and builder references in both counters.
- Read `plans/round46_c1_verify.py` lines 123–216 and 480–530; read `plans/order_check.py` lines 3–41, 68–210; read `plans/round46_c3_verify.py` documented dependency surface and constants/imports.
- `git log --all --format='%H' -- '.ufo/waves/round-48/claims'`; `git ls-tree -r` of those commits; scanned blobs for `^\s*(gate: )?P10 (DEFECT|ok)\b|^\s*CASE \S+.*\bobserved=`. Repeat for round-46 claims directory. Observed hit: `a593613205db4794d7dcdf205d6b9c985a37cbb` line 15, `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`; exempt hit: `ca436e848a8ce36496ac6645625e283b03522cbb` line 15, `gate: P10 DEFECT receipt unreadable`.
- `git cat-file -e 9d2900af:<path>` for the listed stage-2/3 paths; all round-49 counter/manifests/population/evidence paths tested were absent; `plans/round-48-claims.md` present.
- `grep -n` for `nproc`, `thread`, `RLIMIT`, `1100`, `stage-check`, `bwrap` in frozen `.ufo/waves/round-48/w1/R48C2ExecProbe.md`; `grep -n` for bwrap/temp use in the C2 probe and parent counter.
- Environment spot checks: `ls -la /usr/bin/bwrap /usr/bin/strace /usr/bin/python3`; `/proc/*/task` enumeration returned 8251 task entries while racing process exits, so this is not treated as a stable resource measurement.

## Verdict

**VERDICT: CAUSAL SEPARABILITY IS CONDITIONAL, NOT FULLY ISOLATED.** C1/C2 counter pins and named production files appear disjoint, but C1 receipt bytes in the shared claims scan domain can flip C2 V8, and concurrent counter/probe workload can affect C2's host-budget-sensitive sandbox legs. The receipt-format guard is the bounded, low-cost coverage protection; serialize resource-sensitive scored execution to reduce substrate coupling. No claim admission is made.