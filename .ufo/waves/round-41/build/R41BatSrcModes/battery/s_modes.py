"""battery41 module: the three mode-exclusivity guards and the unreadable-map refusal of
`plans/sources_adopt.py`'s CLI (frozen mutants S01, S04, S08, S09).

Every fixture is one unmodified-tool behaviour, in a lane-shaped tree under the fixture
directory: `corpus/SOURCES.md`, `corpus/SOURCES.append.md`, `corpus/knowledge/`, and a
capture tree `corpus/evidence/r41-captures/` whose files `load_artifact` reads in sorted
order. `expect` is the reference exit class; `defects` is empty because the sources tool's
class set is always empty. Nothing here reads another module, a witness or the lane.
"""

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")

QUOTE = "an adopted row is checked before it is appended"  # 9 words, the located span below
CITED = "https://example.invalid/r41/spec"


def row(rid="S905", url=CITED, anchor="anchor text", status="mined", opened="2026-10-26",
        recheck="180d", used="corpus/knowledge/r41-fixture.md"):
    """One 11-cell registry row in the census shape the gate parses."""
    return (f"| {rid} | {url} | docs | A | r41 fixture scope | {anchor} | fixture teaches one row | "
            f"{status} | {opened} | {recheck} | {used} |\n")


def anchor(cell="p.12"):
    """An anchor cell carrying the located quote, as the live registry writes it."""
    return f'{cell}: "{QUOTE}" (9 words)'


def lane_tree(ctx, d):
    """The realistic tree every fixture shares: a knowledge entry and a two-file capture
    directory whose decoy sorts before the capture that really holds the quote."""
    ctx.write(d / "corpus" / "knowledge" / "r41-fixture.md", "# fixture knowledge entry\n")
    ctx.write(d / "corpus" / "evidence" / "r41-captures" / "a-notes.md",
              "unrelated capture bytes; the quote is not on this line\n")
    ctx.write(d / "corpus" / "evidence" / "r41-captures" / "b-capture.txt",
              f"intro line\n{QUOTE}\nsuffix line\n")
    return str(d / "corpus" / "evidence" / "r41-captures")


def quote_file(ctx, d, rid="S901", url=CITED):
    """The rows file quote mode validates: one row whose anchor cell carries the quote."""
    ctx.write(d / "corpus" / "knowledge" / "quotes-r41.md", HEADER + row(rid=rid, url=url, anchor=anchor()))
    return str(d / "corpus" / "knowledge" / "quotes-r41.md")


def registry_pair(ctx, d, staged=None):
    """A live registry with two admitted rows plus an append package for this round."""
    ctx.write(d / "corpus" / "SOURCES.md",
              HEADER + row(rid="S001", url="https://example.invalid/r41/one", anchor="first live anchor")
              + row(rid="S002", url="https://example.invalid/r41/two", anchor="second live anchor"))
    ctx.write(d / "corpus" / "SOURCES.append.md",
              HEADER + (row(rid="S905", anchor="a staged row for this round") if staged is None else staged))
    return [str(d / "corpus" / "SOURCES.md"), str(d / "corpus" / "SOURCES.append.md")]


# ------------------------------------------------------------------------------- builders

def b_s01_package(ctx, d):
    # S01: quote mode combined with --package. The exclusivity guard refuses (2); an unguarded
    # run silently drops the package work, validates the quote and exits 0.
    art = lane_tree(ctx, d)
    registry_pair(ctx, d)
    return ["--quote-file", quote_file(ctx, d), "--artifact", art,
            "--package", str(d / "corpus" / "SOURCES.append.md")]


def b_s01_both(ctx, d):
    # S01 second trigger: quote mode with BOTH --registry and --package, and a --url-map that
    # would bind the quote correctly -- a combined invocation must still refuse (2), not exit 0.
    art = lane_tree(ctx, d)
    registry_pair(ctx, d)
    ctx.write(d / "corpus" / "evidence" / "r41-url-map.json", '{"b-capture.txt": "' + CITED + '"}\n')
    return ["--quote-file", quote_file(ctx, d, rid="S902"), "--artifact", art,
            "--registry", str(d / "corpus" / "SOURCES.md"),
            "--package", str(d / "corpus" / "SOURCES.append.md"),
            "--url-map", str(d / "corpus" / "evidence" / "r41-url-map.json")]


def b_s04_adopt(ctx, d):
    # S04: --url-map in registry mode with a complete adopt request. The ignored-map guard
    # refuses (2); an unguarded run checks, builds the block and exits 0.
    reg, pkg = registry_pair(ctx, d)
    ctx.write(d / "plans" / "url-map-r41.json", '{"b-capture.txt": "' + CITED + '"}\n')
    return ["--registry", reg, "--package", pkg,
            "--admit-ids", "S905", "--entries", "corpus/knowledge/r41-fixture.md",
            "--access-date", "2026-10-26", "--url-map", str(d / "plans" / "url-map-r41.json")]


def b_s04_check(ctx, d):
    # S04 second trigger: --url-map with a clean check and no --admit-ids. Reference refuses (2);
    # the unguarded run reports the registry counts and exits 0 on the check alone.
    ctx.write(d / "corpus" / "knowledge" / "r41-fixture.md", "# fixture knowledge entry\n")
    reg, pkg = registry_pair(ctx, d,
                             staged=row(rid="S906", anchor="a second staged row")
                             + row(rid="S907", anchor="a third staged row"))
    ctx.write(d / "plans" / "url-map-r41.json", '{"b-capture.txt": "' + CITED + '"}\n')
    return ["--registry", reg, "--package", pkg,
            "--url-map", str(d / "plans" / "url-map-r41.json")]


def b_s08_quote_only(ctx, d):
    # S08: --quote-file without --artifact (plus a readable map). The pairing guard refuses (2);
    # an unguarded run reaches the quote check with no artifact and dies on it (1).
    lane_tree(ctx, d)
    ctx.write(d / "corpus" / "evidence" / "r41-url-map.json", '{"b-capture.txt": "' + CITED + '"}\n')
    return ["--quote-file", quote_file(ctx, d, rid="S903"),
            "--url-map", str(d / "corpus" / "evidence" / "r41-url-map.json")]


def b_s08_artifact_only(ctx, d):
    # S08 second trigger from the other side: --artifact without --quote-file. Pairing guard
    # refuses (2); the unguarded run loads the capture then dies on the absent rows file (1).
    art = lane_tree(ctx, d)
    return ["--artifact", art]


def b_s09_nested(ctx, d):
    # S09: an unreadable --url-map whose shape is a nested object. The map problem is refused
    # (2) before the quote is judged; unguarded, the empty map leaves the located quote
    # unmapped and the run exits 9.
    art = lane_tree(ctx, d)
    ctx.write(d / "corpus" / "evidence" / "r41-url-map.json",
              '{"b-capture.txt": {"url": "' + CITED + '"}}\n')
    return ["--quote-file", quote_file(ctx, d, rid="S908"), "--artifact", art,
            "--url-map", str(d / "corpus" / "evidence" / "r41-url-map.json")]


def b_s09_directory(ctx, d):
    # S09 second trigger: --url-map naming a directory is unreadable at the filesystem level
    # (OSError, not JSON shape), refused as 2; unguarded it becomes an empty map, so the
    # located quote is unmapped (9).
    art = lane_tree(ctx, d)
    ctx.write(d / "corpus" / "evidence" / "r41-url-maps" / "inner.json", "{}\n")
    return ["--quote-file", quote_file(ctx, d, rid="S909"), "--artifact", art,
            "--url-map", str(d / "corpus" / "evidence" / "r41-url-maps")]


def fx(fid, expect, build):
    return {"fid": fid, "tool": "sources", "expect": expect, "defects": [], "build": build}


FIXTURES = [
    fx("s_modes-s01-quote-plus-package", "error", b_s01_package),
    fx("s_modes-s01-quote-plus-registry-and-package", "error", b_s01_both),
    fx("s_modes-s04-url-map-with-adopt", "error", b_s04_adopt),
    fx("s_modes-s04-url-map-with-check-only", "error", b_s04_check),
    fx("s_modes-s08-quote-file-without-artifact", "error", b_s08_quote_only),
    fx("s_modes-s08-artifact-without-quote-file", "error", b_s08_artifact_only),
    fx("s_modes-s09-url-map-nested-shape", "error", b_s09_nested),
    fx("s_modes-s09-url-map-directory", "error", b_s09_directory),
]
