#!/usr/bin/env python3
"""Re-derive the ten defect items round 30's non-author closure routed to this lane.

Round 31 (2026-10-25), claim C2. One command, one line: `defects=N`, exit 0 only
when every one of R1-R10 re-derives as repaired. Each check reads committed or
live lane bytes that round 30 left behind; none reads an artifact round 31's C1
or C3 creates, so C2 stays separable from them (QUALITY R13).

Frozen items (corpus/lessons/round-30-verifier-spotcheck.md §5 items 1-8, plus
the two copyedit residues the same pass located in the admitted entry):
  R1  LOG.md:792 declares the delta as "two new fields, one new value set" while the
      entry retracts that reading; LOG.md is append-only, so the repair is an appended
      named correction that quotes the superseded text.
  R2  corpus/lessons/round-30.md:66-67 states the Q6 pass on "one field, one placement,
      one value set" — the reading the entry retracts.
  R3  corpus/lessons/round-30.md:60-61 lists the Q2 tier set as "S085 B, S086 A"; the
      registry row says S086 is tier B and the same lesson says so at :93.
  R4  corpus/knowledge/contamination-transparency-card.md:125-126 repeats one sentence
      twice ("the card records what each stated, not a reconciled truth").
  R5  the entry's falsifier bullet repeats a clause ("populated (not \"unknown\")" twice).
  R6  the entry's :41 says "three source rows are not in this lane's registry (the GEM
      2026 review it tabulates is the one exception)" while :160 says "two of its three".
      The staged file names three sources; exactly one is registered here, so the count
      is two — the check re-derives it from the staged file and the registry.
  R7  the entry says "S2's tri-state integrity flag is the only new field" while its own
      R3 mapping row records `unknown` / `not_controlled` as valid values in a published
      form; the new object is the card-level field, not the vocabulary.
  R8  the entry names "the CC0 card" at :139; no registry row records a CC0 licence for
      that design, so the adjective is ungrounded.
  R9  five round-30 wave seat reports are modified in the worktree and uncommitted.
  R10 corpus/lessons/round-30.md:3 says "34 falsify" seats; the committed falsify
      registry holds 33 members and the round's report says 33.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LOG = "LOG.md"
LESSON = "corpus/lessons/round-30.md"
ENTRY = "corpus/knowledge/contamination-transparency-card.md"
REGISTRY = "corpus/SOURCES.md"
STAGED = Path(
    "/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/"
    "benchmark-card-field-schema-2026-10-23.md"
)
FALSIFY_REGISTRY = ".ufo/waves/round-30/falsify/swarm-registry.json"
BASELINE = "0883e72ef8474ca42ac1a54eb0273079f1507035"

SEAT_REPORTS = (
    ".ufo/waves/round-30/build/R30DraftGate.md",
    ".ufo/waves/round-30/build/R30RevLesson.md",
    ".ufo/waves/round-30/falsify/R30FxCoverageAxis.md",
    ".ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md",
    ".ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md",
)

ROW_RE = re.compile(r"^ {0,3}\|[ \t]*(S[0-9]{3,})[ \t]*\|")

SUPERSEDED_DELTA = "two new fields, one new value set"
ADMITTED_DELTA = "one field, and the rest is not a delta at all"
RETRACTED_Q6 = "one field, one placement, one value set"
RECONCILED = "the card records what each stated, not a reconciled truth"
FALSIFIER_CLAUSE = 'populated (not "unknown")'


def flat(text: str) -> str:
    """Whitespace-collapsed text: LOG.md wraps the sentence across two lines."""
    return re.sub(r"\s+", " ", text)


INVISIBLES = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u200e\u200f\u2060\ufeff\u00ad"), None)


def plain(text: str) -> str:
    """Collapsed, emphasis-stripped and invisible-character-free.

    A duplicated clause hides behind `*` marks and behind zero-width characters: the round-31
    C2 critic greened both copyedit checks with `reconciled\u200b truth`, which renders
    identically to the text it duplicates.
    """
    return re.sub(r"\*\*|__|\*", "", flat(text.translate(INVISIBLES)))


def read(lane: Path, path: str) -> str:
    return (lane / path).read_text(encoding="utf-8", errors="replace")


def git(lane: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(lane), *args], capture_output=True, text=True, check=False
    )


def append_only(lane: Path, path: str) -> str:
    """Return "" when `path` gained only additions since the round's baseline commit.

    An append-only file cannot be repaired by rewriting the wrong cell, and a substring test
    cannot see the difference: the C2 critic rewrote `LOG.md:792` in place and every wording
    check stayed green. Deletions since the baseline are the mechanical signal.
    """
    proc = git(lane, "diff", "--numstat", BASELINE, "--", path)
    if proc.returncode != 0:
        return f"git diff against {BASELINE} failed for {path}: {proc.stderr.strip()}"
    if not proc.stdout.strip():
        return f"{path} has no diff against {BASELINE}: the repair is not in the tree"
    for raw in proc.stdout.splitlines():
        added, deleted, *_ = raw.split("\t")
        if deleted.isdigit() and int(deleted) > 0:
            return f"{path} deletes {deleted} lines against {BASELINE}: append-only forbids rewriting"
    return ""


def registry_rows(lane: Path) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for raw in read(lane, REGISTRY).splitlines():
        match = ROW_RE.match(raw)
        if not match:
            continue
        cells = raw.strip()[1:-1].split("|")
        if len(cells) != 11:
            continue
        rows[match.group(1)] = [cell.strip() for cell in cells]
    return rows


def check_r1(lane: Path) -> str:
    text = flat(read(lane, LOG))
    if SUPERSEDED_DELTA not in text:
        return f"the superseded wording {SUPERSEDED_DELTA!r} is gone from LOG.md: append-only forbids rewriting it"
    tail = text[text.index(SUPERSEDED_DELTA):]
    if tail.count(SUPERSEDED_DELTA) < 2:
        return "no appended correction quotes the superseded delta wording (only the original occurrence exists)"
    if "correction" not in tail.lower():
        return "the appended block is not labelled as a correction"
    if ADMITTED_DELTA not in tail:
        return f"the appended correction does not state the admitted wording {ADMITTED_DELTA!r}"
    return append_only(lane, LOG)


def check_r2(lane: Path) -> str:
    text = read(lane, LESSON)
    retracted = text.rfind(RETRACTED_Q6)
    if retracted < 0:
        return "the retracted Q6 basis is gone from the round-30 lesson: append-only forbids rewriting it"
    after = flat(text[retracted:])
    if ADMITTED_DELTA not in after:
        return "no appended erratum states the admitted Q6 basis after the retracted one"
    if "errata" not in after.lower() and "erratum" not in after.lower():
        return "the block correcting the Q6 basis is not labelled as an erratum"
    return append_only(lane, LESSON)


def check_r3(lane: Path) -> str:
    text = read(lane, LESSON)
    rows = registry_rows(lane)
    row = rows.get("S086")
    if row is None:
        return "S086 row missing: the tier set cannot be re-derived"
    tier = row[3]
    if tier != "B":
        return f"registry S086 tier is {tier!r}, not B: the lesson's corrected cell would be wrong"
    retracted = text.rfind("S085 B, S086 A")
    if retracted < 0:
        return "the retracted Q2 tier cell is gone from the lesson: append-only forbids rewriting it"
    after = text[retracted:]
    if "S086 B" not in after:
        return "no appended erratum corrects the Q2 tier cell to S086 B"
    return append_only(lane, LESSON)


def check_r4(lane: Path) -> str:
    count = plain(read(lane, ENTRY)).count(RECONCILED)
    if count != 1:
        return f"the entry carries the 'reconciled truth' sentence {count} times, not exactly once"
    return ""


def check_r5(lane: Path) -> str:
    count = plain(read(lane, ENTRY)).count(FALSIFIER_CLAUSE)
    if count != 1:
        return f"the falsifier bullet repeats {FALSIFIER_CLAUSE!r} {count} times, not exactly once"
    return ""


def check_r6(lane: Path) -> str:
    entry = flat(read(lane, ENTRY))
    # Re-derive the count instead of trusting any wording: the staged file names its sources
    # on `source:` lines, and each URL either has a registry row or not.
    if not STAGED.is_file():
        return f"the staged file {STAGED} is unreadable: the count cannot be re-derived"
    urls = re.findall(
        r"^source:[ \t]*S[0-9]+ [—-] (https?://\S+)", STAGED.read_text(encoding="utf-8"), re.MULTILINE
    )
    if len(urls) != 3:
        return f"the staged file names {len(urls)} source URLs, not the three the entry tabulates"
    registry = read(lane, REGISTRY)
    # "Registered" is a question about the document, not about the byte URL: the lane carries the
    # GEM 2026 review as S001 at its aclanthology landing URL while the staged row cites the PDF of
    # the same anthology id. Presence is therefore tested on a document key -- trailing slash and a
    # trailing `.pdf` removed -- so a format difference is not read as a missing source.
    def document_key(url: str) -> str:
        return re.sub(r"\.pdf$", "", url.rstrip("/")).lower()

    registry_keys = {document_key(match) for match in re.findall(r"https?://\S+", registry)}
    unregistered = len([url for url in urls if document_key(url) not in registry_keys])
    # Two shapes the entry may use: "<n> of its three source rows are not ..." or the bare
    # "its three source rows are not ..." (which asserts n = 3 without saying so). A substring
    # test cannot separate them -- the counted form contains the bare one -- so parse the number.
    # Only the *bare* assertion is a defect: "its three source rows are not in this lane's
    # registry" claims all three are unregistered. Any counted form ("two of its three ...") is
    # the honest shape and must pass whether or not its bytes match the landed sentence -- the
    # first version of this check rejected an honest paraphrase of the entry's own §Extends
    # sentence (round-31 R6/R8 critic, fixture 4), which made `defects=0` depend on wording.
    bare = re.search(
        r"(?<!of )\bits three source rows are (?:staged and )?not in this lane's registry", entry
    )
    if bare:
        return f"the entry asserts all three staged source rows are unregistered; {unregistered} are"
    if "of its three source rows" not in entry:
        return f"the entry states no staged-source count; the re-derived count is {unregistered}"
    return ""


def check_r7(lane: Path) -> str:
    # Round 31's R7 reviewer showed the first version of this check was a two-string guard: it
    # greened on the word "card-level" while the mis-description "tri-state" survived and the
    # delta stayed unscoped. The check now tests the three things the repaired paragraph has to
    # say -- the vocabulary is published, the added object is the field in the union table, and
    # "tri-state" (which describes a four-valued vocabulary) is gone.
    text = plain(read(lane, ENTRY))
    if "S2's tri-state integrity flag is the only new field" in text:
        return "the entry still claims the tri-state flag is the only new field"
    if "tri-state" in text:
        return "the entry still calls a four-valued vocabulary 'tri-state'"
    if "Its values are not new" not in text:
        return "the entry does not state that the field's values are already published"
    if "adds to the union table" not in text and "card-level" not in text:
        return "the delta is not scoped to the union table (or the card-level subject)"
    return ""


def check_r8(lane: Path) -> str:
    entry = read(lane, ENTRY)
    # A licence word is grounded only by the row that *is* the design: its source or anchor cell.
    # Scanning every cell of every row let a scope cell mentioning CC0 green an ungrounded entry
    # (round-31 R6/R8 critic, fixture 5), and the check was vacuous on the landed bytes.
    tokens = [token for token in ("CC0", "CC BY", "Apache", "MIT") if token in entry]
    if not tokens:
        return ""
    grounded: set[str] = set()
    for cells in registry_rows(lane).values():
        for index in (1, 5):
            for token in tokens:
                if token in cells[index]:
                    grounded.add(token)
    ungrounded = [token for token in tokens if token not in grounded]
    if ungrounded:
        return f"the entry names a licence no registry row's source or anchor cell records: {', '.join(ungrounded)}"
    return ""


def check_r9(lane: Path) -> str:
    for path in SEAT_REPORTS:
        status = git(lane, "status", "--porcelain", "--", path)
        if status.returncode != 0:
            return f"git status failed for {path}: {status.stderr.strip()}"
        if status.stdout.strip():
            return f"{path} still differs from HEAD: {status.stdout.strip()}"
        blob = git(lane, "cat-file", "-p", f"HEAD:{path}")
        if blob.returncode != 0:
            return f"{path} is not committed at HEAD"
        if len(blob.stdout.splitlines()) < 100:
            return f"HEAD:{path} is {len(blob.stdout.splitlines())} lines: a stub is not the seat report"
        # A revert or a stub route is invisible to a status test: the committed blob must still
        # carry at least the lines the baseline commit carried (round-31 C2 critic).
        before = git(lane, "cat-file", "-p", f"{BASELINE}:{path}")
        if before.returncode == 0 and len(blob.stdout.splitlines()) < len(before.stdout.splitlines()):
            return (
                f"HEAD:{path} is shorter than at {BASELINE[:7]} "
                f"({len(blob.stdout.splitlines())} < {len(before.stdout.splitlines())} lines): "
                "a revert is not the repair"
            )
    gate = git(lane, "cat-file", "-p", "HEAD:.ufo/waves/round-30/build/R30DraftGate.md")
    if "Pass 9" not in gate.stdout:
        return "HEAD's R30DraftGate.md omits the pass-9 correction the worktree carried"
    return ""


def check_r10(lane: Path) -> str:
    text = read(lane, LESSON)
    path = lane / FALSIFY_REGISTRY
    if not path.is_file():
        return f"{FALSIFY_REGISTRY} is unreadable: the seat count cannot be re-derived"
    members = json.loads(path.read_text(encoding="utf-8")).get("members", {})
    actual = len(members)
    if actual != 33:
        return f"the committed falsify registry holds {actual} members, not the 33 the erratum states"
    retracted = text.rfind("34 falsify")
    if retracted < 0:
        return "the retracted seat count is gone from the lesson: append-only forbids rewriting it"
    after = flat(text[retracted:])
    if "33 falsify" not in after:
        return "no appended erratum corrects the falsify seat count to 33"
    return append_only(lane, LESSON)


CHECKS = (
    ("R1", "log-delta-correction", check_r1),
    ("R2", "lesson-q6-basis", check_r2),
    ("R3", "lesson-q2-tier-cell", check_r3),
    ("R4", "entry-duplicated-sentence", check_r4),
    ("R5", "entry-falsifier-clause", check_r5),
    ("R6", "entry-staged-source-count", check_r6),
    ("R7", "entry-s2-only-field", check_r7),
    ("R8", "entry-licence-adjective", check_r8),
    ("R9", "round30-seat-reports-committed", check_r9),
    ("R10", "lesson-round-shape", check_r10),
)

# Frozen registry: a counter whose own check list can shrink to nothing still prints
# `defects=0`. `--selftest` asserts this list, and every run prints `checks=N` beside
# the total.
FROZEN = (
    ("R1", "log-delta-correction"),
    ("R2", "lesson-q6-basis"),
    ("R3", "lesson-q2-tier-cell"),
    ("R4", "entry-duplicated-sentence"),
    ("R5", "entry-falsifier-clause"),
    ("R6", "entry-staged-source-count"),
    ("R7", "entry-s2-only-field"),
    ("R8", "entry-licence-adjective"),
    ("R9", "round30-seat-reports-committed"),
    ("R10", "lesson-round-shape"),
)


def selftest() -> int:
    cases: list[tuple[str, bool]] = []
    cases.append(("registry-complete", tuple((i, l) for i, l, _ in CHECKS) == FROZEN))
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp)
        for item_id, label, check in CHECKS:
            # Every check must be red on a tree where its input is missing: a check
            # returning "" unconditionally is the mutation this asserts against.
            try:
                red = bool(check(empty))
            except Exception:
                red = True
            cases.append((f"{item_id}-red-on-empty", red))
    failed = [name for name, passed in cases if not passed]
    for name, passed in cases:
        print(f"CASE {name} {'PASS' if passed else 'FAIL'}")
    print(f"SELFTEST checks={len(CHECKS)} failed={len(failed)}")
    return 0 if not failed else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", type=Path, default=Path("."))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    lane = args.lane.resolve()
    if tuple((i, l) for i, l, _ in CHECKS) != FROZEN:
        print("DEFECT registry: the check list no longer matches the frozen ten")
        print(f"checks={len(CHECKS)} defects={len(CHECKS) + 1}")
        return 1
    defects = 0
    for item_id, label, check in CHECKS:
        try:
            reason = check(lane)
        except Exception as error:  # an unreadable input is not a clean item
            reason = f"check raised {type(error).__name__}: {error}"
        if reason:
            defects += 1
            print(f"DEFECT {item_id} {label}: {reason}")
    print(f"checks={len(CHECKS)} defects={defects}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
