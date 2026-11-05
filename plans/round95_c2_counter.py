#!/usr/bin/env python3
"""R95-C2 counter — freeze-integrity gate v2, judged through its public CLI only, against the
fourteen false gates the round-94 wave built that pass the round-94 counter 5/5.

The gate under test is `plans/round94_freeze_integrity.py` read at --rev (unchanged since round
94), or a file named by --tool-file, which is how every false-gate control runs through this
same path. Five legs:

  W1 history   (a) paths mode on the round-92 history (freeze B2 f0018773, tip 1df76536):
               broken=3 intact=1, exactly round92_c1_replay.py intact, rc 1;
               (b) claims mode on the round-93 history (freeze F d8d0a4b8, tip 7b8719f3,
               plans/round-93-claims.md): instruments=9 intact=9 broken=0, rc 0
  W2 fixtures  twenty counter-owned fixture repos through the CLI: the twelve round-94 fixtures
               plus eight that model the round-94 wave's false gates — paths-mode duplicate
               (F1, M01), paths-mode path absent at the freeze (F2, F6b), octopus merge
               discarding a side edit (F3b), delete then identical re-add (F4b), rename with
               identical bytes (F5), a table row with a space in its path (F7), an
               unterminated table block (M02), paths-mode edit (paths-mode breach polarity)
  W3 battery   the gate's in-process battery is DRIVEN, not read: (a) the unmutated gate prints
               `SELFTEST cases=15 ok=15` in both W1 runs (echoed); (b) for each of three probe
               mutations of the gate's shared functions (every occurrence of the anchor
               replaced: `--full-history` dropped, touched threshold raised to 2, duplicate-path
               guard disabled) the mutated gate, run on the w2-intact fixture, must report a red
               battery — a `SELFTEST cases=15 ok=<15` line, `PREDICATE freeze-integrity fail`,
               rc 1. A missing anchor is RED. A stubbed battery (X1), a non-fatal battery (M07)
               or a concealed one (M19, M20) keeps printing green or exits 0 and is RED here.
  W4 self      claims mode on plans/round-95-claims.md: --freeze = the single commit that
               added that file, --rev REV; instruments >= 8, broken=0, rc 0
  W5 mutants   ten CLI-path mutants generated from the gate under test (evaluate and
               parse_table copied as *_cli, one mutation applied to the copy or to main, main
               redirected to it, the battery left honest) must each turn their designated W2
               fixture RED, and the unmutated CLI copy (null) must keep every W2 fixture ok.

Every gate run in W1, W2 and W4 must also print exactly one PREDICATE line agreeing with its exit
code (0 pass, 1 fail, 2 could-not-evaluate); a disagreement is RED (M15 printed pass on a
breach). PREDICATE R95-C2 pass iff W1..W5 all pass. Exit 0 pass, 1 fail, 2 could-not-evaluate.
Usage:  python3 plans/round95_c2_counter.py --lane . --rev REV --work DIR [--tool-file PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOL = "plans/round94_freeze_integrity.py"
CLAIMS = "plans/round-95-claims.md"
R92_FREEZE = "f0018773f507f363854123856990f8ff8a87eb8c"
R92_TIP = "1df7653633bd4c5a5f373d139f9f1ed02e0f9c07"
R92_PATHS = ["plans/round92_c1_replay.py", "plans/round92_c2_conformance.py",
             "plans/round92_burndown.py", "plans/round91_counter_pin.py"]
R92_INTACT = {"plans/round92_c1_replay.py"}
R93_FREEZE = "d8d0a4b849f3d031a6ad5525e18611a097e08bfe"
R93_TIP = "7b8719f3eefb3f560add5dd3367b67b7a50a45da"
R93_CLAIMS = "plans/round-93-claims.md"
SELFTEST = "SELFTEST cases=15 ok=15"
SELFTEST_LINE = re.compile(r"^SELFTEST cases=(\d+) ok=(\d+)$", re.M)
PRED_LINE = re.compile(r"^PREDICATE freeze-integrity (\S+)$", re.M)
PRED_FOR_RC = {0: "pass", 1: "fail", 2: "could-not-evaluate"}
MIN_SELF_INSTRUMENTS = 8
BODY = b"def count():\n    return 3\n"
GOOD = hashlib.sha256(BODY).hexdigest()
GIT_ID = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
          "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]

# (name, anchor, replacement, where, designated W2 fixture)
MUTANTS = [
    ("K1-head-not-rev", "    t = resolve(root, rev)\n", "    t = resolve(root, \"HEAD\")\n", "cli", "w2-rev-below-head"),
    ("K2-rev-minus-1", "    f = resolve(root, freeze)\n", "    f = resolve(root, rev + \"~1\")\n", "cli", "w2-edit-revert-unrelated"),
    ("K3-table-at-rev", "        text = blob(root, f, claims)\n", "        text = blob(root, t, claims)\n", "cli", "w2-lie-repaired"),
    ("K4-cne-exit0-pass",
     "        print(f\"DEFECT SETUP {error}\")\n        print(\"PREDICATE freeze-integrity could-not-evaluate\")\n        return 2\n",
     "        print(f\"DEFECT SETUP {error}\")\n        print(\"PREDICATE freeze-integrity pass\")\n        return 0\n",
     "main", "w2-not-ancestor"),
    ("K5-no-full-history", "\"rev-list\", \"--full-history\", ", "\"rev-list\", ", "cli", "w2-treesame-merge"),
    ("K6-second-block-ignored", "    if blocks > 1:\n", "    if blocks > 99:\n", "cli", "w2-second-block"),
    ("K7-duplicate-row-accepted", "    if dups:\n", "    if False and dups:\n", "cli", "w2-duplicate-row"),
    ("K8-paths-dup-accepted", "        if len({p for _, p in table}) != len(table):\n",
     "        if False and len({p for _, p in table}) != len(table):\n", "cli", "w2-paths-dup"),
    ("K9-unterminated-accepted", "    if inside:\n        raise CouldNotEvaluate(",
     "    if False and inside:\n        raise CouldNotEvaluate(", "cli", "w2-unterminated"),
    ("K10-absent-at-freeze-skipped",
     "            if b is None:\n                raise CouldNotEvaluate(f\"path {p} absent at freeze {f[:12]}\")\n",
     "            if b is None:\n                continue\n", "cli", "w2-paths-absent"),
]

# W3 probe mutations of the gate's SHARED functions (all occurrences): each must drive the
# honest battery red (B11, B02, B13 respectively in round94_freeze_integrity.py).
BATTERY_PROBES = [
    ("P1-no-full-history", "\"rev-list\", \"--full-history\", ", "\"rev-list\", "),
    ("P2-touched-threshold-2", "        if touched:\n", "        if touched > 1:\n"),
    ("P3-dups-ignored", "    if dups:\n", "    if False and dups:\n"),
]


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=120)


def run_tool(tool: Path, lane: Path, work: Path, extra: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run([sys.executable, "-I", "-B", str(tool), "--lane", str(lane),
                               "--work", str(work), *extra], capture_output=True, text=True, timeout=600)
    except (OSError, subprocess.SubprocessError) as error:
        return -1, f"tool-run-error {error}"
    return proc.returncode, proc.stdout


def summary(out: str) -> tuple[int, int, int] | None:
    m = re.search(r"^FREEZE-INTEGRITY instruments=(\d+) intact=(\d+) broken=(\d+)$", out, re.M)
    return tuple(int(x) for x in m.groups()) if m else None


def pred_ok(rc: int, out: str) -> bool:
    """Exactly one gate PREDICATE line, and it agrees with the exit code."""
    lines = PRED_LINE.findall(out)
    return len(lines) == 1 and PRED_FOR_RC.get(rc) == lines[0]


def fx_git(d: Path, *args: str) -> None:
    top = git(d, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if Path(top).resolve() != d.resolve():
        raise SystemExit(f"fixture toplevel {top} != {d}")
    subprocess.run(["git", "-C", str(d), *GIT_ID, *args], check=True, capture_output=True)


def fx_commit(d: Path, msg: str) -> str:
    fx_git(d, "add", "-A")
    fx_git(d, "commit", "-q", "--allow-empty", "-m", msg)
    return git(d, "rev-parse", "HEAD").stdout.decode().strip()


def head(d: Path) -> str:
    return git(d, "rev-parse", "HEAD").stdout.decode().strip()


def claims_text(rows: list[tuple[str, str]], extra: str = "", close: bool = True) -> str:
    body = "\n".join(f"{s}  {p}" for s, p in rows)
    return f"# claims\n\n```frozen-instruments\n{body}\n" + ("```\n" if close else "") + extra


def build_fixture(root: Path, name: str) -> tuple[Path, str, str]:
    """Return (repo, freeze, rev) for one named W2 fixture."""
    d = root / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    subprocess.run(["git", "-C", str(d), "init", "-q", "-b", "main"], check=True, capture_output=True)
    (d / "probe.py").write_bytes(BODY)
    (d / "notes.md").write_text("notes\n")
    table = [("f" * 64 if name in ("w2-lying-table", "w2-lie-repaired") else GOOD, "probe.py")]
    extra = ""
    close = True
    if name == "w2-second-block":
        extra = "\n```frozen-instruments\n" + hashlib.sha256(b"notes\n").hexdigest() + "  notes.md\n```\n"
    if name == "w2-duplicate-row":
        table = table + table
    if name == "w2-spaced-row":
        (d / "my file.py").write_bytes(BODY)
        table = table + [(GOOD, "my file.py")]
    if name == "w2-unterminated":
        close = False
    (d / "claims.md").write_text(claims_text(table, extra, close))
    f = fx_commit(d, "freeze")
    edit = lambda: (d / "probe.py").write_bytes(b"def count():\n    return 4\n")
    rev = None
    if name in ("w2-edited", "w2-paths-edited"):
        edit()
    elif name == "w2-edit-revert":
        edit()
        fx_commit(d, "edit")
        (d / "probe.py").write_bytes(BODY)
    elif name == "w2-unrelated":
        (d / "notes.md").write_text("more notes\n")
    elif name == "w2-rev-below-head":
        rev = fx_commit(d, "unrelated empty")
        edit()
    elif name == "w2-edit-revert-unrelated":
        edit()
        fx_commit(d, "edit")
        (d / "probe.py").write_bytes(BODY)
        fx_commit(d, "revert")
        (d / "notes.md").write_text("more notes\n")
    elif name == "w2-lie-repaired":
        (d / "claims.md").write_text(claims_text([(GOOD, "probe.py")]))
    elif name == "w2-treesame-merge":
        fx_git(d, "checkout", "-q", "-b", "side")
        edit()
        fx_commit(d, "side edit")
        fx_git(d, "checkout", "-q", "main")
        fx_git(d, "merge", "-q", "-s", "ours", "--no-edit", "side")
        return d, f, head(d)
    elif name == "w2-not-ancestor":
        fx_git(d, "checkout", "-q", "--orphan", "other")
    elif name == "w2-paths-absent":
        (d / "later.py").write_bytes(BODY)
        fx_commit(d, "add later.py after the freeze")
        (d / "later.py").write_bytes(b"def count():\n    return 5\n")
    elif name == "w2-octopus":
        fx_git(d, "checkout", "-q", "-b", "side1")
        edit()
        fx_commit(d, "side1 edits probe.py")
        fx_git(d, "checkout", "-q", "main")
        fx_git(d, "checkout", "-q", "-b", "side2")
        (d / "notes.md").write_text("side2 notes\n")
        fx_commit(d, "side2 unrelated")
        fx_git(d, "checkout", "-q", "main")
        fx_git(d, "merge", "-q", "-s", "ours", "--no-edit", "side1", "side2")
        return d, f, head(d)
    elif name == "w2-delete-readd":
        (d / "probe.py").unlink()
        fx_commit(d, "delete probe.py")
        (d / "probe.py").write_bytes(BODY)
    elif name == "w2-rename":
        fx_git(d, "mv", "probe.py", "renamed.py")
    t = fx_commit(d, "after")
    return d, f, (rev or t)


CLAIMS_ARGS = ["--claims", "claims.md"]
# (name, gate args, want_rc, want_summary; None summary = could-not-evaluate expected)
W2_SPECS = [
    ("w2-intact", CLAIMS_ARGS, 0, (1, 1, 0)),
    ("w2-edited", CLAIMS_ARGS, 1, (1, 0, 1)),
    ("w2-edit-revert", CLAIMS_ARGS, 1, (1, 0, 1)),
    ("w2-lying-table", CLAIMS_ARGS, 1, (1, 0, 1)),
    ("w2-unrelated", CLAIMS_ARGS, 0, (1, 1, 0)),
    ("w2-rev-below-head", CLAIMS_ARGS, 0, (1, 1, 0)),
    ("w2-edit-revert-unrelated", CLAIMS_ARGS, 1, (1, 0, 1)),
    ("w2-lie-repaired", CLAIMS_ARGS, 1, (1, 0, 1)),
    ("w2-treesame-merge", CLAIMS_ARGS, 1, (1, 0, 1)),
    ("w2-second-block", CLAIMS_ARGS, 2, None),
    ("w2-duplicate-row", CLAIMS_ARGS, 2, None),
    ("w2-not-ancestor", CLAIMS_ARGS, 2, None),
    ("w2-paths-dup", ["--paths", "probe.py", "probe.py"], 2, None),
    ("w2-paths-absent", ["--paths", "probe.py", "later.py"], 2, None),
    ("w2-paths-edited", ["--paths", "probe.py", "notes.md"], 1, (2, 1, 1)),
    ("w2-octopus", CLAIMS_ARGS, 1, (1, 0, 1)),
    ("w2-delete-readd", CLAIMS_ARGS, 1, (1, 0, 1)),
    ("w2-rename", CLAIMS_ARGS, 1, (1, 0, 1)),
    ("w2-spaced-row", CLAIMS_ARGS, 2, None),
    ("w2-unterminated", CLAIMS_ARGS, 2, None),
]


def run_w2(tool: Path, work: Path, tag: str) -> dict[str, tuple[bool, str]]:
    results: dict[str, tuple[bool, str]] = {}
    fx_root = work / f"fx-{tag}"
    for name, args, want_rc, want_s in W2_SPECS:
        d, f, t = build_fixture(fx_root, name)
        rc, out = run_tool(tool, d, work / f"run-{tag}-{name}", ["--freeze", f, "--rev", t, *args])
        s = summary(out)
        if want_s is None:
            ok = rc == 2 and s is None
        else:
            ok = rc == want_rc and s == want_s
        p_ok = pred_ok(rc, out)
        ok = ok and p_ok
        results[name] = (ok, f"rc={rc} want_rc={want_rc} summary={s} want={want_s} predicate_line_ok={p_ok}")
    shutil.rmtree(fx_root, ignore_errors=True)
    return results


def top_level_block(src: str, name: str) -> str | None:
    m = re.search(rf"^def {name}\(.*?(?=^\S)", src, re.M | re.S)
    return m.group(0) if m else None


def make_mutant(src: str, anchor: str | None, repl: str | None, where: str | None) -> str | None:
    """CLI-only copy: evaluate/parse_table copied as *_cli; the mutation hits the copy (or main)."""
    ev = top_level_block(src, "evaluate")
    pt = top_level_block(src, "parse_table")
    mn = top_level_block(src, "main")
    if not ev or not pt or not mn:
        return None
    cli = (pt.replace("def parse_table(", "def parse_table_cli(", 1)
           + ev.replace("def evaluate(", "def evaluate_cli(", 1).replace("parse_table(", "parse_table_cli("))
    new_main = mn
    if anchor is not None:
        if where == "cli":
            if cli.count(anchor) != 1:
                return None
            cli = cli.replace(anchor, repl)
        else:
            if new_main.count(anchor) != 1:
                return None
            new_main = new_main.replace(anchor, repl)
    call = "evaluate(Path(a.lane)"
    if new_main.count(call) != 1:
        return None
    new_main = new_main.replace(call, "evaluate_cli(Path(a.lane)")
    return src.replace(mn, cli + "\n" + new_main)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--work", required=True)
    ap.add_argument("--tool-file")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve()
    if work == lane or lane in work.parents:
        print(f"DEFECT SETUP --work inside the lane {work}")
        print("PREDICATE R95-C2 could-not-evaluate")
        return 2
    work.mkdir(parents=True, exist_ok=True)
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{a.rev}^{{commit}}")
    if proc.returncode != 0:
        print(f"DEFECT SETUP unresolved-revision {a.rev}")
        print("PREDICATE R95-C2 could-not-evaluate")
        return 2
    rev = proc.stdout.decode().strip()
    tool = work / "gate-under-test.py"
    if a.tool_file:
        shutil.copyfile(a.tool_file, tool)
        print(f"TOOL from-file {a.tool_file} sha256={hashlib.sha256(tool.read_bytes()).hexdigest()}")
    else:
        b = git(lane, "show", f"{rev}:{TOOL}")
        if b.returncode != 0:
            print(f"TOOL absent at {rev[:12]}")
            for leg in ("W1", "W2", "W3", "W4", "W5"):
                print(f"{leg} fail tool-absent")
            print("TARGET legs_passed=0 of 5")
            print("PREDICATE R95-C2 fail")
            return 1
        tool.write_bytes(b.stdout)
        print(f"TOOL {TOOL}@{rev[:12]} sha256={hashlib.sha256(b.stdout).hexdigest()}")

    legs: dict[str, bool] = {}
    # W1 history
    rc_a, out_a = run_tool(tool, lane, work / "w1a", ["--freeze", R92_FREEZE, "--rev", R92_TIP, "--paths", *R92_PATHS])
    s_a = summary(out_a)
    intact_a = {m.group(1) for m in re.finditer(r"^INSTRUMENT (\S+) .* verdict=intact$", out_a, re.M)}
    w1a = rc_a == 1 and s_a == (4, 1, 3) and intact_a == R92_INTACT and pred_ok(rc_a, out_a)
    rc_b, out_b = run_tool(tool, lane, work / "w1b", ["--freeze", R93_FREEZE, "--rev", R93_TIP, "--claims", R93_CLAIMS])
    s_b = summary(out_b)
    w1b = rc_b == 0 and s_b == (9, 9, 0) and pred_ok(rc_b, out_b)
    legs["W1"] = w1a and w1b
    print(f"W1a r92 {'ok' if w1a else 'RED'} rc={rc_a} summary={s_a} intact={sorted(intact_a)} predicate_line_ok={pred_ok(rc_a, out_a)}")
    print(f"W1b r93 {'ok' if w1b else 'RED'} rc={rc_b} summary={s_b} predicate_line_ok={pred_ok(rc_b, out_b)}")
    print(f"W1 {'pass' if legs['W1'] else 'fail'}")

    # W2 fixtures
    w2 = run_w2(tool, work, "real")
    for name, (ok, detail) in w2.items():
        print(f"W2 {name} {'ok' if ok else 'RED'} {detail}")
    legs["W2"] = all(ok for ok, _ in w2.values())
    print(f"W2 {'pass' if legs['W2'] else 'fail'} fixtures={len(w2)} ok={sum(1 for ok, _ in w2.values() if ok)}")

    # W3 battery: (a) green line echoed on the unmutated gate, (b) driven red by probe mutations
    lines_a = re.findall(r"^SELFTEST .*$", out_a, re.M)
    lines_b = re.findall(r"^SELFTEST .*$", out_b, re.M)
    for line in lines_a + lines_b:
        print("W3 echo " + line)
    w3 = lines_a == [SELFTEST] and lines_b == [SELFTEST]
    src = tool.read_text()
    d, f, t = build_fixture(work / "fx-w3", "w2-intact")
    for name, anchor, repl in BATTERY_PROBES:
        if src.count(anchor) < 1:
            w3 = False
            print(f"W3 {name} RED anchor-missing")
            continue
        p = work / f"probe-{name}.py"
        p.write_text(src.replace(anchor, repl))
        rc, out = run_tool(p, d, work / f"run-w3-{name}", ["--freeze", f, "--rev", t, *CLAIMS_ARGS])
        st = SELFTEST_LINE.findall(out)
        red_line = len(st) == 1 and st[0][0] == "15" and int(st[0][1]) < 15
        ok = red_line and rc == 1 and PRED_LINE.findall(out) == ["fail"]
        w3 = w3 and ok
        print(f"W3 {name} {'ok' if ok else 'RED'} rc={rc} selftest={['cases=%s ok=%s' % x for x in st]} "
              f"predicate={PRED_LINE.findall(out)} want=battery-red,rc=1,fail")
    shutil.rmtree(work / "fx-w3", ignore_errors=True)
    legs["W3"] = w3
    print(f"W3 {'pass' if w3 else 'fail'} probes={len(BATTERY_PROBES)}")

    # W4 self-application on this round's own frozen table
    added = [x for x in git(lane, "log", "--diff-filter=A", "--format=%H", rev, "--", CLAIMS).stdout.decode().split() if x]
    if len(added) != 1:
        legs["W4"] = False
        print(f"W4 fail claims-add-commits={len(added)} {CLAIMS} at {rev[:12]}")
    else:
        freeze = added[0]
        rc, out = run_tool(tool, lane, work / "w4", ["--freeze", freeze, "--rev", rev, "--claims", CLAIMS])
        s = summary(out)
        legs["W4"] = rc == 0 and s is not None and s[0] >= MIN_SELF_INSTRUMENTS and s[2] == 0 and pred_ok(rc, out)
        print(f"W4 {'pass' if legs['W4'] else 'fail'} freeze={freeze[:12]} rc={rc} summary={s}")
        for line in out.splitlines():
            if line.startswith("INSTRUMENT "):
                print("W4 " + line)

    # W5 CLI-path mutants of the gate under test
    w5 = True
    null_src = make_mutant(src, None, None, None)
    if null_src is None:
        w5 = False
        print("W5 null RED anchor-missing (evaluate/parse_table/main structure)")
    else:
        p = work / "mutant-null.py"
        p.write_text(null_src)
        res = run_w2(p, work, "null")
        null_ok = all(ok for ok, _ in res.values())
        w5 = w5 and null_ok
        print(f"W5 null {'ok' if null_ok else 'RED'} fixtures_ok={sum(1 for ok, _ in res.values() if ok)} of {len(res)}")
    killed = 0
    for name, anchor, repl, where, target in MUTANTS:
        msrc = make_mutant(src, anchor, repl, where)
        if msrc is None:
            w5 = False
            print(f"W5 {name} RED anchor-missing")
            continue
        p = work / f"mutant-{name}.py"
        p.write_text(msrc)
        res = run_w2(p, work, name)
        red = sorted(n for n, (ok, _) in res.items() if not ok)
        hit = target in red
        killed += 1 if hit else 0
        w5 = w5 and hit
        print(f"W5 {name} {'killed' if hit else 'SURVIVED'} designated={target} red={','.join(red) or '-'}")
    legs["W5"] = w5
    print(f"W5 {'pass' if w5 else 'fail'} mutants={len(MUTANTS)} killed={killed}")

    passed = all(legs.get(k) for k in ("W1", "W2", "W3", "W4", "W5"))
    print(f"TARGET legs_passed={sum(1 for v in legs.values() if v)} of 5")
    print(f"PREDICATE R95-C2 {'pass' if passed else 'fail'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
