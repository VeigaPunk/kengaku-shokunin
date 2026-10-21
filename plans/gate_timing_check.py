#!/usr/bin/env python3
"""Check that Gate admits name returned second-seat reports in the landing tree.

The lesson and every report are read from the requested Git commit, not the
working tree. Generic seat references cannot support an admit. The checker is
offline and uses read-only Git operations.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable

FULL_REPORT_RE = re.compile(
    r"(?P<path>\.ufo/waves/round-(?P<round>\d+)/"
    r"(?P<wave>[A-Za-z0-9][A-Za-z0-9_-]*)/"
    r"(?P<name>[A-Za-z0-9][A-Za-z0-9_.-]*\.md))"
)
RELATIVE_REPORT_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])(?P<path>(?P<wave>build|falsify|wave[-_ ]?0*\d+)/"
    r"(?P<name>[A-Za-z0-9][A-Za-z0-9_.-]*\.md))"
)
BARE_REPORT_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])(?P<name>[A-Z][A-Za-z0-9_.-]*\.md)"
    r"(?![A-Za-z0-9_.-])"
)
GENERIC_RE = re.compile(
    r"\b(?:"
    r"wave[\s-]*0*\d+\s+(?:seats?|reports?)|"
    r"by\s+wave[\s-]*0*\d+(?!\s+(?:seats?|reports?)\b)|"
    r"(?:by\s+)?(?:the\s+)?falsify\s+(?:seats?|reports?|wave)|"
    r"(?:the\s+)?rest\s+of\s+(?:the\s+)?falsify\s+wave|"
    r"(?:second|wave[\s-]*0*\d+)\s+seats?"
    r")\b",
    re.IGNORECASE,
)
ROUND_COMPONENT_RE = re.compile(r"^(?:round-(\d+)|r(\d+))(?:\.md)?$", re.IGNORECASE)
ROUND_HEADING_RE = re.compile(r"^\s*#{1,6}\s+Round\s+(\d+)\b", re.IGNORECASE | re.MULTILINE)
ROUND_REPORT_RE = re.compile(r"\.ufo/waves/round-(\d+)/")
ROUND_LESSON_RE = re.compile(r"^round-(\d+)\.md$", re.IGNORECASE)
WRITER_RE = re.compile(r"^writer:\s*`?([^`\s#]+)", re.IGNORECASE | re.MULTILINE)
VERDICT_RE = re.compile(r"^VERDICT:\s*(\S.*?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class GateAdmission:
    line: int
    candidate: str
    decision: str
    reason: str
    source: str


@dataclass(frozen=True)
class Citation:
    raw: str
    path: str
    kind: str
    start: int
    end: int


@dataclass(frozen=True)
class TreeFile:
    mode: str
    size: int


@dataclass(frozen=True)
class AuditResult:
    admission: GateAdmission
    ok: bool
    citations: tuple[Citation, ...]
    generic: tuple[str, ...]
    existing_second: tuple[str, ...]
    invalid_second: tuple[tuple[str, str], ...]
    unresolved_bare: tuple[str, ...]
    reasons: tuple[str, ...]


def split_table_row(line: str) -> list[str] | None:
    """Split one Markdown table row without treating escaped pipes as separators."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    cells: list[str] = []
    cell: list[str] = []
    escaped = False
    for char in stripped:
        if escaped:
            cell.append(char)
            escaped = False
        elif char == "\\":
            cell.append(char)
            escaped = True
        elif char == "|":
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(char)
    if cell:
        cells.append("".join(cell).strip())
    if cells and cells[0] == "":
        cells.pop(0)
    if cells and cells[-1] == "":
        cells.pop()
    return cells


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", ""))
                               for cell in cells)


def plain_cell(cell: str) -> str:
    return re.sub(r"[`*_]", "", cell).strip()


def is_admit(decision: str) -> bool:
    return bool(re.match(r"^admit(?:ted)?(?:\b|$)", plain_cell(decision), re.IGNORECASE))


def parse_gate_admissions(text: str) -> tuple[bool, list[GateAdmission]]:
    """Return whether a Gate section exists and all rows whose decision is admit."""
    in_gate = False
    gate_level = 0
    gate_found = False
    header: list[str] | None = None
    admissions: list[GateAdmission] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        heading = re.match(r"^(#{1,6})[ \t]+(.+?)\s*#*\s*$", line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            if in_gate and level <= gate_level:
                in_gate = False
                header = None
            if re.match(r"^Gate(?:\b|\s*[—:-])", title, re.IGNORECASE):
                in_gate = True
                gate_level = level
                gate_found = True
                header = None
            continue
        if not in_gate:
            continue
        cells = split_table_row(line)
        if cells is None:
            header = None
            continue
        normalized = [plain_cell(cell).casefold() for cell in cells]
        if {"candidate", "decision", "reason"}.issubset(normalized):
            header = normalized
            continue
        if is_separator_row(cells) or header is None:
            continue
        try:
            candidate_i = header.index("candidate")
            decision_i = header.index("decision")
            reason_i = header.index("reason")
        except ValueError:
            header = None
            continue
        if max(candidate_i, decision_i, reason_i) >= len(cells):
            continue
        decision = cells[decision_i]
        if is_admit(decision):
            admissions.append(GateAdmission(
                line=line_no,
                candidate=plain_cell(cells[candidate_i]),
                decision=decision,
                reason=cells[reason_i],
                source=line,
            ))
    return gate_found, admissions


def _overlaps(span: tuple[int, int], ranges: list[tuple[int, int]]) -> bool:
    return any(span[0] < end and start < span[1] for start, end in ranges)


def extract_citations(text: str) -> tuple[Citation, ...]:
    """Find full, wave-relative, and bare seat-report references in one Gate cell."""
    citations: list[Citation] = []
    occupied: list[tuple[int, int]] = []
    for match in FULL_REPORT_RE.finditer(text):
        citations.append(Citation(match.group("path"), match.group("path"), "full",
                                  *match.span("path")))
        occupied.append(match.span())
    for match in RELATIVE_REPORT_RE.finditer(text):
        if _overlaps(match.span(), occupied):
            continue
        citations.append(Citation(match.group("path"), match.group("path"), "relative",
                                  *match.span("path")))
        occupied.append(match.span())
    for match in BARE_REPORT_RE.finditer(text):
        if _overlaps(match.span(), occupied):
            continue
        name = match.group("name")
        citations.append(Citation(name, name, "bare", *match.span("name")))
        occupied.append(match.span("name"))
    return tuple(sorted(citations, key=lambda item: (item.start, item.end)))


def extract_generic_references(text: str, citations: tuple[Citation, ...]) -> tuple[str, ...]:
    chars = list(text)
    for citation in citations:
        for index in range(citation.start, citation.end):
            if chars[index] not in "\r\n":
                chars[index] = " "
    return tuple(match.group(0) for match in GENERIC_RE.finditer("".join(chars)))


def wave_directory(path: str, round_number: int) -> str | None:
    parts = PurePosixPath(path).parts
    if len(parts) != 5 or parts[:3] != (".ufo", "waves", f"round-{round_number}"):
        return None
    return parts[3]


def is_second_wave(directory: str | None) -> bool:
    return bool(directory and (directory.casefold() == "falsify"
                               or re.fullmatch(r"wave[-_ ]?0*2", directory, re.IGNORECASE)))


def valid_repo_path(path: str) -> bool:
    parsed = PurePosixPath(path)
    return not parsed.is_absolute() and bool(parsed.parts) and not any(
        part in ("", ".", "..") for part in parsed.parts)


def candidate_writer(text: str | None) -> str | None:
    if text is None:
        return None
    match = WRITER_RE.search(text)
    return match.group(1).strip() if match else None


def resolve_citations(citations: tuple[Citation, ...], round_number: int,
                      tree_files: dict[str, TreeFile]) -> tuple[set[str], set[str]]:
    """Resolve citation paths and return (second-wave candidates, unresolved bare names)."""
    reports: set[str] = set()
    unresolved: set[str] = set()
    by_name: dict[str, list[str]] = {}
    for path in tree_files:
        if path.endswith(".md") and wave_directory(path, round_number) is not None:
            by_name.setdefault(PurePosixPath(path).name, []).append(path)
    for citation in citations:
        if citation.kind == "full":
            path = citation.path
        elif citation.kind == "relative":
            path = f".ufo/waves/round-{round_number}/{citation.path}"
        else:
            matches = by_name.get(citation.path, [])
            if len(matches) != 1:
                unresolved.add(citation.path)
                continue
            path = matches[0]
        if is_second_wave(wave_directory(path, round_number)):
            reports.add(path)
    return reports, unresolved


def load_members(round_number: int, tree_files: dict[str, TreeFile],
                 read_blob: Callable[[str], str | None]) -> dict[tuple[str, str], str]:
    """Map (wave directory, registered seat name) to its declared role."""
    wave_dirs = sorted({directory for path in tree_files
                        if (directory := wave_directory(path, round_number))
                        and is_second_wave(directory)})
    members: dict[tuple[str, str], str] = {}
    for directory in wave_dirs:
        path = f".ufo/waves/round-{round_number}/{directory}/swarm-registry.json"
        content = read_blob(path)
        if content is None:
            continue
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            continue
        entries = data.get("members") if isinstance(data, dict) else None
        if not isinstance(entries, dict):
            continue
        for seat, member in entries.items():
            if isinstance(seat, str) and isinstance(member, dict):
                role = member.get("role")
                members[(directory, seat)] = role.casefold() if isinstance(role, str) else ""
    return members


def resolve_candidate_path(candidate: str, read_blob: Callable[[str], str | None]) -> str | None:
    if not valid_repo_path(candidate):
        return None
    for path in (candidate, f"corpus/{candidate}"):
        if read_blob(path) is not None:
            return path
    return None

def audit_admission(admission: GateAdmission, round_number: int,
                    tree_files: dict[str, TreeFile],
                    members: dict[tuple[str, str], str],
                    read_blob: Callable[[str], str | None]) -> AuditResult:
    citations = extract_citations(admission.reason)
    generic = extract_generic_references(admission.reason, citations)
    report_paths, unresolved_bare = resolve_citations(citations, round_number, tree_files)
    entry_path = resolve_candidate_path(admission.candidate, read_blob)
    entry_text = read_blob(entry_path) if entry_path is not None else None
    writer = candidate_writer(entry_text)
    invalid: dict[str, str] = {}
    existing: set[str] = set()

    for path in sorted(report_paths):
        meta = tree_files.get(path)
        directory = wave_directory(path, round_number)
        seat = PurePosixPath(path).stem
        role = members.get((directory or "", seat))
        content = read_blob(path) if meta is not None else None
        if meta is None:
            invalid[path] = "absent from commit tree"
        elif meta.mode != "100644" or meta.size <= 0:
            invalid[path] = f"not a nonempty regular report (mode={meta.mode}, size={meta.size})"
        elif role is None:
            invalid[path] = "seat is not in the committed wave registry"
        elif role in {"scribe", "executor"}:
            invalid[path] = f"seat role {role!r} is not an independent re-reader"
        elif writer is None:
            invalid[path] = "candidate has no committed writer: field; self-review cannot be excluded"
        elif seat.casefold() == writer.casefold():
            invalid[path] = f"seat is the candidate writer {writer!r}"
        elif content is None or not any(form in content for form in (admission.candidate, entry_path or "")):
            invalid[path] = "report does not name the admitted candidate path"
        elif not VERDICT_RE.findall(content):
            invalid[path] = "report has no anchored VERDICT line; return is not established"
        else:
            existing.add(path)

    reasons: list[str] = []
    if not entry_path or entry_text is None:
        reasons.append("admitted candidate is absent from the commit tree")
    if not existing:
        reasons.append("no cited, existing, returned second-seat report for this round")
    if invalid:
        reasons.append("one or more cited second-seat reports fail identity/return checks")
    if unresolved_bare:
        reasons.append("one or more bare report references do not resolve uniquely")
    if generic:
        reasons.append("generic seat references are not report evidence")
    ok = bool(existing) and not invalid and not unresolved_bare and not generic and entry_text is not None
    return AuditResult(
        admission=admission,
        ok=ok,
        citations=citations,
        generic=generic,
        existing_second=tuple(sorted(existing)),
        invalid_second=tuple(sorted(invalid.items())),
        unresolved_bare=tuple(sorted(unresolved_bare)),
        reasons=tuple(reasons),
    )


def infer_round_number(lesson_path: str, lesson_text: str) -> int | None:
    """Infer round from conventional path components, then lesson heading, then wave paths."""
    path_rounds: set[int] = set()
    for component in PurePosixPath(lesson_path).parts:
        match = ROUND_COMPONENT_RE.fullmatch(component)
        if match:
            path_rounds.add(int(match.group(1) or match.group(2)))
    if len(path_rounds) == 1:
        return next(iter(path_rounds))
    if len(path_rounds) > 1:
        return None
    heading_rounds = {int(value) for value in ROUND_HEADING_RE.findall(lesson_text)}
    if len(heading_rounds) == 1:
        return next(iter(heading_rounds))
    if len(heading_rounds) > 1:
        return None
    report_rounds = {int(value) for value in ROUND_REPORT_RE.findall(lesson_text)}
    return next(iter(report_rounds)) if len(report_rounds) == 1 else None


def run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def parse_tree(stdout: str) -> dict[str, TreeFile]:
    files: dict[str, TreeFile] = {}
    for line in stdout.splitlines():
        metadata, separator, path = line.partition("\t")
        fields = metadata.split()
        if not separator or len(fields) < 4:
            continue
        mode, kind, _object, size_text = fields[:4]
        if kind != "blob":
            continue
        try:
            size = int(size_text)
        except ValueError:
            continue
        files[path] = TreeFile(mode=mode, size=size)
    return files


def print_result(result: AuditResult, round_number: int, commit: str,
                 second_inventory: list[str]) -> None:
    admission = result.admission
    status = "PASS" if result.ok else "FAIL"
    print(f"{status} line {admission.line} Gate admit: candidate={admission.candidate!r}")
    if not result.ok:
        print(f"  cell[reason]: {admission.reason}")
    if result.citations:
        print("  cited seat-report paths: " + ", ".join(repr(item.path) for item in result.citations))
    else:
        print("  cited seat-report paths: none")
    if result.existing_second:
        print("  existing returned second-seat report(s): " + ", ".join(result.existing_second))
    for path, reason in result.invalid_second:
        print(f"  invalid cited second-seat report: {path} ({reason})")
    if result.unresolved_bare:
        print("  unresolved bare report reference(s): " + ", ".join(result.unresolved_bare))
    if result.generic:
        print("  generic seat reference(s) (not report support): "
              + ", ".join(repr(item) for item in result.generic))
    if not result.ok and not result.existing_second:
        falsify = f".ufo/waves/round-{round_number}/falsify/"
        falsify_reports = [path for path in second_inventory if path.startswith(falsify)]
        if not falsify_reports:
            print(f"  missing: no {falsify} report exists in commit {commit}")
        elif second_inventory:
            print(f"  missing: Gate does not name a valid second-seat report by path; the commit has "
                  f"{len(second_inventory)} second-seat report(s)")
        else:
            print(f"  missing: no second-seat report exists under .ufo/waves/round-{round_number}/ "
                  f"in commit {commit}")
    if result.reasons:
        print("  reasons: " + "; ".join(result.reasons))


def safe_round_path(lesson: str) -> bool:
    parsed = PurePosixPath(lesson)
    return not parsed.is_absolute() and bool(parsed.parts) and not any(
        part in ("", ".", "..") for part in parsed.parts)


def run_selftest() -> int:
    round_number = 7
    report = ".ufo/waves/round-7/falsify/SecondSeat.md"
    other = ".ufo/waves/round-7/falsify/OtherSeat.md"
    build = ".ufo/waves/round-7/build/BuildSeat.md"
    same_writer = ".ufo/waves/round-7/falsify/EntryAuthor.md"
    stub = ".ufo/waves/round-7/falsify/Stub.md"
    index = ".ufo/waves/round-7/falsify/INDEX.md"
    symlink = ".ufo/waves/round-7/falsify/Link.md"
    candidate = "knowledge/x.md"
    report_text = f"Re-read {candidate}\n\nVERDICT: PASS — checked\n"
    header = "## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n"
    reject = "| rejected candidate | reject | no second-seat review |\n"
    writer_text = "writer: EntryAuthor\n# Candidate\n"
    tree = {
        candidate: TreeFile("100644", len(writer_text)),
        report: TreeFile("100644", len(report_text)),
        build: TreeFile("100644", 20),
        same_writer: TreeFile("100644", len(report_text)),
        stub: TreeFile("100644", 0),
        index: TreeFile("100644", 20),
        symlink: TreeFile("120000", len(report_text)),
    }
    members = {
        ("falsify", "SecondSeat"): "reviewer",
        ("falsify", "EntryAuthor"): "reviewer",
        ("falsify", "Stub"): "reviewer",
        ("falsify", "Link"): "reviewer",
        ("build", "BuildSeat"): "reviewer",
    }
    blobs = {candidate: writer_text, report: report_text,
             build: f"Re-read {candidate}\nVERDICT: PASS\n",
             same_writer: f"Re-read {candidate}\nVERDICT: PASS\n",
             stub: "", index: f"Re-read {candidate}\nVERDICT: PASS\n",
             symlink: report}

    cases = [
        ("generic-only red", "Q10 checked by wave-2 seats", False, set(), None),
        ("full path green", f"Q10 `{report}`", True, {report}, None),
        ("bare unique path green", "Q10 `SecondSeat.md`", True, {report}, None),
        ("absent path red", f"Q10 `{other}`", False, {other}, None),
        ("explicit path plus generic red", f"Q10 `{report}` and wave-2 seats", False, {report}, None),
        ("falsify-wave generic red", f"Q10 `{report}` and the rest of the falsify wave", False,
         {report}, None),
        ("unresolved bare red", f"Q10 `{report}` and `LateSeat.md`", False, {report}, None),
        ("build report excluded", f"Q10 `{build}`", False, {build}, None),
        ("unregistered INDEX excluded", f"Q10 `{index}`", False, {index}, None),
        ("empty report excluded", f"Q10 `{stub}`", False, {stub}, None),
        ("symlink excluded", f"Q10 `{symlink}`", False, {symlink}, None),
        ("self-review excluded", f"Q10 `{same_writer}`", False, {same_writer}, None),
        ("unknown writer fails closed", f"Q10 `{report}`", False, {report}, {candidate: "# Candidate\n"}),
        ("unreturned report excluded", f"Q10 `{report}`", False, {report}, {report: None}),
        ("candidate target required", f"Q10 `{report}`", False, {report}, {report: f"unrelated\nVERDICT: PASS\n"}),
        ("verdict required", f"Q10 `{report}`", False, {report}, {report: f"Re-read {candidate}\n"}),
    ]
    for label, reason, expected, cite_paths, content_overrides in cases:
        text = header + f"| `{candidate}` | **admit** | {reason} |\n" + reject
        gate_found, admissions = parse_gate_admissions(text)
        if not gate_found or len(admissions) != 1:
            print(f"selftest: {label}: expected one parsed admit, got {len(admissions)}", file=sys.stderr)
            return 1
        case_tree = dict(tree)
        case_members = dict(members)
        case_blobs = dict(blobs)
        if content_overrides:
            case_blobs.update(content_overrides)
        def read_fixture(path: str) -> str | None:
            return case_blobs.get(path)
        result = audit_admission(admissions[0], round_number, case_tree, case_members, read_fixture)
        if result.ok != expected:
            print(f"selftest: {label}: expected {'PASS' if expected else 'FAIL'}, got "
                  f"{'PASS' if result.ok else 'FAIL'}", file=sys.stderr)
            return 1

    inferred = infer_round_number("plans/fixtures/r26/gate_timing/late-report.md", "# Q13 fixture\n")
    if inferred != 26:
        print(f"selftest: arbitrary lesson basename round inference failed: {inferred!r}", file=sys.stderr)
        return 1
    print("[selftest] ALL PASS (arbitrary lesson basename, generic-only/variant red, explicit/bare citation, "
          "missing/unresolved citation, registry/mode/return/self-review/unknown-writer checks)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lesson", help="repo-relative lesson path")
    parser.add_argument("--commit", help="landing commit or revision")
    parser.add_argument("--repo", type=Path,
                        default=Path(__file__).resolve().parent.parent,
                        help="repository containing the commit (default: this repository)")
    parser.add_argument("--selftest", action="store_true",
                        help="run local in-memory fixtures without repository writes")
    args = parser.parse_args(argv)
    if args.selftest:
        if args.lesson or args.commit:
            parser.error("--selftest cannot be combined with --lesson or --commit")
        return run_selftest()
    if not args.lesson or not args.commit:
        parser.error("--lesson and --commit are required unless --selftest is used")
    if args.commit.startswith("-"):
        parser.error("--commit must not start with '-'")
    if not safe_round_path(args.lesson):
        parser.error("--lesson must be a normalized repository-relative path")

    try:
        repo = args.repo.expanduser().resolve(strict=True)
    except OSError as exc:
        print(f"gate_timing_check: INPUT ERROR: --repo cannot be resolved: {exc}", file=sys.stderr)
        return 2
    if not repo.is_dir():
        print(f"gate_timing_check: INPUT ERROR: --repo is not a directory: {repo}", file=sys.stderr)
        return 2

    lesson_result = run_git(repo, "show", f"{args.commit}:{args.lesson}")
    if lesson_result.returncode:
        detail = lesson_result.stderr.strip() or "git show failed"
        print(f"gate_timing_check: INPUT ERROR: cannot read {args.lesson} at {args.commit}: {detail}",
              file=sys.stderr)
        return 2
    round_number = infer_round_number(args.lesson, lesson_result.stdout)
    if round_number is None:
        print(f"gate_timing_check: INPUT ERROR: cannot infer round number from {args.lesson}",
              file=sys.stderr)
        return 2

    tree_result = run_git(repo, "ls-tree", "-rl", args.commit, "--",
                          f".ufo/waves/round-{round_number}")
    if tree_result.returncode:
        detail = tree_result.stderr.strip() or "git ls-tree failed"
        print(f"gate_timing_check: INPUT ERROR: cannot inspect commit {args.commit}: {detail}",
              file=sys.stderr)
        return 2
    tree_files = parse_tree(tree_result.stdout)
    blob_cache: dict[str, str | None] = {}

    def read_blob(path: str) -> str | None:
        if path in blob_cache:
            return blob_cache[path]
        if not valid_repo_path(path):
            blob_cache[path] = None
            return None
        result = run_git(repo, "show", f"{args.commit}:{path}")
        blob_cache[path] = result.stdout if result.returncode == 0 else None
        return blob_cache[path]

    gate_found, admissions = parse_gate_admissions(lesson_result.stdout)
    if not gate_found:
        print(f"gate_timing_check: FAIL: no ## Gate section in {args.lesson} at {args.commit}")
        print("gate_timing_check: admissions=0 passed=0 failed=1")
        return 1
    if not admissions:
        print(f"gate_timing_check: FAIL: no admit rows in ## Gate of {args.lesson} at {args.commit}")
        print("gate_timing_check: admissions=0 passed=0 failed=1")
        return 1

    members = load_members(round_number, tree_files, read_blob)
    second_inventory = sorted(path for path in tree_files
                              if path.endswith(".md")
                              and is_second_wave(wave_directory(path, round_number)))
    results = [audit_admission(row, round_number, tree_files, members, read_blob)
               for row in admissions]
    for result in results:
        print_result(result, round_number, args.commit, second_inventory)
    passed = sum(result.ok for result in results)
    failed = len(results) - passed
    print(f"gate_timing_check: commit={args.commit} lesson={args.lesson} "
          f"admissions={len(results)} passed={passed} failed={failed} "
          f"second-seat-reports={len(second_inventory)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
