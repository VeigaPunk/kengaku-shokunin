import sys, subprocess, pathlib
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans")
import fibsqrt_probe as P
base = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/R42CritProbe/env")
sim = str(base / "sim")
def run(name, content, ns):
    d = base / "c" / name; d.mkdir(parents=True, exist_ok=True)
    (d / "gates.txt").write_bytes(content.encode())
    return {n: subprocess.run([sim, str(n)], cwd=d, capture_output=True, text=True).stdout.strip() for n in ns}
# A: binary-op-only circuit, no copy/const lines, with trailing spaces
bin_ops = [f"out{k} = out0 & out0" for k in range(32, 64)]
print("A lf     ", run("a_lf", "\n".join(bin_ops) + "\n", [1]))
print("A trail  ", run("a_tr", "\n".join(l + " " for l in bin_ops) + "\n", [1]))
# B: only the final output-copy line carries a trailing space
last = P.L28[:-1] + [P.L28[-1] + " "]
print("B last-line-space", run("b", P.text(last), [48401, 41]))
print("B baseline       ", run("b0", P.text(P.L28), [48401, 41]))
# C: only the first 32 input self-copies carry a trailing space
first = [x + " " for x in P.L28[:32]] + P.L28[32:]
print("C first32-space  ", run("c", P.text(first), [41, 48401]))
# D: one interior AND line with a trailing space (should be harmless if binary parses)
mid = P.L28[:100] + [P.L28[100] + " "] + P.L28[101:]
print("D mid-and-space  ", run("d", P.text(mid), [41, 48401]))
