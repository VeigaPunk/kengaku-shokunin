"""Delete one p6 fixture at a time and show the matching mutant flip to SURVIVED (R37BatP6 evidence)."""
import pathlib, subprocess, sys, os

S = pathlib.Path(sys.argv[1])
lane = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
src = lane / ".ufo/waves/round-37/build/R37BatP6/battery/p6.py"
fids = [("M20", "p6-m20-registry-row-duplicated"), ("M21", "p6-m21-row-with-twelve-cells"),
        ("M22", "p6-m22-url-off-the-pinned-raw-path"), ("M23", "p6-m23-row-tier-b"),
        ("M24", "p6-m24-row-status-queued"), ("M25", "p6-m25-used-by-another-path"),
        ("M26", "p6-m26-five-word-teaches-cell"), ("M27", "p6-m27-two-identical-teaches-cells")]


def wrapper(drop):
    return ("import importlib.util\n"
            f"_s = importlib.util.spec_from_file_location('p6_base', r'{src}')\n"
            "_m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)\n"
            f"FIXTURES = [f for f in _m.FIXTURES if f['fid'] != {drop!r}]\n")


for mid, fid in fids + [("ALL", "none-of-them")]:
    d = S / "load" / mid
    d.mkdir(parents=True, exist_ok=True)
    (d / "p6_trimmed.py").write_text(wrapper(fid))
    only = mid if mid != "ALL" else "M20,M21,M22,M23,M24,M25,M26,M27"
    r = subprocess.run([sys.executable, "plans/round37_c1_verify.py", "--lane", ".", "--battery-dir", str(d),
                        "--only", only, "--work", str(S / "work")],
                       cwd=lane, capture_output=True, text=True, env={**os.environ, "TMPDIR": str(S)})
    out = r.stdout.splitlines()
    print(f"== dropped {fid}  (--only {only})")
    print("\n".join(l for l in out if l.startswith(("BATTERY", "MUTANT"))))
    print(f"exit={r.returncode}")
    if r.returncode not in (0, 1):
        print("STDERR", r.stderr[-800:])
