"""Critic scratch fixture (R40CritC1Equiv): A17 in its declared rc-mirror direction.

A capture that exists at HEAD and is modified in the index: the reference (index mode) accepts the
staged digest, the mutant (HEAD mode) sees the old bytes and rejects. Shape differs from the round-39
X15 witness, whose mutant exit is 2 (Usage: the staged-only capture is absent from HEAD), i.e. an
rc-error shape, not rc-mirror.
"""
import hashlib
import re

CAP = "corpus/evidence/round37/tb2-git-webserver"


def staged_modified(ctx, d):
    lane = ctx.clone(d / "lane")
    f = lane / CAP / "test_outputs.py"
    old = hashlib.sha256(f.read_bytes()).hexdigest()
    f.write_bytes(f.read_bytes() + b"\n# staged-only change\n")
    new = hashlib.sha256(f.read_bytes()).hexdigest()
    sums = lane / CAP / "SHA256SUMS"
    t = sums.read_text()
    sums.write_text(re.sub(r"[0-9a-f]{64}(\s+\*?test_outputs\.py)", new + r"\1", t))
    so = lane / "corpus/SOURCES.md"
    s = so.read_text()
    assert s.count("sha256 " + old) == 1
    so.write_text(s.replace("sha256 " + old, "sha256 " + new, 1))
    ctx.git(lane, "add", f"{CAP}/test_outputs.py", f"{CAP}/SHA256SUMS")
    return ["--lane", str(lane), "--evidence-ref", "index"]


FIXTURES = [
    {"fid": "eq-a17-staged-modified", "tool": "anchor", "expect": "accept", "defects": [],
     "build": staged_modified},
]
