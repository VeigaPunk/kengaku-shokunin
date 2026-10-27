#!/usr/bin/env python3
"""R45SentFenceDesign: enumerate git-config / repo-layout vectors that can make a fence read or trust
outside the fixture directory d, beyond the frozen f1-f10 refusal modules.

Every scenario builds a fixture d = WORK/<id>/fx/f000 and a side tree WORK/<id>/fx/side (outside d,
inside the build scratch, exactly the counter's "outside d" region), then runs the git probes a fence
would run under strace -f -y and records successful / attempted opens outside d.

No writes outside WORK/OUT/LOGS (all under S=/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign).
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign")
WORK, OUT, LOGS = S / "work", S / "out", S / "logs"
BASE_ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/nonexistent",
            "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
GIT_PINS = {
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "4",
    "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
    "GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
    "GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false",
}
PIN_ENV = {**BASE_ENV, **GIT_PINS}
BUILD_ENV = {**PIN_ENV, "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "f@invalid",
             "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "f@invalid"}
STRACE = "/usr/bin/strace"
OPEN_RE = re.compile(r"\bopen(?:at|at2)?\(|creat\(")
DONE_RE = re.compile(r"=\s+(-?\d+|E[A-Z]+)(?:<(.+)>)?\s*$")
ARG_RE = re.compile(r'"(/[^"]*)"')
EXEC_RE = re.compile(r'execve\("([^"]+)"')


def sh(argv, cwd=None, env=None):
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, env=env or BUILD_ENV, capture_output=True,
                          text=True, timeout=120)


def git(repo, *args, check=True):
    r = sh(["git", "-C", str(repo), *args])
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} in {repo} failed: {r.stderr[-300:]}")
    return r.stdout


def fresh(sid):
    base = WORK / sid
    if base.exists():
        shutil.rmtree(base)
    d = base / "fx" / "f000"
    side = base / "fx" / "side"
    d.mkdir(parents=True)
    side.mkdir(parents=True)
    return d, side


def repo(path):
    path.mkdir(parents=True, exist_ok=True)
    r = sh(["git", "init", "-q", "-b", "master", str(path)], cwd=path.parent)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return path


def commit(repo_path, files, msg="c"):
    for rel, text in files.items():
        p = pathlib.Path(repo_path) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    git(repo_path, "add", "-A")
    git(repo_path, "commit", "-qm", msg)


def trace(sid, label, argv, cwd, env, timeout=25):
    """Run argv under strace; classify opens relative to d (WORK/<sid>/fx/f000)."""
    d = (WORK / sid / "fx" / "f000").resolve()
    scratch = (WORK / sid / "fx").resolve()
    log = LOGS / f"{sid}--{label}.log"
    cmd = [STRACE, "-f", "-qq", "-y", "-e", "trace=open,openat,openat2,creat,execve", "-o", str(log), *argv]
    try:
        r = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True, text=True, timeout=timeout,
                           stdin=subprocess.DEVNULL)
        rc, out, err = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = "TIMEOUT", "", ""
    inside, outside, attempts, execs = 0, [], [], []
    if log.exists():
        for line in log.read_text(errors="replace").splitlines():
            em = EXEC_RE.search(line)
            if em:
                p = pathlib.Path(em.group(1))
                if any(p.is_relative_to(s) for s in (scratch,)) and not p.is_relative_to(d):
                    execs.append(str(p))
                continue
            if not OPEN_RE.search(line):
                continue
            done = DONE_RE.search(line)
            args = ARG_RE.findall(line.split(" = ")[0])
            arg = pathlib.Path(args[0]) if args else None
            resolved = None
            ok = False
            if done:
                ok = not done.group(1).startswith(("E", "-"))
                resolved = pathlib.Path(done.group(2)) if done.group(2) else None
            p = resolved or arg
            if p is None:
                continue
            p = pathlib.Path(os.path.normpath(str(p)))
            if any(p == s or p.is_relative_to(s) for s in (scratch,)) and not (p == d or p.is_relative_to(d)):
                if ok:
                    outside.append(str(p))
                else:
                    attempts.append(str(p))
            elif p == d or p.is_relative_to(d):
                if ok:
                    inside += 1
    return {"probe": label, "argv": argv if isinstance(argv, list) else str(argv), "rc": rc,
            "stdout": (out or "").strip()[:220], "stderr": (err or "").strip()[-160:],
            "inside_opens": inside, "outside_opens": len(outside), "outside_paths": sorted(set(outside))[:4],
            "outside_attempts": sorted(set(attempts))[:4], "outside_execs": sorted(set(execs))[:4]}


def run(sid, probes):
    return [trace(sid, label, argv, cwd, env) for (label, argv, cwd, env) in probes]


RESULTS = {}


def record(sid, question, rows, note=""):
    RESULTS[sid] = {"question": question, "probes": rows, "note": note}
    tag = "PARSE" if any(r["outside_opens"] or r["outside_execs"] for r in rows) else "no-outside-open"
    print(f"{sid:26s} {tag:16s} " + " | ".join(
        f"{r['probe']}:rc={r['rc']},out={r['outside_opens']},att={len(r['outside_attempts'])}"
        f"{',exec=' + str(len(r['outside_execs'])) if r['outside_execs'] else ''} :: {r['stdout'][:60]}"
        for r in rows), flush=True)


# ---------------------------------------------------------------- scenarios

def s_worktree_relative():
    sid = "02_worktree_relative"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    (side / "wt").mkdir(parents=True, exist_ok=True)
    sh(["git", "-C", str(lane), "config", "core.worktree", "../side/wt"])
    rows = run(sid, [("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV)])
    record(sid, "core.worktree relative escapes d (r44 leg reads --local --no-includes)", rows)


def s_inc_gitdir_true():
    sid = "03_inc_gitdir_true"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    (side / "inc.cfg").write_text("[user]\n\temail = OUTSIDE@invalid\n")
    with open(lane / ".git" / "config", "a") as f:
        f.write(f'[includeIf "gitdir:{lane.resolve()}/"]\n\tpath = {side / "inc.cfg"}\n')
    rows = run(sid, [
        ("config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
        ("no-includes-getregexp", ["git", "-C", str(lane), "config", "--local", "--no-includes",
                                   "--get-regexp", "^include(if)?\\."], d, PIN_ENV),
    ])
    record(sid, "includeIf gitdir:<match> + outside path: does git parse it?", rows)


def s_inc_gitdir_false():
    sid = "04_inc_gitdir_false"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    git(lane, "config", "user.email", "local@invalid")
    (side / "inc.cfg").write_text("[user]\n\temail = OUTSIDE@invalid\n")
    with open(lane / ".git" / "config", "a") as f:
        f.write(f'[includeIf "gitdir:/nonexistent/zzz/"]\n\tpath = {side / "inc.cfg"}\n')
    rows = run(sid, [
        ("config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
        ("log-oneline", ["git", "-C", str(lane), "log", "--oneline", "-1"], d, PIN_ENV),
    ])
    record(sid, "includeIf gitdir:<non-match>: parsed but not applied (text scan still must refuse)", rows)


def s_inc_onbranch():
    sid = "05_inc_onbranch"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    git(lane, "config", "user.email", "local@invalid")
    (side / "inc.cfg").write_text("[user]\n\temail = OUTSIDE@invalid\n")
    with open(lane / ".git" / "config", "a") as f:
        f.write(f'[includeIf "onbranch:master"]\n\tpath = {side / "inc.cfg"}\n')
    rows = run(sid, [
        ("config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
        ("status-porcelain", ["git", "-C", str(lane), "status", "--porcelain"], d, PIN_ENV),
        ("log-oneline", ["git", "-C", str(lane), "log", "--oneline", "-1"], d, PIN_ENV),
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
    ])
    record(sid, "includeIf onbranch:<HEAD branch> + outside path: which git commands apply it?", rows)


def s_inc_tilde():
    sid = "06_inc_tilde"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    git(lane, "config", "user.email", "local@invalid")
    (side / "inc-tilde.cfg").write_text("[user]\n\temail = TILDE-OUTSIDE@invalid\n")
    with open(lane / ".git" / "config", "a") as f:
        f.write("[include]\n\tpath = ~/inc-tilde.cfg\n")
    home = WORK / sid / "fakehome"
    home.mkdir(exist_ok=True)
    (home / "inc-tilde.cfg").write_text("[user]\n\temail = TILDE-OUTSIDE@invalid\n")
    env_home = {**PIN_ENV, "HOME": str(home)}
    rows = run(sid, [
        ("config-user-email-HOME-nonexistent", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
        ("config-user-email-HOME-writable", ["git", "-C", str(lane), "config", "--get", "user.email"], d, env_home),
    ])
    record(sid, "include.path = ~/... : tilde expands to HOME (outside d)", rows,
           note="fence env in round45_c1_verify.run_fence sets HOME=/nonexistent")


def s_inc_envvar():
    sid = "07_inc_envvar"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    git(lane, "config", "user.email", "local@invalid")
    with open(lane / ".git" / "config", "a") as f:
        f.write("[include]\n\tpath = $HOME/inc-env.cfg\n[include]\n\tpath = ${HOME}/inc-env2.cfg\n")
    home = WORK / sid / "fakehome"
    home.mkdir(exist_ok=True)
    (home / "inc-env.cfg").write_text("[user]\n\temail = ENV-OUTSIDE@invalid\n")
    (home / "inc-env2.cfg").write_text("[user]\n\temail = ENV2-OUTSIDE@invalid\n")
    env_home = {**PIN_ENV, "HOME": str(home)}
    rows = run(sid, [("config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, env_home),
                     ("config-get-all-include", ["git", "-C", str(lane), "config", "--get-all", "include.path"], d, env_home)])
    record(sid, "include.path = $HOME/... : git treats env syntax literally (no expansion)?", rows)


def s_attr_excludes():
    sid = "08_attributes_excludes"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    (side / "attrs").write_text("*.txt filter=outside-filter\n")
    (side / "ign").write_text("a.txt\n")
    sh(["git", "-C", str(lane), "config", "core.attributesFile", str(side / "attrs")])
    sh(["git", "-C", str(lane), "config", "core.excludesFile", str(side / "ign")])
    rows = run(sid, [
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
        ("config-getregexp-core", ["git", "-C", str(lane), "config", "--local", "--no-includes",
                                   "--get-regexp", "^core\\.", ], d, PIN_ENV),
        ("check-attr", ["git", "-C", str(lane), "check-attr", "-a", "--", "a.txt"], d, PIN_ENV),
        ("status-porcelain", ["git", "-C", str(lane), "status", "--porcelain"], d, PIN_ENV),
        ("ls-files-others", ["git", "-C", str(lane), "ls-files", "-o", "--exclude-standard"], d, PIN_ENV),
    ])
    record(sid, "core.attributesFile / core.excludesFile outside d: which commands parse?", rows)


def s_hooks_fsmonitor():
    sid = "09_hooks_fsmonitor"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    hooks = side / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    for h in ("post-checkout", "post-index-change", "post-merge", "pre-commit"):
        p = hooks / h
        p.write_text(f"#!/bin/sh\necho RAN >> {side / 'HOOK-RAN'}\n")
        p.chmod(0o755)
    fs = side / "fsmon.sh"
    fs.write_text(f"#!/bin/sh\necho RAN >> {side / 'FSM-RAN'}\nexit 0\n")
    fs.chmod(0o755)
    sh(["git", "-C", str(lane), "config", "core.hooksPath", str(hooks)])
    sh(["git", "-C", str(lane), "config", "core.fsmonitor", str(fs)])
    rows = run(sid, [
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
        ("status-porcelain-pinned", ["git", "-C", str(lane), "status", "--porcelain"], d, PIN_ENV),
        ("status-porcelain-nopins", ["git", "-C", str(lane), "status", "--porcelain"], d, BASE_ENV),
        ("update-index-refresh-nopins", ["git", "-C", str(lane), "update-index", "-q", "--refresh"], d, BASE_ENV),
        ("log-oneline-nopins", ["git", "-C", str(lane), "log", "--oneline", "-1"], d, BASE_ENV),
    ])
    markers = {n: (side / n).exists() for n in ("HOOK-RAN", "FSM-RAN")}
    record(sid, "core.hooksPath / core.fsmonitor outside d: executed by which commands, under which env?", rows,
           note=f"markers={markers} (core.fsmonitor/core.hooksPath are env-pinned by r44 GIT_PINS)")


def s_mailmap():
    sid = "10_mailmap"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    (side / "mailmap").write_text("Mapped <outside@invalid> <f@invalid>\n")
    sh(["git", "-C", str(lane), "config", "mailmap.file", str(side / "mailmap")])
    rows = run(sid, [
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
        ("log-usemailmap", ["git", "-C", str(lane), "log", "--use-mailmap", "--format=%ae", "-1"], d, PIN_ENV),
        ("shortlog", ["git", "-C", str(lane), "shortlog", "-sne", "HEAD"], d, PIN_ENV),
    ])
    record(sid, "mailmap.file outside d: which commands parse?", rows)


def s_submodule():
    sid = "11_submodule_absurl"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"s.txt": "sub\n"})
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n", ".gitmodules":
                  f'[submodule "x"]\n\tpath = x\n\turl = file://{store.resolve()}\n'})
    rows = run(sid, [
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
        ("submodule-status", ["git", "-C", str(lane), "submodule", "status"], d, PIN_ENV),
        ("submodule-update-init", ["git", "-C", str(lane), "submodule", "update", "--init", "--quiet"], d, PIN_ENV),
    ])
    record(sid, "submodule url = file://<outside>: parsed by which commands, does init read outside?", rows)


def s_alt_relative():
    sid = "12_alternates_relative"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"only-in-store.txt": "BORROWED\n"})
    blob = git(store, "rev-parse", "HEAD:only-in-store.txt").strip()
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    objdir = store / ".git" / "objects"
    (lane / ".git" / "objects" / "info").mkdir(parents=True, exist_ok=True)
    rel = os.path.relpath(objdir, (lane / ".git" / "objects" / "info").resolve())
    (lane / ".git" / "objects" / "info" / "alternates").write_text(rel + "\n")
    rows = run(sid, [
        ("cat-file-borrowed", ["git", "-C", str(lane), "cat-file", "-t", blob], d, PIN_ENV),
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
    ])
    record(sid, f"objects/info/alternates RELATIVE ({rel}) to an outside store: git reads it?", rows)


def s_commondir_relative():
    sid = "13_commondir_relative"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"only-in-store.txt": "BORROWED\n"})
    blob = git(store, "rev-parse", "HEAD:only-in-store.txt").strip()
    lane = d / "lane"
    gd = lane / ".git"
    gd.mkdir(parents=True)
    (gd / "commondir").write_text("../../side/store/.git\n")
    (gd / "HEAD").write_text("ref: refs/heads/master\n")
    rows = run(sid, [
        ("git-common-dir", ["git", "-C", str(lane), "rev-parse", "--git-common-dir"], d, PIN_ENV),
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
        ("cat-file-borrowed", ["git", "-C", str(lane), "cat-file", "-t", blob], d, PIN_ENV),
        ("config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
    ])
    record(sid, "commondir RELATIVE to an outside store: git resolves it and reads outside?", rows)


def s_worktrees_meta():
    sid = "14_worktrees_meta"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    git(lane, "config", "user.email", "local@invalid")
    outside_wt = side / "wt"
    outside_wt.mkdir(parents=True, exist_ok=True)
    meta = lane / ".git" / "worktrees" / "wt"
    meta.mkdir(parents=True)
    (meta / "gitdir").write_text(str(outside_wt / ".git") + "\n")
    (meta / "HEAD").write_text("ref: refs/heads/master\n")
    (side / "inc.cfg").write_text("[user]\n\temail = WT-OUTSIDE@invalid\n")
    (meta / "config.worktree").write_text(f"[include]\n\tpath = {side / 'inc.cfg'}\n")
    sh(["git", "-C", str(lane), "config", "extensions.worktreeConfig", "true"])
    (outside_wt / ".git").write_text(f"gitdir: {meta}\n")
    rows = run(sid, [
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
        ("worktree-list", ["git", "-C", str(lane), "worktree", "list"], d, PIN_ENV),
        ("config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
        ("config-user-email-in-outside-wt", ["git", "-C", str(outside_wt), "config", "--get", "user.email"], outside_wt, PIN_ENV),
        ("rev-parse-in-outside-wt", ["git", "-C", str(outside_wt), "rev-parse", "--show-toplevel"], outside_wt, PIN_ENV),
    ])
    record(sid, ".git/worktrees/<n>/ metadata (gitdir outside + config.worktree include): parsed by which commands?", rows)


def s_env_gitdir():
    sid = "15_env_gitdir"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"a.txt": "x\n"})
    (d / "lane").mkdir()
    env_git = {**PIN_ENV, "GIT_DIR": str(store / ".git")}
    rows = run(sid, [
        ("rev-parse-with-GIT_DIR", ["git", "-C", str(d / "lane"), "rev-parse", "--show-toplevel"], d, env_git),
        ("rev-parse-no-env", ["git", "-C", str(d / "lane"), "rev-parse", "--show-toplevel"], d, PIN_ENV),
    ])
    record(sid, "GIT_DIR in env redirects discovery outside d (fixture cannot set fence env)", rows,
           note="round45_c1_verify.run_fence passes a literal env of 5 keys; no GIT_* passthrough")


def s_gitfile_variants():
    sid = "16_gitfile_variants"
    d, side = fresh(sid)
    grams = {"relative": "gitdir: ../side/gitdir",
             "spacing": "gitdir : ../side/gitdir",
             "nospace": "gitdir:../side/gitdir",
             "upper": "GITDIR: ../side/gitdir",
             "leading-nl": "\ngitdir: ../side/gitdir",
             "trailing-space": "gitdir: ../side/gitdir   "}
    rows = []
    for name, text in grams.items():
        fdir = WORK / sid / "fx" / name
        fdir.mkdir(parents=True, exist_ok=True)
        gd = side / f"gitdir-{name}"
        gd.mkdir(exist_ok=True)
        g = sh(["git", "init", "-q", "-b", "master", "--separate-git-dir", str(gd), str(fdir / "lane")])
        # replace whatever git wrote with the variant
        (fdir / "lane" / ".git").write_text(text + "\n")
        rows.append(trace(sid, f"variant-{name}", ["git", "-C", str(fdir / "lane"), "rev-parse",
                                                   "--absolute-git-dir"], fdir, PIN_ENV))
    record(sid, "`.git` FILE variants (relative target, spacing, case): which does git accept?", rows)


def s_dotgit_symlink():
    sid = "17_dotgit_symlink"
    d, side = fresh(sid)
    gd = side / "gitdir"
    gd.mkdir(parents=True, exist_ok=True)
    lane = d / "lane"
    lane.mkdir()
    (d / "lane" / "a.txt").write_text("x\n")
    sh(["git", "init", "-q", "-b", "master", "--separate-git-dir", str(gd), str(lane)])
    (lane / "a.txt").write_text("x\n")
    commit(lane, {"a.txt": "x\n"})
    # convert: remove the gitdir: file, use a symlink instead
    (lane / ".git").unlink(missing_ok=True)
    os.symlink(gd, lane / ".git")
    rows = run(sid, [
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
        ("rev-parse-absolute-git-dir", ["git", "-C", str(lane), "rev-parse", "--absolute-git-dir"], d, PIN_ENV),
        ("config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
    ])
    record(sid, "`.git` as SYMLINK to an outside git dir: does git follow it?", rows)


def s_symlink_store_config():
    sid = "18_symlink_store_config"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    store = repo(side / "store")
    commit(store, {"only.txt": "BORROWED\n"})
    blob = git(store, "rev-parse", "HEAD:only.txt").strip()
    (side / "cfg-hard").write_text("[user]\n\temail = SYMLINK-CFG-OUTSIDE@invalid\n")
    (lane / ".git" / "config").unlink()
    os.symlink(side / "cfg-hard", lane / ".git" / "config")
    (lane / ".git" / "objects" / "info").mkdir(parents=True, exist_ok=True)
    (lane / ".git" / "objects" / "info" / "alternates").unlink(missing_ok=True)
    os.symlink(store / ".git" / "objects", lane / ".git" / "objlink")
    rows = run(sid, [
        ("config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
        ("cat-file-via-objlink", ["git", "-C", str(lane), "cat-file", "-t", blob], d, PIN_ENV),
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
    ])
    record(sid, "symlinked `.git/config` and `.git/objects`-like store link to outside d", rows)


def s_hardlink():
    sid = "19_hardlink_objects"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"only.txt": "BORROWED-BY-INODE\n"})
    blob = git(store, "rev-parse", "HEAD:only.txt").strip()
    tree = git(store, "rev-parse", "HEAD^{tree}").strip()
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    for h in (blob, tree):
        src = store / ".git" / "objects" / h[:2] / h[2:]
        dst = lane / ".git" / "objects" / h[:2] / h[2:]
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            dst.unlink()
        os.link(src, dst)
    (side / "cfg-hard").write_text("[user]\n\temail = HARDLINK-CFG-OUTSIDE@invalid\n")
    (lane / ".git" / "config").unlink()
    os.link(side / "cfg-hard", lane / ".git" / "config")
    st = os.stat(lane / ".git" / "config")
    st_o = os.stat(side / "store" / ".git" / "objects" / blob[:2] / blob[2:])
    rows = run(sid, [
        ("cat-file-hardlinked", ["git", "-C", str(lane), "cat-file", "-t", blob], d, PIN_ENV),
        ("config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
    ])
    record(sid, "HARDLINKED objects/config: content authored outside d, path inside d", rows,
           note=f"nlink(config)={st.st_nlink} nlink(object)={st_o.st_nlink}; inode-shared with outside file")


def s_case_variants():
    sid = "20_case_variants"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    git(lane, "config", "user.email", "local@invalid")
    (side / "inc1.cfg").write_text("[user]\n\temail = CASE-OUTSIDE@invalid\n")
    cfgt = (lane / ".git" / "config").read_text()
    cfgt += f'[Include]\n\tpath = {side / "inc1.cfg"}\n'
    (lane / ".git" / "config").write_text(cfgt)
    rows = run(sid, [
        ("config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
    ])
    text = (lane / ".git" / "config").read_text()
    lint = {"case_sensitive_[include": bool(re.search(r"\[include", text)),
            "case_insensitive_[include": bool(re.search(r"\[include", text, re.I)),
            "case_sensitive_include.path": bool(re.search(r"include\.path|include\.PATH", text)),
            "case_insensitive_include.PATH": bool(re.search(r"include\.PATH", text, re.I))}
    record(sid, "case-variant section/key spelling `[Include]` / `include.PATH`: git parses it?", rows,
           note=f"naive scan results on the fixture config: {lint}")


def s_promisor():
    sid = "21_promisor_fetch"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"payload.txt": "LAZY-FETCH-CONTENT\n"})
    lane = d / "lane"
    r = sh(["git", "clone", "-q", "--filter=blob:none", "--no-local", f"file://{store.resolve()}",
            str(lane.resolve())])
    built = r.returncode == 0
    if not built:
        record(sid, "partial clone / promisor remote: lazy fetch on cat-file", [], note=f"clone failed: {r.stderr[-200:]}")
        return
    cfg = (lane / ".git" / "config").read_text()
    blob = git(lane, "rev-parse", "HEAD:payload.txt").strip()
    pre = d / "lane" / ".git" / "objects"
    rows = run(sid, [
        ("cat-file-missing-blob", ["git", "-C", str(lane), "cat-file", "-t", blob], d, PIN_ENV),
        ("config-get-promisor", ["git", "-C", str(lane), "config", "--local", "--get-regexp",
                                 "^remote\\.|^extensions\\.|^core\\.repositoryformatversion"], d, PIN_ENV),
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
    ])
    record(sid, "promisor/partialClone remote (file:// outside): cat-file lazy-fetches outside d", rows,
           note="config: " + " / ".join(l for l in cfg.splitlines() if "promisor" in l or "partialclone" in l
                                        or "url" in l or "repositoryformatversion" in l)[:400])


def s_config_fifo():
    sid = "22_config_fifo"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    (lane / ".git" / "config").unlink()
    os.mkfifo(lane / ".git" / "config")
    row = trace(sid, "rev-parse-toplevel-on-fifo-config", ["git", "-C", str(lane), "rev-parse",
                                                           "--show-toplevel"], d, PIN_ENV, timeout=8)
    # a naive fence text scan: plain open() of .git/config with a 3 s budget
    import threading
    verdict = {}

    def scan():
        try:
            with open(lane / ".git" / "config", "r"):
                verdict["v"] = "read-returned"
        except OSError as e:
            verdict["v"] = f"OSError {e.errno}"

    t = threading.Thread(target=scan, daemon=True)
    t.start()
    t.join(3)
    scan_state = verdict.get("v", "BLOCKED (>3s)")
    record(sid, "`.git/config` replaced by a FIFO: does git / a text scan hang?", [row],
           note=f"naive open('.git/config') = {scan_state}; git probe rc={row['rc']}")


def s_objects_tree_symlink():
    sid = "23_gitdir_symlink_objects"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"only.txt": "STORED-OUTSIDE\n"})
    blob = git(store, "rev-parse", "HEAD:only.txt").strip()
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    # replace the whole objects dir with a symlink to the outside store
    objs = lane / ".git" / "objects"
    keep = lane / ".git" / "objects-inside"
    objs.rename(keep)
    os.symlink(store / ".git" / "objects", objs)
    rows = run(sid, [
        ("cat-file-via-objects-symlink", ["git", "-C", str(lane), "cat-file", "-t", blob], d, PIN_ENV),
        ("rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
    ])
    record(sid, "`.git/objects` symlinked to an outside store: git reads outside through the link", rows)


def s_argv_outside():
    sid = "24_argv_outside"
    d, side = fresh(sid)
    outside = repo(side / "outside-lane")
    commit(outside, {"claims.md": "x\n"})
    (d / "lane").mkdir()
    argv = ["--lane", str(outside), "--claims", "claims.md", "--receipt", "claims.md"]
    # what round45_c1_verify.build_module's contract check validates (no path_ok):
    accepted = (isinstance(argv, list) and all(isinstance(t, str) for t in argv))
    rows = run(sid, [
        ("rev-parse-outside-argv", ["git", "-C", argv[1], "rev-parse", "--show-toplevel"], d, PIN_ENV),
    ])
    record(sid, "argv token absolute OUTSIDE d: r45 build_module does not call path_ok", rows,
           note=f"build_module contract check accepts argv={accepted}; d={d}, token={outside}")


def main():
    OUT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)
    for fn in (s_worktree_relative, s_inc_gitdir_true, s_inc_gitdir_false, s_inc_onbranch, s_inc_tilde,
               s_inc_envvar, s_attr_excludes, s_hooks_fsmonitor, s_mailmap, s_submodule, s_alt_relative,
               s_commondir_relative, s_worktrees_meta, s_env_gitdir, s_gitfile_variants, s_dotgit_symlink,
               s_symlink_store_config, s_hardlink, s_case_variants, s_promisor, s_config_fifo,
               s_objects_tree_symlink, s_argv_outside):
        try:
            fn()
        except Exception as e:  # keep going; record the failure
            RESULTS[fn.__name__] = {"error": f"{type(e).__name__}: {e}"}
            print(f"{fn.__name__:26s} ERROR {type(e).__name__}: {e}", flush=True)
    (OUT / "vectors.json").write_text(json.dumps(RESULTS, indent=1, sort_keys=True))
    print(f"wrote {OUT / 'vectors.json'}")


if __name__ == "__main__":
    main()
