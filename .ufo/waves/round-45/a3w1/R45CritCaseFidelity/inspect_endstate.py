#!/usr/bin/env python3
"""R45CritCaseFidelity hostile inspector: for each of the 16 frozen cases, run the captured
setup.sh + the case's recipe.sh in the same bwrap envelope the probe uses, then dump the TRUE
end state (typed listing of /app, the graded path's bytes, an independent per-line format audit,
the image's sha256 and the two fragment windows, leftover/oracle artifacts) as JSON lines.
Independently written bwrap argv + dumper; only the frozen recipe strings are imported.
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CAP = LANE / "corpus/evidence/round45/tb2-password-recovery"
sys.path.insert(0, str(LANE / "plans"))
import password_recovery_probe as prp  # frozen: recipes + pins only

PINS = dict(prp.PINS)
BWRAP = "/usr/bin/bwrap"
PATHENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
           "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
ANSWER = "8XDP5Q2RT9ZK7VB3BV4WW54"

# dumper executed INSIDE the sandbox after seed+recipe. Emits one JSON object on stdout.
DUMP_PY = r'''
import hashlib, json, os, re
out = {"answer": "8XDP5Q2RT9ZK7VB3BV4WW54"}
p = "/app/recovered_passwords.txt"
if not os.path.exists(p):
    out["graded"] = {"state": "absent"}
elif os.path.isdir(p):
    out["graded"] = {"state": "dir", "entries": sorted(os.listdir(p))}
    try:
        open(p).read()
    except BaseException as e:
        out["graded"]["read_exc"] = type(e).__name__
else:
    b = open(p, "rb").read()
    lines = b.split(b"\n")
    audit = []
    for ln in lines:
        s = ln.decode("utf-8", "backslashreplace")
        audit.append({"len": len(s), "len23": len(s) == 23,
                      "prefix8XD": s.startswith("8XD"), "suffixW54": s.endswith("W54"),
                      "charset": bool(re.fullmatch(r"[A-Z0-9]*", s)),
                      "is_answer": s == out["answer"]})
    out["graded"] = {"state": "file", "bytes": len(b), "head": b[:200].decode("utf-8", "backslashreplace"),
                     "tail": b[-80:].decode("utf-8", "backslashreplace"), "n_lines": len(lines),
                     "trailing_nl": b.endswith(b"\n"), "audit_first3": audit[:3], "audit_last2": audit[-2:],
                     "n_len23": sum(a["len23"] for a in audit),
                     "n_prefix": sum(a["prefix8XD"] for a in audit),
                     "n_suffix": sum(a["suffixW54"] for a in audit),
                     "n_charset_ok": sum(a["charset"] for a in audit),
                     "n_answer_lines": sum(a["is_answer"] for a in audit),
                     "n_violate_len23": sum(not a["len23"] for a in audit),
                     "n_violate_prefix": sum(not a["prefix8XD"] for a in audit),
                     "n_violate_suffix": sum(not a["suffixW54"] for a in audit),
                     "n_violate_charset": sum(not a["charset"] for a in audit),
                     "sha256": hashlib.sha256(b).hexdigest()}
walk = []
for root, dirs, files in os.walk("/app"):
    for d in sorted(dirs):
        walk.append("d " + os.path.join(root, d))
    for f in sorted(files):
        fp = os.path.join(root, f)
        walk.append("f %d %s" % (os.path.getsize(fp), fp))
out["tree_n"] = len(walk)
out["leftovers"] = [w for w in walk if re.search(r"launchcode|secret\.|logs\.txt|setup\.sh", w)]
out["oracle_art"] = [w for w in walk if re.search(r"window_|possible_seq|recovered_passwords", w)]
imgs = [os.path.join(root, f) for root, dirs, files in os.walk("/app") for f in files if f.endswith(".dat")]
out["images"] = []
for img in imgs:
    h = hashlib.sha256()
    data = open(img, "rb").read()
    h.update(data)
    out["images"].append({"path": img, "size": len(data), "sha256": h.hexdigest()[:32],
                          "at1MiB": data[1048576:1048592].hex(),
                          "at3MiB": data[3145728:3145744].hex()})
# what the leak channel yields
import subprocess as sp
r = sp.run(["grep", "-ao", "8XD[A-Z0-9]*", "/pub/test_outputs.py"], capture_output=True, text=True)
out["grep_hits"] = r.stdout.split()
print("DUMPJSON " + json.dumps(out, sort_keys=True))
'''

STAGE_SH = "bash -euo pipefail /seed.sh && bash -euo pipefail /recipe.sh"


def argv_for(work, cap):
    a = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
         "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev",
         "--tmpfs", "/tmp", "--ro-bind", str(work / "zeros.bin"), "/dev/urandom",
         "--bind", str(work / "app"), "/app", "--dir", "/pub"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            a += ["--symlink", os.readlink(link), link]
    for name in ("instruction.md", "test_outputs.py", "solve.sh"):
        a += ["--ro-bind", str(cap / name), "/pub/" + name]
    a += ["--ro-bind", str(work / "seed.sh"), "/seed.sh", "--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
          "--ro-bind", str(work / "dump.py"), "/dump.py", "--chdir", "/app"]
    return a


def run_case(case, root):
    work = pathlib.Path(tempfile.mkdtemp(prefix="insp-", dir=root))
    (work / "app").mkdir()
    (work / "zeros.bin").write_bytes(b"\0" * 65536)
    (work / "seed.sh").write_text((CAP / "setup.sh").read_text())
    (work / "recipe.sh").write_text(case.recipe or ":\n")
    (work / "dump.py").write_text(DUMP_PY)
    env = dict(PATHENV)
    st = subprocess.run(argv_for(work, CAP) + ["bash", "-c", STAGE_SH],
                        env=env, capture_output=True, text=True, timeout=900)
    dp = subprocess.run(argv_for(work, CAP) + ["python3", "/dump.py"],
                        env=env, capture_output=True, text=True, timeout=300)
    rec = {"cid": case.cid, "stage_rc": st.returncode,
           "stage_stderr": st.stderr[-400:], "dump_rc": dp.returncode, "dump_stderr": dp.stderr[-400:]}
    for l in dp.stdout.splitlines():
        if l.startswith("DUMPJSON "):
            rec["state"] = json.loads(l[9:])
    shutil.rmtree(work, ignore_errors=True)
    return rec


def main():
    root = sys.argv[1]
    pathlib.Path(root).mkdir(parents=True, exist_ok=True)
    for name, dig in PINS.items():
        import hashlib
        have = hashlib.sha256((CAP / name).read_bytes()).hexdigest()
        assert have == dig, (name, have)
    for c in prp.CASES:
        print(json.dumps(run_case(c, root), sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
