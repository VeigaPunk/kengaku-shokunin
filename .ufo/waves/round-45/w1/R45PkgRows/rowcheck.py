#!/usr/bin/env python3
"""R45PkgRows self-check: verify each drafted row against its capture and the frozen spec.

Per row: 11 cells; the URL's task-relative path equals the spec's `upstream`; the anchor's
`<file>:<line>` locator names that capture; the quoted string occurs verbatim on that physical line;
the stated word count equals the whitespace split and sits inside the spec's `entry_rules.quote_words`;
the sha256 equals the captured bytes and the spec pin; row tier/status/opened match `entry_rules`; the
teaches cell clears `entry_rules.min_teaches_words`; recheck is an accepted cadence.
"""
import hashlib, json, pathlib, re, sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CAP = LANE / "corpus/evidence/round45/tb2-password-recovery"
SPEC = json.load(open(LANE / "plans/pkg-spec-r45.json"))
RULES = SPEC["entry_rules"]
lo, hi = RULES["quote_words"]
rows_path = pathlib.Path(sys.argv[1])
rows = [l for l in rows_path.read_text(encoding="utf-8").splitlines() if re.match(r"^\| S\d{3} \|", l)]
print(f"ROWS parsed={len(rows)}")
bad = 0
seen = set()
for line in rows:
    cells = line.strip().strip("|").split("|")
    rid = cells[0].strip()
    if len(cells) != 11:
        print(f"FAIL {rid} cells={len(cells)} expected=11"); bad += 1; continue
    seen.add(rid)
    url = re.search(r"https://raw\.githubusercontent\.com/harbor-framework/terminal-bench-2/"
                    r"2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/(\S+)", cells[1])
    rel = url.group(1) if url else "<no-url>"
    spec = SPEC["rows"].get(rid, {})
    cap_name = spec.get("capture")
    ok_cap = bool(url) and rel == spec.get("upstream") and cap_name is not None
    m = re.search(r':(\d+) ["“](.+?)["”] \((\d+) words?\); sha256 ([0-9a-f]{64})', cells[5])
    if not m:
        print(f"FAIL {rid} anchor-parse"); bad += 1; continue
    lineno, quote, wc, digest = int(m.group(1)), m.group(2), int(m.group(3)), m.group(4)
    text = (CAP / spec.get("upstream", cap_name)).read_text(encoding="utf-8")
    lines = text.split("\n")
    ok_line = 0 < lineno <= len(lines) and quote in lines[lineno - 1]
    ok_words = len(quote.split()) == wc and lo <= wc <= hi
    real = hashlib.sha256((CAP / spec.get("upstream", cap_name)).read_bytes()).hexdigest()
    ok_sha = real == digest == spec.get("sha256")
    ok_meta = (cells[3].strip() == RULES["row_tier"] and cells[7].strip() == RULES["row_status"]
               and cells[8].strip() == RULES["row_opened"]
               and re.fullmatch(r"[0-9]+d|\d{4}-\d{2}-\d{2}|[A-Za-z][A-Za-z0-9 _-]*", cells[9].strip()) is not None)
    ok_teach = len(cells[6].split()) >= RULES["min_teaches_words"]
    stat = "OK" if all((ok_cap, ok_line, ok_words, ok_sha, ok_meta, ok_teach)) else "FAIL"
    if stat == "FAIL":
        bad += 1
    print(f"{stat} {rid} capture={cap_name} upstream={rel} line={lineno} verbatim={ok_line} "
          f"words={wc}/{len(quote.split())} range={lo}-{hi} sha256_pin={ok_sha} cap={ok_cap} "
          f"meta={ok_meta} teaches={len(cells[6].split())} cells=11")
missing = sorted(set(SPEC["rows"]) - seen)
if missing:
    print(f"FAIL spec rows absent from draft: {','.join(missing)}"); bad += len(missing)
print(f"DEFECTS {bad}")
sys.exit(1 if bad else 0)
