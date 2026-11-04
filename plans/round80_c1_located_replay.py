#!/usr/bin/env python3
"""R80-C1 counter — the six `executed-unlocated` members become located, reproducible replays.

Universe (derived, never listed): the members whose row in
`plans/grader-population-ledger.json` carries `status == "executed-unlocated"` at the frozen base
revision `BASE_REV` (read from git, never from the worktree, so flipping rows cannot shrink it).

A located member has exactly one tracked receipt `corpus/evidence/round80/<member>-probe.txt`:
  subject   first line matches `^# tb2 <member> grader probe`
  stamp     MEMBER, SOURCE_RECEIPT (tracked, sha256 = SOURCE_SHA), TOOL (the frozen table's
            instrument, tracked, sha256 = TOOL_SHA at the measured tip), LANE_TIP (reachable from
            the measured tip), WORKTREE clean, COMMAND (names the tool), EXIT 0, MINTED_BY
  block     between OBSERVATIONS_BEGIN/OBSERVATIONS_END; every line is a frozen observation form
            (`CASE `, `case=`, `cases=`, `MISMATCH `, `OBSERVED-U `, `VECTOR `, `PREDICATE R<n>-C<m>`)
  replay    the block equals the frozen instrument's stdout at the measured tree (REV excluded)
  ledger    the member's row is `executed` with this receipt, `subject=tb2-header`, the receipt's own
            observation form as `verdict`, and `round=80`
plus: the round-79 population gate exits 0 with `executed=24 unlocated=0` (worktree mode).

Historical divergence (the historical receipt's observation lines differ from the block) is reported
and must be noted in the receipt as `HISTORICAL-DIVERGENCE <n> ...`; it is not a defect, because the
tip's instrument may have been corrected after the historical round.

Frozen before data on 2026-11-04 (L1 KengakuR80); see plans/round-80-claims.md §R80-C1.

    python3 plans/round80_c1_located_replay.py --lane .                     # verdict, worktree
    python3 plans/round80_c1_located_replay.py --lane . --rev dce7c275      # bytes at a revision
    python3 plans/round80_c1_located_replay.py --selftest --work DIR        # fixture battery
    python3 plans/round80_c1_located_replay.py --mutants --work DIR         # attributed mutants
    python3 plans/round80_c1_located_replay.py --control-flip-ledger-only --work DIR
    python3 plans/round80_c1_located_replay.py --control-header-only --work DIR
    python3 plans/round80_c1_located_replay.py --control-copy-observations --work DIR

Printed lines:
    UNIVERSE ledger=<path>@<base> members=<n> <csv>
    LOCATED <member> receipt=<path> subject=tb2-header verdict=<form> historical=same|differs
    REPRODUCED <member> lines=<n>
    LEDGER-GATE rc=0 executed=24 unlocated=0 defects=0   (or skipped=<label>)
    DEFECT <CODE> <detail>
    DEFECTS n=<n>
    TARGET members=<n> located=<n> reproduced=<n> ledger_flipped=<n> diverged=<n> defects=<n>
    PREDICATE R80-C1 pass|fail
Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE_REV = "dce7c275381c669e6489f1b795b1505d0824c262"  # round-80 base (round-79 spot-check)
LEDGER = "plans/grader-population-ledger.json"
TABLE = "plans/round80_probes.json"
EVID = "corpus/evidence/round80"
MINTED_BY = "plans/round80_c1_remint.py"
SUBJECT = r"^# tb2 {m} grader probe\b"
UNIVERSE_STATUS = "executed-unlocated"
OBS = (r"^CASE ", r"^case=", r"^cases=", r"^MISMATCH ", r"^OBSERVED-U ", r"^VECTOR ",
       r"^PREDICATE R\d+-C\d+ (?:pass|fail)")
FORMS = (("predicate", r"^PREDICATE R\d+-C\d+ pass", re.M),
         ("vectors", r"^VECTOR ", re.M),
         ("cases", r"^(?:CASE |case=)", re.M))
STAMP_RE = re.compile(r"^([A-Z_]+) (.+)$")
REV_RE = re.compile(r"^REV [0-9a-f]{7,40}\s*$")
BEGIN, END = "OBSERVATIONS_BEGIN", "OBSERVATIONS_END"
REQUIRED = ("MEMBER", "SOURCE_RECEIPT", "SOURCE_SHA", "TOOL", "TOOL_SHA", "LANE_TIP",
            "WORKTREE", "COMMAND", "EXIT", "MINTED_BY")


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True)


def sha256(b: bytes | None) -> str:
    return hashlib.sha256(b or b"").hexdigest()


def obs_lines(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if any(re.match(p, ln) for p in OBS)]


def verdict_form(text: str) -> str | None:
    for name, pattern, flags in FORMS:
        if re.search(pattern, text, flags):
            return name
    return None


def projection(lines) -> list[str]:
    """The compared projection: prediction-bearing observation lines only. Excluded are `REV`
    (commit-dependent), `cases=` summaries and `OBSERVED-U` lines (they derive from the probe's
    declared unpredictable cases), and any `CASE`/`case=` line whose predicted field contains `U`
    (the probe itself marks it observed-only). Freeze amendment A2, 2026-11-04."""
    out = []
    for ln in lines:
        ln = ln.rstrip()
        if not ln.strip() or REV_RE.match(ln):
            continue
        if ln.startswith("OBSERVED-U ") or ln.startswith("cases="):
            continue
        m = re.match(r"^(?:CASE |case=)(\S+) predicted=(\S+)", ln)
        if m and "U" in m.group(2).split("/"):
            continue
        out.append(ln)
    return out


def named_members(text: str, members: list[str]) -> list[str]:
    return [m for m in members
            if re.search(r"(?<![\w.-])" + re.escape(m) + r"(?![\w.-])", text)]


class Tree:
    def __init__(self, root: Path, label: str, tip: str, tracked, getbytes):
        self.root = root
        self.label = label
        self.tip = tip
        self._tracked = tracked
        self._get = getbytes

    def read_bytes(self, rel: str) -> bytes | None:
        return self._get(rel)

    def read(self, rel: str) -> str:
        b = self._get(rel)
        return b.decode("utf-8", "replace") if b is not None else ""

    def tracked(self, rel: str) -> bool:
        return self._tracked(rel)


def _fs_bytes(root: Path, rel: str) -> bytes | None:
    try:
        return (root / rel).read_bytes()
    except OSError:
        return None


def worktree_tree(lane: Path) -> Tree:
    tip = git(lane, "rev-parse", "--verify", "--quiet", "master^{commit}").stdout.decode().strip()
    if not tip:
        raise SystemExit("SETUP unresolved branch master")
    tracked = set(x for x in git(lane, "ls-files", "-z").stdout.decode().split("\0") if x)
    return Tree(lane, "worktree", tip, lambda rel: rel in tracked,
                lambda rel: _fs_bytes(lane, rel))


def rev_tree(lane: Path, rev: str) -> Tree:
    tip = git(lane, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}").stdout.decode().strip()
    if not tip:
        raise SystemExit(f"SETUP unresolved revision {rev!r}")
    tracked = set(git(lane, "ls-tree", "-r", "--name-only", tip).stdout.decode().splitlines())

    def get(rel: str):
        if rel not in tracked:
            return None
        proc = git(lane, "cat-file", "-p", f"{tip}:{rel}")
        return proc.stdout if proc.returncode == 0 else None

    return Tree(lane, rev, tip, lambda rel: rel in tracked, get)


def fixture_tree(root: Path) -> Tree:
    return Tree(root, "fixture", "fixture", lambda rel: (root / rel).is_file(),
                lambda rel: _fs_bytes(root, rel))


def load_base_doc(lane: Path, override: str | None) -> tuple[dict, str]:
    if override:
        return json.loads(Path(override).read_text()), f"file:{override}"
    proc = git(lane, "show", f"{BASE_REV}:{LEDGER}")
    if proc.returncode != 0:
        raise SystemExit(f"SETUP cannot read {LEDGER} at {BASE_REV}")
    return json.loads(proc.stdout.decode()), BASE_REV


def render_argv(spec: dict, member: str, work: Path) -> list[str]:
    w = work / f"{member}.work"
    w.mkdir(parents=True, exist_ok=True)
    out = work / f"{member}.out.txt"
    return [a.replace("{work}", str(w)).replace("{out}", str(out)).replace("{member}", member)
            for a in spec["argv"]]


def run_probe(tree: Tree, member: str, spec: dict, python: str, work: Path) -> tuple[int, str]:
    cmd = (spec.get("prefix") or [python]) + [spec["tool"]] + render_argv(spec, member, work)
    try:
        proc = subprocess.run(cmd, cwd=str(tree.root), capture_output=True, text=True,
                              timeout=int(spec.get("timeout", 300)))
    except subprocess.TimeoutExpired:
        return -1, ""
    except OSError as exc:
        return -2, str(exc)
    return proc.returncode, proc.stdout


def parse_receipt(text: str) -> tuple[dict, list[str]]:
    lines = text.splitlines()
    if BEGIN not in lines or END not in lines:
        return {}, []
    bi, ei = lines.index(BEGIN), lines.index(END)
    if ei <= bi:
        return {}, []
    stamp = {}
    for ln in lines[:bi]:
        m = STAMP_RE.match(ln)
        if m:
            stamp[m.group(1)] = m.group(2).strip()
    return stamp, lines[bi + 1:ei]


def check(tree: Tree, base_doc: dict, table: dict, reproduce: bool, python: str, work: Path,
          verbose: bool = True) -> tuple[list[tuple[str, str]], dict]:
    defects: list[tuple[str, str]] = []
    rows = base_doc.get("members") or {}
    universe = [m for m, row in rows.items()
                if isinstance(row, dict) and row.get("status") == UNIVERSE_STATUS]
    all_members = list(rows)
    ledger = json.loads(tree.read(LEDGER) or "{}")
    cur = ledger.get("members") or {}
    stats = {"members": len(universe), "located": 0, "reproduced": 0, "ledger_flipped": 0,
             "diverged": 0, "ledger_gate": None}
    for m in universe:
        md: list[tuple[str, str]] = []

        def add(code: str, detail: str) -> None:
            md.append((code, f"{m} {detail}"))

        rel = f"{EVID}/{m}-probe.txt"
        raw = tree.read_bytes(rel)
        if raw is None or not tree.tracked(rel):
            add("RECEIPT-UNTRACKED", rel)
            defects.extend(md)
            continue
        text = raw.decode("utf-8", "replace")
        first = text.splitlines()[0] if text else ""
        if not re.match(SUBJECT.format(m=re.escape(m)), first):
            add("SUBJECT-ABSENT", rel)
        named = named_members(text, all_members)
        if named != [m]:
            add("RECEIPT-MEMBER-COUNT", f"names {named}")
        stamp, block = parse_receipt(text)
        for key in REQUIRED:
            if key not in stamp:
                add("STAMP-MISSING", key)
        if stamp.get("MEMBER") != m:
            add("STAMP-MEMBER", repr(stamp.get("MEMBER")))
        src = stamp.get("SOURCE_RECEIPT", "")
        if not src or not tree.tracked(src):
            add("SOURCE-UNTRACKED", repr(src))
        elif sha256(tree.read_bytes(src)) != stamp.get("SOURCE_SHA"):
            add("SOURCE-SHA-MISMATCH", src)
        spec = table.get(m)
        if spec is None:
            add("PROBE-TABLE-MISSING", "no frozen probe row")
            defects.extend(md)
            continue
        if stamp.get("TOOL") != spec["tool"]:
            add("TOOL-MISMATCH", f"{stamp.get('TOOL')!r} != {spec['tool']}")
        elif not tree.tracked(spec["tool"]):
            add("TOOL-UNTRACKED", spec["tool"])
        elif sha256(tree.read_bytes(spec["tool"])) != stamp.get("TOOL_SHA"):
            add("TOOL-SHA-MISMATCH", spec["tool"])
        tip = stamp.get("LANE_TIP", "")
        if tree.label == "fixture":
            if tip != "fixture":
                add("LANE-TIP-INVALID", repr(tip))
        elif not re.fullmatch(r"[0-9a-f]{7,40}", tip or ""):
            add("LANE-TIP-INVALID", repr(tip))
        elif git(tree.root, "merge-base", "--is-ancestor", tip, tree.tip).returncode != 0:
            add("LANE-TIP-UNREACHABLE", f"{tip} is not an ancestor of {tree.tip[:12]}")
        if stamp.get("WORKTREE") != "clean":
            add("WORKTREE-DIRTY", repr(stamp.get("WORKTREE")))
        if stamp.get("EXIT") != "0":
            add("EXIT-NONZERO", repr(stamp.get("EXIT")))
        if spec["tool"] not in stamp.get("COMMAND", ""):
            add("COMMAND-TOOL", repr(stamp.get("COMMAND")))
        if stamp.get("MINTED_BY") != MINTED_BY:
            add("MINTED-BY", repr(stamp.get("MINTED_BY")))
        block = [ln.rstrip() for ln in block if ln.strip()]
        if not obs_lines("\n".join(block)):
            add("OBSERVATIONS-EMPTY", rel)
        stable = projection(block)
        hproj = projection(tree.read(spec["historical"]).splitlines())
        diverged = bool(hproj) and hproj != projection(block)
        if diverged:
            stats["diverged"] += 1
            if not re.search(r"^HISTORICAL-DIVERGENCE \d+", text, re.M):
                add("DIVERGENCE-UNNOTED", "historical observation lines differ")
        receipt_ok = not md
        if receipt_ok:
            stats["located"] += 1
        row = cur.get(m) if isinstance(cur.get(m), dict) else {}
        ledger_ok = True
        if row.get("status") != "executed":
            add("LEDGER-NOT-EXECUTED", repr(row.get("status")))
            ledger_ok = False
        elif row.get("receipt") != rel:
            add("LEDGER-RECEIPT", repr(row.get("receipt")))
            ledger_ok = False
        elif row.get("subject") != "tb2-header":
            add("LEDGER-SUBJECT", repr(row.get("subject")))
            ledger_ok = False
        elif row.get("verdict") != verdict_form(text):
            add("LEDGER-VERDICT", f"{row.get('verdict')!r} != {verdict_form(text)}")
            ledger_ok = False
        elif row.get("round") != 80:
            add("LEDGER-ROUND", repr(row.get("round")))
            ledger_ok = False
        if ledger_ok:
            stats["ledger_flipped"] += 1
        if reproduce:
            rc, out = run_probe(tree, m, spec, python, work)
            fresh = projection(out.splitlines())
            if rc != 0:
                add("REPRODUCTION-EXIT", f"rc={rc}")
            elif fresh != stable:
                add("REPRODUCTION-MISMATCH", f"fresh={len(fresh)} receipt={len(stable)}")
            else:
                stats["reproduced"] += 1
        if verbose:
            print(f"LOCATED {m} receipt={rel} subject=tb2-header "
                  f"verdict={verdict_form(text)} historical={'differs' if diverged else 'same'}")
            if reproduce:
                print(f"REPRODUCED {m} lines={len(block)}" if not md else
                      f"REPRODUCED {m} rejected")
        defects.extend(md)
    if tree.label == "worktree":
        proc = subprocess.run([python, "plans/round79_c1_population_ledger.py", "--lane", "."],
                              cwd=str(tree.root), capture_output=True, text=True, timeout=900)
        m = re.search(r"LEDGER rows=(\d+) executed=(\d+) unlocated=(\d+) unexecuted=(\d+)",
                      proc.stdout)
        gd = re.search(r"DEFECTS n=(\d+)", proc.stdout)
        gate = {"rc": proc.returncode, "executed": int(m.group(2)) if m else -1,
                "unlocated": int(m.group(3)) if m else -1,
                "defects": int(gd.group(1)) if gd else -1}
        stats["ledger_gate"] = gate
        if proc.returncode != 0:
            defects.append(("LEDGER-GATE-FAIL", f"rc={proc.returncode}"))
        elif gate["defects"] != 0:
            defects.append(("LEDGER-GATE-DEFECTS", f"n={gate['defects']}"))
        elif gate["executed"] != 24 or gate["unlocated"] != 0:
            defects.append(("LEDGER-GATE-COUNTS",
                            f"executed={gate['executed']} unlocated={gate['unlocated']}"))
        if verbose:
            print(f"LEDGER-GATE rc={proc.returncode} executed={gate['executed']} "
                  f"unlocated={gate['unlocated']} defects={gate['defects']}")
    elif verbose:
        print(f"LEDGER-GATE skipped={tree.label}")
    return defects, stats


def run(tree: Tree, base_doc: dict, base_label: str, table: dict, reproduce: bool, python: str,
        work: Path, quiet: bool = False) -> int:
    defects, stats = check(tree, base_doc, table, reproduce, python, work, verbose=not quiet)
    universe = [m for m, r in (base_doc.get("members") or {}).items()
                if isinstance(r, dict) and r.get("status") == UNIVERSE_STATUS]
    print(f"UNIVERSE ledger={LEDGER}@{base_label[:12]} members={stats['members']} "
          f"{', '.join(universe)}")
    for code, detail in defects:
        print(f"DEFECT {code} {detail}")
    print(f"DEFECTS n={len(defects)}")
    print(f"TARGET members={stats['members']} located={stats['located']} "
          f"reproduced={stats['reproduced']} ledger_flipped={stats['ledger_flipped']} "
          f"diverged={stats['diverged']} defects={len(defects)}")
    gate = stats["ledger_gate"]
    gate_ok = gate is None or (gate.get("rc") == 0 and gate.get("defects") == 0
                               and gate.get("executed") == 24 and gate.get("unlocated") == 0)
    ok = (not defects and stats["members"] == 6 and stats["located"] == 6
          and stats["ledger_flipped"] == 6
          and stats["reproduced"] == (6 if reproduce else 0) and gate_ok)
    print(f"PREDICATE R80-C1 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


# ------------------------------------------------------------------ fixtures


FIXTURE_TOOL = '''import os, sys
m = sys.argv[sys.argv.index("--member") + 1]
print(f"CASE {m}-one predicted=P observed=P rc=0")
print(f"CASE {m}-speed predicted=U observed={os.environ.get('FIXTURE_U', 'P')} rc=0 (observed-only)")
print("cases=2 observed_pass=2 observed_fail=0 mismatches=0")
print("PREDICATE R80-C1 pass")
'''

FIXTURE_NAMES = ("cancel-async-tasks", "chess-best-move", "distribution-search",
                 "largest-eigenval", "openssl-selfsigned-cert", "protein-assembly")


def hist_text(m: str) -> str:
    return (f"CASE {m}-one predicted=P observed=P rc=0\n"
            f"CASE {m}-speed predicted=U observed=P rc=0 (observed-only)\n"
            "cases=2 observed_pass=2 observed_fail=0 mismatches=0\n"
            "PREDICATE R80-C1 pass\n")


def fixture_table() -> dict:
    return {m: {"tool": "plans/fixture_probe.py", "historical": f"corpus/evidence/round90/{m}.txt",
                "argv": ["--member", "{member}"], "timeout": 60} for m in FIXTURE_NAMES}


def stamp_of(m: str, root: Path, tool: Path, hist: Path, extra: str = "") -> str:
    cmd = f"python3 plans/fixture_probe.py --member {m}"
    return (
        f"# tb2 {m} grader probe (round 80 re-mint)\n"
        f"MEMBER {m}\n"
        f"SOURCE_RECEIPT corpus/evidence/round90/{m}.txt\n"
        f"SOURCE_SHA {sha256(hist.read_bytes())}\n"
        f"TOOL plans/fixture_probe.py\n"
        f"TOOL_SHA {sha256(tool.read_bytes())}\n"
        f"LANE_TIP fixture\n"
        f"WORKTREE clean\n"
        f"COMMAND {cmd}\n"
        f"EXIT 0\n"
        f"MINTED_BY {MINTED_BY}\n"
        f"{extra}"
    )


def ledger_docs(status: str) -> tuple[dict, dict]:
    cur = {"members": {m: {"classes": ["stdout"], "round": 80,
                           "receipt": f"{EVID}/{m}-probe.txt", "status": status,
                           "subject": "tb2-header", "verdict": "predicate"} for m in FIXTURE_NAMES}}
    base = {"members": {m: {"classes": ["stdout"], "round": 90, "status": "executed-unlocated",
                            "receipt": f"corpus/evidence/round90/{m}.txt",
                            "instrument": "plans/fixture_probe.py",
                            "debt": "no-subject-stamp"} for m in FIXTURE_NAMES}}
    return cur, base


def build_fixture(root: Path, *, ledger_status: str = "executed",
                  mutate: str | None = None) -> dict:
    if root.exists():
        shutil.rmtree(root)
    (root / "plans").mkdir(parents=True)
    (root / "corpus/evidence/round80").mkdir(parents=True)
    (root / "corpus/evidence/round90").mkdir(parents=True)
    tool = root / "plans/fixture_probe.py"
    tool.write_text(FIXTURE_TOOL)
    for m in FIXTURE_NAMES:
        hist = root / f"corpus/evidence/round90/{m}.txt"
        hist.write_text(hist_text(m))
        extra = ""
        if mutate == "divergence-noted" and m == FIXTURE_NAMES[0]:
            extra = "HISTORICAL-DIVERGENCE 1 case set corrected after the historical round\n"
        receipt = (stamp_of(m, root, tool, hist, extra)
                   + "OBSERVATIONS_BEGIN\n" + hist_text(m) + "OBSERVATIONS_END\n")
        if m == FIXTURE_NAMES[0]:
            if mutate == "subject-absent":
                receipt = receipt.replace(f"# tb2 {m} grader probe (round 80 re-mint)\n", "")
            elif mutate == "stamp-missing":
                receipt = re.sub(r"^TOOL_SHA .*\n", "", receipt, flags=re.M)
            elif mutate == "tool-sha-mismatch":
                receipt = re.sub(r"^TOOL_SHA .*$", "TOOL_SHA " + "0" * 64, receipt, flags=re.M)
            elif mutate == "exit-nonzero":
                receipt = receipt.replace("EXIT 0", "EXIT 1")
            elif mutate == "lane-tip-invalid":
                receipt = receipt.replace("LANE_TIP fixture", "LANE_TIP not-a-revision")
            elif mutate == "observations-empty":
                receipt = receipt.split("OBSERVATIONS_BEGIN")[0] + "OBSERVATIONS_BEGIN\nOBSERVATIONS_END\n"
            elif mutate == "observations-foreign":
                receipt = receipt.replace("OBSERVATIONS_BEGIN\n",
                                          "OBSERVATIONS_BEGIN\nthis line is not an observation\n")
            elif mutate == "second-member":
                receipt = receipt.replace("OBSERVATIONS_END",
                                          f"NOISE {FIXTURE_NAMES[1]}\nOBSERVATIONS_END")
            elif mutate == "u-case-varies":
                receipt = receipt.replace(f"CASE {m}-speed predicted=U observed=P",
                                          f"CASE {m}-speed predicted=U observed=F")
            elif mutate == "prediction-varies":
                receipt = receipt.replace(f"CASE {m}-one predicted=P observed=P",
                                          f"CASE {m}-one predicted=P observed=F")
            elif mutate == "copy-observations":
                other = hist_text(FIXTURE_NAMES[1])
                head = receipt.split("OBSERVATIONS_BEGIN")[0]
                receipt = head + "OBSERVATIONS_BEGIN\n" + other + "OBSERVATIONS_END\n"
            elif mutate == "divergence-unnoted":
                hist.write_text(hist_text(m) + "CASE corrected-later predicted=P observed=P rc=0\n")
                receipt = (stamp_of(m, root, tool, hist)
                           + "OBSERVATIONS_BEGIN\n" + hist_text(m) + "OBSERVATIONS_END\n")
            elif mutate == "divergence-noted":
                hist.write_text(hist_text(m) + "CASE corrected-later predicted=P observed=P rc=0\n")
                receipt = (stamp_of(m, root, tool, hist,
                                    "HISTORICAL-DIVERGENCE 1 case set corrected after the historical round\n")
                           + "OBSERVATIONS_BEGIN\n" + hist_text(m) + "OBSERVATIONS_END\n")
        if mutate == "receipt-missing" and m == FIXTURE_NAMES[0]:
            pass
        else:
            (root / f"corpus/evidence/round80/{m}-probe.txt").write_text(receipt)
    cur, base = ledger_docs(ledger_status)
    if mutate == "ledger-unlocated":
        cur["members"][FIXTURE_NAMES[0]]["status"] = "executed-unlocated"
    if mutate == "ledger-wrong-receipt":
        cur["members"][FIXTURE_NAMES[0]]["receipt"] = "corpus/evidence/round90/cancel-async-tasks.txt"
    if mutate == "source-sha-mismatch":
        (root / f"corpus/evidence/round90/{FIXTURE_NAMES[0]}.txt").write_text(hist_text(FIXTURE_NAMES[0]) + "# altered\n")
    (root / LEDGER).parent.mkdir(parents=True, exist_ok=True)
    (root / LEDGER).write_text(json.dumps(cur, indent=1) + "\n")
    return base


def fixture_check(root: Path, mutate: str | None = None) -> tuple[list[tuple[str, str]], dict]:
    base = build_fixture(root, mutate=mutate)
    tree = fixture_tree(root)
    work = root.parent / (root.name + ".work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    try:
        return check(tree, base, fixture_table(), True, sys.executable, work, verbose=False)
    finally:
        shutil.rmtree(work, ignore_errors=True)


CASES = [
    ("clean", None),
    ("subject-absent", "SUBJECT-ABSENT"),
    ("stamp-missing", "STAMP-MISSING"),
    ("source-sha-mismatch", "SOURCE-SHA-MISMATCH"),
    ("tool-sha-mismatch", "TOOL-SHA-MISMATCH"),
    ("receipt-missing", "RECEIPT-UNTRACKED"),
    ("observations-empty", "OBSERVATIONS-EMPTY"),
    ("observations-foreign", "REPRODUCTION-MISMATCH"),
    ("second-member", "RECEIPT-MEMBER-COUNT"),
    ("ledger-unlocated", "LEDGER-NOT-EXECUTED"),
    ("ledger-wrong-receipt", "LEDGER-RECEIPT"),
    ("exit-nonzero", "EXIT-NONZERO"),
    ("lane-tip-invalid", "LANE-TIP-INVALID"),
    ("divergence-unnoted", "DIVERGENCE-UNNOTED"),
    ("divergence-noted", None),
    ("u-case-varies", None),
    ("prediction-varies", "REPRODUCTION-MISMATCH"),
    ("copy-observations", "REPRODUCTION-MISMATCH"),
]


def selftest(work: Path) -> int:
    failures = 0
    for name, expect in CASES:
        root = work / f"c1-{name}"
        defects, stats = fixture_check(root, name)
        codes = sorted({c for c, _ in defects})
        good = (not defects and stats["located"] == 6 and stats["reproduced"] == 6
                and stats["ledger_flipped"] == 6) if expect is None else (expect in codes)
        failures += 0 if good else 1
        print(f"CASE {name} expect={expect or 'pass'} observed={','.join(codes) or '-'} "
              f"located={stats['located']} reproduced={stats['reproduced']} "
              f"{'ok' if good else 'FAIL'}")
        shutil.rmtree(root, ignore_errors=True)
    print(f"SELFTEST cases={len(CASES)} red={len(CASES) - 3} failures={failures}")
    return 0 if failures == 0 else 1


MUTANTS = [
    ("flip-ledger-only", "ledger-unlocated"),
    ("strip-stamp", "stamp-missing"),
    ("wrong-tool-sha", "tool-sha-mismatch"),
    ("foreign-block", "copy-observations"),
    ("drop-receipt", "receipt-missing"),
    ("second-member", "second-member"),
]


def mutants(work: Path) -> int:
    killed = survived = 0
    for name, mutate in MUTANTS:
        root = work / f"c1-mut-{name}"
        defects, stats = fixture_check(root, mutate)
        ok = bool(defects) and not (stats["located"] == 6 and stats["reproduced"] == 6
                                    and stats["ledger_flipped"] == 6 and not defects)
        killed += 1 if ok else 0
        survived += 0 if ok else 1
        print(f"MUTANT {name} codes={','.join(sorted({c for c, _ in defects})) or '-'} "
              f"{'killed' if ok else 'SURVIVED'}")
        shutil.rmtree(root, ignore_errors=True)
    print(f"MUTANTS real={len(MUTANTS)} killed={killed} survived={survived}")
    return 0 if survived == 0 else 1


def control(work: Path, name: str) -> int:
    root = work / f"c1-ctl-{name}"
    base = build_fixture(root)
    tree = fixture_tree(root)
    if name == "flip-ledger-only":
        for m in FIXTURE_NAMES:
            (root / f"corpus/evidence/round80/{m}-probe.txt").write_text(hist_text(m))
    elif name == "header-only":
        for m in FIXTURE_NAMES:
            (root / f"corpus/evidence/round80/{m}-probe.txt").write_text(
                f"# tb2 {m} grader probe\nMEMBER {m}\n" + hist_text(m))
    elif name == "copy-observations":
        first = (root / f"corpus/evidence/round80/{FIXTURE_NAMES[0]}-probe.txt").read_text()
        head = first.split("OBSERVATIONS_BEGIN")[0]
        (root / f"corpus/evidence/round80/{FIXTURE_NAMES[0]}-probe.txt").write_text(
            head + "OBSERVATIONS_BEGIN\n" + hist_text(FIXTURE_NAMES[1]) + "OBSERVATIONS_END\n")
    cwork = work / f"c1-ctl-{name}.work"
    cwork.mkdir(parents=True, exist_ok=True)
    try:
        defects, stats = check(tree, base, fixture_table(), True, sys.executable, cwork, verbose=False)
    finally:
        shutil.rmtree(cwork, ignore_errors=True)
    codes = sorted({c for c, _ in defects})
    reached = (not defects and stats["located"] == 6 and stats["reproduced"] == 6
               and stats["ledger_flipped"] == 6)
    print(f"CONTROL {name} located={stats['located']} reproduced={stats['reproduced']} "
          f"defects={len(defects)} codes={','.join(codes) or '-'}")
    print(f"CONTROL {name} target_reached={reached}")
    shutil.rmtree(root, ignore_errors=True)
    return 0 if not reached else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--work", default=None)
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--base-ledger", default=None)
    ap.add_argument("--no-reproduce", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--control-flip-ledger-only", action="store_true")
    ap.add_argument("--control-header-only", action="store_true")
    ap.add_argument("--control-copy-observations", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve() if a.work else Path("/fast/scratch/hyaku/kengaku-r80/c1")
    work.mkdir(parents=True, exist_ok=True)
    if a.selftest:
        return selftest(work)
    if a.mutants:
        return mutants(work)
    for flag, name in (("control_flip_ledger_only", "flip-ledger-only"),
                       ("control_header_only", "header-only"),
                       ("control_copy_observations", "copy-observations")):
        if getattr(a, flag):
            return control(work, name)
    table = json.loads((lane / TABLE).read_text())["members"]
    base_doc, base_label = load_base_doc(lane, a.base_ledger)
    tree = worktree_tree(lane) if a.rev in ("worktree", "", None) else rev_tree(lane, a.rev)
    reproduce = not a.no_reproduce and tree.label != "rev"
    return run(tree, base_doc, base_label, table, reproduce, a.python, work, quiet=a.quiet)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
