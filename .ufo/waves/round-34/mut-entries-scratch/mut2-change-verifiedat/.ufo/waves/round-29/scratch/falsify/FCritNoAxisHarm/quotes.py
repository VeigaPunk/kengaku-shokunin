import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
FLEET = LANE.parent
QUOTES = [
    (LANE / "PROVINCE.md", 201, "generated configs, runtime task validity, hosted judges and contamination remain open."),
    (LANE / "corpus/README.md", 338, "generated eval-time configs, runtime DOM/helper/judge validity and contamination checks remain open."),
    (LANE / "SCORECARD.md", 247, "unindexed files on disk; declared-but-unresolvable surfaces; a gap line contradicted by an artifact already in the repo"),
    (LANE / "SCORECARD.md", 248, "a command in the repo exits 0/1 with a verdict a stranger can run"),
    (LANE / "SCORECARD.md", 249, "a round with no re-verification line"),
    (LANE / "SCORECARD.md", 245, "any artifact that never reaches `LOG.md`/README"),
    (LANE / "SCORECARD.md", 246, "a reader can act on `SKILL.md` alone"),
    (LANE / "plans/round-29-claims.md", 95, "index/coverage and source-used-by links."),
    (LANE / ".ufo/waves/round-29/drafts/webarena-config-projection.md", 10, "Extends corpus/README.md Frontier “generated eval-time configs” left open by round28"),
    (FLEET / "PROTOCOL.md", 398, "a child lane's *registry home* is its own `SKILL.md`."),
    (LANE / "corpus/README.md", 336, "the original Frontier task-spec-audit gap is closed only for this"),
]
bad = 0
for path, line, quote in QUOTES:
    text = path.read_text(encoding="utf-8").splitlines()[line - 1]
    ok = quote in text
    bad += not ok
    print("%s %s:%d words=%d" % ("ok " if ok else "BAD", path.relative_to(FLEET), line, len(quote.split())))
print("bad", bad)
sys.exit(1 if bad else 0)
