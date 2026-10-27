REV a543d92083557dd9b33ee674e9b99b03411f80af
--- mutants.py (scratch-only mutant authoring, sha256 58edff3901a3336e9c69d11dfd03017bd2f1ff3363a1d69861022d5eba8a79cb)
#!/usr/bin/env python3
"""Author the 13 single-edit mutants of the committed C2 package bytes.

Each mutant is applied to a scratch COPY of the clone at the stage-1 freeze (a543d920);
the lane clone itself is never modified. Every mutant is one behavioural edit of one
committed package byte surface:

  capture    corpus/evidence/round46/tb2-polyglot-c-py/*
  entry      corpus/knowledge/tb2-polyglot-c-py-grader.md
  receipt    corpus/evidence/round46/polyglot-c-py-probe.txt
  dry table  corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt
  spec       plans/pkg-spec-r46.json
  probe      plans/polyglot_c_py_probe.py
"""
from __future__ import annotations

import pathlib
import shutil
import sys

CAP = "corpus/evidence/round46/tb2-polyglot-c-py"
ENTRY = "corpus/knowledge/tb2-polyglot-c-py-grader.md"
RECEIPT = "corpus/evidence/round46/polyglot-c-py-probe.txt"
DRY = "corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt"
SPEC = "plans/pkg-spec-r46.json"
PROBE = "plans/polyglot_c_py_probe.py"


def edit(path: pathlib.Path, old: str, new: str, count: int = 1) -> str:
    text = path.read_text()
    if old not in text:
        raise SystemExit("PATTERN NOT FOUND in %s: %r" % (path, old[:80]))
    n = text.count(old)
    if n != count:
        raise SystemExit("PATTERN AMBIGUOUS in %s: %d occurrences of %r" % (path, n, old[:80]))
    path.write_text(text.replace(old, new, count))
    return old[:60]


def m01_capture_test_outputs_value(root):
    """captured grader: the fixed point 42's expected value is changed."""
    return edit(root / CAP / "test_outputs.py",
                'test_cases = [(42, "267914296"), (10, "55"), (0, "0")]',
                'test_cases = [(42, "267914297"), (10, "55"), (0, "0")]')


def m02_capture_manifest_drop(root):
    """capture manifest: the task.toml row is dropped from SHA256SUMS."""
    return edit(root / CAP / "SHA256SUMS",
                "d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea  task.toml\n", "")


def drop_row(path: pathlib.Path, section: str, row_prefix: str) -> str:
    """Remove the first row of `path` whose line starts with `row_prefix`, inside `section`."""
    lines = path.read_text().splitlines(keepends=True)
    out, in_section, dropped = [], False, False
    for line in lines:
        if line.startswith("## "):
            in_section = line.strip() == section
        if in_section and not dropped and line.startswith(row_prefix):
            dropped = True
            continue
        out.append(line)
    if not dropped:
        raise SystemExit("PATTERN NOT FOUND in %s (%s): %r" % (path, section, row_prefix))
    path.write_text("".join(out))
    return "%s %s" % (section, row_prefix)


def m03_capture_readme_line(root):
    """captured README: a comment line is added (capture bytes change)."""
    return edit(root / CAP / "README.md", "# Polyglot C/Python Task\n",
                "# Polyglot C/Python Task\n# mutant M03: comment-only capture edit\n")


def m04_entry_case_table_row(root):
    """entry: one row of the '## Case table' is removed."""
    return drop_row(root / ENTRY, "## Case table", "| `n-parsed-differently` |")


def m05_entry_mechanism_row(root):
    """entry: one row of the '## Mechanism' section is removed."""
    return drop_row(root / ENTRY, "## Mechanism", "| `trailing-ws` | `test_outputs.py:36` |")


def m06_entry_reqmap_row(root):
    """entry: one row of the '## Requirement map' is removed."""
    return drop_row(root / ENTRY, "## Requirement map", "| `instruction.md:5` | `c-build` |")


def m07_receipt_observed_flip(root):
    """receipt: one case's observed verdict is flipped."""
    return edit(root / RECEIPT,
                "CASE nop predicted=fail observed=fail tests=F predicted_tests=F match=yes",
                "CASE nop predicted=fail observed=pass tests=F predicted_tests=F match=yes")


def m08_receipt_summary_counts(root):
    """receipt: the summary line's counts are changed."""
    return edit(root / RECEIPT,
                "cases=18 observed_pass=7 observed_fail=11 mismatches=0",
                "cases=18 observed_pass=8 observed_fail=10 mismatches=0")


def m09_receipt_violates_emptied(root):
    """receipt: one case's violates= list is emptied."""
    return edit(root / RECEIPT,
                "CASE extra-file predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same "
                "violates=single-file",
                "CASE extra-file predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same "
                "violates=")


def m10_dry_table_case_renamed(root):
    """dry table: one CASE id is renamed."""
    return edit(root / DRY, "CASE n-parsed-differently predicted=fail", "CASE n-parsed-diff predicted=fail")


def m11_dry_table_tag_location(root):
    """dry table: one TAG's instruction line is moved."""
    return edit(root / DRY, "TAG stdout-only instruction.md:7", "TAG stdout-only instruction.md:8")


def m12_spec_row_digest(root):
    """spec: one row's capture digest is changed."""
    return edit(root / SPEC,
                '"sha256": "b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec"',
                '"sha256": "b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec"'[:-1] + "0")


def m13_probe_comment(root):
    """probe: a comment line is added (probe bytes change; --dry output stays identical)."""
    return edit(root / PROBE,
                "#!/usr/bin/env python3\n",
                "#!/usr/bin/env python3\n# mutant M13: comment-only edit; the --dry table is unchanged\n")


MUTANTS = [
    ("M01", "capture", "captured test_outputs.py fixed point changed",
     m01_capture_test_outputs_value),
    ("M02", "capture", "SHA256SUMS row for task.toml dropped",
     m02_capture_manifest_drop),
    ("M03", "capture", "captured README.md gains a comment line",
     m03_capture_readme_line),
    ("M04", "entry", "'## Case table' row removed",
     m04_entry_case_table_row),
    ("M05", "entry", "'## Mechanism' row removed",
     m05_entry_mechanism_row),
    ("M06", "entry", "'## Requirement map' row removed",
     m06_entry_reqmap_row),
    ("M07", "receipt", "one CASE observed verdict flipped",
     m07_receipt_observed_flip),
    ("M08", "receipt", "summary counts changed",
     m08_receipt_summary_counts),
    ("M09", "receipt", "one CASE violates= list emptied",
     m09_receipt_violates_emptied),
    ("M10", "dry_table", "one CASE id renamed",
     m10_dry_table_case_renamed),
    ("M11", "dry_table", "one TAG instruction line moved",
     m11_dry_table_tag_location),
    ("M12", "spec", "one row's capture digest changed",
     m12_spec_row_digest),
    ("M13", "probe", "probe comment line added",
     m13_probe_comment),
]


def main(argv=None):
    if len(argv) < 3:
        raise SystemExit("usage: mutants.py <clone-dir> <mutant-id>")
    root = pathlib.Path(argv[1]).resolve()
    mid = argv[2]
    for name, surface, desc, fn in MUTANTS:
        if name != mid:
            continue
        detail = fn(root)
        print("%s surface=%s desc=%s detail=%s" % (name, surface, desc, detail))
        return 0
    raise SystemExit("unknown mutant id: %s" % mid)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
