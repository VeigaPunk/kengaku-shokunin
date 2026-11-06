#!/usr/bin/env python3
"""MutC2: forge commits in a private fixture repo, run the frozen census CLI against them."""
import json, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r97/MutC2")
CLONE = ROOT / "clone"
FX = ROOT / "fx"
REPO = FX / "repo"
CENSUS = CLONE / "plans/round97_gate_selftest_census.py"
BASE = "4992cd0e32b8db23ca20310deb7de12d485f8bcc"
T = "f1083da60e7ff6b88f7420aae7424f7762d14700"
EXPECTED = """REV {rev} BASE {base}
ROWS base=168 rev=171 removed=0 duplicate=0 cells_changed=0
GATES total=84 with_selftest=84 without=0 demoted_with_selftest=0 scripts_changed=0
MISMATCH_TOTAL n=0
PREDICATE R97-C2 pass"""

def sh(*a, **kw):
    return subprocess.run(a, capture_output=True, text=True, **kw)

def git(*a):
    p = sh("git", "-C", str(REPO), *a)
    if p.returncode != 0:
        raise SystemExit(f"git {a} failed: {p.stderr[-400:]}")
    return p.stdout.strip()

def assert_toplevel():
    top = git("rev-parse", "--show-toplevel")
    if Path(top).resolve() != REPO.resolve():
        raise SystemExit(f"BAD TOPLEVEL {top} != {REPO}")

def extract(rev, dest):
    dest.mkdir(parents=True, exist_ok=True)
    p = sh("bash", "-c", f"git -C {CLONE} archive {rev} -- SKILL.md plans grader.py corpus/evidence/round13-coverage | tar -x -C {dest}")
    if p.returncode != 0:
        raise SystemExit(f"archive {rev} failed: {p.stderr[-300:]}")

def copy_tree(src, dst):
    for p in src.rglob("*"):
        if p.is_file():
            q = dst / p.relative_to(src)
            q.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, q)

def rows_of(skill_text):
    lines = skill_text.split("\n")
    st = [i for i, l in enumerate(lines) if l.startswith("## Gate/probe registry")]
    assert len(st) == 1, st
    out = []
    for i in range(st[0] + 1, len(lines)):
        if lines[i].startswith("## "):
            break
        if lines[i].startswith("| `"):
            out.append(i)
    return lines, out

def cell_split(line):
    return [c.strip() for c in re.compile(r"(?<!\\)\|").split(line.strip())[1:-1]]

def set_kind(lines, idx, kind):
    cells = cell_split(lines[idx])
    cells[1] = kind
    lines[idx] = "| " + " | ".join(cells) + " |"

def set_entry(lines, idx, entry):
    cells = cell_split(lines[idx])
    cells[2] = entry
    lines[idx] = "| " + " | ".join(cells) + " |"

def find_row(lines, idxs, name):
    for i in idxs:
        if cell_split(lines[i])[0] == name:
            return i
    raise SystemExit(f"row {name} not found")

def build_base():
    if REPO.exists():
        shutil.rmtree(REPO)
    REPO.mkdir(parents=True)
    assert sh("git", "-C", str(REPO), "init", "-q").returncode == 0
    assert_toplevel()
    base_tree = FX / "base"
    if base_tree.exists():
        shutil.rmtree(base_tree)
    extract(BASE, base_tree)
    copy_tree(base_tree, REPO)
    git("add", "-A")
    git("-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
        "commit", "-q", "--no-gpg-sign", "-m", "base")
    return git("rev-parse", "HEAD")

def build_mutant(base_sha, name, mutate):
    git("checkout", "-q", "--detach", base_sha)
    git("checkout", "-q", base_sha, "--", ".")
    rev_tree = FX / "rev"
    if rev_tree.exists():
        shutil.rmtree(rev_tree)
    extract(T, rev_tree)
    copy_tree(rev_tree, REPO)
    mutate(REPO)
    git("add", "-A")
    git("-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
        "commit", "-q", "--no-gpg-sign", "-m", name)
    return git("rev-parse", "HEAD")

def run_census(rev, base):
    env = dict(os.environ, TMPDIR=str(ROOT / "tmp"))
    p = subprocess.run([sys.executable, "-I", "-B", str(CENSUS), "--lane", str(REPO),
                        "--rev", rev, "--base", base], capture_output=True, text=True, env=env, timeout=600)
    return p.returncode, p.stdout

def main():
    base_sha = build_base()
    print(f"FIXTURE BASE {base_sha}")
    results = []

    def record(name, desc, mutate):
        rev = build_mutant(base_sha, name, mutate)
        rc, out = run_census(rev, base_sha)
        exp = EXPECTED.format(rev=rev, base=base_sha)
        findings = [l for l in out.splitlines() if l.split() and l.split()[0] in
                    ("ROW-REMOVED", "ROW-DUPLICATE", "CELL-CHANGED", "DEMOTED", "SCRIPT-CHANGED", "MISMATCH")]
        exact = out.strip() == exp.strip()
        results.append(dict(name=name, desc=desc, rev=rev, rc=rc, exact_block=exact,
                            findings=findings, out=out))
        print(f"\n=== {name} rc={rc} exact={exact} findings={len(findings)}")
        print(out.strip())
        print("--- findings:", findings[:6], "..." if len(findings) > 6 else "")

    # ---------------- controls (must fail)
    def ctl_row_removed(r):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        i = find_row(lines, idxs, "`round37-c2`")
        del lines[i]
        p.write_text("\n".join(lines))
    record("ctl-row-removed", "delete the `round37-c2` row", ctl_row_removed)

    def ctl_blanket(r):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        for i in idxs:
            if cell_split(lines[i])[1] == "gate":
                set_kind(lines, i, "probe")
        p.write_text("\n".join(lines))
    record("ctl-blanket", "every gate row retyped probe", ctl_blanket)

    def ctl_duplicate(r):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        i = find_row(lines, idxs, "`round37-c2`")
        lines.insert(i + 1, lines[i])
        p.write_text("\n".join(lines))
    record("ctl-duplicate", "duplicate the `round37-c2` row", ctl_duplicate)

    def ctl_script_changed(r):
        f = r / "plans/round37_c2_verify.py"
        f.write_text(f.read_text() + '\nif "--selftest" in sys.argv:\n    pass\n')
    record("ctl-script-changed", "append a --selftest dispatch to closed plans/round37_c2_verify.py", ctl_script_changed)

    def ctl_cell_changed(r):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        i = find_row(lines, idxs, "`round37-c2`")
        cells = cell_split(lines[i]); cells[4] = "`--selftest`"
        lines[i] = "| " + " | ".join(cells) + " |"
        p.write_text("\n".join(lines))
    record("ctl-cell-changed", "rewrite the self-test cell of `round37-c2`", ctl_cell_changed)

    def ctl_prose_only(r):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        (r / "plans/plain_probe.py").write_text('import sys\nsys.exit(0)\n')
        new = ("| `plain-probe` | gate | `python3 plans/plain_probe.py` | `0` clean · `1` failed | "
               "none | pins | read-only | kengaku |")
        lines.insert(idxs[-1] + 1, new)
        p.write_text("\n".join(lines))
    record("ctl-prose-only", "new gate row whose script has no spelling at all", ctl_prose_only)

    # ---------------- survivors
    def mut_45th_kind(r):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        set_kind(lines, find_row(lines, idxs, "`grader-perturb`"), "gate")
        set_kind(lines, find_row(lines, idxs, "`round97-gate-selftest-census`"), "probe")
        p.write_text("\n".join(lines))
    record("mut-45th-kind", "promote probe `grader-perturb` to gate, demote the round-97 gate row to probe", mut_45th_kind)

    def mut_gate_to_Gate(r):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        set_kind(lines, find_row(lines, idxs, "`gate-timing`"), "Gate")
        set_kind(lines, find_row(lines, idxs, "`grader-perturb`"), "gate")
        p.write_text("\n".join(lines))
    record("mut-gate-to-Gate", "retype gate-with-selftest `gate-timing` to `Gate` (non-probe demotion evasion)", mut_gate_to_Gate)

    def mut_strip_selftest(r):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        set_kind(lines, find_row(lines, idxs, "`gate-timing`"), "probe")
        set_kind(lines, find_row(lines, idxs, "`grader-perturb`"), "gate")
        p.write_text("\n".join(lines))
        f = r / "plans/gate_timing_check.py"
        t = f.read_text()
        t = re.sub(r"add_argument\(\s*[\"']--self-?test[\"'][^)]*\)", "add_argument('--unused')", t)
        t = t.replace("--selftest", "--unused").replace("run_selftest", "run_selfcheck")
        f.write_text(t)
    record("mut-strip-selftest", "demote `gate-timing` to probe AND strip its self-test spelling", mut_strip_selftest)

    def promote_with(r, row, snippet, script):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        set_kind(lines, find_row(lines, idxs, row), "gate")
        set_kind(lines, find_row(lines, idxs, "`round97-gate-selftest-census`"), "probe")
        p.write_text("\n".join(lines))
        f = r / script
        f.write_text(f.read_text() + snippet)
    record("mut-launder-comment", "promote a no-selftest probe to gate, launder its script with a comment",
           lambda r: promote_with(r, "`round97-sparql-probe`", '\n# if "--selftest" in sys.argv: pass\n',
                                  "plans/round97_sparql_probe.py"))
    record("mut-dead-def", "promote a no-selftest probe to gate, append a never-called def run_selftest",
           lambda r: promote_with(r, "`round97-sparql-probe`", '\ndef run_selftest():\n    pass\n',
                                  "plans/round97_sparql_probe.py"))
    record("mut-add-arg-no-handler", "promote a no-selftest probe to gate, append an unread add_argument",
           lambda r: promote_with(r, "`round97-sparql-probe`",
                                  '\nimport argparse as _a\n_a.ArgumentParser().add_argument("--selftest", action="store_true")\n',
                                  "plans/round97_sparql_probe.py"))
    record("mut-dead-compare", "promote a no-selftest probe to gate, append a dead constant `in` comparison",
           lambda r: promote_with(r, "`round97-sparql-probe`", '\n_UNUSED = "--selftest" in "never"\n',
                                  "plans/round97_sparql_probe.py"))
    record("mut-reversed-dispatch", "promote a no-selftest probe to gate and give it a REAL dispatch written reversed",
           lambda r: promote_with(r, "`round97-sparql-probe`",
                                  '\nimport sys as _s\nif _s.argv[1:2] == ["--selftest"]:\n    raise SystemExit(0)\n',
                                  "plans/round97_sparql_probe.py"))

    def mut_hidden_row(r):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        new = ("| hidden-gate | gate | `python3 plans/round37_c2_verify.py` | `0` clean · `1` failed | "
               "none | pins | read-only | kengaku |")
        lines.insert(idxs[-1] + 1, new)
        p.write_text("\n".join(lines))
    record("mut-hidden-row", "add a gate row with no backticked name (unparsed by the census)", mut_hidden_row)

    def mut_decoy_entry(r):
        p = r / "SKILL.md"; lines, idxs = rows_of(p.read_text())
        i = find_row(lines, idxs, "`round97-sparql-probe`")
        set_kind(lines, i, "gate")
        set_entry(lines, i, "`python3 plans/round97_gate_selftest_census.py --lane . --work DIR --grader-venv G`")
        set_kind(lines, find_row(lines, idxs, "`round97-gate-selftest-census`"), "probe")
        p.write_text("\n".join(lines))
    record("mut-decoy-entry", "retype the sparql probe row gate and point its entry cell at the census script", mut_decoy_entry)

    def mut_heading_dup(r):
        p = r / "SKILL.md"; t = p.read_text()
        p.write_text(t.replace("## Gate/probe registry", "## Gate/probe registry\n\n## Gate/probe registry", 1))
    record("mut-heading-dup", "duplicate the registry heading", mut_heading_dup)

    (ROOT / "ev" / "mutants.json").write_text(json.dumps(results, indent=1))
    (ROOT / "ev" / "out").mkdir(exist_ok=True)
    (ROOT / "ev" / "diffs").mkdir(exist_ok=True)
    for r in results:
        (ROOT / "ev" / "out" / (r["name"] + ".txt")).write_text(r["out"])
        d = subprocess.run(["git", "-C", str(REPO), "diff", base_sha, r["rev"], "--", "SKILL.md", "plans"],
                           capture_output=True, text=True).stdout
        (ROOT / "ev" / "diffs" / (r["name"] + ".diff")).write_text(d)
        r["diff_bytes"] = len(d)
    print("\nSUMMARY")
    for r in results:
        print(f"{r['name']:24s} rc={r['rc']} exact_block={r['exact_block']} findings={len(r['findings'])}")

if __name__ == "__main__":
    main()
