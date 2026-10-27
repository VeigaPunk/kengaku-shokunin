#!/usr/bin/env python3
"""Bidirectional index parity: corpus/README.md vs disk (knowledge/, lessons/, evidence/).

Final conventions (documented for the L1):
- A backticked token counts as a path when it starts with knowledge/, lessons/ or evidence/
  (after stripping a corpus/ prefix or a ../ prefix, a trailing slash and a :N / :N-M line
  suffix). `*` globs and {a,b} braces are expanded; a pattern resolves when >=1 path matches.
- Direction A (rows resolve): every such token must resolve on disk. Reported for table
  first-cell rows only (round-13 census convention) and for all tokens.
- Direction B (files have rows): every file under the three trees is covered when its own
  corpus-relative path is a token (exact or glob match), or — evidence/ only — an ancestor
  directory under evidence/ is a token (README indexes evidence by directory rows).
- Verdict numbers: m = uncovered files, d = unresolved in-scope tokens.

Usage: python3 index_parity_check.py <lane-root>  — read-only; exit 0 iff d==0 and m==0.
"""
import fnmatch
import json
import re
import sys
from pathlib import Path

LANE = Path(sys.argv[1]).resolve()
CORPUS = LANE / "corpus"
README = CORPUS / "README.md"
TREES = ("knowledge", "lessons", "evidence")
HERE = Path(__file__).resolve().parent
LINE_SUFFIX = re.compile(r"^(?P<path>.+?\.(?:md|py|sh|txt|json|jsonl|log|mjs|tsv|csv|toml|pyc)):\d+(?:-\d+)?$")
TABLE_CELL = re.compile(r"^\|[^|]*\|\s*`([^`]+)`\|")


def brace_expand(t):
    m = re.search(r"\{([^{}]+)\}", t)
    if not m:
        return [t]
    return [x for a in m.group(1).split(",") for x in brace_expand(t[:m.start()] + a + t[m.end():])]


def norm(tok):
    t = tok.strip()
    if not t or " " in t or t.startswith(("http", "~/", "/")) or "`" in t:
        return None
    if t.startswith("../"):
        t = t[3:]
    if t.startswith("corpus/"):
        t = t[len("corpus/"):]
    m = LINE_SUFFIX.match(t)
    if m:
        t = m.group("path")
    t = t.rstrip("/")
    if not t.startswith(TREES) or "/" not in t:
        return None
    if ".." in t.split("/"):
        return None
    return t


def main():
    text = README.read_text()
    tokens = re.findall(r"`([^`\n]+)`", text)
    table_cells = [TABLE_CELL.match(l.strip()).group(1)
                   for l in text.splitlines()
                   if TABLE_CELL.match(l.strip())]
    table_set = {n for c in table_cells if (n := norm(c))}
    cand = {n for tk in tokens if (n := norm(tk))}
    # expand brace tokens into concrete literals before classifying
    braces = {c for c in cand if "{" in c}
    cand = (cand - braces) | {b for c in braces for b in brace_expand(c)}
    for c in braces:
        for b in brace_expand(c):
            table_set.discard(c)
            if b in {n for cc in table_cells if (n := norm(cc))}:
                table_set.add(b)
    patterns = {c for c in cand if "*" in c or "?" in c}
    literals = cand - patterns

    # pre-expand pattern tokens against the three trees
    all_paths = [p.relative_to(CORPUS).as_posix() for t in TREES for p in (CORPUS / t).rglob("*")]
    pattern_hits = {p: sorted(q for q in all_paths if fnmatch.fnmatch(q, p)) for p in patterns}

    dangling_table = sorted(t for t in table_set
                            if ("*" in t or "?" in t) and not pattern_hits.get(t) or
                            ("*" not in t and "?" not in t) and not exists(CORPUS / t))
    dangling_any = sorted(t for t in cand
                          if ("*" in t or "?" in t) and not pattern_hits.get(t) or
                          ("*" not in t and "?" not in t) and not exists(CORPUS / t))
    bare_root_rows = sorted({c for c in table_cells
                             if re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.+-]*\.(log|md|py|txt|jsonl)", c)
                             and not (CORPUS / c).exists()})

    files = [p for t in TREES for p in sorted((CORPUS / t).rglob("*")) if p.is_file()]
    dir_tokens = {c for c in cand if ("*" not in c and (CORPUS / c).is_dir())}
    missing = []
    for p in files:
        rel = p.relative_to(CORPUS).as_posix()
        if rel in literals or any(fnmatch.fnmatch(rel, pat) for pat in patterns):
            continue
        if rel.startswith("evidence/"):
            parts = rel.split("/")
            if any("evidence/" + "/".join(parts[1:k]) in dir_tokens for k in range(2, len(parts))):
                continue
        missing.append(rel)
    by_tree = {}
    for mrel in missing:
        by_tree.setdefault(mrel.split("/")[0], []).append(mrel)

    out = {
        "readme_sha256_rel": "corpus/README.md",
        "files_on_disk": len(files),
        "by_tree": {t: sum(1 for f in files if f.relative_to(CORPUS).as_posix().startswith(t + "/")) for t in TREES},
        "dangling_table_rows": dangling_table,
        "dangling_any_token": dangling_any,
        "pattern_tokens_resolved": {p: len(h) for p, h in sorted(pattern_hits.items())},
        "bare_name_root_table_rows_pointing_at_evidence": bare_root_rows,
        "MISSING_TOTAL": len(missing),
        "missing_by_tree": {k: len(v) for k, v in sorted(by_tree.items())},
    }
    (HERE / "parity-summary.json").write_text(json.dumps(out, indent=1))
    (HERE / "missing-files.txt").write_text("\n".join(missing) + "\n")
    print(json.dumps(out, indent=1))
    if missing:
        print("MISSING LIST:")
        print("\n".join(missing))
    return 0 if not (dangling_any or missing) else 1


def exists(path):
    return path.is_file() or path.is_dir()


if __name__ == "__main__":
    sys.exit(main())
