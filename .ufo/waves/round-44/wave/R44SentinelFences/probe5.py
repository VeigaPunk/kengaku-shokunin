#!/usr/bin/env python3
"""Probe 5: (a) the second config file's include is invisible to the store fence's two config calls but parsed
by every other git call; (b) a primary-config include makes lane_breach's rev-parse (no --no-includes) parse a
file outside d before repo_breach refuses; (c) a commondir can name ANY absolute git dir on the host."""
import json, pathlib, shutil, subprocess, sys

S = pathlib.Path(sys.argv[1]).resolve()
LANE = S / "lane"
base = S / "p5"
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


def run(*a, env=None):
    r = subprocess.run([str(x) for x in a], capture_output=True, text=True, env=env or PIN)
    return [r.returncode, r.stdout.strip()[:300], r.stderr.strip()[:300]]


def repo(path):
    path.mkdir(parents=True)
    run("git", "-C", path, "init", "-q", "-b", "master")
    (path / "x.txt").write_text("x\n")
    run("git", "-C", path, "add", "-A")
    run("git", "-C", path, "commit", "-qm", "x")
    return path


# (a) second config file include, exactly the built fixture's shape
d = dest / "f000"
d.mkdir()
side = dest / "outside.cfg"
side.write_text("[user]\n\temail = OUTSIDE-MARKER@invalid\n")
r = repo(d / "lane")
run("git", "-C", r, "config", "extensions.worktreeConfig", "true")
(r / ".git/config.worktree").write_text(f"[include]\n\tpath = {side}\n")
out["a_second_config"] = {
    "fence_scan": run("git", "-C", r, "config", "--local", "--no-includes", "--get-regexp", r"^include(if)?\."),
    "fence_worktree": run("git", "-C", r, "config", "--local", "--no-includes", "--get", "co" + "re.worktree"),
    "any_parse": run("git", "-C", r, "config", "--get", "user.email"),
    "lane_rev_parse": run("git", "-C", r, "rev-parse", "--show-toplevel"),
    "git_common_dir": run("git", "-C", r, "rev-parse", "--git-common-dir"),
}

# (a2) same file, but the include sets a worktree: the parsed value appears in rev-parse's answer
d2 = dest / "f001"
d2.mkdir()
r2 = repo(d2 / "lane")
run("git", "-C", r2, "config", "extensions.worktreeConfig", "true")
(r2 / ".git/config.worktree").write_text(f"[include]\n\tpath = {side}\n[co" + "re]\n\tworktree = {dest}/outside-wt\n".replace("{dest}", str(dest)))
out["a2_second_config_worktree"] = {
    "fence_scan": run("git", "-C", r2, "config", "--local", "--no-includes", "--get-regexp", r"^include(if)?\."),
    "rev_parse": run("git", "-C", r2, "rev-parse", "--show-toplevel"),
}

# (b) primary-config include: which check speaks first, and what did it read
d3 = dest / "f002"
d3.mkdir()
r3 = repo(d3 / "lane")
with open(r3 / ".git/config", "a") as fh:
    fh.write(f"[co" + "re]\n\tworktree = {dest}/outside-wt\n[include]\n\tpath = {side}\n")
out["b_primary_include"] = {
    "lane_rev_parse": run("git", "-C", r3, "rev-parse", "--show-toplevel"),
    "fence_scan": run("git", "-C", r3, "config", "--local", "--no-includes", "--get-regexp", r"^include(if)?\."),
}

# (c) commondir naming an absolute git dir outside the scratch tree entirely
d4 = dest / "f003"
(d4 / "lane/.git").mkdir(parents=True)
(d4 / "lane/.git/commondir").write_text(str(LANE / ".git") + "\n")
(d4 / "lane/.git/HEAD").write_text("ref: refs/heads/master\n")
out["c_commondir_absolute"] = {
    "show_toplevel": run("git", "-C", d4 / "lane", "rev-parse", "--show-toplevel"),
    "absolute_git_dir": run("git", "-C", d4 / "lane", "rev-parse", "--absolute-git-dir"),
    "common_dir": run("git", "-C", d4 / "lane", "rev-parse", "--git-common-dir"),
    "cat_file_lane_head": run("git", "-C", d4 / "lane", "cat-file", "-t", "HEAD:README.md"),
    "log_head": run("git", "-C", d4 / "lane", "log", "--format=%s", "-1"),
}
print(json.dumps(out, indent=1))
