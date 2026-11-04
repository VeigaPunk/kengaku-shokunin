#!/usr/bin/env python3
"""GateMutate70 probe: hostile mutants the R70-C2 `--mutants` matrix cannot generate.

Read-only against the lane.  Writes only under --scratch.  Five hostile gate sources are
derived from the lane's committed gate by asserted single-hit text substitutions:

  h1  a check that always returns True                    (E3 vacuous, entry retained)
  h2  two CHECKS entries deleted                          (E5 and E8)
  h3  a check whose defect is printed but not counted     (E5 prints, counter skips)
  h4b two entries deleted and re-added as distinct-text aliases of E7's check
  h5  a check that short-circuits on artifact existence   (E7 presence-as-proof)
  h6  h2 plus both control constants derived from len(CHECKS) (no absolute cardinality)

For each hostile gate both shipped control arms are run from the shadow lane (LANE must
resolve to a root holding the ten fixture inputs).  Then a four-lane matrix runs the honest
and hostile gates on a synthetic green lane and on single-defect lanes, so each hostile
mutant is shown against the one frozen defect it hides.

Usage: repro_hostile_mutants.py --lane <L> --scratch <dir>
"""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys

INPUTS = [
    "SKILL.md",
    "corpus/README.md",
    "corpus/SOURCES.md",
    "corpus/QUALITY.md",
    "corpus/knowledge/tb2-nginx-request-logging-offline.md",
    "plans/round63_gate_checks.py",
    "corpus/evidence/round62/class-survey.txt",
    "corpus/evidence/round69/gates/depth-gate.txt",
    ".ufo/waves/round-69/w1/gates/depth-gate.txt",
    "plans/round70_c2_routed_defects.py",
]
EVIDENCE = [
    "corpus/evidence/round70/c2/depth-gate-provenance.txt",
    "corpus/evidence/round70/gates/trio-nginx.txt",
    "corpus/evidence/round70/gates/r69-c2-landing.txt",
]
LESSON_REJECT = (
    "# Round 70 lesson (probe fixture)\n\n## Gate\n\n"
    "- admit: `corpus/knowledge/tb2-nginx-request-logging-offline.md` - reason: re-derives\n"
    "- reject: `merge/kengaku` - reason: its tier-A own-work claim rests on a probe "
    "transcript absent from this lane\n"
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sub1(text, old, new, label):
    if text.count(old) != 1:
        raise SystemExit(f"MUTATION {label} hits={text.count(old)} want=1")
    return text.replace(old, new)


def run(argv, cwd):
    r = subprocess.run(argv, capture_output=True, text=True, cwd=str(cwd))
    return r.returncode, r.stdout, r.stderr


def count_and_predicate(out):
    n = re.search(r"DEFECTS n=(\d+)", out)
    p = re.search(r"PREDICATE R70-C2 (\w+)", out)
    return (n.group(1) if n else "?"), (p.group(1) if p else "?")


def elines(out):
    cells = []
    for ln in out.splitlines():
        m = re.match(r"E(\d+) (ok|defect) (\S+)", ln)
        if m:
            cells.append(f"E{m.group(1)}/{'P' if m.group(2) == 'ok' else 'F'} {m.group(3)}")
    return " ".join(cells)


def snapshot(lane, shadow):
    if shadow.exists():
        shutil.rmtree(shadow)
    pins = {}
    for rel in INPUTS:
        data = (lane / rel).read_bytes()
        dst = shadow / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        pins[rel] = sha(data)
        if sha((lane / rel).read_bytes()) != pins[rel]:
            raise SystemExit(f"RACE {rel} changed during snapshot")
    return pins


def hostile_sources(base):
    h1 = sub1(
        base,
        "def check_instruction_row(root):\n    entry = root / NGINX_ENTRY",
        'def check_instruction_row(root):\n    return True, "problems=[]"\n'
        "    entry = root / NGINX_ENTRY",
        "h1",
    )
    h2 = sub1(base, '    (5, "corpus-index", check_corpus_index),\n', "", "h2-e5")
    h2 = sub1(h2, '    (8, "wave-validation", check_wave_validation),\n', "", "h2-e8")
    h3 = sub1(
        base,
        "        print(f\"E{n} {'ok' if ok else 'defect'} {name} {detail}\")\n"
        "        if not ok:\n            defects += 1",
        "        counted = True if n == 5 else ok\n"
        "        print(f\"E{n} {'ok' if ok else 'defect'} {name} {detail}\")\n"
        "        if not counted:\n            defects += 1",
        "h3",
    )
    h4b = sub1(
        h2,
        '    (7, "gate-reject", check_gate_reject),\n)',
        '    (7, "gate-reject", check_gate_reject),\n'
        '    (5, "corpus-index-v2", check_gate_reject),\n'
        '    (8, "wave-validation-v2", check_gate_reject),\n)',
        "h4b",
    )
    h5 = sub1(
        base,
        "def check_gate_reject(root):\n    problems = []",
        "def check_gate_reject(root):\n    if (root / LESSON70).is_file():\n"
        '        return True, "problems=[]"\n    problems = []',
        "h5",
    )
    h6 = sub1(
        h2,
        "    ok = failed == 8 and rc == 1",
        "    ok = failed == len(CHECKS) and rc == 1",
        "h6-selftest-count",
    )
    h6 = sub1(
        h6,
        'print(f"SELFTEST defects-in-fake={failed} want=8 all-fail={ok}")',
        'print(f"SELFTEST defects-in-fake={failed} want={len(CHECKS)} all-fail={ok}")',
        "h6-selftest-want",
    )
    h6 = sub1(
        h6,
        "dead = got == 7 and run.returncode == 1",
        "dead = got == len(CHECKS) - 1 and run.returncode == 1",
        "h6-mutants-expected",
    )
    if len(re.findall(r'^    \(\d+, "', h2, re.M)) != 6:
        raise SystemExit("h2 entry count != 6")
    if len(re.findall(r'^    \(\d+, "', h4b, re.M)) != 8:
        raise SystemExit("h4b entry count != 8")
    return {
        "h1_always_true": h1,
        "h2_delete_two": h2,
        "h3_printed_uncounted": h3,
        "h4b_delete_two_aliased": h4b,
        "h5_existence_shortcircuit": h5,
        "h6_control_constants_derived": h6,
    }


def build_lane(shadow, dest, evidence, mutate=()):
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(shadow, dest, ignore=shutil.ignore_patterns("h*.py"))
    for rel in evidence:
        dst = dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(evidence[rel])
    (dest / "corpus/lessons").mkdir(parents=True, exist_ok=True)
    (dest / "corpus/lessons/round-70.md").write_text(LESSON_REJECT)
    wave = dest / ".ufo/waves/round-70"
    wave.mkdir(parents=True, exist_ok=True)
    (wave / "w1-validate.rc").write_text("0\n")
    (wave / "w1-validate.out").write_text("w1 validate ok\n")
    (wave / "w1-validate.stderr").write_text("")
    for fn in mutate:
        fn(dest)
    return dest


def break_entry(d):
    p = d / "corpus/knowledge/tb2-nginx-request-logging-offline.md"
    t = p.read_text()
    new = t.replace("instruction.md:6-11,15-18", "instruction.md:1-20").replace("S242", "S241")
    if new == t or "S242" in new or "instruction.md:6-11,15-18" in new:
        raise SystemExit("break_entry did not bite")
    p.write_text(new)


def break_readme(d):
    p = d / "corpus/README.md"
    t = p.read_text()
    new = "\n".join(ln for ln in t.splitlines() if "lessons/round-69.md" not in ln)
    new = new.replace("## Round-69 supporting artifacts", "## Round-69 artifacts")
    if new == t or "lessons/round-69.md" in new or "Round-69 supporting artifacts" in new:
        raise SystemExit("break_readme did not bite")
    p.write_text(new + "\n")


def break_lesson(d):
    p = d / "corpus/lessons/round-70.md"
    t = p.read_text()
    new = "\n".join(ln for ln in t.splitlines() if "reject:" not in ln) + "\n"
    if new == t:
        raise SystemExit("break_lesson did not bite")
    p.write_text(new)


def drop_receipts(d):
    target = d / ".ufo/waves/round-70"
    if not target.is_dir():
        raise SystemExit("drop_receipts: no receipts to drop")
    shutil.rmtree(target)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", required=True)
    ap.add_argument("--scratch", required=True)
    args = ap.parse_args()
    lane = pathlib.Path(args.lane).resolve()
    scratch = pathlib.Path(args.scratch).resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    shadow = scratch / "shadow"

    pins = snapshot(lane, shadow)
    print("== snapshot (sha256 of every shadow input) ==")
    for rel, h in pins.items():
        print(f"   {h}  {rel}")

    base = (shadow / "plans/round70_c2_routed_defects.py").read_text()
    sources = hostile_sources(base)
    print("\n== hostile sources (asserted single-hit substitutions) ==")
    for name, text in sources.items():
        path = shadow / "plans" / f"{name}.py"
        path.write_text(text)
        r = subprocess.run([sys.executable, "-c", "import ast,sys;ast.parse(open(sys.argv[1]).read())",
                            str(path)], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"{name}: {r.stderr}")
        print(f"   {name:28} bytes={len(text):5} sha256={sha(text.encode())[:16]} parses=ok")

    honest = shadow / "plans/round70_c2_routed_defects.py"
    print("\n== shipped control arms applied to each hostile gate ==")
    print(f"   {'gate':28} {'arm':9} {'rc':>3}  tally")
    arm_rows = {}
    for name, text in sources.items():
        gate = shadow / "plans" / f"{name}.py"
        for arm, flag in (("selftest", "--selftest"), ("mutants", "--mutants")):
            work = scratch / "arms" / name / arm / "work"
            work.mkdir(parents=True, exist_ok=True)
            rc, out, err = run([sys.executable, str(gate), flag, "--work", str(work)], shadow)
            (work.parent / "stdout.txt").write_text(out)
            (work.parent / "stderr.txt").write_text(err)
            (work.parent / "rc.txt").write_text(str(rc) + "\n")
            if arm == "selftest":
                tally = " | ".join(re.findall(r"^SELFTEST .*$", out, re.M))
                first = re.findall(r"^DEFECTS n=(\d+)", out, re.M)
                arm_rows[(name, arm)] = {"rc": rc, "fake_defects": first[0] if first else None,
                                         "selftest": tally}
            else:
                tally = (re.search(r"^MUTANTS total=\d+ killed=\d+", out, re.M) or [None])[0] or "NO-TALLY"
                per = re.findall(r"^MUTANT (\d+) (\S+) defects=(-?\d+) killed=(\w+)", out, re.M)
                arm_rows[(name, arm)] = {"rc": rc, "mutants": tally,
                                         "per": [f"{a}:{c}{'K' if d == 'True' else 's'}" for a, b, c, d in per]}
                tally += "   per=" + " ".join(f"{a}:{c}{'K' if d == 'True' else 's'}"
                                             for a, b, c, d in per)
            print(f"   {name:28} {arm:9} {rc:>3}  {tally}")
    (scratch / "arm-rows.json").write_text(json.dumps({f"{k[0]}|{k[1]}": v for k, v in arm_rows.items()},
                                                      indent=1) + "\n")

    evidence = {rel: (lane / rel).read_bytes() for rel in EVIDENCE}
    lanes = {
        "BASE_green": build_lane(shadow, scratch / "lanes/BASE_green", evidence),
        "L_E3": build_lane(shadow, scratch / "lanes/L_E3", evidence, (break_entry,)),
        "L_E5": build_lane(shadow, scratch / "lanes/L_E5", evidence, (break_readme,)),
        "L_E7": build_lane(shadow, scratch / "lanes/L_E7", evidence, (break_lesson,)),
        "L_E5E8": build_lane(shadow, scratch / "lanes/L_E5E8", evidence, (break_readme, drop_receipts)),
    }
    hidden_by = {
        "h1_always_true": "L_E3",
        "h2_delete_two": "L_E5E8",
        "h3_printed_uncounted": "L_E5",
        "h4b_delete_two_aliased": "L_E5E8",
        "h5_existence_shortcircuit": "L_E7",
        "h6_control_constants_derived": "L_E5E8",
    }
    print("\n== lane matrix: honest gate vs hostile gate on the lane holding its hidden defect ==")
    for lane_name, root in lanes.items():
        order = ["<honest>"] + list(sources) if lane_name in hidden_by.values() else ["<honest>"]
        for gate_name in order:
            gate = honest if gate_name == "<honest>" else shadow / "plans" / f"{gate_name}.py"
            rc, out, err = run([sys.executable, str(gate), "--root", str(root)], scratch)
            n, pred = count_and_predicate(out)
            print(f"   {lane_name:10} {gate_name:28} rc={rc}  DEFECTS n={n} {pred}")
            print(f"      {elines(out)}")
            if hidden_by.get(gate_name) == lane_name:
                (scratch / f"hide-{lane_name}-{gate_name}.txt").write_text(
                    f"# {gate_name} --root {root}\n# rc={rc}\n" + out + err)
    print("\n== reading ==")
    print("   H1/H2/H3 are caught by --mutants arithmetic (killed<total); H3's printed line")
    print("   count fools --selftest.  H4b and H5 keep DEFECTS n=8, 8 defect lines, and")
    print("   killed=8/8 while hiding real frozen defects on the lanes named above.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
