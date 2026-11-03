#!/usr/bin/env python3
"""Round-63 gate checks: provenance trio and grader-class decision-table depth.

Frozen by ``plans/round-63-claims.md`` (base tip c78749a5) — R63-C2 and the
section "Frontier step — provenance-trio gate". The predicates are fixed
there; this instrument only measures them, never re-defines them.

Subcommands
-----------

``trio <file>``
    Exit 0 iff lines matching ``^(source|verified-at|recheck):`` appear, in
    that order, within the first 12 lines and before the first line starting
    with ``## ``. Prints ``TRIO pass <file>`` or
    ``TRIO fail missing=<comma list> file=<file>``. Exit 1 on fail, 2 on usage.

``depth --skill <SKILL.md> --receipt <class-survey.txt> [--root <lane root>]``
    Locates the section heading line exactly
    ``## Decision table — grader class → offline replay recipe`` (em dash and
    arrow as written; missing section means 0 rows and fail). Table rows are
    lines in that section starting with ``|``; the first cell, stripped of
    spaces and backticks, is the class name; the header row and separator rows
    are ignored; expected columns are
    class | count | executed | replay recipe | receipt pointer (5 cells).
    The receipt's ``^CLASS (\\S+) count=(\\d+)`` names must equal the table's
    class-name set (16 names) and each row's count must equal the receipt's
    count. Every backticked token in the section containing ``/`` and ending
    in .py .md .json .txt .sh .lst .yml or ``/`` is a repo-relative path; it
    resolves iff it is relative, carries no ``..`` segment, and its lexically
    normalized ``root/token`` stays inside ``root`` (r64-C2: an absolute,
    ``..``-bearing or escaping token is a finding, never a resolution);
    share = resolved / total must be >= 0.90 with total > 0, and each row's
    receipt-pointer cell must hold at least one such token and at least one
    of them must resolve. Prints::

        ROWS n=<n> class_match=<True|False> count_mismatch=<k> paths total=<T> resolved=<R> share=<x.xx>
        [DETAIL ...]                       (only on fail)
        PREDICATE R63-C2 pass|fail         (always the last line)

    Exit 0 on pass, 1 on fail, 2 on usage.

``--selftest --work <dir>`` (alias ``selftest --work <dir>``)
    Builds, inside ``mkdtemp(dir=work)``, four fixtures — GOOD (16 rows
    matching a 16-CLASS fixture receipt, all paths resolving: must pass),
    BAD-COUNT (one count cell wrong: must fail), NO-SECTION (must fail) and
    BAD-ESCAPE (one row's receipt pointer is an absolute out-of-root path,
    plus one ``..`` token: must fail with ``DETAIL escape=``) — and exits 0
    iff all four behave. Fixtures are removed afterwards.

Ambiguity resolutions (the frozen rule is unchanged; see the seat report)
-----------------------------------------------------------------------
* duplicate backticked paths are counted once (set semantics), so a repeated
  broken pointer is not double-priced;
* a row's pointer cell passes when it holds at least one path token and at
  least one of its tokens resolves; the section-wide share still prices the
  rest;
* a trio key appearing out of canonical order counts as not established and
  is therefore listed in ``missing=``;
* trailing whitespace on the decision-table heading is tolerated; leading
  whitespace, case and the em dash / arrow glyphs are compared exactly;
* the markdown header row is the row immediately above a separator row,
  whatever its wording (a first cell literally reading ``class`` is also
  ignored), because the frozen rule says to ignore the header row without
  fixing its text;
* a backticked token carrying a URL scheme (``scheme://``) is not a
  repo-relative path and is excluded from path accounting, so a citation of
  PEP 503 cannot depress the resolution share;
* tokens carrying a line suffix (``path.txt:11``) do not end in a counted
  suffix and are therefore not path tokens — the frozen definition is
  syntactic and is applied as written;
* an unreadable ``--skill`` / ``--receipt`` / argv file is a setup error
  (exit 2), never a vacuous pass;
* (2026-11-03, r64-C2) path tokens are confined to the root: an absolute
  token, a token carrying a ``..`` segment, or a token whose normalized
  ``root/token`` leaves the root is not resolved; the depth command reports
  the set as ``DETAIL escape=<tokens>`` and fails when it is nonempty, even
  when the >= 0.90 share clause alone would pass.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import sys
import tempfile
from fractions import Fraction

TRIO_KEYS = ("source", "verified-at", "recheck")
TRIO_WINDOW = 12
TRIO_KEY_RE = re.compile(r"^(source|verified-at|recheck):")
HEADING_PREFIX = "## "

DEPTH_HEADING = "## Decision table \u2014 grader class \u2192 offline replay recipe"
CLASS_RE = re.compile(r"^CLASS (\S+) count=(\d+)")
TOKEN_RE = re.compile(r"`([^`\n]+)`")
URL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*://")
PATH_SUFFIXES = (".py", ".md", ".json", ".txt", ".sh", ".lst", ".yml")
COLS = 5
EXPECTED_CLASS_ROWS = 16
SHARE_FLOOR = Fraction(90, 100)


# --------------------------------------------------------------------------
# trio
# --------------------------------------------------------------------------
def trio_missing(text: str) -> list[str]:
    """Keys of the trio not established in order inside the frozen window."""
    seen: list[str] = []
    for line in text.splitlines()[:TRIO_WINDOW]:
        if line.startswith(HEADING_PREFIX):
            break
        m = TRIO_KEY_RE.match(line)
        if m:
            seen.append(m.group(1))
    first: dict[str, int] = {}
    for i, key in enumerate(seen):
        first.setdefault(key, i)
    missing: list[str] = []
    last = -1
    for key in TRIO_KEYS:
        i = first.get(key)
        if i is None or i <= last:
            missing.append(key)
        else:
            last = i
    return missing


def cmd_trio(file_arg: str) -> int:
    path = pathlib.Path(file_arg)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"SETUP cannot read {file_arg}: {exc}", file=sys.stderr)
        return 2
    missing = trio_missing(text)
    if missing:
        print(f"TRIO fail missing={','.join(missing)} file={file_arg}")
        return 1
    print(f"TRIO pass {file_arg}")
    return 0


# --------------------------------------------------------------------------
# depth
# --------------------------------------------------------------------------
def section_lines(text: str) -> list[str] | None:
    """Body of the frozen heading's section, or None when it is absent."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.rstrip() == DEPTH_HEADING:
            start = i + 1
            break
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start:]:
        if line.startswith(HEADING_PREFIX):
            break
        body.append(line)
    return body


def _cells(line: str) -> list[str]:
    raw = line.rstrip("\n").split("|")
    if raw and raw[0].strip() == "":
        raw = raw[1:]
    if raw and raw[-1].strip() == "":
        raw = raw[:-1]
    return [cell.strip() for cell in raw]


def _class_name(cell: str) -> str:
    return re.sub(r"[\s`]", "", cell)


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-+:?", c.replace(" ", "")) for c in cells)


def _cell_int(cell: str) -> int | None:
    stripped = cell.replace("`", "").strip()
    return int(stripped) if re.fullmatch(r"\d+", stripped) else None


def _path_tokens(chunk: str) -> list[str]:
    toks: list[str] = []
    for raw in TOKEN_RE.findall(chunk):
        tok = raw.strip()
        if URL_RE.match(tok):
            continue  # a URL is not a repo-relative path
        if "/" not in tok:
            continue
        if not (tok.endswith("/") or tok.endswith(PATH_SUFFIXES)):
            continue
        toks.append(tok)
    return toks


def _escape_reason(root: pathlib.Path, token: str) -> str | None:
    """Why *token* is not a root-confined relative path, or None.

    A token counts as a candidate path only when it is relative, has no
    ``..`` segment, and its lexically normalized ``root/token`` stays inside
    ``root`` (r64-C2, routed defect L-1).
    """
    pure = pathlib.PurePosixPath(token)
    if pure.is_absolute():
        return "absolute"
    if ".." in pure.parts:
        return "dotdot"
    target = pathlib.Path(os.path.normpath(os.path.join(str(root), token)))
    if not target.is_relative_to(pathlib.Path(os.path.normpath(str(root)))):
        return "outside-root"
    return None


def _resolves(root: pathlib.Path, token: str) -> bool:
    if _escape_reason(root, token) is not None:
        return False
    try:
        return (root / token).exists()
    except OSError:
        return False


def _short(items: list[str], limit: int = 10) -> str:
    if len(items) <= limit:
        return ",".join(items)
    return ",".join(items[:limit]) + f",+{len(items) - limit}more"


def depth_measure(
    skill_text: str, receipt_text: str, root: pathlib.Path
) -> tuple[int, list[str]]:
    body = section_lines(skill_text)
    section_present = body is not None
    body = body or []

    receipt: dict[str, int] = {}
    receipt_dupes: list[str] = []
    for line in receipt_text.splitlines():
        m = CLASS_RE.match(line)
        if not m:
            continue
        name = m.group(1)
        if name in receipt:
            receipt_dupes.append(name)
        receipt[name] = int(m.group(2))

    # Table rows: lines in the section starting with '|'. In markdown the row
    # immediately above a separator row is the header, whatever its wording;
    # a first cell reading 'class' is also treated as the header.
    raw_rows: list[tuple[int, list[str]]] = []
    for idx, line in enumerate(body):
        if not line.startswith("|"):
            continue
        cells = _cells(line)
        if not cells:
            continue
        raw_rows.append((idx, cells))
    separator_idx = {idx for idx, cells in raw_rows if _is_separator(cells)}
    header_idx: set[int] = set()
    for sep in separator_idx:
        before = [idx for idx, _ in raw_rows if idx < sep]
        if before:
            header_idx.add(before[-1])
    rows: list[tuple[str, list[str]]] = []
    for idx, cells in raw_rows:
        if idx in separator_idx or idx in header_idx:
            continue
        name = _class_name(cells[0])
        if not name or name.lower() == "class":
            continue
        rows.append((name, cells))

    names = [name for name, _ in rows]
    class_match = (
        len(receipt) == EXPECTED_CLASS_ROWS
        and not receipt_dupes
        and len(rows) == EXPECTED_CLASS_ROWS
        and len(set(names)) == len(names)
        and set(names) == set(receipt)
    )

    count_mismatch = 0
    bad_pairs: list[str] = []
    struct_bad: list[str] = []
    for name, cells in rows:
        if len(cells) != COLS:
            struct_bad.append(f"{name}(cells={len(cells)})")
        got = _cell_int(cells[1]) if len(cells) > 1 else None
        want = receipt.get(name)
        if got is None or want is None or got != want:
            count_mismatch += 1
            bad_pairs.append(f"{name}:got={got},want={want}")

    tokens: list[str] = []
    seen: set[str] = set()
    for tok in _path_tokens("\n".join(body)):
        if tok in seen:
            continue
        seen.add(tok)
        tokens.append(tok)
    resolved_tokens = [tok for tok in tokens if _resolves(root, tok)]
    escapes = [tok for tok in tokens if _escape_reason(root, tok) is not None]
    total = len(tokens)
    resolved = len(resolved_tokens)
    share = Fraction(resolved, total) if total else Fraction(0)

    row_ptr_bad: list[str] = []
    for name, cells in rows:
        if len(cells) < COLS:
            row_ptr_bad.append(f"{name}:missing-pointer-cell")
            continue
        cell_tokens = _path_tokens(cells[COLS - 1])
        if not cell_tokens:
            row_ptr_bad.append(f"{name}:no-path-token")
        elif not any(_resolves(root, tok) for tok in cell_tokens):
            row_ptr_bad.append(f"{name}:{cell_tokens[0]}")

    ok = (
        section_present
        and class_match
        and count_mismatch == 0
        and not struct_bad
        and not row_ptr_bad
        and not escapes
        and total > 0
        and resolved == total
        and share >= SHARE_FLOOR
    )

    out = [
        f"ROWS n={len(rows)} class_match={class_match} "
        f"count_mismatch={count_mismatch} "
        f"paths total={total} resolved={resolved} share={share:.2f}"
    ]
    if not ok:
        if not section_present:
            out.append(f"DETAIL section-absent heading={DEPTH_HEADING!r}")
        else:
            if escapes:
                out.append(f"DETAIL escape={_short(escapes)}")
            if len(receipt) != EXPECTED_CLASS_ROWS:
                out.append(
                    f"DETAIL receipt-classes={len(receipt)} expected={EXPECTED_CLASS_ROWS}"
                )
            if receipt_dupes:
                out.append(f"DETAIL receipt-duplicate-classes={_short(receipt_dupes)}")
            missing_classes = sorted(set(receipt) - set(names))
            unknown_classes = sorted(set(names) - set(receipt))
            if missing_classes:
                out.append(f"DETAIL missing-classes={_short(missing_classes)}")
            if unknown_classes:
                out.append(f"DETAIL unknown-classes={_short(unknown_classes)}")
            if len(names) != EXPECTED_CLASS_ROWS:
                out.append(f"DETAIL rows={len(names)} expected={EXPECTED_CLASS_ROWS}")
            if count_mismatch:
                out.append(f"DETAIL count-mismatch={_short(bad_pairs)}")
            if struct_bad:
                out.append(f"DETAIL structural-rows={_short(struct_bad)}")
            if row_ptr_bad:
                out.append(f"DETAIL row-pointer={_short(row_ptr_bad)}")
            if total == 0:
                out.append("DETAIL paths total=0")
            unresolved = [tok for tok in tokens if tok not in set(resolved_tokens)]
            if unresolved:
                out.append(f"DETAIL unresolved={_short(unresolved)}")
    out.append(f"PREDICATE R63-C2 {'pass' if ok else 'fail'}")
    return (0 if ok else 1), out


def cmd_depth(skill_arg: str, receipt_arg: str, root_arg: str) -> int:
    try:
        skill_text = pathlib.Path(skill_arg).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"SETUP cannot read {skill_arg}: {exc}", file=sys.stderr)
        return 2
    try:
        receipt_text = pathlib.Path(receipt_arg).read_text(
            encoding="utf-8", errors="replace"
        )
    except OSError as exc:
        print(f"SETUP cannot read {receipt_arg}: {exc}", file=sys.stderr)
        return 2
    rc, lines = depth_measure(skill_text, receipt_text, pathlib.Path(root_arg))
    for line in lines:
        print(line)
    return rc


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------
def _fixture_classes(count: int = EXPECTED_CLASS_ROWS) -> list[tuple[str, int]]:
    return [(f"class-{i:02d}", 1 + 3 * i) for i in range(count)]


# r64-C2 BAD-ESCAPE fixture tokens: an existing absolute host path outside any
# fixture root (the unpatched gate resolved it) and a ``..`` token.
SELFTEST_ESCAPE_TOKEN = "/usr/bin/"
SELFTEST_DOTDOT_TOKEN = "../escapee.json"


def _write_fixture(
    dirpath: pathlib.Path,
    *,
    wrong_count_on: int | None = None,
    escape_pointer_on: int | None = None,
    with_section: bool = True,
) -> dict[str, pathlib.Path]:
    dirpath.mkdir(parents=True, exist_ok=True)
    classes = _fixture_classes()
    receipt_lines = [
        "CLASS-CENSUS roster=16 tree-dirs=16 graders-classified=93 "
        f"unclassified=0 classes={len(classes)}"
    ]
    for name, count in classes:
        receipt_lines.append(f"CLASS {name} count={count} members={name}-member")
        record = dirpath / "records" / f"{name}.txt"
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(f"receipt for {name}\n", encoding="utf-8")
    notes = dirpath / "notes" / "summary.md"
    notes.parent.mkdir(parents=True, exist_ok=True)
    notes.write_text("fixture note\n", encoding="utf-8")
    receipt = dirpath / "class-survey.txt"
    receipt.write_text("\n".join(receipt_lines) + "\n", encoding="utf-8")

    md = ["# Fixture skill", "", "Pre-table prose."]
    if with_section:
        md.append(DEPTH_HEADING)
        md.append("")
        md.append("One row per census class.")
        md.append("")
        md.append("| class | count | executed | replay recipe | receipt pointer |")
        md.append("|---|---|---|---|---|")
        for i, (name, count) in enumerate(classes):
            cell_count = count + 1 if wrong_count_on == i else count
            pointer = f"`records/{name}.txt`"
            if escape_pointer_on == i:
                pointer = f"`{SELFTEST_ESCAPE_TOKEN}`"
            md.append(
                f"| {name} | {cell_count} | 0 | "
                f"recipe-unexecuted: stub | {pointer} |"
            )
        md.append("")
        see_also = "See also `records/` and `notes/summary.md`."
        if escape_pointer_on is not None:
            see_also += f" And `{SELFTEST_DOTDOT_TOKEN}`."
        md.append(see_also)
    else:
        md.append("## Grader ledger (not the decision table)")
        md.append("")
        md.append("| class | count |")
        md.append("|---|---|")
        md.append("| class-00 | 1 |")
    skill = dirpath / "SKILL.md"
    skill.write_text("\n".join(md) + "\n", encoding="utf-8")
    return {"skill": skill, "receipt": receipt, "root": dirpath}


def _rows_fields(line: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for token in line.split():
        if "=" in token:
            key, _, value = token.partition("=")
            fields[key] = value
    return fields


def run_selftest(work_arg: str) -> tuple[int, list[str]]:
    work = pathlib.Path(work_arg)
    if work.exists() and not work.is_dir():
        print(f"SETUP --work is not a directory: {work_arg}", file=sys.stderr)
        return 2, []
    work.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="r63-gate-", dir=str(work)))
    # label, fixture kwargs, expected rc, required fields on the ROWS line,
    # expected stable finding line (membership, verbatim)
    legs = [
        (
            "GOOD",
            {},
            0,
            {"n": "16", "class_match": "True", "count_mismatch": "0"},
            ["PREDICATE R63-C2 pass"],
        ),
        (
            "BAD-COUNT",
            {"wrong_count_on": 2},
            1,
            {"n": "16", "count_mismatch": "1"},
            ["DETAIL count-mismatch=class-02:got=8,want=7"],
        ),
        (
            "NO-SECTION",
            {"with_section": False},
            1,
            {"n": "0", "class_match": "False"},
            [f"DETAIL section-absent heading={DEPTH_HEADING!r}"],
        ),
        (
            "BAD-ESCAPE",
            {"escape_pointer_on": 0},
            1,
            {"n": "16", "class_match": "True", "count_mismatch": "0"},
            [f"DETAIL escape={SELFTEST_ESCAPE_TOKEN},{SELFTEST_DOTDOT_TOKEN}"],
        ),
    ]
    out: list[str] = []
    ok = True
    try:
        for label, kwargs, expect_rc, expect_fields, expect_lines in legs:
            fixture = _write_fixture(
                tmp / label.lower().replace("-", "_"), **kwargs
            )
            rc, lines = depth_measure(
                fixture["skill"].read_text(encoding="utf-8", errors="replace"),
                fixture["receipt"].read_text(encoding="utf-8", errors="replace"),
                fixture["root"],
            )
            fields = _rows_fields(lines[0])
            finding_ok = all(line in lines for line in expect_lines)
            leg_ok = (
                rc == expect_rc
                and all(
                    fields.get(key) == want for key, want in expect_fields.items()
                )
                and finding_ok
            )
            ok = ok and leg_ok
            out.append(
                f"SELFTEST {label} rc={rc} expect={expect_rc} "
                f"n={fields.get('n')} class_match={fields.get('class_match')} "
                f"count_mismatch={fields.get('count_mismatch')} "
                f"finding={'ok' if finding_ok else 'BAD'} "
                f"{'ok' if leg_ok else 'BAD'}"
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
        prog="round63_gate_checks.py",
        description="R63-C2 depth gate and provenance-trio gate (frozen round-63 claims).",
    )
    parser.add_argument("--selftest", action="store_true", help="run the four-fixture selftest")
    parser.add_argument("--work", default=None, help="work dir for --selftest (mkdtemp parent)")
    sub = parser.add_subparsers(dest="cmd")

    p_trio = sub.add_parser("trio", help="provenance trio <file>")
    p_trio.add_argument("file")

    p_depth = sub.add_parser("depth", help="grader-class decision-table depth")
    p_depth.add_argument("--skill", required=True)
    p_depth.add_argument("--receipt", required=True)
    p_depth.add_argument("--root", default=".")

    p_self = sub.add_parser("selftest", help="alias for --selftest")
    p_self.add_argument("--work", dest="work_sub", default=None)

    args = parser.parse_args(argv)

    if args.selftest or args.cmd == "selftest":
        work = args.work_sub if args.cmd == "selftest" else args.work
        if not work:
            parser.print_usage(sys.stderr)
            print("error: selftest requires --work <dir>", file=sys.stderr)
            return 2
        rc, lines = run_selftest(work)
        for line in lines:
            print(line)
        return rc
    if args.cmd == "trio":
        return cmd_trio(args.file)
    if args.cmd == "depth":
        return cmd_depth(args.skill, args.receipt, args.root)
    parser.print_usage(sys.stderr)
    print("error: expected 'trio <file>', 'depth ...' or '--selftest --work <dir>'", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
