#!/usr/bin/env python3
"""Witness fixtures for surviving near-variant mutants — seat F40XMutAnchor, round-40 wave 2 (FALSIFY).

For each survivor: build a minimal one-row git repo in scratch, run the reference tool and the mutant
variant on it, and record the (ref rc, ref classes) -> (mut rc, mut classes) delta in the mutant's
declared direction. Receipts land in $S/wit/<witness>.{ref,xmut}.out and wit-summary.json.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r40/F40XMutAnchor")
REF = S / "lane/plans/anchor_digest_check.py"
XMUT = S / "xmut"
OUT = S / "wit"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
ENV = {
    "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
    "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
    "PYTHONDONTWRITEBYTECODE": "1",
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_COUNT": "2",
    "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
    "GIT_AUTHOR_NAME": "witness", "GIT_AUTHOR_EMAIL": "witness@kengaku.invalid",
    "GIT_COMMITTER_NAME": "witness", "GIT_COMMITTER_EMAIL": "witness@kengaku.invalid",
    "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00",
    "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00",
}


def sh(*argv, cwd=None, check=True):
    r = subprocess.run([str(a) for a in argv], cwd=str(cwd) if cwd else None, env=ENV,
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(map(str, argv[:3]))} rc={r.returncode}: {r.stderr.strip()[-300:]}")
    return r


def repo(name):
    d = OUT / name
    d.mkdir(parents=True, exist_ok=True)
    sh("git", "-C", d, "init", "-q", "-b", "master")
    return d


def commit(d, msg="witness"):
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "commit", "-q", "-m", msg)


def dig(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def row(sid, source, anchor, teaches="witness row"):
    return (f"| {sid} | {source} | code | A | witness | sha256 {anchor} | {teaches} | mined | "
            "2026-10-26 | 180d | corpus/knowledge/x.md |")


def capture(d, reldir, body, name="test_outputs.py", sums=True, toml=None):
    cap = d / "corpus/evidence" / reldir
    cap.mkdir(parents=True, exist_ok=True)
    (cap / name).write_bytes(body)
    h = hashlib.sha256(body).hexdigest()
    if sums:
        (cap / "SHA256SUMS").write_text(f"{h}  {name}\n")
    if toml is not None:
        (cap / "task.toml").write_text(toml)
    return h


def classes(out):
    got = set()
    for line in out.splitlines():
        if line.startswith("DEFECT "):
            got.update(re.findall(r"\bclass=(\S+)", line))
    return frozenset(got)


def run(tool, d, extra=()):
    r = subprocess.run([sys.executable, str(tool), "--lane", str(d), *extra], env=ENV,
                       capture_output=True, text=True)
    return r.returncode, classes(r.stdout)


def w1():
    """X1 (provenance-row route removed): PROVENANCE.md binds the row by ticked file only, no URL."""
    d = repo("w1")
    h = capture(d, "round41/anchor-captures", b"w1 capture body\n", name="capture.txt")
    (d / "corpus/evidence/round41/anchor-captures/PROVENANCE.md").write_text(
        "| sid | file | note |\n|---|---|---|\n"
        "| S900 | `capture.txt` | captured beside this table; the table carries no pinned URL |\n")
    (d / "corpus/SOURCES.md").write_text(
        HDR + row("S900", "WebArena task generator, captured beside PROVENANCE.md", h) + "\n")
    commit(d)
    return d, []


def w3():
    """X3 (provenance-url fallback removed): row URL matches PROVENANCE.md, no task.toml slug anywhere."""
    d = repo("w3")
    h = capture(d, "round41/w3cap", b"w3 capture body\n")
    url = f"https://raw.githubusercontent.com/o/r/{PIN}/plain-cap/tests/test_outputs.py"
    (d / "corpus/evidence/round41/w3cap/PROVENANCE.md").write_text(
        "| url | file |\n|---|---|---|\n"
        f"| {url} | `test_outputs.py` | pinned upstream file, no row id in this table |\n")
    (d / "corpus/SOURCES.md").write_text(HDR + row("S901", f"pinned at {url}", h) + "\n")
    commit(d)
    return d, []


def w6():
    """X6 (digest-wrong-capture gate off): row anchored on a sibling capture's committed digest."""
    d = repo("w6")
    capture(d, "round41/w6a", b"w6 capture A\n")
    db = capture(d, "round41/w6b", b"w6 capture B\n")
    (d / "corpus/SOURCES.md").write_text(
        HDR + row("S902", "capture A at corpus/evidence/round41/w6a/test_outputs.py", db) + "\n")
    commit(d)
    return d, []


def w7():
    """X7 (digest-unknown mislabelled): row anchored on a made-up 64-hex digest."""
    d = repo("w7")
    capture(d, "round41/w7", b"w7 capture\n")
    bogus = hashlib.sha256(b"w7 made-up token\n").hexdigest()
    (d / "corpus/SOURCES.md").write_text(
        HDR + row("S903", "capture at corpus/evidence/round41/w7/test_outputs.py", bogus) + "\n")
    commit(d)
    return d, []


def w9():
    """X9 (row-malformed != -> >): a 10-cell row (used-by cell dropped) is no longer malformed."""
    d = repo("w9")
    h = capture(d, "round41/w9", b"w9 capture\n")
    r = row("S909", "capture at corpus/evidence/round41/w9/test_outputs.py", h)
    cells = r.split("|")
    short = "|".join(cells[:-2]) + "|"
    (d / "corpus/SOURCES.md").write_text(HDR + short + "\n")
    commit(d)
    return d, []


def w11():
    """X11 (committed-bytes view dropped): anchor = blob digest while the manifest entry is stale."""
    d = repo("w11")
    stale = hashlib.sha256(b"w11 manifest view, not the capture bytes\n").hexdigest()
    cap = d / "corpus/evidence/round41/w11"
    cap.mkdir(parents=True)
    (cap / "test_outputs.py").write_bytes(b"w11 capture bytes\n")
    db = dig(cap / "test_outputs.py")
    (cap / "SHA256SUMS").write_text(f"{stale}  test_outputs.py\n")
    (d / "corpus/SOURCES.md").write_text(
        HDR + row("S904", "capture at corpus/evidence/round41/w11/test_outputs.py", db) + "\n")
    commit(d)
    return d, []


def w12():
    """X12 (slash-less task.toml name fallback dropped): name = "plain-slug"."""
    d = repo("w12")
    h = capture(d, "round41/w12", b"w12 capture\n", toml='name = "plain-slug"\n')
    url = f"https://raw.githubusercontent.com/o/r/{PIN}/plain-slug/tests/test_outputs.py"
    (d / "corpus/SOURCES.md").write_text(HDR + row("S905", f"pinned at {url}", h) + "\n")
    commit(d)
    return d, []


def w13():
    """X13 (default evidence-ref flipped to index): capture staged beyond HEAD, default ref."""
    d = repo("w13")
    cap = d / "corpus/evidence/round41/w13"
    cap.mkdir(parents=True)
    (cap / "test_outputs.py").write_bytes(b"w13 committed view\n")
    d1 = dig(cap / "test_outputs.py")
    (cap / "SHA256SUMS").write_text(f"{d1}  test_outputs.py\n")
    (d / "corpus/SOURCES.md").write_text(
        HDR + row("S906", "capture at corpus/evidence/round41/w13/test_outputs.py", d1) + "\n")
    commit(d)
    (cap / "test_outputs.py").write_bytes(b"w13 staged view\n")
    d2 = dig(cap / "test_outputs.py")
    (cap / "SHA256SUMS").write_text(f"{d2}  test_outputs.py\n")
    sh("git", "-C", d, "add", "-A")  # staged, not committed
    # the row (working tree) claims the STAGED digest; the tool reads SOURCES.md from the work tree
    (d / "corpus/SOURCES.md").write_text(
        HDR + row("S906", "capture at corpus/evidence/round41/w13/test_outputs.py", d2) + "\n")
    return d, []


def w14():
    """X14 (erratum token scan narrowed to lowercase): uppercase non-committed token on the erratum line."""
    d = repo("w14")
    h = capture(d, "round41/w14", b"w14 capture\n")
    upper = hashlib.sha256(b"w14 bogus uppercase\n").hexdigest().upper()
    (d / "corpus/lessons").mkdir(parents=True)
    (d / "corpus/lessons/round-37.md").write_text(
        f"Erratum (round 37): S907 anchor sha256 {upper} is committed nowhere; the capture's digest is "
        f"sha256 {h} (corpus/evidence/round41/w14/SHA256SUMS).\n")
    (d / "corpus/SOURCES.md").write_text(
        HDR + row("S907", "capture at corpus/evidence/round41/w14/test_outputs.py", h) + "\n")
    commit(d)
    return d, []


def w15():
    """X15 (erratum correction scoped to global A): correction cites a sibling row's committed digest."""
    d = repo("w15")
    capture(d, "round41/w15a", b"w15 capture A\n")
    db = capture(d, "round41/w15b", b"w15 capture B (sibling row's capture)\n")
    w = hashlib.sha256(b"w15 made-up wrong token\n").hexdigest()
    (d / "corpus/lessons").mkdir(parents=True)
    (d / "corpus/lessons/round-37.md").write_text(
        f"Erratum (round 37): S908 anchor sha256 {w} was wrong; the capture's digest is sha256 {db} "
        f"(corpus/evidence/round41/w15b/SHA256SUMS).\n")
    (d / "corpus/SOURCES.md").write_text(
        HDR + row("S908", "capture A at corpus/evidence/round41/w15a/test_outputs.py", w) + "\n")
    commit(d)
    return d, []


WITNESSES = [
    ("w1-provrow-only", w1, "X1", "rc-mirror"),
    ("w3-provurl-fallback", w3, "X3", "rc-mirror"),
    ("w6-wrong-capture-class", w6, "X6", "silence/digest-wrong-capture"),
    ("w7-unknown-class", w7, "X7", "silence/digest-unknown"),
    ("w9-short-row", w9, "X9", "rc-silence"),
    ("w11-blob-view", w11, "X11", "rc-mirror"),
    ("w12-slashless-slug", w12, "X12", "rc-mirror"),
    ("w13-default-ref-index", w13, "X13", "rc-silence"),
    ("w14-erratum-upper", w14, "X14", "silence/erratum-digest-unresolved"),
    ("w15-erratum-global-A", w15, "X15", "rc-silence"),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    summary = []
    for name, build, mid, direction in WITNESSES:
        d, _ = build()
        rrc, rcls = run(REF, d)
        (OUT / f"{name}.ref.out").write_text(
            f"rc={rrc}\n" + subprocess.run([sys.executable, str(REF), "--lane", str(d), "--verbose"],
                                           env=ENV, capture_output=True, text=True).stdout,
            encoding="utf-8")
        mrc, mcls = run(XMUT / f"{mid}.py", d)
        (OUT / f"{name}.{mid}.out").write_text(
            f"rc={mrc}\n" + subprocess.run([sys.executable, str(XMUT / f"{mid}.py"), "--lane", str(d),
                                            "--verbose"], env=ENV, capture_output=True, text=True).stdout,
            encoding="utf-8")
        hit = {"rc-mirror": rrc == 0 and mrc == 1,
               "rc-silence": rrc == 1 and mrc == 0}.get(direction.split("/")[0])
        if direction.startswith("silence/"):
            cls = direction.split("/")[1]
            hit = cls in rcls and cls not in mcls
        summary.append({"witness": name, "mutant": mid, "direction": direction,
                        "ref_rc": rrc, "ref_classes": sorted(rcls),
                        "mut_rc": mrc, "mut_classes": sorted(mcls), "kills": bool(hit)})
        print(f"WITNESS {name} mutant={mid} dir={direction} ref=rc{rrc}/{','.join(sorted(rcls)) or '-'}"
              f" mut=rc{mrc}/{','.join(sorted(mcls)) or '-'} kills={bool(hit)}")
    (OUT / "wit-summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
