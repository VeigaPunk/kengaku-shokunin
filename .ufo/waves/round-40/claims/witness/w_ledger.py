"""Pre-freeze direction witnesses (round 40, L1): L21 stale pin ref, L11 existing clone dir. Not battery40."""


def stale_master(ctx, d):
    lane = ctx.clone(d / "lane")
    ctx.git(lane, "checkout", "-q", "--detach")
    ctx.git(lane, "branch", "-f", "master", "HEAD~6")
    return ["--lane", str(lane)]


def work_exists(ctx, d):
    src = ctx.clone(d / "src")
    return ["--source", str(src), "--work", "{WORK:lane}"]


def tip_source(ctx, d):
    src = ctx.clone(d / "src")
    return ["--source", str(src), "--work", "{WORK}"]


FIXTURES = [
    {"fid": "w-l21-control-stale-master", "tool": "ledger", "expect": "error", "defects": [], "build": stale_master},
    {"fid": "w-l11-work-exists", "tool": "ledger", "expect": "error", "defects": [], "build": work_exists},
    {"fid": "w-ledger-tip-source", "tool": "ledger", "expect": "accept", "defects": [], "build": tip_source},
]
