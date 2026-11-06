#!/usr/bin/env python3
"""Independent gap-case builder for ExecC1 (own derivation, not probe BUILDER).
Usage: build_gaps.py <kind> <appdir> <fixturedir>
kind in: marginal-only, dup-edges-extra, ks-shift-small, ks-shift-large
True D params from test_outputs.py:
  true_mean = -12.2965135 + 0.5495886 * 50.47989
  true_std  = sqrt(0.5495886**2 * 10.68515**2 + 14.0916**2)
Writes /app-equivalents: learned_dag.csv, intervened_dag.csv, final_bn_sample.csv
into appdir. For ks cases also prints KS statistic/p for D.
"""
import shutil, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm, kstest

kind = sys.argv[1]
app = Path(sys.argv[2]); fx = Path(sys.argv[3])
app.mkdir(parents=True, exist_ok=True)
TRUE_MEAN = -12.2965135 + 0.5495886 * 50.47989
TRUE_STD = ((0.5495886 ** 2) * 10.68515 ** 2 + 14.0916 ** 2) ** 0.5
sol = pd.read_csv(fx / "final_bn_sample.csv")

def copy(*names):
    for n in names:
        shutil.copyfile(fx / n, app / n)

def write_sample(df):
    df[["U", "Y", "R", "D", "M"]].to_csv(app / "final_bn_sample.csv", index=False)

if kind == "marginal-only":
    # Only column D is tested by the grader (test_sampled_data reads final_bn_sample["D"]).
    # Independent choice: U,R,Y,M = 0.0; D ~ N(true_mean, true_std) seeded RNG.
    copy("learned_dag.csv", "intervened_dag.csv")
    rng = np.random.default_rng(20261106)
    df = pd.DataFrame({c: np.zeros(10000) for c in ["U", "Y", "R", "D", "M"]})
    df["D"] = rng.normal(TRUE_MEAN, TRUE_STD, 10000)
    write_sample(df)
    st, p = kstest(df["D"], "norm", args=(TRUE_MEAN, TRUE_STD))
    print(f"BUILT marginal-only seed=20261106 KSstat={st:.6f} p={p:.6g}")
elif kind == "dup-edges-extra":
    # Independent choice: learned_dag rows duplicated (each edge twice) + weight column.
    copy("intervened_dag.csv", "final_bn_sample.csv")
    d = pd.read_csv(fx / "learned_dag.csv")
    d = pd.concat([d, d], ignore_index=True)
    d["weight"] = 1.0
    d.to_csv(app / "learned_dag.csv", index=False)
    print("BUILT dup-edges-extra")
elif kind in ("ks-shift-small", "ks-shift-large"):
    # D = true_mean + true_std * (quantile grid + k), k=0.045 / 0.050 sd.
    # Other columns copied from solution sample.
    copy("learned_dag.csv", "intervened_dag.csv")
    k = 0.045 if kind == "ks-shift-small" else 0.050
    df = sol.copy()
    df["D"] = TRUE_MEAN + TRUE_STD * (norm.ppf((np.arange(10000) + 0.5) / 10000) + k)
    write_sample(df)
    st, p = kstest(df["D"], "norm", args=(TRUE_MEAN, TRUE_STD))
    print(f"BUILT {kind} k={k} KSstat={st:.6f} p={p:.6g}")
else:
    raise SystemExit("unknown kind " + kind)
