#!/usr/bin/env python3
"""Build pristine and drop-commit-mutated battery modules via the counter's own --build-module
child (same bwrap shape as build_battery, lane hidden) and compare per-fixture HEAD tree hashes."""
import json, pathlib, shutil, subprocess

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/F42MutBattery")
LANE = S / "lane"
BAT = LANE / "plans" / "battery42"
BUILDER = S / "treeprobe_builder.py"
BUILDER.write_text((LANE / "plans" / "round42_c1_verify.py").read_text())
ENVV = "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/nonexistent " \
       "LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1"


def build(mod_src, tag):
    root = S / "treeprobe" / tag
    dest, tmp = root / "fx", root / "tmp"
    shutil.rmtree(root, ignore_errors=True)
    dest.mkdir(parents=True)
    tmp.mkdir()
    cmd = ["/usr/bin/bwrap", "--ro-bind", "/", "/", "--tmpfs", str(LANE),
           "--dev", "/dev", "--proc", "/proc", "--unshare-pid", "--unshare-net", "--unshare-ipc",
           "--tmpfs", "/run", "--die-with-parent", "--new-session",
           "--bind", str(dest), str(dest), "--bind", str(tmp), str(tmp), "--",
           "env", *ENVV.split(), "/usr/bin/python3", str(BUILDER),
           "--build-module", str(mod_src), "--dest", str(dest)]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(dest))
    assert r.returncode == 0, (tag, r.stderr[-400:])
    built = json.loads([l for l in r.stdout.splitlines() if l.startswith("BUILT ")][0][6:])
    out = {}
    for k, fx in enumerate(built):
        d = dest / f"f{k:03d}"
        repo = d / ("repo" if (d / "repo").is_dir() else "lane")
        t = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD^{tree}"],
                           capture_output=True, text=True)
        out[fx["fid"]] = t.stdout.strip()
    return out


pris = {}
for m in ["a_class.py", "a_route.py", "a_row.py", "o_clause.py"]:
    copy = S / "treeprobe" / f"pris_{m}"
    copy.parent.mkdir(parents=True, exist_ok=True)
    copy.write_text((BAT / m).read_text())
    pris.update(build(copy, "pris_" + m.replace(".py", "")))
for tag, mod in [("C02", "a_class.py"), ("C04", "a_class.py"), ("C06", "a_class.py"),
                 ("C08", "a_route.py"), ("C18", "a_row.py"), ("C20", "o_clause.py"),
                 ("C21", "o_clause.py"), ("C22", "o_clause.py")]:
    got = build(S / "cases" / tag / "battery42" / mod, tag)
    for fid, t in sorted(got.items()):
        mark = "TREE-EQUAL" if pris.get(fid) == t else "TREE-DIFFERS"
        print(f"{tag} {fid} {mark} pris={pris.get(fid, '?')[:12]} mut={t[:12]}")
