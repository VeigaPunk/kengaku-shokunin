# CritIidCluster — statistical validity of C1 interval verdicts (round 25)

Scope attacked: iid assumption behind Clopper–Pearson, one-vs-rest multiclass
specificity, Rogan–Gladen bound mechanics, n=17 power ask, family-wise coverage.

## F1 — STRONGEST COUNTEREXAMPLE: n counts re-sends, not independent draws.

Every authoritative block's `n` is repeated requests of 1–3 identical prompt
bodies; the outcome is a deterministic function of (body, cascade weather), so
intra-cluster correlation is unidentifiable and consistent with rho=1:
- `corpus/evidence/attrib-r22-legs.log:312-345` n=20 = 10x force-hyper (FORCE2,
  `plans/attrib_probe.py:93-94`) + 10x force-opencode-go (FORCE3, :102-103);
  every chain is the same `1/alibaba FAIL 400 -> 2/hyper OK` route.
- `corpus/evidence/attrib-r23-stream.log:268-303` n=30 = 3 bodies
  (24 inspection + 3 marker + 3 hint).
- `corpus/evidence/attrib-r21-impl-ds-trials.log:268-312` n=20, one body
  (COUNT_PROMPT `plans/attrib_probe.py:59`); `attrib-r21-impl-glm-trials.log:142-188`
  n=22, two bodies (std_body :62, err_body :73).
- `grep -c "| NO |" corpus/evidence/attrib-r2[123]-*.log` = 0 in all 9 files:
  zero within-cluster disagreement — nothing in the receipts refutes rho=1.
Under cluster counting m<=3, CP lower for k=m=n<=3 is <=0.29 — every iid-PASS
flips to INDETERMINATE/FAIL. S015 (`corpus/SOURCES.md:37`: "clustered standard
errors ... before running an eval") treats the repeated question — here the
prompt body — as the cluster unit. Receipts themselves concede regime limits:
`attrib-r22-legs.log:347` and `attrib-r23-stream.log:~240` HONEST LIMIT lines
(forced/self-selected coverage, not natural route weather).

## F2 — one-vs-rest specificity is a derived, coupled metric.

No receipt stores specificity (TARGET rows are recall-only, e.g.
`attrib-r22-legs.log:344`; no `SPECIFIC` line exists in any log). C1 invents it.
For K legs, one misclassification decrements its true leg's recall and enters
every other leg's specificity denominator as a correct rejection — estimates
share rows, so each CP interval is *marginal* 95%, never simultaneous. Pooled
one-vs-rest specificity also hides the dominant confusion pair (alibaba->hyper
vs hyper->alibaba collapse into one bin).

## F3 — RG bound: union logic survives; pole edge is a real defect.

`(q+sp-1)/(se+sp-1)` over se in [se_L,1], sp in [sp_L,1]: two 97.5% one-sided
CP lowers give >=95% joint rectangle coverage under ANY dependence (union bound
needs no independence), so "conservative, not Bonferroni-exact"
(`plans/round-25-claims.md:40`) is correct — Bonferroni is unnecessary, not
missing. Verified numerically: whenever the pole line se+sp=1 enters the
rectangle, corner-clipped values already span [0,1]. BUT the corner
`se_lo+sp_lo==1` is a raw division-by-zero, and `se_lo+sp_lo<1` is reachable in
P1 (CP lower for k=n=5 is 0.478; stream-marker/marker legs have n=3 -> 0.293).
The unidentified region must be an explicit contract case, not corner luck.

## F4 — power ask uses the wrong n.

`plans/round-25-claims.md:43-45`: zero-error lower = 0.025^(1/n) needs n>=17
*independent* trials. Effective n = m distinct bodies <= 3 for every P1 block;
n=20-30 on 2-3 bodies meets the letter of the ask while carrying the
inferential weight of n<=3. "Tighten, never loosen" permits requiring the
instrument to print `bodies=<m>` and flag PASS where m is small.

## F5 — dedup necessary, not sufficient.

Cross-file identical tables caught (`attrib-r22-opencode-trials.log:204` ==
`attrib-r22-legs.log:312`, same 20 trials) — dedup fires. But same-file
re-scored blocks 9 s apart (`attrib-r22-legs.log:260` vs :312) and the
`attrib-r22-legs-hyper.log` session sharing frozen_utc 11:49:01Z
(legs.log:8/hyper.log:8) cluster on bodies+session even after dedup.

## F6 — estimand + label drift.

Pooled accuracy is a mixture over regime mixes that differ per file (GT dists
{alibaba:20}, {devin:9,zai:13}, {hyper:10,alibaba:10}, {hyper:24,alibaba:6});
report per-block, never pooled. Stored `n=0 -> FAIL` (attrib-r22-legs.log:293,
attrib-r23-stream.log:239) maps to UNTESTED under claims:36 — the entry must
name the label migration or re-verdicts look contradictory.

## Caveats the knowledge entry MUST carry

C-a Intervals are iid-conditional on re-running the same bodies; they index
observation noise, not body/cascade sampling uncertainty (cite S015).
C-b `bodies=m` printed per estimate; PASS is iid-fragile for small m.
C-c Marginal, not simultaneous coverage; specificity is one-vs-rest coupled.
C-d RG bound = >=95% union bound; returns [0,1] (unidentified) when
se_lo+sp_lo<=1; rg_bound must guard d==0.
C-e Forced/self-selected coverage only (receipts' own HONEST LIMITs).
C-f UNTESTED replaces stored n=0 FAIL — label migration, not contradiction.

## Smallest safe correction

1. `rg_bound` contract: return (0.0,1.0) when se_lo+sp_lo<=1 and guard the
   exact-pole corner (d==0); state it in the claims' leg-share line.
2. `--summary/--json` prints `bodies=<m>` per block + a cluster note; verdict
   rule unchanged but PASS rows carry `iid-fragile` when m<17.
3. Knowledge entry carries C-a..C-f verbatim.
(A stricter variant — verdict under n_eff=m, making every P1 block
INDETERMINATE and the novelty +1 unreachable — is a tradeoff for the canonical
judge, not this critic's call.)

## Falsifiable condition

The clustering caveat is falsified if any authoritative block shows within-body
outcome heterogeneity: `grep "| NO |"` inside a body-class cluster that also
contains `YES` rows. Current count is 0 across all 9 receipts — caveat stands.

VERDICT: C1's intervals are mechanically correct but iid-fragile — every PASS
rests on <=3 effective samples; fixable via bodies=m reporting + rg_bound pole
guard + 6 mandatory caveats, not a claim-killer.

Installs: none.
