#!/usr/bin/env python3
"""F37C2Rerun negative control v2: targeted single-input mutations per C2 check."""
import importlib.util
import pathlib
import re
import shutil
import sys
import tempfile

MUT = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("c2", MUT / "plans/round37_c2_verify.py")
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

SRC = MUT / "corpus/SOURCES.md"
ENTRY = MUT / "corpus/knowledge/tb2-git-webserver-grader.md"
RC = MUT / "corpus/evidence/round37/git-webserver-probe.txt"
work = pathlib.Path(tempfile.mkdtemp(prefix="negctl2-"))
rows = []


def run(label, fn, target, mut):
    bak = target.read_bytes()
    try:
        target.write_bytes(mut(bak))
    except Exception as e:
        target.write_bytes(bak)
        rows.append((label, False, f"mutation failed: {e}"))
        print(f"{label}: MUTATION-FAILED {e}")
        return
    try:
        ok, note = fn()
    except Exception as e:
        ok, note = False, f"error {type(e).__name__}: {e}"
    finally:
        target.write_bytes(bak)
    rows.append((label, ok, note))
    print(f"{label}: {'ok' if ok else 'DEFECT'} {note}")


def edit_row(text, sid, fn):
    out = []
    for line in text.splitlines(True):
        m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
        if m and m.group(1) == sid:
            cells = [c for c in line.rstrip("\n").strip().strip("|").split("|")]
            fn(cells)
            line = "| " + " | ".join(c.strip() for c in cells) + " |\n"
        out.append(line)
    return "".join(out)


def flip_anchor_hex(cells):
    d = re.search(r"([0-9a-f]{64})", cells[5])
    h = d.group(1)
    cells[5] = cells[5].replace(h, h[:-1] + ("0" if h[-1] != "0" else "1"))


def add_second_digest(cells):
    d = re.search(r"([0-9a-f]{64})", cells[5]).group(1)
    cells[5] = cells[5] + f"; sha256 {'f' * 64}"


def drop_sha_prefix(cells):
    cells[5] = cells[5].replace("sha256 ", "", 1)


run("MUT V3 S111 anchor hex digit", lambda: c2.v3(MUT), SRC,
    lambda b: edit_row(b.decode(), "S111", flip_anchor_hex).encode())
run("MUT V3 S112 second sha256 token", lambda: c2.v3(MUT), SRC,
    lambda b: edit_row(b.decode(), "S112", add_second_digest).encode())
run("MUT V3 S113 sha256 prefix dropped", lambda: c2.v3(MUT), SRC,
    lambda b: edit_row(b.decode(), "S113", drop_sha_prefix).encode())
run("MUT V3 row truncated to 10 cells", lambda: c2.v3(MUT), SRC,
    lambda b: edit_row(b.decode(), "S113", lambda c: c.pop()).encode())

run("MUT V6 duplicate id (E03)", lambda: c2.v6(MUT), SRC,
    lambda b: b + b"".join(l for l in b.decode().splitlines(True) if l.startswith("| S111 |")))
run("MUT V6 malformed row (E01)", lambda: c2.v6(MUT), SRC,
    lambda b: b.replace(b"| S111 |", b"| S111 | x |", 1))


def relabel(from_label, to_label):
    def f(b):
        t = b.decode()
        m = re.search(r"^(\|\s*`instruction\.md:\d+(?:-\d+)?`\s*\|\s*)" + from_label, t, re.M)
        return b if not m else (t[:m.end(1)] + to_label + t[m.end(0):]).encode()
    return f


run("MUT V7 unenforced->enforced", lambda: c2.v7(MUT), ENTRY, relabel("unenforced", "enforced"))
run("MUT V7 enforced->unenforced", lambda: c2.v7(MUT), ENTRY, relabel("enforced", "unenforced"))
run("MUT V7 partly->enforced", lambda: c2.v7(MUT), ENTRY, relabel("partly", "enforced"))


def drop_map_row(b):
    lines = b.decode().splitlines(True)
    keep = []
    dropped = False
    for l in lines:
        if not dropped and re.match(r"^\|\s*`instruction\.md:\d", l):
            dropped = True
            continue
        keep.append(l)
    return "".join(keep).encode()


run("MUT V7 unmapped instruction line", lambda: c2.v7(MUT), ENTRY, drop_map_row)


def forge_stdout(b):
    return b.replace(b"'Content: hello world'", b"'Content: hello world!'", 1)


run("MUT V4/V7-only blind: forged stdout text", lambda: c2.v4(MUT), RC, forge_stdout)

shutil.rmtree(work, ignore_errors=True)
baseline = 0
mutants = [(l, ok) for l, ok, _ in rows]
caught = [l for l, ok in mutants if not ok]
print(f"mutations={len(mutants)} caught={len(caught)} uncaught={[l for l, ok in mutants if ok] or 0}")
sys.exit(0)
