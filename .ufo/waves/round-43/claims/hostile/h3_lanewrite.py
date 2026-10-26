"""F42C1Hardened hostile module `h3_lanewrite` — repair R3 (R42SentinelCounter V3, V5).

Vector: the frozen `ro_sandbox` implements `hide` as `--tmpfs <path>` (round42_c1_verify.py:304-305), and a
tmpfs mount point is a *writable* empty directory at the hidden name. A build child can therefore plant
files at `<lane>/...` (measured by R42SentinelCounter: `laneW=WROTE`, host lane untouched), and any check
that tests the lane's existence instead of its contents is fooled.

Observable: the build child writes one file at the lane path and looks for the lane's counter, then puts both
facts in the fixture id:

  frozen counter  FIXTURE h3-lane-WROTE-hidden …     (write accepted at the lane's name, contents hidden: green)
  hardened copy   FIXTURE h3-lane-ERR30-hidden …     (empty read-only bind: EROFS 30: red)

"hidden" in both rows is the measured content state: with `--tmpfs` the lane's *name* stays a writable
directory while its contents vanish. The write lands in the sandbox only (the lane handed to this run is the
clone in this seat's scratch, never the lane under measurement; the clone's `git status` stays empty).
"""

import pathlib

LANE = "/fast/scratch/hyaku/kengaku-r43/L1/ctl/m-base"
M42 = ".ufo/waves/round-42/claims"
CLAIMS = "plans/round-42-claims.md"
PROBE = "corpus/evidence/round42/fibsqrt-probe.txt"
RECEIPT_BODY = "cases=16 observed_pass=7 observed_fail=9 mismatches=0\nregrade cases=16 differ=0\n"


def commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def clean_history(ctx, d):
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS, "# round 42 - frozen claims\n\nThe run is recorded after the freeze.\n")
    ctx.write(repo / M42 / "control.txt", "P10 DEFECT receipt unreadable\n")
    commit(ctx, repo, "freeze")
    ctx.write(repo / PROBE, RECEIPT_BODY)
    commit(ctx, repo, "first recorded run")
    return repo


def lane_state():
    lane = pathlib.Path(LANE)
    try:
        (lane / "k42probe-F42C1Hardened").write_text("written by the build child\n")
        wrote = "WROTE"
    except OSError as e:
        wrote = f"ERR{e.errno}"
    visible = "visible" if (lane / "plans" / "round42_c1_verify.py").is_file() else "hidden"
    return wrote, visible


def build(ctx, d):
    wrote, visible = lane_state()
    FIXTURES[0]["fid"] = f"h3-lane-{wrote}-{visible}"
    repo = clean_history(ctx, d)
    return ["--lane", str(repo), "--claims", CLAIMS, "--receipt", PROBE]


FIXTURES = [
    {"fid": "h3-lane-placeholder", "tool": "order", "expect": "accept", "defects": [], "build": build},
]
