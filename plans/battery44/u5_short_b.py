"""Round-44 C1 battery (seat R44BatU5b): fixtures for frozen mutant U5 of `plans/round44_c1_verify.py`.

U5 (`tool=anchor`, `class=digest-short`, direction `silence`, `direct`) replaces the anchor token-length
branch of `plans/anchor_digest_check.py` so that a token shorter than 64 hex digits is labelled
`digest-long`; the unmodified tool must print `class=digest-short` for an anchor-cell token of 8-63
lowercase hex digits with no ellipsis (`anchor_digest_check.py:88`). Every fixture below reaches that
branch through a different registry shape and declares exactly the class set the unmodified tool prints
on it (`["digest-short"]`, exit 1). Each fixture is built from nothing inside its own directory.
"""

import hashlib

HEADER = (
    "# `corpus/SOURCES.md` (fixture registry)\n\n"
    "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
)
SHA = "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"
RAW = "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/" + SHA + "/"


def _row(sid, source, scope, anchor="-", teaches="-", status="mined"):
    """One census-shaped 11-cell row: id, source, kind, tier, scope, anchor, teaches, status, opened,
    recheck, used-by. The anchor token (if any) is cell 6, which is the cell the tool reads."""
    cells = [sid, source, "task", "A", scope, anchor, teaches, status, "2026-10-26", "-", "-"]
    return "| " + " | ".join(cells) + " |\n"


def _digest(blob):
    return hashlib.sha256(blob.encode()).hexdigest()


def build_registry_url_task(ctx, d):
    """Six-row registry: a 63-hex token in a row bound through a pinned upstream URL (url-task binding)."""
    ctx.init(d)
    orbital = "corpus/evidence/round36/tb2-orbital-log"
    ctx.write(d / orbital / "task.toml", 'name = "harbor/orbital-log"\n')
    ctx.write(d / orbital / "test_outputs.py", "def test_gravity():\n    assert 2 + 2 == 4\n")
    shard = "corpus/evidence/round36/tb2-shard-log"
    ctx.write(d / shard / "task.toml", 'name = "harbor/shard-log"\n')
    sums = "0f" * 32 + "  log.txt\n"
    ctx.write(d / shard / "SHA256SUMS", sums)
    ctx.write(d / shard / "log.txt", "shard 7 replay: 12 lines, 0 errors\n")
    ctx.write(d / "corpus/SOURCES.md", HEADER + "".join([
        _row("S136", RAW + "orbital-log/tests/test_outputs.py", "gravity assertions", "-"),
        _row("S137", "lane ledger, no locator", "held by the census", "-"),
        _row("S138", RAW + "orbital-log/tests/test_outputs.py", "gravity assertions",
             "sha256 `" + "e" * 63 + "`"),
        _row("S139", RAW + "shard-log/SHA256SUMS", "replay manifest", "sha256 `" + _digest(sums) + "`"),
        _row("S140", "corpus/evidence/round36/tb2-shard-log/log.txt", "replay log", "-"),
        _row("S141", "prose only", "no locator", "-"),
    ]))
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-q", "-m", "fixture registry")
    return ["--lane", "."]


def build_index_ref_staged(ctx, d):
    """Minimal registry read with `--evidence-ref index`: the short token names a capture that is staged only."""
    ctx.init(d)
    base = "corpus/evidence/round44/u5b-base/notes.md"
    ctx.write(d / base, "base capture\n")
    ctx.write(d / "corpus/SOURCES.md", HEADER
              + _row("S201", base, "base run", "-")
              + _row("S202", "lane ledger, no locator", "pending", "-"))
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-q", "-m", "base")
    staged = "corpus/evidence/round44/u5b-staged/alpha.log"
    ctx.write(d / staged, "staged capture: replay 9\n")
    ctx.git(d, "add", staged)
    ctx.write(d / "corpus/SOURCES.md", HEADER
              + _row("S201", base, "base run", "-")
              + _row("S202", staged, "replay 9", "sha256 `" + "0badc0de" + "`"))
    return ["--lane", ".", "--evidence-ref", "index"]


def build_lane_path_manifest(ctx, d):
    """Nine-row registry read with `--verbose`: one row resolves via a stale SHA256SUMS entry, one carries a 40-hex token."""
    ctx.init(d)
    cap = "corpus/evidence/round44/u5b-manifest"
    report = "replay 1: 40 lines\nreplay 2: 41 lines\n"
    ctx.write(d / cap / "report.md", report)
    stale = hashlib.sha256(b"replay 1: 39 lines\n").hexdigest()
    ctx.write(d / cap / "SHA256SUMS", stale + "  report.md\n")
    ctx.write(d / "corpus/SOURCES.md", HEADER + "".join([
        _row("S296", "lane ledger, no locator", "carried", "-"),
        _row("S297", "corpus/evidence/round44/u5b-manifest/report.md", "replay 1 and 2", "-"),
        _row("S298", "prose only", "no locator", "-"),
        _row("S299", "corpus/evidence/round44/u5b-manifest", "directory, not a capture", "-"),
        _row("S300", "corpus/evidence/round44/u5b-manifest/report.md", "replay 2 only", "-"),
        _row("S301", "corpus/evidence/round44/u5b-manifest/report.md", "replay 1 only",
             "sha256 `" + stale + "`"),
        _row("S302", "corpus/evidence/round44/u5b-manifest/report.md", "replay 1 and 2",
             "sha256 `" + "0123456789abcdef0123456789abcdef01234567" + "`"),
        _row("S303", "prose only", "no locator", "-"),
        _row("S304", "lane ledger, no locator", "carried", "-"),
    ]))
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-q", "-m", "fixture registry with manifest")
    return ["--lane", ".", "--verbose"]


def build_history_truncation(ctx, d):
    """Two commits: the anchored row is correct at the first, then truncated to 20 hex by a later review commit."""
    ctx.init(d)
    cap = "corpus/evidence/round44/u5b-history/probe.log"
    probe = "probe 0: linear bias 0.03125\nprobe 1: linear bias 0.0234375\n"
    ctx.write(d / cap, probe)
    full = _digest(probe)

    def registry(token):
        return HEADER + _row("S400", cap, "probe replay", "sha256 `" + token + "`") \
            + _row("S401", "lane ledger, no locator", "carried", "-")

    ctx.write(d / "corpus/SOURCES.md", registry(full))
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-q", "-m", "probe capture and anchored row")
    ctx.write(d / "corpus/SOURCES.md", registry(full[:20]))
    ctx.git(d, "add", "corpus/SOURCES.md")
    ctx.git(d, "commit", "-q", "-m", "registry review: shorten anchor")
    return ["--lane", "."]


FIXTURES = [
    # multi-row registry whose short token binds through a pinned upstream URL (url-task route)
    {"fid": "u5_short_b-registry-url-task", "tool": "anchor", "expect": "reject",
     "defects": ["digest-short"], "build": build_registry_url_task},
    # staged-only capture read with --evidence-ref index, 8-hex token at the short boundary
    {"fid": "u5_short_b-index-ref-staged", "tool": "anchor", "expect": "reject",
     "defects": ["digest-short"], "build": build_index_ref_staged},
    # nine rows, --verbose, stale SHA256SUMS entry accepted and a 40-hex token in the same registry
    {"fid": "u5_short_b-lane-path-manifest", "tool": "anchor", "expect": "reject",
     "defects": ["digest-short"], "build": build_lane_path_manifest},
    # two-commit history: the token is correct at commit 1 and truncated to 20 hex at commit 2
    {"fid": "u5_short_b-history-truncation", "tool": "anchor", "expect": "reject",
     "defects": ["digest-short"], "build": build_history_truncation},
]
