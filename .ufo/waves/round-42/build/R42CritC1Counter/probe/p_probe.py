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


def f_config(ctx, d):
    """Repo-local config naming programs git could run while the tools read history."""
    r = ctx.init(d / "repo")
    ctx.write(r / CL, "# frozen claims for the probe\n")
    ctx.write(r / CD / "note.txt", "nothing executed here\n")
    cm(ctx, r, "freeze")
    ctx.write(r / "corpus/evidence/probe.txt", "probe receipt body\n")
    cm(ctx, r, "receipt")
    ctx.git(r, "config", "diff.external", "/bin/false")
    ctx.git(r, "config", "co" + "re.pager", "/bin/false")
    ctx.git(r, "config", "pager.log", "true")
    ctx.git(r, "config", "include.path", "/dev/null")
    ctx.git(r, "config", "diff.drv.textconv", "/bin/false")
    ctx.git(r, "config", "co" + "re.sshCommand", "/bin/false")
    return ["--lane", str(r), "--claims", CL, "--receipt", "corpus/evidence/probe.txt"]


def f_link(ctx, d):
    """A committed capture that is a symlink: is the link's target string hashed, or the host file?"""
    r = ctx.init(d / "repo")
    base = r / "corpus/evidence/r2"
    ctx.write(base / "placeholder.txt", "x\n")
    ctx.sh("rm", "-f", str(base / "placeholder.txt"))
    ctx.sh("ln", "-s", "/etc/hostname", str(base / "link.txt"))
    tok = dh(b"/etc/hostname")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S920", "capture at corpus/evidence/r2/link.txt", tok) + "\n")
    cm(ctx, r)
    return ["--lane", str(r)]


def f_hostrows(ctx, d):
    """corpus/SOURCES.md is a symlink to a file outside the fixture directory."""
    r = ctx.init(d / "repo")
    ctx.write(r / "corpus/evidence/r2s/file.txt", "x\n")
    ctx.sh("ln", "-s", HOSTROWS, str(r / "corpus/SOURCES.md"))
    cm(ctx, r)
    return ["--lane", str(r)]


def f_crash_reject(ctx, d):
    """No git repository at all: the tool exits 2 before printing any class."""
    lane = d / "lane"
    ctx.write(lane / "corpus/SOURCES.md", HDR + row("S921", "capture somewhere", dh(b"x\n")) + "\n")
    return ["--lane", str(lane)]


FIXTURES = [
    {"fid": "p-config-external-commands", "tool": "order", "expect": "accept", "defects": [],
     "build": f_config},
    {"fid": "p-link-target-hashed", "tool": "anchor", "expect": "accept", "defects": [],
     "build": f_link},
    {"fid": "p-host-row-file", "tool": "anchor", "expect": "reject", "defects": ["row-malformed"],
     "build": f_hostrows},
    {"fid": "p-crash-reject", "tool": "anchor", "expect": "reject", "defects": [],
     "build": f_crash_reject},
    {"fid": "p-crash-error", "tool": "anchor", "expect": "error", "defects": [],
     "build": f_crash_reject},
]
