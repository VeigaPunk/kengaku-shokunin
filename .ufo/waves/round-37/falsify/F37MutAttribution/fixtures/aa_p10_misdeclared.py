"""F37MutAttribution hostile fixture (round-37 wave 2): exposes the audit mutant that drops the
declared-defects guard (`defects` must contain the clause).

Same /proc oracle as bait_p10_oracle.py (defects only under the pristine gate), but the fixture
MISDECLARES: expect=reject with `defects=[]` while the reference run observes exactly {P10}.  The frozen
counter flags such a fixture WRONG (declared != observed) -- but the audit never consults that; its only
defense is the declared-defects guard itself.  The pristine audit skips this fixture for every P10 mutant
(P10 is not in the declared set); the mutant audit without the guard attributes M41 and M42 to it.
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
    {"fid": "attr-p10-aa", "expect": "reject", "defects": [], "build": _build},
]
