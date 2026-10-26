#!/usr/bin/env python3
"""F38CritOverclaim counterexample: a NON-ELF fabricated artefact passes all four
`build-pmars` tests when `ldd` resolves earlier on PATH.

Reads the lane's frozen probe module only for `sandbox_argv()` and `HARNESS_PY`
(the same bwrap argv the receipt's cases use) and the pinned capture; stages one
state the frozen 22-case table has no case for:

  /usr/local/bin/pmars  a bash script printing fixed debugger/battle text (not ELF)
  /usr/local/bin/ldd    a bash script, exit 0, no output (shadows /usr/bin/ldd,
                        because Debian's default PATH puts /usr/local/bin first)

  usage: python3 nonelf-ldd-wrapper-probe.py [--lane DIR]   (default: lane root)
"""
import argparse
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile


def load_probe(lane):
    spec = importlib.util.spec_from_file_location("bp", lane / "plans/build_pmars_probe.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["bp"] = mod
    spec.loader.exec_module(mod)
    return mod


PMARS_SH = """#!/bin/bash
for a in "$@"; do
  if [ "$a" = "-b" ]; then printf 'rave scores 12\\nResults: 12 34 78\\n'; exit 0; fi
done
printf '00000   SPL.B  $     2, $     0\\n00001   MOV.I  $     0, $     1\\n'
exit 0
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=str(pathlib.Path(__file__).resolve().parents[5]))
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    bp = load_probe(lane)
    cap = lane / bp.CAP
    work = pathlib.Path(tempfile.mkdtemp(prefix="f38nonelf-"))
    try:
        (work / "ulb").mkdir()
        (work / "ulsb").mkdir()
        (work / "app/pmars-0.9.4/debian").mkdir(parents=True)
        (work / "app/pmars-0.9.4/src").mkdir(parents=True)
        (work / "app/pmars-0.9.4/src/dummy.c").write_bytes(b"")
        pm = work / "ulb/pmars"
        pm.write_text(PMARS_SH)
        os.chmod(pm, 0o755)
        ld = work / "ulb/ldd"
        ld.write_text("#!/bin/bash\nexit 0\n")
        os.chmod(ld, 0o755)
        (work / "harness.py").write_text(bp.HARNESS_PY)
        env = {"PATH": bp.PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        r = subprocess.run(bp.sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py"],
                           env=env, capture_output=True, text=True, timeout=180)
        print(f"# capture {bp.CAP}/test_outputs.py sha256={bp.sha256(cap / 'test_outputs.py')}")
        print("# state: pmars = bash script (file(1) cannot be ELF), ldd = bash script exit 0")
        print(f"harness rc={r.returncode}")
        print(r.stdout, end="")
        d = subprocess.run(bp.sandbox_argv(cap, work) +
                           ["/usr/bin/bash", "-c",
                            "command -v pmars; command -v ldd; ldd /usr/local/bin/pmars; echo ldd_rc=$?"],
                           env=env, capture_output=True, text=True)
        print("# PATH resolution inside the same sandbox:")
        print(d.stdout, end="")
        verdicts = [l.split() for l in r.stdout.splitlines() if l.startswith("TEST ")]
        ok = r.returncode == 0 and len(verdicts) == 4 and all(v[2] == "P" for v in verdicts)
        print(f"ALL_FOUR={ok}")
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
