"""ReviewerR88a correctness attack on R88-C1: forge receipts without executing the grader.

All state lives under the seat scratch dir. The lane is only read (git clone --no-hardlinks).
Commits happen ONLY inside the scratch clone after its toplevel is verified.
"""
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r88/ReviewerR88a")
L = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
TIP = "7fcc680b86599eedd63e862a061848298428b3cc"
BASE = "801b903af6412cb424209a60b3a52e56c3532866"
FRONTIER = "da16ec39cf28d89b0a6a35ce8cacb630bad1de19"
C = S / "clone"
RECEIPT_PATH = "corpus/evidence/round88/fix-git-probe.txt"
CAP_PATH = "corpus/evidence/round52/graders/fix-git/tests/test_outputs.py"
FROZEN = [("exact", "P/P"), ("about-content-mismatch", "F/P"), ("layout-content-mismatch", "P/F"),
          ("both-content-mismatch", "F/F"), ("about-new-absent", "F/P"),
          ("trailing-whitespace-tolerance", "P/P"), ("about-new-is-dir", "E/P"),
          ("layout-old-is-dir", "P/E")]
SUBJECT_SHA = "a8a6f51eb0d7c4ebdf0813c8f0b645edf29c995f1f9faf2aca3886a6713043f3"


def git(repo, *args, env=None, binary=False, input_bytes=None):
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                          env=env, input=input_bytes)
    if not binary:
        proc.stdout = proc.stdout.decode("utf-8", errors="replace")
        proc.stderr = proc.stderr.decode("utf-8", errors="replace")
    return proc


# 1) clone the lane (read-only source) into scratch
if C.exists():
    shutil.rmtree(C)
r = subprocess.run(["git", "clone", "--no-hardlinks", "--quiet", str(L), str(C)],
                   capture_output=True, text=True)
print(f"clone rc={r.returncode} {r.stderr.strip()[:200]}")
tl = git(C, "rev-parse", "--show-toplevel")
assert tl.stdout.strip() == str(C), f"toplevel mismatch: {tl.stdout!r} {tl.stderr}"
for rev in (TIP, BASE, FRONTIER):
    assert git(C, "cat-file", "-e", rev + "^{commit}").returncode == 0, f"missing {rev}"
print("toplevel verified, all revisions present")

# 2) measured counter bytes + stamp inputs, all computed from tree objects (no probe run)
counter_src = git(C, "show", f"{TIP}:plans/round88_c1_replay.py").stdout
(S / "counter_tip.py").write_text(counter_src)
table_b = git(C, "show", f"{TIP}:plans/round88-cases.json", binary=True).stdout
tool_b = git(C, "show", f"{TIP}:plans/round88_fixgit_probe.py", binary=True).stdout
cap_b = git(C, "show", f"{TIP}:{CAP_PATH}", binary=True).stdout
table_sha = hashlib.sha256(table_b).hexdigest()
tool_sha = hashlib.sha256(tool_b).hexdigest()
cap_sha = hashlib.sha256(cap_b).hexdigest()
print(f"cap_sha==frozen {cap_sha == SUBJECT_SHA} table_sha={table_sha[:16]} tool_sha={tool_sha[:16]}")


def receipt(tip, cases=None, summary=("cases=8 legs=16 mismatches=0", "PREDICATE R88-PROBE pass"),
            exit_="0", worktree="clean"):
    lines = ["# tb2 fix-git grader probe", "MEMBER fix-git",
             f"SUBJECT_CAPTURE {CAP_PATH}", f"SUBJECT_SHA {cap_sha}",
             f"CASE_TABLE_SHA {table_sha}", "TOOL plans/round88_fixgit_probe.py",
             f"TOOL_SHA {tool_sha}", "HOST_PYTHON Python 3.14.8",
             "HOST_OPENSSL OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)",
             f"LANE_TIP {tip}", f"WORKTREE {worktree}",
             f"COMMAND python3 plans/round88_fixgit_probe.py --lane . --work {S / 'forge-work'}",
             f"EXIT {exit_}", "OBSERVATIONS_BEGIN"]
    cs = cases if cases is not None else [(cid, p, p) for cid, p in FROZEN]
    for cid, p, o in cs:
        lines.append(f"CASE {cid} predicted={p} observed={o}")
    lines += list(summary) + ["OBSERVATIONS_END", ""]
    return ("\n".join(lines)).encode()


IDENT = ["-c", "user.name=ReviewerR88a", "-c", "user.email=r88a@seat.invalid"]


def forge_commit(tag, blob, parent=TIP, root=False):
    """Replace the receipt blob in TIP's tree via plumbing; return the new commit sha."""
    env = {**os.environ, "GIT_INDEX_FILE": str(S / f"{tag}.index")}
    assert git(C, "read-tree", TIP + "^{tree}", env=env).returncode == 0
    b = git(C, "hash-object", "-w", "--stdin", env=env, binary=True, input_bytes=blob)
    assert b.returncode == 0, b.stderr
    assert git(C, "update-index", "--cacheinfo", f"100644,{b.stdout.decode().strip()},{RECEIPT_PATH}",
               env=env).returncode == 0
    t = git(C, "write-tree", env=env)
    assert t.returncode == 0, t.stderr
    tree = t.stdout.strip()
    argv = ["commit-tree", tree, "-m", f"r88a forge {tag}"]
    if not root:
        argv += ["-p", parent]
    c = git(C, *IDENT, *argv, env=env)
    assert c.returncode == 0, c.stderr
    return c.stdout.strip()


def run_counter(rev, label):
    p = subprocess.run([sys.executable, str(S / "counter_tip.py"), "--lane", str(C),
                        "--rev", rev, "--work", str(S / "counter-work")],
                       capture_output=True, text=True, timeout=900)
    body = p.stdout + (f"[stderr] {p.stderr.strip()}" if p.stderr.strip() else "") + f"\n[exit {p.returncode}]\n"
    (S / f"{label}.out.txt").write_text(body)
    print(f"\n=== {label} rev={rev[:12]} exit={p.returncode}")
    print("\n".join(p.stdout.splitlines()))
    return p.returncode


results = {}

# control 1: do-nothing BASE
results["base"] = run_counter(BASE, "01-base")

# control 2: genuine measurement at the tip
results["tip"] = run_counter(TIP, "02-tip")

# attack A: faithful forgery — receipt minted from frozen data + sha256 only, zero probe executions
blob = receipt(FRONTIER)
results["forge_faithful"] = run_counter(forge_commit("faithful", blob), "03-forge-faithful")

# attack B: same forgery but LANE_TIP names the round BASE (a much older ancestor)
results["forge_oldtip"] = run_counter(forge_commit("oldtip", receipt(BASE)), "04-forge-oldtip")

# control 3 (frozen forged-receipt control): LANE_TIP is a real commit that is NOT an ancestor
tip_tree_placeholder = forge_commit("sib0", receipt("placeholder"))
sib = git(C, *IDENT, "commit-tree", git(C, "rev-parse", TIP + "^{tree}").stdout.strip(),
          "-m", "r88a sibling root (not an ancestor)")
assert sib.returncode == 0, sib.stderr
SIB = sib.stdout.strip()
results["forge_nonancestor"] = run_counter(forge_commit("nonanc", receipt(SIB)), "05-forge-nonancestor")

# attack C: extra CASE line, summary kept at cases=8 (sneaky)
extra = [(c, p, p) for c, p in FROZEN] + [("exact", "P/P", "P/P")]
results["forge_extra"] = run_counter(forge_commit("extra", receipt(FRONTIER, cases=extra)), "06-forge-extra")

# attack D: reordered CASE lines (swap the two mismatch cases)
reord = list((c, p, p) for c, p in FROZEN)
reord[1], reord[2] = reord[2], reord[1]
results["forge_reorder"] = run_counter(forge_commit("reorder", receipt(FRONTIER, cases=reord)), "07-forge-reorder")

# attack E: duplicate case id (exact appears twice), summary kept at cases=8
dup = [(c, p, p) for c, p in FROZEN]
dup.insert(1, ("exact", "P/P", "P/P"))
results["forge_dup"] = run_counter(forge_commit("dup", receipt(FRONTIER, cases=dup)), "08-forge-dup")

print("\n==== SUMMARY ====")
for k, v in results.items():
    print(f"{k}: exit={v}")
