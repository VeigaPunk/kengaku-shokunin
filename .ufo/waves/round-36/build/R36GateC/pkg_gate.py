#!/usr/bin/env python3
"""Hardened package gate (round 36, C1 candidate) — one package definition, re-derived from bytes.

Contract (plans/round36_c1_verify.py): `package --root DIR --spec SPEC [--require-clean-tree]
[--rerun]`, `d4-line --file F --spec SPEC`, `d5-line --file F --capture-dir D --spec SPEC`.
Package: exit 0 accept, 1 reject; exit 2 is usage/setup only (unreadable spec, absent root,
internal error), never 0 or 1. Each check prints one `P<n> ok|DEFECT <reason>` line (or `D4|D5
...`) and a final `defects=<n>` line. Every value is read from the spec and from the bytes the spec
names: no check looks at the caller, the fixture name, or an unnamed path, so a relabelled or
relocated package gets the same verdict. Clauses (round-35 spot-check R35-D1..D4,
plans/round35_hardening.py H1-H6): P1 frozen-instrument SHA-256 pins; P2 receipt pin, green
summary quoted by the entry; P3 entry provenance trio + verified-at + recheck; P4 negative space
with a falsifier; P5 every `## Located quotes` row parses, every quote 3..25 words verbatim on its
cited capture line(s), >=8 distinct quotes at >=8 distinct lines; P6 S105-S107 rows once each, 11
cells, tier A, status mined, pinned URL, used-by = entry, teaches >=8 words pairwise distinct; P7
capture manifest pins every captured byte and leaves none unpinned; P8 README index row + coverage
bullet, knowledge files == index rows; P9 `--require-clean-tree` = no untracked file; P10
`--rerun` = the probe reproduces the receipt byte for byte. The probe toolchain fallback is the
dependency the captured `tests/test.sh` pins (`-w biopython==1.85`, S106), used only when the
running interpreter lacks the module.
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

QUOTE_ROW = re.compile(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$")
SEPARATOR = re.compile(r"^\|[\s|:-]+\|$")
MANIFEST_LINE = re.compile(r"^([0-9a-f]{64}) [ *]([^*\n]+)$")
SUMMARY = re.compile(r"^cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)$")
SOURCES_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
CAPTURE_MANIFEST = "SHA256SUMS"
PROBE_TOOLCHAIN = ["--no-project", "--with", "biopython==1.85"]  # test.sh:21 of the pinned task


def sha256_file(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def section(text, title):
    m = re.search(r"^## " + re.escape(title) + r"\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else None


def quote_table(text):
    """Return (data_rows, unparsed, error). A row that does not parse is a defect, never skipped."""
    block = section(text, "Located quotes")
    if block is None:
        return [], 0, "no `## Located quotes` section"
    rows = [l for l in block.splitlines() if l.startswith("|") and not SEPARATOR.match(l)]
    if not rows:
        return [], 0, "empty quote table"
    header, data = rows[0], rows[1:]
    if "Quote" not in header or "Location" not in header:
        return [], 0, f"quote table header lacks Quote/Location: {header[:60]}"
    parsed = [QUOTE_ROW.match(r) for r in data]
    return [m for m in parsed if m], sum(m is None for m in parsed), None


# ---- package checks -----------------------------------------------------------------------------

def p1_frozen(root, spec, _entry):
    bad = []
    for rel, pin in spec["frozen_instruments"].items():
        p = root / rel
        got = sha256_file(p) if p.is_file() else "absent"
        if got != pin:
            bad.append(f"{rel}={got[:12]}")
    return (not bad, f"frozen_instruments={len(spec['frozen_instruments'])}"
            + (f" changed={','.join(bad)}" if bad else ""))


def p2_receipt(root, spec, entry):
    p = root / spec["receipt"]
    if not p.is_file():
        return False, f"receipt absent: {spec['receipt']}"
    got = sha256_file(p)
    if got != spec["receipt_sha256"]:
        return False, f"receipt sha256={got[:12]} pinned={spec['receipt_sha256'][:12]}"
    lines = [l for l in p.read_text().splitlines() if SUMMARY.match(l)]
    if len(lines) != 1:
        return False, f"receipt summary lines={len(lines)} (want exactly one cases= line)"
    m = SUMMARY.match(lines[0])
    if m.group(4) != "0" or int(m.group(2)) < 1:
        return False, f"receipt summary not green: {lines[0]}"
    if lines[0] not in entry:
        return False, "entry does not quote the receipt summary verbatim"
    return True, f"receipt sha256={got[:12]} {lines[0]}"


def p3_provenance(root, spec, entry):
    if not entry:
        return False, f"entry absent: {spec['entry']}"
    head = entry.splitlines()
    ids = list(spec["rows"])
    cuts = len(head) - 2
    for i, rid in enumerate(ids):
        row = spec["rows"][rid]
        url = spec["raw_base"] + row["upstream"]
        if i >= cuts or not head[i].startswith(f"source: {rid} ") or url not in head[i]:
            return False, f"line {i + 1} is not the {rid} source line with pinned URL {url}"
    n = len(ids)
    if head[n] != f"verified-at: {spec['entry_rules']['verified_at']}":
        return False, f"line {n + 1} is not verified-at: {spec['entry_rules']['verified_at']}"
    if not re.match(r"recheck: (\d+d|\d{4}-\d{2}-\d{2}|on-release)\b", head[n + 1]):
        return False, "recheck line lacks a date or cadence"
    return True, f"sources={','.join(ids)} verified-at={spec['entry_rules']['verified_at']}"


def p4_negative(_root, _spec, entry):
    if not entry:
        return False, "entry absent"
    neg = section(entry, "Negative space")
    if neg is None:
        return False, "no `## Negative space` section"
    if "falsif" not in neg.lower():
        return False, "negative space carries no falsifier"
    return True, f"negative_space_words={len(neg.split())} falsifier=yes"


def p5_quotes(root, spec, entry):
    cap = root / spec["capture_dir"]
    known = {row["capture"]: row for row in spec["rows"].values()}
    rows, unparsed, err = quote_table(entry)
    if err:
        return False, err
    if unparsed:
        return False, f"unparsed_rows={unparsed} of {unparsed + len(rows)}"
    lo, hi = spec["entry_rules"]["quote_words"]
    quotes, locs, short = set(), set(), []
    for m in rows:
        quote, name, a = m.group(1), m.group(2), int(m.group(3))
        b = int(m.group(4) or m.group(3))
        words = len(quote.split())
        if not lo <= words <= hi:
            short.append(f"{quote[:24]!r}={words}w")
            continue
        if name not in known:
            return False, f"quote cites unknown capture {name!r}"
        src = cap / name
        if not src.is_file():
            return False, f"quote cites missing capture {name}"
        span = "\n".join(src.read_text(errors="replace").splitlines()[a - 1:b])
        if quote not in span:
            return False, f"quote not on {name}:{a}-{b}: {quote[:40]!r}"
        quotes.add(quote)
        locs.add((name, a))
    if short:
        return False, f"{len(short)} quote(s) outside {lo}..{hi} words: {','.join(short[:3])}"
    need = spec["entry_rules"]["min_quotes"]
    if len(quotes) < need or len(locs) < spec["entry_rules"]["min_distinct_locations"]:
        return False, f"distinct_quotes={len(quotes)} distinct_lines={len(locs)} (want >= {need})"
    return True, f"rows={len(rows)} distinct_quotes={len(quotes)} distinct_lines={len(locs)}"


def p6_sources(root, spec, _entry):
    text = (root / spec["sources"]).read_text()
    lines = text.splitlines()
    teaches, short = [], []
    want = spec["entry_rules"]["min_teaches_words"]
    for rid, row in spec["rows"].items():
        hits = [l for l in lines if (m := SOURCES_ROW.match(l)) and m.group(1) == rid]
        if len(hits) != 1:
            return False, f"{rid} present {len(hits)} times"
        cells = [c.strip() for c in hits[0].strip().strip("|").split("|")]
        if len(cells) != 11:
            return False, f"{rid} has {len(cells)} cells"
        urls = re.findall(r"https?://\S+", cells[1])
        if urls != [spec["raw_base"] + row["upstream"]]:
            return False, f"{rid} source URL {urls} != pinned"
        if cells[3] != spec["entry_rules"]["row_tier"] or cells[7] != spec["entry_rules"]["row_status"]:
            return False, f"{rid} tier/status = {cells[3]}/{cells[7]}"
        if cells[8] != spec["entry_rules"]["row_opened"]:
            return False, f"{rid} opened = {cells[8]}"
        if cells[10] != spec["entry"]:
            return False, f"{rid} used-by {cells[10]!r} != entry"
        for idx, label in ((4, "scope"), (6, "teaches")):
            if len(cells[idx].split()) < want:
                short.append(f"{rid}.{label}={len(cells[idx].split())}w")
        teaches.append(cells[6])
    if short:
        return False, f"cells under {want} words: {','.join(short)}"
    if len(set(teaches)) != len(teaches):
        return False, "teaches cells are not pairwise distinct"
    return True, f"rows={len(teaches)} cells=11 teaches_min={min(len(t.split()) for t in teaches)}w"


def p7_captures(root, spec, _entry):
    cap = root / spec["capture_dir"]
    man = cap / CAPTURE_MANIFEST
    if not man.is_file():
        return False, f"capture manifest absent: {spec['capture_dir']}/{CAPTURE_MANIFEST}"
    pinned, bad = {}, []
    for line in man.read_text().splitlines():
        if not line.strip():
            continue
        m = MANIFEST_LINE.match(line)
        if not m:
            return False, f"unparsed manifest line: {line[:60]!r}"
        pinned[pathlib.Path(m.group(2).strip()).name] = m.group(1)
    for name, digest in pinned.items():
        p = cap / name
        if not p.is_file() or sha256_file(p) != digest:
            bad.append(name)
    unpinned = sorted(p.name for p in cap.iterdir() if p.is_file() and p.name not in pinned
                      and p.name != CAPTURE_MANIFEST)
    if unpinned:
        bad.append("unpinned:" + ",".join(unpinned))
    for rid, row in spec["rows"].items():
        if pinned.get(row["capture"]) != row["sha256"]:
            bad.append(f"{rid}:{row['capture']}")
    if bad:
        return False, f"capture defects={','.join(bad)}"
    return True, f"pinned_captures={len(pinned)} manifest={CAPTURE_MANIFEST}"


def p8_readme(root, spec, _entry):
    readme = (root / spec["readme"]).read_text()
    rel = spec["entry"].removeprefix("corpus/")
    idx = [l for l in readme.splitlines() if l.startswith(f"| `{rel}` |")]
    if len(idx) != 1:
        return False, f"index rows for {rel} = {len(idx)}"
    missing = [rid for rid in spec["rows"] if rid not in idx[0]]
    if missing:
        return False, f"index row omits {','.join(missing)}"
    cov = section(readme, "Coverage map")
    if cov is None or rel not in cov:
        return False, "coverage-map bullet absent"
    files = sorted((root / "corpus/knowledge").glob("*.md"))
    nidx = sum(1 for l in readme.splitlines() if l.startswith("| `knowledge/"))
    if len(files) != nidx:
        return False, f"knowledge files={len(files)} index rows={nidx}"
    return True, f"index_rows={nidx} knowledge_files={len(files)}"


def p9_clean(root):
    r = subprocess.run(["git", "-C", str(root), "ls-files", "--others", "--exclude-standard"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return False, f"git ls-files failed: {r.stderr.strip()[:60]}"
    left = [x for x in r.stdout.split("\n") if x]
    return (not left, f"untracked={len(left)}" + (f" e.g. {left[0]}" if left else ""))


def p10_rerun(root, spec):
    receipt = (root / spec["receipt"]).read_text()
    probe = spec["probe_cmd"]
    script = str(root / probe[0])
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    cmd = [sys.executable, script, *probe[1:]]
    r = subprocess.run(cmd, cwd=root, capture_output=True, text=True, env=env, timeout=900)
    if r.returncode != 0:
        cmd = ["uv", "run", *PROBE_TOOLCHAIN, "python3", script, *probe[1:]]
        r = subprocess.run(cmd, cwd=root, capture_output=True, text=True, env=env, timeout=900)
    if r.returncode != 0:
        return False, f"probe exit {r.returncode}: {(r.stderr or r.stdout).strip().splitlines()[-1:]!r}"
    if r.stdout != receipt:
        return False, f"fresh probe output differs from receipt (exit {r.returncode})"
    return True, f"rerun exit 0 bytes={len(r.stdout)}"


PACKAGE = [("P1", p1_frozen), ("P2", p2_receipt), ("P3", p3_provenance), ("P4", p4_negative),
           ("P5", p5_quotes), ("P6", p6_sources), ("P7", p7_captures), ("P8", p8_readme)]


# ---- line checks --------------------------------------------------------------------------------

def one_labelled_line(text, label, tag):
    hits = [l for l in text.splitlines() if l.startswith(label)]
    if len(hits) != 1:
        return None, f"{tag} DEFECT labelled_lines={len(hits)} want 1"
    return hits[0], None


def d4_check(path, spec):
    if not path.is_file():
        return False, f"file absent: {path.name}"
    line, err = one_labelled_line(path.read_text(), spec["d4"]["label"], "D4")
    if err:
        return False, err
    for pat in spec["d4"]["patterns"]:
        if not re.search(pat, line):
            return False, f"directional pattern absent near its citation: {pat[:36]}"
    return True, f"citation_tokens={len(spec['d4']['patterns'])} directional"


def d5_check(path, spec, capdir):
    if not path.is_file():
        return False, f"file absent: {path.name}"
    d5 = spec["d5"]
    line, err = one_labelled_line(path.read_text(), d5["label"], "D5")
    if err:
        return False, err
    if d5["require"] not in line:
        return False, f"erratum lacks {d5['require']!r}"
    if d5["forbid"] in line:
        return False, f"erratum says {d5['forbid']!r}"
    cap = capdir / d5["capture_name"]
    if not cap.is_file():
        return False, f"capture absent: {d5['capture_name']}"
    if d5["quote"] not in cap.read_text(errors="replace"):
        return False, "quote not verbatim in the cited capture"
    man = capdir / d5["manifest_name"]
    if not man.is_file():
        return False, f"manifest absent: {d5['manifest_name']}"
    digests = [m.group(1) for l in man.read_text().splitlines()
               if (m := MANIFEST_LINE.match(l)) and pathlib.Path(m.group(2).strip()).name == d5["capture_name"]]
    if len(digests) != 1:
        return False, f"manifest entries for capture={len(digests)}"
    got = sha256_file(cap)
    if got != digests[0]:
        return False, f"capture sha256={got[:12]} manifest={digests[0][:12]}"
    return True, f"capture_sha256={got[:12]} quote_verbatim=yes"


# ---- driver -------------------------------------------------------------------------------------

def load_spec(path):
    try:
        spec = json.loads(pathlib.Path(path).read_text())
    except (OSError, ValueError) as e:
        print(f"GATE setup error: cannot read spec {path}: {e}", file=sys.stderr)
        raise SystemExit(2)
    try:
        spec["rows"], spec["entry"], spec["capture_dir"], spec["receipt"]
        spec["entry_rules"], spec["frozen_instruments"]
    except KeyError as e:
        print(f"GATE setup error: spec lacks {e}", file=sys.stderr)
        raise SystemExit(2)
    return spec


def main(argv):
    ap = argparse.ArgumentParser(description="hardened package gate")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("package")
    p.add_argument("--root", required=True)
    p.add_argument("--spec", required=True)
    p.add_argument("--require-clean-tree", action="store_true")
    p.add_argument("--rerun", action="store_true")
    d4 = sub.add_parser("d4-line")
    d4.add_argument("--file", required=True)
    d4.add_argument("--spec", required=True)
    d5 = sub.add_parser("d5-line")
    d5.add_argument("--file", required=True)
    d5.add_argument("--capture-dir", required=True)
    d5.add_argument("--spec", required=True)
    a = ap.parse_args(argv)
    spec = load_spec(a.spec)

    if a.cmd == "d4-line":
        ok, note = d4_check(pathlib.Path(a.file), spec)
        print(f"D4 {'ok' if ok else 'DEFECT'} {note}")
        print(f"defects={0 if ok else 1}")
        return 0 if ok else 1
    if a.cmd == "d5-line":
        ok, note = d5_check(pathlib.Path(a.file), spec, pathlib.Path(a.capture_dir))
        print(f"D5 {'ok' if ok else 'DEFECT'} {note}")
        print(f"defects={0 if ok else 1}")
        return 0 if ok else 1

    root = pathlib.Path(a.root)
    if not root.is_dir():
        print(f"GATE setup error: root not a directory: {root}", file=sys.stderr)
        return 2
    entry_path = root / spec["entry"]
    entry = entry_path.read_text() if entry_path.is_file() else ""
    defects = 0
    for tag, fn in PACKAGE:
        try:
            ok, note = fn(root, spec, entry)
        except (OSError, ValueError) as e:
            ok, note = False, f"error {type(e).__name__}: {e}"
        print(f"{tag} {'ok' if ok else 'DEFECT'} {note}")
        defects += not ok
    for tag, flag, fn in (("P9", a.require_clean_tree, lambda: p9_clean(root)),
                          ("P10", a.rerun, lambda: p10_rerun(root, spec))):
        try:
            ok, note = fn() if flag else (True, "not-requested")
        except (OSError, ValueError, subprocess.SubprocessError) as e:
            ok, note = False, f"error {type(e).__name__}: {e}"
        print(f"{tag} {'ok' if ok else 'DEFECT'} {note}")
        defects += not ok
    print(f"defects={defects}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SystemExit:
        raise
    except BaseException as e:  # a crash is setup error 2, never an accept or a reject
        print(f"GATE error {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
