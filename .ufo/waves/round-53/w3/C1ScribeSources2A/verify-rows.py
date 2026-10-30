#!/usr/bin/env python3
"""Re-verify every row of rows.md against the archived bytes kept in ./fetched/.

Run from this seat directory:
    python3 verify-rows.py            # writes quote-locations.tsv, prints a summary

For each row it takes the quote out of the row's anchor cell, locates it in the kept bytes
(PDF: plain pdftotext; HTML: raw and tag-stripped; Markdown: raw line), and prints both the
raw and the rendered line numbers so the location labels in rows.md and gate.md can be checked.
"""
import hashlib, html, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FETCHED = os.path.join(HERE, "fetched")

# row id -> file kept in fetched/
FILES = {
    "T01": "barr2015.pdf", "T02": "petrovic-google.pdf", "T03": "schuler-wayback.txt",
    "T04": "jain-kalburgi-pdf.pdf", "T05": "blindspot-2610.32548v1.html",
    "T06": "mutgen-2506.02954-abs.html", "T07": "assertion-roulette-wayback-2025-01-18.html",
    "T08": "konstantinou-2410.21136-abs.html", "T09": "benchjack-2605.12673v1-first1MiB.html",
    "T10": "unearned-passes-2609.34262v1.html", "T11": "verification-horizon-2606.26300v1.html",
    "T12": "holdout-findings-README.md", "T13": "betterbench-2411.12990v1.html",
    "T14": "fantastic-bugs-neurips2025-abstract.html", "T15": "abc-2507.02825v1.html",
    "T16": "abc-project-page.html", "T17": "arxiv-2410.20574-abs.html",
    "T18": "betterbench-project-site-wayback.html",
}
n = lambda s: re.sub(r"\s+", " ", s)


def lines_of(path):
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if path.endswith(".pdf"):
        txt = subprocess.run(["pdftotext", "-q", path, "-"], capture_output=True, text=True).stdout
        return raw, sha, txt.split("\n"), None
    text = raw.decode("utf-8", "replace")
    raw_lines = text.split("\n")
    rendered = html.unescape(re.sub(r"<[^>]+>", " ", text)).split("\n")
    return raw, sha, rendered, raw_lines


def find(lines, quote, span=False):
    q = n(quote)
    hits = [i + 1 for i, l in enumerate(lines) if q in n(l)]
    if hits or not span:
        return hits
    for i in range(len(lines)):
        for j in range(i, min(i + 4, len(lines))):
            if q in n(" ".join(lines[i:j + 1])):
                return [i + 1, j + 1]
    return []


rows = []
for line in open(os.path.join(HERE, "rows.md"), encoding="utf-8"):
    if not re.match(r"^\|\s*T[0-9]{2}\s*\|", line):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    rid = cells[0]
    quote = re.search(r'quote "([^"]+)"', cells[5]).group(1)
    url = re.search(r"https?://[^\s|]+", cells[1]).group(0)
    rows.append((rid, cells[1], cells[2], cells[3], cells[7], cells[8], cells[9], cells[10], quote, url))

out = []
print(f"{'id':4} {'words':>5} {'rendered':>10} {'raw':>8} {'located':>8}  quote")
for rid, source, kind, tier, status, opened, recheck, usedby, quote, url in rows:
    path = os.path.join(FETCHED, FILES[rid])
    raw, sha, rendered, raw_lines = lines_of(path)
    span = path.endswith(".pdf") or path.endswith(".txt")   # PDF/plain-text quotes may wrap lines
    r_hits = find(rendered, quote, span=span)
    raw_hits = find(raw_lines, quote, span=span) if raw_lines is not None else []
    located = bool(r_hits) or bool(raw_hits)
    words = len(quote.split())
    print(f"{rid:4} {words:5} {str(r_hits[:2]):>10} {str(raw_hits[:2]):>8} {'YES' if located else 'MISS':>8}  {quote[:52]}")
    out.append("\t".join([rid, url, tier, kind, status, opened, recheck, usedby,
                           str(len(raw)), sha, str(words),
                           ",".join(map(str, r_hits[:2])), ",".join(map(str, raw_hits[:2])),
                           "located" if located else "MISS", quote]))

with open(os.path.join(HERE, "quote-locations.tsv"), "w", encoding="utf-8") as fh:
    fh.write("\t".join(["id", "url", "tier", "kind", "status", "opened", "recheck", "used-by",
                         "bytes", "sha256", "quote_words", "rendered_lines", "raw_lines",
                         "located", "quote"]) + "\n")
    for line in out:
        fh.write(line + "\n")
print("\nrows:", len(rows), " misses:", sum(1 for line in out if "\tMISS\t" in line))
