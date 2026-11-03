#!/usr/bin/env python3
"""Generate the R67-C2 strict-gate mutation corpus from the committed R65 receipt.

Usage: gen_fixtures.py <base-receipt> <out-fixtures-dir>

Each mutant is derived from the committed receipt by exactly ONE change
(one line replaced, or one line deleted). The generator asserts that:
  * the anchor occurs exactly once in the base bytes, and
  * the mutant differs from the base in exactly one line, and
  * the mutant byte length differs by exactly the expected delta.
Bytes are handled as bytes (no newline translation).
"""

import difflib
import hashlib
import pathlib
import sys

ZERO64 = "0" * 64
INSTRUMENT = b"# instrument plans/round65_c1_sqlite_probe.py version=r65-c1/1"
GRADER_SHA = b"b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b"
AMALG_SHA = b"0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9"


def replace_once(data: bytes, old: bytes, new: bytes) -> bytes:
    found = data.count(old)
    if found != 1:
        raise SystemExit("anchor count %d != 1 for %r" % (found, old[:60]))
    return data.replace(old, new, 1)


def delete_line(data: bytes, line: bytes) -> bytes:
    needle = line + b"\n"
    found = data.count(needle)
    if found != 1:
        raise SystemExit("delete anchor count %d != 1 for %r" % (found, line[:60]))
    return data.replace(needle, b"", 1)


def line_with(data: bytes, prefix: bytes) -> bytes:
    """Return the unique line (newline-stripped) starting with `prefix`."""
    matches = [line for line in data.split(b"\n") if line.startswith(prefix)]
    if len(matches) != 1:
        raise SystemExit("line %r matches %d" % (prefix[:40], len(matches)))
    return matches[0]


# (filename, clause, expected byte-length delta, transform)
MUTATIONS = []


def mutation(name, clause, delta):
    def register(fn):
        MUTATIONS.append((name, clause, delta, fn))
        return fn
    return register


@mutation("m-s1-1.txt", "s1", -len(INSTRUMENT) - 1)
def _(data):
    return delete_line(data, INSTRUMENT)


@mutation("m-s1-2.txt", "s1", 0)
def _(data):
    return replace_once(data, INSTRUMENT, INSTRUMENT.replace(b"version=r65-c1/1",
                                                              b"version=r65-c1/9"))


@mutation("m-s2-1.txt", "s2", 0)
def _(data):
    grader = line_with(data, b"GRADER ")
    return replace_once(data, grader,
                        replace_once(grader, b"sha256=" + GRADER_SHA,
                                     b"sha256=" + ZERO64.encode()))


@mutation("m-s3-1.txt", "s3", 0)
def _(data):
    amalg = line_with(data, b"AMALG ")
    return replace_once(data, amalg,
                        replace_once(amalg, b"sha256=" + AMALG_SHA,
                                     b"sha256=" + ZERO64.encode()))


@mutation("m-s4-1.txt", "s4", 0)
def _(data):
    line = line_with(data, b"TOOLCHAIN ")
    return replace_once(data, line, replace_once(line, b"gcc=16.2.1", b"gcc=15.0.0"))


@mutation("m-s5-1.txt", "s5", 0)
def _(data):
    line = line_with(data, b"RUN G2 ")
    return replace_once(data, line, replace_once(line, b"rc=0", b"rc=1"))


@mutation("m-s5-2.txt", "s5", -7)  # 40-byte driver token -> 33-byte fabricated token
def _(data):
    line = line_with(data, b"RUN G4 ")
    return replace_once(data, line, replace_once(
        line, b'driver="/usr/bin/python3 /ctl/driver.py"',
        b'driver="fabricated - nothing ran"'))


@mutation("m-s5-3.txt", "s5", -len(b"NOBIND G3 listeners_before=35 listeners_after=35 delta=0\n"))
def _(data):
    return delete_line(data, b"NOBIND G3 listeners_before=35 listeners_after=35 delta=0")


@mutation("m-s6-1.txt", "s6", 0)
def _(data):
    return replace_once(data, b"VECTOR G3=P/P/F", b"VECTOR G3=P/P/P")


def one_change(base: bytes, mutant: bytes):
    """Return (removed, added) for the single non-equal diff opcode, else None.

    Exactly one contiguous opcode may differ, and it must remove exactly one
    base line and add at most one mutant line (a replace or a delete).
    """
    matcher = difflib.SequenceMatcher(a=base.split(b"\n"), b=mutant.split(b"\n"),
                                      autojunk=False)
    changed = [op for op in matcher.get_opcodes() if op[0] != "equal"]
    if len(changed) != 1:
        return None
    tag, i1, i2, j1, j2 = changed[0]
    if tag not in ("replace", "delete"):
        return None
    if (i2 - i1) != 1 or (j2 - j1) > 1:
        return None
    return (i2 - i1, j2 - j1)


def main(argv):
    if len(argv) != 3:
        raise SystemExit("usage: gen_fixtures.py <base-receipt> <out-dir>")
    base_path = pathlib.Path(argv[1])
    out_dir = pathlib.Path(argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    base = base_path.read_bytes()
    print("base %s sha256=%s bytes=%d" % (base_path, hashlib.sha256(base).hexdigest(), len(base)))
    print("file\tclause\tsha256\tbytes\tremoved_lines\tadded_lines")
    failures = 0
    for name, clause, delta, fn in MUTATIONS:
        mutant = fn(base)
        if len(mutant) - len(base) != delta:
            print("GENERATOR-FAIL %s length delta %d != %d" % (name, len(mutant) - len(base), delta))
            failures += 1
            continue
        counts = one_change(base, mutant)
        if counts is None:
            print("GENERATOR-FAIL %s not a single-line change" % name)
            failures += 1
            continue
        removed, added = counts
        target = out_dir / name
        target.write_bytes(mutant)
        print("%s\t%s\t%s\t%d\t%d\t%d" % (name, clause,
                                          hashlib.sha256(mutant).hexdigest(),
                                          len(mutant), removed, added))
    if failures:
        raise SystemExit("generator failures: %d" % failures)
    print("GENERATOR ok mutants=%d" % len(MUTATIONS))


if __name__ == "__main__":
    main(sys.argv)
