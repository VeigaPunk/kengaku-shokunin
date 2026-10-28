"""the packed REF line (not the peel) names an object only present in an in-fixture outside store."""
import shutil
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ext = ctx.init(d / "ext")
    ctx.write(ext / "b.txt", "two\n")
    ctx.git(ext, "add", "-A")
    ctx.git(ext, "commit", "-q", "-m", "two")
    foreign = ctx.git(ext, "rev-parse", "HEAD").stdout.strip()
    obj = ext / ".git/objects" / foreign[:2] / foreign[2:]
    ctx.write(d / "outside-store/objects" / foreign[:2] / foreign[2:], obj.read_bytes())
    shutil.rmtree(ext)
    ctx.write(r / ".git/refs/heads/gone", foreign + "\n")
    if ctx.git(r, "cat-file", "-e", foreign, check=False).returncode == 0:
        raise RuntimeError("fixture defect")
    return ["--lane", "repo"]
FIXTURES = [{"fid": "p04-ref-target-outside", "tool": "anchor", "expect": "error", "defects": [], "build": build}]
