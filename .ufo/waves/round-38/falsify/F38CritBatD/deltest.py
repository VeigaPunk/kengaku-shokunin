import pathlib, shutil, subprocess, sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r38/F38CritBatD")
lane = S / "lane"
src = lane / "plans" / "battery38"


def drop(text, fid):
    lines = text.splitlines(True)
    out, i = [], 0
    while i < len(lines):
        if f'"fid": "{fid}"' in lines[i]:
            while i < len(lines) and not lines[i].rstrip().endswith("},"):
                i += 1
            i += 1
            continue
        out.append(lines[i])
        i += 1
    return "".join(out)


cases = [
    ("p4a.py", "p4a-second-row-line-outside", "N03"),
    ("p4a.py", "p4a-text-elsewhere", "N04"),
    ("p4b.py", "p4b-case-only", "N05"),
    ("p4b.py", "p4b-range-end-past-last", "N06"),
]
for mod, fid, mid in cases:
    d = S / f"bat-no-{fid}"
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(src, d)
    p = d / mod
    p.write_text(drop(p.read_text(), fid))
    assert f'"fid": "{fid}"' not in p.read_text(), fid
    r = subprocess.run([sys.executable, str(lane / "plans/round38_c1_verify.py"),
                        "--lane", str(lane), "--battery-dir", str(d), "--only", mid,
                        "--work", str(S / "w")], capture_output=True, text=True)
    keep = [l for l in r.stdout.splitlines()
            if l.startswith(("MUTANT", "BATTERY")) or "p4a" in l or "p4b" in l]
    print(f"### drop {fid} -> --only {mid} (exit={r.returncode})")
    print("\n".join(keep))
    print()

# both modules absent
d = S / "bat-no-p4ab"
shutil.rmtree(d, ignore_errors=True)
shutil.copytree(src, d)
for m in ("p4a.py", "p4b.py"):
    (d / m).unlink()
r = subprocess.run([sys.executable, str(lane / "plans/round38_c1_verify.py"),
                    "--lane", str(lane), "--battery-dir", str(d),
                    "--only", "N03,N04,N05,N06", "--work", str(S / "w")],
                   capture_output=True, text=True)
print(f"### p4a.py + p4b.py absent -> --only N03,N04,N05,N06 (exit={r.returncode})")
print("\n".join(l for l in r.stdout.splitlines() if l.startswith(("MUTANT", "BATTERY"))))
