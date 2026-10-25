# FMutPolicyE7 — one bounded E7 mutation probe

Identity: KengakuR27.FMutPolicyE7; not candidate writer KengakuR27. Advisory mutation evidence only, not admission or outside Q15 closure.
Axes: novelty (legacy mapping → coverage/constructs) and calibration; no score change assessed.
Read all 110 draft lines at `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (including the complete source header), intended canonical `corpus/knowledge/extraction-policy-comparison.md`; read `plans/round-27-claims.md` including disclosed Amendment 1.
Read build reports `ExecPolicyCore.md` and `ExecPolicyEdgeProbe.md`; their population/feature evidence is not substituted for this synthetic mutation result.

## Isolation and observed base
Command (exit 0):
`git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutPolicyE7 && git -C /tmp/kengaku-r27-FMutPolicyE7 switch -c r27-FMutPolicyE7 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutPolicyE7 rev-parse HEAD`
Observed HEAD: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.
Only the private clone's E7 dispatch was mutated; the lane receives this report only. No target Git/jj/index mutation.

## Mutant and expected detector
Contract: preregistration `plans/round-27-claims.md:44-45,165-166`; candidate `:41-42`: E7 selects the first successful decode, E8 the last top-level span.
One-line nearest-policy substitution at `plans/parser_policy_compare.py:145`; E8 and all fixtures unchanged.
Observed diff command (exit 0): `git -C /tmp/kengaku-r27-FMutPolicyE7 diff -- plans/parser_policy_compare.py`
```diff
-    ("E7", e7_decode_first),
+    ("E7", e8_decode_last),
```
Expected red: `E7/array-first` (`plans/parser_policy_compare.py:393-398`) and hand case `E7/array-before-object` (`plans/policy_cases.py:69`).
The hand case must return `[1, {"a": 2}]`, not the trailing `{"later": 3}`.

## Same bounded behavioral detector, three byte states
Exact command, cwd `/tmp/kengaku-r27-FMutPolicyE7`, run once per state:
`env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FMutPolicyE7/plans/parser_policy_compare.py --root /tmp/kengaku-r27-FMutPolicyE7 --selftest`
`plans/policy_cases.py` is a fixture table, not a separate CLI; all 58 rows were exercised by `_selftest_policy_cases` (`plans/parser_policy_compare.py:462-473,543`).

Pristine: exit 0. Actual scoped stdout:
```text
SELFTEST pass policy=E7 probes=4 failed=[]
SELFTEST pass hand_cases=58 failed=[]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=0
```
Mutated: exit 1. Actual scoped stdout:
```text
SELFTEST FAIL policy=E7 probes=4 failed=['array-first']
SELFTEST FAIL hand_cases=58 failed=["E7/array-before-object: got {'later': 3}, expected [1, {'a': 2}]"]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=2
```
Restored: exit 0; complete stdout byte-for-byte identical to the pristine run, including all four quoted pristine lines. All non-E7 policy probes passed in all three runs.
The `killed=9` token counts the instrument's built-in seeded mutants; this external substitution is killed by the two actual failing check IDs above, not inferred from that token.

## Exact-byte restoration evidence
Hash command (exit 0), run pristine, mutated and restored:
`sha256sum /tmp/kengaku-r27-FMutPolicyE7/plans/parser_policy_compare.py /tmp/kengaku-r27-FMutPolicyE7/plans/policy_cases.py`
Parser SHA-256 pristine: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d`
Parser SHA-256 mutated: `0d6ff0c77c298f088334406f988805c45455884f777c255233a1a3525acc7067`
Parser SHA-256 restored: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d`
Cases SHA-256 all three states: `f3e9b57b80584721437358c7fa1d69146d9cf2588ca483c0bc3f1bf73b47417b`
Restored the original dispatch line before the restored run. No survivor or inconclusive baseline in this probe.

Limits: one first↔last dispatch substitution only; no population replay, P4/Q15 evaluation, arbitrary-input safety claim, or unmatched-bracket performance probe. No contract change, integration, or shipping action.
Installs: none. Existing interpreter: `python3 --version` → `Python 3.14.8`, exit 0.
VERDICT: KILLED — E7-first→last-top-level mutant produced the expected exit-1 red checks; pristine and exact-byte-restored detector runs returned exit 0.
