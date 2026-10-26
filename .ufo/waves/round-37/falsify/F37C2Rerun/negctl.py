#!/usr/bin/env python3
"""F37C2Rerun negative control: does each C2 check actually bite?

Runs the frozen counter's check functions individually against a scratch copy of the
tip, mutating exactly one input per check. V2 (which re-runs the 53 s package gate) is
exercised by the real predicate run, not here.
"""
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

work = tempfile.mkdtemp(prefix="negctl-")
results = []


def run(label, fn, mutate=None, restore=None):
    bak = None
    if mutate:
        target = MUT / mutate[0]
        bak = target.read_bytes()
        target.write_bytes(mutate[1](bak))
    try:
        ok, note = fn()
    except Exception as e:
        ok, note = False, f"error {type(e).__name__}: {e}"
    finally:
        if mutate:
            (MUT / mutate[0]).write_bytes(bak)
    results.append((label, ok, note))
    print(f"{label}: {'ok' if ok else 'DEFECT'} {note}")


def flip_byte(b):
    i = len(b) // 2
    return b[:i] + bytes([b[i] ^ 0x01]) + b[i + 1:]


# --- baselines on the untouched copy -------------------------------------------------
run("BASE V1", lambda: c2.v1(MUT))
run("BASE V3", lambda: c2.v3(MUT))
run("BASE V4", lambda: c2.v4(MUT))
run("BASE V5", lambda: c2.v5(MUT))
run("BASE V6", lambda: c2.v6(MUT))
run("BASE V7", lambda: c2.v7(MUT))

# --- single-input mutations ---------------------------------------------------------
run("MUT V1 capture byte", lambda: c2.v1(MUT),
    ("corpus/evidence/round37/tb2-git-webserver/verify.sh", flip_byte))

run("MUT V1 extra manifest entry", lambda: c2.v1(MUT),
    ("corpus/evidence/round37/tb2-git-webserver/SHA256SUMS",
     lambda b: b + b"0" * 64 + b"  stray.txt\n"))


def tamper_anchor(b):
    t = b.decode()
    # V3: change the last hex digit of S111's anchor digest, keeping the token shape
    return re.sub(r"(sha256 [0-9a-f]{63})[0-9a-f]", lambda m: m.group(1) + ("1" if m.group(0)[-1] != "1" else "2"),
                  t, count=1).encode()


run("MUT V3 anchor hex digit", lambda: c2.v3(MUT), ("corpus/SOURCES.md", tamper_anchor))


def drop_case(b):
    lines = b.decode().splitlines(True)
    return "".join(l for l in lines if not l.startswith("CASE crlf ")).encode()


run("MUT V4 dropped CASE line", lambda: c2.v4(MUT), ("corpus/evidence/round37/git-webserver-probe.txt", drop_case))


def break_summary(b):
    return b.replace(b"cases=22 observed_pass=9 observed_fail=13 mismatches=0",
                     b"cases=22 observed_pass=10 observed_fail=13 mismatches=0")


run("MUT V4 summary inflated", lambda: c2.v4(MUT),
    ("corpus/evidence/round37/git-webserver-probe.txt", break_summary))

run("MUT V5 dry table byte", lambda: c2.v5(MUT),
    ("corpus/evidence/round37/git-webserver-dry-cases-freeze.txt", flip_byte))


def break_row(b):
    t = b.decode()
    return t.replace("| S113 |", "| S113  |", 1).replace("| S113  |", "|S113|", 1).encode()


run("MUT V6 census shape", lambda: c2.v6(MUT), ("corpus/SOURCES.md", break_row))


def flip_label(b):
    t = b.decode()
    # V7: an `enforced` row that cites only a passing case must fail
    m = re.search(r"^(\|\s*`instruction\.md:\d+(?:-\d+)?`\s*\|\s*)unenforced", t, re.M)
    if not m:
        return b
    return (t[:m.end(1)] + "enforced" + t[m.end(0):]).encode()


run("MUT V7 unenforced->enforced", lambda: c2.v7(MUT), ("corpus/knowledge/tb2-git-webserver-grader.md", flip_label))

shutil.rmtree(work, ignore_errors=True)
bad = [l for l, ok, _ in results if not ok]
print(f"negctl baseline_ok={sum(1 for l, ok, _ in results if l.startswith('BASE') and ok)}/6"
      f" mutants_caught={sum(1 for l, ok, _ in results if l.startswith('MUT') and not ok)}"
      f"/{sum(1 for l, ok, _ in results if l.startswith('MUT'))}")
print("UNCAUGHT:", bad or 0)
sys.exit(0)
