source: S015 — https://arxiv.org/html/2411.00640 — §1 items 2 and 4, §4.2 “Paired analysis”, §5 “Power analysis”; S016 — https://arxiv.org/html/2410.03492 — Abstract, §5 “Discussion”, §6 “Conclusions”; S017 — https://aclanthology.org/2025.ijcnlp-long.125/ — Abstract; S018 — https://arxiv.org/html/2605.30315 — §1 “Introduction”, §3 “Methodology”, §6.4 “Cluster-aware sensitivity”; S019 — https://arxiv.org/html/2601.20251 — Abstract, §3.2 “Pro-Active Inference”, §4 “Experimental Setup”
verified-at: 2026-10-19
recheck: 2027-01-17 (90d) — re-open S015–S019; verify paired estimands, MDE/resolution and clustering guidance, repeat-run uncertainty, adaptive-selection assumptions, and each paper’s version/publication status

# Paired evaluation uncertainty reporting

## Claim

When models are scored on the same items, estimate their contrast from item-level paired differences. Set a practically relevant minimum detectable effect (MDE), error rate and power target before ranking, then report uncertainty and resolution under the actual item-family clustering and comparison multiplicity. Repeated runs capture a separate source of variation: temperature zero plus a fixed seed does not guarantee deterministic outputs. Adaptive item selection requires an inference method valid for that selection design and its assumptions.

## Evidence

- S015, §1 (item 4): for shared questions, “conducting statistical inference on the question-level paired differences” uses the matched design rather than only aggregate score levels.
- S015, §1 (item 2): “When questions are drawn in related groups, computing clustered standard errors”; S018, §6.4, demonstrates “using the dataset’s 14 subject categories as natural clusters.”
- S015, §5: the MDE is the “mean score difference between two models under the alternative hypothesis”; §1 recommends “using power analysis to determine whether an eval (or a random subsample) is capable of testing a hypothesis of interest.”
- S018, §1: “the assertion that A is meaningfully better than B is a statistical claim about the gap, not the gap itself”; it specifies “the minimum detectable effect (MDE) at the current N” and “the resolution ratio q=N/N⋆.”
- S018, §1/§6.3 “Leaderboard-scale multiplicity”: resolution depends on “how many other adjacent gaps share the table”; the paper evaluates leaderboard pair families under multiplicity correction.
- S016, Abstract: “not all models give deterministic answers, even when setting temperature to zero with a fixed random seed.”
- S017, Abstract: “accounting for both” model- and data-related variation is necessary to avoid “substantially underestimating the overall variability over hypothetical replications.”
- S019, §3.2: “ad-hoc without-replacement variants can fail to yield valid coverage”; adaptive selection therefore needs design-matched inference, not an unmodified IID error bar.

## What this does not establish

- Pairing is valid only when item identities truly match; lower variance is not guaranteed if paired outcomes have non-positive covariance. The methods do not make an under-resolved gap equal to zero or establish a universal model ranking.
- S019’s coverage guarantee is for its stated finite-bank procedure and conditions, not arbitrary adaptive sampling. S016’s experiments do not establish that every API is nondeterministic.
- Falsifier: the paired recommendation does not apply if an audit shows the two systems were not evaluated on the same items; the adaptive-coverage recommendation is contradicted if independent repeated trials of the specified sampling/inference procedure miss its declared coverage beyond sampling uncertainty.

## Attribution

S015 and S016 are canonical earlier methods (S015’s opened version is dated 2024-11; S016 first appeared in 2024, with the opened v2 dated 2025-06), not 2026 current art. S018 and S019 are 2026 arXiv preprints. S017 is peer-reviewed IJCNLP-AACL 2025 proceedings. The distinctions matter: preprint results and canonical methods are not proceedings-level replication of the newer 2026 claims.

## Extends

Extends the README “Statistical reporting” coverage row and the lane’s existing paired work rather than repeating its results: r8 uses problem-level paired contrasts; r11 preregisters a same-problem contrast and MDE; r12 tests an ordered within-problem ladder across task families. `bench-arena-round7-noise-n25.md` documents lag-1 dependence, so the shared-item recipe does not license IID treatment of correlated draws. These external methods add reusable uncertainty, clustering, multiplicity and adaptive-selection reporting; they do not enlarge the local effect claims.

## How kengaku applies it

| Situation | Do | Don’t |
|---|---|---|
| Shared-item ranking | Report the per-item paired difference, interval, item count, and pre-set MDE/power target | Rank by raw score difference or a p-value alone |
| Related tasks | Cluster/resample by the real task family or subject grouping; retain matched outcomes within each item | Treat correlated family members as IID rows |
| Multiple comparisons | State the comparison family and multiplicity rule; report resolution against the target MDE | Select a favorable pair after inspecting an uncorrected leaderboard |
| Repeated runs | Record model/API/version/settings and repeats; quantify run-level prediction uncertainty even at temperature 0 with seed pinned | Claim determinism from temperature-0+seed settings |
| Adaptive item choice | Use an inference procedure with coverage for the actual adaptive selection scheme and its conditions | Reuse a fixed-IID standard error on adaptively selected items |

## Rejected

- **Temperature zero plus a fixed seed makes evaluation deterministic.** Rejected: S016 observed residual nondeterminism under those settings. Flip: repeated, independently launched runs of the exact pinned model/API/hardware/task configuration produce identical per-item outputs; that would support determinism only for that configuration.
- **A nominally significant unadjusted gap proves a resolved ranking.** Rejected: S018 shows resolution depends on paired design, MDE, clustering and multiplicity. Flip: a pre-specified contrast meets the declared power/resolution target and its appropriately adjusted paired interval excludes zero under the actual design.
