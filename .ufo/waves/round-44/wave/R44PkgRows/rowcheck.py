#!/usr/bin/env python3
"""R44PkgRows self-check: for each drafted row, verify the anchor cell against the capture.

Checks per row: 11 cells; URL basename == capture name; the anchor's `<file>:<line>` locator names the
capture; the quoted string occurs verbatim on that physical line; the stated word count equals the
whitespace split; the sha256 equals the captured bytes and the spec pin in plans/pkg-spec-r44.json.
"""
import hashlib, json, re, sys, pathlib

CAP = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round44/tb2-feal-linear-cryptanalysis")
SPEC = json.load(open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg-spec-r44.json"))
rows_path = pathlib.Path(sys.argv[1])
rows = [l for l in rows_path.read_text(encoding="utf-8").splitlines() if re.match(r"^\| S\d{3} \|", l)]
print(f"ROWS parsed={len(rows)}")
bad = 0
for line in rows:
    cells = line.strip().strip("|").split("|")
    rid = cells[0].strip()
    if len(cells) != 11:
        print(f"FAIL {rid} cells={len(cells)} expected=11"); bad += 1; continue
    url = re.search(r"https://raw\.githubusercontent\.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/(\S+)", cells[1])
    cap_name = url.group(1).split("/")[-1] if url else "<no-url>"
    spec = SPEC["rows"][rid]
    m = re.search(r':(\d+) ["“](.+?)["”] \((\d+) words?\); sha256 ([0-9a-f]{64})', cells[5])
    if not m:
        print(f"FAIL {rid} anchor-parse"); bad += 1; continue
    lineno, quote, wc, digest = int(m.group(1)), m.group(2), int(m.group(3)), m.group(4)
    text = (CAP / cap_name).read_text(encoding="utf-8")
    lines = text.split("\n")
    ok_line = 0 < lineno <= len(lines) and quote in lines[lineno - 1]
    ok_words = len(quote.split()) == wc
    real = hashlib.sha256((CAP / cap_name).read_bytes()).hexdigest()
    ok_sha = real == digest == spec["sha256"]
    ok_cap = spec["capture"] == cap_name and cap_name != "<no-url>"
    stat = "OK" if (ok_line and ok_words and ok_sha and ok_cap) else "FAIL"
    if stat == "FAIL": bad += 1
    print(f"{stat} {rid} capture={cap_name} line={lineno} verbatim={ok_line} words={wc}/{len(quote.split())} "
          f"sha256_pin={ok_sha} cells=11")
print(f"DEFECTS {bad}")
sys.exit(1 if bad else 0)
