#!/usr/bin/env python3
"""Round-41 C2 probe: the pinned Terminal-Bench 2.0 `constraints-scheduling` grader, executed offline.

  python3 plans/constraints_probe.py --lane .                run every frozen case, print the receipt
  python3 plans/constraints_probe.py --lane . --dry          print the frozen case table only (no sandbox)
  python3 plans/constraints_probe.py --lane . --stage-check  build every case's end state in the sandbox and
                                                             print only the stage exit codes; the grader is
                                                             never imported

What runs: the captured grader `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88, digest checked before any
case) inside a bubblewrap sandbox per case: private network/pid/ipc namespaces, /usr and /etc read-only, /tmp
private, /app a fresh writable directory, /cap holding only the captures the probe executes (test_outputs.py,
solve.sh), cwd /app, HOME=/tmp. Per case the probe first seeds /app as the task Dockerfile does (`COPY inputs/
/app/`: the three captured calendars), then writes the case's own files and edits on the host side, the sandbox
runs the case recipe under `bash -euo pipefail` (only the oracle case has a non-empty recipe: the task's
solve.sh), then imports the grader and calls its three test functions in file order: an AssertionError is
`F`, any other exception is `F` with its class named, a return is `P`. A case's verdict is `pass` iff all three
are `P` (pytest exits 0 iff no test fails; tests/test.sh writes reward 1 iff pytest exits 0). A recipe that
exits non-zero is a probe error (exit 2), never a verdict. The grader is bound at /cap/test_outputs.py, so its
`Path(__file__).resolve().parent.parent / "inputs"` is /inputs, which does not exist: the integrity check
takes the sha256 branch, as in the task image (tests at /tests, no /inputs).

Re-run stability (considerthese/2026-10-26.md proposal 3, carried from round 40): after the first grading the
harness grades the SAME end state a second time, without rebuilding it; the CASE line carries `regrade=same`
or `regrade=DIFF:<letters>`. The second grading is reported, never used for the verdict.

Ground truth (from the three captured calendars by hand, not from the grader; all times UTC): hard window for
a 1-hour slot is start >= 10:00 (Bob), end <= 14:00 (Alice), no overlap with 12:00-12:30 (Carol's lunch).
Busy: Alice Mon 10-11 13-14, Tue 10-12, Wed 10-11 13-14, Thu 10-11, Fri 10-11 13-14; Bob Mon 11-12 13-15, Tue
13-14, Wed 12-13, Thu 13-14, Fri 12-13; Carol Mon 11-12, Tue 11-12 13-14, Wed 12-13, Thu 12-13, Fri 11-12. Valid
starts: Wed 2024-01-17 11:00 and Thu 2024-01-18 11:00 only; the earliest is Wed 11:00.

Predictions: written before the first recorded run of this probe. The first 16 cases are the round-40 planning
seat's pilot (`.ufo/waves/round-40/build/R40PlanNext/cs/cases.py`, graded on this host before this freeze,
`cs/run1.txt`): their predictions are carried VERBATIM, including the two the pilot observed wrong
(`later-valid-wed-1105`, `seconds-30`: predicted fail set E, pilot observed C,E), and the pilot's id
`oracle-solve.sh` is renamed `oracle-solve-sh` (ids are `[a-z0-9-]+`). The last 9 cases were never graded
before the freeze.

Each case names the instruction requirements it violates (`violates=` tags, see TAGS), frozen with the
predictions; the entry's requirement map is derived from them and from the observed verdicts (round-38 Q28).
An empty `violates=` on a failing case is a grader stricter than the instruction (or than RFC 5545 where the
instruction says "valid ICS format"); on a passing case with tags it is a requirement the grader does not see.

Limits, stated before the first run: host python3 stands in for the image's Ubuntu 24.04 python3 (test.sh runs
pytest under `uvx -p 3.13`, which needs the network); the task image is never pulled; recipes run as the
probing user, not root. This is a probe of the grader on constructed end states, not of any agent.

Deterministic receipt: no temp path, timing or host version is printed. Scratch lives under --work (created if
absent), else $TMPDIR (tempfile default), and is removed on exit.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round41/tb2-constraints-scheduling"
PINS = {
    "alice_calendar.ics": "5a5d45804bffd339c2479d49e76fe817b38244d14d389afe1de583443808ecbc",
    "bob_calendar.ics": "c97e85dbcdd756758f8a80f4db5fd5c1dcacee79298e4d2262f46de5ff680b50",
    "carol_calendar.ics": "32a0f8687637df0a12b8e5c56d49c4192bc3e790856943632d70f237c7c1363b",
    "solve.sh": "802d81ec064fad3050bbade95a2f847ac24e0b7f80fa69b0bcee0347dc92fe77",
    "test_outputs.py": "1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1",
}
INPUTS = ("alice_calendar.ics", "bob_calendar.ics", "carol_calendar.ics")
BWRAP = "/usr/bin/bwrap"
TOOLS = ("/usr/bin/python3", "/usr/bin/bash")
TESTS = ("test_structure_event_title_attendees_duration_window", "test_constraints_conflicts_business_hours",
         "test_earliest_tiebreakers_and_carol_buffer")
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# tag -> the instruction line that states the requirement (instruction.md as captured)
TAGS = {
    "window": "instruction.md:1",
    "output-file": "instruction.md:10",
    "meeting-title": "instruction.md:10",
    "attendees": "instruction.md:10",
    "one-hour": "instruction.md:10",
    "hard-constraints": "instruction.md:12",
    "no-conflict": "instruction.md:12",
    "inputs-readonly": "instruction.md:15",
    "version-prodid": "instruction.md:23",
    "utc-format": "instruction.md:25",
    "earliest": "instruction.md:27",
}

HDR = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//probe//EN\n"
WHO = ("alice", "bob", "carol")


def ev(s, e, summary="Team Planning Meeting", att=WHO):
    a = "".join(f"ATTENDEE;CN={x}:mailto:{x}@example.com\n" for x in att)
    return f"BEGIN:VEVENT\nDTSTART:{s}\nDTEND:{e}\nSUMMARY:{summary}\n{a}END:VEVENT\n"


def ics(*evs, hdr=HDR):
    return hdr + "".join(evs) + "END:VCALENDAR\n"


GOOD = ("20240117T110000Z", "20240117T120000Z")
GOOD_ICS = ics(ev(*GOOD))
TZID_ICS = (HDR + "BEGIN:VEVENT\nDTSTART;TZID=UTC:20240117T110000\nDTEND;TZID=UTC:20240117T120000\n"
            "SUMMARY:Team Planning Meeting\nATTENDEE:mailto:alice@example.com\nATTENDEE:mailto:bob@example.com\n"
            "ATTENDEE:mailto:carol@example.com\nEND:VEVENT\nEND:VCALENDAR\n")
FOLDED_ICS = GOOD_ICS.replace("ATTENDEE;CN=carol:mailto:carol@example.com\n",
                              "ATTENDEE;CN=carol:mailto:carol@exam\n ple.com\n")
VALUE_ICS = GOOD_ICS.replace("DTSTART:", "DTSTART;VALUE=DATE-TIME:").replace("DTEND:", "DTEND;VALUE=DATE-TIME:")
LOWER_ICS = (HDR + "BEGIN:VEVENT\nDTSTART:20240117T110000Z\nDTEND:20240117T120000Z\n"
             "summary:Team Planning Meeting\n"
             + "".join(f"attendee;cn={x}:mailto:{x}@example.com\n" for x in WHO) + "END:VEVENT\nEND:VCALENDAR\n")


@dataclasses.dataclass(frozen=True)
class Case:
    cid: str
    predicted: str          # letters for TESTS in file order: S, C, E
    violates: tuple
    requirement: str
    meeting: str | None = None   # content of /app/meeting_scheduled.ics, None = not written
    edit: str = ""               # host-side edit of the seeded inputs
    recipe: str = ""             # bash run inside the sandbox before grading


ORACLE = "bash /cap/solve.sh >/dev/null 2>&1\n"
CASES = [
    # --- the round-40 pilot's 16 cases, predictions carried verbatim (graded on this host before the freeze)
    Case("nop", "FFF", ("output-file",), "no output file: all three tests read it (pilot)"),
    Case("oracle-solve-sh", "PPP", (), "the task's own solution/solve.sh (pilot `oracle-solve.sh`)", recipe=ORACLE),
    Case("literal-correct-slot", "PPP", (), "hand-typed ICS for Wed 11:00, never reads the calendars (pilot)",
         meeting=GOOD_ICS),
    Case("later-valid-wed-1105", "PPF", ("earliest", "no-conflict"),
         "Wed 11:05-12:05, predicted valid but late; pilot observed C,E (runs into lunch and Bob/Carol 12:00)",
         meeting=ics(ev("20240117T110500Z", "20240117T120500Z"))),
    Case("later-valid-thu-1100", "PPF", ("earliest",), "Thu 11:00, valid but a day late (pilot)",
         meeting=ics(ev("20240118T110000Z", "20240118T120000Z"))),
    Case("conflict-mon-1230", "PFF", ("no-conflict", "earliest"), "Mon 12:30, overlaps Alice's 13:00 event (pilot)",
         meeting=ics(ev("20240115T123000Z", "20240115T133000Z"))),
    Case("bob-start-0900-wed", "PFP", ("hard-constraints", "earliest"),
         "Wed 09:00, before Bob's 10:00; the earliest test passes because no valid slot precedes it (pilot)",
         meeting=ics(ev("20240117T090000Z", "20240117T100000Z"))),
    Case("decoy-first-vevent", "PPP", ("hard-constraints", "earliest"),
         "first VEVENT a decoy at Wed 11:00, the attendee meeting at Fri 15:00 (pilot; TB2.1 PR #245)",
         meeting=ics(ev(*GOOD, summary="decoy", att=()), ev("20240119T150000Z", "20240119T160000Z"))),
    Case("duration-90min", "FPP", ("one-hour",), "Wed 11:00-12:30; DTEND is read only by the structure test (pilot)",
         meeting=ics(ev("20240117T110000Z", "20240117T123000Z"))),
    Case("missing-carol", "FPP", ("attendees",), "Wed 11:00 without Carol's ATTENDEE (pilot)",
         meeting=ics(ev(*GOOD, att=("alice", "bob")))),
    Case("title-wrong", "FPP", ("meeting-title",), "Wed 11:00 titled 'Team Meeting' (pilot)",
         meeting=ics(ev(*GOOD, summary="Team Meeting"))),
    Case("seconds-30", "PPF", ("hard-constraints", "no-conflict", "earliest"),
         "Wed 11:00:30; predicted earliest-only, pilot observed C,E (end 12:00:30 runs into lunch)",
         meeting=ics(ev("20240117T110030Z", "20240117T120030Z"))),
    Case("tzid-form", "FFF", ("utc-format",), "DTSTART;TZID=UTC without Z: every timestamp regex misses (pilot)",
         meeting=TZID_ICS),
    Case("weekend-sat-20", "FFF", ("window", "hard-constraints", "earliest"), "Sat 2024-01-20 11:00 (pilot)",
         meeting=ics(ev("20240120T110000Z", "20240120T120000Z"))),
    Case("input-appended", "FPP", ("inputs-readonly",), "one newline appended to alice_calendar.ics, slot right (pilot)",
         meeting=GOOD_ICS, edit="alice-append"),
    Case("input-event-deleted-wed-1000", "FPP", ("inputs-readonly", "no-conflict", "earliest"),
         "Alice's Wed 10:00 event deleted, meeting booked Wed 10:00 (pilot)",
         meeting=ics(ev("20240117T100000Z", "20240117T110000Z")), edit="alice-delete-wed-1000"),
    # --- 9 cases new at this freeze, never graded before it
    Case("wed-1059-overlaps-alice", "PFP", ("no-conflict", "earliest"),
         "Wed 10:59, one minute before the earliest valid slot, overlaps Alice's 10:00-11:00 event",
         meeting=ics(ev("20240117T105900Z", "20240117T115900Z"))),
    Case("crlf-line-endings", "PPP", (), "the right slot written with CRLF line ends (RFC 5545's own line break)",
         meeting=GOOD_ICS.replace("\n", "\r\n")),
    Case("folded-attendee-line", "FPP", (), "the right slot with Carol's ATTENDEE line folded (RFC 5545 3.1)",
         meeting=FOLDED_ICS),
    Case("dtstart-value-datetime", "FFF", (), "DTSTART;VALUE=DATE-TIME:...Z, an explicit RFC 5545 value parameter",
         meeting=VALUE_ICS),
    Case("no-prodid-header", "FPP", ("version-prodid",), "the right slot, PRODID header left out",
         meeting=ics(ev(*GOOD), hdr="BEGIN:VCALENDAR\nVERSION:2.0\n")),
    Case("decoy-second-vevent", "PFF", ("hard-constraints", "earliest"),
         "attendee meeting first at Fri 15:00, a decoy second at Wed 11:00 (the pilot decoy's mirror)",
         meeting=ics(ev("20240119T150000Z", "20240119T160000Z"), ev(*GOOD, summary="decoy", att=()))),
    Case("extra-attendee-dave", "PPP", (), "the right slot with a fourth attendee",
         meeting=ics(ev(*GOOD, att=WHO + ("dave",)))),
    Case("lowercase-property-names", "FPP", (), "the right slot with lowercase SUMMARY/ATTENDEE names (RFC 5545 2.1)",
         meeting=LOWER_ICS),
    Case("input-crlf-rewrite", "PPP", ("inputs-readonly",),
         "all three input calendars rewritten with CRLF line ends, the right slot booked",
         meeting=GOOD_ICS, edit="inputs-crlf"),
]

HARNESS_PY = r'''
import importlib.util, subprocess, sys
mode = sys.argv[1]
rc = subprocess.run(["bash", "-euo", "pipefail", "/recipe.sh"], cwd="/app", stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
print("STAGE recipe rc=" + str(rc))
if rc or mode == "stage":
    sys.exit(3 if rc else 0)
spec = importlib.util.spec_from_file_location("tb2_constraints_grader", "/cap/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for tag in ("TEST", "REGRADE"):
    for name in %r:
        try:
            getattr(mod, name)()
            print(tag + " " + name + " P")
        except AssertionError:
            print(tag + " " + name + " F")
        except Exception as e:
            print(tag + " " + name + " F error=" + type(e).__name__)
''' % (TESTS,)


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def apply_edit(app, edit):
    if not edit:
        return
    if edit == "alice-append":
        with open(app / "alice_calendar.ics", "a") as fh:
            fh.write("\n")
    elif edit == "alice-delete-wed-1000":
        p = app / "alice_calendar.ics"
        t = p.read_text()
        p.write_text(re.sub(r"BEGIN:VEVENT(?:(?!END:VEVENT).)*?DTSTART:20240117T100000Z.*?END:VEVENT\n?", "", t,
                            flags=re.S))
    elif edit == "inputs-crlf":
        for name in INPUTS:
            p = app / name
            p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    else:
        raise ValueError(f"unknown edit {edit}")


def sandbox_argv(cap, work):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--bind", str(work / "app"), "/app", "--dir", "/cap"]
    for name in ("test_outputs.py", "solve.sh"):
        argv += ["--ro-bind", str(cap / name), f"/cap/{name}"]
    argv += ["--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
             "--ro-bind", str(work / "harness.py"), "/harness.py", "--chdir", "/app"]
    return argv


def run_case(cap, root, case, mode):
    work = pathlib.Path(tempfile.mkdtemp(prefix="csp-", dir=root))
    try:
        app = work / "app"
        app.mkdir()
        for name in INPUTS:
            shutil.copyfile(cap / name, app / name)
        apply_edit(app, case.edit)
        if case.meeting is not None:
            (app / "meeting_scheduled.ics").write_bytes(case.meeting.encode())
        (work / "recipe.sh").write_text(case.recipe or ":\n")
        (work / "harness.py").write_text(HARNESS_PY)
        env = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
               "PYTHONDONTWRITEBYTECODE": "1"}
        p = subprocess.run(sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py", mode],
                           env=env, capture_output=True, text=True, timeout=300)
        return p.returncode, p.stdout
    finally:
        shutil.rmtree(work, ignore_errors=True)


def overall(letters):
    return "pass" if letters == "P" * len(TESTS) else "fail"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    mx = ap.add_mutually_exclusive_group()
    mx.add_argument("--dry", action="store_true")
    mx.add_argument("--stage-check", action="store_true")
    ap.add_argument("--work", default=None, help="scratch parent, created if absent (default: $TMPDIR)")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    cap = lane / CAP
    ids = [c.cid for c in CASES]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r"[a-z0-9-]+", i) for i in ids) \
            or any(t not in TAGS for c in CASES for t in c.violates) \
            or any(len(c.predicted) != len(TESTS) or set(c.predicted) - {"P", "F"} for c in CASES):
        print("SETUP duplicate or malformed case id, unknown tag or malformed prediction", file=sys.stderr)
        return 2
    if a.dry:
        for t, loc in TAGS.items():
            print(f"TAG {t} {loc}")
        for c in CASES:
            print(f"CASE {c.cid} predicted={overall(c.predicted)} tests={c.predicted}"
                  f" violates={','.join(c.violates)} -- {c.requirement}")
        print(f"cases={len(CASES)} predicted_pass={sum(overall(c.predicted) == 'pass' for c in CASES)}"
              f" predicted_fail={sum(overall(c.predicted) == 'fail' for c in CASES)}")
        return 0
    for name, digest in PINS.items():
        if not (cap / name).is_file() or sha256(cap / name) != digest:
            print(f"SETUP capture {name} missing or not at its pinned digest", file=sys.stderr)
            return 2
    for tool in (BWRAP,) + TOOLS:
        if not os.access(tool, os.X_OK):
            print(f"SETUP {tool} is required", file=sys.stderr)
            return 2
    if a.work:
        try:
            pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"SETUP --work {a.work} cannot be created: {e.strerror}", file=sys.stderr)
            return 2
    root = pathlib.Path(tempfile.mkdtemp(prefix="k41-csp-", dir=a.work))
    try:
        if a.stage_check:
            bad = 0
            for c in CASES:
                rc, out = run_case(cap, root, c, "stage")
                stages = " ".join(l.split(" ", 1)[1] for l in out.splitlines() if l.startswith("STAGE "))
                bad += rc != 0
                print(f"STAGECHECK {c.cid} rc={rc} {stages}")
            print(f"stagecheck cases={len(CASES)} failed={bad}")
            return 0 if bad == 0 else 1
        print("# tb2 constraints-scheduling grader probe (kengaku round 41) @ terminal-bench-2 2fd12b88")
        for name in sorted(PINS):
            print(f"# capture {name} sha256={PINS[name]}")
        npass = nfail = mism = rediff = 0
        for c in CASES:
            rc, out = run_case(cap, root, c, "grade")
            got, again = {}, {}
            for l in out.splitlines():
                parts = l.split()
                if len(parts) >= 3 and parts[0] in ("TEST", "REGRADE") and parts[1] in TESTS:
                    (got if parts[0] == "TEST" else again)[parts[1]] = (parts[2], parts[3] if len(parts) > 3 else "")
            if rc != 0 or set(got) != set(TESTS) or set(again) != set(TESTS):
                print(f"SETUP case {c.cid} did not yield three test verdicts twice (rc={rc})", file=sys.stderr)
                print(out, file=sys.stderr)
                return 2
            letters = "".join(got[t][0] for t in TESTS)
            letters2 = "".join(again[t][0] for t in TESTS)
            errs = ",".join(f"{t}:{got[t][1]}" for t in TESTS if got[t][1])
            obs = overall(letters)
            npass += obs == "pass"
            nfail += obs == "fail"
            match = letters == c.predicted
            mism += not match
            rediff += letters2 != letters
            print(f"CASE {c.cid} predicted={overall(c.predicted)} observed={obs} tests={letters}"
                  f" predicted_tests={c.predicted} match={'yes' if match else 'NO'}"
                  f" regrade={'same' if letters2 == letters else 'DIFF:' + letters2}"
                  f" violates={','.join(c.violates)}{' ' + errs if errs else ''} -- {c.requirement}")
        print(f"regrade cases={len(CASES)} differ={rediff}")
        print(f"cases={len(CASES)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
