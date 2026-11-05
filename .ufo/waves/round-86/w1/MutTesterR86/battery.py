#!/usr/bin/env python3
"""MutTesterR86 battery: my own mutants against the two round-86 counters.

Reads the committed counters (never writes them), copies them under scratch, applies one
behavior-bearing edit each, builds the fixture each edit should let through, and runs the
pristine and the mutated copy over the same fixture bytes.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRATCH = Path("/fast/scratch/hyaku/kengaku-r86/MutTesterR86")
C1 = LANE / "plans/round86_c1_replay.py"
C2 = LANE / "plans/round86_c2_repin.py"
BASE_REV = "88651a72ef112ed9f5361e1c8c197babec691f96"
MEMBER = "raman-fitting"
RECEIPT_REL = "corpus/evidence/round86/raman-fitting-probe.txt"
TABLE_REL = "plans/round86-cases.json"
LEDGER_REL = "plans/grader-population-ledger.json"
RUNS = []
LOG = []


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def log(line: str) -> None:
    print(line)
    LOG.append(line)


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(LANE), *args], capture_output=True)


MASTER = git("rev-parse", "master").stdout.decode().strip()


# ---------------------------------------------------------------- fixtures

def archive_copy(dest: Path, rels: tuple[str, ...]) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    for rel in rels:
        src = LANE / rel
        dst = dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            subprocess.run(["cp", "-a", "--reflink=auto", str(src), str(dst.parent)],
                           check=True)
        elif src.is_file():
            subprocess.run(["cp", "-a", "--reflink=auto", str(src), str(dst)], check=True)
    return dest


def reflink_tree(dest: Path) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-a", "--reflink=auto", f"{LANE}/.", str(dest)], check=True)
    return dest


def rewrite(path: Path, old: str, new: str) -> None:
    """Replace through a fresh inode so a reflinked fixture never shares a write with lane."""
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"fixture needle absent in {path}: {old[:60]!r}")
    temp = path.with_suffix(path.suffix + ".mt86")
    temp.write_text(text.replace(old, new, 1), encoding="utf-8")
    os.replace(temp, path)


C1_PATHS = ("plans", "corpus/evidence/round52/graders/raman-fitting",
            "corpus/evidence/round86", "SKILL.md")


def c1_fixture(name: str) -> Path:
    root = archive_copy(SCRATCH / "fixtures" / name, C1_PATHS)
    ledger = root / LEDGER_REL
    doc = json.loads(ledger.read_bytes())
    doc["members"][MEMBER].update(status="executed", round=86,
                                  receipt=RECEIPT_REL, subject="tb2-header",
                                  verdict="cases")
    ledger.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return root


def c1_fixture_exit1(root: Path) -> None:
    rewrite(root / RECEIPT_REL, "EXIT 0", "EXIT 1")


def c1_fixture_member(root: Path, remint: bool) -> None:
    path = root / TABLE_REL
    doc = json.loads(path.read_bytes())
    doc["member"] = "other-member"
    drifted = (json.dumps(doc, indent=2) + "\n").encode()
    path.write_bytes(drifted)
    if remint:
        rewrite(root / RECEIPT_REL, re.search(r"(?m)^CASE_TABLE_SHA (\S+)$",
                                              (root / RECEIPT_REL).read_text(encoding="utf-8")
                                              ).group(0),
                "CASE_TABLE_SHA " + sha_bytes(drifted))


def c1_fixture_ledger_unexecuted(root: Path) -> None:
    path = root / LEDGER_REL
    doc = json.loads(path.read_bytes())
    doc["members"][MEMBER]["status"] = "unexecuted"
    path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def c1_fixture_drop_line(root: Path, line: str) -> None:
    path = root / RECEIPT_REL
    text = path.read_text(encoding="utf-8")
    if line not in text:
        raise SystemExit(f"receipt line absent: {line!r}")
    path.write_text(text.replace(line + "\n", "", 1), encoding="utf-8")


def c1_fixture_worktree(root: Path, value: str) -> None:
    path = root / RECEIPT_REL
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^WORKTREE .*$", "WORKTREE " + value, text)
    path.write_text(text, encoding="utf-8")


def c2_fixture(name: str) -> Path:
    return reflink_tree(SCRATCH / "fixtures" / name)


def c2_break_pin(root: Path) -> None:
    rewrite(root / "SHONEN.md", "PROVINCE.md:151", "PROVINCE.md:129")
    rewrite(root / "plans/state_check.py", '4, "PROVINCE.md:151", 151,',
            '4, "PROVINCE.md:129", 129,')


def c2_break_pin_only(root: Path) -> None:
    rewrite(root / "plans/state_check.py", '4, "PROVINCE.md:151", 151,',
            '4, "PROVINCE.md:129", 129,')


def c2_break_shonen_only(root: Path) -> None:
    rewrite(root / "SHONEN.md", "PROVINCE.md:151", "PROVINCE.md:129")


def c2_break_instrument_selftest(root: Path) -> None:
    rewrite(root / "plans/state_check.py",
            "    if args.selftest:\n        return run_selftest()",
            "    if args.selftest:\n        return 1")


# ---------------------------------------------------------------- runners

def run(script: Path, args: list[str], work: Path) -> dict:
    work.mkdir(parents=True, exist_ok=True)
    started = time.time()
    proc = subprocess.run([sys.executable, "-I", "-B", str(script), *args, "--work", str(work)],
                          capture_output=True, text=True, timeout=1800,
                          env={"PATH": "/usr/bin", "TMPDIR": str(work),
                               "PYTHONDONTWRITEBYTECODE": "1"})
    return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr,
            "seconds": round(time.time() - started, 2)}


def defects_of(out: dict) -> list[str]:
    return [line for line in out["stdout"].splitlines() if line.startswith("DEFECT ")]


def legs_of(out: dict) -> list[str]:
    return sorted({line.split()[1] for line in defects_of(out)})


def predicate_of(out: dict) -> str:
    for line in out["stdout"].splitlines():
        if line.startswith("PREDICATE "):
            return line
    return "<absent>"


def reached(out: dict, counter: str) -> bool:
    return out["returncode"] == 0 and f"PREDICATE {counter} pass" in out["stdout"]


def mutate(source: str, edits: list[tuple[str, str]]) -> tuple[str, list[bool]]:
    text = source
    applied = []
    for needle, repl in edits:
        count = text.count(needle)
        text = text.replace(needle, repl, 1)
        applied.append(count == 1)
    return text, applied


def record(name: str, counter: str, source: str, edits, fixture_desc: str,
           plain: dict, mutant: dict | None, verdict: str, catcher: str = "") -> None:
    row = {
        "mutant": name, "counter": counter, "fixture": fixture_desc,
        "edits": [{"needle": n, "replacement": r} for n, r in edits],
        "unmutated": {"rc": plain["returncode"], "defects": defects_of(plain),
                      "legs": legs_of(plain), "predicate": predicate_of(plain),
                      "target_line": next((l for l in plain["stdout"].splitlines()
                                           if l.startswith("TARGET")), "")},
        "mutated": None if mutant is None else {
            "rc": mutant["returncode"], "defects": defects_of(mutant),
            "legs": legs_of(mutant), "predicate": predicate_of(mutant),
            "target_line": next((l for l in mutant["stdout"].splitlines()
                                 if l.startswith("TARGET")), "")},
        "verdict": verdict, "catcher": catcher,
    }
    RUNS.append(row)
    mutated_legs = ",".join(row["mutated"]["legs"]) if mutant else "n/a"
    mutated_rc = mutant["returncode"] if mutant else "n/a"
    log(f"[{name}] unmutated rc={row['unmutated']['rc']} "
        f"legs={','.join(row['unmutated']['legs']) or 'none'} | mutated rc={mutated_rc} "
        f"legs={mutated_legs or 'none'} -> {verdict}"
        + (f" (catcher {catcher})" if catcher else ""))


# ---------------------------------------------------------------- C1 battery

C1_MUTANTS = {
    # disable the EXIT gate but keep rejecting non-numeric/out-of-range EXIT
    "exit-nonzero-accepted": [
        ('            if stamp.get("EXIT") != "0":',
         '            if stamp.get("EXIT") not in ("0", "1"):')],
    # drop the frozen-table identity guard (member + subject_sha of the freeze anchor)
    "table-member-accepted": [
        ('    if doc.get("member") != MEMBER or doc.get("subject_sha") != SUBJECT_SHA:',
         '    if False:')],
    # drop identity guard, the byte comparison AND the receipt digest, keeping L6
    "table-member-accepted-deep": [
        ('    if doc.get("member") != MEMBER or doc.get("subject_sha") != SUBJECT_SHA:',
         '    if False:'),
        ('    elif table_bytes != frozen_bytes:', '    elif False:'),
        ('            if stamp.get("CASE_TABLE_SHA") != sha256(frozen_bytes):',
         '            if False:')],
    # make a SetupDefect (the missing freeze anchor) non-fatal
    "freeze-anchor-nonfatal": [
        ('    except SetupDefect as error:\n        return setup_failure(str(error))',
         '    except SetupDefect as error:\n'
         '        print(f"SETUP-IGNORED {error}")\n'
         '        return emit([], {"members": 1, "cases": 8, "legs": 24, "mismatches": 0,\n'
         '                         "located": 1, "executed": 1})')],
    # make stats["executed"] always 1
    "executed-always-1": [
        ('            if row.get("status") != "executed":\n'
         '                problems.append(f"status={row.get(\'status\')}")\n'
         '            else:\n'
         '                stats["executed"] = 1',
         '            if row.get("status") != "executed":\n'
         '                problems.append(f"status={row.get(\'status\')}")\n'
         '            stats["executed"] = 1')],
    # accept an observation block that carries no PREDICATE line
    "predicate-absent-accepted": [
        ('        if predicate != "pass":', '        if False:')],
    # accept a stamp that is missing a required field
    "missing-stamp-field-accepted": [
        ('            missing = [field for field in REQUIRED if field not in stamp]',
         '            missing = []')],
}


def battery_c1() -> None:
    source = C1.read_text(encoding="utf-8")
    work = SCRATCH / "work-c1"
    log(f"# C1 source {C1} sha256={sha_file(C1)} rev(master)={MASTER[:12]}")
    plain_base = run(C1, ["--lane", str(LANE), "--repo", str(LANE), "--rev", MASTER,
                          "--quiet"], work / "base")
    log(f"[baseline C1 @ {MASTER[:12]}] rc={plain_base['returncode']} "
        f"{predicate_of(plain_base)} {plain_base['seconds']}s")

    specs = [
        ("exit-nonzero-accepted", "receipt EXIT 0 -> EXIT 1", c1_fixture_exit1,
         "L2-stamp", []),
        ("table-member-accepted", "case table member raman-fitting -> other-member",
         lambda r: c1_fixture_member(r, remint=False), "L4-table", []),
        ("table-member-accepted-deep",
         "case table member -> other-member, receipt CASE_TABLE_SHA re-minted to it",
         lambda r: c1_fixture_member(r, remint=True), "L6-reproduce", []),
        ("freeze-anchor-nonfatal", "measured tree intact, --freeze BASE (table absent)",
         None, "SETUP", ["--freeze", BASE_REV]),
        ("executed-always-1", "ledger row status executed -> unexecuted", 
         c1_fixture_ledger_unexecuted, "L7-ledger", []),
        ("predicate-absent-accepted", "receipt observation block loses its PREDICATE line",
         lambda r: c1_fixture_drop_line(r, "PREDICATE R86-PROBE pass"), "L5-vectors", []),
        ("missing-stamp-field-accepted", "receipt loses its WORKTREE stamp line",
         lambda r: c1_fixture_drop_line(r, "WORKTREE dirty"), "L2-stamp", []),
    ]
    for name, fixture_desc, build, expected_leg, extra in specs:
        root = c1_fixture(f"c1-{name}")
        if build is not None:
            build(root)
        edits = C1_MUTANTS[name]
        mutated_text, applied = mutate(source, edits)
        assert all(applied), (name, applied)
        mutated_path = work / f"mutant-{name}.py"
        mutated_path.parent.mkdir(parents=True, exist_ok=True)
        mutated_path.write_text(mutated_text, encoding="utf-8")
        args = ["--lane", str(root), "--repo", str(LANE), *extra]
        plain = run(C1, args, work / f"plain-{name}")
        mutant = run(mutated_path, args, work / f"mutant-{name}")
        if expected_leg == "SETUP":
            plain_rejects = plain["returncode"] == 2 and "DEFECT SETUP" in plain["stdout"]
            catcher = "setup_failure (fail-closed, rc 2)"
        else:
            plain_rejects = plain["returncode"] == 1 and expected_leg in plain["stdout"]
            catcher = ""
        if plain_rejects and reached(mutant, "R86-C1"):
            verdict, catcher = "necessary", ""
        elif plain_rejects and not reached(mutant, "R86-C1"):
            verdict = "redundant"
            catcher = ",".join(legs_of(mutant)) or "unclassified"
        else:
            verdict, catcher = "not-a-mutant", "unmutated counter does not reject the fixture"
        log(f"  plain rc={plain['returncode']} defects={len(defects_of(plain))} "
            f"mutant_sha={sha_file(mutated_path)[:16]}")
        record(name, "round86_c1_replay.py", source, edits, fixture_desc, plain, mutant,
               verdict, catcher)
        log(f"  plain: {'; '.join(defects_of(plain)) or '<none>'}")
        log(f"  mutant: {'; '.join(defects_of(mutant)) or '<none>'}")

    # the WORKTREE candidate: is there any check at all to disable?
    for label, value in (("delivered-receipt-dirty", None), ("worktree-junk", "exploded // n/a")):
        root = c1_fixture(f"c1-worktree-{label}")
        if value is not None:
            c1_fixture_worktree(root, value)
        plain = run(C1, ["--lane", str(root), "--repo", str(LANE)], work / f"worktree-{label}")
        log(f"[worktree:{label}] WORKTREE={value or 'dirty (committed bytes)'} "
            f"rc={plain['returncode']} {predicate_of(plain)}")
        record(f"worktree-dirty-accepted::{label}", "round86_c1_replay.py", source, [],
               f"receipt WORKTREE -> {value or 'unchanged (already dirty)'}", plain, None,
               "no-check" if plain["returncode"] == 0 else "rejected",
               "" if plain["returncode"] == 0 else ",".join(legs_of(plain)))


# ---------------------------------------------------------------- C2 battery

C2_MUTANTS = {
    "skip-p5-selftest": [("    if selftest:", "    if False:")],
    "derive-returns-stale-line": [("    return hits[0]", "    return STALE_LINE")],
    "pin-line-lax": [("    if not pin_ok or line != derived:", "    if not pin_ok:")],
    "shonen-compares-to-stale": [
        ("    if shonen_pointer(root)[1] != derived:",
         "    if shonen_pointer(root)[1] != STALE_LINE:")],
}


def battery_c2() -> None:
    source = C2.read_text(encoding="utf-8")
    work = SCRATCH / "work-c2"
    log(f"# C2 source {C2} sha256={sha_file(C2)}")
    base = c2_fixture("c2-clean")
    plain_base = run(C2, ["--lane", str(base), "--root", str(base)], work / "base")
    log(f"[baseline C2 @ clean master copy] rc={plain_base['returncode']} "
        f"{predicate_of(plain_base)} {plain_base['seconds']}s")
    log(f"  {'; '.join(defects_of(plain_base)) or '<none>'}")

    specs = [
        ("skip-p5-selftest", "fixture instrument: state_check --selftest returns 1",
         c2_break_instrument_selftest, "P5-selftest", False),
        # P1 is fail-closed (SetupDefect, rc 2); it never prints a defect line, so the
        # unmutated rejection is "any named defect" (P2/P3/P4 here).
        ("derive-returns-stale-line", "stale-pin fixture (SHONEN + pin at 129)",
         c2_break_pin, None, True),
        ("pin-line-lax", "pin line 129, SHONEN pointer 151, bytes 151",
         c2_break_pin_only, "P3-pin", True),
        ("shonen-compares-to-stale", "SHONEN pointer 129, pin 151, bytes 151",
         c2_break_shonen_only, "P2-shonen", True),
    ]
    for name, fixture_desc, build, expected_leg, no_selftest in specs:
        root = c2_fixture(f"c2-{name}")
        build(root)
        edits = C2_MUTANTS[name]
        mutated_text, applied = mutate(source, edits)
        assert all(applied), (name, applied)
        mutated_path = work / f"mutant-{name}.py"
        mutated_path.parent.mkdir(parents=True, exist_ok=True)
        mutated_path.write_text(mutated_text, encoding="utf-8")
        args = ["--lane", str(root), "--root", str(root)]
        if no_selftest:
            args.append("--no-selftest")
        plain = run(C2, args, work / f"plain-{name}")
        mutant = run(mutated_path, args, work / f"mutant-{name}")
        plain_rejects = plain["returncode"] == 1 and bool(defects_of(plain)) and (
            expected_leg is None or expected_leg in plain["stdout"])
        if plain_rejects and reached(mutant, "R86-C2"):
            verdict, catcher = "necessary", ""
        elif plain_rejects and not reached(mutant, "R86-C2"):
            verdict, catcher = "redundant", ",".join(legs_of(mutant)) or "unclassified"
        else:
            verdict, catcher = "not-a-mutant", "unmutated counter does not reject the fixture"
        record(name, "round86_c2_repin.py", source, edits, fixture_desc, plain, mutant,
               verdict, catcher)
        log(f"  plain: {'; '.join(defects_of(plain)) or '<none>'}")
        log(f"  mutant: {'; '.join(defects_of(mutant)) or '<none>'}")

    # derive->STALE_LINE on the clean tree: the mutation must turn the target tree red
    name = "derive-returns-stale-line"
    edits = C2_MUTANTS[name]
    mutated_text, _ = mutate(source, edits)
    mutated_path = work / f"mutant-{name}.py"
    mutant = run(mutated_path, ["--lane", str(base), "--root", str(base)],
                 work / f"mutant-{name}-clean")
    record(f"{name}::clean-tip", "round86_c2_repin.py", source, edits,
           "delivered clean tree (the target tree itself)", plain_base, mutant,
           "falsely-red" if not reached(mutant, "R86-C2") else "survives-on-target",
           ",".join(legs_of(mutant)) or "none")
    log(f"[{name} on clean tip] mutant rc={mutant['returncode']} "
        f"{predicate_of(mutant)} defects={'; '.join(defects_of(mutant)) or '<none>'}")


def main() -> int:
    scratch_hashes = {
        "plans/round86_c1_replay.py": sha_file(C1),
        "plans/round86_c2_repin.py": sha_file(C2),
        "plans/round86_raman_probe.py": sha_file(LANE / "plans/round86_raman_probe.py"),
        TABLE_REL: sha_file(LANE / TABLE_REL),
        RECEIPT_REL: sha_file(LANE / RECEIPT_REL),
        LEDGER_REL: sha_file(LANE / LEDGER_REL),
    }
    log("# instrument bytes at battery start (lane worktree)")
    for rel, digest in scratch_hashes.items():
        log(f"  {digest}  {rel}")
    status_before = git("status", "--porcelain").stdout.decode()
    tracked_before = git("status", "--porcelain", "--untracked-files=no").stdout.decode()
    battery_c1()
    battery_c2()
    status_after = git("status", "--porcelain").stdout.decode()
    tracked_after = git("status", "--porcelain", "--untracked-files=no").stdout.decode()
    log("# instrument bytes at battery end")
    after = {rel: sha_file(LANE / rel) for rel in scratch_hashes}
    for rel in scratch_hashes:
        log(f"  {'SAME' if after[rel] == scratch_hashes[rel] else 'CHANGED'} {after[rel]}  {rel}")
    log("# lane tracked-file status during the battery: "
        f"{'unchanged' if tracked_before == tracked_after else 'CHANGED'} "
        f"(tracked lines before={len(tracked_before.splitlines())} "
        f"after={len(tracked_after.splitlines())})")
    if tracked_after.strip():
        log("# tracked lines after: " + " | ".join(tracked_after.splitlines()))
    log("# full status delta (includes sibling seats' wave files): "
        f"{'none' if status_before == status_after else 'changed'}; "
        f"untracked/modified lines before={len(status_before.splitlines())} "
        f"after={len(status_after.splitlines())}")
    (SCRATCH / "runs.json").write_text(json.dumps(
        {"master": MASTER, "instrument_hashes_before": scratch_hashes,
         "instrument_hashes_after": after,
         "tracked_status_before": tracked_before, "tracked_status_after": tracked_after,
         "runs": RUNS}, indent=2) + "\n", encoding="utf-8")
    (SCRATCH / "runs.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    necessary = sum(1 for r in RUNS if r["verdict"] == "necessary")
    redundant = sum(1 for r in RUNS if r["verdict"] == "redundant")
    no_check = sum(1 for r in RUNS if r["verdict"] == "no-check")
    log(f"# summary necessary={necessary} redundant={redundant} no-check={no_check} "
        f"runs={len(RUNS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
