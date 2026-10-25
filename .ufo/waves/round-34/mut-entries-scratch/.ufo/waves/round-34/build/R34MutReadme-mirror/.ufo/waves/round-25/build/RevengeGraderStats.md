# Round 25 — RevengeGraderStats (grader.py statistical helpers, C1 novelty support)

Seat: KengakuR25.RevengeGraderStats · leaf revenger · read-only; only this report written. Base 3f371d2a2ce5ccf1b40b2161210f6591a8320a0a (pre-registration); `git diff 6180e4f --stat -- grader.py plans/attrib_probe.py` → empty (surface clean at base).
Axes: novelty (primary — C1 instrument numeric core), calibration (keep-harmless). godspeed: parallel recon; every claim below is a run command or a verified path:line.

## Inventory (all stdlib-only, deterministic, no RNG in this surface)

| helper | grader.py lines | method | accuracy evidence |
|---|---|---|---|
| `_betacf` | :879-913 | Lentz-modified continued fraction for incomplete beta (Numerical Recipes), MAXIT=300, EPS=3e-16, FPMIN=1e-300 | ≤2.9e-15 vs exact-rational roots (below) |
| `betai(a,b,x)` | :915-926 | regularized I_x(a,b); lgamma `bt`, reflection at x<(a+1)/(a+b+2) | same; `betai(0.5,0.5,0.5)=0.5`, `betai(1,1,0.25)=0.25` (S6, :5485-5510) |
| `t_two_sided_p(t,df)` | :928-930 | exact identity `I_{df/(df+t²)}(df/2,1/2)` | t=2,df=63→0.0500; t=0→1.0 (S6); t=2,df=10→0.07338803477074045 ✓ |
| `t_crit(df,alpha)` | :933-941 | bisection on p, 200 iters, hi=1e4 → full double precision | t_crit(63,0.05)=1.9983405 (S6 anchor); t_crit(10,0.05)=2.2281388519862757 ✓ |
| `_binom_cdf_le` | :945-947 | exact `math.comb` sum / 2^n (one float rounding) | integer-exact numerator |
| `exact_sign_p` | :949-956 | 2·min(P(X≤w),P(X≥w)) exact, clamped | — |
| `exact_mcnemar_p(b,c)` | :958-962 | 2·P(X≤min(b,c)), Bin(b+c,½), clamped | (3,9)→0.14599609375 = 598/4096 exact ✓ |
| `paired_stats` | :1789-1803 | mean/sample-sd/t/p + t_crit(0.05) CI | S6/S7-adjacent; used by r11 gate |
| `mcnemar_pairs` | :1805-1817 | shared sorted pid set → (b,c,p) | deterministic (sorted, no set order) |
| `_logit/_sigmoid/_loglik/calibration_gradient/logistic_fit/logistic_calibration` | :1819-1896 | damped Newton on logit-logit recalibration, fixed cap 50, step-halving | S7: gradient <1e-6 + independent `_profile_grid_fit` (:4206) agreement ≤1e-4 (grader.py:4172-4184) |
| `brier_scores` | :1898-1914 | pooled + per-arm + BSS vs own climatology | S7 anchors 0.25/0.0 and 0/1 (grader.py:4155-4162) |
| `REL_EDGES`/`reliability_bins`/`_bss` | :1916/:1919-1945/:1948-1962 | 5 fixed bins, top closed; `_bss` None on degenerate ref | S7 anchor (grader.py:4164-4171) |

## Import-safety: YES — importable without running main
- Command: `python3 -c` importlib `spec_from_file_location('grader_mod', grader.py)` + `exec_module` from cwd=/tmp → `IMPORT OK in 0.044s`, no stdout, no file I/O errors. Module level is defs + constant dicts only (`DEFAULTS` :66-76 `os.path.join`, `PINS` :87-97, `ERRATA` :103-111); `main()` guarded by `if __name__ == "__main__"` :5730-5737 (exit-2 wrapper).
- Imports :52-63: argparse ast hashlib itertools json math os random re shutil sys tempfile — no socket/subprocess/urllib → offline-safe import. `find /home/vgpnk/Projects/shokunin -maxdepth 2 -name grader.py` → exactly one (no shadow-source).

## CP equivalence (three independent routes; the numbers attrib_calibration will publish)
- Route A (grader transplant): bisection on `betai(k,n-k+1,x)-α/2` / `betai(k+1,n-k,x)-(1-α/2)`.
- Route B: bisection on float binomial PMF tails (`math.comb·p^j(1-p)^{n-j}` sums). Grid n∈{10,16,17,20,30,50,100,200}×all k: max|A−B| = **2.776e-15** (worst n=200).
- Route C: exact `fractions.Fraction` PMF bisection (60 iters, ~1e-18 width) on anchors (1,10),(5,10),(24,30),(7,50),(3,17),(16,16),(0,9),(9,9),(60,200),(1,200),(0,17): max|A−C| = **2.89e-15**.
- External anchor (sibling SrcScipyBinomtest receipt, SciPy 1.18.0 docs): `clopper_pearson(7,50)` → (0.058191700340371855, 0.2673960024970089) vs docs (0.05819170033997342, 0.26739600249700846) — match ≤4e-13, inside any 1e-9 gate.
- Power ask confirmed mechanically: CP(k=n) lower = 0.025^(1/n): n=16 → 0.7940927858 (< 0.80), n=17 → 0.8049356770 (≥ 0.80). So a 10/10 block (e.g. r22 hyper, P1) has lower 0.025^(1/10)=0.6915 → cannot interval-PASS: re-verdicts INDETERMINATE. Upper(0,n)=1−0.025^(1/n) (e.g. n=17 → 0.195064322969).
- Wilson(24,30, z=1.959963984540054) = (0.6269430358685175, 0.9049489282271013) — formula as documented in the SciPy `proportion_ci` page (method 'wilson').
- Determinism: repeat calls byte-identical; no RNG/hash-order dependence in this surface (`mcnemar_pairs` sorts :1810).

## Recommendation: import, don't re-implement (one convention)
- grader.py has **no** Clopper–Pearson or Wilson today (sweep `grep -nE 'Clopper|Wilson' grader.py` → empty; `grep -rlE 'Clopper|Wilson|confidence interval' corpus/evidence/attrib-* plans/attrib*` → empty, rc=1 — the pre-reg "before" sweep holds). So the new code is `clopper_pearson/wilson/verdict/parse_receipt/rg_bound`; the ONLY grader.py pieces CP needs are `_betacf`+`betai` (~50 lines). Importing those two keeps exactly one I_x(a,b) in the lane — the one the committed operability gate already trusts for its own t-CDF verdicts. Vendoring would create a second betacf that can drift from the gate's.
- Import form: `importlib.util.spec_from_file_location("kengaku_grader", os.path.join(root,"grader.py"))` — pins the file by path (no sys.path shadowing), works from any cwd, satisfies the `--root DIR` CLI contract (resolve grader.py under `--root`, default = parent of plans/). A bare `import grader` also works (0.044s) but is shadow-prone and less explicit; prefer the spec form.
- Do NOT import t/McNemar/Brier into attrib_calibration.py — the C1 contract needs none of them; importing unused 5.7k-line-gate helpers widens the surface for zero gain. Wilson is new code (not in grader.py) with the SciPy-doc anchor above.

## Equivalence-verification recipe (drop into `--selftest`; red-before per contract)
1. `assert clopper_pearson(7,50) ≈ (0.05819170033997342, 0.26739600249700846) ±1e-9` (SciPy docs anchor).
2. `assert clopper_pearson(n,n)[0] == 0.025**(1/n) ±1e-9` for n∈{16,17}; `clopper_pearson(0,17)[1] == 0.195064322969 ±1e-9`.
3. Independent-route cross-check: reimplement the PMF-tail bisection (Route B, ~10 lines, `math.comb` only) inside the selftest and assert max|A−B| ≤1e-9 over the anchor grid — this catches a corrupted transplant without a second shipped betai.
4. Flipped-GT / duplicate-block reds are the parse layer's (contract); the perturb-a-known-CP-value red can reuse (1) or (2) with a deliberate 1e-6 offset.
5. Prove import purity once: `python3 -c "import importlib.util,os; r='<root>'; s=importlib.util.spec_from_file_location('kengaku_grader',os.path.join(r,'grader.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.betai(2,3,0.5))"` → 0.6875000000000002, silent, <0.1s.

## Hazards for the writer
- `rg_bound`: pre-reg min/max over the (se,sp) box is attained at corners — I verified analytically (at se=1 the ratio is exactly q; partials have fixed sign per fixed other var) and numerically: rg(0.6,0.7,0.8)→(0.5,0.857142857), rg(0.5,0.794,0.794)→(0.370277078,0.629722922). BUT if a corner has se+sp−1 == 0 exactly, do not skip it: numerator>0 ⇒ limit +∞ ⇒ clipped 1; numerator≤0 ⇒ 0. Handle den≤0 explicitly instead of a ≠0 guard that drops the corner.
- Receipt contract already matches the emission format: 7-column table `| trial | class | prediction | GT | gt_class | chain | correct |` (attrib_probe.py:1004-1013), block header `## GT + scoring at close` (attrib_probe.py:984-986), authoritative-last-block rule in the receipts themselves (attrib-r21-impl-ds-trials.log:316). P1 = 9 files confirmed present under corpus/evidence/ (4×r21, 3×r22, 2×r23).
- Stored verdicts are point fractions with a min-n rule (attrib_probe.py:1010-1014: PASS iff n≥min_scored_trials_per_shim and acc≥bar.min; bar.min=0.80 in all three frozen tables — attrib-r21-frozen.md:33, r22:51, r23:39). The interval rule replaces the verdict, not the counts; INDETERMINATE is a finding (contract), mirroring grader.py's ERRATA pattern of verdict-vs-recompute separation (grader.py:103-111).

## Installs
None. Stock python3 3.14.8 (stdlib only: math/fractions/importlib); pacman untouched per host-wide pause; no tools needed.

VERDICT: grader.py's betai/t/McNemar/Brier surface is exact-method, anchored in-tree (S6/S7) and ≤3e-15 vs an exact rational re-derivation; import `_betacf`+`betai` from grader.py (spec-from-file, --root-resolved) as the single I_x convention, write clopper_pearson/wilson/verdict/parse_receipt/rg_bound fresh in attrib_calibration.py, and pin equivalence with the SciPy-docs anchor + closed-form power anchors + an in-selftest PMF cross-route.
