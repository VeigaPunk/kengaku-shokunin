#!/usr/bin/env python3
"""Build fixture commits in the seat scratch clone ($S/lane) — never in the lane.

Every fixture = T (09717e4) + exactly one edit, committed with a clone-local throwaway
identity after asserting `git rev-parse --show-toplevel` == the clone. Records revs to
$S/fixtures.json.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r96/MutTesterC1")
LANE = S / "lane"
T = "09717e49ff46fad5b255619d671aaaae52dfc180"
P1B = "e8a80c0e23f8a2b365756b4e971b4210afa3f829"
BASE = "45740a616028015b5dfcf9900753e3bb5e6fe689"
RECEIPT = "corpus/evidence/round96/merger-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
MEMBER = "multi-source-data-merger"
IDENT = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid"]


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(LANE), *args], capture_output=True, text=True)


def blob(rev: str, path: str) -> bytes:
    p = subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:{path}"], capture_output=True)
    if p.returncode != 0:
        sys.exit(f"blob {rev}:{path} failed: {p.stderr}")
    return p.stdout


top = git("rev-parse", "--show-toplevel").stdout.strip()
if top != str(LANE):
    sys.exit(f"toplevel {top} != {LANE}")

rev_set, base_set = set(), set()
led_t = json.loads(blob(T, LEDGER))
led_b = json.loads(blob(BASE, LEDGER))
for n, v in led_t["members"].items():
    if v.get("status") == "executed":
        rev_set.add(n)
for n, v in led_b["members"].items():
    if v.get("status") == "executed":
        base_set.add(n)
victim = sorted((base_set & rev_set) - {MEMBER})[0]
print(f"removal victim (executed at BASE and T): {victim}")
assert MEMBER not in base_set and MEMBER in rev_set


def reset_to_T() -> None:
    p = git("checkout", "-q", "-f", "--detach", T)
    if p.returncode != 0:
        sys.exit(f"checkout failed: {p.stderr}")
    p = git("clean", "-qfd")
    if p.returncode != 0:
        sys.exit(f"clean failed: {p.stderr}")


def commit(msg: str) -> str:
    p = git(*IDENT, "commit", "-q", "-a", "-m", msg)
    if p.returncode != 0:
        sys.exit(f"commit failed: {p.stderr}")
    return git("rev-parse", "HEAD").stdout.strip()


def edit(path: str, fn) -> None:
    f = LANE / path
    data = f.read_bytes()
    f.write_bytes(fn(data))


def sub(old: str, new: str):
    def fn(data: bytes) -> bytes:
        b_old, b_new = old.encode(), new.encode()
        if data.count(b_old) != 1:
            sys.exit(f"anchor count {data.count(b_old)} != 1: {old!r}")
        return data.replace(b_old, b_new, 1)
    return fn


def ledger_edit(fn_member):
    def fn(data: bytes) -> bytes:
        d = json.loads(data)
        fn_member(d["members"])
        out = json.dumps(d, indent=1) + "\n"
        return out.encode()
    return fn


fixtures = {"I0-T": T, "I1-P1b": P1B}

reset_to_T()
edit(RECEIPT, sub("CASE C04 predicted=P,P,P,1 observed=P,P,P,1 ok=True",
                  "CASE C04 predicted=P,P,P,1 observed=P,P,F,0 ok=True"))
fixtures["I2-forged-case"] = commit("fixture: receipt C04 observed P,P,P,1 -> P,P,F,0")

reset_to_T()
edit(LEDGER, ledger_edit(lambda m: m.update({"growth-member-r97": {
    "classes": ["file-artifact"], "evidence": "fixture growth member", "reason": "replayed",
    "status": "executed", "round": 97}})))
fixtures["I3-ledger-grow"] = commit("fixture: ledger growth member added (executed round 97)")

reset_to_T()
def _demote(m):
    m[victim]["status"] = "planned"
edit(LEDGER, ledger_edit(_demote))
fixtures["I4-ledger-remove"] = commit(f"fixture: executed member {victim} demoted to planned")

reset_to_T()
edit(LEDGER, ledger_edit(lambda m: m[MEMBER].update({"subject": "tb2-ledger"})))
fixtures["I5-ledger-legacy"] = commit("fixture: member subject tb2-header -> tb2-ledger")

reset_to_T()
edit(RECEIPT, sub("LANE_TIP be3ff962c3558ece7843119c1df26fa2cdbd313a",
                  "LANE_TIP 0000000000000000000000000000000000000000"))
fixtures["I6-receipt-lanetip"] = commit("fixture: receipt LANE_TIP -> all-zero sha")

reset_to_T()
edit(RECEIPT, sub("HOST_BASH GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)",
                  "HOST_BASH GNU bash, version 4.4.20(1)-release (x86_64-pc-linux-gnu)"))
fixtures["I7-receipt-hostbash"] = commit("fixture: receipt HOST_BASH -> old bash")

reset_to_T()
edit(RECEIPT, sub("GRADER_SIDE python,pandas,pyarrow,numpy 3.13.16 2.3.3 22.0.0 2.5.4",
                  "GRADER_SIDE python,pandas,pyarrow,numpy 3.13.16 2.3.3 21.0.0 2.5.4"))
fixtures["I8-receipt-graderside"] = commit("fixture: receipt GRADER_SIDE pyarrow 22.0.0 -> 21.0.0")

reset_to_T()
CAPDIR = "corpus/evidence/round96/graders/multi-source-data-merger"
edit(CAPDIR + "/environment/Dockerfile", lambda d: d + b"\n# fixture-tamper\n")
fixtures["I9-cap-dockerfile"] = commit("fixture: captured Dockerfile tampered (pin 4 of 7)")

reset_to_T()
PROBE = "plans/round96_merger_probe.py"
edit(PROBE, lambda d: d + b"\n# fixture-cosmetic\n")
new_probe_sha = hashlib.sha256((LANE / PROBE).read_bytes()).hexdigest()
edit(RECEIPT, sub(f"TOOL_SHA {hashlib.sha256(blob(T, PROBE)).hexdigest()}", f"TOOL_SHA {new_probe_sha}"))
fixtures["I10-probe-stamped"] = commit("fixture: probe cosmetic edit + receipt TOOL_SHA restamped to match")

reset_to_T()
TABLE = "plans/round96-cases.json"
edit(TABLE, sub('"positive control: the captured solve.sh run unmodified in the image-equivalent environment (python 3.11, pandas 2.2.3, pyarrow 17.0.0) writes both files"',
                '"positive control: the captured solve.sh run unmodified in the image-equivalent environment (python 3.11, pandas 2.2.3, pyarrow 17.0.0) writes both files (fixture)"'))
new_table_sha = hashlib.sha256((LANE / TABLE).read_bytes()).hexdigest()
edit(RECEIPT, sub(f"CASE_TABLE_SHA {hashlib.sha256(blob(T, TABLE)).hexdigest()}", f"CASE_TABLE_SHA {new_table_sha}"))
fixtures["I11-table-stamped"] = commit("fixture: case table why-edit + receipt CASE_TABLE_SHA restamped to match")

reset_to_T()
(LANE / RECEIPT).unlink()
p = git(*IDENT, "commit", "-q", "-a", "-m", "fixture: receipt deleted from tree")
if p.returncode != 0:
    sys.exit(f"commit failed: {p.stderr}")
fixtures["I12-receipt-deleted"] = git("rev-parse", "HEAD").stdout.strip()

reset_to_T()
edit(LEDGER, ledger_edit(lambda m: m[MEMBER].update({"round": 95})))
fixtures["I13-ledger-round95"] = commit("fixture: member round 96 -> 95")

reset_to_T()
edit(RECEIPT, sub("CASE C17 predicted=P,P,F,0 observed=P,P,F,0 ok=True\n", ""))
fixtures["I14-receipt-missing-case"] = commit("fixture: receipt CASE C17 line removed")

(S / "fixtures.json").write_text(json.dumps(fixtures, indent=1))
print(json.dumps(fixtures, indent=1))
print(f"clone HEAD: {git('rev-parse', 'HEAD').stdout.strip()} worktree clean: {git('status', '--porcelain').stdout!r}")
