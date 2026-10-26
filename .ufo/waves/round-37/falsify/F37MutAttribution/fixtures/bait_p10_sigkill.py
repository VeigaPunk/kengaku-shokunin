"""F37MutAttribution hostile fixture (round-37 wave 2): exposes the audit mutant that drops the
`rc in (0, 1)` guard (a crash or timeout must never be an attributed kill).

Same /proc oracle as bait_p10_oracle.py, but under a non-pristine gate the probe SIGKILLs the running
gate process itself (the ancestor whose bytes carry the gate marker -- NOT getppid(), which under the
gate's `uv run` probe wrapper is uv, not the gate).  The mutant gate therefore dies with returncode -9
and empty stdout, so the pristine audit refuses to attribute (the rc guard fires) while the mutant audit
that accepts any rc attributes M41, M42 and M43 to this fixture.  Under the frozen counter the fixture is
clean: reference, renamed copy and null copy all run pristine gate bytes and defect identically, and
every mutant differs (killed).
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
    """(pid, bytes) of the nearest ancestor process running the package gate, or (None, None)."""
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
                return pid, data
    return None, None


_gpid, _gdata = _gate()
_pristine = _gdata is not None and hashlib.sha256(_gdata).hexdigest() == PRISTINE
_text = open(RECEIPT, encoding="utf-8").read()
if _pristine:
    sys.stdout.write(_text + "bait: pristine gate defects; every mutant gate is killed\n")
    sys.stdout.flush()
    os._exit(0)
if _gpid is not None:
    os.kill(_gpid, 9)
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
    {"fid": "attr-p10-sigkill", "expect": "reject", "defects": ["P10"], "build": _build},
]
