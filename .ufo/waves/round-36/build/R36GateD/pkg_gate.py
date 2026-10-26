#!/usr/bin/env python3
"""Hardened package gate for a pinned knowledge entry (round 36 C1 candidate).
  package --root DIR --spec SPEC [--require-clean-tree] [--rerun] | d4-line --file F --spec SPEC
  d5-line --file F --capture-dir D --spec SPEC | --selftest   (--spec follows the subcommand)

One `P<n> ok|DEFECT <reason>` line per package check (optional ones: `P<n> skip <why>`), then
`defects=<n>`; line modes print `D4|D5 ok|DEFECT <reason>` then `defects=<n>`. Exit 0 accept, 1
reject, 2 usage/setup (a parse exception inside a check is a DEFECT line, exit 1).

Every clause reads the spec JSON, never a fixture name, path or marker string. Package checks:
P1 frozen instruments at their pinned sha256; P2 capture SHA256SUMS (listed digests equal the bytes,
each row capture at its pin); P3 receipt sha256 equals its pin; P4 sources rows (one per spec id, 11
cells, tier/status/opened from entry_rules, pinned URL, used-by = entry, teaches >=
min_teaches_words and pairwise distinct); P5 entry provenance trio in spec order, verified-at,
recheck; P6 `## Negative space` falsifier; P7 `## Located quotes` (Quote/Location header, every row
parses, each quote within quote_words and verbatim on its cited capture lines, >= min_quotes
distinct quotes at >= min_distinct_locations lines); P8 readme index row and coverage bullet;
P9 knowledge files == index rows; P10 no untracked file under --require-clean-tree; P11 --rerun
reproduces the receipt byte-for-byte. No network: the interpreter fallback is `uv run --offline`.
"""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

QUOTE_ROW = re.compile(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$")
SEP_ROW = re.compile(r"^\|[\s|:-]+\|$")
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SUMS_RE = re.compile(r"([0-9a-f]{64})\s+\*?(\S+)")
RECHECK_RE = re.compile(r"recheck: (\d{4}-\d{2}-\d{2}|\d+d|on-release)\b")
KEYS = ("entry", "capture_dir", "receipt", "receipt_sha256", "probe_cmd", "sources", "readme",
        "knowledge_glob", "raw_base", "rows", "entry_rules", "frozen_instruments", "d4", "d5")

def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def read_sums(path):
    """manifest -> {basename: digest}; a line that does not parse is simply not listed."""
    out = {}
    for line in pathlib.Path(path).read_text().splitlines():
        m = SUMS_RE.search(line.strip())
        if m:
            out[pathlib.PurePath(m.group(2)).name] = m.group(1)
    return out

def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)

def p1_instruments(root, spec):
    pins = spec["frozen_instruments"]
    bad = [rel for rel, pin in pins.items()
           if not (root / rel).is_file() or sha256(root / rel) != pin]
    return bool(pins) and not bad, f"instruments={len(pins)} mismatched={bad or 0}"

def p2_captures(root, spec):
    cap, sums = root / spec["capture_dir"], root / spec["capture_dir"] / "SHA256SUMS"
    if not sums.is_file():
        return False, "SHA256SUMS absent"
    listed = read_sums(sums)
    bad = [n for n, d in listed.items() if not (cap / n).is_file() or sha256(cap / n) != d]
    if bad:
        return False, f"listed digest mismatch or missing file: {bad[0]}"
    for rid, row in spec["rows"].items():
        if listed.get(row["capture"]) != row["sha256"]:
            return False, f"{rid} capture {row['capture']} not listed at its pinned sha256"
    return True, f"listed={len(listed)} pinned_rows={len(spec['rows'])}"

def p3_receipt(root, spec):
    rec = root / spec["receipt"]
    if not rec.is_file():
        return False, "receipt absent"
    dig = sha256(rec)
    return dig == spec["receipt_sha256"], f"receipt_sha256={dig[:16]} matched={dig == spec['receipt_sha256']}"

def p4_sources(root, spec):
    rules, teaches, rows = spec["entry_rules"], [], {}
    for line in (root / spec["sources"]).read_text().splitlines():
        m = ROW_RE.match(line)
        if m:
            rows.setdefault(m.group(1), []).append(line)
    for rid, row in spec["rows"].items():
        got = rows.get(rid, [])
        if len(got) != 1:
            return False, f"{rid} present {len(got)} times"
        cells = [c.strip() for c in got[0].strip().strip("|").split("|")]
        if len(cells) != 11:
            return False, f"{rid} has {len(cells)} cells"
        if (cells[3], cells[7], cells[8]) != (rules["row_tier"], rules["row_status"],
                                              rules["row_opened"]):
            return False, f"{rid} tier/status/opened = {cells[3]}/{cells[7]}/{cells[8]}"
        if re.findall(r"https?://\S+", cells[1]) != [spec["raw_base"] + row["upstream"]]:
            return False, f"{rid} source URL is not the pinned raw URL"
        if cells[10] != spec["entry"]:
            return False, f"{rid} used-by {cells[10]!r}"
        if len(cells[6].split()) < rules["min_teaches_words"]:
            return False, f"{rid} teaches has {len(cells[6].split())} words"
        teaches.append(cells[6])
    if len(set(teaches)) != len(teaches):
        return False, "teaches cells are not pairwise distinct"
    return True, f"rows={len(spec['rows'])} min_teaches={min(len(t.split()) for t in teaches)}"

def p5_entry(root, spec):
    p, ids = root / spec["entry"], list(spec["rows"])
    if not p.is_file():
        return False, "entry absent"
    lines = p.read_text().splitlines()
    for i, rid in enumerate(ids):
        want = spec["raw_base"] + spec["rows"][rid]["upstream"]
        if not (len(lines) > i and lines[i].startswith(f"source: {rid} ") and want in lines[i]):
            return False, f"line {i + 1} is not the {rid} source line with its pinned URL"
    verified = spec["entry_rules"]["verified_at"]
    if len(lines) <= len(ids) or lines[len(ids)] != f"verified-at: {verified}":
        return False, "verified-at line absent or mismatched"
    if len(lines) <= len(ids) + 1 or not RECHECK_RE.match(lines[len(ids) + 1]):
        return False, "recheck line lacks date/cadence"
    return True, f"source_lines={len(ids)} verified_at={verified}"

def p6_negative(root, spec):
    m = re.search(r"^## Negative space\n(.*?)(?=^## |\Z)",
                  (root / spec["entry"]).read_text(), re.S | re.M)
    if not m:
        return False, "negative space section absent"
    return "falsif" in m.group(1).lower(), f"falsifier={'falsif' in m.group(1).lower()}"

def quote_rows(text):
    """(section, data_rows, header_ok); the first pipe row is a header when it is not a quote row."""
    m = re.search(r"^## Located quotes\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return None, [], False
    pipe = [l for l in m.group(1).splitlines() if l.startswith("|")]
    if not pipe:
        return m, [], False
    if QUOTE_ROW.match(pipe[0]):
        return m, [l for l in pipe if not SEP_ROW.match(l.strip())], True
    return (m, [l for l in pipe[1:] if not SEP_ROW.match(l.strip())],
            "Quote" in pipe[0] and "Location" in pipe[0])

def p7_quotes(root, spec):
    sec, data, header_ok = quote_rows((root / spec["entry"]).read_text())
    if sec is None or not header_ok:
        return False, "located quotes section or Quote/Location header absent"
    if not data:
        return False, "no quote data rows"
    parsed, unparsed = [], []
    for line in data:
        m = QUOTE_ROW.match(line)
        (parsed if m else unparsed).append(m or line)
    if unparsed:
        return False, f"unparsed quote rows={len(unparsed)}: {str(unparsed[0])[:60]!r}"
    rules, lo, hi = spec["entry_rules"], *spec["entry_rules"]["quote_words"]
    cap, quotes, locs = root / spec["capture_dir"], set(), set()
    for m in parsed:
        quote, name, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
        words = len(quote.split())
        if not lo <= words <= hi:
            return False, f"quote has {words} words (want {lo}..{hi}): {quote[:40]!r}"
        f = cap / name
        if not f.is_file():
            return False, f"quote cites missing capture {name}"
        src = f.read_text().splitlines()
        if not 1 <= a <= b <= len(src):
            return False, f"citation {name}:{a}-{b} outside the capture"
        if quote not in "\n".join(src[a - 1:b]):
            return False, f"quote not verbatim on {name}:{a}-{b}: {quote[:40]!r}"
        quotes.add(quote)
        locs.add((name, a))
    if len(quotes) < rules["min_quotes"] or len(locs) < rules["min_distinct_locations"]:
        return False, (f"distinct quotes={len(quotes)} locations={len(locs)} below "
                       f"{rules['min_quotes']}/{rules['min_distinct_locations']}")
    return True, f"rows={len(parsed)} quotes={len(quotes)} locations={len(locs)}"

def p8_index(root, spec):
    rel = spec["entry"].removeprefix("corpus/")
    text = (root / spec["readme"]).read_text()
    idx = [l for l in text.splitlines() if l.startswith(f"| `{rel}` |")]
    if len(idx) != 1:
        return False, f"index rows for {rel}={len(idx)}"
    missing = [rid for rid in spec["rows"] if rid not in idx[0]]
    if missing:
        return False, f"index row omits {missing}"
    cov = re.search(r"^## Coverage map\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not cov or rel not in cov.group(1):
        return False, "coverage-map bullet absent"
    return True, f"index_rows=1 cites={len(spec['rows'])} coverage=yes"

def p9_parity(root, spec):
    r = git(root, "ls-files", spec["knowledge_glob"])
    if r.returncode != 0:
        return False, f"git ls-files failed: {r.stderr.strip()[:60]}"
    files = [x for x in r.stdout.split() if x]
    nidx = sum(1 for l in (root / spec["readme"]).read_text().splitlines()
               if l.startswith("| `knowledge/"))
    return bool(files) and len(files) == nidx, f"knowledge_files={len(files)} index_rows={nidx}"

def p10_clean(root, _spec):
    r = git(root, "ls-files", "--others", "--exclude-standard")
    if r.returncode != 0:
        return False, f"git ls-files failed: {r.stderr.strip()[:60]}"
    left = [x for x in r.stdout.splitlines() if x.strip()]
    return not left, f"untracked={len(left)}{'' if not left else ': ' + left[0][:60]}"

def p11_rerun(root, spec):
    rec, cmd = (root / spec["receipt"]).read_bytes(), list(spec["probe_cmd"])
    attempts = [[sys.executable, *cmd]]
    m = re.search(rb"biopython=(\d[\w.+-]*)", rec)  # the receipt carries the interpreter pin
    if m:
        attempts.append(["uv", "run", "--offline", "--no-project", "--with",
                         "biopython==" + m.group(1).decode(), "python3", *cmd])
    last = "no attempt"
    for attempt in attempts:
        try:
            r = subprocess.run(attempt, cwd=root, capture_output=True, timeout=600)
        except (OSError, subprocess.SubprocessError) as e:
            last = type(e).__name__
            continue
        if r.returncode == 0 and r.stdout == rec:
            return True, f"probe={pathlib.Path(attempt[0]).name} stdout=byte_equal"
        last = f"exit={r.returncode} stdout_differs={r.stdout != rec}"
    return False, f"receipt not reproduced ({last})"

def check_d4(path, spec):
    d4 = spec["d4"]
    lines = [l for l in path.read_text().splitlines() if l.startswith(d4["label"])]
    if len(lines) != 1:
        return False, f"lines_with_label={len(lines)} (want 1)"
    for i, pat in enumerate(d4["patterns"], 1):
        if not re.search(pat, lines[0]):
            return False, f"pattern_{i}_absent"
    return True, f"patterns={len(d4['patterns'])}"

def check_d5(path, spec, capdir):
    d5 = spec["d5"]
    lines = [l for l in path.read_text().splitlines() if l.startswith(d5["label"])]
    if len(lines) != 1:
        return False, f"lines_with_label={len(lines)} (want 1)"
    if d5["forbid"] in lines[0]:
        return False, f"forbid {d5['forbid']!r} present"
    sent = [s for s in lines[0].split(". ") if d5["capture_name"] in s]
    if not sent or d5["require"] not in sent[0] or sent[0].index(d5["require"]) > sent[0].index(d5["capture_name"]):
        return False, "require phrase not bound to the cited capture"
    cap, man = capdir / d5["capture_name"], capdir / d5["manifest_name"]
    if not cap.is_file() or not man.is_file():
        return False, f"capture {d5['capture_name']} or manifest {d5['manifest_name']} absent"
    listed, dig = read_sums(man), sha256(cap)
    if listed.get(d5["capture_name"]) != dig:
        return False, f"capture digest not pinned by {d5['manifest_name']}"
    bad = [n for n, p in listed.items() if not (capdir / n).is_file() or sha256(capdir / n) != p]
    if bad:
        return False, f"manifest entry mismatched: {bad[0]}"
    if d5["quote"] not in cap.read_text(errors="replace"):
        return False, "quote absent from capture"
    return True, f"capture={d5['capture_name']} sha={dig[:16]} quote=present"

def run_package(root, spec, require_clean, rerun):
    checks = [("P1", p1_instruments), ("P2", p2_captures), ("P3", p3_receipt),
              ("P4", p4_sources), ("P5", p5_entry), ("P6", p6_negative), ("P7", p7_quotes),
              ("P8", p8_index), ("P9", p9_parity), ("P10", p10_clean, require_clean),
              ("P11", p11_rerun, rerun)]
    defects = 0
    for cid, fn, *rest in checks:
        if rest and not rest[0]:
            print(f"{cid} skip flag-absent")
            continue
        try:
            ok, reason = fn(root, spec)
        except Exception as e:  # a parse failure is a defect, never a pass
            ok, reason = False, f"error {type(e).__name__}: {e}"
        defects += not ok
        print(f"{cid} {'ok' if ok else 'DEFECT'} {reason}")
    print(f"defects={defects}")
    return 0 if defects == 0 else 1

def mini_fixture(base, mode):
    """A tiny self-contained package (one row, eight 3-word quotes, no lane bytes)."""
    root = base / "pkg"
    (root / "corpus/knowledge").mkdir(parents=True)
    cap = root / "cap"
    cap.mkdir()
    lines = [f"line{i} alpha{i} beta{i} gamma{i}" for i in range(1, 9)]
    (cap / "cap.txt").write_text("\n".join(lines) + "\n")
    dig = sha256(cap / "cap.txt")
    (cap / "SHA256SUMS").write_text(f"{dig}  cap.txt\n")
    quotes = [f"| c{i} | “{lines[i - 1][:lines[i - 1].index(' gamma')]}” | `cap.txt:{i}` |"
              for i in range(1, 9)]
    if mode == "one-word":
        quotes = [re.sub(r"“(.*?)”", lambda m: "“" + m.group(1).split()[0] + "”", q) for q in quotes]
    if mode == "unparsed":
        quotes.append('| bad | "straight quotes" | `cap.txt:1` |')
    (root / "corpus/knowledge/mini.md").write_text("\n".join([
        "source: S001 — https://example.invalid/base/cap.txt", "verified-at: 2026-10-25",
        "recheck: 180d", "# mini", "", "## Negative space", "",
        "Falsifier: a changed cap.txt digest.", "", "## Located quotes", "",
        "| Claim | Quote | Location |", "|---|---|---|", *quotes]) + "\n")
    (root / "corpus/SOURCES.md").write_text(
        "| S001 | cap — https://example.invalid/base/cap.txt | code | A | scope | anchor | "
        "one two three four five six seven eight | mined | 2026-10-25 | 180d | "
        "corpus/knowledge/mini.md |\n")
    rel = "knowledge/mini.md"
    (root / "corpus/README.md").write_text(
        f"| `{rel}` | mini | S001 |\n\n## Coverage map\n\n- {rel} — mini\n")
    (root / "receipt.txt").write_text("cases=1 mismatches=0\n")
    (root / "probe.py").write_text("print('cases=1 mismatches=0')\n")
    rules = {"verified_at": "2026-10-25", "min_quotes": 8, "min_distinct_locations": 8,
             "quote_words": [3, 25], "min_teaches_words": 8, "row_opened": "2026-10-25",
             "row_tier": "A", "row_status": "mined"}
    spec = {"entry": "corpus/knowledge/mini.md", "capture_dir": "cap", "receipt": "receipt.txt",
            "receipt_sha256": sha256(root / "receipt.txt"), "probe_cmd": ["probe.py"],
            "sources": "corpus/SOURCES.md", "readme": "corpus/README.md",
            "knowledge_glob": "corpus/knowledge/*.md",
            "raw_base": "https://example.invalid/base/",
            "rows": {"S001": {"capture": "cap.txt", "upstream": "cap.txt", "sha256": dig}},
            "entry_rules": rules, "frozen_instruments": {"probe.py": sha256(root / "probe.py")},
            "d4": {"label": "none", "patterns": []}, "d5": {"label": "none"}}
    (base / "spec.json").write_text(json.dumps(spec))
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    return root, base / "spec.json"

def selftest():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="k36-gate-selftest-"))
    want, got = {"pass": 0, "one-word": 1, "unparsed": 1}, {}
    try:
        for mode in want:
            base = tmp / mode
            base.mkdir()
            root, spec = mini_fixture(base, mode)
            got[mode] = run_package(root, json.loads(spec.read_text()), True, False)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST " + " ".join(f"{k}={v}" for k, v in got.items()))
    return 0 if got == want else 1

def main(argv=None):
    ap = argparse.ArgumentParser(description="hardened pinned-entry gate (round 36 C1)")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="mode")
    pk, d4, d5 = (sub.add_parser(n) for n in ("package", "d4-line", "d5-line"))
    pk.add_argument("--root", required=True)
    pk.add_argument("--require-clean-tree", action="store_true")
    pk.add_argument("--rerun", action="store_true")
    d4.add_argument("--file", required=True)
    d5.add_argument("--file", required=True)
    d5.add_argument("--capture-dir", required=True)
    for p in (pk, d4, d5):
        p.add_argument("--spec", required=True)
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.mode is None:
        ap.print_usage(sys.stderr)
        return 2
    try:
        spec = json.loads(pathlib.Path(a.spec).read_text())
        if not isinstance(spec, dict) or any(k not in spec for k in KEYS):
            raise ValueError("spec lacks required keys")
    except Exception as e:
        print(f"P0 DEFECT spec unusable: {type(e).__name__}: {e}")
        return 2
    if a.mode == "package":
        root = pathlib.Path(a.root)
        if not root.is_dir():
            print(f"P0 DEFECT root is not a directory: {root}")
            return 2
        return run_package(root.resolve(), spec, a.require_clean_tree, a.rerun)
    f = pathlib.Path(a.file)
    if not f.is_file():
        print(f"P0 DEFECT file absent: {f}")
        return 2
    tag = "D4" if a.mode == "d4-line" else "D5"
    try:
        if a.mode == "d4-line":
            ok, reason = check_d4(f, spec)
        else:
            capdir = pathlib.Path(a.capture_dir)
            if not capdir.is_dir():
                print(f"P0 DEFECT capture dir absent: {capdir}")
                return 2
            ok, reason = check_d5(f, spec, capdir)
    except Exception as e:
        print(f"{tag} DEFECT error {type(e).__name__}: {e}")
        print("defects=1")
        return 1
    print(f"{tag} {'ok' if ok else 'DEFECT'} {reason}")
    print(f"defects={0 if ok else 1}")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:  # setup error, never a silent accept
        print(f"P0 DEFECT setup error {type(e).__name__}: {e}")
        sys.exit(2)
