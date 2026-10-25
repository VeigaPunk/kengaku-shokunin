# FGateMutant — Q15 working-copy inventory mutation
writer: KengakuR27.FGateMutant (mutation-tester; not candidate writer KengakuR27)
Axes: novelty → canonical coverage/constructs; calibration through bounded failure-capable detector evidence; no score claim.
Observed base: b5f62e5e637b34a1549e3475fc58b4227ed87e5a, branch r27-FGateMutant, private root /tmp/kengaku-r27-FGateMutant.
Clone: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FGateMutant && git -C /tmp/kengaku-r27-FGateMutant switch -c r27-FGateMutant b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FGateMutant rev-parse HEAD` → exit0, observed base above.
Read: whole plans/round-27-claims.md including Amendment1, whole draft .ufo/waves/round-27/drafts/extraction-policy-comparison.md (including complete provenance line), original build/MutGateTiming.md, both retained timing receipts.
Canonical destination considered: corpus/knowledge/extraction-policy-comparison.md; this is a mutation-only advisory report, NOT a qualifying Q10 entry/source reread or outside non-author closure.
Only behavior edit: scratch plans/gate_timing_check.py:799–801 inventory expression; lesson/candidate/report-support/registry commit reads untouched. Recreates old M3's inventory defect, not all old blob/snapshot substitutions.
Contract: corpus/QUALITY.md:123–130; corpus/lessons/round-27.md:90–92; detector assertions plans/gate_timing_check.py:549–587. Old survivor: .ufo/waves/round-27/build/MutGateTiming.md:30–37,51–55.
Same command each phase, cwd /tmp/kengaku-r27-FGateMutant: `env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/kengaku-r27-FGateMutant GIT_AUTHOR_DATE=2026-10-21T00:00:00+00:00 GIT_COMMITTER_DATE=2026-10-21T00:00:00+00:00 python3 /tmp/kengaku-r27-FGateMutant/plans/gate_timing_check.py --selftest`.
Expected: pristine/restored selftest0, early exit1/inventory0, late exit0/inventory1, identical early/late lesson; mutant selftest1 specifically early inventory1 vs expected0, retaining early1/late0 exits.
Observed (selftest exit; early exit/inventory; late exit/inventory): pristine (0;1/0;0/1), mutated (1;1/1;0/1), restored (0;1/0;0/1). No baseline failure, timeout or inconclusive run; exactly three detector invocations.
Hash command before/mutated/restored: `sha256sum /tmp/kengaku-r27-FGateMutant/plans/gate_timing_check.py /tmp/kengaku-r27-FGateMutant/corpus/lessons/round-27.md` (exit0 each); candidate also hashed before/restored (exit0).
Detector before = restored SHA256: 7c8b498ea501a1d4ec67283d51ac0a0d7d57a293e3180a85218dbd2930f284f1.
Detector mutated SHA256: b5b960616459f6e6d70a15a860f0c4e5b24d66fc406ecad865ee6ce9ab528ad0.
Scratch lesson before = mutated = restored SHA256: 62089fee11a817ac56cd1f3e0ac1adfe0758f642452e0b9fb1e0814b6caa41cb.
Draft before = restored SHA256: 4751089d24a16d47219ef792cb7152e540ff50e66db93dd699fe9675d1cc3dee.
Full machine-captured command/env/exit/stdout/stderr retained in /tmp/kengaku-r27-FGateMutant/FGateMutant-evidence/{pristine,mutated,restored}.json; exact patch also retained as mutation.patch. Reproducible command, patch and complete distinct stdout are embedded below, not dependent solely on /tmp retention.

## Exact source mutation (inverse edit restored original bytes)
```diff
--- a/plans/gate_timing_check.py
+++ b/plans/gate_timing_check.py
@@ -799,3 +799,4 @@
-    second_inventory = sorted(path for path in tree_files
-                              if path.endswith(".md")
-                              and is_second_wave(wave_directory(path, round_number)))
+    second_inventory = sorted(
+        path.relative_to(repo).as_posix() for path in repo.rglob("*.md")
+        if is_second_wave(wave_directory(path.relative_to(repo).as_posix(), round_number))
+    )
```
## Pristine and restored stdout (byte-identical); each stderr empty, selftest exit0
```text
[selftest] worktree-only report at early commit:
FAIL line 7 Gate admit: candidate='corpus/knowledge/extraction-policy-comparison.md'
  cell[reason]: Re-read `.ufo/waves/round-27/falsify/TimingSeat.md`.
  cited seat-report paths: '.ufo/waves/round-27/falsify/TimingSeat.md'
  invalid cited second-seat report: .ufo/waves/round-27/falsify/TimingSeat.md (absent from commit tree)
  missing: no .ufo/waves/round-27/falsify/ report exists in commit 7c4e4e3af363397707e8ad78cdc96e2b78c4b35c
  reasons: no cited, existing, returned second-seat report for this round; one or more cited second-seat reports fail identity/return checks
gate_timing_check: commit=7c4e4e3af363397707e8ad78cdc96e2b78c4b35c lesson=corpus/lessons/round-27.md admissions=1 passed=0 failed=1 second-seat-reports=0
exit=1
[selftest] committed report at later commit:
PASS line 7 Gate admit: candidate='corpus/knowledge/extraction-policy-comparison.md'
  cited seat-report paths: '.ufo/waves/round-27/falsify/TimingSeat.md'
  existing returned second-seat report(s): .ufo/waves/round-27/falsify/TimingSeat.md
gate_timing_check: commit=434d6a78b86d5786909de66ad7d9f16211c73911 lesson=corpus/lessons/round-27.md admissions=1 passed=1 failed=0 second-seat-reports=1
exit=0
[selftest] tree inventory matches requested commit (early=0, later=1; lesson unchanged)
[selftest] ALL PASS (five allowed roles; connector/mutation-tester/simplifier and unknown roles rejected; declared writer/author/agentId conflicts red; missing report identity with registered reader green; working-copy inventory leak rejected)
```
## Mutated stdout; selftest exit1
```text
[selftest] worktree-only report at early commit:
FAIL line 7 Gate admit: candidate='corpus/knowledge/extraction-policy-comparison.md'
  cell[reason]: Re-read `.ufo/waves/round-27/falsify/TimingSeat.md`.
  cited seat-report paths: '.ufo/waves/round-27/falsify/TimingSeat.md'
  invalid cited second-seat report: .ufo/waves/round-27/falsify/TimingSeat.md (absent from commit tree)
  missing: Gate does not name a valid second-seat report by path; the commit has 1 second-seat report(s)
  reasons: no cited, existing, returned second-seat report for this round; one or more cited second-seat reports fail identity/return checks
gate_timing_check: commit=7c4e4e3af363397707e8ad78cdc96e2b78c4b35c lesson=corpus/lessons/round-27.md admissions=1 passed=0 failed=1 second-seat-reports=1
exit=1
[selftest] committed report at later commit:
PASS line 7 Gate admit: candidate='corpus/knowledge/extraction-policy-comparison.md'
  cited seat-report paths: '.ufo/waves/round-27/falsify/TimingSeat.md'
  existing returned second-seat report(s): .ufo/waves/round-27/falsify/TimingSeat.md
gate_timing_check: commit=434d6a78b86d5786909de66ad7d9f16211c73911 lesson=corpus/lessons/round-27.md admissions=1 passed=1 failed=0 second-seat-reports=1
exit=0
```
Mutated stderr, complete: `selftest: early commit expected second-seat-reports=0, got 1`.
Restoration comparison from captured records: pristine_restored_exit_stdout_stderr_identical=True; exact source SHA256 also restored. The fixture's unchanged-lesson assertion is enforced at plans/gate_timing_check.py:555–587, not inferred from admission exits alone.
Scoped result: requested inventory-only mutant KILLED specifically by expected0/got1. Admission exits alone remain unchanged; no claim that all commit/identity/content defects are covered or that the deferred candidate is admitted.
Target repo source/Git/index/jj untouched; only this own report written there. All selftest temp Git repositories were under private TMPDIR and cleaned by TemporaryDirectory. No delegation/background jobs, endpoints, builds, linters, formatters or other probe suites.
Installs/updates: none.
VERDICT: KILLED — Q15 bounded inventory detector passed pristine/restored and rejected the working-copy inventory mutant for the required specific reason; exact detector and lesson bytes restored.
