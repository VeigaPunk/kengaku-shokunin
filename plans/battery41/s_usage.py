"""Round-41 C1 battery (seat R41BatSrcUsage): the registry-mode usage refusals of sources_adopt.py.

Every fixture is one registry-mode invocation of `plans/sources_adopt.py` whose reference run is the
advertised usage error (exit 2, `SKILL.md:573` "2 usage error") and whose frozen mutant of the same
branch exits differently in the declared direction: S02 2>1, S03 2>5, S05 2>0, S06 2>0. The sources
tool has no pass/fail classes, so every `defects` list is empty by contract (the counter refuses a
non-empty one). Shapes are deliberately not the pre-freeze witness's: a lane-shaped tree with a
two-row `corpus/SOURCES.md` registry and a `SOURCES.append.md` package, two triggers per guard where
the guard has two operands, and one scoped package whose prose recheck the CLI default would rewrite.
"""
from __future__ import annotations

HEADER = (
    "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
)


def row(rid, source, *, kind="docs", tier="A", status="mined", opened="2026-10-26",
        recheck="180d", used_by="corpus/knowledge/tb2-constraints-scheduling-grader.md"):
    return (
        f"| {rid} | {source} | {kind} | {tier} | one fixture scope | anchor text | fixture teaches one "
        f"refusal | {status} | {opened} | {recheck} | {used_by} |\n"
    )


REG_S118 = row(
    "S118",
    "Terminal-Bench 2.0 build-pmars task instruction (instruction.md) — "
    "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/build-pmars/instruction.md",
    opened="2026-10-19",
)
REG_S124 = row(
    "S124",
    "Terminal-Bench 2.1 PR #245 — https://github.com/harbor-framework/terminal-bench-2-1/pull/245",
    status="queued",
    recheck="on-release",
)
PKG_S131 = row("S131", "Round-41 battery source A — https://example.invalid/r41/a")
PKG_S132 = row("S132", "Round-41 battery source B — https://example.invalid/r41/b", recheck="90d")
PKG_S133 = row(
    "S133",
    "Round-41 battery source C — https://example.invalid/r41/c",
    recheck="2026-10-26 — re-verify at next release",
)


def tree(ctx, d, pkg_rows):
    """A lane-shaped tree: a committed two-row registry plus a package append table."""
    reg = d / "corpus" / "SOURCES.md"
    pkg = d / "corpus" / "SOURCES.append.md"
    ctx.write(reg, "# SOURCES — where kengaku learns\n\nRound 41 fixture registry, two rows.\n\n"
                   + HEADER + REG_S118 + REG_S124)
    ctx.write(pkg, HEADER + "".join(pkg_rows))
    return reg, pkg


ENTRY = "corpus/knowledge/tb2-constraints-scheduling-grader.md"


def b02a(ctx, d):
    # S02 first operand: `--package` omitted, every other flag of a real adoption present.
    reg, _pkg = tree(ctx, d, [PKG_S131])
    return ["--registry", str(reg), "--admit-ids", "S131", "--entries", ENTRY,
            "--access-date", "2026-10-26"]


def b02b(ctx, d):
    # S02 second operand: `--registry` omitted, the package table present and readable.
    _reg, pkg = tree(ctx, d, [PKG_S131])
    return ["--package", str(pkg), "--admit-ids", "S131", "--entries", ENTRY,
            "--access-date", "2026-10-26"]


def b03a(ctx, d):
    # S03 via the opened cell: a dotted date is refused as usage before any row is built.
    reg, pkg = tree(ctx, d, [PKG_S131, PKG_S132])
    return ["--registry", str(reg), "--package", str(pkg), "--admit-ids", "S131,S132",
            "--entries", ENTRY, "--access-date", "26.10.2026"]


def b03b(ctx, d):
    # S03 second trigger: a single-digit month is not ISO, and the request is a duplicate id.
    reg, pkg = tree(ctx, d, [PKG_S131])
    return ["--registry", str(reg), "--package", str(pkg), "--admit-ids", "S131,S131",
            "--entries", ENTRY, "--access-date", "2026-1-5"]


def b05a(ctx, d):
    # S05: `--admit-ids` with no `--entries` for two requested ids (used-by has no fallback).
    reg, pkg = tree(ctx, d, [PKG_S131, PKG_S132])
    return ["--registry", str(reg), "--package", str(pkg), "--admit-ids", "S131,S132",
            "--access-date", "2026-10-26"]


def b05b(ctx, d):
    # S05 second shape: the flag is given but empty, which is the same refusal (`not args.entries`).
    reg, pkg = tree(ctx, d, [PKG_S131])
    return ["--registry", str(reg), "--package", str(pkg), "--admit-ids", "S131", "--entries", "",
            "--access-date", "2026-10-26"]


def b06a(ctx, d):
    # S06 plain rows: a cadence word the symbolic set does not know is refused as usage.
    reg, pkg = tree(ctx, d, [PKG_S131])
    return ["--registry", str(reg), "--package", str(pkg), "--admit-ids", "S131", "--entries", ENTRY,
            "--access-date", "2026-10-26", "--recheck", "monthly"]


def b06b(ctx, d):
    # S06 scoped prose row: the CLI default would rewrite the prose cell, so the recheck is checked.
    reg, pkg = tree(ctx, d, [PKG_S133])
    return ["--registry", str(reg), "--package", str(pkg), "--admit-ids", "S133", "--entries", ENTRY,
            "--access-date", "2026-10-26", "--recheck", "every 30 days", "--scope-to-admit"]


def fx(fid, expect, build):
    return {"fid": fid, "tool": "sources", "expect": expect, "defects": [], "build": build}


FIXTURES = [
    fx("s_usage-02-registry-without-package", "error", b02a),
    fx("s_usage-02-package-without-registry", "error", b02b),
    fx("s_usage-03-dotted-access-date", "error", b03a),
    fx("s_usage-03-single-digit-month-duplicate-request", "error", b03b),
    fx("s_usage-05-two-ids-without-entries", "error", b05a),
    fx("s_usage-05-empty-entries-value", "error", b05b),
    fx("s_usage-06-recheck-cadence-word", "error", b06a),
    fx("s_usage-06-recheck-prose-scoped-row", "error", b06b),
]
