#!/usr/bin/env python3
"""log_appendonly.py — a committed log line is never rewritten (round 46).

Mined mistake (round-45 closure D1, `corpus/lessons/round-45-verifier-spotcheck.md` §1/§5 item 3): the closure's
`git diff -U0 fbad1c5 3d9ea54 -- LOG.md` shows two rewritten lines (`@@ -1374` heading and `@@ -1388` "A/B runs
byte-equal"). The per-commit walk attributes those deletions to `f660ae0`, the earlier commit in that range; it
also finds two different lines rewritten by `3d9ea54` itself (the `@@ -1407`–`@@ -1408` held-out tally). The lane's
own LOG.md recorded an earlier in-place rewrite (`LOG.md:9` cites `git diff 85b22e3 f147a27 -- LOG.md`, one
`-`/`+` pair). The stated rule — append a correction, never rewrite — had been enforced only by human diff review.

What is checked. For every commit reachable from HEAD that touches the log file, the commit's diff against its
first parent (merge commits compared to their mainline parent) is parsed hunk by hunk; every `-` line is a deletion
of a line that existed in the log before this commit, so it was committed earlier. A commit whose diff has only
`+` lines is a pure append and is fine. Line moves, whitespace-only edits and reorderings count: append-only means
never rewrite, so a moved line is still a rewritten line.

Output (oldest commit first), one line per offending commit and, under `--show-lines`, one line per deleted line:

    VIOLATION <sha12> <date> deleted=<n> at=<old-line[,old-line...]> first="<deleted text, <=72 chars>"
    DEL <sha12> :<old-line> -<deleted text, <=100 chars>
    LOG-APPENDONLY commits=<n> violations=<k>

`commits` counts the commits walked (log-touching commits in the bound range), `violations` the commits with at
least one deletion. Exit 0 iff `violations == 0`; 1 when it is > 0; 2 on a usage/setup error (no git, not a repo,
`--since` not an ancestor of HEAD).

Walk. `git log --full-history` — the same commits as plain `git log --format=%H -- LOG.md` plus every merge that
touches the file, which history simplification drops (at the round-46 base: 77 vs 76; the extra is the PR merge
`323b3921`, whose first-parent diff is 7 pure additions). `--verbose` prints that reconciliation on a `WALK` line.
Each commit is diffed against its first parent, so a merge's own conflict-resolution edit cannot hide.

`--since <rev>` binds the walk from a revision forward: only commits in `git log <rev>..HEAD` are inspected, so a
history already known to be clean before `<rev>` is not re-litigated. `<rev>` itself is not inspected (it is the
boundary, not an event); pass its parent to include it.

Read-only: no file in the repository is written, no index lock is taken (`GIT_OPTIONAL_LOCKS=0`), no commit or ref is
created. Diffs are read as text (`-a`) with no textconv and no rename detection, so a rewrite cannot hide behind a
binary guess, a rename or a filter. Subprocesses inherit `TMPDIR`; `--selftest` builds its fixture repos under a
`tempfile.mkdtemp()` honouring `TMPDIR`. Stdlib only.

Limits named: a commit that is not reachable from HEAD (an abandoned side branch) is not inspected; a log file that
did not exist in a commit's first parent has nothing to delete; `--since` trusts the caller that the earlier range
was clean.

Usage: python3 plans/log_appendonly.py [--lane DIR] [--path LOG.md] [--since REV] [--show-lines] [--verbose]
       python3 plans/log_appendonly.py --selftest
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def git(lane, *args, env=None):
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, env=env, text=True)


def resolve(lane, rev):
    r = git(lane, "rev-parse", "--verify", rev + "^{commit}")
    if r.returncode:
        return None
    return r.stdout.strip()


def commits_and_patch(lane, path, since, env):
    """One git process: patch stream with a NUL-prefixed commit header per commit."""
    rng = [f"{since}..HEAD"] if since else ["HEAD"]
    cmd = ["log", "--no-color", "--no-ext-diff", "--no-textconv", "--no-renames", "-a", "--unified=0",
           "--full-history", "--diff-merges=first-parent", "--date=short",
           "--format=%x00%H%x09%ad%x09%s", "-p", *rng, "--", path]
    r = git(lane, *cmd, env=env)
    if r.returncode:
        raise RuntimeError(r.stderr.strip() or f"git log exit {r.returncode}")
    return r.stdout


def simplified_walk(lane, path, since, env):
    rng = [f"{since}..HEAD"] if since else ["HEAD"]
    r = git(lane, "log", "--format=%H", *rng, "--", path, env=env)
    if r.returncode:
        raise RuntimeError(r.stderr.strip() or f"git log exit {r.returncode}")
    return r.stdout.split()


def parse(stream):
    """-> [(hash, date, subject, [(old_lineno, text), ...]), ...] oldest first."""
    commits = []
    cur = None
    old_no = 0
    in_hunk = False
    for line in stream.split("\n"):
        if line.startswith("\x00"):
            head = line[1:].split("\t", 2)
            cur = {"hash": head[0], "date": head[1] if len(head) > 1 else "",
                   "subject": head[2] if len(head) > 2 else "", "dels": []}
            commits.append(cur)
            in_hunk = False
            continue
        if cur is None:
            continue
        m = HUNK_RE.match(line)
        if m:
            old_no = int(m.group(1))
            in_hunk = True
            continue
        if not in_hunk:
            continue  # headers, blank separators and the next commit marker are not content
        if line.startswith("-"):
            cur["dels"].append((old_no, line[1:]))
            old_no += 1
        elif line.startswith(" "):
            old_no += 1
        elif line.startswith("+") or line.startswith("\\"):
            pass
        else:
            in_hunk = False
    commits.reverse()
    return commits


def check(lane, path="LOG.md", since=None, show_lines=False, verbose=False, out=print):
    env = dict(os.environ)
    env["TMPDIR"] = os.environ.get("TMPDIR") or tempfile.gettempdir()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env.pop("GIT_EXTERNAL_DIFF", None)
    since_sha = None
    if since:
        since_sha = resolve(lane, since)
        if since_sha is None:
            raise RuntimeError(f"--since {since}: not a commit")
        anc = git(lane, "merge-base", "--is-ancestor", since_sha, "HEAD", env=env)
        if anc.returncode != 0:
            raise RuntimeError(f"--since {since}: not an ancestor of HEAD")
    commits = parse(commits_and_patch(lane, path, since_sha, env))
    bad = [c for c in commits if c["dels"]]
    for c in bad:
        h = c["hash"][:12]
        first = c["dels"][0][1][:72]
        out(f'VIOLATION {h} {c["date"]} deleted={len(c["dels"])} '
            f'at={",".join(str(n) for n, _ in c["dels"])} first="{first}"')
        if show_lines:
            for n, text in c["dels"]:
                out(f"DEL {h} :{n} -{text[:100]}")
    if verbose:
        simpl = simplified_walk(lane, path, since_sha, env)
        walked = {c["hash"] for c in commits}
        extra = [h[:12] for h in simpl if h not in walked]
        missing = [h[:12] for h in walked if h not in set(simpl)]
        out(f'WALK full-history={len(walked)} simplified={len(simpl)} simplified_only={",".join(extra) or "-"}'
            f' full_only={",".join(missing) or "-"}')
    bound = f" since={since_sha[:12]}" if since_sha else ""
    out(f"LOG-APPENDONLY path={path} head={git(lane, 'rev-parse', '--short=12', 'HEAD', env=env).stdout.strip()}"
        f"{bound}")
    out(f"LOG-APPENDONLY commits={len(commits)} violations={len(bad)}")
    return (1 if bad else 0), {"commits": len(commits), "violations": len(bad), "bad": bad}


# --- selftest ------------------------------------------------------------------------------------------------
BASE = ["# fixture log", "", "- round 0: seeded."]
GITC = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid.example"]


def _commit(repo, body):
    (repo / "LOG.md").write_text("\n".join(body) + "\n")
    subprocess.run(["git", "-C", str(repo), *GITC, "add", "LOG.md"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), *GITC, "commit", "-q", "-m", body[-1][:60]], check=True,
                   capture_output=True)
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True, capture_output=True,
                          text=True).stdout.strip()


def _fixture(root, name):
    repo = root / name
    repo.mkdir()
    subprocess.run(["git", "-C", str(repo), "init", "-q", "-b", "main"], check=True, capture_output=True)
    top = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"], check=True,
                         capture_output=True, text=True).stdout.strip()
    assert pathlib.Path(top).resolve() == repo.resolve(), f"fixture toplevel {top} != {repo}"
    return repo


def selftest():
    ok_all = True
    with tempfile.TemporaryDirectory(prefix="log-appendonly-selftest-") as tmp:
        root = pathlib.Path(tmp)
        # GREEN: two commits, the second appends one line.
        repo = _fixture(root, "green")
        _commit(repo, BASE)
        _commit(repo, BASE + ["- round 1: appended."])
        # RED-EDIT: the second commit rewrites the seeded line.
        repo = _fixture(root, "red-edit")
        _commit(repo, BASE)
        _commit(repo, ["# fixture log", "", "- round 0: rewritten."])
        # RED-DELETE: the second commit drops a line, adds nothing.
        repo = _fixture(root, "red-delete")
        _commit(repo, BASE + ["- round 1: appended."])
        _commit(repo, ["# fixture log", "- round 1: appended."])
        # RED-MOVE: the same lines, reordered — a rewrite, not an append.
        repo = _fixture(root, "red-move")
        _commit(repo, BASE)
        _commit(repo, [BASE[1], BASE[0], BASE[2]])
        # SINCE: edit at c2, append at c3; binding from c2 must inspect c3 only (0), from c1 both (1).
        repo = _fixture(root, "since")
        c1 = _commit(repo, BASE)
        c2 = _commit(repo, ["# fixture log", "", "- round 0: rewritten."])
        _commit(repo, ["# fixture log", "", "- round 0: rewritten.", "- round 2: appended."])
        cases = (("GREEN", "green", None, 0, 2, 0),
                 ("RED-EDIT", "red-edit", None, 1, 2, 1),
                 ("RED-DELETE", "red-delete", None, 1, 2, 1),
                 ("RED-MOVE", "red-move", None, 1, 2, 1),
                 ("SINCE-FULL", "since", None, 1, 3, 1),
                 ("SINCE-C1", "since", c1, 1, 2, 1),
                 ("SINCE-C2", "since", c2, 0, 1, 0))
        for name, fx, since, want_rc, want_n, want_k in cases:
            argv = [sys.executable, os.path.abspath(__file__), "--lane", str(root / fx)]
            if since:
                argv += ["--since", since]
            r = subprocess.run(argv, capture_output=True, text=True)
            tail = [l for l in r.stdout.splitlines() if l.startswith("LOG-APPENDONLY commits=")]
            got = tail[-1] if tail else "<no summary>"
            want = f"commits={want_n} violations={want_k}"
            ok = r.returncode == want_rc and got.endswith(want)
            ok_all &= ok
            print(f"SELFTEST {name} rc={r.returncode} want_rc={want_rc} {'ok' if ok else 'FAIL'} :: {got}")
        # A --since that is not an ancestor of HEAD is a setup error, never a silent zero.
        green = root / "green"
        subprocess.run(["git", "-C", str(green), *GITC, "checkout", "-q", "-b", "side"], check=True,
                       capture_output=True)
        _commit(green, BASE + ["- side: appended."])
        subprocess.run(["git", "-C", str(green), *GITC, "checkout", "-q", "main"], check=True,
                       capture_output=True)
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--lane", str(green), "--since", "side"],
                           capture_output=True, text=True)
        ok = r.returncode == 2 and "not an ancestor of HEAD" in r.stderr
        ok_all &= ok
        print(f"SELFTEST BAD-SINCE rc={r.returncode} want_rc=2 {'ok' if ok else 'FAIL'} :: {r.stderr.strip()}")
    print(f"SELFTEST {'pass' if ok_all else 'fail'}")
    return 0 if ok_all else 1


def main():
    ap = argparse.ArgumentParser(description="report commits that rewrite a committed log line")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--path", default="LOG.md")
    ap.add_argument("--since", default=None, help="bind the walk to <rev>..HEAD")
    ap.add_argument("--show-lines", action="store_true")
    ap.add_argument("--verbose", action="store_true", help="print the walk reconciliation against plain git log")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    lane = pathlib.Path(a.lane).resolve()
    try:
        rc, _ = check(lane, a.path, a.since, a.show_lines, a.verbose)
    except (RuntimeError, OSError) as e:
        print(f"SETUP {e}", file=sys.stderr)
        return 2
    return rc


if __name__ == "__main__":
    sys.exit(main())
