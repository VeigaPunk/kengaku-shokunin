
source: S130 — `lanes/kengaku/round6/toolathlon-grader-behaviour-probe.md` — `# Outcome` — generated 2026-10-23 from `https://github.com/hkust-nlp/Toolathlon` at commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`
verified-at: 2026-10-23
recheck: 180d — re-run the probe against the pinned commit (ran 2026-10-23)

# The Toolathlon grader probe, executed (dated amendment)

**This amends** the lane's staged round-5 entry `toolathlon-grader-contract-2026-10-23.md`.
It replaces neither. Round 5's tabulation was **static** — it read what each grader
declares and compares. This entry reports a **behavioural** measurement, and it is
explicit about how far the behavioural claim reaches.

## Method

Two offline steps, no task executed, no workspace touched, no model round-trip:

1. **Discovery.** All 108 graders were parsed with `ast`. A candidate is a
   two-argument function whose body has no file I/O, no `Path`/`os`/`subprocess` call and
   no `pandas`/`numpy` use, and whose name suggests comparison. **38** candidates.
2. **Isolation and call.** Each candidate's own source was extracted with
   `ast.get_source_segment` and `exec`'d in a fresh namespace — so no module-level
   import, side effect or `sys.exit` inside a grader could run. The function was then
   called with seven generic argument pairs (identical string, list, set, dict,
   dict-of-list, tuple, int) and a one-unit-perturbed counterpart of each. A pair counts
   as **discriminating** when the identical call is accepted and the perturbed call is
   rejected.

## Outcome

| Outcome | Count | of 38 |
|---|---|---|
| isolated and callable | 13 | 38 |
| … discriminate (identical accepted, perturbation rejected) | **4** | 38 |
| … callable but **not** discriminating under the generic shapes | 9 | 38 |
| isolated but not callable with any of the seven shapes | 23 | 38 |
| exec failed in isolation | 1 | 38 |

The four that discriminate: `k8s-redis-helm-upgrade.values_equal_strict`,
`live-transactions.validate_log_payload_structure`, `nvidia-stock-analysis._compare_names`
and `student-interview.iso_times_equal`.

## What this establishes, and what it does not

**Does.** For four graders, the comparison function is a genuine predicate on its
arguments — it accepts identical inputs and rejects a one-unit change. That is a
behavioural claim obtained by *executing* the function, and it is re-derivable from the
pinned commit.

**Does not.** Nothing here says a grader is *correct*: a predicate that rejects a
perturbation can still reject the wrong thing. The nine callable-but-uninformative
results are explicitly **artefacts of a wrong input shape** (several functions expect
file paths or domain objects), not evidence of lax graders — the artefact lists them so
the negative result is not misread. `add-bibtex.entries_match` could not be called at
all in isolation, because it calls a sibling helper defined at module scope, so unlike
the four above it is **not self-contained**. And no task was executed: the probe
examines the comparison function, not the end-to-end grader, and says nothing about
whether a verdict matches a human's.

## The structural finding the probe adds

Beyond the four verdicts, the probe measures something the static tabulation could not:
**self-containedness**. Of 38 pure-looking comparison functions, 23 could not be called
with any generic shape and 1 failed to exec — and at least one (`entries_match`) depends
on a sibling module-scope helper. The comparison logic in this corpus is therefore
**distributed across files**, which means a card that claims "the grader compares X"
cannot be verified by reading one file.

ground: Frontier § "Agentic benchmark task-spec audits" — ledger item N16: the round-5 tabulation's static claim replaced by an executed, bounded behavioural measurement, with its negative results stated rather than suppressed.
