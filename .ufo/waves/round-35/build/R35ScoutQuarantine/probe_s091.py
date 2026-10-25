#!/usr/bin/env python3
"""R35ScoutQuarantine — S091 staged-quote presence probe.

Strip tags from an HTML capture (html.unescape + re.sub('<[^>]+>','') + whitespace removal),
then test whether the staged quote carried at
corpus/lessons/round-34-verifier-spotcheck.md:64 is present, and report its approximate line in
the RAW html.

Usage: probe_s091.py <html-path> <spotcheck-path> [--raw-line]
"""
import html
import re
import sys


def strip_tags(raw: str) -> str:
    return re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", "", raw)))


def staged_quote(spotcheck_path: str):
    """The staged quote is the quoted span on the S091 row of the spot-check table."""
    lines = open(spotcheck_path, encoding="utf-8").read().splitlines()
    row = None
    for i, l in enumerate(lines, 1):
        if "S091" in l and l.startswith("|"):
            row = (i, l)
            break
    if row is None:
        raise SystemExit(f"no S091 table row in {spotcheck_path}")
    ln, text = row
    quotes = re.findall(r"「([^」]+)」", text)
    if not quotes:
        raise SystemExit(f"no 「」 quote on S091 row line {ln}")
    return ln, quotes


def main() -> int:
    html_path, spotcheck_path = sys.argv[1], sys.argv[2]
    want_raw_line = "--raw-line" in sys.argv

    row_line, quotes = staged_quote(spotcheck_path)
    raw = open(html_path, encoding="utf-8", errors="replace").read()
    flat = strip_tags(raw)
    print(f"html_path={html_path}")
    print(f"html_bytes={len(raw.encode('utf-8', 'replace'))} raw_chars={len(raw)}")
    print(f"spotcheck_row_line={row_line} staged_quotes={len(quotes)}")
    for q in quotes:
        qf = re.sub(r"\s+", "", q)
        present = qf in flat
        print(f"  quote_len={len(qf)} present_in_stripped={present} :: {q[:60]}")
        if present and want_raw_line:
            # approximate raw-html line: find the raw line whose tag-stripped form contains it
            hits = []
            for i, l in enumerate(raw.splitlines(), 1):
                lf = strip_tags(l)
                if qf in lf:
                    hits.append(i)
            # fallback: locate the byte offset of the first 12 chars of the quote in the flat text
            off = flat.find(qf)
            prefix = flat[:off]
            approx = raw.count("\n", 0, 0)  # placeholder
            # map flat offset back to raw line by cumulative stripped lengths
            cum = 0
            approx_line = None
            for i, l in enumerate(raw.splitlines(), 1):
                seg = strip_tags(l)
                if cum + len(seg) > off:
                    approx_line = i
                    break
                cum += len(seg)
            print(f"    raw_lines_containing={hits} flat_offset={off} approx_raw_line={approx_line}")
            if hits:
                print(f"    approx_raw_line_from_hit={hits[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
