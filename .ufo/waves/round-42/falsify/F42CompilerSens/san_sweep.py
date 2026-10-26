#!/usr/bin/env python3
"""Full sanitizer sweep: the six graded circuits x 30 inputs under gcc16/clang23 UBSan+ASan."""
import concurrent.futures as cf, pathlib, subprocess, sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/F42CompilerSens")
CIR = S / "circuits"
ENV = ["bwrap", "--dev-bind", "/", "/", "--ro-bind", "/home/vgpnk/.local/bin", "/home/vgpnk/.local/bin",
       "--tmpfs", "/run/user/1000", "--proc", "/proc", "--unshare-pid", "--die-with-parent"]
exp = dict(l.split("\t") for l in (CIR / "expected.tsv").read_text().splitlines())
INPUTS = list(exp)
circuits = ["oracle", "lookup30", "lookup28", "trailing30", "trailing28", "shipped"]
bins = ["gcc16-ubsan", "clang23-ubsan"]
MARK = ("runtime error", "AddressSanitizer", "LeakSanitizer", "UndefinedBehaviorSanitizer", "SEGV")


def run(b, c, n):
    r = subprocess.run(ENV + [str(S / "bin" / b), n], cwd=str(CIR / c), capture_output=True, text=True, timeout=900)
    return b, c, n, r.returncode, r.stdout.strip(), r.stderr


rows = []
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for b, c, n, rc, out, err in ex.map(lambda a: run(*a), [(b, c, n) for b in bins for c in circuits for n in INPUTS]):
        hits = [k for k in MARK if k in err]
        rows.append((b, c, n, rc, out, hits, err.strip().splitlines()[:2]))
        if rc != 0 or hits:
            print(f"FLAG {b}/{c}/{n} rc={rc} hits={hits} out={out!r} err={err.strip()[:300]!r}")
print(f"sweep cells={len(rows)} nonzero_rc={sum(1 for r in rows if r[3])} san_hits={sum(1 for r in rows if r[5])}")
# output equality vs the frozen flag matrix
import json
m = json.loads((S / "matrix.json").read_text())
diff = 0
for b, c, n, rc, out, hits, e in rows:
    ref = m[c][n]["gcc16-O3"]["out"]
    if out != ref:
        diff += 1; print(f"DIFF {b}/{c}/{n} out={out!r} ref={ref!r}")
print(f"sanitizer_build_output_diffs_vs_gcc16-O3={diff}/{len(rows)}")
print("sample stderr lines:", [r[6] for r in rows if r[6]][:3])
