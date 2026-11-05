import importlib.util, json, subprocess
from pathlib import Path

L = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
spec = importlib.util.spec_from_file_location("probe", L / "plans/round86_raman_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

work = Path("/fast/scratch/hyaku/kengaku-r86/SentinelR86/import-demo")
case = work / "case"
(case / "app").mkdir(parents=True, exist_ok=True)
(case / "app" / "appmod.py").write_text("MARKER = 'from-/app'\n", encoding="utf-8")
(case / "app" / "results.json").write_text('{"G": {"x0": 1580.3}}\n', encoding="utf-8")

HARNESS = '''import json, os, sys
print(json.dumps({
    "sys_path": sys.path,
    "cwd": os.getcwd(),
    "argv0_dir_import": _try_import_appmod(),
    "appmod": _marker(),
    "tests_dir_import": _try_import_tests(),
})) if False else None
'''
# simpler, explicit
HARNESS = '''
import json, os, sys

def attempt(name):
    try:
        mod = __import__(name)
    except BaseException as error:
        return type(error).__name__ + ": " + str(error)
    return "IMPORTED " + str(getattr(mod, "MARKER", getattr(mod, "__file__", "?")))

report = {
    "sys_path": sys.path,
    "cwd": os.getcwd(),
    "import_appmod": attempt("appmod"),
    "import_results": attempt("results"),
    "import_test_outputs": attempt("test_outputs"),
    "python": sys.version.split()[0],
    "isolated": sys.flags.isolated,
}
print(json.dumps(report))
'''
(case / "harness.py").write_text(HARNESS, encoding="utf-8")

argv = probe.sandbox_argv(L / probe.CAP, case)
out = subprocess.run(argv, capture_output=True, text=True)
print("rc:", out.returncode)
print(out.stdout)
print("stderr:", out.stderr.strip()[:600])
