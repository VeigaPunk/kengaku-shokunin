#!/usr/bin/env python3
"""F37XMutD5 witness fixtures for the survivors found by harness.py.

Each witness is ONE fixture the full round-37 battery does not contain, built here from lane bytes in
scratch (nothing is added to the lane). It shows whether a survivor is killable by adding a fixture
(smallest safe correction: a battery row, not a gate change) or is structurally invisible to the
counter's observable (exit code, set of clause ids).

  W3  manifest whose matching digest row is NOT the first row (decoy row first)  -> kills X3
  W4  capture holding only a 20-character prefix of the quote, manifest re-pinned -> kills X4
  W5  capture holding the quote split by an HTML tag, manifest re-pinned            -> kills S2
  W6  capture holding the quote split by a newline, manifest re-pinned             -> kills S3
  W5  any input at all                                                            -> cannot kill S1

Run: python3 witness.py --lane CLONE --gate CLONE/plans/pkg_gate.py
"""
import argparse
import hashlib
import importlib.util
import pathlib
import py_compile
import shutil
import subprocess
import sys
import tempfile


def load_counter(lane):
    spec = importlib.util.spec_from_file_location("k37_counter", lane / "plans/round37_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_w3(c, ctx, d):
    d5 = ctx.spec["d5"]
    src = ctx.d5_capture_dir()
    cap = d / "caps"
    cap.mkdir()
    for name in (d5["capture_name"], d5["manifest_name"]):
        shutil.copyfile(src / name, cap / name)
    rows = (cap / d5["manifest_name"]).read_text().splitlines()
    path = rows[0].split()[-1]
    decoy = hashlib.sha256(b"decoy-not-the-capture").hexdigest()
    (cap / d5["manifest_name"]).write_text(f"{decoy}  {path}\n" + "\n".join(rows) + "\n")
    f = d / "erratum.txt"
    f.write_text(ctx.d5_line() + "\n")
    return ["d5-line", "--file", str(f), "--capture-dir", str(cap)]


def build_w4(c, ctx, d):
    d5 = ctx.spec["d5"]
    src = ctx.d5_capture_dir()
    cap = d / "caps"
    cap.mkdir()
    for name in (d5["capture_name"], d5["manifest_name"]):
        shutil.copyfile(src / name, cap / name)
    capture = cap / d5["capture_name"]
    quote = d5["quote"]
    text = capture.read_text()
    assert quote in text
    capture.write_text(text.replace(quote, quote[:20], 1))
    digest = hashlib.sha256(capture.read_bytes()).hexdigest()
    (cap / d5["manifest_name"]).write_text(f"{digest}  {ctx.spec['d5_capture_dir']}/{d5['capture_name']}\n")
    f = d / "erratum.txt"
    f.write_text(ctx.d5_line() + "\n")
    return ["d5-line", "--file", str(f), "--capture-dir", str(cap)]


def _split_quote(ctx, d, joiner):
    """Genuine erratum + capture whose quote is split by `joiner`, manifest re-pinned to the new bytes."""
    d5 = ctx.spec["d5"]
    src = ctx.d5_capture_dir()
    cap = d / "caps"
    cap.mkdir()
    for name in (d5["capture_name"], d5["manifest_name"]):
        shutil.copyfile(src / name, cap / name)
    capture = cap / d5["capture_name"]
    quote = d5["quote"]
    text = capture.read_text()
    assert quote in text
    capture.write_text(text.replace(quote, quote[:35] + joiner + quote[35:], 1))
    digest = hashlib.sha256(capture.read_bytes()).hexdigest()
    (cap / d5["manifest_name"]).write_text(f"{digest}  {ctx.spec['d5_capture_dir']}/{d5['capture_name']}\n")
    f = d / "erratum.txt"
    f.write_text(ctx.d5_line() + "\n")
    return ["d5-line", "--file", str(f), "--capture-dir", str(cap)]


def build_w5(c, ctx, d):
    return _split_quote(ctx, d, "</b><b>")


def build_w6(c, ctx, d):
    return _split_quote(ctx, d, "\n")


WITNESSES = [("W3-manifest-match-row-2", build_w3), ("W4-quote-truncated-to-20", build_w4),
              ("W5-quote-split-by-tags", build_w5), ("W6-quote-split-by-newline", build_w6)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--gate", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    gate = pathlib.Path(a.gate).resolve() if a.gate else lane / "plans/pkg_gate.py"
    c = load_counter(lane)
    src = gate.read_text()
    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k37-wit-", dir=tempfile.gettempdir()))
    try:
        ref_gate = root / "ref.py"
        ref_gate.write_text(src)
        built = []
        for i, (fid, build) in enumerate(WITNESSES):
            d = root / f"w{i}"
            d.mkdir()
            built.append((fid, d, build(c, ctx, d)))
        # mutants from harness.py, read as source so the two files cannot drift apart
        hspec = importlib.util.spec_from_file_location(
            "k37_d5_harness", pathlib.Path(__file__).with_name("harness.py"))
        h = importlib.util.module_from_spec(hspec)
        hspec.loader.exec_module(h)
        gates = {"REFERENCE": ref_gate}
        for mid, _label, old, new in h.MUTANTS:
            assert src.count(old) == 1, mid
            g = root / f"{mid}.py"
            g.write_text(src.replace(old, new, 1))
            py_compile.compile(str(g), doraise=True, cfile=str(root / f"{mid}.pyc"))
            gates[mid] = g
        print("WITNESS reference results")
        ref = {}
        for fid, d, argv in built:
            out = subprocess.run([sys.executable, str(ref_gate), *argv, "--spec", str(ctx.spec_path)],
                                 capture_output=True, text=True)
            note = next(l for l in out.stdout.splitlines() if l.startswith("D5 "))
            ref[fid] = c.run_gate(ref_gate, ctx.spec_path, argv)
            print(f"  {fid} rc={out.returncode} :: {note}")
        for mid, g in gates.items():
            if mid == "REFERENCE":
                continue
            diffs = [fid for fid, _d, argv in built if c.run_gate(g, ctx.spec_path, argv) != ref[fid]]
            print(f"WITNESS {mid} {'KILLED by=' + diffs[0] if diffs else 'SURVIVED'}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
