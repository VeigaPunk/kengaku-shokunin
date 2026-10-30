#!/usr/bin/env python3
"""scan_extended.py - extended secret/injection/path screen for kengaku round 53 wave 3 seat R53SentinelFetch2.

Complements plans/stage_scan.py (fixed-shape credential patterns) with:
  * session/cookie shapes (Bearer, sessionid, JSESSIONID, aws session tokens, signed URLs)
  * absolute host paths that would dangle in a committed corpus
  * prompt-injection shapes (instructions addressed to an AI reading the file)

Usage:  python3 scan_extended.py PATH [PATH...]
Output: one line per hit: <class>\t<path>:<line>\t<rule>\t<snippet<=120ch, redacted-ish>
Exit 0 always (report is the artifact, not the exit code). Bytes of a matched
secret are NEVER printed in full: only the rule and a truncated, masked prefix.
"""
from __future__ import annotations

import os
import re
import sys

MAX_BYTES = 8 * 1024 * 1024
BIN_PROBE = 8 * 1024

# class -> list of (rule, compiled regex, redact?)
RULES: list[tuple[str, str, re.Pattern[str]]] = [
    ("credential", "bearer-header", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-]{16,}")),
    ("credential", "session-cookie", re.compile(r"(?i)\b(?:sessionid|jsessionid|phpsessid|sid|csrftoken|access_token)\s*[=:]\s*['\"]?[A-Za-z0-9._\-]{12,}")),
    ("credential", "signed-url-param", re.compile(r"(?i)[?&](?:X-Amz-Signature|X-Amz-Credential|sig|signature|access_token|token)=[A-Za-z0-9._%\-]{16,}")),
    ("credential", "cookie-header", re.compile(r"(?i)set-cookie:\s*[^\r\n]{12,}")),
    ("credential", "aws-session-token", re.compile(r"(?i)aws_session_token\s*[=:]\s*['\"]?[A-Za-z0-9/+=]{20,}")),
    ("credential", "private-key", re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----")),
    # 1Password reference scheme: assembled from fragments so this scanner never
    # itself contains the literal scheme prefix (it must pass its own scan).
    ("credential", "op-ref", re.compile("op" + ":" + "//" + r"[^\s'\"<>]{3,}")),
    ("credential", "gh-token", re.compile(r"(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{36,}")),
    ("credential", "gh-finepat", re.compile(r"(?<![A-Za-z0-9_])github_pat_[A-Za-z0-9_]{22,}")),
    ("credential", "hf-token", re.compile(r"(?<![A-Za-z0-9_])hf_[A-Za-z0-9]{30,}")),
    ("credential", "sk-key", re.compile(r"(?<![A-Za-z0-9_-])sk-(?:ant-)?[A-Za-z0-9_-]{20,}")),
    ("credential", "aws-key-id", re.compile(r"(?<![A-Z0-9])(?:AKIA|ASIA|ABIA|ACCA)[A-Z0-9]{16}(?![A-Z0-9])")),
    ("credential", "google-api", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("credential", "slack", re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}")),
    ("credential", "generic-assign", re.compile(
        r"(?i)\b(?:api[_-]?key|apikey|secret|password|passwd|token|credential)s?\b\s*[:=]\s*['\"]?[A-Za-z0-9/+=._\-]{16,}")),
    ("privacy", "host-path", re.compile(r"/(?:home|Users|root)/[A-Za-z0-9._\-]+(?:/[A-Za-z0-9._\-]+)*")),
    ("privacy", "scratch-path", re.compile(r"/fast/scratch/[A-Za-z0-9._\-/]*")),
    ("privacy", "tmp-path", re.compile(r"/tmp/[A-Za-z0-9._\-]{4,}")),
    ("privacy", "email", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("injection", "ignore-previous", re.compile(
        r"(?i)\b(?:ignore|disregard|forget|override)\b[^.\n]{0,40}\b(?:previous|prior|earlier|above|all)\b[^.\n]{0,40}\b(?:instruction|prompt|rule|direction|message)s?\b")),
    ("injection", "you-are-now", re.compile(
        r"(?i)\byou are now\b|\bact as\b[^.\n]{0,30}\b(?:assistant|agent|model|ai)\b|\bnew (?:system )?(?:prompt|instruction)s?\b")),
    ("injection", "ai-directed-please", re.compile(
        r"(?i)\b(?:the |an |your )?(?:ai|assistant|model|agent|llm|language model)\b[^.\n]{0,30}"
        r"\b(?:should|must|shall|needs to|has to|please)\b[^.\n]{0,60}\b(?:read|write|report|run|execute|output|answer|ignore|disregard)\b")),
    ("injection", "system-prompt-tag", re.compile(r"(?i)<\|?(?:system|im_start|assistant)\|?>|\[/?INST\]|<<SYS>>")),
    ("injection", "do-not-tell", re.compile(
        r"(?i)\b(?:do not|don'?t|never)\b[^.\n]{0,30}\b(?:tell|inform|mention|reveal|show)\b[^.\n]{0,40}\b(?:the )?(?:user|human|operator)\b")),
]


def looks_binary(path: str) -> bool:
    try:
        with open(path, "rb") as fh:
            return b"\x00" in fh.read(BIN_PROBE)
    except OSError:
        return True


def mask(text: str) -> str:
    text = text.replace("\t", " ").replace("\n", " ")
    if len(text) > 120:
        text = text[:120]
    return text


def scan_file(path: str, rel: str) -> list[str]:
    try:
        size = os.path.getsize(path)
    except OSError as exc:
        return [f"error\t{rel}\tstat\t{exc.strerror}"]
    if size > MAX_BYTES:
        return []
    if looks_binary(path):
        return []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        return [f"error\t{rel}\tread\t{exc.strerror}"]
    out = []
    for n, line in enumerate(lines, 1):
        for cls, rule, rx in RULES:
            m = rx.search(line)
            if m:
                snippet = mask(line)
                if cls == "credential":
                    snippet = mask(re.sub(r"([A-Za-z0-9._\-]{8})[A-Za-z0-9._\-]+", r"\1…", m.group(0)))
                out.append(f"{cls}\t{rel}:{n}\t{rule}\t{snippet}")
    return out


def main(argv: list[str]) -> int:
    targets = argv[1:]
    if not targets:
        print("usage: scan_extended.py PATH [PATH...]")
        return 2
    hits: list[str] = []
    files = 0
    for target in targets:
        if os.path.isdir(target):
            for root, dirs, names in os.walk(target):
                dirs[:] = sorted(d for d in dirs if d != ".git")
                for name in sorted(names):
                    p = os.path.join(root, name)
                    if os.path.islink(p):
                        continue
                    files += 1
                    hits.extend(scan_file(p, os.path.relpath(p, os.getcwd())))
        elif os.path.isfile(target):
            files += 1
            hits.extend(scan_file(target, os.path.relpath(target, os.getcwd())))
        else:
            print(f"error\t{target}\tmissing")
    for h in hits:
        print(h)
    print(f"SCAN files={files} hits={len(hits)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
