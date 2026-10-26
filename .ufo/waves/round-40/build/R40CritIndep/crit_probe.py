#!/usr/bin/env python3
"""Round-40 C2 probe: the pinned Terminal-Bench 2.0 `db-wal-recovery` grader, executed offline.

  python3 plans/db_wal_probe.py --lane .                run every frozen case, print the receipt
  python3 plans/db_wal_probe.py --lane . --dry          print the frozen case table only (no sandbox)
  python3 plans/db_wal_probe.py --lane . --stage-check  build every case's end state in the sandbox and
                                                        print only the stage exit codes; the grader is
                                                        never imported

What runs: the captured grader `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88, digest checked before any
case) inside a bubblewrap sandbox per case: private network/pid/ipc namespaces, /usr and /etc read-only, /tmp
private, /app a fresh writable directory, /cap holding only the captures the probe executes (test_outputs.py,
solve.sh), /k holding the probe's own helper `mk.py`, cwd /app, HOME=/tmp. Per case the probe first seeds /app as
the task Dockerfile does (`COPY main.db /app/main.db`, `COPY main.db-wal.encrypted /app/main.db-wal`; skipped for
`empty-app` only), the sandbox runs the case recipe under `bash -euo pipefail`, then imports the grader and calls
its seven test functions in file order: an AssertionError is `F`, any other exception is `F` with its class
named, a return is `P`. A case's verdict is `pass` iff all seven are `P` (pytest exits 0 iff no test fails;
tests/test.sh writes reward 1 iff pytest exits 0). A recipe that exits non-zero is a probe error (exit 2), never
a verdict.

Re-run stability (considerthese/2026-10-26.md proposal 3, the rider `R39PlanNext` §4 priced): after the first
grading the harness grades the SAME end state a second time, without rebuilding it, and the CASE line carries
`regrade=same` or `regrade=DIFF:<letters>`. The second grading is reported, never used for the verdict.

Ground truth (computed from the two captured files, not from the grader): XOR-decrypting `main.db-wal.encrypted`
with key 0x42 and reading `items` gives 11 rows, id 1..11, names apple banana cherry date elderberry fig grape
honeydew kiwi lemon mango, value 100*id except id 1 -> 150 and id 2 -> 250; the base database alone holds ids 1..5
with values 100..500. `TRUTH` below is that table; `mk.py` writes variants of it to stand in for an agent's
output without opening the database (the `literals-*` and `truth-*` cases).

Each case names the instruction requirements it violates (`violates=` tags, see TAGS), frozen with the
predictions; the entry's requirement map is derived from them and from the observed verdicts (round-38 Q28).

Predictions: written from a static reading of tests/test_outputs.py and instruction.md before the first recorded
run of this probe, EXCEPT the rows the round-39 planning seat already observed on this host
(`.ufo/waves/round-39/build/R39PlanNext/dbwal/run1.txt`): `untouched` (nop), `oracle-solve-sh`, `base-only-ro`,
`literals-never-open-db`, `literals-names-1-2-wrong`, `literals-id3-name-wrong`, `truth-value-float-id1`
(value-float) copy that pilot's verdicts. `plain-read-then-solve` rests on the same seat's measurement that a
plain `sqlite3 /app/main.db` read deletes the encrypted WAL (R39PlanNext.md §3.2); its grading was never run.

Limits, stated before the first run: host sqlite3 3.54.0, python3 and xxd stand in for the task image's Ubuntu
24.04 packages; the task image is never pulled; recipes run as the probing user, not root. This is a probe of
the grader on constructed end states, not of any agent.

Deterministic receipt: no temp path, timing or host version is printed. Scratch lives under --work (created if
absent), else $TMPDIR (tempfile default), and is removed on exit.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round40/tb2-db-wal-recovery"
PINS = {
    "test_outputs.py": "88dc5c2a3abba75bca0e0f9136223ae5bb585d5984b8d9eba51a7829c1d2ba49",
    "solve.sh": "ed8530c94103bf19783a1d41bc63fe4db478cdd9629f22fee25c45a45699f5e8",
    "main.db": "68cb288eb29e76d814b4e7ee6887b37c415675e644f88173bc191348e290d119",
    "main.db-wal.encrypted": "68753bdce26196a53194260d001544cc6bb8f9f38e2f2f6826d09798e31e6e26",
}
BWRAP = "/usr/bin/bwrap"
TOOLS = ("/usr/bin/sqlite3", "/usr/bin/xxd", "/usr/bin/python3")
TESTS = ("test_recovered_json_exists", "test_recovered_json_is_valid", "test_recovered_data_structure",
         "test_recovered_data_sorted", "test_recovered_data_completeness", "test_no_duplicate_ids",
         "test_wal_was_decrypted")
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Instruction requirements (instruction.md line -> tag). A case violates a tag when its end state does not do
# what the instruction asks under that tag, whatever the grader says.
TAGS = {
    "fix-wal": "instruction.md:7",          # fix the WAL file so SQLite can read it
    "extract-all": "instruction.md:8",      # extract ALL data from the database (including WAL changes)
    "json-at-path": "instruction.md:9",     # create a JSON file in /app/recovered.json
    "record-format": "instruction.md:12",   # [{"id": 1, "name": "item1", "value": X}, ...]
    "sorted-by-id": "instruction.md:13",    # sorted by id
    "eleven-records": "instruction.md:13",  # recover all 11 records total
}

NAMES = ("apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon", "mango")
TRUTH = [{"id": i, "name": NAMES[i - 1], "value": {1: 150, 2: 250}.get(i, 100 * i)} for i in range(1, 12)]

MK_PY = r'''
import json, sys
TRUTH = %r
v = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "/app/recovered.json"
rows = [dict(r) for r in TRUTH]
tail = ""
if v == "literals-never-open-db":
    rows = [{"id": r["id"], "name": r["name"], "value": {1: 150, 2: 250}.get(r["id"], 0)} for r in rows]
elif v == "literals-names-1-2-wrong":
    rows = [{"id": r["id"], "name": {1: "x", 2: "y"}.get(r["id"], r["name"]), "value": {1: 150, 2: 250}.get(r["id"], 0)}
            for r in rows]
elif v == "literals-id3-name-wrong":
    rows = [{"id": r["id"], "name": "CHERRY" if r["id"] == 3 else r["name"], "value": {1: 150, 2: 250}.get(r["id"], 0)}
            for r in rows]
elif v == "value-float-id1":
    rows[0]["value"] = 150.0
elif v == "reversed":
    rows = rows[::-1]
elif v == "plus-duplicate-id11":
    rows = rows + [dict(rows[-1])]
elif v == "dup-id10-no-id11":
    rows = rows[:10] + [dict(rows[9])]
elif v == "extra-field":
    rows = [dict(r, note="recovered") for r in rows]
elif v == "wrapped-object":
    rows = {"items": rows}
elif v == "ids-as-strings":
    rows = [dict(r, id=str(r["id"])) for r in rows]
elif v == "ids-as-floats":
    rows = [dict(r, id=float(r["id"])) for r in rows]
elif v == "trailing-garbage":
    tail = "\nEOF\n"
elif v == "empty-list":
    rows = []
elif v == "drop-id11":
    rows = rows[:10]
elif v == "value-id3-wrong":
    rows[2]["value"] = 301
elif v == "bool-value-id5":
    rows[4]["value"] = True
elif v == "name-null-id1":
    rows[0]["name"] = None
elif v == "value-string-id4":
    rows[3]["value"] = "400"
elif v != "truth":
    sys.exit("unknown variant " + v)
with open(out, "w") as f:
    f.write(json.dumps(rows) + tail)
''' % (TRUTH,)

DECRYPT = ("python3 -c 'import sys; d=open(\"/app/main.db-wal\",\"rb\").read(); "
           "open(\"/app/main.db-wal\",\"wb\").write(bytes(b ^ int(sys.argv[1], 16) for b in d))' {key}")
EXTRACT = ("python3 -c 'import sqlite3, json; c=sqlite3.connect(\"{uri}\", uri=True); "
           "rows=[{{\"id\": a, \"name\": b, \"value\": v}} for a, b, v in "
           "c.execute(\"SELECT id, name, value FROM items ORDER BY id\")]; "
           "json.dump(rows, open(\"/app/recovered.json\", \"w\"))'")
RW = "file:/app/main.db"
RO = "file:/app/main.db?mode=ro"


@dataclasses.dataclass(frozen=True)
class Case:
    cid: str
    recipe: str                     # bash, run in /app after the seeding
    predicted: str                  # seven letters P/F in TESTS order
    violates: tuple                 # TAGS keys
    requirement: str
    seed: bool = True               # seed /app/main.db and /app/main.db-wal first


def r(*steps):
    return "\n".join(steps) + "\n"


def mk(variant, out=None):
    return f"python3 /k/mk.py {variant}" + (f" {out}" if out else "")


CASES = [
    Case("empty-app", "true\n", "FFFFFFF", ("extract-all", "json-at-path", "eleven-records"),
         "do-nothing on an empty /app: no database, no recovered.json", seed=False),
    Case("untouched", "true\n", "FFFFFFF", ("fix-wal", "extract-all", "json-at-path", "eleven-records"),
         "do-nothing on the task's initial state (pilot nop)"),
    Case("oracle-solve-sh", "bash /cap/solve.sh >/dev/null 2>&1\n", "PPPPPPP", (),
         "the task's own solution/solve.sh (pilot oracle)"),
    Case("base-only-ro", r(EXTRACT.format(uri=RO)), "PPPPFPF", ("fix-wal", "extract-all", "eleven-records"),
         "read the base database read-only, WAL left encrypted: the 5 base rows with base values (pilot base-only)"),
    Case("plain-read-then-solve", r("sqlite3 /app/main.db 'SELECT count(*) FROM items;' >/dev/null",
                                    "bash /cap/solve.sh >/dev/null 2>&1"),
         "PPPPFPF", ("fix-wal", "extract-all", "eleven-records"),
         "a plain read-write sqlite3 query first (R39PlanNext: it deletes the encrypted WAL), then the task's own "
         "solve.sh: nothing left to decrypt, 5 base rows"),
    Case("xor-wrong-key", r(DECRYPT.format(key="43"), EXTRACT.format(uri=RW)), "PPPPFPF",
         ("fix-wal", "extract-all", "eleven-records"),
         "XOR with the wrong single-byte key 0x43: the WAL magic stays invalid, SQLite ignores it, 5 base rows"),
    Case("decrypt-then-extract", r(DECRYPT.format(key="42"), EXTRACT.format(uri=RW)), "PPPPPPP", (),
         "an own pipeline: XOR 0x42 in place, then read every row with the WAL applied"),
    Case("decrypt-checkpoint-truncate", r(DECRYPT.format(key="42"),
                                          "sqlite3 /app/main.db 'PRAGMA wal_checkpoint(TRUNCATE);' >/dev/null",
                                          EXTRACT.format(uri=RW)), "PPPPPPP", (),
         "XOR 0x42, checkpoint the WAL into main.db, then read every row"),
    Case("decrypt-in-place-no-json", r(DECRYPT.format(key="42")), "FFFFFFF",
         ("extract-all", "json-at-path", "eleven-records"),
         "the WAL fixed in place, no recovered.json written"),
    Case("literals-never-open-db", r(mk("literals-never-open-db")), "PPPPPPP", ("fix-wal", "extract-all"),
         "hand-typed JSON: right names, values 150/250 for ids 1-2 and 0 for ids 3-11, database never opened "
         "(pilot typed-literals-never-open-db)"),
    Case("literals-names-1-2-wrong", r(mk("literals-names-1-2-wrong")), "PPPPPPP", ("fix-wal", "extract-all"),
         "as literals-never-open-db with the names of ids 1 and 2 wrong (pilot)"),
    Case("literals-id3-name-wrong", r(mk("literals-id3-name-wrong")), "PPPPFPP", ("fix-wal", "extract-all"),
         "as literals-never-open-db with id 3 named CHERRY (pilot)"),
    Case("truth-value-float-id1", r(mk("value-float-id1")), "PPFPPPP", ("fix-wal", "record-format"),
         "the true rows typed by hand, id 1's value written 150.0 (pilot value-float)"),
    Case("truth-reversed-order", r(mk("reversed")), "PPPFFPP", ("fix-wal", "sorted-by-id"),
         "the true rows in descending id order"),
    Case("truth-plus-duplicate-id11", r(mk("plus-duplicate-id11")), "PPPPFFP", ("fix-wal", "eleven-records"),
         "the true rows plus a second copy of id 11 (12 records)"),
    Case("truth-dup-id10-no-id11", r(mk("dup-id10-no-id11")), "PPPPFFP", ("fix-wal", "extract-all", "eleven-records"),
         "11 records: ids 1-10 and a second id 10, mango missing"),
    Case("truth-extra-field", r(mk("extra-field")), "PPPPPPP", ("fix-wal", "record-format"),
         "the true rows, each with an extra `note` key the format does not show"),
    Case("truth-wrapped-object", r(mk("wrapped-object")), "PFFFFFF", ("fix-wal", "record-format"),
         "the true rows wrapped in an object {\"items\": [...]} instead of a list"),
    Case("truth-ids-as-strings", r(mk("ids-as-strings")), "PPFFFPP", ("fix-wal", "record-format"),
         "the true rows with ids written as strings \"1\"..\"11\""),
    Case("truth-ids-as-floats", r(mk("ids-as-floats")), "PPFPPPP", ("fix-wal", "record-format"),
         "the true rows with ids written as floats 1.0..11.0 (1.0 == 1 in the completeness test)"),
    Case("truth-trailing-garbage", r(mk("trailing-garbage")), "PFFFFFF", ("fix-wal", "json-at-path"),
         "the true rows followed by a line of text: not a JSON file"),
    Case("truth-wrong-path", r("mkdir /app/out", mk("truth", "/app/out/recovered.json")), "FFFFFFF",
         ("fix-wal", "json-at-path"), "the true rows written to /app/out/recovered.json"),
    Case("empty-list", r(mk("empty-list")), "PFPPFPF", ("fix-wal", "extract-all", "eleven-records"),
         "recovered.json is []"),
    Case("truth-drop-id11", r(mk("drop-id11")), "PPPPFPP", ("fix-wal", "extract-all", "eleven-records"),
         "the true rows without mango (10 records)"),
    Case("truth-value-id3-wrong", r(mk("value-id3-wrong")), "PPPPPPP", ("fix-wal", "extract-all"),
         "the true rows with id 3's value 301 instead of 300"),
    Case("truth-bool-value-id5", r(mk("bool-value-id5")), "PPPPPPP", ("fix-wal", "extract-all", "record-format"),
         "the true rows with id 5's value true (isinstance(True, int) holds)"),
    Case("truth-name-null-id1", r(mk("name-null-id1")), "PPFPPPP", ("fix-wal", "extract-all", "record-format"),
         "the true rows with id 1's name null"),
    Case("truth-value-string-id4", r(mk("value-string-id4")), "PPFPPPP", ("fix-wal", "record-format"),
         "the true rows with id 4's value the string \"400\""),
]

HARNESS_PY = r'''
import importlib.util, subprocess, sys
mode = sys.argv[1]
rc = subprocess.run(["bash", "-euo", "pipefail", "/recipe.sh"], cwd="/app", stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
print("STAGE recipe rc=" + str(rc))
if rc or mode == "stage":
    sys.exit(3 if rc else 0)
spec = importlib.util.spec_from_file_location("tb2_db_wal_grader", "/cap/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for tag in ("TEST", "REGRADE"):
    for name in %r:
        try:
            getattr(mod, name)()
            print(tag + " " + name + " P")
        except AssertionError:
            print(tag + " " + name + " F")
        except Exception as e:
            print(tag + " " + name + " F error=" + type(e).__name__)
''' % (TESTS,)


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sandbox_argv(cap, work):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--bind", str(work / "app"), "/app", "--dir", "/cap", "--dir", "/k"]
    for name in ("test_outputs.py", "solve.sh"):
        argv += ["--ro-bind", str(cap / name), f"/cap/{name}"]
    argv += ["--ro-bind", str(work / "mk.py"), "/k/mk.py",
             "--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
             "--ro-bind", str(work / "harness.py"), "/harness.py", "--chdir", "/app"]
    return argv


def run_case(cap, root, case, mode):
    work = pathlib.Path(tempfile.mkdtemp(prefix="dbw-", dir=root))
    try:
        app = work / "app"
        app.mkdir()
        if case.seed:
            shutil.copyfile(cap / "main.db", app / "main.db")
            shutil.copyfile(cap / "main.db-wal.encrypted", app / "main.db-wal")
        (work / "recipe.sh").write_text(case.recipe)
        (work / "harness.py").write_text(HARNESS_PY)
        (work / "mk.py").write_text(MK_PY)
        env = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
               "PYTHONDONTWRITEBYTECODE": "1"}
        p = subprocess.run(sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py", mode],
                           env=env, capture_output=True, text=True, timeout=300)
        return p.returncode, p.stdout
    finally:
        shutil.rmtree(work, ignore_errors=True)


def overall(letters):
    return "pass" if letters == "P" * len(TESTS) else "fail"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    mx = ap.add_mutually_exclusive_group()
    mx.add_argument("--dry", action="store_true")
    mx.add_argument("--stage-check", action="store_true")
    ap.add_argument("--work", default=None, help="scratch parent, created if absent (default: $TMPDIR)")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    cap = lane / CAP
    ids = [c.cid for c in CASES]
    if len(set(ids)) != len(ids) or any(t not in TAGS for c in CASES for t in c.violates) \
            or any(len(c.predicted) != len(TESTS) or set(c.predicted) - {"P", "F"} for c in CASES):
        print("SETUP duplicate case id, unknown tag or malformed prediction", file=sys.stderr)
        return 2
    if a.dry:
        for t, loc in TAGS.items():
            print(f"TAG {t} {loc}")
        for c in CASES:
            print(f"CASE {c.cid} predicted={overall(c.predicted)} tests={c.predicted}"
                  f" violates={','.join(c.violates)} -- {c.requirement}")
        print(f"cases={len(CASES)} predicted_pass={sum(overall(c.predicted) == 'pass' for c in CASES)}"
              f" predicted_fail={sum(overall(c.predicted) == 'fail' for c in CASES)}")
        return 0
    for name, digest in PINS.items():
        if not (cap / name).is_file() or sha256(cap / name) != digest:
            print(f"SETUP capture {name} missing or not at its pinned digest", file=sys.stderr)
            return 2
    for tool in (BWRAP,) + TOOLS:
        if not os.access(tool, os.X_OK):
            print(f"SETUP {tool} is required", file=sys.stderr)
            return 2
    if a.work:
        try:
            pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"SETUP --work {a.work} cannot be created: {e.strerror}", file=sys.stderr)
            return 2
    root = pathlib.Path(tempfile.mkdtemp(prefix="k40-dbw-", dir=a.work))
    try:
        if a.stage_check:
            bad = 0
            for c in CASES:
                rc, out = run_case(cap, root, c, "stage")
                stages = " ".join(l.split(" ", 1)[1] for l in out.splitlines() if l.startswith("STAGE "))
                bad += rc != 0
                print(f"STAGECHECK {c.cid} rc={rc} {stages}")
            print(f"stagecheck cases={len(CASES)} failed={bad}")
            return 0 if bad == 0 else 1
        print("# tb2 db-wal-recovery grader probe (kengaku round 40) @ terminal-bench-2 2fd12b88")
        for name in sorted(PINS):
            print(f"# capture {name} sha256={PINS[name]}")
        npass = nfail = mism = rediff = 0
        for c in CASES:
            rc, out = run_case(cap, root, c, "grade")
            got, again = {}, {}
            for l in out.splitlines():
                parts = l.split()
                if len(parts) >= 3 and parts[0] in ("TEST", "REGRADE") and parts[1] in TESTS:
                    (got if parts[0] == "TEST" else again)[parts[1]] = (parts[2], parts[3] if len(parts) > 3 else "")
            if rc != 0 or set(got) != set(TESTS) or set(again) != set(TESTS):
                print(f"SETUP case {c.cid} did not yield seven test verdicts twice (rc={rc})", file=sys.stderr)
                print(out, file=sys.stderr)
                return 2
            letters = "".join(got[t][0] for t in TESTS)
            letters2 = "".join(again[t][0] for t in TESTS)
            errs = ",".join(f"{t}:{got[t][1]}" for t in TESTS if got[t][1])
            obs = overall(letters)
            npass += obs == "pass"
            nfail += obs == "fail"
            match = letters == c.predicted
            mism += not match
            rediff += letters2 != letters
            print(f"CASE {c.cid} predicted={overall(c.predicted)} observed={obs} tests={letters}"
                  f" predicted_tests={c.predicted} match={'yes' if match else 'NO'}"
                  f" regrade={'same' if letters2 == letters else 'DIFF:' + letters2}"
                  f" violates={','.join(c.violates)}{' ' + errs if errs else ''} -- {c.requirement}")
        print(f"regrade cases={len(CASES)} differ={rediff}")
        print(f"cases={len(CASES)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
