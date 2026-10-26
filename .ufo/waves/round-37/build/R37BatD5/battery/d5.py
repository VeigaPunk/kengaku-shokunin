"""Battery37 module: D5 (`d5-line`) single-defect fixtures for round-37 C1.

One fixture per frozen gate mutant of the D5 branch (`plans/pkg_gate.py`, `cmd_d5`):

  d5-m48-file-unreadable   M48  --file names no file                    -> "file unreadable"
  d5-m49-two-lines         M49  the erratum is wrapped onto two lines   -> line_count=2
  d5-m50-label-altered     M50  the line does not start with the label  -> labelled=False
  d5-m51-require-missing   M51  required token dropped, forbid not added
  d5-m52-forbid-present    M52  forbidden token added, required token kept
  d5-m53-capture-missing   M53  capture dir has no capture file         -> "capture unreadable"
  d5-m55-quote-absent      M55  capture bytes lack the quote, manifest digest rewritten to the
                                new bytes (so the digest pin passes and only the quote check fires)

Every fixture is a reject whose only DEFECT clause is D5. Builders write inside the empty dir `d`
and return the gate argv tail; nothing keys on the fixture's directory name.

D5 mutants M54 (digest not in the manifest) is already demonstrated by the frozen round-36 battery
(r36-L6), so it has no fixture here.
"""
import hashlib
import shutil


def _capture_files(ctx):
    d5 = ctx.spec["d5"]
    return d5["capture_name"], d5["manifest_name"]


def _copy_capture(ctx, d):
    """Copy the two files `cmd_d5` reads (capture + manifest) into d/caps and return that dir."""
    src = ctx.d5_capture_dir()
    cap = d / "caps"
    cap.mkdir()
    for name in _capture_files(ctx):
        shutil.copyfile(src / name, cap / name)
    return cap


def _write(d, name, text):
    f = d / name
    if not text.endswith("\n"):
        text += "\n"
    f.write_text(text)
    return f


def _argv(f, cap):
    return ["d5-line", "--file", str(f), "--capture-dir", str(cap)]


def _genuine_line(ctx):
    line = ctx.d5_line()
    label = ctx.spec["d5"]["label"]
    require = ctx.spec["d5"]["require"]
    forbid = ctx.spec["d5"]["forbid"]
    assert line.startswith(label), "genuine d5 line does not carry the spec label"
    assert require in line and forbid not in line, "genuine d5 line tokens changed"
    return line


# -- M48: the file the gate is pointed at does not exist -------------------------------------------------
def build_m48(ctx, d):
    cap = _copy_capture(ctx, d)
    return _argv(d / "no-such-erratum.txt", cap)


# -- M49: the erratum is wrapped, so the file holds two non-blank lines -----------------------------------
def build_m49(ctx, d):
    cap = _copy_capture(ctx, d)
    line = _genuine_line(ctx)
    head, sep, tail = line.partition(" in this round's own reopen capture ")
    assert sep, "split anchor absent from the genuine d5 line"
    assert ctx.spec["d5"]["require"] in head and ctx.spec["d5"]["forbid"] not in head
    f = _write(d, "erratum.txt", head + "\n" + (sep + tail).rstrip())
    return _argv(f, cap)


# -- M50: same single line, label changed ----------------------------------------------------------------
def build_m50(ctx, d):
    cap = _copy_capture(ctx, d)
    line = _genuine_line(ctx)
    label = ctx.spec["d5"]["label"]
    alt = label.replace("round 35", "round 34")
    assert alt != label
    f = _write(d, "erratum.txt", alt + line[len(label):])
    return _argv(f, cap)


# -- M51: required token dropped, forbidden token never introduced ----------------------------------------
def build_m51(ctx, d):
    cap = _copy_capture(ctx, d)
    line = _genuine_line(ctx)
    require = ctx.spec["d5"]["require"]
    forbid = ctx.spec["d5"]["forbid"]
    assert line.count(require) == 1
    mutated = line.replace(require, "is here", 1)
    assert require not in mutated and forbid not in mutated
    f = _write(d, "erratum.txt", mutated)
    return _argv(f, cap)


# -- M52: forbidden token added while the required token stays --------------------------------------------
def build_m52(ctx, d):
    cap = _copy_capture(ctx, d)
    line = _genuine_line(ctx)
    require = ctx.spec["d5"]["require"]
    forbid = ctx.spec["d5"]["forbid"]
    mutated = line + " The quote is not present in the 418-byte fetch."
    assert require in mutated and forbid in mutated
    f = _write(d, "erratum.txt", mutated)
    return _argv(f, cap)


# -- M53: capture directory without the capture file (manifest still there) -------------------------------
def build_m53(ctx, d):
    cap = _copy_capture(ctx, d)
    name, _manifest = _capture_files(ctx)
    (cap / name).unlink()
    f = _write(d, "erratum.txt", _genuine_line(ctx))
    return _argv(f, cap)


# -- M55: capture bytes without the quote, manifest digest rewritten to those bytes -----------------------
def build_m55(ctx, d):
    cap = _copy_capture(ctx, d)
    name, manifest = _capture_files(ctx)
    quote = ctx.spec["d5"]["quote"]
    capture = cap / name
    text = capture.read_text()
    assert quote in text, "quote not found verbatim in the genuine capture"
    capture.write_text(text.replace(quote, "（引用は削除されました）", 1))
    digest = hashlib.sha256(capture.read_bytes()).hexdigest()
    assert quote not in capture.read_text()
    (cap / manifest).write_text(f"{digest}  {ctx.spec['d5_capture_dir']}/{name}\n")
    f = _write(d, "erratum.txt", _genuine_line(ctx))
    return _argv(f, cap)


FIXTURES = [
    {"fid": "d5-m48-file-unreadable", "expect": "reject", "defects": ["D5"], "build": build_m48},
    {"fid": "d5-m49-two-lines", "expect": "reject", "defects": ["D5"], "build": build_m49},
    {"fid": "d5-m50-label-altered", "expect": "reject", "defects": ["D5"], "build": build_m50},
    {"fid": "d5-m51-require-missing", "expect": "reject", "defects": ["D5"], "build": build_m51},
    {"fid": "d5-m52-forbid-present", "expect": "reject", "defects": ["D5"], "build": build_m52},
    {"fid": "d5-m53-capture-missing", "expect": "reject", "defects": ["D5"], "build": build_m53},
    {"fid": "d5-m55-quote-absent", "expect": "reject", "defects": ["D5"], "build": build_m55},
]
