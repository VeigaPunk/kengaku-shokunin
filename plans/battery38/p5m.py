"""battery38 module p5m: one P5 (capture-manifest) fixture per frozen mutant N07 and N08.

N07 (silence, P5, "every registry row's capture is pinned in the manifest, not only the first"):
the fixture is the genuine round-35 package with a registry row that is NOT the first in
`spec["rows"]` moved off its spec pin -- the row's capture gains one appended line and the manifest
line follows the new bytes, so the bytes branch stays silent and only
`<sid>: manifest digest differs from the spec pin` fires. The unmodified gate prints P5 DEFECT for
that row; a gate whose row loop covers the first row only prints P5 ok. The appended line lands
after every line the entry quotes, so P4 stays silent.

N08 (mirror, P5, "a blank manifest line is tolerated, not an unparsed line"): the fixture is the
genuine round-35 package with one blank line appended to the capture manifest. The unmodified gate
skips it (P5 ok, exit 0); a gate whose blank-line `continue` is disabled parses it as an unparsed
manifest line and prints P5 DEFECT.
"""

import hashlib
import re

MANIFEST_NAME = "SHA256SUMS"
MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})\s+\*?(\S+?)\*?$")


def _capdir(ctx, d):
    return d / ctx.spec["capture_dir"]


def _package_argv(d):
    return ["package", "--root", str(d), "--require-clean-tree"]


def _entry_name(line):
    m = MANIFEST_LINE.match(line.strip())
    return m.group(2) if m else None


def _append_line(path, line):
    text = path.read_text()
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + line + "\n")


def _non_first_row(ctx):
    """A registry row id that is not the first in the spec's `rows` mapping (the gate's dict order)."""
    sids = list(ctx.spec["rows"])
    if len(sids) < 2:
        raise RuntimeError("the frozen spec has a single registry row; N07 needs a later one")
    return sids[-1]


def _row_off_pin(ctx, d):
    """N07: a later registry row's manifest digest differs from its spec pin; every other P5 branch silent.

    The row's capture gains a line at the end (after the lines the entry quotes, so P4 is silent) and
    the manifest line is rewritten to the new bytes' digest, so the bytes-match branch stays silent and
    the pin comparison is the only failing row branch.
    """
    ctx.genuine_package(d)
    sid = _non_first_row(ctx)
    cap = ctx.spec["rows"][sid]["capture"]
    capdir = _capdir(ctx, d)
    path = capdir / cap
    _append_line(path, "# line appended by the p5m N07 fixture")
    moved = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = capdir / MANIFEST_NAME
    lines = manifest.read_text().splitlines()
    rewritten, hits = [], 0
    for line in lines:
        if _entry_name(line) == cap:
            line = f"{moved}  {cap}"
            hits += 1
        rewritten.append(line)
    if hits != 1:
        raise RuntimeError(f"expected one manifest line for {cap}, rewrote {hits}")
    manifest.write_text("\n".join(rewritten) + "\n")
    ctx.git_add(d)
    return _package_argv(d)


def _manifest_blank_line(ctx, d):
    """N08: the genuine package plus one blank line in the capture manifest (tolerated by the gate)."""
    ctx.genuine_package(d)
    manifest = _capdir(ctx, d) / MANIFEST_NAME
    text = manifest.read_text()
    manifest.write_text(text.rstrip("\n") + "\n\n")
    ctx.git_add(d)
    return _package_argv(d)


FIXTURES = [
    {
        "fid": "p5m-row-off-pin-later-row",
        "expect": "reject",
        "defects": ["P5"],
        "build": _row_off_pin,
    },
    {
        "fid": "p5m-manifest-blank-line",
        "expect": "accept",
        "defects": [],
        "build": _manifest_blank_line,
    },
]
