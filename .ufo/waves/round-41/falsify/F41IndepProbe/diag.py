#!/usr/bin/env python3
"""F41IndepProbe: independent build+inspect of the five non-frozen §Corrections end states.

Does NOT import or reuse plans/constraints_probe.py. Builds each /app itself, then inside a bwrap
sandbox prints, for every file the frozen grader reads: raw sha256, sha256 of read_text().encode(),
and the byte census of CRLF / lone-CR / LF. This is the causal chain behind each verdict.
"""
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

CAP = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round41/"
                   "tb2-constraints-scheduling")
INPUTS = ("alice_calendar.ics", "bob_calendar.ics", "carol_calendar.ics")
PINS = {
    "alice_calendar.ics": "5a5d45804bffd339c2479d49e76fe817b38244d14d389afe1de583443808ecbc",
    "bob_calendar.ics": "c97e85dbcdd756758f8a80f4db5fd5c1dcacee79298e4d2262f46de5ff680b50",
    "carol_calendar.ics": "32a0f8687637df0a12b8e5c56d49c4192bc3e790856943632d70f237c7c1363b",
}
BWRAP = "/usr/bin/bwrap"
PATHENV = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

HDR = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//probe//EN\n"
ATT = "".join(f"ATTENDEE;CN={x}:mailto:{x}@example.com\n" for x in ("alice", "bob", "carol"))
GOOD_ICS = HDR + ("BEGIN:VEVENT\nDTSTART:20240117T110000Z\nDTEND:20240117T120000Z\n"
                  "SUMMARY:Team Planning Meeting\n" + ATT + "END:VEVENT\nEND:VCALENDAR\n")
CRLF = GOOD_ICS.replace("\n", "\r\n")
STATES = {
    "crlf-folded": CRLF.replace("ATTENDEE;CN=carol:mailto:carol@example.com\r\n",
                                "ATTENDEE;CN=carol:mailto:carol@exam\r\n ple.com\r\n"),
    "crlf-lowercase-summary": CRLF.replace("SUMMARY:Team Planning Meeting\r\n",
                                           "summary:Team Planning Meeting\r\n"),
    "crlf-value-datetime": CRLF.replace("DTSTART:", "DTSTART;VALUE=DATE-TIME:").replace(
        "DTEND:", "DTEND;VALUE=DATE-TIME:"),
    "lowercase-attendee-only": GOOD_ICS.replace("ATTENDEE;CN=", "attendee;cn="),
    "cr-only-meeting-file": GOOD_ICS.replace("\n", "\r"),
}
EDIT = {"input-cr-only": "cr"}

HARNESS = r'''
import hashlib, re
from pathlib import Path
PINS = __PINS__
for p in sorted(Path("/app").iterdir()):
    d = p.read_bytes()
    t = p.read_text()
    ts = hashlib.sha256(t.encode()).hexdigest()
    print("FILE %s raw_sha=%s text_sha=%s crlf=%d lonecr=%d lone_lf=%d pins_match=%s" % (
        p.name, hashlib.sha256(d).hexdigest()[:16], ts[:16], d.count(b"\r\n"),
        d.count(b"\r") - d.count(b"\r\n"), d.count(b"\n") - d.count(b"\r\n"),
        PINS.get(p.name) == ts if p.name in PINS else "-"))
m = Path("/app/meeting_scheduled.ics")
if m.exists():
    t = m.read_text()
    dt = re.search(r"DTSTART:(\d{8}T\d{6}Z)", t)
    print("MEETING summary_literal=%s all_emails=%s value_param=%s folded_cont=%s dtstart_literal=%s" % (
        "SUMMARY:Team Planning Meeting" in t,
        all(e in t for e in ("alice@example.com", "bob@example.com", "carol@example.com")),
        "VALUE=DATE-TIME" in t,
        "\n ple.com" in t,
        dt.group(1) if dt else None))
'''.replace('__PINS__', repr(PINS))


def argv(work):
    a = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
         "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            a += ["--symlink", os.readlink(link), link]
    a += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
          "--bind", str(work / "app"), "/app", "--ro-bind", str(work / "h.py"), "/h.py", "--chdir", "/app"]
    return a


def main():
    root = pathlib.Path(tempfile.mkdtemp(prefix="diag-"))
    try:
        (root / "h.py").write_text(HARNESS)
        for name, body in STATES.items():
            app = root / name / "app"
            app.mkdir(parents=True)
            (root / name / "h.py").write_text(HARNESS)
            for f in INPUTS:
                shutil.copyfile(CAP / f, app / f)
            (app / "meeting_scheduled.ics").write_bytes(body.encode())
            p = subprocess.run(argv(root / name) + ["/usr/bin/python3", "/h.py"],
                               env={"PATH": PATHENV, "HOME": "/tmp", "LANG": "C.UTF-8",
                                    "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1"},
                               capture_output=True, text=True, timeout=120)
            print(f"== STATE {name} rc={p.returncode}")
            print(p.stdout.rstrip())
            if p.stderr:
                print("STDERR " + p.stderr.strip()[:300])
        # the input-edit state: cr-only inputs, right slot booked
        app = root / "input-cr-only" / "app"
        app.mkdir(parents=True)
        (root / "input-cr-only" / "h.py").write_text(HARNESS)
        for f in INPUTS:
            d = (CAP / f).read_bytes()
            (app / f).write_bytes(d.replace(b"\r\n", b"\n").replace(b"\n", b"\r"))
        (app / "meeting_scheduled.ics").write_bytes(GOOD_ICS.encode())
        p = subprocess.run(argv(root / "input-cr-only") + ["/usr/bin/python3", "/h.py"],
                           env={"PATH": PATHENV, "HOME": "/tmp", "LANG": "C.UTF-8",
                                "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1"},
                           capture_output=True, text=True, timeout=120)
        print(f"== STATE input-cr-only rc={p.returncode}")
        print(p.stdout.rstrip())
        if p.stderr:
            print("STDERR " + p.stderr.strip()[:300])
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
