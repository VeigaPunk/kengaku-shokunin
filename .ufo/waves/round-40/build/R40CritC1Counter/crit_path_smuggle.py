"""Critic probe: `path_ok` resolves absolute argv tokens but never relative ones, so a fixture can name a
directory outside its own tree with a one-word relative token and the fingerprint hashes only the symlink."""
import pathlib


def link(ctx, d):
    shared = d.parent / "shared"
    ctx.clone(shared)
    (d / "lane").symlink_to("../shared")
    return ["--lane", "lane"]


def absolute(ctx, d):
    shared = d.parent / "shared"
    ctx.clone(shared)
    (d / "lane").symlink_to("../shared")
    return ["--lane", str(d / "lane")]


FIXTURES = [{"fid": "crit-path-relative", "tool": "anchor", "expect": "accept", "defects": [], "build": link}]
