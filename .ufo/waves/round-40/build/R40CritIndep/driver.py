#!/usr/bin/env python3
"""R40CritIndep: independent recompute of the 28 frozen db-wal-probe cases + 4 own cases.

INDEP = my own prediction of the seven test letters, derived from
corpus/evidence/round40/tb2-db-wal-recovery/test_outputs.py (read once, in full) and the
case requirement text only.  The probe module is imported for its sandbox plumbing
(run_case / mk / Case / TESTS) and its CASES list (ids + recipes); its `predicted`
field is never consulted for agreement -- agreement is INDEP vs the receipt file, and
INDEP vs my own observed run.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import sys
import tempfile

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r40/R40CritIndep")
LANE = S / "lane"
RECEIPT = LANE / "corpus/evidence/round40/db-wal-probe.txt"

spec = importlib.util.spec_from_file_location("dbw", S / "crit_probe.py")
dbw = importlib.util.module_from_spec(spec)
sys.modules["dbw"] = dbw          # py3.14 dataclasses need the module registered
spec.loader.exec_module(dbw)

# --- my independent prediction, per case id (derived before running anything) -------
INDEP = {
    "empty-app": "FFFFFFF",                 # no json -> exists F, six FileNotFoundError
    "untouched": "FFFFFFF",
    "oracle-solve-sh": "PPPPPPP",            # oracle decrypts 0x42 + extracts 11 rows
    "base-only-ro": "PPPPFPF",               # 5 rows: completeness len!=11, wal len>5 F
    "plain-read-then-solve": "PPPPFPF",      # rw open drops the bad WAL, oracle recovers 5
    "xor-wrong-key": "PPPPFPF",              # header 367e0783 != 377f06 82/83 -> ignored
    "decrypt-then-extract": "PPPPPPP",
    "decrypt-checkpoint-truncate": "PPPPPPP",
    "decrypt-in-place-no-json": "FFFFFFF",
    "literals-never-open-db": "PPPPPPP",     # grader never opens the db
    "literals-names-1-2-wrong": "PPPPPPP",   # names of ids 1-2 unpinned
    "literals-id3-name-wrong": "PPPPFPP",    # id 3 name IS pinned
    "truth-value-float-id1": "PPFPPPP",      # isinstance(150.0,int) F; 150.0==150 P
    "truth-reversed-order": "PPPFFPP",       # sorted F; ids != 1..11 F
    "truth-plus-duplicate-id11": "PPPPFFP",  # len 12 F; dup F
    "truth-dup-id10-no-id11": "PPPPFFP",     # len 11 but ids != 1..11 F; dup F
    "truth-extra-field": "PPPPPPP",          # issubset, not equality
    "truth-wrapped-object": "PFFFFFF",       # dict: not list; iterating gives keys
    "truth-ids-as-strings": "PPFFFPP",       # id str F; lexicographic sort F; ids F
    "truth-ids-as-floats": "PPFPPPP",        # isinstance float F; 1.0==1 everywhere else
    "truth-trailing-garbage": "PFFFFFF",     # JSONDecodeError
    "truth-wrong-path": "FFFFFFF",
    "empty-list": "PFPPFPF",                 # len>0 F; loop vacuous P; sorted P; len==11 F
    "truth-drop-id11": "PPPPFPP",
    "truth-value-id3-wrong": "PPPPPPP",      # values of ids 3-11 unpinned
    "truth-bool-value-id5": "PPPPPPP",       # isinstance(True,int) P; value 5 unpinned
    "truth-name-null-id1": "PPFPPPP",        # name str F; name of id 1 unpinned elsewhere
    "truth-value-string-id4": "PPFPPPP",     # value int F; value 4 unpinned
}

# --- my own extra cases: ground truth recomputed from the captures, not from the probe
TRUTH = [{"id": i, "name": n, "value": v} for i, n, v in zip(
    range(1, 12),
    ("apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi",
     "lemon", "mango"),
    (150, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1100))]

HEAD = f"import json\nT = {TRUTH!r}\n"

GEN = "cat > /app/gen.py <<'PY'\n{body}\nPY\npython3 /app/gen.py\n"


def recipe(body, pre="", post=""):
    return pre + GEN.format(body=body) + post


EXTRAS = [
    dbw.Case("x1-bool-id1", recipe(HEAD + 'T[0]["id"] = True\n'
                                   'open("/app/recovered.json", "w").write(json.dumps(T))\n'),
             "PPPPPPP", (),
             "EXTRA: truth with id of the first row written as JSON true (bool is int in Python)"),
    dbw.Case("x2-nan-value-id1", recipe(HEAD + 'T[0]["value"] = float("nan")\n'
                                        'open("/app/recovered.json", "w").write(json.dumps(T))\n'),
             "PPFPFPF", ("record-format", "extract-all"),
             "EXTRA: truth with id 1's value written as NaN (json.dumps emits the NaN literal)"),
    dbw.Case("x3-symlink-recovered",
             recipe(HEAD + 'open("/app/out/recovered.json", "w").write(json.dumps(T))\n',
                    pre="mkdir -p /app/out\n", post="ln -s /app/out/recovered.json /app/recovered.json\n"),
             "PPPPPPP", ("json-at-path",),
             "EXTRA: truth at /app/out/recovered.json with /app/recovered.json a symlink to it"),
    dbw.Case("x4-bom-truth",
             recipe(HEAD + 'open("/app/recovered.json", "wb").write('
                           'b"\\xef\\xbb\\xbf" + json.dumps(T).encode())\n'),
             "PFFFFFF", ("json-at-path",),
             "EXTRA: truth prefixed with a UTF-8 BOM (json.load does not strip it)"),
]


def letters_of(out, tag):
    got, errs = {}, {}
    for line in out.splitlines():
        p = line.split()
        if len(p) >= 3 and p[0] == tag and p[1] in dbw.TESTS:
            got[p[1]] = p[2]
            errs[p[1]] = p[3] if len(p) > 3 else ""
    return "".join(got[t] for t in dbw.TESTS if t in got), errs


def receipt_table():
    table = {}
    for line in RECEIPT.read_text().splitlines():
        m = re.match(r"CASE (\S+) predicted=\S+ observed=\S+ tests=(\S+)", line)
        if m:
            table[m.group(1)] = m.group(2)
    return table


def main():
    rec = receipt_table()
    cap = LANE / dbw.CAP
    for name, digest in dbw.PINS.items():
        if dbw.sha256(cap / name) != digest:
            print("SETUP capture mismatch", name, file=sys.stderr)
            return 2
    root = pathlib.Path(tempfile.mkdtemp(prefix="crit-", dir=str(S)))
    agree_indep_obs = agree_indep_rec = agree_obs_rec = 0
    total = 0
    rows = []
    for case in list(dbw.CASES) + EXTRAS:
        rc, out = dbw.run_case(cap, root, case, "grade")
        got, errs = letters_of(out, "TEST")
        again, _ = letters_of(out, "REGRADE")
        if rc != 0 or len(got) != len(dbw.TESTS):
            print(f"CASE {case.cid} SETUP-FAILURE rc={rc}")
            print(out, file=sys.stderr)
            continue
        mine = INDEP.get(case.cid, case.predicted)
        e = ",".join(f"{t}:{errs[t]}" for t in dbw.TESTS if errs.get(t))
        obs_overall = "pass" if got == "P" * 7 else "fail"
        tag = "EXTRA" if case in EXTRAS else "CASE"
        r = rec.get(case.cid)
        print(f"{tag} {case.cid} indep={mine} observed={got} agree={'yes' if mine == got else 'NO'}"
              f" receipt={r or '-'} receipt_agree={'yes' if r == got else ('NO' if r else '-')}"
              f" regrade={'same' if again == got else 'DIFF:' + again}"
              f" overall={obs_overall}{' ' + e if e else ''} -- {case.requirement}")
        if case not in EXTRAS:
            total += 1
            agree_indep_obs += mine == got
            agree_indep_rec += mine == r
            agree_obs_rec += got == r
        rows.append((case.cid, mine, got, r))
    print(f"indep_vs_observed {agree_indep_obs}/{total} indep_vs_receipt {agree_indep_rec}/{total}"
          f" observed_vs_receipt {agree_obs_rec}/{total}")
    print("recompute of the grader's pinned cells: ids 11 + values 2 + names 9 = %d of 33"
          % (11 + 2 + 9))
    return 0 if agree_indep_obs == total == agree_indep_rec == agree_obs_rec else 1


if __name__ == "__main__":
    sys.exit(main())
