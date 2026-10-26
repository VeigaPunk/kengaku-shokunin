#!/usr/bin/env python3
"""F39IndepProbe (kengaku round 39, wave 2): six extra end states for the pinned TB2 `git-leak-recovery`
grader, run through the frozen round-39 C2 probe.

This file is an extension, not a rewrite: it imports the lane's frozen `plans/git_leak_probe.py`
(sha256 4961a50f28ae85e8d8b687d3623aef29b59d4db14c0e62e5244e48cfef8cf68c) and reuses its pin check,
bubblewrap argument construction, per-case workspace and `run_case()` unchanged, so the captures, the
sandbox and the five grader calls are the probe's own. Only two things are added:

  * six `Case`s outside the frozen 25 (refs/replace, packed-refs only, a linked worktree, a `.git` gitfile,
    a secret in a tree entry name, the reflog of a deleted branch), predictions frozen beforehand in
    `.ufo/waves/round-39/falsify/F39IndepProbe/predictions-before-run.txt`;
  * an independent sweep appended to the harness AFTER the five grader calls (PROBE lines): every object in
    the store searched with `cat-file --batch-all-objects --batch`, tree entry names, plaintext under /app,
    the exact T5 checksum command, the fsck dangling count, `git log --reflog -p -S secret[`, the ref list and
    whether `.git` is a gitfile. It never touches the grader's verdict; it separates "the grader's letters"
    from "the secret is still in the repository".

Usage: probe_extra.py <lane-at-tip> <work-parent>
"""
from __future__ import annotations

import importlib.util
import pathlib
import shutil
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
WORK = pathlib.Path(sys.argv[2]).resolve()
spec = importlib.util.spec_from_file_location("glr_probe", LANE / "plans" / "git_leak_probe.py")
m = importlib.util.module_from_spec(spec)
sys.modules["glr_probe"] = m  # dataclasses in the imported probe resolve their class module
spec.loader.exec_module(m)

TESTS = m.TESTS
SECRET = m.SECRET
FLAG = m.FLAG
CLEAN = m.CLEAN
r = m.r

EXTRA_HARNESS = r'''

# ---- F39IndepProbe independent sweep (added after the five grader calls; not part of the grader) ----
import os
REPO = "/app/repo"


def g(argv):
    try:
        return subprocess.run(["git", "-C", REPO] + argv, cwd="/app", stdin=subprocess.DEVNULL,
                              capture_output=True)
    except OSError:
        return None


def p(k, v):
    print("PROBE " + k + "=" + str(v))


p("gitfile", "yes" if os.path.isfile("/app/repo/.git") else ("no" if os.path.isdir("/app/repo/.git") else "absent"))
_r = g(["rev-parse", "--absolute-git-dir"])
p("gitdir", _r.stdout.decode(errors="replace").strip() if _r is not None and _r.returncode == 0 else "-")
_r = g(["for-each-ref", "--format=%(refname)"])
p("refs", ",".join(sorted(_r.stdout.decode(errors="replace").split()))
  if _r is not None and _r.returncode == 0 and _r.stdout.strip() else "-")
_r = g(["cat-file", "--batch-all-objects", "--batch"])
_hits = {"blob": 0, "commit": 0, "tree": 0}
_total = 0
_names = 0
if _r is not None and _r.returncode == 0:
    _b = _r.stdout
    _i = 0
    while _i < len(_b):
        _nl = _b.find(b"\n", _i)
        if _nl < 0:
            break
        _h = _b[_i:_nl].split()
        if len(_h) != 3 or _h[1] not in (b"blob", b"commit", b"tree"):
            break
        _typ = _h[1].decode()
        _size = int(_h[2])
        _body = _b[_nl + 1:_nl + 1 + _size]
        _i = _nl + 1 + _size + 1
        _total += 1
        if b"secret[" in _body:
            _hits[_typ] = _hits.get(_typ, 0) + 1
p("objects", _total)
# tree entry NAMES: the raw tree body is binary (20-byte ids), so read the pretty form per tree object
_nr = g(["cat-file", "--batch-all-objects", "--batch-check=%(objectname) %(objecttype)"])
if _nr is not None and _nr.returncode == 0:
    for _line in _nr.stdout.decode(errors="replace").splitlines():
        _f = _line.split()
        if len(_f) == 2 and _f[1] == "tree":
            _t = g(["cat-file", "-p", _f[0]])
            if _t is not None and _t.returncode == 0:
                for _e in _t.stdout.decode(errors="replace").splitlines():
                    _sp = _e.split("\t", 1)
                    if len(_sp) == 2 and "secret[" in _sp[1]:
                        _names += 1
p("object_hits", "blob=%d commit=%d tree=%d" % (_hits["blob"], _hits["commit"], _hits["tree"]))
p("tree_name_hits", _names)
_r = g(["fsck", "--lost-found"])
p("dangling", len([_l for _l in _r.stdout.decode(errors="replace").splitlines() if "dangling" in _l])
  if _r is not None and _r.returncode == 0 else "-")
_r = g(["log", "--reflog", "-p", "-S", "secret["])
p("reflog", "yes" if _r is not None and _r.returncode == 0 and b"secret[" in _r.stdout else "no")
_pat = "*/" + chr(92) + ".*"
_cs = subprocess.run(["sh", "-c", "find /app/repo -type f -not -path '" + _pat
                     + "' -exec sha256sum {} + | sort | sha256sum"], capture_output=True, text=True)
p("checksum", _cs.stdout.split()[0] if _cs.returncode == 0 and _cs.stdout.split() else "-")
_wk = []
for _root, _dirs, _files in os.walk("/app"):
    for _f in _files:
        _fp = os.path.join(_root, _f)
        if _fp == "/app/secret.txt":
            continue
        try:
            with open(_fp, "rb") as _fh:
                _data = _fh.read()
        except OSError:
            continue
        if b"secret[" in _data:
            _wk.append(_fp)
p("work_hits", len(_wk))
p("work_paths", ",".join(sorted(_wk)) if _wk else "-")
'''
# the closing guard above is a no-op because the frozen probe has no trailing code after HARNESS_PY formatting
m.HARNESS_PY = m.HARNESS_PY + EXTRA_HARNESS

CASES = [
    m.Case("replace-ref-pins-secret-commit",
           r(CLEAN, FLAG, "cd /app/repo",
             f"SB=$(printf '%s\\n' '{SECRET}' | git hash-object -w --stdin)",
             "ST=$(printf '100644 blob %s\\tsecret.txt\\n' \"$SB\" | git mktree)",
             "B=$(git commit-tree \"$ST\" -m 'chore: notes')",
             "P=$(git commit-tree \"$(git rev-parse 'HEAD^{tree}')\" -m 'chore: placeholder')",
             "git update-ref \"refs/replace/$P\" \"$B\""),
           "PFPPP", ("secret-gone",),
           "after the cleanup: a secret-bearing commit pinned as the replacement of an unreferenced commit; "
           "prediction T2 F because --all is all refs in refs/ and refs/replace is one of them"),
    m.Case("packed-refs-only-leak",
           r(CLEAN, FLAG, "cd /app/repo",
             f"SB=$(printf '%s\\n' '{SECRET}' | git hash-object -w --stdin)",
             "ST=$(printf '100644 blob %s\\tsecret.txt\\n' \"$SB\" | git mktree)",
             "B=$(git commit-tree \"$ST\" -p HEAD -m 'chore: notes')",
             "git update-ref refs/heads/keep \"$B\"",
             "git pack-refs --all --prune",
             "test ! -e .git/refs/heads/keep"),
           "PFPPP", ("secret-gone",),
           "after the cleanup: the secret commit is reachable only through a branch that exists solely in "
           ".git/packed-refs; prediction T2 F (packed-refs is the same namespace --all reads)"),
    m.Case("detached-worktree-secret",
           r(CLEAN, FLAG, "cd /app/repo",
             f"SB=$(printf '%s\\n' '{SECRET}' | git hash-object -w --stdin)",
             "ST=$(printf '100644 blob %s\\tsecret.txt\\n' \"$SB\" | git mktree)",
             "B=$(git commit-tree \"$ST\" -m 'chore: notes')",
             "git worktree add -q --detach /app/wt \"$B\""),
           "PPPPP", ("secret-gone",),
           "after the cleanup: the secret commit is checked out in a linked worktree at /app/wt (detached "
           "HEAD, no refs/ entry); prediction PPPPP with /app/wt/secret.txt on disk"),
    m.Case("gitfile-separate-store-dangling-blob",
           r(CLEAN, FLAG, "cd /app/repo",
             "mv .git /app/meta",
             "printf 'gitdir: /app/meta\\n' > .git",
             f"printf '%s\\n' '{SECRET}' | git hash-object -w --stdin",
             "test -f .git"),
           "PPPFP", ("secret-gone",),
           "after the cleanup: .git is a one-line gitfile to /app/meta and a loose secret blob is written "
           "through it; prediction T4 F (the grader's git commands follow the gitfile), T5 P"),
    m.Case("tree-name-secret",
           r(CLEAN, FLAG, "cd /app/repo",
             "SB=$(printf 'x\\n' | git hash-object -w --stdin)",
             "ST=$(printf '100644 blob %s\\tsecret[lost_and_found_in_git]\\n' \"$SB\" | git mktree)",
             "B=$(git commit-tree \"$ST\" -p HEAD -m 'chore: add notes')",
             "git update-ref refs/heads/keep \"$B\""),
           "PPPPP", ("secret-gone",),
           "after the cleanup: a reachable branch adds a file whose NAME is the literal secret and whose "
           "content is 'x'; prediction PPPPP (pickaxe reads changed lines, not tree names)"),
    m.Case("deleted-branch-reflog",
           r(CLEAN, FLAG, "cd /app/repo",
             "git checkout -q -b tmp",
             f"SB=$(printf '%s\\n' '{SECRET}' | git hash-object -w --stdin)",
             "git update-index --add --cacheinfo \"100644,$SB,secret.txt\"",
             "git commit -q -m 'chore: notes'",
             "git checkout -q -",
             "git branch -D tmp"),
           "PPPPP", ("secret-gone",),
           "after the cleanup: the secret commit lived on a temporary branch, which is deleted; only the HEAD "
           "reflog's checkout entry still names it (the work tree never held the file); prediction PPPPP"),
]


def main():
    for name, digest in m.PINS.items():
        if not (LANE / m.CAP / name).is_file() or m.sha256(LANE / m.CAP / name) != digest:
            print(f"SETUP capture {name} not at its pinned digest", file=sys.stderr)
            return 2
    cap = LANE / m.CAP
    runs = []
    for run in (1, 2):
        printed = []
        rows = {}
        root = pathlib.Path(tempfile.mkdtemp(prefix="k39x-", dir=WORK))
        try:
            for c in CASES:
                rc, out = m.run_case(cap, root, c, "grade")
                got = {}
                probe = {}
                stages = []
                for line in out.splitlines():
                    parts = line.split()
                    if not parts:
                        continue
                    if parts[0] == "TEST" and len(parts) >= 3 and parts[1] in TESTS:
                        got[parts[1]] = parts[2]
                    elif parts[0] == "PROBE" and "=" in line:
                        k, v = line.split("=", 1)
                        probe[k.split()[1]] = v
                    elif parts[0] == "STAGE":
                        stages.append(line)
                if rc != 0 or set(got) != set(TESTS):
                    print(f"SETUP case {c.cid} no five verdicts rc={rc} {' '.join(stages)}", file=sys.stderr)
                    print(out, file=sys.stderr)
                    return 2
                letters = "".join(got[t] for t in TESTS)
                rows[c.cid] = letters
                printed.append(
                    f"CASE {c.cid} predicted={m.overall(c.predicted)} observed={m.overall(letters)}"
                    f" tests={letters} predicted_tests={c.predicted}"
                    f" match={'yes' if letters == c.predicted else 'NO'}"
                    f" objects={probe.get('object_hits', '-')} tree_names={probe.get('tree_name_hits', '-')}"
                    f" work_hits={probe.get('work_hits', '-')} paths={probe.get('work_paths', '-')}"
                    f" dangling={probe.get('dangling', '-')} reflog={probe.get('reflog', '-')}"
                    f" checksum={probe.get('checksum', '-')} gitfile={probe.get('gitfile', '-')}"
                    f" gitdir={probe.get('gitdir', '-')} refs={probe.get('refs', '-')}"
                    f" violates={','.join(c.violates)} -- {c.requirement}")
        finally:
            shutil.rmtree(root, ignore_errors=True)
        runs.append((rows, printed))
    print("# F39IndepProbe: six extra states, frozen round-39 probe machinery @ lane tip")
    print(f"# probe plans/git_leak_probe.py sha256={m.sha256(LANE / 'plans' / 'git_leak_probe.py')}")
    for name in sorted(m.PINS):
        print(f"# capture {name} sha256={m.PINS[name]}")
    for line in runs[0][1]:
        print(line)
    agree = sum(rows.get(c.cid) == c.predicted for c in CASES for rows in (runs[0][0],))
    print(f"cases={len(CASES)} predicted_pass={sum(m.overall(c.predicted) == 'pass' for c in CASES)}"
          f" predicted_fail={sum(m.overall(c.predicted) == 'fail' for c in CASES)}"
          f" agree={agree} mismatch={len(CASES) - agree}")
    same = runs[0][0] == runs[1][0]
    print(f"determinism run1_vs_run2={'identical' if same else 'DIFFERENT'}")
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
