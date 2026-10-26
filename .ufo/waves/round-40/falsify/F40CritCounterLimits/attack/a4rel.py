"""a4rel — a relative argv token that leaves d through a symlink (wave-1 A4 / sentinel F4).

The fixture directory holds one symlink to a tree outside d; the tool runs with cwd=d, so the relative
token resolves there. Under the frozen counter this is accepted, `tampered=0`, and the tool reads a tree
the fingerprint does not cover.
"""
import pathlib

OUTSIDE = '/fast/scratch/hyaku/kengaku-r40/F40CritCounterLimits/outside'


def build(ctx, d):
    (d / "lane-link").symlink_to(OUTSIDE)
    return ["--lane", "lane-link"]


FIXTURES = [
    {"fid": "a4-relative-symlink", "tool": "anchor", "expect": "accept", "defects": [], "build": build},
]
