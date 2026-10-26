"""Round-37 battery37 module `p7`: single-defect fixtures for gate clause P7 (provenance).

Every fixture starts from the genuine round-35 package (`ctx.genuine_package`) and edits only the
entry `corpus/knowledge/tb2-protein-assembly-grader.md`, then stages the tree (`ctx.git_add`) so P9
(clean tree) stays green. Each edit breaks exactly one P7 branch; the declared defect set is what the
UNMODIFIED gate prints on that tree. Mutants M28-M33 silence one P7 branch each in
`plans/round37_c1_verify.py`; a fixture kills its mutant only when that branch is the only difference
between reference and mutant, i.e. exactly one P7 `bad` item fires here.

  p7-m28-entry-deleted     entry file removed            -> M28 "entry unreadable"
  p7-m29-source-url        S106 source line URL changed  -> M29 "source line not the pinned url"
  p7-m30-verified-at       verified-at date changed      -> M30 "verified-at ... frozen date"
  p7-m31-recheck-line      `recheck:` line removed       -> M31 "recheck line absent"
  p7-m32-negative-heading  `## Negative space` removed   -> M32 "no '## Negative space' section"
  p7-m33-falsifier-word    falsifier word removed        -> M33 "carries no falsifier"

p7-m28 deletes the entry, so P7 is not the only clause that reads the entry file: P3 (no Located
quotes section), P4 (no parsed quote) and P8 (knowledge files != index rows) also fire. Its
declaration lists that exact set; it still kills M28 because the mutant flips P7 to `ok` while the
reference prints P7 DEFECT.
"""

SOURCE_URL = "protein-assembly/tests/test.sh — reward mapping"
BROKEN_URL = "protein-assembly/tests/test_other.sh — reward mapping"
VERIFIED = "verified-at: 2026-10-25"
VERIFIED_STALE = "verified-at: 2026-10-24"
RECHECK_PREFIX = "recheck:"
NEGATIVE_HEADING = "## Negative space"
FALSIFIER = "**Falsifier:** this entry is falsified if"
NO_FALSIFIER = "**Check:** this entry is contradicted if"


def _package(ctx, d, edit):
    """Build the genuine package, apply one entry edit (None = delete the entry), stage, return argv."""
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    if edit is None:
        entry.unlink()
    else:
        before = entry.read_text()
        after = edit(before)
        if after == before:
            raise RuntimeError("entry edit was a no-op")
        entry.write_text(after)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def _drop_line(text, prefix):
    lines = text.splitlines()
    kept = [l for l in lines if not l.startswith(prefix)]
    if len(kept) != len(lines) - 1:
        raise RuntimeError(f"expected exactly one line starting {prefix!r}")
    return "\n".join(kept) + "\n"


def _only_once(text, needle):
    if text.count(needle) != 1:
        raise RuntimeError(f"expected exactly one {needle!r}, found {text.count(needle)}")
    return text


def _m28(ctx, d):
    return _package(ctx, d, None)


def _m29(ctx, d):
    def edit(text):
        _only_once(text, SOURCE_URL)
        return text.replace(SOURCE_URL, BROKEN_URL, 1)
    return _package(ctx, d, edit)


def _m30(ctx, d):
    def edit(text):
        _only_once(text, VERIFIED)
        return text.replace(VERIFIED, VERIFIED_STALE, 1)
    return _package(ctx, d, edit)


def _m31(ctx, d):
    return _package(ctx, d, lambda text: _drop_line(text, RECHECK_PREFIX))


def _m32(ctx, d):
    def edit(text):
        return _drop_line(text, NEGATIVE_HEADING)
    return _package(ctx, d, edit)


def _m33(ctx, d):
    def edit(text):
        _only_once(text, FALSIFIER)
        return text.replace(FALSIFIER, NO_FALSIFIER, 1)
    return _package(ctx, d, edit)


FIXTURES = [
    {"fid": "p7-m28-entry-deleted", "expect": "reject",
     "defects": ["P3", "P4", "P7", "P8"], "build": _m28},
    {"fid": "p7-m29-source-url", "expect": "reject", "defects": ["P7"], "build": _m29},
    {"fid": "p7-m30-verified-at", "expect": "reject", "defects": ["P7"], "build": _m30},
    {"fid": "p7-m31-recheck-line", "expect": "reject", "defects": ["P7"], "build": _m31},
    {"fid": "p7-m32-negative-heading", "expect": "reject", "defects": ["P7"], "build": _m32},
    {"fid": "p7-m33-falsifier-word", "expect": "reject", "defects": ["P7"], "build": _m33},
]
