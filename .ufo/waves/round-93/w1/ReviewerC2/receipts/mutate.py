import pathlib, subprocess, sys, time
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r93/ReviewerC2")
src = (S/"zgate_T.py").read_text()
COUNTER = S/"zcounter_T.py"
L = S/"lane"; T = "22972a317185216596b3dfe1c189e98d1eb86787"
MUT = {
 "M1-no-touched-check": ('        if touched:\n            reasons.append', '        if False:\n            reasons.append'),
 "M2-no-rev-bytes-check": ('        elif sha(at_t) != want:', '        elif False:'),
 "M3-touched-unscoped": ('log = git(root, "rev-list", f"{f}..{t}", "--", p)', 'log = git(root, "rev-list", f"{f}..{t}")'),
 "M4-battery-skipped": ('        bat = battery(bat_dir)', '        bat = []'),
 "M5-table-read-at-rev": ('        text = blob(root, f, claims)', '        text = blob(root, t, claims)'),
 "M6-no-freeze-bytes-check": ('        if at_f is None or sha(at_f) != want:', '        if at_f is None:'),
 "M7-no-ancestor-check": ('    if git(root, "merge-base", "--is-ancestor", f, t).returncode != 0:', '    if False:'),
 "M8-full-history-touched": ('log = git(root, "rev-list", f"{f}..{t}", "--", p)', 'log = git(root, "rev-list", "--full-history", f"{f}..{t}", "--", p)'),
}
out = []
for name, (old, new) in MUT.items():
    n = src.count(old)
    assert n == 1, (name, n)
    m = S/"mut"/f"{name}.py"; m.parent.mkdir(exist_ok=True); m.write_text(src.replace(old, new))
    t0 = time.time()
    p = subprocess.run([sys.executable, "-I", "-B", str(COUNTER), "--lane", str(L), "--rev", T,
                        "--work", str(S/"mut"/f"work-{name}"), "--tool-file", str(m)],
                       capture_output=True, text=True, timeout=3000)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith(("W1 ","W2 ","W3 ","W4 ","TARGET","PREDICATE"))]
    out.append(f"== {name}: rc={p.returncode} secs={time.time()-t0:.0f}")
    out += ["   " + ln for ln in lines if not ln.startswith("W4 INSTRUMENT")]
    if p.stderr.strip(): out.append("   stderr: " + p.stderr.strip()[-300:])
print("\n".join(out))
