"""Sealed50 hostile: a live (non-sample) hook file in the store.

Witnesses the hook-name leg (`_hooks`): a fence that accepts any regular file under `hooks/` admits a hook a
plain `git init` never writes.
"""
import os
import stat


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    hook = r / ".git/hooks/pre-commit"
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text("#!/bin/sh\nexit 0\n")
    os.chmod(hook, 0o755)
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-04-live-hook", "tool": "anchor", "expect": "error", "defects": [], "build": build}]
