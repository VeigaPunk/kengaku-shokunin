import sys, subprocess, pathlib
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans")
import fibsqrt_probe as P
base = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/R42CritProbe/env")
f = base/"c"/"fake_sim"; f.mkdir(parents=True, exist_ok=True)
(f/"sim").write_text(P.FAKE_SIM); (f/"sim").chmod(0o755)
print("fake-sim 208/20000/41 =>", {n: subprocess.run([str(f/"sim"), str(n)], capture_output=True, text=True).stdout.strip() for n in (208, 20000, 41)})
print("expected =>", {n: P.answer(n) for n in (208, 20000, 41)})
e = base/"c"/"empty"; e.mkdir(parents=True, exist_ok=True); (e/"gates.txt").write_bytes(b"")
r = subprocess.run([str(base/"sim"), "41"], cwd=e, capture_output=True, text=True)
print("empty gates =>", repr(r.stdout), "rc", r.returncode, "stderr", repr(r.stderr))
