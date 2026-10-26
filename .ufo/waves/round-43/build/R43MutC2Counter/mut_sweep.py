#!/usr/bin/env python3
"""R43MutC2Counter mutant sweep: single-line mutants of the C2 counter's v10/v9 points,
each run against the frozen filler/informed/content triple (c2_filler_control.py).
The counter copy inside the scratch clone is patched, run, and restored byte-exactly.
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r43/R43MutC2Counter")
LANE = S / "lane"
CTRL = LANE / ".ufo/waves/round-43/claims/c2_filler_control.py"
COUNTER = LANE / "plans/round43_c2_verify.py"
PRISTINE = (S / "pristine_counter.py").read_bytes()
PRISTINE_SHA = hashlib.sha256(PRISTINE).hexdigest()
EXPECT = {"filler": (False, False), "informed": (True, False), "content": (True, True)}

MUTANTS = [
    ("M01", "v10", "DECISIVE lookup: default widened for off-map captures",
     r"allowed = DECISIVE.get(cid, {}).get(cap, ())",
     r"allowed = DECISIVE.get(cid, {}).get(cap, range(1, 400))"),
    ("M02", "v10", "int(line) not in allowed: weakened to never flag",
     r"if int(line) not in allowed:",
     r"if int(line) not in allowed and False:"),
    ("M03", "v10", "capture pin: sha256 clause dropped",
     r"if cap not in CAPTURES or sha256(capdir / cap) != CAPTURES[cap]:",
     r"if cap not in CAPTURES:"),
    ("M04", "v10", "capture pin: digest comparison inverted",
     r"!= CAPTURES[cap]:",
     r"== CAPTURES[cap]:"),
    ("M05", "v10", "norm made identity (no whitespace normalisation)",
     r'return " ".join(t.split())',
     r"return t"),
    ("M06", "v10", "two-word quote floor weakened to no-op",
     r"len(q.split()) < 2",
     r"len(q.split()) < 0"),
    ("M07", "v10", "ids-equal check: empty-receipt guard dropped",
     r"!= want or not want:",
     r"!= want:"),
    ("M08", "v10", "MECH_ROW: trailing pipe made optional",
     r'“(.+?)”\s*\|\s*$")',
     r'“(.+?)”\s*\|?\s*$")'),
    ("M09", "v10", "MECH_ROW: dash dropped from case-id class",
     r"MECH_ROW = re.compile(r" + '"^' + r"\|" + r"\s*`([a-z0-9_-]+)`",
     r"MECH_ROW = re.compile(r" + '"^' + r"\|" + r"\s*`([a-z0-9_]+)`"),
    ("M10", "v9", "CASE_ROW: dash dropped from case-id class",
     r"CASE_ROW = re.compile(r" + '"^' + r"\|" + r"\s*`([a-z0-9_-]+)`",
     r"CASE_ROW = re.compile(r" + '"^' + r"\|" + r"\s*`([a-z0-9_]+)`"),
    ("M11", "v9", "CASE_ROW: [PF] -> [pF] (P rows stop matching)",
     r"([a-z0-9_-]+)`\s*\|\s*([PF])",
     r"([a-z0-9_-]+)`\s*\|\s*([pF])"),
    ("M12", "v9", "CASE_ROW: (pass|fail) -> (pass|fai1)",
     r"([PF])\s*\|\s*(pass|fail)",
     r"([PF])\s*\|\s*(pass|fai1)"),
    ("M13", "v9", "CASE_ROW: trailing pipe made optional",
     r'.*\|\s*$")',
     r'.*\|?\s*$")'),
]


def run_control(tag):
    work = S / f"w_{tag}"
    work.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(LANE / "plans/__pycache__", ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, str(CTRL), "--lane", str(LANE), "--work", str(work)],
                       capture_output=True, text=True, timeout=600, env=env)
    res = {}
    for l in r.stdout.splitlines():
        p = l.split()
        if len(p) >= 4 and p[0] == "CONTROL" and p[1] in EXPECT and p[2] in ("V9", "V10"):
            res[(p[1], p[2])] = (p[3] == "ok", " ".join(p[4:]))
    return r.returncode, r.stdout, r.stderr, res


def main():
    assert hashlib.sha256(COUNTER.read_bytes()).hexdigest() == PRISTINE_SHA, "clone counter not pristine"
    rows = []
    for mid, leg, what, old, new in MUTANTS:
        text = PRISTINE.decode()
        n = text.count(old)
        assert n == 1, f"{mid}: anchor occurs {n} times, need 1: {old!r}"
        mutated = text.replace(old, new).encode()
        assert mutated != PRISTINE
        COUNTER.write_bytes(mutated)
        mut_sha = hashlib.sha256(COUNTER.read_bytes()).hexdigest()
        try:
            rc, out, err, res = run_control(mid)
        finally:
            COUNTER.write_bytes(PRISTINE)
        restored = hashlib.sha256(COUNTER.read_bytes()).hexdigest()
        assert restored == PRISTINE_SHA, f"{mid}: restore failed"
        flips = []
        for kind, exp in EXPECT.items():
            got = (res.get((kind, "V9"), (None, ""))[0], res.get((kind, "V10"), (None, ""))[0])
            if got != exp:
                flips.append(f"{kind}:V{'9' if got[0] != exp[0] else '10'}")
        verdict = "CAUGHT " + ",".join(flips) if flips else "SURVIVED"
        rows.append({"id": mid, "leg": leg, "what": what, "mut_sha": mut_sha[:16],
                     "rc": rc, "verdict": verdict,
                     "detail": {f"{k[0]}:{k[1]}": [v[0], v[1]] for k, v in res.items()}})
        print(f"== {mid} [{leg}] {what}")
        for kind in ("filler", "informed", "content"):
            v9 = res.get((kind, "V9"), (None, "MISSING"))
            v10 = res.get((kind, "V10"), (None, "MISSING"))
            print(f"   {kind:9s} V9 {'ok ' if v9[0] else 'DEF'} V10 {'ok ' if v10[0] else 'DEF'}"
                  f"  | V9 {v9[1][:60]} | V10 {v10[1][:60]}")
        print(f"   rc={rc} mutant_sha256={mut_sha[:16]} restored={restored[:16]} -> {verdict}")
    killed = sum(1 for r in rows if r["verdict"] != "SURVIVED")
    print(f"SWEEP total={len(rows)} caught={killed} survived={len(rows) - killed}")
    (S / "sweep_results.json").write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
