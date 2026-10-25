# FMutPolicyE4 — bounded E4 strip-omission mutation

Identity: KengakuR27.FMutPolicyE4, not candidate writer KengakuR27. Advisory mutation evidence only; not outside non-author closure or admission.
Axes: C1 legacy novelty → canonical coverage/constructs; calibration of the behavioral detector. No score change or C2/P4 conclusion.
Read the complete frozen draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md:1–110` for proposed canonical `corpus/knowledge/extraction-policy-comparison.md`, plus `plans/round-27-claims.md:1–190`, including Amendment 1.
Scope: one E4 behavior mutation; no performance probes, production edits, model requests, builds, lint, formatters, or other runtime invocation.

## Isolation and observed base
Exact clone command (exit 0):
```sh
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutPolicyE4 && git -C /tmp/kengaku-r27-FMutPolicyE4 switch -c r27-FMutPolicyE4 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutPolicyE4 rev-parse HEAD
```
Observed HEAD: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`; branch `r27-FMutPolicyE4`. All detector cwd/source/root and TMPDIR were inside this private clone. Source anchors below are clone-relative.

## Mutant and expected detector
`plans/parser_policy_compare.py:87–89`: remove only E4's `raw.strip()`, producing whole-output `json.loads(raw)` semantics. This is plausible source-exact drift, but violates the frozen lane contract (`plans/round-27-claims.md:41,167–170`; draft:38,47–50).
Expected detector: built-in `E4/strip-form-feed` at `plans/parser_policy_compare.py:379`, and hand fixture `E4/strip-form-feed` at `plans/policy_cases.py:44`; form-feed-wrapped JSON must parse after strip, whereas the mutant returns None.
Exact diff command (exit 0): `git -C /tmp/kengaku-r27-FMutPolicyE4 diff --no-ext-diff -- plans/parser_policy_compare.py`.
```diff
diff --git i/plans/parser_policy_compare.py w/plans/parser_policy_compare.py
index 54ff51c..61905bb 100755
--- i/plans/parser_policy_compare.py
+++ w/plans/parser_policy_compare.py
@@ -85,7 +85,7 @@ def e3_bare_first(raw):
 
 
 def e4_strict_whole(raw):
-    ok, value = _loads(raw.strip())
+    ok, value = _loads(raw)
     return value if ok else None
 
 
```

## Same bounded detector on pristine, mutated, restored bytes
Exact command, executed three times (cwd `/tmp/kengaku-r27-FMutPolicyE4`):
```sh
env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/kengaku-r27-FMutPolicyE4 python3 /tmp/kengaku-r27-FMutPolicyE4/plans/parser_policy_compare.py --root /tmp/kengaku-r27-FMutPolicyE4 --selftest
```
`plans/policy_cases.py` is a fixture table, not a standalone CLI; its 58 rows ran through `_selftest_policy_cases` (`plans/parser_policy_compare.py:462–473,543`). Actual relevant stdout (stderr empty in all three runs):
```text
PRISTINE exit=0
SELFTEST pass policy=E4 probes=4 failed=[]
SELFTEST pass hand_cases=58 failed=[]
SELFTEST total policies=9 cases=58 killed=9 failures=0
MUTATED exit=1
SELFTEST FAIL policy=E4 probes=4 failed=['strip-form-feed']
SELFTEST FAIL hand_cases=58 failed=["E4/strip-form-feed: got None, expected {'v': 2}"]
SELFTEST total policies=9 cases=58 killed=9 failures=2
RESTORED exit=0
SELFTEST pass policy=E4 probes=4 failed=[]
SELFTEST pass hand_cases=58 failed=[]
SELFTEST total policies=9 cases=58 killed=9 failures=0
```
All three also emitted `SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0`; other policy probes remained green. The built-in seeded-mutant `killed=9` is not the external mutation verdict: the actual patched policy's exit-1 result and two failing assertions kill this one mutant.

## Restoration evidence
Exact hash command before mutation, during mutation and after restoration (each exit 0):
`sha256sum /tmp/kengaku-r27-FMutPolicyE4/plans/parser_policy_compare.py /tmp/kengaku-r27-FMutPolicyE4/plans/policy_cases.py`
- Parser pristine: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d`.
- Parser mutated: `97f143fe986d34fac41bb6f87aa2d7aa18123d9d9303faf6a56c1585304da684`.
- Parser restored: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d` (exact pristine identity).
- Fixture table all three: `f3e9b57b80584721437358c7fa1d69146d9cf2588ca483c0bc3f1bf73b47417b` (unchanged).
Restoration reinserted the original line 88; restored detector returned green. No whole-population summary/oracle, P4, or Q15 authority check was run; no general parser-safety or admission conclusion follows. Build-context limitations read: `build/ExecPolicyCore.md:49–53` and `build/ExecPolicyEdgeProbe.md:33–37` under this wave.

Installs: none. Existing `python3 --version` returned `Python 3.14.8` (exit 0).
VERDICT: KILLED — the E4 strip-omission mutant is detected by both bounded form-feed checks (green 0 → red 1 → restored green 0); exact parser bytes restored. No surviving defect found in this single assigned mutation probe.
