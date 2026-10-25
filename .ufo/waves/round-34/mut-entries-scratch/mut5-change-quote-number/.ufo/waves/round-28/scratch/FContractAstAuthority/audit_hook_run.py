"""Run the lane instrument CLI against the scratch root under a PEP 578 audit hook and record effects."""
import collections
import json
import runpy
import sys
from pathlib import Path

SCRIPT, ROOT, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3])
sys.dont_write_bytecode = True
events = collections.defaultdict(list)
armed = False


def hook(event, args):
    if not armed:
        return
    if event == "open":
        events["open"].append(str(args[0]))
    elif event == "import":
        events["import"].append(args[0])
    elif event == "compile":
        events["compile"].append(str(args[1]))
    elif event == "exec":
        events["exec"].append(getattr(args[0], "co_filename", repr(args[0])))
    elif event.startswith(("socket.", "subprocess.", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "urllib.", "http.", "ctypes.", "os.remove", "os.rename", "shutil.")):
        events[event].append(repr(args)[:200])
    elif event in ("builtins.input", "os.chmod", "os.mkdir", "os.truncate", "os.unlink"):
        events[event].append(repr(args)[:200])


sys.addaudithook(hook)
sys.argv = [SCRIPT, "--root", ROOT, "--json"]
stdout = sys.stdout
sys.stdout = open(OUT.with_suffix(".stdout.json"), "w")
armed = True
try:
    runpy.run_path(SCRIPT, run_name="__main__")
except SystemExit as exit_:
    code = exit_.code
armed = False
sys.stdout.close()
sys.stdout = stdout
opened = sorted(set(events["open"]))
summary = {
    "exit": code,
    "non_stdlib_opens": [p for p in opened if "/usr/lib/python" not in p],
    "imports": sorted(set(events["import"])),
    "compile_sources": collections.Counter(events["compile"]),
    "exec_code_files": collections.Counter(events["exec"]),
    "process_network_fs_mutation_events": {k: v for k, v in events.items() if k not in ("open", "import", "compile", "exec")},
}
OUT.write_text(json.dumps(summary, indent=1, default=list))
print(json.dumps(summary, indent=1, default=list))
