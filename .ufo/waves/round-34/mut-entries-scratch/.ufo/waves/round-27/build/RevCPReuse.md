# RevCPReuse — round 27 build: clopper_pearson verification (C1 cross-check support)

Scope: import purity; endpoint behaviour at k=n and k=0 (n=1964); cp95 bounds for k=1964/1963/1950 for the integrator's summary cross-check. Read-only on the lane; scratch only in /tmp. No subagents, no connector seats (leaf seat; Main's connector FYI has nothing to record here).
Installs: none (system python3 3.14.8; numpy present, unused; mpmath and scipy absent).

## Findings

1. Import is side-effect free; the first call only reads. One-liner (cwd /tmp, `PYTHONDONTWRITEBYTECODE=1`, sys.path[0]=lane plans/, audit hook), exit 0:
   - Import: 93 read opens; 0 write opens; 0 os/subprocess/socket/shutil side effects. Only `os.listdir` events, which are read-only import-system directory listings (plans/, /tmp, stdlib package dirs); the count varied 7 to 10 between runs with directory-cache state.
   - First `clopper_pearson` call: `_load_betai` (attrib_calibration.py:107-117) execs grader.py with `sys.dont_write_bytecode=True`. Its only read is `kengaku-shokunin/__pycache__/grader.cpython-314.pyc`; 0 writes.
   - `find plans grader.py __pycache__ plans/__pycache__ -newer /tmp/r27-revcp-marker` → empty. The existing pyc files predate this seat's runs.
   - Plans-resident script on a /tmp copy (attrib_calibration.py sha256 6656c0b5…, grader.py sha256 90c87c88…, both identical to lane) → `python3 /tmp/r27-revcp-mock/plans/new_probe.py`, exit 0, same values as below.
   - Without the env var, a plain `import attrib_calibration` writes `plans/__pycache__/attrib_calibration.cpython-314.pyc` (ordinary import caching, scratch copy); `_load_betai` writes none. `.gitignore:2` ignores `__pycache__/`. Run every lane command with PYTHONDONTWRITEBYTECODE=1.

2. Endpoints are exact by construction, and closed forms agree. attrib_calibration.py:148-151: n==0 → (0.0,1.0); lo=0.0 if k==0; hi=1.0 if k==n; otherwise bisection on grader.py `betai` (:915-925, lgamma prefactor + continued fraction).
   - k=n=1964: hi == 1.0 (True). lo = 0.9981235146097471 = float(0.025**(1/1964)), diff 0.0. Exact: 0.998123514609747092.
   - k=0: lo == 0.0 (True). hi = 0.001876485390252913. Float closed form 1-0.025**(1/1964) = 0.0018764853902528689 (diff +4.4e-17). Exact: 0.0018764853902529079, so the module error is +5.1e-18. The float closed form is the worse value (1-x cancellation); use the exact reference as oracle here.
   - The selftest closed-form anchors cover n=1..40 only (attrib_calibration.py:737-739). n=1964 is checked only here.

3. cp95 bounds for the integrator cross-check (n=1964, two-sided alpha=0.05, tail 0.025 each; `%.6f` as in the summary lines):

| k | module lo, hi | cp95 | exact lo / hi (Decimal ref) |
|---|---|---|---|
| 1964 | 0.9981235146097471, 1.0 | [0.998124,1.000000] | 0.998123514609747092 / 1 |
| 1963 | 0.9971664138999543, 0.999987109142159 | [0.997166,0.999987] | 0.997166413899954502 / 0.999987109142158957 |
| 1950 | 0.98806880347839, 0.9960975680531943 | [0.988069,0.996098] | 0.988068803478390849 / 0.996097568053194323 |
| 0 (extra) | 0.0, 0.001876485390252913 | [0.000000,0.001876] | 0 / 0.001876485390252908 |

   - Reference: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/r27-revcp-ref.py`, exit 0. It uses 70-digit Decimal bisection on exact binomial tails with no betai; residual P(tail)−0.025 ≤ 5.4e-52. Max |module − exact| over these bounds: 8.5e-16.
   - Tightest 6-dp margins: 1.5e-8 (k=1964 lo; k=0 hi). That is far above the error, so no rounding ambiguity.

4. Full-range sweep, `/tmp/r27-revcp-sweep.py`, exit 0. 177 k values (every 17th k in [0,1964] plus all k in [1900,1964]) against an independent log-space tail bisection (math.lgamma + fsum). Max |diff| 1.18e-14 (k=1343); 0 diffs above 1e-9; 0 six-dp mismatches.

5. LOW (defect): the guard is bypassed under the cache. `clopper_pearson` is `@functools.lru_cache` (attrib_calibration.py:143), so the type/range guard (:146-147) runs only on cache misses. After `cp(1964,1964)`, `cp(1964.0,1964)` returns the cached tuple with no error (cache hits=1). A fresh `cp(1963.0,1964)` raises ValueError, exit 0. Numerics are unaffected and the integrator passes ints, so no action for C1. Fix in lane: validate before the cache.

6. LOW (caller contract): `clopper_pearson(0,0)` returns (0.0,1.0) (:148-149). An empty cell would print cp95=[0.000000,1.000000]. Callers must mark empty cells UNTESTED rather than print an interval.

7. Anchor sanity: clopper_pearson(7,50) = (0.058191700340371855, 0.2673960024970089). The SciPy anchor cited in the lane comment (attrib_calibration.py:727-728) is (0.05819170033997342, 0.26739600249700846); |Δ| = 4.0e-13 (lo), 4.4e-16 (hi). I did not open the SciPy docs; the anchor values are as cited in the lane's own code.

Files written: this report (the only lane write, at its authorised report path; no jj, git, or index writes). Scratch only in /tmp: r27-revcp-ref.py, r27-revcp-sweep.py, r27-revcp-marker, r27-revcp-mock/{plans/attrib_calibration.py, grader.py, plans/new_probe.py}.

VERDICT: clopper_pearson is import-pure (reads only; the first call reads grader's cached pyc and writes nothing); endpoints are exact at k=n (hi=1.0) and k=0 (lo=0.0); accuracy ≤1.2e-14 across k. Summary cross-checks: k=1964 [0.998124,1.000000], k=1963 [0.997166,0.999987], k=1950 [0.988069,0.996098]. Fix the LOW lru_cache guard bypass and the n=0 labelling.
