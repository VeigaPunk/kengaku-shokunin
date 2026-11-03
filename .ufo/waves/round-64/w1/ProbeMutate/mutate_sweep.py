#!/usr/bin/env python3
"""Mutation battery m5..m6 against the R64-C3 trio sweep (--sweep / --selftest).

Fixture lanes are built under S/fixtures; each detector run records cwd, command,
rc, stdout, stderr into a receipt under W/receipts.
Writes only under S (scratch) and W (this seat's dir).
"""

import difflib
import hashlib
import pathlib
import shutil
import subprocess
import sys
import time

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r64/ProbeMutate")
W = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/ProbeMutate")
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SWEEP_BUILD = LANE / ".ufo/waves/round-64/w1/SweepBuild"
SWEEP_SRC = SWEEP_BUILD / "round64_trio_sweep.py"
GATE_SRC = LANE / "plans/round63_gate_checks.py"
PRISTINE = S / "pristine/round64_trio_sweep.py"
FIX = S / "fixtures/sweep"
WORK = S / "work/sweep"
RECEIPTS = W / "receipts"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd, cwd, timeout=300):
    started = time.time()
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                          timeout=timeout)
    return {"cmd": cmd, "cwd": str(cwd), "rc": proc.returncode,
            "stdout": proc.stdout, "stderr": proc.stderr,
            "elapsed": round(time.time() - started, 2)}


def block(title, res, expect=None):
    return "\n".join([
        f"## {title}",
        f"cmd={' '.join(str(c) for c in res['cmd'])}",
        f"cwd={res['cwd']}",
        f"rc={res['rc']}" + (f" expect={expect}" if expect is not None else ""),
        f"elapsed={res['elapsed']}s",
        "--- stdout ---", res["stdout"].rstrip() or "(empty)",
        "--- stderr ---", res["stderr"].rstrip() or "(empty)",
    ])


def apply_mutation(src, dst, transform, diff_path):
    original = src.read_text(encoding="utf-8")
    text = transform(original)
    if text == original:
        raise SystemExit("SPEC ERROR no-byte-change")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    compile(text, str(dst), "exec")
    diff = "".join(difflib.unified_diff(
        original.splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=str(src), tofile=str(dst), n=2))
    diff_path.write_text(diff or "(empty)\n", encoding="utf-8")
    return diff


WRONG_DATE = """# wrong-date-fixture - opening predates the trio rule; addendum carries the wrong round

**Provenance of this note (read first).** Fixture body with no trio key in the
frozen window.

## Body

Fixture body; still no trio key.

## Freshness addendum (round 63)

verified-at: 2026-11-03
recheck: python3 plans/round63_gate_checks.py trio corpus/knowledge/wrong-date.md
"""

RIGHT_DATE = WRONG_DATE.replace("(round 63)", "(round 64)")

OPEN_FILE = """# open-fixture - provenance trio in the frozen window

source: S-fixture - a committed receipt `corpus/evidence/fixture.txt`
verified-at: 2026-11-03
recheck: python3 plans/round63_gate_checks.py trio corpus/knowledge/open.md

## Body

Fixture body.
"""

RED_OTHER = """# red-other - no trio, no addendum

Fixture body with neither an opening trio nor a freshness addendum.

## Body
"""


def build_lane(root, files, frozen_entries):
    knowledge = root / "corpus/knowledge"
    knowledge.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (knowledge / name).write_text(text, encoding="utf-8")
    frozen = root / "frozen.txt"
    frozen.write_text("\n".join(frozen_entries) + "\n", encoding="utf-8")
    return root, frozen


def main():
    for d in (FIX, WORK, RECEIPTS):
        d.mkdir(parents=True, exist_ok=True)
    for stale in (FIX, WORK):
        for child in stale.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    head = [
        "# m5..m6 mutation battery — R64-C3 trio sweep",
        f"ts={time.strftime('%Y-%m-%dT%H:%M:%S')}",
        f"pristine={PRISTINE}",
        f"pristine_sha256={sha256(PRISTINE)}",
        f"sweep_source={SWEEP_SRC}",
        f"sweep_source_sha256_at_battery={sha256(SWEEP_SRC)}",
        f"gate_dependency={GATE_SRC}",
        f"gate_dependency_sha256_at_battery={sha256(GATE_SRC)}",
    ]

    # the sweep imports round63_gate_checks from its own directory
    shutil.copyfile(GATE_SRC, PRISTINE.parent / "round63_gate_checks.py")

    # fixtures ------------------------------------------------------------
    lane_m5, frozen_m5 = build_lane(
        FIX / "lane-m5", {"wrong-date.md": WRONG_DATE},
        ["corpus/knowledge/wrong-date.md"])
    lane_m5c, frozen_m5c = build_lane(
        FIX / "lane-m5-control", {"right-date.md": RIGHT_DATE},
        ["corpus/knowledge/right-date.md"])
    lane_m6, frozen_m6 = build_lane(
        FIX / "lane-m6-vacuous", {"open.md": OPEN_FILE},
        ["corpus/knowledge/gone1.md", "corpus/knowledge/gone2.md",
         "corpus/knowledge/gone3.md"])
    lane_m6b, frozen_m6b = build_lane(
        FIX / "lane-m6-mismatch", {"red-other.md": RED_OTHER},
        ["corpus/knowledge/some-other.md"])
    head += [f"fixture_lane_m5={lane_m5}", f"fixture_lane_m5_control={lane_m5c}",
             f"fixture_lane_m6={lane_m6}", f"fixture_lane_m6_mismatch={lane_m6b}"]

    # mutation transforms ------------------------------------------------
    def mut_m5(text):
        old = ('    headings = [i for i, line in enumerate(lines) '
               'if line.rstrip() == ADDENDUM_HEADING]')
        new = ('    headings = [i for i, line in enumerate(lines) '
               'if line.rstrip() == ADDENDUM_HEADING\n'
               '                  or line.rstrip() == "## Freshness addendum (round 63)"]')
        assert text.count(old) == 1, f"m5 anchor matches={text.count(old)}"
        return text.replace(old, new, 1)

    def mut_m6(text):
        start_anchor = "    if red:\n        observed = sorted(red)"
        end_anchor = '            return 2, ["SETUP frozen-entry-missing"], err\n'
        i = text.find(start_anchor)
        j = text.find(end_anchor)
        assert i != -1 and j != -1 and j > i, "m6 anchors not found"
        j += len(end_anchor)
        return text[:i] + "    # mutant m6: the SETUP frozen-list cross-check is dropped\n" + text[j:]

    specs = {
        "m5": (mut_m5, "accept '## Freshness addendum (round 63)' (wrong date) as a valid addendum"),
        "m6": (mut_m6, "drop the SETUP frozen-list cross-check (mismatch + absent-entry guards)"),
    }

    summary = []
    for name in ("m5", "m6"):
        mdir = S / "mutants" / name
        mdir.mkdir(parents=True, exist_ok=True)
        mutant = mdir / "round64_trio_sweep.py"
        # the sweep imports round63_gate_checks from its own directory
        shutil.copyfile(PRISTINE, mutant)
        shutil.copyfile(GATE_SRC, mdir / "round63_gate_checks.py")
        # re-apply with the transform against the pristine text
        diff = apply_mutation(PRISTINE, mutant, specs[name][0],
                              RECEIPTS / f"{name}-diff.txt")
        shutil.copyfile(GATE_SRC, mdir / "round63_gate_checks.py")

        (WORK / f"st-pristine-{name}").mkdir(parents=True, exist_ok=True)
        (WORK / f"st-mutant-{name}").mkdir(parents=True, exist_ok=True)

        runset = []
        if name == "m5":
            runset = [
                ("pristine-wrongdate", [sys.executable, str(PRISTINE), "--sweep",
                                        "--lane", str(lane_m5), "--frozen-list", str(frozen_m5)], 1),
                ("pristine-control-rightdate", [sys.executable, str(PRISTINE), "--sweep",
                                                "--lane", str(lane_m5c), "--frozen-list", str(frozen_m5c)], 0),
                ("mutant-wrongdate", [sys.executable, str(mutant), "--sweep",
                                      "--lane", str(lane_m5), "--frozen-list", str(frozen_m5)], "0 => SURVIVED"),
                ("mutant-control-rightdate", [sys.executable, str(mutant), "--sweep",
                                              "--lane", str(lane_m5c), "--frozen-list", str(frozen_m5c)], 0),
            ]
        else:
            runset = [
                ("pristine-vacuous-lane", [sys.executable, str(PRISTINE), "--sweep",
                                           "--lane", str(lane_m6), "--frozen-list", str(frozen_m6)], 2),
                ("mutant-vacuous-lane", [sys.executable, str(mutant), "--sweep",
                                         "--lane", str(lane_m6), "--frozen-list", str(frozen_m6)], "0 => SURVIVED"),
                ("pristine-mismatch-lane", [sys.executable, str(PRISTINE), "--sweep",
                                            "--lane", str(lane_m6b), "--frozen-list", str(frozen_m6b)], 2),
                ("mutant-mismatch-lane", [sys.executable, str(mutant), "--sweep",
                                          "--lane", str(lane_m6b), "--frozen-list", str(frozen_m6b)], "1 => SURVIVED (graded)"),
            ]

        runs = []
        for label, cmd, expect in runset:
            runs.append((label, run(cmd, S), expect))
        st_pristine = run([sys.executable, str(PRISTINE), "--selftest", "--work", str(WORK / f"st-pristine-{name}")], S)
        st_mutant = run([sys.executable, str(mutant), "--selftest", "--work", str(WORK / f"st-mutant-{name}")], S)

        if name == "m5":
            primary = dict((label, res) for label, res, _e in runs)["mutant-wrongdate"]
            killed = primary["rc"] != 0
            mech = "--sweep" if killed else ""
        else:
            primary = dict((label, res) for label, res, _e in runs)["mutant-vacuous-lane"]
            killed = primary["rc"] != 0
            mech = "--sweep" if killed else ""
        if not killed and st_mutant["rc"] != 0:
            killed, mech = True, "--selftest"

        checks = [f"{label}_rc={res['rc']} expect={expect}" for label, res, expect in runs]
        checks.append(f"selftest_pristine_rc={st_pristine['rc']} (expect 0)")
        checks.append(f"selftest_mutant_rc={st_mutant['rc']} (0 => selftest blind)")

        text = "\n".join(head + [
            f"# mutation {name}",
            f"defect={specs[name][1]}",
            f"mutant={mutant}",
            f"mutant_sha256={sha256(mutant)}",
            "",
        ] + [block(f"{label} [{name}]", res, expect) + "\n" for label, res, expect in runs] + [
            block(f"selftest-pristine [{name}]", st_pristine, 0), "",
            block(f"selftest-mutant [{name}]", st_mutant, 0), "",
            "--- mutation diff ---", diff, "",
            "--- summary ---", *checks,
            f"VERDICT {name}={'KILLED' if killed else 'SURVIVED'} mechanism={mech or 'NONE'}",
            "",
        ])
        (RECEIPTS / f"{name}.txt").write_text(text, encoding="utf-8")
        summary.append((name, "KILLED" if killed else "SURVIVED", mech or "NONE", checks))

    print("\n".join(head))
    for name, verdict, mech, checks in summary:
        print(f"VERDICT {name}={verdict} mechanism={mech}")
        for c in checks:
            print(f"  {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
