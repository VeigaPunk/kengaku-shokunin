# FMutPolicyE5 — one bounded E5 ordering mutation

Identity: KengakuR27.FMutPolicyE5; not candidate writer KengakuR27. Axes: novelty and calibration; no score or admission decision.
Scope: challenge only E5 last-matched-fence selection; one mutant, same bounded detector on pristine/mutated/restored bytes.
Read the whole draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md:1–110` (including untruncated source header), proposed canonical `corpus/knowledge/extraction-policy-comparison.md`, and `plans/round-27-claims.md:1–190` including Amendment 1. This is a mutation report, not a qualifying whole-entry admission verdict.
Contract anchors: claims `:42,164–166`; draft `:39,77–78,88–91`; implementation `plans/parser_policy_compare.py:92–98`.
Read build `RevSpecE5E6.md:13–20`, `ExecPolicyCore.md:11–27,49–53`, and `ExecPolicyEdgeProbe.md:19–35` for scope/coverage limitations; their observations were not treated as my executions.

## Isolated setup and expected detector
Exact setup command (exit 0):
```sh
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutPolicyE5 && git -C /tmp/kengaku-r27-FMutPolicyE5 switch -c r27-FMutPolicyE5 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutPolicyE5 rev-parse HEAD
```
Observed branch `r27-FMutPolicyE5`; HEAD `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.
All detector calls used cwd `/tmp/kengaku-r27-FMutPolicyE5` and exactly:
```sh
env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FMutPolicyE5/plans/parser_policy_compare.py --root /tmp/kengaku-r27-FMutPolicyE5 --selftest
```
Baseline command was prefixed by `python3 --version &&`, which returned `Python 3.14.8`.
`plans/policy_cases.py` exists and is a data table, not a separate CLI (`:1–8,84`); the detector executes all 58 rows via `parser_policy_compare.py:462–473,543`.
Expected red: `E5/last-invalid-no-earlier-retry`, `plans/policy_cases.py:53`: valid first fence plus invalid last fence must return None.

## Applied mutant and actual outputs
Smallest behavior-bearing edit: only `plans/parser_policy_compare.py:95`, last→first fence (no fallback added).
Applied diff (description of the edit, not claimed git-diff output):
```diff
-        ok, value = _loads(blocks[-1])
+        ok, value = _loads(blocks[0])
```
Pristine detector: exit 0. Relevant stdout excerpts:
```text
SELFTEST pass policy=E5 probes=3 failed=[]
SELFTEST pass hand_cases=58 failed=[]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=0
```
Mutated detector: exit 1. Relevant stdout excerpts:
```text
SELFTEST pass policy=E5 probes=3 failed=[]
SELFTEST KILLED E5 mutant=E5-fallback-leak by=no-fence-no-fallback
SELFTEST FAIL hand_cases=58 failed=["E5/last-invalid-no-earlier-retry: got {'v': 1}, expected None"]
SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0
SELFTEST total policies=9 cases=58 killed=9 failures=1
```
The built-in `E5-fallback-leak` KILLED line describes its different seeded mutant, not my first-fence mutant. My mutant was killed by the hand-case failure above. The three direct E5 PROBES (`parser_policy_compare.py:383–387`) stayed green; the full detector's hand table supplies this ordering protection. No survivor is claimed.
Restored detector: exit 0; stdout was identical to pristine, including all four excerpted lines and all nine built-in mutant KILLED lines. Restoration changed only line 95 back to `blocks[-1]` before this third execution.

## Byte identity and bounds
SHA-256 outputs from `sha256sum` (each hash command exit 0):
- `plans/parser_policy_compare.py`, pristine: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d`.
- Same file, mutant: `fd0c26bc4932e76b7cc40e9b3e23d97eed9e507d9649d86f19bade4ca20d1810`.
- Same file, restored: `7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d` (exact pristine identity).
- `plans/policy_cases.py`, all three stages: `f3e9b57b80584721437358c7fa1d69146d9cf2588ca483c0bc3f1bf73b47417b` (unchanged).
Initial hash command: `sha256sum /tmp/kengaku-r27-FMutPolicyE5/plans/parser_policy_compare.py /tmp/kengaku-r27-FMutPolicyE5/plans/policy_cases.py /tmp/kengaku-r27-FMutPolicyE5/plans/round-27-claims.md /tmp/kengaku-r27-FMutPolicyE5/.ufo/waves/round-27/drafts/extraction-policy-comparison.md /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-27-claims.md /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/drafts/extraction-policy-comparison.md`.
Mutant/restored hash command: `sha256sum /tmp/kengaku-r27-FMutPolicyE5/plans/parser_policy_compare.py /tmp/kengaku-r27-FMutPolicyE5/plans/policy_cases.py`.
Initial clone/live prereg hashes both `f4094be781f221e06fcd3f0f9121091c9d2ed4cce464aae3e5eceecb632177f7`; draft hashes both `4751089d24a16d47219ef792cb7152e540ff50e66db93dd699fe9675d1cc3dee`.
No summary/population comparison, oracle, P4, Q15, build/lint/formatter, performance probe, live endpoint, or other runtime invoked. Selftest's own bounded pin-rejection branches ran as reported. No lane source/index/Git mutations; lane write is this report only.
Installs: none. Existing Python 3.14.8; stdlib-only probe.
VERDICT: KILLED — the E5 first-for-last fence mutant produced exit 1 specifically at E5/last-invalid-no-earlier-retry, between exit-0 pristine and restored runs; exact parser and fixture bytes restored. This supports only the exercised ordering defect detection, not global parser correctness or admission.
