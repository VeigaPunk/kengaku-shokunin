#!/usr/bin/env python3
"""R45LabratReadProof: classify every successful open* in the C1 counter's kept strace logs.

The counter's own rule (plans/round45_c1_verify.py:run_fence) counts a successful open only when the
resolved destination lies under scratch (root/fx, root/btmp) and NOT under the fixture d. This tool
re-derives that rule independently and then widens it: every successful open is resolved (dirfd + cwd=d)
and bucketed, so a scratch-outside open is named, and every system open the fence makes is listed rather
than silently dropped.

usage: analyze_opens.py <strace-dir> <fixture-subdir> <log-name> [<subdir> <log> ...]
"""
import collections
import pathlib
import re
import sys

OPEN_RE = re.compile(r"\bopen(?:at|at2)?\(|creat\(")
RESUMED_RE = re.compile(r"^\s*(\d+)\s*<\.\.\.\s+\w+\s+resumed>")
UNFINISHED_RE = re.compile(r"(<unfinished \.\.\.>|=\s*\?)\s*$")
CALL_RE = re.compile(r"(\w+)\((.*)\)\s*=\s*(-?\d+|E[A-Z]+)(?:<(.+)>)?")


def split_args(call):
    out, buf, q, esc = [], "", False, False
    for ch in call:
        if esc:
            buf += ch
            esc = False
        elif ch == "\\" and q:
            buf += ch
            esc = True
        elif ch == '"':
            buf += ch
            q = not q
        elif ch == "," and not q:
            out.append(buf)
            buf = ""
        else:
            buf += ch
    out.append(buf)
    return out


def opened_target(line):
    m = CALL_RE.search(line)
    if not m:
        return None
    call, args, ret = m.group(1), m.group(2), m.group(3)
    ok = not (ret.startswith("E") or ret.startswith("-"))
    parts = split_args(args)
    if call in ("open", "creat"):
        dirfd, raw = "AT_FDCWD", parts[0].strip()
    elif call in ("openat", "openat2"):
        dirfd, raw = parts[0].strip(), parts[1].strip()
    else:
        return None
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        raw = raw[1:-1]
    return ok, raw, dirfd


def resolve(raw, dirfd, d):
    if not raw:
        return None
    if raw.startswith("/"):
        return pathlib.Path(raw)
    if "AT_FDCWD" in dirfd:
        return d / raw
    if dirfd.endswith(">") and "<" in dirfd:
        return pathlib.Path(dirfd.split("<", 1)[1][:-1]) / raw
    return None


def classify(p, d, scratch, root):
    if p is None:
        return "UNRESOLVED"
    if p == d or p.is_relative_to(d):
        return "inside-d"
    if any(p == s or p.is_relative_to(s) for s in scratch):
        return "SCRATCH-OUTSIDE"
    if p == root or p.is_relative_to(root):
        return "root-other"
    return "system-or-elsewhere"


def main():
    sd = pathlib.Path(sys.argv[1])
    pairs = list(zip(sys.argv[2::2], sys.argv[3::2]))
    totals = collections.Counter()
    for sub, logname in pairs:
        text = (sd / logname).read_text(errors="replace")
        mroot = re.search(r"(/[^\s\"<,]+)/fx/" + re.escape(sub) + r"/f000", text)
        if not mroot:
            print(f"== {sub}: cannot derive root from {logname}")
            continue
        root = pathlib.Path(mroot.group(1)).resolve()
        d = (root / "fx" / sub / "f000").resolve()
        scratch = (root / "fx", root / "btmp")
        cnt = collections.Counter()
        cited = []
        pending = []
        for line in text.splitlines():
            if not OPEN_RE.search(line):
                continue
            tgt = None if RESUMED_RE.search(line) else opened_target(line)
            if UNFINISHED_RE.search(line):
                pending.append(line)
                continue
            if tgt is None:
                continue
            ok, raw, dirfd = tgt
            if not ok:
                continue
            p = resolve(raw, dirfd, d)
            kind = classify(p, d, scratch, root)
            cnt[kind] += 1
            totals[kind] += 1
            if kind in ("SCRATCH-OUTSIDE", "UNRESOLVED", "root-other") and len(cited) < 15:
                cited.append(f"{logname}: {line.strip()[:200]}")
        print(f"== {sub} log={logname} d={d}")
        for k, v in sorted(cnt.items()):
            print(f"   {k}: {v}")
        for c in cited:
            print(f"   CITED {c}")
        if pending:
            print(f"   pending/unfinished open lines: {len(pending)}")
    print("== totals")
    for k, v in sorted(totals.items()):
        print(f"   {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
