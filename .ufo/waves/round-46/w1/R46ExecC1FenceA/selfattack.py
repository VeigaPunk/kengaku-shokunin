"""Self-audit fixtures for the variant-A allowlist fence (seat R46ExecC1FenceA). Each fixture is a plain repo
with exactly one non-plain shape; every one must be refused. Authored by this seat; no sealed module is read."""
import os
import pathlib

CLAIMS = "claims.md"
RECEIPT = "receipt.md"


def _repo(ctx, d, name="lane"):
    r = ctx.init(pathlib.Path(d) / name)
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return r


def _argv():
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def sa_info_commitgraph(ctx, d):
    r = _repo(ctx, d)
    ctx.write(r / ".git/objects/info/commit-graph", "CGPH")
    return _argv()


def sa_core_subsection(ctx, d):
    r = _repo(ctx, d)
    cfg = r / ".git/config"
    cfg.write_text(cfg.read_text() + '[core "x"]\n\tbare = false\n')
    return _argv()


def sa_symbolic_ref(ctx, d):
    r = _repo(ctx, d)
    ctx.write(r / ".git/refs/heads/side", "ref: refs/heads/master\n")
    return _argv()


def sa_head_escape(ctx, d):
    r = _repo(ctx, d)
    ctx.write(r / ".git/HEAD", "ref: ../../etc/passwd\n")
    return _argv()


def sa_packed_escape(ctx, d):
    r = _repo(ctx, d)
    head = (r / ".git/refs/heads/master").read_text().strip()
    ctx.write(r / ".git/packed-refs", f"{head} refs/heads/../../outside\n")
    return _argv()


def sa_index_symlink(ctx, d):
    r = _repo(ctx, d)
    outside = pathlib.Path(d).parent / "index-copy"
    ctx.write(outside, "outside index\n")
    (r / ".git/index").unlink()
    os.symlink(str(outside), r / ".git/index")
    return _argv()


def sa_hook_real(ctx, d):
    r = _repo(ctx, d)
    ctx.write(r / ".git/hooks/pre-commit", "#!/bin/sh\nexit 0\n")
    return _argv()


def sa_bare_truthy(ctx, d):
    r = _repo(ctx, d)
    ctx.write(r / ".git/config", "[core]\n\tbare = yes\n")
    return _argv()


def sa_nlink_worktree(ctx, d):
    r = _repo(ctx, d)
    outside = pathlib.Path(d).parent / "outside-claims"
    ctx.write(outside, "outside marker\n")
    (r / CLAIMS).unlink()
    os.link(outside, r / CLAIMS)
    return _argv()


def sa_dir_symlink_out(ctx, d):
    r = _repo(ctx, d)
    outside = pathlib.Path(d).parent / "outside-dir"
    outside.mkdir()
    os.symlink(str(outside), r / "linked")
    return _argv()


def sa_objects_direct_file(ctx, d):
    r = _repo(ctx, d)
    ctx.write(r / ".git/objects/notadirectory", "x\n")
    return _argv()


def sa_logs_escape_name(ctx, d):
    r = _repo(ctx, d)
    ctx.write(r / ".git/logs/refs/heads/../../outside", "x\n")
    return _argv()


FIXTURES = [
    {"fid": "sa-info-commitgraph", "tool": "order", "expect": "error", "defects": [], "build": sa_info_commitgraph},
    {"fid": "sa-core-subsection", "tool": "order", "expect": "error", "defects": [], "build": sa_core_subsection},
    {"fid": "sa-symbolic-ref", "tool": "order", "expect": "error", "defects": [], "build": sa_symbolic_ref},
    {"fid": "sa-head-escape", "tool": "order", "expect": "error", "defects": [], "build": sa_head_escape},
    {"fid": "sa-packed-escape", "tool": "order", "expect": "error", "defects": [], "build": sa_packed_escape},
    {"fid": "sa-index-symlink", "tool": "order", "expect": "error", "defects": [], "build": sa_index_symlink},
    {"fid": "sa-hook-real", "tool": "order", "expect": "error", "defects": [], "build": sa_hook_real},
    {"fid": "sa-bare-truthy", "tool": "order", "expect": "error", "defects": [], "build": sa_bare_truthy},
    {"fid": "sa-nlink-worktree", "tool": "order", "expect": "error", "defects": [], "build": sa_nlink_worktree},
    {"fid": "sa-dir-symlink-out", "tool": "order", "expect": "error", "defects": [], "build": sa_dir_symlink_out},
    {"fid": "sa-objects-direct-file", "tool": "order", "expect": "error", "defects": [],
     "build": sa_objects_direct_file},
    {"fid": "sa-logs-escape-name", "tool": "order", "expect": "error", "defects": [], "build": sa_logs_escape_name},
]
