# R48C2PosControl — positive package/control execution attack

**Axes named:** coverage (C2). **VERDICT: bounded pass for the narrow “no probe execution” attack; provenance/order gap remains.**

## Counterexample and evidence

At the frozen stage-1 tree `a543d92083557dd9b33ee674e9b99b03411f80af`, a positive C2 package cannot pass the inherited full counter without a full probe execution at scoring: `round46_c3_verify.py::v2` invokes `pkg_gate.py package --rerun --require-clean-tree`; gate P10 runs the probe and requires stdout byte-equal to the receipt. V5 separately runs only `--dry`. I did not execute the full counter, P10, or any scored probe. The permitted stage-check command below succeeded.

The named echo control (dry table copied verbatim as receipt) is rejected by V4’s receipt grammar/summary checks: dry rows lack `observed=` and the dry summary does not match the receipt summary regex. The round-48 freeze additionally requires controls to run the gate with P10 disabled, so verify the counter preserves the non-P10 gate checks while making the echo control fail; do not treat control P10 as evidence of a fresh run.

**Strongest remaining counterexample:** a receipt-shaped echo can be synthesized from the dry table without executing the probe: set each `observed=` to `predicted=`, supply the expected receipt summary, and retain case IDs/tests/violations. The frozen round-46 receipt itself has `mismatches=0`, so its observed values equal predictions. V4’s comparisons and V7/V9/V10 are content/consistency checks; they do not establish execution provenance. If such a transformed receipt is used with P10 disabled and the stage-2 counter does not bind/validate its receipt digest independently, those legs can accept internally consistent bytes. The **exact named** verbatim echo still fails V4; this is a counterexample to broader “receipt provenance” assurance, not evidence that the frozen named control passes. For the positive scored package, P10’s independent fresh execution byte-comparison prevents this transformation from passing unless it matches actual probe output.

The existing `plans/order_check.py` is not a process-execution receipt. It scans committed claims blobs for P10/case lines and requires a claims freeze before receipt introduction. Stage-1 C2 says `plans/order_check.py` pins each control’s ordering receipt, but the inherited implementation does not cryptographically bind a process log to a measured revision. Its source describes the check as “a frozen probe must not run before its receipt is committed.” Therefore the counter can verify fresh execution at scored P10, but cannot establish who generated the committed receipt or that every recorded observation was first produced only after stage 2. A prior receipt already exists in the base: git history records its add commit as `8d7f74ce63c25ad200c69fe0d90158cc7099def6` (2026-10-27 02:33:05 -0300), before stage-1 freeze. Stage 2 must create a new post-freeze receipt/ordering evidence and must not represent the inherited receipt’s history as a new first run.

## Frozen identity discrepancy

The claims prose calls the probe hash `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d` and says it was integrated verbatim. That is the wave artifact hash, not the frozen `plans/polyglot_c_py_probe.py` hash. At the frozen tree the latter hashes to `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`, which is also the inherited counter’s `PROBE_SHA256`. `cmp` found differing bytes; code-only comparison showed meaningful differences including `prlimit`/resource limits and timeout/capped-output handling. The allowed `--dry` stage-check of the committed probe did match the frozen dry table. Do not stage-2-pin the artifact hash as the executable probe identity; reconcile the claim’s provenance description or explicitly pin the actual committed bytes without changing frozen predicates.

## Smallest safe correction

1. Keep the full positive scoring leg P10 enabled and byte-compared to the receipt; controls must run P10-disabled, with control results visibly distinct from the positive scored result.
2. Make the echo control fail for a semantic receipt-vs-independent-digest reason, not just verbatim-format mismatch: freeze an independent receipt digest outside the mutable package under test (or an equivalent counter-owned pin), and require the control gate to consume that pin while P10 remains disabled. Include a receipt-shaped echo as an adversarial control if the contract intends to claim provenance resistance.
3. Stage-2 ordering evidence must bind the post-stage-2 measured revision and full-run result, not infer execution from text presence. Reconcile the frozen probe hash prose with the actual committed probe hash; do not run any full probe before stage 2.

## Commands and observations

All commands below ran in the scratch clone at `a543d92083557dd9b33ee674e9b99b03411f80af`; clone top-level was `/fast/scratch/hyaku/kengaku-r48/R48C2PosControl/lane`.

- `git log --oneline -5` → top entries `bf783c1 ...`, `453ddfd ...`, `a543d92 ...`, `0f77f9b ...`; frozen commit exists.
- `sha256sum plans/polyglot_c_py_probe.py` → `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`.
- `sha256sum .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py` → `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d`.
- `cmp plans/polyglot_c_py_probe.py .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py` → files differ (first difference line 20).
- `timeout 120 python3 plans/polyglot_c_py_probe.py --lane . --dry` → exit 0; `cmp` to `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` → `DRY BYTE-EQUAL`.
- `git log --reverse --diff-filter=A --format='%H %ci %s' -- corpus/evidence/round46/polyglot-c-py-probe.txt` → `8d7f74ce63c25ad200c69fe0d90158cc7099def6 2026-10-27 02:33:05 -0300 round-46: C3 first recorded probe run (polyglot-c-py, 18 cases, mismatches=0) + receipt digest in spec`.
- Read-only source inspection: `round46_c3_verify.py` V2 uses gate `--rerun`; V4 checks case IDs/summary/mismatch consistency; V5 runs `--dry`; `pkg_gate.py::c_rerun` runs the configured probe and compares `r.stdout != want`; `order_check.py` scans committed claim blobs for gate-P10/case lines.

## Source provenance (opened 2026-10-27)

- Local frozen claims: `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md`; quote: “the first full probe run follows the stage-2 commit”.
- Local prior spot-check: `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md`; quote: “V7 lacks violating cases for `both-print` and `toolchain`”.
- Local inherited counter: `file:///fast/scratch/hyaku/kengaku-r48/R48C2PosControl/lane/plans/round46_c3_verify.py`; quote: “V2 runs the gate WITH `--rerun`”.
- Local gate: `file:///fast/scratch/hyaku/kengaku-r48/R48C2PosControl/lane/plans/pkg_gate.py`; quote: “if r.stdout != want”.
- Local order gate: `file:///fast/scratch/hyaku/kengaku-r48/R48C2PosControl/lane/plans/order_check.py`; quote: “a frozen probe must not run before its receipt is committed.”
- Local committed receipt: `file:///fast/scratch/hyaku/kengaku-r48/R48C2PosControl/lane/corpus/evidence/round46/polyglot-c-py-probe.txt`; quote: “cases=18 observed_pass=7 observed_fail=11 mismatches=0”.
- Local dry table: `file:///fast/scratch/hyaku/kengaku-r48/R48C2PosControl/lane/corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`; quote: “TAG both-print instruction.md:7”.
- Local probe: `file:///fast/scratch/hyaku/kengaku-r48/R48C2PosControl/lane/plans/polyglot_c_py_probe.py`; quote: “if a.p.dry:”.
- Local wave artifact: `file:///fast/scratch/hyaku/kengaku-r48/R48C2PosControl/lane/.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py`; quote: “LIMITS = (”.

## Limits

No round-48 counter, stage-2 commit, receipt-shaped echo control, or post-stage-2 ordering receipt existed in the frozen tree. No full probe or scored counter/probe run was performed. Therefore this is a design attack based on the inherited code and frozen contract, not an R48 C2 admission verdict. No C1 judgment.