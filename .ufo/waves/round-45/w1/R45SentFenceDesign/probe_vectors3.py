#!/usr/bin/env python3
"""R45SentFenceDesign round 3: corrected core.worktree / gitfile / textconv fixtures, the submodule
protocol question, and the round-44 fence legs applied to every vector fixture (observed baseline)."""
import importlib.util
import json
import os
import pathlib
import shutil
import signal
import subprocess

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign")
WORK, OUT, LOGS = S / "work", S / "out", S / "logs"
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
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
R = {}


def sh(argv, cwd=None, env=None):
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, env=env or BUILD_ENV, capture_output=True,
                          text=True, timeout=180)


def git(repo, *args, check=True):
    r = sh(["git", "-C", str(repo), *args])
    if check and r.returncode:
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


def commit(rp, files, msg="c"):
    for rel, text in files.items():
        p = pathlib.Path(rp) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    git(rp, "add", "-A")
    git(rp, "commit", "-qm", msg)


def show(label, **kw):
    print(f"{label:34s} " + " ".join(f"{k}={v}" for k, v in kw.items() if not isinstance(v, list)) , flush=True)
    if kw.get("paths"):
        print(f"{'':34s} paths={kw['paths']}", flush=True)


# ---- 02c: core.worktree relative, git's own base -------------------------------

def s_core_worktree_relative():
    sid = "02c_core_worktree_relative"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"claims.md": "x\n"})
    (side / "wt").mkdir(parents=True, exist_ok=True)
    (side / "wt" / "claims.md").write_text("outside worktree\n")
    rows = {}
    for val in ("../side/wt", "../../side/wt", "../../../side/wt", "../../../../side/wt"):
        sh(["git", "-C", str(lane), "config", "--unset", "core.worktree"], check=False)
        sh(["git", "-C", str(lane), "config", "core.worktree", val])
        r = sh(["git", "-C", str(lane), "rev-parse", "--show-toplevel"], env=PIN_ENV)
        rows[val] = {"rc": r.returncode, "stdout": r.stdout.strip(), "stderr": r.stderr.strip()[:120]}
    # what the round-44 leg's own arithmetic says for the value git accepted
    good = [v for v, x in rows.items() if x["rc"] == 0 and x["stdout"].startswith(str(side))]
    leg = {}
    for v in rows:
        p = pathlib.Path(v)
        leg[v] = {"r44_leg_resolves_to": str((lane / p).resolve()),
                  "r44_leg_admits": (lane / p).resolve() == lane.resolve()}
    R[sid] = {"rows": rows, "leg": leg, "accepted_relative_to_outside": good}
    print(sid, json.dumps(rows), flush=True)
    print("  leg arithmetic:", json.dumps(leg), flush=True)


# ---- 16c: gitfile variants, rename first --------------------------------------

def s_gitfile_variants():
    sid = "16c_gitfile_variants"
    d, side = fresh(sid)
    variants = {"relative": "gitdir: ../../../side/gitdir-relative",
                "spacing": "gitdir : ../../../side/gitdir-spacing",
                "nospace": "gitdir:../../../side/gitdir-nospace",
                "upper": "GITDIR: ../../../side/gitdir-upper",
                "leading-nl": "\ngitdir: ../../../side/gitdir-leading-nl",
                "trailing-space": "gitdir: ../../../side/gitdir-trailing-space   ",
                "relative-valid": "gitdir: ../../../side/gitdir-relative-valid"}
    out = {}
    for name, text in variants.items():
        real = side / f"gitdir-{name}"
        shutil.rmtree(real, ignore_errors=True)
        lane = d / f"v-{name}" / "lane"
        lane.mkdir(parents=True)
        sh(["git", "init", "-q", "-b", "master", str(lane)])
        commit(lane, {"a.txt": "x\n"})
        (lane / ".git").rename(real)
        (lane / ".git").write_text(text + "\n")
        r = sh(["git", "-C", str(lane), "rev-parse", "--absolute-git-dir"], env=PIN_ENV)
        cfg = sh(["git", "-C", str(lane), "config", "--get", "user.name"], env=PIN_ENV)
        out[name] = {"rc": r.returncode, "git_dir": r.stdout.strip(), "stderr": r.stderr.strip()[:110],
                     "config_rc": cfg.returncode, "target_in_fixture": str(real)}
    R[sid] = out
    for k, v in out.items():
        print(f"{sid} {k:16s} rc={v['rc']} dir={v['git_dir'][-40:]!r} err={v['stderr'][:60]!r}", flush=True)


# ---- 25c: textconv with a real content change --------------------------------

def s_textconv_exec():
    sid = "25c_textconv_exec"
    d, side = fresh(sid)
    lane = repo(d / "lane")
    commit(lane, {"a.bin": "hello\n"})
    (side / "textconv.sh").write_text(f"#!/bin/sh\necho RAN >> {side / 'TEXTCONV-RAN'}\ncat\n")
    (side / "textconv.sh").chmod(0o755)
    (side / "attrs").write_text("*.bin diff=outside\n")
    git(lane, "config", "core.attributesFile", str(side / "attrs"))
    git(lane, "config", "diff.outside.textconv", str(side / "textconv.sh"))
    git(lane, "config", "diff.outside.binary", "true")
    (lane / "a.bin").write_text("hello world\n")
    r = sh([STRACE, "-f", "-qq", "-y", "-e", "trace=open,execve", "-o", str(LOGS / f"{sid}.log"),
            "git", "-C", str(lane), "diff", "--", "a.bin"], env=PIN_ENV)
    log = (LOGS / f"{sid}.log").read_text(errors="replace")
    execs = [l for l in log.splitlines() if "execve" in l and str(side) in l]
    opens = [l for l in log.splitlines() if str(side) in l and "open" in l]
    R[sid] = {"diff_stdout": r.stdout[:200], "diff_rc": r.returncode,
              "marker": (side / "TEXTCONV-RAN").exists(), "execs": len(execs),
              "outside_open_lines": len(opens), "first_open": (opens[0][:200] if opens else ""),
              "first_exec": (execs[0][:220] if execs else "")}
    print(sid, json.dumps({k: v for k, v in R[sid].items() if k != "first_open"})[:300], flush=True)
    print("  first_open:", R[sid]["first_open"][:160], flush=True)
    print("  first_exec:", R[sid]["first_exec"][:160], flush=True)


# ---- 11c: submodule with file protocol allowed -------------------------------

def s_submodule_allowed():
    sid = "11c_submodule_allowed"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"s.txt": "sub\n"})
    sha = git(store, "rev-parse", "HEAD").strip()
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n", ".gitmodules": f'[submodule "x"]\n\tpath = x\n\turl = file://{store.resolve()}\n'})
    git(lane, "update-index", "--add", "--cacheinfo", f"160000,{sha},x")
    git(lane, "commit", "-qm", "gitlink")
    env = {**PIN_ENV, "GIT_ALLOW_PROTOCOL": "file", "GIT_CONFIG_COUNT": "5",
           **{f"GIT_CONFIG_KEY_{i}": k for i, k in enumerate(
               ("core.fsmonitor", "core.hooksPath", "gpg.program", "log.showSignature", "protocol.file.allow"))},
           **{f"GIT_CONFIG_VALUE_{i}": v for i, v in enumerate(
               ("false", "/dev/null", "/bin/true", "false", "always"))}}
    r = sh([STRACE, "-f", "-qq", "-y", "-e", "trace=open,openat,execve", "-o", str(LOGS / f"{sid}.log"),
            "git", "-C", str(lane), "submodule", "update", "--init"], env=env)
    log = (LOGS / f"{sid}.log").read_text(errors="replace")
    outside = sorted({s for s in log.replace('"', " ").replace(",", " ").split() if str(side) in s})[:6]
    R[sid] = {"rc": r.returncode, "stdout": r.stdout[:200], "stderr": r.stderr[-300:],
              "outside_paths": outside, "cloned": (lane / "x" / ".git").exists()}
    print(sid, json.dumps({k: v for k, v in R[sid].items() if k != "outside_paths"})[:400], flush=True)
    print("  outside:", outside, flush=True)


# ---- 29: alternates as a symlink inside d ------------------------------------

def s_alternates_symlink():
    sid = "29_alternates_symlink"
    d, side = fresh(sid)
    store = repo(side / "store")
    commit(store, {"only.txt": "BORROWED\n"})
    blob = git(store, "rev-parse", "HEAD:only.txt").strip()
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    info = lane / ".git" / "objects" / "info"
    info.mkdir(parents=True, exist_ok=True)
    (side / "alt-target").write_text(str(store / ".git" / "objects") + "\n")
    os.symlink(side / "alt-target", info / "alternates")
    rows = {"cat": sh(["git", "-C", str(lane), "cat-file", "-t", blob], env=PIN_ENV)}
    R[sid] = {"rc": rows["cat"].returncode, "stdout": rows["cat"].stdout.strip(),
              "target_is_symlink_outside": True}
    print(sid, json.dumps(R[sid]), flush=True)


# ---- r44 legs applied to every vector fixture -------------------------------

def s_r44_legs():
    spec = importlib.util.spec_from_file_location("k44", LANE / "plans/round44_c1_verify.py")
    k44 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k44)
    cases = []
    f = WORK
    cases += [("03_includeIf-gitdir-true", f / "03_inc_gitdir_true/fx/f000", "order",
               ["--lane", "lane", "--claims", "claims.md", "--receipt", "claims.md"])]
    cases += [("04_includeIf-gitdir-false", f / "04_inc_gitdir_false/fx/f000", "order",
               ["--lane", "lane", "--claims", "claims.md", "--receipt", "claims.md"])]
    cases += [("05_includeIf-onbranch", f / "05_inc_onbranch/fx/f000", "order",
               ["--lane", "lane", "--claims", "claims.md", "--receipt", "claims.md"])]
    cases += [("06_include-tilde", f / "06_inc_tilde/fx/f000", "order",
               ["--lane", "lane", "--claims", "claims.md", "--receipt", "claims.md"])]
    cases += [("07_include-envvar", f / "07_inc_envvar/fx/f000", "order",
               ["--lane", "lane", "--claims", "claims.md", "--receipt", "claims.md"])]
    cases += [("08-attributes-excludes", f / "08_attributes_excludes/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("09-hooks-fsmonitor", f / "09_hooks_fsmonitor/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("10-mailmap", f / "10_mailmap/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("12b-alternates-relative", f / "12b_alternates_relative/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("13b-commondir-relative", f / "13b_commondir_relative/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("14b-worktrees-meta", f / "14b_worktree_meta_valid/fx/f000", "order",
               ["--lane", "lane", "--claims", "claims.md", "--receipt", "claims.md"])]
    cases += [("16c-gitfile-relative", f / "16c_gitfile_variants/fx/f000/v-relative", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("16c-gitfile-upper", f / "16c_gitfile_variants/fx/f000/v-upper", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("17-dotgit-symlink", f / "17_dotgit_symlink/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("18-symlink-config", f / "18_symlink_store_config/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("19-hardlink", f / "19_hardlink_objects/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("20-case-Include", f / "20_case_variants/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("21b-promisor", f / "21b_promisor_manual/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("23-objects-symlink", f / "23_gitdir_symlink_objects/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("24-argv-outside", f / "24_argv_outside/fx/f000", "order",
               ["--lane", str(f / "24_argv_outside/fx/side/outside-lane"), "--claims", "claims.md",
                "--receipt", "claims.md"])]
    cases += [("26-config-as-dir", f / "26_fence_crash/fx/f000/dir-config", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("26-config-nonutf8", f / "26_fence_crash/fx/f000/badutf8", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("27-inline-include", f / "27_key_spellings/fx/f000", "order",
               ["--lane", "lane", "--claims", "a.txt", "--receipt", "a.txt"])]
    cases += [("02c-core-worktree", f / "02c_core_worktree_relative/fx/f000", "order",
               ["--lane", "lane", "--claims", "claims.md", "--receipt", "claims.md"])]
    results = {}
    for name, d, tool, argv in cases:
        if not d.is_dir():
            results[name] = "MISSING"
            continue
        signal.alarm(90)
        try:
            reason = (k44.argv_shape_breach(tool, argv) or k44.lane_breach(d, argv) or k44.repo_breach(d)
                      or k44.symlink_breach(d) or k44.order_argv_breach(d, argv))
        except Exception as e:
            reason = f"EXC {type(e).__name__}: {e}"
        finally:
            signal.alarm(0)
        results[name] = "BREACH: " + reason if reason else "ADMIT"
        print(f"R44LEG {name:26s} {results[name][:130]}", flush=True)
    R["r44_legs"] = results


def main():
    def _alarm(_s, _f):
        raise TimeoutError("scenario alarm")

    signal.signal(signal.SIGALRM, _alarm)
    for fn in (s_core_worktree_relative, s_gitfile_variants, s_textconv_exec, s_submodule_allowed,
               s_alternates_symlink, s_r44_legs):
        signal.alarm(240)
        try:
            fn()
        except Exception as e:
            R[fn.__name__] = f"ERROR {type(e).__name__}: {e}"
            print(f"{fn.__name__} ERROR {type(e).__name__}: {e}", flush=True)
        finally:
            signal.alarm(0)
    (OUT / "vectors3.json").write_text(json.dumps(R, indent=1, sort_keys=True))
    print("wrote", OUT / "vectors3.json")


if __name__ == "__main__":
    main()
