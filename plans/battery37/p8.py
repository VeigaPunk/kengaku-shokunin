"""Battery37 module R37BatP8: five single-defect fixtures for the P8 clause of plans/pkg_gate.py.

P8 (c_readme) has five advertised branches; each fixture reaches exactly one of them and only edits
corpus/README.md (or adds one unindexed knowledge file), so the unmodified gate prints exactly P8:

  p8-readme-deleted              M34  README unreadable (return False, "README unreadable")
  p8-index-row-duplicated        M35  index rows for knowledge/<entry> not exactly one
  p8-index-row-missing-sid       M36  index row does not cite every registry row
  p8-coverage-bullet-removed     M37  no coverage bullet naming the entry and its receipt
  p8-extra-knowledge-file        M38  knowledge files differ from index rows

Every declared defects set is {"P8"}: no other clause reads corpus/README.md or corpus/knowledge/*
and no fixture touches bytes another clause reads. No builder inspects the directory name.
"""

import pathlib


def _entry_name(ctx):
    return pathlib.PurePosixPath(ctx.spec["entry"]).name


def _index_needle(ctx):
    return f"| `knowledge/{_entry_name(ctx)}` |"


def _readme_path(ctx, d):
    return d / ctx.spec["readme"]


def _one_line(lines, predicate, what):
    hits = [i for i, line in enumerate(lines) if predicate(line)]
    if len(hits) != 1:
        raise RuntimeError(f"expected one {what}, found {len(hits)}")
    return hits[0]


def _rewrite(ctx, d, edit):
    """Copy the genuine package, apply edit to the README lines, write it back and stage."""
    ctx.genuine_package(d)
    path = _readme_path(ctx, d)
    lines = path.read_text().splitlines()
    edit(path, lines)
    return ["package", "--root", str(d), "--require-clean-tree"]


def _readme_deleted(ctx, d):
    ctx.genuine_package(d)
    _readme_path(ctx, d).unlink()
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def _index_row_duplicated(ctx, d):
    def edit(path, lines):
        i = _one_line(lines, lambda l: l.startswith(_index_needle(ctx)), "index row for the entry")
        lines.insert(i + 1, lines[i])
        path.write_text("\n".join(lines) + "\n")

    build = _rewrite(ctx, d, edit)
    ctx.git_add(d)
    return build


def _index_row_missing_sid(ctx, d):
    sid = sorted(ctx.spec["rows"])[-1]

    def edit(path, lines):
        i = _one_line(lines, lambda l: l.startswith(_index_needle(ctx)), "index row for the entry")
        row = lines[i]
        for old in (f", {sid}", f"{sid}, ", sid):
            if old in row:
                lines[i] = row.replace(old, "", 1)
                break
        else:
            raise RuntimeError(f"{sid} absent from the index row")
        path.write_text("\n".join(lines) + "\n")

    build = _rewrite(ctx, d, edit)
    ctx.git_add(d)
    return build


def _coverage_bullet_removed(ctx, d):
    name = _entry_name(ctx)
    receipt_rel = ctx.spec["receipt"].split("/", 1)[1]

    def edit(path, lines):
        i = _one_line(lines, lambda l: l.startswith("- ") and name in l and receipt_rel in l,
                      "coverage bullet naming the entry and its receipt")
        del lines[i]
        path.write_text("\n".join(lines) + "\n")

    build = _rewrite(ctx, d, edit)
    ctx.git_add(d)
    return build


def _extra_knowledge_file(ctx, d):
    ctx.genuine_package(d)
    kdir = d / pathlib.PurePosixPath(ctx.spec["knowledge_glob"]).parent
    (kdir / "zz-unindexed-fixture-note.md").write_text(
        "# Unindexed fixture note\n\n"
        "Single-defect P8 fixture: a knowledge file that no corpus/README.md index row names.\n"
    )
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [
    {"fid": "p8-readme-deleted", "expect": "reject", "defects": ["P8"], "build": _readme_deleted},
    {"fid": "p8-index-row-duplicated", "expect": "reject", "defects": ["P8"],
     "build": _index_row_duplicated},
    {"fid": "p8-index-row-missing-sid", "expect": "reject", "defects": ["P8"],
     "build": _index_row_missing_sid},
    {"fid": "p8-coverage-bullet-removed", "expect": "reject", "defects": ["P8"],
     "build": _coverage_bullet_removed},
    {"fid": "p8-extra-knowledge-file", "expect": "reject", "defects": ["P8"],
     "build": _extra_knowledge_file},
]
