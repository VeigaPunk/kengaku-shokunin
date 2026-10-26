#!/usr/bin/env python3
"""Remediation validation: same probe, argv hardened with --unshare-uts/--hostname + --disable-userns.
The frozen module is NOT edited; sandbox_argv is wrapped in memory only.
Usage: probe_remediation.py <lane> <work> [flags-csv]"""
import importlib.util, pathlib, shutil, subprocess, sys, tempfile

LANE, WORK = sys.argv[1], sys.argv[2]
FLAGS = sys.argv[3] if len(sys.argv) > 3 else "--unshare-uts|--hostname|k41sandbox|--disable-userns"
extra = [f for f in FLAGS.split("|") if f]
spec = importlib.util.spec_from_file_location("probe", str(pathlib.Path(LANE) / "plans/constraints_probe.py"))
probe = importlib.util.module_from_spec(spec); sys.modules["probe"] = probe; spec.loader.exec_module(probe)
orig = probe.sandbox_argv
def hardened(cap, work):
    argv = orig(cap, work)
    return [argv[0]] + extra + argv[1:]
probe.sandbox_argv = hardened
print("HARDENED_FLAGS", extra)
sys.argv = ["constraints_probe.py", "--lane", LANE, "--work", WORK]
rc = probe.main()
print("MAIN_RC", rc)
sys.exit(rc)
