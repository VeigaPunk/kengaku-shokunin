#!/usr/bin/env python3
"""Build R68-C1 checker mutants (one deleted check each) and forged fixtures.

Every artefact lives under the seat scratch root; the lane repo is read-only.
m1-m10 are the seat-specified set; m11-m22 extend coverage to the remaining
checks of the frozen R68-C1 sentence.
"""
import hashlib
import json
import os
import pathlib
import py_compile
import shutil
import sys

L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r68/CounterMutate")
SRC = L / "plans/round68_c1_pypi_finish.py"
BASE = L / "plans/round63_c1_pypi_probe.py"
RECEIPT = L / "corpus/evidence/round68/pypi/receipt.txt"
GRADER_REL = "corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py"
STDERR_REL = "corpus/evidence/round68/pypi/stderr"
LOG_REL = "corpus/evidence/round68/pypi/server-log.txt"

FROZEN_PROBE_SHA = "4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc"
ZERO = "0" * 64

# (id, human label, 1-based inclusive line range in the frozen probe, defect key removed)
MUTANTS = [
    ("m1", "PROBE binding deleted", (250, 254), "probe-sha"),
    ("m2", "BASE-PROBE binding deleted", (256, 264), "base-probe-sha + base-probe-bytes"),
    ("m3", "grader-bytes re-hash deleted", (274, 276), "grader-bytes"),
    ("m4", "duplicate-CASE detection deleted", (293, 294), "case-duplicate"),
    ("m5", "unknown-case detection deleted", (295, 297), "case-unknown"),
    ("m6", "K2 clause-bytes check deleted", (353, 354), "k2-clause-bytes"),
    ("m7", "per-case stderr binding deleted", (358, 368), "*-stderr-sha + *-stderr-capture"),
    ("m8", "server-log fetch-proof checks deleted", (332, 335), "server-log-simple + server-log-wheel"),
    ("m9", "exit-agreement check deleted", (390, 391), "exit-agreement"),
    ("m10", "stored-predicate agreement deleted", (392, 393), "stored-predicate"),
    # --- extension coverage: the remaining clauses of the frozen sentence --------
    ("m11", "per-case observed/expected checks deleted", (306, 309), "*-observed + *-expected"),
    ("m12", "GRADER receipt sha+pin checks deleted", (270, 273), "grader-sha + grader-pin"),
    ("m13", "K1 index_pid check deleted", (315, 316), "K1-index-pid"),
    ("m14", "K1 wheel-sha check deleted", (318, 319), "K1-wheel-sha"),
    ("m15", "server-log sha binding deleted", (329, 330), "server-log-sha"),
    ("m16", "K2 clause line check deleted", (341, 342), "k2-clause-line"),
    ("m17", "K2 connection-refused check deleted", (355, 356), "k2-refused"),
    ("m18", "CLASS line check deleted", (371, 372), "class-line"),
    ("m19", "PREDICTION-VECTOR line checks deleted", (378, 381), "prediction-vector + prediction-drift"),
    ("m20", "per-case leg check deleted", (310, 311), "*-leg"),
    ("m21", "case-missing defect deleted", (302, 302), "*-case-missing"),
    ("m22", "server-log flags check deleted", (336, 337), "server-log-flags"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def build_mutants():
    lines = SRC.read_text(encoding="utf-8").splitlines(keepends=True)
    assert sha(SRC.read_bytes()) == FROZEN_PROBE_SHA, "frozen probe bytes drifted"
    built = []
    for mid, label, (a, b), removed in MUTANTS:
        assert a <= b, f"{mid}: empty range"
        first = lines[a - 1]
        indent = first[: len(first) - len(first.lstrip())]
        marker = (f"{indent}pass  # MUTANT {mid}: {label} -- check removed: {removed}\n")
        out = lines[: a - 1] + [marker] + lines[b:]
        d = S / "mut" / mid / "plans"
        d.mkdir(parents=True, exist_ok=True)
        target = d / "round68_c1_pypi_finish.py"
        target.write_text("".join(out), encoding="utf-8")
        bp = d / BASE.name
        if bp.is_symlink() or bp.exists():
            bp.unlink()
        os.symlink(BASE, bp)
        cl = S / "mut" / mid / "corpus"
        if cl.is_symlink() or cl.exists():
            cl.unlink() if cl.is_symlink() else shutil.rmtree(cl)
        os.symlink(L / "corpus", cl)
        py_compile.compile(str(target), cfile=str(S / "run" / f"{mid}.pyc"),
                           doraise=True)
        removed_text = "".join(lines[a - 1: b])
        built.append({"id": mid, "label": label, "lines": [a, b],
                      "defect_key": removed,
                      "removed_sha256": sha(removed_text.encode()),
                      "mutant_sha256": sha(target.read_bytes()),
                      "removed_block": removed_text})
    return built


def lane_copy(dst, name):
    """Minimal lane tree carrying the evidence bytes check_receipt reads."""
    root = dst / name
    if root.exists():
        shutil.rmtree(root)
    (root / "plans").mkdir(parents=True)
    shutil.copy2(BASE, root / "plans" / BASE.name)
    g = root / GRADER_REL
    g.parent.mkdir(parents=True)
    shutil.copy2(L / GRADER_REL, g)
    sd = root / STDERR_REL
    sd.mkdir(parents=True)
    for f in sorted((L / STDERR_REL).glob("*.txt")):
        shutil.copy2(f, sd / f.name)
    shutil.copy2(L / LOG_REL, root / LOG_REL)
    return root


def main():
    (S / "run").mkdir(parents=True, exist_ok=True)
    (S / "fix").mkdir(parents=True, exist_ok=True)
    built = build_mutants()
    rec = RECEIPT.read_text(encoding="utf-8")
    rec_lines = rec.splitlines(keepends=True)
    fixtures = {}

    def sub_once(text, old, new, what):
        assert text.count(old) == 1, f"{what}: {text.count(old)} occurrences of {old!r}"
        return text.replace(old, new)

    def line_starting(prefix):
        return next(ln for ln in rec_lines if ln.startswith(prefix))

    def write_fixture(name, body, lane, expectation):
        p = S / "fix" / f"{name}.txt"
        p.write_text(body, encoding="utf-8")
        fixtures[name] = {"receipt": str(p), "lane": str(lane),
                          "expect": expectation}

    k1_line = line_starting("CASE K1 ")
    k3_line = line_starting("CASE K3 ")
    k2_sha = line_starting("CASE K2 ").split("stderr_sha256=")[1].strip()
    k1_sha = k1_line.split("stderr_sha256=")[1].strip()
    log_sha = line_starting("K1 server-log ").split("sha256=")[1].split()[0]

    # --- receipt-only forgeries, lane = the real lane -------------------------
    write_fixture("F-probe",
                  sub_once(rec, f"PROBE sha256={FROZEN_PROBE_SHA}",
                           f"PROBE sha256={ZERO}", "probe"), L, "probe-sha")
    write_fixture("F-base",
                  sub_once(rec, "BASE-PROBE sha256=2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929",
                           f"BASE-PROBE sha256={ZERO}", "base"), L, "base-probe-sha")

    write_fixture("F-dup", sub_once(rec, k1_line, k1_line + k1_line, "dup-case"),
                  L, "case-duplicate")

    unknown = rec + (f"CASE K9 leg=test_api observed=P expected=P exception=none "
                     f"index_pid=1 wheel_sha256={'a' * 64} stderr_sha256={'b' * 64}\n")
    write_fixture("F-unknown", unknown, L, "case-unknown")

    write_fixture("F-k1-stderr", sub_once(rec, k1_sha, ZERO, "k1-stderr-sha"),
                  L, "K1-stderr-sha")
    write_fixture("F-k3-stderr",
                  sub_once(rec, k3_line.split("stderr_sha256=")[1].strip(), ZERO,
                           "k3-stderr-sha"), L, "K3-stderr-sha")
    write_fixture("F-exit", sub_once(rec, "CLASS-PROBE-EXIT=0", "CLASS-PROBE-EXIT=1",
                                     "exit"), L, "exit-agreement")
    write_fixture("F-stored", sub_once(rec, "PREDICATE R68-C1 pass",
                                       "PREDICATE R68-C1 fail", "stored"),
                  L, "stored-predicate")
    write_fixture("F-log-flags", sub_once(rec, "served_wheel=True",
                                          "served_wheel=False", "flags"),
                  L, "server-log-flags")
    write_fixture("F-grader-sha",
                  sub_once(rec, "sha256=82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c",
                           f"sha256={ZERO}", "grader-sha"), L, "grader-sha")

    # --- extension fixtures ---------------------------------------------------
    write_fixture("F-k1-observed",
                  sub_once(rec, k1_line,
                           k1_line.replace("observed=P", "observed=F"),
                           "k1-observed"),
                  L, "K1-observed")

    write_fixture("F-k1-pid",
                  sub_once(rec, k1_line, k1_line.replace("index_pid=1323016",
                                                         "index_pid=none"),
                           "k1-pid"), L, "K1-index-pid")

    write_fixture("F-k1-wheel",
                  sub_once(rec, k1_line, k1_line.replace(
                      "wheel_sha256=6fad8ea86492def2ce9bb48ba80c11e2b35ce88d8d2ea3757c276754c9d0ced6",
                      "wheel_sha256=xyz"), "k1-wheel"), L, "K1-wheel-sha")

    write_fixture("F-k1-leg",
                  sub_once(rec, k1_line, k1_line.replace("leg=test_api",
                                                         "leg=test_other"),
                           "k1-leg"), L, "K1-leg")

    write_fixture("F-missing",
                  "".join(ln for ln in rec_lines if not ln.startswith("CASE K4 ")),
                  L, "K4-case-missing")

    write_fixture("F-log-sha",
                  sub_once(rec, log_sha, ZERO, "log-sha"), L, "server-log-sha")

    write_fixture("F-k2-line",
                  sub_once(rec, "K2 stderr-names-endpoint=True",
                           "K2 stderr-names-endpoint=False", "k2-line"),
                  L, "k2-clause-line")

    write_fixture("F-class",
                  sub_once(rec, "CLASS network-service executed=2",
                           "CLASS network-service executed=1", "class"),
                  L, "class-line")

    write_fixture("F-pred",
                  sub_once(rec, "PREDICTION-VECTOR P/F/F/F derived=P/F/F/F",
                           "PREDICTION-VECTOR P/F/F/F derived=F/F/F/F", "pred"),
                  L, "prediction-vector")

    write_fixture("F-grader-pin",
                  sub_once(rec, "pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6",
                           "pin=" + "0" * 40, "grader-pin"), L, "grader-pin")

    write_fixture("F-k1-expected",
                  sub_once(rec, k1_line,
                           k1_line.replace("expected=P", "expected=F"),
                           "k1-expected"), L, "K1-expected")

    # K2's sha is bound twice (its own clause and the per-case loop): a forged K2
    # sha must still be refused when either binding is deleted.
    write_fixture("F-k2-stderr-sha", sub_once(rec, k2_sha, ZERO, "k2-stderr-sha"),
                  L, "k2-stderr-sha")

    # control: the fabricated all-P vector the selftest's r1 refuses
    def flip(line):
        out = []
        for tok in line.split():
            if tok.startswith("observed="):
                out.append("observed=P")
            elif tok.startswith("exception="):
                out.append("exception=none")
            else:
                out.append(tok)
        return " ".join(out) + "\n"

    allp = "".join(flip(ln) if ln.startswith(("CASE K2 ", "CASE K3 ", "CASE K4 "))
                   else ln for ln in rec_lines)
    assert "observed=P expected=F" in allp
    write_fixture("F-vector", allp, L, "K2-observed")

    # --- forged-lane forgeries ------------------------------------------------
    root = lane_copy(S / "fix", "lane-grader-drift")
    g = root / GRADER_REL
    g.write_bytes(g.read_bytes() + b"\n# drift\n")
    write_fixture("F-grader-bytes", rec, root, "grader-bytes")

    root = lane_copy(S / "fix", "lane-k2-clause")
    k2 = root / STDERR_REL / "K2.txt"
    k2_text = k2.read_text(encoding="utf-8")
    assert "host='localhost'" in k2_text and "port=8080" in k2_text
    forged = k2_text.replace("host='localhost'", "host='LOCALHOST'").replace(
        "port=8080", "port=9999")
    assert "Connection refused" in forged or "Errno 111" in forged
    k2.write_text(forged, encoding="utf-8")
    write_fixture("F-k2-clause", sub_once(rec, k2_sha, sha(forged.encode()),
                                          "k2-clause"), root, "k2-clause-bytes")

    root = lane_copy(S / "fix", "lane-k2-refused")
    k2 = root / STDERR_REL / "K2.txt"
    k2_text = k2.read_text(encoding="utf-8")
    forged = (k2_text.replace("[Errno 111] Connection refused", "[refused]")
              .replace("Errno 111", "refused").replace("Connection refused", "refused"))
    assert "host='localhost'" in forged and "port=8080" in forged
    assert "Errno 111" not in forged and "Connection refused" not in forged
    k2.write_text(forged, encoding="utf-8")
    write_fixture("F-k2-refused", sub_once(rec, k2_sha, sha(forged.encode()),
                                           "k2-refused"), root, "k2-refused")

    orig_log = (L / LOG_REL).read_text(encoding="utf-8")
    for name, needle, want in (("F-log-no-simple", "/simple/vectorops", "server-log-simple"),
                               ("F-log-no-wheel", "/packages/vectorops-0.1.0-", "server-log-wheel")):
        root = lane_copy(S / "fix", f"lane-{name.lower()}")
        kept = "".join(ln for ln in orig_log.splitlines(keepends=True)
                       if needle not in ln)
        assert needle not in kept and kept != orig_log
        (root / LOG_REL).write_text(kept, encoding="utf-8")
        write_fixture(name, sub_once(rec, log_sha, sha(kept.encode()), name),
                      root, want)

    root = lane_copy(S / "fix", "lane-k2-capture-missing")
    (root / STDERR_REL / "K2.txt").unlink()
    write_fixture("F-k2-capture-missing", rec, root, "k2-stderr-capture")

    root = lane_copy(S / "fix", "lane-log-missing")
    (root / LOG_REL).unlink()
    write_fixture("F-log-missing", rec, root, "server-log")

    root = lane_copy(S / "fix", "lane-k4-capture")
    (root / STDERR_REL / "K4.txt").unlink()
    write_fixture("F-k4-capture", rec, root, "K4-stderr-capture")

    manifest = {"frozen_probe_sha256": FROZEN_PROBE_SHA,
                "mutants": built, "fixtures": fixtures,
                "record_receipt_sha256": sha(RECEIPT.read_bytes()),
                "lane": str(L)}
    (S / "run" / "manifest.json").write_text(json.dumps(manifest, indent=2),
                                             encoding="utf-8")
    print(f"BUILT mutants={len(built)} fixtures={len(fixtures)}")
    for m in built:
        print(f"  {m['id']:<4} sha={m['mutant_sha256'][:12]} lines={m['lines']} {m['label']}")
    for k, v in fixtures.items():
        print(f"  FIX {k:<16} lane={pathlib.Path(v['lane']).name:<26} expect={v['expect']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
