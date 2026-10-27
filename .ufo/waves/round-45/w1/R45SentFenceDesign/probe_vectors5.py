#!/usr/bin/env python3
"""R45SentFenceDesign round 5: core.worktree base (via --file edits), key spellings with real targets,
submodule repo-scope protocol (full stderr), textconv with openat traced."""
import importlib.util
import json
import pathlib
import shutil
import signal
import subprocess

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign")
WORK, OUT, LOGS = S / "work", S / "out", S / "logs"
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
BASE_ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/nonexistent",
            "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
GIT_PINS = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "4",
            "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
            "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
            "GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
            "GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false"}
PIN_ENV = {**BASE_ENV, **GIT_PINS}
BUILD_ENV = {**PIN_ENV, "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "f@invalid",
             "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "f@invalid"}
R = {}


def sh(argv, cwd=None, env=None):
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, env=env or BUILD_ENV, capture_output=True,
                          text=True, timeout=180)


def git(rp, *args, check=True):
    r = sh(["git", "-C", str(rp), *args])
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(args)}: {r.stderr[-200:]}")
    return r.stdout


def fresh(sid):
    base = WORK / sid
    shutil.rmtree(base, ignore_errors=True)
    d, side = base / "fx" / "f000", base / "fx" / "side"
    d.mkdir(parents=True)
    side.mkdir(parents=True)
    return d, side


def repo(p):
    p.mkdir(parents=True, exist_ok=True)
    sh(["git", "init", "-q", "-b", "master", str(p)], cwd=p.parent)
    return p


def commit(rp, files, msg="c"):
    for rel, text in files.items():
        q = pathlib.Path(rp) / rel
        q.parent.mkdir(parents=True, exist_ok=True)
        q.write_text(text)
    git(rp, "add", "-A")
    git(rp, "commit", "-qm", msg)


def k44():
    spec = importlib.util.spec_from_file_location("k44", LANE / "plans/round44_c1_verify.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def s_core_worktree():
    sid = "02e_core_worktree_base"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    (side / "wt").mkdir(parents=True, exist_ok=True)
    (side / "wt" / "claims.md").write_text("outside worktree\n")
    cfg = lane / ".git" / "config"
    rows = {}
    for val in ("../side/wt", "../../side/wt", "../../../side/wt", "../../../../side/wt"):
        c = cfg.read_text()
        c = "\n".join(l for l in c.splitlines() if "worktree" not in l) + f"\n[core]\n\tworktree = {val}\n"
        cfg.write_text(c)
        r = sh(["git", "-C", str(lane), "rev-parse", "--show-toplevel"], env=PIN_ENV)
        rows[val] = {"rc": r.returncode, "stdout": r.stdout.strip(), "stderr": r.stderr.strip()[:90]}
    R[sid] = rows
    print(sid, json.dumps(rows)[:900], flush=True)


def s_key_spellings():
    sid = "27c_key_spellings"
    d, side = fresh(sid)
    m = k44()
    out = {}
    for name, text, tgt in (
            ("inline-section", lambda p: f"[include] path = {p}\n", "inc1.cfg"),
            ("mixed-case-section", lambda p: f"[InClUdE]\n\tpath = {p}\n", "inc2.cfg"),
            ("inline-lower", lambda p: f"[include]\n\tpath = {p}\n", "inc3.cfg")):
        (side / tgt).write_text("[user]\n\temail = SPELL-OUTSIDE@invalid\n")
        lane = repo(d / name / "lane")
        commit(lane, {"a.txt": "x\n"})
        git(lane, "config", "user.email", "local@invalid")
        with open(lane / ".git" / "config", "a") as f:
            f.write(text(side / tgt))
        r = sh(["git", "-C", str(lane), "config", "--get", "user.email"], env=PIN_ENV)
        argv = ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"]
        signal.alarm(60)
        try:
            v = m.lane_breach(d / name, argv) or m.repo_breach(d / name) or m.symlink_breach(d / name)
        finally:
            signal.alarm(0)
        out[name] = {"git_email": r.stdout.strip(), "r44": "BREACH: " + v if v else "ADMIT"}
        print(f"{sid} {name:20s} email={out[name]['git_email']!r} r44={out[name]['r44'][:70]}", flush=True)
    R[sid] = out


def s_submodule():
    sid = "11e_submodule_repo_config"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"s.txt": "sub\n"})
    sha = git(store, "rev-parse", "HEAD").strip()
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n", ".gitmodules": f'[submodule "x"]\n\tpath = x\n\turl = file://{store.resolve()}\n'})
    git(lane, "update-index", "--add", "--cacheinfo", f"160000,{sha},x")
    git(lane, "commit", "-qm", "gitlink")
    git(lane, "config", "protocol.file.allow", "always")
    r = sh(["git", "-C", str(lane), "submodule", "update", "--init"], env=PIN_ENV)
    R[sid] = {"rc": r.returncode, "stderr_full": r.stderr, "cloned": (lane / "x" / ".git").exists()}
    print(sid, "rc=", r.returncode, "cloned=", R[sid]["cloned"], "err=", r.stderr.strip()[-220:], flush=True)


def s_textconv():
    sid = "25e_textconv"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.bin": "hello\n"})
    (side / "textconv.sh").write_text(f"#!/bin/sh\necho RAN >> {side / 'TEXT-RAN'}\ncat\n")
    (side / "textconv.sh").chmod(0o755)
    (side / "attrs").write_text("*.bin diff=outside\n")
    git(lane, "config", "core.attributesFile", str(side / "attrs"))
    git(lane, "config", "diff.outside.textconv", str(side / "textconv.sh"))
    git(lane, "config", "diff.outside.binary", "true")
    (lane / "a.bin").write_text("hello world\n")
    log = LOGS / f"{sid}.log"
    r = sh(["strace", "-f", "-qq", "-y", "-e", "trace=open,openat,openat2,execve", "-o", str(log),
            "git", "-C", str(lane), "diff", "--", "a.bin"], env=PIN_ENV)
    text = log.read_text(errors="replace")
    opens = [l for l in text.splitlines() if "open" in l and str(side) in l]
    execs = [l for l in text.splitlines() if "execve" in l and str(side) in l]
    R[sid] = {"rc": r.returncode, "marker": (side / "TEXT-RAN").exists(), "open_lines": len(opens),
              "exec_lines": len(execs), "first_open": opens[0][:220] if opens else "",
              "first_exec": execs[0][:220] if execs else ""}
    print(sid, json.dumps({k: v for k, v in R[sid].items() if not k.startswith("first")})[:300], flush=True)
    print("  open:", R[sid]["first_open"][:200])
    print("  exec:", R[sid]["first_exec"][:200])


def main():
    signal.signal(signal.SIGALRM, lambda *_a: (_ for _ in ()).throw(TimeoutError("alarm")))
    for fn in (s_core_worktree, s_key_spellings, s_submodule, s_textconv):
        signal.alarm(240)
        try:
            fn()
        except Exception as e:
            R[fn.__name__] = f"ERROR {type(e).__name__}: {e}"
            print(fn.__name__, "ERROR", type(e).__name__, e, flush=True)
        finally:
            signal.alarm(0)
    (OUT / "vectors5.json").write_text(json.dumps(R, indent=1, sort_keys=True))
    print("wrote", OUT / "vectors5.json")


if __name__ == "__main__":
    main()
