# Round 62 proposal — before independent case freeze

Base: c55a3f8868f352280538cf7d786135d34ac6542f. Author: kengaku-shokunin.
Date: 2026-11-02. Status: PROPOSED, not frozen or implemented.

## Claims

C1 / coverage (lowest non-retired axis, score held at operator cap 7): add
repeated-trial metric auditing to the evaluation repertoire. The existing 17/89
TB2 grader metric stays unchanged: this is NOT an eighteenth grader. Before:
no `plans/repeated_trial_metrics.py` at base, and the bounded corpus search finds
pass^k as a prior-art mention rather than an executable estimator. After:
exact finite-panel pass@k/pass^k calculations, missing-outcome bounds and input
refusals agree with an independently frozen case set; executed upstream metric
functions agree on their legitimate complete balanced input domain. A rejected
candidate claim is that these fixture results establish any model's performance.

C2 / calibration (held 10): discharge the three precision findings R61-D1/D2/D3
by source/commit-derived append-only corrections; original historical bytes stay
unchanged. Independently measurable without C1. No scalar uplift. D2 gets a new
source row, never an immutable-cell rewrite. Existing routed-defect machinery,
not an invented round-specific green counter, is the preferred persistence route.

## C1 proposed interface

`python3 plans/repeated_trial_metrics.py --input PATH --k INT`

JSON input exactly `{ "tasks": [{"task_id": "name", "trials":
[{"trial_id": "slot", "status": "pass|fail|error|missing"}]}] }`.
Task ids unique globally; trial ids unique within each task. Nonempty string ids,
nonempty tasks and trial lists. Unknown keys/statuses and duplicate JSON keys
refused. k is a positive integer. Bounds: at most 100 tasks, 1000 slots per task,
1 MiB input, k at most 1000. These are resource bounds, not statistical evidence.

Every planned slot must be represented. The tool cannot discover an entirely
omitted task or slot: caller's input manifest completeness is an assumption.
`fail` is a valid observed negative score; `error` and `missing` are unresolved,
not false successes, observed failures, or silently discarded trials.

For task t, n=planned slots, c=observed passes, u=error+missing.
For k<=n, finite-panel subset proportions are
A(n,c,k)=1-C(n-c,k)/C(n,k) and R(n,c,k)=C(c,k)/C(n,k).
Report exact rational bounds [A(n,c,k),A(n,c+u,k)] and
[R(n,c,k),R(n,c+u,k)]. C(a,k)=0 for 0<=a<k. These are sharp
missing-outcome bounds, NOT confidence intervals. Point status only if u=0.
Macro-average over every supplied task (equal task weighting), never pooled
trial counts or averages after dropping ineligible tasks. Any n<k makes the
whole suite could-not-evaluate, retaining task diagnostics but no suite score.

Proposed deterministic JSON output: `schema`, `k`, `status` (measured|bounded|
could-not-evaluate), `tasks` sorted by task_id, `macro`. Each task: task_id,
planned, completed, passes, failures, errors, missing, status, pass_at_k,
pass_power_k. Bounds objects `{lower:"p/q",upper:"p/q"}` use reduced fractions
including `0/1` and `1/1`. Ineligible metrics/macro are null. Invalid input:
status could-not-evaluate and stable `reason` identifier. Exit0 = valid computed
panel (measured or bounded), exit2 = invalid/ineligible/setup, never model PASS.

No inferential CI or model ranking. An IID future-draw interpretation of these
U-statistics requires independent identically distributed attempts with stable
success probability within each task, a fixed sampling/stopping design, and
correct score semantics; none is established by synthetic panels. Related
attempts/adaptive retries are descriptive finite-panel results only.

## Source pins and exact execution scope

- HumanEval `b9453e8f1865df0a0057a1383767caa400acfbcf`,
  `human_eval/evaluation.py`, sha256
  e926d5e9b8f1ec040096cd5952e8cf79f8dc0b7fb80ba6667ce604ffea0397bc.
  Only AST-extracted `estimate_pass_at_k` may execute, with its numpy/itertools
  dependencies supplied. No execution.py, check_correctness, code completion,
  ThreadPoolExecutor or evaluate_functional_correctness runs.
- tau-bench `59a200c6d575d595120f1cb70fea53cef0632f6b`,
  `tau_bench/run.py`, sha256
  da3a2f3300a973b499a1a5e874357d05fe8c6e327dc394667b4ae665c7924d87.
  Only AST-extracted `display_metrics` may execute, with math.comb, typing
  annotation dependencies, harmless local records and captured print supplied.
  No run, agent_factory, environment, provider imports or model calls.
  This implementation counts global unique trial ids; equivalence is claimed
  only for balanced complete panels with aligned trial ids. Its run exception
  policy sets reward0, unlike our explicit unresolved-outcome analysis.

AST extraction preserves the function bodies and verifies source digests first.
The newly authored exact math is separately compared with independent literal
expected outputs, not with expectations derived by its own code.

## Independent controls requested, not expected answers

Distinct at-least-one vs all-k; k=1 identity; all success/fail; k=n; unequal n
and task-macro vs pooling; error/missing vs observed fail; n<k; invalid schema,
duplicate identifiers and bool-like k; plug-in-power versus without-replacement
combinatorial estimates. Independent reviewer freezes expectations before
implementation. Source missing/tamper and deliberate wrong estimators must not
turn infrastructure refusal into a killed-semantic-control claim.

## Scope amendment before implementation/scoring — 2026-11-02

The preceding proposal remains historical, NOT silently implemented by another
route. `.ufo/waves/round-62/recon/envelope-smoke.txt` records the harmless strict
bwrap smoke failing `NETLINK_ROUTE socket: Operation not permitted` (exit1).
Parent explicitly prohibited removing namespace flags or using an alternate
execution route. No new metric instrument was implemented; no benchmark or
upstream function executed. The original executable capability proposal is
therefore **could-not-evaluate on this host**, not a passed counter.

Revised C1 is **coverage through sourced domain knowledge**, not a capability
acquisition: a new entry on repeated-trial estimands, exact finite-panel
subset proportions, task-macro aggregation and sharp unresolved-outcome bounds,
with manually worked answers to independently frozen cases and independent
source/derivation review. The score stays7, TB2 17/89 stays unchanged. No
executable or upstream-behavior-equivalence claim. Source-code semantics are
READ, not executed. A count of admitted new entries (before0, proposed after1)
is a discoverability measure; the truth of the entry is established by
source/derivation review, not heading counts. The existing paired-uncertainty
entry is extended in a distinct direction; no claim of new mathematics.

The independent reviewer froze a larger oracle before this amendment and before
any author implementation; the author has read neither challenge nor oracle.
A bounded public subset is requested for manual derivations. The oracle stays
sealed until author answers commit. Criteria: correct exact fractions, explicit
macro weighting and unresolved bounds, refusal to infer a sampling CI or model
performance, and honest n<k ineligibility. Negative controls are false
interpretations rejected with a derivation, not executed mutant-kill claims.

C2 remains the causally independent append-only precision correction. Its
read-only Git/blob/source re-derivations continue. Q23's permanent executable
ledger requirement cannot be claimed satisfied without permitted execution;
any such automation debt will remain explicit rather than converted to a pass.
All new artifacts remain candidate/pending until the independent source and
answer review; no self-admission.
