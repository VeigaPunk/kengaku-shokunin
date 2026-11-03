#!/usr/bin/env python3
"""Mutation battery m1..m4 against the R64-C1 probe (--check-receipt / --selftest).

Runs the SAME bounded detector on pristine, mutated and restored bytes.
Every run captures cwd, command, rc, stdout, stderr into a receipt file.
Writes only under S (scratch) and W (this seat's dir).
"""

import importlib.util
import pathlib
import shutil
import subprocess
import sys
import time

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r64/ProbeMutate")
W = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/ProbeMutate")
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBEBUILD = LANE / ".ufo/waves/round-64/w1/ProbeBuild"
PRISTINE = S / "pristine/round64_c1_kvstore_probe.py"
FIX = S / "fixtures/probe"
WORK = S / "work/probe"
RECEIPTS = W / "receipts"
PROBE_SRC = PROBEBUILD / "round64_c1_kvstore_probe.py"
REAL = PROBEBUILD / "kvstore-probe.txt"


def sha256(path):
    import hashlib
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
    lines = [f"## {title}",
             f"cmd={' '.join(str(c) for c in res['cmd'])}",
             f"cwd={res['cwd']}",
             f"rc={res['rc']}" + (f" expect={expect}" if expect is not None else ""),
             f"elapsed={res['elapsed']}s",
             "--- stdout ---", res["stdout"].rstrip() or "(empty)",
             "--- stderr ---", res["stderr"].rstrip() or "(empty)"]
    return "\n".join(lines)


def apply_mutation(src, dst, steps, diff_path):
    """Exact-string replacement; assert each match count; assert bytes changed."""
    text = src.read_text(encoding="utf-8")
    original = text
    for i, (old, new, want) in enumerate(steps):
        got = text.count(old)
        if got != want:
            raise SystemExit(f"SPEC ERROR step={i} matches={got} want={want} old={old!r}")
        text = text.replace(old, new, want)
    if text == original:
        raise SystemExit("SPEC ERROR no-byte-change")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    compile(text, str(dst), "exec")
    import difflib
    diff = "".join(difflib.unified_diff(
        original.splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=str(src), tofile=str(dst), n=2))
    diff_path.write_text(diff or "(empty)\n", encoding="utf-8")
    return diff


def deep_import(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    for d in (FIX, WORK, RECEIPTS):
        d.mkdir(parents=True, exist_ok=True)
    for stale in (FIX, WORK):
        for child in stale.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    source_sha_snapshot = sha256(PRISTINE)
    head = [f"# m1..m4 mutation battery — R64-C1 probe",
            f"ts={time.strftime('%Y-%m-%dT%H:%M:%S')}",
            f"pristine={PRISTINE}",
            f"pristine_sha256={source_sha_snapshot}",
            f"probe_source={PROBE_SRC}",
            f"probe_source_sha256_at_battery={sha256(PROBE_SRC)}",
            f"real_receipt_present={REAL.is_file()}",
            ""]

    # --- anchor receipt: the real receipt of record if it exists, else the
    # pristine tool's own text-faithful synthesis (documented as a stand-in).
    mod = deep_import(PRISTINE, "r64probe_pristine")
    good = FIX / "good-receipt.txt"
    anchor_kind = ""
    if REAL.is_file():
        shutil.copyfile(REAL, good)
        anchor_kind = "receipt-of-record"
    else:
        good.write_text(mod.synth_receipt(), encoding="utf-8")
        anchor_kind = "synth-from-pristine (receipt of record absent at battery time)"
    head.append(f"anchor={good} kind={anchor_kind} sha256={sha256(good)}")

    good_text = good.read_text(encoding="utf-8")

    # --- corrupted receipts, each the exact corruption its check guards
    bad = {}

    frag_line = [ln for ln in good_text.splitlines() if ln.startswith("K2-FRAGMENT ")][0]
    k2_leg5 = [ln for ln in good_text.splitlines() if ln.startswith("LEG K2 5 ")][0]
    t = good_text.replace(frag_line, "K2-FRAGMENT unrelated message")
    t = t.replace(k2_leg5, k2_leg5.split("frag=")[0] + "frag=unrelated message")
    bad["m2"] = FIX / "bad-m2-no-k2-fragment.txt"
    bad["m2"].write_text(t, encoding="utf-8")

    t = good_text.replace("PORTFREE before-battery True",
                          "PORTFREE before-battery False")
    bad["m3"] = FIX / "bad-m3-port-not-free-at-start.txt"
    bad["m3"].write_text(t, encoding="utf-8")

    case4 = [ln for ln in good_text.splitlines() if ln.startswith("CASE K4 ")][0]
    t = good_text.replace(case4 + "\n", "")
    bad["m4"] = FIX / "bad-m4-no-case-k4.txt"
    bad["m4"].write_text(t, encoding="utf-8")

    # receipt-side vector flip (control for m1: the checker catches a flip)
    vec_k3 = [ln for ln in good_text.splitlines() if ln.startswith("VECTOR K3=")][0]
    cells = vec_k3.split("=", 1)[1].split("/")
    cells[5] = "P" if cells[5] == "F" else "F"
    bad["m1"] = FIX / "bad-m1-vector-k3-leg6-flip.txt"
    bad["m1"].write_text(good_text.replace(vec_k3, "VECTOR K3=" + "/".join(cells)),
                         encoding="utf-8")

    # --- mutation specs (smallest behaviour-bearing edit per defect)
    specs = {
        "m1": [
            ('    "K3": ("P", "P", "P", "P", "P", "F", "F"),',
             '    "K3": ("P", "P", "P", "P", "P", "P", "F"),', 1),
        ],
        "m2": [
            ('    if K2_LEG5_FRAGMENT not in fragment_line:\n'
             '        failures.append("k2-fragment %s lacks %r"\n'
             '                        % (fragment_line or "(missing)", K2_LEG5_FRAGMENT))\n'
             '    if K2_LEG5_FRAGMENT not in leg_frags.get("K2", {}).get(5, ""):\n'
             '        failures.append("k2 leg-5 fragment does not carry the frozen fragment")\n',
             '    # mutant m2: the frozen K2 leg-5 fragment is no longer checked\n', 1),
        ],
        "m3": [
            ('    if "PORTFREE before-battery True" not in lines:\n'
             '        failures.append("port-free-at-battery-start not recorded")\n',
             '    # mutant m3: port-free-at-battery-start is no longer checked\n', 1),
        ],
        "m4": [
            ('            failures.append("%s case-line-missing" % name)',
             '            pass  # mutant m4: a missing CASE line is accepted', 1),
        ],
    }
    expect_fail = {
        "m1": "K3",
        "m2": "k2",
        "m3": "port-free-at-battery-start",
        "m4": "K4 case-line-missing",
    }
    detectors = {
        "m1": "receipt-of-contract anchor: mutant must fail the good receipt",
        "m2": "corrupt receipt: K2 fragment replaced",
        "m3": "corrupt receipt: PORTFREE before-battery False",
        "m4": "corrupt receipt: CASE K4 line deleted",
    }

    summary = []
    for name in ("m1", "m2", "m3", "m4"):
        mdir = S / "mutants" / name
        mdir.mkdir(parents=True, exist_ok=True)
        mutant = mdir / "round64_c1_kvstore_probe.py"
        diff = apply_mutation(PRISTINE, mutant, specs[name],
                              RECEIPTS / f"{name}-diff.txt")

        (WORK / f"st-pristine-{name}").mkdir(parents=True, exist_ok=True)
        (WORK / f"st-mutant-{name}").mkdir(parents=True, exist_ok=True)
        pristine_run_good = run([sys.executable, str(PRISTINE), "--check-receipt", str(good)], S)
        pristine_run_bad = run([sys.executable, str(PRISTINE), "--check-receipt", str(bad[name])], S)
        mutant_run_bad = run([sys.executable, str(mutant), "--check-receipt", str(bad[name])], S)
        mutant_run_good = run([sys.executable, str(mutant), "--check-receipt", str(good)], S)
        st_pristine = run([sys.executable, str(PRISTINE), "--selftest", "--work", str(WORK / f"st-pristine-{name}")], S)
        st_mutant = run([sys.executable, str(mutant), "--selftest", "--work", str(WORK / f"st-mutant-{name}")], S)

        # verdict for m1 is contract-drift detection; m2..m4 are "does the tool
        # still reject the corruption its deleted check used to catch"
        if name == "m1":
            killed = mutant_run_good["rc"] != 0
            mech = "--check-receipt on the contract anchor" if killed else "none"
        else:
            killed = mutant_run_bad["rc"] != 0
            mech = "--check-receipt" if killed else ""
        if not killed and st_mutant["rc"] != 0:
            killed, mech = True, "--selftest"

        checks = []
        if name == "m1":
            checks.append(f"pristine_on_good_rc={pristine_run_good['rc']} (expect 0)")
            checks.append(f"mutant_on_good_rc={mutant_run_good['rc']} (drift detector)")
            checks.append(f"pristine_on_vector-flip_rc={pristine_run_bad['rc']} (control, expect 1)")
        else:
            checks.append(f"pristine_on_good_rc={pristine_run_good['rc']} (expect 0)")
            checks.append(f"pristine_on_corrupt_rc={pristine_run_bad['rc']} (expect 1)")
            checks.append(f"mutant_on_corrupt_rc={mutant_run_bad['rc']} (0 => survived)")
            checks.append(f"mutant_on_good_rc={mutant_run_good['rc']} (expect 0, gross-break guard)")
        checks.append(f"selftest_pristine_rc={st_pristine['rc']} (expect 0)")
        checks.append(f"selftest_mutant_rc={st_mutant['rc']} (0 => selftest blind)")

        text = "\n".join(head + [
            f"# mutation {name}",
            f"defect={detectors[name]}",
            f"mutant={mutant}",
            f"mutant_sha256={sha256(mutant)}",
            f"changed={sha256(mutant) != source_sha_snapshot}",
            "",
            block(f"pristine-good [{name}]", pristine_run_good, 0),
            "",
            block(f"pristine-corrupt [{name}]", pristine_run_bad, 1),
            "",
            block(f"mutant-corrupt [{name}]", mutant_run_bad, "0 => SURVIVED"),
            "",
            block(f"mutant-good [{name}]", mutant_run_good, 0),
            "",
            block(f"selftest-pristine [{name}]", st_pristine, 0),
            "",
            block(f"selftest-mutant [{name}]", st_mutant, 0),
            "",
            "--- mutation diff ---", diff,
            "",
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
