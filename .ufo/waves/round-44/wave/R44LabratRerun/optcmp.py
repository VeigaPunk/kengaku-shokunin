#!/usr/bin/env python3
"""R44LabratRerun extra: does the oracle's result depend on -O3? Rebuild in a bwrap sandbox at a chosen -O level.

  python3 optcmp.py --opt 3 --label o3 --work <dir>
  python3 optcmp.py --opt 0 --label o0 --work <dir>
  python3 optcmp.py --opt 0 --label o0-atk --work <dir> --donor <dir of a previous o3 run>   # attack-only

mode "oracle" (no --donor): replay Dockerfile:6-11 at -O<opt> (feal, decrypt, gen.py, rm orig_plaintexts.txt,
rm gen.py), then run the published solve.sh (attack.c compiled at -O<opt>).
mode "attack" (--donor): copy pairs.txt/ciphertexts.txt from the donor, compile decrypt at -O<opt>, run solve.sh.

Prints: rc, sha256 of /app/plaintexts.txt, the attack's `Found ...` lines (recovered round keys), the count of
decimal lines, and the count of `Maybe` lines. The /app tree stays in <work>/app for cmp across levels.
"""
import argparse
import hashlib
import pathlib
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
CAP = LANE + "/corpus/evidence/round44/tb2-feal-linear-cryptanalysis"
CAP0 = "/fast/scratch/hyaku/kengaku-r44/R44LabratRerun/opt0/cap"
BWRAP = "/usr/bin/bwrap"
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
       "PYTHONDONTWRITEBYTECODE": "1"}


def sandbox_argv(work):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        p = pathlib.Path(link)
        if p.is_symlink():
            argv += ["--symlink", str(p.readlink()), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--bind", str(work / "app"), "/app", "--dir", "/pub",
             "--ro-bind", str(work / "solve.sh"), "/pub/solve.sh",
             "--ro-bind", str(work / "all.sh"), "/all.sh", "--chdir", "/app"]
    return argv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--opt", type=int, choices=(0, 3), required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--donor", default=None)
    a = ap.parse_args()
    cap = CAP0 if a.opt == 0 else CAP
    root = pathlib.Path(a.work)
    work = pathlib.Path(tempfile.mkdtemp(prefix="optcmp-" + a.label + "-", dir=root))
    app = work / "app"
    app.mkdir()
    for name in ("feal.c", "decrypt.c", "gen.py"):
        shutil.copyfile(cap + "/" + name, app / name)
    shutil.copyfile(cap + "/solve.sh", work / "solve.sh")
    steps = []
    if a.donor:
        for name in ("pairs.txt", "ciphertexts.txt"):
            shutil.copyfile(pathlib.Path(a.donor) / "app" / name, app / name)
        steps.append(f"gcc -O{a.opt} -o decrypt decrypt.c")
    else:
        steps += [f"gcc -O{a.opt} -o feal feal.c", f"gcc -O{a.opt} -o decrypt decrypt.c",
                  "python3 gen.py >/dev/null", "rm orig_plaintexts.txt", "rm gen.py"]
    steps.append("bash /pub/solve.sh >/dev/null 2>&1")
    (work / "all.sh").write_text("\n".join(steps) + "\n")
    p = subprocess.run(sandbox_argv(work) + ["/bin/bash", "-euo", "pipefail", "/all.sh"],
                       env=ENV, capture_output=True, text=True, timeout=1800)
    out = app / "plaintexts.txt"
    lines = out.read_text().splitlines() if out.exists() else []
    found = [l for l in lines if l.startswith("Found ")]
    dec = [l for l in lines if l.isdigit()]
    maybe = [l for l in lines if l.startswith("Maybe ")]
    print(f"OPT {a.label} opt=-O{a.opt} mode={'attack' if a.donor else 'oracle'} rc={p.returncode}"
          f" plaintexts={'absent' if not out.exists() else 'sha256=' + hashlib.sha256(out.read_bytes()).hexdigest()}"
          f" lines={len(lines)} decimals={len(dec)} maybe={len(maybe)}")
    for l in found:
        print(f"FOUND {a.label} {l}")
    if p.returncode:
        print("STDERR " + p.stderr[:400], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
