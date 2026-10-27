"""Draft hostile f7 (R44MutC1Fences, AS2 demonstrator): anchor argv using an argparse abbreviation.

All six hostile modules are order-tool modules, so the anchor half of argv_shape_breach (the
exact-option token check) has no hostile coverage at all. This module is an honest anchor lane
(capture + corpus/SOURCES.md row citing its digest) whose argv appends `--verb`, an unambiguous
argparse abbreviation of `--verbose`.
Expected: pristine refuses ("anchor argv token '--verb' is not an exact option"); AS2 mutant
degrades to an accidental KeyError refusal from the consume step (SETUP "'--verb'") — the guard
survives by accident, not by design."""
import hashlib
import pathlib

BODY = b"draft f7 anchor capture seven\n"
DIG = hashlib.sha256(BODY).hexdigest()
HEAD = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n")
ROW = ("| S707 | corpus/knowledge/draft7.md | docs | A | scope | anchor sha256 " + DIG +
       " | teaches | mined | 2026-10-26 | 2027-01-24 | corpus/knowledge/draft7.md |\n")


def build(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(pathlib.Path(d) / "lane" / "corpus/evidence/r7/cap.txt", BODY)
    ctx.write(pathlib.Path(d) / "lane" / "corpus/SOURCES.md", HEAD + ROW)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "fixture")
    return ["--lane", str(r), "--verb"]


FIXTURES = [{"fid": "f7-anchor-abbrev", "tool": "anchor", "expect": "accept", "defects": [], "build": build}]
