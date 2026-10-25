# FMutPolicyE1 — one bounded E1 mutation probe

Identity: KengakuR27.FMutPolicyE1, not candidate writer KengakuR27; lane-dispatched advisory evidence, not outside admission closure.
Axes: novelty (legacy mapping → canonical coverage/constructs) and calibration; no axis rescore claimed.
Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; all commands below used the private clone as cwd.
Clone command: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutPolicyE1 && git -C /tmp/kengaku-r27-FMutPolicyE1 switch -c r27-FMutPolicyE1 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutPolicyE1 rev-parse HEAD` → exit 0.
Observed base: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`; branch `r27-FMutPolicyE1`.

Read `plans/round-27-claims.md:1-190`, including Amendment 1, and the WHOLE 110-line draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (including untruncated source header).
Entry reread explicitly concerns proposed canonical `corpus/knowledge/extraction-policy-comparison.md`; this report is only its scoped E1 mutation evidence.
Draft SHA-256 in both lane and frozen clone: `4751089d24a16d47219ef792cb7152e540ff50e66db93dd699fe9675d1cc3dee` (`sha256sum` → exit 0).
Read build `ExecPolicyCore.md`, `ExecPolicyEdgeProbe.md`, and `ExecStateCheckV4.md`; their reported findings were not substituted for this probe's execution.

## Mutant and expected detector
Contract: `plans/round-27-claims.md:38,160-161`; draft entry:35,44. E1 uses the first matched fence; failed decoding falls back to whole-response bare-last.
Smallest behavior-bearing mutation: only `plans/parser_policy_compare.py:69`, first → last fence. All other policies, fixtures and detector expectations unchanged.
Observed `git diff -- plans/parser_policy_compare.py` → exit 0 (excerpt):
```diff
@@ -66,7 +66,7 @@ def e0_lane(raw):
 def e1_first_fence(raw):
     blocks = gp.FENCED_RE.findall(raw)
     if blocks:
-        ok, value = _loads(blocks[0])
+        ok, value = _loads(blocks[-1])
         if ok:
             return value
     return _bare_last(raw)
```
Expected detector: the same `--selftest` must turn red at E1 ordering/fallback probes (`plans/parser_policy_compare.py:364-365`) and hand-expected cases (`plans/policy_cases.py:18-19`).
`plans/policy_cases.py` is a fixture table, not a separate CLI; `--selftest` exercises all 58 rows via `plans/parser_policy_compare.py:462-473,543`.

## Exact command and actual outputs
Same command, run once on pristine, mutated and restored bytes (no population summary requested):
`env TMPDIR=/tmp/kengaku-r27-FMutPolicyE1 PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FMutPolicyE1 --selftest`
Pristine → exit 0; relevant stdout:
```text
SELFTEST pass policy=E1 probes=3 failed=[]
SELFTEST pass hand_cases=58 failed=[]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=0
```
Mutated → exit 1; relevant stdout/check IDs:
```text
SELFTEST FAIL policy=E1 probes=3 failed=['first-fence-wins', 'bad-first-fence-to-bare']
SELFTEST KILLED E1 mutant=E1-swapped-to-last-fence by=first-fence-wins
SELFTEST FAIL hand_cases=58 failed=["E1/first-matched-fence: got {'v': 2}, expected {'v': 1}", "E1/bad-first-does-not-retry-scalar-fence: got 'later', expected None"]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=4
```
Restored → exit 0; stdout was identical to pristine, including the four lines above. Every other E-policy probe line remained `pass` in all three runs.
Calibration: `killed=9` counts the instrument's internal seeded mutants; the actual source mutation was detected by exit 1 and the four explicit E1 assertion failures, not by that tally alone.

## Exact-byte restoration
Restored only line 69 to `ok, value = _loads(blocks[0])` before the restored detector run.
Command in each phase: `sha256sum /tmp/kengaku-r27-FMutPolicyE1/plans/parser_policy_compare.py /tmp/kengaku-r27-FMutPolicyE1/plans/policy_cases.py` → exit 0.
Parser pristine SHA-256: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d`.
Parser mutated SHA-256: `e93365fe8009be641862f19482809562b17ff670315196286ba90f23e1f94505`.
Parser restored SHA-256: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d` (exact pristine match).
Fixture SHA-256 in all three phases: `f3e9b57b80584721437358c7fa1d69146d9cf2588ca483c0bc3f1bf73b47417b`.
Only sandbox E1 was mutated and restored; the sole lane write is this report. No live Git/jj/index edits, subagents, background jobs, builds, linters, formatters, large-bracket probes, or endpoint/model calls.
Limits: one first↔last mutant only; no population/oracle recomputation, P4 validation, Q15 authority audit, global correctness claim, or admission decision.
Installs/updates: none; existing Git and Python only.

VERDICT: KILLED — pristine exit 0 → E1 source mutant exit 1 (two probe IDs plus two hand-case IDs) → exact-byte restoration exit 0. The assigned E1 detector caught this defect; no survivor from this single probe.
