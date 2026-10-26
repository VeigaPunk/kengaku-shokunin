#!/usr/bin/env python3
"""Round 36, seat R36ProbeHarnessMut: generate and run five probe-harness mutants.

Builds a mini lane tree from the lane's committed probe + capture, then for each mutant makes an
independent copy, applies named string mutations (each asserted to hit exactly once), runs the probe
with `--lane .`, and records stdout + exit code. Nothing outside this build directory is touched.
"""
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
MINI = HERE / "mini"
PROBE_REL = "plans/regex_log_probe.py"
CAP_REL = "corpus/evidence/round36/tb2-regex-log"
CAP_FILES = ["test_outputs.py", "test.sh", "instruction.md", "task.toml", "solve.sh", "SHA256SUMS"]
LOGS = HERE / "logs"

MUTANTS = {
    "m1-path-patch-broken": [
        (PROBE_REL,
         "        real = pathlib.Path\n"
         "        mod.Path = lambda _arg: real(p)  # the grader hard-codes /app/regex.txt\n",
         "        real = pathlib.Path\n"
         "        mod.Path = real  # MUTANT m1: no patch, grader reads the real /app/regex.txt\n"),
    ],
    "m2-every-case-reference": [
        (PROBE_REL,
         "def build_cases():\n",
         "REF = line_rx(ip(), date())  # MUTANT m2: the reference lenient regex\n\n\n"
         "def build_cases():\n"),
        (PROBE_REL,
         "            p.write_text(regex)\n",
         "            p.write_text(REF)  # MUTANT m2: every case gets the reference regex\n"),
    ],
    "m3-flip-one-prediction": [
        (PROBE_REL,
         'add("padded-file", "  " + line_rx(base_ip, date()) + " \\n\\n", "pass",',
         'add("padded-file", "  " + line_rx(base_ip, date()) + " \\n\\n", "fail",  # MUTANT m3: flipped'),
    ],
    "m4-tamper-one-byte": [
        (f"{CAP_REL}/test_outputs.py",
         '\n        "1999-03-05",\n',
         '\n        "1999-03-06",\n'),
    ],
    "m5-tmp-path-leaks": [
        (PROBE_REL,
         '            first = (str(e).splitlines() or ["AssertionError"])[0].replace(d, "<tmp>")\n',
         '            first = (str(e).splitlines() or ["AssertionError"])[0]  # MUTANT m5: no <tmp> scrub\n'),
    ],
}


def build_mini():
    if MINI.exists():
        shutil.rmtree(MINI)
    (MINI / "plans").mkdir(parents=True)
    (MINI / CAP_REL).mkdir(parents=True)
    shutil.copy2(LANE / PROBE_REL, MINI / PROBE_REL)
    for f in CAP_FILES:
        shutil.copy2(LANE / CAP_REL / f, MINI / CAP_REL / f)
    # the capture's .gitignore'd bytecode is not copied; the probe writes it on first run


def make_copy(name):
    d = HERE / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(MINI, d)
    for rel, old, new in MUTANTS.get(name, []):
        f = d / rel
        text = f.read_text()
        hits = text.count(old)
        if hits != 1:
            raise SystemExit(f"{name}: pattern hits={hits} in {rel} (want 1): {old!r}")
        f.write_text(text.replace(old, new))
    return d


def run(d):
    p = subprocess.run([sys.executable, "plans/regex_log_probe.py", "--lane", "."],
                       cwd=d, capture_output=True, text=True)
    return p.stdout, p.stderr, p.returncode


def main():
    LOGS.mkdir(exist_ok=True)
    build_mini()
    summary = []
    # m0 = unmodified control in the same fixture tree, run twice
    m0 = make_copy("m0-unmodified")
    o1, e1, rc1 = run(m0)
    o2, e2, rc2 = run(m0)
    (LOGS / "m0-run1.txt").write_text(o1)
    (LOGS / "m0-run2.txt").write_text(o2)
    receipt = (LANE / "corpus/evidence/round36/regex-log-probe.txt").read_text()
    summary.append(("m0-unmodified", rc1, f"byte_equal_receipt={o1 == receipt} "
                     f"two_runs_equal={o1 == o2} stderr={e1!r}"))
    for name in MUTANTS:
        d = make_copy(name)
        out, err, rc = run(d)
        (LOGS / f"{name}.txt").write_text(out + (f"\nSTDERR={err!r}\n" if err else ""))
        last = [l for l in out.strip().splitlines() if l.startswith("cases=")]
        refuse = [l for l in out.splitlines() if l.startswith("REFUSE")]
        summary.append((name, rc, (last[-1] if last else (refuse[0] if refuse else out.strip()[:120]))))
    # m5 determinism: second run of the same mutant tree, then diff the two logs
    o_a, _, rc_a = run(HERE / "m5-tmp-path-leaks")
    (LOGS / "m5-run2.txt").write_text(o_a)
    same = (LOGS / "m5-tmp-path-leaks.txt").read_text().startswith(o_a)
    summary.append(("m5-tmp-path-leaks(2nd)", rc_a, f"two_runs_byte_equal={same}"))
    # m4 forensic: how many bytes differ between the tampered grader and the capture
    tam = (HERE / "m4-tamper-one-byte" / CAP_REL / "test_outputs.py").read_bytes()
    ori = (LANE / CAP_REL / "test_outputs.py").read_bytes()
    diff = [(i, ori[i:i + 1], tam[i:i + 1]) for i in range(min(len(ori), len(tam))) if ori[i] != tam[i]]
    summary.append(("m4-forensics", 0, f"len_equal={len(ori) == len(tam)} byte_diffs={[(i, a.decode('latin-1'), b.decode('latin-1')) for i, a, b in diff]}"))
    print("\n".join(f"{n}\trc={r}\t{s}" for n, r, s in summary))


if __name__ == "__main__":
    main()
