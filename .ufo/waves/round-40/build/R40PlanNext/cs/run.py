import subprocess, shutil, pathlib, sys, os
sys.path.insert(0, ".")
import cases
S = pathlib.Path(os.environ["CS_SCRATCH"]); T = pathlib.Path(os.environ["TB2"]) / "constraints-scheduling"
H = pathlib.Path(__file__).resolve().parent / "harness.py"
fails_all = 0; mism = 0; differ = 0; n = 0; po = pf = 0
print("# constraints-scheduling probe (R40PlanNext) @ terminal-bench-2 2fd12b88, host python", sys.version.split()[0])
for cid, c in cases.CASES.items():
    app = S / "app" / cid
    if app.exists(): shutil.rmtree(app)
    app.mkdir(parents=True)
    for f in (T / "environment/inputs").iterdir(): shutil.copy(f, app / f.name)
    pre = ":"
    f = c["file"]
    if f == "ORACLE": pre = "bash /solution/solve.sh >/dev/null 2>&1"
    elif f is None: pass
    elif f.startswith("MODIFY:"):
        k = f.split(":")[1]
        if k == "alice-append":
            with open(app / "alice_calendar.ics", "a") as fh: fh.write("\n")
        else:
            p = app / "alice_calendar.ics"; t = p.read_text()
            import re
            t = re.sub(r"BEGIN:VEVENT(?:(?!END:VEVENT).)*?DTSTART:20240117T100000Z.*?END:VEVENT\n?", "", t, flags=re.S); p.write_text(t)
        (app / "meeting_scheduled.ics").write_text(cases.ics(cases.ev("20240117T110000Z" if k == "alice-append" else "20240117T100000Z", "20240117T120000Z" if k == "alice-append" else "20240117T110000Z")))
    else: (app / "meeting_scheduled.ics").write_text(f)
    cmd = ["bwrap","--unshare-net","--unshare-pid","--ro-bind","/usr","/usr","--symlink","usr/bin","/bin","--symlink","usr/lib","/lib","--symlink","usr/lib","/lib64",
           "--ro-bind","/etc","/etc","--proc","/proc","--dev","/dev","--tmpfs","/tmp","--bind",str(app),"/app","--ro-bind",str(T/"tests"),"/tests",
           "--ro-bind",str(T/"solution"),"/solution","--ro-bind",str(H),"/h.py","--chdir","/app","bash","-c",f"{pre}\npython3 /h.py; echo ---; python3 /h.py"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    g1, g2 = r.stdout.split("---")
    def parse(g): return sorted(l.split()[1].replace("test_","") for l in g.splitlines() if l.startswith("T ") and l.split()[2] == "FAIL")
    a, b = parse(g1), parse(g2)
    ntests = sum(1 for l in g1.splitlines() if l.startswith("T "))
    short = {"structure_event_title_attendees_duration_window": "S", "constraints_conflicts_business_hours": "C", "earliest_tiebreakers_and_carol_buffer": "E"}
    obs = ",".join(sorted(short[x] for x in a)) or "-"; pred = ",".join(sorted(c["pred"].split(","))) if c["pred"] != "-" else "-"
    m = "YES" if obs == pred else "NO"
    n += 1; mism += m == "NO"; differ += a != b; po += obs == "-"; pf += obs != "-"
    print(f"{cid:32s} tests={ntests} fail={obs:6s} pred={pred:6s} match={m} regrade={'same' if a==b else 'DIFFER'}  # {c['note']}")
print(f"cases={n} observed_pass={po} observed_fail={pf} mismatches={mism} regrade_differ={differ}")
