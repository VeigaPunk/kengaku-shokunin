"""Self-contained resume of the round-44 fence (round-44 counter legs, sliced by AST from the pinned file 6cf05323), wrapped in the claims/fences/r44_tail.py adapter. Built by R45ExecWitnessFence; not a lane file."""
import os
import pathlib
import subprocess

PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

GIT_PINS = {
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "4",
    "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
    "GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
    "GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false",
}

PIN_CHECK_ENV = {"PATH": PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", **GIT_PINS}

GIT_TIMEOUT = 30

ORDER_SHAPE = ("--lane", "--claims", "--receipt")

ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}

def pin_git(repo, *args, ceiling):
    """Round-44 F4/F6 (`R43SentinelCounter`): every parent-side git call has a timeout, no stdin, and discovery
    stops at `ceiling` (the parent of the fixture directory, which holds no repo), so neither a FIFO include nor a repo above `d` decides it.
    Returns (rc, stdout) or None on a timeout."""
    env = {**PIN_CHECK_ENV, "GIT_CEILING_DIRECTORIES": str(ceiling)}
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=env,
                           stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None
    return r.returncode, r.stdout.strip()

def repo_breach(d):
    """F42C1Hardened R4 (R42CritC1Counter V1b) with the round-44 fence repairs (`R43SentinelCounter` F1, F2, F4,
    F5, F6): a fixture's repo must stay rooted at its own directory AND keep its git store inside `d`.

    Every directory under `d` is walked with no depth cap (F2; a visited-entry bound of 200000 refuses a
    pathological tree instead of skipping it). A `.git` that is a plain FILE is refused (F1: `gitdir:` redirect),
    `rev-parse --absolute-git-dir` must resolve inside `d` (F1), `objects/info/alternates` is refused (F5), and
    `core.worktree` is read with `--local --no-includes` (F5) — any include.path is refused outright, so no file
    outside `d` is parsed. A git call that hangs is a breach (F4)."""
    d = d.resolve()
    repos, seen_entries = [], 0
    for top, dirs, files in os.walk(d):
        seen_entries += len(dirs) + len(files)
        if seen_entries > 200000:
            return "fixture tree exceeds 200000 entries"
        if ".git" in files:
            return f"{os.path.relpath(top, d)}/.git is a file (gitdir redirect), not a directory"
        if ".git" in dirs:
            repos.append(pathlib.Path(top))
        dirs[:] = sorted(x for x in dirs if x != ".git")
    for repo in repos:
        repo = repo.resolve()
        gd = repo / ".git"
        if gd.is_symlink():
            return f"{repo.name}/.git is a symlink"
        if (gd / "objects" / "info" / "alternates").exists():
            return f"{repo.name}/.git/objects/info/alternates present"
        inc = pin_git(repo, "config", "--local", "--no-includes", "--get-regexp", r"^include(if)?\.", ceiling=d.parent)
        if inc is None:
            return f"{repo.name}/git hung"
        if inc[0] == 0 and inc[1]:
            return f"{repo.name}/.git/config carries an include"
        for args, what in ((("rev-parse", "--show-toplevel"), "rev-parse --show-toplevel"),
                           (("rev-parse", "--absolute-git-dir"), "rev-parse --absolute-git-dir")):
            got = pin_git(repo, *args, ceiling=d.parent)
            if got is None:
                return f"{repo.name}/git hung"
            if got[0] == 0:
                p = pathlib.Path(got[1]).resolve()
                ok = p == repo if what.endswith("toplevel") else p.is_relative_to(d)
                if not ok:
                    return f"{repo.name}/{what}={got[1]}"
        wt = pin_git(repo, "config", "--local", "--no-includes", "--get", "core.worktree", ceiling=d.parent)
        if wt is None:
            return f"{repo.name}/git hung"
        val = wt[1] if wt[0] == 0 else ""
        if val:
            p = pathlib.Path(val)
            if (p if p.is_absolute() else repo / p).resolve() != repo:
                return f"{repo.name}/core.worktree={val}"
    return None

def symlink_breach(d):
    """Round 43 leg h (R42CritC1Counter V2b): no symlink under a fixture may resolve outside it."""
    d = d.resolve()
    for top, dirs, files in os.walk(d):
        for name in dirs + files:
            p = pathlib.Path(top) / name
            if p.is_symlink() and not p.resolve().is_relative_to(d):
                return f"symlink {p.relative_to(d)} -> {os.readlink(p)}"
    return None

def argv_shape_breach(tool, argv):
    """Round-44 F3 (`R43SentinelCounter` F3, `R43CritC1Counter` V2'): the argv must use the tool's options exactly
    as the module contract writes them, so no argparse abbreviation or `--opt=value` form can bypass a leg. An
    order argv is exactly `["--lane", v, "--claims", v, "--receipt", v]`, an argv that leaves one flag out (or adds
    one) included; an anchor argv uses only `--lane V`, `--evidence-ref V`, `--verbose`."""
    if tool == "order":
        if len(argv) != 6 or tuple(argv[0::2]) != ORDER_SHAPE:
            return f"order argv is not the contract shape {list(ORDER_SHAPE)}: {argv}"
        return None
    k = 0
    while k < len(argv):
        t = argv[k]
        if t not in ANCHOR_OPTS:
            return f"anchor argv token {t!r} is not an exact option"
        k += 2 if ANCHOR_OPTS[t] else 1
    return None

def order_argv_breach(d, argv):
    """Round 43 leg i (R42CritC1Counter §1 substitutes): an order fixture's `--claims` and `--receipt` must each
    name a BLOB at HEAD of the `--lane` repo when that path exists at HEAD at all (a missing path stays the tool's
    own setup error, exit 2; a directory standing in for a file is refused here). Round 44: the argv is the exact
    contract shape (checked first, `argv_shape_breach`), and the git call is bounded (F4/F6)."""
    vals = dict(zip(argv[0::2], argv[1::2]))
    lane = pathlib.Path(vals.get("--lane", "."))
    lane = lane if lane.is_absolute() else d / lane
    for opt in ("--claims", "--receipt"):
        got = pin_git(lane, "cat-file", "-t", f"HEAD:{vals[opt]}", ceiling=d.resolve().parent)
        if got is None:
            return f"{opt} git hung"
        if got[0] == 0 and got[1] != "blob":
            return f"{opt} {vals[opt]} is a {got[1]} at HEAD, not a blob"
    return None

def lane_breach(d, argv):
    """Round-44 F2/F6 remediation (`R43SentinelCounter` F2 "derive the repos from the argv"): the repo the tool
    will adopt from `--lane` — found by git's own discovery, with no ceiling below the host root, exactly as the
    tool run discovers it up to its scratch-root ceiling — must have its toplevel and its git dir inside `d`. A
    `--lane` that is no repo at all stays the tool's own setup error."""
    vals = dict(zip(argv[0::2], argv[1::2]))
    if "--lane" not in vals:
        return None
    lane = pathlib.Path(vals["--lane"])
    lane = (lane if lane.is_absolute() else d / lane).resolve()
    if not lane.is_dir():
        return None
    d = d.resolve()
    for args in (("rev-parse", "--show-toplevel"), ("rev-parse", "--absolute-git-dir")):
        try:
            r = subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True, env=PIN_CHECK_ENV,
                               stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT)
        except subprocess.TimeoutExpired:
            return "--lane git hung"
        if r.returncode == 0 and not pathlib.Path(r.stdout.strip()).resolve().is_relative_to(d):
            return f"--lane {' '.join(args)}={r.stdout.strip()} is outside the fixture"
    return None

# --- round-45 control adapter: the round-44 counter's fence, in the round-44 order (build_battery) ---
def breach(d, argv, tool):
    d = pathlib.Path(d)
    return (argv_shape_breach(tool, argv) or lane_breach(d, argv) or repo_breach(d) or symlink_breach(d)
            or (order_argv_breach(d, argv) if tool == "order" else None))

