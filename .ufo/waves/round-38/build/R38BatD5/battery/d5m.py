#!/usr/bin/env python3
"""battery38 module `d5m` — D5 fixtures for the frozen round-38 gate mutants N21 and N22.

Frozen mutants (plans/round38_c1_verify.py): both `D5`, both directed `silence`.
  N21  `sums.splitlines()` -> `sums.splitlines()[:1]` — the capture digest is looked up in every
       manifest row, not only the first.
  N22  `re.sub(r"\\s+", "", d5["quote"])` -> `... [:20]` — the whole quote must be present, not a
       20-character prefix.

`d5-line` runs exactly one clause, so every reject fixture declares `["D5"]` and every accept
fixture declares `[]`; the declaration is the exact DEFECT set the unmodified gate prints.

`d5m-n22-quote-prefix` is the attributable kill: the capture holds only `quote[:20]` and the
manifest is re-pinned to those bytes, so the reference gate prints `D5 DEFECT` (quote absent) while
N22 prints `D5 ok` — the silence signature the kill rule wants.

`d5m-n21-manifest-row-2` is the positional coverage row (decoy manifest row first, the genuine
digest row second, genuine capture and erratum line).  The unmodified gate accepts it
(`D5 ok`, digest pinned from row 2); N21 rejects it (`D5 DEFECT`).  That is the *mirror* signature,
not the silence one, so under the frozen `direction=silence` cell the counter cannot count it: the
gate change only ever adds the pin defect, so no input can make the reference defect where the
mutant passes.  The row is kept because it is the only fixture in the whole battery whose matching
manifest row is not row 1 (`F37XMutD5` F2), and it kills N21 the moment the direction cell is
corrected to `mirror`.
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import shutil

FID_PREFIX = "d5m"


def _captures(ctx, d):
    """Copy the frozen capture dir into d; return (copied dir, the D5 capture file inside it)."""
    dst = pathlib.Path(d) / "captures"
    shutil.copytree(ctx.d5_capture_dir(), dst)
    return dst, dst / ctx.spec["d5"]["capture_name"]


def _write_manifest(ctx, capdir, rows):
    text = "".join(f"{digest}  {name}\n" for digest, name in rows)
    (capdir / ctx.spec["d5"]["manifest_name"]).write_text(text)


def _line_file(ctx, d):
    """The single-line erratum file `d5-line --file` reads: the genuine labelled line and nothing else."""
    f = pathlib.Path(d) / "erratum.md"
    f.write_text(ctx.d5_line() + "\n")
    return f


def _argv(ctx, d, capdir):
    return ["d5-line", "--file", str(_line_file(ctx, d)), "--capture-dir", str(capdir)]


def build_quote_prefix(ctx, d):
    """N22: capture truncated to the first 20 non-space characters of the quote, manifest re-pinned."""
    capdir, cap = _captures(ctx, d)
    cap.write_text(re.sub(r"\s+", "", ctx.spec["d5"]["quote"])[:20] + "\n")
    _write_manifest(ctx, capdir, [(hashlib.sha256(cap.read_bytes()).hexdigest(), cap.name)])
    return _argv(ctx, d, capdir)


def build_manifest_row_2(ctx, d):
    """N21: decoy manifest row first, the genuine capture digest row second; everything else genuine."""
    capdir, cap = _captures(ctx, d)
    digest = hashlib.sha256(cap.read_bytes()).hexdigest()
    _write_manifest(ctx, capdir, [("0" * 64, "geniac-s105-reopen.html"), (digest, cap.name)])
    return _argv(ctx, d, capdir)


FIXTURES = [
    {"fid": "d5m-n22-quote-prefix", "expect": "reject", "defects": ["D5"], "build": build_quote_prefix},
    {"fid": "d5m-n21-manifest-row-2", "expect": "accept", "defects": [], "build": build_manifest_row_2},
]
