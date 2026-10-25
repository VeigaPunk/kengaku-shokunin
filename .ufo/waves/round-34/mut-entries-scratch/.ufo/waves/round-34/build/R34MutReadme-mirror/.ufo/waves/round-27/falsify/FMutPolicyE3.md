# FMutPolicyE3 — E3 first-to-last mutation probe
Seat: KengakuR27.FMutPolicyE3; not candidate writer KengakuR27. Axes: novelty and calibration.
Read plans/round-27-claims.md:1–190, including disclosed Amendment 1:155–190.
Read the WHOLE .ufo/waves/round-27/drafts/extraction-policy-comparison.md:1–110 (including untruncated header); proposed canonical corpus/knowledge/extraction-policy-comparison.md is not admitted. This is an E3-only reread, not Q1–Q15 approval.
Clone command (exit 0): `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutPolicyE3 && git -C /tmp/kengaku-r27-FMutPolicyE3 switch -c r27-FMutPolicyE3 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutPolicyE3 rev-parse HEAD`.
Observed HEAD: b5f62e5e637b34a1549e3475fc58b4227ed87e5a. All commands below use cwd /tmp/kengaku-r27-FMutPolicyE3; all source edits stayed there.
Mutant: only plans/parser_policy_compare.py:80 reverses E3's candidate order, contradicting preregistration:40,162–163 and candidate:37. No other policy or fixture changed; no population/P4/Q15 detector or performance probe was run.
Expected detector: parser_policy_compare.py:373–375 E3/first-candidate-wins; independent hand expectations in policy_cases.py:35,37–39; dispatcher at parser_policy_compare.py:462–472,528–547.
Exact same detector on pristine, mutated, restored bytes: `env PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FMutPolicyE3 --selftest`.
policy_cases.py exists and has no standalone CLI; its 58-case table was exercised through --selftest in all three runs, not merely imported as a script.
Mutation capture command (exit 0): `sha256sum plans/parser_policy_compare.py plans/policy_cases.py && git -C /tmp/kengaku-r27-FMutPolicyE3 diff -- plans/parser_policy_compare.py`.
```diff
diff --git i/plans/parser_policy_compare.py w/plans/parser_policy_compare.py
index 54ff51c..2768dff 100755
--- i/plans/parser_policy_compare.py
+++ w/plans/parser_policy_compare.py
@@ -77,7 +77,7 @@ def e2_bare_last(raw):
 
 
 def e3_bare_first(raw):
-    for cand in gp.BARE_RE.findall(raw):
+    for cand in reversed(gp.BARE_RE.findall(raw)):
         ok, value = _loads(cand)
         if ok:
             return value
```
Pristine/restored hash command (exit 0 each): `sha256sum plans/parser_policy_compare.py plans/policy_cases.py`.
Parser SHA-256 pristine: 7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d.
Parser SHA-256 mutated: 298e6eebb2caa992f137fb9e04ddf754d93a66eb7d46da639ce582d9de4e2c67.
Parser SHA-256 restored by inverse one-line edit: 7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d (exact original bytes).
policy_cases.py SHA-256 in all three states: f3e9b57b80584721437358c7fa1d69146d9cf2588ca483c0bc3f1bf73b47417b.
Pristine exit 0 and restored exit 0 each produced this stdout:
```text
SELFTEST pass policy=E0 probes=5 failed=[]
SELFTEST KILLED E0 mutant=E0-no-bare-fallback by=bad-last-fence-to-bare
SELFTEST pass policy=E1 probes=3 failed=[]
SELFTEST KILLED E1 mutant=E1-swapped-to-last-fence by=first-fence-wins
SELFTEST pass policy=E2 probes=3 failed=[]
SELFTEST KILLED E2 mutant=E2-fence-leak by=fence-agnostic-last
SELFTEST pass policy=E3 probes=2 failed=[]
SELFTEST KILLED E3 mutant=E3-order-reversed by=first-candidate-wins
SELFTEST pass policy=E4 probes=4 failed=[]
SELFTEST KILLED E4 mutant=E4-strip-omitted by=strip-form-feed
SELFTEST pass policy=E5 probes=3 failed=[]
SELFTEST KILLED E5 mutant=E5-fallback-leak by=no-fence-no-fallback
SELFTEST pass policy=E6 probes=3 failed=[]
SELFTEST KILLED E6 mutant=E6-label-restricted by=any-label-fence-wins
SELFTEST pass policy=E7 probes=4 failed=[]
SELFTEST KILLED E7 mutant=E7-nesting-limited by=deep-nesting-outermost
SELFTEST pass policy=E8 probes=4 failed=[]
SELFTEST KILLED E8 mutant=E8-contained-span-reuse by=contained-span-skipped
SELFTEST pass hand_cases=58 failed=[]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=0
```
Mutated exit 1 produced this stdout:
```text
SELFTEST pass policy=E0 probes=5 failed=[]
SELFTEST KILLED E0 mutant=E0-no-bare-fallback by=bad-last-fence-to-bare
SELFTEST pass policy=E1 probes=3 failed=[]
SELFTEST KILLED E1 mutant=E1-swapped-to-last-fence by=first-fence-wins
SELFTEST pass policy=E2 probes=3 failed=[]
SELFTEST KILLED E2 mutant=E2-fence-leak by=fence-agnostic-last
SELFTEST FAIL policy=E3 probes=2 failed=['first-candidate-wins']
SELFTEST KILLED E3 mutant=E3-order-reversed by=first-candidate-wins
SELFTEST pass policy=E4 probes=4 failed=[]
SELFTEST KILLED E4 mutant=E4-strip-omitted by=strip-form-feed
SELFTEST pass policy=E5 probes=3 failed=[]
SELFTEST KILLED E5 mutant=E5-fallback-leak by=no-fence-no-fallback
SELFTEST pass policy=E6 probes=3 failed=[]
SELFTEST KILLED E6 mutant=E6-label-restricted by=any-label-fence-wins
SELFTEST pass policy=E7 probes=4 failed=[]
SELFTEST KILLED E7 mutant=E7-nesting-limited by=deep-nesting-outermost
SELFTEST pass policy=E8 probes=4 failed=[]
SELFTEST KILLED E8 mutant=E8-contained-span-reuse by=contained-span-skipped
SELFTEST FAIL hand_cases=58 failed=["E3/bare-first: got {'v': 2}, expected {'v': 1}", "E3/first-array: got {'v': 3}, expected [1, 2]", "E3/nested-whole-candidate: got {'v': 2}, expected {'outer': {'inner': 1}}", "E3/fenced-candidate-is-not-excluded: got {'v': 2}, expected {'v': 1}"]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=5
```
VERDICT: KILLED — external E3 first-to-last source mutant detected by one policy probe plus four hand cases (not inferred from the unchanged built-in killed=9 counter). Green/red/green exits 0/1/0; exact bytes restored. Scoped detector evidence only; no score/admission or broader correctness claim. Installs: none.
