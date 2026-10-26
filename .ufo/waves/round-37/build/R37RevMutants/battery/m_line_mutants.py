"""R37RevMutants review battery: d4-line / d5-line fixtures for M44-M46 and M48-M55."""
import hashlib
import shutil


def _d5_env(ctx, d):
    cap = d / "cap"
    shutil.copytree(ctx.d5_capture_dir(), cap)
    return cap


def _d5_file(ctx, d, text):
    f = d / "d5-line.txt"
    f.write_text(text)
    return f


def _rewrite_quarantine(cap, name, digest):
    m = cap / "quarantine-SHA256SUMS"
    m.write_text("".join((digest + l[len(l.split()[0]):] + "\n") if l.split()[-1].endswith(name) else l + "\n"
                         for l in m.read_text().splitlines()))


# ---- D4 -----------------------------------------------------------------------------

def _m44(ctx, d):
    return ["d4-line", "--file", str(d / "absent-d4.txt")]


def _m45(ctx, d):
    f = d / "d4-two-lines.txt"
    f.write_text(ctx.d4_line() + "\nsecond line present\n")
    return ["d4-line", "--file", str(f)]


def _m46(ctx, d):
    f = d / "d4-nolabel.txt"
    f.write_text(ctx.d4_line()[2:] + "\n")  # strip the leading "- "
    return ["d4-line", "--file", str(f)]


# ---- D5 -----------------------------------------------------------------------------

def _m48(ctx, d):
    return ["d5-line", "--file", str(d / "absent-d5.txt"), "--capture-dir", str(d / "cap")]


def _m49(ctx, d):
    cap = _d5_env(ctx, d)
    f = _d5_file(ctx, d, ctx.d5_line() + "\nsecond line present\n")
    return ["d5-line", "--file", str(f), "--capture-dir", str(cap)]


def _m50(ctx, d):
    cap = _d5_env(ctx, d)
    f = _d5_file(ctx, d, ctx.d5_line().replace("Erratum", "Xrratum", 1) + "\n")
    return ["d5-line", "--file", str(f), "--capture-dir", str(cap)]


def _m51(ctx, d):
    cap = _d5_env(ctx, d)
    f = _d5_file(ctx, d, ctx.d5_line().replace("is present", "was present", 1) + "\n")
    return ["d5-line", "--file", str(f), "--capture-dir", str(cap)]


def _m52(ctx, d):
    cap = _d5_env(ctx, d)
    f = _d5_file(ctx, d, ctx.d5_line() + " An earlier draft wrongly said not present.\n")
    return ["d5-line", "--file", str(f), "--capture-dir", str(cap)]


def _m53(ctx, d):
    cap = _d5_env(ctx, d)
    (cap / ctx.spec["d5"]["capture_name"]).unlink()
    f = _d5_file(ctx, d, ctx.d5_line() + "\n")
    return ["d5-line", "--file", str(f), "--capture-dir", str(cap)]


def _m55(ctx, d):
    cap = _d5_env(ctx, d)
    name = ctx.spec["d5"]["capture_name"]
    p = cap / name
    lines = p.read_text().splitlines()
    hit = [i for i, l in enumerate(lines) if "RAKUDA" in l]
    for i in hit:
        lines[i] = "<p>sentence removed</p>"
    p.write_text("\n".join(lines) + "\n")
    _rewrite_quarantine(cap, name, hashlib.sha256(p.read_bytes()).hexdigest())
    f = _d5_file(ctx, d, ctx.d5_line() + "\n")
    return ["d5-line", "--file", str(f), "--capture-dir", str(cap)]


FIXTURES = [
    {"fid": "rev-m44-d4-file-gone", "expect": "reject", "defects": ["D4"], "build": _m44},
    {"fid": "rev-m45-d4-two-lines", "expect": "reject", "defects": ["D4"], "build": _m45},
    {"fid": "rev-m46-d4-nolabel", "expect": "reject", "defects": ["D4"], "build": _m46},
    {"fid": "rev-m48-d5-file-gone", "expect": "reject", "defects": ["D5"], "build": _m48},
    {"fid": "rev-m49-d5-two-lines", "expect": "reject", "defects": ["D5"], "build": _m49},
    {"fid": "rev-m50-d5-nolabel", "expect": "reject", "defects": ["D5"], "build": _m50},
    {"fid": "rev-m51-d5-require", "expect": "reject", "defects": ["D5"], "build": _m51},
    {"fid": "rev-m52-d5-forbid", "expect": "reject", "defects": ["D5"], "build": _m52},
    {"fid": "rev-m53-d5-capture-gone", "expect": "reject", "defects": ["D5"], "build": _m53},
    {"fid": "rev-m55-d5-quote-gone", "expect": "reject", "defects": ["D5"], "build": _m55},
]
