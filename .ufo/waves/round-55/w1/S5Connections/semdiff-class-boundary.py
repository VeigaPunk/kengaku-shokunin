"""r55 S5Connections — class-boundary probe: r45 line-split MEMBERSHIP vs r55 full-MULTISET EQUALITY.

Both predicate bodies are transcribed from the committed captures:
  r45  corpus/evidence/round45/tb2-password-recovery/tests/test_outputs.py:14,18
       guesses = Path(...).read_text().strip().split("\n"); CONST in guesses
  r55  corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py:23,25
       move = Path("/app/move.txt").read_text().strip().split()
       assert sorted(move) == sorted(["g2g4", "e2e4"])

To compare the two predicate SHAPES on identical bytes, r45's constant is replaced by the
same literal r55 uses ("g2g4"); only the shape differs. The r55 side is the real predicate.
"""
import unicodedata

def r45_shape(text, const="g2g4"):
    # read_text() translates \r\n and lone \r to \n (universal newlines); then split("\n").
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return const in text.strip().split("\n")

def r55_real(text):
    return sorted(text.strip().split()) == sorted(["g2g4", "e2e4"])

CASES = [
    ("both moves, one per line",   "g2g4\ne2e4\n",        "P"),
    ("both moves, reversed order", "e2e4\ng2g4\n",        "P"),
    ("both moves, one line space", "g2g4 e2e4\n",         "P"),
    ("both moves, one line tab",   "g2g4\te2e4\n",        "P"),
    ("both moves, NBSP separated", "g2g4\u00a0e2e4\n",    "P"),
    ("both moves, CRLF",           "g2g4\r\ne2e4\r\n",    "P"),
    ("both moves, padded",         "  g2g4   e2e4  \n\n", "P"),
    ("PARTIAL: only g2g4",         "g2g4\n",              "F"),
    ("PARTIAL: only e2e4",         "e2e4\n",              "F"),
    ("EXTRA decoy token",          "g2g4\ne2e4\na2a3\n", "F"),
    ("DUPLICATE winner",           "g2g4\ne2e4\ne2e4\n",  "F"),
    ("UPPERCASE token",            "G2G4\ne2e4\n",        "F"),
    ("FULLWIDTH digit",            "g\uFF12g4\ne2e4\n",   "F"),
    ("JOINED on one line",         "g2g4e2e4\n",          "F"),
    ("EMPTY file",                 "",                    "F"),
    ("instruction example h1h8",   "h1h8\ne2e4\n",        "F"),
]

print(f"{'case':<28}{'r45 shape':>11}{'r55 real':>10}   r55 pred  verdict")
bad = 0
for name, text, pred in CASES:
    a, b = r45_shape(text), r55_real(text)
    ok = (b == (pred == "P"))
    if not ok: bad += 1
    print(f"{name:<28}{str(a):>11}{str(b):>10}   {pred:^8}  {'OK' if ok else 'MISMATCH'}")

print(f"\nr55 predictions reproduced: {len(CASES)-bad}/{len(CASES)}  (mismatches={bad})")
print(f"shapes disagree on {sum(1 for n,t,p in CASES if r45_shape(t) != r55_real(t))}/{len(CASES)} cases")

print("\n-- the two relations are incomparable (witnesses on identical bytes) --")
for label, t in [("A 'g2g4 e2e4'", "g2g4 e2e4"),
                 ("B 'g2g4\\nnope\\n'", "g2g4\nnope\n")]:
    print(f"  {label:<18} r45-shape={r45_shape(t)!s:<6} r55-real={r55_real(t)}")

print("\n-- normalization surface --")
ws = [c for c in map(chr, range(0x110000)) if c.isspace()]
print(f"  r55 split(): splits on any of {len(ws)} Unicode whitespace code points "
      f"(incl. U+00A0, U+3000); r45 split('\\n'): only U+000A (after universal-newline translation)")
print(f"  r55 case folding: none (str.upper never applied); digit-width folding: none "
      f"(U+FF12 != '2'); unicode normalization: none (raw str equality)")
print(f"  r45 newline handling: read_text() universal newlines, so lone \\r also separates lines")
print(f"  r45 tokenization is LINE-based (split('\\n')); r55 tokenization is TOKEN-based (split())")

print("\n-- multiplicity --")
print("  r55 compares sorted LISTS: a duplicate adds an element -> equality breaks")
print("  r45 membership ignores multiplicity entirely: the same line 1000 times still passes")
