#!/usr/bin/env python3
"""Read-only audit of omp session transcripts: list tool calls whose arguments mention a pattern.

Prints only tool name, timestamp and the matching argument keys truncated to 200 chars; never
prints tool results, environment values or message bodies.
Usage: toolcall_audit.py PATTERN FILE...
"""
import json
import re
import sys

pat = re.compile(sys.argv[1])
for path in sys.argv[2:]:
    hits = 0
    calls = 0
    first_ts = last_ts = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            ts = rec.get("timestamp")
            if ts:
                first_ts = first_ts or ts
                last_ts = ts
            msg = rec.get("message") or {}
            content = msg.get("content") if isinstance(msg, dict) else None
            if not isinstance(content, list):
                continue
            for part in content:
                if not isinstance(part, dict) or part.get("type") not in ("toolCall", "tool_use"):
                    continue
                calls += 1
                args = part.get("arguments") or part.get("input") or {}
                name = part.get("name")
                shown = {}
                for k, v in (args.items() if isinstance(args, dict) else []):
                    s = v if isinstance(v, str) else json.dumps(v)
                    if k in ("content", "contents"):
                        if pat.search(s):
                            m = pat.search(s)
                            shown[k] = "...%s..." % s[max(0, m.start() - 80):m.end() + 80].replace("\n", "\\n")
                        continue
                    if pat.search(s):
                        shown[k] = s[:300].replace("\n", "\\n")
                    elif k in ("path", "file_path"):
                        shown[k] = s[:200]
                if any(pat.search(json.dumps(v)) for v in shown.values()):
                    hits += 1
                    print("%s | %s | %s | %s" % (path.rsplit("/", 1)[-1], ts, name, json.dumps(shown)[:700]))
    print("SUMMARY %s tool_calls=%d matching=%d first=%s last=%s" % (path.rsplit("/", 1)[-1], calls, hits, first_ts, last_ts))
