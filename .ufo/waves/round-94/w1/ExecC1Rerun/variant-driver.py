#!/usr/bin/env python3
"""Report-only portability variants of the frozen probe (ExecC1Rerun scratch; never a claim leg).

Imports plans/round94_compressor_probe.py read-only from the shared clone and monkeypatches
two module globals in memory: the reference build (rustc opt level) and the grader's compile
of decomp.c (gcc -> clang or gcc -O3). The lane files and the frozen PINS are untouched.

Usage: driver.py <variant> <lane> <work>
  variant: rustcO | clang | rustcO+clang | gcc-O3
"""
import importlib.util
import sys
from pathlib import Path

variant, lane, work = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
spec = importlib.util.spec_from_file_location("probe", lane / "plans" / "round94_compressor_probe.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)

GCC_CALL = '["gcc", "-o", "decomp2", "decomp.c"]'


def build_reference_opt(bwrap, cap, work_dir):
    ref = work_dir / "ref"
    if ref.exists():
        P.shutil.rmtree(ref)
    ref.mkdir(parents=True)
    solve = (cap / "solution" / "solve.sh").read_text()
    (ref / "main.rs").write_text(P.heredoc(solve, "cat <<'EOF' > main.rs"))
    P.shutil.copy2(cap / "environment" / "data.txt", ref / "data.txt")
    script = "rustc -O main.rs -o main && cat data.txt | ./main > data.comp"
    proc = P.subprocess.run(P.sandbox(bwrap, [("--bind", str(ref), "/work")], "/work", ["/usr/bin/sh", "-c", script]),
                            capture_output=True, text=True, timeout=P.CASE_TIMEOUT)
    comp = ref / "data.comp"
    if proc.returncode != 0 or not comp.is_file():
        raise SystemExit("VARIANT reference build failed rc=%d %s" % (proc.returncode, proc.stderr.strip()[-200:]))
    return comp.read_bytes()


def patch_grader(replacement):
    orig_stage = P.stage

    def stage(case, cap, ref, root):
        app, tests, size = orig_stage(case, cap, ref, root)
        target = tests / "test_outputs.py"
        text = target.read_text()
        assert text.count(GCC_CALL) == 1, "grader compile call not found exactly once"
        target.write_text(text.replace(GCC_CALL, replacement))
        return app, tests, size

    P.stage = stage


if "rustcO" in variant:
    P.build_reference = build_reference_opt
if "clang" in variant:
    patch_grader('["clang", "-o", "decomp2", "decomp.c"]')
if variant == "gcc-O3":
    patch_grader('["gcc", "-O3", "-o", "decomp2", "decomp.c"]')

print("VARIANT " + variant)
sys.exit(P.main(["--lane", str(lane), "--work", work]))
