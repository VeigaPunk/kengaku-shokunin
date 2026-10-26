"""Hostile hull probe H3: no counter patch, no injected module.  `build` runs once and the same directory
is graded by the reference, by the null copy and by every mutant; a fixture-owned probe executed by P10
(`--rerun`) only needs to tell those runs apart by counting its own invocations.  The tree is healed after
the null run prints, so the reference and the null agree while every mutant is graded on a different tree.
"""

import hashlib
import json

HEAL = ("import pathlib, shutil\n"
        "d = pathlib.Path.cwd().resolve()\n"
        "root = d.parents[1]\n"
        "cf = root / 'h3-count-heal'\n"
        "n = int(cf.read_text()) + 1 if cf.is_file() else 1\n"
        "cf.write_text(str(n))\n"
        "lg = pathlib.Path('/fast/scratch/hyaku/kengaku-r38/R38CritC1Counter/h3heal.log')\n"
        "lg.write_text((lg.read_text() if lg.is_file() else '') + 'heal n=' + str(n) + ' at ' + d.name + chr(10))\n"
        "print('STABLE-PROBE')\n"
        "if n >= 3:\n"
        "    shutil.copytree(root / 'h3-store', d, dirs_exist_ok=True)\n"
        "    r = d / '__RECEIPT__'\n"
        "    r.parent.mkdir(parents=True, exist_ok=True)\n"
        "    r.write_text('STABLE-PROBE' + chr(10))\n")

BREAK = ("import pathlib, re\n"
         "d = pathlib.Path.cwd().resolve()\n"
         "root = d.parents[1]\n"
         "cf = root / 'h3-count-break'\n"
         "n = int(cf.read_text()) + 1 if cf.is_file() else 1\n"
         "cf.write_text(str(n))\n"
         "print('STABLE-PROBE')\n"
         "if n >= 3:\n"
         "    e = d / '__ENTRY__'\n"
         "    t = e.read_text()\n"
         "    m = re.search(r'(?ms)^## Located quotes\\n(.*?)(?=^## |\\Z)', t)\n"
         "    body = [l for l in m.group(1).splitlines() if l.startswith('|')][:2]\n"
         "    e.write_text(t[:m.start(1)] + chr(10).join(body) + chr(10) + chr(10) + t[m.end(1):])\n"
         "    s = d / '__CAPDIR__' / 'SHA256SUMS'\n"
         "    s.write_text(s.read_text() + chr(10))\n"
         "    (d / '__RECEIPT__').write_text('TAMPERED')\n")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def b_heal(ctx, d):
    store = d.parent.parent / "h3-store"
    ctx.r36.copy_package(ctx.lane, ctx.spec, store)
    spec = dict(ctx.spec)
    spec["receipt_sha256"] = sha(b"STABLE-PROBE\n")
    spec["probe_cmd"] = ["-c", HEAL.replace("__RECEIPT__", spec["receipt"])]
    (d / "spec.json").write_text(json.dumps(spec))
    r = d / spec["receipt"]
    r.parent.mkdir(parents=True, exist_ok=True)
    r.write_text("STALE\n")
    return ["package", "--root", str(d), "--spec", str(d / "spec.json"), "--rerun"]


def b_break(ctx, d):
    ctx.genuine_package(d)
    spec = dict(ctx.spec)
    spec["receipt_sha256"] = sha(b"STABLE-PROBE\n")
    spec["probe_cmd"] = ["-c", BREAK.replace("__ENTRY__", spec["entry"])
                         .replace("__CAPDIR__", spec["capture_dir"])
                         .replace("__RECEIPT__", spec["receipt"])]
    (d / "spec.json").write_text(json.dumps(spec))
    (d / spec["receipt"]).write_text("STABLE-PROBE\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--spec", str(d / "spec.json"),
            "--require-clean-tree", "--rerun"]


def line_fixture(fid, spec, filename, body):
    def build(ctx, d):
        (d / "spec.json").write_text(json.dumps(spec))
        if filename:
            (d / "line.txt").write_text(body)
            return None
        return None
    def b(ctx, d):
        (d / "spec.json").write_text(json.dumps(spec))
        (d / "line.txt").write_text(body)
        if "d4" in spec:
            return ["d4-line", "--file", str(d / "line.txt"), "--spec", str(d / "spec.json")]
        cap = d / "cap"
        cap.mkdir()
        (cap / "cap.txt").write_bytes(b"alpha beta gamma delta eel\n")
        (cap / "SHA256SUMS").write_text(sha(b"alpha beta gamma delta eel\n") + "  cap.txt\n")
        return ["d5-line", "--file", str(d / "line.txt"), "--capture-dir", str(cap),
                "--spec", str(d / "spec.json")]
    return {"fid": fid, "expect": "reject", "defects": ["D4" if "d4" in spec else "D5"], "build": b}


def b_main_root(ctx, d):
    (d / "spec.json").write_text(json.dumps(dict(ctx.spec)))
    return ["package", "--root", str(d / "nodir"), "--spec", str(d / "spec.json")]


def b_main_crash(ctx, d):
    (d / "spec.json").write_text("[1, 2]")
    return ["package", "--root", str(d), "--spec", str(d / "spec.json")]


FIXTURES = [
    {"fid": "h3-heal", "expect": "reject",
     "defects": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P10"], "build": b_heal},
    {"fid": "h3-break", "expect": "accept", "defects": [], "build": b_break},
    line_fixture("h3-d4-last", {"d4": {"label": "DIR-R38: ", "patterns": ["[A-Z]{3}", "delta"]}},
                 "line.txt", "DIR-R38: AAA\n"),
    line_fixture("h3-d4-case", {"d4": {"label": "DIR-R38: ", "patterns": ["delta"]}},
                 "line.txt", "DIR-R38: DELTA\n"),
    line_fixture("h3-d5-prefix", {"d5": {"label": "DIR-R38: ", "require": "alpha", "forbid": "zzz",
                                         "capture_name": "cap.txt", "manifest_name": "SHA256SUMS",
                                         "quote": "alpha beta gamma delta epsilon"}},
                 "line.txt", "DIR-R38: alpha\n"),
    {"fid": "h3-main17", "expect": "error", "defects": [], "build": b_main_root},
    {"fid": "h3-main18", "expect": "error", "defects": [], "build": b_main_crash},
]
