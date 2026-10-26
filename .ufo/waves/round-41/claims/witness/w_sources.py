"""Pre-freeze witnesses for the round-41 sources-adopt CLI mutants (L1 KengakuR41). Not the battery."""

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")
ROW = ("| S900 | fixture source — https://example.invalid/x | docs | A | fixture scope | "
       "{anchor} | fixture teaches | {status} | 2026-10-25 | 180d | corpus/knowledge/old.md |\n")


def row(anchor="anchor text", status="mined"):
    return ROW.format(anchor=anchor, status=status)


def files(ctx, d, reg_rows="", pkg_rows=None):
    ctx.write(d / "reg.md", HEADER + reg_rows)
    ctx.write(d / "pkg.md", HEADER + (row() if pkg_rows is None else pkg_rows))
    return ["--registry", str(d / "reg.md"), "--package", str(d / "pkg.md")]


def quote(ctx, d):
    ctx.write(d / "q.md", HEADER + row(anchor='l.1: "fixture quote words here" (4 words)'))
    ctx.write(d / "art.txt", "some text with fixture quote words here inside\n")
    return ["--quote-file", str(d / "q.md"), "--artifact", str(d / "art.txt")]


ADMIT = ["--admit-ids", "S900", "--entries", "corpus/knowledge/x.md", "--access-date", "2026-10-25"]


def b01(ctx, d):
    ctx.write(d / "reg.md", HEADER)
    return quote(ctx, d) + ["--registry", str(d / "reg.md")]


def b02(ctx, d):
    return []


def b03(ctx, d):
    return files(ctx, d) + ["--admit-ids", "S900", "--entries", "corpus/knowledge/x.md", "--access-date",
                            "2026/10/25"]


def b04(ctx, d):
    ctx.write(d / "m.json", "{}\n")
    return files(ctx, d) + ["--url-map", str(d / "m.json")]


def b05(ctx, d):
    return files(ctx, d) + ["--admit-ids", "S900", "--access-date", "2026-10-25"]


def b06(ctx, d):
    return files(ctx, d) + ADMIT + ["--recheck", "soon"]


def b07(ctx, d):
    return files(ctx, d, reg_rows=row()) + ADMIT


def b08(ctx, d):
    ctx.write(d / "q.md", HEADER + row(anchor='l.1: "fixture quote words here" (4 words)'))
    return ["--quote-file", str(d / "q.md")]


def b09(ctx, d):
    return quote(ctx, d) + ["--url-map", str(d / "absent.json")]


def b11(ctx, d):
    return files(ctx, d, pkg_rows=row(status="queued")) + ADMIT


def fx(fid, expect, build):
    return {"fid": fid, "tool": "sources", "expect": expect, "defects": [], "build": build}


FIXTURES = [
    fx("w-s01-quote-plus-registry", "error", b01),
    fx("w-s02-no-arguments", "error", b02),
    fx("w-s03-slash-date", "error", b03),
    fx("w-s04-url-map-with-registry", "error", b04),
    fx("w-s05-admit-without-entries", "error", b05),
    fx("w-s06-recheck-soon", "error", b06),
    fx("w-s07-collision-with-admit", "exit-3", b07),
    fx("w-s08-quote-file-alone", "error", b08),
    fx("w-s09-url-map-unreadable", "error", b09),
    fx("w-s11-queued-row", "exit-5", b11),
]
