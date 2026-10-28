#!/usr/bin/env python3
"""Round-49 C2 pre-receipt control runner (wave-1 executor instrument, scratch-only).

Builds the three frozen controls of `plans/round-49-claims.md` §C2 on clones of the stage-1 freeze
`9d2900af41e4d1fc6022eff99010436fde6dbd93`, commits the candidate counter plus the control transform
into each clone, pins each control's ordering receipt with `plans/order_check.py`, and runs the
candidate with `--no-p10` (the frozen V8 fix: the gate's P10 fresh-probe leg is disabled pre-receipt).

Controls (frozen wording, §C2 "Controls that must print PREDICATE R49-C2 fail"):
  base   the base tree: no plans/polyglot_c_py_probe.py
  filler the round-46 filler package (plans/filler46/) scored via --filler
  echo   the echo receipt: the frozen dry table copied over the probe receipt path

Nothing here is the stage-2 pin. Exit 0 when all three controls print `PREDICATE R49-C2 fail`.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime, timezone

FREEZE = "9d2900af41e4d1fc6022eff99010436fde6dbd93"
COUNTER_REL = "plans/round49_c2_verify.py"
R46_RECEIPT = "corpus/evidence/round46/polyglot-c-py-probe.txt"
R49_RECEIPT = "corpus/evidence/round49/polyglot-c-py-probe.txt"
DRY = "corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt"
CLAIMS = "plans/round-49-claims.md"
ENV = None


def sh(argv, cwd=None):
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, capture_output=True, text=True, env=ENV)


def git(d, *a):
    r = sh(["git", "-C", str(d), *a])
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(a)} failed in {d}: {r.stderr.strip()[:400]}")
    return r.stdout.strip()


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def build(scratch, base, cand, name, transform):
    d = scratch / f"control-{name}" / "lane"
    d.parent.mkdir(parents=True, exist_ok=True)
    r = sh(["git", "clone", "--shared", "-q", str(base), str(d)])
    if r.returncode != 0:
        raise SystemExit(f"clone failed: {r.stderr.strip()[:400]}")
    top = git(d, "rev-parse", "--show-toplevel")
    if pathlib.Path(top).resolve() != d.resolve():
        raise SystemExit(f"clone top-level {top} != {d}")
    git(d, "config", "user.email", "r49c2execcontrols@localhost")
    git(d, "config", "user.name", "R49C2ExecControls")
    shutil.copyfile(cand, d / COUNTER_REL)
    git(d, "add", COUNTER_REL)
    git(d, "commit", "-q", "-m", "wave-1 control: round-49 C2 counter candidate (no stage-2 pin)")
    transform(d)
    commit = git(d, "rev-parse", "HEAD")
    diffstat = git(d, "show", "--stat", "--format=%s", commit)
    return d, commit, diffstat


def t_base(d):
    (d / "plans/polyglot_c_py_probe.py").unlink()
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "control transform: plans/polyglot_c_py_probe.py deleted (base tree, no probe)")


def t_filler(d):
    # the filler package is already committed at the freeze; --filler selects it at run time
    pass


def t_echo(d):
    shutil.copyfile(d / DRY, d / R46_RECEIPT)
    git(d, "add", R46_RECEIPT)
    git(d, "commit", "-q", "-m", "control transform: frozen dry table copied over the probe receipt path (echo)")


def order(d, receipt):
    r = sh([sys.executable, "plans/order_check.py", "--lane", str(d), "--claims", CLAIMS,
            "--receipt", receipt], cwd=d)
    lines = [f"ORDER receipt={receipt} exit={r.returncode}"]
    lines += [l for l in (r.stdout + r.stderr).splitlines() if l]
    return lines, r.returncode


def main(argv=None):
    global ENV
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--cand", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    scratch = pathlib.Path(a.scratch).resolve()
    base = pathlib.Path(a.base).resolve()
    cand = pathlib.Path(a.cand).resolve()
    out = pathlib.Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    import os
    ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(scratch))
    freeze_meta = git(base, "log", "-1", "--format=%H %cI %s", FREEZE)
    cand_sha = sha256(cand)
    summary = []
    controls = (
        ("base", t_base, []),
        ("filler", t_filler, ["--filler"]),
        ("echo", t_echo, []),
    )
    for name, transform, extra in controls:
        d, commit, diffstat = build(scratch, base, cand, name, transform)
        o46, rc46 = order(d, R46_RECEIPT)
        o49, rc49 = order(d, R49_RECEIPT)
        work = scratch / f"work-{name}"
        print(f"[{name}] running candidate on {d} at {commit}", flush=True)
        r = sh([sys.executable, COUNTER_REL, "--lane", str(d), "--work", str(work), "--no-p10", *extra], cwd=d)
        body = r.stdout.splitlines()
        header = [
            f"# control control-r49-c2-{name}: "
            + {"base": "base tree: plans/polyglot_c_py_probe.py deleted; gate run with P10 disabled",
               "filler": "the committed filler package plans/filler46/ scored as the package (--filler)",
               "echo": "the frozen dry table copied as the receipt (echo); gate run with P10 disabled"}[name],
            f"# measured tree: clone of lane {FREEZE} + committed transforms, run at {d}",
            f"# candidate counter {COUNTER_REL} sha256={cand_sha}",
            f"# transform: {commit} "
            + {"base": "plans/polyglot_c_py_probe.py deleted (base tree, no probe)",
               "filler": "none (filler package scored via --filler)",
               "echo": "frozen dry table copied over the probe receipt path (echo)"}[name],
        ]
        for line in diffstat.splitlines():
            header.append(f"# transform: {line}")
        header.append(f"# freeze {freeze_meta} (stage-1, {CLAIMS})")
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        receipt = header + o46 + o49 + [f"ORDER run_utc={now}"] + body + [f"# exit={r.returncode}"]
        if r.stderr.strip():
            receipt.append(f"# stderr: {r.stderr.strip().splitlines()[-1][:300]}")
        (out / f"control-{name}.txt").write_text("\n".join(receipt) + "\n")
        rev = next((l.split()[1] for l in body if l.startswith("REV ")), "?")
        checks = next((l for l in body if l.startswith("checks=")), "checks=?")
        content = next((l for l in body if l.startswith("content_defects=")), "content_defects=?")
        pred = next((l for l in body if l.startswith("PREDICATE ")), "PREDICATE ?")
        summary.append((name, commit, rev, checks, content, pred, r.returncode, rc46, rc49))
        print(f"[{name}] exit={r.returncode} {checks} {content} {pred} order46={rc46} order49={rc49}", flush=True)
    ok = all(s[5] == "PREDICATE R49-C2 fail" and s[6] == 1 for s in summary)
    for s in summary:
        print("SUMMARY " + " | ".join(str(x) for x in s))
    print(f"CONTROLS {'all-fail-as-required' if ok else 'NOT-ALL-FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
