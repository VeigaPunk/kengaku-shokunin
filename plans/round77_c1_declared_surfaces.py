#!/usr/bin/env python3
"""R77-C1 counter — one canonical declared-surface inventory carries every surface PROVINCE.md
declares, each resolved live, each declared verdict agreeing with the host.

Frozen before data on 2026-11-04 (L1 KengakuR77); see plans/round-77-claims.md §R77-C1.
Receipts are stamped with the measured revision and the worktree state (R74-D1/R75 discipline).

    python3 plans/round77_c1_declared_surfaces.py --lane .                    # verdict, worktree
    python3 plans/round77_c1_declared_surfaces.py --lane . --rev 07c97fcd     # declared bytes at rev
    python3 plans/round77_c1_declared_surfaces.py --selftest --work DIR        # fixture battery
    python3 plans/round77_c1_declared_surfaces.py --mutants --work DIR         # attributed mutant matrix
    python3 plans/round77_c1_declared_surfaces.py --control-declared --work DIR # the skip that must lose

Why this counter exists: the round-76 closure's own correction (`corpus/lessons/round-76.md`,
"Round-76 correction") recorded that the `## Surfaces` resolver reads one table while
`## Province map` → `### Core` and `### Historical` declare 21 further surfaces, and that the
repair is "an authoritative supersession of the older tables, not another row". This counter is
that supersession: one canonical table (`## Declared surfaces — canonical, machine-checked`) whose
rows name every surface the lane declares, resolve it live under one typed rule, and state which
older declaration they supersede. A surface declared by a superseded table and carried by no
canonical row is `UNLISTED-SURFACE`.

Canonical table columns (5 cells, no `|` inside a cell):
    | Surface | Kind | Anchor | Verdict | Supersedes |

Kinds and their resolution:
  path   every backticked path in the Anchor cell must exist (`test -e`; `~` expanded; `{a,b}`
         expanded; repo-relative tokens are tried at the lane root, then under `corpus/`).
  http   loopback endpoints only; verdict present for any non-000 status. A non-loopback URL is
         `remote` and needs a dated `REMOTE YYYY-MM-DD` marker instead of a probe (no egress).
  tcp    `host:port`; verdict present when a TCP connect succeeds.
  hash   a path plus `sha256=<first8>…<last6>` (or a full digest); verdict present only when the
         file exists *and* the recomputed digest matches, else `HASH-DRIFT`.
  count  a path plus `rows=<n>`; the row count is recomputed from that file (SOURCES census
         pattern), a mismatch is `COUNT-DRIFT`.
  cmd    a declared check command; every path/endpoint token inside it must resolve (no execution
         of declared commands — the lane refuses that command-execution surface).
  exec   an in-repo script plus `exit=<n>` and `receipt=<path>`; the receipt must exist, carry
         `exit <n>`, and stamp a `LANE_TIP <hex>` that is an ancestor of the measured revision.
         A missing/unstamped receipt is `EXEC-UNVERIFIED`.

Rows (each printed; every defect fails the predicate):
  SURFACE <n> <verdict> <kind> <target> <identity>
  SURFACES total=N present=P absent=A remote=R
  UNLISTED n=<count>                     declared by a superseded table, carried by no canonical row
  RESOLVED live=L                        rows whose verdict came from a live probe or receipt
  AGREE agree=N disagree=D
  DEFECT <class> <row> <detail>          UNLISTED-SURFACE, UNDECLARED-ABSENT, STALE-ABSENT,
                                         STALE-TEXT, UNDECLARED-REMOTE, HASH-DRIFT, COUNT-DRIFT,
                                         EXEC-UNVERIFIED, RECEIPT-STAMP, NOANCHOR, MALFORMED,
                                         MALFORMED-DATE, DUPLICATE-SURFACE, ESCAPE-ANCHOR,
                                         OVERFLOW-ANCHOR, CANONICAL-MISSING
Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import io
import re
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

PROVINCE = "PROVINCE.md"
CANONICAL = "## Declared surfaces"
FALLBACK = "## Surfaces"
SUPERSEDED = ("## Surfaces", "### Core", "### Historical")
CELLSPLIT = re.compile(r"(?<!\\)\|")
BACKTICK = re.compile(r"`([^`]+)`")
ENDPOINT = re.compile(r"^https?://[^\s`]+$")
TCP = re.compile(r"^([A-Za-z0-9_.-]+|\[[0-9a-fA-F:]+\]):(\d{1,5})$")
HOME_PATH = re.compile(r"^~/[^\s`]*$")
FILE_NAME = re.compile(r"^[A-Za-z0-9_.-]+\.(py|sh|md|json|jsonl|txt|adoc|log)$")
PATHISH = re.compile(r"^(?:~/|\./|corpus/|plans/|evidence/|/proc/|/tmp/|/home/|[A-Za-z0-9_.-]+/)")
SHA_PIN = re.compile(r"sha256=([0-9a-f]{8,64})(?:…|\.\.\.)?([0-9a-f]{0,6})")
COUNT_PIN = re.compile(r"rows=(\d+)")
EXIT_PIN = re.compile(r"exit=(\d+)")
RECEIPT_PIN = re.compile(r"receipt=([^\s`]+)")
TIMEOUT = 3
MAX_BRACE_TARGETS = 64
LOOPBACK_HOSTS = ("127.0.0.1", "localhost", "::1")
DATED_ABSENT = re.compile(r"ABSENT (\d{4}-\d{2}-\d{2})")
DATED_REMOTE = re.compile(r"REMOTE (\d{4}-\d{2}-\d{2})")
DECL_ABSENT = re.compile(r"\babsent\b", re.I)
DECL_PRESENT = re.compile(r"\bpresent\b", re.I)
STALE_TEXT = (
    "relocated intact",
    "all resolve at",
    "resolves today",
    "is alive",
    "LISTEN on",
    "still resolves",
    "identity re-probed",
    "re-probed each round",
    "all present",
)
CENSUS_ROW = re.compile(r"^\|[ \t]*S[0-9]{3,}[ \t]*\|")
LANE_TIP = re.compile(r"LANE_TIP ([0-9a-f]{7,40})")


# ---------------------------------------------------------------- revision reads
def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


class Reader:
    """Reads lane paths from the worktree or from a git revision (declared bytes)."""

    def __init__(self, lane: Path, rev: str) -> None:
        self.lane = lane
        self.rev = rev
        ref = "master^{commit}" if rev in ("worktree", "", None) else f"{rev}^{{commit}}"
        proc = git(lane, "rev-parse", "--verify", "--quiet", ref)
        self.tip = proc.stdout.strip() if proc.returncode == 0 and proc.stdout.strip() else "unknown"

    def get(self, rel: str) -> str:
        if self.rev in ("worktree", "", None):
            p = self.lane / rel
            return p.read_text(errors="replace") if p.exists() else ""
        proc = git(self.lane, "show", f"{self.rev}:{rel}")
        return proc.stdout if proc.returncode == 0 else ""

    def ids_file(self, rel: str) -> str:
        """File bytes used by count pins: worktree when the row is worktree-resolved."""
        return self.get(rel)


def worktree_dirty(lane: Path) -> bool:
    return bool(git(lane, "status", "--porcelain", "--untracked-files=no").stdout.strip())


def is_ancestor(lane: Path, commit: str, tip: str) -> str:
    """S252's three-state test: 'ancestor' | 'not-ancestor' | 'unresolved'."""
    obj = git(lane, "rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}")
    if obj.returncode != 0 or not obj.stdout.strip():
        return "unresolved"
    proc = git(lane, "merge-base", "--is-ancestor", commit, tip)
    if proc.returncode == 0:
        return "ancestor"
    if proc.returncode == 1:
        return "not-ancestor"
    return "unresolved"


# ---------------------------------------------------------------- parsing
def cells_of(line: str) -> list[str]:
    return [c.strip() for c in CELLSPLIT.split(line.strip())[1:-1]]


def table_rows(text: str, heading: str) -> list[tuple[int, list[str]]]:
    """(line number, cells) for the first markdown table under `heading`, until the next heading."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith(heading):
            start = i + 1
            break
    if start is None:
        return []
    rows: list[tuple[int, list[str]]] = []
    for i in range(start, len(lines)):
        line = lines[i]
        if line.startswith("#"):
            break
        if not line.startswith("|"):
            continue
        cells = cells_of(line)
        if not cells or all(set(c) <= {"-", ":", " "} for c in cells):
            continue
        if cells[0].strip().lower() in ("surface",):
            continue
        rows.append((i + 1, cells))
    return rows


def expand_braces(token: str) -> list[str]:
    m = re.search(r"\{([^{}]*)\}", token)
    if not m:
        return [token]
    out: list[str] = []
    for alt in m.group(1).split(","):
        out.extend(expand_braces(token[: m.start()] + alt + token[m.end():]))
    return out


def anchor_tokens(cell: str) -> list[str]:
    """Every path / endpoint / tcp / command token in a cell, in order."""
    toks: list[str] = []
    for span in BACKTICK.findall(cell):
        span = span.strip()
        if ENDPOINT.match(span) or TCP.match(span) or HOME_PATH.match(span):
            toks.append(span)
            continue
        if (PATHISH.match(span) or FILE_NAME.match(span)) and " " not in span:
            toks.append(span)
            continue
        for part in span.split():
            part = part.strip("'\"`,;()")
            if ENDPOINT.match(part) or TCP.match(part) or HOME_PATH.match(part):
                toks.append(part)
            elif (PATHISH.match(part) or FILE_NAME.match(part)) and len(part) > 2:
                toks.append(part)
    return toks


def first_anchor(cell: str) -> str:
    toks = anchor_tokens(cell)
    return toks[0] if toks else ""


def normalize_anchor(token: str) -> str:
    tok = token.strip().rstrip("/")
    if "{" in tok:
        tok = tok[: tok.index("{")].rstrip("/")
    return tok


def covers(canon: str, declared: str) -> bool:
    """A canonical anchor covers a superseded declaration on a path-segment boundary."""
    a, b = normalize_anchor(canon), normalize_anchor(declared)
    if not a or not b:
        return False
    variants = {(a, b)}
    if a.startswith("corpus/"):
        variants.add((a[len("corpus/"):], b))
    if b.startswith("corpus/"):
        variants.add((a, b[len("corpus/"):]))
    for x, y in variants:
        if x == y or y.startswith(x + "/") or x.startswith(y + "/"):
            return True
    return False


# ---------------------------------------------------------------- resolution
def endpoint_host(url: str) -> str:
    m = re.match(r"https?://([^/:?#]+)", url)
    return (m.group(1).lower() if m else "")


def http_status(url: str) -> tuple[str, str]:
    host = endpoint_host(url)
    if host not in LOOPBACK_HOSTS:
        return "remote", f"host={host or 'unparsed'}"
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:  # noqa: S310 - loopback only
            final = endpoint_host(resp.geturl())
            if final not in LOOPBACK_HOSTS:
                return "remote", f"redirect={final}"
            return "present", f"http={resp.status}"
    except urllib.error.HTTPError as exc:
        return "present", f"http={exc.code}"
    except (urllib.error.URLError, socket.timeout, ConnectionError, OSError):
        return "absent", "http=000"
    except (UnicodeEncodeError, ValueError) as exc:
        return "malformed", f"url={type(exc).__name__}"


def tcp_status(token: str) -> tuple[str, str]:
    m = TCP.match(token)
    if not m:
        return "malformed", f"token={token}"
    host, port = m.group(1).strip("[]"), int(m.group(2))
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT):
            return "present", f"tcp={host}:{port}"
    except OSError:
        return "absent", f"tcp={host}:{port}=closed"


def resolve_path(lane: Path, token: str) -> tuple[str, str]:
    if ".." in Path(token).parts:
        return "escape", f"path={token}"
    try:
        targets = expand_braces(token)
    except RecursionError:
        return "overflow", f"brace-depth={token[:40]}"
    if len(targets) > MAX_BRACE_TARGETS:
        return "overflow", f"brace-targets={len(targets)}"
    live: list[str] = []
    for t in targets:
        cand = Path(t).expanduser() if t.startswith("~/") or t.startswith("/") else lane / t
        if cand.exists():
            live.append(str(cand))
            continue
        if not t.startswith(("~", "/")) and (lane / "corpus" / t).exists():
            live.append(str(lane / "corpus" / t))
    verdict = "present" if len(live) == len(targets) else "absent"
    detail = f"path={live[0] if live else targets[0]}"
    if len(targets) > 1:
        detail += f" expanded={len(targets)} live={len(live)}"
    return verdict, detail


def blob_bytes(lane: Path, reader: Reader, token: str) -> bytes | None:
    if token.startswith(("~", "/")):
        cand = Path(token).expanduser()
        return cand.read_bytes() if cand.exists() else None
    if reader.rev not in ("worktree", "", None):
        proc = subprocess.run(["git", "-C", str(lane), "cat-file", "blob", f"{reader.rev}:{token}"],
                              capture_output=True)
        if proc.returncode == 0:
            return proc.stdout
        return None
    cand = lane / token
    return cand.read_bytes() if cand.exists() else None


def resolve_hash(lane: Path, token: str, pin: str, reader: Reader) -> tuple[str, str]:
    head, tail = pin.group(1), pin.group(2)
    blob = blob_bytes(lane, reader, token)
    if blob is None:
        return "absent", f"path={token}"
    digest = hashlib.sha256(blob).hexdigest()
    ok = digest.startswith(head[:8]) and (not tail or digest.endswith(tail))
    return ("present" if ok else "hashdrift"), f"sha256={digest[:8]}…{digest[-6:]} pin={head[:8]}…{tail or ''}"


def resolve_count(lane: Path, token: str, want: str, reader: Reader) -> tuple[str, str]:
    proc = git(lane, "show", f"{reader.rev}:{token}") if reader.rev not in ("worktree", "", None) else None
    if proc is not None and proc.returncode == 0:
        text = proc.stdout
    else:
        p = lane / token
        if not p.exists():
            return "absent", f"path={token}"
        text = p.read_text(errors="replace")
    n = sum(1 for line in text.splitlines() if CENSUS_ROW.match(line))
    return ("present" if n == int(want) else "countdrift"), f"rows={n} pin={want} path={token}"


def resolve_exec(lane: Path, token: str, cell: str, reader: Reader) -> tuple[str, str]:
    want = EXIT_PIN.search(cell)
    receipt = RECEIPT_PIN.search(cell)
    script = Path(token).expanduser() if token.startswith(("~/", "/")) else lane / token
    if not script.exists():
        return "absent", f"script={token}"
    if not want or not receipt:
        return "execunverified", f"script={token} pin=missing"
    rel = receipt.group(1)
    path = Path(rel).expanduser() if rel.startswith(("~/", "/")) else lane / rel
    if not path.exists():
        return "execunverified", f"receipt={rel} absent"
    text = path.read_text(errors="replace")
    if f"exit {want.group(1)}" not in text and f"rc={want.group(1)}" not in text:
        return "execunverified", f"receipt={rel} exit={want.group(1)} missing"
    m = LANE_TIP.search(text)
    if not m:
        return "execunverified", f"receipt={rel} unstamped"
    state = is_ancestor(lane, m.group(1), reader.tip)
    if state != "ancestor":
        return "execunverified", f"receipt={rel} tip={m.group(1)} {state}"
    return "present", f"receipt={rel} exit={want.group(1)} tip={m.group(1)[:8]}"


def resolve_row(lane: Path, kind: str, anchor_cell: str, verdict_cell: str,
                reader: Reader) -> tuple[str, str, str, list[str]]:
    """(verdict, identity, kind_reported, defects)."""
    defects: list[str] = []
    toks = anchor_tokens(anchor_cell)
    if not toks:
        return "noanchor", "no-anchor", kind, ["NOANCHOR"]
    cell = anchor_cell + " " + verdict_cell
    if kind == "http":
        verdicts, details = [], []
        for tok in toks:
            if not ENDPOINT.match(tok):
                defects.append("MALFORMED")
                continue
            v, d = http_status(tok)
            verdicts.append(v)
            details.append(d)
        if not verdicts:
            return "malformed", "no-endpoint", kind, defects or ["MALFORMED"]
        if all(v == "remote" for v in verdicts):
            return "remote", details[0], kind, defects
        verdict = "present" if all(v == "present" for v in verdicts) else (
            "absent" if all(v in ("present", "absent") for v in verdicts) else "malformed")
        return verdict, details[0], kind, defects
    if kind == "tcp":
        verdicts, details = [], []
        for tok in toks:
            v, d = tcp_status(tok)
            verdicts.append(v)
            details.append(d)
        verdict = "present" if all(v == "present" for v in verdicts) else (
            "absent" if all(v in ("present", "absent") for v in verdicts) else "malformed")
        return verdict, details[0], kind, defects
    if kind == "hash":
        pin = SHA_PIN.search(cell)
        if not pin:
            return "malformed", "no-pin", kind, ["MALFORMED"]
        return (*resolve_hash(lane, toks[0], pin, reader), kind, defects)
    if kind == "count":
        pin = COUNT_PIN.search(cell)
        if not pin:
            return "malformed", "no-pin", kind, ["MALFORMED"]
        return (*resolve_count(lane, toks[0], pin.group(1), reader), kind, defects)
    if kind == "exec":
        v, d = resolve_exec(lane, toks[0], cell, reader)
        return v, d, kind, defects
    if kind in ("path", "cmd", "remote"):
        if kind == "remote":
            return "remote", f"urls={len(toks)}", kind, defects
        verdicts, details = [], []
        for tok in toks:
            if ENDPOINT.match(tok):
                v, d = http_status(tok)
            elif TCP.match(tok):
                v, d = tcp_status(tok)
            else:
                v, d = resolve_path(lane, tok)
            if v in ("escape", "overflow", "malformed"):
                defects.append({"escape": "ESCAPE-ANCHOR", "overflow": "OVERFLOW-ANCHOR",
                                "malformed": "MALFORMED"}[v])
            verdicts.append(v)
            details.append(d)
        bad = [v for v in verdicts if v in ("escape", "overflow", "malformed")]
        if bad:
            return bad[0], details[0], kind, defects
        verdict = "present" if all(v == "present" for v in verdicts) else "absent"
        return verdict, details[0], kind, defects
    return "malformed", f"kind={kind}", kind, ["MALFORMED"]


# ---------------------------------------------------------------- census
def canonical_rows(reader: Reader) -> list[tuple[int, list[str]]]:
    return table_rows(reader.get(PROVINCE), CANONICAL)


def superseded_rows(reader: Reader) -> list[tuple[str, int, list[str]]]:
    text = reader.get(PROVINCE)
    out: list[tuple[str, int, list[str]]] = []
    for heading in SUPERSEDED:
        for lineno, cells in table_rows(text, heading):
            out.append((heading, lineno, cells))
    return out


def census(lane: Path, reader: Reader) -> tuple[list[str], list[str], dict[str, int]]:
    defects: list[str] = []
    report: list[str] = []
    rows = canonical_rows(reader)
    report.append(f"CANONICAL source={CANONICAL if rows else 'none'} rows={len(rows)}")
    if not rows:
        defects.append(f"DEFECT CANONICAL-MISSING 0 no `{CANONICAL}` inventory in {PROVINCE}")
    counts = {"present": 0, "absent": 0, "remote": 0}
    identities: set[str] = set()
    agree = disagree = live = 0
    for idx, (lineno, cells) in enumerate(rows, start=1):
        if len(cells) < 5:
            defects.append(f"DEFECT MALFORMED {lineno} cells={len(cells)}")
            disagree += 1
            continue
        name, kind, anchor, verdict_cell = cells[0], cells[1].strip().strip("*`").lower(), cells[2], cells[3]
        verdict, identity, kind, row_def = resolve_row(lane, kind, anchor, verdict_cell, reader)
        report.append(f"SURFACE {idx} {verdict} {kind} {name[:44]} {identity}")
        row_bad = False
        for d in row_def:
            defects.append(f"DEFECT {d} {lineno} {name[:40]}")
            row_bad = True
        counts[verdict] = counts.get(verdict, 0) + 1
        key = normalize_anchor(identity.split("=")[-1].split()[0]) if "=" in identity else identity
        identities.add(f"{kind}:{key}")
        if kind != "remote":
            live += 1
        joined = " ".join(cells)
        dated_absent = DATED_ABSENT.search(joined)
        dated_remote = DATED_REMOTE.search(joined)
        stale = [w for w in STALE_TEXT if w in joined.lower()]
        if verdict == "present":
            if dated_absent:
                defects.append(f"DEFECT STALE-ABSENT {lineno} {name[:40]} marker={dated_absent.group(1)}")
                row_bad = True
            elif declared_absent(verdict_cell):
                defects.append(f"DEFECT STALE-ABSENT {lineno} {name[:40]} declares absent")
                row_bad = True
        elif verdict == "absent":
            if not dated_absent:
                if declared_absent(verdict_cell):
                    defects.append(f"DEFECT UNDECLARED-ABSENT {lineno} {name[:40]}")
                else:
                    defects.append(f"DEFECT STALE-TEXT {lineno} {name[:40]}")
                row_bad = True
            elif declared_absent(verdict_cell) and stale:
                defects.append(f"DEFECT STALE-TEXT {lineno} {name[:40]} prose={stale[0]}")
                row_bad = True
        elif verdict in ("hashdrift", "countdrift", "execunverified"):
            label = {"hashdrift": "HASH-DRIFT", "countdrift": "COUNT-DRIFT",
                     "execunverified": "EXEC-UNVERIFIED"}[verdict]
            defects.append(f"DEFECT {label} {lineno} {name[:40]} {identity}")
            row_bad = True
        elif verdict == "remote":
            if not dated_remote:
                defects.append(f"DEFECT UNDECLARED-REMOTE {lineno} {name[:40]}")
                row_bad = True
        for m in DATED_ABSENT.finditer(joined):
            try:
                datetime.date.fromisoformat(m.group(1))
            except ValueError:
                defects.append(f"DEFECT MALFORMED-DATE {lineno} {name[:40]} {m.group(1)}")
                row_bad = True
        if row_bad:
            disagree += 1
        else:
            agree += 1

    canon_anchors: list[str] = []
    for _lineno, cells in rows:
        if len(cells) >= 3:
            canon_anchors.extend(anchor_tokens(cells[2]))
    unlisted = 0
    for heading, lineno, cells in superseded_rows(reader):
        anchor = ""
        for cell in [cells[0]] + list(cells[1:]):
            anchor = first_anchor(cell)
            if anchor:
                break
        if not anchor:
            continue
        if any(covers(c, anchor) for c in canon_anchors):
            continue
        unlisted += 1
        defects.append(f"DEFECT UNLISTED-SURFACE {lineno} {heading}: {anchor}")

    manifest = hashlib.sha256("\n".join(sorted(identities)).encode()).hexdigest()
    report.append(f"SURFACES total={len(rows)} present={counts.get('present', 0)} "
                  f"absent={counts.get('absent', 0)} remote={counts.get('remote', 0)}")
    report.append(f"UNLISTED n={unlisted}")
    report.append(f"RESOLVED live={live}")
    report.append(f"AGREE agree={agree} disagree={disagree}")
    report.append(f"DEFECTS n={len(defects)}")
    report.append(f"IDENTITIES n={len(identities)} unique={len(set(identities))} sha256={manifest[:16]}…")
    metrics = {"total": len(rows), "unlisted": unlisted, "live": live, "agree": agree,
               "disagree": disagree, "defects": len(defects), "present": counts.get("present", 0),
               "absent": counts.get("absent", 0), "remote": counts.get("remote", 0)}
    return defects, report, metrics


def declared_absent(cell: str) -> bool:
    return bool(DECL_ABSENT.search(cell)) and not DECL_PRESENT.search(cell)


TARGET = {"total": 28, "unlisted": 0, "live": 27, "agree": 28, "disagree": 0, "defects": 0}


def emit(lane: Path, rev: str, out: Path | None, expect_manifest: str = "") -> int:
    reader = Reader(lane, rev)
    defects, report, metrics = census(lane, reader)
    lines = [f"PROVINCE_REV {rev}", f"LANE_TIP {reader.tip}",
             f"WORKTREE {'dirty' if worktree_dirty(lane) else 'clean'}"]
    lines.extend(report)
    lines.extend(defects)
    ok = all(metrics.get(k) == v for k, v in TARGET.items()) and not any(
        d.startswith("DEFECT") for d in defects)
    if expect_manifest:
        m = re.search(r"sha256=([0-9a-f]+)…", "\n".join(report))
        if not m or not m.group(1).startswith(expect_manifest[:16]):
            lines.append(f"DEFECT MANIFEST-DRIFT expect={expect_manifest[:16]}")
            ok = False
    lines.append(f"TARGET total={TARGET['total']} unlisted={TARGET['unlisted']} "
                 f"live={TARGET['live']} agree={TARGET['agree']} disagree={TARGET['disagree']}")
    lines.append(f"PREDICATE R77-C1 {'pass' if ok else 'fail'}")
    text = "\n".join(lines) + "\n"
    sys.stdout.write(text)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    return 0 if ok else 1


# ---------------------------------------------------------------- batteries
def build_fixture(root: Path, *, drop_marker: str = "", stale_prose: str = "",
                  hash_pin: str = "", unlisted: bool = False, mode: str = "",
                  count_pin: str = "") -> Path:
    lane = root / "lane"
    (lane / "corpus" / "evidence").mkdir(parents=True, exist_ok=True)
    (lane / "corpus" / "knowledge").mkdir(parents=True, exist_ok=True)
    (lane / "corpus" / "SOURCES.md").write_text("| S001 | x |\n")
    (lane / "corpus" / "README.md").write_text("index\n")
    (lane / "corpus" / "QUALITY.md").write_text("quality\n")
    (lane / "corpus" / "evidence" / "demo").mkdir(exist_ok=True)
    (lane / "grader.py").write_text("print('ok')\n")
    digest = hashlib.sha256((lane / "grader.py").read_bytes()).hexdigest()
    pin = hash_pin or f"{digest[:8]}…{digest[-6:]}"
    marker = "" if drop_marker else "ABSENT 2026-11-01"
    prose = "relocated intact" if stale_prose else ""
    if mode == "absentdecl":
        accounting, marker, prose = "absent", "", ""
    elif mode == "absent-prose":
        accounting, prose = "absent", "relocated intact"
    elif mode == "stale-absent":
        accounting = "absent"
    else:
        accounting = "absent"
    canonical = [
        "## Declared surfaces — canonical, machine-checked",
        "",
        "| Surface | Kind | Anchor | Verdict | Supersedes |",
        "|---|---|---|---|---|",
        f"| Gate | hash | `grader.py` | present sha256={pin} | Surfaces:In-repo gate |",
        f"| Missing tree | path | `{'corpus/README.md' if mode == 'stale-absent' else '~/definitely-absent-r77'}` "
        f"| {accounting} {marker} {prose} | Surfaces:Research notes |",
        f"| Registry | count | `corpus/SOURCES.md` | present rows={count_pin or 1} | Core:Public-literature registry |",
        f"| Index | path | `corpus/README.md` | present | Surfaces:Corpus index |",
        f"| Quality | path | `corpus/QUALITY.md` | present | Core:Corpus gate docs |",
        f"| Evidence | path | `corpus/evidence/` | present | Core:Own probe artifacts |",
        f"| Loopback | tcp | `127.0.0.1:9` | {'absent ABSENT 2026-11-01' if mode != 'live-tcp' else 'present'} | Core:Live probe endpoint |",
    ]
    if unlisted:
        canonical = canonical[:-1]
    canonical += [
        "",
        "### Historical — absent, not governed",
        "",
        "| Surface | Anchor | Result |",
        "|---|---|---|",
        f"| Old evidence | `{'plans/other-tool.py' if unlisted else 'corpus/README.md'}` | absent |",
        "",
    ]
    (lane / "PROVINCE.md").write_text("\n".join(canonical))
    return lane


def run_lane(lane: Path, rev: str = "worktree"):
    reader = Reader(lane, rev)
    return census(lane, reader)


def selftest(work: Path) -> int:
    cases = [
        ("clean", {}, 0),
        ("hash-drift", {"hash_pin": "deadbeef…abcdef"}, 1),
        ("drop-marker", {"drop_marker": "1"}, 1),
        ("stale-prose", {"mode": "absent-prose"}, 1),
        ("unlisted", {"unlisted": True}, 1),
        ("stale-absent", {"mode": "stale-absent"}, 1),
    ]
    failures = 0
    lines: list[str] = []
    for name, kwargs, want in cases:
        root = work / f"case-{name}"
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        lane = build_fixture(root, **kwargs)
        defects, report, _metrics = run_lane(lane)
        got = 1 if any(d.startswith("DEFECT") for d in defects) else 0
        status = "ok" if got == want else "FAIL"
        if status == "FAIL":
            failures += 1
        lines.append(f"SELFTEST {status} {name} rc={got} want={want} defects={len(defects)}")
    lines.append(f"SELFTEST cases={len(cases)} red={len(cases) - 1} failures={failures}")
    print("\n".join(lines))
    return 0 if failures == 0 else 1


def mutants(work: Path) -> int:
    """Kill each mutant: the clean gate must print the expected class, the mutant must lose it."""
    src = Path(__file__).read_text()
    matrix = {
        "drop-unlisted": (
            lambda s: s.replace("    for heading, lineno, cells in superseded_rows(reader):",
                                "    for heading, lineno, cells in []:", 1),
            "UNLISTED-SURFACE", {"unlisted": True}),
        "skip-dated": (
            lambda s: s.replace("        elif verdict == \"absent\":\n            if not dated_absent:",
                                "        elif verdict == \"absent\":\n            if False:", 1),
            "UNDECLARED-ABSENT", {"drop_marker": "1"}),
        "skip-hash": (
            lambda s: s.replace("    ok = digest.startswith(head[:8])", "    ok = True  #", 1),
            "HASH-DRIFT", {"hash_pin": "deadbeef…abcdef"}),
        "skip-count": (
            lambda s: s.replace('    return ("present" if n == int(want) else "countdrift")',
                                '    return ("present" if True else "countdrift")', 1),
            "COUNT-DRIFT", {"count_pin": "2"}),
        "skip-stale": (
            lambda s: s.replace("        stale = [w for w in STALE_TEXT if w in joined.lower()]",
                                "        stale = []", 1),
            "STALE-TEXT", {"mode": "absent-prose"}),
        "trust-declared": (
            lambda s: s.replace("        verdict, identity, kind, row_def = resolve_row(lane, kind, anchor, verdict_cell, reader)",
                                "        verdict, identity, kind, row_def = ('present', 'declared', kind, [])", 1),
            "UNDECLARED-ABSENT", {"mode": "absentdecl"}),
    }
    survived = wrong = 0
    lines: list[str] = []
    for name, (mutate, expect, kwargs) in matrix.items():
        root = work / f"mut-{name}"
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        lane = build_fixture(root, **kwargs)
        clean = subprocess.run([sys.executable, str(Path(__file__)), "--lane", str(lane)],
                               capture_output=True, text=True).stdout
        script = work / f"mut-{name}.py"
        script.write_text(mutate(src))
        mutated = subprocess.run([sys.executable, str(script), "--lane", str(lane)],
                                 capture_output=True, text=True).stdout
        if expect not in clean:
            lines.append(f"MUTANT {name} NO-TRIGGER expected={expect}")
            wrong += 1
        elif expect in mutated:
            lines.append(f"MUTANT {name} SURVIVED expected={expect}")
            survived += 1
        else:
            lines.append(f"MUTANT {name} killed expected={expect}")
    lines.append(f"MUTANTS real={len(matrix)} expected_matched={len(matrix) - survived - wrong} "
                 f"wrong_id={wrong} survived={survived}")
    print("\n".join(lines))
    return 0 if survived == 0 and wrong == 0 else 1


def control_declared(work: Path, lane_arg: Path, rev: str) -> int:
    """The cheapest skip: accept each row's own verdict as if it had been resolved live."""
    root = work / "control-src"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    lane = build_fixture(root, drop_marker="", stale_prose="1", mode="stale-absent")
    reader = Reader(lane, "worktree")
    rows = canonical_rows(reader)
    declared = [cells[3] for _l, cells in rows if len(cells) >= 4]
    agree = sum(1 for d in declared if re.search(r"present|absent|remote", d, re.I))
    print("CONTROL-SKIP mode=declared-only")
    print(f"CONTROL rows={len(rows)} declared_verdicts={len(declared)} agree={agree} live=0 "
          f"target_reached=False")
    print(f"PREDICATE R77-C1-control {'pass' if len(rows) and agree == len(rows) else 'fail'}")
    return 0


class _Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)
        return len(data)

    def flush(self):
        for s in self.streams:
            s.flush()


def run_battery(args: argparse.Namespace, lane: Path, fn) -> int:
    work = args.work
    work.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    with contextlib_redirect(_Tee(sys.stdout, buf)):
        rc = fn()
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        reader = Reader(lane, args.rev)
        head = [f"LANE_TIP {reader.tip}", f"WORKTREE {'dirty' if worktree_dirty(lane) else 'clean'}",
                f"TOOL_SHA {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}"]
        args.receipt.write_text("\n".join(head) + "\n" + buf.getvalue())
    return rc


def contextlib_redirect(target):
    import contextlib
    return contextlib.redirect_stdout(target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", type=Path, default=Path("."), help="Lane root directory")
    parser.add_argument("--rev", default="worktree", help="Read declared bytes at this revision")
    parser.add_argument("--receipt", type=Path, default=None, help="Write the verdict bytes here")
    parser.add_argument("--expect-manifest", default="", help="Fail when the identity manifest differs")
    parser.add_argument("--selftest", action="store_true", help="Run the fixture battery")
    parser.add_argument("--mutants", action="store_true", help="Run the attributed mutant matrix")
    parser.add_argument("--control-declared", action="store_true", help="Run the declaration-trusting control")
    parser.add_argument("--work", type=Path, default=Path("/fast/scratch/hyaku/kengaku-r77/c1"),
                        help="Scratch dir")
    args = parser.parse_args()
    lane = args.lane.resolve()
    if not (lane / PROVINCE).exists():
        print(f"SETUP {PROVINCE} missing under {lane}")
        return 2
    if args.selftest:
        return run_battery(args, lane, lambda: selftest(args.work))
    if args.mutants:
        return run_battery(args, lane, lambda: mutants(args.work))
    if args.control_declared:
        return run_battery(args, lane, lambda: control_declared(args.work, lane, args.rev))
    return emit(lane, args.rev, args.receipt, args.expect_manifest)


if __name__ == "__main__":
    sys.exit(main())
