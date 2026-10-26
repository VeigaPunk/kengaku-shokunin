"""Battery37 module p910: one single-defect fixture per frozen mutant M39, M41, M42, M43.

Each fixture is the genuine round-35 package bytes (``ctx.r36.copy_package``) with exactly one edit, and
declares the exact clause set the unmodified gate prints ``DEFECT`` on it:

  p910-not-a-git-repo     M39, P9   the directory is not a git worktree at all (no ``git init``);
                                   ``git -C d ls-files`` cannot answer, so P9 must report it.
  p910-receipt-deleted    M41, P10  the receipt is gone and ``--rerun`` is passed. P2 fires as well and
                                   that is unavoidable: ``spec["receipt"]`` is the single input to both
                                   P2's digest pin and P10's re-run baseline.
  p910-probe-exits-1      M42, P10  the pinned round-35 probe keeps printing and exits 1. P1 fires as
                                   well and that is unavoidable: the probe is a ``frozen_instruments``
                                   entry, so editing it necessarily changes its pinned digest.
  p910-receipt-one-byte   M43, P10  one byte of the receipt differs; the fresh probe run succeeds but is
                                   no longer byte-equal to it. P2 fires as well (same reason as above).

P10 re-runs ``plans/tb2_grader_probe.py`` with ``cwd = root``; ``spec_from_file_location`` byte-compiles
the captured grader into ``corpus/evidence/round35/tb2-eval/__pycache__``. The fixtures that reach P10
therefore carry the lane's own ``.gitignore`` (``__pycache__/``), staged in the index: without it the
byte-code file is untracked on every gate run after the first, and P9 — not the clause under test —
would be the clause that fires.

stdlib only; no import-time side effects.
"""
import subprocess


def _argv(d, rerun=False):
    argv = ["package", "--root", str(d), "--require-clean-tree"]
    if rerun:
        argv.append("--rerun")
    return argv


def _ignore_rule(ctx, d):
    """Copy the lane's own `.gitignore` beside the package bytes (see the module docstring)."""
    (d / ".gitignore").write_text((ctx.lane / ".gitignore").read_text())


def _not_a_git_repo(ctx, d):
    """M39: `c_clean_tree`'s 'root is not a readable git worktree' branch."""
    ctx.r36.copy_package(ctx.lane, ctx.spec, d)
    _ignore_rule(ctx, d)
    top = subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    if top.returncode == 0:
        # The harness placed the fixture inside somebody else's repository: a .git pointer at an absent
        # directory keeps this directory itself from being a worktree, so no repository is readable here.
        (d / ".git").write_text("gitdir: /nonexistent-k37-p910\n")
    probe = subprocess.run(["git", "-C", str(d), "ls-files", "--others", "--exclude-standard"],
                           capture_output=True, text=True)
    if probe.returncode == 0:
        raise RuntimeError(f"{d} is inside a readable git worktree; pass --work outside any repository")
    return _argv(d)


def _receipt_deleted(ctx, d):
    """M41: `c_rerun`'s 'receipt unreadable' branch."""
    ctx.genuine_package(d)
    _ignore_rule(ctx, d)
    (d / ctx.spec["receipt"]).unlink()
    ctx.git_add(d)
    return _argv(d, rerun=True)


def _probe_exits_nonzero(ctx, d):
    """M42: `c_rerun`'s 'fresh probe exit=' branch — the probe prints, then reports failure."""
    ctx.genuine_package(d)
    _ignore_rule(ctx, d)
    probe = d / "plans/tb2_grader_probe.py"
    text = probe.read_text()
    old = 'if __name__ == "__main__":\n    sys.exit(main())\n'
    new = ('if __name__ == "__main__":\n'
           '    # fixture p910: same output on stdout, then a failing status\n'
           '    _rc = main()\n'
           '    sys.exit(1 if _rc == 0 else _rc)\n')
    if text.count(old) != 1:
        raise RuntimeError("probe entry point line not found exactly once")
    probe.write_text(text.replace(old, new, 1))
    ctx.git_add(d)
    return _argv(d, rerun=True)


def _receipt_one_byte(ctx, d):
    """M43: `c_rerun`'s byte-equality branch — the receipt is readable and one byte off."""
    ctx.genuine_package(d)
    _ignore_rule(ctx, d)
    receipt = d / ctx.spec["receipt"]
    raw = receipt.read_bytes()
    i = raw.index(b"biopython=") + len(b"biopython=")
    flipped = raw[:i] + (b"2" if raw[i:i + 1] != b"2" else b"3") + raw[i + 1:]
    if len(flipped) != len(raw) or flipped == raw or flipped.count(b"\n") != raw.count(b"\n"):
        raise RuntimeError("receipt one-byte edit did not keep the file's shape")
    receipt.write_bytes(flipped)
    ctx.git_add(d)
    return _argv(d, rerun=True)


FIXTURES = [
    {"fid": "p910-not-a-git-repo", "expect": "reject", "defects": ["P9"], "build": _not_a_git_repo},
    {"fid": "p910-receipt-deleted", "expect": "reject", "defects": ["P2", "P10"], "build": _receipt_deleted},
    {"fid": "p910-probe-exits-1", "expect": "reject", "defects": ["P1", "P10"], "build": _probe_exits_nonzero},
    {"fid": "p910-receipt-one-byte", "expect": "reject", "defects": ["P2", "P10"], "build": _receipt_one_byte},
]
