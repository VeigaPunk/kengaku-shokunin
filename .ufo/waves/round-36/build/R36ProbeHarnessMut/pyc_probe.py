#!/usr/bin/env python3
"""Round 36, seat R36ProbeHarnessMut — extra (bonus) integrity probe of regex_log_probe.py.

The probe pins the *source* sha256 of the captured grader, then loads it with importlib. CPython's
SourceFileLoader validates `__pycache__/test_outputs.cpython-<tag>.pyc` by source mtime+size, not by
content hash (PEP 552 timestamp mode is the default). So a poisoned pyc whose 16-byte header carries
the genuine source's mtime and size should execute WITHOUT the source digest changing.

m6: replace the pyc with an always-pass grader; the source stays byte-identical.
Control m6ctl: same poisoned pyc placed where the header does NOT match (proves the pin/loader path
is otherwise sane and the effect is the header forgery, not the mere presence of the file).
"""
import importlib.util
import os
import pathlib
import py_compile
import shutil
import struct
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
MINI = HERE / "mini"
CAP_REL = "corpus/evidence/round36/tb2-regex-log"
SRC_REL = f"{CAP_REL}/test_outputs.py"
LOGS = HERE / "logs"
POISON = "import re\nfrom pathlib import Path\n\n\ndef test_regex_matches_dates():\n    return None\n"


def pyc_tag():
    return f"cpython-{sys.version_info.major}{sys.version_info.minor}"


def build(name, forge_header):
    d = HERE / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(MINI, d)
    src = d / SRC_REL
    # py_compile requires the source name to match the cache filename; compile the poison from a
    # sibling file, then move the resulting pyc over the genuine cache slot.
    poison_src = d / CAP_REL / "_poison.py"
    poison_src.write_text(POISON)
    pyc = d / CAP_REL / "__pycache__" / f"_poison.{pyc_tag()}.pyc"
    pyc.parent.mkdir(exist_ok=True)
    py_compile.compile(str(poison_src), cfile=str(pyc), doraise=True)
    poison_src.unlink()
    blob = bytearray(pyc.read_bytes())
    st = src.stat()
    if forge_header:
        # PEP 552 header: magic(4) flags(4) mtime(4) size(4)
        struct.pack_into("<II", blob, 8, int(st.st_mtime) & 0xFFFFFFFF, st.st_size & 0xFFFFFFFF)
    pyc.write_bytes(bytes(blob))
    pyc.rename(pyc.parent / f"test_outputs.{pyc_tag()}.pyc")
    return d, src


def run(d):
    p = subprocess.run([sys.executable, "plans/regex_log_probe.py", "--lane", "."],
                       cwd=d, capture_output=True, text=True)
    return p.stdout, p.stderr, p.returncode


def main():
    LOGS.mkdir(exist_ok=True)
    for name, forge in (("m6-pyc-substitution", True), ("m6ctl-pyc-stale-header", False)):
        d, src = build(name, forge)
        out, err, rc = run(d)
        (LOGS / f"{name}.txt").write_text(out + (f"\nSTDERR={err!r}\n" if err else ""))
        last = [l for l in out.strip().splitlines() if l.startswith("cases=")]
        print(f"{name}\trc={rc}\tsrc_sha_unchanged={out.splitlines()[0].split('sha256=')[1].split()[0][:12]}"
              f"\t{(last[-1] if last else out.strip()[:120])}\tstderr={err.strip()[:80]!r}")
    # show the header fields of the forged pyc vs the genuine source
    d, src = HERE / "m6-pyc-substitution", HERE / "m6-pyc-substitution" / SRC_REL
    blob = (d / CAP_REL / "__pycache__").glob("test_outputs.*.pyc").__next__().read_bytes()
    mtime, size = struct.unpack_from("<II", blob, 8)
    print(f"forged_pyc_header mtime={mtime} size={size} | genuine_source mtime={int(src.stat().st_mtime)} size={src.stat().st_size}")


if __name__ == "__main__":
    main()
