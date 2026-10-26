"""battery37 module p5: one single-defect fixture per P5 (capture-manifest) branch of the round-36 gate.

Seven mutants of `plans/pkg_gate.py` silence the seven P5 branches (`bad.append(...)` -> `pass`, and the
manifest-absent return). Each fixture below is the genuine round-35 package with exactly one manifest defect,
and the unmodified gate reports the one clause this module declares: P5.

P5 collects every branch into one `bad` list, so a fixture that leaves two branches firing cannot demonstrate
either mutant: the mutant silences its own append and the other append keeps P5 red. Each fixture therefore
removes the other reachable branches of the same clause while leaving its own firing; the reasons are stated
at each builder. No fixture moves a second clause.

Single-defect note for M16/M17/M18: the defect is one manifest property; the extra edits only keep a *second
P5 branch on the same fixture* silent (an uncovered file, a quoted capture left unpinned, or a stale digest),
never a second defect class.
"""

import hashlib
import re

MANIFEST_NAME = "SHA256SUMS"
EXTRA_DOTFILE = ".quote-extra.txt"
EXTRA_FILE = "extra-note.txt"
MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})\s+\*?(\S+?)\*?$")


def _capdir(ctx, d):
    return d / ctx.spec["capture_dir"]


def _append_line(path, line):
    text = path.read_text()
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + line + "\n")


def _entry_name(line):
    m = MANIFEST_LINE.match(line.strip())
    return m.group(2) if m else None


def _rewrite_manifest(capdir, fn):
    path = capdir / MANIFEST_NAME
    lines = [l for l in path.read_text().splitlines() if l.strip()]
    path.write_text("\n".join(fn(lines)) + "\n")


def _cited_captures(ctx, d):
    """Capture names the entry's Located quotes rows cite (same row regex the gate uses)."""
    names = set()
    for line in (d / ctx.spec["entry"]).read_text().splitlines():
        m = ctx.r36.QUOTE_ROW.match(line)
        if m:
            names.add(m.group(2))
    return names


def _pinned_names(ctx, d):
    return [n for n in (_entry_name(l) for l in (_capdir(ctx, d) / MANIFEST_NAME).read_text().splitlines()) if n]


def _unquoted_pinned_capture(ctx, d):
    """A pinned capture that is neither a registry row nor cited by a quote (task.toml with the r35 spec).

    P4 reads only quoted captures, so changing this one's bytes cannot move P4.
    """
    cited = _cited_captures(ctx, d)
    rows = {row["capture"] for row in ctx.spec["rows"].values()}
    for name in _pinned_names(ctx, d):
        if name not in cited and name not in rows:
            return name
    raise RuntimeError("no pinned capture outside the rows and the quotes; these fixtures need one")


def _row_capture(ctx, d):
    """First registry row (sorted by id). Every r35 row capture is quoted, so P4 fires when one is deleted."""
    sid = sorted(ctx.spec["rows"])[0]
    return sid, ctx.spec["rows"][sid]["capture"]


def _package_argv(d):
    return ["package", "--root", str(d), "--require-clean-tree"]


def _manifest_absent(ctx, d):
    """M13: SHA256SUMS deleted. Only P5's manifest-absent return can fire."""
    ctx.genuine_package(d)
    (_capdir(ctx, d) / MANIFEST_NAME).unlink()
    ctx.git_add(d)
    return _package_argv(d)


def _manifest_unparsed_line(ctx, d):
    """M14: the manifest gains one line that is not `<64 hex>  <name>`."""
    ctx.genuine_package(d)
    _append_line(_capdir(ctx, d) / MANIFEST_NAME, "a note the manifest parser cannot read")
    ctx.git_add(d)
    return _package_argv(d)


def _capture_bytes_stale_digest(ctx, d):
    """M15: a pinned capture's bytes change, its pinned digest stays. Every pinned file still matches the
    spec pin (M17 stays silent) and the entry's quotes still resolve (P4 stays silent): the capture is
    `task.toml`, which no row and no quote names."""
    ctx.genuine_package(d)
    cap = _unquoted_pinned_capture(ctx, d)
    _append_line(_capdir(ctx, d) / cap, "# line appended by the M15 fixture")
    ctx.git_add(d)
    return _package_argv(d)


def _row_capture_unpinned(ctx, d):
    """M16: one registry row's capture has no manifest line, so `pinned[name]` misses and the row is unpinned.

    Two facts of the round-35 package force the bookkeeping around that single defect. Every row capture is
    also cited by a quote, so simply dropping the pin also trips the quoted-capture-not-pinned branch (M18)
    in the same clause — and M18 would keep P5 red after M16 is silenced. And a file left on disk without a
    pin trips the not-covered sweep (M19). So the capture's bytes move to a byte-identical copy
    (`<capture>.copy`, pinned with the same digest, so M15 stays silent), the quotes are re-cited to that
    copy at the same line numbers (P4 stays silent), and the original name leaves both the manifest and the
    directory. The one defect left is the unpinned registry row.
    """
    ctx.genuine_package(d)
    _sid, cap = _row_capture(ctx, d)
    capdir = _capdir(ctx, d)
    copy_name = cap + ".copy"
    (capdir / copy_name).write_bytes((capdir / cap).read_bytes())
    (capdir / cap).unlink()
    _rewrite_manifest(capdir, lambda lines: [l.replace(cap, copy_name) if _entry_name(l) == cap else l
                                             for l in lines])
    entry = d / ctx.spec["entry"]

    def fn(rows):
        out = []
        for row in rows:
            m = ctx.r36.QUOTE_ROW.match(row)
            if m and m.group(2) == cap:
                row = row.replace(f"`{cap}:", f"`{copy_name}:")
            out.append(row)
        return out

    entry.write_text(ctx.r36.rewrite_quotes(entry.read_text(), fn))
    ctx.git_add(d)
    return _package_argv(d)


def _manifest_digest_off_pin(ctx, d):
    """M17: one row's manifest digest differs from the spec pin.

    The line is moved to the new bytes' digest, so the manifest still matches the capture bytes (M15 stays
    silent) while differing from `spec['rows'][sid]['sha256']`. The appended line lands after every line the
    entry quotes, so P4 stays silent.
    """
    ctx.genuine_package(d)
    _sid, cap = _row_capture(ctx, d)
    capdir = _capdir(ctx, d)
    path = capdir / cap
    _append_line(path, "# line appended by the M17 fixture")
    moved = hashlib.sha256(path.read_bytes()).hexdigest()

    def fn(lines):
        out = []
        for line in lines:
            if _entry_name(line) == cap:
                line = f"{moved}  {cap}"
            out.append(line)
        return out

    _rewrite_manifest(capdir, fn)
    ctx.git_add(d)
    return _package_argv(d)


def _quote_cites_unpinned_capture(ctx, d):
    """M18: a quote cites a capture that is on disk but not in the manifest.

    The new capture is a dotfile: the not-covered sweep skips names starting with `.`, so only the
    quote-capture-not-pinned branch fires. The quote text sits verbatim on line 1, so P4 stays silent.
    """
    ctx.genuine_package(d)
    capdir = _capdir(ctx, d)
    entry = d / ctx.spec["entry"]
    picked = {}

    def fn(rows):
        for i, row in enumerate(rows):
            m = ctx.r36.QUOTE_ROW.match(row)
            if not m:
                continue
            text = m.group(1)
            loc = f"`{m.group(2)}:{m.group(3)}" + (f"-{m.group(4)}" if m.group(4) else "") + "`"
            picked["text"] = text
            new = [r for r in rows]
            new[i] = row.replace(loc, f"`{EXTRA_DOTFILE}:1`")
            return new
        raise RuntimeError("no parsable quote row to re-cite")

    entry.write_text(ctx.r36.rewrite_quotes(entry.read_text(), fn))
    (capdir / EXTRA_DOTFILE).write_text(picked["text"] + "\n")
    ctx.git_add(d)
    return _package_argv(d)


def _extra_capture_file(ctx, d):
    """M19: one capture file in the directory that the manifest does not cover and no quote cites."""
    ctx.genuine_package(d)
    (_capdir(ctx, d) / EXTRA_FILE).write_text("a capture the manifest does not cover\n")
    ctx.git_add(d)
    return _package_argv(d)


FIXTURES = [
    {"fid": "p5-manifest-absent", "expect": "reject", "defects": ["P5"], "build": _manifest_absent},
    {"fid": "p5-manifest-unparsed-line", "expect": "reject", "defects": ["P5"], "build": _manifest_unparsed_line},
    {"fid": "p5-capture-bytes-stale-digest", "expect": "reject", "defects": ["P5"], "build": _capture_bytes_stale_digest},
    {"fid": "p5-row-capture-unpinned", "expect": "reject", "defects": ["P5"], "build": _row_capture_unpinned},
    {"fid": "p5-manifest-digest-off-pin", "expect": "reject", "defects": ["P5"], "build": _manifest_digest_off_pin},
    {"fid": "p5-quote-cites-unpinned", "expect": "reject", "defects": ["P5"], "build": _quote_cites_unpinned_capture},
    {"fid": "p5-extra-capture-file", "expect": "reject", "defects": ["P5"], "build": _extra_capture_file},
]
