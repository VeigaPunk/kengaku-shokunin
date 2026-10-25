#!/usr/bin/env python3
"""Strict audit of production-source reads and production executions per seat transcript.

Sources: assistant toolCall blocks AND custom tool_execution_start records (the latter are written at
call start, before the assistant message is flushed). Deduplicates by toolCallId. Prints per seat:
source-read calls, first production execution, first write/edit of the seat's own files. Positive
control: the critic's own transcript must show its own sed read of the production file.
Usage: strict_audit_v3.py DIR [name-substring ...]
"""
import json, os, re, sys
D = sys.argv[1]; keep = sys.argv[2:]
reader = re.compile(r"\b(cat|head|tail|sed|awk|grep|rg|nl|less|more|xxd|od|strings|diff|cmp)\b[^|;&\n]*config_projection\.py")
pyopen = re.compile(r"open\([^)]*config_projection|config_projection\.py['\"]?\)?\.read_text|import\s+config_projection|spec_from_file_location")
execr = re.compile(r"config_projection\.py['\"]?\s*,?\s*(['\"]?--root['\"]?\s*,?\s*\S+\s*,?\s*)?['\"]?--(json|summary|selftest)")
for f in sorted(os.listdir(D)):
    if not f.endswith('.jsonl') or (keep and not any(k in f for k in keep)):
        continue
    calls = {}
    for l in open(os.path.join(D, f), errors='replace'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('type') == 'custom' and r.get('customType') == 'tool_execution_start':
            d = r.get('data') or {}
            calls.setdefault(d.get('toolCallId'), (d.get('startedAt') or r.get('timestamp'), d.get('toolName'), d.get('args') or {}))
        m = r.get('message')
        if isinstance(m, dict):
            for p in m.get('content') or []:
                if isinstance(p, dict) and p.get('type') == 'toolCall':
                    calls.setdefault(p.get('id'), (r.get('timestamp'), p.get('name'), p.get('arguments') or {}))
    reads, first_exec, first_write = [], None, None
    for ts, name, a in sorted(calls.values(), key=lambda x: x[0] or ''):
        pth = str(a.get('path', '')); s = str(a.get('command') or a.get('code') or '')
        if name in ('write', 'edit') and first_write is None and 'falsify' in json.dumps(a):
            first_write = (ts, pth or str(a.get('input', ''))[:80])
        if name in ('read', 'grep', 'ast_grep') and 'config_projection.py' in pth:
            reads.append((ts, name, pth))
        elif 'config_projection.py' in s and (reader.search(s) or pyopen.search(s)):
            reads.append((ts, name, s[:200].replace('\n', ' | ')))
        if first_exec is None and execr.search(s):
            first_exec = ts
    print('%s calls=%d source_reads=%d first_prod_exec=%s first_own_write=%s' % (f, len(calls), len(reads), first_exec, first_write))
    for x in reads: print('    ', x)
