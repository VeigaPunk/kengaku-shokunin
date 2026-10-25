# Round 26 — README coverage-map review

Scope: `corpus/README.md` index, coverage map and §Frontier; C1 only.

## Findings / required landing updates

- **Add the C1 knowledge-index row.** In “What’s here” (`corpus/README.md:27-61`), index `knowledge/grader-perturbation-audit.md` (the registered path: `plans/round-26-claims.md:98-99`) with a concise description of the stored-response grader perturbation audit and its committed evidence/source references. Do not describe this as validating grader correctness or human alignment.
- **Add a distinct coverage-map row.** `corpus/README.md:210-229` currently has no row for format-perturbation verdict invariance on stored `raw` responses. Add the measured C1 construct as its own row, linking the new entry, instrument, and its round-26 evidence. Keep the existing rows scoped: line 225 is external judge-calibration material at source-digest depth; line 226 is exact-interval re-verdicts of the lane’s r21-r23 attribution receipts. Neither covers the C1 population/construct.
- **Update the existing Frontier bullet, not a different one.** Under `Judge calibration applied inward` (`corpus/README.md:253-255`), append a new `Partly discharged round 26` sub-bullet after the round-25 correction. Limit it to what C1 measures: grader verdict invariance/sensitivity under its registered perturbations of stored responses from r8/r9/r11/r12. Preserve the residual frontier: C1 does not provide S011 sensitivity/specificity calibration against human labels, and it does not audit `attrib_probe.py`’s r21-r23 receipts. Do not mark the whole bullet closed.
- **Keep inventory indexes in parity with what actually lands.** If the same landing includes them, add the round-26 lesson row in the lesson index (`:82-93`), round-26 evidence row (`:163-168`), and `plans/grader_perturb.py` / `plans/fixtures/r26/` rows in the plans index (`:170-189`). These are discoverability updates, separate from the coverage-map claim.

## Uncovered-ground check

The gap is genuine at the scope C1 registers: README lines 225-226 document related but different coverage, while line 254 explicitly leaves `grader.py` outputs and an S010-style perturbation audit on the frontier. The pre-registration defines C1 as verdict behavior under perturbations of stored response bytes (`plans/round-26-claims.md:37-44, 81-99`). Its round-start receipt records four existing search hits and confirms the new instrument was absent at base (`corpus/evidence/round26-calibration/round-start.txt:8-12`); that hit count alone is not semantic proof. Existing replay claims at README `:194-208` are reproducibility checks, not measurements of response-format invariance.

## State and gaps

- `git status --short -- corpus/README.md` and `git diff -- corpus/README.md` returned no output. The planned knowledge entry and `plans/grader_perturb.py` are absent; `round26-calibration/` currently contains only `round-start.txt`. Thus there is no landed C1 README diff or result to verify yet.
- LSP availability check: `read xd://lsp` returned “No such tool”; no LSP status/references/definition/diagnostics are available in this environment. This is a documentation-only review; no text-search result is used as code-semantic proof.
- Residual risk: add the row and round-26 partial-discharge note only after the entry, evidence and its admit gate have landed; use observed results and source IDs rather than claiming the pre-registered prediction as an outcome.

Installs: none.
VERDICT: The C1 ground is genuinely uncovered; require a separate index and coverage row plus a narrowly scoped round-26 partial-discharge note under “Judge calibration applied inward”; no landed C1 README change exists to review.