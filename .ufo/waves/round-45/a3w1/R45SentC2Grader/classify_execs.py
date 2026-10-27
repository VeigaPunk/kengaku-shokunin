#!/usr/bin/env python3
"""Classify every execve in an strace -f trace of the round-45 C2 counter by environment width.

The frozen probe launches every sandbox with env=probe.ENV (6 vars), and each sandboxed process
inherits it, while host-side processes carry the caller's ~268-var environment. So the number of
environment variables recorded by strace separates "ran inside bwrap" from "ran on the host"
without needing a process tree (bwrap's children straddle a new PID namespace).
"""
import re
import sys
import collections

LINE = re.compile(r'(\d+)\s+[\d:.]+\s+execve\("([^"]+)", (\[[^\]]*\]), [^)\n]*?/\*\s*(\d+) vars\s*\*/')


def main(path):
    inside, outside = collections.Counter(), collections.Counter()
    tried = 0
    for line in open(path):
        m = LINE.search(line)
        if not m:
            continue
        if "= -1" in line:  # an execvp candidate that failed (ENOENT/EACCES) never ran
            tried += 1
            continue
        n = int(m.group(4))
        (inside if n <= 10 else outside)[m.group(2)] += 1
    print(f"# trace={path}")
    print(f"INSIDE bwrap (probe ENV, <=10 vars): {sum(inside.values())} execve")
    for p, n in inside.most_common():
        print(f"{n:5d}  {p}")
    print(f"OUTSIDE bwrap (host env, >10 vars): {sum(outside.values())} execve")
    print(f"# {tried} failed execvp candidates (ENOENT/EACCES) excluded in total")
    for p, n in outside.most_common():
        print(f"{n:5d}  {p}")


if __name__ == "__main__":
    main(sys.argv[1])
