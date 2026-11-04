#!/usr/bin/env python3
"""R81-C1 repair driver — mint located receipts for the two new population members.

Unlike the round-80 driver this mints a *first* receipt: there is no historical receipt to cite.
The subject is the committed round-52 grader capture, sha256-pinned; the environment the replay
depends on is pinned in the stamp (`HOST_PYTHON`, `HOST_OPENSSL`) so a later replay on a different
interpreter or openssl is visibly not the same measurement.

Every probe in `plans/round81_probes.json` runs first; the worktree is re-checked clean before any
receipt is written, `LANE_TIP` is stamped from the executed checkout's `HEAD`, and
`MINTED_BY_SHA` pins this driver's own bytes at that checkout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

TABLE = "plans/round81_probes.json"
LEDGER = "plans/grader-population-ledger.json"
GRADERS = "corpus/evidence/round52/graders"
EVID = "corpus/evidence/round81"
MINTED_BY = "plans/round81_c1_remint.py"
OBS = (r"^CASE ", r"^case=", r"^cases=", r"^MISMATCH ", r"^OBSERVED-U ", r"^VECTOR ",
       r"^PREDICATE R\d+-C\d+ (?:pass|fail)")
FORMS = (("predicate", r"^PREDICATE R\d+-C\d+ pass"), ("vectors", r"^VECTOR "),
         ("cases", r"^(?:CASE |case=)"))


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def obs_lines(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if any(re.match(p, ln) for p in OBS)]


def verdict_form(text: str) -> str:
    for name, pattern in FORMS:
        if re.search(pattern, text, re.M):
            return name
    return "cases"


def host_values(python: str) -> tuple[str, str]:
    py = subprocess.run([python, "-V"], capture_output=True, text=True)
    py_v = ((py.stdout or "") + (py.stderr or "")).strip().splitlines()
    ossl = subprocess.run(["openssl", "version"], capture_output=True, text=True)
    ossl_v = (ossl.stdout or "").strip() if ossl.returncode == 0 else "absent"
    return (py_v[0] if py_v else "unknown"), (ossl_v or "absent")


def render(spec: dict, member: str, work: Path, python: str) -> tuple[list[str], str]:
    w = work / f"{member}.work"
    w.mkdir(parents=True, exist_ok=True)
    out = work / f"{member}.stdout.txt"
    argv = [a.replace("{work}", str(w)).replace("{out}", str(out)).replace("{member}", member)
            for a in spec["argv"]]
    cmd = [python, spec["tool"]] + argv
    return cmd, shlex.join(cmd)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", default="/fast/scratch/hyaku/kengaku-r81/mint")
    ap.add_argument("--python", default=sys.executable)
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)

    status = git(lane, "status", "--porcelain").stdout.strip()
    if status:
        print(f"SETUP worktree not clean ({len(status.splitlines())} paths); run in a fresh clone")
        return 2
    head = git(lane, "rev-parse", "HEAD").stdout.strip()
    if not head:
        print("SETUP unresolved HEAD")
        return 2
    driver_sha = sha256((lane / MINTED_BY).read_bytes())
    host_py, host_ossl = host_values(a.python)
    table = json.loads((lane / TABLE).read_text())["members"]
    doc = json.loads((lane / LEDGER).read_text())
    rows = doc["members"]
    staged: list[tuple[str, str]] = []
    failed = 0
    for m in sorted(table):
        spec = table[m]
        capture = f"{GRADERS}/{m}/tests/test_outputs.py"
        cap_bytes = (lane / capture).read_bytes()
        tool_bytes = (lane / spec["tool"]).read_bytes()
        cmd, command = render(spec, m, work, a.python)
        try:
            proc = subprocess.run(cmd, cwd=str(lane), capture_output=True, text=True,
                                  timeout=int(spec.get("timeout", 300)))
        except subprocess.TimeoutExpired:
            print(f"MINT-FAIL {m} timeout")
            failed += 1
            continue
        if proc.returncode != 0:
            tail = (proc.stderr or "").strip().splitlines()[-1:]
            print(f"MINT-FAIL {m} rc={proc.returncode} stderr={tail}")
            failed += 1
            continue
        obs = obs_lines(proc.stdout)
        if not obs:
            print(f"MINT-FAIL {m} no observations on stdout")
            failed += 1
            continue
        if "mismatches=0" not in proc.stdout and "PREDICATE" not in proc.stdout:
            print(f"MINT-FAIL {m} probe reported a mismatch or no predicate")
            failed += 1
            continue
        text = (
            f"# tb2 {m} grader probe (round 81)\n"
            f"MEMBER {m}\n"
            f"SUBJECT_CAPTURE {capture}\n"
            f"SUBJECT_SHA {sha256(cap_bytes)}\n"
            f"TOOL {spec['tool']}\n"
            f"TOOL_SHA {sha256(tool_bytes)}\n"
            f"HOST_PYTHON {host_py}\n"
            f"HOST_OPENSSL {host_ossl}\n"
            f"LANE_TIP {head}\n"
            f"WORKTREE clean\n"
            f"COMMAND {command}\n"
            f"EXIT 0\n"
            f"MINTED_BY {MINTED_BY}\n"
            f"MINTED_BY_SHA {driver_sha}\n"
            f"OBSERVATIONS_BEGIN\n"
            + "\n".join(ln for ln in proc.stdout.rstrip("\n").splitlines()
                        if not re.match(r"^REV [0-9a-f]{7,40}\s*$", ln)) + "\n"
            + f"OBSERVATIONS_END\n"
        )
        row = rows.get(m)
        if not isinstance(row, dict):
            print(f"MINT-FAIL {m} ledger row absent")
            failed += 1
            continue
        for key in ("reason", "evidence", "instrument", "debt"):
            row.pop(key, None)
        row.update({"status": "executed", "round": 81,
                    "receipt": f"{EVID}/{m}-probe.txt", "subject": "tb2-header",
                    "verdict": verdict_form(proc.stdout)})
        staged.append((m, text))
        print(f"MINT {m} rc=0 obs={len(obs)} verdict={verdict_form(proc.stdout)}")
    after = git(lane, "status", "--porcelain").stdout.strip()
    if after:
        print(f"SETUP worktree not clean after the probe runs ({len(after.splitlines())} paths); "
              f"nothing written")
        return 2
    (lane / EVID).mkdir(parents=True, exist_ok=True)
    for m, text in staged:
        (lane / f"{EVID}/{m}-probe.txt").write_text(text)
    (lane / LEDGER).write_text(json.dumps(doc, indent=1) + "\n")
    print(f"MINT minted={len(staged)} failed={failed}")
    return 0 if failed == 0 and len(staged) == len(table) else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
