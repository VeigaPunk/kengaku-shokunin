#!/usr/bin/env python3
"""R45LabratReadProof: scan every kept C1 strace log.

Independent re-derivation of the counter's opens rule (scratch = <root>/fx, <root>/btmp; an open counts
when it is inside scratch and outside the fixture d) plus a wider classification: every successful open is
resolved (decoded dirfd, else cwd) and bucketed. d is taken from the log itself: the decoded AT_FDCWD
(which is the harness cwd = d), never from a filename.

usage: scan_all.py <strace-dir> [--verbose-kind KIND]
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


def buckets(p, d, scratch, root):
    if p is None:
        return "UNRESOLVED"
    if p == d or p.is_relative_to(d):
        return "inside-d"
    if any(p == s or p.is_relative_to(s) for s in scratch):
        return "SCRATCH-OUTSIDE"
    if p == root or p.is_relative_to(root):
        return "root-other"
    if p.is_relative_to("/usr") or p.is_relative_to("/etc") or p.is_relative_to("/lib") \
            or p.is_relative_to("/lib64") or p.is_relative_to("/proc") or p.is_relative_to("/sys") \
            or p.is_relative_to("/dev") or p.is_relative_to("/run"):
        return "system"
    return "elsewhere"


def main():
    sd = pathlib.Path(sys.argv[1])
    logs = sorted(sd.glob("f*.txt"))
    totals = collections.Counter()
    offenders = []
    unresolved = []
    elsewhere = collections.Counter()
    per_log = {}
    for log in logs:
        text = log.read_text(errors="replace")
        mroot = re.search(r"(/[^\s\"<,]+)/fx/", text)
        mcwd = re.search(r"AT_FDCWD<([^>]+)>", text)
        if not mroot or not mcwd:
            unresolved.append(f"{log.name}: no root/cwd in log")
            continue
        root = pathlib.Path(mroot.group(1)).resolve()
        d = pathlib.Path(mcwd.group(1)).resolve()
        scratch = (root / "fx", root / "btmp")
        cnt = collections.Counter()
        pend = 0
        for line in text.splitlines():
            if not OPEN_RE.search(line):
                continue
            if RESUMED_RE.search(line):
                continue
            if UNFINISHED_RE.search(line):
                pend += 1
                raw_paths = re.findall(r'"(/[^"]+)"', line)
                for rp in raw_paths:
                    k = buckets(pathlib.Path(rp), d, scratch, root)
                    if k == "SCRATCH-OUTSIDE":
                        offenders.append(f"{log.name} PENDING {line.strip()[:200]}")
                continue
            tgt = opened_target(line)
            if tgt is None:
                continue
            ok, raw, dirfd = tgt
            if not ok:
                continue
            p = resolve(raw, dirfd, d)
            k = buckets(p, d, scratch, root)
            cnt[k] += 1
            totals[k] += 1
            if k == "SCRATCH-OUTSIDE":
                offenders.append(f"{log.name} rel={raw} target={p}")
            elif k == "UNRESOLVED":
                unresolved.append(f"{log.name} dirfd={dirfd!r} raw={raw!r}")
            elif k == "elsewhere":
                elsewhere[str(p.parent)] += 1
        per_log[log.name] = (d, cnt, pend)
    print(f"logs={len(logs)} with-d={len(per_log)}")
    print("== totals across all logs")
    for k, v in sorted(totals.items()):
        print(f"   {k}: {v}")
    print(f"== scratch-outside offenders: {len(offenders)}")
    for o in offenders[:20]:
        print(f"   {o}")
    print(f"== unresolved relative/dirfd opens: {len(unresolved)}")
    for u in unresolved[:20]:
        print(f"   {u}")
    print("== 'elsewhere' parents (non /usr,/etc,/proc,...), top 12")
    for p, n in elsewhere.most_common(12):
        print(f"   {p}: {n}")
    print("== per-log delta: logs where inside-d == 0")
    for name, (d, cnt, pend) in per_log.items():
        if cnt["inside-d"] == 0:
            print(f"   {name} d={d} buckets={dict(cnt)} pending={pend}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
