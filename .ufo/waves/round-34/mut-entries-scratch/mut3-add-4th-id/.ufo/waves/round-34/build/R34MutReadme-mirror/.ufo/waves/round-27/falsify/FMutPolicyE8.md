# FMutPolicyE8 — one isolated E8 contained-span mutation

Identity: KengakuR27.FMutPolicyE8, not candidate writer KengakuR27; lane-dispatched advisory evidence only.
Axes: novelty → canonical coverage/constructs (novelty held at 7); calibration through bounded detector sensitivity, not score credit.
Read all 110 candidate lines, including the complete source header, and pre-registration including Amendment 1.
Canonical target: `corpus/knowledge/extraction-policy-comparison.md`; tested draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` is not admitted. This is not a Q1–Q15 admission reread.
Read build/ExecPolicyCore.md:14,26–27,49–53 and build/ExecPolicyEdgeProbe.md:33–36 under `.ufo/waves/round-27/`; their scope limits are retained.

## Frozen sandbox and single mutant
Clone command: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutPolicyE8 && git -C /tmp/kengaku-r27-FMutPolicyE8 switch -c r27-FMutPolicyE8 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutPolicyE8 rev-parse HEAD`
Exit 0; observed HEAD `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`, branch `r27-FMutPolicyE8`.
Contract: `plans/round-27-claims.md:45,165–166` and candidate `:42` require skipping starts inside successfully decoded spans.
Only behavior-bearing edit: `plans/parser_policy_compare.py:131`; advance one character rather than to the decoded end, wrongly reconsidering contained/crossing spans. No other policy or fixture was edited.
`git -C /tmp/kengaku-r27-FMutPolicyE8 diff --no-ext-diff -- plans/parser_policy_compare.py` exited 0; exact changed lines:
```diff
-            i = end  # starts inside an already-decoded top-level span are not candidates
+            i += 1  # starts inside an already-decoded top-level span are not candidates
```
Expected detector: production-policy probe `E8/contained-span-skipped` (`plans/parser_policy_compare.py:400–405`); hand cases `E8/contained-span-skipped` and `E8/crossing-span-start-skipped` (`plans/policy_cases.py:75–83`).

## Same bounded detector on pristine, mutated, restored bytes
Cwd for all three runs: `/tmp/kengaku-r27-FMutPolicyE8`. Exact command each time:
`env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FMutPolicyE8/plans/parser_policy_compare.py --root /tmp/kengaku-r27-FMutPolicyE8 --selftest`
Pristine exit 0; mutated exit 1; restored exit 0. `policy_cases.py` is a fixture table, not a separate CLI: all 58 rows were exercised by each run via `plans/parser_policy_compare.py:462–473,543`.
Complete pristine stdout, also identical to restored stdout:
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
Complete mutated stdout is the same except these three corresponding lines:
```text
SELFTEST FAIL policy=E8 probes=4 failed=['contained-span-skipped']
SELFTEST FAIL hand_cases=58 failed=["E8/contained-span-skipped: got {'inner': 1}, expected {'outer': {'inner': 1}}", "E8/crossing-span-start-skipped: got [', ', 1, ']'], expected ['[', ',1,']"]
SELFTEST total policies=9 cases=58 killed=9 failures=3
```
Mutated and restored stderr were captured as `''`. All E0–E7 checks remained green. The actual edited-policy failure, not the unchanged built-in `killed=9` tally, establishes the kill.

## Exact restoration evidence
Command before, during and after: `sha256sum /tmp/kengaku-r27-FMutPolicyE8/plans/parser_policy_compare.py /tmp/kengaku-r27-FMutPolicyE8/plans/policy_cases.py` (each exit 0).
Parser pristine: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d`
Parser mutated: `b9d8ee6eedb7c20cfc23c896404921f81fbfc60db2b64c1217c59514a6b542ef`
Parser restored: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d`
Cases in all three states: `f3e9b57b80584721437358c7fa1d69146d9cf2588ca483c0bc3f1bf73b47417b`.
The exact line was restored before the final detector run; matching SHA-256 and restored exit 0 establish byte restoration and green behavior.

Scope: one E8 nested-span-selection defect, one existing bounded detector in three byte states; no population rescore, independent oracle run, unmatched-bracket cost probe, P4/Q15 claim, or global parser-safety conclusion. No production/source/index/jj edits; only this report and private sandbox operations. No delegation, services, live endpoints or model requests.
Installs: none. Existing `python3 --version` returned `Python 3.14.8` (exit 0); no tool was installed or upgraded.
VERDICT: KILLED — the one-line E8 contained-span-selection mutant produced the expected named failures (exit 1), between pristine and exact-byte-restored green runs (exit 0). Scoped detector sensitivity demonstrated; admission and scoring remain outside this seat.
