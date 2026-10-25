# SrcS011Reopen: S011 re-open, Lee et al., "How to Correctly Report LLM-as-a-Judge Evaluations" (ICML 2026, PMLR 306:65231-65252)

Seat: KengakuR25.SrcS011Reopen. Round 25, C1 frontier re-open. Report-only; no lane writes. Scratch: /tmp/kengaku-r25-SrcS011Reopen.

## Fetch (sha256, access time)
- HTML https://proceedings.mlr.press/v306/lee26bl.html: 15,551 B, sha256 33a1bcaada76e3af6c2812fb288ef831a798bb62c02c34ff7fa96adb417797ad, accessed 2026-10-21T00:16:15Z (UTC).
- PDF https://raw.githubusercontent.com/mlresearch/v306/main/assets/lee26bl/lee26bl.pdf (URL from HTML `citation_pdf_url`): 3,427,451 B, PDF 1.5, 22 pp, sha256 c1645e31f0f1b6a183ef15ad201b123fb137447897adcea861420f213faa7752, accessed 2026-10-21T00:16:20Z (UTC).
- Rejected: https://proceedings.mlr.press/v306/lee26bl/lee26bl.pdf returned 9,379 B non-PDF; discarded.
- PDF page number = printed page number (footers checked on pp.4, 5, 14). Eqs (4)-(8), (10) and Algorithm 1 verified by rendering pp.4, 5, 14 to PNG (pdftoppm), not text extraction alone.

## Findings
F1. Estimator equals Rogan-Gladen: YES, exactly.
- Eq. (4), §4.1, p.4 (known q): θ̂ = (p̂ + q0 − 1)/(q0 + q1 − 1).
- Eq. (5), §4.2, p.4 (plug-in), verified in crop: θ̂ = (p̂ + q̂0 − 1)/(q̂0 + q̂1 − 1).
- Mapping: q1 = Pr(Ẑ=1|Z=1) = sensitivity; q0 = Pr(Ẑ=0|Z=0) = specificity (eq. (3), §2, p.3); p̂ = observed "correct" rate (eq. (2), p.3). So θ̂ = (p̂ + sp − 1)/(se + sp − 1), the Rogan-Gladen form with q = p̂.
- Paper attributes eq. (5) to Rogan & Gladen (1978) and Lang & Reiczigel (2014), §4.2 p.4. Neither source was opened this round.
- Clipping: the "[0, 1] truncated" sentence follows eq. (6) and applies to CI endpoints, not to θ̂ (eq. (5)).

F2. Bias and assumption.
- Eq. (9), §5.1, p.5: E[p̂] = p = (q0 + q1 − 1)·θ + (1 − q0). Estimator inversion requires q0 + q1 > 1 (§5.1 p.5).
- Distribution-shift claim (§1, p.2): the paper states θ̂ "remains unbiased under such shifts". Stated only; not re-derived here.

F3. CI construction (eq. (6)-(8), §4.2 p.4; eq. (10), §5.2 p.5; derivation App. E.1 p.15).
- Eq. (6): θ̃ + dθ̃ ± z_α · sqrt{ [ p̃(1−p̃)/ñ + (1−θ̃)²·q̃0(1−q̃0)/m̃0 + θ̃²·q̃1(1−q̃1)/m̃1 ] / (q̃0+q̃1−1)² }.
- Eq. (7): ñ = n+z², m̃0 = m0+2, m̃1 = m1+2, p̃ = (n·p̂ + z²/2)/(n+z²), q̃0 = (m0·q̂0+1)/(m0+2), q̃1 = (m1·q̂1+1)/(m1+2), θ̃ = (p̃+q̃0−1)/(q̃0+q̃1−1).
- Center shift dθ̃ (eq. (8)) is dropped as negligible (§5.2 p.5).
- Interval type: asymptotic delta-method Wald form with "add two successes and two failures" adjustment (§5.2 p.5). NOT an exact Clopper-Pearson interval. Full-text search of the paper finds no "Clopper", "Wilson", or exact-binomial interval (only Agresti refs).
- Coverage evidence is empirical only: Table 1, p.8, Chatbot Arena 95% CI coverage: Alpaca 96%, Claude 95%, FastChat-T5 97%, GPT-4 97%, LLaMA 99%, Vicuna 99%.
- The CI targets θ only. It gives no interval for per-class recall or specificity.

F4. Adaptive allocation guidance (Algorithm 1, App. C, p.14; Prop. 5.2, §5, p.5; pilot size §4.2 p.4).
- Pilot: m_pilot per label type (e.g. 10). q̃0, q̃1 with +1/+2 smoothing. κ̂ = (1−q̃0)/(1−q̃1).
- Step 6: m1* = round( m / (1 + (1/p̂ − 1)·√κ̂) ). Step 7: m1 = min{ max{m1*, m_pilot}, m − m_pilot }, m0 = m − m1.
- Prop. 5.2 hypothesis: "Suppose that q̃0 and q̃1 are close to 1." Conclusion: "Then the minimum length of the confidence interval defined in (6) is achieved when m̃0 ≈ (1/p̃ − 1) √κ · m̃1."
- Scope: the optimality is an approximation valid near q → 1 and uses the test-set p̂ in place of θ.

F5. [INFERENCE, my numeric check, not a paper claim]. Minimizing eq. (10) over m0 with m0+m1 = m = 200 gives m1* = m/(1+√(A/B)), with A = (1−θ)²·q0(1−q0), B = θ²·q1(1−q1). Compared with Algorithm 1 step 6 using p (=p̂ in the limit) and using θ:
- θ=0.3, q0=q1=0.95: exact 60.0; step 6 with p=0.320: 64.0; with θ: 60.0.
- θ=0.3, q0=0.9, q1=0.7: exact 79.1; with p=0.280: 80.5; with θ: 85.2.
- θ=0.5, q0=0.99, q1=0.98: exact 116.9; with p=0.495: 116.2; with θ: 117.2.
- θ=0.2, q0=0.8, q1=0.9: exact 31.6; with p=0.340: 53.4; with θ: 30.0.
- Reading: step 6 is close near q≈1 but misallocates by ~20 of 200 at q≈0.8-0.9 when p ≠ θ. The gap comes from the paper dropping the √q factors and using p for θ. Computed with stdlib python3 from eq. (10) and the paper's p = (q0+q1−1)θ+(1−q0) (eq. (9)).

## SOURCES (opened this round)
- https://proceedings.mlr.press/v306/lee26bl.html | 2026-10-21T00:16:15Z | "Additionally, it uses an adaptive strategy to allocate calibration samples for tighter intervals." | Abstract (HTML)
- PDF (above) | 2026-10-21T00:16:20Z | "In this case, an unbiased estimator of the true accuracy θ in (1) is given by" | §4.1, p.4, before eq. (4)
- PDF | 2026-10-21T00:16:20Z | "Substituting estimates q̂1 and q̂0 into (4) gives the bias-corrected estimator (Rogan & Gladen, 1978; Lang & Reiczigel, 2014)." | §4.2, p.4, before eq. (5)
- PDF | 2026-10-21T00:16:20Z | "Assuming q0 + q1 > 1, inverting the above relation in (9) gives the estimator in (4)." | §5.1, p.5
- PDF | 2026-10-21T00:16:20Z | "Based on this variance, we construct a confidence interval for θ using the "add two successes and two failures" adjusted Wald approach" | §5.2, p.5, right column
- PDF | 2026-10-21T00:16:20Z | "where values outside the interval [0, 1] are truncated to 0 or 1." | §4.2, p.4, after eq. (6)
- PDF | 2026-10-21T00:16:20Z | "Applying the delta method and the binomial variance formulas for p̂, q̂0, and q̂1, we obtain the asymptotic variance" | §5.2, p.5, before eq. (10)
- PDF | 2026-10-21T00:16:20Z | "Then the minimum length of the confidence interval defined in (6) is achieved when m̃0 ≈ (1/p̃ − 1) √κ · m̃1." | Prop. 5.2, p.5
- PDF | 2026-10-21T00:16:20Z | "The algorithm first collects a small pilot calibration set (e.g., mpilot = 10 per label type) to obtain preliminary estimates q̂0 and q̂1." | §4.2, p.4
- PDF | 2026-10-21T00:16:20Z | "In contrast, the estimator θ̂ based on Rogan & Gladen (1978) remains unbiased under such shifts." | §1, p.2
- PDF | 2026-10-21T00:16:20Z | "Table 1 reports the coverage of the proposed 95% confidence intervals, which remains close to or slightly above the nominal level across models" | §7 Results, p.8

## Installs
None. Used curl, sha256sum, file, pdftotext/pdfinfo/pdftoppm (poppler, already at /usr/bin), python3 stdlib. No packages installed or updated.

VERDICT: S011 estimator is exactly the Rogan-Gladen form (eq. (4)-(5), p.4). Its CI is an asymptotic delta-method adjusted-Wald (eq. (6)-(8)), not an exact Clopper-Pearson interval, validated only empirically (Table 1, p.8). Algorithm 1 allocation is an approximation that misallocates away from q≈1 when p̂≠θ (my check, [INFERENCE]).
