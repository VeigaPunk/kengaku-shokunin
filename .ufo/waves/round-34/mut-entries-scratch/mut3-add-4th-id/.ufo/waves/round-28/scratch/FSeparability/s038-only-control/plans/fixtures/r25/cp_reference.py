#!/usr/bin/env python3
"""cp_reference.py — independent exact Clopper–Pearson reference (kengaku r25, C1).

N-version reference for `clopper_pearson` in plans/attrib_calibration.py. It
shares no code, formula or library with that implementation: each bound is
found by bisection directly on the exact binomial tail sum, evaluated in
rational arithmetic (fractions.Fraction). No beta or F quantile, no
incomplete-beta series, and no float touches the computation path (floats
appear only in --published, as the independent side of a comparison).

Definition — two-sided, confidence 1 - alpha, R `binom.test` semantics
(src/library/stats/R/binom.test.R: "Determine p s.t. Prob(B(n,p) >= x) = alpha"):
    lo(k, n) = 0 if k == 0, else the p with P(X >= k   | n, p) = alpha/2
    hi(k, n) = 1 if k == n, else the p with P(X >= k+1 | n, p) = 1 - alpha/2
                                 (equivalently P(X <= k   | n, p) = alpha/2)
For 1 <= j <= n, P(X >= j | n, p) is strictly increasing on [0, 1] (its
derivative n*C(n-1, j-1)*p^(j-1)*(1-p)^(n-j) is positive inside), so each root
is unique. n = 0 is vacuous: P(X >= 0) = 1 for every p, so the definition
yields [0, 1]; R's binom.test rejects n = 0.

Every printed digit is proven. Bisection runs on the grid i/10^D and ends with
the root between two neighbours; one exact evaluation at their midpoint decides
the rounding (half-up). A root exactly on a midpoint is reported as a tie.
--verify re-proves a TSV without trusting the search: two exact tail
evaluations per bound show the root lies within half a unit of the printed
value; it also checks grid completeness, the k=0/k=n endpoints, the symmetry
lo(k, n) = 1 - hi(n-k, n) and monotonicity in k.

Usage (exit 0 ok, 1 mismatch or failed proof, 2 usage):
    cp_reference.py [--nmax 40] [--alpha 0.05] [--decimals 12] [--out PATH]
    cp_reference.py --verify PATH [--alpha 0.05]
    cp_reference.py --point K N [--alpha 0.05] [--decimals 12]
    cp_reference.py --published [--nmax 40]
--published exits 1 iff a verdict differs from its pinned expectation or a
closed form disagrees; adjudicated source errors stay MISMATCH and are printed.
The TSV header is `k n lo hi` (tab-separated); rows are ordered by n, then k.
Regenerate the fixture with
    python3 plans/fixtures/r25/cp_reference.py --out plans/fixtures/r25/cp_reference.tsv

Stdlib only, offline.
"""

import argparse
import math
import re
import sys
from fractions import Fraction
from math import comb

NMAX_DEFAULT = 40
ALPHA_DEFAULT = "0.05"
DECIMALS_DEFAULT = 12
EXACT_DECIMALS = 25  # display precision of the exact side in --published
HEADER = "k\tn\tlo\thi"
VALUE_RE = re.compile(r"^[01]\.(\d+)$")

# Values printed in sources opened 2026-10-20 (fetched 2026-10-21T00:22:50Z UTC)
# and found verbatim in the fetched bytes. `conf` is the two-sided level the
# value belongs to: a one-sided 1-a bound equals the two-sided 1-2a bound.
# kind "dec": fixed decimals, must equal the exact root correctly rounded to the
# same places. kind "f64": a float64 repr, must lie within half a unit of the
# 12th decimal of the exact root (the TSV's precision); its ulp error is shown.
# `expect` pins the adjudicated verdict, so drift in either direction fails. The
# three MISMATCH rows are source errors, confirmed by the sign of the tail
# residual at the rounding midpoint in 60-digit decimal arithmetic: the root
# finders behind NIST's numbers (Dataplot ROOTS; R uniroot with its default
# tol = .Machine$double.eps^0.25) miss the root at the printed precision.
STATA = "https://www.stata.com/manuals/rci.pdf"
SCIPY_BT = "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html"
SCIPY_CI = ("https://docs.scipy.org/doc/scipy/reference/generated/"
            "scipy.stats._result_classes.BinomTestResult.proportion_ci.html")
NIST = "https://www.itl.nist.gov/div898/handbook/prc/section2/prc241"
NCSS = "https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/NCSS/One_Proportion.pdf"
PUBLISHED = (
    # (label, k, n, conf, bound, printed, kind, expect, location)
    ("stata-ex6", 2, 20, "0.95", "lo", ".0123485", "dec", "MATCH",
     f"{STATA} PDF p.9 Example 6"),
    ("stata-ex6", 2, 20, "0.95", "hi", ".3169827", "dec", "MATCH",
     f"{STATA} PDF p.9 Example 6"),
    ("stata-tn", 0, 20, "0.95", "hi", ".1684335", "dec", "MATCH",
     f"{STATA} PDF p.10 Technical note (printed as one-sided 97.5%)"),
    ("stata-ex13", 1, 10, "0.99", "lo", ".0005011", "dec", "MATCH",
     f"{STATA} PDF p.14 Example 13"),
    ("stata-ex13", 1, 10, "0.99", "hi", ".5442871", "dec", "MATCH",
     f"{STATA} PDF p.14 Example 13"),
    ("scipy-binomtest", 3, 15, "0.90", "lo", "0.05684686759024681", "f64", "MATCH",
     f"{SCIPY_BT} Examples (alternative='greater', one-sided 0.95)"),
    ("scipy-proportion_ci", 7, 50, "0.95", "lo", "0.05819170033997342", "f64", "MATCH",
     f"{SCIPY_CI} Examples"),
    ("scipy-proportion_ci", 7, 50, "0.95", "hi", "0.26739600249700846", "f64", "MATCH",
     f"{SCIPY_CI} Examples"),
    ("nist-7.2.4.1", 4, 20, "0.90", "lo", "0.071354", "dec", "MATCH",
     f"{NIST}.htm example, Dataplot PL (output in {NIST}.dp)"),
    ("nist-7.2.4.1", 4, 20, "0.90", "hi", "0.401029", "dec", "MISMATCH",
     f"{NIST}.htm example, Dataplot PU (output in {NIST}.dp)"),
    ("nist-7.2.4.1-r", 4, 20, "0.90", "lo", "0.07134838", "dec", "MISMATCH",
     f"{NIST}.r uniroot pl$root"),
    ("nist-7.2.4.1-r", 4, 20, "0.90", "hi", "0.4010294", "dec", "MISMATCH",
     f"{NIST}.r uniroot pu$root"),
    ("ncss-510", 55, 100, "0.95", "lo", "0.4472802", "dec", "MATCH",
     f"{NCSS} p.510-5 Example 1, Exact Confidence Interval for P"),
    ("ncss-510", 55, 100, "0.95", "hi", "0.6496798", "dec", "MATCH",
     f"{NCSS} p.510-5 Example 1, Exact Confidence Interval for P"),
)
# Closed forms for x = 0 and x = n (Wikipedia, "Binomial proportion confidence
# interval", section Clopper–Pearson interval): hi(0, n) = 1 - (alpha/2)^(1/n),
# lo(n, n) = (alpha/2)^(1/n). Evaluated in float64; tolerance covers its error.
CLOSED_FORM_TOL = 1e-15


def tail_ge(j, n, p):
    """Exact P(X >= j) for X ~ Binomial(n, p), p a Fraction in [0, 1]."""
    if j <= 0:
        return Fraction(1)
    if j > n:
        return Fraction(0)
    a = p.numerator
    b = p.denominator - a
    total = sum(comb(n, i) * a**i * b ** (n - i) for i in range(j, n + 1))
    return Fraction(total, p.denominator**n)


def root_units(j, n, target, decimals):
    """Root r of P(X >= j | n, r) = target, correctly rounded half-up to
    `decimals` places, as (units of 10^-decimals, tie). Requires 1 <= j <= n and
    0 < target < 1: the tail rises strictly from 0 at p=0 to 1 at p=1."""
    scale = 10**decimals
    below, above = 0, scale  # invariant: tail(below) <= target < tail(above)
    while above - below > 1:
        mid = (below + above) // 2
        if tail_ge(j, n, Fraction(mid, scale)) <= target:
            below = mid
        else:
            above = mid
    # below/scale <= r < above/scale; the midpoint between them decides.
    at_mid = tail_ge(j, n, Fraction(2 * below + 1, 2 * scale))
    if at_mid < target:
        return above, False
    if at_mid > target:
        return below, False
    return above, True  # r is exactly the midpoint: half-up, reported as a tie


def bound_units(k, n, alpha, bound, decimals):
    """One Clopper–Pearson bound ('lo' or 'hi') as (units of 10^-decimals, tie)."""
    if not 0 <= k <= n:
        raise ValueError(f"need 0 <= k <= n, got k={k} n={n}")
    if bound == "lo":
        return (0, False) if k == 0 else root_units(k, n, alpha / 2, decimals)
    if k == n:
        return 10**decimals, False
    return root_units(k + 1, n, 1 - alpha / 2, decimals)


def fmt(units, decimals):
    whole, frac = divmod(units, 10**decimals)
    return f"{whole}.{frac:0{decimals}d}"


def emit(nmax, alpha, decimals):
    """TSV lines for every 0 <= k <= n <= nmax, plus the (k, n, bound) ties."""
    lines, ties = [HEADER], []
    for n in range(nmax + 1):
        for k in range(n + 1):
            cells = [str(k), str(n)]
            for bound in ("lo", "hi"):
                units, tie = bound_units(k, n, alpha, bound, decimals)
                if tie:
                    ties.append((k, n, bound))
                cells.append(fmt(units, decimals))
            lines.append("\t".join(cells))
    return lines, ties


def certify(j, n, target, value, half):
    """True iff the root r of P(X >= j | n, r) = target lies in
    [value - half, value + half), i.e. `value` is r correctly rounded half-up."""
    left, right = value - half, value + half
    left_ok = left <= 0 or tail_ge(j, n, left) <= target
    right_ok = right >= 1 or tail_ge(j, n, right) > target
    return left_ok and right_ok


def parse_tsv(path):
    """(rows {(k, n): (lo, hi, lineno)}, decimals, failures) from a TSV file."""
    failures, rows, decimals = [], {}, None
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    if not lines or lines[0] != HEADER:
        return rows, decimals, [f"line 1: header is not {HEADER!r}"]
    for lineno, line in enumerate(lines[1:], start=2):
        cells = line.split("\t")
        matches = [VALUE_RE.match(c) for c in cells[2:]]
        if (len(cells) != 4 or not cells[0].isdigit() or not cells[1].isdigit()
                or not all(matches)):
            failures.append(f"line {lineno}: malformed row {line!r}")
            continue
        places = {len(m.group(1)) for m in matches}
        if decimals is None:
            decimals = min(places)
        if places != {decimals}:
            failures.append(f"line {lineno}: values not printed to {decimals} places")
            continue
        key = (int(cells[0]), int(cells[1]))
        if key in rows:
            failures.append(f"line {lineno}: duplicate k={key[0]} n={key[1]} "
                            f"(first at line {rows[key][2]})")
            continue
        rows[key] = (Fraction(cells[2]), Fraction(cells[3]), lineno)
    return rows, decimals, failures


def verify(path, alpha):
    """Re-prove every row of a TSV. Returns (failures, stats)."""
    rows, decimals, failures = parse_tsv(path)
    stats = {"rows": len(rows), "nmax": None, "decimals": decimals, "certified": 0,
             "endpoints": 0, "symmetric": 0, "monotone": 0}
    if not rows:
        return failures or ["no data rows"], stats
    nmax = max(n for _, n in rows)
    stats["nmax"] = nmax
    grid = {(k, n) for n in range(nmax + 1) for k in range(n + 1)}
    for k, n in sorted(grid - rows.keys(), key=lambda kn: (kn[1], kn[0])):
        failures.append(f"missing row k={k} n={n}")
    for k, n in sorted(rows.keys() - grid):
        failures.append(f"line {rows[(k, n)][2]}: k={k} n={n} outside 0<=k<=n")
    half = Fraction(1, 2 * 10**decimals)
    for (k, n), (lo, hi, lineno) in sorted(rows.items(), key=lambda r: r[1][2]):
        if (k, n) not in grid:
            continue
        where = f"line {lineno} k={k} n={n}"
        if k == 0:
            stats["endpoints"] += 1
            if lo != 0:
                failures.append(f"{where}: lo must be exactly 0 when k=0")
        elif certify(k, n, alpha / 2, lo, half):
            stats["certified"] += 1
        else:
            failures.append(f"{where}: lo={fmt(int(lo * 10**decimals), decimals)} "
                            f"is not the correctly rounded root")
        if k == n:
            stats["endpoints"] += 1
            if hi != 1:
                failures.append(f"{where}: hi must be exactly 1 when k=n")
        elif certify(k + 1, n, 1 - alpha / 2, hi, half):
            stats["certified"] += 1
        else:
            failures.append(f"{where}: hi={fmt(int(hi * 10**decimals), decimals)} "
                            f"is not the correctly rounded root")
        mirror = rows.get((n - k, n))
        if mirror is not None:
            if lo + mirror[1] == 1:
                stats["symmetric"] += 1
            else:
                failures.append(f"{where}: lo != 1 - hi(k={n - k}, n={n})")
        upper = rows.get((k + 1, n))
        if upper is not None:
            for name, here, there in (("lo", lo, upper[0]), ("hi", hi, upper[1])):
                if here < there:
                    stats["monotone"] += 1
                else:
                    failures.append(f"{where}: {name} not increasing into k={k + 1}")
    return failures, stats


def exact_text(k, n, alpha, bound):
    units, _ = bound_units(k, n, alpha, bound, EXACT_DECIMALS)
    return fmt(units, EXACT_DECIMALS)


def published(nmax):
    """Cross-check lines, summary line and failure count (verdicts differing
    from their pinned expectation plus closed-form disagreements)."""
    out = ["label\tk\tn\tconf\tbound\tprinted\texact_25dp\tabs_diff\tverdict\texpect\tnote"]
    matched = unexpected = 0
    tsv_half = Fraction(1, 2 * 10**DECIMALS_DEFAULT)
    for label, k, n, conf, bound, printed, kind, expect, _location in PUBLISHED:
        alpha = 1 - Fraction(conf)
        exact_str = exact_text(k, n, alpha, bound)
        exact = Fraction(exact_str)
        if kind == "dec":
            places = len(printed.split(".")[1])
            units, _ = bound_units(k, n, alpha, bound, places)
            value = Fraction(printed)
            ok = units == value * 10**places
            note = f"exact to {places}dp = {fmt(units, places)}"
        else:
            value = Fraction(float(printed))
            ok = abs(value - exact) <= tsv_half
            ulps = (value - exact) / Fraction(math.ulp(float(printed)))
            note = f"float64 error {float(ulps):+.2f} ulp"
        verdict = "MATCH" if ok else "MISMATCH"
        matched += ok
        unexpected += verdict != expect
        out.append(f"{label}\t{k}\t{n}\t{conf}\t{bound}\t{printed}\t{exact_str}\t"
                   f"{float(abs(value - exact)):.1e}\t{verdict}\t{expect}\t{note}")
    worst, closed_bad = Fraction(0), 0
    alpha = Fraction(ALPHA_DEFAULT)
    for n in range(1, nmax + 1):
        root = math.pow(float(alpha / 2), 1.0 / n)
        for k, bound, formula in ((0, "hi", 1.0 - root), (n, "lo", root)):
            diff = abs(Fraction(formula) - Fraction(exact_text(k, n, alpha, bound)))
            worst = max(worst, diff)
            closed_bad += diff > CLOSED_FORM_TOL
    summary = (f"published: values={len(PUBLISHED)} match={matched} "
               f"mismatch={len(PUBLISHED) - matched} unexpected={unexpected} | "
               f"closed_form: values={2 * nmax} match={2 * nmax - closed_bad} "
               f"mismatch={closed_bad} max_abs_diff={float(worst):.1e} "
               f"tol={CLOSED_FORM_TOL:.0e}")
    return out, summary, unexpected + closed_bad


def parse_alpha(text):
    alpha = Fraction(text)
    if not 0 < alpha < 1:
        raise ValueError(f"alpha must lie in (0, 1), got {text}")
    return alpha


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Exact Clopper–Pearson reference by rational bisection.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--verify", metavar="PATH", help="re-prove every row of a TSV")
    mode.add_argument("--point", nargs=2, type=int, metavar=("K", "N"),
                      help="print one interval")
    mode.add_argument("--published", action="store_true",
                      help="cross-check against values printed in opened sources")
    ap.add_argument("--nmax", type=int, default=NMAX_DEFAULT)
    ap.add_argument("--alpha", default=ALPHA_DEFAULT, help="exact decimal or p/q")
    ap.add_argument("--decimals", type=int, default=DECIMALS_DEFAULT)
    ap.add_argument("--out", metavar="PATH", help="write the TSV here, not stdout")
    args = ap.parse_args(argv)
    try:
        alpha = parse_alpha(args.alpha)
    except (ValueError, ZeroDivisionError) as exc:
        ap.error(str(exc))
    if not 1 <= args.decimals <= 60:
        ap.error("--decimals must lie in 1..60")
    if args.nmax < 0:
        ap.error("--nmax must be >= 0")
    if args.out and (args.verify or args.point or args.published):
        ap.error("--out applies only to TSV emission")

    if args.verify:
        failures, stats = verify(args.verify, alpha)
        for line in failures:
            print(f"FAIL {line}")
        print("verify: " + " ".join(f"{k}={v}" for k, v in stats.items())
              + f" alpha={alpha} failures={len(failures)}")
        return 1 if failures else 0
    if args.point:
        k, n = args.point
        if not 0 <= k <= n:
            ap.error("--point needs 0 <= K <= N")
        cells, ties = [str(k), str(n)], 0
        for bound in ("lo", "hi"):
            units, tie = bound_units(k, n, alpha, bound, args.decimals)
            cells.append(fmt(units, args.decimals))
            ties += tie
        print(HEADER)
        print("\t".join(cells))
        if ties:
            print(f"cp_reference: ties={ties} (root exactly on a rounding midpoint; "
                  f"printed half-up)", file=sys.stderr)
        return 0
    if args.published:
        lines, summary, failures = published(args.nmax)
        print("\n".join(lines))
        print(summary)
        return 1 if failures else 0

    lines, ties = emit(args.nmax, alpha, args.decimals)
    text = "\n".join(lines) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
    for k, n, bound in ties:
        print(f"cp_reference: tie k={k} n={n} {bound} (printed half-up)", file=sys.stderr)
    print(f"cp_reference: rows={len(lines) - 1} nmax={args.nmax} alpha={alpha} "
          f"decimals={args.decimals} ties={len(ties)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
