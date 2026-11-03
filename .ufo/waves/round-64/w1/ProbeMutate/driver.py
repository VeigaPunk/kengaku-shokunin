#!/usr/bin/env python3
"""Mutation driver for the r64 ProbeMutate seat (source-agnostic).

Subcommands
-----------
apply  --src F --dst F --spec F
       Apply exact-string replacements from a JSON spec:
         [{"old": "...", "new": "...", "count": 1}, ...]
       Each replacement MUST match exactly `count` times; the result MUST
       differ from the source; the result MUST compile as Python.  Writes the
       mutant, a unified diff, and an apply-receipt to --receipt.

run    --label L --receipt F --cwd D -- CMD [ARG...]
       Run one detector command with a hard timeout, capture rc/stdout/stderr.

hash   F [F ...]

No network, no writes outside the paths given on the command line.
"""

import argparse
import difflib
import hashlib
import json
import pathlib
import subprocess
import sys
import time


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_apply(args):
    src = pathlib.Path(args.src)
    dst = pathlib.Path(args.dst)
    spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))
    before = sha256(src)
    text = src.read_text(encoding="utf-8")
    original = text
    applied = []
    for i, step in enumerate(spec):
        old, new = step["old"], step["new"]
        want = int(step.get("count", 1))
        got = text.count(old)
        if got != want:
            print(f"APPLY fail step={i} matches={got} want={want} old={old!r}")
            return 3
        text = text.replace(old, new, want)
        applied.append({"step": i, "matches": got, "old": old, "new": new})
    if text == original:
        print("APPLY fail no-byte-change (mutant identical to source)")
        return 3
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    after = sha256(dst)
    try:
        compile(text, str(dst), "exec")
        comp = "ok"
    except SyntaxError as exc:
        comp = f"SyntaxError: {exc}"
    diff = "".join(
        difflib.unified_diff(
            original.splitlines(keepends=True),
            text.splitlines(keepends=True),
            fromfile=str(src),
            tofile=str(dst),
            n=3,
        )
    )
    block = [
        "# apply receipt",
        f"ts={time.strftime('%Y-%m-%dT%H:%M:%S')}",
        f"src={src}",
        f"src_sha256={before}",
        f"dst={dst}",
        f"dst_sha256={after}",
        f"changed={before != after}",
        f"compile={comp}",
        f"steps={len(applied)}",
        "--- replacements ---",
    ]
    for step in applied:
        block.append(f"step={step['step']} matches={step['matches']} old={step['old']!r} new={step['new']!r}")
    block += ["--- diff ---", diff if diff else "(empty)"]
    out = "\n".join(block) + "\n"
    pathlib.Path(args.receipt).write_text(out, encoding="utf-8")
    print(out)
    return 0 if comp == "ok" else 4


def cmd_run(args):
    cmd = args.cmd
    started = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=args.cwd,
            capture_output=True,
            text=True,
            timeout=args.timeout,
        )
        rc, out, err, status = proc.returncode, proc.stdout, proc.stderr, "completed"
    except subprocess.TimeoutExpired as exc:
        rc = -9
        out = (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        err = (exc.stderr or b"").decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        status = f"timeout after {args.timeout}s"
    elapsed = time.time() - started
    block = [
        f"# detector run {args.label}",
        f"ts={time.strftime('%Y-%m-%dT%H:%M:%S')}",
        f"cwd={args.cwd}",
        f"cmd={' '.join(cmd)}",
        f"status={status}",
        f"rc={rc}",
        f"elapsed={elapsed:.2f}s",
        "--- stdout ---",
        out if out.strip() else "(empty)",
        "--- stderr ---",
        err if err.strip() else "(empty)",
    ]
    text = "\n".join(block) + "\n"
    pathlib.Path(args.receipt).write_text(text, encoding="utf-8")
    print(text)
    return 0


def cmd_hash(args):
    for f in args.files:
        print(f"{sha256(f)}  {f}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="sub", required=True)

    a = sub.add_parser("apply")
    a.add_argument("--src", required=True)
    a.add_argument("--dst", required=True)
    a.add_argument("--spec", required=True)
    a.add_argument("--receipt", required=True)

    r = sub.add_parser("run")
    r.add_argument("--label", required=True)
    r.add_argument("--receipt", required=True)
    r.add_argument("--cwd", required=True)
    r.add_argument("--timeout", type=int, default=300)
    r.add_argument("cmd", nargs=argparse.REMAINDER)

    h = sub.add_parser("hash")
    h.add_argument("files", nargs="+")

    args = ap.parse_args(argv)
    if args.sub == "apply":
        return cmd_apply(args)
    if args.sub == "run":
        # argparse.REMAINDER keeps a leading '--' separator; strip it.
        if args.cmd and args.cmd[0] == "--":
            args.cmd = args.cmd[1:]
        if not args.cmd:
            print("run: empty command", file=sys.stderr)
            return 2
        return cmd_run(args)
    if args.sub == "hash":
        return cmd_hash(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
