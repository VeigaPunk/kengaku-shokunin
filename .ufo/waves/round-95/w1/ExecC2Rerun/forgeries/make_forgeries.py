#!/usr/bin/env python3
"""ExecC2Rerun (R95-C2 held-out extension): generate gate-v2 variants.

Usage: make_forgeries.py <path-to-round94_freeze_integrity.py> <out-dir>

g1..g5 are false gates (each yields a wrong verdict on one input, see demo_inputs.py).
e5 is an equivalence control: it differs from v2 but is observably identical on every input,
so it is NOT a false gate and is not counted.

Every edit is an exact single-occurrence replacement (asserted); nothing else in v2 changes.
"""
import pathlib
import sys

src = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)


def edit(text, old, new):
    n = text.count(old)
    assert n == 1, (n, old[:70])
    return text.replace(old, new)


G = {}

# g1: touched counts only commits whose numstat is non-zero, so a mode-only (chmod) commit is not a touch.
G["g1-mode-only-invisible"] = edit(
    src,
    '''        log = git(root, "rev-list", "--full-history", f"{f}..{t}", "--", p)
        if log.returncode != 0:
            raise CouldNotEvaluate(f"rev-list failed for {p}")
        touched = len([x for x in log.stdout.decode().split() if x])
''',
    '''        log = git(root, "rev-list", "--full-history", f"{f}..{t}", "--", p)
        if log.returncode != 0:
            raise CouldNotEvaluate(f"rev-list failed for {p}")
        touched = 0
        for c in log.stdout.decode().split():
            ns = git(root, "show", "--numstat", "--format=", c, "--", p).stdout.decode().splitlines()
            if any(line.split("\\t")[:2] != ["0", "0"] for line in ns if line.strip()):
                touched += 1
''')

# g2: table rows whose path starts with "." (dotfiles and ./-prefixed rows) are silently not instruments.
G["g2-dot-row-dropped"] = edit(
    src,
    '''    rows = []
    for want, p in table:
''',
    '''    rows = []
    table = [(w, p) for w, p in table if not p.startswith(".")]
    for want, p in table:
''')

# g3: only commits that descend from the freeze count (ancestry path), so a side branch forked before
# the freeze and merged after it with a treesame merge is not counted as a touch.
G["g3-ancestry-path"] = edit(
    src,
    '''"rev-list", "--full-history", f"{f}..{t}", "--", p)''',
    '''"rev-list", "--full-history", "--ancestry-path", f"{f}..{t}", "--", p)''')

# g4: a table row that is a gitlink (submodule pointer at the freeze) is pinned by the superproject and skipped.
G["g4-gitlink-row-skipped"] = edit(
    src,
    '''    for want, p in table:
        at_f = blob(root, f, p)
''',
    '''    for want, p in table:
        if git(root, "ls-tree", f, "--", p).stdout.startswith(b"160000 commit"):
            continue
        at_f = blob(root, f, p)
''')

# g5: a table row whose path is not ASCII is skipped ("encoding-unsafe path, not an instrument").
G["g5-nonascii-row-skipped"] = edit(
    src,
    '''    for want, p in table:
        at_f = blob(root, f, p)
''',
    '''    for want, p in table:
        if not p.isascii():
            continue
        at_f = blob(root, f, p)
''')

# e5: equivalence control (NOT a false gate): CR-tolerant row match. splitlines() strips the CR before
# parse_table sees the line, so the branch is unreachable and the gate is observably v2.
E = {}
E["e5-crlf-equivalent"] = edit(
    src,
    '''            m = ROW.match(line.strip())
''',
    '''            m = ROW.match(line)
            if not m and line.endswith("\\r"):
                continue
            m = m or ROW.match(line.strip())
''')

for name, text in {**G, **E}.items():
    (out / f"{name}.py").write_text(text)
    print(f"WROTE {out / (name + '.py')} lines={text.count(chr(10))}")
