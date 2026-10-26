#!/usr/bin/env python3
"""Label-swap probe: X6 and X7 change only the printed class, never the exit code.

One from-nothing repo, two rows: S930 anchored on a sibling capture's committed digest (reference:
digest-wrong-capture) and S931 anchored on a made-up 64-hex token (reference: digest-unknown). Prints
rc and the DEFECT classes for the reference, X6 and X7.
"""
import hashlib
import importlib.util
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
    a = b"capture A (the row's own)\n"
    b = b"capture B (a sibling's)\n"
    for name, body in (("a", a), ("b", b)):
        (r / f"corpus/evidence/fx/{name}").mkdir(parents=True)
        (r / f"corpus/evidence/fx/{name}/test_outputs.py").write_bytes(body)
        (r / f"corpus/evidence/fx/{name}/SHA256SUMS").write_text(
            f"{dig(body)}  test_outputs.py\n")
    made_up = dig(b"a token committed nowhere\n")
    (r / "corpus/SOURCES.md").write_text(
        HDR
        + f"| S930 | capture at corpus/evidence/fx/a/test_outputs.py | code | A | fixture | sha256 {dig(b)} | "
          "fixture row | mined | 2026-10-26 | 180d | corpus/knowledge/x.md |\n"
        + f"| S931 | capture at corpus/evidence/fx/a/test_outputs.py | code | A | fixture | sha256 {made_up} | "
          "fixture row | mined | 2026-10-26 | 180d | corpus/knowledge/x.md |\n")
    subprocess.run(["git", "-C", str(r), "add", "-A"], env=ENV, check=True)
    subprocess.run(["git", "-C", str(r), "commit", "-q", "-m", "fixture"], env=ENV, check=True)
    return r


def clss(text):
    return [dict(t.split("=", 1) for t in line.split() if "=" in t).get("class", "?")
            for line in text.splitlines() if line.startswith("DEFECT ")]


def main():
    root = S / "fx_lbl"
    root.mkdir(parents=True, exist_ok=True)
    r = build(root)
    src = (LANE / "plans/anchor_digest_check.py").read_text()
    variants = {"REF": src}
    for mid in ("X6", "X7"):
        m = XMUT[mid]
        variants[mid] = src.replace(m[6], m[7], 1)
    res = {}
    for name, text in variants.items():
        p = root / f"v_{name}.py"
        p.write_text(text)
        out = subprocess.run([sys.executable, str(p), "--lane", str(r)], cwd=str(root), env=ENV,
                             capture_output=True, text=True)
        res[name] = {"rc": out.returncode, "classes": clss(out.stdout)}
        print(f"{name:4s} rc={out.returncode} classes={clss(out.stdout)}")
    (S / "probe_lbl.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
