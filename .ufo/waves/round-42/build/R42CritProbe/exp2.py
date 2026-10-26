import sys, subprocess, pathlib
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans")
import fibsqrt_probe as P
base = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/R42CritProbe/env"); sim = str(base/"sim")
def run(name, lines, ns):
    d = base/"c"/name; d.mkdir(parents=True, exist_ok=True)
    (d/"gates.txt").write_text("\n".join(lines) + "\n")
    return {n: subprocess.run([sim, str(n)], cwd=d, capture_output=True, text=True).stdout.strip() for n in ns}
holds = [f"out{i} = out{i}" for i in range(32)]
bins  = [f"out{32+i} = out0 & out0" for i in range(32)]
print("A2 bin trailing ", run("a2", holds + [l + " " for l in bins], [1]))
print("A3 bin clean    ", run("a3", holds + bins, [1]))
print("A5 undeclared   ", run("a5", ["out40 = out0"], [1]))
print("A6 declared     ", run("a6", ["out0 = out0"] + [f"out{i} = out{i}" for i in range(1,32)] + ["out40 = out0"], [1]))
# comment line: is it skipped, or does it blank a signal?
print("A7 comment      ", run("a7", ["# out40 = out0"] + holds + ["out41 = out40"], [1]))
