#!/usr/bin/env python3
"""Probe 4: reproduce the commondir fixture by hand and run order_check exactly as the counter's tool run does
(cwd=d, sandbox env shape), printing rc/stdout/stderr."""
import json, pathlib, shutil, subprocess, sys

S = pathlib.Path(sys.argv[1]).resolve()
LANE = S / "lane"
base = S / "p4"
if base.exists():
    shutil.rmtree(base)
dest = base / "fx" / "mod"
d = dest / "f000"
d.mkdir(parents=True)
CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"
ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": str(base / "home"),
       "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
       "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
       "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
       "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}
bench = str(base.parent)
TOOL_ENV = dict(ENV, GIT_CEILING_DIRECTORIES=bench,
                GIT_CONFIG_COUNT="4", GIT_CONFIG_KEY_0="core.fsmonitor", GIT_CONFIG_VALUE_0="false",
                GIT_CONFIG_KEY_1="core.hooksPath", GIT_CONFIG_VALUE_1="/dev/null",
                GIT_CONFIG_KEY_2="gpg.program", GIT_CONFIG_VALUE_2="/bin/true",
                GIT_CONFIG_KEY_3="log.showSignature", GIT_CONFIG_VALUE_3="false")
(base / "home").mkdir()


def run(*a, cwd=None, env=None):
    r = subprocess.run([str(x) for x in a], capture_output=True, text=True, env=env or ENV, cwd=cwd)
    return [r.returncode, r.stdout.strip()[:400], r.stderr.strip()[:400]]


store = dest / "storeA"
store.mkdir()
run("git", "-C", store, "init", "-q", "-b", "master")
(store / CLAIMS).parent.mkdir(parents=True)
(store / CLAIMS).write_text("nothing ran\n")
run("git", "-C", store, "add", "-A"); run("git", "-C", store, "commit", "-qm", "claims")
(store / RECEIPT).parent.mkdir(parents=True)
(store / RECEIPT).write_text("receipt\n")
run("git", "-C", store, "add", "-A"); run("git", "-C", store, "commit", "-qm", "receipt")

gd = d / "lane" / ".git"
gd.mkdir(parents=True)
(gd / "commondir").write_text(str(store / ".git") + "\n")
(gd / "HEAD").write_text("ref: refs/heads/master\n")
out = {
    "to": run("git", "-C", d / "lane", "rev-parse", "--show-toplevel", env=TOOL_ENV),
    "gd": run("git", "-C", d / "lane", "rev-parse", "--absolute-git-dir", env=TOOL_ENV),
    "log": run("git", "-C", d / "lane", "log", "--format=%H %s", env=TOOL_ENV),
    "ls_tree": run("git", "-C", d / "lane", "ls-tree", "-r", "--name-only", "HEAD", env=TOOL_ENV),
    "cat": run("git", "-C", d / "lane", "cat-file", "-t", f"HEAD:{RECEIPT}", env=TOOL_ENV),
}
run("git", "-C", store, "config", "user.email", "STORE-MARKER@invalid")
out["store_config_via_parent_shape"] = run("git", "-C", d / "lane", "config", "--local", "--no-includes", "--get", "user.email", env=TOOL_ENV)
out["d_lane_files"] = sorted(str(p.relative_to(d)) for p in (d / "lane").rglob("*"))
out["order_check"] = run("/usr/bin/python3", LANE / "plans/order_check.py", "--lane", "lane",
                         "--claims", CLAIMS, "--receipt", RECEIPT, cwd=d, env=TOOL_ENV)
print(json.dumps(out, indent=1))
