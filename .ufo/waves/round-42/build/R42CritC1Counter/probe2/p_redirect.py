"""Attack probe: the redirect key redirects the tool onto a repository outside the fixture dir.

The decoy repo d/repo contains only the decoy paths the argv names and a clean claims history;
the scenario (a claims blob committed after the receipt) lives in a host repo the module names by
absolute path. `path_ok` checks the argv tokens against d and passes.
"""
CL = "plans/round-42-claims.md"
CD = ".ufo/waves/round-42/claims"
HOST = "/fast/scratch/hyaku/kengaku-r42/R42CritC1Counter/host5"


def cm(ctx, r, msg):
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", msg)


def f_redirect(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / CL, "# frozen claims for the decoy\n")
    ctx.write(r / CD / "note.txt", "nothing executed here\n")
    cm(ctx, r, "decoy freeze")
    ctx.write(r / "corpus/evidence/probe.txt", "probe receipt body\n")
    cm(ctx, r, "decoy receipt")
    ctx.git(r, "config", "co" + "re.worktree", HOST)
    return ["--lane", str(r), "--claims", CL, "--receipt", "corpus/evidence/probe.txt"]


FIXTURES = [
    {"fid": "p-redirect-host-repo", "tool": "order", "expect": "accept", "defects": [],
     "build": f_redirect},
]
