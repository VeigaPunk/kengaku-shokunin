# Practical capability notes: judge calibration and grader evidence

These summaries make reviewed reasoning reusable. They are not new rounds, executable fixes or replacements for the original frozen evidence. The reports preserve the narrower original decisions and defects.

## Round65: know when a corrected score cannot support a decision

For binary human and machine labels, define sensitivity s, specificity c, human-positive rate theta and machine-positive rate r. Total probability gives r=(s+c-1)theta+1-c. When the denominator s+c-1 is zero, machine frequency cannot identify theta. A near-zero denominator magnifies perturbations. More machine-only judgments cannot supply missing calibration information.

Keep known population rates separate from estimated sample rates. An out-of-range plug-in answer is a diagnostic prompt, not permission to clip and certify the model. An incompatible exact population equation and an unstable estimated ratio require different reasoning. Preserve original labels and estimates. A proposed label flip must be defined prospectively and recalibrated, not used to disguise inverse correlation.

Transferring a judge between domains requires evidence about its conditional errors, not just an unchanged version string. Predictive values reverse the conditioning and are not sensitivity or specificity. A calibration sample containing only one human class lacks the other class denominator. Record how labels were selected and adjudicated, including uncertainty from both calibration and target samples. Do not treat a corrected ratio as a binomial success fraction.

A useful limited-budget audit targets the missing premise: absent class, suspected domain shift, selection bias or uncertainty. Hold ranking/release conclusions that the evidence cannot support. The reviewed exercise admitted a qualitative operational triage method, not a new estimator or measured population-rate pass.

## Round66: follow the actual grader predicates

A TCP connection is not proof of an application protocol. Importable client code is not proof of server identity. A caught RPC exception is not a successful application result. Conversely, a permissive handshake does not establish a whole-suite bypass when separate functionality assertions remain. Preserve positive observations while marking the causal links they do not establish.

Inspect the import path, client/schema origin, try/finally boundaries, assertions, timing layers and reward-writing path. Required candidate-generated bindings are ordinary task compliance, not evidence of misconduct. They can still create a provenance question that requires trusted observation. A missing reward artifact is not automatically a zero score or server defect; inspect run identity, termination and the declared outcome policy.

Proposed improvements should strengthen the stated task: trusted verifier imports, status-sensitive semantic positives, distinguishing key/value operations and justified call deadlines. Do not silently add restart persistence when the contract asks only for an in-memory mapping. Proposed patches remain untested until an authorized version-matched execution and independent controls establish their behavior.

The original exercise was manual source analysis with fictional incident records. It adds no executed benchmark coverage and makes no runtime or cheating claim. Existing sandbox restrictions and unresolved checks remain in force.

## Sources and limitations

Lee2026's official PMLR page, the pinned Terminal-Bench2 task and official gRPC documentation are linked in SOURCE-REFERENCES.json. Full papers, source captures and code are excluded. Current documentation explains semantics but cannot prove a historical runtime version. Original attribution/conformance discrepancies remain in the preserved reports rather than being silently amended.
