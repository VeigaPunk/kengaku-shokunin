#!/usr/bin/env python3
"""Classify every tool call in omp transcripts that names plans/config_projection.py.

Classes: EXECUTE (python3 ... config_projection.py with --json/--summary/--selftest only),
SOURCE_READ (read/grep/glob tool on it, or a shell command that cats/greps/heads/seds/opens it),
OTHER. Prints counts per transcript plus each SOURCE_READ/OTHER call (timestamp, tool, 200 chars).
Also records the timestamp of the first EXECUTE and of the first write/edit of the seat's own files,
so commit-before-compare ordering can be checked. Never prints tool results.
Usage: source_read_audit.py FILE...
"""
import json
import re
import sys

TARGET = "config_projection.py"
EXEC = re.compile(r"python3?\s+\S*config_projection\.py(\s+--root\s+\S+)?\s+--(json|summary|selftest)\b")
READERS = re.compile(r"\b(cat|head|tail|sed|awk|grep|rg|less|more|nl|wc|diff|cmp|strings|od|xxd|open\(|read_text|import\s+config_projection|importlib|runpy|exec\()")

for path in sys.argv[1:]:
    counts = {"EXECUTE": 0, "SOURCE_READ": 0, "OTHER": 0}
    first_exec = None
    first_own_write = None
    lines = []
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        msg = rec.get("message")
        if not isinstance(msg, dict):
            continue
        for part in msg.get("content") or []:
            if not isinstance(part, dict) or part.get("type") != "toolCall":
                continue
            name = part.get("name")
            args = part.get("arguments") or {}
            ts = rec.get("timestamp")
            if name in ("write", "edit") and first_own_write is None:
                first_own_write = ts
            blob = json.dumps(args)
            if TARGET not in blob:
                continue
            if name in ("read", "grep", "glob", "ast_grep") and TARGET in str(args.get("path", "")):
                cls = "SOURCE_READ"
            elif name in ("bash", "eval"):
                cmd = str(args.get("command") or args.get("code") or "")
                stripped = EXEC.sub("", cmd)
                if TARGET in stripped and READERS.search(stripped):
                    cls = "SOURCE_READ"
                elif EXEC.search(cmd) and TARGET not in stripped:
                    cls = "EXECUTE"
                elif EXEC.search(cmd):
                    cls = "OTHER"
                else:
                    cls = "OTHER"
            elif name in ("write", "edit"):
                cls = "OTHER"
            else:
                cls = "OTHER"
            counts[cls] += 1
            if cls == "EXECUTE" and first_exec is None:
                first_exec = ts
            if cls != "EXECUTE":
                lines.append("  %s %s %s %s" % (cls, ts, name, blob[:220].replace("\\n", " ")))
    print("%s %s first_execute=%s first_write_or_edit=%s" % (path.rsplit("/", 1)[-1], json.dumps(counts), first_exec, first_own_write))
    for l in lines:
        print(l)
