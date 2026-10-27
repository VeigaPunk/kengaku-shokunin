#!/usr/bin/env python3
"""Probe 7: reproduce the anchor commondir fixture by hand; run the anchor tool in the tool-run shape and show
rc/stdout/stderr, plus the git answers the tool's calls get."""
import json, pathlib, shutil, subprocess, sys

S = pathlib.Path(sys.argv[1]).resolve()
LANE = S / "lane"
base = S / "p7"
if base.exists():
    shutil.rmtree(base)
dest = base / "fx" / "mod"
d = dest / "f000"
d.mkdir(parents=True)
ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": str(base / "home"),
       "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
       "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
       "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
       "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}
(base / "home").mkdir()
TOOL_ENV = dict(ENV, GIT_CEILING_DIRECTORIES=str(base),
                GIT_CONFIG_COUNT="4", GIT_CONFIG_KEY_0="core.fsmonitor", GIT_CONFIG_VALUE_0="false",
                GIT_CONFIG_KEY_1="core.hooksPath", GIT_CONFIG_VALUE_1="/dev/null",
                GIT_CONFIG_KEY_2="gpg.program", GIT_CONFIG_VALUE_2="/bin/true",
                GIT_CONFIG_KEY_3="log.showSignature", GIT_CONFIG_VALUE_3="false")


def run(*a, cwd=None):
    r = subprocess.run([str(x) for x in a], capture_output=True, text=True, env=TOOL_ENV, cwd=cwd)
    return [r.returncode, r.stdout.strip()[:600], r.stderr.strip()[:600]]


store = dest / "storeC"
store.mkdir()
run("git", "-C", store, "init", "-q", "-b", "master")
(store / "note.txt").write_text("x\n")
run("git", "-C", store, "add", "-A"); run("git", "-C", store, "commit", "-qm", "x")
(store / "corpus/evidence/round42").mkdir(parents=True)
(store / "corpus/evidence/round42/x.txt").write_text("capture\n")
run("git", "-C", store, "add", "-A"); run("git", "-C", store, "commit", "-qm", "capture")
(d / ".git").mkdir()
(d / ".git/commondir").write_text(str(store / ".git") + "\n")
(d / ".git/HEAD").write_text("ref: refs/heads/master\n")
(d / "corpus").mkdir()
(d / "corpus/SOURCES.md").write_text("# no rows\n")
out = {
    "dot_git_exists": (d / ".git").exists(),
    "toplevel": run("git", "-C", d, "rev-parse", "--show-toplevel"),
    "ls_tree_evidence": run("git", "-C", d, "ls-tree", "-r", "--name-only", "HEAD", "--", "corpus/evidence"),
    "ls_tree_all": run("git", "-C", d, "ls-tree", "-r", "--name-only", "HEAD"),
    "anchor": run("/usr/bin/python3", LANE / "plans/anchor_digest_check.py", "--lane", ".", cwd=d),
}
print(json.dumps(out, indent=1))
