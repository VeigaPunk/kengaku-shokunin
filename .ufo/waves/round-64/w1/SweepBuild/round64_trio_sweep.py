#!/usr/bin/env python3
"""Round-64 provenance-trio sweep (R64-C3 freshness instrument).

Walks ``corpus/knowledge/*.md`` and classifies every entry:

* ``TRIO-OPEN`` -- the provenance trio (``source:``, ``verified-at:``,
  ``recheck:``) is established in canonical order inside the first 12 lines
  and before the first ``## `` heading.  This is EXACTLY the round-63 gate's
  rule: the function ``trio_missing`` is IMPORTED from
  ``plans/round63_gate_checks.py`` (``rule=import``), never re-implemented
  here, so the sweep cannot drift from the gate it mirrors.
* ``TRIO-ADDENDUM`` -- the opening predates the rule, and the file carries an
  append-only dated ``## Freshness addendum (round 64)`` block holding
  ``verified-at: 2026-11-03`` and a ``recheck:`` line with a non-empty
  command.
* ``TRIO-RED`` -- neither.

CLI
---
``--sweep --lane <L> [--frozen-list <path>]``
    Prints one ``SWEEP files=<n> trio_open=<a> addendum=<b> red=<c>`` line,
    then one line per non-OPEN entry (``ADDENDUM <path>`` / ``RED <path>``),
    then ``PREDICATE R64-C3 pass|fail``.  Paths are lane-relative POSIX.
    Exit 0 on pass, 1 on fail, 2 on setup.

``--selftest --work <dir>``
    Builds RED / ADDENDUM / OPEN fixtures under ``mkdtemp(dir=work)``,
    classifies each, and additionally exercises the sweep pipeline on a
    three-file fixture lane before and after a repair; exits 0 iff every
    case behaves as named.

SETUP cross-check (frozen list)
-------------------------------
``--sweep`` cross-checks its red set against the frozen base list
``corpus/evidence/round64/trio-red-at-base.txt`` (lane-local copy when
present, else the committed path in the lane repo; ``--frozen-list``
overrides).  While red entries are observed, the red set must equal the
frozen list entry-for-entry; any mismatch prints
``SETUP frozen-list-mismatch`` on stdout and exits 2 without a PREDICATE
line.  Once ``red=0`` there is no red set to compare: the cross-check is
then vacuous and the predicate is printed.  The frozen list is the BASE
population -- a repaired tip is expected to fall below it -- and this
resolution is what lets both the frozen red-before command and the frozen
counting command run with no extra flags.  On that ``red=0`` path every
frozen entry must still exist as a file in the lane: a deleted or renamed
entry is not a repair, so it prints ``SETUP frozen-entry-missing`` and exits
2 (an empty knowledge dir can therefore never pass).

Ambiguity resolutions (the frozen rule is unchanged; see the seat report)
-----------------------------------------------------------------------
* ``TRIO-OPEN`` wins over an addendum: an entry whose opening already
  satisfies the gate counts OPEN and is not listed as non-OPEN;
* the addendum heading is compared with trailing whitespace tolerated (the
  gate's own heading comparison) and is exactly
  ``## Freshness addendum (round 64)``; a block runs to the next ``## ``
  heading or EOF, and any occurrence that carries both required lines
  classifies the entry ADDENDUM;
* inside the block ``verified-at:`` must carry the date token
  ``2026-11-03`` (bounded by whitespace/end of line, so trailing prose is
  tolerated but another date is not) and ``recheck:`` must carry a
  non-empty command; the ``ADDENDUM`` classification does not price the
  command's own exit status -- the closure re-runs it (frozen kill rule);
* a ``RED`` file that carries the heading but an incomplete block emits a
  ``NOTE addendum-incomplete`` diagnostic on stderr naming the missing
  lines; stdout stays exactly the frozen shape;
* an unreadable lane, knowledge dir or frozen list is a setup error
  (exit 2), never a vacuous pass.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import shutil
import sys
import tempfile

PLANS_DIR = pathlib.Path(__file__).resolve().parent
if str(PLANS_DIR) not in sys.path:
    sys.path.insert(0, str(PLANS_DIR))
try:
    from round63_gate_checks import trio_missing  # the round-63 rule, imported
except ImportError as exc:  # pragma: no cover - setup guard
    print(f"SETUP gate-import-failed {exc}", file=sys.stderr)
    raise SystemExit(2)

KNOWLEDGE_DIR = pathlib.Path("corpus") / "knowledge"
FROZEN_LIST_REPO = pathlib.Path("corpus/evidence/round64/trio-red-at-base.txt")
FROZEN_LIST_ABS = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round64/trio-red-at-base.txt"
)
ADDENDUM_HEADING = "## Freshness addendum (round 64)"
HEADING_PREFIX = "## "
VERIFIED_RE = re.compile(r"^verified-at:[ \t]*2026-11-03(?:[ \t]|$)")
RECHECK_RE = re.compile(r"^recheck:[ \t]*\S")


# --------------------------------------------------------------------------
# classification
# --------------------------------------------------------------------------
def addendum_state(text: str) -> tuple[bool, list[str]]:
    """(heading present, missing lines of the first block that lacks any)."""
    lines = text.splitlines()
    headings = [i for i, line in enumerate(lines) if line.rstrip() == ADDENDUM_HEADING]
    if not headings:
        return False, []
    first_missing: list[str] = []
    for index in headings:
        block: list[str] = []
        for line in lines[index + 1 :]:
            if line.startswith(HEADING_PREFIX):
                break
            block.append(line)
        missing: list[str] = []
        if not any(VERIFIED_RE.match(line) for line in block):
            missing.append("verified-at: 2026-11-03")
        if not any(RECHECK_RE.match(line) for line in block):
            missing.append("recheck:")
        if not missing:
            return True, []
        if not first_missing:
            first_missing = missing
    return True, first_missing


def classify(text: str) -> tuple[str, str]:
    """(TRIO-OPEN | TRIO-ADDENDUM | TRIO-RED, diagnostic note)."""
    if not trio_missing(text):
        return "TRIO-OPEN", ""
    present, missing = addendum_state(text)
    if present and not missing:
        return "TRIO-ADDENDUM", ""
    if present:
        return "TRIO-RED", "addendum-incomplete missing=" + ",".join(missing)
    return "TRIO-RED", ""


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def frozen_entries(path: pathlib.Path) -> list[str]:
    entries: list[str] = []
    for line in read_text(path).splitlines():
        token = line.strip()
        if token:
            entries.append(token)
    return entries


def resolve_frozen_list(lane: pathlib.Path, override: str | None) -> pathlib.Path:
    if override:
        return pathlib.Path(override)
    local = lane / FROZEN_LIST_REPO
    if local.is_file():
        return local
    return FROZEN_LIST_ABS


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sweep_fields(line: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for token in line.split():
        if "=" in token:
            key, _, value = token.partition("=")
            fields[key] = value
    return fields


# --------------------------------------------------------------------------
# sweep
# --------------------------------------------------------------------------
def measure(
    lane_arg: str, frozen_arg: str | None = None
) -> tuple[int, list[str], list[str]]:
    """(exit code, stdout lines, stderr lines) for one sweep of ``lane_arg``."""
    lane = pathlib.Path(lane_arg)
    if not lane.is_dir():
        return 2, ["SETUP lane-missing"], [f"SETUP lane is not a directory: {lane_arg}"]
    knowledge = lane / KNOWLEDGE_DIR
    if not knowledge.is_dir():
        return 2, ["SETUP knowledge-dir-missing"], [
            f"SETUP knowledge dir is not a directory: {knowledge}"
        ]
    frozen = resolve_frozen_list(lane, frozen_arg)
    if not frozen.is_file():
        return 2, ["SETUP frozen-list-unreadable"], [
            f"SETUP frozen list is not a file: {frozen}"
        ]
    try:
        frozen_set = frozen_entries(frozen)
    except OSError as exc:
        return 2, ["SETUP frozen-list-unreadable"], [f"SETUP cannot read {frozen}: {exc}"]
    try:
        frozen_sha = sha256_file(frozen)
    except OSError as exc:
        return 2, ["SETUP frozen-list-unreadable"], [f"SETUP cannot hash {frozen}: {exc}"]

    paths = sorted(knowledge.glob("*.md"))
    counts = {"TRIO-OPEN": 0, "TRIO-ADDENDUM": 0, "TRIO-RED": 0}
    non_open: list[str] = []
    red: list[str] = []
    notes: list[str] = []
    unreadable: list[str] = []
    for path in paths:
        rel = path.relative_to(lane).as_posix()
        try:
            klass, note = classify(read_text(path))
        except OSError as exc:
            unreadable.append(f"SETUP cannot read {rel}: {exc}")
            continue
        counts[klass] += 1
        if klass == "TRIO-RED":
            red.append(rel)
            non_open.append(f"RED {rel}")
        elif klass == "TRIO-ADDENDUM":
            non_open.append(f"ADDENDUM {rel}")
        if note:
            notes.append(f"NOTE {note} file={rel}")
    if unreadable:
        return 2, ["SETUP knowledge-unreadable"], unreadable

    err = [f"INFO frozen-list={frozen} sha256={frozen_sha} entries={len(frozen_set)}"]
    err.extend(notes)

    if red:
        observed = sorted(red)
        expected = sorted(frozen_set)
        if observed != expected:
            extra = [item for item in observed if item not in expected]
            missing = [item for item in expected if item not in observed]
            err.append(
                "DETAIL frozen=<{0}> observed=<{1}> extra=<{2}> missing=<{3}>".format(
                    len(expected), len(observed), ",".join(extra[:8]) or "-",
                    ",".join(missing[:8]) or "-",
                )
            )
            return 2, ["SETUP frozen-list-mismatch"], err

    if not red:
        present = {path.relative_to(lane).as_posix() for path in paths}
        absent = [entry for entry in sorted(frozen_set) if entry not in present]
        if absent:
            err.append(
                "DETAIL frozen-entries-absent=<{0}> first=<{1}>".format(
                    len(absent), ",".join(absent[:8])
                )
            )
            return 2, ["SETUP frozen-entry-missing"], err

    out = [
        "SWEEP files={0} trio_open={1} addendum={2} red={3}".format(
            len(paths), counts["TRIO-OPEN"], counts["TRIO-ADDENDUM"], counts["TRIO-RED"]
        )
    ]
    out.extend(non_open)
    out.append(f"PREDICATE R64-C3 {'pass' if not red else 'fail'}")
    return (0 if not red else 1), out, err


def count_by(texts: dict[str, str], want: str) -> int:
    return sum(1 for text in texts.values() if classify(text)[0] == want)


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------
OPEN_FIXTURE = """# open-fixture - provenance trio in the frozen window

source: S-fixture - a committed receipt `corpus/evidence/fixture.txt`
verified-at: 2026-11-03
recheck: python3 plans/round63_gate_checks.py trio corpus/knowledge/open.md

## Body

Fixture body.
"""

ADDENDUM_FIXTURE = """# addendum-fixture - opening predates the trio rule

**Provenance of this note (read first).** Fixture body with no trio key in the
frozen window.

## Body

Fixture body; still no trio key.

## Freshness addendum (round 64)

verified-at: 2026-11-03
recheck: python3 plans/round63_gate_checks.py trio corpus/knowledge/addendum.md
"""

RED_FIXTURE = """# red-fixture - no trio, no addendum

Fixture body with neither an opening trio nor a freshness addendum.

## Body

Fixture body.
"""

REPAIRED_RED_FIXTURE = RED_FIXTURE + """
## Freshness addendum (round 64)

verified-at: 2026-11-03
recheck: python3 plans/round63_gate_checks.py trio corpus/knowledge/red.md
"""


def run_selftest(work_arg: str) -> tuple[int, list[str]]:
    work = pathlib.Path(work_arg)
    if work.exists() and not work.is_dir():
        print(f"SETUP --work is not a directory: {work_arg}", file=sys.stderr)
        return 2, []
    work.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="r64-sweep-", dir=str(work)))
    out: list[str] = []
    ok = True
    try:
        fixtures = {"OPEN": OPEN_FIXTURE, "ADDENDUM": ADDENDUM_FIXTURE, "RED": RED_FIXTURE}
        for name in ("RED", "ADDENDUM", "OPEN"):
            got, note = classify(fixtures[name])
            leg_ok = got == f"TRIO-{name}" and not note
            ok = ok and leg_ok
            out.append(
                f"SELFTEST classify case={name} got={got} "
                f"expect=TRIO-{name} {'ok' if leg_ok else 'BAD'}"
            )

        lane = tmp / "lane"
        knowledge = lane / KNOWLEDGE_DIR
        knowledge.mkdir(parents=True)
        for name, text in fixtures.items():
            (knowledge / f"{name.lower()}.md").write_text(text, encoding="utf-8")
        frozen = tmp / "frozen.txt"
        frozen.write_text("corpus/knowledge/red.md\n", encoding="utf-8")

        rc, lines, _err = measure(str(lane), str(frozen))
        fields = sweep_fields(lines[0]) if lines else {}
        base_ok = (
            rc == 1
            and lines[-1] == "PREDICATE R64-C3 fail"
            and fields.get("files") == "3"
            and fields.get("trio_open") == "1"
            and fields.get("addendum") == "1"
            and fields.get("red") == "1"
            and "RED corpus/knowledge/red.md" in lines
            and "ADDENDUM corpus/knowledge/addendum.md" in lines
        )
        ok = ok and base_ok
        out.append(
            f"SELFTEST sweep-base rc={rc} expect=1 red={fields.get('red')} "
            f"trio_open={fields.get('trio_open')} addendum={fields.get('addendum')} "
            f"{'ok' if base_ok else 'BAD'}"
        )

        (knowledge / "red.md").write_text(REPAIRED_RED_FIXTURE, encoding="utf-8")
        rc, lines, _err = measure(str(lane), str(frozen))
        fields = sweep_fields(lines[0]) if lines else {}
        repaired_ok = (
            rc == 0
            and lines[-1] == "PREDICATE R64-C3 pass"
            and fields.get("files") == "3"
            and fields.get("trio_open") == "1"
            and fields.get("addendum") == "2"
            and fields.get("red") == "0"
        )
        ok = ok and repaired_ok
        out.append(
            f"SELFTEST sweep-repaired rc={rc} expect=0 red={fields.get('red')} "
            f"addendum={fields.get('addendum')} {'ok' if repaired_ok else 'BAD'}"
        )

        out.append(f"SELFTEST {'pass' if ok else 'fail'}")
        return (0 if ok else 1), out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(
        prog="round64_trio_sweep.py",
        description="R64-C3 provenance-trio sweep (frozen round-64 claims).",
    )
    parser.add_argument("--sweep", action="store_true", help="classify the lane")
    parser.add_argument("--lane", default=None, help="lane root for --sweep")
    parser.add_argument(
        "--frozen-list", default=None, help="override the frozen base list path"
    )
    parser.add_argument("--selftest", action="store_true", help="run the fixture selftest")
    parser.add_argument("--work", default=None, help="work dir for --selftest")
    args = parser.parse_args(argv)

    if args.sweep and args.selftest:
        parser.print_usage(sys.stderr)
        print("error: choose --sweep or --selftest, not both", file=sys.stderr)
        return 2
    if args.selftest:
        if not args.work:
            parser.print_usage(sys.stderr)
            print("error: --selftest requires --work <dir>", file=sys.stderr)
            return 2
        rc, lines = run_selftest(args.work)
        for line in lines:
            print(line)
        return rc
    if args.sweep:
        if not args.lane:
            parser.print_usage(sys.stderr)
            print("error: --sweep requires --lane <dir>", file=sys.stderr)
            return 2
        rc, lines, err = measure(args.lane, args.frozen_list)
        for line in lines:
            print(line)
        for line in err:
            print(line, file=sys.stderr)
        return rc
    parser.print_usage(sys.stderr)
    print("error: expected '--sweep --lane <dir> --frozen-list <path>'", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
