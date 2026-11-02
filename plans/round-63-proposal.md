# Round63 proposal — fixed-family multiplicity in model comparisons

2026-11-02. Revised baseline 09424fa1fef4635df97b92034fe3196f2f11943f,
canonical round62 parent c78749a565dfd186f10a1d8ac98e19dac2429666.
Read audit/branch-reconciliation-20261102.md in the training root and canonical
round62 report/reviewer. Old cloud62 is supplemental only, not a second round.
Canonical S226/S227 retain their identities. R61 factual repairs are already
landed; no credit for repeating them. Literal Q23 registration remains OPEN.

## One claim C1 — coverage (lowest axis, score7 held)

Before: paired-eval-uncertainty-reporting.md says name the comparison family and
multiplicity rule, but provides neither exact Holm/BH/BY adjusted-p algorithms
nor boundary/step-order examples. Sweep: grep -inE 'holm|bonferroni|multiplicity|BY|BH'
corpus/knowledge/paired-eval-uncertainty-reporting.md and SKILL.md. Existing generic
advice is acknowledged, not misrepresented as an empty statistical corpus.
After: source-grounded new entry and SKILL decision table let a reader calculate
fixed-family adjusted values/rejections and refuse invalid inferential readings.
This is manual knowledge, NOT executable capability, model improvement, new
mathematics, eighteenth TB2 grader, or lifted coverage cap. TB2 stays17/89.

### Frozen assumptions and formulas

Finite complete family of m hypotheses, 1<=m<=6; rational p_i in [0,1], unique
hypothesis IDs, fixed alpha or q in (0,1), family/method/error target fixed before
seeing results. No missing values, API n override, or adaptive stopping claims.
Validity requires super-uniform marginal p-values under each true null: for all
t in [0,1], Pr(p_i<=t)<=t; correcting invalid input p-values does not repair them.
Sort ascending p_(i), preserve labels; reject on adjusted value <= level (inclusive).
Holm adjusted p_(i)=min(1,max_{j<=i}((m-j+1)*p_(j))); equivalently stop at FIRST
p_(i)>alpha/(m-i+1), reject only earlier ranks. FWER=Pr(V>=1); dependence arbitrary.
BH adjusted p_(i)=min(1,min_{j>=i}(m*p_(j)/j)); choose LARGEST rank with
p_(i)<=i*q/m and reject ranks1..k, even if an earlier rank misses its own line.
FDR=E[V/max(R,1)], not a realized FDP bound, posterior probability, or FWER.
BH guarantee only under independence or source's PRDS-on-true-nulls condition;
positive pairwise correlation by itself is not a license for arbitrary tests.
BY uses harmonic H_m=sum_{j=1}^m 1/j and replaces m with m*H_m in BH adjusted
values / q with q/H_m in the threshold. It controls FDR under arbitrary dependence
with valid marginals. Ties receive equal adjusted values; outputs restored to ID
order. Never shrink m to a favorable selected subset. Non-rejection does not
establish equality/equivalence; corrected significance does not establish a
practically important effect or task-population transport.

## Source pins (opened 2026-11-02; read, never executed)

Proposed canonical new IDs S228–S230, unused at baseline:
- S228 R4.5.1 implementation, https://svn.r-project.org/R/tags/R-4-5-1/src/library/stats/R/p.adjust.R
  capture corpus/evidence/round63/sources/p.adjust.R sha256
  f118c13d63412ab45e18191763e3e55e6addd880f5557a908f2f11b5b90e060c.
- S229 R4.5.1 manual source, https://svn.r-project.org/R/tags/R-4-5-1/src/library/stats/man/p.adjust.Rd
  capture corpus/evidence/round63/sources/p.adjust.Rd sha256
  3fb8b4f5620f8b2acf2e400630c4e8fd372b381e948775f1a5419ae1c8d92900.
- S230 Benjamini & Yekutieli (2001), Annals of Statistics29(4):1165–1188,
  DOI10.1214/aos/1013699998; author-hosted full paper
  https://www.math.tau.ac.il/~ybenja/MyPapers/benjamini_yekutieli_ANNSTAT2001.pdf
  capture corpus/evidence/round63/sources/BY2001.pdf sha256
  4bfbec2b1099968fee729852c5d6c3a8123ba6e5748e1e9583a81d5c5ebdef27;
  §1.2 definitions/procedure, Theorems1.2/1.3 pp1168–1169.
R4.6.0 live html was preparation only; no version mixing in algorithm claim.
Failed JSTOR/Euclid stubs and incorrect GitHub tag URL are NOT sources admitted.

## Prospective challenge and falsifiers

Parent-appointed /root/judge_kengaku_round63 independently freezes six arithmetic
cases (m<=6) and four interpretation cases, with hand-derived sealed oracle.
Only public questions released after this proposal commit. Author commits exact
answers with working before oracle release; reviewer compares all ten, preserves
misses. Admission requires all requested arithmetic exact and assumptions/limits
correct, plus independent admit AND reject spot-check and source review. Failure
is reported, never repaired covertly or converted into machine-test evidence.

Prospective bad controls to discriminate: unadjusted singleton selection; Holm
without prefix maximum/first-failure stopping; BH stopping at first failed rank;
BH under arbitrary dependence; FDR as FWER or realized FDP bound; non-rejection
as equivalence; adjusted p as posterior null probability. These are false manual
interpretations, NOT executable mutant kills. Reviewer chooses actual cases; no
author-supplied expected outputs or computed oracle. Metadata shell counts measure
discoverability only, never semantic validity. No benchmark/provider/fetched-code
execution, no bwrap weakening/alternate route. Prior strict envelope NETLINK_ROUTE
failure remains controlling; no retry absent relevant changed environment evidence.

## Maintenance and bounds

Canonical62 provenance omission gets a dated append-only erratum identifying its
historical verification date and prospective recheck; no false current runtime
verification. This is maintenance, not a second axis claim or Q23 durable closure.
Any pending-defect sidecar must say not-run/pending, not pretend canonical ledger
compliance. Preserve old files/rows/failures and supplemental episode unchanged.
Author works only reconciled lane; parent owns exact fleet report landing.
Sequential specialist passes/non-author review follow approved host adaptation;
no eight-agent or promotion claim. Report all axes/trends with bounded evidence.
