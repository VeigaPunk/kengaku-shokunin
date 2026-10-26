"""Critic attack: fixture code re-run by P10 has unsandboxed write access to the lane, and the counter
only watches the mutant file.

`c_rerun` runs `spec["probe_cmd"]` with cwd = the fixture root but the *environment and user* of the
counter, and the gate is invoked with an absolute `--spec <lane>/plans/pkg-spec-r35.json`.  A probe can
read that path out of its ancestor's `/proc/<pid>/cmdline` and therefore address the lane that is being
measured.  Here it appends a line to `<lane>/plans/pkg_gate.py` when, and only when, the gate bytes are
not the pristine ones -- so the reference/renamed/null runs are untouched and the mutant result is
unchanged: the counter reports the mutant as SURVIVED, detects nothing, and the lane's gate file is
corrupt afterwards.

Guard: the shim refuses to write when the derived lane is the real lane
(`/home/vgpnk/Projects/shokunin/kengaku-shokunin`); run this module against a scratch clone only.
"""

_PROBE_SHIM = r'''import hashlib, os, pathlib, sys

PRISTINE = {pristine!r}
RECEIPT = {receipt!r}
REAL_LANE = {real_lane!r}


def _ancestors():
    pid = os.getppid()
    for _ in range(12):
        if pid <= 1:
            return
        try:
            with open("/proc/%d/cmdline" % pid, "rb") as f:
                tokens = f.read().split(b"\0")
            with open("/proc/%d/stat" % pid, "rb") as f:
                nxt = int(f.read().rsplit(b") ", 1)[-1].split()[1])
        except (OSError, IndexError, ValueError):
            return
        yield pid, tokens
        pid = nxt


text = open(RECEIPT, encoding="utf-8").read()
_lane = None
_running = None
for _pid, _tokens in _ancestors():
    if _lane is None and b"--spec" in _tokens:
        _lane = pathlib.Path(_tokens[_tokens.index(b"--spec") + 1].decode()).parent.parent
    if _running is None:
        for _tok in _tokens:
            if not _tok.endswith(b".py"):
                continue
            try:
                _data = pathlib.Path(_tok.decode()).read_bytes()
            except OSError:
                continue
            if b"Hardened package gate" in _data:
                _running = _data
                break
if (_lane is not None and _running is not None and str(_lane) != REAL_LANE
        and hashlib.sha256(_running).hexdigest() != PRISTINE):
    with open(_lane / "plans" / "pkg_gate.py", "ab") as f:
        f.write(b"# corrupted by fixture code during the C1 measurement\n")
sys.stdout.write(text)
sys.stdout.flush()
os._exit(0)
'''


def _build(ctx, d):
    ctx.genuine_package(d)
    import hashlib
    gate_src = (ctx.lane / "plans" / "pkg_gate.py").read_bytes()
    (d / "plans" / "argparse.py").write_text(
        _PROBE_SHIM.format(pristine=hashlib.sha256(gate_src).hexdigest(), receipt=ctx.spec["receipt"],
                           real_lane="/home/vgpnk/Projects/shokunin/kengaku-shokunin"))
    (d / ".gitignore").write_text("__pycache__/\n*.pyc\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--rerun"]


FIXTURES = [
    {"fid": "crit-lane-write", "expect": "accept", "defects": [], "build": _build},
]
