#!/usr/bin/env python3
"""Hardened package gate for one kengaku knowledge package (round 36, C1 candidate).

  package --root DIR --spec SPEC [--require-clean-tree] [--rerun]
  d4-line --file F --spec SPEC
  d5-line --file F --capture-dir D --spec SPEC
exit 0 = accept, 1 = reject, 2 = usage/setup (an unexpected crash never maps onto 0 or 1).

Every clause is spec-driven: paths, digests, row ids, tier, status, quote bounds, labels and
directional tokens come from --spec. The gate never asks what the caller calls its fixture and
never inspects a path for a fixture marker. Parsing happens once into `Package`; each clause is a
read-only check over that parsed state. An unparsed row, a manifest line that fails its own digest,
a quote not verbatim on its cited line, and a receipt a fresh run does not reproduce are defects.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import pathlib
import re
import subprocess
import sys

QUOTE_SECTION = re.compile(r"^## Located quotes\n(.*?)(?=^## |\Z)", re.S | re.M)
QUOTE_ROW = re.compile(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$")
SOURCE_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
INDEX_ROW = re.compile(r"^\|\s*`(knowledge/[^`]+\.md)`\s*\|")
URL = re.compile(r"https?://\S+")
MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})\s+\*?(\S+?)\*?$")

def sha256(path):
    try: return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError: return None

def read(path):
    try: return path.read_text()
    except (OSError, UnicodeDecodeError): return None

@dataclasses.dataclass(frozen=True)
class Quote:
    claim: str
    text: str
    capture: str
    start: int
    end: int

    @property
    def words(self):
        return len(self.text.split())

@dataclasses.dataclass
class Package:
    """Everything the clauses read, parsed once from the tree under test."""

    root: pathlib.Path
    spec: dict
    entry: str | None = None
    quote_section: str | None = None
    quotes: list[Quote] = dataclasses.field(default_factory=list)
    bad_rows: list[str] = dataclasses.field(default_factory=list)
    sources: dict[str, list[list[str]]] = dataclasses.field(default_factory=dict)
    readme: str | None = None
    _captures: dict[str, list[str] | None] = dataclasses.field(default_factory=dict)

    @classmethod
    def load(cls, root, spec):
        pkg = cls(root=root, spec=spec)
        pkg.entry = read(root / spec["entry"])
        pkg.readme = read(root / spec["readme"])
        pkg._parse_quotes()
        pkg._parse_sources()
        return pkg

    def _parse_quotes(self):
        if self.entry is None:
            return
        m = QUOTE_SECTION.search(self.entry)
        if not m:
            return
        self.quote_section = m.group(1)
        rows = [l for l in m.group(1).splitlines()
                if l.startswith("|") and not re.match(r"^\|[\s|:-]+\|$", l)]
        for line in rows[1:]:  # rows[0] is the header
            q = QUOTE_ROW.match(line)
            if not q:
                self.bad_rows.append(line.strip())
                continue
            start = int(q.group(3))
            end = int(q.group(4)) if q.group(4) else start
            self.quotes.append(Quote(line.split("|")[1].strip(), q.group(1), q.group(2), start, end))

    def _parse_sources(self):
        for line in (read(self.root / self.spec["sources"]) or "").splitlines():
            m = SOURCE_ROW.match(line)
            if m:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                self.sources.setdefault(m.group(1), []).append(cells)

    def capture(self, name):
        """Lines of a capture under the spec's capture dir; None when unreadable or unsafe."""
        if name not in self._captures:
            rel = pathlib.PurePosixPath(name)
            safe = bool(rel.parts) and not rel.is_absolute() and ".." not in rel.parts
            text = read(self.root / self.spec["capture_dir"] / name) if safe else None
            self._captures[name] = text.splitlines() if text is not None else None
        return self._captures[name]

# ---- clauses over the parsed package -----------------------------------------------------------

def c_instruments(p):
    pins = p.spec.get("frozen_instruments", {})
    bad = [rel for rel, dig in pins.items() if sha256(p.root / rel) != dig]
    return bool(pins) and not bad, f"pinned={len(pins)} mismatched={bad or 0}"

def c_receipt(p):
    got, want = sha256(p.root / p.spec["receipt"]), p.spec["receipt_sha256"]
    if got is None:
        return False, f"receipt unreadable: {p.spec['receipt']}"
    return got == want, f"receipt_sha256={'pinned' if got == want else got}"

def c_quote_shape(p):
    rules = p.spec["entry_rules"]
    lo, hi = rules["quote_words"]
    if p.quote_section is None:
        return False, "no '## Located quotes' section"
    if p.bad_rows:
        return False, f"unparsed_rows={len(p.bad_rows)} first={p.bad_rows[0][:70]!r}"
    short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]
    texts = {q.text for q in p.quotes}
    locs = {(q.capture, q.start) for q in p.quotes}
    ok = len(texts) >= rules["min_quotes"] and len(locs) >= rules["min_distinct_locations"] \
        and not short
    return ok, (f"rows={len(p.quotes)} distinct_quotes={len(texts)} distinct_lines={len(locs)} "
                f"out_of_word_range={len(short)}")

def c_quote_verbatim(p):
    if not p.quotes:
        return False, "no parsed quote"
    bad = []
    for q in p.quotes:
        lines = p.capture(q.capture)
        if lines is None:
            bad.append(f"{q.capture}: unreadable capture")
        elif q.start > q.end or q.end > len(lines):
            bad.append(f"{q.capture}:{q.start}-{q.end}: line range outside the capture")
        elif q.text not in "\n".join(lines[q.start - 1:q.end]):
            bad.append(f"{q.capture}:{q.start}: quote not verbatim there")
    return not bad, f"checked={len(p.quotes)} bad={len(bad)} first={bad[0] if bad else 0}"

def c_captures(p):
    capdir = p.root / p.spec["capture_dir"]
    text = read(capdir / "SHA256SUMS")
    if text is None:
        return False, f"capture manifest absent: {p.spec['capture_dir']}/SHA256SUMS"
    pinned, bad = {}, []
    for line in text.splitlines():
        if not line.strip():
            continue
        m = MANIFEST_LINE.match(line.strip())
        if not m:
            bad.append(f"unparsed manifest line {line.strip()[:50]!r}")
            continue
        digest, name = m.group(1), m.group(2)
        pinned[name] = digest
        if sha256(capdir / name) != digest:
            bad.append(f"{name}: manifest digest does not match the bytes")
    for sid, row in p.spec["rows"].items():
        name = row["capture"]
        if name not in pinned:
            bad.append(f"{sid}: capture {name} is not pinned in the manifest")
        elif pinned[name] != row["sha256"]:
            bad.append(f"{sid}: manifest digest differs from the spec pin")
    for name in {q.capture for q in p.quotes}:
        if name not in pinned:
            bad.append(f"quote capture {name} is not pinned in the manifest")
    for f in sorted(capdir.iterdir()):
        if f.is_file() and not f.name.startswith(".") and f.name != "SHA256SUMS" \
                and f.name not in pinned:
            bad.append(f"{f.name}: capture file not covered by the manifest")
    return not bad, f"manifest_entries={len(pinned)} bad={len(bad)} first={bad[0] if bad else 0}"

def c_sources(p):
    rules, bad, teaches = p.spec["entry_rules"], [], []
    for sid, row in p.spec["rows"].items():
        found = p.sources.get(sid, [])
        if len(found) != 1:
            bad.append(f"{sid}: rows={len(found)}")
            continue
        cells = found[0]
        if len(cells) != 11:
            bad.append(f"{sid}: cells={len(cells)}")
            continue
        url = URL.search(cells[1])
        if not url or url.group(0) != p.spec["raw_base"] + row["upstream"]:
            bad.append(f"{sid}: url not the pinned raw path")
        if cells[3] != rules["row_tier"]:
            bad.append(f"{sid}: tier={cells[3]!r}")
        if cells[7] != rules["row_status"]:
            bad.append(f"{sid}: status={cells[7]!r}")
        if p.spec["entry"] not in cells[10]:
            bad.append(f"{sid}: used-by is not the entry")
        if len(cells[6].split()) < rules["min_teaches_words"]:
            bad.append(f"{sid}: teaches words={len(cells[6].split())}")
        teaches.append(cells[6].lower())
    if len(set(teaches)) != len(teaches):
        bad.append("teaches cells are not pairwise distinct")
    return not bad, f"rows={len(p.spec['rows'])} bad={len(bad)} first={bad[0] if bad else 0}"

def c_provenance(p):
    if p.entry is None:
        return False, "entry unreadable"
    rules, bad, prov = p.spec["entry_rules"], [], {}
    for line in p.entry.splitlines():
        m = re.match(r"^source:\s*(S\d{3,})\b.*?(https?://\S+)", line)
        if m:
            prov.setdefault(m.group(1), []).append(m.group(2))
    for sid, row in p.spec["rows"].items():
        if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:
            bad.append(f"{sid}: source line {'absent' if sid not in prov else 'not the pinned url'}")
    if f"verified-at: {rules['verified_at']}" not in p.entry:
        bad.append("verified-at line absent or not the frozen date")
    if not re.search(r"^recheck:\s*\S", p.entry, re.M):
        bad.append("recheck line absent")
    m = re.search(r"^## Negative space\n(.*?)(?=^## |\Z)", p.entry, re.S | re.M)
    if not m or not m.group(1).strip():
        bad.append("no '## Negative space' section")
    elif not re.search(r"(?i)falsifi(?:er|ed|es|ability)", m.group(1)):
        bad.append("'## Negative space' carries no falsifier")
    return not bad, f"source_lines={len(prov)} bad={len(bad)} first={bad[0] if bad else 0}"

def c_readme(p):
    if p.readme is None:
        return False, "README unreadable"
    bad, index = [], {}
    for line in p.readme.splitlines():
        m = INDEX_ROW.match(line)
        if m:
            index.setdefault(m.group(1), []).append(line)
    entry_name = pathlib.PurePosixPath(p.spec["entry"]).name
    rows = index.get("knowledge/" + entry_name, [])
    if len(rows) != 1:
        bad.append(f"index rows for knowledge/{entry_name}={len(rows)}")
    elif not all(sid in rows[0] for sid in p.spec["rows"]):
        bad.append("index row does not cite every registry row")
    receipt_rel = p.spec["receipt"].split("/", 1)[1]
    bullet = [l for l in p.readme.splitlines()
              if l.startswith("- ") and entry_name in l and receipt_rel in l]
    if not bullet:
        bad.append("no coverage bullet naming the entry and its receipt")
    files = {f.name for f in p.root.glob(p.spec["knowledge_glob"])}
    indexed = {pathlib.PurePosixPath(k).name for k in index}
    if files != indexed:
        bad.append(f"knowledge files={len(files)} index rows={len(indexed)}")
    note = f"index_rows={len(indexed)} knowledge_files={len(files)}"
    return not bad, f"{note} bad={len(bad)} first={bad[0] if bad else 0}"

def c_clean_tree(p):
    r = subprocess.run(["git", "-C", str(p.root), "ls-files", "--others", "--exclude-standard"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return False, "root is not a readable git worktree"
    left = [x for x in r.stdout.splitlines() if x]
    return not left, f"untracked={len(left)} first={left[0] if left else 0}"

def c_rerun(p):
    want = read(p.root / p.spec["receipt"])
    if want is None:
        return False, "receipt unreadable"
    probe = list(p.spec["probe_cmd"])
    try:
        import Bio  # noqa: F401  (the pinned grader's dependency; host python when available)
        cmd = [sys.executable] + probe
    except ImportError:
        cmd = ["uv", "run", "--no-project", "--with", "biopython==1.85", "python3"] + probe
    try:
        r = subprocess.run(cmd, cwd=str(p.root), capture_output=True, text=True, timeout=600)
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"probe could not be re-run: {type(e).__name__}"
    if r.returncode != 0:
        return False, f"fresh probe exit={r.returncode} stderr={r.stderr.strip()[:80]!r}"
    if r.stdout != want:
        return False, "fresh probe output is not byte-equal to the receipt"
    return True, f"probe_rerun=byte-equal bytes={len(want)}"

PACKAGE_CHECKS = (("P1", c_instruments), ("P2", c_receipt), ("P3", c_quote_shape),
                  ("P4", c_quote_verbatim), ("P5", c_captures), ("P6", c_sources),
                  ("P7", c_provenance), ("P8", c_readme), ("P9", c_clean_tree), ("P10", c_rerun))

# ---- subcommands -------------------------------------------------------------------------------

def run_checks(checks):
    defects = 0
    for name, fn in checks:
        try:
            ok, note = fn()
        except Exception as e:  # a clause that cannot run is a defect, never a pass
            ok, note = False, f"clause error {type(e).__name__}: {e}"
        defects += not ok
        print(f"{name} {'ok' if ok else 'DEFECT'} {note}")
    print(f"defects={defects}")
    return defects

def cmd_package(args, spec):
    pkg = Package.load(args.root, spec)
    wanted = [(n, f) for n, f in PACKAGE_CHECKS
              if (n != "P9" or args.require_clean_tree) and (n != "P10" or args.rerun)]
    return run_checks([(n, lambda f=f: f(pkg)) for n, f in wanted])

def single_line(path):
    text = read(path)
    return None if text is None else [l for l in text.splitlines() if l.strip()]

def cmd_d4(args, spec):
    def check():
        lines = single_line(args.file)
        if lines is None:
            return False, "file unreadable"
        if len(lines) != 1 or not lines[0].startswith(spec["d4"]["label"]):
            return False, f"line_count={len(lines)} labelled=False"
        bad = [f"pattern{i}" for i, pat in enumerate(spec["d4"]["patterns"], 1)
               if not re.search(pat, lines[0])]
        return not bad, f"patterns={len(spec['d4']['patterns'])} failed={bad or 0}"
    return run_checks([("D4", check)])

def cmd_d5(args, spec):
    d5 = spec["d5"]

    def check():
        lines = single_line(args.file)
        if lines is None:
            return False, "file unreadable"
        if len(lines) != 1 or not lines[0].startswith(d5["label"]):
            return False, f"line_count={len(lines)} labelled=False"
        line, bad = lines[0], []
        if d5["require"] not in line:
            bad.append(f"missing {d5['require']!r}")
        if d5["forbid"] in line:
            bad.append(f"carries {d5['forbid']!r}")
        capdir = pathlib.Path(args.capture_dir)
        capture = capdir / d5["capture_name"]
        digest = sha256(capture)
        if digest is None:
            return False, "capture unreadable"
        sums = read(capdir / d5["manifest_name"]) or ""
        pinned = any(len(parts) >= 2 and parts[0] == digest
                     and parts[-1].endswith(d5["capture_name"])
                     for parts in (row.split() for row in sums.splitlines()))
        if not pinned:
            bad.append("capture digest is not the one in the manifest")
        flat = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", read(capture) or ""))
        if re.sub(r"\s+", "", d5["quote"]) not in flat:
            bad.append("quote absent from the capture")
        return not bad, f"directional={not bad} digest_pinned={pinned} bad={bad or 0}"
    return run_checks([("D5", check)])

def main(argv=None):
    ap = argparse.ArgumentParser(description="hardened kengaku package gate")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pp = sub.add_parser("package")
    pp.add_argument("--root", default=".")
    pp.add_argument("--spec", required=True)
    pp.add_argument("--require-clean-tree", action="store_true")
    pp.add_argument("--rerun", action="store_true")
    pd4 = sub.add_parser("d4-line")
    pd4.add_argument("--file", required=True)
    pd4.add_argument("--spec", required=True)
    pd5 = sub.add_parser("d5-line")
    pd5.add_argument("--file", required=True)
    pd5.add_argument("--capture-dir", required=True)
    pd5.add_argument("--spec", required=True)
    args = ap.parse_args(argv)
    try:
        args.root = pathlib.Path(getattr(args, "root", ".")).resolve()
        if getattr(args, "file", None):
            args.file = pathlib.Path(args.file).resolve()
        spec_path = pathlib.Path(args.spec)
        if not spec_path.is_file():
            print(f"setup: spec not found: {spec_path}", file=sys.stderr)
            return 2
        spec = json.loads(spec_path.read_text())
        if args.cmd == "package":
            if not args.root.is_dir():
                print(f"setup: root not a directory: {args.root}", file=sys.stderr)
                return 2
            return 0 if cmd_package(args, spec) == 0 else 1
        if args.cmd == "d4-line":
            return 0 if cmd_d4(args, spec) == 0 else 1
        return 0 if cmd_d5(args, spec) == 0 else 1
    except SystemExit:
        raise
    except Exception as e:  # an unexpected crash is never accept or reject
        print(f"setup: {type(e).__name__}: {e}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
