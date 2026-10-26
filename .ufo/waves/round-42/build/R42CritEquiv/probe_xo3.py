#!/usr/bin/env python3
"""XO3 redundancy probe: how wide is the unique input of order_check clause 2?

A: receipt committed first and still present at the freeze -> clause 1 (freeze-contains-receipt) also fires.
B: receipt committed, removed, then the claims frozen (the witness shape) -> only clause 2 fires.
Prints the reference's ORDER FAIL lines and the XO3 mutant's rc for both, which is the whole argument:
the advertised clause-2 direction is reachable only on shape B.
"""
import pathlib
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/R42CritEquiv")
ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/nonexistent",
       "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
       "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
       "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
       "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}
CLAIMS = "plans/round-42-claims.md"
CDIR = ".ufo/waves/round-42/claims"
RECEIPT = "corpus/evidence/round42/probe.txt"
OLD = '        if freeze != receipt_commit and git.rc("merge-base", "--is-ancestor", receipt_commit, freeze) == 0:'
NEW = '        if False and freeze != receipt_commit and git.rc("merge-base", "--is-ancestor", receipt_commit, freeze) == 0:'


def git(r, *a):
    subprocess.run(["git", "-C", str(r), *a], env=ENV, check=True, capture_output=True)


def write(r, rel, text):
    p = r / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def build(root, name, remove):
    r = root / name
    if r.exists():
        import shutil
        shutil.rmtree(r)
    r.mkdir(parents=True)
    git(r, "init", "-q", "-b", "master")
    write(r, "README.md", "fixture\n")
    write(r, RECEIPT, "early receipt\n")
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "receipt first")
    if remove:
        git(r, "rm", "-q", RECEIPT)
        git(r, "commit", "-q", "-m", "receipt removed")
    write(r, CLAIMS, "# round 42 frozen claims\n")
    write(r, CDIR + "/control.txt", "P10 DEFECT receipt unreadable\n")
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "freeze")
    if remove:
        write(r, RECEIPT, "probe receipt\n")
        git(r, "add", "-A")
        git(r, "commit", "-q", "-m", "receipt again")
    git(r, "log", "--oneline")
    return r


def main():
    root = S / "fx_xo3"
    root.mkdir(parents=True, exist_ok=True)
    src = (LANE / "plans/order_check.py").read_text()
    assert src.count(OLD) == 1
    mut = root / "v_XO3.py"
    mut.write_text(src.replace(OLD, NEW, 1))
    for shape, remove in (("A-receipt-present-at-freeze", False), ("B-receipt-removed-then-freeze", True)):
        r = build(root, shape, remove)
        argv = ["--lane", str(r), "--claims", CLAIMS, "--receipt", RECEIPT]
        for label, tool in (("REF", LANE / "plans/order_check.py"), ("XO3", mut)):
            out = subprocess.run([sys.executable, str(tool)] + argv, cwd=str(root), env=ENV,
                                 capture_output=True, text=True)
            fails = [l for l in out.stdout.splitlines() if "FAIL" in l or l.startswith("ORDER HIT")]
            print(f"{shape} {label:3s} rc={out.returncode} {fails}")


if __name__ == "__main__":
    main()
