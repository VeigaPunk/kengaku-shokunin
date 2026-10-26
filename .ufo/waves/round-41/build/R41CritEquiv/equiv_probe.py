#!/usr/bin/env python3
"""R41CritEquiv scratch probe (critic draft, not a battery module).

For each frozen mutant in plans/round41_c1_verify.py, build an independently written minimal fixture,
run the reference tool and the mutant copy on it, and record: reference rc, mutant rc, the class sets
the frozen counter's own parser reads, whether the declared direction is satisfied, and whether the
mutant's stderr is an unhandled exception.

The pre-freeze witness modules (.ufo/waves/round-41/claims/witness/) are never imported, copied or
read here.
"""
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys

LANE = pathlib.Path(sys.argv[1]).resolve()
S = pathlib.Path(sys.argv[2]).resolve()

spec = importlib.util.spec_from_file_location("c1", LANE / "plans/round41_c1_verify.py")
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
BASE_ENV = {
    "PATH": PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
    "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
    "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00",
}

EV = "corpus/evidence/r/foo-probe.txt"


def sh(argv, cwd=None, env=None):
    r = subprocess.run([str(a) for a in argv], cwd=None if cwd is None else str(cwd),
                       env=env or BASE_ENV, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"fixture build failed: {argv} :: {r.stderr[-400:]}")
    return r


def mklane(d, files, sub=None):
    root = (d / "repo") if sub else (d / "lane")
    root.mkdir(parents=True, exist_ok=True)
    env = dict(BASE_ENV, GIT_CEILING_DIRECTORIES=str(d))
    sh(["git", "init", "-q", "-b", "master"], cwd=root, env=env)
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    sh(["git", "-C", root, "add", "-A"], env=env)
    sh(["git", "-C", root, "commit", "-q", "-m", "fixture"], env=env)
    return (root / sub) if sub else root


def probe_src(name, out, rc=0, runas="python3"):
    return ('"""Stub probe.\n\n  %s plans/%s.py --lane .\n"""\nimport sys\nsys.stdout.write(%r)\nsys.exit(%d)\n'
            % (runas, name, out, rc))


HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")
ROW = ("| S900 | src — https://example.invalid/x | docs | A | sc | {anchor} | t | {status} | 2026-10-25 | "
       "180d | corpus/knowledge/old.md |\n")


def row(anchor="anchor text", status="mined"):
    return ROW.format(anchor=anchor, status=status)


REC = []


def fx(mid, tool, expect, declared, build):
    REC.append({"mid": mid, "tool": tool, "expect": expect, "declared": declared, "build": build})


def b_t02(d):
    lane = mklane(d, {"README.md": "x\n"})
    (d / "w").mkdir(exist_ok=True)
    return ["--lane", str(lane), "--work", str(d / "w")]


def b_t03(d):
    lane = mklane(d, {EV: "X\n", "plans/foo_probe.py": probe_src("foo_probe", "X\n", 3)})
    (d / "w").mkdir(exist_ok=True)
    return ["--lane", str(lane), "--work", str(d / "w")]


def b_t04(d):
    rel = "corpus/evidence/round36/regex-log-probe-first-run.txt"
    lane = mklane(d, {rel: "path /tmp/tmpAAAAAA11/x\n",
                      "plans/regex_log_probe.py": probe_src("regex_log_probe", "path /tmp/tmpBBBBBB22/x\n")})
    (d / "w").mkdir(exist_ok=True)
    return ["--lane", str(lane), "--work", str(d / "w")]


def b_t05(d):
    lane = mklane(d, {EV: "X\n", "plans/foo_probe.py": probe_src("foo_probe", "X\n")})
    (d / "w").mkdir(exist_ok=True)
    return ["--lane", str(lane), "--work", str(d / "w"), "--tamper", "corpus/evidence/nope.txt"]


def b_t06(d):
    lane = mklane(d, {EV: "", "plans/foo_probe.py": probe_src("foo_probe", "")})
    (d / "w").mkdir(exist_ok=True)
    return ["--lane", str(lane), "--work", str(d / "w")]


def b_t07(d):
    lane = mklane(d, {"sub/corpus/evidence/note.md": "x\n", "README.md": "x\n"}, sub="sub")
    (d / "w").mkdir(exist_ok=True)
    return ["--lane", str(lane), "--work", str(d / "w")]


def b_t08(d):
    lane = mklane(d, {EV: "X\n", "plans/foo_probe.py": probe_src("foo_probe", "X\n",
                                                                runas="uv run --no-project python3")})
    (d / "w").mkdir(exist_ok=True)
    return ["--lane", str(lane), "--work", str(d / "w")]


def b_t09(d):
    lane = mklane(d, {EV: "X\n", "plans/foo_probe.py": probe_src("foo_probe", "X\n"),
                      "plans/fooprobe.py": probe_src("fooprobe", "X\n")})
    return ["--lane", str(lane), "--list"]


def b_t10(d):
    lane = mklane(d, {EV: "X\n", "plans/foo_probe.py": probe_src("foo_probe", "X\n")})
    return ["--lane", str(lane), "--list"]


def b_t11(d):
    rel = "corpus/evidence/round35/tb2-grader-probe.txt"
    lane = mklane(d, {rel: "X\n", "plans/tb2_grader_probe.py": probe_src("tb2_grader_probe", "X\n")})
    return ["--lane", str(lane), "--list"]


def b_t12(d):
    lane = mklane(d, {"corpus/evidence/r/foo-probe.log": "X\n"})
    return ["--lane", str(lane), "--list"]


def b_t13(d):
    lane = mklane(d, {EV: "X\n", "plans/foo_probe.py": probe_src("foo_probe", "X\n")})
    (d / "w").mkdir(exist_ok=True)
    return ["--lane", str(lane), "--work", str(d / "w")]


fx("T01", "receipts", 2, "-", b_t02)
fx("T02", "receipts", 2, "-", b_t02)
fx("T03", "receipts", 1, f"differ:{EV}", b_t03)
fx("T04", "receipts", 0, "skip:corpus/evidence/round36/regex-log-probe-first-run.txt:"
                        "declared-nonreproducible-absolute-scratch-paths", b_t04)
fx("T05", "receipts", 2, "-", b_t05)
fx("T06", "receipts", 1, f"equal:{EV} control:unavailable", b_t06)
fx("T07", "receipts", 2, "-", b_t07)
fx("T08", "receipts", 0, f"skip:{EV}:dependency-missing", b_t08)
fx("T09", "receipts", 0, f"skip:{EV}:no-committed-re-run-command", b_t09)
fx("T10", "receipts", 0, f"map:{EV}:derived", b_t10)
fx("T11", "receipts", 0, "map:corpus/evidence/round35/tb2-grader-probe.txt:table", b_t11)
fx("T12", "receipts", 0, "skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command", b_t12)
fx("T13", "receipts", 0, f"equal:{EV} control:differ", b_t13)


def sfiles(d, reg_rows="", pkg_rows=None):
    (d / "reg.md").write_text(HEADER + reg_rows, encoding="utf-8")
    (d / "pkg.md").write_text(HEADER + (row() if pkg_rows is None else pkg_rows), encoding="utf-8")


def squote(d):
    (d / "q.md").write_text(HEADER + row(anchor='l.1: "fixture quote words here" (4 words)'), encoding="utf-8")
    (d / "art.txt").write_text("some text with fixture quote words here inside\n", encoding="utf-8")


ADMIT = ["--admit-ids", "S900", "--entries", "corpus/knowledge/x.md", "--access-date", "2026-10-25"]


def b_s01(d):
    sfiles(d)
    squote(d)
    return ["--quote-file", str(d / "q.md"), "--artifact", str(d / "art.txt"), "--registry", str(d / "reg.md")]


def b_s02(d):
    return []


def b_s03(d):
    sfiles(d)
    return ["--registry", str(d / "reg.md"), "--package", str(d / "pkg.md"), "--admit-ids", "S900",
            "--entries", "corpus/knowledge/x.md", "--access-date", "2026/10/25"]


def b_s04(d):
    sfiles(d)
    (d / "m.json").write_text("{}\n", encoding="utf-8")
    return ["--registry", str(d / "reg.md"), "--package", str(d / "pkg.md"), "--url-map", str(d / "m.json")]


def b_s05(d):
    sfiles(d)
    return ["--registry", str(d / "reg.md"), "--package", str(d / "pkg.md"), "--admit-ids", "S900",
            "--access-date", "2026-10-25"]


def b_s06(d):
    sfiles(d)
    return ["--registry", str(d / "reg.md"), "--package", str(d / "pkg.md")] + ADMIT + ["--recheck", "soon"]


def b_s07(d):
    sfiles(d, reg_rows=row())
    return ["--registry", str(d / "reg.md"), "--package", str(d / "pkg.md")] + ADMIT


def b_s08(d):
    squote(d)
    return ["--quote-file", str(d / "q.md")]


def b_s09(d):
    squote(d)
    return ["--quote-file", str(d / "q.md"), "--artifact", str(d / "art.txt"),
            "--url-map", str(d / "absent.json")]


def b_s11(d):
    sfiles(d, pkg_rows=row(status="queued"))
    return ["--registry", str(d / "reg.md"), "--package", str(d / "pkg.md")] + ADMIT


for mid, exp, b in [("S01", 2, b_s01), ("S02", 2, b_s02), ("S03", 2, b_s03), ("S04", 2, b_s04),
                    ("S05", 2, b_s05), ("S06", 2, b_s06), ("S07", 3, b_s07), ("S08", 2, b_s08),
                    ("S09", 2, b_s09), ("S11", 5, b_s11)]:
    fx(mid, "sources", exp, "-", b)


def variants():
    src = {t: (LANE / p).read_text(encoding="utf-8") for t, p in c1.TOOLS.items()}
    out = {}
    for mid, tool, cls, direction, adv_kind, label, witness, old, new in c1.MUTANTS:
        text = src[tool]
        n = text.count(old)
        if n != 1:
            out[mid] = ("BADOLD", n, None)
            continue
        vdir = S / "var" / mid
        vdir.mkdir(parents=True, exist_ok=True)
        p = vdir / pathlib.Path(c1.TOOLS[tool]).name
        p.write_text(text.replace(old, new, 1), encoding="utf-8")
        out[mid] = ("ok", n, p)
    return out


def direction_ok(cls, direction, expect, ref_rc, ref_out, mut_rc, mut_out, tool):
    if c1.PAIR.match(direction):
        a, b = (int(x) for x in direction.split(">"))
        return ref_rc == a and mut_rc == b
    ref_cls = c1.classes(tool, ref_out)
    mut_cls = c1.classes(tool, mut_out)
    if direction == "silence":
        return (cls in ref_cls) and (cls not in mut_cls)
    if direction == "rc-silence":
        return ref_rc == 1 and mut_rc == 0
    if direction == "rc-mirror":
        return ref_rc == 0 and mut_rc == 1
    if direction == "error":
        return ref_rc == 2 and mut_rc in (0, 1)
    return False


def main():
    S.mkdir(parents=True, exist_ok=True)
    var = variants()
    rows = []
    for rec in REC:
        mid = rec["mid"]
        status, n, vpath = var[mid]
        d = S / "fx" / mid
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        argv_tail = rec["build"](d)
        tool_path = LANE / c1.TOOLS[rec["tool"]]
        env = dict(BASE_ENV, TMPDIR=str(d / "tmp"))
        (d / "tmp").mkdir(exist_ok=True)
        ref = subprocess.run(["/usr/bin/python3", str(tool_path), *argv_tail], cwd=str(d), env=env,
                             capture_output=True, text=True, timeout=300)
        if status != "ok":
            rows.append({"mid": mid, "error": f"old-string count={n}"})
            continue
        mut = subprocess.run(["/usr/bin/python3", str(vpath), *argv_tail], cwd=str(d), env=env,
                             capture_output=True, text=True, timeout=300)
        _, tool, cls, direction, adv_kind, *_ = next(m for m in c1.MUTANTS if m[0] == mid)
        got = direction_ok(cls, direction, rec["expect"], ref.returncode, ref.stdout, mut.returncode,
                           mut.stdout, tool)
        tb = [ln for ln in mut.stderr.splitlines() if ln and not ln.startswith("  ")]
        rows.append({
            "mid": mid, "tool": tool, "cls": cls, "dir": direction,
            "ref_rc": ref.returncode, "mut_rc": mut.returncode,
            "ref_cls": sorted(c1.classes(tool, ref.stdout)),
            "mut_cls": sorted(c1.classes(tool, mut.stdout)),
            "direction_ok": got,
            "mut_traceback": "Traceback (most recent call last)" in mut.stderr,
            "mut_exc": tb[-1][:160] if tb else "",
        })
    print(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
