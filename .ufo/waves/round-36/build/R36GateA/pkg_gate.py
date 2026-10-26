#!/usr/bin/env python3
"""Hardened package gate (round-36 C1): judge a corpus package against plans/pkg-spec-r35.json.

  package --root DIR [--require-clean-tree] [--rerun] --spec SPEC
  d4-line --file F --spec SPEC
  d5-line --file F --capture-dir D --spec SPEC
One `P<n> ok|DEFECT <reason>` line per package check, one `D4`/`D5` line per line check, then
`defects=<n>`.  Exit 0 accept, 1 reject, 2 usage/setup (a crash is never exit 0 or 1); a check whose
enabling flag is absent prints `P<n> skipped (...)`, never a false `ok`.  Every rule comes from the
spec: no fixture id, path suffix or marker string is special-cased, so a renamed copy or a rewritten
package is judged by the same clauses.
"""
import argparse
import hashlib
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys

QUOTE_RE = re.compile(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$")
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SEP_RE = re.compile(r"^\|[\s|:-]+\|$")
MANIFEST_RE = re.compile(r"([0-9a-f]{64})\s+\*?(\S+)")
SECT = r"^## %s\n(.*?)(?=^## |\Z)"


class Setup(Exception):
    """Usage/setup error: exit 2, never a verdict."""


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def section(text, title):
    return re.search(SECT % re.escape(title), text, re.S | re.M)


def manifest(path):
    """{basename: digest} from a SHA256SUMS file, or None on an unparsed or ambiguous line."""
    out = {}
    for line in path.read_text(errors="replace").splitlines():
        if not line.strip():
            continue
        m = MANIFEST_RE.fullmatch(line.strip())
        if not m:
            return None
        name = pathlib.PurePosixPath(m.group(2)).name
        if out.setdefault(name, m.group(1)) != m.group(1):
            return None
    return out


def p1_frozen_instruments(root, spec, _a):
    """Every frozen instrument still hashes to the pinned digest (a stub probe dies here)."""
    bad = []
    for rel, pin in spec["frozen_instruments"].items():
        f = root / rel
        if not f.is_file() or sha(f) != pin:
            bad.append(f"{rel}=" + ("missing" if not f.is_file() else "changed"))
    return not bad, f"pinned={len(spec['frozen_instruments'])} " + (",".join(bad) or "all-match")


def p2_receipt(root, spec, _a):
    """The receipt is byte-pinned: a hand-typed receipt cannot carry the pinned digest."""
    f = root / spec["receipt"]
    if not f.is_file():
        return False, "receipt missing"
    got = sha(f)
    want = spec["receipt_sha256"]
    return got == want, f"receipt={'match' if got == want else got[:12] + '!=' + want[:12]}"


def p3_quotes(root, spec, _a):
    """Every row parses, quotes are 3..25 words, >=N distinct at >=N lines, each verbatim."""
    entry = root / spec["entry"]
    if not entry.is_file():
        return False, "entry missing"
    sec = section(entry.read_text(), "Located quotes")
    if not sec:
        return False, "no '## Located quotes' section"
    rows = [l for l in sec.group(1).splitlines() if l.startswith("|") and not SEP_RE.match(l)]
    if len(rows) < 2:
        return False, "quote table absent"
    cap = (root / spec["capture_dir"]).resolve()
    lo, hi = spec["entry_rules"]["quote_words"]
    quotes, locs = set(), set()
    for i, line in enumerate(rows[1:], 1):
        m = QUOTE_RE.match(line)
        if not m:
            return False, f"unparsed quote row {i}: {line[:50]}"
        text, name, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
        if not lo <= len(text.split()) <= hi:
            return False, f"quote of {len(text.split())} words at row {i}"
        f = (cap / name).resolve()
        if f != cap and cap not in f.parents:
            return False, f"capture escapes dir: {name}"
        if not f.is_file():
            return False, f"missing capture {name}"
        lines = f.read_text(errors="replace").splitlines()
        if not 1 <= a <= b <= len(lines):
            return False, f"range off the capture: {name}:{a}-{b}"
        if text not in "\n".join(lines[a - 1:b]):
            return False, f"not verbatim on {name}:{a}-{b}: {text[:40]}"
        quotes.add(text)
        locs.add((name, a, b))
    r, n = spec["entry_rules"], len(rows) - 1
    ok = n >= r["min_quotes"] and len(quotes) >= r["min_quotes"] and len(locs) >= r["min_distinct_locations"]
    return ok, f"rows={n} distinct_quotes={len(quotes)} distinct_locations={len(locs)}"


def p4_captures(root, spec, _a):
    """The capture manifest is pinned: every listed file hashes to it and every row's digest agrees."""
    d = root / spec["capture_dir"]
    sums = d / "SHA256SUMS"
    if not sums.is_file():
        return False, "capture SHA256SUMS missing"
    listed = manifest(sums)
    if listed is None:
        return False, "unparsed SHA256SUMS line"
    bad = [f"{n}=changed" for n, dig in listed.items()
           if not (d / n).is_file() or sha(d / n) != dig]
    for rid, row in spec["rows"].items():
        if listed.get(row["capture"]) != row["sha256"]:
            bad.append(f"{rid}=unpinned")
        elif not (d / row["capture"]).is_file() or sha(d / row["capture"]) != row["sha256"]:
            bad.append(f"{rid}=digest")
    return not bad, f"manifest_entries={len(listed)} " + (",".join(bad) or "all-pinned")


def p5_sources(root, spec, _a):
    """Rows S*** exist once, 11 cells, tier/status/opened/used-by, pinned URL+digest, >=8-word
    teaches, teaches pairwise distinct."""
    p = root / spec["sources"]
    if not p.is_file():
        return False, "SOURCES missing"
    rows = {}
    for line in p.read_text(errors="replace").splitlines():
        m = ROW_RE.match(line)
        if m:
            rows.setdefault(m.group(1), []).append(line)
    rules, errs, teaches = spec["entry_rules"], [], set()
    for rid, row in spec["rows"].items():
        got = rows.get(rid, [])
        if len(got) != 1:
            errs.append(f"{rid}:count={len(got)}")
            continue
        cells = [c.strip() for c in got[0].strip().strip("|").split("|")]
        if len(cells) != 11:
            errs.append(f"{rid}:cells={len(cells)}")
            continue
        _id, source, _kind, tier, _scope, anchor, teach, status, opened, _re, used = cells
        if re.findall(r"https?://\S+", source) != [spec["raw_base"] + row["upstream"]]:
            errs.append(f"{rid}:url")
        if tier != rules["row_tier"] or status != rules["row_status"] or opened != rules["row_opened"]:
            errs.append(f"{rid}:{tier}/{status}/{opened}")
        if used != spec["entry"]:
            errs.append(f"{rid}:used-by={used}")
        if row["sha256"] not in anchor:
            errs.append(f"{rid}:anchor-no-digest")
        if len(teach.split()) < rules["min_teaches_words"]:
            errs.append(f"{rid}:teaches={len(teach.split())}w")
        if teach in teaches:
            errs.append(f"{rid}:teaches-duplicate")
        teaches.add(teach)
    return not errs, f"rows={len(spec['rows'])} distinct_teaches={len(teaches)} " + (
        ",".join(errs) or "all-match")


def p6_provenance(root, spec, _a):
    """The entry head carries one `source:` line per row with its pinned URL, then verified-at and
    a recheck cadence."""
    f = root / spec["entry"]
    if not f.is_file():
        return False, "entry missing"
    head = f.read_text(errors="replace").splitlines()[:5]
    errs = []
    for i, (rid, row) in enumerate(spec["rows"].items()):
        if i >= len(head) or not head[i].startswith(f"source: {rid} ") \
                or spec["raw_base"] + row["upstream"] not in head[i]:
            errs.append(f"line{i + 1}!={rid}")
    if len(head) < 4 or head[3] != f"verified-at: {spec['entry_rules']['verified_at']}":
        errs.append("verified-at")
    if len(head) < 5 or not re.match(r"recheck: (\d{4}-\d{2}-\d{2}|\d+d|on-release)\b", head[4]):
        errs.append("recheck")
    return not errs, f"sources={len(spec['rows'])} " + (",".join(errs) or "trio+verified-at+recheck")


def p7_negative_space(root, spec, _a):
    """The entry names its negative space and carries a falsifier."""
    f = root / spec["entry"]
    if not f.is_file():
        return False, "entry missing"
    sec = section(f.read_text(errors="replace"), "Negative space")
    if not sec or not sec.group(1).strip():
        return False, "negative space absent or empty"
    has = re.search(r"(?i)falsif\w*.{0,200}?\b(if|when|differ\w*|changed?|fail\w*|refut\w*)\b",
                    sec.group(1), re.S)
    return bool(has), f"chars={len(sec.group(1).strip())} falsifier={'yes' if has else 'no'}"


def p8_index(root, spec, _a):
    """One README index row (naming every row id), a coverage bullet, and knowledge files == rows."""
    readme = root / spec["readme"]
    if not readme.is_file():
        return False, "README missing"
    lines = readme.read_text(errors="replace").splitlines()
    if "corpus/" not in spec["entry"]:
        return False, "entry is outside corpus/"
    rel = spec["entry"].split("corpus/", 1)[1]
    idx = [l for l in lines if l.startswith(f"| `{rel}` |")]
    errs = []
    if len(idx) != 1:
        errs.append(f"index_rows={len(idx)}")
    elif not all(rid in idx[0] for rid in spec["rows"]):
        errs.append("index-row-missing-a-row-id")
    cov = section("\n".join(lines), "Coverage map")
    if not cov or rel not in cov.group(1):
        errs.append("coverage-bullet")
    files = sorted(root.glob(spec["knowledge_glob"]))
    nidx = sum(1 for l in lines if l.startswith("| `knowledge/"))
    if len(files) != nidx:
        errs.append(f"knowledge_files={len(files)}!={nidx}_index_rows")
    return not errs, f"knowledge_files={len(files)} index_rows={nidx} " + (",".join(errs) or "parity")


def p9_clean_tree(root, _spec, _a):
    """--require-clean-tree: no untracked file under the root (D1's working-tree class)."""
    r = subprocess.run(["git", "-C", str(root), "ls-files", "--others", "--exclude-standard"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return False, f"git ls-files exit {r.returncode}"
    left = [x for x in r.stdout.splitlines() if x]
    return not left, f"untracked={len(left)}" + (f" first={left[0]}" if left else "")


def p10_rerun(root, spec, _a):
    """--rerun: the probe command reproduces the pinned receipt byte for byte, under the
    interpreter the receipt pins (`biopython=<v>` on its first line) when the gate's lacks it."""
    probe, receipt = root / spec["probe_cmd"][0], root / spec["receipt"]
    if not probe.is_file() or not receipt.is_file():
        return False, "probe or receipt missing"
    want = receipt.read_text(errors="replace")
    args = [str(probe), *spec["probe_cmd"][1:]]
    cmd = [sys.executable, *args]
    dep = re.search(r"\bbiopython=(\S+)", want.splitlines()[0] if want else "")
    if dep and importlib.util.find_spec("Bio") is None and shutil.which("uv"):
        cmd = ["uv", "run", "--no-project", "--with", f"biopython=={dep.group(1)}", "python3", *args]
    try:
        r = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True, timeout=300)
    except OSError as e:
        return False, f"probe not runnable: {e}"
    except subprocess.TimeoutExpired:
        return False, "probe timeout"
    if r.stdout != want:
        return False, f"receipt differs (probe={len(r.stdout)}B receipt={len(want)}B rc={r.returncode})"
    return True, f"byte-equal ({len(want)}B, rc={r.returncode}, runner={cmd[0].rsplit(chr(47), 1)[-1]})"


CLAUSES = [
    ("P1", p1_frozen_instruments, None),
    ("P2", p2_receipt, None),
    ("P3", p3_quotes, None),
    ("P4", p4_captures, None),
    ("P5", p5_sources, None),
    ("P6", p6_provenance, None),
    ("P7", p7_negative_space, None),
    ("P8", p8_index, None),
    ("P9", p9_clean_tree, "require_clean_tree"),
    ("P10", p10_rerun, "rerun"),
]


def d4_check(path, spec):
    """The D4 correction line: one labelled line, both citations pointing the right way (the draft's
    clean selftest, the harness's green-but-failing run), each pinned pattern present."""
    cand = [l for l in path.read_text(errors="replace").splitlines()
            if l.startswith(spec["d4"]["label"])]
    if len(cand) != 1:
        return False, f"labelled_lines={len(cand)}"
    pats = spec["d4"]["patterns"]
    missed = [i + 1 for i, p in enumerate(pats) if not re.search(p, cand[0])]
    return not missed, f"patterns={len(pats) - len(missed)}/{len(pats)}" + (
        f" missed={missed}" if missed else " directional-ok")


def d5_check(path, spec, capture_dir):
    """The D5 erratum line: one labelled line, the quote affirmed (`require`) and not negated
    (`forbid`), citing the capture, and the capture matches its manifest pin with the quote present."""
    d = spec["d5"]
    cand = [l for l in path.read_text(errors="replace").splitlines() if l.startswith(d["label"])]
    errs = []
    if len(cand) != 1:
        errs.append(f"labelled_lines={len(cand)}")
    else:
        line = cand[0]
        if d["require"] not in line:
            errs.append("require-phrase-absent")
        if d["forbid"] in line:
            errs.append("forbid-phrase-present")
        if d["capture_name"] not in line:
            errs.append("capture-not-cited")
    cap = pathlib.Path(capture_dir)
    f = cap / d["capture_name"]
    man = cap / d["manifest_name"]
    if not f.is_file():
        errs.append("capture-missing")
    if not man.is_file():
        errs.append("manifest-missing")
    elif f.is_file():
        listed = manifest(man)
        if listed is None or listed.get(d["capture_name"]) != sha(f):
            errs.append("capture-digest-unpinned")
    if f.is_file():
        norm = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", f.read_text(errors="replace")))
        if re.sub(r"\s+", "", d["quote"]) not in norm:
            errs.append("quote-absent")
    return not errs, ",".join(errs) or "label+direction+manifest-pin+quote"


def load_spec(raw):
    p = pathlib.Path(raw)
    if not p.is_file():
        raise Setup(f"spec missing: {p}")
    spec = json.loads(p.read_text())
    need = ("entry", "capture_dir", "receipt", "receipt_sha256", "probe_cmd", "sources", "readme",
            "knowledge_glob", "raw_base", "rows", "frozen_instruments", "entry_rules", "d4", "d5")
    missing = [k for k in need if k not in spec]
    if missing:
        raise Setup(f"spec lacks {missing}")
    return spec


def run_package(a):
    root = pathlib.Path(a.root).resolve()
    if not root.is_dir():
        raise Setup(f"root is not a directory: {root}")
    spec = load_spec(a.spec)
    defects = 0
    for pid, fn, flag in CLAUSES:
        if flag and not getattr(a, flag):
            print(f"{pid} skipped (--{flag.replace('_', '-')} absent)")
            continue
        try:
            ok, note = fn(root, spec, a)
        except Exception as e:  # a clause failure is a rejection, never a crash
            ok, note = False, f"error {type(e).__name__}: {e}"
        print(f"{pid} {'ok' if ok else 'DEFECT'} {note}")
        defects += not ok
    print(f"defects={defects}")
    return 0 if defects == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="hardened package gate (round-36 C1)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pkg = sub.add_parser("package")
    pkg.add_argument("--root", default=".")
    pkg.add_argument("--spec", required=True)
    pkg.add_argument("--require-clean-tree", action="store_true")
    pkg.add_argument("--rerun", action="store_true")
    d4 = sub.add_parser("d4-line")
    d4.add_argument("--file", required=True)
    d4.add_argument("--spec", required=True)
    d5 = sub.add_parser("d5-line")
    d5.add_argument("--file", required=True)
    d5.add_argument("--capture-dir", required=True)
    d5.add_argument("--spec", required=True)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "package":
            return run_package(a)
        spec = load_spec(a.spec)
        path = pathlib.Path(a.file)
        if not path.is_file():
            raise Setup(f"file missing: {path}")
        if a.cmd == "d4-line":
            ok, note = d4_check(path, spec)
            print(f"D4 {'ok' if ok else 'DEFECT'} {note}")
        else:
            ok, note = d5_check(path, spec, a.capture_dir)
            print(f"D5 {'ok' if ok else 'DEFECT'} {note}")
        print(f"defects={0 if ok else 1}")
        return 0 if ok else 1
    except Setup as e:
        print(f"setup: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # never exit 0/1 on a crash
        print(f"internal: {type(e).__name__}: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
