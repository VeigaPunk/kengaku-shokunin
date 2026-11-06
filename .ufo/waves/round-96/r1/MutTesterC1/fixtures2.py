#!/usr/bin/env python3
"""Round-96 C1 mutation seat: additional single-edit fixture commits on T in the scratch clone.

Every fixture = T (09717e4) + exactly one edit, committed with a clone-local throwaway identity
after asserting `git rev-parse --show-toplevel` == the clone. Never touches the lane.
Appends to $S/fixtures.json.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r96/MutTesterC1")
LANE = S / "lane"
T = "09717e49ff46fad5b255619d671aaaae52dfc180"
RECEIPT = "corpus/evidence/round96/merger-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
MEMBER = "multi-source-data-merger"
IDENT = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid"]


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(LANE), *args], capture_output=True, text=True)


top = git("rev-parse", "--show-toplevel").stdout.strip()
if top != str(LANE):
    sys.exit(f"toplevel {top} != {LANE}")


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
        return (json.dumps(d, indent=1) + "\n").encode()
    return fn


fixtures = json.loads((S / "fixtures.json").read_text())
BOGUS = "1" * 64

reset_to_T()
edit(RECEIPT, sub("SUBJECT_SHA a070888930cf829aeca039771260b1386bda990ea805f313468d381ba3608ca5",
                  "SUBJECT_SHA " + BOGUS))
fixtures["I15-receipt-subjectsha"] = commit("fixture: receipt SUBJECT_SHA -> wrong sha")

reset_to_T()
edit(RECEIPT, sub("TEST_SH_SHA d5a00e64413c0e1ae452f38a1aa1a47c3ed7b4416bbfccae1a4c053025a336d1",
                  "TEST_SH_SHA " + BOGUS))
fixtures["I16-receipt-testsh"] = commit("fixture: receipt TEST_SH_SHA -> wrong sha")

reset_to_T()
edit(RECEIPT, sub("SOLVE_SHA 1b3d0d50e31930d042495d48f4c8e95f1a9c1a979c803b7f7cec651322537e1e",
                  "SOLVE_SHA " + BOGUS))
fixtures["I17-receipt-solvesha"] = commit("fixture: receipt SOLVE_SHA -> wrong sha")

reset_to_T()
edit(LEDGER, ledger_edit(lambda m: m[MEMBER].update({"round": 97})))
fixtures["I18-ledger-round97"] = commit("fixture: member round 96 -> 97")

reset_to_T()
edit(LEDGER, ledger_edit(lambda m: m[MEMBER].update(
    {"classes": ["file-artifact", "serialization-schema", "extra-class"]})))
fixtures["I19-ledger-classes"] = commit("fixture: member classes gain extra-class")

reset_to_T()
edit(LEDGER, ledger_edit(lambda m: m[MEMBER].update(
    {"receipt": "corpus/evidence/round96/other-receipt.txt"})))
fixtures["I20-ledger-receiptpath"] = commit("fixture: member receipt path -> other-receipt.txt")

reset_to_T()
edit(LEDGER, ledger_edit(lambda m: m[MEMBER].update({"verdict": "tests"})))
fixtures["I21-ledger-verdict"] = commit("fixture: member verdict cases -> tests")

reset_to_T()
edit(RECEIPT, sub("CASE C17 predicted=P,P,F,0 observed=P,P,F,0 ok=True",
                  "CASE C01 predicted=P,P,P,1 observed=P,P,P,1 ok=True"))
fixtures["I22-receipt-dup-case"] = commit("fixture: receipt C17 line replaced by duplicate C01 (count kept)")

reset_to_T()
edit(RECEIPT, sub("OBSERVATIONS_END", "NOTE fixture non-case observation line\nOBSERVATIONS_END"))
fixtures["I23-receipt-obs-note"] = commit("fixture: non-CASE line inserted inside the observation block")

reset_to_T()
edit(RECEIPT, sub("CASE_TABLE_SHA b5efb7b004730ebd6756c32471fccc84bb91c9833faf82be000a894adf3d5354",
                  "CASE_TABLE_SHA " + BOGUS))
fixtures["I24-receipt-tablesha"] = commit("fixture: receipt CASE_TABLE_SHA -> wrong sha (table unchanged)")

reset_to_T()
edit(RECEIPT, sub("ENV_SIDE python,pandas,pyarrow,numpy 3.11.17 2.2.3 17.0.0 2.4.6",
                  "ENV_SIDE python,pandas,pyarrow,numpy 3.11.17 2.2.3 17.0.0 9.9.9"))
fixtures["I25-receipt-envside"] = commit("fixture: receipt ENV_SIDE numpy version forged")

reset_to_T()
edit(RECEIPT, sub("LANE_TIP be3ff962c3558ece7843119c1df26fa2cdbd313a\n", ""))
fixtures["I26-receipt-notip"] = commit("fixture: receipt LANE_TIP line removed")

reset_to_T()
(S / "fixtures.json").write_text(json.dumps(fixtures, indent=1))
print(json.dumps(fixtures, indent=1))
print(f"clone HEAD: {git('rev-parse', 'HEAD').stdout.strip()} clean: {git('status', '--porcelain').stdout!r}")
