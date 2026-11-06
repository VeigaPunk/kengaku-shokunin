#!/usr/bin/env python3
"""MutTesterC1 (round 95) held-out forgery fixtures for plans/round95_c1_replay.py.

Usage: build_fixtures.py <lane> <T> <scratch dir>
Every fixture is a `git clone --shared <lane>` detached at T (or a squashed repo for FX-D) plus ONE
forging commit; every git call is `-C <fixture>` with a throwaway identity and a toplevel assertion.
Probe-regenerated receipts run plans/round95_vuln_probe.py from the fixture itself.
Fixtures live in scratch only; the outputs of the counters run against them are in receipts/matrix/.
"""
import io
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

IDENT = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
         "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]
RECEIPT = "corpus/evidence/round95/vuln-probe.txt"


def gitx(d: Path, *args: str, check: bool = True) -> str:
    top = subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert Path(top).resolve() == Path(d).resolve(), (top, str(d))
    p = subprocess.run(["git", "-C", str(d), *IDENT, *args], capture_output=True, text=True)
    if check and p.returncode:
        raise RuntimeError(f"{args}: {p.stderr}")
    return p.stdout.strip()


def commit(d: Path, msg: str) -> str:
    gitx(d, "add", "-A")
    gitx(d, "commit", "-q", "--allow-empty", "-m", msg)
    return gitx(d, "rev-parse", "HEAD")


def main() -> int:
    lane, T, fxr = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    shutil.rmtree(fxr, ignore_errors=True)
    fxr.mkdir(parents=True)

    def new_clone(name: str) -> Path:
        d = fxr / name
        subprocess.run(["git", "clone", "-q", "--shared", str(lane), str(d)], check=True)
        gitx(d, "checkout", "-q", "--detach", T)
        return d

    def probe_out(d: Path, name: str) -> tuple[int, str]:
        w = fxr / ("probe-" + name)
        p = subprocess.run([sys.executable, "-I", "-B", str(d / "plans/round95_vuln_probe.py"), "--lane", str(d), "--work", str(w)],
                           capture_output=True, text=True, timeout=1800)
        shutil.rmtree(w, ignore_errors=True)
        assert p.returncode in (0, 1), (name, p.returncode, p.stderr[-400:])
        return p.returncode, p.stdout

    def forge_table(d: Path, name: str) -> str:
        # C02 runs the captured solve.sh (bottle=solve); its predicted vector is rewritten to what that run observes
        tbl = json.loads((d / "plans/round95-cases.json").read_text())
        for c in tbl["cases"]:
            if c["id"] == "C02":
                c["bottle"] = "solve"
        (d / "plans/round95-cases.json").write_text(json.dumps(tbl, indent=2) + "\n")
        _, out = probe_out(d, name)
        obs = re.search(r"^CASE C02 .*?observed=(\S+)", out, re.M).group(1)
        for c in tbl["cases"]:
            if c["id"] == "C02":
                c["predicted"] = obs
        (d / "plans/round95-cases.json").write_text(json.dumps(tbl, indent=2) + "\n")
        rc, out = probe_out(d, name)
        assert rc == 0, "forged table still mismatches"
        return out

    trec = (lane / RECEIPT).read_text()
    fix = {}
    # FX-A: count-preserving hiding: C02 line replaced by a duplicate of the C01 line
    d = new_clone("A-dup")
    lines = trec.splitlines(keepends=True)
    c01 = next(x for x in lines if x.startswith("CASE C01 "))
    (d / RECEIPT).write_text("".join(c01 if x.startswith("CASE C02 ") else x for x in lines))
    fix["A-dup"] = commit(d, "fx A")
    # FX-B1: table forged (C02 predicted/bottle), receipt regenerated, claims untouched
    d = new_clone("B1-table")
    (d / RECEIPT).write_text(forge_table(d, "B1"))
    fix["B1-table"] = commit(d, "fx B1")
    # FX-B2: as B1 plus the claims frozen row rewritten at the forged revision
    d = new_clone("B2-table-claims")
    (d / RECEIPT).write_text(forge_table(d, "B2"))
    new_sha = hashlib.sha256((d / "plans/round95-cases.json").read_bytes()).hexdigest()
    claims = (d / "plans/round-95-claims.md").read_text()
    old_sha = next(x.split()[0] for x in claims.splitlines() if x.endswith("plans/round95-cases.json"))
    (d / "plans/round-95-claims.md").write_text(claims.replace(old_sha, new_sha))
    fix["B2-table-claims"] = commit(d, "fx B2")
    # FX-C: same-class member swap (configure-git-webserver unflipped, mailman flipped)
    d = new_clone("C-swap")
    led = json.loads((d / "plans/grader-population-ledger.json").read_text())
    led["members"]["configure-git-webserver"]["status"] = "unexecuted"
    led["members"]["mailman"]["status"] = "executed"
    (d / "plans/grader-population-ledger.json").write_text(json.dumps(led, indent=1) + "\n")
    fix["C-swap"] = commit(d, "fx C")
    # FX-D: squashed repo, no BASE history; receipt regenerated at the squash commit
    d = fxr / "D-squash"
    d.mkdir()
    subprocess.run(["git", "init", "-q", str(d)], check=True)
    arch = subprocess.run(["git", "-C", str(lane), "archive", T], capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(arch)) as tf:
        tf.extractall(d, filter="data")
    commit(d, "fx D tree")
    _, out = probe_out(d, "D")
    (d / RECEIPT).write_text(out)
    fix["D-squash"] = commit(d, "fx D receipt")
    # FX-E: UPSTREAM_BOTTLE_SHA header forged
    d = new_clone("E-upstream")
    (d / RECEIPT).write_text(re.sub(r"^UPSTREAM_BOTTLE_SHA .*$", "UPSTREAM_BOTTLE_SHA " + "0" * 64, trec, flags=re.M))
    fix["E-upstream"] = commit(d, "fx E")
    # FX-F: a BASE-executed member's class list tampered (file-artifact removed from chess-best-move)
    d = new_clone("F-classes-other")
    led = json.loads((d / "plans/grader-population-ledger.json").read_text())
    led["members"]["chess-best-move"]["classes"] = []
    (d / "plans/grader-population-ledger.json").write_text(json.dumps(led, indent=1) + "\n")
    fix["F-classes-other"] = commit(d, "fx F")
    # FX-G: the member's own class list gains an unlisted class (cell counts unchanged)
    d = new_clone("G-member-classes")
    led = json.loads((d / "plans/grader-population-ledger.json").read_text())
    led["members"]["fix-code-vulnerability"]["classes"] = ["file-artifact", "serialization-schema", "stdout-inspection"]
    (d / "plans/grader-population-ledger.json").write_text(json.dumps(led, indent=1) + "\n")
    fix["G-member-classes"] = commit(d, "fx G")
    # FX-H: C05 consistent lie (predicted and observed rewritten to C02's receipt vector)
    d = new_clone("H-c05-lie")
    c02 = next(x for x in trec.splitlines() if x.startswith("CASE C02 "))
    pv = re.search(r"predicted=(\S+)", c02).group(1)
    ov = re.search(r"observed=(\S+)", c02).group(1)
    (d / RECEIPT).write_text("".join(f"CASE C05 predicted={pv} observed={ov} ok=True\n" if x.startswith("CASE C05 ") else x
                                     for x in trec.splitlines(keepends=True)))
    fix["H-c05-lie"] = commit(d, "fx H")
    # FX-I/J/K: one host stamp forged per fixture
    for name, key, val in [("I-host-python", "HOST_PYTHON", "Python 3.13.0"),
                           ("J-host-bash", "HOST_BASH", "GNU bash, version 5.2.0"),
                           ("K-host-sed", "HOST_SED", "/usr/bin/sed (GNU sed) 4.8")]:
        d = new_clone(name)
        (d / RECEIPT).write_text(re.sub(rf"^{key} .*$", f"{key} {val}", trec, flags=re.M))
        fix[name] = commit(d, name)
    # FX-L: capture solve.sh tampered (receipt untouched)
    d = new_clone("L-solve-tamper")
    p = d / "corpus/evidence/round95/graders/fix-code-vulnerability/solution/solve.sh"
    p.write_text(p.read_text() + "\n# tampered\n")
    fix["L-solve-tamper"] = commit(d, "fx L")
    # FX-M: a duplicate extra CASE line appended inside the observation block
    d = new_clone("M-extra-line")
    (d / RECEIPT).write_text(trec.replace("OBSERVATIONS_END",
                                          "CASE C01 predicted=P,P,P,P,P,P,/app/bottle.py observed=P,P,P,P,P,P,/app/bottle.py ok=True\nOBSERVATIONS_END", 1))
    fix["M-extra-line"] = commit(d, "fx M")
    for k, v in fix.items():
        print(k, v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
