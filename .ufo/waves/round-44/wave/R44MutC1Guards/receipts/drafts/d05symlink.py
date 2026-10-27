"""Draft control `d5symlink` (seat R44MutC1Guards) — symlink_breach (round-43 leg h) red control.

A fixture repo whose working tree holds a symlink resolving OUTSIDE d:
  pristine counter  -> `SETUP ... escapes its directory: symlink corpus/link-out -> ...` (exit 2)
  M05 counter (if p.is_symlink() ... -> if False:) -> the fixture is admitted (branch disabled).
"""
import hashlib
import os
import pathlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def build(ctx, d):
    body = b"capture read through nothing; the link itself is the probe\n"
    anchor = hashlib.sha256(body).hexdigest()
    r = ctx.init(d / "repo")
    ctx.write(r / "corpus/evidence/r1/cap.txt", body)
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + "| S910 | captured at corpus/evidence/r1/cap.txt | capture | A | fixture-scalar "
              f"| sha256 {anchor} | symlink breach draft | mined | 2026-10-26 | 180d | - |\n")
    os.symlink(str(pathlib.Path(d).parent / "outside-target.txt"), str(r / "corpus/link-out"))
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture with a symlink resolving outside the fixture dir")
    return ["--lane", str(r)]


FIXTURES = [{"fid": "d5-symlink-outside", "tool": "anchor", "expect": "accept", "defects": [], "build": build}]
