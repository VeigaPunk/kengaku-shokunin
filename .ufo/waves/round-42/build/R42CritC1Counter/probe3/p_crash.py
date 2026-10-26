"""Attack probes for round42_c1_verify.py (config-exec, symlink, crash).

Each fixture is a self-contained repo (or non-repo) built with ctx only. The host-sources file
is a plain file outside every fixture directory, created by the attacking seat before the run.
"""
import hashlib

HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
CL = "plans/round-42-claims.md"
CD = ".ufo/waves/round-42/claims"
HOSTROWS = "/fast/scratch/hyaku/kengaku-r42/R42CritC1Counter/host-sources.md"


def dh(b):
    if isinstance(b, str):
        b = b.encode()
    return hashlib.sha256(b).hexdigest()


def row(sid, source, tok):
    return (f"| {sid} | {source} | code | A | fixture | sha256 {tok} | note | mined | "
            "2026-10-26 | 180d | corpus/knowledge/x.md |")


def cm(ctx, r, msg="fixture"):
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", msg)


def f_crash_reject(ctx, d):
    """No git repository at all: the tool exits 2 before printing any class."""
    lane = d / "lane"
    ctx.write(lane / "corpus/SOURCES.md", HDR + row("S921", "capture somewhere", dh(b"x\n")) + "\n")
    return ["--lane", str(lane)]


FIXTURES = [
    {"fid": "p-crash-only", "tool": "anchor", "expect": "reject", "defects": [],
     "build": f_crash_reject},
]
