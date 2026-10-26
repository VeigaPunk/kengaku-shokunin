#!/usr/bin/env python3
"""From-nothing probe: can X2/X4/X5/X11 be killed WITHOUT a lane clone (the round-42 contract)?

Builds a two-row repo from nothing (a row that binds only by an explicit corpus/evidence path; a row
exempted by an erratum whose anchor token is a 32-hex short token), runs the unmodified anchor tool and
the four round-40 near-variants, and prints rc plus DEFECT lines. Also runs X3 as an unaffected control.
"""
import importlib.util
import hashlib
import json
import pathlib
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/R42CritEquiv")
HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/nonexistent",
       "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
       "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
       "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
       "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


tx = load("tx", LANE / ".ufo/waves/round-40/falsify/F40XMutAnchor/xmut_table.py")
XMUT = {r[0]: r for r in tx.MUTANTS}


def dig(b):
    return hashlib.sha256(b).hexdigest()


def build(root):
    r = root / "repo"
    if r.exists():
        import shutil
        shutil.rmtree(r)
    r.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "master", str(r)], env=ENV, check=True)
    # capture with no manifest entry: only the committed-bytes view exists
    (r / "corpus/evidence/fx/plain").mkdir(parents=True)
    body = b"row-path capture, no SHA256SUMS entry\n"
    (r / "corpus/evidence/fx/plain/base.log").write_bytes(body)
    h_plain = dig(body)
    # capture for the erratum-exempted row (manifest + bytes agree)
    (r / "corpus/evidence/fx/err").mkdir(parents=True)
    eb = b"erratum capture body\n"
    (r / "corpus/evidence/fx/err/test_outputs.py").write_bytes(eb)
    h_err = dig(eb)
    (r / "corpus/evidence/fx/err/SHA256SUMS").write_text(f"{h_err}  test_outputs.py\n")
    short = h_err[:32]
    (r / "corpus/lessons").mkdir(parents=True)
    (r / "corpus/lessons/round-37.md").write_text(
        f"Erratum (round 37): S921 anchor sha256 {short} was wrong; the capture's digest is sha256 {h_err} "
        f"(corpus/evidence/fx/err/SHA256SUMS).\n")
    (r / "corpus/SOURCES.md").write_text(
        HDR
        + f"| S920 | capture at corpus/evidence/fx/plain/base.log | code | A | fixture | sha256 {h_plain} | "
          "fixture row | mined | 2026-10-26 | 180d | corpus/knowledge/x.md |\n"
        + f"| S921 | capture at corpus/evidence/fx/err/test_outputs.py | code | A | fixture | sha256 {short} | "
          "fixture row | mined | 2026-10-26 | 180d | corpus/knowledge/x.md |\n")
    subprocess.run(["git", "-C", str(r), "add", "-A"], env=ENV, check=True)
    subprocess.run(["git", "-C", str(r), "commit", "-q", "-m", "fixture"], env=ENV, check=True)
    return r


def defects(text):
    return [(line.split()[1], dict(t.split("=", 1) for t in line.split() if "=" in t).get("class", "?"))
            for line in text.splitlines() if line.startswith("DEFECT ")]


def main():
    root = S / "fx_none"
    root.mkdir(parents=True, exist_ok=True)
    r = build(root)
    src = (LANE / "plans/anchor_digest_check.py").read_text()
    variants = {"REF": src}
    for mid in ("X2", "X3", "X4", "X5", "X11", "X1"):
        m = XMUT[mid]
        assert src.count(m[6]) == 1, mid
        variants[mid] = src.replace(m[6], m[7], 1)
    res = {}
    for name, text in variants.items():
        p = root / f"v_{name}.py"
        p.write_text(text)
        out = subprocess.run([sys.executable, str(p), "--lane", str(r)], cwd=str(root), env=ENV,
                             capture_output=True, text=True)
        ds = defects(out.stdout)
        res[name] = {"rc": out.returncode, "defects": ds, "stderr": out.stderr.strip()[-160:]}
        print(f"{name:4s} rc={out.returncode} defects={ds} {out.stderr.strip()[-100:]}")
    (S / "probe_none.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
