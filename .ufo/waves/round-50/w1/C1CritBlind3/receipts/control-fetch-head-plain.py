"""Scratch control (NOT a deliverable): the honest partner of the blind module `b2` — the same canonical
FETCH_HEAD bytes in `.git/FETCH_HEAD`, as an ordinary single-link file inside `d`. It isolates link identity as
the only difference between the honest and the hostile fixture, so the verdict matrix shows the discrimination
the sealed module demands of a repair."""


def build(ctx, d):
    lane = ctx.init(d / "lane")
    ctx.write(lane / "a.txt", "one\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "one")
    ctx.write(lane / "b.txt", "two\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "two")
    head = ctx.sh("git", "-C", str(lane), "rev-parse", "HEAD").stdout.strip()
    ctx.write(lane / ".git/FETCH_HEAD", f"{head}\t\tbranch 'master' of ../src\n")
    return ["--lane", "lane"]


FIXTURES = [{"fid": "ctl-fetch-head-plain", "tool": "anchor", "expect": "admit", "defects": [], "build": build}]
