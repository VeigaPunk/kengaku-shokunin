#!/usr/bin/env python3
"""R81-C1 counter — two `unattempted` population members gain located, reproducible replays.

Universe (derived, never listed). At the frozen base revision `BASE_REV` the population ledger
(`plans/grader-population-ledger.json`) is read from git, and a member is a *candidate* when its
row is `status=unexecuted reason=unattempted`, its class set is a subset of
{file-artifact, serialization-schema}, its round-52 grader capture exists, and that capture imports
stdlib modules only. The universe is the candidate set at the **maximum capture assert count** (a
frozen selection rule: coverage effort goes to the grader with the most decision legs; ties are
kept, so the rule never picks arbitrarily). At the freeze the candidates were 11 and the maximum 5
asserts, carried by exactly two members.

A located new member has exactly one tracked receipt `corpus/evidence/round81/<member>-probe.txt`:
  subject   first line matches `^# tb2 <member> grader probe`
  stamp     MEMBER, SUBJECT_CAPTURE (the round-52 capture path) + SUBJECT_SHA (its sha256 at the
            measured tree), TOOL (the frozen table's instrument) + TOOL_SHA at the measured tree,
            HOST_PYTHON (`python3 -V` of the probe interpreter), HOST_OPENSSL (`openssl version`,
            or `absent`), LANE_TIP (reachable from the measured tip), WORKTREE clean, COMMAND
            (names the tool), EXIT 0, MINTED_BY + MINTED_BY_SHA (the driver's bytes)
  block     between OBSERVATIONS_BEGIN/OBSERVATIONS_END; every line is a frozen observation form
            (`CASE `, `case=`, `cases=`, `MISMATCH `, `OBSERVED-U `, `VECTOR `,
            `PREDICATE R<n>-C<m>`); the compared projection drops `REV ` lines and blanks
  replay    the projection equals the frozen instrument's stdout at the measured tree
  ledger    the member's row is `executed` with this receipt, `subject=tb2-header`, the receipt's
            own observation form as `verdict`, and `round=81`
plus: the round-79 population gate exits 0 with `executed=26 unlocated=0` (worktree mode).

Frozen before data on 2026-11-04 (L1 KengakuR81); see plans/round-81-claims.md §R81-C1.

    python3 plans/round81_c1_new_members.py --lane .                    # verdict, worktree
    python3 plans/round81_c1_new_members.py --lane . --rev 4e833e9f     # bytes at a revision
    python3 plans/round81_c1_new_members.py --selftest --work DIR       # fixture battery
    python3 plans/round81_c1_new_members.py --mutants --work DIR        # attributed mutants
    python3 plans/round81_c1_new_members.py --control-flip-ledger-only --work DIR
    python3 plans/round81_c1_new_members.py --control-header-only --work DIR
    python3 plans/round81_c1_new_members.py --control-copy-observations --work DIR

Printed lines:
    CANDIDATES n=<n> rule=<rule> asserts=<n> <csv>
    UNIVERSE members=<n> <csv>
    LOCATED <member> receipt=<path> subject=tb2-header verdict=<form>
    REPRODUCED <member> lines=<n>
    LEDGER-GATE rc=0 executed=26 unlocated=0 defects=0   (or skipped=<label>)
    DEFECT <CODE> <detail>
    DEFECTS n=<n>
    TARGET members=<n> located=<n> reproduced=<n> ledger_flipped=<n> defects=<n>
    PREDICATE R81-C1 pass|fail
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

BASE_REV = "4e833e9fee8022d24559535178c6fe32b2cd62f1"  # round-81 base (round-80 tip)
LEDGER = "plans/grader-population-ledger.json"
GRADERS = "corpus/evidence/round52/graders"
TABLE = "plans/round81_probes.json"
EVID = "corpus/evidence/round81"
MINTED_BY = "plans/round81_c1_remint.py"
POPULATION_GATE = "plans/round79_c1_population_ledger.py"
SUBJECT = r"^# tb2 {m} grader probe\b"
ALLOWED_CLASSES = {"file-artifact", "serialization-schema"}
OBS = (r"^CASE ", r"^case=", r"^cases=", r"^MISMATCH ", r"^OBSERVED-U ", r"^VECTOR ",
       r"^PREDICATE R\d+-C\d+ (?:pass|fail)")
FORMS = (("predicate", r"^PREDICATE R\d+-C\d+ pass", re.M),
         ("vectors", r"^VECTOR ", re.M),
         ("cases", r"^(?:CASE |case=)", re.M))
STAMP_RE = re.compile(r"^([A-Z_]+) (.+)$")
REV_RE = re.compile(r"^REV [0-9a-f]{7,40}\s*$")
BEGIN, END = "OBSERVATIONS_BEGIN", "OBSERVATIONS_END"
REQUIRED = ("MEMBER", "SUBJECT_CAPTURE", "SUBJECT_SHA", "TOOL", "TOOL_SHA", "HOST_PYTHON",
            "HOST_OPENSSL", "LANE_TIP", "WORKTREE", "COMMAND", "EXIT", "MINTED_BY",
            "MINTED_BY_SHA")
IMPORT_RE = re.compile(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", re.M)
STDLIB = set(getattr(sys, "stdlib_module_names", ()))


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


def sha256(b: bytes | None) -> str:
    return hashlib.sha256(b or b"").hexdigest()


def obs_lines(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if any(re.match(p, ln) for p in OBS)]


def verdict_form(text: str) -> str | None:
    for name, pattern, flags in FORMS:
        if re.search(pattern, text, flags):
            return name
    return None


def projection(lines: list[str]) -> list[str]:
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


def imports_stdlib_only(src: str) -> bool:
    mods = set()
    for m in IMPORT_RE.finditer(src):
        mods.add((m.group(1) or m.group(2)).split(".")[0])
    return all(mod in STDLIB for mod in mods)


def assert_count(src: str) -> int:
    return len(re.findall(r"^\s*assert\b", src, re.M))


def host_values(python: str) -> dict[str, str]:
    py = subprocess.run([python, "-V"], capture_output=True, text=True)
    py_v = ((py.stdout or "") + (py.stderr or "")).strip().splitlines()
    ossl = subprocess.run(["openssl", "version"], capture_output=True, text=True)
    ossl_v = (ossl.stdout or "").strip() if ossl.returncode == 0 else "absent"
    return {"HOST_PYTHON": py_v[0] if py_v else "unknown", "HOST_OPENSSL": ossl_v or "absent"}


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
    tip = git(lane, "rev-parse", "--verify", "--quiet", "master^{commit}").stdout.strip()
    if not tip:
        raise SystemExit("SETUP unresolved branch master")
    tracked = set(x for x in git(lane, "ls-files", "-z").stdout.split("\0") if x)
    return Tree(lane, "worktree", tip, lambda rel: rel in tracked,
                lambda rel: _fs_bytes(lane, rel))


def rev_tree(lane: Path, rev: str) -> Tree:
    tip = git(lane, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}").stdout.strip()
    if not tip:
        raise SystemExit(f"SETUP unresolved revision {rev!r}")
    tracked = set(git(lane, "ls-tree", "-r", "--name-only", tip).stdout.splitlines())

    def get(rel: str):
        if rel not in tracked:
            return None
        proc = subprocess.run(["git", "-C", str(lane), "cat-file", "-p", f"{tip}:{rel}"],
                              capture_output=True)
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
    return json.loads(proc.stdout), BASE_REV


def derive_universe(base_doc: dict, base_tree: Tree) -> tuple[list[str], dict[str, int], list[str]]:
    rows = base_doc.get("members") or {}
    cand: list[str] = []
    asserts: dict[str, int] = {}
    for m, row in sorted(rows.items()):
        if not isinstance(row, dict):
            continue
        if row.get("status") != "unexecuted" or row.get("reason") != "unattempted":
            continue
        if not set(row.get("classes") or []) <= ALLOWED_CLASSES:
            continue
        rel = f"{GRADERS}/{m}/tests/test_outputs.py"
        raw = base_tree.read_bytes(rel)
        if raw is None:
            continue
        src = raw.decode("utf-8", "replace")
        if not imports_stdlib_only(src):
            continue
        cand.append(m)
        asserts[m] = assert_count(src)
    if not cand:
        return [], {}, []
    top = max(asserts.values())
    universe = [m for m in cand if asserts[m] == top]
    return universe, asserts, cand


def render_argv(spec: dict, member: str, work: Path) -> list[str]:
    w = work / f"{member}.work"
    w.mkdir(parents=True, exist_ok=True)
    out = work / f"{member}.stdout.txt"
    return [a.replace("{work}", str(w)).replace("{out}", str(out)).replace("{member}", member)
            for a in spec["argv"]]


def run_probe(tree: Tree, member: str, spec: dict, python: str, work: Path) -> tuple[int, str]:
    cmd = [python, spec["tool"]] + render_argv(spec, member, work)
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


def check(tree: Tree, base_doc: dict, table: dict, python: str, work: Path,
          reproduce: bool = True, verbose: bool = True) -> tuple[list[tuple[str, str]], dict]:
    defects: list[tuple[str, str]] = []
    universe, asserts, cand = derive_universe(base_doc, tree)
    ledger = json.loads(tree.read(LEDGER) or "{}")
    cur = ledger.get("members") or {}
    all_members = list((base_doc.get("members") or {}))
    stats = {"members": len(universe), "located": 0, "reproduced": 0, "ledger_flipped": 0}
    print(f"CANDIDATES n={len(cand)} rule=stdlib-only-unattempted-max-asserts "
          f"asserts={max(asserts.values()) if asserts else 0} {','.join(cand)}")
    print(f"UNIVERSE members={len(universe)} {','.join(universe)}")
    if not universe:
        defects.append(("UNIVERSE-EMPTY", "no candidate at the base revision"))
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
        capture = f"{GRADERS}/{m}/tests/test_outputs.py"
        if stamp.get("SUBJECT_CAPTURE") != capture:
            add("SUBJECT-CAPTURE", repr(stamp.get("SUBJECT_CAPTURE")))
        if sha256(tree.read_bytes(capture)) != stamp.get("SUBJECT_SHA"):
            add("SUBJECT-SHA-MISMATCH", capture)
        spec = table.get("members", {}).get(m)
        if spec is None:
            add("PROBE-TABLE-MISSING", "no frozen probe row")
            defects.extend(md)
            continue
        if stamp.get("TOOL") != spec["tool"]:
            add("TOOL-PATH", f"{stamp.get('TOOL')} != {spec['tool']}")
        if not tree.tracked(spec["tool"]):
            add("TOOL-UNTRACKED", spec["tool"])
        elif sha256(tree.read_bytes(spec["tool"])) != stamp.get("TOOL_SHA"):
            add("TOOL-SHA-MISMATCH", spec["tool"])
        if stamp.get("MINTED_BY") != MINTED_BY:
            add("MINTED-BY", repr(stamp.get("MINTED_BY")))
        elif not tree.tracked(MINTED_BY) or sha256(tree.read_bytes(MINTED_BY)) != stamp.get(
                "MINTED_BY_SHA"):
            add("MINTED-BY-SHA-MISMATCH", MINTED_BY)
        host = host_values(python)
        if stamp.get("HOST_PYTHON") != host["HOST_PYTHON"]:
            add("HOST-PYTHON-MISMATCH", f"{stamp.get('HOST_PYTHON')!r} != {host['HOST_PYTHON']!r}")
        if stamp.get("HOST_OPENSSL") != host["HOST_OPENSSL"]:
            add("HOST-OPENSSL-MISMATCH",
                f"{stamp.get('HOST_OPENSSL')!r} != {host['HOST_OPENSSL']!r}")
        if tree.label != "fixture":
            tip = stamp.get("LANE_TIP", "")
            if not tip:
                add("LANE-TIP-ABSENT", "-")
            else:
                anc = git(tree.root, "merge-base", "--is-ancestor", tip, tree.tip)
                if anc.returncode != 0:
                    add("LANE-TIP-UNREACHABLE", f"{tip} not an ancestor of {tree.tip}")
            dirty = git(tree.root, "status", "--porcelain").stdout.strip()
            if stamp.get("WORKTREE") != "clean":
                add("WORKTREE-STAMP", repr(stamp.get("WORKTREE")))
            elif dirty and reproduce:
                add("WORKTREE-DIRTY", dirty.splitlines()[0][:80])
        if stamp.get("EXIT") != "0":
            add("EXIT-NONZERO", repr(stamp.get("EXIT")))
        if spec["tool"] not in stamp.get("COMMAND", ""):
            add("COMMAND-TOOLLESS", repr(stamp.get("COMMAND")))
        form = verdict_form("\n".join(block))
        if not block:
            add("OBS-EMPTY", rel)
        elif any(not any(re.match(p, ln) for p in OBS) for ln in block if ln.strip()):
            add("OBS-FOREIGN-LINE", block[0][:60])
        if not md:
            stats["located"] += 1
        if reproduce and not md:
            rc, out = run_probe(tree, m, spec, python, work)
            if rc != 0:
                add("REPRODUCTION-EXIT", f"rc={rc}")
            elif projection(out.splitlines()) != projection(block):
                add("REPRODUCTION-MISMATCH", "projection differs")
            else:
                stats["reproduced"] += 1
        row = cur.get(m) or {}
        if row.get("status") != "executed":
            add("LEDGER-NOT-EXECUTED", repr(row.get("status")))
        else:
            stats["ledger_flipped"] += 1
            if row.get("receipt") != rel:
                add("LEDGER-RECEIPT", repr(row.get("receipt")))
            if row.get("subject") != "tb2-header":
                add("LEDGER-SUBJECT", repr(row.get("subject")))
            if row.get("verdict") != form:
                add("LEDGER-VERDICT", f"{row.get('verdict')} != {form}")
            if row.get("round") != 81:
                add("LEDGER-ROUND", repr(row.get("round")))
        if verbose:
            print(f"LOCATED {m} receipt={rel} subject={'tb2-header' if not any(c == 'SUBJECT-ABSENT' for c, _ in md) else '-'} "
                  f"verdict={form}")
            if not md and reproduce:
                print(f"REPRODUCED {m} lines={len(projection(block))}")
        defects.extend(md)
    return defects, stats


def population_gate(tree: Tree, python: str, work: Path) -> tuple[int | None, str]:
    if tree.label != "worktree":
        return None, "skipped=" + tree.label
    proc = subprocess.run([python, POPULATION_GATE, "--lane", str(tree.root)],
                          capture_output=True, text=True, cwd=str(tree.root))
    tail = (proc.stdout or "").strip().splitlines()
    line = next((ln for ln in tail if ln.startswith("LEDGER rows=")), "")
    return proc.returncode, line or (proc.stderr or "").strip()[:120]


def run_verdict(lane: Path, rev: str, python: str, work: Path, quiet: bool) -> int:
    tree = worktree_tree(lane) if rev == "worktree" else rev_tree(lane, rev)
    base_doc, label = load_base_doc(lane, None)
    table = json.loads(tree.read(TABLE) or "{}")
    defects, stats = check(tree, base_doc, table, python, work, verbose=not quiet)
    rc, pg = population_gate(tree, python, work)
    if rc is None:
        print(f"LEDGER-GATE {pg}")
    elif rc != 0:
        defects.append(("LEDGER-GATE-FAIL", f"rc={rc} {pg}"))
        print(f"LEDGER-GATE rc={rc} {pg}")
    else:
        m = re.search(r"executed=(\d+)", pg)
        expect = 26
        if m and int(m.group(1)) != expect:
            defects.append(("LEDGER-POPULATION", f"executed={m.group(1)} != {expect}"))
        print(f"LEDGER-GATE rc=0 {pg}")
    for code, detail in defects:
        print(f"DEFECT {code} {detail}")
    print(f"DEFECTS n={len(defects)}")
    print(f"TARGET members={stats['members']} located={stats['located']} "
          f"reproduced={stats['reproduced']} ledger_flipped={stats['ledger_flipped']} "
          f"defects={len(defects)}")
    ok = (not defects and stats["located"] == stats["members"]
          and stats["reproduced"] == stats["members"]
          and stats["ledger_flipped"] == stats["members"])
    print(f"PREDICATE R81-C1 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


# ---------------------------------------------------------------- fixture battery

TOOL_SRC = '''#!/usr/bin/env python3
import sys
print("REV 0123456789abcdef")
for line in (
    "CASE exact-table predicted=P observed=P rc=0",
    "CASE missing-file predicted=F observed=F rc=1",
    "cases=2 observed_pass=1 observed_fail=1 mismatches=0",
    "PREDICATE R81-C1 pass",
):
    print(line)
sys.exit(0)
'''

DRIVER_SRC = "# fixture driver\n"

CAPTURE_TEMPLATE = '''from pathlib import Path


def test_a():
    assert Path("/app/x").exists()
'''

CAPTURE_OTHER = '''from pathlib import Path


def test_a():
    assert Path("/app/y").exists()
    assert 1 == 1
    assert 2 == 2
    assert 3 == 3
    assert 4 == 4
'''


def fixture(root: Path, *, receipt: bool = True, ledger_status: str = "executed",
            ledger_round: int = 81, host_python: str | None = None, host_openssl: str | None = None,
            exit_code: str = "0", block_attrs: str = "own", extra_capture: bool = False) -> None:
    host = host_values(sys.executable)
    m1, m2 = "log-summary-date-ranges", "vulnerable-secret"
    cap1 = CAPTURE_OTHER if block_attrs == "other" else CAPTURE_TEMPLATE
    files = {
        f"{GRADERS}/{m1}/tests/test_outputs.py": CAPTURE_TEMPLATE,
        f"{GRADERS}/{m2}/tests/test_outputs.py": cap1,
        "plans/round81_probe_tool.py": TOOL_SRC,
        MINTED_BY: DRIVER_SRC,
    }
    if extra_capture:
        files[f"{GRADERS}/code-from-image/tests/test_outputs.py"] = CAPTURE_OTHER.replace(
            "y", "z")
    base_rows = {
        m1: {"classes": ["file-artifact"], "reason": "unattempted", "status": "unexecuted"},
        m2: {"classes": ["file-artifact", "serialization-schema"], "reason": "unattempted",
             "status": "unexecuted"},
        "already-done": {"classes": ["file-artifact"], "reason": "unattempted", "status": "executed"},
    }
    if extra_capture:
        base_rows["code-from-image"] = {"classes": ["file-artifact"], "reason": "unattempted",
                                        "status": "unexecuted"}
    cur_rows = json.loads(json.dumps(base_rows))
    for m in (m1, m2):
        cur_rows[m] = {"classes": base_rows[m]["classes"], "receipt": f"{EVID}/{m}-probe.txt",
                       "round": ledger_round, "status": ledger_status, "subject": "tb2-header",
                       "verdict": "predicate"}
    files[LEDGER] = json.dumps({"members": cur_rows})
    files["plans/round81-base-ledger.json"] = json.dumps({"members": base_rows})
    files[TABLE] = json.dumps({"members": {
        m1: {"tool": "plans/round81_probe_tool.py", "argv": ["--m", "{member}"], "timeout": 60},
        m2: {"tool": "plans/round81_probe_tool.py", "argv": ["--m", "{member}"], "timeout": 60},
    }})
    if receipt:
        for m in (m1, m2):
            cap = f"{GRADERS}/{m}/tests/test_outputs.py"
            stamp = "\n".join([
                f"# tb2 {m} grader probe (round 81)",
                f"MEMBER {m}",
                f"SUBJECT_CAPTURE {cap}",
                f"SUBJECT_SHA {hashlib.sha256(files[cap].encode()).hexdigest()}",
                "TOOL plans/round81_probe_tool.py",
                f"TOOL_SHA {hashlib.sha256(TOOL_SRC.encode()).hexdigest()}",
                f"HOST_PYTHON {host_python or host['HOST_PYTHON']}",
                f"HOST_OPENSSL {host_openssl or host['HOST_OPENSSL']}",
                "LANE_TIP fixture",
                "WORKTREE clean",
                "COMMAND python3 plans/round81_probe_tool.py --m " + m,
                f"EXIT {exit_code}",
                f"MINTED_BY {MINTED_BY}",
                f"MINTED_BY_SHA {hashlib.sha256(DRIVER_SRC.encode()).hexdigest()}",
                BEGIN,
            ])
            block = ("\n".join([
                "CASE exact-table predicted=P observed=P rc=0",
                "CASE missing-file predicted=F observed=F rc=1",
                "cases=2 observed_pass=1 observed_fail=1 mismatches=0",
                "PREDICATE R81-C1 pass",
            ]) if block_attrs == "own" else "\n".join([
                "CASE a predicted=P observed=P rc=0",
                "PREDICATE R81-C1 pass",
            ]))
            files[f"{EVID}/{m}-probe.txt"] = stamp + "\n" + block + "\n" + END + "\n"
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


def fixture_check(root: Path, mutate: str | None = None) -> tuple[list[tuple[str, str]], dict]:
    tree = fixture_tree(root)
    base_doc = json.loads((root / "plans/round81-base-ledger.json").read_text())
    table = json.loads(tree.read(TABLE) or "{}")
    if mutate == "drop-receipt":
        (root / f"{EVID}/log-summary-date-ranges-probe.txt").unlink()
    elif mutate == "strip-stamp":
        p = root / f"{EVID}/log-summary-date-ranges-probe.txt"
        p.write_text(p.read_text().replace(f"HOST_PYTHON ", "HOST-PYTHON-DROPPED "))
    elif mutate == "wrong-subject-sha":
        p = root / f"{EVID}/vulnerable-secret-probe.txt"
        p.write_text(re.sub(r"^SUBJECT_SHA .*$", "SUBJECT_SHA " + "0" * 64, p.read_text(), flags=re.M))
    elif mutate == "wrong-tool-sha":
        p = root / f"{EVID}/vulnerable-secret-probe.txt"
        p.write_text(re.sub(r"^TOOL_SHA .*$", "TOOL_SHA " + "0" * 64, p.read_text(), flags=re.M))
    elif mutate == "host-python":
        p = root / f"{EVID}/log-summary-date-ranges-probe.txt"
        p.write_text(re.sub(r"^HOST_PYTHON .*$", "HOST_PYTHON Python 2.7.0", p.read_text(), flags=re.M))
    elif mutate == "exit":
        p = root / f"{EVID}/log-summary-date-ranges-probe.txt"
        p.write_text(re.sub(r"^EXIT .*$", "EXIT 1", p.read_text(), flags=re.M))
    elif mutate == "ledger-round":
        doc = json.loads(tree.read(LEDGER))
        doc["members"]["log-summary-date-ranges"]["round"] = 80
        (root / LEDGER).write_text(json.dumps(doc))
    elif mutate == "ledger-status":
        doc = json.loads(tree.read(LEDGER))
        doc["members"]["log-summary-date-ranges"]["status"] = "unexecuted"
        (root / LEDGER).write_text(json.dumps(doc))
    elif mutate == "foreign-block":
        p = root / f"{EVID}/log-summary-date-ranges-probe.txt"
        p.write_text(p.read_text().replace("CASE exact-table predicted=P observed=P rc=0",
                                           "CASE other-case predicted=P observed=P rc=0"))
    elif mutate == "empty-block":
        p = root / f"{EVID}/vulnerable-secret-probe.txt"
        text = p.read_text()
        p.write_text(re.sub(r"OBSERVATIONS_BEGIN\n.*?OBSERVATIONS_END",
                            f"{BEGIN}\n{END}", text, flags=re.S))
    return check(tree, base_doc, table, sys.executable, root / "_w", reproduce=True,
                 verbose=False)


def selftest(work: Path) -> int:
    cases = [
        ("green", None, 0),
        ("drop-receipt", "drop-receipt", 1),
        ("strip-stamp", "strip-stamp", 1),
        ("wrong-subject-sha", "wrong-subject-sha", 1),
        ("wrong-tool-sha", "wrong-tool-sha", 1),
        ("host-python", "host-python", 1),
        ("exit", "exit", 1),
        ("ledger-round", "ledger-round", 1),
        ("ledger-status", "ledger-status", 1),
        ("foreign-block", "foreign-block", 1),
        ("empty-block", "empty-block", 1),
    ]
    failures = 0
    red = 0
    for name, mutate, want_defects in cases:
        root = work / f"st-{name}"
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        fixture(root)
        defects, _stats = fixture_check(root, mutate)
        got = len(defects)
        ok = (got == 0) if want_defects == 0 else (got > 0)
        if want_defects:
            red += 1
        if not ok:
            failures += 1
            print(f"SELFTEST-FAIL {name} defects={got} {defects[:2]}")
        shutil.rmtree(root)
    print(f"SELFTEST cases={len(cases)} red={red} failures={failures}")
    return 0 if failures == 0 else 1


def mutants(work: Path) -> int:
    names = ["drop-receipt", "strip-stamp", "wrong-subject-sha", "wrong-tool-sha", "host-python",
             "exit", "ledger-round", "ledger-status", "foreign-block", "empty-block"]
    killed = survived = 0
    for name in names:
        root = work / f"mu-{name}"
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        fixture(root)
        defects, _stats = fixture_check(root, name)
        if defects:
            killed += 1
        else:
            survived += 1
            print(f"MUTANT-SURVIVED {name}")
        shutil.rmtree(root)
    print(f"MUTANTS real={len(names)} killed={killed} survived={survived}")
    return 0 if survived == 0 else 1


def control(work: Path, name: str) -> int:
    root = work / f"ctl-{name}"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    if name == "flip-ledger-only":
        fixture(root, receipt=False)
    elif name == "header-only":
        fixture(root, receipt=False)
        for m in ("log-summary-date-ranges", "vulnerable-secret"):
            cap = f"{GRADERS}/{m}/tests/test_outputs.py"
            text = (root / cap).read_text()
            p = root / f"{EVID}/{m}-probe.txt"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f"# tb2 {m} grader probe (round 81)\n" + text[:0] +
                         f"MEMBER {m}\nEXIT 0\n")
    elif name == "copy-observations":
        fixture(root, block_attrs="other")
    defects, stats = fixture_check(root)
    reached = (not defects and stats["located"] == stats["members"]
               and stats["ledger_flipped"] == stats["members"])
    print(f"CONTROL {name} located={stats['located']} ledger_flipped={stats['ledger_flipped']} "
          f"defects={len(defects)} codes={','.join(sorted({c for c, _ in defects}))} "
          f"target_reached={reached}")
    print(f"PREDICATE R81-C1 {'pass' if reached else 'fail'}")
    shutil.rmtree(root)
    return 0 if not reached else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--work", default=None)
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--control-flip-ledger-only", action="store_true")
    ap.add_argument("--control-header-only", action="store_true")
    ap.add_argument("--control-copy-observations", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    work = Path(a.work) if a.work else Path("/fast/scratch/hyaku/kengaku-r81/gate-work")
    work.mkdir(parents=True, exist_ok=True)
    lane = Path(a.lane).resolve()
    if a.selftest:
        return selftest(work)
    if a.mutants:
        return mutants(work)
    for name in ("flip-ledger-only", "header-only", "copy-observations"):
        if getattr(a, "control_" + name.replace("-", "_")):
            return control(work, name)
    return run_verdict(lane, a.rev, a.python, work, a.quiet)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
