"""a2_use — the tool run resolves `git` from the caller PATH; the shim answers by phase.

No build writes outside d: the shim is planted before the run in a directory the invoking
shell names first on PATH (the wave-1 scoped form). Each invocation also writes <lane>/state.lock,
the name the fingerprint skips.
"""

import hashlib

SHIM = '/fast/scratch/hyaku/kengaku-r40/F40CritCounterLimits/attack/shim'
SOURCES = "corpus/SOURCES.md"
EV = "corpus/evidence/x"
CAP = b"a2 replay capture bytes\n"
OTHER = b"a2 replay second capture bytes\n"
ROW = '| S900 | a2 replay row ({tag}) | code | A | one capture | sha256 {dig} | names corpus/evidence/x/cap.txt | fixture | mined | 2026-10-26 | corpus/knowledge/x.md |'
HEAD = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def repo(ctx, d, tag):
    r = ctx.init(d / "repo")
    dig = hashlib.sha256(CAP).hexdigest()
    (r / EV).mkdir(parents=True)
    (r / SOURCES).write_text(HEAD + ROW.format(tag=tag, dig=dig) + "\n")
    (r / EV / "cap.txt").write_bytes(CAP)
    (r / EV / "other.txt").write_bytes(OTHER)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "a2 replay fixture")
    return ["--lane", str(r)]


def build_accept(ctx, d):
    return repo(ctx, d, "accept-in-the-reference-phase")


def build_reject(ctx, d):
    return repo(ctx, d, "reject-in-the-reference-phase")


FIXTURES = [
    {"fid": "a2-replay-accept", "tool": "anchor", "expect": "accept", "defects": [], "build": build_accept},
    {"fid": "a2-replay-injected", "tool": "anchor", "expect": "reject",
     "defects": ["capture-unanchored"], "build": build_reject},
]
