# FMutPolicyE6 — one bounded E6 mutation probe

Seat: KengakuR27.FMutPolicyE6; axes: novelty → coverage/constructs, calibration. Advisory evidence only; no admission/score judgment.
Private clone: `/tmp/kengaku-r27-FMutPolicyE6`, branch `r27-FMutPolicyE6`.
Exact setup: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutPolicyE6 && git -C /tmp/kengaku-r27-FMutPolicyE6 switch -c r27-FMutPolicyE6 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutPolicyE6 rev-parse HEAD` → exit 0, observed base `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.
Entry reread: WHOLE `.ufo/waves/round-27/drafts/extraction-policy-comparison.md:1–110`, including complete source line; proposed canonical `corpus/knowledge/extraction-policy-comparison.md`. I am not candidate writer KengakuR27. This is not a full Q1–Q15 admission review.
Read `plans/round-27-claims.md:1–190`, including disclosed Amendment 1; relevant build reports ExecPolicyCore, RevSpecE5E6 and ExecPolicyEdgeProbe.

## Finding: E6 first-fence mutant SURVIVES the shipped detector
The sole mutation changes E6's last matched fence to its first, at `plans/parser_policy_compare.py:104`; regex, fallback and every other policy remain unchanged.
Frozen E6 inherits E0's last-match ordering (`plans/round-27-claims.md:37,43,164–166`; candidate `:34,40`). A two-fence witness below confirms a genuine behavioral defect, not equivalent bytes.
Expected detector: `parser_policy_compare.py --selftest`, including `plans/policy_cases.py` through `:462–473,543`; expected rejection of wrong E6 selection. Actual: exit 0 on the mutant, identical to pristine/restored stdout.
Coverage location: E6 PROBES `plans/parser_policy_compare.py:388–392` and seven E6 hand rows `plans/policy_cases.py:58–65` contain no competing first/last matched fences. The existing E6 label-restriction mutant is killed, but that is not detection of this ordering mutant.

Mutant diff command (clone cwd): `git --no-pager diff -- plans/parser_policy_compare.py` → exit 0:
```diff
diff --git i/plans/parser_policy_compare.py w/plans/parser_policy_compare.py
index 54ff51c..61ba0ad 100755
--- i/plans/parser_policy_compare.py
+++ w/plans/parser_policy_compare.py
@@ -101,7 +101,7 @@ def e5_fence_only(raw):
 def e6_any_label_fence(raw):
     blocks = FENCE_ANY.findall(raw)
     if blocks:
-        ok, value = _loads(blocks[-1])
+        ok, value = _loads(blocks[0])
         if ok:
             return value
     return _bare_last(raw)
```

## Same detectors on pristine, mutated and restored bytes
Selftest command, cwd `/tmp/kengaku-r27-FMutPolicyE6`:
`PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FMutPolicyE6/plans/parser_policy_compare.py --selftest`
Observed exit codes: pristine **0**, mutated **0**, restored **0**. All stdout was byte-identical (SHA-256 `8b7625e645f8680e61069b0d8e8a36ff3a0901e7feec7ec78f07b4144cf68bbe`); all stderr empty. Actual relevant lines in each run:
```text
SELFTEST pass policy=E6 probes=3 failed=[]
SELFTEST KILLED E6 mutant=E6-label-restricted by=any-label-fence-wins
SELFTEST pass hand_cases=58 failed=[]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=0
```
`policy_cases.py` is a fixture table, not a separate CLI; all 58 rows were exercised in all three runs. No shipped red output/check-id occurred for this mutant.

Independent bounded witness command, cwd `/tmp/kengaku-r27-FMutPolicyE6/plans` (identical command in all three phases):
~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 -c 'import parser_policy_compare as p; raw = '"'"'```python\n{"v":1}\n```\n```json\n{"v":2}\n```'"'"'; actual = p.e6_any_label_fence(raw); expected = {"v": 2}; print(f"WITNESS E6/two-distinct-fences expected={expected!r} actual={actual!r} matches={actual == expected}"); raise SystemExit(0 if actual == expected else 1)'
~~~
Actual witness outputs (all stderr empty):
```text
pristine exit=0: WITNESS E6/two-distinct-fences expected={'v': 2} actual={'v': 2} matches=True
mutated  exit=1: WITNESS E6/two-distinct-fences expected={'v': 2} actual={'v': 1} matches=False
restored exit=0: WITNESS E6/two-distinct-fences expected={'v': 2} actual={'v': 2} matches=True
```
Red check-id: auxiliary `E6/two-distinct-fences`; it kills the mutant but is NOT part of the shipped selftest. Baseline and restoration are green, so this probe is not inconclusive.

## Exact restoration evidence
In each phase: `sha256sum /tmp/kengaku-r27-FMutPolicyE6/plans/parser_policy_compare.py /tmp/kengaku-r27-FMutPolicyE6/plans/policy_cases.py` → exit 0.
Parser SHA-256 pristine: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d`.
Parser SHA-256 mutated: `389bf59c8f12e8df7058ed192c09b06909f921a4dc7f5120718808aa8f188af6`.
Parser SHA-256 restored: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d` (exact original bytes).
Fixture SHA-256 all three phases: `f3e9b57b80584721437358c7fa1d69146d9cf2588ca483c0bc3f1bf73b47417b`.
No permanent code fix made; only this report written to the lane. No corpus replay/summary, large bracket probes, build/lint/formatters, endpoints, services, delegation or background jobs run.
Installs: none; existing Python/stdlib and Git only.

VERDICT: SURVIVED the shipped --selftest/58-row fixture detector; KILLED by the separately identified bounded two-fence witness. E6 first-vs-last selection is a demonstrated coverage gap, not permission to change the frozen contract. Exact parser bytes restored and both restored detectors green.
