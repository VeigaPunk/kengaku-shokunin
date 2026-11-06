#!/usr/bin/env python3
"""R100 C1 mutation battery (seat MutC1). Fixture-only; never touches the lane.

Each mutant: clone --shared at P2 (the last commit before F, so no plans/round-100-claims.md in
history), apply the instrument mutation, commit a fixture-only claims file whose tables are computed
from the bytes the mutant tree will carry (so L4/L8/L11/L12 do not trivially kill counter mutants),
then commit the T tree with the tree mutation on top, then run the counter from the fixture root.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
S = Path("/fast/scratch/hyaku/kengaku-r100/MutC1")
G = S / "G"
T = "dbe0cefa607cf57f7f58346fce64bcc127144ca0"
BASE = "7846037679de77d050141c785996471801e5a19a"
P2 = "5220b71d337a3703eaba4cdf6b85eaf343497ae0"
CLAIMS = "plans/round-100-claims.md"
RECEIPT = "corpus/evidence/round100/fdp-probe.txt"
COUNTER = "plans/round100_c1_replay.py"
PROBE = "plans/round100_fdp_probe.py"
TABLE = "plans/round100-cases.json"
GATE = "plans/anchor_digest_check.py"
LINE_GATE = "plans/anchor_line_check.py"
PROV = ["corpus/evidence/round52/PROVENANCE.md", "corpus/evidence/round58/PROVENANCE.md",
        "corpus/evidence/round94/PROVENANCE.md"]
CAND = ["SKILL.md", "plans/grader-population-ledger.json", "corpus/SOURCES.md"] + PROV
INSTR = [PROBE, TABLE, COUNTER, "plans/round100_c2_rowcensus_bind.py", "plans/round100_provenance_build.py",
         "plans/round100_prefreeze_check.py", GATE, LINE_GATE, ".ufo/waves/round-100/L1/c2-live-refetch.txt",
         "corpus/evidence/round100/tb2-financial-document-processor/SHA256SUMS",
         "corpus/evidence/round100/tb2-financial-document-processor/test_outputs.py",
         "corpus/evidence/round100/tb2-financial-document-processor/test.sh",
         "corpus/evidence/round100/tb2-financial-document-processor/solve.sh",
         "corpus/evidence/round100/fdp-solution/SHA256SUMS",
         "corpus/evidence/round100/fdp-solution/placement.tsv",
         "corpus/evidence/round100/fdp-solution/summary.csv"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit(f"git {args} in {root} rc={p.returncode}: {p.stderr[-500:]}")
    return p


def tbytes(path: str) -> bytes:
    return git(LANE, "show", f"{T}:{path}").stdout.encode()


def sub1(text: str, old: str, new: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"mutation anchor count {n} for {old!r}")
    return text.replace(old, new, 1)


# ---------------- mutation primitives ----------------
def counter_edit(old: str, new: str):
    def f(text: str) -> str:
        return sub1(text, old, new)
    return f


def ledger_edit(fn):
    def f(data: bytes) -> bytes:
        d = json.loads(data.decode())
        fn(d)
        return (json.dumps(d, indent=1, ensure_ascii=False) + "\n").encode()
    return f


def sources_edit(fn):
    def f(data: bytes) -> bytes:
        return fn(data.decode()).encode()
    return f


def receipt_edit(fn):
    def f(data: bytes) -> bytes:
        return fn(data.decode()).encode()
    return f


def detail_forge(text: str) -> str:
    out, n = re.subn(r"(?m)^(DETAIL C03 .*?)summary=[0-9a-f]{16}",
                     r"\1summary=0000000000000000", text, count=1)
    assert n == 1, "DETAIL C03 anchor"
    return out


def drop_case(text: str, cid: str) -> str:
    lines = text.split("\n")
    out = [l for l in lines if not (l.startswith(f"CASE {cid} ") or l.startswith(f"DETAIL {cid} "))]
    assert len(lines) - len(out) == 2
    return "\n".join(out)


def flip_observed(text: str) -> str:
    old = "CASE C01 predicted=P,P,P,P,P,P,P,1 observed=P,P,P,P,P,P,P,1 ok=True"
    new = "CASE C01 predicted=P,P,P,P,P,P,P,1 observed=F,P,P,P,P,P,P,1 ok=False"
    return sub1(text, old, new)


def flip_consistent(text: str) -> str:
    old = "CASE C01 predicted=P,P,P,P,P,P,P,1 observed=P,P,P,P,P,P,P,1 ok=True"
    new = "CASE C01 predicted=F,P,P,P,P,P,P,1 observed=F,P,P,P,P,P,P,1 ok=False"
    return sub1(text, old, new)


def field(text: str, key: str, value: str) -> str:
    return re.sub(rf"(?m)^{key} .*$", f"{key} {value}", text, count=1)


def extra_row(text: str) -> str:
    row = [l for l in text.split("\n") if l.startswith("| S348 ")][0]
    return text.replace(row, row + "\n" + row.replace("| S348 ", "| S350 ", 1), 1)


def drop_row(text: str, rid: str) -> str:
    lines = text.split("\n")
    out = [l for l in lines if not l.startswith(f"| {rid} ")]
    assert len(lines) - len(out) == 1
    return "\n".join(out)


def typed_words(text: str) -> str:
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("| S343 ")]
    assert len(idx) == 1, idx
    old = lines[idx[0]]
    assert "(2 words)" in old
    lines[idx[0]] = old.replace("(2 words)", "(3 words)", 1)
    return "\n".join(lines)


def url_edit(text: str) -> str:
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("| S342 ")]
    assert len(idx) == 1, idx
    old = lines[idx[0]]
    new = old.replace("financial-document-processor/tests/test_outputs.py",
                      "financial-document-processor/tests/test_outputs_absent.py", 1)
    assert new != old
    lines[idx[0]] = new
    return "\n".join(lines)


TABLE_STRAY = (json.dumps({**json.loads(tbytes(TABLE).decode()), "note": "stray"}, indent=1) + "\n").encode()
BASELINE_DIFF = {"SKILL.md", "corpus/SOURCES.md", RECEIPT, "corpus/evidence/round52/PROVENANCE.md",
                 "corpus/evidence/round58/PROVENANCE.md", "corpus/evidence/round94/PROVENANCE.md",
                 "plans/grader-population-ledger.json"}

# ---------------- spec table ----------------
# kind: "counter" (mutate COUNTER before the freeze) | "tree" (mutate the T tree after the freeze)
SPECS = [
    dict(name="P00_positive", kind="tree", tree=[], expect="none (baseline)"),
    # --- counter mutants, each paired with the tree defect its leg must catch ---
    dict(name="M01_L1_true", kind="counter", counter=("l1 = receipt_bytes is not None", "l1 = True"),
         tree=[("del", RECEIPT)], expect="L1 (redundant legs)"),
    dict(name="M02_L2_true", kind="counter", counter=("    l2 = (all(sha(", "    l2 = True or (all(sha("),
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "SUBJECT_SHA", "0" * 64)))], expect="L2"),
    dict(name="M03_L3_true", kind="counter",
         counter=("l3 = bool(tip) and bool(fcommit) and tip == fcommit", "l3 = True"),
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "LANE_TIP", BASE)))], expect="L3"),
    dict(name="M04_L3_weak", kind="counter",
         counter=("l3 = bool(tip) and bool(fcommit) and tip == fcommit", "l3 = bool(tip)"),
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "LANE_TIP", BASE)))], expect="L3"),
    dict(name="M05_L4_true", kind="counter",
         counter=("l4 = bool(frozen.get(TABLE)) and sha(table_bytes) == frozen.get(TABLE)", "l4 = True"),
         instr=[(TABLE, lambda b: TABLE_STRAY)], instr_pristine=[TABLE], expect="L4"),
    dict(name="M05b_L4_true_stamped", kind="counter",
         counter=("l4 = bool(frozen.get(TABLE)) and sha(table_bytes) == frozen.get(TABLE)", "l4 = True"),
         instr=[(TABLE, lambda b: TABLE_STRAY)], instr_pristine=[TABLE],
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "CASE_TABLE_SHA", sha(TABLE_STRAY))))],
         expect="L4"),
    dict(name="M06_L5_drop_frozen", kind="counter",
         counter=("elif obs != pred or pred != predicted[cid]:", "elif obs != pred:"),
         tree=[("edit", RECEIPT, receipt_edit(flip_consistent))], expect="L5"),
    dict(name="M07_L6_obs_true", kind="counter",
         counter=('l6 = rerun.returncode == 0 and bool(receipt["obs"]) and rerun_obs == receipt["obs"] and stamps_equal',
                  'l6 = rerun.returncode == 0 and bool(receipt["obs"]) and stamps_equal'),
         tree=[("edit", RECEIPT, receipt_edit(detail_forge))], expect="L6"),
    dict(name="M08_L6_stamps_true", kind="counter",
         counter=("stamps_equal = all(bool(receipt[\"fields\"].get(k)) and rerun_parsed[\"fields\"].get(k) == receipt[\"fields\"].get(k)",
                  "stamps_equal = True or all(bool(receipt[\"fields\"].get(k)) and rerun_parsed[\"fields\"].get(k) == receipt[\"fields\"].get(k)"),
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "TOOL_SHA", "0" * 64)))], expect="L6/L9"),
    dict(name="M09_L7_set_weak", kind="counter",
         counter=("set_ok = bool(base_set) and MEMBER not in base_set and rev_set == base_set | {MEMBER}",
                  "set_ok = MEMBER not in base_set"),
         tree=[("edit", "plans/grader-population-ledger.json", ledger_edit(
             lambda d: d["members"]["winning-avg-corewars"].update(status="executed", reason="replayed", round=100)))],
         expect="L7"),
    dict(name="M10_L7_legacy_true", kind="counter",
         counter=('legacy_ok = (member.get("receipt") == RECEIPT and member.get("subject") == "tb2-header"',
                  'legacy_ok = (True and member.get("subject") == "tb2-header"'),
         tree=[("edit", "plans/grader-population-ledger.json", ledger_edit(
             lambda d: d["members"]["financial-document-processor"].update(receipt="corpus/evidence/round99/other.txt")))],
         expect="L7"),
    dict(name="M11_L7_classes_true", kind="counter",
         counter=('and member.get("classes") == MEMBER_CLASSES and set_ok and legacy_ok)',
                  'and True and set_ok and legacy_ok)'),
         tree=[("edit", "plans/grader-population-ledger.json", ledger_edit(
             lambda d: d["members"]["financial-document-processor"].update(classes=["crypto-credential"])))],
         expect="L7/TARGET cells"),
    dict(name="M12_L7_round_true", kind="counter",
         counter=('l7 = (member.get("status") == "executed" and member.get("round") == 100',
                  'l7 = (member.get("status") == "executed" and True'),
         tree=[("edit", "plans/grader-population-ledger.json", ledger_edit(
             lambda d: d["members"]["financial-document-processor"].update(round=99)))], expect="L7"),
    dict(name="M13_L8_true", kind="counter",
         counter=("l8 = bool(frozen.get(TOOL)) and sha(tool_at_rev) == frozen.get(TOOL)", "l8 = True"),
         instr=[(PROBE, lambda b: b + b"\n# forged after freeze\n")],
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "TOOL_SHA", sha(tbytes(PROBE) + b"\n# forged after freeze\n"))))],
         instr_pristine=[PROBE], expect="L8"),
    dict(name="M14_L9_hostbash_true", kind="counter",
         counter=('and f.get("HOST_BASH") == host_tool(["/usr/bin/bash", "--version"]))',
                  'and True)'),
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "HOST_BASH", "GNU bash, version 0.0.0(1)-release (forged)")))],
         expect="L9"),
    dict(name="M15_L10_ge", kind="counter",
         counter=("l10 = len(added) == NEW_ROWS and not flagged", "l10 = len(added) >= NEW_ROWS and not flagged"),
         tree=[("edit", "corpus/SOURCES.md", sources_edit(extra_row))], expect="L10"),
    dict(name="M15b_L10_ge_noflag", kind="counter",
         counter=("l10 = len(added) == NEW_ROWS and not flagged", "l10 = len(added) >= NEW_ROWS"),
         tree=[("edit", "corpus/SOURCES.md", sources_edit(extra_row))], expect="L10"),
    dict(name="M16_L10_flag_dropped", kind="counter",
         counter=("l10 = len(added) == NEW_ROWS and not flagged", "l10 = len(added) == NEW_ROWS"),
         tree=[("edit", "corpus/SOURCES.md", sources_edit(url_edit))], expect="L10"),
    dict(name="M17_L11_true", kind="counter",
         counter=("l11 = bool(frozen.get(SELF)) and sha(self_at_rev) == frozen.get(SELF)", "l11 = True"),
         instr=[(COUNTER, lambda b: b + b"\n# forged after freeze\n")], instr_pristine=[COUNTER], expect="L11"),
    dict(name="M18_L12_outside_dropped", kind="counter",
         counter=("l12 = bool(fcommit) and not outside_table and not own_bad", "l12 = bool(fcommit) and not own_bad"),
         extra={"corpus/knowledge/zz-extra.md": b"not in the candidate table\n"}, expect="L12"),
    dict(name="M19_L12_own_dropped", kind="counter",
         counter=("l12 = bool(fcommit) and not outside_table and not own_bad", "l12 = bool(fcommit) and not outside_table"),
         tree=[("edit", "SKILL.md", lambda b: b.replace(b"executed 35 of 76 (round 100 adds",
                                                        b"executed 36 of 76 (round 100 adds", 1))],
         cand_mode="pristine", expect="L12"),
    dict(name="M20_L13_true", kind="counter",
         counter=("l13 = not live_rows", "l13 = True"),
         tree=[("edit", "corpus/SOURCES.md", sources_edit(typed_words))], expect="L13"),
    dict(name="M21_TARGET_exec_total", kind="counter",
         counter=('exec_total = sum(1 for v in members.values() if v.get("status") == "executed")',
                  'exec_total = sum(1 for v in members.values())'), expect="TARGET only"),
    dict(name="M22_parser_obs_eq_pred", kind="counter",
         counter=('cases.append((cid, parts.get("predicted", "?"), parts.get("observed", "?")))',
                  'cases.append((cid, parts.get("predicted", "?"), parts.get("predicted", "?")))'),
         tree=[("edit", RECEIPT, receipt_edit(flip_observed))], expect="parser"),
    dict(name="M23_parser_fields_lower", kind="counter",
         counter=("fields[key] = value.strip()", "fields[key] = value.strip().lower()"), expect="self"),
    # --- tree mutants, counter untouched ---
    dict(name="T01_receipt_lanetip", kind="tree",
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "LANE_TIP", BASE)))], expect="L3"),
    dict(name="T02_receipt_detail", kind="tree",
         tree=[("edit", RECEIPT, receipt_edit(detail_forge))], expect="L6"),
    dict(name="T03_receipt_toolsha", kind="tree",
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "TOOL_SHA", "0" * 64)))], expect="L6/L9"),
    dict(name="T04_receipt_hostbash", kind="tree",
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "HOST_BASH", "GNU bash, version 0.0.0(1)-release (forged)")))],
         expect="L9"),
    dict(name="T05_receipt_tablesha", kind="tree",
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "CASE_TABLE_SHA", "0" * 64)))], expect="L6/L9"),
    dict(name="T06_receipt_drop_case", kind="tree",
         tree=[("edit", RECEIPT, receipt_edit(lambda t: drop_case(t, "C15")))], expect="L5/L6"),
    dict(name="T07_receipt_flip_case", kind="tree",
         tree=[("edit", RECEIPT, receipt_edit(flip_observed))], expect="L5/L6"),
    dict(name="T08_receipt_absent", kind="tree", tree=[("del", RECEIPT)], expect="L1.."),
    dict(name="T09_ledger_extra_member", kind="tree",
         tree=[("edit", "plans/grader-population-ledger.json", ledger_edit(
             lambda d: d["members"]["winning-avg-corewars"].update(status="executed", reason="replayed", round=100)))],
         expect="L7"),
    dict(name="T10_ledger_status", kind="tree",
         tree=[("edit", "plans/grader-population-ledger.json", ledger_edit(
             lambda d: d["members"]["financial-document-processor"].update(status="pending")))], expect="L7"),
    dict(name="T11_ledger_classes", kind="tree",
         tree=[("edit", "plans/grader-population-ledger.json", ledger_edit(
             lambda d: d["members"]["financial-document-processor"].update(classes=["crypto-credential"])))],
         expect="L7"),
    dict(name="T12_ledger_legacy", kind="tree",
         tree=[("edit", "plans/grader-population-ledger.json", ledger_edit(
             lambda d: d["members"]["financial-document-processor"].update(verdict="reward")))], expect="L7"),
    dict(name="T13_sources_extra_row", kind="tree",
         tree=[("edit", "corpus/SOURCES.md", sources_edit(extra_row))], expect="L10"),
    dict(name="T14_sources_typed_words", kind="tree",
         tree=[("edit", "corpus/SOURCES.md", sources_edit(typed_words))], expect="L13"),
    dict(name="T15_sources_drop_row", kind="tree",
         tree=[("edit", "corpus/SOURCES.md", sources_edit(lambda t: drop_row(t, "S349")))], expect="L10"),
    dict(name="T16_sources_url_edit", kind="tree",
         tree=[("edit", "corpus/SOURCES.md", sources_edit(url_edit))], expect="L10"),
    dict(name="T17_skill_cell", kind="tree",
         tree=[("edit", "SKILL.md", lambda b: b.replace(b"executed 35 of 76 (round 100 adds",
                                                        b"executed 36 of 76 (round 100 adds", 1))],
         cand_mode="pristine", expect="L12"),
    dict(name="T18_extra_file", kind="tree", extra={"corpus/knowledge/zz-extra.md": b"not in the candidate table\n"},
         expect="L12"),
    dict(name="T19_probe_comment", kind="tree", instr=[(PROBE, lambda b: b + b"\n# forged after freeze\n")],
         tree=[("edit", RECEIPT, receipt_edit(lambda t: field(t, "TOOL_SHA", sha(tbytes(PROBE) + b"\n# forged after freeze\n"))))],
         instr_pristine=[PROBE], expect="L8"),
    dict(name="T20_table_stray_key", kind="tree",
         instr=[(TABLE, lambda b: TABLE_STRAY)], instr_pristine=[TABLE], expect="L4"),
    dict(name="T21_counter_comment", kind="tree", instr=[(COUNTER, lambda b: b + b"\n# forged after freeze\n")],
         instr_pristine=[COUNTER], expect="L11"),
    dict(name="T22_capture_edit", kind="tree",
         tree=[("edit", "corpus/evidence/round100/tb2-financial-document-processor/test.sh",
                lambda b: b + b"\n# forged\n")], expect="L2/SETUP"),
]


def build_and_run(spec: dict) -> dict:
    name = spec["name"]
    D = S / "fx" / name
    work = S / "work" / name
    if D.exists():
        shutil.rmtree(D)
    if work.exists():
        shutil.rmtree(work)
    D.parent.mkdir(parents=True, exist_ok=True)
    git(S, "clone", "-q", "--shared", str(LANE), str(D), check=True)
    git(D, "-c", "advice.detachedHead=false", "checkout", "-q", P2)
    top = git(D, "rev-parse", "--show-toplevel").stdout.strip()
    if top != str(D):
        raise SystemExit(f"toplevel mismatch {top} != {D}")
    # instrument mutations land in the freeze commit
    touched: set[str] = set()
    for path, fn in spec.get("instr", []):
        p = D / path
        p.write_bytes(fn(p.read_bytes()))
        touched.add(path)
    if spec.get("counter"):
        p = D / COUNTER
        old, new = spec["counter"]
        p.write_text(sub1(p.read_text(), old, new), encoding="utf-8")
        touched.add(COUNTER)
    instr_bytes = {p: (D / p).read_bytes() for p in touched}
    # final (mutant) content of the candidate set and the receipt
    final: dict[str, bytes] = {}
    for path in CAND + [RECEIPT]:
        final[path] = tbytes(path)
    final[RECEIPT] = re.sub(r"(?m)^LANE_TIP .*$", "LANE_TIP @@FTIP@@", final[RECEIPT].decode()).encode()
    for op in spec.get("tree", []):
        if op[0] == "del":
            final.pop(op[1], None)
        else:
            if op[1] not in final:
                final[op[1]] = tbytes(op[1])
            final[op[1]] = op[2](final[op[1]])
    # freeze tables
    pristine = set(spec.get("instr_pristine", []))
    cand_mode = spec.get("cand_mode", "actual")
    instr_sha = {p: (sha(tbytes(p)) if p in pristine else sha((D / p).read_bytes())) for p in INSTR}
    cand_sha = {p: (sha(final[p]) if cand_mode == "actual" and p in final else sha(tbytes(p))) for p in CAND}
    lines = ["# fixture-only freeze table (mutant %s, not the lane's claims file)" % name, "",
             "```frozen-instruments"]
    lines += ["%s  %s" % (instr_sha[p], p) for p in INSTR]
    lines += ["```", "", "```candidate-bytes"]
    lines += ["%s  %s" % (cand_sha[p], p) for p in CAND]
    lines += ["```", ""]
    (D / CLAIMS).write_text("\n".join(lines), encoding="utf-8")
    git(D, "add", "-A", "corpus", "plans", "SKILL.md", ".ufo")
    git(D, "-c", "user.name=fixture", "-c", "user.email=fixture@fixture.invalid", "commit", "-qm", "fixture freeze")
    F = git(D, "rev-parse", "HEAD").stdout.strip()
    # move the tree to T, keep the fixture claims, write the mutant bytes
    git(D, "read-tree", "-u", "--reset", T)
    git(D, "checkout", F, "--", CLAIMS)
    for path, data in instr_bytes.items():
        (D / path).write_bytes(data)
    for path, data in final.items():
        p = D / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    for op in spec.get("tree", []):
        if op[0] == "del":
            (D / op[1]).unlink(missing_ok=True)
    for path, data in spec.get("extra", {}).items():
        p = D / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    if RECEIPT in final and b"@@FTIP@@" in final[RECEIPT]:
        final[RECEIPT] = final[RECEIPT].replace(b"@@FTIP@@", F.encode())
        (D / RECEIPT).write_bytes(final[RECEIPT])
    git(D, "add", "-A")
    git(D, "-c", "user.name=fixture", "-c", "user.email=fixture@fixture.invalid", "commit", "-qm", "mutant " + name)
    REV = git(D, "rev-parse", "HEAD").stdout.strip()
    diff = git(D, "diff", "--name-only", "--no-renames", F, REV).stdout.split()
    instr_proof = {p: ("changed" if sha((D / p).read_bytes()) != sha(tbytes(p)) else "same") for p in touched}
    diff_extra = sorted(set(diff) - BASELINE_DIFF)
    diff_missing = sorted(BASELINE_DIFF - set(diff))
    defect_present = ("changed" in instr_proof.values()) or bool(diff_extra) or bool(diff_missing)
    t0 = time.time()
    proc = subprocess.run([sys.executable, "plans/round100_c1_replay.py", "--lane", ".", "--rev", "HEAD",
                           "--work", str(work), "--grader-venv", str(G)],
                          cwd=str(D), capture_output=True, text=True, timeout=7200)
    dur = time.time() - t0
    out = proc.stdout
    legs = next((l for l in out.splitlines() if l.startswith("LEGS ")), "LEGS <none>")
    target = next((l for l in out.splitlines() if l.startswith("TARGET ")), "TARGET <none>")
    pred = next((l for l in out.splitlines() if l.startswith("PREDICATE ")), "PREDICATE <none>")
    fails = re.findall(r"L(\d+)=fail", legs)
    return dict(name=name, kind=spec["kind"], rc=proc.returncode, legs=legs, target=target, pred=pred,
                failing=fails, expect=spec.get("expect", ""), dur=round(dur, 1), F=F, rev=REV,
                diff=diff, instr=instr_proof, diff_extra=diff_extra, diff_missing=diff_missing,
                defect_present=defect_present, out=out, stderr=proc.stderr[-2000:])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--out", default=str(S / "results.json"))
    a = ap.parse_args()
    specs = SPECS
    if a.only:
        want = set(a.only.split(","))
        specs = [s for s in SPECS if s["name"] in want]
    def safe(spec):
        try:
            return build_and_run(spec)
        except Exception as error:  # noqa: BLE001 - a broken mutant is a result, not a crash
            return dict(name=spec["name"], kind=spec["kind"], rc=-1, legs="LEGS <error>", target="TARGET <error>",
                        pred="PREDICATE <error>", failing=["error"], expect=spec.get("expect", ""), dur=0,
                        F="", rev="", diff=[], instr={}, diff_extra=[], diff_missing=[],
                        defect_present=False, out=f"{type(error).__name__}: {error}", stderr="")

    results = []
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futs = {pool.submit(safe, s): s for s in specs}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            print(f"{r['name']:26s} rc={r['rc']} fails={','.join(r['failing']) or '-'} "
                  f"expect={r['expect']} {r['dur']}s", flush=True)
            Path(a.out).write_text(json.dumps(results, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
