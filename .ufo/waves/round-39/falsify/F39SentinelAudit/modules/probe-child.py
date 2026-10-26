"""F39SentinelAudit: what the audit's build child is allowed to do (run via --build-module)."""
import json, os, socket, subprocess, sys, pathlib
rec = {"argv": sys.argv, "cwd": os.getcwd(), "home": os.path.expanduser("~"),
       "ssh_key_readable": os.access(os.path.expanduser("~/.ssh/id_ed25519"), os.R_OK),
       "lane_git_head_readable": os.access(sys.argv[sys.argv.index("--lane") + 1] + "/.git/HEAD", os.R_OK),
       "lane_file_writable": os.access(sys.argv[sys.argv.index("--lane") + 1] + "/LOG.md", os.W_OK),
       "env_keys": len(os.environ),
       "env_agentish": sorted(k for k in os.environ if k in ("SSH_AUTH_SOCK", "DISPLAY", "XDG_RUNTIME_DIR", "AWS_PROFILE", "GNUPGHOME"))}
try:
    s = socket.create_connection(("1.1.1.1", 53), 3); rec["net"] = "REACHED"; s.close()
except OSError as e:
    rec["net"] = f"{type(e).__name__}:{e.errno}"
pathlib.Path("/fast/scratch/hyaku/kengaku-r39/F39SentinelAudit/child-escape.txt").write_text("wrote outside dest\n")
g = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(90)"], start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
rec["grandchild_pid"] = g.pid
print("PROBE " + json.dumps(rec), flush=True)
