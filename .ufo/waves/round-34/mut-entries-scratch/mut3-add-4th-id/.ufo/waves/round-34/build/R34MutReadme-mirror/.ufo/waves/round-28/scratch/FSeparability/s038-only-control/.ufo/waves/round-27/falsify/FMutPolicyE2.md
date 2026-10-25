# FMutPolicyE2 — bounded E2 mutation probe

Seat: KengakuR27.FMutPolicyE2; mutation-tester, not candidate writer KengakuR27; lane-dispatched advisory evidence only.
Axes: novelty (legacy → coverage/constructs) and calibration; measured here only by E2 detector sensitivity and exact restoration, not score movement.
Observed clone HEAD: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.
Clone command (exit 0): `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutPolicyE2 && git -C /tmp/kengaku-r27-FMutPolicyE2 switch -c r27-FMutPolicyE2 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutPolicyE2 rev-parse HEAD`.
Read all `plans/round-27-claims.md`, including Amendment 1, and the whole 110-line draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (including untruncated source metadata).
Proposed canonical candidate: `corpus/knowledge/extraction-policy-comparison.md`; not admitted by this report. This mutation test is not a complete Q10/Q14 source/number reread or outside non-author closure (`corpus/QUALITY.md:111-128,141`).
Read build limitations in `build/ExecPolicyCore.md:49-53`, `ExecPolicyEdgeProbe.md:30-37`, `RevSpecE1E2.md:28-55`, and `ExecStateCheckV4.md:17-30` under `.ufo/waves/round-27/`; their population/P4 numbers were not independently rerun here.

## Mutant and expected detector
Invariant: E2 returns the last parseable non-overlapping BARE_RE candidate from the original raw string, including fences (`plans/round-27-claims.md:39,162-163`; draft:36; `plans/parser_policy_compare.py:48-53,75-76`).
One behavior-bearing edit, E2 only, in the private clone; shared helpers, POLICIES, expected cases and other policies unchanged:
```diff
--- plans/parser_policy_compare.py (pristine)
+++ plans/parser_policy_compare.py (mutant)
@@ -75,2 +75,2 @@
 def e2_bare_last(raw):
-    return _bare_last(raw)
+    return e3_bare_first(raw)
```
This first↔last selection defect should fail E2 `fence-agnostic-last` and `array-candidate` (`parser_policy_compare.py:368-371`) and E2 hand cases (`plans/policy_cases.py:26,28,32`).

## Identical bounded command, three byte states
Cwd for every run: `/tmp/kengaku-r27-FMutPolicyE2`; existing Python 3.14.8.
Command: `PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FMutPolicyE2 --selftest`.
`plans/policy_cases.py` is the expected-value table, not a separate CLI; `_selftest_policy_cases` exercises all 58 rows (`parser_policy_compare.py:462-473,543`).
Pristine actual stdout excerpts; exit 0:
```text
SELFTEST pass policy=E2 probes=3 failed=[]
SELFTEST pass hand_cases=58 failed=[]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=0
```
Mutated actual stdout excerpts; exit 1:
```text
SELFTEST FAIL policy=E2 probes=3 failed=['fence-agnostic-last', 'array-candidate']
SELFTEST SURVIVED E3 mutant=E3-order-reversed
SELFTEST FAIL hand_cases=58 failed=["E2/bare-last-inside-fence: got {'v': 1}, expected {'v': 2}", "E2/array-reference-is-last-candidate: got {'v': 1}, expected [1]", "E2/non-overlapping-array-candidate: got [{'v': 1}], expected {'last': 2}"]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=8 failures=6
```
The E3 SURVIVED line is reported, not hidden: E3's built-in seed references `e2_bare_last` (`parser_policy_compare.py:447`), which this mutation makes equivalent to E3. It is a coupled seed in the deliberately broken build, not survival of the assigned E2 mutant. Direct E2 probes and three hand expectations independently go red.
Restored actual stdout excerpts; exit 0:
```text
SELFTEST pass policy=E2 probes=3 failed=[]
SELFTEST pass hand_cases=58 failed=[]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=0
```
All three stderr streams were empty. Pristine/restored full stdout and stderr equality: True/True.
Full command/stdout/exit transcripts retained in scratch: `/tmp/kengaku-r27-FMutPolicyE2/FMutPolicyE2-{pristine,mutated,restored}.log`; decisive output is embedded above.

## Exact restoration evidence
Command at each byte state: `sha256sum /tmp/kengaku-r27-FMutPolicyE2/plans/parser_policy_compare.py /tmp/kengaku-r27-FMutPolicyE2/plans/policy_cases.py` (each exit 0).
Parser pristine SHA-256: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d`.
Parser mutant SHA-256: `f0d7cf3a66c24a2a6265555e02cfba2edb0cc6a6ae170d8c1ed135275e66e059`.
Parser restored SHA-256: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d`.
Fixture table SHA-256 in all three states: `f3e9b57b80584721437358c7fa1d69146d9cf2588ca483c0bc3f1bf73b47417b`.
Exact original parser bytes restored before the third detector run. No live source/Git/jj/index mutation; only this report written outside the private clone. No delegation, background jobs, live endpoints, build/lint/formatter, population replay, P4/Q15 detector or unmatched-bracket performance probe.
Installs/updates: none; existing Python 3.14.8, stdlib only.
VERDICT: KILLED — the assigned E2 last→first mutant changes the same bounded detector from exit 0 to exit 1 with named E2 policy and hand-case failures; exact-byte restoration returns exit 0. Scoped mutation sensitivity only, not global correctness or admission.
