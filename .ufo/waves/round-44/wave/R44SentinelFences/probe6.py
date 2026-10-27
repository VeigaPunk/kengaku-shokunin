#!/usr/bin/env python3
"""Probe 6: what the fence-shaped git calls do on the two admission shapes (malformed outside include, include
that sets a worktree outside d) and on a bare-shaped config."""
import json, pathlib, shutil, subprocess, sys

S = pathlib.Path(sys.argv[1]).resolve()
base = S / "p6"
if base.exists():
    shutil.rmtree(base)
dest = base / "fx" / "mod"
dest.mkdir(parents=True)
ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/nonexistent",
       "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
       "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
       "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
       "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}
PIN = dict(ENV, GIT_CONFIG_COUNT="4", GIT_CONFIG_KEY_0="core.fsmonitor", GIT_CONFIG_VALUE_0="false",
           GIT_CONFIG_KEY_1="core.hooksPath", GIT_CONFIG_VALUE_1="/dev/null",
           GIT_CONFIG_KEY_2="gpg.program", GIT_CONFIG_VALUE_2="/bin/true",
           GIT_CONFIG_KEY_3="log.showSignature", GIT_CONFIG_VALUE_3="false")
out = {}


def run(*a):
    r = subprocess.run([str(x) for x in a], capture_output=True, text=True, env=PIN)
    return [r.returncode, r.stdout.strip()[:300], r.stderr.strip()[:300]]


def repo(path, tag):
    path.mkdir(parents=True)
    run("git", "-C", path, "init", "-q", "-b", "master")
    (path / "x.txt").write_text("x\n")
    run("git", "-C", path, "add", "-A"); run("git", "-C", path, "commit", "-qm", tag)
    return path


# (1) malformed include outside d
d1 = dest / "f000"
r1 = repo(d1 / "lane", "one")
bad = dest / "broken.cfg"
bad.write_text("[this line is not config\n")
with open(r1 / ".git/config", "a") as fh:
    fh.write(f"[include]\n\tpath = {bad}\n")
out["malformed_include"] = {
    "rev_parse": run("git", "-C", r1, "rev-parse", "--show-toplevel"),
    "absolute_git_dir": run("git", "-C", r1, "rev-parse", "--absolute-git-dir"),
    "config_scan": run("git", "-C", r1, "config", "--local", "--no-includes", "--get-regexp", r"^include(if)?\."),
}

# (2) include sets an existing worktree outside d
d2 = dest / "f001"
r2 = repo(d2 / "lane", "two")
wt = dest / "outside-wt"
wt.mkdir()
side = dest / "outside.cfg"
side.write_text(f"[co" + f"re]\n\tworktree = {wt}\n")
with open(r2 / ".git/config", "a") as fh:
    fh.write(f"[include]\n\tpath = {side}\n")
out["include_sets_worktree"] = {
    "rev_parse": run("git", "-C", r2, "rev-parse", "--show-toplevel"),
    "config_scan": run("git", "-C", r2, "config", "--local", "--no-includes", "--get-regexp", r"^include(if)?\."),
    "worktree_read": run("git", "-C", r2, "config", "--local", "--no-includes", "--get", "co" + "re.worktree"),
}

# (3) bare-shaped config
d3 = dest / "f002"
r3 = repo(d3 / "lane", "three")
run("git", "-C", r3, "config", "core.bare", "true")
out["bare_shape"] = {
    "rev_parse": run("git", "-C", r3, "rev-parse", "--show-toplevel"),
    "absolute_git_dir": run("git", "-C", r3, "rev-parse", "--absolute-git-dir"),
    "config_scan": run("git", "-C", r3, "config", "--local", "--no-includes", "--get-regexp", r"^include(if)?\."),
    "worktree_read": run("git", "-C", r3, "config", "--local", "--no-includes", "--get", "co" + "re.worktree"),
}
print(json.dumps(out, indent=1))
