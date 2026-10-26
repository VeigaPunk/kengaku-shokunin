#!/usr/bin/env python3
"""Clause-isolation mutants for the C1 gate (scratch, wave 1). Each mutant is built in a mktemp git
repo from the genuine round-35 package and run through the gate with --require-clean-tree; the
report names the clause that fires. Nothing outside /tmp is written."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
GATE = LANE / ".ufo/waves/round-36/build/R36GateA/pkg_gate.py"
SPEC = json.loads((LANE / "plans/pkg-spec-r35.json").read_text())


def copy_pkg(dest):
    for rel in [SPEC["entry"], SPEC["receipt"], SPEC["sources"], SPEC["readme"],
                *SPEC["frozen_instruments"]]:
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(LANE / rel, dest / rel)
    shutil.copytree(LANE / SPEC["capture_dir"], dest / SPEC["capture_dir"],
                    ignore=shutil.ignore_patterns("__pycache__"))
    (dest / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
    for p in (LANE / "corpus/knowledge").glob("*.md"):
        shutil.copy2(p, dest / "corpus/knowledge" / p.name)
    (dest / "corpus/lessons").mkdir(parents=True, exist_ok=True)
    for p in (LANE / "corpus/lessons").glob("*.md"):
        shutil.copy2(p, dest / "corpus/lessons" / p.name)


def make(root, name, mutate):
    d = pathlib.Path(tempfile.mkdtemp(prefix=name + "-", dir=root))
    subprocess.run(["git", "-C", str(d), "init", "-q"], check=True)
    copy_pkg(d)
    mutate(d)
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True)
    return d


def run(d, spec=LANE / "plans/pkg-spec-r35.json", extra=("--require-clean-tree",)):
    r = subprocess.run([sys.executable, str(GATE), "package", "--root", str(d), *extra,
                        "--spec", str(spec)], capture_output=True, text=True)
    bad = [l for l in r.stdout.splitlines() if "DEFECT" in l]
    return r.returncode, bad


def edit_line(path, old, new):
    t = path.read_text()
    assert old in t, (path, old)
    path.write_text(t.replace(old, new, 1))


MUTANTS = {
    # (label, mutate)
    "M0-genuine": lambda d: None,
    "M1-receipt-tampered": lambda d: (d / SPEC["receipt"]).write_text(
        (d / SPEC["receipt"]).read_text() + "extra=1\n"),
    "M2-capture-byte": lambda d: (d / SPEC["capture_dir"] / "test.sh").write_text(
        (d / SPEC["capture_dir"] / "test.sh").read_text() + "\n# mutated\n"),
    "M3-source-head-missing": lambda d: (d / SPEC["entry"]).write_text(
        "\n".join((d / SPEC["entry"]).read_text().splitlines()[:2]
                  + (d / SPEC["entry"]).read_text().splitlines()[3:]) + "\n"),
    "M4a-falsifier-label-renamed": lambda d: (d / SPEC["entry"]).write_text(
        (d / SPEC["entry"]).read_text().replace("**Falsifier:**", "**Note:**")),
    "M4b-falsifier-removed": lambda d: (d / SPEC["entry"]).write_text(
        __import__("re").sub(r"\*\*Falsifier:\*\*.*?(?=\n## )", "", (d / SPEC["entry"]).read_text(),
                             flags=__import__("re").S)),
    "M5-index-row-missing": lambda d: (d / SPEC["readme"]).write_text(
        "\n".join(l for l in (d / SPEC["readme"]).read_text().splitlines()
                  if not l.startswith("| `knowledge/tb2-protein-assembly-grader.md`")) + "\n"),
    "M6-sources-row-duplicated": lambda d: (d / SPEC["sources"]).write_text(
        (d / SPEC["sources"]).read_text() + "\n".join(
            l for l in (d / SPEC["sources"]).read_text().splitlines()
            if l.lstrip().startswith("| S106 |")) + "\n"),
    "M7-quote-not-verbatim": lambda d: (d / SPEC["entry"]).write_text(
        (d / SPEC["entry"]).read_text().replace(
            "“assert len(gblock) <= 3000, \"gBlock must be at most 3000 nucleotides.\"”",
            "“assert len(gblock) <= 3001, \"gBlock must be at most 3000 nucleotides.\"”")),
}


def main():
    root = pathlib.Path(tempfile.mkdtemp(prefix="k36-mut-"))
    try:
        for label, mutate in MUTANTS.items():
            if mutate is None:
                continue
            d = make(root, label, mutate)
            rc, bad = run(d)
            print(f"{label}: rc={rc} {'; '.join(bad) if bad else 'accepted'}")
        # P10 isolation: a spec that pins a tampered receipt; the probe's fresh bytes still differ.
        d = make(root, "M9-rerun", lambda d: (d / SPEC["receipt"]).write_text(
            (d / SPEC["receipt"]).read_text().replace("cases=18", "cases=19")))
        spec = json.loads((LANE / "plans/pkg-spec-r35.json").read_text())
        import hashlib
        spec["receipt_sha256"] = hashlib.sha256((d / SPEC["receipt"]).read_bytes()).hexdigest()
        sp = root / "spec-rerun.json"
        sp.write_text(json.dumps(spec))
        rc, bad = run(d, spec=sp, extra=("--rerun",))
        print(f"M9-rerun-receipt-differs: rc={rc} {'; '.join(bad) if bad else 'accepted'}")
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
