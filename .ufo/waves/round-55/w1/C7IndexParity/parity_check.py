#!/usr/bin/env python3
"""C7IndexParity: corpus README index parity, both directions, at run time.

Read-only. Usage: parity_check.py <lane-repo> <out-prefix>
Writes <out-prefix>.json and prints a summary. Exit 0 always (findings are data).
"""
import json
import os
import re
import sys

lane = sys.argv[1]
out_prefix = sys.argv[2]
readme_path = os.path.join(lane, "corpus", "README.md")
with open(readme_path, encoding="utf-8") as f:
    readme = f.read()
readme_lines = readme.splitlines()

row_re = {
    "knowledge": re.compile(r"^\| `(knowledge/[^`|]+?\.md)`\s*\|"),
    "lessons": re.compile(r"^\| `(lessons/[^`|]+?\.md)`\s*\|"),
    "evidence": re.compile(r"^\| `(evidence/([^`|]+?)/)`\s*\|"),
}
rows = {"knowledge": [], "lessons": [], "evidence": []}
for i, line in enumerate(readme_lines, 1):
    for kind, rx in row_re.items():
        m = rx.match(line)
        if m:
            rows[kind].append({"line": i, "path": m.group(1).rstrip("/")})

# Evidence dirs also appear as bullets in round-support sections: `- `evidence/round43/` ...`
# or `- `corpus/evidence/round55/` ...`. Collect those as "bullet mentions".
bullet_re = re.compile(r"^\s*[-*] `(?:corpus/)?(evidence/([^`]+?)/)`")
bullet_mentions = []
for i, line in enumerate(readme_lines, 1):
    m = bullet_re.match(line)
    if m:
        bullet_mentions.append({"line": i, "path": m.group(1)})

# Also section headings like `### `evidence/round29-attempt2/` — ...`
head_re = re.compile(r"^#{2,4} `(?:corpus/)?(evidence/([^`]+?)/)`")
head_mentions = []
for i, line in enumerate(readme_lines, 1):
    m = head_re.match(line)
    if m:
        head_mentions.append({"line": i, "path": m.group(1)})

# Files / dirs on disk
knowledge_files = sorted(os.listdir(os.path.join(lane, "corpus", "knowledge")))
knowledge_files = [f for f in knowledge_files if f.endswith(".md")]
lessons_files = sorted(os.listdir(os.path.join(lane, "corpus", "lessons")))
lessons_files = [f for f in lessons_files if f.endswith(".md")]
evidence_entries = sorted(os.listdir(os.path.join(lane, "corpus", "evidence")))
evidence_dirs = [d for d in evidence_entries if os.path.isdir(os.path.join(lane, "corpus", "evidence", d))]
evidence_root_files = [d for d in evidence_entries if not os.path.isdir(os.path.join(lane, "corpus", "evidence", d))]


def mentions_for(kind, bare_names):
    """Any README mention: table row OR bullet/heading `...kind/<name>...`."""
    mentioned = {}
    for r in rows[kind]:
        mentioned.setdefault(r["path"], []).append(f"row:{r['line']}")
    token_re = re.compile(r"`(?:corpus/)?(" + kind + r"/[^`\s|]+)`")
    for i, line in enumerate(readme_lines, 1):
        for m in token_re.finditer(line):
            p = m.group(1).rstrip("/")
            base = p[len(kind) + 1:]
            if base in bare_names and p not in mentioned:
                mentioned.setdefault(p, []).append(f"text:{i}")
            elif p in {r["path"] for r in rows[kind]}:
                mentioned[p].append(f"text:{i}")
    return mentioned


def diff(disk_names, row_paths, prefix):
    """disk: bare filenames (or dir names). rows: corpus-relative paths."""
    disk_rel = {f"{prefix}/{n}" for n in disk_names}
    row_set = set(row_paths)
    return {
        "disk_count": len(disk_rel),
        "row_count": len(row_paths),
        "distinct_row_count": len(row_set),
        "files_without_rows": sorted(disk_rel - row_set),
        "rows_without_files": sorted(row_set - disk_rel),
        "duplicate_rows": sorted({p for p in row_paths if row_paths.count(p) > 1}),
    }


# Any-mention parity (table rows + bullets/headings/prose `code` tokens)
kn_mentions = mentions_for("knowledge", set(knowledge_files))
ls_mentions = mentions_for("lessons", set(lessons_files))
ev_mentions = mentions_for("evidence", set(evidence_dirs))

result = {
    "readme_path": readme_path,
    "row_line_numbers": {k: [r["line"] for r in v] for k, v in rows.items()},
    "knowledge": diff(knowledge_files, [r["path"] for r in rows["knowledge"]], "knowledge"),
    "lessons": diff(lessons_files, [r["path"] for r in rows["lessons"]], "lessons"),
    "evidence_table_rows_only": diff(evidence_dirs, [r["path"] for r in rows["evidence"]], "evidence"),
    "evidence_dirs_on_disk": evidence_dirs,
    "evidence_root_files_count": len(evidence_root_files),
    "knowledge_any_mention": {
        "files": len(knowledge_files),
        "mentioned": len(kn_mentions),
        "files_without_any_mention": sorted(f"knowledge/{f}" for f in knowledge_files if f"knowledge/{f}" not in kn_mentions),
        "mentions_without_files": sorted(p for p in kn_mentions if not os.path.exists(os.path.join(lane, "corpus", p))),
    },
    "lessons_any_mention": {
        "files": len(lessons_files),
        "mentioned": len(ls_mentions),
        "files_without_any_mention": sorted(f"lessons/{f}" for f in lessons_files if f"lessons/{f}" not in ls_mentions),
        "mentions_without_files": sorted(p for p in ls_mentions if not os.path.exists(os.path.join(lane, "corpus", p))),
    },
}

# Evidence: union of table rows, bullet mentions, heading mentions
ev_disk = {f"evidence/{d}" for d in evidence_dirs}
result["evidence_any_mention"] = {
    "disk_dirs": len(ev_disk),
    "mentioned": len(ev_mentions),
    "dirs_without_any_mention": sorted(ev_disk - set(ev_mentions)),
    "mentions_without_dirs": sorted(set(ev_mentions) - ev_disk),
}

# Round-55 specific rows
result["round55"] = {
    "knowledge_entry_row": [r["line"] for r in rows["knowledge"] if "tb2-chess-best-move-grader" in r["path"]],
    "knowledge_entry_file_exists": os.path.exists(os.path.join(lane, "corpus", "knowledge", "tb2-chess-best-move-grader.md")),
    "evidence_round55_dir_exists": os.path.isdir(os.path.join(lane, "corpus", "evidence", "round55")),
    "evidence_round55_any_mention": sorted(p for p in ev_mentions if "round55" in p),
    "lessons_round55_row": [r["line"] for r in rows["lessons"] if r["path"] == "lessons/round-55.md"],
    "lessons_round55_file_exists": os.path.exists(os.path.join(lane, "corpus", "lessons", "round-55.md")),
}

with open(out_prefix + ".json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

k = result["knowledge"]; l = result["lessons"]; e = result["evidence_table_rows_only"]; ea = result["evidence_any_mention"]
ka = result["knowledge_any_mention"]; la = result["lessons_any_mention"]
print(f"knowledge(table rows): files={k['disk_count']} rows={k['distinct_row_count']} files_wo_rows={len(k['files_without_rows'])} rows_wo_files={len(k['rows_without_files'])} dupes={k['duplicate_rows']}")
print(f"knowledge(any mention): files={ka['files']} mentioned={ka['mentioned']} files_wo_any={len(ka['files_without_any_mention'])}")
print(f"lessons(table rows):   files={l['disk_count']} rows={l['distinct_row_count']} files_wo_rows={len(l['files_without_rows'])} rows_wo_files={len(l['rows_without_files'])} dupes={l['duplicate_rows']}")
print(f"lessons(any mention):  files={la['files']} mentioned={la['mentioned']} files_wo_any={len(la['files_without_any_mention'])}")
print(f"evidence(table rows only): dirs={e['disk_count']} rows={e['distinct_row_count']} dirs_wo_rows={len(e['files_without_rows'])} rows_wo_dirs={len(e['rows_without_files'])}")
print(f"evidence(any mention): dirs={ea['disk_dirs']} mentioned={ea['mentioned']} dirs_wo_any={len(ea['dirs_without_any_mention'])}")
print("round55:", json.dumps(result["round55"]))
print("knowledge files_wo_rows:", k["files_without_rows"])
print("knowledge rows_wo_files:", k["rows_without_files"])
print("lessons files_wo_rows:", l["files_without_rows"])
print("lessons rows_wo_files:", l["rows_without_files"])
print("evidence dirs_wo_any_mention:", ea["dirs_without_any_mention"])
print("evidence mentions_wo_dirs:", ea["mentions_without_dirs"])
print("lessons files_wo_any_mention:", la["files_without_any_mention"])
