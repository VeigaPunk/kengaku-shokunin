# FCPIndependent — Round 27 CP95 recomputation

Axes: (A) independent CP95 arithmetic; (B) denominator and future/iid claim boundaries; (C) frozen-candidate identity and cited evidence.

Identity: reread the candidate proposed for canonical `corpus/knowledge/extraction-policy-comparison.md`; I am FCPIndependent, **not** candidate writer KengakuR27. Private clone observed at `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`. Frozen blob `18aa324cc8812a63d65e2d8075ff740e417696f7` and lane candidate have matching SHA-256 `4751089d24a16d47219ef792cb7152e540ff50e66db93dd699fe9675d1cc3dee` (both `sha256sum` commands exit 0); candidate bytes match the frozen revision.

## Method and results

Command (stdlib only; no imported `clopper_pearson`): `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FCPIndependent-scratch/cp95_check.py` — exit 0. Exact integer binomial-tail inversion uses p=a/2^66, integer tail sums, exact threshold comparisons against D=2^(66*1964), and adjacent dyadic brackets; float64 `lgamma`/log-sum tails only seed brackets which are validated by exact inequalities and independently cross-check roots. Two-sided alpha=0.05 (tail 0.025). Output:

```text
n=1964 alpha=0.05 two-sided; exact integer tail inversion; S=66, D=2^(66*1964) != 0
k=1964 exact-midpoint=[0.998123514610,1.000000000000]
       round6=[0.998124,1.000000] cand=[0.998124,1.000000] six-decimal-match=True delta=[4.854e-7,0.000e-3]
       independent-float=[0.998123514610,1.000000000000] abs-diff=[7.88e-18,0.00e+1]
k=1947 exact-midpoint=[0.986177282539,0.994949822534]
       round6=[0.986177,0.994950] cand=[0.986177,0.994950] six-decimal-match=True delta=[2.825e-7,1.775e-7]
       independent-float=[0.986177282539,0.994949822534] abs-diff=[1.17e-15,6.96e-16]
k= 952 exact-midpoint=[0.462404625259,0.507091147667]
       round6=[0.462405,0.507091] cand=[0.462405,0.507091] six-decimal-match=True delta=[3.747e-7,1.477e-7]
       independent-float=[0.462404625259,0.507091147667] abs-diff=[2.36e-15,1.38e-15]
k=1938 exact-midpoint=[0.980662636226,0.991334577055]
       round6=[0.980663,0.991335] cand=[0.980663,0.991335] six-decimal-match=True delta=[3.638e-7,4.229e-7]
       independent-float=[0.980662636226,0.991334577055] abs-diff=[6.32e-16,5.63e-16]
ALL_SIX_DECIMAL_MATCH=True MAX|candidate_printed-exact|=4.854e-7 MAX|float-exact|=2.364e-15
```

The four unique intervals match the candidate at all six decimals. Maximum absolute difference from a printed six-decimal endpoint to the exact-inversion midpoint is `4.854e-7`; maximum independent float cross-check difference is `2.364e-15`. Candidate rows are `.../.ufo/waves/round-27/drafts/extraction-policy-comparison.md:61-68`; frozen population n=1964 is pre-registered at `plans/round-27-claims.md:29-31`.

## Boundary checks

- **Zero denominator:** none. Assigned population is n=1964 (>0); recomputation's common denominator D=2^(66*1964) is nonzero (command output). For the k=n=1964 upper endpoint, candidate reports 1.000000 (`...extraction-policy-comparison.md:61,63,67,69`), and the source CP implementation avoids the zero-shape case explicitly: `plans/attrib_calibration.py:148-151` returns for n=0 and uses hi=1.0 when k=n. No zero denominator is evaluated in this edge case.
- **Future/iid guarantee:** none claimed. Candidate calls CP95 nominal/descriptive on a finite, correlated corpus and explicitly says it is not a sampling guarantee for future responses (`...extraction-policy-comparison.md:55-57`); it also disclaims independent future-response precision (`:13-14`) and transfer to future responses (`:107`). This supports no iid/future guarantee, not a future-sampling interpretation.

Residual risk: this verifies the four frozen numeric intervals, zero-denominator edge handling, and stated scope only; it does not assess other Q1–Q15 admission gates or create iid/future-response validity. No tool installed or updated.

VERDICT: Scoped CP95 check PASS; no interval mismatch, zero denominator, or future/iid guarantee defect found. This is a recommendation only, not candidate admission.
## Addendum — full path and identity anchors

The complete finding anchors are `.ufo/waves/round-27/drafts/extraction-policy-comparison.md:61-68` (four interval values), `:61,63,67,69` (k=n upper endpoints), `:55-57` (finite/correlated, no future sampling guarantee), `:13-14` (no independent future-response precision), and `:107` (no future transfer claim). Population n=1964 is `plans/round-27-claims.md:29-31`; zero-edge guards are `plans/attrib_calibration.py:148-151`.

Identity commands and outputs: `git -C /tmp/kengaku-r27-FCPIndependent rev-parse HEAD` → `b5f62e5e637b34a1549e3475fc58b4227ed87e5a` (exit 0); `git -C /tmp/kengaku-r27-FCPIndependent cat-file blob 18aa324cc8812a63d65e2d8075ff740e417696f7 | sha256sum` → `4751089d24a16d47219ef792cb7152e540ff50e66db93dd699fe9675d1cc3dee  -` (exit 0); `sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/drafts/extraction-policy-comparison.md` → the same digest (exit 0). The tracked blob and reread draft therefore have identical bytes.

Findings by severity: **none** in this scoped CP95 check.

Verification gaps: other Q1–Q15 admission gates and any iid/future-response interpretation are outside this recomputation; no such validity is inferred.

Installs: none.

VERDICT: Scoped CP95 check PASS; four unique intervals match at six decimals, with maximum printed-endpoint residual 4.854e-7. No zero denominator or future/iid guarantee defect found. Recommendation only; this is not candidate admission.
