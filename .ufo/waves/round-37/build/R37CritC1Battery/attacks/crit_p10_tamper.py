"""Critic attack: the counter's one integrity check, probed.

The counter re-hashes the mutant gate after `differs()` and calls the mutant `invalid` when the bytes
changed during the run (`plans/round37_c1_verify.py`, "invalid(mutant file changed during the run)").
This fixture triggers exactly that: under a non-pristine gate the shim truncates the gate file it found
through /proc before exiting, so the post-run digest differs.  It is the control for the side-channel
attacks -- it shows which tampering the counter *does* catch (the mutant file, and only that file).
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
                return tok.decode(), data
    return None, None


_gpath, _gdata = _gate()
_text = open(RECEIPT, encoding="utf-8").read()
if _gdata is not None and hashlib.sha256(_gdata).hexdigest() != PRISTINE and _gpath:
    with open(_gpath, "wb") as f:
        f.write(b"# tampered by fixture code\n")
try:
    sys.stdout.write(_text)
    sys.stdout.flush()
except Exception:
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
    {"fid": "crit-p10-tamper", "expect": "accept", "defects": [], "build": _build},
]
