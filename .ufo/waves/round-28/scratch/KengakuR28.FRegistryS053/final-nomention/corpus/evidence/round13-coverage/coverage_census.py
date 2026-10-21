#!/usr/bin/env python3
"""Round-13 coverage census — read-only, revision-aware probe (not a gate).

Counts, for a git REV (tracked snapshot) or the working tree:
  * source markers: for the FIXED source candidates frozen in
    surface-receipt.json (delivered working-tree instrumentation; the
    baseline commit lacks it — never re-derived at measured revision),
    exact `source-status: historical-unavailable` occurrences within the
    first 24 lines.
  * index integrity: markdown files directly under corpus/knowledge and
    corpus/lessons and immediate dirs of corpus/evidence, discovered
    independently of the README, cross-checked against corpus/README.md
    first-column single-code-span table links (files/indexed, unindexed,
    dangling, duplicate rows per category, repo-relative paths).

No network, no live-host reads, no writes. Exit 0 = census completed even
with gaps; exit 2 = unreadable revision or required input.

  python3 corpus/evidence/round13-coverage/coverage_census.py [--revision REV]
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

MARKER = "source-status: historical-unavailable"
SCAN = 24
HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
RECEIPT_REL = "corpus/evidence/round13-coverage/surface-receipt.json"
README = "corpus/README.md"
CATS = {"knowledge": "corpus/knowledge", "lessons": "corpus/lessons",
        "evidence": "corpus/evidence"}
SCHEMA = "r13-coverage-census/1"


class CensusError(Exception):
    """Unreadable revision or required input -> exit 2."""


def git(repo, args):
    try:
        p = subprocess.run(("git", "-C", str(repo)) + tuple(args),
                           capture_output=True)
    except OSError as exc:
        raise CensusError("git executable unavailable: %s" % exc)
    return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace")


def benign_absent(text):
    low = text.lower()
    return ("not found" in low or "does not exist" in low or
            "exists on disk" in low or "not a tree" in low)


class Snapshot:
    """Working tree (label WORKTREE) or one verified git commit."""

    def __init__(self, revision):
        self.label = "WORKTREE"
        if revision is None:
            return
        rc, out, err = git(REPO, ("rev-parse", "--verify", "--quiet",
                                  revision + "^{commit}"))
        if rc != 0 or not out.strip():
            raise CensusError("unreadable revision: %r (%s)"
                              % (revision, err.strip()))
        self.label = out.decode("utf-8", "replace").strip()

    def _entries(self, rel):
        if self.label == "WORKTREE":
            d = REPO / rel
            if not d.is_dir():
                return []
            return [("tree" if d2.is_dir() else "blob", d2.name)
                    for d2 in d.iterdir()]
        rc, out, err = git(REPO, ("ls-tree", "-z", "%s:%s" % (self.label, rel)))
        if rc != 0:
            if benign_absent(err):
                return []
            raise CensusError("unreadable input: ls-tree %s (%s)"
                              % (rel, err.strip()))
        entries = []
        for raw in out.split(b"\0"):
            if raw:
                meta, _, name = raw.decode("utf-8", "replace").partition("\t")
                parts = meta.split(" ")
                if len(parts) == 3:
                    entries.append((parts[1], name))
        return entries

    def list_md(self, rel):
        return sorted(n for k, n in self._entries(rel)
                      if k == "blob" and n.endswith(".md"))

    def list_dirs(self, rel):
        return sorted(n for k, n in self._entries(rel) if k == "tree")

    def read_text(self, rel):
        if self.label == "WORKTREE":
            p = REPO / rel
            if not p.is_file():
                return None
            try:
                return p.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                raise CensusError("unreadable input: %s (%s)" % (rel, exc))
        rc, out, err = git(REPO, ("show", "%s:%s" % (self.label, rel)))
        if rc == 0:
            return out.decode("utf-8", "replace")
        if benign_absent(err):
            return None
        raise CensusError("unreadable input: show %s (%s)"
                          % (rel, err.strip()))


def load_receipt():
    """Delivered working-tree instrumentation, read at every revision."""
    try:
        raw = (REPO / RECEIPT_REL).read_bytes()
        receipt = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise CensusError("unreadable input: receipt (%s)" % exc)
    candidates = receipt.get("source_candidates")
    if not isinstance(candidates, list) or not all(
            isinstance(c, str) and c.strip() for c in candidates):
        raise CensusError("unreadable input: receipt source_candidates")
    return raw, receipt, [c.strip() for c in candidates]


def parse_index(readme_text):
    """category -> linked names in row order; a first cell must be exactly
    one backtick span with a known prefix; headers, prose, other shapes are
    ignored. Discovery is independent of these rows."""
    rows = {"knowledge": [], "lessons": [], "evidence": []}
    for line in readme_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or stripped.count("|") < 3:
            continue
        cell = stripped.split("|")[1].strip()
        if len(cell) < 3 or not (cell.startswith("`") and cell.endswith("`")):
            continue
        link = cell[1:-1].strip()
        for prefix in ("knowledge/", "lessons/"):
            if link.startswith(prefix) and link[len(prefix):]:
                rows[prefix[:-1]].append(link[len(prefix):])
                break
        else:
            rest = link[len("evidence/"):] if link.startswith("evidence/") else ""
            if rest.strip("/"):
                rows["evidence"].append(rest.strip("/").split("/")[0])
    return rows


def count_markers(text):
    return sum(line.count(MARKER) for line in text.splitlines()[:SCAN])


def category(snap, name, linked_names):
    rel = CATS[name]
    names = snap.list_dirs(rel) if name == "evidence" else snap.list_md(rel)
    discovered = {rel + "/" + n for n in names}
    linked = [rel + "/" + n for n in linked_names]
    found = set(linked)
    return {"unit": "dir" if name == "evidence" else "file",
            "files": len(discovered), "indexed": len(discovered & found),
            "unindexed": sorted(discovered - found),
            "dangling": sorted(found - discovered),
            "duplicate_rows": sorted({n for n in linked if linked.count(n) >= 2})}


def build_census(revision):
    snap = Snapshot(revision)
    readme = snap.read_text(README)
    if readme is None:
        raise CensusError("unreadable input: %s absent at measured revision"
                          % README)
    raw, receipt, candidates = load_receipt()
    rows = parse_index(readme)
    marked, unmarked, missing = [], [], []
    for path in candidates:
        text = snap.read_text(path)
        hits = count_markers(text) if text is not None else None
        if hits is None:
            missing.append(path)
        elif hits:
            marked.append({"count": hits, "path": path})
        else:
            unmarked.append(path)
    command = "python3 corpus/evidence/round13-coverage/coverage_census.py"
    if revision is not None:
        command += " --revision " + revision
    return {
        "schema": SCHEMA, "command": command, "revision": snap.label,
        "instrumentation": {
            "path": RECEIPT_REL, "loaded_from": "WORKTREE",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "receipt_baseline_commit": receipt.get("baseline_commit"),
            "denominator": len(candidates),
            "note": "candidates frozen in delivered instrumentation; may "
                    "postdate the measured revision; never re-derived"},
        "source_status": {"marker": MARKER, "scan_lines": SCAN,
                          "denominator": len(candidates),
                          "marked": sorted(marked, key=lambda r: r["path"]),
                          "unmarked": sorted(unmarked),
                          "missing": sorted(missing)},
        "knowledge": category(snap, "knowledge", rows["knowledge"]),
        "lessons": category(snap, "lessons", rows["lessons"]),
        "evidence": category(snap, "evidence", rows["evidence"])}


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="coverage_census.py", description="Read-only revision-aware "
        "coverage census probe (fixed denominator; probe, not gate).")
    parser.add_argument("--revision", default=None,
                        help="git rev to measure; omit for working tree")
    args = parser.parse_args(sys.argv[1:] if argv is None else list(argv))
    try:
        json.dump(build_census(args.revision), sys.stdout, sort_keys=True,
                  indent=2)
        sys.stdout.write("\n")
        return 0
    except CensusError as exc:
        sys.stderr.write("coverage_census: %s\n" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
