#!/usr/bin/env python3
"""F42CompilerSens: compiler/flag sensitivity of the tb2 circuit-fibsqrt sim on the graded circuits."""
import concurrent.futures as cf, json, os, pathlib, subprocess, sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/F42CompilerSens")
CAP = S / "cap" / "sim.c"
BIN = S / "bin"; BIN.mkdir(exist_ok=True)
CIR = S / "circuits"
ENV = ["bwrap", "--dev-bind", "/", "/", "--ro-bind", "/home/vgpnk/.local/bin", "/home/vgpnk/.local/bin",
       "--tmpfs", "/run/user/1000", "--proc", "/proc", "--unshare-pid", "--die-with-parent"]

HOST = {
    "gcc16-O0": ["gcc", "-O0"], "gcc16-O1": ["gcc", "-O1"], "gcc16-O2": ["gcc", "-O2"],
    "gcc16-O3": ["gcc", "-O3"], "gcc16-Os": ["gcc", "-Os"],
    "clang23-O0": ["clang", "-O0"], "clang23-O2": ["clang", "-O2"], "clang23-O3": ["clang", "-O3"],
}

exp = {}
for line in (CIR / "expected.tsv").read_text().splitlines():
    k, v = line.split("\t"); exp[k] = v
INPUTS = [str(k) for k in exp]           # 28 graded + 208 + 20000, order preserved
GRADED = {k for k in INPUTS if k not in ("208", "20000")}


def compile_host():
    for name, cmd in HOST.items():
        p = BIN / name
        r = subprocess.run(ENV + cmd + [str(CAP), "-o", str(p)], capture_output=True, text=True)
        print(f"COMPILE {name} rc={r.returncode} warn={len(r.stderr.splitlines())}")
        if r.returncode:
            print(r.stderr); sys.exit(2)


def compile_bookworm():
    script = "set -e; apt-get update -qq >/dev/null; apt-get install -y -qq gcc >/dev/null; " + \
             "gcc --version | head -1 | sed 's/^/VERSION /'; " + \
             " ".join(f"gcc {flag} /w/cap/sim.c -o /w/bin/bw12-{tag};" for tag, flag in
                      (("O0", "-O0"), ("O2", "-O2"), ("O3", "-O3")))
    r = subprocess.run(ENV + ["docker", "run", "--rm", "-v", f"{S}:/w", "debian:bookworm", "sh", "-c", script],
                       capture_output=True, text=True)
    print("COMPILE bookworm rc=%d %s" % (r.returncode, r.stdout.strip()))
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(2)


def run_one(variant, circuit, n):
    r = subprocess.run([str(BIN / variant), n], cwd=str(CIR / circuit), capture_output=True, text=True,
                       timeout=600)
    return variant, circuit, n, r.returncode, r.stdout, r.stderr


def main():
    compile_host()
    compile_bookworm()
    variants = sorted(HOST) + ["bw12-O0", "bw12-O2", "bw12-O3"]
    circuits = ["oracle", "lookup30", "lookup28", "trailing30", "trailing28", "shipped"]
    jobs = [(v, c, n) for v in variants for c in circuits for n in INPUTS]
    res = {}
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("PAR", "6"))) as ex:
        for v, c, n, rc, out, err in ex.map(lambda a: run_one(*a), jobs):
            res.setdefault(c, {}).setdefault(n, {})[v] = {"rc": rc, "out": out.strip(), "err": err.strip()[:200]}
    (S / "matrix.json").write_text(json.dumps(res, indent=1, sort_keys=True))

    print("\n== per-circuit output divergence across variants ==")
    for c in circuits:
        groups = {}
        for n in INPUTS:
            sig = tuple(sorted({res[c][n][v]["out"] for v in variants}))
            groups.setdefault(sig, []).append(n)
        print(f"{c}: distinct_output_sets={len(groups)}")
        for sig, ns in groups.items():
            print(f"   outputs={sig} n={len(ns)} first={ns[:3]}")
        # expected check
        bad = []
        for n in INPUTS:
            outs = {res[c][n][v]["out"] for v in variants}
            if c == "oracle" or c == "lookup30":
                want = exp[n]
            elif c == "lookup28":
                want = exp[n] if n in GRADED else "0"
            elif c == "shipped":
                want = str(int(n) >> 1)
            else:
                want = ""
            if outs != {want}:
                bad.append((n, want, sorted(outs)))
        print(f"   expected_bad_inputs={len(bad)}/{len(INPUTS)}" + (f" e.g. {bad[:3]}" if bad else ""))
        errs = sum(1 for n in INPUTS for v in variants if res[c][n][v]["err"])
        rcs = {res[c][n][v]["rc"] for n in INPUTS for v in variants}
        print(f"   nonzero_stderr_cells={errs} distinct_rc={sorted(rcs)}")

    print("\n== stderr previews ==")
    seen = set()
    for c in circuits:
        for n in INPUTS:
            for v in variants:
                e = res[c][n][v]["err"]
                if e and (c, e[:60]) not in seen:
                    seen.add((c, e[:60])); print(f"   {c}/{n}/{v}: {e!r}")


if __name__ == "__main__":
    main()
