#!/usr/bin/env python3
"""MutC2: selftest mutants — mutate the frozen census script, run its own --selftest."""
import json, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r97/MutC2")
SRC = ROOT / "clone/plans/round97_gate_selftest_census.py"
WORK = ROOT / "work/stmut"
OUT = ROOT / "ev"

MUTANTS = {
 # case deletion: the selftest never pins its own case count
 "st-drop-case-duplicate": ("remove the `duplicate` case", lambda t: t.replace(
     '''            ("duplicate", base_skill.replace("| `b` | gate |", "| `b` | probe |") + row("a", "gate", "plans/a.py", "`--selftest`"),
             base_scripts, 1, {"ROW-DUPLICATE"}),
''', '')),
 "st-drop-case-script-forged": ("remove the `script-forged` case", lambda t: t.replace(
     '''            ("script-forged", base_skill, {**base_scripts, "plans/b.py": WITHOUT + 'if "--selftest" in sys.argv:\\n    pass\\n'},
             1, {"SCRIPT-CHANGED"}),
''', '')),
 # pattern deletions: which SPELLING regexes are actually exercised?
 "st-drop-add_argument": ("drop add_argument pattern", lambda t: drop_pattern(t, 0)),
 "st-drop-add_parser": ("drop add_parser pattern", lambda t: drop_pattern(t, 1)),
 "st-drop-quoted-selftest-in": ("drop quoted `--selftest` + in/== pattern", lambda t: drop_pattern(t, 2)),
 "st-drop-in-quoted-selftest": ("drop `in/==` + quoted `--selftest` pattern", lambda t: drop_pattern(t, 3)),
 "st-drop-def-run_selftest": ("drop `def run_selftest` pattern", lambda t: drop_pattern(t, 4)),
 "st-drop-in-quoted-plain": ("drop `in/==` + quoted `selftest` pattern", lambda t: drop_pattern(t, 5)),
 # broaden the detector: add a bare quoted-string match (no negative control for prose)
 "st-broaden-quoted-string": ("add a bare `\"--selftest\"` pattern", lambda t: t.replace(
     '    r"def run_selftest\\b",\n', '    r"def run_selftest\\b",\n    r\'"--selftest"\',\n')),
 # output-contract mutations: the frozen predicate quotes these lines, the selftest does not assert them
 "st-counts-zero": ("zero the ROWS count line", lambda t: t.replace(
     'lines.append(f"ROWS base={len(at_base)} rev={len(at_rev)} removed=', 'lines.append(f"ROWS base=0 rev=0 removed=')),
 "st-gates-zero": ("zero the GATES count line", lambda t: t.replace(
     'lines.append(f"GATES total={gates} with_selftest={with_st} without=', 'lines.append(f"GATES total=0 with_selftest=0 without=')),
 "st-predicate-lie": ("print `PREDICATE R97-C2 pass` unconditionally", lambda t: t.replace(
     'print("PREDICATE R97-C2 " + ("pass" if ok else "fail"))', 'print("PREDICATE R97-C2 pass")')),
 # assertion weakening
 "st-ids-subset": ("assert want_ids subset of ids instead of equality", lambda t: t.replace(
     "ok = rc == want_rc and ids == want_ids", "ok = rc == want_rc and want_ids <= ids")),
 "st-no-ids": ("assert rc only", lambda t: t.replace(
     "ok = rc == want_rc and ids == want_ids", "ok = rc == want_rc")),
 # detector narrowing the selftest does not cover
 "st-demoted-unchanged-only": ("DEMOTED only when the script is unchanged", lambda t: t.replace(
     'if brow[1] == "gate" and len(rrow) > 1 and rrow[1] == "probe" and has_selftest(rbody):',
     'if brow[1] == "gate" and len(rrow) > 1 and rrow[1] == "probe" and has_selftest(rbody) and rbody == bbody:')),
 "st-scriptchanged-gate-only": ("SCRIPT-CHANGED only while the row stays gate", lambda t: t.replace(
     'if brow[1] == "gate" and not has_selftest(bbody) and rbody != bbody:',
     'if brow[1] == "gate" and rrow[1] == "gate" and not has_selftest(bbody) and rbody != bbody:')),
 "st-rowfilter-broad": ("parse every `|` line, not only `| \\``", lambda t: t.replace(
     'if line.startswith("| `"):', 'if line.startswith("|"):')),
 "st-script-last-match": ("use the last .py token in the entry cell", lambda t: t.replace(
     'm = SCRIPT.search(row[2]) if len(row) > 2 else None\n    return m.group(1) if m else None',
     'ms = SCRIPT.findall(row[2]) if len(row) > 2 else []\n    return ms[-1] if ms else None')),
}


def drop_pattern(src: str, idx: int) -> str:
    lines = src.splitlines(True)
    start = next(i for i, l in enumerate(lines) if l.startswith("SPELLING = [re.compile"))
    end = next(i for i in range(start, len(lines)) if lines[i].rstrip() == ")]")
    keep = [i for i in range(start + 1, end) if lines[i].strip()]
    del lines[keep[idx]]
    return "".join(lines)

def run(name, desc, fn):
    WORK.mkdir(parents=True, exist_ok=True)
    d = WORK / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir()
    src = SRC.read_text()
    mut = fn(src)
    changed = mut != src
    f = d / "census.py"
    f.write_text(mut)
    env = dict(os.environ, TMPDIR=str(ROOT / "tmp"))
    p = subprocess.run([sys.executable, "-I", "-B", str(f), "--selftest", "--work", str(d / "w")],
                       capture_output=True, text=True, env=env, timeout=900)
    tail = [l for l in p.stdout.splitlines() if l.startswith(("SELFTEST", "CASE"))]
    failed_lines = [l for l in tail if l.startswith("CASE") and "ok=False" in l]
    print(f"\n=== {name} changed={changed} rc={p.returncode}")
    print(f"    {desc}")
    print(f"    {tail[-1] if tail else '(no SELFTEST line)'}  failing={len(failed_lines)}")
    for l in failed_lines[:4]:
        print("    " + l)
    if p.stderr.strip():
        print("    STDERR " + p.stderr.strip().splitlines()[-1][:200])
    return dict(name=name, desc=desc, changed=changed, rc=p.returncode,
                summary=tail[-1] if tail else None, failing=failed_lines,
                stdout=p.stdout, stderr=p.stderr)

def main():
    OUT.mkdir(exist_ok=True)
    res = [run(n, d, f) for n, (d, f) in MUTANTS.items()]
    (OUT / "selftest_mutants.json").write_text(json.dumps(res, indent=1))
    print("\nSUMMARY (survivor = rc 0 / failed=0)")
    for r in res:
        print(f"{r['name']:32s} changed={r['changed']!s:5s} rc={r['rc']} {r['summary']}")

if __name__ == "__main__":
    main()
