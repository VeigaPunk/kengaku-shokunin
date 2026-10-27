#!/usr/bin/env python3
"""R45SentFenceDesign round 4: core.worktree relative (fixed), key spellings retained + r44 oracle per
spelling, submodule protocol from repo config, and a repo ABOVE d whose config carries an include."""
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


def r44_verdict(m, d, tool, argv):
    signal.alarm(90)
    try:
        return ("BREACH: " + (m.argv_shape_breach(tool, argv) or m.lane_breach(d, argv) or m.repo_breach(d)
                              or m.symlink_breach(d) or m.order_argv_breach(d, argv) or "")).strip()
    except Exception as e:
        return f"EXC {type(e).__name__}: {e}"
    finally:
        signal.alarm(0)


def s_core_worktree_relative():
    sid = "02d_core_worktree_relative"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    (side / "wt").mkdir(parents=True, exist_ok=True)
    (side / "wt" / "claims.md").write_text("outside worktree\n")
    rows = {}
    for val in ("../side/wt", "../../side/wt", "../../../side/wt", "../../../../side/wt"):
        sh(["git", "-C", str(lane), "config", "--unset", "core.worktree"])
        sh(["git", "-C", str(lane), "config", "core.worktree", val])
        r = sh(["git", "-C", str(lane), "rev-parse", "--show-toplevel"], env=PIN_ENV)
        rows[val] = {"rc": r.returncode, "stdout": r.stdout.strip(), "stderr": r.stderr.strip()[:100],
                     "r44_leg_resolves": str((lane / val).resolve())}
    R[sid] = rows
    print(sid, json.dumps(rows)[:900], flush=True)


def s_key_spellings():
    sid = "27b_key_spellings"
    d, side = fresh(sid)
    m = k44()
    out = {}
    for name, text in {
            "inline-section": f"[include] path = {side / 'inc1.cfg'}\n",
            "mixed-case-section": f"[InClUdE]\n\tpath = {side / 'inc2.cfg'}\n",
            "dotted-lower": f"include.path = {side / 'inc3.cfg'}\n",
            "dotted-upper-key": f"include.PATH = {side / 'inc4.cfg'}\n"}.items():
        lane = repo(d / name / "lane")
        commit(lane, {"a.txt": "x\n"})
        git(lane, "config", "user.email", "local@invalid")
        with open(lane / ".git" / "config", "a") as f:
            f.write(text)
        r = sh(["git", "-C", str(lane), "config", "--get", "user.email"], env=PIN_ENV)
        argv = ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"]
        out[name] = {"git_email": r.stdout.strip(), "git_rc": r.returncode,
                     "r44": r44_verdict(m, d / name, "order", argv)}
        print(f"{sid} {name:20s} email={out[name]['git_email']!r} rc={r.returncode} r44={out[name]['r44'][:70]}",
              flush=True)
    R[sid] = out


def s_submodule_repo_config():
    sid = "11d_submodule_repo_config"
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
    R[sid] = {"rc": r.returncode, "stderr": r.stderr[-160:], "cloned": (lane / "x" / ".git").exists()}
    print(sid, json.dumps(R[sid])[:400], flush=True)


def s_above_include():
    sid = "31_above_repo_include"
    d, side = fresh(sid)
    fx = d.parent
    above = repo(fx)  # repo at the module build root, ABOVE d (the f6 shape)
    (d / "lane").mkdir()
    commit(above, {"a.txt": "x\n"})
    (side / "inc.cfg").write_text("[user]\n\temail = ABOVE-OUTSIDE@invalid\n")
    with open(above / ".git" / "config", "a") as f:
        f.write(f"[include]\n\tpath = {side / 'inc.cfg'}\n")
    r = sh(["git", "-C", str(d / "lane"), "config", "--get", "user.email"], env=PIN_ENV)
    t = sh(["git", "-C", str(d / "lane"), "rev-parse", "--show-toplevel"], env=PIN_ENV)
    R[sid] = {"lane_config_email": r.stdout.strip(), "lane_toplevel": t.stdout.strip(),
              "above_repo": str(fx)}
    print(sid, json.dumps(R[sid])[:400], flush=True)


def main():
    signal.signal(signal.SIGALRM, lambda *_a: (_ for _ in ()).throw(TimeoutError("alarm")))
    for fn in (s_core_worktree_relative, s_key_spellings, s_submodule_repo_config, s_above_include):
        signal.alarm(240)
        try:
            fn()
        except Exception as e:
            R[fn.__name__] = f"ERROR {type(e).__name__}: {e}"
            print(fn.__name__, "ERROR", type(e).__name__, e, flush=True)
        finally:
            signal.alarm(0)
    (OUT / "vectors4.json").write_text(json.dumps(R, indent=1, sort_keys=True))
    print("wrote", OUT / "vectors4.json")


if __name__ == "__main__":
    main()
