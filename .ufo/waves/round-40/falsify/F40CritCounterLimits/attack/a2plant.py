"""a2_plant — the build child plants the shim (wave-1 A2): the module is non-author code that
writes outside its fixture directory and the counter never notices.
"""

import hashlib
import pathlib

SHIM = '/fast/scratch/hyaku/kengaku-r40/F40CritCounterLimits/attack/shim'
SOURCES = "corpus/SOURCES.md"
EV = "corpus/evidence/x"
CAP = b"a2 replay capture bytes\n"
OTHER = b"a2 replay second capture bytes\n"
ROW = '| S900 | a2 replay row ({tag}) | code | A | one capture | sha256 {dig} | names corpus/evidence/x/cap.txt | fixture | mined | 2026-10-26 | corpus/knowledge/x.md |'
HEAD = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def repo(ctx, d, tag):
    r = ctx.init(d / "repo")
    dig = hashlib.sha256(CAP).hexdigest()
    (r / EV).mkdir(parents=True)
    (r / SOURCES).write_text(HEAD + ROW.format(tag=tag, dig=dig) + "\n")
    (r / EV / "cap.txt").write_bytes(CAP)
    (r / EV / "other.txt").write_bytes(OTHER)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "a2 replay fixture")
    return ["--lane", str(r)]


SHIM_SRC = '#!/usr/bin/env python3\n"""A `git` resolved from PATH by the tool under test (round-40 A2 replay, seat F40CritCounterLimits).\n\nIt answers by phase, phase = the digest of the variant bound at <root>/slots/anchor.py:\n  f000  corrupt in the MUTANT phase   -> reference accepts, mutant prints capture-unanchored\n  f001  corrupt in the REFERENCE phase -> reference prints capture-unanchored, mutant accepts\nand it writes <lane>/state.lock on every invocation (the A5 `.lock` name).\nEverything else is passed straight through to /usr/bin/git.\n"""\nimport hashlib\nimport pathlib\nimport subprocess\nimport sys\n\nREAL = "/usr/bin/git"\nREF = "11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2"\nPROV = b"PROVENANCE.md"\nFAB = (b"| S900 | `cap.txt` | first line |\\n"\n       b"| S900 | `other.txt` | second line |\\n")\nEVID = "corpus/evidence"\n\n\ndef split(argv):\n    a = list(argv)\n    if a[:1] == ["-C"] and len(a) >= 2:\n        return pathlib.Path(a[1]), a[2:]\n    return None, a\n\n\ndef where(lane):\n    if lane is None:\n        return None, None\n    q = lane\n    for _ in range(4):\n        if q.parent.name == "fx":\n            parts = lane.relative_to(q).parts\n            return q.parent.parent, (parts[0] if parts else None)\n        q = q.parent\n    return None, None\n\n\ndef phase(root):\n    try:\n        dig = hashlib.sha256((root / "slots" / "anchor.py").read_bytes()).hexdigest()\n    except OSError:\n        return "ref"\n    return "mut" if dig != REF else "ref"\n\n\ndef run(lane, rest, data=None):\n    cmd = [REAL] + (["-C", str(lane)] if lane is not None else []) + rest\n    return subprocess.run(cmd, input=data, capture_output=True)\n\n\ndef main(argv):\n    lane, rest = split(argv)\n    root, idx = where(lane)\n    if root is None:\n        r = run(lane, rest, sys.stdin.buffer.read() if rest[:1] == ["cat-file"] else None)\n        sys.stdout.buffer.write(r.stdout)\n        sys.stderr.buffer.write(r.stderr)\n        return r.returncode\n    ph = phase(root)\n    corrupt = (idx == "f000" and ph == "mut") or (idx == "f001" and ph == "ref")\n    try:\n        (lane / "state.lock").write_text("the tool run wrote this under a name the fingerprint skips\\n")\n    except OSError:\n        pass\n    if corrupt and rest[:3] == ["ls-tree", "-r", "--name-only"] and rest[-1] == EVID:\n        r = run(lane, rest)\n        out = r.stdout\n        if out and not out.endswith(b"\\0"):\n            out += b"\\0"\n        out += EVID.encode() + b"/x/" + PROV + b"\\0"\n        sys.stdout.buffer.write(out)\n        return r.returncode\n    if corrupt and rest[:1] == ["cat-file"]:\n        specs = [s for s in sys.stdin.buffer.read().split(b"\\n") if s]\n        fab = b"/" + PROV\n        keep = [s for s in specs if not s.endswith(fab)]\n        r = run(lane, rest, b"\\n".join(keep) + b"\\n" if keep else b"")\n        resps, i = {}, 0\n        for s in keep:\n            nl = r.stdout.find(b"\\n", i)\n            if nl < 0:\n                break\n            header = r.stdout[i:nl]\n            parts = header.split()\n            if len(parts) != 3:\n                resps[s] = header + b"\\n"\n                i = nl + 1\n                continue\n            size = int(parts[2])\n            resps[s] = r.stdout[i:nl + 1 + size + 1]\n            i = nl + 1 + size + 1\n        out = b""\n        for s in specs:\n            if s.endswith(fab):\n                out += s + b" blob " + str(len(FAB)).encode() + b"\\n" + FAB + b"\\n"\n            else:\n                out += resps.get(s, s + b" missing\\n")\n        sys.stdout.buffer.write(out)\n        return r.returncode\n    r = run(lane, rest, sys.stdin.buffer.read() if rest[:1] == ["cat-file"] else None)\n    sys.stdout.buffer.write(r.stdout)\n    sys.stderr.buffer.write(r.stderr)\n    return r.returncode\n\n\nif __name__ == "__main__":\n    sys.exit(main(sys.argv[1:]))\n'


def plant():
    p = pathlib.Path(SHIM) / "git"
    p.write_text(SHIM_SRC)
    p.chmod(0o755)


def build_accept(ctx, d):
    plant()
    return repo(ctx, d, "accept-in-the-reference-phase")


def build_reject(ctx, d):
    plant()
    return repo(ctx, d, "reject-in-the-reference-phase")


FIXTURES = [
    {"fid": "a2-replay-accept", "tool": "anchor", "expect": "accept", "defects": [], "build": build_accept},
    {"fid": "a2-replay-injected", "tool": "anchor", "expect": "reject",
     "defects": ["capture-unanchored"], "build": build_reject},
]
