#!/usr/bin/env python3
"""R76-C1 counter — every surface PROVINCE.md declares is resolved live, and the row says so.

Frozen before data on 2026-11-04 (L1 KengakuR76); see plans/round-76-claims.md §R76-C1.
The receipt printed by `--receipt` names the revision whose declared bytes were read and whether
the worktree was clean (the R74-D1/R75 stamp discipline).

    python3 plans/round76_c1_surface_resolver.py --lane .                    # verdict, worktree
    python3 plans/round76_c1_surface_resolver.py --lane . --rev 4c4249a2     # declared bytes at a rev
    python3 plans/round76_c1_surface_resolver.py --selftest --work DIR        # fixture battery
    python3 plans/round76_c1_surface_resolver.py --mutants --work DIR         # attributed mutant matrix
    python3 plans/round76_c1_surface_resolver.py --control-declared --work DIR # the skip that must lose

Why this counter exists: `AXES.md` scores coverage as "PROVINCE.md lists every surface; none
unexplored without reason", and PROVINCE.md is the lane's declaration of what it can measure. Until
round 76 the table's truth was re-derived by hand: a seat sweep (round-75 `SourcesHostR75`) found
`~/archive/bench-arena` absent while the row still read "relocated intact", and no command in the
repo could price the table. This counter parses the `## Surfaces` table, resolves the first declared
path/endpoint of every row *live* (`test -e` for paths, an HTTP status for localhost endpoints) and
requires the row's own dated declaration to agree with the live verdict.

Rows (each printed; every defect fails the predicate):
  SURFACE <n> <verdict> <identity>        one line per declared row, verdict present|absent
  SURFACES total=N present=P absent=A prose=B
  AGREE agree=N disagree=D                D must equal the defect count (no literal tallies)
  DEFECT <class> <n> <name> ...           UNDECLARED-ABSENT, STALE-ABSENT, STALE-TEXT,
                                          NOANCHOR, MALFORMED
Exit 0 pass, 1 fail, 2 setup.

Frozen rules, named here so the closure can re-read them:
  - The surface identity is the **first** backticked span in the row's path cell that names a
    `~/…` path, a repo-relative path, or an `http://` endpoint. A row with no such span is
    `NOANCHOR` (the declaration names nothing a command can resolve).
  - `absent` row with no `ABSENT YYYY-MM-DD` marker in the row  -> UNDECLARED-ABSENT.
  - `present` row that carries an `ABSENT YYYY-MM-DD` marker      -> STALE-ABSENT.
  - `absent` row whose path cell still asserts present-tense life  -> STALE-TEXT
    (the round-74/75 class: prose advertised what the host no longer had).
  - Rows must have at least three cells; anything else is MALFORMED.
"""
from __future__ import annotations

import argparse
import contextlib
import http.server
import re
import io
import shutil
import socket
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

PROVINCE = "PROVINCE.md"
SECTION = "## Surfaces"
CELLSPLIT = re.compile(r"(?<!\\)\|")
BACKTICK = re.compile(r"`([^`]+)`")
HOME_PATH = re.compile(r"^~/[^\s)]*$")
REPO_PATH = re.compile(r"^[A-Za-z0-9_.][A-Za-z0-9_.~/-]*$")
FILE_NAME = re.compile(r"^[A-Za-z0-9_.-]+\.(py|sh|md|json|jsonl|txt)$")
ENDPOINT = re.compile(r"^https?://[^\s`]+$")
MARKER = re.compile(r"\*\*ABSENT (\d{4}-\d{2}-\d{2})\*\*|ABSENT (\d{4}-\d{2}-\d{2})")
STALE_TEXT = (
    "relocated intact",
    "all resolve at",
    "resolves today",
    "is alive",
    "LISTEN on",
    "still resolves",
)
TIMEOUT = 3


# ---------------------------------------------------------------- revision reads
def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


class Reader:
    """Reads a lane path from the worktree or from a git revision (declared bytes)."""

    def __init__(self, lane: Path, rev: str) -> None:
        self.lane = lane
        self.rev = rev
        proc = git(lane, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}" if rev not in ("worktree", "", None) else "master^{commit}")
        self.tip = proc.stdout.strip() if proc.returncode == 0 and proc.stdout.strip() else "unknown"

    def get(self, rel: str) -> str:
        if self.rev in ("worktree", "", None):
            p = self.lane / rel
            return p.read_text(errors="replace") if p.exists() else ""
        proc = git(self.lane, "show", f"{self.rev}:{rel}")
        return proc.stdout if proc.returncode == 0 else ""


def worktree_dirty(lane: Path) -> bool:
    return bool(git(lane, "status", "--porcelain", "--untracked-files=no").stdout.strip())


# ---------------------------------------------------------------- parsing
def table_rows(text: str) -> list[tuple[int, list[str]]]:
    """(line number, cells) for every row of the `## Surfaces` table, in order."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith(SECTION):
            start = i + 1
            break
    if start is None:
        return []
    rows: list[tuple[int, list[str]]] = []
    for i in range(start, len(lines)):
        line = lines[i]
        if line.startswith("## "):
            break
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in CELLSPLIT.split(line.strip())[1:-1]]
        if not cells or all(set(c) <= {"-", ":", " "} for c in cells):
            continue  # separator row
        if cells and cells[0].strip() in ("Surface",):
            continue  # header row
        rows.append((i + 1, cells))
    return rows


def identity(path_cell: str) -> tuple[str, str]:
    """('endpoint'|'path'|'prose', token) from the first resolvable backticked span."""
    for span in BACKTICK.findall(path_cell):
        tok = span.strip()
        if ENDPOINT.match(tok):
            return "endpoint", tok
        if tok.startswith("~/"):
            return "path", tok
        if REPO_PATH.match(tok) and ("/" in tok or FILE_NAME.match(tok)) and " " not in tok:
            return "path", tok
    return "prose", ""


# ---------------------------------------------------------------- resolution
def expand_braces(token: str) -> list[str]:
    """`{a,b}` alternatives expand to concrete paths; the row's verdict covers the set."""
    m = re.search(r"\{([^{}]*)\}", token)
    if not m:
        return [token]
    out: list[str] = []
    for alt in m.group(1).split(","):
        out.extend(expand_braces(token[: m.start()] + alt + token[m.end():]))
    return out


def http_status(url: str) -> str:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:  # noqa: S310 - localhost probe
            return str(resp.status)
    except urllib.error.HTTPError as exc:
        return str(exc.code)
    except (urllib.error.URLError, socket.timeout, ConnectionError, OSError):
        return "000"


def resolve(kind: str, token: str, lane: Path) -> tuple[str, str]:
    if kind == "endpoint":
        code = http_status(token)
        return ("absent" if code == "000" else "present"), f"http={code}"
    if kind == "path":
        targets = expand_braces(token)
        hits = [t for t in targets if (Path(t).expanduser() if t.startswith("~/") else lane / t).exists()]
        verdict = "present" if hits else "absent"
        detail = f"path={hits[0] if hits else targets[0]}"
        if len(targets) > 1:
            detail += f" expanded={len(targets)}"
        return verdict, detail
    return "prose", "no-anchor"


def census(lane: Path, reader: Reader) -> tuple[list[str], list[str]]:
    defects: list[str] = []
    report: list[str] = []
    rows = table_rows(reader.get(PROVINCE))
    if not rows:
        return [f"SETUP no `{SECTION}` table in {PROVINCE}"], []
    counts = {"present": 0, "absent": 0, "prose": 0}
    agree = disagree = 0
    for idx, (_lineno, cells) in enumerate(rows, start=1):
        name = cells[0][:48] if cells else "?"
        if len(cells) < 3:
            defects.append(f"DEFECT MALFORMED {idx} {name} cells={len(cells)}")
            disagree += 1
            continue
        row_text = " | ".join(cells)
        kind, token = identity(cells[1])
        if kind == "prose":
            defects.append(f"DEFECT NOANCHOR {idx} {name}")
            counts["prose"] += 1
            disagree += 1
            report.append(f"SURFACE {idx} prose {name}")
            continue
        verdict, detail = resolve(kind, token, lane)
        counts[verdict] += 1
        report.append(f"SURFACE {idx} {verdict} {token} ({detail})")
        marker = MARKER.search(row_text)
        stale_text = [t for t in STALE_TEXT if t in cells[1] and verdict == "absent"]
        if verdict == "absent" and not marker:
            defects.append(f"DEFECT UNDECLARED-ABSENT {idx} {name} {token}")
            disagree += 1
        elif verdict == "present" and marker:
            defects.append(f"DEFECT STALE-ABSENT {idx} {name} {token} marked {marker.group(0)}")
            disagree += 1
        elif stale_text:
            defects.append(
                f"DEFECT STALE-TEXT {idx} {name} {token} asserts {stale_text[0]!r} while absent"
            )
            disagree += 1
        else:
            agree += 1
    report.append(
        f"SURFACES total={len(rows)} present={counts['present']} "
        f"absent={counts['absent']} prose={counts['prose']}"
    )
    report.append(f"AGREE agree={agree} disagree={disagree}")
    return defects, report


def emit(lane: Path, rev: str, out: Path | None) -> int:
    if not lane.is_dir():
        print(f"SETUP ERROR: lane {lane} is not a directory", file=sys.stderr)
        return 2
    reader = Reader(lane, rev)
    defects, report = census(lane, reader)
    if defects and defects[0].startswith("SETUP"):
        print(defects[0], file=sys.stderr)
        return 2
    disagree = next((int(l.split("disagree=")[1]) for l in report if l.startswith("AGREE")), 0)
    # A printed tally that does not equal the defect list length is itself a defect (R75-M12).
    if disagree != len(defects):
        defects.append(f"DEFECT TALLY-MISMATCH printed={disagree} defects={len(defects)}")
    lines = report + defects
    lines.append(f"PREDICATE R76-C1 {'pass' if not defects else 'fail'}")
    tip, dirty = reader.tip, worktree_dirty(lane)
    text = "\n".join([f"LANE_TIP {tip}", f"WORKTREE {'dirty' if dirty else 'clean'}"] + lines) + "\n"
    print("\n".join(lines) + "\n", end="")
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    return 0 if not defects else 1


# ---------------------------------------------------------------- fixtures
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args: object) -> None:  # silence the fixture server
        return


class Listener:
    """A live localhost endpoint for the selftest's present-endpoint arms (no external traffic)."""

    def __init__(self) -> None:
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def __enter__(self) -> "Listener":
        self.thread.start()
        return self

    def __exit__(self, *exc: object) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()

    @property
    def dead_url(self) -> str:
        """A URL on the same host that refuses connections (port 1)."""
        return "http://127.0.0.1:1/health"


def build_fixture(root: Path, *, live_port: int | None = None, drop_marker: str = "",
                  add_marker: str = "", strip_anchor: str = "", stale_text: bool = False,
                  malformed: bool = False) -> None:
    """A minimal PROVINCE.md with one present path, one absent path, one endpoint, one extra row."""
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    (root / "present.md").write_text("# present\n")
    live = f"http://127.0.0.1:{live_port}/x" if live_port else "http://127.0.0.1:1/x"
    absent_cell = "`~/r76-definitely-absent-path` — **ABSENT 2026-10-01**, never resolved"
    if drop_marker == "absent-path":
        absent_cell = "`~/r76-definitely-absent-path` — never resolved"
    present_cell = "`present.md` (repo root; always on disk)"
    if add_marker == "present-path":
        present_cell = "`present.md` — **ABSENT 2026-10-01**"
    if stale_text:
        absent_cell = "`~/r76-definitely-absent-path` — **ABSENT 2026-10-01**, relocated intact in round 14"
    ep_cell = f"`{live}` — /x  **ABSENT 2026-10-01**" if live_port is None else f"`{live}` — /x"
    rows = [
        "| Surface | Path / endpoint | What |",
        "|---|---|---|",
        f"| Present path | {present_cell} | fixture |",
        f"| Absent path | {absent_cell} | fixture |",
        f"| Endpoint | {ep_cell} | fixture |",
    ]
    if strip_anchor == "literature":
        rows.append("| Literature | arXiv / ACL Anthology (URLs in prose) | fixture |")
    if malformed:
        rows.append("| Malformed | only two cells |")
    body = ["# fixture PROVINCE", "", SECTION, "", *rows, "", "## Next", ""]
    (root / "PROVINCE.md").write_text("\n".join(body) + "\n")


def selftest(work: Path) -> int:
    fails = 0
    cases: list[tuple[str, dict, int, str | None]] = []
    with Listener() as live:
        cases = [
            ("clean", {"live_port": live.port}, 0, "PREDICATE R76-C1 pass"),
            ("absent-undeclared", {"drop_marker": "absent-path"}, 1, "DEFECT UNDECLARED-ABSENT"),
            ("stale-absent", {"add_marker": "present-path"}, 1, "DEFECT STALE-ABSENT"),
            ("no-anchor", {"strip_anchor": "literature"}, 1, "DEFECT NOANCHOR"),
            ("stale-text", {"stale_text": True}, 1, "DEFECT STALE-TEXT"),
            ("malformed", {"malformed": True}, 1, "DEFECT MALFORMED"),
            ("printed-tally", {"drop_marker": "absent-path", "strip_anchor": "literature"}, 1,
             "AGREE agree=2 disagree=2"),
        ]
        for name, kwargs, want_rc, want_line in cases:
            d = work / f"c1_{name}"
            build_fixture(d, **kwargs)
            defects, report = census(d, Reader(d, "worktree"))
            rc = 0 if not defects else 1
            printed = "\n".join(report + defects + [f"PREDICATE R76-C1 {'pass' if rc == 0 else 'fail'}"])
            ok = rc == want_rc and (want_line is None or want_line in printed)
            fails += 0 if ok else 1
            print(f"SELFTEST {'ok' if ok else 'FAIL'} {name} rc={rc} want={want_rc}")
        shutil.rmtree(work / "c1_clean", ignore_errors=True)
        for name, *_ in cases:
            shutil.rmtree(work / f"c1_{name}", ignore_errors=True)
    print(f"SELFTEST cases={len(cases)} red={len(cases) - 1} failures={fails} ok={fails == 0}")
    return 0 if fails == 0 else 1


def mutants(work: Path) -> int:
    """Attributed kills: each mutant must die with its own expected defect id (R74-D4/R75-C2 class)."""
    total = killed = matched = wrong = survived = 0
    with Listener() as live:
        matrix = (
            ("M1-drop-marker", {"drop_marker": "absent-path"}, "UNDECLARED-ABSENT"),
            ("M2-add-marker", {"add_marker": "present-path"}, "STALE-ABSENT"),
            ("M3-strip-anchor", {"strip_anchor": "literature"}, "NOANCHOR"),
            ("M4-stale-text", {"stale_text": True}, "STALE-TEXT"),
            ("M5-malformed", {"malformed": True}, "MALFORMED"),
        )
        for name, kwargs, expected in matrix:
            total += 1
            d = work / f"c1m_{name}"
            build_fixture(d, live_port=live.port, **kwargs)
            defects, _ = census(d, Reader(d, "worktree"))
            hit = [x for x in defects if x.startswith(f"DEFECT {expected} ")]
            if defects:  # killed because the fixture is red at all
                killed += 1
            if hit:
                matched += 1
            elif defects:
                wrong += 1
            else:
                survived += 1
            print(f"MUTANT {name} killed={bool(defects)} expected={expected} matched={bool(hit)}")
            shutil.rmtree(d, ignore_errors=True)
    print(f"MUTANTS total={total} killed={killed} expected_matched={matched} wrong_id={wrong} survived={survived}")
    return 0 if killed == total and matched == total else 1


def control_declared(work: Path) -> int:
    """The cheapest skip: trust the row's own text instead of resolving the surface.

    A counter that reads the declaration scores the table as externally verified; this gate must
    still show the disagreement between what the rows claim and what the host answers.
    """
    root = work / "c1_control_declared"
    lane = Path(__file__).resolve().parent.parent
    rows = table_rows((lane / PROVINCE).read_text(errors="replace"))
    declared_disagree = 0
    for idx, (_lineno, cells) in enumerate(rows, start=1):
        if len(cells) < 3:
            continue
        kind, token = identity(cells[1])
        if kind == "prose":
            continue
        live, _ = resolve(kind, token, lane)
        claimed = "absent" if MARKER.search(" | ".join(cells)) else "present"
        if claimed != live:
            declared_disagree += 1
            print(f"CONTROL declared={claimed} live={live} {idx} {token}")
    print(f"CONTROL-SKIP rows={len(rows)} disagreements={declared_disagree} target_reached={not declared_disagree}")
    print(f"PREDICATE R76-C1-control {'pass' if declared_disagree else 'fail'}")
    shutil.rmtree(root, ignore_errors=True)
    return 0 if declared_disagree else 1


class _Tee:
    """stdout passthrough that also keeps the bytes for the receipt."""

    def __init__(self, *streams: object) -> None:
        self.streams = streams

    def write(self, data: str) -> int:
        for stream in self.streams:
            stream.write(data)  # type: ignore[attr-defined]
        return len(data)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()  # type: ignore[attr-defined]


def run_battery(args: argparse.Namespace, lane: Path, fn) -> int:
    buf = io.StringIO()
    with contextlib.redirect_stdout(_Tee(sys.stdout, buf)):
        rc = fn()
    if args.receipt is not None:
        tip, dirty = Reader(lane, "worktree").tip, worktree_dirty(lane)
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(
            f"LANE_TIP {tip}\nWORKTREE {'dirty' if dirty else 'clean'}\n" + buf.getvalue()
        )
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lane", type=Path, default=Path("."), help="Lane root directory")
    parser.add_argument("--rev", default="worktree", help="Read declared bytes at this revision")
    parser.add_argument("--receipt", type=Path, default=None, help="Write the verdict bytes here")
    parser.add_argument("--selftest", action="store_true", help="Run the fixture battery")
    parser.add_argument("--mutants", action="store_true", help="Run the attributed mutant matrix")
    parser.add_argument("--control-declared", action="store_true", help="Run the declaration-trusting control")
    parser.add_argument("--work", type=Path, default=Path("/fast/scratch/hyaku/kengaku-r76/c1"), help="Scratch dir")
    args = parser.parse_args()

    if args.selftest:
        args.work.mkdir(parents=True, exist_ok=True)
        return run_battery(args, args.lane, lambda: selftest(args.work))
    if args.mutants:
        args.work.mkdir(parents=True, exist_ok=True)
        return run_battery(args, args.lane, lambda: mutants(args.work))
    if args.control_declared:
        args.work.mkdir(parents=True, exist_ok=True)
        return run_battery(args, args.lane, lambda: control_declared(args.work))
    return emit(args.lane, args.rev, args.receipt)


if __name__ == "__main__":
    sys.exit(main())
