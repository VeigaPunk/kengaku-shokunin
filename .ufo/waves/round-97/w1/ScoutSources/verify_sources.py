#!/usr/bin/env python3
"""Reopen S317-S325 from corpus/SOURCES.md at T: HTTP, size, sha256, located quote."""
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
OUT = "/fast/scratch/hyaku/kengaku-r97/ScoutSources/http"
IDS = [f"S{n}" for n in range(317, 326)]

rows = {}
with open(os.path.join(LANE, "corpus/SOURCES.md"), encoding="utf-8") as fh:
    for raw in fh:
        if not raw.startswith("| S3"):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if cells[0] in IDS:
            rows[cells[0]] = cells

res = []
for sid in IDS:
    c = rows[sid]
    # columns: id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by
    src = c[1]
    m = re.search(r"https://\S+", src)
    url = m.group(0) if m else None
    kind, tier, status = c[2], c[3], c[7]
    anchor = c[5]
    teaches = c[6]
    # size/sha/quote live in the anchor cell
    msize = re.search(r"(\d+) B\b", anchor)
    msha = re.search(r"sha256 ([0-9a-f]{64})", anchor)
    mq = re.search(r'(\S+?):(\d+) quote \u201c(.*?)\u201d \((\d+) words\)', anchor)
    rec = {
        "id": sid, "url": url, "kind": kind, "tier": tier, "status": status,
        "anchor": anchor,
        "expected_size": int(msize.group(1)) if msize else None,
        "expected_sha256": msha.group(1) if msha else None,
        "quote_file": mq.group(1) if mq else None,
        "quote_line": int(mq.group(2)) if mq else None,
        "quote": mq.group(3) if mq else None,
        "quote_words": int(mq.group(4)) if mq else None,
    }
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "kengaku-source-recheck/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            rec["http"] = r.status
            rec["final_url"] = r.geturl()
            rec["content_type"] = r.headers.get("Content-Type")
            rec["etag"] = r.headers.get("ETag")
            rec["last_modified"] = r.headers.get("Last-Modified")
    except urllib.error.HTTPError as e:
        body = b""
        rec["http"] = e.code
        rec["error"] = f"HTTPError {e.code}"
    except Exception as e:  # noqa: BLE001
        body = b""
        rec["http"] = None
        rec["error"] = f"{type(e).__name__}: {e}"
    rec["size"] = len(body)
    rec["sha256"] = hashlib.sha256(body).hexdigest()
    name = os.path.basename(url)
    with open(os.path.join(OUT, f"{sid}__{name}"), "wb") as fh:
        fh.write(body)
    # locate quote at the claimed line of the claimed file
    text = body.decode("utf-8", "replace")
    lines = text.splitlines()
    rec["nlines"] = len(lines)
    qline = rec["quote_line"]
    if qline and 1 <= qline <= len(lines):
        got = lines[qline - 1]
        rec["line_text"] = got
        rec["quote_at_line"] = rec["quote"] in got
    else:
        rec["quote_at_line"] = False
        rec["line_text"] = None
    # also: does the quote occur anywhere?
    rec["quote_anywhere"] = (rec["quote"] in text) if rec["quote"] else False
    rec["quote_occurrences"] = text.count(rec["quote"]) if rec["quote"] else 0
    rec["size_ok"] = rec["size"] == rec["expected_size"]
    rec["sha_ok"] = rec["sha256"] == rec["expected_sha256"]
    rec["words_ok"] = (rec["quote_words"] is not None and rec["quote_words"] <= 25)
    rec["actual_quote_words"] = len(rec["quote"].split()) if rec["quote"] else None
    res.append(rec)

with open("/fast/scratch/hyaku/kengaku-r97/ScoutSources/verify.json", "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=2)

for r in res:
    print(f"{r['id']} http={r['http']} size={r['size']} size_ok={r['size_ok']} sha_ok={r['sha_ok']} "
          f"line={r['quote_line']} at_line={r['quote_at_line']} anywhere={r['quote_anywhere']} "
          f"occ={r['quote_occurrences']} words={r['actual_quote_words']} status={r['status']}")
