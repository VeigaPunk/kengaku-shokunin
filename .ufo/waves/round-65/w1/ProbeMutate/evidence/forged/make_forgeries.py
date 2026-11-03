#!/usr/bin/env python3
"""Generate forged receipts from the REAL receipt for the weakening mutants.

Each forgery is one targeted substitution with an occurrence assertion, so the
fixture differs from the receipt of record in exactly the lines named.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
REAL = ROOT / "orig" / "sqlite-gcov-probe.txt"
OUT = ROOT / "forged"
OUT.mkdir(parents=True, exist_ok=True)
text = REAL.read_text(encoding="utf-8")


def sub_one(text, old, new, label):
    count = text.count(old)
    if count != 1:
        sys.exit("FIXTURE-ERROR %s: %d occurrences of %r" % (label, count, old))
    return text.replace(old, new)


# F1: G2 leg-2 fragment replaced by "ok" on BOTH the FRAGMENT line and the LEG line.
f1 = sub_one(text, "FRAGMENT G2 leg2=sqlite3 not found in PATH",
             "FRAGMENT G2 leg2=ok", "f1-fragment-line")
f1 = sub_one(f1,
             "LEG G2 2 test_sqlite_in_path F exc=AssertionError frag=sqlite3 not found in PATH",
             "LEG G2 2 test_sqlite_in_path F exc=AssertionError frag=ok", "f1-leg-line")
(OUT / "forged-g2-fragment.txt").write_text(f1, encoding="utf-8")

# F2: G2 leg 1 verdict flipped P in the LEG row only; VECTOR/CASE lines stay frozen.
f2 = sub_one(text,
             "LEG G2 1 test_sqlite_compiled F exc=PermissionError frag=[Errno 13] Permission denied: 'sqlite3'",
             "LEG G2 1 test_sqlite_compiled P exc=- frag=-", "f2-leg-row")
(OUT / "forged-legrow.txt").write_text(f2, encoding="utf-8")

# F3: stored predicate line says fail although every other field is pristine.
f3 = sub_one(text, "PREDICATE R65-C1 pass", "PREDICATE R65-C1 fail", "f3-predicate")
(OUT / "forged-predicate-fail.txt").write_text(f3, encoding="utf-8")

# F4: the per-case no-bind observation for G3 is dropped.
f4 = sub_one(text, "NOBIND G3 listeners_before=35 listeners_after=35 delta=0\n",
             "", "f4-nobind-g3")
(OUT / "forged-nobind-g3.txt").write_text(f4, encoding="utf-8")

# F5: only the LEG G2 2 fragment field is replaced by "ok"; FRAGMENT line intact.
f5 = sub_one(text,
             "LEG G2 2 test_sqlite_in_path F exc=AssertionError frag=sqlite3 not found in PATH",
             "LEG G2 2 test_sqlite_in_path F exc=AssertionError frag=ok", "f5-leg-frag")
(OUT / "forged-legfrag-only.txt").write_text(f5, encoding="utf-8")

print("wrote", *(str(p) for p in sorted(OUT.iterdir())))
