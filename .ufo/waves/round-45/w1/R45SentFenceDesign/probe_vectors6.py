#!/usr/bin/env python3
"""R45SentFenceDesign round 6: remaining rows — relative include target, diff.external exec,
.git/HEAD symlink, and a `.git/config` readable-through-bind sanity check."""
import json
import pathlib
import shutil
import subprocess

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign")
WORK, OUT, LOGS = S / "work", S / "out", S / "logs"
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
                          text=True, timeout=120)


def git(rp, *a, check=True):
    r = sh(["git", "-C", str(rp), *a])
    if check and r.returncode:
        raise RuntimeError(r.stderr[-200:])
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


def strace_run(label, argv, cwd, env):
    log = LOGS / f"r6--{label}.log"
    r = sh(["strace", "-f", "-qq", "-y", "-e", "trace=open,openat,openat2,creat,execve", "-o", str(log), *argv],
           cwd=cwd, env=env)
    lines = log.read_text(errors="replace").splitlines()
    return r, lines


def outside_lines(lines, side):
    return [l for l in lines if str(side) in l and ("open" in l or "execve" in l)]


def main():
    # 33: relative include target, resolved against .git
    d, side = fresh("33_relative_include")
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    git(lane, "config", "user.email", "local@invalid")
    (side / "inc.cfg").write_text("[user]\n\temail = RELOUTSIDE@invalid\n")
    with open(lane / ".git" / "config", "a") as f:
        f.write("[include]\n\tpath = ../../../side/inc.cfg\n")
    r, lines = strace_run("relative-include", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV)
    R["33_relative_include"] = {"rc": r.returncode, "email": r.stdout.strip(),
                                "outside": [l[:180] for l in outside_lines(lines, side)][:3]}
    print("33", json.dumps(R["33_relative_include"])[:400], flush=True)

    # 34: diff.external (repo config, no attributes file needed)
    d, side = fresh("34_diff_external")
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "one\n"})
    (side / "dext.sh").write_text(f"#!/bin/sh\necho RAN >> {side / 'DEXT-RAN'}\ndiff \"$2\" \"$5\"\n")
    (side / "dext.sh").chmod(0o755)
    git(lane, "config", "diff.external", str(side / "dext.sh"))
    (lane / "a.txt").write_text("two\n")
    r, lines = strace_run("diff-external", ["git", "-C", str(lane), "diff"], d, PIN_ENV)
    R["34_diff_external"] = {"rc": r.returncode, "marker": (side / "DEXT-RAN").exists(),
                             "outside": [l[:180] for l in outside_lines(lines, side)][:3]}
    print("34", json.dumps(R["34_diff_external"])[:400], flush=True)

    # 35: .git/HEAD as a symlink to a file outside d
    d, side = fresh("35_head_symlink")
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    (side / "HEAD-copy").write_text("ref: refs/heads/master\n")
    (lane / ".git" / "HEAD").unlink()
    (lane / ".git" / "HEAD").symlink_to(side / "HEAD-copy")
    r, lines = strace_run("head-symlink", ["git", "-C", str(lane), "rev-parse", "--abbrev-ref", "HEAD"], d, PIN_ENV)
    R["35_head_symlink"] = {"rc": r.returncode, "stdout": r.stdout.strip(),
                            "outside": [l[:180] for l in outside_lines(lines, side)][:3]}
    print("35", json.dumps(R["35_head_symlink"])[:400], flush=True)

    # 36: .git/info/refs? (inside) sanity: config include with `~` while HOME is a real dir inside scratch
    #     (already covered) -> instead measure `.git/config` through a hardlink to an outside file with nlink
    d, side = fresh("36_hardlink_config_nlink")
    lane = repo(d / "lane")
    commit(lane, {"a.txt": "x\n"})
    (side / "cfg").write_text("[user]\n\temail = HARDLINK@invalid\n")
    (lane / ".git" / "config").unlink()
    import os
    os.link(side / "cfg", lane / ".git" / "config")
    st = os.stat(lane / ".git" / "config")
    r, lines = strace_run("hardlink-config", ["git", "-C", str(lane), "config", "--get", "user.email"], d, PIN_ENV)
    R["36_hardlink_config_nlink"] = {"rc": r.returncode, "email": r.stdout.strip(), "nlink": st.st_nlink,
                                     "outside": [l[:160] for l in outside_lines(lines, side)][:3]}
    print("36", json.dumps(R["36_hardlink_config_nlink"])[:400], flush=True)

    (OUT / "vectors6.json").write_text(json.dumps(R, indent=1, sort_keys=True))
    print("wrote", OUT / "vectors6.json")


if __name__ == "__main__":
    main()
