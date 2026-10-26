#!/usr/bin/env python3
"""Round-39 C2 probe: the pinned Terminal-Bench 2.0 `git-leak-recovery` grader, executed offline.

  python3 plans/git_leak_probe.py --lane .                run every frozen case, print the receipt
  python3 plans/git_leak_probe.py --lane . --dry          print the frozen case table only (no sandbox)
  python3 plans/git_leak_probe.py --lane . --stage-check  build every case's state (setup + recipe) in the
                                                          sandbox and print only the stage exit codes; the
                                                          grader is never imported

What runs: the captured grader `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88, digest checked before
any case), inside a bubblewrap sandbox per case: private network/pid/ipc namespaces, /usr and /etc
read-only, /tmp private, /app a fresh writable directory, /cap holding only the three captures the probe
executes (test_outputs.py, challenge-setup.sh, solve.sh), cwd /app, HOME=/tmp, GIT_CONFIG_NOSYSTEM=1 and
GIT_CONFIG_GLOBAL=/dev/null (no host git configuration reaches a case). Per case the sandbox first runs the
task's own `environment/challenge-setup.sh` in /app (as the task Dockerfile does at image build; skipped for
`empty-app` only), then the case recipe under `bash -euo pipefail`, then imports the grader and calls its five
test functions in file order: an AssertionError is `F`, any other exception is `F` with its class named, a
return is `P`. A case's verdict is `pass` iff all five are `P` (pytest exits 0 iff no test fails; tests/test.sh
writes reward 1 iff pytest exits 0). A setup or recipe that exits non-zero is a probe error (exit 2), never a
verdict.

Each case names the instruction requirements it violates (`violates=` tags, see TAGS), frozen with the
predictions; the entry's requirement map is derived from them and from the observed verdicts (round-38 Q28).

Predictions: written from a static reading of tests/test_outputs.py and instruction.md before the first
recorded run of this probe, EXCEPT the rows the round-38 wave-1 pilot already observed on this host with git
2.56.0 (`.ufo/waves/round-38/build/R38PlanNext.md` §2.3, controls A, B, C, D, G, H, and E/F as constructed
there): `untouched` (A), `oracle-solve-sh` (B), `echo-only` (C), `empty-app` (D), `echo-reflog-expire` (G),
`history-rebuilt` (H), `blob-ref-keeps-secret` (E), `tag-message-secret` (F) copy the pilot's verdicts. Where the
static reading disagrees with the pilot it is said in the case text (`oracle-solve-sh`: git fsck consults
reflogs by default, so the reset-away commit should not be `dangling` and solve.sh should find nothing; the
pilot observed the oracle pass).

Limits, stated before the first run: host git 2.56.0 and host bash stand in for the task image's Ubuntu 24.04
git and dash (the grader's checksum runs `sh -c`); the task image is never pulled; the setup runs as the probing
user, not root; commit object ids differ per run (wall-clock dates) and are never printed. This is a probe of
the grader on constructed end states, not of any agent.

Deterministic receipt: no temp path, object id, timing or host version is printed. Scratch lives under --work,
else $TMPDIR (tempfile default), and is removed on exit.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round39/tb2-git-leak-recovery"
PINS = {
    "test_outputs.py": "dc7b01c1b9dbb0c123def54b146dc1dd399a600edee5970d043a5db5eac4c775",
    "challenge-setup.sh": "a0a19652fc595b0bd06b6970e1d6a455bd4c50991c2ffdcc37fe5b66452b23e2",
    "solve.sh": "791a7eb23019ee7c93307b35cc77ea334469c4d3688e1171fe1e5ba6fd9a14dd",
}
BWRAP = "/usr/bin/bwrap"
GIT = "/usr/bin/git"
TESTS = ("test_flag_file_exists_and_correct", "test_no_secrets_in_commits", "test_good_commits_preserved",
         "test_no_secrets_in_unreachable_objects", "test_repository_contents_checksum")
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Instruction requirements (instruction.md line -> tag). A case violates a tag when its end state does not do
# what the instruction asks under that tag, whatever the grader says.
TAGS = {
    "recover-secret": "instruction.md:3",      # recover the secret and write it to /app/secret.txt
    "secret-gone": "instruction.md:4",         # it cannot be found anywhere in that repo
    "files-untouched": "instruction.md:5",     # irrelevant files remain untouched
    "messages-untouched": "instruction.md:5",  # commit messages remain untouched
}

SECRET = "secret[lost_and_found_in_git]"
FLAG = f"printf '%s\\n' '{SECRET}' > /app/secret.txt"
CLEAN = "git -C /app/repo reflog expire --expire=now --all && git -C /app/repo gc --prune=now -q"
INIT_MSG = "chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc"


@dataclasses.dataclass(frozen=True)
class Case:
    cid: str
    recipe: str                     # bash, run in /app after the setup
    predicted: str                  # five letters P/F in TESTS order
    violates: tuple                 # TAGS keys
    requirement: str
    setup: bool = True              # run challenge-setup.sh first


def r(*steps):
    return "\n".join(steps) + "\n"


CASES = [
    Case("empty-app", "true\n", "FFFFF", ("recover-secret", "files-untouched", "messages-untouched"),
         "do-nothing on an empty /app: no repo, no secret.txt (pilot D)", setup=False),
    Case("untouched", "true\n", "FPPPP", ("recover-secret", "secret-gone"),
         "do-nothing on the task's initial state: the secret commit is reset away but still in the reflog (pilot A)"),
    Case("oracle-solve-sh", "bash /cap/solve.sh\n", "PPPPP", (),
         "the task's own solution/solve.sh; static reading says fsck honours reflogs so nothing is dangling and "
         "secret.txt stays empty (FPPPP), the round-38 pilot observed pass (pilot B) - the pilot is followed"),
    Case("echo-only", r(FLAG), "PPPPP", ("secret-gone",),
         "write the literal only; the secret commit and blob stay in the object store (pilot C)"),
    Case("echo-reflog-expire", r(FLAG, "git -C /app/repo reflog expire --expire=now --all"), "PPPPP", ("secret-gone",),
         "literal + reflog expired, no gc: the commit is dangling, its tree and blob are not, cat-file -p of a "
         "commit prints no file content (pilot G)"),
    Case("echo-gc-only", r(FLAG, "git -C /app/repo gc --prune=now -q"), "PPPPP", ("secret-gone",),
         "literal + gc --prune=now without expiring the reflog: the reflog keeps the secret commit"),
    Case("clean-echo", r(CLEAN, FLAG), "PPPPP", (),
         "reflog expired, gc --prune=now, literal written: the cleanup the instruction asks for"),
    Case("dangling-secret-blob", r(CLEAN, FLAG, f"printf '%s\\n' '{SECRET}' | git -C /app/repo hash-object -w --stdin"),
         "PPPFP", ("secret-gone",), "after the cleanup a loose blob holding the secret is written: fsck lists it dangling"),
    Case("dangling-secret-commit", r(CLEAN, FLAG, "cd /app/repo",
                                     f"git commit-tree \"$(git rev-parse 'HEAD^{{tree}}')\" -p HEAD -m '{SECRET}'"),
         "PPPFP", ("secret-gone",), "after the cleanup an unreferenced commit whose message is the secret"),
    Case("branch-keeps-leak", r("cd /app/repo", "c=$(git rev-parse 'HEAD@{2}')",
                                "test \"$(git log -1 --format=%s \"$c\")\" = 'feat: add scratch notes'",
                                "git branch leak \"$c\"", CLEAN, FLAG),
         "PFPPP", ("secret-gone",), "the reset-away secret commit re-pointed by a branch before the cleanup: log --all -S sees it"),
    Case("blob-ref-keeps-secret", r(CLEAN, FLAG, "cd /app/repo",
                                    f"git update-ref refs/blobs/keep \"$(printf '%s\\n' '{SECRET}' | git hash-object -w --stdin)\""),
         "PPPPP", ("secret-gone",), "after the cleanup a non-branch ref pins a blob holding the secret (pilot E shape)"),
    Case("tag-message-secret", r(CLEAN, FLAG, f"git -C /app/repo tag -a keep -m '{SECRET}' HEAD"), "PPPPP",
         ("secret-gone",), "after the cleanup an annotated tag whose message is the secret (pilot F shape)"),
    Case("commit-message-secret", r(CLEAN, FLAG, f"git -C /app/repo commit -q --allow-empty -m '{SECRET}'"), "PFPPP",
         ("secret-gone",), "after the cleanup a reachable empty commit whose message is the secret: --grep sees it"),
    Case("notes-secret", r(CLEAN, FLAG, f"git -C /app/repo notes add -m '{SECRET}' HEAD"), "PFPPP", ("secret-gone",),
         "after the cleanup a git note carrying the secret: refs/notes/commits is under --all and its commit adds the note blob"),
    Case("stash-secret", r(CLEAN, FLAG, "cd /app/repo", f"printf '%s\\n' '{SECRET}' >> README.md", "git stash -q"),
         "PPPPP", ("secret-gone",),
         "after the cleanup the secret appended to README.md and stashed: refs/stash is a merge commit, and log -p -S "
         "without -m is not expected to diff merges (static reading, uncertain)"),
    Case("dotfile-in-worktree", r(CLEAN, FLAG, f"printf '%s\\n' '{SECRET}' > /app/repo/.leak"), "PPPPP",
         ("secret-gone",), "after the cleanup a dot file holding the secret in the work tree: the checksum skips dot paths"),
    Case("untracked-file-secret", r(CLEAN, FLAG, f"printf '%s\\n' '{SECRET}' > /app/repo/notes.txt"), "PPPPF",
         ("secret-gone",), "after the cleanup a non-dot untracked file holding the secret: the checksum sees a new file"),
    Case("config-secret", r(CLEAN, FLAG, f"git -C /app/repo config kengaku.note '{SECRET}'"), "PPPPP", ("secret-gone",),
         "after the cleanup the secret stored in .git/config: no test reads repository configuration"),
    Case("readme-edited", r(CLEAN, FLAG, "printf 'edited\\n' >> /app/repo/README.md"), "PPPPF", ("files-untouched",),
         "cleanup + literal + an irrelevant file edited in the work tree"),
    Case("message-rewritten", r("git -C /app/repo commit -q --amend -m 'chore: tidy'", CLEAN, FLAG), "PPPPP",
         ("messages-untouched",),
         "the tip commit's message rewritten before the cleanup; the first commit carries the same init message"),
    Case("history-rebuilt", r("cd /app/repo", "rm -rf .git", "git init -q", "git config user.name TerminalBench",
                              "git config user.email tb@example.com", "git add README.md", f"git commit -q -m '{INIT_MSG}'",
                              FLAG),
         "PPPPP", ("messages-untouched",), "history discarded and rebuilt as one init commit (pilot H)"),
    Case("flag-extra-text", r(CLEAN, f"printf 'flag: %s\\n' '{SECRET}' > /app/secret.txt"), "FPPPP", ("recover-secret",),
         "cleanup + secret.txt carrying a label before the literal"),
    Case("flag-padded-crlf", r(CLEAN, f"printf '  %s\\r\\n' '{SECRET}' > /app/secret.txt"), "PPPPP", (),
         "cleanup + the literal with leading spaces and CRLF: strip() removes both"),
    Case("flag-is-directory", r(CLEAN, "mkdir /app/secret.txt"), "FPPPP", ("recover-secret",),
         "cleanup + /app/secret.txt is a directory: exists() holds, read_text raises IsADirectoryError"),
    Case("flag-in-repo-only", r(CLEAN, f"printf '%s\\n' '{SECRET}' > /app/repo/secret.txt"), "FPPPF",
         ("recover-secret", "secret-gone"), "cleanup + the literal written into the repo work tree instead of /app"),
]

HARNESS_PY = r'''
import importlib.util, subprocess, sys
mode, setup = sys.argv[1], sys.argv[2] == "1"
def stage(label, argv):
    rc = subprocess.run(argv, cwd="/app", stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL).returncode
    print("STAGE " + label + " rc=" + str(rc))
    return rc
if setup and stage("setup", ["bash", "/cap/challenge-setup.sh"]):
    sys.exit(3)
if stage("recipe", ["bash", "-euo", "pipefail", "/recipe.sh"]):
    sys.exit(3)
if mode == "stage":
    sys.exit(0)
spec = importlib.util.spec_from_file_location("tb2_git_leak_grader", "/cap/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name in %r:
    try:
        getattr(mod, name)()
        print("TEST " + name + " P")
    except AssertionError:
        print("TEST " + name + " F")
    except Exception as e:
        print("TEST " + name + " F error=" + type(e).__name__)
''' % (TESTS,)


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sandbox_argv(cap, work):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--bind", str(work / "app"), "/app", "--dir", "/cap"]
    for name in sorted(PINS):
        argv += ["--ro-bind", str(cap / name), f"/cap/{name}"]
    argv += ["--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
             "--ro-bind", str(work / "harness.py"), "/harness.py", "--chdir", "/app"]
    return argv


def run_case(cap, root, case, mode):
    work = pathlib.Path(tempfile.mkdtemp(prefix="glr-", dir=root))
    try:
        (work / "app").mkdir()
        (work / "recipe.sh").write_text(case.recipe)
        (work / "harness.py").write_text(HARNESS_PY)
        env = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
               "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
        p = subprocess.run(sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py", mode,
                                                      "1" if case.setup else "0"],
                           env=env, capture_output=True, text=True, timeout=300)
        return p.returncode, p.stdout
    finally:
        shutil.rmtree(work, ignore_errors=True)


def overall(letters):
    return "pass" if letters == "P" * len(TESTS) else "fail"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    mx = ap.add_mutually_exclusive_group()
    mx.add_argument("--dry", action="store_true")
    mx.add_argument("--stage-check", action="store_true")
    ap.add_argument("--work", default=None, help="scratch parent (default: $TMPDIR via tempfile)")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    cap = lane / CAP
    ids = [c.cid for c in CASES]
    if len(set(ids)) != len(ids) or any(t not in TAGS for c in CASES for t in c.violates) \
            or any(len(c.predicted) != len(TESTS) or set(c.predicted) - {"P", "F"} for c in CASES):
        print("SETUP duplicate case id, unknown tag or malformed prediction", file=sys.stderr)
        return 2
    if a.dry:
        for t, loc in TAGS.items():
            print(f"TAG {t} {loc}")
        for c in CASES:
            print(f"CASE {c.cid} predicted={overall(c.predicted)} tests={c.predicted}"
                  f" violates={','.join(c.violates)} -- {c.requirement}")
        print(f"cases={len(CASES)} predicted_pass={sum(overall(c.predicted) == 'pass' for c in CASES)}"
              f" predicted_fail={sum(overall(c.predicted) == 'fail' for c in CASES)}")
        return 0
    for name, digest in PINS.items():
        if not (cap / name).is_file() or sha256(cap / name) != digest:
            print(f"SETUP capture {name} missing or not at its pinned digest", file=sys.stderr)
            return 2
    for tool in (BWRAP, GIT):
        if not os.access(tool, os.X_OK):
            print(f"SETUP {tool} is required", file=sys.stderr)
            return 2
    root = pathlib.Path(tempfile.mkdtemp(prefix="k39-glr-", dir=a.work))
    try:
        if a.stage_check:
            bad = 0
            for c in CASES:
                rc, out = run_case(cap, root, c, "stage")
                stages = " ".join(l.split(" ", 1)[1] for l in out.splitlines() if l.startswith("STAGE "))
                bad += rc != 0
                print(f"STAGECHECK {c.cid} rc={rc} {stages}")
            print(f"stagecheck cases={len(CASES)} failed={bad}")
            return 0 if bad == 0 else 1
        print("# tb2 git-leak-recovery grader probe (kengaku round 39) @ terminal-bench-2 2fd12b88")
        for name in sorted(PINS):
            print(f"# capture {name} sha256={PINS[name]}")
        npass = nfail = mism = 0
        for c in CASES:
            rc, out = run_case(cap, root, c, "grade")
            got = {}
            for l in out.splitlines():
                parts = l.split()
                if len(parts) >= 3 and parts[0] == "TEST" and parts[1] in TESTS:
                    got[parts[1]] = (parts[2], parts[3] if len(parts) > 3 else "")
            if rc != 0 or set(got) != set(TESTS):
                print(f"SETUP case {c.cid} did not yield five test verdicts (rc={rc})", file=sys.stderr)
                print(out, file=sys.stderr)
                return 2
            letters = "".join(got[t][0] for t in TESTS)
            errs = ",".join(f"{t}:{got[t][1]}" for t in TESTS if got[t][1])
            obs = overall(letters)
            npass += obs == "pass"
            nfail += obs == "fail"
            match = letters == c.predicted
            mism += not match
            print(f"CASE {c.cid} predicted={overall(c.predicted)} observed={obs} tests={letters}"
                  f" predicted_tests={c.predicted} match={'yes' if match else 'NO'}"
                  f" violates={','.join(c.violates)}{' ' + errs if errs else ''} -- {c.requirement}")
        print(f"cases={len(CASES)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
