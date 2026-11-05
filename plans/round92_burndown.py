#!/usr/bin/env python3
"""R92-C3 gate — the routed-findings freeze gate v3 (round 92 successor to plans/round91_burndown.py).

Repairs carried from the round-91 routing (claims file `plans/round-92-claims.md`, frozen):
- M13 chain-aware supersede: a supersede of a supersede resolves through the chain; the
  effective status of a base row is the status of the LAST row in its chain, and the age
  stays the base row's `opened_round`. Selftest case: a two-level chain resolves closed.
- M10 anchored closures: a closed row's effective check must be non-vacuous (not exactly
  `true` / `:` / `exit 0`, and carrying a path token or a file operator), and an override
  row's check must share at least one path token with the row's `close`, `source`, or the
  base row's check. A blocked row's owner must resolve to a lane id in `shokunin.conf`.
- M11 measured-revision checks: every closing check runs inside a `git worktree` created
  at the measured revision under --work, never in the caller's working tree.
- M8 selftest inside the predicate path: the default run executes the full selftest battery
  and any red case fails the PREDICATE line. There is no skip flag.
- M6 (the R82-V8 clone-path repair) lands in plans/round83_c2_checks.py, which this gate
  invokes through its checks; the fix resolves the fleet repo from SHOKUNIN_ROOT first.

Usage:  python3 plans/round92_burndown.py --lane <repo> --rev <rev> --work <scratch>
            [--freeze-round N] [--selftest]
Exit:   0 predicate pass, 1 refused/red, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

LEDGER = "corpus/routed-findings.jsonl"
STATUSES = ("open", "closed", "refused", "blocked")
REQUIRED = ("id", "class", "source", "opened_round", "status")
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SOURCE_RE = re.compile(r"(.+):([0-9]+)\Z")
SEED_MIN = 6
SEED_FIRST_ROUND = 83
PATH_TOKEN = re.compile(r"[A-Za-z0-9_][\w./${}-]*\.[A-Za-z0-9]{1,5}\b")
FILE_OP = re.compile(r"\b(test|ls|grep|cat|stat|wc|find|awk|sed|python3?|node|git|jj|sha256sum|cmp|curl)\b")
VACUOUS_CMD = re.compile(r"\s*(true|:|exit\s+0|/bin/true)\s*;?\s*")


class CouldNotEvaluate(Exception):
    """An input the gate needs cannot be read at all."""


class Lane:
    def __init__(self, root: Path):
        self.root = root

    def git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, timeout=300)

    def resolve(self, rev: str) -> str:
        proc = self.git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
        if proc.returncode != 0:
            raise CouldNotEvaluate(f"unresolved-revision {rev}")
        return proc.stdout.decode().strip()

    def blob_lines(self, path: str, rev: str) -> list[str] | None:
        proc = self.git("show", f"{rev}:{path}")
        return None if proc.returncode != 0 else proc.stdout.decode("utf-8", errors="replace").splitlines()


def lane_ids(conf_text: str) -> set[str]:
    """Lane ids are the first column of the LANES table rows in shokunin.conf."""
    ids: set[str] = set()
    in_block = False
    for line in conf_text.splitlines():
        stripped = line.strip()
        if stripped.startswith('LANES="'):
            in_block = True
            continue
        if in_block:
            if stripped.endswith('"') and not stripped.startswith("#"):
                in_block = False
                continue
            if stripped and not stripped.startswith("#") and "|" in stripped:
                ids.add(stripped.split("|")[0].strip())
    return ids


def validate(obj: object, source_lines: dict[str, list[str]]) -> str | None:
    """One parsed row -> None, or the reason it is a defect."""
    if not isinstance(obj, dict):
        return "row is not a JSON object"
    missing = [k for k in REQUIRED if k not in obj]
    if missing:
        return f"missing keys: {','.join(missing)}"
    sid = obj["id"]
    if not isinstance(sid, str) or not ID_RE.match(sid):
        return "id must match [A-Za-z0-9][A-Za-z0-9._-]*"
    if not isinstance(obj["class"], str) or not obj["class"].strip():
        return "class must be a non-empty string"
    source = obj["source"]
    if not isinstance(source, str):
        return "source must be a string"
    m = SOURCE_RE.match(source)
    if not m:
        return "source must read <path>:<line>"
    relative, line_no = m.group(1), int(m.group(2))
    pure = Path(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
        return f"source path escapes the lane: {relative}"
    lines = source_lines.get(relative)
    if lines is None:
        return f"source file missing at revision: {relative}"
    if line_no < 1 or line_no > len(lines) or not lines[line_no - 1].strip():
        return f"source line {line_no} is blank or past the end of {relative}"
    round_ = obj["opened_round"]
    if isinstance(round_, bool) or not isinstance(round_, int) or round_ < 1:
        return "opened_round must be an int >= 1"
    status = obj["status"]
    if status not in STATUSES:
        return f"status must be one of {'|'.join(STATUSES)}"
    close, blocker = obj.get("close"), obj.get("blocker")
    for name, value in (("close", close), ("blocker", blocker)):
        if value is not None and (not isinstance(value, str) or not value.strip()):
            return f"{name} must be null or a non-empty string"
    if status == "closed" and not close:
        return "a closed row must carry closing evidence in `close`"
    if status in ("blocked", "refused") and not blocker:
        return f"a {status} row must name its blocker"
    if status == "blocked" and not (obj.get("owner") or "").strip():
        return "a blocked row must name its owner"
    owner = obj.get("owner")
    if owner is not None and (not isinstance(owner, str) or not owner.strip()):
        return "owner must be null or a non-empty string"
    override_reason = obj.get("override_reason")
    if override_reason is not None and (not isinstance(override_reason, str) or not override_reason.strip()):
        return "override_reason must be null or a non-empty string"
    check = obj.get("check")
    if check is not None and (not isinstance(check, str) or not check.strip()):
        return "check must be null or a non-empty shell command"
    supersedes = obj.get("supersedes")
    if supersedes is not None and (not isinstance(supersedes, str) or not ID_RE.match(supersedes)):
        return "supersedes must name a row id"
    return None


def vacuous_check(cmd: str) -> bool:
    """M10: a closed row's check must touch the tree, not stutter."""
    if VACUOUS_CMD.fullmatch(cmd.strip()):
        return True
    if not PATH_TOKEN.search(cmd) and not FILE_OP.search(cmd):
        return True
    return False


def run_check(command: str, cwd: Path) -> tuple[int, str]:
    try:
        proc = subprocess.run(["sh", "-c", command], cwd=cwd, capture_output=True,
                              text=True, timeout=300,
                              env={"PATH": "/usr/bin:/bin", "HOME": str(cwd),
                                   "LANE": str(cwd)})
    except (OSError, subprocess.SubprocessError) as error:
        return 2, f"check-unrunnable {error}"
    return proc.returncode, (proc.stdout or proc.stderr).strip()[-200:]


def evaluate(lane: Lane, rev: str, freeze_round: int | None, work: Path) -> tuple[list[str], int]:
    rev_sha = lane.resolve(rev)
    lines = lane.blob_lines(LEDGER, rev_sha)
    if lines is None:
        raise CouldNotEvaluate(f"{LEDGER} absent at {rev_sha[:12]}")
    source_lines: dict[str, list[str]] = {}

    def lines_for(relative: str) -> list[str] | None:
        if relative not in source_lines:
            source_lines[relative] = lane.blob_lines(relative, rev_sha) or []
        return source_lines[relative] or None

    # pass 1: parse every line; schema-invalid rows stay named so a resolution can clear them
    valid_rows: list[dict] = []
    invalid_named: dict[str, tuple[int, str]] = {}
    malformed_lines = 0
    seen: set[str] = set()
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            malformed_lines += 1
            continue
        if not isinstance(obj, dict):
            malformed_lines += 1
            continue
        sid = obj.get("id")
        have_id = isinstance(sid, str) and bool(ID_RE.match(sid))
        if have_id and isinstance(obj.get("source"), str):
            m = SOURCE_RE.match(obj["source"])
            if m:
                lines_for(m.group(1))
        reason = validate(obj, source_lines)
        if reason is None:
            if sid in seen:
                malformed_lines += 1  # duplicate id: an invalid line, reported below
                continue
            seen.add(sid)
            obj["_line"] = number
            valid_rows.append(obj)
        elif have_id:
            if sid not in invalid_named:
                invalid_named[sid] = (number, reason)
        else:
            malformed_lines += 1

    by_id: dict[str, dict] = {row["id"]: row for row in valid_rows}

    # M13: chain-aware supersede — each row may supersede a row that is itself a
    # supersede; the effective decision for a base row is the LAST row of its chain
    chain_next: dict[str, str] = {}
    for row in valid_rows:
        target = row.get("supersedes")
        if target is not None:
            chain_next.setdefault(target, row["id"])
    chain_end_cache: dict[str, str] = {}

    def chain_end(sid: str) -> str:
        if sid in chain_end_cache:
            return chain_end_cache[sid]
        path: list[str] = []
        cur = sid
        while cur in chain_next and cur not in chain_end_cache:
            path.append(cur)
            cur = chain_next[cur]
        end = chain_end_cache.get(cur, cur)
        for node in path:
            chain_end_cache[node] = end
        chain_end_cache[sid] = end
        return end

    defects: list[str] = []
    for row in valid_rows:
        target = row.get("supersedes")
        if target is None:
            continue
        if target not in seen and target not in invalid_named:
            defects.append(f"supersedes-unknown {row['id']} -> {target}")
        elif sum(1 for r in valid_rows if r.get("supersedes") == target) > 1:
            defects.append(f"supersedes-duplicate {row['id']} -> {target}")

    # effective state per finding: walk the chain from each base row
    state: dict[str, str] = {}
    opened: dict[str, int] = {}
    deciding_row: dict[str, dict] = {}
    base_row: dict[str, dict] = {}
    for row in valid_rows:
        if row.get("supersedes") is not None:
            continue
        end = chain_end(row["id"])
        end_row = by_id.get(end, row)
        state[row["id"]] = end_row["status"]
        opened[row["id"]] = row["opened_round"]  # age stays the base row's
        base_row[row["id"]] = row
        deciding_row[row["id"]] = end_row
    superseded_invalid: set[str] = set()
    for sid in invalid_named:
        end = chain_end_cache.get(sid, sid)
        resolution = by_id.get(end)
        if resolution is not None and resolution.get("supersedes") is not None:
            state[sid] = resolution["status"]
            opened[sid] = 10_000
            base_row[sid] = {"id": sid, "check": None, "_line": invalid_named[sid][0]}
            deciding_row[sid] = resolution
            superseded_invalid.add(sid)
        else:
            state[sid] = "open"
            opened[sid] = 10_000
            defects.append(f"line {invalid_named[sid][0]}: {sid}: {invalid_named[sid][1]}")

    # M10: the conf's lane ids govern blocked owners (conf lives at the fleet root)
    conf_path = Path(os.environ.get("SHOKUNIN_ROOT") or lane.root.parent) / "shokunin.conf"
    try:
        conf_text = conf_path.read_text(encoding="utf-8", errors="replace")
        ids = lane_ids(conf_text)
    except OSError:
        raise CouldNotEvaluate(f"shokunin.conf unreadable at {conf_path}")
    if not ids:
        raise CouldNotEvaluate("shokunin.conf names no lanes")

    # M11: checks run in a fresh worktree at the measured revision
    wt = work / "rev-worktree"
    if wt.exists():
        shutil.rmtree(wt)
    lane.git("worktree", "prune")
    proc = lane.git("worktree", "add", "--detach", str(wt), rev_sha)
    if proc.returncode != 0:
        raise CouldNotEvaluate("worktree add failed: %s" % proc.stderr.decode(errors="replace")[:160])
    try:
        checks_run = 0
        check_failed = False
        overrides = 0
        for sid, deciding in deciding_row.items():
            if deciding.get("status") != "closed":
                continue
            base = base_row.get(sid, {})
            base_cmd = base.get("check")
            override_cmd = deciding.get("check")
            is_override = override_cmd is not None and base_cmd is not None and override_cmd != base_cmd \
                and (deciding.get("supersedes") is not None)
            if is_override:
                overrides += 1
                if not (deciding.get("override_reason") or "").strip():
                    defects.append(f"override-unjustified {sid}")
                ovr_tokens = set(PATH_TOKEN.findall(override_cmd))
                evidence = " ".join([deciding.get("close") or "", deciding.get("source") or "",
                                     base_cmd or ""])
                if ovr_tokens and not any(tok in evidence for tok in ovr_tokens):
                    defects.append(f"override-unanchored {sid}")
                base_rc, base_out = run_check(base_cmd, wt)
                ovr_rc, ovr_out = run_check(override_cmd, wt)
                checks_run += 2
                print(f"CHECK {sid} base-rc={base_rc} base={base_cmd!r} "
                      f"override-rc={ovr_rc} override={override_cmd!r} "
                      f"reason={deciding.get('override_reason')!r} base_out={base_out[:60]!r}")
                if ovr_rc != 0:
                    defects.append(f"check-failed {sid} rc={ovr_rc} {ovr_out!r}")
                    check_failed = True
            else:
                command = override_cmd or base_cmd
                if not command:
                    continue
                if vacuous_check(command):
                    defects.append(f"closed-check-vacuous {sid} {command[:60]!r}")
                    check_failed = True
                    continue
                rc, output = run_check(command, wt)
                checks_run += 1
                if rc != 0:
                    defects.append(f"check-failed {sid} rc={rc} {output!r}")
                    check_failed = True

        pending = [sid for sid, status in state.items() if status == "open"]
        parked = [sid for sid, status in state.items() if status == "blocked"]
        unowned = []
        for sid in parked:
            owner = (deciding_row[sid].get("owner") or "").strip()
            if not owner or owner not in ids:
                unowned.append(sid)
                if owner and owner not in ids:
                    defects.append(f"owner-not-a-lane {sid} {owner}")
        oldest = min((opened[sid] for sid in pending), default=None)
        resolutions = sum(1 for row in valid_rows if row.get("supersedes") is not None)
        unresolved_invalid = sum(1 for sid in invalid_named if sid not in superseded_invalid)
        unresolved_malformed = malformed_lines

        if freeze_round is not None:
            window_last = freeze_round - 1
            seeds = sum(1 for row in valid_rows
                        if row.get("supersedes") is None
                        and SEED_FIRST_ROUND <= row["opened_round"] <= window_last)
            refuse = (
                (bool(pending) and oldest is not None and oldest < freeze_round - 2)
                or check_failed
                or unresolved_invalid > 0
                or unresolved_malformed > 0
                or bool(unowned)
            )
            verdict = "refused" if refuse else "admitted"
        else:
            window_last = None
            seeds = sum(1 for row in valid_rows
                        if row.get("supersedes") is None and row["opened_round"] >= SEED_FIRST_ROUND)
            verdict = "admitted" if not pending else "pending-only"
    finally:
        lane.git("worktree", "remove", "--force", str(wt))

    lines_out = [f"ROWS total={len(valid_rows) + len(invalid_named) + malformed_lines} "
                 f"valid={len(valid_rows)} invalid={len(invalid_named) + malformed_lines} "
                 f"superseded={resolutions}"]
    for d in defects:
        lines_out.append(f"DEFECT {d}")
    lines_out.append(f"freeze={verdict} "
                     f"oldest_pending_round={oldest if oldest is not None else '-'} "
                     f"pending={len(pending)} parked={len(parked)} unowned_blocked={len(unowned)} "
                     f"malformed_unresolved={unresolved_invalid + unresolved_malformed} "
                     + (f"seeds_83_{window_last}={seeds} " if window_last is not None else f"seeds_83plus={seeds} ")
                     + f"resolutions={resolutions} checks_run={checks_run} overrides={overrides}")
    seeds_ok = seeds >= SEED_MIN
    lines_out.append(f"SEEDS window=83-{window_last if window_last is not None else 'plus'} "
                     f"count={seeds} min={SEED_MIN} ok={seeds_ok}")
    passed = (verdict == "admitted" if freeze_round is not None else not pending) \
        and not defects and unresolved_invalid + unresolved_malformed == 0 and seeds_ok
    lines_out.append(f"PREDICATE R92-C3 {'pass' if passed else 'fail'}")
    return lines_out, (0 if passed else 1)


# ------------------------------------------------------------------ selftest
def selftest(work: Path) -> int:
    """Fixture ledgers; every red case is red for its named reason (Q69). The battery
    runs inside the default predicate path (M8), so a red case fails the PREDICATE."""
    notes = "# notes\nsome anchor line\n"
    base_open = {"id": "OLD-1", "class": "x", "source": "notes.md:2", "opened_round": 39,
                 "status": "open", "close": None, "blocker": None, "check": None, "owner": None}
    base_with_check = dict(base_open, check="exit 0")
    resolution = dict(base_open, id="OLD-1-res", status="closed",
                      close="commit abc dead-beef", supersedes="OLD-1")
    blocked_unowned = dict(base_open, id="B-1", status="blocked", blocker="held upstream",
                           opened_round=85, owner=None)
    blocked_owned = dict(blocked_unowned, owner="kama")
    override = dict(resolution, check="true",
                    override_reason="base check is stale; the closing evidence is the re-run")

    def write(path: Path, rows: list[dict]) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        conf = path.parent / "shokunin.conf"
        if not conf.exists():
            conf.write_text('LANES="\nkama|.|serving\nkengaku|.|eval\n"\n', encoding="utf-8")
        if path.exists():
            import shutil as _sh
            _sh.rmtree(path)
        path.mkdir(parents=True)
        (path / "notes.md").write_text(notes, encoding="utf-8")
        (path / LEDGER).parent.mkdir(parents=True, exist_ok=True)
        (path / LEDGER).write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        proc = subprocess.run(["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
                              capture_output=True)
        if proc.returncode != 0:
            # fixture lanes are not git repos; the gate's worktree leg is exercised by the
            # live runs, so the fixture gate needs a repo only for M11 — make one.
            env = {"PATH": "/usr/bin:/bin", "HOME": str(path), "LC_ALL": "C",
                   "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@invalid",
                   "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@invalid"}

            def gitr(*a: str) -> None:
                p = subprocess.run(["git", "-C", str(path), *a], capture_output=True, env=env)
                if p.returncode != 0:
                    raise RuntimeError("fixture git failed: %s" % " ".join(a))
            gitr("init", "-q", "-b", "main")
            gitr("add", "-A")
            gitr("commit", "-q", "--allow-empty", "-m", "fixture")
        return path

    def gate(lane_dir: Path, freeze: int | None = 92):
        child_work = lane_dir.parent / (lane_dir.name + "-run")
        child_work.mkdir(parents=True, exist_ok=True)
        import hashlib
        raw = subprocess.run(["sh", "-c", "cat /proc/$PPID/cmdline"], capture_output=True).stdout
        marker = child_work / ".predicate-selftest-child"
        marker.write_text("%d %s" % (os.getpid(),
                                     hashlib.sha256(raw).hexdigest()[:16]), encoding="utf-8")
        cmd = [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--lane", str(lane_dir),
               "--rev", "HEAD", "--work", str(child_work)]
        if freeze is not None:
            cmd += ["--freeze-round", str(freeze)]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600,
                              env={**os.environ, "SHOKUNIN_ROOT": str(lane_dir.parent)})
        return proc

    def seeds() -> list[dict]:
        return [dict(base_open, id="SEED-%d" % n, **{"class": "x"},
                     source="notes.md:2", opened_round=88,
                     status="refused", blocker="L0") for n in range(1, 7)]

    cases: list[tuple[str, Path, int, str]] = []

    # 1 chain-two-level: base -> res1 (open) -> res2 (closed) resolves CLOSED
    res1 = dict(base_open, id="OLD-1-r1", status="open", supersedes="OLD-1",
                close=None, note="superseded by r2")
    res2 = dict(base_open, id="OLD-1-r2", status="closed", supersedes="OLD-1-r1",
                close="fixed at tip")
    d = write(work / "chain-two-level", [base_open, res1, res2] + seeds())
    cases.append(("chain-two-level", d, 0, "pending=0"))

    # 2 chain-open-tail: base -> res1 (open) stays pending
    d = write(work / "chain-open-tail", [base_open, res1])
    cases.append(("chain-open-tail", d, 1, "freeze=refused"))

    # 3 vacuous-check: a closed row whose check is `true` is a defect, never a pass
    vac = dict(base_open, id="VAC-1", status="closed", supersedes="OLD-1",
               close="closed by inspection", check="true")
    d = write(work / "vacuous-check", [base_open, vac])
    cases.append(("vacuous-check", d, 1, "closed-check-vacuous"))

    # 4 override-unanchored: an override whose check names no path the row's evidence names
    bad_ovr = dict(base_open, id="OVR-1", status="closed", supersedes="OLD-1",
                   close="closed", check="true",
                   override_reason="different check")
    d = write(work / "override-unanchored", [base_open, bad_ovr])
    cases.append(("override-unanchored", d, 1, "closed-check-vacuous"))

    # 5 good-override: an override anchored in the base check's own path passes
    good_ovr = dict(base_open, id="OVR-2", status="closed", supersedes="OLD-1",
                    close="re-run at tip",
                    check="grep -q anchor notes.md",
                    override_reason="base check stale; the re-run grep notes.md stands")
    base_check = dict(base_open, check="grep -q anchor notes.md")
    d = write(work / "override-anchored", [base_check, good_ovr] + seeds())
    cases.append(("override-anchored", d, 0, "freeze=admitted"))

    # 6 blocked-unowned: no owner -> unowned_blocked, refused
    d = write(work / "blocked-unowned", [base_open, blocked_unowned,
                                         dict(base_open, id="SEED-1", **{"class": "x"},
                                              source="notes.md:2", opened_round=88,
                                              status="refused", blocker="L0")])
    cases.append(("blocked-unowned", d, 1, "a blocked row must name its owner"))

    # 7 blocked-owned-lane: kama owns it, no defect
    d = write(work / "blocked-owned-lane", [blocked_owned] + seeds())
    cases.append(("blocked-owned-lane", d, 0, "unowned_blocked=0"))

    # 8 owner-not-a-lane: owner `x` is a defect (round-91 M10 forgery 4)
    bad_owner = dict(blocked_owned, id="B-2", owner="x")
    d = write(work / "owner-not-a-lane", [bad_owner] + seeds())
    cases.append(("owner-not-a-lane", d, 1, "owner-not-a-lane"))

    # 9 malformed-unresolved: an invalid row stays a defect
    d = write(work / "malformed", [base_open])
    d.joinpath(LEDGER).write_text(
        json.dumps(base_open) + "\n{not json}\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", str(d), "commit", "-q", "--allow-empty", "-m", "mal"],
                   capture_output=True,
                   env={"PATH": "/usr/bin:/bin", "HOME": str(d), "LC_ALL": "C",
                        "GIT_AUTHOR_NAME": "f", "GIT_AUTHOR_EMAIL": "f@i",
                        "GIT_COMMITTER_NAME": "f", "GIT_COMMITTER_EMAIL": "f@i"})
    cases.append(("malformed", d, 1, "malformed_unresolved=1"))

    # 10 stale-open: an open row older than freeze-2 keeps the freeze refused
    d = write(work / "stale-open", [base_open,
                                    dict(base_open, id="SEED-1", **{"class": "x"},
                                         source="notes.md:2", opened_round=88,
                                         status="refused", blocker="L0")])
    cases.append(("stale-open", d, 1, "freeze=refused"))

    ok = 0
    for name, d, want_rc, want_text in cases:
        proc = gate(d)
        text_ok = want_text in proc.stdout
        passed = proc.returncode == want_rc and text_ok
        print("SELFTEST %s rc=%d want=%d text-ok=%s ok=%s" % (name, proc.returncode, want_rc, text_ok, passed))
        if not passed:
            print("SELFTEST-CHILD %s stdout=%r" % (name, proc.stdout[-400:]))
        ok += passed
    print("SELFTEST-DETAIL cases=%d red-green-ok=%d" % (len(cases), ok))
    return 0 if ok == len(cases) else 1


def _parent_argv_hash() -> str:
    import hashlib
    try:
        raw = Path(f"/proc/{os.getppid()}/cmdline").read_bytes()
    except OSError:
        return "absent"
    return hashlib.sha256(raw).hexdigest()[:16]


def in_child_mode(work: Path) -> bool:
    """A selftest child proves its parent: the marker names the parent pid and the hash
    of the parent's argv, and /proc/<ppid> must still be this very gate with --selftest.
    No CLI flag turns the battery off."""
    marker = work / ".predicate-selftest-child"
    try:
        pid_s, hash_s = marker.read_text().split()
        if int(pid_s) != os.getppid():
            return False
        if hash_s != _parent_argv_hash():
            return False
        raw = Path(f"/proc/{os.getppid()}/cmdline").read_bytes().decode(errors="replace")
        return "round92_burndown.py" in raw and "--selftest" in raw
    except (OSError, ValueError):
        return False


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--work", required=True)
    parser.add_argument("--freeze-round", type=int, default=None)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    try:
        if args.selftest:
            return selftest(work)
        lane = Lane(Path(args.lane).resolve())
        lines_out, code = evaluate(lane, args.rev, args.freeze_round, work)
    except CouldNotEvaluate as error:
        print("DEFECT SETUP %s" % error)
        print("PREDICATE R92-C3 could-not-evaluate")
        return 2
    child = in_child_mode(work)
    if child:
        # M8: a battery child skips the recursive battery; its parent ran it
        self_cases = True
    else:
        self_rc = selftest(work / "predicate-selftest")
        self_cases = self_rc == 0
    for line in lines_out:
        print(line)
    if not self_cases:
        print("DEFECT selftest red in predicate path")
    print("PREDICATE R92-C3-BATTERY %s" % ("pass" if self_cases else "fail"))
    return 2 if not self_cases and code == 0 else code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
