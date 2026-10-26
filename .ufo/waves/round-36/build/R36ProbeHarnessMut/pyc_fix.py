#!/usr/bin/env python3
"""Round 36, seat R36ProbeHarnessMut — operable repair demo for the pyc-substitution limit (m6).

m7 loads the pinned grader SOURCE bytes with compile()+exec into a namespace, so no `__pycache__`
entry is consulted and none is written. Run against the same forged-pyc fixture as m6; if the repair
works the poisoned cache is ignored (8 pass / 16 fail / mismatches=0, rc 0) and no pyc is created.
"""
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
MINI = HERE / "mini"
LOGS = HERE / "logs"
PROBE_REL = "plans/regex_log_probe.py"
CAP_REL = "corpus/evidence/round36/tb2-regex-log"

OLD = """    spec = importlib.util.spec_from_file_location("tb2_regex_log_grader", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
"""
NEW = """    import types as _types

    src = pathlib.Path(mod_path).read_bytes()
    mod = _types.ModuleType("tb2_regex_log_grader")
    mod.__file__ = str(mod_path)
    # MUTANT m7: compile the pinned bytes; no __pycache__ entry is consulted or written
    exec(compile(src, str(mod_path), "exec"), mod.__dict__)
"""


def main():
    LOGS.mkdir(exist_ok=True)
    d = HERE / "m7-source-exec-repair"
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(MINI, d)
    f = d / PROBE_REL
    text = f.read_text()
    assert text.count(OLD) == 1, "loader block not found once"
    f.write_text(text.replace(OLD, NEW))
    # plant the SAME forged pyc that defeated the digest pin in m6
    src_pyc = (HERE / "m6-pyc-substitution" / CAP_REL / "__pycache__"
               / f"test_outputs.cpython-{sys.version_info.major}{sys.version_info.minor}.pyc")
    dst_dir = d / CAP_REL / "__pycache__"
    dst_dir.mkdir(exist_ok=True)
    shutil.copy2(src_pyc, dst_dir / src_pyc.name)
    runs = []
    for i in (1, 2):
        p = subprocess.run([sys.executable, "plans/regex_log_probe.py", "--lane", "."],
                           cwd=d, capture_output=True, text=True)
        (LOGS / f"m7-run{i}.txt").write_text(p.stdout)
        runs.append((p.stdout, p.returncode, p.stderr))
    last = [l for l in runs[0][0].strip().splitlines() if l.startswith("cases=")]
    created = sorted(x.name for x in (d / CAP_REL / "__pycache__").iterdir())
    print(f"m7-source-exec-repair\trc={runs[0][1]}\t{last[-1]}")
    print(f"two_runs_byte_equal={runs[0][0] == runs[1][0]}\tstderr={runs[0][2]!r}")
    print(f"pycache_after_runs={created}  (only the planted forged file should remain)")
    print(f"matches_committed_receipt={runs[0][0] == pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round36/regex-log-probe.txt').read_text()}")


if __name__ == "__main__":
    main()
