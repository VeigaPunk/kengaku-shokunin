source: S245 — Howard et al., https://arxiv.org/pdf/1810.08240v9, §1 Eq1/P1–P4, pp1–3; S246 — Ramdas et al., https://arxiv.org/html/2210.01948v2, §§1.1/2.2–2.10; original application: corpus/evidence/round70/first-answers.md
verified-at: 2026-11-03, primary reading and frozen manual application; no executable coverage validation
recheck: 180d or before operational use; reopen pinned definitions and independently audit the actual sampling, filtration, stakes, wealth accounting and target

# Anytime-valid evidence for sequential model evaluation

Round63's multiplicity card explicitly excludes online testing. This card adds a
bounded manual audit of sequential evaluation, not a general-purpose inference
library. Source foundations: S245 defines confidence sequences by simultaneous
coverage, rather than a separate guarantee at each time. S246 supplies predictable
bets, nonnegative test wealth, Ville's crossing bound and the distinction between
current wealth, historical crossing and valid evidence combination. Sources do not
validate a particular model evaluator or its task-sampling assumptions.

## Worked audit, derived from the frozen synthetic protocols

Let X_t be binary correctness and F_(t-1) the information available before its
revelation, including task selection and relevant predictors. For the null
E[X_t|F_(t-1)]<=1/2, set M0=1 and multiply by
1+lambda_t(X_t-1/2), with lambda_t predictable and in[0,2]. Both possible factors
are nonnegative. Conditional expectation is
M_(t-1)[1+lambda_t(E[X_t|F_(t-1)]-1/2)]<=M_(t-1).
Thus this bounded-factor construction meets the nonnegative supermartingale
conditions; at alpha=.05 the ever-crossing threshold is20. It does not test every
conceivable meaning of 'model accuracy<=50%'. The null's conditioning is decisive.

With constant lambda1, eight successes give6561/256=25.62890625; a following
failure gives6561/512=12.814453125. The historical-crossing test has rejected,
although current evidence decreases. Neither number is a posterior probability.
A fair response copied twice has expected product(2.25+.25)/2=1.25: marginal
correctness.5 does not make correlated copies valid new bets.

| Evaluator behavior | Manual decision | Concrete falsifying control |
|---|---|---|
| Looks at three independent exact95% fixed-time intervals | Simultaneous coverage is.95^3=.857375, not.95 | Pointwise labeling hides the larger joint miss probability |
| Chooses stakes after seeing the same outcome | Invalid conditional bet | Choose sign matching a fair bit: factor always1.5 |
| Chooses next stake from previous bits under iid equality-null fair bits | Legal predictable adaptation if factors remain nonnegative | Do not reject all adaptation; negative stakes need equality rather than the one-sided null |
| Selects richer of two historical wealth paths30 and2 | Generic.05 guarantee not established | Prechosen equal mixture16 misses20; allocation.025 each requires40 |
| Restarts independent exact.05 protocols until success, at most twice | Overall null risk.0975 | One wealth account or prospective error allocation, not erased losses |
| Reports max-to-date25 with current10 | Anytime p=.04; current reciprocal=.1 | Raw historical maximum is not automatically e-wealth for multiplication |
| Picks easy tasks from a pool whose unweighted mean is.5 | Conditional premise unestablished | Half deterministic successes/half failures, choose successes first |

A predictable change in future valid bets using existing capital differs from
allocating all initial capital retrospectively to a historical winner. Validity
requires conditional validity under the actual information, not simply that each
strategy works under a smaller information set. Likewise, a first-hit stopped
process differs from choosing the peak retrospectively. A fair one-step wealth
2-or0 has max including initial1 of2-or1, with expectation1.5: this original
counterexample explains why the raw maximum cannot be reused as an e-value.

## Decision contract

Record target/contrast, scoring unit, selection scheme, information available,
null model, stake timing, valid range, initial capital, all looks/restarts and
threshold/error budget. Reconstruct current wealth and crossing history separately.
Check sampling assumptions before applying the formula; without-replacement or
adaptive task sampling needs its own valid derivation. Freeze full-strategy mixture
weights before seeing their histories, or justify future predictable reinvestment.

Reject unsupported population superiority, effect-size, transport and causal
training claims even after a valid threshold crossing. Accept the narrower
sequential-null rejection when its premises hold. No crossing is not proof of the
null. A confidence sequence's simultaneous guarantee addresses timing, not a new
deployment population. Source guarantees are repeated-sampling statements.

## Boundaries and falsifiability

The eight original cases and first answers are in corpus/evidence/round70/;
independent reviewer freeze and terminal judgment are under
.ufo/waves/round-70/reviewer/. A wrong decisive calculation, retrospective stake,
unsupported conditional-null substitution or rejection of the legal positive
control defeats the exploratory claim. These examples demonstrate finite manual
judgment, not measured stochastic error control, causal learning gain or runtime
capability. General statistical methodology remains outside province ownership;
operational inference and deployment transport remain frontier. TB2=17/89, cap7.
