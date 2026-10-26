#!/usr/bin/env python3
"""Order-of-operations gate: a frozen probe must not run before its receipt is committed.

Mined from round-38 closure R3 (`corpus/lessons/round-38-verifier-spotcheck.md` §5 item 3) and
`considerthese/2026-10-25.md` proposal 2(b) ("blocks pre-registration when a class recurs twice").
The class recurred: round 37 (`corpus/lessons/round-37.md:42`) and round 38
(`corpus/lessons/round-38.md:36`) each ran the C2 skip-control at freeze time; the skip-control's V2
step passes `--rerun` to the gate, whose `P10` clause executes the frozen probe, so the probe ran
before the first recorded run. Each round disclosed it in its claims header and the disclosure was
the only artefact. This gate reads git history and makes the ordering checkable.

The rule, over commits only (working tree and index are ignored):

  FAIL  when any file committed under `.ufo/waves/round-NN/claims/` at or before the first commit that
        adds <receipt> proves the probe executed — a gate `P10` line whose detail is anything other
        than `receipt unreadable`, or a receipt-shaped `CASE ... observed=` line;
  FAIL  when the freeze commit (the first commit adding <claims>) already contains <receipt>;
  FAIL  when <receipt> was committed before <claims> (pre-registration inverted: the receipt is an
        ancestor of the freeze commit, or both land in one commit — see the clause above).

Usage:
  python3 plans/order_check.py --lane . \\
      --claims plans/round-38-claims.md \\
      --receipt corpus/evidence/round38/build-pmars-probe.txt

Exit: 0 order holds · 1 order broken · 2 setup error (not a git work tree, claims or receipt never
committed, unparseable round number, bad arguments).

Read-only by construction: the only commands issued are `rev-parse`, `log`, `rev-list`, `ls-tree`,
`cat-file` and `merge-base --is-ancestor`. It writes nothing, touches no network, imports no probe,
gate or counter, and never runs the probe it polices.

Limits named:
  * Token heuristic: a claims/ file that merely *quotes* a forbidden line trips it (the rule is
    literal about what a committed file shows, not about who wrote it). The named false-negative
    side is a gate `P10` line broken across lines, or a probe run whose stdout was committed as a
    file whose name this gate does not read — it reads every blob under claims/, so only the
    pattern matters, not the file name.
  * Commit order is not authorship order: it polices what the history proves, not what happened in
    a scratch clone whose output was never committed (that is the loss the receipt commit repairs).
  * `--receipt` must be committed in HEAD; an uncommitted receipt is a setup error (2), not a pass.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

CLAIMS_NAME = re.compile(r"^round-(\d+)-claims\.md$")
# a gate output line, with or without the C2 counter's `gate: ` echo prefix
GATE_P10 = re.compile(r"^\s*P10\s+(DEFECT|ok)\b[ \t]*(.*)$")
# a probe receipt line (the probe's per-case verdict record)
CASE_LINE = re.compile(r"^\s*CASE\s+\S+.*\bobserved=[^\s]*")
# The one P10 detail the gate prints before executing anything, optionally echoing the receipt path
# (`receipt unreadable: <path>` is the shape P2 uses; P10 itself prints the bare sentence). Anything
# else -- `P10 ok …`, `fresh probe output is not byte-equal …`, `fresh probe exit=…` -- means the
# probe ran.
EXECUTED_EXCUSE = re.compile(r"^receipt unreadable(?:: \S+)?$")


class SetupError(Exception):
    """Anything that makes the question unanswerable: exit 2, never a silent pass."""


class Git:
    def __init__(self, root: Path):
        self.root = root

    def run(self, *args: str) -> subprocess.CompletedProcess:
        r = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True)
        if r.returncode != 0:
            raise SetupError(f"git {' '.join(args)} rc={r.returncode} {r.stderr.decode('utf-8', 'replace').strip()[:200]}")
        return r

    def out(self, *args: str) -> str:
        return self.run(*args).stdout.decode("utf-8", "replace")

    def rc(self, *args: str) -> int:
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True).returncode


def repo_path(root: Path, given: str) -> str:
    """Normalize a CLI path to a repo-relative posix path under <root>."""
    p = Path(given)
    p = (p if p.is_absolute() else (root / p))
    try:
        rel = p.resolve().relative_to(root)
    except ValueError:
        raise SetupError(f"path outside the lane: {given} (lane root {root})")
    return rel.as_posix()


def add_commit(git: Git, path: str) -> str:
    """The first commit (oldest) that adds `path`; empty when it was never added."""
    lines = git.out("log", "--reverse", "--diff-filter=A", "--format=%H", "--", path).split()
    return lines[0] if lines else ""


def blob_hits(text: str) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []
    for n, line in enumerate(text.splitlines(), 1):
        m = GATE_P10.match(line)
        if m:
            detail = m.group(2).strip()
            if not (m.group(1) == "DEFECT" and EXECUTED_EXCUSE.match(detail)):
                hits.append((n, "gate-p10", line.strip()))
            continue
        if CASE_LINE.match(line):
            hits.append((n, "case-observed", line.strip()))
    return hits


def scan_claims(git: Git, claims_dir: str, upto: str) -> tuple[int, int, list[tuple[str, str, int, str, str]]]:
    """Every blob ever committed under claims_dir up to and including `upto`; return hits."""
    commits = git.out("rev-list", "--reverse", upto, "--", claims_dir).split()
    first_seen: dict[str, tuple[str, str]] = {}
    files = 0
    for commit in commits:
        for entry in git.out("ls-tree", "-r", commit, "--", claims_dir).splitlines():
            if "\t" not in entry:
                continue
            meta, path = entry.split("\t", 1)
            parts = meta.split()
            if len(parts) != 3 or parts[1] != "blob":
                continue
            files += 1
            first_seen.setdefault(parts[2], (commit, path))
    hits: list[tuple[str, str, int, str, str]] = []
    for sha, (commit, path) in first_seen.items():
        blob = subprocess.run(["git", "-C", str(git.root), "cat-file", "blob", sha], capture_output=True)
        if blob.returncode != 0:
            raise SetupError(f"git cat-file blob {sha[:12]} rc={blob.returncode}")
        text = blob.stdout.decode("utf-8", "replace")
        for n, kind, line in blob_hits(text):
            hits.append((commit, path, n, kind, line))
    return len(commits), files, len(first_seen), hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="order-of-operations gate (frozen probe before its receipt)")
    ap.add_argument("--lane", required=True, help="lane (git work tree) to read; nothing is written")
    ap.add_argument("--claims", required=True, help="the round's frozen claims file, repo-relative")
    ap.add_argument("--receipt", required=True, help="the round's probe receipt, repo-relative")
    args = ap.parse_args(argv)

    try:
        lane = Path(args.lane).resolve()
        if not lane.is_dir():
            raise SetupError(f"not a directory: {args.lane}")
        top = subprocess.run(["git", "-C", str(lane), "rev-parse", "--show-toplevel"], capture_output=True)
        if top.returncode != 0:
            raise SetupError(f"not a git work tree: {args.lane}")
        root = Path(top.stdout.decode().strip())
        git = Git(root)

        claims = repo_path(root, args.claims)
        receipt = repo_path(root, args.receipt)
        m = CLAIMS_NAME.match(Path(claims).name)
        if not m:
            raise SetupError(f"claims file name is not round-NN-claims.md: {claims}")
        round_no = int(m.group(1))
        claims_dir = f".ufo/waves/round-{round_no}/claims"

        for label, path in (("claims", claims), ("receipt", receipt)):
            if git.rc("cat-file", "-e", f"HEAD:{path}") != 0:
                raise SetupError(f"{label} not committed in HEAD: {path}")

        freeze = add_commit(git, claims)
        if not freeze:
            raise SetupError(f"no commit adds the claims file: {claims}")
        receipt_commit = add_commit(git, receipt)
        if not receipt_commit:
            raise SetupError(f"no commit adds the receipt: {receipt}")

        print(f"ORDER claims={claims} round={round_no} freeze={freeze}")
        print(f"ORDER receipt={receipt} receipt_commit={receipt_commit} claims_dir={claims_dir}/")

        failures: list[str] = []

        # (1) the freeze commit must not already carry the receipt
        if git.rc("cat-file", "-e", f"{freeze}:{receipt}") == 0:
            print(f"ORDER FAIL freeze-contains-receipt {freeze} already has {receipt}")
            failures.append("freeze-contains-receipt")

        # (2) pre-registration order: the claims commit must not follow the receipt commit
        if freeze != receipt_commit and git.rc("merge-base", "--is-ancestor", receipt_commit, freeze) == 0:
            print(f"ORDER FAIL receipt-before-claims {receipt_commit} is an ancestor of {freeze}")
            failures.append("receipt-before-claims")

        # (3) no claims/ file committed at or before the receipt commit may show the probe executed
        commits, files, blobs, hits = scan_claims(git, claims_dir, receipt_commit)
        print(f"ORDER scanned commits={commits} file_entries={files} distinct_blobs={blobs}")
        for commit, path, n, kind, line in hits:
            print(f"ORDER HIT {path}@{commit[:12]}:{n} kind={kind} `{line[:120]}`")
        if hits:
            failures.append("probe-executed-before-receipt")

        if failures:
            print(f"ORDER FAIL {' '.join(failures)} hits={len(hits)}")
            print("ORDER RESULT FAIL")
            return 1
        print("ORDER ok no claims file committed at or before the receipt shows the frozen probe executed")
        print("ORDER RESULT PASS")
        return 0
    except SetupError as e:
        print(f"ORDER ERROR {e}", file=sys.stderr)
        print("ORDER RESULT ERROR")
        return 2


if __name__ == "__main__":
    sys.exit(main())
