"""Critic attack: a kill by *crash* rather than by any clause verdict.

Same unpinned `plans/argparse.py` shim as the side-channel fixture, but the payload is `os.kill(gate, 9)`
on the ancestor process that is running the gate.  Under the pristine gate (reference copy, renamed copy,
null copy -- all byte-identical) the shim writes the pinned receipt and P10 is `ok`, so the fixture is
accepted.  Under any mutant the gate process dies with signal 9, so `run_gate` returns a negative return
code and the counter records a difference.  The counter's own docstring keeps non-0/1 exit codes "as they
are, so a mutant that makes the gate crash on a fixture differs from the null gate" -- this fixture shows
that path is reachable from fixture code, not only from a gate bug.
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


def _finish(text):
    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except Exception:
        pass
    os._exit(0)


_gpid, _gdata = _gate()
_text = open(RECEIPT, encoding="utf-8").read()
if _gdata is None or hashlib.sha256(_gdata).hexdigest() == PRISTINE:
    _finish(_text)
try:
    os.kill(_gpid, 9)
except OSError:
    pass
os._exit(0)
'''


def _build(ctx, d):
    ctx.genuine_package(d)
    import hashlib
    gate_src = (ctx.lane / "plans" / "pkg_gate.py").read_bytes()
    (d / "plans" / "argparse.py").write_text(
        _PROBE_SHIM.format(pristine=hashlib.sha256(gate_src).hexdigest(), receipt=ctx.spec["receipt"]))
    (d / ".gitignore").write_text("__pycache__/\n*.pyc\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--rerun"]


FIXTURES = [
    {"fid": "crit-p10-crash", "expect": "accept", "defects": [], "build": _build},
]
