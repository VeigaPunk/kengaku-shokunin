#!/usr/bin/env python3
"""R40PlanNext pre-freeze witnesses for six proposed tip_receipts.py mutants (round-41 candidate). Builds fake lanes
(git repos carrying the exact RECEIPTS rel paths) in $S, runs the unmodified tool and each mutant, prints rc + first lines.
Mutants are the harness's (res_tip_receipts.json): applied by line + description, single replacement."""
import json, os, pathlib, shutil, subprocess, sys
S = pathlib.Path(sys.argv[1]); R = pathlib.Path(sys.argv[2]); TOOL = pathlib.Path(sys.argv[3])
src = TOOL.read_bytes(); muts = json.load(open(R / "res_tip_receipts.json"))["mutants"]
def pick(line, desc): return next(m for m in muts if m["line"] == line and m["desc"] == desc)
def sh(*a, cwd=None, **k): return subprocess.run(a, cwd=cwd, capture_output=True, text=True, **k)
def mk(name, receipts, script_body_by_script, evidence=True, subdir=False):
    d = S / name; shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    sh("git", "init", "-q", cwd=d); 
    for k, v in [("user.name", "w"), ("user.email", "w@x")]: sh("git", "config", k, v, cwd=d)
    (d / "plans").mkdir()
    for rel, blob in receipts.items():
        p = d / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(blob)
    if not evidence: shutil.rmtree(d / "corpus", ignore_errors=True); (d / "README").write_text("x")
    for script, body in script_body_by_script.items():
        (d / script).write_text(body)
    sh("git", "add", "-A", cwd=d); sh("git", "commit", "-qm", "f", cwd=d)
    return d / "sub" if subdir else d
def script(name, out, exit_code=0):
    return f'"""probe\n\n  python3 plans/{name} --lane .\n"""\nimport sys\nsys.stdout.buffer.write({out!r})\nsys.exit({exit_code})\n'
cases = {}
G = "corpus/evidence/round35/tb2-grader-probe.txt"; GS = "plans/tb2_grader_probe.py"
cases["W1-T01-die-exit0|lane-not-toplevel"] = (lambda: (mk("l1", {G: b"hello\n"}, {GS: script("tb2_grader_probe.py", b"hello\n")}) / "plans"), ["--lane"], (76, "SystemExit(2) -> 0"), None)
cases["W2-L210|no-evidence-dir"] = (lambda: mk("l2", {}, {GS: script("tb2_grader_probe.py", b"x")}, evidence=False), ["--lane"], (210, "if-test -> False"), None)
cases["W3-L280|probe-exit-3"] = (lambda: mk("l3", {G: b"hello\n"}, {GS: script("tb2_grader_probe.py", b"hello\n", 3)}), ["--lane"], (280, "if-test -> False"), None)
RF = "corpus/evidence/round36/regex-log-probe-first-run.txt"; RS = "plans/regex_log_probe.py"
cases["W5-L285|temp-paths-masked-equal"] = (lambda: mk("l5", {RF: b"path=/tmp/tmpAAAAAAAA ok\n"}, {RS: script("regex_log_probe.py", b"path=/tmp/tmpBBBBBBBB ok\n")}), ["--lane"], (285, "== -> !="), None)
cases["W6-L302|unknown-tamper"] = (lambda: mk("l6", {G: b"hello\n"}, {GS: script("tb2_grader_probe.py", b"hello\n")}), ["--lane"], (302, "if-test -> False"), ["--tamper", "corpus/evidence/nope.txt"])
cases["W7-L347|empty-receipt-control-unavailable"] = (lambda: mk("l7", {G: b""}, {GS: script("tb2_grader_probe.py", b"")}), ["--lane"], (347, "and -> or"), None)
def run(tool, lane, extra, w):
    r = sh("python3", str(tool), "--lane", str(lane), "--work", str(w), *(extra or []))
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1][:120] if (r.stdout + r.stderr).strip() else ""
for name, (build, _a, (line, desc), extra) in cases.items():
    lane = build(); w = S / "w"; w.mkdir(exist_ok=True)
    if name.startswith("W1"): lane = lane  # subdir of the repo: not a toplevel
    ref = run(TOOL, lane, extra, w)
    m = pick(line, desc); mf = S / f"mut_{name[:2]}.py"; mf.write_bytes(src[:m["a"]] + m["new"].encode() + src[m["b"]:])
    mt = run(mf, lane, extra, w)
    print(f"{name:46s} ref rc={ref[0]} [{ref[1]}]  mut rc={mt[0]} [{mt[1]}]  {'DIFFER' if ref != mt else 'same'}")
