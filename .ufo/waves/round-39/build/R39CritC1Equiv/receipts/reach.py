#!/usr/bin/env python3
"""Critic-side battery39 probe (NOT for landing): one fixture per surviving frozen mutant, built only
from the documented Ctx surface, to show the four declared directions are reachable inside the frozen
counter's own machinery.

  reach-pin2      M02 P1 silence     genuine package + off-pin byte in the SECOND frozen instrument
  reach-words26   M03 P3 silence     first quote row rewritten to hi+1 words
  reach-srcline   M04 P7 silence     a stale duplicate `source: Sxxx` line appended to the entry
  reach-d5tag     M07 D5 mirror      a tag inside the D5 quote span, manifest re-pinned
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import shutil

ROW = re.compile(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$")


def _genuine(ctx, d):
    d = pathlib.Path(d)
    ctx.genuine_package(d)
    return d


def build_pin2(ctx, d):
    d = _genuine(ctx, d)
    rel = list(ctx.spec["frozen_instruments"])[1]
    f = d / rel
    f.write_text(f.read_text() + "\n# off-pin witness byte\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def build_words26(ctx, d):
    d = _genuine(ctx, d)
    _, hi = ctx.spec["entry_rules"]["quote_words"]
    entry = d / pathlib.PurePosixPath(ctx.spec["entry"])
    lines = entry.read_text().splitlines()
    out, done = [], False
    for line in lines:
        m = ROW.match(line)
        if m and not done:
            cells = line.split("|")
            text = " ".join([f"w{i}" for i in range(1, hi + 2)])
            out.append(f'| {cells[1].strip()} | “{text}” | `{m.group(2)}:{m.group(3)}` |')
            done = True
        else:
            out.append(line)
    entry.write_text("\n".join(out) + "\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def build_srcline(ctx, d):
    d = _genuine(ctx, d)
    entry = d / pathlib.PurePosixPath(ctx.spec["entry"])
    text = entry.read_text()
    sid = sorted(ctx.spec["rows"])[0]
    line = next(l for l in text.splitlines() if l.startswith(f"source: {sid}"))
    url = re.search(r"https?://\S+", line).group(0)
    entry.write_text(text + "\n" + line.replace(url, url + "-stale") + "\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def build_d5tag(ctx, d):
    d = pathlib.Path(d)
    cd = d / "captures"
    shutil.copytree(ctx.d5_capture_dir(), cd)
    name = ctx.spec["d5"]["capture_name"]
    man = ctx.spec["d5"]["manifest_name"]
    quote = ctx.spec["d5"]["quote"]
    raw = (cd / name).read_text()
    win = next(quote[j:j + 10] for j in range(len(quote) - 10) if quote[j:j + 10] in raw)
    at = raw.index(win)
    (cd / name).write_text(raw[:at + 4] + "<b></b>" + raw[at + 4:])
    digest = hashlib.sha256((cd / name).read_bytes()).hexdigest()
    rows = (cd / man).read_text().splitlines()
    rows = [f"{digest}  {name}" if l.split() and l.split()[-1].endswith(name) else l for l in rows]
    (cd / man).write_text("\n".join(rows) + "\n")
    line = d / "erratum.md"
    line.write_text(ctx.d5_line() + "\n")
    return ["d5-line", "--file", str(line), "--capture-dir", str(cd)]


FIXTURES = [
    {"fid": "reach-pin2", "expect": "reject", "defects": ["P1"], "build": build_pin2},
    {"fid": "reach-words26", "expect": "reject", "defects": ["P3", "P4"], "build": build_words26},
    {"fid": "reach-srcline", "expect": "reject", "defects": ["P7"], "build": build_srcline},
    {"fid": "reach-d5tag", "expect": "accept", "defects": [], "build": build_d5tag},
]
