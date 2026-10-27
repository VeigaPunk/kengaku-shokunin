#!/usr/bin/env python3
"""R45SentFenceDesign round 2: corrected relative-path vectors plus new vector classes
(promisor lazy fetch, textconv exec, fence-crash layouts, per-worktree config, key spellings).

Same envelope: writes only under S.
"""
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import threading

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
RESULTS = {}


def sh(argv, cwd=None, env=None):
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, env=env or BUILD_ENV, capture_output=True,
                          text=True, timeout=180)


def git(repo, *args, check=True):
    r = sh(["git", "-C", str(repo), *args])
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr[-300:]}")
    return r.stdout


def fresh(sid):
    base = WORK / sid
    if base.exists():
        shutil.rmtree(base)
    d, side = base / "fx" / "f000", base / "fx" / "side"
    d.mkdir(parents=True)
    side.mkdir(parents=True)
    return d, side


def repo(path):
    path.mkdir(parents=True, exist_ok=True)
    r = sh(["git", "init", "-q", "-b", "master", str(path)], cwd=path.parent)
    if r.returncode:
        raise RuntimeError(r.stderr)
    return path


def commit(repo_path, files, msg="c"):
    for rel, text in files.items():
        p = pathlib.Path(repo_path) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    git(repo_path, "add", "-A")
    git(repo_path, "commit", "-qm", msg)


def trace(sid, label, argv, cwd, env, timeout=25, fixture=None):
    d = (fixture or (WORK / sid / "fx" / "f000")).resolve()
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
                if p.is_relative_to(scratch) and not p.is_relative_to(d):
                    execs.append(str(p))
                continue
            if not OPEN_RE.search(line):
                continue
            done = DONE_RE.search(line)
            args = ARG_RE.findall(line.split(" = ")[0])
            arg = pathlib.Path(args[0]) if args else None
            resolved, ok = None, False
            if done:
                ok = not done.group(1).startswith(("E", "-"))
                resolved = pathlib.Path(done.group(2)) if done.group(2) else None
            p = resolved or arg
            if p is None:
                continue
            p = pathlib.Path(os.path.normpath(str(p)))
            if p == d or p.is_relative_to(d):
                inside += bool(ok)
            elif p == scratch or p.is_relative_to(scratch):
                (outside if ok else attempts).append(str(p))
    return {"probe": label, "argv": argv, "rc": rc, "stdout": (out or "").strip()[:240],
            "stderr": (err or "").strip()[-200:], "inside_opens": inside,
            "outside_opens": len(outside), "outside_paths": sorted(set(outside))[:4],
            "outside_attempts": sorted(set(attempts))[:4], "outside_execs": sorted(set(execs))[:4]}


def record(sid, question, rows, note=""):
    RESULTS[sid] = {"question": question, "probes": rows, "note": note}
    tag = "PARSE" if any(r["outside_opens"] or r["outside_execs"] for r in rows) else "no-outside"
    print(f"{sid:26s} {tag:9s} " + " | ".join(
        f"{r['probe']}:rc={r['rc']},out={r['outside_opens']},ex={len(r['outside_execs'])}"
        f" :: {r['stdout'][:50]!r}" for r in rows), flush=True)


# ---- corrected relative vectors -------------------------------------------------

def s_core_worktree_relative():
    sid = "02b_core_worktree_relative"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    (side / "wt").mkdir(parents=True, exist_ok=True)
    (side / "wt" / "claims.md").write_text("outside worktree\n")
    git(lane, "config", "core.worktree", "../../side/wt")
    rows = [trace(sid, "rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
            trace(sid, "rev-parse-git-dir", ["git", "-C", str(lane), "rev-parse", "--git-dir"], d, PIN_ENV)]
    record(sid, "core.worktree = ../../side/wt (relative): resolved against gitdir, escapes d", rows,
           note=f"config value: {git(lane, 'config', '--local', '--get', 'core.worktree').strip()}")


def s_submodule_gitlink():
    sid = "11b_submodule_gitlink"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"s.txt": "sub\n"})
    sha = git(store, "rev-parse", "HEAD").strip()
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n", ".gitmodules": f'[submodule "x"]\n\tpath = x\n\turl = file://{store.resolve()}\n'})
    git(lane, "update-index", "--add", "--cacheinfo", f"160000,{sha},x")
    git(lane, "commit", "-qm", "gitlink")
    rows = [trace(sid, "submodule-status", ["git", "-C", str(lane), "submodule", "status"], d, PIN_ENV),
            trace(sid, "submodule-update-init", ["git", "-C", str(lane), "submodule", "update", "--init"], d, PIN_ENV)]
    record(sid, "submodule gitlink + file://<outside> url: does update --init read/clone outside d?", rows,
           note="traces show opens of side/store when the transport serves the submodule")


def s_alternates_relative():
    sid = "12b_alternates_relative"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"only-in-store.txt": "BORROWED\n"})
    blob = git(store, "rev-parse", "HEAD:only-in-store.txt").strip()
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    info = lane / ".git" / "objects" / "info"
    info.mkdir(parents=True, exist_ok=True)
    for name, rel in (("relative-correct", "../../../../side/store/.git/objects"),
                      ("relative-dot", "../../../side/store/.git/objects"),
                      ("absolute-control", str(store / ".git" / "objects"))):
        (info / "alternates").write_text(rel + "\n")
        RESULTS.setdefault(sid + ":" + name, []).append(
            trace(sid, f"cat-{name}", ["git", "-C", str(lane), "cat-file", "-t", blob], d, PIN_ENV))
    record(sid, "alternates relative vs absolute: does git resolve a relative alternates entry?", [], note="see keys")
    for name in ("relative-correct", "relative-dot", "absolute-control"):
        RESULTS[name] = RESULTS.pop(sid + ":" + name)
    for name in ("12b_alternates_relative", "relative-correct", "relative-dot", "absolute-control"):
        v = RESULTS[name]
        rows = v if isinstance(v, list) else v.get("probes", [])
        print(f"{name:26s} " + " | ".join(f"{r['probe']}:rc={r['rc']},out={r['outside_opens']} :: {r['stdout'][:40]!r}"
                                          for r in rows), flush=True)
    del RESULTS["12b_alternates_relative"]


def s_commondir_relative():
    sid = "13b_commondir_relative"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"only-in-store.txt": "BORROWED\n"})
    blob = git(store, "rev-parse", "HEAD:only-in-store.txt").strip()
    lane = d / "lane"
    gd = lane / ".git"
    gd.mkdir(parents=True)
    (gd / "commondir").write_text("../../../side/store/.git\n")
    (gd / "HEAD").write_text("ref: refs/heads/master\n")
    rows = [trace(sid, "rev-parse-common-dir", ["git", "-C", str(lane), "rev-parse", "--git-common-dir"], d, PIN_ENV),
            trace(sid, "rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
            trace(sid, "cat-file-borrowed", ["git", "-C", str(lane), "cat-file", "-t", blob], d, PIN_ENV)]
    record(sid, "commondir = ../../../side/store/.git (relative): git resolves it outside d", rows)


def s_gitfile_variants():
    sid = "16b_gitfile_variants"
    d, side = fresh(sid)
    variants = {"relative": "gitdir: ../../../side/gitdir-relative",
                "spacing": "gitdir : ../../../side/gitdir-spacing",
                "nospace": "gitdir:../../../side/gitdir-nospace",
                "upper": "GITDIR: ../../../side/gitdir-upper",
                "leading-nl": "\ngitdir: ../../../side/gitdir-leading-nl",
                "trailing-space": "gitdir: ../../../side/gitdir-trailing-space   "}
    rows = []
    for name, text in variants.items():
        gd = side / f"gitdir-{name}"
        gd.mkdir(parents=True, exist_ok=True)
        lane = d / f"v-{name}" / "lane"
        lane.mkdir(parents=True)
        r = sh(["git", "init", "-q", "-b", "master", str(lane)])
        commit(lane, {"a.txt": "x\n"})
        # move the real gitdir out, then write the variant .git file
        real = gd
        (lane / ".git").rename(real) if not real.exists() else shutil.rmtree(real)
        (lane / ".git").write_text(text + "\n")
        rows.append(trace(sid, f"variant-{name}", ["git", "-C", str(lane), "rev-parse", "--absolute-git-dir"],
                          d, PIN_ENV))
    record(sid, "`.git` FILE forms: does git accept relative target / spacing / case?", rows)


def s_worktree_meta_valid():
    sid = "14b_worktree_meta_valid"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    git(lane, "config", "user.email", "local@invalid")
    git(lane, "config", "extensions.worktreeConfig", "true")
    outside_wt = side / "wt"
    outside_wt.mkdir(parents=True, exist_ok=True)
    meta = lane / ".git" / "worktrees" / "wt"
    meta.mkdir(parents=True)
    (meta / "commondir").write_text("../..\n")
    (meta / "gitdir").write_text(str(outside_wt / ".git") + "\n")
    (meta / "HEAD").write_text("ref: refs/heads/master\n")
    (side / "inc.cfg").write_text("[user]\n\temail = WT-OUTSIDE@invalid\n")
    (meta / "config.worktree").write_text(f"[include]\n\tpath = {side / 'inc.cfg'}\n")
    (outside_wt / ".git").write_text(f"gitdir: {meta}\n")
    rows = [trace(sid, "main-rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV),
            trace(sid, "main-worktree-list", ["git", "-C", str(lane), "worktree", "list"], d, PIN_ENV),
            trace(sid, "main-config-user-email", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV),
            trace(sid, "outside-wt-config-user-email", ["git", "-C", str(outside_wt), "config", "--get", "user.email"],
                  outside_wt, PIN_ENV),
            trace(sid, "outside-wt-rev-parse", ["git", "-C", str(outside_wt), "rev-parse", "--show-toplevel"],
                  outside_wt, PIN_ENV)]
    record(sid, "valid linked-worktree metadata with outside gitdir + config.worktree include", rows)


def s_promisor_manual():
    sid = "21b_promisor_manual"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"payload.txt": "LAZY-FETCH-CONTENT\n"})
    blob = git(store, "rev-parse", "HEAD:payload.txt").strip()
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    git(lane, "config", "core.repositoryFormatVersion", "1")
    git(lane, "config", "extensions.partialClone", "origin")
    git(lane, "config", "remote.origin.url", f"file://{store.resolve()}")
    git(lane, "config", "remote.origin.promisor", "true")
    git(lane, "config", "remote.origin.partialclonefilter", "blob:none")
    rows = [trace(sid, "cat-file-foreign-blob", ["git", "-C", str(lane), "cat-file", "-t", blob], d, PIN_ENV),
            trace(sid, "rev-parse-toplevel", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV)]
    record(sid, "promisor remote + extensions.partialClone: cat-file of an absent object lazy-fetches", rows,
           note="config keys: " + git(lane, "config", "--local", "--get-regexp",
                                     "^(extensions|remote|core)\\.", check=False).strip().replace("\n", " ; ")[:400])


def s_textconv_exec():
    sid = "25_textconv_exec"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.bin": "hello\n"})
    (side / "textconv.sh").write_text(f"#!/bin/sh\necho RAN >> {side / 'TEXTconv-RAN'}\necho converted\n")
    (side / "textconv.sh").chmod(0o755)
    (side / "attrs").write_text("*.bin diff=outside\n")
    git(lane, "config", "core.attributesFile", str(side / "attrs"))
    git(lane, "config", "diff.outside.textconv", str(side / "textconv.sh"))
    git(lane, "config", "diff.outside.binary", "true")
    rows = [trace(sid, "show-textconv", ["git", "-C", str(lane), "show", "HEAD:a.bin"], d, PIN_ENV),
            trace(sid, "diff-textconv", ["git", "-C", str(lane), "diff", "HEAD~0", "--", "a.bin"], d, PIN_ENV)]
    record(sid, "core.attributesFile outside + diff.<d>.textconv outside: git executes an outside binary", rows,
           note=f"marker TEXTconv-RAN exists={ (side / 'TEXTconv-RAN').exists() }")


def s_fence_crash():
    sid = "26_fence_crash"
    d, side = fresh(sid)
    notes = {}
    # (a) .git/config is a directory
    lane = repo(d / "dir-config" / "lane")
    commit(lane, {"a.txt": "x\n"})
    (lane / ".git" / "config").unlink()
    (lane / ".git" / "config").mkdir()
    notes["config-as-dir"] = _crash(lane / ".git" / "config")
    # (b) .git/config unreadable (chmod 000)
    lane2 = repo(d / "unreadable" / "lane")
    commit(lane2, {"a.txt": "x\n"})
    (lane2 / ".git" / "config").chmod(0)
    notes["config-chmod0"] = _crash(lane2 / ".git" / "config")
    notes["git-on-chmod0"] = trace(sid, "git-chmod0", ["git", "-C", str(lane2), "rev-parse", "--show-toplevel"],
                                   d, PIN_ENV)["rc"]
    # (c) invalid UTF-8 config
    lane3 = repo(d / "badutf8" / "lane")
    commit(lane3, {"a.txt": "x\n"})
    (lane3 / ".git" / "config").write_bytes(b"[core]\n\tfoo = \xff\xfe\n")
    notes["config-nonutf8"] = _crash(lane3 / ".git" / "config")
    # (d) FIFO config
    lane4 = repo(d / "fifo" / "lane")
    commit(lane4, {"a.txt": "x\n"})
    (lane4 / ".git" / "config").unlink()
    os.mkfifo(lane4 / ".git" / "config")
    notes["config-fifo"] = _crash(lane4 / ".git" / "config")
    (lane2 / ".git" / "config").chmod(0o644)
    record(sid, "layouts that make a naive config text scan raise/block (counter counts ERROR as admitted)", [],
           note=json.dumps(notes))


def _crash(path):
    """What a naive `path.read_text()` fence scan does, without ever blocking on a FIFO."""
    try:
        st = os.stat(path)
        if stat.S_ISFIFO(st.st_mode):
            try:
                fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
                os.close(fd)
                return "fifo-nonblock-open-ok (plain read_text would block)"
            except OSError as e:
                return f"fifo OSError({e.errno})"
        path.read_bytes().decode("utf-8")
        return "read-ok"
    except PermissionError:
        return "PermissionError"
    except IsADirectoryError:
        return "IsADirectoryError"
    except UnicodeDecodeError:
        return "UnicodeDecodeError"
    except OSError as e:
        return f"OSError({e.errno})"


def s_fifo_scan():
    sid = "22b_fifo_scan"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    (lane / ".git" / "config").unlink()
    os.mkfifo(lane / ".git" / "config")
    state = {}

    def scan():
        try:
            with open(lane / ".git" / "config", "rb"):
                state["v"] = "read-returned"
        except OSError as e:
            state["v"] = f"OSError {e.errno}"

    t = threading.Thread(target=scan, daemon=True)
    t.start()
    t.join(5)
    rows = [trace(sid, "git-rev-parse-on-fifo-config", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"],
                  d, PIN_ENV, timeout=6)]
    record(sid, "`.git/config` as FIFO: git hangs; plain open() blocks past 5 s", rows,
           note=f"naive open = {state.get('v', 'BLOCKED >5s')}")


def s_key_spellings():
    sid = "27_key_spellings"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    git(lane, "config", "user.email", "local@invalid")
    (side / "inc.cfg").write_text("[user]\n\temail = SPELL-OUTSIDE@invalid\n")
    spellings = {"dotted-upper-key": f"include.PATH = {side / 'inc.cfg'}\n",
                 "inline-section": f"[include] path = {side / 'inc.cfg'}\n",
                 "section-lower-mixed": f"[InClUdE]\n\tpath = {side / 'inc.cfg'}\n"}
    rows, notes = [], {}
    for name, text in spellings.items():
        cfg = (lane / ".git" / "config").read_text() + text
        (lane / ".git" / "config").write_text(cfg)
        r = trace(sid, f"spelling-{name}", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV)
        rows.append(r)
        notes[name] = {"stdout": r["stdout"], "outside_opens": r["outside_opens"],
                       "naive_ci_regex": bool(re.search(r"include\.path|\[include", cfg, re.I)),
                       "naive_cs_regex": bool(re.search(r"include\.path|\[include", cfg))}
        (lane / ".git" / "config").write_text(cfg[: -len(text)])
    record(sid, "config key spellings: is `include.PATH` / inline section parsed by git and by a naive scan?", rows,
           note=json.dumps(notes))


def s_gitdir_symlink_only():
    sid = "17b_dotgit_symlink_scan"
    d, side = fresh(sid)
    gd = side / "gitdir"
    gd.mkdir(parents=True, exist_ok=True)
    lane = d / "lane"
    lane.mkdir()
    r = sh(["git", "init", "-q", "-b", "master", "--separate-git-dir", str(gd), str(lane)])
    commit(lane, {"a.txt": "x\n"})
    (lane / ".git").unlink(missing_ok=True)
    os.symlink(gd, lane / ".git")
    rows = [trace(sid, "walk-lists-.git-as-dir", ["python3", "-c",
                 f"import os;print([ (t,d) for t,d,f in os.walk('{lane}') if '.git' in d])"], d, PIN_ENV),
            trace(sid, "read-config-through-symlink", ["python3", "-c",
                 f"print(open('{lane}/.git/config').read()[:40])"], d, PIN_ENV),
            trace(sid, "git-rev-parse", ["git", "-C", str(lane), "rev-parse", "--show-toplevel"], d, PIN_ENV)]
    record(sid, "`.git` symlink: os.walk lists it as a dir; reading `.git/config` follows it outside", rows)


def main():
    import signal

    class _TO(Exception):
        pass

    def _alarm(_sig, _frm):
        raise _TO("scenario exceeded 150 s")

    signal.signal(signal.SIGALRM, _alarm)
    OUT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    for fn in (s_core_worktree_relative, s_submodule_gitlink, s_alternates_relative, s_commondir_relative,
               s_gitfile_variants, s_worktree_meta_valid, s_promisor_manual, s_textconv_exec, s_fence_crash,
               s_fifo_scan, s_key_spellings, s_gitdir_symlink_only):
        signal.alarm(150)
        try:
            fn()
        except Exception as e:
            RESULTS[fn.__name__] = {"error": f"{type(e).__name__}: {e}"}
            print(f"{fn.__name__:26s} ERROR {type(e).__name__}: {e}", flush=True)
        finally:
            signal.alarm(0)
    (OUT / "vectors2.json").write_text(json.dumps(RESULTS, indent=1, sort_keys=True))
    print("wrote", OUT / "vectors2.json")


if __name__ == "__main__":
    main()
