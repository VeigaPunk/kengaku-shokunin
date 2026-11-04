#!/usr/bin/env python3
"""R82-C3 counter — sweep at one tip: which executed replays still reproduce?

Frozen before data on 2026-11-04 (L1 KengakuR82); see plans/round-82-claims.md §R82-C3 for the
predicate this implements. The predicate sentence, the projection and the refusal codes below are
the same ones the claims doc froze.

    python3 plans/round82_c3_sweep.py --lane . --check                # verdict over committed bytes
    python3 plans/round82_c3_sweep.py --lane . --run --work DIR       # the sweep (writes the receipt)
    python3 plans/round82_c3_sweep.py --lane . --verify-at-tip --work DIR
    python3 plans/round82_c3_sweep.py --selftest --work DIR           # fixture battery
    python3 plans/round82_c3_sweep.py --mutants --work DIR            # attributed receipt mutants
    python3 plans/round82_c3_sweep.py --control-ledger-copy --work DIR
    python3 plans/round82_c3_sweep.py --control-exit-only --work DIR
    python3 plans/round82_c3_sweep.py --control-fabricated-line --work DIR

Receipt shape (corpus/evidence/round82/sweep.txt):

    SWEEP_MAP <path> sha256=<hex>          LEDGER <path> sha256=<hex>
    LANE_TIP <rev>                          WORKTREE clean|dirty
    WORKDIR <abs path the sweep ran with>
    ENV python=<line> openssl=<line> bwrap=<line>
    MEMBER <name> status=<reproduced|diverged:<n>|unrunnable:<code>> exit=<n> secs=<s> argv=<argv>
    PROJECTION <name> lines=<n> sha256=<hex of the compared projection text>
    DIFF <name> <differing line>          (n of them for a diverged member, at most 3)
    HISTOGRAM status reproduced=<a> diverged=<b> unrunnable=<c> total=<n>
    HISTOGRAM-CLASS <class>=<n> … sum=<m>
    TARGET members=<n> located=<n> status_lines=<n> histogram_total=<n> mismatches=<n>
    PREDICATE R82-C3 pass|fail

Exit 0 pass, 1 fail (each defect on its own line), 2 setup.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MAP_REL = "plans/round82-sweep-map.json"
LEDGER_REL = "plans/grader-population-ledger.json"
RECEIPT_REL = "corpus/evidence/round82/sweep.txt"
BASE_REV = "a3a03ac31451e58f1742b9bccb73b72c2d90a95c"   # round-82 base (round-81 tip)
FORMS = re.compile(r"^(CASE |case=|TEST |VECTOR |LEG |regrade )")
DROP = re.compile(r"^cases=")
U_LINE = re.compile(r"(^OBSERVED-U )|(predicted=U)|(predicted=fail\?U)")
STATUS = re.compile(r"^(reproduced|diverged:(\d+)|unrunnable:([a-z0-9-]+))$")
MEMBER_LINE = re.compile(r"^MEMBER (\S+) status=(\S+) exit=(-?\d+) secs=([0-9.]+) argv=(.+)$")
PROJ_LINE = re.compile(r"^PROJECTION (\S+) lines=(\d+) sha256=([0-9a-f]{64})$")
DIFF_LINE = re.compile(r"^DIFF (\S+) (.*)$")
HIST_LINE = re.compile(r"^HISTOGRAM status reproduced=(\d+) diverged=(\d+) unrunnable=(\d+) total=(\d+)$")
HIST_CLASS = re.compile(r"^HISTOGRAM-CLASS (.*) sum=(\d+)$")
TARGET_LINE = re.compile(r"^TARGET members=(\d+) located=(\d+) status_lines=(\d+) histogram_total=(\d+) mismatches=(\d+)$")
EXIT_LINE = re.compile(r"^EXIT (\d+)$")
TIMEOUT_DEFAULT = 300


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else ""


def load_json(path: Path):
    try:
        return json.loads(read(path))
    except Exception:
        return None


def executed(ledger) -> dict:
    if not isinstance(ledger, dict):
        return {}
    m = ledger.get("members")
    if not isinstance(m, dict):
        return {}
    return {k: v for k, v in m.items() if isinstance(v, dict) and v.get("status") == "executed"}


def projection_of(text: str) -> list[str]:
    """The frozen projection: observation-form lines, minus the volatile ones (round-80 A2)."""
    out = []
    for line in text.split("\n"):
        s = line.rstrip("\r")
        if not FORMS.match(s):
            continue
        if DROP.match(s) or U_LINE.search(s):
            continue
        out.append(s)
    return out


def receipt_block(text: str) -> str:
    """OBSERVATIONS_BEGIN..END when the receipt marks it, else the whole receipt."""
    if "OBSERVATIONS_BEGIN" in text:
        body = text.split("OBSERVATIONS_BEGIN", 1)[1]
        return body.split("OBSERVATIONS_END", 1)[0]
    return text


def expected_exit(text: str) -> int:
    for line in text.split("\n"):
        m = EXIT_LINE.match(line.strip())
        if m:
            return int(m.group(1))
    return 0   # every committed receipt that carries no EXIT line is the output of a successful run


def map_argv(entry: dict, member: str, work: Path) -> list[str]:
    out = []
    for tok in entry["argv"]:
        out.append(tok.replace("<WORK>", str(work)).replace("<MEMBER>", member))
    return out


# ── check (committed bytes only) ────────────────────────────────────────────────────────────────
def check(lane: Path, receipt: Path | None = None, quiet: bool = False) -> int:
    defects: list[tuple[str, str]] = []
    rpath = receipt or (lane / RECEIPT_REL)
    mp = lane / MAP_REL
    lp = lane / LEDGER_REL
    if not mp.is_file():
        print("SETUP map absent: %s" % MAP_REL)
        return 2
    if not lp.is_file():
        print("SETUP ledger absent: %s" % LEDGER_REL)
        return 2
    if not rpath.is_file():
        print("SETUP receipt absent: %s" % rpath)
        return 2
    mdoc, ldoc, rtext = load_json(mp), load_json(lp), read(rpath)
    if not isinstance(mdoc, dict) or not isinstance(mdoc.get("members"), dict):
        print("SETUP map unreadable")
        return 2
    ex, led = executed(ldoc), {}
    mmap = mdoc["members"]
    led = executed(ldoc)
    lines = [l.rstrip() for l in rtext.split("\n")]
    members: dict[str, dict] = {}
    proj: dict[str, tuple[int, str]] = {}
    diffs: dict[str, list[str]] = {}
    hist = None
    hist_class = {}
    target = None
    predicate = None
    workdir = None
    for line in lines:
        m = MEMBER_LINE.match(line)
        if m:
            name = m.group(1)
            if name in members:
                defects.append(("MEMBER-DUPLICATE", name))
            members[name] = {"status": m.group(2), "exit": int(m.group(3)),
                             "secs": m.group(4), "argv": m.group(5)}
            continue
        m = PROJ_LINE.match(line)
        if m:
            proj[m.group(1)] = (int(m.group(2)), m.group(3))
            continue
        m = DIFF_LINE.match(line)
        if m:
            diffs.setdefault(m.group(1), []).append(m.group(2))
            continue
        m = HIST_LINE.match(line)
        if m:
            hist = tuple(int(x) for x in m.groups())
            continue
        m = HIST_CLASS.match(line)
        if m:
            pairs = re.findall(r"([A-Za-z0-9_.-]+)=(\d+)", m.group(1))
            hist_class[tuple((k, int(v)) for k, v in pairs)] = int(m.group(2))
            continue
        m = TARGET_LINE.match(line)
        if m:
            target = tuple(int(x) for x in m.groups())
            continue
        if line.startswith("PREDICATE R82-C3 "):
            predicate = line.split()[-1]
            continue
        if line.startswith("WORKDIR "):
            workdir = line.split(None, 1)[1].strip()

    want = set(led)
    got = set(members)
    for name in sorted(want - got):
        defects.append(("STATUS-LINE-MISSING", name))
    for name in sorted(got - want):
        defects.append(("MEMBER-EXTRA", name))
    for name in sorted(want & got):
        rec = members[name]
        if not STATUS.match(rec["status"]):
            defects.append(("STATUS-SHAPE", "%s %s" % (name, rec["status"])))
        entry = mmap.get(name)
        if not isinstance(entry, dict) or "argv" not in entry:
            defects.append(("LOCATOR-MISS", name))
            continue
        if not (lane / entry["instrument"]).is_file() and not (Path(entry["instrument"])).is_file():
            defects.append(("LOCATOR-MISS", "%s %s" % (name, entry["instrument"])))
        if workdir is None:
            defects.append(("WORKDIR-MISSING", name))
        else:
            expect = " ".join(map_argv(entry, name, Path(workdir) / name))
            if rec["argv"] != expect:
                defects.append(("COMMAND-MISMATCH", "%s receipt=%r map=%r" % (name, rec["argv"], expect)))
        if name not in proj:
            defects.append(("PROJECTION-UNCHECKED", name))
        st = rec["status"]
        if st.startswith("diverged:"):
            n = int(st.split(":", 1)[1])
            have = len(diffs.get(name, []))
            # the receipt stores at most the first three differing lines; the declared count is the
            # true number of differing projection lines.
            if not (1 <= have <= min(n, 3)):
                defects.append(("DIFF-COUNT", "%s declared=%d lines=%d" % (name, n, have)))
        elif st == "reproduced" and diffs.get(name):
            defects.append(("DIFF-ON-REPRODUCED", name))
        if st == "reproduced" and rec["exit"] != 0:
            defects.append(("EXIT-ON-REPRODUCED", "%s exit=%d" % (name, rec["exit"])))

    if hist is None:
        defects.append(("HISTOGRAM-MISSING", "-"))
    else:
        a, b, c, total = hist
        counts = {"reproduced": 0, "diverged": 0, "unrunnable": 0}
        for rec in members.values():
            st = rec["status"]
            if st == "reproduced":
                counts["reproduced"] += 1
            elif st.startswith("diverged:"):
                counts["diverged"] += 1
            elif st.startswith("unrunnable:"):
                counts["unrunnable"] += 1
        if (a, b, c) != (counts["reproduced"], counts["diverged"], counts["unrunnable"]):
            defects.append(("HISTOGRAM-COUNT", "declared=%s counted=%s" % ((a, b, c), tuple(counts.values()))))
        if total != len(members) or total != len(want):
            defects.append(("HISTOGRAM-SUM", "total=%d members=%d ledger=%d" % (total, len(members), len(want))))

    if not hist_class:
        defects.append(("HISTOGRAM-CLASS-MISSING", "-"))
    else:
        pairs, declared_sum = next(iter(hist_class.items()))
        want_sum = sum(len(v.get("classes", [])) for v in led.values())
        if declared_sum != want_sum:
            defects.append(("HISTOGRAM-CLASS-SUM", "declared=%d recomputed=%d" % (declared_sum, want_sum)))
        cl = dict(pairs)
        want_cl: dict[str, int] = {}
        for v in led.values():
            for c in v.get("classes", []):
                want_cl[c] = want_cl.get(c, 0) + 1
        for k in sorted(set(cl) | set(want_cl)):
            if cl.get(k, 0) != want_cl.get(k, 0):
                defects.append(("HISTOGRAM-CLASS", "%s declared=%s recomputed=%s" % (k, cl.get(k), want_cl.get(k))))
    if target is None:
        defects.append(("TARGET-MISSING", "-"))
    else:
        tm, tl, ts, th, tmis = target
        if (tm, tl, ts, th) != (len(want), len(want & got), len(members), (hist[3] if hist else -1)):
            defects.append(("TARGET-INCONSISTENT", "target=%s measured=(%d,%d,%d,%s)" % (
                target, len(want), len(want & got), len(members), hist[3] if hist else None)))
        if tmis != 0:
            defects.append(("TARGET-MISMATCH", str(tmis)))
    if predicate != "pass":
        defects.append(("PREDICATE", str(predicate)))
    # NO-RUN: a census whose statuses were copied from the ledger carries no exit evidence and no
    # projection hash; the two structural markers below are what a copy cannot produce.
    if not proj:
        defects.append(("NO-RUN", "no PROJECTION lines — the census was not measured"))
    if workdir is None:
        defects.append(("NO-RUN", "no WORKDIR line"))

    print("MEMBERS ledger=%d map=%d status_lines=%d" % (len(want), len(mmap), len(members)))
    if hist:
        print("HISTOGRAM status reproduced=%d diverged=%d unrunnable=%d total=%d" % hist)
    for code, detail in defects:
        print("DEFECT %s %s" % (code, detail))
    print("DEFECTS n=%d" % len(defects))
    print("TARGET members=%d located=%d status_lines=%d histogram_total=%d mismatches=%d" % (
        len(want), len(want & got), len(members), (hist[3] if hist else -1), len(defects)))
    ok = not defects
    print("PREDICATE R82-C3 %s" % ("pass" if ok else "fail"))
    return 0 if ok else 1


# ── run (the sweep) ─────────────────────────────────────────────────────────────────────────────
def run(lane: Path, work: Path, receipt: Path) -> int:
    mp = lane / MAP_REL
    lp = lane / LEDGER_REL
    mdoc, ldoc = load_json(mp), load_json(lp)
    if not isinstance(mdoc, dict) or not isinstance(mdoc.get("members"), dict):
        print("SETUP map unreadable")
        return 2
    led = executed(ldoc)
    mmap = mdoc["members"]
    dirty = git(lane, "status", "--porcelain")
    tip = git(lane, "rev-parse", "HEAD") or git(lane, "rev-parse", "master")
    body, hist_c, loc, stat = [], {}, 0, 0
    class_counts: dict[str, int] = {}
    for name in sorted(led):
        entry = mmap.get(name)
        if not isinstance(entry, dict):
            body.append("MEMBER %s status=unrunnable:locator-miss exit=2 secs=0 argv=-" % name)
            stat += 1
            continue
        inst = lane / entry["instrument"]
        if not inst.is_file():
            body.append("MEMBER %s status=unrunnable:instrument-absent exit=2 secs=0 argv=-" % name)
            stat += 1
            continue
        loc += 1
        wd = work / name
        wd.mkdir(parents=True, exist_ok=True)
        rcp = wd / ("%s.receipt.txt" % name)
        argv = map_argv(entry, name, wd)
        t0 = time.time()
        # A member that spawns bwrap children must be killed as a process GROUP: killing only the
        # direct child leaves the pipes open and communicate() blocks past the timeout (observed on
        # cancel-async-tasks in this round's first run).
        try:
            proc = subprocess.Popen(argv, cwd=str(lane), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, start_new_session=True,
                                    env={**os.environ, "TMPDIR": str(wd)})
            try:
                out, err = proc.communicate(timeout=entry.get("timeout", TIMEOUT_DEFAULT))
                rc = proc.returncode
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(os.getpgid(proc.pid), 9)
                except Exception:
                    proc.kill()
                out, err = proc.communicate()
                rc = 124
        except Exception as exc:   # noqa: BLE001 - a launch failure is an unrunnable member
            rc, out, err = 125, "", str(exc)
        secs = time.time() - t0
        rpath = lane / entry["receipt"]
        proj = projection_of(receipt_block(out))
        if not proj and rcp.is_file():
            # several instruments print nothing on stdout and write their report into --receipt;
            # the instrument's own receipt is then the observation source (still the instrument's
            # output, never the committed block it is compared against).
            proj = projection_of(receipt_block(read(rcp)))
        if rc == 124:
            status = "unrunnable:timeout"
        elif rc != 0:
            status = "unrunnable:exit-%d" % rc
        elif not rpath.is_file():
            status = "unrunnable:receipt-absent"
        elif not proj:
            status = "unrunnable:no-observations"
        else:
            want = projection_of(receipt_block(read(rpath)))
            diffs = [w for w in want if w not in proj]
            extra = [g for g in proj if g not in want]
            ndiff = len(diffs) + len(extra)
            if ndiff == 0 and expected_exit(read(rpath)) == rc:
                status = "reproduced"
            else:
                status = "diverged:%d" % ndiff
                for d in (diffs + extra)[:3]:
                    body.append("DIFF %s %s" % (name, d))
        body.append("MEMBER %s status=%s exit=%d secs=%.1f argv=%s" % (name, status, rc, secs, " ".join(argv)))
        body.append("PROJECTION %s lines=%d sha256=%s" % (name, len(proj), sha("\n".join(proj))))
        stat += 1
        key = status.split(":", 1)[0]
        hist_c[key] = hist_c.get(key, 0) + 1
        for cls in led[name].get("classes", ["unclassified"]):
            class_counts[cls] = class_counts.get(cls, 0) + 1
    env = {"python": subprocess.run([sys.executable, "-V"], capture_output=True, text=True).stdout.strip(),
           "openssl": subprocess.run(["openssl", "version"], capture_output=True, text=True).stdout.strip() or "absent",
           "bwrap": subprocess.run(["bwrap", "--version"], capture_output=True, text=True).stdout.strip() or "absent"}
    head = [
        "# kengaku round 82 — sweep at one tip (R82-C3)",
        "SWEEP_MAP %s sha256=%s" % (MAP_REL, sha(read(mp))),
        "LEDGER %s sha256=%s" % (LEDGER_REL, sha(read(lp))),
        "LANE_TIP %s" % tip,
        "WORKTREE %s" % ("clean" if not dirty else "dirty (%d paths)" % len(dirty.split("\n"))),
        "WORKDIR %s" % work,
        "ENV python=%s openssl=%s bwrap=%s" % (env["python"], env["openssl"], env["bwrap"]),
    ]
    total = len(led)
    hist_line = "HISTOGRAM status reproduced=%d diverged=%d unrunnable=%d total=%d" % (
        hist_c.get("reproduced", 0), hist_c.get("diverged", 0), hist_c.get("unrunnable", 0), total)
    class_line = "HISTOGRAM-CLASS " + " ".join("%s=%d" % (k, v) for k, v in sorted(class_counts.items())) + \
                 " sum=%d" % sum(class_counts.values())
    tail = [hist_line, class_line,
            "TARGET members=%d located=%d status_lines=%d histogram_total=%d mismatches=0" % (total, loc, stat, total),
            "PREDICATE R82-C3 pass"]
    # staged write: nothing lands until every member has a status line
    if stat != total:
        print("STAGED-WRITE aborted: %d/%d status lines" % (stat, total))
        return 1
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text("\n".join(head + body + tail) + "\n")
    print("\n".join(head + [hist_line, class_line, tail[-2], tail[-1]]))
    return 0


# ── verify at tip ──────────────────────────────────────────────────────────────────────────────
def verify_at_tip(lane: Path, work: Path) -> int:
    tip = git(lane, "rev-parse", "master") or git(lane, "rev-parse", "HEAD")
    clone = work / "tip-clone"
    if clone.exists():
        shutil.rmtree(clone)
    p = subprocess.run(["git", "clone", "--shared", "-q", str(lane), str(clone)], capture_output=True, text=True)
    if p.returncode != 0:
        print("SETUP clone failed: %s" % p.stderr.strip()[:200])
        return 2
    subprocess.run(["git", "-C", str(clone), "checkout", "-q", tip], capture_output=True, text=True)
    r = subprocess.run([sys.executable, str(clone / "plans" / "round82_c3_sweep.py"), "--selftest",
                        "--work", str(work / "selftest-at-tip")], capture_output=True, text=True)
    last = r.stdout.strip().split("\n")[-1] if r.stdout.strip() else "(no output)"
    print("VERIFY-AT-TIP rev=%s selftest_rc=%d %s" % (tip[:8], r.returncode, last))
    ok = r.returncode == 0 and "failures=0" in r.stdout
    print("VERIFY-AT-TIP %s" % ("pass" if ok else "fail"))
    return 0 if ok else 1


# ── fixtures ───────────────────────────────────────────────────────────────────────────────────
GREEN_MAP = {"schema": "r82-sweep-map/1", "members": {
    "m1": {"instrument": "plans/p1.py", "argv": ["python3", "plans/p1.py", "--lane", ".", "--work", "<WORK>"],
           "receipt": "corpus/evidence/fx/m1.txt"},
    "m2": {"instrument": "plans/p2.py", "argv": ["python3", "plans/p2.py", "--lane", ".", "--work", "<WORK>"],
           "receipt": "corpus/evidence/fx/m2.txt"},
}}
GREEN_LEDGER = {"members": {
    "m1": {"status": "executed", "classes": ["file-artifact"]},
    "m2": {"status": "executed", "classes": ["numeric-band"]},
    "m3": {"status": "unexecuted", "classes": ["file-artifact"]},
}}


def green_receipt(workdir="/w"):
    a1 = " ".join(["python3", "plans/p1.py", "--lane", ".", "--work", workdir + "/m1"])
    a2 = " ".join(["python3", "plans/p2.py", "--lane", ".", "--work", workdir + "/m2"])
    return "\n".join([
        "# fixture sweep",
        "SWEEP_MAP plans/round82-sweep-map.json sha256=" + "0" * 64,
        "LANE_TIP " + "1" * 40,
        "WORKTREE clean",
        "WORKDIR " + workdir,
        "ENV python=x openssl=x bwrap=x",
        "MEMBER m1 status=reproduced exit=0 secs=1.0 argv=" + a1,
        "PROJECTION m1 lines=3 sha256=" + sha("a\nb\nc"),
        "MEMBER m2 status=diverged:1 exit=0 secs=2.0 argv=" + a2,
        "PROJECTION m2 lines=2 sha256=" + sha("a\nb"),
        "DIFF m2 CASE k1 predicted=P observed=F",
        "HISTOGRAM status reproduced=1 diverged=1 unrunnable=0 total=2",
        "HISTOGRAM-CLASS file-artifact=1 numeric-band=1 sum=2",
        "TARGET members=2 located=2 status_lines=2 histogram_total=2 mismatches=0",
        "PREDICATE R82-C3 pass",
    ]) + "\n"


def fixture_tree(work: Path, receipt_text: str | None = None) -> Path:
    root = Path(tempfile.mkdtemp(dir=work))
    (root / "plans").mkdir(parents=True)
    (root / "corpus/evidence/round82").mkdir(parents=True)
    (root / "plans/round82-sweep-map.json").write_text(json.dumps(GREEN_MAP, indent=1))
    (root / "plans/grader-population-ledger.json").write_text(json.dumps(GREEN_LEDGER, indent=1))
    (root / "plans/p1.py").write_text("print('p1')\n")
    (root / "plans/p2.py").write_text("print('p2')\n")
    (root / "corpus/evidence/round82/sweep.txt").write_text(receipt_text if receipt_text is not None else green_receipt())
    return root


def selftest(work: Path) -> int:
    work.mkdir(parents=True, exist_ok=True)
    cases, reds, failures = 0, 0, 0

    def case(name: str, text: str | None, expect_rc: int):
        nonlocal cases, reds, failures
        root = fixture_tree(work, text)
        rc = check(root, quiet=True)
        cases += 1
        got_red = rc != 0
        if got_red:
            reds += 1
        if rc != expect_rc:
            failures += 1
            print("CASE %s FAIL want_rc=%d got_rc=%d" % (name, expect_rc, rc))
        else:
            print("CASE %s ok want_rc=%d got_rc=%d" % (name, expect_rc, rc))
        shutil.rmtree(root, ignore_errors=True)

    green = green_receipt()
    case("green", green, 0)
    case("missing-status-line", green.replace(next(l for l in green.split("\n") if l.startswith("MEMBER m2")), ""), 1)
    case("extra-member", green + "MEMBER m9 status=reproduced exit=0 secs=0.0 argv=x\n", 1)
    case("histogram-sum", green.replace("unrunnable=0 total=2", "unrunnable=1 total=3"), 1)
    case("histogram-count", green.replace("reproduced=1 diverged=1", "reproduced=2 diverged=0"), 1)
    case("command-mismatch", green.replace("--work /w/m1", "--work /other/m1"), 1)
    case("projection-unchecked", "\n".join(l for l in green.split("\n") if not l.startswith("PROJECTION ")) + "\n", 1)
    case("diff-count", green.replace("DIFF m2 CASE k1 predicted=P observed=F\n", ""), 1)
    case("diff-overflow", green + "DIFF m2 CASE extra\n", 1)
    case("no-run", "\n".join(l for l in green.split("\n")
                             if not l.startswith("PROJECTION ") and not l.startswith("DIFF ")) + "\n", 1)
    case("predicate-fail", green.replace("PREDICATE R82-C3 pass", "PREDICATE R82-C3 fail"), 1)
    case("target-inconsistent", green.replace("TARGET members=2 located=2", "TARGET members=3 located=3"), 1)
    print("SELFTEST cases=%d red=%d failures=%d" % (cases, reds, failures))
    return 0 if failures == 0 else 1


def mutants(work: Path) -> int:
    work.mkdir(parents=True, exist_ok=True)
    green = green_receipt()
    M = [
        ("drop-status-line", lambda t: "\n".join(l for l in t.split("\n") if not l.startswith("MEMBER m1")) + "\n"),
        ("duplicate-member", lambda t: t.replace("MEMBER m2", "MEMBER m1 status=reproduced exit=0 secs=1.0 argv=x\nMEMBER m2", 1)),
        ("zero-divergence", lambda t: t.replace("status=diverged:1", "status=diverged:0")),
        ("overflow-diffs", lambda t: t.replace("DIFF m2 CASE k1 predicted=P observed=F", "DIFF m2 a\nDIFF m2 b\nDIFF m2 c\nDIFF m2 d")),
        ("zero-out-diff", lambda t: t.replace("DIFF m2 CASE k1 predicted=P observed=F\n", "")),
        ("swap-argv", lambda t: t.replace("--work /w/m2", "--work /w/m3")),
        ("strip-projection", lambda t: "\n".join(l for l in t.split("\n") if not l.startswith("PROJECTION ")) + "\n"),
        ("bad-histogram", lambda t: t.replace("HISTOGRAM-CLASS file-artifact=1 numeric-band=1 sum=2",
                                              "HISTOGRAM-CLASS file-artifact=1 numeric-band=1 sum=3")),
        ("pass-on-fail", lambda t: t.replace("PREDICATE R82-C3 fail", "PREDICATE R82-C3 pass")
         if "fail" in t else t.replace("PREDICATE R82-C3 pass", "PREDICATE R82-C3 fail").replace("mismatches=0", "mismatches=1")),
        ("target-zero", lambda t: t.replace("mismatches=0", "mismatches=4")),
        ("status-shape", lambda t: t.replace("status=reproduced", "status=ok")),
    ]
    killed = survived = 0
    for name, f in M:
        text = f(green)
        if text == green:
            print("MUTANT %s invalid (no change)" % name)
            continue
        root = fixture_tree(work, text)
        rc = check(root, quiet=True)
        shutil.rmtree(root, ignore_errors=True)
        if rc != 0:
            killed += 1
            print("MUTANT %s killed" % name)
        else:
            survived += 1
            print("MUTANT %s SURVIVED" % name)
    print("MUTANTS real=%d killed=%d survived=%d" % (killed + survived, killed, survived))
    return 0 if survived == 0 else 1


def control_ledger_copy(work: Path) -> bool:
    root = fixture_tree(work)
    r = root / "corpus/evidence/round82/sweep.txt"
    r.write_text("\n".join([
        "# control: statuses copied from the ledger, nothing run",
        "WORKDIR /w",
        "MEMBER m1 status=reproduced exit=0 secs=0 argv=x",
        "MEMBER m2 status=reproduced exit=0 secs=0 argv=y",
        "HISTOGRAM status reproduced=2 diverged=0 unrunnable=0 total=2",
        "HISTOGRAM-CLASS file-artifact=1 numeric-band=1 sum=2",
        "TARGET members=2 located=2 status_lines=2 histogram_total=2 mismatches=0",
        "PREDICATE R82-C3 pass",
    ]) + "\n")
    rc = check(root, quiet=True)
    shutil.rmtree(root, ignore_errors=True)
    return rc != 0


def control_exit_only(work: Path) -> bool:
    text = "\n".join(l for l in green_receipt().split("\n") if not l.startswith("PROJECTION ")) + "\n"
    root = fixture_tree(work, text)
    rc = check(root, quiet=True)
    shutil.rmtree(root, ignore_errors=True)
    return rc != 0


def control_fabricated_line(work: Path) -> bool:
    """A receipt line whose observation the instrument does not emit: re-run one fixture instrument."""
    root = fixture_tree(work)
    inst = root / "plans" / "p1.py"
    inst.write_text("print('CASE k1 predicted=P observed=P')\n")
    out = subprocess.run([sys.executable, str(inst)], capture_output=True, text=True).stdout
    proj = projection_of(receipt_block(out))
    fabricated = projection_of("CASE k1 predicted=P observed=F\n")
    caught = proj != fabricated
    shutil.rmtree(root, ignore_errors=True)
    return caught


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="R82-C3 sweep-at-one-tip counter/runner")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--verify-at-tip", action="store_true")
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--control-ledger-copy", action="store_true")
    ap.add_argument("--control-exit-only", action="store_true")
    ap.add_argument("--control-fabricated-line", action="store_true")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    if a.selftest:
        if not a.work:
            print("SETUP --work required")
            return 2
        return selftest(Path(a.work))
    if a.mutants:
        if not a.work:
            print("SETUP --work required")
            return 2
        return mutants(Path(a.work))
    if a.control_ledger_copy:
        if not a.work:
            print("SETUP --work required")
            return 2
        ok = control_ledger_copy(Path(a.work))
        print("CONTROL ledger-copy caught=%s target_reached=%s" % (ok, "False" if ok else "True"))
        return 0 if ok else 1
    if a.control_exit_only:
        if not a.work:
            print("SETUP --work required")
            return 2
        ok = control_exit_only(Path(a.work))
        print("CONTROL exit-only caught=%s target_reached=%s" % (ok, "False" if ok else "True"))
        return 0 if ok else 1
    if a.control_fabricated_line:
        if not a.work:
            print("SETUP --work required")
            return 2
        ok = control_fabricated_line(Path(a.work))
        print("CONTROL fabricated-line caught=%s target_reached=%s" % (ok, "False" if ok else "True"))
        return 0 if ok else 1
    if a.run:
        if not a.work:
            print("SETUP --work required")
            return 2
        rcp = Path(a.receipt) if a.receipt else (lane / RECEIPT_REL)
        return run(lane, Path(a.work).resolve(), rcp)
    if a.verify_at_tip:
        if not a.work:
            print("SETUP --work required")
            return 2
        return verify_at_tip(lane, Path(a.work).resolve())
    if a.check or True:
        rcp = Path(a.receipt) if a.receipt else None
        return check(lane, rcp)


if __name__ == "__main__":
    sys.exit(main())
