#!/usr/bin/env python3
"""MutC2: delete each SPELLING regex in turn; compare the gate's own --selftest with the T census."""
import json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r97/MutC2")
SRC = ROOT / "clone/plans/round97_gate_selftest_census.py"
LANE = ROOT / "clone"
T = "f1083da60e7ff6b88f7420aae7424f7762d14700"
B = "4992cd0e32b8db23ca20310deb7de12d485f8bcc"
OUT = ROOT / "work/pat"
ENV = dict(os.environ, TMPDIR=str(ROOT / "tmp"))

def drop_pattern(src: str, idx: int) -> str:
    lines = src.splitlines(True)
    start = next(i for i, l in enumerate(lines) if l.startswith("SPELLING = [re.compile"))
    end = next(i for i in range(start, len(lines)) if lines[i].rstrip() == ")]")
    block = list(range(start + 1, end))
    keep = [i for i in block if lines[i].strip()]
    if idx >= len(keep):
        raise SystemExit(f"pattern {idx} out of range ({len(keep)})")
    del lines[keep[idx]]
    return "".join(lines)

def run(script: Path, args: list[str]):
    p = subprocess.run([sys.executable, "-I", "-B", str(script), *args],
                       capture_output=True, text=True, env=ENV, timeout=900)
    return p.returncode, p.stdout

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    src = SRC.read_text()
    res = []
    for idx in range(6):
        d = OUT / f"P{idx}"
        d.mkdir(parents=True, exist_ok=True)
        f = d / "census.py"
        f.write_text(drop_pattern(src, idx))
        st_rc, st_out = run(f, ["--selftest", "--work", str(d / "w")])
        t_rc, t_out = run(f, ["--lane", str(LANE), "--rev", T])
        b_rc, b_out = run(f, ["--lane", str(LANE), "--rev", B, "--base", B])
        def line(out, pref):
            return next((l for l in out.splitlines() if l.startswith(pref)), "-")
        r = dict(pattern=idx, selftest_rc=st_rc,
                 selftest=line(st_out, "SELFTEST"),
                 t_rc=t_rc, t_gates=line(t_out, "GATES"), t_pred=line(t_out, "PREDICATE"),
                 t_mismatch=[l for l in t_out.splitlines() if l.startswith("MISMATCH ")],
                 b_rc=b_rc, b_gates=line(b_out, "GATES"), b_pred=line(b_out, "PREDICATE"))
        res.append(r)
        print(f"P{idx}: selftest rc={st_rc} {r['selftest']} | T rc={t_rc} {r['t_gates']} {r['t_pred']} | "
              f"BASE rc={b_rc} {r['b_gates']}")
        if r["t_mismatch"]:
            print("     T mismatches:", r["t_mismatch"][:6])
    (ROOT / "ev" / "pattern_probe.json").write_text(json.dumps(res, indent=1))

if __name__ == "__main__":
    main()
