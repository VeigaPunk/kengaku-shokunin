"""Critic battery module (round 37, seat R37CritC1Battery): does the C1 counter accept a kill that
demonstrates no advertised class?

Attack 1 -- P10 is an oracle for the mutant identity.  The gate's P10 clause (`c_rerun`) re-runs the
package's own probe (`spec["probe_cmd"]`) with cwd = the fixture root.  The probe file itself is pinned
by P1 (`plans/tb2_grader_probe.py`), so a fixture may not rewrite it -- but `sys.path[0]` for
`python3 plans/tb2_grader_probe.py` is `<fixture>/plans/`, so an *extra, unpinned* module there is
imported by the probe before any of its own code runs.  `plans/argparse.py` is the first import of the
frozen probe (`plans/tb2_grader_probe.py:22`), so it executes first, inside the gate's P10 child.

From there the fixture walks `/proc/<pid>/stat` to its ancestor gate, hashes the gate's bytes, and:
  * pristine gate (reference copy and the null copy, which are byte-identical) -> write the pinned
    receipt verbatim, exit 0, so P10 prints `ok` and the whole fixture is accepted;
  * any other gate (every one of the 55 frozen mutants) -> write the receipt plus one line, so P10
    prints `DEFECT` and the gate exits 1.

Result: the fixture is declared `expect=accept`, the reference matches the declaration, the renamed
run agrees (the probe keys on gate bytes, never on a directory name), the null copy is undetected, and
every mutant's result differs -- including M44..M55, which belong to the d4-line/d5-line subcommands
that this package fixture never invokes.  No advertised defect class is exercised.

FIXTURES: list of dicts {fid, expect, defects, build}. build(ctx, d) fills the empty dir d and returns
the gate argv tail (never --spec).
"""

_PROBE_SHIM = r'''import hashlib, os, sys

PRISTINE = {pristine!r}
RECEIPT = {receipt!r}
LANE_GUARD = {lane_guard!r}


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
    """(pid, path, bytes) of the nearest ancestor process that is running the package gate."""
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
                return pid, tok.decode(), data
    return None, None, None


def _finish(text):
    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except Exception:
        pass
    os._exit(0)


_gpid, _gpath, _gdata = _gate()
_oracle = _gdata is not None and hashlib.sha256(_gdata).hexdigest() == PRISTINE
_text = open(RECEIPT, encoding="utf-8").read()
if _oracle:
    _finish(_text)
_finish(_text + "critic: this gate is not the pinned one\n")
'''


def _build(ctx, d):
    ctx.genuine_package(d)
    gate_src = (ctx.lane / "plans" / "pkg_gate.py").read_bytes()
    import hashlib
    shim = _PROBE_SHIM.format(pristine=hashlib.sha256(gate_src).hexdigest(),
                              receipt=ctx.spec["receipt"],
                              lane_guard=str(ctx.lane))
    (d / "plans" / "argparse.py").write_text(shim)
    # the shim is imported, so CPython caches plans/__pycache__/argparse.*.pyc on the first run; without
    # this ignore that cache is an untracked file and P9 defects from the second run on (renamed/null).
    (d / ".gitignore").write_text("__pycache__/\n*.pyc\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--rerun"]


FIXTURES = [
    {"fid": "crit-p10-sidechannel", "expect": "accept", "defects": [], "build": _build},
]
