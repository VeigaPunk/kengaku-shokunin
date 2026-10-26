#!/usr/bin/env python3
"""Re-run every case of the frozen fibsqrt probe's gates content under all 11 builds.

Only the sim's stdout depends on the compiler; the gates content per case is byte-fixed, so
test 3's verdict per build is computable from the 28 graded inputs.
"""
import concurrent.futures as cf, importlib.util, json, pathlib, subprocess, sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/F42CompilerSens")
CIR = S / "circuits"
CASES = S / "cases"; CASES.mkdir(exist_ok=True)
ENV = ["bwrap", "--dev-bind", "/", "/", "--ro-bind", "/home/vgpnk/.local/bin", "/home/vgpnk/.local/bin",
       "--tmpfs", "/run/user/1000", "--proc", "/proc", "--unshare-pid", "--die-with-parent"]
spec = importlib.util.spec_from_file_location("probe", S / "probe.py")
probe = importlib.util.module_from_spec(spec); sys.modules["probe"] = probe; spec.loader.exec_module(probe)
exp = dict(l.split("\t") for l in (CIR / "expected.tsv").read_text().splitlines())
GRADED = [str(n) for n in probe.GRADED]
BUILDS = ["gcc16-O0", "gcc16-O1", "gcc16-O2", "gcc16-O3", "gcc16-Os", "gcc16-O3-native", "gcc16-O3-lto",
          "clang23-O0", "clang23-O2", "clang23-O3", "bw12-O0", "bw12-O2", "bw12-O3"]
SAN = ["gcc16-ubsan", "clang23-ubsan"]


def materialise(case):
    d = CASES / case.cid; d.mkdir(exist_ok=True)
    g = (d / "gates.txt")
    if g.exists() or g.is_symlink():
        g.unlink()
    if case.cid == "oracle-solve-sh":
        g.write_bytes((CIR / "oracle" / "gates.txt").read_bytes()); return d, "file"
    if case.gates is None:
        return d, "missing"
    if case.gates == "<dir>":
        g.mkdir(); return d, "dir"
    txt = (CIR / "shipped" / "gates.txt").read_text() if case.gates == "" else case.gates
    if case.gates == "<empty>":
        txt = ""
    g.write_text(txt); return d, "file"


def run(build, d, n):
    r = subprocess.run(ENV + [str(S / "bin" / build), n], cwd=str(d), capture_output=True, text=True, timeout=900)
    return build, n, r.returncode, r.stdout.strip(), r.stderr.strip()[:160]


def main():
    rows = []
    for case in probe.CASES:
        d, kind = materialise(case)
        lines = 0
        if kind == "file":
            lines = sum(1 for _ in open(d / "gates.txt", "rb"))
        t1 = kind != "missing"
        t2 = kind == "file" and lines < 32000
        outs = {}
        if kind == "file":
            jobs = [(b, str(d), n) for b in BUILDS + SAN for n in GRADED]
            with cf.ThreadPoolExecutor(max_workers=8) as ex:
                for b, n, rc, out, err in ex.map(lambda a: run(*a), jobs):
                    outs.setdefault(b, {})[n] = (rc, out, err)
            verdicts = {}
            for b, per in outs.items():
                ok = all(per[n][0] == 0 and per[n][1] == exp[n] for n in GRADED)
                verdicts[b] = "P" if ok else "F"
        else:
            verdicts = {}
        letters = {}
        for b in BUILDS + SAN:
            letters[b] = ("P" if t1 else "F") + ("P" if t2 else "F") + verdicts.get(b, "F")
        uniq = sorted(set(letters.values()))
        pred = case.predicted
        rows.append((case.cid, kind, lines, pred, uniq, letters))
        print(f"{case.cid:26s} kind={kind:8s} lines={lines:6d} predicted={pred} builds_verdicts={uniq} "
              f"{'' if uniq == [pred] else '<<< DIFFERS'}")
        # sim-stdout divergence across builds
        if kind == "file":
            dv = [n for n in GRADED if len({(outs[b][n][0], outs[b][n][1]) for b in outs}) > 1]
            if dv:
                print(f"   stdout divergence across {len(outs)} builds on {len(dv)} inputs, e.g. " +
                      "; ".join(f"n={n}:" + str(sorted({(b, outs[b][n][0], outs[b][n][1]) for b in outs})[:3]) for n in dv[:2]))
            sanerr = [(b, n, outs[b][n][2]) for b in SAN for n in GRADED if outs[b][n][2]]
            print(f"   sanitizer_stderr_cells={len(sanerr)} rc_nonzero={sum(1 for b in outs for n in GRADED if outs[b][n][0])}")
    (S / "case_matrix.json").write_text(json.dumps(
        [{"cid": r[0], "kind": r[1], "lines": r[2], "predicted": r[3], "verdicts": r[5]} for r in rows], indent=1))
    bad = [r for r in rows if r[4] != [r[3]]]
    print(f"\ncases={len(rows)} cases_where_build_choice_changes_verdicts={len(bad)}")
    for r in bad:
        print("  CHANGES:", r[0], r[3], r[4])


if __name__ == "__main__":
    main()
