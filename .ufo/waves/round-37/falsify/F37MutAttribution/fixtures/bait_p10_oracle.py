"""F37MutAttribution hostile fixture (round-37 wave 2): attacks the post-hoc attribution audit
(plans/round37_c1_attribution.py), not the frozen counter.

The audit attributes a mutant kill to a fixture when the subcommand family matches, the reference run
prints the clause as DEFECT, the fixture declares the clause in `defects`, and the mutant run exits 0/1
without printing it.  This fixture satisfies all four guards while exercising no advertised class: its
probe (an unpinned plans/argparse.py shim imported by the frozen probe before its own code) reads the
running gate's bytes from /proc and defects ONLY under the pristine gate -- under every mutant gate it
emits the receipt verbatim and exits 0, so under mutants the receipt is readable, the fresh probe exits
0 and its output is byte-equal: none of M41/M42/M43's advertised classes is present.

Under the frozen counter the fixture is indistinguishable from an honest one: reference, renamed copy and
null copy all run pristine gate bytes and defect identically (wrong=0, renamed_disagree=0,
null_detected=0), and every mutant is killed.  Under the audit the same fixture fraudulently attributes
M41, M42 and M43.
"""

_PROBE_SHIM = r'''import hashlib, os, sys

PRISTINE = {pristine!r}
RECEIPT = {receipt!r}


def _chain():
    pid = os.getppid()
    for _ in range(12):
        if pid <= 1:
            return
        yield pid
        try:
            with open("/proc/%d/stat" % pid, "rb") as f:
                pid = int(f.read().rsplit(b") ", 1)[-1].split()[1])
        except (OSError, IndexError, ValueError):
            return


def _gate():
    """Bytes of the nearest ancestor process running the package gate, or None."""
    for pid in _chain():
        try:
            with open("/proc/%d/cmdline" % pid, "rb") as f:
                tokens = f.read().split(b"\0")
        except OSError:
            continue
        for tok in tokens:
            if not tok.endswith(b".py"):
                continue
            try:
                with open(tok, "rb") as f:
                    data = f.read()
            except OSError:
                continue
            if b"Hardened package gate" in data:
                return data
    return None


_data = _gate()
_pristine = _data is not None and hashlib.sha256(_data).hexdigest() == PRISTINE
_text = open(RECEIPT, encoding="utf-8").read()
if _pristine:
    sys.stdout.write(_text + "bait: pristine gate defects; every mutant gate is fed the receipt verbatim\n")
else:
    sys.stdout.write(_text)
sys.stdout.flush()
os._exit(0)
'''


def _build(ctx, d):
    ctx.genuine_package(d)
    gate_src = (ctx.lane / "plans" / "pkg_gate.py").read_bytes()
    import hashlib
    shim = _PROBE_SHIM.format(pristine=hashlib.sha256(gate_src).hexdigest(),
                              receipt=ctx.spec["receipt"])
    (d / "plans" / "argparse.py").write_text(shim)
    (d / ".gitignore").write_text("__pycache__/\n*.pyc\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--rerun"]


FIXTURES = [
    {"fid": "attr-p10-bait", "expect": "reject", "defects": ["P10"], "build": _build},
]
