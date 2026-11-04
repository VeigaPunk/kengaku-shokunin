# SiblingConnectorR73 — adjacency scan

## Axes and evidence

Coverage (R73-C1), calibration (R73-C2). Frozen claims read in full before shell commands. Evidence: `corpus/evidence/round73/w1/sibling-overlap.md`.

The evidence provides absolute paths, source-line references, differences from kengaku and explicit borrow verdicts for tabi, kama, kotoba, mori, tsukuroi, tameshi, kotodama, kasegi, souji and protocol instruments. All four requested categories are covered:

- Actual tabi `scripts/check-gate-registry.mjs` located and read, including its evaluator and eight-field checks.
- Tree-derived registry universes found in tabi, kama, kotoba, mori and tsukuroi; distinguished from registry-derived and document-advertised sets.
- Actual kama round-50 `/proc/{pid}/environ` reader located at `tools/round50-replay-bind-audit.py:273` and read; no live process environment inspected.
- Kotoba/mori declared-field checks compared with C2; protocol closure-check and root-ledgers distinguished from eight-field registry audits.

## One bounded proposed move

Borrow mori's population-digest technique **only as supplementary landing evidence**: retain C1's sorted advertised paths with source-document provenance and C2's ordered row-name/entry-script pairs, each with its own digest, derived from the same landing snapshot. No new predicate, population, script, counting rule, target or kill rule.

Calibration benefit: equal cardinalities cannot hide substituted identities. Coverage is unchanged. Runtime remains static/read-only. Risks: moving-snapshot receipts, deduplicating away second rows, or digest-only evidence without inspectable manifests. Independent reproduction is proposed verification, not a check this seat ran.

## Explicit contradictions

- Tabi's latest-row-wins conflicts with C2's every-row/duplicate rejection; do not import it.
- Tree-derived, advertised-document and registry-derived universes are not equivalent.
- Kengaku's inspected implementation reads filesystem bytes despite the C2 docstring's committed-bytes wording; landing snapshot identity must be established separately.
- Active-handler proof, declaration text and actual runtime replay are different evidence surfaces.

## Commands, outputs and limits

Source/discovery batches returned exit 0; source facts are grounded in the opened lines in the evidence file. No sibling instrument, selftest or mutant battery was executed. No R73 claim verdict or landing commit is asserted.

An incidental legacy control pipeline printed `ADVERTISED total=113`, `MISSING 0`, `PREDICATE R73-C1 fail`, then `rc=0`; that rc belonged to `head`, not the counter. The evidence preserves the exact command and explicitly invalidates the rc as a counter measurement. No separate stderr was retained; no conclusion relies on that moving-tree control.

No implementation edits, code copies, tool installs, git mutations, external fetches or sibling writes. Only this report and the assigned overlap evidence were written in the lane. Empty seat scratch removed by `rmdir -- /fast/scratch/hyaku/kengaku-r73/SiblingConnectorR73`, exit 0; no temporary artifacts remain from this seat.

## Handoff

Report out; never absorb sibling ownership or general-method novelty. L1 retains frozen claim evaluation and any supplementary receipt decision. The proposed move is not implemented, admitted or shipped.

Report: .ufo/waves/round-73/w1/SiblingConnectorR73.md
