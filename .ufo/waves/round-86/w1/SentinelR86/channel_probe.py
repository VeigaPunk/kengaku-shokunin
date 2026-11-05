import importlib.util, json, os
from pathlib import Path

L = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
spec = importlib.util.spec_from_file_location("probe", L / "plans/round86_raman_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

work = Path("/fast/scratch/hyaku/kengaku-r86/SentinelR86/channel-demo")
(work / "staged").mkdir(parents=True, exist_ok=True)
forged = work / "staged/test_outputs.py"
forged.write_text(
    "import json, os, sys\n"
    "print(json.dumps({'tests': [['test_result_file_exists', 'P', ''],"
    " ['test_G_Peak', 'P', ''], ['test_2D_Peak', 'P', '']]}))\n"
    "sys.stdout.flush()\n"
    "os._exit(0)\n",
    encoding="utf-8")

payload = probe.run_case(forged, work, None)
print("accepted payload:", json.dumps(payload))
print("observed vector the probe would record:",
      "/".join(row[1] for row in payload["tests"]))

# the same bytes through the front door, which is where the sha pin lives
try:
    probe.load_inputs(L)
except probe.SetupDefect as error:
    print("load_inputs refused a same-shaped lane? ", error)
try:
    import subprocess, sys
    out = subprocess.run([sys.executable, "-I", "-B", str(L / "plans/round86_raman_probe.py"),
                          "--lane", str(L), "--work", str(work / "w")],
                         capture_output=True, text=True)
    print("probe with a hostile staged capture (via --lane is not possible) rc:", out.returncode)
except Exception as error:
    print("probe error", error)
